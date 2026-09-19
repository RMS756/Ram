# MATHEMATICAL_TRACEABILITY

> **Generated file — do not edit by hand.**
> Produced by `scripts/generate_traceability.py` by importing the `rem`
> package and collecting every `@derivation`-decorated callable.

Generated: 2026-09-19 04:57 UTC

## Registry status

**The authoritative Equation-to-Source Registry has NOT been supplied.**

Per `CLAUDE.md` § EQUATION-ID LOCK, no provisional identifiers have been
created. Every operation below therefore carries a *citation* but no
*equation ID*, and is marked `AWAITING REGISTRY ID`. This report does
**not** represent a complete traceability chain, and must not be read as
one. Supplying the registry and re-running this script is what closes it.

## Operations

| Code Component | Function | Algorithm | Statement | Equation ID | Source | Location | Status |
| -------------- | -------- | --------- | --------- | ----------- | ------ | -------- | ------ |
| `rem.algorithms.attribution.linear_shapley` | `LinearShapleyAttributor.base_value` | Linear SHAP (base value) | `phi_0 = f(E[x]) = beta_0 + sum_i beta_i * E[x_i]` | *not assigned* | Lundberg, S. M., & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. NeurIPS 30, pp. 4765-4774 ('Linear SHAP'); Shapley, L. S. (1953). A Value for n-Person Games. Contributions to the Theory of Games II, Princeton University Press, pp. 307-317. | Lundberg & Lee (2017), 'Linear SHAP' — base value phi_0. | **AWAITING REGISTRY ID** |
| `rem.algorithms.attribution.linear_shapley` | `LinearShapleyAttributor.shapley_value` | Linear SHAP (exact Shapley values for a linear model) | `phi_i = beta_i * (x_i - E[x_i])` | *not assigned* | Lundberg, S. M., & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. NeurIPS 30, pp. 4765-4774 ('Linear SHAP'); Shapley, L. S. (1953). A Value for n-Person Games. Contributions to the Theory of Games II, Princeton University Press, pp. 307-317. | Lundberg & Lee (2017), 'Linear SHAP' — the closed form for a linear model under feature independence. | **AWAITING REGISTRY ID** |
| `rem.algorithms.calibration.platt` | `PlattLogitCalibrator.calibrate` | Platt (logistic) calibration on the logit | `p_t = sigmoid(gamma_1 * s_t + gamma_0)` | *not assigned* | CLAUDE.md, MATHEMATICAL LOCK -> Calibration (frozen specification); method per Platt, J. C. (1999), 'Probabilistic Outputs for Support Vector Machines and Comparisons to Regularized Likelihood Methods', in Advances in Large Margin Classifiers, MIT Press, pp. 61-74. | CLAUDE.md, MATHEMATICAL LOCK -> Calibration. | **AWAITING REGISTRY ID** |
| `rem.algorithms.calibration.platt` | `PlattLogitCalibrator.fit` | Platt (logistic) calibration on the logit | `fit gamma_0, gamma_1 by minimising -sum_i [t_i log p_i + (1-t_i) log(1-p_i)], p_i = sigmoid(gamma_1 * s_i + gamma_0), with Platt's smoothed targets t+ = (N+ + 1)/(N+ + 2) and t- = 1/(N- + 2)` | *not assigned* | Platt, J. C. (1999). Probabilistic Outputs for Support Vector Machines and Comparisons to Regularized Likelihood Methods. In Advances in Large Margin Classifiers, MIT Press, pp. 61-74. | Section 2 — the sigmoid fit and its regularised (smoothed) targets. | **AWAITING REGISTRY ID** |
| `rem.algorithms.decision.expected_loss` | `ExpectedLossDecisionEngine.argmin_verdict` | Cost-sensitive expected-loss (Bayes) decision rule | `v*_t = argmin_v R_t(v)` | *not assigned* | CLAUDE.md, MATHEMATICAL LOCK -> Decision (frozen specification). Expected-cost decision principle: Elkan, C. (2001), 'The Foundations of Cost-Sensitive Learning', IJCAI 2001, pp. 973-978. Reject/abstain tradeoff: Chow, C. K. (1970), 'On Optimum Recognition Error and Reject Tradeoff', IEEE Trans. Information Theory, 16(1), 41-46. Neither source invented REM's four-action architecture. | CLAUDE.md, MATHEMATICAL LOCK -> Decision (verdict). | **AWAITING REGISTRY ID** |
| `rem.algorithms.decision.expected_loss` | `ExpectedLossDecisionEngine.conditional_risk` | Cost-sensitive expected-loss (Bayes) decision rule | `R_t(v) = (1 - p_t) * L(v, 0, k_t) + p_t * L(v, 1, k_t)` | *not assigned* | CLAUDE.md, MATHEMATICAL LOCK -> Decision (frozen specification). Expected-cost decision principle: Elkan, C. (2001), 'The Foundations of Cost-Sensitive Learning', IJCAI 2001, pp. 973-978. Reject/abstain tradeoff: Chow, C. K. (1970), 'On Optimum Recognition Error and Reject Tradeoff', IEEE Trans. Information Theory, 16(1), 41-46. Neither source invented REM's four-action architecture. | CLAUDE.md, MATHEMATICAL LOCK -> Decision (conditional risk). | **AWAITING REGISTRY ID** |
| `rem.algorithms.detection.ridge_logistic` | `RidgeLogisticRegression.decision_function` | Ridge logistic regression (runtime score) | `s_t = beta_0 + beta^T x_t` | *not assigned* | CLAUDE.md, MATHEMATICAL LOCK -> Probability estimation (frozen specification); fitting per Hastie, Tibshirani & Friedman (2009), The Elements of Statistical Learning (2nd ed.), Springer. | CLAUDE.md, MATHEMATICAL LOCK -> Probability estimation. | **AWAITING REGISTRY ID** |
| `rem.algorithms.detection.ridge_logistic` | `RidgeLogisticRegression.fit` | Ridge (L2-penalised) logistic regression, Newton-Raphson/IRLS | `minimise J(b0, b) = -sum_i [y_i log p_i + (1-y_i) log(1-p_i)] + (lambda/2)\|\|b\|\|^2, solved by Newton-Raphson: b <- b - H^-1 g, g = X^T(p - y) + lambda*b, H = X^T W X + lambda*I, W = diag(p_i(1-p_i)); the intercept is unpenalised` | *not assigned* | Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning (2nd ed.). Springer. | Section 4.4.1 'Fitting Logistic Regression Models' for the Newton-Raphson/IRLS procedure; Section 3.4.1 'Ridge Regression' for the L2 penalty. | **AWAITING REGISTRY ID** |
| `rem.algorithms.detection.ridge_logistic` | `RidgeLogisticRegression.uncalibrated_probability` | Ridge logistic regression (uncalibrated probability) | `p_tilde_t = sigmoid(s_t)` | *not assigned* | CLAUDE.md, MATHEMATICAL LOCK -> Probability estimation (frozen specification); fitting per Hastie, Tibshirani & Friedman (2009), The Elements of Statistical Learning (2nd ed.), Springer. | CLAUDE.md, MATHEMATICAL LOCK -> Probability estimation. | **AWAITING REGISTRY ID** |
| `rem.algorithms.detection.ridge_logistic` | `sigmoid` | Logistic (sigmoid) link | `sigmoid(z) = 1 / (1 + exp(-z))` | *not assigned* | Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning (2nd ed.). Springer. | Section 4.4, 'Logistic Regression' — the logistic link function. | **AWAITING REGISTRY ID** |
| `rem.evaluation.metrics` | `accuracy` | Confusion-matrix evaluation | `accuracy = (TP + TN) / (P + N)` | *not assigned* | Fawcett, T. (2006). An introduction to ROC analysis. Pattern Recognition Letters, 27(8), 861-874. | Section 2 ('Classifier performance'), p. 862 — definitions read off the confusion matrix. accuracy = (TP + TN) / (P + N). | **AWAITING REGISTRY ID** |
| `rem.evaluation.metrics` | `brier_score` | Brier score (proper scoring rule for probabilistic forecasts) | `BS = (1/n) * sum_i (p_i - o_i)^2` | *not assigned* | Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. Monthly Weather Review, 78(1), 1-3. | Equation (1), pp. 1-2. | **AWAITING REGISTRY ID** |
| `rem.evaluation.metrics` | `f1_score` | Confusion-matrix evaluation | `F1 = 2 * P * R / (P + R)` | *not assigned* | van Rijsbergen, C. J. (1979). Information Retrieval (2nd ed.). London: Butterworths. | Chapter 7 ('Evaluation') — F from the E-measure at beta = 1. | **AWAITING REGISTRY ID** |
| `rem.evaluation.metrics` | `false_negative_rate` | Confusion-matrix evaluation | `FNR = FN / (TP + FN)` | *not assigned* | Fawcett, T. (2006). An introduction to ROC analysis. Pattern Recognition Letters, 27(8), 861-874. | Section 2 ('Classifier performance'), p. 862 — definitions read off the confusion matrix. FN rate is the complement of tp rate over the positives. | **AWAITING REGISTRY ID** |
| `rem.evaluation.metrics` | `false_positive_rate` | Confusion-matrix evaluation | `FPR = FP / (FP + TN)` | *not assigned* | Fawcett, T. (2006). An introduction to ROC analysis. Pattern Recognition Letters, 27(8), 861-874. | Section 2 ('Classifier performance'), p. 862 — definitions read off the confusion matrix. fp rate = FP / (FP + TN). | **AWAITING REGISTRY ID** |
| `rem.evaluation.metrics` | `precision` | Confusion-matrix evaluation | `precision = TP / (TP + FP)` | *not assigned* | van Rijsbergen, C. J. (1979). Information Retrieval (2nd ed.). London: Butterworths. | Chapter 7 ('Evaluation') — precision as relevant retrieved / retrieved. | **AWAITING REGISTRY ID** |
| `rem.evaluation.metrics` | `recall` | Confusion-matrix evaluation | `recall = TP / (TP + FN)` | *not assigned* | Fawcett, T. (2006). An introduction to ROC analysis. Pattern Recognition Letters, 27(8), 861-874. | Section 2 ('Classifier performance'), p. 862 — definitions read off the confusion matrix. tp rate = TP / (TP + FN). | **AWAITING REGISTRY ID** |
| `rem.evaluation.runtime` | `mean` | Descriptive statistics | `mean(x) = (1/n) * sum_i x_i` | *not assigned* | Hyndman, R. J., & Fan, Y. (1996). Sample Quantiles in Statistical Packages. The American Statistician, 50(4), 361-365. | p. 361 — sample mean, preceding the quantile definitions. | **AWAITING REGISTRY ID** |
| `rem.evaluation.runtime` | `quantile` | Sample quantile, Hyndman & Fan Definition 7 | `h = (n - 1)p + 1; Q(p) = x_(floor(h)) + (h - floor(h)) * (x_(floor(h)+1) - x_(floor(h)))` | *not assigned* | Hyndman, R. J., & Fan, Y. (1996). Sample Quantiles in Statistical Packages. The American Statistician, 50(4), 361-365. | Definition 7, p. 363. | **AWAITING REGISTRY ID** |

## Counts

```text
TOTAL MATHEMATICAL OPERATIONS   19
CITED (source recorded)         19
UNSOURCED                       0
AUTHORITATIVE EQUATION IDs      0
AWAITING REGISTRY ID            19
```

19 operation(s) are cited but carry no authoritative
equation ID. The traceability chain
`Literature -> Requirement -> Algorithm -> Equation -> Code -> Test`
is therefore **open at the Equation link** and cannot be closed until the
authoritative registry is supplied.
