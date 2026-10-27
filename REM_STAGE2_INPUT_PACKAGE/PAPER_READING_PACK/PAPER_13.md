# PAPER_13 — Beta calibration: A well-founded and easily implemented improvement on logistic calibration for binary classifiers

**Category:** C. Algorithms used in REM · **Stage 1 Ref ID:** REF-027 · **Read-only reading note.** Nothing in the thesis was changed.

## Bibliographic record

| Field | Value | Source of this field |
| --- | --- | --- |
| Paper number | 13 | This pack |
| Exact title (as cited) | *Beta calibration: A well-founded and easily implemented improvement on logistic calibration for binary classifiers* | Ch2 reference list L275 and Ch3 reference list L1022 |
| Full authors (as cited) | Kull, M., Silva Filho, T., & Flach, P. | Ch2 reference list L275 and Ch3 reference list L1022 |
| Year (as cited) | 2017 | Ch2 reference list L275 and Ch3 reference list L1022 |
| Venue (as cited) | In *Proceedings of the 20th International Conference on Artificial Intelligence and Statistics* (Vol. 54, pp. 623–631). PMLR. | Ch2 reference list L275 and Ch3 reference list L1022 |
| Pages | 623–631 (PMLR Vol. 54) | Chapter reference entry; Stage 1 metadata check |
| DOI | None recorded | — |
| arXiv ID | Not recorded | — |
| Official publisher / record URL | https://proceedings.mlr.press/v54/kull17a.html | Chapter reference entry (PMLR proceedings page) |
| Official PDF URL | Not recorded in any verification record | Search of all repository documents |
| Local copy | **PDF NOT LOCALLY AVAILABLE** | Repository search: no PDF of any cited paper is stored |

## Verification status

- **Reference status (THESIS_READING_INDEX.md):** VERIFIED
- **Depth of reading:** **SOURCE TEXT READ IN STAGE 1 — not reproducible in this environment (PMLR PDF text): monotonicity constraint, §2.2, Proposition 1**
- **Basis:** Stage 1 reference master: "PMLR PDF text: monotonicity constraint and Proposition 1". Stage 1 equation audit: "Kull §2.2 and Prop. 1 read".

## Where the thesis uses it

**Used in:** Both chapters.

- **Chapter 2** (reference #21): §2.9 Probability Calibration (L124)
- **Chapter 3** (reference #20): §3.7.2 Calibration on the logit (L342, L355); §3.13 Contribution and Novelty Boundaries (L879); §3.15 Equation Provenance Summary (L946)

Line numbers refer to `working/Chapter2_working.md` and `working/Chapter3_working.md`.

## Thesis claims that depend on it

Every sentence in the chapters that cites this paper, or continues a paragraph about it, with the audit record for that specific claim. **"NOT AUDITED AT CLAIM LEVEL" means no audit record checks that sentence against the paper.** It is not a finding that the paper does not support it. Full records are in `CLAIM_TO_PAPER_MAP.md`.

| Claim | Ch · § · line | Link | Status for this paper |
| --- | --- | --- | --- |
| **CM-042** — Kull et al. (2017) point out that logistic calibration applied to raw scores in the unit interval cannot represent the identity map and propose beta calibration. | Ch2 §2.9 L124 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-090** — The monotonicity condition follows Kull et al. (2017), who require a non-negative slope for a non-decreasing map; REM requires a strictly positive slope so that the ranking of steps is preserved. | Ch3 §3.7.2 L342 | cited | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-093** — Kull et al. (2017) prove that beta calibration with equal shape parameters equals logistic calibration applied to the log-odds of a score. | Ch3 §3.7.2 L355 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-112** — \| Platt (logistic) calibration \| Platt (1999); Guo et al. (2017); Kull et al. (2017) \| | Ch3 §3.13 L879 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-125** — \| 3.3 \| Logistic calibration on the logit, γ_{1} > 0 \| Adapted \| Platt (1999); Guo et al. (2017); Kull et al. (2017) \| Platt NC; Guo FV; Kull FV \| | Ch3 §3.15 L946 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |

## What to read in the paper

**Reading mode:** Targeted reading.

Section and page numbers are given **only where a Stage 1 or Stage 2 record documents them**. Anything else is described by content, because the paper's own section numbering is not recorded.

- **§2.2 and Proposition 1.** These are the Stage 1 locations for the monotonicity condition used in Ch3 Eq. 3.3.
- **The limitation that logistic calibration on unit-interval scores cannot represent the identity map.** Ch2 L124. No claim-level audit record; its location in the paper is not recorded.
- **The relation between beta calibration with equal shape parameters and logistic calibration on the log-odds.** Ch3 L355 says the paper "prove[s]" this. No claim-level audit record, and which part of the paper states it is not recorded.

## Why this paper matters for understanding REM

Two points about Eq. 3.3 rest on this paper: the positive-slope (monotonicity) condition, and the argument that logistic calibration on the logit is beta calibration with equal shape parameters. That argument is why beta calibration is not adopted separately. Stage 1 read the PMLR text.

## Retrieval

**PDF NOT LOCALLY AVAILABLE.** Retrieve it manually from the official record above. This working environment blocks arXiv, publisher and author-hosted domains, so the files here could not be downloaded.
