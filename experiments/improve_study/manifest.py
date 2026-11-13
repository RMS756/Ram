"""Split manifest and hashes for the improvement study (no outcome is read)."""
import hashlib, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import improve as I
from improve import S, common, build, load_raw, load_fresh, sha_file, REPO


def h(items):
    return hashlib.sha256("\n".join(sorted(items)).encode()).hexdigest()


def main():
    st = common.make_setup()
    data = build("primary", load_raw())
    valid = S.load("fit_aux")["valid"]
    fresh, meta = load_fresh(st, data)
    pil = os.environ["PILOT_RESULTS_DIR"]
    az = os.environ["AUTHZ_STATE"]
    up = os.environ.get("PROGENT_UPSTREAM", "")
    out = {
        "date": "2026-11-13",
        "agentdojo_package": common.provenance()["agentdojo_package"], "agentdojo_runs_commit": common.provenance()["agentdojo_runs_commit"],
        "config_sha256": common.provenance()["config_sha256"],
        "primary": {"episodes_loaded": len(data.episodes), "eligible": len(valid), "eligible_ids_sha256": h(valid),
                    "steps": len(data.steps), "folds": sorted(set(map(str, data.fold.tolist()))),
                    "eligible_by_fold": {str(f): sum(1 for e in valid if str(data.episode_fold[e]) == str(f)) for f in sorted(set(map(str, data.fold.tolist())))},
                    "eligible_by_user_task": {u: sum(1 for e in valid if data.episodes[e].user_task_id == u) for u in sorted({ep.user_task_id for ep in data.episodes.values()})}},
        "dev2_formerly_confirmatory": {"episodes_loaded": len(fresh), "loaded_ids_sha256": h(fresh), "by_source": {s: sum(1 for m in meta.values() if m["source"] == s) for s in I.FRESH}},
        "S2_cells": sum(1 for k in S.load("cells") if k[0] == "S2"),
        "state_sha256": {"pilot/steps.pkl": sha_file(os.path.join(pil, "steps.pkl")), "pilot/state/crossfit.pkl": sha_file(os.path.join(pil, "state", "crossfit.pkl")),
                         "pilot/state/rmod.pkl": sha_file(os.path.join(pil, "state", "rmod.pkl")), "authz/cells.pkl": sha_file(os.path.join(az, "cells.pkl")),
                         "authz/cells_posthoc_a2.pkl": sha_file(os.path.join(az, "cells_posthoc_a2.pkl"))},
        "code_sha256": {f: sha_file(os.path.join(HERE, f)) for f in ("intent.py", "permission.py", "improve.py", "progent_manual.py", "verifier.py")},
        "fixtures_sha256": {"set4": sha_file(os.path.join(REPO, "REM_IMPROVEMENT_STUDY", "fixtures", "set4_permission_fixtures.json"))},
        "upstream": {"progent": {"repository": "github.com/sunblaze-ucb/progent", "commit": I.PG.COMMIT, "files_sha256": I.PG.upstream_hashes(up) if up else None},
                     "melon": {"repository": "github.com/kaijiezhu11/MELON", "commit": "4d3cc9c", "status": "not executed"}},
        "verifier_prompt_sha256": __import__("verifier").PROMPT_SHA256,
    }
    p = os.path.join(REPO, "REM_IMPROVEMENT_STUDY", "protocol", "SPLIT_MANIFEST.json")
    json.dump(out, open(p, "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("primary", "dev2_formerly_confirmatory", "S2_cells")}, indent=1)[:900])


if __name__ == "__main__":
    main()
