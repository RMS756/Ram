# Experiment protocol and validity

[PROPOSED — SUPERVISOR APPROVAL REQUIRED]

Machine-readable freeze: `experiments/authorization_generalization/protocol.json`, committed in `6acf2c2`; hash in `artifacts/protocol.sha256`. The historical dataset and aggregate findings were already known. This is not independent preregistration.

## Two analyses kept separate

**Historical reproduction:** unchanged pilot, AgentDojo package 0.1.35, recorded repository commit `089ed468cf3ed0322acc66b0211f26d9d90dbf60`, native suite v1, original seed 20261027 and original mixed-version recordings. Outputs written outside committed results. This tests reproducibility, not a new algorithm.

**New primary comparison:** explicitly versioned `v1.2.1` recordings only; remove all `user_task_15`, check trusted request equals that version's canonical prompt, require B0 replay agreement on both native outcomes. One Llama-3.3-70B pipeline; 150 episodes, 135 attacked and 15 benign, 442 steps, 109 positive attempts. All 150 passed outcome agreement. Native execution uses suite `v1.2.1`; original labels are unchanged for retained tasks. Unknown versions are excluded rather than inferred.

Baseline refits use only this cohort with the original fixed eight features, lambda grid, nested grouped OOF fitting and label-NLL calibration. Nine outer injection-objective folds; benign user tasks round-robin assigned as in the pilot. Every test objective is absent from its model's fitting folds. Benign transitions are estimated from fitting-only benign episodes. Original oracle-replay residuals are estimated without the held-out objective. This is objective holdout, **not a user-task-disjoint security evaluation**. User tasks can recur across objective folds; report that limitation explicitly.

Candidate A has no fitted parameters. All 150 episodes are unseen by a trained candidate because none is trained; per-task strata are diagnostic, not evidence that a learned semantic authorization model generalizes. Contracts are absent, so its positive authorization and repair behavior is evaluated only by synthetic correctness tests.

## Metrics and uncertainty

Primary metric: paired benign task success difference. No defensible noninferiority margin exists; no numerical improvement target or financial-loss coefficients are invented. Report ASR/utility Pareto points. Native ASR is the scorer's attacker-goal flag after **stateful recorded-trace replay under NO-ADAPT**. It is not an adaptive/live result.

Use paired bootstrap differences with the same episode pairs. Resample benign user-task clusters, attacked injection-objective clusters, 2,000 times; seed 20261111; 95% percentile intervals. Also report attacked user-task clustering sensitivity because the task/objective grid has crossed dependence. Neither one-way analysis fully resolves crossed task dependence; this small cohort cannot support a strong population inference. Repeated steps are never independent statistical replicates.

When all observed outcomes are zero the ordinary bootstrap interval is [0,0]. This is a degenerate descriptive interval, **not a zero population-risk upper bound or security proof**. Fifteen benign tasks and nine objectives give weak precision. No multiple-comparison significance claim is made.

Offline FNR/precision/recall compare withholding against legacy *attempt* labels. Benign action approval, false block and escalation rates are proxies, not adjudicated authorization rates. True unauthorized-banking-action rate, true authorization false blocks and true unnecessary escalations are unavailable without independent authorization labels. Candidate ROC-AUC/PR-AUC/calibration/Brier are not applicable because it emits no probability. Original-model metrics are reported separately.

## Unavailable controlled experiments

No cross-template trace has explicit version metadata in the selected cohort; candidate cross-template controlled efficacy is unavailable. The original full-cohort cross-template and held-out-user-task discrimination analyses remain separate exploratory diagnostics. Cross-benchmark transfer, adaptive closed-loop behavior and human review were not run. Published PROVISO/Task Shield/MELON/CASEL outcome comparisons were not substituted with their reported scores or approximate defenses.
