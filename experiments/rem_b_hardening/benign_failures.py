"""Phase 3: root causes of legitimate-task losses of frozen REM-B, on DEVELOPMENT populations only (primary S1, dev2).

An episode is a guard-caused loss if the unguarded replay (B0) completes the user task and REM-B does not.
REM-B is re-run on those episodes only, capturing arguments and decision details of every restricted call.
H (the earlier held-out traces) is deliberately NOT analysed here, so that it is not used to design new mechanisms.
Output: results/benign_failures.json (per call) and results/benign_failures_summary.json.
"""
import collections
import json
import pickle
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "architecture_redesign"))
import arch_run as A  # noqa: E402

OUT = ROOT / "REM_B_HARDENING_VALIDATION_2026_11_19" / "results"


def main():
    d, aux, eps, folds = A._populations()
    st = A.common.make_setup()
    cells, cs = A.J.load("cells"), A.C.load("cs_cells")
    A.RA.factory()
    res = pickle.load((A.STATE / "arch_replays.pkl").open("rb"))
    by = collections.defaultdict(dict)
    for scheme, role, e, a, u, s, err, aud in res:
        if scheme == "S1" and role in ("primary", "dev2"):
            by[(role, e)][a] = (u, s, err)
    rows = []
    for (role, e), v in sorted(by.items()):
        if not (v["B0"][0] and not v["REM_B"][0]):
            continue
        ep = eps[role][e]
        g = A.RA.build_cell("REM_B", ep, cells[("S1", folds[role][e])], cs[("S1", folds[role][e])], st)
        seen = []
        ev = g.evaluate

        def cap(tool, args, _s=seen, _ev=ev):
            _s.append(dict(args))
            return _ev(tool, args)
        g.evaluate = cap
        A.S.replay_episode(ep, st.suite, g)
        for k, a in enumerate(g.audit):
            if a["tool"] not in st.restricted or a["released"]:
                continue
            det = a["details"] or {}
            kk = det.get("contract")
            rows.append({"population": role, "episode": e, "user_task": ep.user_task_id, "injection_task": ep.injection_task_id,
                         "attacked": bool(ep.injection_task_id), "tool": a["tool"], "args": seen[k] if k < len(seen) else {},
                         "label": a["label"], "verdict": str(a["verdict"]), "source": a["verdict_source"],
                         "contract_status": kk[0] if kk else None, "contract_reason": kk[2] if kk else None,
                         "expected": [str(x) for x in kk[1]] if kk and kk[1] else None,
                         "object": det.get("object"), "objective": ep.objective})
    (OUT / "benign_failures.json").write_text(json.dumps(rows, indent=1, default=str))
    summ = collections.Counter((r["user_task"], r["tool"], r["source"], r["label"], (r["contract_reason"] or "")[:90]) for r in rows)
    lost = collections.Counter((role, ep_ut) for (role, e), v in by.items() if v["B0"][0] and not v["REM_B"][0]
                               for ep_ut in [eps[role][e].user_task_id])
    out = {"lost_episodes_by_population_and_task": {f"{a}|{b}": n for (a, b), n in sorted(lost.items())},
           "withheld_calls_in_lost_episodes": [{"user_task": k[0], "tool": k[1], "source": k[2], "attack_label": k[3],
                                                "reason": k[4], "n": n} for k, n in summ.most_common()]}
    (OUT / "benign_failures_summary.json").write_text(json.dumps(out, indent=1))
    print("lost episodes", sum(lost.values()), dict(lost))
    for k, n in summ.most_common(60):
        print(n, k)


if __name__ == "__main__":
    main()
