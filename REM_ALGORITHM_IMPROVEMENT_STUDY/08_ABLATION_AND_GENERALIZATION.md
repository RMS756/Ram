# Ablations and generalization

[PROPOSED — SUPERVISOR APPROVAL REQUIRED]

## Candidate components

AA_REM, AA_no_authorization, AA_no_provenance, AA_no_behavior and AA_no_repair each ran on the same 150 native replays. All yield ASR 0/135 and benign success 5/15. With no contracts, these components cannot activate. The zero difference is a **coverage limitation**, not evidence that authorization/provenance/behavior/repair never matter.

Synthetic correctness ablations demonstrate the intended semantics: removing authorization withholds directly authorized operations; removing provenance withholds delegated fields but preserves direct grants; removing single-use behavior permits a duplicate; removing repair blocks a correctable recipient. These tests are not empirical component-effectiveness evidence. A learned-intervention ablation is inapplicable because no learned intervention component was adopted.

## Original evidence and calibration ablations

| Refitted original estimator | Calibrated ROC-AUC | Average precision | Binary Brier |
|---|---:|---:|---:|
| Full | 0.88456 | 0.74639 | 0.09990 |
| No context | 0.88313 | 0.74571 | 0.09852 |
| No behavioral features | 0.84842 | 0.67259 | 0.09743 |
| No action features | 0.73857 | 0.50787 | 0.14082 |

The action group remains dominant on labels that share its matching mechanism. Removing behavior reduces discrimination here while slightly improving Brier, which differs from historical utility behavior; do not equate discrimination with policy quality. Primary unsmoothed and secondary smoothed calibration are reproduced in the original pilot. Raw/full and evidence-removed decision counts plus the original 4×3 miss/escalation-cost grid are in `artifacts/sensitivity.json`. Cost variation uses only inherited exploratory values and produces decision diagnostics, not new bank-specific economics.

Original estimator alternatives investigated: label-NLL versus original smoothed Platt fitting, removal of groups, and x_act1-only rule. No extra classifier is selected using the test set. Random-forest intervention-value learning is not a valid substitute without its outcome targets.

## Generalization boundaries

The primary learned baselines leave out injection objectives; the fixed candidate has no statistical fitting. Per-user-task and per-objective native replay results are in `artifacts/generalization_strata.json`. These strata do not establish task-disjoint learned security. The original reproduction separately estimates held-out-user-task and held-out-backbone discrimination. No cross-benchmark transfer was evaluated.

New beneficiaries, malicious/legitimate matched contracts, case/space/hyphen/zero-width IBAN formats, conflicting external fields and alternative banking tools are synthetic specification probes only. No perturbed benchmark efficacy dataset was fabricated. All cross-template recordings lack explicit versions and were excluded from the new controlled experiment; their original exploratory results remain a reproduction diagnostic.

A claim that AA_REM generalizes better than original REM or published controllers is **not supported**.

## Historical diagnostics independently rerun

On the separately reproduced full mixed-version cohort, held-out-user-task ROC-AUC is 0.943124, compared with held-out-objective ROC-AUC 0.938288. This evaluates original attempt-label discrimination, not candidate authorization or causal task-held-out enforcement. Cross-template results are archived in `artifacts/historical/e4_cross_template_and_defenses.json`.
