# Parser candidate: review (opt-in, [PD], not adopted)

**Reported by Codex (not reproduced: the commit `bb4218d` is unavailable to this audit).**
- Primary: 11 / 2,979 attacks, 105 / 334 benign, and 1,087 utility under attack against 1,083 for the original: 6 episodes recovered and 2 lost, a net change of +4 / 2,979.
- The paired cluster CI for the difference crosses 0.
- User-task holdout: 12 / 2,979, 110 / 334, and 1,068 against 1,060 utility under attack.
- On the fresh fixtures the parser alone released the same calls as the original (2 legitimate `get_balance` calls, 0 unsafe).

## What this audit verified

1. **A real deviation exists in the frozen tokenizer (F-IMPL-1).** `_NUMBER` in `rem/algorithms/context/provenance.py:123` truncates comma-grouped decimals: "1,312.40" is read as 1312. This violates the declared matching rule. It is pinned by a strict-xfail test.
2. **The deviation explains two fixture outcomes**, SUB-A2 and P5: amount substitutions with no distinguishing feature.
3. **The deviation does not occur in the evaluation corpus.** A diagnostic complete-number tokenizer agrees with the frozen one on all 825 distinct objective and tool-output texts of the 3,313 eligible episodes.
   - **Therefore the reported corpus effect of the parser (6 recovered, 2 lost) cannot come from comma-grouped decimals.** It must come from another part of Codex's parser change: for example string amounts, Decimal equality, handling of tokens adjacent to punctuation, or numbers inside dates and identifiers.
   - That part could not be inspected. **The corpus-level parser result is unexplained by this audit.**
4. **The reported 6 recovered / 2 lost, net +4, and the CI including 0 could not be recomputed**, because Codex's per-episode outcomes are not available. The audit does not dispute the arithmetic: 1,087 − 1,083 = +4 and 6 − 2 = 4 are consistent.

## Interpretation

- **No detectable improvement.** With the CI crossing 0, the honest statement is "no detectable difference in utility under attack; attacks and benign successes unchanged".
- **F-IMPL-1 is an implementation defect.** Correcting it is still not "free": it changes x_act1 values and so the fitted model, which needs a refit, a newly exported and separately hashed bundle, and a re-run.
- **Correction is a supervisor decision, not a silent fix.** The fixed and unfixed systems are different evaluated systems.

## Disposition

- **[PD] opt-in candidate only.** It must not become the default.
- A refitted parser version requires its own exported bundle (never `983c5b0d…`).
- It needs a statement of exactly what changed, and an independent evaluation corpus before any claim beyond "exploratory".
- Before it is cited at all, Codex's diff must be supplied so that the cause of the 6 / 2 episode changes can be identified.
