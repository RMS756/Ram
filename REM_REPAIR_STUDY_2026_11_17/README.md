# Repair study of 17 November 2026: derived amounts

Status: `[PROPOSED - EXPLORATORY - NOT PART OF THE APPROVED REM DESIGN]`. Offline recorded-trace replay and proposed-call diagnostics. No live agent, no paid model call, no supervisor decision. The frozen modules, configurations, stored results and thesis editions R1–R5 are unchanged (`FROZEN_INPUT_HASHES.json`, checked by `tests/test_repair_study.py`).

## Deliverables

| File | Content |
|---|---|
| `DEFECT_REPORT_C1_C2_2026-11-17.md` | dated defect report with reproduction and root-cause trace (frozen modules) |
| `PROTOCOL.md` | development protocol, frozen at commit `f81f6b3` before any repaired-arm outcome on a cohort |
| `AMOUNT_GRAMMAR.md` | the finite grammar, evidence rules, status semantics and known limits |
| `SOURCE_AND_ASSUMPTION_REGISTRY.csv` | arithmetic used; assumptions deliberately **not** made (rounding, currency, tolerance, limits) |
| `03_RESULTS_TABLES.md` | tables generated from `results/` by `experiments/repair_study/rs_tables.py` |
| `04_RESULTS_AND_INTERPRETATION.md` | claim criteria, cost, failure analysis (before/after), guard-vs-learner attribution |
| `05_ARABIC_REPORT.md` | concise explanation in Arabic |
| `07_INDEPENDENT_VALIDATION_KIT.md`, `validation_kit/` | validation on independently written requests (**not executed**) |
| `08_PROGENT_THREE_CONFIGURATIONS.md` | PG executed (replay); generated and generated+updated policies **not executed** |
| `11_CLOSE_WORK_AND_NOVELTY.md` | Progent, CaMeL, Task Shield, NEXUS, PACT, ROPE, CapLite with reading levels |
| `12_BIBLIOGRAPHY_CORRECTIONS.md` | NEXUS, MELON, PRISMA 2020, PRISMA-S, new entries |
| `DEFECT_REPORT_D3_D4_2026-11-17.md` | defects D3 (partial compound expression) and D4 (amount from an unmet-condition instruction), stage order |
| `PROTOCOL_AMENDMENT_V2.md` | dated amendment, frozen at `95549b2` before version 2 was scored |
| `13_V2_RESULTS_TABLES.md`, `14_V2_INTERPRETATION.md`, `results_v2/` | version-2 results and interpretation |
| `results/` | per-episode outcomes, restricted-call audit, cohort hashes, defects before/after, residual-stage diagnostics |
| `logs/` | replay, report and diagnostics logs |

Code: `experiments/repair_study/` (`amount_verifier.py`, `repaired_arms.py`, `rs_run.py`, `rs_tables.py`, `diagnostics.py`, `reproduce_defects.py`). Tests: `tests/test_repair_study.py`. Thesis: `REM_FINAL_SUBMISSION/thesis_r6/`.

## Commands (from the repository root)

```bash
# environment of the competitive study: AGENTDOJO_RUNS, PILOT_RESULTS_DIR, INTEGRATION_STATE, PROGENT_UPSTREAM,
# COMPETITIVE_STATE (caches outside the repository), PYTHONHASHSEED=0
python3 experiments/repair_study/reproduce_defects.py            # results/defects_before.json (frozen arms)
python3 -m pytest -q -o addopts= tests/test_repair_study.py       # 103 tests, synthetic cells
python3 experiments/repair_study/rs_run.py replay report          # 27,631 replays of the repaired arms; results/
python3 experiments/repair_study/diagnostics.py                   # results/defects_after.json, residual_stage_diagnostics.json
python3 experiments/repair_study/rs_tables.py                     # 03_RESULTS_TABLES.md
python3 REM_FINAL_SUBMISSION/thesis_r6/tools/gen_r6.py            # Chapter 4 section from the result files
python3 REM_FINAL_SUBMISSION/thesis_r6/tools/make_r6.py           # assemble R6 from R5 + spec_r6.py
python3 REM_FINAL_SUBMISSION/thesis_r6/tools/build_final.py       # DOCX + PDF (pinned LibreOffice 24.2.7.2, pandoc 3.9)
python3 REM_FINAL_SUBMISSION/thesis_r6/tools/build_supplement.py
python3 REM_FINAL_SUBMISSION/thesis_r6/tools/check_pages.py REM_FINAL_SUBMISSION/thesis_r6
```

## Status

| Item | Status |
|---|---|
| Reproduction of C1/C2 on the frozen arms (G3, GV, HV, HVx, GVc, GVp) | **executed** (proposed-call diagnostics) |
| Typed amount verifier and repaired arms G3_math, GV_math, HV_math | **implementation-tested** (103 tests) |
| C1/C2 repaired, three injection variants | **executed** (diagnostics) |
| Replay of repaired arms: primary S1/S2, second population, probe, 43 fixtures | **executed**; **development evidence** (0 successful attacks; −95 and −159 tasks in user tasks 3 and 11; one legitimate fixture lost) |
| Learned contribution (HV_math vs GV_math) | **not established** (identical outcomes; no labelled attack reaches the stage) |
| Residual-stage diagnostics (delegated amounts) | **executed**; shows an unprotected stage; not a rate |
| Benefit of supporting computed amounts on AgentDojo | **not established** (no benchmark request uses a supported expression) |
| Independent validation on requests written by others | **not executed** |
| Progent with generated / generated+updated policies | **not executed** (no credential, no approved budget) |
| PACT, ROPE, CapLite comparison | **not executed**; reviewed at abstract level (ROPE also repository) |
| D3/D4 reproduced on version 1 (24 unauthorized releases) | **executed** (diagnostics) |
| Version 2 (coverage, single witness, literal stage order) and the separate appositive extension | **implementation-tested** (104 tests); D3/D4 diagnostics: 0 unauthorized releases |
| Version-2 replay (47,156 replays) and fixtures | **executed**; **development evidence**: no episode changes; 0 attacks; one legitimate fixture newly withheld (S1) by the coverage rule; extension recovers P2; HV_math2 = GV_math2 |
| Thesis R6 (212 pages; supplement 124 pages) | **built and checked** (page references 150/150; 25 equations; citations both directions); page target 145–160 **not reached**; not approved, not submitted |
| Thesis R7 (212 pages; supplement 126 pages): version 2, corrected stage order | **built and checked** (page references 151/151; 25 equations; citations both directions); not approved, not submitted |
| `15_RESPONSE_TO_REVIEW_2.md` | point-by-point response to the second review |
| Full test suite (17 Nov, after version 2) | 702 passed, 6 skipped, 1 expected failure (without the study environment) |
| Full test suite (17 Nov, version 1) | 598 passed, 6 skipped, 1 expected failure without the study environment. With `AUTHZ_STATE` set to this session's cache, `test_authz_study::test_intervention_value_rule_and_original_arm_on_a_direct_transfer` fails on that cache (module unchanged since `3e96e8e`) |
