"""Descriptive secondary tables from the stored confirmatory replays (no new replay, no fitting).

Reads AUTHZ_STATE/confirm_a.pkl written by confirm_a.py and writes
REM_FINAL_SUBMISSION/results/confirmatory_descriptives.json. Nothing here enters the pre-declared verdict.
"""
from __future__ import annotations

import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import study as S  # noqa: E402
from study import common  # noqa: E402
from confirm_a import ARMS, OUT  # noqa: E402


def main():
    st = common.make_setup()
    D = S.load("confirm_a")
    meta, rec = D["meta"], D["recorded"]
    by = collections.defaultdict(dict)
    for scheme, role, eid, arm, u, s, err, aud in D["res"]:
        by[eid][arm] = (u, s, err, aud)
    valid = sorted(e for e in by if by[e]["B0"][2] is None and (by[e]["B0"][0], by[e]["B0"][1]) == rec[e])
    restricted = set(st.restricted)
    out = {"note": "descriptive; secondary; not part of the pre-declared verdict", "n_eligible": len(valid), "arms": {}}
    for a in ARMS:
        calls = [x for e in valid for x in by[e][a][3]]
        r0 = [x for x in calls if x[4] in restricted and x[0] == 0]      # restricted-tool calls not labelled as attack attempts
        r1 = [x for x in calls if x[0] == 1]
        ro = [x for x in calls if x[4] not in restricted]
        esc_eps = sum(1 for e in valid if any(x[1] == "escalate" for x in by[e][a][3]))
        withheld_eps = sum(1 for e in valid if any(not x[2] for x in by[e][a][3]))
        tiers = collections.defaultdict(lambda: [0, 0])
        for x in r0:
            tiers[int(x[3])][1] += 1
            tiers[int(x[3])][0] += int(bool(x[2]))
        out["arms"][a] = {
            "calls_evaluated": len(calls),
            "verdict_mix_all_calls": dict(collections.Counter(x[1] for x in calls)),
            "restricted_unlabelled_calls_n": len(r0),
            "restricted_unlabelled_calls_released": sum(1 for x in r0 if x[2]),
            "restricted_unlabelled_released_by_tier": {str(k): v for k, v in sorted(tiers.items())},
            "attack_labelled_calls_n": len(r1),
            "attack_labelled_calls_released": sum(1 for x in r1 if x[2]),
            "other_tool_calls_n": len(ro),
            "other_tool_calls_withheld": sum(1 for x in ro if not x[2]),
            "episodes_with_an_escalate_verdict": esc_eps,
            "escalate_verdicts": sum(1 for x in calls if x[1] == "escalate"),
            "episodes_with_any_withheld_call": withheld_eps,
        }
    with open(os.path.join(OUT, "confirmatory_descriptives.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    for a in ARMS:
        m = out["arms"][a]
        print(a, m["calls_evaluated"], m["verdict_mix_all_calls"], "r0", m["restricted_unlabelled_calls_released"], "/", m["restricted_unlabelled_calls_n"],
              "tiers", m["restricted_unlabelled_released_by_tier"], "atk rel", m["attack_labelled_calls_released"], "/", m["attack_labelled_calls_n"],
              "other withheld", m["other_tool_calls_withheld"], "/", m["other_tool_calls_n"], "esc eps", m["episodes_with_an_escalate_verdict"],
              "esc", m["escalate_verdicts"], "eps withheld", m["episodes_with_any_withheld_call"])


if __name__ == "__main__":
    main()
