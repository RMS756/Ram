# STAGE 3 — IMPLEMENTATION CONSISTENCY AND CHANGE PLAN

**Date:** 2026-09-19 · **Baseline `f46c126`, tree clean, 154/154 passing**
**Analysis only — NO code, test or configuration was modified.**

---

# N. IMPLEMENTATION CONSISTENCY FINDINGS

## N.1 Audit results

| # | Check (§24) | Finding | Severity |
| - | ----------- | ------- | -------- |
| 1 | **`detect()` threshold usage** | `ridge_logistic.py:380` returns `label="unthresholded"`. Grep for `(>=|>) 0.5` across `rem/` returns **no matches**. The only `0.5` literals are the p50 percentile level and the ½ in `(λ/2)‖β‖²` | ✅ **No inconsistency** |
| 2 | Detection vs Decision separation | Detection emits `s_t`, `p̃_t`; the Decision Engine determines the verdict. `decide()` reads `.calibrated_probability`, which raises on uncalibrated input | ✅ Correct |
| 3 | Five-layer architecture | `Layer.FROZEN_LAYERS` has exactly 5; test-enforced | ✅ Correct |
| 4 | Feedback treatment | No feedback layer, no sink; a test greps the pipeline source | ✅ Correct |
| 5 | Calibration implementation | Platt-on-logit; smoothed targets verified verbatim; `γ₁ > 0` enforced | ✅ Correct |
| 6 | Decision policy | `argmin_v R_t(v)`; full risk table recorded; ties raise | ✅ Correct |
| 7 | Mitigation implementation | Canonical step-level; mapping immutable; no episode-level mechanism | ✅ Correct |
| 8 | Equation ↔ implementation | 19 operations, each carrying statement + citation | ✅ Correct |
| 9 | **Feature definitions** | **None exist.** `FeatureVector` is a contract; no extractor is implemented | ⚠️ **Gap — expected** |
| 10 | **No behavioural algorithm** | L3 has a contract only | ⚠️ **Gap — expected** |
| 11 | **No sequential component** | No CUSUM implementation; `configs/behavior.yaml` records it observe-only | ⚠️ **Gap + Conflict 2** |
| 12 | **SHAP status** | Implemented as frozen audit-only; instruction proposes "optional" | ⚠️ **Conflict 3** |
| 13 | **Calibration ablation path** | Pipeline **refuses** `REM − Calibration`, foreclosing formulation B | ⚠️ **Defect D2 (carried)** |
| 14 | **Loss-grid coherence** | `LossGrid` checks completeness, **not** Elkan's conditions | ⚠️ **Defect D1 (carried)** |
| 15 | Platt fitting protocol | Single held-out split vs Platt's 3-fold CV | ⚠️ **Defect D3 (carried)** |

**No methodology inconsistency was found in the existing code.** Items 9–11 are
absent components, not wrong ones — and their absence is correct under
fail-closed operation. Items 12–15 are carried forward, unfixed.

## N.2 Newly identified — REM's evaluation design must change

Two verified findings change the evaluation design, not the code:

**N.2.1 Closed-loop identifiability** (*What Can Be Enforced?*, arXiv:2607.22868,
result 3). Once blocking changes future proposals, static scores and ungated
trajectories need not identify the closed-loop frontier. REM's current
experiment runner evaluates trajectories offline. **Offline Q1/Q2 results cannot
establish Q3.** Requires either a gated/online evaluation arm or an explicit
stated limitation.

**N.2.2 Detector latency budget.** PromptGuard 2 22M costs **19.3 ms per
classification at 512 tokens on an A100**. DreamGuard reports **25 ms total**
end-to-end. If REM adopts the extractor naively, the extractor alone nearly
exhausts a competitive budget. Mitigations to evaluate: invoke only on untrusted
content, cache by content digest, batch. **Must be measured on the target
hardware, not assumed.**

## N.3 Tension between the instruction and the frozen lock

Summarised from `STAGE3_PRIOR_ART_AND_POSITIONING.md`; all three require
supervisor decisions before any code changes.

| # | Conflict | Instruction | `CLAUDE.md` | Recommendation |
| - | -------- | ----------- | ----------- | -------------- |
| 1 | Beta calibration | §11 "investigate Platt **and Beta**, select by evidence" | Beta is a **forbidden reintroduction** | **Keep Platt.** NEXUS independently selected Platt over isotonic for lowest ECE on a small calibration split — corroborating evidence, no lock change needed |
| 2 | CUSUM in C4 | §15 C4 makes the sequential detector a candidate configuration | *"CUSUM MUST NOT enter the core verdict path"* | **CUSUM statistic as an evidence feature in `x_t`.** This is REM's strongest remaining contribution; without it REM reduces toward NEXUS. **Pivotal decision** |
| 3 | SHAP status | §14 "optional supplementary" | *"audit-only"* (frozen) | **Retain as-is.** Already implemented, `O(d)`, removing it gains nothing |

---

# O. EXACT LIST OF FILES REQUIRING MODIFICATION

**Nothing below has been changed.** Each entry states the trigger that must
clear first. Per §25, files are modified only after the analysis stages, and
per `CLAUDE.md` § CHANGE CONTROL, frozen items need explicit approval.

## O.1 GREEN — implementable now, no decision required

| File | Change | Rationale |
| ---- | ------ | --------- |
| `rem/algorithms/decision/expected_loss.py` | Add Elkan coherence validation to `LossGrid.__post_init__` | **D1.** Elkan's conditions are source-verified and checkable **independently of the values** |
| `rem/evaluation/metrics.py` | Add `log_loss`; add `expected_calibration_error` marked supplementary-only | Both proper scoring rules cited; ECE explicitly **not** proper |
| `rem/evaluation/metrics.py` | Add `verdict_reachability_report` | Mathematical property of the frozen rule (each `R_t(v)` affine in `p_t`); adds no design decision |
| `tests/test_frozen_math.py` | Tests for the above | Standard |
| `docs/MATHEMATICAL_TRACEABILITY.md` | Regenerate | Auto-generated |

## O.2 YELLOW — blocked on a supervisor decision

| File | Change | Blocked on |
| ---- | ------ | ---------- |
| `rem/algorithms/context/` *(empty)* | Group A/B/C feature extractors | **SD-FEAT** — final feature set |
| `rem/algorithms/context/` | PromptGuard 2 22M wrapper as fixed extractor | **SD-DET** — approval to add the dependency + latency budget |
| `rem/algorithms/behavior/` *(empty)* | CUSUM with stated ARL₀ | **Conflict 2** — pivotal |
| `rem/algorithms/decision/expected_loss.py` | Consequence-tier assigner | **SD-2** — tier definition (recommend reversibility + amount + authorization) |
| `rem/core/mitigation.py` | Modify mechanism | **SD-3** — the ONE declared mechanism |
| `rem/core/pipeline.py` | Named, logged `p̃`-substitution path for the calibration ablation | **ED-4** — ablation formulation (**D2**) |
| `rem/algorithms/calibration/platt.py` | CV-based fitting option | **ED-5** — protocol (**D3**) |
| `configs/detection.yaml` | `feature_set`, `ridge_penalty_lambda`, `injection_classifier` | SD-FEAT, ED-2→ED-3 |
| `configs/decision.yaml` | `loss_grid`, `consequence_tiers`, `policy_predicates`, `tie_breaking_rule` | **SD-1**, SD-2, SD-4 |
| `configs/mitigation.yaml` | `modify_mechanism` | SD-3 |
| `configs/behavior.yaml` | CUSUM parameters + target ARL₀ | **Conflict 2** |
| `configs/experiment.yaml` | `agentdojo_version`, `grouping_scheme`, benchmarks, splits, repeats | ED-1, **ED-2** |
| `pyproject.toml` | Add benchmark + extractor dependencies | SD-DET, ED-1 |
| `experiments/` | Nine-category experimental matrix; baselines B0–B4; five ablations | Everything above |

## O.3 RED — must not be modified

| File | Reason |
| ---- | ------ |
| `CLAUDE.md` | The contract. Amendable **only** by explicit supervisor decision |
| `rem/algorithms/detection/ridge_logistic.py` — runtime scoring | Frozen equations, correct |
| `rem/algorithms/calibration/platt.py` — `calibrate()` | Frozen equation, verified faithful |
| `rem/algorithms/decision/expected_loss.py` — `conditional_risk`, `argmin_verdict` | Frozen equations |
| `rem/core/results.py` — `Verdict`, `MitigationAction` | Frozen verdict set and canonical semantics |
| `rem/core/mitigation.py` — `CANONICAL_MECHANISM` | Frozen mapping, immutable by design |
| `rem/traceability/registry.py` | Equation-ID lock enforcement |
| `tests/test_contract_compliance.py` | Encodes the lock; weakening it would disable the guard |

## O.4 New files (once unblocked)

`rem/algorithms/context/{provenance,features_a,features_b,features_c}.py` ·
`rem/algorithms/behavior/cusum.py` ·
`rem/algorithms/decision/consequence_tier.py` ·
`rem/data/{loaders,splits}.py` ·
`experiments/{run_baselines,run_ablations,run_scenarios}.py` ·
`tests/test_features.py`, `tests/test_cusum.py`

## O.5 Files explicitly NOT to touch

No file outside the lists above is to be modified. In particular, the Stage 2
documents and the reconciliation records are **historical evidence** and must not
be rewritten to match later decisions.

---

# DECISION REGISTER — STAGE 3

| ID | Decision | Type | Gates |
| -- | -------- | ---- | ----- |
| **Conflict 2** | CUSUM as evidence feature vs strictly observe-only | **SUPERVISOR** | **REM's strongest contribution**; C4; clause C |
| **SD-1** | Loss grid values | SUPERVISOR | Every verdict and metric |
| **SD-2** | Consequence tiers — recommend reversibility + amount + authorization | SUPERVISOR | SD-1; supported by *Calibration Is Not Control* |
| **SD-3** | Modify mechanism | SUPERVISOR | Modify semantics |
| **SD-4** | Policy-predicate semantics | SUPERVISOR | Chapter 3 framing |
| **SD-FEAT** | Final feature set from Groups A/B/C | SUPERVISOR | Estimator, attribution |
| **SD-DET** | Adopt PromptGuard 2 22M as fixed extractor | SUPERVISOR | Latency budget |
| **Conflict 1** | Beta calibration — recommend keeping Platt | SUPERVISOR | Lock amendment |
| **Conflict 3** | SHAP status — recommend retaining audit-only | SUPERVISOR | Lock amendment |
| **ED-1** | AgentDojo version pin + benchmark set | EXPERIMENTAL | All runs |
| **ED-2** | Grouping scheme | EXPERIMENTAL | **ED-3, all inference, ablation power** |
| **ED-3** | λ via grouped CV | EXPERIMENTAL | Fitting |
| **ED-4** | Calibration-ablation formulation | EXPERIMENTAL | D2 |
| **ED-5** | Platt fitting protocol | PD | D3 |
| **RG-1** | Author the equation registry | ARTEFACT | Traceability closure |

## Recommended order

```text
Conflict 2  ──► determines whether REM retains a defensible contribution
                 └─► SD-FEAT ──► SD-DET
SD-2 ──► SD-1 ──► ED-4
ED-1 ──► ED-2 ──► ED-3
Independent: SD-3 · SD-4 · Conflict 1 · Conflict 3 · ED-5 · RG-1
Proceed now regardless: all of O.1 (GREEN)
```

> **Conflict 2 is the single highest-leverage decision in the project.** It
> determines whether clause C — the only clause not owned by verified prior work
> — is available to REM at all. If CUSUM cannot influence the verdict even as an
> evidence feature, REM's separation from NEXUS narrows to the decision-theoretic
> derivation alone, and the gap statement must be weakened accordingly.
