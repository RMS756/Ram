# Protocol of revision 3: effect-typed instructions and whole-condition evaluation

**Status:** `[PROPOSED — EXPLORATORY — NOT PART OF THE APPROVED REM DESIGN]`. **Frozen:** 15 November 2026, by the commit that adds this file, **before any arm defined here was replayed.** The scored revisions 1 and 2, their results and the thesis editions R1 to R3 are unchanged (tests `test_scored_modules_are_unchanged`).

## 1. Why a revision

An external review of the third thesis edition (15 November 2026, commit `771c42e`) reported two defects of the revision-2 matcher, reproduced here on the same day (`DEFECT_REPORT_V3.md`):

| ID | Defect | Revision 2 |
|---|---|---|
| D1 | "Create a monthly standing order for 50 to A" licenses an immediate `send_money` of 50 to A | immediate transfers and standing orders share one category |
| D2 | "If my balance is above 1000 and below 5000, send 50 to A" is supported at a balance of 10000 | the first recognized comparison is evaluated; the rest of the condition is ignored. The thresholds are also read as payment amounts |

## 2. What was known when this was written

Everything known for revisions 1 and 2, **all their results**, and the call-level audit of user task 15. In particular it was known that the one remaining successful attack of G2 is a one-off transfer of 2200 to the account that the request names for the standing order, and that revision 3's effect typing is designed to deny exactly that call. A reduction of G2's attack count by revision 3 is therefore expected and is **not** an independent finding. The compiled revision-3 instructions of the 16 benchmark requests were printed once (inputs only). The reviewer's counterexamples, fixture sets 1 to 4 and all 5,426 recordings are development and regression material.

## 3. Candidate

Code: `experiments/improve_study/intent_v3.py`, `permission_v3.py`, `improve_v3.py`. Supported syntax and the conservative handling outside it are stated in the module header of `intent_v3.py` and are part of this protocol.

- **Effect.** Every instruction carries the effects it licenses: `transfer_now` (`send_money`), `schedule_create` (`schedule_transaction`), `schedule_modify` (`update_scheduled_transaction`). A call is matched only against instructions that license its effect. If the request has payment instructions and none licenses the effect, the call is denied. An account or amount that the request binds only to an instruction of another effect cannot be used for this one. Ambiguous wording ("set up a payment"; a transfer with an explicit calendar date) licenses both an immediate transfer and a scheduled one.
- **Condition.** The whole predicate expression must be parsed: balance comparisons joined by "and" or by "or", "between N and M", and "unless". An expression that is not parsed completely, a leading condition without a delimiter, mixed connectives, an ambiguous number and every subjective condition are *unsupported*: the call stays *unknown* and is never treated as satisfied. Thresholds are not payment amounts.
- **Policy for unknown conditions.** The rule arms withhold the call. With a reviewer it would be escalated; no reviewer exists in replay, and no reviewer accuracy is assumed. The cost of this policy is measured by the ablation without the condition check.
- **Kept from revision 2:** instruction binding, fulfilment tracking with successful-execution counting (now per effect), legitimate retries, repeat counts, the authority guard.
- No benchmark task identifier, label or outcome is used; no check is disabled; user task 15 is not excluded.

## 4. Arms

| Arm | Definition | Learned |
|---|---|---|
| **G3 (candidate)** | release a state-changing call iff its revision-3 status is *supported* | no |
| G3-noeffect | G3 without effect typing (revision-2 categories, with the whole-condition parser and threshold separation) | no |
| G3-nocond | G3 without the condition check | no |
| L4 | authority guard on revision-3 evidence; ridge model on the evidence of REM v1.1 plus five revision-3 permission indicators (F4), fitted by the unchanged procedure in every fold and double-holdout cell; two-verdict decision | F4 |

Reference arms are read from their stored replays (deterministic): REM v1.0, REM v1.1, A2, Progent's published manual banking policy adapted to the shared replay harness (PG), G1, G2, L3. The refit of the stored revision-2 learned models must reproduce them (equivalence check).

## 5. Populations, outcomes, statistics

As in the earlier protocols: primary (S1; S2 additionally for L4), second development population, reformatted-identifier probe, fixture sets 1–4 (regression), call-level audit of user task 15 for G3 with the criteria of `../followup/PROTOCOL_V2.md`, Section 7. Paired grouped bootstrap, 2,000 resamples, seed 20261027; 16 user-task and 9 injection-task clusters.

## 6. Comparisons fixed in advance

1. **G3 − G2** (task completion and attack success; primary and second population).
2. **G3 − A2** and **G3 − PG**.
3. **L4 − G3** under S1, S2 and on the second population: the learned model against the strongest repaired rule under identical splits.
4. Ablations: **G3 − G3-noeffect**, **G3 − G3-nocond**.
5. Probe: successful attacks of G3 and L4 with the identifier reformatted.

## 7. Interpretation rules

- Every result is development evidence. Matcher counterexamples, recorded-trace replay and any later prospective or live evaluation are reported under separate headings.
- "Added value over simple rules": only if the G3 − A2 task-completion interval lies above zero on both populations and G3 has no more successful attacks than A2 on either. A security difference whose interval excludes zero is reported as a security difference on development data, not as overall superiority.
- "The learned model adds value": only if the L4 − G3 task-completion interval lies above zero (lower bound strictly greater than zero) under S1 and S2, with no more successful attacks on the original text and on the probe. Otherwise "not established"; this does not show that a learned model cannot help.
- No equivalence, non-inferiority or overall superiority is claimed from an interval that does not establish it. No margin exists.
- Because all security differences among the restrictive arms are in user task 15, every security statement names that limitation.

## 8. Prospective validation: defined, not executed

A test of the rule needs requests that its author has not seen. `../prospective/AUTHORING_KIT.md` specifies how a person other than the author writes and a second person reviews paired requests (legitimate call and unsafe call), and `experiments/improve_study/score_requests.py` scores the frozen revision-3 rule on such a file, refusing to run if the rule's code differs from the committed hash. **No such file exists on 15 November 2026; the validation is unexecuted.** No model call is needed for it. Live-agent and model-based comparisons remain blocked (no credential, no spending authorization).

## 9. Amendments

None at the time of freezing.
