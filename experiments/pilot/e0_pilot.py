"""Pilot E0 (Chapter 3 Sec. 3.11.8) — fitting portions only, never held-out folds.

For each outer fold f, a nested grouped cross-fit is run on D_train(f) alone
(its own leave-one-injection-task-out folds); the ROC-AUC of those predictions
is the fold-f fitting-portion AUC. Reported per evidence group and combined.
Decision values (pre-registered): min_positive_steps, min_group_roc_auc.
"""

from __future__ import annotations

import collections

import numpy as np

from common import load_config, provenance, write_json
from data import Designer, build, load_raw

from rem.algorithms.behavior.evidence import FEATURE_GROUPS, FEATURE_ORDER
from rem.algorithms.calibration.logit_nll import LabelNLLLogitCalibrator
from rem.evaluation.crossfit import nested_crossfit
from rem.evaluation.probabilistic import roc_auc


def main():
    cfg = load_config()
    E, P = cfg["estimation"], cfg["pilot_E0_decision_values"]
    raw = load_raw()
    data = build("primary", raw)
    counts = collections.Counter()
    for s in data.steps:
        counts[s.pipeline] += s.label
    pos_total = int(data.y.sum())

    variants = {"ctx": FEATURE_GROUPS["ctx"], "beh": FEATURE_GROUPS["beh"], "act": FEATURE_GROUPS["act"],
                "combined": FEATURE_ORDER}
    out = {}
    for name, feats in variants.items():
        aucs = {}
        for f in sorted(set(data.fold.tolist()), key=str):
            tr = data.fold != f
            sub = np.flatnonzero(tr)
            designer = Designer(data, feats)

            def design(mask_sub, sub=sub):
                full = np.zeros(len(data.steps), bool)
                full[sub[mask_sub]] = True
                return designer(full)[sub]

            res = nested_crossfit(
                design=design, y=data.y[sub], outer_fold=data.fold[sub], inner_group=data.inner_group[sub],
                inner_is_benign_group=~data.attacked[sub], feature_order=feats,
                lambda_grid=E["lambda_grid"], inner_folds=E["inner_folds"],
                calibrator_factory=LabelNLLLogitCalibrator, alpha_blk=None, alpha_mod=None,
                clip=E["probability_clip"],
            )
            aucs[f] = roc_auc(data.y[sub], res.logit)
        vals = [v for v in aucs.values() if v == v]
        out[name] = {"per_outer_fold_fitting_auc": aucs, "mean": float(np.mean(vals)), "min": float(np.min(vals))}
        print(name, out[name]["mean"], out[name]["min"])

    retained = [g for g in ("ctx", "beh", "act") if out[g]["mean"] >= P["min_group_roc_auc"]]
    decision = {
        "positive_steps_total": pos_total,
        "positive_steps_per_backbone": dict(counts),
        "backbones_below_min_positive_steps": sorted(k for k, v in counts.items() if v < P["min_positive_steps"]),
        "proceed": pos_total >= P["min_positive_steps"],
        "retained_groups": retained,
        "decision_rule": "retain group iff mean fitting-portion ROC-AUC >= min_group_roc_auc; "
                         "proceed iff pooled positive steps >= min_positive_steps (pooled analysis)",
        "decision_values": P,
    }
    write_json("e0_pilot.json", {"provenance": provenance(), "group_auc": out, "decision": decision})
    print(decision)


if __name__ == "__main__":
    main()
