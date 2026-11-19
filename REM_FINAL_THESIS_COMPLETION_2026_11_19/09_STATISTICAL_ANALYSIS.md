# 09 Statistical analysis (19 November 2026)

## 1 Units, dependence and the interval method

- **Unit of outcome:** the AgentDojo episode, i.e. one (backbone, user task, injection task) run. ASR is attack successes divided by attacked episodes. Utility is completed tasks divided by episodes.
- **Dependence.** Episodes are **not independent**: they share user tasks, injection-task templates and backbones, and each recorded trace is a single run. AgentDojo is an executable environment, not a sample of i.i.d. rows.
- **Interval method.** `rem.evaluation.bootstrap.grouped_bootstrap` (Chapter 3, Section 3.11.9):
  - resample the groups with replacement, recompute the statistic on the union of their episodes, and take the 2.5 and 97.5 percentiles;
  - 2,000 resamples, seed 20261027 and level 0.95, all declared in `configs/exploratory/pilot_e0.yaml` before the pilot.
- **Groups:**
  - ASR and ASR differences: by **injection task** (9 groups);
  - benign utility and its differences: by **user task** (16 groups);
  - all-task completion (attacked and benign pooled): by user task;
  - recorded external runs: the same rule.
- **Paired differences.** The statistic is the mean of the per-episode difference (arm − A0) within each resample, so the pairing on identical episodes is preserved.

## 2 What the intervals can and cannot support

| Issue | Consequence |
|---|---|
| Only 9 or 16 clusters | Percentile bootstrap intervals with this few clusters are known to under-cover. They are reported as **descriptive**, and the protocol's interpretation rules ("interval excludes 0") are decision rules, not significance tests at a guaranteed level. |
| Degenerate intervals [0, 0] | When no episode changes, or every change falls in one cluster that is rarely drawn, the interval collapses. [0.00, 0.00] means "no resample moved", not certainty. |
| Zero events | 0 / n is reported with the rule of three: an upper 95% bound of about 3/n, assuming independence. Examples: residual ASR after Modify, 0 / 610 episodes, bound about 0.5%; D1 + REM, 0 / 135, bound about 2.2%. Zero is never read as perfect security. |
| Development population | Every ablation interval describes variation over task templates **within the development population**. None estimates performance on unseen tasks, suites or models. |
| Multiplicity | 9 contrasts × 3 outcomes in the ablation, and 8 contrasts in the external study, are reported without adjustment. The protocol fixed interpretation rules, not a family-wise error rate. A single "excludes 0" among many is weak evidence. |

## 3 Post-hoc sensitivity: exact McNemar tests on discordant episodes

This analysis was **not in protocol 02**. It **ignores clustering**, so its p-values are anti-conservative. Source: `results/ablation_mcnemar_POSTHOC.json`.

| Contrast | Attacks (gained / removed) | p (exact) | Tasks (gained / lost) | p (exact) |
|---|---|---|---|---|
| A1 − A0 | 1 / 1 | 1.0 | 105 / 6 | < 1e-20 |
| A2 − A0 | 0 / 0 | – | 24 / 0 | 1.2e-07 |
| A3 − A0 | 153 / 0 | < 1e-40 | 552 / 38 | < 1e-100 |
| A4a − A0 | 0 / 0 | – | 0 / 2 | 0.50 |
| A4b − A0 | 9 / 3 | 0.146 | 56 / 77 | 0.082 |
| A5 − A0 | 0 / 0 | – | 0 / 0 | – |
| A6 − A0 | 661 / 0 | < 1e-190 | 599 / 98 | < 1e-80 |
| A7 − A0 | 0 / 0 | – | 0 / 5 | 0.0625 |

**Agreement with the pre-registered rule.** The sensitivity analysis agrees with the rule-based conclusions of `04`:
- **Resolved:** A3 and A6 for security; A1, A2, A3 and A6 for utility.
- **Not resolved:** A4b, even ignoring clustering.
- **Too few changes to test:** A4a and A7.

## 4 External comparison

- **Recorded closed loop.** One run per (user task, injection task) pair. The ASR interval is clustered by injection task, the benign interval by user task, with n = 16.
- **Replay contrasts.** Paired on identical episodes within each replay set.
- **Cross-kind contrasts.** Paired on identical (user, injection) pairs, but they compare two evaluation modes, closed loop and NO-ADAPT replay. Their intervals quantify task-template variation only, **not** the mode difference, which is a systematic bias of unknown sign and size.

## 5 Calibration metrics

The metrics are computed on 6,762 held-out steps (921 positives) shared by all model arms:
- **ECE:** 10 equal-width bins.
- **Log-loss:** clipped at the configured ε.

No intervals are given for them, because the steps within an episode are dependent and the protocol did not specify a step-level resampling scheme. They are therefore point descriptions.

## 6 Latency

- **What is reported:** mean, median and p95 of the complete-call timer over all 6,684 calls per arm. These describe the sample, and no interval is given.
- **Setting:** one shared CPU container, with REM running in the same process as the replay. The timings include the evaluation bookkeeping (reference-label lookup).
- **Scope:** they are not deployment latencies and are not comparable to the published defences' latencies, which were not measured here.
