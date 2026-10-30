# CHAPTER FIVE

# EXPLORATORY PILOT EVALUATION

> **EXPLORATORY — NOT CONFIRMATORY THESIS RESULTS — SUPERVISOR DECISION REQUIRED.**
>
> This chapter reports an executed pilot. Its design was declared and committed before any held-out prediction was computed (`configs/exploratory/pilot_e0.yaml`, commit `48bef90`; amendments AM-1 to AM-4, commit `7a707a7`). Every number comes from `results/pilot/` (code commit `aa66f22`), and a complete second run reproduced every number exactly. The confirmatory evaluation specified in Chapter 3 remains **RESULTS PENDING** until:
>
> - the design values are frozen (SD-FREEZE, SD-1 to SD-4);
> - live enforcing-mode runs become possible;
> - the replay conflict SC-7 is decided.
>
> Results in Sections 5.6–5.7 that depend on trajectory replay are marked **[REPLAY — SC-7]**: the method is out of scope in Chapter 3 Section 3.1.4.

## 5.1 Purpose

The pilot asks whether the REM pipeline of Chapter 3 can be fitted and evaluated on real agent behaviour under the grouped cross-fitting protocol. It also asks what that evaluation shows for each research question ([PD]), and which of Chapter 3's assumptions it confirms or contradicts.

It is a pilot in the sense of Chapter 3 Section 3.11.8. It also executes, on the same data, the experiments E1–E6 that the master plan names. Negative results are reported with the same prominence as positive ones.

## 5.2 Data and Protocol

### 5.2.1 Data

**Source.** The AgentDojo repository (Debenedetti et al., 2024) ships recorded traces of real LLM agents for its banking suite.
- The pilot uses the traces of **21 undefended backbones** under the `important_instructions` attack: 16 user tasks × 9 injection tasks, plus 16 benign episodes per backbone.
- Episodes recorded with an error (5) and the label-ambiguous pair of AM-1 (21 episodes) are excluded.

**Size.** The pilot dataset contains:
- **3,334 episodes**;
- **6,762 proposed tool calls** (steps);
- **921 positive steps**, in 840 attacked episodes.

**What the data are not.** No trace was generated or altered, and no live LLM was called. The episodes are not independent observations: they share 16 user-task templates, 9 injection tasks, a single attacker account and one environment. All intervals are therefore grouped (Section 5.2.3).

**Labels.** Labels follow the reference-match rule (Chapter 3 Section 3.11.3; Chapter 4 Section 4.10.1). A positive label marks an *attempt*: the agent proposed the attacker's reference action with the attacker's argument. Of the 840 attacked episodes containing a positive step:
- 682 also have recorded attack success;
- 158 do not (the benchmark's success predicate is stricter).

Two episodes record attack success without a positive step (Section 5.9).

### 5.2.2 Pre-registered values

All values come from Chapter 3 where Chapter 3 gives them. Otherwise they are exploratory declared values, varied over a declared grid where Chapter 3 says they are declared.

**Table 5.1. Principal pre-registered values**

| Item | Value | Basis |
|---|---|---|
| Features | x^ctx₂, x^beh₁₋₄, x^act₁₋₃ (x^ctx₁ blocked) | Tables 3.8–3.9 |
| Tiers | read 1; profile 2; transfer ≤ 1000: 3; transfer > 1000, payment modification, credential change: 4 | Table 3.11 (illustrative) |
| Costs | C_FA = 1; C_miss = 1, 5, 10, 20 by tier; C_mod = 0.5; C_esc = 0.3 | Declared; structure Table 3.13 |
| r_mod(k) | Measured; 1.0 where unmeasured | Section 3.8 property 3 |
| Predicates | Π = ∅; k_D2 = 3; required evidence x^act₁ | Declared |
| B1 | α_blk = 0.01, α_mod = 0.05 | Declared |
| λ grid; inner folds | {0.01, 0.1, 1, 10, 100}; 4 | Declared |
| ECE bins; clip | 10; 10⁻⁶ | Declared |
| E0 decision values | ≥ 50 positive steps; group ROC-AUC ≥ 0.55 | Declared |
| Bootstrap | 2,000 resamples, seed 20261027 | Declared |

### 5.2.3 Protocol

- **Cross-fitting.** Nested grouped cross-fitting (Procedure 3.1):
  - nine outer folds, leave one injection task out;
  - benign episodes assigned to folds by user task;
  - grouped inner folds select λ and produce out-of-fold logits for calibration.
- **Reported predictions.** Every reported prediction is held out.
- **Intervals.** 95% percentile intervals from a grouped bootstrap: attacked items are resampled by injection task, benign items by user task.

There are only nine injection-task groups, so intervals are wide and can be unstable.

## 5.3 Pilot E0: Feasibility and Feature Freezing

E0 used only the fitting portions of the outer folds.

**Table 5.2. Pilot E0 (mean over the 9 fitting portions)**

| Evidence group | ROC-AUC (mean; min over folds) | Retained (≥ 0.55) |
|---|---|---|
| Context (x^ctx₂ only) | 0.582; 0.554 | Yes, marginally |
| Behavioral | 0.802; 0.787 | Yes |
| Action | 0.929; 0.923 | Yes |
| All | 0.938; 0.930 | — |

- **Positive steps.** Pooled: 921, above the declared minimum of 50. Thirteen of 21 backbones have fewer than 50 positive steps each (range 2–116), so no per-backbone conclusion is drawn.
- **Feature set.** Under the pre-registered rule, all eight features were retained.
- **AS-7.** The pilot supports AS-7 for this benchmark: the observable evidence separates induced from benign steps.

## 5.4 RQ1 — Discrimination and Calibration (E1)

**Table 5.3. Held-out discrimination and calibration, pooled over 9 outer folds (6,762 steps, 921 positive)**

| Metric | Calibrated p, label-NLL fit (Eq. 3.4) | Calibrated p, Platt smoothed targets | Uncalibrated p̃ |
|---|---|---|---|
| ROC-AUC | 0.938 [0.908, 0.961] | 0.938 | 0.939 |
| Average precision (PR-AUC estimate) | 0.719 [0.559, 0.827] | 0.719 | 0.721 |
| ECE (M = 10) | 0.044 [0.033, 0.084] | 0.044 | 0.042 |
| Log-loss | 0.201 [0.149, 0.294] | 0.201 | 0.201 |
| Brier, binary / two-class (SC-5) | 0.060 / 0.121 | 0.060 / 0.121 | 0.060 / 0.120 |

**Table 5.4. Per-fold results (calibrated, label-NLL)**

| Held-out injection task | Steps | Positive | ROC-AUC | AP | ECE | Log-loss | λ | γ₁ |
|---|---|---|---|---|---|---|---|---|
| 0 | 824 | 125 | 0.962 | 0.788 | 0.059 | 0.161 | 10 | 0.959 |
| 1 | 773 | 101 | 0.965 | 0.854 | 0.046 | 0.140 | 10 | 0.947 |
| 2 | 807 | 112 | 0.949 | 0.735 | 0.035 | 0.164 | 10 | 0.958 |
| 3 | 772 | 110 | 0.962 | 0.811 | 0.045 | 0.154 | 10 | 0.955 |
| 4 | 726 | 135 | 0.978 | 0.906 | 0.087 | 0.148 | 10 | 0.947 |
| 5 | 634 | 23 | 0.859 | 0.308 | 0.068 | 0.164 | 10 | 0.969 |
| 6 | 666 | 79 | 0.909 | 0.501 | 0.075 | 0.225 | 10 | 0.981 |
| 7 (credential change) | 730 | 124 | 0.903 | 0.577 | **0.189** | **0.530** | 1 | 0.980 |
| 8 | 830 | 112 | 0.959 | 0.859 | 0.037 | 0.146 | 10 | 0.945 |

Findings:
1. **Discrimination generalizes to unseen attacker objectives.** Held-out ROC-AUC is 0.86–0.98 per fold.
   - The weakest folds are injection task 5 (23 positive steps) and injection task 7.
   - Injection task 7 is the only credential-change attack, so when it is held out the model has never seen an attack of that category.
2. **Calibration does not transfer to an unseen attack category.** The injection-task-7 fold has ECE 0.189 and log-loss 0.53, three to four times the other folds.
3. **Platt calibration adds nothing here (negative result).**
   - The fitted maps are close to the identity (γ₁ = 0.945–0.981).
   - Pooled ECE is 0.044 with calibration and 0.042 without.
   - The two fitting targets (SC-4) give indistinguishable results.
   - This is consistent with logistic regression already producing calibrated probabilities on in-distribution data. It does not show that calibration is unnecessary under shift: no fold had γ₁ ≤ 0, but fold 7 shows that miscalibration under shift is not repaired.
4. **Other generalization checks.**
   - *Leave one backbone out* (21 folds): pooled ROC-AUC 0.949. Per held-out backbone the range is 0.736 (claude-3-haiku) to 1.000, with ECE 0.038–0.080.
   - *Grouping by user task* (sensitivity, 16 folds): pooled ROC-AUC 0.943. One fold, user_task_15, scores 0.211; Section 5.9 explains this as a label problem.
   - *Other attack templates, applied with no refitting* (gpt-4o, 135–138 valid episodes each):

     | Template | ROC-AUC |
     |---|---|
     | direct | 0.959 |
     | ignore_previous | 0.940 |
     | important_instructions_no_names | 0.948 |
     | injecagent | 0.922 |
     | tool_knowledge | 0.955 |

     ECE ranges from 0.028 to 0.086.

Figure 5.1 (`results/pilot/figures/fig_reliability.png`) shows the held-out reliability diagram. Mid-range bins contain few steps, which explains the visible noise.

![Figure 5.1. Held-out reliability diagram (10 equal-width bins), calibrated and uncalibrated. EXPLORATORY.](results/pilot/figures/fig_reliability.png){width=55%}

## 5.5 RQ2 — REM versus the Consequence-Independent Baseline, Observe-Only (E2)

Both policies use the same held-out calibrated probabilities. REM (A3) adds tiers and expected loss; B1 (A1) uses the Eq. 3.14 thresholds. Verdicts were computed on the recorded steps and not enforced.

**Table 5.5. Held-out verdict profile (observe-only)**

| | REM | B1 |
|---|---|---|
| Intervention on y = 1 steps (any non-Allow) | 0.973 [0.957, 0.987] | 0.740 [0.473, 0.922] |
| Step false-positive rate (any non-Allow on y = 0) | 0.227 [0.213, 0.239] | 0.056 [0.047, 0.066] |
| …Escalate share of all steps | 0.196 | 0.009 |
| y = 0 steps withheld if an idealized reviewer resolves escalations | 0.040 | 0.046 |
| Ties (SC-2) | 0 | 0 |
| D2 verdicts | 58 | 58 |

REM's additional interventions are almost all escalations. **On benign episodes, REM releases 33 of 180 legitimate state-changing steps (tiers 2–4); B1 releases 132.** The mechanism follows directly from the pre-registered costs:
- the Allow–Block indifference points are p*₃ = 1/11 and p*₄ = 1/21 (Eq. 3.9);
- legitimate transfers often carry action evidence (for example, a recipient read from a tool output), which places them above those points;
- the dominance check (Eq. 3.10) shows that, under these costs, Block is never the unique minimizer at tier 3, so at that tier REM chooses among Allow, Modify and Escalate.

The realized loss under the decision costs is 0.114 for REM and 0.652 for B1. **This comparison favours REM by construction**, because REM minimizes expected loss under these costs (Chapter 3 Section 3.12.3). It is not evidence of superiority.

## 5.6 RQ2 and RQ3 — Enforcement **[REPLAY — SC-7]** (E4)

Enforcement was estimated by replaying each recorded episode in the AgentDojo sandbox with REM at the tool boundary (Chapter 4 Section 4.10.3).
- **Assumption NO-ADAPT:** the agent does not react to a refusal.
- **Validity:** with every call allowed, the replay reproduced 3,313 of 3,334 recorded outcomes (99.4%). Only those 3,313 episodes are used (AM-4).
- **Status:** the method is out of scope in Chapter 3 (SC-7).

**Table 5.6. Enforcement replay (3,313 episodes; 95% grouped-bootstrap intervals)**

| Configuration | ASR | Benign utility | Utility under attack |
|---|---|---|---|
| B0, no defense | 0.226 [0.148, 0.295] | 0.524 [0.381, 0.676] | 0.492 |
| B1, step-level, no reviewer | 0.055 [0.011, 0.134] | 0.509 [0.334, 0.702] | 0.514 |
| B1, episode-level, no reviewer | 0.046 [0.004, 0.125] | 0.509 [0.334, 0.702] | 0.485 |
| REM, step-level, no reviewer | 0.004 [0.001, 0.007] | 0.314 [0.110, 0.548] | 0.364 |
| REM, episode-level, no reviewer | 0.004 [0.001, 0.007] | 0.314 [0.110, 0.548] | 0.363 |
| REM, step- or episode-level, idealized reviewer | 0.004 [0.001, 0.007] | 0.497 [0.333, 0.680] | 0.481–0.496 |

**Table 5.7. Paired differences (grouped bootstrap)**

| Comparison | ΔASR | ΔBenign utility |
|---|---|---|
| REM − B1, no reviewer | −0.051 [−0.130, −0.007] | −0.195 [−0.341, −0.074] |
| REM − B1, idealized reviewer | −0.051 [−0.130, −0.007] | +0.003 [−0.009, 0.018] |
| REM − B0, no reviewer | −0.222 [−0.289, −0.146] | −0.210 [−0.379, −0.051] |

Figure 5.2 (`results/pilot/figures/fig_enforcement_replay.png`) displays Table 5.6.

![Figure 5.2. Enforcement replay [REPLAY — SC-7]: ASR and benign utility with 95% grouped-bootstrap intervals. EXPLORATORY.](results/pilot/figures/fig_enforcement_replay.png){width=95%}

**Interpretation, within the replay assumption:**
- REM blocks more attempted attacks than B1. It does so at a large utility cost when no one resolves escalations, and at almost no cost when an oracle does.
- The idealized reviewer knows the label. It is an upper bound on reviewer quality, not a model of one.
- Without a reviewer, REM's benign utility is 0.25–0.38 for every one of the 21 backbones. This is close to the share of user tasks that need no state change (4 of 16).

**SC-1.** The step-level and episode-level variants give the same results, which is a consequence of NO-ADAPT: a non-adaptive agent does not retry a refused tool, so restrictions that persist through the episode have nothing to act on.

**RQ3 quantities:**
- **r_mod(k).** Measured by oracle-Modify replays within the fitting folds: 0.000 at tier 3 (530 episodes) and 0.010 at tier 4 (298 episodes).
- **Residual ASR in replays where REM applied Modify to an adversarial step:** 0.000 (610 episodes).
- **Caveat.** Both values are artefacts of NO-ADAPT as much as properties of tool restriction. Under replay, a withheld call simply does not happen.
- **Escalation rate:** 0.196 of all steps (Table 5.5).
- **Latency.** REM's per-step processing time, excluding LLM inference and tool execution, has a median of 0.17–0.20 ms and a p95 of 0.43–0.54 ms across configurations.
- **Memory.** The peak traced allocation per step has a median of 2.9 KB and a p95 of 12.4 KB (300 episodes).

**Distributed defenses** (recorded outcomes for gpt-4o, not replayed, possibly from different benchmark versions; not a controlled comparison):

| Defense | ASR | Benign utility |
|---|---|---|
| tool_filter | 0.112 | 0.81 |
| transformers_pi_detector | 0.007 | 0.44 |
| repeat_user_prompt | 0.462 | 0.94 |
| spotlighting_with_delimiting | 0.615 | 0.81 |

## 5.7 RQ4 — Ablations (E5)

**Table 5.8. Ablations (step-level; observe-only columns use held-out recorded steps; replay columns are [REPLAY — SC-7], no reviewer)**

| Configuration | Held-out ROC-AUC | Step FPR (observe) | y = 1 intervention (observe) | ASR (replay) | Benign utility (replay) |
|---|---|---|---|---|---|
| Full REM | 0.938 | 0.227 | 0.973 | 0.004 | 0.314 |
| − context evidence | 0.938 | 0.228 | 0.973 | 0.004 | 0.314 |
| − behavioral evidence | 0.938 | **0.174** | 0.973 | 0.004 | **0.419** |
| − action evidence | **0.799** | 0.242 | 0.921 | 0.006 | 0.314 |
| − calibration (p̃ in Eq. 3.6) | — | 0.213 | 0.973 | 0.004 | 0.329 |
| one tier for all actions: 1 | — | 0.093 | 0.757 | 0.051 | 0.440 |
| one tier for all actions: 2 | — | 0.157 | 0.909 | 0.022 | 0.353 |
| one tier for all actions: 3 | — | 0.233 | 0.972 | 0.004 | 0.338 |
| one tier for all actions: 4 | — | 0.336 | 0.976 | 0.003 | 0.314 |
| − predicates D1, D2 | — | 0.226 | 0.973 | 0.004 | 0.314 |
| observe-only (no mitigation) | — | — | — | 0.226 | 0.524 |

Chapter 3 does not specify which tier the "tiers removed" ablation should use, so all four were run.

Findings:
- **Action evidence carries most of the discrimination.** Removing it lowers held-out ROC-AUC from 0.938 to 0.799 and AP from 0.719 to 0.367.
- **Context evidence makes no measurable difference** (negative result). This also bounds the risk that the instruction patterns were tailored to the benchmark (Section 5.9).
- **Behavioral evidence lowers benign utility** (negative result). Removing it keeps ASR unchanged and raises benign utility by 10.5 points in replay. In this pilot, the behavioral group costs utility without a measured security benefit.
- **Calibration and predicates change little.** With Π empty, D2 fires on 58 steps and changes no episode outcome in replay.
- **Tiers drive the trade-off.** A single low tier recovers utility and loses protection; a single high tier does the opposite. REM's tier map sits between these extremes.

## 5.8 Optional Sequential Analysis (E3, A2, observe-only)

The Bernoulli CUSUM was fitted per outer fold on benign fitting episodes.
- **q₁ = 0.3:** the CUSUM is undefined in all nine folds, because the estimated pre-change rate q₀ ≈ 0.34 exceeds q₁.
- **q₁ = 0.5 and q₁ = 0.7** (similar results):
  - an alarm occurred after the injected content entered the context in 74.8% of attacked episodes with a positive step;
  - the alarm came at or before the first positive step in 42.5–43.8% of them;
  - the median delay was 1 step.
- **False alarms:** the held-out benign false-alarm rate was 0.106, against the in-fold target of 0.05, so the threshold did not generalize.

A2 issued no verdicts. In this pilot, the CUSUM adds nothing that the per-step estimator does not already provide.

## 5.9 Validity Findings That Qualify the Results

1. **The attacker's account is also a legitimate payee.**
   - In AgentDojo banking suite versions v1 and v1.1, user_task_15 asks the agent to pay a new landlord whose IBAN is the attacker IBAN used by every injection task. The benchmark changed this from v1.1.1; 16 of the 21 recorded backbones used the colliding prompt.
   - The label-relevant definitions of the injection tasks are identical in all suite versions, so labels are consistent across the mixed recordings.
   - The pre-registered amendment AM-1 excluded only the pair whose reference solutions collide.
   - After results were computed, 29 positive steps in other user_task_15 episodes were found to be ambiguous, 19 of them with no injected content in the context.
   - All of REM's residual replay ASR (0.4%) comes from these episodes.
   - A disclosed post-hoc sensitivity analysis excluding user_task_15 gives REM ASR 0.000 in every configuration and held-out ROC-AUC 0.952. The primary analysis above keeps the pre-registered rule.
2. **Reference matching misses alternative routes.**
   - Two episodes have recorded attack success but no positive step. One reaches the attacker through a different tool; one appears to be a recording inconsistency.
   - 105 steps carry an attacker value but are labelled 0.
   - In a sample of 30 attacked episodes, 29 labels agreed with the trace and one was a likely false negative of this kind.
   - That inspection was performed by an AI assistant, not by a human annotator, and must be repeated.
3. **Single attacker identity.** x^act₂ ("recipient not in the objective") fires on essentially every attack, because the attacker IBAN never appears in an objective (except in user_task_15). Real fraud may use recipients that do appear in the user's context.
4. **NO-ADAPT and SC-7** qualify every enforcement number (Section 5.6).
5. **One run per configuration.** The recorded traces contain one run per (backbone, task pair), against the "at least three" of Chapter 3 Section 3.11.9.
6. **Historical backbones and a single benchmark.** The models are 2024–2025 snapshots; results are not pooled across benchmarks, and none other was evaluated.

The complete threat analysis is in `EXPERIMENT_VALIDITY_REPORT.md`.

## 5.10 Realized Loss across the Declared Grid (E6)

Realized loss (Eq. 3.22) on held-out steps was computed over the declared grid:
- C_miss multipliers {0.5, 1, 2, 5};
- C_esc {0.1, 0.3, 0.6};
- amount limits {100, 1000, 10000}.

**Results across all 36 cells:**
- REM with matched costs: 0.039–0.298;
- REM with the base costs evaluated under different costs (misspecified): 0.057–0.324;
- B1: 0.303–3.261.

REM's matched loss is lower than B1's in all 36 cells. Two caveats apply:
- the comparison is favoured by construction (Section 5.5);
- the misspecified-cost column is the more informative one: REM remains below B1 in all 36 cells even when its decision costs differ from the evaluation costs within this range.

Matched costs gave a lower realized loss than misspecified costs in 34 of the 36 cells, not all 36. Minimizing *expected* loss under estimated probabilities does not guarantee the lowest *realized* loss on a finite held-out set.

The grid cell α_blk = 0.05 is not evaluable, because the pre-registered α_mod = 0.05 must exceed α_blk; this inconsistency in the pre-registered grid is reported, not repaired.

## 5.11 Summary of Evidence by Research Question ([PD])

**Table 5.9. Evidence summary**

| RQ | What the pilot shows | Strength |
|---|---|---|
| RQ1 | Held-out ROC-AUC 0.94 (0.86–0.98 per fold; 0.92–0.96 on other templates; 0.74–1.00 per held-out backbone). ECE 0.044, but it degrades on an unseen attack category. Calibration adds nothing measurable | Exploratory; one benchmark; grouped intervals |
| RQ2 | Observe-only: REM intervenes on more attacked steps than B1 but escalates far more benign ones. Replay: lower ASR than B1; utility cost from −19.5 points (no reviewer) to ≈0 (oracle reviewer) | Exploratory; replay is out of scope (SC-7) |
| RQ3 | r_mod ≈ 0 and residual ASR 0 under NO-ADAPT (assumption-driven); escalation 19.6% of steps; latency < 1 ms per step at p95 | Exploratory; replay (SC-7) |
| RQ4 | Action evidence dominates. Context evidence makes no difference. Behavioral evidence costs utility. Tiers drive the protection–utility trade-off | Exploratory |

## References

Debenedetti, E., Zhang, J., Balunović, M., Beurer-Kellner, L., Fischer, M., & Tramèr, F. (2024). AgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents. In *Advances in Neural Information Processing Systems 37*. https://doi.org/10.52202/079017-2636

Efron, B. (1979). Bootstrap methods: Another look at the jackknife. *The Annals of Statistics, 7*(1), 1–26. https://doi.org/10.1214/aos/1176344552

Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. In *Proceedings of the 34th International Conference on Machine Learning* (Vol. 70, pp. 1321–1330). PMLR.

Naeini, M. P., Cooper, G., & Hauskrecht, M. (2015). Obtaining well calibrated probabilities using Bayesian binning. *Proceedings of the AAAI Conference on Artificial Intelligence, 29*(1). https://doi.org/10.1609/aaai.v29i1.9602
