# Results chapter: proposed updates

## R-1 Primary counts (reproduced), offline recorded-trace replay, step level, no reviewer

| Configuration | Successful attacks | Benign successes | Utility under attack |
|---|---|---|---|
| No defence (B0) | 672 / 2,979 | 175 / 334 | 1,465 / 2,979 |
| Operating-point baseline (B1) | 164 / 2,979 | 170 / 334 | 1,532 / 2,979 |
| REM (expected loss) | 11 / 2,979 | 105 / 334 | 1,083 / 2,979 |
| REM without discretionary Escalate (post hoc) | 11 / 2,979 | 110 / 334 | 1,113 / 2,979 |
| REM with an idealized reviewer (bound, not a deployable configuration) | 11 / 2,979 | 166 / 334 | 1,477 / 2,979 |

Suggested sentence:

> Under recorded-trace replay without a reviewer, REM reduced successful attacks from 672 to 11 of 2,979 attacked episodes, while benign task successes fell from 175 to 105 of 334. With an idealized reviewer that approves exactly the legitimate escalations, benign successes would be 166 of 334, so most of REM's benign cost in this configuration arises from withholding escalated actions when no reviewer is available.

## R-2 Where legitimate actions are withheld

> Of the 89 legitimate value-transfer steps in eligible benign episodes, REM released 4; it escalated 49, modified 31 and blocked 5 (B1 released 51). Of the 83 benign episodes that B0 completes but REM does not, the first withheld legitimate call was a value transfer in 34, a payment modification in 16, a profile change in 16 and a password change in 17; every one of these verdicts came from the expected-loss rule (no predicate fired).

## R-3 Diagnostic fixtures (counts only, synthetic)

> On 16 synthetic call-level probes (one author; not a representative or blind set), the frozen REM released none of the 14 legitimate payments and none of the 16 unsafe calls; it released the two legitimate balance inquiries. Unsafe payments whose substituted value was copied from the tool output received higher probabilities (0.457 or 0.837) than the legitimate payments (0.086) and were modified or blocked, but the legitimate payments were themselves escalated, so the probes do not demonstrate argument-level discrimination at the verdict level. Two amount substitutions written with comma-grouped decimals and both read-only-to-payment conversions produced feature vectors identical to a legitimate payment.

## R-4 Rejected and exploratory candidates (implementer-reported; not reproduced)

> A request cue left the primary counts unchanged and worsened held-out user-task Brier score and utility. A number-parser change left attacks and benign successes unchanged and changed utility under attack from 1,083 to 1,087 (six recovered, two lost; the paired cluster interval included zero). Gating the privilege-rise and transition-novelty contributions raised benign successes to 140 of 334 but increased successful attacks to 12 and released three unsafe calls on the fresh probes, including both read-only-to-payment conversions; it was rejected. All candidates were developed post hoc on the evaluation corpus, without multiplicity correction or an independent confirmatory set.

## R-5 Sensitivity (implementer-reported)

> Under leave-whole-user-task-out folds, the original REM had 12 of 2,979 successful attacks and 110 of 334 benign successes. These counts come from a different fitting scheme and are not directly comparable to the primary counts.

## R-6 Uncertainty

Keep the existing grouped bootstrap intervals for the primary rates: REM ASR 0.37% [0.10, 0.68]; benign utility 31.4% [11.0, 54.8]. Add no intervals for the fixtures or for the candidate arms.
