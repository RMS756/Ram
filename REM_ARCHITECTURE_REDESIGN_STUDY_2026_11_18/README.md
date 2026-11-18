# REM architecture redesign study (18 November 2026)

**Branch:** `claude/rem-architecture-redesign-20261118`.

**Status:** `[PROPOSED - EXPLORATORY]`. The approved REM v1.0 design, its frozen results and the thesis objectives are **not** modified.

**Evidence base:**
- offline replay of recorded AgentDojo banking traces (NO-ADAPT);
- author-written suites;
- a scripted closed loop.

No language model was called. Full Progent and live-agent experiments were **not executed**.

## Outcome in one table

| Question | Result |
|---|---|
| Selected architecture | **REM-B**: preferred on security; utility **INCONCLUSIVE** vs C1 on held-out H, +0.0077 [0.000, 0.021] |
| REM-C (hybrid, learned stage on unresolved calls) | **NO-GO**: 121 / 24 audited violations; unsafe suite releases |
| Learned stage | harmful / redundant (REM-A); harmful (REM-C); consequence-aware = threshold; calibration without decision effect |
| Object binding | **INCONCLUSIVE**: security part met; one authorised held-out probe withheld (designator defect, `08a`) |
| Progent | manual policy only, with parity to upstream on 3,213 calls; no superiority claim; full Progent NOT EXECUTED |
| Live LLM | NOT EXECUTED (no endpoint, no approved budget) |

## Documents

| # | File |
|---|---|
| 01 | `01_EXISTING_REM_ARCHITECTURE_AUDIT.md`: evidence table, component assessment, reachability diagnosis |
| 02 | `02_RELATED_WORK_AND_NOVELTY_AUDIT.md` |
| 03 | `03_THREAT_MODEL_AND_SECURITY_CONTRACT.md`: invariants I1–I6 |
| 04–06 | `04_REM_A_DESIGN.md`, `05_REM_B_DESIGN.md`, `06_REM_C_DESIGN.md` |
| 07 | `07_ALGORITHM_SELECTION.md` |
| 08 | `08_FROZEN_EXPERIMENT_PROTOCOL.md` + `08_PROTOCOL_HASHES.sha256` (frozen at `6705c07`); `08a_AMENDMENTS.md` (post-scoring notes) |
| 09 | `09_SECURITY_UTILITY_RESULTS.csv` |
| 10 | `10_ABLATION_STUDY.md` |
| 11 | `11_GENERALIZATION_EVALUATION.md` |
| 12 | `12_PROGENT_COMPARISON.md` |
| 13 | `13_LIVE_LLM_EXPERIMENT.md` |
| 14 | `14_ARCHITECTURE_SELECTION_DECISION.md` |
| 15 | `15_RESEARCH_GAP_AND_CONTRIBUTION_AUDIT.md`: includes the supervisor change proposal |
| 16–17 | `16_THESIS_READY_CHAPTER_3.md`, `17_THESIS_READY_CHAPTER_4.md` (draft sections, status-labelled) |
| 18 | `18_SUPERVISOR_PRESENTATION_SUMMARY.md` |
| 19 | `19_ARABIC_DETAILED_EXPLANATION.md` |
| 20 | `20_REPRODUCIBILITY_MANIFEST.md` + `manifests/reproducibility_manifest.json` |
| – | `CHANGELOG.md`, `results/`, `logs/`, `figures/` |

**Code:** `experiments/architecture_redesign/`.

**Tests:** `tests/test_architecture_redesign.py`.
