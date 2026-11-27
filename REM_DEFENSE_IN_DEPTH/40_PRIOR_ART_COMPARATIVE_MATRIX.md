# Deliverable 1: Prior-art comparison and the origin of every REM-DiD mechanism

**This file extends files 30–36 with source-code inspection done in this session.**

**Code inspected (read only):**
- CaMeL `google-research/camel-prompt-injection` @ `f083b6b` (20 Jun 2025; a fetch on 27 Nov 2026 found no newer commit);
- Progent `sunblaze-ucb/progent` @ `0d7ea07`;
- Fides `microsoft/fides` @ `669c046`;
- AgentDojo 0.1.35 (installed package) and repository @ `089ed468`;
- ASB `agiresearch/ASB` @ `544540f` (cloned for this task).

**No public code was found** for RTBAS or AgentCap. A NeurIPS 2026 page, "AgentGate: Capability-Based Runtime Access Control for LLM Agents", has an abstract almost identical to AgentCap's. It may be a renamed published version. **This is unverified.**

**Full texts.** Apart from Progent v3 (read in full on 16 Nov), the papers are known at abstract or repository level, because arXiv is blocked in this session (file 30). **The CaMeL SaTML 2026 version could not be obtained, and its publication there could not be confirmed.**

**Evidence levels:** F = full text, R = repository code read, A = abstract, S = search excerpt, L = local package.

## 1. Comparative matrix

| | CaMeL | Progent | RTBAS | AgentCap | Fides | REM v1.0 |
|---|---|---|---|---|---|---|
| **Reference / status** | Debenedetti et al., arXiv 2503.18813 v2; preprint (SaTML 2026 not confirmed) | Shi et al., arXiv 2504.11703 v3; preprint | Zhong, Chen, Wang, McCall, Titzer, Miller & Gibbons, arXiv 2502.08966; preprint | Kabbinamakki Suresh & Gao, arXiv 2611.00729; preprint | Costa et al., arXiv 2505.23643; NeurIPS 2026 per Microsoft Research page | This thesis |
| **Security objective** | Untrusted data never alters control flow; data flows obey policies | Least privilege at each tool call | Integrity and confidentiality of tool calls with minimal confirmations | Authorization of model-proposed effects independent of the model | IFC guarantees for planners | Withhold injection-induced actions of a banking agent |
| **Threat model** | Trusted query; untrusted tool data (R) | Benign query; attacker controls observations (F) | Injection via tool outputs; privacy leakage (A) | Injection turns influence into unauthorized effects (A) | Injection; confidentiality (A) | Indirect injection; REM trusted |
| **Architecture** | Privileged LLM writes code from the query; quarantined LLM reads untrusted data; custom interpreter; policy engine per suite (R) | Policy DSL, LLM policy generation and update, SMT narrowing check, approver (F) | IFC labels, dependency screeners, confirmation (A) | MCP wrapper, policy engine, capability tokens, trust state (A, S) | Planner with labels and hiding primitives (A) | Five layers; learned expected-loss verdict |
| **Data provenance** | Sources on every value, propagated through interpreter dependencies (`get_all_sources`) (R) | None in the policy language (F) | Labels on tool outputs (A) | Provenance of security-sensitive arguments (A) | Integrity and confidentiality labels (A) | Segment labels; exact string matching |
| **IFC** | Data and control flow by construction; a state-changing call that depends on non-public values is denied (`check_policy`) (R) | No | Yes, adapted (A) | Not determined | Dynamic taint tracking (A) | No |
| **Detection** | None (R) | None (F) | Screeners judge dependency, not injection (A) | Not determined | None (A) | 6-pattern detector |
| **Behavioral monitoring** | None (R) | None (F) | Not determined | Per-agent trust score (S) | Not determined | History features |
| **Authorization** | Banking `send_money`: **recipient must be trusted** (user, CaMeL, assistant or trusted tool); amount, subject and date need only be readable by the recipient (R) | Allow/forbid rules over arguments; manual or LLM-written (F) | Auto-execute if integrity holds, else ask the user (A) | Intent per request; constraints; budget-bounded tokens (A) | Deterministic policies (A) | D1 prohibited tools only |
| **Decision mechanism** | Deterministic policy function per tool (R) | First-match, default deny (F) | Rule over labels and screener output (A) | Deterministic plus trust threshold (A, S) | Deterministic (A) | Calibrated p, tier, expected loss |
| **Enforcement** | Interpreter at tool call (R) | Tool call (F) | Before execution (A) | Token validated at the tool boundary (A) | Tool call (A) | Before the tool call (replay) |
| **Fail-safe** | Default deny if no policy matches (R) | Default block; fallback message (F) | Confirmation (A) | Revocation or sandbox (S) | Not determined | Gateway fail-closed; D2 escalation |
| **Adaptive attack** | Not determined | Yes (F, App. E) | Not determined | Not determined | Not determined | No (NO-ADAPT) |
| **Financial relevance** | AgentDojo banking policy written (R) | Banking pooled (F) | Motivation (A) | Not determined | Banking in per-suite tables (S) | Banking only |
| **Benchmark** | AgentDojo | AgentDojo, ASB, AgentPoison | AgentDojo | AgentDojo, InjecAgent | AgentDojo | AgentDojo 0.1.35 banking |
| **Strengths** | Guarantees for control flow and recipient origin, independent of model behaviour | Simple, auditable, deterministic; tested with adaptive attacks | Fewer confirmations than confirm-everything | Tokens make authorization checkable at the tool | Formal characterization of enforceable properties | Graded verdicts; calibrated, consequence-aware |
| **Limitations (stated or observed)** | Re-architects the agent (interpreter, two LLMs); a legitimately delegated recipient (a bill from a file) is denied unless trusted (observed in policy code); amount injection is not covered by trust (R) | Initial policy may exceed least privilege; no provenance (F) | LM screener reliability not established here | Who declares the intent is not determined | Agent re-architecture | Detector is a template fingerprint; over-blocking; exact matching |
| **Integration into REM (classification)** | **Adaptation:** value sources, field-level trust of tool outputs, and "recipient must have a trusted origin unless pinned" (L1 PROV rule). **Not adopted:** the interpreter and privileged/quarantined LLM split (would replace REM's black-box mediation) | **Adaptation:** deterministic argument-level authorization (4A) and default deny for unauthorized operations. **Not adopted:** the DSL and LLM-generated policies, because earlier REM studies found NL-derived authorization unreliable | **Inspiration:** dependency of arguments on untrusted inputs. **Not adopted:** LM screeners (no model calls) | **Inspiration:** short-lived, budget-bounded, session-bound permits validated at the tool (L5 gateway) | **Inspiration:** integrity labels | Baseline; kept read-only as 4B |

**Benchmarks (inspected).**
- **AgentDojo banking v1** (L, R):
  - 16 user tasks, 9 injection tasks, 11 tools, 4 injection vectors;
  - the vectors are a transaction `subject` field and three files: bill, landlord notice, address change;
  - attacks in the package: `important_instructions` and variants, `ignore_previous`, `direct`, `tool_knowledge`, `injecagent`, `system_message`, `manual`, DoS variants;
  - no currency or source-account parameter in any tool;
  - **user_task_15 authorizes the attacker's IBAN** as a new landlord, a benchmark collision.
- **ASB** @ `544540f` (R):
  - the finance scenario (`financial_analyst_agent`) has 5 tasks, 2 normal tools and 40 attacker tools;
  - **simulated tools take no arguments** (`parameters: None`) and return fixed strings;
  - attack success means calling an attacker tool by name.
  - **ASB therefore cannot exercise argument-level authorization, provenance or amount controls. It is compatible with REM only as a tool-name allow-listing test.** It was not used.

## 2. Origin of every REM-DiD mechanism

| REM-DiD mechanism (layer) | Original source of the idea | Classification | Status in this study |
|---|---|---|---|
| Field-level trust labels for tool outputs: free-text fields untrusted, typed bank fields trusted (L1) | CaMeL sources; RTBAS labels | Adaptation | Implemented and tested; evaluated in replay |
| Canonical value forms: IBAN separators, decimal amounts (L1) | Earlier REM extension studies (canonical provenance) | Implementation (REM's own) | Implemented and tested |
| Value lineage by canonical matching (L1) | CaMeL dependency tracking (true IFC); ProvenanceGuard evidence tracing | **Adaptation with weaker guarantee:** inferred co-occurrence, not tracked dataflow | Implemented and tested |
| TAE: pinned, unspecified and wildcard fields; HMAC integrity; session binding; expiry; uses; cumulative budget (L1) | AGATE grants, AIS single-use authority, AgentCap budget-bounded tokens, Progent argument rules | Adaptation; the combination is not claimed as novel | Implemented and tested; **trusted issuance is simulated by an oracle** |
| 4A non-compensatory authorization; default deny for unauthorized operations; "fields not in the entry may not change" (L4) | Progent default deny; CaMeL "no matching policy" deny | Adaptation | Implemented and tested; evaluated |
| Precedence "most restrictive wins; learned risk may tighten, never loosen" (L4) | GuardRail ordering statement (abstract) | Adaptation | Implemented and tested; evaluated |
| Evidence checks act only on values not pinned by verified authorization (L4) | — | **Original design decision of this study** (to be checked against full texts) | Implemented; evaluated (B9 vs B9p) |
| Detector diversity with explicit unavailability (L2) | Fail-safe defaults (classical) | Implementation | Implemented and tested; SIG-2 |
| Call-linked detection: the call's value occurs in a segment where a detector fired (L2) | ProvenanceGuard (evidence-supported calls) | Adaptation | Implemented and tested |
| First-payee, redirect, repeat, retry and switch rules (L3) | Banking fraud practice; AGATE effect ledger; ScopeGate idempotency | Adaptation | Implemented and tested; retry and switch are inert under NO-ADAPT |
| Parameter-bound, session-bound, single-use permits re-validated at the tool (L5) | AgentCap tokens; AGATE grants; GuardRail Action Passport | Adaptation | Implemented and tested |
| Hash-chained audit (cross-cutting) | MCP enforcement point, LATTICE (thesis Ch. 2) | Implementation | Implemented and tested |
| Bypass and failure-injection evaluation with remaining controls fixed | Evasion analysis of DiD-1/DiD-2 (this thesis) | **Candidate empirical contribution** (file 35 §4 checks pending) | Run in DiD-3 |
