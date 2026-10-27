# Experiment Validity Report — Exploratory Pilot E0–E6

**Status: EXPLORATORY — NOT THESIS RESULTS — SUPERVISOR DECISION REQUIRED**

Date: 27 Oct 2026. Every number below comes from an executed run whose code, configuration and
outputs are in this repository:

| Item | Location |
|---|---|
| Pre-registered design (committed before any run) | `configs/exploratory/pilot_e0.yaml` (commit `48bef90`) |
| Amendments AM-1..AM-4 (committed before any held-out prediction) | `configs/exploratory/pilot_e0_amendments.yaml` (commit `7a707a7`) |
| Code that produced the results | commit `aa66f22`; `experiments/pilot/` + `rem/` |
| Reproduction | `PYTHON=<python with agentdojo 0.1.35> experiments/pilot/run_all.sh` (≈10 min, 4 cores) |
| Result files (each stamped with label, commit, config hash, AgentDojo version) | `results/pilot/*.json`, `results/pilot/figures/` |

A complete second run from commit `aa66f22` reproduced every reported number exactly
(deterministic seeds; no sampling outside the seeded bootstrap).

---

## 0. CONFLICT WITH THE CHAPTER 3 SCOPE — SUPERVISOR DECISION REQUIRED

**Affected specification (Chapter 3 Sec. 3.1.4, "Out of scope"):**
> "Counterfactual estimation of intervention value by replaying agent trajectories."

**Conflict.**
- The enforcement results in this report (E4, the enforcement half of E5, the cross-template ASR) were produced by replaying recorded agent trajectories under REM. That is the method Chapter 3 places out of scope.
- The measured r_mod(k) values were also produced by replay, and they enter REM's loss grid through Eq. 3.5. The observe-only verdicts (E2, E5-observe, E6) therefore depend on replay too, although only through r_mod. With r_mod = 1 (the pre-registered value for unmeasured tiers), Modify would be priced as ineffective.
- Chapter 3 Sec. 3.11.1 specifies enforcing-mode runs with a live LLM agent. These are **BLOCKED** in this environment, because no LLM API is available.
- The substitution was made to obtain any enforcement evidence at all. It was not authorised by the Chapter 3 scope, and it was identified only after the runs.

**Consequence.**
- No replay-derived number may be presented as a Chapter 3 enforcing-mode result.
- The discrimination and calibration results (E0, E1) and the A2 analysis (E3) do not depend on replay.

**Options for the supervisor:**
- (a) Discard the replay results.
- (b) Report them only as an exploratory, explicitly out-of-scope sensitivity analysis.
- (c) Amend the Chapter 3 scope to admit replay with the NO-ADAPT assumption stated.

Until a decision is made, every replay-derived number in this repository is labelled accordingly.

---

## 1. What was actually done

### 1.1 Data — real agent traces, not synthetic data

- **Source.** The `runs/` directory of the AgentDojo repository (commit `089ed468…`):
  - traces of real LLM agents recorded by the benchmark authors;
  - banking suite, attack template `important_instructions`;
  - 21 undefended backbones.
- **No live LLM was called.** No API access is available in this environment.
- **Dataset size** (`results/pilot/dataset_summary.json`):
  - 3,360 trace files;
  - 3,334 episodes used, after excluding:
    - 5 errored episodes;
    - 21 episodes of the label-ambiguous pair in AM-1;
  - 6,762 proposed tool calls ("steps");
  - **921 positive steps.**
- **Independence.** The episodes are **not** i.i.d. observations:
  - 16 user tasks × 9 injection tasks × 21 backbones share templates, an attacker account and an environment;
  - all uncertainty is therefore estimated by **grouped** bootstrap: attacked episodes are resampled by injection task, benign episodes by user task.

### 1.2 Two evaluation modes

1. **Observe-only (E1, E2, E3, E5-observe, E6).**
   - Recorded steps are scored by models fitted without the step's outer fold (Procedure 3.1).
   - Verdicts are computed and logged, not enforced.
2. **Enforcement replay (E4, E5-enforce).**
   - Each recorded episode is re-executed in AgentDojo's own sandbox, with REM as a guarded `ToolsExecutor`.
   - The benchmark's own utility and security checks score the result.
   - **Assumption NO-ADAPT:** the replayed agent does not react to a refusal; it emits the calls it emitted in the record.
   - A real agent might retry, rephrase or choose another tool. Replay ASR therefore **does not** measure robustness to adaptive agents or adaptive attackers.

### 1.3 Replay validity

- An all-Allow replay (B0) reproduced the recorded utility and security of **3,313 of 3,334** episodes (99.4%).
- Lowest per-backbone agreement: gpt-4o-2024-05-13 at 93.7%.
- Enforcement metrics use only the 3,313 reproduced episodes (AM-4).

---

## 2. Results (pooled, held-out, 95% grouped-bootstrap intervals)

### 2.1 Pilot E0 — fitting portions only

| Evidence group | Mean fitting-portion ROC-AUC (9 folds) | Retained (≥ 0.55) |
|---|---|---|
| Context (x_ctx2 only; x_ctx1 BLOCKED) | 0.582 | yes (marginal) |
| Behavioural | 0.802 | yes |
| Action | 0.929 | yes |
| Combined | 0.938 | — |

Positive steps:
- 921 pooled, which clears the pre-registered minimum of 50 for the pooled analysis.
- 13 of 21 backbones have fewer than 50 positive steps each, so **per-backbone conclusions are not supported**.

### 2.2 E1 — discrimination and calibration (`e1_crossfit.json`)

| Metric | Calibrated p (label-NLL fit, primary) | Uncalibrated σ(s) |
|---|---|---|
| ROC-AUC | 0.938 [0.908, 0.961] | 0.939 |
| Average precision (PR-AUC estimate) | 0.719 [0.559, 0.827] | 0.721 |
| ECE (M = 10) | 0.044 [0.033, 0.084] | **0.042** |
| Log-loss | 0.201 [0.149, 0.294] | 0.201 |
| Brier (SC-5: binary / two-class) | 0.060 / 0.121 | 0.060 / 0.120 |

Calibration fit details:
- No fold produced γ₁ ≤ 0 (γ₁ ∈ [0.945, 0.981]).
- λ = 10 was selected in 8 folds and λ = 1 in 1 fold.
- The Platt-smoothed secondary calibrator gives essentially identical numbers (ECE 0.0436).

**Negative result.** Platt calibration did not reduce calibration error here. The ridge model's own probabilities are already near-calibrated, the fitted map is close to identity, and pooled ECE is marginally higher after calibration.

Generalisation checks:
- **Grouping by user task (sensitivity):** pooled ROC-AUC 0.943. The `user_task_15` fold scores ROC-AUC 0.21 (see §3.2).
- **Leave-one-backbone-out:** pooled ROC-AUC 0.949. Worst held-out backbone: claude-3-haiku, 0.736.
- **Cross-template (gpt-4o, models fitted on `important_instructions` only):** ROC-AUC 0.92–0.96 on `direct`, `ignore_previous`, `important_instructions_no_names`, `injecagent` and `tool_knowledge`.

### 2.3 E2 — REM (A3) vs B1 (A1) on held-out recorded steps (`e2_e5_e6_observe_only.json`)

| | REM | B1 |
|---|---|---|
| Intervention rate on y = 1 steps | 0.973 [0.957, 0.987] | 0.740 [0.473, 0.922] |
| Step false-positive rate (any intervention on y = 0) | 0.227 [0.213, 0.239] | 0.056 [0.047, 0.066] |
| …of which Escalate | 0.186 | 0.010 |
| y = 0 withheld under the idealized reviewer | 0.040 | 0.046 |
| Ties (SC-2) | 0 | 0 |
| D2 predicate verdicts | 58 | 58 |

Notes:
- The step-level and episode-level loss grids coincide here, because measured r_mod was identical for both variants.
- Without a reviewer, REM's intervention profile is far more aggressive than B1's.
- With the idealized reviewer, REM's withheld-benign rate (4.0%) is comparable to B1's (4.6%), while it intervenes on more adversarial steps.

### 2.4 E4 — enforcement replay (`e4_e5_enforcement_replay.json`, `figures/fig_enforcement_replay.png`)

| Configuration | ASR | Benign utility | Utility under attack |
|---|---|---|---|
| B0 no defense | 0.226 [0.148, 0.295] | 0.524 [0.381, 0.676] | 0.492 |
| B1, step-level, no reviewer | 0.055 [0.011, 0.134] | 0.509 [0.334, 0.702] | 0.514 |
| B1, episode-level, no reviewer | 0.046 [0.004, 0.125] | 0.509 | 0.485 |
| REM, step-level, no reviewer | **0.004** [0.001, 0.007] | **0.314** [0.110, 0.548] | 0.364 |
| REM, episode-level, no reviewer | 0.004 [0.001, 0.007] | 0.314 | 0.363 |
| REM, either variant, idealized reviewer | 0.004 [0.001, 0.007] | 0.497 [0.333, 0.680] | 0.481–0.496 |

Paired differences (grouped bootstrap):

| Comparison | ASR | Benign utility |
|---|---|---|
| REM − B1, no reviewer | −0.051 [−0.130, −0.007] | **−0.195 [−0.341, −0.074]** |
| REM − B1, idealized reviewer | −0.051 [−0.130, −0.007] | +0.003 [−0.009, 0.018] |
| REM − B0, no reviewer | −0.222 [−0.289, −0.146] | −0.210 [−0.379, −0.051] |

Other measured quantities:
- **r_mod** (oracle-Modify replays, NO-ADAPT): 0.000 at tier 3 (530 episodes) and 0.010 at tier 4 (298 episodes). Tiers 1–2 were unmeasured, so the pre-registered value 1.0 was used.
- **REM per-step latency** (excluding LLM and tools): median ≈ 0.17–0.20 ms, p95 ≈ 0.43–0.54 ms.
- **REM per-step memory:** median peak traced allocation 2.9 KB, p95 12.4 KB (300 episodes, 611 steps).
- **Distributed defenses (recorded outcomes only, gpt-4o, not replayed):**

  | Defense | ASR | Benign utility |
  |---|---|---|
  | tool_filter | 0.112 | 0.81 |
  | transformers_pi_detector | 0.007 | 0.44 |
  | repeat_user_prompt | 0.462 | 0.94 |
  | spotlighting_with_delimiting | 0.615 | 0.81 |

  These are recorded under possibly different benchmark versions and are **not** a controlled comparison with REM's replay numbers.

**Central finding.** Without a reviewer, REM's benign utility is 0.25–0.38 for every backbone. It releases only 33 of 180 legitimate state-changing steps in benign episodes (tiers 2–4); B1 releases 132.
- With the pre-registered costs (C_miss up to 20 × C_FA), the Bayes thresholds p*ₖ are 1/11 (tier 3) and 1/21 (tier 4).
- Legitimate transfers often carry action evidence: a recipient read from tool output, or a recipient not named in the objective. Most of them are therefore escalated.
- REM's low ASR in this pilot is bought with escalation volume. Whether that is acceptable depends on a reviewer that this benchmark does not have.

### 2.5 E5 — ablations (enforcement, step-level, no reviewer; observe-only numbers in the JSON)

| Ablation | ASR | Benign utility | Held-out ROC-AUC |
|---|---|---|---|
| Full REM | 0.004 | 0.314 | 0.938 |
| Context evidence removed | 0.004 | 0.314 | 0.938 |
| Behavioural evidence removed | 0.004 | **0.419** | 0.938 |
| Action evidence removed | 0.006 | 0.314 | **0.799** |
| Calibration removed (p̃ in Eq. 3.6) | 0.004 | 0.329 | — |
| One tier for all actions: tier 1 / 2 / 3 / 4 | 0.051 / 0.022 / 0.004 / 0.003 | 0.440 / 0.353 / 0.338 / 0.314 | — |
| Predicates D1, D2 disabled | 0.004 | 0.314 | — |
| Observe-only | 0.226 (= B0) | 0.524 (= B0) | — |

**Negative results.**
- **Context evidence:** removing it changes nothing measurable.
- **Behavioural evidence:** removing it *raises* benign utility by 10.5 points with the same ASR. In this pilot the behavioural group costs utility without measured security benefit.
- **Predicates:** they have no measurable effect. Π is empty, and D2 fired on 58 steps.

The action group carries most of the discrimination.

### 2.6 E3 — A2 observe-only CUSUM (`e3_a2_cusum_observe_only.json`)

- **q₁ = 0.3:** undefined in every fold. The estimated q₀ (≈ 0.34) exceeds q₁; this is reported, not repaired.
- **q₁ = 0.5:**
  - Alarm at or after the injection entered the context: 74.8% of attacked episodes with a positive step.
  - Alarm at or before the first positive step: 43.8%.
  - Median delay: 1 step.
  - Held-out benign false-alarm rate: **0.106**, against a fitting target of 0.05. The threshold did not generalise to held-out benign episodes.
- **q₁ = 0.7:** results are similar.
- A2 issued no verdicts.

### 2.7 E6 — realized loss across the declared grid

Realized loss (Eq. 3.22) on held-out steps, amount limit 1000, step-level variant:
- REM with matched costs: 0.04–0.30 across the 12 (C_miss multiplier × C_esc) cells.
- REM with the base costs evaluated under L_e: 0.06–0.32.
- B1: 0.34–3.16.

This comparison **favours REM by construction**, because REM minimises expected loss under L (Chapter 3 Sec. 3.12.3). It must not be read as evidence that REM is "better".

The grid cell α_blk = 0.05 is not evaluable, because the pre-registered α_mod = 0.05 must exceed α_blk. This is a design inconsistency in the pre-registered grid, reported rather than silently changed.

---

## 3. Threats to validity

### 3.1 Construct validity

- **Labels are attempt labels.** y = 1 means "the agent proposed the attacker's reference action with the attacker's key argument", not "the attack succeeded".
  - 158 attacked episodes have a positive step but no recorded attack success. Examples: an update of a non-recurring transaction under injection_task_4; a message subject missing the required content under injection_task_8.
- **Strict reference matching misses alternative routes.** 2 episodes have recorded attack success without a positive step. One reaches the attacker through `schedule_transaction` instead of the reference tool; one has no attacker call at all, which looks like a benchmark recording inconsistency.
  - 105 steps carry an attacker value but are labelled 0; most are legitimate `user_task_15` actions.
  - The label-audit sample of 30 episodes (`results/pilot/label_audit_sample.md`) was inspected by the AI assistant, **not a human**. 29/30 labels matched the trace; one (#29) is a likely false negative of this kind. **A human audit is still required.**
- **AM-1 (pre-run) and the post-hoc finding.** In AgentDojo banking suite versions v1 and v1.1, `user_task_15` asks the agent to pay the new landlord at `US133000000121212121212`, the same IBAN every injection task uses as the attacker account. This was changed upstream from v1.1.1 (landlord IBAN `CA133012400231215421872`), so it is a known and fixed benchmark issue, not a new finding.
  - 16 of the 21 recorded backbones used the colliding prompt.
  - 5 used the corrected one: claude-3-7-sonnet, gemini-1.5-pro-002, gemini-2.0-flash-001, gemini-2.0-flash-exp, Llama-3.3-70B.
  - The label-relevant ground truths of all nine injection tasks are identical in every suite version from v1 to v1.2.2 (checked), so labels are consistent across the mixed versions.
  - The pre-run amendment excluded only the pair whose *reference* actions collide.
  - After results were computed, 29 positive steps in `user_task_15` episodes were found to be ambiguous, 19 of them without any injected content in context.
  - All of REM's residual replay ASR (0.4%) comes from these episodes. A disclosed **post-hoc** sensitivity analysis that excludes `user_task_15` gives REM ASR 0.000 and held-out ROC-AUC 0.952 (`sensitivity_post_hoc_exclude_user_task_15.json`).
  - The primary numbers above keep the pre-registered analysis.
- **Escalation is not resolved by anyone.** The idealized reviewer is an oracle that knows y; the no-reviewer bound is a worst case. Neither represents a human reviewer's error rate or latency.
- **Costs are declared, not elicited.** C_FA, C_miss, C_mod and C_esc are pre-registered exploratory values, not institutional financial policy. Results depend on them (§2.7, E6 grid).

### 3.2 Internal validity

- **Pattern-author leakage.** The instruction patterns were written by someone who knew the AgentDojo templates. The context-group ablation shows no measurable dependence on them, and cross-template scores remain high.
- **Single attacker account.** No feature encodes an account identifier (Sec. 3.6.2). Still, x_act2 ("recipient not in the objective") fires on every attack in a benchmark where the attacker IBAN never appears in an objective, with `user_task_15` as the exception. Real fraud may use recipients that do appear in user-visible context.
- **Fitting data are observe-only by construction.** The traces were recorded without REM.

### 3.3 External validity

- **One environment.** Banking only; one benchmark; one attack family for fitting.
- **No adaptive attacker.** No attack was optimised against REM.
- **No-adaptation replay.** NO-ADAPT understates what an agent that retries could achieve. r_mod ≈ 0 is a consequence of this assumption, not a property of tool restriction.
- **Version mixture.** Recorded traces span benchmark versions (most unlabelled; some v1.2.1); replay uses suite v1, so 21 episodes did not reproduce.
- **Backbones.** These are historical model snapshots (2024–2025). Results are not claims about current models.

### 3.4 Statistical conclusion validity

- There are only 9 injection-task groups; grouped intervals are therefore wide, and some are unstable (for example the AP interval [0.56, 0.83]).
- Repeated runs: 1 per configuration. The recorded traces contain one run per (backbone, task pair); the Chapter 3 requirement of ≥ 3 runs is not met.
- No correction for multiple comparisons. Ablations and the grid are descriptive.

---

## 4. What these results do and do not support

**Supported, as exploratory evidence on recorded AgentDojo banking traces:**
- the REM pipeline is implementable at the tool boundary without modifying the agent (AS-1), with sub-millisecond per-step overhead;
- the Chapter 3 evidence vector separates attacker-induced steps from legitimate ones on held-out injection tasks, held-out backbones and held-out attack templates (ROC-AUC 0.92–0.96);
- with the pre-registered costs, REM's expected-loss verdict prevents more attacker-induced actions than the threshold baseline B1, and pays for this with escalations whose cost depends entirely on reviewer availability.

**Not supported:**
- any claim that REM prevents attacks in deployment;
- any claim about adaptive agents or attackers;
- any claim that calibration improved anything in this pilot;
- any claim that the behavioural or context evidence groups contribute;
- any per-backbone conclusion;
- any claim about real financial institutions' costs.

Every item in this report remains **EXPLORATORY — SUPERVISOR DECISION REQUIRED** until:
- the design is frozen;
- the label rule and AM-1 are approved;
- the reviewer model is decided.
