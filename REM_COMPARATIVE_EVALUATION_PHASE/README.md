# REM comparative evaluation phase (22 November 2026)

- **Branch:** `claude/rem-comparative-evaluation-20261122`.
- **Start:** `76ac629`.
- **Protocol frozen:** `09d49c0`, before any scored run.

**What ran:**
- offline replay;
- reference-solution evaluation;
- scripted integration tests.

**What did not run:** no live model run, no paid call. REM, R8 and earlier studies are unchanged.

## Files

| File | Content |
|---|---|
| `01_EXPERIMENTAL_PROTOCOL.md` | Frozen protocol for D0–D4 (live, blocked items) and offline section O |
| `01a_AMENDMENTS.md` | Amendment 1 (runner report key) |
| `01_PROTOCOL_HASHES.sha256`, `01a_AMENDMENT_HASHES.sha256` | Hashes, checked by a test |
| `02_PROGENT_IMPLEMENTATION_AND_RESULTS.md` | Source, oracle analysis, reference-solution and offline results |
| `03_DRIFT_IMPLEMENTATION_AND_RESULTS.md` | Agent changes, D4 control, scripted integration and call counts |
| `04_MELON_STATUS_AND_COMPATIBILITY.md` | Pending; what is missing |
| `05_REM_ABLATION_DESIGN.md` | Layer map and ablation arms |
| `06_ABLATION_RESULTS.md` | Episode-level ablation results |
| `07_STATISTICAL_ANALYSIS.md` | Units, pairing, intervals, exclusions |
| `08_REPRODUCIBILITY_AND_HASHES.md` | Pins, hashes, commands |
| `09_THESIS_READY_RESULTS.md` | Thesis-ready table and interpretation |
| `10_PENDING_DECISIONS_AND_LIMITATIONS.md` | Blocked decisions and limitations |

## Code, data and tests

- **Code:** `experiments/comparative_phase/`.
- **Results and logs:** `results/`, `logs/`.
- **Tests:** `tests/test_comparative_phase.py`.
