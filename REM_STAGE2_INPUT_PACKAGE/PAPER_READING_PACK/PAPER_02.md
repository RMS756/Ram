# PAPER_02 — The foundations of cost-sensitive learning

**Category:** A. Foundations · **Stage 1 Ref ID:** REF-017 · **Read-only reading note.** Nothing in the thesis was changed.

## Bibliographic record

| Field | Value | Source of this field |
| --- | --- | --- |
| Paper number | 02 | This pack |
| Exact title (as cited) | *The foundations of cost-sensitive learning* | Ch2 reference list L257 and Ch3 reference list L1006 |
| Full authors (as cited) | Elkan, C. | Ch2 reference list L257 and Ch3 reference list L1006 |
| Year (as cited) | 2001 | Ch2 reference list L257 and Ch3 reference list L1006 |
| Venue (as cited) | In *Proceedings of the Seventeenth International Joint Conference on Artificial Intelligence (IJCAI-01)*. | Ch2 reference list L257 and Ch3 reference list L1006 |
| Pages | 973–978 | Stage 2 (dblp and ACM DL index records). The working chapters give no page numbers; only the Stage 2 revised copy adds them. |
| DOI | None registered with Crossref (Stage 2). ACM Digital Library record identifier: `10.5555/1642194.1642224` (Stage 2 report; also `STAGE2_5_PRIOR_ART_RECONCILIATION.md`). | Stage 2 Crossref check; ACM DL record from dblp and ACM index records (Stage 2) |
| arXiv ID | Not applicable | — |
| Official publisher / record URL | https://dl.acm.org/doi/10.5555/1642194.1642224 | ACM Digital Library record, recorded in `STAGE2_FINAL_ALGORITHM_MATHEMATICAL_DECISION_REPORT.md` and `STAGE3_CHAPTER3_DESIGN.md`. The chapter entry itself cites only the author-hosted PDF. |
| Official PDF URL | https://cseweb.ucsd.edu/~elkan/rescale.pdf | Chapter reference entry. This is an **author-hosted copy**, not the publisher's PDF. Stage 1 read it; the host is blocked in this environment. |
| Local copy | **PDF NOT LOCALLY AVAILABLE** | Repository search: no PDF of any cited paper is stored |

## Verification status

- **Reference status (THESIS_READING_INDEX.md):** VERIFIED
- **Depth of reading:** **SOURCE TEXT READ IN STAGE 1 (author PDF) — PARTS READ: cost-matrix convention and Eq. (1). Printed threshold expression NOT inspected.**
- **Basis:** Stage 1 reference master: "Author PDF: cost convention and Eq. (1) read". Stage 1 equation audit: "Elkan Eq. (1) read on page 1 of the author PDF". Chapter 3 (L456) states that the printed threshold expression "could not be inspected directly during verification".
- **Record conflict:** `STAGE2_FINAL_ALGORITHM_MATHEMATICAL_DECISION_REPORT.md` lists "Venue + content (expected-cost rule, reasonableness conditions, `p*` formula)" as verified, and `STAGE3_CHAPTER3_DESIGN.md` gives the cost-matrix conditions `c(0,1) > c(1,1)`, `c(1,0) > c(0,0)`. `STAGE2_5_PRIOR_ART_RECONCILIATION.md` classifies this same source as **SIV** (search-index verified). The later Stage 1 audit records only the cost convention and Eq. (1) as read. This pack follows Stage 1: treat the reasonableness conditions and the `p*` formula as **not yet verified** in the paper.

## Where the thesis uses it

**Used in:** Both chapters.

- **Chapter 2** (reference #12): §2.10 Runtime Decision and Mitigation (L134)
- **Chapter 3** (reference #12): §3.7.5 Expected-loss verdict selection (L426, L456); §3.13 Contribution and Novelty Boundaries (L882); §3.15 Equation Provenance Summary (L949, L950, L952)

Line numbers refer to `working/Chapter2_working.md` and `working/Chapter3_working.md`.

## Thesis claims that depend on it

Every sentence in the chapters that cites this paper, or continues a paragraph about it, with the audit record for that specific claim. **"NOT AUDITED AT CLAIM LEVEL" means no audit record checks that sentence against the paper.** It is not a finding that the paper does not support it. Full records are in `CLAIM_TO_PAPER_MAP.md`.

| Claim | Ch · § · line | Link | Status for this paper |
| --- | --- | --- | --- |
| **CM-049** — Elkan (2001) states that an example should be assigned the prediction with the lowest expected cost, computed from the conditional probability of each class and a cost matrix whose entries give the cost of each predic… | Ch2 §2.10 L134 | cited | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-096** — Elkan (2001) states that the optimal prediction is the one that minimizes expected cost, computed from the conditional probability of each class and the cost of each prediction for each true class. | Ch3 §3.7.5 L426 | cited | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-097** — Elkan's criterion is stated for predictions of classes. | Ch3 §3.7.5 L432 | status-line | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-098** — *Status:* adapted from source; the tie-breaking order is a design definition that makes the rule a function. | Ch3 §3.7.5 L440 | status-line | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-099** — It has the form of the standard two-class cost-sensitive threshold for zero-cost correct decisions, which Elkan (2001) obtains from the same expected-cost criterion; the printed threshold expression in that paper coul… | Ch3 §3.7.5 L456 | cited | PARTLY SUPPORTED — source read, but the specific passage was not inspected |
| **CM-114** — \| Expected-cost decisions; reject option \| Elkan (2001); Chow (1970) \| | Ch3 §3.13 L882 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-127** — \| 3.6 \| Conditional risk \| Adapted \| Elkan (2001) \| FV (Eq. 1 form) \| | Ch3 §3.15 L949 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-128** — \| 3.7 \| Bayes verdict with tie-breaking \| Adapted \| Elkan (2001) \| FV; tie order DEF \| | Ch3 §3.15 L950 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-129** — \| 3.9 \| Allow–Block threshold \| Derived \| From Eq. 3.8; consistent with Elkan (2001) \| DER \| | Ch3 §3.15 L952 | table row | PARTLY SUPPORTED — source read, but the specific passage was not inspected |

## What to read in the paper

**Reading mode:** Read completely.

Section and page numbers are given **only where a Stage 1 or Stage 2 record documents them**. Anything else is described by content, because the paper's own section numbering is not recorded.

- **Page 1 of the author PDF — Eq. (1) and the cost-matrix convention.** This is the **only verified in-paper location** among the 18 papers. Ch3 Eqs. 3.6–3.7 are adapted from it (Stage 1 equation audit).
- **The two-class decision threshold (location not recorded).** Ch3 §3.7.5 (L456) compares Eq. 3.9 with it, and the chapter says it has not been inspected (OI-11).
- **The conditions under which a cost matrix is "reasonable" (location not recorded).** The older reports cite them, but the Stage 1 audit did not read them.
- **Whole paper, pp. 973–978.** Six pages. It is the source of the decision principle behind REM's verdict rule.

## Why this paper matters for understanding REM

Chapter 3's conditional risk and Bayes verdict (Eqs. 3.6–3.7) are marked "Adapted" from this paper's expected-cost criterion, and Chapter 2 introduces decision theory through it. Reading it shows exactly what REM takes from Elkan (a two-class, cost-matrix decision rule) and what REM adds (four verdicts, consequence tiers). The threshold form of Eq. 3.9 is compared against this paper, and its printed threshold expression has not yet been inspected.

## Retrieval

**PDF NOT LOCALLY AVAILABLE.** Retrieve it manually from the official record above. This working environment blocks arXiv, publisher and author-hosted domains, so the files here could not be downloaded.
