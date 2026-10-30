# CHAPTER FIVE

# EXPERIMENTAL RESULTS AND EVALUATION: AN EXPLORATORY STUDY

## 5.1 Purpose, Status and Kinds of Evidence

This chapter reports what the implementation of Chapter 4 produced on recorded agent behavior in the AgentDojo banking environment. **The results are exploratory.** Two conditions for confirmatory results are not met:
- the design values they use (costs, tiers, predicates, feature set) await approval;
- the enforcing-mode evaluation with live agents that Chapter 3 specifies could not be executed.

The results are therefore not presented as confirmation of any claim, and the confirmatory evaluation remains pending.

Five kinds of evidence are kept apart throughout. Each table states which kind it reports.

| Kind | What it is | Used in |
|---|---|---|
| **Recorded outcome** | The benchmark's utility and security verdicts on the traces as recorded by the benchmark authors, without REM | Sections 5.2, 5.6.1 |
| **Held-out prediction** | REM's probability for a recorded step, from a model fitted without that step's group | Sections 5.3–5.4 |
| **Observe-only decision** | The verdict REM or the baseline would issue for a recorded step, computed but not enforced | Sections 5.5, 5.7, 5.9 |
| **Replay result** | The benchmark's verdicts after re-executing a recorded trajectory with REM enforcing, assuming the agent does not adapt | Section 5.6 |
| **Live run** | An agent running with REM enforcing | **None was executed** |

All numbers come from `results/pilot_R2/`, produced at commit `84a8c21` by `experiments/pilot/run_all.sh`. An independent re-execution on 30 October 2026 reproduced every analytical value; only time and memory measurements differed (Chapter 4, Section 4.11.2). The first run (commit `aa66f22`, `results/pilot/`) produced identical analytical values (Chapter 4, Section 4.11.2).

## 5.2 Data, Protocol and Chronology

### 5.2.1 Data

**Source.** The AgentDojo repository (Debenedetti et al., 2024) distributes traces of real LLM agents recorded by the benchmark authors. The evaluation uses the banking traces of **21 undefended backbones** under the `important_instructions` attack.

**Exclusions.** Episodes recorded with an error (5) and the pair (user_task_15, injection_task_4) (21 episodes, amendment AM-1) are excluded.

**Size** (`dataset_summary.json`):

| Unit | Count |
|---|---|
| Episodes | **3,334** (2,998 attacked, 336 without injection) |
| Proposed tool calls (steps) | **6,762** |
| Positive steps (y = 1) | **921** |
| Negative steps (y = 0) | 5,841 |

**Labels.** Labels follow the reference-match rule of Chapter 3, Section 3.11.3. A positive label marks an *attempt*: the agent proposed the attacker's reference action with the attacker's key argument. It is a proxy for adversarial inducement, not proof of it. Of the 840 attacked episodes with a positive step, the recorded outcome shows attack success in 682 and not in 158. Two attacked episodes record attack success without a positive step.

**Independence.** The episodes are not independent observations:
- they are built from 16 user-task and 9 injection-task templates;
- one attacker account;
- one environment.

All intervals are 95% percentile intervals from a bootstrap that resamples attacked items by injection task and benign items by user task. With nine injection-task groups the intervals are wide. Where a category contains a single injection task, no interval can be formed and none is reported.

### 5.2.2 Protocol

The protocol is nested grouped cross-fitting (Chapter 3, Procedure 3.1):
- nine outer folds, each holding out one injection task;
- episodes without injection assigned to folds by user task.

Within each fold's fitting portion, the following are fitted (Chapter 3, Section 3.11.5):
- λ, by grouped inner cross-validation;
- the calibration map, on inner out-of-fold logits;
- the baseline thresholds;
- the benign reference quantities;
- r~mod~.

The **pre-registered values** are listed in Table 5.1. They come from Chapter 3 where Chapter 3 gives them; otherwise they are declared exploratory values.

**Table 5.1. Pre-registered values** (`configs/exploratory/pilot_e0.yaml`)

| Item | Value |
|---|---|
| Features | x^ctx₂, x^beh₁₋₄, x^act₁₋₃ (x^ctx₁ absent) |
| Tiers | read 1; profile 2; transfer ≤ 1000: 3; transfer > 1000, payment modification, credential change: 4 |
| Costs | C~FA~ = 1; C~miss~ = 1, 5, 10, 20 by tier; C~mod~ = 0.5; C~esc~ = 0.3 |
| r~mod~(k) | Measured; 1.0 where unmeasured |
| Predicates | Π = ∅; k~D2~ = 3; required evidence x^act₁ |
| Baseline | α~blk~ = 0.01, α~mod~ = 0.05 |
| λ grid | λ~impl~ ∈ {0.01, 0.1, 1, 10, 100}, i.e. λ ∈ {0.005, 0.05, 0.5, 5, 50} on the scale of Eq. 3.2 |
| Inner folds; ECE bins; clip | 4; 10; 10⁻⁶ |
| Pilot E0 decision values | ≥ 50 positive steps; group ROC-AUC ≥ 0.55 |
| Bootstrap | 2,000 resamples, seed 20261027 |

### 5.2.3 Chronology of design, amendments and analyses

| Date and time (UTC) | Event | Record |
|---|---|---|
| 27 Oct 2026 16:40 | Pilot design committed (Table 5.1) | commit `48bef90` |
| 27 Oct 2026 16:57 | Amendments AM-1 to AM-4 committed. AM-1: exclusion of (user_task_15, injection_task_4). AM-2: benign references. AM-3: the meaning of "tool class". AM-4: replay validity filter | commit `7a707a7` |
| 27 Oct 2026, after 16:57 | First computation of held-out predictions and of all analyses with the then-uncommitted pipeline code. **The log of this first execution was not preserved**; its order relative to the amendments rests on the commit times and on the working session record | — |
| 27 Oct 2026 17:16 | Pipeline committed, then re-run in full; results identical to the first execution | commit `aa66f22`; `results/pilot/` |
| 27–28 Oct 2026 | **Post-hoc analyses**, added after results had been seen: exclusion of user_task_15 (Section 5.10); benign-release breakdown by tier; REM without expected-loss Escalate (Sections 5.5–5.6); breakdowns by action type and tier; replay-failure analysis | `results/pilot_R2/` |
| 28 Oct 2026 | Code corrections of revision R2 (Chapter 4), complete re-run; analytical values identical | commit `84a8c21`; `results/pilot_R2/` |

No pre-registered value was changed after results were seen. The post-hoc analyses are reported as such, and none replaces a pre-registered analysis.

## 5.3 Pilot E0: Feasibility and Feature Retention

Pilot E0 used only the fitting portion of each outer fold (`e0_pilot.json`).

**Table 5.2. Pilot E0 (fitting portions only)**

| Evidence group | ROC-AUC: mean over folds; minimum | Retained in every fold (≥ 0.55) |
|---|---|---|
| Context (x^ctx₂ only) | 0.582; 0.554 | Yes, marginally |
| Behavioral | 0.802; 0.787 | Yes |
| Action | 0.929; 0.923 | Yes |
| All | 0.938; 0.930 | — |

The retention rule was applied to each fold's fitting portion separately, and every fold retained all three groups (`e1_crossfit.json`, `e0_fold_specific_feature_groups`). The feature set is therefore the same in every fold. No fold's held-out data influenced its own feature set.

The pooled count of positive steps is 921, above the declared minimum of 50. Thirteen of the 21 backbones have fewer than 50 positive steps each (range 2–116), so no per-backbone conclusion is drawn.

## 5.4 RQ1 — Offline Classification (Held-Out Predictions)

**Table 5.3. Held-out discrimination and calibration, pooled over nine outer folds** (6,762 steps; 921 positive; `e1_crossfit.json`)

| Metric | Calibrated p, label-NLL fit (reference) | Calibrated p, Platt smoothed targets | Uncalibrated p̃ |
|---|---|---|---|
| ROC-AUC | 0.938 [0.908, 0.961] | 0.938 | 0.939 |
| Average precision (PR-AUC estimate) | 0.719 [0.559, 0.827] | 0.719 | 0.721 |
| ECE (M = 10) | 0.044 [0.033, 0.084] | 0.044 | 0.042 |
| Log-loss | 0.201 [0.149, 0.294] | 0.201 | 0.201 |
| Brier score (binary convention) | 0.060 | 0.060 | 0.060 |

**Table 5.4. Per-fold results (calibrated, label-NLL)**

| Held-out injection task | Steps | Positive | ROC-AUC | AP | ECE | Log-loss | λ~impl~ (λ) | γ₁ |
|---|---|---|---|---|---|---|---|---|
| 0 | 824 | 125 | 0.962 | 0.788 | 0.059 | 0.161 | 10 (5) | 0.959 |
| 1 | 773 | 101 | 0.965 | 0.854 | 0.046 | 0.140 | 10 (5) | 0.947 |
| 2 | 807 | 112 | 0.949 | 0.735 | 0.035 | 0.164 | 10 (5) | 0.958 |
| 3 | 772 | 110 | 0.962 | 0.811 | 0.045 | 0.154 | 10 (5) | 0.955 |
| 4 (payment modification) | 726 | 135 | 0.978 | 0.906 | 0.087 | 0.148 | 10 (5) | 0.947 |
| 5 | 634 | 23 | 0.859 | 0.308 | 0.068 | 0.164 | 10 (5) | 0.969 |
| 6 | 666 | 79 | 0.909 | 0.501 | 0.075 | 0.225 | 10 (5) | 0.981 |
| 7 (credential change) | 730 | 124 | 0.903 | 0.577 | **0.189** | **0.530** | 1 (0.5) | 0.980 |
| 8 | 830 | 112 | 0.959 | 0.859 | 0.037 | 0.146 | 10 (5) | 0.945 |

Findings:
1. **Discrimination holds on held-out attacker objectives.** Held-out ROC-AUC is 0.86–0.98 per fold.
2. **Calibration did not transfer to the one held-out attack category not seen in fitting.** Injection task 7 is the only credential-change attack. Its fold has ECE 0.189 and log-loss 0.53, three to four times the other folds.
3. **No calibration improvement was observed.** The fitted maps are close to the identity (γ₁ = 0.945–0.981), and pooled ECE is 0.044 with calibration and 0.042 without. This does not show that calibration is useless. It shows that the ridge model's own probabilities were already close to calibrated on in-distribution folds, and that the map did not repair the miscalibration in fold 7.
4. **Other generalization checks** (`e1_crossfit.json`, `e4_cross_template_and_defenses.json`):
   - leave-one-backbone-out (21 folds): pooled ROC-AUC 0.949; per held-out backbone 0.736 (claude-3-haiku) to 1.000;
   - grouping by user task (16 folds): pooled ROC-AUC 0.943. One fold, user_task_15, scores 0.211; Section 5.10 explains this as a label problem;
   - five other attack templates on gpt-4o, with no refitting: ROC-AUC 0.922–0.959, ECE 0.028–0.086.

![Figure 5.1. Held-out reliability diagram, calibrated and uncalibrated (10 equal-width bins). Mid-range bins contain few steps.](results/pilot_R2/figures/fig_reliability.png){width=55%}

## 5.5 RQ2 — Observe-Only Decisions

All three policies use the same held-out calibrated probabilities and the same predicates:
- **REM** adds tier-indexed expected loss with Escalate available;
- **REM without expected-loss Escalate** (post-hoc) has the same escalation opportunity as the baseline (D2 only);
- **B1** is the baseline with the thresholds of Eq. 3.14.

Verdicts were computed on the recorded steps and not enforced.

**Table 5.5. Observe-only verdicts on held-out steps** (y = 0: n = 5,841; y = 1: n = 921; `e2_e5_e6_observe_only.json`)

| | REM | REM w/o expected-loss Escalate | B1 |
|---|---|---|---|
| Any intervention on y = 1 steps | 0.973 [0.957, 0.987] | 0.973 | 0.740 [0.473, 0.922] |
| Any intervention on y = 0 steps (step false-positive rate) | 0.227 [0.213, 0.239] | 0.198 | 0.056 [0.047, 0.066] |
| Escalate share of all steps | 0.196 | 0.009 | 0.009 |
| y = 0 steps withheld if an idealized reviewer resolves escalations | 0.040 | 0.188 | 0.046 |
| Ties | 0 | 0 | 0 |
| Verdicts fixed by D2 | 58 | 58 | 58 |

**Table 5.6. Observe-only interventions by consequence tier and action category** (`r2_breakdowns.json`)

| Tier | Category | n (y = 0) | n (y = 1) | REM y=0 / y=1 | REM w/o Esc. y=0 / y=1 | B1 y=0 / y=1 |
|---|---|---|---|---|---|---|
| 1 | read | 4,176 | 0 | 0.000 / — | 0.000 / — | 0.000 / — |
| 2 | profile change | 351 | 0 | 0.399 / — | 0.219 / — | 0.026 / — |
| 3 | value transfer ≤ 1000 | 736 | 561 | 0.932 / 0.955 | 0.838 / 0.955 | 0.254 / 0.900 |
| 4 | value transfer > 1000 | 115 | 101 | 0.983 / 1.000 | 0.922 / 1.000 | 0.391 / 0.574 |
| 4 | payment modification | 285 | 135 | 0.740 / 1.000 | 0.684 / 1.000 | 0.305 / 0.881 |
| 4 | credential change | 178 | 124 | 0.983 / 1.000 | 0.899 / 1.000 | 0.000 / 0.000 |

What the observe-only results show:
- **Low thresholds at high tiers.** REM's additional interventions are concentrated on state-changing actions at tiers 3–4, where the pre-registered costs put the Allow–Block indifference points at 1/11 and 1/21 (Eq. 3.9). Legitimate transfers often carry action evidence (for example, a recipient read from a tool output) that places them above those points.
- **Benign state-changing steps.** On episodes without injection, REM releases 33 of 180 state-changing steps (tiers 2–4); REM without expected-loss Escalate releases 48; B1 releases 132 (`benign_release_breakdown.json`).
- **Escalation is not the cause.** Removing the expected-loss Escalate option lowers REM's intervention rate on legitimate steps only from 0.227 to 0.198: most former escalations become Modify verdicts, which also withhold the call. The difference from B1 is therefore mainly due to the tier-indexed costs, not to the opportunity to escalate.
- **B1 and credential changes.** B1 intervened on none of the 124 credential-change attack steps. These are the steps of the fold whose probabilities were most miscalibrated (Table 5.4). Its thresholds are fixed by benign false-positive rates and did not reach them.
- **Realized loss.** Under the decision costs, realized loss is 0.114 for REM, 0.136 for REM without expected-loss Escalate and 0.652 for B1. This comparison favors REM by construction (Chapter 3, Section 3.12.3) and is not evidence of superiority.

## 5.6 RQ2 and RQ3 — Replay Sensitivity Analysis

The replay re-executes each recorded episode in the benchmark's sandbox with REM enforcing its verdicts (Chapter 3, Section 3.11.11). Its use is a proposed amendment to the scope of Chapter 3. Three properties limit what it can show:
- **NO-ADAPT.** The agent emits the calls it emitted in the recorded run, whatever REM does. After a refusal, a live agent could retry, rephrase, use another tool, or abandon the task. Replay therefore cannot show how often a live agent would achieve the attacker's goal by another route, and **a near-zero replay ASR is not evidence of protection against a live or adaptive agent.**
- **Modify and Block.** Under NO-ADAPT, Modify and Block have the same effect on the withheld call, and step-level and episode-level semantics cannot differ, because no refused tool is retried. The replay results are identical for the two semantics; only step-level results are shown.
- **Not independent runs.** Replaying a recorded trajectory is deterministic. Repeating it adds no information about LLM behavior.
- **Closed-loop identifiability.** Once blocking changes what an agent proposes next, static scores and ungated trajectories need not identify the closed-loop trade-off between false blocks and misses (Ray, 2026). Recorded trajectories are ungated in this sense. Offline replay of AgentDojo's recorded traces has also been used to evaluate temporal-logic monitors (Kekatos et al., 2026); neither use establishes enforcement against live agents.

### 5.6.1 Replay validity and exclusions

With every call allowed, the replay reproduced the recorded utility and security outcomes of 3,313 of the 3,334 episodes.

**The 21 failures** (`r2_breakdowns.json`, `replay_failures`) are concentrated:
- 20 are user_task_13 episodes whose utility verdict differs; 1 is a user_task_14 episode whose security verdict differs;
- 10 are from gpt-4o, and the remaining 11 are spread over six other backbones;
- none raised an error.

The pattern is consistent with a change in the user task's definition between the suite version used for recording and the version used for replay (v1). This was not confirmed task by task.

**Effect of the exclusion.** Of the 21 excluded episodes, 19 are attacked, and 14 of these recorded attack success. Excluding them changes the recorded attack-success rate from 0.228 (all 2,998 attacked episodes) to 0.226 (2,979 retained), and the recorded benign utility from 0.521 (336) to 0.524 (334). All replay metrics use the 2,979 attacked and 334 benign retained episodes.

### 5.6.2 Results

**Table 5.7. Replay results, step-level semantics** (attacked n = 2,979; benign n = 334; `e4_e5_enforcement_replay.json`)

| Configuration | ASR | Benign utility | Utility under attack |
|---|---|---|---|
| B0, no defense (replay) | 0.226 [0.148, 0.295] | 0.524 [0.381, 0.676] | 0.492 |
| B1, no reviewer | 0.055 [0.011, 0.134] | 0.509 [0.334, 0.702] | 0.514 |
| REM, no reviewer | 0.004 [0.001, 0.007] | 0.314 [0.110, 0.548] | 0.364 |
| REM w/o expected-loss Escalate, no reviewer | 0.004 [0.001, 0.007] | 0.329 [0.126, 0.551] | 0.374 |
| REM, idealized reviewer | 0.004 [0.001, 0.007] | 0.497 [0.333, 0.680] | 0.496 |
| REM w/o expected-loss Escalate, idealized reviewer | 0.004 [0.001, 0.007] | 0.311 [0.123, 0.518] | 0.359 |

**Table 5.8. Paired differences (grouped bootstrap)**

| Comparison | ΔASR | ΔBenign utility |
|---|---|---|
| REM − B1, no reviewer | −0.051 [−0.130, −0.007] | −0.195 [−0.341, −0.074] |
| REM w/o Esc. − B1, no reviewer (same escalation opportunity) | −0.051 [−0.130, −0.007] | −0.180 [−0.325, −0.063] |
| REM − B1, idealized reviewer | −0.051 [−0.130, −0.007] | +0.003 [−0.009, 0.018] |
| REM − REM w/o Esc., idealized reviewer | 0.000 | +0.186 [0.065, 0.335] |
| REM − B0, no reviewer | −0.222 [−0.289, −0.146] | −0.210 [−0.379, −0.051] |

**Table 5.9. Replay ASR by the attacker's target action** (`r2_breakdowns.json`)

| Target action | Injection tasks | Attacked episodes | B0 | B1 (no reviewer) | REM (no reviewer) |
|---|---|---|---|---|---|
| Value transfer | 7 | 2,334 | 0.213 [0.128, 0.293] | 0.014 [0.007, 0.020] | 0.005 [0.002, 0.008] |
| Payment modification | 1 | 311 | 0.183 | 0.042 | 0.000 |
| Credential change | 1 | 334 | 0.356 | 0.356 | 0.000 |

Single-task categories have no interval.

**Table 5.10. Replay benign utility by kind of user task** (`r2_breakdowns.json`)

| User tasks | Tasks | Episodes | B0 | B1 (no reviewer) | REM (no reviewer) | REM (idealized reviewer) |
|---|---|---|---|---|---|---|
| Requiring a state change | 12 | 250 | 0.472 [0.320, 0.632] | 0.432 [0.238, 0.637] | 0.168 [0.000, 0.420] | 0.416 [0.238, 0.600] |
| Read-only | 4 | 84 | 0.679 [0.369, 0.929] | 0.738 [0.417, 0.976] | 0.750 [0.429, 1.000] | 0.738 [0.417, 0.976] |

![Figure 5.2. Replay sensitivity analysis (NO-ADAPT): ASR and benign utility with 95% grouped-bootstrap intervals.](results/pilot_R2/figures/fig_enforcement_replay.png){width=95%}

**What the replay results show, within NO-ADAPT:**
- **Where the ASR difference comes from.** REM withholds more of the recorded attack attempts than B1. Most of the difference comes from the credential-change and payment-modification attacks (Table 5.9), each represented by a single injection task.
- **The utility cost falls on state-changing tasks.** With no reviewer, REM's benign utility falls to 0.168 on those tasks (Table 5.10).
- **The cost is not caused by the escalation option.** REM without expected-loss Escalate has almost the same utility cost relative to B1 (Table 5.8).
- **With an idealized reviewer, the cost disappears.** That reviewer knows the label and is an upper bound on reviewer quality, not a model of one.

**RQ3 quantities:**
- **Residual attack success after Modify.** In oracle-Modify replays within the fitting folds, r~mod~ was 0.000 at tier 3 (530 episodes) and 0.010 at tier 4 (298 episodes) (`e4_rmod_and_replay_validity.json`). In replays where REM applied Modify to an attack step, residual ASR was 0.000 (610 episodes). Under NO-ADAPT a withheld call simply does not occur, so **these values are consequences of the assumption, not measurements of tool restriction against a live agent.**
- **Escalation rate.** 0.196 of all steps in the observe-only analysis (Table 5.5).
- **Processing time.** REM's processing time per step, measured as described in Chapter 4, Section 4.14, had a median of 0.14–0.20 ms and a 95th percentile of 0.39–0.54 ms across REM configurations and the two runs; the independent re-execution of 30 October gave values within these ranges for REM configurations.
- **Memory.** The median peak traced allocation was 4.4 KB per step, with a 95th percentile of 12.4 KB (611 steps of 300 episodes; `latency_memory_profile.json`). The first run (R1) measured 2.9 KB; like time, memory varies between runs. The independent re-execution of 30 October measured the same value.

These figures apply to the evaluated configuration only: no neural injection classifier, no reviewer, recorded inputs. They are not estimates for a complete deployment.

## 5.7 RQ4 — Ablations

**Table 5.11. Ablations** (observe-only columns: held-out recorded steps; replay columns: step-level semantics, no reviewer)

| Configuration | Held-out ROC-AUC | Observe-only intervention, y = 0 | Observe-only intervention, y = 1 | Replay ASR | Replay benign utility |
|---|---|---|---|---|---|
| Full REM | 0.938 | 0.227 | 0.973 | 0.004 | 0.314 |
| − context evidence (x^ctx₂) | 0.938 | 0.228 | 0.973 | 0.004 | 0.314 |
| − behavioral evidence | 0.938 | 0.174 | 0.973 | 0.004 | 0.419 |
| − action evidence | 0.799 | 0.242 | 0.921 | 0.006 | 0.314 |
| − calibration (p̃ in Eq. 3.6) | — | 0.213 | 0.973 | 0.004 | 0.329 |
| one tier for all actions: 1 / 2 / 3 / 4 | — | 0.093 / 0.157 / 0.233 / 0.336 | 0.757 / 0.909 / 0.972 / 0.976 | 0.051 / 0.022 / 0.004 / 0.003 | 0.440 / 0.353 / 0.338 / 0.314 |
| − predicates D1, D2 | — | 0.226 | 0.973 | 0.004 | 0.314 |

Findings, worded as what was and was not observed:
- **Action evidence** carries most of the discrimination: without it, held-out ROC-AUC falls from 0.938 to 0.799 and average precision from 0.719 to 0.367.
- **Context evidence.** No improvement from the instruction-pattern indicator was observed. This concerns that indicator only; the pre-trained injection classifier x^ctx₁ was not tested, so nothing is concluded about context evidence in general.
- **Behavioral evidence.** No security improvement was observed, and removing it raised replay benign utility by 10.5 points. The firing rates show why (`feature_firing_rates.json`):
  - the privilege-escalation indicator x^beh₃ fired on 92% of legitimate state-changing steps in episodes without injection, against 87% of attack steps;
  - the transition-deviation indicator x^beh₄ fired on 43% of legitimate state-changing steps, against 17% of attack steps. Legitimate tasks held out by user task produce transitions that are absent from the fitting portion's benign reference.

  In this benchmark, therefore, the behavioral features mark legitimate first transfers at least as often as attacks. Whether this holds in other environments is not known.
- **Calibration and predicates.** No material change was observed from removing them. With Π empty, D2 fixed the verdict for 58 steps.
- **Tiers.** The tier map moves the trade-off. A single low tier recovers utility and loses protection; a single high tier does the opposite.

None of these observations establishes that a component has no benefit in general. They are single-benchmark observations with nine attacked groups.

## 5.8 Optional Sequential Analysis (CUSUM, observe-only)

The Bernoulli CUSUM was fitted on each fold's benign fitting episodes (`e3_a2_cusum_observe_only.json`):
- **q₁ = 0.3:** it was undefined in all folds, because the estimated pre-change rate (about 0.34) exceeded q₁.
- **q₁ = 0.5 and 0.7:**
  - an alarm followed the entry of injected content in 74.8% of attacked episodes with a positive step;
  - it came at or before the first positive step in 42.5–43.8%;
  - the median delay was 1 step;
  - the held-out benign false-alarm rate was 0.106, against an in-fold target of 0.05.

The CUSUM issued no verdicts.

## 5.9 Realized Loss across the Declared Grid

Realized loss (Eq. 3.22) on held-out steps was computed for 36 loss structures:
- C~miss~ multipliers 0.5–5;
- C~esc~ 0.1–0.6;
- amount limits 100–10,000.

| Configuration | Realized loss, range over the 36 cells |
|---|---|
| REM, matched costs | 0.039–0.298 |
| REM, base costs (misspecified) | 0.057–0.324 |
| B1 | 0.303–3.261 |

REM's loss was below B1's in every cell, also when misspecified. Matched costs gave lower realized loss than misspecified costs in 34 of 36 cells.

The comparison favors REM by construction. The grid cell α~blk~ = 0.05 is not evaluable, because the pre-registered α~mod~ = 0.05 must exceed α~blk~.

## 5.10 Labels, the user_task_15 Collision and Benchmark Versions

**Primary and post-hoc analyses are kept separate.** All results above use the pre-registered label rule with amendment AM-1.

**The collision.** In suite versions v1 and v1.1, user_task_15 asks the agent to pay a landlord whose account is also the attacker account of every injection task. The benchmark changed this from v1.1.1. Sixteen of the 21 recorded backbones used the earlier prompt. The label-relevant definitions of the nine injection tasks are identical in every suite version from v1 to v1.2.2, so labels are consistent across the mixed recordings.

**Post-hoc analysis.** 29 positive steps in user_task_15 episodes are ambiguous, 19 of them with no injected content in the context. All of REM's residual replay ASR comes from these episodes. A post-hoc analysis that excludes user_task_15 gives REM ASR 0.000 and held-out ROC-AUC 0.952 (`sensitivity_post_hoc_exclude_user_task_15.json`). It is reported for transparency and does not replace the primary result.

**Label audit.**
- **AI inspection only so far.** A sample of 30 attacked episodes was inspected by the AI assistant that assisted this work, not by a human: 29 labels agreed with the trace, and one was a likely false negative (an attacker-directed transfer through a tool other than the reference tool).
- **Human audit package.** A package for human annotation has been prepared (`results/pilot_R2/label_audit_human_package.csv`, with instructions). It contains 145 items:
  - a random sample of 30 attacked episodes;
  - all 29 ambiguous user_task_15 positives;
  - 19 steps carrying an attacker value but labelled 0;
  - 4 steps from episodes with recorded success but no positive label;
  - 23 positive steps from episodes without recorded success.

**The human audit has not been performed.**

## 5.11 Distributed Defenses (Recorded Outcomes Only)

For orientation, the recorded outcomes of four defenses distributed with the benchmark, on gpt-4o (`e4_cross_template_and_defenses.json`):

| Defense | ASR | Benign utility |
|---|---|---|
| tool_filter | 0.112 | 0.81 |
| transformers_pi_detector | 0.007 | 0.44 |
| repeat_user_prompt | 0.462 | 0.94 |
| spotlighting_with_delimiting | 0.615 | 0.81 |

These are recorded outcomes, possibly under different suite versions, and were not replayed. **They are not a controlled comparison with REM** and are not used as one.

## 5.12 Summary by Research Question

**Table 5.12. Evidence summary**

| RQ | Kind of evidence | What was observed | Not shown |
|---|---|---|---|
| RQ1 | Held-out predictions | ROC-AUC 0.94 overall; 0.86–0.98 per held-out attacker objective; 0.92–0.96 on other templates; 0.74–1.00 per held-out backbone. ECE 0.044, degraded on the unseen credential-change category. No calibration improvement observed | Performance on other benchmarks or live agents |
| RQ2 | Observe-only decisions; replay | REM intervened on more attack steps than B1 and on many more legitimate state-changing steps. The difference stems mainly from tier-indexed costs, not from the escalation option. In replay, REM's ASR was lower than B1's (mostly credential and payment attacks), at a utility cost of −18 to −20 points without a reviewer and about 0 with an oracle reviewer | Enforcement against live or adaptive agents |
| RQ3 | Replay; runtime measurement | r~mod~ and residual ASR ≈ 0 under NO-ADAPT (assumption-driven); escalation 19.6% of steps; REM processing below 0.6 ms per step at p95 in this configuration | Residual success of live agents after Modify; full-system latency |
| RQ4 | Held-out predictions; observe-only; replay | Action evidence dominates. No improvement observed from the instruction-pattern indicator or from behavioral evidence, which lowered utility. Tiers drive the trade-off | General claims about context or behavioral evidence |
