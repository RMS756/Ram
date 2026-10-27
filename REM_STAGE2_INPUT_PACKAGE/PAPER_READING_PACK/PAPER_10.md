# PAPER_10 — Ridge estimators in logistic regression

**Category:** C. Algorithms used in REM · **Stage 1 Ref ID:** REF-004 · **Read-only reading note.** Nothing in the thesis was changed.

## Bibliographic record

| Field | Value | Source of this field |
| --- | --- | --- |
| Paper number | 10 | This pack |
| Exact title (as cited) | *Ridge estimators in logistic regression* | Ch3 reference list L1024 |
| Full authors (as cited) | le Cessie, S., & van Houwelingen, J. C. | Ch3 reference list L1024 |
| Year (as cited) | 1992 | Ch3 reference list L1024 |
| Venue (as cited) | *Applied Statistics, 41*(1), 191–201. | Ch3 reference list L1024 |
| Pages | 191–201 as cited. Crossref records the first page (191) only. | Chapter reference entry; Crossref (Stage 2) |
| DOI | `10.2307/2347628` | Chapter reference entry; Crossref (Stage 1 and Stage 2: Applied Statistics 41(1), first page 191, publisher JSTOR) |
| arXiv ID | Not applicable | — |
| Official publisher / record URL | https://doi.org/10.2307/2347628 | Chapter reference entry (DOI resolver link) |
| Official PDF URL | Not recorded in any verification record | Search of all repository documents |
| Local copy | **PDF NOT LOCALLY AVAILABLE** | Repository search: no PDF of any cited paper is stored |

## Verification status

- **Reference status (THESIS_READING_INDEX.md):** PARTIALLY VERIFIED
- **Depth of reading:** **ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
- **Basis:** Stage 1: "Crossref metadata only; penalty formulation not read".

## Where the thesis uses it

**Used in:** Chapter 3 only.

- **Chapter 3** (reference #21): §3.7.1 Ridge logistic estimation (L318, L329); §3.13 Contribution and Novelty Boundaries (L878); §3.15 Equation Provenance Summary (L945)

Line numbers refer to `working/Chapter2_working.md` and `working/Chapter3_working.md`.

## Thesis claims that depend on it

Every sentence in the chapters that cites this paper, or continues a paragraph about it, with the audit record for that specific claim. **"NOT AUDITED AT CLAIM LEVEL" means no audit record checks that sentence against the paper.** It is not a finding that the paper does not support it. Full records are in `CLAIM_TO_PAPER_MAP.md`.

| Claim | Ch · § · line | Link | Status for this paper |
| --- | --- | --- | --- |
| **CM-085** — The parameters are estimated offline by maximizing a ridge-penalized log-likelihood (le Cessie & van Houwelingen, 1992): | Ch3 §3.7.1 L318 | cited | PARTIALLY SUPPORTED — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (metadata only; source text not read) |
| **CM-086** — *Status:* established from source. | Ch3 §3.7.1 L325 | status-line | PARTIALLY SUPPORTED — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (metadata only; source text not read) |
| **CM-087** — The exact scaling constant of the penalty in le Cessie and van Houwelingen (1992) is pending full-text verification. | Ch3 §3.7.1 L329 | cited | PARTIALLY SUPPORTED — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (metadata only; source text not read) |
| **CM-111** — \| Ridge regularization of logistic regression \| le Cessie and van Houwelingen (1992) \| | Ch3 §3.13 L878 | table row | NOT AUDITED AT CLAIM LEVEL |
| **CM-124** — \| 3.2 \| Ridge-penalized log-likelihood \| Established \| le Cessie & van Houwelingen (1992) \| IV (penalty constant pending) \| | Ch3 §3.15 L945 | table row | PARTIALLY SUPPORTED — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (metadata only; source text not read) |

## What to read in the paper

**Reading mode:** Targeted reading.

Section and page numbers are given **only where a Stage 1 or Stage 2 record documents them**. Anything else is described by content, because the paper's own section numbering is not recorded.

- **The definition of the ridge-penalized log-likelihood.** Source of Ch3 Eq. 3.2. The penalty's scaling constant is pending (OI-10; the chapter says so at L329).
- **Whether and how the intercept is penalized.** Eq. 3.2 leaves the intercept unpenalized. Stage 2 checked this against the frozen design, not against the paper.
- **The motivation for ridge estimation in logistic regression.** Ch3 §3.7.1 (L327) gives the reason the penalty is needed (non-finite estimates with separated binary features). Compare it with the paper's own motivation.

## Why this paper matters for understanding REM

Source of the ridge-penalized log-likelihood, Eq. 3.2. Chapter 3 states that the penalty's scaling constant is pending full-text verification.

## Retrieval

**PDF NOT LOCALLY AVAILABLE.** Retrieve it manually from the official record above. This working environment blocks arXiv, publisher and author-hosted domains, so the files here could not be downloaded.
