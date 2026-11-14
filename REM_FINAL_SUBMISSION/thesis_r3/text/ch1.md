<!-- @frag ch1_problem_tail -->
A defense placed at the action boundary must decide, for each proposed tool call, whether to release it, modify it, refer it for human review or block it. Three questions about that decision are not settled by the literature examined (Chapter 2, Sections 2.9, 2.12 and 2.13.42):

- how an estimated probability that an action was adversarially induced should be combined with the consequence of that action when choosing among responses;
- how often each response is chosen, and at what cost to legitimate work;
- whether a learned, consequence-aware decision of this kind adds anything over simple rules on the provenance of the action's arguments, when the attack objective and the user task have not been seen before.

The problem addressed in this thesis is the runtime compromise of tool-using financial agents through indirect prompt injection. The thesis designs a decision layer at the action boundary, and evaluates it on recorded agent behavior in a banking environment against threshold and rule baselines.

<!-- @frag ch1_gap -->
## 1.41 Research Gap

The gap is not the absence of a mechanism. Runtime guardrails, probability calibration, graduated interventions, human review, provenance analysis and consequence-aware control are all present in the literature (Chapter 2, Section 2.13.3). Several published systems are close to the design studied here:

- **NEXUS** is a structured-plan safety monitor that applies a formal intervention policy to choose among allow, block, request confirmation and request revision. It combines deterministic rules, argument-level inspection and a calibrated logistic-regression risk score (Hossain et al., 2026).
- **CASEL** selects among execution modes by a per-mode cost that weights failure probability by consequence; its authors state that intervention effectiveness is assumed, not measured (Y. Zhang et al., 2026).
- **PROVISO** commits the proposed or an alternative action by a value learned from outcomes over provenance-typed observations; its authors state that the controller is fitted separately for each benchmark and that transfer is not studied (Yan et al., 2026).
- **C. Zhang et al. (2026)** show that a calibrated risk score is not sufficient for choosing interventions.
- **AgentBoundary** reports that high safety frequently coexists with poor completion of authorized tasks (T. Yang et al., 2026).
- **Task Shield** and **MELON** defend against indirect injection with a language model in the decision path (F. Jia et al., 2025; Zhu, Yang, et al., 2025).

The systematic review of Chapter 2 was conducted at record level in September 2026. Six of the papers above were read in full in November 2026, outside that review (Chapter 2, Section 2.13.41). NEXUS is known from its abstract and its authors' repository documentation; its full text was not read.

Within these limits, the gap this thesis addresses is one of **evidence** (Chapter 2, Section 2.13.42):

> Runtime defenses for tool-using agents now combine risk scoring, provenance and graduated interventions, and their authors report benchmark-specific fitting and unmeasured intervention effectiveness. Limited controlled evidence establishes whether a learned, consequence-aware runtime decision adds value over simple provenance and authorization rules for a banking agent when both the user task and the attack objective are unseen, and at what cost in legitimate task completion.

The statement asks a question and does not presuppose its answer. It is proposed wording, pending the supervisor's confirmation. The thesis does not rest any claim of originality on the absence of a mechanism from the records examined.

<!-- @frag ch1_rq_note -->
No research question was added after the pilot. The analyses added in November 2026 (rule baselines, a double-holdout evaluation, robustness probes and a confirmatory run on recordings unread until then; Chapter 3, Sections 3.11.41–3.11.44) bear on RQ2 and RQ4. An exploratory extension investigated on 13 November 2026 (Chapter 3, Section 3.44) asks, within the same questions, whether task-permission evidence compiled from the user's request improves the trade-off and which component is responsible.

<!-- @frag ch1_approach_v11 -->
**One versioned amendment is proposed.** The evaluation found that the behavioral evidence group lowers legitimate task completion without a measured security benefit, and a confirmatory run on recordings unread until then supported removing it for task completion; its effect on security is not resolved (Chapter 4, Section 4.45). The original specification is referred to as **REM v1.0** and remains the frozen baseline. The same framework without the behavioral evidence group is referred to as **REM v1.1** and is a proposed amendment awaiting the supervisor's approval (Chapter 3, Section 3.41). Both are reported in every table that includes either.

<!-- @frag ch1_methodology -->
## 1.42 Research Methodology

The research follows design science research. In design science, knowledge is produced by building an artifact that addresses an identified problem and evaluating it (Hevner et al., 2004), following the six activities of Peffers et al. (2007) (Chapter 3, Section 3.1.1). The artifact is REM.

The evaluation is quantitative and uses the AgentDojo banking environment (Debenedetti et al., 2024). Live agent runs with REM enforcing its verdicts require access to a language model, which was not available. The evaluation therefore rests on traces of real agents recorded by the benchmark authors (Chapter 3, Sections 3.11.1 and 3.11.11). It has five parts:

- **Offline classification** of recorded tool calls, under nested grouped cross-fitting that holds out one whole attack objective per fold (Chapter 3, Section 3.11.5).
- **Observe-only policy analysis**, in which verdicts are computed but not enforced.
- **Recorded-trace replay**, which re-executes recorded trajectories in the benchmark's sandbox with a policy that may withhold calls, assuming the agent does not adapt to refusals. REM is compared with a no-defense reference, a consequence-independent threshold baseline on the same estimator, and three rules that use no model (Chapter 3, Section 3.11.41). A double-holdout scheme tests user tasks and attack objectives that are both unseen (Chapter 3, Section 3.11.42).
- **A confirmatory replay** of one proposed modification on recordings that no analysis had read before that run, under a protocol and a decision rule committed before those recordings were opened (Chapter 3, Section 3.11.44).
- **An exploratory extension**, in which a deterministic permission rule compiled from the user's request, a published fixed-list policy (the manual banking policy of Progent) and learned variants are replayed on the same recordings under a protocol committed before their outcomes were computed (Chapter 3, Section 3.44). All of its results are development evidence.

The replay analysis is a proposed amendment to the original scope, which excluded replay-based estimation; its status is stated wherever its results are used. No result in this thesis comes from a live agent.

<!-- @frag ch1_contrib -->
## 1.43 Contributions: Proposed and Demonstrated

**Proposed contribution.** The contribution proposed at the design stage was empirical and integrative: the design and evaluation, on an open and executable banking benchmark under indirect prompt injection, of a non-invasive five-layer runtime layer that combines provenance-based action evidence, a calibrated per-step probability of adversarial inducement, verdict selection by minimum conditional risk with losses declared per consequence tier, and deterministic mitigation.

**What the thesis demonstrates**, with the evidence for each item (Chapter 5, Table 5.43 gives the precedent, code, experiment, result and limits of each):

1. **A specified, implemented and tested framework.** REM is specified in Chapter 3 and implemented so that an undeclared design value stops the software. *Evidence:* 278 passing software tests and exact re-execution of the pilot (Chapter 3, Section 3.42; Chapter 4, Section 4.83).
2. **A controlled evaluation protocol.** It isolates the decision rule from the estimator, holds out whole attack objectives, adds a double holdout of user task and attack objective, compares the learned policy with rules that use no model and with one published policy replayed in the same harness, and includes one confirmatory run under a pre-committed protocol. *Evidence:* Chapters 3 and 4.
3. **Measured security and its cost.** In replay, REM v1.0 reduces attack success from 22.6% to 0.4% on the primary recordings and from 21.1% to 0.15% on the second population. It completes 31% of benign tasks where the undefended agent completes 52% (Chapter 4, Sections 4.6 and 4.45).
4. **A confirmed gain in task completion within the framework.** Removing the behavioral evidence group raises task completion by 7.5 percentage points (95% interval 1.2 to 16.0) on 2,113 episodes that were unread before that run, with 1 successful attack against 3 of 2,065. The pre-declared decision rule was met; the security difference is not resolved statistically (Chapter 4, Section 4.45).
5. **Negative results.** Four are documented (Chapter 5, Section 5.45): behavioral evidence did not help; an authorization-aware policy supervised on intervention outcomes did not transfer to an unseen attack objective; a rule that trusts documents named by the user was unsafe; and exact-string provenance failed when an identifier was reformatted.
6. **An identified limit of provenance evidence.** None of the policies tested up to 11 November, learned or rule-based, separates an authorized payment from an unrequested one whose details appear in the user's words. Their evidence describes where a call's arguments come from, not what the user asked for (Chapter 4, Section 4.44).
7. **An exploratory extension with an attribution result.** A deterministic rule that compiles the user's request and matches operation, recipient and amount completes more benign tasks than REM v1.0 with no more successful attacks, on development data. Its advantage over the strongest simple rule is not resolved; a published fixed-list policy is better on security; and a learned model on the same evidence adds no demonstrated value. The gain is due to the rule and not to the learned core (Chapter 4, Sections 4.89, 4.91 and 4.92). An external review then found three defects in the rule; the repaired rule removes nine of its ten successful attacks on the primary recordings, at the cost of the one user task whose condition it does not evaluate, and is still not resolved against the simple rule or the published policy (Chapter 4, Sections 4.93 and 4.94).

**What the thesis does not demonstrate:**

- that REM adds value over simple provenance or authorization rules: on the second population neither REM version is distinguishable from them (Chapter 4, Section 4.45);
- that the learned, consequence-aware core is what improves the trade-off: the improvements that were observed came from removing evidence and from deterministic rules;
- any effect on live agents: a closed-loop harness is implemented and tested with scripted agents and was not executed with a language model (Chapter 4, Section 4.46);
- any difference in effect among Modify, Escalate and Block, which coincide in this evaluation;
- results under supervisor-approved design values, or with human-audited labels;
- any comparison with a published defense that needs a language model; the one published policy that was replayed has no successful attack and completes more tasks than REM (Chapter 4, Section 4.89).

**What the thesis does not claim:** a new algorithm; the first runtime guardrail, calibrated agent risk score or consequence-aware controller; that calibration improves control; robustness against adaptive adversaries; any prevention guarantee; that the tested features establish what the user authorized; that the permission rule of the extension generalizes beyond the benchmark's requests; or validity in production financial deployment. Each constituent mechanism is established and attributed to its source (Chapter 2, Table 2.12).

<!-- @frag ch1_org -->
## 1.44 Thesis Organization

The thesis is organized in five chapters:

- **Chapter 1** introduces the background, problem, gap, aim, objectives, research questions, approach, scope and contributions.
- **Chapter 2** reports a record-level systematic review of runtime security for tool-using AI agents, three dated literature updates that lie outside that review, a comparison of the closest prior work, and the research gap.
- **Chapter 3** specifies the research methodology and the design of REM (architecture, threat model, evidence, estimator, calibration, consequence tiers, expected-loss decision, mitigation, audit), the experimental methodology, baselines, ablations and metrics, the proposed amendment REM v1.1, and the implementation.
- **Chapter 4** is organized in six sections: implementation tools and environment; dataset preparation and training; experimental setup and evaluation metrics; comparisons with existing models and defense frameworks; ablation studies; and results and discussion. It states that no live-agent experiment was executed and that the one published policy evaluated was replayed on recorded episodes.
- **Chapter 5** answers the research questions, assesses the objectives and contributions, records the rejected variants and the negative findings, and ends with limitations and future work.

Appendices A to F hold the evidence matrix of the review, the implementation details, the equation provenance table, the design and status of the live-agent and MELON evaluations, the sensitivity analysis of the mitigation semantics, and the register of open supervisor decisions.
