"""External defence comparison (protocol: REM_FINAL_THESIS_COMPLETION_2026_11_19/05_EXTERNAL_BASELINE_PROTOCOL.md).

Two kinds of evidence, never pooled:
  (R) RECORDED CLOSED LOOP. AgentDojo's own banking runs of gpt-4o-2024-05-13 (repository ethz-spylab/agentdojo @ 089ed468,
      runs/): no defence, repeat_user_prompt, spotlighting_with_delimiting, tool_filter, transformers_pi_detector; attack
      important_instructions (144 user x injection pairs) and benign runs (16 user tasks). These were executed by the
      benchmark's authors with a real model; the agent saw each defence. Nothing is re-executed here; outcomes are read
      from the run files.
  (P) OFFLINE REPLAY OF REM v1.0. The frozen REM v1.0 (A0 configuration, cross-fitted fold models of the fresh pilot run)
      replayed (NO-ADAPT) on (a) the undefended gpt-4o traces and (b) each defence's traces (defence + REM layered).
      The replayed agent never sees REM's refusals.
Metrics with grouped-bootstrap intervals; paired differences on identical (user task, injection task) pairs.
Output: results/external_results.json, 06_EXTERNAL_BASELINE_RESULTS.csv
"""
from __future__ import annotations

import collections
import csv
import json
import os
import pickle
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "pilot"))
import run_main as RM  # noqa: E402
from data import build, load_raw, reference_from_mask  # noqa: E402
from rem.evaluation.bootstrap import grouped_bootstrap  # noqa: E402

OUT = ROOT / "REM_FINAL_THESIS_COMPLETION_2026_11_19"
KW = dict(resamples=RM.B["resamples"], seed=RM.SEED, level=RM.B["interval"])
GPT = "gpt-4o-2024-05-13"
DEF = {"D0": GPT, "D1": GPT + "-repeat_user_prompt", "D2": GPT + "-spotlighting_with_delimiting", "D3": GPT + "-tool_filter",
       "D4": GPT + "-transformers_pi_detector"}
NAMES = {"D0": "No defence", "D1": "repeat_user_prompt", "D2": "spotlighting_with_delimiting", "D3": "tool_filter",
         "D4": "transformers_pi_detector"}
RUNS = Path(os.environ.get("AGENTDOJO_RUNS", "/home/user/ethz-spylab/agentdojo/runs"))


def recorded(pipe):
    """All recorded banking runs of a pipeline: attacked (important_instructions) and benign user tasks (none)."""
    rows = []
    for f in sorted((RUNS / pipe / "banking").glob("user_task_*/*/*.json")):
        atk = f.parent.name
        if atk not in ("important_instructions", "none"):
            continue
        d = json.loads(f.read_text())
        inj = d.get("injection_task_id")
        rows.append({"pipeline": pipe, "user_task": d["user_task_id"], "injection_task": inj if atk != "none" else None,
                     "attacked": atk != "none", "utility": bool(d.get("utility")), "security": bool(d.get("security")),
                     "error": d.get("error")})
    return rows


def summarize_recorded(rows):
    att = [r for r in rows if r["attacked"] and r["error"] is None]
    ben = [r for r in rows if not r["attacked"] and r["error"] is None]
    return {"n_attacked": len(att), "n_benign": len(ben), "errors": sum(1 for r in rows if r["error"] is not None),
            "attack_successes": sum(r["security"] for r in att), "tasks_under_attack": sum(r["utility"] for r in att),
            "benign_completed": sum(r["utility"] for r in ben),
            "ASR": grouped_bootstrap(att, lambda r: r["injection_task"], lambda s: float(np.mean([r["security"] for r in s])), **KW),
            "utility_under_attack": grouped_bootstrap(att, lambda r: r["user_task"], lambda s: float(np.mean([r["utility"] for r in s])), **KW),
            "benign_utility": grouped_bootstrap(ben, lambda r: r["user_task"], lambda s: float(np.mean([r["utility"] for r in s])), **KW),
            "asr_by_injection_task": {i: sum(r["security"] for r in att if r["injection_task"] == i)
                                      for i in sorted({r["injection_task"] for r in att})}}


def main():
    raw = load_raw()
    prim = build("primary", raw)
    dfn = build("defense", raw)
    fits = RM.load_state("crossfit")
    rm = RM.load_state("rmod")
    pol = RM.build_policies(fits, rm["rmod"])
    folds = sorted(set(prim.fold.tolist()), key=str)
    refs = {f: reference_from_mask(prim, prim.fold != f) for f in folds}
    RM.G.update(policies=pol, fits=fits)
    base = RM.replay_configs()
    C = {"B0": base["B0"], "REM": base["REM_step_level_no_reviewer"]}
    st = RM.make_setup()
    # replay sets: undefended gpt-4o traces (primary role) and each defence's traces (defense role)
    sets = {"D0": (prim, [e for e in prim.episodes if prim.episodes[e].pipeline == GPT])}
    for k in ("D1", "D2", "D3", "D4"):
        sets[k] = (dfn, [e for e in dfn.episodes if dfn.episodes[e].pipeline == DEF[k]])
    rep = {}
    for k, (data, eids) in sets.items():
        res = RM.run_replays(C, sorted(eids), st, data, refs)
        by = collections.defaultdict(dict)
        for eid, c, u, s, err, aud in res:
            by[eid][c] = (u, s, err, aud)
        rep[k] = (data, by)
    with open(os.path.join(RM.STATE, "final_external_replays.pkl"), "wb") as fh:
        pickle.dump({k: dict(v[1]) for k, v in rep.items()}, fh)
    out = {"status": "two evidence kinds: recorded closed loop (AgentDojo authors' runs) and offline replay of REM v1.0 (NO-ADAPT); "
                     "not pooled; no model call in this study", "recorded": {}, "replay": {}, "paired": {}}
    rows_csv = []
    recs = {k: recorded(p) for k, p in DEF.items()}
    for k in DEF:
        s = summarize_recorded(recs[k])
        out["recorded"][k] = {"name": NAMES[k], **s}
        rows_csv.append({"evidence": "recorded_closed_loop", "arm": f"{k} {NAMES[k]}", "n_attacked": s["n_attacked"], "n_benign": s["n_benign"],
                         "attack_successes": s["attack_successes"], "ASR": s["ASR"][0], "ASR_lo": s["ASR"][1], "ASR_hi": s["ASR"][2],
                         "tasks_under_attack": s["tasks_under_attack"], "benign_completed": s["benign_completed"],
                         "benign_utility": s["benign_utility"][0], "benign_lo": s["benign_utility"][1], "benign_hi": s["benign_utility"][2]})
    for k, (data, by) in rep.items():
        eps = data.episodes
        valid = [e for e in by if by[e]["B0"][2] is None and (bool(by[e]["B0"][0]), bool(by[e]["B0"][1])) == (bool(eps[e].utility), bool(eps[e].security))]
        att = [e for e in valid if eps[e].attacked]
        ben = [e for e in valid if not eps[e].attacked]
        for arm in ("B0", "REM"):
            label = f"{k} {NAMES[k]} + REM v1.0 (replay)" if arm == "REM" else f"{k} {NAMES[k]} replayed without REM"
            m = {"loaded": len(by), "eligible": len(valid), "n_attacked": len(att), "n_benign": len(ben),
                 "attack_successes": int(sum(by[e][arm][1] for e in att)), "tasks_under_attack": int(sum(by[e][arm][0] for e in att)),
                 "benign_completed": int(sum(by[e][arm][0] for e in ben)),
                 "ASR": grouped_bootstrap(att, lambda e: eps[e].injection_task_id, lambda s: float(np.mean([by[e][arm][1] for e in s])), **KW),
                 "benign_utility": (grouped_bootstrap(ben, lambda e: eps[e].user_task_id, lambda s: float(np.mean([by[e][arm][0] for e in s])), **KW)
                                    if ben else [None, None, None]),
                 "latency_ms_median": float(np.median([x[8] for e in valid for x in by[e][arm][3]])) if valid else None,
                 "latency_ms_p95": float(np.percentile([x[8] for e in valid for x in by[e][arm][3]], 95)) if valid else None}
            out["replay"][f"{k}|{arm}"] = {"name": label, **m}
            rows_csv.append({"evidence": "offline_replay_NO_ADAPT", "arm": label, "n_attacked": len(att), "n_benign": len(ben),
                             "attack_successes": m["attack_successes"], "ASR": m["ASR"][0], "ASR_lo": m["ASR"][1], "ASR_hi": m["ASR"][2],
                             "tasks_under_attack": m["tasks_under_attack"], "benign_completed": m["benign_completed"],
                             "benign_utility": m["benign_utility"][0], "benign_lo": m["benign_utility"][1], "benign_hi": m["benign_utility"][2]})
        # paired: REM replay vs the same traces without REM (within one evidence kind)
        out["paired"][f"{k}: REM replay minus no-REM replay"] = {
            "ASR": grouped_bootstrap(att, lambda e: eps[e].injection_task_id, lambda s: float(np.mean([by[e]["REM"][1] - by[e]["B0"][1] for e in s])), **KW),
            "utility_under_attack": grouped_bootstrap(att, lambda e: eps[e].user_task_id, lambda s: float(np.mean([by[e]["REM"][0] - by[e]["B0"][0] for e in s])), **KW),
            "benign_utility": (grouped_bootstrap(ben, lambda e: eps[e].user_task_id, lambda s: float(np.mean([by[e]["REM"][0] - by[e]["B0"][0] for e in s])), **KW)
                               if ben else None)}
    # descriptive cross-kind contrast on identical pairs: defence (recorded closed loop) vs REM on undefended traces (replay)
    d0data, d0by = rep["D0"]
    rem_by_pair = {(d0data.episodes[e].user_task_id, d0data.episodes[e].injection_task_id): d0by[e]["REM"] for e in d0by
                   if d0by[e]["B0"][2] is None and (bool(d0by[e]["B0"][0]), bool(d0by[e]["B0"][1])) == (bool(d0data.episodes[e].utility), bool(d0data.episodes[e].security))}
    for k in ("D1", "D2", "D3", "D4"):
        pairs = [(r["user_task"], r["injection_task"], r) for r in recs[k] if r["attacked"] and r["error"] is None
                 and (r["user_task"], r["injection_task"]) in rem_by_pair]
        out["paired"][f"REM v1.0 replay on undefended traces minus {NAMES[k]} recorded (DIFFERENT EVIDENCE KINDS; descriptive)"] = {
            "pairs": len(pairs),
            "ASR": grouped_bootstrap(pairs, lambda t: t[1], lambda s: float(np.mean([rem_by_pair[(u, i)][1] - r["security"] for u, i, r in s])), **KW),
            "utility_under_attack": grouped_bootstrap(pairs, lambda t: t[0], lambda s: float(np.mean([rem_by_pair[(u, i)][0] - r["utility"] for u, i, r in s])), **KW)}
    (OUT / "results" / "external_results.json").write_text(json.dumps(out, indent=1, default=float))
    with (OUT / "06_EXTERNAL_BASELINE_RESULTS.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows_csv[0]))
        w.writeheader()
        w.writerows(rows_csv)
    for r in rows_csv:
        print(r["evidence"][:8], r["arm"], r["attack_successes"], "/", r["n_attacked"], r["tasks_under_attack"], r["benign_completed"], "/", r["n_benign"])


if __name__ == "__main__":
    main()
