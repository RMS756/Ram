# Results tables (generated from committed result files; no value typed by hand)

Sources: `results/rem_lite/2026-11-05/rem_lite_results.json` (replay, offline), `results/deployment_sim/2026-11-05_four_configs/summary.json` (deployment simulation). Mode A = recorded traces of 21 real agents, AgentDojo banking v1, `important_instructions`; NO-ADAPT replay; 3,313 valid episodes (2,979 attacked, 334 benign). Intervals: 95% grouped bootstrap (attacked: by injection task; benign: by user task).

## Table R1. Main comparison (Mode A: recorded traces; Mode B live: NOT EXECUTED)

| Configuration | ASR | Benign utility | Utility under attack | Defence latency per call, median (ms) | End-to-end episode latency, median (ms) | LLM calls added by defence | API cost |
|---|---|---|---|---|---|---|---|
| No Defense | 0.226 [0.148, 0.295] | 0.524 [0.381, 0.676] | 0.492 [0.479, 0.503] | 0.09 | 30.9 | 0 | 0 (recorded traces; no model call) |
| REM-Lite | 0.055 [0.011, 0.134] | 0.509 [0.334, 0.702] | 0.514 [0.501, 0.527] | 0.17 | 31.5 | 0 | 0 (recorded traces; no model call) |
| Full REM | 0.004 [0.001, 0.007] | 0.314 [0.110, 0.548] | 0.364 [0.345, 0.389] | 0.18 | 30.0 | 0 | 0 (recorded traces; no model call) |
| MELON | Not executed | Not executed | Not executed | Not executed | Not executed | Not executed (≥ 1 masked LLM call per loop iteration + embeddings, by design) | Not executed |

No Defense's defence latency is the gateway's allow-all evaluation (feature computation without a decision rule). End-to-end latency is per replayed episode through the deployment simulation (client → REM gateway → simulated bank, localhost, 4 concurrent episodes); it contains no LLM time. Live (Mode B) values for all four configurations: **Not executed**.

## Table R2. Paired differences on matched replay episodes

| Comparison | ΔASR | Δ Utility under attack | Δ Benign utility | Attacked pairs (a secure, b breached) / (a breached, b secure) / both breached |
|---|---|---|---|---|
| Full REM − REM-Lite | -0.051 [-0.130, -0.007] | -0.151 [-0.172, -0.126] | -0.195 [-0.341, -0.074] | 153 / 0 / 11 |
| REM-Lite − No Defense | -0.171 [-0.246, -0.092] | 0.022 [0.014, 0.030] | -0.015 [-0.099, 0.062] | 508 / 0 / 164 |
| Full REM − No Defense | -0.222 [-0.289, -0.146] | -0.128 [-0.151, -0.102] | -0.210 [-0.379, -0.051] | 661 / 0 / 11 |

## Table R3. Mitigation decisions on held-out steps (observe-only; 6,762 steps: 921 attack, 5,841 legitimate)

| Configuration | Intervene on attack steps | Intervene on legitimate steps | Attack steps: allow / modify / escalate / block | Legitimate steps: allow / modify / escalate / block | Realized loss (declared grid, base) |
|---|---|---|---|---|---|
| REM-Lite | 0.740 | 0.056 | 239 / 378 / 0 / 304 | 5513 / 218 / 58 / 52 | 0.652 |
| Full REM | 0.973 | 0.227 | 25 / 626 / 234 / 36 | 4516 / 219 / 1089 / 17 | 0.114 |

REM-Lite and the thesis's B1 produce identical verdicts on 6762 of 6762 steps; Full REM changes 1658 verdicts relative to REM-Lite. The realized loss uses the declared exploratory cost matrix (C_FA = 1; C_miss = 1/5/10/20; C_mod = 0.5; C_esc = 0.3). It is a decision-quality measure under those declared costs, **not a measurement of financial loss**; sensitivity to the cost grid is in thesis §4.9.

## Table R4. Calibration of the risk probability (held-out, step level, 6,762 steps)

| Probability used by | ECE (10 bins) | Brier (binary) | Log loss | ROC-AUC |
|---|---|---|---|---|
| REM-Lite (uncalibrated p~) | 0.0415 | 0.0598 | 0.2014 | 0.9393 |
| Full REM (calibrated p) | 0.0438 | 0.0603 | 0.2013 | 0.9383 |

Calibration produced no improvement here (the uncalibrated probability is marginally better calibrated); this matches thesis §4.4. Pooled ROC-AUC differs slightly because each outer fold has its own calibration map: strictly increasing within a fold, so it does not change any within-fold ranking or any threshold decision, but pooling across folds can reorder steps from different folds (values from E1, `results/pilot_R2/e1_crossfit.json`).

## Table R5. Failure and error cases

| Item | Count |
|---|---|
| Replay errors (B0) | 0 |
| Replay errors (REMLite_step_level_no_reviewer) | 0 |
| Replay errors (REM_step_level_no_reviewer) | 0 |
| Deployment-simulation errors (all four configurations) | 0 |
| Episodes excluded as invalid (recorded outcome not reproducible in the sandbox, AM-4) | 21 of 3,334 |
| Withheld calls that reached the bank backend | 0 (backend executed 22774 = released 22774) |
| Attack successes remaining under Full REM (valid attacked episodes) | 11 of 2,979 |
