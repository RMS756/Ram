# REM competitive study, 16 November 2026

**Status:** `[PROPOSED - EXPLORATORY - DEVELOPMENT EVIDENCE]`. Local work only: nothing is pushed, published or merged. The approved REM design, every earlier study and result file, and all thesis editions are unchanged.

**One-paragraph result.** Behind the request-derived authority front, the guard used alone (GV) has exactly the outcomes of HV and of every learned or statistically calibrated variant tested (Neyman-Pearson cutoff, conformal-risk-control cutoff, gradient-boosted trees, no calibration, four verdicts): no successful attack and 1,532 of 3,313 and 1,386 of 2,113 completed tasks. Every attack-labelled call is stopped by the deterministic front, so no learner has anything to decide but legitimate work. Against the one Progent configuration that can be run here (its manual banking policy, in replay) nothing is resolved. No superiority is claimed.

| File | Content |
|---|---|
| `00_SOURCE_OF_TRUTH_AND_REPRODUCTION.md` | Attachments, how the package was applied, reproduction audit, test suite |
| `01_PROGENT_READING_NOTE.md` | Full-text reading note (v3, 17 pages) with page anchors; paper-to-code differences; comparison with REM, G3, L4, HV |
| `MATHEMATICAL_SOURCE_REGISTRY.csv` | Sources of every method, with the verification level of each |
| `CANDIDATE_FEASIBILITY.md` | Candidates compared before scoring |
| `PROTOCOL.md`, `PROTOCOL_ADDENDUM_SECTION11.md` | Frozen protocols (commits `3710267`, `d3cdee6`) |
| `EXPOSURE_AND_SPLIT_MANIFEST.json`, `FROZEN_INPUT_HASHES.json` | Data inventory, exposure history, splits; hashes of 93 frozen input files |
| `03_RESULTS_TABLES.md` | All tables, generated from `results/` |
| `04_RESULTS_AND_INTERPRETATION.md` | Reading of the results by the rules fixed in advance |
| `05_ARABIC_REPORT.md` | Arabic explanation of designs, experiments, findings and limits |
| `06_THESIS_CHANGE_MAP.md` | Proposed thesis changes (none applied) |
| `07_PROSPECTIVE_VALIDATION_KIT.md`, `prospective/` | Independent-request kit, label schema, test manifest: **not executed** |
| `08_PROGENT_FULL_FRAMEWORK_PLAN.md` | Matched live comparison with Progent: plan, commands, cost-estimation method: **not run** |
| `09_CLAIM_AUDIT_AND_CHANGE_LOG.md` | Claim audit, equation-to-code mapping, change log |
| `10_FINAL_DECISION_TABLE.md` | Decision table and reproduction commands |
| `11_RELATED_WORK_PROPOSALS.md` | Cedar, FIDES, CaMeL, IsolateGPT: feasibility, what was run, what was not |
| `results/` | `results.json`, `results_section11.json`, `fits_summary.json`, per-episode outcomes, per-call audit of restricted calls |
| `logs/` | fit, replay, report logs |

Code: `experiments/competitive_study/` (`candidates.py`, `fitting.py`, `guards.py`, `cs_run.py`, `cedar_front.py`, `guards_s11.py`, `cs_run_s11.py`, `cs_tables.py`). Tests: `tests/test_competitive_study.py`, `tests/test_competitive_study_s11.py`.
