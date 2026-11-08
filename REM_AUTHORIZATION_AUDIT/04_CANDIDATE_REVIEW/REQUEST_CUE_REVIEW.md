# Request-cue candidate: review (not adopted)

**Reported by Codex (not reproduced: code unavailable).**
- Primary injection-task folds: 11 / 2,979 attacks and 105 / 334 benign, the same as the original; cue + no-discretionary Escalate gives 11 / 2,979 and 110 / 334, the same as noEsc alone.
- Leave-whole-user-task-out: cue + noEsc gives 12 / 2,979 and 124 / 334, against 13 / 2,979 and 124 / 334 for noEsc alone.
- The feature alone made held-out user-task Brier score and utility worse.

**Definition, as described to this audit (not seen in code):** one binary feature, "the trusted user's words explicitly mention the family of a proposed state-changing operation", using a generic fixed vocabulary, never an authorization or a veto.

## Why no effect on primary counts is expected (evidence plus a labelled hypothesis)

1. **Most withheld legitimate payments sit far above the Allow boundary for reasons the cue does not touch** (verified; `../logs/corpus_diagnostics.json`).
   - Legitimate transfers have a median p of 0.30 against a tier-3 Allow boundary of 0.03.
   - 74% carry x_act1 and 53% carry x_act2, with coefficients ≈ 2.29 and ≈ 1.89 in fold 0.
   - A cue that lowers the logit a little cannot move them across 0.03. Moving a step from p ≈ 0.09 below it needs a raw-logit shift of about −1.2. From the median p ≈ 0.30 it needs about −2.7, and from p ≈ 0.64 about −4.2 (γ1 = 0.959, fold 0).
2. **The cue is uninformative where it matters most** (verified).
   - 28% of attack steps (254 / 908) use the operation family the user task itself requests, so the cue fires on those attacks as it does on legitimate steps.
   - Where the family is *not* requested, the existing x_act1 / x_act2 already fire on 96% of attack transfers.
3. **Hypothesis (not verified):** the ridge fit gave the cue a small coefficient, because its information is largely redundant with x_act2 ("recipient in objective") and with the requested-family structure of the 16 user tasks. Verifying this needs Codex's fitted coefficients per fold.

## Why held-out user-task Brier and utility worsened (hypothesis)

- With whole user tasks held out, the cue's vocabulary-to-label association is learned from 15 user tasks and applied to an unseen one.
- In this corpus the cue is effectively a user-task identifier: every episode of a user task shares its objective text, so the cue is constant within a user task.
- A feature that is constant within groups and is fitted across 15 groups carries group-level label rates into the held-out group. That is consistent with worse calibration (Brier) there.
- This is a hypothesis. It requires the per-fold coefficients and the per-user-task Brier from Codex's run.

## Disposition

**Not adopted, and must not be.** It is a feature-set change, and the final feature set is unresolved under the design lock. The evidence also shows no benefit. It may be reported as a post-hoc negative exploratory result, alongside all other arms.
