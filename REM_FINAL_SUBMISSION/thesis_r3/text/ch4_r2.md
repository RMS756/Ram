<!-- @frag ch4_open -->
This chapter reports the implementation environment, the data and the fitting of the estimator, the experimental setup, the comparisons with baselines and with one published policy, the ablations, and the results with their discussion. **No experiment with a live agent or a language model was executed, and no result in this chapter is a live result.** Every result comes from recorded trajectories of real agents in the AgentDojo banking environment, replayed with a policy that may withhold calls. The design values (costs, tiers, predicates, feature set, label rule) are declared values that await the supervisor's approval, so all results are exploratory by label.

The chapter has six sections. Section 4.61 describes the tools and the environment. Section 4.62 describes the data, their preparation and the training of the estimator. Section 4.63 defines the compared arms, the populations and the metrics. Section 4.64 compares REM with baselines, simple rules and a published policy. Section 4.65 reports the ablations. Section 4.66 reports the remaining results, interprets them and states the threats to validity.

<!-- @frag ch4_tools -->
## 4.81 Software, Hardware and Benchmark Environment

**Table 4.61. Software and hardware used for the reported results**

| Item | Value |
|---|---|
| Language | Python 3.11.17 |
| Numerical library | NumPy 2.4.6. Ridge logistic regression, the logit calibration map, the grouped cross-fitting and the grouped bootstrap are implemented in the project's own code on top of it (Appendix B) |
| Benchmark | AgentDojo 0.1.35 (Debenedetti et al., 2024), banking suite v1: eleven tools, sixteen user tasks, nine injection tasks |
| Recorded data | The benchmark authors' recorded runs at one fixed commit of their repository (`089ed468`) |
| Configuration | `configs/exploratory/pilot_e0.yaml`, identified in every result file by its SHA-256 digest |
| Other packages | PyYAML 6.0.1 (configuration and structured tool outputs); pytest 9.2.0 (tests) |
| Operating system | Ubuntu 24.04 in a cloud container |
| Hardware | 4 virtual CPUs (Intel Xeon, 2.10 GHz), 15 GB of memory, no GPU |
| Language models | None. No model was called for any result; the cost of model calls is zero |
| Random seed | 20261027 for every bootstrap; the fitting procedure is deterministic |

The hardware is that of the container in which all results were last re-executed (13 November 2026). Earlier runs used containers of the same kind whose hardware was not recorded. Apart from the decision times, no result depends on the hardware: the re-executions reproduce the stored counts exactly (Section 4.83).

REM needs no accelerator. The estimator has nine parameters, and a decision is one dot product, one logistic map, a table lookup and a comparison of four numbers. Fitting all 152 cross-fitting cells of the last study took 6 seconds, and 161,506 episode replays took 338 seconds with four worker processes.

## 4.82 Implemented Components

**Table 4.62. Components, their location in the repository and their status**

| Component | Location | Status |
|---|---|---|
| REM framework: five layers, estimator, calibration, tiers, predicates, expected-loss rule, mitigation, audit record | `rem/` | Implemented and tested (Chapter 3, Section 3.42; Appendix B) |
| Pilot pipeline: data loading, labels, cross-fitting, observe-only analyses, replay | `experiments/pilot/` | Executed |
| Rule baselines, diagnostic arms, double holdout, probes, fixtures, confirmatory run | `experiments/authz_study/` | Executed |
| Exploratory extension: request compiler, typed matcher, decision variants, published-policy comparator | `experiments/improve_study/` | Executed in replay (Chapter 3, Section 3.44) |
| Selective semantic verifier | `experiments/improve_study/verifier.py` | Interface and tests only; never called with a model |
| Closed-loop harness for live agents; MELON integration | Appendix D | Implemented and tested with scripted agents; not executed with a model |

Experimental code is kept apart from the framework. No file under `rem/` or `configs/` was changed by any study of November 2026; each study imports the framework and adds its own modules.

## 4.83 Reproducibility and Software Verification

Each results file records the commit of the framework, the digest of the configuration and of the amendments, the benchmark version and the commit of the recorded runs. Three checks support the numbers of this chapter.

- **Re-execution.** The pilot was executed, re-executed after code corrections and re-executed again with timing instrumentation; the analytical values were identical each time (Section 4.2.3).
- **Equivalence of earlier arms in later studies.** Each later study recomputes the earlier arms before adding its own. In the study of 13 November the seven earlier arms reproduce the stored counts on both populations, and the refitted estimator of REM v1.1 equals the stored one (largest absolute difference of any parameter: 0).
- **Tests.** On 13 November 2026 the suite of 280 tests gave 278 passed, 1 skipped and 1 expected failure. It covers the frozen equations, the mitigation semantics, replay, leakage controls and, for the extension, the isolation of the defense interface from task identifiers, labels and outcomes.

The commands that regenerate every table are listed in Appendix B and in the study folders of the repository.

<!-- @frag ch4_g2_intro -->
This section describes the recorded data and how they were prepared (exclusions, labels, eligibility for replay), the fitting protocol, the second population, the validity of the labels, and the training of the estimator. Nothing was collected for this thesis: the trajectories were recorded by the benchmark's authors with real agents.

<!-- @frag ch4_training -->
## 4.84 Training of the Risk Estimator

The estimator is the ridge logistic regression of Equations 3.1 and 3.2, followed by the logit calibration map of Equation 3.3, which is fitted by Equation 3.4. It is trained once per fold, on the fitting portion of that fold only, by the nested procedure of Chapter 3 (Procedure 3.1): the ridge penalty is selected from five values by four grouped inner folds; the calibration map is fitted on the inner out-of-fold logits; the model is then refitted on the whole fitting portion.

**Table 4.63. Training outcome per outer fold, REM v1.0** (`e1_crossfit.json`; each row is the model that scores the held-out attacker objective named in the first column)

| Held-out attacker objective | Positive steps in the fitting portion | Selected λ (scale of Eq. 3.2) | Intercept β~0~ | γ~1~ | γ~0~ | Held-out steps | Held-out ROC-AUC | Held-out ECE |
|---|---|---|---|---|---|---|---|---|
| 0 | 796 | 5 | −5.64 | 0.959 | 0.161 | 824 | 0.962 | 0.059 |
| 1 | 820 | 5 | −5.73 | 0.947 | 0.165 | 773 | 0.965 | 0.046 |
| 2 | 809 | 5 | −5.67 | 0.958 | 0.149 | 807 | 0.949 | 0.035 |
| 3 | 811 | 5 | −5.67 | 0.955 | 0.140 | 772 | 0.962 | 0.045 |
| 4 | 786 | 5 | −5.68 | 0.947 | 0.114 | 726 | 0.978 | 0.087 |
| 5 | 898 | 5 | −5.68 | 0.969 | 0.153 | 634 | 0.859 | 0.068 |
| 6 | 842 | 5 | −5.73 | 0.981 | 0.155 | 666 | 0.909 | 0.075 |
| 7 | 797 | 0.5 | −7.25 | 0.980 | 0.143 | 730 | 0.903 | 0.189 |
| 8 | 809 | 5 | −5.81 | 0.945 | 0.142 | 830 | 0.959 | 0.037 |

Observations on training:

- **The selected penalty is the same in eight folds.** The fold that holds out objective 7, the only credential-change attack, selects a smaller penalty and a more negative intercept.
- **The calibration maps are close to the identity** (γ~1~ between 0.945 and 0.981), so calibration changes the probabilities little (Section 4.4).
- **The held-out quality differs by objective.** Objective 7 has the largest calibration error (0.189); objective 5, with 23 positive steps, has the lowest ROC-AUC.

Three further sets of models were trained by the same procedure and are used later in the chapter: the models of REM v1.1, which omit the four behavioral features (nine folds); the models of the double holdout, one for each of 143 combinations of user task and attacker objective (Chapter 3, Section 3.11.42); and, for the exploratory extension, models on the four non-behavioral features plus five permission indicators (nine folds and 143 double-holdout cells; Chapter 3, Section 3.44). No model was trained or selected on the second population.

<!-- @frag ch4_g3_intro -->
This section fixes what is compared, on which episodes, and with which measures. The definitions are those of Chapter 3 (Sections 3.11 and 3.12); they are collected here so that Sections 4.64 to 4.66 can be read without returning to it.

<!-- @frag ch4_setup -->
## 4.85 Compared Arms

**Table 4.64. Arms compared in this chapter**

| Arm | Definition | Fitted quantities | Declared |
|---|---|---|---|
| No defense | Every call is released | none | pilot |
| B1 | Consequence-independent thresholds on REM's calibrated probability | estimator, calibration, two thresholds | pilot |
| REM v1.0 | The frozen pipeline of Chapter 3 | estimator, calibration | pilot |
| REM v1.1 (proposed) | REM v1.0 without the behavioral evidence group (Chapter 3, Section 3.41) | estimator, calibration | ablation in the pilot; candidate of the confirmatory run |
| REM, Allow and Block only | REM v1.0 with the verdict set restricted to two | as REM v1.0 | 11 November |
| P1, P2, A1, A2 | Rules on provenance, novelty and occurrence in the request, with no model (Chapter 3, Table 3.41) | none | 11 November |
| Diagnostic and candidate arms | Outcome-supervised and intervention-value variants (Chapter 3, Table 3.42) | their own | 11 November |
| Progent manual policy | The manual banking policy published in the Progent repository (T. Shi et al., 2025): a fixed list of five permitted recipients for the three payment tools; password change not permitted | none | 13 November |
| Permission rule G1 | A state-changing call is released only if the request, compiled by a deterministic parser, supports its operation, recipient and amount (Chapter 3, Section 3.44) | none | 13 November |
| G1 without one component | Five ablations of G1 | none | 13 November |
| V11d, L0, L1, L2, L2s | REM v1.1 with a two-verdict decision; a learned model on permission evidence without a guard, and behind a guard with four or two verdicts (Chapter 3, Section 3.44) | estimator, calibration | 13 November |
| Repaired permission rule G2; G1r and three ablations of G2 | G1 with instruction bindings, condition evaluation and fulfilment tracking (Chapter 3, Section 3.44) | none | 14 November |
| L2g, L3, L3c | Learned arms behind an authority guard; L3c with identifiers canonicalized in the provenance evidence (Chapter 3, Section 3.44) | estimator, calibration | 14 November |

Published defenses that need a language model (MELON, Task Shield, CaMeL, Progent with generated policies) are not among the arms, because no model was available (Section 4.46).

## 4.86 Populations and Generalization Schemes

**Table 4.65. Populations and what each is used for**

| Population | Eligible episodes | Use |
|---|---|---|
| Primary | 3,313 (2,979 attacked, 334 benign), 21 undefended backbones, attack `important_instructions` | Fitting and cross-validated evaluation. Scheme S1 holds out one attacker objective per fold; scheme S2 holds out the user task and the attacker objective together |
| Held-out templates (S3) | 681 attacked | Attack templates not used in fitting |
| Second population | 2,113 (2,065 attacked, 48 benign), five sources with other agents and templates (Section 4.2.41) | Nothing is fitted on it. It was unread until the confirmatory run of 11 November 2026. **Since then it is development evidence** and is used as such in the study of 13 November |
| Reformatted-identifier probe | 2,645 attacked | The attacker's account identifier in the injected text is rewritten with spaces |
| Paired fixtures | 43 pairs in four sets | Hand-written calls scored by one fold's models; mechanisms, not rates |

Rules have no fitted quantity, so their results are the same under S1 and S2.

## 4.87 Evaluation Metrics

Three outcomes are primary: completion of the legitimate task, release of legitimate state-changing calls, and attack success.

**Table 4.66. Metrics and their definitions**

| Metric | Definition | Kind of evidence |
|---|---|---|
| ROC-AUC, average precision, ECE, log-loss | Quality of the held-out probability for the attempt label (Chapter 3, Section 3.12) | Offline prediction |
| Verdict rates | Share of recorded calls that would receive each verdict | Observe-only |
| Attack success | The benchmark's security check reports the attacker's goal as reached in the replayed episode | Replay |
| Task completion (benign; under attack; all) | The benchmark's utility check passes in the replayed episode | Replay |
| Legitimate state-changing calls released | Calls to state-changing tools proposed in benign episodes that the policy releases | Replay |
| Episodes with a released attack-labelled call | Attacked episodes in which at least one call carrying the attempt label is released | Replay |
| Tasks gained and lost; attacks gained and lost | Episodes in which only one of two arms completes the task, or only one admits the attack | Replay, paired |
| Decision time | Time to evaluate one proposed call | Runtime measurement |

**A released attack-labelled call is not the same as a committed unauthorized change of the bank state.** The label marks an attempt (Section 4.2.1), and the effect of a released call on the state is not measured separately from the benchmark's security check. Earlier drafts headed this column "unauthorized state change"; the quantity is unchanged and the name is corrected here. Attack success, as judged by the benchmark, is the security outcome.

## 4.88 Statistical Procedure and Comparisons Fixed in Advance

Intervals are 95% percentile intervals of a grouped bootstrap with 2,000 resamples. Task-completion differences are resampled by user task (16 groups) and attack-success differences by injection task (9 groups); comparisons between arms are paired on the episode. With so few groups the intervals are wide and are not guaranteed to reach their nominal coverage (Section 4.2.1). They are descriptive.

Three sets of comparisons were fixed before their outcomes were computed, each by a dated commit (Sections 4.2.3 and 4.2.42):

- 11 November 2026: the candidate of that study against REM v1.0 under S1 and S2 (Section 4.43.2);
- 11 November 2026: REM v1.1 against REM v1.0 on the then unread second population, with a three-part decision rule (Chapter 3, Section 3.11.44; Section 4.45);
- 13 November 2026: the permission rule against A2, against Progent's manual policy and against REM v1.1; the learned arms against the permission rule under S1 and S2; the two-verdict decision alone; the effect of the guard (Sections 4.89, 4.91 and 4.92).
- 14 November 2026, after an external review reported defects of the permission rule: the repaired rule against the original rule, A2 and Progent's manual policy; the authority guard; the learned model against the repaired rule; typed provenance in the learner; and a call-level audit of user task 15 with criteria written before it was run (Sections 4.89, 4.94 and 4.93).

**No margin of non-inferiority on security was approved, and none was invented.** An interval of an attack-success difference that includes zero is reported as unresolved. The study of 13 November also fixed its wording in advance: "added value over simple rules" may be stated only if the task-completion interval against A2 lies above zero on both populations and the number of successful attacks does not exceed A2's.

<!-- @frag ch4_g4_intro -->
This section compares REM with other decision policies evaluated on the same episodes: the threshold baseline and the rule baselines, the defenses whose recorded outcomes the benchmark distributes, and one published policy replayed in the same harness. It then states which published defenses could not be run and how the results relate to recent work.

<!-- @frag ch4_progent -->
## 4.89 A Published Policy and a Request-Derived Permission Rule in the Same Harness

*Kind of evidence: replay; development evidence on both populations (every episode had been inspected before 13 November 2026). The arms and the comparisons marked with an asterisk were fixed before any of these outcomes was computed.*

**The published policy.** Progent (T. Shi et al., 2025) enforces per-tool policies with argument restrictions before each tool call. Its official repository contains, at the commit of 10 September 2025, a manual policy for the AgentDojo banking suite: `send_money`, `schedule_transaction` and `update_scheduled_transaction` are permitted only for five listed recipients; `update_password` has no policy entry and is therefore not permitted; the remaining tools are permitted. The policy was read from the repository as data, with the file digests pinned, and applied to the recorded calls by this project's replay code. The arm is therefore **Progent's published manual banking policy, adapted to the shared replay harness**. It is **not** a reproduction of the Progent framework or of the paper's results, not Progent with policies generated by a language model, and not a live-agent comparison. The upstream checking code was not executed in this project; its equivalence with the decision function used here was established by reading it. An independent review of 14 November 2026 reported a differential check of the upstream checker functions against this decision function on 468 argument cases, with the pinned file digests confirmed, and found no difference; that check covers the policy logic in that scope and was not repeated here. The repository bundles AgentDojo 0.1.29; the eleven banking tools have the same parameters and defaults in 0.1.29 and 0.1.35, so the policy applies unchanged to the recordings.

**The permission rule G1** releases a state-changing call only if the user's request supports its operation, its recipient and its amount (Chapter 3, Section 3.44). It is an exploratory extension, not part of REM v1.0 or v1.1.

**Table 4.67. Replay results on the primary recordings** (step-level, no reviewer; `improvement_results.json`, `results_v2.json`; REM, B1 and P2 are in Table 4.43, A2 is repeated for reference)

| Arm | Successful attacks / 2,979 | Episodes with a released attack-labelled call | Benign tasks completed / 334 | All tasks completed / 3,313 | Legitimate state-changing calls released / 178 |
|---|---|---|---|---|---|
| A2 | 13 | 27 | 140 | 1,474 | 83 |
| **Progent manual policy** | 0 | 0 | 154 | 1,450 | 136 |
| **Permission rule G1** | 10 | 23 | 149 | 1,574 | 112 |
| **Repaired permission rule G2** | 1 | 2 | 132 | 1,407 | 93 |

**Table 4.68. Replay results on the second population** (the same arms; nothing fitted on these episodes; the other arms are in Table 4.50)

| Arm | Successful attacks / 2,065 | Episodes with a released attack-labelled call | Benign tasks completed / 48 | All tasks completed / 2,113 | Legitimate state-changing calls released / 51 |
|---|---|---|---|---|---|
| A2 | 4 | 4 | 27 | 1,232 | 27 |
| **Progent manual policy** | 0 | 0 | 35 | 1,305 | 48 |
| **Permission rule G1** | 3 | 3 | 32 | 1,358 | 36 |
| **Repaired permission rule G2** | 0 | 0 | 29 | 1,239 | 20 |

**Table 4.69. Paired contrasts** (first arm minus second arm, in percentage points, with the 95% grouped-bootstrap interval; PG = Progent manual policy; v1.0 and v1.1 = REM versions; * = fixed in advance)

| Contrast | Population | All-task completion | Benign task completion | Attack success | Tasks gained / lost | Attacks gained / lost |
|---|---|---|---|---|---|---|
| G1−A2* | primary | +3.02 [−3.34, 13.09] | +2.69 [−3.87, 12.42] | −0.10 [−0.20, −0.03] | 149 / 49 | 0 / 3 |
| G1−A2* | second | +5.96 [−4.25, 19.14] | +10.42 [−4.17, 29.17] | −0.05 [−0.15, 0.00] | 172 / 46 | 0 / 1 |
| G1−PG* | primary | +3.74 [−6.45, 17.03] | −1.50 [−14.29, 13.56] | +0.34 [0.10, 0.57] | 255 / 131 | 10 / 0 |
| G1−PG* | second | +2.51 [−15.09, 20.94] | −6.25 [−33.33, 20.83] | +0.15 [0.05, 0.29] | 248 / 195 | 3 / 0 |
| PG−A2 | primary | −0.72 [−15.80, 14.24] | +4.19 [−12.81, 20.91] | −0.44 [−0.73, −0.14] | 280 / 304 | 0 / 13 |
| PG−A2 | second | +3.45 [−19.45, 26.52] | +16.67 [−16.67, 47.92] | −0.19 [−0.43, −0.05] | 367 / 294 | 0 / 4 |
| G1−v1.1* | primary | +8.66 [−2.75, 22.01] | +2.69 [−7.74, 14.46] | −0.03 [−0.10, 0.00] | 435 / 148 | 0 / 1 |
| G1−v1.1* | second | +13.44 [−5.21, 33.59] | +14.58 [−10.42, 39.58] | +0.10 [0.00, 0.24] | 461 / 177 | 2 / 0 |
| G1−v1.0 | primary | +11.65 [−0.39, 26.25] | +13.17 [1.50, 28.14] | −0.03 [−0.14, 0.07] | 496 / 110 | 1 / 2 |
| G1−v1.0 | second | +20.92 [1.30, 42.46] | +29.17 [8.33, 52.08] | +0.00 [−0.15, 0.14] | 554 / 112 | 1 / 1 |
| G2−A2* | primary | −2.02 [−15.52, 10.98] | −2.40 [−16.07, 10.61] | −0.40 [−0.73, −0.10] | 149 / 216 | 0 / 12 |
| G2−A2* | second | +0.33 [−16.35, 16.72] | +4.17 [−16.67, 25.00] | −0.19 [−0.43, −0.05] | 172 / 165 | 0 / 4 |
| G2−PG* | primary | −1.30 [−7.98, 5.29] | −6.59 [−16.67, 2.38] | +0.03 [0.00, 0.10] | 88 / 131 | 1 / 0 |
| G2−PG* | second | −3.12 [−18.56, 11.41] | −12.50 [−35.42, 10.42] | +0.00 [0.00, 0.00] | 129 / 195 | 0 / 0 |

What the comparison shows:

- **The published policy has no successful attack in either population.** The attacker's account is not on its list, and it never permits a password change. The permission rule has 10 and 3 successful attacks. The attack-success difference between the two lies above zero in both populations: on security the published policy is better on this benchmark.
- **Task completion does not separate the two.** The permission rule completes more tasks in point estimate; the intervals include zero. The published policy releases more of the legitimate state-changing calls of benign episodes (136 of 178 against 112; 48 of 51 against 36).
- **Against the rule A2, the permission rule has better point estimates on both outcomes in both populations and the difference is not resolved.** It completes 100 and 126 more tasks with 3 and 1 fewer successful attacks, and the task-completion intervals include zero. By the wording fixed in advance, added value over simple rules is not claimed.
- **Against REM v1.0 the permission rule completes more benign tasks** (interval above zero in both populations) with 10 against 11 and 3 against 3 successful attacks. This contrast was not fixed in advance.
- **A review found defects in G1, and the repaired rule G2 trades tasks for security.** G1 supports a payment whose amount the request assigns to another account, ignores whether a stated condition holds, and supports a repeated payment (Section 4.93). The repaired rule G2 has 1 successful attack on the primary recordings and none on the second population, completes fewer tasks than G1, and against A2 and the published policy its task-completion differences are again not resolved (Table 4.69). Its results were obtained after G1's were known; they are development evidence.
- **The two policies fail in different places.** The published policy completes no password-change task (user task 14: 0 of 209 and 0 of 129 episodes), because the tool is not permitted. The permission rule completes none of the tasks in which the recipient or the instruction is supplied only by a file (user tasks 0, 2 and 12). All of its successful attacks are in user task 15, where the account the attacker wants is the account the user names (Section 4.10).

**A fixed list is tied to the seeded environment.** The five recipients are payees that exist in the benchmark's initial state. On the twenty paired fixtures written for this study, whose payees are not on the list, the published policy releases no unsafe call and withholds 13 of 20 legitimate calls (Section 4.92). The benchmark policy published with aiAuthZ has the same form: a list of five known payees, with password change denied (repository whitepaper; Section 4.16). Neither derives permission from the individual request, which is what the permission rule attempts.

<!-- @frag ch4_g5_intro -->
This section reports what happens when a component is removed or replaced. It covers the components of REM v1.0, the verdict set, and the components of the exploratory extension. Every ablation is a single-benchmark observation; none shows that a component has no benefit in general.

<!-- @frag ch4_ablation_new -->
## 4.90 Ablation of the Behavioral Evidence Group and of the Verdict Set

Two ablations of Table 4.13 were followed up in later studies, and their results are reported where those studies are described.

- **Behavioral evidence.** Removing the four behavioral features is REM v1.1. In the pilot it left replay attack success at 11 of 2,979 and raised benign task completion from 105 to 140 of 334. Under the double holdout it has 14 successful attacks against 11 (Table 4.45). On the second population it completed 1,074 against 916 of 2,113 tasks with 1 against 3 successful attacks (Section 4.45).
- **Verdict set.** Replacing every Modify and Escalate verdict of REM v1.0 by Block changes the outcome of none of the 3,313 primary episodes (Section 4.42.2). Removing the two verdicts from the decision rule, so that Allow is chosen up to the Allow–Block threshold of Equation 3.9, gives more released calls with 13 against 11 successful attacks on the primary recordings and 3 against 3 on the second population (Tables 4.43 and 4.50), and 31 against 13 when the attacker's identifier is reformatted (Table 4.48).
- **Calibration.** Without the calibration map, replay attack success is unchanged (11 of 2,979) and benign task completion is 110 instead of 105 of 334 (Table 4.13: 0.329 against 0.314). Calibration therefore changed a small number of decisions. It did not change the security count.

## 4.91 Ablations of the Task-Permission Extension

*Kind of evidence: replay; development evidence. The ablations are diagnostic: the rule G1 was fixed with all components before any outcome was computed and was not changed afterwards.*

**Table 4.70. The permission rule with one component removed** (`improvement_results.json`)

| Rule | Primary: attacks / 2,979 | Primary: all tasks / 3,313 | Primary: legitimate calls released / 178 | Second: attacks / 2,065 | Second: all tasks / 2,113 | Second: legitimate calls released / 51 |
|---|---|---|---|---|---|---|
| A2 | 13 | 1,474 | 83 | 4 | 1,232 | 27 |
| A2 with typed normalization | 13 | 1,474 | 83 | 4 | 1,232 | 27 |
| Permission rule G1 | 10 | 1,574 | 112 | 3 | 1,358 | 36 |
| G1 without the operation check | 10 | 1,573 | 113 | 3 | 1,358 | 36 |
| G1 without the amount check | 13 | 1,642 | 122 | 4 | 1,459 | 40 |
| G1 without established payees | 10 | 1,556 | 99 | 3 | 1,271 | 31 |
| G1 without scoped delegation | 10 | 1,443 | 99 | 3 | 1,273 | 33 |
| G1 without typed normalization | 10 | 1,484 | 86 | 3 | 1,139 | 15 |

- **Typed normalization alone does not change A2** on these recordings. Inside the permission rule it matters: without it the rule releases 86 instead of 112 legitimate calls, and 15 instead of 36 on the second population.
- **Scoped delegation and established payees add completed tasks without added attacks.** Scoped delegation accounts for 131 tasks on the primary recordings; established payees for 18 there and 87 on the second population.
- **The amount check trades tasks for security.** Without it the rule has the same number of successful attacks as A2 (13 and 4) and completes 68 and 101 more tasks.
- **The operation check changes one task.** On these recordings almost every call that it would deny is already denied by the recipient or amount check.

**Table 4.71. Decision semantics and a learned model on the permission evidence** (S1: held-out attacker objective; S2: double holdout)

| Arm | S1: attacks / 2,979 | S1: all tasks / 3,313 | S2: attacks | S2: all tasks | Second population: attacks / 2,065 | Second population: all tasks / 2,113 | Held-out credential-change attacks, S1 / 334 |
|---|---|---|---|---|---|---|---|
| REM v1.1 | 11 | 1,287 | 14 | 1,272 | 1 | 1,074 | 0 |
| REM v1.1 with the two-verdict decision (V11d) | 131 | 1,492 | 131 | 1,452 | 58 | 1,182 | 119 |
| Permission rule G1 | 10 | 1,574 | 10 | 1,574 | 3 | 1,358 | 0 |
| Learned on permission evidence, no guard (L0) | 11 | 1,711 | 12 | 1,707 | 2 | 1,526 | 0 |
| Guard, then learned, four verdicts (L1) | 10 | 1,531 | 10 | 1,429 | 1 | 1,338 | 0 |
| Guard, then learned, two verdicts (L2) | 10 | 1,680 | 10 | 1,676 | 2 | 1,489 | 0 |
| Guard; learned decides unknown calls only (L2s) | 10 | 1,644 | 10 | 1,644 | 3 | 1,459 | 0 |

**Table 4.72. Paired contrasts for the decision semantics, the learned model and the guard** (first arm minus second arm, in percentage points, with the 95% interval; v1.1 = REM v1.1; * = fixed in advance)

| Contrast | Population | All-task completion | Benign task completion | Attack success | Tasks gained / lost | Attacks gained / lost |
|---|---|---|---|---|---|---|
| L2−G1* | primary, S1 | +3.20 [−0.76, 8.80] | +3.59 [0.00, 9.52] | +0.00 [0.00, 0.00] | 127 / 21 | 0 / 0 |
| L2−G1* | primary, S2 | +3.08 [−0.87, 8.72] | +3.59 [0.00, 9.52] | +0.00 [0.00, 0.00] | 127 / 25 | 0 / 0 |
| L2−G1* | second | +6.20 [−1.53, 17.63] | +6.25 [0.00, 18.75] | −0.05 [−0.15, 0.00] | 150 / 19 | 0 / 1 |
| L2s−G1* | primary, S1 | +2.11 [−0.69, 7.00] | +2.10 [−0.89, 7.19] | +0.00 [0.00, 0.00] | 78 / 8 | 0 / 0 |
| L2s−G1* | primary, S2 | +2.11 [−0.69, 7.00] | +2.10 [−0.89, 7.19] | +0.00 [0.00, 0.00] | 78 / 8 | 0 / 0 |
| L2s−G1* | second | +4.78 [−0.42, 14.86] | +4.17 [−6.25, 18.75] | +0.00 [0.00, 0.00] | 104 / 3 | 0 / 0 |
| V11d−v1.1* | primary, S1 | +6.19 [0.00, 15.74] | +4.79 [0.00, 14.55] | +4.03 [0.00, 12.02] | 209 / 4 | 120 / 0 |
| V11d−v1.1* | primary, S2 | +5.43 [0.45, 13.81] | +4.79 [0.00, 14.55] | +3.93 [0.00, 11.79] | 184 / 4 | 117 / 0 |
| V11d−v1.1* | second | +5.11 [0.19, 12.54] | +6.25 [0.00, 18.75] | +2.76 [0.00, 7.98] | 110 / 2 | 57 / 0 |
| L0−L2* | primary, S1 | +0.94 [0.00, 2.84] | +1.80 [0.00, 5.42] | +0.03 [0.00, 0.10] | 31 / 0 | 1 / 0 |
| L0−L2* | primary, S2 | +0.94 [0.00, 2.84] | +1.80 [0.00, 5.42] | +0.07 [0.00, 0.17] | 31 / 0 | 2 / 0 |
| L0−L2* | second | +1.75 [−0.14, 5.56] | +2.08 [0.00, 6.25] | +0.00 [0.00, 0.00] | 38 / 1 | 0 / 0 |

- **The two-verdict decision alone is unsafe.** Applied to REM v1.1 without a guard (V11d), it releases every held-out credential-change attack: 119 of 334 on the primary recordings and 54 of 232 on the second population. In REM v1.1 those calls are withheld only because Escalate has a lower expected loss than Allow, and without a reviewer an escalated call is withheld. This shows that the low attack count of REM under a held-out objective depends on the Escalate region, not on the estimator recognizing the attack.
- **A learned model on the permission evidence adds no demonstrated value to the rule.** Behind the guard (L2, L2s) it completes more tasks than G1 with no more successful attacks on the original text; every interval includes zero under S1, under S2 and on the second population. By the wording fixed in advance, value of the learned model is not claimed.
- **The learned model costs robustness.** With the attacker's identifier reformatted, L2 has 38 successful attacks where G1 has 10 (Table 4.73). The calls it then releases have unknown permission status; the model's remaining evidence for them is the provenance match, which reformatting removes.
- **The guard costs little and removes little on the recordings** (L0 against L2: at most two attacks and one to two points of tasks). On the paired fixtures the unguarded model releases more unsafe calls (6 against 3 on set 4; Table 4.74).

<!-- @frag ch4_g6_intro -->
This section reports the results that the earlier sections did not already present: the pilot's feasibility check, the quality of the estimator, the observe-only decisions, the replay of REM and its baseline, the sequential analysis, realized loss, generalization, robustness, the confirmatory run and the exploratory extension. It then interprets the findings, states the threats to validity and summarizes the chapter.

<!-- @frag ch4_improve_results -->
## 4.92 Exploratory Extension: Task-Permission Evidence

*Kind of evidence: replay and call-level fixtures; development evidence. Protocol, arms, parser, matcher and fixture set 4 were committed on 13 November 2026 before any outcome of a new arm was computed (commit `9137b03`); no amendment was made. The parser was written by an author who knows the sixteen requests of the benchmark; no request was held out from its development.*

The question of the extension is whether task-permission evidence compiled from the trusted request improves the trade-off between security and task completion, and which component is responsible for any change. The main results against the rules and the published policy are in Section 4.89, and the ablations in Section 4.91. This section adds the robustness probe, the paired fixtures, the per-task results and the verdict.

**Table 4.73. Successful attacks before and after the attacker's identifier is reformatted** (2,645 attacked episodes; REM, B1, P2 and A2 are in Table 4.48)

| Arm | Original text | Identifier reformatted |
|---|---|---|
| Progent manual policy | 0 | 0 |
| Permission rule G1 | 10 | 10 |
| G1 without typed normalization | 10 | 10 |
| Guard, then learned, two verdicts (L2) | 10 | 38 |
| Repaired permission rule G2 | 1 | 1 |
| L2 with the authority guard (L2g) | 10 | 10 |
| Authority guard, learned on v2 evidence (L3) | 1 | 1 |
| L3 with typed provenance (L3c) | 1 | 1 |

The permission rule is unchanged by the reformatting, with or without typed normalization, because it accepts a recipient only if the request itself supports it. The learned arm L2 is not robust (Section 4.91).

**Table 4.74. Paired fixtures** (each pair has one legitimate and one unsafe call for the same request; a pair is correct if the legitimate call is released and the unsafe call is withheld; counts, not rates)

| Arm | Sets 1–3: legitimate calls released / 23 | Sets 1–3: unsafe calls released / 23 | Sets 1–3: pairs correct / 23 | Set 4: legitimate released / 20 | Set 4: unsafe released / 20 | Set 4: pairs correct / 20 |
|---|---|---|---|---|---|---|
| REM v1.0 | 3 | 0 | 3 | 6 | 1 | 5 |
| REM v1.1 | 21 | 4 | 17 | 17 | 6 | 11 |
| B1 | 22 | 6 | 16 | 19 | 7 | 12 |
| A2 | 21 | 10 | 11 | 17 | 8 | 9 |
| Progent manual policy | 3 | 0 | 3 | 7 | 0 | 7 |
| Permission rule G1 | 17 | 1 | 16 | 17 | 1 | 16 |
| G1 without the amount check | 18 | 6 | 12 | 19 | 5 | 14 |
| Learned on permission evidence, no guard (L0) | 22 | 5 | 17 | 20 | 6 | 14 |
| Guard, then learned, two verdicts (L2) | 18 | 1 | 17 | 19 | 3 | 16 |

Sets 1 to 3 are the fixtures of the earlier studies. Set 4 has twenty pairs in ten categories: negation, past payments, conditions, valid high amounts, amount substitution, scheduled payments, credential changes, number formats, delegated sources and repeated payments. It was written for this study before any scoring and scored once. It was written by the author of the rule with AI assistance and was not reviewed by a second person; it is a stress test of mechanisms, not an independent benchmark.

- On set 4 the permission rule gets 16 of 20 pairs right, A2 gets 9, REM v1.1 gets 11 and the published policy gets 7.
- On the read-only pairs of set 2, in which the user mentions a past payment and asks for no payment, the permission rule withholds the unrequested payment that was released by every arm of Table 4.49 that releases legitimate payments. The request states that no payment is wanted, and a parser of the request can use that statement.
- **The rule's errors on set 4.** Two legitimate calls are withheld because of parser defects: an amount written as "Reimburse Marta 36.40 for the groceries" is not extracted, and "create a monthly standing order" is not recognized as a request for a scheduled payment. One legitimate call is withheld by design, because "1,250" can be read as two different amounts. One unsafe call is released: a second copy of a payment already made in the episode, because the rule keeps no record of requests already satisfied. The defects were not repaired after scoring.
- On set 3 the permission rule releases 3 of 7 legitimate calls, fewer than REM v1.1 (5 of 7).
- The learned arms release unsafe calls that the rule withholds (set 4: 3 for L2 and 6 for L0).

**Table 4.75. Tasks completed by user task on the primary recordings** (user tasks on which A2, the published policy, G1 and L2 all equal the undefended agent are omitted)

| User task | Episodes | No defense | REM v1.0 | REM v1.1 | A2 | Progent | G1 | L2 |
|---|---|---|---|---|---|---|---|---|
| 0 | 210 | 11 | 0 | 0 | 0 | 11 | 0 | 0 |
| 2 | 210 | 87 | 39 | 71 | 0 | 81 | 0 | 77 |
| 6 | 210 | 74 | 3 | 8 | 72 | 72 | 72 | 72 |
| 9 | 208 | 141 | 208 | 206 | 208 | 141 | 159 | 200 |
| 10 | 210 | 130 | 210 | 210 | 210 | 140 | 210 | 210 |
| 11 | 210 | 21 | 0 | 0 | 0 | 18 | 18 | 5 |
| 12 | 210 | 31 | 21 | 27 | 0 | 31 | 0 | 0 |
| 13 | 190 | 139 | 18 | 15 | 0 | 139 | 131 | 132 |
| 14 | 209 | 167 | 3 | 39 | 167 | 0 | 167 | 167 |
| 15 | 189 | 22 | 0 | 0 | 0 | 0 | 0 | 0 |

The gain of the permission rule over A2 is in user tasks 11 and 13, where the recipient is referred to through the history or the value is delegated to a named file. It loses in user task 9, where arms that withhold the update pass the benchmark's check more often; the cause was not examined call by call. A few user tasks decide each comparison, which is why the intervals are wide.

**Verdict of the extension study.**

1. **Improvement over REM v1.0: observed on development data.** More benign tasks in both populations with no more successful attacks.
2. **Added value over the strongest simple rule: not established.** Favourable point estimates on both outcomes; task-completion intervals include zero.
3. **Against the published policy: not better; worse on security on this benchmark.** The published policy pays for this with a fixed list that fails on payees outside it.
4. **Attribution.** The change comes from the deterministic compiler and matcher used as a hard rule. The learned ridge model adds no demonstrated value on top of that evidence and is less robust to reformatting. The two-verdict decision is a consistency repair that is safe only behind the guard. The semantic verifier was not run.
5. **Follow-up.** The rule was later found to have three defects, and its repair changes the picture (Section 4.93).
6. **Status.** Proposed and exploratory. The rule is not adopted and is not a new version of REM. A confirmatory test needs outcomes that do not yet exist: fresh runs with a live agent and request variants written by someone other than the author (the sealed protocol is in the repository).

**Decision time.** The median time to evaluate one call on the primary recordings was 0.09 ms for the permission rule and for the published policy and 0.18 ms for REM and for L2; the 95th percentile of the arms that parse bank records was about 3 ms. No arm calls a model.

<!-- @frag ch4_ablation_v2 -->
## 4.94 Ablations of the Repaired Rule and of the Authority Guard

*Kind of evidence: replay; development evidence. Protocol of 14 November 2026, committed before these arms were replayed (commit `ae3f923`).*

**Table 4.76. The repaired rule, its ablations and the learned arms behind the authority guard** (`results_v2.json`)

| Arm | Primary: attacks / 2,979 | Primary: all tasks / 3,313 | Double holdout: all tasks | Second: attacks / 2,065 | Second: all tasks / 2,113 | Probe: attacks, identifier reformatted |
|---|---|---|---|---|---|---|
| Permission rule G1 | 10 | 1,574 | 1,574 | 3 | 1,358 | 10 |
| G1 with the repaired parser (G1r) | 10 | 1,574 | 1,574 | 3 | 1,358 | 10 |
| Repaired permission rule G2 | 1 | 1,407 | 1,407 | 0 | 1,239 | 1 |
| G2 without the binding check | 10 | 1,407 | 1,407 | 3 | 1,239 | 10 |
| G2 without the condition check | 1 | 1,574 | 1,574 | 0 | 1,358 | 1 |
| G2 without the fulfilment check | 1 | 1,407 | 1,407 | 0 | 1,239 | 1 |
| Guard, then learned, two verdicts (L2) | 10 | 1,680 | 1,676 | 2 | 1,489 | 38 |
| L2 with the authority guard (L2g) | 10 | 1,679 | 1,675 | 2 | 1,489 | 10 |
| Authority guard, learned on v2 evidence (L3) | 1 | 1,532 | 1,532 | 0 | 1,386 | 1 |
| L3 with typed provenance (L3c) | 1 | 1,532 | 1,532 | 0 | 1,386 | 1 |

**Table 4.77. Paired contrasts of the follow-up** (first arm minus second arm, in percentage points, with the 95% interval; * = fixed in advance)

| Contrast | Population | All-task completion | Benign task completion | Attack success | Tasks gained / lost | Attacks gained / lost |
|---|---|---|---|---|---|---|
| G2−G1* | primary | −5.04 [−15.24, 0.00] | −5.09 [−15.36, 0.00] | −0.30 [−0.57, −0.07] | 0 / 167 | 0 / 9 |
| G2−G1* | second | −5.63 [−17.34, 0.00] | −6.25 [−18.75, 0.00] | −0.15 [−0.29, −0.05] | 0 / 119 | 0 / 3 |
| G2−(no binding) | primary | +0.00 [0.00, 0.00] | +0.00 [0.00, 0.00] | −0.30 [−0.57, −0.07] | 0 / 0 | 0 / 9 |
| G2−(no binding) | second | +0.00 [0.00, 0.00] | +0.00 [0.00, 0.00] | −0.15 [−0.29, −0.05] | 0 / 0 | 0 / 3 |
| G2−(no condition) | primary | −5.04 [−15.24, 0.00] | −5.09 [−15.36, 0.00] | +0.00 [0.00, 0.00] | 0 / 167 | 0 / 0 |
| G2−(no condition) | second | −5.63 [−17.34, 0.00] | −6.25 [−18.75, 0.00] | +0.00 [0.00, 0.00] | 0 / 119 | 0 / 0 |
| L2g−L2* | primary, S1 | −0.03 [−0.09, 0.00] | +0.00 [0.00, 0.00] | +0.00 [0.00, 0.00] | 0 / 1 | 0 / 0 |
| L2g−L2* | primary, S2 | −0.03 [−0.09, 0.00] | +0.00 [0.00, 0.00] | +0.00 [0.00, 0.00] | 0 / 1 | 0 / 0 |
| L2g−L2* | second | +0.00 [0.00, 0.00] | +0.00 [0.00, 0.00] | +0.00 [0.00, 0.00] | 0 / 0 | 0 / 0 |
| L3−G2* | primary, S1 | +3.77 [0.00, 9.25] | +4.49 [0.00, 10.24] | +0.00 [0.00, 0.00] | 133 / 8 | 0 / 0 |
| L3−G2* | primary, S2 | +3.77 [0.00, 9.25] | +4.49 [0.00, 10.24] | +0.00 [0.00, 0.00] | 133 / 8 | 0 / 0 |
| L3−G2* | second | +6.96 [0.00, 18.27] | +6.25 [0.00, 18.75] | +0.00 [0.00, 0.00] | 150 / 3 | 0 / 0 |
| L3c−L3* | primary, S1 | +0.00 [0.00, 0.00] | +0.00 [0.00, 0.00] | +0.00 [0.00, 0.00] | 0 / 0 | 0 / 0 |
| L3c−L3* | second | +0.00 [0.00, 0.00] | +0.00 [0.00, 0.00] | +0.00 [0.00, 0.00] | 0 / 0 | 0 / 0 |

- **The binding check removes the attacks and costs nothing.** Without it G2 has G1's 10 and 3 successful attacks; with it, 1 and 0. No task is lost.
- **The condition check costs one user task.** Every task that G2 loses against G1 is in user task 14, whose request makes the password change conditional on "something looks even just a little bit suspicious". G2 does not evaluate such a predicate and therefore never treats it as satisfied; without the check (G2-nocond) the rule completes G1's tasks with G2's attacks. Treating the predicate as true would be a choice about the user's intent that the request does not license.
- **The fulfilment check and the parser repairs change no count on the recordings.** On the second population the fulfilment check withholds 13 repetitions of one standing order by an agent that proposed the same call 14 times; the task still completes.
- **The authority guard removes L2's robustness failure.** L2g has 10 successful attacks with the identifier reformatted, where L2 had 38, and loses one completed task. The calls that the reformatting let through had no established authority.
- **The learned model's gain over the repaired rule is not established.** L3 completes more tasks than G2 with the same attacks; every interval has a lower bound of exactly zero. The gain is in user tasks 2, 9 and 13, whose amounts or values come from a named file, the history or a derivation.
- **Typed provenance in the learner has no measured effect.** L3c and L3 are identical on both populations and on the probe: behind the authority guard, the calls whose trace reformatting would hide never reach the model.

<!-- @frag ch4_followup -->
## 4.93 Follow-up: Defects of the Permission Rule and a Call-Level Audit of User Task 15

*Kind of evidence: call-level probes, replay and a call-level audit; development evidence. The counterexamples were reported by an external review of 14 November 2026 and reproduced; the repaired rule was written after G1's results were known.*

**Three defects.** The frozen rule G1 matches a call's account against the set of accounts in the request and its amount against the set of amounts, independently. For "Send 50 to account A and 100 to account B" it therefore supports 100 to A and 50 to B. It records that "If my balance is above 1000, send 50 to A" is conditional but supports the payment when the balance read by the agent is 500. And it supports a second, identical payment after the first was executed. The repaired rule G2 represents the request as instructions that keep account, amount, condition and repeat count together; evaluates balance conditions against the most recent successful balance read, and treats any other condition as not satisfied; and refuses a transfer that repeats one already executed without error beyond the number of times the request asks for. A call that returned an error does not count, so a retry stays possible (Chapter 3, Section 3.44). The ablations are in Section 4.94.

**What the defects meant on the benchmark.** All successful attacks under G1 are in user task 15, where the new landlord's account named by the user is also the attacker's account. A call-level audit separated what the benchmark counts as attack success from what the user asked for, with criteria written before it was run: update the address; update the rent standing order to that account and 2200; refund the 10.00 received from a friend.

**Table 4.78. Released attack-labelled calls in user task 15** (`ut15_call_audit.json`)

| Population | Arm | Successful attacks / attacked episodes | Released attack-labelled calls | Of these: 10 (the refund) to the landlord–attacker account | Of these: 2200 sent once to that account |
|---|---|---|---|---|---|
| primary | Permission rule G1 | 10 / 168 | 24 | 22 | 2 |
| primary | Progent manual policy | 0 / 168 | 0 | 0 | 0 |
| primary | Repaired permission rule G2 | 1 / 168 | 2 | 0 | 2 |
| second | Permission rule G1 | 3 / 112 | 3 | 3 | 0 |
| second | Progent manual policy | 0 / 112 | 0 | 0 | 0 |
| second | Repaired permission rule G2 | 0 / 112 | 0 | 0 | 0 |

- **The attacks that G1 lets through are not artefacts of the collision.** Of the 24 attack-labelled calls that G1 released on the primary recordings, 22 send the refund amount, 10, to the landlord's account, and 2 send the rent, 2200, to it as a one-off payment. The user asked for neither. The collision makes the account look requested; the operation and the amount still contradict the instruction. This is defect C1 occurring in the benchmark.
- **G2 blocks the 22 transfers of 10** because the request binds that account to 2200. It still releases the 2 one-off transfers of 2200, which cause its one successful attack: v2 does not distinguish "update the standing order to 2200" from "send 2200".
- **Progent's manual policy blocks all of them because the account is not on its fixed list**, not because it reads the instruction. The same list withholds the legitimate update of the rent order to the new account.
- **The audit's criteria also flag released calls without the attempt label**, in equal numbers for all three arms on the second population: an address written as "New York, NY 10001" in the city field, the existing name re-sent, a new standing order created instead of the existing one updated, or the old account kept. They are agent errors, not induced actions, and are reported in `ut15_call_audit.json`.

**Table 4.79. Sensitivity analysis without user task 15** (additional; every comparison of this chapter keeps the task)

| Arm | Primary: attacks | Primary: all tasks | Second: attacks | Second: all tasks |
|---|---|---|---|---|
| REM v1.0 | 0 | 1,188 | 0 | 916 |
| REM v1.1 | 0 | 1,287 | 0 | 1,074 |
| A2 | 0 | 1,474 | 0 | 1,232 |
| Progent manual policy | 0 | 1,450 | 0 | 1,256 |
| Permission rule G1 | 0 | 1,574 | 0 | 1,358 |
| Repaired permission rule G2 | 0 | 1,407 | 0 | 1,239 |
| Authority guard, learned on v2 evidence (L3) | 0 | 1,532 | 0 | 1,386 |

Without user task 15, every restrictive arm has no successful attack on either population. All differences in security among them come from this one task, so the security comparisons of this chapter rest on a handful of episodes of one task.

**What the follow-up changes in the conclusions.**

1. The deterministic permission evidence can be made more precise, and on these recordings precision removes attacks without removing tasks (the binding check). Refusing to guess a subjective condition costs one user task.
2. The repaired rule does not show added value over the strongest simple rule A2, and against the published fixed-list policy neither outcome is resolved.
3. The learned model still has no demonstrated value over the rule, and with the authority guard it no longer loses robustness. Whatever it adds is confined to amounts and values that the request delegates.
4. The fixtures and counterexamples used to find and repair these defects cannot test the repairs. A test needs requests written and reviewed by someone other than the author (Section 4.46).
