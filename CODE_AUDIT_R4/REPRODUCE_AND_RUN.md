# Reproduce and Run REM: commands verified on 2 November 2026

Every command below was **executed in this audit**, and its output is stored in `CODE_AUDIT_R4/logs/`. Commands that were not executed are marked **NOT EXECUTED**, with the blocker.

All financial actions run inside AgentDojo's simulated banking environment. Nothing contacts a bank or a payment system, and no real transaction is possible.

## 1. Environment actually used

| Item | Value (verified) |
|---|---|
| Repository commit | `bec4d1c894d2d66a2906d039612d61c141a27f75` on `claude/rem-r4-corrections-3ktvze`. Code, configuration and experiment files are identical to the R4 thesis commit `9ab3f9e` |
| OS / CPU | Linux x86_64 container, 4 vCPU, Intel Xeon @ 2.80 GHz |
| Python | 3.11.17 (`/usr/local/bin/python3`) |
| Packages | numpy 2.4.6, PyYAML 6.0.1, pytest 9.2.0, agentdojo 0.1.35, matplotlib 3.11.2, pillow 13.0.0, pydantic 2.14.2; `rem-framework` 0.2.0 installed editable from the repository |
| Benchmark traces | `ethz-spylab/agentdojo` cloned to `/home/user/ethz-spylab/agentdojo` at commit `089ed468cf3ed0322acc66b0211f26d9d90dbf60` (clean working tree); `runs/` is 525 MB |
| Pilot configuration | `configs/exploratory/pilot_e0.yaml`, sha256 `8e1aa107cf3ea0ba5eecbb92bc90a2463202cdde476cfe8a98047ffad74e11d0` (committed in `48bef90`, unchanged since) |
| Amendments | `configs/exploratory/pilot_e0_amendments.yaml`, sha256 `8c4f8fc0…f34106f` (committed in `7a707a7`) |
| Seed | 20261027 (configuration line 28); 2,000 bootstrap resamples |
| Credentials | None used. No LLM API key exists in the environment |

## 2. Setup

```bash
# from the repository root
python3 -m pip install -e ".[dev]" agentdojo==0.1.35 matplotlib     # already satisfied in this container
git clone https://github.com/ethz-spylab/agentdojo.git /home/user/ethz-spylab/agentdojo
git -C /home/user/ethz-spylab/agentdojo checkout 089ed468cf3ed0322acc66b0211f26d9d90dbf60
```

The clone and checkout were already present and were verified with `git rev-parse HEAD` and `git status --porcelain` (empty).

## 3. Verified commands and their outputs

| # | Command | Duration | Output (this audit) | Log |
|---|---|---|---|---|
| 1 | `python3 -m pytest -o addopts="" -q -p no:cacheprovider` | 7.9 s | 205 passed | `logs/pytest_full.log`, `logs/pytest_per_file.log` |
| 2 | `PILOT_RESULTS_DIR=$OUT PYTHON=python3 AGENTDOJO_RUNS=/home/user/ethz-spylab/agentdojo/runs bash experiments/pilot/run_all.sh` | 11 min 20 s | exit 0. Writes 13 JSON files, 3 figures, `steps.pkl` and `state/*.pkl` to `$OUT` (outside the repository; committed results untouched) | `logs/reproduction_run.log` |
| 3 | `python3 REM_FINAL_THESIS/verification/compare_reproduction.py $OUT results/pilot_R2 CODE_AUDIT_R4/logs/reproduction_comparison_vs_pilot_R2.json` | < 5 s | shared 6,057; equal 5,942; volatile 115; **analytical 0** | `logs/reproduction_comparison_summary.log` |
| 4 | same, against `results/pilot_R4` | < 5 s | shared 6,207; **analytical 0** | same |
| 5 | `python3 CODE_AUDIT_R4/audit_checks/list_all_differences.py $OUT results/pilot_R2` | < 5 s | 115 differing values: `rem_commit` 13, `latency_ms_median` 50, `latency_ms_p95` 50, `peak_bytes_per_step_median` 1 (4,349 vs 4,364 bytes), `file` 1 | `logs/all_differences_vs_pilot_R2.log` |
| 6 | `PILOT_RESULTS_DIR=$OUT python3 CODE_AUDIT_R4/audit_checks/audit_invariants.py` | about 30 s | 8 PASS, 1 FAIL, 6 INFO (see `CODE_VERIFICATION_REPORT.md`) | `logs/audit_invariants.log`, `.json` |
| 7 | `PILOT_RESULTS_DIR=$OUT python3 CODE_AUDIT_R4/audit_checks/audit_results.py` | about 40 s | Headline metrics and six replay configurations identical to `results/pilot_R2` | `logs/audit_results.log`, `.json` |
| 8 | `PILOT_RESULTS_DIR=$OUT python3 CODE_AUDIT_R4/audit_checks/e2e_example.py` | about 20 s | Illustrative trace, plus one sandbox replay with and without REM | `logs/e2e_example.log` |
| 9 | `python3 REM_FINAL_THESIS/verification/verify_equations.py` | < 5 s | 21 equation checks, then ALL PASS | `logs/verify_equations.log` |
| 10 | `python3 REM_FINAL_THESIS/verification/trace_cells_R4.py` | < 5 s | 126 / 126 PASS | `logs/trace_cells_R4.log` |
| 11 | `cp -r chapter2 $TMP && (cd $TMP/slr/tools && python3 build_slr.py) && diff <(python3 -m json.tool chapter2/slr/prisma_counts.json) <(python3 -m json.tool $TMP/slr/prisma_counts.json)` | < 10 s | identical; the raw files Q*.json sum to 320 records | (recorded in `THESIS_WRITING_PROCESS_AR.md`) |

`$OUT` in this audit was the session scratchpad directory `.../scratchpad/repro_A1`. The reproduced `steps.pkl` has sha256 `876211cdf4975568b0fe9b8f4fb1312471fd514c66f3dac283273ac28f792c5d`.

## 4. Headline values reproduced (identical to `results/pilot_R2`)

| Quantity | Reproduced value | Source field |
|---|---|---|
| Episodes / steps / positive steps | 3,334 / 6,762 / 921 | `dataset_summary.json` |
| Held-out ROC-AUC, AP, ECE (M = 10), log-loss, Brier (binary) | 0.938288, 0.718886, 0.043761, 0.201344, 0.060330 | `e1_crossfit.json → label_nll_primary.pooled_calibrated` |
| Observe-only intervention: REM y = 0 / y = 1; B1 y = 0 / y = 1 | 0.2268 / 0.9729; 0.0562 / 0.7405 | `e2_e5_e6_observe_only.json → verdicts` |
| Replay ASR: B0, B1 (step-level), REM (step-level) | 672/2979 = 0.2256; 164/2979 = 0.0551; 11/2979 = 0.0037 | `e4_e5_enforcement_replay.json → configs.*.ASR[0]` |
| Benign utility: B0, B1, REM without reviewer, REM idealised | 0.5240, 0.5090, 0.3144, 0.4970 | same, `benign_utility[0]` |
| r_mod by tier (step-level, pooled) | tier 3: 0.000 (n = 530); tier 4: 0.0101 (n = 298) | `e4_rmod_and_replay_validity.json` |
| Complete-call latency, REM step-level without reviewer | median 0.250 ms, p95 0.566 ms (committed R4: 0.274 ms). Machine-dependent | `latency_full_ms_*` |

## 5. Expected artefacts of `run_all.sh`

`dataset_summary.json`, `e0_pilot.json`, `e1_crossfit.json`, `e2_e5_e6_observe_only.json`, `e3_a2_cusum_observe_only.json`, `e4_cross_template_and_defenses.json`, `e4_e5_enforcement_replay.json`, `e4_rmod_and_replay_validity.json`, `sensitivity_post_hoc_exclude_user_task_15.json`, `benign_release_breakdown.json`, `r2_breakdowns.json`, `feature_firing_rates.json`, `latency_memory_profile.json`, `label_audit_sample.md`, `label_audit_human_package.csv`, `figures/fig_{architecture,reliability,enforcement_replay}.png`, `steps.pkl`, `state/{crossfit,rmod,replay_rmod,observe_verdicts,replay_main}.pkl`.

## 6. Not executed, with blockers

| Item | Attempted command or route | Blocker | Effect |
|---|---|---|---|
| Live enforcing-mode evaluation | `experiments/live/` (protocol only; no runner was executed) | No LLM API key; no authorisation decision (D-15) | No evidence about agents that retry or adapt |
| Human label audit | `results/pilot_R2/label_audit_human_package.csv` (145 items) | Needs human annotators | Label validity unverified |
| Full-text source verification | WebFetch `https://arxiv.org/abs/1706.04599` | `getaddrinfo ENOTFOUND arxiv.org` (outside the network allow-list) | Equation sources checked at metadata or abstract level only |
| Thesis DOCX/PDF rebuild | `REM_VERSION=R4 python3 REM_FINAL_THESIS/tools/build_thesis.py` | Not run in this audit (not needed for code verification; it rewrites committed build files) | The build itself was not re-verified here |
| Frozen `RemPipeline` end-to-end | — | No experiment entry point uses it | Unit tests only |

## 7. Re-running the audit checks

```bash
OUT=/path/to/rerun   # any directory outside the repository
PILOT_RESULTS_DIR=$OUT PYTHON=python3 AGENTDOJO_RUNS=/home/user/ethz-spylab/agentdojo/runs bash experiments/pilot/run_all.sh
for s in audit_invariants audit_results e2e_example; do
  PILOT_RESULTS_DIR=$OUT python3 CODE_AUDIT_R4/audit_checks/$s.py
done
python3 CODE_AUDIT_R4/audit_checks/list_all_differences.py $OUT results/pilot_R2
```

`audit_invariants.py` writes `CODE_AUDIT_R4/logs/audit_invariants.json`, and `audit_results.py` writes `CODE_AUDIT_R4/logs/audit_results.json`. Neither script modifies REM code or committed results.
