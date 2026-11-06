# REM — Data Leakage Audit

**Question:** was REM trained, calibrated or tuned on the AgentDojo banking cases it is evaluated on, and does any reported number use test labels in fitting?

## 1. Data

All REM fitting and evaluation data are recorded AgentDojo **banking v1** traces of 21 real LLM agents:
- 3,334 episodes and 6,762 proposed calls;
- `important_instructions` attack plus benign runs;
- 16 user tasks and 9 injection tasks.

## 2. Split design (verified in code: `rem/evaluation/crossfit.py`, `experiments/pilot/data.py`)

**Outer folds.** There are 9 outer folds, grouped by **injection task** (attacker objective):
- an attacked episode belongs to the fold of its injection task;
- a benign episode belongs to the fold its user task is assigned to round-robin.

All steps of one episode stay in one fold.

**What is fitted inside each fold, on its fitting portion only:**

| Quantity | How it is fitted |
|---|---|
| Ridge penalty λ | Selected by an inner 4-fold cross-validation |
| Coefficients | Fitted on the fitting portion |
| Calibration (γ₀, γ₁) | Fitted on inner out-of-fold logits |
| B1 / REM-Lite thresholds | Selected on benign inner out-of-fold probabilities (development data) |
| x̄ (attribution baseline) | Fitting portion only |
| Benign transition reference (x^beh₄) | Fitting portion only |
| r_mod | Oracle-Modify replays within the fitting folds |
| Feature-group retention (pilot E0) | Per fold, fitting portion only |

**Test predictions:** held-out predictions for a fold come only from that fold's fit.

## 3. Findings

| Check | Finding | Severity |
|---|---|---|
| Training and testing share episodes | **No.** An episode is in exactly one outer fold | — |
| Same attack objective in train and test | **No** for the attack objective (held out by fold). **Yes** for the *template*: `important_instructions` is shared, so the held-out unit is the objective, not the attack style | Limits generalisation to new objectives with the same template |
| Same user tasks in train and test | **Yes.** All 16 user tasks appear in every fold's fitting data (in other episodes) | Evaluation is on **familiar tasks**; no unseen-task claim |
| Same backbones in train and test | **Yes.** All 21 agents appear in every fold | No unseen-model claim (a leave-one-backbone-out sensitivity exists: ROC-AUC 0.74–1.00) |
| Calibration uses final-test labels | **No.** Inner out-of-fold labels only | — |
| Hyperparameters tuned on test | **No** for λ, calibration and thresholds. **Yes, indirectly** for design-level choices: costs, tiers and predicates were declared before the pilot, but the post-hoc REM-without-Escalate comparison (AM-series) and the user_task_15 sensitivity were added after seeing results, and are labelled post hoc | Disclosed; no number is re-tuned |
| Evaluation cases reused during development | **Yes.** The same benchmark was used for the pilot, the ablations and the replay; there is no untouched lock-box set | All results are labelled **exploratory**; a confirmatory test needs new data or a pre-registered live run |
| Label rule | Automatic reference-match rule (exploratory); AI-only inspection; **no human audit**; user_task_15 collision handled post hoc (D-6) | Disclosed |

## 4. Consequences for this validation package

- REM-Lite and Full REM are compared on **identical held-out predictions and identical replay episodes**, so their *relative* comparison is leakage-free within this design.
- No result is presented as an unseen-task, unseen-model or confirmatory evaluation.
- The historical exploratory results are preserved unchanged (`results/pilot_R2`, `pilot_R4`). Nothing was deleted or re-tuned.
- A **clean held-out test** for a future live run would hold out user tasks *and* attacker objectives, or use a pre-registered confirmatory set. Within AgentDojo banking (16 user × 9 injection tasks) this leaves very little data, which is a stated limitation, not something to work around.
