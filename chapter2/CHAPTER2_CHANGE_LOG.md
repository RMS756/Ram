# Chapter 2: Change Log (merge of v2.0 July 2026 and September 2026 DOCX into the integrated version)

**Baseline.** The September 2026 DOCX (`Chapter2_Literature_Review.docx`) is the current baseline. The July v2.0 draft (`REM_Chapter2_Literature_Review_v2.0.md`; also printed as `chapter_2_v2.pdf`) was mined for retained material.

**Unchanged by design.** Chapter 3 was not modified. The five REM layers (Input & Context, Detection, Behavioral Analysis, Decision Engine, Mitigation) are preserved, and no sixth layer is introduced. **SC-1 (mitigation semantics conflict)** and **SC-2 (tie-breaking conflict)** remain **SUPERVISOR DECISION REQUIRED**: Chapter 2 refers the operational semantics of Modify and the tie-breaking rule to Chapter 3 (§2.12.3) and does not define either.

---

## 1. Structural changes

| Integrated section | Derived from | Type of change |
|---|---|---|
| 2.1 Introduction and review approach | DOCX 2.1 + v2.0 2.1 | **Rewritten.** Kept the DOCX "structured narrative review" description and dropped v2.0's PRISMA claim (no screening statistics exist). Added the eight-step argument, the source hierarchy, and the NOT REPORTED / NOT APPLICABLE / NOT VERIFIED convention. |
| 2.2 AI agents and emerging security risks | DOCX 2.2 + v2.0 2.2–2.3 | **Merged.** v2.0's six-characteristics and lifecycle material condensed into three structural properties; Toolformer and the Yu et al. survey retained from v2.0; CoT, Reflexion, RAG, InstructGPT and Constitutional AI removed as generic capability background. |
| 2.3 Threats against AI agents | DOCX 2.3 + v2.0 2.4 | **Merged and rewritten.** v2.0's 12-class taxonomy reduced to the classes relevant to REM (jailbreak, multi-agent and pure data-exfiltration subsections dropped). New subsections: 2.3.6 abnormal/repetitive execution and 2.3.7 adaptive attackers. Table 2.1 rebuilt. |
| 2.4 Benchmarks and threat models | DOCX 2.12 | **Moved earlier and expanded.** Added AgentHarm (listed in v2.0 but never cited) and a threat-model column. FinVault is reported as withdrawn only. Benchmark-validity audits and Arp et al. are consolidated here. |
| 2.5 Defensive approaches | DOCX 2.4.1–2.4.3, 2.8 + v2.0 2.7.1–2.7.2 | **Reorganized by intervention point.** New Table 2.3 (where defenses intervene and what they observe). New subsections: model-level defenses (StruQ) and goal–action consistency (Task Shield, MELON, ProvenanceGuard). The execution-monitoring foundation (Schneider, 2000) was added. |
| 2.6 Runtime monitoring and behavioral analysis | DOCX 2.5 + v2.0 2.6 | **Substantially expanded.** Step- vs sequence-level monitoring; provenance as behavioral evidence; classical foundations (Forrest et al.; Chandola et al. 2009 and 2012; Sommer & Paxson); evidence on the empirical value of trajectory components. |
| 2.7 Statistical and algorithmic foundations | DOCX 2.9, 2.10 (decision part), 2.11 (attribution part) | **Consolidated into one algorithm section** covering logistic regression, calibration, the limits of calibration, CUSUM, expected-cost decisions and additive attribution. Six sourced equations (2.1–2.6) and Table 2.4 added. |
| 2.8 Runtime security and mitigation | DOCX 2.4.4, 2.6, 2.10 + v2.0 2.7.3 | **Rewritten.** New Table 2.5 (response types and decision granularity). Separate, detailed subsections for AgentTrust (2.8.3), NEXUS (2.8.4) and Jackson (2.8.5); consequence-aware control (2.8.6); transactional mitigation (2.8.7). |
| 2.9 Financial AI-agent security | DOCX 2.7 + v2.0 2.9 | **Rewritten.** SoK on agentic commerce added; FinHarness's dependency on the withdrawn FinVault made explicit; EU AI Act retained; R1–R6 retained, with R6 extended to calibration and latency. |
| 2.10 Comparative analysis | DOCX 2.13 (Table 2.2) + v2.0 2.10 (Tables 2.3–2.12) | **Replaced.** v2.0's twelve ✓/△/✗ tables and DOCX Table 2.2 were replaced by two evidence-based tables (2.6 capability; 2.7 decision mechanism) that use NOT REPORTED / NOT APPLICABLE / NOT VERIFIED. The REM row is clearly labeled as design, not result. |
| 2.11 Critical synthesis | New (draws on DOCX 2.13 text) | **New section:** well addressed / fragmented / where approaches stop / promising combinations / recurring limitations / missing evidence / implication. |
| 2.12 Research gap and positioning | DOCX 2.14–2.15 | **Rewritten.** Four-part derived gap; DOCX gap statement retained in substance (calibration added to the measured quantities); positioning expanded (AgentTrust, NEXUS, ProvenanceGuard/Task Shield/MELON, CUSUM); new Table 2.8 (adopted vs contribution); Table 2.9 (requirements → Chapter 3). |
| 2.13 Chapter summary | DOCX 2.16 | **Rewritten.** |
| v2.0 §2.8 Explainable AI (whole section) | v2.0 | **Removed as a section.** Its only load-bearing element (additive attribution) moved to §2.7.6, where it is presented as an established audit technique. |
| v2.0 "Potential examiner questions" and "Quality report" (self-score 88/100) | v2.0 | **Removed.** Not chapter content; the self-assessment was unsupported. |

---

## 2. Sources retained (55 of 80 existing works)

**From both drafts (30):** L. Wang 2024; Yao 2023; Ruan 2024; OWASP; Y. Liu 2024; Greshake 2023; Zhan 2024; H. Zhang 2025 (ASB); Z. Chen 2024 (AgentPoison); Debenedetti 2024 (AgentDojo); Arp 2022; Chennabasappa 2025; Shi 2025 (Progent); H. Wang 2026 (AgentSpec); Debenedetti 2025 (CaMeL); Xiang 2025 (GuardAgent); Z. Chen, Kang & Li 2025 (ShieldAgent); Luo 2025 (AGrail); Jiang 2025 (Thought-Aligner); She 2026 (ProvenanceGuard); C. L. Wang 2025 (MI9); F. Li 2026 (PRISM); H. Wang 2025 (ProbGuard/Pro2Guard); Jackson 2025; H.-H. Chen 2026; Z. Chen 2026 (Cordon); Lundberg & Lee 2017; Z. Chen, J. Chen et al. 2025; H. Jia 2026 (FinHarness); Z. Yang 2026 (FinVault, withdrawn).

**From the DOCX only (17):** Basseville & Nikiforov 1993; Chow 1970; Elkan 2001; EU AI Act 2024; Guo 2017; Hines 2024; Hossain 2026 (NEXUS); Kull 2017; M. Q. Li 2026; Lin 2026 (DreamGuard); H. Liu 2026 (SafeAgent); Naeini 2015; E. S. Page 1954; Platt 1999; Y. Wang 2026; C. Yang 2026 (AgentTrust); C. Zhang 2026.

**From v2.0 only (8), restored:** Andriushchenko 2025 (AgentHarm), which was listed in v2.0 but never cited and is now used in §2.3.3 and §2.4; Chandola 2009 (anomaly taxonomy, needed for §2.6.3); Hua 2024 (TrustAgent, plan-level intervention point); Inan 2023 (Llama Guard, input/output classifier family); Perez & Ribeiro 2022 (early direct injection); Schick 2023 (Toolformer, learned tool calling); Tsai & Bagdasarian 2025 (Conseca, contextual policy); Yu 2025 (component-level threat survey).

---

## 3. Sources removed (25) and why

| Removed source | Reason (Source Rules 6, 8, 16, 17) |
|---|---|
| Anwar et al. 2024 | Generic alignment-assurance claim; not needed for the REM argument |
| Bai et al. 2022 (Constitutional AI) | Generic alignment background |
| Ouyang et al. 2022 (InstructGPT) | Generic alignment background |
| Lewis et al. 2020 (RAG) | Generic capability background; memory risk covered by AgentPoison |
| Shinn et al. 2023 (Reflexion) | Generic capability background |
| J. Wei et al. 2022 (Chain-of-thought) | Generic capability background |
| A. Wei et al. 2023 (Jailbroken) | Jailbreak is outside the REM threat model (malicious *user*); AgentHarm covers the contrast |
| Zou et al. 2023 (GCG) | Same as above; preprint |
| Khan et al. 2024 | Preprint taxonomy; superseded by the peer-reviewed Yu et al. 2025 |
| Syros et al. 2026 (SAGA) | Multi-agent security is outside the thesis scope |
| Neelou et al. 2025 (A2AS) | Preprint; no substantive claim used in v2.0 beyond a classification row |
| Rebedea et al. 2023 (NeMo Guardrails) | Dialogue-level rails; Llama Guard suffices as the message-level representative (metadata verified) |
| Han et al. 2024 (WildGuard) | Message-level moderation; redundant with Llama Guard |
| Zeng et al. 2024 (ShieldGemma) | Same; preprint |
| Liang et al. 2025 (SafeRAG) | RAG-specific; context manipulation covered by AgentPoison and Greshake |
| Xie et al. 2024 (FinBen) | Financial *capability* benchmark; the task forbids a generic financial-AI review |
| H. Li et al. 2025 (InvestorBench) | Same |
| Ribeiro et al. 2016 (LIME) | The XAI section was removed; only additive attribution is needed |
| Guidotti et al. 2018 | Same |
| Barredo Arrieta et al. 2020 | Same |
| Doshi-Velez & Kim 2017 | Same; preprint |
| Capuano et al. 2022 | Same |
| Moustafa et al. 2023 | Same; also **never verified** (volume/pages) |
| NIST AI RMF 2023 | Not needed; the EU AI Act provisions suffice for the audit and oversight motivation (NIST is still mentioned inside the Jackson summary as that paper's framing, without a separate citation) |
| M. J. Page et al. 2021 (PRISMA 2020) | The review is not PRISMA-conformant; the claim was removed |

**Cross-version duplicate or variant entries merged (8):** Pro2Guard/ProbGuard; "Chen, Z. (2026)"/H.-H. Chen; the placeholder Cordon, FinHarness, FinVault, She and Jiang entries; and the two OWASP entries.

---

## 4. Sources newly added (13) and why

| New source | Why it was added (the gap it closes) | Section |
|---|---|---|
| Zhan et al. 2025 (NAACL Findings), *Adaptive attacks break defenses…* | Evidence that detector results are upper bounds under adaptive attack; the review previously had no adaptive-attack evidence | 2.3.7; 2.5 |
| S. Chen et al. 2025 (USENIX Sec), StruQ | Required model-level intervention point (Step 3) | 2.5.2 |
| F. Jia et al. 2025 (ACL), Task Shield | Goal–action consistency defense; peer-reviewed, on AgentDojo | 2.5.5; 2.6.2 |
| Zhu et al. 2025 (ICML), MELON | Tool-call-level IPI detection by masked re-execution; peer-reviewed | 2.5.5; 2.6.2 |
| Schneider 2000 (ACM TISSEC) | Original source for runtime enforcement by execution monitoring (Source Rule 2) | 2.5.3 |
| Forrest et al. 1996 (IEEE S&P) | Original behavioral anomaly detection over action (system-call) sequences | 2.6.3 |
| Chandola et al. 2012 (IEEE TKDE) | Sequence-anomaly problem formulations for the Behavioral Analysis Layer | 2.3.6; 2.6.3 |
| Sommer & Paxson 2010 (IEEE S&P) | Operational cautions for anomaly detection in security, complementing Arp et al. | 2.6.3 |
| Lorden 1971 (Ann. Math. Stat.) | Optimality property of CUSUM (the strength of the alternative method) | 2.7.4 |
| Cox 1958 (JRSS-B) | Original source for logistic regression (Source Rule 2; Eq. 2.1) | 2.7.1 |
| Zadrozny & Elkan 2002 (KDD) | Original isotonic calibration; NEXUS evaluates isotonic | 2.7.2 |
| Niculescu-Mizil & Caruana 2005 (ICML) | Empirical Platt-versus-isotonic comparison; justifies the data-size trade-off | 2.7.2 |
| Mao et al. 2026 (SoK, preprint) | Financial execution-risk systematization (transaction authorization); fills the financial-context gap | 2.9.1 |

Candidates considered and not added, to avoid reference bloat: SecAlign (redundant with StruQ); DataSentinel (input-level detection already represented); the Brier (1950) score (not needed for the argument); Wald (1945) SPRT (CUSUM is adequately sourced by Page, Basseville & Nikiforov, and Lorden); EWMA control charts; SHADE-Arena; IPIGuard; DRIFT.

---

## 5. Content corrections (claims changed, and why)

| # | Earlier claim | Corrected treatment | Reason |
|---|---|---|---|
| 1 | v2.0: REM's distinguishing contribution is additive per-factor attribution (the "empty column" in Table 2.8) | Attribution is an established audit technique, not a contribution (§2.7.6) | Lundberg & Lee (2017); audit traces exist in NEXUS, AgentTrust, ShieldAgent and PRISM; the DOCX had already retracted it |
| 2 | v2.0: ProvenanceGuard 42.9% → 1.8% "while reducing unnecessary interventions" | 44.3% → 2.1%; intervention rate rose from 10.9% to 14.5% | Primary source |
| 3 | v2.0: ProvenanceGuard authors "She, [initials], Liang, Z., & Kang, D." | She, Y., Liang, Y., & Kang, E. | Primary source |
| 4 | v2.0: "Chen, Z. (2026) Insuring every action" | H.-H. Chen (2026) | arXiv metadata |
| 5 | v2.0: Pro2Guard | ProbGuard (renamed); cited as a preprint (ASE acceptance not confirmed) | arXiv versions |
| 6 | DOCX: ShieldAgent and GuardAgent as preprints | ICML 2025, PMLR 267 | Proceedings |
| 7 | DOCX: Y. Wang et al. "higher capability can correlate with worse safety scores" | Metric-validity failure and small-panel instability | Abstract |
| 8 | v2.0: FinVault's "up to 50.0% residual ASR" used as evidence | Not used; cited only as withdrawn | Withdrawal confirmed |
| 9 | DOCX: FinHarness results reported without noting their substrate | The dependency on the withdrawn FinVault is stated | Evidence integrity |
| 10 | v2.0: LlamaFirewall 83% / 96%; ASB memory poisoning 7.92%; MI9 99.81%; Thought-Aligner sub-100 ms; the Chen–Sra "ten categories incl. interpretability" | Removed or reworded | Not re-confirmed in this pass (Source Rule 9) |
| 11 | v2.0: Jackson "no documented calibration; no attribution; no ablation" | Not repeated; recorded as NOT VERIFIED | Only the abstract was accessible |
| 12 | v2.0: Jackson's pipeline "near-isomorphic", and at the same time REM novelty in attribution + calibration + ablation | Jackson recorded as verdict-set prior art; REM's claim is integrative and empirical only | Consistency with the prior-art evidence |
| 13 | DOCX: AgentSpec "95.56% precision / 70.96% recall" for LLM-generated rules | Omitted | Not re-confirmed in this pass; not needed |
| 14 | DOCX: ShieldAgent/GuardAgent performance percentages | Omitted | Not re-confirmed; not needed for the argument |
| 15 | v2.0 and DOCX: CaMeL 77% vs 84% | Retained, with the version note (earlier version: 67%) | Version conflict recorded |
| 16 | DOCX gap statement: measured "attack success, benign utility, intervention behavior, and latency" | "…intervention behavior, calibration and latency" | Consistent with the DOCX's own §2.9 and §2.15 (calibration reported separately) and with C. Zhang et al. (2026) |
| 17 | DOCX R6: "security measured together with benign task utility" | Extended to include latency and calibration | Same reason as #16 |
| 18 | v2.0 Tables 2.4–2.10: ✓/△/✗ marks, including ✗ where the source was merely silent | Replaced by explicit labels | Task §18 |
| 19 | v2.0: "no system… provides X" framed as a universal negative in places | All gap claims bounded: "the reviewed literature provides limited evidence…" | Task §13; Source Rule 15 |
| 20 | v2.0: British spelling | American spelling throughout, matching the DOCX baseline | Consistency |

---

## 6. Items explicitly *not* changed

- Chapter 3 (not modified; its section cross-references in Table 2.9 are carried over from the DOCX and should be re-checked against the current Chapter 3).
- The REM architecture: five layers, the Allow / Modify / Escalate / Block verdict set, tier-indexed losses, provenance features in the Behavioral Analysis Layer, and linear attribution restricted to the audit record.
- **SC-1** (mitigation semantics) and **SC-2** (tie-breaking): **SUPERVISOR DECISION REQUIRED**.
- The primary algorithm: the per-step calibrated estimator with the expected-loss decision, as described in the DOCX. CUSUM and the alternative calibration methods (beta, isotonic) are reviewed as *established alternatives* and are not presented as replacements. **The identity of the designated "backup algorithm" could not be confirmed**, because the REM Algorithm Selection Study was not available to this merge.
