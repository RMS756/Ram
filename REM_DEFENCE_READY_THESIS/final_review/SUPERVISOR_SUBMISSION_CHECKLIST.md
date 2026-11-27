# Supervisor-submission checklist (27 November 2026)

**Status values:**
- **Corrected:** done and verified in the built files.
- **Verified:** checked, no change needed.
- **Pending:** must be done by the student before sending.
- **Confirm:** needs a supervisor or university decision.

## Mandatory items from the brief

| Item | Status | Verification |
|---|---|---|
| Committee page no longer claims a defense or approval | Corrected | Rendered page ii: "This thesis has not yet been defended." Test `test_final_review_corrections_present`. |
| Figures 4.6–4.8 use the labels of Tables 4.25–4.31 | Corrected | Regenerated from stored results; counts asserted against raw records; rendered pages inspected |
| Table 4.27 contains only percentage-point differences (with intervals, discordant counts, p) | Corrected | 498 cells checked, 0 mismatches; rendered page inspected |
| DOCX and PDF consistent | Corrected | Independent re-export of the DOCX: 272 = 272 pages (rebuilt 27 November after the Future Work addition), identical text on every page, TOC, LoT and LoF on the same pages |
| LoT and LoF updatable in Word | Corrected | Word TOC fields on the caption styles; `updateFields` set in the DOCX |
| Ablation described as component-level, with limits stated | Verified | Sections 4.5.1, 4.5.4, 4.5.5, 4.5.11; threat 21; abstract |
| Framework comparison fair; kinds of evidence distinguished | Verified | Section 4.4; `FRAMEWORK_COMPARISON_VALIDATION.md` |
| No tool names in the thesis body or front matter | Corrected | No "Claude" or "ChatGPT" in the thesis. The remaining "claude-3-haiku" is the name of a recorded benchmark backbone (research data). |

## Scientific content

| Item | Status |
|---|---|
| Title, topic, scope, five-layer architecture unchanged | Verified |
| Unimplemented injection classifier no longer described as in use (Section 3.5) | Corrected |
| Numerical results consistent with the raw records | Verified |
| Offline replay never described as live; no deployment claim | Verified |
| Negative findings and limitations preserved | Verified |
| RQs and design values marked as not approved | Verified (U-2, U-3: Confirm) |
| Appendix B updated (DRIFT in D-15; SD-ABL; SD-CMP) | Corrected |
| Component-level ablation accepted as answering the request | Confirm (U-4) |
| Scope of the DRIFT and MELON comparison accepted | Confirm (U-11) |

## References

| Item | Status |
|---|---|
| 106 entries (Arike et al., 2025, added with Future Work item 13), all cited; no citation without an entry | Verified |
| DRIFT and AgentDyn bibliographic data | Verified with Crossref, OpenAlex and repositories; author names need a final PDF check (U-12: Pending) |
| Full re-verification of all other entries | Not repeated in this round (U-13) |

## Formatting and production

| Item | Status |
|---|---|
| Open the DOCX in Word with Times New Roman; update all fields (Ctrl+A, F9); save; export the PDF from Word | Pending (U-5) |
| Check wide tables (4.12, 4.25, 5.3) in Word | Pending |
| University template | Confirm (U-14) |
| Title-page faculty, department, degree, supervisor titles | Confirm (U-6) |

## Front matter

| Item | Status |
|---|---|
| Committee page completed by the university | Pending, after the defense (U-7) |
| Declaration of originality in the university's wording; any declaration on AI tools | Confirm (U-1, U-7) |
| Dedication, acknowledgement | Pending (student) |
| Arabic abstract language review | Pending (U-8) |

## Files to send

1. `REM_Master_Thesis_Defence_Ready.pdf`: the corrected thesis, 272 pages.
2. `REM_Master_Thesis_Defence_Ready.docx`: the editable source.
3. Optional companions:
   - `SUPERVISOR_REQUIREMENTS_MAPPING.md`
   - `ABLATION_LAYER_COVERAGE_MATRIX.md`
   - `FRAMEWORK_COMPARISON_VALIDATION.md`
   - `final_review/ACADEMIC_REVIEW_REPORT.md`
