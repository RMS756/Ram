# Project baseline audit — 11 November 2026

[PROPOSED — SUPERVISOR APPROVAL REQUIRED]

## Authority and immutable baseline

Repository: https://github.com/RMS756/Ram . Baseline is `fca0319f888a9be2105464496f4c975b6d393738`, tip of `codex/rem-ollama-pilot`. It descends from R4 corrections `9fddfa748a4eb036f200206e874413147bf237b5`; the default branch is older R3 `181a38cfd521f40a54e0d2492b46edb04eb21a76`. All five remote branches were enumerated through Git and the GitHub connector; see `artifacts/remote_refs.txt`.

Experimental branch: `codex/rem-authorization-generalization-experiment`. Protocol and initial candidate were committed at `6acf2c2` before candidate benchmark outcomes. This is an analysis freeze on previously studied data, not independent prospective preregistration.

`CLAUDE.md` was read before changes. The user explicitly authorized isolated research candidates and preservation of the frozen design; that authorization applies here, without declaring supervisor approval. Only the two experimental directories change. No official chapter, original config, original result, or `rem/` source is edited. Integrity evidence: `artifacts/baseline_integrity.json`.

## Sources inspected

Read the root README, frozen lock, supervisor register, novelty audit, experiment-validity report, R4 code verification/reproduction reports, pilot and live runners, replay integration, feature/label extraction, estimator/calibration/decision/mitigation code, and current Chapter 2/3 sources under `REM_FINAL_THESIS/final_five_chapters/src/`. These are distinguished from older R3/R4/R5 chapter generations. The three November 11 planning filenames were absent from the available remote branch trees/history: `REM_SOURCE_OF_TRUTH.md`, `REM_SCOPE_AND_GAP_DECISION_MEMO.md`, `REM_CUT_PLAN.csv`. Absence of files is not evidence of a supervisor decision.

## Architecture and unresolved issues

Five layers remain Input & Context, Detection, Behavioral Analysis, Decision Engine, Mitigation. Original flow: provenance → eight pilot evidence features → ridge logistic → logit calibration → tier → D1/D2 → expected-loss verdict → deterministic mitigation → audit. SHAP is audit-only; CUSUM observe-only. Paths: `rem/algorithms/behavior/evidence.py`, `rem/integration/steps.py`, `rem/algorithms/detection/ridge_logistic.py`, `rem/algorithms/calibration/`, `rem/algorithms/decision/`, `rem/core/mitigation.py`.

The executable historical research baseline is `experiments/pilot/run_main.py`, not an approved end-to-end frozen `RemPipeline`. Its costs, tiers, features, label rule and reviewer assumptions remain exploratory. SC-1 mitigation, SC-2 ties, SC-3 calibration ablation, SC-4 fitting targets, SC-5 Brier convention, SC-6 layer assignment, equation-registry absence, and SD-FREEZE remain unresolved. This study does not settle them.

The Ollama branch refactors fold policy construction and adds local inference adapters; it does not establish a completed live security experiment. No usable LLM endpoint or managed model credential was configured for this study.

## Data audit findings

Fresh extraction reproduced 3,334 primary episodes, 6,762 steps and 921 reference-positive attempts. Labels encode reference tool plus attacker key argument, not independently adjudicated user authorization. Historical positives without `x_act1` are concentrated in `user_task_15`. The user/attacker recipient collision and alternative-tool reference-match false negatives already appear in R4 audits; they are not new discoveries.

Only 159 primary episodes explicitly identify version `v1.2.1` (one Llama-3.3-70B pipeline); 3,175 have no version. Nine task-15 episodes in the explicit cohort were removed, leaving 150 episodes (135 attacked, 15 benign), 442 steps and 109 positive attempts. All 150 reproduced both recorded native outcomes under `v1.2.1`. The fresh primary training/evaluation cohort therefore uses one declared version. Historical reproduction remains separate and mixed-version by design.

Original tests before changes: 221 passed, 3 skipped. Final combined tests with AGENTDOJO_RUNS configured: 275 passed, no skips. The three baseline replay tests initially skipped due to their default dataset path were enabled and passed.

Fresh full historical replay reproduced all headline outcome counts exactly. Non-bit-identical analytical numeric values are disclosed: 454 differing fields, max absolute delta 1.11e-14; see the complete differences artifact.
