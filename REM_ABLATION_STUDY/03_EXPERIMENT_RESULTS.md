# 03 Experiment results: REM v1.0 component ablation (21 November 2026)

**What was executed**
- **Offline recorded-trace replay only** (NO-ADAPT), under the protocol frozen at `93e6630` (`01`), with no amendment.
- **Data:** 6,107 eligible episodes across three populations, each replayed in 9 arms: **54,963 analysed episode replays**. In all, 55,584 replays were executed, including the 69 loaded episodes that failed the eligibility rule, with 0 replay errors.
- **Fresh state:** the fitted state comes from a fresh run of the frozen pilot pipeline, which reproduced REM v1.0 exactly: 11 / 2,979, 105 / 334, 1,083 / 2,979 (`results/reproduction_gate.json`).

**What was not executed**
- **Closed-loop ablation: NOT EXECUTED.** It needs a real agent model, and there is no model endpoint or API credential, no GPU, and model hosts are blocked by the network policy (re-checked 21 Nov). The closed-loop table is therefore absent, not empty.

**How to read the numbers**
- **Call-level rates.** These describe REM's decisions on recorded calls; they are **not attack success rates**.
- **Replay episode outcomes.** These are AgentDojo's checks after replay. The agent never sees a refusal, so they are **not closed-loop ASR or task completion**.
- **Development data.** P1 was used to design REM v1.0. P2 and P3 are stricter (unseen templates, and unseen backbones and templates) but were read before this study (R2 and 11 Nov), so **no population is an independent holdout**.

## 1 Summary of findings

| Component (arm) | Attack-labelled calls withheld | Legitimate calls blocked in benign episodes | Verdict under the protocol rules |
|---|---|---|---|
| **Learned decision**: estimator + calibration + expected loss (A3 = predicates only) | Without it: **0** of 907 / 202 / 559 (P1 / P2 / P3), against 882 / 200 / 556 with it; Δ −97.2 / −99.0 / −99.5 pp, intervals exclude 0 | Without it: 6 / 178 (P1) and 1 / 51 (P3), against 145 / 178 and 47 / 51; Δ −78.1 pp [−100.0, −53.4] (P1) | **Measurable contribution to attack-call withholding on all three populations, and a measurable cost in benign-call blocking.** Every call whose release it changes, it withholds. |
| **Deterministic controls** D1 / D2 (A3P = learned only) | no change on any population | no change | **No measurable contribution.** Only 6 / 3 / 10 unlabelled calls in attacked episodes change (D2 escalations). |
| **Detection evidence** `x_ctx2` (A1a) | no change | no change | **No measurable contribution.** 5 / 2 / 0 unlabelled-call release changes. |
| **Detection layer** `x_ctx2` + `x_beh1` (A1b, new refit) | no change | no change | **No measurable contribution.** Held-out ROC-AUC 0.937 vs 0.938. |
| **Behavioural evidence** (A2) | P1 2 + / 2 −; P3 2 more withheld; Δ intervals include 0 | P1: removing it lowers benign-call blocking by 28.1 pp [−54.1, −8.6]. P3: −13.7 pp [−37.5, 0.0]. | **Measurable utility cost on P1** (it adds false-positive blocking); security effect not resolved; on P3 not resolved |
| **Input & Context provenance evidence** (AIC) | Without it: 833 / 191 / 505 withheld. Δ −5.4 [−17.0, 0.0] (P1), −4.5 [−13.0, 0.4] (P2), **−9.1 [−23.5, −0.7] (P3)** | Without it, blocking rises: +16.3 pp [−1.9, 39.2] (P1); 51 / 51 blocked (P3) | **Measurable contribution to attack-call withholding on P3; not resolved on P1 and P2.** Removing it also makes benign blocking worse (point estimates). |
| **Mitigation in shadow mode** (A4) | 0 withheld, but **882 / 200 / 556 attack-labelled calls flagged** | 0 blocked | **Enforcement carries all of the effect.** Shadow verdicts equal enforced verdicts on 99.6% / 99.7% / 99.7% of calls. Divergence arises from history: tool outputs differ when calls are withheld. |
| **Input & Context hygiene** | – | – | **Not exercised:** 0 of 16,727 tool-output segments contain characters it removes. An ablation would be a provable no-op on these traces. |

## 2 The learned decision (priority question)

**The earlier observation does not apply to REM v1.0.** The observation that "deterministic controls give the same decisions as learned variants" came from the exploratory REM-B family (R8, Section 4.5.6), where a request-derived guard decided first. REM v1.0 has no such guard. Its only deterministic controls are D1 (prohibited tools) and D2 (high tier with missing evidence).

1. **Does the learned score change final decisions?** Yes.
   - 2,129 / 553 / 2,123 call releases change between A0 and A3 (P1 / P2 / P3), and every one is a withholding by the learned decision.
   - Episode level (P1): 661 replay attack outcomes are removed and none added; McNemar p = 2.1e-199, which ignores clustering.
2. **Does it catch attack calls that deterministic controls miss?** Yes.
   - D1 and D2 alone withhold **no** attack-labelled call in any population.
   - The learned decision withholds 882 of 907, 200 of 202 and 556 of 559.
3. **Does it add blocking of legitimate calls?** Yes.
   - 139 of 178 legitimate restricted calls in benign episodes on P1, and 46 of 51 on P3, are withheld only because of it.
   - It also withholds 1,108 / 353 / 1,521 unlabelled calls in attacked episodes. These are mostly the user's own task.
   - Withhold precision is 0.40 / 0.34 / 0.25.
4. **Under stricter settings** (P2 unseen attack templates; P3 unseen backbones and templates), the pattern is the same, with attack-call withholding of 99.0% and 99.5%. Benign blocking on P3 is 92.2% (47 / 51).
5. **Computational overhead.**
   - Median complete-call time is 0.151 ms with the learned path and 0.070 ms without it; p95 is 0.388 vs 0.300 ms.
   - This is about +0.08 ms per call on one CPU container. It includes the audit attribution, which runs only when a scorer exists.
6. **Useful where aggregates hide it?** Within REM v1.0 the learned decision is not hidden: it is the arm whose removal changes everything. Conversely, **removing the deterministic controls changes nothing measurable**. The redundant component in REM v1.0 is the predicate layer, not the learned decision.

## 3 Generated tables (per population)


### P1_primary: 3313 eligible episodes (2979 attacked, 334 benign) of 3313 loaded

#### Call level (restricted tools)

| Arm | Attack-labelled withheld / calls | Withholding rate % [95% CI] | Benign-episode calls withheld / calls | Benign-call blocking % [95% CI] | Unlabelled calls in attacked episodes withheld / calls | Precision | Median / p95 ms |
|---|---|---|---|---|---|---|---|
| B0 | 0 / 907 | 0.0 [0.0, 0.0] | 0 / 178 | 0.0 [0.0, 0.0] | 0 / 1466 | n/a | 0.067 / 0.286 |
| A0 | 882 / 907 | 97.2 [95.5, 98.5] | 145 / 178 | 81.5 [56.6, 100.0] | 1160 / 1466 | 0.403 | 0.151 / 0.388 |
| A1a | 882 / 907 | 97.2 [95.5, 98.5] | 145 / 178 | 81.5 [56.6, 100.0] | 1165 / 1466 | 0.402 | 0.146 / 0.375 |
| A1b | 882 / 907 | 97.2 [95.5, 98.5] | 145 / 178 | 81.5 [56.6, 100.0] | 1155 / 1466 | 0.404 | 0.147 / 0.394 |
| A2 | 882 / 907 | 97.2 [95.3, 98.5] | 95 / 178 | 53.4 [31.0, 83.7] | 941 / 1466 | 0.460 | 0.146 / 0.378 |
| AIC | 833 / 907 | 91.8 [79.9, 97.9] | 174 / 178 | 97.8 [95.5, 100.0] | 1267 / 1466 | 0.366 | 0.142 / 0.371 |
| A3 | 0 / 907 | 0.0 [0.0, 0.0] | 6 / 178 | 3.4 [0.0, 11.2] | 52 / 1466 | 0.000 | 0.070 / 0.300 |
| A3P | 882 / 907 | 97.2 [95.5, 98.5] | 145 / 178 | 81.5 [56.6, 100.0] | 1154 / 1466 | 0.404 | 0.148 / 0.392 |
| A4 | 0 / 907 | 0.0 [0.0, 0.0] | 0 / 178 | 0.0 [0.0, 0.0] | 0 / 1466 | n/a | 0.143 / 0.364 |

#### Paired comparison with A0 (arm − A0)

| Arm | Δ attack-call withholding pp [95% CI] | Δ benign-call blocking pp [95% CI] | Call verdict changes | Call release changes (class: direction = count) | Δ replay attack outcome pp [95% CI] (NO-ADAPT) | Discordant episodes arm/A0 (McNemar p) | Δ replay benign completion pp [95% CI] (NO-ADAPT) |
|---|---|---|---|---|---|---|---|
| B0 | -97.24 [-98.55, -95.49] | -81.5 [-100.0, -56.6] | 2187 | attack_labelled:released by arm = 882; benign_episode:released by arm = 145; unlabelled_in_attacked_episode:released by arm = 1160 | 22.19 [14.55, 28.86] | 661/0 (2.09e-199) | 21.0 [5.1, 37.9] |
| A1a | 0.00 [0.00, 0.00] | 0.0 [0.0, 0.0] | 21 | unlabelled_in_attacked_episode:withheld by arm = 5 | 0.00 [0.00, 0.00] | 0/0 (–) | 0.0 [0.0, 0.0] |
| A1b | 0.00 [0.00, 0.00] | 0.0 [0.0, 0.0] | 137 | unlabelled_in_attacked_episode:withheld by arm = 10; unlabelled_in_attacked_episode:released by arm = 15 | 0.00 [0.00, 0.00] | 0/0 (–) | 0.0 [0.0, 0.0] |
| A2 | 0.00 [-0.39, 0.31] | -28.1 [-54.1, -8.6] | 465 | attack_labelled:withheld by arm = 2; attack_labelled:released by arm = 2; benign_episode:released by arm = 50; unlabelled_in_attacked_episode:withheld by arm = 4; unlabelled_in_attacked_episode:released by arm = 223 | 0.00 [-0.10, 0.10] | 1/1 (1) | 10.5 [1.2, 22.6] |
| AIC | -5.40 [-17.00, 0.00] | 16.3 [-1.9, 39.2] | 1220 | attack_labelled:withheld by arm = 5; attack_labelled:released by arm = 54; benign_episode:withheld by arm = 30; benign_episode:released by arm = 1; unlabelled_in_attacked_episode:withheld by arm = 260; unlabelled_in_attacked_episode:released by arm = 153 | 0.20 [-0.07, 0.43] | 9/3 (0.146) | 0.0 [0.0, 0.0] |
| A3 | -97.24 [-98.55, -95.49] | -78.1 [-100.0, -53.4] | 2129 | attack_labelled:released by arm = 882; benign_episode:released by arm = 139; unlabelled_in_attacked_episode:released by arm = 1108 | 22.19 [14.55, 28.86] | 661/0 (2.09e-199) | 22.5 [8.0, 38.5] |
| A3P | 0.00 [0.00, 0.00] | 0.0 [0.0, 0.0] | 6 | unlabelled_in_attacked_episode:released by arm = 6 | 0.00 [0.00, 0.00] | 0/0 (–) | 0.0 [0.0, 0.0] |
| A4 | -97.24 [-98.55, -95.49] | -81.5 [-100.0, -56.6] | 30 | attack_labelled:released by arm = 882; benign_episode:released by arm = 145; unlabelled_in_attacked_episode:released by arm = 1160 | 22.19 [14.55, 28.86] | 661/0 (2.09e-199) | 21.0 [5.1, 37.9] |

#### Replay episode outcomes (NO-ADAPT; not closed-loop ASR or task completion)

| Arm | Replay attack outcomes / attacked | Replay tasks completed under attack | Replay benign completed / benign |
|---|---|---|---|
| B0 | 672 / 2979 | 1465 | 175 / 334 |
| A0 | 11 / 2979 | 1083 | 105 / 334 |
| A1a | 11 / 2979 | 1081 | 105 / 334 |
| A1b | 11 / 2979 | 1094 | 105 / 334 |
| A2 | 11 / 2979 | 1147 | 140 / 334 |
| AIC | 17 / 2979 | 1062 | 105 / 334 |
| A3 | 672 / 2979 | 1509 | 180 / 334 |
| A3P | 11 / 2979 | 1078 | 105 / 334 |
| A4 | 672 / 2979 | 1465 | 175 / 334 |

Shadow mode (A4): verdict agreement with enforced A0 on 6654 of 6684 calls; episodes with at least one diverging verdict: 30; calls executed although the shadow verdict would withhold them: 2190; attack-labelled calls flagged in shadow: 882 / 907.

### P2_cross_template: 681 eligible episodes (681 attacked, 0 benign) of 715 loaded

#### Call level (restricted tools)

| Arm | Attack-labelled withheld / calls | Withholding rate % [95% CI] | Benign-episode calls withheld / calls | Benign-call blocking % [95% CI] | Unlabelled calls in attacked episodes withheld / calls | Precision | Median / p95 ms |
|---|---|---|---|---|---|---|---|
| B0 | 0 / 202 | 0.0 [0.0, 0.0] | 0 / 0 | n/a | 0 / 468 | n/a | 0.074 / 0.285 |
| A0 | 200 / 202 | 99.0 [97.6, 100.0] | 0 / 0 | n/a | 379 / 468 | 0.345 | 0.150 / 0.361 |
| A1a | 200 / 202 | 99.0 [97.6, 100.0] | 0 / 0 | n/a | 381 / 468 | 0.344 | 0.153 / 0.378 |
| A1b | 200 / 202 | 99.0 [97.6, 100.0] | 0 / 0 | n/a | 382 / 468 | 0.344 | 0.147 / 0.363 |
| A2 | 200 / 202 | 99.0 [97.6, 100.0] | 0 / 0 | n/a | 283 / 468 | 0.414 | 0.147 / 0.356 |
| AIC | 191 / 202 | 94.6 [86.0, 99.1] | 0 / 0 | n/a | 414 / 468 | 0.316 | 0.148 / 0.371 |
| A3 | 0 / 202 | 0.0 [0.0, 0.0] | 0 / 0 | n/a | 26 / 468 | 0.000 | 0.075 / 0.273 |
| A3P | 200 / 202 | 99.0 [97.6, 100.0] | 0 / 0 | n/a | 376 / 468 | 0.347 | 0.146 / 0.358 |
| A4 | 0 / 202 | 0.0 [0.0, 0.0] | 0 / 0 | n/a | 0 / 468 | n/a | 0.145 / 0.354 |

#### Paired comparison with A0 (arm − A0)

| Arm | Δ attack-call withholding pp [95% CI] | Δ benign-call blocking pp [95% CI] | Call verdict changes | Call release changes (class: direction = count) | Δ replay attack outcome pp [95% CI] (NO-ADAPT) | Discordant episodes arm/A0 (McNemar p) | Δ replay benign completion pp [95% CI] (NO-ADAPT) |
|---|---|---|---|---|---|---|---|
| B0 | -99.01 [-100.00, -97.62] | n/a | 579 | attack_labelled:released by arm = 200; unlabelled_in_attacked_episode:released by arm = 379 | 25.26 [18.57, 30.65] | 172/0 (3.34e-52) | n/a |
| A1a | 0.00 [0.00, 0.00] | n/a | 4 | unlabelled_in_attacked_episode:withheld by arm = 2 | 0.00 [0.00, 0.00] | 0/0 (–) | n/a |
| A1b | 0.00 [0.00, 0.00] | n/a | 28 | unlabelled_in_attacked_episode:withheld by arm = 4; unlabelled_in_attacked_episode:released by arm = 1 | 0.00 [0.00, 0.00] | 0/0 (–) | n/a |
| A2 | 0.00 [0.00, 0.00] | n/a | 164 | unlabelled_in_attacked_episode:released by arm = 96 | 0.00 [0.00, 0.00] | 0/0 (–) | n/a |
| AIC | -4.46 [-13.00, 0.43] | n/a | 334 | attack_labelled:withheld by arm = 1; attack_labelled:released by arm = 10; unlabelled_in_attacked_episode:withheld by arm = 83; unlabelled_in_attacked_episode:released by arm = 48 | 0.15 [-0.30, 0.59] | 2/1 (1) | n/a |
| A3 | -99.01 [-100.00, -97.62] | n/a | 553 | attack_labelled:released by arm = 200; unlabelled_in_attacked_episode:released by arm = 353 | 25.26 [18.57, 30.65] | 172/0 (3.34e-52) | n/a |
| A3P | 0.00 [0.00, 0.00] | n/a | 3 | unlabelled_in_attacked_episode:released by arm = 3 | 0.00 [0.00, 0.00] | 0/0 (–) | n/a |
| A4 | -99.01 [-100.00, -97.62] | n/a | 5 | attack_labelled:released by arm = 200; unlabelled_in_attacked_episode:released by arm = 379 | 25.26 [18.57, 30.65] | 172/0 (3.34e-52) | n/a |

#### Replay episode outcomes (NO-ADAPT; not closed-loop ASR or task completion)

| Arm | Replay attack outcomes / attacked | Replay tasks completed under attack | Replay benign completed / benign |
|---|---|---|---|
| B0 | 174 / 681 | 504 | 0 / 0 |
| A0 | 2 / 681 | 302 | 0 / 0 |
| A1a | 2 / 681 | 300 | 0 / 0 |
| A1b | 2 / 681 | 299 | 0 / 0 |
| A2 | 2 / 681 | 370 | 0 / 0 |
| AIC | 3 / 681 | 271 | 0 / 0 |
| A3 | 174 / 681 | 530 | 0 / 0 |
| A3P | 2 / 681 | 299 | 0 / 0 |
| A4 | 174 / 681 | 504 | 0 / 0 |

Shadow mode (A4): verdict agreement with enforced A0 on 1592 of 1597 calls; episodes with at least one diverging verdict: 5; calls executed although the shadow verdict would withhold them: 579; attack-labelled calls flagged in shadow: 200 / 202.

### P3_second_population: 2113 eligible episodes (2065 attacked, 48 benign) of 2148 loaded

#### Call level (restricted tools)

| Arm | Attack-labelled withheld / calls | Withholding rate % [95% CI] | Benign-episode calls withheld / calls | Benign-call blocking % [95% CI] | Unlabelled calls in attacked episodes withheld / calls | Precision | Median / p95 ms |
|---|---|---|---|---|---|---|---|
| B0 | 0 / 559 | 0.0 [0.0, 0.0] | 0 / 51 | 0.0 [0.0, 0.0] | 0 / 1803 | n/a | 0.095 / 0.286 |
| A0 | 556 / 559 | 99.5 [98.7, 100.0] | 47 / 51 | 92.2 [74.5, 100.0] | 1583 / 1803 | 0.254 | 0.159 / 0.353 |
| A1a | 556 / 559 | 99.5 [98.7, 100.0] | 47 / 51 | 92.2 [74.5, 100.0] | 1583 / 1803 | 0.254 | 0.153 / 0.358 |
| A1b | 556 / 559 | 99.5 [98.7, 100.0] | 47 / 51 | 92.2 [74.5, 100.0] | 1579 / 1803 | 0.255 | 0.153 / 0.359 |
| A2 | 558 / 559 | 99.8 [99.4, 100.0] | 40 / 51 | 78.4 [52.6, 96.7] | 1317 / 1803 | 0.291 | 0.152 / 0.342 |
| AIC | 505 / 559 | 90.3 [76.0, 98.9] | 51 / 51 | 100.0 [100.0, 100.0] | 1624 / 1803 | 0.232 | 0.156 / 0.356 |
| A3 | 0 / 559 | 0.0 [0.0, 0.0] | 1 / 51 | 2.0 [0.0, 7.5] | 62 / 1803 | 0.000 | 0.087 / 0.261 |
| A3P | 556 / 559 | 99.5 [98.7, 100.0] | 47 / 51 | 92.2 [74.5, 100.0] | 1573 / 1803 | 0.256 | 0.149 / 0.353 |
| A4 | 0 / 559 | 0.0 [0.0, 0.0] | 0 / 51 | 0.0 [0.0, 0.0] | 0 / 1803 | n/a | 0.149 / 0.351 |

#### Paired comparison with A0 (arm − A0)

| Arm | Δ attack-call withholding pp [95% CI] | Δ benign-call blocking pp [95% CI] | Call verdict changes | Call release changes (class: direction = count) | Δ replay attack outcome pp [95% CI] (NO-ADAPT) | Discordant episodes arm/A0 (McNemar p) | Δ replay benign completion pp [95% CI] (NO-ADAPT) |
|---|---|---|---|---|---|---|---|
| B0 | -99.46 [-100.00, -98.66] | -92.2 [-100.0, -74.5] | 2186 | attack_labelled:released by arm = 556; benign_episode:released by arm = 47; unlabelled_in_attacked_episode:released by arm = 1583 | 20.97 [16.85, 24.63] | 433/0 (9.02e-131) | 41.7 [10.4, 70.8] |
| A1a | 0.00 [0.00, 0.00] | 0.0 [0.0, 0.0] | 7 | none | 0.00 [0.00, 0.00] | 0/0 (–) | 0.0 [0.0, 0.0] |
| A1b | 0.00 [0.00, 0.00] | 0.0 [0.0, 0.0] | 119 | unlabelled_in_attacked_episode:released by arm = 4 | 0.00 [0.00, 0.00] | 0/0 (–) | 0.0 [0.0, 0.0] |
| A2 | 0.36 [0.00, 1.09] | -13.7 [-37.5, 0.0] | 467 | attack_labelled:withheld by arm = 2; benign_episode:released by arm = 7; unlabelled_in_attacked_episode:released by arm = 266 | -0.10 [-0.29, 0.00] | 0/2 (0.5) | 14.6 [0.0, 33.3] |
| AIC | -9.12 [-23.45, -0.74] | 7.8 [0.0, 25.5] | 1148 | attack_labelled:withheld by arm = 1; attack_labelled:released by arm = 52; benign_episode:withheld by arm = 4; unlabelled_in_attacked_episode:withheld by arm = 204; unlabelled_in_attacked_episode:released by arm = 163 | 0.24 [0.00, 0.58] | 6/1 (0.125) | 0.0 [0.0, 0.0] |
| A3 | -99.46 [-100.00, -98.66] | -90.2 [-100.0, -72.4] | 2123 | attack_labelled:released by arm = 556; benign_episode:released by arm = 46; unlabelled_in_attacked_episode:released by arm = 1521 | 20.92 [16.82, 24.58] | 432/0 (1.8e-130) | 43.8 [14.6, 70.8] |
| A3P | 0.00 [0.00, 0.00] | 0.0 [0.0, 0.0] | 10 | unlabelled_in_attacked_episode:released by arm = 10 | 0.00 [0.00, 0.00] | 0/0 (–) | 0.0 [0.0, 0.0] |
| A4 | -99.46 [-100.00, -98.66] | -92.2 [-100.0, -74.5] | 23 | attack_labelled:released by arm = 556; benign_episode:released by arm = 47; unlabelled_in_attacked_episode:released by arm = 1583 | 20.97 [16.85, 24.63] | 433/0 (9.02e-131) | 41.7 [10.4, 70.8] |

#### Replay episode outcomes (NO-ADAPT; not closed-loop ASR or task completion)

| Arm | Replay attack outcomes / attacked | Replay tasks completed under attack | Replay benign completed / benign |
|---|---|---|---|
| B0 | 436 / 2065 | 1413 | 38 / 48 |
| A0 | 3 / 2065 | 898 | 18 / 48 |
| A1a | 3 / 2065 | 898 | 18 / 48 |
| A1b | 3 / 2065 | 902 | 18 / 48 |
| A2 | 1 / 2065 | 1049 | 25 / 48 |
| AIC | 8 / 2065 | 838 | 18 / 48 |
| A3 | 435 / 2065 | 1458 | 39 / 48 |
| A3P | 3 / 2065 | 893 | 18 / 48 |
| A4 | 436 / 2065 | 1413 | 38 / 48 |

Shadow mode (A4): verdict agreement with enforced A0 on 8198 of 8221 calls; episodes with at least one diverging verdict: 21; calls executed although the shadow verdict would withhold them: 2186; attack-labelled calls flagged in shadow: 556 / 559.

A1b refit: features ['x_beh2', 'x_beh3', 'x_beh4', 'x_act1', 'x_act2', 'x_act3']; held-out ROC-AUC 0.9367, PR-AUC 0.7030.
Hygiene check: 0 of 16727 tool-output segments would be changed.

## 4 Statistical notes

- **Intervals.** Grouped percentile bootstrap: 2,000 resamples, clusters = injection task (attacked) or user task (benign). Calls are never resampled independently.
- **Small samples.** Benign-call metrics rest on 178 calls in 334 episodes from 16 user tasks (P1), and 51 calls in 48 episodes (P3). Their intervals are wide, and P2 has no benign episodes.
- **"[0.0, 0.0]"** means no resample moved. It does not mean certainty.
- **McNemar p-values** use discordant episodes and ignore clustering, so they are anti-conservative. They are reported as a sensitivity analysis only.
- **Effect sizes** are the paired differences in percentage points.

## 5 Limitations

1. **NO-ADAPT replay.** A withheld call cannot change what the recorded agent proposes next. The ablations' effects on retries, re-planning and closed-loop task completion are not measured.
2. **Development and previously read data.** Results for A0, A1a, A2, AIC, A3 and A3P on P1 were known from R8. P2 and P3 were read before.
3. **Labels.** Reference-matched attempt labels, not audited by a human. The "unlabelled calls in attacked episodes" have no legitimacy label of their own.
4. **One benchmark** (AgentDojo banking). Absent component: the injection classifier `x_ctx1`.
5. **Latency.** Measured in replay on a shared container. It is not a deployment latency.
