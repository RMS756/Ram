# Chapter 2: Current-State Audit (before rewriting)

**Prepared:** 24 September 2026
**Scope:** An audit of the existing Chapter 2 material, done before any rewriting (Step 2 of the merge instructions).

---

## 0. Inputs actually available to this audit

| Requested input | Available? | Notes |
|---|---|---|
| Existing Chapter 2, **v2.0** (`REM_Chapter2_Literature_Review_v2.0.md`, July 2026) | Yes | 745 lines, 54 references, 13 tables. |
| Existing Chapter 2, **PDF** (`chapter_2_v2.pdf`, 40 pp.) | Yes | Image-only print of the v2.0 markdown (PDF title metadata: `REM_Chapter2_Literature_Review_v2.0.md`, created 29 July 2026). Spot-checks of pp. 1, 20 and 40 matched v2.0 exactly. It is not a separate version. |
| Existing Chapter 2, **DOCX** (`Chapter2_Literature_Review.docx`) | Yes | The later **September 2026 update** (Sections 2.1–2.16, 47 references, 3 tables). It already integrates AgentTrust, NEXUS, SafeAgent, H.-H. Chen (2026), C. Zhang et al. (2026), ProbGuard, DreamGuard and the calibration literature. **It is treated as the current baseline.** |
| Chapter 3 | **No** | Not in the repository (the repository was empty) and not uploaded. The DOCX cross-references Sections 3.2, 3.6, 3.7, 3.7.6, 3.10, 3.11 and 3.12. Those references are preserved but could not be checked. |
| Approved proposal, `CLAUDE.md`, Decision Ledger, Research Memory | **No** | Not available. |
| Reference database, verification reports, prior-art audit reports | **No** | Not available as files. The prior-art findings embedded in the DOCX (AgentTrust, NEXUS, SafeAgent, H.-H. Chen, C. Zhang) are treated as the prior audit. |
| REM Algorithm Selection Study; backup-algorithm research | **No** | Not available. The algorithmic content is taken from the DOCX: logistic risk score, Platt/beta calibration, expected-loss decision (Elkan; Chow), CUSUM as the "statistically grounded alternative for accumulating evidence", and linear attribution. **The identity of the designated backup algorithm could not be confirmed from a primary project document** (see §9). |
| Literature matrices / supporting notes | **No** | None available. |

**Consequence.** This audit covers the two real versions of Chapter 2 (v2.0 and the September DOCX). Statements about Chapter 3 and about the algorithm selection come from what the DOCX says about them. They are not taken from those documents directly.

---

## 1. Current structure

### 1.1 v2.0 (July 2026)
2.1 Introduction (PRISMA-informed methodology) · 2.2 Foundations of AI agents · 2.3 Architecture and lifecycle · 2.4 Threats (12 sub-sections, Table 2.1 taxonomy) · 2.5 Runtime security · 2.6 Detection and behavioural analysis · 2.7 Guardrails, policy enforcement, mitigation · 2.8 Explainable AI · 2.9 Financial applications · 2.10 Comparative analysis (Tables 2.3–2.12) · 2.11 Research gap · 2.12 Summary · examiner Q&A · references · self-assessed quality report.

### 1.2 September DOCX (current baseline)
2.1 Introduction (structured narrative review) · 2.2 Agent security problem · 2.3 Prompt injection / IPI · 2.4 Runtime guardrails and architectures (incl. SafeAgent, AgentTrust, NEXUS) · 2.5 Stateful and trajectory-aware protection · 2.6 Action-boundary security · 2.7 Financial-agent requirements (R1–R6) · 2.8 Detection · 2.9 Probability calibration · 2.10 Decision and mitigation · 2.11 Explainability/auditability · 2.12 Benchmarks (Table 2.1) · 2.13 Comparative synthesis (Table 2.2) · 2.14 Research gap · 2.15 Positioning (Table 2.3) · 2.16 Summary.

---

## 2. Reference counts

| Measure | v2.0 | DOCX | Union (distinct works) |
|---|---:|---:|---:|
| Reference-list entries | **63** (the v2.0 quality report claims 54, which is an internal inconsistency) | 47 | **80** |
| Works in both versions (after matching renamed or placeholder entries) | 30 | 30 | — |
| Only in v2.0 | 33 | — | — |
| Only in DOCX | — | 17 | — |

Entries were matched across versions where the same work appears under a different name, an incomplete author list, or a wrong author: Pro2Guard/ProbGuard; "Chen, Z. (2026) Insuring every action"/H.-H. Chen; "Chen [et al.] Cordon"; "FinHarness [authors to be confirmed]"; "Yang [et al.] FinVault"; "She, [initials]"; "Jiang [et al.]"; and "OWASP Top 10 (2025)"/"LLM01:2025". These **8 variant entries were merged**.

**Only in v2.0 (33):** AgentHarm (in the reference list but **never cited in the v2.0 text**); Anwar et al.; Bai et al.; Barredo Arrieta et al.; Capuano et al.; Chandola et al. (2009); Doshi-Velez & Kim; Guidotti et al.; Han et al. (WildGuard); Hua et al. (TrustAgent); Inan et al. (Llama Guard); Khan et al.; Lewis et al.; H. Li et al. (InvestorBench); Liang et al. (SafeRAG); Moustafa et al.; NIST AI RMF; Neelou et al. (A2AS); Ouyang et al.; M. J. Page et al. (PRISMA 2020); Perez & Ribeiro; Rebedea et al. (NeMo Guardrails); Ribeiro et al. (LIME); Schick et al. (Toolformer); Shinn et al.; Syros et al. (SAGA); Tsai & Bagdasarian (Conseca); A. Wei et al.; J. Wei et al.; Xie et al. (FinBen); Yu et al. (2025); Zeng et al. (ShieldGemma); Zou et al.

**Only in DOCX (17):** Basseville & Nikiforov; Chow; Elkan; EU AI Act; Guo et al.; Hines et al.; Hossain et al. (NEXUS); Kull et al.; M. Q. Li et al.; Lin et al. (DreamGuard); H. Liu et al. (SafeAgent); Naeini et al.; E. S. Page (1954); Platt; Y. Wang et al. (2026); C. Yang (AgentTrust); C. Zhang et al. (2026).

---

## 3. Verification status of existing references (after this session's checks)

Checks used Crossref (DOI registration and full metadata), OpenAlex, and web-search retrieval of arXiv, publisher and proceedings abstracts. **Direct access to arXiv and publisher full texts was blocked by the container's network policy**, so full-text-only claims are marked PARTIALLY VERIFIED unless a retrieved passage confirmed them. The per-source detail is in `CHAPTER2_VERIFICATION_LOG.md` and `CHAPTER2_REFERENCE_EVIDENCE_MATRIX.md`.

Of the 80 distinct existing works, **55 are retained** and **25 are removed** (the reasons are in the change log).

| Status (existing works) | Count | Works |
|---|---:|---|
| Retained, FULLY VERIFIED (metadata and the specific claim used) | 47 | e.g., Greshake 2023; Thought-Aligner; InjecAgent; ASB; AgentDojo; AgentHarm; ToolEmu; Y. Liu 2024; Arp 2022; AgentSpec; ShieldAgent; GuardAgent; AGrail; Progent; CaMeL; ProvenanceGuard; MI9; PRISM; ProbGuard; DreamGuard; FinHarness; C. Zhang 2026; M. Q. Li 2026; Y. Wang 2026; E. S. Page 1954; Chow; Naeini; Guo; Kull; Elkan; Platt; Chandola 2009; TrustAgent; Conseca; Yu 2025; L. Wang 2024; OWASP; EU AI Act; FinVault (withdrawal status) |
| Retained, PARTIALLY VERIFIED | 8 | AgentTrust (headline results verified; max-severity aggregation and step-function confidence not re-confirmed); NEXUS (ECE, latency, F1 and test size verified; rule-cascade versus expected-loss detail not re-confirmed); SafeAgent (architecture verified; action list, no-calibration and no-latency claims not re-confirmed); Jackson 2025 (abstract only); H.-H. Chen 2026 (abstract; given name from a single secondary source); Cordon (claims verified; author **order** conflicts between sources); Lundberg & Lee (metadata verified; Linear SHAP corollary not re-read this session); Basseville & Nikiforov (book not accessed) |
| Removed; SOURCE NOT FULLY VERIFIED | 1 | Moustafa et al. 2023 (volume/pages never verified) |
| Removed; not re-checked because out of scope | 23 | see change log |
| Removed; verified but not needed | 1 | Rebedea et al. 2023 (metadata verified via Crossref) |

## 4. Duplicates and version conflicts

| Issue | Detail | Resolution |
|---|---|---|
| Same work under two names | "Pro2Guard" (v2.0) = "ProbGuard" (DOCX), arXiv 2508.00500 (renamed across versions) | Cite once as ProbGuard (H. Wang et al., 2025), with the earlier name noted in the matrix |
| Same work, different titles | Progent: "Programmable privilege control for LLM agents" (v1) versus "Securing AI agents with privilege control" (current) | Cite current title |
| Same work, different titles | Z. Chen, J. Chen et al. (2025): "Position: Standard benchmarks fail – LLM agents present overlooked risks for financial applications" (v1) versus "Standard benchmarks fail – Auditing LLM agents in finance must prioritize risk" (current) | Cite current title as a preprint; venue not confirmed |
| Same work, different titles | MI9: "MI9 – Agent Intelligence Protocol" (v1/v2) versus "An integrated runtime governance framework" (current; also on OpenReview) | Cite current title |
| Author-name collision | "AgentTrust" (C. Yang, 2605.04785) versus a different 2026 preprint "AgentTrust: A self-improving trust layer for AI-agent actions" (2606.08539) | Only 2605.04785 is cited; the collision is flagged in the matrix |
| Wrong author | v2.0 attributes "Insuring every action" to "Chen, Z."; the author is H.-H. Chen (Hao-Hsuan Chen per search metadata) | Corrected |
| Wrong author initials | v2.0: She, Liang **Z.**, Kang **D.** (ProvenanceGuard); correct: Yining She, **Yiliang** Liang, **Eunsuk** Kang | Corrected |
| Conflicting numbers | ProvenanceGuard: v2.0 "42.9% → 1.8%, while reducing unnecessary interventions"; verified: **44.3% → 2.1%** on Agent-SafetyBench misaligned traces, with the intervention rate on aligned traces **rising** from 10.9% (baseline) to 14.5% | v2.0 figure and claim removed; DOCX figure retained; the intervention-cost trade-off is now reported |
| Conflicting numbers across versions | CaMeL: "67%" (earlier arXiv version) versus "77% versus 84% undefended" (current v2 abstract) | Current v2 figures used, with the version noted |
| Status upgrade | ShieldAgent and GuardAgent listed as arXiv/"accepted" in DOCX; both are **published** in ICML 2025, PMLR 267 | Upgraded to proceedings citations |
| Status not confirmed | ProbGuard "accepted to ASE 2026" (DOCX): acceptance not confirmed this session | Cited as preprint; flagged |

---

## 5. Repeated concepts (in the union of both versions)

- **"Indirect injection bypasses input-time inspection"** is stated in v2.0 §§2.3, 2.4.2, 2.5.1, 2.6, 2.12 and in DOCX §§2.3, 2.6. It should be stated once and then referenced.
- **"Deterministic enforcement answers permission, not risk"** appears in v2.0 §§2.7.1, 2.10.3, Q4 and DOCX §2.4.2.
- **Evaluation-metric non-comparability caveat** appears in v2.0 §2.10 and DOCX §2.1.1. It should be kept once in §2.1.
- **Detection/decision/mitigation separation** appears in v2.0 §2.7 intro, §2.10.4 and §2.11.

---

## 6. Missing topic areas (against the requested scope, §3 A–E)

| Required area | Coverage before merge | Gap |
|---|---|---|
| A. Multi-step attack propagation / action manipulation | Partial (Ruan; InjecAgent; ASB) | Adaptive-attack evidence against defenses (Zhan et al., 2025) missing; the AgentHarm benchmark is listed in v2.0 but never cited in the text |
| B. Runtime interception / policy enforcement foundations | Agent-specific only | No original runtime-enforcement source (e.g., Schneider, 2000, on execution monitoring) |
| C. Agent-specific defenses by mechanism | Good | Model-level defenses (e.g., StruQ) and goal/action-consistency monitors (Task Shield; MELON) missing |
| D. Behavioural and sequential analysis | Weak in DOCX (CUSUM mentioned in two sentences; anomaly-detection foundations dropped from v2.0) | No sequence-anomaly foundation (Forrest et al., 1996; Chandola et al., 2012); no CUSUM optimality source; no base-rate/operational caution specific to anomaly detection (Sommer & Paxson, 2010) |
| D. Calibrated probabilistic prediction | Good (Platt, Guo, Naeini, Kull) | Missing: the original logistic-regression source (Cox, 1958), isotonic calibration (Zadrozny & Elkan, 2002), and the empirical Platt-versus-isotonic comparison (Niculescu-Mizil & Caruana, 2005), although NEXUS itself compares Platt and isotonic |
| E. Financial AI-agent security | Thin: FinHarness; FinVault (withdrawn); Z. Chen et al. position paper | No systematization of financial/commerce agent execution risk (e.g., the SoK on agentic commerce, Mao et al., 2026) |

---

## 7. Weak synthesis areas, unsupported claims and outdated content

### 7.1 Unsupported or incorrect claims in v2.0 (not carried forward)
1. **The "empty per-factor attribution column" gap (v2.0 §2.8.3, Table 2.8, §2.11.2)** presented additive attribution as REM's distinguishing contribution. The DOCX correctly retracted this: linear/SHAP attribution is established (Lundberg & Lee, 2017), and NEXUS, AgentTrust and ShieldAgent provide auditable decision traces. **The v2.0 gap statement is superseded.**
2. **Jackson (2025) described as "near-isomorphic" four-verdict prior art for which REM "claims no novelty"**, while at the same time v2.0 claimed "attribution + calibration + ablation" as REM's novelty. The Jackson abstract (verified) confirms a multi-dimensional risk score feeding allow/deny/sanitize/escalate decisions. The full text was not accessed, so v2.0's claims that Jackson has "no documented calibration; no attribution; no ablation" are **not verifiable** and are not repeated.
3. **ProvenanceGuard figures and "reduces unnecessary interventions"**: incorrect (see §4).
4. **"MI9 reports 99.81% detection"** (v2.0 Q3): not re-confirmed; dropped.
5. **"ASB: memory poisoning lowest success, 7.92%"**: not re-confirmed; dropped.
6. **"LlamaFirewall AlignmentCheck reduces attack success by 83%; CodeShield 96% precision"**: not re-confirmed; dropped.
7. **"Thought-Aligner sub-100 ms latency"**: this figure appears in the arXiv v1 abstract; the current abstract says "low per-step latency". The chapter uses the current wording.
8. **"Chen, Chen, Chen & Sra identify ten overlooked categories including lack of interpretability"**: not in the current abstract; dropped.
9. **"FinVault: existing defences leave average ASR as high as 50%"** used as quantitative evidence: the source is **withdrawn**, so its numbers are not used as evidence.
10. **PRISMA-informed methodology claim** (v2.0 §2.1.1): no screening statistics exist. The DOCX correctly re-described the review as a structured narrative review.
11. **"Twelve tables… four quantitative traces"** rhetoric, and self-scored "88/100": removed as non-academic.
12. **Tables with ✓/△/✗ marks** (v2.0 Tables 2.4–2.10) mixed "not reported" with "not addressed" in several cells (e.g., ✗ for "risk evaluation" on CaMeL) and were not re-derivable from verified sources. They are replaced by one evidence-based table with NOT REPORTED / NOT APPLICABLE / NOT VERIFIED labels.

### 7.2 Claims in the DOCX needing adjustment
1. **Y. Wang et al. (2026)**: "higher capability can correlate with worse scores on safety measures" was not confirmed by the retrieved abstract, which reports a metric-validity failure and small-panel correlation instability (−0.64 at n = 7 to +0.02 at n = 18). Reworded to the verified findings.
2. **FinHarness evaluated on FinVault**: FinHarness's headline numbers (ASR 38.3% → 15.0%) were obtained on a benchmark that has since been withdrawn. This dependency is now stated explicitly.
3. **ShieldAgent / GuardAgent / Thought-Aligner** publication status: updated (see §4).
4. **Behavioural analysis** was thin (CUSUM in two sentences). It is expanded into a proper foundation section without redesigning REM.

### 7.3 Weak synthesis areas
- The DOCX §2.8 (Detection) and §2.4.3 (learned guardrails) overlap.
- The DOCX has no explicit **where-it-intervenes / what-it-observes** analysis (requested Steps 3–4).
- The comparison table (DOCX Table 2.2) lacks columns for threat focus, input/context monitoring, behavioural monitoring, multi-step awareness and main limitation, and it uses "—" for both NOT REPORTED and NOT APPLICABLE.

---

## 8. Prior-art collisions (retained, not minimized)

| Prior work | Overlap with REM | Status |
|---|---|---|
| **NEXUS** (Hossain et al., 2026) | Calibrated logistic-regression risk score (Platt; isotonic also evaluated); four interventions (allow / block / request confirmation / request revision); irreversibility feature; expected-loss objective; sub-millisecond latency | **Strongest collision.** REM cannot claim calibrated logistic scoring, a four-way intervention set, or consequence features. |
| **AgentTrust** (C. Yang, 2026) | Pre-execution interception of tool calls; four verdicts (allow / warn / block / review); session-level chain detection; LLM judge with a reversibility dimension; latency and component ablations | **Strong collision.** REM cannot claim interception, graduated verdicts with human review, or ablation with latency. |
| **Jackson** (2025, working paper) | Multi-dimensional risk score and allow / deny / sanitize / escalate decisions | Collision at the verdict-set level; full text unavailable. |
| **SafeAgent** (H. Liu et al., 2026) | Runtime controller plus stateful decision core with utility-cost and consequence modelling | Collision on the consequence-aware stateful decision; the mechanism differs (LLM-realized operators). |
| **H.-H. Chen** (2026) | Consequence pricing of each action before execution | Collision on consequence-aware gating; it does not estimate adversarial induction. |
| **FinHarness** (Jia et al., 2026) | Inline runtime protection for finance agents, with per-step tool monitoring | Collision on domain and position. |
| **C. Zhang et al.** (2026) | Shows that calibration does not repair control regret | Constrains REM's claims about calibration. |
| **ProvenanceGuard** (She et al., 2026) | Provenance of tool-call arguments as detection evidence | Constrains any novelty claim about provenance features. |

---

## 9. Current research-gap statement (DOCX §2.14) and assessment

> "Among the studies reviewed in this chapter, none reports an empirical evaluation of a non-invasive runtime layer for a financial tool-using agent that combines (i) provenance-based evidence about proposed financial actions, (ii) a calibrated per-step probability that the proposed action is adversarially induced, (iii) a decision that minimizes expected loss over Allow, Modify, Escalate, and Block using losses declared per consequence tier, and (iv) deterministic mitigation, with attack success, benign utility, intervention behavior, and latency measured separately and compared against a consequence-independent baseline that uses the same estimator."

**Assessment.** The statement is appropriately bounded, integrative and empirical, and it survives the prior-art checks above. It is retained in substance. Two refinements are needed:
- It should be derived from an explicit gap structure (integration; behavioural-evidence value; financial execution; evaluation), not simply stated.
- The phrase "none reports" should remain bounded to the reviewed corpus and the September 2026 cut-off.

**Unresolved items that this chapter must not resolve:**
- **SC-1 (mitigation semantics conflict):** SUPERVISOR DECISION REQUIRED.
- **SC-2 (tie-breaking conflict):** SUPERVISOR DECISION REQUIRED.
- **Backup algorithm identity:** the Algorithm Selection Study was not available. The chapter reviews CUSUM (sequential evidence accumulation) and beta/isotonic calibration as *established alternatives*, consistent with the DOCX. **Confirmation of which is the designated backup is required.**
