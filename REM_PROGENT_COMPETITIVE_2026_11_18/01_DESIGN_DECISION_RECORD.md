# Design decision record: REM candidates against full Progent (18 November 2026)

Status: `[PROPOSED - EXPLORATORY - NOT PART OF THE APPROVED REM DESIGN]`. Provisional experimental names; no new REM version is approved. The frozen REM v1.0 (`rem/`, frozen configurations), the scored arms, prior result files and the thesis editions R1–R7 are untouched.

## Context

- **Frozen v2 (repair study) still releases three unauthorized amounts in the diagnostics** (`results/f_before_v2.json`):
  - F1: a calculation suffix placed after the recipient escapes coverage (50 is "verified" where the request totals 60);
  - F2: a repetition allowance is borrowed from another instruction (a second 50 after "once").
- **F3:** the version-2 diagnostic scoring kept a correct total outside the "authorized" label.
- **The frozen front over-blocks.** The v1 compiler reads "twice" as a calculation cue and drops the amount. The front then contradicts a legitimate second instruction (F2b: 100 withheld).

## Decision

### Separate authority from amount and state
Four questions are answered by different, named components:
1. Is this operation on this account requested at all?
2. Does the amount equal what the request determines?
3. Does the instruction's own condition hold?
4. Is the instruction's allowance still available?

### Components (within the five REM layers; no sixth layer)

| Layer | Component | Source |
|---|---|---|
| Input & Context | request compiler (frozen revision-3 instructions with **stable ids** = compile order); typed amount bindings (frozen v1 grammar); **contract scope** (new, below); declared evidence-integrity rules | frozen `intent_v3`, `amount_verifier` (reused unchanged) |
| Detection | provenance and action evidence as before; in C3 the stored ridge estimator | frozen |
| Behavioral Analysis | **per-instruction execution ledger** (reserve on release; commit on a successful execution signal; release on refusal or execution error) | new |
| Decision Engine | authority front (revision 3 with `bind=False, fulfil=False`: the contract takes over amount binding and repetition); **single complete witness**; C2 adds a Progent policy check; C3 adds the learned decision, which may only withhold | frozen front reused; witness new |
| Mitigation | unchanged step-level semantics (Allow releases; Block and Escalate withhold; no reviewer) | frozen |

Policy governance (Progent's generation, update and subset check) is cross-cutting in C2 and C3. It is not a layer.

### Contract scope (repairs F1 without regressing S1 or P2)

The amount scope of a statement runs from its governing payment verb to the next payment verb that begins another instruction, or to the end of the sentence. **It does not stop at the account.** Inside the scope the following are removed:
- recognised statements;
- account identifiers, quoted text and the condition;
- dates and identifier numbers (invoice/order/id/ref + digits);
- repetition phrases (once, twice, N times) that the frozen compiler records as a count.

An **operator word** (plus, minus, additional, extra, more, less, total/totaling, add, including, excluding, difference, increase, decrease, discount, remaining, split, divide, times, twice, half, third, quarter, percent, %, +, −, ×, /) or a **stray number** left in the scope makes the instruction unresolved. Descriptive nouns (fee, bill, rent, share, …) are not operators. For example, "the annual fee" in S1 is a purpose description. Words before the governing verb are context, as in "my half of the bill, so send 27.35". Compound arithmetic is **not** supported, so a correct compound total stays unresolved, and that cost is counted as authorized work withheld.

### Duplicate instructions of one sentence

The frozen compiler can split one sentence into two instructions. For example, "Send 50 to X for order #123." yields a second instruction with an open target and the amount 123. Once the amount binding is attached to the account, both instructions describe the same payment. Contracts of the same sentence with the same effects, account, binding and condition are therefore merged: the bound target is kept, with the larger count and the smaller id. This keeps their allowances from adding up. (Found while inspecting the compiler output, before any scoring.)

### Witness (repairs F2 and keeps D4 repaired)

A call is accepted only if **one** contract matches all of the following at once:
- licenses the tool's effect;
- matches the account (its target, or its bound account when the target is open);
- has a condition that holds (or none);
- has an amount binding that verifies the amount (or states nothing);
- has **remaining allowance** = count − committed − reserved > 0.

The contract chosen for the call is reserved at release. A reservation is committed only on a successful execution signal and is released on refusal or error. A verified amount is preferred to an open one, then the lowest id. Values, conditions and allowances are never combined across contracts.

### Evidence integrity (declared)

Operands come from the trusted request or from two structured bank fields: an executed `get_balance` result, and the `sender`/`amount` fields of executed transaction records.

In AgentDojo banking v1 the attacker writes to injection vectors (file contents, transaction subjects, landlord notices), not to these fields. The harness therefore guarantees their origin. In a deployment this guarantee must come from the bank API. **It is an assumption, not a property of REM.** Free text is never an operand. Benchmark labels and evaluator state are never read.

## Arms

| Arm | Content | Status of its policy core in this session |
|---|---|---|
| P0 | full Progent: pinned upstream engine, LLM policy generation/update, Auto-Deny or Auto-Approve | adapter written; **not executed** (no model backend; running upstream code was refused in this session) |
| C1 | contract guard: front (`bind=False`, `fulfil=False`), contract scope, witness, ledger; no learner (`contracts.py`, `contract_arms.py`) | implemented; replayed |
| C2[PG] | C1 ∧ the manual banking policy of Progent's repository (REM's replay adaptation of its checker, cross-checked by an earlier review against upstream on 468 argument cases) | replayed; **not** C2 with generated policies |
| C2[gen] | C1 ∧ the upstream engine with LLM-generated and updated policies | adapter written; not executed |
| C3[PG] | C2[PG] + the stored ridge / calibration / two-verdict expected-loss decision (features from the frozen evidence, as trained) | replayed |
| references | REM v1.0, G3, GV, GV_math2, HV_math2, PG (stored) | stored |

**Attribution:**
- C2[PG] − C1 measures what Progent's manual policy adds to the contract.
- C2[PG] − PG measures what the financial contract adds to Progent's manual policy.
- C3[PG] − C2[PG] measures the learner.
- C2[gen] − P0 is the financial extension of full Progent; it needs a model and is not run here.

## Consequences known before scoring

- **The front still compares a stated literal.** With `bind=False`, the frozen front no longer applies the binding stage, but its typed base match still compares a stated literal amount. A wrong literal can therefore be blocked by the front (`permission_guard_authority_v3`) before the contract sees it. The two components agree on such calls; the audit records whichever acted first.
- **The front's condition check comes first.** With `cond=True`, the front withholds a conditional instruction whose condition cannot be evaluated before the contract does (D4 with an unread balance).
- **C2[PG] and C3[PG] reject unlisted accounts.** Progent's manual banking policy accepts only the AgentDojo recipients on its `trusted_recipient_list`. On synthetic accounts, these arms therefore withhold every payment. Their diagnostic rows say nothing about the contract; they are measured on the AgentDojo replay.
