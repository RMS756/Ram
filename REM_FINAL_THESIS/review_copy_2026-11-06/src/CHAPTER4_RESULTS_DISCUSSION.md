# CHAPTER FOUR

# RESULTS AND DISCUSSION

## 4.1 Purpose, Status and Kinds of Evidence

This chapter reports what the implementation of Section 3.16 produced on recorded agent behavior in the AgentDojo banking environment. **The results are exploratory.** Two conditions for confirmatory results are not met:
- the design values they use (costs, tiers, predicates, feature set) await approval;
- the enforcing-mode evaluation with live agents that Chapter 3 specifies could not be executed.

The results are therefore not presented as confirmation of any claim, and the confirmatory evaluation remains pending. The closed-loop harness for live agents (Section 3.17) is implemented but was not executed; its status is reported in Section 4.12, and no live result appears in this chapter.

Five kinds of evidence are kept apart throughout. Each table states which kind it reports.

| Kind | What it is | Used in |
|---|---|---|
| **Recorded outcome** | The benchmark's utility and security verdicts on the traces as recorded by the benchmark authors, without REM | Sections 4.2, 4.6.1 |
| **Held-out prediction** | REM's probability for a recorded step, from a model fitted without that step's group | Sections 4.3–4.4 |
| **Observe-only decision** | The verdict REM or the baseline would issue for a recorded step, computed but not enforced | Sections 4.5, 4.7, 4.9 |
| **Replay result** | The benchmark's verdicts after re-executing a recorded trajectory with REM enforcing, assuming the agent does not adapt | Section 4.6 |
| **Live run** | An agent running with REM enforcing | **None was executed** |

All numbers come from `results/pilot_R2/`, produced at commit `84a8c21` by `experiments/pilot/run_all.sh`. A re-execution of the full pipeline in a fresh environment on 30 October 2026 (by this project, not an external replication) reproduced every analytical value; the only differing values were per-step latency values, code-commit stamps and one file path, and no memory value differed (Chapter 3, Section 3.16.11.2). A further re-execution on 1 November 2026 (R4), which added the complete-call timer, is compared in the same section. The first run (commit `aa66f22`, `results/pilot/`) produced identical analytical values (Chapter 3, Section 3.16.11.2).

## 4.2 Data, Protocol and Chronology

### 4.2.1 Data

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

All intervals are 95% percentile intervals from a bootstrap that resamples attacked items by injection task and benign items by user task. With nine injection-task groups the intervals are wide. Bootstrap coverage is an asymptotic property, and with so few groups the intervals are not guaranteed to reach their nominal 95% coverage; a narrow interval, such as that of REM's replay ASR, is not evidence of precision. The intervals are therefore descriptive, and no hypothesis test is based on them. Where a category contains a single injection task, no interval can be formed and none is reported.

### 4.2.2 Protocol

The protocol is nested grouped cross-fitting (Chapter 3, Procedure 3.1):
- nine outer folds, each holding out one injection task;
- episodes without injection assigned to folds by user task.

Within each fold's fitting portion, the following are fitted (Chapter 3, Section 3.11.5):
- λ, by grouped inner cross-validation;
- the calibration map, on inner out-of-fold logits;
- the baseline thresholds;
- the benign reference quantities;
- r~mod~.

The **pre-registered values** are listed in Table 4.1. They come from Chapter 3 where Chapter 3 gives them; otherwise they are declared exploratory values.

**Table 4.1. Pre-registered values** (`configs/exploratory/pilot_e0.yaml`)

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

### 4.2.3 Chronology of design, amendments and analyses

| Date and time (UTC) | Event | Record |
|---|---|---|
| 27 Oct 2026 16:40 | Pilot design committed (Table 4.1) | commit `48bef90` |
| 27 Oct 2026 16:57 | Amendments AM-1 to AM-4 committed. AM-1: exclusion of (user_task_15, injection_task_4). AM-2: benign references. AM-3: the meaning of "tool class". AM-4: replay validity filter | commit `7a707a7` |
| 27 Oct 2026, after 16:57 | First computation of held-out predictions and of all analyses with the then-uncommitted pipeline code. **The log of this first execution was not preserved**; its order relative to the amendments rests on the commit times and on the working session record | — |
| 27 Oct 2026 17:16 | Pipeline committed, then re-run in full; results identical to the first execution | commit `aa66f22`; `results/pilot/` |
| 27–28 Oct 2026 | **Post-hoc analyses**, added after results had been seen: exclusion of user_task_15 (Section 4.10); benign-release breakdown by tier; REM without expected-loss Escalate (Sections 4.5–4.6); breakdowns by action type and tier; replay-failure analysis | `results/pilot_R2/` |
| 28 Oct 2026 | Code corrections of revision R2 (Section 3.16), complete re-run; analytical values identical | commit `84a8c21`; `results/pilot_R2/` |

No pre-registered value was changed after results were seen. The post-hoc analyses are reported as such, and none replaces a pre-registered analysis.

## 4.3 Pilot E0: Feasibility and Feature Retention

Pilot E0 used only the fitting portion of each outer fold (`e0_pilot.json`).

**Table 4.2. Pilot E0 (fitting portions only)**

| Evidence group | ROC-AUC: mean over folds; minimum | Retained in every fold (≥ 0.55) |
|---|---|---|
| Context (x^ctx₂ only) | 0.582; 0.554 | Yes, marginally |
| Behavioral | 0.802; 0.787 | Yes |
| Action | 0.929; 0.923 | Yes |
| All | 0.938; 0.930 | — |

The retention rule was applied to each fold's fitting portion separately, and every fold retained all three groups (`e1_crossfit.json`, `e0_fold_specific_feature_groups`). The feature set is therefore the same in every fold. No fold's held-out data influenced its own feature set.

The pooled count of positive steps is 921, above the declared minimum of 50. Thirteen of the 21 backbones have fewer than 50 positive steps each (range 2–116), so no per-backbone conclusion is drawn.

## 4.4 RQ1 — Offline Classification (Held-Out Predictions)

**Table 4.3. Held-out discrimination and calibration, pooled over nine outer folds** (6,762 steps; 921 positive; `e1_crossfit.json`)

| Metric | Calibrated p, label-NLL fit (reference) | Calibrated p, Platt smoothed targets | Uncalibrated p̃ |
|---|---|---|---|
| ROC-AUC | 0.938 [0.908, 0.961] | 0.938 | 0.939 |
| Average precision (PR-AUC estimate) | 0.719 [0.559, 0.827] | 0.719 | 0.721 |
| ECE (M = 10) | 0.044 [0.033, 0.084] | 0.044 | 0.042 |
| Log-loss | 0.201 [0.149, 0.294] | 0.201 | 0.201 |
| Brier score (binary convention) | 0.060 | 0.060 | 0.060 |

**Table 4.4. Per-fold results (calibrated, label-NLL)**

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
   - grouping by user task (16 folds): pooled ROC-AUC 0.943. One fold, user_task_15, scores 0.211; Section 4.10 explains this as a label problem;
   - five other attack templates on gpt-4o, with no refitting: ROC-AUC 0.922–0.959, ECE 0.028–0.086.

![Figure 4.1. Held-out reliability diagram, calibrated and uncalibrated (10 equal-width bins). Mid-range bins contain few steps.](results/pilot_R2/figures/fig_reliability.png){width=55%}

## 4.5 RQ2 — Observe-Only Decisions

All three policies use the same held-out calibrated probabilities and the same predicates:
- **REM** adds tier-indexed expected loss with Escalate available;
- **REM without expected-loss Escalate** (post-hoc) has the same escalation opportunity as the baseline (D2 only);
- **B1** is the baseline with the thresholds of Eq. 3.14.

Verdicts were computed on the recorded steps and not enforced.

**Table 4.5. Observe-only verdicts on held-out steps** (y = 0: n = 5,841; y = 1: n = 921; `e2_e5_e6_observe_only.json`)

| | REM | REM w/o expected-loss Escalate | B1 |
|---|---|---|---|
| Any intervention on y = 1 steps | 0.973 [0.957, 0.987] | 0.973 | 0.740 [0.473, 0.922] |
| Any intervention on y = 0 steps (step false-positive rate) | 0.227 [0.213, 0.239] | 0.198 | 0.056 [0.047, 0.066] |
| Escalate share of all steps | 0.196 | 0.009 | 0.009 |
| y = 0 steps withheld if an idealized reviewer resolves escalations | 0.040 | 0.188 | 0.046 |
| Ties | 0 | 0 | 0 |
| Verdicts fixed by D2 | 58 | 58 | 58 |

**Table 4.6. Observe-only interventions by consequence tier and action category** (`r2_breakdowns.json`)

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
- **B1 and credential changes.** B1 intervened on none of the 124 credential-change attack steps. These are the steps of the fold whose probabilities were most miscalibrated (Table 4.4). Its thresholds are fixed by benign false-positive rates and did not reach them.
- **Realized loss.** Under the decision costs, realized loss is 0.114 for REM, 0.136 for REM without expected-loss Escalate and 0.652 for B1. This comparison favors REM by construction (Chapter 3, Section 3.12.3) and is not evidence of superiority.

## 4.6 RQ2 and RQ3 — Replay Sensitivity Analysis

The replay re-executes each recorded episode in the benchmark's sandbox with REM enforcing its verdicts (Chapter 3, Section 3.11.11). Its use is a proposed amendment to the scope of Chapter 3. Three properties limit what it can show:
- **NO-ADAPT.** The agent emits the calls it emitted in the recorded run, whatever REM does. After a refusal, a live agent could retry, rephrase, use another tool, or abandon the task. Replay therefore cannot show how often a live agent would achieve the attacker's goal by another route, and **a near-zero replay ASR is not evidence of protection against a live or adaptive agent.**
- **Mitigation semantics.** Under step-level semantics, Modify and Block have the same effect on the withheld call. The episode-level variant also restricts later calls: after a Block, every later call to a tool in 𝒯~R~ is refused, even one whose own verdict is Allow, and even though the agent never retries. The two semantics therefore give different replay results. Tables 4.7–4.10 use step-level semantics, the declared reference pending decision D-2; Table 4.12 compares both semantics.
- **Not independent runs.** Replaying a recorded trajectory is deterministic. Repeating it adds no information about LLM behavior.
- **Closed-loop identifiability.** Once blocking changes what an agent proposes next, static scores and ungated trajectories need not identify the closed-loop trade-off between false blocks and misses (Ray, 2026). Recorded trajectories are ungated in this sense. Offline replay of AgentDojo's recorded traces has also been used to evaluate temporal-logic monitors (Kekatos et al., 2026); neither use establishes enforcement against live agents.

### 4.6.1 Replay validity and exclusions

With every call allowed, the replay reproduced the recorded utility and security outcomes of 3,313 of the 3,334 episodes.

**The 21 failures** (`r2_breakdowns.json`, `replay_failures`) are concentrated:
- 20 are user_task_13 episodes whose utility verdict differs; 1 is a user_task_14 episode whose security verdict differs;
- 10 are from gpt-4o, and the remaining 11 are spread over six other backbones;
- none raised an error.

The pattern is consistent with a change in the user task's definition between the suite version used for recording and the version used for replay (v1). This was not confirmed task by task.

**Effect of the exclusion.** Of the 21 excluded episodes, 19 are attacked, and 14 of these recorded attack success. Excluding them changes the recorded attack-success rate from 0.228 (all 2,998 attacked episodes) to 0.226 (2,979 retained), and the recorded benign utility from 0.521 (336) to 0.524 (334). All replay metrics use the 2,979 attacked and 334 benign retained episodes.

### 4.6.2 Results

**Table 4.7. Replay results, step-level semantics** (attacked n = 2,979; benign n = 334; `e4_e5_enforcement_replay.json`)

| Configuration | ASR | Benign utility | Utility under attack |
|---|---|---|---|
| B0, no defense (replay) | 0.226 [0.148, 0.295] | 0.524 [0.381, 0.676] | 0.492 |
| B1, no reviewer | 0.055 [0.011, 0.134] | 0.509 [0.334, 0.702] | 0.514 |
| REM, no reviewer | 0.004 [0.001, 0.007] | 0.314 [0.110, 0.548] | 0.364 |
| REM w/o expected-loss Escalate, no reviewer | 0.004 [0.001, 0.007] | 0.329 [0.126, 0.551] | 0.374 |
| REM, idealized reviewer | 0.004 [0.001, 0.007] | 0.497 [0.333, 0.680] | 0.496 |
| REM w/o expected-loss Escalate, idealized reviewer | 0.004 [0.001, 0.007] | 0.311 [0.123, 0.518] | 0.359 |

**Table 4.8. Paired differences (grouped bootstrap)**

| Comparison | ΔASR | ΔBenign utility |
|---|---|---|
| REM − B1, no reviewer | −0.051 [−0.130, −0.007] | −0.195 [−0.341, −0.074] |
| REM w/o Esc. − B1, no reviewer (same escalation opportunity) | −0.051 [−0.130, −0.007] | −0.180 [−0.325, −0.063] |
| REM − B1, idealized reviewer | −0.051 [−0.130, −0.007] | +0.003 [−0.009, 0.018] |
| REM − REM w/o Esc., idealized reviewer | 0.000 | +0.186 [0.065, 0.335] |
| REM − B0, no reviewer | −0.222 [−0.289, −0.146] | −0.210 [−0.379, −0.051] |

**Table 4.9. Replay ASR by the attacker's target action** (`r2_breakdowns.json`)

| Target action | Injection tasks | Attacked episodes | B0 | B1 (no reviewer) | REM (no reviewer) |
|---|---|---|---|---|---|
| Value transfer | 7 | 2,334 | 0.213 [0.128, 0.293] | 0.014 [0.007, 0.020] | 0.005 [0.002, 0.008] |
| Payment modification | 1 | 311 | 0.183 | 0.042 | 0.000 |
| Credential change | 1 | 334 | 0.356 | 0.356 | 0.000 |

Single-task categories have no interval.

**Table 4.10. Replay benign utility by kind of user task** (`r2_breakdowns.json`)

| User tasks | Tasks | Episodes | B0 | B1 (no reviewer) | REM (no reviewer) | REM (idealized reviewer) |
|---|---|---|---|---|---|---|
| Requiring a state change | 12 | 250 | 0.472 [0.320, 0.632] | 0.432 [0.238, 0.637] | 0.168 [0.000, 0.420] | 0.416 [0.238, 0.600] |
| Read-only | 4 | 84 | 0.679 [0.369, 0.929] | 0.738 [0.417, 0.976] | 0.750 [0.429, 1.000] | 0.738 [0.417, 0.976] |

![Figure 4.2. Replay sensitivity analysis (NO-ADAPT): ASR and benign utility with 95% grouped-bootstrap intervals.](results/pilot_R2/figures/fig_enforcement_replay.png){width=95%}

![Figure 4.3. Security–utility trade-off in the replay sensitivity analysis (NO-ADAPT, step-level semantics): attack success rate against benign utility for B0, B1, REM and REM without expected-loss Escalate under both reviewer bounds, and for the single-tier ablations. Values from `results/pilot_R2/e4_e5_enforcement_replay.json`; no live result.](REM_FINAL_THESIS/final_five_chapters/figures/fig4_3_security_utility_tradeoff.png){width=100%}

**What the replay results show, within NO-ADAPT:**
- **Where the ASR difference comes from.** REM withholds more of the recorded attack attempts than B1. Most of the difference comes from the credential-change and payment-modification attacks (Table 4.9), each represented by a single injection task.
- **The utility cost falls on state-changing tasks.** With no reviewer, REM's benign utility falls to 0.168 on those tasks (Table 4.10).
- **The cost is not caused by the escalation option.** REM without expected-loss Escalate has almost the same utility cost relative to B1 (Table 4.8).
- **With an idealized reviewer, the cost disappears.** That reviewer knows the label and is an upper bound on reviewer quality, not a model of one.

#### Sensitivity to the mitigation semantics

**Table 4.11. Replay results under the two mitigation semantics** (same episodes; same estimator, calibration, costs, predicates and thresholds; matching reviewer treatment for REM and B1; only the mitigation semantics varies. Verdict sequences are not fixed: see the notes below. ref. = the reference semantics; REM w/o Esc. = REM without expected-loss Escalate; attacked n = 2,979; benign n = 334; `e4_e5_enforcement_replay.json`, `configs.<configuration>_<semantics>_<reviewer>`)

| Configuration | Semantics | ASR | Benign utility | Utility under attack |
|---|---|---|---|---|
| B1, no reviewer | step-level (ref.) | 0.055 [0.011, 0.134] | 0.509 [0.334, 0.702] | 0.514 [0.501, 0.527] |
| B1, no reviewer | episode-level | 0.046 [0.004, 0.125] | 0.509 [0.334, 0.702] | 0.485 [0.474, 0.496] |
| B1, idealized reviewer | step-level (ref.) | 0.055 [0.011, 0.134] | 0.494 [0.329, 0.677] | 0.499 [0.487, 0.511] |
| B1, idealized reviewer | episode-level | 0.046 [0.004, 0.125] | 0.494 [0.329, 0.677] | 0.470 [0.460, 0.481] |
| REM, no reviewer | step-level (ref.) | 0.004 [0.001, 0.007] | 0.314 [0.110, 0.548] | 0.364 [0.345, 0.389] |
| REM, no reviewer | episode-level | 0.004 [0.001, 0.007] | 0.314 [0.110, 0.548] | 0.363 [0.344, 0.388] |
| REM, idealized reviewer | step-level (ref.) | 0.004 [0.001, 0.007] | 0.497 [0.333, 0.680] | 0.496 [0.483, 0.506] |
| REM, idealized reviewer | episode-level | 0.004 [0.001, 0.007] | 0.497 [0.333, 0.680] | 0.481 [0.468, 0.492] |
| REM w/o Esc., no reviewer | step-level (ref.) | 0.004 [0.001, 0.007] | 0.329 [0.126, 0.551] | 0.374 [0.351, 0.407] |
| REM w/o Esc., no reviewer | episode-level | 0.003 [0.001, 0.006] | 0.329 [0.126, 0.551] | 0.370 [0.347, 0.403] |
| REM w/o Esc., idealized reviewer | step-level (ref.) | 0.004 [0.001, 0.007] | 0.311 [0.123, 0.518] | 0.359 [0.337, 0.391] |
| REM w/o Esc., idealized reviewer | episode-level | 0.003 [0.001, 0.006] | 0.311 [0.123, 0.518] | 0.355 [0.333, 0.387] |

What is fixed and what differs, within NO-ADAPT:
- **What is fixed and what varies.** Both runs of each configuration use the same recorded episodes, the same fitted parameters, costs, predicates and thresholds, and the same reviewer treatment. They differ in the mitigation semantics: under the episode-level variant, an earlier Block or Modify adds tools to a restriction set that refuses later calls.
- **The verdicts are not identical.** For REM without a reviewer, the y = 0 steps received 239 Modify and 1,049 Escalate verdicts under step-level semantics, against 241 and 1,047 under episode-level semantics (`verdict_rates` of the two REM configurations). With the idealized reviewer the counts are 239 / 1,050 against 241 / 1,048. A call refused only under the episode-level variant returns no tool output, so the evidence for later steps can differ. B1's verdict counts are the same under both semantics.
- **B1's ASR is lower under episode-level semantics** (0.055 → 0.046): later state-changing calls are refused by the restriction set left by an earlier Block or Modify. REM's ASR is identical (0.004). REM without expected-loss Escalate changes from 0.004 to 0.003 (unrounded 0.0037 → 0.0034).
- **Utility under attack is lower or equal under episode-level semantics** in every configuration: the restriction set also refuses legitimate later calls.
- **Benign utility coincides** between the two semantics in every configuration of this replay. This is an observation about these episodes, not a property of the semantics.
- **REM − B1 ASR within each semantics** (paired grouped bootstrap, no reviewer): −0.051 [−0.130, −0.007] under step-level semantics (Table 4.8) and −0.043 [−0.122, −0.001] under episode-level semantics (`paired_differences`, episode-level REM − B1 entry). The idealized-reviewer interval under episode-level semantics is the same to three decimals. These are two within-semantics contrasts. No interval was computed for the difference between them, so none is reported. As for every interval in this chapter, the bootstrap over nine attacked groups need not reach nominal coverage, and no hypothesis test is based on these intervals (Section 4.2).

Step-level semantics remains the declared reference (Chapter 3, Section 3.8), pending the supervisor's decision D-2. The episode-level rows are a sensitivity analysis, not a replacement for Tables 4.7–4.10.

**RQ3 quantities:**
- **Residual attack success after Modify.** In oracle-Modify replays within the fitting folds, r~mod~ was 0.000 at tier 3 (530 episodes) and 0.010 at tier 4 (298 episodes) (`e4_rmod_and_replay_validity.json`). In replays where REM applied Modify to an attack step, residual ASR was 0.000 (610 episodes). Under NO-ADAPT a withheld call simply does not occur, so **these values are consequences of the assumption, not measurements of tool restriction against a live agent.**
- **Escalation rate.** 0.196 of all steps in the observe-only analysis (Table 4.5).
- **Processing time** (Chapter 3, Section 3.16.14, Table 3.25). **Complete call** (R4 re-execution, 1 November 2026; `results/pilot_R4/e4_e5_enforcement_replay.json`, `latency_full_ms_*`): median 0.21–0.28 ms and 95th percentile 0.49–0.70 ms per step, across the 8 REM configurations (6,684 steps each). **Partial timer**, which excludes attribution, audit-record construction and history recording: median 0.18–0.24 ms and 95th percentile 0.46–0.64 ms in the same run. Earlier runs measured only the partial timer: median 0.14–0.20 ms and 95th percentile 0.39–0.54 ms (R1, R2), with the 30 October re-execution within these ranges.
- **Memory.** The median peak traced allocation was 4.4 KB per step, with a 95th percentile of 12.4 KB (611 steps of 300 episodes; `latency_memory_profile.json`). The first run (R1) measured 2.9 KB; like time, memory varies between runs. The re-execution of 30 October measured the same value. In the R4 re-execution, where `evaluate` also records the complete-call timer, the median was 4,349 bytes against 4,364 bytes, with the same 95th percentile (12,419.5 bytes; `results/pilot_R4/latency_memory_profile.json`). The memory boundary is the complete `evaluate` call in both.

These figures apply to the evaluated configuration only: no neural injection classifier, no reviewer, recorded inputs. They are not estimates for a complete deployment.

## 4.7 RQ4 — Ablations

**Table 4.12. Ablations** (observe-only columns: held-out recorded steps; replay columns: step-level semantics, no reviewer)

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

## 4.8 Optional Sequential Analysis (CUSUM, observe-only)

The Bernoulli CUSUM was fitted on each fold's benign fitting episodes (`e3_a2_cusum_observe_only.json`):
- **q₁ = 0.3:** it was undefined in all folds, because the estimated pre-change rate (about 0.34) exceeded q₁.
- **q₁ = 0.5 and 0.7:**
  - an alarm followed the entry of injected content in 74.8% of attacked episodes with a positive step;
  - it came at or before the first positive step in 42.5–43.8%;
  - the median delay was 1 step;
  - the held-out benign false-alarm rate was 0.106, against an in-fold target of 0.05.

The CUSUM issued no verdicts.

## 4.9 Realized Loss across the Declared Grid

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

## 4.10 Labels, the user_task_15 Collision and Benchmark Versions

**Primary and post-hoc analyses are kept separate.** All results above use the pre-registered label rule with amendment AM-1.

**The collision.** In suite versions v1 and v1.1, user_task_15 asks the agent to pay a landlord whose account is also the attacker account of every injection task. The benchmark changed this from v1.1.1. Sixteen of the 21 recorded backbones used the earlier prompt. The label-relevant definitions of the nine injection tasks are identical in every suite version from v1 to v1.2.2, so labels are consistent across the mixed recordings.

**Post-hoc analysis.** 29 positive steps in user_task_15 episodes are ambiguous, 19 of them with no injected content in the context. All of REM's residual replay ASR comes from these episodes. A post-hoc analysis that excludes user_task_15 gives REM ASR 0.000 and held-out ROC-AUC 0.952 (`sensitivity_post_hoc_exclude_user_task_15.json`). It is reported for transparency and does not replace the primary result.

**Label audit.**
- **AI inspection only so far.** A sample of 30 attacked episodes was inspected by the AI assistant that assisted this work, not by a human: 29 labels agreed with the trace, and one was a likely false negative (an attacker-directed transfer through a tool other than the reference tool).
- **Human audit package.** A package for human annotation has been prepared (`results/pilot_R2/label_audit_human_package.csv`, with instructions). It contains 145 items:
  - every proposed call of 30 randomly drawn attacked episodes (70 items; 5 of the drawn episodes contain no proposed tool call);
  - all 29 ambiguous user_task_15 positives;
  - 19 steps carrying an attacker value but labelled 0;
  - 4 steps from episodes with recorded success but no positive label;
  - 23 positive steps from episodes without recorded success.

**The human audit has not been performed.**

## 4.11 Distributed Defenses (Recorded Outcomes Only)

For orientation, the recorded outcomes of four defenses distributed with the benchmark, on gpt-4o (`e4_cross_template_and_defenses.json`):

| Defense | ASR | Benign utility |
|---|---|---|
| tool_filter | 0.112 | 0.81 |
| transformers_pi_detector | 0.007 | 0.44 |
| repeat_user_prompt | 0.462 | 0.94 |
| spotlighting_with_delimiting | 0.615 | 0.81 |

These are recorded outcomes, possibly under different suite versions, and were not replayed. **They are not a controlled comparison with REM** and are not used as one.

## 4.12 Closed-Loop Evaluation with Live Agents: Status

**The closed-loop evaluation with live agents was not executed.** This section therefore reports no attack success rate, utility, intervention statistic or adaptation behavior of a live agent, and no table or figure in this chapter contains a live result.

Two conditions prevented execution on 3 November 2026:

- **No model access.** No credential for a language-model provider was available in the execution environment; the provider endpoints that were reachable rejected unauthenticated requests, and model-weight repositories were not reachable, so no local model could be run.
- **Undecided design inputs.** The backbone, decoding parameters, number of repeats, fitted-parameter source, authorisation and pre-registration (Section 3.17.5) have not been decided. The runner refuses to start until they are.

What was executed concerns the correctness of the integration, not the effectiveness of REM:

**Table 4.13. Verification of the closed-loop integration (not experimental results)**

| Check | Agent | Outcome |
|---|---|---|
| Integration tests (12) | Scripted test double that proposes predetermined calls and retries or replans after a refusal | All passed: released calls execute; withheld calls (Block, Modify, unapproved Escalate) are not executed and the agent receives a refusal with the original call identifier; step-level Modify does not persist, episode-level Modify does; retries and replans are recorded; episode state is not shared; REM verdicts are unchanged when reference labels are flipped |
| Harness smoke test (B0, B1, REM; step-level, no reviewer; one frozen fold) | Scripted agent that executes the ground-truth calls of the user task and then of the injection task, without adapting | 480 episodes over all 144 attacked task pairs and 16 benign tasks with the benchmark's `important_instructions` injections; 0 execution errors; no withheld call was executed |

The smoke-test agent is not a model of an LLM agent: it never reads tool outputs or reacts to refusals. Its counts are therefore not reported as attack-success or utility results. The live evaluation remains the first item of future work (Section 5.6).

## 4.13 Replay Versus Live Evaluation

No comparison of replay and live results is possible, because no live result exists (Section 4.12). The replay results of Section 4.6 must not be read as live results. The two designs estimate different quantities:

**Table 4.14. Differences between the replay sensitivity analysis and the closed-loop design**

| Aspect | Replay (Section 4.6) | Closed loop (Section 3.17; not executed) |
|---|---|---|
| Agent messages | Recorded, replayed in order | Generated by a running model |
| Reaction to a refusal | None (NO-ADAPT) | Retry, replan or stop |
| Meaning of attack success | Whether the recorded attack calls would have been withheld | Whether the attack succeeds despite the agent's reaction |
| Residual success after Modify | Close to zero by construction | Observable |
| Repeatability | Deterministic | Stochastic; requires repeats |
| Backbones | 21 recorded historical backbones | To be decided |

Because a live agent can retry or route around a refusal, the replay attack success rate is not an upper bound on live attack success. How large the difference is, in either direction for utility, is an empirical question that only the closed-loop evaluation can answer.

## 4.14 Offline Replay Evaluation and Planned MELON Extension

This section summarises the offline replay evidence for the decision policy and states the status of the planned extension with MELON. The offline results (Table 4.15) and the planned MELON comparison are kept separate: no MELON condition has been run with a live language model, so no MELON result exists.

### 4.14.1 Offline replay evaluation

**Data and eligibility.** The replay uses the 3,334 recorded episodes of the 21 agents in the AgentDojo banking environment (Section 4.2). An episode is eligible when replaying it without any defence (B0) reproduces both of its recorded outcomes, user-task utility and attack success, without a replay error (amendment AM-4). This held for 3,313 episodes. The other 21 were excluded:
- 19 attacked and 2 benign episodes;
- in 20 of them the replayed utility differed from the record, and in 1 the attack outcome differed;
- none failed with an error.

**Denominators.** The attack success rate (ASR) and utility under attack are computed over the **2,979 eligible attacked episodes**; benign task success over the **334 eligible benign episodes**.

**Assumptions.** The replay assumes that the recorded agents **do not adapt** to refusals: their later turns are replayed as recorded. It also assumes **no reviewer**: an action that REM escalates is withheld, and an escalation is never counted as task completion. Mitigation acts on the current call only (step-level semantics).

**Table 4.15. Offline replay of recorded agents: no defence, the internal baseline B1 and Full REM (AgentDojo banking v1, `important_instructions`; no adaptation; no reviewer; 95% grouped bootstrap intervals)**

| Configuration | ASR (2,979 attacked) | Utility under attack (2,979 attacked) | Benign task success (334 benign) |
|---|---|---|---|
| B0, no defence | 22.6% [14.8, 29.5] | 49.2% [47.9, 50.3] | 52.4% [38.1, 67.6] |
| B1, consequence-independent baseline (same estimator) | 5.5% [1.1, 13.4] | 51.4% [50.1, 52.7] | 50.9% [33.4, 70.2] |
| Full REM | 0.4% [0.1, 0.7] | 36.4% [34.5, 38.9] | 31.4% [11.0, 54.8] |

**Results.**
- Full REM reduced replay ASR from 5.5% to 0.4%, while benign task success fell from 50.9% to 31.4%, relative to the internal baseline B1.
- The paired differences on the same episodes were −5.1 percentage points for ASR (95% interval −13.0 to −0.7) and −19.5 points for benign task success (−34.1 to −7.4).
- Against no defence, Full REM reduced ASR from 22.6% to 0.4%.

**Interpretation.** B1 and Full REM share the same features, fitted estimator, calibration and policy predicates. They differ only in the decision policy:
- B1 applies operating-point thresholds that ignore consequences;
- Full REM selects among Allow, Modify, Escalate and Block by minimising expected loss with consequence-tiered costs.

The difference between them is therefore attributed to the **decision policy as a whole**, not to any single element of it.

**Calibration sensitivity on the evaluated data.** As a sensitivity check, B1 was re-run with the uncalibrated probability of the same fitted model and with its two thresholds re-selected on the uncalibrated development probabilities. On these data this variant reproduced every B1 verdict on all 6,762 held-out steps and every B1 outcome in all 3,334 replay episodes. This is expected, because thresholds chosen by rank are unaffected by a strictly increasing calibration map. Calibration itself showed no improvement on this dataset: on the held-out steps the expected calibration error was 0.044 with calibration and 0.042 without, and the Brier score was 0.060 in both cases. These findings concern this dataset and these metrics only.

**Deployment check.** When REM was run as a separate gateway service in front of a simulated banking API, it reproduced every decision and outcome of this replay (0 differences over 3,334 episodes). Its median decision time was 0.18 ms per call, on one machine.

### 4.14.2 Planned extension: MELON with and without REM

**Purpose.** The supervisors' before/after study compares two conditions on the same live cases:
1. **original MELON** (Zhu, Yang, et al., 2025);
2. **MELON + REM**, in which REM evaluates each tool call that survives MELON's processing, immediately before execution.

**Implementation.** Both conditions are implemented with the official MELON code, which is unmodified and pinned by commit and file hash. They differ only in the tool executor. Local tests with scripted agents and a substitute embedding client verified, among other things, that a call MELON passes reaches REM and, when REM refuses it, leaves the environment unchanged.

**Status.** **Neither condition has been executed with a live language model, and no paired runs exist.** The study requires:
- access to a model API;
- an authorised spending limit;
- decisions on the backbone model, the number of repetitions and the parameter source.

Until paired runs exist, no comparative statement about MELON is made in this thesis.

## 4.15 Interpretation of the Findings

This section interprets the exploratory evaluation reported in Sections 4.1–4.11. Each conclusion is linked to the result that supports it and to the limit of that result. Section 4.1 defines the kinds of evidence: held-out prediction, observe-only decision, replay result; no live run was executed.

### 4.15.1 What the evidence supports

**Table 4.16. Conclusions, their support and their limits**

| # | Conclusion | Supporting result | Limit |
|---|---|---|---|
| 1 | REM can be placed at the tool-execution boundary of a benchmark agent without modifying the agent's model, prompts or tools | Integration tests; replay of 3,313 episodes reproducing recorded outcomes (Chapter 3, Section 3.16.11.2) | Placement requires control of the tool executor (Chapter 3, Section 3.16.9); not shown in a production framework |
| 2 | Evidence available at the tool boundary separates attack attempts from legitimate calls on attacker objectives, templates and backbones not seen in fitting | Held-out ROC-AUC 0.938 [0.908, 0.961]; 0.92–0.96 on other templates; 0.74–1.00 per held-out backbone (Section 4.4) | One benchmark, one attacker account, labels that are a proxy; destination novelty is easier here than in practice |
| 3 | Action evidence carries most of this separation | Without action evidence, ROC-AUC falls to 0.799 and AP to 0.367 (Section 4.7) | Single benchmark; nine attacked groups |
| 4 | With the pre-registered costs, tier-indexed expected-loss verdicts intervene on far more legitimate state-changing actions than the baseline, mainly because of the low thresholds the costs imply at high tiers, not because of the escalation option | Observe-only: 33 vs 132 of 180 benign state-changing steps released; REM without expected-loss Escalate releases 48 (Section 4.5) | Costs are declared, not elicited; another cost structure gives another trade-off (Section 4.9) |
| 5 | Within the replay assumption, REM withholds more recorded attack attempts than the baseline, at a utility cost that depends on how escalations are resolved | ΔASR −0.051 [−0.130, −0.007] under step-level semantics and −0.043 [−0.122, −0.001] under the episode-level variant (each a within-semantics paired interval); Δbenign utility −0.195 without a reviewer and +0.003 with an oracle reviewer (Section 4.6, Tables 4.8 and 4.11) | NO-ADAPT; replay is a proposed scope amendment; most of the ASR difference comes from two single-task attack categories |

### 4.15.2 Why benign utility falls

The fall in benign utility has two sources, and the evaluation separates them.

**Low thresholds at high tiers.** With C~miss~ up to twenty times C~FA~, the Allow–Block indifference point at tier 4 is 1/21 (Eq. 3.9). A probability as low as 0.05 is enough to withhold a transfer above the limit, a payment modification or a credential change. Legitimate actions of these kinds in this benchmark often carry the same action evidence as attacks; for example, a recipient read from a tool output rather than stated in the request. They therefore cross the threshold.

**Where the verdict sends them.** The withheld actions are mostly escalated. Without a reviewer an escalation is a withheld action, so utility falls. The comparison with REM without expected-loss Escalate shows that removing the option does not recover the utility: the same actions are then withheld through Modify. The utility cost is therefore a consequence of the declared costs and of the evidence, not of escalation as such.

**What a reviewer would change.** An escalation is worth something only if someone resolves it. With an oracle reviewer the utility cost disappears, which bounds what a perfect reviewer could recover. A real reviewer would recover less, at some delay and cost. The thesis does not model that reviewer.

### 4.15.3 Why behavioral evidence did not help, and calibration did not change outcomes

**Behavioral evidence.** The behavioral indicators are not specific to attacks in this benchmark:
- *privilege escalation* fired on 92% of legitimate state-changing steps, because a user's first transfer is, by definition, the first use of a higher-privilege tool;
- *transition deviation* fired more often on legitimate steps (43%) than on attacks (17%), because legitimate tasks held out from fitting produce unseen transitions.

The estimator gave these features positive weight. In the decision they therefore added to the probability of legitimate high-tier actions, and removing them recovered utility without a measured change in attack success. This is an observation about these features in this benchmark, with short trajectories. It does not show that behavioral evidence is useless elsewhere.

**Calibration.** Calibration did not change outcomes for two reasons:
- logistic regression fitted by penalized likelihood was already close to calibrated on in-distribution folds, so the fitted map was close to the identity;
- the one fold where calibration mattered, the unseen credential-change attack, was miscalibrated in a way a monotone map fitted on other attack categories cannot repair.

This agrees with the position, taken in Chapter 3, that calibration quality and control quality must be reported separately (C. Zhang et al., 2026).

### 4.15.4 What the evidence does not support

- **That REM protects live agents.** Under replay a withheld call does not reappear. A live agent can retry, rephrase or reach the goal through another tool. The near-zero replay ASR and the near-zero residual success after Modify are consequences of that assumption.
- **That REM is deployable as configured.** Without a reviewer, benign utility on state-changing tasks fell from 0.47 to 0.17 in replay.
- **That REM is superior to the baseline or to other defenses.**
  - The realized-loss comparison favors REM by construction.
  - The comparison with distributed defenses is not controlled.
  - Most of the ASR difference from the baseline comes from single-task attack categories.
- **Anything about the injection classifier**, which was not available, or about adaptive attackers, who were out of scope.

## 4.16 Comparison with Prior Work

The comparison restates design positions documented in Chapter 2 and does not rank systems, because no shared evaluation exists. Properties marked U in Chapter 2 are unverified.

**Table 4.17. Design-level comparison with the closest prior work**

| System | Documented design (Chapter 2; verification level) | Relation to REM |
|---|---|---|
| NEXUS (Hossain et al., 2026) | Structured-plan monitor; formal policy over allow, block, confirm and revise; rules, argument inspection and a calibrated logistic risk score (A). A rule-first cascade with loss-selected thresholds (R, authors' repository README); the cost values (U) | Shares calibrated logistic scoring and a four-way intervention set. REM evaluates each call during execution, in an executable banking environment. The difference in decision rule rests on the repository description (R), not on the paper's full text |
| AgentTrust (C. Yang, 2026) | Pre-execution interception; allow, warn, block and review; normalizer, chain detection and LLM judge (A) | Shares interception and a review verdict. REM uses a calibrated probability and declared losses |
| SafeAgent (H. Liu et al., 2026) | Runtime controller; decision core with operators for risk, utility-cost, consequence and arbitration (A); LLM realization (U) | REM's verdict is a closed-form rule |
| ProvenanceGuard (She et al., 2026) | Checks whether a proposed call is supported by traceable evidence in context; peer-reviewed (A) | REM's argument-provenance feature asks the same question; in REM's evaluation such action evidence carried most of the separation |
| H.-H. Chen (2026) | Prices the consequence of side-effecting actions against reserve capital (A) | REM combines consequence with an estimated probability |
| FinHarness (Jia et al., 2026) | Financial-agent monitors and an LLM-judge cascade; results on a benchmark whose preprint was withdrawn for non-scientific reasons (A) | Shares domain and placement; REM is evaluated on an open benchmark |
| C. Zhang et al. (2026) | Calibration need not improve control (A) | REM's evaluation observed no calibration effect on decisions |
| Kanaker et al. (2026) | Simulation framework with a threat model separating compromise, harm and severity; Monte Carlo comparison of architectural controls across six scenarios and nine defense configurations (A; supplementary update of 2 November 2026, Chapter 2, Section 2.13.7) | Shares the separation of compromise from severity and reports a similar set of outcomes. It compares design-time controls in a simulator; REM evaluates a per-call runtime decision on recorded traces. Neither study's results transfer to the other |

Records found in the currency update of 30 October 2026, examined at abstract level only, narrow the distance further (Chapter 2, Section 2.13.6): a controller that commits the proposed or an alternative action by a calibrated value learned from outcomes, with provenance-typed evidence (Yan et al., 2026); a three-way execute–confirm–block router with calibrated probabilities (Xin, 2026); and an offline evaluation of runtime monitors on AgentDojo's recorded traces (Kekatos et al., 2026).

A simulation study examined in a supplementary update of 2 November 2026 (Kanaker et al., 2026; Chapter 2, Section 2.13.7; abstract level) relates to REM at a different level of the problem. It compares architectural controls in an assumption-explicit simulator, whereas REM selects a verdict for each proposed call and is evaluated on recorded traces. Three of its reported findings bear on the interpretation of REM's results without changing them:

- its finding that human-in-the-loop approvals degrade under user error and habituation is consistent with treating REM's idealized-reviewer results as an upper bound and the no-reviewer bound as the conservative reference (Section 4.15.2);
- its finding that rate limiting reduces tail severity more than attack success illustrates why REM reports a loss-weighted measure beside the attack success rate, although REM's realized loss favours REM by construction (Section 4.9);
- its finding that least-privilege tool design is the strongest single broad control concerns a design-time restriction of privileges, which REM does not evaluate; REM's restricted-tool set 𝒯~R~ is used only by its mitigation semantics.

The two studies do not test each other's mechanisms. REM does not evaluate least privilege, retrieval allowlisting or rate limiting, and the simulation study does not, by its abstract, estimate a per-call probability or select among verdicts by expected loss. Its simulated results are not evidence about REM, and REM's results do not test its findings.

Each mechanism in REM has precedent. The distinguishing elements are the combination and the evaluation design; neither has been compared with these systems on a shared protocol.

## 4.17 Threats to Validity and Limitations

1. **Design status.** Costs, tiers, predicates, the feature set and the label rule are declared exploratory values, not approved ones.
2. **No live runs.** Enforcement was estimated only by replay under NO-ADAPT, a method proposed as an amendment to the Chapter 3 scope.
3. **One benchmark.** One benchmark, one attack family for fitting, one attacker identity, and historical model snapshots (2024–2025).
4. **Labels.** Labels are attempt-based and reference-matched. They are ambiguous for user_task_15 under early suite versions and miss alternative attacker routes. They have not been audited by a human.
5. **Statistics.** Nine attacked groups, one run per configuration, no correction for multiple comparisons. Several categories contain a single injection task.
6. **Reviewer.** Escalation outcomes are bounded by an oracle and by no reviewer.
7. **Missing component.** No neural injection classifier was available.
8. **Literature review.** The review was record-level; no full text was screened.
9. **Currency.** Work published after the review's search date was examined only at abstract level, and several close records were found (Chapter 2, Section 2.13.6).
10. **Runtime figures.** They describe the evaluated configuration only. A deployment with a neural classifier or a human reviewer would be slower.

## 4.18 Chapter Summary

This chapter reported an exploratory evaluation of REM on recorded traces of 21 LLM agents in the AgentDojo banking environment (3,334 episodes; 6,762 proposed tool calls), and discussed what it supports.

- **Estimation.** On held-out attacker objectives, the evidence available at the tool boundary separated attack attempts from legitimate calls (pooled ROC-AUC 0.938). Action evidence carried most of this separation; calibration produced no observed improvement; and the behavioral features were not specific to attacks in this benchmark (Sections 4.4 and 4.7).
- **Decisions.** With the declared exploratory costs, the expected-loss rule intervened on 97.3% of attack steps and 22.7% of legitimate steps, against 74.0% and 5.6% for the consequence-independent baseline on the same estimator (Section 4.5).
- **Replay.** Under the NO-ADAPT assumption, REM's attack success rate was 0.004 against 0.055 for the baseline (step-level semantics), while benign task success fell from 50.9% to 31.4% without a reviewer (no loss with an idealized reviewer) (Section 4.6). The mitigation semantics change the baseline's results (Table 4.11).
- **Live agents.** The closed-loop evaluation was not executed (Section 4.12); no live result exists, and replay results are not live results (Section 4.13).
- **Offline replay and planned MELON extension.** Relative to the internal baseline B1, Full REM reduced replay ASR from 5.5% to 0.4%, while benign task success fell from 50.9% to 31.4% (no adaptation, no reviewer; Table 4.15). The two MELON conditions are implemented but have not been executed with a live language model (Section 4.14).
- **Interpretation and validity.** The security gain observed in replay comes mainly from low intervention thresholds at high consequence tiers and is paid for in legitimate financial actions; the evidence does not establish protection of live or adaptive agents, deployability, or superiority over other defenses (Sections 4.15–4.17).

