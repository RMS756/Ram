# Deliverable 8: Deterministic authorization and learned-risk decision (Layer 4)

**Code:** `remdid/decision.py`, `remdid/guard.py`, `remdid/tae.py`.

**Status:**
- 4A: implemented and tested.
- 4B: REM v1.0, unchanged and frozen.
- Precedence: implemented and tested; evaluated in DiD-3.

## 1. Four separate questions

| Question | Answered by | Kind |
|---|---|---|
| Is the action authorized? | 4A against the TAE | Deterministic, non-compensatory |
| Is there evidence of adversarial induction? | PROV (L1), DET (L2), BEH (L3) rules; 4B probability | Deterministic rules plus learned estimate |
| What is the consequence? | v1.0 consequence tier (declared exploratory tier map, amount limit 1,000) inside 4B | Declared |
| Which intervention? | Precedence over all of the above | Most restrictive wins |

**Injection probability is not consequence, and neither is authorization.** A call can have low p and still be unauthorized. In that case it is BLOCKED by P1 whatever p is (unit test `test_learned_allow_cannot_override_hard_denial`).

## 2. Precedence (declared before scoring, protocol commit 8678add)

| Rank | Condition | Verdict |
|---|---|---|
| P1 | Mandatory authorization denial: 4A VIOLATION, NO_ENTRY or UNVERIFIABLE (tampered, expired, reused, cross-session) | **Block** |
| P2 | Mandatory escalation: 4A UNSPECIFIED; mandatory input unavailable (TAE store, AUTH evaluator, PROV metadata, detector on the relevant segment, BEH monitor, 4B model) for a **state-changing** call, under fail-safe | Escalate |
| P3 | Deterministic evidence on a sensitive value that a verified TAE entry does **not** pin: PROV untrusted or missing lineage of an identity field, or untrusted amount; DET call-linked; any BEH rule | Escalate |
| P4 | 4B: REM v1.0 verdict (calibrated p, tier, expected loss; reachable verdicts as in v1.0) | As computed |
| — | **Final verdict = the maximum severity** (Allow < Modify < Escalate < Block) | — |

Notes on the precedence:
- **High-risk vs low-confidence evidence.** There is no confidence-weighted tier among the deterministic rules. All P3 evidence leads to Escalate, never Block, because each P3 signal has known legitimate firings (for example, bills come from untrusted files). Only authorization failures Block.
- **Variants.** `strict` consults 4B for every call. `pinned_release` skips 4B for calls whose sensitive fields are all pinned by a verified entry. Both are evaluated; **neither is adopted**.

## 3. Verdict semantics in REM-DiD

| Verdict | Meaning in REM-DiD |
|---|---|
| Allow | A permit is issued for exactly this call; the gateway executes it |
| Escalate | Withheld. Without a reviewer the call is not executed. With the idealized reviewer it is approved iff the reference label is 0, an upper bound on a perfect human |
| Block | Not executed |
| Modify | REM-DiD's rules never produce it: **no safe Modify mechanism is declared** (CLAUDE.md MITIGATION LOCK). A Modify from 4B keeps v1.0 semantics (withhold this call). **No operational benefit of Modify is claimed.** |

## 4. Cost structure and sensitivity

- **Costs:** 4B uses the exploratory declared losses of `configs/exploratory/pilot_e0.yaml` (C_FA = 1; C_miss by tier 1/5/10/20; C_mod 0.5; C_esc 0.3; declared 27 Oct 2026). No new cost value is introduced by REM-DiD.
- **Sensitivity:** a protocol over the **already-declared** grid is in `52_COST_SENSITIVITY_PROTOCOL.md`:
  - C_miss multiplier {0.5, 1, 2, 5};
  - C_esc {0.1, 0.3, 0.6};
  - amount limit {100, 1,000, 10,000}.

## 5. Does 4B add value behind 4A?

Measured in DiD-3 (B9 vs B9n vs B9p; `51_DID3_RESULTS.md`). This is the thesis's G5 question.
