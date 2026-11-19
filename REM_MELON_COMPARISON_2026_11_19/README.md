# REM v1.0 vs MELON vs no defence (AgentDojo banking): 19 November 2026

**Status: the live comparison is NOT EXECUTED.** There is:
- no language model, local or API;
- no MELON embedding endpoint;
- no spending authorisation;
- no network route to any of them in this session (`03`, `14`).

**No REM or MELON attack-success or utility result exists**, and none is reported. R8 remains the valid thesis.

## Done

| Item | Where |
|---|---|
| REM v1.0 and R8 verified; R8 unchanged | `01` |
| Official MELON pinned and audited. `ucsb-mlsec@06014c7` and `kaijiezhu11@4d3cc9c` have an identical `pi_detector.py`; the README's `ContrastPIDetector` does not exist, and the real class is `MELON`. | `02` |
| Three-arm closed-loop harness and fail-closed live runner, using unmodified MELON | `experiments/rem_vs_melon/` |
| Scripted integration pilot: 480 episodes, 0 errors, every mechanism active. Scripted agent; **not a result.** | `05`, `results/scripted_pilot_full/` |
| Protocol frozen with hashes before any scored episode (`a1db36a`) | `04`, `06` |
| Workload planning estimate: MELON adds about 73% model calls and about 138% input characters; REM adds none (0.27 ms of CPU per call) | `10`, `figures/` |
| Thesis feasibility subsection (proposed; R8 not overwritten) | `12` |
| Arabic report | `13` |
| Tests: 9 new, passing (MELON environment) | `tests/test_rem_vs_melon.py` |

## Files

01 baseline · 02 MELON audit · 03 compute · 04 fairness · 05 pilot log · 06 frozen protocol (+ hashes) · 07 results CSV (live rows NOT EXECUTED) · 08 security–utility (no data; pre-recorded hypotheses) · 09 statistics plan · 10 latency and cost · 11 manifest · 12 Chapter 4 addendum · 13 Arabic report · 14 status, blockers and answers · CHANGELOG
