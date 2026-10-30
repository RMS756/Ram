# CHAPTER SIX

# DISCUSSION, CONTRIBUTIONS, LIMITATIONS, AND CONCLUSION

> **Status.** This chapter interprets the exploratory pilot of Chapter 5. Every empirical statement inherits the pilot's label: EXPLORATORY, pending supervisor decisions. Statements that depend on recorded-trace replay are out of scope under Chapter 3 Section 3.1.4 (SC-7). The research questions remain [PD].

## 6.1 Interpretation of the Findings

### 6.1.1 What the evidence supports

1. **The REM pipeline can be built at the tool boundary without modifying the agent (AS-1).**
   - Chapter 4 placed REM inside AgentDojo's own execution loop as a guarded tool executor.
   - It adds a median of under 0.2 ms and a p95 of under 0.6 ms per step, with a few kilobytes of transient memory.
   - Runtime cost is therefore not an obstacle to step-level mediation.
2. **Evidence available at the tool boundary separates attacker-induced from legitimate actions in this benchmark (AS-7, RQ1).**
   - Held-out ROC-AUC is 0.94 when the attacker objective is unseen.
   - It remains 0.92–0.96 on attack templates not used for fitting, and 0.74–1.00 on backbones not used for fitting.
   - The action evidence carries most of this separation: argument provenance, destination novelty and sensitive egress. This matches the position, reported in Chapter 2, that the proposed action and the provenance of its arguments are the most informative place to look (She et al., 2026).
3. **Consequence-tiered expected-loss verdicts change behaviour in the direction Chapter 3 predicts (RQ2).**
   - REM intervenes on more attacker-induced steps than the consequence-independent baseline with the same estimator.
   - It concentrates its additional interventions on high-consequence actions, as an escalation.
   - The single-tier ablations show that the tier map, not the estimator, moves the protection–utility trade-off.

### 6.1.2 What the evidence does not support

1. **That REM is deployable as configured.**
   - With the pre-registered costs and no reviewer, REM withholds most legitimate state-changing actions: benign utility drops from 0.52 to 0.31.
   - With an oracle reviewer the cost disappears, but an oracle is not a reviewer.
   - The practical value of REM's Escalate verdict therefore depends on a human process that this thesis has not modelled. C. Zhang et al. (2026) argue that oversight requires intervention capacity, not only calibrated scores; the pilot shows the same dependence from the other side.
2. **That calibration helped.**
   - Platt calibration on the logit left calibration error unchanged on in-distribution folds.
   - It did not repair the miscalibration on the one fold with an unseen attack category (credential change).
   - Chapter 3 already declines to claim that calibration improves control (Section 3.7.2), and the pilot gives no reason to strengthen that position.
3. **That every evidence group is needed.**
   - Context evidence made no measurable difference.
   - Behavioral evidence lowered benign utility without a measured security benefit.
   - Both observations are specific to one benchmark with templated attacks, but they are the opposite of what a "more evidence is better" reading of Chapter 3 would predict.
4. **Anything about adaptive agents or adaptive attackers.**
   - The near-zero residual attack success under Modify reflects the replay assumption that the agent never tries again.
   - It is not evidence about tool restriction as a mechanism.
5. **The optional CUSUM analysis.**
   - Its threshold did not hold its false-alarm target on held-out benign episodes.
   - Its alarms rarely preceded the first attacker-induced step.

### 6.1.3 A benchmark-version effect

In AgentDojo banking suite versions v1 and v1.1, the attacker's account in every injection task is also the legitimate new payee in user_task_15. For that user task, a legitimate payment therefore satisfies the attacker's success predicate, and the reference-match label marks legitimate actions as attacker-induced.

The benchmark changed the payee from v1.1.1. Most of the recorded traces used here (16 of 21 backbones) predate the change, and all of REM's residual attack success in the replay came from these episodes.

The finding is not new. It is a reminder that recorded traces from mixed benchmark versions must be checked task by task before pooling.

## 6.2 Relationship to the Objectives

**Table 6.1. Objectives and status**

| Objective (approved) | Status after this thesis |
|---|---|
| O1 — Design a REM framework for financial AI agents' security | Designed (Chapter 3) and implemented (Chapter 4). Design values await approval |
| O2 — Evaluate the framework against adversarial attacks | Exploratory pilot on recorded real-agent traces (Chapter 5). Confirmatory evaluation pending SD-FREEZE and live enforcing-mode runs |
| O3 — Compare performance with existing security approaches | Compared with the same-estimator baseline B1 and with recorded outcomes of four distributed defenses (not a controlled comparison). Comparison with the systems of Table 6.2 remains at the design level |

## 6.3 Comparison with Prior Work

The comparison below restates design positions documented in Chapter 2 and adds what the pilot measured for REM. It does not rank systems, because no shared evaluation exists.

**Table 6.2. Design-level comparison with the closest prior work**

| System | Documented design (Chapter 2) | Relation to REM | REM evidence from the pilot |
|---|---|---|---|
| NEXUS (Hossain et al., 2026) | Rules, argument inspection, logistic-regression risk score with Platt scaling; expected-loss objective over allow/revise/confirm/block; deployed as a rule cascade; plan-level evaluation on generated templates | Shares calibrated logistic scoring and a four-way intervention set. Differs in per-step minimization of conditional risk with tier-indexed losses at the tool boundary of an executing agent. NEXUS numerical claims remain unverified (Chapter 2) | Per-step expected-loss verdicts executed on 6,762 real-agent steps; B1 comparison with the same estimator |
| AgentTrust (C. Yang, 2026) | Pattern features, policy rules, analyzer risk scoring, maximum-severity aggregation, four verdicts including review | Shares interception, a review verdict and ablation with latency. Differs in using calibrated probability and declared losses rather than rule severity | Ablation and latency measured |
| SafeAgent (H. Liu et al., 2026) | Runtime controller whose decision operators are LLM-realized | REM excludes LLM arbitration by design; its verdict is a closed-form rule | Deterministic verdicts; 0 ties in 6,762 steps |
| ProvenanceGuard (She et al., 2026) | Checks whether a proposed call is supported by traceable evidence in context | REM's argument-provenance feature asks the same question and is not claimed as new | Action evidence, including provenance, carried most of the discrimination |
| H.-H. Chen (2026) | Prices action consequence deterministically against reserved capital | Shares consequence-dependent control; REM combines consequence with an estimated probability | Single-tier ablations show the consequence map drives the trade-off |
| FinHarness (Jia et al., 2026) | Financial-agent monitors and judge cascade | Shares domain and placement; differs in decision mechanism | Banking-environment pilot executed |
| C. Zhang et al. (2026) | Calibration can leave threshold-routed control unchanged | REM reports calibration and control separately and does not claim calibration improves control | Calibration gave no measurable gain; the B1 thresholds are invariant to monotone recalibration (tested) |

## 6.4 Contributions

The contributions are stated narrowly. Each mechanism has precedent (Chapter 3, Table 3.16), and none is claimed as an original invention.

1. **A specified composition.** The framework is specified for one point of an executing financial agent, its tool boundary. It composes:
   - provenance-based evidence;
   - a ridge logistic estimator with calibration on the logit;
   - consequence tiers;
   - policy predicates;
   - a four-verdict expected-loss decision with a feasible set and a dominance check;
   - deterministic mitigation;
   - an audit record whose attribution cannot reach the verdict.

   The composition, not any component, is the design contribution.
2. **An evaluation protocol that isolates the decision rule.** REM and B1 share the estimator and its calibration, so differences between them are attributable to the decision rule. Grouped cross-fitting holds out whole attacker objectives.
3. **An executed, reproducible pilot on real agent traces**, with:
   - a pre-registered design;
   - recorded amendments;
   - negative results reported;
   - exact reproduction from a single script.

   It includes a measured protection–utility trade-off whose dependence on the reviewer is quantified, from the no-reviewer bound to the oracle reviewer.
**Not claimed:**
- a new learning, calibration or decision-theoretic method;
- prevention guarantees;
- robustness to adaptive attackers;
- validity in production financial deployment;
- superiority over the systems of Table 6.2.

## 6.5 Limitations

1. **Design status.** The costs, tiers, predicates, feature set and label rule are pending supervisor approval. The pilot used declared exploratory values for them.
2. **No live agent runs.** Enforcement was estimated by replay (SC-7), under the assumption that the agent does not adapt. ASR under replay is not the ASR of a live agent.
3. **One benchmark, one attack family for fitting, one attacker identity.** Features such as destination novelty may be easier in this benchmark than in practice.
4. **Labels.** The reference-match rule marks attempts, misses alternative attacker routes, and is ambiguous for user_task_15. The label audit was performed by an AI assistant, not by a human.
5. **Statistics.** There are nine injection-task groups and one run per configuration. Intervals are wide and are not corrected for multiple comparisons.
6. **Reviewer model.** Escalation outcomes were bounded by an oracle and by "no reviewer"; real reviewers lie between and add latency.
7. **Missing component.** The pre-trained injection classifier (x^ctx₁) was not available.

## 6.6 Future Work

Ordered by dependency:
1. **Decisions.** Resolve:
   - SC-1 to SC-7;
   - SD-FREEZE, SD-1 to SD-5, SD-FEAT, SD-DET;
   - the label rule (LABEL-UT15, LABEL-ROUTE);
   - the reviewer model.
2. **Live enforcing-mode runs.** Run B0, B1 and REM with live backbones and at least three repeats, so that adaptive agent behaviour after refusals is observed and r_mod is measured as Chapter 3 intends.
3. **A realistic escalation model.** Specify reviewer error and delay, so that the utility cost of Escalate can be estimated between the two bounds.
4. **Re-examine the evidence set.** Investigate why the behavioral group lowers utility, for example through the privilege-escalation and transition-deviation features on legitimate first transfers, and re-run E0 with the pre-trained classifier if approved.
5. **Calibration under shift.** Study held-out attack categories, where the pilot shows miscalibration that Platt calibration does not repair.
6. **Other benchmarks and adaptive attacks.** Report results separately per benchmark, without pooling.

## 6.7 Conclusion

This thesis set out to design and evaluate a runtime framework that decides, for each tool call proposed by a financial AI agent, whether to allow, modify, escalate or block it. The decision minimizes expected loss under a calibrated probability of adversarial inducement and a declared consequence tier, and every verdict is recorded for audit.

The framework was specified (Chapter 3) and implemented with fail-closed handling of undeclared design values (Chapter 4). It was evaluated in an exploratory pilot on 6,762 tool calls proposed by 21 real LLM agents in the AgentDojo banking environment (Chapter 5).

The pilot shows that the evidence available at the tool boundary identifies attacker-induced actions on unseen attacker objectives, templates and backbones (ROC-AUC 0.92–0.96 for the first two). Consequence-tiered expected-loss verdicts intercept more of those actions than a threshold baseline with the same estimator.

It also shows the price. With the pre-registered costs, REM escalates most legitimate high-consequence actions, and its utility depends on who resolves those escalations. Calibration added nothing measurable, and two of the three evidence groups showed no measured benefit.

Because the design values are not yet approved and enforcement could be estimated only by a replay that Chapter 3 excludes, these findings are exploratory. The confirmatory evaluation that Chapter 3 specifies remains to be run, and the decisions it depends on are listed in `SUPERVISOR_DECISIONS_REQUIRED.md`.

## References

Chen, H.-H. (2026). *Insuring every action: An authority frontier framework for runtime actuarial control of autonomous AI agents* (arXiv:2605.25632) [Preprint]. arXiv. https://arxiv.org/abs/2605.25632

Hossain, E., Nipu, M. M. H., Ornee, T. N., Rana, R., & Yousefi, N. (2026). *NEXUS: Structured runtime safety for tool-using LLM agents* (arXiv:2607.19356) [Preprint]. arXiv. https://arxiv.org/abs/2607.19356

Jia, H., Liu, Y., Chong, B., Yang, Y., Chen, Y., Liang, J., Li, Q., Lu, H., Xu, K., Zheng, H., Zhang, C., Peng, H., & Yu, P. S. (2026). *FinHarness: An inline lifecycle safety harness for finance LLM agents* (arXiv:2605.27333) [Preprint]. arXiv. https://arxiv.org/abs/2605.27333

Liu, H., Ilyushin, E., Ni, J., & Zhu, M. (2026). *SafeAgent: A runtime protection architecture for agentic systems* (arXiv:2604.17562) [Preprint]. arXiv. https://arxiv.org/abs/2604.17562

She, Y., Liang, Y., & Kang, E. (2026). *Safeguarding LLM agents from misalignment through provenance analysis* (arXiv:2607.01236) [Preprint]. arXiv. https://arxiv.org/abs/2607.01236

Yang, C. (2026). *AgentTrust: Runtime safety evaluation and interception for AI agent tool use* (arXiv:2605.04785) [Preprint]. arXiv. https://arxiv.org/abs/2605.04785

Zhang, C., Wan, Z., Yu, X., Wu, J., Wen, Q., Zhou, P., Zhao, W., & Tsang, I. (2026). *Calibration is not control: Why LLM-agent oversight needs intervention* (arXiv:2606.21399) [Preprint]. arXiv. https://arxiv.org/abs/2606.21399
