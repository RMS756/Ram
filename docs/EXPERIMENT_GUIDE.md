# EXPERIMENT_GUIDE

How to run, reproduce and ablate REM experiments.

> **No experiment can produce results yet.** Nineteen design parameters are
> unresolved. The runner validates everything it can, writes a readiness report,
> and stops. See [`RECONCILIATION.md`](../RECONCILIATION.md).

---

## Running

```bash
pip install -e ".[dev]"

python experiments/run_experiment.py --dry-run   # validate, exit 0
python experiments/run_experiment.py             # exit 1 with DESIGN BLOCKED
python experiments/run_experiment.py --seed 7 --experiment-id my-run
```

Artefacts land in `experiments/results/<experiment-id>/`:

| File | Contents |
| ---- | -------- |
| `manifest.json` | Python version, platform, git commit and dirty flag, package version, **digest of `CLAUDE.md`**, seed and seeded sources, config digests, dataset digests, installed dependencies |
| `readiness.json` | Frozen parameter count, unresolved parameters, unattached components, planned ablations |
| `audit.jsonl` | One JSON record per evaluated step |

The `CLAUDE.md` digest matters: it records **which frozen design** a result was
produced under. If the contract changes, old results are no longer comparable,
and the digest is what makes that visible rather than a matter of memory.

---

## Reproducibility

| Requirement | Mechanism |
| ----------- | --------- |
| Random seeds | `seed_everything()` seeds stdlib `random`, `PYTHONHASHSEED`, NumPy, and PyTorch if present; the manifest records what was actually seeded |
| Configuration | `configs/*.yaml`, SHA-256 digested into the manifest |
| Frozen design version | `CLAUDE.md` digest in the manifest |
| Logging | `audit.jsonl`, one record per step |
| Experiment IDs | `new_experiment_id()`, timestamped |
| Code version | Package version, git commit, dirty flag |
| Dataset versions | SHA-256 per dataset file |
| Dependency versions | Every installed distribution |

To reproduce: check out the recorded commit, confirm the `CLAUDE.md` digest
matches, restore configs matching the recorded digests, pass the recorded
`--seed` and `--experiment-id`.

A fixed seed makes one run repeatable; it does not make a *result*
seed-independent. `experiment.number_of_repeats` is unresolved, so the
repetition protocol is a blocking item.

---

## Statistical caution

`CLAUDE.md` § DATA / EVALUATION LOCK is explicit:

> AgentDojo is an executable environment, not a set of independent i.i.d. rows.
> Never describe repeated runs of the same task pairing as independent
> observations without explicit statistical justification.

The metric functions compute point estimates over whatever they are given; they
cannot establish independence. **The grouping scheme is unresolved**, so no
interval, standard error or significance test may be reported until it is
frozen. Do not invent sample counts.

---

## Ablations

```text
Full REM
REM - Context
REM - Behavior
REM - Attribution
REM - Mitigation
```

Each disables one element while keeping the same control flow.

**`REM - Calibration` is deliberately absent.** The expected-loss Bayes verdict
is defined on the calibrated probability `p_t`; removing calibration does not
ablate the frozen design, it replaces it with a different decision rule. The
pipeline raises rather than substituting `p̃_t`, because reporting that
substitution as an ablation result would misattribute the difference to
calibration when it actually came from changing the decision layer. Ablating the
decision layer alongside it is permitted.

`REM - Attribution` must leave every verdict unchanged — attribution is
audit-only. `tests/test_pipeline.py` asserts exactly that, which makes the
ablation a live check on the audit-only guarantee rather than a formality.

---

## Data pipeline

Intended flow:

```text
Dataset → Validation → Preprocessing → Evidence extraction → x_t
       → Ridge logistic regression → Platt calibration → Consequence tier
       → Policy predicates → Expected-loss verdict → Mitigation → Evaluation
```

**Not implemented** — no dataset is available and no AgentDojo version is
frozen. What *is* fixed:

- **Split unit is the trajectory, not the step.** Splitting by step would place
  steps of one execution in both train and test, letting the model exploit
  within-trajectory correlation.
- **Calibration fits on validation only**, never train (which reproduces the
  model's optimistic bias) and never test (which invalidates the evaluation).
- **Test is touched once**, at final evaluation.

---

## Metrics

Implemented and cited — see
[`MATHEMATICAL_TRACEABILITY.md`](MATHEMATICAL_TRACEABILITY.md):

| Category | Metrics |
| -------- | ------- |
| Security | Attack detection rate (recall), precision, F1, FPR, FNR, accuracy |
| Runtime | Mean / p50 / p95 / p99 latency, throughput |
| Utility | FPR; intervention rate derived from the audit log |
| Calibration | Brier score — refuses uncalibrated input |

Undefined metrics return NaN rather than a substituted number, so a system that
made no predictions is visibly undefined rather than appearing uniformly wrong.

---

## Baselines

Per `CLAUDE.md`, the **operating-point threshold policy is a baseline only** and
must never be presented as a second primary methodology. Its threshold-selection
procedure is itself unresolved, so the baseline is not yet implementable.

CUSUM, if used, is **optional and observe-only** and must not enter the verdict
path.

---

## Adding a frozen algorithm

1. Confirm the item is **FROZEN** in `RECONCILIATION.md`. If it is PD,
   UNVERIFIED or CONFLICT, stop and report — do not implement it.
2. Implement it in `rem/algorithms/<layer>/`, decorating each mathematical
   function with `@derivation(statement=..., source=..., location=...,
   algorithm=...)`.
3. **Do not pass `equation_id`** unless the authoritative registry is configured
   via `REM_EQUATION_REGISTRY`; it will raise otherwise, by design.
4. Record the parameters in `configs/*.yaml` with `status: FROZEN` and a source.
   Anything not frozen stays `REQUIRED_FROM_DESIGN`.
5. Add tests, including at least one hand-computed expected value and one
   fail-closed case.
6. Regenerate traceability: `python scripts/generate_traceability.py`.
7. `pytest` — the contract-compliance suite must stay green.
