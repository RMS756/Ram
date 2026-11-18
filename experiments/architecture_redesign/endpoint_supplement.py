"""Supplement to the frozen report (08): the utility endpoint "per candidate vs C1" was pre-specified for every candidate,
but arch_run.CONTRASTS computed it only for REM_B and REM_C. This script computes REM_A minus C1 with the SAME
eligibility rules, the SAME stored replays (arch_replays.pkl) and the SAME grouped bootstrap (report.paired); no arm is
re-run and nothing is tuned. Output: results/endpoint_supplement.json.
"""
import json
import pickle
import collections
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import arch_run as A  # noqa: E402



def main():
    d, aux, eps, folds = A._populations()
    with (A.STATE / "arch_replays.pkl").open("rb") as f:
        res = pickle.load(f)
    by = collections.defaultdict(lambda: collections.defaultdict(dict))
    for scheme, role, e, a, u, s, err, aud in res:
        by[(scheme, role)][e][a] = (int(u), int(s), err, aud)
    fresh = aux["fresh"]
    b0 = {r[2]: r for r in A.J.load("replays") if r[0] == "S1" and r[1] == "dev2" and r[3] == "B0"}
    elig_dev2 = sorted(e for e, r in b0.items() if r[6] is None and (int(r[4]), int(r[5])) == (fresh[e].utility, fresh[e].security))
    H = by[("S1", "heldout")]
    elig_h = sorted(e for e, v in H.items() if v["B0"][2] is None and (v["B0"][0], v["B0"][1]) == (int(eps["heldout"][e].utility), int(eps["heldout"][e].security)))
    out = {"status": "pre-specified endpoint computed after the frozen report (supplement); same data, rules and bootstrap"}
    for name, role, ids, episodes in [("primary_S1", "primary", aux["valid"], d.episodes), ("dev2", "dev2", elig_dev2, fresh),
                                      ("heldout_H", "heldout", elig_h, eps["heldout"])]:
        B = by[("S1", role)]
        att = [e for e in ids if episodes[e].attacked]
        ben = [e for e in ids if not episodes[e].attacked]
        out[name] = {"n": len(ids), "REM_A minus C1": A.R.paired(B, att, ben, lambda e, _p=episodes: _p[e].user_task_id,
                                                                 lambda e, _p=episodes: _p[e].injection_task_id, "REM_A", "C1")}
        print(name, len(ids), out[name]["REM_A minus C1"]["task_completion_all"], out[name]["REM_A minus C1"]["tasks_gained_lost"])
    path = Path(__file__).resolve().parents[2] / "REM_ARCHITECTURE_REDESIGN_STUDY_2026_11_18" / "results" / "endpoint_supplement.json"
    path.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
