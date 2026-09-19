# STAGE 2 — EQUATION-TO-SOURCE TRACEABILITY

**Stage:** 2 (verification only — no code modified)
**Baseline commit:** `afc1137`
**Date:** 2026-09-19

---

## REGISTRY STATUS

```text
AUTHORITATIVE EQUATION REGISTRY: NOT FOUND
```

Searched: repository root, `docs/`, `configs/`, `rem/`, and the
`REM_EQUATION_REGISTRY` environment hook. No registry exists.

Per `CLAUDE.md` § EQUATION-ID LOCK and Stage 2 brief §10, **no registry was
created and no identifier was invented**. Every operation below is marked
`AWAITING REGISTRY ID`.

```text
TOTAL MATHEMATICAL OPERATIONS IN CODEBASE   19
CITED (source recorded)                     19
UNSOURCED                                    0
AUTHORITATIVE EQUATION IDs                   0
AWAITING REGISTRY ID                        19
```

> The traceability chain
> `Literature → Requirement → Algorithm → Equation → Code → Test`
> is **open at the Equation link** and cannot be closed until the authoritative
> registry is authored. This report does not claim otherwise.

---

## HOW TO READ THE "DIRECTLY SUPPORTED?" COLUMN

| Value | Meaning |
| ----- | ------- |
| **Yes** | The cited source states this exact formulation |
| **Method supported** | The source establishes the method; the specific form here is a standard convention or a REM adaptation. *Per brief §18, the thesis must say "Method supported; REM-specific formulation requires project-level justification."* |
| **Frozen by contract** | The formulation is fixed by `CLAUDE.md` rather than derived from a paper; the paper supports the underlying principle |

Locator confidence:

| Mark | Meaning |
| ---- | ------- |
| ✅ | Source located and content verified during Stage 2 |
| ⚠️ | Source confirmed at venue level; **page/section/equation locator NOT re-verified against the primary document** |

---

## A. FROZEN CORE EQUATIONS (4 operations, 6 code sites)

### A1 — Linear score

| Field | Value |
| ----- | ----- |
| **Operation** | `rem.algorithms.detection.ridge_logistic::RidgeLogisticRegression.decision_function` |
| **Current formulation** | `s_t = β₀ + βᵀx_t` |
| **Source** | `CLAUDE.md` § MATHEMATICAL LOCK → Probability estimation ✅ |
| **Directly supported?** | **Frozen by contract.** The linear-predictor form is standard for logistic regression |
| **Project-specific?** | Yes — frozen by the project contract |
| **Equation ID** | AWAITING REGISTRY ID |
| **Status** | **FROZEN** |
| **Test** | `test_frozen_math.py::test_decision_function_is_the_frozen_linear_form` |

### A2 — Uncalibrated probability

| Field | Value |
| ----- | ----- |
| **Operation** | `…::RidgeLogisticRegression.uncalibrated_probability`; link in `…::sigmoid` |
| **Current formulation** | `p̃_t = σ(s_t)`, `σ(z) = 1/(1+e^{−z})` |
| **Source** | `CLAUDE.md` ✅; logistic link, Hastie et al. (2009) ⚠️ *(§4.4 locator unverified)* |
| **Directly supported?** | **Yes** |
| **Project-specific?** | No — standard logistic link |
| **Note** | Implemented in a numerically stable branch form; mathematically identical |
| **Equation ID** | AWAITING REGISTRY ID |
| **Status** | **FROZEN** |
| **Tests** | `test_sigmoid_matches_definition`, `test_sigmoid_is_overflow_safe`, `test_uncalibrated_probability_is_sigmoid_of_the_logit` |

### A3 — Platt calibration on the logit

| Field | Value |
| ----- | ----- |
| **Operation** | `rem.algorithms.calibration.platt::PlattLogitCalibrator.calibrate` |
| **Current formulation** | `p_t = σ(γ₁s_t + γ₀)`, with `γ₁ > 0` enforced |
| **Source** | `CLAUDE.md` ✅; Platt (1999), *Advances in Large Margin Classifiers*, MIT Press, 61–74 ✅ |
| **Directly supported?** | **Yes**, with a documented re-parameterisation |
| **Project-specific?** | Sign convention only |
| **Note** | Platt's published form is `P(y=1\|f) = 1/(1+exp(Af+B))`. REM's frozen form is equivalent with **`γ₁ = −A`**; REM's `γ₁ > 0` is Platt's `A < 0`. Verified consistent |
| **Equation ID** | AWAITING REGISTRY ID |
| **Status** | **FROZEN** |
| **Tests** | `test_platt_produces_the_frozen_form`, `test_platt_slope_is_positive`, `test_platt_is_monotone_increasing`, `test_platt_rejects_an_inverted_detector` |

### A4 — Conditional risk

| Field | Value |
| ----- | ----- |
| **Operation** | `rem.algorithms.decision.expected_loss::ExpectedLossDecisionEngine.conditional_risk` |
| **Current formulation** | `R_t(v) = (1−p_t)·L(v,0,k_t) + p_t·L(v,1,k_t)` |
| **Source** | `CLAUDE.md` ✅; Elkan (2001), IJCAI, 973–978 ✅ |
| **Directly supported?** | **Method supported.** Elkan establishes expected-cost minimisation over **class predictions** (2 actions). REM's version is over **4 actions indexed by a consequence tier** |
| **Project-specific?** | **YES — this is a REM extension** |
| **Required thesis wording** | *"Method supported; REM-specific formulation requires project-level justification."* Do **not** write that this equation is Elkan's |
| **Equation ID** | AWAITING REGISTRY ID |
| **Status** | **FROZEN (rule)** / **SUPERVISOR DECISION REQUIRED (`L`, `k`)** |
| **Test** | `test_conditional_risk_matches_the_frozen_equation` |

### A5 — Verdict selection

| Field | Value |
| ----- | ----- |
| **Operation** | `…::ExpectedLossDecisionEngine.argmin_verdict` |
| **Current formulation** | `v*_t = argmin_v R_t(v)` over `{Allow, Modify, Escalate, Block}` |
| **Source** | `CLAUDE.md` ✅; Elkan (2001) ✅ (principle); Chow (1970), *IEEE Trans. Inf. Theory* 16(1), 41–46 ✅ (abstain) |
| **Directly supported?** | **Method supported.** Bayes decision rule is standard; the **four-action set is REM's** |
| **Project-specific?** | **YES — action set is REM's** |
| **Supporting finding** | Chow's reject threshold is **derived from costs**: `t = (C_r − C_c)/(C_e − C_c)`. This supports deriving Escalate from the argmin rather than from a hand-set threshold |
| **Contract note** | `CLAUDE.md`: *"Neither source may be presented as having invented REM's four-action architecture."* Verified respected in code docstrings |
| **Equation ID** | AWAITING REGISTRY ID |
| **Status** | **FROZEN** |
| **Tests** | `test_argmin_selects_allow_when_risk_is_low`, `test_argmin_selects_block_when_risk_is_high`, `test_exact_tie_raises_rather_than_choosing` |

### A6 — Linear Shapley attribution (audit-only)

| Field | Value |
| ----- | ----- |
| **Operations** | `rem.algorithms.attribution.linear_shapley::LinearShapleyAttributor.shapley_value` and `.base_value` |
| **Current formulation** | `φᵢ = βᵢ(xᵢ − E[xᵢ])`; `φ₀ = f(E[x]) = β₀ + Σβᵢ·E[xᵢ]` |
| **Source** | `CLAUDE.md` ✅; Lundberg & Lee (2017), NeurIPS 30, 4765–4774, "Linear SHAP" ✅; Shapley (1953) ✅ *(venue only)* |
| **Directly supported?** | **Yes — the closed form was verified verbatim** (exact for a linear model under feature independence) |
| **Project-specific?** | No |
| **Note** | Computed on the **logit scale**, where the model is linear; additivity does not survive the sigmoid. Local accuracy `f(x) = φ₀ + Σφᵢ` holds and is tested |
| **Equation ID** | AWAITING REGISTRY ID |
| **Status** | **FROZEN — AUDIT ONLY** |
| **Tests** | `test_shapley_value_matches_the_closed_form`, `test_base_value_is_the_model_at_the_background_mean`, `test_local_accuracy_holds`, `test_attribution_cannot_reach_the_decision_engine` |

---

## B. FITTING PROCEDURES (2 operations)

### B1 — Ridge logistic objective and Newton–Raphson fit

| Field | Value |
| ----- | ----- |
| **Operation** | `rem.algorithms.detection.ridge_logistic::RidgeLogisticRegression.fit` |
| **Current formulation** | Minimise `J(β₀,β) = −Σ[yᵢ log pᵢ + (1−yᵢ)log(1−pᵢ)] + (λ/2)‖β‖²`, intercept unpenalised; Newton step `β ← β − H⁻¹g`, `g = Xᵀ(p−y) + λβ`, `H = XᵀWX + λI`, `W = diag(pᵢ(1−pᵢ))` |
| **Source** | Hoerl & Kennard (1970), *Technometrics* 12(1), 55–67 ✅ (L2 penalty); Hastie et al. (2009) ⚠️ *(§4.4.1 IRLS and §3.4.1 ridge locators unverified)* |
| **Directly supported?** | **Method supported.** Penalised logistic regression and Newton/IRLS fitting are standard. The **½ scaling** and **unpenalised intercept** are conventions, not results quoted from a source |
| **Project-specific?** | Conventions only |
| **λ** | **NOT SPECIFIED.** Selection procedure (grouped K-fold CV) is source-verified; the value is EXPERIMENTAL and gated on the grouping scheme |
| **Equation ID** | AWAITING REGISTRY ID |
| **Status** | **SOURCE-VERIFIED (method)** / **EXPERIMENTAL (λ)** |
| **Tests** | `test_ridge_penalty_shrinks_coefficients`, `test_intercept_is_unpenalised`, `test_fit_without_penalty_is_design_blocked` |

### B2 — Platt sigmoid fit with smoothed targets

| Field | Value |
| ----- | ----- |
| **Operation** | `rem.algorithms.calibration.platt::PlattLogitCalibrator.fit` |
| **Current formulation** | Minimise `−Σ[tᵢ log pᵢ + (1−tᵢ)log(1−pᵢ)]` with `pᵢ = σ(γ₁sᵢ + γ₀)` and targets `t⁺ = (N⁺+1)/(N⁺+2)`, `t⁻ = 1/(N⁻+2)` |
| **Source** | Platt (1999) ✅ |
| **Directly supported?** | **Yes — targets verified verbatim against the source** |
| **Project-specific?** | No |
| **Documented difference (D3)** | Platt fits on **cross-validated out-of-sample scores (3-fold)**; the implementation fits on a **single held-out validation split**. Both are out-of-sample; CV yields a lower-variance `γ`. **Recorded, not changed** |
| **Equation ID** | AWAITING REGISTRY ID |
| **Status** | **SOURCE-VERIFIED**; fitting protocol **PD** |
| **Tests** | `test_platt_smoothed_targets_keep_separable_data_finite`, `test_platt_requires_both_classes` |

---

## C. EVALUATION METRICS (7 operations)

All measurement apparatus, not REM algorithms. None is project-specific.

| # | Operation | Formulation | Source | Directly supported? | Status |
| - | --------- | ----------- | ------ | ------------------- | ------ |
| C1 | `metrics::precision` | `TP/(TP+FP)` | van Rijsbergen (1979), ch. 7 ⚠️ | Yes | SOURCE-VERIFIED |
| C2 | `metrics::recall` | `TP/(TP+FN)` | Fawcett (2006), §2 p. 862 ⚠️ | Yes | SOURCE-VERIFIED |
| C3 | `metrics::false_positive_rate` | `FP/(FP+TN)` | Fawcett (2006) ⚠️ | Yes | SOURCE-VERIFIED |
| C4 | `metrics::false_negative_rate` | `FN/(TP+FN)` | Fawcett (2006) ⚠️ | Yes | SOURCE-VERIFIED |
| C5 | `metrics::f1_score` | `2PR/(P+R)` | van Rijsbergen (1979) ⚠️ | Yes (E-measure at β=1) | SOURCE-VERIFIED |
| C6 | `metrics::accuracy` | `(TP+TN)/(P+N)` | Fawcett (2006) ⚠️ | Yes | SOURCE-VERIFIED |
| C7 | `metrics::brier_score` | `(1/n)Σ(pᵢ−oᵢ)²` | Brier (1950), *Monthly Weather Review* 78(1), 1–3 ⚠️ | Yes | SOURCE-VERIFIED |

**Convention recorded:** undefined quantities (zero denominator) return `NaN`
rather than a substituted `0`. Substituting a value would be an unsourced
convention. This is an implementation decision `[I]`, documented in code.

**Calibration-metric finding (Stage 2):** Brier score and log loss are **proper
scoring rules**; **ECE is not** — it admits trivial optima, e.g. predicting the
base rate. Brier (implemented) is therefore defensible as primary. **Log loss is
newly GREEN** for Stage 3. ECE may be reported only as a supplementary
diagnostic, stating bin count and binning scheme.

---

## D. DESCRIPTIVE STATISTICS (2 operations)

| # | Operation | Formulation | Source | Directly supported? | Status |
| - | --------- | ----------- | ------ | ------------------- | ------ |
| D1 | `runtime::mean` | `(1/n)Σxᵢ` | Hyndman & Fan (1996) ⚠️ | Yes | SOURCE-VERIFIED |
| D2 | `runtime::quantile` | `h=(n−1)p+1`; linear interpolation between order statistics | Hyndman & Fan (1996), **Definition 7** ⚠️ | Yes | SOURCE-VERIFIED |

**Why pinned:** sample-quantile definitions differ between packages (Hyndman &
Fan catalogue nine). Definition 7 is the R/NumPy default; pinning it makes
reported p95/p99 latencies reproducible across environments.

---

## E. OPERATIONS REQUIRING AUTHORITATIVE IDs

All **19**, listed for the registry author:

| # | Module | Operation |
| - | ------ | --------- |
| 1 | `rem.algorithms.detection.ridge_logistic` | `sigmoid` |
| 2 | `rem.algorithms.detection.ridge_logistic` | `RidgeLogisticRegression.decision_function` |
| 3 | `rem.algorithms.detection.ridge_logistic` | `RidgeLogisticRegression.uncalibrated_probability` |
| 4 | `rem.algorithms.detection.ridge_logistic` | `RidgeLogisticRegression.fit` |
| 5 | `rem.algorithms.calibration.platt` | `PlattLogitCalibrator.calibrate` |
| 6 | `rem.algorithms.calibration.platt` | `PlattLogitCalibrator.fit` |
| 7 | `rem.algorithms.decision.expected_loss` | `ExpectedLossDecisionEngine.conditional_risk` |
| 8 | `rem.algorithms.decision.expected_loss` | `ExpectedLossDecisionEngine.argmin_verdict` |
| 9 | `rem.algorithms.attribution.linear_shapley` | `LinearShapleyAttributor.shapley_value` |
| 10 | `rem.algorithms.attribution.linear_shapley` | `LinearShapleyAttributor.base_value` |
| 11 | `rem.evaluation.metrics` | `precision` |
| 12 | `rem.evaluation.metrics` | `recall` |
| 13 | `rem.evaluation.metrics` | `false_positive_rate` |
| 14 | `rem.evaluation.metrics` | `false_negative_rate` |
| 15 | `rem.evaluation.metrics` | `f1_score` |
| 16 | `rem.evaluation.metrics` | `accuracy` |
| 17 | `rem.evaluation.metrics` | `brier_score` |
| 18 | `rem.evaluation.runtime` | `mean` |
| 19 | `rem.evaluation.runtime` | `quantile` |

Once the registry exists, each is bound by passing `equation_id=` to
`@derivation(...)`. The decorator validates the ID against the registry and
**raises if the registry is absent**, so an ID can never be accepted on trust.

---

## F. SOURCE LIST

| Source | Identifier | Supports | Verified |
| ------ | ---------- | -------- | -------- |
| Elkan, C. (2001). The Foundations of Cost-Sensitive Learning | IJCAI 2001, 973–978 | Expected-cost decision principle; cost-matrix reasonableness conditions | ✅ content |
| Chow, C. K. (1970). On Optimum Recognition Error and Reject Tradeoff | IEEE TIT 16(1), 41–46; DOI 10.1109/TIT.1970.1054406 | Reject/abstain action; cost-derived reject threshold | ✅ content |
| Platt, J. C. (1999). Probabilistic Outputs for SVMs | *Advances in Large Margin Classifiers*, MIT Press, 61–74 | Sigmoid calibration; smoothed targets; out-of-sample fitting | ✅ content |
| Lundberg, S. M. & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions | NeurIPS 30, 4765–4774; arXiv:1705.07874 | Linear SHAP closed form | ✅ content |
| Shapley, L. S. (1953). A Value for n-Person Games | *Contributions to the Theory of Games II*, 307–317 | Shapley value | ✅ venue |
| Hoerl, A. E. & Kennard, R. W. (1970). Ridge Regression | *Technometrics* 12(1), 55–67; DOI 10.1080/00401706.1970.10488634 | L2 penalty | ✅ content |
| Hastie, Tibshirani & Friedman (2009). *ESL* 2nd ed. | Springer | Penalised logistic regression; IRLS; K-fold CV for λ | ⚠️ locators |
| Brier, G. W. (1950) | *Monthly Weather Review* 78(1), 1–3 | Brier score | ⚠️ locator |
| Fawcett, T. (2006) | *Pattern Recognition Letters* 27(8), 861–874 | tp/fp rates, accuracy | ⚠️ locator |
| van Rijsbergen, C. J. (1979) | *Information Retrieval* 2nd ed. | Precision; F-measure | ⚠️ locator |
| Hyndman, R. J. & Fan, Y. (1996) | *The American Statistician* 50(4), 361–365 | Sample quantile Definition 7 | ⚠️ locator |
| Debenedetti, E. et al. (2024). AgentDojo | NeurIPS 2024 D&B; arXiv:2406.13352 | Benchmark: 97 tasks, 629 security cases, 4 suites | ✅ content |

### Outstanding verification action

The ⚠️ rows are correct at venue level; their **in-code page/section locators
were not re-checked against primary documents** during Stage 2. Closing this is
a narrowly-scoped Stage 3 task (GREEN) and does not affect any equation's
correctness — only the precision of its citation.

---

## G. STAGE 2 COMPLIANCE

- [x] No equation ID invented — grep for `EQ-[A-Z]+-[0-9]+` across `rem/`, `scripts/`, `configs/`: **no matches**
- [x] No registry created
- [x] No equation changed
- [x] No code modified
- [x] Literature support distinguished from project-specific formulation (A4, A5, B1)
- [x] Locator confidence stated honestly rather than asserted
