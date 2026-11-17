# Change log: seventh edition (condensed editorial edition, updated), 17 November 2026

**Files:**
- main text: `REM_THESIS_EDITORIAL_R7.docx` and `.pdf`;
- supplement: `supplement/REM_THESIS_R7_SUPPLEMENT.docx` and `.pdf`.

**Status:** editorial draft for supervisor review. It is not approved, not submitted and not ready for submission. R5 and R6 are unchanged. R7 is assembled by the same tool and specification as R6 (`tools/make_r6.py`, `tools/spec_r6.py`), with the changes below. See `../thesis_r6/CHANGE_LOG_R6.md` for everything R6 changed relative to R5.

## Changes relative to R6

| Change | Where | Source |
|---|---|---|
| Version 2 of the amount verifier: defects D3 and D4, the repair, the separate grammar extension, results on recordings and fixtures, and the new over-blocking failure (fixture S1). Generated from the result files (`tools/gen_r6.py` + `tools/gen_r7_v2.py`) | Section 4.5.4, Table 4.21 | `REM_REPAIR_STUDY_2026_11_17/` (amendment `95549b2`) |
| **Corrected statement of the stage order.** The version-1 verifier was computed for every call; the statement is now "for no benchmark-labelled attack call could the verifier's or the learned decision's output change the release". For version 2 the stronger statement holds literally | 4.5.4 | second review, section on stage order |
| Paragraph F of 3.14 extended with version 2 | 3.14 | — |
| Threat 19, Chapter 4 summary, rejected-variants row of Chapter 5, decision SD-AMT | 4.6.11, 4.6.12, 5.5, Appendix B | — |
| Section 2.8.3 (NEXUS) condensed. The full R5 text is in the supplement | 2.8.3 | second review, recommendation 6 |
| Abstracts (English and Arabic) and status page | front matter | — |

## Size and verification

| Item | R6 | R7 |
|---|---:|---:|
| Total pages | 212 | 212 |
| Chapters 1–5 (printed pages) | 168 | 168 |
| Tables / figures / equations | 65 / 9 / 25 | 66 / 9 / 25 |
| Page references checked (mismatches) | 150 (0) | 151 (0) |
| Reference entries (all cited; reverse check clean) | 103 | 103 |
| Supplement pages | 124 | 126 |

The page target of about 145–160 is **still not reached**. The second review notes correctly that most of the R6 reduction came from the appendices, and that the body was shortened by only 12 pages. Reaching the target needs paragraph-level rewriting of Chapters 3 and 4. That is a supervisor decision about which method and result text may leave the main body; candidates are listed in `../thesis_r6/CHANGE_LOG_R6.md` §2.

**Still to complete:**
- the PACT author list (3 of 6 known; arXiv not reachable from this session);
- a re-check of the MELON page range against PMLR.

Numbers in the new text: 196 distinct numbers. Those not found in any result file or in R5 are CapLite's 29.0 and 27.2 (taken from its indexed abstract) and three temporary table numbers (`audit/number_audit_r6.json`). Pages 126–127 (the new table) were inspected after rendering; not all pages were.
