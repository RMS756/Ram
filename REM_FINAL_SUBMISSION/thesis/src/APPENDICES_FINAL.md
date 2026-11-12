# Appendix A: Systematic Review: Search Strings, Supporting Tables and Evidence Matrix

This appendix holds material of the systematic review that Chapter 2 summarizes: the comparative evidence matrix of the 42 defense and design studies, and three supporting tables. The tables are reproduced unchanged from the review record of September and October 2026.

## A.1 Database searches

**Table A.1. Database searches (OpenAlex; 25 September 2026; years 2019–2026)**

| Query | Exact search string | Blocks | Records screened | Index estimate |
|---|---|---|---:|---:|
| Q1 (pages 1–2) | LLM agent indirect prompt injection runtime defense tool use | A+B+C | 50 | 1,366 |
| Q2 (pages 1–2) | LLM agent security runtime monitoring guardrail tool call | A+B+C | 49 | 1,123 |
| Q3 | tool-using language model agent behavioral trajectory monitoring anomaly detection safety | A+B+C | 24 | 5,572 |
| Q4 | LLM agent provenance goal alignment tool call misalignment detection | A+B+C | 25 | 484 |
| Q5 | prompt injection benchmark tool-integrated LLM agents attacks and defenses evaluation | A+B+C | 24 | 2,950 |
| Q6 | LLM agent memory poisoning goal hijacking multi-step attack | A+B | 24 | 579 |
| Q7 | financial LLM agent security prompt injection tool misuse | Fin+A+B+C | 24 | 1,368 |
| Q8 | banking agent safety benchmark financial transaction LLM agent | Fin+A+B | 25 | 536 |
| Q9 | calibrated risk score intervention policy LLM agent runtime safety | A+B+C | 25 | 880 |
| Q10 | privilege control policy enforcement LLM agents tool calls prompt injection | A+B+C | 25 | 1,380 |
| Q11 | pre-execution action validation guardrail autonomous LLM agent unsafe actions | A+B+C | 25 | 744 |
| **Total** | | | **320** | — |

## A.2 Benchmarks used by included studies

**Table A.2. Critical evaluation of benchmarks used by included studies**

| Benchmark (source) | What it measures | Threat model | Execution realism | Financial relevance | Multi-step coverage | Utility measured | Limitations |
|---|---|---|---|---|---|---|---|
| AgentDojo (Debenedetti et al., 2024) | Task utility, utility under attack and targeted attack success per episode; 97 user tasks, 629 security cases | Indirect injection via tool outputs | Executable, stateful tools; outcomes checked against environment state | One of four suites is Banking; no finance-specific analysis in the verified record | Yes (multi-tool episodes); number of genuinely multi-step attacks not verified | Yes, jointly with security | Limited number of distinct tasks; robustness claims bounded by the attacks evaluated (Section 2.3.2) |
| InjecAgent (Zhan et al., 2024) | Whether the next action after one injected tool response serves the attacker; 1,054 cases | Indirect injection (direct harm; data exfiltration) | Simulated single tool response | Not reported | No (short cases) | No | Isolates injection susceptibility; no benign utility |
| ASB (H. Zhang et al., 2025) | Attack success across stages; utility–security trade-off metric | Direct/indirect injection, memory poisoning, backdoor, mixed | Agent framework with >400 tools | Finance is one of 10 scenarios; not analysed separately | Yes (multiple stages) | Yes | Breadth over depth per scenario |
| AgentHarm (Andriushchenko et al., 2025) | Whether harmful multi-step tasks are completed | Malicious user | Synthetic tools | Fraud is one of 11 categories | Yes | Capability retention after jailbreak | Different threat actor from REM's |
| ToolEmu (Ruan et al., 2024) | Risky failures without adversary; 144 cases | No adversary | LM-emulated tools | Not reported (financial loss among risk examples) | Yes | Not the focus | Emulator and evaluator are LMs |
| R-Judge (Yuan et al., 2024) | LLM ability to judge safety risk in 569 multi-turn records | Behavioural safety risks | Recorded interactions (offline) | Not reported | Yes | Not applicable | Offline judgement, not runtime interception |
| ClawSafety (Wei et al., 2026) | Attack success in high-privilege workspaces; 120 scenarios, 2,520 trials | Injection via skills, email, web | Sandboxed real frameworks | Finance is one of five domains | Not verified | Not verified | Preprint; release announced |
| SIREN (J. Lin et al., 2026, VIGIL) | Tool-stream injection defense; 959 cases | Injection via tool metadata and feedback | Not verified | Not reported | Not verified | Utility under attack | Introduced with the defense evaluated on it |
| TS-Bench (Mou et al., 2026, ToolSafe) | Step-level detection of unsafe tool invocations | Unsafe invocations incl. injection | Not verified | Not reported | Yes (interaction history) | Benign completion | Introduced with the guardrail evaluated on it |
| NEXUS-Bench (Hossain et al., 2026) | Plan-level intervention accuracy; 128 held-out synthetic instances | Unsafe plans | Author-generated templates | Not reported | Plan-level | Paired benign cases | Authors: in-distribution results are upper bounds |
| FinVault (Z. Yang et al., 2026) | Financial-agent security (as originally reported) | Financial-agent attacks | Execution-grounded (as originally reported) | Yes | Not verified | Not verified | **Withdrawn by its authors; not evidence** |

## A.3 Where included defenses intervene and what they observe

**Table A.3. Where included defenses intervene and what they observe**

| Point of intervention | Included studies | Primary unit observed | What this position can and cannot see |
|---|---|---|---|
| Input / context text | InstructDetector (Wen et al., 2025); PromptShield (Jacob et al., 2025); attack-technique defenses (Y. Chen et al., 2025); Spotlighting (Hines et al., 2024); PromptGuard 2 in LlamaFirewall (Chennabasappa et al., 2025) | An input or retrieved text | Sees text before the model acts; does not see how the agent then acts |
| Model | StruQ (S. Chen et al., 2025) | Model behaviour under separated channels | Addresses the instruction/data confusion; requires training and model access |
| System architecture / information flow | f-secure IFC (F. Wu et al., 2024); RTBAS (Zhong et al., 2025); ACE (E. Li et al., 2026); IsolateGPT (Y. Wu et al., 2025); CaMeL (Debenedetti et al., 2025) | Data flow into planning and between tools or apps | Can prevent untrusted data from steering control flow; changes how the agent executes |
| Policy / privilege at the tool boundary | Progent (T. Shi et al., 2025); AgentSpec (H. Wang et al., 2026); Conseca (Tsai & Bagdasarian, 2025); MCP policy-enforcement point (S. Wang et al., 2026); LATTICE (Calboreanu, 2026) | Each tool call against a policy | Deterministic and auditable; answers "is this permitted?", not "how likely is this induced?" |
| Plan or reasoning | TrustAgent (Hua et al., 2024); Thought-Aligner (Jiang et al., 2025); NEXUS (Hossain et al., 2026); DRIFT planner (H. Li et al., 2025) | A plan or intermediate thought | Can intervene before actions exist; plans can change after new observations |
| Runtime around the agent loop | Task Shield (F. Jia et al., 2025); MELON (Zhu, Yang, et al., 2025); ProvenanceGuard (She et al., 2026); VIGIL (J. Lin et al., 2026); ToolSafe (Mou et al., 2026); DRIFT validator (H. Li et al., 2025); GuardAgent (Xiang et al., 2025); ShieldAgent (Z. Chen, Kang, & Li, 2025); AGrail (Luo et al., 2025); SafeScientist (K. Zhu et al., 2025); AlignmentCheck (Chennabasappa et al., 2025); AgentTrust (C. Yang, 2026); MI9 (C. L. Wang et al., 2025); PRISM (F. Li, 2026); ProbGuard (H. Wang et al., 2025); DreamGuard (Lin et al., 2026); SafeAgent (H. Liu et al., 2026); FinHarness (H. Jia et al., 2026); constitutional monitors (Storf et al., 2026) | Proposed action in context; sometimes the trajectory | Observes the action boundary; costs are latency and false interventions |
| Post-action / transactional | Cordon (Z. Chen et al., 2026); GoEX (Patil et al., 2024) | Staged or reversible effects | Can hold, undo or confine effects; consumes rather than produces a risk judgement |
| Consequence gating | Actuarial Action Interface (H.-H. Chen, 2026) | Priced action | Prices consequence; does not estimate adversarial induction |

## A.4 Runtime responses reported by included systems

**Table A.4. Runtime responses reported by included systems**

| System | Allow | Block | Modify / sanitize / revise | Escalate / human review | Restrict tools or privileges | Interrupt / terminate | Stage / roll back / undo | Decision granularity |
|---|---|---|---|---|---|---|---|---|
| Progent | Yes | Yes | Not Reported | Yes (approval for privilege expansion) | Yes | Not Reported | Not Reported | Per tool call |
| AgentSpec | Yes | Yes | Rule-defined | Not Verified | Not Reported | Not Verified | Not Reported | Per triggered event |
| RTBAS | Yes (auto-execute) | Not Verified | Not Reported | Yes (user confirmation) | Not Reported | Not Reported | Not Reported | Per tool call |
| MCP policy-enforcement point | Yes | Yes (deny) | Not Reported | Not Reported | Yes (capability tokens) | Not Reported | Not Reported | Per tool call with cross-step labels |
| LATTICE | Yes | Yes | Not Reported | Yes (confidence-based escalation to humans) | Not Reported | Not Reported | Not Reported | Per gated action |
| VIGIL | Yes (commit) | Yes (no commit) | Not Verified | Not Reported | Not Reported | Not Reported | Not Reported | Per speculative action |
| ToolSafe | Yes | Not Verified | Yes (guardrail feedback to agent) | Not Reported | Not Reported | Not Reported | Not Reported | Per tool invocation |
| MI9 | Yes | Yes | Not Verified | Not Verified | Yes (graduated containment) | Yes | Not Reported | Continuous, agent-level |
| PRISM | Yes | Yes | Not Verified | Not Verified | Yes (policy controls) | Not Verified | Not Reported | Per hook, session accumulation |
| SafeAgent | Yes | Yes | Yes (sanitization, replanning, argument rewriting) | Yes (human escalation) | Not Verified | Yes | Yes (rollback) | Per step over session state (PARTLY UNVERIFIED) |
| AgentTrust | Yes | Yes | Yes (safer alternatives) | Yes (warn; review) | Not Reported | Not Reported | Not Reported | Per tool call, session chains |
| NEXUS | Yes | Yes | Yes (request revision) | Yes (request confirmation) | Not Reported | Not Reported | Not Reported | Per plan, before execution |
| DreamGuard | Yes (PASS) | Yes (BLOCK) | Not Reported | HOLD (semantics Not Verified) | Not Reported | Not Reported | Not Reported | Per action with trajectory state |
| FinHarness | Yes (approve) | Yes | Not Reported | Escalation to an advanced LLM judge (not a human) | Not Reported | Not Reported | Not Reported | Per step, cross-turn |
| Jackson | Yes | Yes (deny) | Yes (sanitize) | Yes (escalate) | Not Verified | Not Verified | Not Verified | Not Verified |
| Cordon | Not Applicable | Not Applicable | Not Applicable | Not Verified | Not Applicable | Not Applicable | Yes (shadow state; effect outbox) | Per task transaction |
| GoEX | Not Applicable | Not Applicable | Not Applicable | Post-facto human validation | Not Reported | Not Reported | Yes (undo; damage confinement) | Per executed action |

## A.5 Comparative evidence matrix of defense and design studies

Coding as in Section 2.10: Yes = reported in the verified record; NR = Not Reported (not evidence of absence); NV = Not Verified; NA = Not Applicable. Evidence levels refer to record-visible evidence (Section 2.2.5).

**Table A.5. Comparative evidence for included defense and design studies (n = 42)**

| Study | Threat | Entry Point | Observation Unit | Runtime | Behavior | Tool/Action | Multi-Step | Provenance | Decision | Mitigation | Financial Context | Evidence Level |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C. L. Wang et al. (2025) [P59] | Emergent/unsafe agent behaviour (governance) | NA | Agent state and actions over time | Yes | Yes | Yes | Yes | NR | Yes | Yes (graduated containment) | NV | MOD |
| C. Yang (2026) [P64] | Unsafe tool-use side effects | Proposed tool call | Each proposed tool call (plus session chains) | Yes | Yes (seven chain detectors) | Yes | Yes (session tracker; no measurable effect in ablation) | NR | Yes | Yes (allow/warn/block/review; safer alternatives) | NR | MOD |
| Calboreanu (2026) [P40] | Unauthorised actions | NA | Proposed action at gated execution path | Yes | NR | Yes | NR | NR | Yes | Yes | NR | HIGH |
| Castro-Maldonado et al. (2026) [P32] | Customer-data protection / security (threat model not specified in abstract) | User queries and retrieved content | Query/response | Yes | NR | NV | NR | NR | Yes | NV | Yes | LIM |
| Chennabasappa et al. (2025) [P16] | Prompt injection; jailbreak; agent misalignment; insecure code | Untrusted inputs; agent reasoning; generated code | Inputs and chain-of-thought | Yes | Yes | NV | NV | NR | Yes | NV | NR | LIM |
| Debenedetti et al. (2025) [P52] | Prompt injection; data exfiltration | Untrusted data | Program control and data flow | Yes | NR | Yes | Yes (data flow across steps) | Yes | Yes | Yes | NR | MOD |
| E. Li et al. (2026) [P12] | Malicious apps; indirect prompt injection; planning/execution integrity and availability | Third-party apps and their outputs | Abstract plan, concrete plan and execution | Yes | NR | Yes | Yes | Yes | Yes | Yes | NR | MOD |
| F. Jia et al. (2025) [P01] | Indirect prompt injection | External data returned by tools | Each instruction and tool call | Yes | NR | Yes | NV | NR | Yes | NV | NR | HIGH |
| F. Li (2026) [P60] | IPI, unsafe tools, credential leakage, tampering | Tool inputs/outputs; files; credentials | Lifecycle hook events within a session | Yes | Yes (session risk accumulation) | Yes | Yes | NR | Yes | Yes | NR | LIM |
| F. Wu, Cecchetti, & Xiao (2024) [P08] | Indirect prompt injection | Any untrusted source feeding the planner | Planning inputs and structured plans | Yes | NR | Yes | Yes | Yes | Yes | Yes | NR | LIM |
| H. Jia et al. (2026) [P71] | Prompt-induced unauthorised financial actions | User queries; tool calls | Query and tool call with cross-turn state | Yes | Yes (partial: cross-turn drift, accumulated risk) | Yes | Yes | NR | Yes | Yes (block/approve; escalation to advanced judge) | Yes | LIM |
| H. Li et al. (2025) [P38] | Prompt injection via external tools | Tool outputs; memory stream | Function trajectory vs. planned trajectory | Yes | Yes | Yes | Yes | NR | Yes | Yes | NR | MOD |
| H. Liu et al. (2026) [P63] | Prompt injection propagating through workflows | Inputs and intermediate context | Stateful workflow | Yes | Yes | Yes | Yes | NR | Yes | Yes | NR | LIM |
| H. Wang et al. (2025) [P61] | Safety-specification violations | NA | Abstract state sequence | Yes | Yes | Yes | Yes | NR | Yes | Yes | No (non-financial) | MOD |
| H. Wang, Poskitt, & Sun (2026) [P50] | Unsafe actions | NA | Triggered action vs. rule predicate | Yes | NR | Yes | NV | NR | Yes | Yes | NR | MOD |
| H.-H. Chen (2026) [P67] | Consequences of side-effecting actions | NA | Each priced action | Yes | NR | Yes | NR | NR | Yes (consequence pricing vs. reserve) | Yes (gating) | Yes (partial: payments, refunds as examples) | LIM |
| Hines et al. (2024) [P47] | Indirect prompt injection | Untrusted documents | Input text | Yes | NA | NA | NA | Yes | NA | NA | NR | MOD |
| Hossain et al. (2026) [P65] | Unsafe plans | Proposed plan and arguments | Plan (with cross-turn session state) | Yes | Yes (partial: session manager) | Yes (argument-level) | Yes (partial: plan-level) | NR | Yes | Yes (allow/block/confirm/revise) | NR | MOD |
| Hua et al. (2024) [P55] | Unsafe planning | NA | Plan | Yes (planning stage) | NR | Yes (plan-level) | Yes (plan-level) | NR | NV | Yes (plan revision) | NR | LIM |
| Jackson (2025) [P66] | Governance violations | NA | Governed action | Yes | NV | Yes | NV | NR | Yes (multi-dimensional risk score) | Yes (allow/deny/sanitize/escalate) | NR | LIM |
| Jacob et al. (2025) [P23] | Prompt injection | Conversational and application-structured inputs | Input text | Yes | NR | NR | NR | NR | Yes | NR | NR | MOD |
| Jiang et al. (2025) [P56] | Unsafe intermediate thoughts | NA | Intermediate thought before action | Yes | Yes (thought-level) | NR | Yes (partial) | NR | NV | Yes (thought correction) | NR | MOD |
| J. Lin et al. (2026) [P11] | Tool-stream injection (manipulated tool metadata and runtime feedback) | Tool metadata and tool feedback | Speculative action before commit | Yes | NR | Yes | NV | NR | Yes | Yes | NR | HIGH |
| W. Lin et al. (2026) [P62] | Long-horizon hazardous drift | NA | Each call with trajectory prefix | Yes | Yes | Yes | Yes | NR | Yes | Yes (PASS/HOLD/BLOCK) | NR | MOD |
| Luo et al. (2025) [P39] | Task-specific and systemic risks | NV | Agent actions | Yes | NV | Yes | NR | NR | Yes | NV | NR | LIM |
| Mou et al. (2026) [P33] | Unsafe tool invocations incl. prompt injection | Requests and tool interaction history | Each tool invocation with history | Yes | Yes | Yes | Yes | NR | Yes | Yes | NR | MOD |
| Patil et al. (2024) [P10] | Incorrect or unsafe LLM-generated actions (non-adversarial) | NA | Executed action | Yes | NR | Yes | NR | NR | NV | Yes | NR | LIM |
| S. Chen et al. (2025) [P48] | Prompt injection | Data channel | Model input | NA | NA | NA | NA | Yes | NA | NA | NR | LIM |
| S. Wang, Zhu, & Li (2026) [P37] | Indirect prompt injection (path traversal, exfiltration, high-frequency tool abuse) | Externally retrieved data | Each tool call with cross-step labels | Yes | NR | Yes | Yes | Yes | Yes | Yes | NR | HIGH |
| She et al. (2026) [P58] | Misaligned tool calls incl. IPI | Tool outputs; context | Each tool call and its evidence provenance | Yes | Yes (partial) | Yes | NR | Yes | Yes | Yes | NR | MOD |
| T. Shi et al. (2025) [P49] | Indirect prompt injection; tool misuse | Tool outputs | Each tool call vs. privilege policy | Yes | NR | Yes | Yes (policy updates during task) | NR | Yes | Yes | NR | MOD |
| Storf et al. (2026) [P34] | Scheming (covert pursuit of misaligned goals) | NA | Externally observable trajectory | Yes | Yes | Yes | Yes | NR | Yes | NR | NR | LIM |
| Tsai & Bagdasarian (2025) [P51] | Context-inappropriate actions | NA | Proposed action vs. task-context policy | Yes | NR | Yes | NR | NR | Yes | Yes | NR | LIM |
| Wen et al. (2025) [P03] | Indirect prompt injection | Retrieved external content | Model hidden states and gradients for an input | Yes | NR | NR | NR | NR | Yes | NR | NR | MOD |
| Xiang et al. (2025) [P53] | Violations of safety guard requests | NA | Target agent actions | Yes | NR | Yes | NR | NR | Yes | Yes | NR | LIM |
| Y. Chen et al. (2025) [P24] | Prompt injection in retrieved data | Retrieved content | Input prompt | Yes | NR | NR | NR | NR | NR | NR | NR | LIM |
| Y. Wu et al. (2025) [P36] | Untrusted apps; cross-app security, privacy and safety issues | Third-party apps | App interactions | Yes | NR | Yes | NR | NR | NV | Yes | NR | MOD |
| Z. Chen et al. (2026) [P68] | Irreversible effects; cross-step violations | NA | Task-level transaction | Yes | NR | Yes | Yes | NR | NR | Yes (staging, rollback, recovery) | NR | LIM |
| Z. Chen, Kang, & Li (2025) [P54] | Policy violations over trajectories | NA | Action trajectory | Yes | Yes (trajectory-level) | Yes | Yes | NR | Yes | Yes | NR | LIM |
| Zhong et al. (2025) [P06] | Prompt injection; privacy leakage | Tool outputs / external content | Each tool call and its data dependencies | Yes | NR | Yes | NV | Yes | Yes | Yes | NR | MOD |
| Zhu, Yang, et al. (2025) [P57] | Indirect prompt injection | Tool outputs | Tool calls under original vs. masked re-execution | Yes | Yes | Yes | Yes | NR | Yes | NV | NR | LIM |
| Zhu, Zhang, et al. (2025) [P18] | High-risk or unethical tasks; adversarial attacks | Task prompts; tool use; agent collaboration | Prompts, agent messages and tool use | Yes | Yes | Yes | NV | NR | Yes | Yes | NR | MOD |

## A.6 Eligibility criteria

A study was included when it satisfied all six criteria.

- **I1 — Population.** The study addresses AI or LLM agents, tool-using agents or agentic systems. *Operational clarification, fixed before eligibility assessment:* LLM-integrated applications that ingest untrusted third-party content were counted as satisfying I1 when the attack or defense applies to the agent's input channel, because indirect injection against agents originates in that setting. Studies whose threat is specific to inter-agent communication in multi-agent systems were treated as outside the review population, which is single tool-using agents.
- **I2 — Problem.** The study addresses a security, safety, robustness, monitoring or misuse problem.
- **I3 — Contribution.** The study contains a substantive technical method, benchmark, empirical evaluation or analytical contribution. Position papers qualified only if they supplied a formal framework, a system design, or an empirical analysis of primary data. Argument-only position papers did not qualify.
- **I4 — Relevance.** The study directly informs at least one REM-relevant dimension: input or context security, runtime monitoring, behavioral analysis, action or tool monitoring, provenance, decision, mitigation, or financial execution security.
- **I5 — Extractability.** The study provides enough information to extract its relevant contribution.
- **I6 — Period.** The study was published between January 2019 and 25 September 2026, or it is a necessary **FOUNDATIONAL SOURCE**.

**Exclusion labels.** Records were excluded with a standard label:

- wrong population/system;
- wrong threat;
- wrong outcome;
- insufficient technical evidence;
- duplicate;
- outside scope;
- inaccessible full text or insufficient information;
- secondary study (survey, review, SoK or tutorial);
- metadata conflict;
- withdrawn.

**Secondary studies and methodological sources.** Secondary studies were not synthesized as primary evidence. Three of them, identified by the database search, are cited only as background: two definitional surveys and a finance SoK.

Methodological sources that do not concern agents also fail I1. These are the statistical, calibration, change-detection, decision-theoretic and anomaly-detection sources, and they were admitted under the second clause of I6 as **FOUNDATIONAL SOURCES**. Those published within the review period are labelled methodological sources. They support Section 2.7 and do not count as included studies.

The prior-art studies named in the protocol were given no special route. Each of AgentTrust, NEXUS, ProvenanceGuard, FinHarness, AgentDojo, AgentHarm, Progent, AgentSpec, ShieldAgent, Task Shield, MELON, CaMeL and LlamaFirewall passed through the same criteria.

## A.7 Exclusions at screening and at eligibility

**Exclusions at screening.** The 174 records excluded at screening break down as follows:

- 81 outside scope;
- 71 secondary studies;
- 7 multi-agent-channel studies;
- 7 wrong threat;
- 4 wrong population;
- 2 official reports;
- 1 wrong outcome;
- 1 duplicate.

**Exclusions at eligibility.** Five records passed screening but were excluded at eligibility:

- a retrieval-augmented question-answering system without tool actions (wrong population/system);
- a record whose index metadata attached AgentDojo's DOI and authors to an unrelated abstract (metadata conflict);
- an argument-only position paper (insufficient technical evidence);
- an observability taxonomy without a security evaluation (wrong outcome);
- a record without an abstract (insufficient information).

## A.8 Quality appraisal

Every included study was appraised against the protocol's ten-item checklist. The items ask whether the study reports:

- Q1 — its objective;
- Q2 — its threat model;
- Q3 — its method;
- Q4 — reproducibility;
- Q5 — its dataset or benchmark;
- Q6 — its metrics;
- Q7 — its comparators;
- Q8 — its limitations;
- Q9 — evidence for its quantitative claims;
- Q10 — peer-review status.

**Codes.** Each item is coded Yes, No, Not Verified or Not Applicable. Q10 also has a "preprint clearly labelled" code.

**Categories.** No numeric score is computed. A fixed, published rule assigns each study to a category of **record-visible evidence**:

- **HIGH EVIDENCE:** peer reviewed, with benchmark, figures and comparator all reported in the record;
- **MODERATE EVIDENCE:** quantitative results in a peer-reviewed or clearly labelled preprint record, or a peer-reviewed evaluation without verifiable figures;
- **LIMITED EVIDENCE:** everything else.

These categories describe **how much evidence the record makes visible**, which depends on how much information could be accessed. They are not a judgement of the study's intrinsic quality: a rigorous study with a terse abstract can fall into LIMITED EVIDENCE, and a full-text appraisal could move it.

**Override.** One override is applied and documented. FinHarness is set to LIMITED EVIDENCE because all of its figures were measured on FinVault, whose preprint was recorded on 25 September 2026 as withdrawn by its authors with a comment citing legal, intellectual-property and affiliation reasons rather than a scientific error. The withdrawal does not show that FinHarness's measurements are wrong; it means they cannot be confirmed against a publicly maintained benchmark. The override reflects confirmability, not invalidity (Section 2.9.2).

**Results.** Of the 71 included studies:

- 10 are HIGH EVIDENCE, 36 MODERATE EVIDENCE and 25 LIMITED EVIDENCE;
- 36 are peer reviewed and 35 are preprints or working papers;
- 62 are RECORD-VERIFIED and 9 PARTLY UNVERIFIED. RECORD-VERIFIED means that the bibliographic metadata and the cited contribution were checked against the study's index record (title, abstract, metadata); it does **not** mean that the full text was read. PARTLY UNVERIFIED means that at least one cited detail rests only on search-engine excerpts and is unverified.

**Levels of claim verification.** Every claim this chapter makes about a study is at one of four levels:

| Level | Meaning |
|---|---|
| **M** — metadata verified | Title, authors, venue and year checked against Crossref or the index record |
| **A** — abstract-supported | The claim is stated in the study's abstract as indexed |
| **F** — full-text verified | The claim was checked against the full text |
| **U** — unverified | The claim rests on search-engine excerpts or an earlier reading that could not be reproduced |

**No claim of the systematic review is at level F**, because no full text was retrieved for it. Six papers were read in full on 11 November 2026, outside the review; they are reported separately in Section 2.12.6. Claims at level U are marked "(unverified)" where they are used.

**What the categories measure.** Because full texts were unavailable, the categories measure **how much of each study's evidence could be verified from its record**, not the study's intrinsic quality (`CHAPTER2_QUALITY_APPRAISAL.md`). Items that depend on the full text (Q4 reproducibility, Q7 comparators, Q8 limitations) are most often Not Verified.

**How the categories are used.** They qualify how strongly a finding is worded in the synthesis. They were not used to exclude studies.

## A.9 Data extraction

A single reviewer extracted 21 fields per included study into `CHAPTER2_SYSTEMATIC_EVIDENCE_MATRIX.csv`:

- study, year and venue;
- agent type;
- threat and attack entry point;
- whether the study operates at runtime;
- context, behavioral, tool/action, multi-step and provenance evidence;
- decision mechanism and mitigation;
- benchmark;
- financial context;
- metrics;
- main result and limitation;
- evidence level.

**Coding values.** Each property is coded **Yes**, **No**, **Not Reported**, **Not Applicable** or **Not Verified**. "Yes" is never entered for a property that is merely absent from the record. Conversely, **Not Reported is not evidence of absence**: a property that the record does not mention may still be present in the system. Counts of "Not Reported" cells therefore describe the records, not the systems, and are never used in this chapter to argue that a capability is missing from the literature.

**Definitions and verification.** Financial context is coded "Yes" only where the study's setting is primarily financial. A general benchmark that contains one financial scenario is coded "No", with a note. Every included study also carries a verification label, RECORD-VERIFIED or PARTLY UNVERIFIED, following the thesis rule that search-engine text cannot settle a primary claim.

**Numbers.** Every number reported in this chapter is taken from the primary report of the study concerned, as recorded in the matrix.

## A.10 Evidence synthesis

**No meta-analysis.** Quantitative pooling was not possible. The included studies use different agents, attack sets, benchmarks, success definitions and metrics, and many report only author-selected configurations. A pooled estimate would have no interpretable common parameter.

**Structured synthesis.** The synthesis is therefore qualitative and structured. Evidence is organized into eleven themes:

1. threats;
2. entry points;
3. observation granularity;
4. runtime intervention;
5. behavioral and trajectory evidence;
6. provenance and goal–action consistency;
7. statistical and algorithmic methods;
8. decision and consequence handling;
9. mitigation;
10. financial-agent evidence;
11. evaluation quality.

**Five questions per theme.** For each theme the synthesis asks:

- what the literature establishes;
- what remains uncertain;
- what is under-evaluated;
- what differs across studies;
- what this implies for REM.

The syntheses are consolidated in Table A.9. Conflicting findings are presented side by side rather than resolved in favor of either side.

**How results are worded.** Author-reported figures are stated as such, with their setting, and are not compared across studies as if they were measured on a common scale. Claims that rest on a single study are worded as single-study findings.

## A.11 Threat classes and the included evidence

**Table A.6. Threat classes and the included evidence**

| Threat class | Entry point | Temporal scope | Why it is hard to detect | Included studies (evidence level) |
|---|---|---|---|---|
| Direct prompt injection | User channel | Single turn | Injected instructions resemble legitimate ones | Y. Liu et al. 2024 (MOD); Y. Liu et al. 2023 (MOD) |
| Indirect prompt injection | Observation channel (tool outputs, retrieved content, web pages) | Cross-step | Enters after input inspection | Greshake et al. 2023 (MOD); Zhan et al. 2024 (HIGH); H. Zhang et al. 2025 (HIGH); Z. Wang et al. 2025 (HIGH); Johnson et al. 2025 (LIM); Wei et al. 2026 (MOD) |
| Tool channel attacks (selection, metadata, servers, skills) | Tool library, tool metadata, skill files | Setup-time or cross-step | Poisoned artefacts are trusted as configuration | J. Shi et al. 2026 (LIM); C. Huang et al. 2026 (MOD); Hasan et al. 2026 (HIGH); X. Jia et al. 2026 (LIM) |
| Tool misuse / action manipulation | Tool arguments; action plans | Step or chain | Call is well formed; anomaly is relational | Fu et al. 2024 (MOD); Y. Zhang et al. 2024 (MOD); T. Liu et al. 2023 (MOD); Pedro et al. 2023 (LIM); Andriushchenko et al. 2025 (MOD) |
| Context and memory manipulation | Memory, retrieval corpus | Cross-session | Write and activation separated in time | Z. Chen et al. 2024 (MOD) |
| Goal drift / multi-step propagation | Trajectory | Trajectory | No single step need be anomalous | C. L. Wang et al. 2025 (MOD); W. Lin et al. 2026 (MOD); Z. Chen et al. 2026 (LIM) |
| Abnormal / repetitive execution | Trajectory | Trajectory | Anomaly lies in the pattern | B. Zhang et al. 2025 (MOD) |
| Misaligned (scheming) agent | Agent itself | Trajectory | Covert pursuit of another goal | Storf et al. 2026 (LIM) |
| Adaptive attacks | Any | Any | Designed against the defense | Zhan et al. 2025 (MOD); J. Shi et al. 2026 (LIM); Y. Zhang et al. 2024 (MOD) |

*Evidence levels: HIGH, MOD (moderate) and LIM (limited), as defined in Section 2.2.5.*

## A.12 Learned and LLM-based guardrails

A further family uses learned models or LLMs to judge actions or trajectories:

- **GuardAgent** generates guardrail code from safety requests (Xiang et al., 2025).
- **ShieldAgent** verifies trajectories against probabilistic rule circuits extracted from policy documents (Z. Chen, Kang, & Li, 2025).
- **AGrail** keeps adaptive safety checks in a lifelong memory (Luo et al., 2025).
- **TrustAgent** applies an agent constitution around planning (Hua et al., 2024).
- **Thought-Aligner** corrects unsafe intermediate thoughts. It raised behavioral safety from about 50% to about 90% on average across six LLMs (Jiang et al., 2025).
- **ToolSafe** trains a step-level guardrail that judges each tool invocation before execution from the interaction history. Its feedback-driven framework reduced harmful invocations by 65% on average and improved benign completion by about 10% under injection (Mou et al., 2026).
- **VIGIL** replaces isolation with verify-before-commit. It reduced attack success by over 22% relative to dynamic defenses and more than doubled utility under attack relative to static baselines on its SIREN benchmark (J. Lin et al., 2026; PARTLY UNVERIFIED).
- **DRIFT** combines a secure planner, a dynamic validator of plan deviations and privileges, and an injection isolator for the memory stream. It is evaluated on AgentDojo, ASB and AgentDyn (H. Li et al., 2025).
- **SafeScientist** monitors prompts, agent collaboration and tool use in scientific agents (Zhu, Zhang, et al., 2025).

**Limitations.** These systems cover a broad range of semantic violations without writing a policy for each. Their limitations also recur:

- LLM judgement adds latency and can vary between runs;
- accuracies are measured on the authors' own benchmarks;
- the outputs are verdicts, and the verified records do not report calibrated probabilities that could be combined with the consequence of an action. The one exception is NEXUS (Section 2.8.3).

## A.13 Step-level, sequence-level and accumulating monitors

Runtime monitors differ along two dimensions that are easily conflated: **decision granularity** (whether a decision is taken for each proposed step, for a plan, or for an episode) and **evidence scope** (whether that decision uses only the current step or also the history that led to it). A step-level decision can be history-aware: it can be taken for each proposed call while conditioning on the episode so far.

**Step-level monitors with current-step evidence** judge each proposed action against a policy or the current context. Examples are Progent and AgentSpec. They are fast and interpretable, but a monitor that uses no history cannot see an attack whose individual steps are each acceptable.

**Step-level monitors with history-aware evidence** still decide per proposed action, but their evidence includes earlier context. Task Shield, ProvenanceGuard and VIGIL check a proposed call against the user's goal or against evidence accumulated in the context; REM (Chapter 3) belongs to this group, because its per-step features include repeated calls, privilege escalation, transition deviation and argument provenance computed over the episode.

**Sequence-level monitors** judge an action against a model of the trajectory:

- MI9 enforces temporal behavioral patterns through finite-state conformance engines and detects goal-conditioned drift. It reports 99.81% detection across 1,033 *synthetic* scenarios (C. L. Wang et al., 2025; preprint; PARTLY UNVERIFIED).
- ProbGuard learns a discrete-time Markov chain over abstract states. It intervenes when the estimated probability of remaining safe falls below a threshold, with PAC-style guarantees on the learned model (H. Wang et al., 2025; preprint).
- DreamGuard maintains a recurrent latent state and fuses immediate-hazard and prefix-risk scores into PASS, HOLD or BLOCK, at about 25 ms per call (W. Lin et al., 2026; preprint).
- ToolSafe's guardrail reasons over the interaction history (Mou et al., 2026).
- Constitutional monitors judge whole trajectories for scheming (Storf et al., 2026).

**Accumulating monitors** keep an explicit running state across steps. PRISM accumulates session risk with time-to-live decay (F. Li, 2026). AgentTrust applies seven order-aware chain detectors (C. Yang, 2026). FinHarness integrates per-step risk in a cascade (H. Jia et al., 2026).

**A formal view.** A formal account of runtime governance frames policies as functions of the agent's identity, its *partial execution path*, the proposed next action and the organizational state, mapped to a probability of policy violation. It shows that system prompts and static access control are special cases, and it lists risk calibration as an open problem (Kaptein et al., 2026; preprint; LIMITED EVIDENCE). This formalization supports evaluating actions in the light of their path. It also shows that the idea of a path-conditioned violation probability is not new.

## A.14 Foundations: behavioral anomaly detection and its cautions

**Foundational work.** The idea of detecting compromise from behavior predates LLM agents. Forrest et al. (1996) built a profile of normal system-call sequences and flagged sequences absent from it. That is the closest classical analogue to monitoring an agent's tool-call sequence. Chandola et al. (2009, 2012) distinguished three kinds of anomaly and formalized anomaly detection over discrete sequences:

- *point* anomalies: in agents, a single out-of-policy call;
- *contextual* anomalies: a transfer that is normal in general but anomalous given its provenance;
- *collective* anomalies: goal drift and multi-step chains.

**Cautions.** The same literature carries cautions that transfer directly:

- attacks differ from typical learning tasks, with high error costs and a diverse normal class (Sommer & Paxson, 2010);
- security evaluations recur with sampling bias, base-rate neglect and lab-only testing (Arp et al., 2022).

For an agent monitor, these imply three requirements: a representative benign workload, interpretation of deviations in security terms, and models of "normal" learned from data resembling deployment. These are foundational and methodological sources, not included studies.

**Themes 5 and 6 (behavioral/trajectory evidence; provenance and goal–action consistency): synthesis.**

- **Established.** Many runtime systems observe trajectories: 17 of 42 code behavioral evidence and 21 code multi-step handling. Provenance and goal consistency are established signals against injected or misaligned actions.
- **Uncertain.** The measured contribution of each kind of evidence. One ablation found no effect of a session tracker, and another found a 26.4-point effect of cross-step labels. Both are single-study results on the authors' own benchmarks.
- **Under-evaluated.** The effect of trajectory and provenance evidence when it feeds a probability estimator rather than a rule or a judge. Evaluation in financial settings.
- **Differs across studies.** How provenance is obtained (analysis, construction or labels) and how sequences are modeled (automata, Markov chains, latent states or heuristics).
- **Implication for REM.** REM cannot claim trajectory monitoring or provenance analysis as new. Its evaluation must report the contribution of behavioral and provenance evidence, and must not assume it. It must also show that the benchmark contains the behavior the features are meant to detect.

## A.15 What attribution contributes to auditability

**Additive attribution.** Additive attribution explains a prediction as a sum of per-feature contributions. For a linear model under feature independence, the Shapley attribution of a feature is its coefficient times the feature's deviation from its mean (Lundberg & Lee, 2017). On the log-odds of a logistic model, that decomposition is exact and costs no more than the score itself. This makes it suitable for an audit record that shows which evidence contributed to a decision.

**Other audit traces.** It is not a distinguishing mechanism. Included systems already provide audit traces in other forms:

- rules and findings (NEXUS; AgentTrust);
- verifiable rule circuits (ShieldAgent);
- traceable evidence (ProvenanceGuard);
- tamper-evident or hash-chained logs (PRISM; the MCP policy-enforcement point; LATTICE's cryptographic audit trail).

In REM, attribution is **audit-only** and never enters the verdict.

**Table A.7. Established methods reviewed as the algorithmic basis for REM**

| Problem | Method (original source) | Why relevant | Main limitation | Use among included studies |
|---|---|---|---|---|
| Probabilistic risk scoring | Logistic regression (Cox, 1958); ridge penalty (le Cessie & van Houwelingen, 1992); naive Bayes as alternative (Ng & Jordan, 2002) | Fast, inspectable, probabilistic output | Linear log-odds; distribution shift | NEXUS (plan level) |
| Calibration | Platt (2000); temperature (Guo et al., 2017); isotonic (Zadrozny & Elkan, 2002); beta (Kull et al., 2017) | Makes scores usable with costs | Calibration does not imply good control | NEXUS (Platt, isotonic evaluated); C. Zhang et al. (analysis); DreamGuard (calibrated fusion) |
| Calibration measurement | ECE (Naeini et al., 2015; Guo et al., 2017) | Quantifies miscalibration | Bin-dependent; unstable with small sets | NEXUS; C. Zhang et al. |
| Sequential accumulation | CUSUM (Page, 1954; Basseville & Nikiforov, 1993); optimality (Lorden, 1971) | Statistically grounded accumulation | Assumptions not met by agent trajectories; evadable by pacing | Heuristic analogues only (PRISM; FinHarness). In REM: optional, observe-only |
| Response selection | Minimum expected cost (Elkan, 2001); reject option (Chow, 1970) | Uses consequences explicitly; human-review region | Costs uncertain; recoverability omitted | NEXUS objective (fixed costs, cascade); consequence pricing (H.-H. Chen) |
| Audit decomposition | Additive attribution (Lundberg & Lee, 2017) | Exact for linear scores; cheap | Not a novel explanation mechanism | Rule/evidence/audit traces in NEXUS, AgentTrust, ShieldAgent, ProvenanceGuard, PRISM, LATTICE |

**Theme 7 (statistical and algorithmic methods): synthesis.**

- **Established.** Each building block is established, and several are already applied in agent security.
- **Uncertain.** How these blocks perform in combination at the action boundary of an executing agent under indirect injection.
- **Under-evaluated.** Calibration of agent-safety probabilities. Only NEXUS reports calibration error for a deployed scorer, and C. Zhang et al. and LATTICE show that calibration or a threshold on confidence does not by itself secure good control.
- **Differs across studies.** Probabilities are produced by logistic scores, learned Markov chains, latent world models, or LLM judges.
- **Implication for REM.** REM's estimator, calibrator and decision rule are adopted, not contributed. Calibration must be reported separately from control. The comparison that isolates the effect of using consequences is against a consequence-independent rule that uses the *same* estimator.

## A.16 Decision mechanisms of the runtime systems closest to REM

**Table A.8. Decision mechanism, calibration, consequence and reported evaluation dimensions (runtime systems closest to REM)**

| System | Decision basis | Calibrated probability | Consequence used in decision | Human review / graduated response | Benign utility or false interventions reported | Latency reported | Financial focus | Evidence level |
|---|---|---|---|---|---|---|---|---|
| Progent | Privilege policy (solver-checked updates) | NA | NR | Approval for privilege expansion | Yes (functionality maintained) | NR | NR | MOD |
| AgentSpec | Deterministic rules | NA | NR | NV | NV | Yes (ms) | NR | MOD |
| RTBAS | Information-flow screeners | NR | NR | User confirmation when integrity/confidentiality not ensured | Yes (2% utility loss under attack) | NR | NR | MOD |
| MCP policy-enforcement point | Declarative rules over cross-step labels | NA | NR | NR | Yes (task-level FP 30.0%; 0/30 rule FPs) | Yes (sub-ms) | NR | HIGH |
| LATTICE | Policy-as-code; deterministic verdicts; confidence-based escalation | NR (confidence baseline analysed) | NR | Yes (human escalation) | Yes (operating point auto-allowed no action) | Yes (µs–ms) | NR | HIGH |
| Task Shield | LLM verification of task alignment | NR | NR | NR | Yes (69.79% utility) | NR | NR | HIGH |
| VIGIL | Intent-grounded verification before commit | NR | NR | NR | Yes (utility under attack) | NR | NR | HIGH (PV) |
| ToolSafe | Learned step-level guardrail with feedback | NR | NR | Feedback to agent | Yes (benign completion) | NR | NR | MOD |
| ProvenanceGuard | Evidence support for tool calls | NR | NR | Intervention | Yes (aligned-trace intervention rate; PV) | Yes (higher than baselines; PV) | NR | MOD (PV) |
| MI9 | Governance components; agency-risk index | NR | NR | Graduated containment | NV | Overhead noted (PV) | NV | MOD (PV) |
| ProbGuard | Probability of remaining safe (learned DTMC) vs threshold | NR (PAC-style bounds on learned model) | NR | NR | Yes (task completion) | NV | NR | MOD |
| DreamGuard | Calibrated fusion of hazard and prefix-risk scores | Partial ("calibrated fusion"; no calibration metric verified) | NR | HOLD | NV | Yes (~25 ms) | NR | MOD |
| SafeAgent | LLM operators; policy arbitration | NV | Yes (LLM consequence modelling; PV) | Yes | NV | NV | NR | LIM (PV) |
| AgentTrust | Rules and analysers; worst-case over normalized variants; LLM judge for ambiguity | NR | Partial (reversibility as a judge dimension; PV) | Yes (warn; review) | NR | Yes (~1.72 ms; PV) | NR | MOD (PV) |
| NEXUS | Rule-first cascade; calibrated logistic score with loss-optimal thresholds | Yes (Platt; ECE 0.085→0.013; PV) | Yes (plan annotations used by rules); intervention costs fixed (PV) | Yes (confirm; revise) | Yes (paired benign cases) | Yes (0.205 ms median) | NR | MOD (PV) |
| FinHarness | Monitors and LLM-judge cascade | NR | NR | Escalation to an advanced LLM judge | Yes (benign approval; benchmark withdrawn for non-scientific reasons) | NR (judge-call counts) | Yes | LIM |
| H.-H. Chen | Deterministic pricing against reserve capital | NA | Yes | NR | NR | NR | Partial | LIM |
| Jackson | Multi-dimensional risk score; enforcement state machine | NV | NV | Yes (escalate; sanitize) | NV | Qualitative only | NR | LIM (PV) |
| C. Zhang et al. (analysis) | Action-conditioned intervention value | Analysed (calibration did not reduce regret; PV) | Yes (recoverability) | NA | Regret reported | NR | NR | MOD (PV) |
| **REM (this thesis; design, Chapter 3)** | Calibrated per-step probability with consequence-tier losses in an expected-loss rule | Designed | Designed (declared tiers) | Designed (Escalate; Modify) | Exploratory evaluation (Chapter 4) | Measured (Chapter 4) | AgentDojo Banking | — |

*PV = figure or property unverified (level U: search-engine excerpt only).*

## A.17 Thematic synthesis of the included evidence

**Table A.9. Thematic synthesis of the included evidence**

| Theme | What the literature establishes | What is uncertain | What is under-evaluated | What differs across studies | Implication for REM |
|---|---|---|---|---|---|
| 1 Threats | Indirect injection is demonstrated, benchmarked and adaptive; defenses of the time were bypassed | Magnitude: 24% to 84.30% average ASR across benchmarks | Tool-metadata, tool-library, skill and MCP-server threats against runtime defenses | Threat actor and success criterion | Focus on indirect injection; state other classes as out of scope |
| 2 Entry points | The observation channel (tool outputs, retrieved content, tool metadata) is the decisive entry for tool-using agents | Relative danger of channels (skills > email/web in one study) | Defenses against setup-time channels | Which channel each benchmark exercises | Mediate at the action, where all channels converge |
| 3 Observation granularity | Input, call, plan, data-flow and trajectory units all implemented | Which unit gives the best security–utility trade-off | Head-to-head comparisons on a shared workload | Unit observed; question asked | Per-call observation with provenance context is a defensible, not novel, choice |
| 4 Runtime intervention | Interception at the tool boundary is widespread (41/42 runtime; 34/42 tool/action) and fast | Robustness to adaptive attacks | Evaluation on benchmarks the authors did not build | Permission vs. alignment vs. provenance vs. harm | REM cannot claim interception |
| 5 Behavioral / trajectory evidence | Many monitors model sequences (17/42 behavioral; 21/42 multi-step) | Contribution: one null ablation (session tracker) | Contribution inside a probabilistic estimator; financial settings | Automata, Markov chains, latent states, heuristics | Measure and report the contribution; do not assume it |
| 6 Provenance / goal–action consistency | Informative against injected or misaligned calls; cross-step labels had a 26.4-point effect in one study | Whether the effect generalizes beyond the authors' datasets | Provenance as input to a calibrated estimator; financial arguments | Obtained by analysis, construction or labels | Use as estimator input; test the contribution |
| 7 Statistical / algorithmic methods | Logistic scoring, calibration, expected cost, reject option and attribution are established; one agent-safety precedent (NEXUS) | Behaviour in combination at the action boundary | Calibration of agent-safety probabilities; calibration vs. control | How probabilities are produced | Adopted methods; report calibration separately from control |
| 8 Decision and consequence | Graduated responses and consequence information are common | How to combine an induction probability with a declared consequence | Intervention rates; per-response effectiveness | Fixed costs, pricing, rules, judge dimensions | Test the combination against a same-estimator consequence-independent baseline |
| 9 Mitigation | Block, modify, escalate, restrict, roll back and undo all implemented | Effectiveness of each response once chosen | Residual risk after modify-type responses | Meaning of "escalate" (human vs. stronger judge) and "modify" | Report residual attack success and escalation rate; SC-1 and SC-2 remain open |
| 10 Financial evidence | Financial actions lie within general benchmarks' attack surface; one financial harness exists | Defense performance on financial actions | Every financial-context study is LIMITED EVIDENCE; key figures were measured on a benchmark withdrawn for non-scientific reasons and cannot be confirmed | Chatbot firewall, position paper, actuarial framework, judge harness | Report results per financial action type and consequence tier |
| 11 Evaluation quality | Results are benchmark-specific; many benchmarks are built with the defense they evaluate | Multi-step content of benchmarks | Independent evaluation; decomposition into security, utility, intervention, calibration and latency | Metrics and baselines | Per-benchmark reporting with benign utility, intervention rates, calibration and latency |

## A.18 Assessment of candidate research gaps

**Table A.10. Evidence-based assessment of candidate research gaps**

| Candidate gap | Evidence for | Evidence against | Decision |
|---|---|---|---|
| **A. Integration.** Capabilities exist across separate approaches | Tables A.5–A.8: calibrated scoring (NEXUS), consequence pricing (H.-H. Chen), provenance (ProvenanceGuard; MCP policy-enforcement point), graduated verdicts (AgentTrust; LATTICE) are in different studies | NEXUS combines calibration and graduated responses (level A) and, per level-U evidence, costs, at the plan level | **Retained only as a weak, record-bounded observation.** A calibrated per-call probability combined with consequence-indexed losses at the action boundary was not reported in the examined records. Because the combination is specific and the review is record-level, its absence is not treated as evidence of originality |
| **B. Runtime action-boundary evaluation.** Limited evidence combining multiple signals at the point of action | — | AgentTrust, the MCP policy-enforcement point, ToolSafe, DRIFT, SafeAgent and FinHarness combine several signals at or near the tool call | **Not retained as stated.** Its defensible residue, combination into a calibrated probability, is part of Gap A |
| **C. Behavioral/provenance contribution.** Insufficient evidence separating the contribution of behavioral and provenance signals | Only three component-level tests found; they conflict (null session-tracker ablation vs. a 26.4-point cross-step-label effect); none inside a probabilistic estimator; none financial | The MCP policy-enforcement point does separate the contribution of cross-step labels in a rule-based enforcer (HIGH EVIDENCE) | **Retained, narrowed.** Limited and conflicting evidence on the contribution of behavioral and provenance evidence *as inputs to a calibrated estimator* for financial actions under indirect injection |
| **D. Financial-agent evidence.** Limited verified evidence in executable financial settings | Four financial-context studies, all LIMITED EVIDENCE; the only quantitative runtime results cannot be confirmed against a maintained benchmark; general benchmarks with financial suites report no finance-specific analysis in the verified record | FinHarness shows the problem is recognized | **Retained** |
| **E. Evaluation decomposition.** Insufficient evaluation separating security, benign utility, calibration or decision quality, intervention behavior and latency | Calibration reported for one deployed scorer (NEXUS); intervention rates by few studies; no study compares a consequence-aware decision with a consequence-independent baseline that shares its estimator | Several studies report more than attack success (MCP policy-enforcement point; LATTICE; NEXUS; ToolSafe) | **Retained, narrowed.** The missing element is the same-estimator comparison, with calibration reported separately from control and intervention rates reported |

## A.19 AI agents and emerging security risks

### A.19.1 From language models to agents

In the survey literature, an LLM-based autonomous agent is a system in which a language model acts as the controller for perception, reasoning, planning and action in pursuit of a task, supported by memory and tool-use modules (L. Wang et al., 2024; background source). Two capability developments made this architecture practical:

- **ReAct** interleaves reasoning with action. The model generates a thought, selects an action, receives the environment's observation, and conditions its next step on that observation (Yao et al., 2023).
- **Toolformer** showed that a language model can learn which application programming interfaces to call, when to call them, and with what arguments (Schick et al., 2023).

Both are capability papers. They fail criterion I2 and are cited only as background. Together they describe the execution pattern that most agent frameworks still follow: a loop of reasoning, tool invocation and observation, which continues until the model judges the task complete.

### A.19.2 Why agent architecture changes the security problem

The loop that makes agents useful also creates their attack surface. Three structural properties distinguish agent security from the security of a stand-alone model:

- **Several input channels of different trustworthiness.** The system prompt, the user's request, tool outputs, retrieved documents and stored memory all enter the same context window, and the model interprets all of them.
- **Statefulness across a trajectory.** Content that enters at one step can influence an action several steps later. The unit of analysis is therefore a trajectory, not an input–output pair.
- **Outputs with external effects.** An agent's outputs include tool calls. A successful manipulation does not stay in the text domain; it becomes a state change in an external system.

A component view of agent threats organizes the same observation around the model "brain", memory, tools and environment interaction (Yu et al., 2025; background source).

Two included benchmark studies show that these properties matter empirically:

- **ClawSafety** ran 2,520 sandboxed trials of personal agents with elevated local privileges. Attack success varied from 40% to 75% across five backbone models, and varied sharply with the channel through which the injection arrived. Cross-scaffold experiments showed that safety depended on the whole deployment stack, not on the backbone model alone (Wei et al., 2026; preprint).
- **ToolEmu** showed that agent risk does not require an attacker. In an LM-emulated sandbox with 36 toolkits and 144 test cases, even the safest agent tested failed in 23.9% of cases. Human evaluators judged 68.8% of the failures identified to be valid real-world failures (Ruan et al., 2024).

### A.19.3 Implication

The reviewed studies locate agent risk at the interaction between the model, its heterogeneous input channels, its accumulated state and its tools, and ClawSafety adds the agent framework itself. A defense that inspects only the user's input, or only the final text, does not observe the point at which the agent's decision becomes an external effect. The remainder of the chapter therefore attends to **where** defenses intervene and **what** they observe.

## A.20 Tool misuse, action manipulation and new tool channels

Tool misuse is the use of a legitimate capability against the user's intent. Action manipulation is its adversarially induced form: a well-formed call to a permitted tool, with attacker-chosen arguments or timing. The included studies show that the tool interface is now an attack surface in its own right:

- **Tool selection.** ToolHijacker injects a malicious tool document into the tool library so that the agent selects the attacker's tool. Six prevention-based and detection-based defenses proved insufficient against it (J. Shi et al., 2026).
- **Tool metadata.** A STRIDE/DREAD threat model of the Model Context Protocol (MCP) identified *tool poisoning*, meaning instructions embedded in tool metadata, as the most prevalent client-side vulnerability. Most of the seven MCP clients tested showed weaknesses in static validation and parameter visibility (C. Huang et al., 2026).
- **Tool servers.** A study of 1,899 open-source MCP servers found MCP-specific tool poisoning in 5.5% of servers and general vulnerabilities in 7.2% (Hasan et al., 2026).
- **Tool arguments and plans.** Imprompter optimizes obfuscated prompts that cause improper tool use; its information-exfiltration attack succeeded end to end in nearly 80% of trials against a production agent (Fu et al., 2024; preprint). AI² builds semantically harmless inputs that hijack an application's action plan. It reports an average success rate of 84.30% and bypasses common safety filters in 92.7% of cases (Y. Zhang et al., 2024; preprint).
- **Framework tools.** In LLM-integrated frameworks, prompt injection reaches code-execution and database tools. LLMSmith found 20 vulnerabilities in 11 frameworks, 19 of them remote code execution, of which 17 were confirmed and 11 received CVEs (T. Liu et al., 2023; preprint). Prompt-to-SQL injection was shown to be pervasive across seven LLMs in LangChain applications (Pedro et al., 2023; preprint).
- **Skills.** Reusable agent "skills" create a supply-chain channel. SkillJect automatically poisons skill instructions and helper scripts and outperforms manual skill-injection attacks (X. Jia et al., 2026; preprint; LIMITED EVIDENCE).

**Malicious users.** Harmful behavior can also be requested directly. AgentHarm contains 110 malicious agentic tasks (440 with augmentations) in 11 harm categories (Andriushchenko et al., 2025). Its threat model, a malicious *user*, contrasts with REM's primary threat model, in which the adversary sits in the data read by a benign user's agent.

## A.21 Context and memory manipulation

Where an agent retrieves from memory or a knowledge base, an adversary can plant content that is acted on later. AgentPoison reported an attack success rate of at least 80%, with benign impact of at most 1%, at a poison rate below 0.1% (Z. Chen et al., 2024). Memory poisoning separates the write from the activation in time. To an observer without provenance information, the eventual retrieval therefore looks legitimate.

## A.22 Multi-step propagation, goal drift and abnormal execution

Some compromises contain no single anomalous step. Several runtime systems target this pattern:

- goal-conditioned drift detection (C. L. Wang et al., 2025);
- cross-turn drift in a financial query monitor (H. Jia et al., 2026);
- hazardous drift through individually benign actions (W. Lin et al., 2026);
- task-level transactions that expose cross-step violations (Z. Chen et al., 2026).

**Abnormal execution.** Abnormal execution can itself be the attack. Malfunction amplification misleads agents into repetitive or irrelevant actions. It induced failure rates above 80% in several scenarios, and its authors found it harder to detect than overtly harmful attacks (B. Zhang et al., 2025). In anomaly-detection terms, a sequence of individually normal events whose *combination* is anomalous is a *collective* anomaly (Chandola et al., 2009; foundational source).

**Misaligned agents.** A distinct threat is posed by an agent that is itself misaligned. Monitors for covert "scheming" operate on observable trajectories. Monitors trained on synthetic data generalized to more realistic environments, but their performance saturated quickly (Storf et al., 2026; preprint).

## A.23 Input-, context- and model-level protection

**Input detectors.** Detectors that act on text report strong in-distribution results:

- InstructDetector uses a model's hidden states and gradients to detect embedded instructions. It reports 99.60% in-domain and 96.90% out-of-domain accuracy, and reduces attack success to 0.03% on BIPIA (Wen et al., 2025).
- PromptShield curates a benchmark for deployable detectors, and its fine-tuned detector improves performance in the low-false-positive regime (Jacob et al., 2025).
- Spotlighting transforms untrusted input so that the model receives a continuous provenance signal, reducing attack success from above 50% to below 2% with GPT-family models (Hines et al., 2024).

**Model-level protection.** StruQ trains the model to follow instructions only in the prompt channel (S. Chen et al., 2025). This addresses the root cause identified by Greshake et al. (2023), but it requires training and access to the model. That is a significant constraint for a financial institution that deploys a third-party model.

**Shared limitations.** These approaches share two limitations for tool-using agents:

- they act on text, not on actions, so an input detector does not observe what the agent then does;
- ToolHijacker defeated six such defenses (J. Shi et al., 2026), and AI² bypassed common safety filters in 92.7% of cases (Y. Zhang et al., 2024).

## A.24 System-level and information-flow defenses

A second family changes the system so that untrusted data cannot steer control flow:

- **f-secure LLM systems.** A security monitor filters untrusted input out of the planning process, and formal models state the security guarantee (F. Wu et al., 2024; preprint).
- **RTBAS.** Information-flow control is adapted to tool-based agents. Tool calls whose integrity and confidentiality can be established are executed automatically, and the user is asked to confirm the rest. On AgentDojo it prevented all targeted attacks with a 2% utility loss under attack (Zhong et al., 2025; preprint).
- **ACE.** Planning is decoupled: an abstract plan is built from trusted information only, its information-flow constraints are checked statically, and data and capability barriers are enforced during execution. It reports security against InjecAgent and ASB attacks, and it demonstrates new attacks against IsolateGPT (E. Li et al., 2026).
- **IsolateGPT.** Third-party apps run in isolation, with overhead under 30% for three-quarters of tested queries (Y. Wu et al., 2025).
- **CaMeL.** Control and data flow are extracted from the trusted query and capability policies are enforced at each tool call. CaMeL solved 77% of AgentDojo tasks with provable security, against 84% for the undefended agent (Debenedetti et al., 2025, v2; an earlier version reported 67%).

**Conflicting evidence.** The IsolateGPT–ACE pair is a direct conflict within this family. One peer-reviewed study reports that isolation protects against the attacks it tested. A later peer-reviewed study constructs attacks that defeat it. Architectural guarantees hold only for the threat models their authors formalized.

## A.25 Why logistic regression

Logistic regression models the probability of a binary outcome as a logistic function of a linear score (Cox, 1958):

$$\Pr(y = 1 \mid x) = \frac{1}{1 + \exp\!\big(-(\beta_0 + \beta^\top x)\big)} \qquad (2.1)$$

**Why it suits a runtime layer.**

- Evaluation costs one inner product.
- Coefficients can be inspected.
- The output is intended as a probability, not as an arbitrary score.

**Limitations.**

- Interactions must be engineered into the features.
- A model fitted on one attack distribution can be miscalibrated on another.
- With scarce adversarial examples and binary indicators, the unpenalized estimate may not be finite. A ridge penalty addresses this (le Cessie & van Houwelingen, 1992).
- Naive Bayes is the generative counterpart with the same linear form. It may reach its (higher) asymptotic error with fewer examples (Ng & Jordan, 2002). It is an established alternative estimator and is not part of REM.

**Use in agent security.** Among the included studies, only NEXUS uses a logistic risk score for agent safety (Hossain et al., 2026). The choice of estimator family therefore has one direct precedent in agent security, and that precedent operates at the plan level.

## A.26 Why sequential evidence matters

When evidence arrives step by step, a monitor must decide when the accumulated evidence justifies action.

**CUSUM.** Classical sequential analysis gives a statistically grounded answer. The cumulative-sum procedure (Page, 1954) accumulates log-likelihood ratios of post-change against pre-change behavior and raises an alarm when the accumulated statistic crosses a threshold (Basseville & Nikiforov, 1993). Under the classical change-point model, with independent observations before and after the change, it has an asymptotic optimality property for detection delay at a given false-alarm constraint (Lorden, 1971).

**Limits for agents.** These assumptions are only approximately satisfied by tool-call sequences, and an adversary can pace an attack to stay below the threshold. The procedure also detects a *change*, whereas an agent episode may be adversarial from its first injected observation.

**Heuristic alternatives.** Among the included studies, sequential accumulation is heuristic: PRISM's session risk with time-to-live decay (F. Li, 2026) and FinHarness's cascade (H. Jia et al., 2026).

**Role in REM.** CUSUM is **not part of REM's verdict path**. Chapter 3 uses it only as an optional, offline, observe-only analysis of logged indicators that never influences a verdict.

## A.27 Currency update of 30 October 2026 (outside the PRISMA flow)

The registered search ran on 25 September 2026. On 30 October 2026 the eleven queries of Table A.1 were re-run in the same index (OpenAlex, through the same literature-search tool), restricted to publication year 2026, to find work that could change the gap assessment. **This update is not part of the PRISMA flow, and no count in Table 2.1 or Figure 2.1 changes:**

- the index returns the publication year but not the date, so records published after 25 September could not be separated reliably from earlier 2026 records;
- of the 215 unique records returned, 200 were not in the stored output of the registered search; they were title-screened by one reviewer for direct relevance to REM's decision mechanism or evaluation design, and were not assessed against criteria I1–I6;
- no record was added to the 71 included studies.

The raw output is stored with the thesis verification records (`update_search_2026-10-30.json`). Five records bear directly on REM's positioning. Each is described only as far as its index record states (level A); no full text was read.

| Record | Type | What the record states | Bearing on REM |
|---|---|---|---|
| Kekatos et al. (2026) | Peer-reviewed workshop paper (ACM, Crossref-registered) | Replays the recorded trajectories distributed with AgentDojo, STAC and R-Judge through a temporal-logic monitor, offline and without running an agent. Five generic obligations flag 70.1% of successful AgentDojo attacks and fire on 29.3% of benign runs. A planted line defeats a naive provenance check on 94–99% of the runs it would otherwise flag | Offline evaluation on AgentDojo's recorded traces has a published precedent, so it is not a methodological contribution of this thesis. Provenance evidence is itself attackable |
| Z. Liu (2026) | Preprint | Replays the ground-truth tool calls of AgentDojo and tau-bench without an LLM and evaluates fifteen prompt-injection detectors, including Prompt Guard 2. Rankings transfer poorly: the best detector on BIPIA catches 2% of AgentDojo injections at a 1% false-positive rate | The choice of the injection classifier x^ctx^~1~ (pending) should be evaluated on the agent's own tool outputs at a low false-positive rate |
| Ray (2026) | Preprint | Once blocking changes future proposals, static scores and ungated trajectories need not identify the closed-loop frontier; benign calibration alone does not transfer | Theoretical support for the limit of REM's replay analysis: replay of recorded trajectories cannot establish closed-loop enforcement |
| Yan et al. (2026) | Preprint | A controller that acts after the agent proposes an action and before it executes; it encodes trusted and external observations in provenance-typed memory and commits the action, proposed or alternative, with the highest calibrated value learned from outcomes | The closest record found to REM's combination of provenance evidence and a calibrated decision at the action boundary. It differs, by its abstract, in choosing between actions by learned value rather than among four verdicts by declared, tier-indexed losses. Prior-art risk to Gap A |
| Xin (2026) | Journal article | A pre-execution router with temperature-scaled three-class probabilities (execute, confirm, block), a fixed rule floor and confidence-triggered confirmation, evaluated on mobile-agent tasks that include financial applications | Calibrated multi-way routing with a confirmation verdict before execution has a further precedent. REM differs in deriving its thresholds from declared losses per consequence tier |

The other records of the update concern, among other topics, enforcement at the execution boundary, banking-agent benchmarks and step-labeled injection trajectories. They were not assessed and should be screened in the full update recommended in Section 2.12.4.

**Effect on the gap.** At abstract level, none of the five records reports the combination and evaluation stated in Section 2.12.2, but Yan et al. (2026) and Xin (2026) narrow the distance to it, and Kekatos et al. (2026) removes any claim of methodological novelty for offline evaluation on recorded AgentDojo traces. Because only records were examined, this conclusion has the same limits as the main review.

## A.28 Supplementary literature update of 2 November 2026: Kanaker et al. (2026) (outside the PRISMA flow)

**Status of this addition.** Kanaker et al. (2026), *Securing Tool-Using AI Agents Against Injection and Authority Misuse* (*Computation*, 14(5), Article 98), is added on 2 November 2026 as a dated supplementary literature update. The record was returned by query Q7 of the currency update of 30 October 2026 (OpenAlex W7160053090, stored in `update_search_2026-10-30.json`) but was not among the five records selected at title screening in Section 2.12.5. It was not part of the registered search of 25 September 2026. **No count in Table 2.1 or Figure 2.1 changes, it is not added to the 71 included studies, and no screening record is created retrospectively.**

**Evidence level.** The bibliographic metadata were checked against the Crossref record of the DOI (10.3390/computation14050098): six authors in the order H. Kanaker, H. Fakhouri, N. Abdel Karim, M. Abuhamdeh, N. H. A. Ismail and S. Fakhouri; *Computation*, volume 14, issue 5, article 98; 2026. The abstract was read in the OpenAlex record. The full text could not be retrieved in this revision, because the publisher and DOI hosts were refused by the network policy. Every statement below is therefore at **level A**: it reports what the abstract states, not what the paper's methods or results sections contain. Parameter values, the number of simulation runs, uncertainty estimates and the exact definitions of the metrics were not read.

**What the study does (level A).** The study argues that large-scale testing of deployed agents is difficult, vendor-specific and ethically sensitive, and proposes a transparent, theoretical simulation framework for user-facing risk in tool-using agents. Its stated methodological contribution is a formal threat model that **separates compromise, harm and severity**, together with a Monte Carlo pipeline that maps architectural choices (permissions, retrieval, memory exposure and approvals) and defensive controls to comparable outcome metrics. It instantiates the framework for six threat scenarios and nine defense configurations, and reports attack success rate, benign task success, latency overhead and severity-weighted harm. Its abstract reports four findings:

- least-privilege tool design is the strongest single broad control;
- human-in-the-loop approvals sharply reduce high-impact actions and exports, but degrade under user error and habituation;
- retrieval allowlisting nearly eliminates indirect injection while leaving other channels largely unaffected;
- rate limiting reduces tail severity more than attack success rate.

**Critical assessment.**

- *Strengths visible in the record.* The threat model makes the distinction between whether an agent is compromised and how much harm follows explicit. The study reports more than attack success, including benign task success, latency and a severity-weighted outcome, and it compares architectural controls side by side. Its assumptions are declared rather than hidden.
- *Limits stated by the authors.* The results come from an assumption-explicit simulator, not from field measurements, and the authors present them as comparative design guidance rather than incident-rate estimates for any deployed product. They do not measure how a particular agent or language model behaves.
- *Limits of this review.* Whether the simulated risks are calibrated to observed agent behavior, how sensitive the rankings are to the simulator's parameters, and how severity is weighted could not be assessed without the full text.
- *Consistency with other evidence in this chapter.* The approval finding agrees with the approval-fatigue trade-off reported by P. Wang et al. (2026) (Section 2.8.1). The allowlisting finding concerns one injection channel, whereas the provenance-based defenses of Section 2.5.2 examine the content that actually reaches a proposed call. The rate-limiting finding illustrates why attack success rate alone can miss differences in the severity of outcomes.

**Bearing on the gap assessment (Table A.10).** The study adds to the "evidence against" column of Gap E: another study reports security, benign success, latency and a severity-weighted outcome together, although in simulation. It does not, by its abstract, compare a consequence-aware decision with a consequence-independent baseline that shares its estimator, so the narrowed residue of Gap E is unchanged. For Gap D, the study evaluates transaction-capable tools in a simulator rather than in an open, executable benchmark, so the retained statement is not contradicted. For Gap A, the abstract describes no calibrated per-call probability and no selection among verdicts by expected loss. These conclusions have the same record-level limits as the rest of the review.

**Table A.11. Kanaker et al. (2026) and REM compared (Kanaker et al.: level A, abstract and metadata only; REM: Chapters 3–4)**

| Dimension | Kanaker et al. (2026) | REM (this thesis) |
|---|---|---|
| Research question | How architectural choices and defensive controls change user-facing risk in tool-using agents, evaluated without testing deployed products | Whether consequence-tiered expected-loss verdicts at the tool-execution boundary change intervention, attack success and utility relative to a consequence-independent threshold with the same estimator (Section 1.7; [PD]) |
| Method | Formal threat model separating compromise, harm and severity; Monte Carlo evaluation pipeline over architectural choices and defenses | Provenance, behavioral and action evidence; ridge logistic regression; logistic calibration on the logit; consequence tiers; expected-loss verdict among Allow, Modify, Escalate and Block; deterministic mitigation; audit record |
| Data and evidence | Assumption-explicit simulation; six threat scenarios; nine defense configurations | Recorded AgentDojo banking traces of 21 language-model agents; held-out predictions, observe-only decisions and replay under a no-adaptation assumption; no live runs (Chapter 4) |
| Treatment of harm and severity | Severity separated from compromise in the threat model; severity-weighted harm reported as an outcome | Consequence tier k~t~ separated from the probability p~t~; severity enters the decision through tier-indexed declared losses (Eqs. 3.5–3.9); realized loss reported (Eq. 3.22) |
| Defensive mechanisms | Least-privilege tool design, human-in-the-loop approvals, retrieval allowlisting, rate limiting (abstract); the full set of nine configurations was not read | Per-call verdicts with step-level withholding of the current call, an episode-level restriction variant, and escalation evaluated under an idealized-reviewer and a no-reviewer bound |
| Reported outcomes | Attack success rate, benign task success, latency overhead, severity-weighted harm | Discrimination and calibration, intervention rates, attack success rate, benign utility, utility under attack, processing time, realized loss |
| Limitations | Simulator rather than field measurement; results are comparative design guidance, not incident-rate estimates (stated by the authors) | Exploratory pilot; recorded traces and replay only; unaudited proxy labels; declared, unapproved costs; one benchmark (Chapter 4, Section 4.19) |

**What is and is not taken from this study.** The study is cited where it is consistent with existing positions of this thesis: the separation of compromise from severity (Chapter 3, Section 3.7.3) and the optimism of a perfect-reviewer assumption (Chapter 3, Section 3.7.5). REM's design was fixed before this record was examined, and no REM mechanism, parameter or experiment is derived from it. Its simulation results are not used as evidence for REM's effectiveness, and REM's results are not used to assess its findings.

# Appendix B: System Implementation: Details

This appendix gives the implementation details that Chapter 3, Section 3.14, summarizes. It is reproduced from the thesis draft of 3 to 5 November 2026 without change of content. Test counts in this appendix are those of 1 November 2026 (205 tests); the count on 11 November 2026, after the integration, deployment-simulation and study tests were added, is 241 passed, 3 skipped and 1 expected failure.

## B.1 Implementation of the REM framework

This section reports how the methodology of Chapter 3 is implemented in software: the environment, the organisation of the code and its execution paths, the implementation of each layer, the verification of the software, the correspondence between equations, code, tests and results, and the measurement of processing time. It was Chapter 4 of the six-chapter draft (R5); its content is preserved and renumbered.

### B.1.1 Purpose and Scope

Chapter 3 specified REM as a five-layer runtime framework that selects one of four verdicts (Allow, Modify, Escalate, Block) for each tool call proposed by an LLM agent. The verdict minimizes expected loss under a calibrated probability of adversarial inducement and a declared consequence tier, and every verdict is recorded for audit.

This section reports how that specification was realized in software, how the software reaches the benchmark, and how it was verified. It distinguishes three kinds of verification throughout:
- **Unit verification:** a function computes what its equation states, on constructed inputs.
- **Integration verification:** the components operate together inside the benchmark's execution loop, and the benchmark's own checks behave as expected.
- **Security effectiveness:** whether REM reduces attack success at acceptable cost.

**This section establishes only the first two.** Chapter 4 reports the evidence on the third, and its limits.

Three rules governed the implementation:
1. **Fail closed.** A design value that has not been declared stops the software (`DesignNotSpecifiedError`) instead of being replaced by a default.
2. **No silent resolution.** Where the methodology of Chapter 3 and the design decisions of Stage 2 disagree, both alternatives are implemented and selected explicitly. The correspondence is recorded in Appendix B.1.12.
3. **Separation of decision and audit.** Attribution is computed after the verdict and cannot reach the decision function; this is enforced by the function's signature and checked by a test.

### B.1.2 Software Environment

**Table B.1. Software and hardware environment of the reported runs**

| Item | Value |
|---|---|
| Language | Python 3.11.17 |
| Numerical library | NumPy 2.4.6 |
| Benchmark | AgentDojo 0.1.35 (PyPI), banking suite; suite version v1 for execution |
| Recorded traces | AgentDojo repository `runs/`, commit `089ed468cf3ed0322acc66b0211f26d9d90dbf60` |
| Test framework | pytest 9.1.1 |
| Hardware | Linux container, 4 vCPU (Intel Xeon @ 2.80 GHz), 15 GB RAM |
| Re-execution in a fresh environment (R3) | 30 Oct 2026, merged repository state, Python 3.11.17, NumPy 2.4.6, AgentDojo 0.1.35, Intel Xeon @ 2.10 GHz, 4 vCPU; see Appendix B.1.11 |
| Re-execution with the complete-call timer (R4) | 1 Nov 2026, branch `claude/rem-r4-corrections-3ktvze`, Python 3.11.17, NumPy 2.4.6, AgentDojo 0.1.35, Intel Xeon @ 2.80 GHz, 4 vCPU; results in `results/pilot_R4/`; see Appendix B.1.11 |
| Code version of the reported results | git commit `84a8c21` (revision R2). The first run (commit `aa66f22`) gave identical analytical results; see Appendix B.1.11 |

No machine-learning framework is used. The estimator, the calibrators and every metric are implemented directly in NumPy, so that each operation can be traced to its equation (Table B.6).

### B.1.3 Code Organization and Execution Paths

**Table B.2. Code organization**

| Package | Content |
|---|---|
| `rem/core/` | Frozen pipeline skeleton (`RemPipeline`), interfaces, step-level mitigation engine, append-only audit log, result types |
| `rem/algorithms/detection/` | Ridge logistic regression (Eqs. 3.1–3.2); instruction-pattern indicator x^ctx₂ |
| `rem/algorithms/calibration/` | Platt calibration on the logit: smoothed-target fit (`PlattLogitCalibrator`) and label-NLL fit (`LabelNLLLogitCalibrator`, Eq. 3.4) |
| `rem/algorithms/context/` | Provenance labels, hygiene, entity extraction |
| `rem/algorithms/behavior/` | Evidence features (Tables 3.6–3.7); Bernoulli CUSUM (observe-only) |
| `rem/algorithms/decision/` | Expected-loss engine; consequence tiers; loss structure and dominance check; predicates and feasible set |
| `rem/algorithms/a3.py`, `a1.py`, `a2.py` | REM verdict rule; baseline B1; observe-only CUSUM analysis |
| `rem/evaluation/` | Discrimination and calibration metrics; grouped bootstrap; nested grouped cross-fitting |
| `rem/integration/` | AgentDojo trace loader, labeller, step builder, replay harness with the REM guard |
| `experiments/pilot/` | Experiment scripts and the reproduction script `run_all.sh` |

The names A1, A2 and A3 come from the project brief and do not denote three methodologies:
- **A3** is the REM verdict rule;
- **A1** is the consequence-independent baseline B1 (Section 3.7.7);
- **A2** is the optional observe-only CUSUM (Appendix C.3).

**Layer of the estimator.** In this thesis the ridge estimator and the calibration map belong to the Decision Engine (Layer 4), as in the methodology of Chapter 3 and Figure 3.1. The comments and layer constants of the frozen pipeline's code label the estimator as part of Detection (Layer 2). The label does not affect any computation, and the frozen code was not edited to change it.

**Two execution paths exist, and the experiments use only one of them.**

1. **The frozen pipeline** (`rem/core/pipeline.py`, `RemPipeline.evaluate_step`) chains injected components through the five layers. It is exercised by unit and contract tests. It is **not** the path that produced any result in Chapter 4.
2. **The evaluation path** (`rem/integration/agentdojo_replay.py`, `RemGuard.evaluate`, together with `rem/algorithms/a3.py`, `A3Policy.decide`) is the path used in every experiment. It calls the frozen components:
   - the fitted ridge coefficients;
   - the calibration map;
   - `ExpectedLossDecisionEngine.conditional_risk` for Eq. 3.6;
   - `LinearShapleyAttributor` for Eq. 3.11.

   It adds the Chapter 3 components the frozen pipeline lacks: features, tiers, predicates, feasible set and both mitigation semantics. Mitigation is implemented in `RemGuard._mitigate`, not in the frozen `DeterministicMitigationEngine`.

**Table B.3. Entry points and call paths of each experiment**

| Experiment (Chapter 4) | Entry point | Call path |
|---|---|---|
| Dataset | `experiments/pilot/build_dataset.py` | `load_episode` → `build_steps` → `EpisodeTracker.features` → `ReferenceLabeler.label` → `ConsequenceTierMap.tier` |
| Pilot E0 | `e0_pilot.py` | `nested_crossfit` on each fold's fitting portion → `roc_auc` |
| E1 discrimination and calibration; ablation refits; grouping sensitivity | `run_main.py crossfit` | `Designer` (fold-specific x^beh₄) → `nested_crossfit` → `RidgeLogisticRegression.fit` → calibrator `fit` → `A1Thresholds.fit` |
| r~mod~ and replay validity | `run_main.py rmod` | `replay_episode` → `GuardedToolsExecutor.query` → `RemGuard.evaluate` (oracle Modify) |
| E2, E5 and E6 observe-only | `run_main.py observe` | `A3Policy.decide` / `A1Policy.decide` on held-out recorded steps |
| E4, E5 replay | `run_main.py replay` | `replay_episode` → `RemGuard.evaluate` → `A3Policy.decide` → `RemGuard._mitigate` |
| E3 CUSUM | `run_main.py a2` | `fit_a2` → `evaluate_episode` |
| Cross-template; recorded defenses | `run_main.py xt` | as E1 scoring, and as E4 replay |
| Breakdowns, replay failures, label-audit package | `r2_analyses.py` | stored state from the stages above |
| All of the above | `run_all.sh` | in order; writes `results/pilot_R2/` when `PILOT_RESULTS_DIR` is set |

### B.1.4 Layer 1 — Input and Context

`rem/algorithms/context/provenance.py` implements the provenance rule of Section 3.4.2:
- every segment is labelled trusted (system), semi-trusted (user) or untrusted (tool output);
- derived content takes the least-trusted label of its inputs;
- model-generated content has no channel label, so asking for one raises an error rather than guessing.

**Hygiene.** Zero-width, bidirectional and other Unicode format characters are removed from REM's copy of untrusted text (`strip_invisible`). The text the agent receives is not altered.

**Entity extraction** is partly implemented:

| Entity (Section 3.4.3) | Status |
|---|---|
| Account identifiers | Implemented (IBAN pattern) |
| Monetary amounts | Implemented (numeric tokens) |
| User-profile values | Implemented for the values returned by the profile read |
| Tool names mentioned in text | Implemented, through the instruction-pattern indicator |
| Credential values | Not extracted as entities; a password argument is still traced to its source through argument provenance |
| Phone numbers and other profile identifiers | Not implemented separately |

A declared matching rule (`value_occurs_in`) links an argument value to the texts that contain it:
- numbers match numerically;
- strings match as case-insensitive substrings;
- strings shorter than three characters never match.

### B.1.5 Layer 2 — Detection

**x^ctx₂ (instruction-pattern indicator)** is implemented by `InstructionPatternDetector`. It fires if a declared regular expression, or the name of a tool, occurs in new untrusted segments. The pattern set is declared in the pilot configuration, and the detector refuses to run without one. The configuration discloses that the author of the patterns knew the benchmark's templates.

**x^ctx₁ (pre-trained injection classifier) is not implemented.** The classifier choice is pending, and the candidate model's host was unreachable from the execution environment. The feature is absent from x~t~; it is not replaced by a substitute. The context evidence tested in Chapter 4 is therefore the instruction-pattern indicator only.

### B.1.6 Layer 3 — Behavioral and Action Evidence

`rem/algorithms/behavior/evidence.py` implements x^beh₁–x^beh₄ and x^act₁–x^act₃ (Table 3.7). An `EpisodeTracker` holds the episode history; it is reset at each episode start and never changes REM's parameters. Where the methodology of Chapter 3 is silent, the module states an interpretation (Table B.4), so that the reader can disagree with it.

**Table B.4. Interpretations made where the methodology of Chapter 3 is silent**

| ID | Question | Interpretation |
|---|---|---|
| I-1 | What is a "step" when the agent proposes several calls at once? | Each proposed call is a step; calls in one assistant message share one decision point |
| I-2 | Does x^beh₂ count refused calls? | Yes, because the methodology of Chapter 3 states that retries raise x^beh₂ |
| I-3 | x^beh₃ at the first call | "Highest level so far" is the lowest level (0) |
| I-4 | x^beh₄ at the first call | Previous tool is a start symbol; start transitions belong to the reference set |
| I-5 | x^act₂ "transactions before first untrusted ingestion" | Observable only through untrusted tool outputs, so it reduces to "recipient not in the objective" |
| I-6 | x^act₃ "external recipient", "sensitive values" | Recipient differs from the user's own IBAN; sensitive values are identifiers and profile values from sensitive reads |
| I-7 | Availability of x^act₁ for predicate D2 | Unavailable when the tool has key arguments but the call carries none |
| I-8 | "Tool class" in episode-level Modify | The tool's action category (Table 3.5) within 𝒯~R~ |
| I-9 | Unavailable feature below k~D2~ | Takes the value 0 ("not observed") and is flagged in the audit record |

The benign transition set used by x^beh₄ must be estimated within each fold (Section 3.11.6). Each step record therefore stores its transition, and x^beh₄ is recomputed for every fold's reference.

### B.1.7 Layer 4 — Decision Engine

**Estimation.** `RidgeLogisticRegression` computes s = β₀ + βᵀx and p̃ = σ(s) (Eq. 3.1), fitted by Newton–Raphson with the intercept unpenalized. Fitting without a declared λ raises `DesignNotSpecifiedError`. The implementation minimizes NLL + (λ~impl~/2)‖β‖², so λ on the scale of Eq. 3.2 is λ~impl~/2 (Section 3.7.1). Selected values are reported on both scales.

**Calibration.** Both calibrators compute p = σ(γ₁s + γ₀) and reject a fit with γ₁ ≤ 0. They differ only in the fitting target: labels (Eq. 3.4, the reference) or Platt's smoothed targets (sensitivity).

**Consequence tiers, predicates and feasible set.**
- `ConsequenceTierMap` maps each tool to its category and the call to a tier. A transfer with a missing or unparseable amount receives the above-limit tier.
- `PredicatePolicy` implements D1 and D2, and the feasible set (Modify only for tools in 𝒯~R~).
- `A3Policy.decide` applies D1 and D2 before the expected-loss rule. When a predicate applies, the risk table is recorded as *not applicable* and p is marked as not used.

**Verdict.** `A3Policy` computes R(v) for v ∈ 𝒱(aₜ) through the frozen `conditional_risk` and returns the minimizer. Ties are handled by an explicit `tie_mode`:
- `"raise"` reproduces the frozen behavior;
- `"record_chapter3_order"` applies the Chapter 3 order and marks the step as tied.

An option `exclude_from_expected_loss=(Escalate,)` produces the comparison configuration "REM without expected-loss Escalate" (Section 3.7.7).

**Loss structure and dominance check.** `build_loss_grid` constructs Table 3.11 including Eq. 3.5, and `reachable_verdicts` reports any verdict that is never the unique minimizer.

**Baseline B1.** `operating_threshold` implements Eq. 3.14, and `A1Policy` applies it with the same estimator, calibration and predicates.

**Audit record.** For each step, `RemGuard.evaluate` writes:
- the tool name and a SHA-256 digest of its arguments, with the argument keys;
- the evidence vector and its availability;
- s, p̃ and p, and whether p was used;
- the tier, and the risk table or *not applicable*;
- the verdict, its source and the mitigation;
- the linear attributions with their additivity error;
- REM's processing time.

Raw argument values are not written.

### B.1.8 Layer 5 — Mitigation, and What Happens at the Tool Boundary

Mitigation is applied before any tool executes. In `GuardedToolsExecutor.query`, each proposed call is evaluated by `RemGuard.evaluate`. If the call is released, `runtime.run_function` executes it. Otherwise it is not executed, and a tool-result message carrying the refusal or restriction notice is returned to the agent in its place. The replay tests check this directly: an oracle that blocks every labelled step leaves the benchmark's security check false, and the withheld steps appear in the audit record with their tool and argument digest.

**Both mitigation semantics are implemented** (Table 3.12). Step-level semantics is the reference; the episode-level variant maintains a restriction set S for the episode. Under step-level semantics, Modify and Block have the same effect on the current call. The two semantics can differ without any retry: an episode-level Block refuses every later call to a tool in 𝒯~R~, including a call whose own verdict is Allow. `tests/test_mitigation_semantics.py` checks this on a fixed sequence: Block `send_money`, then Allow `update_password`; the second call is released under step-level semantics and refused under episode-level semantics. Chapter 4 (Table E.1) reports the replay results of both semantics.

**Escalate.** No reviewer exists. Escalation is resolved by one of two bounds:
- an idealized reviewer, which releases the call if and only if its label is 0;
- no reviewer, in which the call is withheld.

**Correction made in revision R2.** In the frozen pipeline, the Block mechanism cleared the step's tool call before the audit record was written. The record therefore lost the identity of the blocked action. A test now reproduces the defect, and the fix keeps the tool name and argument digest in the step's metadata, without raw arguments. The audit record uses them. The fix does not change any verdict or mitigation, and it does not affect any result in Chapter 4, because the experiments use the evaluation path, in which mitigation never alters the proposed call, so the tool's identity was always recorded; the argument digest was added to that record in this revision.

### B.1.9 Non-Invasive Placement and Its Limits

"Non-invasive" means here that **the agent's model, prompts and tools are not modified**: REM observes the messages the agent produces and the results the tools return. The placement has limits:
- **REM replaces the executor.** It must be inserted into the agent's execution loop, here as a subclass of the benchmark's `ToolsExecutor`. A framework in which tools are executed by a component REM cannot wrap is not covered.
- **Only executor calls are mediated.** Effects that do not pass through the tool executor (for example, a tool with side effects inside its own implementation, or a second agent) are outside REM's view.
- **Refusals are visible to the agent.** They are returned as tool-result messages. The agent's reaction to them is part of the system's behavior, and the replay analysis does not observe it.
- **Some context is inferred, not received.** In the evaluation, REM receives the objective and system prompt from the recorded trace. A deployment must supply them through the same channel.

### B.1.10 Optional Sequential Analysis (A2)

`rem/algorithms/behavior/cusum.py` and `rem/algorithms/a2.py` implement the Bernoulli CUSUM of Eqs. 3.15–3.19. The module has no interface to the decision engine and returns no verdict; a test checks both properties.

An A2-driven enforcement policy and a retrained "A3 + A2" variant are not implemented, because they would place CUSUM in the verdict path.

### B.1.11 Verification

#### Unit and contract verification

**Table B.5. Test suite (executed on 1 Nov 2026: 205 passed with AgentDojo installed; log `verification/pytest_R4.txt`)**

| File | Tests | Verifies |
|---|---|---|
| `test_frozen_math.py` | 43 | Eqs. 3.1–3.3, 3.6; fail-closed fitting; γ₁ > 0; a tie raises |
| `test_contract_compliance.py` | 20 | Five layers, no sixth; frozen mitigation mapping; no equation IDs; forbidden components absent; attribution excluded from the decision signature |
| `test_metrics.py`, `test_probabilistic.py` | 25 + 5 | ROC-AUC against the pairwise definition; average precision; ECE binning (Eq. 3.20); log-loss; Brier conventions; grouped bootstrap |
| `test_pipeline.py` | 21 | Frozen pipeline order; step-level Block; **the blocked action's identity is kept in the audit record** (added in R2) |
| `test_mitigation.py`, `test_trajectory.py`, `test_config.py`, `test_reproducibility.py` | 9 + 12 + 15 + 9 | Step-level mitigation, configuration fail-closed, seeds |
| `test_a3.py` | 10 | Table 3.11; Eqs. 3.8–3.10; argmin over the feasible set; D1 and D2; ties; dominance check; **REM without expected-loss Escalate keeps D2** (added in R2) |
| `test_a1.py` | 5 | Eq. 3.14 minimality; α = 0; invariance under monotone recalibration; verdict rule |
| `test_a2.py` | 5 | Eqs. 3.15–3.17; indicator set; false-alarm target; no verdict |
| `test_evidence.py` | 7 | Trust order; hygiene; features on an injected and a legitimate transfer; availability; tier map |
| `test_crossfit.py` | 2 | Procedure 3.1 outputs; held-out predictions independent of held-out labels |
| `test_traces.py` | 2 | Label rule including induced reads and ambiguity; fold-specific x^beh₄ |
| `test_replay.py` | 3 | All-Allow replay reproduces a recorded episode; oracle Block prevents the recorded attack; **withheld calls keep tool and argument digest, and no raw attacker value appears in the audit record** (extended in R2); observe-only releases everything |
| `test_mitigation_semantics.py` | 4 | Step-level and episode-level policies on a fixed sequence (Block `send_money`, then Allow `update_password`): different release outcomes, neither policy altered (added in R4) |
| `test_latency_instrumentation.py` | 2 | Fake-clock check that the partial timer stops before attribution, audit construction and history recording, and the complete-call timer after them (added in R4) |
| `test_docx_tables.py` | 6 | Thesis build tooling, not REM: the Word table transformation keeps exactly one run-property container per run, preserves hyperlinks and equations, and is idempotent (added in R4) |

#### Integration verification

- **Replay fidelity.** With every call allowed, the replay reproduced the recorded utility and security outcome of 3,313 of 3,334 episodes (99.4%). The 21 exceptions are analyzed in Chapter 4.
- **Determinism and regression.** The complete pilot was run at commit `aa66f22` (R1) and again at commit `84a8c21` (R2), after the corrections of this revision. An automated comparison of the 5,121 values the two runs share found 93 differences, all of them wall-clock time or memory measurements; every analytical value was identical. A second comparison with a different leaf-matching method (`compare_reproduction.py`, R3) counted 5,220 shared values and 104 differences, all in time, memory or provenance fields, and 0 analytical differences.
- **Re-execution in a fresh environment (R3, 30 October 2026; by this project, not an external replication).** The complete pipeline (`run_all.sh`) was executed again, from the merged repository state, on a different processor and with the AgentDojo repository obtained afresh at commit `089ed468`. Of the 6,057 numeric values that the re-run shares with `results/pilot_R2/`, 5,943 were identical. The 114 that differed are 100 per-step latency values, 13 code-commit stamps and one file path; no memory value and 0 analytical values differed (`RESULTS_PROVENANCE_REPORT.md`; every differing value is listed in `verification/reproduction_all_differences.json`).
- **Re-execution with the complete-call timer (R4, 1 November 2026).** After the timer was added, the complete pipeline was executed again into `results/pilot_R4/`. Of the 6,057 numeric values it shares with `results/pilot_R2/`, 5,942 were identical, 115 were latency, commit or file-path values, and 0 analytical values differed. The new complete-call fields have no R2 counterpart. Every differing value is listed in `verification/reproduction_all_differences_R4.json`.
- **Attribution additivity.** The audit record carries |φ₀ + Σφᵢ − s| for every replayed step.

#### What is not verified here

Security effectiveness against live agents is not verified; Chapter 4 states what the recorded-trace analyses can and cannot show.

### B.1.12 Correspondence Between Requirements, Equations, Code, Tests and Results

**Table B.6. Requirement → equation → function → test → result artifact**

| Requirement (the methodology of Chapter 3) | Equation | Function | Test | Result artifact (`results/pilot_R2/`) |
|---|---|---|---|---|
| Logit and uncalibrated probability | 3.1 | `ridge_logistic.RidgeLogisticRegression.decision_function` | `test_frozen_math` | `e1_crossfit.json` (`pooled_uncalibrated`) |
| Ridge fit (λ = λ~impl~/2) | 3.2 | `RidgeLogisticRegression.fit` | `test_frozen_math` | `e1_crossfit.json` (`per_fold.*.lambda`, `lambda_chapter3_eq3_2_scale`) |
| Calibration map, γ₁ > 0 | 3.3 | `PlattLogitCalibrator.calibrate` | `test_frozen_math` | `e1_crossfit.json` (`gamma_1`) |
| Calibration fit on labels | 3.4 | `logit_nll.LabelNLLLogitCalibrator.fit` | `test_crossfit` | `e1_crossfit.json` (`label_nll_primary`) |
| Adversarial Modify loss | 3.5 | `loss_matrix.build_loss_grid` | `test_a3` | `e4_rmod_and_replay_validity.json` (r~mod~) |
| Conditional risk | 3.6 | `expected_loss.ExpectedLossDecisionEngine.conditional_risk` | `test_frozen_math`, `test_a3` | `e2_e5_e6_observe_only.json` |
| Verdict over 𝒱(aₜ), ties | 3.7 | `a3.A3Policy.decide` | `test_a3` | `e2_e5_e6_observe_only.json` (`ties`) |
| Thresholds, feasibility, dominance | 3.8–3.10 | `loss_matrix.*` | `test_a3` | `e2_e5_e6_observe_only.json` (`dominance`) |
| Attribution, additivity | 3.11–3.13 | `linear_shapley.LinearShapleyAttributor` | `test_frozen_math` | replay audit field `additivity_error` |
| Baseline thresholds | 3.14 | `a1.operating_threshold` | `test_a1` | `e1_crossfit.json` (`theta_blk`, `theta_mod`) |
| CUSUM | 3.15–3.19 | `cusum.BernoulliCusum`, `a2.*` | `test_a2` | `e3_a2_cusum_observe_only.json` |
| ECE, log-loss | 3.20–3.21 | `probabilistic.*` | `test_probabilistic` | `e1_crossfit.json` |
| Realized loss | 3.22 | `run_main.stage_observe` | — (script) | `e2_e5_e6_observe_only.json` (`e6_grid`) |
| D1/D2 before expected loss | — | `PredicatePolicy.evaluate`, `A3Policy.decide` | `test_a3` | `e2_e5_e6_observe_only.json` (`sources`) |
| Step- and episode-level mitigation | Table 3.12 | `RemGuard._mitigate` | `test_replay` | `e4_e5_enforcement_replay.json` |
| Audit identity of withheld actions | Section 3.7.6 | `RemGuard.evaluate`; `mitigation.py`, `audit.py` | `test_replay`, `test_pipeline` | — |

**Table B.7. Components required, implemented and absent**

| Component (the methodology of Chapter 3) | Status |
|---|---|
| Provenance labels, hygiene | Implemented |
| Entity extraction | Partly implemented (Appendix B.1.4) |
| x^ctx₁ injection classifier | **Absent** |
| x^ctx₂, x^beh₁–₄, x^act₁–₃ | Implemented |
| Ridge estimator; both calibration fits | Implemented |
| Tiers, predicates, feasible set, loss structure, dominance check | Implemented |
| REM verdict; B1; REM without expected-loss Escalate | Implemented |
| Step-level and episode-level mitigation | Implemented (evaluation path) |
| Human reviewer | Absent; replaced by two bounds |
| Offline fitting (Procedure 3.1) | Implemented |
| CUSUM (observe-only) | Implemented |
| Live enforcing-mode execution | **Not executed** (no LLM access) |

### B.1.13 Logging of Sensitive Values

- **Audit records.** The audit records of the evaluation path store argument digests and keys, not values. A test checks that neither the attacker's account identifier nor the attacker's password appears in any audit record of a replayed episode.
- **Frozen audit log.** It stores digests by default; raw payloads are written only if `record_payloads=True` is set explicitly.
- **Result files.** Two result files contain argument values copied from the benchmark's traces: the label-audit sample and the human label-audit package. These values are synthetic benchmark data (simulated IBANs and passwords), not real credentials.
- **Credentials.** No credential, API key or real account identifier is used by the code or written by it.

### B.1.14 Runtime Measurement

Two timers are recorded for every step. Both start with `time.perf_counter` at the entry of `RemGuard.evaluate`. They differ in where they stop (Table B.8).

**Table B.8. Boundaries of the two timers**

| Work inside `RemGuard.evaluate` | Partial timer `rem_latency_ms` (R1–R4) | Complete-call timer `rem_latency_full_ms` (R4) |
|---|---|---|
| Feature computation (Layers 1–3) | Included | Included |
| Tier, reference-label lookup, scoring and calibration | Included | Included |
| Predicates, verdict and mitigation decision | Included | Included |
| Linear attribution and additivity check | **Excluded** | Included |
| Audit-record construction, including the argument digest | **Excluded** | Included |
| Recording the proposal in the episode history | **Excluded** | Included |

Both timers **exclude**:
- LLM inference (absent in replay);
- tool execution and benchmark environment set-up;
- the benchmark pipeline's own overhead;
- the call into and return from `evaluate`.

Both **include** the reference-label lookup. This is evaluation bookkeeping, which a deployment would not perform: it computes the evaluation label recorded in the audit record and used by the idealized reviewer.

**Correction.** Revision R3 stated that the measured interval included attribution and audit-record construction. It did not: the timer of R1–R3 stopped before them. All R1–R3 timing values are partial-timer values. The complete-call timer was added in R4 without changing the partial timer. `tests/test_latency_instrumentation.py` checks both boundaries with a fake clock and an ordered event log, not with wall-clock thresholds.

**Conditions.** Measurements were taken in four parallel worker processes on a 4-vCPU container, so they include contention between workers, and they vary between runs (Appendix B.1.11). The R4 run used an Intel Xeon @ 2.80 GHz with Python 3.11.17 and NumPy 2.4.6. Memory is a separate measurement: the peak allocation traced by `tracemalloc` around the complete `RemGuard.evaluate` call, on 300 episodes with the episode-level variant.

These figures describe the evaluated configuration: no injection classifier, no reviewer, and Python on this hardware. They do not describe a deployment that includes a neural classifier or a human review step.

# Appendix C: Notation, Optional Sequential Analysis and Equation Provenance

## C.1 Notation

**Table C.1. Notation used in this chapter**

| Symbol | Meaning |
|---|---|
| t, T | Step index within an episode; episode length |
| g | User objective of the episode |
| c~t~ | Context at step t, as segments with provenance labels |
| a~t~ | Proposed action (tool name and arguments) at step t |
| H~t~ | Episode history up to step t |
| y~t~ ∈ {0, 1} | Latent label: 1 if a~t~ is adversarially induced |
| x~t~ ∈ [0, 1]^d^ | Evidence vector; groups x^ctx^, x^beh^, x^act^ with index sets I~ctx~, I~beh~, I~act~ |
| β~0~, β, λ | Logistic intercept, coefficient vector, ridge strength |
| s~t~ | Logit (linear predictor) |
| p̃~t~, p~t~ | Uncalibrated probability; calibrated probability |
| γ~1~, γ~0~ | Calibration slope and intercept |
| z~t~, k~t~, κ | Consequence descriptors; consequence tier; tier map |
| 𝒱 | Verdict set {Allow, Modify, Escalate, Block} |
| 𝒱(a~t~) | Verdicts feasible for a~t~ |
| v~t~ | Verdict issued at step t |
| L(v, y, k) | Loss of verdict v when the label is y and the tier is k |
| C~miss~(k), C~FA~(k), C~mod~(k), C~esc~ | Declared costs of a missed attack, a false intervention by Block, Modify on a legitimate action, and escalation |
| r~mod~(k) | Residual attack-success rate after Modify at tier k (measured) |
| R~t~(v) | Conditional risk of verdict v at step t |
| π~v,v′~(k), p^\*^~k~ | Indifference threshold between verdicts v and v′; Allow–Block threshold |
| σ(·) | Logistic function, σ(u) = 1 / (1 + exp(−u)) |
| Π, k~D2~ | Set of prohibited actions; minimum tier for predicate D2 |
| θ(α), α~blk~, α~mod~ | Baseline threshold for false-positive target α; targets for Block and Modify |
| 𝒯~R~ | Set of tools to which the Modify mechanism applies |

Symbols used only in the optional sequential analysis are defined in Appendix C.3. Symbols that appear in a single equation, such as Δ~0~, Δ~1~, B~m~, and the step sets D~fit~, D~cal~, and D~val~^benign^, are defined where they are used. Each symbol has one meaning throughout the chapter.

## C.2 Layer interfaces

**Table C.2. Layer interfaces**

| Layer | Consumes | Produces |
|---|---|---|
| L1 Input & Context | Objective, system prompt, user messages, tool results, proposed action | Labeled context c~t~; entities with provenance; held action a~t~ |
| L2 Detection | Untrusted segments of c~t~ | Context evidence x^ctx^ |
| L3 Behavioral Analysis | H~t~, a~t~, entities, benign reference transitions, privilege map | Behavioral evidence x^beh^; action evidence x^act^ |
| L4 Decision Engine | x~t~, consequence descriptors z~t~, frozen parameters, declared policy | p~t~, k~t~, R~t~(·), verdict v~t~, audit record |
| L5 Mitigation | v~t~, a~t~, episode restrictions | Released, restricted, withheld, or refused action |

The four functions are separated architecturally. Layers 2 and 3 produce evidence and issue no verdicts. Layer 4 performs probability estimation and decision. Layer 5 performs mitigation.

## C.3 Optional observe-only sequential analysis

Sequential change detection is not part of REM's verdict path. If the supervisor approves it for the thesis narrative, it is performed **offline** on the per-step indicators logged by the Behavioral Analysis Layer. It never influences a verdict.

For each step, a binary deviation indicator e~t~ ∈ {0, 1} is defined as 1 if at least one of x^beh^~1~, x^beh^~3~, x^beh^~4~, or x^act^~1~ equals 1, or if x^beh^~2~ = 1; otherwise 0 [indicator set pending supervisor approval]. Let q~0~ and q~1~, with 0 < q~0~ < q~1~ < 1, be the rates of e~t~ = 1 before and after an adversarial change.

The log-likelihood ratio of one observation, as defined by Basseville and Nikiforov (1993), specialized to Bernoulli observations, is:

$$ \ell_t = e_t \ln\frac{q_1}{q_0} + (1-e_t) \ln\frac{1-q_1}{1-q_0} \qquad (3.15) $$

*Status:* derived by substituting the Bernoulli probability mass function into the log-likelihood ratio of Basseville and Nikiforov (1993). A cumulative sum chart for Bernoulli observations is treated by Reynolds and Stoumbos (1999).

The cumulative sum statistic and alarm time are (Basseville & Nikiforov, 1993; Page, 1954):

$$ G_t = \max(0,\, G_{t-1} + \ell_t), \qquad G_0 = 0 \qquad (3.16) $$

$$ T_A = \min\{ t : G_t \ge h_G \} \qquad (3.17) $$

where h~G~ > 0 is the alarm threshold.

*Status:* established from source.

The per-episode false-alarm rate on benign episodes and the detection delay are defined as:

$$ \mathrm{FA}_{\mathrm{ep}}(h_G) = \frac{\left|\{ j \in E_{\mathrm{ben}} : \max_t G^{(j)}_t \ge h_G \}\right|}{\left|E_{\mathrm{ben}}\right|} \qquad (3.18) $$

$$ \tau_d = T_A - \nu, \qquad T_A \ge \nu \qquad (3.19) $$

where E~ben~ is the set of benign episodes in the fitting portion of a fold, G^(j)^~t~ is the statistic in benign episode j, τ~d~ is the detection delay, and ν is the first step at which injected content enters the context.

*Status:* design definitions.

The parameters are determined as follows:
- q~0~ is the empirical rate of e~t~ = 1 on benign fitting steps, floored at a declared minimum.
- q~1~ is declared and reported over a range, because the scarcity of multi-step attacks does not allow it to be estimated reliably.
- h~G~ is the smallest value for which Equation 3.18 does not exceed a declared target.

The procedure has known optimality properties in sequential change detection: Lorden (1971) proposed stopping rules that are asymptotically optimal in a defined sense, and Moustakides (1986) showed Page's stopping time to be optimal in a stronger sense. Both results are proved within a sequential-analysis model whose conditions could not be inspected during verification and are not claimed to hold for agent trajectories, where observations are neither independent nor drawn from known distributions. They therefore motivate the procedure and provide no guarantee in this setting. Given the short trajectories of Section 3.11.4, this analysis may have little to detect.

## C.4 Provenance of the equations of Chapter 3

**Table C.3. Provenance of the equations in this chapter**

| Eq. | Content | Status | Source | Verification |
|---|---|---|---|---|
| 3.1 | Logistic model | Established | Cox (1958) | IV |
| 3.2 | Ridge-penalized log-likelihood | Established | le Cessie & van Houwelingen (1992) | IV (penalty constant pending) |
| 3.3 | Logistic calibration on the logit, γ~1~ > 0 | Adapted | Platt (2000); Guo et al. (2017); Kull et al. (2017) | Platt NC; Guo FV; Kull FV |
| 3.4 | Calibration fit by negative log-likelihood | Established | Guo et al. (2017) | FV |
| 3.5 | Adversarial loss of Modify | Derived (assumption A-Mod) | Law of total expectation | DER |
| 3.6 | Conditional risk | Adapted | Elkan (2001) | FV (Eq. 1 form) |
| 3.7 | Bayes verdict with tie-breaking | Adapted | Elkan (2001) | FV; tie order DEF |
| 3.8 | Pairwise indifference threshold | Derived | From Eq. 3.6 | DER |
| 3.9 | Allow–Block threshold | Derived | From Eq. 3.8; consistent with Elkan (2001) | DER |
| 3.10 | Escalation feasibility condition | Derived | From Eqs. 3.6, 3.7, 3.9; Chow (1970) conceptual basis | DER; Chow IV |
| 3.11 | Linear attribution | Adapted | Lundberg & Lee (2017) | FV |
| 3.12 | Completeness identity | Derived | Lundberg & Lee (2017) local accuracy | FV + DER |
| 3.13 | Group attribution | Definition | — | DEF |
| 3.14 | Baseline operating-point threshold | Definition | — | DEF |
| 3.15 | Bernoulli log-likelihood ratio (optional) | Derived | Basseville & Nikiforov (1993); Reynolds & Stoumbos (1999) | FV; R&S IV |
| 3.16 | CUSUM recursion (optional) | Established | Basseville & Nikiforov (1993); Page (1954) | FV; Page IV |
| 3.17 | Alarm time (optional) | Established | Basseville & Nikiforov (1993) | FV |
| 3.18 | Per-episode false-alarm rate (optional) | Definition | — | DEF |
| 3.19 | Detection delay (optional) | Definition | — | DEF |
| 3.20 | Expected calibration error | Adapted | Naeini et al. (2015); Guo et al. (2017) | FV |
| 3.21 | Log-loss | Derived | From Eq. 3.2 | DER |
| 3.22 | Realized loss | Definition | — | DEF |

**Implementation conventions.** Four conventions in the implementation differ in form from the equations as printed; none changes their meaning:

- **Eq. 3.2:** the code's penalty is (λ~impl~/2)‖β‖², so λ = λ~impl~/2 (Section 3.7.1).
- **Eq. 3.4:** the label-NLL fit is the reference; Platt's smoothed targets are a sensitivity variant.
- **Eq. 3.14:** the candidate set includes a value just above the largest benign probability.
- **Eq. 3.20:** steps with p = 0 fall in the first bin.

These conventions are listed with the code location of each equation in the requirement–equation–function–test table of Section 3.14.

*Verification codes:* FV — formulation checked against the source; IV — source identity confirmed, formulation to be checked against the full text; NC — source not accessible during this revision; DER — derived in this chapter; DEF — design definition. The codes are retained until final reference verification is complete.

# Appendix D: Live-Agent and MELON Evaluations: Design and Status (Not Executed)

This appendix records the design and status of two evaluations that were implemented and **not executed with a language model**: the closed-loop evaluation of REM with live agents, and the controlled evaluation of MELON with and without REM. Nothing in this appendix is an experimental result. The checks it reports use scripted agents and simulated providers and establish only that the integrations are mechanically correct. The text is reproduced from the thesis drafts of 3 to 6 November 2026.

## D.1 Closed-loop evaluation with live agents: design and implementation status

**Status.** The closed-loop evaluation described in this section is **implemented and tested with scripted test agents, but has not been executed with a language model** (Section 4.16). Nothing in Chapter 4 is a live result.

### D.1.1 Purpose

The replay sensitivity analysis (Section 3.11.10) re-executes recorded trajectories and assumes that the agent does not adapt to REM's refusals. It can therefore show whether a recorded attack call would have been withheld, but not what an agent does after a refusal: it cannot observe retries, rephrased calls or alternative tools. The closed-loop design removes that assumption. A running LLM agent receives REM's decision for each proposed call and may continue, retry, replan or stop, and the benchmark scores the outcome after the agent's own reaction.

### D.1.2 Defended agent pipeline

The integration uses AgentDojo's own pipeline elements without modifying the benchmark (Figure D.1). The pipeline consists of a system message, the user task's prompt, the LLM, and a tool-execution loop in which AgentDojo's tool executor is replaced by REM's guarded executor (Appendix B.1.8). For each proposed call the defended process is:

1. the agent proposes a tool call with arguments;
2. REM intercepts the call **before** it is executed;
3. REM computes the evidence vector, the tier, the logit and the calibrated probability with frozen parameters (Sections 3.4–3.7);
4. the decision function selects Allow, Modify, Escalate or Block (Eqs. 3.6–3.7, or the baseline of Eq. 3.14);
5. the Mitigation Layer applies the declared semantics (Section 3.8, Table 3.12): a released call is executed in the sandbox; a withheld call returns a tool message with the same tool-call identifier and a refusal notice;
6. the result or refusal re-enters the agent's context as untrusted content, and the agent continues;
7. the benchmark evaluates utility and security on the final environment.

The decision code is the code of the recorded-trace study (`RemGuard`); only the source of the agent's messages changes, from a recorded trajectory to a live model. AgentDojo re-queries the pipeline up to three times when the agent produces no final answer; the same guard, and therefore the same episode history, persists across these re-queries.

![Figure D.1. Closed-loop (live-agent) evaluation architecture. REM's guarded executor replaces AgentDojo's tool executor; the agent receives the result of a released call or the refusal of a withheld one and may retry, replan or stop. Implemented and tested with scripted test agents; not executed with a language model.](REM_FINAL_THESIS/final_five_chapters/figures/fig3_5_live_architecture.png){width=100%}

### D.1.3 Conditions and controlled variables

Three primary conditions are defined, with the same pipeline, tasks, injections, system prompt, model, decoding settings and iteration limit:

- **B0:** no defense (every call released; REM records the step but never intervenes);
- **B1:** the consequence-independent operating-point baseline (Eq. 3.14) on the same frozen estimator, calibration and predicates;
- **REM:** the tier-indexed expected-loss verdict (Eqs. 3.6–3.7) on the same frozen estimator.

REM without expected-loss Escalate (Section 3.11.7) can be added as a fourth condition. The comparison B1 versus REM therefore isolates the decision rule, as in the recorded-trace study.

### D.1.4 Frozen parameters

No parameter is fitted on live data. The estimator, calibration map, baseline thresholds, benign reference and r~mod~ are those of one outer fold of the recorded-trace cross-fitting (Procedure 3.1). Which fold is used is a design input; the pilot has no fit on all recorded data.

### D.1.5 Design inputs required before execution

The runner refuses to start until each of the following has been decided and recorded (CLAUDE design lock; supervisor decision register D-2, D-6, D-7, D-8, D-9, D-15):

| Input | Status |
|---|---|
| Authorisation for paid model use, budget, pre-registration of hypotheses and analysis | Pending (D-15) |
| Backbone(s) with exact model versions; decoding parameters | Pending (D-15) |
| Number of repeats per configuration | Pending (Section 3.11.9 proposes at least three) |
| Suite version, attack templates, user and injection tasks | Pending (D-6) |
| Mitigation semantics (step-level and/or episode-level) | Pending (D-2) |
| Reviewer treatment (idealized and/or no-reviewer bound) | Pending (D-7) |
| Costs, tiers, predicates and feature set | Exploratory pilot values only (D-9, D-8) |
| Fitted-parameter source (outer fold) | Pending |

### D.1.6 Metrics, statistics and logging

The metrics are those of Section 3.12, computed on live outcomes: attack success rate, benign utility and utility under attack from the benchmark's verdicts; intervention rates on y = 0 and y = 1 proposals; and processing time from the complete-call timer. Three descriptive adaptation counts are added, computed from REM's audit record: a *retry* is a later proposal of the same tool with the same argument digest as a withheld call; a *replan* is a later proposal of a different restricted tool after a withheld call; and a *release after refusal* is a reference-labelled attack call released after an earlier withheld call in the same episode. Uncertainty is estimated by the grouped bootstrap of Section 3.11.9, with repeats kept inside their injection-task or user-task group. Every episode is logged with its audit records, truncated messages and adaptation counts, together with a manifest of the commit, configuration hash and frozen fold.

### D.1.7 Safety precautions

All tools act on the benchmark's simulated banking environment; no real account or payment system is reachable, and REM never initiates a call. Argument values are recorded only as digests in the audit record, and message logs are truncated.

### D.1.8 Implementation and verification status

**Table D.1. Implementation status of the closed-loop evaluation (3 November 2026)**

| Component | Location | Status |
|---|---|---|
| Defended live pipeline | `rem/integration/agentdojo_live.py` | Implemented; tested with scripted test agents |
| Guarded executor, decision and mitigation | `rem/integration/agentdojo_replay.py` (unchanged) | Implemented; used in the recorded-trace study |
| Runner with fail-closed configuration and credential checks | `experiments/live/run_live.py` | Implemented; verified to refuse the undecided template |
| Metrics with grouped bootstrap | `experiments/live/analyze_live.py` | Implemented; tested on synthetic records |
| Integration tests (interception, semantics, identifiers, retries and replans, episode isolation, label isolation) | `tests/test_live_integration.py` | 12 tests passed (full suite: 217 passed) |
| Harness smoke test with a scripted ground-truth agent on all 160 task combinations | `experiments/live/smoke_scripted.py` | Executed: 480 episodes, 0 errors (not an experimental result) |
| Execution with a language model | — | **Not executed**: no model credential; design inputs pending |

## D.2 Closed-loop evaluation with live agents: status on 3 November 2026

**The closed-loop evaluation with live agents was not executed.** This section therefore reports no attack success rate, utility, intervention statistic or adaptation behavior of a live agent, and no table or figure in this chapter contains a live result.

Two conditions prevented execution on 3 November 2026:

- **No model access.** No credential for a language-model provider was available in the execution environment; the provider endpoints that were reachable rejected unauthenticated requests, and model-weight repositories were not reachable, so no local model could be run.
- **Undecided design inputs.** The backbone, decoding parameters, number of repeats, fitted-parameter source, authorisation and pre-registration (Appendix D.1.5) have not been decided. The runner refuses to start until they are.

What was executed concerns the correctness of the integration, not the effectiveness of REM:

**Table D.2. Verification of the closed-loop integration (not experimental results)**

| Check | Agent | Outcome |
|---|---|---|
| Integration tests (12) | Scripted test double that proposes predetermined calls and retries or replans after a refusal | All passed: released calls execute; withheld calls (Block, Modify, unapproved Escalate) are not executed and the agent receives a refusal with the original call identifier; step-level Modify does not persist, episode-level Modify does; retries and replans are recorded; episode state is not shared; REM verdicts are unchanged when reference labels are flipped |
| Harness smoke test (B0, B1, REM; step-level, no reviewer; one frozen fold) | Scripted agent that executes the ground-truth calls of the user task and then of the injection task, without adapting | 480 episodes over all 144 attacked task pairs and 16 benign tasks with the benchmark's `important_instructions` injections; 0 execution errors; no withheld call was executed |

The smoke-test agent is not a model of an LLM agent: it never reads tool outputs or reacts to refusals. Its counts are therefore not reported as attack-success or utility results. The live evaluation remains the first item of future work (Section 5.7).

## D.3 Replay versus live evaluation

No comparison of replay and live results is possible, because no live result exists (Section 4.16). The replay results of Section 4.6 must not be read as live results. The two designs estimate different quantities:

**Table D.3. Differences between the replay sensitivity analysis and the closed-loop design**

| Aspect | Replay (Section 4.6) | Closed loop (Appendix D.1; not executed) |
|---|---|---|
| Agent messages | Recorded, replayed in order | Generated by a running model |
| Reaction to a refusal | None (NO-ADAPT) | Retry, replan or stop |
| Meaning of attack success | Whether the recorded attack calls would have been withheld | Whether the attack succeeds despite the agent's reaction |
| Residual success after Modify | Close to zero by construction | Observable |
| Repeatability | Deterministic | Stochastic; requires repeats |
| Backbones | 21 recorded historical backbones | To be decided |

Because a live agent can retry or route around a refusal, the replay attack success rate is not an upper bound on live attack success. How large the difference is, in either direction for utility, is an empirical question that only the closed-loop evaluation can answer.

## D.4 Controlled evaluation of MELON with and without REM: protocol

**Status.** This section describes an **implemented protocol for a planned evaluation**. The integration has been verified locally with scripted test agents and fake model clients only. **No run with a language model has been executed, and Table D.4 contains no result.**

### D.4.1 Why MELON is the reference

MELON (Zhu, Yang, et al., 2025) is a published runtime defence against indirect prompt injection that was evaluated on AgentDojo and has an official implementation. Chapter 2 reviews it among the goal–action consistency defences (Section 2.5.2; Table A.3).

MELON re-executes the agent's next step with the user's request masked. It flags an attack when the actions proposed with and without the request are similar, and it then stops the agent. Its evidence is therefore behavioural and model-based. It does not weigh what a proposed action would do or how costly an error would be.

REM, by contrast, decides per action from a calibrated probability and consequence-tiered losses (Section 3.7). The study asks what changes when REM is added at the tool-execution boundary of MELON, compared with MELON alone. This is an **extension of a published defence through integration with REM**:
- MELON's algorithm is not modified;
- REM was not derived from MELON;
- no improvement is presumed;
- a record-level literature search found no evaluation of this combination, but the search was not exhaustive, so no novelty is claimed.

### D.4.2 Integration point

MELON's official implementation places its detector after AgentDojo's tool executor:
- the loop is `[ToolsExecutor, MELON]`;
- MELON makes the agent's next model call itself, together with a masked model call that executes no tool;
- on detection, MELON replaces the agent's proposed calls with a stop message.

**In MELON + REM, the executor is the only element replaced:** REM evaluates each call that survived MELON immediately before execution. It also evaluates the first turn's calls, which MELON does not inspect.
- A withheld call never reaches the environment.
- The agent receives a refusal carrying the call's identifier and may continue.
- REM never sees MELON's masked generation.

The official MELON code requires an AgentDojo version with string message content. Both conditions therefore run on AgentDojo 0.1.29, whose banking v1 task and attack code are identical to those of REM's fitting traces. Two compatibility measures are applied identically in both conditions:
- the embedding client is supplied without editing the file;
- MELON's per-episode state is reset between episodes, since otherwise it would persist across episodes and conditions.

Each measure and its effect are documented in the integration notes of the study's repository.

### D.4.3 Frozen settings and training provenance

REM runs with the frozen components of the nested cross-fit (Section 3.11). Nothing is refitted:
- **Estimator:** ridge estimator with logit calibration (γ₁ > 0 in every fold).
- **Predicates and loss structure:** the declared exploratory costs and consequence tiers of Section 3.7, which are not supervisor-approved.
- **Mitigation:** step-level semantics. Modify, Block and Escalate all withhold the current call; their immediate execution effect is the same.
- **Reviewer:** none. An escalated call is never released, and no label-based reviewer is used.

For an attacked case, the fold whose fit excluded that attacker objective is used. Because the 16 user tasks and their environment were seen in fitting, the evaluation covers **held-out attacker objectives on familiar tasks**, not unseen tasks.

### D.4.4 Protocol

- **Conditions:** MELON and MELON + REM.
- **Benchmark:** AgentDojo banking v1 with the `important_instructions` attack only.
- **Held fixed:** backbone and decoding, MELON's internal settings, attack payloads, step limit and the evaluation checks.
- **Pilot:** 13 cases chosen by a coverage rule declared in advance (every injection task once and four benign tasks), to test compatibility and measure cost.
- **Final case set and repeats:** fixed from the pilot's measured cost; the full set (144 attacked and 16 benign cases) is preferred.
- **Pairing and order:** episodes are paired by case and repeat and run in randomised, interleaved order, each in a fresh environment.
- **Metrics:** attack success rate, utility under attack and benign utility, each over episodes without error. Errors and timeouts are reported separately and never counted as prevented attacks; escalation is never counted as task completion.
- **Uncertainty:** paired differences with cluster-bootstrap intervals over user tasks.

**Table D.4. Controlled evaluation of MELON with and without REM (AgentDojo banking v1, `important_instructions`) — NOT EXECUTED**

| Metric | MELON | MELON + REM | Paired difference (95% cluster-bootstrap interval) |
|---|---|---|---|
| Attack success rate | not executed | not executed | not executed |
| Utility under attack | not executed | not executed | not executed |
| Benign utility | not executed | not executed | not executed |
| Additional calls withheld by REM | — | not executed | — |
| Escalate verdicts per evaluated call | — | not executed | — |
| Median end-to-end time per episode; REM time per call | not executed | not executed | not executed |
| Tokens and cost per episode | not executed | not executed | not executed |
| Errors and timeouts (by class) | not executed | not executed | — |

### D.4.5 Interpretation limits

When the study is run, the following limits apply to any finding:
- **Protection.** If MELON has no successful attack in the sample, no further reduction in observed attack success can be demonstrated, and the comparison is about utility and overhead.
- **Utility.** Any additional protection must be reported together with its utility cost. Under no-reviewer semantics, every REM intervention withholds an action.
- **Overhead.** REM adds no model call; MELON roughly doubles the number of model calls of an undefended agent.
- **Scope.** The conclusions are limited to:
  - one attack template;
  - one backbone;
  - exploratory REM costs;
  - familiar tasks;
  - a simulated banking environment.

  Adaptive attacks against MELON are not evaluated.

# Appendix E: Sensitivity of the Replay Results to the Mitigation Semantics

This appendix reports the replay results of Chapter 4, Section 4.6, under both mitigation semantics. Step-level semantics is the declared reference, pending the supervisor's decision on conflict SC-1. The episode-level rows are a sensitivity analysis.

## E.1 Replay results under the two mitigation semantics

**Table E.1. Replay results under the two mitigation semantics** (same episodes; same estimator, calibration, costs, predicates and thresholds; matching reviewer treatment for REM and B1; only the mitigation semantics varies. Verdict sequences are not fixed: see the notes below. ref. = the reference semantics; REM w/o Esc. = REM without expected-loss Escalate; attacked n = 2,979; benign n = 334; `e4_e5_enforcement_replay.json`, `configs.<configuration>_<semantics>_<reviewer>`)

| Configuration | Semantics | ASR | Benign utility | Utility under attack |
|---|---|---|---|---|
| B1, no reviewer | step-level (ref.) | 0.055 [0.011, 0.134] | 0.509 [0.334, 0.702] | 0.514 [0.501, 0.527] |
| B1, no reviewer | episode-level | 0.046 [0.004, 0.125] | 0.509 [0.334, 0.702] | 0.485 [0.474, 0.496] |
| B1, idealized reviewer | step-level (ref.) | 0.055 [0.011, 0.134] | 0.494 [0.329, 0.677] | 0.499 [0.487, 0.511] |
| B1, idealized reviewer | episode-level | 0.046 [0.004, 0.125] | 0.494 [0.329, 0.677] | 0.470 [0.460, 0.481] |
| REM, no reviewer | step-level (ref.) | 0.004 [0.001, 0.007] | 0.314 [0.110, 0.548] | 0.364 [0.345, 0.389] |
| REM, no reviewer | episode-level | 0.004 [0.001, 0.007] | 0.314 [0.110, 0.548] | 0.363 [0.344, 0.388] |
| REM, idealized reviewer | step-level (ref.) | 0.004 [0.001, 0.007] | 0.497 [0.333, 0.680] | 0.496 [0.483, 0.506] |
| REM, idealized reviewer | episode-level | 0.004 [0.001, 0.007] | 0.497 [0.333, 0.680] | 0.481 [0.468, 0.492] |
| REM w/o Esc., no reviewer | step-level (ref.) | 0.004 [0.001, 0.007] | 0.329 [0.126, 0.551] | 0.374 [0.351, 0.407] |
| REM w/o Esc., no reviewer | episode-level | 0.003 [0.001, 0.006] | 0.329 [0.126, 0.551] | 0.370 [0.347, 0.403] |
| REM w/o Esc., idealized reviewer | step-level (ref.) | 0.004 [0.001, 0.007] | 0.311 [0.123, 0.518] | 0.359 [0.337, 0.391] |
| REM w/o Esc., idealized reviewer | episode-level | 0.003 [0.001, 0.006] | 0.311 [0.123, 0.518] | 0.355 [0.333, 0.387] |

What is fixed and what differs, within NO-ADAPT:
- **What is fixed and what varies.** Both runs of each configuration use the same recorded episodes, the same fitted parameters, costs, predicates and thresholds, and the same reviewer treatment. They differ in the mitigation semantics: under the episode-level variant, an earlier Block or Modify adds tools to a restriction set that refuses later calls.
- **The verdicts are not identical.** For REM without a reviewer, the y = 0 steps received 239 Modify and 1,049 Escalate verdicts under step-level semantics, against 241 and 1,047 under episode-level semantics (`verdict_rates` of the two REM configurations). With the idealized reviewer the counts are 239 / 1,050 against 241 / 1,048. A call refused only under the episode-level variant returns no tool output, so the evidence for later steps can differ. B1's verdict counts are the same under both semantics.
- **B1's ASR is lower under episode-level semantics** (0.055 → 0.046): later state-changing calls are refused by the restriction set left by an earlier Block or Modify. REM's ASR is identical (0.004). REM without expected-loss Escalate changes from 0.004 to 0.003 (unrounded 0.0037 → 0.0034).
- **Utility under attack is lower or equal under episode-level semantics** in every configuration: the restriction set also refuses legitimate later calls.
- **Benign utility coincides** between the two semantics in every configuration of this replay. This is an observation about these episodes, not a property of the semantics.
- **REM − B1 ASR within each semantics** (paired grouped bootstrap, no reviewer): −0.051 [−0.130, −0.007] under step-level semantics (Table 4.10) and −0.043 [−0.122, −0.001] under episode-level semantics (`paired_differences`, episode-level REM − B1 entry). The idealized-reviewer interval under episode-level semantics is the same to three decimals. These are two within-semantics contrasts. No interval was computed for the difference between them, so none is reported. As for every interval in this chapter, the bootstrap over nine attacked groups need not reach nominal coverage, and no hypothesis test is based on these intervals (Section 4.2).

Step-level semantics remains the declared reference (Chapter 3, Section 3.8), pending the supervisor's decision D-2. The episode-level rows are a sensitivity analysis, not a replacement for Tables 4.9–4.12.

# Appendix F: Register of Open Supervisor Decisions

**No supervisor decision is recorded in the project repository.** Every item below is open. Where the thesis needed a wording, it uses the option marked "handling", labelled as pending. The full register, with options and effects, is kept with the project records (`SUPERVISOR_DECISIONS_REQUIRED.md` and the register of the five-chapter draft).

**Table F.1. Open decisions that determine what the thesis may claim**

| ID | Item | Handling in this thesis | Decision needed |
|---|---|---|---|
| SD-FREEZE | Approval of the Chapter 3 specification as frozen | Implemented as specified; values declared | Approve or amend |
| SD-FEAT | Feature set; **proposed amendment REM v1.1** (behavioral evidence removed) | v1.0 is the design; v1.1 is reported beside it as a confirmed ablation | Approve v1.1, or keep v1.0 |
| D-9 | Costs, tier map and predicates | Declared exploratory values | Approve, or elicit new values |
| SC-1 / D-2 | Mitigation semantics: step-level or episode-level | Step-level reference; episode-level in Appendix E | Confirm |
| SC-2 / D-4 | Tie rule | Chapter 3 order, with ties counted; no tie occurred in any run | Confirm |
| SC-3 | Calibration-removed ablation run in the evaluation path | Reported | Confirm |
| SC-4 / D-3 | Calibration fitting target: labels or Platt's smoothed targets | Both implemented; label fit is the reference | Confirm |
| SC-5 | Brier score convention | Binary convention reported, with the convention stated | Confirm |
| SC-6 | Layer label of the estimator in code comments | Decision Engine in the thesis; code comment differs | Confirm |
| SC-7 / D-1 | Recorded-trace replay against the original scope, which excluded replay-based estimation | Kept as a labelled NO-ADAPT analysis | Keep, drop, or replace by live runs |
| D-6 | Label rule; the user_task_15 collision; no human label audit | Rule kept; collision reported; audit package prepared, not annotated | Keep or redefine; audit |
| D-7 | Reviewer model for Escalate | Two bounds; headline results use no reviewer | Confirm |
| D-8 / SD-DET | Injection classifier of the Detection Layer | Absent; not replaced | Choose a classifier, or record its absence as final |
| D-10 | Wording of the research questions | Marked proposed | Confirm |
| D-12 | Thesis title | As supplied by the author | Confirm |
| D-15 | Live closed-loop experiment and the MELON comparison: backbone, decoding, repeats, budget, credentials | Not run | Authorize with a spending limit, or accept submission without them |
| SD-5 | Banking-only evaluation against objective O1, which also names task-automation agents | O1 achieved for banking only | Accept or extend |
| GAP | Research-gap wording of Chapter 2, Section 2.12.7 | Proposed wording | Confirm |
| RULES | Rule baselines P1, P2 and A2 as mandatory comparators | Included | Confirm |
| RG-1 | Authoritative equation registry | Missing; no equation identifier was created | Provide, or accept the provenance table of Appendix C |
| OI-01 to OI-06 | Statements about NEXUS | Abstract and repository documentation only; full text not read | Supply the full text |
| FULLTEXT | Full texts of aiAuthZ and Kairos; full-text screening of the systematic review | Abstract level; six papers read in full in November 2026 | Supply; decide on a full-text update |
| N-1, N-2 | Supervisor roles on the title page; faculty, department and degree | As in the latest instruction; not verified against official records | Confirm |
| N-3 | Arabic abstract and Arabic spellings of names | Draft translation | Review |
| N-6 | The co-supervisor is a co-author of one cited study (Kanaker et al., 2026) | Cited as a source only; evidence level stated | Decide whether a disclosure is required |
| N-8 | Committee page, declaration (including any declaration on the use of AI tools), dedication, acknowledgement | Placeholders | Complete with the university's wording |
| N-9 / TEMPLATE | University thesis template and formatting rules | **Not available**; an assumed A4 thesis layout is used | Provide; re-check the layout |

Smaller items (the Platt reference year, the regularization convention, one cell of the false-positive grid, and the optional sequential analysis) are listed in the project register and do not affect any reported result.
