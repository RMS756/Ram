# Chapter 2: Review of Partially Verified Sources (Parts A–D)

**Date:** 25 September 2026
**Branch:** `claude/rem-thesis-lit-review-merge-j1px4f`
**Scope:** The sources flagged as partially verified in the Chapter 2 reports, a focused re-verification of AgentTrust and NEXUS, and the verification rule applied from this review onward.

---

## 0. Evidence rule applied in this review

Direct access to arXiv, SSRN and publisher full texts remained **blocked by the container's egress policy** in this session. The same limitation was recorded earlier in the thesis project (`V1_NEXUS_DIRECT_VERIFICATION.md`, 21 Sep 2026, branch `claude/rem-algorithm-implementation-3ktvze`). That record defines evidence tiers and rules that **search-engine-retrieved text (tier 7) cannot settle a primary question**. This review adopts the same standard.

| Status | Rule |
|---|---|
| **FULLY VERIFIED** | Identity and metadata confirmed (Crossref, proceedings page, or the arXiv abstract listing), **and** every claim Chapter 2 uses is either an abstract-level statement or is recorded as FV (formulation checked) in the thesis's own verification register (Chapter 3 Table 3.17 / Stage 2 report). |
| **PARTIALLY VERIFIED** | Identity confirmed, but at least one claim Chapter 2 uses rests only on a search-retrieved excerpt of the body text (tier 7), on a secondary description, or on an abstract when the full text is required (prior-art mechanism analysis). |
| **SOURCE NOT FULLY VERIFIED** | Identity or the central claim cannot be confirmed. No retained source has this status. |

**Correction of the 25 September pass.** That pass upgraded NEXUS, AgentTrust, SafeAgent and Lundberg & Lee to FULLY VERIFIED on the basis of search-retrieved excerpts of their body text. Under the rule above, and under this task's instruction to "preserve PARTIALLY VERIFIED" when the full paper is unavailable, the three prior-art systems are **reverted** to PARTIALLY VERIFIED. Lundberg & Lee is upgraded on a different, documented basis: the thesis register.

---

## A1. The eight sources previously reported as partially verified

The previous final report (24 Sep) listed eight partially verified sources. Their individual review follows.

| # | Source | Current status (before this review) | What was verified | What remains unverified | Importance to Chapter 2 | Action | Status after this review |
|---|---|---|---|---|---|---|---|
| 1 | **AgentTrust** (C. Yang, 2026, arXiv 2605.04785) | FULLY (25 Sep upgrade) | Identity, author and date; abstract-level architecture (8 components; 42 patterns; 170 rules; 37 SafeFix rules; 7 RiskChain detectors; MCP server); allow/warn/block/review verdicts; 300- and 630-scenario benchmarks; 95.0% / 73.7% / 96.7% (patched rules, not zero-shot) | ~1.72 ms and ~1.35 s latency figures; worst-case verdict over normalized variants; the judge's five dimensions; the session-tracker ablation result (all tier-7 body excerpts) | **Critical** (research gap; REM positioning; comparison tables) | **RETAIN AS PARTIALLY VERIFIED** | PARTIALLY VERIFIED. The chapter text now names the tier-7 details (§2.8.3) |
| 2 | **NEXUS** (Hossain et al., 2026, arXiv 2607.19356) | FULLY (25 Sep upgrade) | Identity and authors; four interventions; rules + argument inspection + calibrated LR score; 128-instance synthetic benchmark; F1 0.949; 4-class accuracy 0.6406; +27.3 pp over rule-only; 92% / 78% of GPT-4o at ~4,800× speed | Fixed costs 0 / 0.1 / 0.3 / 1 and loss-optimal thresholds; rule-first cascade detail; ECE 0.085 → 0.013; 0.205 ms median; the upper-bound caveat; OOD F1 0.861 / 0.881; nine rules; session manager (all tier 7, though corroborated by independent retrievals on 21 and 25 Sep) | **Critical** (Gap 1; decision-mechanism comparison) | **RETAIN AS PARTIALLY VERIFIED** | PARTIALLY VERIFIED. The chapter text now names the tier-7 details (§2.8.4) |
| 3 | **SafeAgent** (H. Liu et al., 2026, arXiv 2604.17562) | FULLY (25 Sep upgrade) | Identity and authors; runtime controller + context-aware decision core; operator list; evaluation on ASB and InjecAgent; ablation over recovery confidence / policy weighting | The recovery-action list (sanitization, replanning, argument rewriting, escalation, rollback, termination); whether calibration or latency are reported | Important (Table 2.5; consequence-aware prior art) | **RETAIN AS PARTIALLY VERIFIED** | PARTIALLY VERIFIED. Flagged in §2.8.2 |
| 4 | **Jackson** (2025, SSRN 5904104) | PARTIAL | Identity (Freeman Jackson; 13 Nov 2025); abstract: governed-action model; multi-dimensional risk score; allow/deny/sanitize/escalate enforcement state machine | Everything beyond the abstract: calibration, evaluation, attribution, ablation. The SSRN full text is inaccessible | Important (verdict-set prior art) | **RETAIN AS PARTIALLY VERIFIED** | PARTIALLY VERIFIED. The chapter makes only abstract-level claims and explicitly makes no negative claims |
| 5 | **H.-H. Chen** (2026, arXiv 2605.25632) | PARTIAL (given name single-sourced) | Author **Hao-Hsuan Chen** now confirmed on the arXiv listing by two independent arXiv-domain retrievals; AAI and Authority Frontier claims are abstract-level | — | Moderate (consequence-aware prior art) | **FULLY VERIFY** | **FULLY VERIFIED** |
| 6 | **Cordon** (Z. Chen et al., 2026, arXiv 2606.17573) | PARTIAL (author-order conflict) | Author order Chen, Dong, Liu, Li, Zhai, Xu, Pu confirmed on the arXiv listing by two independent arXiv-domain retrievals (with affiliations); all claims abstract-level | — | Low–moderate (transactional mitigation) | **FULLY VERIFY** | **FULLY VERIFIED**. The reference entry already uses the confirmed order |
| 7 | **Lundberg & Lee** (2017) | FULLY (25 Sep upgrade via a hosted copy) | Metadata (NIPS 30, pp. 4765–4774); Corollary 1 (Linear SHAP) recorded as **FV** in the thesis register (Chapter 3 Table 3.17 for Eq. 3.11; Stage 2 report "SOURCE-VERIFIED") | — | Important (Eq. 2.6; audit attribution) | **FULLY VERIFY** (basis: thesis register, Source Rule 1) | **FULLY VERIFIED (thesis register)** |
| 8 | **Basseville & Nikiforov** (1993) | PARTIAL (book not accessed) | Identity (Prentice Hall; author PDF hosted at irisa.fr); the Bernoulli LLR and CUSUM recursion recorded as **FV** in the thesis register (Chapter 3 Table 3.17, Eqs. 3.15–3.17) | Not re-read in this session | Moderate (Eq. 2.4 presentation) | **FULLY VERIFY** (basis: thesis register, Source Rule 1) | **FULLY VERIFIED (thesis register)** |

**Result for the eight:**
- Fully verified now: 4 (H.-H. Chen, Cordon, Lundberg & Lee, Basseville & Nikiforov).
- Still partially verified: 4 (AgentTrust, NEXUS, SafeAgent, Jackson).
- Removed or replaced: 0.

---

## A2. Additional sources re-classified under the same rule

Applying the rule consistently to every retained source identified five further sources whose Chapter 2 claims include tier-7 body-text details or secondary-only support. These are **downgraded**, not removed, because each supports a relevant point and the chapter text does not overstate them.

| Source | Detail relying on tier-7 or secondary evidence | Importance | Action |
|---|---|---|---|
| C. Zhang et al. (2026) | ALFWorld figures (ECE 0.463 → 0.006; regret 0.318). The argument itself (intervention advantage; calibration ≠ control) is abstract-level | Important (§2.7.3; Gap 4) | RETAIN AS PARTIALLY VERIFIED |
| ProvenanceGuard (She et al., 2026) | Aligned-trace intervention rates (10.9% / 12.0% / 14.5%); cost and latency. The headline error reductions are abstract-level | Important (§2.5.5; Table 2.6) | RETAIN AS PARTIALLY VERIFIED |
| MI9 (C. L. Wang et al., 2025) | Limitations list (instrumentation, overhead, adversarial evaluation deferred). 99.81% / 1,033 are in the v1 abstract | Moderate | RETAIN AS PARTIALLY VERIFIED |
| Niculescu-Mizil & Caruana (2005) | Small-calibration-set finding (retrieved passage of the authors' PDF; the cut-off was inconsistent across retrievals) | Low | RETAIN AS PARTIALLY VERIFIED |
| Lorden (1971) | Optimality claim supported only by secondary descriptions. Chapter 3 likewise records that the conditions "could not be inspected" | Low | RETAIN AS PARTIALLY VERIFIED. Chapter 2 wording weakened to match Chapter 3 |

**Avoided downgrade.** For Arp et al. (2022), the body-only percentages (90% / 73%) were **removed** from the chapter. The remaining claims are abstract- and website-level, so the source stays FULLY VERIFIED.

---

## B. Priority ordering applied

1. **Research gap / REM positioning / AgentTrust / NEXUS**: received focused verification (Parts C and D below). They remain partially verified only because the full texts are inaccessible. Their central *abstract-level* facts, which carry the prior-art collision, are fully verified.
2. **Algorithmic foundations**: resolved through the thesis register (Lundberg & Lee; Basseville & Nikiforov), and a new original source was added for the ridge penalty (le Cessie & van Houwelingen, 1992; Crossref-verified).
3. **Financial-agent security**: FinHarness numbers are abstract-level (verified); FinVault's withdrawal is verified.
4. **Numerical claims**: see `CHAPTER2_NUMERICAL_CLAIMS_AUDIT.md`.
5. **Comparison tables**: cells resting on tier-7 details are identified in the partial-verification notes of §§2.8.2–2.8.4.

---

## C. AgentTrust: focused verification

| Chapter 2 statement | Evidence | Tier | Status |
|---|---|---|---|
| Runtime safety layer intercepting tool calls **before execution** | arXiv abstract (retrieved repeatedly, including arXiv-domain-restricted retrieval) | Abstract | ✅ Verified |
| Verdicts **allow / warn / block / review** | Abstract | Abstract | ✅ |
| Components: normalizer (9 strategies), analyzer (42 regex patterns), policy engine (170 rules), reporter, SafeFix (37 rules), SessionTracker/RiskChain (7 detectors), cache-aware LLM judge, MCP server | Abstract | Abstract | ✅ |
| Multi-step awareness via RiskChain | Abstract | Abstract | ✅ |
| Mitigation / remediation: safer alternatives (SafeFix) | Abstract | Abstract | ✅ |
| Evaluation: 300-scenario internal benchmark, 95.0% verdict and 73.7% risk-level accuracy at low-ms latency; 630 external scenarios, 96.7% under a patched rule set, not zero-shot | Abstract | Abstract | ✅ |
| Latency ≈ 1.72 ms vs ≈ 1.35 s for a zero-shot LLM-judge baseline | Search-retrieved excerpt of the paper | Tier 7 | ⚠ Partially verified |
| Worst-case verdict over normalized variants | Search-retrieved excerpt | Tier 7 | ⚠ |
| LLM judge: five dimensions (data exposure, system impact, credential risk, scope creep, reversibility) | Search-retrieved excerpt | Tier 7 | ⚠ |
| Disabling SessionTracker leaves verdict accuracy unchanged on both benchmarks | Search-retrieved excerpt | Tier 7 | ⚠ |
| Bulk of performance delivered by analyzer + 170 rules | Search-retrieved excerpt | Tier 7 | ⚠ |
| *(earlier drafts)* maximum-severity aggregation; step-function confidence | Not found in any retrieval | — | ❌ **Not used**; removed from the argument on 25 Sep |
| Calibrated probability of adversarial induction | Not mentioned in any retrieval | — | Reported as NOT REPORTED (absence in consulted material; no negative claim) |

**Overall:** PARTIALLY VERIFIED. The collision facts that REM must concede (interception, four verdicts, chain detection, safer alternatives, ablation with latency) are abstract-level and verified. The differentiating details REM relies on (no calibrated probability; reversibility used only as a judge dimension) rest on the absence of those features from the consulted material, and the chapter words them accordingly. **Name collision:** arXiv 2606.08539 ("AgentTrust: A self-improving trust layer…") is a different work and is not cited.

---

## D. NEXUS: focused verification

| Item requested | Chapter 2 statement | Evidence | Tier | Status |
|---|---|---|---|---|
| Calibrated logistic risk score | Calibrated LR scorer; Platt default; isotonic also evaluated | Abstract (calibrated LR score) + excerpts (Platt chosen for lowest ECE; isotonic lowest Brier) | Abstract + tier 7 | ✅ existence; ⚠ details |
| Consequence features | The plan records side-effect category, irreversibility flag, sensitivity flag, permissions and estimated cost per tool call; nine rules cover irreversible actions, sensitive access, budget, etc. | Excerpts (two retrievals) | Tier 7 | ⚠ Partially verified. The chapter **no longer claims** these are features of the *scorer* (not confirmed) |
| Expected-loss objective | Objective with fixed intervention costs c(ALLOW)=0, c(REVISE)=0.1, c(CONFIRM)=0.3, c(BLOCK)=1; loss-optimal thresholds deployed uniformly | Excerpt | Tier 7 | ⚠ Partially verified |
| Intervention options | allow / block / request confirmation / request revision | Abstract | Abstract | ✅ |
| Deployment policy | Top-down cascade: rules first; multiple critical violations → block; exactly one critical violation → calibrated score decides block vs confirm; threshold crossings route to confirm | Excerpts (25 Sep) consistent with the V-1 record (21 Sep: "scorer-gated demotion… when exactly one critical rule fires") | Tier 7 (two independent retrievals, 4 days apart) | ⚠ Partially verified |
| **Does the deployed system minimize expected loss at every decision?** | **Not established as such.** The evidence indicates that expected loss sets *thresholds* on the score *inside* a rule-first cascade. Rules pre-empt the score in several branches, and REVISE cannot be reached without a rule. The chapter states exactly this and does **not** claim that NEXUS performs per-decision argmin over all actions | Excerpts | Tier 7 | ⚠ **UNRESOLVED at paper level**. Chapter 2 wording is conditional and flagged |
| Session / cross-turn state | Session manager for cross-turn state (4th component) | Excerpts (21 and 25 Sep) | Tier 7 | ⚠ Chapter 2 corrected (was NOT REPORTED) |
| Evaluation / caveats | 128-instance synthetic test; authors call in-distribution results upper bounds; OOD R-Judge 0.861, stress 0.881; organic traces future work | Abstract (128; 0.949; 0.6406) + excerpts (caveat; OOD) | Mixed | ✅ / ⚠ |
| Latency | median 0.205 ms (the V-1 record: "sub-millisecond CPU latency") | Excerpts | Tier 7 | ⚠ |
| Comparison against REM | REM differs in (i) per-tool-call evaluation during execution vs pre-execution plan evaluation, (ii) losses indexed by each action's consequence tier vs fixed intervention costs, (iii) an executable banking benchmark vs author templates | Built on the rows above | — | Differences (i) and (iii) rest on abstract-level facts ✅. Difference (ii) rests on tier-7 cost values ⚠, and the chapter says so |

**Overall:** PARTIALLY VERIFIED. The finding that NEXUS uses expected loss more directly than the July and early-September drafts said (conflict C13) **narrows Gap 1**. It is retained in Chapter 2 *because it weakens REM's position* (Source Rule 14: do not silently choose the source supporting REM), and it is flagged as tier-7 evidence pending full-text confirmation.

**Action required before submission:** obtain the NEXUS and AgentTrust full texts (for example from an unrestricted network) and confirm the ⚠ rows. If confirmed, upgrade both to FULLY VERIFIED. If any ⚠ row is contradicted, revise §§2.8.3–2.8.4, Tables 2.6–2.7 and Gap 1.

---

## Summary counts (after this review)

| Measure | Count |
|---|---:|
| Retained sources | 70 (68 + le Cessie & van Houwelingen 1992 + Ng & Jordan 2002) |
| FULLY VERIFIED | 61 |
| PARTIALLY VERIFIED | 9 (AgentTrust, NEXUS, SafeAgent, Jackson, C. Zhang, ProvenanceGuard, MI9, Niculescu-Mizil & Caruana, Lorden) |
| SOURCE NOT FULLY VERIFIED | 0 |
| Removed / replaced | 0 |
