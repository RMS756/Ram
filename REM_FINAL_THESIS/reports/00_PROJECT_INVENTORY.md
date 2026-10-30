# Project Inventory and Selection of Authoritative Sources (Phase 1)

**Date:** 30 October 2026 · **Working branch:** `claude/rem-algorithm-implementation-3ktvze`
**Branches inspected:** the working branch; `origin/claude/rem-thesis-lit-review-merge-j1px4f` (head `f13f113`, 27 Oct); `origin/claude/rem-thesis-revision-r2-j1px4f` (head `7e19265`, 28 Oct). The R2 branch contains every commit of the lit-review branch, so it supersedes it. It was merged into the working branch in merge commit `4a286a5`. No file was deleted or overwritten by the merge.

## 1. Thesis chapter versions

There are four generations of chapter files. Authority was decided by content and lineage, not by timestamps alone.

| Location | Version / commit | Purpose | Status | Selected? |
|---|---|---|---|---|
| `REM_STAGE2_INPUT_PACKAGE/working/Chapter{2,3}_working.md` | `7559cc3`, 22 Sep | Stage 2 working chapters; Chapter 3 SHA-256 prefix `5085e117…` | Historical | Excluded. Superseded by later chapter versions, which state their changes from these files |
| `REM_STAGE2_OUTPUT/revised_chapters/` | 22 Sep | Stage 2 copies | Historical | Excluded |
| `REM_STAGE2_OUTPUT/THESIS_COMPLETION/CHAPTER{1,4,5}*` | `e05cb6b`, 24 Sep | Chapters 1, 4, 5 written before any experiment existed (implementation-only state) | Superseded: their statement "no experiment executed" became false once the pilot was run on 27 Oct | Excluded. Kept as a historical record |
| `chapter2/CHAPTER2_SYSTEMATIC_REVIEW.md` | `06ee182`, 25 Sep | Record-level PRISMA review with search, screening and appraisal records | Source of Chapter 2 | Excluded as text; its records under `chapter2/slr/` remain the evidence base |
| `thesis/CHAPTER1–6*.md` | `f13f113`, 27 Oct | First six-chapter draft (R1) | Superseded by R2 | Excluded |
| `revision_R2/chapters_md/CHAPTER1–6*_R2.md` | `3b15dc8`, 28 Oct | Revised six-chapter draft (R2), with the change record in `revision_R2/reports_ar/01_…` | Latest complete version | **Selected as the base of the final version (R3)** |
| `REM_FINAL_THESIS/chapters/CHAPTER*_FINAL.md` | this work, 30 Oct | R3: R2 plus the verified corrections listed in `CHANGE_LOG_R3.md` | Final working version | Output |

Generated DOCX and PDF files (`thesis/build/`, `revision_R2/build/`) were treated as build products, not as sources. Each is regenerated from its Markdown by the build script stored beside it.

## 2. Implementation and experiments

| Location | Purpose | Status |
|---|---|---|
| `CLAUDE.md` | Design lock: governs the implementation | Unchanged since `1c18cdf` (SHA-256 prefix `6fef971e`) |
| `rem/` (46 Python modules) | Frozen core (`rem/core`, `rem/algorithms/{detection,calibration,decision,attribution}`) plus Chapter 3 components added on 27 Oct (`context`, `behavior`, `decision/{consequence,loss_matrix,policy}`, `a1/a2/a3`, `evaluation/{crossfit,probabilistic,bootstrap}`, `integration/`) | Verified by the test run of 30 Oct (193 passed) |
| `tests/` (16 files) | Unit, contract and integration tests | Executed 30 Oct |
| `configs/*.yaml`, `configs/exploratory/pilot_e0*.yaml` | Frozen configuration; pre-registered pilot values (`48bef90`) and amendments AM-1 to AM-4 (`7a707a7`) | Present |
| `experiments/pilot/` | Pilot pipeline and the reproduction script `run_all.sh` | Re-executed 30 Oct (see `RESULTS_PROVENANCE_REPORT.md`) |
| `results/pilot/` | R1 results (`aa66f22`) | Historical; kept |
| `results/pilot_R2/` | R2 results (`84a8c21`): the source of every number in Chapter 5 | **Authoritative result set**; independently re-run on 30 Oct |
| External: AgentDojo 0.1.35 (PyPI) and repository commit `089ed468cf3ed0322acc66b0211f26d9d90dbf60` (`runs/`, 525 MB) | Recorded traces of real LLM agents (data source) | Obtained 30 Oct from the public repository; not stored in this repository |

## 3. Literature and verification records

| Location | Content | Status |
|---|---|---|
| `chapter2/slr/` | Raw OpenAlex search output (25 Sep), deduplication, PRISMA counts, included register | Present; counts recomputed by its script |
| `chapter2/CHAPTER2_SCREENING_LOG.csv`, `CHAPTER2_QUALITY_APPRAISAL.md`, `CHAPTER2_VERIFICATION_LOG.md` | Screening decisions, appraisal, metadata verification | Present |
| `revision_R2/evidence/` | R2 quality appraisal, included register, literature checks of 28 Oct | Present |
| `SOURCE_VERIFICATION_REPORT.md`, `REFERENCE_VERIFICATION_MATRIX.xlsx`, `REFERENCES.bib` | Foundational sources (21) | Present |
| `REM_STAGE2_INPUT_PACKAGE/stage1_audits/*.xlsx`, `THESIS_READING_INDEX.md` | Stage 1 reference and claim audits | Historical evidence |
| `EQUATION_PROVENANCE_AUDIT.md`, `STAGE2_EQUATION_TO_SOURCE_TRACEABILITY.md` | Equation-to-source records | Present; no equation registry exists (RG-1) |

## 4. Decision records

`SUPERVISOR_DECISIONS_REQUIRED.md` (root, consolidated 27 Oct), `revision_R2/reports_ar/05_مذكرة_قرارات_المشرف.md` (D-1 to D-15) and `REM_STAGE2_OUTPUT/THESIS_COMPLETION/SUPERVISOR_DECISIONS_REQUIRED.md` (SC-1 to SC-6) are merged in `UNRESOLVED_ITEMS_AND_SUPERVISOR_DECISIONS.md`. No record of any supervisor decision was found. The user's own decisions recorded in `PROJECT_PROGRESS.md` (27 Oct) and in this request (six-chapter structure; institutional details) are recorded as **author decisions**, not as supervisor approvals.

## 5. Missing materials

| Item | Effect |
|---|---|
| Approved thesis proposal | Objectives are known only as quoted in Chapter 3 §3.1.2; title approval is unverifiable |
| University thesis template and formatting rules | Formatting is provisional (Section 15 of the request) |
| Decision ledger and authoritative equation registry | No equation identifiers can be issued (`CLAUDE.md` § EQUATION-ID LOCK) |
| Full texts of cited works | Network policy refuses arXiv, Crossref, OpenAlex and publisher hosts; verification is record-level, through the literature connector |
| LLM API access | Live enforcing-mode runs cannot be executed |
| Student name, committee, dates of approval | Not supplied; left blank on the title page rather than invented |

## 6. Known inconsistencies found during the inventory

1. Twenty-one cited works were formatted differently in different chapters. Each chapter had its own list. This is resolved in R3 by one consolidated reference list.
2. Chapter 1 R2 stated RQ1–RQ4 without the [PD] status that Chapter 3 and the decision register assign to them. This is corrected in R3.
3. The 24 Sep Chapters 1, 4 and 5 (implementation-only state) contradict the 27–28 Oct chapters, because experiments were run in between. The older files are excluded, not edited.
