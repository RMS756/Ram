# 05 — Specification of the tested candidate (`M11+AZ`) and its relatives

**Status:** `[PROPOSED — SUPERVISOR APPROVAL REQUIRED]`. **Not adopted, and after the experiments (`08`) not recommended for adoption.** This document specifies exactly what was implemented and tested, so that the negative result is reproducible.

**Implementation:** `experiments/authz_study/` (isolated). Nothing under `rem/` and no approved configuration was changed.

## 1. Relationship to the approved REM

| REM layer | Approved design | Candidate `M11+AZ` | Conflict with the design lock? |
|---|---|---|---|
| 1 Input & Context | provenance labelling; trusted = system prompt and user objective | unchanged; additionally records which earlier reads were of user-named sources | Addition, isolated |
| 2 Detection / 3 Behavioural Analysis | eight features x_ctx2, x_beh1–4, x_act1–3 | the same eight, plus `z_exp`, `z_del` | **Yes**: the final feature set is unresolved (SD-FEAT); any addition needs approval |
| 4 Decision Engine | ridge logistic → logit calibration → four-verdict expected loss on P(attempt) | same estimator and calibration, fitted on *branch outcomes*; two-branch value rule | **Yes**: the mathematical lock fixes R_t(v) and argmin over four verdicts |
| 5 Mitigation | Allow / Modify / Escalate / Block, step level | Allow or Block (step level) | Narrower, not redefined; Modify and Escalate are not exercised |
| Audit | linear Shapley, audit only | not implemented for the candidate | — |

The five-layer architecture is preserved. No sixth layer, risk-score layer, LLM arbiter or sequence model is introduced.

## 2. Mathematical provenance

| # | Expression | Source | Status |
|---|---|---|---|
| E1 | τ_i(h) = Q_i(h) − Q_continue(h), Q_a(h) = E[U_a(h) \| h]; A*(h) = argmax_a Q_a(h) | Zhang et al. (2026), Eq. (1), Sec. 2.1 | Quoted |
| E2 | U_a(h) = outcome score − costs | Zhang et al. (2026), App. C.1 | Quoted (form) |
| E3 | s = β0 + βᵀx; p̃ = σ(s); p = σ(γ1 s + γ0) | REM mathematical lock (`CLAUDE.md`) | Quoted, unchanged |
| E4 | L(Allow, 1, k) = C_miss(k); L(Block, 0, k) = C_FA(k) | REM Chapter 3 Table 3.13; values declared exploratory in `pilot_e0.yaml` | Quoted, unchanged |
| E5 | withhold iff C_miss(k)·ΔŜ(x) ≥ C_FA(k)·ΔÛ(x) and C_miss(k)·ΔŜ(x) > 0 | this study | **DERIVED — NOT DIRECTLY QUOTED FROM THE SOURCE** (derivation below) |

### Derivation of E5

Let the action set at a proposed call h be {r = release, w = withhold}. For each branch a, let S_a ∈ {0,1} be the benchmark's attack-success outcome of the episode and U_a ∈ {0,1} its user-task outcome, with every other recorded call released (the fixed continuation policy required by Zhang et al., Sec. 4.1).

Define the branch utility in REM's declared cost units, in the form of E2 (an outcome score minus costs), using the two costs of E4:

  𝒰_a(h) = − C_miss(k)·S_a − C_FA(k)·(1 − U_a).

Then, by E1,

  τ_w(h) = Q_w(h) − Q_r(h) = C_miss(k)·E[S_r − S_w | h] − C_FA(k)·E[U_r − U_w | h].

Write ΔS = S_r − S_w and ΔU = U_r − U_w, each in {−1, 0, 1}. With a = 1[ΔS = 1], a⁻ = 1[ΔS = −1], b = 1[ΔU = 1], b⁻ = 1[ΔU = −1]:

  E[ΔS | h] = P(a = 1 | h) − P(a⁻ = 1 | h),  E[ΔU | h] = P(b = 1 | h) − P(b⁻ = 1 | h).

A*(h) = w iff τ_w(h) > 0, i.e. C_miss(k)·E[ΔS | h] > C_FA(k)·E[ΔU | h]. Replacing the conditional expectations by estimates on features x gives E5; the tie convention (withhold on equality when the left side is positive) is a declared choice that follows REM's Chapter 3 tie order.

**Assumptions added by the adaptation** (none is in the source):
1. The two costs C_miss and C_FA may be read as costs of realized outcomes (attack succeeded; user task failed) and not only of step labels.
2. The cost of a successful attack is charged at the tier of the call being decided.
3. Outcomes are those of the benchmark's own checks; an unauthorized transfer that does not satisfy the benchmark's success check contributes nothing to ΔS. (This assumption turned out to matter; see `08`. Arm `M11y` replaces the security side by P(y = 1 | x) to test it.)
4. NO-ADAPT: the continuation after either branch is the recorded one.

**Independent check of the derivation.** With ΔÛ ≡ 1 (every withheld legitimate call breaks the task) and ΔŜ ≡ p, E5 becomes p·C_miss(k) ≥ C_FA(k), which is not REM's Allow–Block boundary p ≥ C_FA/(C_FA + C_miss) (Eq. 3.9): REM charges C_FA for a withheld call only when the call is legitimate (probability 1 − p), while this special case charges it always. The two rules are therefore different rules even in that special case; `M01` (REM's own rule restricted to Allow and Block) is included to keep the comparison honest.

## 3. Authorization evidence (declared definitions, not published formulas)

Rationale: PROVISO's admissibility statement (operation and target licensed by trusted observations; arguments may be supplied by external ones) and Task Shield's remark that a tool output may define subtasks when the user delegates to it.

For a call to a restricted tool: K = declared key arguments present; K_id = K without `amount`; K_ref = K_id if non-empty else K; g = user objective. A *user-named source* is the output of an earlier executed read call one of whose string arguments (length ≥ 3) occurs in g.

- `z_exp` = 1 iff K_ref ≠ ∅ and every value of K_ref occurs in g.
- `z_del` = 1 iff K_ref ≠ ∅, not all values occur in g, and every value not in g occurs in a user-named source.

Code: `experiments/authz_study/authz_evidence.py` (`authz_evidence`, `offline_authz`, `RuntimeAuthz`). Tests: `tests/test_authz_study.py`.

**Known limitation, by construction:** both features test *where a value occurs*. A recipient and amount mentioned by the user in a read-only request give `z_exp` = 1.

## 4. Pseudocode

```
Offline (per fitting portion; REM Procedure 3.1 unchanged except for the target)
  for each recorded episode e and each proposed call j:
      (U0, S0)  <- replay e with every call released
      (Uj, Sj)  <- replay e with call j withheld, all others released
      a_j, a⁻_j, b_j, b⁻_j  <- indicators of ΔS_j = S0 − Sj and ΔU_j = U0 − Uj
  for target t in {a, a⁻, b, b⁻}:
      skip t if it has fewer than 50 positive steps in the fitting portion
      select λ by 4-fold grouped inner CV; calibrate on inner out-of-fold logits; refit   (REM's routine)

Runtime (per proposed call; no label or outcome is read)
  x  <- REM features (8) and authorization evidence (2)
  k  <- consequence tier (REM's tier map)
  if predicate D1 or D2 fires: return its verdict                         (REM's predicates)
  ΔŜ <- P̂(a=1|x) − P̂(a⁻=1|x);  ΔÛ <- P̂(b=1|x) − P̂(b⁻=1|x)
  if C_miss(k)·ΔŜ ≥ C_FA(k)·ΔÛ and C_miss(k)·ΔŜ > 0: return Block (withhold this call only)
  else: return Allow
```

## 5. Interfaces

- `study.fit_cell(train_mask, feature_sets, targets)` → fitted models and the benign transition reference for one fitting portion. On the original folds, features and label it reproduces the frozen REM fits to 4·10⁻¹⁴.
- `study.make_guard(arm, cell, episode, setup)` → a `RemGuard` (REM's own class) whose decide function implements the arm. Enforcement, tool execution and auditing are REM's unchanged replay code.

## 6. What the candidate does not do

- It does not decide between Modify, Escalate and Block: their outcomes cannot be told apart in replay, so no value can be learned for them without inventing one.
- It does not use an oracle reviewer.
- It does not establish authorization: see the limitation in section 3.
