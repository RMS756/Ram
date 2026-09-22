# PAPER READING PACK — the 18 papers behind REM

**Read-only reading preparation.** This pack helps you read the papers that Chapters 2 and 3 are built on. No chapter, reference, citation, algorithm, equation, experiment or architecture was changed to produce it. Chapter digests at creation: Ch2 `1e59d4a74d9205a2`, Ch3 `5085e11732dee82f` (unchanged from the Stage 1 baseline).

**Built from:** `../THESIS_READING_INDEX.md` (Section 5 selected the 18 papers), `../working/Chapter2_working.md`, `../working/Chapter3_working.md`, the Stage 1 audit workbooks in `../stage1_audits/` (01, 02, 03, 05, 06), the Stage 2 report `../../REM_STAGE2_OUTPUT/STAGE2_RESOLUTION_REPORT.md`, and older project reports where they record a URL (each flagged where used).

## Files

| File | Contents |
| --- | --- |
| `README.md` | This overview |
| `PAPER_01.md` … `PAPER_18.md` | One reading note per paper: the bibliographic record with a source for every field, verification status, where the thesis uses it, the claims that depend on it, what to read, and why it matters |
| `READING_ORDER.md` | A reading sequence (not a ranking) with the mode, sections and purpose of each reading |
| `CLAIM_TO_PAPER_MAP.md` | Every thesis sentence that depends on these papers, traced to the paper, its section and line, the evidence location and the verification status |

## The 18 papers, grouped by category

Grouped under the four categories from `THESIS_READING_INDEX.md` Section 5, in the same order: alphabetical within each group. **The papers are not ranked.**

### A. Foundations

| No. | Paper | Used in | Reference status | Depth of reading on record | Claims |
| :---: | --- | --- | --- | --- | :---: |
| [01](PAPER_01.md) | Chow (1970) — *On optimum recognition error and reject tradeoff* | Both chapters | PARTIALLY VERIFIED | ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED | 4 |
| [02](PAPER_02.md) | Elkan (2001) — *The foundations of cost-sensitive learning* | Both chapters | VERIFIED | SOURCE TEXT READ IN STAGE 1 (author PDF) — PARTS READ: cost-matrix convention and Eq. (1). Printed threshold expression NOT inspected. | 9 |
| [03](PAPER_03.md) | Greshake et al. (2023) — *Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection* | Both chapters | VERIFIED | ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED | 3 |

### B. Prior-art / competing approaches

| No. | Paper | Used in | Reference status | Depth of reading on record | Claims |
| :---: | --- | --- | --- | --- | :---: |
| [04](PAPER_04.md) | H.-H. Chen (2026) — *Insuring every action: An authority frontier framework for runtime actuarial control of autonomous AI agents* | Both chapters | VERIFIED | ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED | 11 |
| [05](PAPER_05.md) | Hossain et al. (2026) — NEXUS — *NEXUS: Structured runtime safety for tool-using LLM agents* | Both chapters | PARTIALLY VERIFIED | SOURCE TEXT READ IN STAGE 1 (full HTML) — not reproducible in this environment. METADATA CONFLICT: arXiv ID vs submission date. Four figures UNVERIFIED. | 23 |
| [06](PAPER_06.md) | H. Liu et al. (2026) — SafeAgent — *SafeAgent: A runtime protection architecture for agentic systems* | Both chapters | VERIFIED | SOURCE TEXT READ IN STAGE 1 — not reproducible in this environment (full HTML text) | 15 |
| [07](PAPER_07.md) | She et al. (2026) — ProvenanceGuard — *Safeguarding LLM agents from misalignment through provenance analysis* | Both chapters | VERIFIED | ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED | 6 |
| [08](PAPER_08.md) | C. Yang (2026) — AgentTrust — *AgentTrust: Runtime safety evaluation and interception for AI agent tool use* | Both chapters | VERIFIED | SOURCE TEXT READ IN STAGE 1 — not reproducible in this environment (full HTML text) | 19 |
| [09](PAPER_09.md) | C. Zhang et al. (2026) — Calibration is not control — *Calibration is not control: Why LLM-agent oversight needs intervention* | Both chapters | VERIFIED | SOURCE TEXT READ IN STAGE 1 — not reproducible in this environment (full HTML text) | 13 |

### C. Algorithms used in REM

| No. | Paper | Used in | Reference status | Depth of reading on record | Claims |
| :---: | --- | --- | --- | --- | :---: |
| [10](PAPER_10.md) | le Cessie & van Houwelingen (1992) — *Ridge estimators in logistic regression* | Chapter 3 only | PARTIALLY VERIFIED | ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED | 5 |
| [11](PAPER_11.md) | Cox (1958) — *The regression analysis of binary sequences* | Chapter 3 only | PARTIALLY VERIFIED | ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED | 4 |
| [12](PAPER_12.md) | Guo et al. (2017) — *On calibration of modern neural networks* | Both chapters | VERIFIED | SOURCE TEXT READ IN STAGE 1 — not reproducible in this environment (ar5iv rendering): calibration definition, ECE bins, Platt form, NLL fit; §4.1 | 11 |
| [13](PAPER_13.md) | Kull et al. (2017) — *Beta calibration: A well-founded and easily implemented improvement on logistic calibration for binary classifiers* | Both chapters | VERIFIED | SOURCE TEXT READ IN STAGE 1 — not reproducible in this environment (PMLR PDF text): monotonicity constraint, §2.2, Proposition 1 | 5 |
| [14](PAPER_14.md) | Lundberg & Lee (2017) — *A unified approach to interpreting model predictions* | Both chapters | VERIFIED | SOURCE TEXT READ IN STAGE 1 — not reproducible in this environment (ar5iv rendering): Properties 1–3, Theorem 1, Corollary 1 | 7 |
| [15](PAPER_15.md) | Platt (1999) — *Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods* | Both chapters | PARTIALLY VERIFIED | SOURCE NOT OPENED — METADATA CONFLICT (cited title/year vs registered record). FULL TEXT NOT VERIFIED. | 4 |

### D. Financial-agent evaluation

| No. | Paper | Used in | Reference status | Depth of reading on record | Claims |
| :---: | --- | --- | --- | --- | :---: |
| [16](PAPER_16.md) | Z. Chen, J. Chen, et al. (2025) — *Standard benchmarks fail — Auditing LLM agents in finance must prioritize risk* | Chapter 2 only | VERIFIED | ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED | 2 |
| [17](PAPER_17.md) | Debenedetti et al. (2024) — AgentDojo — *AgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents* | Both chapters | VERIFIED | ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (benchmark source code inspected separately) | 6 |
| [18](PAPER_18.md) | Jia et al. (2026) — FinHarness — *FinHarness: An inline lifecycle safety harness for finance LLM agents* | Both chapters | VERIFIED | ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED | 10 |

## Rules followed

- **Nothing is invented.** Every title, author list, year and venue is copied from the chapter reference entry. Every DOI, arXiv ID, URL and page range comes from the chapter entry, a Stage 1 or Stage 2 record, or an older project report that is named where it is used. A field with no record says so.
- **PDF NOT LOCALLY AVAILABLE** is stated for every paper. A search of the repository found no stored PDF of any cited paper.
- **ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED** marks every paper, and every claim, where only an abstract or metadata was checked.
- **No support is claimed without a record.** Each claim in `CLAIM_TO_PAPER_MAP.md` shows the Stage 1 record that checks it. Where none exists, it is marked **NOT AUDITED AT CLAIM LEVEL**, with only the reference-level record shown.
- **Section and page numbers** are given only where a record documents them. Other reading targets are described by content.

## Record conflicts you should know about

Some older project reports claim more verification than the later Stage 1 audit recorded. In each case this pack follows the **Stage 1** record and shows the older claim so that you can check it against the paper.

| Paper | Older record says | Stage 1 records | Treat as |
| --- | --- | --- | --- |
| 02 Elkan (2001) | "Venue + content (expected-cost rule, reasonableness conditions, `p*` formula)" (`STAGE2_FINAL_ALGORITHM_MATHEMATICAL_DECISION_REPORT.md`); classed **SIV**, search-index verified, in `STAGE2_5_PRIOR_ART_RECONCILIATION.md` | Only the cost convention and Eq. (1) read; Chapter 3 says the printed threshold was not inspected | Reasonableness conditions and `p*` formula **not verified** |
| 01 Chow (1970) | "Venue + content (reject rule, cost-derived threshold)"; threshold `t = (C_r − C_c)/(C_e − C_c)` (`STAGE3_CHAPTER3_DESIGN.md`) | "Crossref metadata only; reject rule not read" | Reject rule and threshold **not verified** |
| 15 Platt (1999) | "Venue + content (sigmoid form, smoothed targets, out-of-sample fitting)" | Could not be opened (certificate error). Stage 2 found a title/year conflict | **Nothing** about its content is verified |
| 14 Lundberg & Lee (2017) | NeurIPS 30, pp. 4765–4774 | Pages not verified | Pages **UNVERIFIED** |
| 17 AgentDojo (2024) | Venue NeurIPS 2024 Datasets & Benchmarks | Chapter cites arXiv only; venue not verified | Venue **UNVERIFIED** |
| 05 NEXUS (2026) | `V1_NEXUS_DIRECT_VERIFICATION.md`: V-1 unresolved, written before the Stage 1 records were in this repository | Expected-loss objective and rule-cascade sentences supported from a full-text reading; four figures not read | See OI-01 to OI-06 in `../THESIS_READING_INDEX.md` |

## Why most papers must be read outside this environment

This working environment blocks arXiv, SSRN, publisher sites and author-hosted pages. Stage 1 read some sources in full elsewhere, and those readings cannot be reproduced here. Every paper therefore has to be obtained manually from the official record given in its note.

## Totals

```text
PATH:                                  REM_STAGE2_INPUT_PACKAGE/PAPER_READING_PACK/
TOTAL PAPERS LISTED:                   18
TOTAL PAPERS WITH OFFICIAL URLS:       17
TOTAL PAPERS WITH OFFICIAL PDFS:       1
TOTAL PAPERS REQUIRING MANUAL RETRIEVAL: 18
TOTAL CLAIMS MAPPED:                   133   (157 claim–paper links)
```

**Official URLs** (17): DOI resolver (4: 01, 03, 10, 11); ACM Digital Library record (1: 02); arXiv record (10: 04, 05, 06, 07, 08, 09, 14, 16, 17, 18); PMLR proceedings page (2: 12, 13). Not counted: 15 Platt, because the chapter cites no URL and the only Crossref record found has a different title and year (OI-07).

**Official PDFs** (1): 14 Lundberg & Lee (2017) — the arXiv PDF of the preprint version, not the NeurIPS proceedings PDF. Not counted: 02 Elkan (2001) (author-hosted copy). No PDF is stored locally.

**Manual retrieval** (18): all papers. None is stored in the repository.
