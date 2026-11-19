# 02 Frozen ablation protocol (19 November 2026). Committed before any arm of this study was scored

**Hashes.** The runner, the frozen code it imports, and this file are hashed in `02_05_PROTOCOL_HASHES.sha256`, committed together with this file and `05`. A later change is a dated amendment, reported next to the frozen result.

## Object of study

The **approved REM v1.0**, unchanged:
- `rem/` core identical to commit `9fddfa7`. `git diff 9fddfa7 HEAD -- rem/` shows only two added modules outside the decision path, `rem/deployment/gateway.py` and `rem/integration/melon_rem.py`, plus the empty `rem/deployment/__init__.py`.
- The frozen pilot pipeline `experiments/pilot/` at `ea621c3`.
- The configuration `configs/exploratory/pilot_e0.yaml`, declared in `48bef90` before any run.

Its components:
- the evidence vector (context, behavioural and action/provenance groups);
- ridge logistic regression;
- logistic (Platt-type) recalibration of the logit, fitted by label negative log-likelihood (the primary calibrator of the pilot);
- consequence tiers;
- policy predicates D1/D2;
- the expected-loss decision over Allow / Modify / Escalate / Block;
- step-level mitigation, with no reviewer (the deployment configuration);
- linear SHAP attribution, **audit-only by design**. It cannot change a verdict, so it is not ablated; its additivity is reported.

**Fitted state.** A fresh run of the frozen pilot pipeline at this branch's base commit:

```
build_dataset.py; e0_pilot.py; run_main.py crossfit rmod replay
```

It writes into a new state directory. **Reproduction gate:** before this study's runner is executed, REM v1.0 in that run must reproduce the published counts: 11 / 2,979 successful attacks, 105 / 334 benign tasks, 1,083 / 2,979 tasks under attack (thesis R7, Table 4.10). If it does not, the study stops.

## Arms

All arms use the same fold models, the same 3,313 episodes, step-level mitigation and no reviewer.

| Arm | Change | Retraining? |
|---|---|---|
| B0 | no defence (reference) | – |
| **A0** | **REM v1.0, frozen** | – |
| A1 | behavioural evidence group removed | refit (existing pilot refit `no_beh`) |
| A2 | Platt calibration removed: the raw logistic probability enters the same expected-loss engine. The loss-derived decision boundaries stay fixed (they are not re-selected). | no |
| A3 | consequence-independent thresholds: the frozen baseline B1 (Eq. 3.14). θ_blk and θ_mod are selected on each outer fold's training data (α fixed in the configuration); the test folds are never used. | thresholds per fold |
| A4a | context evidence group removed | refit (`no_ctx`) |
| A4b | action / provenance evidence group removed (the authorisation-related evidence of REM v1.0) | refit (`no_act`) |
| A5 | Modify removed from the verdict set (expected loss over Allow / Escalate / Block) | no |
| A6 | the learned decision removed: predicates D1/D2 only, every other call allowed | no |
| A7 | policy predicates removed (expected loss only) | no |

**Not ablated, and why:**
- **Linear SHAP:** audit-only by construction.
- **Offline recalibration:** it is the calibration step itself (A2).
- **An "authorisation layer"** separate from the evidence groups does not exist in REM v1.0. The request-derived permission rules of later studies are not part of the approved design.

## Data

- **Population.** Primary population, scheme S1: the outer fold holds out one attacker objective, and benign episodes are assigned to folds by user task, round robin.
- **Episodes.** 3,313 eligible episodes (AM-4): 2,979 attacked and 334 benign; 21 undefended backbones; attack `important_instructions`.
- **Predictions.** Every probability is a held-out (cross-fitted) prediction.

**Disclosure.**
- This population was used to design REM v1.0 (the pilot) and in every later study. It is development evidence, not an independent test set.
- The outcomes of B0, A0, A1, A2, A3, A4a, A4b and A7 were computed in the pilot (27 October to 1 November 2026) and are known (thesis R7, Section 4.5.1).
- New in this study: A5 and A6, the call-level reachability analysis, the latency per arm, the calibration table per arm, and the statistical contrasts against A0.

## Metrics

| Group | Metrics |
|---|---|
| Security | attack successes and ASR (/2,979); attack-labelled calls released; episodes with a released attack-labelled call (a proxy, not a measured state change) |
| Utility | benign tasks completed (/334); tasks completed under attack; all tasks (/3,313); legitimate state-changing calls released (/178 in benign episodes); legitimate payments released; false-positive intervention rate |
| Decision | Allow / Modify / Escalate / Block counts and rates over restricted calls; residual ASR in episodes where an attack call was Modified; precision, recall and F1 of "withhold" against the attempt label |
| Model (offline, held-out steps) | ROC-AUC, PR-AUC, Brier, ECE (10 bins), log-loss, for A0, A2 (raw), A1, A4a, A4b |
| Reachability (A0 vs A6, same recorded calls) | calls scored; calls forced by predicates before the expected-loss decision; calls reaching it; calls whose release changes because of the learned decision, by label; episodes whose task or attack outcome changes because of it |
| Runtime | complete-call latency: mean, median, p95 |

## Statistics

- **Paired contrasts against A0:** grouped bootstrap of the pilot configuration (2,000 resamples, seed and level from `pilot_e0.yaml`). ASR is clustered by injection task (9 clusters); utility by user task (16 clusters).
- **Few clusters.** The intervals are descriptive, and coverage is not guaranteed.
- **Zero counts:** reported with the rule of three.

## Interpretation rules (fixed now)

| Statement about a component | Allowed only if |
|---|---|
| "measurable security contribution" | removing it increases attack successes **and** the ASR-difference interval excludes 0 |
| "security effect not resolved" | attack successes change, but the interval includes 0 |
| "measurable utility cost" | removing it increases benign or all-task completion and that interval excludes 0 |
| "redundant in this evaluation (NULL)" | no episode changes its task or attack outcome |
| "calibration improves protection" | A2 has more attack successes **and** the interval excludes 0. Better Brier or ECE alone never supports it. |
| "the learned decision contributes" | the A0 − A6 attack difference excludes 0 in A0's favour, **or** utility is higher under A0 with an interval excluding 0 |

**No margin of non-inferiority is used.** None was approved by the supervisors.

## Command

```
PILOT_RESULTS_DIR=<fresh state> python3 experiments/final_thesis/ablation_run.py
```
