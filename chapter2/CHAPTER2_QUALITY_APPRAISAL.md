# Chapter 2: Quality Appraisal of Included Studies

**Studies appraised:** 71 (all included studies; none excluded on quality).
**Appraiser:** single reviewer, 25 September 2026.
**Evidence base:** the accessible record only. That means the index abstract and metadata, Crossref metadata, and for other-methods studies the verification record in `CHAPTER2_REFERENCE_EVIDENCE_MATRIX.md`. **No full text was read** during this appraisal, because full texts were not retrievable in the review environment (see `CHAPTER2_SYSTEMATIC_SEARCH_STRATEGY.md` §1).
**Consequence:** the appraisal measures **how much of each study's evidence could be verified**, not the intrinsic quality of the study. A peer-reviewed paper whose abstract gives no figures can receive LIMITED EVIDENCE here and a higher category after full-text appraisal.

## 1. Checklist (the protocol's ten questions)

| Item | Question | Coding rule used |
|---|---|---|
| Q1 | Is the research objective clearly stated? | Y if the record states the aim; otherwise NV |
| Q2 | Is the threat model clearly defined? | Y if the attacker capability or threat class is named (e.g., indirect injection through tool outputs); NA for meta-research; otherwise NV |
| Q3 | Is the proposed method sufficiently described? | Y if the record describes the method at component level (record-level judgement only) |
| Q4 | Is the evaluation methodology reproducible? | Y only if code, data or benchmark release is stated in the record; otherwise NV |
| Q5 | Are the dataset, benchmark or task characteristics reported? | Y if a named benchmark or quantified dataset is given; NA for design or formal papers without evaluation; otherwise NV |
| Q6 | Are the evaluation metrics appropriate and clearly defined? | Y if named metrics (ASR, utility, accuracy, ECE, latency…) are reported; otherwise NV/NA |
| Q7 | Are baselines or comparators described? | Y if a comparison with defenses, baselines, models or configurations is stated; NA for measurement studies without a comparator by design |
| Q8 | Are limitations or failure cases discussed? | Y if the record states a limitation or failure case (e.g., a rule-coverage gap or overfitting); otherwise NV |
| Q9 | Are quantitative claims supported by reported evidence? | Y if the record reports the figures behind its claims; NV if claims are qualitative only; NA if the study makes no quantitative claim |
| Q10 | Is the work peer-reviewed or otherwise appropriately identified? | Y peer-reviewed venue (verified via Crossref/DOI or the prior register); P preprint or working paper clearly labelled as such; N neither |

Codes: **Y** = Yes, **N** = No, **P** = partially (Q10 only), **NV** = Not Verified (not visible in the accessible record), **NA** = Not Applicable.

## 2. Evidence categories and the deterministic rule

No numeric quality score is computed. Each study's category follows from its codes by a fixed rule, implemented in `slr/tools/build_slr.py`, function `category`:

- **HIGH EVIDENCE:** Q10 = Y **and** Q9 = Y **and** Q5 = Y **and** Q7 ∈ {Y, NA}. A peer-reviewed study that reports its benchmark or dataset, its figures, and its comparator (or needs none).
- **MODERATE EVIDENCE:** not HIGH, **and** either (Q9 = Y and Q10 ∈ {Y, P}) or (Q10 = Y and Q5 = Y). Quantitative evidence in a peer-reviewed or clearly labelled preprint record, or a peer-reviewed evaluation whose figures are not in the record.
- **LIMITED EVIDENCE:** all other cases. No verifiable quantitative evaluation in the accessible record, or a design, position or working paper.

**Override (one study).** FinHarness (P71) meets the MODERATE rule but is set to **LIMITED EVIDENCE**, because every reported figure was measured on FinVault, a withdrawn benchmark. The protocol (§29) forbids using withdrawn FinVault as affirmative evidence.

**Verification status is recorded separately and is not merged into the category.** A study can hold HIGH EVIDENCE while being PARTIALLY VERIFIED: its abstract was obtained only through search-engine text (VIGIL, R-Judge), or specific body-text figures rest on tier-7 excerpts (AgentTrust, NEXUS, ProvenanceGuard, MI9, SafeAgent, C. Zhang et al., Jackson). In the synthesis, PARTIALLY VERIFIED figures are always flagged, and no gap relies on them alone.

## 3. Summary

| Measure | Count |
|---|---:|
| HIGH EVIDENCE | 10 |
| MODERATE EVIDENCE | 36 |
| LIMITED EVIDENCE | 25 |
| Peer-reviewed (Q10 = Y) | 36 |
| Preprint or working paper (Q10 = P) | 35 |
| FULLY VERIFIED (metadata and cited contribution) | 62 |
| PARTIALLY VERIFIED | 9 |
| Studies with Q4 (reproducibility) = Y | 9 |
| Studies with Q8 (limitations) = Y | 9 |

**Patterns relevant to the synthesis.**

1. **Reproducibility is rarely verifiable from the record.** Q4 is NV for most studies. This reflects abstract-level appraisal as much as the studies themselves.
2. **Limitations are rarely stated in abstracts** (Q8). The studies that state them are among the most informative for REM: AgentTrust (session tracker had no measurable effect), NEXUS (in-distribution upper bounds), the MCP policy-enforcement point (a rule-coverage gap on one backend), LATTICE (zero false-allow only at an operating point that auto-allowed nothing) and constitutional monitors (saturation and overfitting).
3. **About half the corpus is preprints.** They include most of the closest prior art (AgentTrust, NEXUS, ProvenanceGuard, FinHarness, Progent, CaMeL).
4. **The only included primary studies coded Financial Context = Yes** are a peer-reviewed but LIMITED study (semantic firewall for a banking RAG chatbot, P32), a design preprint (P67, partial), a position paper (P70) and a study evaluated on a withdrawn benchmark (P71). Financial evidence is therefore thin in quality, not only in quantity.

## 4. Appraisal table

| ID | Study | Role | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 | Verification | Evidence level |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P01 | F. Jia et al. (2025) | Defense | Y | Y | Y | NV | Y | Y | Y | NV | Y | Y | FULLY VERIFIED | HIGH EVIDENCE |
| P02 | Z. Wang et al. (2025) | Attack | Y | Y | Y | NV | Y | Y | Y | NV | Y | Y | FULLY VERIFIED | HIGH EVIDENCE |
| P03 | Wen et al. (2025) | Defense | Y | Y | Y | Y | Y | Y | NV | NV | Y | Y | FULLY VERIFIED | MODERATE EVIDENCE |
| P04 | C. Huang et al. (2026) | Threat analysis | Y | Y | Y | NV | Y | NV | NA | NV | NA | Y | FULLY VERIFIED | MODERATE EVIDENCE |
| P05 | Johnson et al. (2025) | Attack | Y | Y | Y | Y | NV | NV | NV | NV | NV | Y | FULLY VERIFIED | LIMITED EVIDENCE |
| P06 | Zhong et al. (2025) | Defense | Y | Y | Y | NV | Y | Y | NV | NV | Y | P | FULLY VERIFIED | MODERATE EVIDENCE |
| P07 | P. Wang, Li, & Tian (2026) | Analysis | Y | NV | Y | NV | Y | NA | NA | NV | Y | P | FULLY VERIFIED | MODERATE EVIDENCE |
| P08 | F. Wu, Cecchetti, & Xiao (2024) | Defense | Y | Y | Y | Y | NV | NV | NV | NV | NV | P | FULLY VERIFIED | LIMITED EVIDENCE |
| P09 | Fu et al. (2024) | Attack | Y | Y | Y | NV | Y | Y | NV | NV | Y | P | FULLY VERIFIED | MODERATE EVIDENCE |
| P10 | Patil et al. (2024) | Design | Y | NV | Y | Y | NA | NA | NA | NV | NA | P | FULLY VERIFIED | LIMITED EVIDENCE |
| P11 | Lin et al. (2026) | Defense | Y | Y | Y | NV | Y | Y | Y | NV | Y | Y | PARTIALLY VERIFIED | HIGH EVIDENCE |
| P12 | E. Li et al. (2026) | Defense | Y | Y | Y | NV | Y | NV | Y | NV | NV | Y | FULLY VERIFIED | MODERATE EVIDENCE |
| P13 | T. Liu et al. (2023) | Threat analysis | Y | Y | Y | NV | Y | Y | NA | NV | Y | P | FULLY VERIFIED | MODERATE EVIDENCE |
| P14 | X. Jia et al. (2026) | Attack | Y | Y | Y | NV | NV | NV | Y | NV | NV | P | FULLY VERIFIED | LIMITED EVIDENCE |
| P15 | Wei et al. (2026) | Benchmark | Y | Y | Y | NV | Y | Y | Y | NV | Y | P | FULLY VERIFIED | MODERATE EVIDENCE |
| P16 | Chennabasappa et al. (2025) | Defense | Y | Y | Y | Y | NV | NV | NV | NV | NV | P | FULLY VERIFIED (components only) | LIMITED EVIDENCE |
| P17 | Hasan et al. (2026) | Threat analysis | Y | Y | Y | NV | Y | Y | NA | NV | Y | Y | FULLY VERIFIED | HIGH EVIDENCE |
| P18 | K. Zhu et al. (2025) | Defense | Y | Y | Y | NV | Y | NV | Y | NV | Y | P | FULLY VERIFIED | MODERATE EVIDENCE |
| P19 | Kaptein, Khan, & Podstavnychy (2026) | Analysis | Y | Y | Y | NV | NA | NA | NA | Y | NA | P | FULLY VERIFIED | LIMITED EVIDENCE |
| P20 | Zhan et al. (2024) | Benchmark | Y | Y | Y | NV | Y | Y | Y | NV | Y | Y | FULLY VERIFIED | HIGH EVIDENCE |
| P21 | Zhan et al. (2025) | Attack | Y | Y | Y | NV | NV | Y | Y | NV | Y | Y | FULLY VERIFIED | MODERATE EVIDENCE |
| P22 | Shi et al. (2026) | Attack | Y | Y | Y | NV | NV | NV | Y | NV | NV | Y | FULLY VERIFIED | LIMITED EVIDENCE |
| P23 | Jacob et al. (2025) | Defense | Y | Y | Y | NV | Y | Y | Y | NV | NV | Y | FULLY VERIFIED (Crossref issued-year 2024 vs. 2025 proceedings recorded) | MODERATE EVIDENCE |
| P24 | Y. Chen et al. (2025) | Defense | Y | Y | Y | NV | NV | NV | Y | NV | NV | Y | FULLY VERIFIED | LIMITED EVIDENCE |
| P25 | Y. Liu et al. (2023) | Attack | Y | Y | Y | NV | Y | Y | NA | NV | Y | P | FULLY VERIFIED | MODERATE EVIDENCE |
| P26 | Greshake et al. (2023) | Threat analysis | Y | Y | Y | NV | Y | NA | NA | NV | NA | Y | FULLY VERIFIED | MODERATE EVIDENCE |
| P27 | H. Zhang et al. (2025) | Benchmark | Y | Y | Y | Y | Y | Y | Y | NV | Y | Y | FULLY VERIFIED | HIGH EVIDENCE |
| P28 | B. Zhang et al. (2025) | Attack | Y | Y | Y | NV | NV | NV | NV | Y | Y | Y | FULLY VERIFIED | MODERATE EVIDENCE |
| P29 | Pedro et al. (2023) | Attack | Y | Y | Y | NV | Y | NV | NA | NV | NV | P | FULLY VERIFIED | LIMITED EVIDENCE |
| P30 | Y. Zhang et al. (2024) | Attack | Y | Y | Y | NV | Y | Y | Y | NV | Y | P | FULLY VERIFIED | MODERATE EVIDENCE |
| P31 | Yuan et al. (2024) | Benchmark | Y | Y | Y | NV | Y | Y | Y | NV | Y | Y | PARTIALLY VERIFIED | HIGH EVIDENCE |
| P32 | Castro-Maldonado et al. (2026) | Defense | Y | NV | Y | NV | NV | NV | NV | NV | NV | Y | FULLY VERIFIED (metadata and abstract) | LIMITED EVIDENCE |
| P33 | Mou et al. (2026) | Defense | Y | Y | Y | NV | Y | Y | NV | NV | Y | Y | FULLY VERIFIED | MODERATE EVIDENCE |
| P34 | Storf et al. (2026) | Defense | Y | Y | Y | NV | Y | NV | Y | Y | NV | P | FULLY VERIFIED | LIMITED EVIDENCE |
| P35 | Ruan et al. (2024) | Benchmark | Y | Y | Y | NV | Y | Y | Y | NV | Y | Y | FULLY VERIFIED | HIGH EVIDENCE |
| P36 | Y. Wu et al. (2025) | Defense | Y | Y | Y | NV | NV | Y | NV | NV | Y | Y | FULLY VERIFIED | MODERATE EVIDENCE |
| P37 | S. Wang, Zhu, & Li (2026) | Defense | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | FULLY VERIFIED | HIGH EVIDENCE |
| P38 | H. Li et al. (2025) | Defense | Y | Y | Y | Y | Y | NV | NV | NV | NV | Y | FULLY VERIFIED | MODERATE EVIDENCE |
| P39 | Luo et al. (2025) | Defense | Y | Y | Y | NV | NV | NV | NV | NV | NV | Y | FULLY VERIFIED (metadata; contribution) | LIMITED EVIDENCE |
| P40 | Calboreanu (2026) | Defense | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | FULLY VERIFIED | HIGH EVIDENCE |
| P41 | Y. Liu et al. (2024) | Benchmark | Y | Y | Y | NV | Y | Y | Y | NV | NV | Y | FULLY VERIFIED | MODERATE EVIDENCE |
| P42 | Andriushchenko et al. (2025) | Benchmark | Y | Y | Y | NV | Y | NV | NV | NV | NV | Y | FULLY VERIFIED | MODERATE EVIDENCE |
| P43 | Z. Chen et al. (2024) | Attack | Y | Y | Y | NV | Y | Y | NV | NV | Y | Y | FULLY VERIFIED | MODERATE EVIDENCE |
| P44 | Debenedetti et al. (2024) | Benchmark | Y | Y | Y | NV | Y | Y | Y | NV | NV | Y | FULLY VERIFIED | MODERATE EVIDENCE |
| P45 | M. Q. Li et al. (2026) | Analysis | Y | NA | Y | NV | Y | Y | NA | NV | Y | P | FULLY VERIFIED | MODERATE EVIDENCE |
| P46 | Y. Wang et al. (2026) | Analysis | Y | NA | Y | NV | Y | Y | Y | NV | Y | P | FULLY VERIFIED | MODERATE EVIDENCE |
| P47 | Hines et al. (2024) | Defense | Y | Y | Y | NV | NV | Y | NV | NV | Y | P | FULLY VERIFIED | MODERATE EVIDENCE |
| P48 | S. Chen et al. (2025) | Defense | Y | Y | Y | NV | NV | NV | NV | NV | NV | Y | FULLY VERIFIED | LIMITED EVIDENCE |
| P49 | Shi et al. (2025) | Defense | Y | Y | Y | NV | Y | Y | Y | NV | Y | P | FULLY VERIFIED | MODERATE EVIDENCE |
| P50 | H. Wang, Poskitt, & Sun (2026) | Defense | Y | Y | Y | NV | Y | Y | NV | NV | Y | Y | FULLY VERIFIED | MODERATE EVIDENCE |
| P51 | Tsai & Bagdasarian (2025) | Design | Y | Y | Y | NV | NA | NA | NA | NV | NA | Y | FULLY VERIFIED | LIMITED EVIDENCE |
| P52 | Debenedetti et al. (2025) | Defense | Y | Y | Y | NV | Y | Y | Y | NV | Y | P | FULLY VERIFIED | MODERATE EVIDENCE |
| P53 | Xiang et al. (2025) | Defense | Y | Y | Y | NV | NV | NV | NV | NV | NV | Y | FULLY VERIFIED | LIMITED EVIDENCE |
| P54 | Z. Chen, Kang, & Li (2025) | Defense | Y | Y | Y | NV | NV | NV | NV | NV | NV | Y | FULLY VERIFIED | LIMITED EVIDENCE |
| P55 | Hua et al. (2024) | Defense | Y | Y | Y | NV | NV | NV | NV | NV | NV | Y | FULLY VERIFIED | LIMITED EVIDENCE |
| P56 | Jiang et al. (2025) | Defense | Y | Y | Y | NV | Y | Y | NV | NV | Y | P | FULLY VERIFIED | MODERATE EVIDENCE |
| P57 | Zhu et al. (2025) | Defense | Y | Y | Y | NV | NV | NV | NV | NV | NV | Y | FULLY VERIFIED | LIMITED EVIDENCE |
| P58 | She et al. (2026) | Defense | Y | Y | Y | NV | Y | Y | Y | NV | Y | P | PARTIALLY VERIFIED | MODERATE EVIDENCE |
| P59 | C. L. Wang et al. (2025) | Defense | Y | NV | Y | NV | Y | Y | NV | Y | Y | P | PARTIALLY VERIFIED | MODERATE EVIDENCE |
| P60 | F. Li (2026) | Defense | Y | Y | Y | NV | NV | NV | NV | Y | NV | P | FULLY VERIFIED | LIMITED EVIDENCE |
| P61 | H. Wang et al. (2025) | Defense | Y | Y | Y | NV | Y | Y | NV | NV | Y | P | FULLY VERIFIED | MODERATE EVIDENCE |
| P62 | Lin et al. (2026) | Defense | Y | Y | Y | NV | NV | NV | NV | NV | Y | P | FULLY VERIFIED | MODERATE EVIDENCE |
| P63 | H. Liu et al. (2026) | Defense | Y | Y | Y | NV | Y | NV | NV | NV | NV | P | PARTIALLY VERIFIED | LIMITED EVIDENCE |
| P64 | C. Yang (2026) | Defense | Y | Y | Y | NV | Y | Y | Y | Y | Y | P | PARTIALLY VERIFIED | MODERATE EVIDENCE |
| P65 | Hossain et al. (2026) | Defense | Y | Y | Y | NV | Y | Y | Y | Y | Y | P | PARTIALLY VERIFIED | MODERATE EVIDENCE |
| P66 | Jackson (2025) | Design | Y | NV | Y | NV | NV | NV | NV | NV | NV | P | PARTIALLY VERIFIED | LIMITED EVIDENCE |
| P67 | H.-H. Chen (2026) | Design | Y | Y | Y | NV | NA | NA | NA | NV | NA | P | FULLY VERIFIED | LIMITED EVIDENCE |
| P68 | Z. Chen et al. (2026) | Defense | Y | Y | Y | NV | NV | NV | NV | NV | NV | P | FULLY VERIFIED | LIMITED EVIDENCE |
| P69 | C. Zhang et al. (2026) | Analysis | Y | NA | Y | NV | Y | Y | Y | NV | Y | P | PARTIALLY VERIFIED | MODERATE EVIDENCE |
| P70 | Z. Chen, J. Chen, et al. (2025) | Analysis | Y | Y | Y | NV | Y | NV | NV | NV | NV | P | FULLY VERIFIED | LIMITED EVIDENCE |
| P71 | H. Jia et al. (2026) | Defense | Y | Y | Y | NV | Y | Y | Y | NV | Y | P | FULLY VERIFIED | LIMITED EVIDENCE |

## 5. Limitations of this appraisal

- **Single reviewer, no calibration exercise, no inter-rater agreement.** Every code is one person's judgement.
- **Record-level evidence only.** NV codes cluster in Q4, Q7 and Q8 and would change after full-text appraisal.
- **A checklist, not a validated risk-of-bias tool.** No validated risk-of-bias instrument exists for this heterogeneous computer-security literature. The ten questions follow the review protocol and are not a domain-standard tool.
- **The category rule is a transparent convention, not a validated scale.** It is applied mechanically so that it can be audited and re-run after full-text appraisal.
