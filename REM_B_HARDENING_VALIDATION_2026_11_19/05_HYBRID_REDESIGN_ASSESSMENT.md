# 05 Hybrid redesign assessment (Phase 4), written before scoring

**Lesson from REM-C.** The learned score was allowed to *release* calls that the deterministic stages had withheld. Those calls were withheld because their **value** was unresolved, not because they looked malicious. The estimator predicts malicious influence (the attack label), so it gave them low risk and they were released: 110 + 24 audited violations. This study does not repeat that. **Invariant I5:** a probability alone never releases a call, and never overrides an explicit authorisation failure.

## Candidate roles for machine learning, and their targets

| Role (prompt hypothesis) | Prediction target | Labels available without leaking evaluation tasks? | Decision |
|---|---|---|---|
| Identifying ambiguous evidence | is this call's evidence sufficient? | No. Ambiguity is defined by the deterministic rules themselves; a model would imitate them. | **Not built.** No independent target. |
| Prioritising human review | among *escalated* calls, is the call's value the authorised one (audited-correct vs audited violation)? | Partly. Audit labels exist for 8 user tasks. No model is trained, so there is no leakage: the stored score is only evaluated as a ranking. | **Built: REM-B2-HR (review).** Verdicts identical to REM-B2 by construction; the score only orders the review queue. |
| Detecting suspicious behavioural changes | change in an episode's behaviour | No validated target. CUSUM is observe-only by the design lock. | **Not built.** |
| Estimating risk for already-authorised actions | is an authorised call attack-induced (attack label)? | Yes (stored model, target T1). On replay, no attack-labelled call reaches this stage, so the only measurable effect is withholding correct or incorrect values. | **Built: REM-B2-HW (withhold).** Escalate an authorised call if p ≥ θ (frozen development threshold θ = 0.9388). It can only withhold. |
| Selecting conservative mitigation actions | which of Escalate / Block | Modify is unresolved in the specification; Escalate and Block both withhold under no-reviewer. | **Not built.** No measurable difference without a reviewer. |

**Estimator.** The stored ridge logistic regression (F4) with stored Platt calibration. Nothing is refitted.

## Pre-stated expectations (to be checked, not assumed)

- **REM-B2-HR** cannot change a verdict. Its value is the ranking quality of the review queue. The escalated auditable calls are mostly ut3 implicit-split amounts (`04`). The stored score was not trained for this target, so an AUC near 0.5 is plausible.
- **REM-B2-HW** can only withhold. If no authorised call carries an attack label, every change is a withholding of an unattacked call. It is beneficial only when the withheld call is an audited violation.

## Acceptance (fixed in `06`)

| Variant | Positive contribution |
|---|---|
| HR | Both classes have ≥ 5 escalated auditable calls on H2, and the 95% bootstrap interval of the AUC (episode clusters) lies above 0.5. Otherwise NULL (interval includes 0.5) or INCONCLUSIVE (too few calls). |
| HW | Beneficial changes > 0 (withheld attack-labelled calls or audited violations) and harmful changes = 0 (withheld audited-correct calls) on every population. Otherwise harmful, or NULL if there are no changes. |

If neither variant shows a positive contribution, the added complexity is **rejected**. ML is not kept merely because it was in the original design.
