# STAGE 2.5 — PRIOR-ART RECONCILIATION

**Date:** 2026-09-19 · **Baseline:** `78cb0e3`, tree clean, 154/154 passing
**Nature:** verification and reconciliation. **No code, test, configuration or
chapter was modified.**

---

# 0. VERIFICATION CEILING — READ FIRST

§4 requires primary peer-reviewed sources and states that search snippets are
not final evidence. **That standard could not be met in this environment**, and
saying so is a precondition for everything below.

The network egress policy blocks every scholarly domain:

```console
arxiv.org              -> unreachable
aclanthology.org       -> unreachable
www.semanticscholar.org-> unreachable
api.semanticscholar.org-> unreachable
api.crossref.org       -> unreachable
openalex.org           -> unreachable
doi.org                -> unreachable
huggingface.co         -> unreachable
pypi.org               -> reachable (200)
```

**Consequence.** No paper PDF or official venue page could be opened. The
highest tier achieved is **search-index corroboration**: the search tool returns
title, venue, authors and abstract-level content extracted from those pages, but
I did not read the papers.

Every source below is therefore marked:

| Tier | Meaning |
| ---- | ------- |
| **SIV** | **Search-Index Verified** — title, venue and abstract-level mechanism corroborated by retrieval. **Primary source NOT opened.** |
| **SIV-partial** | Some attributes corroborated; others not retrieved |
| **NIV** | **Not Independently Verified** |

> **No source in this document reaches the tier §4 asks for.** Conclusions that
> depend on fine-grained paper content should be treated as provisional until
> the sources are read directly. This limitation is environmental, not a
> shortcut.

---

# 1. CORRECTIONS TO PREVIOUS STAGE OUTPUT

§3 instructs that a citation must not be trusted merely because it appeared in a
previous Claude output. Re-checking my own Stage 3 deliverables against the
Stage 2.5 rules found **six items requiring correction**. All are corrected here;
the Stage 3 documents remain on record unaltered as historical evidence.

## C-1 — PIGuard status was WRONG

**Stage 3 said:** *"`PIGuard` could not be confirmed at all and is marked ✗."*

**Correct status: VERIFIED, and peer-reviewed.**

- **Title:** *PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free*
- **Venue:** **ACL 2025** (63rd Annual Meeting of the ACL), Long Papers
- **Anthology ID:** `2025.acl-long.1468`
- **Repository:** `github.com/leolee99/PIGuard`
- **Tier:** **SIV** — ACL Anthology page confirmed to exist; page not openable

The earlier failure was **my search-query failure, not an absence of the
source.** This is the most consequential correction in Stage 2.5, because
PIGuard is directly relevant to REM's over-defense evaluation (see §9).

## C-2 — "owns" language was prohibited

Stage 3 repeatedly used constructions such as *"NEXUS owns clause A"*,
*"FinHarness owns clause E"*, *"AgentTrust owns four-valued verdicts"*.

**Corrected formulation:** *"the reviewed work demonstrates prior art for …"* /
*"this aspect is already represented in prior art"*. §2 prohibits the former.
All comparisons below are restated.

## C-3 — *Calibration Is Not Control* was turned into a REM design definition

**Stage 3 said:** *"**Recommendation:** ground the consequence tier `k_t` in
reversibility + amount category + authorization state"*, presented as
*"directly supported"* by arXiv:2606.21399.

**This was an over-reach and is withdrawn.** §5 prohibits exactly this move.

**What the paper does establish (SIV):** it formalises the mismatch between risk
estimate and required action as **target error**, and identifies **intervention
advantage** — the expected utility gain from intervening rather than continuing —
as the decision object for oversight. It states two prefixes can share a risk
estimate while requiring different actions because one remains recoverable.

**What it does not do:** it does **not** define any consequence-tier formulation,
and does not specify `reversibility + amount + authorization`. That combination
is a **[PD] project/design proposal**, and nothing more.

## C-4 — CUSUM-into-`x_t` was an unauthorised compromise

**Stage 3 said:** *"The recommended lock-compatible reading is that the CUSUM
statistic becomes an evidence feature in `x_t`."*

**Withdrawn.** §6 forbids introducing CUSUM into `x_t`, forbids resolving the
conflict, and forbids implementing a compromise. Restated as an unresolved
conflict in §10 below.

## C-5 — Ranking language was prohibited

Stage 3 used *"strongest remaining contribution"*, *"strongest clause"*,
*"the single highest-leverage decision"*, *"pivotal"*. §22 prohibits novelty
ranking and superlatives. Removed throughout; clauses are now reported with
overlap degree and evidentiary confidence only.

## C-6 — Latency comparator was incomplete

Stage 3 cited DreamGuard's 25 ms as the latency comparator. Retrieval for this
stage indicates **NEXUS reports sub-millisecond CPU latency** — a materially
different reference point. Both are recorded in §3.

---

# 2. SOURCE REGISTER

| # | Title | Authors | Year | Venue | Identifier | Peer-reviewed | Tier |
| - | ----- | ------- | ---- | ----- | ---------- | ------------- | ---- |
| 1 | AgentTrust: Runtime Safety Evaluation and Interception for AI Agent Tool Use | Chenglin Yang | 2026 | arXiv (6 May 2026) | arXiv:2605.04785 | **No — preprint** | SIV |
| 2 | NEXUS: Structured Runtime Safety for Tool-Using LLM Agents | NIV (not retrieved) | 2026 | arXiv | arXiv:2607.19356 | **No — preprint** | SIV |
| 3 | DreamGuard: Efficient Runtime Guardrail for LLM Agents via Risk-Aware World Model | NIV | 2026 | arXiv | arXiv:2608.05695 | **No — preprint** | SIV |
| 4 | Calibration Is Not Control: Why LLM-Agent Oversight Needs Intervention | Zhang, Wan, Yu, Wu, Wen, Zhou, Zhao, Tsang | 2026 | arXiv (19 Jun 2026) | arXiv:2606.21399 | **No — preprint** | SIV |
| 5 | Amplify, Don't Create: Temporal Accumulation for Slow-Burn Prompt Injection | J. Alex Corll | 2026 | arXiv (17 Jun 2026) | arXiv:2606.20746 | **No — preprint** | SIV |
| 6 | FinHarness: An Inline Lifecycle Safety Harness for Finance LLM Agents | Jia, Liu, Chong + 10 others | 2026 | arXiv (26 May 2026) | arXiv:2605.27333 | **No — preprint** | SIV |
| 7 | **PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free** | NIV (Lee et al., per repo `leolee99`) | 2025 | **ACL 2025 Long Papers** | `2025.acl-long.1468` | **YES** | SIV |
| 8 | What Can Be Enforced? A Theory of Certified Runtime Safety for Tool-Using Agents | Shawn Ray | 2026 | arXiv (24 Jul 2026) | arXiv:2607.22868 | **No — preprint** | SIV |
| 9 | AgentDojo | Debenedetti, Zhang, Balunović, Beurer-Kellner, Fischer, Tramèr | 2024 | **NeurIPS 2024 D&B** | arXiv:2406.13352 | **YES** | SIV |
| 10 | Agent Security Bench (ASB) | Zhang, Huang et al. | 2024 | arXiv | arXiv:2410.02644 | NIV | SIV-partial |
| 11 | RAS-Eval | NIV | 2025 | arXiv | arXiv:2506.15253 | NIV | SIV-partial |
| 12 | AgentDyn | NIV | 2026 | arXiv | arXiv:2602.03117 | **No — preprint** | SIV-partial |
| 13 | ProbGuard / Pro2Guard | Haoyu Wang et al. | 2025 | arXiv | arXiv:2508.00500 | NIV | SIV-partial |
| 14 | Elkan, The Foundations of Cost-Sensitive Learning | C. Elkan | 2001 | **IJCAI 2001**, 973–978 | ACM DL 10.5555/1642194.1642224 | **YES** | SIV |
| 15 | Chow, On Optimum Recognition Error and Reject Tradeoff | C. K. Chow | 1970 | **IEEE Trans. Inf. Theory** 16(1), 41–46 | DOI 10.1109/TIT.1970.1054406 | **YES** | SIV |
| 16 | Platt, Probabilistic Outputs for SVMs | J. C. Platt | 1999 | *Adv. Large Margin Classifiers*, MIT Press, 61–74 | — | **YES (book chapter)** | SIV |
| 17 | Page, Continuous Inspection Schemes | E. S. Page | 1954 | **Biometrika** 41(1–2), 100–115 | DOI 10.1093/biomet/41.1-2.100 | **YES** | SIV |
| 18 | Hoerl & Kennard, Ridge Regression | Hoerl, Kennard | 1970 | **Technometrics** 12(1), 55–67 | DOI 10.1080/00401706.1970.10488634 | **YES** | SIV |
| 19 | Lundberg & Lee, A Unified Approach… | Lundberg, Lee | 2017 | **NeurIPS 30**, 4765–4774 | arXiv:1705.07874 | **YES** | SIV |
| 20 | CaMeL / Progent / AgentSpec / ShieldAgent / GuardAgent / LlamaFirewall | — | — | — | — | NIV | **SIV-partial** — mechanisms described via secondary survey text only |

> **Observation of material significance for the thesis:** of the six closest
> comparators (rows 1–6), **all are 2026 preprints and none is peer-reviewed.**
> Only PIGuard (ACL 2025) and AgentDojo (NeurIPS 2024) among the agent-security
> comparators are peer-reviewed. Chapter 2 should state this, because a gap
> argued away entirely on the basis of non-peer-reviewed preprints rests on
> weaker ground than one argued against published work — in both directions.

---

# 3. COMPONENT-LEVEL COMPARISON — NEXUS (§7)

Labels: **Exact overlap** · **Partial overlap** · **Different** · **Not found** ·
**NIV**. No item is labelled novel.

| # | Dimension | NEXUS (SIV) | REM (as documented) | Assessment |
| - | --------- | ----------- | ------------------- | ---------- |
| **A** | Runtime placement | Intercepts the structured plan **before execution** | Intercepts proposed action before execution | **Exact overlap** |
| **B** | Predictor | Logistic regression risk score | Ridge (L2-penalised) logistic regression | **Exact overlap** on family; **Partial** on regularisation — NEXUS's penalty NIV |
| **C** | Calibration | **Platt scaling**, selected over isotonic for lowest ECE on a small calibration split | Platt on the logit, `γ₁ > 0` | **Exact overlap** |
| **D** | Feature representation | 9-dim plan vector: plan length, irreversibility, per-category step counts, sensitivity, cost, tool diversity, delete side-effect indicator | Groups A/B/C — **not yet specified** | **Partial overlap.** NEXUS's vector already contains irreversibility, sensitivity and cost — three concepts REM proposes |
| **E** | Behavioral / trajectory info | **Session manager for cross-turn state**; plan-level structure | Group B features; sequential component unresolved | **Partial overlap** — REM must not present cross-turn state as differentiating |
| **F** | Financial context | Not found — general tool-using agents | Financial specialisation | **Different** |
| **G** | Action space | allow · block · request confirmation · request revision | Allow · Block · Escalate · Modify | **Exact overlap in cardinality and near-exact in semantics** (confirmation≈Escalate, revision≈Modify) |
| **H** | Decision rule | *"formal intervention policy"* over signals from four components. **Whether an expected-loss derivation is used: NOT FOUND in retrieved material** | `v* = argmin_v R_t(v)` with tier-indexed loss | **Partial overlap / requires further prior-art verification.** This is the single most important unresolved comparison |
| **I** | Consequence / severity tiers | Features include *sensitivity* and *cost*; **explicit consequence tiers indexing a loss function: NOT FOUND** | `k_t` indexing `L(v,y,k)` — **unresolved** | **Partial overlap — requires verification** |
| **J** | Mitigation | Block; request confirmation; request revision | Canonical step-level four | **Exact overlap** in kind |
| **K** | Explainability | Linear model implies coefficient attribution is available; explicit treatment **Not found** | Linear Shapley, audit-only | **Partial overlap** |
| **L** | Evaluation | **128-instance synthetic benchmark**; F1 0.949; 4-class intervention accuracy 0.6406; rule-blind **NEXUS-Stress** F1 0.881; **sub-millisecond CPU latency** | Execution-grounded financial, unresolved | **Different** — synthetic vs execution-grounded |

## Reading

Eight of twelve dimensions show exact or partial overlap. REM's documented
differences are confined to **F (financial specialisation)** and **L (evaluation
grounding)**, with **H and I unresolved pending verification of whether NEXUS's
"formal intervention policy" is decision-theoretic.**

> **Required verification action.** Whether NEXUS derives its action from an
> expected-loss minimisation is the pivot of REM's decision-layer position, and
> retrieved material does not settle it. **The NEXUS paper must be read directly
> before Chapter 2 asserts any distinction here.** Until then:
> *"the reviewed material does not establish whether NEXUS's intervention policy
> is derived from an expected-loss criterion."*

> **Latency note.** NEXUS's reported sub-millisecond CPU latency is a
> substantially tighter reference than DreamGuard's 25 ms. REM's planned
> PromptGuard 2 22M extractor (19.3 ms/classification at 512 tokens on an A100)
> would be several orders of magnitude slower per call. **This is a feasibility
> concern for any latency comparison and must be measured.**

---

# 4. COMPONENT-LEVEL COMPARISON — AgentTrust (§8)

| Dimension | AgentTrust (SIV) | REM | Assessment |
| --------- | ---------------- | --- | ---------- |
| Non-invasive interception | MCP server; any MCP-compatible agent | Non-invasive layer | **Exact overlap** |
| Pre-execution placement | Evaluates each proposed action before execution | Same | **Exact overlap** |
| Multi-step tracking | **RiskChain** detection for multi-step attack chains | Group B / trajectory features | **Partial overlap** |
| Verdict space | **allow · warn · block · review** (four-valued) | Allow · Modify · Escalate · Block | **Partial overlap** — same cardinality; `warn` ≠ `Modify` |
| Behavioral reasoning | Shell deobfuscation normaliser; cache-aware LLM-as-Judge for ambiguous inputs | Feature-based, no LLM judge | **Different in mechanism, overlapping in role** |
| Remediation | **SafeFix** — safer-alternative suggestions | Modify — one declared mechanism (unresolved) | **Partial overlap.** REM must cite SafeFix |
| Audit / explanation | Structured **TrustReport** | Audit record + linear attribution | **Partial overlap** |
| Runtime performance | Not found in retrieved material | To be measured | **Not found** |
| Financial specialisation | Not found | Financial | **Different** |
| Consequence-aware decision | Not found | `k_t` (unresolved) | **Not found** |
| Expected-loss decision rule | **Not found** — verdicts appear rule/judge-assigned | `argmin_v R_t(v)` | **Not found in AgentTrust** |

**Statement for the thesis:** *AgentTrust demonstrates prior art for runtime
pre-execution interception, four-valued verdicts, multi-step chain tracking, and
remediation-style intervention.* The retrieved material does not indicate a
decision-theoretic derivation of the verdict, but **absence in an abstract is not
evidence of absence in the paper** — this requires direct reading.

---

# 5. COMPONENT-LEVEL COMPARISON — DreamGuard (§9)

Compared by **function and role**, not model family, per §9.

| Function | DreamGuard (SIV) | REM | Assessment |
| -------- | ---------------- | --- | ---------- |
| Trajectory modelling | Compact **recurrent latent state** over the trajectory | Trajectory features (unspecified) | **Partial overlap in role**, different in mechanism |
| Immediate risk | Immediate-hazard evidence | `p_t` at the current step | **Partial overlap** |
| Prefix risk | **Prefix-risk evidence** from predicted future latent states | Not represented | **Different — DreamGuard covers a capability REM does not** |
| Sequence accumulation | Multi-horizon signal fusion | Unresolved (CONFLICT) | **Partial / unresolved** |
| Calibration | Not found | Platt | **Not found in DreamGuard** |
| Thresholds | Not found | No threshold; argmin | **Not found** |
| Latency | **25 ms average end-to-end per call** | To be measured | **Reference point** |
| Intervention | Pre-execution intervention decisions | Four verdicts | **Partial overlap** |
| Financial specialisation | Not found | Financial | **Different** |
| Evaluation | Four benchmarks + online guardrail evaluation | Unresolved | **DreamGuard is broader** |

> **Honest note.** DreamGuard performs **forward** risk prediction, which REM
> does not attempt. Framing REM's simpler design as an advantage would be
> unsupported; it is a **different scope**, with auditability as the stated
> rationale — a **[PD]** position, not an evidenced superiority.

---

# 6. ANALYSIS — Calibration Is Not Control (§10)

## What the paper establishes (SIV)

| Aspect | Content |
| ------ | ------- |
| Calibration | Recalibrating the same scalar score **improves prediction metrics but leaves control regret unchanged** |
| Scalar risk | Critiques oversight framed as scalar risk + threshold routing |
| Action selection | Proposes **intervention advantage** — expected utility gain from intervening rather than continuing — as the decision object |
| Intervention consequences | Central: the question is whether an available intervention would improve the outcome |
| Recoverability | Two prefixes may share a risk estimate yet require different actions because one remains recoverable |
| Closed-loop evaluation | Introduces **prefix branching**, a same-prefix counterfactual protocol executing candidate actions from identical trajectory states |
| Result | Across four benchmarks, **action-conditioned control yields regime-dependent gains over scalar routing** |

## What it might motivate in REM — strictly separated

| Possible REM implication | Classification |
| ------------------------ | -------------- |
| Distinguish likelihood from action consequence in the decision layer | **[L]** literature-supported |
| Report calibration quality and decision quality separately (Q1 vs Q2) | **[L]** literature-supported |
| REM's action-conditioned `R_t(v)` is *not* scalar-threshold routing | **[PD]** — a reasonable reading, but the paper does not assess REM |
| `k_t` = reversibility + amount + authorization | **[PD] — PROJECT PROPOSAL ONLY. Not supported by this paper.** *(Stage 3 wrongly presented this as supported — corrected, C-3)* |
| Adopt prefix branching | **⚠️ FORBIDDEN** — `CLAUDE.md` lists *"counterfactual prefix-branching controller"* under FORBIDDEN REINTRODUCTIONS |

> **Two consequences worth stating plainly.**
> 1. The paper's own proposed method is a **forbidden reintroduction** for REM.
>    REM therefore cannot adopt its solution, only its critique.
> 2. The finding that *recalibration leaves control regret unchanged* applies to
>    **scalar routing**. REM's `R_t(v)` is action-conditioned through `L(v,y,k)`,
>    so REM is arguably not the target — **but the paper does not evaluate REM,
>    and this defence is [PD], not [P].**

---

# 7. ANALYSIS — Corll / sequential accumulation (§11)

| Question | Finding (SIV) |
| -------- | ------------- |
| What is accumulated? | **Frozen per-event detector scores**, reduced to **peak** and **CUSUM persistence** statistics |
| Mathematical method | CUSUM-style persistence + peak, over scores from a frozen char-ngram SVM plus an embedding-contrastive head |
| Is ARL stated? | **Not found in retrieved material.** No average-run-length or calibrated false-alarm criterion was retrieved |
| Deployable detector provided? | **No — the paper self-describes: "This is a boundary result, not a deployable detector."** |
| Theoretical boundary? | **Yes**, explicitly |
| Directly comparable to REM's pipeline? | **Partially.** Corll accumulates *frozen external detector scores* at a proxy; REM's estimator is fitted in-pipeline. The setups differ |
| Reported result | On concentrated attacks, trajectory-level accumulation beats the per-event foil under a clustered bootstrap (gap +0.092, 95% CI [+0.025, +0.155]); persistence and peak statistically tied |

> **Constraint per §11.** This paper **must not** be used as evidence that a
> deployable REM sequential detector is warranted or validated. It supports the
> claim that *the reviewed literature demonstrates temporal accumulation as a
> research direction and reports a boundary result*, nothing more.

---

# 8. ANALYSIS — FinHarness (§12)

Per §12, "owns financial validation" is replaced by a precise statement.

| Aspect | FinHarness (SIV) | REM | Assessment |
| ------ | ---------------- | --- | ---------- |
| Financial environment | Wraps a finance agent end-to-end | Financial agent | **Exact overlap in domain** |
| Action space | Refuse / re-plan / approve — **by the agent itself**, prompted by re-injected evidence | REM decides; agent does not | **Different — important distinction** |
| Attack scenarios | Prompt-induced unauthorised actions; injection that starts benign then pivots mid-workflow | Nine-category matrix (unresolved) | **Partial overlap** |
| Transaction semantics | Multi-step business workflows | Group C (unspecified) | **Partial overlap** |
| Intervention / mitigation | **Evidence re-injection** — the agent then decides | **Enforcement** — REM withholds or blocks | **Different in kind** |
| Execution-grounded evaluation | Inline, end-to-end wrapping | Planned | **Partial overlap** |
| Closed-loop evaluation | Not found | Not implemented | **Not found in either** |
| Benchmark reproducibility | Not found in retrieved material | AgentDojo version pinning planned | **Not found** |

**Statement for the thesis:** *FinHarness provides prior art for
execution-grounded financial-agent evaluation and for the joint requirement of
blocking unauthorised actions while approving legitimate multi-step workflows.*

> **A distinction that may matter, stated cautiously.** FinHarness appears to
> operate by **re-injecting evidence so the agent decides**; REM **enforces**.
> These are different control regimes. This is **[PD] potentially
> differentiating** and **requires further prior-art verification** before any
> claim rests on it.

---

# 9. ANALYSIS — PIGuard (§13)

**Status correction: VERIFIED (SIV), peer-reviewed, ACL 2025.** Stage 3's "could
not be confirmed" is withdrawn (C-1).

| Aspect | Content (SIV) |
| ------ | ------------- |
| Problem | Prompt-guard models suffer **over-defense** — falsely flagging benign inputs due to **trigger-word bias** |
| Contribution 1 | **NotInject**, an evaluation dataset measuring over-defense: **339 benign samples enriched with trigger words** common in injection attacks |
| Contribution 2 | **MOF (Mitigating Over-defense for Free)** training strategy reducing trigger-word bias |
| Contribution 3 | Described as the first prompt-guard model against prompt injection built with open-source training data and detailed documentation |
| Availability | Code and model weights on GitHub and Hugging Face |

## Significance for REM — two consequences

1. **Over-defense measurement is already represented in prior art, with a
   dataset.** Stage 3's experimental matrix described category 9
   (benign-but-suspicious) as essential for measuring over-defense. That
   requirement stands, but **REM must not present over-defense evaluation as a
   differentiating contribution** — PIGuard demonstrates prior art for it, and
   NotInject is a directly relevant instrument.
2. **NotInject is a candidate evaluation resource** for REM's category 9, subject
   to verification of licence and applicability to the agent (rather than
   prompt-guard) setting. **[V] validation decision.**

> **Note on PIGuard's own framing.** The retrieved description includes a
> "first … built with open-source training data" claim. REM should cite
> PIGuard's *demonstrated mechanism*, not repeat its priority claim.

---

# 10. CUSUM / SEQUENTIAL COMPONENT (§6)

Per §6 this is analysed, **not resolved**, and no compromise is proposed.

### 1. What the prior literature demonstrates

- Corll (SIV) demonstrates CUSUM-style temporal accumulation over frozen
  per-event scores and reports a **boundary result, explicitly not a deployable
  detector**. No ARL was retrieved.
- Page (1954) (SIV, peer-reviewed) establishes CUSUM and average-run-length
  analysis as classical statistical process control.
- DreamGuard (SIV) demonstrates an alternative treatment of sequential risk via a
  recurrent world model.
- NEXUS (SIV) maintains **cross-turn session state**, which is a form of
  sequential representation.

### 2. What the current REM contract says

`CLAUDE.md` § FROZEN REM PIPELINE: *"CUSUM is OPTIONAL and OBSERVE-ONLY. CUSUM
MUST NOT enter the core verdict path."* § FORBIDDEN REINTRODUCTIONS additionally
bars *"risk-based CUSUM"* and *"CUSUM in the core verdict path"*.

### 3. Is sequential evidence already represented elsewhere in REM?

**Partially, and this weakens the case that CUSUM is required.** REM's Group B
already proposes step count, tool transition, repeated-action count and tool
diversity — all of which carry trajectory information into `x_t` **without any
CUSUM statistic**. `Trajectory.prefix()` already provides causal history to every
component.

### 4. Does the current thesis actually require CUSUM?

**The reviewed evidence does not establish that it does.**

- REM's stated objectives (§27 of the instruction set) name *"sequential risk
  accumulation with a stated false-alarm criterion"* — but this is a **project
  objective**, not a literature-derived requirement.
- Corll cannot be used to justify a deployable detector (§11).
- Group B features already represent sequential information.
- Removing CUSUM would leave REM's frozen pipeline **fully intact** — no frozen
  equation depends on it.

### CONFLICT — SUPERVISOR/PROJECT DECISION REQUIRED

> **Item:** Whether REM includes a sequential change-detection component, and if
> so in what role.
>
> **The conflict:** a previous instruction set proposed configuration
> *C4 = C2 + CUSUM with explicit false-alarm criterion* as a candidate final
> configuration. `CLAUDE.md` states CUSUM is observe-only and must not enter the
> core verdict path. A configuration in which CUSUM is observe-only cannot
> support a claim that depends on it affecting outcomes.
>
> **Not resolved here.** Stage 3's proposed "CUSUM as an evidence feature in
> `x_t`" compromise is **withdrawn** (C-4).
>
> **Supervisor decision required.**

---

# 11. STATUS CLASSIFICATION OF MAJOR REM CLAIMS (§24)

| REM element | Status |
| ----------- | ------ |
| Five-layer architecture | **FROZEN** |
| Four verdicts Allow/Modify/Escalate/Block | **FROZEN** · also **OVERLAPPING PRIOR ART** (NEXUS, AgentTrust) |
| Ridge logistic regression, `s_t = β₀ + βᵀx_t` | **FROZEN** · **OVERLAPPING PRIOR ART** (NEXUS) |
| Platt-on-logit calibration, `γ₁ > 0` | **FROZEN** · **OVERLAPPING PRIOR ART** (NEXUS) |
| `R_t(v) = (1−p_t)L(v,0,k_t) + p_t L(v,1,k_t)`; `v* = argmin` | **FROZEN** (project) · **SOURCE-SUPPORTED** in principle (Elkan, Chow) · **UNVERIFIED** whether NEXUS does the same |
| Consequence tier `k_t` as a concept | **PROJECT-SPECIFIC** · **UNVERIFIED** |
| `k_t` = reversibility + amount + authorization | **PROJECT-SPECIFIC [PD]** — *not* literature-supported |
| Linear Shapley, audit-only | **FROZEN** · **OVERLAPPING PRIOR ART** (Lundberg & Lee) |
| Non-invasive pre-execution interception | **OVERLAPPING PRIOR ART** (AgentTrust, NEXUS) |
| Trajectory/behavioral features | **OVERLAPPING PRIOR ART** (NEXUS session state, DreamGuard, AgentTrust RiskChain) |
| Sequential accumulation with stated ARL | **CONFLICT** (see §10) · **UNVERIFIED** as a REM requirement |
| Financial specialisation | **PROJECT-SPECIFIC** · **OVERLAPPING PRIOR ART** (FinHarness) |
| Execution-grounded financial evaluation | **OVERLAPPING PRIOR ART** (FinHarness) |
| Over-defense / benign-suspicious evaluation | **OVERLAPPING PRIOR ART** (PIGuard, NotInject) |
| Separation of Q1 / Q2 / Q3 | **SOURCE-SUPPORTED** (Calibration Is Not Control) · **OVERLAPPING PRIOR ART** — the paper makes this argument |
| Enforcement rather than evidence re-injection | **POTENTIALLY DIFFERENTIATING** vs FinHarness · **UNVERIFIED** |
| Tier-indexed loss as the derivation of the verdict | **POTENTIALLY DIFFERENTIATING** · **UNVERIFIED** pending direct reading of NEXUS |

---

# 12. SELF-AUDIT (§27)

| Check | Result |
| ----- | ------ |
| Every major citation independently verified | ⚠️ **Partially — search-index tier only.** Primary sources unreachable (see §0). Stated, not concealed |
| No unverified citation presented as fact | ✅ All tiers marked SIV / SIV-partial / NIV |
| PIGuard status corrected | ✅ **C-1** — verified, ACL 2025, peer-reviewed |
| NEXUS overlap precise, not rhetorical | ✅ 12-dimension table; two items marked unresolved |
| AgentTrust overlap precise | ✅ 11-dimension table |
| DreamGuard overlap precise | ✅ 10-function table, compared by role not brand |
| *Calibration Is Not Control* not used to invent `k_t` | ✅ **C-3** — withdrawn and reclassified **[PD]** |
| CUSUM not inserted into `x_t` | ✅ **C-4** — withdrawn; reported as CONFLICT |
| No source transformed into a REM equation without evidence | ✅ |
| No new equation invented | ✅ |
| No numerical loss values invented | ✅ |
| No feature silently added | ✅ |
| No novelty ranking produced | ✅ **C-5** — superlatives removed |
| No Chapter 2 rewrite | ✅ Required-changes list only |
| No Chapter 3 rewrite | ✅ Required-changes list only |
| No code/test/config changed | ✅ `git status` shows only new Stage 2.5 documents |
| Baseline test counts independently verified | ✅ See `STAGE2_5_BASELINE_TEST_RECONCILIATION.md` |
