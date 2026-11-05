# CHAPTER FIVE

# CONCLUSIONS AND RECOMMENDATIONS

## 5.1 Introduction

This chapter draws the conclusions of the thesis. Section 5.2 answers the research questions from the evidence of Chapter 4; Section 5.3 assesses the objectives; Section 5.4 separates the contributions achieved from those proposed; Section 5.5 summarises the limitations discussed in Section 4.16; Section 5.6 gives recommendations and future work ordered by dependency; and Section 5.7 concludes. Every conclusion is bounded by the exploratory status of the evidence: recorded traces, observe-only decisions and a replay that assumes the agent does not adapt. No live-agent result exists (Section 4.12).

## 5.2 Answers to the Research Questions

**Table 5.1. Evidence summary**

| RQ | Kind of evidence | What was observed | Not shown |
|---|---|---|---|
| RQ1 | Held-out predictions | ROC-AUC 0.94 overall; 0.86–0.98 per held-out attacker objective; 0.92–0.96 on other templates; 0.74–1.00 per held-out backbone. ECE 0.044, degraded on the unseen credential-change category. No calibration improvement observed | Performance on other benchmarks or live agents |
| RQ2 | Observe-only decisions; replay | REM intervened on more attack steps than B1 and on many more legitimate state-changing steps. The difference stems mainly from tier-indexed costs, not from the escalation option. In replay, REM's ASR was lower than B1's under both mitigation semantics (mostly credential and payment attacks; Table 4.11), at a utility cost of −18 to −20 points without a reviewer and about 0 with an oracle reviewer | Enforcement against live or adaptive agents |
| RQ3 | Replay; runtime measurement | r~mod~ and residual ASR ≈ 0 under NO-ADAPT (assumption-driven); escalation 19.6% of steps; REM complete-call processing per step: median 0.21–0.28 ms, 95th percentile 0.49–0.70 ms in this configuration (R4); earlier values are partial | Residual success of live agents after Modify; full-system latency |
| RQ4 | Held-out predictions; observe-only; replay | Action evidence dominates. No improvement observed from the instruction-pattern indicator or from behavioral evidence, which lowered utility. Tiers drive the trade-off | General claims about context or behavioral evidence |
## 5.3 Achievement of the Objectives

**Table 5.2. Objectives and how far they were achieved**

| Objective | Achieved | Not achieved |
|---|---|---|
| **O1.** Design a REM framework for financial AI agents' and task automation agents' security | Designed (Chapter 3) and implemented (Section 3.16) for a financial (banking) agent; design values declared for exploration | Supervisor-approved design values; any task-automation setting; the injection classifier |
| **O2.** Evaluate the framework against adversarial attacks | Exploratory evaluation on recorded attacks against 21 real agents: offline classification, observe-only decisions, replay sensitivity (Chapter 4) | Enforcing-mode evaluation with live agents; repeated runs; human label audit; adaptive attacks |
| **O3.** Compare performance with existing security approaches | Controlled comparison with a same-estimator baseline (B1) and a same-escalation-opportunity variant; recorded outcomes of four distributed defenses for orientation | A controlled comparison with any published defense (NEXUS, AgentTrust, FinHarness or the distributed defenses) on a shared protocol |

O1 is achieved for the banking setting. O2 and O3 are partly achieved: the evidence is exploratory, and the decisive experiment, enforcement with live agents, was not run.

## 5.4 Contributions

**Achieved, with their evidence:**
1. **A specified and implemented composition.** It comprises:
   - provenance-based evidence;
   - a ridge estimator calibrated on the logit;
   - consequence tiers and policy predicates;
   - a four-verdict expected-loss rule with a feasible set and a dominance check;
   - deterministic mitigation under two stated semantics;
   - an audit record whose attribution cannot reach the verdict.

   Undeclared design values stop the software. *Evidence:* Chapter 3; 205 tests.
2. **An evaluation protocol that isolates the decision rule.** REM, the baseline and the same-escalation variant share the estimator, calibration and predicates. Grouped cross-fitting holds out whole attacker objectives, and every fitted quantity, including the feature set, is fitted within the fold. *Evidence:* Chapter 4 and its exact reproduction.
3. **Exploratory evidence on recorded real-agent traces.** The evidence covers:
   - discrimination on unseen attacker objectives;
   - the observed absence of calibration and behavioral-feature benefit;
   - a quantified protection–utility trade-off and its dependence on reviewer availability and on declared costs.

   *Evidence:* exploratory; one benchmark; no live enforcement.

**Proposed in Chapter 3 but not achieved:** an evaluation of enforcement against live agents, which is necessary to support any claim that REM reduces attack success in operation. Until it is run, the central practical claim of the thesis, that tier-indexed expected-loss verdicts reduce financial harm at acceptable utility cost, remains **unestablished**.

**Not claimed:**
- a new learning, calibration or decision-theoretic method;
- prevention guarantees;
- robustness to adaptive attackers;
- operational readiness;
- superiority over the systems of Table 4.17.

## 5.5 Limitations

The limitations are discussed in full in Section 4.17. In summary, the conclusions of this thesis are bounded by:

1. **Design status.** Costs, tiers, predicates, the feature set and the label rule are declared exploratory values, not approved ones.
2. **No live evaluation.** Enforcement was estimated only by replay under NO-ADAPT. The closed-loop harness is implemented and tested but was not executed with a language model (Section 4.12).
3. **One benchmark and one attack family for fitting**, one attacker identity, and historical model snapshots.
4. **Labels** that are reference-matched attempt labels, ambiguous for one user task in early suite versions, and not audited by a human.
5. **Statistics**: nine attacked groups, one run per configuration, and no correction for multiple comparisons.
6. **Reviewer**: escalation outcomes are bounded by an idealized reviewer and by no reviewer; no real reviewer was modeled.
7. **Missing component**: no injection classifier was available for the Detection Layer.
8. **Literature**: the review was conducted at record level, without full-text screening.

## 5.6 Recommendations and Future Work, Ordered by Dependency

1. **Decisions** (`SUPERVISOR_DECISIONS_REQUIRED`): approve or replace the declared design values, the label rule, the mitigation semantics and the replay scope amendment.
2. **Label audit.** Annotate the prepared package (`results/pilot_R2/label_audit_human_package.csv`) with at least one human annotator, and preferably two. Report agreement and revise the label rule if needed.
3. **Live enforcing-mode evaluation**, required for the central claim:
   - run B0, B1, REM and REM without expected-loss Escalate with live backbones;
   - use at least three repeated runs;
   - fix and record the benchmark version, model versions, decoding parameters and costs.

   This measures adaptive agent behavior after refusals and the true residual success after Modify, and shows how the two mitigation semantics differ once the agent can react to refusals; in replay they already differ, because episode-level restrictions also refuse later, different calls (Chapter 4, Table 4.11).
4. **A reviewer model** with error rate and delay, so that the utility cost of escalation can be estimated between the two bounds.
5. **Feature revision.** Revise the behavioral features, for example by conditioning privilege escalation on provenance, and add the injection classifier, selected on the agent's own tool outputs at a low false-positive rate (Z. Liu, 2026). Then re-run Pilot E0 on new fitting data.
6. **Elicited costs.** Repeat the decision analysis with costs elicited from a financial-institution context, rather than declared.
7. **Full-text literature review.** Complete the review by searching the named databases and screening full texts, and re-examine the unverified properties of the closest systems.
8. **Further benchmarks and adaptive attacks**, reported per benchmark.

## 5.7 Conclusion

This thesis set out to design a runtime framework that decides, for each tool call proposed by a financial AI agent, whether to allow, modify, escalate or block it. The decision minimizes expected loss under a calibrated probability of adversarial inducement and a declared consequence tier, and every verdict is recorded for audit. The framework was specified, implemented at the tool boundary of a benchmark agent, and evaluated in an exploratory study of 6,762 tool calls proposed by 21 real LLM agents.

**What was observed:**
- The evidence available at the tool boundary separates attack attempts from legitimate calls well on attacker objectives not seen in fitting, mainly through evidence about the action's arguments.
- With the costs declared for exploration, the expected-loss rule intervenes on nearly all attack attempts, and also on most legitimate high-consequence actions. Whether that is acceptable depends on a human reviewer that the benchmark does not provide.
- Calibration and the behavioral features produced no observed improvement.

These findings come from recorded traces and from a replay that assumes the agent does not adapt. They do not show that REM protects a live agent. The experiment needed to show that, enforcement with live agents, is the first item of future work, and the thesis does not claim its result in advance.
