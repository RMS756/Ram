# Code-to-Thesis Traceability (R4)

**Audited version:**
- branch `claude/rem-r4-corrections-3ktvze`;
- code at commit `bec4d1c`, whose `rem/` and `experiments/` files are byte-identical to `9ab3f9e` (the R4 thesis commit) and were last changed in `ea621c3`;
- thesis: `REM_FINAL_THESIS/chapters_R4/`.

**Audit date:** 2 November 2026.

**Status codes:**
- **MATCH**: the code implements the thesis statement, verified by reading and/or an executed check.
- **MATCH (conv.)**: it matches under a convention the thesis states.
- **DIFF**: the code differs from the thesis text.
- **PARTIAL**: only part of the statement is implemented.
- **ABSENT**: specified in the thesis but not implemented.
- **NOT EVAL.**: implemented but not used for any reported result.

**Evidence columns:** "Test" names the existing unit test file. "Audit check" names a check run in this audit (`logs/audit_invariants.log`, `logs/audit_results.log`, `logs/e2e_example.log`).

## 1. Runtime path: proposed tool call → verdict → mitigation (evaluated path)

The evaluated path is the replay harness. The frozen five-layer `RemPipeline` (`rem/core/pipeline.py:147`) is not used for any reported number (§4).

| # | Step | Implementation (file:line) | Thesis location | Test / output | Status |
|---|---|---|---|---|---|
| 1 | AgentDojo replays the recorded assistant message; each proposed call reaches the guarded executor | `rem/integration/agentdojo_replay.py:289-308` (`ReplayLLM`), `:317-343` (`GuardedToolsExecutor.query`) | Ch. 3 §3.11.11 (NO-ADAPT replay); Ch. 4 §4.9 | `tests/test_replay.py`; audit check e2e Part B | MATCH (replay only, not live) |
| 2 | Calls naming an unknown tool return an error **without** passing through REM | `agentdojo_replay.py:327-332` | — (not stated) | — | DIFF (minor: no side effect occurs, but no audit record is written) |
| 3 | The decision point opens, and untrusted segments since the last decision point are collected | `rem/algorithms/behavior/evidence.py:186-192`; `agentdojo_replay.py:320` | Ch. 3 §3.6.1, interpretation I-1 | `tests/test_evidence.py` | MATCH |
| 4 | Evidence vector x_t from history and the proposed arguments only (computed before execution) | `evidence.py:199-273` | Ch. 3 Tables 3.8–3.9 | Audit check `features_precede_result_ingestion` PASS | MATCH |
| 5 | Consequence tier k_t from tool category and amount | `rem/algorithms/decision/consequence.py:89-100` | Ch. 3 Tables 3.10–3.11 | `tests/test_contract_compliance.py`; audit `tier_boundaries` | MATCH (exploratory values) |
| 6 | Reference label y_t looked up for the audit record and the idealised reviewer | `agentdojo_replay.py:173`; `rem/integration/agentdojo_traces.py:217-223` | Ch. 3 §3.11.3 | — | MATCH. The label is not an input of A3 or B1 (verified: only `_decide_oracle_modify` and `_mitigate` read it) |
| 7 | Logit s_t = β₀ + βᵀx_t | `agentdojo_replay.py:86-87` (`FrozenScorer.logit`) | Eq. 3.1 | Audit `ridge_refit_matches_committed_coefficients` PASS | MATCH |
| 8 | Calibrated p_t = σ(γ₁s_t + γ₀), with γ₁ > 0 enforced | `agentdojo_replay.py:83-84, 177` | Eq. 3.3 | `tests/test_frozen_math.py` | MATCH |
| 9 | Predicates D1 (Π) and D2 (missing evidence at k ≥ k_D2) | `rem/algorithms/decision/policy.py:53-63`; required-evidence name mapping in `experiments/pilot/run_main.py:189-193` | Ch. 3 §3.7.4 | `tests/test_a3.py` | MATCH (Π = ∅; D2 fired on 58 steps) |
| 10 | Feasible set 𝒱(a): Modify only for tools in 𝒯_R | `policy.py:65-70` | Ch. 3 §3.7.5 | `tests/test_a3.py` | MATCH |
| 11 | Conditional risk R(v) = (1−p)L(v,0,k) + pL(v,1,k) | `rem/algorithms/decision/expected_loss.py:201-233`; `rem/algorithms/a3.py:95` | Eq. 3.6 | Audit `a3_verdict_equals_bruteforce_argmin` PASS (0 / 160,008) | MATCH |
| 12 | Verdict v* = argmin, with ties counted and the Ch. 3 order applied in the experiments | `a3.py:96-104`; `run_main.py:323` (`tie_mode="record_chapter3_order"`) | Eq. 3.7 | 0 ties in all runs | MATCH (conv.): SC-2 unresolved; the frozen default `raise` is not used in the experiments |
| 13 | Loss grid L(v,y,k) with L(Mod,1,k) = r_mod(k)·C_miss(k) | `rem/algorithms/decision/loss_matrix.py:72-84` | Table 3.13; Eq. 3.5 | `tests/test_frozen_math.py` | MATCH |
| 14 | r_mod(k) from oracle-Modify replay on the fitting folds | `run_main.py:256-258, 265-316` | Ch. 3 §3.8 property 3 says "estimated from **enforcing-mode runs**"; §3.11.7 says oracle replay | Audit `r_mod_residual_episodes` | **DIFF** (property 3 vs implementation); see CV-3 |
| 15 | Mitigation, step-level: Allow → release; Modify, Block and unapproved Escalate → withhold the current call | `agentdojo_replay.py:236-258` | Ch. 3 §3.8; CLAUDE.md mitigation lock | `tests/test_mitigation_semantics.py`; e2e Part B (call withheld before execution) | MATCH. Modify ≡ Block on the current call (stated in Ch. 3 line 549) |
| 16 | Mitigation, episode-level: Modify restricts the tool class; Block restricts all of 𝒯_R for the rest of the episode | `agentdojo_replay.py:238-240, 250-256` | Ch. 3 Table 3.14 | `tests/test_mitigation_semantics.py` | MATCH (sensitivity variant) |
| 17 | Escalate: "idealized" releases iff y = 0; "no_reviewer" withholds | `agentdojo_replay.py:244-248` | Ch. 3 §3.11.7 | — | MATCH. Both reviewer models are bounds, not reviewers |
| 18 | Execution happens only if released; the result is ingested as untrusted | `agentdojo_replay.py:333-342` | Ch. 3 TB-2 | e2e Part B: the withheld `send_money` was not executed and replay security = False | MATCH |
| 19 | Linear attribution φ_i = β_i(x_i − x̄_i); base value; additivity recorded | `rem/algorithms/attribution/linear_shapley.py:128-156`; `agentdojo_replay.py:189-195` | Eqs. 3.11–3.13 | Audit `attribution_completeness` PASS (max error 2.2e-15) | MATCH; computed **after** the verdict (audit-only) |
| 20 | Audit record (digest of arguments, features, p, tier, risks, verdict, mechanism) | `agentdojo_replay.py:197-229`; `rem/core/audit.py` | Ch. 3 §3.10; Ch. 4 | `tests/test_contract_compliance.py` | MATCH |
| 21 | Partial and complete-call timers | `agentdojo_replay.py:169, 186, 231` | Ch. 4 §4.14 (R4) | `tests/test_latency_instrumentation.py` | MATCH |

## 2. Offline fitting and evaluation

| Component | Implementation (file:line) | Thesis | Test / output | Status |
|---|---|---|---|---|
| Label y = 1: the call matches the tool of an injection-task reference call and carries the attacker value in the declared key arguments; read tools are excluded | `agentdojo_traces.py:208-223`; config `labels` (`configs/exploratory/pilot_e0.yaml:73-79`) | Ch. 3 §3.11.3 | `tests/test_traces.py`; audit `label_semantics` | MATCH. An *attempt* label, not causation (CV-4) |
| AM-1 exclusion of pairs whose legitimate reference call is labelled 1 under suite v1 | `agentdojo_traces.py:230-237`; `experiments/pilot/build_dataset.py:41-43` | Ch. 5 §5.2 | 21 episodes excluded | MATCH; does not remove the user_task_15 collision of older recorded suite versions (CV-4) |
| Outer folds: attacked by injection task; benign by user task (round robin) | `experiments/pilot/data.py:37-67` | Ch. 3 §3.11.5 | `dataset_summary.json` | MATCH |
| x_beh4 benign reference refitted on the fitting rows only | `data.py:70-92`; `rem/integration/steps.py:144-157` | Ch. 3 §3.11.6 (AM-2) | — | MATCH |
| Nested CV: λ from inner out-of-fold log-loss; ties go to the stronger penalty | `rem/evaluation/crossfit.py:130-155` | Proc. 3.1 lines 3–4 | `tests/test_crossfit.py` | MATCH |
| Ridge objective: summed NLL + (λ_impl/2)‖β‖², intercept unpenalised, Newton without line search | `rem/algorithms/detection/ridge_logistic.py:261-291, 295-307` | Eq. 3.2 (summed log-likelihood − λ‖β‖²; λ = λ_impl/2 stated at line 319 and in Table 3.17 notes) | Audit `ridge_kkt` PASS (gradient 1e-13) | MATCH (conv.). Loss is a **sum** in both the thesis and the code, so the grid is not per-sample |
| Calibrator fitted on inner out-of-fold logits; the map is applied to the refitted model | `crossfit.py:157-171` | Proc. 3.1 lines 5–7 | — | MATCH (small train/apply distribution mismatch, inherent to the design) |
| Calibration by label NLL (primary) and Platt-smoothed targets (secondary) | `rem/algorithms/calibration/logit_nll.py:30-65`; `rem/algorithms/calibration/platt.py:159-228`; `run_main.py:133` | Eq. 3.4; SC-4 | Audit `calibration_label_nll_recovers_parameters` PASS; `calibration_rejects_negative_slope` PASS | MATCH |
| B1 thresholds θ(α) from out-of-fold calibrated y = 0 training steps | `crossfit.py:170-175`; `rem/algorithms/a1.py:35-100` | Eq. 3.14 | `tests/test_a1.py` | MATCH. B1 blocks a read tool when θ_mod ≤ p < θ_blk (`a1.py:99`), a detail not stated in Ch. 3 |
| Same estimator for REM and B1 | `run_main.py:323-339, 503-504` (both use `label_nll_primary` fits) | Ch. 3 §3.11.7 | — | MATCH: the comparison isolates the decision rule, but REM also has an Escalate option (REMnoEsc variant provided) |
| ROC-AUC (ties ½), AP (step, no interpolation), ECE (right-closed bins, M = 10), log-loss (clip 1e-6), Brier (both conventions) | `rem/evaluation/probabilistic.py:45-144` | Eqs. 3.20–3.21; SC-5 | Audit `heldout_*` PASS | MATCH (Ch. 3 withholds the Brier score; Ch. 5 reports it) |
| ASR = mean over AM-4-valid attacked episodes of AgentDojo `security` (attacker goal reached in the post-environment); benign utility = AgentDojo `utility` on benign episodes | `run_main.py:521-553` | Ch. 3 §3.12.1 | Audit `replay_*` | MATCH; Ch. 3 says "(enforcing mode)" but only replay exists |
| Grouped / stratified bootstrap (2,000; seed 20261027) | `rem/evaluation/bootstrap.py:26-84` | Ch. 3 §3.11.9 | `tests/test_reproducibility.py` | MATCH |
| Realized loss (Eq. 3.22) | `run_main.py:419-420` | Eq. 3.22 | — | MATCH; favours REM by construction (stated) |
| Control regret against an oracle | — | Cited (Zhang et al.) but not defined | — | **ABSENT** |
| CUSUM (A2), observe-only | `rem/algorithms/behavior/cusum.py:30-73`; `rem/algorithms/a2.py:47-100`; `run_main.py:615-674` | Eqs. 3.15–3.19 | `tests/test_a2.py`; `e3_a2_cusum_observe_only.json` | MATCH. It is never imported by the guard or the policies, so it has no effect on execution |

## 3. Features (Ch. 3 Tables 3.8–3.9)

| Feature | Implementation (`evidence.py`) | Thesis definition | Status | Note |
|---|---|---|---|---|
| x_ctx1, injection classifier | — | Table 3.8 | **ABSENT** | Blocked (no classifier chosen; no network) |
| x_ctx2, instruction pattern in new untrusted segments | `:210-211` | Table 3.8 | MATCH | Patterns were written with knowledge of the AgentDojo templates (disclosed in config line 90) |
| x_beh1, last result untrusted and matches a pattern | `:213-215` | Table 3.8 | MATCH | — |
| x_beh2, consecutive repeats / n_max | `:217-225` | Table 3.8, I-2 | MATCH | Fold injection_task_6 coefficient **−0.043**, so "retries raise risk" does not hold there (CV-7) |
| x_beh3, privilege escalation | `:227-229` | Table 3.8, I-3 | MATCH | Fires on any first transfer |
| x_beh4, transition not in the benign reference | `:231-233`; recomputed in `steps.py:153-154` | Table 3.8, I-4 | MATCH | — |
| x_act1, a key argument occurs in untrusted text and not in trusted text | `:235-245`; matcher `provenance.py:145-171` | Table 3.9 | MATCH | Numbers match any numeric token, for example amount 3 vs the date "2022-03-10" (audit `provenance_matcher_boundary_cases`). An IBAN split by spaces is missed |
| x_act2, destination novelty | `:247-249` | Table 3.9 (benign history) | **PARTIAL** | Reduced to "recipient not in the objective" (I-5) |
| x_act3, sensitive egress | `:251-255` | Table 3.9, I-6 | MATCH | — |
| Missing values | `available` flags (`:245`, `:266-268`) and D2 | Ch. 3 §3.7.4 | MATCH | Only x_act1 can be unavailable; the others are always computable |
| Normalisation | All features are in [0, 1] by construction; no scaling | Eq. 3.1 ("x ∈ [0,1]^d") | MATCH | — |
| Episode reset | A new `RemGuard`/`EpisodeTracker` per replay job (`run_main.py:225-235`; `agentdojo_replay.py:146-155`) | Ch. 3 §3.6.1 | MATCH | — |

## 4. Architecture claims

| Claim | Evidence | Status |
|---|---|---|
| Exactly five layers (Input & Context → Detection → Behavioural Analysis → Decision Engine → Mitigation) | `rem/core/pipeline.py:56-76, 147-337` names five layers. The evaluated path (`RemGuard`) implements them as one function, with no layer objects | MATCH in the frozen code; PARTIAL in the evaluated path |
| Detection layer = ridge LR on context evidence | In the evaluated path, "Detection" contributes only x_ctx2 (a regex). The estimator combines all eight features | PARTIAL |
| No sixth layer / no feedback loop | Fitting is offline (`crossfit.py`); no online update in `RemGuard` | MATCH |
| SHAP is not a decision input | Attribution is computed after `_mitigate` (`agentdojo_replay.py:183` before `:189-195`); `tests/test_contract_compliance.py` | MATCH |
| CUSUM is observe-only | Not referenced in `agentdojo_replay.py`, `a3.py` or `a1.py` | MATCH |
| Fail-closed configuration | `rem/config/loader.py:43-190` (frozen configs). The pilot reads raw YAML (`experiments/pilot/common.py:34-36`): a missing key raises `KeyError`, but the loader's UNRESOLVED semantics are not used | PARTIAL |
| Non-invasive placement | The guard wraps AgentDojo's `ToolsExecutor` (`agentdojo_replay.py:310-343`); the agent's model, prompts and tools are unchanged. This requires control of the tool executor (Ch. 4 §4.9) | MATCH (in the sandbox) |
| Frozen `RemPipeline` / `DeterministicMitigationEngine` produce the results | Unit-tested only (`tests/test_pipeline.py`, `tests/test_mitigation.py`); no result file is produced by them | **NOT EVAL.** |
