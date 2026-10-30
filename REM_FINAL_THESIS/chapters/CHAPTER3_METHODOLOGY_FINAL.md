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
- *[Proposed scope amendment, pending supervisor approval]* A recorded-trace replay sensitivity analysis under a stated no-adaptation assumption (Section 3.11.11). It is reported as exploratory evidence about fixed recorded trajectories, not as an estimate of enforcement against live or adaptive agents.

**Out of scope:**
- Training-time defenses and modification of the agent's model or prompts.
- Multi-agent systems.
- Evaluation against adaptive adversaries who tune attacks to REM.
- Production deployment in a financial institution.
- Counterfactual estimation of intervention value for adaptive agents, for example by replaying agent prefixes and executing alternative actions from the same state (C. Zhang et al., 2026).

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
| c~t~ | Context at step t, as segments with provenance labels |
| a~t~ | Proposed action (tool name and arguments) at step t |
| H~t~ | Episode history up to step t |
| y~t~ ∈ {0, 1} | Latent label: 1 if a~t~ is adversarially induced |
| x~t~ ∈ [0, 1]^d^ | Evidence vector; groups x^ctx^, x^beh^, x^act^ with index sets I~ctx~, I~beh~, I~act~ |
| β~0~, β, λ | Logistic intercept, coefficient vector, ridge strength |
| s~t~ | Logit (linear predictor) |
| p̃~t~, p~t~ | Uncalibrated probability; calibrated probability |
| γ~1~, γ~0~ | Calibration slope and intercept |
| z~t~, k~t~, κ | Consequence descriptors; consequence tier; tier map |
| 𝒱 | Verdict set {Allow, Modify, Escalate, Block} |
| 𝒱(a~t~) | Verdicts feasible for a~t~ |
| v~t~ | Verdict issued at step t |
| L(v, y, k) | Loss of verdict v when the label is y and the tier is k |
| C~miss~(k), C~FA~(k), C~mod~(k), C~esc~ | Declared costs of a missed attack, a false intervention by Block, Modify on a legitimate action, and escalation |
| r~mod~(k) | Residual attack-success rate after Modify at tier k (measured) |
| R~t~(v) | Conditional risk of verdict v at step t |
| π~v,v′~(k), p^\*^~k~ | Indifference threshold between verdicts v and v′; Allow–Block threshold |
| σ(·) | Logistic function, σ(u) = 1 / (1 + exp(−u)) |
| Π, k~D2~ | Set of prohibited actions; minimum tier for predicate D2 |
| θ(α), α~blk~, α~mod~ | Baseline threshold for false-positive target α; targets for Block and Modify |
| 𝒯~R~ | Set of tools to which the Modify mechanism applies |

Symbols used only in the optional sequential analysis are defined in Section 3.11.10. Symbols that appear in a single equation, such as Δ~0~, Δ~1~, B~m~, and the step sets D~fit~, D~cal~, and D~val~^benign^, are defined where they are used. Each symbol has one meaning throughout the chapter.

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

![Figure 3.1. REM architecture as implemented. Five layers at the tool-execution boundary; offline fitting and recalibration are cross-cutting and never run within an episode; the audit record is written for every step and its attribution cannot reach the verdict.](results/pilot_R2/figures/fig_architecture.png){width=100%}

Figure 3.1 shows the runtime path from the proposed tool call through Layers 1–5 to the environment, the return of tool results as untrusted context, the append-only audit record, and the cross-cutting offline fitting. The human reviewer to whom Escalate refers is outside REM. In this thesis no reviewer is present, and escalations are resolved by the two bounds of Section 3.11.7.

### 3.2.3 Layer interfaces

**Table 3.5. Layer interfaces**

| Layer | Consumes | Produces |
|---|---|---|
| L1 Input & Context | Objective, system prompt, user messages, tool results, proposed action | Labeled context c~t~; entities with provenance; held action a~t~ |
| L2 Detection | Untrusted segments of c~t~ | Context evidence x^ctx^ |
| L3 Behavioral Analysis | H~t~, a~t~, entities, benign reference transitions, privilege map | Behavioral evidence x^beh^; action evidence x^act^ |
| L4 Decision Engine | x~t~, consequence descriptors z~t~, frozen parameters, declared policy | p~t~, k~t~, R~t~(·), verdict v~t~, audit record |
| L5 Mitigation | v~t~, a~t~, episode restrictions | Released, restricted, withheld, or refused action |

The four functions are separated architecturally. Layers 2 and 3 produce evidence and issue no verdicts. Layer 4 performs probability estimation and decision. Layer 5 performs mitigation.

## 3.3 Threat Model and Financial Action Boundary

### 3.3.1 Protected system

The protected system is a single LLM-based agent that pursues a user objective by proposing tool calls. REM treats the agent as opaque: it observes inputs, context, proposed actions, and tool results, but not model parameters or internal reasoning (AS-10). The evaluation instance is an agent operating the AgentDojo banking environment (Debenedetti et al., 2024), described in Section 3.11.2.

### 3.3.2 Episodes and steps

An episode is one execution of the agent on one user objective g. It is a finite sequence of steps t = 1, …, T, where step t is the interval in which the agent proposes action a~t~. At step t, REM observes g, the labeled context c~t~, the proposed action a~t~, and the history H~t~ of prior contexts, actions, verdicts, and tool results.

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

A proposed action a~t~ is **adversarially induced** (y~t~ = 1) if executing it would advance an objective introduced by the adversary rather than the user objective g. The label is not observable at runtime. Actions that are unsafe because of the agent's own error without adversarial involvement are outside this definition. The operational derivation of y~t~ for evaluation data is given in Section 3.11.3.

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
- the proposed action a~t~, captured at TB-3 and held until Layer 5 acts.

Invisible and formatting characters, such as zero-width characters, are removed from untrusted text before further processing. This is a deterministic hygiene step applied to **REM's analysis copy** of the text. The content delivered to the agent is not altered, because REM is non-invasive (AS-1); hygiene therefore protects REM's feature computation, not the agent. It reduces some encoding-based concealment but does not prevent paraphrase-based evasion.

### 3.4.2 Provenance labeling

Each context segment receives one label from the ordered set trusted (system prompt) ≻ semi-trusted (user input) ≻ untrusted (tool output, retrieved content, memory). Content derived from several segments inherits the least-trusted label among them, and processing never promotes content to a more trusted label. This rule is a design definition that preserves the distinction between data and instruction exploited by indirect injection. It asserts no empirical claim.

### 3.4.3 Entity extraction

The layer extracts security-relevant entities from each segment and from the arguments of a~t~, and records the provenance of each occurrence:
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
| x^ctx^~1~ | Maximum score of a fixed, pre-trained prompt-injection classifier over untrusted segments added since the previous step | [0, 1] | Derived (classifier choice pending supervisor approval) |
| x^ctx^~2~ | 1 if an untrusted segment added since the previous step matches the declared instruction-pattern set; otherwise 0 | Binary | Derived (pattern set declared before evaluation) |

The classifier is used with fixed inference and is not retrained. A classifier distributed with an existing guardrail system, such as PromptGuard 2 in LlamaFirewall (Chennabasappa et al., 2025), is a candidate. The instruction-pattern set contains declared indicators such as imperative instructions addressed to an assistant, references to tool names, and role or delimiter markers.

Both features are individually evadable, and benchmark-based scores of detectors are fragile (Arp et al., 2022; M. Q. Li et al., 2026). The Detection Layer is therefore not relied upon to be decisive. Its evidence is combined with behavioral and action evidence in the Decision Engine, and its contribution is measured by ablation (Section 3.11.7).

## 3.6 Behavioral Analysis Layer

The Behavioral Analysis Layer maintains the episode history and computes evidence about the trajectory and the proposed action. All reference quantities it uses are estimated offline from benign data and are frozen at runtime.

### 3.6.1 Step tracking

The layer maintains H~t~: the sequence of proposed actions, their arguments with provenance, the verdicts issued, and the tool results returned. H~t~ is reset at the start of each episode.

### 3.6.2 Behavioral and action evidence

**Table 3.9. Behavioral and action evidence**

| Feature | Definition | Type | Availability |
|---|---|---|---|
| x^beh^~1~ | Post-observation shift: 1 if the most recent tool result was untrusted and had x^ctx^~2~ = 1; otherwise 0 | Binary | Derived from H~t~ |
| x^beh^~2~ | Repeated calls: min(n~rep~, n~max~) / n~max~, where n~rep~ is the number of consecutive calls with the same tool and key arguments and n~max~ is declared | [0, 1] | Derived from H~t~ |
| x^beh^~3~ | Privilege escalation: 1 if the privilege level of a~t~'s tool exceeds the highest level used so far in the episode; otherwise 0 | Binary | Derived; privilege map declared |
| x^beh^~4~ | Transition deviation: 1 if the pair (previous tool, current tool) does not occur in the benign reference transition set; otherwise 0 | Binary | Derived; reference set estimated on benign fitting data |
| x^act^~1~ | Argument provenance: 1 if a key argument of a~t~ (recipient account identifier, amount, password, or profile value) occurs in untrusted content but not in g or trusted content; otherwise 0 | Binary | Derived from L1 entities |
| x^act^~2~ | Destination novelty: 1 if the recipient of a~t~ appears neither in g nor among the transactions observed before the episode's first untrusted ingestion; otherwise 0 | Binary | Derived; applicable to value-transfer and payment-modification tools |
| x^act^~3~ | Sensitive egress: 1 if a~t~ sends to an external recipient a value obtained from a sensitive read (account identifier, profile value, or credential); otherwise 0 | Binary | Derived from L1 entities and H~t~ |

All features are bounded in [0, 1] by definition, so no further rescaling is applied. Three design rules govern them:

1. **No identity-based features.** No feature may encode a specific account identifier. In the evaluated benchmark, one attacker account identifier is shared by most injection tasks (Section 3.11.2), and a feature keyed on that value would leak the label.
2. **Evidence is kept separate from consequence.** Whether a payee appears only in untrusted content is evidence about *whether* an action is adversarially induced; it belongs in x~t~. Whether the action transfers a large amount irreversibly describes *what would happen*; it belongs in the consequence descriptors z~t~ (Section 3.7.3) and enters the decision only through the loss.
3. **The feature set is frozen after pilot E0** (Section 3.11.8), before any held-out predictions are examined.

## 3.7 Decision Engine Layer

The Decision Engine turns evidence into a verdict in five stages: probability estimation, calibration, consequence assessment, policy predicates, and expected-loss verdict selection. It also writes the audit record. Each equation below states its source and whether it is established from the source, adapted from it, or derived here.

### 3.7.1 Ridge logistic estimation

The probability that the proposed action is adversarially induced is modeled by logistic regression (Cox, 1958):

$$ s_t = \beta_0 + \beta^{\top} x_t, \qquad \tilde{p}_t = \sigma(s_t) = \frac{1}{1+\exp(-s_t)} \qquad (3.1) $$

where x~t~ ∈ [0, 1]^d^ is the evidence vector [x^ctx^; x^beh^; x^act^], β~0~ ∈ ℝ is the intercept, β ∈ ℝ^d^ is the coefficient vector, s~t~ is the logit, and p̃~t~ is the uncalibrated estimate of P(y~t~ = 1 | x~t~).

*Role in REM:* maps the evidence of Layers 2 and 3 to a score and an uncalibrated probability.
*Status:* established from source (Cox, 1958).

The parameters are estimated offline by maximizing a ridge-penalized log-likelihood (le Cessie & van Houwelingen, 1992):

$$ (\hat{\beta}_0, \hat{\beta}) = \arg\max_{\beta_0,\beta} \sum_{i \in D_{\mathrm{fit}}} \left[ y_i \ln \tilde{p}_i + (1-y_i)\ln(1-\tilde{p}_i) \right] - \lambda \lVert \beta \rVert_2^2 \qquad (3.2) $$

where D~fit~ is the set of labeled fitting steps, y~i~ ∈ {0, 1} are their labels, p̃~i~ is given by Equation 3.1, and λ ≥ 0 controls the strength of the quadratic penalty. The intercept is not penalized.

*Role in REM:* produces finite and stable coefficients from small, imbalanced data with binary features.
*Status:* established from source.

The quadratic penalty is needed for a specific reason. The evidence features are mostly binary, and adversarial steps are scarce (Section 3.11.4). If a single indicator appears only in adversarial fitting steps, the unpenalized maximum-likelihood estimate does not exist as a finite value. The penalty keeps the estimates finite.

**Reference parameterization of λ.** This thesis fixes the penalty as written in Equation 3.2, λ‖β‖². The implementation (Chapter 4) minimizes the negative log-likelihood plus (λ~impl~/2)‖β‖², so the two parameterizations correspond exactly when λ = λ~impl~/2. Because λ is selected from a *finite* grid, the two scales are equivalent only under this conversion: the declared grid λ~impl~ ∈ {0.01, 0.1, 1, 10, 100} is the grid λ ∈ {0.005, 0.05, 0.5, 5, 50} on the scale of Equation 3.2. Every selected value is reported on both scales. The scaling constant in le Cessie and van Houwelingen (1992) has not been checked against the full text; it does not affect the method, which depends only on the stated objective and the declared grid.

No interaction terms are included by default. Equation 3.1 assumes that the log-odds of adversarial induction are approximately linear in the evidence.

### 3.7.2 Calibration on the logit

The uncalibrated probability p̃~t~ need not agree with observed frequencies. Ridge shrinkage and class imbalance can both distort it. Because the decision rule in Section 3.7.5 treats the probability as a probability, REM recalibrates it with a two-parameter logistic map applied to the logit:

$$ p_t = \sigma(\gamma_1 s_t + \gamma_0), \qquad \gamma_1 > 0 \qquad (3.3) $$

where γ~1~ is the calibration slope and γ~0~ is the calibration intercept.

*Role in REM:* produces the calibrated probability used by the decision rule.
*Status:* adapted from source. The method is Platt scaling (Platt, 1999). The two-parameter logistic form with parameters fitted by negative log-likelihood on held-out data follows Guo et al. (2017). The map is applied here to the logit of a logistic regression model. The monotonicity condition follows Kull et al. (2017), who require a non-negative slope for a non-decreasing map; REM requires a strictly positive slope so that the ranking of steps is preserved.

The calibration parameters are fitted by minimizing the negative log-likelihood on held-out logits (Guo et al., 2017):

$$ (\hat{\gamma}_1, \hat{\gamma}_0) = \arg\min_{\gamma_1,\gamma_0} \; -\sum_{i \in D_{\mathrm{cal}}} \left[ y_i \ln p_i + (1-y_i)\ln(1-p_i) \right] \qquad (3.4) $$

where D~cal~ is a set of steps whose logits s~i~ were produced by a model that was not fitted on those steps. Fitting Equation 3.4 on the model's own training logits would be close to degenerate, so REM uses out-of-fold logits from grouped cross-fitting (Section 3.9).

*Status:* established from source (Guo et al., 2017).

**Fitting target.** Equation 3.4 fits the calibration map to the observed labels y~i~. Platt's original procedure instead fits against smoothed targets, t₊ = (N₊ + 1)/(N₊ + 2) and t₋ = 1/(N₋ + 2), to reduce overfitting on small calibration sets. This thesis takes Equation 3.4 as the reference definition and evaluates Platt's smoothed targets as a sensitivity analysis.

Four properties of this choice are stated.

1. **It changes probabilities, not rankings.** With γ~1~ > 0, Equation 3.3 is strictly increasing in s~t~. Calibration therefore leaves ROC-AUC, PR-AUC, and any decision based only on the ordering of steps unchanged. If the fitted slope is not positive, calibration is rejected for that fit and the event is reported.
2. **It is the minimal adequate family.** Kull et al. (2017) prove that beta calibration with equal shape parameters equals logistic calibration applied to the log-odds of a score. Since p̃~t~ = σ(s~t~), the log-odds of p̃~t~ is s~t~, so Equation 3.3 is exactly beta calibration with equal shape parameters applied to p̃~t~. The identity map is included (γ~1~ = 1, γ~0~ = 0). Full beta calibration adds a third parameter, and isotonic regression is nonparametric; neither is adopted, given the limited calibration data.
3. **It is not a contribution.** Calibrated logistic risk scores are already used in agent safety (Hossain et al., 2026).
4. **It does not guarantee good control.** C. Zhang et al. (2026) show that recalibrating a scalar risk score can improve calibration error while leaving control regret under threshold routing unchanged, because a scalar probability does not represent whether an intervention would improve the outcome. REM therefore reports calibration quality and control outcomes separately (Section 3.12) and does not claim that calibration improves control.

### 3.7.3 Consequence tiers

The consequence of a proposed action is described by descriptors z~t~ obtained from the action itself (Table 3.10). They are mapped to a consequence tier k~t~ = κ(z~t~) ∈ {1, …, K} by a declared policy function κ. Consequence descriptors do not enter Equation 3.1; they affect the verdict only through the loss.

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
| Learned | β~0~, β, γ~1~, γ~0~ | Fitted on labeled data by Equations 3.2 and 3.4 |
| Measured | r~mod~(k); benign reference mean x̄; benign transition set; utility impact of Modify | Estimated from observe-only and enforcing-mode runs |
| Policy | κ, amount limits, C~miss~(k), C~FA~(k), C~mod~(k), C~esc~, Π, k~D2~, privilege map, tie-breaking order | Declared before evaluation; varied over a declared grid where they affect outcomes |

Policy quantities encode institutional judgment. They are not presented as empirical findings, and their influence is reported through the loss grid of Section 3.12.3.

### 3.7.4 Policy predicates

Two deterministic predicates are evaluated before verdict selection.

- **D1, prohibited action.** If a~t~ ∈ Π, the verdict is Block irrespective of p~t~. A prohibition that a sufficiently low probability could override would not be a prohibition.
- **D2, missing required evidence.** If the evidence required for tier k~t~ cannot be computed (for example, argument provenance is unavailable) and k~t~ ≥ k~D2~, the verdict is Escalate. Absent evidence is not treated as evidence of safety.

Π, k~D2~, and the evidence required at each tier are declared policy. When a predicate applies, it determines the verdict, the expected-loss rule is not consulted, and the audit record names the predicate as the source of the verdict. Both predicates are disabled in one ablation (Section 3.11.7).

**Order of evaluation and unavailable evidence.** Availability of each feature is determined first, from the proposed action alone. D1 and then D2 are applied *before* any probability enters the decision, so no verdict that a predicate fixes depends on a value computed from unavailable evidence. Two cases follow:

- **A predicate fixes the verdict.** s~t~ and p~t~ may still be computed and stored for audit, but they are marked as not used, and the audit record contains no risk table: the field is recorded as *not applicable* (Section 3.7.6).
- **No predicate applies, but a feature is unavailable** (possible only below k~D2~). The feature takes its "not observed" value 0, and the audit record flags the imputation. This is a design definition: an unavailable indicator is treated as not fired, which can only lower the estimated probability. It is therefore used only below the tier at which missing evidence forces escalation.

### 3.7.5 Expected-loss verdict selection

**Loss structure.** For each tier k, the loss of issuing verdict v when the label is y is given in Table 3.13.

**Table 3.13. Tier-indexed loss structure L(v, y, k)**

| Verdict v | L(v, 0, k): legitimate action | L(v, 1, k): adversarially induced action |
|---|---|---|
| Allow | 0 | C~miss~(k) |
| Modify | C~mod~(k) | r~mod~(k) · C~miss~(k) |
| Escalate | C~esc~ | C~esc~ |
| Block | C~FA~(k) | 0 |

All declared costs are non-negative and expressed in common relative units. Correct automatic decisions are assigned zero loss, which is a declared convention.

**Reviewer assumptions.** The Escalate entries assign the same loss C~esc~ whatever the label. This assumes a reviewer who:
- resolves every escalation correctly (accuracy 1);
- does so within the time the transaction allows, with delay and effort priced into C~esc~;
- is always available.

The verdict rule is optimal only under these assumptions. They are not tested in this thesis, because no reviewer is present. The rule is instead *evaluated* under two bounds (Section 3.11.7): an idealized reviewer that satisfies the assumptions, and no reviewer, in which every escalation withholds the action. A policy designed for a perfect reviewer and evaluated without one is expected to withhold legitimate actions; that cost is reported, not hidden. A reviewer with error rate e would add e·C~miss~(k) to the adversarial entry and e·C~FA~(k) to the legitimate entry of Escalate; such a model is not specified here.

The adversarial Modify entry is a derivation. Under the stated assumption A-Mod — whether Modify neutralizes an adversarially induced action is independent of x~t~ given the tier, and the attack fails with probability 1 − r~mod~(k) — the law of total expectation gives:

$$ L(\mathrm{Modify},1,k) = r_{\mathrm{mod}}(k)\, C_{\mathrm{miss}}(k) + \bigl(1-r_{\mathrm{mod}}(k)\bigr)\cdot 0 = r_{\mathrm{mod}}(k)\, C_{\mathrm{miss}}(k) \qquad (3.5) $$

where r~mod~(k) ∈ [0, 1] is the residual attack-success rate after Modify at tier k, measured in enforcing-mode runs (Section 3.11.7).

*Status:* derived under assumption A-Mod.

**Conditional risk.** Elkan (2001) states that the optimal prediction is the one that minimizes expected cost, computed from the conditional probability of each class and the cost of each prediction for each true class. REM applies this criterion to the four verdicts, with losses indexed by the consequence tier and the calibrated probability of Equation 3.3 in place of the true conditional probability:

$$ R_t(v) = (1-p_t)\, L(v,0,k_t) + p_t\, L(v,1,k_t), \qquad v \in \mathcal{V}(a_t) \qquad (3.6) $$

where R~t~(v) is the conditional risk of verdict v at step t.

*Status:* adapted from source. Elkan's criterion is stated for predictions of classes. REM extends the set of choices to four verdicts, indexes the losses by consequence tier, and substitutes the calibrated estimate p~t~ for the true posterior. The substitution is justified only to the extent that p~t~ is calibrated.

**Bayes verdict.** The verdict is:

$$ v_t = \arg\min_{v \in \mathcal{V}(a_t)} R_t(v) \qquad (3.7) $$

with ties resolved toward the more restrictive verdict in the declared order Block ⪰ Escalate ⪰ Modify ⪰ Allow.

*Status:* adapted from source; the tie-breaking order is a design definition that makes the rule a function. Ties are counted and reported whenever the rule is evaluated, so that the influence of the tie order on any result is visible.

The feasible set 𝒱(a~t~) contains Allow, Escalate, and Block for every action, and Modify only if the tool of a~t~ belongs to the set 𝒯~R~ to which the Modify mechanism applies (Section 3.8).

**Derived thresholds.** Each R~t~(v) is affine in p~t~, so the verdict changes only where two conditional risks are equal. For verdicts v and v′ at tier k, let Δ~0~ = L(v′, 0, k) − L(v, 0, k) and Δ~1~ = L(v, 1, k) − L(v′, 1, k), with Δ~0~ + Δ~1~ > 0. Setting R(v) = R(v′) in Equation 3.6 and solving for p gives:

$$ \pi_{v,v'}(k) = \frac{\Delta_0}{\Delta_0 + \Delta_1} \qquad (3.8) $$

*Status:* derived from Equation 3.6.

Derivation: R(v) − R(v′) = −Δ~0~ + p(Δ~0~ + Δ~1~). This is zero at p = π~v,v′~(k), negative below it (v is preferred), and positive above it (v′ is preferred).

For v = Allow and v′ = Block, Δ~0~ = C~FA~(k) and Δ~1~ = C~miss~(k), so:

$$ p^{*}_k = \frac{C_{\mathrm{FA}}(k)}{C_{\mathrm{FA}}(k) + C_{\mathrm{miss}}(k)} \qquad (3.9) $$

*Status:* derived from Equation 3.8. It has the form of the standard two-class cost-sensitive threshold for zero-cost correct decisions, which Elkan (2001) obtains from the same expected-cost criterion; the printed threshold expression in that paper could not be inspected directly during verification, so the derivation above stands on Equation 3.8 alone.

Thresholds are therefore consequences of declared costs rather than independently chosen constants. The question "why this threshold?" becomes "why this cost ratio?", which the loss grid of Section 3.12.3 addresses.

**When escalation can be selected.** Chow (1970) analyzed the tradeoff between recognition error and rejection, which is the classical basis for withholding an automatic decision. In REM, Escalate is not implemented as a separate rejection test; it is one of the verdicts inside Equation 3.7. For the verdict set {Allow, Escalate, Block} at tier k, Escalate is selected for some probability if and only if:

$$ C_{\mathrm{esc}} < \frac{C_{\mathrm{FA}}(k)\, C_{\mathrm{miss}}(k)}{C_{\mathrm{FA}}(k) + C_{\mathrm{miss}}(k)} \qquad (3.10) $$

*Status:* derived from Equations 3.6, 3.7, and 3.9.

Derivation: R(Allow) = p · C~miss~(k) increases in p and R(Block) = (1 − p) · C~FA~(k) decreases in p. Their minimum is largest at p^\*^~k~, where it equals C~FA~(k) · C~miss~(k) / (C~FA~(k) + C~miss~(k)). The constant C~esc~ lies strictly below this minimum for some p if and only if Equation 3.10 holds; at equality, ties resolve toward Block.

When Modify is also feasible, Equation 3.10 remains a necessary condition, because adding a verdict can only lower the minimum risk. In the symmetric case C~FA~(k) = C~miss~(k) = C, Equation 3.10 reduces to C~esc~ < C/2: deferral is selected only when it costs less than half an error.

**Dominance check.** Before a loss structure is used, it is checked for dominated verdicts. For example, R(Modify) − R(Block) = (1 − p)(C~mod~(k) − C~FA~(k)) + p · r~mod~(k) · C~miss~(k), which is non-negative for every p whenever C~mod~(k) ≥ C~FA~(k). In that case Modify can never be selected at tier k. A declaration that makes a verdict unreachable, by this check or by Equation 3.10, is reported as such rather than silently producing a smaller verdict set.

### 3.7.6 Explainability and audit record

For every verdict the Decision Engine writes an audit record containing:
- the identity of the proposed action: tool name and a digest of its arguments, recorded *before* any mitigation alters the step. Raw argument values, which may include credentials, are not stored;
- the evidence vector x~t~ with its availability flags, the logit s~t~, and the probabilities p̃~t~ and p~t~, with a flag stating whether p~t~ was used for the verdict;
- the tier k~t~ and the conditional risks R~t~(v), or *not applicable* when D1 or D2 fixed the verdict;
- the verdict v~t~ and its source (D1, D2, or the expected-loss rule), and the mitigation applied;
- the model, calibration, and policy versions;
- a linear attribution of the logit.

The attribution follows the linear case of Shapley-value attribution given by Lundberg and Lee (2017):

$$ \phi_{t,i} = \beta_i \,(x_{t,i} - \bar{x}_i),\; i = 1,\dots,d; \qquad \phi_0 = \beta_0 + \beta^{\top}\bar{x} \qquad (3.11) $$

where x̄ is the mean evidence vector over benign fitting steps, φ~t,i~ is the contribution of feature i to the logit relative to that benign reference, and φ~0~ is the logit at the reference.

*Status:* adapted from source. Lundberg and Lee (2017) state the linear case under feature independence with printed indices that do not match between the two sides of the expression and with base value equal to the model intercept. REM uses the index-consistent form and sets the base value to the logit at the reference point, which is the value required by their local-accuracy property when the reference mean is not zero.

The decomposition is exact:

$$ \phi_0 + \sum_{i=1}^{d} \phi_{t,i} = s_t \qquad (3.12) $$

*Status:* derived. Summing Equation 3.11 gives β~0~ + β^⊤^x̄ + β^⊤^x~t~ − β^⊤^x̄ = s~t~. This is the local-accuracy property of Lundberg and Lee (2017) for a linear model, and REM checks it as a correctness invariant.

For reporting by evidence group, REM defines:

$$ \Phi_J = \sum_{i \in I_J} \phi_{t,i}, \qquad J \in \{\mathrm{ctx}, \mathrm{beh}, \mathrm{act}\} \qquad (3.13) $$

*Status:* design definition. Because the groups partition the features, Φ~ctx~ + Φ~beh~ + Φ~act~ = s~t~ − φ~0~.

Four qualifications apply:

1. **The attribution never influences the verdict.** It is an audit component only.
2. **It decomposes the logit, not the calibrated probability.** On the calibrated logit scale each contribution is multiplied by γ~1~, which preserves relative contributions because γ~1~ > 0.
3. **Correlation limits interpretation, not the identity.** The independence assumption affects the interpretation of each φ~t,i~ as a Shapley value when features are correlated; it does not affect the identity of Equation 3.12.
4. **It is not a contribution.** Auditable decision records are provided by several existing systems (Hossain et al., 2026; C. Yang, 2026). Because the attribution is determined by the logged x~t~ and the frozen parameters, it can equally be computed at audit time.

### 3.7.7 Consequence-independent baseline policy

The baseline uses the same estimator and calibration but a decision rule that ignores consequence. Its thresholds are selected as operating points on benign validation steps:

$$ \theta(\alpha) = \min\{\theta : \mathrm{FPR}_{\mathrm{val}}(\theta) \le \alpha\}, \qquad \mathrm{FPR}_{\mathrm{val}}(\theta) = \frac{\left|\{ i \in D^{\mathrm{benign}}_{\mathrm{val}} : p_i \ge \theta \}\right|}{\left|D^{\mathrm{benign}}_{\mathrm{val}}\right|} \qquad (3.14) $$

where α is a declared false-positive target, D~val~^benign^ is the set of benign validation steps in the relevant cross-fitting fold, and θ ranges over the observed probabilities.

The baseline verdict is:
- **Block** if p~t~ ≥ θ(α~blk~);
- **Modify** if θ(α~mod~) ≤ p~t~ < θ(α~blk~) and Modify is feasible, otherwise Block;
- **Allow** otherwise.

The targets satisfy α~mod~ > α~blk~. Predicates D1 and D2 apply as in Section 3.7.4, so the baseline issues Escalate only through D2. In implementation the candidate set for θ also includes a value just above the largest benign probability, so that α = 0 can be met.

*Status:* design definition.

**What the comparison isolates.** REM and the baseline share the estimator, the calibration and the predicates. They differ in two respects: REM's losses depend on the consequence tier, and REM's expected-loss rule can choose Escalate, whereas the baseline can escalate only through D2. A difference between them therefore reflects both consequence tiers and the extra escalation opportunity, not tiers alone. A third configuration separates the two: **REM without expected-loss Escalate**, in which Escalate is removed from the set 𝒱(a~t~) used by Equation 3.7 but D2 is kept, gives REM exactly the baseline's opportunity to escalate.

Because Equation 3.14 selects thresholds by ranking, a strictly increasing recalibration re-selects equivalent thresholds and leaves the baseline's verdicts unchanged. Cost-derived thresholds such as Equation 3.9 are fixed in probability units and can change after recalibration. This contrast is used in the ablation of Section 3.11.7 and is consistent with the finding of C. Zhang et al. (2026) that recalibration need not change threshold-routed control.

## 3.8 Mitigation Layer

The Mitigation Layer executes, deterministically, the mechanism associated with each verdict. It never initiates an action on the agent's behalf.

**Table 3.14. Verdict-to-mitigation mapping: reference (step-level) semantics and the episode-level variant**

| Verdict | Step-level semantics (reference) | Episode-level variant |
|---|---|---|
| Allow | a~t~ is released across TB-3 and the event is logged. | Same, unless the tool is restricted in S, in which case a~t~ is refused. |
| Modify | a~t~ is withheld, and a structured tool-restriction notice is returned for this call only. No restriction persists. Applies only to tools in 𝒯~R~. | a~t~ is withheld, and the tool class of a~t~ (its action category within 𝒯~R~) is added to S for the rest of the episode. |
| Escalate | a~t~ is withheld and referred for review; it is released only if the reviewer approves. | Same. |
| Block | a~t~ is not executed, and a structured refusal is returned. No other tool is affected. | a~t~ is not executed, and every tool in 𝒯~R~ is added to S, so no further side-effecting action is released in the episode. |

**Which semantics is the reference.** The design decisions of Stage 2 fix step-level semantics: Block prevents the current action, and Modify applies one declared mechanism to the current action. Any restriction that persists through the episode is a separate experimental policy. The episode-level reading was specified in an earlier version of this chapter. Both are implemented and evaluated, and step-level semantics is the reference definition. This alignment with the frozen design lock awaits the supervisor's confirmation (decision D-2, conflict SC-1). Under the replay of Section 3.11.11 the two cannot differ, because a non-adaptive agent never retries a refused tool; distinguishing them requires live, adaptive agents.

Tool restriction is the single Modify mechanism because it is deterministic, does not depend on an LLM rewriting content, and can be measured. Under step-level semantics, Modify and Block have the same effect on the current call; they differ in the declared loss (Table 3.13), in the notice returned to the agent, and, under the episode-level variant, in what persists. Input sanitization, such as spotlighting (Hines et al., 2024), is an alternative that is not adopted as the primary mechanism.

Four properties are stated:

1. **Restrictiveness ordering.** Under the episode-level variant, Block halts all further side effects, Escalate defers the decision, and Modify removes one tool class. Under step-level semantics the ordering reflects the declared losses rather than persistence. The ordering underlies the tie-breaking order of Equation 3.7.
2. **𝒯~R~ is declared.** In the banking environment it contains value-transfer, payment-modification, credential-change, and profile-change tools; read tools are not restricted.
3. **Mitigation effectiveness is measured, not assumed.** The residual attack-success rate r~mod~(k) used in Equation 3.5 is estimated from enforcing-mode runs.
4. **Retries are observed.** A restricted or blocked agent may retry. Retries raise x^beh^~2~, and calls to restricted tools are refused by the Mitigation Layer.

## 3.9 Offline Fitting and Recalibration

Offline fitting and recalibration are cross-cutting activities. They are performed between deployments on logged data, they are not a layer, and they never modify REM's parameters during an episode. Runtime adaptation from observed traffic is excluded because it would allow an adversary who generates traffic to shift REM's reference behavior.

The offline procedure fits and freezes:
- the benign reference quantities (x̄ and the benign transition set);
- the coefficients by Equation 3.2, with λ selected by grouped cross-validation on held-out log-loss;
- the calibration parameters by Equation 3.4 on out-of-fold logits;
- the baseline thresholds by Equation 3.14;
- the measured residual rates r~mod~(k).

It also checks the declared loss structure for dominated verdicts (Section 3.7.5) and records all model, data, policy, benchmark, and software versions.

Between deployments, calibration can be monitored against later-established labels using the metrics of Section 3.12. If calibration drifts beyond a declared tolerance, the procedure is repeated on new data.

**Procedure 3.1. Offline fitting (cross-cutting; never executed within an episode)**

```
Input: logged observe-only traces grouped by injection task and user task; labels y;
       declared policy (κ, L, Π, k_D2, privilege map, 𝒯_R, α_blk, α_mod)
1  for each outer fold f (Section 3.11.5):
2      D_train ← steps outside fold f;  D_test ← steps in fold f
2a     apply the Pilot E0 retention rule to D_train only; fix the feature set for fold f
3      estimate x̄ and the benign transition set on benign steps of D_train
4      select λ by grouped inner cross-validation on D_train (held-out log-loss)
5      obtain out-of-fold logits on D_train from inner folds; fit (γ1, γ0) by Eq. 3.4
6      if γ1 ≤ 0 then record calibration failure for fold f
7      refit (β0, β) on all of D_train with the selected λ (Eq. 3.2)
8      select θ(α_blk), θ(α_mod) by Eq. 3.14 on out-of-fold calibrated benign steps of D_train
9      apply Eqs. 3.1, 3.3 to D_test; store predictions for evaluation only
9a     estimate r_mod(k) from episodes outside fold f: enforcing-mode runs (Section 3.11.7),
       or, where these are unavailable, oracle-Modify replays (Section 3.11.11)
10 (r_mod is estimated per fold in line 9a)
11 check the loss structure for dominated verdicts (Section 3.7.5)
12 freeze parameters and record all versions
```

## 3.10 Algorithm 1: REM Runtime Evaluation and Mitigation

Algorithm 1 gives the per-step runtime procedure. Every operation is defined in Sections 3.4–3.8.

```
Algorithm 1. REM Runtime Evaluation and Mitigation (as implemented; Chapter 4)

Frozen (offline, per fold):  β0, β, γ1 (> 0), γ0, x̄, benign transition set,
                             privilege map, instruction-pattern set, n_max
Declared policy:             κ, L (Table 3.13), Π, k_D2, required evidence, 𝒯_R,
                             tie order Block ⪰ Escalate ⪰ Modify ⪰ Allow,
                             mitigation semantics ∈ {step-level, episode-level}
Input at step t:             objective g; tool results since the last step;
                             proposed call a_t = (tool, args); history H_t; restrictions S
Output:                      verdict v_t; released or withheld call; audit record r_t

 1  for each tool result returned since the last decision point:           // Layer 1
 2      label it untrusted; strip invisible characters in REM's copy;
 3      extract identifiers and profile values from sensitive reads
 4  begin a decision point (calls proposed in one agent message share it)
 5  for each proposed call a_t in the message:
 6      x_t, avail ← features of Tables 3.8–3.9 from H_t, a_t, g           // Layers 2–3
 7      k_t ← κ(z_t)                                                       // Layer 4
 8      s_t ← β0 + βᵀx_t;  p_t ← σ(γ1·s_t + γ0)       // computed for audit; see lines 9–14
 9      if tool(a_t) ∈ Π then v_t ← Block; src ← "D1"; R ← not applicable
10      else if k_t ≥ k_D2 and required evidence ⊄ avail then
11          v_t ← Escalate; src ← "D2"; R ← not applicable
12      else                                   // unavailable features below k_D2 are 0 and flagged
13          V_t ← {Allow, Escalate, Block} ∪ ({Modify} if tool(a_t) ∈ 𝒯_R)
14          R[v] ← (1 − p_t)·L(v,0,k_t) + p_t·L(v,1,k_t) for v ∈ V_t;  v_t ← argmin, ties by order
15      // Layer 5
16      if episode-level and tool(a_t) ∈ S then refuse a_t
17      else if v_t = Allow then release a_t
18      else if v_t = Modify then withhold a_t; if episode-level, S ← S ∪ class(a_t)
19      else if v_t = Escalate then withhold a_t; release only on reviewer approval
20      else (Block) withhold a_t; if episode-level, S ← S ∪ 𝒯_R
21      r_t ← (tool name, argument digest, x_t, avail, s_t, p̃_t, p_t, p-used flag, k_t,
               R, v_t, src, mitigation, φ0, φ_t, |φ0 + Σφ − s_t|, versions, REM time)
22      append r_t to the audit log; append a_t to H_t (released or not)
23  released calls execute; their results enter line 1 at the next decision point
```

Line 8 computes the probability for every step so that the audit record is complete; when line 9 or line 10 applies, the record marks p~t~ as not used. Lines 16–20 implement both mitigation semantics of Table 3.14. Attribution (line 21) is computed after the verdict and cannot reach it.

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

**Execution status.** Enforcing-mode runs with a live agent require access to an LLM, which was not available for this thesis. The observe-only analyses (Sections 3.11.5–3.11.10) use recorded traces of real agents distributed with the benchmark (Section 3.11.2). Enforcement is examined only through the replay sensitivity analysis of Section 3.11.11.

### 3.11.2 Dataset

The banking suite definition inspected for this chapter (suite v1, AgentDojo repository main branch, accessed September 2026) contains:

- **16 user tasks.** Examples include paying a bill described in a file, refunding a friend, updating a recurring rent payment, and updating account details. Their reference solutions use between one and five tool calls.
- **9 injection tasks.** Eight direct money or a recurring payment toward one shared attacker account identifier. One changes the account password. The reference attacker actions consist of one call for seven tasks, two calls for one task (reading scheduled transactions, then sending money), and three calls for one task (a total amount split into smaller transfers).
- **11 tools:** get_iban, send_money, schedule_transaction, update_scheduled_transaction, get_balance, get_most_recent_transactions, get_scheduled_transactions, read_file, get_user_info, update_password, and update_user_info.

These counts were re-confirmed against suite v1 in AgentDojo 0.1.35. The recorded traces used in the evaluation come from the AgentDojo repository at commit 089ed468; most carry no suite-version field, and some backbones were recorded under later suite versions (Chapter 5). The label-relevant definitions of the nine injection tasks are identical in every suite version from v1 to v1.2.2.

AgentDojo is an environment, not a fixed dataset of traces. Traces are generated by running an agent, so the number of traces depends on the number of backbones, attack templates, and repeated runs. The counts used in this thesis are reported, from the data, in Chapter 5. The 144 combinations of user task and injection task are not 144 independent samples. They are built from 16 user-task templates and 9 injection-task templates, and every trace inherits the dependence of its templates.

### 3.11.3 Label construction

The label must represent the quantity the estimator is asked to predict, which is whether a proposed call serves the attacker's objective rather than the user's. Labels are therefore derived from the injection task's own reference solution, not from the presence of an injection in the episode, because an attacked episode also contains benign calls. The derivation is mechanical, so the rules below state exactly what is matched, where the rule is known to be uncertain, and how that uncertainty is measured.

- **Step labels.** In an attacked episode, a proposed tool call is labeled y~t~ = 1 if it matches a call in the injection task's reference solution on tool name and on the attacker-controlled key argument, such as the attacker account identifier or the attacker-specified password. All other proposed calls, including calls that continue the user's task in attacked episodes, are labeled y~t~ = 0, as are all calls in episodes without injection.
- **Induced read steps.** Some injection tasks include a read call in their reference solution. Whether such a read step is labeled y~t~ = 1 is pending supervisor decision, because it is induced but has no direct external effect.
- **Label audit.** Matching on arguments can mislabel steps, for example when an agent alters an amount or reaches the attacker through a different tool. The derivation is therefore to be audited by a human annotator on a stratified sample of episodes, including ambiguous cases, and the disagreement rate reported.
- **What the label measures.** The reference-match label is a *practical proxy* for adversarial inducement. It records that the agent proposed the attacker's reference action with the attacker's key argument; it is not a causal proof that the injected content caused the proposal. A legitimate action that coincides with the attacker's reference action is mislabelled as induced, and an induced action that takes another route is mislabelled as legitimate. Both errors are measured, not assumed away.

### 3.11.4 Data limitations

The design must respect five limitations of the data:

1. **Positive-step scarcity.** A step is labeled y~t~ = 1 only if the agent actually proposes the attacker's call. The number of positive steps therefore depends on how often the chosen backbone follows injected instructions, and it may be small; the observed count is reported in Chapter 5. Most steps are benign, so the classes are strongly imbalanced.
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

**Independence of every fitted quantity from the held-out fold.** For outer fold f, each of the following uses only the fitting portion D_train(f):
- the benign transition set and x̄, re-estimated also within each inner fold;
- λ, selected by grouped inner cross-validation;
- (γ₁, γ₀), fitted on out-of-fold logits from the inner folds;
- the baseline thresholds θ(α), selected on out-of-fold calibrated benign steps;
- r~mod~(k), estimated from episodes outside fold f;
- the feature set: the Pilot E0 rule (Section 3.11.8) is applied to each fold's fitting portion. If the folds disagreed, each fold would use its own set. In this thesis they agree (Chapter 5).
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
- **REM without expected-loss Escalate.** As REM, with Escalate available only through D2, which gives REM the baseline's escalation opportunity (Section 3.7.7). This configuration was added after the first pilot results and is reported as a post-hoc comparison.
- **B2, detection-only (pending supervisor approval).** The Detection Layer's classifier score applied to untrusted content with an operating-point threshold. It tests whether Layers 3 and 4 add value.
- **Distributed defenses (pending supervisor approval).** Any defenses distributed with the pinned benchmark version, to address O3.

**Ablations of REM** (each changes one element, all else fixed; the estimator is refitted when an evidence group is removed):

1. Context evidence removed.
2. Behavioral evidence removed.
3. Action evidence removed.
4. Calibration removed (p̃~t~ used in Equation 3.6).
5. Consequence tiers removed (one tier for all actions).
6. Predicates D1 and D2 disabled.
7. Observe-only (no mitigation).

**Mitigation-effectiveness runs.** Enforcing-mode runs in which Modify is applied to adversarial steps estimate r~mod~(k) per tier and the utility impact of Modify on benign steps. These estimates feed Equation 3.5 and are fitted within the outer folds so that no held-out episode informs its own loss values. In this thesis, live enforcing-mode runs were not available. r~mod~(k) was therefore estimated by replaying recorded attack episodes with Modify applied to every labelled attack step (Section 3.11.11). Under the no-adaptation assumption these estimates are close to zero by construction, and they are reported as such. The utility impact of Modify on benign steps was not estimated separately.

**Escalation in experiments.** No human reviewer is available in the benchmark. Escalation is resolved in two ways:
- by an idealized reviewer who releases the action if y~t~ = 0 and prevents it if y~t~ = 1;
- by a no-reviewer bound in which every escalation is treated as Block.

Both are reported, so the dependence of any result on the reviewer assumption is visible.

### 3.11.8 Pilot E0

Before the feature set is frozen, a pilot run on the fitting portions of the outer folds checks feasibility:

- the number of positive steps per backbone and attack template;
- the ROC-AUC of each evidence group alone and combined.

The pilot's decision values are project decisions declared before the pilot, not literature-derived thresholds [pending supervisor approval]:
- the minimum number of positive steps needed to proceed;
- the minimum group ROC-AUC needed to retain an evidence group.

If the positive-step count is insufficient, additional attack templates or backbones are added before the main experiments. The pilot never uses held-out fold predictions. Because every outer fold's held-out data belong to the fitting portions of the other folds, a single global decision taken from all folds' pilot results would use each fold's held-out data indirectly. The retention rule is therefore applied per fold, to that fold's fitting portion only.

### 3.11.9 Repeated runs and uncertainty

Each configuration is run at least three times with fixed decoding parameters to characterize LLM non-determinism [number of runs pending supervisor approval]. Repeated runs of the same template are not independent. Results are therefore aggregated per episode template before uncertainty is estimated.

Confidence intervals are obtained by bootstrap resampling (Efron, 1979) at the level of injection-task groups for attacked episodes and user-task groups for benign episodes. Resampling groups rather than steps is a design choice that respects the dependence described in Section 3.11.2.

With nine injection-task groups, intervals will be wide. No statistical power has been established, so differences are reported as measured differences with their intervals, and the word "significant" is not used unless a stated test supports it.

### 3.11.10 Optional observe-only sequential analysis

Sequential change detection is not part of REM's verdict path. If the supervisor approves it for the thesis narrative, it is performed **offline** on the per-step indicators logged by the Behavioral Analysis Layer. It never influences a verdict.

For each step, a binary deviation indicator e~t~ ∈ {0, 1} is defined as 1 if at least one of x^beh^~1~, x^beh^~3~, x^beh^~4~, or x^act^~1~ equals 1, or if x^beh^~2~ = 1; otherwise 0 [indicator set pending supervisor approval]. Let q~0~ and q~1~, with 0 < q~0~ < q~1~ < 1, be the rates of e~t~ = 1 before and after an adversarial change.

The log-likelihood ratio of one observation, as defined by Basseville and Nikiforov (1993), specialized to Bernoulli observations, is:

$$ \ell_t = e_t \ln\frac{q_1}{q_0} + (1-e_t) \ln\frac{1-q_1}{1-q_0} \qquad (3.15) $$

*Status:* derived by substituting the Bernoulli probability mass function into the log-likelihood ratio of Basseville and Nikiforov (1993). A cumulative sum chart for Bernoulli observations is treated by Reynolds and Stoumbos (1999).

The cumulative sum statistic and alarm time are (Basseville & Nikiforov, 1993; Page, 1954):

$$ G_t = \max(0,\, G_{t-1} + \ell_t), \qquad G_0 = 0 \qquad (3.16) $$

$$ T_A = \min\{ t : G_t \ge h_G \} \qquad (3.17) $$

where h~G~ > 0 is the alarm threshold.

*Status:* established from source.

The per-episode false-alarm rate on benign episodes and the detection delay are defined as:

$$ \mathrm{FA}_{\mathrm{ep}}(h_G) = \frac{\left|\{ j \in E_{\mathrm{ben}} : \max_t G^{(j)}_t \ge h_G \}\right|}{\left|E_{\mathrm{ben}}\right|} \qquad (3.18) $$

$$ \tau_d = T_A - \nu, \qquad T_A \ge \nu \qquad (3.19) $$

where E~ben~ is the set of benign episodes in the fitting portion of a fold, G^(j)^~t~ is the statistic in benign episode j, τ~d~ is the detection delay, and ν is the first step at which injected content enters the context.

*Status:* design definitions.

The parameters are determined as follows:
- q~0~ is the empirical rate of e~t~ = 1 on benign fitting steps, floored at a declared minimum.
- q~1~ is declared and reported over a range, because the scarcity of multi-step attacks does not allow it to be estimated reliably.
- h~G~ is the smallest value for which Equation 3.18 does not exceed a declared target.

The procedure has known optimality properties in sequential change detection: Lorden (1971) proposed stopping rules that are asymptotically optimal in a defined sense, and Moustakides (1986) showed Page's stopping time to be optimal in a stronger sense. Both results are proved within a sequential-analysis model whose conditions could not be inspected during verification and are not claimed to hold for agent trajectories, where observations are neither independent nor drawn from known distributions. They therefore motivate the procedure and provide no guarantee in this setting. Given the short trajectories of Section 3.11.4, this analysis may have little to detect.

### 3.11.11 Recorded-trace replay sensitivity analysis *[proposed scope amendment, pending supervisor approval]*

Live enforcing-mode runs were not possible (Section 3.11.1). To obtain any evidence about enforcement, each recorded episode is re-executed in the benchmark's own sandbox with REM at the tool boundary:
- a replay element emits the agent's recorded messages in order;
- the benchmark executes the released calls;
- the benchmark's utility and security checks score the result.

**Assumption NO-ADAPT.** The agent emits the calls it emitted in the recorded run, whatever REM does. A live agent may retry, rephrase or choose another tool after a refusal. Replay results therefore do not estimate enforcement against live or adaptive agents, and they cannot distinguish step-level from episode-level semantics.

**Validity checks.** An all-Allow replay must reproduce the recorded utility and security outcome. Episodes for which it does not are excluded from every replay metric, and the exclusions are reported.

**Not independent repetitions.** Replaying the same recorded trace several times is deterministic. It is not an independent repetition of LLM behavior and does not substitute for the repeated runs of Section 3.11.9.

**Relation to the excluded method.** This analysis differs from counterfactual estimation of intervention value (Section 3.1.4): it executes no alternative actions and makes no claim about what an agent would have done instead.

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

**Discrimination.** ROC-AUC (Fawcett, 2006) and PR-AUC (Davis & Goadrich, 2006) are computed on held-out probabilities. PR-AUC is emphasized because positive steps are rare. Within a fold, both are unchanged by calibration with γ~1~ > 0. Because each outer fold has its own calibration map, metrics are reported per fold as well as on the pooled held-out predictions.

**Calibration error.** For binary outcomes, calibration error is measured on the positive-class probability (Naeini et al., 2015) with M equal-width bins (Guo et al., 2017):

$$ \mathrm{ECE} = \sum_{m=1}^{M} \frac{|B_m|}{N} \left| \bar{y}(B_m) - \bar{p}(B_m) \right|, \qquad B_m = \{ i : (m-1)/M < p_i \le m/M \} \qquad (3.20) $$

where N is the number of held-out steps, ȳ(B~m~) is the fraction of positive steps in bin m, p̄(B~m~) is the mean calibrated probability in bin m, and M is declared in advance (steps with p~i~ = 0 are assigned to the first bin).

*Status:* adapted from source. Naeini et al. (2015) supply the binary form; Guo et al. (2017) supply the equal-width binning.

Because a global ECE averages over all probabilities, reliability is also reported within declared windows around each tier's threshold p^\*^~k~.

**Log-loss.** The mean negative log-likelihood of held-out steps is:

$$ \mathrm{LL} = -\frac{1}{N} \sum_{i=1}^{N} \left[ y_i \ln p_i + (1-y_i)\ln(1-p_i) \right] \qquad (3.21) $$

*Status:* derived as the negated, averaged, unpenalized log-likelihood term of Equation 3.2 evaluated at the calibrated probabilities. Probabilities are bounded away from 0 and 1 by a declared small constant for numerical evaluation.

**Brier score.** The Brier score is not reported until the convention of its original source (Brier, 1950) has been confirmed; log-loss serves as the proper scoring measure in the meantime.

### 3.12.3 Realized loss across a declared grid

Realized loss is secondary because it depends on declared costs, and because a rule that minimizes expected loss under L is favored by construction when evaluated under the same L. For an evaluation loss structure L~e~:

$$ \bar{L}(L_e) = \frac{1}{N} \sum_{i=1}^{N} L_e(v_i, y_i, k_i) \qquad (3.22) $$

where v~i~ is the verdict issued for held-out step i under the decision loss structure L~d~, y~i~ is its label, and k~i~ is its tier.

*Status:* design definition.

The grid is declared before held-out predictions are examined and varies three things:
- the ratio C~miss~(k)/C~FA~(k) per tier;
- C~esc~;
- the amount limits of the tier map.

For each evaluation structure L~e~, the grid reports:
- REM with L~d~ = L~e~ (matched);
- REM with L~d~ ≠ L~e~ (misspecified costs);
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

The contribution holds only to the extent that the experiments specified in this chapter support it. Chapter 5 reports which of these experiments were executed (offline classification, observe-only policy analysis, replay sensitivity) and which were not (live enforcing-mode runs).

## 3.14 Threats to Validity

**Construct validity.**
- Step labels are derived and can be wrong; the derivation is audited on a sample (Section 3.11.3).
- The idealized reviewer overstates the protective value of Escalate; the no-reviewer bound is reported alongside it.
- Declared costs cannot be validated empirically; their influence is reported across the grid.
- A low ASR can reflect task failure rather than protection, so utility metrics accompany every security metric (Y. Wang et al., 2026).

**Internal validity.**
- Leakage through shared templates and the shared attacker account identifier is controlled by grouping and by excluding identity-based features, but template dependence remains.
- Features designed with knowledge of the benchmark may fit its style; the feature set is frozen after the pilot and before held-out predictions are examined.
- LLM non-determinism is characterized by repeated runs; the recorded traces contain one run per configuration, so this requirement is not met in this thesis.

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
- A scalar probability cannot represent whether an adversarial trajectory remains recoverable, so REM inherits the limitation identified by C. Zhang et al. (2026); estimating intervention value for adaptive agents by counterfactual replay is outside the scope of this thesis.

## 3.15 Equation Provenance Summary

**Table 3.17. Provenance of the equations in this chapter**

| Eq. | Content | Status | Source | Verification |
|---|---|---|---|---|
| 3.1 | Logistic model | Established | Cox (1958) | IV |
| 3.2 | Ridge-penalized log-likelihood | Established | le Cessie & van Houwelingen (1992) | IV (penalty constant pending) |
| 3.3 | Logistic calibration on the logit, γ~1~ > 0 | Adapted | Platt (1999); Guo et al. (2017); Kull et al. (2017) | Platt NC; Guo FV; Kull FV |
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

**Implementation conventions.** Four conventions in the implementation differ in form from the equations as printed; none changes their meaning:

- **Eq. 3.2:** the code's penalty is (λ~impl~/2)‖β‖², so λ = λ~impl~/2 (Section 3.7.1).
- **Eq. 3.4:** the label-NLL fit is the reference; Platt's smoothed targets are a sensitivity variant.
- **Eq. 3.14:** the candidate set includes a value just above the largest benign probability.
- **Eq. 3.20:** steps with p = 0 fall in the first bin.

These conventions are listed with the code location of each equation in the requirement–equation–function–test table of Chapter 4.

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
