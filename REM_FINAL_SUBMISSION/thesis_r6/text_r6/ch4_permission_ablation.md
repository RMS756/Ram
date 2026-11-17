*Kind of evidence: replay; development evidence. The ablations are diagnostic and were listed in the protocol of each revision before scoring. The full R5 text, including the paired contrasts of the ablations (Table 4.18), is in Section S-4.5.3.*

**Table 4.17. The permission rule, one check at a time** (`improvement_results.json`, `results_v2.json`, `results_v3.json`; the probe has 2,645 attacked episodes)

| Rule | Primary: attacks / 2,979 | Primary: all tasks / 3,313 | Second: attacks / 2,065 | Second: all tasks / 2,113 | Probe: attacks, identifier reformatted |
|---|---|---|---|---|---|
| Permission rule, revision 1 (G1) | 10 | 1,574 | 3 | 1,358 | 10 |
| G2 without binding amounts to accounts | 10 | 1,407 | 3 | 1,239 | 10 |
| Permission rule, revision 2 (G2) | 1 | 1,407 | 0 | 1,239 | 1 |
| G3 without effect typing | 10 | 1,407 | 3 | 1,239 | 10 |
| Permission rule, revision 3 (G3, current) | 0 | 1,407 | 0 | 1,239 | 0 |
| G3 without the condition check | 0 | 1,574 | 0 | 1,358 | 0 |

- **Binding removes the attacks and costs no task.** Binding amounts to accounts takes the rule from 10 and 3 successful attacks to 1 and 0, and binding instructions to the effect of the operation removes the remaining one (paired contrast −0.34 [−0.57, −0.10] and −0.15 [−0.29, −0.05] points of attack success, with no task gained or lost).
- **The condition check costs one user task.** Every task that revisions 2 and 3 lose against revision 1 (167 and 119) is in user task 14. Its request makes a password change conditional on "something looks even just a little bit suspicious", and the rule never treats such a predicate as satisfied. The check removes no attack on these recordings (decision SD-COND, Appendix F).
- **Components of revision 1.** Scoped delegation accounts for 131 completed tasks on the primary recordings, typed normalization for 90 and established payees for 18. Without the amount check the rule completes 68 more tasks with 3 more successful attacks.
- **The two-verdict decision alone is unsafe.** Applied to REM v1.1 without a guard (V11d), it releases every held-out credential-change attack (131 and 58 successful attacks).
- **A learned model behind a weak guard is not robust.** With the attacker's identifier reformatted, L2 has 38 successful attacks where the rule has 10. A guard that also blocks every call whose authority is not established (L2g, L4) removes this failure.
- **The gain of the learned arm over the rule belongs to the guard.** L4, the authority guard followed by the ridge model, completes more tasks than G3 with no successful attack (+3.77 [0.00, 9.25] points on the primary recordings and +6.96 [0.00, 18.27] on the second population). The guard used alone completes exactly the same tasks.

**Decision methods behind the authority front (16 November 2026).** *Protocol committed before any fit or outcome of these arms (commit `3710267`); an addendum (commit `d3cdee6`) added two arms after the first results were known.* Every arm in Table 4.19 shares the revision-3 authority guard and the direct-value constraint of GV; only the decision for the calls that pass them differs. The candidates are published methods with documented implementations: a Neyman-Pearson umbrella threshold (Tong et al., 2018), a conformal-risk-control threshold (Angelopoulos et al., 2022), and gradient-boosted trees in place of the ridge estimator (Friedman, 2001). Their procedures were taken from the authors' or the library's implementations. No formal guarantee is claimed, because their sampling assumptions do not hold for clustered episodes and an unseen attacker objective.

**Table 4.19. Decision methods behind the authority front** (primary recordings under S1; `REM_COMPETITIVE_STUDY_2026_11_16/results/`)

| Decision for calls that pass the authority front | Primary: attacks; all tasks / 3,313 | Second: attacks; all tasks / 2,113 | Fixtures: unsafe released; pairs correct / 43 | Attack-labelled calls reaching the decision (primary; second) |
|---|---|---|---|---|
| **None: release (guard alone, GV)** | 0; 1,532 | 0; 1,386 | 0; 36 | 0; 0 |
| Ridge model, calibration, two-verdict expected loss (HV) | 0; 1,532 | 0; 1,386 | 0; 36 | 0; 0 |
| HV without the calibration map | 0; 1,532 | 0; 1,386 | 0; 36 | 0; 0 |
| HV with all four verdicts | 0; 1,532 | 0; 1,386 | 0; 36 | 0; 0 |
| Neyman-Pearson threshold, alpha 0.05 | 0; 1,532 | 0; 1,386 | 0; 36 | 0; 0 |
| Neyman-Pearson threshold, alpha 0.01 | 0; 1,526 | 0; 1,383 | 0; 36 | 0; 0 |
| Conformal-risk-control threshold, alpha 0.05 | 0; 1,532 | 0; 1,386 | 0; 36 | 0; 0 |
| Conformal-risk-control threshold, alpha 0.01 | 0; 1,532 | 0; 1,386 | 0; 36 | 0; 0 |
| Gradient-boosted trees in place of ridge | 0; 1,532 | 0; 1,386 | 0; 36 | 0; 0 |
| GV written as Cedar policies | 0; 1,532 | 0; 1,386 | 0; 36 | not separable (Cedar takes every decision) |
| GV plus a provenance rule | 0; 1,530 | 0; 1,389 | 0; 36 | 0; 0 |

Under the double holdout every arm has the same counts except the Neyman-Pearson threshold at 0.01 (1,479 tasks). With the attacker's identifier reformatted, no arm has a successful attack.

- **Every attack-labelled call is stopped by the guard.** The guard blocks all 907 attack-labelled calls to restricted tools on the primary recordings and all 559 on the second population. No attack-labelled call reaches the stage where a model, a threshold or a tree decides. The 1,059 and 903 calls that GV releases at that stage are *not attack-labelled*. That is a statement about the benchmark's attacker goals, not an independent authorization audit; Section 4.5.90 shows calls that the request does not authorize and that this guard admitted.
- **No decision method improved an outcome; one lost tasks.** The ridge model with or without calibration, all four verdicts, both conformal thresholds, the Neyman-Pearson threshold at 0.05 and the boosted trees give exactly GV's *episode* outcomes on both populations, the probe and the fixtures. Equal episode outcomes are not equal call decisions: the Neyman-Pearson threshold at 0.05 withholds 3 calls and the boosted trees 1 call on the primary recordings without changing an outcome. **The Neyman-Pearson threshold at 0.01 is the exception.** It withholds 25 and 12 calls and completes 1,526 and 1,383 tasks against GV's 1,532 and 1,386. No learned or calibrated decision added a measured benefit over the guard used alone. This does not show that a learner cannot help: the recordings contain no attack that passes the guard.
- **The estimator is not the reason.** On held-out attacker objectives the ridge estimator reaches ROC-AUC 0.993 on all steps and 0.976 on calls to restricted tools. The boosted trees are not better (log loss 0.074 against 0.071).
- **The calibrated thresholds do not carry their nominal levels to an unseen attacker objective.** Deciding alone on the held-out objective:
  - the Neyman-Pearson threshold at 0.05 would release 18 of 921 attack-labelled steps, above 5% in 1 of 9 objectives;
  - the conformal threshold at 0.05 would release 155 of 921, above its level in 7 of 9 objectives;
  - the conformal threshold at 0.01 would be above its level in 5 of 9.
- **Policy engine and provenance.**
  - The same guard written as nine Cedar policies (Cedar Policy, 2026), with a wrapper that withholds on any evaluation error, gave the same release decision on all 7,098 restricted calls of 8,106 replays.
  - A rule that withholds a call whose value occurs only in untrusted content removes no attack and withholds 27 and 6 calls. This is provenance tracking, not the information-flow control of FIDES (Costa et al., 2025).
- **A declared predicate withholds supported calls.** In GV, L4 and HV, predicate D2 withholds 55 and 62 updates of a scheduled transaction that the request supports (decision SD-D2, Appendix F).
- **The guard's amount handling is defective.** The outcomes in Table 4.19 are those of the frozen guard, which accepted unverified computed amounts and misread percentage coefficients. Section 4.5.90 reports the repair and its cost.
