# Change log: thesis draft of 12 November 2026 → second edition of 14 November 2026

**Status:** draft for supervisor review; not approved; not submitted. **The first edition is preserved unchanged** in `REM_FINAL_SUBMISSION/thesis/` (commit `1e84c14`). This edition is in `REM_FINAL_SUBMISSION/thesis_r2/`.

## Files

| Output | Path |
|---|---|
| Chapters (Markdown) | `src/CHAPTER_01_FINAL.md` … `src/CHAPTER_05_FINAL.md`, `src/APPENDICES_FINAL.md` |
| Chapters (Word) | `docx/CHAPTER_01_FINAL.docx` … `docx/CHAPTER_05_FINAL.docx`, `docx/APPENDICES_FINAL.docx`, `docx/REFERENCES_FINAL.docx` |
| Combined thesis | `REM_THESIS_FINAL_R2.docx`, `REM_THESIS_FINAL_R2.pdf` (306 pages: preliminary pages i–xxvii; main text pages 1–175; references from 176; appendices A–F from 191) |
| Build | `tools/gen_ch4_r2.py` + `tools/ch4_r2_template.md` (new Chapter 4 text with tables generated from the result files), `tools/make_final.py`, `tools/spec_final.py`, `tools/build_final.py`, `tools/docx_layout_r2.py`, `tools/check_layout.py`, `tools/audit_numbers_r2.py` |
| Audit | `audit/CHAPTER4_REQUIREMENT_MATRIX.md`, `audit/CLAIM_AUDIT_R2.md`, `audit/final_source_map.json`, `audit/final_crossref_check.txt` |

Rebuild from the repository root:

```bash
python3 REM_FINAL_SUBMISSION/thesis_r2/tools/gen_ch4_r2.py
python3 REM_FINAL_SUBMISSION/thesis_r2/tools/make_final.py
python3 REM_FINAL_SUBMISSION/thesis_r2/tools/build_final.py
python3 REM_FINAL_SUBMISSION/thesis_r2/tools/check_layout.py REM_FINAL_SUBMISSION/thesis_r2/REM_THESIS_FINAL_R2.pdf
```

## Length

| Part | First edition | Second edition |
|---|---|---|
| Main text (Chapters 1–5) | 146 pages | 175 pages |
| Chapter 4 | 38 pages | 61 pages |
| Whole document | 284 pages | 306 pages |

Chapter 4 grew because of the three new sections asked for by the supervisor (tools and environment; setup and metrics; training) and the extension study. If a page limit applies, the candidates for an appendix are the per-task tables, the intervention-burden table and the diagnostic arms; nothing was moved without a decision.

## Changes by chapter

| Chapter | Change |
|---|---|
| 1 | Research methodology: fifth part (exploratory extension). Contributions: item 4 reworded (gain in task completion confirmed; security not resolved), item 6 limited to the tested policies, new item 7 (extension and attribution result); "not demonstrated" and "not claimed" lists updated. Test count updated. Organization paragraph for Chapter 4 |
| 2 | NEXUS section: repository read on 13 November; the authors' working document on the scorer against rules. Update table: reading levels (A, R), aiAuthZ from its repository whitepaper, new rows for Progent and CaMeL; note on what could not be read and why |
| 3 | New Section 3.14, exploratory extension (request compiler, typed matching, two-verdict decision, verifier interface, arms, relation to prior work, limits). Outcome-layer table: "unauthorized state-change rate" renamed "rate of episodes with a released attack-labelled call", with the reason. GO verdict stated as a decision rule and not a non-inferiority test. Test count updated |
| 4 | **Reorganized into six sections** (see `audit/CHAPTER4_REQUIREMENT_MATRIX.md`). New: 4.1.1–4.1.3, 4.2.4, 4.3 (all), 4.4.3, 4.5.2, 4.5.3, 4.6.9. Corrected: see below |
| 5 | Answers to RQ2 and RQ4, objective O3, contribution table (items 5 and 7 reworded, item 8 added), "not confirmed" and "rejected variants" lists, negative finding 3, limitations 6, 9 and 10, future work 2, 4 and 7, conclusion (a fourth finding added) |
| Front matter | Both abstracts (corrections and one paragraph on the extension); status page; title-page date |
| Appendix F | New decision SD-PERM; SD-FEAT, D-15, RULES, FULLTEXT and the NEXUS items updated |
| References | Reading-level notes on NEXUS, aiAuthZ, Progent and CaMeL. No entry added or removed |

## Corrections of statements of the first edition

| # | First edition | Second edition | Basis |
|---|---|---|---|
| a | "Calibration changed no outcome / no decision"; "No material change was observed from removing [calibration]" | Without calibration the attack count is unchanged (11 of 2,979) and benign task completion is 110 instead of 105 of 334 | Table 4.17 (0.329 against 0.314); abstract, Chapters 4 and 5 |
| b | "REM v1.0's results do not change when the user task is also held out" | The attack count (11) and the benign task count (105) are the same; tasks under attack (1,083 and 1,078) and released calls (33 and 35 of 178) differ | `improvement_results.json`, S1 and S2 |
| c | "No policy … separates …"; "the fact … is not among the inputs"; "authorization cannot be read from text" | Limited to the features and policies tested up to 11 November; the request text does contain the user's statement, and one deterministic parser used it on most author-written cases | Sections 4.6.7, 4.6.9, 4.6.10 |
| d | "The verdict is GO … confirmed" | GO is the outcome of a pre-declared decision rule; it is not a test of non-inferiority; the security interval includes zero; 14 against 11 under the double holdout is restated | Section 4.6.8 |
| e | Column and metric "unauthorized state change" | "Episodes with a released attack-labelled call", a proxy that is not a measured change of the bank state | Chapters 3 and 4 |
| f | NEXUS, aiAuthZ, Kairos "abstract only" | NEXUS and aiAuthZ also from the authors' repositories (read, not executed); Kairos still abstract only; full texts still not read | Chapter 2; Table 4.16; references |
| — | "untouched recordings" (present tense) | "recordings unread before that run"; since the run they are development evidence | all chapters |
| — | "No published defense was run" | One published policy (Progent's manual banking policy) was replayed; no defense that needs a language model was run | Sections 4.4.3 and 4.4.4 |

## Formatting

| Item | First edition | Second edition |
|---|---|---|
| Table of contents in the Word file | The field had an empty stored result; it was filled only in memory for the PDF | The entries (254, with page numbers) are stored in the field result of the DOCX and equal the contents pages of the PDF (`audit/toc_entries.json`; checked by script) |
| Tall tables | Every table of up to 25 rows was kept on one page and no row could break, which left headings and captions alone on nearly empty pages | Tables estimated taller than about half a page may break between rows, and very tall rows may break inside; the header and first rows stay with the caption |
| Near-empty pages (`tools/check_layout.py`, pages under 90 words that are not the last page of a chapter or appendix) | 6, among them the divider page before the appendices and 3 pages on which a table caption was separated from its table | 1 short page (before a figure); no caption separated from its table; divider page removed |
| Equations | 25 editable (OMML) | 25 editable (OMML), unchanged |
| Contrast tables | — | Short labels so that the first column does not wrap |

## Not changed

`rem/`, `configs/`, every earlier result file, the MELON bundle, the first edition of the thesis and all earlier versions. Placeholders (committee page, declaration, dedication, acknowledgement) and all supervisor decisions remain pending.
