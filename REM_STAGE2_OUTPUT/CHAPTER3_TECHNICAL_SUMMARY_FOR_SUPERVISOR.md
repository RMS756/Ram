---
title: "Chapter 3 — REM Framework, Algorithmic Design, Mathematical Formulation, and Implementation Requirements"
subtitle: "Technical summary of the current Chapter 3 for supervisor review"
author:
  - "Master's thesis supporting document — Runtime Evaluation and Mitigation (REM) framework for securing financial AI agents"
date: "23 September 2026"
abstract: |
  This document explains the current version of Chapter 3 (working file `working/Chapter3_working.md`, SHA-256 prefix `5085e11732dee82f`). It is an explanation and documentation of that chapter. It does not modify, rewrite or redesign Chapter 3, and it introduces no algorithm, equation, parameter value, dataset or result that is absent from Chapter 3 or from an existing verified project record. Documented uncertainty is preserved throughout.
toc-title: "Contents"
abstract-title: "Document status"
lang: en-GB
---

# Document Scope and Conventions

## Sources

The primary source is the current Chapter 3 working file. Supporting evidence is taken only from the following project records:

- `REM_STAGE2_INPUT_PACKAGE/THESIS_READING_INDEX.md` (reference-level verification status of every cited source);
- `REM_STAGE2_INPUT_PACKAGE/PAPER_READING_PACK/` (claim-to-paper map and per-paper reading notes);
- `REM_STAGE2_OUTPUT/STAGE2_RESOLUTION_REPORT.md` (Stage 2 verification results);
- the Stage 1 audit workbooks (reference master, claim audits, equation-source audit, numerical-claims audit);
- the existing algorithm-selection and mathematical-decision documents, and the design contract `CLAUDE.md`.

Line numbers written as "L" followed by a number refer to the Chapter 3 working file unless another file is named.

## Verification Terminology

Two independent kinds of verification status are reported, and they are not merged.

Table: Table 1. Verification terminology used in this document

| Term | Meaning | Origin |
|------------------|---------------------------------------------|-------------------------------------|
| VERIFIED | Reference-level status: the work exists, its metadata matches the record, and the content attributed to it was checked in the source (full text, or the abstract where the claim appears there) | THESIS_READING_INDEX.md |
| PARTIALLY VERIFIED | Reference-level status: the work is identified, but the content used was not checked in the source, or part of the cited metadata conflicts with the record | THESIS_READING_INDEX.md |
| FV | Equation formulation checked against the source | Chapter 3, Table 3.17 |
| IV | Source identity confirmed; formulation still to be checked against the full text | Chapter 3, Table 3.17 |
| NC | Source not accessible during the revision | Chapter 3, Table 3.17 |
| DER | Derived within Chapter 3 | Chapter 3, Table 3.17 |
| DEF | Design definition introduced by Chapter 3 | Chapter 3, Table 3.17 |
| SOURCE NOT FULLY VERIFIED | The attribution of an expression to a source has not been confirmed against the source text | This document |
| NOT SPECIFIED IN CURRENT CHAPTER 3 | A requirement that implementation needs but that Chapter 3 does not specify | This document |
| SUPERVISOR DECISION REQUIRED | An item that Chapter 3 or the project records leave open, or a conflict between Chapter 3 and a frozen project record | This document |

Open verification items are cited by the identifiers used in `THESIS_READING_INDEX.md`, Section 6 (for example OI-01 and OI-07). Where a reference is marked VERIFIED, the verification may have been performed at abstract level; the reference list at the end of this document states the basis for each source.

## Specification Conflicts Identified During Preparation

Two points on which the current Chapter 3 differs from other frozen project records were identified while this summary was prepared. They are described in Sections 7.5 and 15.1 and are not resolved here.

1. **Mitigation semantics.** Chapter 3 (Table 3.14, L536–L538) specifies Modify as removal of a tool class for the rest of the episode and Block as restriction of every tool in the declared set $\mathcal{T}_R$ for the rest of the episode. The project design contract (`CLAUDE.md`, Mitigation Lock) defines Modify and Block at the level of the current action and states that any episode-level restriction is a separate experimental policy requiring explicit specification. SUPERVISOR DECISION REQUIRED.
2. **Tie-breaking.** Chapter 3 resolves an exact tie in the verdict rule toward the more restrictive verdict (Equation 3.7). The project prototype records that no tie-breaking rule is frozen and raises an error on an exact tie. SUPERVISOR DECISION REQUIRED.

# 1. Introduction and Purpose

## 1.1 Purpose of Chapter 3

Chapter 3, *Research Methodology and Design of the REM Framework*, states the research methodology of the thesis and specifies the design of the Runtime Evaluation and Mitigation (REM) framework. The thesis follows design science research, in which knowledge is produced by building an artifact that addresses an identified problem and evaluating it rigorously (Hevner et al., 2004). The research process follows the six activities of the design science research methodology of Peffers et al. (2007).

Table: Table 2. Design science research activities (Chapter 3, Table 3.1)

| Activity | Realization in the thesis | Location |
|--------------------------|----------------------------------------------|---------------------------|
| Problem identification and motivation | Runtime compromise of tool-using financial agents through indirect prompt injection | Chapters 1 and 2 |
| Definition of objectives for a solution | Objectives O1–O3; research questions RQ1–RQ4; security objectives SO-1 to SO-6 | Chapter 3, Sections 3.1.2, 3.1.3, 3.3.7 |
| Design and development | Five-layer REM architecture and runtime pipeline | Chapter 3, Sections 3.2–3.10 |
| Demonstration | Integration of REM with the AgentDojo banking environment | Chapter 4 |
| Evaluation | Controlled experiments, baseline comparison and ablation | Chapter 3, Sections 3.11–3.12; Chapter 5 |
| Communication | Thesis and derived publications | Chapter 6 |

The evaluation is quantitative and experimental. REM is compared against a baseline that uses the same probability estimator with a consequence-independent decision rule, so that differences in outcome can be attributed to the decision rule rather than to the estimator.

## 1.2 Problem Addressed

The problem addressed is the runtime compromise of tool-using financial agents through indirect prompt injection. Indirect prompt injection occurs when content from an external source, processed by the agent, alters its behavior (OWASP Gen AI Security Project, 2025). Chapter 3 defines REM's target event more narrowly and at the level of the action: a proposed action $a_t$ is *adversarially induced* ($y_t = 1$) if executing it would advance an objective introduced by the adversary rather than the user objective $g$. The label is not observable at runtime. Actions that are unsafe because of the agent's own error, without adversarial involvement, are outside this definition (Chapter 3, Section 3.3.5).

## 1.3 Runtime Evaluation and Mitigation (REM)

Chapter 3 describes REM as a runtime mediation layer between one agent and its environment, comprising exactly five layers (Section 2). At each step REM evaluates the action the agent proposes, estimates the probability that the action is adversarially induced, selects one of four verdicts (Allow, Modify, Escalate, Block) and executes the associated mitigation mechanism before the action is released to the environment.

## 1.4 Financial AI-Agent Security Context

The evaluation instance is an agent operating the AgentDojo banking environment (Debenedetti et al., 2024). Chapter 3 groups the eleven tools of that environment by the consequence of an adversarially induced call. The grouping is a design classification, not a property reported by the benchmark.

Table: Table 3. Action categories in the banking environment (Chapter 3, Table 3.7)

| Category | Tools | Consequence if adversarially induced |
|-----------------|---------------------------------------|---------------------------------------------|
| Read | get_balance, get_iban, get_most_recent_transactions, get_scheduled_transactions, get_user_info, read_file | No direct external effect; may expose data later sent elsewhere |
| Value transfer | send_money, schedule_transaction | Money sent to an attacker-controlled account |
| Payment modification | update_scheduled_transaction | Redirection or alteration of a recurring payment |
| Credential change | update_password | Loss of control over the account |
| Profile change | update_user_info | Alteration of account holder information |

## 1.5 Non-Invasive Deployment

REM is designed to operate without modifying the agent. Training-time defences and modification of the agent's model or prompts are out of scope (Chapter 3, Section 3.1.4). REM is placed at the tool-execution boundary of the agent loop, where it intercepts each proposed tool call before execution and each tool result on return (Section 3.11.1). Chapter 3 states that the achievability of this placement without modifying the agent's internals is assumption AS-1, "to be demonstrated" in Chapter 4. Non-invasiveness is therefore a design requirement whose feasibility has not yet been demonstrated.

## 1.6 Agent, REM and External Environment

The protected system is a single LLM-based agent that pursues a user objective by proposing tool calls. REM treats the agent as opaque (Section 3.3.1). At each step, REM executes its five layers before the proposed action is released to the environment. After an action is released, its tool result re-enters REM's first layer as untrusted content for the next step (Section 3.2.2). The external elements named in the architecture specification are user and system inputs, tool outputs and retrieved content (untrusted), the agent (opaque), tools and environment, and a human reviewer.

## 1.7 Observation and Action Boundaries

Chapter 3 defines four trust boundaries.

Table: Table 4. Trust boundaries (Chapter 3, Table 3.6)

| ID | Boundary | Direction | Treatment in REM |
|----------|----------------|------------------------------------|--------------------------------------|
| TB-1 | User input | User → agent context | Labeled semi-trusted |
| TB-2 | Observation | Tool outputs and retrieved content → agent context | Labeled untrusted; primary observation point |
| TB-3 | Action | Agent → tools and external systems | Primary enforcement point |
| TB-4 | Memory | Context ↔ persistent store | Provenance retained on read and write (design scope only) |

Untrusted content is any context segment that entered through TB-2 or TB-4, or that was derived from such a segment. The observation boundary matters because content arriving there enters after the user's request, which is the route exploited by indirect prompt injection (Greshake et al., 2023; OWASP Gen AI Security Project, 2025). The action boundary matters because it is the last point at which an induced action can be prevented rather than repaired (Section 3.3.3).

## 1.8 What REM Observes and What It Does Not Modify

At step $t$, REM observes the user objective $g$, the labeled context $c_t$, the proposed action $a_t$, and the history $H_t$ of prior contexts, actions, verdicts and tool results (Section 3.3.2). REM observes inputs, context, proposed actions and tool results, but not model parameters or internal reasoning (assumption AS-10).

REM does not modify the agent's model, prompts or internals (Section 3.1.4; AS-1). The Mitigation Layer never initiates an action on the agent's behalf (Section 3.8). REM's own parameters are never changed during an episode; fitting and recalibration are performed offline between deployments (Section 3.9).

## 1.9 Objectives, Research Questions and Scope

The approved objectives are O1 (design a REM framework for financial AI agents' and task automation agents' security), O2 (evaluate the framework against adversarial attacks) and O3 (compare performance with existing security approaches). The evaluation uses a financial (banking) environment; task-automation environments are outside the evaluation scope unless approved as an extension.

The approved proposal does not state research questions. Chapter 3 derives four research questions from the objectives and presents them for supervisor confirmation. They are therefore proposed, not approved: RQ1 (estimation), RQ2 (decision), RQ3 (mitigation and cost) and RQ4 (component contribution). SUPERVISOR DECISION REQUIRED (confirmation of RQ1–RQ4).

Table: Table 5. Scope (Chapter 3, Section 3.1.4)

| In scope | Out of scope |
|--------------------------------------------------|--------------------------------------------------|
| A single LLM-based agent that invokes tools with generated arguments | Training-time defences and modification of the agent's model or prompts |
| A financial (banking) task environment with executable tools and state-based checks | Multi-agent systems |
| Indirect prompt injection through tool outputs as the evaluated attack class | Evaluation against adaptive adversaries who tune attacks to REM |
| Runtime mediation of each proposed tool call before it is released | Production deployment in a financial institution; counterfactual estimation of intervention value by replaying agent trajectories |

The evaluated adversary (AD-1) can author or modify content that the agent receives through tool outputs, including instruction-like text and values such as account identifiers. It cannot access the user channel, observe or modify REM's parameters, or modify agent or REM code. A prompt-channel adversary (AD-2) is in design scope only. Adversaries who modify model weights, agent code or REM, infrastructure compromise, a malicious operator and adaptive adversaries are excluded (Section 3.3.4).

# 2. REM Framework Architecture

## 2.1 Overview of the Five Layers

REM comprises exactly five layers, as approved in the research proposal. Offline fitting and recalibration are cross-cutting activities performed between deployments. They are not a layer, are not numbered with the layers, and never change REM's parameters during an episode. No sixth layer, separate risk-score layer or feedback-loop layer exists in the design.

Table: Table 6. The five REM layers (Chapter 3, Sections 3.2.1 and 3.2.3)

| Layer | Purpose | Consumes | Produces |
|---------------|-----------------------------------|--------------------------|------------------------|
| L1 Input & Context | Capture the information the agent handles and the action it proposes; label each context segment with its provenance | Objective, system prompt, user messages, tool results, proposed action | Labeled context $c_t$; entities with provenance; held action $a_t$ |
| L2 Detection | Compute evidence about untrusted context | Untrusted segments of $c_t$ | Context evidence $x^{\text{ctx}}$ |
| L3 Behavioral Analysis | Compute evidence about the episode history and the proposed action | $H_t$, $a_t$, entities, benign reference transitions, privilege map | Behavioral evidence $x^{\text{beh}}$; action evidence $x^{\text{act}}$ |
| L4 Decision Engine | Estimate the probability of adversarial induction, assign a consequence tier, apply policy predicates, select a verdict and write the audit record | $x_t$, consequence descriptors $z_t$, frozen parameters, declared policy | $p_t$, $k_t$, $R_t(\cdot)$, verdict $v_t$, audit record |
| L5 Mitigation | Execute the mechanism associated with the verdict | $v_t$, $a_t$, episode restrictions | Released, restricted, withheld or refused action |

The four functions are separated architecturally. Layers 2 and 3 produce evidence and issue no verdicts. Layer 4 performs probability estimation and decision. Layer 5 performs mitigation. At each step REM executes Layer 1, then Layers 2 and 3 in parallel on Layer 1's output, then Layer 4, then Layer 5. Because Layers 2 and 3 compute their evidence independently and are combined only in the Decision Engine, an evidence group can be removed in ablation without changing the computation of the other (Section 3.2.2).

## 2.2 Layer 1: Input & Context Layer

Table: Table 7. Layer 1 — Input & Context

| Aspect | Description (Chapter 3, Section 3.4) |
|-------------------|---------------------------------------------------------------------------------|
| Purpose | Collect and label information. The layer computes no risk evidence. |
| Inputs | User objective $g$ and user messages (TB-1); system prompt; results of previously executed tools (TB-2); proposed action $a_t$, captured at TB-3 and held until Layer 5 acts. |
| Processing | (i) Removal of invisible and formatting characters, such as zero-width characters, from untrusted text (deterministic hygiene). (ii) Provenance labeling with the ordered set trusted (system prompt) ≻ semi-trusted (user input) ≻ untrusted (tool output, retrieved content, memory); derived content inherits the least-trusted label among its sources, and processing never promotes content to a more trusted label. (iii) Extraction of security-relevant entities with the provenance of each occurrence: account identifiers (such as IBAN-formatted strings), monetary amounts, password and credential values, user-profile values, and tool names mentioned in text. |
| Outputs | Labeled context $c_t$; extracted entities with provenance ($\text{Ent}_t$ in Algorithm 1); the held action $a_t$. |
| Relationship with next layer | Provides untrusted segments to Layer 2 and history, action and entities to Layer 3; both run in parallel on its output. |
| Security role | Preserves the distinction between data and instruction that indirect injection exploits; enables Layer 3 to test whether an argument of the proposed action can be traced to the user objective or trusted content, or only to untrusted content. |
| Implementation implications | Extraction patterns are declared in configuration and fixed before evaluation. Reliable attribution of context segments to their source channel is assumption AS-2 ("to be demonstrated"). The hygiene step reduces some encoding-based concealment but does not prevent paraphrase-based evasion. The provenance rule is a design definition and asserts no empirical claim. |

## 2.3 Layer 2: Detection Layer

Table: Table 8. Layer 2 — Detection

| Aspect | Description (Chapter 3, Section 3.5) |
|-------------------|---------------------------------------------------------------------------------|
| Purpose | Compute context evidence from untrusted segments. The layer issues no verdict. |
| Inputs | Untrusted segments of $c_t$ added since the previous step. |
| Processing | $x^{\text{ctx}}_1$: maximum score of a fixed, pre-trained prompt-injection classifier over untrusted segments added since the previous step (range [0, 1]). $x^{\text{ctx}}_2$: indicator (binary) that an untrusted segment added since the previous step matches the declared instruction-pattern set (imperative instructions addressed to an assistant, references to tool names, role or delimiter markers). |
| Outputs | Context evidence $x^{\text{ctx}} = (x^{\text{ctx}}_1, x^{\text{ctx}}_2)$. |
| Relationship with next layer | Passed to the Decision Engine, where it is combined with behavioral and action evidence. |
| Security role | Provides evidence about content arriving at the observation boundary TB-2 (security objective SO-1). |
| Implementation implications | The classifier is used with fixed inference and is not retrained. The classifier choice is pending supervisor approval; PromptGuard 2 in LlamaFirewall (Chennabasappa et al., 2025) is named as a candidate only. Both features are individually evadable and benchmark-based detector scores are fragile (Arp et al., 2022; M. Q. Li et al., 2026); the layer is therefore not relied upon to be decisive, and its contribution is measured by ablation. |

## 2.4 Layer 3: Behavioral Analysis Layer

Table: Table 9. Layer 3 — Behavioral Analysis

| Aspect | Description (Chapter 3, Section 3.6) |
|-------------------|---------------------------------------------------------------------------------|
| Purpose | Maintain the episode history and compute evidence about the trajectory and the proposed action. |
| Inputs | History $H_t$; proposed action $a_t$; Layer 1 entities; benign reference transition set; declared privilege map. |
| Processing | Step tracking: $H_t$ holds the sequence of proposed actions, their arguments with provenance, the verdicts issued and the tool results returned, and is reset at the start of each episode. Four behavioral features (post-observation shift, repeated calls, privilege escalation, transition deviation) and three action features (argument provenance, destination novelty, sensitive egress) are computed as defined in Chapter 3, Table 3.9. |
| Outputs | Behavioral evidence $x^{\text{beh}} = (x^{\text{beh}}_1, \ldots, x^{\text{beh}}_4)$; action evidence $x^{\text{act}} = (x^{\text{act}}_1, x^{\text{act}}_2, x^{\text{act}}_3)$. All features are bounded in [0, 1]. |
| Relationship with next layer | Passed to the Decision Engine. |
| Security role | Detects proposed actions whose arguments originate in untrusted content or that deviate from the episode's benign pattern (security objective SO-2). |
| Implementation implications | All reference quantities are estimated offline from benign data and frozen at runtime. No feature may encode a specific account identifier, because one attacker account identifier is shared by most injection tasks and a feature keyed on it would leak the label. Evidence about *whether* an action is induced is kept separate from consequence (*what would happen*), which enters only through the loss. The feature set is frozen after pilot E0, before held-out predictions are examined. |

Table: Table 10. Behavioral and action evidence (Chapter 3, Table 3.9)

| Feature | Definition | Type |
|-----------|-------------------------------------------------------------------------------|----------|
| $x^{\text{beh}}_1$ | Post-observation shift: 1 if the most recent tool result was untrusted and had $x^{\text{ctx}}_2 = 1$; otherwise 0 | Binary |
| $x^{\text{beh}}_2$ | Repeated calls: $\min(n_{\text{rep}}, n_{\text{max}}) / n_{\text{max}}$, where $n_{\text{rep}}$ is the number of consecutive calls with the same tool and key arguments and $n_{\text{max}}$ is declared | [0, 1] |
| $x^{\text{beh}}_3$ | Privilege escalation: 1 if the privilege level of $a_t$'s tool exceeds the highest level used so far in the episode; otherwise 0 | Binary |
| $x^{\text{beh}}_4$ | Transition deviation: 1 if the pair (previous tool, current tool) does not occur in the benign reference transition set; otherwise 0 | Binary |
| $x^{\text{act}}_1$ | Argument provenance: 1 if a key argument of $a_t$ (recipient account identifier, amount, password or profile value) occurs in untrusted content but not in $g$ or trusted content; otherwise 0 | Binary |
| $x^{\text{act}}_2$ | Destination novelty: 1 if the recipient of $a_t$ appears neither in $g$ nor among the transactions observed before the episode's first untrusted ingestion; otherwise 0 (value-transfer and payment-modification tools) | Binary |
| $x^{\text{act}}_3$ | Sensitive egress: 1 if $a_t$ sends to an external recipient a value obtained from a sensitive read (account identifier, profile value or credential); otherwise 0 | Binary |

## 2.5 Layer 4: Decision Engine Layer

Table: Table 11. Layer 4 — Decision Engine

| Aspect | Description (Chapter 3, Section 3.7) |
|-------------------|---------------------------------------------------------------------------------|
| Purpose | Turn evidence into a verdict in five stages — probability estimation, calibration, consequence assessment, policy predicates and expected-loss verdict selection — and write the audit record. |
| Inputs | Evidence vector $x_t = [x^{\text{ctx}}; x^{\text{beh}}; x^{\text{act}}]$; consequence descriptors $z_t$; frozen parameters; declared policy. |
| Processing | Logit and uncalibrated probability (Equation 3.1); calibrated probability (Equation 3.3); consequence tier $k_t = \kappa(z_t)$; predicates D1 (prohibited action → Block) and D2 (missing required evidence at tier $k_t \ge k_{\text{D2}}$ → Escalate); otherwise, conditional risk of each feasible verdict (Equation 3.6) and minimum-risk verdict (Equation 3.7); linear attribution for the audit record (Equations 3.11–3.13). |
| Outputs | Calibrated probability $p_t$, tier $k_t$, conditional risks $R_t(\cdot)$, verdict $v_t$ with its source (D1, D2 or the expected-loss rule), and the audit record. |
| Relationship with next layer | The verdict is passed to Layer 5, which executes the associated mechanism. |
| Security role | Accounts for the consequence of the proposed action when selecting a verdict (SO-3); provides human escalation as a response (SO-4); emits an audit record from which every verdict can be reproduced (SO-5). |
| Implementation implications | Parameters $\beta_0$, $\beta$, $\gamma_1$, $\gamma_0$ are learned offline and frozen; policy quantities are declared before evaluation. The attribution never influences the verdict. Details are given in Section 7. |

## 2.6 Layer 5: Mitigation Layer

Table: Table 12. Layer 5 — Mitigation

| Aspect | Description (Chapter 3, Section 3.8) |
|-------------------|---------------------------------------------------------------------------------|
| Purpose | Execute, deterministically, the mechanism associated with each verdict. The layer never initiates an action on the agent's behalf. |
| Inputs | Verdict $v_t$; proposed action $a_t$; episode restrictions $S$. |
| Processing | Allow → release; Modify → tool restriction; Escalate → withhold and refer to a human reviewer; Block → interrupt with safe fallback (Chapter 3, Table 3.14; see Section 7.5 of this document). Calls to tools already restricted in the episode are refused (Algorithm 1, line 29). |
| Outputs | Released, restricted, withheld or refused action; a structured notice or refusal returned to the agent where applicable. |
| Relationship with next step | A released action's tool result re-enters Layer 1 as untrusted content at step $t + 1$; the history $H_t$ is updated with the action and verdict. |
| Security role | Enforces the verdict at the action boundary TB-3. |
| Implementation implications | The set $\mathcal{T}_R$ of tools to which Modify applies is declared; in the banking environment it contains value-transfer, payment-modification, credential-change and profile-change tools, and read tools are not restricted. Mitigation effectiveness is measured, not assumed: $r_{\text{mod}}(k)$ is estimated from enforcing-mode runs. A restricted or blocked agent may retry; retries raise $x^{\text{beh}}_2$ and calls to restricted tools are refused. The episode-level restriction semantics conflict with the project design contract (Section 15.1). |

## 2.7 Cross-Cutting Offline Fitting and Recalibration (Not a Layer)

Offline fitting and recalibration are performed between deployments on logged data (Chapter 3, Section 3.9). They fit and freeze the benign reference quantities, the coefficients (Equation 3.2), the calibration parameters (Equation 3.4), the baseline thresholds (Equation 3.14) and the measured residual rates $r_{\text{mod}}(k)$, check the declared loss structure for dominated verdicts, and record all model, data, policy, benchmark and software versions. Runtime adaptation from observed traffic is excluded because it would allow an adversary who generates traffic to shift REM's reference behaviour. Between deployments, calibration can be monitored against later-established labels; if calibration drifts beyond a declared tolerance, the procedure is repeated on new data. This mechanism is the only feedback path in the design. It is a cross-cutting support activity, not a sixth layer, and no arrow connects it to the runtime path within an episode.

## 2.8 Stores and Architecture Figure Specification

Chapter 3 specifies Figure 3.1 textually, to be drawn with the listed elements and no others. The specification is reproduced below; no figure is drawn in this summary.

Table: Table 13. Specification of Figure 3.1 (Chapter 3, Section 3.2.2)

| Element | Content |
|------------------|----------------------------------------------------------------------------------|
| External elements | User and system inputs; tool outputs and retrieved content (untrusted); the agent (opaque); tools and environment; human reviewer |
| L1 | Capture and normalization; provenance labeling; entity extraction |
| L2 | Injection-classifier score; instruction-pattern indicator |
| L3 | History tracker; behavioral features; action features |
| L4 | Logistic estimation; calibration; consequence tier; policy predicates; expected-loss verdict with four outputs; audit record |
| L5 | Release; tool restriction; withhold and escalate; block with safe fallback |
| Stores (not layers) | Declared policy; frozen parameters; audit log |
| Cross-cutting box | Offline fitting and recalibration (dashed, outside the layer stack), connected to the audit log and the frozen parameters |
| Runtime arrows | L1 to L2 and L3 in parallel; L2 and L3 to L4; each verdict to its mechanism in L5; L5 to the environment or back to the agent. No arrow connects the offline box to the runtime path within an episode. |

# 3. End-to-End Operation

## 3.1 Execution Sequence

The per-step procedure is Algorithm 1 of Chapter 3 (Section 3.10). Every operation in it is defined in Chapter 3, Sections 3.4–3.8. Table 14 follows the algorithm's order.

Table: Table 14. End-to-end execution flow (Chapter 3, Algorithm 1)

| Stage | Input | Process | Output | Purpose | Security significance |
|------------------|-----------------|-------------------------|--------------|---------------------|----------------------------|
| 1. Input capture (L1; lines 1–4) | Objective $g$; new context segments with source channel; proposed action $a_t$ | Capture and hold $a_t$ at TB-3 | Held action; raw context | Ensure nothing is released before evaluation | The action boundary is the last point of prevention |
| 2. Context inspection (L1) | New untrusted segments | Remove invisible and formatting characters; label provenance with least-trusted inheritance; extract entities with provenance | $c_t$; $\text{Ent}_t$ | Establish the origin of every segment and value | Preserves the data–instruction distinction exploited by indirect injection |
| 3. Detection (L2; lines 5–6) | Untrusted segments since the previous step | Classifier score and instruction-pattern match | $x^{\text{ctx}}$ | Evidence about untrusted content | Observation-boundary evidence (SO-1); not decisive on its own |
| 4. Behavioral analysis (L3; lines 7–9) | $H_t$, $a_t$, $\text{Ent}_t$, $g$, benign transitions, privilege map | Compute four behavioral and three action features | $x^{\text{beh}}$, $x^{\text{act}}$ | Evidence about the trajectory and the action | Detects arguments traced only to untrusted content and deviations from benign patterns (SO-2) |
| 5. Evidence assembly (L4; line 11) | $x^{\text{ctx}}$, $x^{\text{beh}}$, $x^{\text{act}}$ | Concatenate; record which features are computable (avail) | $x_t$; avail | Single evidence vector for estimation | Missing evidence is tracked explicitly and used by predicate D2 |
| 6. Estimation and calibration (L4; lines 12–13) | $x_t$; frozen $\beta_0$, $\beta$, $\gamma_1$, $\gamma_0$ | Equations 3.1 and 3.3 | $s_t$, $\tilde{p}_t$, $p_t$ | Calibrated probability of adversarial induction | The decision rule treats $p_t$ as a probability |
| 7. Consequence assessment (L4; line 14) | Descriptors $z_t$ of $a_t$ | $k_t = \kappa(z_t)$ | Tier $k_t$ | Index the losses by consequence | Consequence enters only through the loss (SO-3) |
| 8. Policy predicates (L4; lines 15–18) | $a_t$, $\Pi$, avail, $k_t$, $k_{\text{D2}}$ | D1, then D2 | Verdict Block or Escalate, if a predicate applies | Deterministic overrides | A prohibition cannot be overridden by a low probability; absent evidence is not treated as evidence of safety |
| 9. Expected-loss verdict (L4; lines 19–23) | $p_t$, $k_t$, loss structure, feasible set | Equation 3.6 for each feasible verdict; Equation 3.7 with restrictive tie-breaking | $v_t$ ∈ {Allow, Modify, Escalate, Block}; source | Select the minimum-risk verdict | Consequence-dependent response |
| 10. Audit record (L4; lines 24–27) | $x_t$, $s_t$, $\tilde{p}_t$, $p_t$, $k_t$, $R$, $v_t$, source, parameters | Equations 3.11–3.13; identity check (Equation 3.12); append to log | Record $r_t$ | Reproducibility of every verdict (SO-5) | Audit operations do not affect the verdict |
| 11. Mitigation (L5; lines 28–33) | $v_t$, $a_t$, restrictions $S$ | Refuse if the tool is restricted; otherwise release, restrict, withhold and refer, or interrupt | Mitigated outcome; structured notice or refusal | Enforce the verdict | Enforcement at TB-3 |
| 12. History update (line 34) | $a_t$, $v_t$, tool result | Update $H_t$; released tool result enters Layer 1 at $t + 1$ | $H_{t+1}$ | Continuity of the episode | Tool results are treated as untrusted at the next step |

## 3.2 Continuation, Interruption and Safe Fallback

Under Allow, the action is released and the episode continues. Under Modify, the action is not executed, a structured notice is returned, and the agent may continue with its remaining tools. Under Escalate, the action is withheld and released only if the reviewer approves. Under Block, the action is not executed, a structured refusal is returned, and — as specified in Chapter 3 — every tool in $\mathcal{T}_R$ is restricted for the rest of the episode, so that read tools remain available while no further side-effecting action is released (Chapter 3, L639). The episode-level parts of these semantics are subject to the specification conflict described in Section 15.1.

## 3.3 Operating Modes

REM runs in two modes (Chapter 3, Section 3.11.1). In observe-only mode, verdicts are computed and logged but not enforced; fitting data are collected in this mode because enforced verdicts would alter the trajectories from which REM is fitted. In enforcing mode, verdicts are executed by the Mitigation Layer.

# 4. Algorithmic Design

This section identifies only the algorithms and methods that are present in Chapter 3. Thirteen methods are identified. Where Chapter 3 names an alternative only in order to state that it is not adopted (beta calibration, isotonic regression, input sanitization), this is recorded as such.

## 4.1 Provenance Labeling and Entity Extraction

Table: Table 15. Method 1 — Provenance labeling and entity extraction

| Aspect | Description |
|---------------------|-------------------------------------------------------------------------------|
| Definition | Each context segment receives one label from the ordered set trusted ≻ semi-trusted ≻ untrusted; derived content inherits the least-trusted label and is never promoted. Security-relevant entities are extracted with the provenance of each occurrence. |
| Role in REM | Layer 1; supplies provenance to the argument-provenance and sensitive-egress features. |
| Input | Context segments with their source channel; arguments of $a_t$. |
| Output | Labeled context $c_t$; entities with provenance. |
| Rationale | Preserves the distinction between data and instruction exploited by indirect injection (Chapter 3, Section 3.4.2). |
| Assumptions | AS-2: segments can be attributed to their source channel reliably (to be demonstrated). |
| Implementation requirements | Extraction patterns declared in configuration and fixed before evaluation. |
| Source | Design definition of Chapter 3; no literature source is claimed. |
| Verification status | DEF (design definition); "asserts no empirical claim" (Chapter 3). |

## 4.2 Context Evidence: Fixed Injection Classifier and Instruction-Pattern Indicator

Table: Table 16. Method 2 — Context evidence

| Aspect | Description |
|----------------------|------------------------------------------------------------------------------|
| Definition | $x^{\text{ctx}}_1$: maximum score of a fixed, pre-trained prompt-injection classifier over untrusted segments added since the previous step. $x^{\text{ctx}}_2$: binary indicator of a match with a declared instruction-pattern set. |
| Role in REM | Layer 2 (Detection). |
| Input | Untrusted segments added since the previous step. |
| Output | $x^{\text{ctx}} \in {[0,1]}^{2}$. |
| Rationale | Evidence about untrusted content entering through TB-2 (SO-1). |
| Assumptions | Neither feature is assumed decisive; both are individually evadable. |
| Implementation requirements | A fixed classifier with fixed inference, not retrained; an instruction-pattern set declared before evaluation. |
| Source | Candidate classifier: PromptGuard 2 in LlamaFirewall (Chennabasappa et al., 2025). The final choice is pending supervisor approval. |
| Verification status | Chennabasappa et al. (2025): VERIFIED at reference level (abstract). Classifier choice: SUPERVISOR DECISION REQUIRED. |

## 4.3 Behavioral and Action Features

Table: Table 17. Method 3 — Behavioral and action features

| Aspect | Description |
|-----------------------|-----------------------------------------------------------------------------|
| Definition | Seven features defined in Chapter 3, Table 3.9 (reproduced in Table 10). |
| Role in REM | Layer 3 (Behavioral Analysis). |
| Input | $H_t$, $a_t$, entities with provenance, $g$, benign reference transition set, privilege map, declared $n_{\text{max}}$. |
| Output | $x^{\text{beh}} \in {[0,1]}^{4}$, $x^{\text{act}} \in \{0,1\}^3$. |
| Rationale | Evidence about argument origin and deviation from benign behaviour (SO-2). |
| Assumptions | AS-7: observable evidence separates adversarially induced from benign proposed actions (tested in pilot E0). AS-8: benign reference data are representative (threatened by benchmark scope). |
| Implementation requirements | Reference quantities estimated on benign fitting data within each outer fold and frozen; no identity-based features; feature set frozen after pilot E0. |
| Source | Design definitions of Chapter 3. |
| Verification status | DEF. Empirical adequacy is to be tested (AS-7). |

## 4.4 Logistic Regression

Table: Table 18. Method 4 — Logistic regression

| Aspect | Description |
|------------------------|----------------------------------------------------------------------------|
| Definition | $s_t = \beta_0 + \beta^{\top} x_t$ and $\tilde{p}_t = \sigma(s_t)$ (Equation 3.1). |
| Role in REM | Layer 4, stage 1: maps the evidence of Layers 2 and 3 to a logit and an uncalibrated probability. |
| Input | Evidence vector $x_t \in {[0,1]}^{d}$; frozen $\beta_0$, $\beta$. |
| Output | Logit $s_t$; uncalibrated probability $\tilde{p}_t$. |
| Rationale | Provides a probability estimate of adversarial induction from the combined evidence groups (Chapter 3, Section 3.7.1). |
| Assumptions | The log-odds of adversarial induction are approximately linear in the evidence; no interaction terms are included by default. |
| Implementation requirements | Coefficients fitted offline (Method 5) and frozen. |
| Source | Cox (1958). |
| Verification status | Cox (1958): PARTIALLY VERIFIED (Crossref metadata; formulation not read). Chapter 3 code IV. SOURCE NOT FULLY VERIFIED (OI-12). |

## 4.5 Ridge (L2-Penalized) Estimation

Table: Table 19. Method 5 — Ridge-penalized logistic regression

| Aspect | Description |
|--------------------|--------------------------------------------------------------------------------|
| Definition | Maximization of the log-likelihood minus a quadratic penalty $\lambda \lVert \beta \rVert_2^2$ on the coefficients; the intercept is not penalized (Equation 3.2). |
| Role in REM | Offline fitting of the Layer 4 estimator. |
| Input | Labeled fitting steps $D_{\text{fit}}$; penalty strength $\lambda \ge 0$. |
| Output | Frozen estimates $\hat{\beta}_0$, $\hat{\beta}$. |
| Rationale | The evidence features are mostly binary and adversarial steps are scarce; if an indicator appears only in adversarial fitting steps, the unpenalized maximum-likelihood estimate does not exist as a finite value. The penalty keeps the estimates finite (Chapter 3, L327). |
| Assumptions | As for logistic regression. |
| Implementation requirements | $\lambda$ selected by grouped inner cross-validation on held-out log-loss. The mapping from library parameterization (inverse penalty strength) is to be documented from the library version used. The library itself is NOT SPECIFIED IN CURRENT CHAPTER 3. |
| Source | le Cessie & van Houwelingen (1992). |
| Verification status | PARTIALLY VERIFIED (Crossref record verified; formulation not read). Chapter 3 code IV (penalty constant pending). SOURCE NOT FULLY VERIFIED (OI-10). |

## 4.6 Logistic (Platt) Calibration on the Logit

Table: Table 20. Method 6 — Logistic calibration on the logit

| Aspect | Description |
|----------------------|------------------------------------------------------------------------------|
| Definition | $p_t = \sigma(\gamma_1 s_t + \gamma_0)$ with $\gamma_1 > 0$ (Equation 3.3), with parameters fitted by minimizing the negative log-likelihood on held-out logits (Equation 3.4). |
| Role in REM | Layer 4, stage 2: produces the calibrated probability used by the decision rule. |
| Input | Logit $s_t$; frozen $\gamma_1$, $\gamma_0$. Offline: out-of-fold logits from grouped cross-fitting. |
| Output | Calibrated probability $p_t$. |
| Rationale | The uncalibrated probability need not agree with observed frequencies; ridge shrinkage and class imbalance can distort it. Because the decision rule treats the probability as a probability, it is recalibrated (Chapter 3, Section 3.7.2). |
| Assumptions | A two-parameter logistic map on the logit is adequate; $\gamma_1 > 0$. Fitting on the model's own training logits would be close to degenerate, so out-of-fold logits are used. |
| Implementation requirements | If the fitted slope is not positive, calibration is rejected for that fit and the event is reported (Procedure 3.1, line 6). |
| Source | Platt (1999) as the method; Guo et al. (2017) for the two-parameter form and its fit; Kull et al. (2017) for the monotonicity condition. |
| Verification status | Guo: FV (full text read in Stage 1). Kull: FV (Section 2.2 and Proposition 1 read). Platt: NC; PARTIALLY VERIFIED; the 1999/2000 citation conflict is unresolved (OI-07). |
| Beta calibration and isotonic regression | Not adopted. Chapter 3 cites Kull et al. (2017) for the result that beta calibration with equal shape parameters equals logistic calibration applied to the log-odds of a score; since the log-odds of $\tilde{p}_t$ is $s_t$, Equation 3.3 is beta calibration with equal shape parameters applied to $\tilde{p}_t$. Full beta calibration adds a third parameter and isotonic regression is nonparametric; neither is adopted, given the limited calibration data. |

## 4.7 Consequence Tiering and Policy Predicates

Table: Table 21. Method 7 — Consequence tiering and policy predicates

| Aspect | Description |
|-------------------|---------------------------------------------------------------------------------|
| Definition | Descriptors $z_t$ of the action (category, amount, recurring-payment change, credential change, irreversibility) are mapped to a tier $k_t = \kappa(z_t) \in \{1, \ldots, K\}$ by a declared policy function. D1: if $a_t \in \Pi$, the verdict is Block. D2: if evidence required for tier $k_t$ cannot be computed and $k_t \ge k_{\text{D2}}$, the verdict is Escalate. |
| Role in REM | Layer 4, stages 3 and 4. |
| Input | $a_t$ and its descriptors; declared $\kappa$, amount limits, $\Pi$, $k_{\text{D2}}$, required evidence per tier; availability of features. |
| Output | Tier $k_t$; a predicate verdict where applicable, with the predicate named as the source in the audit record. |
| Rationale | Consequence is kept separate from evidence and enters the decision only through the loss. A prohibition that a sufficiently low probability could override would not be a prohibition; absent evidence is not treated as evidence of safety. |
| Assumptions | Irreversibility is declared per tool; the benchmark does not simulate settlement. |
| Implementation requirements | Tier policy (Chapter 3, Table 3.11) is illustrative and pending supervisor approval. The number of tiers $K$, the amount limits, $\Pi$ and $k_{\text{D2}}$ are declared policy; their values are NOT SPECIFIED IN CURRENT CHAPTER 3. |
| Source | Design definitions of Chapter 3. |
| Verification status | DEF. Tier policy: SUPERVISOR DECISION REQUIRED. |

## 4.8 Expected-Loss (Bayes) Verdict Selection

Table: Table 22. Method 8 — Expected-loss verdict selection over Allow, Modify, Escalate and Block

| Aspect | Description |
|-------------------|---------------------------------------------------------------------------------|
| Definition | For each feasible verdict, the conditional risk $R_t(v) = (1 - p_t) L(v, 0, k_t) + p_t L(v, 1, k_t)$ is computed (Equation 3.6); the verdict with minimum risk is selected, with ties resolved toward the more restrictive verdict (Equation 3.7). |
| Role in REM | Layer 4, stage 5. |
| Input | $p_t$; $k_t$; tier-indexed loss structure (Chapter 3, Table 3.13); feasible set $\mathcal{V}(a_t)$. |
| Output | Verdict $v_t$ and conditional risks $R_t(\cdot)$. |
| Rationale | Thresholds become consequences of declared costs rather than independently chosen constants (Equations 3.8–3.10). |
| Assumptions | $p_t$ is calibrated (the substitution of $p_t$ for the true posterior is justified only to that extent); assumption A-Mod for the Modify loss; a reviewer who resolves escalations correctly for the Escalate entries. |
| Implementation requirements | Declared loss structure checked for dominated verdicts before use; loss values declared before evaluation and varied over a declared grid. |
| Source | Elkan (2001), adapted; Chow (1970) as conceptual basis for escalation. Neither source is presented as the origin of the four-verdict architecture. |
| Verification status | Elkan: VERIFIED (author PDF; Eq. 1 read); printed threshold not inspected (OI-11). Chow: PARTIALLY VERIFIED; reject rule not read (OI-13). |

## 4.9 Linear Shapley Attribution (Audit Only)

Table: Table 23. Method 9 — Linear Shapley attribution

| Aspect | Description |
|----------------------|------------------------------------------------------------------------------|
| Definition | $\varphi_{t,i} = \beta_i (x_{t,i} - \overline{x}_i)$ with base value $\varphi_0 = \beta_0 + \beta^{\top}\overline{x}$ (Equation 3.11); group sums $\Phi_J$ (Equation 3.13). |
| Role in REM | Audit record only. The attribution never influences the verdict. |
| Input | $x_t$; frozen $\beta_0$, $\beta$; benign reference mean $\overline{x}$. |
| Output | Per-feature and per-group contributions to the logit. |
| Rationale | Makes each verdict's evidence contributions inspectable and reproducible (SO-5). |
| Assumptions | Feature independence affects the interpretation of each contribution as a Shapley value, not the identity of Equation 3.12. |
| Implementation requirements | The identity check (Equation 3.12) is applied at runtime as a correctness invariant with tolerance $\varepsilon$; the value of $\varepsilon$ is NOT SPECIFIED IN CURRENT CHAPTER 3. |
| Source | Lundberg & Lee (2017). |
| Verification status | FV (Properties 1–3, Theorem 1 and Corollary 1 read in Stage 1). Chapter 3 notes that the printed indices in the source do not match across the expression and that REM uses an index-consistent form. |

## 4.10 Deterministic Mitigation Mapping

Table: Table 24. Method 10 — Verdict-to-mitigation mapping

| Aspect | Description |
|-----------------------|-----------------------------------------------------------------------------|
| Definition | A fixed mapping from each verdict to one mechanism (Chapter 3, Table 3.14): release, tool restriction, withhold and refer, interrupt with safe fallback. |
| Role in REM | Layer 5. |
| Input | $v_t$, $a_t$, restrictions $S$. |
| Output | Mitigated outcome. |
| Rationale | Tool restriction is chosen as the single Modify mechanism because it is deterministic, does not depend on an LLM rewriting content, and can be measured. Input sanitization, such as spotlighting (Hines et al., 2024), is named as an alternative that is not adopted. |
| Assumptions | Mitigation effectiveness is measured, not assumed. |
| Implementation requirements | Declared $\mathcal{T}_R$; restriction state per episode. |
| Source | Design definition of Chapter 3. |
| Verification status | DEF. The episode-level restriction semantics conflict with the project design contract: SUPERVISOR DECISION REQUIRED (Section 15.1). |

## 4.11 Consequence-Independent Baseline Threshold Policy (Baseline Only)

Table: Table 25. Method 11 — Baseline operating-point threshold policy

| Aspect | Description |
|-------------------------|---------------------------------------------------------------------------|
| Definition | Thresholds $\theta(\alpha)$ selected on benign validation steps at declared false-positive targets (Equation 3.14); Block if $p_t \ge \theta(\alpha_{\text{blk}})$, Modify if $\theta(\alpha_{\text{mod}}) \le p_t < \theta(\alpha_{\text{blk}})$ and Modify is feasible (otherwise Block), Allow otherwise, with $\alpha_{\text{mod}} > \alpha_{\text{blk}}$. |
| Role in REM | Comparator B1 only; it is not a second primary method. |
| Input | $p_t$; out-of-fold calibrated benign steps. |
| Output | Baseline verdict; Escalate only through predicate D2. |
| Rationale | Isolates the effect of the decision rule by using the same estimator and calibration. |
| Assumptions | None beyond those of the estimator. |
| Implementation requirements | Targets $\alpha_{\text{blk}}$, $\alpha_{\text{mod}}$ declared before held-out predictions are examined. |
| Source | Design definition of Chapter 3. |
| Verification status | DEF. |

## 4.12 Nested Grouped Cross-Fitting and Group Bootstrap

Table: Table 26. Method 12 — Estimation protocol

| Aspect | Description |
|-------------------|---------------------------------------------------------------------------------|
| Definition | Outer folds: attacked episodes grouped by injection task (nine leave-one-injection-task-out folds); benign-only episodes assigned by user task. Inner grouped cross-validation selects $\lambda$ and produces out-of-fold logits for calibration and thresholds. Confidence intervals by bootstrap resampling of injection-task and user-task groups. |
| Role in REM | Evaluation and offline fitting (cross-cutting). |
| Input | Logged observe-only traces with labels. |
| Output | Held-out predictions for all reported metrics; intervals. |
| Rationale | Positive-step scarcity, a shared attacker account identifier, repeated task templates, short trajectories and scarce calibration data make four independent partitions unsupportable (Chapter 3, Section 3.11.4). |
| Assumptions | Grouping by injection task does not remove dependence on shared user-task templates; a sensitivity analysis grouped by user task is pending supervisor approval. |
| Implementation requirements | No step is scored by a model fitted on its own group; the deployment model is used only for demonstrations and latency. |
| Source | Efron (1979) for the bootstrap; grouping scheme is a design choice. |
| Verification status | Efron: PARTIALLY VERIFIED (Crossref metadata only). |

## 4.13 Optional Observe-Only Sequential Change Detection

Table: Table 27. Method 13 — Optional CUSUM analysis

| Aspect | Description |
|-------------------|---------------------------------------------------------------------------------|
| Definition | A Bernoulli cumulative sum statistic on a per-step deviation indicator $e_t$ (Equations 3.15–3.19). |
| Role in REM | Not part of REM's verdict path. Performed offline on logged indicators, and only if the supervisor approves it for the thesis narrative. It never influences a verdict. |
| Input | $e_t$ derived from logged behavioral and action indicators (indicator set pending supervisor approval); $q_0$, $q_1$, $h_G$. |
| Output | Statistic $G_t$, alarm time $T_A$, false-alarm rate and detection delay. |
| Rationale | Sequential change detection has known optimality properties (Lorden, 1971; Moustakides, 1986), but these are proved under conditions that could not be inspected and are not claimed to hold for agent trajectories. |
| Assumptions | $0 < q_0 < q_1 < 1$; $q_1$ is declared and reported over a range. Given short trajectories, the analysis may have little to detect. |
| Implementation requirements | Offline only. |
| Source | Page (1954); Basseville & Nikiforov (1993); Reynolds & Stoumbos (1999); Lorden (1971); Moustakides (1986). |
| Verification status | Basseville & Nikiforov: FV. Page: IV. Reynolds & Stoumbos: IV (not read). Lorden and Moustakides: PARTIALLY VERIFIED (abstracts only; assumptions not read). Inclusion: SUPERVISOR DECISION REQUIRED. |

# 5. Mathematical Formulation

## 5.1 Scope of the Extraction

Chapter 3 contains 22 numbered equations (3.1–3.22) and 15 unnumbered mathematical expressions. All are reproduced below without correction or rewriting; only the typesetting differs from the working file. Equation numbers are those of Chapter 3. For each equation the Chapter 3 status (Established, Adapted, Derived, Definition) is given together with the classification requested for this summary:

- **Directly sourced from literature** — Chapter 3 status "Established";
- **Adapted from literature** — Chapter 3 status "Adapted";
- **Derived from cited literature** — Chapter 3 status "Derived" from sourced equations;
- **Implementation notation** — design definitions used to compute quantities at runtime or offline;
- **Conceptual notation** — design definitions used to define evaluation quantities.

Evidence locations are those recorded in the Stage 1 equation-source audit and the Stage 2 resolution report. Where an attribution has not been confirmed against the source text, the entry states SOURCE NOT FULLY VERIFIED.

## 5.2 Probability Estimation

### Equation 3.1 — Logistic model

$$ s_{t} = \beta_{0} + \beta^{\top} x_{t}, \qquad \tilde{p}_{t} = \sigma(s_{t}) = 1 / (1 + \exp(-s_{t})) \qquad\qquad (3.1) $$

Table: Table 28. Equation 3.1

| Field | Content |
|-----------------------------|-----------------------------------------------------------------------|
| Purpose | Map the evidence to a logit and an uncalibrated probability. |
| Variables and meaning | $s_t$: logit (linear predictor); $\beta_0 \in \mathbb{R}$: intercept; $\beta \in \mathbb{R}^d$: coefficient vector; $x_t \in {[0,1]}^{d}$: evidence vector $[x^{\text{ctx}}; x^{\text{beh}}; x^{\text{act}}]$; $\tilde{p}_t$: uncalibrated estimate of $P(y_t = 1 \mid x_t)$; $\sigma$: logistic function. |
| Input / Output | Input $x_t$ and frozen $\beta_0$, $\beta$; output $s_t$, $\tilde{p}_t$. |
| REM component | Layer 4, estimation (Chapter 3, Section 3.7.1). |
| Chapter 3 status / classification | Established from source / directly sourced from literature. |
| Academic source | Cox (1958). |
| Evidence location | Stage 1: "Paper not read; Crossref record only". Stage 2: bibliographic record matched against Crossref (JRSS Series B 20(2), 215–232). |
| Verification status | IV. SOURCE NOT FULLY VERIFIED (printed formulation not inspected; OI-12). |

### Equation 3.2 — Ridge-penalized log-likelihood

$$ (\hat{\beta}_{0}, \hat{\beta}) = \arg\max_{\beta_{0}, \beta} \sum_{i \in D_{\text{fit}}} \left[ y_{i} \ln \tilde{p}_{i} + (1 - y_{i}) \ln(1 - \tilde{p}_{i}) \right] - \lambda \lVert \beta \rVert^{2}_{2} \qquad\qquad (3.2) $$

Table: Table 29. Equation 3.2

| Field | Content |
|-----------------------|-----------------------------------------------------------------------------|
| Purpose | Offline estimation of the intercept and coefficients with a quadratic penalty. |
| Variables and meaning | $D_{\text{fit}}$: set of labeled fitting steps; $y_i \in \{0,1\}$: labels; $\tilde{p}_i$: given by Equation 3.1; $\lambda \ge 0$: strength of the quadratic penalty; $\lVert \beta \rVert_2^2$: squared Euclidean norm of the coefficients. The intercept is not penalized. |
| Input / Output | Input: labeled fitting steps and $\lambda$ (selected by grouped cross-validation on held-out log-loss). Output: $\hat{\beta}_0$, $\hat{\beta}$, frozen. |
| REM component | Offline fitting (cross-cutting) for Layer 4. |
| Chapter 3 status / classification | Established from source / directly sourced from literature. |
| Academic source | le Cessie & van Houwelingen (1992). |
| Evidence location | Stage 1: "Paper not read; Crossref record only". Chapter 3 (L329): the exact scaling constant of the penalty is pending full-text verification; rescaling the penalty by a positive constant changes the selected $\lambda$, not the set of attainable solutions. Stage 2: Crossref record verified; the reasoning on rescaling was checked and found correct. |
| Verification status | IV (penalty constant pending). SOURCE NOT FULLY VERIFIED (OI-10). |

## 5.3 Calibration

### Equation 3.3 — Logistic calibration on the logit

$$ p_{t} = \sigma(\gamma_{1} s_{t} + \gamma_{0}), \qquad \gamma_{1} > 0 \qquad\qquad (3.3) $$

Table: Table 30. Equation 3.3

| Field | Content |
|------------------------|----------------------------------------------------------------------------|
| Purpose | Produce the calibrated probability used by the decision rule. |
| Variables and meaning | $p_t$: calibrated probability; $\gamma_1$: calibration slope (strictly positive so that the ranking of steps is preserved); $\gamma_0$: calibration intercept; $s_t$: logit from Equation 3.1. |
| Input / Output | Input $s_t$ and frozen $\gamma_1$, $\gamma_0$; output $p_t$. |
| REM component | Layer 4, calibration (Chapter 3, Section 3.7.2). |
| Chapter 3 status / classification | Adapted from source / adapted from literature. |
| Academic source | Platt (1999) — method; Guo et al. (2017) — two-parameter form fitted by negative log-likelihood on held-out data; Kull et al. (2017) — monotonicity condition (Kull et al. require a non-negative slope for a non-decreasing map; REM requires a strictly positive slope). |
| Evidence location | Guo: Section 4.1 read (Stage 1). Kull: Section 2.2 and Proposition 1 read (Stage 1). Platt: inaccessible (Stage 1). |
| Verification status | Platt NC; Guo FV; Kull FV. The form is verified; Platt's original parameterization is SOURCE NOT FULLY VERIFIED; the Platt 1999/2000 citation conflict is unresolved (OI-07). |

### Equation 3.4 — Calibration fitted by negative log-likelihood

$$ (\hat{\gamma}_{1}, \hat{\gamma}_{0}) = \arg\min_{\gamma_{1}, \gamma_{0}} - \sum_{i \in D_{\text{cal}}} \left[ y_{i} \ln p_{i} + (1 - y_{i}) \ln(1 - p_{i}) \right] \qquad\qquad (3.4) $$

Table: Table 31. Equation 3.4

| Field | Content |
|------------------------------|----------------------------------------------------------------------|
| Purpose | Fit the calibration parameters. |
| Variables and meaning | $D_{\text{cal}}$: a set of steps whose logits $s_i$ were produced by a model that was not fitted on those steps (out-of-fold logits from grouped cross-fitting); $p_i$: from Equation 3.3; $y_i$: labels. |
| Input / Output | Input: out-of-fold logits and labels. Output: $\hat{\gamma}_1$, $\hat{\gamma}_0$, frozen; if $\hat{\gamma}_1 \le 0$, calibration is rejected for that fit and the event is reported. |
| REM component | Offline fitting (cross-cutting). |
| Chapter 3 status / classification | Established from source / directly sourced from literature. |
| Academic source | Guo et al. (2017). |
| Evidence location | Stage 1: full text read (ar5iv rendering): calibration definition, ECE bins, Platt form, NLL fit. |
| Verification status | FV. |

## 5.4 Loss Structure and Verdict Selection

Chapter 3 declares the tier-indexed loss structure $L(v, y, k)$ in Table 3.13, reproduced as expression U-6 in Section 5.9. All declared costs are non-negative and expressed in common relative units; correct automatic decisions are assigned zero loss by declared convention.

### Equation 3.5 — Adversarial loss of Modify

$$ L(\text{Modify}, 1, k) = r_{\text{mod}}(k) \cdot C_{\text{miss}}(k) + (1 - r_{\text{mod}}(k)) \cdot 0 = r_{\text{mod}}(k) \cdot C_{\text{miss}}(k) \qquad\qquad (3.5) $$

Table: Table 32. Equation 3.5

| Field | Content |
|---------------------------|-------------------------------------------------------------------------|
| Purpose | Define the loss of Modify on an adversarially induced action. |
| Variables and meaning | $r_{\text{mod}}(k) \in [0,1]$: residual attack-success rate after Modify at tier $k$, measured in enforcing-mode runs; $C_{\text{miss}}(k)$: declared cost of a missed attack at tier $k$. |
| Input / Output | Input: measured $r_{\text{mod}}(k)$ and declared $C_{\text{miss}}(k)$. Output: the loss entry $L(\text{Modify}, 1, k)$. |
| REM component | Layer 4, loss structure; $r_{\text{mod}}(k)$ estimated offline. |
| Chapter 3 status / classification | Derived under assumption A-Mod / derived (from a stated assumption, by the law of total expectation). |
| Academic source | None; law of total expectation. |
| Evidence location | Chapter 3, Section 3.7.5. Assumption A-Mod: whether Modify neutralizes an adversarially induced action is independent of $x_t$ given the tier, and the attack fails with probability $1 - r_{\text{mod}}(k)$. |
| Verification status | DER. Assumption A-Mod is not empirically validated. |

### Equation 3.6 — Conditional risk

$$ R_{t}(v) = (1 - p_{t}) \cdot L(v, 0, k_{t}) + p_{t} \cdot L(v, 1, k_{t}), \qquad v \in \mathcal{V}(a_{t}) \qquad\qquad (3.6) $$

Table: Table 33. Equation 3.6

| Field | Content |
|---------------------------|-------------------------------------------------------------------------|
| Purpose | Compute the expected loss (conditional risk) of each feasible verdict. |
| Variables and meaning | $R_t(v)$: conditional risk of verdict $v$ at step $t$; $p_t$: calibrated probability; $L(v, y, k_t)$: declared loss of verdict $v$ for label $y$ at tier $k_t$; $\mathcal{V}(a_t)$: feasible verdicts for $a_t$. |
| Input / Output | Input $p_t$, $k_t$, loss structure; output $R_t(v)$ for every $v \in \mathcal{V}(a_t)$. |
| REM component | Layer 4, expected-loss verdict selection (Chapter 3, Section 3.7.5). |
| Chapter 3 status / classification | Adapted from source / adapted from literature. |
| Academic source | Elkan (2001). REM extends the choice set to four verdicts, indexes the losses by consequence tier, and substitutes the calibrated estimate $p_t$ for the true posterior; the substitution is justified only to the extent that $p_t$ is calibrated. |
| Evidence location | Stage 1: Elkan Eq. (1), read on page 1 of the author PDF. |
| Verification status | FV (Eq. 1 form). |

### Equation 3.7 — Bayes verdict with tie-breaking

$$ v_{t} = \arg\min_{v \in \mathcal{V}(a_{t})} R_{t}(v) \qquad\qquad (3.7) $$

Table: Table 34. Equation 3.7

| Field | Content |
|-------------------------------|---------------------------------------------------------------------|
| Purpose | Select the verdict with minimum conditional risk. |
| Variables and meaning | $v_t$: verdict issued at step $t$. Ties are resolved toward the more restrictive verdict in the declared order Block ⪰ Escalate ⪰ Modify ⪰ Allow. |
| Input / Output | Input $R_t(\cdot)$; output $v_t$. |
| REM component | Layer 4. |
| Chapter 3 status / classification | Adapted from source; the tie-breaking order is a design definition that makes the rule a function / adapted from literature. |
| Academic source | Elkan (2001); tie order defined by Chapter 3. |
| Evidence location | Stage 1: Elkan Eq. (1). |
| Verification status | FV; tie order DEF. The tie rule diverges from the project prototype, which raises an error on an exact tie (Section 15.1). |

### Equation 3.8 — Pairwise indifference threshold

$$ \pi_{v,v'}(k) = \Delta_{0} / (\Delta_{0} + \Delta_{1}) \qquad\qquad (3.8) $$

Table: Table 35. Equation 3.8

| Field | Content |
|------------------------------|----------------------------------------------------------------------|
| Purpose | Give the probability at which two verdicts have equal conditional risk. |
| Variables and meaning | For verdicts $v$ and $v'$ at tier $k$: $\Delta_0 = L(v', 0, k) - L(v, 0, k)$; $\Delta_1 = L(v, 1, k) - L(v', 1, k)$; $\Delta_0 + \Delta_1 > 0$. Below $\pi_{v,v'}(k)$, $v$ is preferred; above it, $v'$ is preferred. |
| Input / Output | Input: loss entries; output: threshold in probability units. |
| REM component | Layer 4 (analysis of the decision rule). |
| Chapter 3 status / classification | Derived from Equation 3.6 / derived from cited literature. |
| Academic source | Derived from Equation 3.6 (Elkan, 2001). |
| Evidence location | Chapter 3, Section 3.7.5, with derivation $R(v) - R(v') = -\Delta_0 + p(\Delta_0 + \Delta_1)$. Stage 2 re-derived the expression independently and confirmed it. |
| Verification status | DER (confirmed in Stage 2). |

### Equation 3.9 — Allow–Block threshold

$$ p^{\text{*}}_{k} = C_{\text{FA}}(k) / (C_{\text{FA}}(k) + C_{\text{miss}}(k)) \qquad\qquad (3.9) $$

Table: Table 36. Equation 3.9

| Field | Content |
|---------------------|-------------------------------------------------------------------------------|
| Purpose | Give the probability above which Block is preferred to Allow at tier $k$. |
| Variables and meaning | $p^{\text{*}}_{k}$: Allow–Block threshold; $C_{\text{FA}}(k)$: declared cost of a false intervention by Block; $C_{\text{miss}}(k)$: declared cost of a missed attack. For $v$ = Allow and $v'$ = Block, $\Delta_0 = C_{\text{FA}}(k)$ and $\Delta_1 = C_{\text{miss}}(k)$. |
| Input / Output | Input: declared costs; output: threshold. |
| REM component | Layer 4 (analysis); also used for reliability reporting in windows around each tier's threshold (Chapter 3, Section 3.12.2). |
| Chapter 3 status / classification | Derived from Equation 3.8 / derived from cited literature. |
| Academic source | Derived from Equation 3.8. Chapter 3 states that it has the form of the standard two-class cost-sensitive threshold for zero-cost correct decisions, which Elkan (2001) obtains from the same expected-cost criterion, and that the printed threshold expression in that paper could not be inspected, so the derivation stands on Equation 3.8 alone. |
| Evidence location | Stage 1: "Elkan's printed threshold equation not extracted" (PARTIALLY VERIFIED). Stage 2: derivation re-checked independently and confirmed (VERIFIED as a derivation). |
| Verification status | DER. The attribution of the printed form to Elkan (2001) is SOURCE NOT FULLY VERIFIED (OI-11). |

### Equation 3.10 — Escalation feasibility condition

$$ C_{\text{esc}} < C_{\text{FA}}(k) \cdot C_{\text{miss}}(k) / (C_{\text{FA}}(k) + C_{\text{miss}}(k)) \qquad\qquad (3.10) $$

Table: Table 37. Equation 3.10

| Field | Content |
|-----------------------|-----------------------------------------------------------------------------|
| Purpose | State when Escalate can be selected for some probability, for the verdict set {Allow, Escalate, Block} at tier $k$. |
| Variables and meaning | $C_{\text{esc}}$: declared cost of escalation; $C_{\text{FA}}(k)$, $C_{\text{miss}}(k)$ as above. $R(\text{Allow}) = p \cdot C_{\text{miss}}(k)$ increases and $R(\text{Block}) = (1 - p) \cdot C_{\text{FA}}(k)$ decreases in $p$; their minimum is largest at $p^{\text{*}}_{k}$. At equality, ties resolve toward Block. When Modify is also feasible, the condition remains necessary. |
| Input / Output | Input: declared costs; output: a feasibility condition on the loss declaration. |
| REM component | Layer 4 (analysis; used in the dominance check of declared loss structures). |
| Chapter 3 status / classification | Derived from Equations 3.6, 3.7 and 3.9; Chow (1970) as conceptual basis / derived from cited literature. |
| Academic source | Derived; Chow (1970) provides the conceptual basis for withholding an automatic decision. The formula is not attributed to Chow. |
| Evidence location | Chapter 3, Section 3.7.5, with derivation. Stage 1: Chow not read. Stage 2: re-derived and confirmed. |
| Verification status | DER; Chow IV. Content of Chow (1970) SOURCE NOT FULLY VERIFIED (OI-13). |

## 5.5 Attribution

### Equation 3.11 — Linear attribution

$$ \varphi_{t,i} = \beta_{i} (x_{t,i} - \overline{x}_{i}), \; i = 1, \ldots, d; \qquad \varphi_{0} = \beta_{0} + \beta^{\top} \overline{x} \qquad\qquad (3.11) $$

Table: Table 38. Equation 3.11

| Field | Content |
|-------------------------|---------------------------------------------------------------------------|
| Purpose | Decompose the logit into per-feature contributions for the audit record. |
| Variables and meaning | $\overline{x}$: mean evidence vector over benign fitting steps; $\varphi_{t,i}$: contribution of feature $i$ to the logit relative to that benign reference; $\varphi_0$: logit at the reference. |
| Input / Output | Input $x_t$, $\beta_0$, $\beta$, $\overline{x}$; output $\varphi_0$, $\varphi_{t,i}$. |
| REM component | Layer 4, audit record (never influences the verdict). |
| Chapter 3 status / classification | Adapted from source / adapted from literature. |
| Academic source | Lundberg & Lee (2017). The source states the linear case under feature independence with printed indices that do not match between the two sides of the expression and with base value equal to the model intercept; REM uses the index-consistent form and sets the base value to the logit at the reference point, as required by the local-accuracy property when the reference mean is not zero. |
| Evidence location | Stage 1: Corollary 1 and Property 1 read (ar5iv full text). |
| Verification status | FV. |

### Equation 3.12 — Completeness identity

$$ \varphi_{0} + \sum_{i=1}^{d} \varphi_{t,i} = s_{t} \qquad\qquad (3.12) $$

Table: Table 39. Equation 3.12

| Field | Content |
|---------------------------------|-------------------------------------------------------------------|
| Purpose | Guarantee that the attribution decomposes the logit exactly; checked as a runtime correctness invariant. |
| Variables and meaning | As in Equations 3.1 and 3.11. Summing Equation 3.11 gives $\beta_0 + \beta^{\top}\overline{x} + \beta^{\top}x_t - \beta^{\top}\overline{x} = s_t$. |
| Input / Output | Input: $\varphi_0$, $\varphi_{t,i}$, $s_t$; output: pass or fail of the identity check (Algorithm 1, line 25). |
| REM component | Layer 4, audit record. |
| Chapter 3 status / classification | Derived; local-accuracy property of Lundberg & Lee (2017) / derived from cited literature. |
| Academic source | Lundberg & Lee (2017). |
| Evidence location | Stage 1: Property 1 read. |
| Verification status | FV + DER. |

### Equation 3.13 — Group attribution

$$ \Phi_{J} = \sum_{i \in I_{J}} \varphi_{t,i}, \qquad J \in \{\text{ctx}, \text{beh}, \text{act}\} \qquad\qquad (3.13) $$

Table: Table 40. Equation 3.13

| Field | Content |
|--------------------------------------|--------------------------------------------------------------|
| Purpose | Report attribution by evidence group. |
| Variables and meaning | $I_J$: index set of evidence group $J$; $\Phi_J$: group contribution. Because the groups partition the features, $\Phi_{\text{ctx}} + \Phi_{\text{beh}} + \Phi_{\text{act}} = s_t - \varphi_0$. |
| Input / Output | Input $\varphi_{t,i}$; output $\Phi_{\text{ctx}}$, $\Phi_{\text{beh}}$, $\Phi_{\text{act}}$. |
| REM component | Layer 4, audit record. |
| Chapter 3 status / classification | Design definition / implementation notation. |
| Academic source | None. |
| Evidence location | Chapter 3, Section 3.7.6. |
| Verification status | DEF. |

## 5.6 Baseline Threshold

### Equation 3.14 — Baseline operating-point threshold

$$ \theta(\alpha) = \min \{ \theta : \text{FPR}_{\text{val}}(\theta) \le \alpha \}, \qquad \text{FPR}_{\text{val}}(\theta) = \left\vert \{ i \in D_{\text{val}}^{\text{benign}} : p_{i} \ge \theta \} \right\vert \, / \, \left\vert D_{\text{val}}^{\text{benign}} \right\vert \qquad\qquad (3.14) $$

Table: Table 41. Equation 3.14

| Field | Content |
|--------------------------|--------------------------------------------------------------------------|
| Purpose | Select the thresholds of the consequence-independent baseline B1 at declared false-positive targets. |
| Variables and meaning | $\alpha$: declared false-positive target; $D_{\text{val}}^{\text{benign}}$: benign validation steps in the relevant cross-fitting fold; $\theta$: ranges over the observed probabilities; $\text{FPR}_{\text{val}}(\theta)$: fraction of benign validation steps with $p_i \ge \theta$. |
| Input / Output | Input: out-of-fold calibrated benign probabilities; output: $\theta(\alpha_{\text{blk}})$ and $\theta(\alpha_{\text{mod}})$. |
| REM component | Baseline B1 only (comparator; not part of REM's decision rule). |
| Chapter 3 status / classification | Design definition / implementation notation. |
| Academic source | None. |
| Evidence location | Chapter 3, Section 3.7.7. Because the thresholds are selected by ranking, a strictly increasing recalibration leaves the baseline's verdicts unchanged, whereas cost-derived thresholds such as Equation 3.9 are fixed in probability units and can change after recalibration. |
| Verification status | DEF. |

## 5.7 Optional Sequential Analysis (Observe-Only, Not in the Verdict Path)

### Equation 3.15 — Bernoulli log-likelihood ratio

$$ \ell_{t} = e_{t} \ln(q_{1} / q_{0}) + (1 - e_{t}) \ln((1 - q_{1}) / (1 - q_{0})) \qquad\qquad (3.15) $$

Table: Table 42. Equation 3.15

| Field | Content |
|--------------------------|--------------------------------------------------------------------------|
| Purpose | Log-likelihood ratio of one Bernoulli observation of the deviation indicator. |
| Variables and meaning | $e_t \in \{0, 1\}$: deviation indicator (1 if at least one of $x^{\text{beh}}_1$, $x^{\text{beh}}_3$, $x^{\text{beh}}_4$ or $x^{\text{act}}_1$ equals 1, or if $x^{\text{beh}}_2 = 1$; indicator set pending supervisor approval); $q_0$, $q_1$ with $0 < q_0 < q_1 < 1$: rates of $e_t = 1$ before and after an adversarial change. |
| Input / Output | Input $e_t$, $q_0$, $q_1$; output $\ell_t$. |
| REM component | Optional offline analysis; never influences a verdict. |
| Chapter 3 status / classification | Derived by substituting the Bernoulli probability mass function into the log-likelihood ratio / derived from cited literature. |
| Academic source | Basseville & Nikiforov (1993); Reynolds & Stoumbos (1999) for the Bernoulli cumulative sum chart. |
| Evidence location | Stage 1: Basseville & Nikiforov Eq. 2.1.2 (book text read); Reynolds & Stoumbos not read. |
| Verification status | FV (general form); Reynolds & Stoumbos IV. The Bernoulli reference is SOURCE NOT FULLY VERIFIED. |

### Equation 3.16 — CUSUM recursion

$$ G_{t} = \max(0, G_{t-1} + \ell_{t}), \qquad G_{0} = 0 \qquad\qquad (3.16) $$

Table: Table 43. Equation 3.16

| Field | Content |
|---------------------------------|-------------------------------------------------------------------|
| Purpose | Cumulative sum statistic with reset at zero. |
| Variables and meaning | $G_t$: cumulative sum statistic at step $t$; $\ell_t$: from Equation 3.15. |
| Input / Output | Input $\ell_t$, $G_{t-1}$; output $G_t$. |
| REM component | Optional offline analysis. |
| Chapter 3 status / classification | Established from source / directly sourced from literature. |
| Academic source | Basseville & Nikiforov (1993); Page (1954). |
| Evidence location | Stage 1: Basseville & Nikiforov Eqs. 2.2.8–2.2.9 (book text read); Page (1954): Crossref metadata only. |
| Verification status | FV; Page IV. The attribution to Page (1954) is SOURCE NOT FULLY VERIFIED. |

### Equation 3.17 — Alarm time

$$ T_{A} = \min \{ t : G_{t} \ge h_{G} \} \qquad\qquad (3.17) $$

Table: Table 44. Equation 3.17

| Field | Content |
|-----------------------------------|-----------------------------------------------------------------|
| Purpose | First step at which the statistic reaches the alarm threshold. |
| Variables and meaning | $T_A$: alarm time; $h_G > 0$: alarm threshold, chosen as the smallest value for which Equation 3.18 does not exceed a declared target. |
| Input / Output | Input $G_t$, $h_G$; output $T_A$. |
| REM component | Optional offline analysis. |
| Chapter 3 status / classification | Established from source / directly sourced from literature. |
| Academic source | Basseville & Nikiforov (1993). |
| Evidence location | Stage 1: Eq. 2.2.10 (book text read). |
| Verification status | FV. |

### Equation 3.18 — Per-episode false-alarm rate

$$ \text{FA}_{\text{ep}}(h_{G}) = \left\vert \{ j \in E_{\text{ben}} : \max_{t} G^{(j)}_{t} \ge h_{G} \} \right\vert \, / \, \left\vert E_{\text{ben}} \right\vert \qquad\qquad (3.18) $$

Table: Table 45. Equation 3.18

| Field | Content |
|-------------------------------------|---------------------------------------------------------------|
| Purpose | Empirical fraction of benign episodes that raise an alarm. |
| Variables and meaning | $E_{\text{ben}}$: benign episodes in the fitting portion of a fold; $G^{(j)}_t$: statistic in benign episode $j$. |
| Input / Output | Input: statistics over benign episodes and $h_G$; output: false-alarm rate. |
| REM component | Optional offline analysis. |
| Chapter 3 status / classification | Design definition / conceptual notation. |
| Academic source | None. |
| Evidence location | Chapter 3, Section 3.11.10. |
| Verification status | DEF. |

### Equation 3.19 — Detection delay

$$ \tau_{d} = T_{A} - \nu, \qquad T_{A} \ge \nu \qquad\qquad (3.19) $$

Table: Table 46. Equation 3.19

| Field | Content |
|---------------------------------------|-------------------------------------------------------------|
| Purpose | Delay between the entry of injected content and the alarm. |
| Variables and meaning | $\tau_d$: detection delay; $\nu$: first step at which injected content enters the context. |
| Input / Output | Input $T_A$, $\nu$; output $\tau_d$. |
| REM component | Optional offline analysis. |
| Chapter 3 status / classification | Design definition / conceptual notation. |
| Academic source | None. |
| Evidence location | Chapter 3, Section 3.11.10. |
| Verification status | DEF. |

## 5.8 Evaluation Measures

### Equation 3.20 — Expected calibration error

$$ \text{ECE} = \sum_{m=1}^{M} (\left\vert B_{m} \right\vert / N) \cdot \left\vert \overline{y}(B_{m}) - \overline{p}(B_{m}) \right\vert, \qquad B_{m} = \{ i : (m - 1)/M < p_{i} \le m/M \} \qquad\qquad (3.20) $$

Table: Table 47. Equation 3.20

| Field | Content |
|----------------------------|------------------------------------------------------------------------|
| Purpose | Measure calibration error of held-out calibrated probabilities. |
| Variables and meaning | $N$: number of held-out steps; $M$: number of equal-width bins, declared in advance; $B_m$: bin $m$ (steps with $p_i = 0$ are assigned to the first bin); $\overline{y}(B_m)$: fraction of positive steps in bin $m$; $\overline{p}(B_m)$: mean calibrated probability in bin $m$. |
| Input / Output | Input: held-out $p_i$, $y_i$; output: ECE. |
| REM component | Evaluation (Chapter 3, Section 3.12.2). Reliability is also reported within declared windows around each tier's threshold $p^{\text{*}}_{k}$. |
| Chapter 3 status / classification | Adapted from source / adapted from literature. |
| Academic source | Naeini et al. (2015) for the binary form; Guo et al. (2017) for equal-width binning. |
| Evidence location | Stage 1: both read in full text (Naeini: PMC full text; Guo: ar5iv). |
| Verification status | FV. |

### Equation 3.21 — Log-loss

$$ \text{LL} = -(1/N) \sum_{i=1}^{N} \left[ y_{i} \ln p_{i} + (1 - y_{i}) \ln(1 - p_{i}) \right] \qquad\qquad (3.21) $$

Table: Table 48. Equation 3.21

| Field | Content |
|------------------------------|----------------------------------------------------------------------|
| Purpose | Proper scoring measure of held-out calibrated probabilities. |
| Variables and meaning | $N$: number of held-out steps; $y_i$: labels; $p_i$: calibrated probabilities, bounded away from 0 and 1 by a declared small constant for numerical evaluation (value NOT SPECIFIED IN CURRENT CHAPTER 3). |
| Input / Output | Input: held-out $p_i$, $y_i$; output: log-loss. |
| REM component | Evaluation; also the criterion for selecting $\lambda$. |
| Chapter 3 status / classification | Derived as the negated, averaged, unpenalized log-likelihood term of Equation 3.2 evaluated at calibrated probabilities / derived from cited literature. |
| Academic source | Derived from Equation 3.2. |
| Evidence location | Chapter 3, Section 3.12.2. |
| Verification status | DER. |

### Equation 3.22 — Realized loss

$$ \overline{L}(L_{e}) = (1/N) \sum_{i=1}^{N} L_{e}(v_{i}, y_{i}, k_{i}) \qquad\qquad (3.22) $$

Table: Table 49. Equation 3.22

| Field | Content |
|-----------------------------|-----------------------------------------------------------------------|
| Purpose | Average loss of issued verdicts under an evaluation loss structure. |
| Variables and meaning | $L_e$: evaluation loss structure; $v_i$: verdict issued for held-out step $i$ under the decision loss structure $L_d$; $y_i$: label; $k_i$: tier. |
| Input / Output | Input: held-out verdicts, labels, tiers and $L_e$; output: realized loss. |
| REM component | Evaluation (secondary metric; Chapter 3, Section 3.12.3). A rule that minimizes expected loss under $L$ is favoured by construction when evaluated under the same $L$; the grid therefore reports matched ($L_d = L_e$) and misspecified ($L_d \ne L_e$) costs and the baseline B1. |
| Chapter 3 status / classification | Design definition / conceptual notation. |
| Academic source | None. |
| Evidence location | Chapter 3, Section 3.12.3. |
| Verification status | DEF. |

## 5.9 Unnumbered Mathematical Expressions

Chapter 3 also contains the following unnumbered expressions. They are reproduced without alteration.

Table: Table 50. Unnumbered mathematical expressions in Chapter 3

| ID | Expression | Location in Chapter 3 | Role | Classification |
|---|----------------------------------------|-------------|-----------------------|-------------------|
| U-1 | $\sigma(u) = 1 / (1 + \exp(-u))$ | Table 3.4 | Logistic function | Conceptual notation |
| U-2 | $y_t \in \{0,1\}$; $x_t \in {[0,1]}^{d}$ with groups $x^{\text{ctx}}$, $x^{\text{beh}}$, $x^{\text{act}}$ and index sets $I_{\text{ctx}}$, $I_{\text{beh}}$, $I_{\text{act}}$ | Table 3.4 | Label and evidence vector | Conceptual notation |
| U-3 | $x^{\text{beh}}_2 = \min(n_{\text{rep}}, n_{\text{max}}) / n_{\text{max}}$ | Table 3.9 | Repeated-call feature | Implementation notation |
| U-4 | $k_t = \kappa(z_t) \in \{1, \ldots, K\}$ | Section 3.7.3 | Consequence tier mapping | Implementation notation (declared policy) |
| U-5 | D1: $a_t \in \Pi \Rightarrow v_t = \text{Block}$; D2: required evidence unavailable and $k_t \ge k_{\text{D2}} \Rightarrow v_t = \text{Escalate}$ | Section 3.7.4 | Policy predicates | Implementation notation |
| U-6 | Loss structure: Allow $(0, C_{\text{miss}}(k))$; Modify $(C_{\text{mod}}(k), r_{\text{mod}}(k) \cdot C_{\text{miss}}(k))$; Escalate $(C_{\text{esc}}, C_{\text{esc}})$; Block $(C_{\text{FA}}(k), 0)$, each pair giving $(L(v,0,k), L(v,1,k))$ | Table 3.13 | Declared tier-indexed losses | Conceptual notation (declared convention) |
| U-7 | $\mathcal{V}(a_t) = \{\text{Allow}, \text{Escalate}, \text{Block}\} \cup \{\text{Modify}\}$ if the tool of $a_t$ is in $\mathcal{T}_R$ | Section 3.7.5; Algorithm 1, line 20 | Feasible verdict set | Implementation notation |
| U-8 | Block ⪰ Escalate ⪰ Modify ⪰ Allow | Section 3.7.5 | Tie-breaking order | Implementation notation (design definition) |
| U-9 | $R(v) - R(v') = -\Delta_0 + p(\Delta_0 + \Delta_1)$ | Section 3.7.5 | Derivation of Equation 3.8 | Derived |
| U-10 | $C_{\text{FA}}(k) = C_{\text{miss}}(k) = C \Rightarrow C_{\text{esc}} < C/2$ | Section 3.7.5 | Symmetric special case of Equation 3.10 | Derived |
| U-11 | $R(\text{Modify}) - R(\text{Block}) = (1 - p)(C_{\text{mod}}(k) - C_{\text{FA}}(k)) + p \cdot r_{\text{mod}}(k) \cdot C_{\text{miss}}(k)$ | Section 3.7.5 | Dominance check: non-negative for every $p$ whenever $C_{\text{mod}}(k) \ge C_{\text{FA}}(k)$ | Derived |
| U-12 | $\Phi_{\text{ctx}} + \Phi_{\text{beh}} + \Phi_{\text{act}} = s_t - \varphi_0$ | Section 3.7.6 | Group partition identity | Derived |
| U-13 | Block if $p_t \ge \theta(\alpha_{\text{blk}})$; Modify if $\theta(\alpha_{\text{mod}}) \le p_t < \theta(\alpha_{\text{blk}})$ and feasible, otherwise Block; Allow otherwise; $\alpha_{\text{mod}} > \alpha_{\text{blk}}$ | Section 3.7.7 | Baseline verdict rule | Implementation notation |
| U-14 | $\left\vert \varphi_0 + \sum_i \varphi_{t,i} - s_t \right\vert < \varepsilon$ | Algorithm 1, line 25 | Runtime identity check ($\varepsilon$ NOT SPECIFIED IN CURRENT CHAPTER 3) | Implementation notation |
| U-15 | $e_t \in \{0,1\}$; $0 < q_0 < q_1 < 1$ | Section 3.11.10 | Deviation indicator and rates (optional analysis) | Conceptual notation |

# 6. Mathematical Justification

## 6.1 Separation of the Quantities

Chapter 3 keeps six kinds of quantity distinct, and the mathematical design depends on this separation. Evidence determines the probability; consequence determines the loss; the verdict is determined only by combining the two through expected loss.

Table: Table 51. The chain from evidence to intervention

| Stage | Quantity | Equation | Nature (Chapter 3, Table 3.12) | Question answered |
|-----------------|-----------------|------------|-----------------------|-------------------------------|
| Probability estimation | $s_t$, $\tilde{p}_t$ | 3.1, 3.2 | Learned ($\beta_0$, $\beta$) | How strongly does the evidence indicate adversarial induction? |
| Calibration | $p_t$ | 3.3, 3.4 | Learned ($\gamma_1$, $\gamma_0$) | What probability of adversarial induction does the score correspond to? |
| Behavioral evidence | $x^{\text{beh}}$, $x^{\text{act}}$ (with $x^{\text{ctx}}$) | Table 3.9 | Derived features; reference quantities measured on benign data | What does the trajectory and the action indicate? (Enters only through $x_t$.) |
| Decision costs | $L(v, y, k)$; $C_{\text{miss}}(k)$, $C_{\text{FA}}(k)$, $C_{\text{mod}}(k)$, $C_{\text{esc}}$; $r_{\text{mod}}(k)$ | Table 3.13; 3.5 | Policy (declared costs); measured ($r_{\text{mod}}$) | What would each verdict cost if the action were legitimate or induced? |
| Expected loss | $R_t(v)$ | 3.6 | Computed | What is the expected cost of each verdict at this step? |
| Final intervention | $v_t$ | 3.7 (with D1, D2) | Computed; tie order declared | Which verdict is issued? |

Behavioral evidence is not a separate stage of the decision: it is part of the evidence vector $x_t$ and influences the verdict only through the probability. Consequence descriptors do not enter Equation 3.1; they affect the verdict only through the loss (Chapter 3, Section 3.7.3).

## 6.2 Why Logistic Regression Is Used

Chapter 3 uses logistic regression (Cox, 1958) to map the combined context, behavioral and action evidence to a logit and an uncalibrated probability of adversarial induction (Section 3.7.1). The model assumes that the log-odds of adversarial induction are approximately linear in the evidence, and no interaction terms are included by default. Two further properties of the linear logit are used elsewhere in the design: the calibration map is applied to the logit (Section 6.4), and the logit decomposes exactly into per-feature contributions for the audit record (Section 6.6). Chapter 3 does not present logistic regression as a contribution (Table 3.16).

## 6.3 Why Regularization Is Used

The evidence features are mostly binary and adversarial steps are scarce (Chapter 3, Section 3.11.4). If a single indicator appears only in adversarial fitting steps, the unpenalized maximum-likelihood estimate does not exist as a finite value; the quadratic penalty of Equation 3.2 keeps the estimates finite (L327). The intercept is not penalized. The penalty strength $\lambda$ is selected by grouped cross-validation on held-out log-loss, so the unverified scaling constant of the penalty in le Cessie and van Houwelingen (1992) changes the selected value of $\lambda$ but not the set of attainable solutions (L329). This argument was checked in Stage 2 and found correct; the constant itself remains SOURCE NOT FULLY VERIFIED (OI-10).

## 6.4 Why Calibration Is Required, and the Roles of NLL and ECE

The decision rule of Equation 3.6 treats $p_t$ as a probability. Ridge shrinkage and class imbalance can both distort the uncalibrated probability, so it is recalibrated with a two-parameter logistic map on the logit (Equation 3.3). Chapter 3 states four properties of this choice (Section 3.7.2):

1. **It changes probabilities, not rankings.** With $\gamma_1 > 0$, Equation 3.3 is strictly increasing in $s_t$, so ROC-AUC, PR-AUC and any decision based only on ordering are unchanged. A non-positive fitted slope causes calibration to be rejected for that fit and reported.
2. **It is the minimal adequate family** (Section 6.5).
3. **It is not a contribution.** Calibrated logistic risk scores are already used in agent safety (Hossain et al., 2026).
4. **It does not guarantee good control.** Recalibrating a scalar risk score can improve calibration error while leaving control regret under threshold routing unchanged (C. Zhang et al., 2026). REM therefore reports calibration quality and control outcomes separately and does not claim that calibration improves control.

Negative log-likelihood appears in three roles: as the fitting criterion for the calibration parameters on out-of-fold logits (Equation 3.4); as the held-out criterion for selecting $\lambda$; and, averaged over held-out steps, as log-loss (Equation 3.21), which serves as the proper scoring measure. Expected calibration error (Equation 3.20) measures calibration on the positive-class probability with equal-width bins; because a global ECE averages over all probabilities, reliability is also reported within declared windows around each tier's threshold $p^{\text{*}}_{k}$. The Brier score is not reported until the convention of its original source (Brier, 1950) has been confirmed (OI-09).

## 6.5 Beta Calibration: Role in the Argument (Not Adopted)

Beta calibration is not a component of REM. Chapter 3 refers to it only to justify the choice of logistic calibration on the logit. Kull et al. (2017) show that beta calibration with equal shape parameters equals logistic calibration applied to the log-odds of a score. Since $\tilde{p}_t = \sigma(s_t)$, the log-odds of $\tilde{p}_t$ is $s_t$, so Equation 3.3 is exactly beta calibration with equal shape parameters applied to $\tilde{p}_t$, and it includes the identity map ($\gamma_1 = 1$, $\gamma_0 = 0$). Full beta calibration adds a third parameter and isotonic regression is nonparametric; neither is adopted, given the limited calibration data (Chapter 3, Section 3.7.2). Stage 2 checked that this equivalence follows from the chapter's definitions. The design contract (`CLAUDE.md`) likewise excludes beta, isotonic and temperature calibration as the adopted calibrator. The claim-to-paper map records that the specific statement that Kull et al. "prove" the equivalence (L355) has no claim-level audit record.

## 6.6 Role of Shapley Attribution

The audit record contains a linear attribution of the logit (Equation 3.11), following the linear case of Shapley-value attribution given by Lundberg and Lee (2017). Its decomposition is exact (Equation 3.12, the local-accuracy property), and REM checks the identity as a correctness invariant. Four qualifications apply (Chapter 3, Section 3.7.6): the attribution never influences the verdict and is an audit component only; it decomposes the logit, not the calibrated probability (on the calibrated logit scale each contribution is multiplied by $\gamma_1 > 0$, which preserves relative contributions); feature correlation limits the interpretation of each contribution as a Shapley value but not the identity; and it is not a contribution, because auditable decision records are provided by existing systems (Hossain et al., 2026; C. Yang, 2026). The attribution can equally be computed at audit time from the logged evidence and frozen parameters.

## 6.7 Relevance of Sequential Monitoring

Sequential change detection is not part of REM's verdict path. It is an optional, offline, observe-only analysis of logged per-step indicators, to be performed only if the supervisor approves it for the thesis narrative (Chapter 3, Section 3.11.10). Its relevance is the question of whether deviations accumulate over an episode. The procedure has known optimality properties (Lorden, 1971; Moustakides, 1986), but these are proved within a model whose conditions could not be inspected and are not claimed to hold for agent trajectories, whose observations are neither independent nor drawn from known distributions. The results therefore motivate the procedure and provide no guarantee in this setting. Given the short trajectories of the benchmark, the analysis may have little to detect.

## 6.8 Why Decision Making Requires Costs

A probability alone does not determine an intervention: the same probability can warrant different responses depending on what the action would do. Chapter 3 introduces costs so that the verdict accounts for the consequence of the proposed action (security objective SO-3). Costs are policy quantities that encode institutional judgment; they are declared before evaluation, are not presented as empirical findings, and are varied over a declared grid (Chapter 3, Section 3.7.3 and Table 3.12). Correct automatic decisions are assigned zero loss by declared convention. The Modify loss on an induced action depends on the measured residual attack-success rate $r_{\text{mod}}(k)$ (Equation 3.5), so mitigation effectiveness enters the decision as a measured quantity. The Escalate entries assume a reviewer who resolves escalations correctly; this assumption is bounded in the experiments by a no-reviewer bound (Section 7.5).

## 6.9 Expected Loss as the Link Between Probability and Intervention

Expected loss connects the calibrated probability to the verdict. For each feasible verdict, the conditional risk (Equation 3.6) weights the loss for a legitimate action by $1 - p_t$ and the loss for an induced action by $p_t$; the verdict minimizes this risk (Equation 3.7). Because each $R_t(v)$ is affine in $p_t$, the verdict changes only where two conditional risks are equal, which yields the pairwise indifference thresholds of Equation 3.8 and the Allow–Block threshold of Equation 3.9. Thresholds are therefore consequences of declared costs rather than independently chosen constants: the question "why this threshold?" becomes "why this cost ratio?", which the loss grid addresses (Chapter 3, Section 3.7.5). Equation 3.10 states when escalation can be selected at all, and the dominance check identifies verdicts that a declaration makes unreachable; such cases are reported rather than silently producing a smaller verdict set. The substitution of $p_t$ for the true conditional probability is justified only to the extent that $p_t$ is calibrated.

# 7. Decision Engine

## 7.1 Evidence Entering the Decision Engine

Table: Table 52. Inputs to the Decision Engine

| Input | Content | Origin |
|--------------------|----------------------------------------------------|---------------------------|
| Prompt and context evidence | $x^{\text{ctx}}_1$ (injection-classifier score), $x^{\text{ctx}}_2$ (instruction-pattern indicator) | Layer 2 |
| Behavioral evidence | $x^{\text{beh}}_1$ (post-observation shift), $x^{\text{beh}}_2$ (repeated calls), $x^{\text{beh}}_3$ (privilege escalation), $x^{\text{beh}}_4$ (transition deviation) | Layer 3 |
| Tool and action evidence | $x^{\text{act}}_1$ (argument provenance), $x^{\text{act}}_2$ (destination novelty), $x^{\text{act}}_3$ (sensitive egress) | Layer 3 |
| Feature availability | Set of features computable at step $t$ ("avail") | Layer 4, Algorithm 1 line 11 |
| Consequence descriptors | Action category, amount, recurring-payment change, credential change, irreversibility (declared per tool) | The proposed action $a_t$ (Chapter 3, Table 3.10) |
| Frozen parameters | $\beta_0$, $\beta$, $\gamma_1 > 0$, $\gamma_0$, $\overline{x}$ | Offline fitting |
| Declared policy | $\kappa$, amount limits, loss structure, $\Pi$, $k_{\text{D2}}$, required evidence per tier, $\mathcal{T}_R$, tie-breaking order | Declared before evaluation |

## 7.2 Risk-Related Quantities

The Decision Engine computes the logit $s_t$, the uncalibrated probability $\tilde{p}_t$, the calibrated probability $p_t$, the consequence tier $k_t$ and the conditional risks $R_t(v)$ for each feasible verdict. Chapter 3 does not define any composite risk score beyond these quantities; the probability and the consequence remain separate until they are combined in Equation 3.6.

## 7.3 Decision Logic

The decision proceeds in a fixed order (Chapter 3, Algorithm 1, lines 11–23):

1. Assemble $x_t = [x^{\text{ctx}}; x^{\text{beh}}; x^{\text{act}}]$ and record feature availability.
2. Compute $s_t$ and $\tilde{p}_t$ (Equation 3.1), then $p_t$ (Equation 3.3).
3. Assign the tier $k_t = \kappa(z_t)$.
4. If $a_t \in \Pi$, issue Block with source D1.
5. Otherwise, if the evidence required at tier $k_t$ is not available and $k_t \ge k_{\text{D2}}$, issue Escalate with source D2.
6. Otherwise, form the feasible set $\mathcal{V}(a_t)$ (Allow, Escalate and Block for every action; Modify only if the tool of $a_t$ belongs to $\mathcal{T}_R$), compute $R_t(v)$ for each feasible verdict (Equation 3.6), and select the minimum, resolving ties toward the more restrictive verdict (Equation 3.7), with source "expected loss".
7. Write the audit record (Section 7.4.6).

When a predicate applies, it determines the verdict, the expected-loss rule is not consulted, and the audit record names the predicate as the source (Chapter 3, Section 3.7.4).

## 7.4 Expected-Loss Formulation

The formulation below is reproduced from Chapter 3, Section 3.7.5; no additional mathematics is inferred.

### 7.4.1 States

The state of the proposed action is the latent label $y_t \in \{0, 1\}$: $y_t = 1$ if $a_t$ is adversarially induced, and $y_t = 0$ if it is legitimate. The label is not observable at runtime.

### 7.4.2 Actions

The actions of the decision problem are the verdicts in the feasible set $\mathcal{V}(a_t) \subseteq \{\text{Allow}, \text{Modify}, \text{Escalate}, \text{Block}\}$.

### 7.4.3 Costs and Losses

Table: Table 53. Tier-indexed loss structure $L(v, y, k)$ (Chapter 3, Table 3.13)

| Verdict $v$ | $L(v, 0, k)$: legitimate action | $L(v, 1, k)$: adversarially induced action |
|-------------------|---------------------------------|-----------------------------------------------|
| Allow | $0$ | $C_{\text{miss}}(k)$ |
| Modify | $C_{\text{mod}}(k)$ | $r_{\text{mod}}(k) \cdot C_{\text{miss}}(k)$ |
| Escalate | $C_{\text{esc}}$ | $C_{\text{esc}}$ |
| Block | $C_{\text{FA}}(k)$ | $0$ |

$C_{\text{miss}}(k)$, $C_{\text{FA}}(k)$, $C_{\text{mod}}(k)$ and $C_{\text{esc}}$ are declared costs of a missed attack, a false intervention by Block, Modify on a legitimate action, and escalation. $r_{\text{mod}}(k)$ is measured. The values of the declared costs are NOT SPECIFIED IN CURRENT CHAPTER 3; they are policy quantities declared before evaluation and varied over a declared grid.

### 7.4.4 Probabilities

The probability of the state $y_t = 1$ is replaced by the calibrated estimate $p_t$ of Equation 3.3. Chapter 3 states that this substitution is justified only to the extent that $p_t$ is calibrated.

### 7.4.5 Expected Loss and Decision Rule

$$ R_{t}(v) = (1 - p_{t}) \cdot L(v, 0, k_{t}) + p_{t} \cdot L(v, 1, k_{t}), \qquad v \in \mathcal{V}(a_{t}) \qquad\qquad (3.6) $$

$$ v_{t} = \arg\min_{v \in \mathcal{V}(a_{t})} R_{t}(v) \qquad\qquad (3.7) $$

with ties resolved toward the more restrictive verdict in the order Block ⪰ Escalate ⪰ Modify ⪰ Allow. The derived thresholds (Equations 3.8–3.9), the escalation feasibility condition (Equation 3.10) and the dominance check (expression U-11) characterize this rule for a declared loss structure (Section 5.4).

### 7.4.6 Audit Record

For every verdict the Decision Engine writes an audit record containing the evidence vector $x_t$, the logit $s_t$, the probabilities $\tilde{p}_t$ and $p_t$, the tier $k_t$, the conditional risks $R_t(v)$, the verdict $v_t$ and its source (D1, D2 or the expected-loss rule), the model, calibration and policy versions, and a linear attribution of the logit. The record is appended to an append-only audit log (Algorithm 1, lines 24–27).

## 7.5 Operational Meaning of the Four Verdicts

Table 54 reproduces the mechanisms specified in Chapter 3, Table 3.14, alongside the canonical semantics of the project design contract.

Table: Table 54. Verdict semantics in Chapter 3 and in the design contract

| Verdict | Chapter 3 (Table 3.14) | Design contract (`CLAUDE.md`, Mitigation Lock) |
|------------|-----------------------------------------------|-----------------------------------------|
| Allow | Release: $a_t$ is released across TB-3 and the event is logged. | Release the current action. |
| Modify | Tool restriction: $a_t$ is not executed; the tool class of $a_t$ is removed from the agent's available tools for the rest of the episode; a structured notice is returned; applies only to tools in $\mathcal{T}_R$. | Apply one declared modification mechanism to the current action or execution context. The contract states: "Do NOT silently redefine Modify as removing a tool class for the rest of the episode." |
| Escalate | Withhold and refer: $a_t$ is withheld and the audit record is presented to a human reviewer; the action is released only if the reviewer approves. | Withhold the current action pending review. |
| Block | Interrupt with safe fallback: $a_t$ is not executed, every tool in $\mathcal{T}_R$ is restricted for the rest of the episode, and a structured refusal is returned. | Prevent execution of the current proposed action. The contract states: "Do NOT silently redefine Block as disabling all state-changing tools for the rest of the episode." |

> **Specification conflict — SUPERVISOR DECISION REQUIRED.** The Allow and Escalate semantics agree. The Modify and Block semantics of Chapter 3 include episode-level restrictions that the design contract treats as "a separate experimental policy requiring explicit specification". Project records document the same point: `RECONCILIATION.md` (item C7) records tool-class withholding as a conflict with the Mitigation Lock, and `STAGE2_BLOCKED_DECISIONS.md` records tool restriction as excluded. The project prototype implements step-level mechanisms only. This summary describes Chapter 3 as written and does not resolve the conflict.

In the experiments, no human reviewer is available in the benchmark. Escalation is resolved in two ways, and both are reported: by an idealized reviewer who releases the action if $y_t = 0$ and prevents it if $y_t = 1$, and by a no-reviewer bound in which every escalation is treated as Block (Chapter 3, Section 3.11.7).

## 7.6 Consequence-Independent Baseline

The primary comparator B1 uses the same estimator and calibration with the threshold policy of Equation 3.14 and expression U-13. It issues Escalate only through predicate D2. Because its thresholds are selected by ranking, a strictly increasing recalibration leaves its verdicts unchanged, whereas cost-derived thresholds such as Equation 3.9 are fixed in probability units and can change after recalibration. Chapter 3 states that this contrast is consistent with the finding of C. Zhang et al. (2026) that recalibration need not change threshold-routed control. The operating-point policy is a baseline only; it is not a second primary methodology.

## 7.7 Relation to the NEXUS Decision Policy

Chapter 2 records that NEXUS (Hossain et al., 2026) combines deterministic safety rules, argument-level inspection and a logistic-regression risk score calibrated by Platt scaling; that its deployed policy selects among four interventions (allow, block, request confirmation, request revision) through a rule cascade in which the calibrated score gates certain cases; and that the paper **also defines an expected-loss objective with fixed costs for each intervention** (Chapter 2, L65 and L134). Chapter 2 draws the distinction from REM on the following ground: NEXUS's "deployed policy, however, is a rule cascade in which the learned score adjudicates particular cases, not a per-decision minimization of conditional risk" (Chapter 2, L134).

The distinction is therefore not that NEXUS lacks an expected-loss formulation; it concerns whether that formulation is used to select each verdict. Evidence status: the Stage 1 claim audit records the expected-loss-objective sentence (Ch2-C028) and the rule-cascade sentence (Ch2-C024) as supported from a full-text reading of NEXUS. That reading cannot be reproduced in the current verification environment, the sentence stating that the deployed policy is "not a per-decision minimization of conditional risk" has no separate claim-level audit record, and the relationship between the NEXUS objective and its deployed policy remains open (OI-01). Chapter 3 accordingly does not claim calibrated logistic risk scores or four-way intervention as novel (Table 3.16).

# 8. System Design and Implementation

## 8.1 Basis of This Section

Chapter 3 specifies the design and the per-step runtime procedure (Algorithm 1) and the offline procedure (Procedure 3.1); it states that Chapter 4 describes the implementation. This section therefore describes the components specified in Chapter 3 (Part A) and, separately, the elements that an implementation requires but Chapter 3 does not specify (Part B). No unspecified element is given a value or design here.

## 8.2 Part A — Components Explicitly Specified in Chapter 3

### 8.2.1 Context Capture and Hygiene (Layer 1)

Table: Table 55. Component C1

| Field | Specification |
|--------------------|--------------------------------------------------------------------------------|
| Purpose | Receive the step's inputs and hold the proposed action; remove invisible and formatting characters from untrusted text. |
| Inputs | $g$ and user messages; system prompt; tool results; proposed action $a_t$. |
| Outputs | Normalized segments with source channel; held $a_t$. |
| Dependencies | Interception at the tool-execution boundary (AS-1). |
| Required data | None beyond the step's inputs. |
| Parameters | Set of characters removed: zero-width and formatting characters (exact set NOT SPECIFIED IN CURRENT CHAPTER 3). |
| Runtime role | First operation at every step. |
| Failure behavior | NOT SPECIFIED IN CURRENT CHAPTER 3. |

### 8.2.2 Provenance Labeler (Layer 1)

Table: Table 56. Component C2

| Field | Specification |
|----------------------|------------------------------------------------------------------------------|
| Purpose | Label every context segment trusted, semi-trusted or untrusted, with least-trusted inheritance and no promotion. |
| Inputs | Segments with source channel. |
| Outputs | Labeled context $c_t$. |
| Dependencies | C1; reliable source attribution (AS-2). |
| Required data | Source channel of each segment. |
| Parameters | The ordered label set (specified). |
| Runtime role | Every step. |
| Failure behavior | NOT SPECIFIED IN CURRENT CHAPTER 3 (for example, a segment whose source cannot be attributed). |

### 8.2.3 Entity Extractor (Layer 1)

Table: Table 57. Component C3

| Field | Specification |
|-----------------------|-----------------------------------------------------------------------------|
| Purpose | Extract account identifiers, amounts, credential values, profile values and tool names, with provenance, from $c_t$, $g$ and the arguments of $a_t$. |
| Inputs | $c_t$, $g$, $a_t$. |
| Outputs | $\text{Ent}_t$. |
| Dependencies | C2. |
| Required data | None. |
| Parameters | Extraction patterns, declared in configuration and fixed before evaluation (pattern content NOT SPECIFIED IN CURRENT CHAPTER 3). |
| Runtime role | Every step. |
| Failure behavior | NOT SPECIFIED IN CURRENT CHAPTER 3. |

### 8.2.4 Context-Evidence Computer (Layer 2)

Table: Table 58. Component C4

| Field | Specification |
|------------------|----------------------------------------------------------------------------------|
| Purpose | Compute $x^{\text{ctx}}_1$ and $x^{\text{ctx}}_2$. |
| Inputs | Untrusted segments added since the previous step. |
| Outputs | $x^{\text{ctx}}$. |
| Dependencies | A fixed, pre-trained prompt-injection classifier (choice pending supervisor approval); declared instruction-pattern set. |
| Required data | None at runtime; the classifier is not retrained. |
| Parameters | Classifier identity and version (pending); instruction-pattern set (declared before evaluation; content NOT SPECIFIED IN CURRENT CHAPTER 3). |
| Runtime role | Every step, in parallel with Layer 3. |
| Failure behavior | If evidence required at a tier cannot be computed and $k_t \ge k_{\text{D2}}$, predicate D2 issues Escalate. Other failure handling NOT SPECIFIED IN CURRENT CHAPTER 3. |

### 8.2.5 History Tracker (Layer 3)

Table: Table 59. Component C5

| Field | Specification |
|------------------------|----------------------------------------------------------------------------|
| Purpose | Maintain $H_t$: proposed actions, arguments with provenance, verdicts issued and tool results returned. |
| Inputs | Each step's action, verdict and tool result. |
| Outputs | $H_t$. |
| Dependencies | C3; Layer 5 outcomes (Algorithm 1, line 34). |
| Required data | None. |
| Parameters | None specified. |
| Runtime role | Reset at the start of each episode; updated at every step. |
| Failure behavior | NOT SPECIFIED IN CURRENT CHAPTER 3. |

### 8.2.6 Behavioral and Action Feature Computer (Layer 3)

Table: Table 60. Component C6

| Field | Specification |
|---------------------|-------------------------------------------------------------------------------|
| Purpose | Compute the seven features of Chapter 3, Table 3.9. |
| Inputs | $H_t$, $a_t$, $\text{Ent}_t$, $g$. |
| Outputs | $x^{\text{beh}}$, $x^{\text{act}}$. |
| Dependencies | Benign reference transition set; declared privilege map; declared $n_{\text{max}}$. |
| Required data | Benign fitting data (for the transition set, estimated offline within each outer fold). |
| Parameters | $n_{\text{max}}$, privilege map (declared; values NOT SPECIFIED IN CURRENT CHAPTER 3). |
| Runtime role | Every step, in parallel with Layer 2. |
| Failure behavior | Unavailable features are recorded in "avail"; predicate D2 applies at tiers $k_t \ge k_{\text{D2}}$. |

### 8.2.7 Probability Estimator and Calibrator (Layer 4)

Table: Table 61. Component C7

| Field | Specification |
|-----------------------|-----------------------------------------------------------------------------|
| Purpose | Compute $s_t$, $\tilde{p}_t$ and $p_t$ (Equations 3.1 and 3.3). |
| Inputs | $x_t$. |
| Outputs | $s_t$, $\tilde{p}_t$, $p_t$. |
| Dependencies | Frozen $\beta_0$, $\beta$, $\gamma_1 > 0$, $\gamma_0$ from offline fitting. |
| Required data | Labeled observe-only traces (offline). |
| Parameters | $\lambda$ (selected offline); $\beta_0$, $\beta$, $\gamma_1$, $\gamma_0$ (learned). |
| Runtime role | Every step. |
| Failure behavior | Offline: a fitted $\gamma_1 \le 0$ is recorded as a calibration failure for that fold. Runtime failure handling NOT SPECIFIED IN CURRENT CHAPTER 3. |

### 8.2.8 Consequence Tier Mapper (Layer 4)

Table: Table 62. Component C8

| Field | Specification |
|---------------------------|-------------------------------------------------------------------------|
| Purpose | Assign $k_t = \kappa(z_t)$. |
| Inputs | Descriptors $z_t$ of $a_t$. |
| Outputs | $k_t$. |
| Dependencies | Declared $\kappa$ and amount limits. |
| Required data | None. |
| Parameters | $K$, amount limits, irreversibility per tool (declared; tier policy pending supervisor approval). |
| Runtime role | Every step. |
| Failure behavior | NOT SPECIFIED IN CURRENT CHAPTER 3. |

### 8.2.9 Policy Predicate Evaluator (Layer 4)

Table: Table 63. Component C9

| Field | Specification |
|---------------------|-------------------------------------------------------------------------------|
| Purpose | Apply D1 (prohibited action → Block) and D2 (missing required evidence at $k_t \ge k_{\text{D2}}$ → Escalate) before verdict selection. |
| Inputs | $a_t$, $k_t$, feature availability. |
| Outputs | A predicate verdict and source, or no verdict. |
| Dependencies | Declared $\Pi$, $k_{\text{D2}}$ and required evidence per tier. |
| Required data | None. |
| Parameters | $\Pi$, $k_{\text{D2}}$, required evidence per tier (declared; values NOT SPECIFIED IN CURRENT CHAPTER 3). |
| Runtime role | Every step, before expected-loss selection. |
| Failure behavior | D2 is itself the specified response to missing evidence. |

### 8.2.10 Expected-Loss Verdict Selector (Layer 4)

Table: Table 64. Component C10

| Field | Specification |
|-------------------|---------------------------------------------------------------------------------|
| Purpose | Compute $R_t(v)$ for each feasible verdict and select the minimum (Equations 3.6–3.7). |
| Inputs | $p_t$, $k_t$, feasible set $\mathcal{V}(a_t)$. |
| Outputs | $v_t$, $R_t(\cdot)$, source "expected loss". |
| Dependencies | Declared loss structure; measured $r_{\text{mod}}(k)$; declared $\mathcal{T}_R$; declared tie order. |
| Required data | Enforcing-mode runs (for $r_{\text{mod}}(k)$, offline). |
| Parameters | $C_{\text{miss}}(k)$, $C_{\text{FA}}(k)$, $C_{\text{mod}}(k)$, $C_{\text{esc}}$ (declared; values NOT SPECIFIED IN CURRENT CHAPTER 3). |
| Runtime role | Every step on which no predicate applies. |
| Failure behavior | Exact ties are resolved toward the more restrictive verdict (Chapter 3); see Section 15.1 for the divergence from the prototype. |

### 8.2.11 Attribution and Audit-Record Writer; Audit Log (Layer 4 and Store)

Table: Table 65. Component C11

| Field | Specification |
|--------------------|--------------------------------------------------------------------------------|
| Purpose | Compute the attribution (Equations 3.11 and 3.13), check the identity (Equation 3.12), and append the audit record to the append-only log. |
| Inputs | $x_t$, $s_t$, $\tilde{p}_t$, $p_t$, $k_t$, $R$, $v_t$, source, versions, timestamps. |
| Outputs | Audit record $r_t$. |
| Dependencies | Frozen parameters and $\overline{x}$. |
| Required data | Benign fitting data (for $\overline{x}$, offline). |
| Parameters | Identity tolerance $\varepsilon$ (NOT SPECIFIED IN CURRENT CHAPTER 3). |
| Runtime role | Every step; does not affect the verdict. |
| Failure behavior | Behaviour when the identity check fails is NOT SPECIFIED IN CURRENT CHAPTER 3. Protection of the log is assumed (AS-3). |

### 8.2.12 Mitigation Executor and Restriction State (Layer 5)

Table: Table 66. Component C12

| Field | Specification |
|--------------------|--------------------------------------------------------------------------------|
| Purpose | Execute the mechanism associated with $v_t$ and enforce restrictions from earlier verdicts. |
| Inputs | $v_t$, $a_t$, restriction state $S$. |
| Outputs | Released, restricted, withheld or refused action; structured notice or refusal. |
| Dependencies | Declared $\mathcal{T}_R$. |
| Required data | None. |
| Parameters | $\mathcal{T}_R$ (specified by category for the banking environment). |
| Runtime role | Every step, before the action is released. |
| Failure behavior | Calls to restricted tools are refused with a structured notice (Algorithm 1, line 29). Episode-level restriction semantics subject to the conflict in Section 15.1. |

### 8.2.13 Human Review Path (External Element)

Table: Table 67. Component C13

| Field | Specification |
|-----------------------|-----------------------------------------------------------------------------|
| Purpose | Decide on escalated actions using the audit record. |
| Inputs | Audit record $r_t$. |
| Outputs | Approval (release) or refusal. |
| Dependencies | Escalate verdicts. |
| Required data | None specified. |
| Parameters | None specified. |
| Runtime role | Only when Escalate is issued; in experiments replaced by an idealized reviewer and a no-reviewer bound. |
| Failure behavior | Reviewer interface, response time and timeout behaviour are NOT SPECIFIED IN CURRENT CHAPTER 3. |

### 8.2.14 Offline Fitting Procedure (Cross-Cutting)

Table: Table 68. Component C14

| Field | Specification |
|-----------------|-----------------------------------------------------------------------------------|
| Purpose | Fit and freeze reference quantities, coefficients, calibration parameters, baseline thresholds and $r_{\text{mod}}(k)$; check the loss structure; record versions (Procedure 3.1). |
| Inputs | Logged observe-only traces grouped by injection task and user task; labels; declared policy. |
| Outputs | Frozen parameters; stored held-out predictions; version records. |
| Dependencies | Grouped cross-fitting (Section 4.12); enforcing-mode runs. |
| Required data | Labeled traces (label construction, Chapter 3, Section 3.11.3). |
| Parameters | Fold structure; $\lambda$ search (search range NOT SPECIFIED IN CURRENT CHAPTER 3); $\alpha_{\text{blk}}$, $\alpha_{\text{mod}}$. |
| Runtime role | None; never executed within an episode. |
| Failure behavior | A fitted $\gamma_1 \le 0$ is recorded as a calibration failure for the fold; drift beyond a declared tolerance triggers refitting (tolerance NOT SPECIFIED IN CURRENT CHAPTER 3). |

## 8.3 Part B — Elements Necessary but Not Specified in Chapter 3

The following are required for an implementation but are not specified in the current Chapter 3. They are listed without proposed values.

Table: Table 69. Implementation elements not specified in Chapter 3

| Element | Status |
|------------------------------------------------|----------------------------------------------------|
| Programming language, libraries and their versions | NOT SPECIFIED IN CURRENT CHAPTER 3 (Chapter 3 requires that versions be recorded) |
| Interception mechanism at the tool-execution boundary | NOT SPECIFIED IN CURRENT CHAPTER 3 (AS-1; to be demonstrated in Chapter 4) |
| Behaviour when REM itself fails at runtime (for example, a component error or timeout) | NOT SPECIFIED IN CURRENT CHAPTER 3 |
| Latency budget | NOT SPECIFIED IN CURRENT CHAPTER 3 (latency is measured and reported, not bounded) |
| Audit-log storage and integrity mechanism | NOT SPECIFIED IN CURRENT CHAPTER 3 (log protection is assumed, AS-3) |
| Human reviewer interface and timeout | NOT SPECIFIED IN CURRENT CHAPTER 3 |
| Injection classifier identity | SUPERVISOR DECISION REQUIRED (pending approval) |
| Instruction-pattern set and extraction patterns | NOT SPECIFIED IN CURRENT CHAPTER 3 (declared before evaluation) |
| Values of $n_{\text{max}}$, privilege map, $K$, amount limits, $\Pi$, $k_{\text{D2}}$, required evidence per tier | NOT SPECIFIED IN CURRENT CHAPTER 3 (declared policy) |
| Values of $C_{\text{miss}}(k)$, $C_{\text{FA}}(k)$, $C_{\text{mod}}(k)$, $C_{\text{esc}}$ and the loss grid | NOT SPECIFIED IN CURRENT CHAPTER 3 (declared before evaluation) |
| $\alpha_{\text{blk}}$, $\alpha_{\text{mod}}$; $\varepsilon$; the numerical clipping constant for log-loss; number of ECE bins $M$; calibration-drift tolerance | NOT SPECIFIED IN CURRENT CHAPTER 3 |
| Exact AgentDojo version or commit | NOT SPECIFIED IN CURRENT CHAPTER 3 (OI-14) |
| LLM backbone(s) and attack templates | SUPERVISOR DECISION REQUIRED (pending approval) |
| Number of repeated runs | SUPERVISOR DECISION REQUIRED (Chapter 3 states "at least three", pending approval) |

## 8.4 Relation to the Project Prototype

The project repository contains a prototype implementation, described in Chapter 4. Two divergences between the prototype and the current Chapter 3 are documented in project records and are listed in Section 15.1: the prototype's mitigation mechanisms are step-level only, and the prototype raises an error on an exact verdict tie because no tie-breaking rule is frozen in the design contract. This summary does not align either side.

# 9. Implementation Requirements

## 9.1 Software Requirements

Chapter 3 explicitly specifies:

- the AgentDojo framework and its banking suite as the evaluation environment (Debenedetti et al., 2024); the exact version is to be pinned and is not yet specified (OI-14);
- a fixed, pre-trained prompt-injection classifier used with fixed inference and not retrained; the candidate named is PromptGuard 2 in LlamaFirewall (Chennabasappa et al., 2025), and the choice is pending supervisor approval;
- recording of the AgentDojo release or commit identifier, the suite version, the attack template, the LLM backbone identifier and version, access date and decoding parameters, and REM's model, calibration and policy versions for every run;
- documentation of the mapping between the penalty parameterization of Equation 3.2 and the parameterization used by the software library.

Programming language, machine-learning library, logging infrastructure and deployment platform: NOT SPECIFIED IN CURRENT CHAPTER 3.

## 9.2 Data Requirements

Chapter 3 specifies the following data and signals:

- the banking suite definition inspected for Chapter 3 (suite v1, AgentDojo repository main branch, accessed September 2026): 16 user tasks, 9 injection tasks and 11 tools, to be re-confirmed against the pinned version. Stage 2 confirmed these counts from the source of the `agentdojo` 0.1.35 package and found them unchanged across benchmark versions 1.0.0–1.2.2, while task content differs between versions;
- traces generated by running an agent, whose number depends on the backbones, attack templates and repeated runs [DATA COUNT REQUIRES VERIFICATION]. The 144 combinations of user task and injection task are not 144 independent samples;
- step labels derived from the injection task's reference solution by matching on tool name and attacker-controlled key argument; the labeling of induced read steps is pending supervisor decision; the derivation is audited on a manually inspected sample, and the disagreement rate is reported;
- benign reference data for $\overline{x}$ and the benign transition set;
- enforcing-mode runs for $r_{\text{mod}}(k)$ and the utility impact of Modify;
- per-step runtime signals listed in Section 10.

Chapter 3 records five data limitations: positive-step scarcity, a shared attacker account identifier (eight of the nine injection tasks), repeated task templates, short trajectories, and scarce calibration data.

## 9.3 Training Requirements

Training, validation, calibration and testing follow nested grouped cross-fitting (Chapter 3, Section 3.11.5), because four statistically independent partitions cannot be supported:

- **Outer folds:** nine leave-one-injection-task-out folds for attacked episodes; episodes without injection assigned by user task.
- **Inner folds:** grouped inner cross-validation within each outer fold's fitting portion selects $\lambda$ by held-out log-loss and produces out-of-fold logits for calibration (Equation 3.4) and baseline thresholds (Equation 3.14).
- **Held-out scoring:** all reported metrics are computed from outer held-out predictions.
- **Deployment model:** a model fitted on all data is used only for runtime demonstrations and latency measurement.
- **Pilot E0:** before the feature set is frozen, a pilot on the fitting portions checks the number of positive steps and the ROC-AUC of each evidence group; the pilot decision values are project decisions pending supervisor approval.
- **Leakage controls:** no identity-based features; benign reference quantities estimated within each fold's fitting portion; all declared quantities fixed before held-out predictions are examined; fitting data collected in observe-only mode; no pooling across benchmarks.
- **Repetition and uncertainty:** each configuration is run at least three times with fixed decoding parameters (number pending supervisor approval); results are aggregated per episode template; intervals are obtained by group bootstrap (Efron, 1979); the word "significant" is not used unless a stated test supports it.
- **Sensitivity analysis:** a repetition with folds grouped by user task is pending supervisor approval.

## 9.4 Runtime Requirements

- **Observation:** interception of each proposed tool call before execution and each tool result on return, without modifying the agent (AS-1, to be demonstrated).
- **Interception and sequencing:** at each step, Layer 1, then Layers 2 and 3 in parallel, then Layer 4, then Layer 5, before the action is released.
- **State tracking:** the history $H_t$, reset per episode, and the episode restriction state $S$.
- **Decision execution:** frozen parameters and declared policy only; no runtime adaptation.
- **Mitigation:** deterministic execution of the verdict's mechanism; refusal of calls to restricted tools.
- **Modes:** observe-only and enforcing.
- **Latency:** wall-clock time of REM's per-step processing, excluding LLM inference and tool execution, reported as median and 95th percentile. A latency budget is NOT SPECIFIED IN CURRENT CHAPTER 3.

## 9.5 Security Requirements

- **Trust boundaries:** TB-1 to TB-4 as defined in Table 4; TB-2 is the primary observation point and TB-3 the primary enforcement point; TB-4 is in design scope only.
- **Untrusted content:** tool outputs and retrieved content are untrusted by default (AS-5); derived content inherits the least-trusted label and is never promoted.
- **Tool outputs:** a released action's tool result re-enters Layer 1 as untrusted content at the next step.
- **State integrity:** REM's parameters are never changed during an episode; runtime adaptation is excluded so that an adversary who generates traffic cannot shift REM's reference behaviour; the adversary is assumed unable to modify REM's code, parameters, policy or logs (AS-3, a stated limitation). A technical mechanism for protecting that state is NOT SPECIFIED IN CURRENT CHAPTER 3.
- **Logging:** an append-only audit log from which every verdict can be reproduced (SO-5).
- **Fail-safe behaviour within the decision rule:** a prohibited action is always blocked (D1); missing required evidence at high tiers leads to escalation, because absent evidence is not treated as evidence of safety (D2); Block returns a structured refusal as a safe fallback.
- **Fail-safe behaviour on REM's own failure:** NOT SPECIFIED IN CURRENT CHAPTER 3.
- **No identity-based features:** to prevent label leakage through the shared attacker account identifier.

# 10. Data and Information Flow

Content enters REM at the trust boundaries and is labeled in Layer 1. Evidence is generated in Layers 2 and 3 and assembled in Layer 4. The Decision Engine receives only the evidence vector, the consequence descriptors, frozen parameters and declared policy. Mitigation acts on the held action at TB-3, and its outcome returns to the history.

Table: Table 70. Data and information flow

| Data / Signal | Source | REM Stage | Representation | Purpose |
|-------------------|---------------|--------------|---------------------------|-------------------------|
| User objective $g$ and user messages | User (TB-1) | L1 | Segments labeled semi-trusted | Reference for argument provenance and destination novelty |
| System prompt | System | L1 | Segment labeled trusted | Context |
| Tool results, retrieved content | Tools and environment (TB-2) | L1 | Segments labeled untrusted | Primary observation point |
| Memory content | Persistent store (TB-4) | L1 | Untrusted, provenance retained (design scope only) | Context |
| Proposed action $a_t$ | Agent (TB-3) | L1 (held until L5) | Tool name and arguments | Object of the decision |
| Labeled context $c_t$ | L1 | L2, L3 | Segments with provenance labels | Evidence computation |
| Entities $\text{Ent}_t$ | L1 | L3 | Values with provenance | Argument provenance, egress |
| History $H_t$ | L3 | L3 | Sequence of actions, arguments with provenance, verdicts, tool results | Behavioral features |
| $x^{\text{ctx}}_1$, $x^{\text{ctx}}_2$ | L2 | L4 | [0, 1]; binary | Context evidence |
| $x^{\text{beh}}_1$–$x^{\text{beh}}_4$ | L3 | L4 | Binary or [0, 1] | Behavioral evidence |
| $x^{\text{act}}_1$–$x^{\text{act}}_3$ | L3 | L4 | Binary | Action evidence |
| Feature availability (avail) | L4 | L4 (predicate D2) | Set of computable features | Detect missing required evidence |
| Consequence descriptors $z_t$ | $a_t$ | L4 | Category, amount, flags, declared irreversibility | Tier assignment |
| $s_t$, $\tilde{p}_t$, $p_t$ | L4 | L4 | Real number; probabilities | Estimation and calibration |
| Tier $k_t$ | L4 | L4 | Integer in $\{1, \ldots, K\}$ | Loss indexing |
| $R_t(v)$ | L4 | L4 | Real number per feasible verdict | Verdict selection |
| Verdict $v_t$ and source | L4 | L5; audit log | One of four verdicts; D1, D2 or expected loss | Mitigation |
| Attribution $\varphi_0$, $\varphi_t$, $\Phi$ | L4 | Audit log | Real numbers per feature and group | Audit only |
| Audit record $r_t$ | L4 | Audit log; human reviewer | Structured record | Reproducibility (SO-5); escalation |
| Restriction state $S$ | L5 | L5 | Set of restricted tool classes | Enforcement of earlier verdicts |
| Reviewer decision | Human reviewer | L5 | Approve or refuse | Resolution of Escalate |
| Structured notice or refusal | L5 | Agent | Message | Informs the agent of the outcome |
| Frozen parameters | Offline fitting | L3, L4 | $\beta_0$, $\beta$, $\gamma_1$, $\gamma_0$, $\overline{x}$, transition set | Estimation, calibration, features, attribution |
| Declared policy | Project declaration | L3, L4, L5 | $\kappa$, $L$, $\Pi$, $k_{\text{D2}}$, $\mathcal{T}_R$, privilege map, tie order | Decision and mitigation |

# 11. Equation-to-Component Traceability

Every numbered equation of Chapter 3 appears in Table 71. Unnumbered expressions are traced in Table 50.

Table: Table 71. Equation-to-component traceability

| Equation | Purpose | REM Component | Variables | Source | Evidence Location | Verification |
|----------|-----------------|-------------|--------------|-----------------|-----------------|--------------|
| 3.1 | Logit and uncalibrated probability | L4 estimation | $s_t$, $\beta_0$, $\beta$, $x_t$, $\tilde{p}_t$ | Cox (1958) | Crossref record only | IV; SOURCE NOT FULLY VERIFIED |
| 3.2 | Ridge-penalized fit | Offline fitting | $\beta_0$, $\beta$, $D_{\text{fit}}$, $y_i$, $\lambda$ | le Cessie & van Houwelingen (1992) | Crossref record only; constant pending | IV; SOURCE NOT FULLY VERIFIED |
| 3.3 | Calibration on the logit | L4 calibration | $p_t$, $\gamma_1$, $\gamma_0$, $s_t$ | Platt (1999); Guo et al. (2017); Kull et al. (2017) | Guo §4.1; Kull §2.2, Prop. 1; Platt inaccessible | Guo FV; Kull FV; Platt NC (OI-07) |
| 3.4 | Calibration fit by NLL | Offline fitting | $\gamma_1$, $\gamma_0$, $D_{\text{cal}}$ | Guo et al. (2017) | Full text (ar5iv) | FV |
| 3.5 | Modify loss on induced action | L4 loss structure | $r_{\text{mod}}(k)$, $C_{\text{miss}}(k)$ | Law of total expectation (A-Mod) | Chapter 3 §3.7.5 | DER |
| 3.6 | Conditional risk | L4 verdict selection | $R_t(v)$, $p_t$, $L$, $k_t$, $\mathcal{V}(a_t)$ | Elkan (2001), adapted | Elkan Eq. (1), p. 1 of author PDF | FV |
| 3.7 | Minimum-risk verdict | L4 verdict selection | $v_t$ | Elkan (2001); tie order REM-defined | Elkan Eq. (1) | FV; tie order DEF |
| 3.8 | Pairwise indifference threshold | L4 analysis | $\pi_{v,v'}(k)$, $\Delta_0$, $\Delta_1$ | Derived from 3.6 | Chapter 3 §3.7.5 | DER (confirmed, Stage 2) |
| 3.9 | Allow–Block threshold | L4 analysis; reliability reporting | $p^{\text{*}}_{k}$, $C_{\text{FA}}(k)$, $C_{\text{miss}}(k)$ | Derived from 3.8; consistent with Elkan (2001) | Elkan printed threshold not inspected | DER; SOURCE NOT FULLY VERIFIED (OI-11) |
| 3.10 | Escalation feasibility | L4 analysis; dominance check | $C_{\text{esc}}$, $C_{\text{FA}}(k)$, $C_{\text{miss}}(k)$ | Derived; Chow (1970) conceptual | Chapter 3 §3.7.5; Chow not read | DER; Chow IV (OI-13) |
| 3.11 | Linear attribution | L4 audit record | $\varphi_{t,i}$, $\varphi_0$, $\overline{x}$ | Lundberg & Lee (2017), adapted | Corollary 1, Property 1 | FV |
| 3.12 | Completeness identity | L4 audit invariant | $\varphi_0$, $\varphi_{t,i}$, $s_t$ | Lundberg & Lee (2017) local accuracy | Property 1 | FV + DER |
| 3.13 | Group attribution | L4 audit record | $\Phi_J$, $I_J$ | Definition | Chapter 3 §3.7.6 | DEF |
| 3.14 | Baseline thresholds | Baseline B1 | $\theta(\alpha)$, $\alpha$, $D_{\text{val}}^{\text{benign}}$ | Definition | Chapter 3 §3.7.7 | DEF |
| 3.15 | Bernoulli LLR | Optional analysis | $\ell_t$, $e_t$, $q_0$, $q_1$ | Basseville & Nikiforov (1993); Reynolds & Stoumbos (1999) | B&N Eq. 2.1.2; R&S not read | FV; R&S IV |
| 3.16 | CUSUM recursion | Optional analysis | $G_t$, $\ell_t$ | Basseville & Nikiforov (1993); Page (1954) | B&N Eqs. 2.2.8–2.2.9; Page Crossref only | FV; Page IV |
| 3.17 | Alarm time | Optional analysis | $T_A$, $h_G$ | Basseville & Nikiforov (1993) | B&N Eq. 2.2.10 | FV |
| 3.18 | False-alarm rate | Optional analysis | $\text{FA}_{\text{ep}}$, $E_{\text{ben}}$, $h_G$ | Definition | Chapter 3 §3.11.10 | DEF |
| 3.19 | Detection delay | Optional analysis | $\tau_d$, $T_A$, $\nu$ | Definition | Chapter 3 §3.11.10 | DEF |
| 3.20 | Expected calibration error | Evaluation | $B_m$, $M$, $N$, $\overline{y}$, $\overline{p}$ | Naeini et al. (2015); Guo et al. (2017) | Both full text | FV |
| 3.21 | Log-loss | Evaluation; $\lambda$ selection | $N$, $y_i$, $p_i$ | Derived from 3.2 | Chapter 3 §3.12.2 | DER |
| 3.22 | Realized loss | Evaluation | $L_e$, $L_d$, $v_i$, $y_i$, $k_i$ | Definition | Chapter 3 §3.12.3 | DEF |

# 12. Algorithm-to-Source Traceability

Evidence level states how deeply the source was read for the use made of it; verification status is the reference-level status from `THESIS_READING_INDEX.md`.

Table: Table 72. Algorithm-to-source traceability

| Algorithm / Method | REM Role | Academic Source | Evidence Level | Verification Status |
|----------------------|-----------------|-----------------------|-------------------|--------------------|
| 1. Provenance labeling and entity extraction | L1 | None (design definition) | Not applicable | DEF |
| 2. Context evidence (classifier; instruction patterns) | L2 | Chennabasappa et al. (2025), candidate classifier only | Abstract | VERIFIED; classifier choice pending |
| 3. Behavioral and action features | L3 | None (design definitions) | Not applicable | DEF |
| 4. Logistic regression | L4 estimation | Cox (1958) | Metadata only | PARTIALLY VERIFIED |
| 5. Ridge-penalized estimation | Offline fitting | le Cessie & van Houwelingen (1992) | Metadata only | PARTIALLY VERIFIED |
| 6. Logistic calibration on the logit | L4 calibration | Platt (1999); Guo et al. (2017); Kull et al. (2017) | Platt not opened; Guo full text; Kull PDF text | Platt PARTIALLY VERIFIED (citation conflict); Guo VERIFIED; Kull VERIFIED |
| 7. Consequence tiering; policy predicates | L4 | None (design definitions) | Not applicable | DEF; tier policy pending |
| 8. Expected-loss verdict selection | L4 | Elkan (2001); Chow (1970) conceptual | Elkan author PDF (Eq. 1); Chow metadata only | Elkan VERIFIED; Chow PARTIALLY VERIFIED |
| 9. Linear Shapley attribution | L4 audit | Lundberg & Lee (2017) | Full text (Properties 1–3, Theorem 1, Corollary 1) | VERIFIED |
| 10. Deterministic mitigation mapping | L5 | None (design definition); Hines et al. (2024) named as non-adopted alternative | Abstract (Hines) | DEF; conflict with design contract |
| 11. Baseline threshold policy | Baseline B1 | None (design definition) | Not applicable | DEF |
| 12. Grouped cross-fitting; group bootstrap | Evaluation; offline fitting | Efron (1979) | Metadata only | PARTIALLY VERIFIED |
| 13. Optional CUSUM analysis | Offline, observe-only | Page (1954); Basseville & Nikiforov (1993); Reynolds & Stoumbos (1999); Lorden (1971); Moustakides (1986) | B&N book text; others metadata or abstract | B&N VERIFIED; others PARTIALLY VERIFIED |
| Evaluation metrics: ECE, log-loss, ROC-AUC, PR-AUC | Evaluation | Naeini et al. (2015); Guo et al. (2017); Fawcett (2006); Davis & Goadrich (2006) | Naeini and Guo full text; Fawcett and Davis metadata only | Naeini VERIFIED; Guo VERIFIED; Fawcett PARTIALLY VERIFIED; Davis & Goadrich PARTIALLY VERIFIED |

# 13. Relation to Prior Work

Chapter 3 states that REM "does not introduce a new learning algorithm or a new decision-theoretic method" and attributes each constituent mechanism to prior work (Table 3.16). The relationships below are taken from Chapters 2 and 3. They are stated factually; the systems are not ranked, and no system is described as better than another. Where a statement about a prior system has no claim-level audit record, this is noted, following the claim-to-paper map of the reading pack.

## 13.1 NEXUS (Hossain et al., 2026)

**Similarities.** Pre-execution evaluation of what the agent proposes; deterministic rules combined with argument-level inspection and a logistic-regression risk score calibrated by Platt scaling; four graduated interventions (allow, block, request confirmation, request revision); auditable decisions traced to a named rule, an argument-inspector finding or a calibrated threshold crossing; a defined expected-loss objective with fixed costs for each intervention.

**Differences recorded in Chapter 2.** NEXUS evaluates plans on author-generated templates; its deployed policy is a rule cascade in which the calibrated score gates certain cases, which Chapter 2 distinguishes from REM's per-decision minimization of conditional risk (Section 7.7).

**Evidence status.** Reference PARTIALLY VERIFIED (metadata conflict between the arXiv identifier and the stated submission date, OI-06). Several claims are supported in Stage 1 from a full-text reading that cannot be reproduced in the current environment. Four numerical figures quoted in Chapter 2 are unverified (OI-02 to OI-05). The relationship between the objective and the deployed policy is open (OI-01).

## 13.2 AgentTrust (C. Yang, 2026)

**Similarities.** Interception of agent tool use; policy rules and analyzer-based risk scoring; session-based chain detection; four verdicts including review (allow, warn, block, review); auditable output of the rules that fired; component ablation with latency; reversibility as part of the labeling rubric.

**Differences recorded in Chapter 2.** Risk is aggregated by maximum severity over the signals that fire; confidence is assigned by a step function of evidence strength rather than by probabilistic calibration; AgentTrust does not use a calibrated probability. Its own ablation found that its session tracker had no measurable effect on its benchmarks.

**Evidence status.** Reference VERIFIED (full text read in Stage 1). The reported figures (170 rules; 95.0%, 73.7% and 96.7% accuracy; 630 scenarios) are verified in the Stage 1 numerical audit; several descriptive sentences have no claim-level audit record.

## 13.3 SafeAgent (H. Liu et al., 2026)

**Similarities.** A runtime controller that mediates actions in the agent loop; stateful decision-making over session history; graduated recovery including human approval; consequence reasoning.

**Differences recorded in Chapter 2.** The decision core's operators (risk encoding, advantage–cost modeling, consequence simulation, policy arbitration) are realized through LLM reasoning rather than formal equations; the action space includes sanitization, replanning, rollback, termination and argument rewriting; the paper does not address probability calibration and does not report latency.

**Evidence status.** Reference VERIFIED (full text read in Stage 1). The comparative-table row is supported; the descriptive and negative statements in Chapter 2's prose have no claim-level audit record.

## 13.4 ProvenanceGuard (She et al., 2026)

**Similarities.** Provenance analysis of tool calls: ProvenanceGuard asks whether a proposed tool call is supported by traceable evidence in the agent's context, which relates directly to REM's argument-provenance feature $x^{\text{act}}_1$.

**Differences.** The Stage 1 prior-art collision matrix records that ProvenanceGuard produces an allow-condition, whereas REM uses provenance as a feature inside a probability model.

**Evidence status.** Reference VERIFIED at abstract level (including the reported reduction of error on misaligned traces from 44.3% to 2.1%). Chapter 3 lists provenance analysis of tool calls as not novel (with Debenedetti et al., 2025).

## 13.5 H.-H. Chen's Authority Frontier Framework (H.-H. Chen, 2026)

**Similarities.** Consequence-dependent control of agent actions before execution: the Actuarial Action Interface prices actions deterministically against reserved capital, and an Authority Frontier measures how much operational authority an agent receives at different budget levels. Chapter 2 states that this work establishes that pricing the consequence of an agent action before execution is not new.

**Differences recorded in Chapter 2.** The work prices consequence without estimating the probability that a specific action was induced by an adversary.

**Evidence status.** Reference VERIFIED at abstract level. The statements that the work does not model an adversarial-inducement probability have no claim-level audit record.

## 13.6 Calibration and Oversight: C. Zhang et al. (2026)

**Relationship.** C. Zhang et al. (2026) argue that oversight based on a scalar risk score routed through a threshold targets the wrong quantity, because what matters for control is the intervention advantage, the expected utility gain from intervening rather than continuing, and two trajectory states can share a risk estimate while differing in recoverability. They propose an action-conditioned controller trained by replaying the agent from identical decision states.

**Position of REM.** REM does not claim that calibration improves control. It reports calibration quality and control outcomes separately, acknowledges that a scalar probability cannot represent whether an adversarial trajectory remains recoverable, and places counterfactual replay outside the scope of the thesis (Chapter 3, Sections 3.1.4 and 3.14).

**Evidence status.** Reference VERIFIED (full text read in Stage 1). The ALFWorld figures quoted in Chapter 2 (ECE 0.463 to 0.006; regret 0.318) are not recorded in the Stage 1 numerical audit, and Chapter 3's statements citing this work have no claim-level audit record.

## 13.7 Other Prior Work Named in Chapter 3

Chapter 3 also attributes runtime interception, human review and graduated response to MI9 (C. L. Wang et al., 2025), provenance analysis of tool calls to CaMeL (Debenedetti et al., 2025), and runtime protection of financial agents to FinHarness (Jia et al., 2026). Chapter 2 describes FinHarness as the closest domain-specific runtime system, combining monitors with verification routed between judges rather than a calibrated probability and declared losses.

Table: Table 73. Mechanisms that Chapter 3 does not claim as novel (Chapter 3, Table 3.16)

| Mechanism | Prior work |
|----------------------------------------------------|------------------------------------------------|
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

# 14. Contribution of the Current Design

Chapter 3 characterizes the contribution as empirical and integrative and states that it "holds only to the extent that the experiments specified in this chapter support it". The components are separated below.

## 14.1 Algorithms from the Literature

Logistic regression (Cox, 1958); ridge regularization (le Cessie & van Houwelingen, 1992); logistic calibration (Platt, 1999; Guo et al., 2017; Kull et al., 2017); linear Shapley attribution (Lundberg & Lee, 2017); expected-cost decisions and the reject option (Elkan, 2001; Chow, 1970); cumulative sum change detection (Page, 1954; Basseville & Nikiforov, 1993); the bootstrap (Efron, 1979); expected calibration error (Naeini et al., 2015; Guo et al., 2017). None is claimed as new.

## 14.2 Security Concepts from Prior Work

The indirect prompt injection threat (Greshake et al., 2023; OWASP Gen AI Security Project, 2025); provenance analysis of tool calls (She et al., 2026; Debenedetti et al., 2025); runtime interception, human review and graduated response (H. Liu et al., 2026; C. Yang, 2026; C. L. Wang et al., 2025); calibrated logistic risk scores and four-way intervention (Hossain et al., 2026); consequence-aware and consequence-priced control (H.-H. Chen, 2026; Hossain et al., 2026; C. Yang, 2026); the distinction between calibration and control (C. Zhang et al., 2026); and pitfalls of machine learning in security evaluation (Arp et al., 2022).

## 14.3 Shared Architectural Concepts

Runtime interception of agent actions, graduated verdicts that include human review, hybrids of rules and learned scores, calibrated logistic risk scores, and component ablations that report latency are all present in the reviewed literature (Chapter 2, synthesis of Section 2.4). REM shares these concepts.

## 14.4 Composition Specific to REM

The investigated contribution is the design and evaluation, on the AgentDojo banking environment under indirect prompt injection, of a non-invasive five-layer runtime layer that combines (Chapter 3, Section 3.13):

- provenance-based evidence about proposed financial actions;
- a calibrated per-step probability of adversarial induction;
- verdict selection over Allow, Modify, Escalate and Block by minimizing conditional risk with losses declared per consequence tier;
- deterministic mitigation whose effectiveness is measured and used in the loss structure.

Because NEXUS also defines an expected-loss objective, the distinction of this composition from NEXUS rests on the per-decision use of expected loss, which is subject to OI-01. Non-invasiveness is a design requirement still to be demonstrated (AS-1).

## 14.5 Financial-Agent Specialization

The specialization to financial agents consists of the classification of banking tools by consequence (Table 3), the consequence descriptors (amount, recurring-payment change, credential change, declared irreversibility), the illustrative tier policy (pending supervisor approval), the entity types extracted (such as IBAN-formatted account identifiers and monetary amounts), the destination-novelty and sensitive-egress features, and the declared set $\mathcal{T}_R$. Runtime protection of financial agents is itself not claimed as new (Jia et al., 2026).

## 14.6 Evaluation and Measurement Aspects

The evaluation design compares REM with a consequence-independent baseline on the same estimator; reports cost-free primary metrics (attack success rate, benign utility, utility under attack, intervention rates, step false-positive rate, residual ASR under Modify, escalation rate, latency), and never reports ASR without the utility metrics; reports realized loss only across a declared grid that includes misspecified costs; reports both an idealized-reviewer and a no-reviewer bound for escalation; uses nested grouped cross-fitting; and performs seven ablations.

## 14.7 Explicitly Not Claimed

Chapter 3 explicitly does not claim a new algorithm; the first runtime guardrail, the first calibrated agent risk score or the first consequence-aware controller; that calibration improves control; robustness against adaptive adversaries; any prevention guarantee; or validity in production financial deployment.

# 15. Limitations and Open Issues

No issue in this section is resolved by this document.

## 15.1 Specification Conflicts Requiring Supervisor Decision

Table: Table 74. Specification conflicts

| ID | Conflict | Chapter 3 | Other project record | Status |
|-------|----------------|---------------|-------------------------------------------|-----------------|
| SC-1 | Mitigation semantics | Modify removes a tool class for the rest of the episode; Block restricts every tool in $\mathcal{T}_R$ for the rest of the episode (Table 3.14, L536–L538) | `CLAUDE.md` Mitigation Lock: step-level semantics; episode-level restriction is a separate experimental policy requiring explicit specification. `RECONCILIATION.md` C7 and `STAGE2_BLOCKED_DECISIONS.md` record tool restriction as a conflict / excluded. Prototype is step-level only. | SUPERVISOR DECISION REQUIRED |
| SC-2 | Tie-breaking | Ties resolved toward the more restrictive verdict, Block ⪰ Escalate ⪰ Modify ⪰ Allow (Equation 3.7; design definition) | Project `README.md` and prototype: no tie-break rule is frozen; an exact tie raises `VerdictTieError` | SUPERVISOR DECISION REQUIRED |

## 15.2 Open Evidence Issues

Table: Table 75. Open evidence issues relevant to Chapter 3 (identifiers from THESIS_READING_INDEX.md, Section 6)

| ID | Issue | Current evidence | Still needed |
|---------|------------------------------|-----------------------------------|--------------------------|
| OI-01 | NEXUS: relationship between its expected-loss objective and its deployed rule-cascade policy | Stage 1 full-text reading (claims Ch2-C024, Ch2-C028 supported); not reproducible here; the "not a per-decision minimization" sentence has no claim-level record | Full-text reading of the NEXUS objective and decision-procedure sections |
| OI-02 | NEXUS "99 plan features" (N038) | Unverified; index descriptions refer to nine deterministic rules | Feature count in the NEXUS method section |
| OI-03 | NEXUS ECE 0.085 to 0.013 on a 128-instance test set (N039) | Unverified; 128 consistent with index descriptions | Calibration results in the paper |
| OI-04 | NEXUS 60-instance calibration split (N040) | Unverified | Calibration split in the paper |
| OI-05 | NEXUS 300/63/128 split (N067) | Stage 1 records disagree (supported in one workbook, unverified in another) | Dataset split in the paper |
| OI-06 | NEXUS arXiv identifier vs stated submission date | Chapter citation fields match index records; conflict is in the source's record | arXiv version history |
| OI-07 | Platt 1999/2000 citation conflict | Crossref registers the MIT Press chapter at pp. 61–74 as "Probabilities for SV Machines" (2000); the cited title and year differ; no 1999 report number confirmed | The volume or a confirmed record of the 1999 item; Platt's printed parameterization |
| OI-09 | Brier (1950) scoring convention | Crossref record matches; paper not read; Chapter 3 defers the Brier score | The paper's definition |
| OI-10 | le Cessie & van Houwelingen (1992) penalty scaling constant | Crossref record matches; formulation not read | Printed penalized log-likelihood |
| OI-11 | Elkan (2001) printed threshold expression | Author PDF read for cost convention and Eq. (1) only | Threshold expression and its equation number |
| OI-12 | Cox (1958) printed formulation | Crossref record matches; paper not read | Printed model |
| OI-13 | Chow (1970) reject rule | Crossref record matches; paper not read | Statement of the error–reject tradeoff |
| OI-14 | AgentDojo pinned version | Counts confirmed from package source and version-stable; task content differs between versions | The version or commit used in the experiments |
| CF-01 | Davis & Goadrich (2006) — PR-AUC | Metadata only | Paper content |
| CF-02 | Efron (1979) — bootstrap | Metadata only | Paper content |
| CF-03 | Fawcett (2006) — ROC-AUC | Metadata only | Paper content |
| CF-04 | Hevner et al. (2004) — design science | Metadata only | Paper content |
| CF-05 | Peffers et al. (2007) — six activities | Metadata only | Paper content |
| CF-06 | Page (1954) — CUSUM recursion | Metadata only | Printed recursion |
| CF-07 | Reynolds & Stoumbos (1999) — Bernoulli CUSUM | Metadata only | Paper content |
| CF-08 | Lorden (1971) — asymptotic optimality | Abstract only; assumptions not read | Conditions of the result |
| CF-09 | Moustakides (1986) — optimality of Page's stopping time | Abstract only; assumptions not read | Conditions of the result |

OI-08 of the reading index (Jackson, 2025) concerns a source cited only in Chapter 2 and not used in this summary; it is therefore omitted here.

## 15.3 Equations with Incomplete Source Verification

Equation 3.1 (Cox, IV); Equation 3.2 (le Cessie & van Houwelingen, IV, penalty constant pending); Equation 3.3 (Platt, NC, citation conflict); Equation 3.9 (attribution of the printed threshold to Elkan not inspected; the derivation itself is verified); Equation 3.10 (Chow, IV; conceptual attribution only); Equation 3.15 (Reynolds & Stoumbos, IV); Equation 3.16 (Page, IV).

## 15.4 Assumptions Not Empirically Validated

- AS-1 (interception without modifying the agent) and AS-2 (reliable source attribution): to be demonstrated.
- AS-3 (the adversary cannot modify REM): assumed; stated as a limitation.
- AS-6 (non-adaptive adversaries): declared limitation.
- AS-7 (observable evidence separates induced from benign actions): tested in pilot E0.
- AS-8 (representative benign reference data): threatened by benchmark scope.
- AS-9 (bounded LLM non-determinism): measured through repeated runs.
- Assumption A-Mod underlying Equation 3.5.
- A reviewer who resolves escalations correctly (bounded by the no-reviewer bound).
- Approximate linearity of the log-odds in the evidence (Equation 3.1).
- Feature independence in the interpretation of attributions as Shapley values.
- The conditions of the sequential-analysis optimality results, which are not claimed to hold for agent trajectories.
- Declared costs, which cannot be validated empirically and are reported across a grid.

## 15.5 Design Items Pending Supervisor Decision (as Stated in Chapter 3)

Confirmation of RQ1–RQ4; the injection-classifier choice; the consequence tier policy; labeling of induced read steps; the LLM backbone(s) and attack templates; the user-task grouping sensitivity analysis; configurations B2 (detection-only) and distributed defences; the pilot E0 decision values; the number of repeated runs; inclusion of the optional sequential analysis and its indicator set.

## 15.6 Implementation Elements Not Specified in Chapter 3

These are listed in Section 8.3 (Table 69) and Section 9.

## 15.7 Threats to Validity Recorded in Chapter 3

- **Construct validity:** derived step labels can be wrong; the idealized reviewer overstates the protective value of Escalate; declared costs cannot be validated empirically; a low ASR can reflect task failure rather than protection (Y. Wang et al., 2026).
- **Internal validity:** template dependence remains after grouping; features designed with knowledge of the benchmark may fit its style; LLM non-determinism.
- **External validity:** one simulated banking environment with benchmark-authored attacks; results may not transfer to other benchmarks, whose conclusions can disagree (M. Q. Li et al., 2026), or to production systems; dependence on the LLM backbone; FinVault is not used because its preprint was withdrawn.
- **Statistical conclusion validity:** few independent task templates; wide intervals; no power analysis.
- **Security-specific threats:** every evidence feature can be evaded individually; REM's configuration and logs are assumed protected; a scalar probability cannot represent whether an adversarial trajectory remains recoverable (C. Zhang et al., 2026).

## 15.8 Claim-Level Audit Coverage

The Stage 1 claim audit sampled claims rather than checking every sentence. The claim-to-paper map of the reading pack records which Chapter 3 statements have a claim-level audit record. Among those without one are the statements that auditable decision records are provided by existing systems (L506, citing Hossain et al. and C. Yang), that Kull et al. prove the equivalence used in Section 6.5 (L355), and the three statements citing C. Zhang et al. (L357, L525, L936). Absence of a claim-level record is not evidence against a statement; it identifies statements still to be checked against the source.

# 16. Executive Technical Summary

**What is REM?** REM (Runtime Evaluation and Mitigation) is a runtime mediation layer placed between one LLM-based agent and its environment. It evaluates each tool call the agent proposes before the call is released and decides whether to allow it, modify it, escalate it to a human reviewer, or block it. It is designed for tool-using financial agents threatened by indirect prompt injection, and it is evaluated on the AgentDojo banking environment. It treats the agent as opaque: it observes inputs, context, proposed actions and tool results, but not model parameters or internal reasoning, and it does not modify the agent. That this interception is achievable without modifying the agent is an assumption to be demonstrated.

**How does it work?** REM has exactly five layers. The Input & Context Layer captures the step's inputs and the proposed action and labels every context segment by provenance (trusted, semi-trusted or untrusted), with derived content inheriting the least-trusted label. The Detection Layer computes evidence about untrusted content: a fixed prompt-injection classifier score and an instruction-pattern indicator. The Behavioral Analysis Layer tracks the episode history and computes four behavioral features and three action features, including whether a key argument of the proposed action (such as a recipient account) appears only in untrusted content. The Decision Engine estimates a calibrated probability that the action is adversarially induced, assigns a consequence tier, applies two deterministic predicates, selects a verdict and writes an audit record. The Mitigation Layer executes the verdict. Offline fitting and recalibration are cross-cutting activities between deployments, not a layer; REM's parameters never change within an episode.

**What algorithms does it use?** Ridge-penalized logistic regression estimates the probability of adversarial induction (Cox, 1958; le Cessie & van Houwelingen, 1992). A two-parameter logistic calibration on the logit, with a positive slope, calibrates it (Platt, 1999; Guo et al., 2017; Kull et al., 2017); beta calibration and isotonic regression are not adopted. An expected-loss decision rule selects the verdict (adapted from Elkan, 2001, with Chow, 1970, as conceptual basis for escalation). A linear Shapley attribution of the logit is written to the audit record and never influences the verdict (Lundberg & Lee, 2017). A consequence-independent threshold policy serves only as the baseline comparator. A cumulative sum analysis is optional, offline and observe-only, and outside the verdict path.

**How is the mathematical decision formulated?** The logit $s_t = \beta_0 + \beta^{\top}x_t$ is calibrated to $p_t = \sigma(\gamma_1 s_t + \gamma_0)$. The action's consequence descriptors determine a tier $k_t$, which indexes a declared loss structure $L(v, y, k)$. For each feasible verdict the conditional risk $R_t(v) = (1 - p_t)L(v, 0, k_t) + p_t L(v, 1, k_t)$ is computed, and the verdict minimizing it is issued. A prohibited action is always blocked, and missing required evidence at high tiers leads to escalation. Thresholds follow from declared costs — for example, the Allow–Block threshold $p^{\text{*}}_{k} = C_{\text{FA}}(k) / (C_{\text{FA}}(k) + C_{\text{miss}}(k))$ — rather than being chosen independently. The loss of Modify on an induced action uses a measured residual attack-success rate.

**How is it implemented?** Chapter 3 specifies the per-step runtime algorithm and the offline fitting procedure; Chapter 4 describes the implementation. Parameters are fitted by nested grouped cross-fitting (nine leave-one-injection-task-out outer folds) on traces collected in observe-only mode, because the benchmark does not support independent training, calibration, validation and test partitions. The software stack, interception mechanism, latency budget, failure handling of REM itself and all declared policy values are not specified in the current Chapter 3.

**What are its documented contributions?** Chapter 3 claims no new algorithm and attributes every mechanism to prior work. The contribution is empirical and integrative: the design and evaluation, on a financial benchmark, of a non-invasive five-layer runtime layer combining provenance-based evidence, a calibrated per-step probability of adversarial induction, tier-indexed expected-loss verdict selection over four verdicts, and deterministic mitigation whose measured effectiveness enters the loss structure. Its evaluation isolates the decision rule by comparing against a baseline on the same estimator and reports cost-dependent results only across a declared loss grid. The closest prior system, NEXUS, also uses a calibrated logistic risk score, four interventions and a defined expected-loss objective; Chapter 2 distinguishes REM by NEXUS's rule-cascade deployed policy, a distinction whose evidence remains open.

**What are its current limitations?** The contribution holds only to the extent that the planned experiments support it. The evaluation uses one simulated banking environment, non-adaptive adversaries and a small number of task templates. Declared costs cannot be validated empirically. Several source attributions are not fully verified (Cox, le Cessie & van Houwelingen, Platt, Chow, Page, Reynolds & Stoumbos), the Platt 1999/2000 citation conflict is unresolved, and four NEXUS figures quoted in Chapter 2 are unverified. Chapter 3's episode-level Modify and Block semantics conflict with the project design contract, and its tie-breaking rule diverges from the prototype; both require a supervisor decision. Several design items, including the classifier, the tier policy, the loss values, the backbones and the pinned benchmark version, remain pending.

# References Used in This Summary

The entries below are the reference entries of the current Chapter 3, reproduced exactly as they appear there; every source cited in this summary is among them. The verification status and basis recorded in the project records follow each entry. No entry has been corrected in this summary.

## Academic Sources (36)

::: {custom-style="Reference Entry"}
Arp, D., Quiring, E., Pendlebury, F., Warnecke, A., Pierazzi, F., Wressnegger, C., Cavallaro, L., & Rieck, K. (2022). Dos and don'ts of machine learning in computer security. In *31st USENIX Security Symposium*. USENIX Association. https://arxiv.org/abs/2010.09470
:::

::: {custom-style="Reference Note"}
*Verification: VERIFIED. Stage 1: arXiv abstract (claim used is in the abstract).*
:::

::: {custom-style="Reference Entry"}
Basseville, M., & Nikiforov, I. V. (1993). *Detection of abrupt changes: Theory and application*. Prentice Hall. https://people.irisa.fr/Michele.Basseville/kniga/
:::

::: {custom-style="Reference Note"}
*Verification: VERIFIED. Stage 1: Author-hosted PDF text: eqs. 2.1.2, 2.2.8-2.2.10 read.*
:::

::: {custom-style="Reference Entry"}
Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review, 78*(1), 1–3. https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2
:::

::: {custom-style="Reference Note"}
*Verification: PARTIALLY VERIFIED. Crossref record matches every cited field (Stage 2); paper not read. Chapter 3 defers the Brier score until its convention is confirmed (OI-09).*
:::

::: {custom-style="Reference Entry"}
Chen, H.-H. (2026). *Insuring every action: An authority frontier framework for runtime actuarial control of autonomous AI agents* (arXiv:2605.25632) [Preprint]. arXiv. https://arxiv.org/abs/2605.25632
:::

::: {custom-style="Reference Note"}
*Verification: VERIFIED. Stage 1: arXiv abstract.*
:::

::: {custom-style="Reference Entry"}
Chennabasappa, S., Nikolaidis, C., Song, D., Molnar, D., Ding, S., Wan, S., Whitman, S., Deason, L., Doucette, N., Montilla, A., Gampa, A., de Paola, B., Gabi, D., Crnkovich, J., Testud, J.-C., He, K., Chaturvedi, R., Zhou, W., & Saxe, J. (2025). *LlamaFirewall: An open source guardrail system for building secure AI agents* (arXiv:2505.03574) [Preprint]. arXiv. https://arxiv.org/abs/2505.03574
:::

::: {custom-style="Reference Note"}
*Verification: VERIFIED. Stage 1: arXiv abstract (components).*
:::

::: {custom-style="Reference Entry"}
Chow, C. K. (1970). On optimum recognition error and reject tradeoff. *IEEE Transactions on Information Theory, 16*(1), 41–46. https://doi.org/10.1109/TIT.1970.1054406
:::

::: {custom-style="Reference Note"}
*Verification: PARTIALLY VERIFIED. Crossref record matches (Stage 1 and Stage 2); reject rule not read (OI-13).*
:::

::: {custom-style="Reference Entry"}
Cox, D. R. (1958). The regression analysis of binary sequences. *Journal of the Royal Statistical Society: Series B (Methodological), 20*(2), 215–232. https://doi.org/10.1111/j.2517-6161.1958.tb00292.x
:::

::: {custom-style="Reference Note"}
*Verification: PARTIALLY VERIFIED. Crossref record matches (Stage 1 and Stage 2); model formulation not read (OI-12).*
:::

::: {custom-style="Reference Entry"}
Davis, J., & Goadrich, M. (2006). The relationship between precision-recall and ROC curves. In *Proceedings of the 23rd International Conference on Machine Learning* (pp. 233–240). ACM. https://doi.org/10.1145/1143844.1143874
:::

::: {custom-style="Reference Note"}
*Verification: PARTIALLY VERIFIED. Stage 1: Crossref metadata only.*
:::

::: {custom-style="Reference Entry"}
Debenedetti, E., Shumailov, I., Fan, T., Hayes, J., Carlini, N., Fabian, D., Kern, C., Shi, C., Terzis, A., & Tramèr, F. (2025). *Defeating prompt injections by design* (arXiv:2503.18813) [Preprint]. arXiv. https://arxiv.org/abs/2503.18813
:::

::: {custom-style="Reference Note"}
*Verification: VERIFIED. Stage 1: arXiv abstract (77% vs 84%).*
:::

::: {custom-style="Reference Entry"}
Debenedetti, E., Zhang, J., Balunović, M., Beurer-Kellner, L., Fischer, M., & Tramèr, F. (2024). *AgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents* (arXiv:2406.13352). arXiv. https://arxiv.org/abs/2406.13352
:::

::: {custom-style="Reference Note"}
*Verification: VERIFIED. Stage 1: arXiv abstract; banking suite read in the public repository.*
:::

::: {custom-style="Reference Entry"}
Efron, B. (1979). Bootstrap methods: Another look at the jackknife. *The Annals of Statistics, 7*(1). https://doi.org/10.1214/aos/1176344552
:::

::: {custom-style="Reference Note"}
*Verification: PARTIALLY VERIFIED. Stage 1: Crossref metadata only.*
:::

::: {custom-style="Reference Entry"}
Elkan, C. (2001). The foundations of cost-sensitive learning. In *Proceedings of the Seventeenth International Joint Conference on Artificial Intelligence (IJCAI-01)*. https://cseweb.ucsd.edu/~elkan/rescale.pdf
:::

::: {custom-style="Reference Note"}
*Verification: VERIFIED. Author PDF read for the cost convention and Eq. (1) (Stage 1); pp. 973–978 confirmed from dblp and ACM DL records (Stage 2) and not shown in the working chapter entry; printed threshold not inspected (OI-11).*
:::

::: {custom-style="Reference Entry"}
Fawcett, T. (2006). An introduction to ROC analysis. *Pattern Recognition Letters, 27*(8), 861–874. https://doi.org/10.1016/j.patrec.2005.10.010
:::

::: {custom-style="Reference Note"}
*Verification: PARTIALLY VERIFIED. Stage 1: Crossref metadata only.*
:::

::: {custom-style="Reference Entry"}
Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., & Fritz, M. (2023). Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection. In *Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security* (pp. 79–90). ACM. https://doi.org/10.1145/3605764.3623985
:::

::: {custom-style="Reference Note"}
*Verification: VERIFIED. Stage 1: Crossref metadata and arXiv abstract.*
:::

::: {custom-style="Reference Entry"}
Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. In *Proceedings of the 34th International Conference on Machine Learning* (Vol. 70, pp. 1321–1330). PMLR. https://proceedings.mlr.press/v70/guo17a.html
:::

::: {custom-style="Reference Note"}
*Verification: VERIFIED. Stage 1: ar5iv full text: calibration definition, ECE bins, Platt form, NLL fit.*
:::

::: {custom-style="Reference Entry"}
Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly, 28*(1), 75–106. https://doi.org/10.2307/25148625
:::

::: {custom-style="Reference Note"}
*Verification: PARTIALLY VERIFIED. Stage 1: Crossref metadata only.*
:::

::: {custom-style="Reference Entry"}
Hines, K., Lopez, G., Hall, M., Zarfati, F., Zunger, Y., & Kiciman, E. (2024). *Defending against indirect prompt injection attacks with spotlighting* (arXiv:2403.14720) [Preprint]. arXiv. https://arxiv.org/abs/2403.14720
:::

::: {custom-style="Reference Note"}
*Verification: VERIFIED. Stage 1: arXiv abstract (>50% to <2%).*
:::

::: {custom-style="Reference Entry"}
Hossain, E., Nipu, M. M. H., Ornee, T. N., Rana, R., & Yousefi, N. (2026). *NEXUS: Structured runtime safety for tool-using LLM agents* (arXiv:2607.19356) [Preprint]. arXiv. https://arxiv.org/abs/2607.19356
:::

::: {custom-style="Reference Note"}
*Verification: PARTIALLY VERIFIED. Full HTML text read in Stage 1; not reproducible in the current environment. The arXiv identifier conflicts with the stated 25 May 2026 submission date (OI-06). Open items OI-01 to OI-05.*
:::

::: {custom-style="Reference Entry"}
Jia, H., Liu, Y., Chong, B., Yang, Y., Chen, Y., Liang, J., Li, Q., Lu, H., Xu, K., Zheng, H., Zhang, C., Peng, H., & Yu, P. S. (2026). *FinHarness: An inline lifecycle safety harness for finance LLM agents* (arXiv:2605.27333) [Preprint]. arXiv. https://arxiv.org/abs/2605.27333
:::

::: {custom-style="Reference Note"}
*Verification: VERIFIED. Stage 1: arXiv abstract (components and numbers).*
:::

::: {custom-style="Reference Entry"}
Kull, M., Silva Filho, T., & Flach, P. (2017). Beta calibration: A well-founded and easily implemented improvement on logistic calibration for binary classifiers. In *Proceedings of the 20th International Conference on Artificial Intelligence and Statistics* (Vol. 54, pp. 623–631). PMLR. https://proceedings.mlr.press/v54/kull17a.html
:::

::: {custom-style="Reference Note"}
*Verification: VERIFIED. Stage 1: PMLR PDF text: monotonicity constraint and Proposition 1.*
:::

::: {custom-style="Reference Entry"}
le Cessie, S., & van Houwelingen, J. C. (1992). Ridge estimators in logistic regression. *Applied Statistics, 41*(1), 191–201. https://doi.org/10.2307/2347628
:::

::: {custom-style="Reference Note"}
*Verification: PARTIALLY VERIFIED. Crossref record matches (Stage 1 and Stage 2; Crossref stores the first page only); penalty formulation not read (OI-10).*
:::

::: {custom-style="Reference Entry"}
Li, M. Q., Fung, B. C. M., Li, B., Ismail, H., & Iqbal, F. (2026). *Taxonomy and consistency analysis of safety benchmarks for AI agents* (arXiv:2605.16282) [Preprint]. arXiv. https://arxiv.org/abs/2605.16282
:::

::: {custom-style="Reference Note"}
*Verification: VERIFIED. Stage 1: arXiv abstract (hooks, TTL decay, preliminary results).*
:::

::: {custom-style="Reference Entry"}
Liu, H., Ilyushin, E., Ni, J., & Zhu, M. (2026). *SafeAgent: A runtime protection architecture for agentic systems* (arXiv:2604.17562) [Preprint]. arXiv. https://arxiv.org/abs/2604.17562
:::

::: {custom-style="Reference Note"}
*Verification: VERIFIED. Stage 1: Full HTML text read.*
:::

::: {custom-style="Reference Entry"}
Lorden, G. (1971). Procedures for reacting to a change in distribution. *The Annals of Mathematical Statistics, 42*(6), 1897–1908. https://doi.org/10.1214/aoms/1177693055
:::

::: {custom-style="Reference Note"}
*Verification: PARTIALLY VERIFIED. Stage 1: Project Euclid abstract read 2026-09-22 (identity and asymptotic-optimality statement confirmed); independence and known-distribution assumptions not read.*
:::

::: {custom-style="Reference Entry"}
Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. In *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1705.07874
:::

::: {custom-style="Reference Note"}
*Verification: VERIFIED. Stage 1: ar5iv full text: Properties 1-3, Theorem 1, Corollary 1.*
:::

::: {custom-style="Reference Entry"}
Moustakides, G. V. (1986). Optimal stopping times for detecting changes in distributions. *The Annals of Statistics, 14*(4). https://doi.org/10.1214/aos/1176350164
:::

::: {custom-style="Reference Note"}
*Verification: PARTIALLY VERIFIED. Stage 1: Project Euclid abstract read 2026-09-22 (identity confirmed; Page's stopping time shown optimal in a defined sense); assumptions not read.*
:::

::: {custom-style="Reference Entry"}
Naeini, M. P., Cooper, G., & Hauskrecht, M. (2015). Obtaining well calibrated probabilities using Bayesian binning. *Proceedings of the AAAI Conference on Artificial Intelligence, 29*(1). https://doi.org/10.1609/aaai.v29i1.9602
:::

::: {custom-style="Reference Note"}
*Verification: VERIFIED. Stage 1: PMC full text: ECE definition read.*
:::

::: {custom-style="Reference Entry"}
Page, E. S. (1954). Continuous inspection schemes. *Biometrika, 41*(1–2), 100–115. https://doi.org/10.1093/biomet/41.1-2.100
:::

::: {custom-style="Reference Note"}
*Verification: PARTIALLY VERIFIED. Stage 1: Crossref metadata only.*
:::

::: {custom-style="Reference Entry"}
Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems, 24*(3), 45–77. https://doi.org/10.2753/MIS0742-1222240302
:::

::: {custom-style="Reference Note"}
*Verification: PARTIALLY VERIFIED. Stage 1: Crossref metadata only.*
:::

::: {custom-style="Reference Entry"}
Platt, J. C. (1999). Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. In A. J. Smola, P. Bartlett, B. Schölkopf, & D. Schuurmans (Eds.), *Advances in large margin classifiers* (pp. 61–74). MIT Press.
:::

::: {custom-style="Reference Note"}
*Verification: PARTIALLY VERIFIED. UNRESOLVED CITATION CONFLICT (OI-07). Crossref registers the MIT Press chapter at pp. 61–74 as "Probabilities for SV Machines" by John C. Platt, published 2000 (DOI 10.7551/mitpress/1113.003.0008). The cited title and year differ from that record, and no report number for a 1999 item could be confirmed. The entry is reproduced exactly as cited in Chapter 3.*
:::

::: {custom-style="Reference Entry"}
Reynolds, M. R., Jr., & Stoumbos, Z. G. (1999). A CUSUM chart for monitoring a proportion when inspecting continuously. *Journal of Quality Technology, 31*(1), 87–108. https://doi.org/10.1080/00224065.1999.11979900
:::

::: {custom-style="Reference Note"}
*Verification: PARTIALLY VERIFIED. Stage 1: Crossref metadata only.*
:::

::: {custom-style="Reference Entry"}
She, Y., Liang, Y., & Kang, E. (2026). *Safeguarding LLM agents from misalignment through provenance analysis* (arXiv:2607.01236) [Preprint]. arXiv. https://arxiv.org/abs/2607.01236
:::

::: {custom-style="Reference Note"}
*Verification: VERIFIED. Stage 1: arXiv abstract (44.3% to 2.1%).*
:::

::: {custom-style="Reference Entry"}
Wang, C. L., Singhal, T., Kelkar, A., & Tuo, J. (2025). *MI9: An integrated runtime governance framework for agentic AI* (arXiv:2508.03858) [Preprint]. arXiv. https://arxiv.org/abs/2508.03858
:::

::: {custom-style="Reference Note"}
*Verification: VERIFIED. Stage 1: arXiv abstract (six components).*
:::

::: {custom-style="Reference Entry"}
Wang, Y., Han, X., Shang, D., Tang, Y., & Liu, B. (2026). *Safety, or just capability? A validity audit of agent-safety benchmarks* (arXiv:2607.28685) [Preprint]. arXiv. https://arxiv.org/abs/2607.28685
:::

::: {custom-style="Reference Note"}
*Verification: VERIFIED. Stage 1: arXiv abstract.*
:::

::: {custom-style="Reference Entry"}
Yang, C. (2026). *AgentTrust: Runtime safety evaluation and interception for AI agent tool use* (arXiv:2605.04785) [Preprint]. arXiv. https://arxiv.org/abs/2605.04785
:::

::: {custom-style="Reference Note"}
*Verification: VERIFIED. Stage 1: Full HTML text read.*
:::

::: {custom-style="Reference Entry"}
Zhang, C., Wan, Z., Yu, X., Wu, J., Wen, Q., Zhou, P., Zhao, W., & Tsang, I. (2026). *Calibration is not control: Why LLM-agent oversight needs intervention* (arXiv:2606.21399) [Preprint]. arXiv. https://arxiv.org/abs/2606.21399
:::

::: {custom-style="Reference Note"}
*Verification: VERIFIED. Stage 1: Full HTML text read.*
:::

## Other Source (1)

The following industry resource is cited by Chapter 3 for the definition of indirect prompt injection. It is not an academic publication.

::: {custom-style="Reference Entry"}
OWASP Gen AI Security Project. (2025). *LLM01:2025 Prompt injection*. OWASP Foundation. https://genai.owasp.org/llmrisk/llm01-prompt-injection/
:::

::: {custom-style="Reference Note"}
*Verification: VERIFIED. Stage 1: Official page read.*
:::

