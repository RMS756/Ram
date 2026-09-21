# V-1 — NEXUS DIRECT VERIFICATION

**Task:** Resolve the outstanding V-1 question from Stage 2.5
**Target:** NEXUS — *Structured Runtime Safety for Tool-Using LLM Agents*, arXiv:2607.19356
**Date:** 2026-09-21
**Baseline:** `ffa8efc`, working tree clean, 154/154 passing
**Scope:** verification only. No redesign, no chapter edit, no code change.

---

## 1. Verification Status

### UNVERIFIED

> **V-1 remains unresolved because direct paper-level verification was unavailable.**

**Why.** The NEXUS paper could not be accessed from this environment. Every route
to the paper, its mirrors, and every scholarly index is blocked by the
organization's egress policy:

| Route | Result |
| ----- | ------ |
| `https://arxiv.org/abs/2607.19356` | blocked (no connection) |
| `https://arxiv.org/html/2607.19356` | blocked |
| `https://arxiv.org/pdf/…` (via WebFetch) | `EGRESS_BLOCKED` — *"Access to arxiv.org is blocked by the network egress proxy"* |
| `https://export.arxiv.org/abs/2607.19356` | blocked |
| `http://export.arxiv.org/api/query?id_list=2607.19356` | **403** from the proxy |
| `https://www.alphaxiv.org/abs/2607.19356` | blocked |
| `https://bytez.com/docs/arxiv/2607.19356/paper` | blocked |
| `https://pith.science/paper/2607.19356` | blocked |
| `https://huggingface.co/papers/2607.19356` | blocked |
| `https://api.semanticscholar.org/graph/v1/paper/arXiv:2607.19356` | blocked |
| `openreview.net`, `paperswithcode.com`, `emergentmind.com`, `awesomepapers.io` | blocked |

The proxy documentation states: *"The destination host is not allowed by your
organization's egress policy for this session. **Do not retry or route around it
— report the blocked host.**"* Probing stopped at that point; no circumvention
was attempted.

**Consequence.** Source-priority tiers 1–6 (publisher, PDF, author repository,
preprint, author page, scholarly index) are all unavailable. Only tier 7
(search-engine result) was reachable. Per the CRITICAL EVIDENCE RULE, tier-7
material **cannot** be used to answer the primary question.

---

## 2. Direct Evidence

### Evidence item E1 — paper access attempt

| Field | Value |
| ----- | ----- |
| Source | arxiv.org and nine mirrors/indices |
| Identifier | arXiv:2607.19356 |
| Evidence type | Access attempt |
| **Full paper accessed** | **NO** |
| Page/section | N/A |
| Interpretation | Paper-level verification is impossible in this environment |

### Evidence item E2 — search-index description of the intervention mechanism

| Field | Value |
| ----- | ----- |
| Source | Web search result text, retrieved 2026-09-21 |
| Identifier | Describing arXiv:2607.19356 |
| Evidence type | **TIER 7 — search-index/abstract-level only** |
| **Full paper accessed** | **NO** |
| Page/section | **Not available** |
| Retrieved text | *"the scorer-gated demotion step: when exactly one critical rule fires, the calibrated risk score decides between a hard block and a request for user confirmation. The learned, calibrated scalar risk score ρ(P) becomes useful not as a primary unsafe-plan detector but as an arbitration signal inside a formal intervention policy."* |
| Interpretation | **Suggestive but NOT determinative.** Describes the score arbitrating between two named actions after a rule fires. No loss function, utility function, or minimisation objective appears in the retrieved text. **This does not establish what the paper does or does not define elsewhere.** |

### Evidence item E3 — search-index description of components

| Field | Value |
| ----- | ----- |
| Source | Web search result text, retrieved 2026-09-21 and 2026-09-19 |
| Evidence type | **TIER 7** |
| **Full paper accessed** | **NO** |
| Retrieved text | *"NEXUS combines deterministic safety rules, argument-level inspection, and a calibrated logistic-regression risk score for graded escalation"*; four components — *"a deterministic rule set for explicit safety violations, an argument inspector for sensitive values and risky inputs, a calibrated learned risk scorer for graded escalation, and a session manager for cross-turn state"*; actions — *"allow, block, request confirmation, or request revision"* |
| Interpretation | Confirms at tier 7 that a calibrated LR score and a four-action policy exist. Says nothing determinative about the selection rule's formal basis |

### Evidence item E4 — reported results

| Field | Value |
| ----- | ----- |
| Evidence type | **TIER 7** |
| **Full paper accessed** | **NO** |
| Retrieved text | 128-instance synthetic benchmark; F1 0.949; 4-class intervention accuracy 0.6406; *"outperforming rule-only intervention selection by 27.3 percentage points"*; rule-blind NEXUS-Stress F1 0.881; *"sub-millisecond CPU latency"* |
| Interpretation | Contextual only; does not bear on the decision-rule question |

### Explicit terminology warning

The expansion **"Neural EXecution Utility and Safety"** contains the word
*Utility*. **This must not be read as evidence of a utility function.** It is an
acronym expansion. The CRITICAL EVIDENCE RULE prohibits assumptions based on
terminology, and this is precisely such a trap.

---

## 3. Does NEXUS Use Expected Loss?

### UNRESOLVED

**Evidence.** No retrieved material mentions expected loss, expected utility,
cost function, loss function, Bayes decision rule, cost-sensitive decision
theory, misclassification cost, or an optimisation objective in connection with
NEXUS's action selection. Searches specifically targeting those terms returned
no such content.

**Why this is not a "NO".** Absence of a term in tier-7 extracted material is
**not** evidence of its absence from the paper. Abstracts and index summaries
routinely omit formal machinery. A "NO" here would be exactly the inference the
CRITICAL EVIDENCE RULE forbids.

**What the evidence leans toward, stated with its tier.** E2 describes the
calibrated score as *"an arbitration signal inside a formal intervention
policy"* and as a *"scorer-gated demotion step"* deciding *"between a hard block
and a request for user confirmation"* when *"exactly one critical rule fires"*.
Read at face value, that describes **rule-triggered arbitration between two
specific actions**, not a minimisation over the full action set.

> ⚠️ **This lean favours REM's position, which is precisely why it must not be
> relied upon.** If NEXUS does not derive its policy from expected loss, REM's
> expected-loss derivation survives as potentially differentiating. Evidence
> that supports one's own claim, obtained at the weakest available tier,
> warrants more scrutiny than evidence that opposes it — not less. **It is
> recorded here as a lead for paper-level checking, not as a finding.**

---

## 4. Does NEXUS Define a Formal Intervention Policy?

### YES — at tier-7 confidence, for the existence of the policy; UNRESOLVED for its formal basis

The retrieved material consistently and repeatedly uses the phrase *"formal
intervention policy"*. That the policy exists and selects among four actions is
corroborated across multiple independent retrievals. **What "formal" denotes in
the paper is not established.**

### The four levels, kept distinct

| Level | NEXUS | Evidence tier | Note |
| ----- | ----- | ------------- | ---- |
| **A. Risk calibration** | **YES** | Tier 7, multiply corroborated | Platt scaling; reported as selected over isotonic for lowest ECE on a small calibration split |
| **B. Risk thresholding** | **Suggested, NOT established** | Tier 7 | *"graded escalation"*, *"scorer-gated demotion"* — wording consistent with banding or gating, but no threshold values or rule retrieved |
| **C. Action selection** | **YES** | Tier 7, multiply corroborated | Four actions: allow, block, request confirmation, request revision |
| **D. Formal loss/utility-based intervention** | **UNRESOLVED** | — | No retrieved material addresses this either way |

> **These four are not equivalent and must not be collapsed.** A system can
> exhibit A + B + C — calibrate a score, band it, and pick an action — without
> any D. Whether NEXUS exhibits D is the open question, and it is the only one
> that bears on REM's claim.

---

## 5. Comparison With REM

Factual comparison. **Neither system is ranked.**

| Element | NEXUS | REM | Evidence Status |
| ------- | ----- | --- | --------------- |
| Risk estimation | Logistic-regression risk score `ρ(P)` over plan features | Ridge (L2-penalised) logistic regression, `s_t = β₀ + βᵀx_t` | NEXUS: **tier 7**. REM: implemented, frozen |
| Calibration | Platt scaling | Platt on the logit, `γ₁ > 0` enforced | NEXUS: **tier 7**. REM: implemented, verified against Platt (1999) |
| Intervention actions | allow · block · request confirmation · request revision | Allow · Block · Escalate · Modify | NEXUS: **tier 7**. REM: frozen |
| Formal loss function | **NOT ESTABLISHED** | `L(v, y, k)` — declared; **values unresolved** | NEXUS: **UNVERIFIED**. REM: frozen form, unresolved values |
| Expected-loss derivation | **NOT ESTABLISHED** | `R_t(v) = (1−p_t)L(v,0,k_t) + p_t L(v,1,k_t)` | NEXUS: **UNVERIFIED**. REM: frozen, implemented |
| Action-selection rule | Described as a *"formal intervention policy"*; retrieved text indicates a scorer-gated demotion when one critical rule fires | `v*_t = argmin_v R_t(v)` over all four actions | NEXUS: **tier 7, mechanism not established**. REM: frozen, implemented |
| Runtime enforcement | Pre-execution, on a structured plan; sub-millisecond CPU latency reported | Pre-execution, per proposed action; latency not yet measured | NEXUS: **tier 7**. REM: implemented, unmeasured |
| Financial-agent specialisation | Not indicated in any retrieved material | Stated project scope | NEXUS: **not found**. REM: project design |

---

## 6. Impact on REM Novelty Claims

| # | Statement | Classification | Reason |
| - | --------- | -------------- | ------ |
| 1 | "REM derives the verdict from a tier-indexed expected-loss minimisation rather than assigning it by rule or threshold." | **UNRESOLVED** | The comparative half is unverifiable here. The claim about REM's own construction is true and implemented; the implied contrast with NEXUS is not established |
| 2 | "No reviewed system derives its intervention from an expected-loss criterion." | **WITHDRAW** | Unsupportable. Cannot be asserted without reading the papers; a universal negative over inaccessible sources |
| 3 | "REM's expected-loss derivation is potentially differentiating." | **MODIFY** | Retain only with the qualifier: *"the reviewed material does not establish whether NEXUS's formal intervention policy is derived from an expected-loss criterion; this requires paper-level verification."* Do not state the distinction as established |
| 4 | "REM uses calibrated logistic regression" as a contribution | **WITHDRAW** | Already withdrawn in Stage 2.5; E3 re-corroborates NEXUS's calibrated LR at tier 7 |
| 5 | "REM's four-action policy is differentiating" | **WITHDRAW** | Already withdrawn; NEXUS's four actions re-corroborated |
| 6 | "REM is lightweight / low-latency relative to prior work" | **WITHDRAW** | NEXUS reports sub-millisecond CPU latency (tier 7). REM's latency is unmeasured. No comparative claim is supportable |
| 7 | "REM applies consequence tiering `k_t` to a financial action space" | **RETAIN** as **[PD] project design, unresolved** | Unchanged by V-1. `k_t` remains undefined and supervisor-gated |
| 8 | REM's implementation-rigour claims (fail-closed, no decision threshold, re-checkable risk table, attribution unreachable from the decision layer) | **RETAIN** | Independent of NEXUS; verified in-repository |

**No replacement claim is proposed.** The instruction permits one only if
directly supported, and nothing here is directly supported.

---

## 7. V-1 Gate Decision

### NOT RESOLVED

**Direct evidence could not be obtained.** The NEXUS paper and every route to it
are blocked by the organization's egress policy for this session. Source tiers
1–6 were unavailable; only tier 7 was reachable, and the CRITICAL EVIDENCE RULE
prohibits answering the primary question from tier-7 material.

**No conclusion is manufactured.** In particular, the retrieved
*"scorer-gated demotion"* description is **not** treated as establishing that
NEXUS lacks an expected-loss formulation, even though it leans that way and
would favour REM.

### What would resolve V-1

A single action by someone with network access to arXiv:

1. Open `arxiv.org/abs/2607.19356` (or the PDF/HTML version).
2. Search the text for: *expected loss · expected utility · loss function ·
   utility function · cost-sensitive · Bayes decision · risk minimisation ·
   argmin · objective*.
3. Locate the section defining the intervention policy and record whether the
   action is selected by **minimising a loss/cost** or by **rule-plus-threshold
   arbitration**.
4. Record section number and a short verbatim quotation.

That single check converts V-1 from NOT RESOLVED to PASS or to a withdrawal of
REM claim #3 above.

### Until then

REM claim #3 must be stated with the qualifier in §6, and claim #2 must not
appear at all. The Stage 2.5 gate (**NOT READY — DECISIONS STILL REQUIRED**)
stands unchanged.

---

## File / Code Safety Confirmation

Verified immediately before writing this document:

| Check | Command | Result |
| ----- | ------- | ------ |
| `rem/` unchanged | `git diff HEAD --stat -- rem/` | **empty — unchanged** |
| Tests unchanged | `git diff HEAD --stat -- tests/` | **empty — unchanged** |
| Configuration unchanged | `git diff HEAD --stat -- configs/` | **empty — unchanged** |
| `CLAUDE.md` unchanged | `git diff HEAD --stat -- CLAUDE.md` | **empty — unchanged** |
| Working tree | `git status --porcelain` | **clean** (before this file was written) |
| Frozen formulations intact | `grep -c "statement=" rem/algorithms/*/*.py` | ridge_logistic 4 · platt 2 · expected_loss 2 · linear_shapley 2 — **unchanged** |
| Test suite | `pytest -o addopts=""` | **154 passed** |

- No Chapter 2 or Chapter 3 file exists in the repository, and none was created or modified.
- No frozen mathematical formulation was modified.
- **CUSUM was not reintroduced.** It remains an unresolved conflict per Stage 2.5; nothing in V-1 bears on it and nothing here settles it.
- *Calibration Is Not Control* was not used; prefix branching was not introduced.
- PIGuard was not revisited beyond the already-accepted correction.

**The only file created by this task is `V1_NEXUS_DIRECT_VERIFICATION.md`.**
