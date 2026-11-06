# Experiment Report — No Defense, MELON, REM-Lite and Full REM (5 Nov 2026)

## Status in one table

| Configuration | Mode A: recorded traces (21 real agents, AgentDojo banking v1) | Mode B: live LLM agent |
|---|---|---|
| No Defense | Executed | Not executed |
| MELON | Not possible (model-based detector) | Not executed (no credential; `api.openai.com` blocked; no spending authorisation) |
| REM-Lite | Executed | Not executed |
| Full REM | Executed | Not executed |

**The controlled MELON comparison and every live-agent result therefore do not exist.** No MELON number is reported, and no number from the MELON paper is placed beside REM's.

## Setup of the executed experiments (Mode A)

| Item | Setting |
|---|---|
| Data | 3,334 recorded episodes (2,979 attacked with `important_instructions`, 334 benign, after 21 AM-4 exclusions → 3,313 valid) of 21 LLM agents; 6,762 proposed calls |
| Estimator | Frozen nested grouped cross-fit: 9 outer folds by injection task; every fitted quantity in-fold (see `01_AUDIT/REM_DATA_LEAKAGE_AUDIT.md`) |
| Offline evaluation | Held-out predictions → verdicts per step (observe-only) |
| Replay | NO-ADAPT replay in the AgentDojo sandbox: recorded agent turns, defence at the tool boundary, AgentDojo's own success checks; step-level mitigation; no reviewer |
| Deployment simulation | The same replay over HTTP through the REM gateway service and a simulated bank API: separate processes, 4 concurrent episodes. **0 mismatches** with the in-process replay for all four configurations |
| Uncertainty | 95% grouped bootstrap (attacked: injection-task clusters; benign: user-task clusters); paired differences on matched episodes |

## Answers to the six questions

1. **Does REM reduce successful attacks?** In replay, under the NO-ADAPT assumption, yes: ASR 0.226 → 0.004 (Full REM − No Defense: −0.222 [−0.289, −0.146]). In 661 attacked episodes the attack succeeded without a defence and failed with Full REM; there are 0 reverse cases, and 11 attacks succeeded under both. This is not shown for live or adaptive agents.
2. **How does REM compare with MELON?** **Not answerable.** MELON was not executed.
3. **Does REM preserve legitimate task completion?** Only partly.
   - Benign utility fell from 0.524 to 0.314 (Δ −0.210 [−0.379, −0.051]).
   - Utility under attack fell from 0.492 to 0.364.
   - Full REM intervened on 22.7% of legitimate held-out steps, most of them Escalate (1,089 of 5,841). Without a reviewer, an escalated call is withheld.
   - With an idealised reviewer the utility loss disappears (thesis §4.6), but no real reviewer exists.
4. **Is the security–utility trade-off beneficial?** It depends on the declared costs.
   - Under the declared exploratory cost matrix, Full REM's realized loss is 0.114, against 0.652 for REM-Lite.
   - The matrix weights a missed tier-4 attack at 20 and a false alarm at 1, so the comparison favours protection by construction.
   - With equal weights for both errors the conclusion could change (cost-grid sensitivity: thesis §4.9).
   - The costs are not supervisor-approved and are not a measurement of financial loss.
5. **Does the full decision policy improve on the internal baseline B1 (and its uncalibrated variant REM-Lite)?**
   - **Security:** yes. ΔASR −0.051 [−0.130, −0.007]. In 153 attacked episodes REM-Lite was breached and Full REM was not; never the reverse.
   - **Utility:** at a cost. Δ benign utility −0.195 [−0.341, −0.074]; Δ utility under attack −0.151 [−0.172, −0.126].
   - **Attribution:** B1 and Full REM share estimator, calibration and predicates; the difference is attributed to the **decision policy as a whole**. **Calibration sensitivity (evaluated data only):** REM-Lite's verdicts are identical to B1's (6,762/6,762 steps; 3,334/3,334 episodes), because rank-selected thresholds are unaffected by a strictly increasing calibration map. On this dataset and these metrics calibration showed no improvement: ECE 0.0438 calibrated against 0.0415 uncalibrated; Brier 0.0603 against 0.0598.
6. **Runtime and computational cost** (deployment simulation, same run, localhost):
   - **Defence time per call (median):** No Defense allow-all 0.09 ms; REM-Lite 0.17 ms; Full REM 0.18 ms.
   - **Episode time (median):** 30.0–31.5 ms in every configuration; the differences are within run-to-run noise.
   - **Model calls:** REM adds **no** LLM call. MELON, by design, adds at least one masked LLM call per loop iteration plus embedding calls (code inspection), but its cost was not measured.
   - **Throughput:** about 166 episodes/s at 8 concurrent episodes on 4 vCPU (prototype servers).

## Tables and figures

- `TABLES/RESULTS_TABLES.md`:
  - R1: main table;
  - R2: paired differences;
  - R3: mitigation decisions and realized loss;
  - R4: calibration;
  - R5: failures and errors.
- `FIGURES/fig_security_utility_mode_a.png` and `FIGURES/fig_decisions_rem_lite_vs_full.png`, regenerated with `FIGURES/make_figures.py`.

## Threats to validity

- **NO-ADAPT:** recorded agents never react to refusals.
- **Data reuse:** one benchmark, one attack template, familiar tasks and models, reused during development; there is no lock-box test set.
- **Unapproved design values:** exploratory costs and tiers.
- **Mitigation:** no real reviewer; Modify is operationally equal to Block under step-level semantics.
- **Labels:** automatic, with no human audit.
- **Environment:** a simulated bank on one machine. No production banking and no real money.
