# STAGE 2 — PRE-FLIGHT CORPUS VERIFICATION

**Date:** 2026-09-22
**Input package:** `REM_STAGE2_INPUT_PACKAGE.zip`
**Purpose:** confirm which files Stage 2 is operating on, before any substantive audit.

---

## 1. The Phase-1 block is lifted

The earlier audit stopped at Phase 1 of 13 because Chapter 2 and Chapter 3 were
not present in the workspace (`BLOCKED_CHAPTER_SOURCES_MISSING.md`). That finding
was correct **for the workspace as it then stood**, and it is now superseded: the
chapters were supplied in the Stage 1 output package, not in the repository.

`00_WORKSPACE_INVENTORY.md` and `BLOCKED_CHAPTER_SOURCES_MISSING.md` are retained
unchanged as the historical record of that state. They are **not** deleted, per the
instruction that evidence is never removed to tidy a problem away.

---

## 2. Chapter files in use

Stage 2 uses the Stage 1 **working copies** as the audited baseline, as instructed.
The section-design files are not used as chapter text.

| | Chapter 2 | Chapter 3 |
| --- | --- | --- |
| **File** | `working/Chapter2_working.md` | `working/Chapter3_working.md` |
| **Lines** | 327 | 1,056 |
| **Words** | 7,936 | 12,894 |
| **Characters** | 54,648 | 85,167 |
| **SHA-256 (first 16)** | `1e59d4a74d9205a2` | `5085e11732dee82f` |
| **`## References` heading** | present, line 233 | present, line 982 |
| **Reference entries** | **47** | **37** |
| **Parenthetical in-text citations** | 72 | 23 |

Both reference lists are present and populated. Chapter 3's lower parenthetical
count reflects its methodological style, which names sources in running text and
in per-equation *Status* lines rather than in trailing parentheses; it is not a
sign of missing attribution.

> **Note on word counts.** An earlier pass reported 7,852 and 12,741 words. The
> difference is tokenisation (whitespace splitting versus a word-boundary regex),
> not a change in the files: the SHA-256 digests above are identical to those
> recorded when the package was first opened. The corpus is byte-for-byte the one
> Stage 1 produced.

### Files deliberately NOT used as chapter text

`STAGE3_CHAPTER2_DESIGN.md` and `STAGE3_CHAPTER3_DESIGN.md` are section-by-section
structure plans. They are excluded, as instructed.

---

## 3. Package integrity

`sha256sum -c PACKAGE_SHA256SUMS.txt` → **16 files OK, 1 reported failure.**

The single failure is `PACKAGE_SHA256SUMS.txt` verifying **itself**: a manifest
cannot contain its own post-write digest. This is expected and benign. Every
content file in the package verifies.

---

## 4. Stage 1 audit workbooks — all accessible

| Workbook | Loads | Rows × Cols |
| --- | :---: | --- |
| `01_CHAPTER2_LITERATURE_EVIDENCE_AUDIT.xlsx` | ✅ | 53 × 11 |
| `02_CHAPTER3_LITERATURE_EVIDENCE_AUDIT.xlsx` | ✅ | 56 × 11 |
| `03_REFERENCE_VERIFICATION_MASTER.xlsx` | ✅ | 59 × 14 |
| `04_PRIOR_ART_COLLISION_MATRIX.xlsx` | ✅ | 21 × 12 |
| `05_EQUATION_SOURCE_AUDIT.xlsx` | ✅ | 24 × 9 |
| `06_NUMERICAL_CLAIMS_AUDIT.xlsx` | ✅ | 75 × 11 |
| `07_AI_STYLE_AUDIT.xlsx` | ✅ | 12 × 8 |

Also present and read: `10_MASTER_AUDIT_REPORT.md`, `11_EDIT_CHANGELOG.md`,
`00_BASELINE_CHECKSUMS.md`, `00_WORKSPACE_INVENTORY.md`, and the two Stage 1
reference DOCX chapters.

The 9 valid Stage 1 corrections recorded in `11_EDIT_CHANGELOG.md` are preserved.
Stage 2 does not restart the Stage 1 audit.

---

## 5. Verification capability — materially changed since Stage 1

Stage 1 recorded that every scholarly domain was blocked, capping verification at
search-index tier. **That cap has partly lifted.** The channels now available were
re-tested at the start of Stage 2:

| Channel | Status | Tier reached |
| --- | :---: | --- |
| Crossref (via literature MCP server) | ✅ reachable | **Bibliographic registration — authoritative** |
| OpenAlex / Semantic Scholar (via MCP) | ✅ reachable | Indexed metadata + abstracts |
| Web search | ✅ reachable | Search-index / snippet only |
| `pypi.org` (via curl) | ✅ reachable | Package source (used for AgentDojo) |
| `arxiv.org` (curl, WebFetch, export API) | ❌ egress-blocked | — |
| `cseweb.ucsd.edu`, `pith.science`, `bytez.com`, author pages | ❌ egress-blocked | — |
| SSRN, publisher PDF pages | ❌ blocked | — |

**What this means for the audit's honesty.** References can now be verified as
*registered works with correct metadata* — author list, year, venue, volume, issue,
pages, DOI — against Crossref, which is the agency that issues most scholarly DOIs.
That is a genuine and authoritative upgrade over Stage 1.

It is **not** full-text access. No claim about *what a paper says on a given page*
has been upgraded on the strength of a Crossref record or a search snippet. Where
a chapter attributes a specific figure or argument to a source, and the source's
text could not be opened, the item remains recorded as content-unverified. The two
tiers are kept separate throughout the Stage 2 report and in the updated workbooks.

No blocked host was retried or routed around.

---

## 6. Ready to proceed

All required inputs are present, verified and readable. Stage 2 proceeds to
tasks A–K in `STAGE2_RESOLUTION_REPORT.md`.
