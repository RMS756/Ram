# STAGE 2 — FINAL ALGORITHM & MATHEMATICAL DECISION REPORT

## REM — Runtime Evaluation and Mitigation for Securing a Financial AI Agent

**Stage:** 2 (scientific reconciliation, literature verification, mathematical decision)
**Date:** 2026-09-19
**Baseline commit:** `afc1137` (protected — unmodified by this stage)
**Governing contract:** `CLAUDE.md` — REM Claude Code Hard Design Lock

---

## EXECUTIVE STATUS

### Current implementation state

The frozen mathematical core is implemented and under test. The working tree is
clean and **no source code, test, equation or configuration was modified during
Stage 2**.

| Measure | Brief states | **Actually verified** |
| ------- | ------------ | --------------------- |
| Total tests passing | 154 | **154** ✓ |
| Frozen-math tests | 43 | **43** ✓ |
| Contract-compliance tests | 139 | **20** ✗ |

> **Discrepancy noted, not corrected in code.** The brief's "139
> contract-compliance tests" does not match the repository: `154` is the whole
> suite, of which `tests/test_contract_compliance.py` contributes `20`. The
> figure 139 was the total suite size at an intermediate commit before
> `tests/test_config.py` (15 tests) was added. Per-file counts:
> `test_frozen_math` 43, `test_metrics` 25, `test_pipeline` 21,
> `test_contract_compliance` 20, `test_config` 15, `test_trajectory` 12,
> `test_mitigation` 9, `test_reproducibility` 9.

### Frozen mathematical components (implemented)

| Ref | Component | Formulation | Status |
| --- | --------- | ----------- | ------ |
| EQ-1 | Ridge logistic regression | `s_t = β₀ + βᵀx_t`, `p̃_t = σ(s_t)` | FROZEN, implemented |
| EQ-2 | Platt calibration on the logit | `p_t = σ(γ₁s_t + γ₀)`, `γ₁ > 0` | FROZEN, implemented |
| EQ-3 | Expected-loss Bayes decision | `R_t(v) = (1−p_t)L(v,0,k_t) + p_t L(v,1,k_t)`, `v* = argmin_v R_t(v)` | FROZEN, implemented |
| EQ-4 | Linear Shapley attribution | `φᵢ = βᵢ(xᵢ − E[xᵢ])` — audit-only | FROZEN, implemented |

*(EQ-1…EQ-4 are the Stage 2 brief's own reference labels for discussion. They
are **not** equation IDs. No authoritative registry exists — see Blocked Item 5.)*

### Should the current implementation remain unchanged?

**Yes — with three documented defects recorded for Stage 3.** None is fixed here.

- **D1.** `LossGrid` validates completeness but **does not enforce Elkan's
  reasonableness conditions**, so an economically incoherent loss matrix would
  be accepted. (§15.3)
- **D2.** The pipeline **refuses** the `REM − Calibration` ablation, which
  forecloses what is arguably the methodologically meaningful formulation of
  that experiment. (§16)
- **D3.** Platt's published protocol fits the sigmoid on **cross-validated
  out-of-sample scores**; the implementation fits on a **single held-out split**.
  Both are out-of-sample and defensible; they are not identical. (§14)

### Blocked decisions

**7 blocked items** carried in from Stage 1, plus AgentDojo version and the
calibration-ablation formulation. Stage 2 resolves **2 fully**, **3 partially**,
and leaves **4 requiring supervisor or experimental decision**. See
`STAGE2_BLOCKED_DECISIONS.md`.

### Immediate next step

Obtain **five supervisor decisions** (§32). Until then the Stage 3 gate is
RED for the decision layer, and no empirical result can be produced.

---

## 1. FILES FOUND AND MISSING

Reported exactly as required by the brief §3. **No file was assumed to exist.**

| # | Required reading | Status | Path |
| - | ---------------- | ------ | ---- |
| 1 | `CLAUDE.md` | ✅ **FOUND** | `/CLAUDE.md` |
| 2 | `RECONCILIATION.md` | ✅ **FOUND** | `/RECONCILIATION.md` |
| 3 | Chapter 2 (Literature Review) | ❌ **MISSING** | — |
| 4 | Chapter 3 (Methodology) | ❌ **MISSING** | — |
| 5 | REM algorithm-selection study | ❌ **MISSING** | — |
| 6 | Existing mathematical decision report | ❌ **MISSING** | — (this stage produces the first) |
| 7 | Equation registry | ❌ **MISSING** | — (deliberately absent; see Blocked Item 5) |
| 8 | Configuration files | ✅ **FOUND** | `configs/` — 7 files, 46 parameters |
| 9 | README / project documentation | ✅ **FOUND** | `README.md`, `docs/ARCHITECTURE.md`, `docs/EXPERIMENT_GUIDE.md`, `docs/MATHEMATICAL_TRACEABILITY.md` |
| 10 | Tests encoding the frozen contract | ✅ **FOUND** | `tests/` — 8 files, 154 tests |
| 11 | Decision ledger | ❌ **MISSING** | — |
| 12 | Research-memory / project-memory | ❌ **MISSING** | — |
| 13 | Reference database | ❌ **MISSING** | — |
| — | Guard package (supplied) | ✅ **FOUND** | `docs/guard/START_PROMPT.md`, `docs/guard/README.md` |

**Six of thirteen required documents are absent**, including both thesis
chapters and any prior algorithm-selection study. Every conclusion below that
would normally rest on Chapter 2 or Chapter 3 is therefore derived from
`CLAUDE.md` plus verified literature only, and is labelled accordingly.

### Scope observation — requires confirmation

The Stage 2 brief titles the project *"Securing a **Financial** AI Agent"*.
`CLAUDE.md` contains **no scope statement** and never mentions finance,
banking or transactions. The financial scope is material — it bears directly on
consequence tiers (Blocked Item 2), the feature set (Item 3) and AgentDojo suite
selection (§13).

**Status: UNVERIFIED** — not a CONFLICT (the contract is silent rather than
contradictory), but it must be frozen before tiers or features are defined.

---

## 2. SOURCE VERIFICATION

Per brief §18, no mathematical claim below rests on memory. Each source was
located during this stage. **Verification depth is stated honestly**: several
sources are confirmed to venue level but their exact page/equation numbers were
not re-checked against the primary PDF, and those are marked accordingly rather
than asserted.

| Source | Venue / identifier | Verified | Depth |
| ------ | ------------------ | -------- | ----- |
| Elkan, C. (2001). The Foundations of Cost-Sensitive Learning | IJCAI 2001, pp. 973–978. [ACM DL](https://dl.acm.org/doi/10.5555/1642194.1642224) | ✅ | Venue + content (expected-cost rule, reasonableness conditions, `p*` formula) |
| Chow, C. K. (1970). On Optimum Recognition Error and Reject Tradeoff | IEEE Trans. Inf. Theory **16**(1), 41–46. [DOI 10.1109/TIT.1970.1054406](https://dl.acm.org/doi/10.1109/TIT.1970.1054406) | ✅ | Venue + content (reject rule, cost-derived threshold) |
| Platt, J. C. (1999). Probabilistic Outputs for SVMs… | *Advances in Large Margin Classifiers*, MIT Press, pp. 61–74 | ✅ | Venue + content (sigmoid form, smoothed targets, out-of-sample fitting) |
| Lundberg, S. M. & Lee, S.-I. (2017). A Unified Approach… | NeurIPS 30, pp. 4765–4774. [arXiv:1705.07874](https://arxiv.org/pdf/1705.07874) | ✅ | Venue + content (Linear SHAP closed form) |
| Shapley, L. S. (1953). A Value for n-Person Games | *Contributions to the Theory of Games II*, Princeton UP, pp. 307–317 | ✅ | Venue only |
| Hoerl, A. E. & Kennard, R. W. (1970). Ridge Regression | *Technometrics* **12**(1), 55–67. [DOI 10.1080/00401706.1970.10488634](https://www.tandfonline.com/doi/abs/10.1080/00401706.1970.10488634) | ✅ | Venue + content (L2 penalty origin) |
| Hastie, Tibshirani & Friedman (2009). *ESL* (2nd ed.) | Springer | ⚠️ | Venue confirmed; **§ numbers cited in code (§3.4.1, §4.4, §4.4.1) NOT re-verified against the book** |
| Brier, G. W. (1950) | *Monthly Weather Review* **78**(1), 1–3 | ⚠️ | Venue confirmed; equation number not re-verified |
| Fawcett, T. (2006) | *Pattern Recognition Letters* **27**(8), 861–874 | ⚠️ | Venue confirmed; p. 862 not re-verified |
| van Rijsbergen, C. J. (1979). *Information Retrieval* (2nd ed.) | Butterworths | ⚠️ | Venue confirmed; ch. 7 not re-verified |
| Hyndman, R. J. & Fan, Y. (1996) | *The American Statistician* **50**(4), 361–365 | ⚠️ | Venue confirmed; Definition 7 / p. 363 not re-verified |
| Debenedetti, E. et al. (2024). AgentDojo | NeurIPS 2024 D&B. [arXiv:2406.13352](https://arxiv.org/abs/2406.13352) | ✅ | Venue + content (97 tasks, 629 security cases, 4 suites) |
| Guo, C. et al. (2017). On Calibration of Modern Neural Networks | ICML 2017 | ⚠️ | Referenced indirectly; used only for the ECE-is-not-proper point, which is independently attested |

> **ACTION REQUIRED (Stage 3):** the ⚠️ rows need page-level verification against
> the primary sources before the traceability chain can be called closed. They
> are cited correctly at venue level; the locators inside the code docstrings
> are the unverified part.

---

## 3. REQUIRED OUTPUT 2 — ALGORITHM DECISION TABLE

| Component | Mathematical role | Evidence | Status | Decision needed |
| --------- | ----------------- | -------- | ------ | --------------- |
| Ridge logistic regression | Estimate `P(attack \| x_t)` via linear score `s_t` | `CLAUDE.md` MATHEMATICAL LOCK; Hoerl & Kennard (1970) for L2 penalty; ESL for penalised logistic fitting | **FROZEN** | None on the estimator. λ is separate → Item 4 |
| Platt calibration on logit | Map `s_t` → calibrated `p_t` | `CLAUDE.md`; Platt (1999) | **FROZEN** | None on the method. Fitting protocol → D3 |
| Expected-loss Bayes decision | Select `v*` minimising conditional risk | `CLAUDE.md`; Elkan (2001) expected-cost principle; Chow (1970) reject/abstain | **FROZEN** (rule) / **SUPERVISOR DECISION REQUIRED** (loss values) | Items 1, 2 |
| Linear Shapley attribution | Explain `s_t` feature-wise, audit only | `CLAUDE.md`; Lundberg & Lee (2017) Linear SHAP; Shapley (1953) | **FROZEN** | Background mean `E[x]` → derived from Item 3 |
| Behavioral analysis (L3) | Contribute behavioural evidence to `x_t` | `CLAUDE.md` FROZEN ARCHITECTURE (layer exists) | **UNVERIFIED** | No algorithm is named anywhere. Item 3 |
| CUSUM | Observe-only change detection | `CLAUDE.md` (optional, observe-only, never in verdict path) | **FROZEN as excluded from verdict path** | Whether to run it at all → PD |
| Operating-point threshold policy | Baseline comparator only | `CLAUDE.md` ("BASELINE ONLY") | **FROZEN as baseline** | Threshold-selection procedure for the baseline is unspecified |

No algorithm is scored or ranked, per brief §24.

---

## 4. REQUIRED OUTPUT 3 — MATHEMATICAL TRACEABILITY TABLE

Full table in **`STAGE2_EQUATION_TO_SOURCE_TRACEABILITY.md`** (19 operations).
Summary:

| Equation / Operation | Current formulation | Source | Directly supported? | Project-specific? | Status |
| -------------------- | ------------------- | ------ | ------------------- | ----------------- | ------ |
| Linear score | `s_t = β₀ + βᵀx_t` | `CLAUDE.md`; standard logistic model | **Yes** | Frozen by project | FROZEN / AWAITING REGISTRY ID |
| Uncalibrated probability | `p̃_t = σ(s_t)` | `CLAUDE.md`; logistic link | **Yes** | Frozen by project | FROZEN / AWAITING REGISTRY ID |
| Ridge objective | `−Σ[y log p + (1−y)log(1−p)] + (λ/2)‖β‖²` | Hoerl & Kennard (1970); ESL | **Method supported**; the ½ scaling and unpenalised intercept are conventions | Implementation convention | SOURCE-VERIFIED (method) |
| Newton–Raphson / IRLS fit | `β ← β − H⁻¹g` | ESL §4.4.1 *(locator unverified)* | **Method supported** | Solver choice, not modelling | SOURCE-VERIFIED (method) |
| Platt calibration | `p_t = σ(γ₁s_t + γ₀)` | `CLAUDE.md`; Platt (1999) | **Yes** — note sign convention `γ₁ = −A` | REM re-parameterisation | FROZEN / AWAITING REGISTRY ID |
| Platt smoothed targets | `t⁺=(N⁺+1)/(N⁺+2)`, `t⁻=1/(N⁻+2)` | Platt (1999) | **Yes — verified verbatim** | No | SOURCE-VERIFIED |
| Conditional risk | `R_t(v) = (1−p_t)L(v,0,k_t) + p_t L(v,1,k_t)` | `CLAUDE.md`; Elkan (2001) | **Principle supported**; Elkan is over *classes*, REM over *4 actions* + tier `k` | **REM-specific extension** | FROZEN (rule) / AWAITING REGISTRY ID |
| Verdict | `v* = argmin_v R_t(v)` | `CLAUDE.md`; Elkan (2001) | **Principle supported** | REM-specific action set | FROZEN / AWAITING REGISTRY ID |
| Linear Shapley | `φᵢ = βᵢ(xᵢ − E[xᵢ])` | Lundberg & Lee (2017) | **Yes — verified** | No | SOURCE-VERIFIED |
| Shapley base value | `φ₀ = f(E[x])` | Lundberg & Lee (2017) | **Yes** | No | SOURCE-VERIFIED |
| Evaluation metrics (7) | precision, recall, FPR, FNR, F1, accuracy, Brier | van Rijsbergen (1979); Fawcett (2006); Brier (1950) | **Yes** *(locators unverified)* | No | SOURCE-VERIFIED |
| Descriptive statistics (2) | mean; quantile (H&F Def. 7) | Hyndman & Fan (1996) | **Yes** *(locator unverified)* | No | SOURCE-VERIFIED |

**Every row carries `AWAITING REGISTRY ID`.** No equation ID exists or was
invented.

### Critical distinction — REM-specific extension

`CLAUDE.md` states Elkan supports the *expected-cost decision principle* and that
neither Elkan nor Chow invented REM's four-action architecture. Stage 2
**confirms and sharpens this**:

- Elkan's formulation is over **class predictions** (2 actions), with
  `p* = (c(1,0)−c(0,0)) / ((c(1,0)−c(0,0)) + (c(0,1)−c(1,1)))`.
- Chow's formulation adds **one reject action**, with threshold
  `t = (C_r − C_c)/(C_e − C_c)` — i.e. the reject threshold is **derived from
  costs**, not chosen independently.
- REM uses **four actions indexed by a consequence tier** `k_t`.

> **Finding.** REM's `L(v, y, k)` is a *generalisation* of both. It is
> **not** stated in either source. The correct thesis claim is:
> *"Method supported; REM-specific formulation requires project-level
> justification."* Writing that REM's decision rule "is Elkan's" would
> overclaim.
>
> **Corollary that strengthens the design:** because Chow shows the abstain
> threshold is a consequence of the cost structure, REM's Escalate verdict
> emerging from `argmin` — rather than from a separate hand-set threshold — is
> the theoretically correct construction. This is a defensible point for the viva.

---

## 5. REQUIRED OUTPUT 4 — BLOCKED-ITEM RESOLUTION TABLE

| ID | Blocked item | Evidence found | Possible resolution | Status | Exact next action |
| -- | ------------ | -------------- | ------------------- | ------ | ----------------- |
| **1** | Loss function `L(v,y,k)` | Elkan (2001): expected-cost rule + **reasonableness conditions** `c(0,1)>c(1,1)`, `c(1,0)>c(0,0)`; Chow (1970): reject cost ordering `C_c < C_r < C_e` | Literature fixes **admissibility constraints**, never values. Values must be set by the project | **Constraints: SOURCE-VERIFIED**<br>**Values: SUPERVISOR DECISION REQUIRED** | Supervisor sets the 8 (or 4×2×\|k\|) entries; Stage 3 adds constraint validation (D1) |
| **2** | Consequence tier `k_t` | No project definition exists. Financial scope (unconfirmed) suggests transaction-value banding; AgentDojo Banking suite exists | Cannot be derived from literature — it is a domain policy choice | **SUPERVISOR DECISION REQUIRED** | Confirm financial scope, then define tier count + boundaries |
| **3** | Feature vector `x_t` | Provenance/taint literature supports trust-labelled evidence; no project feature list exists | Small, defensible set; labelled candidates in §7 | **PARTIALLY RESOLVED** — categories `[L]`, exact set `[S]` | Supervisor approves a small set from §7 |
| **4** | Ridge penalty λ | K-fold CV (K=5 or 10) is the **standard selection procedure** (ESL) | **Procedure** is source-verified; **value** must be estimated. **Blocked transitively** on grouping scheme | **Procedure: SOURCE-VERIFIED**<br>**Value: EXPERIMENTAL DECISION REQUIRED** | Fix grouping scheme first, then grouped K-fold CV on the training split |
| **5** | Equation registry | **Searched: NOT FOUND.** No registry in repository | Must be authored as a project artefact; Stage 2 forbidden from creating one | **UNVERIFIED — registry absent** | Supervisor/student authors it; 19 operations listed in the traceability doc |
| **6** | Modify mechanism | Literature offers argument sanitisation, argument minimisation, redaction, tool-output filtering, human confirmation | **Human confirmation is excluded** — it is already REM's *Escalate*. Narrows to argument-level transforms | **PARTIALLY RESOLVED** — candidate set narrowed; choice **SUPERVISOR DECISION REQUIRED** | Supervisor picks ONE from the narrowed list |
| **7** | Provenance / policy predicates | Taint-tracking consensus: system=trusted, user=untrusted-but-authorised, retrieval=semi-trusted, tool output=untrusted unless known-safe | Minimum viable predicate set is literature-supported at the *category* level | **PARTIALLY RESOLVED** — categories `[L]`, exact predicates `[S]` | Supervisor approves minimum predicate set |
| **A** | AgentDojo version | **36 releases** 0.1.0 (Jun 2024) → 0.1.35 (Oct 2025); repo `ethz-spylab/agentdojo`; NeurIPS paper ≠ latest release | Must pin an exact version + commit. Cross-version comparison **not** defensible | **EXPERIMENTAL DECISION REQUIRED** | Pin one version; record in `configs/experiment.yaml` and the manifest |
| **B** | `REM − Calibration` ablation | Bayes optimality depends on `p_t` being calibrated; four candidate formulations differ materially | Formulation B (substitute `p̃` for `p`) is the well-defined intervention; A leaves the rule undefined | **EXPERIMENTAL DESIGN DECISION REQUIRED** | Choose formulation; note current code forecloses B (defect D2) |

---

## 6. BLOCKED ITEM 1 — LOSS FUNCTION `L(v,y,k)`

### Classification required by brief §6

Of options A–E: **not A** (not explicitly frozen), **partially B** (constraints
are directly supported; values are not), **not C alone**, **D — supervisor
decision required** for the values, and **E** for anything tier-indexed.

### What literature *does* supply

Elkan (2001) gives the expected-cost decision rule — predict the class with
lowest expected cost — and, critically, **conditions a cost matrix must satisfy
to be economically coherent**:

```text
c(0,1) > c(1,1)      cost of a false negative exceeds cost of a true positive
c(1,0) > c(0,0)      cost of a false positive exceeds cost of a true negative
```

i.e. **diagonal (correct) entries must be strictly cheaper than off-diagonal
(incorrect) entries**. Elkan shows that violating these produces matrices where
it is optimal to predict one class regardless of the data.

Chow (1970) adds the ordering for an abstain action: `C_c < C_r < C_e` — reject
must cost more than a correct decision but less than an error, else the reject
option is never or always selected.

### What literature does **not** supply

**No numerical values.** Any loss values appearing in another study were chosen
for that study's domain and cost model, and per the brief must be recorded as
*"reported in literature"*, never *"selected for this thesis"*.

### Implication for REM's four actions

REM's `L(v,y,k)` has 4 actions × 2 labels × |k| tiers. Generalising the
conditions above, a minimum admissibility set for REM would require (for each
tier):

- `L(Allow,1,k) > L(Block,1,k)` — allowing an attack costs more than blocking it
- `L(Block,0,k) > L(Allow,0,k)` — blocking a benign action costs more than allowing it
- Escalate/Modify strictly between the extremes on both labels, else they are never selected

> **This generalisation is REM-specific and is NOT stated by Elkan or Chow.**
> It is offered as a *proposed* constraint set for supervisor approval, not as a
> verified result. **Do not cite Elkan as its source.**

**Defect D1:** `rem/algorithms/decision/expected_loss.py::LossGrid` validates
completeness and requires a `source`, but does **not** check these conditions.
An incoherent grid would be accepted silently. **Recorded, not fixed.**

### Loss matrix — Required Output 6

| Action `v` | `y=0` (benign) | `y=1` (attack) | consequence `k` | Source / status |
| ---------- | -------------: | -------------: | --------------- | --------------- |
| Allow | NOT YET SPECIFIED | NOT YET SPECIFIED | per tier | SUPERVISOR DECISION REQUIRED |
| Modify | NOT YET SPECIFIED | NOT YET SPECIFIED | per tier | SUPERVISOR DECISION REQUIRED |
| Escalate | NOT YET SPECIFIED | NOT YET SPECIFIED | per tier | SUPERVISOR DECISION REQUIRED |
| Block | NOT YET SPECIFIED | NOT YET SPECIFIED | per tier | SUPERVISOR DECISION REQUIRED |

**No numbers are inserted.** The structure alone is given, per brief §28.

---

## 7. BLOCKED ITEM 2 — CONSEQUENCE TIER `k_t`

`k_t` indexes the loss function, i.e. it states **how much the outcome matters
at this step**. No definition exists in any available project document.

Candidate bases, with honest labelling:

| Candidate basis | Rationale | Label | Note |
| --------------- | --------- | ----- | ---- |
| Transaction amount / financial exposure | Direct monetary consequence | `[S]` | Requires financial scope confirmation; AgentDojo Banking suite exposes transaction values |
| Action reversibility | Irreversible actions carry higher consequence | `[L]` | Broadly supported in agent-security literature as a risk axis |
| Tool criticality / privilege | Write/state-changing vs read-only | `[L]` | Aligns with taint-tracking "privileged sink" notion |
| Data sensitivity of the target | Exposure of credentials or PII | `[L]` | Supported as a risk axis |
| External reachability | Egress to an external endpoint | `[L]` | Directly relevant to exfiltration |

> **Not selected here.** Brief §7: *"Do not select any feature merely because it
> seems useful."* Tier count and boundaries are a **domain policy choice** and
> cannot be derived from literature.

**Status: SUPERVISOR DECISION REQUIRED.**

**Coupling warning:** `|k|` multiplies the loss grid size (4 × 2 × |k| entries).
Three tiers means 24 supervisor-set numbers. Feasibility argues for a **small**
tier count, but that judgement belongs to the supervisor.

---

## 8. BLOCKED ITEM 3 — FEATURE VECTOR `x_t`

### Required Output 5 — Feature decision table

Labels per brief §8: `[P]` prior research · `[L]` literature-supported candidate
· `[I]` implementation · `[S]` supervisor · `[PD]` project/design · `[V]` validation.

| Feature | REM layer | Security purpose | Literature support | Project support | Status |
| ------- | --------- | ---------------- | ------------------ | --------------- | ------ |
| Untrusted-provenance content present in context | L1 | Indirect injection arrives via tool output | `[L]` strong — taint-tracking consensus | None | **Candidate** |
| Injection-classifier score on tool output | L1/L2 | Direct injection indicator | `[L]` strong | Named unresolved in `CLAUDE.md` | **Candidate — needs Item "injection classifier"** |
| Action is state-changing (write vs read) | L1 | Privileged-sink proxy | `[L]` strong | None | **Candidate** |
| Argument value traceable to untrusted source | L1 | Authority-bearing argument tainted | `[L]` strong (argument-level provenance) | None | **Candidate** |
| External egress endpoint in arguments | L1 | Exfiltration indicator | `[L]` moderate | None | **Candidate** |
| Tool-sequence deviation from task goal | L3 | Goal drift | `[L]` moderate | L3 exists in frozen architecture | **Candidate** |
| Repeated / looping tool invocation | L3 | Loop or persistence behaviour | `[L]` weak–moderate | None | **Candidate** |
| Transaction amount | L1 | Financial exposure | `[S]` | Scope unconfirmed | **Held — may belong to `k_t` instead** |

### Findings

1. **No feature is `[P]`.** Nothing in the available project documents specifies
   any feature, so none can be labelled "directly supported by prior REM research".
2. **Transaction amount is probably a tier, not a feature.** Putting monetary
   exposure into `x_t` makes it evidence *that an attack is occurring*; putting
   it into `k_t` makes it *how much the outcome matters*. These are different
   claims and the second is more defensible. **Supervisor decision.**
3. **Feature-set size drives λ.** A small set is both a feasibility requirement
   (brief §21) and a statistical one, given the limited number of independent
   trajectory groups.
4. **The behavioural layer (L3) has no named algorithm** anywhere. The frozen
   architecture requires the layer to exist; what it computes is unspecified.
   Rows 6–7 above are the minimum that would make L3 non-vacuous.

**Status: categories `[L]`, exact set `[S]` — SUPERVISOR DECISION REQUIRED.**

---

## 9. BLOCKED ITEM 4 — RIDGE PENALTY λ

Answering brief §9's six questions directly:

| Question | Answer |
| -------- | ------ |
| 1. Is λ frozen anywhere? | **No.** Absent from `CLAUDE.md` and every available document |
| 2. Does a cited paper specify it? | **No.** Hoerl & Kennard (1970) introduce the penalty; no source prescribes a value for REM's problem |
| 3. Should it be selected by cross-validation? | **Yes — this is the standard procedure.** K-fold CV with K=5 or 10 (ESL) |
| 4. Is it an experimental hyperparameter? | **Yes** |
| 5. Does it require supervisor approval? | **The protocol does; the resulting number does not** |
| 6. Would a default be scientifically justified? | **No.** A library default (e.g. scikit-learn `C=1.0`) encodes an arbitrary penalty and must not be adopted |

### Algorithm definition vs hyperparameter-selection procedure

Brief §9 requires these be kept apart:

- **Algorithm definition** — ridge logistic regression, i.e. L2-penalised
  logistic regression. **FROZEN.**
- **Selection procedure** — grouped K-fold CV over a λ grid on the training
  split, selecting by a stated criterion. **SOURCE-VERIFIED as standard
  practice**, but the criterion and grid are PD.

### Blocking dependency — important

> **λ cannot be selected by naive K-fold CV.** `CLAUDE.md` states AgentDojo is an
> executable environment, not i.i.d. rows. Standard K-fold would split steps of
> the same task pairing across folds, leaking within-trajectory correlation into
> the λ estimate and biasing it.
>
> **λ is therefore blocked transitively on the grouping scheme.** Folds must
> respect trajectory/task-pairing groups. The grouping scheme must be frozen
> *before* λ can be estimated.

**Status: EXPERIMENTAL DECISION REQUIRED, gated on the grouping scheme.**

---

## 10. BLOCKED ITEM 5 — AUTHORITATIVE EQUATION REGISTRY

```text
AUTHORITATIVE EQUATION REGISTRY: NOT FOUND
```

Searched: repository root, `docs/`, `configs/`, `rem/`, and the
`REM_EQUATION_REGISTRY` environment hook. No registry file exists. The absence
is deliberate — `rem/traceability/registry.py` refuses to synthesise one, and
`tests/test_contract_compliance.py` asserts none is shipped.

**Not created during Stage 2** (brief §10: do not create one unless an existing
project document instructs it; none does).

**19 operations require authoritative IDs** — enumerated in
`STAGE2_EQUATION_TO_SOURCE_TRACEABILITY.md`. All are currently
`AWAITING REGISTRY ID`.

**Status: UNVERIFIED — registry absent.**

---

## 11. BLOCKED ITEM 6 — MODIFY MECHANISM

### Key disambiguation

`CLAUDE.md` MITIGATION LOCK already assigns:

- **Escalate** = withhold the current action **pending review**
- **Modify** = apply **ONE declared modification** to the current action or execution context

> **Therefore "human confirmation" / "require approval" — the most commonly
> cited intervention in the agent-security literature — is REM's *Escalate*, not
> its *Modify*.** Selecting it for Modify would collapse two distinct verdicts.
> This meaningfully narrows the candidate set.

### Candidates, classified per brief §11

| Mechanism | Documented by project | Found in literature | Compatible with frozen REM? |
| --------- | --------------------- | ------------------- | --------------------------- |
| Tool-call **argument sanitisation / redaction** | ❌ | ✅ (content sanitisers; type-specific redaction tokens) | ✅ Step-level, single transform |
| Tool-call **argument minimisation** (strip unnecessary data) | ❌ | ✅ (tool-input firewall / minimiser) | ✅ Step-level |
| **Tool-output sanitisation** (filter injected instructions before they re-enter context) | ❌ | ✅ (tool-output firewall / sanitiser) | ⚠️ Modifies *execution context* rather than the action — permitted by the lock's wording, but changes what Modify means |
| **Parameter/transaction modification** (e.g. cap an amount) | ❌ | ⚠️ weak | ⚠️ Requires financial scope confirmation |
| **Tool restriction** | ❌ | ✅ | ❌ **Excluded** — the lock explicitly forbids redefining Modify as removing a tool class |
| **Human confirmation** | ❌ | ✅ | ❌ **Excluded** — this is Escalate |

**No mechanism is documented by the project.** All candidates are literature-only.

**Status: SUPERVISOR DECISION REQUIRED** — pick exactly one from rows 1–4.

---

## 12. BLOCKED ITEM 7 — PROVENANCE / POLICY PREDICATES

### Provenance labelling

Current agent-security literature converges on a trust ordering:

```text
system prompt        → trusted
user instruction     → untrusted content, authorised principal
retrieval context    → semi-trusted
tool output          → untrusted unless the tool is known-safe
```

This is **`[L]` literature-supported at the category level** and matches the
`Provenance` enum already present in `rem/agent/trajectory.py`
(`SYSTEM`/`USER`/`TOOL_OUTPUT`/`MODEL`, defaulting to `UNLABELLED`). The
enum is representation only — **the labelling rule is not implemented**, which
is correct given it is unspecified.

### Minimum viable predicate set

Brief §12 asks for the **minimum** predicates, not a policy engine. Proposed
minimum (all `[S]` pending approval):

| Predicate | Purpose | Label |
| --------- | ------- | ----- |
| `argument_derived_from_untrusted_source` | Authority-bearing argument is tainted | `[L]` |
| `action_is_state_changing` | Distinguishes privileged sinks | `[L]` |
| `action_authorised_by_user_instruction` | Action traceable to the principal's request | `[L]` |

> **Not adopted.** Three predicates is a *proposal for approval*, not a finding.

**A design question the supervisor must settle:** `CLAUDE.md` places policy
predicates between tiering and the Bayes verdict but never says what they do.
Two coherent readings:
1. **Hard constraints** — a firing predicate removes actions from the argmin domain.
2. **Evidence** — predicates are features in `x_t`, not a separate stage.

Reading 2 would make the predicate stage redundant; reading 1 makes REM a hybrid
of decision theory and policy enforcement. **These are materially different
systems and the choice affects Chapter 3.** The implementation currently
**refuses to proceed when a predicate fires** with no policy defined — which is
the correct fail-closed behaviour under either reading.

**Status: UNVERIFIED — SUPERVISOR DECISION REQUIRED.**

---

## 13. AGENTDOJO VERSION AND GROUPING

| Question | Finding |
| -------- | ------- |
| 1. Which version is used/intended? | **Unspecified in every project document** |
| 2. Does the repo pin a version? | **No.** `configs/experiment.yaml: agentdojo_version = REQUIRED_FROM_DESIGN`; AgentDojo is not a dependency in `pyproject.toml` |
| 3. Does the thesis specify it? | **Unknown** — Chapters 2 and 3 are absent |
| 4. Relevant task categories? | Four suites: **Banking**, Slack, Workspace, Travel. Banking is the candidate for a financial-agent scope |
| 5. Evaluation population? | **Undefined** — depends on suite selection and the grouping scheme |
| 6. Comparable with previous studies? | **Not without pinning.** 36 releases exist, 0.1.0 (Jun 2024) → 0.1.35 (Oct 2025). The NeurIPS 2024 paper's reported figures correspond to an early release, not the latest |

Benchmark composition (verified): 97 realistic tasks, 629 security test cases,
4 suites, with designated injection points in tool responses.

> **Do not claim cross-version comparability.** Utility and attack-success
> figures from the paper are not directly comparable to figures produced by a
> 2025 release unless the version is matched.

```text
AGENTDOJO VERSION = SUPERVISOR/EXPERIMENTAL DECISION REQUIRED
```

### Grouping

Because tasks are executable scenarios, repeated runs of the same
(user task × injection task) pairing are **not independent**. The grouping
scheme must state the unit of independence — candidates: task pairing, user
task, or suite. Until frozen:

- no standard error, confidence interval or significance test may be reported;
- λ cannot be selected by CV (§9);
- the `REM − Calibration` ablation cannot be powered.

**Status: UNVERIFIED — blocks three downstream decisions.**

---

## 14. CALIBRATION ANALYSIS

Answering brief §14's seven questions:

| # | Question | Finding |
| - | -------- | ------- |
| 1 | Faithful to published Platt scaling? | **Yes, with one documented difference (D3).** Form and targets match |
| 2 | Is the smoothing convention correct? | **Yes — verified verbatim.** `t⁺=(N⁺+1)/(N⁺+2)`, `t⁻=1/(N⁻+2)` matches Platt (1999) exactly |
| 3 | Must the calibration set be separate from training? | **Yes.** Fitting on training scores reproduces the model's optimistic bias |
| 4 | Must calibration be out-of-sample? | **Yes.** Platt uses an out-of-sample model (3-fold CV) specifically to avoid overfitting the calibration set |
| 5–6 | Which metrics? | **Brier score and log loss are proper scoring rules; ECE is not.** ECE has trivial optima (e.g. predicting the base rate), so it must not be a primary metric. Report Brier (implemented) and optionally log loss; ECE only as a supplementary diagnostic, stating bin count and binning scheme |
| 7 | Training or evaluation? | **Both, in distinct roles.** Fitting `γ` is a training-time operation on held-out data; assessing calibration quality is evaluation |

### Sign convention — confirmed correct

Platt's published form is `P(y=1|f) = 1/(1 + exp(Af + B))`. REM's frozen form is
`p_t = σ(γ₁s_t + γ₀)`. These are equivalent with **`γ₁ = −A`**, and REM's
requirement `γ₁ > 0` corresponds to Platt's `A < 0`, i.e. monotone increasing in
the score. The implementation documents this and enforces `γ₁ > 0`. **No defect.**

### Defect D3 — recorded, not fixed

Platt fits the sigmoid on **cross-validated out-of-sample scores** (3-fold);
the implementation fits on a **single held-out validation split**. Both are
out-of-sample and both are defensible. The difference is that CV uses all
training data for calibration and yields a lower-variance `γ` estimate, which
matters when the calibration split is small — likely here, given the limited
number of independent trajectory groups.

**Status: PD — requires an explicit protocol decision. Do not change code in Stage 2.**

---

## 15. BAYES DECISION ANALYSIS

### 15.1 Verification against decision theory

| Property | Status |
| -------- | ------ |
| Probabilistic interpretation | ✅ `(1−p_t, p_t)` is a proper posterior over `y ∈ {0,1}` |
| Expected-risk formulation | ✅ `R_t(v)` is the expectation of `L(v, y, k_t)` under that posterior |
| Action selection | ✅ `argmin` over actions is the Bayes decision rule |
| Asymmetric costs | ✅ Supported by construction — `L` is unconstrained in shape |
| Calibration ↔ decision quality | ✅ Optimality requires `p_t` to be a true posterior; miscalibration makes the argmin systematically wrong |
| When does calibration matter? | Only when miscalibration crosses a decision boundary. Monotone recalibration changes verdicts **only** where it moves `p_t` across a boundary between argmin regions |
| Appropriate for security actions? | ✅ Provided losses are stated. The four-action space is a REM extension of the 2-action (Elkan) and 3-action (Chow) cases |

### 15.2 No forbidden substitution

Confirmed absent from the codebase: 0.5 thresholding, arbitrary risk score,
weighted heuristic, invented formula. Grep audit in §19.

### 15.3 Defect D1 — loss-matrix coherence unchecked

As set out in §6. `LossGrid` requires completeness and a source but not Elkan's
conditions. **Recorded for Stage 3.**

### 15.4 Structural note on the four-action partition

With `p_t ∈ [0,1]` and fixed `k`, each `R_t(v)` is **affine in `p_t`**:

```text
R_t(v) = L(v,0,k) + p_t · [ L(v,1,k) − L(v,0,k) ]
```

The argmin of four affine functions partitions `[0,1]` into at most four
intervals with boundaries at the pairwise intersections. Two consequences:

1. **Some verdicts may be unreachable** for a given loss grid — a verdict whose
   line lies above the lower envelope everywhere is never selected. A grid can
   silently disable Modify or Escalate entirely.
2. **The interval boundaries are the effective operating points.** They are
   *derived* from `L`, which is exactly why hand-setting thresholds is forbidden
   and why the loss grid must be supervisor-approved.

> This analysis is a **mathematical property of the frozen rule**, not a new
> design decision. It is recommended as a Chapter 3 verification step: after the
> loss grid is set, report which verdicts are reachable and at what `p_t`
> boundaries. Currently **not implemented** — Stage 3 candidate.

---

## 16. `REM − CALIBRATION` ABLATION

Four candidate formulations, assessed without presuming an answer:

| Formulation | Description | Assessment |
| ----------- | ----------- | ---------- |
| **A** | Remove calibration from the pipeline entirely | **Ill-defined.** The frozen decision rule requires `p_t`. Removing calibration leaves the rule without an input — this is not an ablation, it is a different system |
| **B** | Substitute uncalibrated `p̃_t` for `p_t` in the Bayes rule | **Well-defined.** A single controlled intervention; isolates the contribution of calibration to decision quality. Measures exactly what §15.1 predicts matters |
| **C** | Change the decision input more broadly (e.g. `s_t` + a re-derived rule) | **Confounded.** Changes the decision layer as well as calibration |
| **D** | Measure calibration as an independent component (Brier/log-loss on `p̃` vs `p`) | **Well-defined but different question.** Measures calibration quality directly, not its effect on verdicts |

**Observation (not a decision):** B and D answer different questions and are
complementary — B gives the *end-to-end* effect on verdicts, D gives the
*intrinsic* calibration improvement. A is incoherent; C is confounded.

### Defect D2 — recorded, not fixed

`rem/core/pipeline.py` currently **raises** when calibration is ablated while the
decision layer is enabled, with the message that this "is not a valid ablation
of the frozen design". That reasoning is right about **A** but it also
**forecloses B**, which is the formulation most likely to be wanted.

> **Do not change this in Stage 2.** If the supervisor selects formulation B,
> Stage 3 must add an explicitly-named, explicitly-logged experimental path —
> not a silent fallback — so that a run using `p̃` as `p` is unmistakable in the
> audit record.

```text
REM − CALIBRATION FORMULATION = EXPERIMENTAL DESIGN DECISION REQUIRED
```

---

## 17. ALGORITHM JUSTIFICATION

Per brief §17. Abbreviated where fields repeat.

### 17.1 Ridge Logistic Regression

- **Purpose** — estimate `P(attack | x_t)` as a linear score `s_t`.
- **Mathematical foundation** — L2-penalised logistic regression; runtime
  `s_t = β₀ + βᵀx_t`, `p̃_t = σ(s_t)`.
- **Authoritative source** — `CLAUDE.md` (frozen); Hoerl & Kennard (1970) for
  the L2 penalty; ESL for penalised logistic fitting *(locators unverified)*.
- **Why it fits REM** — yields a **logit**, which is exactly what Platt-on-logit
  consumes; linear in features, which makes Linear SHAP **exact** rather than
  approximate; low latency, suiting per-step runtime evaluation; interpretable
  coefficients for a thesis defence.
- **Input / Output** — `x_t ∈ ℝᵈ` / `s_t ∈ ℝ`, `p̃_t ∈ [0,1]`.
- **Assumptions** — log-odds approximately linear in features; fixed feature order.
- **Hyperparameters** — **λ (UNRESOLVED)**; solver tolerance and iteration cap
  are numerical, not scientific.
- **Training** — offline, on the training split. **Runtime** — one dot product.
- **Complexity** — fit `O(n d² + d³)` per Newton iteration; predict `O(d)`.
- **Security relevance** — coefficient signs are directly auditable, so a
  reviewer can check the model is not keying on a spurious feature.
- **Limitations** — cannot represent feature interactions; feature set unresolved.
- **Status: FROZEN** (estimator) / **EXPERIMENTAL** (λ).

### 17.2 Platt Calibration

- **Purpose** — map `s_t` to a calibrated probability usable in the Bayes rule.
- **Foundation** — `p_t = σ(γ₁s_t + γ₀)`; `γ` by MLE against smoothed targets.
- **Source** — `CLAUDE.md`; Platt (1999) — **verified including targets**.
- **Why it fits REM** — the Bayes rule's optimality depends on `p_t` being a
  genuine posterior; a two-parameter map is estimable from a small calibration
  split, which matters given limited independent groups.
- **Input / Output** — held-out `(s_i, y_i)` / `γ₀, γ₁`; runtime `s_t` → `p_t`.
- **Assumptions** — sigmoidal score→probability relationship; out-of-sample split.
- **Hyperparameters** — none beyond the fitting protocol (D3).
- **Complexity** — fit `O(n)` per iteration on 2 parameters; predict `O(1)`.
- **Limitations** — two parameters cannot correct non-sigmoidal miscalibration;
  isotonic would, but is a **forbidden reintroduction**.
- **Status: FROZEN**; fitting protocol **PD**.

### 17.3 Expected-Loss Bayes Decision

- **Purpose** — select `v* ∈ {Allow, Modify, Escalate, Block}`.
- **Foundation** — `R_t(v) = (1−p_t)L(v,0,k_t) + p_t L(v,1,k_t)`; `v* = argmin`.
- **Source** — `CLAUDE.md` (frozen); Elkan (2001) expected-cost principle;
  Chow (1970) reject/abstain. **Neither invented REM's four-action architecture.**
- **Why it fits REM** — security costs are inherently asymmetric and
  context-dependent; the tier index `k_t` lets the same probability produce
  different verdicts at different stakes, which a fixed threshold cannot express.
- **Input / Output** — `p_t`, `k_t`, `L` / verdict + full risk table.
- **Assumptions** — `p_t` calibrated; `L` complete **and coherent (unchecked, D1)**.
- **Hyperparameters** — the loss grid itself. **UNRESOLVED.**
- **Complexity** — `O(|V|) = O(4)`.
- **Limitations** — entirely determined by `L`; §15.4 shows a grid can silently
  render verdicts unreachable.
- **Status: FROZEN** (rule) / **SUPERVISOR DECISION REQUIRED** (`L`, `k`).

### 17.4 Linear Shapley Attribution

- **Purpose** — audit-only explanation of `s_t`.
- **Foundation** — `φᵢ = βᵢ(xᵢ − E[xᵢ])`, `φ₀ = f(E[x])`; local accuracy
  `f(x) = φ₀ + Σφᵢ`.
- **Source** — Lundberg & Lee (2017) Linear SHAP — **verified**; Shapley (1953).
- **Why it fits REM** — for a linear model the Shapley values are **exact and
  closed-form**, so explanation adds negligible latency and introduces no
  approximation error to defend.
- **Assumptions** — linearity (satisfied by construction); **feature
  independence** (unlikely to hold exactly — a stated limitation).
- **Complexity** — `O(d)`.
- **Limitations** — computed on the **logit scale**; additivity does not survive
  the sigmoid. Feature independence is an idealisation.
- **Status: FROZEN, AUDIT-ONLY.** Verified unreachable from the decision layer.

### 17.5 Sequential / Behavioural Component (L3)

- **Status: UNVERIFIED — no algorithm named in any available document.**
- The frozen architecture requires the layer; `CLAUDE.md` forbids GRU/LSTM/
  Transformer trajectory models and confines CUSUM to observe-only.
- The only frozen statement about its role is that the evidence stage covers
  *"context / behavioral / action evidence"* — i.e. L3 contributes to `x_t`.
- **No algorithm is proposed here.** Minimum candidate features in §8, rows 6–7.

---

## 18. REQUIRED OUTPUT 7 — FINAL ALGORITHM SPECIFICATION

Only frozen/verified components appear. Nothing is added.

```text
Input & Context (L1)
   provenance labeling                      [rule UNVERIFIED]
   context / behavioral / action evidence → x_t   [feature set UNVERIFIED]
        ↓
Behavioral Analysis (L3)
   contributes behavioural evidence to x_t  [algorithm UNVERIFIED]
   CUSUM, if used: OBSERVE-ONLY, never in the verdict path
        ↓
Detection (L2) — Ridge Logistic Regression          [FROZEN]
   s_t = β₀ + βᵀx_t
   p̃_t = σ(s_t)                            (uncalibrated — not usable as p_t)
        ↓
Calibration (cross-cutting) — Platt on the logit    [FROZEN]
   p_t = σ(γ₁s_t + γ₀),  γ₁ > 0
        ↓
Decision Engine (L4)                                 [rule FROZEN]
   consequence tier k_t                      [tiers UNVERIFIED]
   policy predicates                         [predicates UNVERIFIED]
   R_t(v) = (1−p_t)L(v,0,k_t) + p_t L(v,1,k_t)      [L UNVERIFIED]
   v*_t = argmin_v R_t(v)
        ↓
Mitigation (L5) — deterministic, step-level          [semantics FROZEN]
   Allow    → release the current action
   Modify   → ONE declared mechanism         [mechanism UNVERIFIED]
   Escalate → withhold pending review
   Block    → prevent execution of this action
        ↓
Audit record                                         [implemented]
   digests, evidence, s_t, p̃_t, p_t, k_t, full R_t(v) table,
   verdict, mitigation, Shapley attributions (audit-only)
```

Attribution is drawn after the verdict is final. There is no feedback layer.

---

## 19. NO-CODE-CHANGES VERIFICATION (brief §34)

- [x] **No source code modified** — `git status --porcelain` empty; HEAD `afc1137`
- [x] **No tests modified** — 154 pass, unchanged
- [x] **No equations changed**
- [x] **No configuration changed** — 7 files, 46 parameters, 27 FROZEN / 19 UNVERIFIED
- [x] **No new algorithm implemented**
- [x] **No provisional equation IDs created** — grep for `EQ-[A-Z]+-[0-9]+` across `rem/`, `scripts/`, `configs/`: **no matches**
- [x] **No frozen architecture changed** — five layers intact
- [x] **No feedback layer introduced** — `Layer.ALL` has no `feedback` member
- [x] **No arbitrary threshold introduced** — grep for `0.5` in `rem/` returns exactly two hits, both non-thresholds: `quantile(samples_ms, 0.50)` (a percentile level) and `0.5 * sum(...)` (the ½ in `(λ/2)‖β‖²`)

Only three new **documentation** files were created.

---

## 20. REQUIRED OUTPUT 8 — CHAPTER 2 IMPACT

Chapter 2 is **absent**, so these are requirements for when it is written or
supplied.

| # | Required update | Reason |
| - | --------------- | ------ |
| C2-1 | Add Elkan (2001) with the **reasonableness conditions**, not merely the expected-cost rule | The conditions are the citable constraint on REM's loss grid |
| C2-2 | Add Chow (1970) positioned as **conceptual support for abstain**, with the cost-derived threshold `t = (C_r−C_c)/(C_e−C_c)` | Shows Escalate-from-argmin is theoretically correct, not an improvisation |
| C2-3 | State explicitly that **no source specifies a four-action, tier-indexed loss** | Prevents overclaiming; this is REM's own extension |
| C2-4 | Add Platt (1999) **including smoothed targets and out-of-sample fitting** | Both are load-bearing methodological details |
| C2-5 | Add a calibration-metric subsection: **Brier/log loss are proper, ECE is not** | Justifies the metric choice and pre-empts a viva question |
| C2-6 | Add Lundberg & Lee (2017) **Linear SHAP**, stressing exactness for linear models | Justifies both attribution and the choice of a linear detector |
| C2-7 | Add AgentDojo (Debenedetti et al. 2024) with **97 tasks / 629 security cases / 4 suites**, and state the version-comparability caveat | Required before any comparison to published figures |
| C2-8 | Add the provenance / taint-tracking literature as the basis for trust-labelled evidence | Grounds the provenance stage and several candidate features |
| C2-9 | Revisit gap wording: position REM against **argument-level provenance and IFC defences**, which are the current comparators | The 2024–2026 literature has moved; a gap framed only against classifier defences may no longer hold |
| C2-10 | Add Hoerl & Kennard (1970) for the ridge penalty | Currently only ESL is cited in code |

> **C2-9 is the substantive one.** Recent work on execution provenance,
> argument-level trust contracts and information-flow control targets the same
> problem REM addresses. The gap statement should be checked against these
> before Chapter 2 is finalised.

---

## 21. REQUIRED OUTPUT 9 — CHAPTER 3 IMPACT

Chapter 3 is **absent**. Requirements for when written:

| # | Required content | Status |
| - | ---------------- | ------ |
| C3-1 | The four frozen equations, verbatim, with the `γ₁ = −A` sign note | Ready |
| C3-2 | Statement that `L(v,y,k)` is a **REM extension**, with Elkan/Chow as principle-level support only | Ready |
| C3-3 | Loss-matrix **coherence conditions** and confirmation the chosen grid satisfies them | Blocked on Item 1 |
| C3-4 | Consequence-tier definition and boundaries | Blocked on Item 2 |
| C3-5 | Feature table: name, layer, purpose, provenance, transformation | Blocked on Item 3 |
| C3-6 | λ selection protocol — **grouped** K-fold CV, grid, criterion | Blocked on Item 4 + grouping |
| C3-7 | Calibration protocol — split vs CV (D3), and the metric set | PD |
| C3-8 | Decision-rule section including the **reachability analysis** of §15.4 | Method ready; needs `L` |
| C3-9 | Modify mechanism, precisely specified | Blocked on Item 6 |
| C3-10 | Provenance rule + minimum predicate set, and which reading of "policy predicates" applies | Blocked on Item 7 |
| C3-11 | AgentDojo version, suite selection, grouping scheme, repeats | Blocked |
| C3-12 | Ablation protocol incl. the chosen `REM − Calibration` formulation | Blocked on Item B |
| C3-13 | Statistical reporting rules — no independence claims without the grouping scheme | Ready as a constraint |
| C3-14 | Evaluation metrics with definitions | Ready |

---

## 22. SUPERVISOR DECISIONS REQUIRED

Only decisions that **cannot** be resolved from authoritative sources.

### SD-1 — Loss grid values `L(v,y,k)`

- **Why unresolved** — literature supplies coherence *constraints* only; values
  encode institutional risk appetite.
- **Options** — (a) supervisor sets values directly; (b) derive from a stated
  monetary/impact model; (c) sensitivity analysis over a family of grids.
- **Evidence** — Elkan (2001) constrains; no source prescribes.
- **What changes** — every verdict, every security and utility metric, and
  which verdicts are reachable at all (§15.4). This is the single highest-impact
  open decision.

### SD-2 — Consequence tiers `k_t`

- **Why unresolved** — a domain policy choice; no project definition exists.
- **Options** — (a) no tiering (|k|=1); (b) 2–3 tiers by action reversibility /
  privilege; (c) tiers by financial exposure (needs SD-5).
- **Evidence** — reversibility and privilege are `[L]`; monetary banding is `[S]`.
- **What changes** — loss-grid size (4 × 2 × |k| supervisor-set numbers), Chapter 3
  methodology, and whether REM's stake-sensitivity claim is demonstrable at all.

### SD-3 — Modify mechanism

- **Why unresolved** — no project document names one; literature offers several.
- **Options** — argument sanitisation/redaction; argument minimisation;
  tool-output sanitisation. **Excluded:** human confirmation (= Escalate), tool
  restriction (forbidden by the lock).
- **Evidence** — all `[L]`; none project-documented.
- **What changes** — what Modify *is*, and hence whether Modify is ever the
  minimum-risk action.

### SD-4 — Policy-predicate semantics

- **Why unresolved** — the frozen pipeline names the stage without defining it.
- **Options** — (a) hard constraints restricting the argmin domain;
  (b) evidence folded into `x_t`, making the stage redundant; (c) audit-only.
- **Evidence** — categories `[L]`; the role is `[PD]`.
- **What changes** — whether REM is a pure decision-theoretic system or a hybrid
  with policy enforcement. Materially different Chapter 3 framing.

### SD-5 — Project scope confirmation

- **Why unresolved** — the Stage 2 brief says "Financial AI Agent"; `CLAUDE.md`
  is silent.
- **Options** — (a) financial/banking scope, AgentDojo Banking suite;
  (b) general agent scope, all four suites.
- **Evidence** — brief title only; no contract statement.
- **What changes** — tier basis (SD-2), feature admissibility, suite selection,
  and the external validity of every result.

*No option is selected on the supervisor's behalf.*

### Experimental decisions (not supervisor decisions)

| ID | Decision | Gate |
| -- | -------- | ---- |
| ED-1 | AgentDojo version + commit pin | Must precede any run |
| ED-2 | Grouping scheme | **Gates ED-3 and all inference** |
| ED-3 | λ via grouped K-fold CV | Gated on ED-2 |
| ED-4 | `REM − Calibration` formulation (A/B/C/D) | Gated on SD-1 |
| ED-5 | Calibration fitting protocol — single split vs CV (D3) | Independent |

---

## 23. STAGE 3 IMPLEMENTATION GATE

### 🟢 GREEN — ready for implementation

Scientifically and contractually resolved. **All are already implemented and
require no change.**

| Item | Note |
| ---- | ---- |
| Ridge logistic regression (runtime + fitting) | Frozen; awaits λ only |
| Platt-on-logit calibration incl. smoothed targets | Verified faithful to Platt (1999) |
| `γ₁ > 0` monotonicity enforcement | Frozen requirement, enforced |
| Expected-loss Bayes rule (structure) | Frozen; awaits `L` and `k` |
| Linear Shapley attribution, audit-only | Verified; unreachable from decision layer |
| Canonical step-level mitigation semantics | Frozen; awaits Modify mechanism |
| Five-layer architecture | Frozen; verified in tests |
| Evaluation metrics (confusion-matrix family, Brier) | Source-verified |
| Fail-closed behaviour throughout | Contract-required, verified |
| Audit record incl. full risk table | Implemented |

**Newly GREEN for Stage 3 work** (not yet implemented, now justified):

| Item | Justification |
| ---- | ------------- |
| **Loss-grid coherence validation (D1)** | Elkan's conditions are source-verified; the check is implementable *independently of the values* |
| **Verdict-reachability analysis (§15.4)** | A mathematical property of the frozen rule; adds no design decision |
| **Log loss alongside Brier** | Both are proper scoring rules; source-verified |
| **Page-level source verification** | Closes the ⚠️ rows in §2 |

### 🟡 YELLOW — needs explicit project/supervisor decision

Do not implement yet.

| Item | Blocking decision |
| ---- | ----------------- |
| Loss grid values | SD-1 |
| Consequence tiers | SD-2 |
| Modify mechanism | SD-3 |
| Policy predicates | SD-4 |
| Feature set `x_t` | SD-5 + Item 3 |
| Provenance labelling rule | SD-4 |
| λ value | ED-2 → ED-3 |
| AgentDojo version + suites | ED-1, SD-5 |
| Grouping scheme | ED-2 |
| `REM − Calibration` path (D2) | ED-4 |
| Calibration protocol (D3) | ED-5 |

### 🔴 RED — insufficient evidence / blocked

| Item | Reason |
| ---- | ------ |
| **Authoritative equation registry** | Does not exist. 19 operations `AWAITING REGISTRY ID`. Must be authored as a project artefact |
| **Behavioural analysis (L3) algorithm** | No algorithm named in any available document |
| **Injection classifier** | Named unresolved in `CLAUDE.md`; no candidate specified |
| **Labelling of attacker-induced reads** | Changes the positive class and every metric |
| **Chapter 2 / Chapter 3 alignment** | Both documents absent |
| **Any empirical result** | Requires SD-1, SD-2, ED-1, ED-2 minimum |
| **Baselines** | Operating-point baseline needs a threshold-selection procedure; none specified |

> **The current code must remain unchanged until this gate is resolved.**

---

## 24. SELF-AUDIT (brief §35)

| # | Question | Answer |
| - | -------- | ------ |
| 1 | Did I invent any equation? | **No** |
| 2 | Did I invent any parameter? | **No** |
| 3 | Did I invent any loss value? | **No** — matrix is `NOT YET SPECIFIED` throughout |
| 4 | Did I invent any feature? | **No** — candidates are labelled `[L]`/`[S]`, none adopted |
| 5 | Did I invent any Equation ID? | **No** — `AWAITING REGISTRY ID` everywhere; grep confirms none in code |
| 6 | Did I silently choose λ? | **No** — procedure identified, value left open and shown to be gated on grouping |
| 7 | Did I silently choose consequence tiers? | **No** — SD-2 |
| 8 | Did I silently choose an AgentDojo version? | **No** — versions enumerated, choice left open |
| 9 | Did I modify the frozen architecture? | **No** |
| 10 | Did I modify code? | **No** — verified clean, §19 |
| 11 | Did I introduce a 0.5 threshold? | **No** — grep audit in §19 |
| 12 | Did I allow Shapley to affect the decision? | **No** — verified unreachable |
| 13 | Did I introduce a feedback layer? | **No** |
| 14 | Did I confuse literature support with project-specific design? | **No** — §4 explicitly separates them; the four-action loss is marked REM-specific |
| 15 | Did I use an authoritative source for every mathematical claim? | **Partially — stated honestly.** All sources located this stage; several locators marked ⚠️ as needing page-level verification rather than asserted |

**One caveat is carried openly rather than resolved:** the ⚠️ rows in §2 are
verified at venue level but their in-code page/section locators were not
re-checked against primary PDFs. They are listed as a Stage 3 action rather than
presented as complete.

---

## 25. CONCLUSION

The frozen mathematical core is **faithful to its sources** and should remain
unchanged. Stage 2's substantive findings are:

1. **Literature constrains the loss matrix but cannot supply it.** Elkan's
   coherence conditions are citable and checkable; the values are irreducibly a
   supervisor decision.
2. **Escalate-from-argmin is theoretically correct.** Chow shows the abstain
   threshold is cost-derived, so deriving Escalate from the argmin rather than a
   hand-set threshold is the principled construction — a strong viva point.
3. **λ is gated on the grouping scheme**, not merely open. Naive K-fold CV would
   leak within-trajectory correlation.
4. **Modify's candidate set is narrower than it looks** — human confirmation is
   already Escalate, and tool restriction is forbidden.
5. **A loss grid can silently render verdicts unreachable** (§15.4). Reachability
   should be reported, not assumed.
6. **REM's four-action tier-indexed loss is a genuine extension**, stated by no
   source. Claiming it as Elkan's would be an overclaim; presenting it as REM's
   own adaptation is both honest and a contribution.

**The project is NOT ready for Stage 3 implementation of the decision layer.**
Five supervisor decisions and two gating experimental decisions are outstanding.
Four narrowly-scoped Stage 3 items are newly GREEN and may proceed once the gate
is formally opened.
