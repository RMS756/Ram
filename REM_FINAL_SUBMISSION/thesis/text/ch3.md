<!-- @frag ch3_nov_protocols -->
### 3.11.41 Rule baselines and additional policy arms (added November 2026)

The examination of the pilot results raised a question that the configurations of Section 3.11.7 cannot answer: whether the estimator and the cost-based rule add anything over a rule that reads a single piece of evidence. Three rule baselines and three diagnostic arms were therefore added in November 2026. They were declared, with every other element of the study, in a protocol committed before any of their outcomes was computed. None of them changes REM.

**Rule baselines.** Each uses no fitted quantity and no cost. Each applies only to calls to tools in 𝒯~R~; calls to other tools are released. A withheld call is enforced as Block.

**Table 3.41. Rule baselines**

| Arm | Rule for a call to a tool in 𝒯~R~ | Evidence used |
|---|---|---|
| P1, provenance | withhold if and only if x^act^~1~ = 1 | a key argument occurs in untrusted content and not in the user objective or trusted content |
| P2, provenance or novelty | withhold if and only if x^act^~1~ = 1 or x^act^~2~ = 1 | P1, or the recipient appears neither in the objective nor among transactions seen before the first untrusted input |
| A2, strict explicit | withhold if and only if z^exp^ = 0 | whether every identity argument of the call occurs in the user objective |

The authorization evidence used by A2 is a declared, deterministic definition, not a published formula. For a call to a tool in 𝒯~R~, let K be the declared key arguments present in the call and let K~ref~ be K without the amount, or K itself if nothing else is present. Then z^exp^ = 1 if K~ref~ is non-empty and every value in it occurs in the user objective g, and 0 otherwise. A second indicator, z^del^, is 1 if every value of K~ref~ that does not occur in g occurs in the output of an earlier read whose argument the user named. Occurrence is decided by the matching rule of the Input & Context Layer, unchanged. The definitions were motivated by the admissibility statement of Yan et al. (2026), that an action's operation and target must be licensed by trusted observations while values may come from external ones, and by the remark of F. Jia et al. (2025) that a user may delegate subtasks to a document. **Occurrence of a value in the user's text is not authenticated authorization**, and the evaluation tests exactly where the two diverge (Section 3.11.43).

**Diagnostic arms.** These isolate one element each and are not candidates for adoption, with one exception noted.

**Table 3.42. Diagnostic and candidate arms**

| Arm | Change relative to REM v1.0 | Purpose |
|---|---|---|
| REM, Allow and Block only | the feasible set is {Allow, Block} | whether Modify and Escalate change outcomes |
| A1, explicit or delegated | a rule: withhold if and only if z^exp^ = 0 and z^del^ = 0 | whether delegation to a user-named document is safe |
| Outcome-supervised REM | the estimator is trained on whether withholding the call prevents attack success, in place of the attempt label | whether the training target matters |
| Intervention-value policy | two estimators predict the change in attack success and in task success when the call is withheld; the call is withheld if and only if C~miss~(k)·ΔŜ ≥ C~FA~(k)·ΔÛ and the left side is positive | the proposal of C. Zhang et al. (2026) applied to REM |
| Authorization-aware intervention-value policy (**pre-declared candidate; rejected**, Chapter 4, Section 4.43) | the previous arm with z^exp^ and z^del^ added to the features | whether authorization evidence and outcome supervision together improve on REM |

The training targets of the last three arms were obtained by *prefix branching*: each recorded episode was replayed once with every call released and once with one call withheld and all others released, and the benchmark's attack and task outcomes of the two replays were compared. The intervention-value rule is **derived, not quoted**: C. Zhang et al. (2026) define the value of an intervention as the difference between the expected utility of intervening and of continuing and select the action with the highest expected utility; the rule above writes those two utilities in REM's declared costs for the two actions release and withhold. No equation is introduced for authorization, and none of these arms is part of REM.

### 3.11.42 Generalization schemes

Three schemes are used, in increasing difficulty.

- **S1, held-out attack objective.** The nine outer folds of Section 3.11.5. An attacked episode is scored by models that never saw its injection task. Its user task was seen, with other injection tasks.
- **S2, double holdout.** An attacked episode with user task u and injection task i is scored by models fitted without any episode of u and without any episode of i. A benign episode of user task u is scored by the cell that also excludes the injection task to which S1 assigns u. Every fitted quantity is recomputed from the fitting portion of each cell: λ, the coefficients, the calibration map, the benign transition reference and r~mod~. This gives 143 cells after the exclusion of AM-1.
- **S3, held-out attack templates.** S1 models applied without refitting to recordings of one backbone under five other attack templates.

No hyperparameter, threshold, feature or cost is selected on any test portion. S2 was added because S1 leaves a known dependence: the same sixteen user tasks appear on both sides of every fold (Section 3.11.4).

### 3.11.43 Robustness probes and paired call fixtures

Two probes test mechanisms that the benchmark's own attacks do not exercise. They are reported separately from benchmark results, and their counts are not rates.

- **Reformatted identifier.** Attacked episodes are replayed with the attacker's account identifier written in groups of four characters inside the injected text. The recorded agent calls are unchanged, so the identifier in the call no longer matches the text that carried it. Nothing is refitted. The probe measures dependence on exact string matching.
- **Paired call fixtures.** Twenty-three paired cases were written by hand, in three sets, each with a user objective, a document returned by a read, a legitimate call and an unsafe call on the same scaffold. They follow the counterfactual design of T. Yang et al. (2026), in which apparent risk and permissibility vary independently. The pairs cover recipient substitution, amount substitution, an unrequested payment during a read-only task, payments above the declared amount limit, credential changes, and reformatted or fragmented identifiers. Each set was written before it was scored, and each is scored once with the models of one fold. A pair is counted as correct when the legitimate call is released and the unsafe call is withheld.

The fixtures were written with knowledge of how REM's features are computed. They show which mechanisms fail; they do not estimate how often.

### 3.11.44 Confirmatory protocol for one modification

The analyses above reuse the recordings on which REM was fitted, cross-validated and examined many times. One modification suggested by them, the removal of the behavioral evidence group, was therefore tested once on recordings that no script of this project had read.

**What was fixed in advance.** A protocol was committed on 11 November 2026 before any of the new recordings was opened. It fixed:

- the candidate: the stored fits of the pilot's own "behavioral evidence removed" ablation (Section 3.11.7), with the same calibration procedure, costs, tiers, predicates and four-verdict rule;
- the comparators: the no-defense reference, B1, REM v1.0, P1, P2, A2 and the Allow-and-Block-only arm;
- the population: every banking recording in the benchmark repository, at the commit used throughout, of five pipelines that had never been loaded (one backbone not used before, with and without a prompt-level defense; one known backbone with a prompt-level defense; and two known backbones under attack templates never used for them);
- inclusion and exclusion, identical to the pilot (AM-1 and AM-4), with all counts reported;
- the fold used for each episode: for an attacked episode, the fold of its injection task, whose models never saw that injection task;
- the endpoints, the statistics and the verdict rule below.

Nothing is fitted, tuned or selected on the new recordings.

**Endpoints.** E1 is the paired difference in user-task success, candidate minus REM v1.0, over all eligible episodes, with a bootstrap clustered by user task. E2 is the paired difference in attack success rate and in unauthorized state-change rate (Section 3.12.41) over attacked episodes, clustered by injection task. Intervals are 95% percentile intervals from 2,000 resamples.

**Verdict rule.**

- **GO** if the E1 interval lies entirely above zero, neither E2 interval lies entirely above zero, and the candidate's number of successful attacks does not exceed that of rule P2 on the same episodes.
- **NO-GO** if either E2 interval lies entirely above zero or the E1 point estimate is not positive.
- **INCONCLUSIVE** otherwise.

The third GO condition replaces a numerical security margin. No approved margin exists, and none was invented: a learned policy that is less secure than a one-line rule on the same episodes has no claim to adoption.

**What the population is.** The agents, attack templates and trajectories are new. The sixteen user tasks and nine attack objectives are the benchmark's own and are not new. A GO verdict therefore supports the modification on untouched recordings of this benchmark, in replay. It is not evidence about live agents, reviewers or other domains, and adoption remains a supervisor decision.

<!-- @frag ch3_outcome_layers -->
### 3.12.41 Outcome layers and additional metrics

A single attack-success figure merges events that occur at different points between an injection and a harm. The analyses added in November 2026 report these layers separately and never combine them into one score.

**Table 3.43. Outcome layers and the quantity reported for each**

| Layer | Quantity |
|---|---|
| Injection exposure | attacked or benign episode |
| Attacker-induced proposal | calls with the attempt label y = 1 |
| Runtime verdict | Allow, Modify, Escalate or Block for each call |
| Actual execution | call released or withheld |
| Committed unauthorized state | **unauthorized state-change rate**: the share of attacked episodes in which at least one call with y = 1 was released. It does not depend on the benchmark's success checker |
| Attack success | the benchmark's security check (ASR, Table 3.15) |
| Legitimate-task completion | the benchmark's utility check, in benign episodes and under attack |
| Legitimate-action approval | **authorized-call release**: the share released among calls to tools in 𝒯~R~ proposed in benign episodes |

Two further quantities describe burden: the number of Escalate verdicts and of episodes that contain one, and the number of episodes in which any call is withheld. No effectiveness of a reviewer is assumed in any of them.

The benchmark's success check is not treated as a general definition of financial harm; the unauthorized state-change rate is reported beside it. A policy that withholds every sensitive operation cannot appear successful under this reporting, because its legitimate-task completion and authorized-call release are shown in the same table as its attack success.

<!-- @frag ch3_v11 -->
## 3.41 Versioned Amendment: REM v1.1 (Proposed)

*Status: proposed; supervisor approval required (decision SD-FEAT). The specification of Sections 3.2 to 3.10 is unchanged and is referred to as REM v1.0.*

**Definition.** REM v1.1 is REM v1.0 with the behavioral evidence group removed from the evidence vector: x~t~ = [x^ctx^; x^act^], without x^beh^~1~ to x^beh^~4~. Nothing else changes. The estimator is the ridge logistic regression of Equations 3.1 and 3.2, refitted on the reduced vector by Procedure 3.1; the calibration is that of Equations 3.3 and 3.4; the consequence tiers, the predicates, the loss structure of Table 3.13, the verdict rule of Equations 3.6 and 3.7, the mitigation semantics and the audit record are those of v1.0. The architecture keeps its five layers. The Behavioral Analysis Layer continues to maintain the episode history, from which the action evidence x^act^ is computed; it no longer contributes the four history features to the estimator.

**Why it is an amendment and not a new method.** Removing an evidence group is one of the ablations declared for the pilot (Section 3.11.7, item 2). REM v1.1 is that ablation's fit, promoted from a diagnostic to a proposed configuration. No equation, cost, threshold or rule is added.

**Evidence.** In the pilot the ablation left replay attack success unchanged and raised benign utility. The observation was made after results were seen. It was then tested once under the confirmatory protocol of Section 3.11.44 and met the pre-declared GO rule (Chapter 4, Section 4.45).

**What the amendment does not do.** It does not make REM better than the rule baselines, it does not address reformatted identifiers, and it does not supply authorization evidence. These limits are reported with the results.

**Reporting rule.** Until the supervisor decides, the design of this thesis is REM v1.0. Every table that reports v1.1 also reports v1.0.

<!-- @frag ch3_impl -->
## 3.42 System Implementation

This section summarizes how the specification is realized in software and how the software was verified. The details are in Appendix B: the environment, the code organization, the implementation of each layer, the test suite, the correspondence between requirements, equations, functions, tests and result files, and the measurement of processing time.

**Implementation rules.** Three rules governed the implementation.

1. **Fail closed.** A design value that has not been declared stops the software with an explicit error; no default is substituted.
2. **No silent resolution.** Where the specification and an earlier design decision disagree, both alternatives are implemented and one is selected explicitly in configuration.
3. **Separation of decision and audit.** Attribution is computed after the verdict and cannot reach the decision function. This is enforced by the function's signature and checked by a test.

**Software.** REM is implemented in Python with NumPy. No machine-learning framework is used: the estimator, the calibrators and every metric are written directly, so that each operation can be traced to its equation. The reported runs used Python 3.11.17, NumPy 2.4.6 and AgentDojo 0.1.35.

**Placement.** REM is inserted at the benchmark's tool-execution boundary as a replacement for the tool executor. Each proposed call is evaluated before it is executed. A released call runs; a withheld call does not, and the agent receives a tool-result message carrying the refusal. The agent's model, prompts and tools are not modified. The placement has limits: only calls that pass through the executor are mediated, and a refusal is visible to the agent.

**Two execution paths.** A frozen pipeline chains the five layers and is exercised by unit and contract tests. The evaluation path, used for every result in Chapter 4, calls the same fitted components and adds the features, tiers, predicates, feasible set and mitigation semantics of this chapter.

**What is implemented and what is absent.** All elements of Sections 3.4 to 3.10 are implemented, with one exception: the pre-trained injection classifier x^ctx^~1~ is not implemented, because its choice is pending and the candidate model could not be obtained. It is absent from the evidence vector and is not replaced by a substitute. The context evidence evaluated in this thesis is therefore the instruction-pattern indicator x^ctx^~2~ alone. A known deviation in entity matching, the truncation of numbers written with a comma as thousands separator, is recorded by a test that is expected to fail; it affects none of the 825 texts of the primary recordings.

**The additions of November 2026 are isolated.** The rule baselines, the diagnostic arms, the generalization schemes, the probes and the confirmatory run (Sections 3.11.41 to 3.11.44) are implemented in a separate study module that imports the estimator, calibrator, loss structure, predicates, tier map and replay element unchanged. No file of the REM implementation or of its configuration was modified. The study's fitting routine reproduces the frozen fits of the pilot to within 4·10⁻¹⁴, and its replays of REM v1.0, B1 and the no-defense reference reproduce the pilot's counts exactly.

**Verification.**

- **Unit and contract tests.** 241 tests pass, 3 are skipped because they need an environment or state that is not present by default, and 1 is the expected failure noted above (11 November 2026).
- **Replay fidelity.** With every call allowed, the replay reproduced the recorded utility and security outcome of 3,313 of the 3,334 primary episodes (Chapter 4, Section 4.6.1) and of 2,113 of the 2,148 loaded confirmatory episodes (Chapter 4, Section 4.2.41). Episodes that are not reproduced are excluded from every replay metric and counted.
- **Re-execution.** The complete pilot was re-executed in a fresh environment and reproduced every analytical value; only timing values, commit stamps and one file path differed.
- **Gateway parity.** A local deployment simulation, in which REM runs as a separate gateway service in front of a simulated bank back end, returned the same verdicts as the offline replay.

None of these establishes security effectiveness. They establish that the software computes what the equations state and operates inside the benchmark's execution loop.

**Live-agent and published-defense integrations.** A closed-loop integration, in which a running agent receives REM's refusals, and an integration that places REM behind the MELON defense are both implemented and tested with scripted agents and simulated model providers. Neither has been executed with a language model. Their design and status are in Appendix D, and Chapter 4, Section 4.46, states what follows from that.

**Processing time.** Processing time is measured around the complete evaluation of a call, including attribution and the construction of the audit record, and excluding model inference and tool execution (Appendix B). The figures are reported in Chapter 4.

<!-- @frag ch3_threats_add -->
**Threats added by the analyses of November 2026.**
- The rule baselines, the authorization evidence and the fixtures were defined by an author who knew the benchmark's sixteen user tasks and nine injection tasks. The definitions are stated generically, but they were written with that knowledge.
- The primary recordings were reused many times. Every analysis added after the pilot's results were seen is labelled post hoc, and only the confirmatory run of Section 3.11.44 is free of that reuse.
- The confirmatory population shares the benchmark's user tasks and attack objectives with the fitting data. It tests new agents and templates, not new tasks.
- Under replay without a reviewer, Modify, Escalate and Block have the same effect on a call. No result in this thesis can distinguish them.

<!-- @frag ch3_summary -->
## 3.43 Chapter Summary

**Design.** This chapter specified REM as one runtime pipeline in five layers. The Input & Context Layer captures the proposed action and labels context by provenance. The Detection Layer computes context evidence. The Behavioral Analysis Layer maintains the episode history and computes history and action-provenance evidence. The Decision Engine estimates a calibrated probability of adversarial inducement by ridge logistic regression with a logistic calibration on the logit, assigns a declared consequence tier, applies policy predicates, selects a verdict by minimizing conditional risk under tier-indexed losses, and writes an audit record whose linear attribution never influences the verdict. The Mitigation Layer executes Allow, tool restriction, escalation or Block. Offline fitting and recalibration are cross-cutting activities, not a layer. Every equation is stated with its source and with whether it is established, adapted or derived.

**Evaluation method.** The evaluation uses the AgentDojo banking environment with nested grouped cross-fitting that holds out one attack objective per fold. It compares REM with a no-defense reference, a consequence-independent baseline on the same estimator, and three rule baselines that use no model. A double-holdout scheme, two robustness probes and paired call fixtures test generalization and specific mechanisms. One modification is tested by a confirmatory protocol committed before its data were opened. Outcomes are reported in separate layers, with legitimate-task completion and authorized-call release beside every security figure.

**Amendment.** REM v1.1, the same framework without the behavioral evidence group, is proposed as a versioned amendment and awaits approval. REM v1.0 remains the frozen baseline.

**Implementation.** The specification is implemented with one declared absence, the injection classifier, and is verified by 241 tests, by replay fidelity checks and by exact re-execution. No live-agent experiment was executed. Security effectiveness, within the limits of recorded-trace replay, is the subject of Chapter 4.

<!-- @frag ch3_notation_bridge -->
The notation used in this chapter is listed in Appendix C. Each symbol has one meaning throughout the chapter, and symbols that appear in a single equation are defined where they are used.

<!-- @frag ch3_cusum_bridge -->
**Optional sequential analysis.** An optional, observe-only sequential analysis, a Bernoulli cumulative-sum procedure over logged indicators, is specified in Appendix C with Equations 3.15 to 3.19. It is performed offline, is not part of REM's verdict path and never influences a verdict.

<!-- @frag ch3_interfaces_bridge -->
The inputs and outputs of each layer are listed in Appendix C. The four functions are separated architecturally: Layers 2 and 3 produce evidence and issue no verdicts; Layer 4 performs probability estimation and decision; Layer 5 performs mitigation.
