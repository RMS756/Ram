# REM Final Thesis: R3 Verification Draft (30 October 2026)

**Status:** ready for **supervisor review**. **Not** ready for formal submission (see `reports/FINAL_SUBMISSION_READINESS_REPORT.md`).

## Required deliverables

| # | Deliverable | File |
|---|---|---|
| 1 | Full thesis (Word) | `REM_FINAL_THESIS.docx` |
| 2 | Full thesis (PDF, 218 pages A4) | `REM_FINAL_THESIS.pdf` |
| 3 | Chapters 1–6 | `CHAPTER{1..6}_*_FINAL.docx`; Markdown sources in `chapters/` |
| 4 | Verified references | `REFERENCES_VERIFIED.md` (status of each of the 113 entries); list in `chapters/REFERENCES.md` |
| 5 | Source verification log | `reports/SOURCE_VERIFICATION_LOG.md` |
| 6 | Equation verification | `reports/EQUATION_VERIFICATION_REPORT.md`; `verification/verify_equations.py` |
| 7 | Methodology–code traceability | `reports/METHODOLOGY_CODE_TRACEABILITY.md` |
| 8 | Results provenance | `reports/RESULTS_PROVENANCE_REPORT.md` |
| 9 | Experiment reproduction guide | `reports/EXPERIMENT_REPRODUCTION_GUIDE.md` |
| 10 | Cross-chapter consistency, with the RQ → Method → Code → Experiment → Result → Conclusion matrix | `reports/CROSS_CHAPTER_CONSISTENCY_REPORT.md` |
| 11 | Unresolved items and supervisor decisions | `reports/UNRESOLVED_ITEMS_AND_SUPERVISOR_DECISIONS.md` |
| 12 | Submission readiness, per-chapter YES/NO | `reports/FINAL_SUBMISSION_READINESS_REPORT.md` |
| — | Examiner-style review (CRITICAL / MAJOR / MINOR) | `reports/EXAMINER_REVIEW.md` |
| — | Inventory and source selection; change log | `reports/00_PROJECT_INVENTORY.md`; `reports/CHANGE_LOG_R3.md` |

## Rebuilding

```bash
python3 REM_FINAL_THESIS/tools/make_r3.py               # R2 chapters + scripted, logged R3 corrections
python3 REM_FINAL_THESIS/tools/build_references_verified.py
python3 REM_FINAL_THESIS/tools/build_thesis.py           # DOCX + PDF (needs pandoc, LibreOffice with libreoffice-math)
```

`verification/` holds every check run on 30 October 2026, with its output.
