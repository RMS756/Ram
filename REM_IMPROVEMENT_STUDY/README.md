# REM improvement study (13 November 2026)

**Status: `[PROPOSED — EXPLORATORY — NOT PART OF THE APPROVED REM DESIGN]`.** Isolated investigation on branch `claude/rem-improvement-study` (from `1e84c14`). REM v1.0, the proposed v1.1, their configuration and all earlier result files are unchanged. Every result is development evidence from recorded-trace replay; no live agent and no language model was used.

| # | Deliverable | File |
|---|---|---|
| 1 | Source of truth and closest-prior-art matrix | `01_SOURCE_OF_TRUTH_AND_PRIOR_ART.md` |
| 2 | Failure-to-mechanism map and candidate decision | `02_FAILURE_MAP_AND_CANDIDATE_DECISION.md` |
| 3 | Frozen development protocol; sealed prospective protocol (not executed); split manifest and hashes; fixture set 4 | `protocol/`, `fixtures/` |
| 4 | Implementation, pinned dependencies, commands, tests, budget and blockers | `04_IMPLEMENTATION_AND_TESTS.md`; code in `experiments/improve_study/`; tests in `tests/test_improve_study.py` |
| 5 | Results, exclusions, uncertainty, ablations, failure cases | `05_RESULTS.md`; `results/improvement_results.json`, `results/tables.md`, `results/failure_analysis.json`; `logs/` |
| 6 | Final verdict | `06_FINAL_VERDICT.md` |
| 7 | Chapter 4 in the supervisor's six sections, with the requirement-to-section and evidence matrix | `REM_FINAL_SUBMISSION/thesis_r2/` (previous edition kept in `REM_FINAL_SUBMISSION/thesis/`) |

**One-paragraph result.** A deterministic rule that compiles what the user asked for from the request and matches each state-changing call on operation, recipient and amount (G1) completes more benign tasks than REM v1.0 on both recorded populations with no more successful attacks. Against the strongest simple rule of the earlier studies (A2) its point estimates are better on both outcomes, but the task-completion intervals include zero, so added value over simple rules is not established. Progent's published manual banking policy, replayed in the same harness, has no successful attack and is better on security. A ridge model given the same permission evidence adds no demonstrated value and is less robust to reformatted identifiers. The gain is due to the hard rule, not to the learned core.

**Order of events.** Protocol, candidate code, fixture set 4 and the prospective protocol were committed (`9137b03`) before any new arm was replayed. Analysis code (`report.py`, `tables.py`, `failures.py`) was written afterwards and changes no arm. No amendment to the protocol was made.
