# A1-01: Updated prior-art comparison matrix

**Scope.**
- Design-only amendment to `REM_X_DESIGN/03`. That file is kept unchanged as the historical record; this file supersedes it where they differ.
- Nothing was implemented or run. ROPE's published run logs were **read and tabulated as data**; no code from any repository was executed.

## 1. Evidence status (updated 27 Nov 2026)

**Levels:**

| Level | Meaning |
|---|---|
| F | Full text read |
| R | Repository code read (and, for ROPE, the authors' run logs read) |
| A | Abstract |
| S | Search-engine excerpt of the full text. Indirect, may be paraphrased; treated as a lead, not a quotation |
| C | Crossref record |

**Why full texts were not read.** Full texts of AGATE, AgentCap, Agent-Sentry and ROPE are publicly available on arXiv, and AIS on mdpi.com. They **are not readable from this session**: the web-fetch tool failed DNS resolution for `arxiv.org`, `www.mdpi.com` and `www.alphaxiv.org`.

**How to remedy this.**
- The saved environment `ram-thesis-research` allows `arxiv.org`, but this session cannot be moved onto it.
- No environment here allows `www.mdpi.com`.
- Full-text reading therefore remains an open condition (A1-09, C1). It is **not** a reason to describe these papers as abstract-only works.

| System | Version / identifier | Level now | Change since `REM_X_DESIGN/03` | Code |
|---|---|---|---|---|
| **ROPE** (Ma, Xiao, Yeoh, Zhang & Vorobeychik, 2026; arXiv 2608.27496; a v2 dated 19 Nov 2026 is reported by search) | Repository commit `ffe27c4` ("S&P release") | **R** (source, scope tables, run logs) + A + S | Added to the main matrix; mechanism-level analysis in A1-02 | **Public:** `github.com/xhOwenMa/ROPE`. Enforcement is deterministic; running the agent needs a live LLM (OpenRouter key) |
| **AGATE** (X. Zhang et al., 2026; arXiv 2609.30830) | v1 | A + S | Added to the main matrix; analysis in A1-03 | **None found** (web search; a third-party tracking issue only) |
| **AgentCap** (Kabbinamakki Suresh & Gao, 2026; arXiv 2611.00729) | — | A + S | S-level details added (trust score, utility under attack) | None found |
| **Agent-Sentry** (Sequeira, Damianakis, Iqbal & Psounis, 2026; arXiv 2603.22868) | v1 and v2 report different figures | A + S | S-level details added (provenance-aware allowlist) | None found |
| **AIS** (Gong, Samawi & Medda, 2026; *Systems* 14(10) 1329; earlier arXiv 2608.30519 with a different subtitle) | Journal version | C + A + S | S-level details added (replay and substitution results; reservation not integrated into the EVM gate) | Not determined |
| Progent | Paper v3, code `0d7ea07` | F + R | Unchanged | Public; bundles AgentDojo 0.1.29 |
| CaMeL | Code `f083b6b` | R | Unchanged. A copy is also vendored inside ROPE's repository (`agentlab/.../defenses/camel`), not compared | Public; needs an LLM |
| Fides | Repository `669c046` (tutorial) | R + A | Unchanged | Tutorial only |
| RTBAS | — | A | Unchanged | None found |

**Newly relevant sources (leads, not reviewed):**
- **AutoDojo** (arXiv 2606.15057), at level S. Reports a bill injection with **no explicit instruction sentence** that passed an injection detector and led the agent to pay the attacker. This bears directly on D1 (A1-04).
- **MAS "Safeguards for Agentic Finance at Runtime"** white paper v1.1 (Oct 2026), at level S. Regulatory guidance on bounded agent payment authority.
- Practitioner sources on invoice-borne IBAN substitution, at level S, **non-scholarly**: a blog post and two GitHub projects. They are cited only as practice evidence that independent payee-master checks are used.

## 2. Mechanism × system (main matrix, now including ROPE and AGATE)

**Cell values:** ✓ = present; ◐ = partial or analogous; — = not present at the level read; n.d. = not determined at the level read. Each cell carries its level.

| Mechanism | ROPE | AGATE | AgentCap | Agent-Sentry | AIS | Progent | CaMeL | Fides | RTBAS |
|---|---|---|---|---|---|---|---|---|---|
| Origin / provenance of sensitive arguments | ✓ R: origin labels on tool outputs; whole-token match of the argument value against admitted origins | ✓ A: source registration links inputs to later transfers | ✓ A | ✓ A/S: argument provenance in classifier and allowlist | ◐ A | — F | ✓ R | ✓ A | ✓ A |
| **User delegation to a named source** | ✓ R: `named_source` chosen by an LLM router reading only the request; admitted only for **structured** items whose `sender`/`from` field equals the named source | n.d. (operator declarations ground authorization, A) | n.d. | n.d. | n.d. | — F | — R (banking policy requires a trusted recipient) | n.d. | ◐ A |
| Treatment of **ordinary file bodies / web pages** | Untrusted, R: any unstructured tool output is labelled INJ | ◐ A: "content-based provenance policies" deny 6 of 11 benign file-processing scenarios | n.d. | ◐ S: secondary summary says arguments may trace to "descriptive fields in a retrieved file" (low confidence) | n.d. | — | Untrusted unless policy allows readers | Labelled | Labelled |
| Field-bound binding (argument tied to one field of one item) | — R: the check is a substring match against **any** string field of an admitted item | n.d. | n.d. | n.d. | ✓ A (typed intent fields) | — | ✓ R (value-level) | ✓ A | ◐ |
| Amount / economic-term control | — R: banking table guards **recipient only**. A `MAGNITUDE` marker exists in the code but checks only that the value is a number | n.d. | n.d. | n.d. | ✓ A: "exact economic terms" | ◐ F (if written) | — R | — | — |
| Cumulative monetary limits | — R | — at A/S: the ledger tracks **repeated requests** (S: recent request keys per session) | ◐ A: "budget-bounded" tokens; whether budget is monetary is n.d. | — | ◐ A: mandate. S: "reservation and consumption tracking is not integrated into the EVM gate" | — | — | — | — |
| Repeated-request deduplication | — | ✓ A/S | n.d. | — | ✓ A/S: token replays rejected | — | — | — | — |
| Exact-parameter, limited-use grants | ◐ R: router may pin a value (`CONST`/`ONEOF`); no use count | ✓ A | ✓ A: short-lived, budget-bounded tokens | — | ✓ A: single-use authority | — | — | — | — |
| Independent execution-side check | ◐ R: guard wraps `run_function` in the same process | ✓ A: adapters at host veto points; enforcement depth differs by host | ✓ A: validated at tool boundary | — | ✓ A: EVM verifier | ◐ | ◐ interpreter | ◐ | ◐ |
| Post-execution verification | — | ✓ A: forensic replay of decisions with execution evidence | ◐ A: outcomes update trust | — | ✓ A: replayable assurance, settlement evidence | — | — | — | — |
| Outcome on violation | **Deny** the call; error text returned to agent; no escalation channel, R | Deny (denial events), A | Deny, A | Block / LLM judge on ambiguity, A | Reject / withhold completion, S | Deny, F | Deny / confirm | Deny | Confirm (user), A |
| LLM in policy path | Router reads the request only; enforcement deterministic, R | None in decision path, A | n.d. | LLM judge on residual, A | Model-in-the-loop tests, S | Optional LLM policy generation, F | P-LLM plans; Q-LLM extracts | Planner | LM dependency screening |
| Evaluation on AgentDojo banking | ✓ R: logs for banking v1.2.2, three agent models, static and adaptive attacks | — (own harnesses) | ✓ A (AgentDojo, InjecAgent) | ✓ A (AgentDojo, AgentDyn) | — (own scenarios) | ✓ F | ✓ | ✓ | ✓ A |
| Per-component evasion analysis | ◐ R: policy-mode ablations exist (removal-style); evasion of one component with others fixed n.d. | ◐ S: bypass by parameter rewriting observed in deployment | n.d. | n.d. | ◐ A: mechanism ablations | ◐ F: adaptive attacks | ◐ | n.d. | n.d. |

## 3. What changed in the assessment

| Point | Before (`REM_X_DESIGN/03`) | After this amendment |
|---|---|---|
| D1's closest prior art | ROPE at abstract/README level | ROPE is now read at code level. Its named-source delegation **is** a deterministic, LLM-free admission of values from a user-named origin. It differs from D1 mainly in **what counts as a named source**: an authenticated structured sender in ROPE, a document in D1 (A1-02, A1-05) |
| Ordinary documents | Not examined | ROPE labels them untrusted, and in its own logs the bill payee is refused under all three agent models (A1-02 §4) |
| Cumulative limits | "n.d." for most systems | AGATE's ledger is evidenced (S) as **request deduplication**, not cumulative exposure. AIS's journal version states (S) that reservation is not integrated into its EVM gate. These are differences in scope, recorded at S level only |
| Novelty of D1 | "Candidate architectural differentiator" | **Downgraded** (A1-05): after the security reassessment (A1-04), the part of D1 that can be made safe largely coincides with ROPE's record/named-source admission plus REM's existing verdict semantics and economic limits |
