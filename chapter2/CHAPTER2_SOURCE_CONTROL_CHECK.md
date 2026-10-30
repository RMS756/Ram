# Chapter 2: Source-Control Check (Source-Use Priority Rules 1–20)

**Date:** 25 September 2026
**Scope:** The integrated Chapter 2 (`CHAPTER2_LITERATURE_REVIEW_INTEGRATED.md`), after a dedicated compliance pass against the Source-Use Priority Rules. This pass re-verified central claims **against primary-source domains only** (arXiv, ACL Anthology, PMLR, OpenReview, USENIX, proceedings pages, EUR-Lex / the AI Act Service Desk, and the authors' own PDFs). It also corrected every place where the text relied on an earlier draft's unverified characterization.

---

## Rule 1 and Rule 18: existing verified sources first; replacements recorded

- No existing verified thesis source was replaced by a newer, weaker source. Of the 80 existing works, 55 were retained. The 25 removals were for scope, redundancy or non-verification (change log §3), never for recency.
- Replacements and corrections of existing citations (all recorded in the change log, §5):

| Existing citation | Replaced / corrected by | Rule 18 ground |
|---|---|---|
| "Chen, Z. (2026)" (*Insuring every action*) | H.-H. Chen (2026) | Current source incorrect (author) |
| "Pro2Guard" (v2.0) | ProbGuard (same arXiv ID, renamed) | Primary source's current identity |
| ShieldAgent / GuardAgent as arXiv preprints | ICML 2025 (PMLR 267) proceedings versions | Peer-reviewed version preferable (Rule 4) |
| ProvenanceGuard figures and authors (v2.0) | Primary-source figures and authors | Existing claim did not match the source |
| "ECE introduced by Guo et al. (2017)" (integrated draft of 24 Sep) | Naeini et al. (2015) as the origin; Guo et al. for the confidence-based form | Original source preferable (Rule 2) |
| FinVault numbers as evidence | FinVault cited only as withdrawn | Source withdrawn |
| NEXUS "rule cascade, not expected-loss" (earlier drafts) | Primary-source description (fixed-cost expected-loss thresholds inside a rule-first cascade) | Newer primary evidence materially changes the understanding |
| AgentTrust "max-severity aggregation; step-function confidence" (earlier drafts) | Verified description (worst-case verdict over normalized variants; analyzer + rules; LLM judge) | Existing claim not confirmable against the source |

---

## Rules 2 and 10: original sources for algorithms and traceable equations

| Method / concept | Original source cited | Also cited (role) | Equation | Equation source | Status |
|---|---|---|---|---|---|
| Logistic regression for binary outcomes | Cox (1958) | NEXUS (application) | Eq. 2.1 | Cox (1958) | ✅ Original |
| Platt scaling | Platt (1999) | Guo et al. (2017) (describes it as the parent of temperature scaling) | Eq. 2.2 | Platt (1999) | ✅ Original |
| Temperature scaling | Guo et al. (2017) | — | — | — | ✅ Original |
| Isotonic calibration | Zadrozny & Elkan (2002) | Niculescu-Mizil & Caruana (2005) (empirical comparison) | — | — | ✅ Original |
| Beta calibration | Kull et al. (2017) | — | Functional form described in text | Kull et al. (2017) | ✅ Original; the a = b reduction is stated as derived from the form |
| Expected calibration error | Naeini et al. (2015) | Guo et al. (2017) (confidence-based form) | Eq. 2.3 | Guo et al. (2017) form | ✅ **Corrected in this pass** |
| CUSUM | Page (1954) | Basseville & Nikiforov (1993) (authoritative presentation); Lorden (1971) (optimality) | Eq. 2.4 | Page's procedure in the recursive log-likelihood-ratio form of Basseville & Nikiforov (1993) | ✅ Original cited; ⚠ the book was not accessed (PARTIALLY VERIFIED). The recursion is the standard equivalent of Page's rule |
| Minimum expected-cost decision | Elkan (2001) (cost-sensitive classification) | NEXUS (application) | Eq. 2.5 | Elkan (2001) | ✅ Authoritative source for the cost-matrix formulation used |
| Reject option / error–reject trade-off | Chow (1970) | — | — | — | ✅ Retained existing verified source (Rule 1). Note: Chow's earlier 1957 paper introduced a reject rule; the 1970 paper is the standard source for the optimum error–reject trade-off cited here |
| Additive attribution / Linear SHAP | Lundberg & Lee (2017) | — | Eq. 2.6 | Lundberg & Lee (2017), Corollary 1 | ✅ **Verified in this pass** |
| Execution monitoring (runtime enforcement) | Schneider (2000) | — | — | — | ✅ Original |
| Behavioral anomaly detection over action sequences | Forrest et al. (1996) | Chandola et al. (2009, 2012) (systematizations) | — | — | ✅ Original + surveys used only as surveys |
| Base-rate / ML-for-security pitfalls | Arp et al. (2022); Sommer & Paxson (2010) | — | — | — | ✅ Primary |

No equation is taken from a secondary paper. No REM risk equation is introduced.

---

## Rules 3 and 16: primary sources for systems; independent verification of major prior art

Each dimension was checked against the system's own paper. **V** = verified from the primary source in the September 2026 passes; **P** = partially verified; **NV** = not verifiable from the consulted material.

| System | Architecture | Runtime position | Monitored information | Behavioral scope | Decision mechanism | Mitigation | Evaluation | Reported limitations |
|---|---|---|---|---|---|---|---|---|
| **AgentTrust** (C. Yang, 2026) | V: normalizer, 42-pattern analyzer, 170 rules, reporter, SafeFix (37), RiskChain (7), LLM judge, MCP server | V: pre-execution interception of tool calls | V: tool-call content (shell, files, HTTP, credentials) after deobfuscation | V: session chain detectors | V: analyzer + rules; worst-case verdict over normalized variants; LLM judge (5 dimensions incl. reversibility). NV: aggregation beyond that | V: allow / warn / block / review; safer alternatives | V: 300 internal (95.0% verdict / 73.7% risk level; ~1.72 ms); 630 external (96.7%, patched, not zero-shot); session-tracker ablation shows no effect | V: 630 result not zero-shot; P: others not retrieved |
| **NEXUS** (Hossain et al., 2026) | V: rules (9), argument inspector, calibrated LR scorer | V: pre-execution, plan level | V: structured plan with side-effect category, irreversibility, sensitivity, permissions, cost per tool call | NV: no trajectory component described | V: top-down cascade; rules first; the score decides block vs confirm under a single critical violation; loss-optimal thresholds from an expected-loss objective with fixed costs 0 / 0.1 / 0.3 / 1 | V: allow / block / confirm / revise | V: 128-instance synthetic test (F1 0.949; 4-class 0.6406; +27.3 pp); ECE 0.085 → 0.013; 0.205 ms; OOD F1 0.861 / 0.881 | V: in-distribution results are upper bounds; no REVISE signal without a rule; organic traces future work |
| **SafeAgent** (H. Liu et al., 2026) | V: runtime controller + context-aware decision core (risk encoding, utility–cost, consequence modeling, policy arbitration, state sync) | V: around the agent loop | V: persistent session state; inputs, responses, observations | V: stateful over trajectories | V: LLM-realized operators and policy arbitration | V: sanitization, replanning, argument rewriting, human escalation, rollback, termination | V: ASB, InjecAgent; ablation over recovery confidence / policy weighting | V: human approval increases cost and reduces responsiveness; NV: calibration and latency reporting |
| **FinHarness** (H. Jia et al., 2026) | V: query monitor, tool monitor, cascade | V: inline, per step | V: single-turn intent, cross-turn drift, prospective tool calls | V: cross-turn drift; accumulated per-step risk | V: routing between lightweight and advanced LLM judges on accumulated risk | V: block / approve; escalation to the advanced judge | V: FinVault only; ASR 38.3% → 15.0%; approve 41.1% → 39.3%; advanced calls 646 → 138 (4.7×) | NV: limitations section not retrieved; the withdrawal of FinVault is an external limitation |
| **MI9** (C. L. Wang et al., 2025) | V: six components | V: runtime governance | V: agent-semantic telemetry | V: FSM conformance; goal-conditioned drift | V: agency-risk index; authorization monitoring | V: graduated containment | V: 1,033 synthetic scenarios; 99.81% detection | V: synthetic only; instrumentation dependence; overhead; adversarial evaluation deferred |
| **PRISM** (F. Li, 2026) | V: in-process plugin + sidecars; 10 lifecycle hooks | V: gateway lifecycle hooks | V: ingress, prompt construction, tool execution/results, outbound | V: conversation/session risk with TTL decay | V: heuristic + LLM scanning; policy controls | V: policy enforcement; tamper-evident audit | V: preliminary benchmarks; per-hook profiling | V: results preliminary; weaker than deployment-level study |
| **ProvenanceGuard** (She et al., 2026) | V: three-stage provenance pipeline | V: before tool-call execution | V: evidence in the agent context for each call | NV | V: whether the call is supported by traceable evidence | V: intervention on unsupported calls | V: Agent-SafetyBench 44.3% → 2.1%; WorkBench 32.4% → 18.7%; aligned intervention 14.5% vs 10.9% | V: ~3.6 LLM calls per case; higher tokens, cost and latency than baselines |
| **Jackson** (2025) | P: governed-action model; OPA / Envoy / Kubernetes reference architecture (abstract) | P: runtime enforcement | P: inference, tool usage, data access, actuation | NV | P: multi-dimensional risk score → deterministic enforcement state machine | P: allow / deny / sanitize / escalate | P: "significant reductions… minimal latency" (qualitative) | NV: full text not accessible |
| **H.-H. Chen** (2026) | V: Actuarial Action Interface; quote–bind–commit; 7-class taxonomy | V: pre-execution gate | V: side-effect-bearing actions | NV | V: deterministic pricing against a safe default; reserve-capital gating | V: gating / denial | V: Authority Frontier; reserve demand varies 22× across domains; live panel prevents realized loss at low budget | NV: limitations section not retrieved |

The chapter uses only the **V** cells as factual claims. **P** and **NV** cells appear in the chapter only with an explicit "not verified" / "abstract only" qualifier.

---

## Rules 4 and 13: peer review preferred; preprints labeled

| Source type | Count | Notes |
|---|---:|---|
| Peer-reviewed (journal / conference / workshop) | 40 | Including all foundational algorithm sources |
| Book / book chapter | 2 | Basseville & Nikiforov; Platt |
| Preprint | 22 | Each marked "[Preprint]" in the reference list |
| Working paper | 1 | Jackson (SSRN), marked "[Working paper]" |
| Withdrawn preprint | 1 | FinVault, marked "[Withdrawn preprint]", not used as evidence |
| Official sources | 2 | OWASP; EU AI Act, marked "[Official source]" |

**Why each preprint is retained (Rule 13 category).**
- *Important recent prior art, with no peer-reviewed equivalent:* AgentTrust, NEXUS, SafeAgent, Jackson, H.-H. Chen, FinHarness, MI9, PRISM, ProbGuard, DreamGuard, Cordon, ProvenanceGuard, Progent, CaMeL.
- *Important recent evidence:* C. Zhang et al. (calibration vs control); M. Q. Li et al. and Y. Wang et al. (benchmark validity); Mao et al. (financial SoK); Z. Chen, J. Chen et al. (financial evaluation).
- *Directly relevant component with no peer-reviewed equivalent:* LlamaFirewall/PromptGuard; Llama Guard; spotlighting.
- *Accepted but not yet in proceedings:* Thought-Aligner (ICML 2026).

---

## Rule 5: recency

Rapidly evolving topics (agent threats, defenses, runtime systems, benchmarks) are covered with 2023–2026 sources. Foundational methods retain their original older publications (1945–2017 range; Wald 1945 was considered but not needed). No recent secondary source displaces a foundational one.

---

## Rules 6, 17 and 8: relevance, retention and citation stacking

- **Retention (Rule 17).** Every retained source has a stated "exact contribution used in Chapter 2" (evidence matrix, Part B).
- **Relevance (Rule 6).** Sources retained only for generic "LLM/agent/security" relevance were removed (change log §3).
- **Stacking (Rule 8).** Multi-citation sentences were reviewed. Where several sources appear together, each supplies a different mechanism or an independent confirmation: for example, the list of trajectory-aware systems in §2.3.5 and the decision mechanisms in §2.8 synthesis. No claim is supported by redundant secondary citations.

---

## Rule 9: provenance of numerical results

Every number in the chapter is taken from the paper that produced it. None comes from a secondary summary.

| Number(s) in Chapter 2 | Source | Where verified |
|---|---|---|
| 36 toolkits; 144 cases; 23.9%; 68.8% | Ruan et al. (2024) | ICLR proceedings abstract |
| 5 attacks / 10 defenses / 10 LLMs / 7 tasks | Y. Liu et al. (2024) | USENIX page / abstract |
| 1,054 cases; 17 user tools; 62 attacker tools; 24%; ~2× | Zhan et al. (2024) | ACL Anthology / arXiv abstract |
| 10 scenarios; >400 tools; 27 methods; 13 backbones; 84.30% | H. Zhang et al. (2025) | ICLR/OpenReview abstract |
| 110 (440) tasks; 11 categories | Andriushchenko et al. (2025) | ICLR/arXiv abstract |
| ≥80%; ≤1%; <0.1% | Z. Chen et al. (2024) | NeurIPS paper abstract |
| 97 tasks; 629 cases; 4 environments | Debenedetti et al. (2024) | NeurIPS proceedings |
| 40 benchmarks; Kendall's *W* | M. Q. Li et al. (2026) | arXiv abstract |
| 4 benchmarks; 22 models; −0.64 → +0.02 | Y. Wang et al. (2026) | arXiv HTML |
| 30 papers; 90% / 73%; ≥3 pitfalls | Arp et al. (2022) | Authors' paper (arXiv / USENIX PDF passages) |
| >50% → <2% | Hines et al. (2024) | arXiv abstract |
| 39.9% → 1.0%; 70.3% → 3.9% | Shi et al. (2025) | arXiv abstract |
| >90%; all embodied hazards; 100% AV; ms | H. Wang et al. (2026) | ICSE / arXiv abstract |
| 77% vs 84% (earlier 67%) | Debenedetti et al. (2025) | arXiv v2 abstract |
| ~50% → ~90% | Jiang et al. (2025) | arXiv abstract |
| 2.07%; 69.79% | F. Jia et al. (2025) | ACL Anthology abstract |
| 44.3% → 2.1%; 32.4% → 18.7%; 10.9% / 12.0% / 14.5% | She et al. (2026) | arXiv HTML |
| 38.66 s; 65.37%; 80.4% | H. Wang et al. (2025) | arXiv abstract (not used in the chapter text beyond the matrix) |
| ~25 ms | Lin et al. (2026) | arXiv abstract |
| 1,033 scenarios; 99.81% | C. L. Wang et al. (2025) | arXiv HTML (v1) |
| 95.0%; 73.7%; 96.7%; ~1.72 ms; ~1.35 s; 300 / 630 scenarios | C. Yang (2026) | arXiv abstract / HTML |
| 0.949; 0.6406; 27.3 pp; 92%; 78%; ~4,800×; 0.085 → 0.013; 0.205 ms; 0.861; 0.881; costs 0 / 0.1 / 0.3 / 1; 128 instances | Hossain et al. (2026) | arXiv abstract / HTML |
| 0.463 → 0.006; 0.318 | C. Zhang et al. (2026) | arXiv HTML |
| 38.3% → 15.0%; 41.1% → 39.3%; 4.7× | H. Jia et al. (2026) | arXiv abstract |
| 12 attack vectors; 5 dimensions | Mao et al. (2026) | arXiv abstract |

**Removed because no primary evidence could be retrieved:** v2.0's MI9 "99.81%" was *initially* removed and is now **restored** after verification. Still removed: LlamaFirewall 83% / 96%; ASB memory-poisoning 7.92%; AgentSpec 95.56% / 70.96%; ShieldAgent and GuardAgent percentages; all FinVault numbers.

---

## Rules 11 and 12: official and web sources

| Source | Type | Use | Flag |
|---|---|---|---|
| OWASP LLM01:2025 | Official (practitioner taxonomy) | Terminology only (§2.3) | Verified on genai.owasp.org |
| EU AI Act, Arts. 12 and 14 | Official (regulation) | Motivation for R4 / R5 only (§2.9.3) | Art. 12 and Art. 14(4)(a)–(d) confirmed on the official AI Act Service Desk (europa.eu). **Art. 14(4)(e) "stop button… safe state" wording confirmed only via secondary reproductions of the text; re-check against the EUR-Lex PDF before submission** |
| Web pages, blogs, news | — | **None cited** | — |

Non-primary *hosts* were used only to read the primary text itself, never as sources: an annotated copy of Lundberg & Lee (Corollary 1), and the authors' own PDF for Niculescu-Mizil & Caruana. They are not cited.

---

## Rule 14: source conflicts

All 16 conflicts are recorded in the evidence matrix, Part C (C1–C16), with Source A, Source B, the disagreement, evidence strength, thesis impact and handling. Two affect the thesis argument:
- **C9:** FinHarness's results rest on a withdrawn benchmark.
- **C13:** NEXUS's use of expected loss is stronger than earlier drafts stated. This narrows Gap 1, and the chapter now says so.

---

## Rule 15: claim–evidence fit (edits made in this pass)

| Location | Before | After |
|---|---|---|
| §2.2 synthesis | "The literature consistently locates agent risk…" | "Taken together, the reviewed studies locate agent risk…" |
| §2.3 synthesis | "The threat literature is mature…"; "decisive channel / moment" | "The main threat classes relevant to REM have been defined, demonstrated and benchmarked"; "critical entry point / moment" |
| §2.5 synthesis | provenance "the property that matters most for indirect injection" | "a property of particular relevance to indirect injection" |
| §2.6.2 | "among the most informative behavioral signals" | Results reported by ProvenanceGuard and Task Shield "suggest… informative signals", plus the caveat that no common financial comparison exists |
| §2.6.3 | Sommer & Paxson: "attack instances are rare…" | Limited to the paper's verified themes (cost of errors, diversity, semantic gap, evaluation) |
| §2.8 synthesis | "graduated responses are standard rather than exceptional" | "graduated responses are common" |
| §2.11 | "The literature has substantially solved *where* to intervene" | "The literature offers many implementations of the point of intervention" |
| §2.11 | provenance "the most informative signal against indirect injection" | "has shown strong reported results… in the reviewed studies" |
| §2.8.3 / §2.8.4 | Unverified mechanism descriptions from earlier drafts | Replaced by verified primary-source descriptions; residual unverified items explicitly qualified |

Single-study findings are consistently introduced as "its authors reported…", "one ablation found…" or "one study reported…".

---

## Rule 19: final source-hierarchy decisions

For every claim, the chapter uses the highest available level:
1. relevant, verified, original academic source (algorithms; foundational security);
2. peer-reviewed version where one exists (ShieldAgent, GuardAgent, AgentSpec, MELON, Task Shield, InjecAgent, ASB, AgentDojo, AgentHarm);
3. preprint only where no peer-reviewed equivalent exists;
4. official sources only for terminology and regulation.

No secondary or web source is used for any claim.

---

## Rule 20: final source-control checklist

| Check | Result |
|---|---|
| Every major claim has an appropriate source | ✅ |
| Original algorithm papers used for foundational algorithms | ✅ (ECE origin corrected in this pass) |
| Primary papers used for major systems | ✅ (8-dimension table above) |
| Numerical results come from their original evidence | ✅ (Rule 9 table) |
| Equations traceable | ✅ (Eq. 2.1–2.6; Eq. 2.4 presentation source not accessed, flagged) |
| Peer-reviewed sources preferred where available | ✅ |
| Recent sources for rapidly evolving topics | ✅ |
| Older foundational sources preserved | ✅ |
| Official sources clearly distinguished | ✅ |
| Weak web sources not used | ✅ (none cited) |
| Duplicate / low-value references removed | ✅ (25 removed; 8 variants merged) |
| Conflicting evidence explicitly handled | ✅ (C1–C16) |
| No source retained solely to increase the count | ✅ (68 retained; each with a stated contribution) |
| No citation supports a claim stronger than its evidence | ✅ (Rule 15 edits) |

**Residual items (PARTIALLY VERIFIED, 4 of 68):**
- Jackson (2025): abstract only.
- H.-H. Chen (2026): given name from a single secondary listing.
- Cordon: author order conflict.
- Basseville & Nikiforov (1993): book not accessed.

None of these carries a claim that the argument depends on alone.
