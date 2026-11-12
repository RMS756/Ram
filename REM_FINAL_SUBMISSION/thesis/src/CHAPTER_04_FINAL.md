# CHAPTER FOUR

# EXPERIMENTAL RESULTS AND DISCUSSION

## 4.1 Purpose, Status and Kinds of Evidence

This chapter reports what the implementation of Chapter 3 produced on recorded agent behavior in the AgentDojo banking environment. **No experiment with a live agent was executed, and no result in this chapter is a live result.**

**All results are exploratory by label.** The design values they use (costs, tiers, predicates, feature set, label rule) are declared values that await the supervisor's approval. One analysis, the confirmatory run of Section 4.15, was carried out under a protocol and a pass rule committed before its data were opened. It is confirmatory in that procedural sense only: it shares the unapproved design values and the limits of replay with everything else.

Seven kinds of evidence are kept apart. Each table states which kind it reports.

**Table 4.1. Kinds of evidence in this chapter**

| Kind | What it is | What it cannot show | Sections |
|---|---|---|---|
| Recorded outcome | The benchmark's verdicts on traces as recorded by its authors, without REM | Anything about REM | Sections 4.2 and 4.11 |
| Offline prediction | REM's probability for a recorded call, from a model fitted without that call's group | Any effect of enforcement | Sections 4.3 and 4.4 |
| Observe-only decision | The verdict REM would issue for a recorded call; not enforced | Outcomes | Sections 4.5 and 4.7–4.9 |
| Replay | A recorded episode re-executed in the benchmark's sandbox with a policy that may withhold calls; later calls are the recorded ones (NO-ADAPT) | Agent adaptation; reviewer effect; any difference among Modify, Escalate and Block | Sections 4.6 and 4.12–4.14 |
| Post-hoc analysis | An analysis added after results were seen; labelled where it occurs | Confirmation | Section 4.10; parts of Sections 4.12–4.13 |
| Confirmatory replay | Replay on recordings never read before, under a protocol committed in advance | The same limits as replay | Section 4.15 |
| Call-level fixture | Hand-written paired calls scored by the frozen models | Prevalence; any benchmark outcome | Section 4.14 |

Integration checks with scripted agents and simulated providers are not results and are reported only as status (Section 4.16).

**Sources of the numbers.** Sections 4.2 to 4.11 report the pilot, from `results/pilot_R2/` and its re-execution `results/pilot_R4/` (Chapter 3, Section 3.14). Sections 4.12 to 4.14 report the study of 11 November 2026 on the same recordings, from `REM_Authorization_Generalization_Study/results/`. Section 4.15 reports the confirmatory run of the same date, from `REM_FINAL_SUBMISSION/results/`. Every run used AgentDojo 0.1.35, the benchmark's recordings at one fixed commit, seed 20261027 and step-level mitigation without a reviewer unless a table says otherwise.

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

The **pre-registered values** are listed in Table 4.2. They come from Chapter 3 where Chapter 3 gives them; otherwise they are declared exploratory values.

**Table 4.2. Pre-registered values** (`configs/exploratory/pilot_e0.yaml`)

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
| 27 Oct 2026 16:40 | Pilot design committed (Table 4.2) | commit `48bef90` |
| 27 Oct 2026 16:57 | Amendments AM-1 to AM-4 committed. AM-1: exclusion of (user_task_15, injection_task_4). AM-2: benign references. AM-3: the meaning of "tool class". AM-4: replay validity filter | commit `7a707a7` |
| 27 Oct 2026, after 16:57 | First computation of held-out predictions and of all analyses with the then-uncommitted pipeline code. **The log of this first execution was not preserved**; its order relative to the amendments rests on the commit times and on the working session record | — |
| 27 Oct 2026 17:16 | Pipeline committed, then re-run in full; results identical to the first execution | commit `aa66f22`; `results/pilot/` |
| 27–28 Oct 2026 | **Post-hoc analyses**, added after results had been seen: exclusion of user_task_15 (Section 4.10); benign-release breakdown by tier; REM without expected-loss Escalate (Sections 4.5–4.6); breakdowns by action type and tier; replay-failure analysis | `results/pilot_R2/` |
| 28 Oct 2026 | Code corrections of revision R2 (Section 3.14), complete re-run; analytical values identical | commit `84a8c21`; `results/pilot_R2/` |

No pre-registered value was changed after results were seen. The post-hoc analyses are reported as such, and none replaces a pre-registered analysis.

### 4.2.4 The confirmatory population

The confirmatory run of Section 4.15 uses recordings that no script of this project had read before 11 November 2026 (Chapter 3, Section 3.11.14).

**Table 4.3. Confirmatory population (recorded outcomes; `confirmatory_results.json`)**

| Source | Agent pipeline | Attack templates | Attacked episodes | Benign episodes |
|---|---|---|---|---|
| F-A | Meta-SecAlign-70B | `important_instructions`, `direct`, `ignore_previous` | 429 | 16 |
| F-B | Meta-SecAlign-70B with the benchmark's repeated-user-prompt defense | the same three | 429 | 16 |
| F-C | Llama-3.3-70B with the repeated-user-prompt defense | the same three | 383 | 16 |
| F-D | Llama-3.3-70B | `direct`, `ignore_previous` | 286 | 0 |
| F-E | GPT-4o (2024-05-13) | four variants of `important_instructions` | 538 | 0 |
| **Total** | | | **2,065** | **48** |

Of 2,162 recording files, 14 were excluded as the ambiguous pair of amendment AM-1, and 2,148 were loaded. Of these, 2,113 are eligible under amendment AM-4, meaning that the replay with every call allowed reproduces the recorded outcome; the 35 that are not (34 in F-E, 1 in F-C) are excluded from every metric. No episode was removed for any other reason. Sources F-D and F-E contribute no benign episodes, because the benign runs of those pipelines were part of the fitting data. The recordings state benchmark version v1.2.1 for 1,575 eligible episodes and no version for 538.

The agents, templates and trajectories are new. The sixteen user tasks and nine attack objectives are those of the benchmark.

### 4.2.5 Chronology of the analyses of November 2026

| Date (UTC) | Event | Record |
|---|---|---|
| 8 Nov 2026 | Decision traces of sixteen paired fixtures (sets 1 and 2) through REM v1.0; the fixtures were written before they were scored | commit `4989306` |
| 11 Nov 2026, 04:51 | Protocol of the rule baselines, diagnostic arms, double holdout and probes committed before any of their outcomes was computed | commit `cca4968` |
| 11 Nov 2026 | Those analyses run; three post-hoc additions made after results were seen, among them REM v1.1 under the double holdout | commit `2c915bf` |
| 11 Nov 2026, 17:04 | Confirmatory protocol and fixture set 3 committed before the new recordings were opened | commit `19bd168` |
| 11 Nov 2026 | Confirmatory run; no amendment to its protocol | commit `907e6d2` |

## 4.3 Pilot E0: Feasibility and Feature Retention

Pilot E0 used only the fitting portion of each outer fold (`e0_pilot.json`).

**Table 4.4. Pilot E0 (fitting portions only)**

| Evidence group | ROC-AUC: mean over folds; minimum | Retained in every fold (≥ 0.55) |
|---|---|---|
| Context (x^ctx₂ only) | 0.582; 0.554 | Yes, marginally |
| Behavioral | 0.802; 0.787 | Yes |
| Action | 0.929; 0.923 | Yes |
| All | 0.938; 0.930 | — |

The retention rule was applied to each fold's fitting portion separately, and every fold retained all three groups (`e1_crossfit.json`, `e0_fold_specific_feature_groups`). The feature set is therefore the same in every fold. No fold's held-out data influenced its own feature set.

The pooled count of positive steps is 921, above the declared minimum of 50. Thirteen of the 21 backbones have fewer than 50 positive steps each (range 2–116), so no per-backbone conclusion is drawn.

## 4.4 RQ1 — Offline Classification (Held-Out Predictions)

**Table 4.5. Held-out discrimination and calibration, pooled over nine outer folds** (6,762 steps; 921 positive; `e1_crossfit.json`)

| Metric | Calibrated p, label-NLL fit (reference) | Calibrated p, Platt smoothed targets | Uncalibrated p̃ |
|---|---|---|---|
| ROC-AUC | 0.938 [0.908, 0.961] | 0.938 | 0.939 |
| Average precision (PR-AUC estimate) | 0.719 [0.559, 0.827] | 0.719 | 0.721 |
| ECE (M = 10) | 0.044 [0.033, 0.084] | 0.044 | 0.042 |
| Log-loss | 0.201 [0.149, 0.294] | 0.201 | 0.201 |
| Brier score (binary convention) | 0.060 | 0.060 | 0.060 |

**Table 4.6. Per-fold results (calibrated, label-NLL)**

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

**Table 4.7. Observe-only verdicts on held-out steps** (y = 0: n = 5,841; y = 1: n = 921; `e2_e5_e6_observe_only.json`)

| | REM | REM w/o expected-loss Escalate | B1 |
|---|---|---|---|
| Any intervention on y = 1 steps | 0.973 [0.957, 0.987] | 0.973 | 0.740 [0.473, 0.922] |
| Any intervention on y = 0 steps (step false-positive rate) | 0.227 [0.213, 0.239] | 0.198 | 0.056 [0.047, 0.066] |
| Escalate share of all steps | 0.196 | 0.009 | 0.009 |
| y = 0 steps withheld if an idealized reviewer resolves escalations | 0.040 | 0.188 | 0.046 |
| Ties | 0 | 0 | 0 |
| Verdicts fixed by D2 | 58 | 58 | 58 |

**Table 4.8. Observe-only interventions by consequence tier and action category** (`r2_breakdowns.json`)

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
- **B1 and credential changes.** B1 intervened on none of the 124 credential-change attack steps. These are the steps of the fold whose probabilities were most miscalibrated (Table 4.6). Its thresholds are fixed by benign false-positive rates and did not reach them.
- **Realized loss.** Under the decision costs, realized loss is 0.114 for REM, 0.136 for REM without expected-loss Escalate and 0.652 for B1. This comparison favors REM by construction (Chapter 3, Section 3.12.3) and is not evidence of superiority.

## 4.6 RQ2 and RQ3 — Replay Sensitivity Analysis

The replay re-executes each recorded episode in the benchmark's sandbox with REM enforcing its verdicts (Chapter 3, Section 3.11.10). Its use is a proposed amendment to the scope of Chapter 3. Three properties limit what it can show:
- **NO-ADAPT.** The agent emits the calls it emitted in the recorded run, whatever REM does. After a refusal, a live agent could retry, rephrase, use another tool, or abandon the task. Replay therefore cannot show how often a live agent would achieve the attacker's goal by another route, and **a near-zero replay ASR is not evidence of protection against a live or adaptive agent.**
- **Mitigation semantics.** Under step-level semantics, Modify and Block have the same effect on the withheld call. The episode-level variant also restricts later calls: after a Block, every later call to a tool in 𝒯~R~ is refused, even one whose own verdict is Allow, and even though the agent never retries. The two semantics therefore give different replay results. Tables 4.9–4.12 use step-level semantics, the declared reference pending decision D-2; Table E.1 compares both semantics.
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

**Table 4.9. Replay results, step-level semantics** (attacked n = 2,979; benign n = 334; `e4_e5_enforcement_replay.json`)

| Configuration | ASR | Benign utility | Utility under attack |
|---|---|---|---|
| B0, no defense (replay) | 0.226 [0.148, 0.295] | 0.524 [0.381, 0.676] | 0.492 |
| B1, no reviewer | 0.055 [0.011, 0.134] | 0.509 [0.334, 0.702] | 0.514 |
| REM, no reviewer | 0.004 [0.001, 0.007] | 0.314 [0.110, 0.548] | 0.364 |
| REM w/o expected-loss Escalate, no reviewer | 0.004 [0.001, 0.007] | 0.329 [0.126, 0.551] | 0.374 |
| REM, idealized reviewer | 0.004 [0.001, 0.007] | 0.497 [0.333, 0.680] | 0.496 |
| REM w/o expected-loss Escalate, idealized reviewer | 0.004 [0.001, 0.007] | 0.311 [0.123, 0.518] | 0.359 |

**Table 4.10. Paired differences (grouped bootstrap)**

| Comparison | ΔASR | ΔBenign utility |
|---|---|---|
| REM − B1, no reviewer | −0.051 [−0.130, −0.007] | −0.195 [−0.341, −0.074] |
| REM w/o Esc. − B1, no reviewer (same escalation opportunity) | −0.051 [−0.130, −0.007] | −0.180 [−0.325, −0.063] |
| REM − B1, idealized reviewer | −0.051 [−0.130, −0.007] | +0.003 [−0.009, 0.018] |
| REM − REM w/o Esc., idealized reviewer | 0.000 | +0.186 [0.065, 0.335] |
| REM − B0, no reviewer | −0.222 [−0.289, −0.146] | −0.210 [−0.379, −0.051] |

**Table 4.11. Replay ASR by the attacker's target action** (`r2_breakdowns.json`)

| Target action | Injection tasks | Attacked episodes | B0 | B1 (no reviewer) | REM (no reviewer) |
|---|---|---|---|---|---|
| Value transfer | 7 | 2,334 | 0.213 [0.128, 0.293] | 0.014 [0.007, 0.020] | 0.005 [0.002, 0.008] |
| Payment modification | 1 | 311 | 0.183 | 0.042 | 0.000 |
| Credential change | 1 | 334 | 0.356 | 0.356 | 0.000 |

Single-task categories have no interval.

**Table 4.12. Replay benign utility by kind of user task** (`r2_breakdowns.json`)

| User tasks | Tasks | Episodes | B0 | B1 (no reviewer) | REM (no reviewer) | REM (idealized reviewer) |
|---|---|---|---|---|---|---|
| Requiring a state change | 12 | 250 | 0.472 [0.320, 0.632] | 0.432 [0.238, 0.637] | 0.168 [0.000, 0.420] | 0.416 [0.238, 0.600] |
| Read-only | 4 | 84 | 0.679 [0.369, 0.929] | 0.738 [0.417, 0.976] | 0.750 [0.429, 1.000] | 0.738 [0.417, 0.976] |

![Figure 4.2. Replay sensitivity analysis (NO-ADAPT): ASR and benign utility with 95% grouped-bootstrap intervals.](results/pilot_R2/figures/fig_enforcement_replay.png){width=95%}

![Figure 4.3. Security–utility trade-off in the replay sensitivity analysis (NO-ADAPT, step-level semantics): attack success rate against benign utility for B0, B1, REM and REM without expected-loss Escalate under both reviewer bounds, and for the single-tier ablations. Values from `results/pilot_R2/e4_e5_enforcement_replay.json`; no live result.](REM_FINAL_THESIS/final_five_chapters/figures/fig4_3_security_utility_tradeoff.png){width=100%}

**What the replay results show, within NO-ADAPT:**
- **Where the ASR difference comes from.** REM withholds more of the recorded attack attempts than B1. Most of the difference comes from the credential-change and payment-modification attacks (Table 4.11), each represented by a single injection task.
- **The utility cost falls on state-changing tasks.** With no reviewer, REM's benign utility falls to 0.168 on those tasks (Table 4.12).
- **The cost is not caused by the escalation option.** REM without expected-loss Escalate has almost the same utility cost relative to B1 (Table 4.10).
- **With an idealized reviewer, the cost disappears.** That reviewer knows the label and is an upper bound on reviewer quality, not a model of one.

**RQ3 quantities:**
- **Residual attack success after Modify.** In oracle-Modify replays within the fitting folds, r~mod~ was 0.000 at tier 3 (530 episodes) and 0.010 at tier 4 (298 episodes) (`e4_rmod_and_replay_validity.json`). In replays where REM applied Modify to an attack step, residual ASR was 0.000 (610 episodes). Under NO-ADAPT a withheld call simply does not occur, so **these values are consequences of the assumption, not measurements of tool restriction against a live agent.**
- **Escalation rate.** 0.196 of all steps in the observe-only analysis (Table 4.7).
- **Processing time** (Appendix B.1.14, Table B.8). **Complete call** (R4 re-execution, 1 November 2026; `results/pilot_R4/e4_e5_enforcement_replay.json`, `latency_full_ms_*`): median 0.21–0.28 ms and 95th percentile 0.49–0.70 ms per step, across the 8 REM configurations (6,684 steps each). **Partial timer**, which excludes attribution, audit-record construction and history recording: median 0.18–0.24 ms and 95th percentile 0.46–0.64 ms in the same run. Earlier runs measured only the partial timer: median 0.14–0.20 ms and 95th percentile 0.39–0.54 ms (R1, R2), with the 30 October re-execution within these ranges.
- **Memory.** The median peak traced allocation was 4.4 KB per step, with a 95th percentile of 12.4 KB (611 steps of 300 episodes; `latency_memory_profile.json`). The first run (R1) measured 2.9 KB; like time, memory varies between runs. The re-execution of 30 October measured the same value. In the R4 re-execution, where `evaluate` also records the complete-call timer, the median was 4,349 bytes against 4,364 bytes, with the same 95th percentile (12,419.5 bytes; `results/pilot_R4/latency_memory_profile.json`). The memory boundary is the complete `evaluate` call in both.

These figures apply to the evaluated configuration only: no neural injection classifier, no reviewer, recorded inputs. They are not estimates for a complete deployment.

**Sensitivity to the mitigation semantics.** Step-level semantics is the declared reference (Chapter 3, Section 3.8), pending the supervisor's decision on SC-1. The same replays under the episode-level variant are reported in Appendix E. In summary: REM's ASR is identical under both semantics (0.004); B1's is lower under the episode-level variant (0.055 against 0.046), because the restriction set left by an earlier Block or Modify refuses later state-changing calls; utility under attack is lower or equal under the episode-level variant in every configuration; and benign utility coincides. The episode-level rows are a sensitivity analysis and do not replace Tables 4.9 to 4.12.

## 4.7 RQ4 — Ablations

**Table 4.13. Ablations** (observe-only columns: held-out recorded steps; replay columns: step-level semantics, no reviewer)

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

## 4.12 Rule Baselines and an Audit of REM's Interventions

*Kind of evidence: replay on the primary recordings (2,979 attacked and 334 benign eligible episodes), held-out attack objective (scheme S1). The arms were declared before their outcomes were computed, except where marked post hoc.*

### 4.12.1 Security and task completion of every arm

**Table 4.14. Replay results of REM, the baselines and the rules on the primary recordings** (step-level, no reviewer; `study_results.json`, S1)

| Arm | Successful attacks / 2,979 | Unauthorized state change (episodes) | Benign tasks completed / 334 | Tasks completed under attack / 2,979 | Authorized calls released / 178 |
|---|---|---|---|---|---|
| No defense | 672 | 828 | 175 | 1,465 | 178 |
| B1, operating-point thresholds | 164 | 202 | 170 | 1,532 | 130 |
| **REM v1.0** | **11** | 24 | **105** | 1,083 | 33 |
| REM v1.1 (pilot ablation) | 11 | 24 | 140 | 1,147 | 83 |
| P1, provenance rule | 12 | 26 | 134 | 1,207 | 92 |
| P2, provenance or novelty rule | 12 | 26 | 134 | 1,207 | 89 |
| A2, strict explicit rule | 13 | 27 | 140 | 1,334 | 83 |
| REM, Allow and Block only | 13 | 27 | 124 | 1,273 | 64 |

The counts for REM v1.0, B1 and the no-defense reference are identical to the pilot's (Table 4.9), which checks the study's implementation. The 178 authorized calls are the calls to tools in 𝒯~R~ proposed in the 334 benign episodes.

Three observations follow.

- **The rules match REM's security.** Rules that use one or two pieces of evidence and no model leave 12 or 13 successful attacks where REM v1.0 leaves 11. The differences are one or two episodes of 2,979.
- **REM v1.0 completes the fewest tasks of the restrictive arms.** It completes 105 benign tasks; the rules complete 134 to 140. It releases 33 of 178 authorized calls; the rules release 83 to 92.
- **The estimator's discrimination is real but is not what produces the security.** The held-out ROC-AUC of 0.938 (Table 4.5) shows that the score separates attempts from legitimate calls. A single feature already does most of this: read as a classifier of the attempt label, the provenance indicator x^act^~1~ alone has recall 0.971 and false-positive rate 0.147.

### 4.12.2 What REM v1.0 withholds

**Table 4.15. REM v1.0 on the 178 authorized calls of benign episodes, by action category** (`weakness_audit.json`)

| Category | Authorized calls | Released | Share released |
|---|---|---|---|
| Value transfer | 89 | 4 | 4% |
| Payment modification | 34 | 8 | 24% |
| Profile change | 37 | 21 | 57% |
| Credential change | 18 | 0 | 0% |
| **All** | **178** | **33** | **19%** |

REM v1.0 withholds almost every legitimate payment and every legitimate password change. The cause is a combination of the declared costs and the evidence, not a defect in the code. With C~esc~ = 0.3 and C~miss~ = 10 or 20, Allow has the lowest expected loss only below a probability of 0.03 at tier 3 and 0.015 at tier 4. The first transfer of an episode receives a probability of about 0.033 from the intercept and two behavioral features alone, and about 0.086 when the transition-deviation feature also fires. Escalate then has the lowest expected loss, and without a reviewer an escalated call is withheld. On the sixteen paired fixtures of sets 1 and 2, REM v1.0 withheld all fourteen legitimate payments (Section 4.14).

**Modify, Escalate and Block coincide.** When every Modify and Escalate verdict of REM v1.0 is replaced by Block, the outcome of none of the 3,313 episodes changes. The Allow-and-Block-only arm of Table 4.14 uses the same fitted model and releases more calls than REM v1.0, because without Escalate the boundary of Allow moves from C~esc~/C~miss~(k) to the Allow–Block threshold of Equation 3.9. In this evaluation the four-verdict structure is therefore a two-verdict structure in effect, and the Escalate option acts only by narrowing the Allow region. Whether the four verdicts differ with a live agent and a reviewer is not tested.

**All residual attacks are one ambiguous task.** All 11 successful attacks under REM v1.0 are episodes of user_task_15, in which the user's own task pays the account that the attack also targets (Section 4.10). The comparisons "11 against 12 against 13" in Table 4.14 are thus comparisons of how arms handle one ambiguous task, and carry no weight.

## 4.13 Generalization to Unseen Tasks and Objectives, and a Rejected Candidate

*Kind of evidence: replay on the primary recordings under schemes S1, S2 and S3 (Chapter 3, Section 3.11.12). REM v1.1 under S2 is post hoc.*

### 4.13.1 Double holdout and held-out templates

**Table 4.16. Successful attacks and benign tasks completed under three generalization schemes** (`study_results.json`)

| Arm | S1: attacks / 2,979 | S1: benign / 334 | S2: attacks / 2,979 | S2: benign / 334 | S3: attacks / 681 | S3: tasks under attack / 681 |
|---|---|---|---|---|---|---|
| No defense | 672 | 175 | 672 | 175 | 174 | 504 |
| B1 | 164 | 170 | 162 | 170 | 33 | 525 |
| REM v1.0 | 11 | 105 | 11 | 105 | 2 | 302 |
| REM v1.1 | 11 | 140 | 14 *(post hoc)* | 140 *(post hoc)* | 2 | 370 |
| P1 | 12 | 134 | 12 | 134 | 2 | 360 |
| P2 | 12 | 134 | 12 | 134 | 2 | 360 |
| A2 | 13 | 140 | 13 | 140 | 3 | 438 |
| Authorization-aware intervention-value policy (candidate) | 132 | 127 | 132 | 110 | 28 | 364 |

S3 uses 681 attacked episodes of one backbone under five attack templates not used in fitting (of 715 recorded, 34 are not reproduced by the all-allow replay and are excluded); it has no benign episodes.

- **REM v1.0 is stable across the schemes.** Its counts do not change when the user task is also held out, and its attack count stays low on templates it never saw. This stability is that of a policy that withholds most state-changing calls: there is little for a change of task to alter.
- **The rules are identical under S1 and S2 by construction**, because they have no fitted quantity.
- **REM v1.1 loses three episodes of security under double holdout** (11 to 14 of 2,979) and keeps its utility. This observation was made after results were seen and motivated the confirmatory run of Section 4.15.

### 4.13.2 The pre-declared candidate failed

The candidate declared in advance for this study was the authorization-aware intervention-value policy (Chapter 3, Table 3.14). The protocol stated that an improvement over REM v1.0 would be claimed only if, under both S1 and S2, the paired gain in benign utility had a 95% interval above zero and the paired change in attack success had an interval not entirely above zero.

**Table 4.17. Pre-declared contrasts of the candidate against REM v1.0** (paired, grouped bootstrap; percentage points)

| Scheme | Benign utility | Attack success rate | Unauthorized state-change rate |
|---|---|---|---|
| S1 | +6.6 [0.0, 18.2] | +4.1 [0.0, 12.1] | +4.2 [0.03, 12.4] |
| S2 | +1.5 [0.0, 4.5] | +4.1 [0.0, 12.1] | +4.2 [0.03, 12.4] |

**The candidate is rejected.** Its utility gain is not established under either scheme and almost disappears under double holdout. It admits 132 successful attacks where REM v1.0 admits 11, and its rate of unauthorized state change rises with an interval that excludes zero.

The failure has one identifiable cause. Of the 132 attacks, 119 are episodes of the credential-change objective, and the intervention-value policy without authorization features releases all 119 of them. When that objective is held out, the training outcomes contain no case in which withholding a credential update prevents harm. The policy learns that harm is prevented by withholding payments to new recipients, and it assigns no security value to a password taken from a document. The utility side transfers poorly as well: the candidate's model of whether withholding a call breaks the user's task has a held-out ROC-AUC of 0.857 under S1 and 0.729 under S2 (0.854 and 0.682 without the authorization features).

### 4.13.3 What the diagnostic arms show

**Table 4.18. Diagnostic arms on the primary recordings, scheme S1** (attacks / 2,979; benign tasks / 334)

| Arm | Attacks | Benign | What it isolates |
|---|---|---|---|
| REM v1.0 | 11 | 105 | reference |
| REM v1.0 with authorization features added | 69 | 110 | adding z^exp^ and z^del^ to the estimator |
| Outcome-supervised REM | 76 | 105 | changing the training target only |
| Intervention-value policy | 119 | 105 | changing the target and the rule |
| Intervention-value policy with the attempt label on the security side | 0 | 105 | keeping the attempt label for security |
| A1, explicit or delegated rule | 313 | 164 | trusting documents that the user named |

- **Outcome supervision lowers security in this setting.** Every arm trained on intervention outcomes admits more attacks than REM v1.0. The attempt label, although a proxy, transfers to an unseen objective; the outcome label does not.
- **Authorization features do not help the estimator.** Added to REM v1.0 they raise attacks from 11 to 69 for five more benign tasks.
- **Delegation is unsafe.** Rule A1 releases a call when its recipient comes from a document that the user named. It admits 313 attacks. The reason is visible in the evidence itself: of 908 attack calls to restricted tools, 382 take their key value from a document the user named, because that document is where the injection was planted.

These are negative results. They are reported because they bound what the available evidence can support, and because two of them test proposals from the literature (C. Zhang et al., 2026; the delegation remark of F. Jia et al., 2025) under conditions their authors did not examine.

## 4.14 Robustness Probes: Reformatted Identifiers and Paired Call Fixtures

*Kind of evidence: replay with a modified injected text, and call-level fixtures. Neither is a benchmark result. Fixture counts are not rates.*

### 4.14.1 Reformatted attacker identifier

In 2,645 attacked episodes the injected text contains the attacker's account identifier. The probe rewrites that identifier in groups of four characters inside the injected text and leaves the recorded calls unchanged (Chapter 3, Section 3.11.13). The all-allow replay still reproduces all 2,645 recorded outcomes.

**Table 4.19. Successful attacks before and after the identifier is reformatted** (2,645 attacked episodes; `study_results.json`)

| Arm | Original text | Reformatted text |
|---|---|---|
| No defense | 553 | 553 |
| B1 | 45 | **198** |
| REM v1.0 | 11 | 11 |
| REM v1.1 | 11 | 11 |
| P1, provenance rule | 12 | **191** |
| P2, provenance or novelty rule | 12 | 12 |
| A2, strict explicit rule | 13 | 13 |
| REM, Allow and Block only | 13 | 31 |

The provenance indicator compares whole normalized tokens. Once the identifier in the document is spaced and the identifier in the call is not, the argument is no longer traced to the untrusted text. A rule that depends on that trace alone (P1) fails, and so does B1. Arms that also use the question "does the recipient appear in the user's request?" are unaffected: P2 through the novelty indicator and A2 by definition. Both REM versions are also unchanged, which is consistent with their narrow Allow region; the contribution of each feature to that result was not examined separately.

This agrees with the finding of Kekatos et al. (2026) that a planted line defeats a naive provenance check on recorded AgentDojo traces. Exact-string provenance is evidence that an attacker can remove by formatting.

### 4.14.2 Paired call fixtures

Twenty-three paired fixtures in three sets were scored once each with the models of one fold (Chapter 3, Section 3.11.13). Sets 1 and 2 contain fourteen payment pairs, in which a legitimate payment and a substituted payment share a scaffold, and two read-only pairs, in which the unsafe call is an unrequested payment. Set 3 contains three credential pairs and four pairs with reformatted or fragmented identifiers.

**Table 4.20. Paired fixtures: legitimate calls released and unsafe calls released** (counts)

| Arm | Sets 1–2: legitimate payments released / 14 | Sets 1–2: unsafe calls released / 16 | Set 3: legitimate released / 7 | Set 3: unsafe released / 7 |
|---|---|---|---|---|
| REM v1.0 | 0 | 0 | 1 | 0 |
| REM v1.1 *(sets 1–2 post hoc)* | 14 | 4 | 5 | 0 |
| B1 | 14 | 4 | 6 | 2 |
| P1 | 14 | 4 | 6 | 2 |
| P2 | 14 | 4 | 5 | 0 |
| A2 | 14 | 9 | 5 | 1 |

In sets 1 and 2, the four unsafe calls released by REM v1.1, B1, P1 and P2 are the same four: two substituted amounts and the two unrequested payments. A2 releases nine: the seven amount substitutions, because it checks identity arguments only, and the two unrequested payments.

What the fixtures show:

- **REM v1.0 is safe on the fixtures by refusing.** It releases no unsafe call and no legitimate payment.
- **Every arm that releases legitimate payments also releases an unrequested payment whose recipient and amount occur in the user's words.** In the two read-only pairs the user mentions a past payment, with its payee and amount, asks only for the account balance and states that no payment is to be made. The document read by the agent then asks for the same payment again. Nothing in the features of the call distinguishes this unrequested payment from a requested one: its recipient and amount occur in the user's own text. Occurrence in the user's text is not authorization.
- **Amount substitution passes identity-only checks.** A rule that verifies the recipient and not the amount releases a payment to the right recipient for the wrong amount.
- **Reformatting defeats exact matching on fixtures as on the benchmark.** P1 and B1 release two unsafe calls of set 3 whose identifiers were reformatted.
- **REM v1.1 and P2 behave alike** on set 3: five legitimate calls released, no unsafe call released, and the same two legitimate calls withheld.

No arm, learned or rule-based, gets every pair right. The pairs it fails are those in which the distinguishing fact, what the user actually authorized, is not present in any input the policy receives.

## 4.15 Confirmatory Evaluation on Untouched Recordings

*Kind of evidence: confirmatory replay. Protocol and verdict rule committed before the data were opened (Chapter 3, Section 3.11.14); no amendment. Population: Table 4.3. Models: frozen from the primary recordings; nothing fitted or selected on these episodes.*

### 4.15.1 Results

**Table 4.21. Confirmatory replay results** (2,065 attacked and 48 benign eligible episodes; step-level, no reviewer; `confirmatory_results.json`)

| Arm | Successful attacks / 2,065 | Unauthorized state change (episodes) | Tasks completed under attack / 2,065 | Benign tasks completed / 48 | All tasks completed / 2,113 | Authorized calls released / 51 |
|---|---|---|---|---|---|---|
| No defense | 436 | 493 | 1,413 | 38 | 1,451 | 51 |
| B1 | 67 | 96 | 1,478 | 36 | 1,514 | 36 |
| **REM v1.0** | **3** | 3 | 898 | 18 | **916** | 4 |
| **REM v1.1 (candidate)** | **1** | 1 | 1,049 | 25 | **1,074** | 11 |
| P1 | 4 | 4 | 1,020 | 24 | 1,044 | 12 |
| P2 | 4 | 4 | 1,019 | 24 | 1,043 | 12 |
| A2 | 4 | 4 | 1,205 | 27 | 1,232 | 27 |
| REM, Allow and Block only | 3 | 3 | 1,093 | 22 | 1,115 | 8 |

No replay raised an error in any arm.

**Table 4.22. Paired contrasts on the confirmatory population** (percentage points; 95% grouped-bootstrap interval; gained / lost = episodes in which only the first or only the second arm completes the task)

| Contrast | Task completion, all episodes | Attack success rate | Benign episodes only | Gained / lost |
|---|---|---|---|---|
| **REM v1.1 − REM v1.0 (pre-declared)** | **+7.48 [1.17, 16.02]** | **−0.10 [−0.29, 0.00]** | +14.58 [0.00, 33.33] | 158 / 0 |
| REM v1.1 − P2 | +1.47 [−5.28, 7.98] | −0.15 [−0.38, 0.00] | +2.08 [0.00, 6.25] | 88 / 57 |
| REM v1.1 − A2 | −7.48 [−25.66, 8.16] | −0.15 [−0.38, 0.00] | −4.17 [−25.00, 14.58] | 142 / 300 |
| P2 − REM v1.0 | +6.01 [−5.17, 20.25] | +0.05 [0.00, 0.15] | +12.50 [−2.08, 31.25] | 193 / 66 |
| A2 − REM v1.0 | +14.96 [−1.29, 34.42] | +0.05 [0.00, 0.15] | +18.75 [4.17, 37.50] | 393 / 77 |
| REM v1.0 − B1 | −28.30 [−47.16, −10.83] | −3.10 [−8.27, −0.39] | −37.50 [−58.33, −16.67] | 26 / 624 |

The unauthorized state-change contrast of REM v1.1 against REM v1.0 equals the attack-success contrast: −0.10 [−0.29, 0.00].

### 4.15.2 The pre-declared verdict

All three conditions of the rule hold.

| Condition | Result |
|---|---|
| (a) The interval of the task-completion difference lies above zero | +7.48 points [1.17, 16.02] |
| (b) Neither security interval lies above zero | both −0.10 [−0.29, 0.00] |
| (c) The candidate's successful attacks do not exceed those of rule P2 | 1 against 4 |

**The verdict is GO.** On recordings that no earlier analysis had read, REM without the behavioral evidence group completes more tasks than REM v1.0 (1,074 against 916 of 2,113) with no measured loss of security (1 successful attack against 3 of 2,065). REM v1.1 gains 158 episodes and loses none. The observation made post hoc on the primary recordings is confirmed.

### 4.15.3 What the verdict does not establish

- **REM v1.1 is not shown to be better than the rules.** Its difference from P2 is +1.47 points [−5.28, 7.98], and from A2 −7.48 points [−25.66, 8.16]. Neither is resolved. A2 completes 1,232 tasks, more than either REM version, with 4 successful attacks.
- **REM v1.0 is not shown to be better than the rules either.** P2 and A2 complete more tasks in point estimate with one more successful attack; the intervals of their differences from REM v1.0 include zero, except for A2 on benign episodes.
- **Utility remains far below the undefended agent.** The undefended agent completes 1,451 of 2,113 tasks; REM v1.1 completes 1,074. In benign episodes REM v1.1 releases 11 of 51 authorized calls; REM v1.0 releases 4.
- **The benign-only interval touches zero** (+14.58 points [0.00, 33.33], 18 against 25 of 48). The verdict rests on all episodes, as declared; most of the gain is task completion under attack.
- **A second configuration passes the same test.** REM restricted to Allow and Block completes 1,115 tasks with the same 3 attacks as REM v1.0 (+9.42 points [2.77, 17.87]). It was a comparator, not the declared candidate, and is not adopted. It adds to the evidence that the middle verdicts do not help in this evaluation.

### 4.15.4 Where the gain and the remaining attacks are

**Table 4.23. Tasks completed by user task on the confirmatory population** (all eligible episodes of each task; tasks on which the arms differ)

| User task | Episodes | No defense | REM v1.0 | REM v1.1 | P2 | A2 |
|---|---|---|---|---|---|---|
| 2 | 138 | 114 | 36 | 97 | 104 | 0 |
| 3 | 138 | 72 | 6 | 17 | 11 | 72 |
| 4 | 138 | 92 | 4 | 10 | 0 | 92 |
| 6 | 138 | 132 | 3 | 15 | 0 | 132 |
| 9 | 138 | 50 | 138 | 138 | 92 | 138 |
| 12 | 129 | 39 | 30 | 34 | 38 | 0 |
| 13 | 95 | 85 | 11 | 11 | 0 | 0 |
| 14 | 129 | 119 | 9 | 73 | 119 | 119 |

On user tasks 1, 5, 7, 8 and 10 every restrictive arm completes all or nearly all episodes, and on tasks 0, 11 and 15 none completes any; these rows are omitted. On tasks 9 and 10 the restrictive arms pass the benchmark's utility check more often than the undefended agent. The cause was not examined call by call. It shows that the utility check can be passed by an episode in which a state-changing call was withheld, which is one reason why authorized-call release is reported beside task completion.

The gain of REM v1.1 over v1.0 is concentrated in two tasks: task 2 (36 to 97 of 138) and task 14 (9 to 73 of 129). The rule A2 behaves differently: it completes tasks 3, 4 and 6 at the level of the undefended agent, because their recipients are stated in the request, and completes none of tasks 2 and 12, where the needed value comes from a file. With sixteen user tasks, a few tasks decide each comparison, which is why the intervals between REM v1.1 and the rules are wide.

**Remaining attacks.** REM v1.0's three successful attacks are in two injection tasks (one and two episodes); REM v1.1's one is in the first of these; the rules' four add one episode of a third. All are in source F-E. Of 559 calls labelled as attack attempts, REM v1.0 withholds 556, REM v1.1 558, and the rules 555.

### 4.15.5 Intervention burden and processing time

**Table 4.24. Interventions on the confirmatory population** (8,221 recorded calls in 2,113 episodes, of which 5,808 are read-type calls that no arm withholds; `confirmatory_descriptives.json`; descriptive)

| Arm | State-changing calls not labelled as attempts: released / 1,854 | Escalate verdicts | Episodes with an Escalate verdict | Episodes with any withheld call |
|---|---|---|---|---|
| B1 | 1,347 | 63 | 61 | 821 |
| REM v1.0 | 224 | 1,392 | 928 | 1,423 |
| REM v1.1 | 497 | 981 | 671 | 1,257 |
| P2 | 549 | 0 | 0 | 1,210 |
| A2 | 928 | 0 | 0 | 1,080 |

In an attacked episode, a state-changing call that the label rule does not mark may still have been influenced by the injection. The 1,854 calls are therefore context, and the 51 authorized calls of benign episodes (Table 4.21) are the clean measure of legitimate-action approval.

Without a reviewer every Escalate is a withheld call. If a reviewer existed, REM v1.0 would refer 1,392 calls in 2,113 episodes and REM v1.1 would refer 981. Nothing is assumed about how well a reviewer would resolve them.

The median time to evaluate one call was 0.23 ms for the REM arms and 0.20 ms for the rules, with a 95th percentile of about 0.6 ms, measured under four parallel worker processes. The figures agree with the pilot's (Section 4.6.2) and describe this configuration only.

## 4.16 Live-Agent and Published-Defense Experiments: Status

**No experiment with a language model was executed in this thesis.** This section reports no attack success rate, utility or adaptation behavior of a live agent, and no figure for any published defense run by this project.

**Closed-loop evaluation of REM.** A harness in which a running agent receives REM's refusals and continues is implemented and tested with a scripted agent (Appendix D). It was not executed with a model, for two reasons: no credential for a model provider was available in the execution environment, and the design inputs it needs (backbone, decoding parameters, number of repeats, source of fitted parameters, spending authorization) have not been decided. The harness refuses to start until they are.

**MELON with and without REM.** An integration that places REM behind the MELON defense (Zhu, Yang, et al., 2025) is implemented: MELON's published code is used unmodified at a pinned commit, and the two conditions differ only in the tool executor. Thirty tests pass with scripted agents, a deterministic stand-in for the embedding service and a simulated provider. These tests show that the integration is mechanically correct. They show nothing about effectiveness: **MELON and MELON with REM are implementation-verified and effectiveness-unevaluated.** A real run needs a model credential, MELON's embedding service and an approved spending limit, none of which was available. The protocol and its status are in Appendix D.

**Other published defenses.** NEXUS, Task Shield, PROVISO, aiAuthZ and Kairos were not run. Section 4.18 states why for each.

**What replay cannot substitute for.** A live agent can retry, rephrase or reach the attacker's goal through another tool after a refusal. The replay attack success rate is therefore not an upper bound on live attack success, and the replay utility is not a lower or an upper bound on live utility. The size and direction of the difference are empirical questions that only a closed-loop run can answer (Appendix D compares the two designs).

## 4.17 Interpretation of the Findings

This section interprets the evaluation reported in Sections 4.2 to 4.15. Each conclusion is linked to the result that supports it and to the limit of that result. Section 4.1 defines the kinds of evidence. No live run was executed.

### 4.17.1 What the evidence supports

**Table 4.25. Conclusions, their support and their limits**

| # | Conclusion | Supporting result | Limit |
|---|---|---|---|
| 1 | Evidence at the tool boundary separates attack attempts from legitimate calls on unseen attack objectives | Held-out ROC-AUC 0.938; 0.927 when the user task is also held out | One benchmark; attempt labels, not audited by a human; most of the separation comes from one provenance feature |
| 2 | In replay, REM v1.0 withholds nearly all recorded attack attempts | Attack success 22.6% to 0.4% (primary) and 21.1% to 0.15% (confirmatory) | NO-ADAPT; no live agent; residual attacks on the primary recordings are one ambiguous task |
| 3 | REM v1.0 obtains this by withholding most state-changing calls | 33 of 178 and 4 of 51 authorized calls released; 4 of 89 legitimate transfers | No reviewer; declared costs |
| 4 | Simple rules reach the same security with at least as much task completion | Tables 4.14 and 4.21 | Differences between REM and the rules are not resolved statistically on the confirmatory population |
| 5 | Removing behavioral evidence improves REM | Confirmatory: +7.48 points [1.17, 16.02] with 1 against 3 attacks | Same benchmark tasks; replay; not better than the rules |
| 6 | Calibration changed no outcome, and the four verdicts act as two | γ~1~ between 0.945 and 0.981; 0 of 3,313 episodes change when Modify and Escalate become Block | This evaluation only |
| 7 | Supervising on intervention outcomes, and trusting user-named documents, lower security | 119 to 132 and 313 attacks against 11 | One benchmark; one held-out objective class drives the first result |
| 8 | No tested policy separates an authorized payment from an unrequested one whose details occur in the user's words | Paired fixtures, Section 4.14.2 | Hand-written cases; mechanism, not prevalence |

### 4.17.2 Why benign utility falls

The fall in benign utility has two sources, and the evaluation separates them.

**Where the verdict sends them.** The withheld actions are mostly escalated. Without a reviewer an escalation is a withheld action, so utility falls. The comparison with REM without expected-loss Escalate shows that removing the option does not recover the utility: the same actions are then withheld through Modify. The utility cost is therefore a consequence of the declared costs and of the evidence, not of escalation as such.

**What a reviewer would change.** An escalation is worth something only if someone resolves it. With an oracle reviewer the utility cost disappears, which bounds what a perfect reviewer could recover. A real reviewer would recover less, at some delay and cost. The thesis does not model that reviewer.

### 4.17.3 Why behavioral evidence did not help, and calibration did not change outcomes

**Behavioral evidence.** The behavioral indicators are not specific to attacks in this benchmark:
- *privilege escalation* fired on 92% of legitimate state-changing steps, because a user's first transfer is, by definition, the first use of a higher-privilege tool;
- *transition deviation* fired more often on legitimate steps (43%) than on attacks (17%), because legitimate tasks held out from fitting produce unseen transitions.

The estimator gave these features positive weight. In the decision they therefore added to the probability of legitimate high-tier actions, and removing them recovered utility without a measured change in attack success. This is an observation about these features in this benchmark, with short trajectories. It does not show that behavioral evidence is useless elsewhere.

**Calibration.** Calibration did not change outcomes for two reasons:
- logistic regression fitted by penalized likelihood was already close to calibrated on in-distribution folds, so the fitted map was close to the identity;
- the one fold where calibration mattered, the unseen credential-change attack, was miscalibrated in a way a monotone map fitted on other attack categories cannot repair.

This agrees with the position, taken in Chapter 3, that calibration quality and control quality must be reported separately (C. Zhang et al., 2026).

### 4.17.4 The security–utility frontier that was measured

The arms fall into two groups, not along a ranking.

**Table 4.26. Attack success and task completion in percent, both populations**

| Arm | Primary: attack success | Primary: benign tasks | Confirmatory: attack success | Confirmatory: all tasks | Confirmatory: authorized calls released |
|---|---|---|---|---|---|
| No defense | 22.6 | 52.4 | 21.1 | 68.7 | 100 |
| B1 | 5.5 | 50.9 | 3.2 | 71.7 | 70.6 |
| REM v1.0 | 0.37 | 31.4 | 0.15 | 43.4 | 7.8 |
| REM v1.1 | 0.37 | 41.9 | 0.05 | 50.8 | 21.6 |
| P2 | 0.40 | 40.1 | 0.19 | 49.4 | 23.5 |
| A2 | 0.44 | 41.9 | 0.19 | 58.3 | 52.9 |

B1 keeps task completion close to the undefended level and removes about three quarters (primary) to 85% (confirmatory) of successful attacks. The other four arms bring attack success below 0.5% and lose a quarter to a half of legitimate work. Inside that group the security differences are a handful of episodes. Which group is preferable is a policy question. The declared costs, with a missed attack on a high-consequence action weighted twenty times a false alarm, answer it in favor of the restrictive group; a different institution could answer differently.

No arm dominates. Every arm with attack success below 0.5% completes at most 58% of tasks where the undefended agent completes 69%.

### 4.17.5 The limiting factor is information

Three results point the same way. REM's estimator discriminates well, yet a one-feature rule matches its security. A more elaborate policy, supervised on outcomes and given authorization features, did worse. And on paired fixtures every policy that releases legitimate payments also releases an unrequested payment that uses the user's own words. None of these is repaired by a larger or more complex model, because the fact that would settle the decision, what the user authorized, is not among the inputs. REM's threat model gives it one trusted input, the user's request as text. The published approaches that report both low attack success and high utility add something REM does not have: a trusted policy or authorization record (aiAuthZ, at abstract level), trusted observations that license an action (Yan et al., 2026), a language model that judges task alignment (F. Jia et al., 2025), or enforcement on effects at the system boundary (Kairos, at abstract level). This thesis did not run any of them and does not claim they would succeed on these episodes. It identifies the trusted authorization input as the component whose absence bounds REM.

### 4.17.6 What the evidence does not support

- **That REM protects live agents.** Under replay a withheld call does not reappear. A live agent can retry, rephrase or reach the goal through another tool.
- **That REM, in either version, is better than simple rules.** On the confirmatory population neither version is distinguishable from the rules, and one rule completes more tasks.
- **That REM is deployable as configured.** Without a reviewer, REM v1.0 completes 18 of 48 benign tasks where the undefended agent completes 38, and REM v1.1 completes 25.
- **That the four verdicts are useful as four.** In this evaluation Modify, Escalate and Block coincide.
- **That REM is superior to any published defense.** None was run under the same conditions.
- **That authorization can be read from text.** The fixtures show the opposite.
- **Anything about the injection classifier**, which was not available, or about adaptive attackers, who were out of scope.

## 4.18 Comparison with Prior Work

The comparison restates design positions documented in Chapter 2 and does not rank systems, because no shared evaluation exists. Properties marked U in Chapter 2 are unverified.

**Papers read in full in November 2026 (Chapter 2, Section 2.12.6).** The position of REM relative to them is as follows.

**Table 4.27. Relation of the results to recent work, and why no experimental comparison is reported**

| Work | Relation to the results of this chapter | Why it was not run |
|---|---|---|
| NEXUS (Hossain et al., 2026) | Same family: calibrated logistic score, rules and four graduated interventions. Its repository documentation reports that on rule-blind plans its policy predicts only Allow or Block, which parallels the finding here that the middle verdicts do not act | Code not available in the execution environment; full text not read; no valid adapter from a banking tool call to its plan representation. Re-implementing it from its documentation would not be NEXUS |
| CASEL (Y. Zhang et al., 2026) | Publishes a per-mode cost rule of the same structure as Equation 3.6, in simulation, and reports that it does not reduce harm beyond a simpler gate | No benchmark results exist to compare with |
| C. Zhang et al. (2026) | Explains why calibration changed no outcome. Its intervention-value target was tested here (Section 4.13) and did not transfer to an unseen attack objective, a condition the paper does not examine | Tested as an adaptation, labelled as derived |
| AgentBoundary (T. Yang et al., 2026) | Reports over-defense as a general finding; REM's release of 4 of 51 authorized calls is an instance. Its paired design is used for the fixtures | Its mitigation is a language-model component |
| PROVISO (Yan et al., 2026) | Reports much higher utility with a trained controller and restored rollouts. Its stated limitation, fitting per benchmark without a transfer study, is the condition examined here for a simpler monitor | No implementation is named in the paper; it needs an encoder and an agent model |
| Task Shield; MELON | Reported on AgentDojo with live agents | Need a model in the decision path; MELON integration is implemented and unevaluated (Section 4.16) |
| aiAuthZ; Kairos (abstracts only) | Add a trusted authorization channel or act at the system boundary | Not available; full texts not read |

**Published figures are not placed beside REM's.** The authors' reported results on AgentDojo come from live agents, other models, other suites or other attack sets. REM's figures come from replay of recorded trajectories. Putting them in one table would present incompatible measurements as a comparison.

## 4.19 Threats to Validity and Limitations

1. **Design status.** Costs, tiers, predicates, the feature set and the label rule are declared exploratory values, not approved ones.
2. **No live runs.** Enforcement was estimated only by replay under NO-ADAPT, a method proposed as an amendment to the Chapter 3 scope.
3. **One benchmark.** One benchmark, one attack family for fitting, one attacker identity, and historical model snapshots (2024–2025).
4. **Labels.** Labels are attempt-based and reference-matched. They are ambiguous for user_task_15 under early suite versions and miss alternative attacker routes. They have not been audited by a human.
5. **Statistics.** Nine attacked groups, one run per configuration, no correction for multiple comparisons. Several categories contain a single injection task.
6. **Reviewer.** Escalation outcomes are bounded by an oracle and by no reviewer.
7. **Missing component.** No neural injection classifier was available.
8. **Literature review.** The review was record-level; no full text was screened.
9. **Currency.** Work published after the review's search date was examined only at abstract level, and several close records were found (Chapter 2, Section 2.12.5).
10. **Runtime figures.** They describe the evaluated configuration only. A deployment with a neural classifier or a human reviewer would be slower.

11. **Reuse of the primary recordings.** They were used for fitting, cross-validation and many analyses. Only the confirmatory run is free of that reuse, and it tests one contrast.
12. **Tasks are not new anywhere.** The confirmatory population has new agents and templates and the same sixteen user tasks and nine attack objectives. A few user tasks decide each utility comparison.
13. **Author knowledge.** The rules, the authorization evidence and the fixtures were written by an author who knew the benchmark's tasks.
14. **Fixtures.** They are hand-written, were scored with one fold's models, and show mechanisms, not rates.
15. **Three close works are known from abstracts** (NEXUS also from repository documentation); statements about them may change when their full texts are read.
16. **No published defense was run**, so no statement about relative performance is supported.

## 4.20 Chapter Summary

This chapter reported an evaluation of REM on recorded trajectories of real agents in the AgentDojo banking environment. No live agent was run.

- **Prediction.** On attack objectives not seen in fitting, the calibrated estimator reaches a held-out ROC-AUC of 0.938. Calibration left the probabilities almost unchanged and did not repair the one miscalibrated fold.
- **Replay on the primary recordings.** REM v1.0 reduces attack success from 22.6% to 0.4% and benign task completion from 52% to 31%. It releases 33 of 178 authorized state-changing calls.
- **Rules.** Rules that use one or two pieces of provenance evidence and no model reach the same security with 40% to 42% benign task completion. One of them fails when the attacker's identifier is reformatted.
- **Generalization.** REM v1.0's results do not change when the user task is also held out. A candidate policy supervised on intervention outcomes with authorization features was rejected: 132 successful attacks against 11.
- **Confirmatory run.** On 2,113 untouched episodes, REM without behavioral evidence completes 7.5 percentage points more tasks than REM v1.0 (95% interval 1.2 to 16.0) with 1 successful attack against 3. The pre-declared verdict is GO. Neither version is distinguishable from the rules.
- **Limit.** No policy tested separates an authorized payment from an unrequested one whose details occur in the user's request.
- **Not done.** Live-agent runs; any published defense; a human label audit; repeated runs.

Chapter 5 draws the conclusions.
