# CHAPTER SIX

# DISCUSSION, CONTRIBUTIONS, LIMITATIONS, AND CONCLUSION

This chapter interprets the exploratory evaluation of Chapter 5. Each conclusion is linked to the result that supports it and to the limit of that result. Section 5.1 defines the kinds of evidence: held-out prediction, observe-only decision, replay result; no live run was executed.

## 6.1 Interpretation of the Findings

### 6.1.1 What the evidence supports

**Table 6.1. Conclusions, their support and their limits**

| # | Conclusion | Supporting result | Limit |
|---|---|---|---|
| 1 | REM can be placed at the tool-execution boundary of a benchmark agent without modifying the agent's model, prompts or tools | Integration tests; replay of 3,313 episodes reproducing recorded outcomes (Chapter 4, Section 4.11.2) | Placement requires control of the tool executor (Chapter 4, Section 4.9); not shown in a production framework |
| 2 | Evidence available at the tool boundary separates attack attempts from legitimate calls on attacker objectives, templates and backbones not seen in fitting | Held-out ROC-AUC 0.938 [0.908, 0.961]; 0.92–0.96 on other templates; 0.74–1.00 per held-out backbone (Section 5.4) | One benchmark, one attacker account, labels that are a proxy; destination novelty is easier here than in practice |
| 3 | Action evidence carries most of this separation | Without action evidence, ROC-AUC falls to 0.799 and AP to 0.367 (Section 5.7) | Single benchmark; nine attacked groups |
| 4 | With the pre-registered costs, tier-indexed expected-loss verdicts intervene on far more legitimate state-changing actions than the baseline, mainly because of the low thresholds the costs imply at high tiers, not because of the escalation option | Observe-only: 33 vs 132 of 180 benign state-changing steps released; REM without expected-loss Escalate releases 48 (Section 5.5) | Costs are declared, not elicited; another cost structure gives another trade-off (Section 5.9) |
| 5 | Within the replay assumption, REM withholds more recorded attack attempts than the baseline, at a utility cost that depends on how escalations are resolved | ΔASR −0.051 [−0.130, −0.007]; Δbenign utility −0.195 without a reviewer and +0.003 with an oracle reviewer (Section 5.6) | NO-ADAPT; replay is a proposed scope amendment; most of the ASR difference comes from two single-task attack categories |

### 6.1.2 Why benign utility falls

The fall in benign utility has two sources, and the evaluation separates them.

**Low thresholds at high tiers.** With C~miss~ up to twenty times C~FA~, the Allow–Block indifference point at tier 4 is 1/21 (Eq. 3.9). A probability as low as 0.05 is enough to withhold a transfer above the limit, a payment modification or a credential change. Legitimate actions of these kinds in this benchmark often carry the same action evidence as attacks; for example, a recipient read from a tool output rather than stated in the request. They therefore cross the threshold.

**Where the verdict sends them.** The withheld actions are mostly escalated. Without a reviewer an escalation is a withheld action, so utility falls. The comparison with REM without expected-loss Escalate shows that removing the option does not recover the utility: the same actions are then withheld through Modify. The utility cost is therefore a consequence of the declared costs and of the evidence, not of escalation as such.

**What a reviewer would change.** An escalation is worth something only if someone resolves it. With an oracle reviewer the utility cost disappears, which bounds what a perfect reviewer could recover. A real reviewer would recover less, at some delay and cost. The thesis does not model that reviewer.

### 6.1.3 Why behavioral evidence did not help, and calibration did not change outcomes

**Behavioral evidence.** The behavioral indicators are not specific to attacks in this benchmark:
- *privilege escalation* fired on 92% of legitimate state-changing steps, because a user's first transfer is, by definition, the first use of a higher-privilege tool;
- *transition deviation* fired more often on legitimate steps (43%) than on attacks (17%), because legitimate tasks held out from fitting produce unseen transitions.

The estimator gave these features positive weight. In the decision they therefore added to the probability of legitimate high-tier actions, and removing them recovered utility without a measured change in attack success. This is an observation about these features in this benchmark, with short trajectories. It does not show that behavioral evidence is useless elsewhere.

**Calibration.** Calibration did not change outcomes for two reasons:
- logistic regression fitted by penalized likelihood was already close to calibrated on in-distribution folds, so the fitted map was close to the identity;
- the one fold where calibration mattered, the unseen credential-change attack, was miscalibrated in a way a monotone map fitted on other attack categories cannot repair.

This agrees with the position, taken in Chapter 3, that calibration quality and control quality must be reported separately (C. Zhang et al., 2026).

### 6.1.4 What the evidence does not support

- **That REM protects live agents.** Under replay a withheld call does not reappear. A live agent can retry, rephrase or reach the goal through another tool. The near-zero replay ASR and the near-zero residual success after Modify are consequences of that assumption.
- **That REM is deployable as configured.** Without a reviewer, benign utility on state-changing tasks fell from 0.47 to 0.17 in replay.
- **That REM is superior to the baseline or to other defenses.**
  - The realized-loss comparison favors REM by construction.
  - The comparison with distributed defenses is not controlled.
  - Most of the ASR difference from the baseline comes from single-task attack categories.
- **Anything about the injection classifier**, which was not available, or about adaptive attackers, who were out of scope.

## 6.2 Achievement of the Objectives

**Table 6.2. Objectives and how far they were achieved**

| Objective | Achieved | Not achieved |
|---|---|---|
| **O1.** Design a REM framework for financial AI agents' and task automation agents' security | Designed (Chapter 3) and implemented (Chapter 4) for a financial (banking) agent; design values declared for exploration | Supervisor-approved design values; any task-automation setting; the injection classifier |
| **O2.** Evaluate the framework against adversarial attacks | Exploratory evaluation on recorded attacks against 21 real agents: offline classification, observe-only decisions, replay sensitivity (Chapter 5) | Enforcing-mode evaluation with live agents; repeated runs; human label audit; adaptive attacks |
| **O3.** Compare performance with existing security approaches | Controlled comparison with a same-estimator baseline (B1) and a same-escalation-opportunity variant; recorded outcomes of four distributed defenses for orientation | A controlled comparison with any published defense (NEXUS, AgentTrust, FinHarness or the distributed defenses) on a shared protocol |

O1 is achieved for the banking setting. O2 and O3 are partly achieved: the evidence is exploratory, and the decisive experiment, enforcement with live agents, was not run.

## 6.3 Comparison with Prior Work

The comparison restates design positions documented in Chapter 2 and does not rank systems, because no shared evaluation exists. Properties marked U in Chapter 2 are unverified.

**Table 6.3. Design-level comparison with the closest prior work**

| System | Documented design (Chapter 2; verification level) | Relation to REM |
|---|---|---|
| NEXUS (Hossain et al., 2026) | Structured-plan monitor; formal policy over allow, block, confirm and revise; rules, argument inspection and a calibrated logistic risk score (A). Fixed intervention costs and a rule-first cascade (U) | Shares calibrated logistic scoring and a four-way intervention set. REM evaluates each call during execution, in an executable banking environment. The difference in decision rule rests partly on unverified evidence |
| AgentTrust (C. Yang, 2026) | Pre-execution interception; allow, warn, block and review; normalizer, chain detection and LLM judge (A) | Shares interception and a review verdict. REM uses a calibrated probability and declared losses |
| SafeAgent (H. Liu et al., 2026) | Runtime controller; decision core with operators for risk, utility-cost, consequence and arbitration (A); LLM realization (U) | REM's verdict is a closed-form rule |
| ProvenanceGuard (She et al., 2026) | Checks whether a proposed call is supported by traceable evidence in context; peer-reviewed (A) | REM's argument-provenance feature asks the same question; in REM's evaluation such action evidence carried most of the separation |
| H.-H. Chen (2026) | Prices the consequence of side-effecting actions against reserve capital (A) | REM combines consequence with an estimated probability |
| FinHarness (Jia et al., 2026) | Financial-agent monitors and an LLM-judge cascade; results on a benchmark whose preprint was withdrawn for non-scientific reasons (A) | Shares domain and placement; REM is evaluated on an open benchmark |
| C. Zhang et al. (2026) | Calibration need not improve control (A) | REM's evaluation observed no calibration effect on decisions |

Each mechanism in REM has precedent. The distinguishing elements are the combination and the evaluation design; neither has been compared with these systems on a shared protocol.

## 6.4 Contributions

**Achieved, with their evidence:**
1. **A specified and implemented composition.** It comprises:
   - provenance-based evidence;
   - a ridge estimator calibrated on the logit;
   - consequence tiers and policy predicates;
   - a four-verdict expected-loss rule with a feasible set and a dominance check;
   - deterministic mitigation under two stated semantics;
   - an audit record whose attribution cannot reach the verdict.

   Undeclared design values stop the software. *Evidence:* Chapters 3–4; 193 tests.
2. **An evaluation protocol that isolates the decision rule.** REM, the baseline and the same-escalation variant share the estimator, calibration and predicates. Grouped cross-fitting holds out whole attacker objectives, and every fitted quantity, including the feature set, is fitted within the fold. *Evidence:* Chapter 5 and its exact reproduction.
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
- superiority over the systems of Table 6.3.

## 6.5 Limitations

1. **Design status.** Costs, tiers, predicates, the feature set and the label rule are declared exploratory values, not approved ones.
2. **No live runs.** Enforcement was estimated only by replay under NO-ADAPT, a method proposed as an amendment to the Chapter 3 scope.
3. **One benchmark.** One benchmark, one attack family for fitting, one attacker identity, and historical model snapshots (2024–2025).
4. **Labels.** Labels are attempt-based and reference-matched. They are ambiguous for user_task_15 under early suite versions and miss alternative attacker routes. They have not been audited by a human.
5. **Statistics.** Nine attacked groups, one run per configuration, no correction for multiple comparisons. Several categories contain a single injection task.
6. **Reviewer.** Escalation outcomes are bounded by an oracle and by no reviewer.
7. **Missing component.** No neural injection classifier was available.
8. **Literature review.** The review was record-level; no full text was screened.
9. **Runtime figures.** They describe the evaluated configuration only. A deployment with a neural classifier or a human reviewer would be slower.

## 6.6 Future Work, Ordered by Dependency

1. **Decisions** (`SUPERVISOR_DECISIONS_REQUIRED`): approve or replace the declared design values, the label rule, the mitigation semantics and the replay scope amendment.
2. **Label audit.** Annotate the prepared package (`results/pilot_R2/label_audit_human_package.csv`) with at least one human annotator, and preferably two. Report agreement and revise the label rule if needed.
3. **Live enforcing-mode evaluation**, required for the central claim:
   - run B0, B1, REM and REM without expected-loss Escalate with live backbones;
   - use at least three repeated runs;
   - fix and record the benchmark version, model versions, decoding parameters and costs.

   This measures adaptive agent behavior after refusals and the true residual success after Modify, and distinguishes step-level from episode-level semantics.
4. **A reviewer model** with error rate and delay, so that the utility cost of escalation can be estimated between the two bounds.
5. **Feature revision.** Revise the behavioral features, for example by conditioning privilege escalation on provenance, and add the injection classifier. Then re-run Pilot E0 on new fitting data.
6. **Elicited costs.** Repeat the decision analysis with costs elicited from a financial-institution context, rather than declared.
7. **Full-text literature review.** Complete the review by searching the named databases and screening full texts, and re-examine the unverified properties of the closest systems.
8. **Further benchmarks and adaptive attacks**, reported per benchmark.

## 6.7 Conclusion

This thesis set out to design a runtime framework that decides, for each tool call proposed by a financial AI agent, whether to allow, modify, escalate or block it. The decision minimizes expected loss under a calibrated probability of adversarial inducement and a declared consequence tier, and every verdict is recorded for audit. The framework was specified, implemented at the tool boundary of a benchmark agent, and evaluated in an exploratory study of 6,762 tool calls proposed by 21 real LLM agents.

**What was observed:**
- The evidence available at the tool boundary separates attack attempts from legitimate calls well on attacker objectives not seen in fitting, mainly through evidence about the action's arguments.
- With the costs declared for exploration, the expected-loss rule intervenes on nearly all attack attempts, and also on most legitimate high-consequence actions. Whether that is acceptable depends on a human reviewer that the benchmark does not provide.
- Calibration and the behavioral features produced no observed improvement.

These findings come from recorded traces and from a replay that assumes the agent does not adapt. They do not show that REM protects a live agent. The experiment needed to show that, enforcement with live agents, is the first item of future work, and the thesis does not claim its result in advance.

## References

Chen, H.-H. (2026). *Insuring every action: An authority frontier framework for runtime actuarial control of autonomous AI agents* (arXiv:2605.25632) [Preprint]. arXiv. https://arxiv.org/abs/2605.25632

Hossain, E., Nipu, M. M. H., Ornee, T. N., Rana, R., & Yousefi, N. (2026). *NEXUS: Structured runtime safety for tool-using LLM agents* (arXiv:2607.19356) [Preprint]. arXiv. https://arxiv.org/abs/2607.19356

Jia, H., Liu, Y., Chong, B., Yang, Y., Chen, Y., Liang, J., Li, Q., Lu, H., Xu, K., Zheng, H., Zhang, C., Peng, H., & Yu, P. S. (2026). *FinHarness: An inline lifecycle safety harness for finance LLM agents* (arXiv:2605.27333) [Preprint]. arXiv. https://arxiv.org/abs/2605.27333

Liu, H., Ilyushin, E., Ni, J., & Zhu, M. (2026). *SafeAgent: A runtime protection architecture for agentic systems* (arXiv:2604.17562) [Preprint]. arXiv. https://arxiv.org/abs/2604.17562

She, Y., Liang, Y., & Kang, E. (2026). Safeguarding LLM agents from misalignment through provenance analysis. In *Proceedings of the 41st IEEE/ACM International Conference on Automated Software Engineering* (pp. 3036–3048). ACM. https://doi.org/10.1145/3832783.3837535

Yang, C. (2026). *AgentTrust: Runtime safety evaluation and interception for AI agent tool use* (arXiv:2605.04785) [Preprint]. arXiv. https://arxiv.org/abs/2605.04785

Zhang, C., Wan, Z., Yu, X., Wu, J., Wen, Q., Zhou, P., Zhao, W., & Tsang, I. (2026). *Calibration is not control: Intervention value for LLM-agent oversight* (arXiv:2606.21399) [Preprint]. arXiv. https://arxiv.org/abs/2606.21399
