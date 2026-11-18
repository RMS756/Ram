# 04 Improvement design (Phase 4)

Status: `[PROPOSED - EXPLORATORY - NOT PART OF THE APPROVED REM DESIGN]`.

This document and the pre-registered generalisation cases (`experiments/improvement_controlled/generalization_cases.py`) are committed **before** the candidate code exists. No new mathematical relation is introduced: both extensions evaluate the user's own stated expression, or select a record, using exact rational arithmetic and the frozen v2 binding semantics (equality; a rounding ambiguity stays unresolved). The expected-loss decision engine is unchanged.

## Candidate C1I = C1 + E1 + E2 (evidence resolution); C1IL = C1I + the stored learned stage

### E1 — explicit percentage of a past payment, plus an optional fee

| Item | Specification |
|---|---|
| Problem | ut11: "send them the difference of an additional 19.5% of the amount we paid + a fee of 5.29". The frozen calculation-cue rule makes the contract unresolved; 18 withheld calls carry the request's value (200.29). |
| Evidence | `03_FALSE_POSITIVE_ROOT_CAUSE.md`, rank 5 |
| Change in semantics | In a money instruction whose contract is unresolved by the calculation cue, an expression of the form `[the difference of] [an] [additional] P% / P percent of the amount (we\|I) paid [(+\|plus) [a fee of] L]` becomes a binding with value = P/100 × R + L. R is the amount of the **single** outgoing record (sender `me`) to the call's recipient account in an **executed** `get_most_recent_transactions` result, read from its structured fields. Zero or several such records → unresolved. Anything else left in the contract scope (operator word or stray number) → unresolved, as in C1. |
| Security assumption | The `recipient` and `amount` fields of executed transaction records are trusted. This extends the declared evidence-integrity assumption (which named `sender`/`amount`) to `recipient`. Free text (file contents, subjects) is never an operand. |
| Expected utility effect | Recovers explicit expressions such as ut11 (≤ 18 replay calls). It does **not** cover implicit phrasing (ut5 "prices increased 10% … the difference", case G5), which is expected to stay withheld. |
| New attack surface | An attacker who can create an outgoing record to their own account (i.e. has already been paid) and inject a request with such an expression. The expression must come from the user's request, so injected text cannot supply it. An agent paying the wrong account is still stopped by the front. |
| Tests | G1–G6, unit tests of the parser and of record selection |

### E2 — refund recipient from the trusted record with the stated amount

| Item | Specification |
|---|---|
| Problem | ut15: "refund that 10.00 I just got from my friend". No account is stated, so the front cannot establish authority; 22 withheld calls carry the request's value. |
| Evidence | `03_FALSE_POSITIVE_ROOT_CAUSE.md`, rank 4 |
| Change in semantics | A refund sentence of the user's request that states an amount L, names no account, and says the money was received (`got`, `received`, `sent me`) licenses **one** `send_money` of exactly L to the account S, where S is the sender of the **single** incoming record of amount L in an executed `get_most_recent_transactions` result. Zero or several such records → not licensed. The license is a contract with count 1 in the C1 ledger. It applies only when the front has not established authority; every other stage (predicates, Progent policy if present, learned stage if present) is unchanged. |
| Security assumption | The `sender` and `amount` fields of executed transaction records are trusted (already declared). |
| Expected utility effect | ut15 refunds (≤ 22 replay calls); the scripted benign ut15 if its other calls are released. |
| New attack surface | A payment of the same amount from an attacker's account to the user, followed by the user's own refund request, would make the attacker the refund recipient. This is the classic refund scam, and uniqueness only reduces it. The license cannot be created by injected text, because the refund sentence must be in the user's request (case R5). |
| Tests | R1–R6, unit tests |

### What was considered and not implemented
- **Relaxing the calculation cue wholesale.** Rejected: about 83 wrong amounts would be released (`03`).
- **Trusting file contents.** Rejected: the files are injection vectors.
- **Auto-approving subjective conditions.** Rejected: that needs a reviewer, and the study has none.
- **Object binding for standing-order modifications** (`02` order-dependence finding). Not designed here: it needs an analysis of whether scheduled-transaction subjects are attacker-writable.

## Acceptance and rejection criteria
They are fixed in `05_FROZEN_EXPERIMENT_PROTOCOL.md`, which is committed before any scored run.
