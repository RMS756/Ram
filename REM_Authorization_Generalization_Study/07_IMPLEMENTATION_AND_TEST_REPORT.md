# 07 — Implementation and test report

**Branch:** local `claude/rem-authz-generalization-study`, created from `4989306`. Protocol frozen at commit `cca4968` (11 Nov 2026, 04:51 UTC) before any candidate outcome existed. **Nothing was pushed.**

## 1. What was and was not changed

| Area | Changed? |
|---|---|
| `rem/` (approved implementation) | **No.** `git diff` against `4989306` is empty for `rem/`, `configs/`, `experiments/pilot/`, `experiments/melon_rem/`. |
| Approved configuration (`pilot_e0.yaml`), costs, tiers, thresholds, feature definitions | **No.** |
| Frozen MELON bundle (`983c5b0d…`) | **No**; hash re-checked after all runs. |
| Thesis files | **No.** |
| New, isolated files | Yes; listed below. |

## 2. Files added

| File | Lines | Purpose |
|---|---|---|
| `experiments/authz_study/authz_evidence.py` | 113 | `z_exp`, `z_del`: pure functions, an offline builder aligned with the recorded steps, and a runtime helper |
| `experiments/authz_study/study.py` | 513 | stages `branch` (prefix-branch outcomes), `fit` (REM's estimator procedure on any fitting portion, target and feature set), `replay` (all arms; S1, S2, S3, probe) |
| `experiments/authz_study/analyze.py` | 309 | metrics, grouped bootstrap, contrasts, Pareto set, fixtures |
| `experiments/authz_study/weakness_audit.py` | 144 | measurements for `03` (original REM only) |
| `experiments/authz_study/posthoc_a1.py`, `posthoc_a2.py` | 76, 90 | post-hoc amendments A-1 and A-2, labelled as such in the code |
| `tests/test_authz_study.py` | 98 | seven tests |
| `REM_Authorization_Generalization_Study/` | — | the ten deliverables, results JSON, logs, paper hashes |

Every estimator, calibrator, loss grid, predicate, tier map, replay element and bootstrap routine is imported unchanged from `rem/` and `experiments/pilot/`.

## 3. Verification of the implementation

| Check | Result |
|---|---|
| The study's fitting routine against the frozen original fits (9 folds: intercept, coefficients, γ0, γ1, B1 thresholds, λ) | maximum absolute difference 3.6·10⁻¹⁴ |
| The same for the original "no behavioural evidence" fits | 2.6·10⁻¹⁴ |
| Arm M00 under S1 against the original REM result | 11 / 2,979 and 105 / 334: identical |
| Arm B1 under S1 against the original baseline | 164 / 2,979 and 170 / 334: identical |
| Arm B0 against the original no-defence replay | 672 / 2,979 and 175 / 334: identical |
| Arm M00 without behavioural evidence under S1 against the stored original ablation | 11 / 2,979 and 140 / 334: identical |
| Replay errors, any arm | 0 |
| Exact ties in a decision rule, any arm | 0 |
| Calibration failures (γ1 ≤ 0), any cell or target | 0 |
| Alignment of branch outcomes with recorded steps | 6 of 6,762 steps have no branch outcome (their tool call is not executed in replay); they are given ΔS = ΔU = 0 and counted |

## 4. Tests

```
python3 -m pytest -q                                                  # 241 passed, 3 skipped, 1 xfailed
PILOT_RESULTS_DIR=<pilot dir> AUTHZ_STATE=<state dir> python3 -m pytest -q   # 243 passed, 1 skipped, 1 xfailed
```

- The seven new tests cover: explicit identity argument; value from an unnamed source; value from a user-named file (and that a withheld read is not a source); amount-only calls and reads; the documented limitation that a historical value counts as explicit; equality of the study's fits with the frozen fits; and the behaviour of five arms on a direct, correctly specified transfer.
- Two of the seven need the study state and are skipped without it.
- The one expected failure is the earlier audit's deliberate record of the comma-grouped decimal deviation. The remaining skip is the MELON integration module, which needs AgentDojo 0.1.29.
- All 236 tests that passed before this study still pass.

## 5. Runs executed

| Stage | Size | Wall time |
|---|---|---|
| Prefix-branch outcomes | 4,049 episodes, 12,500 replays | 20 s |
| Cell fits | 9 S1 cells and 143 S2 cells; up to 5 targets × 5 feature sets | 26 s |
| Enforcement replays | 182,826 | 328 s |
| Weakness audit (two extra replays of the original REM) | 6,626 | about 15 s |
| Post-hoc A-1 and A-2 | 3,313 and 9,986 replays | under 1 min each |
| Analysis (2,000-resample grouped bootstrap) | — | about 10 min |

Environment: Python 3.11.17, numpy 2.4.6, agentdojo 0.1.35, AgentDojo runs at `089ed468…`, seed 20261027, four worker processes, `PYTHONHASHSEED=0`.

## 6. Reproduction

```bash
# 0. the unchanged pilot state (about 5 min)
cd experiments/pilot && export PILOT_RESULTS_DIR=<pilot dir> PYTHONHASHSEED=0
python3 build_dataset.py && python3 e0_pilot.py && python3 run_main.py crossfit rmod replay
# 1. this study
cd ../.. && export AUTHZ_STATE=<state dir>
python3 experiments/authz_study/study.py branch fit replay
python3 experiments/authz_study/weakness_audit.py REM_Authorization_Generalization_Study/results/weakness_audit.json
python3 experiments/authz_study/posthoc_a1.py      # post hoc, labelled
python3 experiments/authz_study/posthoc_a2.py      # post hoc, labelled
python3 experiments/authz_study/analyze.py         # writes results/study_results.json
```

State hashes of this run (SHA-256 prefixes): `branch.pkl` 67763d06…, `cells.pkl` 98088ec5…, `replay.pkl` f8aaec9a…. The state files are in the session scratch directory and are not committed (39 MB); they are regenerated by the commands above.

## 7. Unresolved issues

1. **Published defences not run.** Task Shield, MELON and PROVISO need a model API (and, for PROVISO, an implementation and an encoder download). `arxiv.org`, `huggingface.co` and `api.openai.com` are blocked in this session.
2. **The code repository of Calibration Is Not Control was not accessed**, so its implementation was not compared with the adaptation here.
3. **No independent benchmark.** Evidence definitions are banking-specific; conclusions are limited to within-benchmark generalization.
4. **Runtime authorization evidence treats a released read as executed**; a released read that fails at run time is still treated as a source. The offline builder uses the recorded error flag. No effect was observed (0 replay errors), but the two code paths are not identical.
5. **Decision times** were measured under multi-process load and are indicative only.
6. **Post-hoc analyses** A-1 to A-3 were added after results were seen and are labelled in the code, the protocol and the results.
