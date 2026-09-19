# REM RECONCILIATION TABLE

**Produced under:** `docs/guard/START_PROMPT.md` steps 6–7 (*"DO NOT code until this table has been produced"*)
**Governing contract:** `CLAUDE.md` — REM Claude Code Hard Design Lock
**Date:** 2026-09-19

---

## 0. Document availability

START_PROMPT requires five documents to be read before coding. Availability:

| # | Document | Status |
| - | -------- | ------ |
| 1 | `CLAUDE.md` (hard design lock) | ✅ **SUPPLIED** — governs everything below |
| 2 | Stage 2 Final Algorithm & Mathematical Decision Report | ❌ **NOT SUPPLIED** |
| 3 | Approved thesis proposal | ❌ **NOT SUPPLIED** |
| 4 | Equation-to-Source verification material | ❌ **NOT SUPPLIED** |
| 5 | Current implementation specification | ✅ present — this repository (commit `0a7a803`) |

`CLAUDE.md` freezes the pipeline, architecture, verdicts, three core equations,
attribution role and mitigation semantics. That is enough to implement the
mathematical core. It does **not** supply the loss grid, consequence tiers,
feature set, ridge penalty or benchmark version, all of which stay blocked.

---

## 1. FROZEN — implement exactly

| Item | Current value | Source | Status |
| ---- | ------------- | ------ | ------ |
| Pipeline order | provenance → evidence → ridge logistic regression → Platt-on-logit → consequence tier → policy predicates → expected-loss Bayes verdict → deterministic mitigation → audit | `CLAUDE.md` § FROZEN REM PIPELINE | **FROZEN** |
| Architecture | Exactly 5 layers: L1 Input & Context, L2 Detection, L3 Behavioral Analysis, L4 Decision Engine, L5 Mitigation. Offline fitting/recalibration cross-cutting. No 6th layer, no risk-score layer, no operator node, no feedback layer | `CLAUDE.md` § FROZEN ARCHITECTURE | **FROZEN** |
| Verdict set | Allow, Modify, Escalate, Block | `CLAUDE.md` § FROZEN REM PIPELINE | **FROZEN** |
| Probability estimator | Ridge logistic regression; `s_t = β₀ + βᵀx_t`; `p̃_t = sigmoid(s_t)` | `CLAUDE.md` § MATHEMATICAL LOCK → Probability estimation | **FROZEN** |
| Calibration | Platt/logistic on the logit; `p_t = sigmoid(γ₁ s_t + γ₀)`; `γ₁ > 0` required for monotone interpretation | `CLAUDE.md` § MATHEMATICAL LOCK → Calibration | **FROZEN** |
| Decision rule | `R_t(v) = (1−p_t)·L(v,0,k_t) + p_t·L(v,1,k_t)`; `v*_t = argmin_v R_t(v)` | `CLAUDE.md` § MATHEMATICAL LOCK → Decision | **FROZEN** |
| Decision-theory attribution | Elkan supports the expected-cost principle; Chow is conceptual support for reject/abstain escalation. Neither may be presented as having invented REM's four-action architecture | `CLAUDE.md` § MATHEMATICAL LOCK → Decision | **FROZEN** |
| Attribution | Linear Shapley attribution, **audit-only**, MUST NOT affect the verdict | `CLAUDE.md` § MATHEMATICAL LOCK → Attribution | **FROZEN** |
| Allow semantics | Release the current action | `CLAUDE.md` § MITIGATION LOCK | **FROZEN** |
| Modify semantics | Apply ONE declared modification mechanism to the current action or execution context | `CLAUDE.md` § MITIGATION LOCK | **FROZEN** |
| Escalate semantics | Withhold the current action pending review | `CLAUDE.md` § MITIGATION LOCK | **FROZEN** |
| Block semantics | Prevent execution of the current proposed action (step-level, **not** episode-level) | `CLAUDE.md` § MITIGATION LOCK | **FROZEN** |
| Operating-point threshold policy | BASELINE ONLY — not a second primary methodology | `CLAUDE.md` § FROZEN REM PIPELINE | **FROZEN** |
| CUSUM | OPTIONAL and OBSERVE-ONLY; must not enter the core verdict path | `CLAUDE.md` § FROZEN REM PIPELINE | **FROZEN** |
| Fail-closed requirement | Missing design input → `DesignNotSpecifiedError` or equivalent; no guessed defaults | `CLAUDE.md` § IMPLEMENTATION FAIL-CLOSED REQUIREMENT | **FROZEN** |

## 2. FROZEN AS EXCLUDED — must not be reintroduced

| Item | Status |
| ---- | ------ |
| `risk = p × S` as an NIST-defined equation | **FROZEN-OUT** |
| `confidence = Σ|β_i|` | **FROZEN-OUT** |
| Persistence variable ρ | **FROZEN-OUT** |
| Invented composite risk equations | **FROZEN-OUT** |
| Risk-based CUSUM; CUSUM in the core verdict path | **FROZEN-OUT** |
| SPRT as a required methodology | **FROZEN-OUT** |
| Hand-picked risk thresholds as the primary decision mechanism | **FROZEN-OUT** |
| LLM-based decision arbitration | **FROZEN-OUT** |
| GRU/LSTM/Transformer trajectory model | **FROZEN-OUT** |
| Counterfactual prefix-branching controller | **FROZEN-OUT** |
| Beta / isotonic / temperature calibration as the adopted calibrator | **FROZEN-OUT** |
| SHAP as a decision input | **FROZEN-OUT** |
| CARE-EL as the official algorithm name | **FROZEN-OUT** (unless explicitly approved) |
| Three independent methodologies A1/A2/A3 | **FROZEN-OUT** |

## 3. CONFLICT — existing code violates the contract

These are defects in commit `0a7a803`, introduced before `CLAUDE.md` was
available. Each must be corrected.

| # | Item | Current value | Conflicting rule | Status |
| - | ---- | ------------- | ---------------- | ------ |
| C1 | Provisional equation IDs `EQ-MET-01`…`EQ-STAT-02` used in `@equation(...)` inside implementation code | 9 fabricated identifiers | `CLAUDE.md` § EQUATION-ID LOCK: *"Do not create provisional equation IDs inside implementation code"* | **CONFLICT** |
| C2 | `docs/equation_registry.yaml` shipping 9 invented IDs marked `provisional` | invented registry | § EQUATION-ID LOCK: *"If the authoritative registry is unavailable: STOP"* | **CONFLICT** |
| C3 | `MATHEMATICAL_TRACEABILITY.md` reporting `VERIFIED 9 / UNVERIFIED 0` | report appears complete | § EQUATION-ID LOCK: *"Do not make generated traceability reports appear complete by inventing identifiers"* | **CONFLICT** |
| C4 | Feedback layer: `FeedbackSink`, `InMemoryFeedbackSink`, `Component.FEEDBACK`, feedback ablation | 8-component architecture | § FROZEN ARCHITECTURE: *"There is NO feedback-loop layer"* | **CONFLICT** |
| C5 | Mitigation mechanism `REDUCE_PRIVILEGE` (sets episode flag) | episode-level | § MITIGATION LOCK: *"Any episode-level restriction is a separate experimental policy requiring explicit specification"* | **CONFLICT** |
| C6 | Mitigation mechanism `TERMINATE_EXECUTION` (ends episode) | episode-level | § MITIGATION LOCK, as C5 | **CONFLICT** |
| C7 | Mitigation mechanism `RESTRICT_TOOL` (tool-class withholding) | tool-class | § MITIGATION LOCK: *"Do NOT silently redefine Modify as removing a tool class for the rest of the episode"* | **CONFLICT** |
| C8 | Free verdict→mechanism policy mapping in `configs/mitigation.yaml` | arbitrary mapping | § MITIGATION LOCK fixes canonical semantics per verdict | **CONFLICT** |

### Resolution applied

| # | Resolution |
| - | ---------- |
| C1 | All `EQ-*` identifiers removed from code. Operations now carry a **citation only**, with registry ID recorded as `NOT_ASSIGNED`. |
| C2 | `docs/equation_registry.yaml` deleted. The loader now refuses to synthesise a registry; supplying the authoritative one is the only way to obtain IDs. |
| C3 | Generator rewritten: reports `AUTHORITATIVE IDs: 0` and lists every operation as `AWAITING REGISTRY ID`. It can no longer show a complete traceability chain while the registry is absent. |
| C4 | Feedback layer removed entirely — sink, contract, pipeline stage, ablation option, tests. |
| C5–C7 | Episode-level and tool-class mechanisms removed from the runtime enumeration; retained only as an explicitly-unspecified experimental extension that raises if invoked. |
| C8 | Verdict→mechanism mapping replaced by the canonical semantics fixed in § MITIGATION LOCK. Only the *Modify* mechanism remains configurable, and it is unresolved. |

## 4. UNVERIFIED — blocked, must not be defaulted

Listed as unresolved by `CLAUDE.md` § DATA / EVALUATION LOCK unless explicitly frozen.

| Item | Why the implementation needs it | Status |
| ---- | ------------------------------- | ------ |
| Exact AgentDojo version / commit | Reproducibility; dataset identity | **UNVERIFIED** |
| Injection classifier | Produces the provenance/injection evidence feature | **UNVERIFIED** |
| Final feature set `x_t` | Input vector to ridge logistic regression | **UNVERIFIED** |
| Labeling of attacker-induced read operations | Defines the positive class for fitting and evaluation | **UNVERIFIED** |
| Consequence tiers `k_t` | Indexes the loss function `L(v, y, k_t)` | **UNVERIFIED** |
| Loss values / loss grid `L` | Without it the Bayes verdict cannot be computed | **UNVERIFIED** |
| Modify mechanism | The ONE declared modification the Modify verdict applies | **UNVERIFIED** |
| Grouping scheme | Determines valid statistical aggregation | **UNVERIFIED** |
| LLM backbones | Experimental configuration | **UNVERIFIED** |
| Number of repeats | Experimental configuration | **UNVERIFIED** |
| External benchmarks | Comparative evaluation | **UNVERIFIED** |
| Optional CUSUM scenarios | Observe-only analysis | **UNVERIFIED** |
| Ridge penalty λ | Required to fit the estimator; not frozen anywhere | **UNVERIFIED** |
| Policy predicates | Named in the frozen pipeline; contents never specified | **UNVERIFIED** |
| Provenance labeling rule | First stage of the frozen pipeline; rule never specified | **UNVERIFIED** |
| Authoritative equation IDs | Every equation's registry identifier | **UNVERIFIED** |

## 5. PD — proposed, not approved

| Item | Status |
| ---- | ------ |
| Research questions | **[PD]** — `CLAUDE.md` § RESEARCH-QUESTION LOCK: the proposal contains objectives, not necessarily current RQ wording; a derived RQ stays `[PD]` until explicitly frozen |
| Objective→RQ mapping | **[PD]** — proposal not supplied |

---

## DESIGN BLOCKED

### DESIGN BLOCKED

**Item:** Loss grid `L(v, y, k)` and consequence tiers `k_t`

**Why required:** The frozen decision rule is `R_t(v) = (1−p_t)L(v,0,k_t) + p_t L(v,1,k_t)` with `v* = argmin_v R_t(v)`. Without `L` and `k_t` no verdict can be produced. These are the only free quantities in the frozen decision layer, so any value chosen here silently *is* REM's decision policy.

**Current source status:** Explicitly listed as unresolved in `CLAUDE.md` § DATA / EVALUATION LOCK. Stage 2 report not supplied.

**Safe action:** STOP — do not choose a value.

**Supervisor decision needed:** YES

### DESIGN BLOCKED

**Item:** Final feature set `x_t`

**Why required:** `x_t` is the input to `s_t = β₀ + βᵀx_t`. Ridge logistic regression cannot be fitted or scored without it, and the feature definition determines what the coefficients mean.

**Current source status:** Listed as unresolved in § DATA / EVALUATION LOCK.

**Safe action:** STOP — do not choose a value.

**Supervisor decision needed:** YES

### DESIGN BLOCKED

**Item:** Ridge penalty λ

**Why required:** Ridge logistic regression is defined by its penalised objective; λ must be fixed or selected by a specified procedure before fitting. It is frozen neither in `CLAUDE.md` nor in any supplied document.

**Current source status:** Not mentioned in any supplied document.

**Safe action:** STOP — do not choose a value, and do not adopt a library default.

**Supervisor decision needed:** YES

### DESIGN BLOCKED

**Item:** Authoritative Equation-to-Source Registry

**Why required:** § EQUATION-ID LOCK forbids fabricating equation IDs and forbids provisional IDs in implementation code. Without the registry no operation can carry a verified identifier.

**Current source status:** Not supplied. Nine provisional IDs previously created in error have been removed (conflicts C1–C3).

**Safe action:** STOP — cite sources without identifiers; do not synthesise a registry.

**Supervisor decision needed:** NO — supplying the document resolves it.

### DESIGN BLOCKED

**Item:** Modify mechanism (the ONE declared modification)

**Why required:** § MITIGATION LOCK defines Modify as applying *one declared modification mechanism*. Which one is not declared anywhere.

**Current source status:** Listed as unresolved in § DATA / EVALUATION LOCK.

**Safe action:** STOP — the mitigation engine refuses to construct a modifier.

**Supervisor decision needed:** YES

### DESIGN BLOCKED

**Item:** Provenance labeling rule and policy predicates

**Why required:** Both are named stages of the frozen pipeline (`provenance labeling → …` and `… → policy predicates → …`) but neither is defined in any supplied document.

**Current source status:** Named in § FROZEN REM PIPELINE; contents never specified.

**Safe action:** STOP — implemented as fail-closed stages that raise when invoked.

**Supervisor decision needed:** YES

### DESIGN BLOCKED

**Item:** AgentDojo version / commit and the benchmark dataset

**Why required:** No fitting, calibration or evaluation is possible without data. § DATA / EVALUATION LOCK also warns that AgentDojo is an executable environment, not i.i.d. rows, so the grouping scheme is required before any statistic is reported.

**Current source status:** Listed as unresolved in § DATA / EVALUATION LOCK.

**Safe action:** STOP — do not invent sample counts or a version.

**Supervisor decision needed:** YES

---

## Implementation authorisation

Per `CLAUDE.md` § FINAL RULE (`FROZEN → IMPLEMENT EXACTLY`), the following may
now be implemented, each fail-closed on its UNVERIFIED inputs:

| Component | Authorised because |
| --------- | ------------------ |
| Ridge logistic regression scoring | Equation frozen in § MATHEMATICAL LOCK |
| Platt-on-logit calibration, with `γ₁ > 0` check | Equation frozen in § MATHEMATICAL LOCK |
| Expected-loss Bayes verdict | Equation frozen in § MATHEMATICAL LOCK |
| Linear Shapley attribution (audit-only) | Frozen in § MATHEMATICAL LOCK |
| Canonical mitigation semantics | Frozen in § MITIGATION LOCK |
| Five-layer architecture | Frozen in § FROZEN ARCHITECTURE |

Fitting procedures that require λ, the feature set, the loss grid or the
consequence tiers remain blocked and raise `DesignNotSpecifiedError`.
