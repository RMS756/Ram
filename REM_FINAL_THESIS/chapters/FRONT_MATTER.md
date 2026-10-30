---
title: "Runtime Evaluation and Mitigation (REM): A Security Framework for Financial AI Agents"
subtitle: "Working title as supplied by the author; no approved title is on record (decision D-12)"
author:
  - "A thesis submitted in partial fulfilment of the requirements for the degree of Master of Science in Cybersecurity (Cyberspace Security)"
  - "Al-Balqa Applied University — Faculty of Artificial Intelligence — Department of Intelligent Systems"
  - "Student: [NAME NOT SUPPLIED]"
  - "Supervisor: Dr. Husam Fakhouri"
date: "Final verification draft R3 — 30 October 2026 — for supervisor review"
lang: en-GB
toc-title: "Table of Contents"
abstract-title: "Abstract"
abstract: |
  Tool-using agents built on large language models can now initiate payments, change account details and send data to external recipients. Indirect prompt injection is content placed in a tool output or a retrieved document that the agent then follows. It can make such an agent propose a financial action that serves an attacker rather than the user.

  This thesis designs, implements and evaluates the Runtime Evaluation and Mitigation (REM) framework. REM is a five-layer runtime layer placed at the tool-execution boundary. For each proposed tool call, it:

  - estimates the probability that the call was adversarially induced, using ridge logistic regression calibrated on the logit;
  - assigns a declared consequence tier;
  - applies policy predicates;
  - selects one of four verdicts (Allow, Modify, Escalate or Block) by minimising expected loss under tier-indexed costs;
  - records every verdict for audit, with an attribution that cannot influence the verdict.

  Each constituent mechanism is established in prior work. The contribution is the combination and its evaluation.

  The framework was implemented in Python and verified by 193 automated tests. It was evaluated in an exploratory study on recorded traces of 21 real LLM agents in the AgentDojo banking environment: 3,334 episodes and 6,762 proposed tool calls. The evaluation used nested grouped cross-fitting, which holds out whole attacker objectives. An independent re-execution reproduced every analytical result.

  On held-out attacker objectives, the evidence available at the tool boundary separated attack attempts from legitimate calls (pooled ROC-AUC 0.938). Most of this separation came from evidence about the action's arguments. Calibration produced no observed improvement. The behavioral features were not specific to attacks in this benchmark.

  With the declared exploratory costs, the expected-loss rule intervened on 97.3% of attack steps and on 22.7% of legitimate steps, against 74.0% and 5.6% for a baseline that uses the same estimator but ignores consequences. In a replay that assumes the agent does not adapt to refusals, REM's attack success rate was 0.004, against 0.055 for the baseline. Without a reviewer, this came at a loss of about 20 points of benign utility. With an idealised reviewer, the loss disappeared.

  These results are exploratory. They do not show protection of a live or adaptive agent. That would require an enforcing-mode experiment with live agents, which remains future work.

  **Keywords:** AI agent security; indirect prompt injection; runtime monitoring; financial AI agents; tool-use security; probability calibration; expected-loss decision; human escalation; AgentDojo.
---

# Status of This Document {.unnumbered}

This is the R3 verification draft. It was produced for **supervisor review**. It is **not** a version for formal submission. The reasons are stated in the submission-readiness report that accompanies it and are summarised here:

- The design values used in the evaluation (costs, consequence tiers, predicates, feature set and label rule) are declared exploratory values. None has been approved by the supervisor.
- The evaluation is exploratory. It rests on recorded traces of real agents and on a replay analysis that assumes the agent does not adapt to refusals. No live enforcing-mode experiment was executed.
- The university's thesis template and the approved proposal were not available. The formatting is therefore provisional, and the title, student name, committee and approval pages are left to be completed from official records.
- Open decisions are listed in `UNRESOLVED_ITEMS_AND_SUPERVISOR_DECISIONS.md`.

- An AI coding assistant (Claude Code) was used in this project, as recorded in the project files and the repository history. It assisted with the literature screening records, the software and tests, the execution of the analyses, the AI-only label inspection (Chapter 5, Section 5.10), and the drafting and verification of this text. The university's declaration of AI use, if one is required, must be completed by the author. This note is a factual record, not that declaration.

No acknowledgment, declaration, approval or signature page is included. These pages require information and statements that only the author and the university can provide.

# List of Abbreviations {.unnumbered}

| Abbreviation | Meaning |
|---|---|
| AP | Average precision (an estimate of the area under the precision–recall curve) |
| ASR | Attack success rate |
| AUC | Area under the curve |
| B0, B1 | No-defense configuration; consequence-independent baseline with the same estimator |
| CUSUM | Cumulative sum (sequential change detection) |
| D1, D2 | Policy predicates: prohibited action; missing required evidence |
| ECE | Expected calibration error |
| FPR | False-positive rate |
| IPI | Indirect prompt injection |
| LLM | Large language model |
| NLL | Negative log-likelihood |
| NO-ADAPT | Assumption that a replayed agent does not adapt to REM's refusals |
| PRISMA | Preferred Reporting Items for Systematic Reviews and Meta-Analyses |
| REM | Runtime Evaluation and Mitigation framework |
| ROC | Receiver operating characteristic |
| RQ | Research question |
| SC | Specification conflict (supervisor decision register) |
| TB | Trust boundary |
