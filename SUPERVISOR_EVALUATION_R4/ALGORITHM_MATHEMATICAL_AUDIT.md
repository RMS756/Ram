# Algorithm and Mathematical Audit

**Scope:**
- Ch. 2 Eqs. 2.1–2.3;
- Ch. 3 Eqs. 3.1–3.22;
- Procedure 3.1 and Algorithm 1;
- the code implementing them.

**Thesis version:** R4 at `9ab3f9e`.

**Checks performed on 1 Nov 2026:**
- every derivation re-done by hand;
- `REM_FINAL_THESIS/verification/verify_equations.py`: 21 PASS lines, then ALL PASS;
- core modules read: `ridge_logistic.py`, `logit_nll.py`, `expected_loss.py`, `a3.py`, `crossfit.py`;
- the headline metrics recomputed with independent NumPy code.

## 1. Equation-by-equation verdicts

| Eq. | Content | Mathematically correct? | Variables defined? | Source / derivation | Code | Hidden assumptions / risks |
|---|---|---|---|---|---|---|
| 2.1 / 3.1 | s = β₀ + βᵀx; p̃ = σ(s) | Yes | Yes (Table 3.4) | Cox (1958); metadata only (IV) | `RidgeLogisticRegression` | Log-odds linear in binary features; no interactions |
| 3.2 | Ridge log-likelihood, λ‖β‖², intercept unpenalized | Yes | Yes | le Cessie & van Houwelingen (1992); penalty constant not read (IV) | Newton, gradient Xᵀ(p−y)+λ_impl β ✓ | λ = λ_impl/2 stated explicitly. λ_impl = 10 was selected in 8 of 9 folds (grid maximum 100), so it is not at the boundary. No line search, and convergence is not checked (minor) |
| 2.2 / 3.3 | p = σ(γ₁s + γ₀), γ₁ > 0 | Yes | Yes | Platt (2000, never read: NC); Guo (FV); the equal-shape beta equivalence (Kull) is correct | `PlattLogitCalibrator.calibrate`, rejects γ₁ ≤ 0 ✓ | Monotone, so AUC is invariant (confirmed: calibrated 0.938288, raw 0.939334; the difference comes from per-fold maps, as Ch. 3 §3.12.2 states) |
| 3.4 | NLL fit of (γ₁, γ₀) on out-of-fold logits | Yes | Yes | Guo et al. (2017) | `LabelNLLLogitCalibrator` (Newton with backtracking ✓) | The map is fitted on inner out-of-fold logits but applied to a model refitted on all of D_train. This is standard cross-fit practice with a small distribution mismatch. The code default used Platt targets (SC-4); both fits are reported, and the difference is negligible (ECE 0.0438 vs 0.0436) |
| 3.5 | L(Mod,1,k) = r_mod·C_miss | Yes, given A-Mod | Yes | Derived (total expectation) | `build_loss_grid` | **Circular in this thesis:** r_mod is estimated by oracle replay under NO-ADAPT, so it is ≈ 0 by construction, yet it determines the Modify verdicts (Issue M-2) |
| 2.3 / 3.6 | R(v) = (1−p)L(v,0,k) + pL(v,1,k) | Yes | Yes | Elkan (2001) criterion (FV, Eq. 1 form) | `conditional_risk` ✓ | Plug-in rule: the calibrated p replaces the true posterior. Valid only insofar as p is calibrated *in the region of the threshold*. Fold 7 (ECE 0.189) shows it is not, for unseen attack categories |
| 3.7 | argmin over 𝒱(a), with a tie order | Yes | Yes | Design definition | `A3Policy.decide` ✓ | Ch. 3 tie order vs the frozen code's `VerdictTieError` (SC-2) is unresolved; 0 ties observed |
| 3.8 | π = Δ₀/(Δ₀+Δ₁) | Yes. R(v)−R(v′) = −Δ₀ + p(Δ₀+Δ₁) | Yes | Derived | `indifference_threshold` | Requires Δ₀+Δ₁ > 0 (stated) |
| 3.9 | p* = C_FA/(C_FA+C_miss) | Yes: 1/2, 1/6, 1/11, 1/21 for the pilot costs | Yes | Derived; Elkan's printed form not read | `allow_block_threshold` | The thresholds are as arbitrary as the declared costs. The thesis says so ("why this cost ratio?") but has no elicitation |
| 3.10 | Escalate feasible iff C_esc < C_FA·C_miss/(C_FA+C_miss) | Yes (the maximum of min(R_A, R_B) is at p*); symmetric case C/2 ✓ | Yes | Derived; Chow conceptual (IV) | `escalation_feasible` | Necessary, not sufficient, when Modify is feasible (stated) |
| §3.7.5 | R(Mod) − R(Block) = (1−p)(C_mod−C_FA) + p·r·C_miss | Yes | Yes | Derived | `reachable_verdicts` | — |
| 3.11–3.13 | φ_i = β_i(x_i − x̄_i); φ₀ = β₀ + βᵀx̄; Σ = s | Yes (exact for linear models) | Yes | Lundberg & Lee (2017), linear case | `LinearShapleyAttributor` | "Linear SHAP" is the interventional/independent case, so its interpretation is distorted by correlated binary features (acknowledged). **Audit-only:** it cannot reach the verdict (contract test) |
| 3.14 | θ(α) = min{θ : FPR_val ≤ α} | Yes | Yes | Design definition | `operating_threshold` | Invariant to recalibration (stated correctly). Selected on y = 0 steps of the fitting portion (AM-2) |
| 3.15 | Bernoulli LLR | Yes | Yes | Derived | `BernoulliCusum` | Requires q₀ < q₁. Undefined at q₁ = 0.3 (q̂₀ ≈ 0.34), as reported |
| 3.16–3.19 | CUSUM recursion, alarm time, false-alarm rate, delay | Yes | Yes | Page; Basseville & Nikiforov | `a2.*` | Optimality not claimed for agents ✓. Observe-only ✓. Benign false-alarm rate 0.106 against a 0.05 target |
| 3.20 | ECE, binary, equal-width bins | Yes | Yes | Naeini; Guo | `probabilistic.ece` | Recomputed independently: 0.043761 ✓. Unstable with sparse middle bins (acknowledged) |
| 3.21 | Log-loss with clipping | Yes | Yes | Derived | ✓ | Recomputed: 0.201344 ✓ |
| — | Brier score | The binary convention is correct | Not defined in Ch. 3 (deferred) | — | `brier_binary` | Ch. 3 withholds it; Ch. 5 reports it (SC-5) |
| 3.22 | Realized loss | Yes | Yes | Definition | `stage_observe` | Favours REM by construction (stated). **No regret metric** is defined (none against an oracle policy or a matched-cost optimum) |

No equation is mathematically wrong. Every symbol is defined in Table 3.4 or at its point of use, and the notation is consistent across Ch. 3–6. One textual inconsistency affects the methodology: §3.11.11 still claims that the two mitigation semantics cannot differ under replay (Issue M-3).

## 2. Specific questions

**Is Platt scaling justified after logistic regression?**
Only weakly. Penalized logistic regression is fitted by likelihood and was already close to calibrated: γ₁ = 0.945–0.981, and ECE was 0.044 with calibration and 0.042 without. The thesis admits that calibration gave no improvement and could not repair the miscalibration of the unseen category (fold 7). Calibration is defensible as a safeguard, because ridge shrinkage and fold shift can distort probabilities. Its *empirical* justification in this thesis, however, is nil.

**Is calibration free of leakage?**
Yes. `crossfit.py` fits (γ₁, γ₀) on inner out-of-fold logits within each outer fitting portion, and never uses held-out labels. The reference sets (x̄, benign transitions) and E0 feature retention are fold-specific. No leakage was found.

**Is the decision mechanism "Bayesian"?**
It is a *plug-in Bayes decision rule*: it minimizes expected loss under an estimated posterior. There is no Bayesian inference (no prior over β, no posterior predictive). Calling it "Bayesian expected loss" is acceptable only with that qualification.

**Is the expected-loss rule a research contribution?**
No. The thesis says so itself (§3.13). It is a standard cost-sensitive rule (Elkan; Chow) extended to four actions with tier-indexed losses. The derived results (Eqs. 3.8–3.10, the dominance check) are correct, elementary consequences, useful for auditability and for the "threshold = cost ratio" argument. They are not novel theory.

**Step-level vs episode-level mitigation and tie-breaking.**
Both remain unresolved supervisor decisions (D-2/SC-1 and D-4/SC-2). They must not be resolved silently, and they are not. The R4 sensitivity table (Ch. 5 Table 5.11) shows that the semantics change B1's ASR (0.055 → 0.046) and every configuration's utility under attack. One residual sentence (Ch. 3 line 821) still contradicts this.

**Numerical and statistical risks:**
- The intervals come from a percentile bootstrap over nine groups and need not reach nominal coverage (stated).
- p in [1/21, 1/2] decides the tier-4 verdicts. Calibration quality in that region is not reported separately, although §3.12.2 promised "reliability within declared windows around each tier's threshold".
- There is no correction for multiple comparisons.

## 3. Algorithmic contribution audit

| Question | Answer |
|---|---|
| What is novel? | No algorithmic or mathematical element. The candidate novelty is the *composition* (provenance evidence → calibrated per-call probability → tier-indexed four-verdict expected loss → deterministic mitigation and audit) and the *evaluation design* (same-estimator baseline; a variant with the same escalation opportunity) |
| What is adapted? | Elkan's rule to four verdicts with tiers; Platt calibration applied to a logit; linear SHAP as an audit field |
| Integration of existing methods? | Yes, entirely |
| Is the integration justified? | Theoretically coherent: thresholds follow from costs, and Escalate's feasibility is explicit. Empirically **not shown to be necessary**: calibration and behavioural features add nothing, and a one-feature provenance rule matches REM's attack interception with fewer false interventions (Issue C-2) |
| Is the theoretical foundation correct? | Yes (Section 1) |
| Does the evidence demonstrate the contribution? | No. The evidence is exploratory and replay-based. It shows that the configuration intervenes far more on legitimate actions than B1, and it does not isolate any benefit of the decision layer over simpler rules |

**Verdict on the algorithm.** It is mathematically correct and implemented faithfully in the evaluation path. As a master's-level *integrative* artifact it is defensible **only if** the thesis:
- reframes the contribution as an empirical study of when consequence-tiered expected-loss decisions help or hurt;
- adds the missing simple baselines;
- corrects the residual inconsistency.

As a claimed advance in runtime protection, it is **not currently defensible**.
