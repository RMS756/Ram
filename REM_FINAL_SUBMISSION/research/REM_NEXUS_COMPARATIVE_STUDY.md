# REM and NEXUS: comparative study

**Date:** 11 November 2026. **The NEXUS paper's full text has not been read.** The comparison rests on two verified sources below the level of the paper and says so cell by cell.

## 1. Evidence available

| Code | Source | What it is | Retrieved |
|---|---|---|---|
| **A** | Abstract of the published version: "NEXUS: Structured Runtime Safety for Tool-Using LLM Agent(s)", Hossain et al. (five authors), Findings of AACL 2026, DOI 10.18653/2026.findings-aacl.112 | index record with abstract | 11 November 2026 (scholarly index) |
| **A0** | Abstract of the earlier preprint, arXiv:2607.19356 | index record | 28 October 2026 (recorded in Chapter 2) |
| **R** | README of the authors' public repository | `REM_FINAL_THESIS/verification/sources_R4/nexus_README.md`, sha256 `a48e7de8…` | 1 November 2026 |
| — | Paper full text | **not read**: `aclanthology.org` and `arxiv.org` are blocked in this session; the earlier attempt of 21 September (`V1_NEXUS_DIRECT_VERIFICATION.md`) failed for the same reason | — |
| — | Repository code, fitted scorer, benchmarks | **not accessed**: only the README was retrieved | — |

A README can differ from the paper. Where A and R disagree, both are given.

Correction to the thesis record: the reference list cites the preprint; the published version (Findings of AACL 2026) must be cited.

## 2. What NEXUS is, with the level of each statement

| Statement | Level |
|---|---|
| A structured-plan safety monitor applying a formal intervention policy Π to select among allow, block, request confirmation, request revision | A, R |
| Combines deterministic safety rules, argument-level inspection, and a calibrated logistic-regression risk score for graded escalation | A, R |
| Π operates on a structured plan representation and selects one intervention **per plan** | R |
| Rule set covers permission, irreversible action, sensitive-data exposure, network access, resource budget, suspicious patterns; the argument inspector covers credentials, sensitive paths, table and field names, suspicious URLs | R |
| Risk score ρ trained on a 9-dimensional plan feature vector; Platt-scaled on a 60-instance calibration split | R |
| Policy: Block if any critical violation; Block if ρ ≥ τ_b and at least one violation; Confirm if ρ ≥ τ_c or any high-severity violation; Revise if any medium-severity violation; otherwise Allow | R |
| (τ_b, τ_c) = (0.75, 0.70), selected on a safety–utility loss L(Π) = E[λ_s·u_s + λ_o·u_o + λ_c·c(Π(P))] over a 5×5 grid of (λ_s, λ_o) | R |
| Platt scaling reduces ECE from 0.085 to 0.013 on the 128-instance test split | R |
| Synthetic 128-instance benchmark: F1 0.949, four-class intervention accuracy 0.6406, +27.3 points over rule-only selection | A (R gives 0.965 and 0.945 for a retrained scorer) |
| R-Judge: F1 0.861 against 0.849 rule-only; AgentHarm: matches rule-only; indirect-injection set: 0% attack success at 99% control allow | A |
| Rule-blind NEXUS-Stress: F1 0.897 with Revise recall 0.500 | A (A0: 0.881; R: 0.836 with four-class accuracy 0.420, and the note that Π predicts only Allow or Block on rule-blind plans) |
| Median latency 0.38 ms | A (A0: 0.205 ms) |
| Code, benchmarks and the calibrated scorer are released | A |
| The feature definitions, the intervention costs c(·), the utility terms u_s and u_o, the fitting procedure, and the stated limitations | **not established** (paper not read) |

## 3. Comparison

| Dimension | REM | NEXUS | Level for NEXUS | Assessment |
|---|---|---|---|---|
| Interception level | each proposed tool call, before execution | a structured plan; one intervention per plan | A, R | **Different.** REM sees calls one at a time with the episode history; NEXUS judges a plan. |
| Feature construction | provenance of call arguments against tool outputs and the user's request; behavioural counters; action type and amount (eight features) | 9-dimensional plan feature vector; rules and an argument inspector act beside it | R | Different inputs. Whether any NEXUS feature encodes provenance of arguments is not established. |
| Risk estimation | ridge logistic regression | logistic regression | A | Same family. |
| Calibration | Platt-type map on the logit, fitted out of fold | Platt scaling on a held-out calibration split | R | Same method. |
| Decision-rule structure | every call: argmin of expected loss over four verdicts; predicates as hard constraints | rule-first cascade; the score enters through two fixed thresholds | R | **Different.** In REM the boundaries between verdicts follow from cost ratios and change with the consequence tier. In NEXUS rules decide first and two thresholds, chosen once by a loss criterion, apply to all plans. |
| Consequence awareness | explicit: C_miss depends on a four-level consequence tier, so the same probability yields different verdicts | through rule severities (critical, high, medium) and rules for irreversible actions | R | Both use consequence. REM puts it in the loss; NEXUS puts it in the rules. |
| Intervention semantics | Allow; Modify (tool-restriction notice for the call); Escalate (withhold pending review); Block | allow; block; request confirmation; request revision | A | Close: Escalate ≈ request confirmation. Modify and "request revision" differ. |
| Runtime overhead | median 0.23 ms per decision in replay, p95 0.6 ms (under multi-process load) | median 0.38 ms | A | Same order; different machines and inputs. |
| Evaluation benchmarks | AgentDojo banking: recorded trajectories of real agents, 5,426 eligible episodes | synthetic plans (128-instance test split), an indirect-injection set, a stress set, R-Judge, AgentHarm | A | **Not comparable.** Different units and tasks. |
| Security–utility measurement | attack success, unauthorized state change, task completion, legitimate-call release, by replay of outcomes | F1 for unsafe-plan detection; four-class intervention accuracy against labelled interventions; over-block and control-allow rates | A, R | Different constructs. NEXUS's intervention accuracy needs a labelled correct intervention per plan; REM has none and measures outcomes. |
| Held-out attack objective | yes (nine folds; double holdout; confirmatory population) | external and rule-blind sets; whether attack objectives are held out from scorer training is not established | A | — |
| A finding in common | Modify, Escalate and Block are not distinguishable in the evaluation | on rule-blind plans the policy predicts only Allow or Block | R | Both report that the graded middle interventions are hard to exercise. |

## 4. Equal-conditions experiment: not attempted

A faithful run needs four things. None is satisfied.

| Requirement | Status |
|---|---|
| NEXUS code and fitted scorer at a pinned commit | Not in this container; the repository is outside the session's allowed scope |
| Paper full text, to confirm that the code path matches the published method | Not read |
| A valid adapter from an AgentDojo tool call (or trajectory prefix) to NEXUS's structured plan, including the annotations its rules read | Does not exist. Writing it requires choices (what is a "plan" for a single call; how permission, irreversibility and sensitivity annotations are assigned to banking tools) that change the method's inputs |
| A decision on scorer use | Applying the released scorer unchanged is a transfer test of NEXUS; refitting it on AgentDojo is a NEXUS-style method, not NEXUS |

Re-implementing NEXUS from its README inside this project and reporting it as NEXUS would be a fabricated comparator. **No NEXUS experiment was run and none is reported.** The comparison is architectural and methodological only.

## 5. Consequences for the thesis

1. REM is an instance of the same family as NEXUS. "Calibrated logistic risk score + rules or predicates + four graduated interventions" is published.
2. The differences that can be stated are: per-call versus per-plan mediation; an expected-loss rule over all four verdicts with tier-dependent costs versus a rule-first cascade with two fixed thresholds; and outcome-based evaluation on recorded banking trajectories versus label-based evaluation on synthetic plans. Each is stated at the level A or R shown above, never as a reading of the paper.
3. No claim that either design is better is supported.
4. Chapter 2 cites the published version, keeps the level labels, and states that the full text was not read. Register items OI-01 to OI-06 stay open.

## 6. Request

The published PDF (ACL Anthology) is needed from the candidate to replace levels A and R by a full-text reading before submission.
