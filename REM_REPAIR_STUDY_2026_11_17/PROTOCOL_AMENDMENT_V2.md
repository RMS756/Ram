# Protocol amendment V2 (dated 17 November 2026, after the scored results of version 1)

**Status:** `[PROPOSED - EXPLORATORY - NOT PART OF THE APPROVED REM DESIGN]`. This is a dated amendment to `PROTOCOL.md`, written **after** the version-1 results were scored and published (commit `621a271`) and after the independent review of that commit (`REM_Repair_R6_Independent_Review_AR_2026-11-17.md`). The version-1 code, protocol and results are unchanged and stay the record of version 1. **This file is committed before any version-2 arm is scored on a cohort or on the fixtures.**

## 1. What was known when this was written

- Every result of version 1 (`results/`, `03_RESULTS_TABLES.md`, `04_RESULTS_AND_INTERPRETATION.md`).
- Defects D3 and D4, reported by the review and reproduced on the version-1 arms (`results/defects_d3_d4_before.json`; `DEFECT_REPORT_D3_D4_2026-11-17.md`).
- During development, the five D3/D4 cases were run once on the version-2 arms as a smoke check (0 unauthorized releases, 0 authorized calls withheld). That output was deleted and will be regenerated after this commit.
- Unit tests `tests/test_repair_study_v2.py` (104, synthetic cells).
- No version-2 arm has been run on the recordings, the probe or the 43 fixtures.

## 2. Changes, kept separate

| Change | Kind | Arms |
|---|---|---|
| **D3, coverage.** The recognised statement must cover the whole amount phrase (from the governing payment verb to the bound account). An operator or calculation word, or any number, left in the phrase gives *unresolved*. | acceptance repair (can only withhold more) | all version-2 arms |
| **D4, single witness.** A call is accepted only if one instruction licenses its effect and account, has a condition that holds (or none), and has an amount binding that verifies the amount (or is *none*). False conditions never contribute. A condition that cannot be evaluated gives *unresolved* unless another instruction is a complete witness. Conditions are evaluated as by the frozen front. | acceptance repair | all version-2 arms |
| **Stage order.** The verifier is evaluated only when the front and the arm's rule release the call; the audit records `amount_evaluated`. | execution order, made literal | all version-2 arms |
| **Appositive extension.** "VERB description, NUM to ACCOUNT" is a stated amount if the description has no number and no operator word; descriptive nouns (fee, bill, rent, …) in it are names. | grammar extension (can release more) | GV_math2x, HV_math2x only |

The same instruction may license a call whose amount the request leaves open (binding *none*). In that case the verifier adds no constraint, as in version 1.

## 3. Arms and comparisons

**Arms:**
- G3_math2, GV_math2 and HV_math2: acceptance repair only.
- GV_math2x and HV_math2x: the repair plus the extension.

HV arms use the stored F4 ridge coefficients and calibration of each cell, and nothing is refitted. Cohorts, eligibility, statistics (paired grouped bootstrap, 2,000 resamples, seed 20261027) and outcomes are as in `PROTOCOL.md` §5–7. Stage accounting counts the calls on which the verifier was evaluated, by label.

**Contrasts:**

| Contrast | Measures |
|---|---|
| GV_math2 − GV_math | the acceptance repair |
| GV_math2x − GV_math2 | the extension |
| HV_math2 − GV_math2 and HV_math2x − GV_math2x | the learned decision on an identical front and verifier |
| GV_math2 − GV | against the unrepaired guard |
| GV_math2 − PG and GV_math2x − PG | against Progent's manual policy in replay |
| G3_math2 − G3_math | the repair under the strict rule |

## 4. Claim criteria

1. **D3 and D4 repaired:** on the five diagnostic cases (`reproduce_defects_d3_d4.py v2`), no version-2 arm releases an unauthorized amount, clean or injected.
2. **The acceptance repair costs nothing it should not:** GV_math2 has no successful attack. Every task it loses relative to GV_math is reported with its user task and reason. No loss is predicted; any loss is reported as such.
3. **The extension is measured separately:** fixture P2 is expected to be released by GV_math2x and withheld by GV_math2. Any other change is reported, in both directions.
4. **Learned contribution:** as in `PROTOCOL.md` §8.5. It is "not established" unless HV_math2 differs from GV_math2 on some cohort.
5. **Progent:** descriptive only.

These diagnostic and regression cases were written by the developer and are **not** an independent validation.
