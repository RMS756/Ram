<!-- @frag ch2_structure -->
**Chapter structure.** Section 2.2 reports the review methodology. Sections 2.3 to 2.5 cover agent risk, threats, benchmarks and threat models. Section 2.6 organizes defenses by where they intervene, and Section 2.7 examines runtime monitoring, behavioral evidence and provenance. Section 2.8 reviews the statistical foundations of a runtime decision layer; the REM specification itself is left to Chapter 3. Section 2.9 examines how runtime systems decide and mitigate, and Section 2.10 separates financial-agent evidence from general evidence. Sections 2.11 and 2.12 compare and synthesize the evidence. Section 2.13 states the research gap, positions REM, records the limitations of the review and reports three dated literature updates that lie outside the systematic review. Section 2.14 summarizes the chapter.

<!-- @frag ch2_nexus -->
### 2.9.3 NEXUS: calibrated risk scoring with a four-way intervention set

NEXUS (Hossain et al., 2026; MODERATE EVIDENCE; PARTLY UNVERIFIED) is the closest prior art to REM's *decision* component. It passed the inclusion criteria through the other-methods stream as a preprint. It has since been published in the Findings of AACL 2026; the published record was checked on 11 November 2026. **The full text has not been read in either version.** Three sources below the level of the paper are used, and each statement names its source:

- **A**: the abstract of the published version (index record, 11 November 2026);
- **A0**: the abstract of the preprint (index record, 28 October 2026);
- **R**: the README of the authors' public repository (retrieved 1 November 2026; a copy and its SHA-256 are kept in the verification records). Repository documentation can differ from the paper.

**Architecture (A, R).** NEXUS is a structured-plan safety monitor that "applies a formal intervention policy" to select among allow, block, request confirmation and request revision. It combines deterministic safety rules, argument-level inspection and a *calibrated* logistic-regression risk score used for graded escalation. According to the README, the policy selects one intervention per plan, and the score is trained on a nine-dimensional plan feature vector.

**Decision policy (R).** The README states the policy explicitly: Block if any critical violation, or if the risk score ρ ≥ τ~b~ with at least one violation; Confirm if ρ ≥ τ~c~ or any high-severity violation; Revise if any medium-severity violation; otherwise Allow. It states that (τ~b~, τ~c~) = (0.75, 0.70) was selected on a safety–utility loss L(Π) = E[λ~s~u~s~ + λ~o~u~o~ + λ~c~c(Π(P))] over a 5×5 grid of (λ~s~, λ~o~), and that Platt scaling, fitted on a 60-instance calibration split, reduced ECE from 0.085 to 0.013 on the 128-instance test split.

**Results (A).** On a 128-instance synthetic benchmark the published abstract reports F1 of 0.949 and four-class intervention accuracy of 0.6406, 27.3 percentage points above rule-only selection. On R-Judge it reports F1 0.861 against 0.849 for rule-only; it matches rule-only on AgentHarm; and it reports 0% ASR at 99% control allow on an indirect-injection set. On its rule-blind stress set it reports F1 0.897 with a Revise recall of 0.500, and a median latency of 0.38 ms. The preprint abstract (A0) gave 0.881 and 0.205 ms for the last two figures, and the README gives different headline figures for a retrained scorer (for example F1 0.965 on the synthetic test split). The published abstract's figures are used here, and the differences are recorded rather than resolved. The README adds that on rule-blind plans the policy predicts only Allow or Block.

**Still unverified (level U).** The intervention costs, the definitions of the nine features and of the consequence annotations read by the rules, the session manager, and the limitations stated by the authors.

**What REM cannot claim.** NEXUS already provides calibrated logistic risk scoring, a formal policy over a four-way intervention set with confirmation and revision routes, a loss criterion for selecting its thresholds, and sub-millisecond latency.

**Where the difference lies.** Three differences can be stated at levels A and R:

- **Point of evaluation.** REM evaluates each proposed tool call during execution, with the episode history; NEXUS judges a structured plan.
- **Decision rule.** REM selects each verdict by minimum expected loss, with losses indexed by the consequence tier of the call, so the boundaries between verdicts move with consequence. NEXUS applies a rule-first cascade with two score thresholds chosen once by a loss criterion; consequence enters through rule severities.
- **Evaluation.** REM is evaluated by replaying recorded trajectories of real agents in an executable banking environment and scoring outcomes. NEXUS's headline results score plans against labeled interventions on a synthetic benchmark, with R-Judge, AgentHarm and an injection set as additional evaluations.

Whether any of these differences changes outcomes is an empirical question. NEXUS was not run in this thesis: its code was not available in the execution environment, and no valid adapter from a banking tool call to its plan representation exists (Chapter 4, Section 4.16).

<!-- @frag ch2_update_nov11 -->
### 2.13.41 Literature update of 11 November 2026: full-text readings (outside the PRISMA flow)

**Status of this addition.** On 11 November 2026 six papers were read in full from PDF files supplied by the author, whose SHA-256 values are kept with the study records. **This is the only place in this chapter where a full text was read.** The update is not part of the PRISMA flow. No count in Table 2.2 or Figure 2.1 changes, and no screening record is created retrospectively. Two of the six (Task Shield and MELON) are included studies of the review; three (PROVISO, CASEL, and the paper of C. Zhang et al.) were known from records; one (AgentBoundary) is new. Three further works are described from their abstracts only and are marked so. No systematic search to this date was possible, and newer competing work may exist.

**Table 2.41. Works examined in the update of 11 November 2026 (F = full text read; A = abstract only)**

| Work | Level | What it does | Evaluation | Statement most relevant to this thesis |
|---|---|---|---|---|
| PROVISO (Yan et al., 2026; preprint) | F | Decides at the commitment point, after an action is proposed and before it is executed. Observations are typed by provenance into trusted and external. A trained controller estimates the value of the proposed and of an alternative action and commits the higher, after subtracting an offset chosen on development data | AgentDojo, four suites, by rolling out both continuations in a restored environment; folds keep all attack variants of a user task together | The controller is "fitted separately for each benchmark and therefore requires labeled outcomes from the target setting; we do not study transfer of a single trained controller across tasks" |
| AgentBoundary (T. Yang et al., 2026; preprint) | F | Counterfactual task families that vary apparent risk and permissibility independently on the same workflow; reports authorized-task completion and unsafe behavior separately | 17 agent configurations on general agent tasks | "high safety frequently coexists with poor authorized-task completion" |
| Calibration Is Not Control (C. Zhang et al., 2026; preprint, header states NeurIPS 2026) | F | Defines the value of an intervention as the difference between the expected utility of intervening and of continuing; proves that a strictly increasing recalibration of a score preserves the class of threshold policies | Prefix branching on agent benchmarks; no security benchmark | A risk score is sufficient for control only if the sign of the intervention value can be recovered from it |
| CASEL (Y. Zhang et al., 2026; preprint) | F | Selects among six execution modes by minimizing a per-mode cost that multiplies a failure probability by a consequence and adds mode costs | Simulation only | "Intervention effectiveness is assumed, not measured"; the per-mode cost "does not reduce harm beyond a product-score gate" |
| Task Shield (F. Jia et al., 2025; ACL) | F | Requires every instruction and tool call to contribute to a user-level task; contribution is scored by a language model | AgentDojo, live agents | A tool output may legitimately define subtasks when the user delegates to it |
| MELON (Zhu, Yang, et al., 2025; ICML) | F | Re-executes the step with the user prompt masked and flags an attack when the resulting tool calls remain similar | AgentDojo, live agents | Reported benign utility with GPT-4o falls from 80.41% to 68.04% |
| aiAuthZ (Kodathala, 2026; preprint) | A | An off-host gateway that enforces identity-bound, argument-level authorization policy on tool calls | AgentDojo banking, per its abstract | Blocks all seven attacker-directed calls "at the cost of one legitimate first-time payment" |
| Kairos (Hempel et al., 2026; preprint) | A | A reference monitor at the isolation boundary that defers and checks effects | AgentDojo, per its abstract | Attack success 47.0% to 2.7% with benign utility at the undefended level |
| NEXUS, published version (Hossain et al., 2026) | A | See Section 2.9.3 | — | — |

The figures in Table 2.41 come from different agents, suites, attack sets and evaluation modes. They are listed to show what each work reports and are not compared with one another or with REM.

**What the update changes.**

- **The decision form is published.** CASEL's per-mode cost has the same structure as REM's expected-loss rule: a residual-risk term for each mode and a cost for choosing it. Together with NEXUS, this removes any claim that combining a risk estimate with consequence to choose among graduated responses is new.
- **Calibration is known not to be the lever.** C. Zhang et al. give the formal reason why recalibrating a score, or re-thresholding it, cannot recover a distinction that the score lacks. Their intervention-value target was tested in this thesis and failed on an unseen attack objective (Chapter 4, Section 4.43).
- **Over-defense is a general finding.** AgentBoundary measures at scale what this thesis measures for REM: safety obtained by withholding authorized actions.
- **Stronger utility is reported by heavier or differently placed mechanisms.** PROVISO, Task Shield and MELON report higher utility than REM reaches in replay, with a trained controller and restored rollouts or with a language model in the decision path. Kairos and aiAuthZ, at abstract level, act at the system boundary or add a trusted authorization channel. None was run under the conditions of this thesis.
- **Authorization needs a trusted input.** aiAuthZ, at abstract level, and PROVISO's admissibility rule both rest on trusted statements of what is authorized. REM's threat model has only the user's request as text.

### 2.13.42 Revised statement of the research gap

The statement of Section 2.13.2 was written from the records of September 2026. It framed the gap partly as the absence of a combined evaluation of a calibrated, consequence-aware decision. After the update of Section 2.13.41 the mechanism side of that statement is closed, and the gap is restated as follows. It is proposed wording, pending the supervisor's confirmation.

> Runtime defenses for tool-using agents now combine risk scoring, provenance and graduated interventions, and their authors report benchmark-specific fitting and unmeasured intervention effectiveness. Limited controlled evidence establishes whether a learned, consequence-aware runtime decision adds value over simple provenance and authorization rules for a banking agent when both the user task and the attack objective are unseen, and at what cost in legitimate task completion.

**Table 2.42. Assessment of the revised gap statement**

| Criterion | Assessment |
|---|---|
| Supported by recent literature | PROVISO states that transfer of its fitted controller is not studied, and it holds out user tasks, not attack objectives. CASEL states that intervention effectiveness is assumed. AgentBoundary reports widespread over-defense. None of the six papers read in full compares a learned monitor with parameter-free rules on the same trajectories. For NEXUS, aiAuthZ and Kairos this is known only from abstracts |
| Distinct from published work | As an evidence gap, yes. As a mechanism gap, no: every mechanism involved is published |
| Specific | It names the class of system (a monitor without a language model in the decision path), the domain, the comparison and the conditions |
| Answerable by experiment | Yes, by recorded-trace replay with held-out objectives and tasks (Chapter 3, Sections 3.11.42 and 3.11.44) |
| Falsifiable | Yes. The statement "the learned policy adds value over the rules" is a paired contrast with an interval, and the data could have supported it |
| Consistent with the results | Yes. The answer obtained is largely negative (Chapter 4, Section 4.45) |

**Bounds.** The gap is bounded by the record-level review, by the absence of a systematic search after 30 October 2026, and by the abstract-level knowledge of three close works. A study that reports a held-out-objective comparison of a learned monitor with rule baselines on banking tasks would require the statement to be revised.

<!-- @frag ch2_summary_gap -->
**The gap.** The gap stated from the systematic review concerned the evaluation of a calibrated, consequence-aware decision at the action boundary of a financial agent. Full-text readings in November 2026 showed that the decision form itself is published (NEXUS; CASEL) and that its known weaknesses are documented (C. Zhang et al.; AgentBoundary). The gap was therefore restated as one of evidence (Section 2.13.42): whether a learned, consequence-aware runtime decision adds value over simple provenance and authorization rules for a banking agent under unseen user tasks and attack objectives, and at what cost in legitimate task completion. Every mechanism involved is established. Only the controlled evaluation, including its negative results, is offered by this thesis.

Chapter 3 specifies the REM methodology through which the gap is addressed.

<!-- @frag ch2_bridge_eligibility -->
**Eligibility.** A study was included when it met six criteria fixed before assessment: it concerns tool-using AI agents or LLM-integrated applications that ingest untrusted content; it addresses a security, safety, robustness, monitoring or misuse problem; it makes a substantive technical or empirical contribution; it informs at least one dimension relevant to REM; it gives enough information to extract that contribution; and it was published between January 2019 and 25 September 2026, or is a necessary foundational source. Secondary studies were not synthesized as primary evidence. The full criteria and the exclusion labels are in Appendix A.

<!-- @frag ch2_bridge_agent_risk -->
**Why agents change the problem.** Three structural properties distinguish agent security from the security of a stand-alone model: several input channels of different trustworthiness enter the same context; state persists across a trajectory, so content read at one step can shape an action several steps later; and outputs include tool calls with external effects. Benchmark studies show that these properties matter empirically (Wei et al., 2026; Ruan et al., 2024). The background on agent architecture, and the evidence on tool-channel threats, memory poisoning and multi-step drift, which lie outside the threat model evaluated in this thesis, are in Appendix A.

<!-- @frag ch2_bridge_defenses -->
Two families that act before the action boundary are summarized here and reviewed in Appendix A. *Input- and model-level protection* (detectors of embedded instructions, input transformation, and training the model to follow only the prompt channel) reports strong in-distribution results but acts on text, not on actions, and has been bypassed by adaptive attacks (J. Shi et al., 2026; Y. Zhang et al., 2024). *System-level and information-flow defenses* change the architecture so that untrusted data cannot steer control flow; their guarantees hold for the threat models their authors formalized, and one such design was later defeated by new attacks (Y. Wu et al., 2025; E. Li et al., 2026).

<!-- @frag ch2_bridge_foundations -->
The reasons for choosing logistic regression as the estimator, and the classical basis of sequential change detection, which REM uses only as an optional observe-only analysis, are reviewed in Appendix A.

<!-- @frag ch2_updates_early -->
### 2.13.40 Dated literature updates of 30 October and 2 November 2026 (outside the PRISMA flow)

Two updates were made after the registered search of 25 September 2026. Neither is part of the PRISMA flow: no count in Table 2.2 or Figure 2.1 changes, no record was added to the 71 included studies, and every statement below is at abstract level. Both are reproduced in full in Appendix A.

**30 October 2026.** The eleven queries of the registered search were re-run in the same index, restricted to publication year 2026. Of 215 unique records, 200 were not in the stored output of the registered search; they were title-screened by one reviewer. Five records bear directly on REM's positioning, among them:

- Kekatos et al. (2026) replay the recorded trajectories distributed with AgentDojo through a temporal-logic monitor, offline and without running an agent. Offline evaluation on AgentDojo's recorded traces therefore has a published precedent and is not a methodological contribution of this thesis. They also report that a planted line defeats a naive provenance check on most of the runs it would otherwise flag.
- Z. Liu (2026) replays ground-truth tool calls without a language model to evaluate fifteen injection detectors and reports that detector rankings transfer poorly between benchmarks.
- Yan et al. (2026) and Xin (2026) describe controllers close to REM's decision component: one commits the proposed or an alternative action by a learned value, the other routes among execute, confirm and block with calibrated probabilities. The first was later read in full (Section 2.13.41).

**2 November 2026.** Kanaker et al. (2026) propose an assumption-explicit simulation framework that separates compromise, harm and severity, and compare architectural controls across six threat scenarios and nine defense configurations. Their abstract reports that least-privilege tool design is the strongest single broad control and that human-in-the-loop approvals reduce high-impact actions but degrade under user error and habituation. The study is cited where it is consistent with positions of this thesis; no REM mechanism, parameter or experiment is derived from it.

<!-- @frag ch2_bridge_appraisal -->
### 2.2.40 Quality appraisal, data extraction and synthesis

Every included study was appraised against a ten-item checklist and assigned to a category of **record-visible evidence**: HIGH, MODERATE or LIMITED. The categories describe how much of a study's evidence could be verified from its record, not its intrinsic quality. Of the 71 included studies, 10 are HIGH, 36 MODERATE and 25 LIMITED; 36 are peer reviewed. Every claim this chapter makes about a study is marked with its level of verification: **M**, metadata verified; **A**, supported by the abstract as indexed; **R**, supported by the authors' repository documentation; **U**, resting only on search-engine excerpts and unverified; **F**, verified in the full text. Twenty-one fields were extracted per study. No meta-analysis was possible, because the studies differ in agents, attacks, benchmarks, success definitions and metrics; the synthesis is qualitative and structured by theme, and author-reported figures are never compared across studies as if they were measured on a common scale. The appraisal rules, the extraction fields and the synthesis procedure are given in full in Appendix A.

<!-- @frag ch2_bridge_comparative -->
Table 2.9, reproduced in Appendix A, records for the runtime systems closest to REM the decision basis, whether a calibrated probability is produced, whether consequence enters the decision, the human-review and graduated responses, and which evaluation dimensions are reported.

<!-- @frag ch2_bridge_critical -->
This section draws the thematic syntheses together. The full thematic table (Table 2.10) is in Appendix A.

<!-- @frag ch2_bridge_gaps -->
The review protocol listed five candidate gaps, A to E, to be retained only if the systematic evidence supported them. Their assessment is in Appendix A (Table 2.11). In summary, the review did not support a gap in the existence of runtime interception, graduated responses, calibration or consequence awareness; it supported narrowed versions of three gaps concerning evidence: on the value of behavioral and provenance evidence as input to a calibrated estimator (Gap C), on runtime defenses for financial actions in an open, executable benchmark (Gap D), and on a comparison of a consequence-aware decision with a consequence-independent baseline on the same estimator (Gap E).

<!-- @frag ch2_bridge_guardrails -->
**Learned and LLM-based guardrails.** A further family uses learned models or language models to judge actions or trajectories: generated guardrail code, verification against rule circuits, adaptive checks kept in memory, step-level guardrail models and verify-before-commit designs (reviewed in Appendix A). These cover a broad range of semantic violations without a hand-written policy for each. Their limits recur: judgement by a language model adds latency and can vary between runs, accuracies are measured on the authors' own benchmarks, and the verified records do not report calibrated probabilities that could be combined with the consequence of an action, with the single exception of NEXUS (Section 2.9.3).

<!-- @frag ch2_bridge_monitors -->
Runtime monitors differ in **decision granularity** (whether a decision is taken for each proposed step, for a plan, or for an episode) and in **evidence scope** (whether the decision uses only the current step or also the history that led to it). REM decides for each proposed call and conditions on the episode so far; Task Shield, ProvenanceGuard and VIGIL are in the same group. Sequence-level and accumulating monitors (finite-state conformance engines, learned Markov chains, latent-state models, session risk with decay) are reviewed in Appendix A.

<!-- @frag ch2_bridge_attribution -->
**Attribution for audit.** For a linear model under feature independence, the Shapley attribution of a feature is its coefficient times the feature's deviation from a reference, and on the log-odds of a logistic model the decomposition is exact (Lundberg & Lee, 2017). It is therefore suitable for an audit record that shows which evidence contributed to a decision. It is not a distinguishing mechanism: included systems provide audit traces as rules and findings, rule circuits, traceable evidence or hash-chained logs. In REM, attribution is audit-only and never enters the verdict. The full discussion is in Appendix A.
