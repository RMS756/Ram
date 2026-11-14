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

A defense placed at the action boundary must decide, for each proposed tool call, whether to release it, modify it, refer it for human review or block it. Three questions about that decision are not settled by the literature examined (Chapter 2, Sections 2.8, 2.11 and 2.12.7):

- how an estimated probability that an action was adversarially induced should be combined with the consequence of that action when choosing among responses;
- how often each response is chosen, and at what cost to legitimate work;
- whether a learned, consequence-aware decision of this kind adds anything over simple rules on the provenance of the action's arguments, when the attack objective and the user task have not been seen before.

The problem addressed in this thesis is the runtime compromise of tool-using financial agents through indirect prompt injection. The thesis designs a decision layer at the action boundary, and evaluates it on recorded agent behavior in a banking environment against threshold and rule baselines.

## 1.3 Motivation

Three considerations motivate the work.

**Concrete financial consequences.** Tools that transfer value, modify payments or change credentials expose money, account control and personal data to manipulation (Chapter 2, Section 2.9). Conventional evaluation of financial LLM agents, based on accuracy and return metrics, has been argued to give an illusion of reliability while overlooking vulnerabilities such as adversarial prompt manipulation (Z. Chen, J. Chen, et al., 2025).

**Record-keeping and human control.** Regulation (EU) 2024/1689 requires high-risk AI systems to allow the automatic recording of events and effective human oversight, including the ability to intervene (European Parliament & Council of the European Union, 2024). Whether a given financial agent falls within a high-risk category is not assessed here. The provisions motivate two design properties: an audit record for every decision and an explicit route to human review.

**Fragile evaluation.** Pitfalls in the design and evaluation of learning-based security systems lead to unrealistic performance estimates (Arp et al., 2022). Audits of agent-safety benchmarks report metric flaws, inconsistent rankings and contradictory conclusions across benchmarks (Y. Wang et al., 2026; M. Q. Li et al., 2026). A defense for financial agents must therefore be evaluated so that:
- attack success is reported together with benign utility;
- dependence between benchmark tasks is respected;
- leakage between fitting and test data is controlled.

## 1.4 Research Gap

The gap is not the absence of a mechanism. Runtime guardrails, probability calibration, graduated interventions, human review, provenance analysis and consequence-aware control are all present in the literature (Chapter 2, Section 2.12.3). Several published systems are close to the design studied here:

- **NEXUS** is a structured-plan safety monitor that applies a formal intervention policy to choose among allow, block, request confirmation and request revision. It combines deterministic rules, argument-level inspection and a calibrated logistic-regression risk score (Hossain et al., 2026).
- **CASEL** selects among execution modes by a per-mode cost that weights failure probability by consequence; its authors state that intervention effectiveness is assumed, not measured (Y. Zhang et al., 2026).
- **PROVISO** commits the proposed or an alternative action by a value learned from outcomes over provenance-typed observations; its authors state that the controller is fitted separately for each benchmark and that transfer is not studied (Yan et al., 2026).
- **C. Zhang et al. (2026)** show that a calibrated risk score is not sufficient for choosing interventions.
- **AgentBoundary** reports that high safety frequently coexists with poor completion of authorized tasks (T. Yang et al., 2026).
- **Task Shield** and **MELON** defend against indirect injection with a language model in the decision path (F. Jia et al., 2025; Zhu, Yang, et al., 2025).

The systematic review of Chapter 2 was conducted at record level in September 2026. Six of the papers above were read in full in November 2026, outside that review (Chapter 2, Section 2.12.6). NEXUS is known from its abstract and its authors' repository documentation; its full text was not read.

Within these limits, the gap this thesis addresses is one of **evidence** (Chapter 2, Section 2.12.7):

> Runtime defenses for tool-using agents now combine risk scoring, provenance and graduated interventions, and their authors report benchmark-specific fitting and unmeasured intervention effectiveness. Limited controlled evidence establishes whether a learned, consequence-aware runtime decision adds value over simple provenance and authorization rules for a banking agent when both the user task and the attack objective are unseen, and at what cost in legitimate task completion.

The statement asks a question and does not presuppose its answer. It is proposed wording, pending the supervisor's confirmation. The thesis does not rest any claim of originality on the absence of a mechanism from the records examined.

## 1.5 Research Aim

The approved research proposal states objectives but no separate aim. The aim below is derived from the approved objectives of Section 1.6 and adds nothing to them.

The aim of this research is to design a runtime evaluation and mitigation framework for the security of financial AI agents, to evaluate it against adversarial attacks, and to compare it with existing security approaches.

## 1.6 Research Objectives

The approved objectives are (Chapter 3, Section 3.1.2):

- **O1:** Design a REM framework for financial AI agents' and task automation agents' security.
- **O2:** Evaluate the framework against adversarial attacks.
- **O3:** Compare performance with existing security approaches.

O1 names task-automation agents as well as financial agents. **The evaluation in this thesis is restricted to a banking environment.** No task-automation environment was evaluated, so the evidence bears on financial agents only.

## 1.7 Research Questions

The research questions below are derived from the approved objectives (Chapter 3, Section 3.1.3). The approved proposal states no research questions, and these have not yet been confirmed by the supervisor; they remain proposed ([PD], decision D-10). Each is stated together with the kind of evidence this thesis could produce for it.

- **RQ1 (estimation).** How well does a ridge logistic regression estimator, using context, behavioral and action evidence available at the tool-call boundary, discriminate adversarially induced proposed actions in the AgentDojo banking environment, and how well calibrated are its probabilities under grouped cross-fitting? *Evidence:* offline classification of recorded steps.
- **RQ2 (decision).** Compared with a consequence-independent threshold policy that uses the same estimator, how does consequence-tiered expected-loss verdict selection change intervention behavior, attack success and utility, across a declared range of loss structures? *Evidence:* observe-only policy analysis of recorded steps, and a replay sensitivity analysis.
- **RQ3 (mitigation and cost).** What residual attack success remains after the Modify mechanism, how often is escalation selected, and what per-step processing time does REM add? *Evidence:* replay sensitivity analysis and runtime measurement. Residual success against live, adaptive agents is not measured.
- **RQ4 (component contribution).** What is the marginal contribution of each evidence group, of calibration, and of consequence tiers, as determined by ablation? *Evidence:* offline and observe-only ablations, and replay.

No research question was added after the pilot. The analyses added in November 2026 (rule baselines, a double-holdout evaluation, robustness probes and a confirmatory run on recordings unread until then; Chapter 3, Sections 3.11.11–3.11.14) bear on RQ2 and RQ4. An exploratory extension investigated on 13 November 2026 (Chapter 3, Section 3.14) asks, within the same questions, whether task-permission evidence compiled from the user's request improves the trade-off and which component is responsible.

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
- Runtime interception of tool calls, probability calibration and a four-way set of graduated verdicts all have precedents (Chapter 2, Section 2.12.3).
- In REM, declared costs play the role that hand-chosen thresholds play in threshold policies: the threshold between two verdicts follows from the declared cost ratio for the action's consequence tier (Chapter 3, Section 3.7.5).

**One versioned amendment is proposed.** The evaluation found that the behavioral evidence group lowers legitimate task completion without a measured security benefit, and a confirmatory run on recordings unread until then supported removing it for task completion; its effect on security is not resolved (Chapter 4, Section 4.6.8). The original specification is referred to as **REM v1.0** and remains the frozen baseline. The same framework without the behavioral evidence group is referred to as **REM v1.1** and is a proposed amendment awaiting the supervisor's approval (Chapter 3, Section 3.13). Both are reported in every table that includes either.

## 1.9 Research Methodology

The research follows design science research. In design science, knowledge is produced by building an artifact that addresses an identified problem and evaluating it (Hevner et al., 2004), following the six activities of Peffers et al. (2007) (Chapter 3, Section 3.1.1). The artifact is REM.

The evaluation is quantitative and uses the AgentDojo banking environment (Debenedetti et al., 2024). Live agent runs with REM enforcing its verdicts require access to a language model, which was not available. The evaluation therefore rests on traces of real agents recorded by the benchmark authors (Chapter 3, Sections 3.11.1 and 3.11.10). It has five parts:

- **Offline classification** of recorded tool calls, under nested grouped cross-fitting that holds out one whole attack objective per fold (Chapter 3, Section 3.11.5).
- **Observe-only policy analysis**, in which verdicts are computed but not enforced.
- **Recorded-trace replay**, which re-executes recorded trajectories in the benchmark's sandbox with a policy that may withhold calls, assuming the agent does not adapt to refusals. REM is compared with a no-defense reference, a consequence-independent threshold baseline on the same estimator, and three rules that use no model (Chapter 3, Section 3.11.11). A double-holdout scheme tests user tasks and attack objectives that are both unseen (Chapter 3, Section 3.11.12).
- **A confirmatory replay** of one proposed modification on recordings that no analysis had read before that run, under a protocol and a decision rule committed before those recordings were opened (Chapter 3, Section 3.11.14).
- **An exploratory extension**, in which a deterministic permission rule compiled from the user's request, a published fixed-list policy (the manual banking policy of Progent) and learned variants are replayed on the same recordings under a protocol committed before their outcomes were computed (Chapter 3, Section 3.14). All of its results are development evidence.

The replay analysis is a proposed amendment to the original scope, which excluded replay-based estimation; its status is stated wherever its results are used. No result in this thesis comes from a live agent.

## 1.10 Scope

**In scope (Chapter 3, Section 3.1.4):**

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

The design rests on stated assumptions (Chapter 3, Table 3.3). Among them:

- REM can intercept tool calls and results without modifying the agent (AS-1);
- REM's own code, parameters and logs are protected from the adversary (AS-3);
- adversaries do not adapt to REM in the primary evaluation (AS-6).

## 1.11 Contributions: Proposed and Demonstrated

**Proposed contribution.** The contribution proposed at the design stage was empirical and integrative: the design and evaluation, on an open and executable banking benchmark under indirect prompt injection, of a non-invasive five-layer runtime layer that combines provenance-based action evidence, a calibrated per-step probability of adversarial inducement, verdict selection by minimum conditional risk with losses declared per consequence tier, and deterministic mitigation.

**What the thesis demonstrates**, with the evidence for each item (Chapter 5, Table 5.3 gives the precedent, code, experiment, result and limits of each):

1. **A specified, implemented and tested framework.** REM is specified in Chapter 3 and implemented so that an undeclared design value stops the software. *Evidence:* 278 passing software tests and exact re-execution of the pilot (Chapter 3, Section 3.15; Chapter 4, Section 4.1.3).
2. **A controlled evaluation protocol.** It isolates the decision rule from the estimator, holds out whole attack objectives, adds a double holdout of user task and attack objective, compares the learned policy with rules that use no model and with one published policy replayed in the same harness, and includes one confirmatory run under a pre-committed protocol. *Evidence:* Chapters 3 and 4.
3. **Measured security and its cost.** In replay, REM v1.0 reduces attack success from 22.6% to 0.4% on the primary recordings and from 21.1% to 0.15% on the second population. It completes 31% of benign tasks where the undefended agent completes 52% (Chapter 4, Sections 4.6.3 and 4.6.8).
4. **A confirmed gain in task completion within the framework.** Removing the behavioral evidence group raises task completion by 7.5 percentage points (95% interval 1.2 to 16.0) on 2,113 episodes that were unread before that run, with 1 successful attack against 3 of 2,065. The pre-declared decision rule was met; the security difference is not resolved statistically (Chapter 4, Section 4.6.8).
5. **Negative results.** Four are documented (Chapter 5, Section 5.5): behavioral evidence did not help; an authorization-aware policy supervised on intervention outcomes did not transfer to an unseen attack objective; a rule that trusts documents named by the user was unsafe; and exact-string provenance failed when an identifier was reformatted.
6. **An identified limit of provenance evidence.** None of the policies tested up to 11 November, learned or rule-based, separates an authorized payment from an unrequested one whose details appear in the user's words. Their evidence describes where a call's arguments come from, not what the user asked for (Chapter 4, Section 4.6.7).
7. **An exploratory extension with an attribution result.** A deterministic rule that compiles the user's request and matches operation, recipient and amount completes more benign tasks than REM v1.0 with no more successful attacks, on development data. Its advantage over the strongest simple rule is not resolved; a published fixed-list policy is better on security; and a learned model on the same evidence adds no demonstrated value. The gain is due to the rule and not to the learned core (Chapter 4, Sections 4.4.3, 4.5.3 and 4.6.9).

**What the thesis does not demonstrate:**

- that REM adds value over simple provenance or authorization rules: on the second population neither REM version is distinguishable from them (Chapter 4, Section 4.6.8);
- that the learned, consequence-aware core is what improves the trade-off: the improvements that were observed came from removing evidence and from deterministic rules;
- any effect on live agents: a closed-loop harness is implemented and tested with scripted agents and was not executed with a language model (Chapter 4, Section 4.4.4);
- any difference in effect among Modify, Escalate and Block, which coincide in this evaluation;
- results under supervisor-approved design values, or with human-audited labels;
- any comparison with a published defense that needs a language model; the one published policy that was replayed has no successful attack and completes more tasks than REM (Chapter 4, Section 4.4.3).

**What the thesis does not claim:** a new algorithm; the first runtime guardrail, calibrated agent risk score or consequence-aware controller; that calibration improves control; robustness against adaptive adversaries; any prevention guarantee; that the tested features establish what the user authorized; that the permission rule of the extension generalizes beyond the benchmark's requests; or validity in production financial deployment. Each constituent mechanism is established and attributed to its source (Chapter 2, Table 2.2).

## 1.12 Thesis Organization

The thesis is organized in five chapters:

- **Chapter 1** introduces the background, problem, gap, aim, objectives, research questions, approach, scope and contributions.
- **Chapter 2** reports a record-level systematic review of runtime security for tool-using AI agents, three dated literature updates that lie outside that review, a comparison of the closest prior work, and the research gap.
- **Chapter 3** specifies the research methodology and the design of REM (architecture, threat model, evidence, estimator, calibration, consequence tiers, expected-loss decision, mitigation, audit), the experimental methodology, baselines, ablations and metrics, the proposed amendment REM v1.1, and the implementation.
- **Chapter 4** is organized in six sections: implementation tools and environment; dataset preparation and training; experimental setup and evaluation metrics; comparisons with existing models and defense frameworks; ablation studies; and results and discussion. It states that no live-agent experiment was executed and that the one published policy evaluated was replayed on recorded episodes.
- **Chapter 5** answers the research questions, assesses the objectives and contributions, records the rejected variants and the negative findings, and ends with limitations and future work.

Appendices A to F hold the evidence matrix of the review, the implementation details, the equation provenance table, the design and status of the live-agent and MELON evaluations, the sensitivity analysis of the mitigation semantics, and the register of open supervisor decisions.
