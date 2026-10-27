# STAGE 2.5 — REM vs PRIOR-ART MATRIX

**Date:** 2026-09-19 · **Analysis only — no code, test, config or chapter modified**

> **Verification tier applies throughout.** Every non-REM cell rests on
> **search-index corroboration only** — the egress policy blocks arxiv.org,
> aclanthology.org, Semantic Scholar, Crossref, OpenAlex and doi.org, so no
> paper was opened. See `STAGE2_5_PRIOR_ART_RECONCILIATION.md` §0.
>
> **`NOT VERIFIED` means the attribute was not established by retrieval — it does
> NOT mean the system lacks the capability.** Absence from an abstract is not
> absence from a paper. No cell is manufactured.

---

# 1. CAPABILITY MATRIX (§19)

Values: **YES** · **PARTIAL** · **NO** · **NOT VERIFIED (NV)**. No scores.

| Capability | REM | NEXUS | AgentTrust | DreamGuard | Calib-Is-Not-Control | Corll | FinHarness | PIGuard |
| ---------- | --- | ----- | ---------- | ---------- | -------------------- | ----- | ---------- | ------- |
| Runtime interception | YES | YES | YES | YES | NO (position/method paper) | PARTIAL (proxy-side) | YES | PARTIAL (input guard) |
| Pre-execution enforcement | YES | YES | YES | YES | NO | NO | PARTIAL (evidence re-injection, agent decides) | NV |
| Logistic regression | YES | YES | NV | NV | NO | NO (char-ngram SVM + embedding head) | NV | NV |
| Probability calibration | YES | YES | NV | NV | YES (subject of study) | NO | NV | NV |
| Platt scaling | YES | YES | NV | NV | NV | NO | NV | NV |
| Trajectory / behavior signals | PARTIAL (features; set unresolved) | PARTIAL (plan structure + cross-turn session state) | YES (RiskChain) | YES (recurrent latent state) | YES (prefix branching) | YES (trajectory accumulation) | YES (cross-turn drift) | NO |
| Sequence accumulation | **CONFLICT — unresolved** | PARTIAL (session state) | PARTIAL | YES (multi-horizon fusion) | NV | YES (CUSUM + peak) | PARTIAL | NO |
| Consequence-aware decision | PARTIAL (`k_t` unresolved) | PARTIAL (sensitivity, cost features) | NV | NV | YES (intervention advantage) | NO | PARTIAL | NO |
| Expected-loss decision | YES (frozen `argmin_v R_t(v)`) | **NV — retrieved material does not establish this** | NV | NV | PARTIAL (utility-gain framing) | NO | NV | NO |
| Multi-action policy | YES (4) | YES (4) | YES (4) | PARTIAL | NV | NO | PARTIAL | NO (binary) |
| Mitigation | YES | YES | YES (SafeFix) | YES | NV | NO | PARTIAL | NO |
| Financial specialisation | YES | NO | NO | NO | NO | NO | YES | NO |
| Execution-grounded evaluation | PLANNED (unresolved) | NO (128-instance synthetic + NEXUS-Stress) | NV | YES (4 benchmarks + online) | YES (4 benchmarks, prefix branching) | PARTIAL | YES (inline end-to-end) | PARTIAL (NotInject dataset) |
| Calibration metrics | YES (Brier; ECE/log-loss planned) | YES (ECE reported) | NV | NV | YES (calibration decomposition) | NV | NV | NV |
| Sequential-control metrics (ARL) | **CONFLICT — unresolved** | NV | NV | NV | NV | **NO — not retrieved; paper self-describes as a boundary result** | NV | NO |
| Attribution / explanation | YES (linear Shapley, audit-only) | PARTIAL (linear model implies coefficients; explicit treatment NV) | YES (TrustReport) | NV | NV | NO | PARTIAL (evidence re-injection) | NO |
| Over-defense evaluation | PLANNED (category 9) | NV | NV | NV | NV | NV | PARTIAL (benign workflows) | **YES (NotInject, 339 benign samples)** |
| Reported latency | TO BE MEASURED | **sub-millisecond CPU** | NV | **25 ms avg end-to-end** | NV | NV | NV | NV |
| Peer-reviewed | — | NO (preprint) | NO (preprint) | NO (preprint) | NO (preprint) | NO (preprint) | NO (preprint) | **YES (ACL 2025)** |

## Notes on reading this matrix

**Three rows carry unusual weight and each has a caveat.**

- **Expected-loss decision.** REM is the only YES, but NEXUS is **NV, not NO** —
  retrieval did not establish whether its "formal intervention policy" is
  decision-theoretic. This row must not be used as evidence of distinction until
  the NEXUS paper is read directly.
- **Financial specialisation.** REM and FinHarness are both YES. This row
  distinguishes REM from the general-purpose systems, not from FinHarness.
- **Sequential-control metrics (ARL).** Every column is NO or NV. Corll is the
  only work accumulating sequentially, and no ARL was retrieved for it. REM's own
  cell is **CONFLICT**, because `CLAUDE.md` bars CUSUM from the verdict path.
  **An empty column is not the same as an available gap** — it may equally
  indicate that ARL is not considered the relevant instrument in this literature.

**Latency is a feasibility concern, not a positioning one.** NEXUS reports
sub-millisecond CPU latency; PromptGuard 2 22M costs ~19.3 ms per classification
at 512 tokens on an A100. If REM adopts that extractor, per-call cost is orders
of magnitude above NEXUS's reported figure.

---

# 2. PRIOR-ART COLLISION REGISTER (§21)

Collision level is a **citation/gap-analysis risk label**, not a judgement of
scientific quality and not a novelty score.

| REM claim | Closest prior art | Collision level | Why | What wording should change |
| --------- | ----------------- | --------------- | --- | -------------------------- |
| Non-invasive runtime interception before execution | AgentTrust; NEXUS | **HIGH** | Both intercept proposed actions pre-execution; AgentTrust ships an MCP server for drop-in use | Remove any framing as a contribution. State: *"REM adopts the non-invasive pre-execution placement demonstrated by AgentTrust and NEXUS."* |
| Calibrated logistic-regression risk estimation | NEXUS | **HIGH** | NEXUS uses a Platt-scaled logistic-regression score, selected over isotonic for lowest ECE on a small calibration split | Remove any suggestion that the estimator or the calibration choice is a REM finding. Cite NEXUS's selection as corroboration of REM's frozen choice |
| Four-action intervention policy | NEXUS; AgentTrust | **HIGH** | Both use four-valued verdicts with near-identical semantics | State the action set is established. Any distinction must rest on the *derivation*, and that is currently **UNVERIFIED** |
| Trajectory / behavioral risk signals | DreamGuard; AgentTrust RiskChain; NEXUS session state; FinHarness drift | **HIGH** | Sequential representation appears in four reviewed systems | Do not present trajectory awareness as differentiating |
| Remediation / Modify action | AgentTrust SafeFix | **HIGH** | SafeFix provides safer-alternative suggestions | Cite SafeFix explicitly when describing Modify |
| Execution-grounded financial-agent evaluation | FinHarness | **HIGH** | FinHarness wraps a finance agent end-to-end with per-step risk and joint benign/attack framing | State: *"FinHarness provides prior art for execution-grounded financial-agent evaluation."* Do not claim the framing |
| Over-defense / benign-suspicious evaluation | **PIGuard (ACL 2025) + NotInject** | **HIGH** | PIGuard targets over-defense directly and supplies 339 benign trigger-word samples | **Stage 3 treated this as a REM contribution — correct it.** Cite PIGuard; consider NotInject as an instrument |
| Separation of prediction from control (Q1/Q2/Q3) | Calibration Is Not Control | **HIGH** | The paper's central argument is exactly this separation | Cite as motivation, not as REM's insight |
| Per-factor attribution via linear Shapley | Lundberg & Lee (2017) | **HIGH** | Closed form for linear models is established; reduces to coefficient × centred feature | Present as standard practice, explicitly not a novelty claim |
| Sequential accumulation with a stated ARL | Corll; Page (1954) | **MEDIUM** | Corll demonstrates the accumulation idea and self-describes as a boundary result; ARL not retrieved. Page establishes ARL classically | Do not claim a gap from Corll's limitations alone. **REM's own status is CONFLICT** — the contract bars CUSUM from the verdict path |
| Verdict derived from a **tier-indexed expected-loss minimisation** | NEXUS ("formal intervention policy"); Elkan (2001); Chow (1970) | **UNVERIFIED** | Elkan/Chow establish the principle for 2 and 3 actions; whether NEXUS derives its policy this way was **not established by retrieval** | Use: *"the reviewed material does not establish whether NEXUS's intervention policy is derived from an expected-loss criterion; this requires direct verification."* |
| Consequence tier `k_t` indexing the loss | NEXUS (sensitivity, cost features) | **MEDIUM–UNVERIFIED** | NEXUS's feature vector contains sensitivity and cost, but explicit tiers indexing a loss function were not retrieved | Present `k_t` as **[PD] project-specific**, requiring further prior-art verification |
| Enforcement rather than evidence re-injection | FinHarness | **LOW–UNVERIFIED** | FinHarness appears to re-inject evidence so the agent decides; REM enforces. Different control regimes | State cautiously as a **potentially differentiating** design difference requiring verification |
| Lightweight / auditable design as a virtue | DreamGuard (25 ms); NEXUS (sub-ms) | **HIGH** | Both report favourable latency; NEXUS's figure is far below REM's likely extractor cost | **Do not claim a lightweight advantage.** Report measured latency without comparative framing unless measured on comparable hardware |

## Collision summary

| Level | Count | Items |
| ----- | ----: | ----- |
| **HIGH** | 10 | Interception · calibrated LR · four-action policy · trajectory signals · remediation · financial evaluation · over-defense evaluation · Q1/Q2/Q3 separation · attribution · lightweight framing |
| **MEDIUM** | 2 | Sequential accumulation with ARL · consequence tier |
| **LOW** | 1 | Enforcement vs re-injection |
| **UNVERIFIED** | 1 | Expected-loss derivation of the verdict |

> **What this register shows.** Ten of fourteen examined REM claims carry HIGH
> collision risk and require wording changes. The two items on which a cautious
> position might rest — the **expected-loss derivation** and the **enforcement
> regime** — are both **UNVERIFIED or LOW-verified**, and **each depends on
> reading a paper that could not be opened in this environment.**
>
> This is a statement about the state of the evidence, not about REM's merit.
> It does mean that **no positioning claim should be finalised until the NEXUS
> and FinHarness papers are read directly.**
