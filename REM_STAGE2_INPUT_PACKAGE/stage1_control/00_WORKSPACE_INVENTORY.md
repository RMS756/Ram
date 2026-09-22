# 00 — Workspace Inventory

Recorded 2026-09-22. Read-only survey of the thesis workspace before any file in `REM_AUDIT_OUTPUT/` was written.

Root: `D:\Documents\REM`

## Thesis deliverables (source of truth, not modified by this stage)

| File | Size (bytes) | Last modified |
|---|---|---|
| `Chapter2_Literature_Review.docx` | 26,190 | 2026-09-17 |
| `Chapter2_Literature_Review.md` | 54,407 | 2026-09-17 |
| `Chapter3_Methodology.docx` | 45,058 | 2026-09-17 |
| `Chapter3_Methodology.md` | 83,976 | 2026-09-17 |
| `Stage3_Change_Log_and_Verification.docx` | 18,265 | 2026-09-17 |
| `Stage3_Change_Log_and_Verification.md` | 24,894 | 2026-09-17 |
| `~$apter2_Literature_Review.docx` | 162 | 2026-09-17 |

## Build tools

| File | Size (bytes) | Purpose |
|---|---|---|
| `tools/build_docx.py` | 20,370 | Dependency-free Markdown to DOCX writer used for every DOCX deliverable |
| `tools/fix_citations.py` | 3,829 | APA-7 initial disambiguation for shared surnames |

## Previous literature-audit stage

`literature_audit/` contains 72 files (66 Markdown, 3 Python, 3 JSON). These are inputs to the present stage and were not modified.

## Environment constraints recorded at the start of this stage

| Capability | Status |
|---|---|
| Python | 3.13, standard library only (no third-party packages installed) |
| Microsoft Word (COM) | Available; used only for visual inspection of generated DOCX files |
| Node.js / pandoc / LibreOffice / PDF library / poppler | Not available |
| External AI-detection tool | Not available; no detector was executed in this stage |
| web.archive.org | Blocked in this environment; not worked around |
| SSRN full text (Jackson, 2025) | HTTP 403; not worked around |
| Publisher host for Brier (1950) | HTTP 403; not worked around |
