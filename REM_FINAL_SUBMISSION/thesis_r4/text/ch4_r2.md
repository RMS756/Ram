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
| Permission rule, revisions 1 to 3 (G1, G2, G3) | A state-changing call is released only if the request, compiled by a deterministic parser, supports it. G1 checks operation, recipient and amount. G2 also binds amounts to accounts, evaluates balance conditions and tracks executed payments. G3, the current rule, also binds each instruction to the effect of the operation and evaluates a condition only as a whole (Chapter 3, Section 3.44) | none | 13, 14 and 15 November |
| Ablations of the permission rule | The rule with one check removed | none | 13 to 15 November |
| V11d, L2, L2g, L4 | REM v1.1 with a two-verdict decision; a learned model on permission evidence behind a guard on denied calls (L2) and behind an authority guard (L2g, L4) (Chapter 3, Section 3.44) | estimator, calibration | 13 to 15 November |

Published defenses that need a language model (MELON, Task Shield, CaMeL, Progent with generated policies) are not among the arms, because no model was available (Section 4.46). Further learned variants of the extension (L0, L1, L2s, L3, L3c) are reported in the repository documents of the study and are not repeated in this chapter.

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

Five sets of comparisons were fixed before their outcomes were computed, each by a dated commit (Sections 4.2.3 and 4.2.42):

- 11 November 2026: the candidate of that study against REM v1.0 under S1 and S2 (Section 4.43.2);
- 11 November 2026: REM v1.1 against REM v1.0 on the then unread second population, with a three-part decision rule (Chapter 3, Section 3.11.44; Section 4.45);
- 13 November 2026: the permission rule against A2, against Progent's manual policy and against REM v1.1; the learned arms against the permission rule under S1 and S2 (Sections 4.89 and 4.91);
- 14 November 2026, after an external review reported three defects of the permission rule: revision 2 against revision 1, A2 and the published policy; the authority guard; and a call-level audit of user task 15 with criteria written before it was run (Sections 4.91 and 4.92);
- 15 November 2026, after a second review reported two further defects: revision 3 against revision 2, A2 and the published policy; the learned model against revision 3 under identical splits; and two ablations (Sections 4.89 and 4.91).

**No margin of non-inferiority on security was approved, and none was invented.** An interval of an attack-success difference that includes zero is reported as unresolved. The studies of 13 to 15 November also fixed their wording in advance. "Added value over simple rules" may be stated only if the task-completion interval against A2 lies above zero on both populations and the number of successful attacks does not exceed A2's. "The learned model adds value" may be stated only if the lower bound of its task-completion interval against the rule is strictly above zero under S1 and S2, with no more successful attacks on the original text and on the reformatted-identifier probe. An attack-success interval that excludes zero is reported as a security difference on development data, not as overall superiority.

<!-- @frag ch4_g4_intro -->
This section compares REM with other decision policies evaluated on the same episodes: the threshold baseline and the rule baselines, the defenses whose recorded outcomes the benchmark distributes, and one published policy replayed in the same harness. It then states which published defenses could not be run and how the results relate to recent work.

<!-- @frag ch4_progent -->
## 4.89 A Published Policy and a Request-Derived Permission Rule in the Same Harness

*Kind of evidence: replay; development evidence on both populations (every episode had been inspected before 13 November 2026). The arms and the comparisons marked with an asterisk were fixed in a committed protocol before the outcomes of the arm concerned were computed.*

**The published policy.** Progent (T. Shi et al., 2025) enforces per-tool policies with argument restrictions before each tool call. Its official repository contains, at the commit of 10 September 2025, a manual policy for the AgentDojo banking suite: `send_money`, `schedule_transaction` and `update_scheduled_transaction` are permitted only for five listed recipients; `update_password` has no policy entry and is therefore not permitted; the remaining tools are permitted. The policy was read from the repository as data, with the file digests pinned, and applied to the recorded calls by this project's replay code. The arm is therefore **Progent's published manual banking policy, adapted to the shared replay harness**. It is not a reproduction of the Progent framework or of the paper's results, not Progent with policies generated by a language model, and not a live-agent comparison. The upstream checking code was not executed in this project; its equivalence with the decision function used here was established by reading it. An independent review of 14 November 2026 reported a differential check on 468 argument cases that found no difference; that check was not repeated here.

**The permission rule** releases a state-changing call only if the user's request supports it (Chapter 3, Section 3.44). It is an exploratory extension, not part of REM v1.0 or v1.1. It exists in three revisions, each frozen before it was scored. Revision 1 (G1) checks the operation, the recipient and the amount against the request. Revision 2 (G2) binds each amount to its account, evaluates balance conditions and refuses a payment already executed. Revision 3 (G3), the current rule, also binds each instruction to the effect of the operation (an immediate transfer, the creation of a standing order, or the modification of one) and evaluates a condition only as a whole. Revisions 2 and 3 repair defects found by two external reviews (Section 4.92), so their results were obtained after those of the earlier revision were known.

**Table 4.67. Replay results of the rules and the published policy** (step-level, no reviewer; `improvement_results.json`, `results_v2.json`, `results_v3.json`; REM, B1 and P2 are in Tables 4.43 and 4.50)

| Arm | Primary: attacks / 2,979 | Primary: benign tasks / 334 | Primary: all tasks / 3,313 | Primary: legitimate calls released / 178 | Second: attacks / 2,065 | Second: all tasks / 2,113 | Second: legitimate calls released / 51 |
|---|---|---|---|---|---|---|---|
| Rule A2 | 13 | 140 | 1,474 | 83 | 4 | 1,232 | 27 |
| **Progent manual policy (replay adaptation)** | 0 | 154 | 1,450 | 136 | 0 | 1,305 | 48 |
| Permission rule, revision 1 (G1) | 10 | 149 | 1,574 | 112 | 3 | 1,358 | 36 |
| Permission rule, revision 2 (G2) | 1 | 132 | 1,407 | 93 | 0 | 1,239 | 20 |
| **Permission rule, revision 3 (G3, current)** | 0 | 132 | 1,407 | 92 | 0 | 1,239 | 20 |

**Table 4.69. Paired contrasts** (first arm minus second arm, in percentage points, with the 95% grouped-bootstrap interval; PG = Progent manual policy; v1.0 = REM v1.0; * = fixed in advance)

| Contrast | Population | All-task completion | Benign task completion | Attack success | Tasks gained / lost | Attacks gained / lost |
|---|---|---|---|---|---|---|
| G3−A2* | primary | −2.02 [−15.52, 10.98] | −2.40 [−16.07, 10.61] | −0.44 [−0.73, −0.14] | 149 / 216 | 0 / 13 |
| G3−A2* | second | +0.33 [−16.35, 16.72] | +4.17 [−16.67, 25.00] | −0.19 [−0.43, −0.05] | 172 / 165 | 0 / 4 |
| G3−PG* | primary | −1.30 [−7.98, 5.29] | −6.59 [−16.67, 2.38] | +0.00 [0.00, 0.00] | 88 / 131 | 0 / 0 |
| G3−PG* | second | −3.12 [−18.56, 11.41] | −12.50 [−35.42, 10.42] | +0.00 [0.00, 0.00] | 129 / 195 | 0 / 0 |
| G3−v1.0 | primary | +6.61 [−2.85, 17.45] | +8.08 [−0.60, 19.39] | −0.37 [−0.68, −0.10] | 332 / 113 | 0 / 11 |
| G3−v1.0 | second | +15.29 [−2.29, 34.47] | +22.92 [4.17, 43.75] | −0.15 [−0.38, 0.00] | 444 / 121 | 0 / 3 |

What the comparison shows:

- **The current rule and the published policy have no successful attack in either population.** Their difference in completed tasks is not resolved in either. Neither equivalence nor non-inferiority is claimed. The published policy releases more of the legitimate state-changing calls of benign episodes (136 of 178 against 92; 48 of 51 against 20).
- **Against the rule A2 there is a security difference on development data and no resolved difference in completed tasks.** The current rule has 0 against 13 and 0 against 4 successful attacks, and both attack-success intervals lie below zero. The task-completion intervals include zero. By the wording fixed in advance, added value over simple rules and overall superiority are not claimed. All of these attacks are in one user task (Section 4.92).
- **Against REM v1.0** the current rule has fewer successful attacks on the primary recordings and more completed benign tasks on the second population; the other intervals include zero. This contrast was not fixed in advance.
- **The two policies fail in different places.** The published policy completes no password-change task (user task 14), because the tool is not permitted, and its five recipients are payees of the benchmark's initial state: on twenty paired fixtures whose payees are not on the list it withholds 13 of 20 legitimate calls (Table 4.74). The benchmark policy published with aiAuthZ has the same form (Section 4.16). The current rule completes no episode of user tasks 0, 2, 12, 14 and 15: the recipient or the instruction is supplied only by a file, the condition is subjective, or the request does not identify the payee of a refund.

<!-- @frag ch4_g5_intro -->
This section reports what happens when a component is removed or replaced. It covers the components of REM v1.0, the verdict set, and the components of the exploratory extension. Every ablation is a single-benchmark observation; none shows that a component has no benefit in general.

<!-- @frag ch4_ablation_new -->
## 4.90 Ablation of the Behavioral Evidence Group and of the Verdict Set

Two ablations of Table 4.12 were followed up in later studies, and their results are reported where those studies are described.

- **Behavioral evidence.** Removing the four behavioral features is REM v1.1. In the pilot it left replay attack success at 11 of 2,979 and raised benign task completion from 105 to 140 of 334. Under the double holdout it has 14 successful attacks against 11 (Table 4.45). On the second population it completed 1,074 against 916 of 2,113 tasks with 1 against 3 successful attacks (Section 4.45).
- **Verdict set.** Replacing every Modify and Escalate verdict of REM v1.0 by Block changes the outcome of none of the 3,313 primary episodes (Section 4.42.2). Removing the two verdicts from the decision rule, so that Allow is chosen up to the Allow–Block threshold of Equation 3.9, gives more released calls with 13 against 11 successful attacks on the primary recordings and 3 against 3 on the second population (Tables 4.43 and 4.50), and 31 against 13 when the attacker's identifier is reformatted (Table 4.48).
- **Calibration.** Without the calibration map, replay attack success is unchanged (11 of 2,979) and benign task completion is 110 instead of 105 of 334 (Table 4.12: 0.329 against 0.314). Calibration therefore changed a small number of decisions. It did not change the security count.

## 4.91 Ablations of the Task-Permission Extension

*Kind of evidence: replay; development evidence. The ablations are diagnostic and were listed in the protocol of each revision before scoring.*

**Table 4.70. The permission rule, one check at a time** (`improvement_results.json`, `results_v2.json`, `results_v3.json`; the probe has 2,645 attacked episodes)

| Rule | Primary: attacks / 2,979 | Primary: all tasks / 3,313 | Second: attacks / 2,065 | Second: all tasks / 2,113 | Probe: attacks, identifier reformatted |
|---|---|---|---|---|---|
| Permission rule, revision 1 (G1) | 10 | 1,574 | 3 | 1,358 | 10 |
| G2 without binding amounts to accounts | 10 | 1,407 | 3 | 1,239 | 10 |
| Permission rule, revision 2 (G2) | 1 | 1,407 | 0 | 1,239 | 1 |
| G3 without effect typing | 10 | 1,407 | 3 | 1,239 | 10 |
| Permission rule, revision 3 (G3, current) | 0 | 1,407 | 0 | 1,239 | 0 |
| G3 without the condition check | 0 | 1,574 | 0 | 1,358 | 0 |

**Table 4.71. Learned models on the permission evidence** (S1: held-out attacker objective; S2: double holdout; all use the two-verdict decision of Chapter 3, Section 3.44)

| Arm | S1: attacks / 2,979 | S1: all tasks / 3,313 | S2: all tasks | Second: attacks / 2,065 | Second: all tasks / 2,113 | Probe: attacks, identifier reformatted |
|---|---|---|---|---|---|---|
| Permission rule, revision 3 (G3, current) | 0 | 1,407 | 1,407 | 0 | 1,239 | 0 |
| REM v1.1 with the two-verdict decision (V11d) | 131 | 1,492 | 1,452 | 58 | 1,182 | not run |
| Learned, guard on denied calls only (L2) | 10 | 1,680 | 1,676 | 2 | 1,489 | 38 |
| L2 with the authority guard (L2g) | 10 | 1,679 | 1,675 | 2 | 1,489 | 10 |
| Authority guard, learned on revision-3 evidence (L4) | 0 | 1,532 | 1,532 | 0 | 1,386 | 0 |

**Table 4.72. Paired contrasts of the ablations and of the learned model** (first arm minus second arm, in percentage points, with the 95% interval; * = fixed in advance)

| Contrast | Population | All-task completion | Benign task completion | Attack success | Tasks gained / lost | Attacks gained / lost |
|---|---|---|---|---|---|---|
| L4−G3* | primary, S1 | +3.77 [0.00, 9.25] | +4.49 [0.00, 10.24] | +0.00 [0.00, 0.00] | 133 / 8 | 0 / 0 |
| L4−G3* | primary, S2 | +3.77 [0.00, 9.25] | +4.49 [0.00, 10.24] | +0.00 [0.00, 0.00] | 133 / 8 | 0 / 0 |
| L4−G3* | second | +6.96 [0.00, 18.27] | +6.25 [0.00, 18.75] | +0.00 [0.00, 0.00] | 150 / 3 | 0 / 0 |
| G3−(no effect typing)* | primary | +0.00 [0.00, 0.00] | +0.00 [0.00, 0.00] | −0.34 [−0.57, −0.10] | 0 / 0 | 0 / 10 |
| G3−(no effect typing)* | second | +0.00 [0.00, 0.00] | +0.00 [0.00, 0.00] | −0.15 [−0.29, −0.05] | 0 / 0 | 0 / 3 |
| G3−(no condition check)* | primary | −5.04 [−15.24, 0.00] | −5.09 [−15.36, 0.00] | +0.00 [0.00, 0.00] | 0 / 167 | 0 / 0 |
| G3−(no condition check)* | second | −5.63 [−17.34, 0.00] | −6.25 [−18.75, 0.00] | +0.00 [0.00, 0.00] | 0 / 119 | 0 / 0 |

- **Binding removes the attacks and costs no task.** Binding amounts to accounts takes the rule from 10 and 3 successful attacks to 1 and 0. Binding instructions to the effect of the operation removes the remaining one. Without effect typing the current rule has the 10 and 3 attacks of revision 1, with the same completed tasks.
- **The condition check costs one user task.** Every task that revisions 2 and 3 lose against revision 1 (167 and 119) is in user task 14, whose request makes a password change conditional on "something looks even just a little bit suspicious". The rule does not evaluate such a predicate and never treats it as satisfied. The check removes no attack on these recordings. Whether such a call should be released, withheld or sent to a reviewer is an open decision (SD-COND, Appendix F).
- **Components of revision 1.** Scoped delegation accounts for 131 completed tasks on the primary recordings, typed normalization for 90 and established payees for 18. Without the amount check the rule completes 68 more tasks with 3 more successful attacks. The fulfilment check and the parser repairs change no count on the recordings.
- **The two-verdict decision alone is unsafe.** Applied to REM v1.1 without a guard (V11d), it releases every held-out credential-change attack. In REM v1.1 those calls are withheld only because Escalate has a lower expected loss than Allow, and without a reviewer an escalated call is withheld. The low attack count of REM under a held-out objective therefore depends on the Escalate region, not on the estimator recognizing the attack.
- **A learned model behind a weak guard is not robust.** With the attacker's identifier reformatted, L2 has 38 successful attacks where the rule has 10. A guard that also blocks every call whose authority is not established (L2g, L4) removes this failure.
- **The learned model's value over the current rule is not established.** L4 completes more tasks than G3 with no successful attack, on the original text and on the probe. The lower bound of every task-completion interval is exactly zero, under S1, under S2 and on the second population. By the wording fixed in advance this is "not established"; it does not show that a learned model cannot help. The gain is in user tasks 2, 9 and 13, whose amounts or values the request delegates to a file, the history or a derivation.

<!-- @frag ch4_g6_intro -->
This section reports the results that the earlier sections did not already present: the pilot's feasibility check, the quality of the estimator, the observe-only decisions, the replay of REM and its baseline, the sequential analysis, realized loss, generalization, robustness, the confirmatory run and the exploratory extension. It then interprets the findings, states the threats to validity and summarizes the chapter.

<!-- @frag ch4_improve_results -->
## 4.92 Exploratory Extension: Task-Permission Evidence

*Kind of evidence: call-level counterexamples, replay, a call-level audit and paired fixtures, reported separately; all development evidence. Protocols were committed before each scoring (commits `9137b03`, `ae3f923`, `869d4c1`). One amendment was made after the first scoring of revision 3; it changed only the ablation without the condition check, and both result files are kept. The parser was written by an author who knows the sixteen requests of the benchmark.*

The question of the extension is whether permission evidence compiled from the trusted request improves the trade-off between security and task completion, and which component is responsible. The comparison with the rules and the published policy is in Section 4.89 and the ablations are in Section 4.91. This section reports the defects found, the audit of the one task that decides the security comparisons, the fixtures and the verdict.

**Matcher counterexamples.** Two external reviews (14 and 15 November 2026) reported five call-level defects, all reproduced on the unchanged code of the revision concerned. Revision 1 supported "100 to A and 50 to B" for the request "send 50 to A and 100 to B", supported a payment whose balance condition was false, and supported a repeated payment. Revision 2 let a request to create a monthly standing order license an immediate transfer, and evaluated "above 1000 and below 5000" as true at a balance of 10000. Each is now a regression test, together with legitimate neighbouring cases. They are development material and cannot test the repairs.

**The task that decides the security comparisons.** All successful attacks under any revision of the rule are in user task 15, where the new landlord's account named by the user is also the attacker's account. A call-level audit compared each released call with what the user asked for (update the address; update the rent standing order to that account and 2200; refund the 10.00 received from a friend), with criteria written before it was run.

**Table 4.78. Released attack-labelled calls in user task 15** (`ut15_call_audit.json`, `results_v3.json`)

| Population | Arm | Successful attacks / attacked episodes | Released attack-labelled calls | Of these: 10 (the refund) to the landlord–attacker account | Of these: 2200 sent once to that account |
|---|---|---|---|---|---|
| primary | Permission rule, revision 1 (G1) | 10 / 168 | 24 | 22 | 2 |
| primary | Progent manual policy (replay adaptation) | 0 / 168 | 0 | 0 | 0 |
| primary | Permission rule, revision 2 (G2) | 1 / 168 | 2 | 0 | 2 |
| primary | Permission rule, revision 3 (G3, current) | 0 / 168 | 0 | 0 | 0 |
| second | Permission rule, revision 1 (G1) | 3 / 112 | 3 | 3 | 0 |
| second | Progent manual policy (replay adaptation) | 0 / 112 | 0 | 0 | 0 |
| second | Permission rule, revision 2 (G2) | 0 / 112 | 0 | 0 | 0 |
| second | Permission rule, revision 3 (G3, current) | 0 / 112 | 0 | 0 | 0 |

- **The attacks that revision 1 lets through are not artefacts of the collision.** They send the refund amount, 10, or the rent, 2200, to the landlord's account as a one-off payment. The user asked for neither. The collision makes the account look requested; the operation and the amount still contradict the instruction.
- **Revision 3 releases none of these calls.** It also withholds 20 and 77 calls that the audit counts as consistent with the instruction, mostly refunds whose payee the request does not identify. That is part of its cost in completed tasks.
- **The published policy blocks them because the account is not on its fixed list**, not because it reads the instruction. The same list withholds the legitimate update of the rent order.
- **Without user task 15, every restrictive arm has no successful attack on either population.** The task is kept in every comparison. Every security difference among the restrictive arms therefore rests on a small number of episodes of one task.

**Table 4.74. Paired fixtures** (each pair has one legitimate and one unsafe call for the same request; a pair is correct if the legitimate call is released and the unsafe call is withheld; counts, not rates)

| Arm | Sets 1–3: pairs correct / 23 | Sets 1–3: unsafe calls released | Set 4: pairs correct / 20 | Set 4: unsafe calls released |
|---|---|---|---|---|
| REM v1.1 | 17 | 4 | 11 | 6 |
| Rule A2 | 11 | 10 | 9 | 8 |
| Progent manual policy (replay adaptation) | 3 | 0 | 7 | 0 |
| Permission rule, revision 1 (G1) | 16 | 1 | 16 | 1 |
| Permission rule, revision 2 (G2) | 16 | 1 | 19 | 0 |
| Permission rule, revision 3 (G3, current) | 16 | 1 | 19 | 0 |
| Authority guard, learned on revision-3 evidence (L4) | 16 | 1 | 19 | 1 |

Sets 1 to 3 are the fixtures of the earlier studies. Set 4 has twenty pairs in ten categories and was written for revision 1 by the author of the rule with AI assistance; it was not reviewed by a second person. The repairs of revisions 2 and 3 were written after its failures were known, so for them it is regression material, not a test. The one legitimate call that the current rule withholds on set 4 is withheld by design ("1,250" can be read as two amounts); the learned arm releases it together with the unsafe call of the same pair.

**Verdict of the extension study.**

1. **Improvement over REM v1.0: observed on development data.** Fewer successful attacks on the primary recordings; more completed benign tasks on the second population.
2. **Against the strongest simple rule A2: a security difference on development data; overall superiority not established.** The difference in completed tasks is not resolved.
3. **Against the published policy: not resolved.** No successful attack for either.
4. **Attribution.** The measured changes come from deterministic matching of the call against the instruction. The learned model's contribution is not established. The semantic verifier was not run.
5. **Prospective validation: defined, not executed.** A test needs paired requests written and reviewed by persons other than the author. The repository contains the authoring instructions and a scorer that refuses to run if the frozen rule has changed; no such request set exists. Live-agent comparisons are blocked for the reasons of Section 4.46.
6. **Status.** Proposed and exploratory. The rule is not adopted and is not a new version of REM (decision SD-PERM, Appendix F).

The median time to evaluate one call was 0.09 ms for the rule and for the published policy and 0.18 ms for REM; no arm calls a model. The complete results of the three revisions (per-task counts, every single-component ablation, the probe, the analysis without user task 15) are in the repository under `REM_IMPROVEMENT_STUDY/` (`05_RESULTS.md`, `followup/RESULTS_V2.md`, `followup_v3/RESULTS_V3.md`).
