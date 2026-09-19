# STAGE 3 — CHAPTER 3 DESIGN, ALGORITHM AND EVALUATION

**Date:** 2026-09-19 · **Analysis only — no code modified**

---

# D. FINAL CHAPTER 3 STRUCTURE

## 3.1 Research Design

Design-science: construct REM, then evaluate it against three **separately
measured** questions (Q1 risk estimation, Q2 decision quality, Q3 mitigation
effectiveness). The separation is mandated by *Calibration Is Not Control*
(arXiv:2606.21399) and must not be collapsed into a single accuracy figure.

## 3.2 System Model

```text
            ┌──────────────────────── REM (non-invasive) ────────────────────────┐
 Financial  │  L1 Input & Context → L2 Detection → L3 Behavioral Analysis →      │  External
   Agent  ──┤       ↓ calibration (cross-cutting)                                ├── Environment
            │  L4 Decision Engine → L5 Mitigation → audit                        │   (tools, APIs)
            └────────────────────────────────────────────────────────────────────┘
                     offline fitting / recalibration (cross-cutting)
```

REM observes proposed actions **before execution** and returns a verdict. It
does not alter the agent's internals. *Non-invasive interception is established
by AgentTrust and NEXUS and is not claimed as a contribution.*

## 3.3 Threat Model

**In scope:** direct and indirect prompt injection; tool misuse; unauthorised
financially consequential actions; slow-burn multi-step attacks where each step
is individually sub-threshold.
**Out of scope:** model weight compromise; the agent's own misalignment absent
injection; attacks on REM itself.
**Assumption:** REM sees every proposed tool call and its arguments.
**Adversary:** controls content reaching the agent through tool output
(the AgentDojo injection-point model).

## 3.4 REM Architecture — exactly five layers

| Layer | Function | Output |
| ----- | -------- | ------ |
| L1 Input & Context | Provenance labelling; Group A/B/C evidence extraction | `x_t` |
| L2 Detection | Ridge logistic regression | `s_t`, `p̃_t` — **no class label** |
| L3 Behavioral Analysis | Session/trajectory features; sequential statistic | Group B entries of `x_t` |
| *(cross-cutting)* | Platt calibration on the logit | `p_t` |
| L4 Decision Engine | Consequence tier; policy predicates; expected-loss argmin | `v*_t` |
| L5 Mitigation | Canonical step-level control | outcome |

**No sixth layer. Feedback/recalibration is cross-cutting and offline only.**

## 3.5 Data and Feature Representation

Three conceptual groups. Each feature is labelled **SOURCE-SUPPORTED** (a prior
system uses an equivalent signal) or **POLICY-DEFINED** (an institutional design
choice, not a regulatory standard).

### Group A — Context / Text Risk

| Feature | Type | Basis |
| ------- | ---- | ----- |
| Injection-classifier score on untrusted content | **SOURCE-SUPPORTED** | PromptGuard 2 22M as a fixed extractor; LlamaFirewall alignment checking |
| Untrusted-provenance content present in context | **SOURCE-SUPPORTED** | Taint-tracking / IFC literature; CaMeL |
| Instruction-like imperative in tool output | **SOURCE-SUPPORTED** | Standard IPI indicator |
| Context inconsistency vs stated task | **SOURCE-SUPPORTED** | FinHarness cross-turn drift |
| Lightweight text representation (TF-IDF) | **POLICY-DEFINED** | Justified only if it measurably adds over the extractor score; otherwise omit |

### Group B — Behavioral / Action Risk

| Feature | Type | Basis |
| ------- | ---- | ----- |
| Tool type / category | **SOURCE-SUPPORTED** | NEXUS per-category step counts |
| Tool transition (previous → current) | **SOURCE-SUPPORTED** | Standard sequence feature |
| Step count / plan length | **SOURCE-SUPPORTED** | NEXUS plan length |
| Repeated action count | **SOURCE-SUPPORTED** | Loop/persistence indicator |
| Tool diversity | **SOURCE-SUPPORTED** | NEXUS tool diversity |
| Sensitive-tool usage flag | **POLICY-DEFINED** | Which tools are "sensitive" is institutional |
| Sequential accumulation statistic | **SOURCE-SUPPORTED** | Corll; Page (1954) — see §3.7 |

### Group C — Financial Action Risk

| Feature | Type | Basis |
| ------- | ---- | ----- |
| Transaction type | **SOURCE-SUPPORTED** | FinHarness; ASB finance |
| Amount category | **SOURCE-SUPPORTED** | FinHarness |
| Authorization state | **SOURCE-SUPPORTED** | Progent; FinHarness |
| Beneficiary change | **SOURCE-SUPPORTED** | Established financial-fraud indicator |
| Action reversibility | **SOURCE-SUPPORTED** | NEXUS irreversibility feature; *Calibration Is Not Control* recoverability |
| Tool sensitivity | **POLICY-DEFINED** | Institutional |
| Transaction sensitivity | **POLICY-DEFINED** | Institutional |

> **Policy-defined variables must never be presented as regulatory standards.**
> They are stated design choices with stated rationale.

### Design recommendation — reversibility belongs in `k_t`, not `x_t`

*Calibration Is Not Control* shows two prefixes can share a risk estimate yet
require different actions **because one is recoverable and the other is not**.
That is precisely a statement about the *loss*, not the *likelihood*.

> **Recommendation:** ground the consequence tier `k_t` in **reversibility +
> amount category + authorization state**, and keep those out of `x_t`. Placing
> them in `x_t` asserts they are evidence that an attack is occurring; placing
> them in `k_t` asserts they determine how much an error costs. The second is
> the defensible claim and is directly supported. **[SUPERVISOR DECISION
> REQUIRED]** — this resolves Stage 2's SD-2 if approved.

## 3.6 Detection Layer

Per §8: use a lightweight external detector as a **fixed feature extractor**;
**do not train a new deep detector**.

**PromptGuard 2 22M** (verified): DeBERTa-xsmall, 22M parameters, binary
benign/malicious, **19.3 ms per classification at 512 tokens on an A100**,
modified tokenizer resisting adversarial tokenization.

**Practicality assessment: YES, with one caveat.** The score becomes *one
feature* in Group A. The caveat is latency: 19.3 ms per classification against
DreamGuard's 25 ms **total** end-to-end budget means the extractor alone could
consume most of REM's budget. Mitigations to evaluate: invoke only on untrusted
content, cache by content digest, batch. **Latency must be measured, not
assumed** — the A100 figure will not transfer.

**The Detection Layer emits evidence only.** No threshold, no class label. This
is already implemented (`label="unthresholded"`).

## 3.7 Behavioral Analysis and the Sequential Component

Per §9: simple session/trajectory features first; **no GRU/LSTM/Transformer**
(also a forbidden reintroduction under `CLAUDE.md`).

CUSUM is justified only if it addresses slow-burn accumulation, stays simple,
and **its false-alarm criterion / ARL can be stated and evaluated**. Corll
establishes the accumulation idea and **explicitly lacks the calibrated
false-alarm criterion**, which is exactly the gap REM can fill.

> ⚠️ **BLOCKED — see Conflict 2 in `STAGE3_PRIOR_ART_AND_POSITIONING.md`.**
> `CLAUDE.md` states CUSUM is observe-only and *"MUST NOT enter the core verdict
> path"*. Configuration C4 requires it to matter. The recommended
> lock-compatible reading is that the CUSUM statistic becomes an **evidence
> feature in `x_t`**, influencing the verdict only through the calibrated
> posterior. **This requires supervisor approval before implementation.**

## 3.8 Decision Engine

Frozen and implemented:

```text
R_t(v) = (1 − p_t)·L(v, 0, k_t) + p_t·L(v, 1, k_t)
v*_t   = argmin_v R_t(v),   v ∈ {Allow, Modify, Escalate, Block}
```

Loss values remain **SUPERVISOR DECISION REQUIRED**. Elkan's coherence
conditions constrain them; no source supplies values.

**Prior-art overlap, stated explicitly:** NEXUS applies a *formal intervention
policy* over four actions; *What Can Be Enforced?* gives the Neyman-Pearson
false-block/miss frontier. REM's distinction is that the action is the argmin of
a **tier-indexed expected loss**, not a policy assignment or a threshold.

## 3.9 Mitigation

Canonical step-level semantics (frozen). Mapping to controls:

| Verdict | Control | Prior art |
| ------- | ------- | --------- |
| Allow | Release action | — |
| Modify | ONE declared mechanism — sanitise / minimise arguments | **AgentTrust SafeFix** — must be cited |
| Escalate | Withhold pending review | AgentTrust `review`; NEXUS confirmation request |
| Block | Prevent this action | AgentTrust `block`; NEXUS block |

**Mitigation is not claimed as novel.** The Modify mechanism is unresolved.

## 3.10 Research Variables

Three conceptual variables (§16):

| # | Variable | Operationalisation |
| - | -------- | ------------------ |
| 1 | Context/Behavioral Risk Signals | Groups A + B → `x_t` |
| 2 | Financial Action Risk | Group C → `k_t` (recommended) |
| 3 | Runtime Decision / Security Outcome | `v*_t` and the realised outcome |

Calibration, latency, mitigation effectiveness, utility and false positives are
**evaluation dimensions**, not independent variables.

---

# G. ALGORITHM CONFIGURATION MATRIX

Neutral dimensions. **No configuration is labelled "best".**

| Dimension | **C1** Rules+LR+Policy | **C2** C1+Behavioral | **C3** C2+Calibration | **C4** C2+Sequential (ARL) |
| --------- | ---------------------- | -------------------- | --------------------- | -------------------------- |
| Complexity | Lowest | Low | Low–moderate | Moderate |
| Data requirements | Labelled steps | + trajectory grouping | + held-out calibration split | + change-point tuning data |
| Interpretability | High (coefficients) | High | High | Moderate (two statistics) |
| Latency | Lowest | Low (+ sequence bookkeeping) | Low (+ O(1) sigmoid) | Low–moderate (+ O(1) update) |
| Trajectory coverage | None | Partial (features) | Partial | **Highest (explicit accumulation)** |
| Calibration | **Absent — `p̃` uncalibrated** | Absent | **Present (Platt)** | Depends on base |
| Mitigation integration | Full | Full | Full | Full |
| Financial applicability | Via Group C | Via Group C | Via Group C | Via Group C |
| **Prior-art overlap** | **High — NEXUS rules+LR** | **High — NEXUS plan features** | **Very high — NEXUS is exactly Platt+LR+rules** | **Lowest — Corll lacks the ARL** |
| Lock compatibility | ✅ | ✅ | ✅ | ⚠️ **Conflict 2** |

## Selection reasoning

Two constraints decide this, and they point in the same direction:

1. **The frozen decision rule requires a calibrated `p_t`.** C1 and C2 have no
   calibration, so their `p̃` cannot legitimately enter `R_t(v)`. They are
   viable only as **baselines**, not as the final configuration.
2. **C3 is where REM most resembles NEXUS** — Platt-calibrated LR plus rules is
   NEXUS's core. C3 alone leaves REM with little separation.

> **Recommended configuration: C3 + C4**, i.e. the calibrated pipeline with the
> sequential statistic supplying an evidence feature under a stated ARL. C3
> satisfies the frozen decision rule; C4 supplies the one clause not owned by
> prior work. **C4 is contingent on resolving Conflict 2.**
>
> **If Conflict 2 is resolved against including CUSUM**, REM reduces
> substantially toward NEXUS and the gap statement must be weakened further.
> This should be put to the supervisor in exactly those terms.

---

# H. MATHEMATICAL SOURCE MAP

| Mechanism | Formulation | Source | Identifier | Original or adapted |
| --------- | ----------- | ------ | ---------- | ------------------- |
| Logistic regression | `s = β₀ + βᵀx`; `p̃ = σ(s)` | Hastie, Tibshirani & Friedman, *ESL* 2nd ed. (2009) | Springer — ⚠️ section locators not re-verified | **Original method**, used unchanged |
| Ridge (L2) penalty | `+ (λ/2)‖β‖²` | Hoerl & Kennard (1970), *Technometrics* 12(1), 55–67 | [DOI 10.1080/00401706.1970.10488634](https://www.tandfonline.com/doi/abs/10.1080/00401706.1970.10488634) | **Original method** |
| Newton–Raphson / IRLS fit | `β ← β − H⁻¹g` | Hastie et al. (2009) | ⚠️ locator unverified | **Original method**; ½-scaling and unpenalised intercept are conventions |
| Platt scaling | `p = σ(γ₁s + γ₀)`; targets `t⁺=(N⁺+1)/(N⁺+2)`, `t⁻=1/(N⁻+2)` | Platt (1999), *Advances in Large Margin Classifiers*, MIT Press, 61–74 | — | **Original method**; REM's sign convention is `γ₁ = −A`, an **adaptation of notation only** |
| Beta calibration | — | Kull, Silva Filho & Flach (2017), AISTATS | ⚠️ not verified this session | **Discussed only** — forbidden as adopted calibrator (Conflict 1) |
| Expected-loss decision | `R(v) = Σ_y P(y)·L(v,y)`; `v* = argmin` | Elkan (2001), *IJCAI* 2001, 973–978 | [ACM DL](https://dl.acm.org/doi/10.5555/1642194.1642224) | **Principle original**; REM's **four-action, tier-indexed** form is an **adaptation stated by no source** |
| Cost-matrix coherence | `c(0,1) > c(1,1)`, `c(1,0) > c(0,0)` | Elkan (2001) | as above | **Original**, directly applicable |
| Reject / abstain | threshold `t = (C_r − C_c)/(C_e − C_c)` | Chow (1970), *IEEE Trans. Inf. Theory* 16(1), 41–46 | [DOI 10.1109/TIT.1970.1054406](https://dl.acm.org/doi/10.1109/TIT.1970.1054406) | **Original**; conceptual support for Escalate only |
| CUSUM | `S_t = max(0, S_{t−1} + z_t − k)`, alarm at `S_t > h` | **Page (1954), *Biometrika* 41(1–2), 100–115** | [DOI 10.1093/biomet/41.1-2.100](https://academic.oup.com/biomet/article-abstract/41/1-2/100/456627) | **Original method** |
| ARL / false-alarm analysis | ARL₀ (in-control), ARL₁ (out-of-control) | Page (1954) | as above | **Original**; REM's contribution is *stating and evaluating* ARL₀ for this application, which Corll does not |
| Neyman-Pearson frontier | false-block/miss frontier | What Can Be Enforced? (2607.22868) | [arXiv:2607.22868](https://arxiv.org/abs/2607.22868) | **Used as characterisation of the threshold baseline** |
| Linear SHAP | `φᵢ = βᵢ(xᵢ − E[xᵢ])`; `φ₀ = f(E[x])` | Lundberg & Lee (2017), NeurIPS 30, 4765–4774 | [arXiv:1705.07874](https://arxiv.org/pdf/1705.07874) | **Original**; reduces to linear-model attribution — **explicitly not a novelty claim** |
| Shapley value | — | Shapley (1953) | — | **Original** |
| Brier score | `(1/n)Σ(pᵢ−oᵢ)²` | Brier (1950), *Monthly Weather Review* 78(1), 1–3 | ⚠️ locator unverified | **Original** |
| ECE | binned |accuracy − confidence| | Guo et al. (2017), ICML | ⚠️ not verified this session | **Original**; **not a proper scoring rule** — supplementary only |
| Confusion-matrix metrics | precision, recall, FPR, FNR, F1 | van Rijsbergen (1979); Fawcett (2006) | ⚠️ locators unverified | **Original** |

> **No equation is presented as newly invented.** Adapted items are marked.
> **No equation ID is assigned** — the authoritative registry does not exist
> (`AWAITING REGISTRY ID`).

---

# J. REM PSEUDOCODE

```text
# Offline (cross-cutting; never at runtime)
fit_offline(train_split, val_split):
    X_tr, y_tr   ← extract_features(train_split)          # Groups A,B,C
    λ            ← grouped_k_fold_cv(X_tr, y_tr, groups)  # BLOCKED: grouping scheme
    β₀, β        ← ridge_logistic_fit(X_tr, y_tr, λ)
    s_val        ← β₀ + βᵀ·extract_features(val_split)
    γ₀, γ₁       ← platt_fit(s_val, y_val)                # smoothed targets
    assert γ₁ > 0                                          # frozen requirement
    (k_cusum, h) ← calibrate_cusum_for_target_ARL0(val_split)   # BLOCKED: Conflict 2
    return β₀, β, γ₀, γ₁, k_cusum, h

# Runtime, per proposed action
evaluate_step(step, history):
    # ---- L1 Input & Context -------------------------------------------
    step         ← label_provenance(step)                  # BLOCKED: rule unspecified
    a            ← group_A_context_features(step, history) # incl. PromptGuard score
    b            ← group_B_behavioral_features(step, history)
    c            ← group_C_financial_features(step)
    # ---- L3 Behavioral Analysis (feeds the evidence stage) -------------
    S_t          ← cusum_update(S_{t-1}, z_t, k_cusum)     # BLOCKED: Conflict 2
    b            ← b ∪ {cusum_statistic: S_t}
    x_t          ← concat(a, b)                            # c is reserved for k_t
    # ---- L2 Detection --------------------------------------------------
    s_t          ← β₀ + βᵀx_t
    p̃_t          ← sigmoid(s_t)            # UNCALIBRATED — never used as p_t
    # ---- Calibration (cross-cutting) ------------------------------------
    p_t          ← sigmoid(γ₁·s_t + γ₀)    # the only admissible p_t
    # ---- L4 Decision Engine ---------------------------------------------
    k_t          ← consequence_tier(c)                     # BLOCKED: tiers unspecified
    preds        ← policy_predicates(step, history)        # BLOCKED: semantics unspecified
    if any(preds): STOP — DESIGN BLOCKED
    for v in {Allow, Modify, Escalate, Block}:
        R[v]     ← (1 − p_t)·L(v,0,k_t) + p_t·L(v,1,k_t)   # BLOCKED: loss grid
    if argmin is tied: STOP — no tie-break rule is frozen
    v*           ← argmin_v R[v]
    # ---- L5 Mitigation ---------------------------------------------------
    outcome      ← apply_canonical_mechanism(v*, step)     # Modify BLOCKED
    # ---- Audit-only (after the verdict is final) --------------------------
    φ            ← linear_shapley(β, x_t, E[x])            # MUST NOT affect v*
    audit.write(step, x_t, s_t, p̃_t, p_t, k_t, preds, R, v*, outcome, φ)
    return v*, outcome
```

**Five blocking points remain**, each currently raising `DesignNotSpecifiedError`
rather than defaulting.

---

# K. EXPERIMENTAL MATRIX

| # | Category | Purpose | Expected verdict | Primary metric |
| - | -------- | ------- | ---------------- | -------------- |
| 1 | Benign activity | False-positive floor | Allow | FPR, benign completion |
| 2 | Direct prompt injection | Baseline detection | Block/Modify | Recall, ASR |
| 3 | Indirect prompt injection | Primary threat | Block/Modify | Recall, ASR |
| 4 | Unsafe tool use | Tool-level misuse | Block/Escalate | Recall |
| 5 | Abnormal tool sequence | Group B validity | Escalate/Block | Recall, Q1 |
| 6 | Repeated / goal-drift | Slow-burn; **clause C** | Block after accumulation | Detection delay, **ARL₁** |
| 7 | Financially sensitive **legitimate** action | Over-defense on high-stakes benign | **Allow or Escalate, never Block** | Unnecessary blocking |
| 8 | Financially risky malicious action | Highest-stakes true positive | Block | ASR, harm prevented |
| 9 | **Benign-but-suspicious** | **Over-defense measurement** | Allow, or Escalate at worst | **Unnecessary intervention rate** |

> **Categories 7 and 9 carry the utility argument.** Category 6 is the only one
> that can substantiate clause C: it requires reporting **detection delay under
> a stated ARL₀**, which is precisely what Corll does not provide.

---

# L. BASELINES AND ABLATIONS

## Baselines

| ID | Baseline | Purpose | Notes |
| -- | -------- | ------- | ----- |
| **B0** | No REM | Upper bound on attack success, upper bound on utility | Essential reference |
| **B1** | Rule-based defense only | Isolates the learned component | Represents AgentSpec/GuardAgent class |
| **B2** | Risk estimator without behavioral features (Group A + C only) | Isolates Group B | — |
| **B3** | Full candidate (C3, or C3+C4 if approved) | The proposal | — |
| **B4** | **Operating-point threshold on `p_t`** | Isolates the decision layer | **Must be included.** Characterised by the Neyman-Pearson frontier (2607.22868), so it is a *principled*, not a straw-man, baseline. Frozen as BASELINE ONLY |

> A **weak-baseline check** is required: B1 and B4 must be tuned on the
> validation split with the same budget as B3. An untuned baseline would be the
> "artificially weak baseline" a viva would challenge.

## Ablations

| Ablation | Removes | Question answered |
| -------- | ------- | ----------------- |
| − Behavioral features | Group B | Does trajectory evidence contribute? |
| − Financial features | Group C / tiering (`|k|=1`) | Does consequence tiering contribute? |
| − Calibration | Platt | ⚠️ **See below** |
| − Sequential detector | CUSUM feature | Does accumulation contribute? (clause C) |
| − Mitigation | Enforcement | Q3: does intervening change outcomes? |

> ⚠️ **The `− Calibration` ablation needs an explicit formulation.** The frozen
> decision rule is *defined* on a calibrated `p_t`, so "remove calibration" is
> ambiguous. Stage 2 identified four readings; **formulation B (substitute `p̃_t`
> for `p_t`)** is the well-defined controlled intervention. The current pipeline
> **refuses** this path (defect D2), so implementing it requires an explicitly
> named, explicitly logged experimental route — never a silent fallback.

---

# M. EVALUATION FRAMEWORK

## The three questions — never collapsed

| | Question | What it measures | Metrics |
| - | -------- | ---------------- | ------- |
| **Q1** | Does the model estimate risk meaningfully? | Discrimination + calibration of `p_t` | Recall, precision, F1, FPR, AUC; ECE, Brier, reliability diagram |
| **Q2** | Does the Decision Engine choose an appropriate action? | Action quality *given* `p_t` | Expected loss realised, action-level error, inappropriate-intervention rate, 4-class action accuracy |
| **Q3** | Does intervention actually reduce harm? | Outcome change from enforcing | Harmful actions prevented, residual ASR, mitigation success rate |

> **Q1 → Q2 is where most systems conflate.** *Calibration Is Not Control*
> shows a well-calibrated model can still choose the wrong action. Reporting a
> single "accuracy" would reproduce exactly the error that paper identifies.

## Metric categories

**Security:** ASR, recall, precision, F1, FPR.
**Calibration:** ECE (with bin count and binning scheme stated — *not a proper
scoring rule*), **Brier score** (proper, primary), log loss (proper), reliability
diagram.
**Decision quality:** realised expected loss, inappropriate intervention,
action-level error.
**Mitigation effectiveness:** harmful actions prevented, residual ASR, mitigation
success.
**Utility:** benign task completion, unnecessary blocking / escalation /
modification.
**Runtime:** decision latency (mean, p50, p95, p99), per-step overhead, total
overhead. **Comparator: DreamGuard's 25 ms average end-to-end.**

## Two mandatory methodological statements

1. **Closed-loop identifiability.** *What Can Be Enforced?* result 3: once
   blocking changes future proposals, static scores on ungated trajectories need
   not identify the closed-loop frontier. **Offline Q1/Q2 results therefore do
   not establish Q3.** Q3 requires a gated/online arm, and where that is
   infeasible the limitation must be stated explicitly.
2. **Non-independence.** AgentDojo is an executable environment, not i.i.d.
   rows. **No interval or significance test may be reported until the grouping
   scheme is frozen.** Repeated runs of the same task pairing are not independent
   observations.

## Validation sources

| Source | Role | Status |
| ------ | ---- | ------ |
| AgentDojo (Banking suite) | Primary execution-grounded | **Version must be pinned** — 36 releases exist |
| ASB finance scenario | Financial breadth | Candidate |
| RAS-Eval | Real-execution, CWE-mapped | Candidate |
| AgentDyn | Dynamic open-ended | Supporting |
| **FinVault v2** | — | **WITHDRAWN — must not be a validation source; reference only as withdrawn** |

No single source provides execution grounding + financial domain + a benign set,
so **at least two must be used** and the composition stated.
