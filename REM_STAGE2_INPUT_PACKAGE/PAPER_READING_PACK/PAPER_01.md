# PAPER_01 — On optimum recognition error and reject tradeoff

**Category:** A. Foundations · **Stage 1 Ref ID:** REF-011 · **Read-only reading note.** Nothing in the thesis was changed.

## Bibliographic record

| Field | Value | Source of this field |
| --- | --- | --- |
| Paper number | 01 | This pack |
| Exact title (as cited) | *On optimum recognition error and reject tradeoff* | Ch2 reference list L251 and Ch3 reference list L994 |
| Full authors (as cited) | Chow, C. K. | Ch2 reference list L251 and Ch3 reference list L994 |
| Year (as cited) | 1970 | Ch2 reference list L251 and Ch3 reference list L994 |
| Venue (as cited) | *IEEE Transactions on Information Theory, 16*(1), 41–46. | Ch2 reference list L251 and Ch3 reference list L994 |
| Pages | 41–46 (whole article) | Chapter reference entry; Crossref (Stage 2) |
| DOI | `10.1109/TIT.1970.1054406` | Chapter reference entry; matched against Crossref in Stage 1 (reference master) and Stage 2 (volume 16, issue 1, pp. 41–46, publisher IEEE) |
| arXiv ID | Not applicable (1970 journal article) | — |
| Official publisher / record URL | https://doi.org/10.1109/TIT.1970.1054406 | Chapter reference entry (DOI resolver link) |
| Other recorded URL | https://dl.acm.org/doi/10.1109/TIT.1970.1054406 — ACM Digital Library record of the same DOI, recorded in `STAGE3_CHAPTER3_DESIGN.md` and `STAGE2_FINAL_ALGORITHM_MATHEMATICAL_DECISION_REPORT.md` | Repository records named in the value |
| Official PDF URL | Not recorded in any verification record | Search of all repository documents |
| Local copy | **PDF NOT LOCALLY AVAILABLE** | Repository search: no PDF of any cited paper is stored |

## Verification status

- **Reference status (THESIS_READING_INDEX.md):** PARTIALLY VERIFIED
- **Depth of reading:** **ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
- **Basis:** Stage 1: "Crossref metadata only; reject rule not read". No stage has read the article text.
- **Record conflict:** `STAGE2_FINAL_ALGORITHM_MATHEMATICAL_DECISION_REPORT.md` lists this source as verified for "Venue + content (reject rule, cost-derived threshold)", and `STAGE3_CHAPTER3_DESIGN.md` gives a reject threshold `t = (C_r − C_c)/(C_e − C_c)` attributed to it. Both predate the Stage 1 audit, which records that the reject rule was **not** read. This pack follows the Stage 1 record: treat that formula as unverified until you read it in the paper.

## Where the thesis uses it

**Used in:** Both chapters.

- **Chapter 2** (reference #9): §2.10 Runtime Decision and Mitigation (L134)
- **Chapter 3** (reference #6): §3.7.5 Expected-loss verdict selection (L460); §3.13 Contribution and Novelty Boundaries (L882); §3.15 Equation Provenance Summary (L953)

Line numbers refer to `working/Chapter2_working.md` and `working/Chapter3_working.md`.

## Thesis claims that depend on it

Every sentence in the chapters that cites this paper, or continues a paragraph about it, with the audit record for that specific claim. **"NOT AUDITED AT CLAIM LEVEL" means no audit record checks that sentence against the paper.** It is not a finding that the paper does not support it. Full records are in `CLAIM_TO_PAPER_MAP.md`.

| Claim | Ch · § · line | Link | Status for this paper |
| --- | --- | --- | --- |
| **CM-050** — Chow (1970) analyzed the tradeoff between recognition error and rejection, providing the classical basis for withholding an automatic decision. | Ch2 §2.10 L134 | cited | PARTIALLY SUPPORTED — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (metadata only; source text not read) |
| **CM-100** — Chow (1970) analyzed the tradeoff between recognition error and rejection, which is the classical basis for withholding an automatic decision. | Ch3 §3.7.5 L460 | cited | PARTIALLY SUPPORTED — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (metadata only; source text not read) |
| **CM-114** — \| Expected-cost decisions; reject option \| Elkan (2001); Chow (1970) \| | Ch3 §3.13 L882 | table row | PARTIALLY SUPPORTED — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (metadata only; source text not read) |
| **CM-130** — \| 3.10 \| Escalation feasibility condition \| Derived \| From Eqs. 3.6, 3.7, 3.9; Chow (1970) conceptual basis \| DER; Chow IV \| | Ch3 §3.15 L953 | table row | PARTIALLY SUPPORTED — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (metadata only; source text not read) |

## What to read in the paper

**Reading mode:** Read completely.

Section and page numbers are given **only where a Stage 1 or Stage 2 record documents them**. Anything else is described by content, because the paper's own section numbering is not recorded.

- **Whole article, pp. 41–46.** It is six pages. No stage has read it, so every claim built on it (OI-13) waits on this reading.
- **The part that defines the optimum decision rule with a reject option.** Ch2 §2.10 and Ch3 §3.7.5 cite it as "the classical basis for withholding an automatic decision". Check what the paper actually states about the error–reject tradeoff.
- **Any expression of the reject threshold in terms of costs.** The older reports attribute a cost-derived threshold to this paper, but no reading of the paper confirms it.

## Why this paper matters for understanding REM

The Escalate verdict rests on this paper as its conceptual basis for withholding an automatic decision (Ch2 §2.10; Ch3 §3.7.5, Eq. 3.10 context). Stage 1 read only the metadata, not the reject rule itself.

## Retrieval

**PDF NOT LOCALLY AVAILABLE.** Retrieve it manually from the official record above. This working environment blocks arXiv, publisher and author-hosted domains, so the files here could not be downloaded.
