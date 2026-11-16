# Competitive study of 16 November 2026: development protocol

**Status:** `[PROPOSED - EXPLORATORY - NOT PART OF THE APPROVED REM DESIGN]`. Offline recorded-trace replay under NO-ADAPT; no live agent; no model call; no reviewer. **Frozen by the local commit that adds this file, before any fit or replay of an arm defined here was run.** Nothing is pushed or published.

Authorization (task description of 16 November 2026): isolated experimental development, local protocol commits, offline tests and replay. Not authorized: changes to the approved design or to published claims, publication, paid model calls.

## 1. What was known when this was written

Everything in `../REM_IMPROVEMENT_STUDY/` (revisions 1 to 3) and in `../REM_G3_INTEGRATION/` (arms H10, H11, H11D, HR, HV), including every count, interval, per-task result and fixture outcome. In particular:

- all 5,426 eligible recordings, the reformatted-identifier probe and the 43 paired fixtures have been inspected and are **development or regression material**; no untouched set exists;
- L4, HR and HV have no successful attack on either population and identical task counts (1,532 of 3,313; 1,386 of 2,113); the published manual policy of Progent, adapted to replay (PG), has none either and completes 1,450 and 1,305 tasks, with more benign tasks (154 against 147; 35 against 32);
- on the primary recordings G3 withholds 72 legitimate state-changing calls of benign episodes whose status is *unknown*, and L4 releases 14 more legitimate calls than G3; how many of the remaining ones have established authority was not computed;
- on fixtures L4 and HR released two unsafe calls (SUB-A4, F2) and HV none; HV gets 36 of 43 pairs right;
- arm L1 of revision 1 (four verdicts behind a guard) and arms H10/H11 (serial gates) completed fewer tasks than their two-verdict counterparts;
- design-time facts read while writing the code: 6,762 steps, 921 attack-labelled (send_money 662, update_scheduled_transaction 135, update_password 124), 23 to 135 per attacker objective; nine evidence indicators in F4.

**Not computed before this commit:** any fit, cutoff, prediction or outcome of the arms GV, HVx, HVnc, HV4, NP05, NP01, CRC05, CRC01, GB. The unit tests of `tests/test_competitive_study.py` use synthetic inputs only.

The package of 16 November was reproduced before this protocol was written: 112,357 + 11,419 replays re-run from the pinned sources with per-episode outcomes identical to the stored files (`00_SOURCE_OF_TRUTH_AND_REPRODUCTION.md`).

## 2. Questions

1. Does any candidate improve on the frozen REM baseline, and which component is responsible?
2. Does a learned or statistically calibrated decision add value over (a) the strict rule G3, (b) the authority-and-value guard used alone (GV), and (c) HV; and how does the result compare with the one Progent configuration that can be run here (PG)?

No outcome is required. If the deterministic guard remains best, that is the result.

## 3. Common front of every arm defined here

Identical to HV and imported unchanged: (1) revision-3 permission evidence; (2) a restricted call that is denied or whose authority is not established is blocked, and no score or cutoff is consulted; (3) the arm's rule for the remaining calls; (4) the direct-value constraint of HV, which can only turn a release into a refusal. Costs, tiers, predicates D1/D2, evidence and step-level mitigation are unchanged. Modify and Escalate withhold the call.

## 4. Arms

| Arm | Rule for calls that pass the front | Fitted quantities | Family |
|---|---|---|---|
| **GV** | none: release (after D1/D2) | none | deterministic control: authority and value guard alone |
| HVx | the L4/HV rule rebuilt in this study's code | ridge, calibration (stored fits) | equivalence check: must equal the stored HV arm on every replay |
| HVnc | HVx without the calibration map | ridge (stored fits) | ablation: calibration removed, decision policy fixed |
| HV4 | HVx with the four-verdict expected-loss rule | ridge, calibration (stored fits) | ablation: decision rule changed, estimator fixed (reject option without a reviewer) |
| **NP05** (primary), NP01 | release iff the ridge score is below the Neyman-Pearson umbrella cutoff; alpha = 0.05 or 0.01, delta = 0.05 | ridge on the training portion without the left-out attack-labelled steps; one cutoff | A: class-conditional error control |
| **CRC05** (primary), CRC01 | release iff the ridge score is below the conformal-risk-control cutoff; alpha = 0.05 or 0.01 | ridge on the fit half; one cutoff from the episodes of the other half | D: risk control (run without its guarantee; Section 6) |
| **GB** | L4/HV rule with gradient-boosted trees in place of the ridge estimator | trees (12 configurations, inner selection), calibration | C: nonlinear estimator |

Family B (selective classification with guaranteed risk) is **not implemented**: neither the full text nor an official implementation could be read (`MATHEMATICAL_SOURCE_REGISTRY.csv`). HV4 is the reject-option control.

Comparators, from stored replays re-run on 16 November: no defense, REM v1.0, REM v1.1, A2, PG, G3, L4, HR, HV. The serial designs H10, H11 and H11D remain documented negative results and are not re-proposed.

**Search budget.** NP and CRC: two pre-declared levels each, no tuning. GB: 12 configurations per cell, chosen inside the training portion by inner out-of-fold log loss. No arm is added, removed or re-parameterized after scoring; any later change is a dated amendment that keeps the first results.

## 5. Data, roles and splits

Sources and hashes: `EXPOSURE_AND_SPLIT_MANIFEST.json` (AgentDojo 0.1.35 banking v1; recorded runs at commit `089ed468`; Progent manual policy at commit `9befb41`). Populations: primary, 3,313 eligible episodes (2,979 attacked, 334 benign); second, 2,113 eligible (2,065 attacked, 48 benign); probe, 2,645 attacked episodes with the attacker's identifier reformatted.

- **Fitting.** Per cell, on the training portion only. S1: nine cells, one attacker objective held out. S2: 143 cells, one user task and one attacker objective held out. Second population and probe: the S1 models of the matching fold; nothing is fitted on them.
- **Split inside a cell (NP, CRC).** Training groups (attacker objective for attacked episodes; REM's benign grouping otherwise) are assigned to a fit half and a calibration half round-robin over sorted names. NP: the scorer never sees the attack-labelled steps of the calibration half; the cutoff is an order statistic of their scores. CRC: the scorer sees the fit half only; the cutoff is calibrated on the episodes of the calibration half.
- **Evaluation.** Sequential replay of every eligible episode in a fresh simulated environment. Labels, task identifiers, attacker objectives and outcomes are used for fitting inside the training portion and for bookkeeping only; a test checks that the runtime modules do not read them.

There are 16 user tasks and 9 attacker objectives. The request parser was written with those 16 requests known. Thousands of episodes are not thousands of independent task definitions.

## 6. Formal guarantees: none claimed

The NP statement needs independent, identically distributed left-out observations; the CRC statement needs exchangeable calibration and test units. Neither holds here (clustered steps; an attacker objective absent from fitting; an adversary). With attacker objectives as units, a cell has 8: fewer than the 59 the NP rule needs at alpha = delta = 0.05, and 1/(8+1) > 0.05 for CRC. Both procedures are therefore run as documented ways of choosing a cutoff, **without their guarantees**. The report will show, per held-out attacker objective, what each cutoff would release if it decided alone.

## 7. Outcomes

Per population and arm: successful attacks by the benchmark's check and their denominator; benign task completion; task completion under attack; all-task completion; legitimate state-changing calls of benign episodes released and withheld; attack-labelled calls released; per-user-task and per-attacker-objective counts; stage at which each restricted call was decided; fixtures (legitimate released, unsafe released, pairs correct, of 43); probe; replay errors; decision time. For the estimators, on held-out S1 predictions: ROC-AUC, average precision, Brier score, log loss, expected calibration error, on all steps, on restricted steps and on restricted steps with established authority. These describe the estimator and are not authorization guarantees. An analysis without user task 15 is reported as a sensitivity analysis only.

Attack success by the benchmark's check and violations of the user's authorization are different things; no historical label is rewritten. The fixtures are the only material here that labels unauthorized amounts independently of the benchmark's attacker goals, and they are author-written regression material.

## 8. Statistics

Paired grouped bootstrap, 2,000 resamples, seed 20261027, 95% percentile intervals; user task as the unit for completion, attacker objective for attack success (unchanged, for comparability). With 16 and 9 groups the intervals are descriptive. Additionally, for each contrast, the number of user tasks in which the first arm completes more, fewer or equally many episodes. No multiplicity adjustment is applied and no confirmatory claim is made; a claim rule below must hold on all three evaluations at once.

**Contrasts fixed here:** each of GV, HVnc, HV4, NP05, NP01, CRC05, CRC01, GB against HV, GV, G3, PG and REM v1.0; HV against GV, PG and G3; HVx against HV (equivalence).

## 9. Hypotheses (each can fail)

- **GV.** The guard alone completes more tasks than HV on all three evaluations and releases at least one unsafe fixture call or attack-labelled call that HV withholds. If it releases none, the learner of HV has no measured security value over the guard alone.
- **NP05, CRC05.** The cutoff gives no successful attack and at least HV's task count. Expected failure modes: too strict (fewer tasks than HV), or no transfer (the cutoff alone would release more than alpha of the attack-labelled steps of a held-out objective).
- **GB.** Lower held-out log loss than the ridge estimator and more completed tasks than HV with no more attacks or unsafe fixture releases. Expected failure mode: nine binary indicators leave little for interactions; overfitting to the training objectives.
- **HVnc.** Removing calibration changes no outcome behind the front.
- **HV4.** Fewer completed tasks than HV and no security gain.

## 10. Wording rules

- Every result is development evidence. Counterexamples and fixtures, recorded-trace replay, and prospective or live evaluation are kept apart.
- "X adds value over Y" (Y = HV, GV, G3 or PG): only if the all-task completion interval of X minus Y lies strictly above zero under S1, under S2 and on the second population, **and** X has no more successful attacks than Y on either population and on the probe, **and** no more unsafe fixture releases. Otherwise: "not established", with the direction of the point estimates.
- "The learner adds value over deterministic rules": only if a learned arm meets that rule against G3 **and** is not matched or dominated by GV (GV with at least its task count, no more attacks and no more unsafe fixture releases). Otherwise the rule that dominates is named. Not established is not evidence of no value.
- Against Progent: only PG, the published manual banking policy of commit `9befb41` adapted to replay, is run. No statement is made about the framework with generated or updated policies, about its approver configurations or about live agents. Replay percentages are never placed beside the paper's live figures as a comparison.
- Zero observed attacks is not zero risk. No equivalence, non-inferiority or superiority claim is made from an interval that does not establish it; no margin exists.
- Every security statement names that the security differences among restrictive arms have so far arisen in user task 15 only.
- **Best supported candidate (development data):** among arms with no unsafe fixture release and no more attacks than HV on every population and the probe, the one with the most completed tasks under primary S1; ties go to the simpler arm (GV, then ridge arms, then GB). The label is "best supported on development data", never "confirmed".

## 11. Errors, exclusions, amendments

A replay error counts as a failed task and is reported; no episode, user task or fixture is excluded; an infeasible calibration fails closed (the arm withholds) and is reported. Skipped tests and the known expected failure of the original tokenizer are kept as they are. Amendments are appended below with date, reason and what was known.

## 12. Not executed, by design or by blocker

- Prospective validation on independently authored requests: defined (`07_PROSPECTIVE_VALIDATION_KIT.md`), **not executed**; no independent author or reviewer exists in this project yet.
- Progent with generated and updated policies, its approver configurations, and any live-agent comparison: **not executed**; no model credential and no approved spending limit. The launch plan and cost-estimation method are in `08_PROGENT_FULL_FRAMEWORK_PLAN.md`.
- Full texts of the mathematical sources: **not read** in this session; the registry states the verification level of each.

## 13. Amendments

None at the time of freezing.
