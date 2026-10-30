# Chapter 2: Systematic Review Audit and Final Consistency Check

**Date:** 25 September 2026.
**Scope:** `CHAPTER2_SYSTEMATIC_REVIEW.md` / `.docx` and the supporting files.
**Chapter 3 was not modified. SC-1 and SC-2 were not resolved.**

---

## 1. What was actually done

| Step | Performed? | Evidence | Limitation |
|---|---|---|---|
| Protocol (questions, criteria, concept blocks) | Yes | §2.2; review specification | Not registered; operational clarifications of I1/I3 made during screening and reported |
| Database search | Yes, **one database** (OpenAlex) | `slr/raw_search/Q*.json`; `search_call_log.tsv` | 11 named libraries and Elicit: DATABASE ACCESS UNAVAILABLE (`database_access_test_2026-09-25.txt`) |
| Search record (exact strings, dates, filters, counts) | Yes | `CHAPTER2_SYSTEMATIC_SEARCH_STRATEGY.md` | Boolean blocks not executable as Boolean; retrieval cap of 24–25 records per page |
| Deduplication | Yes, automated | `slr/tools/build_slr.py` | DOI/normalized-title rule; one manual duplicate |
| Title/abstract screening | Yes, 219 records | `CHAPTER2_SCREENING_LOG.csv` | Single reviewer |
| Full-text eligibility | **No**, record-level eligibility instead | Screening log; PRISMA diagram | Full texts not retrievable (network policy) |
| Other-methods stream | Yes, 70 records | Screening log (S01–S70) | Not independent of the author's prior reading |
| Quality appraisal | Yes, Q1–Q10 for 71 studies | `CHAPTER2_QUALITY_APPRAISAL.md` | Record-level; single appraiser; not a validated RoB tool |
| Data extraction | Yes, 21 fields for 71 studies | `CHAPTER2_SYSTEMATIC_EVIDENCE_MATRIX.csv` | Record-level; single extractor |
| PRISMA flow diagram | Yes, generated from counts | `CHAPTER2_PRISMA_FLOW_DIAGRAM.png` | — |
| Synthesis | Yes, 11 themes × 5 questions | §§2.4–2.12; Table 2.10 | Qualitative; no meta-analysis |
| Gap derivation after synthesis | Yes, candidates A–E assessed | §2.13.1; `CHAPTER2_RESEARCH_GAP_MAP.md` | Gap B not retained; A, C and E narrowed |
| PRISMA checklist | Yes | `CHAPTER2_PRISMA_CHECKLIST.md` | Items 2, 13f, 24a, 25 and 26 not met; items 6, 8, 9, 11 and others partial |

## 2. Integrity checks performed

1. **Counts.** All PRISMA and selection counts are computed by `build_slr.py` from the stored raw search output and the decisions file (`slr/prisma_counts.json`). The script asserts that the stored deduplicated order matches the recomputation, and that the number of included database studies equals the number of eligibility "Include" decisions.
2. **Numbers in the chapter.** Every numeric string in the chapter body was matched against the evidence base: `slr_data.py`, `tools/sources.py`, the search strategy and the computed counts. Only three strings were unmatched, and all three are Chapter 3 section references (3.1.2, 3.1.3, 3.13).
3. **Citations and references.** Every one of the 100 references is cited in the body. No in-text citation lacks a reference entry, apart from a date string caught by the automated check, which is not a citation.
4. **Disambiguation.** Same-surname citations were disambiguated: J. Lin (VIGIL) versus W. Lin (DreamGuard); T. Shi (Progent) versus J. Shi (ToolHijacker); Zhu, Yang, et al. (MELON) versus Zhu, Zhang, et al. (SafeScientist).
5. **No invented material.** No study, count, screening decision, quality score or number was invented. Where the record did not show a property, it is coded "Not Verified", not "Yes".
6. **Verification labels.** Nine included studies are PARTIALLY VERIFIED: AgentTrust, NEXUS, ProvenanceGuard, MI9, SafeAgent, C. Zhang et al., Jackson, VIGIL and R-Judge. None was promoted.
7. **FinVault.** It is cited only as withdrawn. FinHarness is downgraded to LIMITED EVIDENCE by a documented override.
8. **Metadata corrections from Crossref:**
   - ACE's first author is Evan Li (the index had "Enlai Li");
   - PromptShield's Crossref issued year is 2024, while it was published online in 2025 in the CODASPY '25 proceedings (recorded in the reference);
   - the AgentDojo index record R016 is corrupted and was excluded as a metadata conflict.
9. **Author lists.** Author lists for 13 arXiv-only records identified by the database search are abbreviated and marked as such in the references.

## 3. Final consistency audit

**Sources compared:**
- Chapter 3: `REM_STAGE2_INPUT_PACKAGE/working/Chapter3_working.md` on branch `claude/rem-algorithm-implementation-3ktvze`;
- `CLAUDE.md`;
- the Stage 2 final decision report;
- the implementation (`rem/`);
- the previous integrated Chapter 2 and its reference register.

| Item | Chapter 2 (systematic review) | Reference source | Status |
|---|---|---|---|
| REM definition | Runtime mediation layer between a financial tool-using agent and its environment | Chapter 3 §3.2.1 | Consistent |
| Five-layer architecture | Input & Context; Detection; Behavioral Analysis; Decision Engine; Mitigation; no sixth layer | Chapter 3 §3.2.1; `CLAUDE.md` FROZEN ARCHITECTURE | Consistent |
| Primary algorithm | Adopted methods named; REM's own specification deferred to Chapter 3; no REM pseudocode or verdict equation reproduced | `CLAUDE.md` FROZEN REM PIPELINE | Consistent (overlap with Chapter 3 minimized) |
| Calibrator | Platt on the logit adopted; beta, isotonic and temperature reviewed and **not adopted** | `CLAUDE.md` forbidden reintroductions; `rem/algorithms/calibration/platt.py` | Consistent |
| CUSUM | Optional, offline, observe-only; not in the verdict path | `CLAUDE.md`; `rem/core/interfaces.py` | Consistent |
| Attribution | Audit-only; never used for the verdict | `CLAUDE.md` MATHEMATICAL LOCK | Consistent |
| Elkan / Chow | Support the expected-cost principle and reject-style escalation; "neither source proposed REM's four-action architecture" | `CLAUDE.md` | Consistent |
| Equations | Three generic equations only: logistic (2.1), Platt's original form (2.2), Elkan's minimum expected cost (2.3). ECE, CUSUM and Shapley are described in words. | Chapter 3 §3.7 | Consistent. **Note:** Eq. 2.2 uses Platt's sign convention exp(As + B). Chapter 3 writes σ(γ₁s + γ₀) with γ₁ > 0, which is equivalent with A = −γ₁, B = −γ₀. |
| Verdict terminology | Allow, Modify, Escalate, Block | Chapter 3; `rem/core/results.py` | Consistent |
| Research objectives | O1–O3 quoted from Chapter 3 §3.1.2; RQ1–RQ4 [PD] | Chapter 3 §§3.1.2–3.1.3 | Consistent. The proposal/RQ inconsistency is recorded, not resolved. |
| Research gap | Integrative and empirical; clause (iv) aligned to Chapter 3 wording ("measured and used in the loss structure"); adds that calibration is reported separately from control | Chapter 3 §3.13 | Consistent. The calibration clause corresponds to RQ1 [PD]. |
| Novelty claims | No mechanism claimed as novel; only the combination and the evaluation design | Chapter 3 Table 3.16 | Consistent. **Recommendation:** Chapter 3 Table 3.16 does not list the new HIGH-EVIDENCE prior art found by the systematic search. The author should consider adding the MCP policy-enforcement point (S. Wang et al., 2026), LATTICE (Calboreanu, 2026), RTBAS (Zhong et al., 2025) and ACE (E. Li et al., 2026). **Chapter 3 was not modified.** |
| AgentTrust | Explicit comparison; PV details flagged | Chapter 3 Table 3.16 cites C. Yang (2026) | Consistent |
| NEXUS | Explicit comparison; fixed costs and cascade flagged PV | Chapter 3 Table 3.16 cites Hossain et al. (2026) | Consistent |
| FinHarness citation | "H. Jia et al. (2026)" | Chapter 3 Table 3.16 writes "Jia et al. (2026)" | **Minor inconsistency.** It is ambiguous with F. Jia et al. (2025, Task Shield). Suggest "H. Jia et al. (2026)" in Chapter 3. Not modified. |
| Financial-agent scope | AgentDojo Banking; general versus financial evidence separated | Chapter 3 §3.1.2 | Consistent |
| SC-1 (mitigation semantics) | Unresolved: "Chapter 3: episode-level Modify/Block; implementation: step-level semantics; SUPERVISOR DECISION REQUIRED" | `rem/core/mitigation.py` (DeterministicMitigationEngine applies the canonical mechanism "at step level") | Unresolved, as required |
| SC-2 (tie-breaking) | Unresolved: "Chapter 3: Block ≥ Escalate ≥ Modify ≥ Allow; prototype: VerdictTieError; SUPERVISOR DECISION REQUIRED" | `rem/algorithms/decision/expected_loss.py` (VerdictTieError) | Unresolved, as required |
| Approved proposal | Objectives taken as quoted in Chapter 3 ("as approved in the research proposal") | Proposal file not present in the workspace | **Could not be checked directly** |
| Decision Ledger | Not relied on | Stage 2 final report lists the Decision ledger as "MISSING" | **Could not be checked (source missing)** |
| Existing reference register (S01–S70) | All 70 classified: 31 included, 11 cross-stream duplicates, 21 foundational/methodological, 6 background, 1 withdrawn | `tools/sources.py` | Consistent. Perez & Ribeiro (2022) and Inan et al. (2023) are no longer cited in the chapter body; they remain in the register as background. |

## 4. Cross-references from other chapters (not modified)

Chapter 1 and Chapter 5 cite section numbers of the September DOCX version of Chapter 2. Under the systematic-review structure, the cited content is now located as follows:

| Citing location | Cited content | Old section | Section in systematic review |
|---|---|---|---|
| Chapter 1, line 16 | Moment a proposed action crosses into the environment | 2.1 | 2.1 |
| Chapter 1, line 28 | Results depend on benchmark; cannot be pooled | 2.3 | 2.5 (benchmarks); 2.2.8 (no pooling) |
| Chapter 1, line 30 | Last point at which an action can be prevented | 2.6 | 2.4 (Themes 1–2 synthesis); 2.6 |
| Chapter 1, line 32 | Two questions the literature leaves open | 2.10 | 2.12; 2.13.1 |
| Chapter 1, line 43 | Financial exposure of transfers and credentials | 2.7 | 2.10 |
| Chapter 1, lines 51, 59, 68 | Mechanisms present in prior work; gap statement | 2.14 | 2.13.2–2.13.3 |
| Chapter 5, line 105 | Each mechanism has precedent | 2.13 | 2.13.3 (Table 2.12) |
| Chapter 5, line 217 | Regulatory recording and oversight | 2.7 | 2.10.3 |

**Caution.** The new numbering reuses 2.6 and 2.10 for different content (defenses and financial evidence). Chapter 1's "Section 2.10" reference for the open questions would now point to the wrong section. These references must be updated when the systematic review replaces the chapter. They were not edited here.

## 5. Differences from the integrated narrative version (`CHAPTER2_LITERATURE_REVIEW_INTEGRATED.md`)

| Aspect | Integrated narrative version | Systematic review version |
|---|---|---|
| Review type | Structured narrative review | Systematic review with structured qualitative synthesis (PRISMA 2020 / PRISMA-S) |
| Evidence base | 70 references, selected narratively | 71 included studies (40 from the database, 31 via other methods), plus 21 foundational/methodological sources, 7 cited background sources (9 records classified as background) and 1 withdrawn source (100 references) |
| New included studies | — | 32 studies not in the previous chapter: MCP policy-enforcement point, LATTICE, RTBAS, ACE, IsolateGPT, VIGIL, ToolSafe, DRIFT, InstructDetector, PromptShield, Y. Chen et al. (attack-technique defense), ToolHijacker, AgentVigil, web-navigation IPI demonstration, ClawSafety, R-Judge, MCP threat-modelling study, MCP server study, Breaking Agents, AI², Imprompter, SkillJect, GoEX, Kaptein et al., constitutional monitors, semantic firewall (finance), AHI analysis, HouYi, LLMSmith, P2SQL, SafeScientist, f-secure |
| Equations | Six | Three (overlap with Chapter 3 reduced) |
| Gap | Four gaps | Candidate gaps A–E assessed. B not retained; A, C and E narrowed; D retained. New conflicting evidence on provenance contribution (26.4-point effect) and on confidence thresholds (LATTICE). |
| Comparative tables | Tables 2.6–2.7 (narrative selection) | Tables 2.8–2.9 generated from the evidence matrix (42 defense/design studies) |

**Preserved strong content** (revalidated against the systematic evidence):
- the agent security transition;
- the threat taxonomy;
- benchmark analysis;
- the intervention-point taxonomy;
- runtime monitoring;
- trajectory and provenance discussion;
- algorithmic foundations (condensed);
- the AgentTrust and NEXUS analyses;
- financial-agent context;
- critical synthesis and gap reasoning.

## 6. Outstanding actions (not performed; require the author or supervisor)

1. Search IEEE Xplore, the ACM DL, Scopus or Web of Science, the ACL Anthology and arXiv directly with the Boolean blocks, then update the PRISMA flow.
2. Obtain full texts through institutional access and re-appraise Not Verified items. Resolve the PARTIALLY VERIFIED labels, starting with AgentTrust and NEXUS.
3. Optionally, have a second reviewer screen a sample and report agreement.
4. Update the Chapter 1 and Chapter 5 cross-references (Section 4 above).
5. Consider adding the new HIGH-EVIDENCE prior art to Chapter 3 Table 3.16, and "H." to the FinHarness citation. This is a Chapter 3 change and was not made here.
6. SC-1 and SC-2: SUPERVISOR DECISION REQUIRED (unchanged).
