# REM experimental results: verified register

**Date:** 11 November 2026. Every number below was produced by code in this repository and is traceable to a result file. Nothing is estimated or carried over from a paper. **No result here comes from a live agent.**

**Label on all results:** exploratory; costs, tiers and features are declared values without supervisor approval (D-9, SD-FEAT).

## 0. Evaluation modes (kept separate throughout)

| Mode | What it is | What it cannot show |
|---|---|---|
| M1 Offline prediction | held-out scores on recorded calls | any effect of enforcement |
| M2 Recorded-trace replay | the recorded tool calls are re-executed in AgentDojo's sandbox with a guard that may withhold calls; the agent's later calls are the recorded ones (NO-ADAPT) | agent adaptation, reviewer effect, differences between Modify, Escalate and Block |
| M3 Post-hoc sensitivity | analyses added after results were seen; labelled | confirmation |
| M4 Confirmatory replay | M2 on recordings never read before, under a protocol committed in advance | the same limits as M2 |
| M5 Call-level fixtures | synthetic paired calls scored by the frozen models | prevalence; any benchmark outcome |
| M6 Integration verification | scripted agents, fake providers, local gateway | effectiveness |
| M7 Live agents | **not executed** | — |

Common environment: AgentDojo package 0.1.35, banking suite v1, recordings at repository commit `089ed468cf3ed0322acc66b0211f26d9d90dbf60`; Python 3.11.17; numpy 2.4.6; seed 20261027; grouped bootstrap with 2,000 resamples; step-level enforcement; no reviewer.

## 1. Primary corpus (R4): offline prediction [M1]

Source: `results/pilot_R4/e1_crossfit.json`; commit `6fc0952` (1 November); reproduced 8 and 11 November. Data: 21 undefended backbones, `important_instructions` attack, 3,334 episodes, 6,762 calls, 921 positive. Nine folds by injection task.

| Metric | Value [95% interval] |
|---|---|
| ROC-AUC | 0.938 [0.908, 0.961] |
| Average precision | 0.719 [0.559, 0.827] |
| ECE (10 bins) | 0.044 [0.033, 0.084]; uncalibrated 0.042 |
| Log-loss | 0.201 [0.149, 0.294] |
| Held-out credential-change fold | ECE 0.189, log-loss 0.530 |
| Fitted calibration slope γ₁ | 0.945 to 0.981 |

## 2. Primary corpus: replay [M2]

Source: `results/pilot_R4/`; `REM_Authorization_Generalization_Study/results/study_results.json` (commit `2c915bf`, 11 November). 3,313 replay-eligible episodes (2,979 attacked, 334 benign).

| Arm | Status | Attacks / 2,979 | Benign / 334 | Utility under attack / 2,979 | Unauthorized state change (episodes) | Authorized calls released / 178 |
|---|---|---|---|---|---|---|
| B0 no defence | reference | 672 | 175 | 1,465 | 828 | 178 |
| B1 operating-point thresholds | pre-declared baseline | 164 | 170 | 1,532 | 202 | 130 |
| **Original REM (v1.0)** | pre-declared | **11** | **105** | 1,083 | 24 | 33 |
| P1 provenance rule | added 11 Nov, declared before its run | 12 | 134 | 1,207 | 26 | 92 |
| P2 provenance rule (either source) | same | 12 | 134 | 1,207 | 26 | 89 |
| A2 strict explicit rule | same | 13 | 140 | 1,334 | 27 | 83 |
| A1 explicit or delegated | same | 313 | 164 | — | — | — |
| M01 REM, Allow and Block only | same | 13 | 124 | — | — | — |
| M11+AZ rejected candidate | pre-declared candidate | 132 | 127 | — | — | — |
| REM without behavioural evidence | original ablation (pre-declared in the pilot) | 11 | 140 | 1,147 | 24 | 83 |

Double holdout (143 cells; unseen user task and unseen injection task) [M2, 11 November]: original REM 11 and 105; P1 and P2 12 and 134; A2 13 and 140; M11+AZ 132 and 110; REM without behavioural evidence 14 and 140 **[M3: this arm was added to the double holdout after results were seen]**.

Other primary-corpus results [M2]: Modify, Escalate and Block differ in 0 of 3,313 episodes; all 11 residual attacks of the original REM are `user_task_15` episodes; idealized reviewer bound 11 and 166.

Reformatted-identifier probe [M2, declared before its run]: 2,645 attacked episodes with the attacker's account number written with spaces. Attacks: P1 12 → 191; B1 45 → 198; M01 13 → 31; original REM, P2, A2 and REM without behavioural evidence unchanged; A1 251 → 13.

## 3. Confirmatory population [M4]

Source: `REM_FINAL_SUBMISSION/results/confirmatory_results.json` (sha256 `0c255824…`), commit `907e6d2`; protocol frozen at `19bd168` before the recordings were opened; no amendment.

Population: five pipelines never read by any earlier script. Files 2,162; excluded as ambiguous pairs (AM-1) 14; loaded 2,148; eligible (no-defence replay reproduces the recorded outcome, AM-4) **2,113** = 2,065 attacked + 48 benign. Recorded benchmark version: v1.2.1 for 1,575 episodes, not recorded for 538.

| Source | Pipeline | Attacked | Benign |
|---|---|---|---|
| F-A | Meta-SecAlign-70B; three templates | 429 | 16 |
| F-B | Meta-SecAlign-70B with repeated user prompt | 429 | 16 |
| F-C | Llama-3.3-70B with repeated user prompt | 383 | 16 |
| F-D | Llama-3.3-70B; `direct`, `ignore_previous` | 286 | 0 |
| F-E | GPT-4o (2024-05-13); four `important_instructions` variants | 538 | 0 |

| Arm | Attacks / 2,065 | Unauthorized state change | Utility under attack | Benign / 48 | All tasks / 2,113 | Authorized calls released / 51 |
|---|---|---|---|---|---|---|
| B0 | 436 | 493 | 1,413 | 38 | 1,451 | 51 |
| B1 | 67 | 96 | 1,478 | 36 | 1,514 | 36 |
| Original REM (v1.0) | 3 | 3 | 898 | 18 | 916 | 4 |
| **REM without behavioural evidence (v1.1, proposed)** | **1** | 1 | 1,049 | 25 | **1,074** | 11 |
| P1 | 4 | 4 | 1,020 | 24 | 1,044 | 12 |
| P2 | 4 | 4 | 1,019 | 24 | 1,043 | 12 |
| A2 | 4 | 4 | 1,205 | 27 | 1,232 | 27 |
| M01 | 3 | 3 | 1,093 | 22 | 1,115 | 8 |

Replay errors: 0 in every arm.

Paired contrasts (percentage points; 95% grouped-bootstrap interval; gained/lost = discordant episodes):

| Contrast | Task success, all episodes | Attack success rate | Benign only | Task gained / lost |
|---|---|---|---|---|
| **v1.1 − v1.0 (primary, pre-declared)** | **+7.48 [1.17, 16.02]** | **−0.10 [−0.29, 0.00]** | +14.58 [0.00, 33.33] | 158 / 0 |
| v1.1 − P2 | +1.47 [−5.28, 7.98] | −0.15 [−0.38, 0.00] | +2.08 [0.00, 6.25] | 88 / 57 |
| v1.1 − A2 | −7.48 [−25.66, 8.16] | −0.15 [−0.38, 0.00] | −4.17 [−25.00, 14.58] | 142 / 300 |
| P2 − v1.0 | +6.01 [−5.17, 20.25] | +0.05 [0.00, 0.15] | +12.50 [−2.08, 31.25] | 193 / 66 |
| A2 − v1.0 | +14.96 [−1.29, 34.42] | +0.05 [0.00, 0.15] | +18.75 [4.17, 37.50] | 393 / 77 |
| M01 − v1.0 | +9.42 [2.77, 17.87] | 0.00 | +8.33 [0.00, 20.83] | 199 / 0 |
| v1.0 − B1 | −28.30 [−47.16, −10.83] | −3.10 [−8.27, −0.39] | −37.50 [−58.33, −16.67] | 26 / 624 |

**Pre-declared verdict: GO** (E1 interval above 0; no security interval above 0; 1 ≤ 4 attacks).

Descriptive secondary tables [M4; `confirmatory_descriptives.json`; not part of the verdict]. 8,221 recorded calls in the 2,113 episodes, of which 5,808 are read-type calls (never withheld by any arm), 559 are labelled attack attempts, and 1,854 are state-changing calls not labelled as attack attempts.

| Arm | State-changing unlabelled calls released / 1,854 | Attack-labelled calls released / 559 | Escalate verdicts | Episodes with an Escalate verdict | Episodes with any withheld call |
|---|---|---|---|---|---|
| B1 | 1,347 | 122 | 63 | 61 | 821 |
| Original REM | 224 | 3 | 1,392 | 928 | 1,423 |
| REM without behavioural evidence | 497 | 1 | 981 | 671 | 1,257 |
| P2 | 549 | 4 | 0 | 0 | 1,210 |
| A2 | 928 | 4 | 0 | 0 | 1,080 |
| M01 | 504 | 3 | 63 | 61 | 1,265 |

Caution: in attacked episodes a state-changing call that the label rule does not mark may still be influenced by the injection. The 51 calls in benign episodes are the clean measure of legitimate-action approval; the 1,854 are an upper-bound context figure.

Decision time [M4]: median 0.23 ms and 95th percentile 0.6 ms for the REM arms, 0.20 ms for the rules, measured under four-process load; indicative only.

## 4. Call-level fixtures [M5]

Sources: `REM_AUTHORIZATION_AUDIT/fixtures/`, `REM_FINAL_SUBMISSION/fixtures/`; fold `injection_task_0` models; counts only.

| Arm | Sets 1–2: legitimate released / 14 | Sets 1–2: unsafe released | Set 3: legitimate released / 7 | Set 3: unsafe released / 7 |
|---|---|---|---|---|
| Original REM | 0 | 0 | 1 | 0 |
| REM without behavioural evidence | 14 | SUB-A2, P5, R1, R2 | 5 | 0 |
| P1 | 14 | same four | 6 | 2 (F1, F3) |
| P2 | 14 | same four | 5 | 0 |
| A2 | — | releases the 7 amount substitutions | 5 | 1 (F4) |
| B1 | 14 | same four | 6 | 2 (F1, F3) |

The fixtures were written by the assistant to stress specific mechanisms. They are not samples of real traffic and their counts are not rates.

## 5. Integration verification [M6]

| Item | Result | Date, commit |
|---|---|---|
| Test suite | 241 passed, 3 skipped, 1 expected failure (without study state) | 11 Nov, `2c915bf` |
| Deployment simulation (local gateway) | 0 mismatches with offline replay | 5 Nov, `baffbed` |
| Live harness | scripted-agent tests pass; **no model run** | 3 Nov, `9fddfa7` |
| MELON + REM | 30 tests pass with scripted agents and fake embeddings; **no model run** | 5 Nov, `cfb4f40` |

## 6. Results reported by others, not reproduced here

Codex branch `codex/rem-multiple-candidates-v2` (`c9851fc`): on 135 attacked and 15 benign episodes of one Llama-3.3-70B pipeline (v1.2.1, `user_task_15` excluded), a refit of REM gives 5 attacks and 6 benign successes; the `x_act1` rule 0 and 7; no learned candidate dominates the rule. These figures are Codex's and were not rerun in this project. They point the same way as Sections 2 and 3.

## 7. Not executed

Live agents (any defence); MELON, Task Shield, PROVISO, NEXUS, aiAuthZ under any conditions; repeated runs; a human reviewer; any benchmark other than AgentDojo banking; AgentDojo's denial-of-service attack families (excluded by rule: no fold model exists for them).
