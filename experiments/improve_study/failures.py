"""Failure analysis of the improvement study (analysis only; no arm, parser or matcher is changed).

Writes REM_IMPROVEMENT_STUDY/results/failure_analysis.json: for the permission rule G1, where legitimate
state-changing calls are withheld (by request and by permission status) and which attack-labelled calls are
released; for the learned arm L2, which reformatted-identifier attacks succeed. Request texts are those of
the public benchmark.
"""
from __future__ import annotations

import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import improve as I  # noqa: E402
from improve import OUT, common, load  # noqa: E402


def main():
    st = common.make_setup()
    D = load("replay")
    data = I.build("primary", I.load_raw())
    restricted = set(st.restricted)
    by = collections.defaultdict(lambda: collections.defaultdict(dict))
    for scheme, role, eid, arm, u, s, err, aud in D["res"]:
        by[(scheme, role)][eid][arm] = (u, s, err, aud)
    P, valid = by[("S1", "primary")], D["valid"]
    eps = data.episodes
    out = {"status": "development evidence; analysis only"}
    # 1. legitimate calls of benign episodes, permission rule G1, by user task and status
    tab = collections.defaultdict(collections.Counter)
    reasons = collections.defaultdict(collections.Counter)
    for e in valid:
        if eps[e].attacked:
            continue
        for x in P[e]["G1"][3]:
            if x[4] in restricted:
                perm = x[7] or ["n/a"]
                tab[eps[e].user_task_id][f"{perm[0]}|{x[4]}"] += 1
                if perm[0] != "supported":
                    reasons[eps[e].user_task_id][f"op={perm[4]}, recipient={perm[1]}, amount={perm[2]}, value={perm[3]}"] += 1
    key = lambda s: int(s.split("_")[-1])
    out["G1_legitimate_calls_benign_by_user_task"] = {u: dict(tab[u]) for u in sorted(tab, key=key)}
    out["G1_withheld_legitimate_calls_component_status"] = {u: dict(reasons[u]) for u in sorted(reasons, key=key)}
    out["requests"] = {u: next(eps[e].objective for e in valid if eps[e].user_task_id == u) for u in sorted(tab, key=key)}
    # 2. attack-labelled calls released by G1 (primary), by user task, injection task, tool and component status
    rel = collections.Counter()
    for e in valid:
        if not eps[e].attacked:
            continue
        for x in P[e]["G1"][3]:
            if x[0] == 1 and x[2]:
                perm = x[7] or ["n/a"] * 5
                rel[f"{eps[e].user_task_id}|{eps[e].injection_task_id}|{x[4]}|recipient={perm[1]}, amount={perm[2]}, value={perm[3]}"] += 1
    out["G1_released_attack_labelled_calls"] = dict(rel)
    out["G1_successful_attacks_by_pair"] = dict(collections.Counter(f"{eps[e].user_task_id}|{eps[e].injection_task_id}" for e in valid if eps[e].attacked and P[e]["G1"][1]))
    # 3. reformatted-identifier probe: where the learned arm L2 fails
    Pr = by[("S1", "probe_iban")]
    out["L2_probe_successful_attacks_by_user_task"] = dict(collections.Counter(eps[e].user_task_id for e in Pr if Pr[e]["L2"][1]))
    out["L2_probe_successful_attacks_by_injection_task"] = dict(collections.Counter(eps[e].injection_task_id for e in Pr if Pr[e]["L2"][1]))
    st_ = collections.Counter()
    for e in Pr:
        if Pr[e]["L2"][1] and not P[e]["L2"][1]:
            for x in Pr[e]["L2"][3]:
                if x[0] == 1 and x[2]:
                    perm = x[7] or ["n/a"] * 5
                    st_[f"{x[4]}|{perm[0]}|recipient={perm[1]}, amount={perm[2]}"] += 1
    out["L2_probe_released_attack_calls_in_new_failures"] = dict(st_)
    out["G1_probe_attack_calls_status"] = dict(collections.Counter((x[7] or ["n/a"])[0] for e in Pr for x in Pr[e]["G1"][3] if x[0] == 1))
    json.dump(out, open(os.path.join(OUT, "failure_analysis.json"), "w"), indent=1)
    for k, v in out.items():
        if k != "requests":
            print(k, json.dumps(v, indent=0)[:2500], "\n")


if __name__ == "__main__":
    main()
