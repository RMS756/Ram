"""Read-only corpus diagnostics for the REM authorization audit (no refit, no tuning).

Inputs: a pilot results directory produced by the unchanged pipeline
(experiments/pilot: build_dataset.py, e0_pilot.py, run_main.py crossfit rmod replay), i.e.
<dir>/steps.pkl, <dir>/state/{crossfit,rmod,replay_main}.pkl and <dir>/e4_e5_enforcement_replay.json.

Outputs (JSON to stdout and <out>/corpus_diagnostics.json):
  1. primary counts recomputed from per-episode replay outcomes (not copied from reports);
  2. verdict distribution of proposed calls by tool and reference label, for REM, B1, REMnoEsc, B0;
  3. benign episodes that B0 completes but REM does not, and the first withheld legitimate call;
  4. observe-mode feature profile and calibrated probability of legitimate (y=0) value-transfer steps,
     with the fold's frozen scorer, versus the tier-specific Allow boundary C_esc / C_miss(k);
  5. the same for positive (y=1) value-transfer steps;
  6. comma-grouped decimal amounts in the corpus (the provenance-number parser boundary).
All quantities are descriptive diagnostics of the frozen system; nothing here selects a value.

usage: PILOT_RESULTS_DIR=<dir> python3 REM_AUTHORIZATION_AUDIT/tools/corpus_diagnostics.py <out_dir>
"""
from __future__ import annotations

import collections
import json
import os
import pickle
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "experiments", "pilot"))

import common  # noqa: E402
from data import build, reference_from_mask  # noqa: E402
from rem.algorithms.behavior.evidence import FEATURE_ORDER  # noqa: E402
from rem.algorithms.detection.ridge_logistic import sigmoid  # noqa: E402

CONFIGS = ("B0", "REM_step_level_no_reviewer", "REMnoEsc_step_level_no_reviewer", "B1_step_level_no_reviewer",
           "REM_step_level_idealized")
VT = {"send_money", "schedule_transaction"}


def load(name):
    with open(os.path.join(common.RESULTS, "state", f"{name}.pkl"), "rb") as fh:
        return pickle.load(fh)


def main(out_dir):
    data = build("primary")
    fits = load("crossfit")["label_nll_primary"]
    rm = load("rmod")
    res = load("replay_main")
    valid = sorted(e for e, ok in rm["agree"].items() if ok)
    vset = set(valid)
    by = collections.defaultdict(dict)
    for eid, c, u, s, err, aud in res:
        by[eid][c] = (u, s, err, aud)
    att = [e for e in valid if data.episodes[e].attacked]
    ben = [e for e in valid if not data.episodes[e].attacked]
    out = {"provenance": common.provenance(), "n_valid": len(valid), "n_attacked": len(att), "n_benign": len(ben)}

    # 1. counts
    counts = {}
    for c in CONFIGS:
        counts[c] = {"attacks_successful": int(sum(by[e][c][1] for e in att)),
                     "benign_successful": int(sum(by[e][c][0] for e in ben)),
                     "utility_under_attack": int(sum(by[e][c][0] for e in att)),
                     "replay_errors": int(sum(1 for e in valid if by[e][c][2]))}
    out["counts"] = counts

    # 2. verdicts by tool and label (all proposed calls in valid episodes)
    vd = {}
    for c in CONFIGS:
        t = collections.Counter()
        for e in valid:
            for a in by[e][c][3]:
                label, verdict, released, tier, tool = a[0], a[1], a[2], a[3], a[4]
                grp = "value_transfer" if tool in VT else ("read" if tool.startswith("get_") or tool == "read_file" else "other_state_change")
                t[(("benign_ep" if e in set(ben) else "attacked_ep"), grp, int(label), verdict, bool(released))] += 1
        vd[c] = [{"episode": k[0], "tool_group": k[1], "label": k[2], "verdict": k[3], "released": k[4], "n": n}
                 for k, n in sorted(t.items())]
    out["verdicts_by_tool_group"] = vd

    # 3. benign episodes lost relative to B0
    lost = []
    for e in ben:
        if by[e]["B0"][0] and not by[e]["REM_step_level_no_reviewer"][0]:
            first = next((a for a in by[e]["REM_step_level_no_reviewer"][3] if not a[2]), None)
            lost.append({"episode": e, "user_task": data.episodes[e].user_task_id,
                         "first_withheld_tool": first[4] if first else None,
                         "first_withheld_verdict": first[1] if first else None,
                         "first_withheld_label": first[0] if first else None,
                         "first_withheld_tier": first[3] if first else None,
                         "first_withheld_source": first[7] if first else None})
    out["benign_lost_vs_B0"] = {
        "n": len(lost),
        "by_first_withheld_tool_and_verdict": collections.Counter(f"{r['first_withheld_tool']}|{r['first_withheld_verdict']}|{r['first_withheld_source']}" for r in lost),
        "by_user_task": collections.Counter(r["user_task"] for r in lost),
        "first_withheld_label_counts": collections.Counter(str(r["first_withheld_label"]) for r in lost),
    }
    gained = [e for e in ben if by[e]["REM_step_level_no_reviewer"][0] and not by[e]["B0"][0]]
    out["benign_gained_vs_B0"] = len(gained)

    # 4-5. observe-mode features and probabilities of value-transfer steps (frozen fold scorers)
    folds = sorted(set(data.fold.tolist()), key=str)
    refs = {f: reference_from_mask(data, data.fold != f) for f in folds}
    loss = common.load_config()["losses"]
    allow_bound = {int(k): float(loss["C_esc"]) / float(loss["C_miss"][k]) for k in loss["C_miss"]}
    prof = {}
    for lab in (0, 1):
        rows = []
        for i, s in enumerate(data.steps):
            if s.tool not in VT or s.label != lab or s.episode_id not in vset:
                continue
            if lab == 0 and data.episodes[s.episode_id].attacked:
                continue   # legitimate transfers from benign episodes only (cleanest y=0 set)
            f = data.fold[i]
            ff = fits.fits[f]
            x = {n: (float(s.transition not in refs[f].transitions) if n == "x_beh4" else float(s.features[n]))
                 for n in FEATURE_ORDER}
            z = ff.intercept + sum(c * x[n] for n, c in zip(FEATURE_ORDER, ff.coefficients))
            p = float(sigmoid(ff.gamma_1 * z + ff.gamma_0))
            rows.append((x, p, s.tier, s.user_task_id, s.transition[0]))
        if not rows:
            continue
        P = np.array([r[1] for r in rows])
        K = np.array([r[2] for r in rows])
        above = np.array([r[1] >= allow_bound[r[2]] for r in rows])
        prof[f"label_{lab}"] = {
            "n_steps": len(rows),
            "feature_firing_rate": {n: float(np.mean([r[0][n] > 0 for r in rows])) for n in FEATURE_ORDER},
            "x_beh2_mean": float(np.mean([r[0]["x_beh2"] for r in rows])),
            "p_quantiles": {q: float(np.quantile(P, q)) for q in (0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0)},
            "tier_counts": collections.Counter(int(k) for k in K),
            "share_p_at_or_above_allow_boundary": float(np.mean(above)),
            "allow_boundary_by_tier": allow_bound,
            "previous_tool_counts": collections.Counter(r[4] for r in rows),
            "pattern_counts": collections.Counter(
                "beh3={:.0f},beh4={:.0f},act1={:.0f},act2={:.0f},act3={:.0f}".format(
                    r[0]["x_beh3"], r[0]["x_beh4"], r[0]["x_act1"], r[0]["x_act2"], r[0]["x_act3"]) for r in rows).most_common(12),
        }
    out["value_transfer_step_profile_observe_mode"] = prof

    # 6. comma-grouped decimals: tokens like 1,234.56 in objectives and tool outputs
    pat = re.compile(r"\d{1,3}(?:,\d{3})+\.\d+")
    n_obj = n_tool = 0
    ex = set()
    for e in vset:
        ep = data.episodes[e]
        if pat.search(ep.objective or ""):
            n_obj += 1
            ex.update(pat.findall(ep.objective))
        if any(m.role == "tool" and pat.search(m.text or "") for m in ep.messages):
            n_tool += 1
    out["comma_grouped_decimal_tokens"] = {"episodes_with_token_in_objective": n_obj,
                                           "episodes_with_token_in_tool_output": n_tool,
                                           "examples": sorted(ex)[:10]}
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "corpus_diagnostics.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=common._default)
    print(json.dumps({k: out[k] for k in ("counts", "benign_lost_vs_B0", "benign_gained_vs_B0",
                                          "comma_grouped_decimal_tokens")}, indent=1, default=common._default))
    for k, v in prof.items():
        print(k, json.dumps({kk: v[kk] for kk in ("n_steps", "feature_firing_rate", "p_quantiles", "tier_counts",
                                                   "share_p_at_or_above_allow_boundary", "pattern_counts")}, default=common._default))


if __name__ == "__main__":
    main(sys.argv[1])
