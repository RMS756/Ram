# CHAPTER ONE

# INTRODUCTION

## 1.1 Background

Large language model (LLM) agents use a language model as the controller of a system that perceives, reasons, plans and acts in pursuit of a task (L. Wang et al., 2024). In the execution pattern made explicit by ReAct (Yao et al., 2023), the model interleaves reasoning with actions, and the observations returned by those actions re-enter its context and shape the next step. Tool-using agents act through calls to external tools with arguments that the model generates.

When such an agent operates in a financial setting, a single proposed tool call can have direct external effects:

- initiate a payment;
- schedule or alter a recurring payment;
- change account credentials;
- send customer data to an external recipient.

The security question therefore shifts from what a model says to what an agent does: to the moment at which a proposed action crosses from the agent into its environment (Chapter 2, Section 2.1).

## 1.2 Problem Statement

An agent receives input through channels of different trustworthiness:

- the system prompt;
- the user's request;
- tool outputs;
- retrieved content;
- stored memory.

Indirect prompt injection exploits the difference. Content from an external source, processed by the agent, alters its behavior without any access to the user channel (OWASP Gen AI Security Project, 2025; Greshake et al., 2023). Benchmarks designed for tool-using agents show that the threat is practical, including in environments with financial tools (Debenedetti et al., 2024; Zhan et al., 2024; H. Zhang et al., 2025). The attack-success rates they report depend strongly on benchmark, model and attack template, and they cannot be pooled across studies (Chapter 2, Sections 2.4–2.5).

Defenses can intervene at several points: at the input, inside the model, in the system architecture, or at the moment a proposed action is about to be executed (Chapter 2, Section 2.6). **This thesis chooses the last of these, the action boundary, as its point of intervention.** It is the point at which an induced financial action becomes visible as a concrete tool call with concrete arguments, and at which it can still be withheld before it takes effect. It is not the only place where an attack can be stopped, and other defenses act earlier.

A defense placed at the action boundary must decide, for each proposed tool call, whether to release it, modify it, refer it for human review or block it. Two questions about that decision are not settled by the reviewed literature (Chapter 2, Sections 2.9 and 2.12):

- how an estimated probability that an action was adversarially induced should be combined with the consequence of that action when choosing among responses;
- how often each response is chosen, and at what cost to legitimate work.

The problem addressed in this thesis is the runtime compromise of tool-using financial agents through indirect prompt injection. The thesis designs a decision layer at the action boundary that addresses these two questions, and evaluates it on recorded agent behavior in a banking environment.

## 1.3 Motivation

Three considerations motivate the work.

**Concrete financial consequences.** Tools that transfer value, modify payments or change credentials expose money, account control and personal data to manipulation (Chapter 2, Section 2.10). Conventional evaluation of financial LLM agents, based on accuracy and return metrics, has been argued to give an illusion of reliability while overlooking vulnerabilities such as adversarial prompt manipulation (Z. Chen, J. Chen, et al., 2025).

**Record-keeping and human control.** Regulation (EU) 2024/1689 requires high-risk AI systems to allow the automatic recording of events and effective human oversight, including the ability to intervene (European Parliament & Council of the European Union, 2024). Whether a given financial agent falls within a high-risk category is not assessed here. The provisions motivate two design properties: an audit record for every decision and an explicit route to human review.

**Fragile evaluation.** Pitfalls in the design and evaluation of learning-based security systems lead to unrealistic performance estimates (Arp et al., 2022). Audits of agent-safety benchmarks report metric flaws, inconsistent rankings and contradictory conclusions across benchmarks (Y. Wang et al., 2026; M. Q. Li et al., 2026). A defense for financial agents must therefore be evaluated so that:
- attack success is reported together with benign utility;
- dependence between benchmark tasks is respected;
- leakage between fitting and test data is controlled.

## 1.4 Research Gap

The gap is not the absence of runtime guardrails, probability calibration, graduated interventions, human review, provenance analysis or consequence-aware control. Each of these is present in the reviewed literature (Chapter 2, Section 2.13.3). Several recent systems are close to the design studied here:

- **NEXUS** is a structured-plan safety monitor that applies a formal intervention policy to choose among allow, block, request confirmation and request revision. It combines deterministic rules, argument-level inspection and a calibrated logistic-regression risk score (Hossain et al., 2026).
- **AgentTrust** intercepts tool calls before execution and returns one of four verdicts, combining a normalizer, multi-step chain detection and an LLM judge for ambiguous inputs (C. Yang, 2026).
- **H.-H. Chen (2026)** prices the consequence of agent actions against a safe default before execution.
- **FinHarness** addresses runtime safety of financial agents through monitors and an LLM-judge cascade (Jia et al., 2026).
- **C. Zhang et al. (2026)** show that calibrating a risk score need not improve the decisions taken with it.

A currency update of 30 October 2026 found further records close to this design, among them a controller that commits the proposed or an alternative action by a calibrated value learned from outcomes (Yan et al., 2026) and a three-way execute–confirm–block router with calibrated probabilities (Xin, 2026). They were examined at abstract level only and lie outside the systematic review (Chapter 2, Section 2.13.6).

The systematic review of Chapter 2 was conducted at record level: full texts could not be retrieved. Within that limit, the gap it supports is **empirical** (Chapter 2, Section 2.13.2). The review found three things:
- limited and conflicting evidence on whether behavioral and provenance evidence improves runtime decisions, and none testing it as input to a calibrated estimator for financial actions;
- no verified quantitative evaluation of a runtime defense on financial actions in an open, executable benchmark;
- no evaluation comparing a consequence-aware decision with a consequence-independent baseline that shares its estimator, with attack success, benign utility, intervention behavior, calibration and latency reported separately.

The specific combination that REM implements was not found in the records examined. Because the combination is specific and the review was record-level, its absence is not used as evidence of originality.

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

## 1.8 Proposed Approach

The Runtime Evaluation and Mitigation (REM) framework is a runtime mediation layer placed between one agent and its environment. It treats the agent as opaque: it observes inputs, context, proposed actions and tool results, but not model parameters or internal reasoning (Chapter 3, Section 3.3.1). REM comprises exactly five layers (Chapter 3, Section 3.2.1):

1. **Input & Context Layer.** Captures the information the agent handles and the action it proposes, and labels each context segment with its provenance.
2. **Detection Layer.** Computes evidence about untrusted context.
3. **Behavioral Analysis Layer.** Computes evidence about the episode history and the proposed action.
4. **Decision Engine Layer.** Performs five steps:
   - estimates the probability that the proposed action is adversarially induced, using ridge logistic regression (Cox, 1958; le Cessie & van Houwelingen, 1992);
   - calibrates that probability on the logit (Platt, 1999; Guo et al., 2017);
   - assigns a declared consequence tier and applies policy predicates;
   - selects the verdict among Allow, Modify, Escalate and Block by minimizing conditional risk under tier-indexed losses (Elkan, 2001; Chow, 1970);
   - writes an audit record.
5. **Mitigation Layer.** Executes the mechanism associated with the verdict.

Offline fitting and recalibration are cross-cutting activities performed between deployments; they are not a layer. A linear attribution of the logit (Lundberg & Lee, 2017) is written to the audit record and never influences the verdict.

**None of these elements is new.**
- Runtime interception of tool calls, probability calibration and a four-way set of graduated verdicts all have precedents (Chapter 2, Section 2.13.3).
- In REM, declared costs play the role that hand-chosen thresholds play in threshold policies: the threshold between two verdicts follows from the declared cost ratio for the action's consequence tier (Chapter 3, Section 3.7.5).

## 1.9 Research Methodology

The research follows design science research. In design science, knowledge is produced by building an artifact that addresses an identified problem and evaluating it (Hevner et al., 2004), following the six activities of Peffers et al. (2007) (Chapter 3, Section 3.1.1). The artifact is REM.

The evaluation is quantitative and uses the AgentDojo banking environment (Debenedetti et al., 2024). It compares REM with a baseline that uses the same estimator but a consequence-independent decision rule. A further configuration gives both the same opportunity to escalate, so that the effect of consequence tiers can be separated from the effect of escalation. Estimation, calibration and threshold selection use nested grouped cross-fitting, because the benchmark does not support independent partitions (Chapter 3, Sections 3.11.4–3.11.5).

Live agent runs with REM enforcing its verdicts require access to a language model, which was not available. The evaluation therefore rests on traces of real agents recorded by the benchmark authors, used in three ways (Chapter 3, Sections 3.11.1 and 3.11.11):
- **offline classification** of recorded steps;
- **observe-only policy analysis**, in which verdicts are computed but not enforced;
- a **replay sensitivity analysis** that re-executes recorded trajectories under REM, assuming the agent does not adapt to refusals.

The replay analysis is a proposed amendment to the original scope, which excluded replay-based estimation; its status is stated wherever its results are used.

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

## 1.11 Contributions: Proposed and Achieved

**Proposed contribution.** The contribution proposed in Chapter 3 (Section 3.13) is empirical and integrative. It is the design and evaluation, on an open and executable banking benchmark under indirect prompt injection, of a non-invasive five-layer runtime layer that combines:
- provenance-based action evidence;
- a calibrated per-step probability of adversarial inducement;
- verdict selection by minimizing conditional risk with losses declared per consequence tier;
- deterministic mitigation whose effectiveness is measured.

It is compared against a consequence-independent baseline on the same estimator.

**What this thesis achieves**, and the evidence for each item (Chapters 4–6):

1. **A specified and implemented framework.** The framework is specified (Chapter 3) and implemented, with undeclared design values stopping the software rather than being replaced by defaults (Chapter 4). REM was placed at the tool-execution boundary of the benchmark without modifying the agent. *Evidence:* software tests and integration runs.
2. **An evaluation protocol** that isolates the decision rule from the estimator, and consequence tiers from escalation opportunity. It uses grouped cross-fitting that holds out whole attacker objectives. *Evidence:* the protocol and its execution (Chapter 5).
3. **Exploratory empirical evidence** on traces of 21 real LLM agents. It covers three kinds of analysis: offline discrimination and calibration; observe-only verdict behavior; and a replay sensitivity analysis of attack success and utility. *Evidence:* exploratory, from one benchmark, without live enforcement.

**What this thesis does not achieve:**
- an evaluation of enforcement against live agents;
- confirmatory results under supervisor-approved design values;
- a human audit of the labels;
- any per-backbone conclusion.

**What the thesis does not claim:**
- a new algorithm;
- the first runtime guardrail, calibrated agent risk score or consequence-aware controller;
- that calibration improves control;
- robustness against adaptive adversaries;
- any prevention guarantee;
- validity in production financial deployment.

Each constituent mechanism is established and attributed to its source (Chapter 3, Table 3.16).

## 1.12 Thesis Organization

The thesis is organized in six chapters:

- **Chapter 1** introduces the problem, gap, aim, objectives, research questions, approach and scope.
- **Chapter 2** reports a record-level systematic review of runtime security for tool-using AI agents and states the research gap it supports.
- **Chapter 3** specifies the research methodology and the design of REM: its architecture, threat model, algorithms and equations, runtime procedure, experimental methodology and metrics.
- **Chapter 4** reports the implementation, the integration with AgentDojo, the verification of the software, and the correspondence between Chapter 3 and the code.
- **Chapter 5** reports the exploratory evaluation, with its limits and negative results.
- **Chapter 6** discusses the findings against the objectives, research questions and prior work, separates achieved from proposed contributions, and concludes with future work ordered by dependency.
