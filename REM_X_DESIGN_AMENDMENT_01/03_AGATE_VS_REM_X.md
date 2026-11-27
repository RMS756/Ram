# A1-03: AGATE versus REM-X, mechanism by mechanism

**Evidence.**
- AGATE (X. Zhang, Z. Cheng, K. Liu et al., 2026; arXiv 2609.30830 v1).
- Levels:
  - **A** = abstract, via the OpenAlex record W7214603931;
  - **S** = web-search excerpts of the full text (indirect; may be paraphrased).
- The full text exists on arXiv but **could not be read from this session**.
- **No code repository was found** by web search. One third-party issue only tracks the paper.

**Every "n.d." below means "not determined at A/S level".** It does **not** mean "absent from AGATE".

## 1. Requested aspects

| Aspect | What is known | Level |
|---|---|---|
| **Source registration** | "Source registration connects observed inputs to subsequent transfers." Matching method (exact, substring, transformed) is n.d. The paper names "content transformation" and "legitimate reuse" as limits of content-based provenance, which suggests value-level matching that transformations defeat | A; interpretation flagged |
| **Parameter-bound grants** | "Delegated actions are constrained by grants that bind to exact parameters, expire, and permit a limited number of uses." Grounded in "operator declarations and host approval events" | A |
| **Effect ledger** | "An effect ledger tracks repeated requests." S: it keeps **recent request keys per session**, with a nominal retention bound of 128 keys. Nothing found indicates summing of amounts or financial exposure | A; S |
| **Repeated-action detection** | Via the ledger's request keys, i.e. **deduplication or repetition detection of requests**. Behaviour after a denial is n.d. | A; S |
| **Cross-operation provenance** | Sequences of ordinary operations ("compositional attacks") are judged by combining authority and data origin across operations. The paper reports "replay agrees with live graph projections for all 63 scenarios on each of two platforms" (252 runs) | A |
| **Enforcement adapters** | Three production harnesses (DeepSeek Harness, OpenCode, OpenClaw) without modifying host code. The "judgment core is identical in all three, and only enforcement depth differs" | A |
| **Parameter rewriting** | "The deployment observations expose … a bypass through parameter rewriting." S: observed in business-tool workflows, with a mailbox-deletion case as the example; parameter rewriting is named as a challenge for content-based provenance. The exact mechanism of the bypass is n.d. | A; S |
| **Benign utility losses** | "Six of eleven benign file-processing scenarios contain denial events, revealing the utility cost of content-based provenance policies." S: authorization denials of 5, 5 and 11 under full, minimal and empty operator declarations | A; S |
| **Financial scenarios** | "Business actions"; no AgentDojo banking evaluation found; financial tasks n.d. | A |
| **Evasion or removal analysis of components** | n.d. (153 exercised attack-chain records; the deployment bypass is an observed failure, not a designed per-component evasion study) | A |

## 2. Cumulative monetary limits are not repeated-request deduplication

The task asks to keep these two apart. They are **different properties**, stated here in words:

| Property | What it prevents | What it does not prevent |
|---|---|---|
| **Repeated-request deduplication** (AGATE effect ledger, at A/S; idempotency in ScopeGate, at A) | The *same* request (same key) being executed again, e.g. a replayed payment | Several *different* requests that each look new, e.g. transfers with different amounts, subjects or dates to the same payee, whose total exceeds what the user intended |
| **Limited-use grants** (AGATE, AIS, AgentCap) | Using one authorization more times than allowed | Many separately authorized operations adding up |
| **Cumulative financial exposure limit** (REM-DiD TAE budget [DiD-T]; REM-X envelope [X-P]) | The total committed value, per recipient or per session, going beyond what the user declared | Any single transfer inside the limit that is itself fraudulent |

**For REM-X:**
- The split-transfer threat needs the third property. Deduplication alone does not address it.
- **This difference is not a novelty claim.** Cumulative limits are established in payments practice and named in prior agent work (AIS mandates at A; ScopeGate money ceiling at A; AgentCap "budget-bounded" tokens at A, with budget semantics n.d.).

## 3. Mechanism comparison

| Mechanism | AGATE | REM-X | Kind of difference |
|---|---|---|---|
| Authorization grounding | Operator declarations + host approval events | Trusted-UI authorization record (assumed channel) | Equivalent role; REM-X adopts it [PA] |
| Exact-parameter, expiring, limited-use grants | ✓ (A) | Single-use permits bound to canonical arguments [DiD-I] | Adopted [PA] |
| Source registration / provenance | ✓ (A); matching n.d. | Inferred lineage with canonical forms [DiD-I]; field-bound document extraction [X-P] | Possibly a refinement; cannot be judged without AGATE's matching rule |
| Effect ledger | Repeated-request keys (S) | Transaction ledger with reservations, permits and observed effects, plus cumulative exposure [X-P] | **Scope difference** (cumulative exposure vs repetition); both are established ideas |
| Parameter rewriting | Observed bypass | REM-X permits bind to the **canonical form of every argument**, and the adapter re-checks economic terms. Whether this closes AGATE's case **cannot be assessed** without its details | Unverified |
| File-processing denials | 6 of 11 benign scenarios with denials | REM-X would **escalate** rather than deny where a value is unverifiable (A1-04) | Converts denial into review; the utility gain depends on a reviewer |
| Enforcement adapters across hosts | ✓ three harnesses | One harness (AgentDojo) | AGATE is broader; REM-X is narrower and financial |
| Forensic replay | ✓ | Hash-chained audit [DiD-I] + reconciliation [X-P] | Adopted |
| Financial semantics | n.d. | Typed amount, recipient and envelope | Domain specialization; AIS is closer than AGATE here |

## 4. Precise research question versus AGATE [PD]

> For multi-step financial operations in which each individual request is distinct and authorized, does tracking cumulative committed and reserved value per recipient and per session prevent split-transfer exposures that request-level deduplication and limited-use grants do not, and at what utility cost?

**Feasibility.**
- AGATE's code is not available, and its harnesses are coding and business agents, not AgentDojo banking.
- An empirical AGATE comparison is therefore **not feasible as a reproduction**. It can only be:
  1. a **descriptive** comparison; or
  2. a clearly labelled **"deduplication-class" baseline**, built from the published description only, with every deviation listed.
- Option 2 requires the full text first (A1-09, C1).
