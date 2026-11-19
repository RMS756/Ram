# 11 Claim audit of thesis R8 (19 November 2026)

**Scope.** This audit covers the major claims of R8, with emphasis on the text added or changed in R8. The claims of R7 were audited in `REM_FINAL_SUBMISSION/thesis_r7/audit/CLAIM_AUDIT_R7.md`. Unchanged R7 claims were rechecked only where the new results bear on them.

**Status values:**
- **OK:** supported as worded.
- **CORRECTED:** wording changed in R8.
- **FLAG:** a limit that must stay visible.

## 1 Claim table

| # | Claim (location in R8) | Support | Metric / population | Status |
|---|---|---|---|---|
| 1 | REM v1.0 reduces replay ASR from 22.6% to 0.4% (Ch. 1, 4, 5; abstract) | Pilot R4 and today's fresh reproduction (identical 11 / 2,979; 672 / 2,979) | ASR, primary population, NO-ADAPT replay, no reviewer | OK. Labelled replay throughout. |
| 2 | Benign task completion 52% → 31%; 33 of 178 legitimate calls released | Same; `03_…csv` | Benign utility / 334; legitimate restricted calls in benign episodes | OK |
| 3 | "The learned decision prevents 661 of the 672 attacks that REM stops and admits none, at a cost of 22.5 points of benign utility" (abstract, 4.5.5, 5.8) | A6 − A0: 661 / 0 episodes; benign +22.5 [8.0, 38.5] | Paired episodes, primary population | OK. Development data, stated. 672 = B0 successes = A6 successes; 661 prevented + 11 remaining = 672. |
| 4 | Calibration and Modify change no attack outcome (abstract, 4.5.5, 5.x) | A2 and A5: 0 / 0 attack changes | Paired | OK. A2 changes 24 task outcomes, stated in 4.5.5. |
| 5 | "Calibration does not improve protection"; raw probabilities are not worse calibrated | A2: no attack change; ECE 0.0415 vs 0.0438, Brier 0.0598 vs 0.0603 | Offline held-out steps (6,762) | OK. Calibration and decision utility are kept apart. No claim that calibration is harmful in general. |
| 6 | Behavioural evidence has a negative net effect in this evaluation | A1: benign +10.5 [1.2, 22.6]; all +2.99 [0.45, 6.11]; attacks 1 / 1 | Paired | OK. "In this evaluation" is stated. Consistent with the confirmatory run (R7, 4.6.8). |
| 7 | The consequence-aware rule has a measurable security contribution against thresholds, with a utility cost | A3 − A0: +5.14 ASR pp [0.70, 13.05]; benign +19.5 [7.4, 34.1] | Paired | OK. Worded as a trade-off, not dominance. The thresholds are B1 with per-fold training-data selection, never test folds. |
| 8 | Modify is redundant in this evaluation (NULL) | A5: 0 episode changes | Paired | OK. Bounded to step-level mitigation without a reviewer. Consistent with R7 4.4.1 ("Modify, Escalate and Block coincide"). |
| 9 | Action / provenance evidence carries the discrimination; security effect not resolved | ROC-AUC 0.938 → 0.799; A4b +0.20 pp [−0.07, 0.43] | Offline; paired | OK |
| 10 | Context evidence and predicates: no measurable effect | A4a 0 / 0 attacks, 2 tasks; A7 0 / 0, 5 tasks | Paired | OK. Worded "no measurable effect", not "NULL", because some episodes change. |
| 11 | The learned decision in REM v1.0 is reached and decides (6,626 of 6,684 calls; 2,129 releases changed) | Reachability table | Call level, A0 vs A6 | OK. Distinguished explicitly from the REM-B family's NULL learned components (4.5.6). |
| 12 | Recorded defences: ASR 62.5 / 46.5 / 61.8 / 11.1 / 0.7% on 144 runs | Run files @ `089ed468` | Recorded closed loop, gpt-4o | CORRECTED in R8. R7 gave the 143-run AM-1 figures without explaining the denominator; both are now explained. |
| 13 | "On the same task pairs, REM's replayed decisions left fewer successful attacks than three defences and about as many as the injection classifier" (abstract, 4.4.2, 5.x) | Cross-kind contrasts on 134 identical pairs | **Different evidence kinds** | OK, as descriptive. Searching the new text for "outperform", "superior" and "better than" finds one occurrence, the disclaimer "No claim that REM outperforms any of these defenses". |
| 14 | Adding REM to a defence's traces removes almost every remaining success, at about half of benign completion | Within-replay contrasts | NO-ADAPT replay | OK. Bounded "under NO-ADAPT". |
| 15 | tool_filter traces are not replayable with the frozen harness | 0 calls in 159 replays; amendment 05a | – | OK. Reported as a limitation, not hidden. |
| 16 | MELON not executed | `08` | – | OK. No MELON number appears in any table. |
| 17 | REM-B family: 0 attacks in replay; NO-GO on held-out probes (4.5.6) | `REM_B_HARDENING_VALIDATION_2026_11_19/12_FINAL_ARCHITECTURE_DECISION.md` | Exploratory | OK. Labelled exploratory and not adopted; not merged into REM v1.0. |
| 18 | Latency 0.149 ms median (complete-call timer) | `results/ablation_results.json` | 6,684 calls, replay, one container | OK. R8 notes that it is lower than the R4 run's 0.21–0.28 ms (run-to-run variation). Not a deployment latency. |

## 2 Flags requested by the task

| Check | Finding |
|---|---|
| Unsupported superiority claims | None in the R8 additions. The cross-kind comparison is labelled descriptive in 4.4.2, Ch. 1, Ch. 5 and the abstracts. |
| Fabricated citations | None. `check_citations.py` on R8: 103 reference entries, all cited. `check_citations_reverse.py`: no cited surname-and-year is missing from the list. The new citations, T. Shi et al. (2026) and Debenedetti et al. (2024), are existing, verified entries. |
| Unverified publication details | MELON is ICML 2025, PMLR 267 (verified earlier through PMLR and OpenAlex). Progent v3 was read in full. The status of each preprint is stated in the reference list. Unchanged from R7. |
| Incorrect equations | No equation was added or changed. `make_r8.py` checks that the set of numbered equations is identical to R7's (no problem reported). |
| Inconsistent numerical results | A0 equals the published REM v1.0 counts (test `test_reproduction_gate_and_A0_match_published_counts`). The paired differences equal the count differences (test). The 143 vs 144 denominators are explained. |
| Data leakage | Predictions are cross-fitted (outer fold holds out an attacker objective). A3 thresholds are selected on training folds only. The population is **development data** in every new analysis, and this is stated (02, 4.5.5). |
| Unreported post-hoc modifications | Amendment 05a is reported. The post-hoc descriptive analyses (attacks by injection task; McNemar sensitivity) are marked POSTHOC in file names and text. The "primary / secondary endpoint" labelling of `04` is stated as added at analysis time. |
| Unjustified novelty claims | None added. R8 contribution 9 is a measured result, attributed to an established method (component ablation as in Progent). |
| Replay vs live confusion | Every new table states "replay (NO-ADAPT)" or "recorded closed loop". No result is called live. |
| Policy-only vs complete-framework confusion | The Progent comparison (4.4.3) remains "a manual banking policy from Progent's repository … not a reproduction of the Progent framework". The distributed defences are the benchmark's own implementations. |

## 3 Corrections made in R8

1. **Section 4.4.2** is replaced. The recorded figures are now on 144 runs, with the reason for R7's 143, and the replay of REM on the same traces is added.
2. **Chapter 1, "does not demonstrate".** The bullet "any comparison with a published defense that needs a language model" is reworded, because a descriptive comparison now exists. A closed-loop comparison is still not demonstrated.
3. **Chapter 5, Table 5.2 (O3).** Updated to the same effect.
4. **Chapter 5, limitation 10.** Updated: the defences are compared descriptively, REM is not run in a closed loop, and tool_filter is not replayable.
5. **Front matter.** Edition statement dated 19 November 2026, and "draft for supervisor review" is kept. The thesis is **not** described as approved anywhere.

## 4 Residual risks a reader should know

- **Every new result is development evidence.** The independent confirmatory evidence of the thesis remains the single run of 11 November (R7, 4.6.8).
- **The comparison with the distributed defences is the closest the thesis comes to O3 for model-based defences.** It is descriptive. A closed-loop comparison needs supervisor authorisation (`13`, decision D-15).
