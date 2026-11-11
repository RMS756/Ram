# REM and NEXUS: comparative study

**Date:** 11 November 2026. **Status of the NEXUS evidence: abstract and index record only.**

## 1. What could and could not be verified

| Item | Status |
|---|---|
| Bibliographic record | Verified through a scholarly index: "NEXUS: Structured Runtime Safety for Tool-Using LLM Agents", Findings of AACL 2026, DOI 10.18653/2026.findings-aacl.112; earlier preprint arXiv:2607.19356. The thesis reference list still carries the preprint and must be updated to the published version. |
| Abstract | Read (index copy). |
| Full text | **Not read.** `aclanthology.org` and `arxiv.org` are blocked in this session; the paper is not in the repository. An earlier attempt (21 September, `V1_NEXUS_DIRECT_VERIFICATION.md`) failed for the same reason. |
| Published implementation | The abstract states that code is released. **The repository was not accessed**; its location is not recorded in this project. |
| Mathematical policy | **Not verified.** The form of the intervention rule is not established from the abstract. |

Consequence: the comparison below is at the level of the abstract. Cells that would need the full text say "not established". This is not a full-text verification and must not be presented as one.

## 2. What the abstract establishes

- Components: a deterministic rule set for explicit safety violations; an argument inspector for sensitive values and risky inputs; a calibrated logistic-regression risk scorer for graded escalation; a session manager for cross-turn state.
- Actions: allow, block, request confirmation, request revision.
- Role of the score: the calibrated score is described as an arbitration signal inside the intervention policy; when exactly one critical rule fires, it decides between a hard block and a request for confirmation.
- Evaluation: a 128-instance synthetic benchmark (F1 0.949; four-class intervention accuracy 0.6406, reported as 27.3 points above rule-only intervention selection); a rule-blind stress set (F1 0.881); CPU latency of 0.38 ms.

## 3. Comparison

| Dimension | REM | NEXUS (abstract level) | Assessment |
|---|---|---|---|
| Interception level | each proposed tool call, before execution | plan-level or call-level: **not established** (earlier project notes describe the score as ρ(P), a score of a plan P; unverified) | Open until the full text is read |
| Feature construction | provenance of call arguments against tool outputs and the user objective; behavioural counters; action type and amount | rule firings and argument inspection; the scorer's features are **not established** | REM's provenance features are computed from the episode context; whether NEXUS uses provenance is not established |
| Risk estimation | ridge logistic regression on eight features | logistic regression | Same model family |
| Calibration | Platt-type map on the logit, fitted out of fold | "calibrated"; method **not established** | Same intent |
| Decision-rule structure | every call: argmin of expected loss over four verdicts, with policy predicates as hard constraints | rules first; the score arbitrates in a stated case | **Different on the abstract's description**: REM derives all four verdicts from one cost-based rule; NEXUS is described as rule-led with score-gated demotion. Whether NEXUS defines a loss or utility is not established. |
| Consequence awareness | explicit: C_miss varies by a four-level consequence tier | **not established** | Possibly the main structural difference; unverified |
| Intervention semantics | Allow; Modify (one declared mechanism); Escalate (withhold pending review); Block | allow; block; request confirmation; request revision | Close correspondence: Escalate ≈ request confirmation; Modify and "request revision" differ (REM modifies the call; NEXUS asks the agent to revise) |
| Runtime overhead | median 0.23 ms per decision in replay (p95 0.6 ms), measured under multi-process load | 0.38 ms on CPU | Same order; measured on different machines and inputs, not comparable in detail |
| Evaluation benchmark | AgentDojo banking recordings of real agents; 5,426 eligible episodes | 128 synthetic instances and a stress set | **Not comparable**: different units (episodes with outcomes versus labelled instances) |
| Security–utility measurement | attack success, unauthorized state change, task success, legitimate-call release, all in replay | F1 and four-class intervention accuracy against labels | Different constructs. NEXUS's intervention accuracy presupposes a labelled correct intervention per instance; REM has no such label and measures outcomes |
| Held-out attack objective | yes | **not established** | — |

## 4. Equal-conditions experiment: not attempted

An equal-conditions comparison needs (i) the NEXUS implementation, (ii) its rule set and fitted scorer or training data, and (iii) an adapter that maps AgentDojo tool calls to NEXUS's input without changing its method. None of the three is available in this session. Re-implementing NEXUS from its abstract and calling it NEXUS would be a fabrication of a comparator. **No NEXUS experiment was run and none is reported.**

What would be needed to run it later: the full text; the released code at a pinned commit; confirmation of whether NEXUS scores plans or calls; and a decision on whether its synthetic-benchmark scorer may be applied unchanged to AgentDojo calls (a transfer test) or must be refitted (which would then be a NEXUS-style method, not NEXUS).

## 5. Consequences for the thesis

1. REM must be positioned as an instance of the same family as NEXUS, not as a first combination of calibrated scoring and four graduated actions.
2. The differences that can be stated today are limited to: the unit and kind of evaluation data, and the description of the decision rule in the abstract. Consequence tiers and the expected-loss formulation may be differences; this is unverified and must be worded as such.
3. Chapter 2 must cite the published version and keep the "abstract-level" label until the full text is read. Items OI-01 to OI-06 of the decision register remain open.
4. The thesis must state that no experimental comparison with NEXUS exists.

## 6. Request

The full text (ACL Anthology PDF) is needed from the candidate. With it, Section 3 can be completed in under a day, and the feasibility of an adapter can be judged.
