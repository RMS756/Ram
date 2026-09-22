# PAPER_12 — On calibration of modern neural networks

**Category:** C. Algorithms used in REM · **Stage 1 Ref ID:** REF-020 · **Read-only reading note.** Nothing in the thesis was changed.

## Bibliographic record

| Field | Value | Source of this field |
| --- | --- | --- |
| Paper number | 12 | This pack |
| Exact title (as cited) | *On calibration of modern neural networks* | Ch2 reference list L263 and Ch3 reference list L1012 |
| Full authors (as cited) | Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. | Ch2 reference list L263 and Ch3 reference list L1012 |
| Year (as cited) | 2017 | Ch2 reference list L263 and Ch3 reference list L1012 |
| Venue (as cited) | In *Proceedings of the 34th International Conference on Machine Learning* (Vol. 70, pp. 1321–1330). PMLR. | Ch2 reference list L263 and Ch3 reference list L1012 |
| Pages | 1321–1330 (PMLR Vol. 70) | Chapter reference entry; Stage 1 metadata check |
| DOI | None recorded | — |
| arXiv ID | Not recorded. Stage 1 read an ar5iv (arXiv HTML) rendering, but its identifier was not recorded. | — |
| Official publisher / record URL | https://proceedings.mlr.press/v70/guo17a.html | Chapter reference entry (PMLR proceedings page) |
| Official PDF URL | Not recorded in any verification record | Search of all repository documents |
| Local copy | **PDF NOT LOCALLY AVAILABLE** | Repository search: no PDF of any cited paper is stored |

## Verification status

- **Reference status (THESIS_READING_INDEX.md):** VERIFIED
- **Depth of reading:** **SOURCE TEXT READ IN STAGE 1 — not reproducible in this environment (ar5iv rendering): calibration definition, ECE bins, Platt form, NLL fit; §4.1**
- **Basis:** Stage 1 reference master: "ar5iv full text: calibration definition, ECE bins, Platt form, NLL fit". Stage 1 equation audit: "Guo §4.1 read". Section numbering refers to the version Stage 1 read.
- **Record conflict:** `STAGE2_FINAL_ALGORITHM_MATHEMATICAL_DECISION_REPORT.md` recorded this source as "Referenced indirectly". It is superseded by the Stage 1 full-text reading.

## Where the thesis uses it

**Used in:** Both chapters.

- **Chapter 2** (reference #15): §2.9 Probability Calibration (L122, L124)
- **Chapter 3** (reference #15): §3.7.2 Calibration on the logit (L342, L344, L350); §3.12.2 Secondary metrics (L829, L835); §3.13 Contribution and Novelty Boundaries (L879); §3.15 Equation Provenance Summary (L946, L947, L963)

Line numbers refer to `working/Chapter2_working.md` and `working/Chapter3_working.md`.

## Thesis claims that depend on it

Every sentence in the chapters that cites this paper, or continues a paragraph about it, with the audit record for that specific claim. **"NOT AUDITED AT CLAIM LEVEL" means no audit record checks that sentence against the paper.** It is not a finding that the paper does not support it. Full records are in `CLAIM_TO_PAPER_MAP.md`.

| Claim | Ch · § · line | Link | Status for this paper |
| --- | --- | --- | --- |
| **CM-039** — Guo et al. (2017) define perfect calibration as agreement between predicted confidence and the probability of being correct, and measure deviation with the expected calibration error (ECE), a weighted average of the g… | Ch2 §2.9 L122 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-041** — Guo et al. (2017) describe Platt scaling for the binary case as a logistic transformation of the model's score with two parameters fitted by negative log-likelihood on a validation set, a transformation that preserves… | Ch2 §2.9 L124 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-089** — The two-parameter logistic form with parameters fitted by negative log-likelihood on held-out data follows Guo et al. (2017). | Ch3 §3.7.2 L342 | cited | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-091** — The calibration parameters are fitted by minimizing the negative log-likelihood on held-out logits (Guo et al., 2017): | Ch3 §3.7.2 L344 | cited | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-092** — *Status:* established from source (Guo et al., 2017). | Ch3 §3.7.2 L350 | cited | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-108** — For binary outcomes, calibration error is measured on the positive-class probability (Naeini et al., 2015) with M equal-width bins (Guo et al., 2017): | Ch3 §3.12.2 L829 | cited | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-109** — Naeini et al. (2015) supply the binary form; Guo et al. (2017) supply the equal-width binning. | Ch3 §3.12.2 L835 | cited | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-112** — \| Platt (logistic) calibration \| Platt (1999); Guo et al. (2017); Kull et al. (2017) \| | Ch3 §3.13 L879 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-125** — \| 3.3 \| Logistic calibration on the logit, γ_{1} > 0 \| Adapted \| Platt (1999); Guo et al. (2017); Kull et al. (2017) \| Platt NC; Guo FV; Kull FV \| | Ch3 §3.15 L946 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-126** — \| 3.4 \| Calibration fit by negative log-likelihood \| Established \| Guo et al. (2017) \| FV \| | Ch3 §3.15 L947 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-133** — \| 3.20 \| Expected calibration error \| Adapted \| Naeini et al. (2015); Guo et al. (2017) \| FV \| | Ch3 §3.15 L963 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |

## What to read in the paper

**Reading mode:** Targeted reading.

Section and page numbers are given **only where a Stage 1 or Stage 2 record documents them**. Anything else is described by content, because the paper's own section numbering is not recorded.

- **The definition of calibration and of ECE with equal-width bins.** Ch2 L122; Ch3 Eq. 3.20 (Stage 1 equation audit: read).
- **§4.1 — Platt scaling as a two-parameter logistic map fitted by NLL; temperature scaling.** Ch2 L124; Ch3 Eqs. 3.3–3.4 (Stage 1: §4.1 read).
- **Fitting on a held-out (validation) set.** Ch3 L344 and L348.

## Why this paper matters for understanding REM

This paper supplies three pieces: the two-parameter logistic calibration form and negative log-likelihood fit (Eqs. 3.3–3.4), the equal-width binning in the ECE metric (Eq. 3.20), and Chapter 2's definition of calibration. Stage 1 read its full text.

## Retrieval

**PDF NOT LOCALLY AVAILABLE.** Retrieve it manually from the official record above. This working environment blocks arXiv, publisher and author-hosted domains, so the files here could not be downloaded.
