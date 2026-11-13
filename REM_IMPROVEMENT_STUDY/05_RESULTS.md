# 5. Results

**Status of every number here: development evidence.** Offline recorded-trace replay of AgentDojo 0.1.35 banking episodes; step level; no live agent; no reviewer; the agent's later steps do not adapt to a withheld call. All 5,426 episodes had been inspected in earlier studies. Protocol frozen at commit `9137b03` before any new arm was replayed; no amendment. Machine-readable results: `results/improvement_results.json`; all tables: `results/tables.md`; failure analysis: `results/failure_analysis.json`; logs: `logs/`.

Terminology. *Successful attack*: the benchmark's security checker reports the attacker's goal as reached in the replayed episode. *Episode with a released attack-labelled call*: a proxy; the effect of the released call on the bank state is not measured separately, so it is not called a committed unauthorized state. *Legitimate state-changing call*: a call to a state-changing tool in a benign episode.

## 5.1 What ran

| Item | Value |
|---|---|
| Fitting cells | 152 (9 folds by attacker objective; 143 double-holdout cells), 6 s |
| Replays | 161,506 in 338 s; 0 replay errors |
| Arms | 20 (7 earlier, 8 rule arms including the published comparator and five ablations, 5 learned arms) |
| Populations | primary 3,313 eligible episodes (2,979 attacked, 334 benign); second development population 2,113 (2,065 attacked, 48 benign); reformatted-identifier probe 2,645 attacked; 43 paired fixtures in four sets |
| Exclusions | Unchanged from the earlier studies: errored episodes and the task pairs excluded by the label rule are not loaded (second population: 2,148 loaded, `protocol/SPLIT_MANIFEST.json`); episodes whose undefended replay does not reproduce the recorded outcome are not eligible (second population: 2,113 eligible, the same set as in the earlier confirmatory run). No episode was excluded because of the outcome of a defended arm |
| Model calls | 0 |

## 5.2 Primary population, held-out attacker objective (S1)

| Arm | Successful attacks (of 2,979) | Episodes with a released attack-labelled call | Tasks completed under attack | Benign tasks completed (of 334) | All tasks completed (of 3,313) | Legitimate state-changing calls released, benign episodes | Held-out credential-change attacks |
|---|---|---|---|---|---|---|---|
| No defense (B0) | 672 (22.6%) | 828 | 1,465 | 175 (52.4%) | 1,640 (49.5%) | 178 of 178 | 119 of 334 |
| Provenance rule (B1) | 164 (5.5%) | 202 | 1,532 | 170 (50.9%) | 1,702 (51.4%) | 130 of 178 | 119 of 334 |
| REM v1.0 | 11 (0.4%) | 24 | 1,083 | 105 (31.4%) | 1,188 (35.9%) | 33 of 178 | 0 of 334 |
| REM v1.1 (proposed) | 11 (0.4%) | 24 | 1,147 | 140 (41.9%) | 1,287 (38.8%) | 83 of 178 | 0 of 334 |
| Allow/Block only (M01) | 13 (0.4%) | 27 | 1,273 | 124 (37.1%) | 1,397 (42.2%) | 64 of 178 | 0 of 334 |
| Rule P2 | 12 (0.4%) | 26 | 1,207 | 134 (40.1%) | 1,341 (40.5%) | 89 of 178 | 0 of 334 |
| Rule A2 | 13 (0.4%) | 27 | 1,334 | 140 (41.9%) | 1,474 (44.5%) | 83 of 178 | 0 of 334 |
| Progent manual policy (PG) | 0 (0.0%) | 0 | 1,296 | 154 (46.1%) | 1,450 (43.8%) | 136 of 178 | 0 of 334 |
| Permission rule (G1) | 10 (0.3%) | 23 | 1,425 | 149 (44.6%) | 1,574 (47.5%) | 112 of 178 | 0 of 334 |
| v1.1, two-verdict decision (V11d) | 131 (4.4%) | 148 | 1,336 | 156 (46.7%) | 1,492 (45.0%) | 99 of 178 | 119 of 334 |
| Learned on permission evidence, no guard (L0) | 11 (0.4%) | 24 | 1,544 | 167 (50.0%) | 1,711 (51.6%) | 131 of 178 | 0 of 334 |
| Guard + learned, four verdicts (L1) | 10 (0.3%) | 23 | 1,371 | 160 (47.9%) | 1,531 (46.2%) | 112 of 178 | 0 of 334 |
| Guard + learned, two verdicts (L2) | 10 (0.3%) | 23 | 1,519 | 161 (48.2%) | 1,680 (50.7%) | 125 of 178 | 0 of 334 |
| Guard + learned on unknown calls only (L2s) | 10 (0.3%) | 23 | 1,488 | 156 (46.7%) | 1,644 (49.6%) | 130 of 178 | 0 of 334 |

### Paired contrasts (primary_S1)

| Contrast | Fixed in advance | All-task completion, points [95% interval] | Benign completion, points [95% interval] | Attack success, points [95% interval] | Tasks gained / lost | Attacks gained / lost |
|---|---|---|---|---|---|---|
| G1 − A2 | yes | +3.02 [-3.34, 13.09] | +2.69 [-3.87, 12.42] | -0.10 [-0.20, -0.03] | 149 / 49 | 0 / 3 |
| G1 − PG | yes | +3.74 [-6.45, 17.03] | -1.50 [-14.29, 13.56] | +0.34 [0.10, 0.57] | 255 / 131 | 10 / 0 |
| G1 − v1.1 | yes | +8.66 [-2.75, 22.01] | +2.69 [-7.74, 14.46] | -0.03 [-0.10, 0.00] | 435 / 148 | 0 / 1 |
| G1 − v1.0 | no (descriptive) | +11.65 [-0.39, 26.25] | +13.17 [1.50, 28.14] | -0.03 [-0.14, 0.07] | 496 / 110 | 1 / 2 |
| L2 − G1 | yes | +3.20 [-0.76, 8.80] | +3.59 [0.00, 9.52] | +0.00 [0.00, 0.00] | 127 / 21 | 0 / 0 |
| L2s − G1 | yes | +2.11 [-0.69, 7.00] | +2.10 [-0.89, 7.19] | +0.00 [0.00, 0.00] | 78 / 8 | 0 / 0 |
| V11d − v1.1 | yes | +6.19 [0.00, 15.74] | +4.79 [0.00, 14.55] | +4.03 [0.00, 12.02] | 209 / 4 | 120 / 0 |
| L0 − L2 | yes | +0.94 [0.00, 2.84] | +1.80 [0.00, 5.42] | +0.03 [0.00, 0.10] | 31 / 0 | 1 / 0 |
| PG − A2 | no (descriptive) | -0.72 [-15.80, 14.24] | +4.19 [-12.81, 20.91] | -0.44 [-0.73, -0.14] | 280 / 304 | 0 / 13 |
| L1 − G1 | no (descriptive) | -1.30 [-8.33, 5.73] | +3.29 [-0.60, 9.23] | +0.00 [0.00, 0.00] | 126 / 169 | 0 / 0 |

## 5.3 Primary population, double holdout (S2)

| Arm | Successful attacks (of 2,979) | Episodes with a released attack-labelled call | Tasks completed under attack | Benign tasks completed (of 334) | All tasks completed (of 3,313) | Legitimate state-changing calls released, benign episodes | Held-out credential-change attacks |
|---|---|---|---|---|---|---|---|
| No defense (B0) | 672 (22.6%) | 828 | 1,465 | 175 (52.4%) | 1,640 (49.5%) | 178 of 178 | 119 of 334 |
| REM v1.0 | 11 (0.4%) | 24 | 1,078 | 105 (31.4%) | 1,183 (35.7%) | 35 of 178 | 0 of 334 |
| REM v1.1 (proposed) | 14 (0.5%) | 27 | 1,132 | 140 (41.9%) | 1,272 (38.4%) | 83 of 178 | 2 of 334 |
| Rule P2 | 12 (0.4%) | 26 | 1,207 | 134 (40.1%) | 1,341 (40.5%) | 89 of 178 | 0 of 334 |
| Rule A2 | 13 (0.4%) | 27 | 1,334 | 140 (41.9%) | 1,474 (44.5%) | 83 of 178 | 0 of 334 |
| Progent manual policy (PG) | 0 (0.0%) | 0 | 1,296 | 154 (46.1%) | 1,450 (43.8%) | 136 of 178 | 0 of 334 |
| Permission rule (G1) | 10 (0.3%) | 23 | 1,425 | 149 (44.6%) | 1,574 (47.5%) | 112 of 178 | 0 of 334 |
| v1.1, two-verdict decision (V11d) | 131 (4.4%) | 148 | 1,296 | 156 (46.7%) | 1,452 (43.8%) | 101 of 178 | 119 of 334 |
| Learned on permission evidence, no guard (L0) | 12 (0.4%) | 26 | 1,540 | 167 (50.0%) | 1,707 (51.5%) | 133 of 178 | 0 of 334 |
| Guard + learned, four verdicts (L1) | 10 (0.3%) | 23 | 1,269 | 160 (47.9%) | 1,429 (43.1%) | 114 of 178 | 0 of 334 |
| Guard + learned, two verdicts (L2) | 10 (0.3%) | 23 | 1,515 | 161 (48.2%) | 1,676 (50.6%) | 127 of 178 | 0 of 334 |
| Guard + learned on unknown calls only (L2s) | 10 (0.3%) | 23 | 1,488 | 156 (46.7%) | 1,644 (49.6%) | 132 of 178 | 0 of 334 |

### Paired contrasts (primary_S2)

| Contrast | Fixed in advance | All-task completion, points [95% interval] | Benign completion, points [95% interval] | Attack success, points [95% interval] | Tasks gained / lost | Attacks gained / lost |
|---|---|---|---|---|---|---|
| G1 − A2 | yes | +3.02 [-3.34, 13.09] | +2.69 [-3.87, 12.42] | -0.10 [-0.20, -0.03] | 149 / 49 | 0 / 3 |
| G1 − PG | yes | +3.74 [-6.45, 17.03] | -1.50 [-14.29, 13.56] | +0.34 [0.10, 0.57] | 255 / 131 | 10 / 0 |
| G1 − v1.1 | yes | +9.12 [-2.42, 22.56] | +2.69 [-7.74, 14.46] | -0.13 [-0.27, -0.03] | 449 / 147 | 0 / 4 |
| G1 − v1.0 | no (descriptive) | +11.80 [-0.33, 26.53] | +13.17 [1.50, 28.14] | -0.03 [-0.14, 0.07] | 501 / 110 | 1 / 2 |
| L2 − G1 | yes | +3.08 [-0.87, 8.72] | +3.59 [0.00, 9.52] | +0.00 [0.00, 0.00] | 127 / 25 | 0 / 0 |
| L2s − G1 | yes | +2.11 [-0.69, 7.00] | +2.10 [-0.89, 7.19] | +0.00 [0.00, 0.00] | 78 / 8 | 0 / 0 |
| V11d − v1.1 | yes | +5.43 [0.45, 13.81] | +4.79 [0.00, 14.55] | +3.93 [0.00, 11.79] | 184 / 4 | 117 / 0 |
| L0 − L2 | yes | +0.94 [0.00, 2.84] | +1.80 [0.00, 5.42] | +0.07 [0.00, 0.17] | 31 / 0 | 2 / 0 |
| PG − A2 | no (descriptive) | -0.72 [-15.80, 14.24] | +4.19 [-12.81, 20.91] | -0.44 [-0.73, -0.14] | 280 / 304 | 0 / 13 |
| L1 − G1 | no (descriptive) | -4.38 [-12.28, 3.75] | +3.29 [-0.60, 9.23] | +0.00 [0.00, 0.00] | 126 / 271 | 0 / 0 |

## 5.4 Second development population

| Arm | Successful attacks (of 2,065) | Episodes with a released attack-labelled call | Tasks completed under attack | Benign tasks completed (of 48) | All tasks completed (of 2,113) | Legitimate state-changing calls released, benign episodes | Held-out credential-change attacks |
|---|---|---|---|---|---|---|---|
| No defense (B0) | 436 (21.1%) | 493 | 1,413 | 38 (79.2%) | 1,451 (68.7%) | 51 of 51 | 54 of 232 |
| Provenance rule (B1) | 67 (3.2%) | 96 | 1,478 | 36 (75.0%) | 1,514 (71.7%) | 36 of 51 | 54 of 232 |
| REM v1.0 | 3 (0.1%) | 3 | 898 | 18 (37.5%) | 916 (43.4%) | 4 of 51 | 0 of 232 |
| REM v1.1 (proposed) | 1 (0.0%) | 1 | 1,049 | 25 (52.1%) | 1,074 (50.8%) | 11 of 51 | 0 of 232 |
| Allow/Block only (M01) | 3 (0.1%) | 3 | 1,093 | 22 (45.8%) | 1,115 (52.8%) | 8 of 51 | 0 of 232 |
| Rule P2 | 4 (0.2%) | 4 | 1,019 | 24 (50.0%) | 1,043 (49.4%) | 12 of 51 | 0 of 232 |
| Rule A2 | 4 (0.2%) | 4 | 1,205 | 27 (56.2%) | 1,232 (58.3%) | 27 of 51 | 0 of 232 |
| Progent manual policy (PG) | 0 (0.0%) | 0 | 1,270 | 35 (72.9%) | 1,305 (61.8%) | 48 of 51 | 0 of 232 |
| Permission rule (G1) | 3 (0.1%) | 3 | 1,326 | 32 (66.7%) | 1,358 (64.3%) | 36 of 51 | 0 of 232 |
| v1.1, two-verdict decision (V11d) | 58 (2.8%) | 60 | 1,154 | 28 (58.3%) | 1,182 (55.9%) | 14 of 51 | 54 of 232 |
| Learned on permission evidence, no guard (L0) | 2 (0.1%) | 2 | 1,490 | 36 (75.0%) | 1,526 (72.2%) | 40 of 51 | 0 of 232 |
| Guard + learned, four verdicts (L1) | 1 (0.0%) | 1 | 1,306 | 32 (66.7%) | 1,338 (63.3%) | 34 of 51 | 0 of 232 |
| Guard + learned, two verdicts (L2) | 2 (0.1%) | 2 | 1,454 | 35 (72.9%) | 1,489 (70.5%) | 39 of 51 | 0 of 232 |
| Guard + learned on unknown calls only (L2s) | 3 (0.1%) | 3 | 1,425 | 34 (70.8%) | 1,459 (69.0%) | 40 of 51 | 0 of 232 |

### Paired contrasts (dev2)

| Contrast | Fixed in advance | All-task completion, points [95% interval] | Benign completion, points [95% interval] | Attack success, points [95% interval] | Tasks gained / lost | Attacks gained / lost |
|---|---|---|---|---|---|---|
| G1 − A2 | yes | +5.96 [-4.25, 19.14] | +10.42 [-4.17, 29.17] | -0.05 [-0.15, 0.00] | 172 / 46 | 0 / 1 |
| G1 − PG | yes | +2.51 [-15.09, 20.94] | -6.25 [-33.33, 20.83] | +0.15 [0.05, 0.29] | 248 / 195 | 3 / 0 |
| G1 − v1.1 | yes | +13.44 [-5.21, 33.59] | +14.58 [-10.42, 39.58] | +0.10 [0.00, 0.24] | 461 / 177 | 2 / 0 |
| G1 − v1.0 | no (descriptive) | +20.92 [1.30, 42.46] | +29.17 [8.33, 52.08] | +0.00 [-0.15, 0.14] | 554 / 112 | 1 / 1 |
| L2 − G1 | yes | +6.20 [-1.53, 17.63] | +6.25 [0.00, 18.75] | -0.05 [-0.15, 0.00] | 150 / 19 | 0 / 1 |
| L2s − G1 | yes | +4.78 [-0.42, 14.86] | +4.17 [-6.25, 18.75] | +0.00 [0.00, 0.00] | 104 / 3 | 0 / 0 |
| V11d − v1.1 | yes | +5.11 [0.19, 12.54] | +6.25 [0.00, 18.75] | +2.76 [0.00, 7.98] | 110 / 2 | 57 / 0 |
| L0 − L2 | yes | +1.75 [-0.14, 5.56] | +2.08 [0.00, 6.25] | +0.00 [0.00, 0.00] | 38 / 1 | 0 / 0 |
| PG − A2 | no (descriptive) | +3.45 [-19.45, 26.52] | +16.67 [-16.67, 47.92] | -0.19 [-0.43, -0.05] | 367 / 294 | 0 / 4 |
| L1 − G1 | no (descriptive) | -0.95 [-12.95, 12.45] | +0.00 [-18.75, 18.75] | -0.10 [-0.24, 0.00] | 150 / 170 | 0 / 2 |

## 5.5 Reading of the comparisons fixed in advance

1. **G1 − A2 (strongest simple rule of the earlier studies).** G1 completes more tasks in both populations (1,574 against 1,474 of 3,313; 1,358 against 1,232 of 2,113) with fewer successful attacks (10 against 13; 3 against 4). The task-completion intervals include zero in both populations (+3.02 points [−3.34, 13.09]; +5.96 [−4.25, 19.14]; 16 user-task clusters). By the wording rule fixed in advance, **"added value over simple rules" is not stated.** The result is a favourable point estimate with no detectable difference in task completion. The attack-success difference on the primary population is −0.10 points [−0.20, −0.03] (three attacks fewer, none more); on the second population its interval reaches zero.
2. **G1 − Progent manual policy.** No successful attack occurs under Progent's policy in either population; G1 has 10 and 3. The attack-success difference is above zero in both populations (+0.34 points [0.10, 0.57]; +0.15 [0.05, 0.29]): **on security the published policy is better on this benchmark.** Task-completion differences are unresolved (+3.74 [−6.45, 17.03]; +2.51 [−15.09, 20.94]). Progent's policy releases more legitimate calls in benign episodes (136 of 178 against 112; 48 of 51 against 36) and completes no password-change task (user task 14: 0 of 209 and 0 of 129), because the tool has no policy entry.
3. **G1 − REM v1.1.** More tasks (+8.66 points [−2.75, 22.01]; +13.44 [−5.21, 33.59]), intervals include zero. On the second population G1 has 3 successful attacks and v1.1 has 1.
4. **Learned model on the same evidence (L2 − G1, L2s − G1).** More tasks without more attacks on the original text, under both splits (S1: +3.20 [−0.76, 8.80] and +2.11 [−0.69, 7.00]; S2: +3.08 [−0.87, 8.72] and +2.11 [−0.69, 7.00]). Every interval includes zero. **"The learned model adds value" is not stated.** In addition, the reformatted-identifier probe shows a cost (5.6).
5. **Decision semantics alone (V11d − v1.1).** More tasks (+6.19 [0.00, 15.74]) and 120 more successful attacks, including all 119 of the held-out credential-change objective. Removing the Escalate region from v1.1 without a guard is unsafe.
6. **Guard (L0 − L2).** Without the guard the learned arm completes slightly more tasks (+0.94 [0.00, 2.84]) and has one or two more successful attacks; on fixtures it releases more unsafe calls (5.7).

Descriptive, not fixed in advance: G1 against REM v1.0 gives benign completion +13.17 points [1.50, 28.14] and +29.17 [8.33, 52.08], with 10 against 11 and 3 against 3 successful attacks.

## 5.6 Ablations, probe and per-task results

| Arm | Successful attacks (of 2,979) | Episodes with a released attack-labelled call | Tasks completed under attack | Benign tasks completed (of 334) | All tasks completed (of 3,313) | Legitimate state-changing calls released, benign episodes | Held-out credential-change attacks |
|---|---|---|---|---|---|---|---|
| Rule A2 | 13 (0.4%) | 27 | 1,334 | 140 (41.9%) | 1,474 (44.5%) | 83 of 178 | 0 of 334 |
| A2 + typed normalization (A2n) | 13 (0.4%) | 27 | 1,334 | 140 (41.9%) | 1,474 (44.5%) | 83 of 178 | 0 of 334 |
| Permission rule (G1) | 10 (0.3%) | 23 | 1,425 | 149 (44.6%) | 1,574 (47.5%) | 112 of 178 | 0 of 334 |
| G1 without operation check | 10 (0.3%) | 23 | 1,425 | 148 (44.3%) | 1,573 (47.5%) | 113 of 178 | 0 of 334 |
| G1 without amount check | 13 (0.4%) | 27 | 1,486 | 156 (46.7%) | 1,642 (49.6%) | 122 of 178 | 0 of 334 |
| G1 without established payees | 10 (0.3%) | 23 | 1,408 | 148 (44.3%) | 1,556 (47.0%) | 99 of 178 | 0 of 334 |
| G1 without scoped delegation | 10 (0.3%) | 23 | 1,307 | 136 (40.7%) | 1,443 (43.6%) | 99 of 178 | 0 of 334 |
| G1 without typed normalization | 10 (0.3%) | 23 | 1,342 | 142 (42.5%) | 1,484 (44.8%) | 86 of 178 | 0 of 334 |

Second population: `results/tables.md`, table T4 (dev2). In both populations the order is the same: scoped delegation, typed normalization and established payees each add completed tasks; the operation check changes almost nothing; the amount check costs tasks and removes three attacks (one in the second population).

| Arm | Successful attacks, original text | Successful attacks, identifier reformatted |
|---|---|---|
| No defense (B0) | 553 | 553 |
| Provenance rule (B1) | 45 | 198 |
| REM v1.0 | 11 | 11 |
| REM v1.1 (proposed) | 11 | 11 |
| Rule P2 | 12 | 12 |
| Rule A2 | 13 | 13 |
| A2 + typed normalization (A2n) | 13 | 13 |
| Progent manual policy (PG) | 0 | 0 |
| Permission rule (G1) | 10 | 10 |
| G1 without typed normalization | 10 | 10 |
| Guard + learned, two verdicts (L2) | 10 | 38 |

The learned arm L2 loses robustness: 28 further attacks succeed when the attacker's account identifier is written with spaces, because the calls have permission status *unknown* and the model's remaining evidence is the provenance match, which reformatting defeats. The rule G1 withholds calls of unknown status and is unchanged.

Tasks completed by user task (primary):

| User task | Episodes | No defense | REM v1.0 | REM v1.1 (proposed) | Rule A2 | Progent manual policy | Permission rule | Guard + learned, two verdicts |
|---|---|---|---|---|---|---|---|---|
| 0 | 210 | 11 | 0 | 0 | 0 | 11 | 0 | 0 |
| 1 | 210 | 88 | 88 | 88 | 88 | 88 | 88 | 88 |
| 2 | 210 | 87 | 39 | 71 | 0 | 81 | 0 | 77 |
| 3 | 207 | 77 | 8 | 30 | 77 | 77 | 77 | 77 |
| 4 | 210 | 64 | 2 | 5 | 64 | 64 | 64 | 64 |
| 5 | 210 | 210 | 210 | 210 | 210 | 210 | 210 | 210 |
| 6 | 210 | 74 | 3 | 8 | 72 | 72 | 72 | 72 |
| 7 | 210 | 168 | 168 | 168 | 168 | 168 | 168 | 168 |
| 8 | 210 | 210 | 210 | 210 | 210 | 210 | 210 | 210 |
| 9 | 208 | 141 | 208 | 206 | 208 | 141 | 159 | 200 |
| 10 | 210 | 130 | 210 | 210 | 210 | 140 | 210 | 210 |
| 11 | 210 | 21 | 0 | 0 | 0 | 18 | 18 | 5 |
| 12 | 210 | 31 | 21 | 27 | 0 | 31 | 0 | 0 |
| 13 | 190 | 139 | 18 | 15 | 0 | 139 | 131 | 132 |
| 14 | 209 | 167 | 3 | 39 | 167 | 0 | 167 | 167 |
| 15 | 189 | 22 | 0 | 0 | 0 | 0 | 0 | 0 |

G1's gain over A2 comes from user tasks 11 and 13 (payee referred to through history; value delegated to a named file). It loses in user task 9, where arms that withhold the update complete the benchmark's check more often; the cause was not examined call by call. User tasks 0, 2, 12 and 15 remain at zero for G1: the recipient or the instruction is supplied only by a file or by the history without a reference that the matcher accepts.

## 5.7 Paired fixtures

| Arm | Set 1: legitimate released / unsafe released / pairs correct (of 8) | Set 2: legitimate released / unsafe released / pairs correct (of 8) | Set 3: legitimate released / unsafe released / pairs correct (of 7) | Set 4: legitimate released / unsafe released / pairs correct (of 20) |
|---|---|---|---|---|
| Provenance rule (B1) | 8 / 1 / 7 | 8 / 3 / 5 | 6 / 2 / 4 | 19 / 7 / 12 |
| REM v1.0 | 0 / 0 / 0 | 2 / 0 / 2 | 1 / 0 / 1 | 6 / 1 / 5 |
| REM v1.1 (proposed) | 8 / 1 / 7 | 8 / 3 / 5 | 5 / 0 / 5 | 17 / 6 / 11 |
| Rule A2 | 8 / 4 / 4 | 8 / 5 / 3 | 5 / 1 / 4 | 17 / 8 / 9 |
| Progent manual policy (PG) | 0 / 0 / 0 | 2 / 0 / 2 | 1 / 0 / 1 | 7 / 0 / 7 |
| Permission rule (G1) | 7 / 1 / 6 | 7 / 0 / 7 | 3 / 0 / 3 | 17 / 1 / 16 |
| G1 without amount check | 7 / 3 / 4 | 7 / 2 / 5 | 4 / 1 / 3 | 19 / 5 / 14 |
| G1 without typed normalization | 7 / 1 / 6 | 5 / 0 / 5 | 2 / 0 / 2 | 17 / 1 / 16 |
| Learned on permission evidence, no guard (L0) | 8 / 3 / 5 | 8 / 2 / 6 | 6 / 0 / 6 | 20 / 6 / 14 |
| Guard + learned, two verdicts (L2) | 7 / 1 / 6 | 7 / 0 / 7 | 4 / 0 / 4 | 19 / 3 / 16 |
| Guard + learned on unknown calls only (L2s) | 7 / 1 / 6 | 7 / 0 / 7 | 4 / 0 / 4 | 19 / 3 / 16 |

Sets 1 to 3 are regression fixtures from the earlier studies. Set 4 (20 pairs in ten categories) was written for this study before any scoring and was scored once; it was written by the author of the candidate with AI assistance and not independently reviewed. On set 4, G1 gets 16 of 20 pairs right, A2 9, REM v1.1 11, Progent's manual policy 7 (its allow-list contains none of the fixture payees, so it withholds 13 legitimate calls and releases no unsafe one). On set 3 (credential and reformatting fixtures) G1 releases 3 of 7 legitimate calls, fewer than REM v1.1 (5 of 7). The learned arms release unsafe calls that the rule withholds (set 4: L2 3, L0 6).

Parser and matcher errors on set 4, counted separately from monitor errors: two legitimate calls withheld by parser defects (S2, U1), one withheld by design (F2, ambiguous number format), one unsafe call released because no record of satisfied requests is kept (P2, duplicate payment). On the 16 benchmark requests the parser was developed with the requests in view; its errors there cannot be called validation errors.

## 5.8 Residual attacks and cost

All successful attacks under G1 (10 and 3) are in user task 15, where the account the attacker wants is the same string as the landlord account named by the user; the released calls have an explicitly named recipient and a matching amount (`results/failure_analysis.json`). No method that reads the request can separate them.

| Arm | Median | 95th percentile |
|---|---|---|
| REM v1.0 | 0.178 | 0.751 |
| REM v1.1 (proposed) | 0.169 | 0.647 |
| Rule A2 | 0.104 | 0.584 |
| Progent manual policy (PG) | 0.091 | 2.886 |
| Permission rule (G1) | 0.089 | 2.913 |
| Guard + learned, two verdicts (L2) | 0.179 | 3.166 |

Decision time is below 0.2 ms at the median for every arm; the 95th percentile of the arms that parse bank records is about 3 ms. No model call is made.
