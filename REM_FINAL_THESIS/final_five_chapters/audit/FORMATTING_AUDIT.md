# FORMATTING AUDIT — five-chapter thesis

**Files:** `REM_THESIS_5CH_FINAL.docx` (editable) and `REM_THESIS_5CH_FINAL.pdf` (LibreOffice 24.2
export of the same DOCX), plus `chapters/CHAPTER1…5*.docx`. Build: `python3 REM_FINAL_THESIS/tools/build_5ch.py`.
QA: `python3 REM_FINAL_THESIS/tools/qa_5ch.py` (logs in `audit/qa_logs/`).

## 1. Reference documents

| Document | Status |
|---|---|
| `enas-thesis_2026 (1).pdf` (layout reference named in the instruction) | **Not available** in the working environment (filesystem search found no such file; no attachment reached the session). |
| Al-Balqa Applied University formatting guide | **Not available.** |
| Earlier R5 cover / official template | Not available. |

**Consequence.** Every layout property below is an **assumed** common A4 university-thesis
style, **not verified** against the university's rules or the reference thesis. No margin, font
or spacing value is claimed to be the university's requirement.

## 2. Properties: what was set, what was verified, what is assumed

| Property | Value in the build | Verified how | University conformance |
|---|---|---|---|
| Page size | A4 (21.0 × 29.7 cm) | `pdfinfo`: 595.3 × 841.9 pt (A4) | Assumed |
| Margins | left 3.0 cm; right, top, bottom 2.5 cm; header/footer 1.25 cm | set in `build_5ch.py` (lines 108–115); margin scan: no ink in the outer 2.2 cm of any of 237 pages | Assumed |
| Body font | Times New Roman 12 pt (style definition in the DOCX) | DOCX styles. **In the PDF, Times New Roman is substituted by Liberation Serif** (metric-compatible) because Times New Roman is not installed in the build container; `pdffonts` lists LiberationSerif and no Times | Assumed; re-export from Word on a machine with Times New Roman before submission |
| Line spacing | 1.5 (body); 1.15 in compact table text | DOCX paragraph styles | Assumed |
| Alignment | justified body; centred chapter titles and captions | visual inspection (title page, front matter, Chapter 1 opening, sample body pages) | Assumed |
| Table text | 10 pt | `docx_structure.txt`: 0 table runs not 10 pt (3,515 table runs) | Assumed |
| Captions | "Table N.M." above tables; "Figure N.M." below figures | List of Tables / List of Figures: every caption has a page number (build log: `captions without page {'LOF': 0, 'LOT': 0}`) | Assumed convention |
| Page numbering | lower-case Roman for preliminary pages (i–xxii); Arabic from Chapter One (1–215); title page counted but not numbered | `pdf_properties.txt`: physical page 2 → "ii", 20 → "xx", 23 → "1", 237 → "215" | Assumed convention (common) |
| Chapter starts | each chapter on a new page; "CHAPTER ONE: INTRODUCTION" style headings | visual inspection | Assumed |
| Equations | 25 native Word (OMML) equations, numbered (Ch2: 3; Ch3: 22) | structure log (`math_nor_and_sty` 0); content check: 25 = R5 | — |
| Tables / figures | 57 tables in the DOCX = 57 table captions (the content check counts 58 because one body sentence in §2.11 begins with "**Table 2.8**" when pointing to Appendix 2A); 10 figures at 300 dpi | build log; content check | — |
| Arabic abstract | right-to-left paragraph direction, Arabic font DejaVu Sans in the PDF | visual inspection (page xxi) | Arabic font and spelling of names to be checked by the student |
| Tracked changes / comments | none | `tracked_changes_comments.txt`: 0 w:ins, 0 w:del, 0 w:comment in all 6 DOCX files | — |
| Blank pages | none | margin scan: 0 near-blank pages | — |
| DOCX structural validity | all 6 files PASS (run properties order, paragraph properties order, idempotent table formatting) | `docx_structure.txt` | — |

## 3. Preliminary pages (order as built)

| # | Page | Content status |
|---|---|---|
| i | Title page | Title, university, faculty/department, student, supervisor, co-supervisor, degree, month/year, "Draft for supervisor review — not approved". Faculty, department and degree **not verified** (N-2). |
| ii | Committee Decision | **Placeholder**; no names, date or signature inserted. |
| iii | Declaration of Authorship and Originality | **Placeholder**, unsigned; a factual (non-declaratory) note on AI assistance. |
| — | Dedication; Acknowledgement | **Placeholders** for the student. |
| — | Table of Contents | Word TOC field, populated at export (LibreOffice index update). |
| — | List of Tables; List of Figures | Filled from captions with displayed page numbers (2–3 passes until stable). |
| — | List of Abbreviations | From the R5 front matter. |
| — | Abstract (English) | R5 abstract plus one sentence on the live harness. |
| xxi | الملخص (Arabic abstract) | AI-assisted draft translation; requires the student's review. |
| xxii | Status of This Draft | Lists the draft's limits (restructuring, exploratory evidence, live status, formatting assumed, unverified metadata, Arabic draft, placeholders). |

Nothing on these pages signs, affirms or approves anything on behalf of the student, the
committee or the university.

## 4. Visual inspection performed

Rendered pages were inspected: title page; committee and declaration placeholders; TOC; List of
Tables; List of Figures; abbreviations; English and Arabic abstracts; Status page; the opening of
each chapter; every page with a new figure (Figures 1.1, 3.2–3.5, 4.3); sample table-heavy pages in
Chapters 2–4; the References. Defects found and fixed during the build (see the build history):
figure text overflow and overlapping labels (Figures 1.1, 3.2, 3.3, 3.5, 4.3); TOC heading in a blue
sans-serif style; title-page paragraph-property order; a near-blank page caused by the Arabic
translation note (moved to the Status page).

## 5. Not verified / to do before submission

1. Obtain the university's formatting rules (or the reference thesis) and compare margins, fonts,
   spacing, heading styles, caption placement and page-number placement.
2. Open the DOCX in Microsoft Word, update all fields (TOC, lists), and export the PDF on a
   machine with Times New Roman; recheck the page numbers in the lists.
3. Confirm the order of preliminary pages required by the university (e.g. whether the Arabic
   abstract precedes or follows the English abstract, and whether a "Status" page is allowed — it
   should be removed in the submission version).
4. Replace the placeholders with the official committee page and the signed declaration.
