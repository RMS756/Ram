# REM authorization-generalization study (provisional working name)

**Status:** `[PROPOSED — SUPERVISOR APPROVAL REQUIRED]`. Exploratory and isolated. The approved REM design, code (`rem/`), configuration, results and thesis are unchanged.

**Evaluation mode:** offline recorded-trace replay (AgentDojo banking, step level, no reviewer, NO-ADAPT) and synthetic call-level probes. No live agent, no model API.

**Result in one sentence:** the tested authorization-aware, outcome-supervised candidate does not improve REM (132 vs 11 successful attacks of 2,979; benign gain not established), so the recommendation is to retain the approved algorithm, add simple rule baselines to the thesis, and put the removal of behavioural evidence to the supervisors as a decision.

| File | Content |
|---|---|
| `01_RESEARCH_GAP_VERIFICATION.md` | the proposed gap checked against six full-text papers; narrowed wording |
| `02_PAPER_AND_ALGORITHM_EVIDENCE_MATRIX.md` | equations, locations, limitations and applicability, paper by paper |
| `03_ORIGINAL_REM_WEAKNESS_AUDIT.md` | Problems A–E measured on the original REM |
| `04_ALGORITHM_CANDIDATE_COMPARISON.md` | candidates A–D and the selection made before the experiments |
| `05_PROPOSED_REM_ALGORITHM_SPECIFICATION.md` | exact specification and derivation of the tested candidate |
| `06_EXPERIMENTAL_PROTOCOL.md` | protocol frozen at commit `cca4968` before any outcome; amendments listed |
| `07_IMPLEMENTATION_AND_TEST_REPORT.md` | files, verification, tests, runs, reproduction |
| `08_EXPERIMENTAL_RESULTS_AND_COMPARISON.md` | all results, intervals, ablations, probes, negative findings |
| `09_SUPERVISOR_DECISION_MEMO.md` | draft memo with the decisions requested |
| `10_THESIS_UPDATE_PLAN.md` | proposed chapter updates (not applied) |
| `results/` | `study_results.json`, `weakness_audit.json`, same-backbone table |
| `logs/` | stage logs |
| `papers_provided/SHA256SUMS.txt` | hashes of the six PDFs read (the PDFs themselves are not stored here) |

Code: `experiments/authz_study/`. Tests: `tests/test_authz_study.py`.
