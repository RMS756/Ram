# Deliverable 15: Cost-sensitivity experiment protocol (DiD-3c, exploratory)

**Status.**
- Committed before the cost-grid replay is run.
- **Classification: EXPLORATORY.** All held-out folds of POP-P were used in earlier analyses, including the E6 grid of the pilot. There is no untouched confirmatory set.

## 1. Inspected equations and implementation (REM v1.0, unchanged)

**Conditional risk** for each verdict v:

R_t(v) = (1 − p_t) · L(v, 0, k_t) + p_t · L(v, 1, k_t)

**Verdict:** v* = argmin_v R_t(v), with v1.0's predicates D1/D2 applied first and its declared tie order.

**Losses** (`configs/exploratory/pilot_e0.yaml`, `experiments/pilot/run_main.py::loss_spec`):

| Verdict | L(v, 0, k) (benign call) | L(v, 1, k) (attack call) |
|---|---|---|
| Allow | 0 | C_miss(k) |
| Block | C_FA(k) | 0 |
| Escalate | C_esc | C_esc |
| Modify | C_mod(k) | r_mod(k) · C_miss(k) |

The construction is `rem/algorithms/decision/loss_matrix.py::build_loss_grid`.

**Declared values:**

| Quantity | Value | Status |
|---|---|---|
| C_FA(k) | 1 for every tier | EXPLORATORY DECLARED, 27 Oct 2026 |
| C_miss(k) | 1, 5, 10, 20 for tiers 1–4 | EXPLORATORY DECLARED, 27 Oct 2026 |
| C_mod(k) | 0.5 | EXPLORATORY DECLARED, 27 Oct 2026 |
| C_esc | 0.3 | EXPLORATORY DECLARED, 27 Oct 2026 |
| r_mod | Measured by replay within the fitting folds | — |
| Tier of a value transfer | 3 if amount ≤ amount_limit, else 4 | Base amount_limit 1,000 |

**None of these is a frozen REM value** (CLAUDE.md: the loss grid remains unresolved).

## 2. Grid (already declared in `pilot_e0.yaml` §grid; no new value is introduced)

| Axis | Values |
|---|---|
| C_miss multiplier | 0.5, 1, 2, 5 |
| C_esc | 0.1, 0.3, 0.6 |
| amount_limit | 100, 1,000, 10,000 |

This gives 36 cells. The grid's `alpha_blk` axis belongs to baseline B1 of the pilot and is not used here.

## 3. Arms and data

| Arm | Description |
|---|---|
| B1 | REM v1.0 alone |
| B9 | Full REM-DiD, oracle TAE |
| X0 | Full REM-DiD with authorization bypassed (broad TAE) |

- Each arm is replayed on POP-P (2,979 attacked + 334 benign) for every cell, with 4B's policy rebuilt from that cell.
- Everything else is as in DiD-3. Folds are unchanged; the fitted models are unchanged (costs do not enter fitting).

## 4. Outputs and analysis

**Per cell and arm:**
- successful attacks;
- benign tasks completed;
- legitimate state-changing calls withheld;
- escalations.

**Analysis:**
- **All 36 cells are reported, in a table and a figure.** No cell is selected as "best".
- Stability of two questions across cells:
  - (a) Does 4B add security behind oracle authorization? Compare B9 with B9n from DiD-3; B9n does not depend on costs.
  - (b) How much residual protection does 4B give when authorization is bypassed? Compare X0 with X-only-LEARN.

## 5. Split note

**There is no development / validation / confirmatory split.** All data was used before. The grid analysis is therefore descriptive sensitivity analysis, not model selection, and **no cost setting is recommended from it**.

## 6. Results (added after the run, 357,804 replays, 0 errors)

See `51_DID3_RESULTS.md` §9 and `figures/fig_did3_cost_grid.png`. In summary:
- REM v1.0: 0–13 attacks and 105–124 benign tasks across cells.
- B9: 0 attacks in all cells, 105–124 benign tasks (B9n, which does not depend on costs, completes 173).
- X0: 0–1 attacks.
