# STAGE 2.5 — RESEARCH-GAP OPTIONS

**Date:** 2026-09-19 · **Analysis only — no code, test, config or chapter modified**

> Every prior-art statement here rests on **search-index corroboration only**;
> the egress policy blocked every scholarly domain. See
> `STAGE2_5_PRIOR_ART_RECONCILIATION.md` §0.

---

# 1. A–E CLAIM RECONCILIATION (§14)

| Clause | REM currently specifies | Verified prior art | Degree of overlap | Defensible status | Evidence |
| ------ | ----------------------- | ------------------ | ----------------- | ----------------- | -------- |
| **A** — calibrated probability from context + behavioral evidence | Ridge LR → Platt-on-logit, `γ₁>0`. Feature set **unresolved** | NEXUS: Platt-scaled logistic-regression risk score over a 9-dim plan vector incl. irreversibility, sensitivity, cost | **Substantial** — estimator family, calibration method and role all correspond | **Overlapping prior art** | SIV — arXiv:2607.19356 |
| **B** — consequence-tiered expected-loss over four actions | `R_t(v)=(1−p_t)L(v,0,k_t)+p_t L(v,1,k_t)`; `v*=argmin`. `L` and `k_t` **unresolved** | NEXUS: four-action *formal intervention policy*. AgentTrust: four-valued verdicts. Elkan (2001): expected-cost principle, 2 actions. Chow (1970): +1 reject action | **Substantial on the action set; unresolved on the derivation** — retrieval did not establish whether NEXUS's policy is expected-loss-derived | **Partially supported** — the tier-indexed four-action form is **[PD]**, and the comparison to NEXUS is **Unverified** | SIV — 2607.19356, 2605.04785, Elkan, Chow |
| **C** — sequential accumulation with stated ARL | **Nothing implemented.** `CLAUDE.md` bars CUSUM from the verdict path | Corll: CUSUM + peak over frozen per-event scores; **self-describes as a boundary result, not a deployable detector**; ARL not retrieved. Page (1954): ARL classically established | **Partial** — accumulation represented; the false-alarm criterion was not retrieved for Corll | **Conflict** — project contract and the proposed configuration disagree; REM specifies nothing here | SIV — 2606.20746; Page DOI 10.1093/biomet/41.1-2.100 |
| **D** — per-factor attribution | Linear Shapley, audit-only, implemented | Lundberg & Lee (2017): Linear SHAP closed form `φᵢ = βᵢ(xᵢ − E[xᵢ])` | **Exact** — for a linear model this reduces to coefficient × centred feature | **Overlapping prior art** | SIV — arXiv:1705.07874 |
| **E** — execution-grounded financial validation | Planned; benchmark, version, grouping **all unresolved** | FinHarness: inline end-to-end finance-agent harness, per-step tool risk, joint block-unauthorised / approve-legitimate framing. PIGuard: NotInject, 339 benign trigger-word samples for over-defense | **Substantial** | **Overlapping prior art** | SIV — 2605.27333; ACL `2025.acl-long.1468` |

## Reading

Two clauses (**A**, **D**) show substantial-to-exact overlap. **E** shows
substantial overlap. **B** is partially supported with its decisive comparison
unverified. **C** is in conflict and currently unimplemented.

> **An A–E conjunction is not supportable on the present evidence.** This is not
> a conclusion about REM's merit; it is a statement about what the retrieved
> literature already represents and what REM currently documents.

---

# 2. RESEARCH-GAP RECONCILIATION (§15)

## Assessment of options A–D

| Option | Assessment |
| ------ | ---------- |
| **A. Retain** the current gap | **Not supportable.** Three of five clauses overlap substantially with reviewed prior art |
| **B. Narrow** | **Viable**, but narrowing alone leaves the decisive NEXUS comparison unverified |
| **C. Reframe** | **Viable** — shift from "which mechanisms" to "how the intervention is derived and how it is evaluated" |
| **D. Split into smaller gaps** | **Viable** — the evaluation-separation question and the decision-derivation question are independent and can be argued separately |

**Reconciliation: a combination of B, C and D is indicated by the evidence.** No
single option is selected here; the three candidate formulations in §5 below
correspond to different combinations, and are **not ranked**.

## Test against the five criteria for a defensible gap

| Criterion | Status |
| --------- | ------ |
| 1. Matters to the research problem | ✅ Financial agents, irreversible actions — supported by FinHarness's motivation |
| 2. Not already fully addressed by reviewed prior art | ⚠️ **Cannot be established** for the decision-derivation question until NEXUS is read directly |
| 3. Can actually be evaluated by the thesis | ⚠️ Depends on ED-1 (benchmark), ED-2 (grouping), SD-1 (loss values) |
| 4. Does not depend on an invented equation | ✅ All REM equations trace to Elkan, Chow, Platt, Hoerl & Kennard, Lundberg & Lee |
| 5. Does not require a large new system | ✅ Current implementation is small and complete apart from unresolved inputs |

**Criteria 2 and 3 are not yet satisfied.** This is the substantive finding of
Stage 2.5.

---

# 3. CLAIMS REM MUST NOT MAKE (§16)

Each item is listed **only** because verified literature supports the exclusion.

| # | Claim REM must not make | Supporting evidence |
| - | ----------------------- | ------------------- |
| 1 | Generic runtime interception as a contribution | AgentTrust and NEXUS both intercept pre-execution |
| 2 | Generic use of logistic regression for agent risk | NEXUS uses a logistic-regression risk score |
| 3 | Generic Platt calibration as a contribution | NEXUS uses Platt scaling and reports selecting it over isotonic |
| 4 | Generic four-action intervention policy | NEXUS (allow/block/confirm/revise); AgentTrust (allow/warn/block/review) |
| 5 | Generic trajectory or multi-step risk awareness | DreamGuard (recurrent latent state); AgentTrust (RiskChain); NEXUS (session state); FinHarness (cross-turn drift) |
| 6 | Generic Shapley explanation as a contribution | Lundberg & Lee (2017); reduces to coefficient × centred feature for a linear model |
| 7 | Generic financial-agent security evaluation | FinHarness wraps a finance agent end-to-end |
| 8 | Over-defense / benign-suspicious evaluation as a REM contribution | **PIGuard (ACL 2025)** + NotInject (339 benign trigger-word samples) |
| 9 | The separation of prediction from control as REM's insight | *Calibration Is Not Control* makes exactly this argument |
| 10 | That calibration quality demonstrates control quality | Refuted by the same paper: recalibrating a scalar score improves prediction metrics but leaves control regret unchanged |
| 11 | That offline metrics identify closed-loop performance | *What Can Be Enforced?*: once blocking changes future proposals, static scores on ungated trajectories need not identify the closed-loop frontier |
| 12 | A lightweight or low-latency advantage | NEXUS reports sub-millisecond CPU latency; DreamGuard 25 ms. REM's planned extractor alone is ~19.3 ms/classification at 512 tokens on an A100 |
| 13 | That CUSUM-based sequential detection is established as needed for REM | Corll self-describes as a boundary result, not a deployable detector |
| 14 | Any "first", "novel", "unique", "no prior work" formulation | No such statement is supportable at the achieved verification tier |

---

# 4. CURRENTLY DEFENSIBLE REM CLAIMS (§17)

**Not a ranking.** Confidence is **evidentiary**, not a probability of novelty.

| # | Claim | Type | Confidence | Evidence / basis |
| - | ----- | ---- | ---------- | ---------------- |
| 1 | REM's runtime pipeline is fully specified and its frozen equations trace to named sources | Documented project design | **HIGH** | 19 operations, each with statement + citation; 154/154 tests |
| 2 | REM implements Platt-on-logit faithfully, including Platt's smoothed targets, with `γ₁ > 0` enforced | Literature-grounded methodology | **HIGH** | Targets verified verbatim against Platt (1999) |
| 3 | REM's Detection Layer emits evidence only and applies no decision threshold | Implementation contribution | **HIGH** | `label="unthresholded"`; no `>= 0.5` anywhere in `rem/` |
| 4 | REM fails closed on every unresolved design input rather than defaulting | Implementation contribution | **HIGH** | 19 unresolved parameters raise `DesignNotSpecifiedError`; test-enforced |
| 5 | REM records the full conditional-risk table, so the argmin is re-checkable from the audit trail | Implementation contribution | **HIGH** | `Decision.conditional_risk`; audit record |
| 6 | REM enforces that attribution cannot reach the decision layer | Implementation contribution | **HIGH** | Signature excludes it; engine rejects audit-only payloads; test-enforced |
| 7 | REM reports risk estimation, decision quality and mitigation effectiveness as three separate questions | Evaluation contribution | **MEDIUM** | Motivated by *Calibration Is Not Control*, which also **argues this** — so the separation is adopted, not originated |
| 8 | REM derives the verdict from a tier-indexed expected-loss minimisation rather than assigning it by rule or threshold | Potentially differentiating combination | **LOW** | **Requires reading NEXUS directly.** Retrieval did not establish whether NEXUS's "formal intervention policy" is expected-loss-derived |
| 9 | REM enforces directly, rather than re-injecting evidence for the agent to act on | Potentially differentiating combination | **LOW** | FinHarness appears to re-inject; not confirmed at primary-source tier |
| 10 | REM applies consequence tiering to a financial action space | Documented project design | **LOW** | `k_t` is **[PD]** and unresolved; NEXUS already carries sensitivity and cost features |

> **Items 8 and 9 are the only *potentially differentiating* entries, and both
> carry LOW evidentiary confidence** — each depends on a paper that could not be
> opened. Items 1–6 are solid but are **implementation and rigour claims**, not
> research-gap claims.

---

# 5. CANDIDATE GAP STATEMENTS (§18)

Three candidates. **Not ranked. No winner selected.**

---

## Candidate Gap 1 — Decision derivation

### Candidate Gap
The reviewed literature demonstrates runtime guards that estimate a calibrated
risk and then select among several interventions, but the reviewed material does
not establish whether any of them **derives** the intervention from an explicit
consequence-indexed expected-loss minimisation rather than assigning it by rule,
threshold or policy.

### Supporting prior art
NEXUS (calibrated LR + formal intervention policy); AgentTrust (four-valued
verdicts); Elkan (2001) and Chow (1970) for the principle at 2 and 3 actions.

### Missing capability identified
An explicit decision-theoretic derivation over four actions indexed by a
consequence tier, with the loss structure stated and its coherence checkable.

### Why this remains relevant
*Calibration Is Not Control* shows recalibrating a scalar score leaves control
regret unchanged, and reports that action-conditioned control yields
regime-dependent gains over scalar routing — which makes *how the action is
derived* a substantive question rather than a presentational one.

### What REM would evaluate
Q2 decision quality against a threshold-routing baseline characterised by the
Neyman-Pearson frontier (*What Can Be Enforced?*), holding the estimator and
calibration fixed.

### Risk of prior-art collision
**UNVERIFIED — potentially HIGH.** If NEXUS's intervention policy turns out to
be expected-loss-derived, this candidate collapses. **This must be checked
before the candidate is adopted.**

### Status
**Partially supported · Unverified**

---

## Candidate Gap 2 — Evaluation separation in a financial setting

### Candidate Gap
The reviewed literature demonstrates financial-agent security harnesses and
demonstrates, separately, that calibration quality does not imply control
quality; the reviewed material does not establish that these have been brought
together — i.e. that risk estimation, action selection and mitigation
effectiveness have been reported as three separately measured quantities on an
execution-grounded financial workload including a benign-but-suspicious set.

### Supporting prior art
FinHarness (execution-grounded financial evaluation, joint benign/attack
framing); *Calibration Is Not Control* (the separation argument); PIGuard +
NotInject (over-defense measurement instrument); *What Can Be Enforced?*
(closed-loop identifiability limit).

### Missing capability identified
A reported evaluation that keeps Q1, Q2 and Q3 distinct in the financial setting,
with over-defense measured explicitly.

### Why this remains relevant
Conflating the three is precisely the error *Calibration Is Not Control*
identifies, and over-defense is the failure mode PIGuard documents.

### What REM would evaluate
All three questions separately across the nine scenario categories, with
utility and latency reported alongside security.

### Risk of prior-art collision
**MEDIUM.** Each ingredient is represented in prior art; the claim is about
their conjunction in one evaluation. Conjunction claims are weaker but are
consistent with the instruction's stated position that the contribution is
integration and evaluation.

### Status
**Partially supported**

---

## Candidate Gap 3 — Sequential evidence with a stated false-alarm criterion

### Candidate Gap
The reviewed literature demonstrates temporal accumulation for slow-burn
injection and reports a boundary result; the reviewed material does not establish
a deployed agent-security sequential component operated under an explicitly
stated and evaluated false-alarm criterion.

### Supporting prior art
Corll (CUSUM + peak over frozen scores; self-described boundary result; ARL not
retrieved); Page (1954) (ARL classically established); DreamGuard (alternative
sequential treatment via a recurrent world model).

### Missing capability identified
A stated ARL₀ with measured detection delay, in an agent-security deployment.

### Why this remains relevant
Slow-burn attacks keep each step below threshold; without a false-alarm criterion
an accumulator's operating point is unstated.

### What REM would evaluate
Detection delay under a stated ARL₀ on scenario category 6 (repeated / goal-drift).

### Risk of prior-art collision
**MEDIUM**, but this is **not the binding constraint**.

### Status
> ⚠️ **CONFLICT — SUPERVISOR/PROJECT DECISION REQUIRED.**
> `CLAUDE.md` states CUSUM is observe-only and must not enter the core verdict
> path. A component that cannot affect outcomes cannot support this candidate.
> Stage 2.5 analysis also found that **REM's Group B features already carry
> sequential information without CUSUM**, so the evidence does not establish
> that REM requires a CUSUM component at all. **Not resolved here.**

---

# 6. CHAPTER 2 REQUIRED CHANGES (§23)

**No rewrite performed.** Changes identified only.

| # | Change | Reason |
| - | ------ | ------ |
| C2-1 | Weaken every statement implying REM originates runtime interception, calibrated LR, four-action policies, trajectory awareness, remediation, or financial evaluation | Ten HIGH-collision items in the register |
| C2-2 | **Add PIGuard (ACL 2025, `2025.acl-long.1468`) and NotInject** to the benchmarks/evaluation section | Corrects the Stage 3 omission; supplies over-defense prior art and an instrument |
| C2-3 | Replace all "owns" constructions with "demonstrates prior art for" | §2 |
| C2-4 | State that five of the six closest comparators are **2026 preprints, not peer-reviewed** | Material to how strongly the gap can be argued, in both directions |
| C2-5 | Add the NEXUS component comparison, marking the expected-loss question **unverified** | Prevents an unsupported distinction |
| C2-6 | Record NEXUS's **sub-millisecond CPU latency** alongside DreamGuard's 25 ms | Stage 3 cited only the weaker comparator |
| C2-7 | Remove any claim that *Calibration Is Not Control* supports a specific `k_t` formulation | Correction C-3 |
| C2-8 | Note that the paper's own method — **prefix branching** — is a forbidden reintroduction under `CLAUDE.md` | REM can adopt its critique, not its solution |
| C2-9 | Add the closed-loop identifiability limitation from *What Can Be Enforced?* | Bounds all offline claims |
| C2-10 | State the **verification ceiling**: primary sources were not accessible; all prior-art statements are search-index corroborated | Required for honesty about evidence quality |

---

# 7. CHAPTER 3 REQUIRED CHANGES (§23)

| # | Change | Reason |
| - | ------ | ------ |
| C3-1 | Mark `k_t` explicitly as **[PD] project-specific and unresolved**, not literature-derived | Correction C-3 |
| C3-2 | Attribute the expected-loss principle to Elkan (2001) and Chow (1970) while stating the **four-action tier-indexed form is stated by neither** | Adaptation must not read as original mathematics |
| C3-3 | Remove the proposed "CUSUM as an evidence feature in `x_t`" | Correction C-4; §6 forbids it |
| C3-4 | Mark the sequential component as **CONFLICT — unresolved**, not as a planned configuration | §6 |
| C3-5 | Present the feature groups as **candidates requiring supervisor approval**, distinguishing SOURCE-SUPPORTED from POLICY-DEFINED | No feature set is frozen |
| C3-6 | Qualify λ as an experimental hyperparameter whose selection is gated on the grouping scheme | Naive K-fold would leak within-trajectory correlation |
| C3-7 | State that the `REM − Calibration` ablation requires an explicit formulation, and that the current pipeline forecloses the substitution reading | Carried defect D2 |
| C3-8 | Add over-defense measurement with attribution to PIGuard, and evaluate NotInject as an instrument **[V]** | Correction; C2-2 |
| C3-9 | Narrow any latency claim to measured numbers on stated hardware, with no comparative framing | NEXUS's sub-ms figure makes comparison hazardous |
| C3-10 | State that offline Q1/Q2 results do not establish Q3 | Closed-loop identifiability |

---

# 8. OPEN DECISIONS

| ID | Decision | Type |
| -- | -------- | ---- |
| **V-1** | **Read NEXUS (arXiv:2607.19356) directly** and determine whether its intervention policy is expected-loss-derived | **Verification — gates Candidate Gap 1** |
| **V-2** | Read FinHarness directly to confirm the re-injection vs enforcement distinction | Verification |
| **V-3** | Read Corll directly to confirm whether any ARL is stated | Verification |
| **CONF-1** | Sequential component: whether REM includes one, and in what role | **SUPERVISOR — unresolved conflict** |
| **CONF-2** | Beta calibration vs the `CLAUDE.md` prohibition | SUPERVISOR |
| **CONF-3** | SHAP status: frozen audit-only vs optional | SUPERVISOR |
| **SD-1** | Loss grid values `L(v,y,k)` | SUPERVISOR |
| **SD-2** | Consequence tier definition `k_t` | SUPERVISOR |
| **SD-3** | Modify mechanism | SUPERVISOR |
| **SD-4** | Policy-predicate semantics | SUPERVISOR |
| **SD-FEAT** | Final feature set | SUPERVISOR |
| **ED-1** | Benchmark set and AgentDojo version pin | EXPERIMENTAL |
| **ED-2** | Grouping scheme | EXPERIMENTAL — gates ED-3 and all inference |
| **ED-3** | λ via grouped CV | EXPERIMENTAL |
| **ED-4** | `REM − Calibration` ablation formulation | EXPERIMENTAL |
| **ED-5** | Platt fitting protocol (single split vs CV) | PD |
| **V-4** | Whether NotInject is applicable to the agent setting | VALIDATION |
| **RG-1** | Author the equation registry | ARTEFACT |

---

# STAGE 2.5 EXECUTIVE SUMMARY

## Verified

All eight supplied arXiv identifiers resolve to the described works at
search-index tier. **PIGuard was located and is peer-reviewed** (ACL 2025,
`2025.acl-long.1468`). Page (1954) verified for CUSUM/ARL with DOI. Baseline
independently re-verified: **154 collected / 154 executed / 154 passed / 0
failed / 0 skipped / 0 xfailed.**

**Verification ceiling, stated plainly:** the egress policy blocks arxiv.org,
aclanthology.org, Semantic Scholar, Crossref, OpenAlex and doi.org. **No primary
source was opened.** Every prior-art statement is search-index corroborated and
falls below the tier §4 requires.

## Corrected

Six corrections to previous stage output:

1. **PIGuard "could not be confirmed" was wrong** — it is verified and peer-reviewed. My earlier search failed; the source exists.
2. **"Owns" language removed** throughout.
3. ***Calibration Is Not Control* was wrongly used to support a `k_t` formulation.** Withdrawn; reclassified **[PD]**.
4. **"CUSUM as an evidence feature in `x_t`" was an unauthorised compromise.** Withdrawn; reported as an unresolved conflict.
5. **Ranking language removed** ("strongest", "pivotal", "highest-leverage").
6. **Latency comparator was incomplete** — NEXUS reports sub-millisecond CPU latency, materially tighter than DreamGuard's 25 ms.

## Overlapping prior art

Substantial overlap on: non-invasive pre-execution interception; calibrated
logistic regression; Platt scaling; four-action intervention; trajectory
signals; remediation; financial-agent evaluation; over-defense evaluation;
attribution; and the prediction/control separation argument. **Ten of fourteen
examined claims carry HIGH collision risk.**

## Still potentially differentiating

Only two, **both at LOW evidentiary confidence**, and each dependent on a paper
that could not be opened:

- Deriving the verdict from a **tier-indexed expected-loss minimisation** rather
  than assigning it by rule or threshold — **requires reading NEXUS**.
- **Enforcing** rather than re-injecting evidence for the agent to act on —
  requires reading FinHarness.

Separately, REM's **implementation rigour** claims hold at HIGH confidence
(fail-closed behaviour, no decision threshold, re-checkable risk table,
attribution structurally unreachable from the decision layer). These are
engineering and reproducibility contributions, not research-gap claims.

## Must not claim

Fourteen items listed in §3, each supported by verified literature. Notably: no
"first/novel/unique" formulation is supportable at the achieved verification
tier, and no lightweight-latency advantage should be claimed.

## Open decisions

Three verification actions (**V-1 NEXUS is the binding one**), three unresolved
conflicts, five supervisor decisions, five experimental decisions, one artefact.

## Baseline

**154 / 154 passing**, composed of **43 frozen-math + 20 contract-compliance +
91 other**. The historical "139 contract-compliance" is corrected to **20**; 139
is reproducible and uniquely decomposable as the full suite minus
`test_config.py`, i.e. a full-suite count containing the 43, which is why
`43 + 139` exceeds 154 by exactly 28.

## Gate to Stage 3

### NOT READY — DECISIONS STILL REQUIRED

Three independent reasons, any one of which is sufficient:

1. **The decisive prior-art comparison is unverified.** Whether NEXUS derives
   its intervention policy from an expected-loss criterion determines whether
   REM's principal candidate distinction exists. Primary sources were
   unreachable here.
2. **An unresolved conflict governs a proposed component.** The sequential
   component cannot be specified while `CLAUDE.md` bars CUSUM from the verdict
   path, and analysis indicates REM's Group B features already carry sequential
   information — so it is not established that REM requires one.
3. **The decision layer cannot run.** `L(v,y,k)`, `k_t`, the feature set, λ, the
   Modify mechanism, the benchmark and the grouping scheme all remain
   unresolved.

Documentation was produced; **that is not grounds for a positive gate.**
