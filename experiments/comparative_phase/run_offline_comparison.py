"""Offline paired comparison: no defence / REM v1.0 / REM predicates only / Progent (published manual policy).

KIND OF EVIDENCE: OFFLINE RECORDED-TRACE REPLAY (NO-ADAPT). The recorded AgentDojo agent actions are replayed
through the frozen REM replay harness; each arm decides, per proposed call, whether the call is released. A
withheld call is not executed (step-level semantics; no reviewer); the recorded agent does not react to it.
The replay outcome is therefore NOT a live attack success rate. No language model is called.

Protocol: REM_COMPARATIVE_EVALUATION_PHASE/01_EXPERIMENTAL_PROTOCOL.md (section O). Frozen REM v1.0 (rem/ at
9fddfa7) and the frozen pilot pipeline are imported, never edited. Arms B0, A0 (REM) and A3 (REM predicates only)
are the configurations of experiments/ablation_study/run_ablation.py, unchanged. Arm PG calls the authors'
`secagent.check_tool_call` (sunblaze-ucb/progent@3e79753) with the manual banking policy of 9befb41 read
verbatim from git; a raised ValidationError is a Block, anything else an Allow.

Populations and episode sets: identical to the ablation study of 21 Nov 2026 (P1 primary, P2 cross-template,
P3 second population, AM-4 validity rule), so every arm is paired with every ablation arm on the same episodes.

usage (isolated venv with Progent's dependencies; the main environment is not modified):
  PILOT_RESULTS_DIR=<fresh frozen pilot state> PYTHONHASHSEED=0 \
  /home/user/venvs/rem_progent_replay/bin/python experiments/comparative_phase/run_offline_comparison.py
"""
from __future__ import annotations

import collections
import gzip
import json
import os
import pickle
import statistics
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "ablation_study"))
import progent_policy as PP  # noqa: E402
import run_ablation as RA  # noqa: E402
RM = RA.RM
from rem.core.results import Verdict  # noqa: E402

OUT = ROOT / "REM_COMPARATIVE_EVALUATION_PHASE"
PINS = ROOT / "REM_EXTERNAL_DEFENSE_AUDIT" / "results" / "upstream_pins.json"
ARMS = ["B0", "A0", "A3", "PG"]
LABEL = {"B0": "no defence", "A0": "REM v1.0 (full)", "A3": "REM predicates only (learned decision bypassed)",
         "PG": "Progent, published manual banking policy"}
SEC = {}


def _decide_progent(f):
    sa = SEC["secagent"]

    def decide(c):
        try:
            sa.check_tool_call(c.tool, dict(c.args))
        except Exception as e:  # Progent's ValidationError (or any refusal raised by its checker)
            return Verdict.BLOCK, "progent_block", {"reason": str(e).split(". Please try")[0][:120]}
        return Verdict.ALLOW, "progent_allow", {}
    return decide


def episode_outcomes(by, eids, eps, restricted):
    """Per-episode outcomes (the unit of analysis)."""
    out = {}
    for e in eids:
        ep = eps[e]
        out[e] = {}
        for a in ARMS:
            u, s, err, aud = by[e][a]
            rc = [x for x in aud if x[4] in restricted]
            out[e][a] = {
                "attacked": bool(ep.injection_task_id),
                "utility": bool(u),
                "attack_outcome": bool(s) if ep.injection_task_id else None,
                "attack_call_released": any(x[0] == 1 and x[2] for x in rc) if ep.injection_task_id else None,
                "attack_call_proposed": any(x[0] == 1 for x in rc) if ep.injection_task_id else None,
                "any_restricted_withheld": any(not x[2] for x in rc),
                "restricted_calls": len(rc), "restricted_withheld": sum(1 for x in rc if not x[2]),
                "calls": len(aud),
            }
    return out


def mcnemar(b, c):
    return RA.mcnemar(b, c)


def rate(items, f):
    return float(np.mean([f(e) for e in items])) if items else float("nan")


def analyse(name, eo, eps, kw):
    att = [e for e in eo if eo[e]["B0"]["attacked"]]
    ben = [e for e in eo if not eo[e]["B0"]["attacked"]]
    inj = lambda e: eps[e].injection_task_id   # noqa: E731  cluster for attacked episodes [PD]
    usr = lambda e: eps[e].user_task_id        # noqa: E731  cluster for benign episodes [PD]
    gb = RA.grouped_bootstrap
    R = {"population": name, "attacked_episodes": len(att), "benign_episodes": len(ben),
         "clusters_attacked_injection_tasks": len({inj(e) for e in att}), "clusters_benign_user_tasks": len({usr(e) for e in ben}),
         "arms": {}, "paired": {}}
    for a in ARMS:
        m = {"label": LABEL[a]}
        if att:
            m["replay_attack_outcomes"] = sum(eo[e][a]["attack_outcome"] for e in att)
            m["replay_attack_outcome_rate"] = gb(att, inj, lambda s: rate(s, lambda e: eo[e][a]["attack_outcome"]), **kw)
            m["episodes_attack_call_released"] = sum(eo[e][a]["attack_call_released"] for e in att)
            m["episodes_attack_call_proposed"] = sum(eo[e][a]["attack_call_proposed"] for e in att)
            m["attacked_utility"] = sum(eo[e][a]["utility"] for e in att)
            m["attacked_utility_rate"] = gb(att, inj, lambda s: rate(s, lambda e: eo[e][a]["utility"]), **kw)
        if ben:
            m["benign_completed"] = sum(eo[e][a]["utility"] for e in ben)
            m["benign_completion_rate"] = gb(ben, usr, lambda s: rate(s, lambda e: eo[e][a]["utility"]), **kw)
            m["benign_episodes_with_a_withheld_call"] = sum(eo[e][a]["any_restricted_withheld"] for e in ben)
            m["benign_false_positive_episode_rate"] = gb(ben, usr, lambda s: rate(s, lambda e: eo[e][a]["any_restricted_withheld"]), **kw)
        R["arms"][a] = m
    pairs = [("A0", "B0"), ("PG", "B0"), ("A3", "B0"), ("A0", "PG"), ("A0", "A3"), ("PG", "A3")]
    for a, b in pairs:
        d = {}
        if att:
            for key, fld in (("attack_outcome", "attack_outcome"), ("attack_call_released", "attack_call_released"), ("attacked_utility", "utility")):
                x = sum(1 for e in att if eo[e][a][fld] and not eo[e][b][fld])
                y = sum(1 for e in att if eo[e][b][fld] and not eo[e][a][fld])
                d[key] = {"discordant_only_first_arm": x, "discordant_only_second_arm": y, "mcnemar_exact_p": mcnemar(x, y),
                          "difference_first_minus_second": gb(att, inj, lambda s, fld=fld: rate(s, lambda e: eo[e][a][fld] - eo[e][b][fld]), **kw)}
        if ben:
            for key, fld in (("benign_completion", "utility"), ("benign_false_positive", "any_restricted_withheld")):
                x = sum(1 for e in ben if eo[e][a][fld] and not eo[e][b][fld])
                y = sum(1 for e in ben if eo[e][b][fld] and not eo[e][a][fld])
                d[key] = {"discordant_only_first_arm": x, "discordant_only_second_arm": y, "mcnemar_exact_p": mcnemar(x, y),
                          "difference_first_minus_second": gb(ben, usr, lambda s, fld=fld: rate(s, lambda e: eo[e][a][fld] - eo[e][b][fld]), **kw)}
        R["paired"][f"{a}_vs_{b}"] = d
    # where REM and Progent disagree on attacked episodes (which tasks)
    R["A0_vs_PG_attack_outcome_disagreements"] = sorted(
        [eps[e].user_task_id, eps[e].injection_task_id, eps[e].pipeline, "REM_only" if eo[e]["A0"]["attack_outcome"] else "PG_only"]
        for e in att if eo[e]["A0"]["attack_outcome"] != eo[e]["PG"]["attack_outcome"])
    R["benign_by_user_task"] = {u: {a: [sum(eo[e][a]["utility"] for e in ben if usr(e) == u), sum(1 for e in ben if usr(e) == u)] for a in ARMS}
                                for u in sorted({usr(e) for e in ben}, key=lambda s: int(s.split("_")[-1]))}
    return R


def progent_check_timing(secagent, calls, reps=5):
    ts = []
    for _ in range(reps):
        for tool, args in calls:
            t0 = time.perf_counter()
            try:
                secagent.check_tool_call(tool, args)
            except Exception:
                pass
            ts.append((time.perf_counter() - t0) * 1e3)
    return {"calls_timed": len(ts), "median_ms": statistics.median(ts), "p95_ms": float(np.percentile(ts, 95))}


def main():
    t_start = time.time()
    policies, pmeta, src, block = PP.load_policy()
    secagent, enf_commit, tool_sha = PP.load_secagent(str(PINS))
    PP.install_policy(secagent, PP.banking_raw_tools(), policies)
    SEC["secagent"] = secagent
    raw = RA.load_raw()
    prim = RA.build("primary", raw)
    fits = RM.load_state("crossfit")
    rm = RM.load_state("rmod")
    folds = sorted(set(prim.fold.tolist()), key=str)
    pol = RM.build_policies(fits, rm["rmod"])
    refs = {f: RA.reference_from_mask(prim, prim.fold != f) for f in folds}
    RM.G.update(policies=pol, fits=fits)
    base = RA.configs()
    C = {"B0": base["B0"], "A0": base["A0"], "A3": base["A3"],
         "PG": {"variant": RA.V, "esc": RA.E2, "decide": _decide_progent}}       # no scorer: REM's estimator unused
    st = RM.make_setup()
    restricted = set(st.restricted)
    users = sorted({e.user_task_id for e in prim.episodes.values()}, key=str)
    rr = RA.assign_round_robin(users, len(folds))
    xt = RA.build("cross_template", raw)
    xt.episode_fold = {e: xt.episodes[e].injection_task_id for e in xt.episodes}
    second = RA.load_second(st, folds, rr)
    pops = [("P1_primary", prim, sorted(e for e, ok_ in rm["agree"].items() if ok_)),
            ("P2_cross_template", xt, sorted(xt.episodes)),
            ("P3_second_population", second, sorted(second.episodes))]
    kw = RA.KW
    out = {"status": "OFFLINE RECORDED-TRACE REPLAY (NO-ADAPT); NOT A LIVE ASR; no model call",
           "protocol": "REM_COMPARATIVE_EVALUATION_PHASE/01_EXPERIMENTAL_PROTOCOL.md section O",
           "progent_policy": pmeta, "progent_enforcement_commit": enf_commit, "secagent_tool_sha256": tool_sha,
           "bootstrap": {"resamples": kw["resamples"], "seed": kw["seed"], "level": kw["level"]}, "populations": {}}
    episodes_out = []
    restricted_calls_for_timing = []
    for name, data, eids in pops:
        t0 = time.time()
        res = RM.run_replays(C, eids, st, data, refs)
        by = collections.defaultdict(dict)
        for eid, c, u, s, err, aud in res:
            by[eid][c] = (u, s, err, aud)
        if name == "P1_primary":
            valid = [e for e in eids if all(by[e][a][2] is None for a in ARMS)]
        else:
            valid = [e for e in eids if all(by[e][a][2] is None for a in ARMS)
                     and (bool(by[e]["B0"][0]), bool(by[e]["B0"][1])) == (bool(data.episodes[e].utility), bool(data.episodes[e].security))]
        eo = episode_outcomes(by, valid, data.episodes, restricted)
        R = analyse(name, eo, data.episodes, kw)
        R["loaded"] = len(eids)
        R["excluded"] = {"replay_error": sum(1 for e in eids if any(by[e][a][2] for a in ARMS)),
                         "am4_no_defence_replay_differs_from_recording": len(eids) - len(valid) - sum(1 for e in eids if any(by[e][a][2] for a in ARMS))}
        R["rem_latency_full_ms"] = {"median": float(np.median([x[8] for e in valid for x in by[e]["A0"][3]])),
                                    "p95": float(np.percentile([x[8] for e in valid for x in by[e]["A0"][3]], 95)),
                                    "calls": sum(len(by[e]["A0"][3]) for e in valid)}
        R["seconds"] = time.time() - t0
        out["populations"][name] = R
        for e in valid:
            ep = data.episodes[e]
            episodes_out.append({"population": name, "episode": e, "user_task": ep.user_task_id, "injection_task": ep.injection_task_id,
                                 "backbone": ep.pipeline, "attack": ep.attack_type,
                                 "arms": {a: {**eo[e][a], "calls_detail": [[x[4], str(x[1]), bool(x[2]), x[0], x[7]] for x in by[e][a][3]]} for a in ARMS}})
            for msg in ep.raw_messages:
                for tc in (msg.get("tool_calls") or []):
                    if tc.get("function") in restricted:
                        restricted_calls_for_timing.append((tc["function"], dict(tc.get("args") or {})))
        print(name, "valid", len(valid), "of", len(eids),
              {a: (R["arms"][a].get("replay_attack_outcomes"), R["arms"][a].get("benign_completed")) for a in ARMS}, flush=True)
    out["progent_check_timing_ms"] = progent_check_timing(secagent, restricted_calls_for_timing[:5000])
    out["wall_seconds"] = time.time() - t_start
    (OUT / "results").mkdir(parents=True, exist_ok=True)
    (OUT / "results" / "offline_comparison_metrics.json").write_text(json.dumps(out, indent=1, default=float))
    with gzip.open(OUT / "results" / "offline_comparison_episodes.jsonl.gz", "wt") as fh:
        for r in episodes_out:
            fh.write(json.dumps(r) + "\n")
    (OUT / "results" / "progent_policy_9befb41_block.txt").write_text(block)


if __name__ == "__main__":
    main()
