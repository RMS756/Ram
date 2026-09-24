# CHAPTER ONE

# INTRODUCTION

## 1.1 Background

Large language model (LLM) agents use a language model as the controller of a system that perceives, reasons, plans and acts in pursuit of a task (L. Wang et al., 2024). In the execution pattern made explicit by ReAct (Yao et al., 2023), the model interleaves reasoning with actions, and the observations returned by those actions re-enter its context and shape the next step. Tool-using agents act through calls to external tools with arguments that the model generates.

When such an agent operates in a financial setting, a single proposed tool call can have direct external effects:

- initiate a payment;
- schedule or alter a recurring payment;
- change account credentials;
- send customer data to an external recipient.

The security question therefore shifts from what a model says to what an agent does. It concerns the moment at which a proposed action crosses from the agent into its environment (Chapter 2, Section 2.1).

## 1.2 Problem Statement

An agent receives input through channels of different trustworthiness:

- the system prompt;
- the user's request;
- tool outputs;
- retrieved content;
- stored memory.

Indirect prompt injection exploits the difference. Content from an external source, processed by the agent, alters its behavior without any access to the user channel (OWASP Gen AI Security Project, 2025; Greshake et al., 2023). Benchmarks designed for tool-using agents establish that this threat is practical, including in environments with financial tools (Debenedetti et al., 2024; Zhan et al., 2024; H. Zhang et al., 2025). The rates they report depend strongly on benchmark, model and attack template, and they cannot be pooled across studies (Chapter 2, Section 2.3).

For a financial agent, the effect of a successful injection becomes visible, and still preventable, at one point: when the agent proposes an action that serves the attacker's objective. This is the last point at which the action can be prevented rather than repaired (Chapter 2, Section 2.6). A defense placed at this point must decide, for each proposed tool call, whether to release it, modify it, refer it for human review or block it.

That decision raises two questions that the reviewed literature leaves open (Chapter 2, Section 2.10):

- how an estimated probability that an action was adversarially induced should be combined with the consequence of that action when choosing among responses;
- how effective each response actually is.

The problem addressed in this thesis is the runtime compromise of tool-using financial agents through indirect prompt injection, and the design and evaluation of a decision layer at the action boundary that addresses these two questions (Chapter 3, Table 3.1).

## 1.3 Motivation

Three considerations motivate the work.

First, the consequences in the financial domain are concrete. Tools that transfer value, modify payments or change credentials expose money, account control and personal data to manipulation (Chapter 2, Section 2.7). Conventional evaluation of financial LLM agents, based on accuracy and return metrics, has been argued to give an illusion of reliability while overlooking vulnerabilities such as adversarial prompt manipulation (Z. Chen, J. Chen, et al., 2025).

Second, regulation adds requirements for record-keeping and human control. Regulation (EU) 2024/1689 requires high-risk AI systems to allow the automatic recording of events and effective human oversight, including the ability to intervene (European Parliament & Council of the European Union, 2024). Whether a given financial agent falls within a high-risk category is not assessed in this thesis. The provisions motivate two design properties: an audit record for every decision and an explicit route to human review.

Third, the evaluation of learned security mechanisms is known to be fragile. Pitfalls in the design and evaluation of learning-based security systems lead to unrealistic performance estimates (Arp et al., 2022). Audits of agent-safety benchmarks report metric flaws, inconsistent rankings and contradictory conclusions across benchmarks (Y. Wang et al., 2026; M. Q. Li et al., 2026). A defense for financial agents must therefore be evaluated so that attack success is reported together with benign utility, dependence between benchmark tasks is respected, and leakage between fitting and test data is controlled.

## 1.4 Research Gap

The gap is not the absence of runtime guardrails, probability calibration, graduated interventions, human review, provenance analysis or consequence-aware control. Each of these is present in the reviewed literature (Chapter 2, Section 2.14). Several recent systems are close to the design studied here:

- **NEXUS** combines rules and argument inspection with a logistic-regression risk score calibrated by Platt scaling. It defines an expected-loss objective with fixed costs for its interventions, while its deployed policy is a rule cascade in which the calibrated score gates certain cases (Hossain et al., 2026).
- **AgentTrust** intercepts tool use and returns one of four verdicts through rule-based severity aggregation (C. Yang, 2026).
- **H.-H. Chen (2026)** prices the consequence of agent actions before execution.
- **FinHarness** addresses runtime safety of financial agents through monitors and a judge cascade (Jia et al., 2026).
- **C. Zhang et al. (2026)** show that calibrating a risk score need not improve control.

Among the studies reviewed in Chapter 2, none reports an empirical evaluation of a non-invasive runtime layer for a financial tool-using agent with all of the following features (Chapter 2, Section 2.14):

- provenance-based evidence about proposed financial actions;
- a calibrated per-step probability that the proposed action is adversarially induced;
- a verdict that minimizes expected loss over Allow, Modify, Escalate and Block, using losses declared per consequence tier;
- deterministic mitigation;
- separate measurement of attack success, benign utility, intervention behavior and latency;
- comparison against a consequence-independent baseline that uses the same estimator.

This gap is empirical and integrative. It concerns the combination and evaluation of established mechanisms, not a new learning algorithm. It is bounded by the sources reviewed and by the September 2026 literature update (Chapter 2, Section 2.14).

## 1.5 Research Aim

The approved research proposal states objectives but no separate aim statement. The aim below is derived from the approved objectives of Section 1.6 and adds nothing to them.

The aim of this research is to design a runtime evaluation and mitigation framework for the security of financial AI agents, to evaluate it against adversarial attacks, and to compare it with existing security approaches.

## 1.6 Research Objectives

The approved objectives are (Chapter 3, Section 3.1.2):

- **O1:** Design a REM framework for financial AI agents' and task automation agents' security.
- **O2:** Evaluate the framework against adversarial attacks.
- **O3:** Compare performance with existing security approaches.

The evaluation designed in this thesis uses a financial (banking) environment. Task-automation environments are outside the evaluation scope unless approved as an extension (Chapter 3, Section 3.1.2).

## 1.7 Research Questions

The approved proposal does not state research questions. The following questions are derived from the objectives in Chapter 3 (Section 3.1.3) and are presented for supervisor confirmation. **Until confirmed, they remain proposed ([PD]).**

- **RQ1 (estimation).** How well does a ridge logistic regression estimator, using context, behavioral and action evidence available at the tool-call boundary, discriminate adversarially induced proposed actions in the AgentDojo banking environment, and how well calibrated are its probabilities under grouped cross-fitting?
- **RQ2 (decision).** Compared with a consequence-independent threshold policy that uses the same estimator, how does consequence-tiered expected-loss verdict selection change attack success, benign utility, utility under attack and intervention rates, across a declared range of loss structures?
- **RQ3 (mitigation and cost).** What residual attack success remains after the Modify mechanism, how often is escalation selected, and what per-step latency does REM add?
- **RQ4 (component contribution).** What is the marginal contribution of each evidence group, of calibration, and of consequence tiers, as determined by ablation?

## 1.8 Proposed Approach

The Runtime Evaluation and Mitigation (REM) framework is a runtime mediation layer placed between one agent and its environment. It treats the agent as opaque: it observes inputs, context, proposed actions and tool results, but not model parameters or internal reasoning (Chapter 3, Section 3.3.1). REM comprises exactly five layers (Chapter 3, Section 3.2.1):

1. **Input & Context Layer.** Captures the information the agent handles and the action it proposes, and labels each context segment with its provenance.
2. **Detection Layer.** Computes evidence about untrusted context.
3. **Behavioral Analysis Layer.** Computes evidence about the episode history and the proposed action.
4. **Decision Engine Layer.** Performs the following steps:
   - estimates the probability that the proposed action is adversarially induced, using ridge logistic regression (Cox, 1958; le Cessie & van Houwelingen, 1992);
   - calibrates that probability on the logit (Platt, 1999; Guo et al., 2017);
   - assigns a declared consequence tier and applies policy predicates;
   - selects the verdict among Allow, Modify, Escalate and Block by minimizing conditional risk under tier-indexed losses (Elkan, 2001; Chow, 1970);
   - writes an audit record.
5. **Mitigation Layer.** Executes the mechanism associated with the verdict.

Offline fitting and recalibration are cross-cutting activities performed between deployments. They are not a layer. A linear attribution of the logit (Lundberg & Lee, 2017) is written to the audit record and never influences the verdict.

Declared costs play the role that hand-chosen thresholds play in threshold policies. The threshold between two verdicts becomes a consequence of the declared cost ratio for the action's consequence tier (Chapter 3, Section 3.7.5).

## 1.9 Research Methodology

The research follows design science research. In design science, knowledge is produced by building an artifact that addresses an identified problem and evaluating it (Hevner et al., 2004), following the six activities of Peffers et al. (2007) (Chapter 3, Section 3.1.1). The artifact is REM. The planned evaluation is quantitative and experimental, in the AgentDojo banking environment (Debenedetti et al., 2024). It compares REM with a baseline that uses the same estimator but a consequence-independent decision rule, so that differences in outcomes can be attributed to the decision rule. Estimation, calibration and threshold selection use nested grouped cross-fitting, because the benchmark does not support independent partitions (Chapter 3, Sections 3.11.4–3.11.5).

## 1.10 Scope

The scope is set in Chapter 3 (Section 3.1.4).

**In scope:**

- a single LLM-based agent that invokes tools with generated arguments;
- a financial (banking) task environment with executable tools and state-based checks;
- indirect prompt injection through tool outputs as the evaluated attack class;
- runtime mediation of each proposed tool call before it is released.

**Out of scope:**

- training-time defenses and modification of the agent's model or prompts;
- multi-agent systems;
- adaptive adversaries who tune attacks to REM;
- production deployment in a financial institution;
- counterfactual estimation of intervention value by replaying agent trajectories.

The design rests on stated assumptions (Chapter 3, Table 3.3). Among them:

- REM can intercept tool calls and results without modifying the agent (AS-1);
- REM's own code, parameters and logs are protected from the adversary (AS-3);
- adversaries do not adapt to REM in the primary evaluation (AS-6).

## 1.11 Significance and Expected Contribution

The expected contribution is empirical and integrative (Chapter 3, Section 3.13). It consists of the design and evaluation, on an open and executable banking benchmark under indirect prompt injection, of a non-invasive five-layer runtime layer that combines:

- provenance-based action evidence;
- a calibrated per-step probability of adversarial inducement;
- verdict selection by minimizing conditional risk with losses declared per consequence tier;
- deterministic mitigation whose effectiveness is measured.

The evaluation compares this combination with a consequence-independent baseline on the same estimator, and measures security, utility, intervention behavior and latency separately.

The thesis does not claim:

- a new algorithm;
- the first runtime guardrail, calibrated agent risk score or consequence-aware controller;
- that calibration improves control;
- robustness against adaptive adversaries;
- any prevention guarantee;
- validity in production financial deployment.

Each constituent mechanism is established and attributed to its source (Chapter 3, Table 3.16). The contribution holds only to the extent that the specified experiments support it.

## 1.12 Current Status of the Research

The design is specified in full in Chapter 3. The implementation reported in Chapter 4 realizes the following:

- the mathematical core of the Decision Engine (estimation, calibration on the logit, conditional risk and verdict selection);
- the audit-only attribution;
- step-level mitigation;
- a per-step audit record;
- a configuration that refuses to run while design inputs are undeclared.

It is verified by 154 passing software tests.

The following are not yet implemented:

- the evidence features;
- the consequence tiers, policy predicates and loss values;
- the Modify mechanism;
- the integration with AgentDojo.

The experimental evaluation has not been executed. Consequently, this thesis does not yet report empirical results for objectives O2 and O3 or for RQ1–RQ4 (Chapter 4, Section 4.12; Chapter 5, Section 5.2).

Six specification conflicts between Chapter 3 and the implementation (SC-1 to SC-6) await supervisor decision. They concern the mitigation semantics, tie-breaking, the calibration ablation, the calibration fitting procedure, the Brier score and the component-to-layer mapping (Chapter 4, Section 4.16).

## 1.13 Thesis Organization

The thesis is organized in five chapters:

- **Chapter 1** introduces the problem, gap, aim, objectives, research questions, approach and scope.
- **Chapter 2** reviews the literature on runtime protection of LLM agents, with emphasis on indirect prompt injection, runtime guardrails, action-boundary security, financial agents, calibration, decision and mitigation, auditability and evaluation benchmarks, and states the research gap.
- **Chapter 3** specifies the research methodology and the design of REM: its architecture, threat model, the algorithms and equations of each layer, the runtime procedure, and the experimental methodology and metrics.
- **Chapter 4** reports the implementation, the specified experimental design and its execution status, and the available evidence.
- **Chapter 5** discusses the findings, relates them to the objectives and to prior work, states limitations and threats to validity, and concludes with future work.

Chapter 3, which was written before this chapter structure was set, refers to a demonstration chapter, an evaluation chapter and a communication chapter numbered 4, 5 and 6 (Chapter 3, Table 3.1). The alignment of those cross-references with the five-chapter structure is pending supervisor decision.

## References

Arp, D., Quiring, E., Pendlebury, F., Warnecke, A., Pierazzi, F., Wressnegger, C., Cavallaro, L., & Rieck, K. (2022). Dos and don'ts of machine learning in computer security. In *31st USENIX Security Symposium*. USENIX Association. https://arxiv.org/abs/2010.09470

Chen, H.-H. (2026). *Insuring every action: An authority frontier framework for runtime actuarial control of autonomous AI agents* (arXiv:2605.25632) [Preprint]. arXiv. https://arxiv.org/abs/2605.25632

Chen, Z., Chen, J., Chen, J., & Sra, M. (2025). *Standard benchmarks fail — Auditing LLM agents in finance must prioritize risk* (arXiv:2502.15865) [Preprint]. arXiv. https://arxiv.org/abs/2502.15865

Chow, C. K. (1970). On optimum recognition error and reject tradeoff. *IEEE Transactions on Information Theory, 16*(1), 41–46. https://doi.org/10.1109/TIT.1970.1054406

Cox, D. R. (1958). The regression analysis of binary sequences. *Journal of the Royal Statistical Society: Series B (Methodological), 20*(2), 215–232. https://doi.org/10.1111/j.2517-6161.1958.tb00292.x

Debenedetti, E., Zhang, J., Balunović, M., Beurer-Kellner, L., Fischer, M., & Tramèr, F. (2024). *AgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents* (arXiv:2406.13352). arXiv. https://arxiv.org/abs/2406.13352

Elkan, C. (2001). The foundations of cost-sensitive learning. In *Proceedings of the Seventeenth International Joint Conference on Artificial Intelligence (IJCAI-01)*. https://cseweb.ucsd.edu/~elkan/rescale.pdf

European Parliament & Council of the European Union. (2024). *Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 laying down harmonised rules on artificial intelligence*. Official Journal of the European Union. https://eur-lex.europa.eu/eli/reg/2024/1689/oj

Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., & Fritz, M. (2023). Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection. In *Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security* (pp. 79–90). ACM. https://doi.org/10.1145/3605764.3623985

Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. In *Proceedings of the 34th International Conference on Machine Learning* (Vol. 70, pp. 1321–1330). PMLR. https://proceedings.mlr.press/v70/guo17a.html

Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly, 28*(1), 75–106. https://doi.org/10.2307/25148625

Hossain, E., Nipu, M. M. H., Ornee, T. N., Rana, R., & Yousefi, N. (2026). *NEXUS: Structured runtime safety for tool-using LLM agents* (arXiv:2607.19356) [Preprint]. arXiv. https://arxiv.org/abs/2607.19356

Jia, H., Liu, Y., Chong, B., Yang, Y., Chen, Y., Liang, J., Li, Q., Lu, H., Xu, K., Zheng, H., Zhang, C., Peng, H., & Yu, P. S. (2026). *FinHarness: An inline lifecycle safety harness for finance LLM agents* (arXiv:2605.27333) [Preprint]. arXiv. https://arxiv.org/abs/2605.27333

le Cessie, S., & van Houwelingen, J. C. (1992). Ridge estimators in logistic regression. *Applied Statistics, 41*(1), 191–201. https://doi.org/10.2307/2347628

Li, M. Q., Fung, B. C. M., Li, B., Ismail, H., & Iqbal, F. (2026). *Taxonomy and consistency analysis of safety benchmarks for AI agents* (arXiv:2605.16282) [Preprint]. arXiv. https://arxiv.org/abs/2605.16282

Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. In *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1705.07874

OWASP Gen AI Security Project. (2025). *LLM01:2025 Prompt injection*. OWASP Foundation. https://genai.owasp.org/llmrisk/llm01-prompt-injection/

Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems, 24*(3), 45–77. https://doi.org/10.2753/MIS0742-1222240302

Platt, J. C. (1999). Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. In A. J. Smola, P. Bartlett, B. Schölkopf, & D. Schuurmans (Eds.), *Advances in large margin classifiers* (pp. 61–74). MIT Press.

Wang, L., Ma, C., Feng, X., Zhang, Z., Yang, H., Zhang, J., Chen, Z., Tang, J., Chen, X., Lin, Y., Zhao, W. X., Wei, Z., & Wen, J. (2024). A survey on large language model based autonomous agents. *Frontiers of Computer Science, 18*(6), Article 186345. https://doi.org/10.1007/s11704-024-40231-1

Wang, Y., Han, X., Shang, D., Tang, Y., & Liu, B. (2026). *Safety, or just capability? A validity audit of agent-safety benchmarks* (arXiv:2607.28685) [Preprint]. arXiv. https://arxiv.org/abs/2607.28685

Yang, C. (2026). *AgentTrust: Runtime safety evaluation and interception for AI agent tool use* (arXiv:2605.04785) [Preprint]. arXiv. https://arxiv.org/abs/2605.04785

Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing reasoning and acting in language models. In *International Conference on Learning Representations*. https://arxiv.org/abs/2210.03629

Zhan, Q., Liang, Z., Ying, Z., & Kang, D. (2024). InjecAgent: Benchmarking indirect prompt injections in tool-integrated large language model agents. In *Findings of the Association for Computational Linguistics: ACL 2024*. https://arxiv.org/abs/2403.02691

Zhang, C., Wan, Z., Yu, X., Wu, J., Wen, Q., Zhou, P., Zhao, W., & Tsang, I. (2026). *Calibration is not control: Why LLM-agent oversight needs intervention* (arXiv:2606.21399) [Preprint]. arXiv. https://arxiv.org/abs/2606.21399

Zhang, H., Huang, J., Mei, K., Yao, Y., Wang, Z., Zhan, C., Wang, H., & Zhang, Y. (2025). Agent Security Bench (ASB): Formalizing and benchmarking attacks and defenses in LLM-based agents. In *International Conference on Learning Representations*. https://arxiv.org/abs/2410.02644
