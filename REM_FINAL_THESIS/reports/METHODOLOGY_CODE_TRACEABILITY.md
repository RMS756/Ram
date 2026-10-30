# Methodology-to-Code Traceability (R3, 30 October 2026)

**Basis:**
- Chapter 3 (final) and the code at merge commit `4a286a5`;
- the test run of 30 October (193 passed; `verification/pytest_2026-10-30.txt`);
- an automated check that every function, class or module named in Chapter 4 exists in `rem/`, `experiments/` or `tests/`: 106 identifiers checked, all found.

Runtime verification (tests and pilot execution) is distinguished from static inspection throughout.

## 1. Chapter 3 component → code → test → result

| Chapter 3 component | Code | Verified by | Kind | Result artifact | Status |
|---|---|---|---|---|---|
| Five layers; no sixth layer | `rem/core/pipeline.py` `Layer.FROZEN_LAYERS` | `test_contract_compliance::test_exactly_five_frozen_layers` | Runtime (test) | — | Consistent |
| Provenance labels, least-trusted inheritance (§3.4.2) | `rem/algorithms/context/provenance.py` | `test_evidence.py` | Runtime | Used in every pilot step | Consistent |
| Hygiene on REM's analysis copy (§3.4.1) | `provenance.strip_invisible` | `test_evidence.py` | Runtime | — | Consistent |
| Entity extraction (§3.4.3) | `rem/algorithms/behavior/evidence.py`, `value_occurs_in` | `test_evidence.py` | Runtime | — | **Partial**: credentials and phone numbers not extracted as entities (Ch. 4 §4.4) |
| x^ctx^~1~ injection classifier (Table 3.8) | — | — | — | — | **Not implemented** (classifier pending, D-8) |
| x^ctx^~2~ instruction patterns | `rem/algorithms/detection/instruction_patterns.py` | `test_evidence.py` | Runtime | `feature_firing_rates.json` | Consistent; patterns authored with knowledge of the benchmark (disclosed) |
| x^beh^~1–4~, x^act^~1–3~ (Table 3.9) | `evidence.py` `EpisodeTracker` | `test_evidence.py`, `test_traces.py` (fold-specific x^beh^~4~) | Runtime | `e1_crossfit.json` | Consistent, with interpretations I-1 to I-9 (Ch. 4 Table 4.4) |
| Eq. 3.1–3.2 ridge LR | `detection/ridge_logistic.py` | `test_frozen_math` (13 tests) | Runtime | `e1_crossfit.json` | Consistent; λ = λ_impl/2 |
| Eq. 3.3 calibration on the logit, γ₁ > 0 | `calibration/platt.py`, `calibration/logit_nll.py` | `test_frozen_math`, `test_crossfit` | Runtime | `e1_crossfit.json` (`gamma_1` 0.945–0.981) | Consistent |
| Eq. 3.4 fit on labels | `logit_nll.LabelNLLLogitCalibrator` | `test_crossfit` | Runtime | `label_nll_primary` | Consistent. **SC-4**: the frozen calibrator uses Platt targets; both are reported |
| Tiers κ (Tables 3.10–3.11) | `decision/consequence.py` `ConsequenceTierMap` | `test_evidence.py` | Runtime | `r2_breakdowns.json` | Consistent with the pre-registered exploratory tier map (not approved, D-9) |
| Predicates D1, D2 (§3.7.4) | `decision/policy.py` `PredicatePolicy` | `test_a3.py` | Runtime | `sources: D2 = 58` | Consistent; Π = ∅ declared |
| Table 3.13, Eq. 3.5, dominance check | `decision/loss_matrix.py` | `test_a3.py` | Runtime | `dominance` per fold | Consistent |
| Eqs. 3.6–3.7, feasible set 𝒱(a_t) | `expected_loss.conditional_risk`; `a3.A3Policy.decide` | `test_frozen_math`, `test_a3.py` | Runtime | `e2_e5_e6_observe_only.json` | Consistent. **SC-2**: the frozen engine raises on ties; A3 offers `tie_mode`; 0 ties occurred |
| Eqs. 3.8–3.10 | `loss_matrix.indifference_threshold`, `allow_block_threshold`, `escalation_feasible` | `test_a3.py`; `verify_equations.py` | Runtime and symbolic | — | Consistent |
| Eqs. 3.11–3.13 attribution, audit-only | `attribution/linear_shapley.py`; `evidence.FEATURE_GROUPS` | `test_frozen_math`, `test_contract_compliance::test_decision_engine_signature_excludes_attribution` | Runtime | `additivity_error` in the replay audit | Consistent |
| Eq. 3.14, baseline B1 | `a1.operating_threshold`, `A1Policy` | `test_a1.py` | Runtime; `verify_equations.py` | `theta_blk`, `theta_mod` | Consistent; α grid cell 0.05 not evaluable (D-14) |
| Mitigation, Table 3.14, step and episode level | `integration/agentdojo_replay.py` `RemGuard._mitigate` | `test_replay.py` | Runtime | `e4_e5_enforcement_replay.json` | Consistent. **SC-1 / D-2**: step level is the reference; confirmation pending |
| Escalate with a human reviewer | — | — | — | — | **Not implemented**: replaced by two bounds (idealized reviewer, no reviewer) |
| Procedure 3.1 nested grouped cross-fitting | `rem/evaluation/crossfit.py` | `test_crossfit.py` (held-out predictions independent of held-out labels) | Runtime | `e1_crossfit.json` | Consistent |
| Pilot E0 | `experiments/pilot/e0_pilot.py` | Pilot run | Runtime | `e0_pilot.json` | Consistent; fold-specific retention checked |
| Eqs. 3.15–3.19 CUSUM, observe-only | `behavior/cusum.py`, `a2.py` | `test_a2.py` (no verdict path) | Runtime | `e3_a2_cusum_observe_only.json` | Consistent |
| Eqs. 3.20–3.21 ECE, log-loss | `evaluation/probabilistic.py` | `test_probabilistic.py`; `verify_equations.py` | Runtime and direct comparison | `e1_crossfit.json` | Consistent |
| Eq. 3.22 realized loss | `experiments/pilot/run_main.py` `stage_observe` | Pilot run | Runtime | `e6_grid` | Consistent |
| Grouped bootstrap (§3.11.9) | `evaluation/bootstrap.py` | `test_probabilistic.py` | Runtime | Every interval | Consistent |
| Observe-only and enforcing modes (§3.11.1) with live agents | `integration/agentdojo_replay.py` (replay only) | `test_replay.py` | Runtime (replay) | — | **Live mode not executed**. Replay is a proposed scope amendment (SC-7 / D-1) |
| Audit record (§3.7.6) | `RemGuard.evaluate`; `core/audit.py` | `test_replay.py`, `test_pipeline.py` | Runtime | — | Consistent; raw argument values not logged |
| Latency (Table 3.15) | `time.perf_counter` around `RemGuard.evaluate` | Pilot run | Runtime | `e4_e5_enforcement_replay.json` | Excludes LLM and tool time, as Chapter 3 specifies |

## 2. Two execution paths

The frozen pipeline (`rem/core/pipeline.py`) is exercised only by unit and contract tests. Every Chapter 5 result comes from the evaluation path (`rem/integration/agentdojo_replay.py` with `rem/algorithms/a3.py`). The evaluation path reuses the frozen estimator, calibration, conditional-risk function and attribution. Chapter 4 §4.3 states this explicitly. An examiner should treat the frozen pipeline as an architecture skeleton, not as the evaluated system.

## 3. Mismatches between methodology and code (none silently resolved)

| ID | Mismatch | Where documented | Decision |
|---|---|---|---|
| SC-1 | Mitigation scope: step-level reference vs episode-level variant (cannot differ under replay) | Ch. 3 §3.8; Ch. 4 §4.8 | D-2 |
| SC-2 | Tie rule: frozen code raises vs Chapter 3 order (0 ties observed) | Ch. 4 §4.7 | D-4 |
| SC-3 | "Calibration removed" ablation refused by the frozen pipeline; run in the evaluation path as p̃ in Eq. 3.6 | Ch. 5 Table 5.11 | Open |
| SC-4 | Calibration target: labels (Eq. 3.4) vs Platt smoothed targets | Ch. 5 Table 5.3 (both reported) | D-3 |
| SC-5 | Brier score: Chapter 3 defers it; reported in the binary convention | Ch. 5 Table 5.3 | Open |
| SC-6 | Layer label of the estimator in code comments (L2) vs Chapter 3 (L4) | Ch. 4 §4.3 | Open; no computational effect |
| SC-7 | Replay used although Chapter 3 originally excluded replay-based estimation | Ch. 3 §3.11.11; Ch. 5 §5.6 | D-1 |
| M1 | Penalty scale λ vs λ_impl/2 | Ch. 3 §3.7.1; Ch. 4 §4.7 | Resolved by stated conversion; values reported on both scales |

No code was changed in R3.
