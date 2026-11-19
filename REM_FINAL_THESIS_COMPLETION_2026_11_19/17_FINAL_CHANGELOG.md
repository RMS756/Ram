# 17 Final changelog (19 November 2026)

Branch `claude/rem-final-thesis-completion-20261119`, from `bf36381`.

## Code (no file of REM v1.0 or of the frozen pilot pipeline was modified)

| File | Change |
|---|---|
| `experiments/final_thesis/ablation_run.py` | **new.** Arms B0, A0–A7 (A5 and A6 as configurations of the frozen `A3Policy` and `PredicatePolicy`), reachability, latency, calibration and paired contrasts. Frozen at `dc8407d`. |
| `experiments/final_thesis/external_run.py` | **new.** Recorded closed-loop outcomes of D0–D4 and REM v1.0 replay on their traces. Frozen at `dc8407d`; amended (05a: E1 tool_filter not replayable, E2 latency crash) at `204f7ad`. |
| `experiments/final_thesis/make_figures.py`, `make_tables.py`, `export_raw.py` | **new.** Figures, tables (with the post-hoc descriptive files) and raw CSV exports, all from stored outputs. |
| `tests/test_final_thesis_completion.py` | **new.** 8 consistency and integrity tests: gate, protocol hashes, paired differences against counts, reachability partition, A5 equivalence, CSV and JSON, external completeness, generated tables. |

## Study documents

`01`–`17`, `05a`, `README.md`; `results/`, `figures/`, `logs/` and `manifests/` in `REM_FINAL_THESIS_COMPLETION_2026_11_19/`.

## Thesis R8 (`REM_FINAL_SUBMISSION/thesis_r8/`; R7 unchanged)

**Tools**
- `tools/make_r8.py` and `tools/spec_r8.py` assemble R8 from R7 plus the dated fragments in `text_r8/`.
- `tools/build_final.py` is copied from R7, with only the output folder and name changed. It uses the same pinned rendering environment.

**Chapter 4**
- Section 4.4.2 replaced: recorded closed-loop outcomes on 144 runs (R7's 143 explained), REM replay on the defences' traces, paired and cross-kind contrasts. Tables 4.11a–4.11c; Figure 4.1.
- New Section 4.5.5: final pre-registered ablation. Tables 4.21a–4.21e; Figures 4.2–4.4.
- New Section 4.5.6: exploratory redesign studies of 18–19 November (not adopted).
- Introduction, Table 4.3, sources paragraph, 4.5 introduction, Table 4.39 (rows 12–13) and chapter summary updated.
- Figures 4.1–4.3 of R7 are now Figures 4.5–4.7. Existing table numbers are unchanged.

**Other chapters**
- **Chapter 1:** contribution 8 added; the "does not demonstrate" bullet on external comparison reworded.
- **Chapter 3:** Section 3.11.7 documents the final ablation's arms and the status of the distributed-defence comparison.
- **Chapter 5:** Table 5.1 (RQ4), Table 5.2 (O3), Table 5.3 (contribution 9), limitation 10 and the conclusion updated.
- **Appendix B:** new decision SD-ARCH.

**Front matter**
- Edition statement dated 19 November 2026, still "draft for supervisor review".
- English and Arabic abstracts extended by one passage each.

**Unchanged:** Chapter 2 and every equation (checked by `make_r8.py`).

**Outputs**
- `REM_THESIS_EDITORIAL_R8.docx` and `.pdf` (230 pages), copied as `REM_THESIS_FINAL.docx` and `.pdf`.
- Chapter Markdown files copied as `CHAPTER_n_FINAL.md`.

## Historical results

None modified. `results/pilot_R2`, `results/pilot_R4` and all earlier study folders are unchanged. The fresh reproduction is stored separately as `results/fresh_pilot_*.json`.
