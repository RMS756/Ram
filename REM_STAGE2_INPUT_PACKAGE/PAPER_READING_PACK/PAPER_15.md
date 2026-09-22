# PAPER_15 — Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods

**Category:** C. Algorithms used in REM · **Stage 1 Ref ID:** REF-041 · **Read-only reading note.** Nothing in the thesis was changed.

## Bibliographic record

| Field | Value | Source of this field |
| --- | --- | --- |
| Paper number | 15 | This pack |
| Exact title (as cited) | *Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods* | Ch2 reference list L297 and Ch3 reference list L1044 |
| Full authors (as cited) | Platt, J. C. | Ch2 reference list L297 and Ch3 reference list L1044 |
| Year (as cited) | 1999 | Ch2 reference list L297 and Ch3 reference list L1044 |
| Venue (as cited) | In A. J. Smola, P. Bartlett, B. Schölkopf, & D. Schuurmans (Eds.), *Advances in large margin classifiers* (pp. 61–74). MIT Press. | Ch2 reference list L297 and Ch3 reference list L1044 |
| Pages | 61–74 | Chapter reference entry; Crossref (Stage 2) gives the same pages for the 2000 MIT Press chapter |
| DOI | None cited. Crossref records `10.7551/mitpress/1113.003.0008` for the MIT Press chapter at pp. 61–74, titled **"Probabilities for SV Machines"**, by John C. Platt, published **2000** (Stage 2). Its title and year differ from the citation. | Stage 2 Crossref check |
| arXiv ID | Not applicable | — |
| Official publisher / record URL | None cited in the chapter entry. The only official identifier recorded is the Crossref DOI above, which belongs to a record whose title and year differ from the citation (OI-07). | Chapter reference entry; Stage 2 report |
| Official PDF URL | Not recorded in any verification record | Search of all repository documents |
| Local copy | **PDF NOT LOCALLY AVAILABLE** | Repository search: no PDF of any cited paper is stored |

## Verification status

- **Reference status (THESIS_READING_INDEX.md):** PARTIALLY VERIFIED
- **Depth of reading:** **SOURCE NOT OPENED — METADATA CONFLICT (cited title/year vs registered record). FULL TEXT NOT VERIFIED.**
- **Basis:** Stage 1: "Hosting site certificate error; chapter and pages not confirmed". Stage 2: Crossref record found; title and year differ.
- **Record conflict:** `STAGE2_FINAL_ALGORITHM_MATHEMATICAL_DECISION_REPORT.md` lists this source as verified for "Venue + content (sigmoid form, smoothed targets, out-of-sample fitting)". The later Stage 1 audit could not open it. This pack follows Stage 1: none of those content points is verified.

## Where the thesis uses it

**Used in:** Both chapters.

- **Chapter 2** (reference #32): §2.9 Probability Calibration (L124)
- **Chapter 3** (reference #31): §3.7.2 Calibration on the logit (L342); §3.13 Contribution and Novelty Boundaries (L879); §3.15 Equation Provenance Summary (L946)

Line numbers refer to `working/Chapter2_working.md` and `working/Chapter3_working.md`.

## Thesis claims that depend on it

Every sentence in the chapters that cites this paper, or continues a paragraph about it, with the audit record for that specific claim. **"NOT AUDITED AT CLAIM LEVEL" means no audit record checks that sentence against the paper.** It is not a finding that the paper does not support it. Full records are in `CLAIM_TO_PAPER_MAP.md`.

| Claim | Ch · § · line | Link | Status for this paper |
| --- | --- | --- | --- |
| **CM-040** — Platt (1999) fitted a sigmoid to support-vector-machine outputs. | Ch2 §2.9 L124 | cited | UNVERIFIED — source could not be opened |
| **CM-088** — The method is Platt scaling (Platt, 1999). | Ch3 §3.7.2 L342 | cited | UNVERIFIED — source could not be opened |
| **CM-112** — \| Platt (logistic) calibration \| Platt (1999); Guo et al. (2017); Kull et al. (2017) \| | Ch3 §3.13 L879 | table row | UNVERIFIED — source could not be opened |
| **CM-125** — \| 3.3 \| Logistic calibration on the logit, γ_{1} > 0 \| Adapted \| Platt (1999); Guo et al. (2017); Kull et al. (2017) \| Platt NC; Guo FV; Kull FV \| | Ch3 §3.15 L946 | table row | UNVERIFIED — source could not be opened |

## What to read in the paper

**Reading mode:** Read completely.

Section and page numbers are given **only where a Stage 1 or Stage 2 record documents them**. Anything else is described by content, because the paper's own section numbering is not recorded.

- **Whole chapter, pp. 61–74 of the MIT Press volume.** No stage has read it.
- **The sigmoid fitting procedure and its parameterization.** Ch3 Eq. 3.3 adapts this method. Compare the sign convention with `p_t = σ(γ₁ s_t + γ₀)`, `γ₁ > 0`.
- **The title page and publication details.** OI-07: establish whether the cited 1999 title and year or the registered 2000 title and year describe what you read.

## Why this paper matters for understanding REM

Named in both chapters as the origin of Platt scaling, the method Eq. 3.3 adapts. The citation's title and year do not match the Crossref record of the MIT Press chapter at the cited pages (OI-07).

## Retrieval

**PDF NOT LOCALLY AVAILABLE.** Retrieve it manually from the official record above. This working environment blocks arXiv, publisher and author-hosted domains, so the files here could not be downloaded.
