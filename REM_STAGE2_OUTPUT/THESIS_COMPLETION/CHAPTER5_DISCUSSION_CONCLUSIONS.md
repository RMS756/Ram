# CHAPTER FIVE

# DISCUSSION, CONCLUSIONS, LIMITATIONS, AND FUTURE WORK

This chapter interprets the evidence reported in Chapter 4, relates it to the research objectives and to prior work, and states the conclusions that the evidence supports. The evidence base is narrower than the evaluation designed in Chapter 3. Chapter 4 established two facts. First, the mathematical core of the REM Decision Engine and the step-level mitigation mapping are implemented and verified by 154 passing tests. Second, no empirical evaluation has been executed: no result exists for attack success, utility, calibration, discrimination, intervention behavior or latency. The discussion is therefore confined to what an implemented and tested design can support. Every statement about security effectiveness is marked as intended or as not yet demonstrated.

## 5.1 Interpretation of Findings

### 5.1.1 What the evidence establishes

The evidence of Chapter 4 supports four findings. Each concerns the properties of the implemented software, not its effect on an agent.

1. **The decision path of Chapter 3 can be realized as specified.** The implemented operations compute:
   - the logit and uncalibrated probability of Equation 3.1;
   - the calibrated probability of Equation 3.3 with a positive slope;
   - the conditional risk of Equation 3.6 and the minimum-risk verdict of Equation 3.7.

   They are verified against hand-computed values (Chapter 4, Section 4.6). The core of the decision rule is therefore expressed directly in the chosen method rather than in a rule cascade, heuristic aggregation or LLM arbitration.

2. **The separation of quantities that Chapter 3 requires is enforced in code.**
   - The decision engine accepts only a probability that has passed through calibration.
   - It rejects attribution output.
   - It refuses to act without a consequence tier.
   - It records the full table of conditional risks with every verdict.

   These properties correspond to Chapter 3's requirements that the calibrated probability, not the raw score, enter the decision (Section 3.7.2), that attribution never influence the verdict (Section 3.7.6), and that the verdict be reproducible from the audit record (SO-5). They are verified by tests (Chapter 4, Sections 4.6.2–4.6.5).

3. **The implementation refuses to substitute undeclared design values.** Where a loss value, tier, predicate policy, feature definition, ridge penalty or Modify mechanism is missing, the software stops rather than using a default (Chapter 4, Sections 4.2.5 and 4.14). This refusal is itself evidence. It shows that no result produced later by this code could have been driven by a value that the thesis did not declare. It also means that no such result exists yet.

4. **The five-layer architecture is preserved in code.** Exactly five layers are declared, and no feedback or risk-score layer exists (Chapter 4, Section 4.2.3). The assignment of components to layers in the code differs from Chapter 3 (SC-6).

### 5.1.2 What the evidence does not establish

The evidence does not establish any of the following:

- that REM reduces the success of indirect prompt injection against a financial agent;
- that it preserves benign utility;
- that its probabilities are calibrated on agent data;
- that its evidence features discriminate adversarially induced actions;
- that consequence-tiered verdicts change outcomes relative to a consequence-independent baseline;
- that its per-step latency is acceptable.

These were the purposes of the evaluation specified in Chapter 3 (Sections 3.11–3.12), and that evaluation has not been executed (Chapter 4, Sections 4.8–4.15).

The pipeline test in which a fixture step following an injected instruction does not receive Allow (Chapter 4, Section 4.12.2) is not evidence of protection. Its features, tier and losses are test fixtures that the test file declares are not design values. It shows only that the implemented stages are connected in the specified order.

### 5.1.3 Status of the analytical results of Chapter 3

Chapter 3 derives several properties of the decision rule analytically:

- the pairwise indifference thresholds (Equation 3.8);
- the Allow–Block threshold as a function of declared costs (Equation 3.9);
- the condition under which Escalate can be selected (Equation 3.10);
- the dominance check (Section 3.7.5).

These derivations follow from Equation 3.6 under the stated loss structure and are classified in Chapter 3 as derived (DER). The source attributions of Equations 3.9 and 3.10 remain incomplete (SOURCE NOT FULLY VERIFIED). The derivations are not empirical findings, and nothing in Chapter 4 tests them against data. Their practical relevance depends on loss values that have not been declared (SD-1) and on the resolution of the tie-breaking conflict SC-2. The tie order is used at the boundary cases of Equation 3.10 in Chapter 3.

## 5.2 Relationship to Research Objectives

The approved objectives are O1–O3 (Chapter 3, Section 3.1.2). The research questions RQ1–RQ4 were derived from them in Chapter 3 and are presented there for supervisor confirmation. They remain proposed ([PD]). Table 5.1 maps each objective and question to the evidence that exists.

Table: Table 5.1. Research objectives and questions against available evidence

| Objective / question | Evidence available | Status |
|---|---|---|
| O1: Design a REM framework for financial AI agents' and task automation agents' security | Chapter 3 design; Chapter 4 implementation of the decision core, mitigation mapping, audit record and fail-closed configuration | Partly met. Design specified; implementation partial (Chapter 4, Table 4.17); task-automation environments outside the evaluation scope (Chapter 3, Section 3.1.2) |
| O2: Evaluate the framework against adversarial attacks | None | Not met. PLANNED — NOT EXECUTED |
| O3: Compare performance with existing security approaches | None; baselines B0, B1 and B2 not implemented | Not met. PLANNED — NOT EXECUTED |
| RQ1, estimation [PD] | None | RESULT NOT AVAILABLE |
| RQ2, decision [PD] | None | RESULT NOT AVAILABLE |
| RQ3, mitigation and cost [PD] | None; the Modify mechanism is undeclared and its semantics are in conflict (SC-1) | RESULT NOT AVAILABLE |
| RQ4, component contribution [PD] | None; the calibration ablation is in conflict (SC-3) | RESULT NOT AVAILABLE |

Chapter 3 also states six security objectives (Section 3.3.7). Table 5.2 records how far each is supported at present. Here, "supported in code" means that the implemented software has the stated property on test inputs. It does not mean that the objective has been achieved for an agent.

Table: Table 5.2. Security objectives of Chapter 3 against available evidence

| Security objective | Supported in code | Demonstrated on an agent |
|---|---|---|
| SO-1 Use evidence about untrusted content entering through TB-2 | No: context features not implemented | No |
| SO-2 Detect actions whose arguments originate in untrusted content or deviate from the benign pattern | No: behavioral and action features not implemented | No |
| SO-3 Account for the consequence of the proposed action | Partly: the decision rule accepts a tier-indexed loss; tiers and losses not declared | No |
| SO-4 Provide human escalation | Partly: Escalate withholds the action; no reviewer workflow | No |
| SO-5 Emit an audit record from which the verdict can be reproduced | Yes: per-step record with the full risk table; verdict source for predicates missing | No |
| SO-6 Preserve benign utility and report per-step latency | No: no measurement | No |

## 5.3 Comparison with Prior Work

A comparison of outcomes with prior systems is not possible, because REM has produced no outcomes. The comparison below is therefore at the level of design. It restates the positions documented in Chapter 2 and does not rank systems. A property listed for a prior system is one reported in the sources consulted for Chapter 2. A property listed for REM is one specified in Chapter 3, with its implementation status from Chapter 4.

Table: Table 5.3. Design-level comparison with the closest prior work (from Chapter 2; no ranking implied)

| System | Documented design (Chapter 2) | Relation to REM as specified | REM implementation status |
|---|---|---|---|
| NEXUS (Hossain et al., 2026) | Deterministic rules, argument inspection and a logistic-regression risk score calibrated by Platt scaling. Defines an expected-loss objective with fixed costs for allow, revise, confirm and block. Its deployed policy is a rule cascade in which the calibrated score gates certain cases. Evaluates plans before execution on author-generated templates | Shares calibrated logistic scoring and a four-way intervention set. Differs in selecting each verdict by per-decision minimization of conditional risk with tier-indexed losses, and in evaluating each proposed tool call of an executing agent. The account of how NEXUS relates its expected-loss objective to its deployed cascade rests on a Stage 1 reading that could not be reproduced (OI-01). The NEXUS numerical claims remain unverified (OI-02 to OI-05) | Per-decision minimization implemented; losses and tiers not declared; no agent evaluation |
| AgentTrust (C. Yang, 2026) | Normalization, pattern features, configurable policy rules, analyzer risk scoring, session chain detection, optional LLM judgment. Maximum-severity aggregation. Four verdicts (allow, warn, block, review). Confidence by a step function of evidence strength | Shares runtime interception, a four-verdict set including review, and component ablation with latency as an evaluation practice. Differs in using a calibrated probability and declared losses rather than rule severity | Decision core implemented; no ablation or latency measured |
| SafeAgent (H. Liu et al., 2026) | Runtime controller with a decision core whose operators are realized through LLM reasoning; broad action space including human approval | Shares runtime mediation and human approval. Differs in using a formal decision rule rather than LLM arbitration, which the REM design lock excludes | Formal rule implemented; no comparison possible |
| ProvenanceGuard (She et al., 2026) | Asks whether a proposed tool call is supported by traceable evidence in the agent's context | Chapter 3 draws on the same question for its argument-provenance evidence (Table 3.9) and does not claim provenance analysis as new (Table 3.16) | Provenance features not implemented |
| H.-H. Chen (2026) | Prices the consequence of an agent action deterministically against reserved capital | Shares consequence-dependent control. Differs in combining consequence with an estimated probability that the action was adversarially induced | Consequence tiers not implemented |
| FinHarness (Jia et al., 2026) | Financial-agent runtime system with query and tool monitors and a judge cascade | Shares the financial domain and runtime placement. Differs in decision mechanism: calibrated probability and declared losses rather than judge routing | No financial-environment evaluation executed |
| C. Zhang et al. (2026) | Shows that calibrating a scalar risk score can leave control regret under threshold routing unchanged | REM does not claim that calibration improves control and reports calibration and control separately (Chapter 3, Section 3.7.2). REM inherits the limitation that a scalar probability does not represent recoverability (Section 3.14) | Neither calibration nor control measured |

Two observations follow from the comparison.

- **Each individual mechanism in REM has precedent in the reviewed work**, as Chapter 2 concludes (Section 2.13) and Chapter 3 records (Table 3.16).
- **The distinguishing features of REM are compositional.** Chapter 3 specifies:
  - selection among four verdicts by minimizing conditional risk under a calibrated per-step probability and tier-indexed losses;
  - evaluation against a baseline that uses the same estimator but ignores consequence;
  - the financial action boundary of an executing agent.

  Only the first of these is implemented, and none has been evaluated. Consequently, the thesis cannot at present claim that this composition performs differently from the prior systems.

## 5.4 Security Implications

The security implications of the current evidence are limited, and they must be separated from the protection that REM is designed to provide. Table 5.4 makes the separation explicit.

Table: Table 5.4. Demonstrated properties and intended protection

| Aspect | Demonstrated (software level, on test inputs) | Intended (Chapter 3), not demonstrated |
|---|---|---|
| Decision integrity | The verdict is a deterministic function of the calibrated probability, the tier and a sourced, complete loss grid; the risk table is recorded; attribution cannot alter it | Verdicts that reduce financial harm at acceptable utility cost |
| Fail-closed behavior | Missing design inputs stop the system rather than defaulting | Behavior under missing evidence at runtime through predicate D2 (not implemented) |
| Untrusted content | Content is carried verbatim; provenance defaults to unlabeled | Provenance labeling and context evidence that reflect TB-2 content (not implemented) |
| Action boundary | Block removes the proposed tool call from the step; Escalate withholds it | Prevention of adversarially induced transfers, payee changes and credential changes in AgentDojo (not executed) |
| Auditability | Per-step record with evidence, probabilities, tier, risks, verdict, mitigation and attribution; digests by default | An audit record usable by a human reviewer under Escalate (no reviewer workflow) |

For a financial agent, the demonstrated properties are necessary conditions for trustworthy mediation, not sufficient ones. They ensure that a verdict can be traced to declared quantities. They do not ensure that the quantities are adequate or that the evidence detects attacks. Chapter 3 states that every evidence feature can be evaded individually and that adversaries are assumed non-adaptive (Section 3.14). No claim of robustness or prevention is made.

## 5.5 Limitations

The limitations of the thesis at its present state are grouped below. None of them is resolved in this chapter.

**Missing experiments.** None of the following has been executed:

- the observe-only and enforcing runs;
- pilot E0;
- the configurations B0, B1, REM and B2;
- the seven ablations;
- the mitigation-effectiveness runs;
- the latency measurements.

All metrics of Chapter 3, Table 3.15, and Section 3.12.2 are RESULT NOT AVAILABLE.

**Implementation maturity.** The following specified parts are not implemented (Chapter 4, Table 4.17):

- the Input & Context operations;
- the Detection and Behavioral Analysis evidence;
- the consequence tiers and predicates;
- the loss structure and dominance check;
- the feasible verdict set;
- the baseline threshold policy;
- the offline fitting procedure;
- the AgentDojo integration.

Assumption AS-1, interception without modifying the agent, has not been demonstrated.

**Unresolved specification conflicts.** Six conflicts between Chapter 3 and the implementation or the design lock remain open:

- SC-1: mitigation semantics;
- SC-2: tie-breaking;
- SC-3: the calibration ablation;
- SC-4: the calibration fitting;
- SC-5: the Brier score;
- SC-6: the layer mapping.

Whether the Chapter 3 specifications are approved as frozen (SD-FREEZE), and the chapter structure of the thesis (SD-STRUCT), are also undecided. Several parts of the design depend on these decisions: the justification of the tie order, the definition of r_mod(k), and the meaning of RQ3 and RQ4.

**Dataset size and threat coverage.** The planned evaluation uses one banking suite with 16 user-task and 9 injection-task templates, as reported in Chapter 3 and still to be re-confirmed. Eight of the nine injection tasks share one attacker account. Most attacker objectives require one call. The evaluated attack class is indirect prompt injection through tool outputs, and adaptive adversaries are excluded. Chapter 3 anticipates wide intervals and no statistical power analysis (Sections 3.11.4, 3.11.9).

**External validity.** Results from one simulated environment may not transfer to other benchmarks, backbones or production systems (Chapter 3, Section 3.14). No production deployment is in scope.

**Computational measurement.** No latency has been measured. The dominant cost, the fixed prompt-injection classifier, has not been chosen.

**Reference verification.** The following remain open:

- 15 of the 37 Chapter 3 references are partially verified;
- the Platt citation conflict OI-07;
- the NEXUS evidence issues OI-01 to OI-06;
- the source verification of Equations 3.1, 3.2, 3.3, 3.9, 3.10, 3.15 and 3.16;
- four sources cited in code with no verification record.

**Missing records.** There is no approved proposal, decision ledger or authoritative equation registry on record.

## 5.6 Threats to Validity

The threats below are discussed only to the extent that the present study supports them. They concern the verification evidence of Chapter 4. The threats to the planned evaluation are those stated in Chapter 3, Section 3.14. They cannot be assessed until that evaluation is run.

**Internal validity.**

- The verification tests were written together with the implementation. They verify the properties their authors chose to check.
- The pipeline tests use fixture components rather than the specified ones.
- A passing test shows that the code behaves as the test expects. It does not show that the expectation matches Chapter 3. Where the two differ, the difference has been recorded as a conflict (SC-1 to SC-6) rather than treated as an error in either.

**Construct validity.** The count of passing tests measures agreement between code and tests, not security. Treating it as a measure of protection would be a construct error, and this chapter does not do so.

**External validity.** The verification results hold for the environment recorded in Chapter 4 (Python 3.11.15, NumPy 2.4.6). Behavior under other versions has not been checked.

**Reproducibility.**

- The verification results are reproducible from the commit and the commands listed in Chapter 4, Table 4.14.
- The implementation records a digest of the design lock, the configuration digests, the seed and the dependency versions in an environment manifest (Chapter 4, Table 4.9). This mechanism would support the reproducibility of the planned experiments, but it has not yet recorded an experimental run.
- Project reporting of test counts contained an error in the past (Chapter 4, Table 4.16, F-10). The figures in this thesis are taken from the evidence files, not from earlier reports.

## 5.7 Practical Implications

REM is not ready for deployment, and nothing in this thesis supports its use to protect a production financial agent. Its possible practical relevance lies in the pattern it specifies: a mediation layer at the tool-call boundary in which an estimated probability of adversarial inducement and a declared consequence tier are combined through an explicit loss structure, with a reproducible audit record for every verdict.

For this pattern to be usable in practice, at least the following conditions would have to hold. Each is an assumption or open item of Chapter 3, not an established fact:

- the agent framework exposes each proposed tool call and each tool result for interception without modification of the agent (AS-1);
- content can be attributed to its source channel reliably enough for provenance labeling (AS-2);
- REM's code, parameters, policy and logs are protected from the adversary (AS-3);
- the institution can declare consequence tiers and relative costs, and accepts that these are policy choices rather than empirical findings (Section 3.7.3; Table 3.12);
- a human reviewer is available to resolve escalations, because the protective value of Escalate depends on the reviewer (Section 3.11.7);
- per-step latency is acceptable for the application, which is unmeasured.

Regulatory requirements for event recording and human oversight motivate two properties of the design, the audit record and the escalation route (Chapter 2, Section 2.7). Whether a particular financial agent falls within a regulated category is not assessed in this thesis.

## 5.8 Future Work

Future work follows directly from the limitations of Section 5.5. It is ordered by dependency. It completes the work that Chapter 3 specifies and does not substitute for it.

1. **Resolve the open decisions.** Obtain supervisor decisions on:
   - SC-1 to SC-6;
   - SD-FREEZE and SD-STRUCT;
   - RQ1–RQ4;
   - the pending design values: the classifier, tier map, costs and loss grid, predicates, Modify mechanism, backbones, attack templates, repeats, AgentDojo version and induced-read labeling.
2. **Complete the implementation.** Implement:
   - the Input & Context operations;
   - the Detection and Behavioral Analysis features of Tables 3.8–3.9;
   - the tier map and predicates;
   - the loss structure with the dominance check and feasible verdict set;
   - the declared Modify mechanism;
   - the baseline threshold policy of Equation 3.14;
   - the offline fitting of Procedure 3.1;
   - the metrics of Section 3.12.
3. **Demonstrate the integration.** Connect REM to a pinned AgentDojo version and demonstrate AS-1.
4. **Execute the evaluation of Chapter 3.** Run, in order:
   - observe-only runs and label construction with its audit;
   - pilot E0 and feature freezing;
   - grouped cross-fitting;
   - enforcing-mode runs of B0, B1 and REM;
   - the ablations and mitigation-effectiveness runs;
   - latency measurement on declared hardware.

   Then report results with grouped bootstrap intervals and across the declared loss grid.
5. **Close the evidence issues.** Resolve:
   - the Platt citation conflict (OI-07);
   - the NEXUS evidence issues (OI-01 to OI-06);
   - the partially verified references and equation sources;
   - the four unrecorded code citations.
6. **Extensions outside the current scope** (listed as out of scope in Chapter 3, Section 3.1.4):
   - evaluation against adaptive adversaries;
   - other benchmarks, reported without pooling;
   - task-automation environments, if approved;
   - the counterfactual estimation of intervention value discussed by C. Zhang et al. (2026).

## 5.9 Conclusion

This thesis set out to design and evaluate a runtime evaluation and mitigation framework for financial AI agents. The framework selects among Allow, Modify, Escalate and Block for each proposed tool call by minimizing expected loss under a calibrated probability of adversarial inducement and declared consequence tiers. It records every verdict for audit.

The design is specified in full in Chapter 3. Its mathematical decision core is implemented and verified in Chapter 4, together with step-level mitigation, a per-step audit record and a configuration that refuses to run on undeclared values.

The empirical part of the thesis has not been carried out. No evidence yet shows that REM reduces attack success, preserves utility, produces calibrated probabilities on agent data, or differs in outcome from a consequence-independent baseline. Objectives O2 and O3 and research questions RQ1–RQ4 therefore remain open.

Six specification conflicts between Chapter 3 and the implementation, and several design values, await supervisor decision. The conclusion supported by the present evidence is limited to three statements:

- REM's decision rule can be implemented as specified;
- the separation between calibrated probability, declared loss, verdict and audit that Chapter 3 requires can be enforced in software;
- the evaluation designed to test REM's security value remains to be executed.

## References

Chen, H.-H. (2026). *Insuring every action: An authority frontier framework for runtime actuarial control of autonomous AI agents* (arXiv:2605.25632) [Preprint]. arXiv. https://arxiv.org/abs/2605.25632

Hossain, E., Nipu, M. M. H., Ornee, T. N., Rana, R., & Yousefi, N. (2026). *NEXUS: Structured runtime safety for tool-using LLM agents* (arXiv:2607.19356) [Preprint]. arXiv. https://arxiv.org/abs/2607.19356

Jia, H., Liu, Y., Chong, B., Yang, Y., Chen, Y., Liang, J., Li, Q., Lu, H., Xu, K., Zheng, H., Zhang, C., Peng, H., & Yu, P. S. (2026). *FinHarness: An inline lifecycle safety harness for finance LLM agents* (arXiv:2605.27333) [Preprint]. arXiv. https://arxiv.org/abs/2605.27333

Liu, H., Ilyushin, E., Ni, J., & Zhu, M. (2026). *SafeAgent: A runtime protection architecture for agentic systems* (arXiv:2604.17562) [Preprint]. arXiv. https://arxiv.org/abs/2604.17562

She, Y., Liang, Y., & Kang, E. (2026). *Safeguarding LLM agents from misalignment through provenance analysis* (arXiv:2607.01236) [Preprint]. arXiv. https://arxiv.org/abs/2607.01236

Yang, C. (2026). *AgentTrust: Runtime safety evaluation and interception for AI agent tool use* (arXiv:2605.04785) [Preprint]. arXiv. https://arxiv.org/abs/2605.04785

Zhang, C., Wan, Z., Yu, X., Wu, J., Wen, Q., Zhou, P., Zhao, W., & Tsang, I. (2026). *Calibration is not control: Why LLM-agent oversight needs intervention* (arXiv:2606.21399) [Preprint]. arXiv. https://arxiv.org/abs/2606.21399
