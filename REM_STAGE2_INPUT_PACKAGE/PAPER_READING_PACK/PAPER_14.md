# PAPER_14 — A unified approach to interpreting model predictions

**Category:** C. Algorithms used in REM · **Stage 1 Ref ID:** REF-034 · **Read-only reading note.** Nothing in the thesis was changed.

## Bibliographic record

| Field | Value | Source of this field |
| --- | --- | --- |
| Paper number | 14 | This pack |
| Exact title (as cited) | *A unified approach to interpreting model predictions* | Ch2 reference list L287 and Ch3 reference list L1032 |
| Full authors (as cited) | Lundberg, S. M., & Lee, S.-I. | Ch2 reference list L287 and Ch3 reference list L1032 |
| Year (as cited) | 2017 | Ch2 reference list L287 and Ch3 reference list L1032 |
| Venue (as cited) | In *Advances in Neural Information Processing Systems 30*. | Ch2 reference list L287 and Ch3 reference list L1032 |
| Pages | UNVERIFIED. The older reports give NeurIPS 30 pp. 4765–4774, but Stage 1 did not verify this, and the chapter entry gives no pages. | Older reports only |
| DOI | None recorded | — |
| arXiv ID | `1705.07874` | URL in the chapter reference entry |
| Official publisher / record URL | https://arxiv.org/abs/1705.07874 | Chapter reference entry (arXiv record). The chapter names the venue as *Advances in Neural Information Processing Systems 30*; no NeurIPS proceedings URL is recorded. |
| Official PDF URL | https://arxiv.org/pdf/1705.07874 | Recorded in `STAGE2_FINAL_ALGORITHM_MATHEMATICAL_DECISION_REPORT.md` and `STAGE3_CHAPTER3_DESIGN.md`. This is the **arXiv** PDF, not the NeurIPS proceedings PDF. It is blocked in this environment. |
| Local copy | **PDF NOT LOCALLY AVAILABLE** | Repository search: no PDF of any cited paper is stored |

## Verification status

- **Reference status (THESIS_READING_INDEX.md):** VERIFIED
- **Depth of reading:** **SOURCE TEXT READ IN STAGE 1 — not reproducible in this environment (ar5iv rendering): Properties 1–3, Theorem 1, Corollary 1**
- **Basis:** Stage 1: "ar5iv full text: Properties 1-3, Theorem 1, Corollary 1". Stage 1 equation audit: "Corollary 1 and Property 1 read"; "Property 1 read".

## Where the thesis uses it

**Used in:** Both chapters.

- **Chapter 2** (reference #27): §2.11 Explainability and Auditability (L142)
- **Chapter 3** (reference #25): §3.7.6 Explainability and audit record (L481, L487, L493); §3.13 Contribution and Novelty Boundaries (L880); §3.15 Equation Provenance Summary (L954, L955)

Line numbers refer to `working/Chapter2_working.md` and `working/Chapter3_working.md`.

## Thesis claims that depend on it

Every sentence in the chapters that cites this paper, or continues a paragraph about it, with the audit record for that specific claim. **"NOT AUDITED AT CLAIM LEVEL" means no audit record checks that sentence against the paper.** It is not a finding that the paper does not support it. Full records are in `CLAIM_TO_PAPER_MAP.md`.

| Claim | Ch · § · line | Link | Status for this paper |
| --- | --- | --- | --- |
| **CM-055** — Lundberg and Lee (2017) unified such methods under Shapley values and showed that, for a linear model under an assumption of feature independence, the attribution of each feature is its coefficient multiplied by the f… | Ch2 §2.11 L142 | cited | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-101** — The attribution follows the linear case of Shapley-value attribution given by Lundberg and Lee (2017): | Ch3 §3.7.6 L481 | cited | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-102** — Lundberg and Lee (2017) state the linear case under feature independence with printed indices that do not match between the two sides of the expression and with base value equal to the model intercept. | Ch3 §3.7.6 L487 | cited | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-103** — This is the local-accuracy property of Lundberg and Lee (2017) for a linear model, and REM checks it as a correctness invariant. | Ch3 §3.7.6 L493 | cited | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-113** — \| Linear Shapley attribution \| Lundberg and Lee (2017) \| | Ch3 §3.13 L880 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-131** — \| 3.11 \| Linear attribution \| Adapted \| Lundberg & Lee (2017) \| FV \| | Ch3 §3.15 L954 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-132** — \| 3.12 \| Completeness identity \| Derived \| Lundberg & Lee (2017) local accuracy \| FV + DER \| | Ch3 §3.15 L955 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |

## What to read in the paper

**Reading mode:** Targeted reading.

Section and page numbers are given **only where a Stage 1 or Stage 2 record documents them**. Anything else is described by content, because the paper's own section numbering is not recorded.

- **Property 1 (local accuracy).** Ch3 Eq. 3.12 is checked as an invariant (Stage 1: read).
- **Corollary 1 — the linear-model case under feature independence.** Ch3 Eq. 3.11. The chapter notes that the printed indices do not match across the expression (L487).
- **Properties 2–3 and Theorem 1.** The Shapley-value unification cited in Ch2 L142.

## Why this paper matters for understanding REM

Source of the linear attribution and local-accuracy identity in REM's audit record (Eqs. 3.11–3.12). In REM these are audit-only and do not affect the verdict. Chapter 3 notes an index mismatch in the printed formula.

## Retrieval

**PDF NOT LOCALLY AVAILABLE.** Retrieve it manually from the official record above. This working environment blocks arXiv, publisher and author-hosted domains, so the files here could not be downloaded.
