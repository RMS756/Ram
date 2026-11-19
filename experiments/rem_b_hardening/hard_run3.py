"""Amendment round 06a runner: REM-B3 and its ablations, reusing hard_run.py (frozen) unchanged.

Stages: replay | suites | fixtures | scripted | cost | report      (offline; no model call)
The frozen arms' replays are read from hard_replays.pkl (frozen round); REM-B3 arms are written to hard3_replays.pkl.
"""
from __future__ import annotations

import collections
import json
import multiprocessing as mp
import pickle
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import hard_run as HR  # noqa: E402
import remb3 as RB3  # noqa: E402

_orig_build = HR.RB.build_cell2


def _build(arm, ep, cell, extra, st):
    """REM-B3 arms -> remb3; every other arm -> remb2.build_cell2 (unchanged)."""
    if arm in RB3.CONFIGS3:
        return RB3.make_guard3(RB3.CONFIGS3[arm], cell, ep, st)
    return _orig_build(arm, ep, cell, extra, st)


HR.RB.build_cell2 = _build
B3_ARMS = ["REM_B3", "B3_noF1", "B3_noF2"]
SUITE_ARMS = ["B0", "GV_math2", "C1", "PG", "REM_B", "REM_B2"] + B3_ARMS
CONTRASTS3 = [("REM_B3", "REM_B"), ("REM_B3", "REM_B2"), ("REM_B3", "PG"), ("REM_B3", "C1"), ("REM_B3", "B3_noF1"), ("REM_B3", "B3_noF2"),
              ("REM_B3", "GV_math2")]
OUT = HR.OUT


def stage_replay():
    d, aux, eps, folds = HR._populations()
    HR._setup_workers(eps, folds)
    RB3.factory3()
    jobs = [("S1", role, e, a) for role in eps for a in B3_ARMS for e in sorted(eps[role])]
    t = time.time()
    with mp.get_context("fork").Pool(4) as p:
        res = list(p.imap_unordered(HR.replay_job, jobs, chunksize=32))
    with (HR.STATE / "hard3_replays.pkl").open("wb") as f:
        pickle.dump(res, f)
    print("replay3 done", len(res), round(time.time() - t), "s; errors", sum(1 for r in res if r[6]), flush=True)


def stage_suites():
    import diag_harness as H
    import generalization_cases as GC
    import heldout_probes as HPR
    import heldout_probes2 as HP2
    import heldout_probes3 as HP3
    import ledger_cases as LC
    HR.RB.CURRENT_ENV["env"] = None
    f = RB3.factory3()
    out = {}
    for name, cases, kind in (("ledger_dev", LC.CASES, "seq"), ("heldout_probes_v1", HPR.CASES, "seq"), ("heldout_probes2", HP2.CASES, "seq"),
                              ("heldout_probes3", HP3.CASES, "seq"), ("diagnostics", H.CASES, "diag"), ("generalization", GC.CASES, "diag")):
        if kind == "seq":
            rows = [r for case in cases for arm in SUITE_ARMS for seq in case["seqs"] for r in HR.run_case2(f, arm, case, seq)]
            res = HR.SH.dump(OUT / f"suite3_{name}.json", rows)
        else:
            res = H.dump(OUT / f"suite3_{name}.json", H.run_all(lambda a, ep: f(a, ep), SUITE_ARMS, cases=cases))
        out[name] = res["score"]
        for a, s in res["score"].items():
            print(name, a, "auth", s["authorized_released"], "/", s["authorized_n"], "| unauth", s["unauthorized_released"], "/",
                  s["unauthorized_n"], "| amb", s["ambiguous_released"], "/", s["ambiguous_n"], flush=True)
    (OUT / "suites3_summary.json").write_text(json.dumps(out, indent=1, default=str))


def stage_fixtures():
    arms, HR.ARMS = HR.ARMS, B3_ARMS
    fx_path = OUT / "fixtures.json"
    keep = fx_path.read_text()
    try:
        HR.stage_fixtures()
        (OUT / "fixtures3.json").write_text(fx_path.read_text())
    finally:
        fx_path.write_text(keep)
        HR.ARMS = arms


def stage_scripted():
    arms, HR.ARMS = HR.ARMS, B3_ARMS
    files = {n: (OUT / n).read_text() if (OUT / n).exists() else None for n in ("scripted_closed_loop.json", "scripted_summary.json")}
    try:
        HR.stage_scripted()
        for n in files:
            (OUT / n.replace("scripted", "scripted3")).write_text((OUT / n).read_text())
    finally:
        for n, v in files.items():
            if v is not None:
                (OUT / n).write_text(v)
        HR.ARMS = arms


def stage_cost():
    arms, HR.ARMS = HR.ARMS, B3_ARMS
    p = OUT / "operational_cost.json"
    keep = p.read_text() if p.exists() else None
    try:
        HR.stage_cost()
        (OUT / "operational_cost3.json").write_text(p.read_text())
    finally:
        if keep is not None:
            p.write_text(keep)
        HR.ARMS = arms


def stage_report():
    d, aux, eps, folds = HR._populations()
    restricted = set(HR.common.make_setup().restricted)
    res = pickle.load((HR.STATE / "hard_replays.pkl").open("rb")) + pickle.load((HR.STATE / "hard3_replays.pkl").open("rb"))
    by = collections.defaultdict(lambda: collections.defaultdict(dict))
    for scheme, role, e, a, u, s, err, aud in res:
        by[role][e][a] = (int(u), int(s), err, aud)
    frozen = json.loads((OUT / "hardening_results.json").read_text())
    elig_n = frozen["eligible"]
    fresh = aux["fresh"]
    b0 = {r[2]: r for r in HR.J.load("replays") if r[0] == "S1" and r[1] == "dev2" and r[3] == "B0"}
    elig = {"primary": sorted(aux["valid"]), "probe": sorted(eps["probe"]),
            "dev2": sorted(e for e, r in b0.items() if r[6] is None and (int(r[4]), int(r[5])) == (fresh[e].utility, fresh[e].security))}
    for role in ("heldout", "heldout2"):
        elig[role] = sorted(e for e, v in by[role].items() if v["B0"][2] is None
                            and (v["B0"][0], v["B0"][1]) == (int(eps[role][e].utility), int(eps[role][e].security)))
    assert {k: len(v) for k, v in elig.items()} == elig_n, "eligibility must equal the frozen round"
    names = {"primary": "primary_S1", "dev2": "dev2", "probe": "probe", "heldout": "heldout_H", "heldout2": "heldout_H2"}
    arms = HR.ARMS + B3_ARMS
    pops, rows_csv = {}, []
    for role, name in names.items():
        B, ids, episodes = by[role], elig[role], eps[role]
        att = [e for e in ids if episodes[e].attacked]
        ben = [e for e in ids if not episodes[e].attacked]
        usr = lambda e, _ep=episodes: _ep[e].user_task_id      # noqa: E731
        inj = lambda e, _ep=episodes: _ep[e].injection_task_id  # noqa: E731
        M = {}
        for a in B3_ARMS:
            M[a] = HR.CR._metrics(B, att, ben, a, restricted)
            M[a].update(HR._extra(B, ids, a, restricted))
            M[a]["unique_user_tasks"] = len({episodes[e].user_task_id for e in ids})
            M[a]["unique_task_pairs"] = len({(episodes[e].user_task_id, episodes[e].injection_task_id) for e in ids})
            rows_csv.append({"population": name, "arm": a, **M[a]})
        HR.CR.DESIGN_TASKS, HR.CR.SEEN_INJECTIONS = HR.DESIGN_TASKS, HR.SEEN_INJECTIONS
        pops[name] = {"n_attacked": len(att), "n_benign": len(ben), "metrics": M,
                      "contrasts": {f"{a} minus {b}": HR.R.paired(B, att, ben, usr, inj, a, b) for a, b in CONTRASTS3},
                      "partitions": {f"{a} vs {b}": HR.CR._partition_changes(B, ids, episodes, a, b) for a, b in CONTRASTS3[:3]},
                      "call_changes": {f"{a} vs {b}": HR._changes(B, ids, b, a) for a, b in CONTRASTS3},
                      "sources_of_changes_vs_REM_B2": dict(collections.Counter(
                          y[6] for e in ids for x, y in zip(B[e]["REM_B2"][3], B[e]["REM_B3"][3]) if x[2] != y[2])),
                      "gains_by_user_task": {f"{a} vs {b}": dict(collections.Counter(
                          episodes[e].user_task_id for e in ids if B[e][a][0] and not B[e][b][0])) for a, b in CONTRASTS3[:3]},
                      "losses_by_user_task": {f"{a} vs {b}": dict(collections.Counter(
                          episodes[e].user_task_id for e in ids if B[e][b][0] and not B[e][a][0])) for a, b in CONTRASTS3[:3]}}
        print(name, {a: (m["attack_objectives_reached"], m["benign_completed"], m["all_tasks_completed"], m["audited_violations_released"])
                     for a, m in M.items()}, flush=True)
    out = {"status": "AMENDMENT 06a (post-hoc, exploratory); offline replay (NO-ADAPT); no model call", "eligible": elig_n,
           "populations": pops, "replays_amendment": sum(1 for r in res if r[3] in B3_ARMS),
           "replay_errors_amendment": sum(1 for r in res if r[3] in B3_ARMS and r[6])}
    (OUT / "hardening_results_amendment.json").write_text(json.dumps(out, indent=1, default=HR.common._default), encoding="utf-8")
    import csv
    with (OUT / "security_utility_amendment.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_csv[0]))
        w.writeheader()
        w.writerows(rows_csv)


if __name__ == "__main__":
    for stage in sys.argv[1:]:
        {"replay": stage_replay, "suites": stage_suites, "fixtures": stage_fixtures, "scripted": stage_scripted, "cost": stage_cost,
         "report": stage_report}[stage]()
