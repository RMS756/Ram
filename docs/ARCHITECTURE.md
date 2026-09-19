# ARCHITECTURE

The structure of the REM implementation and the reasoning behind it. The layer
count, pipeline order, verdicts and mitigation semantics are **not** decisions
made here — they are fixed by [`CLAUDE.md`](../CLAUDE.md). This document
explains how the code realises them.

---

## 1. The five frozen layers

`CLAUDE.md` § FROZEN ARCHITECTURE fixes exactly five, with offline fitting and
recalibration cross-cutting.

| Layer | Responsibility | Module |
| ----- | -------------- | ------ |
| L1 Input & Context | Provenance labeling; context/behavioural/action evidence → `x_t` | `rem/core/interfaces.py` (contracts) |
| L2 Detection | `s_t = β₀ + βᵀx_t`, `p̃_t = σ(s_t)` | `rem/algorithms/detection/ridge_logistic.py` |
| L3 Behavioral Analysis | Behavioural evidence feeding L1's evidence stage | `rem/core/interfaces.py` (contract) |
| L4 Decision Engine | Consequence tier, policy predicates, `argmin_v R_t(v)` | `rem/algorithms/decision/expected_loss.py` |
| L5 Mitigation | Canonical step-level enforcement | `rem/core/mitigation.py` |
| *cross-cutting* | Platt-on-logit calibration | `rem/algorithms/calibration/platt.py` |
| *audit-only* | Linear Shapley attribution | `rem/algorithms/attribution/linear_shapley.py` |

`Layer.FROZEN_LAYERS` names the five in code, and a test asserts there are
exactly five and that `feedback` is not among them.

**Where L3 sits.** The frozen pipeline string does not list behavioural analysis
as its own stage; its second stage is *"context / behavioral / action evidence"*.
Behavioural analysis therefore **feeds the evidence vector** rather than
bypassing it into the verdict. `ContextProcessor.process` accepts the
`BehaviorResult` for that reason. An observe-only signal (CUSUM) sets
`observe_only=True` and never becomes a feature.

---

## 2. Data flow

```text
TrajectoryStep(t) + Trajectory.prefix(t)      ← causal: steps ≥ t are withheld
        │
        ├─ ProvenanceLabeler ──────────────► labels on content
        ├─ BehaviorModel (L3) ─────────────► BehaviorResult
        └─ ContextProcessor (L1) ──────────► FeatureVector x_t
                    │
                    ▼
          RidgeLogisticRegression (L2) ────► s_t (LOGIT), p̃_t (UNCALIBRATED)
                    │
                    ▼
          PlattLogitCalibrator ────────────► p_t (CALIBRATED)
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
  ConsequenceTier k_t     PolicyPredicates
        └───────────┬───────────┘
                    ▼
      ExpectedLossDecisionEngine (L4) ─────► Decision + full R_t(v) table
                    │
                    ▼
      DeterministicMitigationEngine (L5) ──► MitigationOutcome
                    │
                    ▼
          LinearShapleyAttributor ─────────► AttributionResult (audit only)
                    │
                    ▼
                AuditLog ────────────────► JSONL record
```

Attribution is drawn **after** mitigation deliberately: by the time it runs, the
verdict is already final and recorded, so it cannot influence it even by
accident.

---

## 3. Load-bearing decisions

### 3.1 Score semantics travel with the score

`ScoreSemantics` distinguishes `LOGIT`, `UNCALIBRATED_PROBABILITY` and
`CALIBRATED_PROBABILITY`. The decision engine reads `.calibrated_probability`,
which raises on anything else.

This closes a specific failure: in the frozen design `p̃_t = σ(s_t)` is *also* a
number in [0,1], so it would substitute for `p_t` silently and the Bayes verdict
would still compute — just wrong. The type system makes that impossible.

### 3.2 Calibration operates on the logit, not the probability

`Calibrator.transform` requires `DetectionResult.logit`. `DetectionResult`
carries `logit` as a separate field for this reason: the frozen equation is
`p_t = σ(γ₁·s_t + γ₀)`, and calibrating `p̃_t` instead would be a different
method with different parameters.

### 3.3 Causality is structural

Components receive `trajectory.prefix(t)`, containing only steps `0..t-1`. A
runtime detector that peeks at later steps reports offline performance while
claiming runtime performance. Withholding the future removes the possibility.

### 3.4 The detector emits no class label

`detect()` returns `label="unthresholded"`. Applying a 0.5 cut would be an
invented operating point, and in the frozen design the verdict comes from the
Bayes rule, not from thresholding the detector. The operating-point threshold
policy exists only as a **baseline**.

### 3.5 The full risk table is recorded

`Decision.conditional_risk` and the audit record carry `R_t(v)` for all four
verdicts, not just the winner. The argmin can then be re-checked from the audit
trail alone — which matters because the loss grid is the one place a decision
policy could be smuggled in.

### 3.6 Evidence carries no weight

`Evidence` has `name`, `value`, `producer`, `detail` — no `weight`, no
`severity`. Combining evidence is the fitted model's job; a severity field would
be an invented weight entering through the data model, inherited by every
consumer. A test asserts the fields stay absent.

### 3.7 Mitigation is enforcement, never inference

`rem/core/mitigation.py` contains no scoring. The verdict→mechanism mapping is
`MappingProxyType`, immutable at runtime, because it is frozen design rather
than configuration. All four mechanisms act on the current step; the enumeration
contains no episode-level mechanism at all, so "Block disables all tools for the
episode" cannot be expressed without adding a new member — which a test blocks.

### 3.8 Ties and monotonicity fail loudly

An exact argmin tie raises `VerdictTieError`; a fitted `γ₁ ≤ 0` raises
`MonotonicityViolationError`. Both are cases where a plausible silent choice
exists and neither is frozen, so both stop.

### 3.9 Observed states are not model states

`AgentState` records observed execution states. It is not a latent state space —
the frozen design has no latent-variable trajectory model, and GRU/LSTM/
Transformer trajectory models are forbidden reintroductions.

### 3.10 The audit log stores digests

Prompts, model outputs and tool arguments are the agent's payload and in a
security setting are exactly what may contain credentials or personal data.
SHA-256 digests prove *which* payload a decision concerned without retaining it.
Verbatim capture is opt-in for offline experiments.

---

## 4. Ablation

`AblationSpec` disables elements; the pipeline skips them while keeping one
control flow, so a difference in results is attributable to the element rather
than to a second code path.

**`REM - Calibration` is not a valid ablation** and the pipeline refuses it. The
expected-loss verdict is *defined* on the calibrated probability; removing
calibration does not ablate the frozen design, it replaces it with a different
one. Substituting `p̃_t` silently would misreport that as an ablation result.
Ablating the decision layer as well is permitted.

---

## 5. Traceability

`rem/traceability/registry.py` separates two things the previous iteration
conflated:

* a **citation** — a fact about the literature, always recorded;
* an **equation ID** — a key into the authoritative registry, recorded only when
  that registry exists.

`@derivation` therefore takes `statement`, `source`, `location` and `algorithm`
as required arguments and `equation_id` as optional. Passing an ID without a
configured registry raises `RegistryUnavailableError`. Nothing is synthesised,
and `docs/MATHEMATICAL_TRACEABILITY.md` reports `AUTHORITATIVE EQUATION IDs: 0`
so it cannot be read as a closed chain.

---

## 6. Dependencies

NumPy (the frozen estimator is fitted by Newton-Raphson) and PyYAML
(configuration). Nothing else. scikit-learn is deliberately absent: its
`LogisticRegression` default `C=1.0` would silently supply the ridge penalty
that the design leaves unresolved.
