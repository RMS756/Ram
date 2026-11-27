# A1-08: Updated research contribution statement [PD]

**Status.**
- Proposed wording only. It supersedes `REM_X_DESIGN/09`.
- The thesis is not edited.
- **Nothing here is claimed as established.** Every bracketed part is filled only from a frozen, executed protocol.

## 1. Withdrawn from the earlier statement

| Withdrawn | Reason |
|---|---|
| "Its specific contribution is evidence-gated source delegation …" | D1 in that form is unsafe (A1-04). In its safe form it is an implementation variant of ROPE-style origin delegation (A1-05) |
| "The document carries no detected injection" as part of an admission rule | Detector silence is not evidence of authenticity |
| "Proposes and applies an evaluation method …" presented as a contribution | Removal-versus-evasion testing is a methodological practice without established novelty (A1-10) |
| "At equal security, including attacks injected into the delegated documents" | Not achievable without independent payee references; security under review depends on the reviewer |

## 2. Defensible at the present design stage

1. The REM v1.0 statement, unchanged: the evaluated five-layer framework, the frozen pipeline, and the thesis results.
2. **REM-DiD findings** (exploratory; NO-ADAPT replay; oracle authorization). Each is stated with its limits:
   - behind oracle authorization, the learned decision added no security in the declared cost grid;
   - with authorization bypassed, the evidence controls together stopped the replayed attacks but were largely redundant;
   - removal and evasion gave opposite conclusions on one REM component family.
3. **A design analysis** (this amendment):
   - origin-based delegation as released in ROPE refuses document-derived recipients and does not guard amounts in banking (code and the authors' logs);
   - detector silence cannot justify admitting document-derived financial values;
   - a design that admits such values must rest on independent payee references, declared economic limits and review.

   **This is analysis, not an experimental result.**

## 3. Conditional statement (only if a frozen comparison is executed)

> *REM-X adopts established mechanisms — origin and field provenance (ROPE, CaMeL, Fides), exact-parameter single-use authorization and execution-side verification (AIS, AgentCap, AGATE), and declared economic limits (AIS, ScopeGate) — inside REM's five-layer architecture and four-verdict semantics.*
>
> *On [suite, version, phase], compared under identical traces with ROPE as released [and other arms], REM-X [did / did not] change the outcome on document-derived payment tasks:*
> - *automatic completion: [result];*
> - *completion under review: [result];*
> - *successful attacks with structurally valid forged fields: [result];*
> - *bounded exposure on amount manipulation: [result].*

**This is an empirical comparison, not a mechanism novelty claim.** If no difference is detected, that is the reported result.

## 4. Not claimed

- Novelty of:
  - delegation;
  - provenance;
  - capability or permit;
  - ledger;
  - reconciliation;
  - cumulative limits;
  - evaluation method.
- Superiority over any system not run under identical conditions.
- Adaptive-agent robustness from replay or from the scripted agent.
- Zero successful attacks for document-derived payees without independent references.
- Any new equation, score or threshold (A1-11).
