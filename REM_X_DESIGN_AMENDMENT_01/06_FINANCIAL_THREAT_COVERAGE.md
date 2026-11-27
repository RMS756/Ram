# A1-06: Revised financial threat-coverage matrix

**What this file changes.**
- Supersedes `REM_X_DESIGN/04` §2.
- The DELEG column now means **revised D1 (A1-04)**. A document can only propose a value; detector silence is never a release condition.

**Status.** Every cell is a **design expectation [X-P]**, not a measured result.

**Cell values:**

| Value | Meaning |
|---|---|
| P | Primary control |
| S | Secondary control |
| B | Bounds the loss but does not prevent it |
| R | Depends on a reviewer |
| — | None |

**Inputs:**

| Code | Control | What it reads |
|---|---|---|
| AUTH | Authorization | The authorization record |
| REF | Independent payee reference | Records, directory, pins |
| DELEG | Delegation | Field-bound extraction plus uniqueness |
| PROV | Provenance | Lineage |
| DET | Detection | Text |
| BEH | Behaviour | Actions |
| LEDGER | Ledger | Cumulative state |
| ENF | Enforcement | Permit plus adapter |
| RECON | Reconciliation | System of record |

**Independence requirement.** The original requirement "at least two independent controls per threat" was a **number I introduced**; A1-11 flags it. It is restated here **in words**: a threat class should not depend on a single control, or on controls that read the same input. The required number of controls is a **supervisor decision**.

## Matrix

| Threat | AUTH | REF | DELEG | PROV | DET | BEH | LEDGER | ENF | RECON | Comment |
|---|---|---|---|---|---|---|---|---|---|---|
| Beneficiary substitution via injected instruction | P | P | S | S | S | S | — | — | S | Several distinct inputs |
| Fake IBAN in a valid-looking document field | P (if pinned) | **P** | S (binding only) | — | **—** (no instruction) | S (new payee) | B | — | — | **Without REF and a pin: R.** Detection gives no coverage |
| Modified amount in a genuine document | S (envelope) | — | — | — | — | — | **B** | S (adapter re-check of envelope) | S | **Bounded, not prevented.** Exact amounts can only be checked when the user states them |
| Duplicate beneficiary fields / conflicting amounts | — | — | **P** (ambiguity → Escalate) | — | — | — | — | — | — | Single control. **Weak**: depends on parser correctness |
| Instruction-free data manipulation | P (if pinned) | P | S | — | — | S | B | — | — | DET does not apply |
| Unicode or formatting obfuscation of an account | P (canonical compare) | P | P (non-canonical → ambiguous) | S | — | — | — | S | — | Needs a published confusables reference [DESIGN BLOCKED] |
| Document structure mimicry | — | P | P (duplicate) | — | S (if instruction text present) | S | B | — | — | — |
| Malicious document from a source the user named | — | **P** | S | — | S | S | B | — | — | **Without REF: R.** Naming a source is not integrity evidence |
| Correct extraction from compromised content | — | **P** | — | — | — | — | B | — | — | As above |
| Amount escalation to a trusted recipient | P (envelope / exact) | — | — | — | — | — | P | S | S | ROPE's banking table does not cover this (A1-02) |
| Split transfer under limits | P (budget) | — | — | — | — | S | **P** (cumulative) | S | — | Deduplication alone does not cover this (A1-03 §2) |
| Repeated or replayed request | P (uses) | — | — | — | — | P | S | P (single-use) | — | — |
| Tool switching after denial | P | — | — | S | S | P | — | — | — | — |
| Recurring-payment redirection | P | P | — | S | S | P | — | — | S | — |
| Collision (attacker value in the user's own request) | — (authorized) | — | — | — | — | P | B | — | — | **Residual risk**: single control plus bound |
| Exfiltration through payment subject | S (if pinned) | — | — | S | S | — | — | — | — | **Weak.** A subject rule needs a design decision |
| Policy-engine failure | fail-safe | — | — | — | — | — | — | P | — | — |
| Adapter or tool deviation | — | — | — | — | — | — | — | P | P | — |

## Summary

- **The document-delegation classes are covered in two ways only:**
  - (a) an independent payee reference or a pin;
  - (b) a reviewer.

  Without (a) they rely on (b). **No claim of autonomous protection for these classes is made.**
- **Amount manipulation is bounded by declared limits, not prevented,** unless the exact amount is pinned.
- **Classes with a single control** are listed as residual risks, not as covered:
  - duplicate or conflicting fields;
  - collision;
  - subject exfiltration.
