# CHAPTER TWO

# LITERATURE REVIEW

## 2.1 Introduction

Large language model (LLM) agents no longer only generate text for a human reader. They plan multi-step tasks, call external tools with generated arguments, read the results of those calls, and act again. When such an agent is deployed in a financial setting, a single proposed tool call can initiate a payment, change a payee, alter account credentials, or send customer data to an external recipient. The security question therefore moves from what a model *says* to what an agent *does*, and to the moment at which a proposed action crosses from the agent into the environment.

This chapter reviews the literature that bears on runtime protection of such agents. Its purpose is not to catalogue systems but to establish, for each part of the problem, what existing work already solves, where its mechanisms overlap with the Runtime Evaluation and Mitigation (REM) framework studied in this thesis, what limitations remain, and what REM can legitimately investigate. The chapter proceeds from the security problem (Section 2.2) and the dominant attack class, prompt injection (Section 2.3), through runtime guardrails and agent security architectures (Section 2.4), stateful protection (Section 2.5), action-boundary security (Section 2.6), and the requirements of financial agents (Section 2.7). It then reviews the methodological building blocks on which a runtime decision layer depends: detection (Section 2.8), probability calibration (Section 2.9), decision and mitigation (Section 2.10), and auditability (Section 2.11). Section 2.12 reviews evaluation benchmarks. Section 2.13 synthesizes the comparison, Section 2.14 states the research gap, and Section 2.15 positions REM.

### 2.1.1 Review approach

The review is a structured narrative review rather than a systematic review. Sources were identified through targeted searches of the arXiv preprint server, the ACL Anthology, the Proceedings of Machine Learning Research, the USENIX, ACM, and IEEE digital libraries, and official documentation from standards and regulatory bodies. Search terms combined *LLM agent security*, *prompt injection*, *indirect prompt injection*, *runtime guardrail*, *agent monitoring*, *tool misuse*, *financial agent safety*, *probability calibration*, and *cost-sensitive decision*. Peer-reviewed publications were preferred. Preprints were included where they represent current work in a field that moves faster than conference cycles, and each is identified as a preprint in the reference list. An update pass was carried out in September 2026, and it identified several 2026 preprints that overlap directly with the design studied here. They are reviewed explicitly rather than omitted.

Two conventions apply throughout. First, performance figures are reported as stated by the authors of each study, on that study's own benchmark, models, and settings. They characterize individual systems and are not comparable across studies. Second, because no screening statistics were recorded, the chapter does not claim exhaustive coverage. Statements about what "the reviewed work" does or does not report are bounded by the sources cited in this chapter.

## 2.2 The AI-Agent Security Problem

An LLM-based autonomous agent can be described as a system in which a language model serves as the controller for perception, reasoning, planning, and action in pursuit of a task (L. Wang et al., 2024). The ReAct paradigm (Yao et al., 2023) made explicit the execution pattern that most of the systems reviewed here assume: the model interleaves reasoning traces with actions, and the observations returned by those actions re-enter its context and shape the next step. This loop is what makes agents useful. It is also what makes them attackable, because every observation is an input that the model interprets and on which it may act.

Three structural properties distinguish agent security from the security of a conventional classifier. First, an agent receives input through several channels of different trustworthiness: the system prompt, the user's request, tool outputs, retrieved documents, and stored memory. Second, the agent is stateful across a trajectory, so content that enters at one step can influence an action several steps later. Third, the agent's outputs include actions with external effects, so an error or a successful manipulation does not remain in the text domain.

Risk arises even without an adversary. Ruan et al. (2024) evaluated LLM agents in an LM-emulated sandbox of 36 high-stakes tools and 144 test cases and reported that even the safest agent they tested exhibited risky failures in 23.9% of cases, with 68.8% of the identified failures judged to be valid real-world failures. The presence of an adversary adds deliberate pressure on exactly the channels and actions described above, which is the subject of the next section.

**Synthesis.** The literature establishes that agent risk is located at the interaction between the model, its input channels, its accumulated state, and its tools. A defense that inspects only the user's input, or only the final text output, does not observe the point at which an agent's decision becomes an external effect.

## 2.3 Prompt Injection and Indirect Prompt Injection

The OWASP Gen AI Security Project lists prompt injection as the first risk for LLM applications in its 2025 list. It distinguishes direct prompt injection, in which a user's prompt alters the model's behavior in unintended ways, from indirect prompt injection, in which the model accepts input from external sources such as websites or files and that content alters its behavior (OWASP Gen AI Security Project, 2025). For tool-using agents, the indirect form is the more consequential, because the attacker does not need access to the user channel.

Greshake et al. (2023) demonstrated that adversarial instructions placed in data that an LLM-integrated application retrieves can compromise the application remotely, without direct access to its interface. Y. Liu et al. (2024) moved the field from individual demonstrations toward systematic evaluation by proposing a framework that formalizes prompt injection attacks and by benchmarking five attacks and ten defenses across ten LLMs and seven tasks.

Several benchmarks quantify the threat for agents specifically. InjecAgent (Zhan et al., 2024) contains 1,054 test cases covering 17 user tools and 62 attacker tools across two attack intentions, direct harm and data stealing. Across 30 agents, a ReAct-prompted GPT-4 agent was vulnerable 24% of the time, and the success rate nearly doubled when the injected instruction was reinforced with a hacking prompt. Agent Security Bench (ASB; H. Zhang et al., 2025) covers 10 scenarios, including finance, with 10 agents, more than 400 tools, and 27 attack and defense methods. Across 13 LLM backbones it reported a highest average attack success rate of 84.30%. AgentDojo (Debenedetti et al., 2024) provides 97 realistic tasks and 629 security test cases across environments that include e-banking, and it measures both utility and security. Its authors report that current models fail many tasks even without attacks and that existing attacks break some security properties but not all.

Attacks can also persist across interactions. AgentPoison (Z. Chen et al., 2024) poisons an agent's memory or knowledge base so that a trigger retrieves malicious demonstrations. The authors report an average attack success rate above 80% with a poison rate below 0.1% and less than 1% impact on benign performance.

**Synthesis.** Indirect prompt injection enters through the observation channel after the user's request has been received. Its effect becomes visible, and preventable, when the agent proposes an action that serves the attacker's objective. The benchmark evidence establishes the threat for tool-using agents, including agents operating on financial tools, but the reported rates depend strongly on the benchmark, the model, and the attack template, and they cannot be pooled or ranked across studies.

## 2.4 Runtime Guardrails and Agent Security Architectures

Defenses that operate while the agent runs fall into four broad design families. The distinction matters because the families answer different questions, and a system should not be judged deficient for omitting a capability outside its stated purpose.

### 2.4.1 Defenses by construction

CaMeL (Debenedetti et al., 2025) prevents prompt injection from affecting program execution by extracting control and data flow from the trusted user query and enforcing capability-based security policies on tool access, so that untrusted data cannot change what the program does. In AgentDojo it solved 77% of tasks with provable security, compared with 84% for the undefended system. The guarantee is strong for the class of attacks it addresses. It is obtained by changing how the agent's execution is structured rather than by estimating risk.

### 2.4.2 Deterministic policy enforcement

Progent (Shi et al., 2025) enforces privilege control over agent tool calls through explicit policies. AgentSpec (H. Wang et al., 2026) provides a domain-specific language of triggers, predicates, and enforcement actions. Its authors report that it prevents unsafe executions in over 90% of code-agent cases, eliminates all hazardous actions in the embodied-agent setting, enforces 100% compliance for autonomous vehicles, and adds overheads in milliseconds. Rules generated automatically by an LLM reached 95.56% precision and 70.96% recall for embodied agents. Deterministic enforcement is auditable and fast, but it evaluates whether an action is *permitted* under a specified policy. It does not estimate how likely a permitted action is to have been induced by an adversary.

### 2.4.3 Learned and LLM-based guardrails

What unites the third family is that the check itself is learned or generated rather than written by hand. LlamaFirewall (Chennabasappa et al., 2025) composes three such checks: PromptGuard 2, a jailbreak and injection detector; Agent Alignment Checks, a chain-of-thought auditor that inspects agent reasoning for prompt injection and goal misalignment; and CodeShield, an online static analyzer for generated code. In GuardAgent (Xiang et al., 2025) the generation is of code: safety requirements are converted into executable guardrail code, for which the authors reported guardrail accuracies above 98% and 83% on two benchmarks. AGrail (Luo et al., 2025) goes further and keeps optimizing its safety checks against task-specific and systemic risks after deployment. ShieldAgent (Z. Chen, Kang, & Li, 2025) instead extracts verifiable rules from policy documents and structures them into action-based probabilistic rule circuits; its authors reported an average improvement of 11.3% over prior methods with 90.1% recall, while reducing API queries by 64.7% and inference time by 58.2%.

### 2.4.4 Integrated runtime layers

A fourth family places a dedicated layer around the agent that combines several functions. OpenClaw PRISM (F. Li, 2026) instruments ten lifecycle hooks, including message ingress, tool execution, and outbound messaging, and combines heuristic and LLM scanning with conversation- and session-scoped risk accumulation that decays over time. Its author describes the reported results as preliminary. MI9 (C. L. Wang et al., 2025) is a runtime governance framework with six components: an agency-risk index, agent-semantic telemetry, continuous authorization monitoring, finite-state-machine conformance engines, goal-conditioned drift detection, and graduated containment.

Three 2026 preprints are particularly close to the design studied in this thesis and are therefore described in more detail.

**SafeAgent** (H. Liu et al., 2026) consists of a runtime controller that mediates actions in the agent loop and a context-aware decision core over persistent session state. The core's operators for risk encoding, advantage–cost modeling, consequence simulation, and policy arbitration are realized through LLM reasoning rather than formal equations. The action space includes context sanitization, replanning, rollback, session termination, tool-argument rewriting, and human approval. SafeAgent was evaluated on ASB and InjecAgent using attack success rate and performance under no attack. Its ablations show that a policy-weighting setting moves the system between safety-first and task-first operating points. The paper does not address probability calibration and does not report latency, which its authors acknowledge as a limitation in terms of computational overhead.

**AgentTrust** (C. Yang, 2026) intercepts agent tool use through a pipeline of command normalization, pattern-based feature extraction, 170 configurable policy rules, analyzer-based risk scoring, session-based chain detection, and optional LLM judgment. Risk is aggregated by taking the maximum severity over the signals that fire, and the system returns one of four verdicts: allow, warn, block, or review. Confidence is assigned by a step function of evidence strength rather than by probabilistic calibration. The authors report component ablations with verdict accuracy, false-negative rate, and latency; a rule-only configuration reached 95.0% verdict accuracy and 73.7% risk-level accuracy at low-millisecond latency, and verdict accuracy was 96.7% on an external set of 630 scenarios. Reversibility is part of the labeling rubric.

**NEXUS** (Hossain et al., 2026) evaluates the plan an agent proposes before execution. It combines deterministic safety rules, argument-level inspection, and a logistic-regression risk score over 99 plan features, including an irreversibility indicator and estimated cost. The score is calibrated by Platt scaling, with isotonic regression also evaluated. On a 128-instance held-out test set the expected calibration error fell from 0.085 for the raw model to 0.013 after Platt scaling, using a 60-instance calibration split. The deployed policy selects among four interventions (allow, block, request confirmation, or request revision) through a rule cascade in which the calibrated score gates certain cases. The paper also defines an expected-loss objective with fixed costs for each intervention. The authors report a median decision latency of 0.205 ms and caution that results on their author-generated templates should be read as upper bounds rather than deployment estimates.

**Synthesis.** Runtime interception of agent actions, graduated verdicts that include human review, hybrids of rules and learned scores, calibrated logistic risk scores, and component ablations that report latency are all present in the reviewed literature. None of these can be claimed as new by a thesis entering the field in 2026. What differs across systems is how evidence is turned into a decision: by capability policy (CaMeL), by rule (Progent, AgentSpec, AgentTrust), by LLM reasoning (SafeAgent, LlamaFirewall's alignment checks), or by a rule cascade gated by a calibrated score (NEXUS).

## 2.5 Stateful and Trajectory-Aware Protection

Some attacks have no single anomalous step. An agent may first read sensitive data, then add a payee, and only later transfer funds, with each step plausible in isolation. The literature responds by making protection stateful.

MI9 includes goal-conditioned drift detection and conformance checking against expected behavior (C. L. Wang et al., 2025). PRISM accumulates risk over a conversation or session with time-based decay (F. Li, 2026). ProbGuard (H. Wang et al., 2025, accepted to ASE 2026) models agent behavior as a discrete-time Markov chain and anticipates safety violations through probabilistic prediction of reaching unsafe states. SafeAgent treats security as a stateful decision problem over evolving interaction trajectories (H. Liu et al., 2026). FinHarness (Jia et al., 2026) tracks user intent across multiple interactions in its Query Monitor. DreamGuard (Lin et al., 2026), which appeared in August 2026, maintains a recurrent latent representation of the trajectory to detect gradual drift toward hazardous outcomes, at approximately 25 ms per evaluation.

Classical sequential change detection offers a statistically grounded alternative for accumulating evidence. The cumulative sum (CUSUM) procedure, introduced by Page (1954), accumulates log-likelihood-ratio evidence and resets at zero, and its properties are treated in detail by Basseville and Nikiforov (1993).

The empirical value of trajectory components depends on whether the evaluation data contain genuinely multi-step attacks. AgentTrust's own ablation found that its session tracker had no measurable effect on either of its benchmarks (C. Yang, 2026), which suggests that single-action signals dominated the scenarios tested.

**Synthesis.** Stateful and trajectory-aware protection is an active and well-populated area. A thesis that adds trajectory analysis must show that its evaluation data contain the multi-step behavior the analysis is meant to detect. Otherwise the component adds complexity without measurable effect.

## 2.6 Tool-Use and Action-Boundary Security

The point at which a proposed tool call is released to the environment is the last point at which an adversarially induced action can be prevented rather than repaired. Several lines of work focus on this boundary.

Progent and AgentSpec enforce policies on tool calls (Shi et al., 2025; H. Wang et al., 2026), and CaMeL constrains which data may flow into tool arguments (Debenedetti et al., 2025). ProvenanceGuard (She et al., 2026) formulates misalignment detection as the question of whether a proposed tool call is supported by traceable evidence in the agent's context. Compared with an LLM-as-a-judge baseline on Agent-SafetyBench, it reduced the error rate on misaligned traces from 44.3% to 2.1%. This provenance question, whether an action's arguments can be traced to trusted sources, is directly relevant to indirect prompt injection, where the attacker supplies values such as an account identifier inside untrusted content.

Other work intervenes before or around the action. Thought-Aligner (Jiang et al., 2025, accepted to ICML 2026) corrects unsafe intermediate thoughts before action execution and reported raising behavioral safety from approximately 50% to approximately 90% on average. Cordon (Z. Chen et al., 2026) provides a transactional runtime in which the effects of agent actions are staged and validated before commitment. The Actuarial Action Interface of H.-H. Chen (2026) takes a consequence-pricing view: agent actions are priced deterministically against reserved capital, and an Authority Frontier measures how much operational authority an agent receives at different budget levels.

**Synthesis.** Pre-execution mediation at the action boundary, provenance-based evidence about tool arguments, and consequence-dependent control of actions all have published precedents. H.-H. Chen (2026) in particular establishes that pricing the consequence of an agent action before execution is not new. What that work does not model is an estimated probability that a specific action was induced by an adversary. It prices the action's consequence irrespective of how the action arose.

## 2.7 Financial-Agent Security Requirements

Financial agents make the consequences of an action-boundary failure concrete. Tools that initiate transfers, schedule or modify recurring payments, change account settings, or read customer data expose value, credentials, and personal information to manipulation.

Z. Chen, J. Chen, et al. (2025) argue that conventional evaluation of financial LLM agents, based on accuracy and return metrics, gives an illusion of reliability while overlooking vulnerabilities such as hallucinated facts, stale data, and adversarial prompt manipulation. They recommend auditing risk-aware metrics and treating a safety budget as a primary success criterion. FinVault (Z. Yang et al., 2026) was introduced as an execution-grounded security benchmark for financial agents, built from 31 regulatory case-driven sandbox scenarios, 107 real-world vulnerabilities, and 963 test cases. Its authors reported attack success rates of up to 50.0% on the strongest models they tested and 6.7% for the most robust configuration. Its arXiv version was withdrawn in July 2026 by its authors, who cited legal, intellectual-property, and affiliation concerns. It is therefore cited here only as a withdrawn preprint and is not used in this thesis's evaluation.

FinHarness (Jia et al., 2026) is the closest domain-specific runtime system. It combines a Query Monitor that tracks intent across interactions, a Tool Monitor that assesses each proposed action, and a Cascade that routes verification between lighter and more capable judges. Its authors report that the routed configuration reduced attack success from 38.3% to 15.0% while largely preserving benign approval, with 4.7 times fewer calls to the advanced judge. ASB also includes a finance scenario among its ten (H. Zhang et al., 2025).

Regulation adds requirements for record-keeping and human control. Regulation (EU) 2024/1689 requires that high-risk AI systems technically allow the automatic recording of events over their lifetime (Article 12) and that they can be effectively overseen by natural persons, including the ability to intervene in or interrupt the system so that it halts in a safe state (Article 14) (European Parliament & Council of the European Union, 2024). Whether a given financial agent falls within a high-risk category depends on its use and is not assessed in this thesis. The provisions are used here only as motivation for two design properties: an audit record for every decision and an explicit route to human review.

From this literature, six requirements for a runtime layer protecting a financial agent can be stated:

- **R1.** Proposed actions are mediated before they are released to the environment.
- **R2.** The decision uses evidence about whether an action's arguments originate in untrusted content.
- **R3.** Actions with different consequences can receive different responses at the same estimated probability.
- **R4.** Human review is available as a response.
- **R5.** Every decision produces a record of the evidence and quantities behind it.
- **R6.** Security is measured together with benign task utility, so that a defense cannot appear effective merely by blocking legitimate work.

**Synthesis.** Financial-agent runtime safety is not an unaddressed domain. FinHarness addresses it directly, and consequence pricing has been proposed by H.-H. Chen (2026). The evidence base is nevertheless small, largely preprint-based, and in one case withdrawn, which makes careful evaluation on a reproducible open benchmark valuable.

## 2.8 Detection and Classification Approaches

Detection approaches differ in what they inspect and how they decide. Classifier-based detectors such as PromptGuard 2 score text for jailbreak or injection content (Chennabasappa et al., 2025). LLM-based auditors, such as LlamaFirewall's alignment checks, inspect the agent's reasoning for goal misalignment. Rule- and pattern-based detectors, such as AgentTrust's regular-expression features and policies (C. Yang, 2026), are fast and inspectable but bounded by their rule coverage. Provenance analysis asks whether an action is supported by evidence (She et al., 2026). Input transformations take a different route: spotlighting marks the provenance of untrusted input so the model can distinguish it from instructions, and its authors reported reducing attack success from above 50% to below 2% with GPT-family models (Hines et al., 2024).

Two methodological cautions apply to learned detectors in security. Arp et al. (2022) analyzed learning-based security systems published at top security venues and identified pitfalls in design, implementation, and evaluation that lead to unrealistic performance estimates and misleading interpretations. Recent audits of agent-safety benchmarks reinforce this caution. Y. Wang et al. (2026) found that metric design flaws and small panel sizes in four prominent benchmarks produce inconsistent model rankings, and that higher capability can correlate with worse scores on safety measures. M. Q. Li et al. (2026) examined 40 agent-safety benchmarks and found that the choice of benchmark can yield contradictory safety conclusions, with concordance analysis showing essentially no agreement across evaluation approaches.

**Synthesis.** Individual detectors are evadable and their benchmark scores are fragile. A detector's output is better treated as one piece of evidence than as a verdict, and evaluations must control for leakage between training and test data, report benign utility alongside attack success, and avoid pooling results across benchmarks with different definitions.

## 2.9 Probability Calibration

A classifier is calibrated when its predicted probabilities agree with observed frequencies. Guo et al. (2017) define perfect calibration as agreement between predicted confidence and the probability of being correct, and measure deviation with the expected calibration error (ECE), a weighted average of the gap between accuracy and confidence over equal-width probability bins. For binary problems, Naeini et al. (2015) define ECE on the probability of the positive class as the weighted absolute difference between the fraction of positive instances and the mean predicted probability in each bin.

Post-hoc calibration methods learn a map from a model's score to a calibrated probability on held-out data. Platt (1999) fitted a sigmoid to support-vector-machine outputs. Guo et al. (2017) describe Platt scaling for the binary case as a logistic transformation of the model's score with two parameters fitted by negative log-likelihood on a validation set, a transformation that preserves the ranking of predictions, and they introduce temperature scaling as a one-parameter variant. Kull et al. (2017) point out that logistic calibration applied to raw scores in the unit interval cannot represent the identity map and propose beta calibration. They also prove that beta calibration with equal shape parameters is equivalent to logistic calibration applied to the log-odds of the score. This result is relevant whenever the model being calibrated is itself a logistic model, because its log-odds are already its natural score.

Calibration of agent-safety scores is established practice. NEXUS calibrates its logistic-regression risk score with Platt scaling and reports ECE and Brier scores with a reliability diagram (Hossain et al., 2026). The limits of calibration for control have also been shown directly. C. Zhang et al. (2026) argue that oversight based on a scalar risk score routed through a threshold targets the wrong quantity: what matters for control is the *intervention advantage*, the expected utility gain from intervening rather than continuing. Two trajectory states can share a risk estimate while differing in whether they are recoverable. In their experiments on ALFWorld, Platt scaling reduced the ECE of a confidence score from 0.463 to 0.006 while control regret under threshold routing remained unchanged at 0.318. They propose an action-conditioned controller trained by replaying the agent from identical decision states and executing alternative actions.

**Synthesis.** Calibration makes a score interpretable as a probability, which is necessary whenever a decision rule multiplies that probability by a cost. It is not sufficient for good control, and it does not make scalar routing aware of recoverability. A thesis that uses calibration must therefore neither claim calibration as a contribution nor claim that calibration improves control, and it should report calibration quality separately from control outcomes.

## 2.10 Runtime Decision and Mitigation

The reviewed systems turn evidence into action in several ways: by rule verdicts with maximum-severity aggregation (C. Yang, 2026), by thresholds on a predicted probability (H. Wang et al., 2025), by a rule cascade gated by a calibrated score (Hossain et al., 2026), by routing verification between judges (Jia et al., 2026), by LLM-based arbitration over candidate recoveries (H. Liu et al., 2026), by deterministic pricing of action consequence (H.-H. Chen, 2026), and by action-conditioned value estimation (C. Zhang et al., 2026). A working paper by Jackson (2025), listed on SSRN as *Designing a policy engine for agentic AI systems: From governance requirements to runtime enforcement*, appears from its title to address the same question. Its full text returned an access error throughout the September 2026 verification pass, so its mechanism is not described here. It is not peer reviewed, and no claim in this thesis rests on it.

Decision theory provides a classical basis for choosing among responses with different costs. Elkan (2001) states that an example should be assigned the prediction with the lowest expected cost, computed from the conditional probability of each class and a cost matrix whose entries give the cost of each prediction for each true class. Chow (1970) analyzed the tradeoff between recognition error and rejection, providing the classical basis for withholding an automatic decision. NEXUS defines an expected-loss objective with fixed costs for allow, revise, confirm, and block (Hossain et al., 2026). Its deployed policy, however, is a rule cascade in which the learned score adjudicates particular cases, not a per-decision minimization of conditional risk.

Mitigation is graduated in most mature systems. MI9 uses graduated containment (C. L. Wang et al., 2025); SafeAgent selects among sanitization, replanning, rollback, termination, argument rewriting, and human approval (H. Liu et al., 2026); AgentTrust distinguishes warn and review from allow and block (C. Yang, 2026); NEXUS requests confirmation or revision (Hossain et al., 2026); and Cordon stages effects before commitment (Z. Chen et al., 2026). Human review is the operational form of the oversight requirement discussed in Section 2.7.

**Synthesis.** Graduated interventions, including human review, are standard. Two questions remain open. The first is how an estimated probability of adversarial induction and a declared consequence should be combined when choosing among interventions. The second is how effective each intervention actually is: SafeAgent's ablations and the intervention-advantage argument of C. Zhang et al. (2026) both indicate that the value of an intervention depends on what it achieves, not only on the risk estimate that triggered it.

## 2.11 Explainability and Auditability

Additive feature attribution explains a prediction as a sum of per-feature contributions. Lundberg and Lee (2017) unified such methods under Shapley values and showed that, for a linear model under an assumption of feature independence, the attribution of each feature is its coefficient multiplied by the feature's deviation from its expected value. For a linear score this decomposition is exact and costs no more than computing the score.

Auditability in agent security is addressed in several forms. NEXUS traces each decision to a named rule, an argument-inspector finding, or a calibrated threshold crossing (Hossain et al., 2026). AgentTrust reports the rules that fired (C. Yang, 2026). ShieldAgent derives verifiable rules from policy documents (Z. Chen, Kang, & Li, 2025). ProvenanceGuard grounds decisions in traceable evidence (She et al., 2026). PRISM provides tamper-evident auditing (F. Li, 2026). The regulatory requirement for automatic event logging in high-risk systems (European Parliament & Council of the European Union, 2024, Article 12) gives these properties practical weight.

**Synthesis.** Auditable decision records are widely provided. A linear attribution of a learned score adds a numerical decomposition of that score, but it is an established technique and not a distinguishing explanation mechanism. In a runtime decision layer it can support an audit record, provided it is not presented as a novel contribution and does not influence the decision itself.

## 2.12 Evaluation Benchmarks and Datasets

Table 2.1 summarizes the benchmarks relevant to runtime protection of tool-using agents.

**Table 2.1. Benchmarks relevant to runtime agent security**

| Benchmark | Content (as reported) | Utility measured | Relevance and caveats |
|---|---|---|---|
| AgentDojo (Debenedetti et al., 2024) | 97 tasks and 629 security test cases across environments including e-banking; extensible to new tasks, defenses, and adaptive attacks | Yes | Open source; security and utility determined by checks on environment state; the banking suite is directly relevant to financial agents |
| InjecAgent (Zhan et al., 2024) | 1,054 indirect-injection test cases; 17 user tools, 62 attacker tools | No | Short cases suited to isolating injection detection |
| ASB (H. Zhang et al., 2025) | 10 scenarios including finance; more than 400 tools; 27 attack and defense methods | Yes | Broad attack coverage, including memory poisoning and mixed attacks |
| ToolEmu (Ruan et al., 2024) | 36 toolkits and 144 test cases in an LM-emulated sandbox | — | Risk without an adversary; emulated rather than executed tools |
| FinVault (Z. Yang et al., 2026) | 31 scenarios, 107 vulnerabilities, 963 test cases | Reported | arXiv version withdrawn in July 2026; not used in this thesis |
| NEXUS-Bench (Hossain et al., 2026) | 300/63/128 train/validation/test synthetic instances and further splits | — | Author-generated templates; results described by the authors as upper bounds |

The validity audits discussed in Section 2.8 apply to all of these (M. Q. Li et al., 2026; Y. Wang et al., 2026). Their practical implications for this thesis are that results should be reported per benchmark, that benign utility must accompany attack success, and that the number of distinct tasks, rather than the number of generated runs, limits what can be concluded.

**Synthesis.** AgentDojo's banking environment offers an open, executable, and state-checked setting for a financial tool-using agent, with separate utility and security checks. Its limitations, notably a small number of distinct tasks, are methodological constraints to be addressed in the evaluation design rather than reasons to prefer less reproducible benchmarks.

## 2.13 Comparative Synthesis

Table 2.2 compares the reviewed systems along the dimensions that matter for the design studied in this thesis. A mark indicates that the property is reported in the source material consulted for this review. A dash means that the property was not reported there, not that the system is deficient. The final row describes what REM is designed to investigate and is not a result.

**Table 2.2. Comparison of reviewed runtime protection approaches**

| Approach | Decision basis | Calibrated probability | Consequence or reversibility used | Human review / graduated response | Utility reported | Latency reported | Financial focus |
|---|---|---|---|---|---|---|---|
| CaMeL (Debenedetti et al., 2025) | Capability and data-flow policy | — | — | — | ✓ | — | — |
| Progent (Shi et al., 2025) | Privilege policy | — | — | — | — | — | — |
| AgentSpec (H. Wang et al., 2026) | Rules (DSL) | — | — | — | — | ✓ | — |
| ShieldAgent (Z. Chen, Kang, & Li, 2025) | Probabilistic rule circuits | — | — | — | — | ✓ | — |
| MI9 (C. L. Wang et al., 2025) | Governance components; agency-risk index | — | — | ✓ (graduated containment) | — | — | — |
| PRISM (F. Li, 2026) | Hooks, scanning, accumulated session risk | — | — | — | — | ✓ (microbenchmarks) | — |
| ProbGuard (H. Wang et al., 2025) | Predicted probability of unsafe states | — | — | — | — | — | — |
| ProvenanceGuard (She et al., 2026) | Evidence support for tool calls | — | — | — | — | — | — |
| FinHarness (Jia et al., 2026) | Monitors and judge cascade | — | — | — | ✓ (benign approval) | — | ✓ |
| H.-H. Chen (2026) | Deterministic pricing against reserved capital | — | ✓ | — | — | — | Partial (actuarial framing) |
| NEXUS (Hossain et al., 2026) | Rules, argument inspection, calibrated logistic score in a cascade | ✓ | ✓ | ✓ | ✓ (paired benign cases) | ✓ | — |
| SafeAgent (H. Liu et al., 2026) | LLM-based operators and policy arbitration | — | ✓ (LLM consequence simulation) | ✓ | ✓ | — | — |
| AgentTrust (C. Yang, 2026) | Rules with maximum-severity aggregation | — (heuristic confidence) | ✓ (labeling rubric) | ✓ | — | ✓ | — |
| C. Zhang et al. (2026) | Action-conditioned intervention value | Analyzed | — | — | Regret | — | — |
| **REM (investigated in this thesis)** | Calibrated per-step probability combined with tier-indexed losses in an expected-loss rule | Designed | Designed (consequence tiers) | Designed (Escalate) | Planned | Planned | Planned (AgentDojo banking) |

Read together, the table shows that each individual property in REM's design already appears in prior work. Calibrated logistic risk scoring and a four-way intervention set appear in NEXUS. Consequence-dependent control appears in H.-H. Chen (2026), NEXUS, AgentTrust, and SafeAgent. Human review appears in several systems, and latency and component ablation are reported by AgentTrust and NEXUS. Financial runtime safety is addressed by FinHarness. The limits of calibration for control are established by C. Zhang et al. (2026).

The reviewed studies differ in the combination they use and in what they measure. NEXUS evaluates plans on author-generated templates and combines its calibrated score with rules through a cascade. H.-H. Chen (2026) prices consequence without estimating adversarial induction. FinHarness addresses the financial domain with monitors and judges rather than a calibrated probability and declared losses. SafeAgent reasons about consequences through an LLM and does not report calibration or latency. AgentTrust does not use a calibrated probability.

## 2.14 Research Gap

The gap addressed by this thesis is not the absence of runtime guardrails, probability calibration, graduated interventions, human review, provenance analysis, or consequence-aware control. Each of these is present in the literature reviewed above.

Among the studies reviewed in this chapter, none reports an empirical evaluation of a non-invasive runtime layer for a financial tool-using agent that combines (i) provenance-based evidence about proposed financial actions, (ii) a calibrated per-step probability that the proposed action is adversarially induced, (iii) a decision that minimizes expected loss over Allow, Modify, Escalate, and Block using losses declared per consequence tier, and (iv) deterministic mitigation, with attack success, benign utility, intervention behavior, and latency measured separately and compared against a consequence-independent baseline that uses the same estimator.

This is an empirical and integrative gap. It concerns the combination and evaluation of established mechanisms under indirect prompt injection, not the absence of any of those mechanisms and not a new learning algorithm. The statement is bounded by the sources reviewed and by the September 2026 update. Identification of a study that reports this combination and evaluation would require the contribution of this thesis to be revised accordingly.

## 2.15 Positioning of REM

REM is positioned as a runtime mediation layer between a financial tool-using agent and its environment, organized in five layers: Input & Context, Detection, Behavioral Analysis, Decision Engine, and Mitigation. Its design reuses established mechanisms and attributes each to its source.

The literature places four constraints on how REM is studied:

- **Relation to NEXUS.** REM does not claim calibrated logistic risk scoring or a four-way intervention set. It differs in evaluating each proposed tool call at the action boundary of an executing agent under indirect injection, and in selecting the verdict by minimizing conditional risk with tier-indexed losses rather than through a rule cascade.
- **Relation to C. Zhang et al. (2026).** REM does not claim that calibration improves control. It reports calibration quality and control outcomes separately, and it acknowledges that a scalar probability cannot represent whether an adversarial trajectory remains recoverable.
- **Relation to H.-H. Chen (2026), SafeAgent, and AgentTrust.** REM does not claim consequence-aware control, human escalation, or component ablation with latency as new. Its consequence tiers are declared policy inputs, and its losses are reported across a declared grid rather than as fixed truths.
- **Relation to FinHarness.** REM does not claim to be the first runtime protection for financial agents. It studies a different decision mechanism, based on a calibrated probability and declared losses rather than judge routing, on an open and executable banking benchmark.

Table 2.3 traces the requirements of Section 2.7 to the parts of Chapter 3 that address them.

**Table 2.3. Requirements derived from the literature and their treatment in Chapter 3**

| Requirement | Literature basis | Treatment in Chapter 3 |
|---|---|---|
| R1 Pre-execution mediation | Sections 2.4, 2.6 | REM intercepts each proposed tool call before release (Sections 3.2, 3.10) |
| R2 Provenance evidence for action arguments | Section 2.6 | Action-provenance features in the Behavioral Analysis Layer (Section 3.6) |
| R3 Consequence-differentiated responses | Sections 2.6, 2.10 | Consequence tiers and tier-indexed losses (Section 3.7) |
| R4 Human review | Sections 2.7, 2.10 | Escalate verdict (Sections 3.7, 3.8) |
| R5 Audit record | Sections 2.7, 2.11 | Audit record with linear attribution, never used for the verdict (Section 3.7.6) |
| R6 Joint security and utility measurement | Sections 2.7, 2.8, 2.12 | Primary metrics and baseline comparison (Sections 3.11, 3.12) |

## 2.16 Chapter Summary

This chapter reviewed the literature on runtime protection of LLM agents with a focus on financial tool use. Indirect prompt injection is a demonstrated threat whose effect becomes preventable at the action boundary. Runtime guardrails and integrated protection layers already provide interception, graduated verdicts with human review, rule and learned hybrids, calibrated risk scores, stateful analysis, provenance checks, consequence pricing, and component ablations with latency. Calibration is necessary for interpreting a probability in a cost-based decision but has been shown not to be sufficient for good control. Financial-agent runtime safety has begun to be addressed directly, but on a small and partly withdrawn evidence base.

The research gap is accordingly stated as an empirical and integrative one: the evaluation, on an open executable banking benchmark, of a runtime layer that combines provenance-based action evidence, a calibrated per-step probability, consequence-tiered expected-loss decisions, and deterministic mitigation, measured jointly for security, utility, intervention behavior, and latency against a consequence-independent baseline. Chapter 3 specifies this methodology.

## References

Arp, D., Quiring, E., Pendlebury, F., Warnecke, A., Pierazzi, F., Wressnegger, C., Cavallaro, L., & Rieck, K. (2022). Dos and don'ts of machine learning in computer security. In *31st USENIX Security Symposium*. USENIX Association. https://arxiv.org/abs/2010.09470

Basseville, M., & Nikiforov, I. V. (1993). *Detection of abrupt changes: Theory and application*. Prentice Hall. https://people.irisa.fr/Michele.Basseville/kniga/

Chen, H.-H. (2026). *Insuring every action: An authority frontier framework for runtime actuarial control of autonomous AI agents* (arXiv:2605.25632) [Preprint]. arXiv. https://arxiv.org/abs/2605.25632

Chen, Z., Chen, J., Chen, J., & Sra, M. (2025). *Standard benchmarks fail — Auditing LLM agents in finance must prioritize risk* (arXiv:2502.15865) [Preprint]. arXiv. https://arxiv.org/abs/2502.15865

Chen, Z., Kang, M., & Li, B. (2025). *ShieldAgent: Shielding agents via verifiable safety policy reasoning* (arXiv:2503.22738) [Preprint]. arXiv. https://arxiv.org/abs/2503.22738

Chen, Z., Liu, H., Xu, D., Dong, D., Li, J., Pu, B., & Zhai, J. (2026). *Cordon: Semantic transactions for tool-using LLM agents* (arXiv:2606.17573) [Preprint]. arXiv. https://arxiv.org/abs/2606.17573

Chen, Z., Xiang, Z., Xiao, C., Song, D., & Li, B. (2024). *AgentPoison: Red-teaming LLM agents via poisoning memory or knowledge bases* (arXiv:2407.12784) [Preprint]. arXiv. https://arxiv.org/abs/2407.12784

Chennabasappa, S., Nikolaidis, C., Song, D., Molnar, D., Ding, S., Wan, S., Whitman, S., Deason, L., Doucette, N., Montilla, A., Gampa, A., de Paola, B., Gabi, D., Crnkovich, J., Testud, J.-C., He, K., Chaturvedi, R., Zhou, W., & Saxe, J. (2025). *LlamaFirewall: An open source guardrail system for building secure AI agents* (arXiv:2505.03574) [Preprint]. arXiv. https://arxiv.org/abs/2505.03574

Chow, C. K. (1970). On optimum recognition error and reject tradeoff. *IEEE Transactions on Information Theory, 16*(1), 41–46. https://doi.org/10.1109/TIT.1970.1054406

Debenedetti, E., Shumailov, I., Fan, T., Hayes, J., Carlini, N., Fabian, D., Kern, C., Shi, C., Terzis, A., & Tramèr, F. (2025). *Defeating prompt injections by design* (arXiv:2503.18813) [Preprint]. arXiv. https://arxiv.org/abs/2503.18813

Debenedetti, E., Zhang, J., Balunović, M., Beurer-Kellner, L., Fischer, M., & Tramèr, F. (2024). *AgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents* (arXiv:2406.13352). arXiv. https://arxiv.org/abs/2406.13352

Elkan, C. (2001). The foundations of cost-sensitive learning. In *Proceedings of the Seventeenth International Joint Conference on Artificial Intelligence (IJCAI-01)* (pp. 973–978). https://cseweb.ucsd.edu/~elkan/rescale.pdf

European Parliament & Council of the European Union. (2024). *Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 laying down harmonised rules on artificial intelligence*. Official Journal of the European Union. https://eur-lex.europa.eu/eli/reg/2024/1689/oj

Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., & Fritz, M. (2023). Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection. In *Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security* (pp. 79–90). ACM. https://doi.org/10.1145/3605764.3623985

Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. In *Proceedings of the 34th International Conference on Machine Learning* (Vol. 70, pp. 1321–1330). PMLR. https://proceedings.mlr.press/v70/guo17a.html

Hines, K., Lopez, G., Hall, M., Zarfati, F., Zunger, Y., & Kiciman, E. (2024). *Defending against indirect prompt injection attacks with spotlighting* (arXiv:2403.14720) [Preprint]. arXiv. https://arxiv.org/abs/2403.14720

Hossain, E., Nipu, M. M. H., Ornee, T. N., Rana, R., & Yousefi, N. (2026). *NEXUS: Structured runtime safety for tool-using LLM agents* (arXiv:2607.19356) [Preprint]. arXiv. https://arxiv.org/abs/2607.19356

Jackson, F. (2025). *Designing a policy engine for agentic AI systems: From governance requirements to runtime enforcement* [Working paper]. SSRN. https://doi.org/10.2139/ssrn.5904104

Jia, H., Liu, Y., Chong, B., Yang, Y., Chen, Y., Liang, J., Li, Q., Lu, H., Xu, K., Zheng, H., Zhang, C., Peng, H., & Yu, P. S. (2026). *FinHarness: An inline lifecycle safety harness for finance LLM agents* (arXiv:2605.27333) [Preprint]. arXiv. https://arxiv.org/abs/2605.27333

Jiang, C., Zhang, W., Pan, X., Hong, G., & Yang, M. (2025). *Think twice before you act: Enhancing agent behavioral safety with thought correction* (arXiv:2505.11063) [Preprint; accepted to ICML 2026]. arXiv. https://arxiv.org/abs/2505.11063

Kull, M., Silva Filho, T., & Flach, P. (2017). Beta calibration: A well-founded and easily implemented improvement on logistic calibration for binary classifiers. In *Proceedings of the 20th International Conference on Artificial Intelligence and Statistics* (Vol. 54, pp. 623–631). PMLR. https://proceedings.mlr.press/v54/kull17a.html

Li, F. (2026). *OpenClaw PRISM: A zero-fork, defense-in-depth runtime security layer for tool-augmented LLM agents* (arXiv:2603.11853) [Preprint]. arXiv. https://arxiv.org/abs/2603.11853

Li, M. Q., Fung, B. C. M., Li, B., Ismail, H., & Iqbal, F. (2026). *Taxonomy and consistency analysis of safety benchmarks for AI agents* (arXiv:2605.16282) [Preprint]. arXiv. https://arxiv.org/abs/2605.16282

Lin, W., Yu, C., Lin, X., Cao, S., Chen, X., Xue, L., Yu, L., Sha, L., & Wu, C. (2026). *DreamGuard: Efficient runtime guardrail for LLM agents via risk-aware world model* (arXiv:2608.05695) [Preprint]. arXiv. https://arxiv.org/abs/2608.05695

Liu, H., Ilyushin, E., Ni, J., & Zhu, M. (2026). *SafeAgent: A runtime protection architecture for agentic systems* (arXiv:2604.17562) [Preprint]. arXiv. https://arxiv.org/abs/2604.17562

Liu, Y., Jia, Y., Geng, R., Jia, J., & Gong, N. Z. (2024). Formalizing and benchmarking prompt injection attacks and defenses. In *33rd USENIX Security Symposium*. USENIX Association. https://arxiv.org/abs/2310.12815

Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. In *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1705.07874

Luo, W., Dai, S., Liu, X., Banerjee, S., Sun, H., Chen, M., & Xiao, C. (2025). AGrail: A lifelong agent guardrail with effective and adaptive safety detection. In *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)* (pp. 8104–8139). Association for Computational Linguistics.

Naeini, M. P., Cooper, G., & Hauskrecht, M. (2015). Obtaining well calibrated probabilities using Bayesian binning. *Proceedings of the AAAI Conference on Artificial Intelligence, 29*(1). https://doi.org/10.1609/aaai.v29i1.9602

OWASP Gen AI Security Project. (2025). *LLM01:2025 Prompt injection*. OWASP Foundation. https://genai.owasp.org/llmrisk/llm01-prompt-injection/

Page, E. S. (1954). Continuous inspection schemes. *Biometrika, 41*(1–2), 100–115. https://doi.org/10.1093/biomet/41.1-2.100

Platt, J. C. (1999). Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. In A. J. Smola, P. Bartlett, B. Schölkopf, & D. Schuurmans (Eds.), *Advances in large margin classifiers* (pp. 61–74). MIT Press.

Ruan, Y., Dong, H., Wang, A., Pitis, S., Zhou, Y., Ba, J., Dubois, Y., Maddison, C. J., & Hashimoto, T. (2024). *Identifying the risks of LM agents with an LM-emulated sandbox* (arXiv:2309.15817). arXiv. https://arxiv.org/abs/2309.15817

She, Y., Liang, Y., & Kang, E. (2026). *Safeguarding LLM agents from misalignment through provenance analysis* (arXiv:2607.01236) [Preprint]. arXiv. https://arxiv.org/abs/2607.01236

Shi, T., He, J., Wang, Z., Li, H., Wu, L., Guo, W., & Song, D. (2025). *Progent: Securing AI agents with privilege control* (arXiv:2504.11703) [Preprint]. arXiv. https://arxiv.org/abs/2504.11703

Wang, C. L., Singhal, T., Kelkar, A., & Tuo, J. (2025). *MI9: An integrated runtime governance framework for agentic AI* (arXiv:2508.03858) [Preprint]. arXiv. https://arxiv.org/abs/2508.03858

Wang, H., Poskitt, C. M., & Sun, J. (2026). AgentSpec: Customizable runtime enforcement for safe and reliable LLM agents. In *Proceedings of the 48th IEEE/ACM International Conference on Software Engineering (ICSE '26)* (pp. 2938–2950). https://arxiv.org/abs/2503.18666

Wang, H., Poskitt, C. M., Wei, J., & Sun, J. (2025). *ProbGuard: Proactive runtime monitoring for LLM agent safety via probabilistic prediction* (arXiv:2508.00500) [Preprint; accepted to ASE 2026]. arXiv. https://arxiv.org/abs/2508.00500

Wang, L., Ma, C., Feng, X., Zhang, Z., Yang, H., Zhang, J., Chen, Z., Tang, J., Chen, X., Lin, Y., Zhao, W. X., Wei, Z., & Wen, J. (2024). A survey on large language model based autonomous agents. *Frontiers of Computer Science, 18*(6), Article 186345. https://doi.org/10.1007/s11704-024-40231-1

Wang, Y., Han, X., Shang, D., Tang, Y., & Liu, B. (2026). *Safety, or just capability? A validity audit of agent-safety benchmarks* (arXiv:2607.28685) [Preprint]. arXiv. https://arxiv.org/abs/2607.28685

Xiang, Z., Zheng, L., Li, Y., Hong, J., Li, Q., Xie, H., Zhang, J., Xiong, Z., Xie, C., Yang, C., Song, D., & Li, B. (2025). *GuardAgent: Safeguard LLM agents by a guard agent via knowledge-enabled reasoning* (arXiv:2406.09187) [Accepted to ICML 2025]. arXiv. https://arxiv.org/abs/2406.09187

Yang, C. (2026). *AgentTrust: Runtime safety evaluation and interception for AI agent tool use* (arXiv:2605.04785) [Preprint]. arXiv. https://arxiv.org/abs/2605.04785

Yang, Z., Li, R., Qiang, Q., Wang, J., Lou, F., Li, M., Cheng, D., Xu, R., Lian, H., Zhang, S., Liang, X., Huang, X., Wei, Z., Liu, Z., Guo, X., Wang, H., Chen, R., & Zhang, L. (2026). *FinVault: Benchmarking financial agent safety in execution-grounded environments* (arXiv:2601.07853) [Withdrawn preprint]. arXiv. https://arxiv.org/abs/2601.07853

Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing reasoning and acting in language models. In *International Conference on Learning Representations*. https://arxiv.org/abs/2210.03629

Zhan, Q., Liang, Z., Ying, Z., & Kang, D. (2024). InjecAgent: Benchmarking indirect prompt injections in tool-integrated large language model agents. In *Findings of the Association for Computational Linguistics: ACL 2024*. https://arxiv.org/abs/2403.02691

Zhang, C., Wan, Z., Yu, X., Wu, J., Wen, Q., Zhou, P., Zhao, W., & Tsang, I. (2026). *Calibration is not control: Why LLM-agent oversight needs intervention* (arXiv:2606.21399) [Preprint]. arXiv. https://arxiv.org/abs/2606.21399

Zhang, H., Huang, J., Mei, K., Yao, Y., Wang, Z., Zhan, C., Wang, H., & Zhang, Y. (2025). Agent Security Bench (ASB): Formalizing and benchmarking attacks and defenses in LLM-based agents. In *International Conference on Learning Representations*. https://arxiv.org/abs/2410.02644
