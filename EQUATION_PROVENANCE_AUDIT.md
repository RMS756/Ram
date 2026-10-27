# Equation Provenance Audit

Date: 27 Oct 2026. Scope: the 22 equations of Chapter 3 (`REM_STAGE2_INPUT_PACKAGE/working/Chapter3_working.md`,
Table 3.17), traced to their sources, to the code that implements them, and to the tests that execute that code.

**Equation identifiers.** The Chapter 3 equation numbers (3.1–3.22) are used as *document references only*. No
`EQUATION_ID` has been created: the authoritative equation registry is unavailable, and the implementation still
reports every operation as awaiting a registry ID (`tests/test_contract_compliance.py::test_no_equation_ids_appear_in_implementation_code`
passes).

**What "verified" means here.**
- *Source metadata* was checked in this session against Crossref or OpenAlex (`REFERENCE_VERIFICATION_MATRIX.xlsx`).
- *Formulation against the full text* was **not** re-checked in this session; the Chapter 3 codes are carried forward
  unchanged:
  - FV: formulation checked;
  - IV: identity only;
  - NC: not accessed;
  - DER: derived in Chapter 3;
  - DEF: design definition.
- *Implementation* means the code exists **and** a test executes it; the test results come from the run of
  27 Oct 2026 (192 passed with AgentDojo installed, 189 passed and 3 skipped without it).

---

## 1. Equation-by-equation trace

| Eq. | Content | Status (Ch. 3) | Source (metadata status) | Implementation | Executed by | Findings |
|---|---|---|---|---|---|---|
| 3.1 | s = β₀ + βᵀx, p̃ = σ(s) | Established, IV | Cox (1958) — VERIFIED | `rem/algorithms/detection/ridge_logistic.py` `decision_function`, `sigmoid` | `test_frozen_math.py::test_decision_function_is_the_frozen_linear_form`, `::test_uncalibrated_probability_is_sigmoid_of_the_logit` | — |
| 3.2 | Ridge-penalised log-likelihood | Established, IV | le Cessie & van Houwelingen (1992) — VERIFIED | `ridge_logistic.py` `fit` (Newton/IRLS) | `::test_ridge_penalty_shrinks_coefficients`, `::test_intercept_is_unpenalised` | **M1:** code minimises NLL + (λ/2)‖β‖²; Ch. 3 writes λ‖β‖². Equivalent up to rescaling λ; the pilot reports λ on the code's scale. Needs one-line alignment in Ch. 3 or code (SUPERVISOR DECISION). |
| 3.3 | p = σ(γ₁s + γ₀), γ₁ > 0 | Adapted; Platt NC | Platt — **DISCREPANCY** (cited 1999 title vs Crossref 2000 chapter "Probabilities for SV Machines"); Guo (2017) — EXISTS; Kull (2017) — ambiguous (two 2017 works) | `rem/algorithms/calibration/platt.py` `calibrate`; γ₁ ≤ 0 → `MonotonicityViolationError` | `::test_platt_produces_the_frozen_form`, `::test_platt_slope_is_positive`, `::test_platt_rejects_an_inverted_detector` | Map is correct. Pilot: γ₁ ∈ [0.945, 0.981] in all 9 folds. |
| 3.4 | Calibration fit by NLL on labels | Established, FV | Guo et al. (2017) | `rem/algorithms/calibration/logit_nll.py` `LabelNLLLogitCalibrator.fit` | `tests/test_crossfit.py` (both calibrators) | **SC-4:** frozen `PlattLogitCalibrator` fits Platt's *smoothed targets*, not labels. Both implemented, neither adopted; pilot difference is negligible (ECE 0.0438 vs 0.0436). |
| 3.5 | L(Modify,1,k) = r_mod(k)·C_miss(k) | Derived (A-Mod) | Law of total expectation | `rem/algorithms/decision/loss_matrix.py` `build_loss_grid` | `tests/test_a3.py::test_table_3_13_rows` | r_mod measured under NO-ADAPT replay (≈0–0.01); the assumption drives the value. |
| 3.6 | R(v) = (1−p)L(v,0,k) + pL(v,1,k) | Adapted, FV | Elkan (2001) — EXISTS; abstract states the lowest-expected-cost rule | `rem/algorithms/decision/expected_loss.py` `conditional_risk` | `test_frozen_math.py::test_conditional_risk_matches_the_frozen_equation`; `test_a3.py::test_argmin_is_eq_3_7_over_feasible_set` | — |
| 3.7 | v* = argmin over 𝒱(aₜ); ties → Block ⪰ Escalate ⪰ Modify ⪰ Allow | Adapted; tie order DEF | Elkan (2001) | `rem/algorithms/a3.py` `A3Policy.decide` (feasible set); frozen `argmin_verdict` raises on ties | `test_a3.py::test_ties_raise_or_are_recorded_never_silently_resolved`, `::test_modify_only_feasible_for_restricted_tools` | **SC-2:** frozen code raises `VerdictTieError`; Ch. 3 breaks ties by order. `tie_mode` makes the choice explicit. Pilot: 0 ties in 6,762 held-out steps. **M4:** frozen `argmin_verdict` ranges over all four verdicts; Ch. 3 restricts to 𝒱(aₜ). A3 implements 𝒱(aₜ) without editing frozen code. |
| 3.8 | π_{v,v′}(k) = Δ₀/(Δ₀+Δ₁) | Derived | From Eq. 3.6 | `loss_matrix.py` `indifference_threshold` | `test_a3.py::test_thresholds_eq_3_8_and_3_9` | — |
| 3.9 | p*ₖ = C_FA/(C_FA + C_miss) | Derived | Eq. 3.8; consistent with Elkan | `loss_matrix.py` `allow_block_threshold` | same | Pilot costs give p*₃ = 1/11 and p*₄ = 1/21, which explains REM's escalation volume (validity report §2.4). |
| 3.10 | C_esc < C_FA·C_miss/(C_FA + C_miss) | Derived; Chow conceptual | Chow (1970) — VERIFIED (conceptual support only) | `loss_matrix.py` `escalation_feasible`, `reachable_verdicts` | `test_a3.py::test_escalation_feasibility_eq_3_10`, `::test_dominance_check` | Pilot dominance check: Modify unreachable at tiers 1–2 (not in 𝒯_R); **Block unreachable at tier 3** under the pilot costs. Reported in `e2_e5_e6_observe_only.json`. |
| 3.11 | φᵢ = βᵢ(xᵢ − x̄ᵢ) | Adapted, FV | Lundberg & Lee (2017) — EXISTS | `rem/algorithms/attribution/linear_shapley.py` | `test_frozen_math.py` attribution tests; replay audit records | Audit-only; never reaches the verdict (`test_contract_compliance.py::test_decision_engine_signature_excludes_attribution`). |
| 3.12 | φ₀ + Σφᵢ = s | Derived | Local accuracy (Lundberg & Lee) | `linear_shapley.py` `base_value`; additivity error logged per step | replay audit field `additivity_error` | — |
| 3.13 | Group sums over I_ctx, I_beh, I_act | Definition | — | `rem/algorithms/behavior/evidence.py` `FEATURE_GROUPS` | `experiments/pilot/e0_pilot.py` | — |
| 3.14 | θ(α) = min{θ : FPR_val(θ) ≤ α} | Definition | — | `rem/algorithms/a1.py` `operating_threshold` | `test_a1.py` (4 tests incl. monotone invariance) | Candidate set extended by nextafter(max) so that α = 0 is attainable (documented). Pre-registered grid α_blk = 0.05 = α_mod violates α_mod > α_blk and is reported as not evaluable. |
| 3.15 | Bernoulli LLR increment | Derived | Basseville & Nikiforov (1993) — EXISTS; Reynolds & Stoumbos (1999) — VERIFIED | `rem/algorithms/behavior/cusum.py` `BernoulliCusum.increment` | `test_a2.py::test_increments_and_recursion` | Observe-only. |
| 3.16 | G_t = max(0, G_{t−1} + l_t) | Established | Page (1954) — VERIFIED; Basseville & Nikiforov | `cusum.py` `path` | same | — |
| 3.17 | T_A = min{t : G_t ≥ h_G} | Established | Basseville & Nikiforov | `cusum.py` `alarm_time` | same | — |
| 3.18 | Per-episode false-alarm rate | Definition | — | `rem/algorithms/a2.py` `episode_false_alarm_rate` | `test_a2.py::test_fit_meets_false_alarm_target_and_delay` | Fitting target 0.05 met in-fold; held-out rate 0.106 (did not generalise). |
| 3.19 | τ_d = T_A − ν | Definition | — | `a2.py` `evaluate_episode` | same | ν is detected by locating the episode's injected payload in tool output (`rem/integration/steps.py` `injection_entered`). |
| 3.20 | ECE, equal-width bins, (m−1)/M < p ≤ m/M | Adapted, FV | Naeini et al. (2015) — VERIFIED; Guo et al. (2017) | `rem/evaluation/probabilistic.py` `expected_calibration_error` | `tests/test_probabilistic.py::test_ece_binning_eq_3_20` | p = 0 assigned to bin 1 as specified. |
| 3.21 | Log-loss with declared clip | Derived | Eq. 3.2 | `probabilistic.py` `log_loss` | `test_probabilistic.py::test_log_loss_and_brier` | — |
| 3.22 | L̄(L_e) = mean L_e(v, y, k) | Definition | — | `experiments/pilot/run_main.py` `stage_observe` | pilot run | Matched-cost evaluation favours REM by construction (stated in the validity report). |

## 2. Equations or claims that must NOT be introduced

The forbidden reintroductions in `CLAUDE.md` were checked against the code:
- `rg "class (Isotonic|Temperature|Beta)Calibrat"` returns nothing;
- no `risk = p × S`;
- no Σ|βᵢ| confidence;
- no ρ persistence variable;
- no risk-based CUSUM;
- no SPRT.

A2 (CUSUM) has no verdict path; `tests/test_a2.py::test_a2_is_observe_only_and_issues_no_verdict` enforces this.

## 3. Open items (carried to `SUPERVISOR_DECISIONS_REQUIRED.md`)

1. M1 — penalty constant (λ vs λ/2).
2. SC-4 — calibration fitting targets (labels vs Platt smoothed targets).
3. SC-2 — ties (raise vs Chapter 3 order).
4. Platt citation — 1999 report vs 2000 chapter (title differs); the full text is still needed for the "NC" status.
5. Kull et al. (2017) — which of the two 2017 works is cited.
6. SC-5 — Brier convention: the record is confirmed (Crossref), but the r-class sum still needs the full text.
7. α grid inconsistency (α_blk = 0.05 with α_mod = 0.05).
