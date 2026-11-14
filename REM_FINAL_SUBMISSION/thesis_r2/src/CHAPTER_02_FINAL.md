# CHAPTER TWO

# LITERATURE REVIEW: A RECORD-LEVEL SYSTEMATIC REVIEW OF RUNTIME SECURITY FOR TOOL-USING AI AGENTS

## 2.1 Introduction

Large language model (LLM) agents no longer only produce text for a human reader. They break tasks into steps, call external tools with arguments they generate themselves, read the results of those calls, and act again on what they read. When such an agent operates on financial tools, a single proposed tool call can:

- initiate a transfer;
- change a payee;
- modify a scheduled payment;
- send customer data to an external recipient.

The security question therefore shifts from what a model *says* to what an agent *does*. More precisely, it shifts to the moment at which a proposed action leaves the agent and takes effect in its environment.

This chapter reviews the literature on protecting such an agent at runtime. Earlier versions of the chapter were structured narrative reviews. This version is a **systematic review conducted at record level, with qualitative, structured evidence synthesis**. The search, screening, eligibility assessment, quality appraisal and data extraction followed a predefined protocol and are reported following PRISMA 2020 and PRISMA-S. Full-text reports could not be retrieved, so eligibility, appraisal and extraction rest on records: titles, abstracts and index metadata. **No full-text screening was performed**, and the chapter does not claim the depth of a full-text systematic review. The methodology in Section 2.2 records what was actually done: which sources were searched and which could not be accessed, the exact search strings, the screening decisions, the quality appraisal and the extraction. Where a step of the systematic-review process could not be carried out in full, the limitation is stated rather than concealed. No meta-analysis is attempted. The included studies differ in architecture, threat model, benchmark, metric and intervention, so their quantitative results cannot be pooled (Section 2.2.5).

The review is used to build an argument in eight steps:

1. agents create security risks that differ from those of conventional LLM use;
2. prior research has characterized the main threats and proposed many defenses;
3. those defenses differ in *where* they intervene;
4. they also differ in *what* they observe;
5. some capabilities are now well addressed;
6. others remain fragmented or weakly evidenced;
7. these patterns locate the Runtime Evaluation and Mitigation (REM) framework studied in this thesis;
8. the financial setting raises the stakes of each of these questions.

The research gap at the end of the chapter was derived only after screening, extraction and synthesis were complete. Section 2.12.1 assesses five candidate gaps against the evidence and retains, narrows or rejects each.

**Chapter structure.** Section 2.2 reports the review methodology. Sections 2.3 and 2.4 cover threats, benchmarks and threat models. Section 2.5 organizes defenses by where they intervene, and Section 2.6 examines runtime monitoring, behavioral evidence and provenance. Section 2.7 reviews the statistical foundations of a runtime decision layer; the REM specification itself is left to Chapter 3. Section 2.8 examines how runtime systems decide and mitigate, and Section 2.9 separates financial-agent evidence from general evidence. Sections 2.10 and 2.11 compare and synthesize the evidence. Section 2.12 states the research gap, positions REM, records the limitations of the review and reports three dated literature updates that lie outside the systematic review. Section 2.13 summarizes the chapter.

## 2.2 Systematic Review Methodology

### 2.2.1 Review objectives and research questions

**Derivation.** The review questions are derived from the approved thesis direction and introduce no new thesis research questions. The approved proposal states three objectives:

- **O1:** design a REM framework for financial AI agents' and task automation agents' security;
- **O2:** evaluate the framework against adversarial attacks;
- **O3:** compare performance with existing security approaches (Chapter 3, Section 3.1.2).

The proposal does not state research questions. Chapter 3 (Section 3.1.3) derives four questions, RQ1–RQ4, from these objectives. They concern estimation, decision, mitigation and cost, and component contribution.

**Review questions.** The review is designed to supply the literature basis that O1–O3 and RQ1–RQ4 require. It asks five review questions (SRQ). These define the scope of this chapter only; they are not thesis research questions.

| Review question | Wording | Serves |
|---|---|---|
| SRQ1 | What security threats affect tool-using AI agents, particularly those operating through external tools and multi-step execution? | O1 (threat model); O2 (attack scenarios) |
| SRQ2 | What defensive approaches have been proposed to detect, monitor, evaluate and mitigate these threats at runtime? | O1 (design space); O3 (comparators) |
| SRQ3 | What behavioral, provenance, probabilistic, sequential and decision-theoretic techniques are used? | O1; RQ1, RQ2 and RQ4 |
| SRQ4 | What evidence exists for these approaches in financial or financially consequential agent settings? | O1 (financial scope); O2 |
| SRQ5 | What limitations and evidence gaps remain that motivate the REM framework? | Research gap (Section 2.12) |

### 2.2.2 Information sources

The review protocol named eleven preferred sources:

- IEEE Xplore;
- ACM Digital Library;
- Scopus or Web of Science;
- ScienceDirect;
- SpringerLink;
- ACL Anthology;
- NeurIPS and PMLR proceedings;
- ICLR proceedings;
- USENIX;
- arXiv, as a supplementary source.

These sources were not directly searchable from the review environment. Direct access was attempted on 25 September 2026, and the network policy refused every connection. The connection log is retained with the search record. An attempt to use Elicit, a second scholarly index, also failed: the account's plan does not include API access. Each of these sources is therefore recorded as **DATABASE ACCESS UNAVAILABLE** (`CHAPTER2_SYSTEMATIC_SEARCH_STRATEGY.md`, §1).

**Source actually searched.** The one bibliographic database searched was **OpenAlex**, through a literature-search tool that queries its index of about 250 million records. OpenAlex indexes the proceedings and journals of the publishers listed above, as well as arXiv. Studies from those venues could therefore be retrieved, but only through OpenAlex's index and relevance ranking, not through each library's own search interface. The review accordingly does **not** claim to have searched the named digital libraries.

**Other methods.** A second, non-database stream was used, as PRISMA 2020 allows. It consists of the 70 sources in the reference list of the previous integrated version of this chapter. That list was assembled by known-item searching of the thesis corpus and backward citation checking, and it was verified between 16 and 25 September 2026. Crossref was used only to verify metadata, never to identify records.

### 2.2.3 Search strategy

**Concept blocks.** The protocol defines three concept blocks and a financial block:

- **A — Agents:** "LLM agent", "AI agent", "language model agent", "tool-using agent", "autonomous agent";
- **B — Security:** "security", "prompt injection", "indirect prompt injection", "tool misuse", "agent safety", "goal hijacking", "memory poisoning", "action manipulation";
- **C — Runtime, behavior and mitigation:** "runtime monitoring", "runtime interception", "behavioral monitoring", "trajectory", "tool use", "provenance", "anomaly detection", "mitigation", "guardrail", "policy enforcement";
- **Financial:** "financial agent", "banking agent", "financial AI agent", "financial tool", "financial transaction", combined with security, prompt-injection, tool-misuse, runtime, safety or mitigation terms.

**Database variant.** The OpenAlex interface available to the review is lexical and relevance-ranked, and it does not accept Boolean operators. The blocks were therefore translated into eleven free-text queries, each combining at least one term from blocks A, B and C. Two queries (Q7, Q8) carried the financial block. The exact strings are reproduced in Table A.1. Each query was restricted to publication years 2019–2026. Page 2 was also retrieved for the two queries with the highest page-1 yield of eligible records (Q1, Q2), giving 13 result pages and 320 records in total.

The final search date was **25 September 2026**, and every counted search ran on that date. The raw output of every query is stored unchanged, and a script recomputes all counts from it (`chapter2/slr/`).

**Retrieval cap.** Only the relevance-ranked top of each query was screened: 24–25 records per page, the maximum the tool returned. The index estimates show that far more records matched the query terms. This cap is a deliberate feasibility decision, consistent with the protocol's instruction not to screen thousands of records manually. It is also the review's largest search limitation (Section 2.12.4). The stopping rule, the tool's handling of each string, and a one-off pilot probe that is not counted are all documented in the search record.

**Eligibility.** A study was included when it met six criteria fixed before assessment: it concerns tool-using AI agents or LLM-integrated applications that ingest untrusted content; it addresses a security, safety, robustness, monitoring or misuse problem; it makes a substantive technical or empirical contribution; it informs at least one dimension relevant to REM; it gives enough information to extract that contribution; and it was published between January 2019 and 25 September 2026, or is a necessary foundational source. Secondary studies were not synthesized as primary evidence. The full criteria and the exclusion labels are in Appendix A.

### 2.2.4 Study selection

Selection had two stages, both carried out by a single reviewer: the thesis author, assisted by an AI coding assistant (Claude Code), as recorded in the search-strategy file (`CHAPTER2_SYSTEMATIC_SEARCH_STRATEGY.md`).

1. **Title and abstract screening** of the 219 records that remained after automated deduplication. Records counted as duplicates when they shared a DOI or their normalized titles matched; this removed 101 of the 320 hits.
2. **Eligibility assessment** of the records that passed screening.

**Full texts were not retrieved.** The network policy that blocked the databases also blocked publisher and preprint servers. All 104 reports sought for retrieval (45 database, 59 other-methods) were therefore *not retrieved*, and eligibility was assessed on **records**: title, abstract, indexed metadata, Crossref metadata and, for two records without an indexed abstract (VIGIL and R-Judge), the abstract text returned by a web search. PRISMA 2020 distinguishes records, reports and studies; in this review each included study is represented by a single index record, and no full-text report was assessed. This departure from standard practice is shown in the PRISMA flow diagram (Figure 2.1). A supplementary check on 28 October 2026 (Section 2.12.4) re-examined the records of the closest studies; it did not add full texts.

**Other-methods stream.** The 70 other-methods records were assessed in the same way against the prior verification record. Eleven were the same study as a database record and were counted once.

**Screening log.** Every decision, with its reason, is in `CHAPTER2_SCREENING_LOG.csv`.

**Table 2.1. Study selection (counts computed from the screening log)**

| Stage | Unit | Databases (OpenAlex) | Other methods |
|---|---|---:|---:|
| Identified | records | 320 | 70 |
| Removed before screening (duplicates; same study as a database record) | records | 101 | 11 |
| Screened (title/abstract) | records | 219 | — |
| Excluded at screening | records | 174 | — |
| Sought for retrieval (full text) | reports | 45 | 59 |
| **Not retrieved** (network policy) | reports | **45** | **59** |
| Assessed for eligibility **at record level** (no full-text report available) | records | 45 | 59 |
| Excluded at eligibility | records | 5 | 28 (6 background, 21 foundational/methodological, 1 withdrawn) |
| **Included** | **studies** | **40** | **31** |
| **Total included studies** (each represented by its index record) | studies | **71** | |

**Recall of the database search.** Of the thirteen named prior-art studies, the database search retrieved three: Task Shield, LlamaFirewall and, with corrupted metadata, AgentDojo. The other ten entered through the other-methods stream. This low recall of known relevant studies is itself a finding about the search, discussed in Section 2.12.4.

![Figure 2.1. PRISMA 2020 flow diagram of the record-level review. Full-text reports were sought but not retrieved; eligibility was assessed on records. Counts are computed by script from the stored search output and the screening log.](revision_R2/figures/fig2_1_prisma_r2.png){width=88%}

### 2.2.5 Quality appraisal, data extraction and synthesis

Every included study was appraised against a ten-item checklist and assigned to a category of **record-visible evidence**: HIGH, MODERATE or LIMITED. The categories describe how much of a study's evidence could be verified from its record, not its intrinsic quality. Of the 71 included studies, 10 are HIGH, 36 MODERATE and 25 LIMITED; 36 are peer reviewed. Every claim this chapter makes about a study is marked with its level of verification: **M**, metadata verified; **A**, supported by the abstract as indexed; **R**, supported by the authors' repository documentation; **U**, resting only on search-engine excerpts and unverified; **F**, verified in the full text. Twenty-one fields were extracted per study. No meta-analysis was possible, because the studies differ in agents, attacks, benchmarks, success definitions and metrics; the synthesis is qualitative and structured by theme, and author-reported figures are never compared across studies as if they were measured on a common scale. The appraisal rules, the extraction fields and the synthesis procedure are given in full in Appendix A.

## 2.3 Threats Against AI Agents

The OWASP Gen AI Security Project lists prompt injection first among risks to LLM applications. It distinguishes *direct* injection through the user's prompt from *indirect* injection through external content (OWASP Gen AI Security Project, 2025). This is an official practitioner source and is used only for terminology.

The threat evidence below comes from 23 included studies whose primary role is an attack, benchmark or threat analysis. Studies of defenses contribute threat evidence where they evaluate against named attacks.

**Why agents change the problem.** Three structural properties distinguish agent security from the security of a stand-alone model: several input channels of different trustworthiness enter the same context; state persists across a trajectory, so content read at one step can shape an action several steps later; and outputs include tool calls with external effects. Benchmark studies show that these properties matter empirically (Wei et al., 2026; Ruan et al., 2024). The background on agent architecture, and the evidence on tool-channel threats, memory poisoning and multi-step drift, which lie outside the threat model evaluated in this thesis, are in Appendix A.

### 2.3.1 Direct and indirect prompt injection

**Indirect injection.** Greshake et al. (2023) showed that instructions planted in data retrieved at inference time can compromise an LLM-integrated application remotely. Such retrieved prompts can act like arbitrary code execution and control which APIs are called. In tool-using agents, the attacker needs only to influence some content the agent will read. The malicious content then enters through the **observation channel**, *after* the user's request has been received and inspected.

**Benchmark evidence.** Agent-specific benchmarks quantify the threat:

- **InjecAgent** has 1,054 cases covering 17 user tools and 62 attacker tools. A ReAct-prompted GPT-4 agent was vulnerable in 24% of cases, and success nearly doubled when the injection was reinforced with a "hacking prompt" (Zhan et al., 2024).
- **Agent Security Bench (ASB)** covers ten scenarios with more than 400 tools and 27 attack and defense methods. It reported a highest average attack success rate of 84.30% across 13 backbones, and found current defenses of limited effectiveness (H. Zhang et al., 2025).
- **AgentVigil** automates black-box red-teaming. It achieved 71% and 70% success against agents based on o3-mini and GPT-4o on AgentDojo and VWA-adv, nearly double handcrafted baselines (Z. Wang et al., 2025).
- A demonstration against web-navigation agents embedded universal triggers in page HTML and achieved credential exfiltration and forced clicks on real websites (Johnson et al., 2025). This study is LIMITED EVIDENCE: its abstract gives no figures.

### 2.3.2 Adaptive attackers

Adaptive attacks bypassed all eight indirect-injection defenses evaluated by Zhan et al. (2025), with attack success consistently above 50%. ToolHijacker (J. Shi et al., 2026) and AI² (Y. Zhang et al., 2024) report similar defeats of the defenses they tested. Detection results measured against fixed attack templates are therefore upper bounds on robustness, not estimates of it.

## 2.4 Benchmarks and Threat Models

Benchmarks operationalize threat models, and they bound what a defense can be shown to achieve. Table A.2 evaluates the benchmarks used by included studies on seven dimensions:

- what the benchmark actually measures;
- its threat model;
- its execution realism;
- its financial relevance;
- its multi-step coverage;
- whether it measures utility;
- its limitations.

**Audits of benchmark validity.** Two included meta-research studies qualify how far any of these scores can be read as measurements of safety:

- M. Q. Li et al. (2026; preprint) catalogued 40 agent-safety benchmarks and found no ranking concordance across evaluation dimensions (Kendall's *W*). Benchmark choice alone can therefore change which system appears safest.
- Y. Wang et al. (2026; preprint) found that on one binary trace-judgment benchmark an "always positive" baseline outranked five models under F1. They also found that a cross-benchmark correlation moved from −0.64 with seven models to +0.02 with eighteen, an artefact of small panels.

**Benchmarks built with the defense.** Two further observations come from the extraction. First, six included defense or benchmark studies introduce the benchmark on which their own method is evaluated: SIREN, TS-Bench, SciSafetyBench, NEXUS-Bench, PromptShield and the MCP policy-enforcement point's controlled dataset. Second, most of these report no evaluation on an independent benchmark in the verified record. NEXUS is an exception: it reports out-of-distribution results on R-Judge.

**AgentDojo in particular.** AgentDojo receives particular attention because of its executable Banking suite, but the evidence does not support calling it the best benchmark. Its advantages for REM's question are specific:

- tools execute and change environment state;
- utility and security are measured separately;
- a Banking suite exists.

Its limitations are equally specific:

- a small number of distinct user tasks;
- robustness claims bounded by the attacks actually evaluated (Section 2.3.2);
- no verified finance-specific analysis in the literature reviewed here.

The number of distinct tasks, not the number of generated runs, bounds what an evaluation on it can conclude (Chapter 3 treats this under grouping).

## 2.5 Defensive Approaches

The 42 included defense and design studies differ along two dimensions that the literature rarely separates:

- **where they intervene:** at the input, in the context, in the model, in the system architecture, at the policy or tool layer, around the agent loop at runtime, or after an action has taken effect;
- **what they observe:** an isolated input, an individual tool call, a plan, the flow of data between steps, a trajectory, or the consequence of an action.

This section organizes defenses by where they intervene. Section 2.6 examines what runtime monitors observe, and Section 2.8 examines how they decide and mitigate.

Two families that act before the action boundary are summarized here and reviewed in Appendix A. *Input- and model-level protection* (detectors of embedded instructions, input transformation, and training the model to follow only the prompt channel) reports strong in-distribution results but acts on text, not on actions, and has been bypassed by adaptive attacks (J. Shi et al., 2026; Y. Zhang et al., 2024). *System-level and information-flow defenses* change the architecture so that untrusted data cannot steer control flow; their guarantees hold for the threat models their authors formalized, and one such design was later defeated by new attacks (Y. Wu et al., 2025; E. Li et al., 2026).

### 2.5.1 Policy enforcement and tool restriction

**Classical basis.** This family descends from execution monitoring. Schneider (2000; foundational source) characterized the policies a monitor can enforce by observing a system's execution and halting it before a violation: the safety properties.

**Included instances:**

- **Progent** expresses privileges as rules over tool names and arguments, with solver-checked updates. It reduced attack success from 39.9% to 1.0% on AgentDojo and from 70.3% to 3.9% on ASB (T. Shi et al., 2025; preprint).
- **AgentSpec** enforces rules written as trigger, predicate and enforcement. It prevented over 90% of unsafe code-agent executions and all hazardous embodied actions, and gave 100% compliance in autonomous driving, at millisecond overhead (H. Wang et al., 2026).
- **Conseca** argues for policies generated just in time for each task context and enforced deterministically (Tsai & Bagdasarian, 2025; LIMITED EVIDENCE).
- **MCP policy-enforcement point.** A policy-enforcement point for MCP agents intercepts at the tool-call boundary with declarative rules over cross-step information-flow labels, and keeps a hash-chained audit log. On a controlled dataset, it reduced attack success from 40.0% to 5.0%, against 35.0% for the strongest prompt-only baseline (S. Wang et al., 2026). The same study also reports:
  - a task-level false-positive rate of 30.0%, attributed mainly to by-design capability denials;
  - residual attack success of 16.7% on one backend, due to a rule-coverage gap;
  - sub-millisecond overhead.
- **LATTICE** gates execution through policy-as-code with deterministic verdicts, escalates to human operators on a confidence basis, and keeps cryptographic audit trails (Calboreanu, 2026).

**Limitations for REM.** These studies are fast, auditable and, in the architectural cases, provable for the threats they address. Two limitations recur:

- **The question is binary.** An enforcer answers whether an action is permitted. It does not estimate how likely a *permitted* action is to have been induced by an adversary.
- **Policy coverage bounds protection.** The policy-enforcement point's residual 16.7% attack success on one backend is a rule-coverage gap in its authors' own words.

**Learned and LLM-based guardrails.** A further family uses learned models or language models to judge actions or trajectories: generated guardrail code, verification against rule circuits, adaptive checks kept in memory, step-level guardrail models and verify-before-commit designs (reviewed in Appendix A). These cover a broad range of semantic violations without a hand-written policy for each. Their limits recur: judgement by a language model adds latency and can vary between runs, accuracies are measured on the authors' own benchmarks, and the verified records do not report calibrated probabilities that could be combined with the consequence of an action, with the single exception of NEXUS (Section 2.8.3).

### 2.5.2 Goal–action consistency and provenance

The family most directly aimed at indirect injection asks whether a proposed action is *justified* by the user's task, rather than whether it is harmful in itself:

- **Task Shield** verifies whether each instruction and tool call serves the user's goals. It reduced attack success to 2.07% with 69.79% utility on AgentDojo with GPT-4o (F. Jia et al., 2025).
- **MELON** re-executes the trajectory with the user's prompt masked and flags an attack when the actions remain similar (Zhu, Yang, et al., 2025).
- **ProvenanceGuard** asks whether a tool call is supported by traceable evidence in the context. Relative to an LLM-as-judge baseline, it reduced error on misaligned traces from 44.3% to 2.1% on Agent-SafetyBench and from 32.4% to 18.7% on WorkBench (She et al., 2026; preprint). Its reported intervention rate on aligned traces (14.5% against 10.9%) and its extra cost are PARTLY UNVERIFIED.

These approaches share one insight: under indirect injection, the useful evidence concerns the *relation* between an action and its sources. They differ in cost. MELON adds an execution, and Task Shield and ProvenanceGuard add LLM reasoning.

## 2.6 Runtime Monitoring and Behavioral Analysis

This section concerns the evidence a runtime layer can extract from the agent's behavior, as distinct from the text it receives. That evidence is the domain of REM's Behavioral Analysis Layer.

Runtime monitors differ in **decision granularity** (whether a decision is taken for each proposed step, for a plan, or for an episode) and in **evidence scope** (whether the decision uses only the current step or also the history that led to it). REM decides for each proposed call and conditions on the episode so far; Task Shield, ProvenanceGuard and VIGIL are in the same group. Sequence-level and accumulating monitors (finite-state conformance engines, learned Markov chains, latent-state models, session risk with decay) are reviewed in Appendix A.

### 2.6.1 Provenance and cross-step information flow as evidence

A second line of evidence concerns *where an action's content comes from*. In an indirect injection against a banking agent, the attacker typically supplies the decisive arguments inside untrusted content: a recipient account, an amount, a new payee. Whether an argument can be traced to the user's request or to trusted state is therefore strong evidence of adversarial induction.

**Included studies.** Eight of the 42 included defense and design studies code provenance or information-flow evidence as present (Table A.5). They realize it in three ways:

- **by analysis:** ProvenanceGuard's evidence tracing;
- **by construction:** CaMeL, ACE and f-secure extract flows from trusted inputs;
- **by labels:** RTBAS's dependency screeners and the MCP policy-enforcement point's labels for source integrity and data sensitivity.

### 2.6.2 What is known about the empirical value of behavioral and provenance evidence

The review found **conflicting evidence** on whether trajectory and provenance components change outcomes. All three direct tests of a component's contribution are single studies on their authors' own benchmarks.

- **A null result for trajectory evidence (unverified).** According to search-engine excerpts that could not be checked against the abstract or the full text (level U), AgentTrust's ablation found that disabling its session tracker left verdict accuracy unchanged on both of its benchmarks (C. Yang, 2026). Because this result is unverified, the conflict described below rests on one verified and one unverified finding.
- **A positive result for cross-step provenance.** In the MCP policy-enforcement point, disabling cross-step label propagation raised the call-level false-negative rate by 26.4 percentage points on the authors' controlled dataset (S. Wang et al., 2026; HIGH EVIDENCE). The authors frame the result as mechanism-coverage evidence, not a deployment estimate.
- **A positive result for provenance against an LLM judge.** ProvenanceGuard's error reductions relative to an LLM-as-judge baseline indicate that evidence tracing is informative on misaligned tool calls (She et al., 2026; the headline figures are verified at abstract level).
- **Context for these results:**
  - MI9's evaluation was synthetic;
  - ProbGuard's gains were in autonomous-driving and embodied settings;
  - DreamGuard's figures in the verified record concern latency, not detection;
  - constitutional monitors saturated quickly, and further optimization overfitted (Storf et al., 2026).

The conflict is informative rather than contradictory:

- The null result concerns a *session tracker of order-aware chain detectors* in a rule-dominated system on coding- and shell-oriented scenarios.
- The positive results concern *cross-step information-flow labels* and *evidence provenance* against injected or misaligned tool calls.

On the included evidence, it is plausible that provenance-type trajectory evidence contributes under indirect injection while generic sequence patterns may not. No included study tests either kind of evidence as an input to a *calibrated estimator*, and none tests it on financial actions.

## 2.7 Statistical and Algorithmic Foundations Relevant to REM

A runtime decision layer that assigns graduated responses must solve four methodological problems:

- turn evidence into an estimate of how likely an action is to be adversarially induced;
- make that estimate interpretable as a probability;
- combine the probability with the consequence of the action to reach a decision;
- record why the decision was made.

A layer that observes several steps must also decide how to accumulate evidence over time. This section explains **why** each established method is relevant and what the included studies show about its use in agent security. The methods are established, and none is a contribution of this thesis. Their precise form in REM, including the estimator, the calibration map, the loss structure and the verdict rule, is specified in Chapter 3 and is not repeated here. The sources in this section are **FOUNDATIONAL** or **METHODOLOGICAL SOURCES** admitted under criterion I6 (Appendix A.6).

The reasons for choosing logistic regression as the estimator, and the classical basis of sequential change detection, which REM uses only as an optional observe-only analysis, are reviewed in Appendix A.

### 2.7.1 Why calibration matters, and its limits

**Definition.** A classifier is *calibrated* when its predicted probabilities match observed frequencies. Calibration matters whenever a probability is multiplied by a cost, because miscalibration distorts the comparison between actions.

**Platt scaling.** Platt (2000) fits a sigmoid to a model's score *s* on held-out data:

$$\hat{p} = \frac{1}{1 + \exp(A s + B)} \qquad (2.2)$$

The mapping is monotone, so it preserves the ranking of predictions.

**Alternatives.**

- **Temperature scaling** is a one-parameter variant (Guo et al., 2017).
- **Isotonic regression** is nonparametric (Zadrozny & Elkan, 2002). Platt scaling tends to perform better with small calibration sets, whereas isotonic regression performs as well or better once calibration data are plentiful (Niculescu-Mizil & Caruana, 2005).
- **Beta calibration** contains the identity map on scores in [0, 1], which the logistic family applied to such scores does not (Kull et al., 2017).

In REM, Platt scaling on the logit is the adopted calibrator. Beta, isotonic and temperature calibration are reviewed alternatives and are **not adopted** (Chapter 3).

**Measuring calibration.** Calibration is measured by the expected calibration error (ECE; Naeini et al., 2015; Guo et al., 2017). ECE depends on the binning and on the size of the calibration set.

**Evidence from included studies.**

- **NEXUS** reports that Platt scaling reduced ECE from 0.085 to 0.013 on its benchmark. It also evaluated isotonic regression, and its authors report that Platt was less prone to overfitting on the small calibration split (Hossain et al., 2026; the calibration details are PARTLY UNVERIFIED).
- **C. Zhang et al. (2026)** caution against over-reading such improvements. In their ALFWorld analysis, Platt scaling reduced a confidence score's ECE from 0.463 to 0.006, while control regret under threshold routing stayed at 0.318 (preprint; figures PARTLY UNVERIFIED). A calibrated risk estimate is not the decision-relevant quantity for choosing an intervention.
- **LATTICE** adds independent peer-reviewed evidence in the same direction from a different setting. Across four planner families and 4,000 trajectories, a *confidence-threshold baseline* had a false-allow rate ranging from 0.03 to 0.998 (Calboreanu, 2026). A single threshold on a confidence signal was therefore unstable across the upstream models that produced the actions.

**Implication.** Calibration quality and control quality must be measured and reported separately. A probability, however well calibrated, does not by itself represent whether a trajectory remains recoverable.

### 2.7.2 Why expected-loss decisions are relevant

**The principle.** Cost-sensitive decision theory chooses the response with the lowest expected cost given the class probabilities and a cost matrix (Elkan, 2001). For responses *a* and a binary state *y*:

$$a^{\text{*}}(x) = \arg\min_{a} \sum_{y \in \{0,1\}} \Pr(y \mid x)\, C(a, y) \qquad (2.3)$$

**The reject option.** Chow (1970) showed that withholding an automatic decision is optimal when the expected cost of deciding exceeds the cost of rejecting. This is the classical basis for routing uncertain cases to human review.

**Requirements.** The rule needs calibrated probabilities (Section 2.7.1) and costs that reflect real preferences, which are rarely known precisely in security. Elkan's principle and Chow's analysis support REM's expected-loss verdict and its Escalate route. Neither source proposed REM's four-action design.

**Precedents among included studies.**

- **NEXUS** defines an expected-loss objective with fixed intervention costs and uses it to set loss-optimal thresholds inside a rule-first cascade (Hossain et al., 2026; cascade and loss-based threshold selection stated in the authors' repository README, level R; the cost values are PARTLY UNVERIFIED).
- **H.-H. Chen (2026)** prices the consequence of each action deterministically against a reserve.
- **Kaptein et al. (2026)** formalize a path-conditioned probability of policy violation.

Cost-based reasoning about agent actions therefore has precedents.

**Attribution for audit.** For a linear model under feature independence, the Shapley attribution of a feature is its coefficient times the feature's deviation from a reference, and on the log-odds of a logistic model the decomposition is exact (Lundberg & Lee, 2017). It is therefore suitable for an audit record that shows which evidence contributed to a decision. It is not a distinguishing mechanism: included systems provide audit traces as rules and findings, rule circuits, traceable evidence or hash-chained logs. In REM, attribution is audit-only and never enters the verdict. The full discussion is in Appendix A.

## 2.8 Runtime Decision and Mitigation

This section examines how runtime systems *act* on what they detect. It distinguishes four functions that the literature often conflates:

- **detection:** recognizing that something may be wrong;
- **risk estimation:** quantifying how likely or how severe;
- **decision:** selecting a response;
- **mitigation:** executing the response.

### 2.8.1 The space of runtime responses

The included systems use a common, graduated vocabulary:

- allow;
- block;
- modify: rewrite arguments, sanitize context, propose a safer alternative or request a revision;
- escalate: request confirmation or human review;
- restrict tools or privileges;
- interrupt or terminate;
- stage, undo or roll back effects.

Human participation is also studied directly. An analysis of 21 production agent systems found runtime approval in 15 of them, policy specification in 14 and scope configuration in 16. It found no production deployment of intent anchoring or trust labeling, the mechanisms most studied academically. It also identified a trade-off between approval fatigue and uncontrolled autonomy (P. Wang et al., 2026; preprint). A simulation study added in the supplementary update of 2 November 2026 reports, at abstract level, that human-in-the-loop approvals sharply reduce high-impact actions but degrade under user error and habituation (Kanaker et al., 2026; Section 2.12.5).

### 2.8.2 AgentTrust: runtime interception with graduated verdicts

AgentTrust (C. Yang, 2026; preprint; MODERATE EVIDENCE; PARTLY UNVERIFIED) is among the closest prior art to REM. It passed the inclusion criteria through the other-methods stream. The protocol asks that its runtime interception, verdicts, monitoring, multi-step handling, mitigation, evaluation, latency and ablation claims each be verified; the verification status of each is given below.

**Architecture and verdicts (level A).** AgentTrust intercepts agent tool calls *before execution* and returns one of four verdicts: allow, warn, block or review. Its abstract names a shell deobfuscation normalizer, SafeFix suggestions of safer alternatives, RiskChain detection of multi-step attack chains, and a cache-aware LLM judge for ambiguous inputs.

**Results (level A).** On its 300-scenario internal benchmark, a production-only rule set reached 95.0% verdict accuracy and 73.7% risk-level accuracy. On 630 independently constructed adversarial scenarios, the author reports 96.7% under a *patched* rule set, explicitly not zero-shot.

**What REM cannot claim.** AgentTrust already provides:

- pre-execution interception;
- a four-way graduated verdict set that includes human review;
- a modify-like response (SafeFix);
- session-level multi-step detection;
- component ablations with latency.

**Where the difference lies.** The defensible differences are narrower:

- **Evidence to verdict.** AgentTrust's verdicts come from analyzers and rules, with an LLM judge for ambiguous cases. The verified material reports no calibrated probability of adversarial induction.
- **Use of consequence.** Reversibility is one of the judge's dimensions, not an explicit loss that changes the decision at a fixed probability.
- **Threat and domain.** AgentTrust targets side effects of coding and shell agents. It does not report evaluation on indirect injection against a financial agent.

### 2.8.3 NEXUS: calibrated risk scoring with a four-way intervention set

NEXUS (Hossain et al., 2026; MODERATE EVIDENCE; PARTLY UNVERIFIED) is the closest prior art to REM's *decision* component. It passed the inclusion criteria through the other-methods stream as a preprint. It has since been published in the Findings of AACL 2026; the published record was checked on 11 November 2026. **The full text has not been read in either version.** Three sources below the level of the paper are used, and each statement names its source:

- **A**: the abstract of the published version (index record, 11 November 2026);
- **A0**: the abstract of the preprint (index record, 28 October 2026);
- **R**: the README of the authors' public repository (retrieved 1 November 2026; a copy and its SHA-256 are kept in the verification records). Repository documentation can differ from the paper.

**Architecture (A, R).** NEXUS is a structured-plan safety monitor that "applies a formal intervention policy" to select among allow, block, request confirmation and request revision. It combines deterministic safety rules, argument-level inspection and a *calibrated* logistic-regression risk score used for graded escalation. According to the README, the policy selects one intervention per plan, and the score is trained on a nine-dimensional plan feature vector.

**Decision policy (R).** The README states the policy explicitly: Block if any critical violation, or if the risk score ρ ≥ τ~b~ with at least one violation; Confirm if ρ ≥ τ~c~ or any high-severity violation; Revise if any medium-severity violation; otherwise Allow. It states that (τ~b~, τ~c~) = (0.75, 0.70) was selected on a safety–utility loss L(Π) = E[λ~s~u~s~ + λ~o~u~o~ + λ~c~c(Π(P))] over a 5×5 grid of (λ~s~, λ~o~), and that Platt scaling, fitted on a 60-instance calibration split, reduced ECE from 0.085 to 0.013 on the 128-instance test split.

**Results (A).** On a 128-instance synthetic benchmark the published abstract reports F1 of 0.949 and four-class intervention accuracy of 0.6406, 27.3 percentage points above rule-only selection. On R-Judge it reports F1 0.861 against 0.849 for rule-only; it matches rule-only on AgentHarm; and it reports 0% ASR at 99% control allow on an indirect-injection set. On its rule-blind stress set it reports F1 0.897 with a Revise recall of 0.500, and a median latency of 0.38 ms. The preprint abstract (A0) gave 0.881 and 0.205 ms for the last two figures, and the README gives different headline figures for a retrained scorer (for example F1 0.965 on the synthetic test split). The published abstract's figures are used here, and the differences are recorded rather than resolved. The README adds that on rule-blind plans the policy predicts only Allow or Block.

**Still unverified (level U).** The intervention costs, the definitions of the nine features and of the consequence annotations read by the rules, the session manager, and the limitations stated by the authors.

**What REM cannot claim.** NEXUS already provides calibrated logistic risk scoring, a formal policy over a four-way intervention set with confirmation and revision routes, a loss criterion for selecting its thresholds, and sub-millisecond latency.

**Where the difference lies.** Three differences can be stated at levels A and R:

- **Point of evaluation.** REM evaluates each proposed tool call during execution, with the episode history; NEXUS judges a structured plan.
- **Decision rule.** REM selects each verdict by minimum expected loss, with losses indexed by the consequence tier of the call, so the boundaries between verdicts move with consequence. NEXUS applies a rule-first cascade with two score thresholds chosen once by a loss criterion; consequence enters through rule severities.
- **Evaluation.** REM is evaluated by replaying recorded trajectories of real agents in an executable banking environment and scoring outcomes. NEXUS's headline results score plans against labeled interventions on a synthetic benchmark, with R-Judge, AgentHarm and an injection set as additional evaluations.

Whether any of these differences changes outcomes is an empirical question. NEXUS was not run in this thesis. Its repository was read on 13 November 2026 and not executed, and no valid adapter from a banking tool call to its plan representation exists (Chapter 4, Section 4.4.5).

**The scorer against the rules, as documented by the authors (R).** A working document in the repository, dated 23 May 2026 and written to answer reviewers, states that a paired test of NEXUS against its rule-only variant gives no difference in binary detection, and that the contribution of the learned scorer is to the choice among the four interventions (accuracy 0.6406 against 0.3672 for rules only on the synthetic test split). This is not the published paper and its figures may differ from the paper's. It matters here because it is the same pattern that this thesis measures for REM: the learned score adds nothing measurable to security beyond rules.

### 2.8.4 Other decision mechanisms

**Jackson (2025).** A working paper (LIMITED EVIDENCE; PARTLY UNVERIFIED) describes a policy engine in which a multi-dimensional risk score drives a deterministic enforcement state machine with allow, deny, sanitize and escalate decisions. Its decision set corresponds closely to REM's four verdicts. It is unrefereed, its full text was not accessed, and its evaluation claims are qualitative.

**Consequence-aware control.**

- H.-H. Chen (2026; preprint) prices each side-effect-bearing action, such as a payment or refund, against a safe default and gates it against a reserve capital budget. It does not estimate how likely the action is to have been induced.
- SafeAgent's decision core instantiates operators for risk encoding, utility-cost evaluation, consequence modeling and policy arbitration over persistent session state (H. Liu et al., 2026; level A). Whether these operators are realized through LLM reasoning is unverified (level U).
- NEXUS encodes consequence in plan annotations and rules.

**Confidence-based escalation.** LATTICE separates deciding from judging, so that no component both proposes and approves an action. It escalates to human operators on confidence, and reports zero unsafe actions across four planner families (Calboreanu, 2026). It achieved this at a conservative operating point that auto-allowed no action. In the same study, a confidence-threshold baseline's false-allow rate varied from 0.03 to 0.998 across planners.

**Transactional and reversible mitigation.**

- Cordon stages outward-facing effects in an outbox and executes reversible mutations in shadow state (Z. Chen et al., 2026).
- GoEX offers undo and damage confinement for post-facto validation (Patil et al., 2024).

Such substrates *consume* a decision and could supply the mechanics of a hold or undo response.

## 2.9 Financial AI-Agent Security

The protocol asks that general agent-security evidence be kept separate from financial-agent evidence. A general benchmark is not counted as financial evidence merely because one of its scenarios is financial.

### 2.9.1 General agent-security evidence with a financial component

Several included general studies contain a financial element but report no finance-specific analysis in the verified record:

- **AgentDojo** includes an executable Banking suite (Debenedetti et al., 2024).
- **ASB** includes finance as one of ten scenarios (H. Zhang et al., 2025).
- **AgentHarm** includes fraud among eleven harm categories (Andriushchenko et al., 2025).
- **ClawSafety** includes finance among five professional domains. Its scenarios include redirecting financial transactions (Wei et al., 2026).
- **ToolEmu** cites financial loss as a risk example (Ruan et al., 2024).
- **RTBAS** cites financial transactions as a motivating example (Zhong et al., 2025).

These studies establish that financial actions are within the attack surface that general benchmarks cover. They do not establish how defenses perform on financial actions specifically.

### 2.9.2 Financial-agent evidence

Four included studies have a primarily financial setting, and none reaches MODERATE or HIGH EVIDENCE:

- **Castro-Maldonado et al. (2026)**, peer reviewed, study a semantic firewall with online ensemble learning in an agentic retrieval-augmented banking chatbot. The record specifies neither the threat model nor the results (LIMITED EVIDENCE).
- **Z. Chen, J. Chen, et al. (2025)**, a preprint position paper, argue that accuracy and return metrics give an illusion of reliability for financial agents. They propose model-, workflow- and system-level stress testing, illustrated by an audit of six agents on three tasks (LIMITED EVIDENCE).
- **H.-H. Chen (2026)**, a preprint, frames consequence pricing actuarially, with payments and refunds as examples (LIMITED EVIDENCE; partial financial focus).
- **FinHarness** (H. Jia et al., 2026; preprint) is the closest domain-specific runtime system. It combines a query monitor fusing intent with cross-turn drift, a tool monitor for each prospective call, and a cascade routing verification between a lightweight and an advanced LLM judge. It reports attack success falling from 38.3% to 15.0%, with benign approval moving from 41.1% to 39.3%. All of these figures were measured on **FinVault** (Z. Yang et al., 2026). The review record of 25 September 2026 notes that FinVault's arXiv preprint was **withdrawn by its authors**, with a comment citing legal, intellectual-property and affiliation reasons rather than an error in the benchmark; its OpenAlex record carries no retraction flag, and the withdrawal notice could not be re-checked on 28 October 2026 because arXiv was unreachable. A withdrawal for non-scientific reasons does not invalidate measurements made on the benchmark. It does mean that FinHarness's figures cannot be confirmed against a publicly maintained version, so they are reported as author-reported results with that caveat, and FinHarness is appraised LIMITED EVIDENCE by override.

**Background SoK.** A systematization of LLM-agent security in agentic commerce (Mao et al., 2026) organizes financial threats along five dimensions and derives twelve cross-layer attack vectors. It places *transaction authorization* at the center of the financial threat model. It is a secondary study, cited as background.

### 2.9.3 Why financial execution raises the requirements

Three properties of financial execution raise the requirements on a runtime layer. The first two are established in the included sources; the third is this chapter's inference from them.

- **Irreversibility.** Some financial actions cannot be recalled. This is encoded in consequence pricing (H.-H. Chen), in irreversibility flags checked by rules (NEXUS), and in transactional staging (Cordon).
- **Attacker-supplied arguments.** Under indirect injection, recipients and amounts can be planted in the content the agent reads, which makes argument provenance especially informative (Section 2.6.1).
- **Heterogeneous consequences.** A balance query and a transfer may both be permitted, yet differ sharply in the harm an induced call could cause. The same probability of adversarial induction therefore need not warrant the same response.

**Regulatory motivation.** Regulation (EU) 2024/1689 requires that high-risk AI systems allow automatic event logging (Article 12) and effective human oversight, including the ability to intervene or halt (Article 14) (European Parliament & Council of the European Union, 2024). Whether a given financial agent is high-risk is not assessed here. The provisions motivate an audit record for every decision and an explicit route to human review.

### 2.9.4 Requirements derived for a runtime layer protecting a financial agent

Six requirements follow from Sections 2.3–2.9:

- **R1** pre-execution mediation of each proposed action;
- **R2** provenance evidence on action arguments;
- **R3** consequence-differentiated responses at the same estimated probability;
- **R4** a human-review route;
- **R5** an audit record for every decision;
- **R6** joint measurement of security, benign utility, intervention behavior, calibration and latency.

## 2.10 Comparative Evidence Synthesis

Two tables compare the included runtime defense and design studies. Both are built from the systematic evidence matrix (`CHAPTER2_SYSTEMATIC_EVIDENCE_MATRIX.csv`).

- **Table A.5** (Appendix A) records what each study observes and does, using the columns specified in the review protocol.
- **Table A.8** records how the studies closest to REM turn evidence into a decision.

**Coding.** Yes = reported in the verified record; NR = Not Reported; NV = Not Verified; NA = Not Applicable. A property that the record does not report is **not** inferred to be present or absent. Financial context is coded Yes only for a primarily financial setting. Evidence levels are HIGH, MOD (moderate) and LIM (limited), as defined in Section 2.2.5.

**Table A.5** (42 defense and design studies × 13 properties) is reproduced in **Appendix A**. In summary: 41 of the 42 studies operate at runtime, 34 code tool/action evidence, 21 multi-step handling, 17 behavioral evidence and 8 provenance evidence as present in the record; these counts describe what the records report (Section 2.2.5), not what the systems lack.

**Reading the tables.**

*Row by row*, every individual property in REM's design appears somewhere in the included studies:

- calibrated logistic scoring with a four-way intervention set: NEXUS;
- pre-execution interception with graduated verdicts and human review: AgentTrust, RTBAS, LATTICE;
- consequence-dependent control: H.-H. Chen, NEXUS, SafeAgent;
- provenance and cross-step information-flow evidence: ProvenanceGuard, CaMeL, ACE, RTBAS, the MCP policy-enforcement point;
- trajectory-aware monitoring: MI9, PRISM, ProbGuard, DreamGuard, ToolSafe, AgentTrust;
- latency and component ablation: AgentTrust, NEXUS, the MCP policy-enforcement point;
- a financial runtime harness: FinHarness;
- the limits of calibration and confidence thresholds for control: C. Zhang et al.; LATTICE.

*Column by column*, the combinations thin out:

- **NEXUS** alone reports a calibrated probability together with costs and a graduated response. It does so at the plan level, on author-generated templates, with fixed intervention costs setting thresholds inside a rule-first cascade.
- **Provenance evidence**, where its contribution has been measured, feeds rules (the MCP policy-enforcement point) or a detector (ProvenanceGuard), not a probability estimator.
- **Financial focus** appears only in LIMITED EVIDENCE studies.
- **No included record** reports all three of the following together:
  - a calibrated probability of adversarial induction per proposed tool call;
  - consequence-dependent losses used to select among graduated responses;
  - evaluation on an executable financial environment with utility, intervention behavior and latency reported.

  This observation concerns the *records* examined. A combination this specific is easy to miss in a record-level review and is weak evidence of originality on its own (Section 2.12.2).

Table A.8, reproduced in Appendix A, records for the runtime systems closest to REM the decision basis, whether a calibrated probability is produced, whether consequence enters the decision, the human-review and graduated responses, and which evaluation dimensions are reported.

## 2.11 Critical Synthesis

**What is well addressed.**

- Threats are well characterized and benchmarked.
- Interception at the tool-call boundary is implemented in many forms, and deterministic enforcement is fast.
- Graduated responses, including human review, are standard.
- Architectural defenses offer formal guarantees for the threats they formalize.
- Calibration methods are mature and have one agent-safety application.

**What remains fragmented.** The pieces of a probabilistic, consequence-aware decision exist, but in different studies:

- a calibrated score with fixed-cost thresholds in a plan-level cascade (NEXUS);
- deterministic consequence pricing that ignores how an action arose (H.-H. Chen);
- consequence reasoning realized by LLM operators (SafeAgent);
- provenance evidence feeding rules or a detector (the MCP policy-enforcement point; ProvenanceGuard);
- financial focus in a judge cascade evaluated on a benchmark that is no longer publicly maintained (FinHarness).

**Conflicting evidence, presented rather than resolved.**

- **Value of trajectory evidence.** The AgentTrust ablation reportedly found no effect of a session tracker (level U). The MCP policy-enforcement point found a large effect of cross-step labels. The kind of trajectory evidence differs, and both are single studies.
- **Architectural guarantees.** IsolateGPT reports protection against the attacks it tested, and ACE later defeats it with new attacks.
- **Calibration as a remedy.** NEXUS reports a large ECE improvement. C. Zhang et al. report that a similar improvement left control regret unchanged. LATTICE reports that a confidence threshold's false-allow rate ranged from 0.03 to 0.998 across planners.
- **Safety figures versus utility.** LATTICE's zero false-allow was obtained at an operating point that auto-allowed no action. The MCP policy-enforcement point's attack-success reduction came with a 30.0% task-level false-positive rate. A safety figure alone is therefore not evidence of a usable defense.

**Where current approaches stop.**

- Most detectors and guardrails stop at a verdict and do not produce a probability that could be traded off against consequence.
- Most consequence-aware designs stop at the consequence and do not estimate the likelihood of adversarial induction.
- Most trajectory-aware systems stop at detection. The two ablations disagree about whether the trajectory component changes outcomes.
- Most evaluations stop at attack success: benign utility, intervention behavior, calibration and latency are reported unevenly.

**What the evidence does not support.** The systematic evidence does **not** support three claims that earlier drafts could have been read as making:

- that runtime interception, graduated verdicts or consequence awareness are absent from the literature;
- that combining several signals at the action boundary is rare. AgentTrust, the MCP policy-enforcement point, ToolSafe, DRIFT and FinHarness all combine signals at or near the tool call;
- that trajectory evidence is known to be ineffective. The evidence is mixed.

This section draws the thematic syntheses together. The full thematic table (Table A.9) is in Appendix A.

## 2.12 Research Gap and REM Positioning

### 2.12.1 Assessment of candidate gaps

The review protocol listed five candidate gaps, A to E, to be retained only if the systematic evidence supported them. Their assessment is in Appendix A (Table A.10). In summary, the review did not support a gap in the existence of runtime interception, graduated responses, calibration or consequence awareness; it supported narrowed versions of three gaps concerning evidence: on the value of behavioral and provenance evidence as input to a calibrated estimator (Gap C), on runtime defenses for financial actions in an open, executable benchmark (Gap D), and on a comparison of a consequence-aware decision with a consequence-independent baseline on the same estimator (Gap E).

### 2.12.2 Research gap supported by the systematic review (September 2026)

> The gap supported by the examined evidence is **empirical**. In the records of the 71 included studies (search date 25 September 2026), the review found (a) limited and conflicting evidence on whether behavioral and provenance evidence improves runtime decisions, and none testing it as input to a calibrated estimator for financial actions (Gap C); (b) no verified quantitative evaluation of a runtime defense on financial actions in an open, executable benchmark (Gap D); and (c) no evaluation that compares a consequence-aware decision with a consequence-independent baseline sharing the same estimator, while reporting attack success, benign utility, intervention behavior, calibration and latency separately (Gap E).

**Nature of the gap.** The gap concerns *evidence*: how established mechanisms behave when combined at the action boundary of a financial agent under indirect prompt injection, measured against a baseline that isolates the decision rule. It does not concern the absence of any single mechanism, and it does not concern a new learning algorithm. The specific combination that REM implements (Gap A) was not found in the examined records, but the thesis does not rest its originality on that absence: a combination this specific is easy to miss in a record-level review, and closely related designs exist (NEXUS, AgentTrust, SafeAgent).

**Bounds.** The gap is bounded by the search, which covered one database with a retrieval cap and a partly non-independent other-methods stream. It is also bounded by record-level appraisal: no study was read in full, and several properties of the closest studies are unverified (Section 2.12.4).

**Falsifiability.** A study that reports this combination and evaluation would require the contribution to be revised.

### 2.12.3 REM positioning: established by prior research versus proposed by this thesis

REM is a runtime mediation layer between a financial tool-using agent and its environment. It is organized in exactly five layers:

1. **Input & Context**;
2. **Detection**;
3. **Behavioral Analysis**;
4. **Decision Engine**;
5. **Mitigation**.

Chapter 3 specifies it. Table 2.2 separates what REM adopts from prior research from what this thesis proposes.

**Table 2.2. Established by prior research versus proposed by this thesis**

| Element | Established by prior research (included or foundational sources) | Role in REM |
|---|---|---|
| Runtime interception of each proposed tool call | Progent; AgentSpec; AgentTrust; RTBAS; MCP policy-enforcement point; LATTICE; PRISM; SafeAgent; Task Shield | Adopted, not claimed |
| Provenance / goal–action consistency evidence | ProvenanceGuard; Task Shield; MELON; CaMeL; ACE; RTBAS; MCP policy-enforcement point | Adopted as estimator input, not claimed |
| Behavioral / trajectory monitoring | MI9; ProbGuard; DreamGuard; PRISM; AgentTrust; ToolSafe; Forrest et al. (1996); Chandola et al. (2009, 2012) | Adopted, not claimed |
| Ridge logistic risk scoring | Cox (1958); le Cessie & van Houwelingen (1992); NEXUS | Adopted, not claimed |
| Platt calibration on the logit | Platt (2000); Guo et al. (2017); NEXUS | Adopted, not claimed. Beta, isotonic and temperature calibration are reviewed and **not adopted** |
| Minimum expected-cost decision; reject option | Elkan (2001); Chow (1970); NEXUS objective | Adopted, not claimed. Neither source proposed REM's four-action architecture |
| Consequence-dependent control | H.-H. Chen (2026); NEXUS; SafeAgent; AgentTrust | Adopted as declared consequence tiers, not claimed |
| Graduated responses including human review | AgentTrust; NEXUS; RTBAS; LATTICE; SafeAgent; Jackson; MI9 | Adopted, not claimed |
| Deterministic mitigation; reversible and staged effects | Progent; AgentSpec; Cordon; GoEX | Adopted, not claimed |
| Sequential change detection (CUSUM) | Page (1954); Basseville & Nikiforov (1993); Lorden (1971) | Optional, offline, observe-only analysis outside the verdict path; not claimed |
| Additive attribution for audit | Lundberg & Lee (2017); audit traces in NEXUS, AgentTrust, PRISM, LATTICE | Audit record only; never used for the verdict; not claimed |
| **Combination of provenance evidence, a calibrated per-step probability, tier-indexed expected-loss verdicts and deterministic mitigation at the action boundary, on an open executable banking benchmark** | Not reported in the examined records (record-level; weak evidence of absence) | **Proposed by this thesis (integrative design)** |
| **Evaluation that separates attack success, benign utility, intervention behavior, calibration and latency, against a consequence-independent baseline with the same estimator** | Not reported in the examined records | **Proposed by this thesis (empirical)** |

**Relation to AgentTrust and NEXUS.** What REM cannot claim against AgentTrust and NEXUS, and the narrower differences that remain, are set out in Sections 2.8.2 and 2.8.3 and are not repeated here. Several of the properties on which those differences rest are unverified (level U).

**Relation to other close studies.** REM does not claim:

- to be the first financial runtime protection (FinHarness);
- a risk-score-to-graduated-verdict pipeline (Jackson; SafeAgent);
- deterministic consequence pricing (H.-H. Chen);
- provenance analysis (ProvenanceGuard; the MCP policy-enforcement point);
- that calibration improves control (C. Zhang et al.; LATTICE).

### 2.12.4 Limitations of this review

The review is systematic in procedure but **not exhaustive**, and its conclusions are bounded as follows.

1. **Database accessibility.** Only OpenAlex was searched. IEEE Xplore, the ACM DL, Scopus and Web of Science, ScienceDirect, SpringerLink, the ACL Anthology, NeurIPS/PMLR, ICLR/OpenReview, USENIX and arXiv could not be reached (DATABASE ACCESS UNAVAILABLE). Elicit access was also unavailable. Their content was reached only through OpenAlex's index.
2. **Index coverage, ranking and retrieval cap.** OpenAlex's lexical relevance ranking surfaced general surveys ahead of specific recent preprints. Only the top 24–25 records per query page were screened, although index estimates ran to thousands. The database search retrieved only 3 of the 13 named prior-art studies, which shows that relevant studies can be missed.
3. **Non-independent second stream.** Thirty-one included studies came from the reference list of the previous chapter, which reflects the author's prior reading. This introduces selection bias, which the protocol's requirement to treat named prior art identically mitigates but does not remove.
4. **No full texts.** Eligibility, extraction and appraisal were performed on records; no full-text screening was performed and no claim is at level F. Nine included studies are PARTLY UNVERIFIED. Appraisal items that depend on full text (reproducibility, comparators, limitations) are mostly Not Verified. A supplementary record check on 28 October 2026 re-examined the closest studies (NEXUS, AgentTrust, ProvenanceGuard, FinHarness, FinVault, SafeAgent, C. Zhang et al., H.-H. Chen): it found a peer-reviewed version of ProvenanceGuard (ASE 2026), a changed title for C. Zhang et al., and several details of NEXUS and AgentTrust that are not supported by their current abstracts, which are now marked level U. Full texts remained unreachable.
5. **Single reviewer, AI-assisted.** Screening, extraction and appraisal were each done by one reviewer, assisted by an AI coding assistant, with no independent second screener and no agreement statistic. The appraisal checklist is transparent but is not a validated risk-of-bias instrument.
6. **Rapidly changing preprint literature.** 35 of the 71 included studies are preprints or working papers, and the field produces new preprints monthly. One source (FinVault) was recorded as withdrawn by its authors for non-scientific reasons. Preprint results may change or be withdrawn.
7. **Publication bias.** Defenses are usually reported on the authors' own benchmarks with favorable configurations. Negative results appear mainly in attack papers.
8. **Heterogeneity and no pooling.** Architectures, threats, benchmarks and metrics differ too much for meta-analysis. The synthesis is qualitative, and numeric comparisons across studies are avoided.
9. **Metadata errors in the index.** One record was corrupted (AgentDojo's DOI attached to another abstract) and one venue year was inconsistent (PromptShield). Both were detected and recorded, but others may have gone unnoticed.

**Before submission.** The protocol's Boolean blocks should be run directly in at least IEEE Xplore, the ACM DL, Scopus or Web of Science, and arXiv. Full texts of the included studies should be appraised, and the PRISMA flow and gap assessment updated.

### 2.12.5 Dated literature updates of 30 October and 2 November 2026 (outside the PRISMA flow)

Two updates were made after the registered search of 25 September 2026. Neither is part of the PRISMA flow: no count in Table 2.1 or Figure 2.1 changes, no record was added to the 71 included studies, and every statement below is at abstract level. Both are reproduced in full in Appendix A.

**30 October 2026.** The eleven queries of the registered search were re-run in the same index, restricted to publication year 2026. Of 215 unique records, 200 were not in the stored output of the registered search; they were title-screened by one reviewer. Five records bear directly on REM's positioning, among them:

- Kekatos et al. (2026) replay the recorded trajectories distributed with AgentDojo through a temporal-logic monitor, offline and without running an agent. Offline evaluation on AgentDojo's recorded traces therefore has a published precedent and is not a methodological contribution of this thesis. They also report that a planted line defeats a naive provenance check on most of the runs it would otherwise flag.
- Z. Liu (2026) replays ground-truth tool calls without a language model to evaluate fifteen injection detectors and reports that detector rankings transfer poorly between benchmarks.
- Yan et al. (2026) and Xin (2026) describe controllers close to REM's decision component: one commits the proposed or an alternative action by a learned value, the other routes among execute, confirm and block with calibrated probabilities. The first was later read in full (Section 2.12.6).

**2 November 2026.** Kanaker et al. (2026) propose an assumption-explicit simulation framework that separates compromise, harm and severity, and compare architectural controls across six threat scenarios and nine defense configurations. Their abstract reports that least-privilege tool design is the strongest single broad control and that human-in-the-loop approvals reduce high-impact actions but degrade under user error and habituation. The study is cited where it is consistent with positions of this thesis; no REM mechanism, parameter or experiment is derived from it.

### 2.12.6 Literature update of 11 November 2026: full-text readings (outside the PRISMA flow)

**Status of this addition.** On 11 November 2026 six papers were read in full from PDF files supplied by the author, whose SHA-256 values are kept with the study records. **This is the only place in this chapter where a full text was read.** The update is not part of the PRISMA flow. No count in Table 2.1 or Figure 2.1 changes, and no screening record is created retrospectively. Two of the six (Task Shield and MELON) are included studies of the review; three (PROVISO, CASEL, and the paper of C. Zhang et al.) were known from records; one (AgentBoundary) is new. Three further works are described from their abstracts only and are marked so. No systematic search to this date was possible, and newer competing work may exist.

**Table 2.3. Works examined in the updates of 11 and 13 November 2026 (F = full text read; A = abstract only; R = authors' repository read, paper not read)**

| Work | Level | What it does | Evaluation | Statement most relevant to this thesis |
|---|---|---|---|---|
| PROVISO (Yan et al., 2026; preprint) | F | Decides at the commitment point, after an action is proposed and before it is executed. Observations are typed by provenance into trusted and external. A trained controller estimates the value of the proposed and of an alternative action and commits the higher, after subtracting an offset chosen on development data | AgentDojo, four suites, by rolling out both continuations in a restored environment; folds keep all attack variants of a user task together | The controller is "fitted separately for each benchmark and therefore requires labeled outcomes from the target setting; we do not study transfer of a single trained controller across tasks" |
| AgentBoundary (T. Yang et al., 2026; preprint) | F | Counterfactual task families that vary apparent risk and permissibility independently on the same workflow; reports authorized-task completion and unsafe behavior separately | 17 agent configurations on general agent tasks | "high safety frequently coexists with poor authorized-task completion" |
| Calibration Is Not Control (C. Zhang et al., 2026; preprint, header states NeurIPS 2026) | F | Defines the value of an intervention as the difference between the expected utility of intervening and of continuing; proves that a strictly increasing recalibration of a score preserves the class of threshold policies | Prefix branching on agent benchmarks; no security benchmark | A risk score is sufficient for control only if the sign of the intervention value can be recovered from it |
| CASEL (Y. Zhang et al., 2026; preprint) | F | Selects among six execution modes by minimizing a per-mode cost that multiplies a failure probability by a consequence and adds mode costs | Simulation only | "Intervention effectiveness is assumed, not measured"; the per-mode cost "does not reduce harm beyond a product-score gate" |
| Task Shield (F. Jia et al., 2025; ACL) | F | Requires every instruction and tool call to contribute to a user-level task; contribution is scored by a language model | AgentDojo, live agents | A tool output may legitimately define subtasks when the user delegates to it |
| MELON (Zhu, Yang, et al., 2025; ICML) | F | Re-executes the step with the user prompt masked and flags an attack when the resulting tool calls remain similar | AgentDojo, live agents | Reported benign utility with GPT-4o falls from 80.41% to 68.04% |
| aiAuthZ (Kodathala, 2026; preprint) | A, R | An off-host gateway that binds each user message to an identity by a keyed signature and enforces role allow-lists, argument-level constraints and rate limits on tool calls, with a hash-chained audit log (repository whitepaper) | AgentDojo 0.1.35 banking, twenty task pairs, one model, with a fixed list of five known payees and password change denied (whitepaper) | Abstract: blocks all seven attacker-directed calls "at the cost of one legitimate first-time payment". Whitepaper: six blocked calls; clean utility 80% against 100%. The whitepaper states that the policy "stops what it is configured to stop" and that a comparison with CaMeL and Progent on AgentDojo "is not yet done" |
| Kairos (Hempel et al., 2026; preprint) | A | A reference monitor at the isolation boundary that defers and checks effects | AgentDojo, per its abstract | Attack success 47.0% to 2.7% with benign utility at the undefended level |
| NEXUS, published version (Hossain et al., 2026) | A, R | See Section 2.8.3 | — | A working document in the authors' repository states that the learned scorer gives no gain in binary detection over rules alone and contributes to four-class intervention accuracy |
| Progent (T. Shi et al., 2025; preprint) | R | Per-tool policies with argument restrictions, checked deterministically before each tool call. The repository holds a hand-written policy per AgentDojo suite at one commit and policies generated and updated by a language model at its current head | AgentDojo 0.1.29 is bundled with the repository | Its manual banking policy is a fixed list of five permitted recipients, with no entry for password change. It is replayed in Chapter 4, Section 4.4.3 |
| CaMeL (Debenedetti et al., 2025; preprint) | R | Extracts control and data flow from the trusted query and enforces capabilities at tool-call time (repository description) | Not examined | Not run and not approximated in this thesis |

The figures in Table 2.3 come from different agents, suites, attack sets and evaluation modes. They are listed to show what each work reports and are not compared with one another or with REM.

**Reading of the authors' repositories on 13 November 2026.** The publishers' sites of the works marked A were not reachable from the working environment, and no full text of NEXUS, aiAuthZ, Kairos, Progent or CaMeL was read. The official code repositories of four of them were reachable and were read, not executed, at fixed commits: Progent, aiAuthZ, NEXUS and CaMeL. Statements at level R come from the authors' own repository documents. They are below the level of the paper and may differ from it; where a repository document and an abstract differ, both are given. For Kairos only the abstract is known.

**What the update changes.**

- **The decision form is published.** CASEL's per-mode cost has the same structure as REM's expected-loss rule: a residual-risk term for each mode and a cost for choosing it. Together with NEXUS, this removes any claim that combining a risk estimate with consequence to choose among graduated responses is new.
- **Calibration is known not to be the lever.** C. Zhang et al. give the formal reason why recalibrating a score, or re-thresholding it, cannot recover a distinction that the score lacks. Their intervention-value target was tested in this thesis and failed on an unseen attack objective (Chapter 4, Section 4.6.6).
- **Over-defense is a general finding.** AgentBoundary measures at scale what this thesis measures for REM: safety obtained by withholding authorized actions.
- **Stronger utility is reported by heavier or differently placed mechanisms.** PROVISO, Task Shield and MELON report higher utility than REM reaches in replay, with a trained controller and restored rollouts or with a language model in the decision path. Kairos and aiAuthZ, at abstract level, act at the system boundary or add a trusted authorization channel. None was run under the conditions of this thesis.
- **Authorization needs a trusted input.** aiAuthZ, at abstract level, and PROVISO's admissibility rule both rest on trusted statements of what is authorized. REM's threat model has only the user's request as text.

### 2.12.7 Revised statement of the research gap

The statement of Section 2.12.2 was written from the records of September 2026. It framed the gap partly as the absence of a combined evaluation of a calibrated, consequence-aware decision. After the update of Section 2.12.6 the mechanism side of that statement is closed, and the gap is restated as follows. It is proposed wording, pending the supervisor's confirmation.

> Runtime defenses for tool-using agents now combine risk scoring, provenance and graduated interventions, and their authors report benchmark-specific fitting and unmeasured intervention effectiveness. Limited controlled evidence establishes whether a learned, consequence-aware runtime decision adds value over simple provenance and authorization rules for a banking agent when both the user task and the attack objective are unseen, and at what cost in legitimate task completion.

**Table 2.4. Assessment of the revised gap statement**

| Criterion | Assessment |
|---|---|
| Supported by recent literature | PROVISO states that transfer of its fitted controller is not studied, and it holds out user tasks, not attack objectives. CASEL states that intervention effectiveness is assumed. AgentBoundary reports widespread over-defense. None of the six papers read in full compares a learned monitor with parameter-free rules on the same trajectories. For NEXUS, aiAuthZ and Kairos this is known only from abstracts and, for the first two, from the authors' repositories |
| Distinct from published work | As an evidence gap, yes. As a mechanism gap, no: every mechanism involved is published |
| Specific | It names the class of system (a monitor without a language model in the decision path), the domain, the comparison and the conditions |
| Answerable by experiment | Yes, by recorded-trace replay with held-out objectives and tasks (Chapter 3, Sections 3.11.12 and 3.11.14) |
| Falsifiable | Yes. The statement "the learned policy adds value over the rules" is a paired contrast with an interval, and the data could have supported it |
| Consistent with the results | Yes. The answer obtained is largely negative (Chapter 4, Section 4.6.8) |

**Bounds.** The gap is bounded by the record-level review, by the absence of a systematic search after 30 October 2026, and by the abstract-level knowledge of three close works. A study that reports a held-out-objective comparison of a learned monitor with rule baselines on banking tasks would require the statement to be revised.

## 2.13 Chapter Summary

This chapter reported a record-level systematic review, reported following PRISMA 2020 and PRISMA-S, of runtime security for tool-using AI agents, with attention to financial execution. Full texts were not retrieved, so its findings rest on records.

**Selection.** The search of OpenAlex on 25 September 2026 identified 320 records. (A simulation study added in a supplementary update of 2 November 2026 is discussed separately at abstract level in Section 2.12.5; it does not change these counts.) After deduplication, 219 were screened, and 45 were assessed for eligibility at record level. Forty database studies were included. Another 31 came from the verified reference list of the previous chapter, giving 71 included studies. Of these, 10 are HIGH, 36 MODERATE and 25 LIMITED record-visible evidence.

**Themes.** The synthesis established the following:

- **Threats.** Indirect prompt injection through the observation channel is the best-evidenced threat to tool-using agents, and it is adaptive. Its harm materializes at the proposed tool call.
- **Defenses.** Runtime interception, deterministic enforcement, information-flow architectures, learned guardrails and provenance checks are all established. Adaptive attacks have repeatedly broken defenses, including architectural ones.
- **Behavioral and provenance evidence.** Many monitors observe trajectories. Evidence on their contribution is sparse and conflicting: a null ablation of a session tracker, and a large effect of cross-step information-flow labels.
- **Algorithmic foundations.** Logistic scoring, Platt calibration, expected-cost decisions with a reject option, and additive attribution are established. One agent-safety system (NEXUS) combines calibration with costs at the plan level. Calibration or a confidence threshold alone did not secure good control in two independent studies. CUSUM is reviewed only as an optional, observe-only analysis.
- **Decision and mitigation.** Graduated responses with human review are standard. How to combine a probability of adversarial induction with a declared consequence remains open. Intervention rates are rarely reported.
- **Financial agents.** All financial-context evidence is LIMITED, and the only quantitative financial runtime results cannot be confirmed against a maintained benchmark.

**The gap.** The gap stated from the systematic review concerned the evaluation of a calibrated, consequence-aware decision at the action boundary of a financial agent. Full-text readings in November 2026 showed that the decision form itself is published (NEXUS; CASEL) and that its known weaknesses are documented (C. Zhang et al.; AgentBoundary). The gap was therefore restated as one of evidence (Section 2.12.7): whether a learned, consequence-aware runtime decision adds value over simple provenance and authorization rules for a banking agent under unseen user tasks and attack objectives, and at what cost in legitimate task completion. Every mechanism involved is established. Only the controlled evaluation, including its negative results, is offered by this thesis.

Chapter 3 specifies the REM methodology through which the gap is addressed.
