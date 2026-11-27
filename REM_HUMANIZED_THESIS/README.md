# REM thesis: humanized edition (27 November 2026)

| Path | Content |
|---|---|
| `REM_Master_Thesis_Humanized.docx` / `.pdf` | The revised thesis (272 pages; the PDF is an export of the DOCX and matches an independent re-export on every page) |
| `original/` | The defence-ready thesis before this revision (unchanged; also unchanged in `REM_DEFENCE_READY_THESIS/`) |
| `reports/01_HUMANIZATION_COVERAGE_REPORT.md` | Stage 1: chapter-by-chapter coverage and measured effect |
| `reports/02_Q1_ACADEMIC_REVIEW_REPORT.md` | Stage 2: independent academic review |
| `reports/03_SCIENTIFIC_INTEGRITY_REPORT.md` | Preservation and verification of numbers, citations, equations, tables, identifiers, architecture |
| `reports/04_CHANGE_LOG.md` and `reports/EDIT_LIST.md` | Significant changes, and all 118 edits with before and after |
| `reports/05_UNRESOLVED_ISSUES_REPORT.md` | Category C items for the supervisor (not implemented) |
| `reports/06_PUBLICATION_READINESS_ASSESSMENT.md` | Candid assessment for journal publication |
| `orig_src/`, `edits/`, `src/`, `text_front/`, `references/` | Original sources, edit lists, revised sources |
| `tools/` | `apply_edits.py`, `check_preservation.py`, `build_h.py` (copy of the defence-ready build), number and citation checkers |
| `audit/` | Outputs of every check, including `stage4_qc.txt` |

Reproduce from the repository root:

    python3 REM_HUMANIZED_THESIS/tools/apply_edits.py
    python3 REM_HUMANIZED_THESIS/tools/check_preservation.py
    python3 REM_HUMANIZED_THESIS/tools/build_h.py
    python3 REM_HUMANIZED_THESIS/tools/check_thesis_numbers.py
