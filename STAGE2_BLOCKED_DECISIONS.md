# STAGE 2 — BLOCKED DECISIONS

**Stage:** 2 (decision and verification — no code modified)
**Baseline commit:** `afc1137`
**Date:** 2026-09-19
**Classification vocabulary:** `CLAUDE.md` + Stage 2 brief §22 — FROZEN ·
SOURCE-VERIFIED · PD · SUPERVISOR DECISION REQUIRED · EXPERIMENTAL DECISION
REQUIRED · UNVERIFIED · CONFLICT

---

## SUMMARY

| | Count |
| - | ----- |
| Blocked items carried into Stage 2 | 9 (7 original + AgentDojo + calibration ablation) |
| **Fully resolved** | **0** |
| **Partially resolved** (constraints or candidates established) | **5** |
| Still fully blocked | 4 |
| Supervisor decisions required | 5 |
| Experimental decisions required | 5 |
| Newly-identified blocking dependencies | 2 |

> **No item moved from UNVERIFIED to FROZEN.** Stage 2 narrowed several items by
> establishing what literature *does* and *does not* constrain, but the
> decisions themselves remain with the supervisor or the evaluation protocol.

### Two dependencies discovered in Stage 2

```text
grouping scheme  ──gates──►  λ selection (ED-3)
                 ──gates──►  every interval / significance claim
                 ──gates──►  ablation power

project scope    ──gates──►  consequence tiers (SD-2)
(financial?)     ──gates──►  feature admissibility (SD-5)
                 ──gates──►  AgentDojo suite selection
```

Neither was visible before this stage. **The grouping scheme is the highest-
leverage unblock: it alone gates three downstream decisions.**

---

## BLOCKED ITEM 1 — LOSS FUNCTION `L(v,y,k)`

### DESIGN BLOCKED

**Item:** Numerical values of the loss function `L(v, y, k)`

**Why required:** The frozen decision rule is
`R_t(v) = (1−p_t)L(v,0,k_t) + p_t L(v,1,k_t)`, `v* = argmin_v R_t(v)`.
Without `L` no verdict can be computed. `L` is the only free quantity in the
frozen decision layer, so whatever values are chosen **are** REM's security
policy.

**Current source status:** Listed as unresolved in `CLAUDE.md`
§ DATA / EVALUATION LOCK. Stage 2 literature search found **constraints but no
values**.

**Safe action:** STOP — do not choose a value.

**Supervisor decision needed:** **YES**

### What Stage 2 established

**Literature supplies admissibility conditions.** Elkan (2001) states that for a
two-class cost matrix to be economically coherent:

```text
c(0,1) > c(1,1)     cost of a false negative  >  cost of a true positive
c(1,0) > c(0,0)     cost of a false positive  >  cost of a true negative
```

i.e. **correct outcomes must be strictly cheaper than incorrect ones**. Elkan
shows violating these yields matrices where one action is optimal regardless of
the data. Chow (1970) adds, for an abstain action, `C_c < C_r < C_e`.

**Classification (brief §6 options A–E):** not A · **partially B** (constraints
directly supported; values not) · not C alone · **D for the values** · E for
anything tier-indexed.

### Proposed generalisation — NOT literature-verified

For REM's four actions, per tier `k`, the analogous conditions would be:

```text
L(Allow,1,k) > L(Block,1,k)      allowing an attack costs more than blocking it
L(Block,0,k) > L(Allow,0,k)      blocking a benign action costs more than allowing it
Modify, Escalate strictly interior on both labels
```

> **This generalisation is REM-specific and is stated by no source.** It is
> offered for supervisor approval, not presented as verified. **Do not cite
> Elkan as its source.**

### Loss matrix structure (values withheld)

| Action `v` | `y=0` (benign) | `y=1` (attack) | consequence `k` | Source / status |
| ---------- | -------------: | -------------: | --------------- | --------------- |
| Allow | NOT YET SPECIFIED | NOT YET SPECIFIED | per tier | SUPERVISOR DECISION REQUIRED |
| Modify | NOT YET SPECIFIED | NOT YET SPECIFIED | per tier | SUPERVISOR DECISION REQUIRED |
| Escalate | NOT YET SPECIFIED | NOT YET SPECIFIED | per tier | SUPERVISOR DECISION REQUIRED |
| Block | NOT YET SPECIFIED | NOT YET SPECIFIED | per tier | SUPERVISOR DECISION REQUIRED |

### Warning — a loss grid can silently disable verdicts

With `k` fixed, each `R_t(v)` is **affine in `p_t`**:
`R_t(v) = L(v,0,k) + p_t·[L(v,1,k) − L(v,0,k)]`. The argmin of four affine
functions is their lower envelope, partitioning `[0,1]` into **at most** four
intervals. A verdict whose line never touches the envelope is **never selected**
— a grid can render Modify or Escalate unreachable without any error being
raised.

**Recommendation for Stage 3 (GREEN):** after the grid is set, report which
verdicts are reachable and at which `p_t` boundaries. This is a property of the
frozen rule, not a new design decision.

### Defect D1 — recorded, not fixed

`rem/algorithms/decision/expected_loss.py::LossGrid` validates completeness and
requires a `source`, but does **not** check Elkan's conditions. An incoherent
grid would be accepted. **Stage 3 GREEN** — implementable without knowing the
values.

**Status: Constraints SOURCE-VERIFIED · Values SUPERVISOR DECISION REQUIRED**

---

## BLOCKED ITEM 2 — CONSEQUENCE TIER `k_t`

### DESIGN BLOCKED

**Item:** Definition, count and boundaries of the consequence tiers `k_t`

**Why required:** `k_t` indexes `L(v, y, k_t)` — it states how much the outcome
matters at this step. It is what lets the same probability yield different
verdicts at different stakes, which is REM's substantive claim over a fixed
threshold.

**Current source status:** Listed as unresolved in `CLAUDE.md`. No project
document defines it. No literature definition is transferable.

**Safe action:** STOP — do not choose a value.

**Supervisor decision needed:** **YES**

### Candidate bases (none selected)

| Basis | Rationale | Label |
| ----- | --------- | ----- |
| Transaction amount / financial exposure | Direct monetary consequence | `[S]` — needs scope confirmation |
| Action reversibility | Irreversible actions carry higher consequence | `[L]` |
| Tool criticality / privilege (write vs read) | Privileged-sink notion from IFC literature | `[L]` |
| Data sensitivity of target | Credential/PII exposure | `[L]` |
| External reachability (egress) | Exfiltration relevance | `[L]` |

### Coupling warning

`|k|` multiplies the loss grid: **4 actions × 2 labels × |k| tiers**
supervisor-set numbers. Three tiers ⇒ 24 values. Feasibility (brief §21) argues
for a small count, but that judgement belongs to the supervisor.

**Status: SUPERVISOR DECISION REQUIRED** — gated on SD-5 (scope)

---

## BLOCKED ITEM 3 — FEATURE VECTOR `x_t`

### DESIGN BLOCKED

**Item:** The final feature set `x_t`

**Why required:** `x_t` is the input to `s_t = β₀ + βᵀx_t`. The estimator cannot
be fitted or scored without it, and the feature definitions determine what the
coefficients — and hence the Shapley attributions — mean.

**Current source status:** Listed as unresolved in `CLAUDE.md`. No project
document lists any feature.

**Safe action:** STOP — do not choose a value.

**Supervisor decision needed:** **YES** (final set), with `[L]` candidates below

### Candidates

| Feature | Layer | Purpose | Label |
| ------- | ----- | ------- | ----- |
| Untrusted-provenance content present in context | L1 | Indirect injection surface | `[L]` strong |
| Injection-classifier score on tool output | L1/L2 | Direct injection indicator | `[L]` strong — needs the unresolved classifier |
| Action is state-changing (write vs read) | L1 | Privileged-sink proxy | `[L]` strong |
| Argument value traceable to untrusted source | L1 | Tainted authority-bearing argument | `[L]` strong |
| External egress endpoint in arguments | L1 | Exfiltration indicator | `[L]` moderate |
| Tool-sequence deviation from stated goal | L3 | Goal drift | `[L]` moderate |
| Repeated / looping tool invocation | L3 | Persistence behaviour | `[L]` weak–moderate |
| Transaction amount | L1 | Financial exposure | `[S]` — **probably belongs in `k_t`** |

### Findings

1. **No feature qualifies as `[P]`** — nothing in the available project
   documents specifies any feature.
2. **Transaction amount is probably a tier, not a feature.** In `x_t` it asserts
   *evidence of attack*; in `k_t` it asserts *stakes*. The second is the more
   defensible claim. **Supervisor decision.**
3. **Rows 6–7 are the minimum that make L3 non-vacuous** — the frozen
   architecture requires a Behavioral Analysis layer but names no algorithm.
4. **Keep the set small** — both for feasibility (brief §21) and because the
   number of independent trajectory groups is limited.

**Status: Categories `[L]` · Exact set SUPERVISOR DECISION REQUIRED**

---

## BLOCKED ITEM 4 — RIDGE PENALTY λ

### DESIGN BLOCKED

**Item:** The ridge penalty λ

**Why required:** Ridge logistic regression is defined by its penalised
objective. λ must be fixed or estimated before the estimator can be fitted.

**Current source status:** Frozen nowhere. Absent from `CLAUDE.md` and every
available document. No source prescribes a value for REM's problem.

**Safe action:** STOP — do not choose a value, and do not adopt a library
default (e.g. scikit-learn `C=1.0`).

**Supervisor decision needed:** **NO for the value** (it is estimated) /
**YES for the protocol**

### Algorithm definition vs selection procedure

| Aspect | Status |
| ------ | ------ |
| **Algorithm definition** — L2-penalised logistic regression | **FROZEN** |
| **Selection procedure** — K-fold CV (K = 5 or 10) over a λ grid | **SOURCE-VERIFIED** as standard practice (ESL) |
| **Grid, criterion** | **PD** |
| **Resulting value** | **EXPERIMENTAL DECISION REQUIRED** |

### Blocking dependency discovered in Stage 2

> **λ cannot be selected by naive K-fold cross-validation.**
>
> `CLAUDE.md` states AgentDojo is an executable environment, not i.i.d. rows.
> Standard K-fold would place steps of the same task pairing in different folds,
> leaking within-trajectory correlation into the λ estimate and biasing it
> downward (too little regularisation).
>
> **Folds must respect the grouping scheme — which is itself unresolved.**
> λ is therefore blocked *transitively* on ED-2.

**Status: Procedure SOURCE-VERIFIED · Value EXPERIMENTAL DECISION REQUIRED,
gated on the grouping scheme**

---

## BLOCKED ITEM 5 — AUTHORITATIVE EQUATION REGISTRY

### DESIGN BLOCKED

**Item:** The authoritative Equation-to-Source Registry

**Why required:** `CLAUDE.md` § EQUATION-ID LOCK forbids fabricating equation
IDs and forbids provisional IDs in implementation code. Without the registry no
operation can carry a verified identifier, and the traceability chain stays open
at the Equation link.

**Current source status:**

```text
AUTHORITATIVE EQUATION REGISTRY: NOT FOUND
```

Searched: repository root, `docs/`, `configs/`, `rem/`, and the
`REM_EQUATION_REGISTRY` environment hook.

**Safe action:** STOP — cite sources without identifiers. **Not created during
Stage 2** (brief §10: do not create one unless an existing project document
instructs it; none does).

**Supervisor decision needed:** **NO** — authoring the registry resolves it

### Scale

**19 operations** require authoritative IDs — enumerated in
`STAGE2_EQUATION_TO_SOURCE_TRACEABILITY.md` §E. The enforcement machinery
already exists: passing `equation_id=` to `@derivation(...)` validates against
the registry and **raises if the registry is absent**, so an ID can never be
accepted on trust.

**Status: UNVERIFIED — registry absent**

---

## BLOCKED ITEM 6 — MODIFY MECHANISM

### DESIGN BLOCKED

**Item:** The ONE declared modification mechanism applied under the Modify verdict

**Why required:** `CLAUDE.md` § MITIGATION LOCK defines Modify as *"apply ONE
declared modification mechanism to the current action or execution context"*.
Which one is declared nowhere. Rewriting an agent action changes system
behaviour and may not be improvised.

**Current source status:** Listed as unresolved in `CLAUDE.md`. **No mechanism
is documented by the project.** All candidates below are literature-only.

**Safe action:** STOP — the mitigation engine refuses to construct a modifier.

**Supervisor decision needed:** **YES**

### Key disambiguation established in Stage 2

`CLAUDE.md` already assigns **Escalate = withhold pending review**. Therefore:

> **"Human confirmation" / "require approval" — the most commonly cited
> intervention in the agent-security literature — is REM's *Escalate*, not its
> *Modify*.** Selecting it for Modify would collapse two distinct verdicts.

This materially narrows the candidate set.

| Mechanism | Project-documented | In literature | Compatible with frozen REM |
| --------- | ------------------ | ------------- | -------------------------- |
| Argument sanitisation / redaction | ❌ | ✅ | ✅ step-level, single transform |
| Argument minimisation (strip unnecessary data) | ❌ | ✅ | ✅ step-level |
| Tool-output sanitisation | ❌ | ✅ | ⚠️ modifies *execution context*, permitted by the lock's wording but changes what Modify means |
| Parameter / transaction modification (e.g. cap an amount) | ❌ | ⚠️ weak | ⚠️ needs scope confirmation (SD-5) |
| Tool restriction | ❌ | ✅ | ❌ **excluded** — lock forbids redefining Modify as removing a tool class |
| Human confirmation | ❌ | ✅ | ❌ **excluded** — this is Escalate |

**Status: Candidate set narrowed · SUPERVISOR DECISION REQUIRED** — choose one
of rows 1–4

---

## BLOCKED ITEM 7 — PROVENANCE / POLICY PREDICATES

### DESIGN BLOCKED

**Item:** (a) the provenance labelling rule; (b) the policy predicates and
their semantics

**Why required:** Both are named stages of the frozen pipeline
(`provenance labeling → …` and `… → policy predicates → …`) but neither is
defined in any available document.

**Current source status:** Named in `CLAUDE.md` § FROZEN REM PIPELINE; contents
never specified.

**Safe action:** STOP — both are implemented as fail-closed stages that raise
when invoked.

**Supervisor decision needed:** **YES**

### (a) Provenance labelling — literature-supported at category level

Current agent-security literature converges on:

```text
system prompt      → trusted
user instruction   → untrusted content, authorised principal
retrieval context  → semi-trusted
tool output        → untrusted unless the tool is known-safe
```

`[L]` at the **category** level. This matches the `Provenance` enum already
present in `rem/agent/trajectory.py`, which defaults to `UNLABELLED` because the
rule is unspecified — correct fail-closed behaviour.

### (b) Minimum viable predicate set — proposed, not adopted

| Predicate | Purpose | Label |
| --------- | ------- | ----- |
| `argument_derived_from_untrusted_source` | Authority-bearing argument is tainted | `[L]` |
| `action_is_state_changing` | Distinguishes privileged sinks | `[L]` |
| `action_authorised_by_user_instruction` | Action traceable to the principal's request | `[L]` |

> Three predicates is a **proposal for approval**, not a finding. Brief §12 asks
> for the *minimum*, not a policy engine.

### Unresolved semantics — materially different systems

`CLAUDE.md` places policy predicates between tiering and the Bayes verdict but
never says what they do. Two coherent readings:

1. **Hard constraints** — a firing predicate removes actions from the argmin
   domain. REM becomes a hybrid of decision theory and policy enforcement.
2. **Evidence** — predicates are features in `x_t`, making the separate stage
   redundant. REM stays purely decision-theoretic.

**These imply different Chapter 3 framings.** The implementation currently
**refuses to proceed when a predicate fires with no policy defined**, which is
correct fail-closed behaviour under either reading.

**Status: UNVERIFIED · SUPERVISOR DECISION REQUIRED (SD-4)**

---

## BLOCKED ITEM A — AGENTDOJO VERSION AND GROUPING

### DESIGN BLOCKED

**Item:** (a) exact AgentDojo version/commit; (b) suite selection; (c) grouping
scheme

**Why required:** No fitting, calibration or evaluation is possible without
data. The grouping scheme additionally determines whether any statistic may be
reported at all.

**Current source status:** Listed as unresolved in `CLAUDE.md`. The repository
pins nothing — `configs/experiment.yaml: agentdojo_version =
REQUIRED_FROM_DESIGN`, and AgentDojo is not a dependency in `pyproject.toml`.

**Safe action:** STOP — do not invent sample counts or select a version.

**Supervisor decision needed:** **YES** for suite selection (tied to scope);
**EXPERIMENTAL** for version pinning

### Verified benchmark facts

| Fact | Value |
| ---- | ----- |
| Paper | Debenedetti et al., *AgentDojo*, NeurIPS 2024 D&B; arXiv:2406.13352 |
| Repository | `ethz-spylab/agentdojo` |
| Composition | **97 realistic tasks**, **629 security test cases**, 4 suites |
| Suites | **Banking**, Slack, Workspace, Travel |
| Releases | **36**: `0.1.0` (18 Jun 2024) → `0.1.35` (27 Oct 2025) |

> **Cross-version comparability warning.** The NeurIPS 2024 figures correspond
> to an early release. Comparing them against results from a 2025 release is
> **not defensible** without matching the version. Do not claim comparability.

### Grouping

Repeated runs of the same (user task × injection task) pairing are **not
independent observations**. Candidate units: task pairing · user task · suite.

**Until the grouping scheme is frozen:**

- no standard error, confidence interval or significance test may be reported;
- λ cannot be selected by CV (Item 4);
- the `REM − Calibration` ablation cannot be powered.

```text
AGENTDOJO VERSION = SUPERVISOR/EXPERIMENTAL DECISION REQUIRED
GROUPING SCHEME   = EXPERIMENTAL DECISION REQUIRED (gates three downstream items)
```

---

## BLOCKED ITEM B — `REM − CALIBRATION` ABLATION FORMULATION

### DESIGN BLOCKED

**Item:** Which experimental formulation of `REM − Calibration` is used

**Why required:** The frozen Bayes rule is defined on the calibrated `p_t`.
"Removing calibration" is therefore ambiguous, and the four readings measure
different things.

**Current source status:** Not addressed by any project document.

**Safe action:** STOP — do not assume a formulation.

**Supervisor decision needed:** **EXPERIMENTAL DESIGN DECISION REQUIRED**

### The four formulations

| | Formulation | Assessment |
| - | ----------- | ---------- |
| **A** | Remove calibration entirely | **Ill-defined** — leaves the decision rule without an input. Not an ablation but a different system |
| **B** | Substitute uncalibrated `p̃_t` for `p_t` | **Well-defined.** Single controlled intervention; isolates calibration's contribution to *verdict quality* |
| **C** | Change the decision input more broadly | **Confounded** — alters the decision layer as well |
| **D** | Measure calibration independently (Brier/log-loss on `p̃` vs `p`) | **Well-defined but a different question** — measures *intrinsic* calibration quality, not its effect on verdicts |

**Observation, not a decision:** B and D are complementary — B gives the
end-to-end effect on verdicts, D the intrinsic improvement. A is incoherent; C
is confounded.

### Defect D2 — recorded, not fixed

`rem/core/pipeline.py` currently **raises** when calibration is ablated while the
decision layer is enabled. That reasoning is correct about **A**, but it also
**forecloses B**, the formulation most likely to be wanted.

> **Not changed in Stage 2.** If the supervisor selects B, Stage 3 must add an
> explicitly-named, explicitly-logged experimental path — never a silent
> fallback — so a run using `p̃` as `p` is unmistakable in the audit record.

**Status: EXPERIMENTAL DESIGN DECISION REQUIRED**

---

## ADDITIONAL ITEMS SURFACED BY STAGE 2

### Defect D3 — Platt fitting protocol

Platt (1999) fits the sigmoid on **cross-validated out-of-sample scores**
(3-fold); the implementation fits on a **single held-out validation split**.
Both are out-of-sample and defensible; CV yields a lower-variance `γ`, which
matters when the calibration split is small — likely here.
**Status: PD — protocol decision required. Code unchanged.**

### Scope confirmation

The Stage 2 brief titles the project *"Securing a **Financial** AI Agent"*.
`CLAUDE.md` contains **no scope statement** and never mentions finance. Not a
CONFLICT (the contract is silent, not contradictory), but it gates tiers,
features and suite selection.
**Status: UNVERIFIED — SUPERVISOR DECISION REQUIRED (SD-5)**

### Behavioural analysis (L3) has no algorithm

The frozen architecture requires the layer; no document names what it computes.
Forbidden: GRU/LSTM/Transformer trajectory models. CUSUM is observe-only.
**Status: UNVERIFIED — no candidate proposed here**

### Test-count discrepancy in the brief

The brief states "139 contract-compliance tests pass". Verified actual:
**154 total**, of which `test_contract_compliance.py` contributes **20**.

Audited in full (see BASELINE TEST-COUNT RECONCILIATION in the Stage 2 report).
139 is reproducible **exactly and uniquely** as the full suite minus
`tests/test_config.py` (15 tests) — i.e. a **full-suite** count from an
uncommitted working state, never a contract-compliance count. It is a *superset*
of the 43 frozen-math tests, which is why `43 + 139 = 182` exceeds 154 by
exactly 28 (`+43` double-counted, `−15` absent).

All three commits contain all eight test files and yield 154/154.

**Verdict: BASELINE COUNTS RECONCILED.** Category mislabel of a reproducible
number — no test-suite defect. **No code implication.**

### Operating-point baseline is not implementable

`CLAUDE.md` designates the threshold policy a BASELINE ONLY, but no
threshold-selection procedure is specified for it. A baseline with an invented
threshold would be exactly the "artificially weak baseline" a viva would
challenge.
**Status: UNVERIFIED — procedure required before the baseline can be built**

---

## DECISION REGISTER

| ID | Decision | Type | Gated on | Blocks |
| -- | -------- | ---- | -------- | ------ |
| **SD-1** | Loss grid values `L(v,y,k)` | SUPERVISOR | SD-2 | Every verdict and metric |
| **SD-2** | Consequence tiers `k_t` | SUPERVISOR | SD-5 | SD-1, loss-grid size |
| **SD-3** | Modify mechanism | SUPERVISOR | — | Modify verdict semantics |
| **SD-4** | Policy-predicate semantics | SUPERVISOR | — | Chapter 3 framing |
| **SD-5** | Project scope (financial?) | SUPERVISOR | — | SD-2, features, suites |
| **ED-1** | AgentDojo version + commit | EXPERIMENTAL | SD-5 | All runs |
| **ED-2** | Grouping scheme | EXPERIMENTAL | ED-1 | **ED-3, all inference, ablation power** |
| **ED-3** | λ via grouped K-fold CV | EXPERIMENTAL | ED-2 | Fitting |
| **ED-4** | `REM − Calibration` formulation | EXPERIMENTAL | SD-1 | Ablation |
| **ED-5** | Calibration protocol (D3) | PD | — | Calibration variance |
| **RG-1** | Author the equation registry | PROJECT ARTEFACT | — | Traceability closure |

### Recommended unblocking order

```text
SD-5 (scope)
  └─► SD-2 (tiers) ──► SD-1 (loss values) ──► ED-4 (ablation formulation)
  └─► ED-1 (version) ──► ED-2 (grouping) ──► ED-3 (λ)

Independent, can proceed in parallel:
  SD-3 (Modify)   SD-4 (predicates)   ED-5 (calibration protocol)   RG-1 (registry)
```

**SD-5 and ED-2 are the two highest-leverage decisions.** SD-5 unblocks the
tier/loss chain; ED-2 unblocks λ and every statistical claim.

---

## COMPLIANCE CHECK

- [x] No blocked item silently resolved
- [x] No loss value invented — matrix is `NOT YET SPECIFIED` throughout
- [x] No feature adopted — all labelled `[L]` / `[S]`
- [x] λ not chosen — procedure identified, value left open
- [x] No consequence tier chosen
- [x] No AgentDojo version chosen
- [x] No equation ID invented
- [x] No option selected on the supervisor's behalf
- [x] Literature support distinguished from project-specific proposal throughout
- [x] No code, test, equation or configuration modified
