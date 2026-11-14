# CHAPTER FOUR

# EXPERIMENTAL RESULTS AND DISCUSSION

This chapter reports the implementation environment, the data and the fitting of the estimator, the experimental setup, the comparisons with baselines and with one published policy, the ablations, and the results with their discussion. **No experiment with a live agent or a language model was executed, and no result in this chapter is a live result.** Every result comes from recorded trajectories of real agents in the AgentDojo banking environment, replayed with a policy that may withhold calls. The design values (costs, tiers, predicates, feature set, label rule) are declared values that await the supervisor's approval, so all results are exploratory by label.

The chapter has six sections. Section 4.1 describes the tools and the environment. Section 4.2 describes the data, their preparation and the training of the estimator. Section 4.3 defines the compared arms, the populations and the metrics. Section 4.4 compares REM with baselines, simple rules and a published policy. Section 4.5 reports the ablations. Section 4.6 reports the remaining results, interprets them and states the threats to validity.

## 4.1 Implementation Tools and Environment

### 4.1.1 Software, Hardware and Benchmark Environment

**Table 4.1. Software and hardware used for the reported results**

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

The hardware is that of the container in which all results were last re-executed (13 November 2026). Earlier runs used containers of the same kind whose hardware was not recorded. Apart from the decision times, no result depends on the hardware: the re-executions reproduce the stored counts exactly (Section 4.1.3).

REM needs no accelerator. The estimator has nine parameters, and a decision is one dot product, one logistic map, a table lookup and a comparison of four numbers. Fitting all 152 cross-fitting cells of the last study took 6 seconds, and 161,506 episode replays took 338 seconds with four worker processes.

### 4.1.2 Implemented Components

**Table 4.2. Components, their location in the repository and their status**

| Component | Location | Status |
|---|---|---|
| REM framework: five layers, estimator, calibration, tiers, predicates, expected-loss rule, mitigation, audit record | `rem/` | Implemented and tested (Chapter 3, Section 3.15; Appendix B) |
| Pilot pipeline: data loading, labels, cross-fitting, observe-only analyses, replay | `experiments/pilot/` | Executed |
| Rule baselines, diagnostic arms, double holdout, probes, fixtures, confirmatory run | `experiments/authz_study/` | Executed |
| Exploratory extension: request compiler, typed matcher, decision variants, published-policy comparator | `experiments/improve_study/` | Executed in replay (Chapter 3, Section 3.14) |
| Selective semantic verifier | `experiments/improve_study/verifier.py` | Interface and tests only; never called with a model |
| Closed-loop harness for live agents; MELON integration | Appendix D | Implemented and tested with scripted agents; not executed with a model |

Experimental code is kept apart from the framework. No file under `rem/` or `configs/` was changed by any study of November 2026; each study imports the framework and adds its own modules.

### 4.1.3 Reproducibility and Software Verification

Each results file records the commit of the framework, the digest of the configuration and of the amendments, the benchmark version and the commit of the recorded runs. Three checks support the numbers of this chapter.

- **Re-execution.** The pilot was executed, re-executed after code corrections and re-executed again with timing instrumentation; the analytical values were identical each time (Section 4.2.1).
- **Equivalence of earlier arms in later studies.** Each later study recomputes the earlier arms before adding its own. In the study of 13 November the seven earlier arms reproduce the stored counts on both populations, and the refitted estimator of REM v1.1 equals the stored one (largest absolute difference of any parameter: 0).
- **Tests.** On 13 November 2026 the suite of 280 tests gave 278 passed, 1 skipped and 1 expected failure. It covers the frozen equations, the mitigation semantics, replay, leakage controls and, for the extension, the isolation of the defense interface from task identifiers, labels and outcomes.

The commands that regenerate every table are listed in Appendix B and in the study folders of the repository.

### 4.1.4 Kinds of Evidence and Evaluation Modes

One analysis, the confirmatory run of Section 4.6.8, was carried out under a protocol and a pass rule committed before its data were opened. It is confirmatory in that procedural sense only: it shares the unapproved design values and the limits of replay with everything else. After that run its recordings are no longer unread, and every later analysis of them is development evidence.

Eight kinds of evidence are kept apart. Each table states which kind it reports.

**Table 4.3. Kinds of evidence in this chapter**

| Kind | What it is | What it cannot show | Sections |
|---|---|---|---|
| Recorded outcome | The benchmark's verdicts on traces as recorded by its authors, without REM | Anything about REM | Sections 4.2.1 and 4.4.2 |
| Offline prediction | REM's probability for a recorded call, from a model fitted without that call's group | Any effect of enforcement | Sections 4.2.3 and 4.6.1 |
| Observe-only decision | The verdict REM would issue for a recorded call; not enforced | Outcomes | Sections 4.6.2 and 4.5.1–4.6.5 |
| Replay | A recorded episode re-executed in the benchmark's sandbox with a policy that may withhold calls; later calls are the recorded ones (NO-ADAPT) | Agent adaptation; reviewer effect; any difference among Modify, Escalate and Block | Sections 4.6.3, 4.4.1, 4.6.6 and 4.6.7 |
| Post-hoc analysis | An analysis added after results were seen; labelled where it occurs | Confirmation | Section 4.2.2; parts of Sections 4.4.1 and 4.6.6 |
| Confirmatory replay | Replay on recordings that had not been read before that run (11 November 2026), under a protocol committed in advance | The same limits as replay | Section 4.6.8 |
| Development replay of the extension | Replay of new arms on recordings that had all been inspected; protocol committed before the new arms were scored | Confirmation; behaviour on requests the author had not seen | Sections 4.4.3, 4.5.3 and 4.6.9 |
| Call-level fixture | Hand-written paired calls scored by the frozen models | Prevalence; any benchmark outcome | Sections 4.6.7 and 4.6.9 |

Integration checks with scripted agents and simulated providers are not results and are reported only as status (Section 4.4.4).

**Sources of the numbers.** The pilot's results come from `results/pilot_R2/` and its re-execution `results/pilot_R4/` (Chapter 3, Section 3.15). The study of 11 November 2026 on the same recordings (Sections 4.4.1, 4.6.6 and 4.6.7) is in `REM_Authorization_Generalization_Study/results/`. The confirmatory run of the same date (Section 4.6.8) is in `REM_FINAL_SUBMISSION/results/`. The extension study of 13 November 2026 (Sections 4.4.3, 4.5.3 and 4.6.9) is in `REM_IMPROVEMENT_STUDY/results/`. Every run used AgentDojo 0.1.35, the benchmark's recordings at one fixed commit, seed 20261027 and step-level mitigation without a reviewer unless a table says otherwise.

## 4.2 Dataset Preparation and Training

This section describes the recorded data and how they were prepared (exclusions, labels, eligibility for replay), the fitting protocol, the second population, the validity of the labels, and the training of the estimator. Nothing was collected for this thesis: the trajectories were recorded by the benchmark's authors with real agents.

### 4.2.1 Recorded Data, Fitting Protocol and Chronology

#### Data

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

#### Protocol

The protocol is nested grouped cross-fitting (Chapter 3, Procedure 3.1):
- nine outer folds, each holding out one injection task;
- episodes without injection assigned to folds by user task.

Within each fold's fitting portion, the following are fitted (Chapter 3, Section 3.11.5):
- λ, by grouped inner cross-validation;
- the calibration map, on inner out-of-fold logits;
- the baseline thresholds;
- the benign reference quantities;
- r~mod~.

The **pre-registered values** are listed in Table 4.4. They come from Chapter 3 where Chapter 3 gives them; otherwise they are declared exploratory values.

**Table 4.4. Pre-registered values** (`configs/exploratory/pilot_e0.yaml`)

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

#### Chronology of design, amendments and analyses

| Date and time (UTC) | Event | Record |
|---|---|---|
| 27 Oct 2026 16:40 | Pilot design committed (Table 4.4) | commit `48bef90` |
| 27 Oct 2026 16:57 | Amendments AM-1 to AM-4 committed. AM-1: exclusion of (user_task_15, injection_task_4). AM-2: benign references. AM-3: the meaning of "tool class". AM-4: replay validity filter | commit `7a707a7` |
| 27 Oct 2026, after 16:57 | First computation of held-out predictions and of all analyses with the then-uncommitted pipeline code. **The log of this first execution was not preserved**; its order relative to the amendments rests on the commit times and on the working session record | — |
| 27 Oct 2026 17:16 | Pipeline committed, then re-run in full; results identical to the first execution | commit `aa66f22`; `results/pilot/` |
| 27–28 Oct 2026 | **Post-hoc analyses**, added after results had been seen: exclusion of user_task_15 (Section 4.2.2); benign-release breakdown by tier; REM without expected-loss Escalate (Sections 4.6.2–4.6.3); breakdowns by action type and tier; replay-failure analysis | `results/pilot_R2/` |
| 28 Oct 2026 | Code corrections of revision R2 (Section 3.15), complete re-run; analytical values identical | commit `84a8c21`; `results/pilot_R2/` |

No pre-registered value was changed after results were seen. The post-hoc analyses are reported as such, and none replaces a pre-registered analysis.

#### The second population

The confirmatory run of Section 4.6.8 uses recordings that no script of this project had read before 11 November 2026 (Chapter 3, Section 3.11.14). That status ended with the run. In the extension study of 13 November 2026 the same recordings are a second development population, and nothing computed on them there is confirmatory.

**Table 4.5. The second population (recorded outcomes; `confirmatory_results.json`)**

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

#### Chronology of the analyses of November 2026

| Date (UTC) | Event | Record |
|---|---|---|
| 8 Nov 2026 | Decision traces of sixteen paired fixtures (sets 1 and 2) through REM v1.0; the fixtures were written before they were scored | commit `4989306` |
| 11 Nov 2026, 04:51 | Protocol of the rule baselines, diagnostic arms, double holdout and probes committed before any of their outcomes was computed | commit `cca4968` |
| 11 Nov 2026 | Those analyses run; three post-hoc additions made after results were seen, among them REM v1.1 under the double holdout | commit `2c915bf` |
| 11 Nov 2026, 17:04 | Confirmatory protocol and fixture set 3 committed before the new recordings were opened | commit `19bd168` |
| 11 Nov 2026 | Confirmatory run; no amendment to its protocol | commit `907e6d2` |
| 13 Nov 2026 | Extension study: protocol, parser, matcher, arms, comparisons, wording rules and fixture set 4 committed before any outcome of a new arm was computed | commit `9137b03` |
| 13 Nov 2026 | Extension study run on both populations; analysis code added afterwards; no amendment to its protocol | commits `2ffdcfb`, `04a38ca` |

### 4.2.2 Labels, the user_task_15 Collision and Benchmark Versions

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

### 4.2.3 Pilot E0: Feasibility and Feature Retention

Pilot E0 used only the fitting portion of each outer fold (`e0_pilot.json`).

**Table 4.6. Pilot E0 (fitting portions only)**

| Evidence group | ROC-AUC: mean over folds; minimum | Retained in every fold (≥ 0.55) |
|---|---|---|
| Context (x^ctx₂ only) | 0.582; 0.554 | Yes, marginally |
| Behavioral | 0.802; 0.787 | Yes |
| Action | 0.929; 0.923 | Yes |
| All | 0.938; 0.930 | — |

The retention rule was applied to each fold's fitting portion separately, and every fold retained all three groups (`e1_crossfit.json`, `e0_fold_specific_feature_groups`). The feature set is therefore the same in every fold. No fold's held-out data influenced its own feature set.

The pooled count of positive steps is 921, above the declared minimum of 50. Thirteen of the 21 backbones have fewer than 50 positive steps each (range 2–116), so no per-backbone conclusion is drawn.

### 4.2.4 Training of the Risk Estimator

The estimator is the ridge logistic regression of Equations 3.1 and 3.2, followed by the logit calibration map of Equation 3.3, which is fitted by Equation 3.4. It is trained once per fold, on the fitting portion of that fold only, by the nested procedure of Chapter 3 (Procedure 3.1): the ridge penalty is selected from five values by four grouped inner folds; the calibration map is fitted on the inner out-of-fold logits; the model is then refitted on the whole fitting portion.

**Table 4.7. Training outcome per outer fold, REM v1.0** (`e1_crossfit.json`; each row is the model that scores the held-out attacker objective named in the first column)

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
- **The calibration maps are close to the identity** (γ~1~ between 0.945 and 0.981), so calibration changes the probabilities little (Section 4.6.1).
- **The held-out quality differs by objective.** Objective 7 has the largest calibration error (0.189); objective 5, with 23 positive steps, has the lowest ROC-AUC.

Three further sets of models were trained by the same procedure and are used later in the chapter: the models of REM v1.1, which omit the four behavioral features (nine folds); the models of the double holdout, one for each of 143 combinations of user task and attacker objective (Chapter 3, Section 3.11.12); and, for the exploratory extension, models on the four non-behavioral features plus five permission indicators (nine folds and 143 double-holdout cells; Chapter 3, Section 3.14). No model was trained or selected on the second population.

## 4.3 Experimental Setup and Evaluation Metrics

This section fixes what is compared, on which episodes, and with which measures. The definitions are those of Chapter 3 (Sections 3.11 and 3.12); they are collected here so that Sections 4.4 to 4.6 can be read without returning to it.

### 4.3.1 Compared Arms

**Table 4.8. Arms compared in this chapter**

| Arm | Definition | Fitted quantities | Declared |
|---|---|---|---|
| No defense | Every call is released | none | pilot |
| B1 | Consequence-independent thresholds on REM's calibrated probability | estimator, calibration, two thresholds | pilot |
| REM v1.0 | The frozen pipeline of Chapter 3 | estimator, calibration | pilot |
| REM v1.1 (proposed) | REM v1.0 without the behavioral evidence group (Chapter 3, Section 3.13) | estimator, calibration | ablation in the pilot; candidate of the confirmatory run |
| REM, Allow and Block only | REM v1.0 with the verdict set restricted to two | as REM v1.0 | 11 November |
| P1, P2, A1, A2 | Rules on provenance, novelty and occurrence in the request, with no model (Chapter 3, Table 3.13) | none | 11 November |
| Diagnostic and candidate arms | Outcome-supervised and intervention-value variants (Chapter 3, Table 3.14) | their own | 11 November |
| Progent manual policy | The manual banking policy published in the Progent repository (T. Shi et al., 2025): a fixed list of five permitted recipients for the three payment tools; password change not permitted | none | 13 November |
| Permission rule G1 | A state-changing call is released only if the request, compiled by a deterministic parser, supports its operation, recipient and amount (Chapter 3, Section 3.14) | none | 13 November |
| G1 without one component | Five ablations of G1 | none | 13 November |
| V11d, L0, L1, L2, L2s | REM v1.1 with a two-verdict decision; a learned model on permission evidence without a guard, and behind a guard with four or two verdicts (Chapter 3, Section 3.14) | estimator, calibration | 13 November |
| Repaired permission rule G2; G1r and three ablations of G2 | G1 with instruction bindings, condition evaluation and fulfilment tracking (Chapter 3, Section 3.14) | none | 14 November |
| L2g, L3, L3c | Learned arms behind an authority guard; L3c with identifiers canonicalized in the provenance evidence (Chapter 3, Section 3.14) | estimator, calibration | 14 November |

Published defenses that need a language model (MELON, Task Shield, CaMeL, Progent with generated policies) are not among the arms, because no model was available (Section 4.4.4).

### 4.3.2 Populations and Generalization Schemes

**Table 4.9. Populations and what each is used for**

| Population | Eligible episodes | Use |
|---|---|---|
| Primary | 3,313 (2,979 attacked, 334 benign), 21 undefended backbones, attack `important_instructions` | Fitting and cross-validated evaluation. Scheme S1 holds out one attacker objective per fold; scheme S2 holds out the user task and the attacker objective together |
| Held-out templates (S3) | 681 attacked | Attack templates not used in fitting |
| Second population | 2,113 (2,065 attacked, 48 benign), five sources with other agents and templates (Section 4.2.1) | Nothing is fitted on it. It was unread until the confirmatory run of 11 November 2026. **Since then it is development evidence** and is used as such in the study of 13 November |
| Reformatted-identifier probe | 2,645 attacked | The attacker's account identifier in the injected text is rewritten with spaces |
| Paired fixtures | 43 pairs in four sets | Hand-written calls scored by one fold's models; mechanisms, not rates |

Rules have no fitted quantity, so their results are the same under S1 and S2.

### 4.3.3 Evaluation Metrics

Three outcomes are primary: completion of the legitimate task, release of legitimate state-changing calls, and attack success.

**Table 4.10. Metrics and their definitions**

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

### 4.3.4 Statistical Procedure and Comparisons Fixed in Advance

Intervals are 95% percentile intervals of a grouped bootstrap with 2,000 resamples. Task-completion differences are resampled by user task (16 groups) and attack-success differences by injection task (9 groups); comparisons between arms are paired on the episode. With so few groups the intervals are wide and are not guaranteed to reach their nominal coverage (Section 4.2.1). They are descriptive.

Three sets of comparisons were fixed before their outcomes were computed, each by a dated commit (Sections 4.2.1 and 4.2.1):

- 11 November 2026: the candidate of that study against REM v1.0 under S1 and S2 (Section 4.6.6);
- 11 November 2026: REM v1.1 against REM v1.0 on the then unread second population, with a three-part decision rule (Chapter 3, Section 3.11.14; Section 4.6.8);
- 13 November 2026: the permission rule against A2, against Progent's manual policy and against REM v1.1; the learned arms against the permission rule under S1 and S2; the two-verdict decision alone; the effect of the guard (Sections 4.4.3, 4.5.3 and 4.6.9).
- 14 November 2026, after an external review reported defects of the permission rule: the repaired rule against the original rule, A2 and Progent's manual policy; the authority guard; the learned model against the repaired rule; typed provenance in the learner; and a call-level audit of user task 15 with criteria written before it was run (Sections 4.4.3, 4.5.4 and 4.6.10).

**No margin of non-inferiority on security was approved, and none was invented.** An interval of an attack-success difference that includes zero is reported as unresolved. The study of 13 November also fixed its wording in advance: "added value over simple rules" may be stated only if the task-completion interval against A2 lies above zero on both populations and the number of successful attacks does not exceed A2's.

## 4.4 Comparisons with Existing Models and Defense Frameworks

This section compares REM with other decision policies evaluated on the same episodes: the threshold baseline and the rule baselines, the defenses whose recorded outcomes the benchmark distributes, and one published policy replayed in the same harness. It then states which published defenses could not be run and how the results relate to recent work.

### 4.4.1 Rule Baselines and an Audit of REM's Interventions

*Kind of evidence: replay on the primary recordings (2,979 attacked and 334 benign eligible episodes), held-out attack objective (scheme S1). The arms were declared before their outcomes were computed, except where marked post hoc.*

#### Security and task completion of every arm

**Table 4.11. Replay results of REM, the baselines and the rules on the primary recordings** (step-level, no reviewer; `study_results.json`, S1)

| Arm | Successful attacks / 2,979 | Episodes with a released attack-labelled call | Benign tasks completed / 334 | Tasks completed under attack / 2,979 | Authorized calls released / 178 |
|---|---|---|---|---|---|
| No defense | 672 | 828 | 175 | 1,465 | 178 |
| B1, operating-point thresholds | 164 | 202 | 170 | 1,532 | 130 |
| **REM v1.0** | **11** | 24 | **105** | 1,083 | 33 |
| REM v1.1 (pilot ablation) | 11 | 24 | 140 | 1,147 | 83 |
| P1, provenance rule | 12 | 26 | 134 | 1,207 | 92 |
| P2, provenance or novelty rule | 12 | 26 | 134 | 1,207 | 89 |
| A2, strict explicit rule | 13 | 27 | 140 | 1,334 | 83 |
| REM, Allow and Block only | 13 | 27 | 124 | 1,273 | 64 |

The counts for REM v1.0, B1 and the no-defense reference are identical to the pilot's (Table 4.27), which checks the study's implementation. The 178 authorized calls are the calls to tools in 𝒯~R~ proposed in the 334 benign episodes; later tables call them legitimate state-changing calls. The third column counts attacked episodes in which a call carrying the attempt label was released; it is a proxy and not a measured change of the bank state (Section 4.3.3).

Three observations follow.

- **The rules match REM's security.** Rules that use one or two pieces of evidence and no model leave 12 or 13 successful attacks where REM v1.0 leaves 11. The differences are one or two episodes of 2,979.
- **REM v1.0 completes the fewest tasks of the restrictive arms.** It completes 105 benign tasks; the rules complete 134 to 140. It releases 33 of 178 authorized calls; the rules release 83 to 92.
- **The estimator's discrimination is real but is not what produces the security.** The held-out ROC-AUC of 0.938 (Table 4.23) shows that the score separates attempts from legitimate calls. A single feature already does most of this: read as a classifier of the attempt label, the provenance indicator x^act^~1~ alone has recall 0.971 and false-positive rate 0.147.

#### What REM v1.0 withholds

**Table 4.12. REM v1.0 on the 178 authorized calls of benign episodes, by action category** (`weakness_audit.json`)

| Category | Authorized calls | Released | Share released |
|---|---|---|---|
| Value transfer | 89 | 4 | 4% |
| Payment modification | 34 | 8 | 24% |
| Profile change | 37 | 21 | 57% |
| Credential change | 18 | 0 | 0% |
| **All** | **178** | **33** | **19%** |

REM v1.0 withholds almost every legitimate payment and every legitimate password change. The cause is a combination of the declared costs and the evidence, not a defect in the code. With C~esc~ = 0.3 and C~miss~ = 10 or 20, Allow has the lowest expected loss only below a probability of 0.03 at tier 3 and 0.015 at tier 4. The first transfer of an episode receives a probability of about 0.033 from the intercept and two behavioral features alone, and about 0.086 when the transition-deviation feature also fires. Escalate then has the lowest expected loss, and without a reviewer an escalated call is withheld. On the sixteen paired fixtures of sets 1 and 2, REM v1.0 withheld all fourteen legitimate payments (Section 4.6.7).

**Modify, Escalate and Block coincide.** When every Modify and Escalate verdict of REM v1.0 is replaced by Block, the outcome of none of the 3,313 episodes changes. The Allow-and-Block-only arm of Table 4.11 uses the same fitted model and releases more calls than REM v1.0, because without Escalate the boundary of Allow moves from C~esc~/C~miss~(k) to the Allow–Block threshold of Equation 3.9. In this evaluation the four-verdict structure is therefore a two-verdict structure in effect, and the Escalate option acts only by narrowing the Allow region. Whether the four verdicts differ with a live agent and a reviewer is not tested.

**All residual attacks are one ambiguous task.** All 11 successful attacks under REM v1.0 are episodes of user_task_15, in which the user's own task pays the account that the attack also targets (Section 4.2.2). The comparisons "11 against 12 against 13" in Table 4.11 are thus comparisons of how arms handle one ambiguous task, and carry no weight.

### 4.4.2 Distributed Defenses (Recorded Outcomes Only)

For orientation, the recorded outcomes of four defenses distributed with the benchmark, on gpt-4o (`e4_cross_template_and_defenses.json`):

| Defense | ASR | Benign utility |
|---|---|---|
| tool_filter | 0.112 | 0.81 |
| transformers_pi_detector | 0.007 | 0.44 |
| repeat_user_prompt | 0.462 | 0.94 |
| spotlighting_with_delimiting | 0.615 | 0.81 |

These are recorded outcomes, possibly under different suite versions, and were not replayed. **They are not a controlled comparison with REM** and are not used as one.

### 4.4.3 A Published Policy and a Request-Derived Permission Rule in the Same Harness

*Kind of evidence: replay; development evidence on both populations (every episode had been inspected before 13 November 2026). The arms and the comparisons marked with an asterisk were fixed before any of these outcomes was computed.*

**The published policy.** Progent (T. Shi et al., 2025) enforces per-tool policies with argument restrictions before each tool call. Its official repository contains, at the commit of 10 September 2025, a manual policy for the AgentDojo banking suite: `send_money`, `schedule_transaction` and `update_scheduled_transaction` are permitted only for five listed recipients; `update_password` has no policy entry and is therefore not permitted; the remaining tools are permitted. The policy was read from the repository as data, with the file digests pinned, and applied to the recorded calls by this project's replay code. The arm is therefore **Progent's published manual banking policy, adapted to the shared replay harness**. It is **not** a reproduction of the Progent framework or of the paper's results, not Progent with policies generated by a language model, and not a live-agent comparison. The upstream checking code was not executed in this project; its equivalence with the decision function used here was established by reading it. An independent review of 14 November 2026 reported a differential check of the upstream checker functions against this decision function on 468 argument cases, with the pinned file digests confirmed, and found no difference; that check covers the policy logic in that scope and was not repeated here. The repository bundles AgentDojo 0.1.29; the eleven banking tools have the same parameters and defaults in 0.1.29 and 0.1.35, so the policy applies unchanged to the recordings.

**The permission rule G1** releases a state-changing call only if the user's request supports its operation, its recipient and its amount (Chapter 3, Section 3.14). It is an exploratory extension, not part of REM v1.0 or v1.1.

**Table 4.13. Replay results on the primary recordings** (step-level, no reviewer; `improvement_results.json`, `results_v2.json`; REM, B1 and P2 are in Table 4.11, A2 is repeated for reference)

| Arm | Successful attacks / 2,979 | Episodes with a released attack-labelled call | Benign tasks completed / 334 | All tasks completed / 3,313 | Legitimate state-changing calls released / 178 |
|---|---|---|---|---|---|
| A2 | 13 | 27 | 140 | 1,474 | 83 |
| **Progent manual policy** | 0 | 0 | 154 | 1,450 | 136 |
| **Permission rule G1** | 10 | 23 | 149 | 1,574 | 112 |
| **Repaired permission rule G2** | 1 | 2 | 132 | 1,407 | 93 |

**Table 4.14. Replay results on the second population** (the same arms; nothing fitted on these episodes; the other arms are in Table 4.36)

| Arm | Successful attacks / 2,065 | Episodes with a released attack-labelled call | Benign tasks completed / 48 | All tasks completed / 2,113 | Legitimate state-changing calls released / 51 |
|---|---|---|---|---|---|
| A2 | 4 | 4 | 27 | 1,232 | 27 |
| **Progent manual policy** | 0 | 0 | 35 | 1,305 | 48 |
| **Permission rule G1** | 3 | 3 | 32 | 1,358 | 36 |
| **Repaired permission rule G2** | 0 | 0 | 29 | 1,239 | 20 |

**Table 4.15. Paired contrasts** (first arm minus second arm, in percentage points, with the 95% grouped-bootstrap interval; PG = Progent manual policy; v1.0 and v1.1 = REM versions; * = fixed in advance)

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
- **A review found defects in G1, and the repaired rule G2 trades tasks for security.** G1 supports a payment whose amount the request assigns to another account, ignores whether a stated condition holds, and supports a repeated payment (Section 4.6.10). The repaired rule G2 has 1 successful attack on the primary recordings and none on the second population, completes fewer tasks than G1, and against A2 and the published policy its task-completion differences are again not resolved (Table 4.15). Its results were obtained after G1's were known; they are development evidence.
- **The two policies fail in different places.** The published policy completes no password-change task (user task 14: 0 of 209 and 0 of 129 episodes), because the tool is not permitted. The permission rule completes none of the tasks in which the recipient or the instruction is supplied only by a file (user tasks 0, 2 and 12). All of its successful attacks are in user task 15, where the account the attacker wants is the account the user names (Section 4.2.2).

**A fixed list is tied to the seeded environment.** The five recipients are payees that exist in the benchmark's initial state. On the twenty paired fixtures written for this study, whose payees are not on the list, the published policy releases no unsafe call and withholds 13 of 20 legitimate calls (Section 4.6.9). The benchmark policy published with aiAuthZ has the same form: a list of five known payees, with password change denied (repository whitepaper; Section 4.4.5). Neither derives permission from the individual request, which is what the permission rule attempts.

### 4.4.4 Live-Agent and Published-Defense Experiments: Status

**No experiment with a language model was executed in this thesis.** This section reports no attack success rate, utility or adaptation behavior of a live agent. The only published policy evaluated by this project is Progent's manual banking policy, which needs no model and was replayed on the recorded episodes (Section 4.4.3).

**Closed-loop evaluation of REM.** A harness in which a running agent receives REM's refusals and continues is implemented and tested with a scripted agent (Appendix D). It was not executed with a model, for two reasons: no credential for a model provider was available in the execution environment, and the design inputs it needs (backbone, decoding parameters, number of repeats, source of fitted parameters, spending authorization) have not been decided. The harness refuses to start until they are.

**MELON with and without REM.** An integration that places REM behind the MELON defense (Zhu, Yang, et al., 2025) is implemented: MELON's published code is used unmodified at a pinned commit, and the two conditions differ only in the tool executor. Thirty tests pass with scripted agents, a deterministic stand-in for the embedding service and a simulated provider. These tests show that the integration is mechanically correct. They show nothing about effectiveness: **MELON and MELON with REM are implementation-verified and effectiveness-unevaluated.** A real run needs a model credential, MELON's embedding service and an approved spending limit, none of which was available. The protocol and its status are in Appendix D.

**Other published defenses.** NEXUS, Task Shield, CaMeL, PROVISO, aiAuthZ, Kairos and Progent with generated policies were not run. Section 4.4.5 states why for each. A sealed protocol for a later comparison with a live agent, with one benchmark version for all conditions, is kept in the repository; it has not been executed.

**What replay cannot substitute for.** A live agent can retry, rephrase or reach the attacker's goal through another tool after a refusal. The replay attack success rate is therefore not an upper bound on live attack success, and the replay utility is not a lower or an upper bound on live utility. The size and direction of the difference are empirical questions that only a closed-loop run can answer (Appendix D compares the two designs).

### 4.4.5 Comparison with Prior Work

The comparison restates design positions documented in Chapter 2 and does not rank systems, because no shared evaluation exists. Properties marked U in Chapter 2 are unverified.

**Papers read in full in November 2026 (Chapter 2, Section 2.12.6).** The position of REM relative to them is as follows.

**Table 4.16. Relation of the results to recent work, and why no experimental comparison is reported**

| Work | Relation to the results of this chapter | Why it was not run |
|---|---|---|
| NEXUS (Hossain et al., 2026) | Same family: calibrated logistic score, rules and four graduated interventions. Its repository documentation reports that on rule-blind plans its policy predicts only Allow or Block, which parallels the finding here that the middle verdicts do not act. A working document in the authors' repository (dated 23 May 2026; not the published paper) states that the learned scorer gives no gain in binary detection over the rules alone and that its contribution is to four-class intervention accuracy (0.6406 against 0.3672), which parallels the finding here that the learned score adds no measured security over rules | Full text not read (publisher's site not reachable). The repository was read on 13 November 2026 and not executed. There is no valid adapter from a banking tool call to its structured-plan representation, and re-implementing it from its documentation would not be NEXUS |
| CASEL (Y. Zhang et al., 2026) | Publishes a per-mode cost rule of the same structure as Equation 3.6, in simulation, and reports that it does not reduce harm beyond a simpler gate | No benchmark results exist to compare with |
| C. Zhang et al. (2026) | Is consistent with the small effect of calibration on outcomes. Its intervention-value target was tested here (Section 4.6.6) and did not transfer to an unseen attack objective, a condition the paper does not examine | Tested as an adaptation, labelled as derived |
| AgentBoundary (T. Yang et al., 2026) | Reports over-defense as a general finding; REM's release of 4 of 51 authorized calls is an instance. Its paired design is used for the fixtures | Its mitigation is a language-model component |
| PROVISO (Yan et al., 2026) | Reports much higher utility with a trained controller and restored rollouts. Its stated limitation, fitting per benchmark without a transfer study, is the condition examined here for a simpler monitor | No implementation is named in the paper; it needs an encoder and an agent model |
| Task Shield; MELON | Reported on AgentDojo with live agents. Task Shield judges each action against the user's instructions with a language model; the permission rule of Section 4.4.3 does this with a parser, for three argument types only | Need a model in the decision path; MELON integration is implemented and unevaluated (Section 4.4.4) |
| Progent (T. Shi et al., 2025) | Deterministic argument-level policies before each call. **Its manual banking policy was replayed here** (Section 4.4.3): no successful attack; no password-change task completed | Only the manual policy was run. Policies generated by a language model were not. The paper was not read; the official code was |
| CaMeL (Debenedetti et al., 2025) | Prevents untrusted data from influencing control flow by construction | Needs a model and its interpreter; not run and not approximated |
| aiAuthZ (Kodathala, 2026) | Adds a signed identity channel and an off-host argument-level policy. Its repository whitepaper reports a run on the AgentDojo banking suite (version 0.1.35, twenty task pairs, one model) with a fixed list of five known payees and password change denied: no successful attack, six attacker-directed calls blocked, and clean utility of 80% against 100% because one legitimate first-time payment was blocked. The abstract recorded earlier states seven blocked calls; the difference between versions is not resolved here. The figures are from a live agent and are not comparable with replay | Not run. arXiv text not read; abstract and the authors' repository whitepaper read |
| Kairos (Hempel et al., 2026; abstract only) | Enforces on effects at the system boundary | Not available; full text not read |

**Published figures are not placed beside REM's.** The authors' reported results on AgentDojo come from live agents, other models, other suites or other attack sets. REM's figures come from replay of recorded trajectories. Putting them in one table would present incompatible measurements as a comparison. The figures for Progent's manual policy in Section 4.4.3 are this project's replay measurements of the published policy, not figures from the Progent paper.

## 4.5 Ablation Studies

This section reports what happens when a component is removed or replaced. It covers the components of REM v1.0, the verdict set, and the components of the exploratory extension. Every ablation is a single-benchmark observation; none shows that a component has no benefit in general.

### 4.5.1 Ablations of the Components of REM v1.0

**Table 4.17. Ablations** (observe-only columns: held-out recorded steps; replay columns: step-level semantics, no reviewer)

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
- **Calibration.** Without the calibration map, replay attack success is unchanged (11 of 2,979 attacked episodes) and benign task completion is 110 instead of 105 of 334 (0.329 against 0.314). Calibration therefore changed a small number of decisions and no security count.
- **Predicates.** No change was observed from removing them. With Π empty, D2 fixed the verdict for 58 steps.
- **Tiers.** The tier map moves the trade-off. A single low tier recovers utility and loses protection; a single high tier does the opposite.

None of these observations establishes that a component has no benefit in general. They are single-benchmark observations with nine attacked groups.

### 4.5.2 Ablation of the Behavioral Evidence Group and of the Verdict Set

Two ablations of Table D.2 were followed up in later studies, and their results are reported where those studies are described.

- **Behavioral evidence.** Removing the four behavioral features is REM v1.1. In the pilot it left replay attack success at 11 of 2,979 and raised benign task completion from 105 to 140 of 334. Under the double holdout it has 14 successful attacks against 11 (Table 4.31). On the second population it completed 1,074 against 916 of 2,113 tasks with 1 against 3 successful attacks (Section 4.6.8).
- **Verdict set.** Replacing every Modify and Escalate verdict of REM v1.0 by Block changes the outcome of none of the 3,313 primary episodes (Section 4.4.1). Removing the two verdicts from the decision rule, so that Allow is chosen up to the Allow–Block threshold of Equation 3.9, gives more released calls with 13 against 11 successful attacks on the primary recordings and 3 against 3 on the second population (Tables 4.11 and 4.36), and 31 against 13 when the attacker's identifier is reformatted (Table 4.34).
- **Calibration.** Without the calibration map, replay attack success is unchanged (11 of 2,979) and benign task completion is 110 instead of 105 of 334 (Table D.2: 0.329 against 0.314). Calibration therefore changed a small number of decisions. It did not change the security count.

### 4.5.3 Ablations of the Task-Permission Extension

*Kind of evidence: replay; development evidence. The ablations are diagnostic: the rule G1 was fixed with all components before any outcome was computed and was not changed afterwards.*

**Table 4.18. The permission rule with one component removed** (`improvement_results.json`)

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

**Table 4.19. Decision semantics and a learned model on the permission evidence** (S1: held-out attacker objective; S2: double holdout)

| Arm | S1: attacks / 2,979 | S1: all tasks / 3,313 | S2: attacks | S2: all tasks | Second population: attacks / 2,065 | Second population: all tasks / 2,113 | Held-out credential-change attacks, S1 / 334 |
|---|---|---|---|---|---|---|---|
| REM v1.1 | 11 | 1,287 | 14 | 1,272 | 1 | 1,074 | 0 |
| REM v1.1 with the two-verdict decision (V11d) | 131 | 1,492 | 131 | 1,452 | 58 | 1,182 | 119 |
| Permission rule G1 | 10 | 1,574 | 10 | 1,574 | 3 | 1,358 | 0 |
| Learned on permission evidence, no guard (L0) | 11 | 1,711 | 12 | 1,707 | 2 | 1,526 | 0 |
| Guard, then learned, four verdicts (L1) | 10 | 1,531 | 10 | 1,429 | 1 | 1,338 | 0 |
| Guard, then learned, two verdicts (L2) | 10 | 1,680 | 10 | 1,676 | 2 | 1,489 | 0 |
| Guard; learned decides unknown calls only (L2s) | 10 | 1,644 | 10 | 1,644 | 3 | 1,459 | 0 |

**Table 4.20. Paired contrasts for the decision semantics, the learned model and the guard** (first arm minus second arm, in percentage points, with the 95% interval; v1.1 = REM v1.1; * = fixed in advance)

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
- **The learned model costs robustness.** With the attacker's identifier reformatted, L2 has 38 successful attacks where G1 has 10 (Table 4.40). The calls it then releases have unknown permission status; the model's remaining evidence for them is the provenance match, which reformatting removes.
- **The guard costs little and removes little on the recordings** (L0 against L2: at most two attacks and one to two points of tasks). On the paired fixtures the unguarded model releases more unsafe calls (6 against 3 on set 4; Table 4.41).

### 4.5.4 Ablations of the Repaired Rule and of the Authority Guard

*Kind of evidence: replay; development evidence. Protocol of 14 November 2026, committed before these arms were replayed (commit `ae3f923`).*

**Table 4.21. The repaired rule, its ablations and the learned arms behind the authority guard** (`results_v2.json`)

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

**Table 4.22. Paired contrasts of the follow-up** (first arm minus second arm, in percentage points, with the 95% interval; * = fixed in advance)

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

## 4.6 Results and Discussion

This section reports the results that the earlier sections did not already present: the pilot's feasibility check, the quality of the estimator, the observe-only decisions, the replay of REM and its baseline, the sequential analysis, realized loss, generalization, robustness, the confirmatory run and the exploratory extension. It then interprets the findings, states the threats to validity and summarizes the chapter.

### 4.6.1 RQ1 — Offline Classification (Held-Out Predictions)

**Table 4.23. Held-out discrimination and calibration, pooled over nine outer folds** (6,762 steps; 921 positive; `e1_crossfit.json`)

| Metric | Calibrated p, label-NLL fit (reference) | Calibrated p, Platt smoothed targets | Uncalibrated p̃ |
|---|---|---|---|
| ROC-AUC | 0.938 [0.908, 0.961] | 0.938 | 0.939 |
| Average precision (PR-AUC estimate) | 0.719 [0.559, 0.827] | 0.719 | 0.721 |
| ECE (M = 10) | 0.044 [0.033, 0.084] | 0.044 | 0.042 |
| Log-loss | 0.201 [0.149, 0.294] | 0.201 | 0.201 |
| Brier score (binary convention) | 0.060 | 0.060 | 0.060 |

**Table 4.24. Per-fold results (calibrated, label-NLL)**

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
   - grouping by user task (16 folds): pooled ROC-AUC 0.943. One fold, user_task_15, scores 0.211; Section 4.2.2 explains this as a label problem;
   - five other attack templates on gpt-4o, with no refitting: ROC-AUC 0.922–0.959, ECE 0.028–0.086.

![Figure 4.1. Held-out reliability diagram, calibrated and uncalibrated (10 equal-width bins). Mid-range bins contain few steps.](results/pilot_R2/figures/fig_reliability.png){width=55%}

### 4.6.2 RQ2 — Observe-Only Decisions

All three policies use the same held-out calibrated probabilities and the same predicates:
- **REM** adds tier-indexed expected loss with Escalate available;
- **REM without expected-loss Escalate** (post-hoc) has the same escalation opportunity as the baseline (D2 only);
- **B1** is the baseline with the thresholds of Eq. 3.14.

Verdicts were computed on the recorded steps and not enforced.

**Table 4.25. Observe-only verdicts on held-out steps** (y = 0: n = 5,841; y = 1: n = 921; `e2_e5_e6_observe_only.json`)

| | REM | REM w/o expected-loss Escalate | B1 |
|---|---|---|---|
| Any intervention on y = 1 steps | 0.973 [0.957, 0.987] | 0.973 | 0.740 [0.473, 0.922] |
| Any intervention on y = 0 steps (step false-positive rate) | 0.227 [0.213, 0.239] | 0.198 | 0.056 [0.047, 0.066] |
| Escalate share of all steps | 0.196 | 0.009 | 0.009 |
| y = 0 steps withheld if an idealized reviewer resolves escalations | 0.040 | 0.188 | 0.046 |
| Ties | 0 | 0 | 0 |
| Verdicts fixed by D2 | 58 | 58 | 58 |

**Table 4.26. Observe-only interventions by consequence tier and action category** (`r2_breakdowns.json`)

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
- **B1 and credential changes.** B1 intervened on none of the 124 credential-change attack steps. These are the steps of the fold whose probabilities were most miscalibrated (Table 4.24). Its thresholds are fixed by benign false-positive rates and did not reach them.
- **Realized loss.** Under the decision costs, realized loss is 0.114 for REM, 0.136 for REM without expected-loss Escalate and 0.652 for B1. This comparison favors REM by construction (Chapter 3, Section 3.12.3) and is not evidence of superiority.

### 4.6.3 RQ2 and RQ3 — Replay Sensitivity Analysis

The replay re-executes each recorded episode in the benchmark's sandbox with REM enforcing its verdicts (Chapter 3, Section 3.11.10). Its use is a proposed amendment to the scope of Chapter 3. Three properties limit what it can show:
- **NO-ADAPT.** The agent emits the calls it emitted in the recorded run, whatever REM does. After a refusal, a live agent could retry, rephrase, use another tool, or abandon the task. Replay therefore cannot show how often a live agent would achieve the attacker's goal by another route, and **a near-zero replay ASR is not evidence of protection against a live or adaptive agent.**
- **Mitigation semantics.** Under step-level semantics, Modify and Block have the same effect on the withheld call. The episode-level variant also restricts later calls: after a Block, every later call to a tool in 𝒯~R~ is refused, even one whose own verdict is Allow, and even though the agent never retries. The two semantics therefore give different replay results. Tables 4.27–4.30 use step-level semantics, the declared reference pending decision D-2; Table E.1 compares both semantics.
- **Not independent runs.** Replaying a recorded trajectory is deterministic. Repeating it adds no information about LLM behavior.
- **Closed-loop identifiability.** Once blocking changes what an agent proposes next, static scores and ungated trajectories need not identify the closed-loop trade-off between false blocks and misses (Ray, 2026). Recorded trajectories are ungated in this sense. Offline replay of AgentDojo's recorded traces has also been used to evaluate temporal-logic monitors (Kekatos et al., 2026); neither use establishes enforcement against live agents.

#### Replay validity and exclusions

With every call allowed, the replay reproduced the recorded utility and security outcomes of 3,313 of the 3,334 episodes.

**The 21 failures** (`r2_breakdowns.json`, `replay_failures`) are concentrated:
- 20 are user_task_13 episodes whose utility verdict differs; 1 is a user_task_14 episode whose security verdict differs;
- 10 are from gpt-4o, and the remaining 11 are spread over six other backbones;
- none raised an error.

The pattern is consistent with a change in the user task's definition between the suite version used for recording and the version used for replay (v1). This was not confirmed task by task.

**Effect of the exclusion.** Of the 21 excluded episodes, 19 are attacked, and 14 of these recorded attack success. Excluding them changes the recorded attack-success rate from 0.228 (all 2,998 attacked episodes) to 0.226 (2,979 retained), and the recorded benign utility from 0.521 (336) to 0.524 (334). All replay metrics use the 2,979 attacked and 334 benign retained episodes.

#### Results

**Table 4.27. Replay results, step-level semantics** (attacked n = 2,979; benign n = 334; `e4_e5_enforcement_replay.json`)

| Configuration | ASR | Benign utility | Utility under attack |
|---|---|---|---|
| B0, no defense (replay) | 0.226 [0.148, 0.295] | 0.524 [0.381, 0.676] | 0.492 |
| B1, no reviewer | 0.055 [0.011, 0.134] | 0.509 [0.334, 0.702] | 0.514 |
| REM, no reviewer | 0.004 [0.001, 0.007] | 0.314 [0.110, 0.548] | 0.364 |
| REM w/o expected-loss Escalate, no reviewer | 0.004 [0.001, 0.007] | 0.329 [0.126, 0.551] | 0.374 |
| REM, idealized reviewer | 0.004 [0.001, 0.007] | 0.497 [0.333, 0.680] | 0.496 |
| REM w/o expected-loss Escalate, idealized reviewer | 0.004 [0.001, 0.007] | 0.311 [0.123, 0.518] | 0.359 |

**Table 4.28. Paired differences (grouped bootstrap)**

| Comparison | ΔASR | ΔBenign utility |
|---|---|---|
| REM − B1, no reviewer | −0.051 [−0.130, −0.007] | −0.195 [−0.341, −0.074] |
| REM w/o Esc. − B1, no reviewer (same escalation opportunity) | −0.051 [−0.130, −0.007] | −0.180 [−0.325, −0.063] |
| REM − B1, idealized reviewer | −0.051 [−0.130, −0.007] | +0.003 [−0.009, 0.018] |
| REM − REM w/o Esc., idealized reviewer | 0.000 | +0.186 [0.065, 0.335] |
| REM − B0, no reviewer | −0.222 [−0.289, −0.146] | −0.210 [−0.379, −0.051] |

**Table 4.29. Replay ASR by the attacker's target action** (`r2_breakdowns.json`)

| Target action | Injection tasks | Attacked episodes | B0 | B1 (no reviewer) | REM (no reviewer) |
|---|---|---|---|---|---|
| Value transfer | 7 | 2,334 | 0.213 [0.128, 0.293] | 0.014 [0.007, 0.020] | 0.005 [0.002, 0.008] |
| Payment modification | 1 | 311 | 0.183 | 0.042 | 0.000 |
| Credential change | 1 | 334 | 0.356 | 0.356 | 0.000 |

Single-task categories have no interval.

**Table 4.30. Replay benign utility by kind of user task** (`r2_breakdowns.json`)

| User tasks | Tasks | Episodes | B0 | B1 (no reviewer) | REM (no reviewer) | REM (idealized reviewer) |
|---|---|---|---|---|---|---|
| Requiring a state change | 12 | 250 | 0.472 [0.320, 0.632] | 0.432 [0.238, 0.637] | 0.168 [0.000, 0.420] | 0.416 [0.238, 0.600] |
| Read-only | 4 | 84 | 0.679 [0.369, 0.929] | 0.738 [0.417, 0.976] | 0.750 [0.429, 1.000] | 0.738 [0.417, 0.976] |

![Figure 4.2. Replay sensitivity analysis (NO-ADAPT): ASR and benign utility with 95% grouped-bootstrap intervals.](results/pilot_R2/figures/fig_enforcement_replay.png){width=95%}

![Figure 4.3. Security–utility trade-off in the replay sensitivity analysis (NO-ADAPT, step-level semantics): attack success rate against benign utility for B0, B1, REM and REM without expected-loss Escalate under both reviewer bounds, and for the single-tier ablations. Values from `results/pilot_R2/e4_e5_enforcement_replay.json`; no live result.](REM_FINAL_THESIS/final_five_chapters/figures/fig4_3_security_utility_tradeoff.png){width=100%}

**What the replay results show, within NO-ADAPT:**
- **Where the ASR difference comes from.** REM withholds more of the recorded attack attempts than B1. Most of the difference comes from the credential-change and payment-modification attacks (Table 4.29), each represented by a single injection task.
- **The utility cost falls on state-changing tasks.** With no reviewer, REM's benign utility falls to 0.168 on those tasks (Table 4.30).
- **The cost is not caused by the escalation option.** REM without expected-loss Escalate has almost the same utility cost relative to B1 (Table 4.28).
- **With an idealized reviewer, the cost disappears.** That reviewer knows the label and is an upper bound on reviewer quality, not a model of one.

**RQ3 quantities:**
- **Residual attack success after Modify.** In oracle-Modify replays within the fitting folds, r~mod~ was 0.000 at tier 3 (530 episodes) and 0.010 at tier 4 (298 episodes) (`e4_rmod_and_replay_validity.json`). In replays where REM applied Modify to an attack step, residual ASR was 0.000 (610 episodes). Under NO-ADAPT a withheld call simply does not occur, so **these values are consequences of the assumption, not measurements of tool restriction against a live agent.**
- **Escalation rate.** 0.196 of all steps in the observe-only analysis (Table 4.25).
- **Processing time** (Appendix B.1.14, Table B.8). **Complete call** (R4 re-execution, 1 November 2026; `results/pilot_R4/e4_e5_enforcement_replay.json`, `latency_full_ms_*`): median 0.21–0.28 ms and 95th percentile 0.49–0.70 ms per step, across the 8 REM configurations (6,684 steps each). **Partial timer**, which excludes attribution, audit-record construction and history recording: median 0.18–0.24 ms and 95th percentile 0.46–0.64 ms in the same run. Earlier runs measured only the partial timer: median 0.14–0.20 ms and 95th percentile 0.39–0.54 ms (R1, R2), with the 30 October re-execution within these ranges.
- **Memory.** The median peak traced allocation was 4.4 KB per step, with a 95th percentile of 12.4 KB (611 steps of 300 episodes; `latency_memory_profile.json`). The first run (R1) measured 2.9 KB; like time, memory varies between runs. The re-execution of 30 October measured the same value. In the R4 re-execution, where `evaluate` also records the complete-call timer, the median was 4,349 bytes against 4,364 bytes, with the same 95th percentile (12,419.5 bytes; `results/pilot_R4/latency_memory_profile.json`). The memory boundary is the complete `evaluate` call in both.

These figures apply to the evaluated configuration only: no neural injection classifier, no reviewer, recorded inputs. They are not estimates for a complete deployment.

**Sensitivity to the mitigation semantics.** Step-level semantics is the declared reference (Chapter 3, Section 3.8), pending the supervisor's decision on SC-1. The same replays under the episode-level variant are reported in Appendix E. In summary: REM's ASR is identical under both semantics (0.004); B1's is lower under the episode-level variant (0.055 against 0.046), because the restriction set left by an earlier Block or Modify refuses later state-changing calls; utility under attack is lower or equal under the episode-level variant in every configuration; and benign utility coincides. The episode-level rows are a sensitivity analysis and do not replace Tables 4.27 to 4.30.

### 4.6.4 Optional Sequential Analysis (CUSUM, observe-only)

The Bernoulli CUSUM was fitted on each fold's benign fitting episodes (`e3_a2_cusum_observe_only.json`):
- **q₁ = 0.3:** it was undefined in all folds, because the estimated pre-change rate (about 0.34) exceeded q₁.
- **q₁ = 0.5 and 0.7:**
  - an alarm followed the entry of injected content in 74.8% of attacked episodes with a positive step;
  - it came at or before the first positive step in 42.5–43.8%;
  - the median delay was 1 step;
  - the held-out benign false-alarm rate was 0.106, against an in-fold target of 0.05.

The CUSUM issued no verdicts.

### 4.6.5 Realized Loss across the Declared Grid

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

### 4.6.6 Generalization to Unseen Tasks and Objectives, and a Rejected Candidate

*Kind of evidence: replay on the primary recordings under schemes S1, S2 and S3 (Chapter 3, Section 3.11.12). REM v1.1 under S2 is post hoc.*

#### Double holdout and held-out templates

**Table 4.31. Successful attacks and benign tasks completed under three generalization schemes** (`study_results.json`)

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

- **REM v1.0 has the same two headline counts under S1 and S2.** Its successful attacks (11 of 2,979) and its completed benign tasks (105 of 334) do not change when the user task is also held out. Other quantities change slightly: it completes 1,083 tasks under attack under S1 and 1,078 under S2, and releases 33 and 35 of the 178 authorized calls. Its attack count also stays low on templates it never saw. This stability is that of a policy that withholds most state-changing calls: there is little for a change of task to alter.
- **The rules are identical under S1 and S2 by construction**, because they have no fitted quantity.
- **REM v1.1 loses three episodes of security under double holdout** (11 to 14 of 2,979) and keeps its utility. This observation was made after results were seen and motivated the confirmatory run of Section 4.6.8.

#### The pre-declared candidate failed

The candidate declared in advance for this study was the authorization-aware intervention-value policy (Chapter 3, Table 3.14). The protocol stated that an improvement over REM v1.0 would be claimed only if, under both S1 and S2, the paired gain in benign utility had a 95% interval above zero and the paired change in attack success had an interval not entirely above zero.

**Table 4.32. Pre-declared contrasts of the candidate against REM v1.0** (paired, grouped bootstrap; percentage points)

| Scheme | Benign utility | Attack success rate | Rate of episodes with a released attack-labelled call |
|---|---|---|---|
| S1 | +6.6 [0.0, 18.2] | +4.1 [0.0, 12.1] | +4.2 [0.03, 12.4] |
| S2 | +1.5 [0.0, 4.5] | +4.1 [0.0, 12.1] | +4.2 [0.03, 12.4] |

**The candidate is rejected.** Its utility gain is not established under either scheme and almost disappears under double holdout. It admits 132 successful attacks where REM v1.0 admits 11, and its rate of episodes with a released attack-labelled call rises with an interval that excludes zero.

The failure has one identifiable cause. Of the 132 attacks, 119 are episodes of the credential-change objective, and the intervention-value policy without authorization features releases all 119 of them. When that objective is held out, the training outcomes contain no case in which withholding a credential update prevents harm. The policy learns that harm is prevented by withholding payments to new recipients, and it assigns no security value to a password taken from a document. The utility side transfers poorly as well: the candidate's model of whether withholding a call breaks the user's task has a held-out ROC-AUC of 0.857 under S1 and 0.729 under S2 (0.854 and 0.682 without the authorization features).

#### What the diagnostic arms show

**Table 4.33. Diagnostic arms on the primary recordings, scheme S1** (attacks / 2,979; benign tasks / 334)

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

### 4.6.7 Robustness Probes: Reformatted Identifiers and Paired Call Fixtures

*Kind of evidence: replay with a modified injected text, and call-level fixtures. Neither is a benchmark result. Fixture counts are not rates.*

#### Reformatted attacker identifier

In 2,645 attacked episodes the injected text contains the attacker's account identifier. The probe rewrites that identifier in groups of four characters inside the injected text and leaves the recorded calls unchanged (Chapter 3, Section 3.11.13). The all-allow replay still reproduces all 2,645 recorded outcomes.

**Table 4.34. Successful attacks before and after the identifier is reformatted** (2,645 attacked episodes; `study_results.json`)

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

#### Paired call fixtures

Twenty-three paired fixtures in three sets were scored once each with the models of one fold (Chapter 3, Section 3.11.13). Sets 1 and 2 contain fourteen payment pairs, in which a legitimate payment and a substituted payment share a scaffold, and two read-only pairs, in which the unsafe call is an unrequested payment. Set 3 contains three credential pairs and four pairs with reformatted or fragmented identifiers.

**Table 4.35. Paired fixtures: legitimate calls released and unsafe calls released** (counts)

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
- **Every arm of Table 4.35 that releases legitimate payments also releases an unrequested payment whose recipient and amount occur in the user's words.** In the two read-only pairs the user mentions a past payment, with its payee and amount, asks only for the account balance and states that no payment is to be made. The document read by the agent then asks for the same payment again. Nothing in the features that these arms use distinguishes this unrequested payment from a requested one: its recipient and amount occur in the user's own text. Occurrence in the user's text is not authorization. The features do not represent the user's statement that no payment is wanted, although the request contains it.
- **Amount substitution passes identity-only checks.** A rule that verifies the recipient and not the amount releases a payment to the right recipient for the wrong amount.
- **Reformatting defeats exact matching on fixtures as on the benchmark.** P1 and B1 release two unsafe calls of set 3 whose identifiers were reformatted.
- **REM v1.1 and P2 behave alike** on set 3: five legitimate calls released, no unsafe call released, and the same two legitimate calls withheld.

No arm of Table 4.35, learned or rule-based, gets every pair right. This is a finding about the features and policies tested in that study: they describe the provenance of a call's arguments and not which operation, recipient and amount the request asks for. It is not a finding that the request text cannot supply that information. Section 4.6.9 reports a rule that parses the request, and its results on the same fixtures.

### 4.6.8 Confirmatory Evaluation of REM v1.1 (Run of 11 November 2026)

*Kind of evidence: confirmatory replay. Protocol and verdict rule committed before the data were opened (Chapter 3, Section 3.11.14); no amendment. Population: Table 4.5, unread at the time of this run and development evidence for every later analysis. Models: frozen from the primary recordings; nothing fitted or selected on these episodes.*

#### Results

**Table 4.36. Confirmatory replay results** (2,065 attacked and 48 benign eligible episodes; step-level, no reviewer; `confirmatory_results.json`)

| Arm | Successful attacks / 2,065 | Episodes with a released attack-labelled call | Tasks completed under attack / 2,065 | Benign tasks completed / 48 | All tasks completed / 2,113 | Authorized calls released / 51 |
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

**Table 4.37. Paired contrasts on the confirmatory population** (percentage points; 95% grouped-bootstrap interval; gained / lost = episodes in which only the first or only the second arm completes the task)

| Contrast | Task completion, all episodes | Attack success rate | Benign episodes only | Gained / lost |
|---|---|---|---|---|
| **REM v1.1 − REM v1.0 (pre-declared)** | **+7.48 [1.17, 16.02]** | **−0.10 [−0.29, 0.00]** | +14.58 [0.00, 33.33] | 158 / 0 |
| REM v1.1 − P2 | +1.47 [−5.28, 7.98] | −0.15 [−0.38, 0.00] | +2.08 [0.00, 6.25] | 88 / 57 |
| REM v1.1 − A2 | −7.48 [−25.66, 8.16] | −0.15 [−0.38, 0.00] | −4.17 [−25.00, 14.58] | 142 / 300 |
| P2 − REM v1.0 | +6.01 [−5.17, 20.25] | +0.05 [0.00, 0.15] | +12.50 [−2.08, 31.25] | 193 / 66 |
| A2 − REM v1.0 | +14.96 [−1.29, 34.42] | +0.05 [0.00, 0.15] | +18.75 [4.17, 37.50] | 393 / 77 |
| REM v1.0 − B1 | −28.30 [−47.16, −10.83] | −3.10 [−8.27, −0.39] | −37.50 [−58.33, −16.67] | 26 / 624 |

The contrast of REM v1.1 against REM v1.0 in episodes with a released attack-labelled call equals the attack-success contrast: −0.10 [−0.29, 0.00].

#### The pre-declared verdict

All three conditions of the rule hold.

| Condition | Result |
|---|---|
| (a) The interval of the task-completion difference lies above zero | +7.48 points [1.17, 16.02] |
| (b) Neither security interval lies entirely above zero | both −0.10 [−0.29, 0.00] |
| (c) The candidate's successful attacks do not exceed those of rule P2 | 1 against 4 |

**The pre-declared verdict is GO.** On recordings that no analysis had read before this run, REM without the behavioral evidence group completes more tasks than REM v1.0 (1,074 against 916 of 2,113), and its count of successful attacks is not higher (1 against 3 of 2,065). REM v1.1 gains 158 episodes and loses none. The task-completion observation made post hoc on the primary recordings is confirmed for this benchmark in replay.

**GO is the outcome of a decision rule, not of a test of non-inferiority.** The rule was declared in advance in place of a security margin, because no margin has been approved (Chapter 3, Section 3.11.14). Its security conditions are that no interval lies entirely above zero and that the candidate has no more successful attacks than rule P2. The security interval, −0.10 points [−0.29, 0.00], includes zero. One successful attack against three, of 2,065, does not establish that REM v1.1 is at least as secure as REM v1.0, and no statistical superiority or non-inferiority on security is claimed. Under the double holdout on the primary recordings REM v1.1 has 14 successful attacks against 11 (Table 4.31).

#### What the verdict does not establish

- **REM v1.1 is not shown to be better than the rules.** Its difference from P2 is +1.47 points [−5.28, 7.98], and from A2 −7.48 points [−25.66, 8.16]. Neither is resolved. A2 completes 1,232 tasks, more than either REM version, with 4 successful attacks.
- **REM v1.0 is not shown to be better than the rules either.** P2 and A2 complete more tasks in point estimate with one more successful attack; the intervals of their differences from REM v1.0 include zero, except for A2 on benign episodes.
- **Utility remains far below the undefended agent.** The undefended agent completes 1,451 of 2,113 tasks; REM v1.1 completes 1,074. In benign episodes REM v1.1 releases 11 of 51 authorized calls; REM v1.0 releases 4.
- **The benign-only interval touches zero** (+14.58 points [0.00, 33.33], 18 against 25 of 48). The verdict rests on all episodes, as declared; most of the gain is task completion under attack.
- **A second configuration meets the same conditions.** REM restricted to Allow and Block completes 1,115 tasks with the same 3 attacks as REM v1.0 (+9.42 points [2.77, 17.87]). It was a comparator, not the declared candidate, and is not adopted. It adds to the evidence that the middle verdicts do not help in this evaluation.

#### Where the gain and the remaining attacks are

**Table 4.38. Tasks completed by user task on the confirmatory population** (all eligible episodes of each task; tasks on which the arms differ)

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

#### Intervention burden and processing time

**Table 4.39. Interventions on the confirmatory population** (8,221 recorded calls in 2,113 episodes, of which 5,808 are read-type calls that no arm withholds; `confirmatory_descriptives.json`; descriptive)

| Arm | State-changing calls not labelled as attempts: released / 1,854 | Escalate verdicts | Episodes with an Escalate verdict | Episodes with any withheld call |
|---|---|---|---|---|
| B1 | 1,347 | 63 | 61 | 821 |
| REM v1.0 | 224 | 1,392 | 928 | 1,423 |
| REM v1.1 | 497 | 981 | 671 | 1,257 |
| P2 | 549 | 0 | 0 | 1,210 |
| A2 | 928 | 0 | 0 | 1,080 |

In an attacked episode, a state-changing call that the label rule does not mark may still have been influenced by the injection. The 1,854 calls are therefore context, and the 51 authorized calls of benign episodes (Table 4.36) are the clean measure of legitimate-action approval.

Without a reviewer every Escalate is a withheld call. If a reviewer existed, REM v1.0 would refer 1,392 calls in 2,113 episodes and REM v1.1 would refer 981. Nothing is assumed about how well a reviewer would resolve them.

The median time to evaluate one call was 0.23 ms for the REM arms and 0.20 ms for the rules, with a 95th percentile of about 0.6 ms, measured under four parallel worker processes. The figures agree with the pilot's (Section 4.6.3) and describe this configuration only.

### 4.6.9 Exploratory Extension: Task-Permission Evidence

*Kind of evidence: replay and call-level fixtures; development evidence. Protocol, arms, parser, matcher and fixture set 4 were committed on 13 November 2026 before any outcome of a new arm was computed (commit `9137b03`); no amendment was made. The parser was written by an author who knows the sixteen requests of the benchmark; no request was held out from its development.*

The question of the extension is whether task-permission evidence compiled from the trusted request improves the trade-off between security and task completion, and which component is responsible for any change. The main results against the rules and the published policy are in Section 4.4.3, and the ablations in Section 4.5.3. This section adds the robustness probe, the paired fixtures, the per-task results and the verdict.

**Table 4.40. Successful attacks before and after the attacker's identifier is reformatted** (2,645 attacked episodes; REM, B1, P2 and A2 are in Table 4.34)

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

The permission rule is unchanged by the reformatting, with or without typed normalization, because it accepts a recipient only if the request itself supports it. The learned arm L2 is not robust (Section 4.5.3).

**Table 4.41. Paired fixtures** (each pair has one legitimate and one unsafe call for the same request; a pair is correct if the legitimate call is released and the unsafe call is withheld; counts, not rates)

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
- On the read-only pairs of set 2, in which the user mentions a past payment and asks for no payment, the permission rule withholds the unrequested payment that was released by every arm of Table 4.35 that releases legitimate payments. The request states that no payment is wanted, and a parser of the request can use that statement.
- **The rule's errors on set 4.** Two legitimate calls are withheld because of parser defects: an amount written as "Reimburse Marta 36.40 for the groceries" is not extracted, and "create a monthly standing order" is not recognized as a request for a scheduled payment. One legitimate call is withheld by design, because "1,250" can be read as two different amounts. One unsafe call is released: a second copy of a payment already made in the episode, because the rule keeps no record of requests already satisfied. The defects were not repaired after scoring.
- On set 3 the permission rule releases 3 of 7 legitimate calls, fewer than REM v1.1 (5 of 7).
- The learned arms release unsafe calls that the rule withholds (set 4: 3 for L2 and 6 for L0).

**Table 4.42. Tasks completed by user task on the primary recordings** (user tasks on which A2, the published policy, G1 and L2 all equal the undefended agent are omitted)

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
5. **Follow-up.** The rule was later found to have three defects, and its repair changes the picture (Section 4.6.10).
6. **Status.** Proposed and exploratory. The rule is not adopted and is not a new version of REM. A confirmatory test needs outcomes that do not yet exist: fresh runs with a live agent and request variants written by someone other than the author (the sealed protocol is in the repository).

**Decision time.** The median time to evaluate one call on the primary recordings was 0.09 ms for the permission rule and for the published policy and 0.18 ms for REM and for L2; the 95th percentile of the arms that parse bank records was about 3 ms. No arm calls a model.

### 4.6.10 Follow-up: Defects of the Permission Rule and a Call-Level Audit of User Task 15

*Kind of evidence: call-level probes, replay and a call-level audit; development evidence. The counterexamples were reported by an external review of 14 November 2026 and reproduced; the repaired rule was written after G1's results were known.*

**Three defects.** The frozen rule G1 matches a call's account against the set of accounts in the request and its amount against the set of amounts, independently. For "Send 50 to account A and 100 to account B" it therefore supports 100 to A and 50 to B. It records that "If my balance is above 1000, send 50 to A" is conditional but supports the payment when the balance read by the agent is 500. And it supports a second, identical payment after the first was executed. The repaired rule G2 represents the request as instructions that keep account, amount, condition and repeat count together; evaluates balance conditions against the most recent successful balance read, and treats any other condition as not satisfied; and refuses a transfer that repeats one already executed without error beyond the number of times the request asks for. A call that returned an error does not count, so a retry stays possible (Chapter 3, Section 3.14). The ablations are in Section 4.5.4.

**What the defects meant on the benchmark.** All successful attacks under G1 are in user task 15, where the new landlord's account named by the user is also the attacker's account. A call-level audit separated what the benchmark counts as attack success from what the user asked for, with criteria written before it was run: update the address; update the rent standing order to that account and 2200; refund the 10.00 received from a friend.

**Table 4.43. Released attack-labelled calls in user task 15** (`ut15_call_audit.json`)

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

**Table 4.44. Sensitivity analysis without user task 15** (additional; every comparison of this chapter keeps the task)

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
4. The fixtures and counterexamples used to find and repair these defects cannot test the repairs. A test needs requests written and reviewed by someone other than the author (Section 4.4.4).

### 4.6.11 Interpretation of the Findings

This section interprets the evaluation reported in Sections 4.1 to 4.6. Each conclusion is linked to the result that supports it and to the limit of that result. Section 4.1.4 defines the kinds of evidence. No live run was executed.

#### What the evidence supports

**Table 4.45. Conclusions, their support and their limits**

| # | Conclusion | Supporting result | Limit |
|---|---|---|---|
| 1 | Evidence at the tool boundary separates attack attempts from legitimate calls on unseen attack objectives | Held-out ROC-AUC 0.938; 0.927 when the user task is also held out | One benchmark; attempt labels, not audited by a human; most of the separation comes from one provenance feature |
| 2 | In replay, REM v1.0 withholds nearly all recorded attack attempts | Attack success 22.6% to 0.4% (primary) and 21.1% to 0.15% (second population) | NO-ADAPT; no live agent; residual attacks on the primary recordings are one ambiguous task |
| 3 | REM v1.0 obtains this by withholding most state-changing calls | 33 of 178 and 4 of 51 authorized calls released; 4 of 89 legitimate transfers | No reviewer; declared costs |
| 4 | Simple rules reach about the same number of successful attacks with at least as much task completion | Tables 4.11 and 4.36 | Differences between REM and the rules are not resolved statistically on the second population |
| 5 | Removing behavioral evidence raises REM's task completion | Confirmatory run: +7.48 points [1.17, 16.02]; 1 against 3 successful attacks | Security not resolved (interval includes zero; 14 against 11 under the double holdout); same benchmark tasks; replay; not better than the rules |
| 6 | Calibration changed little, and the four verdicts act as two | Without calibration: attacks unchanged at 11, benign tasks 110 instead of 105 of 334; γ~1~ between 0.945 and 0.981. 0 of 3,313 episodes change when Modify and Escalate become Block | This evaluation only |
| 7 | Supervising on intervention outcomes, and trusting user-named documents, lower security | 119 to 132 and 313 attacks against 11 | One benchmark; one held-out objective class drives the first result |
| 8 | None of the policies of the study of 11 November separates an authorized payment from an unrequested one whose details occur in the user's words | Paired fixtures, Section 4.6.7 | Hand-written cases; mechanism, not prevalence; concerns the tested features, not the request text as such |
| 9 | A deterministic rule that compiles the request and matches operation, recipient and amount completes more benign tasks than REM v1.0 with no more successful attacks | Sections 4.4.3 and 4.6.9: 149 against 105 of 334 and 32 against 18 of 48; 10 against 11 and 3 against 3 attacks | Development evidence; parser written with the benchmark's requests in view; not resolved against rule A2; worse on security than a published fixed-list policy |
| 10 | The learned model adds no demonstrated value to that permission evidence | Section 4.5.3: intervals include zero under both schemes; 38 against 10 attacks under reformatting. Behind the authority guard: 10 attacks under reformatting, gain over the repaired rule with interval lower bounds of zero (Section 4.5.4) | Ridge logistic regression only; one benchmark |
| 11 | Binding each amount to its account removes the successful attacks of the permission rule in user task 15 without losing tasks | Section 4.6.10: 10 → 1 and 3 → 0 successful attacks; G2 − G2 without binding: no task lost | Post hoc with respect to the defects; one task; development evidence |

#### Why benign utility falls

The fall in benign utility has two sources, and the evaluation separates them.

**Where the verdict sends them.** The withheld actions are mostly escalated. Without a reviewer an escalation is a withheld action, so utility falls. The comparison with REM without expected-loss Escalate shows that removing the option does not recover the utility: the same actions are then withheld through Modify. The utility cost is therefore a consequence of the declared costs and of the evidence, not of escalation as such.

**What a reviewer would change.** An escalation is worth something only if someone resolves it. With an oracle reviewer the utility cost disappears, which bounds what a perfect reviewer could recover. A real reviewer would recover less, at some delay and cost. The thesis does not model that reviewer.

#### Why behavioral evidence did not help, and calibration changed little

**Behavioral evidence.** The behavioral indicators are not specific to attacks in this benchmark:
- *privilege escalation* fired on 92% of legitimate state-changing steps, because a user's first transfer is, by definition, the first use of a higher-privilege tool;
- *transition deviation* fired more often on legitimate steps (43%) than on attacks (17%), because legitimate tasks held out from fitting produce unseen transitions.

The estimator gave these features positive weight. In the decision they therefore added to the probability of legitimate high-tier actions, and removing them recovered utility without a measured change in attack success. This is an observation about these features in this benchmark, with short trajectories. It does not show that behavioral evidence is useless elsewhere.

**Calibration.** Calibration changed little (the same 11 successful attacks; 105 benign tasks with it and 110 without it), for two reasons:
- logistic regression fitted by penalized likelihood was already close to calibrated on in-distribution folds, so the fitted map was close to the identity;
- the one fold where calibration mattered, the unseen credential-change attack, was miscalibrated in a way a monotone map fitted on other attack categories cannot repair.

This agrees with the position, taken in Chapter 3, that calibration quality and control quality must be reported separately (C. Zhang et al., 2026).

#### The security–utility frontier that was measured

The arms fall into two groups, not along a ranking. The counts behind this section are in Tables 4.11 and 4.36 (REM, the baselines and the rules) and Tables 4.13 and 4.14 (the published policy and the permission rules); they are not repeated here.

B1 keeps task completion close to the undefended level and removes about three quarters (primary) to 85% (second population) of successful attacks. The other arms bring attack success below 0.5% and lose up to a half of legitimate work. Inside that group the security differences are a handful of episodes. Which group is preferable is a policy question. The declared costs, with a missed attack on a high-consequence action weighted twenty times a false alarm, answer it in favor of the restrictive group; a different institution could answer differently.

No arm dominates on every measure. On the second population every arm with attack success below 0.5% completes at most 64.3% of tasks where the undefended agent completes 68.7%. The two arms nearest to the undefended level of task completion are deterministic rules that use what the user or the environment permits: a published fixed list of payees, and the request-derived permission rule.

#### The limiting factor is what the evidence represents

Three results of the studies up to 11 November point the same way. REM's estimator discriminates well, yet a one-feature rule matches its security. A more elaborate policy, supervised on outcomes and given authorization features, did worse. And on paired fixtures every tested policy that releases legitimate payments also releases an unrequested payment that uses the user's own words. In each case the evidence described where the arguments of a call came from and not what the user asked for. The conclusion is limited to the features and policies that were tested: with them, neither a better estimator nor a more elaborate decision rule moved the frontier.

The extension study of 13 November tested the complementary proposition. A deterministic parser of the request, with typed matching of operation, recipient and amount, moved the frontier on development data: more legitimate calls released, no more successful attacks than REM v1.0, and most of the paired fixtures right (Sections 4.4.3 and 4.6.9). The improvement came from the representation of the request used as a hard rule. A learned model on the same representation added nothing that could be demonstrated and was less robust (Section 4.5.3). Three limits remain. The parser was written with the benchmark's requests in view. Requests that delegate the operation itself to a file stay unresolved. And a user task whose own payee is the attacker's account cannot be resolved from the request at all.

REM's threat model gives it one trusted input, the user's request as text. The published approaches that report both low attack success and high utility add something REM does not have: a trusted policy or authorization record (aiAuthZ, at abstract level), trusted observations that license an action (Yan et al., 2026), a language model that judges task alignment (F. Jia et al., 2025), or enforcement on effects at the system boundary (Kairos, at abstract level). Of these, this thesis ran only a fixed-list policy published with Progent, in replay (Section 4.4.3); it does not claim that the others would succeed on these episodes. A trusted authorization record would remove the dependence on parsing free text, and remains the principal future work.

#### What the evidence does not support

- **That REM protects live agents.** Under replay a withheld call does not reappear. A live agent can retry, rephrase or reach the goal through another tool.
- **That REM, in either version, is better than simple rules.** On the second population neither version is distinguishable from the rules, and one rule completes more tasks.
- **That REM is deployable as configured.** Without a reviewer, REM v1.0 completes 18 of 48 benign tasks where the undefended agent completes 38, and REM v1.1 completes 25.
- **That the four verdicts are useful as four.** In this evaluation Modify, Escalate and Block coincide.
- **That REM is superior to any published defense.** The one published policy that was replayed has no successful attack and completes more tasks than either REM version. No defense that needs a language model was run.
- **That the tested provenance features identify what the user authorized.** On the paired fixtures they did not. Whether a model or a parser can recover authorization from the request text in general is not settled by this thesis: one deterministic parser did so for most of the author-written cases and failed on some.
- **That the learned core of REM is what improves the trade-off.** In every comparison of this chapter, the gains came from removing evidence, from simple rules, or from a deterministic permission rule.
- **That the permission rule generalizes.** It was developed and evaluated on the same sixteen requests and on fixtures written by its author, and its repairs were written after its defects and results were known.
- **That the security differences among the restrictive arms are general.** Without user task 15 every restrictive arm has no successful attack (Section 4.6.10).
- **Anything about the injection classifier**, which was not available, or about adaptive attackers, who were out of scope.

### 4.6.12 Threats to Validity and Limitations

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

11. **Reuse of the recordings.** The primary recordings were used for fitting, cross-validation and many analyses. Only the confirmatory run of 11 November was made on recordings unread at the time, and it tests one contrast. Since that run the second population is development evidence too, and the extension study has no confirmatory part.
12. **Tasks are not new anywhere.** The second population has new agents and templates and the same sixteen user tasks and nine attack objectives. A few user tasks decide each utility comparison.
13. **Author knowledge.** The rules, the authorization evidence, the request parser of the extension and the fixtures were written by an author who knew the benchmark's tasks. For the parser this is the main threat: no request was held out from its development, and its only test on other requests is a set of twenty author-written pairs that nobody else reviewed.
14. **Fixtures.** They are hand-written, were scored with one fold's models, and show mechanisms, not rates.
15. **Three close works were not read in full.** NEXUS and aiAuthZ are known from their abstracts and from their authors' repositories; Kairos from its abstract. Progent and CaMeL are known from their official repositories. Statements about them may change when the papers are read.
16. **One published policy was replayed, and no defense that needs a language model was run.** The equivalence of the replayed decision function with Progent's own checker rests on reading its code and on a differential check of 468 argument cases reported by an independent review; the Progent framework itself was not run. No statement about the relative performance of REM and model-based defenses is supported.
17. **Repairs after results.** The repaired rule of Section 4.6.10 was written after the original rule's results, its defects and the composition of user task 15 were known. Its results cannot be read as an independent test.

### 4.6.13 Chapter Summary

This chapter reported an evaluation of REM on recorded trajectories of real agents in the AgentDojo banking environment. No live agent was run.

- **Environment and training.** Python, NumPy and AgentDojo 0.1.35 on four CPU cores; no model call. The estimator has nine parameters and is trained once per fold in a nested, grouped procedure.
- **Prediction.** On attack objectives not seen in fitting, the calibrated estimator reaches a held-out ROC-AUC of 0.938. Calibration left the probabilities almost unchanged and did not repair the one miscalibrated fold; without it the attack count is the same and five more benign tasks are completed.
- **Replay on the primary recordings.** REM v1.0 reduces attack success from 22.6% to 0.4% and benign task completion from 52% to 31%. It releases 33 of 178 authorized state-changing calls.
- **Rules.** Rules that use one or two pieces of provenance evidence and no model reach the same security with 40% to 42% benign task completion. One of them fails when the attacker's identifier is reformatted.
- **Generalization.** REM v1.0's attack count and benign task count do not change when the user task is also held out. A candidate policy supervised on intervention outcomes with authorization features was rejected: 132 successful attacks against 11.
- **Confirmatory run.** On 2,113 episodes unread before that run, REM without behavioral evidence completes 7.5 percentage points more tasks than REM v1.0 (95% interval 1.2 to 16.0) with 1 successful attack against 3. The pre-declared decision rule gives GO; this is not a test of non-inferiority on security. Neither version is distinguishable from the rules.
- **Published policy.** Progent's manual banking policy, replayed on the same episodes, has no successful attack and completes more tasks than either REM version; it permits no password change.
- **Exploratory extension.** A deterministic permission rule compiled from the user's request completes more benign tasks than REM v1.0 with no more successful attacks (development evidence). Its advantage over the strongest simple rule is not resolved, and it is worse on security than the published policy. A learned model on the same evidence adds no demonstrated value. The gain belongs to the rule, not to the learned core.
- **Follow-up.** Three defects of the rule were found by an external review and repaired. The repaired rule has 1 and 0 successful attacks and loses one user task whose condition it does not evaluate; it is not resolved against A2 or the published policy. An authority guard removes the learned model's robustness failure; the model's gain is still not established.
- **Limit.** The provenance features of REM do not represent what the user asked for; the request parser of the extension was developed on the benchmark's own requests.
- **Not done.** Live-agent runs; any defense that needs a language model; a human label audit; repeated runs; an independent review of the fixtures.

Chapter 5 draws the conclusions.
