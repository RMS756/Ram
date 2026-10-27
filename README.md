# REM — Runtime Evaluation and Mitigation Framework for Securing LLM-based AI Agents

Master's thesis implementation, governed by **[`CLAUDE.md`](CLAUDE.md)** — the
REM Claude Code Hard Design Lock.

---

## Status

The **frozen mathematical core is implemented exactly as specified**. The
**unresolved design items are fail-closed**: REM refuses to run rather than
default them.

| | |
| - | - |
| Tests | 154 passing |
| Mathematical operations | 19, each cited |
| Unsourced operations | **0** |
| Authoritative equation IDs | **0** — registry not supplied |
| Frozen parameters | 27 |
| Unresolved parameters | 19 |
| DESIGN BLOCKED items | 7 |

Read **[`RECONCILIATION.md`](RECONCILIATION.md)** first: it classifies every
design item as FROZEN / PD / UNVERIFIED / CONFLICT and states the blocking
items in the contract's required format.

---

## The frozen pipeline

```text
provenance labeling
  -> context / behavioral / action evidence
    -> ridge logistic regression          s_t = β₀ + βᵀx_t ,  p̃_t = σ(s_t)
      -> Platt calibration on the logit   p_t = σ(γ₁ s_t + γ₀) ,  γ₁ > 0
        -> consequence tier               k_t
          -> policy predicates
            -> expected-loss Bayes        R_t(v) = (1−p_t)L(v,0,k_t) + p_t L(v,1,k_t)
                                          v*_t = argmin_v R_t(v)
              -> deterministic mitigation
                -> audit record
```

Architecture is **exactly five layers** — Input & Context, Detection,
Behavioral Analysis, Decision Engine, Mitigation — with offline fitting and
recalibration cross-cutting. There is no sixth layer, no risk-score layer and
no feedback-loop layer. Linear Shapley attribution is **audit-only**.

| Frozen element | Implementation |
| -------------- | -------------- |
| Ridge logistic regression | `rem/algorithms/detection/ridge_logistic.py` |
| Platt-on-logit calibration | `rem/algorithms/calibration/platt.py` |
| Expected-loss Bayes verdict | `rem/algorithms/decision/expected_loss.py` |
| Linear Shapley attribution | `rem/algorithms/attribution/linear_shapley.py` |
| Canonical mitigation semantics | `rem/core/mitigation.py` |

---

## Installation and use

```bash
pip install -e ".[dev]"
pytest                                          # 154 passed
python scripts/generate_traceability.py         # regenerate traceability
python experiments/run_experiment.py --dry-run  # readiness report
```

Requires Python ≥ 3.10. Runtime dependencies: NumPy and PyYAML. No ML framework
is pinned — the frozen design names no model that needs one, and neural
trajectory models are forbidden reintroductions.

---

## How the contract is enforced in code

The lock is not a comment; each clause has a mechanism and a test.

**Equation IDs cannot be invented.** `@derivation(...)` records a formula and
its citation. An `equation_id` may be supplied *only* when the authoritative
registry is configured, and passing one without it raises. No registry ships, so
all 19 operations are `AWAITING_REGISTRY_ID` and the generated report states
`AUTHORITATIVE EQUATION IDs: 0` — it cannot be mistaken for a closed chain.

**Unresolved parameters cannot be defaulted.** Reading one raises with a
`## DESIGN BLOCKED` report naming the item, why it is required, and whether a
supervisor decision is needed. `RidgeLogisticRegression` refuses to fit without
an explicit λ; `ExpectedLossDecisionEngine` refuses to exist without a loss grid.

**An uncalibrated score cannot become `p_t`.** Every score carries its
`ScoreSemantics`, and the decision engine reads `calibrated_probability`, which
raises on anything that has not been through Platt-on-logit.

**Attribution cannot reach the verdict.** It runs after the decision, the
`decide()` signature has no attribution parameter, and the engine rejects any
payload flagged `audit_only`.

**γ₁ > 0 is checked, not assumed.** A fitted non-positive slope raises
`MonotonicityViolationError` rather than silently inverting the detector.

**Ties are not broken silently.** No tie-break rule is frozen, so an exact
argmin tie raises `VerdictTieError`.

`tests/test_contract_compliance.py` asserts these clauses directly — including
that no feedback sink exists, that the canonical mitigation mapping is immutable,
and that no episode-level mitigation mechanism has crept in.

---

## What is blocked

Seven DESIGN BLOCKED items, detailed in `RECONCILIATION.md`:

1. **Loss grid `L(v,y,k)` and consequence tiers `k_t`** — the only free
   quantities in the frozen decision layer, so any value chosen silently *is*
   REM's policy.
2. **Final feature set `x_t`** — determines what the coefficients mean.
3. **Ridge penalty λ** — frozen nowhere; a library default must not be adopted.
4. **Authoritative Equation-to-Source Registry** — without it no operation can
   carry a verified identifier.
5. **Modify mechanism** — the ONE declared modification.
6. **Provenance labeling rule and policy predicates** — named in the frozen
   pipeline, never defined.
7. **AgentDojo version and the benchmark dataset** — plus the grouping scheme,
   since AgentDojo is an executable environment, not i.i.d. rows.

Supplying the **Stage 2 Final Algorithm & Mathematical Decision Report** and the
**Equation-to-Source Registry** unblocks most of these.

---

## Documentation

| Document | Contents |
| -------- | -------- |
| [`CLAUDE.md`](CLAUDE.md) | The hard design lock (authoritative) |
| [`RECONCILIATION.md`](RECONCILIATION.md) | FROZEN / PD / UNVERIFIED / CONFLICT table and blocking items |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Layer structure and design decisions |
| [`docs/MATHEMATICAL_TRACEABILITY.md`](docs/MATHEMATICAL_TRACEABILITY.md) | Generated: formula → citation → code |
| [`docs/EXPERIMENT_GUIDE.md`](docs/EXPERIMENT_GUIDE.md) | Running, reproducing and ablating |
| [`docs/guard/`](docs/guard/) | The supplied guard package |

---

## Novelty classification

| Category | In this repository |
| -------- | ------------------ |
| **Established** | Ridge logistic regression (Hastie et al. 2009); Platt calibration (Platt 1999); Bayes decision under loss (Elkan 2001); Shapley values (Shapley 1953; Lundberg & Lee 2017); confusion-matrix metrics (van Rijsbergen 1979; Fawcett 2006); Brier score (Brier 1950); sample quantiles (Hyndman & Fan 1996) |
| **Adapted** | Applying cost-sensitive expected-loss decision theory to four runtime agent actions, indexed by a consequence tier |
| **Integrated** | The frozen pipeline composing provenance, evidence, estimation, calibration, tiering, verdict and mitigation into one runtime path |
| **Proposed** | Nothing is claimed here. The REM-specific contribution is fixed by the thesis design documents, not by this implementation |

Per `CLAUDE.md`, Elkan and Chow are supporting sources for the expected-cost
principle and reject/abstain escalation respectively; **neither may be presented
as having invented REM's four-action architecture.**
