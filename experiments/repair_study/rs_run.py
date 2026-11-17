"""Repair study of 17 November 2026: replay and report of the repaired arms. No model API call; no refit.

Status: [PROPOSED - EXPLORATORY - DEVELOPMENT EVIDENCE]. See REM_REPAIR_STUDY_2026_11_17/PROTOCOL.md, committed before
any outcome of G3_math, GV_math or HV_math on a cohort was computed.

Stages: replay | report | diagnostics
Environment: the competitive study's (AGENTDOJO_RUNS, PILOT_RESULTS_DIR, INTEGRATION_STATE, PROGENT_UPSTREAM,
COMPETITIVE_STATE). The baselines G3, GV, HV, REM10 and PG are read from the stored replays; they are not re-run.
"""
from __future__ import annotations

import collections
import gzip
import hashlib
import json
import multiprocessing as mp
import pickle
import sys
import time
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
for _p in ("experiments/repair_study", "experiments/competitive_study", "experiments/g3_integration", "experiments/improve_study",
           "experiments/pilot", "REM_AUTHORIZATION_AUDIT/tools"):
    sys.path.insert(0, str(ROOT / _p))

import cs_run as C            # noqa: E402  (populations, stored caches)
import repaired_arms as RA    # noqa: E402

J, S, R, common = C.J, C.S, C.R, C.common
OUT = ROOT / "REM_REPAIR_STUDY_2026_11_17" / "results"
OUT.mkdir(parents=True, exist_ok=True)
STATE = C.STATE
BASELINES = ["REM10", "PG", "G3", "GV", "HV"]
TABLE_ARMS = BASELINES + list(RA.ARMS)
CONTRASTS = [("G3_math", "G3"), ("GV_math", "GV"), ("HV_math", "HV"), ("HV_math", "GV_math"), ("GV_math", "PG"), ("HV_math", "PG"),
             ("GV_math", "G3_math"), ("GV_math", "REM10")]
W = {}


def replay_job(job):
    scheme, role, e, arm = job
    ep = W["eps"][role][e]
    key = ("S1", W["fold"][role][e]) if scheme == "S1" else ("S2", ep.user_task_id, ep.injection_task_id or W["fold"][role][e])
    g = RA.make_guard(arm, W["jcells"][key], W["cs"][key], ep, W["setup"])
    out = S.replay_episode(ep, W["setup"].suite, g)
    audit = [(a["label"], a["verdict"], bool(a["released"]), a["tier"], a["tool"], a["rem_latency_full_ms"], a["verdict_source"],
              a["details"].get("perm") or a["details"].get("permission"), (a["details"].get("cs") or {}).get("stage"),
              a["details"].get("amount"), a["details"].get("stage_before_veto")) for a in out.audit]
    return scheme, role, e, arm, bool(out.utility), bool(out.security), out.error, audit


def stage_replay():
    d, aux, eps, folds = C._populations()
    W.update(setup=common.make_setup(), jcells=J.load("cells"), cs=C.load("cs_cells"), eps=eps, fold=folds)
    jobs = [("S1", role, e, a) for role, pop in eps.items() for a in RA.ARMS for e in sorted(pop)]
    jobs += [("S2", "primary", e, a) for a in RA.FITTED for e in aux["valid"]]
    t = time.time()
    results = []
    with mp.get_context("fork").Pool(4) as p:
        for i, v in enumerate(p.imap_unordered(replay_job, jobs, chunksize=32), 1):
            results.append(v)
            if i % 5000 == 0:
                print("replay", i, "/", len(jobs), "elapsed", round(time.time() - t), "s", flush=True)
    with (STATE / "rs_replays.pkl").open("wb") as f:
        pickle.dump(results, f)
    print("replay done", len(results), round(time.time() - t), "s; errors", sum(1 for r in results if r[6]), flush=True)


# ---------------------------------------------------------------------------------------------------- report
def stage_of(arm, x):
    """Stage that decided a restricted call (x: audit tuple of this study or a stored one)."""
    src = x[6]
    if src.startswith("amount_"):
        return "amount_" + src.split("_", 1)[1]
    if src.startswith("direct_value_"):
        return "value_constraint_refused"
    if src == "permission_guard_authority_v3":
        return "front_blocked"
    if src == "rule_permission_v3":                         # G3: release iff supported
        return "rule_released" if x[2] else "front_blocked"
    if src in ("D1", "D2"):
        return "predicate_" + x[1]
    return "rule_released" if x[2] else "rule_withheld_" + x[1]


def _hash_ids(ids):
    return hashlib.sha256("\n".join(sorted(ids)).encode()).hexdigest()


def fixtures(cells, cs):
    import trace_fixtures as tf
    st = common.make_setup()
    key = ("S1", "injection_task_0")
    paths = ["REM_AUTHORIZATION_AUDIT/fixtures/set1_substitution_fixtures.json", "REM_AUTHORIZATION_AUDIT/fixtures/set2_fresh_fixtures.json",
             "REM_FINAL_SUBMISSION/fixtures/set3_credential_and_reformatting_fixtures.json",
             "REM_IMPROVEMENT_STUDY/fixtures/set4_permission_fixtures.json"]
    result = {}
    for path in paths:
        v = json.loads((ROOT / path).read_text())
        records = v["records"] if isinstance(v, dict) else v
        summary = {}
        for a in RA.ARMS:
            rr = []
            for fx in records:
                fx = dict(fx)
                if "authorized" in fx:
                    fx["legitimate_call"] = {"tool": "send_money", "args": dict(fx["authorized"])}
                    fx["unsafe_call"] = {"tool": "send_money", "args": dict(fx["substituted"])}
                hist = fx.get("history") or [{"tool": "read_file", "args": {"file_path": "document.txt"}, "output": fx["tool_output"], "executed": True}]
                pair = {}
                for role in ("legitimate", "unsafe"):
                    ep = SimpleNamespace(objective=fx["objective"], system_prompt=tf.SYSTEM_PROMPT, injection_task_id=None, episode_id="fixture")
                    g = RA.make_guard(a, cells[key], cs[key], ep, st)
                    for h in hist:
                        g.begin_decision_point()
                        g.evaluate(h["tool"], dict(h["args"]))
                        g.ingest(h["tool"], h["output"], executed=g.audit[-1]["released"] and h.get("executed", True))
                    g.begin_decision_point()
                    g.evaluate(fx[role + "_call"]["tool"], dict(fx[role + "_call"]["args"]))
                    pair[role] = bool(g.audit[-1]["released"])
                    pair[role + "_source"] = g.audit[-1]["verdict_source"]
                rr.append({"fixture": fx["id"], **pair})
            summary[a] = {"n": len(rr), "legitimate_released": sum(r["legitimate"] for r in rr), "unsafe_released": sum(r["unsafe"] for r in rr),
                          "pairs_correct": sum(r["legitimate"] and not r["unsafe"] for r in rr), "rows": rr}
        result[Path(path).stem] = summary
    return result


def stage_report():
    d, aux, eps, folds = C._populations()
    st = common.make_setup()
    restricted = set(st.restricted)
    with (STATE / "rs_replays.pkl").open("rb") as f:
        mine = pickle.load(f)
    stored = J.load("replays") + J.load("value_replays") + C.load("cs_replays")
    by = collections.defaultdict(lambda: collections.defaultdict(dict))
    for scheme, role, e, a, u, s, err, aud in stored:
        if a in BASELINES:
            by[(scheme, role)][e][a] = (int(u), int(s), err, aud)
    for scheme, role, e, a, u, s, err, aud in mine:
        by[(scheme, role)][e][a] = (int(u), int(s), err, aud)
    fresh = aux["fresh"]
    # eligibility rule of the competitive study (unchanged): the stored B0 replay reproduces the recorded outcome
    b0 = {r[2]: r for r in J.load("replays") if r[0] == "S1" and r[1] == "dev2" and r[3] == "B0"}
    elig_dev2 = sorted(e for e, r in b0.items() if r[6] is None and (int(r[4]), int(r[5])) == (fresh[e].utility, fresh[e].security))
    prev = json.loads((ROOT / "REM_COMPETITIVE_STUDY_2026_11_16" / "results" / "results.json").read_text())
    assert len(aux["valid"]) == 3313 and len(elig_dev2) == 2113
    pops = {}
    cohort_hashes = {}
    for name, scheme, role, ids in [("primary_S1", "S1", "primary", aux["valid"]), ("primary_S2", "S2", "primary", aux["valid"]),
                                    ("dev2", "S1", "dev2", elig_dev2)]:
        B = by[(scheme, role)]
        if scheme == "S2":
            for e in ids:
                for a in TABLE_ARMS:
                    if a not in B[e]:
                        B[e][a] = by[("S1", "primary")][e][a]       # arms without a fitted quantity are identical under S2
        episodes = d.episodes if role == "primary" else fresh
        att = [e for e in ids if episodes[e].attacked]
        ben = [e for e in ids if not episodes[e].attacked]
        cohort_hashes[name] = {"episodes": len(ids), "attacked": len(att), "benign": len(ben), "sha256_sorted_ids": _hash_ids(ids)}
        usr = lambda e: episodes[e].user_task_id          # noqa: E731
        inj = lambda e: episodes[e].injection_task_id     # noqa: E731
        users = sorted({usr(e) for e in ids}, key=lambda u: int(u.split("_")[-1]))
        mm = R.block(B, att, ben, TABLE_ARMS, restricted)
        stages, withheld_benign, amount_reasons = {}, {}, {}
        for a in TABLE_ARMS:
            c = collections.Counter()
            wb = collections.Counter()
            ar = collections.Counter()
            for e in ids:
                for x in B[e][a][3]:
                    if x[4] not in restricted:
                        c["unrestricted_withheld"] += int(not x[2])
                        continue
                    lab = "attack_labelled" if x[0] == 1 else "not_attack_labelled"
                    stg = stage_of(a, x)
                    c[f"{lab}|{stg}"] += 1
                    if not x[2] and not episodes[e].attacked:
                        wb[f"{usr(e)}|{stg}"] += 1
                    if len(x) > 9 and x[9] is not None and stg.startswith("amount_"):
                        ar[f"{lab}|{stg}|{x[9][2]}"] += 1
            stages[a] = dict(sorted(c.items()))
            withheld_benign[a] = dict(sorted(wb.items()))
            amount_reasons[a] = dict(sorted(ar.items()))
        changed = {}
        for a, b in (("GV_math", "GV"), ("HV_math", "HV"), ("G3_math", "G3"), ("HV_math", "GV_math")):
            rows = []
            for e in ids:
                if B[e][a][:2] != B[e][b][:2]:
                    srcs = [x[6] for x in B[e][a][3] if x[4] in restricted and x[6].startswith("amount_")]
                    rows.append({"episode": e, "user_task": usr(e), "injection_task": inj(e), "attacked": bool(episodes[e].attacked),
                                 a: list(B[e][a][:2]), b: list(B[e][b][:2]), "amount_sources_in_" + a: srcs})
            changed[f"{a} vs {b}"] = {"episodes_with_different_outcome": len(rows),
                                     "by_user_task": dict(collections.Counter(r["user_task"] for r in rows)), "rows": rows}
        pops[name] = {
            "n_attacked": len(att), "n_benign": len(ben), "arms": mm,
            "contrasts": {a + " minus " + b: R.paired(B, att, ben, usr, inj, a, b) for a, b in CONTRASTS},
            "completion_by_user_task": {a: {u: [sum(B[e][a][0] for e in ids if usr(e) == u), sum(1 for e in ids if usr(e) == u)] for u in users}
                                        for a in TABLE_ARMS},
            "benign_completion_by_user_task": {a: {u: [sum(B[e][a][0] for e in ben if usr(e) == u), sum(1 for e in ben if usr(e) == u)] for u in users}
                                               for a in TABLE_ARMS},
            "restricted_call_stages": stages,
            "withheld_restricted_calls_in_benign_episodes": withheld_benign,
            "amount_verifier_reasons": amount_reasons,
            "outcome_changes": changed,
        }
        print(name, [(a, m["attacks_successful"], m["benign_completed"], m["all_tasks_completed"]) for a, m in mm.items()], flush=True)
    probe = by[("S1", "probe")]
    out = {
        "status": "EXPLORATORY DEVELOPMENT EVIDENCE: offline recorded-trace replay; no live agent, no model API; development protocol, "
                  "not a preregistration; the defects and the benchmark request texts were known before the repair was written",
        "cohorts": cohort_hashes,
        "populations": pops,
        "probe_reformatted_identifier": {"n": len(probe), "arms": {a: {"attacks": sum(v[a][1] for v in probe.values()),
                                                                           "replay_errors": sum(v[a][2] is not None for v in probe.values())}
                                                                       for a in TABLE_ARMS if all(a in v for v in probe.values())}},
        "replays_new_arms": len(mine), "replay_errors_new_arms": sum(1 for r in mine if r[6]),
        "fixtures": fixtures(J.load("cells"), C.load("cs_cells")),
        "fixtures_baselines_stored": {k: {a: {kk: vv for kk, vv in s.items() if kk != "rows"} for a, s in v.items() if a in BASELINES}
                                      for k, v in prev["fixtures"].items()},
    }
    (OUT / "results.json").write_text(json.dumps(out, indent=1, default=common._default), encoding="utf-8")
    (OUT / "cohort_hashes.json").write_text(json.dumps(cohort_hashes, indent=1), encoding="utf-8")
    with gzip.open(OUT / "episode_outcomes.jsonl.gz", "wt", encoding="utf-8") as f:
        for scheme, role, e, a, u, s, err, aud in sorted(mine, key=lambda z: z[:4]):
            f.write(json.dumps({"scheme": scheme, "population": role, "episode_id": e, "arm": a, "utility": u, "security": s, "error": err}) + "\n")
    with gzip.open(OUT / "restricted_call_audit.jsonl.gz", "wt", encoding="utf-8") as f:
        for scheme, role, e, a, u, s, err, aud in sorted(mine, key=lambda z: z[:4]):
            for k, x in enumerate(aud):
                if x[4] in restricted:
                    f.write(json.dumps({"scheme": scheme, "population": role, "episode_id": e, "arm": a, "call": k, "tool": x[4],
                                        "attempt_label": x[0], "verdict": x[1], "released": x[2], "source": x[6], "permission": x[7],
                                        "rule_stage": x[8], "amount": x[9], "source_before_veto": x[10]}, default=common._default) + "\n")


if __name__ == "__main__":
    for stage in sys.argv[1:]:
        {"replay": stage_replay, "report": stage_report}[stage]()
