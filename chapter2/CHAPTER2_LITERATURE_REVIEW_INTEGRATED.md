# CHAPTER TWO
# LITERATURE REVIEW

## 2.1 Introduction

Large language model (LLM) agents no longer only produce text for a human reader. They decompose tasks, call external tools with arguments they generate themselves, read the results of those calls, and act again on what they read. When such an agent operates on financial tools, a single proposed tool call can initiate a transfer, change a payee, modify a scheduled payment, or send customer data to an external recipient. The security question therefore shifts from what a model *says* to what an agent *does*, and specifically to the moment at which a proposed action leaves the agent and takes effect in its environment.

This chapter reviews the literature that bears on protecting such an agent at runtime. Its purpose is not to catalogue systems but to build an argument in eight steps:

1. agents create security risks that differ from those of conventional LLM use;
2. prior research has characterized the main threats and proposed many defenses;
3. those defenses differ in *where* they intervene;
4. they also differ in *what* they observe;
5. some capabilities are now well addressed;
6. others remain fragmented or weakly evidenced;
7. these patterns locate the Runtime Evaluation and Mitigation (REM) framework studied in this thesis;
8. the financial setting raises the stakes of each of these questions.

The research gap stated at the end of the chapter is derived from this comparison rather than asserted in advance.

The chapter proceeds as follows. Section 2.2 explains why agent architecture changes the security problem. Section 2.3 reviews the threats relevant to REM, and Section 2.4 the benchmarks and threat models used to measure them. Section 2.5 organizes defenses by mechanism and point of intervention. Section 2.6 examines runtime monitoring and behavioral analysis, the area that underlies REM's Behavioral Analysis Layer. Section 2.7 reviews the established statistical and algorithmic methods on which a runtime decision layer depends. Section 2.8 compares how runtime systems act on what they detect. Section 2.9 connects this literature to financial-agent execution risk. Section 2.10 compares the reviewed approaches systematically. Section 2.11 synthesizes the comparison critically, and Section 2.12 states the research gap and positions REM.

### 2.1.1 Review approach

The review is a structured narrative review, not a systematic review. Sources were identified through targeted searches of the arXiv preprint server, the ACL Anthology, the Proceedings of Machine Learning Research, the ICLR and NeurIPS proceedings, the USENIX, ACM and IEEE digital libraries, and official documentation from standards and regulatory bodies. Search terms combined *LLM agent security*, *prompt injection*, *indirect prompt injection*, *runtime guardrail*, *agent monitoring*, *tool misuse*, *trajectory monitoring*, *financial agent safety*, *probability calibration*, *sequential change detection*, and *cost-sensitive decision*. The review merges two earlier drafts of this chapter (July and September 2026) with a verification and update pass completed in September 2026. No screening statistics were recorded, so the chapter does not claim exhaustive coverage. Statements about what "the reviewed literature" does or does not report are bounded by the sources cited here and by that date.

Four conventions apply throughout.

- **Source hierarchy.** Peer-reviewed publications are preferred. Original sources are cited for foundational algorithms. The primary paper is cited for each system. Preprints are included where they represent current work in a field that moves faster than publication cycles, and each is identified as a preprint in the reference list. Official sources (OWASP; the EU AI Act) are used only for definitions and regulatory provisions and are not treated as research findings.
- **Reported numbers.** Performance figures are reported as stated by the authors of each study, on that study's own benchmark, models and settings. They characterize individual systems and are not comparable across studies.
- **Claim strength.** The wording of a claim is matched to the evidence behind it. A finding from one study is reported as such ("one study reported…"), not as an established result.
- **Absence of evidence.** In the comparison tables, *not reported* means that the consulted source does not report the property. It does not mean that the system lacks it. *Not applicable* and *not verified* are distinguished from *not reported*.

---

## 2.2 AI Agents and Emerging Security Risks

### 2.2.1 From language models to agents

In the survey literature, an LLM-based autonomous agent is a system in which a language model acts as the controller for perception, reasoning, planning and action in pursuit of a task, supported by memory and tool-use modules (L. Wang et al., 2024). Two capability developments made this architecture practical. The ReAct paradigm interleaves reasoning traces with actions: the model generates a thought, selects an action, receives the environment's observation, and conditions its next step on that observation (Yao et al., 2023). Toolformer showed that a language model can learn which application programming interfaces to call, when to call them, and what arguments to pass (Schick et al., 2023). Together, these works describe the execution pattern that most contemporary agent frameworks still follow. That pattern is a loop of reasoning, tool invocation and observation, which continues until the model judges the task complete.

### 2.2.2 Why agent architecture changes the security problem

The same loop that makes agents useful also creates their attack surface. Three structural properties distinguish agent security from the security of a stand-alone model or a conventional classifier.

- **Several input channels of different trustworthiness.** An agent receives the system prompt, the user's request, tool outputs, retrieved documents and stored memory. Content from all of these channels enters the same context window, and the model interprets all of it.
- **Statefulness across a trajectory.** Content that enters at one step can influence an action several steps later. The unit of security analysis is therefore not a single input–output pair but a trajectory of reasoning, actions and observations.
- **Outputs with external effects.** An agent's outputs include tool calls. An error or a successful manipulation therefore does not remain in the text domain; it becomes a state change in an external system.

Surveys of agent trustworthiness organize threats around the same components: the model "brain", memory, tools, and the interaction between agents and their environment (Yu et al., 2025). The practical implication is that the security-relevant question changes over the course of execution. At the input boundary the question is whether the text is malicious. At the action boundary it is whether this particular action, given everything that preceded it, should be released.

### 2.2.3 Risk without an adversary

Agent risk does not require an attacker. Ruan et al. (2024) evaluated LLM agents in an LM-emulated sandbox with 36 high-stakes toolkits and 144 test cases. They reported that even the safest agent they tested exhibited failures in 23.9% of cases according to their automatic evaluator, and that human evaluators judged 68.8% of the identified failures to be valid real-world failures. The failures arise from the interaction of model, tools and context: for example, executing consequential actions without adequate verification. Such failures are not properties of the model in isolation. An adversary adds deliberate pressure on exactly these channels and actions, which is the subject of Section 2.3.

**Synthesis.** The literature consistently locates agent risk at the interaction between the model, its heterogeneous input channels, its accumulated state and its tools. A defense that inspects only the user's input, or only the final text output, does not observe the point at which an agent's decision becomes an external effect. This observation motivates the attention given in the rest of the chapter to *where* defenses intervene and *what* they observe.

---

## 2.3 Threats Against AI Agents

The OWASP Gen AI Security Project lists prompt injection as the first risk in its 2025 list for LLM applications. It distinguishes *direct* prompt injection, in which a user's prompt alters the model's behavior in unintended ways, from *indirect* prompt injection, in which content from external sources such as websites or files alters that behavior (OWASP Gen AI Security Project, 2025). This practitioner taxonomy is consistent with the academic literature reviewed below and is used here only for terminology. The section concentrates on the threat classes that bear directly on REM: the manipulation of a tool-using agent into proposing an action that serves an attacker rather than the user.

### 2.3.1 Direct prompt injection and malicious instructions

Early demonstrations showed that simple handcrafted inputs could redirect a model toward an attacker's goal ("goal hijacking") or cause it to reveal its instructions ("prompt leaking") (Perez & Ribeiro, 2022). Y. Liu et al. (2024) moved the field from individual demonstrations toward systematic evaluation. They proposed a framework that formalizes prompt injection attacks, showed that existing attacks are special cases of it, and benchmarked five attacks and ten defenses across ten LLMs and seven tasks. For agents, direct injection matters less than its indirect counterpart, because the user of a financial agent is usually the principal the agent serves rather than the adversary. The main detection difficulty is shared by both forms, however: injected instructions are natural language and are distributionally similar to legitimate instructions.

### 2.3.2 Indirect prompt injection

Greshake et al. (2023) demonstrated that adversarial instructions placed in data retrieved by an LLM-integrated application can compromise the application remotely, without any access to its user interface. The model processes the retrieved content as instructions rather than as data. For tool-using agents this is the more consequential variant. The attacker needs only to influence some content that the agent will read, such as an email, a web page, a document or a transaction description. The malicious content then enters through the observation channel *after* the user's request has been received and inspected.

Agent-specific benchmarks quantify the threat. InjecAgent contains 1,054 test cases covering 17 user tools and 62 attacker tools across two attack intentions, direct harm and data stealing. Across the agents evaluated, a ReAct-prompted GPT-4 agent was vulnerable in 24% of cases, and the success rate nearly doubled when the injected instruction was reinforced with a "hacking prompt" (Zhan et al., 2024). Agent Security Bench (ASB) covers ten scenarios, including finance, with ten agents, more than 400 tools and 27 attack and defense methods. Across 13 LLM backbones it reported a highest average attack success rate of 84.30% and found existing defenses often ineffective (H. Zhang et al., 2025).

### 2.3.3 Tool misuse and action manipulation

Tool misuse is the invocation of a legitimate capability in a way that is inconsistent with the user's intent or with policy. Action manipulation is its adversarially induced form: the agent proposes a well-formed call to a permitted tool, but with arguments or at a moment chosen by the attacker. In most injection chains, this is the stage at which internal compromise becomes external effect (H. Zhang et al., 2025; Zhan et al., 2024). The detection difficulty is that a manipulated call is often syntactically valid and individually plausible. Its anomaly lies in its relation to the user's request and to the preceding trajectory, not in the call itself. Several defenses reviewed later formalize exactly this relational question. They ask whether an action serves the user's stated task (F. Jia et al., 2025), whether its arguments are supported by traceable evidence in the context (She et al., 2026), or whether it would still be proposed if the user's request were masked (Zhu et al., 2025).

Harmful behavior can also be requested directly. AgentHarm contains 110 explicitly malicious agent tasks (440 with augmentations) across 11 harm categories, including fraud and cybercrime. Scoring well on it requires a jailbroken agent to retain enough capability to complete a multi-step task (Andriushchenko et al., 2025). This benchmark is relevant to REM mainly as a contrast. Its threat model is a malicious *user*, whereas REM's primary threat model, indirect injection against a benign user's financial agent, places the adversary in the data.

### 2.3.4 Context and memory manipulation

Where an agent maintains long-term memory or retrieves from a knowledge base, an adversary can plant content that is retrieved and acted on later. AgentPoison poisons an agent's memory or retrieval corpus with a small number of malicious demonstrations containing an optimized trigger. Its authors reported an average attack success rate of at least 80%, with less than 1% impact on benign performance, at a poison rate below 0.1% and without any model training (Z. Chen et al., 2024). Memory poisoning separates the write from the activation in time. The eventual retrieval therefore appears legitimate to any observer that lacks information about where the content came from. This is one reason why the provenance of content is increasingly treated as security evidence (Section 2.6.2).

### 2.3.5 Goal drift and multi-step attack propagation

Some compromises have no single anomalous step. An agent may read an attacker-controlled document, add a payee in a later step, and transfer funds after that, with each step plausible in isolation. Several runtime systems target this pattern explicitly. MI9 includes goal-conditioned drift detection (C. L. Wang et al., 2025). FinHarness fuses single-turn intent with cross-turn drift in its query monitor (H. Jia et al., 2026). DreamGuard is motivated by the observation that individually benign-looking actions can gradually move an agent toward hazardous states (Lin et al., 2026). Cordon's authors report that task-level transactional tracking exposes cross-step violations missed by existing defenses (Z. Chen et al., 2026). The threat is therefore well recognized. Whether a given evaluation actually contains such multi-step attacks is a separate empirical question, discussed in Section 2.6.5.

### 2.3.6 Abnormal and repetitive execution

A final class concerns behavior that is abnormal as a *pattern* rather than as a single action: unusually repeated tool calls, unexpected orderings of operations, or sequences that depart from an agent's normal operating profile. The reviewed agent-security literature addresses this mainly through session-level chain detection (C. Yang, 2026), conformance checking against expected behavioral patterns (C. L. Wang et al., 2025), and probabilistic models of state transitions (H. Wang et al., 2025). The underlying concept is older. In the anomaly-detection literature, a sequence of individually normal events whose *combination* is anomalous is a *collective* anomaly (Chandola et al., 2009). Anomaly detection over discrete sequences is a distinct problem formulation with its own methods (Chandola et al., 2012). Section 2.6.3 examines what that literature contributes, and what it cautions, when transferred to agents.

### 2.3.7 Adaptive attackers

Threat evaluations are only as strong as the attacks they include. Zhan et al. (2025) evaluated eight defenses against indirect prompt injection on LLM agents and bypassed all of them with adaptive attacks designed with knowledge of each defense. This finding echoes the earlier conclusion of Y. Liu et al. (2024) that claimed defensive efficacy requires independent verification. It implies that detection results measured against fixed attack templates are upper bounds on robustness, not estimates of it.

**Table 2.1. Threat classes relevant to REM**

| Threat class | Entry point | Temporal scope | Why it is hard to detect | Representative sources |
|---|---|---|---|---|
| Direct prompt injection | User channel | Single turn | Injected instructions resemble legitimate ones | Perez & Ribeiro (2022); Y. Liu et al. (2024) |
| Indirect prompt injection | Observation channel (tool outputs, retrieved content) | Cross-step | Enters after input inspection has concluded | Greshake et al. (2023); Zhan et al. (2024); H. Zhang et al. (2025) |
| Tool misuse / action manipulation | Tool interface | Step or chain | The call is well formed; the anomaly is relational | Zhan et al. (2024); H. Zhang et al. (2025); Andriushchenko et al. (2025) |
| Context and memory manipulation | Memory, retrieval corpus | Cross-session | Write and activation are separated in time | Z. Chen et al. (2024) |
| Goal drift / multi-step propagation | Planning and trajectory | Trajectory | No single step need be anomalous | C. L. Wang et al. (2025); Lin et al. (2026); H. Jia et al. (2026) |
| Abnormal / repetitive execution | Trajectory | Trajectory | Anomaly lies in the pattern (collective anomaly) | Chandola et al. (2009, 2012); C. Yang (2026) |
| Adaptive attacks | Any | Any | Attacks are designed against the specific defense | Zhan et al. (2025) |

**Synthesis.** The threat literature is mature in the sense that the main classes are defined, demonstrated and benchmarked. Two properties recur across them.

- **The decisive channel is the observation channel.** Indirect injection and memory manipulation enter after the user's request, so input-boundary defenses do not observe them.
- **The decisive moment is the proposed action.** Whatever the entry point, the harm materializes when the agent proposes a tool call that serves the attacker. For many threats this is also the last point at which harm can be prevented rather than repaired.

These two properties define the observation point for a runtime layer such as REM. The adaptive-attack evidence adds a caution that applies to every defense reviewed below.

---

## 2.4 AI-Agent Security Benchmarks and Threat Models

Benchmarks operationalize threat models. They also determine what a defense can be shown to achieve, so their construction deserves the same critical attention as the defenses evaluated on them.

**Table 2.2. Benchmarks relevant to runtime protection of tool-using agents**

| Benchmark | Content (as reported) | Threat model | Utility measured | Relevance and caveats |
|---|---|---|---|---|
| AgentDojo (Debenedetti et al., 2024) | 97 user tasks and 629 security test cases in four environments: Workspace, Slack, Travel, Banking | Indirect prompt injection via tool outputs | Yes, jointly with security | Executable and extensible; state-based checks; the Banking suite is directly relevant to financial agents |
| InjecAgent (Zhan et al., 2024) | 1,054 test cases; 17 user tools, 62 attacker tools | Indirect injection (direct harm; data stealing) | No | Short cases, suited to isolating injection detection |
| ASB (H. Zhang et al., 2025) | 10 scenarios including finance; 10 agents; more than 400 tools; 27 attack and defense methods; 7 metrics | Direct and indirect injection, memory poisoning, mixed attacks | Yes | Broad attack coverage |
| AgentHarm (Andriushchenko et al., 2025) | 110 malicious tasks (440 with augmentations); 11 harm categories | Malicious user | Capability retention after jailbreak | Tests refusal of harmful requests, not injection against a benign user |
| ToolEmu (Ruan et al., 2024) | 36 toolkits; 144 test cases; LM-emulated tools | No adversary (risky failures) | Not the focus | Emulated rather than executed tools |
| FinVault (Z. Yang et al., 2026) | 31 regulatory scenarios; 107 vulnerabilities; 963 test cases (as originally reported) | Financial-agent attacks | Benign cases reported | **arXiv version withdrawn by its authors** (legal, intellectual-property and affiliation concerns); not used as evidence in this thesis |
| NEXUS-Bench (Hossain et al., 2026) | Synthetic plan instances; 128-instance held-out test set | Unsafe plans | Paired benign cases | Author-generated templates |

Two recent audits question how far benchmark scores can be interpreted as measurements of "safety". M. Q. Li et al. (2026) catalogued 40 behavioral agent-safety benchmarks published between 2023 and 2026 and proposed a six-axis taxonomy of evaluation methodology. Their consistency analysis, using confidence intervals and Kendall's *W*, found no evidence of ranking concordance across evaluation dimensions, and they concluded that benchmark choice systematically alters reported safety. Y. Wang et al. (2026) ran four benchmarks (R-Judge, InjecAgent, AgentHarm and AgentDojo) under their official implementations on up to 22 models. They identified a metric-validity failure: on a binary trace-judgment benchmark scored by F1, an "always positive" baseline outranked five evaluated models. They also showed that a cross-benchmark correlation moved from −0.64 with seven models to +0.02 with eighteen, an artefact of small panels.

These audits sharpen a caution that the machine-learning-for-security literature raised earlier. Arp et al. (2022) examined 30 papers from top security venues and identified recurring pitfalls in the design, implementation and evaluation of learning-based security systems, including sampling bias, data snooping and inappropriate baselines, that lead to over-optimistic results.

**Synthesis.** For a financial tool-using agent, AgentDojo offers the most suitable open setting among those reviewed. Its Banking environment is executable, its outcomes are checked against environment state, and it measures utility and security separately. The audits nevertheless impose three constraints on any evaluation:

- report results per benchmark rather than pooled across benchmarks;
- report benign utility alongside attack success;
- treat the number of distinct tasks, rather than the number of generated runs, as the limit on what can be concluded.

The withdrawal of FinVault further narrows the verified evidence base for finance-specific evaluation, a point taken up in Section 2.9.

---

## 2.5 Defensive Approaches for AI Agents

Defenses differ along two dimensions that the literature rarely separates explicitly. The first is **where they intervene**: at the input, in the context, in the model, at the policy or tool layer, at runtime around the agent loop, or after an action has taken effect. The second is **what they observe**: an isolated request, an individual tool call, a full action sequence, the integrity of the context, or the consequence of an action. This section organizes defenses by mechanism along both dimensions. Integrated runtime layers, the systems closest to REM, are treated separately in Section 2.8.

**Table 2.3. Where defenses intervene and what they observe**

| Point of intervention | Representative approaches | Primary unit observed | What this position can and cannot see |
|---|---|---|---|
| Input / request | PromptGuard 2 in LlamaFirewall (Chennabasappa et al., 2025); Llama Guard (Inan et al., 2023) | Isolated request or message | Sees what the user sends; does not see content that enters later through tools |
| Context / data provenance | Spotlighting (Hines et al., 2024); CaMeL data-flow separation (Debenedetti et al., 2025) | Untrusted content and its flow | Can mark or isolate untrusted data; depends on correct identification of trust boundaries |
| Model | StruQ (S. Chen et al., 2025) | Model behavior under separated channels | Changes how the model treats data; requires training and model access |
| Policy / tool privilege | Progent (Shi et al., 2025); AgentSpec (H. Wang et al., 2026); Conseca (Tsai & Bagdasarian, 2025) | Individual tool call against a policy | Deterministic and auditable; answers "is this permitted?", not "is this likely induced?" |
| Reasoning / plan | Thought-Aligner (Jiang et al., 2025); TrustAgent (Hua et al., 2024); NEXUS (Hossain et al., 2026) | Intermediate thoughts or a whole plan | Can intervene before actions exist; the plan may change after new observations |
| Runtime, around the agent loop | AlignmentCheck (Chennabasappa et al., 2025); GuardAgent (Xiang et al., 2025); ShieldAgent (Z. Chen, Kang, & Li, 2025); Task Shield (F. Jia et al., 2025); MELON (Zhu et al., 2025); ProvenanceGuard (She et al., 2026) | Proposed action in its context; sometimes the trajectory | Observes the action boundary; cost is latency and false interventions |
| Post-action / transactional | Cordon (Z. Chen et al., 2026) | Staged effects of a task | Can roll back or hold effects; consumes rather than produces a risk judgment |

### 2.5.1 Input- and context-level protection

The earliest defenses operate on text before it reaches the model's decision. Classifier-based detectors score inputs for injection or jailbreak content. PromptGuard 2, part of LlamaFirewall, is designed to operate on raw input and reject obvious attacks (Chennabasappa et al., 2025). Llama Guard classifies both prompts and responses against a configurable safety taxonomy (Inan et al., 2023). Context-level approaches instead try to preserve the distinction between instructions and data. Spotlighting transforms untrusted input, for example by marking or encoding it, so that the model receives a continuous signal of provenance. Its authors reported that it reduced attack success from above 50% to below 2% with GPT-family models, with minimal impact on task performance (Hines et al., 2024).

These approaches are inexpensive and deployable, but they share a structural limitation for agents: they act on text, not on actions. A detector at the input boundary does not observe content that enters later through tool outputs. A transformation that improves the model's discrimination between data and instructions still leaves the final decision to the model. The adaptive-attack results reported by Zhan et al. (2025) indicate that such decisions can be overturned by attacks designed against the defense.

### 2.5.2 Model-level protection

Model-level defenses change the model itself. StruQ separates the prompt and the data into two channels and trains the model, through structured instruction tuning, to follow instructions only in the prompt channel (S. Chen et al., 2025). Unlike input filtering, this approach addresses the root cause identified by Greshake et al. (2023): models do not reliably distinguish instructions from data. It requires training and access to the model, however. This is a significant constraint for a financial institution that deploys a third-party model and can only mediate its inputs and outputs. For such a deployer, model-level defenses are complementary to, not a substitute for, protection placed around the agent.

### 2.5.3 Policy enforcement and tool restriction

A second family enforces explicit constraints on tool use, with deterministic semantics. The approach inherits from the classical security literature on execution monitoring. Schneider (2000) characterized the class of security policies that can be enforced by a monitor observing a system's execution and halting it before a violation. That class consists of safety properties, which a monitor can check using only the execution observed so far. Agent policy enforcers are contemporary instances of this idea, adapted to tools and natural-language tasks.

- **Progent** represents privilege as symbolic rules over tool names and arguments, expressed in a domain-specific language. Policy updates are checked with a satisfiability-modulo-theories solver: narrowings of privilege are applied automatically, while expansions require explicit approval. This yields monotonic confinement. Its authors reported reducing attack success from 39.9% to 1.0% on AgentDojo and from 70.3% to 3.9% on ASB while maintaining functionality (Shi et al., 2025).
- **AgentSpec** provides a lightweight language of triggers, predicates and enforcement actions. Its authors reported preventing unsafe executions in over 90% of code-agent cases, eliminating all hazardous actions in their embodied-agent tasks, and enforcing full compliance for autonomous vehicles, with overheads in milliseconds (H. Wang et al., 2026).
- **Conseca** argues that policies should be generated just in time for the specific task context and then enforced deterministically (Tsai & Bagdasarian, 2025).
- **CaMeL** goes further and restructures the agent itself. It extracts control and data flow from the trusted user query, so that untrusted data retrieved during execution cannot alter the program flow, and it enforces capability-based policies at each tool call. Its authors reported that CaMeL solved 77% of AgentDojo tasks with provable security, compared with 84% for the undefended system (Debenedetti et al., 2025, arXiv v2; an earlier version reported 67%).

This family is fast, auditable and, in CaMeL's case, provably secure for the attacks it addresses. Two recurring limitations matter for REM.

- **The question is binary.** Each enforcer answers whether an action is permitted under a specified policy. None estimates how likely a *permitted* action is to have been induced by an adversary, which is the residual risk that remains once a policy is correctly specified.
- **Integration can be invasive.** CaMeL obtains its guarantee by changing how the agent executes. Progent's authors present their mechanism as integrating without altering agent internals, and AgentSpec integrates as a runtime layer. How invasive the integration is therefore differs substantially across the family.

### 2.5.4 Learned and LLM-based guardrails

A third family uses learned classifiers or LLMs to judge actions or trajectories.

- **GuardAgent** analyzes safety requests, generates a task plan, and maps it into guardrail code that checks whether a target agent's actions satisfy those requests (Xiang et al., 2025).
- **ShieldAgent** extracts verifiable rules from policy documents, structures them into action-based probabilistic rule circuits, and verifies compliance of the protected agent's action trajectory (Z. Chen, Kang, & Li, 2025).
- **AGrail** generates and optimizes adaptive safety checks and retains them in a lifelong memory across tasks (Luo et al., 2025).
- **TrustAgent** applies an agent "constitution" with safety strategies before, during and after planning (Hua et al., 2024).
- **Thought-Aligner** corrects unsafe intermediate thoughts before they become actions. Its authors reported raising behavioral safety from about 50% to about 90% on average across benchmarks and six LLMs, with low per-step latency (Jiang et al., 2025, accepted to ICML 2026).
- **LlamaFirewall** combines its input classifier with *AlignmentCheck*, a chain-of-thought auditor that compares an agent's proposed actions with the user's objective to detect goal hijacking, and with *CodeShield*, a static analyzer for generated code (Chennabasappa et al., 2025).

Compared with deterministic enforcers, these systems cover a broader range of semantic violations without a hand-written policy for each case. Their shared limitations are also recurring. LLM-based judgment adds latency and can vary between runs. Reported accuracies are measured against known attack distributions, and the adaptive-attack evidence (Zhan et al., 2025) warns against reading them as robustness guarantees. Most importantly for REM, their outputs are verdicts or classifications. The reviewed papers do not report calibrated probabilities that could be combined with the consequence of an action in a cost-based decision.

### 2.5.5 Goal–action consistency and provenance

A fourth family, the most directly relevant to indirect injection, asks whether a proposed action is *justified* by the user's task rather than whether it is harmful in itself.

- **Task Shield** verifies whether each instruction and tool call contributes to user-specified goals. On AgentDojo it reduced attack success to 2.07% while maintaining 69.79% task utility with GPT-4o (F. Jia et al., 2025).
- **MELON** re-executes the agent's trajectory with the user's prompt masked and compares the resulting actions with the original ones. The rationale is that, under a successful injection, the next action depends more on the injected task than on the user's task (Zhu et al., 2025).
- **ProvenanceGuard** formalizes misalignment detection as whether a proposed tool call is supported by traceable evidence in the agent's context. Relative to an LLM-as-judge baseline, it reduced the average error rate on misaligned traces from 44.3% to 2.1% on Agent-SafetyBench and from 32.4% to 18.7% on WorkBench. This came at a modest cost: the intervention rate on aligned traces was 14.5%, compared with 10.9% for the baseline (She et al., 2026).

These approaches share an insight: under indirect injection, the useful evidence concerns the *relation* between an action and its sources, not the action alone. They also differ in cost. MELON requires an additional execution. Task Shield and ProvenanceGuard require LLM reasoning over the context. ProvenanceGuard's own results show a small trade-off between detecting misaligned actions and intervening unnecessarily on aligned ones.

**Synthesis.** Organized by intervention point, the defense literature shows a clear progression.

- Input-level detection is cheap but cannot see the observation channel.
- Model-level protection addresses the root cause but requires model access.
- Policy enforcement is deterministic but binary and dependent on the policy.
- Learned guardrails are broad but produce uncalibrated verdicts.
- Provenance and goal-consistency methods target the relational character of injected actions, which is the property that matters most for indirect injection.

Organized by what they observe, most defenses evaluate either an isolated request or an individual action. Fewer reason over the trajectory, and fewer still combine an estimate of adversarial induction with the *consequence* of the action. These last two dimensions are examined in Sections 2.6 and 2.8.

---

## 2.6 Runtime Monitoring and Behavioral Analysis

This section concerns the evidence a runtime layer can extract from the agent's behavior, as distinct from the text it receives. That evidence is the domain of REM's Behavioral Analysis Layer. Three questions structure the section: at what granularity behavior is monitored; what the established anomaly-detection literature contributes; and what is currently known about the empirical value of trajectory-level evidence.

### 2.6.1 Step-level and sequence-level monitoring

Runtime monitors differ in the temporal scope of their judgment.

- **Step-level monitors** evaluate each proposed action given the current context. Examples are AgentSpec's rules, Progent's policies, Task Shield's alignment check and ProvenanceGuard's evidence check. They are interpretable and fast, and they intervene at the action boundary.
- **Sequence-level monitors** evaluate the action in the light of a model of the trajectory. MI9 enforces temporal behavioral patterns through finite-state-machine conformance engines and detects goal-conditioned deviations (C. L. Wang et al., 2025). ProbGuard abstracts agent executions into symbolic states, learns a discrete-time Markov chain from execution traces, and intervenes when the estimated probability of remaining safe falls below a user-defined threshold. Its authors reported PAC-style guarantees on the learned model under standard assumptions (H. Wang et al., 2025). DreamGuard maintains a recurrent latent state over the interaction history, predicts the successor state for each proposed action, and fuses an immediate-hazard score and a prefix-risk score into PASS, HOLD or BLOCK decisions, at an average of about 25 ms per call (Lin et al., 2026).
- **Accumulating monitors** sit between the two. PRISM accumulates risk over a conversation or session with time-to-live decay (F. Li, 2026). AgentTrust's session tracker applies seven order-aware detectors for multi-step attack chains (C. Yang, 2026).

The distinction is not merely technical. A step-level monitor cannot, by construction, detect an attack whose individual steps are each acceptable. A sequence-level monitor can, but it requires either a model of normal trajectories, learned from traces as in ProbGuard and DreamGuard, or a specification of acceptable ones, as in MI9's conformance engines. Such a model must itself be trustworthy and representative.

### 2.6.2 Provenance and goal–action consistency as behavioral evidence

A second line of evidence concerns where an action's content comes from rather than how it fits a sequence. ProvenanceGuard's formulation (She et al., 2026) is especially relevant to financial agents. In an indirect injection against a banking agent, the attacker typically supplies the decisive argument values, such as a recipient account identifier, an amount or a new payee, inside untrusted content. Whether an argument can be traced to the user's request or to trusted state, rather than to a tool output under attacker influence, is therefore strong evidence about adversarial induction. Task Shield (F. Jia et al., 2025) and MELON (Zhu et al., 2025) approach the same question from the side of the task: does the action serve the user's goal, and would it be proposed without the user's instruction? LlamaFirewall's AlignmentCheck (Chennabasappa et al., 2025) and FinHarness's tool monitor (H. Jia et al., 2026) perform related goal–action checks with LLM judges.

Collectively, these studies suggest that provenance and goal consistency are among the most informative behavioral signals available at the action boundary under indirect injection. They also show that the signals can be computed in different ways, by LLM reasoning, by re-execution, or by evidence tracing, with different costs.

### 2.6.3 Foundations: anomaly detection over behavior and sequences

The idea of detecting compromise from behavior predates LLM agents by decades. Forrest et al. (1996) proposed a "sense of self" for Unix processes. They built a profile of normal behavior from short sequences of system calls and flagged sequences absent from the profile as potential intrusions. This original formulation of behavioral anomaly detection over action sequences is the closest classical analogue to monitoring an agent's tool-call sequence.

Chandola et al. (2009) systematized anomaly detection and distinguished three kinds of anomaly:

- *point* anomalies, where a single instance deviates;
- *contextual* anomalies, where an instance is anomalous only in a given context;
- *collective* anomalies, where a set of related instances is anomalous although no individual instance is.

Their later survey of anomaly detection for discrete sequences distinguishes further problem formulations: detecting anomalous whole sequences, anomalous subsequences within a long sequence, and sequences whose pattern frequency is anomalous (Chandola et al., 2012). In this vocabulary:

- a single out-of-policy tool call is a point anomaly;
- a transfer that is normal in general but anomalous given its provenance is a contextual anomaly;
- goal drift and multi-step injection chains are collective anomalies.

The classification clarifies why step-level monitors address the first two classes but not the third.

The same literature carries cautions that transfer directly. Sommer and Paxson (2010) argued that anomaly detection in operational security settings differs fundamentally from other machine-learning applications. The cost of errors is high, attack instances are rare relative to benign activity, normal behavior is diverse, and a gap separates a statistical deviation from an actionable security judgment. Arp et al. (2022) later documented how neglect of the base rate, together with lab-only evaluation and inappropriate baselines, leads to over-optimistic results. For an agent-monitoring layer, these cautions have three concrete implications:

- a representative *benign* workload is needed to estimate false interventions;
- deviations must be interpreted in terms of their security meaning, not only their statistical rarity;
- models of "normal" agent behavior must be learned from data that resemble deployment.

### 2.6.4 Sequential accumulation of behavioral evidence

A distinct methodological question is how evidence observed at successive steps should be *accumulated*. Several agent systems accumulate evidence heuristically: PRISM through session-scoped risk with time-to-live decay (F. Li, 2026), and FinHarness through a cascade that integrates per-step risk and escalates verification when accumulated risk crosses a threshold (H. Jia et al., 2026). Classical sequential change detection provides a statistically grounded alternative for the same task. Its foundations are reviewed in Section 2.7.4, because they belong to the algorithmic basis of the thesis rather than to the agent-security literature.

### 2.6.5 What is known about the empirical value of trajectory evidence

The evidence that trajectory components improve protection *in practice* is thinner than the number of trajectory-aware systems suggests. AgentTrust's ablation is a direct example. Its author reported that disabling the session tracker left verdict accuracy unchanged on both of the benchmarks used, attributing the remaining gap to four benchmark-compatibility rules (C. Yang, 2026). This suggests that single-action signals dominated the scenarios tested. MI9's evaluation used synthetic scenarios (C. L. Wang et al., 2025). ProbGuard's reported gains were obtained in autonomous-driving and embodied-agent settings rather than in tool-using financial agents (H. Wang et al., 2025). The benchmark audits in Section 2.4 add that the number of genuinely multi-step attack tasks in common benchmarks may be small (M. Q. Li et al., 2026; Y. Wang et al., 2026).

**Synthesis.** Trajectory-aware protection is an active and well-populated area. REM cannot claim trajectory monitoring, session accumulation or provenance analysis as new. Three observations nevertheless emerge.

- **Sequence evidence and provenance evidence are complementary.** The first targets collective anomalies such as drift and multi-step chains. The second targets the contextual anomaly that is characteristic of indirect injection: a well-formed action whose decisive arguments come from untrusted content.
- **The classical anomaly-detection literature imposes discipline.** It requires benign-workload evaluation, attention to base rates, and interpretation of deviations. Several agent studies apply this discipline unevenly.
- **The empirical value of trajectory components is uncertain.** One ablation found no measurable effect. A thesis that includes behavioral analysis must therefore show that its evaluation contains the behavior the analysis is meant to detect, and must report the component's contribution rather than assume it.

---

## 2.7 Statistical and Algorithmic Foundations Relevant to REM

A runtime decision layer that assigns graduated responses must solve three methodological problems. It must turn evidence into an estimate of how likely an action is to be adversarially induced. It must make that estimate interpretable as a probability. And it must turn the probability, together with the consequence of the action, into a decision. A layer that observes several steps must additionally decide how to accumulate evidence over time. This section reviews the established methods for each problem that are used or considered in this thesis. For each method it states the problem addressed, the assumptions, the strengths and the limitations, citing the original sources. The methods are established. None is presented as a contribution of this thesis. Only equations needed to understand a reviewed method are reproduced, with notation kept consistent across the section: *x* denotes a feature vector, *s* a score, *y* ∈ {0, 1} a binary label (1 = adversarially induced), and *p̂* an estimated probability.

### 2.7.1 Logistic regression as a probabilistic risk scorer

Logistic regression models the probability of a binary outcome as a logistic function of a linear combination of explanatory variables. Its original statistical formulation for binary data is due to Cox (1958):

$$\Pr(y = 1 \mid x) = \frac{1}{1 + \exp\!\big(-(\beta_0 + \beta^\top x)\big)} \qquad (2.1)$$

The model's assumptions are that the log-odds are linear in the features and that observations are conditionally independent given the features. Its strengths for runtime security are practical. Evaluation costs one inner product. Coefficients are directly inspectable. Because the model is fitted by maximizing likelihood, its outputs are intended as probabilities rather than arbitrary scores. Its limitations are equally clear. It cannot represent interactions or nonlinear effects unless they are engineered into the features, and a model fitted on one distribution of attacks may be miscalibrated on another. Its use for agent safety is not new. NEXUS combines deterministic rules and argument-level inspection with a logistic-regression risk score over plan features, including an irreversibility indicator (Hossain et al., 2026).

### 2.7.2 Probability calibration

A classifier is *calibrated* when its predicted probabilities agree with observed frequencies: among all cases assigned probability 0.8, about 80% should be positive. Calibration matters whenever a probability is multiplied by a cost, as in the decision rules of Section 2.7.5, because a miscalibrated probability distorts the comparison between actions.

**Post-hoc methods.** Several methods learn a map from a model's score to a calibrated probability on held-out data.

- **Platt scaling.** Platt (1999) fitted a sigmoid to the outputs of a support vector machine:

$$\hat{p} = \Pr(y = 1 \mid s) = \frac{1}{1 + \exp(A s + B)} \qquad (2.2)$$

  Here *A* and *B* are fitted by maximum likelihood on a calibration set. The transformation is monotone, so it preserves the ranking of predictions.
- **Temperature scaling.** Guo et al. (2017) found modern neural networks to be poorly calibrated and described temperature scaling as a single-parameter variant of Platt scaling that is effective on many datasets.
- **Isotonic regression.** Zadrozny and Elkan (2002) introduced isotonic regression for classifier calibration, a nonparametric monotone mapping. Niculescu-Mizil and Caruana (2005) compared Platt scaling with isotonic regression across learning algorithms. The comparison motivates a widely followed rule of thumb: isotonic regression is more flexible but needs more calibration data, whereas the sigmoid is preferable when calibration data are scarce.
- **Beta calibration.** Kull et al. (2017) observed that the logistic family applied to scores in the unit interval does not contain the identity function. Logistic calibration can therefore *uncalibrate* an already calibrated classifier. They proposed beta calibration, a logistic model in the features ln *s* and ln(1 − *s*). When the two shape parameters are equal, it reduces to logistic calibration applied to the log-odds of the score. This observation is relevant whenever the model being calibrated is itself logistic, because its log-odds are its natural score.

**Measuring calibration.** Guo et al. (2017) measure calibration error with the *expected calibration error* (ECE). Predictions are partitioned into *M* equal-width bins *B*<sub>*m*</sub>, and the gap between accuracy and confidence is averaged, weighted by bin size:

$$\mathrm{ECE} = \sum_{m=1}^{M} \frac{|B_m|}{n}\,\big|\operatorname{acc}(B_m) - \operatorname{conf}(B_m)\big| \qquad (2.3)$$

For binary problems, Naeini et al. (2015) define the analogous quantity on the probability of the positive class: the weighted absolute difference between the observed fraction of positives and the mean predicted probability in each bin. ECE depends on the binning and on the number of calibration instances. It is best reported together with reliability diagrams and a proper scoring rule, as NEXUS does (Hossain et al., 2026).

**Use in agent safety.** Calibration of agent-safety scores is established practice. NEXUS calibrates its logistic-regression score with Platt scaling and also evaluates isotonic regression. Its authors report that Platt scaling achieved the lowest ECE among their settings and was less prone to overfitting on the small calibration split, while isotonic regression achieved the lowest Brier score. ECE fell from 0.085 for the raw model to 0.013 after Platt scaling (Hossain et al., 2026). DreamGuard likewise converts its scores into decisions through a calibrated fusion rule (Lin et al., 2026).

### 2.7.3 The limits of calibration for control

Calibration makes a score interpretable as a probability. It does not make the score the right quantity for choosing an intervention. C. Zhang et al. (2026) argued that runtime oversight framed as scalar risk prediction, with intervention once a score crosses a threshold, targets the wrong object for control. The decision-relevant quantity is the *intervention advantage*: the expected utility gain from intervening rather than continuing. Two trajectory prefixes can share the same risk estimate while differing in whether they remain recoverable. The authors measured this "target error" with a counterfactual protocol that executes candidate actions from identical trajectory states. On ALFWorld, Platt scaling reduced the ECE of a confidence score from 0.463 to 0.006, while control regret under threshold routing remained unchanged at 0.318. Across four benchmarks, action-conditioned control produced regime-dependent gains over scalar routing.

This finding constrains any design that uses a calibrated probability. It implies that calibration quality and control quality must be reported separately. It also implies that a scalar probability, however well calibrated, does not by itself represent whether an adversarial trajectory can still be recovered. A decision rule that multiplies the probability by consequence-dependent losses addresses part of this limitation, because different consequences can then receive different responses at the same probability. It does not address recoverability of the trajectory, and it should not be presented as doing so.

### 2.7.4 Sequential change detection

When evidence arrives step by step, a monitor must decide when accumulated evidence justifies an alarm. Sequential analysis provides the classical answer. Page (1954) introduced the cumulative sum (CUSUM) procedure for continuous inspection. In the notation of Basseville and Nikiforov (1993), let *s*<sub>*t*</sub> be the log-likelihood ratio of observation *z*<sub>*t*</sub> under a post-change density *p*<sub>1</sub> relative to a pre-change density *p*<sub>0</sub>. CUSUM maintains the statistic

$$g_t = \max\!\big(0,\; g_{t-1} + s_t\big), \qquad s_t = \ln\frac{p_1(z_t)}{p_0(z_t)}, \qquad g_0 = 0 \qquad (2.4)$$

and raises an alarm at the first *t* for which *g*<sub>*t*</sub> ≥ *h*, for a threshold *h*.

- **Mechanism.** Evidence consistent with the pre-change regime drives the statistic back toward zero. Evidence consistent with the post-change regime accumulates.
- **Tuning.** The threshold trades detection delay against the rate of false alarms.
- **Optimality.** Lorden (1971) showed that CUSUM is asymptotically optimal in a minimax sense: among procedures with a given false-alarm rate, it minimizes the worst-case expected detection delay as the false-alarm constraint becomes strict.
- **Assumptions.** The pre- and post-change distributions are known or estimated, and observations are independent given the regime.
- **Limitations for agents.** Both assumptions are only approximately satisfied by tool-call sequences, and adversaries can pace an attack to stay below a threshold. The procedure detects a *change*, whereas an agent episode may be adversarial from its first injected observation.

CUSUM is relevant to REM as an **established alternative** for accumulating behavioral evidence across steps. It is statistically grounded and has a transparent tuning parameter, whereas heuristic accumulation schemes such as session risk with time-to-live decay (F. Li, 2026) or cascaded escalation (H. Jia et al., 2026) do not. Its role in this thesis is that of a reviewed alternative method. It is not a contribution, and it does not replace the per-step estimator described in Chapter 3.

### 2.7.5 Decision-theoretic selection among responses

Once a probability is available, classical decision theory specifies how to choose among responses whose costs depend on the unknown state. Elkan (2001) stated the principle for cost-sensitive classification: an example should be assigned the prediction with the lowest expected cost, computed from the conditional probability of each class and a cost matrix whose entries give the cost of each prediction for each true class. For a set of actions *a* and a binary state *y*:

$$a^{*}(x) = \arg\min_{a} \sum_{y \in \{0,1\}} \Pr(y \mid x)\, C(a, y) \qquad (2.5)$$

Elkan also discussed when a cost matrix is "reasonable". This characterization matters because an incoherent cost matrix can make some responses never optimal. Chow (1970) analyzed the trade-off between recognition error and *rejection*. His analysis shows that withholding an automatic decision is optimal when the expected cost of deciding exceeds the cost of rejecting. This is the classical basis for routing uncertain cases to a human reviewer.

The decision rule in Equation 2.5 is only as good as its two inputs. It requires the probability to be calibrated (Section 2.7.2). It requires the cost matrix to reflect real preferences, which in security settings are rarely known precisely. These two dependencies explain why the reviewed agent systems use cost-based decisions cautiously. NEXUS defines an expected-loss objective with fixed costs for allow, revise, confirm and block. Its deployed policy, however, is described as a rule cascade in which the calibrated score adjudicates particular cases, rather than a per-decision minimization of Equation 2.5 (Hossain et al., 2026; see Section 2.8.4). The analysis of C. Zhang et al. (2026) adds that a cost-weighted probability still omits recoverability.

### 2.7.6 Additive attribution for audit records

Additive feature attribution explains a prediction as a sum of per-feature contributions. Lundberg and Lee (2017) unified such methods under Shapley values. They showed that for a linear model *f*(*x*) = *β*<sub>0</sub> + Σ<sub>*j*</sub> *β*<sub>*j*</sub>*x*<sub>*j*</sub>, under an assumption of feature independence, the attribution of feature *j* is

$$\phi_j = \beta_j\,\big(x_j - \mathbb{E}[x_j]\big) \qquad (2.6)$$

For a logistic model, applied to the log-odds, this decomposition is exact and costs no more than computing the score. It is therefore well suited to a runtime audit record that shows which evidence contributed to a decision. It is nevertheless an established technique, and several agent systems already provide auditable decision traces in other forms: the rule, finding or threshold behind a NEXUS decision (Hossain et al., 2026); the rules that fired in AgentTrust (C. Yang, 2026); verifiable rule circuits in ShieldAgent (Z. Chen, Kang, & Li, 2025); traceable evidence in ProvenanceGuard (She et al., 2026); and PRISM's tamper-evident audit plane (F. Li, 2026). An additive attribution adds a numerical decomposition of a learned score. It does not constitute a distinguishing explanation mechanism.

**Table 2.4. Established methods reviewed as the algorithmic basis for REM**

| Problem | Method (original source) | Assumptions | Strengths | Limitations | Use in agent-security literature |
|---|---|---|---|---|---|
| Probabilistic risk scoring | Logistic regression (Cox, 1958) | Linear log-odds; conditional independence | Fast; inspectable; probabilistic output | No interactions unless engineered; distribution shift | NEXUS risk score (Hossain et al., 2026) |
| Calibration (parametric) | Platt scaling (Platt, 1999); temperature scaling (Guo et al., 2017) | Sigmoid-shaped miscalibration | Few parameters; robust with little data; preserves ranking | Cannot represent the identity on [0, 1] scores (Kull et al., 2017) | NEXUS (Platt); C. Zhang et al. (2026) |
| Calibration (flexible) | Isotonic regression (Zadrozny & Elkan, 2002); beta calibration (Kull et al., 2017) | Monotone map (isotonic); beta-distributed scores (beta) | More flexible; beta contains the identity | Isotonic needs more data (Niculescu-Mizil & Caruana, 2005) | NEXUS evaluated isotonic |
| Calibration measurement | ECE (Guo et al., 2017; Naeini et al., 2015) | Binning scheme | Simple, interpretable | Bin-dependent; unstable with small sets | NEXUS; C. Zhang et al. (2026) |
| Sequential evidence accumulation | CUSUM (Page, 1954; Basseville & Nikiforov, 1993); optimality (Lorden, 1971) | Known or estimated pre/post-change distributions; independence | Statistically grounded; minimax-optimal delay; one threshold | Detects change, not adversarial-from-start; can be evaded by pacing | Heuristic analogues: PRISM decay; FinHarness cascade |
| Response selection | Minimum expected cost (Elkan, 2001); reject option (Chow, 1970) | Calibrated probabilities; coherent costs | Principled use of consequences; explicit human-review region | Costs uncertain; ignores recoverability (C. Zhang et al., 2026) | NEXUS objective (deployed as cascade) |
| Audit decomposition | Additive attribution / Linear SHAP (Lundberg & Lee, 2017) | Linear model; feature independence | Exact for linear scores; negligible cost | Not a novel explanation mechanism | Audit traces in NEXUS, AgentTrust, ShieldAgent, PRISM |

**Synthesis.** Each methodological building block of a probabilistic runtime decision layer is established, well understood, and already applied in agent security. The literature also specifies the conditions each block needs.

- A logistic score needs representative training data.
- Calibration needs held-out data, with the choice of method governed by the amount of data available.
- A cost-based decision needs both calibrated probabilities and coherent costs.
- Sequential accumulation needs a defensible model of normal and abnormal regimes.
- Calibration alone does not improve control.

What the literature leaves open is not whether these methods work in general but how they perform in *combination*, at the action boundary of an executing agent, under indirect injection, when losses depend on the consequence of a financial action. That question is taken up in Section 2.12.

---

## 2.8 Runtime Security and Mitigation

This section examines how runtime systems *act* on what they detect. Four functions are distinguished that the literature often conflates: **detection** (recognizing that something may be wrong), **risk estimation** (quantifying how likely or how severe), **decision** (selecting a response), and **mitigation** (executing it). The section also records where each system intervenes, and whether its decision is made per step or per episode where the source reports this.

### 2.8.1 The space of runtime responses

The reviewed systems use a common, graduated vocabulary of responses. Its elements are to allow the action; to block it; to *modify* it (rewrite arguments, sanitize context, propose a safer alternative, request revision of a plan); to *escalate* it (request confirmation or human review); to *restrict* the agent's tools or privileges; to *interrupt or terminate* the episode; and to *stage or roll back* effects. Table 2.5 records which responses each system reports.

**Table 2.5. Runtime responses reported by reviewed systems**

| System | Allow | Block | Modify / sanitize / revise | Escalate / human review | Restrict tools or privileges | Interrupt / terminate | Stage / roll back | Decision granularity |
|---|---|---|---|---|---|---|---|---|
| Progent (Shi et al., 2025) | Yes | Yes | NOT REPORTED | Yes (approval for privilege expansion) | Yes | NOT REPORTED | NOT REPORTED | Per tool call |
| AgentSpec (H. Wang et al., 2026) | Yes | Yes | Rule-defined enforcement actions | NOT VERIFIED | NOT REPORTED | NOT VERIFIED | NOT REPORTED | Per triggered event |
| MI9 (C. L. Wang et al., 2025) | Yes | Yes | NOT VERIFIED | NOT VERIFIED | Yes (graduated containment) | Yes (graduated containment) | NOT REPORTED | Continuous, agent-level governance |
| PRISM (F. Li, 2026) | Yes | Yes | NOT VERIFIED | NOT VERIFIED | Yes (policy controls over tools, paths, networks) | NOT VERIFIED | NOT REPORTED | Per hook, with session accumulation |
| SafeAgent (H. Liu et al., 2026) | Yes | Yes | Yes (sanitization, replanning, argument rewriting)ᵃ | Yes (human approval)ᵃ | NOT VERIFIED | Yes (session termination)ᵃ | Yes (rollback)ᵃ | Per step over session state |
| AgentTrust (C. Yang, 2026) | Yes | Yes | Yes (SafeFix safer alternatives) | Yes (warn; review) | NOT REPORTED | NOT REPORTED | NOT REPORTED | Per tool call, with session chain detection |
| NEXUS (Hossain et al., 2026) | Yes | Yes | Yes (request revision) | Yes (request confirmation) | NOT REPORTED | NOT REPORTED | NOT REPORTED | Per plan, before execution |
| DreamGuard (Lin et al., 2026) | Yes (PASS) | Yes (BLOCK) | NOT REPORTED | HOLD (semantics NOT VERIFIED) | NOT REPORTED | NOT REPORTED | NOT REPORTED | Per action, with trajectory state |
| FinHarness (H. Jia et al., 2026) | Yes (approval) | Yes | NOT REPORTED | Escalation to an advanced LLM judge (not to a human) | NOT REPORTED | NOT REPORTED | NOT REPORTED | Per step, with cross-turn tracking |
| Jackson (2025) | Yes | Yes (deny) | Yes (sanitize) | Yes (escalate) | NOT VERIFIED | NOT VERIFIED | NOT VERIFIED | NOT VERIFIED (full text not accessed) |
| Cordon (Z. Chen et al., 2026) | NOT APPLICABLE (substrate) | NOT APPLICABLE | NOT APPLICABLE | NOT VERIFIED | NOT APPLICABLE | NOT APPLICABLE | Yes (shadow state; effect outbox) | Per task-level transaction |

ᵃ As described in the September 2026 draft of this chapter; the action list was not re-confirmed against the primary source in the final verification pass (PARTIALLY VERIFIED).

### 2.8.2 Integrated runtime layers

Several systems place a dedicated layer around the agent that combines detection, risk estimation, decision and mitigation.

- **PRISM** instruments ten lifecycle hooks, spanning message ingress, prompt construction, tool execution, tool-result persistence, outbound messaging, sub-agent spawning and gateway startup. It combines heuristic and LLM scanning with conversation- and session-scoped risk accumulation that decays over time, policy controls, and a tamper-evident audit plane (F. Li, 2026). It is tied to one agent-gateway ecosystem.
- **MI9** is a runtime *governance* framework with six components: an agency-risk index, agent-semantic telemetry, continuous authorization monitoring, finite-state-machine conformance engines, goal-conditioned drift detection, and graduated containment. It was evaluated on synthetic multi-domain scenarios (C. L. Wang et al., 2025). Its agency-risk index calibrates governance intensity across *agent populations* rather than scoring individual actions, and its orientation is governance rather than adversarial robustness.
- **SafeAgent** treats agent safety as a stateful decision problem over evolving trajectories. A runtime controller mediates actions around the agent loop, and a context-aware decision core operates over persistent session state through operators for risk encoding, utility–cost evaluation, consequence modeling, policy arbitration and state synchronization. It was evaluated on ASB and InjecAgent (H. Liu et al., 2026). Its consequence reasoning and arbitration are realized through LLM reasoning rather than through an explicit probabilistic model. According to the earlier draft of this chapter, its authors do not address probability calibration and do not report latency (PARTIALLY VERIFIED).

These systems establish that integrated runtime mediation, graduated mitigation and stateful reasoning are already present in the literature.

### 2.8.3 AgentTrust: runtime interception with graduated verdicts

AgentTrust (C. Yang, 2026) is among the closest prior art to REM and is described in detail. It is a runtime safety layer that intercepts agent tool calls *before execution* and returns one of four verdicts: **allow, warn, block or review**. Its components are:

- a normalizer that deobfuscates shell input through nine syntactic strategies;
- an action analyzer that extracts risk-relevant features with 42 regular-expression patterns;
- a policy engine with 170 configurable rules;
- a reporter that produces human-readable explanations;
- a *SafeFix* engine with 37 rules that propose safer alternatives to dangerous actions;
- a session tracker (*RiskChain*) with seven order-aware detectors for multi-step attack chains;
- a cache-aware LLM judge for ambiguous inputs, which assesses actions along dimensions that include reversibility.

The system is exposed as a Model Context Protocol server. On its 300-scenario internal benchmark, a production-only rule set achieved 95.0% verdict accuracy and 73.7% risk-level accuracy at low-millisecond end-to-end latency. On an additional 630 externally constructed adversarial scenarios, the author reported 96.7% verdict accuracy under a *patched* rule set, explicitly not claimed as zero-shot. As noted in Section 2.6.5, disabling the session tracker left verdict accuracy unchanged on both benchmarks.

Measured against REM's design, AgentTrust already provides:

- pre-execution interception of each tool call;
- a four-way graduated verdict set that includes human review;
- a mechanism for proposing safer alternatives, which is comparable to a "modify" response;
- session-level multi-step detection;
- component ablations reporting accuracy, error rates and latency.

These capabilities cannot be claimed as new by REM. The dimensions on which a defensible distinction can be drawn are narrower, and they are stated as differences rather than improvements:

- **Evidence-to-verdict mechanism.** In AgentTrust, risk is aggregated from rule and analyzer signals. The earlier audit of this chapter recorded that aggregation takes the maximum severity over fired signals and that confidence follows a step function of evidence strength. Those two details were not re-confirmed in the final pass (PARTIALLY VERIFIED). No calibrated probability of adversarial induction is reported.
- **Use of consequence.** Reversibility enters AgentTrust as a dimension of the LLM judge's assessment and of its labeling. It is not reported as an explicit loss that varies the decision at a fixed probability.
- **Threat and domain.** AgentTrust targets side effects of coding and shell-oriented agents (file operations, shell commands, HTTP requests, credential exposure). It does not report evaluation on indirect injection against a financial tool-using agent.

### 2.8.4 NEXUS: calibrated risk scoring with a four-way intervention set

NEXUS (Hossain et al., 2026) is the closest prior art to REM's *decision* component. It is a structured-plan safety monitor that evaluates the plan an agent proposes *before execution* and selects among four interventions: **allow, block, request confirmation, or request revision**. It combines deterministic safety rules, argument-level inspection, and a logistic-regression risk score used for graded escalation. The score is calibrated with Platt scaling, and isotonic regression is also evaluated (Section 2.7.2). The authors report the following on a 128-instance held-out synthetic benchmark:

- an F1 score of 0.949 and a four-class intervention accuracy of 0.6406, outperforming rule-only intervention selection by 27.3 percentage points;
- 92% of GPT-4o's binary F1 and 78% of its intervention accuracy, while running about 4,800 times faster;
- a median decision latency of 0.205 ms.

Three features of NEXUS must be represented precisely.

- **Objective versus deployed policy.** The paper defines an expected-loss objective with fixed costs for each intervention. According to the earlier audit of this chapter, however, the *deployed* policy is a rule cascade in which the calibrated score gates particular cases, not a minimization of expected loss at every decision. That audit also recorded the authors' caution that results on their author-generated templates should be read as upper bounds rather than as deployment estimates. Both points are retained from the earlier audit but were not re-confirmed against the full text in the final pass (PARTIALLY VERIFIED).
- **Consequence features.** The risk features include an irreversibility indicator and estimated cost. Consequence therefore enters the *probability model* as features, as well as the costs of the objective.
- **Plan level.** NEXUS evaluates a proposed plan, not each tool call as it is released during an executing trajectory. Its evaluation is on synthetic instances, not on an executable benchmark under indirect injection.

Measured against REM's design, NEXUS already provides calibrated logistic risk scoring, a four-way intervention set that includes a human-confirmation route and a revision route, consequence-related features, an expected-loss formulation, and sub-millisecond latency. REM cannot claim any of these. The defensible differences are:

- the *point of evaluation*: each proposed tool call at the action boundary of an executing agent, rather than a pre-execution plan;
- the *threat model and setting*: indirect prompt injection in an executable banking environment, rather than synthetic plan templates;
- the *decision rule*: per-step minimization of expected loss with losses indexed by declared consequence tiers, rather than a rule cascade gated by the score. Whether this difference produces different behavior is an empirical question, not a presumption.

### 2.8.5 Governance-to-enforcement: Jackson (2025)

A working paper by Jackson (2025) proposes a policy engine for agentic AI that maps governance requirements to runtime enforcement. According to its abstract, it classifies agent behavior into inference, tool usage, data access and external actuation. It computes a multi-dimensional risk score aligned with the NIST AI Risk Management Framework, and it uses a deterministic enforcement state machine that issues **allow, deny, sanitize or escalate** decisions with auditable safety and liveness properties. The paper reports reductions in unsafe actions with minimal latency overhead. It is not peer reviewed, and its full text could not be accessed during the final verification pass. It is nevertheless recorded as prior art, because its decision set corresponds closely to REM's Allow, Block, Modify and Escalate. No claim about its calibration, attribution or ablation is made here, because none could be verified.

### 2.8.6 Consequence-aware control of actions

Two lines of work make the consequence of an action central to the decision. H.-H. Chen (2026) proposes an Actuarial Action Interface: a deterministic runtime contract that prices each side-effect-bearing action, such as a database mutation, refund or payment, against a safe default under a time-consistent risk mapping, and gates execution against a reserve capital budget. An "Authority Frontier" measures how much autonomous authority the runtime releases at each level of reserve capital. This establishes that pricing the consequence of an agent action *before execution* is not new. What the work does not model is an estimated probability that a specific action was induced by an adversary. It prices the consequence of an action irrespective of how the action arose. SafeAgent's consequence-modeling operator (H. Liu et al., 2026) and the irreversibility feature of NEXUS (Hossain et al., 2026) are further instances of consequence-aware control, realized by LLM reasoning and by a risk feature respectively.

### 2.8.7 Transactional mitigation

Mitigation need not be limited to allowing or blocking. Cordon provides a transactional runtime in which tool intents and result lineage are bound to reversible local state. Reversible mutations execute in shadow state, and outward-facing actions are staged in an effect outbox before commitment. Its authors report that it exposes cross-step violations missed by existing defenses and reduces irreversible-effect failures while preserving benign task completion (Z. Chen et al., 2026). Such a substrate *consumes* a decision rather than producing one. It is therefore complementary to a risk-based decision layer, for which it could supply the mechanics of a "hold" or "stage" response.

**Synthesis.** Across the mitigation literature, graduated responses are standard rather than exceptional. Human review appears in several systems (Progent, AgentTrust, NEXUS, SafeAgent, Jackson), action modification appears in several forms, and transactional staging is available. The systems differ mainly in **how evidence becomes a decision**:

- by capability or privilege policy (CaMeL; Progent);
- by rule verdicts with severity aggregation (AgentTrust);
- by thresholds on a predicted probability of reaching unsafe states (ProbGuard);
- by a calibrated fusion of learned scores (DreamGuard);
- by a rule cascade gated by a calibrated score (NEXUS);
- by routing verification between LLM judges (FinHarness);
- by LLM-based arbitration (SafeAgent);
- by deterministic pricing of consequences (H.-H. Chen);
- by action-conditioned estimates of intervention value (C. Zhang et al., 2026).

Two questions remain comparatively open. The first is how an estimated probability of adversarial induction and a declared consequence should be *combined* when choosing among graduated responses at the action boundary. The second is how effective each response actually is once chosen, which is the question C. Zhang et al. (2026) show that risk estimates alone cannot answer.

---

## 2.9 Financial AI-Agent Security

### 2.9.1 Why financial execution raises the stakes

A financial tool-using agent turns a successful manipulation into a financial event. Its tools can initiate transfers, schedule or modify recurring payments, change payees or account settings, and read customer data. A systematization of knowledge on autonomous LLM agents in commerce and finance (Mao et al., 2026, preprint) organizes the resulting threats along five dimensions: agent integrity, transaction authorization, inter-agent trust, market manipulation and regulatory compliance. From a curated corpus of academic papers, protocol documents, industry reports and incident evidence, its authors derive twelve cross-layer attack vectors. They show how failures propagate from the reasoning and tooling layers into custody, settlement, market harm and compliance exposure. Their analysis is a systematization, not an empirical evaluation of a defense. Its relevance here is that it places *transaction authorization*, the question of whether a proposed payment action is sanctioned by its principal, at the center of the financial-agent threat model.

Three properties of financial execution elevate the requirements on a runtime layer; the first two are established in the reviewed sources, and the third is this chapter's inference from them.

- **Irreversibility.** Some financial actions cannot be recalled by the system that issued them. Several reviewed systems encode this property: in consequence pricing (H.-H. Chen, 2026), as an irreversibility feature (Hossain et al., 2026), and as transactional staging (Z. Chen et al., 2026).
- **Attacker-supplied arguments.** Under indirect injection the decisive values, such as a recipient account or an amount, can be planted in the content the agent reads. This makes the provenance of arguments especially informative (Section 2.6.2).
- **Heterogeneous consequences.** Actions of the same *type* can have very different consequences. Reading a balance and transferring funds may both be permitted, but they differ sharply in the harm an induced call could cause. It follows that the same estimated probability of adversarial induction need not warrant the same response for every action.

### 2.9.2 Evidence on financial-agent security

The finance-specific evidence base is small. Z. Chen, J. Chen, et al. (2025, preprint) argue that conventional evaluation of financial LLM agents, based on accuracy and return metrics, gives an illusion of reliability while overlooking vulnerabilities such as hallucinated facts, stale data and adversarial prompt manipulation. They propose a three-level agenda for stress-testing agents at the model, workflow and system levels, illustrated by an audit of six agents on three high-impact tasks. ASB includes a finance scenario among its ten (H. Zhang et al., 2025), and AgentDojo includes a Banking environment (Debenedetti et al., 2024). In both benchmarks, however, finance is one domain within a general evaluation rather than the object of analysis.

FinHarness (H. Jia et al., 2026, preprint) is the closest domain-specific runtime system. It wraps a finance agent end-to-end with three components:

- a *query monitor* that fuses single-turn intent with cross-turn drift;
- a *tool monitor* that evaluates each prospective tool call;
- a *cascade* that integrates per-step risk and routes verification between a lightweight and an advanced LLM judge.

Its authors motivate the design by two observations: boundary filters miss irreversible mid-trajectory tool calls, and post-hoc judges act only after termination. They report that the routed configuration reduced attack success from 38.3% to 15.0% while largely preserving benign approval (41.1% to 39.3%), with 4.7 times fewer calls to the advanced judge. These results were obtained on FinVault (Z. Yang et al., 2026). FinVault was introduced as an execution-grounded financial-agent security benchmark, but its arXiv version has since been **withdrawn** by its authors, who cited legal, intellectual-property and affiliation concerns. FinVault is therefore cited here only as a withdrawn preprint. Its results are not used as evidence in this thesis, and FinHarness's reported figures should be read with that dependency in mind.

### 2.9.3 Regulatory requirements for record-keeping and oversight

Regulation adds requirements that bear directly on runtime design. Regulation (EU) 2024/1689 requires that high-risk AI systems technically allow the automatic recording of events over their lifetime (Article 12). It also requires that such systems can be effectively overseen by natural persons, including the ability to intervene in or interrupt the system through a "stop" button or similar procedure that brings it to a halt in a safe state (Article 14) (European Parliament & Council of the European Union, 2024). Whether a given financial agent falls into a high-risk category depends on its use and is not assessed in this thesis. The provisions are used only as motivation for two design properties: an audit record for every decision, and an explicit route to human review.

### 2.9.4 Requirements for a runtime layer protecting a financial agent

From Sections 2.3 to 2.9, six requirements can be stated for a runtime layer that protects a financial tool-using agent. Each is traceable to the literature above.

- **R1. Pre-execution mediation.** Proposed actions are mediated before they are released to the environment (Sections 2.3, 2.5, 2.8).
- **R2. Provenance evidence.** The decision uses evidence about whether an action's arguments originate in untrusted content (Sections 2.3.2, 2.6.2).
- **R3. Consequence-differentiated responses.** Actions with different consequences can receive different responses at the same estimated probability (Sections 2.7.5, 2.8.6, 2.9.1).
- **R4. Human review.** Human review is available as a response (Sections 2.7.5, 2.8, 2.9.3).
- **R5. Audit record.** Every decision produces a record of the evidence and quantities behind it (Sections 2.7.6, 2.9.3).
- **R6. Joint measurement of security and utility.** Security is measured together with benign task utility, latency and calibration, so that a defense cannot appear effective merely by blocking legitimate work (Sections 2.4, 2.6.3, 2.7.3).

**Synthesis.** Financial-agent runtime safety is not an unaddressed domain. FinHarness addresses it directly, consequence pricing has been proposed by H.-H. Chen (2026), and the commerce SoK systematizes the threat landscape. The verified evidence base is nevertheless small, preprint-dominated, and in one important case withdrawn. General-purpose benchmarks contain financial environments but are rarely analyzed at the level of financial actions and their consequences. This makes careful evaluation on an open, executable banking benchmark valuable in itself.

---

## 2.10 Comparative Analysis of Existing Approaches

Two tables compare the reviewed approaches. Table 2.6 records *what* each approach observes and does, using the columns required by the research problem. Table 2.7 records *how* each approach turns evidence into a decision. The entries follow the primary sources consulted for this review, with these conventions:

- **Yes (…)** means the capability is reported, with a brief note.
- **NOT REPORTED** means the consulted source does not report the capability. This is not a claim that the system lacks it.
- **NOT APPLICABLE** means the capability falls outside the kind of artefact (for example, a benchmark or an analysis paper).
- **NOT VERIFIED** means the capability was described in an earlier draft or a secondary source but could not be confirmed against the primary source in the final verification pass.
- "Partial" is used only when the source describes a limited form of the capability, and the note says which.

**Table 2.6. Capability comparison of reviewed approaches**

| Study / system | Threat focus | Input / context monitoring | Behavioral monitoring | Tool / action monitoring | Runtime intervention | Multi-step awareness | Mitigation | Financial context | Main limitation (relative to the REM research problem) |
|---|---|---|---|---|---|---|---|---|---|
| CaMeL (Debenedetti et al., 2025) | Prompt injection; data exfiltration | Yes (untrusted data isolated; control/data flow from trusted query) | NOT REPORTED | Yes (capability policies at tool calls) | Yes (custom interpreter) | Partial (data-flow tracking through the program) | Policy-violating calls prevented | NOT REPORTED (AgentDojo includes Banking; no finance-specific analysis) | Requires restructuring agent execution; utility 77% vs 84% undefended |
| Progent (Shi et al., 2025) | Indirect injection; tool misuse | NOT APPLICABLE (operates on tool calls) | NOT REPORTED | Yes (privilege rules over tool names and arguments) | Yes | Partial (policy updated during execution) | Block; approval required for privilege expansion | NOT REPORTED | Binary permission; depends on policy quality |
| AgentSpec (H. Wang et al., 2026) | Unsafe actions (code, embodied, AV) | NOT REPORTED | NOT REPORTED | Yes (trigger–predicate–enforcement rules) | Yes (ms overhead) | NOT VERIFIED | Rule-defined enforcement | NOT REPORTED | Requires specified rules; answers permission, not likelihood |
| LlamaFirewall (Chennabasappa et al., 2025) | Injection; jailbreak; goal misalignment; insecure code | Yes (PromptGuard 2) | Yes (AlignmentCheck audits reasoning and actions against objective) | Partial (AlignmentCheck; CodeShield for code) | Yes | Partial (reasoning audit over execution) | NOT VERIFIED | NOT REPORTED | Verdict outputs; calibration and consequence use NOT REPORTED |
| GuardAgent (Xiang et al., 2025) | Violations of safety guard requests | NOT REPORTED | NOT REPORTED | Yes (generated guardrail code checks actions) | Yes | NOT REPORTED | Denies non-compliant actions | NOT REPORTED | Depends on specified requests; calibration NOT REPORTED |
| ShieldAgent (Z. Chen, Kang, & Li, 2025) | Policy violations over trajectories | NOT REPORTED | Partial (trajectory compliance) | Yes (probabilistic rule circuits) | Yes | Yes (action trajectory) | Shielding of non-compliant actions | NOT REPORTED | Policy-compliance focus; requires policy documents |
| Task Shield (F. Jia et al., 2025) | Indirect injection | Yes (instructions checked against user goals) | Yes (goal–action consistency) | Yes | Yes (test time) | Partial (each instruction and call vs user goal) | NOT VERIFIED | NOT REPORTED (evaluated on AgentDojo) | LLM-based verification cost |
| MELON (Zhu et al., 2025) | Indirect injection | Partial (masked user prompt) | Yes (masked re-execution comparison) | Yes (tool-call comparison) | Yes | Yes (re-executes trajectory) | NOT VERIFIED | NOT REPORTED | Requires additional execution per step |
| ProvenanceGuard (She et al., 2026) | Misaligned actions | Yes (evidence provenance in context) | Partial (evidence support for actions) | Yes | Yes | NOT REPORTED | Intervention on unsupported calls | NOT REPORTED | Aligned-trace intervention rate 14.5% vs 10.9% baseline |
| Thought-Aligner (Jiang et al., 2025) | Unsafe intermediate reasoning | NOT APPLICABLE | Yes (thought-level) | NOT REPORTED | Yes (before action) | Partial | Thought correction | NOT REPORTED | Requires a trained correction model |
| MI9 (C. L. Wang et al., 2025) | Emergent agent behavior (governance) | Yes (semantic telemetry) | Yes (FSM conformance; goal-conditioned drift) | Yes (continuous authorization) | Yes | Yes | Graduated containment | NOT VERIFIED | Agent-level governance; synthetic evaluation |
| PRISM (F. Li, 2026) | Indirect injection; unsafe tools; credential leakage; tampering | Yes (ingress and prompt-construction hooks) | Partial (session risk accumulation) | Yes | Yes (ten lifecycle hooks) | Yes (session-scoped, TTL decay) | Policy controls; audit | NOT REPORTED | Single gateway ecosystem; heuristic accumulation |
| ProbGuard (H. Wang et al., 2025) | Violations of safety specifications | NOT REPORTED | Yes (DTMC over symbolic states) | Yes | Yes (threshold on probability of remaining safe) | Yes | Intervention when below threshold | NOT REPORTED (AV, embodied) | Requires state abstraction; non-financial evaluation |
| DreamGuard (Lin et al., 2026) | Long-horizon hazardous drift | NOT REPORTED | Yes (recurrent latent trajectory state) | Yes | Yes (~25 ms per call) | Yes | PASS / HOLD / BLOCK | NOT REPORTED | Learned world model; non-financial evaluation |
| SafeAgent (H. Liu et al., 2026) | Prompt injection across multi-step workflows | Yes (persistent session state) | Yes (stateful decision core) | Yes (runtime controller) | Yes | Yes | Graduated (see Table 2.5) | NOT REPORTED | LLM-realized operators; calibration and latency NOT REPORTED (partially verified) |
| AgentTrust (C. Yang, 2026) | Side effects of tool use (shell, files, HTTP, credentials) | Partial (command normalization; action content) | Yes (seven chain detectors) | Yes (pre-execution interception) | Yes (low ms) | Yes (no measurable effect in its ablation) | Allow / warn / block / review; safer alternatives | NOT REPORTED | Rule-based aggregation; calibrated probability NOT REPORTED |
| NEXUS (Hossain et al., 2026) | Unsafe plans of tool-using agents | NOT REPORTED | NOT REPORTED | Yes (argument-level inspection of plans) | Yes (pre-execution, 0.205 ms median) | Plan-level (whole plan evaluated once) | Allow / block / confirm / revise | NOT REPORTED | Plan-level; synthetic 128-instance test set |
| FinHarness (H. Jia et al., 2026) | Prompt-induced unauthorized financial actions | Yes (query monitor: intent, cross-turn drift) | Partial (drift; accumulated per-step risk) | Yes (tool monitor) | Yes (inline) | Yes | Block / approve; escalation to advanced judge | Yes | Evaluated on a withdrawn benchmark; LLM-judge based |
| H.-H. Chen (2026) | Consequence of side-effect-bearing actions | NOT APPLICABLE | NOT REPORTED | Yes (each action priced) | Yes (gate against reserve capital) | NOT REPORTED | Gating | Partial (actuarial framing; payments and refunds as examples) | Prices consequence; no estimate of adversarial induction |
| Cordon (Z. Chen et al., 2026) | Irreversible effects in multi-step workflows | NOT APPLICABLE | NOT REPORTED | Yes (tool intents and result lineage) | Yes (transaction manager) | Yes (task-level transactions) | Staging; rollback; recovery | NOT REPORTED | Consumes rather than produces a risk decision |
| C. Zhang et al. (2026) | Oversight of agent failure | NOT APPLICABLE | NOT APPLICABLE | NOT APPLICABLE | Analysis of intervention policies | Yes (trajectory prefixes) | Action-conditioned control | NOT REPORTED | Analysis and method paper; not a deployed layer |

**Table 2.7. Decision mechanism, calibration, consequence and evaluation**

| Approach | Decision basis | Calibrated probability | Consequence or reversibility used | Human review / graduated response | Benign utility reported | Latency reported | Financial focus |
|---|---|---|---|---|---|---|---|
| CaMeL | Capability and data-flow policy | NOT APPLICABLE | NOT REPORTED | NOT REPORTED | Yes | NOT REPORTED | NOT REPORTED |
| Progent | Privilege policy (SMT-checked updates) | NOT APPLICABLE | NOT REPORTED | Approval for privilege expansion | Yes ("maintaining functionality") | NOT REPORTED | NOT REPORTED |
| AgentSpec | Deterministic rules | NOT APPLICABLE | NOT REPORTED | NOT VERIFIED | NOT VERIFIED | Yes (milliseconds) | NOT REPORTED |
| Task Shield | LLM verification of task alignment | NOT REPORTED | NOT REPORTED | NOT REPORTED | Yes (69.79% utility, GPT-4o) | NOT REPORTED | NOT REPORTED |
| ProvenanceGuard | Evidence support for tool calls | NOT REPORTED | NOT REPORTED | Intervention (rates reported) | Yes (aligned-trace intervention rate) | NOT REPORTED | NOT REPORTED |
| MI9 | Governance components; agency-risk index | NOT REPORTED | NOT REPORTED | Yes (graduated containment) | NOT VERIFIED | NOT VERIFIED | NOT VERIFIED |
| PRISM | Hooks, scanning, accumulated session risk | NOT REPORTED | NOT REPORTED | NOT VERIFIED | NOT VERIFIED | NOT VERIFIED | NOT REPORTED |
| ProbGuard | Probability of remaining safe (learned DTMC) vs threshold | NOT REPORTED (PAC-style bounds on learned model) | NOT REPORTED | NOT REPORTED | Yes (task completion) | NOT VERIFIED | NOT REPORTED |
| DreamGuard | Calibrated fusion of hazard and prefix-risk scores | Partial ("calibrated fusion rule") | NOT REPORTED | HOLD | Yes (safety–utility trade-off) | Yes (~25 ms) | NOT REPORTED |
| SafeAgent | LLM-based operators and policy arbitration | NOT REPORTED | Yes (LLM consequence modeling) | Yes | Yes | NOT REPORTED | NOT REPORTED |
| AgentTrust | Rules and analyzers; LLM judge for ambiguous cases | NOT REPORTED | Partial (reversibility as a judge dimension) | Yes (warn; review) | NOT REPORTED | Yes (low milliseconds) | NOT REPORTED |
| NEXUS | Rules, argument inspection, calibrated logistic score in a cascade | Yes (Platt; isotonic evaluated) | Yes (irreversibility feature; fixed intervention costs) | Yes (confirm; revise) | Yes (paired benign cases) | Yes (0.205 ms median) | NOT REPORTED |
| FinHarness | Monitors and a judge cascade | NOT REPORTED | NOT REPORTED | Escalation to an advanced LLM judge | Yes (benign approval) | NOT REPORTED (judge-call counts reported) | Yes |
| H.-H. Chen (2026) | Deterministic pricing against reserve capital | NOT APPLICABLE | Yes | NOT REPORTED | NOT REPORTED | NOT REPORTED | Partial |
| Jackson (2025) | Multi-dimensional risk score; enforcement state machine | NOT VERIFIED | NOT VERIFIED | Yes (escalate; sanitize) | NOT VERIFIED | Reported qualitatively ("minimal") | NOT REPORTED (enterprise framing) |
| C. Zhang et al. (2026) | Action-conditioned intervention value | Analyzed (calibration does not change regret) | Yes (recoverability) | NOT APPLICABLE | Regret reported | NOT REPORTED | NOT REPORTED |
| **REM (investigated in this thesis; not a result)** | Calibrated per-step probability combined with consequence-tier losses in an expected-loss rule | Designed | Designed (declared consequence tiers) | Designed (Escalate; Modify) | Planned | Planned | Planned (AgentDojo Banking) |

**Reading the tables.** Read row by row, the tables show that every individual property in REM's design already appears somewhere in prior work:

- calibrated logistic risk scoring and a four-way intervention set: NEXUS;
- pre-execution interception with graduated verdicts and human review: AgentTrust;
- consequence-dependent control: H.-H. Chen, NEXUS, SafeAgent and AgentTrust;
- provenance evidence: ProvenanceGuard;
- trajectory-aware monitoring: MI9, PRISM, ProbGuard, DreamGuard, SafeAgent and AgentTrust;
- latency and component ablations: AgentTrust and NEXUS;
- financial runtime safety: FinHarness;
- the limits of calibration for control: C. Zhang et al.

Read column by column, the tables show where the combinations thin out. Only NEXUS reports a calibrated probability *and* consequence information *and* a graduated response, and it does so at the plan level, on synthetic templates, through a rule cascade. Only FinHarness reports financial focus, and it relies on LLM judges and on a withdrawn benchmark. No reviewed approach reports all of the following together: a calibrated probability of adversarial induction per proposed tool call; declared consequence-dependent losses used to select among graduated responses; and evaluation on an executable financial environment with utility and latency reported.

---

## 2.11 Critical Synthesis

This section draws the comparison together rather than restating it.

**What is well addressed.** The literature has substantially solved *where* to intervene. Pre-execution mediation of tool calls is implemented in many forms (Progent, AgentSpec, AgentTrust, PRISM, SafeAgent, NEXUS, FinHarness). Deterministic enforcement is fast and auditable. Graduated responses, including human review, are standard. Threats are well characterized and benchmarked, and indirect injection is recognized across the literature as the decisive threat for tool-using agents. Calibration methods are mature and have been applied to agent-safety scores.

**What remains fragmented.** The pieces of a probabilistic, consequence-aware decision exist, but in different systems. A calibrated risk score sits in a plan-level monitor evaluated on synthetic data (NEXUS). Consequence pricing sits in a deterministic actuarial gate that ignores how an action arose (H.-H. Chen). Consequence reasoning sits in LLM operators without reported calibration (SafeAgent). Provenance evidence sits in a detector that outputs interventions rather than probabilities (ProvenanceGuard). Financial focus sits in a judge cascade (FinHarness). No reviewed study reports their combination at the action boundary of an executing financial agent.

**Where current approaches stop.** Most detectors and guardrails stop at a verdict. They do not produce a probability that could be traded off against the consequence of the action. Most consequence-aware systems stop at the consequence and do not estimate the likelihood of adversarial induction. Most trajectory-aware systems stop at detection and report little about whether their trajectory component changes outcomes; the one available ablation found no effect (C. Yang, 2026). Most evaluations stop at attack success. Benign utility, latency and calibration are reported unevenly, and C. Zhang et al. (2026) show that calibration and control quality must be reported separately.

**Promising combinations.** Three combinations are suggested by the evidence, though none is established by it:

- provenance evidence, the most informative signal against indirect injection, used as input to a *calibrated* probability rather than to a binary verdict;
- that probability combined with *declared* consequence-dependent losses, so that the same probability can yield different responses for a balance query and a transfer;
- statistically grounded accumulation of evidence across steps (Section 2.7.4), as an alternative to heuristic session scores where multi-step behavior is present.

**Recurring limitations.**

- Evaluation is often on synthetic or author-generated data (MI9; NEXUS).
- Reported figures are author-reported and measured against fixed attacks, which adaptive attacks can overturn (Zhan et al., 2025).
- Benchmark results do not transfer across benchmarks (M. Q. Li et al., 2026; Y. Wang et al., 2026).
- The finance-specific evidence depends in part on a withdrawn benchmark.
- Base-rate and benign-workload discipline is applied unevenly (Arp et al., 2022; Sommer & Paxson, 2010).

**Missing evidence.** The reviewed literature provides limited evidence on the following:

- whether a probability-and-loss decision behaves differently from a consequence-independent threshold that uses the *same* estimator, which is the comparison needed to isolate the contribution of consequence tiers;
- how intervention behavior (the rates of Allow, Modify, Escalate and Block) changes with declared losses;
- how provenance-based features perform as inputs to a calibrated estimator for financial actions under indirect injection;
- how such a layer affects benign utility and latency in an executable banking environment.

**Implication for REM.** REM cannot be positioned as introducing interception, graduated verdicts, calibration, consequence awareness, provenance analysis, trajectory monitoring or audit records. It can be positioned as an *integrative and empirical* study of a specific combination of these established elements, at a specific point of intervention, under a specific threat, in a specific domain, evaluated in a way that separates the contributions of its parts.

---

## 2.12 Research Gap and REM Positioning

### 2.12.1 Structure of the gap

The gap is derived from the comparison in Sections 2.10 and 2.11. It is stated in four parts, each bounded by the evidence reviewed.

**Gap 1 — Integration of a calibrated probability with declared consequences at the action boundary.** Existing studies provide calibrated logistic risk scoring (NEXUS), consequence pricing (H.-H. Chen), consequence reasoning (SafeAgent) and graduated verdicts with human review (AgentTrust; NEXUS; Jackson). The reviewed literature, however, provides limited evidence on selecting among graduated responses by minimizing expected loss per proposed tool call, using a calibrated probability of adversarial induction together with losses declared per consequence tier. NEXUS, the closest study, defines an expected-loss objective but is described as deploying a rule cascade, at the plan level, on synthetic data.

**Gap 2 — The measured value of behavioral evidence under indirect injection.** Trajectory-aware and provenance-based monitoring are well represented, but evidence on their contribution is thin. One ablation found that a session tracker had no measurable effect (C. Yang, 2026). Several trajectory-aware systems were evaluated in non-financial or synthetic settings (C. L. Wang et al., 2025; H. Wang et al., 2025; Lin et al., 2026). Provenance evidence has been evaluated as a detector (She et al., 2026) rather than as input to a calibrated estimator for financial actions. The reviewed literature therefore provides limited evidence on how much behavioral and provenance evidence contributes to a runtime decision for a financial tool-using agent under indirect injection.

**Gap 3 — Financial execution.** General agent-security research treats finance as one scenario among many (ASB; AgentDojo). The finance-specific runtime evidence consists mainly of one preprint system evaluated on a benchmark that has since been withdrawn (FinHarness; FinVault), together with a position paper and a systematization (Z. Chen, J. Chen, et al., 2025; Mao et al., 2026). The reviewed literature provides limited verified evidence on runtime protection evaluated at the level of individual financial actions and their consequences in an open, executable environment.

**Gap 4 — Evaluation that separates the parts.** Latency, benign utility, intervention behavior and calibration are reported unevenly across the reviewed systems. C. Zhang et al. (2026) show that calibration and control must be measured separately. The benchmark audits show that results must be reported per benchmark and interpreted with caution (M. Q. Li et al., 2026; Y. Wang et al., 2026). Few reviewed studies compare a consequence-aware decision against a consequence-independent baseline that uses the same estimator, which is the comparison required to attribute any difference to the use of consequences.

### 2.12.2 Statement of the research gap

> Among the studies reviewed in this chapter, none reports an empirical evaluation of a non-invasive runtime layer for a financial tool-using agent that combines (i) provenance-based evidence about proposed financial actions, (ii) a calibrated per-step probability that the proposed action is adversarially induced, (iii) a decision that minimizes expected loss over Allow, Modify, Escalate and Block using losses declared per consequence tier, and (iv) deterministic mitigation, with attack success, benign utility, intervention behavior, calibration and latency measured separately and compared against a consequence-independent baseline that uses the same estimator.

This is an **integrative and empirical** gap. It concerns the combination and evaluation of established mechanisms under indirect prompt injection. It does not concern the absence of any of those mechanisms, and it does not concern a new learning algorithm. The statement is bounded by the sources reviewed and by the September 2026 verification pass. Identification of a study that reports this combination and evaluation would require the contribution of this thesis to be revised accordingly.

### 2.12.3 Positioning of REM relative to the closest prior work

REM is positioned as a runtime mediation layer between a financial tool-using agent and its environment, organized in five layers: **Input & Context, Detection, Behavioral Analysis, Decision Engine, and Mitigation**. Its design reuses established mechanisms and attributes each to its source. The literature places the following constraints on how REM is studied and described.

- **Relation to NEXUS.** REM does not claim calibrated logistic risk scoring, a four-way intervention set, consequence-related features or an expected-loss formulation. It differs in the point of evaluation (each proposed tool call at the action boundary of an executing agent), the threat model and setting (indirect injection in an executable banking environment), and the decision rule (per-step minimization of conditional expected loss with tier-indexed losses, rather than a rule cascade). Whether these differences change outcomes is to be tested, not assumed.
- **Relation to AgentTrust.** REM does not claim pre-execution interception, graduated verdicts including human review, safer-alternative suggestions, session-level chain detection, or component ablation with latency. It differs in how evidence becomes a decision (a calibrated probability combined with declared losses, rather than rule-based aggregation) and in its threat model and domain.
- **Relation to Jackson (2025), SafeAgent and H.-H. Chen (2026).** REM does not claim a risk-score-to-graduated-verdict pipeline, consequence-aware control or human escalation as new. Its consequence tiers are declared policy inputs, and its losses are reported across a declared grid rather than as fixed truths.
- **Relation to FinHarness.** REM does not claim to be the first runtime protection for financial agents. It studies a different decision mechanism, based on a calibrated probability and declared losses rather than judge routing, on an open, executable benchmark.
- **Relation to ProvenanceGuard, Task Shield and MELON.** REM does not claim provenance or goal-consistency analysis. It uses action-provenance evidence as input to an estimator in its Behavioral Analysis Layer.
- **Relation to C. Zhang et al. (2026).** REM does not claim that calibration improves control. It reports calibration quality and control outcomes separately. It acknowledges that a scalar probability, even when combined with consequence-dependent losses, does not represent whether an adversarial trajectory remains recoverable.
- **Relation to the sequential-detection literature.** Where evidence is accumulated across steps, CUSUM (Page, 1954) is reviewed as an established alternative method. It is not a contribution, and it does not replace the per-step estimator. The operational semantics of the Modify response and the rule for resolving ties between responses of equal expected loss are specified in Chapter 3.

**Table 2.8. What REM adopts from prior work and what constitutes the thesis contribution**

| Element | Status in the literature | Source(s) | Role in REM |
|---|---|---|---|
| Pre-execution mediation of tool calls | Established | Progent; AgentSpec; AgentTrust; PRISM; SafeAgent | Adopted (not claimed) |
| Provenance / goal-consistency evidence | Established | ProvenanceGuard; Task Shield; MELON | Adopted as estimator input (not claimed) |
| Logistic risk scoring | Established | Cox (1958); NEXUS | Adopted (not claimed) |
| Post-hoc calibration (Platt; beta; isotonic) | Established | Platt (1999); Kull et al. (2017); Zadrozny & Elkan (2002); NEXUS | Adopted (not claimed) |
| Minimum expected-cost decision; reject option | Established | Elkan (2001); Chow (1970); NEXUS objective | Adopted (not claimed) |
| Consequence-dependent control | Established | H.-H. Chen (2026); NEXUS; SafeAgent; AgentTrust | Adopted as declared tiers (not claimed) |
| Graduated responses incl. human review | Established | AgentTrust; NEXUS; SafeAgent; Jackson; MI9 | Adopted (not claimed) |
| Sequential evidence accumulation (CUSUM) | Established | Page (1954); Basseville & Nikiforov (1993); Lorden (1971) | Reviewed alternative method (not claimed) |
| Additive attribution for audit | Established | Lundberg & Lee (2017) | Audit record only; not used for the verdict (not claimed) |
| **Combination of (i)–(iv) in §2.12.2 at the action boundary, under indirect injection, on an open executable banking benchmark** | **Not reported in reviewed corpus** | — | **Thesis contribution (integrative)** |
| **Evaluation separating attack success, benign utility, intervention behavior, calibration and latency, against a consequence-independent baseline with the same estimator** | **Not reported in reviewed corpus** | — | **Thesis contribution (empirical)** |

**Table 2.9. Requirements derived from the literature and their treatment in Chapter 3**

| Requirement | Literature basis | Treatment in Chapter 3 |
|---|---|---|
| R1 Pre-execution mediation | Sections 2.5, 2.8 | REM intercepts each proposed tool call before release (Sections 3.2, 3.10) |
| R2 Provenance evidence for action arguments | Sections 2.3.2, 2.6.2 | Action-provenance features in the Behavioral Analysis Layer (Section 3.6) |
| R3 Consequence-differentiated responses | Sections 2.7.5, 2.8.6, 2.9.1 | Consequence tiers and tier-indexed losses (Section 3.7) |
| R4 Human review | Sections 2.7.5, 2.8, 2.9.3 | Escalate verdict (Sections 3.7, 3.8) |
| R5 Audit record | Sections 2.7.6, 2.9.3 | Audit record with linear attribution, never used for the verdict (Section 3.7.6) |
| R6 Joint security, utility, calibration and latency measurement | Sections 2.4, 2.6.3, 2.7.3 | Primary metrics and baseline comparison (Sections 3.11, 3.12) |

---

## 2.13 Chapter Summary

This chapter reviewed the literature on runtime protection of LLM agents, with a focus on financial tool use.

- **Threats.** Agent architecture creates risk at the interaction between heterogeneous input channels, accumulated state and consequential tools. Indirect prompt injection enters through the observation channel, and its harm materializes at the proposed action, which is the last point at which harm can be prevented.
- **Defenses.** Defenses differ in where they intervene and what they observe. Input and model-level defenses do not see the action boundary. Policy enforcers answer permission rather than likelihood. Guardrails produce uncalibrated verdicts. Provenance and goal-consistency methods target the relational character of injected actions.
- **Behavioral analysis.** Trajectory-aware monitoring is well populated, but evidence on its measured contribution is thin, and the classical anomaly-detection literature imposes cautions on its evaluation.
- **Algorithmic foundations.** The methods underlying a probabilistic decision layer are established: logistic regression, Platt, isotonic and beta calibration, expected-cost decisions with a reject option, CUSUM as an alternative for sequential accumulation, and additive attribution. Calibration has been shown to be necessary for cost-based decisions but not sufficient for good control.
- **Runtime systems.** Interception, graduated verdicts, calibrated scoring, consequence awareness and transactional mitigation all have precedents, most directly in AgentTrust and NEXUS.
- **Financial agents.** Financial-agent security has begun to be addressed, but on a small, preprint-dominated and partly withdrawn evidence base.

The research gap is accordingly integrative and empirical. It concerns the evaluation, on an open, executable banking benchmark, of a runtime layer that combines provenance-based action evidence, a calibrated per-step probability, consequence-tiered expected-loss decisions and deterministic mitigation, measured separately for security, utility, intervention behavior, calibration and latency against a consequence-independent baseline. Chapter 3 specifies the methodology through which this gap is addressed.

---

## References

*Preprints, working papers and withdrawn preprints are marked. Official and regulatory sources are marked [Official source] and are not treated as research literature.*

Andriushchenko, M., Souly, A., Dziemian, M., Duenas, D., Lin, M., Wang, J., Hendrycks, D., Zou, A., Kolter, Z., Fredrikson, M., Winsor, E., Wynne, J., Gal, Y., & Davies, X. (2025). AgentHarm: A benchmark for measuring harmfulness of LLM agents. In *The Thirteenth International Conference on Learning Representations (ICLR 2025)*. https://arxiv.org/abs/2410.09024

Arp, D., Quiring, E., Pendlebury, F., Warnecke, A., Pierazzi, F., Wressnegger, C., Cavallaro, L., & Rieck, K. (2022). Dos and don'ts of machine learning in computer security. In *31st USENIX Security Symposium* (pp. 3971–3988). USENIX Association.

Basseville, M., & Nikiforov, I. V. (1993). *Detection of abrupt changes: Theory and application*. Prentice Hall.

Chandola, V., Banerjee, A., & Kumar, V. (2009). Anomaly detection: A survey. *ACM Computing Surveys, 41*(3), Article 15, 1–58. https://doi.org/10.1145/1541880.1541882

Chandola, V., Banerjee, A., & Kumar, V. (2012). Anomaly detection for discrete sequences: A survey. *IEEE Transactions on Knowledge and Data Engineering, 24*(5), 823–839. https://doi.org/10.1109/TKDE.2010.235

Chen, H.-H. (2026). *Insuring every action: An authority frontier framework for runtime actuarial control of autonomous AI agents* (arXiv:2605.25632) [Preprint]. arXiv. https://arxiv.org/abs/2605.25632

Chen, S., Piet, J., Sitawarin, C., & Wagner, D. (2025). StruQ: Defending against prompt injection with structured queries. In *34th USENIX Security Symposium*. USENIX Association.

Chen, Z., Chen, J., Chen, J., & Sra, M. (2025). *Standard benchmarks fail — Auditing LLM agents in finance must prioritize risk* (arXiv:2502.15865) [Preprint]. arXiv. https://arxiv.org/abs/2502.15865

Chen, Z., Dong, D., Liu, H., Li, J., Zhai, J., Xu, D., & Pu, B. (2026). *Cordon: Semantic transactions for tool-using LLM agents* (arXiv:2606.17573) [Preprint]. arXiv. https://arxiv.org/abs/2606.17573

Chen, Z., Kang, M., & Li, B. (2025). ShieldAgent: Shielding agents via verifiable safety policy reasoning. In *Proceedings of the 42nd International Conference on Machine Learning* (Proceedings of Machine Learning Research, Vol. 267, pp. 8313–8344). PMLR.

Chen, Z., Xiang, Z., Xiao, C., Song, D., & Li, B. (2024). AgentPoison: Red-teaming LLM agents via poisoning memory or knowledge bases. In *Advances in Neural Information Processing Systems 37 (NeurIPS 2024)*.

Chennabasappa, S., Nikolaidis, C., Song, D., Molnar, D., Ding, S., Wan, S., Whitman, S., Deason, L., Doucette, N., Montilla, A., Gampa, A., de Paola, B., Gabi, D., Crnkovich, J., Testud, J.-C., He, K., Chaturvedi, R., Zhou, W., & Saxe, J. (2025). *LlamaFirewall: An open source guardrail system for building secure AI agents* (arXiv:2505.03574) [Preprint]. arXiv. https://arxiv.org/abs/2505.03574

Chow, C. K. (1970). On optimum recognition error and reject tradeoff. *IEEE Transactions on Information Theory, 16*(1), 41–46. https://doi.org/10.1109/TIT.1970.1054406

Cox, D. R. (1958). The regression analysis of binary sequences. *Journal of the Royal Statistical Society: Series B (Methodological), 20*(2), 215–232. https://doi.org/10.1111/j.2517-6161.1958.tb00292.x

Debenedetti, E., Shumailov, I., Fan, T., Hayes, J., Carlini, N., Fabian, D., Kern, C., Shi, C., Terzis, A., & Tramèr, F. (2025). *Defeating prompt injections by design* (arXiv:2503.18813v2) [Preprint]. arXiv. https://arxiv.org/abs/2503.18813

Debenedetti, E., Zhang, J., Balunović, M., Beurer-Kellner, L., Fischer, M., & Tramèr, F. (2024). AgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents. In *Advances in Neural Information Processing Systems 37 (NeurIPS 2024), Datasets and Benchmarks Track*.

Elkan, C. (2001). The foundations of cost-sensitive learning. In *Proceedings of the Seventeenth International Joint Conference on Artificial Intelligence (IJCAI-01)* (pp. 973–978).

European Parliament & Council of the European Union. (2024). *Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act)*. Official Journal of the European Union. https://eur-lex.europa.eu/eli/reg/2024/1689/oj [Official source]

Forrest, S., Hofmeyr, S. A., Somayaji, A., & Longstaff, T. A. (1996). A sense of self for Unix processes. In *Proceedings of the 1996 IEEE Symposium on Security and Privacy* (pp. 120–128). IEEE. https://doi.org/10.1109/SECPRI.1996.502675

Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., & Fritz, M. (2023). Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection. In *Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security* (pp. 79–90). ACM. https://doi.org/10.1145/3605764.3623985

Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. In *Proceedings of the 34th International Conference on Machine Learning* (Proceedings of Machine Learning Research, Vol. 70, pp. 1321–1330). PMLR.

Hines, K., Lopez, G., Hall, M., Zarfati, F., Zunger, Y., & Kiciman, E. (2024). *Defending against indirect prompt injection attacks with spotlighting* (arXiv:2403.14720) [Preprint]. arXiv. https://arxiv.org/abs/2403.14720

Hossain, E., Nipu, M. M. H., Ornee, T. N., Rana, R., & Yousefi, N. (2026). *NEXUS: Structured runtime safety for tool-using LLM agents* (arXiv:2607.19356) [Preprint]. arXiv. https://arxiv.org/abs/2607.19356

Hua, W., Yang, X., Jin, M., Li, Z., Cheng, W., Tang, R., & Zhang, Y. (2024). TrustAgent: Towards safe and trustworthy LLM-based agents. In *Findings of the Association for Computational Linguistics: EMNLP 2024* (pp. 10000–10016). Association for Computational Linguistics. https://doi.org/10.18653/v1/2024.findings-emnlp.585

Inan, H., Upasani, K., Chi, J., Rungta, R., Iyer, K., Mao, Y., Tontchev, M., Hu, Q., Fuller, B., Testuggine, D., & Khabsa, M. (2023). *Llama Guard: LLM-based input-output safeguard for human-AI conversations* (arXiv:2312.06674) [Preprint]. arXiv. https://arxiv.org/abs/2312.06674

Jackson, F. (2025). *Designing a policy engine for agentic AI systems: From governance requirements to runtime enforcement* [Working paper]. SSRN. https://doi.org/10.2139/ssrn.5904104

Jia, F., Wu, T., Qin, X., & Squicciarini, A. (2025). The Task Shield: Enforcing task alignment to defend against indirect prompt injection in LLM agents. In *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*. Association for Computational Linguistics. https://aclanthology.org/2025.acl-long.1435/

Jia, H., Liu, Y., Chong, B., Yang, Y., Chen, Y., Liang, J., Li, Q., Lu, H., Xu, K., Zheng, H., Zhang, C., Peng, H., & Yu, P. S. (2026). *FinHarness: An inline lifecycle safety harness for finance LLM agents* (arXiv:2605.27333) [Preprint]. arXiv. https://arxiv.org/abs/2605.27333

Jiang, C., Zhang, W., Pan, X., Hong, G., & Yang, M. (2025). *Think twice before you act: Enhancing agent behavioral safety with thought correction* (arXiv:2505.11063) [Preprint; accepted to ICML 2026]. arXiv. https://arxiv.org/abs/2505.11063

Kull, M., Silva Filho, T., & Flach, P. (2017). Beta calibration: A well-founded and easily implemented improvement on logistic calibration for binary classifiers. In *Proceedings of the 20th International Conference on Artificial Intelligence and Statistics* (Proceedings of Machine Learning Research, Vol. 54, pp. 623–631). PMLR.

Li, F. (2026). *OpenClaw PRISM: A zero-fork, defense-in-depth runtime security layer for tool-augmented LLM agents* (arXiv:2603.11853) [Preprint]. arXiv. https://arxiv.org/abs/2603.11853

Li, M. Q., Fung, B. C. M., Li, B., Ismail, H., & Iqbal, F. (2026). *Taxonomy and consistency analysis of safety benchmarks for AI agents* (arXiv:2605.16282) [Preprint]. arXiv. https://arxiv.org/abs/2605.16282

Lin, W., Yu, C., Lin, X., Cao, S., Chen, X., Xue, L., Yu, L., Sha, L., & Wu, C. (2026). *DreamGuard: Efficient runtime guardrail for LLM agents via risk-aware world model* (arXiv:2608.05695) [Preprint]. arXiv. https://arxiv.org/abs/2608.05695

Liu, H., Ilyushin, E., Ni, J., & Zhu, M. (2026). *SafeAgent: A runtime protection architecture for agentic systems* (arXiv:2604.17562) [Preprint]. arXiv. https://arxiv.org/abs/2604.17562

Liu, Y., Jia, Y., Geng, R., Jia, J., & Gong, N. Z. (2024). Formalizing and benchmarking prompt injection attacks and defenses. In *33rd USENIX Security Symposium* (pp. 1831–1847). USENIX Association.

Lorden, G. (1971). Procedures for reacting to a change in distribution. *The Annals of Mathematical Statistics, 42*(6), 1897–1908. https://doi.org/10.1214/aoms/1177693055

Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. In *Advances in Neural Information Processing Systems 30 (NIPS 2017)* (pp. 4765–4774).

Luo, W., Dai, S., Liu, X., Banerjee, S., Sun, H., Chen, M., & Xiao, C. (2025). AGrail: A lifelong agent guardrail with effective and adaptive safety detection. In *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)* (pp. 8104–8139). Association for Computational Linguistics. https://doi.org/10.18653/v1/2025.acl-long.399

Mao, Q., Wang, J., Liu, Y., Zhu, L., Ma, C., & Yan, J. (2026). *SoK: Security of autonomous LLM agents in agentic commerce* (arXiv:2604.15367) [Preprint]. arXiv. https://arxiv.org/abs/2604.15367

Naeini, M. P., Cooper, G., & Hauskrecht, M. (2015). Obtaining well calibrated probabilities using Bayesian binning. *Proceedings of the AAAI Conference on Artificial Intelligence, 29*(1). https://doi.org/10.1609/aaai.v29i1.9602

Niculescu-Mizil, A., & Caruana, R. (2005). Predicting good probabilities with supervised learning. In *Proceedings of the 22nd International Conference on Machine Learning* (pp. 625–632). ACM. https://doi.org/10.1145/1102351.1102430

OWASP Gen AI Security Project. (2025). *LLM01:2025 Prompt injection*. OWASP Foundation. https://genai.owasp.org/llmrisk/llm01-prompt-injection/ [Official source]

Page, E. S. (1954). Continuous inspection schemes. *Biometrika, 41*(1–2), 100–115. https://doi.org/10.1093/biomet/41.1-2.100

Perez, F., & Ribeiro, I. (2022). *Ignore previous prompt: Attack techniques for language models* (arXiv:2211.09527). NeurIPS 2022 ML Safety Workshop. https://arxiv.org/abs/2211.09527

Platt, J. C. (1999). Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. In A. J. Smola, P. Bartlett, B. Schölkopf, & D. Schuurmans (Eds.), *Advances in large margin classifiers* (pp. 61–74). MIT Press.

Ruan, Y., Dong, H., Wang, A., Pitis, S., Zhou, Y., Ba, J., Dubois, Y., Maddison, C. J., & Hashimoto, T. (2024). Identifying the risks of LM agents with an LM-emulated sandbox. In *The Twelfth International Conference on Learning Representations (ICLR 2024)*.

Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Hambro, E., Zettlemoyer, L., Cancedda, N., & Scialom, T. (2023). Toolformer: Language models can teach themselves to use tools. In *Advances in Neural Information Processing Systems 36 (NeurIPS 2023)*.

Schneider, F. B. (2000). Enforceable security policies. *ACM Transactions on Information and System Security, 3*(1), 30–50. https://doi.org/10.1145/353323.353382

She, Y., Liang, Y., & Kang, E. (2026). *Safeguarding LLM agents from misalignment through provenance analysis* (arXiv:2607.01236) [Preprint]. arXiv. https://arxiv.org/abs/2607.01236

Shi, T., He, J., Wang, Z., Wu, L., Li, H., Guo, W., & Song, D. (2025). *Progent: Securing AI agents with privilege control* (arXiv:2504.11703) [Preprint]. arXiv. https://arxiv.org/abs/2504.11703

Sommer, R., & Paxson, V. (2010). Outside the closed world: On using machine learning for network intrusion detection. In *2010 IEEE Symposium on Security and Privacy* (pp. 305–316). IEEE. https://doi.org/10.1109/SP.2010.25

Tsai, L., & Bagdasarian, E. (2025). Contextual agent security: A policy for every purpose. In *Proceedings of the Workshop on Hot Topics in Operating Systems (HotOS '25)* (pp. 8–17). ACM. https://doi.org/10.1145/3713082.3730378

Wang, C. L., Singhal, T., Kelkar, A., & Tuo, J. (2025). *MI9: An integrated runtime governance framework for agentic AI* (arXiv:2508.03858) [Preprint]. arXiv. https://arxiv.org/abs/2508.03858

Wang, H., Poskitt, C. M., & Sun, J. (2026). AgentSpec: Customizable runtime enforcement for safe and reliable LLM agents. In *Proceedings of the IEEE/ACM 48th International Conference on Software Engineering (ICSE '26)*. ACM. https://doi.org/10.1145/3744916.3764546

Wang, H., Poskitt, C. M., Wei, J., & Sun, J. (2025). *ProbGuard: Probabilistic runtime monitoring for LLM agent safety* (arXiv:2508.00500; earlier versions titled "Pro2Guard") [Preprint]. arXiv. https://arxiv.org/abs/2508.00500

Wang, L., Ma, C., Feng, X., Zhang, Z., Yang, H., Zhang, J., Chen, Z., Tang, J., Chen, X., Lin, Y., Zhao, W. X., Wei, Z., & Wen, J. (2024). A survey on large language model based autonomous agents. *Frontiers of Computer Science, 18*(6), Article 186345. https://doi.org/10.1007/s11704-024-40231-1

Wang, Y., Han, X., Shang, D., Tang, Y., & Liu, B. (2026). *Safety, or just capability? A validity audit of agent-safety benchmarks* (arXiv:2607.28685) [Preprint]. arXiv. https://arxiv.org/abs/2607.28685

Xiang, Z., Zheng, L., Li, Y., Hong, J., Li, Q., Xie, H., Zhang, J., Xiong, Z., Xie, C., Yang, C., Song, D., & Li, B. (2025). GuardAgent: Safeguard LLM agents via knowledge-enabled reasoning. In *Proceedings of the 42nd International Conference on Machine Learning* (Proceedings of Machine Learning Research, Vol. 267, pp. 68316–68342). PMLR.

Yang, C. (2026). *AgentTrust: Runtime safety evaluation and interception for AI agent tool use* (arXiv:2605.04785) [Preprint]. arXiv. https://arxiv.org/abs/2605.04785

Yang, Z., Li, R., Qiang, Q., Wang, J., Lou, F., Li, M., Cheng, D., Xu, R., Lian, H., Zhang, S., Liang, X., Huang, X., Wei, Z., Liu, Z., Guo, X., Wang, H., Chen, R., & Zhang, L. (2026). *FinVault: Benchmarking financial agent safety in execution-grounded environments* (arXiv:2601.07853) [Withdrawn preprint]. arXiv. https://arxiv.org/abs/2601.07853

Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing reasoning and acting in language models. In *The Eleventh International Conference on Learning Representations (ICLR 2023)*.

Yu, M., Meng, F., Zhou, X., Wang, S., Mao, J., Pan, L., Chen, T., Wang, K., Li, X., Zhang, Y., An, B., & Wen, Q. (2025). A survey on trustworthy LLM agents: Threats and countermeasures. In *Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2* (pp. 6216–6226). ACM. https://doi.org/10.1145/3711896.3736561

Zadrozny, B., & Elkan, C. (2002). Transforming classifier scores into accurate multiclass probability estimates. In *Proceedings of the Eighth ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 694–699). ACM. https://doi.org/10.1145/775047.775151

Zhan, Q., Fang, R., Panchal, H. S., & Kang, D. (2025). Adaptive attacks break defenses against indirect prompt injection attacks on LLM agents. In *Findings of the Association for Computational Linguistics: NAACL 2025* (pp. 7116–7132). Association for Computational Linguistics. https://aclanthology.org/2025.findings-naacl.395/

Zhan, Q., Liang, Z., Ying, Z., & Kang, D. (2024). InjecAgent: Benchmarking indirect prompt injections in tool-integrated large language model agents. In *Findings of the Association for Computational Linguistics: ACL 2024* (pp. 10471–10506). Association for Computational Linguistics. https://doi.org/10.18653/v1/2024.findings-acl.624

Zhang, C., Wan, Z., Yu, X., Wu, J., Wen, Q., Zhou, P., Zhao, W., & Tsang, I. (2026). *Calibration is not control: Why LLM-agent oversight needs intervention* (arXiv:2606.21399) [Preprint]. arXiv. https://arxiv.org/abs/2606.21399

Zhang, H., Huang, J., Mei, K., Yao, Y., Wang, Z., Zhan, C., Wang, H., & Zhang, Y. (2025). Agent Security Bench (ASB): Formalizing and benchmarking attacks and defenses in LLM-based agents. In *The Thirteenth International Conference on Learning Representations (ICLR 2025)*.

Zhu, K., Yang, X., Wang, J., Guo, W., & Wang, W. Y. (2025). MELON: Provable defense against indirect prompt injection attacks in AI agents. In *Proceedings of the 42nd International Conference on Machine Learning* (Proceedings of Machine Learning Research, Vol. 267). PMLR.
