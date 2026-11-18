# 08 Learned component contribution (Phase 7)

**Learned stage.** Stored ridge logistic estimator on the F4 evidence, Platt calibration on the logit, then the frozen two-verdict expected-loss decision (Allow vs Block; Escalate and Modify excluded from the minimisation).
- It runs after the deterministic contract witness, and it can only withhold.
- No refit; scores are out of fold (each episode uses the stored S1 cell of its own fold).

Source: `results/ablation_results.json` → `learned_component`, `calibration_primary_S1_C1L`, `expected_loss_switch_points`.

## 1–3. Does it change verdicts, and are the changes good?

| Comparison (same recorded call sequence) | Population | Scores computed | Learned stage reached | Verdict changes | Beneficial | Harmful | Redundant |
|---|---|---|---|---|---|---|---|
| C1L vs C1 | primary S1 | 2,551 | 710 | **0** | 0 | 0 | 710 |
| C1L vs C1 | dev2 | 2,413 | 617 | **0** | 0 | 0 | 617 |
| C1IL vs C1I | primary S1 | 2,551 | 750 | 22 | **0** | **22** | 728 |
| C1IL vs C1I | dev2 | 2,413 | 783 | 79 | **0** | **79** | 704 |
| C3PG vs C2PG | primary S1 | – | 638 | 0 | 0 | 0 | 638 |
| C3PG vs C2PG | dev2 | – | 585 | 0 | 0 | 0 | 585 |

- **Every change in C1IL vs C1I withholds a call without an attack label.** All of them are E2 refunds to the single sender of the stated amount (learned probability 0.28–0.67). This costs 18 tasks (primary) and 79 tasks (dev2), with no attack removed.
- **Author-written suites.** The learned stage withholds 4 more authorised diagnostic proposals (C1L 46/62 vs C1 50/62) and 4 authorised generalisation proposals (C1IL 4/14 vs C1I 8/14). It withholds no unauthorised or ambiguous proposal that the deterministic arm releases.
- **Scripted closed loop.** C1L and C1IL behave like C1 (10/16 benign; same breaches). C1IL loses the ut15 refund that C1I recovers.

## 4. Is it evaluated where the deterministic guard leaves uncertainty?
**No.**
- All 907 attack-labelled restricted calls (primary) are blocked by the authority front **before** the learned stage. The 710 calls that reach it in C1L contain **0** attack-labelled calls.
- On that population the learned stage can only cost utility: there is nothing for it to catch.

## 5. Calibration (labelled outcomes; frozen implementations; 10 bins as declared)

| Set (primary S1, A5) | n | Positives | Brier | ECE (10 bins) | p range |
|---|---|---|---|---|---|
| All restricted calls | 2,551 | 907 | 0.0586 | 0.0239 | 6.5e-8 – 0.99999 |
| Learned-stage calls | 710 | 0 | 2.3e-6 | 0.00033 | 6.5e-8 – 0.0192 |

- **Calibration is good, but it does not translate into decisions.** The estimator is well calibrated on the full restricted-call population (out of fold). The calls it would act on, however, are already decided by the front.
- **The learned-stage numbers are uninformative.** On the learned-stage subset the ECE is tiny only because there are no positives and all scores are near 0.

## 6. Consequence-aware vs consequence-independent rule (same estimator)

**Switch points p\*.** The frozen two-verdict rule switches from Allow to Block at these probabilities, computed from the frozen engine's conditional risks (Elkan 2001):

| Tier | p\* |
|---|---|
| 2 | 0.1667 |
| 3 | 0.0909 |
| 4 | 0.0476 |

**C1L.** The maximum learned-stage score is 0.0192, below every p\*. Any consequence-independent threshold in (0.0192, 1] gives exactly the same decisions. The difference between consequence-aware and consequence-independent decisions is **not identifiable on these data**.

**C1IL.** The E2 refunds score 0.28–0.67, above p\*(tier 3). A single threshold below 0.28 would block them too; one above 0.67 would release them. Choosing such a threshold now would be post hoc, so no threshold arm was run. No frozen threshold exists for this estimator (the stored NP/CRC thresholds belong to other fits).

## 7. Runtime cost (primary S1, all calls)

| Arm | Median (ms) | p95 (ms) |
|---|---|---|
| C1 | 0.135 | 3.35 |
| C1L | 0.224 | 6.87 |
| C1I | 0.157 | 3.47 |
| C1IL | 0.214 | 6.96 |

The learned stage roughly doubles the p95 latency. It includes scoring every restricted call for this analysis.

## 8. Can simpler deterministic mechanisms do the same?
**Yes, on every population measured here.**
- The deterministic arm (C1, or C1I) makes every security decision the learned arm makes.
- The learned stage's only measured effect is to withhold legitimate refunds that the deterministic evidence-resolution step had recovered.

## Verdict on the learned component
- **NULL** on C1 (no decision change).
- **Harmful** on C1I (−18 / −79 tasks; 0 beneficial changes).

No claim that REM's learned decision improves security is supported by this evidence. The estimator itself is well calibrated. It adds value only if it is placed where the deterministic stages leave genuine uncertainty, which these populations do not contain.
