# 01: Framework classification: what each framework protects

**Protection targets:**

| Code | Target |
|---|---|
| T1 | Standalone LLM |
| T2 | LLM-powered application |
| T3 | RAG chatbot |
| T4 | AI agent |
| T5 | AI agent using external tools or MCP |
| T6 | Financial AI agent executing sensitive operations |

**Relevance to REM.** REM protects a tool-using banking agent (T5, with a T6 domain) against indirect prompt injection, at the tool-call boundary.
- **High:** protects T5 or T6 at or before tool execution.
- **Medium:** protects T2 or T3, or T5 by a mechanism REM cannot use as is.
- **Low:** protects T1 or T2 with output-level mechanisms.

Evidence levels are those of `09_REFERENCE_VERIFICATION.md`.

| # | Framework | Primary target | Where it intervenes | Relevance to REM | Basis (level) |
|---|---|---|---|---|---|
| 1 | **NEXUS** | **T5**: a monitor over a tool-using agent's structured plan, "before tool execution" | Plan / tool boundary | **High.** Closest analogue of REM's Decision Engine: deterministic rules, argument inspection, a calibrated logistic-regression risk score, four interventions | O, S, repository |
| 2 | **Progent** | **T5**: privilege policies over tool names and arguments | Tool-call boundary | **High.** Deterministic argument-level authorization; its manual banking policy was replayed on REM's episodes | F, R |
| 3 | **Agent-Sentry** | **T5**: bounds an agent's execution | Tool-call boundary | **High.** Combines a learned action-sequence classifier, argument provenance and a provenance-aware allow-list | O, S |
| 4 | **MELON** | **T5**: IPI against tool-using agents | After each tool turn, before the next action | **High** in threat model; **Medium** in mechanism. It needs a second LLM run and an embedding model per step | O, R |
| 5 | **CaMeL** | **T5**: redesigns the agent (privileged planner, quarantined parser, interpreter with capabilities) | Architecture + tool boundary | **High** conceptually. Its mechanism replaces the agent, which REM treats as opaque | R, S |
| 6 | **AgentDojo** | **T5 benchmark** with a banking suite (T6 tasks in simulation) | — (evaluation environment) | **High.** REM's evaluation environment | O, package and runs |
| 7 | **Intelligent Multilayer DiD (CMC 2026)** | **T2/T3** with agentic events: local LLMs in air-gapped networks, covering direct injection, RAG-based indirect injection and multi-turn bypass. Its inference layer observes retrieval queries, tool calls and action arguments | Five layers along the inference pipeline (per abstract) | **Medium.** A layered design grounded in MITRE ATLAS. Its trajectory signal compares the approved initial intent with observed events. Not a financial or tool-authorization system | C, O |
| 8 | **PromptGuard (Sci. Rep. 2026)** | **T1/T2**: an LLM's prompt-response pipeline | Input gatekeeping, prompt structuring, output validation, response refinement | **Low.** No tool-call or action control. Output refinement does not apply to financial actions | C, O, S |
| 9 | **Layered RAG chatbot framework** | **T3**: RAG chatbot | Input screening; provenance-based instruction hierarchy at context assembly; output audit | **Medium.** Its Layer 2 (retrieved content may not override operator policy) is a trust-boundary principle REM shares. No tool actions | O (arXiv version) |
| 10 | **CASCADE** (through its audit) | **T5 (MCP)**: tool descriptions, schemas and outputs | Rules → embedding similarity → optional local LLM review; allow / review / block | **Medium** for mechanism. **High for evaluation methodology:** the audit shows how decision conventions and corpus construction set the headline numbers | O (audit only) |
| 11 | **Spotlight-Guard** | **T4/T5**: LLM agents receiving tool content | Spotlighting isolation; LLM detection and quarantine; HMAC instruction integrity | **Medium.** Peer-reviewed layered IPI defense with a component ablation and an adaptive test. Content-side, not action authorization | O |
| 12 | **AIS** | **T6**: agents with financial authority | Execution authority: typed intent vs mandate, policy, state, approvals, exact economic terms; single-use authority; EVM enforcement | **High for the financial domain.** Separates model inference from execution authority | C, O, S |

**Additional works** (02 and 04 use them only where they add a mechanism):

| Work | Target | Relevance |
|---|---|---|
| ROPE | T5, AgentDojo banking | High (origin provenance, R level) |
| AgentCap | T5 | High (capability tokens) |
| AGATE | T5, business harnesses | Medium-high |
| ClawGuard | T5 incl. MCP | High (boundary rule set) |
| CapLite | T5 | High (request-stated authority) |
| SIEVE | T5 | High (deterministic first, escalate) |
| A-VIP | **T6**: payment agents (AP2) | High for finance |
| DEFER1 | Multi-agent T5 | Medium |
| BARBICAN, "Deletion is not substitution" | T5 (MCP gateway) | **High for ablation methodology** |

## Summary

| Group | Frameworks |
|---|---|
| **Designed to protect AI agents that use tools** | NEXUS, Progent, Agent-Sentry, MELON, CaMeL, CASCADE (MCP), Spotlight-Guard (agents receiving tool content); also ROPE, AgentCap, AGATE, ClawGuard, CapLite, SIEVE, DRIFT |
| **Agents executing financial operations** | AIS; A-VIP (payment protocol). AgentDojo provides the banking environment, and several agent defenses are evaluated on its banking suite |
| **General LLM / RAG security references only** | PromptGuard (T1/T2); the layered RAG chatbot framework (T3); the Multilayer DiD framework (T2/T3 with observed agentic events, an intermediate case) |

**A framework's layer count says nothing about its relevance.** PromptGuard has four layers and the RAG framework three, but none of them governs a tool call.
