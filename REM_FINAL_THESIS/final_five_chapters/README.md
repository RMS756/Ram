# REM Thesis — Five-Chapter Version (3 November 2026)

**Status:** draft for **supervisor review**; formal submission **blocked**
(`audit/FINAL_SUBMISSION_READINESS.md`). **The live AgentDojo experiment was NOT executed; no
live result exists.**

| Deliverable | File |
|---|---|
| Full thesis (Word, PDF; 241 A4 pages; i–xxii + 1–219) | `REM_THESIS_5CH_FINAL.docx`, `REM_THESIS_5CH_FINAL.pdf` |
| Chapters | `chapters/CHAPTER1_INTRODUCTION.docx` … `CHAPTER5_CONCLUSIONS.docx`; Markdown sources in `src/` |
| Appendices | `appendices/EXPERIMENT_REPRODUCTION.md`, `appendices/LIVE_AGENTDOJO_DETAILS.md` |
| Audits | `audit/THESIS_SOURCE_MAP.md`, `SCIENTIFIC_CLAIM_AUDIT.md`, `REFERENCES_AUDIT.md`, `FORMATTING_AUDIT.md`, `EXPERIMENT_STATUS.md`, `UNRESOLVED_SUPERVISOR_DECISIONS.md`, `FINAL_SUBMISSION_READINESS.md`; QA logs in `audit/qa_logs/` |
| Figures (10 in the thesis; the 6 new ones here, 300 dpi) | `figures/` |
| Tables (all 57, CSV, exported from the text) | `tables/INDEX.md`, `tables/Table_*.csv` |
| Result pointers, test logs, live-harness smoke summary | `experiment_results/` |
| Live-experiment documents (8) | `../../experiments/live/*.md` |

**Source:** R5 (`../chapters_R5/`), read and never modified. Mapping R5 → five chapters:
Ch1→1, Ch2→2, Ch3→3 (§3.1–3.15), Ch4→§3.16, Ch5→Ch4 (§4.1–4.11) and §5.2, Ch6→§4.15–4.17 and Ch5. New §4.14 (5 Nov 2026): MELON with and without REM — implemented protocol, not executed.

Rebuild (from the repository root; needs pandoc, python-docx, lxml, matplotlib, LibreOffice):

```bash
python3 REM_FINAL_THESIS/tools/figures_5ch.py
python3 REM_FINAL_THESIS/tools/make_5ch.py
python3 REM_FINAL_THESIS/tools/build_5ch.py
python3 REM_FINAL_THESIS/tools/check_5ch.py
python3 REM_FINAL_THESIS/tools/qa_5ch.py
python3 REM_FINAL_THESIS/tools/tables_5ch.py
python3 REM_FINAL_THESIS/tools/source_map_5ch.py
```

`build/` holds intermediate build files and is git-ignored.
