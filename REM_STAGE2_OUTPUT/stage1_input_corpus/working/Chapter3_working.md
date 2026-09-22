# CHAPTER THREE

# RESEARCH METHODOLOGY AND DESIGN OF THE REM FRAMEWORK

## 3.1 Research Methodology and System Scope

### 3.1.1 Design science research

This thesis follows design science research, in which knowledge is produced by building an artifact that addresses an identified problem and evaluating it rigorously (Hevner et al., 2004). The research process follows the six activities of the design science research methodology of Peffers et al. (2007). Table 3.1 maps these activities to the thesis.

**Table 3.1. Design science research activities in this thesis**

| Activity (Peffers et al., 2007) | Realization in this thesis | Location |
|---|---|---|
| Problem identification and motivation | Runtime compromise of tool-using financial agents through indirect prompt injection | Chapter 1; Chapter 2 |
| Definition of objectives for a solution | Objectives O1–O3; research questions RQ1–RQ4; security objectives SO-1 to SO-6 | Sections 3.1.2, 3.1.3, 3.3.7 |
| Design and development | Five-layer REM architecture and its runtime pipeline | Sections 3.2–3.10 |
| Demonstration | Integration of REM with the AgentDojo banking environment | Chapter 4 |
| Evaluation | Controlled experiments, baseline comparison, and ablation | Sections 3.11–3.12; Chapter 5 |
| Communication | Thesis and derived publications | Chapter 6 |

The evaluation is quantitative and experimental. REM is compared against a baseline that uses the same probability estimator but a consequence-independent decision rule, so that differences in outcomes can be attributed to the decision rule rather than to the estimator.

### 3.1.2 Research objectives

The approved objectives are:

- **O1:** Design a REM framework for financial AI agents' and task automation agents' security.
- **O2:** Evaluate the framework against adversarial attacks.
- **O3:** Compare performance with existing security approaches.

This chapter realizes O1 through the architecture and runtime pipeline, O2 through the attack scenarios and metrics of Sections 3.11–3.12, and O3 through the baselines of Section 3.11.7. The evaluation in this thesis uses a financial (banking) environment. Task-automation environments are outside the evaluation scope unless approved as an extension.

### 3.1.3 Research questions

The approved proposal does not state research questions. The following questions are derived from the objectives and are presented for supervisor confirmation.

- **RQ1 (estimation).** How well does a ridge logistic regression estimator, using context, behavioral, and action evidence available at the tool-call boundary, discriminate adversarially induced proposed actions in the AgentDojo banking environment, and how well calibrated are its probabilities under grouped cross-fitting?
- **RQ2 (decision).** Compared with a consequence-independent threshold policy that uses the same estimator, how does consequence-tiered expected-loss verdict selection change attack success, benign utility, utility under attack, and intervention rates, across a declared range of loss structures?
- **RQ3 (mitigation and cost).** What residual attack success remains after the Modify mechanism, how often is escalation selected, and what per-step latency does REM add?
- **RQ4 (component contribution).** What is the marginal contribution of each evidence group, of calibration, and of consequence tiers, as determined by ablation?

**Table 3.2. Traceability of research questions**

| RQ | Objectives | Principal components | Principal metrics |
|---|---|---|---|
| RQ1 | O1, O2 | Detection and Behavioral Analysis evidence; estimator; calibration | ROC-AUC, PR-AUC, ECE, log-loss |
| RQ2 | O2, O3 | Consequence tiers; expected-loss decision; baseline policy | ASR, benign utility, utility under attack, intervention rates, realized loss |
| RQ3 | O2 | Mitigation Layer; Escalate; runtime pipeline | Residual ASR under Modify, escalation rate, latency |
| RQ4 | O2 | All components (ablation) | Change in the metrics above |

### 3.1.4 Scope

**In scope:**
- A single LLM-based agent that invokes tools with generated arguments.
- A financial (banking) task environment with executable tools and state-based checks.
- Indirect prompt injection through tool outputs as the evaluated attack class.
- Runtime mediation of each proposed tool call before it is released.

**Out of scope:**
- Training-time defenses and modification of the agent's model or prompts.
- Multi-agent systems.
- Evaluation against adaptive adversaries who tune attacks to REM.
- Production deployment in a financial institution.
- Counterfactual estimation of intervention value by replaying agent trajectories.

### 3.1.5 Assumptions

**Table 3.3. Assumptions**

| ID | Assumption | Type | Status |
|---|---|---|---|
| AS-1 | REM can intercept each proposed tool call and each tool result without modifying the agent's internals. | Architectural | To be demonstrated on the chosen platform (Chapter 4) |
| AS-2 | Context segments can be attributed to their source channel reliably enough to assign a provenance label. | Architectural | To be demonstrated |
| AS-3 | The adversary cannot modify REM's code, parameters, policy, or logs. | Architectural | Assumed; stated as a limitation |
| AS-4 | The user's objective is legitimate; REM protects the user against external manipulation. | Scoping | Stated choice |
| AS-5 | Tool outputs and retrieved content are untrusted by default. | Scoping | Follows from the indirect injection threat (Greshake et al., 2023) |
| AS-6 | Adversaries do not adapt to REM's parameters in the primary evaluation. | Scoping | Declared limitation |
| AS-7 | Observable evidence separates adversarially induced from benign proposed actions. | Empirical | Tested in pilot E0 (Section 3.11.8) |
| AS-8 | The benign reference data are representative of the evaluated workload. | Empirical | Threatened by benchmark scope (Section 3.14) |
| AS-9 | LLM non-determinism is bounded enough for repeated runs to characterize variance. | Empirical | Measured through repeated runs |
| AS-10 | The agent's internal reasoning is not used; REM relies only on observable inputs, proposed actions, and tool results. | Architectural | Design constraint |

### 3.1.6 Notation

**Table 3.4. Notation used in this chapter**

| Symbol | Meaning |
|---|---|
| t, T | Step index within an episode; episode length |
| g | User objective of the episode |
| c_{t} | Context at step t, as segments with provenance labels |
| a_{t} | Proposed action (tool name and arguments) at step t |
| H_{t} | Episode history up to step t |
| y_{t} ∈ {0, 1} | Latent label: 1 if a_{t} is adversarially induced |
| x_{t} ∈ [0, 1]^{d} | Evidence vector; groups x^{ctx}, x^{beh}, x^{act} with index sets I_{ctx}, I_{beh}, I_{act} |
| β_{0}, β, λ | Logistic intercept, coefficient vector, ridge strength |
| s_{t} | Logit (linear predictor) |
| p̃_{t}, p_{t} | Uncalibrated probability; calibrated probability |
| γ_{1}, γ_{0} | Calibration slope and intercept |
| z_{t}, k_{t}, κ | Consequence descriptors; consequence tier; tier map |
| 𝒱 | Verdict set {Allow, Modify, Escalate, Block} |
| 𝒱(a_{t}) | Verdicts feasible for a_{t} |
| v_{t} | Verdict issued at step t |
| L(v, y, k) | Loss of verdict v when the label is y and the tier is k |
| C_{miss}(k), C_{FA}(k), C_{mod}(k), C_{esc} | Declared costs of a missed attack, a false intervention by Block, Modify on a legitimate action, and escalation |
| r_{mod}(k) | Residual attack-success rate after Modify at tier k (measured) |
| R_{t}(v) | Conditional risk of verdict v at step t |
| π_{v,v′}(k), p^{*}_{k} | Indifference threshold between verdicts v and v′; Allow–Block threshold |
| σ(·) | Logistic function, σ(u) = 1 / (1 + exp(−u)) |
| Π, k_{D2} | Set of prohibited actions; minimum tier for predicate D2 |
| θ(α), α_{blk}, α_{mod} | Baseline threshold for false-positive target α; targets for Block and Modify |
| 𝒯_{R} | Set of tools to which the Modify mechanism applies |

Symbols used only in the optional sequential analysis are defined in Section 3.11.10. Symbols that appear in a single equation, such as Δ_{0}, Δ_{1}, B_{m}, and the step sets D_{fit}, D_{cal}, and D_{val}^{benign}, are defined where they are used. Each symbol has one meaning throughout the chapter.

## 3.2 REM Architecture

### 3.2.1 Five layers

REM is a runtime mediation layer between one agent and its environment. It comprises exactly five layers, as approved in the research proposal:

1. **Input & Context Layer.** Captures the information the agent handles and the action it proposes, and labels each context segment with its provenance.
2. **Detection Layer.** Computes evidence about untrusted context.
3. **Behavioral Analysis Layer.** Computes evidence about the episode history and the proposed action.
4. **Decision Engine Layer.** Estimates the probability that the proposed action is adversarially induced, assigns a consequence tier, applies policy predicates, selects a verdict, and writes the audit record.
5. **Mitigation Layer.** Executes the mechanism associated with the verdict.

Offline fitting and recalibration (Section 3.9) are cross-cutting activities performed between deployments. They are not a layer, are not numbered with the layers, and never change REM's parameters during an episode.

### 3.2.2 Topology and information flow

At each step, REM executes Layer 1, then Layers 2 and 3 in parallel on Layer 1's output, then Layer 4, then Layer 5, before the proposed action is released to the environment. The Detection and Behavioral Analysis Layers compute their evidence independently; they are combined only in the Decision Engine. This independence allows an evidence group to be removed in ablation without changing the computation of the other. After an action is released, its tool result re-enters Layer 1 as untrusted content for the next step.

**Figure 3.1. REM architecture.** The figure is to be drawn with the following elements and no others:

- **External elements:** user and system inputs; tool outputs and retrieved content (untrusted); the agent (opaque); tools and environment; human reviewer.
- **Five layer boxes:**
  - L1: capture and normalization; provenance labeling; entity extraction.
  - L2: injection-classifier score; instruction-pattern indicator.
  - L3: history tracker; behavioral features; action features.
  - L4: logistic estimation; calibration; consequence tier; policy predicates; expected-loss verdict with four outputs; audit record.
  - L5: release; tool restriction; withhold and escalate; block with safe fallback.
- **Stores (not layers):** declared policy; frozen parameters; audit log.
- **Cross-cutting box** (dashed, outside the layer stack): offline fitting and recalibration, connected to the audit log and to the frozen parameters.
- **Runtime arrows:** from L1 to L2 and L3 in parallel; from L2 and L3 to L4; from each verdict to its mechanism in L5; from L5 to the environment or back to the agent.

No arrow connects the offline box to the runtime path within an episode.

### 3.2.3 Layer interfaces

**Table 3.5. Layer interfaces**

| Layer | Consumes | Produces |
|---|---|---|
| L1 Input & Context | Objective, system prompt, user messages, tool results, proposed action | Labeled context c_{t}; entities with provenance; held action a_{t} |
| L2 Detection | Untrusted segments of c_{t} | Context evidence x^{ctx} |
| L3 Behavioral Analysis | H_{t}, a_{t}, entities, benign reference transitions, privilege map | Behavioral evidence x^{beh}; action evidence x^{act} |
| L4 Decision Engine | x_{t}, consequence descriptors z_{t}, frozen parameters, declared policy | p_{t}, k_{t}, R_{t}(·), verdict v_{t}, audit record |
| L5 Mitigation | v_{t}, a_{t}, episode restrictions | Released, restricted, withheld, or refused action |

The four functions are separated architecturally. Layers 2 and 3 produce evidence and issue no verdicts. Layer 4 performs probability estimation and decision. Layer 5 performs mitigation.

## 3.3 Threat Model and Financial Action Boundary

### 3.3.1 Protected system

The protected system is a single LLM-based agent that pursues a user objective by proposing tool calls. REM treats the agent as opaque: it observes inputs, context, proposed actions, and tool results, but not model parameters or internal reasoning (AS-10). The evaluation instance is an agent operating the AgentDojo banking environment (Debenedetti et al., 2024), described in Section 3.11.2.

### 3.3.2 Episodes and steps

An episode is one execution of the agent on one user objective g. It is a finite sequence of steps t = 1, …, T, where step t is the interval in which the agent proposes action a_{t}. At step t, REM observes g, the labeled context c_{t}, the proposed action a_{t}, and the history H_{t} of prior contexts, actions, verdicts, and tool results.

### 3.3.3 Trust boundaries and untrusted content

**Table 3.6. Trust boundaries**

| ID | Boundary | Direction | Treatment in REM |
|---|---|---|---|
| TB-1 | User input | User → agent context | Labeled semi-trusted |
| TB-2 | Observation | Tool outputs and retrieved content → agent context | Labeled untrusted; primary observation point |
| TB-3 | Action | Agent → tools and external systems | Primary enforcement point |
| TB-4 | Memory | Context ↔ persistent store | Provenance retained on read and write (design scope only) |

**Untrusted content** is any context segment that entered through TB-2 or TB-4, or that was derived from such a segment. The observation boundary matters because content arriving there enters after the user's request, which is the route exploited by indirect prompt injection (Greshake et al., 2023; OWASP Gen AI Security Project, 2025). The action boundary matters because it is the last point at which an induced action can be prevented rather than repaired.

### 3.3.4 Adversary model

- **AD-1, content-control adversary (primary, evaluated).**
  - *Can:* author or modify content that the agent receives through tool outputs, including instruction-like text and values such as account identifiers.
  - *Cannot:* access the user channel, observe or modify REM's parameters, or modify agent or REM code.
- **AD-2, prompt-channel adversary (design scope only).** Can submit crafted input through a compromised user channel. The evaluated banking attacks do not exercise this channel.

**Excluded:**
- adversaries who modify model weights, agent code, or REM;
- infrastructure compromise;
- a malicious operator;
- adaptive adversaries (AS-6).

### 3.3.5 Indirect injection and adversarially induced actions

Indirect prompt injection occurs when content from an external source, processed by the agent, alters its behavior (OWASP Gen AI Security Project, 2025). REM's target event is narrower and defined at the action level.

A proposed action a_{t} is **adversarially induced** (y_{t} = 1) if executing it would advance an objective introduced by the adversary rather than the user objective g. The label is not observable at runtime. Actions that are unsafe because of the agent's own error without adversarial involvement are outside this definition. The operational derivation of y_{t} for evaluation data is given in Section 3.11.3.

### 3.3.6 Sensitive financial actions

Table 3.7 groups the tools of the evaluated banking environment by the consequence of an adversarially induced call. The tool names are those registered in the AgentDojo banking suite inspected for this chapter (Section 3.11.2). The grouping is a design classification, not a property reported by the benchmark.

**Table 3.7. Action categories in the banking environment**

| Category | Tools | Consequence if adversarially induced |
|---|---|---|
| Read | get_balance, get_iban, get_most_recent_transactions, get_scheduled_transactions, get_user_info, read_file | No direct external effect; may expose data later sent elsewhere |
| Value transfer | send_money, schedule_transaction | Money sent to an attacker-controlled account |
| Payment modification | update_scheduled_transaction | Redirection or alteration of a recurring payment |
| Credential change | update_password | Loss of control over the account |
| Profile change | update_user_info | Alteration of account holder information |

### 3.3.7 Security objectives

The threat model above states what an adversary can do; the objectives below state what REM must therefore do about it. They are ordered along the path of a single proposed tool call: from the evidence available about it, through the verdict selected for it, to the record left behind and the cost of producing it.

- **SO-1:** Use evidence about untrusted content that enters through TB-2.
- **SO-2:** Detect proposed actions whose arguments originate in untrusted content or that deviate from the episode's benign pattern.
- **SO-3:** Account for the consequence of the proposed action when selecting a verdict.
- **SO-4:** Provide human escalation as a response.
- **SO-5:** Emit, for every verdict, an audit record from which the verdict can be reproduced.
- **SO-6:** Preserve benign task utility and report per-step latency.

## 3.4 Input & Context Layer

The Input & Context Layer collects and labels information. It computes no risk evidence.

### 3.4.1 Context capture

At step t the layer receives:
- the user objective g and user messages (TB-1);
- the system prompt;
- the results of previously executed tools (TB-2);
- the proposed action a_{t}, captured at TB-3 and held until Layer 5 acts.

Invisible and formatting characters, such as zero-width characters, are removed from untrusted text before further processing. This is a deterministic hygiene step. It reduces some encoding-based concealment but does not prevent paraphrase-based evasion.

### 3.4.2 Provenance labeling

Each context segment receives one label from the ordered set trusted (system prompt) ≻ semi-trusted (user input) ≻ untrusted (tool output, retrieved content, memory). Content derived from several segments inherits the least-trusted label among them, and processing never promotes content to a more trusted label. This rule is a design definition that preserves the distinction between data and instruction exploited by indirect injection. It asserts no empirical claim.

### 3.4.3 Entity extraction

The layer extracts security-relevant entities from each segment and from the arguments of a_{t}, and records the provenance of each occurrence:
- account identifiers (such as IBAN-formatted strings);
- monetary amounts;
- password and credential values;
- user-profile values (such as addresses and phone numbers);
- tool names mentioned in text.

The extraction patterns are declared in configuration and are fixed before evaluation. These entities allow Layer 3 to ask whether an argument of the proposed action can be traced to the user objective or to trusted content, or only to untrusted content.

## 3.5 Detection Layer

The Detection Layer computes context evidence from untrusted segments. It issues no verdict.

**Table 3.8. Context evidence**

| Feature | Definition | Type | Availability |
|---|---|---|---|
| x^{ctx}_{1} | Maximum score of a fixed, pre-trained prompt-injection classifier over untrusted segments added since the previous step | [0, 1] | Derived (classifier choice pending supervisor approval) |
| x^{ctx}_{2} | 1 if an untrusted segment added since the previous step matches the declared instruction-pattern set; otherwise 0 | Binary | Derived (pattern set declared before evaluation) |

The classifier is used with fixed inference and is not retrained. A classifier distributed with an existing guardrail system, such as PromptGuard 2 in LlamaFirewall (Chennabasappa et al., 2025), is a candidate. The instruction-pattern set contains declared indicators such as imperative instructions addressed to an assistant, references to tool names, and role or delimiter markers.

Both features are individually evadable, and benchmark-based scores of detectors are fragile (Arp et al., 2022; M. Q. Li et al., 2026). The Detection Layer is therefore not relied upon to be decisive. Its evidence is combined with behavioral and action evidence in the Decision Engine, and its contribution is measured by ablation (Section 3.11.7).

## 3.6 Behavioral Analysis Layer

The Behavioral Analysis Layer maintains the episode history and computes evidence about the trajectory and the proposed action. All reference quantities it uses are estimated offline from benign data and are frozen at runtime.

### 3.6.1 Step tracking

The layer maintains H_{t}: the sequence of proposed actions, their arguments with provenance, the verdicts issued, and the tool results returned. H_{t} is reset at the start of each episode.

### 3.6.2 Behavioral and action evidence

**Table 3.9. Behavioral and action evidence**

| Feature | Definition | Type | Availability |
|---|---|---|---|
| x^{beh}_{1} | Post-observation shift: 1 if the most recent tool result was untrusted and had x^{ctx}_{2} = 1; otherwise 0 | Binary | Derived from H_{t} |
| x^{beh}_{2} | Repeated calls: min(n_{rep}, n_{max}) / n_{max}, where n_{rep} is the number of consecutive calls with the same tool and key arguments and n_{max} is declared | [0, 1] | Derived from H_{t} |
| x^{beh}_{3} | Privilege escalation: 1 if the privilege level of a_{t}'s tool exceeds the highest level used so far in the episode; otherwise 0 | Binary | Derived; privilege map declared |
| x^{beh}_{4} | Transition deviation: 1 if the pair (previous tool, current tool) does not occur in the benign reference transition set; otherwise 0 | Binary | Derived; reference set estimated on benign fitting data |
| x^{act}_{1} | Argument provenance: 1 if a key argument of a_{t} (recipient account identifier, amount, password, or profile value) occurs in untrusted content but not in g or trusted content; otherwise 0 | Binary | Derived from L1 entities |
| x^{act}_{2} | Destination novelty: 1 if the recipient of a_{t} appears neither in g nor among the transactions observed before the episode's first untrusted ingestion; otherwise 0 | Binary | Derived; applicable to value-transfer and payment-modification tools |
| x^{act}_{3} | Sensitive egress: 1 if a_{t} sends to an external recipient a value obtained from a sensitive read (account identifier, profile value, or credential); otherwise 0 | Binary | Derived from L1 entities and H_{t} |

All features are bounded in [0, 1] by definition, so no further rescaling is applied. Three design rules govern them:

1. **No identity-based features.** No feature may encode a specific account identifier. In the evaluated benchmark, one attacker account identifier is shared by most injection tasks (Section 3.11.2), and a feature keyed on that value would leak the label.
2. **Evidence is kept separate from consequence.** Whether a payee appears only in untrusted content is evidence about *whether* an action is adversarially induced; it belongs in x_{t}. Whether the action transfers a large amount irreversibly describes *what would happen*; it belongs in the consequence descriptors z_{t} (Section 3.7.3) and enters the decision only through the loss.
3. **The feature set is frozen after pilot E0** (Section 3.11.8), before any held-out predictions are examined.

## 3.7 Decision Engine Layer

The Decision Engine turns evidence into a verdict in five stages: probability estimation, calibration, consequence assessment, policy predicates, and expected-loss verdict selection. It also writes the audit record. Each equation below states its source and whether it is established from the source, adapted from it, or derived here.

### 3.7.1 Ridge logistic estimation

The probability that the proposed action is adversarially induced is modeled by logistic regression (Cox, 1958):

$$ s_{t} = β_{0} + β^{⊤}x_{t},     p̃_{t} = σ(s_{t}) = 1 / (1 + exp(−s_{t})) $$ (3.1)

where x_{t} ∈ [0, 1]^{d} is the evidence vector [x^{ctx}; x^{beh}; x^{act}], β_{0} ∈ ℝ is the intercept, β ∈ ℝ^{d} is the coefficient vector, s_{t} is the logit, and p̃_{t} is the uncalibrated estimate of P(y_{t} = 1 | x_{t}).

*Role in REM:* maps the evidence of Layers 2 and 3 to a score and an uncalibrated probability.
*Status:* established from source (Cox, 1958).

The parameters are estimated offline by maximizing a ridge-penalized log-likelihood (le Cessie & van Houwelingen, 1992):

$$ (β̂_{0}, β̂) = argmax_{β_{0}, β} Σ_{i ∈ D_{fit}} [ y_{i} ln p̃_{i} + (1 − y_{i}) ln(1 − p̃_{i}) ] − λ ‖β‖²_{2} $$ (3.2)

where D_{fit} is the set of labeled fitting steps, y_{i} ∈ {0, 1} are their labels, p̃_{i} is given by Equation 3.1, and λ ≥ 0 controls the strength of the quadratic penalty. The intercept is not penalized.

*Role in REM:* produces finite and stable coefficients from small, imbalanced data with binary features.
*Status:* established from source.

The quadratic penalty is needed for a specific reason. The evidence features are mostly binary, and adversarial steps are scarce (Section 3.11.4). If a single indicator appears only in adversarial fitting steps, the unpenalized maximum-likelihood estimate does not exist as a finite value. The penalty keeps the estimates finite.

The exact scaling constant of the penalty in le Cessie and van Houwelingen (1992) is pending full-text verification. This does not affect the method: λ is selected by grouped cross-validation on held-out log-loss (Section 3.9), and rescaling the penalty by a positive constant changes the selected value of λ, not the set of attainable solutions. Software libraries often parameterize the penalty through an inverse strength; the mapping used in implementation will be documented from the library version used.

No interaction terms are included by default. Equation 3.1 assumes that the log-odds of adversarial induction are approximately linear in the evidence.

### 3.7.2 Calibration on the logit

The uncalibrated probability p̃_{t} need not agree with observed frequencies. Ridge shrinkage and class imbalance can both distort it. Because the decision rule in Section 3.7.5 treats the probability as a probability, REM recalibrates it with a two-parameter logistic map applied to the logit:

$$ p_{t} = σ(γ_{1} s_{t} + γ_{0}),     γ_{1} > 0 $$ (3.3)

where γ_{1} is the calibration slope and γ_{0} is the calibration intercept.

*Role in REM:* produces the calibrated probability used by the decision rule.
*Status:* adapted from source. The method is Platt scaling (Platt, 1999). The two-parameter logistic form with parameters fitted by negative log-likelihood on held-out data follows Guo et al. (2017). The map is applied here to the logit of a logistic regression model. The monotonicity condition follows Kull et al. (2017), who require a non-negative slope for a non-decreasing map; REM requires a strictly positive slope so that the ranking of steps is preserved.

The calibration parameters are fitted by minimizing the negative log-likelihood on held-out logits (Guo et al., 2017):

$$ (γ̂_{1}, γ̂_{0}) = argmin_{γ_{1}, γ_{0}} − Σ_{i ∈ D_{cal}} [ y_{i} ln p_{i} + (1 − y_{i}) ln(1 − p_{i}) ] $$ (3.4)

where D_{cal} is a set of steps whose logits s_{i} were produced by a model that was not fitted on those steps. Fitting Equation 3.4 on the model's own training logits would be close to degenerate, so REM uses out-of-fold logits from grouped cross-fitting (Section 3.9).

*Status:* established from source (Guo et al., 2017).

Four properties of this choice are stated.

1. **It changes probabilities, not rankings.** With γ_{1} > 0, Equation 3.3 is strictly increasing in s_{t}. Calibration therefore leaves ROC-AUC, PR-AUC, and any decision based only on the ordering of steps unchanged. If the fitted slope is not positive, calibration is rejected for that fit and the event is reported.
2. **It is the minimal adequate family.** Kull et al. (2017) prove that beta calibration with equal shape parameters equals logistic calibration applied to the log-odds of a score. Since p̃_{t} = σ(s_{t}), the log-odds of p̃_{t} is s_{t}, so Equation 3.3 is exactly beta calibration with equal shape parameters applied to p̃_{t}. The identity map is included (γ_{1} = 1, γ_{0} = 0). Full beta calibration adds a third parameter, and isotonic regression is nonparametric; neither is adopted, given the limited calibration data.
3. **It is not a contribution.** Calibrated logistic risk scores are already used in agent safety (Hossain et al., 2026).
4. **It does not guarantee good control.** C. Zhang et al. (2026) show that recalibrating a scalar risk score can improve calibration error while leaving control regret under threshold routing unchanged, because a scalar probability does not represent whether an intervention would improve the outcome. REM therefore reports calibration quality and control outcomes separately (Section 3.12) and does not claim that calibration improves control.

### 3.7.3 Consequence tiers

The consequence of a proposed action is described by descriptors z_{t} obtained from the action itself (Table 3.10). They are mapped to a consequence tier k_{t} = κ(z_{t}) ∈ {1, …, K} by a declared policy function κ. Consequence descriptors do not enter Equation 3.1; they affect the verdict only through the loss.

**Table 3.10. Consequence descriptors**

| Descriptor | Meaning | How obtained | Availability |
|---|---|---|---|
| Action category | Read, value transfer, payment modification, credential change, profile change (Table 3.7) | Tool name | Available |
| Amount | Monetary amount of a value-transfer or payment-modification call | Action arguments | Available where the tool takes an amount |
| Recurring-payment change | Whether the action alters a scheduled or recurring payment | Tool name | Available |
| Credential change | Whether the action changes account credentials | Tool name | Available |
| Irreversibility | Whether the effect is treated as irreversible once executed | Declared per tool | Proposed (policy); the benchmark does not simulate settlement |

**Table 3.11. Illustrative consequence tiers (policy pending supervisor approval)**

| Tier | Illustrative membership |
|---|---|
| 1 | Read tools |
| 2 | Profile change |
| 3 | Value transfer at or below a declared amount limit |
| 4 | Value transfer above the declared limit; payment modification; credential change |

The quantities used by the Decision Engine fall into three classes, which are kept distinct throughout the thesis.

**Table 3.12. Learned, measured, and policy quantities**

| Class | Quantities | How determined |
|---|---|---|
| Learned | β_{0}, β, γ_{1}, γ_{0} | Fitted on labeled data by Equations 3.2 and 3.4 |
| Measured | r_{mod}(k); benign reference mean x̄; benign transition set; utility impact of Modify | Estimated from observe-only and enforcing-mode runs |
| Policy | κ, amount limits, C_{miss}(k), C_{FA}(k), C_{mod}(k), C_{esc}, Π, k_{D2}, privilege map, tie-breaking order | Declared before evaluation; varied over a declared grid where they affect outcomes |

Policy quantities encode institutional judgment. They are not presented as empirical findings, and their influence is reported through the loss grid of Section 3.12.3.

### 3.7.4 Policy predicates

Two deterministic predicates are evaluated before verdict selection.

- **D1, prohibited action.** If a_{t} ∈ Π, the verdict is Block irrespective of p_{t}. A prohibition that a sufficiently low probability could override would not be a prohibition.
- **D2, missing required evidence.** If the evidence required for tier k_{t} cannot be computed (for example, argument provenance is unavailable) and k_{t} ≥ k_{D2}, the verdict is Escalate. Absent evidence is not treated as evidence of safety.

Π, k_{D2}, and the evidence required at each tier are declared policy. When a predicate applies, it determines the verdict, the expected-loss rule is not consulted, and the audit record names the predicate as the source of the verdict. Both predicates are disabled in one ablation (Section 3.11.7).

### 3.7.5 Expected-loss verdict selection

**Loss structure.** For each tier k, the loss of issuing verdict v when the label is y is given in Table 3.13.

**Table 3.13. Tier-indexed loss structure L(v, y, k)**

| Verdict v | L(v, 0, k): legitimate action | L(v, 1, k): adversarially induced action |
|---|---|---|
| Allow | 0 | C_{miss}(k) |
| Modify | C_{mod}(k) | r_{mod}(k) · C_{miss}(k) |
| Escalate | C_{esc} | C_{esc} |
| Block | C_{FA}(k) | 0 |

All declared costs are non-negative and expressed in common relative units. Correct automatic decisions are assigned zero loss, which is a declared convention. The Escalate entries assume a reviewer who resolves escalations correctly; this assumption is examined in Sections 3.12 and 3.14.

The adversarial Modify entry is a derivation. Under the stated assumption A-Mod — whether Modify neutralizes an adversarially induced action is independent of x_{t} given the tier, and the attack fails with probability 1 − r_{mod}(k) — the law of total expectation gives:

$$ L(Modify, 1, k) = r_{mod}(k) · C_{miss}(k) + (1 − r_{mod}(k)) · 0 = r_{mod}(k) · C_{miss}(k) $$ (3.5)

where r_{mod}(k) ∈ [0, 1] is the residual attack-success rate after Modify at tier k, measured in enforcing-mode runs (Section 3.11.7).

*Status:* derived under assumption A-Mod.

**Conditional risk.** Elkan (2001) states that the optimal prediction is the one that minimizes expected cost, computed from the conditional probability of each class and the cost of each prediction for each true class. REM applies this criterion to the four verdicts, with losses indexed by the consequence tier and the calibrated probability of Equation 3.3 in place of the true conditional probability:

$$ R_{t}(v) = (1 − p_{t}) · L(v, 0, k_{t}) + p_{t} · L(v, 1, k_{t}),     v ∈ 𝒱(a_{t}) $$ (3.6)

where R_{t}(v) is the conditional risk of verdict v at step t.

*Status:* adapted from source. Elkan's criterion is stated for predictions of classes. REM extends the set of choices to four verdicts, indexes the losses by consequence tier, and substitutes the calibrated estimate p_{t} for the true posterior. The substitution is justified only to the extent that p_{t} is calibrated.

**Bayes verdict.** The verdict is:

$$ v_{t} = argmin_{v ∈ 𝒱(a_{t})} R_{t}(v) $$ (3.7)

with ties resolved toward the more restrictive verdict in the declared order Block ⪰ Escalate ⪰ Modify ⪰ Allow.

*Status:* adapted from source; the tie-breaking order is a design definition that makes the rule a function.

The feasible set 𝒱(a_{t}) contains Allow, Escalate, and Block for every action, and Modify only if the tool of a_{t} belongs to the set 𝒯_{R} to which the Modify mechanism applies (Section 3.8).

**Derived thresholds.** Each R_{t}(v) is affine in p_{t}, so the verdict changes only where two conditional risks are equal. For verdicts v and v′ at tier k, let Δ_{0} = L(v′, 0, k) − L(v, 0, k) and Δ_{1} = L(v, 1, k) − L(v′, 1, k), with Δ_{0} + Δ_{1} > 0. Setting R(v) = R(v′) in Equation 3.6 and solving for p gives:

$$ π_{v,v′}(k) = Δ_{0} / (Δ_{0} + Δ_{1}) $$ (3.8)

*Status:* derived from Equation 3.6.

Derivation: R(v) − R(v′) = −Δ_{0} + p(Δ_{0} + Δ_{1}). This is zero at p = π_{v,v′}(k), negative below it (v is preferred), and positive above it (v′ is preferred).

For v = Allow and v′ = Block, Δ_{0} = C_{FA}(k) and Δ_{1} = C_{miss}(k), so:

$$ p^{*}_{k} = C_{FA}(k) / (C_{FA}(k) + C_{miss}(k)) $$ (3.9)

*Status:* derived from Equation 3.8. It has the form of the standard two-class cost-sensitive threshold for zero-cost correct decisions, which Elkan (2001) obtains from the same expected-cost criterion; the printed threshold expression in that paper could not be inspected directly during verification, so the derivation above stands on Equation 3.8 alone.

Thresholds are therefore consequences of declared costs rather than independently chosen constants. The question "why this threshold?" becomes "why this cost ratio?", which the loss grid of Section 3.12.3 addresses.

**When escalation can be selected.** Chow (1970) analyzed the tradeoff between recognition error and rejection, which is the classical basis for withholding an automatic decision. In REM, Escalate is not implemented as a separate rejection test; it is one of the verdicts inside Equation 3.7. For the verdict set {Allow, Escalate, Block} at tier k, Escalate is selected for some probability if and only if:

$$ C_{esc} < C_{FA}(k) · C_{miss}(k) / (C_{FA}(k) + C_{miss}(k)) $$ (3.10)

*Status:* derived from Equations 3.6, 3.7, and 3.9.

Derivation: R(Allow) = p · C_{miss}(k) increases in p and R(Block) = (1 − p) · C_{FA}(k) decreases in p. Their minimum is largest at p^{*}_{k}, where it equals C_{FA}(k) · C_{miss}(k) / (C_{FA}(k) + C_{miss}(k)). The constant C_{esc} lies strictly below this minimum for some p if and only if Equation 3.10 holds; at equality, ties resolve toward Block.

When Modify is also feasible, Equation 3.10 remains a necessary condition, because adding a verdict can only lower the minimum risk. In the symmetric case C_{FA}(k) = C_{miss}(k) = C, Equation 3.10 reduces to C_{esc} < C/2: deferral is selected only when it costs less than half an error.

**Dominance check.** Before a loss structure is used, it is checked for dominated verdicts. For example, R(Modify) − R(Block) = (1 − p)(C_{mod}(k) − C_{FA}(k)) + p · r_{mod}(k) · C_{miss}(k), which is non-negative for every p whenever C_{mod}(k) ≥ C_{FA}(k). In that case Modify can never be selected at tier k. A declaration that makes a verdict unreachable, by this check or by Equation 3.10, is reported as such rather than silently producing a smaller verdict set.

### 3.7.6 Explainability and audit record

For every verdict the Decision Engine writes an audit record containing:
- the evidence vector x_{t}, the logit s_{t}, and the probabilities p̃_{t} and p_{t};
- the tier k_{t} and the conditional risks R_{t}(v);
- the verdict v_{t} and its source (D1, D2, or the expected-loss rule);
- the model, calibration, and policy versions;
- a linear attribution of the logit.

The attribution follows the linear case of Shapley-value attribution given by Lundberg and Lee (2017):

$$ φ_{t,i} = β_{i} (x_{t,i} − x̄_{i}),  i = 1, …, d;     φ_{0} = β_{0} + β^{⊤}x̄ $$ (3.11)

where x̄ is the mean evidence vector over benign fitting steps, φ_{t,i} is the contribution of feature i to the logit relative to that benign reference, and φ_{0} is the logit at the reference.

*Status:* adapted from source. Lundberg and Lee (2017) state the linear case under feature independence with printed indices that do not match between the two sides of the expression and with base value equal to the model intercept. REM uses the index-consistent form and sets the base value to the logit at the reference point, which is the value required by their local-accuracy property when the reference mean is not zero.

The decomposition is exact:

$$ φ_{0} + Σ_{i=1}^{d} φ_{t,i} = s_{t} $$ (3.12)

*Status:* derived. Summing Equation 3.11 gives β_{0} + β^{⊤}x̄ + β^{⊤}x_{t} − β^{⊤}x̄ = s_{t}. This is the local-accuracy property of Lundberg and Lee (2017) for a linear model, and REM checks it as a correctness invariant.

For reporting by evidence group, REM defines:

$$ Φ_{J} = Σ_{i ∈ I_{J}} φ_{t,i},     J ∈ {ctx, beh, act} $$ (3.13)

*Status:* design definition. Because the groups partition the features, Φ_{ctx} + Φ_{beh} + Φ_{act} = s_{t} − φ_{0}.

Four qualifications apply:

1. **The attribution never influences the verdict.** It is an audit component only.
2. **It decomposes the logit, not the calibrated probability.** On the calibrated logit scale each contribution is multiplied by γ_{1}, which preserves relative contributions because γ_{1} > 0.
3. **Correlation limits interpretation, not the identity.** The independence assumption affects the interpretation of each φ_{t,i} as a Shapley value when features are correlated; it does not affect the identity of Equation 3.12.
4. **It is not a contribution.** Auditable decision records are provided by several existing systems (Hossain et al., 2026; C. Yang, 2026). Because the attribution is determined by the logged x_{t} and the frozen parameters, it can equally be computed at audit time.

### 3.7.7 Consequence-independent baseline policy

The baseline uses the same estimator and calibration but a decision rule that ignores consequence. Its thresholds are selected as operating points on benign validation steps:

$$ θ(α) = min { θ : FPR_{val}(θ) ≤ α },     FPR_{val}(θ) = |{ i ∈ D_{val}^{benign} : p_{i} ≥ θ }| / |D_{val}^{benign}| $$ (3.14)

where α is a declared false-positive target, D_{val}^{benign} is the set of benign validation steps in the relevant cross-fitting fold, and θ ranges over the observed probabilities.

The baseline verdict is:
- **Block** if p_{t} ≥ θ(α_{blk});
- **Modify** if θ(α_{mod}) ≤ p_{t} < θ(α_{blk}) and Modify is feasible, otherwise Block;
- **Allow** otherwise.

The targets satisfy α_{mod} > α_{blk}. Predicates D1 and D2 apply as in Section 3.7.4, so the baseline issues Escalate only through D2.

*Status:* design definition.

Because Equation 3.14 selects thresholds by ranking, a strictly increasing recalibration re-selects equivalent thresholds and leaves the baseline's verdicts unchanged. Cost-derived thresholds such as Equation 3.9 are fixed in probability units and can change after recalibration. This contrast is used in the ablation of Section 3.11.7 and is consistent with the finding of C. Zhang et al. (2026) that recalibration need not change threshold-routed control.

## 3.8 Mitigation Layer

The Mitigation Layer executes, deterministically, the mechanism associated with each verdict. It never initiates an action on the agent's behalf.

**Table 3.14. Verdict-to-mitigation mapping**

| Verdict | Mechanism | Operation |
|---|---|---|
| Allow | Release | a_{t} is released across TB-3 and the event is logged. |
| Modify | Tool restriction | a_{t} is not executed. The tool class of a_{t} is removed from the agent's available tools for the rest of the episode, and a structured notice is returned to the agent, which may continue with its remaining tools. Applies only to tools in 𝒯_{R}. |
| Escalate | Withhold and refer | a_{t} is withheld and the audit record is presented to a human reviewer. The action is released only if the reviewer approves. |
| Block | Interrupt with safe fallback | a_{t} is not executed, every tool in 𝒯_{R} is restricted for the rest of the episode so that no further side-effecting action is released, and a structured refusal is returned to the agent. |

Tool restriction is the single Modify mechanism because it is deterministic, does not depend on an LLM rewriting content, and can be measured. Input sanitization, such as spotlighting (Hines et al., 2024), is an alternative that is not adopted as the primary mechanism.

Four properties are stated:

1. **Restrictiveness ordering.** Block halts all further side effects, Escalate defers the decision, and Modify removes one tool class. This ordering underlies the tie-breaking order of Equation 3.7.
2. **𝒯_{R} is declared.** In the banking environment it contains value-transfer, payment-modification, credential-change, and profile-change tools; read tools are not restricted.
3. **Mitigation effectiveness is measured, not assumed.** The residual attack-success rate r_{mod}(k) used in Equation 3.5 is estimated from enforcing-mode runs.
4. **Retries are observed.** A restricted or blocked agent may retry. Retries raise x^{beh}_{2}, and calls to restricted tools are refused by the Mitigation Layer.

## 3.9 Offline Fitting and Recalibration

Offline fitting and recalibration are cross-cutting activities. They are performed between deployments on logged data, they are not a layer, and they never modify REM's parameters during an episode. Runtime adaptation from observed traffic is excluded because it would allow an adversary who generates traffic to shift REM's reference behavior.

The offline procedure fits and freezes:
- the benign reference quantities (x̄ and the benign transition set);
- the coefficients by Equation 3.2, with λ selected by grouped cross-validation on held-out log-loss;
- the calibration parameters by Equation 3.4 on out-of-fold logits;
- the baseline thresholds by Equation 3.14;
- the measured residual rates r_{mod}(k).

It also checks the declared loss structure for dominated verdicts (Section 3.7.5) and records all model, data, policy, benchmark, and software versions.

Between deployments, calibration can be monitored against later-established labels using the metrics of Section 3.12. If calibration drifts beyond a declared tolerance, the procedure is repeated on new data.

**Procedure 3.1. Offline fitting (cross-cutting; never executed within an episode)**

```
Input: logged observe-only traces grouped by injection task and user task; labels y;
       declared policy (κ, L, Π, k_D2, privilege map, 𝒯_R, α_blk, α_mod)
1  for each outer fold f (Section 3.11.5):
2      D_train ← steps outside fold f;  D_test ← steps in fold f
3      estimate x̄ and the benign transition set on benign steps of D_train
4      select λ by grouped inner cross-validation on D_train (held-out log-loss)
5      obtain out-of-fold logits on D_train from inner folds; fit (γ1, γ0) by Eq. 3.4
6      if γ1 ≤ 0 then record calibration failure for fold f
7      refit (β0, β) on all of D_train with the selected λ (Eq. 3.2)
8      select θ(α_blk), θ(α_mod) by Eq. 3.14 on out-of-fold calibrated benign steps of D_train
9      apply Eqs. 3.1, 3.3 to D_test; store predictions for evaluation only
10 estimate r_mod(k) from enforcing-mode runs (Section 3.11.7)
11 check the loss structure for dominated verdicts (Section 3.7.5)
12 freeze parameters and record all versions
```

## 3.10 Algorithm 1: REM Runtime Evaluation and Mitigation

Algorithm 1 gives the per-step runtime procedure. Every operation is defined in Sections 3.4–3.8.

```
Algorithm 1. REM Runtime Evaluation and Mitigation

Frozen (offline, cross-cutting):  β0, β, γ1 (> 0), γ0, x̄, benign transition set,
                                   privilege map, instruction-pattern set, n_max,
                                   injection classifier (fixed)
Declared policy:                  κ, L (Table 3.13), Π, k_D2, required evidence per tier,
                                   𝒯_R, order Block ⪰ Escalate ⪰ Modify ⪰ Allow
Input at step t:                  objective g; new context segments with source channel;
                                   proposed action a_t; history H_t; episode restrictions S
Output:                           verdict v_t; mitigated outcome; audit record r_t

 1  // Layer 1: Input & Context (Section 3.4)
 2  remove invisible and formatting characters from new untrusted segments
 3  c_t   ← label segments trusted | semi-trusted | untrusted (least-trusted inheritance)
 4  Ent_t ← extract account identifiers, amounts, credentials, profile values, tool names,
            each with provenance, from c_t, g, and the arguments of a_t
 5  // Layer 2: Detection (Section 3.5, Table 3.8)
 6  x_ctx ← (x^ctx_1, x^ctx_2)
 7  // Layer 3: Behavioral Analysis (Section 3.6, Table 3.9)
 8  x_beh ← (x^beh_1, x^beh_2, x^beh_3, x^beh_4) from H_t, a_t, benign transitions, privilege map
 9  x_act ← (x^act_1, x^act_2, x^act_3) from a_t, Ent_t, g, H_t
10  // Layer 4: Decision Engine (Section 3.7)
11  x_t ← [x_ctx; x_beh; x_act];  avail ← features computable at step t
12  s_t ← β0 + βᵀx_t;  p̃_t ← σ(s_t)                                   // Eq. 3.1
13  p_t ← σ(γ1·s_t + γ0)                                              // Eq. 3.3
14  k_t ← κ(z_t), where z_t are the descriptors of a_t (Table 3.10)
15  if a_t ∈ Π then
16      v_t ← Block;  src ← "D1"
17  else if the evidence required at tier k_t ⊄ avail and k_t ≥ k_D2 then
18      v_t ← Escalate;  src ← "D2"
19  else
20      V_t ← {Allow, Escalate, Block} ∪ ({Modify} if tool(a_t) ∈ 𝒯_R)
21      for each v in V_t:  R[v] ← (1 − p_t)·L(v,0,k_t) + p_t·L(v,1,k_t)   // Eq. 3.6
22      v_t ← verdict in V_t with minimum R[v]; ties → more restrictive   // Eq. 3.7
23      src ← "expected loss"
24  φ0 ← β0 + βᵀx̄;  φ_t ← β ⊙ (x_t − x̄);  Φ ← group sums over I_ctx, I_beh, I_act  // Eqs. 3.11, 3.13
25  check |φ0 + Σ_i φ_t,i − s_t| < ε                                   // Eq. 3.12
26  r_t ← (t, x_t, s_t, p̃_t, p_t, k_t, R, v_t, src, φ0, φ_t, Φ, versions, timestamps)
27  append r_t to the audit log (append-only)
28  // Layer 5: Mitigation (Section 3.8, Table 3.14)
29  if tool(a_t) is restricted in S then refuse a_t and return a structured notice
30  else if v_t = Allow    then release a_t
31  else if v_t = Modify   then withhold a_t; add tool class of a_t to S; return structured notice
32  else if v_t = Escalate then withhold a_t; send r_t to reviewer; release a_t only on approval
33  else if v_t = Block    then do not execute a_t; add every tool in 𝒯_R to S (halt);
                              return structured refusal
34  update H_t with (a_t, v_t) and, if released, its tool result, which enters Layer 1
    as untrusted content at step t + 1
35  return v_t, outcome, r_t
```

Line 29 enforces restrictions imposed by earlier Modify or Block verdicts. After Block, every tool in 𝒯_{R} is restricted, so the episode refuses every further side-effecting action while read tools remain available. Lines 24–25 are audit operations and do not affect the verdict.

## 3.11 Experimental Methodology

### 3.11.1 Environment and instrumentation

REM is evaluated in the banking environment of AgentDojo (Debenedetti et al., 2024), an open-source framework that evaluates both the utility and the security of LLM agents. Security is determined by checks on the environment state before and after an episode, and utility by task-specific checks.

REM is placed at the tool-execution boundary of the agent loop, where it intercepts each proposed tool call before execution and each tool result on return. That this is achievable without modifying the agent's internals is assumption AS-1, to be demonstrated in Chapter 4.

REM runs in two modes:
- **Observe-only:** verdicts are computed and logged but not enforced. Fitting data are collected in this mode, because enforced verdicts would alter the trajectories from which REM is fitted.
- **Enforcing:** verdicts are executed by the Mitigation Layer.

For every run, the following are recorded:
- the AgentDojo release or commit identifier;
- the suite version;
- the attack template;
- the LLM backbone identifier and version, access date, and decoding parameters;
- REM's model, calibration, and policy versions.

The LLM backbone or backbones and the attack templates are pending supervisor approval.

### 3.11.2 Dataset

The banking suite definition inspected for this chapter (suite v1, AgentDojo repository main branch, accessed September 2026) contains:

- **16 user tasks.** Examples include paying a bill described in a file, refunding a friend, updating a recurring rent payment, and updating account details. Their reference solutions use between one and five tool calls.
- **9 injection tasks.** Eight direct money or a recurring payment toward one shared attacker account identifier. One changes the account password. The reference attacker actions consist of one call for seven tasks, two calls for one task (reading scheduled transactions, then sending money), and three calls for one task (a total amount split into smaller transfers).
- **11 tools:** get_iban, send_money, schedule_transaction, update_scheduled_transaction, get_balance, get_most_recent_transactions, get_scheduled_transactions, read_file, get_user_info, update_password, and update_user_info.

These counts must be re-confirmed against the benchmark version pinned for the experiments.

AgentDojo is an environment, not a fixed dataset of traces. Traces are generated by running an agent, so the number of traces depends on the number of backbones, attack templates, and repeated runs [DATA COUNT REQUIRES VERIFICATION]. The 144 combinations of user task and injection task are not 144 independent samples. They are built from 16 user-task templates and 9 injection-task templates, and every trace inherits the dependence of its templates.

### 3.11.3 Label construction

The label must represent the quantity the estimator is asked to predict, which is whether a proposed call serves the attacker's objective rather than the user's. Labels are therefore derived from the injection task's own reference solution, not from the presence of an injection in the episode, because an attacked episode also contains benign calls. The derivation is mechanical, so the rules below state exactly what is matched, where the rule is known to be uncertain, and how that uncertainty is measured.

- **Step labels.** In an attacked episode, a proposed tool call is labeled y_{t} = 1 if it matches a call in the injection task's reference solution on tool name and on the attacker-controlled key argument, such as the attacker account identifier or the attacker-specified password. All other proposed calls, including calls that continue the user's task in attacked episodes, are labeled y_{t} = 0, as are all calls in episodes without injection.
- **Induced read steps.** Some injection tasks include a read call in their reference solution. Whether such a read step is labeled y_{t} = 1 is pending supervisor decision, because it is induced but has no direct external effect.
- **Label audit.** Matching on arguments can mislabel steps, for example when an agent alters an amount. The derivation is therefore audited on a manually inspected sample of episodes, and the disagreement rate is reported.

### 3.11.4 Data limitations

The design must respect five limitations of the data:

1. **Positive-step scarcity.** A step is labeled y_{t} = 1 only if the agent actually proposes the attacker's call. The number of positive steps therefore depends on how often the chosen backbone follows injected instructions, and it may be small [DATA COUNT REQUIRES VERIFICATION]. Most steps are benign, so the classes are strongly imbalanced.
2. **Shared attacker account identifier.** Eight of the nine injection tasks use the same attacker account identifier. Any feature keyed on that value would leak the label across folds (Section 3.6.2).
3. **Repeated task templates.** The same user tasks appear with every injection task, so benign behavior learned in one fold recurs in others.
4. **Short trajectories.** Reference solutions contain one to five calls, and most attacker objectives require one call. Trajectory-level evidence therefore has limited opportunity to accumulate.
5. **Calibration data.** A calibration set separate from training, validation, and test data would contain very few positive steps.

As a result, four statistically independent partitions for training, calibration, validation, and testing cannot be supported, and the design uses grouped cross-fitting instead.

### 3.11.5 Grouping and cross-fitting

Estimation, calibration, and threshold selection use nested grouped cross-fitting. No step is ever scored by a model fitted on data from its own group.

1. **Outer folds.**
   - *Attacked episodes* are grouped by injection task, giving nine leave-one-injection-task-out folds. The held-out fold therefore contains an attacker objective not seen during fitting.
   - *Episodes without injection* are assigned to the outer folds by user task, so that no user task's benign-only episodes appear in both the fitting and held-out portions of a fold.
2. **Inner folds.** Within the fitting portion of each outer fold, grouped inner cross-validation selects λ by held-out log-loss and produces out-of-fold logits. These are used to fit the calibration parameters (Equation 3.4) and to select the baseline thresholds (Equation 3.14).
3. **Held-out scoring.** The outer held-out fold is scored by the model fitted on the rest. All reported metrics are computed from these held-out predictions.
4. **Deployment model.** A model fitted on all data is used only for runtime demonstrations and latency measurement, never for reported accuracy or calibration.

Grouping by injection task does not remove the dependence introduced by shared user-task templates in attacked episodes. As a sensitivity analysis pending supervisor approval, the fitting is repeated with folds grouped by user task, and differences between the two groupings are reported.

### 3.11.6 Leakage controls

Because the injection tasks in the banking suite share a small number of templates and a single attacker account, an estimator can reach a high score by memorizing the benchmark rather than by recognizing adversarial inducement. Arp et al. (2022) identify this family of errors as a recurring cause of overstated security-classification results. The following controls are therefore fixed before any held-out prediction is examined.

- No feature encodes a specific account identifier (Section 3.6.2).
- Benign reference quantities are estimated within each outer fold's fitting portion.
- The feature set, instruction-pattern set, privilege map, tier map, loss grid, false-positive targets, and pilot decision values are declared before held-out predictions are examined.
- Fitting data are collected in observe-only mode.
- Results are reported per benchmark and are not pooled across benchmarks.

### 3.11.7 Configurations, baselines, and ablations

**Configurations:**
- **B0, no defense.** Establishes attack success and utility without protection.
- **B1, consequence-independent baseline.** The same estimator and calibration with the threshold policy of Section 3.7.7. This is the primary comparator for RQ2.
- **REM.** The expected-loss verdict selection of Section 3.7.5.
- **B2, detection-only (pending supervisor approval).** The Detection Layer's classifier score applied to untrusted content with an operating-point threshold. It tests whether Layers 3 and 4 add value.
- **Distributed defenses (pending supervisor approval).** Any defenses distributed with the pinned benchmark version, to address O3.

**Ablations of REM** (each changes one element, all else fixed; the estimator is refitted when an evidence group is removed):

1. Context evidence removed.
2. Behavioral evidence removed.
3. Action evidence removed.
4. Calibration removed (p̃_{t} used in Equation 3.6).
5. Consequence tiers removed (one tier for all actions).
6. Predicates D1 and D2 disabled.
7. Observe-only (no mitigation).

**Mitigation-effectiveness runs.** Enforcing-mode runs in which Modify is applied to adversarial steps estimate r_{mod}(k) per tier and the utility impact of Modify on benign steps. These estimates feed Equation 3.5 and are fitted within the outer folds so that no held-out episode informs its own loss values.

**Escalation in experiments.** No human reviewer is available in the benchmark. Escalation is resolved in two ways:
- by an idealized reviewer who releases the action if y_{t} = 0 and prevents it if y_{t} = 1;
- by a no-reviewer bound in which every escalation is treated as Block.

Both are reported, so the dependence of any result on the reviewer assumption is visible.

### 3.11.8 Pilot E0

Before the feature set is frozen, a pilot run on the fitting portions of the outer folds checks feasibility:

- the number of positive steps per backbone and attack template;
- the ROC-AUC of each evidence group alone and combined.

The pilot's decision values are project decisions declared before the pilot, not literature-derived thresholds [pending supervisor approval]:
- the minimum number of positive steps needed to proceed;
- the minimum group ROC-AUC needed to retain an evidence group.

If the positive-step count is insufficient, additional attack templates or backbones are added before the main experiments. The pilot never uses held-out fold predictions.

### 3.11.9 Repeated runs and uncertainty

Each configuration is run at least three times with fixed decoding parameters to characterize LLM non-determinism [number of runs pending supervisor approval]. Repeated runs of the same template are not independent. Results are therefore aggregated per episode template before uncertainty is estimated.

Confidence intervals are obtained by bootstrap resampling (Efron, 1979) at the level of injection-task groups for attacked episodes and user-task groups for benign episodes. Resampling groups rather than steps is a design choice that respects the dependence described in Section 3.11.2.

With nine injection-task groups, intervals will be wide. No statistical power has been established, so differences are reported as measured differences with their intervals, and the word "significant" is not used unless a stated test supports it.

### 3.11.10 Optional observe-only sequential analysis

Sequential change detection is not part of REM's verdict path. If the supervisor approves it for the thesis narrative, it is performed **offline** on the per-step indicators logged by the Behavioral Analysis Layer. It never influences a verdict.

For each step, a binary deviation indicator e_{t} ∈ {0, 1} is defined as 1 if at least one of x^{beh}_{1}, x^{beh}_{3}, x^{beh}_{4}, or x^{act}_{1} equals 1, or if x^{beh}_{2} = 1; otherwise 0 [indicator set pending supervisor approval]. Let q_{0} and q_{1}, with 0 < q_{0} < q_{1} < 1, be the rates of e_{t} = 1 before and after an adversarial change.

The log-likelihood ratio of one observation, as defined by Basseville and Nikiforov (1993), specialized to Bernoulli observations, is:

$$ ℓ_{t} = e_{t} ln(q_{1} / q_{0}) + (1 − e_{t}) ln((1 − q_{1}) / (1 − q_{0})) $$ (3.15)

*Status:* derived by substituting the Bernoulli probability mass function into the log-likelihood ratio of Basseville and Nikiforov (1993). A cumulative sum chart for Bernoulli observations is treated by Reynolds and Stoumbos (1999).

The cumulative sum statistic and alarm time are (Basseville & Nikiforov, 1993; Page, 1954):

$$ G_{t} = max(0, G_{t−1} + ℓ_{t}),     G_{0} = 0 $$ (3.16)

$$ T_{A} = min { t : G_{t} ≥ h_{G} } $$ (3.17)

where h_{G} > 0 is the alarm threshold.

*Status:* established from source.

The per-episode false-alarm rate on benign episodes and the detection delay are defined as:

$$ FA_{ep}(h_{G}) = |{ j ∈ E_{ben} : max_{t} G^{(j)}_{t} ≥ h_{G} }| / |E_{ben}| $$ (3.18)

$$ τ_{d} = T_{A} − ν,     T_{A} ≥ ν $$ (3.19)

where E_{ben} is the set of benign episodes in the fitting portion of a fold, G^{(j)}_{t} is the statistic in benign episode j, τ_{d} is the detection delay, and ν is the first step at which injected content enters the context.

*Status:* design definitions.

The parameters are determined as follows:
- q_{0} is the empirical rate of e_{t} = 1 on benign fitting steps, floored at a declared minimum.
- q_{1} is declared and reported over a range, because the scarcity of multi-step attacks does not allow it to be estimated reliably.
- h_{G} is the smallest value for which Equation 3.18 does not exceed a declared target.

The procedure has known optimality properties in sequential change detection: Lorden (1971) proposed stopping rules that are asymptotically optimal in a defined sense, and Moustakides (1986) showed Page's stopping time to be optimal in a stronger sense. Both results are proved within a sequential-analysis model whose conditions could not be inspected during verification and are not claimed to hold for agent trajectories, where observations are neither independent nor drawn from known distributions. They therefore motivate the procedure and provide no guarantee in this setting. Given the short trajectories of Section 3.11.4, this analysis may have little to detect.

## 3.12 Evaluation Metrics

### 3.12.1 Primary metrics

Primary metrics do not depend on declared costs.

**Table 3.15. Primary metrics**

| Metric | Definition | Unit |
|---|---|---|
| Attack success rate (ASR) | Fraction of attacked episodes in which the benchmark's security check reports that the injection goal was achieved (enforcing mode) | Episode |
| Benign utility | Fraction of episodes without injection in which the benchmark's utility check passes | Episode |
| Utility under attack | Fraction of attacked episodes in which the utility check passes | Episode |
| Intervention rates | Fraction of steps receiving Modify, Escalate, or Block, reported per verdict and separately for y = 0 and y = 1 steps | Step |
| Step false-positive rate | Interventions on y = 0 steps divided by the number of y = 0 steps | Step |
| Residual ASR under Modify | ASR in episodes where Modify was applied to an adversarial step | Episode |
| Escalation rate | Fraction of steps receiving Escalate, with outcomes under the idealized reviewer and the no-reviewer bound | Step |
| Latency | Wall-clock time of REM's per-step processing, excluding LLM inference and tool execution; median and 95th percentile | Step |

ASR is never reported without benign utility and utility under attack. A low ASR can reflect an agent that fails to complete tasks rather than an effective defense (Y. Wang et al., 2026).

### 3.12.2 Secondary metrics

**Discrimination.** ROC-AUC (Fawcett, 2006) and PR-AUC (Davis & Goadrich, 2006) are computed on held-out probabilities. PR-AUC is emphasized because positive steps are rare. Within a fold, both are unchanged by calibration with γ_{1} > 0. Because each outer fold has its own calibration map, metrics are reported per fold as well as on the pooled held-out predictions.

**Calibration error.** For binary outcomes, calibration error is measured on the positive-class probability (Naeini et al., 2015) with M equal-width bins (Guo et al., 2017):

$$ ECE = Σ_{m=1}^{M} (|B_{m}| / N) · | ȳ(B_{m}) − p̄(B_{m}) |,     B_{m} = { i : (m − 1)/M < p_{i} ≤ m/M } $$ (3.20)

where N is the number of held-out steps, ȳ(B_{m}) is the fraction of positive steps in bin m, p̄(B_{m}) is the mean calibrated probability in bin m, and M is declared in advance (steps with p_{i} = 0 are assigned to the first bin).

*Status:* adapted from source. Naeini et al. (2015) supply the binary form; Guo et al. (2017) supply the equal-width binning.

Because a global ECE averages over all probabilities, reliability is also reported within declared windows around each tier's threshold p^{*}_{k}.

**Log-loss.** The mean negative log-likelihood of held-out steps is:

$$ LL = −(1/N) Σ_{i=1}^{N} [ y_{i} ln p_{i} + (1 − y_{i}) ln(1 − p_{i}) ] $$ (3.21)

*Status:* derived as the negated, averaged, unpenalized log-likelihood term of Equation 3.2 evaluated at the calibrated probabilities. Probabilities are bounded away from 0 and 1 by a declared small constant for numerical evaluation.

**Brier score.** The Brier score is not reported until the convention of its original source (Brier, 1950) has been confirmed; log-loss serves as the proper scoring measure in the meantime.

### 3.12.3 Realized loss across a declared grid

Realized loss is secondary because it depends on declared costs, and because a rule that minimizes expected loss under L is favored by construction when evaluated under the same L. For an evaluation loss structure L_{e}:

$$ L̄(L_{e}) = (1/N) Σ_{i=1}^{N} L_{e}(v_{i}, y_{i}, k_{i}) $$ (3.22)

where v_{i} is the verdict issued for held-out step i under the decision loss structure L_{d}, y_{i} is its label, and k_{i} is its tier.

*Status:* design definition.

The grid is declared before held-out predictions are examined and varies three things:
- the ratio C_{miss}(k)/C_{FA}(k) per tier;
- C_{esc};
- the amount limits of the tier map.

For each evaluation structure L_{e}, the grid reports:
- REM with L_{d} = L_{e} (matched);
- REM with L_{d} ≠ L_{e} (misspecified costs);
- the baseline B1, which does not use costs.

The conclusion takes the form "across this declared range of loss structures, outcomes vary as follows", not "under the chosen costs, outcomes are these".

## 3.13 Contribution and Novelty Boundaries

REM does not introduce a new learning algorithm or a new decision-theoretic method. Its constituent mechanisms are established and are attributed to their sources.

**Table 3.16. Mechanisms that are not claimed as novel**

| Mechanism | Prior work |
|---|---|
| Logistic regression | Cox (1958) |
| Ridge regularization of logistic regression | le Cessie and van Houwelingen (1992) |
| Platt (logistic) calibration | Platt (1999); Guo et al. (2017); Kull et al. (2017) |
| Linear Shapley attribution | Lundberg and Lee (2017) |
| Cumulative sum change detection | Page (1954); Basseville and Nikiforov (1993) |
| Expected-cost decisions; reject option | Elkan (2001); Chow (1970) |
| Calibrated logistic risk scores for agent safety; four-way intervention | Hossain et al. (2026) |
| Distinction between calibration and control | C. Zhang et al. (2026) |
| Runtime interception; human review; graduated response | H. Liu et al. (2026); C. Yang (2026); C. L. Wang et al. (2025) |
| Provenance analysis of tool calls | She et al. (2026); Debenedetti et al. (2025) |
| Consequence-aware and consequence-priced control | H.-H. Chen (2026); Hossain et al. (2026); C. Yang (2026) |
| Component ablation with latency | C. Yang (2026) |
| Runtime protection of financial agents | Jia et al. (2026) |

**Investigated contribution.** The contribution of this thesis is empirical and integrative. It is the design and evaluation, on the AgentDojo banking environment under indirect prompt injection, of a non-invasive five-layer runtime layer that combines:

- provenance-based evidence about proposed financial actions;
- a calibrated per-step probability of adversarial induction;
- verdict selection over Allow, Modify, Escalate, and Block by minimizing conditional risk with losses declared per consequence tier;
- deterministic mitigation whose effectiveness is measured and used in the loss structure.

It is evaluated against a consequence-independent baseline that uses the same estimator, with attack success, benign utility, utility under attack, intervention behavior, and latency measured separately and cost-dependent outcomes reported across a declared loss grid.

**Explicitly not claimed:**
- a new algorithm;
- the first runtime guardrail, the first calibrated agent risk score, or the first consequence-aware controller;
- that calibration improves control;
- robustness against adaptive adversaries;
- any prevention guarantee;
- validity in production financial deployment.

The contribution holds only to the extent that the experiments specified in this chapter support it.

## 3.14 Threats to Validity

**Construct validity.**
- Step labels are derived and can be wrong; the derivation is audited on a sample (Section 3.11.3).
- The idealized reviewer overstates the protective value of Escalate; the no-reviewer bound is reported alongside it.
- Declared costs cannot be validated empirically; their influence is reported across the grid.
- A low ASR can reflect task failure rather than protection, so utility metrics accompany every security metric (Y. Wang et al., 2026).

**Internal validity.**
- Leakage through shared templates and the shared attacker account identifier is controlled by grouping and by excluding identity-based features, but template dependence remains.
- Features designed with knowledge of the benchmark may fit its style; the feature set is frozen after the pilot and before held-out predictions are examined.
- LLM non-determinism is characterized by repeated runs.

**External validity.**
- The evaluation uses one simulated banking environment with benchmark-authored attacks.
- Results may not transfer to other benchmarks, whose definitions and conclusions can disagree (M. Q. Li et al., 2026), or to production systems.
- Results may depend on the LLM backbone.
- FinVault is not used because its preprint was withdrawn.

**Statistical conclusion validity.**
- The number of independent task templates is small.
- Intervals are wide and no power analysis is available, so conclusions are limited to differences supported by their intervals.

**Security-specific threats.**
- Every evidence feature can be evaded individually, and adversaries are assumed non-adaptive (AS-6).
- REM's own configuration and logs are assumed protected (AS-3).
- A scalar probability cannot represent whether an adversarial trajectory remains recoverable, so REM inherits the limitation identified by C. Zhang et al. (2026); estimating intervention value by counterfactual replay is outside the scope of this thesis.

## 3.15 Equation Provenance Summary

**Table 3.17. Provenance of the equations in this chapter**

| Eq. | Content | Status | Source | Verification |
|---|---|---|---|---|
| 3.1 | Logistic model | Established | Cox (1958) | IV |
| 3.2 | Ridge-penalized log-likelihood | Established | le Cessie & van Houwelingen (1992) | IV (penalty constant pending) |
| 3.3 | Logistic calibration on the logit, γ_{1} > 0 | Adapted | Platt (1999); Guo et al. (2017); Kull et al. (2017) | Platt NC; Guo FV; Kull FV |
| 3.4 | Calibration fit by negative log-likelihood | Established | Guo et al. (2017) | FV |
| 3.5 | Adversarial loss of Modify | Derived (assumption A-Mod) | Law of total expectation | DER |
| 3.6 | Conditional risk | Adapted | Elkan (2001) | FV (Eq. 1 form) |
| 3.7 | Bayes verdict with tie-breaking | Adapted | Elkan (2001) | FV; tie order DEF |
| 3.8 | Pairwise indifference threshold | Derived | From Eq. 3.6 | DER |
| 3.9 | Allow–Block threshold | Derived | From Eq. 3.8; consistent with Elkan (2001) | DER |
| 3.10 | Escalation feasibility condition | Derived | From Eqs. 3.6, 3.7, 3.9; Chow (1970) conceptual basis | DER; Chow IV |
| 3.11 | Linear attribution | Adapted | Lundberg & Lee (2017) | FV |
| 3.12 | Completeness identity | Derived | Lundberg & Lee (2017) local accuracy | FV + DER |
| 3.13 | Group attribution | Definition | — | DEF |
| 3.14 | Baseline operating-point threshold | Definition | — | DEF |
| 3.15 | Bernoulli log-likelihood ratio (optional) | Derived | Basseville & Nikiforov (1993); Reynolds & Stoumbos (1999) | FV; R&S IV |
| 3.16 | CUSUM recursion (optional) | Established | Basseville & Nikiforov (1993); Page (1954) | FV; Page IV |
| 3.17 | Alarm time (optional) | Established | Basseville & Nikiforov (1993) | FV |
| 3.18 | Per-episode false-alarm rate (optional) | Definition | — | DEF |
| 3.19 | Detection delay (optional) | Definition | — | DEF |
| 3.20 | Expected calibration error | Adapted | Naeini et al. (2015); Guo et al. (2017) | FV |
| 3.21 | Log-loss | Derived | From Eq. 3.2 | DER |
| 3.22 | Realized loss | Definition | — | DEF |

*Verification codes:* FV — formulation checked against the source; IV — source identity confirmed, formulation to be checked against the full text; NC — source not accessible during this revision; DER — derived in this chapter; DEF — design definition. The codes are retained until final reference verification is complete.

## 3.16 Chapter Summary

This chapter specified the REM methodology as one runtime pipeline in five layers:
- **Input & Context:** captures the proposed action and labels context by provenance.
- **Detection:** computes context evidence.
- **Behavioral Analysis:** computes history and action-provenance evidence.
- **Decision Engine:** estimates a calibrated probability of adversarial induction with ridge logistic regression and Platt calibration on the logit, assigns a declared consequence tier, applies policy predicates, selects a verdict by minimizing conditional risk under tier-indexed losses, and writes an audit record whose linear attribution never influences the verdict.
- **Mitigation:** executes Allow, tool restriction, escalation, or Block.

Offline fitting and recalibration are cross-cutting activities, not a layer.

The evaluation uses the AgentDojo banking environment with nested grouped cross-fitting instead of independent partitions. It explicitly accounts for positive-step scarcity, the shared attacker account identifier, repeated task templates, and short trajectories. It compares REM with a consequence-independent baseline on the same estimator, reports cost-free primary metrics, and reports realized loss only across a declared grid that includes misspecified costs. The contribution is bounded as an empirical and integrative one. Chapter 4 describes the implementation.

## References

Arp, D., Quiring, E., Pendlebury, F., Warnecke, A., Pierazzi, F., Wressnegger, C., Cavallaro, L., & Rieck, K. (2022). Dos and don'ts of machine learning in computer security. In *31st USENIX Security Symposium*. USENIX Association. https://arxiv.org/abs/2010.09470

Basseville, M., & Nikiforov, I. V. (1993). *Detection of abrupt changes: Theory and application*. Prentice Hall. https://people.irisa.fr/Michele.Basseville/kniga/

Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review, 78*(1), 1–3. https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2

Chen, H.-H. (2026). *Insuring every action: An authority frontier framework for runtime actuarial control of autonomous AI agents* (arXiv:2605.25632) [Preprint]. arXiv. https://arxiv.org/abs/2605.25632

Chennabasappa, S., Nikolaidis, C., Song, D., Molnar, D., Ding, S., Wan, S., Whitman, S., Deason, L., Doucette, N., Montilla, A., Gampa, A., de Paola, B., Gabi, D., Crnkovich, J., Testud, J.-C., He, K., Chaturvedi, R., Zhou, W., & Saxe, J. (2025). *LlamaFirewall: An open source guardrail system for building secure AI agents* (arXiv:2505.03574) [Preprint]. arXiv. https://arxiv.org/abs/2505.03574

Chow, C. K. (1970). On optimum recognition error and reject tradeoff. *IEEE Transactions on Information Theory, 16*(1), 41–46. https://doi.org/10.1109/TIT.1970.1054406

Cox, D. R. (1958). The regression analysis of binary sequences. *Journal of the Royal Statistical Society: Series B (Methodological), 20*(2), 215–232. https://doi.org/10.1111/j.2517-6161.1958.tb00292.x

Davis, J., & Goadrich, M. (2006). The relationship between precision-recall and ROC curves. In *Proceedings of the 23rd International Conference on Machine Learning* (pp. 233–240). ACM. https://doi.org/10.1145/1143844.1143874

Debenedetti, E., Shumailov, I., Fan, T., Hayes, J., Carlini, N., Fabian, D., Kern, C., Shi, C., Terzis, A., & Tramèr, F. (2025). *Defeating prompt injections by design* (arXiv:2503.18813) [Preprint]. arXiv. https://arxiv.org/abs/2503.18813

Debenedetti, E., Zhang, J., Balunović, M., Beurer-Kellner, L., Fischer, M., & Tramèr, F. (2024). *AgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents* (arXiv:2406.13352). arXiv. https://arxiv.org/abs/2406.13352

Efron, B. (1979). Bootstrap methods: Another look at the jackknife. *The Annals of Statistics, 7*(1). https://doi.org/10.1214/aos/1176344552

Elkan, C. (2001). The foundations of cost-sensitive learning. In *Proceedings of the Seventeenth International Joint Conference on Artificial Intelligence (IJCAI-01)*. https://cseweb.ucsd.edu/~elkan/rescale.pdf

Fawcett, T. (2006). An introduction to ROC analysis. *Pattern Recognition Letters, 27*(8), 861–874. https://doi.org/10.1016/j.patrec.2005.10.010

Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., & Fritz, M. (2023). Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection. In *Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security* (pp. 79–90). ACM. https://doi.org/10.1145/3605764.3623985

Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. In *Proceedings of the 34th International Conference on Machine Learning* (Vol. 70, pp. 1321–1330). PMLR. https://proceedings.mlr.press/v70/guo17a.html

Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly, 28*(1), 75–106. https://doi.org/10.2307/25148625

Hines, K., Lopez, G., Hall, M., Zarfati, F., Zunger, Y., & Kiciman, E. (2024). *Defending against indirect prompt injection attacks with spotlighting* (arXiv:2403.14720) [Preprint]. arXiv. https://arxiv.org/abs/2403.14720

Hossain, E., Nipu, M. M. H., Ornee, T. N., Rana, R., & Yousefi, N. (2026). *NEXUS: Structured runtime safety for tool-using LLM agents* (arXiv:2607.19356) [Preprint]. arXiv. https://arxiv.org/abs/2607.19356

Jia, H., Liu, Y., Chong, B., Yang, Y., Chen, Y., Liang, J., Li, Q., Lu, H., Xu, K., Zheng, H., Zhang, C., Peng, H., & Yu, P. S. (2026). *FinHarness: An inline lifecycle safety harness for finance LLM agents* (arXiv:2605.27333) [Preprint]. arXiv. https://arxiv.org/abs/2605.27333

Kull, M., Silva Filho, T., & Flach, P. (2017). Beta calibration: A well-founded and easily implemented improvement on logistic calibration for binary classifiers. In *Proceedings of the 20th International Conference on Artificial Intelligence and Statistics* (Vol. 54, pp. 623–631). PMLR. https://proceedings.mlr.press/v54/kull17a.html

le Cessie, S., & van Houwelingen, J. C. (1992). Ridge estimators in logistic regression. *Applied Statistics, 41*(1), 191–201. https://doi.org/10.2307/2347628

Li, M. Q., Fung, B. C. M., Li, B., Ismail, H., & Iqbal, F. (2026). *Taxonomy and consistency analysis of safety benchmarks for AI agents* (arXiv:2605.16282) [Preprint]. arXiv. https://arxiv.org/abs/2605.16282

Liu, H., Ilyushin, E., Ni, J., & Zhu, M. (2026). *SafeAgent: A runtime protection architecture for agentic systems* (arXiv:2604.17562) [Preprint]. arXiv. https://arxiv.org/abs/2604.17562

Lorden, G. (1971). Procedures for reacting to a change in distribution. *The Annals of Mathematical Statistics, 42*(6), 1897–1908. https://doi.org/10.1214/aoms/1177693055

Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. In *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1705.07874

Moustakides, G. V. (1986). Optimal stopping times for detecting changes in distributions. *The Annals of Statistics, 14*(4). https://doi.org/10.1214/aos/1176350164

Naeini, M. P., Cooper, G., & Hauskrecht, M. (2015). Obtaining well calibrated probabilities using Bayesian binning. *Proceedings of the AAAI Conference on Artificial Intelligence, 29*(1). https://doi.org/10.1609/aaai.v29i1.9602

OWASP Gen AI Security Project. (2025). *LLM01:2025 Prompt injection*. OWASP Foundation. https://genai.owasp.org/llmrisk/llm01-prompt-injection/

Page, E. S. (1954). Continuous inspection schemes. *Biometrika, 41*(1–2), 100–115. https://doi.org/10.1093/biomet/41.1-2.100

Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems, 24*(3), 45–77. https://doi.org/10.2753/MIS0742-1222240302

Platt, J. C. (1999). Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. In A. J. Smola, P. Bartlett, B. Schölkopf, & D. Schuurmans (Eds.), *Advances in large margin classifiers* (pp. 61–74). MIT Press.

Reynolds, M. R., Jr., & Stoumbos, Z. G. (1999). A CUSUM chart for monitoring a proportion when inspecting continuously. *Journal of Quality Technology, 31*(1), 87–108. https://doi.org/10.1080/00224065.1999.11979900

She, Y., Liang, Y., & Kang, E. (2026). *Safeguarding LLM agents from misalignment through provenance analysis* (arXiv:2607.01236) [Preprint]. arXiv. https://arxiv.org/abs/2607.01236

Wang, C. L., Singhal, T., Kelkar, A., & Tuo, J. (2025). *MI9: An integrated runtime governance framework for agentic AI* (arXiv:2508.03858) [Preprint]. arXiv. https://arxiv.org/abs/2508.03858

Wang, Y., Han, X., Shang, D., Tang, Y., & Liu, B. (2026). *Safety, or just capability? A validity audit of agent-safety benchmarks* (arXiv:2607.28685) [Preprint]. arXiv. https://arxiv.org/abs/2607.28685

Yang, C. (2026). *AgentTrust: Runtime safety evaluation and interception for AI agent tool use* (arXiv:2605.04785) [Preprint]. arXiv. https://arxiv.org/abs/2605.04785

Zhang, C., Wan, Z., Yu, X., Wu, J., Wen, Q., Zhou, P., Zhao, W., & Tsang, I. (2026). *Calibration is not control: Why LLM-agent oversight needs intervention* (arXiv:2606.21399) [Preprint]. arXiv. https://arxiv.org/abs/2606.21399
