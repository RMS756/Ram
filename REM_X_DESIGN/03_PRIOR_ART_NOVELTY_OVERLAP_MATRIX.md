# Deliverable 3: Prior-art novelty and overlap matrix

**Evidence levels for the prior systems:**

| System | Level | Notes |
|---|---|---|
| Progent | Full text (v3) and code (`0d7ea07`) | — |
| CaMeL | Code (`f083b6b`) | — |
| Fides | Repository (`669c046`, tutorial) and abstract | — |
| AgentCap | Abstract; search excerpt for the trust score | No code found |
| Agent-Sentry | Abstract | No code found |
| AIS | Abstract and Crossref record | — |
| RTBAS | Abstract | No code found |

Sources are listed in `REM_DEFENSE_IN_DEPTH/30–40`. **A cell is only as reliable as its level.** A full text could contain a mechanism its abstract does not mention. "Not determined" is written where the level read is silent.

**Cell values:** ✓ = present; ◐ = partial or analogous; — = not present (stated or evident at the level read); n.d. = not determined.

## 1. Mechanism × system

| REM-X mechanism | AgentCap | Agent-Sentry | AIS | Progent | Fides | CaMeL | RTBAS |
|---|---|---|---|---|---|---|---|
| M1 Field-level provenance / lineage | ✓ (provenance of sensitive arguments) | ◐ (argument provenance as classifier feature) | ◐ (evidence lineage) | — | ✓ (labels, taint) | ✓ (value sources, by construction) | ✓ (labels) |
| M2 Selective isolation of untrusted content | n.d. | — | — | — | ✓ (hiding primitives) | ✓ (quarantined LLM) | — |
| M3 Financial semantic analysis (typed economic terms) | n.d. | — | ✓ (typed financial action intent, exact economic terms) | ◐ (argument conditions if written) | — | ◐ (banking policy over typed arguments) | — |
| M4 Multi-step / tool-call sequence monitoring | ◐ (trust score from outcomes) | ✓ (learned bound over action sequences) | — | — | — | ◐ (control flow fixed by plan) | — |
| M5 Cross-call cumulative financial limits | ◐ (budget-bounded tokens; budget semantics n.d.) | — | ◐ (mandate and state checks) | — | — | — | — |
| M6 Intent-bound financial authorization | ◐ (declared intent; issuer n.d.) | — | ✓ | ◐ (task policies, LLM-generated) | ◐ (policies) | ◐ (plan from trusted query) | ◐ (confirmation) |
| M6′ Evidence-gated source delegation for untrusted financial documents | n.d. | — | n.d. | — | — | — (recipient must be trusted; code level) | ◐ (dependency screening; LM) |
| M7 Exact-action single-use capability | ✓ (short-lived, budget-bounded) | — | ✓ (single-use authority) | — | — | — | — |
| M8 Independent tool-boundary verification | ✓ (token validated at the tool) | — | ✓ (EVM enforcement) | ◐ (check at the tool call) | ◐ | ◐ (interpreter) | ◐ |
| M9 Atomic limit reservation | n.d. | — | n.d. (single-use authority) | — | — | — | — |
| M10 Post-execution verification and reconciliation | ◐ (outcomes update trust) | — | ✓ (replayable assurance; settlement record) | — | — | — | — |
| M11 Non-compensatory precedence (learned risk cannot loosen a denial) | n.d. | ◐ (judge only on residual) | ✓ (deterministic gate) | ✓ (deterministic) | ✓ | ✓ | ✓ |
| M12 Evasion-based failure-independence evaluation | — at level read | — (per-layer contribution not reported in abstract) | ◐ (mechanism ablations, removal) | ◐ (approver ablations, adaptive attacks) | n.d. | ◐ (no-policy variant, removal) | n.d. |

## 2. Questions a–e for each REM-X mechanism

| Mechanism | (a) Exists in prior work? | (b) Materially different integration in REM-X? | (c) New measurable security property? | (d) Reusable implementation | (e) Nature of difference |
|---|---|---|---|---|---|
| M1 Provenance / lineage | Yes (CaMeL, Fides, RTBAS, AgentCap) | No. REM-X infers lineage for a black-box agent, which is weaker than CaMeL's tracking | No | REM-DiD `provenance.py` (own); CaMeL capabilities (Apache-2.0) as reference | Operational, and weaker |
| M2 Selective isolation | Yes | No | No | CaMeL quarantined LLM; DRIFT isolator | — (not in the minimal set) |
| M3 Financial semantics | Yes (AIS) | Partly: deterministic extraction from **named documents**, used only for delegation | Only through M6′ | REM-DiD canonical forms (own) | Operational |
| M4 Sequence monitoring | Yes (Agent-Sentry: learned) | No. REM-X uses deterministic rules plus an optional advisory model | Only as a second covering control (DiD-3: 17 collision calls) | REM-DiD `behavior.py` (own) | Operational |
| M5 Cumulative limits | Partly (AgentCap budgets, AIS mandates; AGATE ledger and ScopeGate ceiling outside this list) | No, unless the full texts show none is cross-call and per-recipient | Yes, as a property *of REM*: split-transfer integrity. Not new to the field | REM-DiD TAE budget (own) | Operational |
| M6 Intent-bound authorization | Yes (AIS) | No | No | REM-DiD TAE / 4A (own) | Terminological, versus AIS's "financial action intent" |
| **M6′ Evidence-gated source delegation** | **Partly:** ROPE (outside this list) admits values from a user-named source; CaMeL denies them; RTBAS screens dependencies with an LM | **Possibly:** the conjunction of named-source delegation, deterministic extraction, injection-evidence gate on the delegated source, and economic caps. Not found at the level read | **Candidate:** delegated-document utility at zero successful attacks, including attacks injected into the delegated document | No existing implementation found; new code needed | **Architectural** if confirmed by full texts |
| M7 Exact-action capability | Yes (AgentCap, AIS) | No | No | REM-DiD `enforcement.py` (own) | Adopted |
| M8 Independent adapter check | Yes (AIS, AgentCap) | No | No | — | Adopted |
| M9 Atomic reservation | Standard in transaction processing; n.d. in agent systems | No (engineering) | Integrity under interleaved calls; not new | Standard two-phase pattern | Operational |
| M10 Post-execution reconciliation | Yes (AIS) | No | Execution assurance; not new | — | Adopted |
| M11 Non-compensatory precedence | Yes (deterministic gates everywhere; GuardRail outside this list) | No | No | REM-DiD `decision.py` (own) | Terminological |
| **M12 Evasion-based failure-independence testing** | Removal ablations exist (AIS, Progent, CaMeL); evasion-with-others-fixed not found at the level read | Yes, as an **evaluation requirement**, not a mechanism | **Yes:** resilience matrix; removal-vs-evasion disagreement (DiD-2: 11 vs 11 under removal, 653 vs 90 under evasion) | REM-DiD DiD-2/3 harness (own) | **Methodological** |

## 3. Conclusion of the matrix

| Category | Mechanisms |
|---|---|
| Adopted (not claimed) | M1, M2 (optional), M4, M6, M7, M8, M9, M10, M11 |
| Operational variants | M3, M5 |
| Candidate architectural differentiator | **M6′ only.** It depends on full-text checks of AgentCap, AIS and ROPE |
| Candidate methodological contribution | **M12** |

**REM-X cannot claim to be a new kind of architecture.** It can claim, if experiments confirm it:
1. that one specific integration (M6′) preserves utility on legitimate untrusted financial documents better than strict-provenance or parameter-provenance authorization, at equal security;
2. an evaluation method (M12).
