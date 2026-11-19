# Change log: REM vs MELON (branch claude/rem-melon-comparison-20261119, from f4ff23f)

## 19 Nov 2026

**Added**
- `experiments/rem_vs_melon/`: harness, scripted pilot, live runner, configuration template, analysis, summary, workload estimate, figure.
- `tests/test_rem_vs_melon.py`: 9 tests.
- `REM_MELON_COMPARISON_2026_11_19/`: deliverables 01–14, results, figures, manifests, logs.

**Freeze**
- Protocol 04/06 and the code hashes were committed at `a1db36a`, before any scored episode.

**Pilot fix (test double only)**
- The scripted agent now recognises the injected payload by its fixed `<INFORMATION>` marker, after smoke run 1 showed that it never saw the payload.
- REM and MELON were not changed.

**Unchanged**
- REM v1.0 (`rem/` decision path), the frozen REM bundle, upstream MELON, `rem/integration/melon_rem.py`, and R8 (thesis and deliverables).

**Not executed**
- Live closed-loop runs of any arm.
- MELON with `text-embedding-3-large`.
- Replay-based or detector-only MELON analyses (not supported by MELON's algorithm).
