# CHAPTER ONE

# INTRODUCTION

## 1.1 Background

### 1.1.1 Language models and AI agents

Artificial intelligence systems based on large language models (LLMs) generate text, and increasingly structured actions, from natural-language input. An *LLM agent* uses such a model as the controller of a system that perceives its context, reasons, plans and acts in pursuit of a task (L. Wang et al., 2024). In the execution pattern made explicit by ReAct (Yao et al., 2023), the model interleaves reasoning with actions, and the observations returned by those actions re-enter its context and shape the next step. The term *agentic AI* is used in this thesis only in this operational sense: a model-driven system that selects and executes actions with some autonomy.

### 1.1.2 Tool-using and financial AI agents

Tool-using agents act through calls to external tools, such as file readers, messaging services or payment interfaces, with arguments that the model generates. When such an agent operates in a financial setting, a single proposed tool call can have direct external effects:

- initiate a payment;
- schedule or alter a recurring payment;
- change account credentials;
- send customer data to an external recipient.

Evaluations of agents in finance have argued that capability benchmarks alone are insufficient and that the risk of such actions must be assessed directly (Z. Chen et al., 2025).

### 1.1.3 Indirect prompt injection

Indirect prompt injection is content placed in data that the agent retrieves or receives from a tool, rather than in the user's request, and that the agent then treats as an instruction (Greshake et al., 2023; OWASP Gen AI Security Project, 2025). Because tool outputs re-enter the model's context, an attacker who can write into an e-mail, a file or a transaction description can attempt to redirect the agent's next action. The resulting harm is caused by the action, not by the text: an injected instruction is dangerous when it leads the agent to propose a call that serves the attacker. Figure 1.1 illustrates this path in a banking task of the kind used in this thesis.

![Figure 1.1. A financial agent task with an indirect prompt injection. The user request is trusted; the tool output carrying the injected instruction is untrusted; the harm occurs only if the proposed state-changing call (here a transfer to the attacker) is executed. REM is placed at the tool-execution boundary.](REM_FINAL_THESIS/final_five_chapters/figures/fig1_1_threat_scenario.png){width=100%}

### 1.1.4 Runtime security at the tool-execution boundary

The security question therefore shifts from what a model says to what an agent does: to the moment at which a proposed action crosses from the agent into its environment (Chapter 2, Section 2.1).

## 1.2 Problem Statement

An agent receives input through channels of different trustworthiness:

- the system prompt;
- the user's request;
- tool outputs;
- retrieved content;
- stored memory.

Indirect prompt injection exploits the difference. Content from an external source, processed by the agent, alters its behavior without any access to the user channel (OWASP Gen AI Security Project, 2025; Greshake et al., 2023). Benchmarks designed for tool-using agents show that the threat is practical, including in environments with financial tools (Debenedetti et al., 2024; Zhan et al., 2024; H. Zhang et al., 2025). The attack-success rates they report depend strongly on benchmark, model and attack template, and they cannot be pooled across studies (Chapter 2, Sections 2.3–2.4).

Defenses can intervene at several points: at the input, inside the model, in the system architecture, or at the moment a proposed action is about to be executed (Chapter 2, Section 2.5). **This thesis chooses the last of these, the action boundary, as its point of intervention.** It is the point at which an induced financial action becomes visible as a concrete tool call with concrete arguments, and at which it can still be withheld before it takes effect. It is not the only place where an attack can be stopped, and other defenses act earlier.

A defense placed at the action boundary must decide, for each proposed tool call, whether to release it, modify it, refer it for human review or block it. Three questions about that decision are not settled by the literature examined (Chapter 2, Sections 2.8, 2.10 and 2.11.5):

- how an estimated probability that an action was adversarially induced should be combined with the consequence of that action when choosing among responses;
- how often each response is chosen, and at what cost to legitimate work;
- whether a learned, consequence-aware decision of this kind adds anything over simple rules on the provenance of the action's arguments, when the attack objective and the user task have not been seen before.

The problem addressed in this thesis is the runtime compromise of tool-using financial agents through indirect prompt injection, and the question of whether a layered defense at the action boundary actually protects in depth. Such defenses are commonly organized as several layers (content inspection, behavioral analysis, action evidence, a risk-informed decision and enforcement), but layering is a property of the design, whereas defense in depth is a property of the protection: it holds only if more than one component contributes protection and the loss of one is covered by another. The thesis designs such a five-layer framework, REM, and evaluates on recorded agent behavior in a banking environment which of its components actually carry protection, at what cost to legitimate financial work, and how it compares with threshold and simple rule baselines.

## 1.3 Motivation

Three considerations motivate the work.

**Concrete financial consequences.** Tools that transfer value, modify payments or change credentials expose money, account control and personal data to manipulation (Chapter 2, Section 2.9). Conventional evaluation of financial LLM agents, based on accuracy and return metrics, has been argued to give an illusion of reliability while overlooking vulnerabilities such as adversarial prompt manipulation (Z. Chen, J. Chen, et al., 2025).

**Record-keeping and human control.** Regulation (EU) 2024/1689 requires high-risk AI systems to allow the automatic recording of events and effective human oversight, including the ability to intervene (European Parliament & Council of the European Union, 2024). Whether a given financial agent falls within a high-risk category is not assessed here. The provisions motivate two design properties: an audit record for every decision and an explicit route to human review.

**Fragile evaluation.** Pitfalls in the design and evaluation of learning-based security systems lead to unrealistic performance estimates (Arp et al., 2022). Audits of agent-safety benchmarks report metric flaws, inconsistent rankings and contradictory conclusions across benchmarks (Y. Wang et al., 2026; M. Q. Li et al., 2026). A defense for financial agents must therefore be evaluated so that:
- attack success is reported together with benign utility;
- dependence between benchmark tasks is respected;
- leakage between fitting and test data is controlled.

## 1.4 Research Gap

The gap is not the absence of a mechanism. Runtime guardrails, probability calibration, graduated interventions, human review, provenance analysis and consequence-aware control are all present in the literature (Chapter 2, Section 2.11.2). Several published systems are close to the design studied here:

- **NEXUS**, published in the Findings of IJCNLP-AACL 2026, is a structured-plan safety monitor that applies a formal intervention policy to choose among allow, block, request confirmation and request revision. It combines deterministic rules, argument-level inspection and a calibrated logistic-regression risk score, and its abstract reports a comparison with rule-only intervention selection on non-financial benchmarks (Hossain et al., 2026). It is the closest published analogue of REM's Decision Engine.
- **CASEL** selects among execution modes by a per-mode cost that weights failure probability by consequence; its authors state that intervention effectiveness is assumed, not measured (Y. Zhang et al., 2026).
- **PROVISO** commits the proposed or an alternative action by a value learned from outcomes over provenance-typed observations; its authors state that the controller is fitted separately for each benchmark and that transfer is not studied (Yan et al., 2026).
- **C. Zhang et al. (2026)** show that a calibrated risk score is not sufficient for choosing interventions.
- **AgentBoundary** reports that high safety frequently coexists with poor completion of authorized tasks (T. Yang et al., 2026).
- **Task Shield** and **MELON** defend against indirect injection with a language model in the decision path (F. Jia et al., 2025; Zhu, Yang, et al., 2025).

The systematic review of Chapter 2 was conducted at record level in September 2026. Six of the papers above were read in full in November 2026, outside that review (Chapter 2, Section 2.11.4), and the Progent paper (version 3) on 16 November 2026. NEXUS is a peer-reviewed publication; its full text was not read, and statements about it rest on its abstract and its authors' repository documentation. Several later works with layered or authorization-based designs (Chapter 2, Sections 2.11.4, 2.11.6 and 2.11.7) are known only from their abstracts. Substantial prior-art overlap therefore exists for every component of REM and for layered combinations of them, and this thesis does not claim an architectural or mechanism novelty. The review is not exhaustive, and no claim is made that every possible combination has been published.

Within these limits, the gap this thesis addresses is one of **evidence** (Chapter 2, Sections 2.11.5 and 2.11.7):

> Layered runtime defenses against indirect prompt injection, combining content inspection, provenance-aware, behavioral, learned and rule-based controls, have been proposed and, in several cases, ablated layer by layer. Among the studies examined, most of them at abstract level, the evidence remains limited on three questions for a financial agent acting on an executable banking benchmark: which components of such a defense actually carry its protection, and whether removing a component and suppressing its evidence at test time lead to the same assessment; whether a learned, consequence-aware decision adds value over simple deterministic rules on the same proposed financial calls; and what the measured protection costs in legitimate financial task completion, including against a reference that executes no state-changing call.

The statement asks a question and does not presuppose its answer. It is proposed wording, pending the supervisor's confirmation. The thesis does not rest any claim of originality on the absence of a mechanism from the records examined.

## 1.5 Research Aim

The approved research proposal states objectives but no separate aim. The aim below is derived from the approved objectives of Section 1.6 and adds nothing to them.

The aim of this research is to design a runtime evaluation and mitigation framework for the security of financial AI agents, to evaluate it against adversarial attacks, and to compare it with existing security approaches.

*Proposed focus, pending the supervisor's confirmation.* Within this aim, the evaluation focuses on one question: whether the framework's five-layer organization produces defense in depth, that is, which of its components contribute protection against indirect prompt injection, what that protection costs in legitimate task completion, and how it compares with simple deterministic rules.

## 1.6 Research Objectives

The approved objectives are (Chapter 3, Section S-3.1.2):

- **O1:** Design a REM framework for financial AI agents' and task automation agents' security.
- **O2:** Evaluate the framework against adversarial attacks.
- **O3:** Compare performance with existing security approaches.

O1 names task-automation agents as well as financial agents. **The evaluation in this thesis is restricted to a banking environment.** No task-automation environment was evaluated, so the evidence bears on financial agents only.

## 1.7 Research Questions

The research questions below are derived from the approved objectives (Chapter 3, Section S-3.1.3). The approved proposal states no research questions, and these have not yet been confirmed by the supervisor; they remain proposed ([PD], decision D-10). Each is stated together with the kind of evidence this thesis could produce for it.

- **RQ1 (estimation).** How well does a ridge logistic regression estimator, using context, behavioral and action evidence available at the tool-call boundary, discriminate adversarially induced proposed actions in the AgentDojo banking environment, and how well calibrated are its probabilities under grouped cross-fitting? *Evidence:* offline classification of recorded steps.
- **RQ2 (decision).** Compared with a consequence-independent threshold policy that uses the same estimator, how does consequence-tiered expected-loss verdict selection change intervention behavior, attack success and utility, across a declared range of loss structures? *Evidence:* observe-only policy analysis of recorded steps, and a replay sensitivity analysis.
- **RQ3 (mitigation and cost).** What residual attack success remains after the Modify mechanism, how often is escalation selected, and what per-step processing time does REM add? *Evidence:* replay sensitivity analysis and runtime measurement. Residual success against live, adaptive agents is not measured.
- **RQ4 (component contribution).** What is the marginal contribution of each evidence group, of calibration, and of consequence tiers, as determined by ablation? *Evidence:* offline and observe-only ablations, and replay.

No research question was added after the pilot. The analyses added in November 2026 (rule baselines, a double-holdout evaluation, robustness probes and a confirmatory run on recordings unread until then; Chapter 3, Sections 3.11.10–3.11.13) bear on RQ2 and RQ4. An exploratory extension investigated from 13 to 16 November 2026 (Chapter 3, Section 3.14) asks, within the same questions, whether task-permission evidence compiled from the user's request improves the trade-off and which component is responsible.

## 1.8 Proposed Approach

The Runtime Evaluation and Mitigation (REM) framework is a runtime mediation layer placed between one agent and its environment. It treats the agent as opaque: it observes inputs, context, proposed actions and tool results, but not model parameters or internal reasoning (Chapter 3, Section 3.3.1). REM comprises exactly five layers (Chapter 3, Section 3.2.1):

1. **Input & Context Layer.** Captures the information the agent handles and the action it proposes, and labels each context segment with its provenance.
2. **Detection Layer.** Computes evidence about untrusted context.
3. **Behavioral Analysis Layer.** Computes evidence about the episode history and the proposed action.
4. **Decision Engine Layer.** Performs five steps:
   - estimates the probability that the proposed action is adversarially induced, using ridge logistic regression (Cox, 1958; le Cessie & van Houwelingen, 1992);
   - calibrates that probability on the logit (Platt, 2000; Guo et al., 2017);
   - assigns a declared consequence tier and applies policy predicates;
   - selects the verdict among Allow, Modify, Escalate and Block by minimizing conditional risk under tier-indexed losses (Elkan, 2001; Chow, 1970);
   - writes an audit record.
5. **Mitigation Layer.** Executes the mechanism associated with the verdict.

Offline fitting and recalibration are cross-cutting activities performed between deployments; they are not a layer. A linear attribution of the logit (Lundberg & Lee, 2017) is written to the audit record and never influences the verdict.

**None of these elements is new.**
- Runtime interception of tool calls, probability calibration and a four-way set of graduated verdicts all have precedents (Chapter 2, Section 2.11.2).
- In REM, declared costs play the role that hand-chosen thresholds play in threshold policies: the threshold between two verdicts follows from the declared cost ratio for the action's consequence tier (Chapter 3, Section 3.7.5).

**One versioned amendment is proposed.** The evaluation found that the behavioral evidence group lowers legitimate task completion without a measured security benefit. A confirmatory run on recordings unread until then supported removing it for task completion, but its effect on security is not resolved (Chapter 4, Section 4.6.8). The original specification is referred to as **REM v1.0** and remains the frozen baseline. The same framework without the behavioral evidence group is referred to as **REM v1.1** and is a proposed amendment awaiting the supervisor's approval (Chapter 3, Section 3.13). Both are reported in every table that includes either.

## 1.9 Research Methodology

The research follows design science research. In design science, knowledge is produced by building an artifact that addresses an identified problem and evaluating it (Hevner et al., 2004), following the six activities of Peffers et al. (2007) (Chapter 3, Section 3.1.1). The artifact is REM.

The evaluation is quantitative and uses the AgentDojo banking environment (Debenedetti et al., 2024). Live agent runs with REM enforcing its verdicts require access to a language model, which was not available. The evaluation therefore rests on traces of real agents recorded by the benchmark authors (Chapter 3, Sections 3.11.1 and 3.11.9). It has five parts:

- **Offline classification** of recorded tool calls, under nested grouped cross-fitting that holds out one whole attack objective per fold (Chapter 3, Section 3.11.5).
- **Observe-only policy analysis**, in which verdicts are computed but not enforced.
- **Recorded-trace replay**, which re-executes recorded trajectories in the benchmark's sandbox with a policy that may withhold calls, assuming the agent does not adapt to refusals. REM is compared with a no-defense reference, a consequence-independent threshold baseline on the same estimator, and three rules that use no model (Chapter 3, Section 3.11.10). A double-holdout scheme tests user tasks and attack objectives that are both unseen (Chapter 3, Section 3.11.11).
- **A confirmatory replay** of one proposed modification on recordings that no analysis had read before that run, under a protocol and a decision rule committed before those recordings were opened (Chapter 3, Section 3.11.13).
- **An exploratory extension**, in which a deterministic permission rule compiled from the user's request, a fixed-list policy from Progent's repository (a manual banking policy) and learned or calibrated variants are replayed on the same recordings under a protocol committed before their outcomes were computed (Chapter 3, Section 3.14). All of its results are development evidence.

The replay analysis is a proposed amendment to the original scope, which excluded replay-based estimation; its status is stated wherever its results are used. No result in this thesis comes from a live agent.

## 1.10 Scope

**In scope (Chapter 3, Section S-3.1.4):**

- a single LLM-based agent that invokes tools with generated arguments;
- a financial (banking) task environment with executable tools and state-based checks;
- indirect prompt injection through tool outputs as the evaluated attack class;
- runtime mediation of each proposed tool call before it is released.

**Out of scope:**

- training-time defenses and modification of the agent's model or prompts;
- multi-agent systems;
- adaptive adversaries who tune attacks to REM;
- production deployment in a financial institution;
- task-automation environments other than banking;
- counterfactual estimation of intervention value for adaptive agents.

The design rests on stated assumptions (Chapter 3, Table 3.2). Among them:

- REM can intercept tool calls and results without modifying the agent (AS-1);
- REM's own code, parameters and logs are protected from the adversary (AS-3);
- adversaries do not adapt to REM in the primary evaluation (AS-6).

## 1.11 Contributions: Proposed and Demonstrated

**Proposed contribution.** The contribution proposed at the design stage was empirical and integrative. It was the design and evaluation of a non-invasive runtime framework of five layers that combines provenance-based action evidence, a calibrated per-step probability of adversarial inducement, verdict selection by minimum conditional risk with losses declared per consequence tier, and deterministic mitigation. The framework was to be evaluated on an open and executable banking benchmark under indirect prompt injection.

**Primary empirical contribution.** The thesis examines whether REM's five-layer architecture produces defense in depth, rather than assuming that it does. On recorded AgentDojo banking traces, protocol-frozen paired component-level ablations and an exploratory comparison of removal with test-time suppression show that it does so only narrowly. Enforcement and the combined learned scoring-and-decision pathway are each necessary for the measured protection. That protection rests on two evidence families that cover different attack classes: action/provenance evidence, whose removal measurably lowers the withholding of attack calls on one population, and behavioral evidence, which under modelled suppression is the only evidence that stops the credential-change objective. Context detection and the deterministic predicates show no measurable effect. The protection is obtained with low specificity: on the primary population, REM v1.0 completes exactly the benign tasks that withholding every state-changing call completes. All results are replay results on data examined during development.

**What the thesis demonstrates**, with the evidence for each item (Chapter 5, Table 5.3 gives the precedent, code, experiment, result and limits of each):

1. **A specified, implemented and tested framework.** REM is specified in Chapter 3 and implemented so that an undeclared design value stops the software. *Evidence:* 278 passing software tests and exact re-execution of the pilot (Chapter 3, Section S-3.15; Chapter 4, Section 4.1.3).
2. **A controlled evaluation protocol.** The protocol isolates the decision rule from the estimator and holds out whole attack objectives, with a double holdout of user task and attack objective. It compares the learned policy with rules that use no model and with one published policy replayed in the same harness. It also includes one confirmatory run under a pre-committed protocol. *Evidence:* Chapters 3 and 4.
3. **Measured security and its cost.** In replay, REM v1.0 reduces attack success from 22.6% to 0.4% on the primary recordings and from 21.1% to 0.15% on the second population. It completes 31% of benign tasks where the undefended agent completes 52%. On the primary recordings, the 105 benign tasks it completes are exactly those completed when every state-changing call is withheld, so in replay it completes no benign task that requires a payment, payment change or credential change. It completes 94 more tasks under attack than that reference and lets 11 attacks through, all in one task whose request names the attacker's account. This identity is established on the primary recordings only (Chapter 4, Sections 4.6.3 and 4.6.8).
4. **A confirmed gain in task completion within the framework.** Removing the behavioral evidence group raises task completion by 7.5 percentage points (95% interval 1.2 to 16.0) on 2,113 episodes that were unread before that run, with 1 successful attack against 3 of 2,065. The pre-declared decision rule was met; the security difference is not resolved statistically (Chapter 4, Section 4.6.8).
5. **Negative results.** Four are documented (Chapter 5, Section 5.5): behavioral evidence, when removed and refitted, did not help (under exploratory test-time suppression it was the only evidence that stopped the credential-change objective; Chapter 4, Section 4.6.12); an authorization-aware policy supervised on intervention outcomes did not transfer to an unseen attack objective; a rule that trusts documents named by the user was unsafe; and exact-string provenance failed when an identifier was reformatted.
6. **An identified limit of provenance evidence.** None of the policies tested up to 11 November, learned or rule-based, separates an authorized payment from an unrequested one whose details appear in the user's words. Their evidence describes where a call's arguments come from, not what the user asked for (Chapter 4, Section 4.6.7).
7. **An exploratory extension with an attribution result.** A deterministic rule compiles the user's request into instructions and releases a state-changing call only if it matches one in operation, recipient, amount and stated condition. Two external reviews found defects in the matching, and each repair was frozen before it was scored. On development data the current rule has no successful attack and completes more benign tasks than REM v1.0 in point estimate. Against the strongest simple rule it has fewer successful attacks, while the difference in completed tasks is not resolved. Against a fixed-list policy from Progent's repository, no difference is resolved. The rule's authority guard used alone (GV), without any learned decision, gives the outcomes of every learned or statistically calibrated decision tested behind it, except a Neyman-Pearson threshold at 0.01, which loses tasks. The measured change is due to deterministic components and not to the learned core. An external review then found that the guard accepted computed amounts it never computed and read a percentage coefficient as an amount. A typed amount verifier repairs both defects, at the cost of the tasks whose amounts the request does not determine. Request-derived argument checks of this kind have also been published by others (Chapter 2, Section 2.11.4). A validation on independently written requests was defined and not executed (Chapter 4, Sections 4.4.7, 4.5.8 and 4.6.9).
8. **Protocol-frozen component-level ablations within the layered architecture, and a comparison with existing frameworks (19 to 22 November 2026).** With protocols committed before any arm was scored, on recordings that had been examined during development, the ablations show how REM v1.0's protection is produced:
   - enforcement and the combined learned pathway (estimator, calibration and expected-loss selection, removed together) are each necessary: without either, attack outcomes return to the no-defense level;
   - on the primary population, removing calibration alone changes no attack outcome, and replacing expected-loss selection by consequence-independent thresholds raises successful attacks from 11 to 164;
   - removing the action/provenance evidence lowers attack-call withholding measurably on the second population (−9.1 points, 95% interval −23.5 to −0.7) and increases the episodes in which an attack call is executed, while its effect on final attack outcomes is not resolved on any population;
   - removing behavioral evidence raises task completion with no measured security change, whereas suppressing it at test time (exploratory) lets the credential-change objective succeed;
   - context detection, the predicates and Modify show no measurable effect;
   - provenance labelling and the Detection layer's classifier could not be ablated (the first is a dependency of later features, the second does not exist), and the context-hygiene step was not exercised by the recorded data.

   The four defenses distributed with the benchmark are compared descriptively through their authors' recorded runs. Progent's published banking policy, decided by its authors' code on the same episodes, admits no attack and completes more tasks than REM; its list of permitted recipients is specific to the benchmark. DRIFT and MELON are compared at the level of architecture and code only (Chapter 4, Sections 4.4, 4.5 and 4.6.12).

**What the thesis does not demonstrate:**

- that REM adds value over simple provenance or authorization rules: on the second population neither REM version is distinguishable from them (Chapter 4, Section 4.6.8);
- that the learned, consequence-aware core is what improves the trade-off: the improvements that were observed came from removing evidence and from deterministic rules;
- any effect on live agents: a closed-loop harness is implemented and tested with scripted agents and was not executed with a language model (Chapter 4, Section S-4.4.4);
- any difference in effect among Modify, Escalate and Block, which coincide in this evaluation;
- results under supervisor-approved design values, or with human-audited labels;
- that a component without a measurable effect in the ablation is unnecessary (Chapter 4, Section 4.5.10);
- any closed-loop comparison with a published defense. The four distributed defenses are compared through their authors' recorded runs against REM's replay, which is descriptive (Chapter 4, Section 4.4.7). MELON and DRIFT were not run with a language model; their official code was executed only with scripted agents. The one published policy that was replayed, decided by its authors' own code, has no successful attack and completes more tasks than REM (Chapter 4, Section 4.4.7).

**What the thesis does not claim:**

- a new algorithm;
- the first runtime guardrail, calibrated agent risk score or consequence-aware controller;
- that calibration improves control;
- robustness against adaptive adversaries;
- any prevention guarantee;
- that the tested features establish what the user authorized, or that REM authorizes actions: it estimates and decides, and holds no representation of what the user permitted (Chapter 3, Section 3.2.2);
- that the number of layers, or the contributions found by removing them, is by itself evidence of defense in depth;
- that the permission rule of the extension generalizes beyond the benchmark's requests;
- validity in production financial deployment.

Each constituent mechanism is established and attributed to its source (Chapter 2, Table 2.2).

## 1.12 Thesis Organization

The thesis is organized in five chapters:

- **Chapter 1** introduces the background, problem, gap, aim, objectives, research questions, approach, scope and contributions.
- **Chapter 2** reports a record-level systematic review of runtime security for tool-using AI agents, three dated literature updates that lie outside that review, a comparison of the closest prior work, and the research gap.
- **Chapter 3** specifies the research methodology and the design of REM (architecture, threat model, evidence, estimator, calibration, consequence tiers, expected-loss decision, mitigation, audit), the experimental methodology, baselines, ablations and metrics, the proposed amendment REM v1.1, and the implementation.
- **Chapter 4** is organized in six sections: implementation tools and environment; dataset preparation and training; experimental setup and evaluation metrics; comparison with existing security frameworks (Progent, DRIFT, MELON and the defenses distributed with the benchmark); an ablation study of REM's five layers; and results and discussion. It states that no live-agent experiment was executed, that the one published policy evaluated was replayed on recorded episodes, and that DRIFT and MELON were compared at the level of architecture and code.
- **Chapter 5** answers the research questions, assesses the objectives and contributions, records the rejected variants and the negative findings, and ends with limitations and future work.

Appendix A holds the notation, the layer interfaces, the optional sequential analysis, the provenance of the equations and the logistic model of Equation 2.1, and Appendix B the register of open supervisor decisions. This condensed edition prints the review's evidence matrix, the implementation details, the live-agent and MELON status, the sensitivity analysis of the mitigation semantics, and the history of the analyses in an indexed supplement; a reference of the form "Section S-x" or "Table S-x" points to it. Nothing was removed from the record: the fifth edition is preserved.
