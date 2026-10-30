# Results Provenance Report (R3, 30 October 2026)

## 1. Classification of all evidence reported in Chapter 5

| Category (request §10) | Present? | Where | Notes |
|---|---|---|---|
| Real empirical measurements of REM enforcing on live agents | **NO** | — | **NOT EXECUTED — NO EMPIRICAL RESULT AVAILABLE.** No LLM access (D-15) |
| Recorded outcomes (benchmark's own verdicts on traces recorded by its authors) | Yes | §5.2, §5.6.1, §5.11 | Real agent behaviour, recorded by the AgentDojo authors, not by this project |
| Recomputed metrics from recorded traces: held-out predictions | Yes | §5.3–5.4, §5.7 | Real traces, nested grouped cross-fitting; labels by the reference-match rule (proxy, not human-audited) |
| Recomputed decisions from recorded traces: observe-only | Yes | §5.5, §5.7, §5.9 | Verdicts computed, not enforced |
| Simulated results: replay under NO-ADAPT | Yes, labelled | §5.6, §5.7 replay columns | Deterministic re-execution of recorded trajectories in the benchmark sandbox, assuming the agent does not adapt. A sensitivity analysis under a proposed scope amendment (SC-7 / D-1). **Not evidence of protection against live or adaptive agents** |
| Illustrative examples | No | — | Unit-test fixtures are not reported as results |
| Exploratory pilot results | Yes: all of Chapter 5 | — | Every result file carries the label "EXPLORATORY — NOT THESIS RESULTS — SUPERVISOR DECISION REQUIRED". Design values are pre-registered exploratory values, not approved ones |
| Unverified claims | None found | — | Every number traced (§3 below) |

## 2. Data provenance

| Item | Value | Evidence |
|---|---|---|
| Benchmark | AgentDojo banking suite; package 0.1.35 (PyPI); suite v1 for execution | `dataset_summary.json` provenance; Ch. 4 Table 4.1 |
| Traces | AgentDojo repository `runs/` at commit `089ed468cf3ed0322acc66b0211f26d9d90dbf60`; 21 undefended backbones under the `important_instructions` attack | Obtained again on 30 Oct from the public repository; the commit was checked out exactly |
| Observations | 3,334 episodes (2,998 attacked, 336 without injection); 6,762 proposed tool calls; 921 positive steps | `dataset_summary.json`. 2,998 = 2,156 + 682 + 158 + 2 (sum of the per-group consistency counts) |
| Exclusions | 5 error episodes; 21 episodes of (user_task_15, injection_task_4), amendment AM-1, committed before held-out predictions (`7a707a7`) | `dataset_summary.json` |
| Partitions | No train/calibration/test split. Nested grouped cross-fitting: 9 outer folds by injection task (benign episodes by user task), 4 inner folds | `configs/exploratory/pilot_e0.yaml`; Ch. 3 §3.11.5 |
| Seeds | 20261027 (bootstrap and every random source) | `pilot_e0.yaml` line 28 |
| Bootstrap | 2,000 resamples, grouped by injection task (attacked) and user task (benign) | `pilot_e0.yaml` lines 186–187 |
| Independence | Episodes are not independent: 16 user-task and 9 injection-task templates, one attacker account, one run per configuration | Stated in Ch. 5 §5.2.1 |

## 3. Independent reproduction of 30 October 2026

**Procedure.**
1. The repository was merged (`4a286a5`).
2. AgentDojo 0.1.35 was installed and the repository was cloned at commit `089ed468`.
3. `experiments/pilot/run_all.sh` was executed with `PILOT_RESULTS_DIR` pointing outside the repository, so that no committed artifact was overwritten. It finished with exit code 0.
4. `verification/compare_reproduction.py` then compared every numeric leaf of the 13 result files with `results/pilot_R2/`.

**Environment of the re-run.**

| Item | Value |
|---|---|
| Python | 3.11.17 |
| NumPy | 2.4.6 |
| Processor | Intel Xeon @ 2.10 GHz, 4 vCPU (the R2 run used a 2.80 GHz Xeon) |

**Result** (`verification/reproduction_comparison.json`):

| Measure | Count |
|---|---:|
| Values shared by both runs | 6,057 |
| Identical | 5,943 |
| Different: 50 `latency_ms_median`, 50 `latency_ms_p95`, 13 `rem_commit`, 1 `file` | 114 |
| **Different analytical values** | **0** |

**Check of the classifier.** The comparison script classes a difference as non-analytical when its key path contains a time, memory or provenance word. A substring match could in principle hide an analytical difference. All 114 differing values were therefore listed individually (`verification/reproduction_all_differences.json`). Every one is a latency, commit or file-path field. No analytical value is among them.

- **Memory.** The median per-step peak allocation reproduced exactly: 4,364 bytes.
- **Processing time.** REM's per-step median was 0.137–0.156 ms and its 95th percentile 0.400–0.476 ms across REM configurations. These are within the ranges Chapter 5 reports for the earlier runs.

A separate comparison of the committed R1 and R2 result sets found 5,220 shared values, 104 differences and 0 analytical differences (`verification/r1_vs_r2_comparison.json`). Listed individually (`verification/r1_vs_r2_all_differences.json`), the 104 differences are 92 latency values, 11 commit stamps and the median memory per step (the 2.9 KB → 4.4 KB change).

## 4. Number-by-number check of the chapters

`verification/check_chapter_numbers.py` compared every decimal number, percentage and count of 10 or more in Chapters 1, 4, 5 and 6 with the values in `results/pilot_R2/*.json`. Output: `verification/chapter_number_check.txt`.

| Chapter | Numbers checked | Matched directly | Not matched directly | Resolution of the unmatched |
|---|---:|---:|---:|---|
| 5 | 538 | 524 | 14 | Sums of per-group counts (2,998; 682); configuration values (2,000; seed); section or time stamps; bytes shown in KB (4.4; 12.4); the historical R1 value 2.9 KB, now labelled as such; a difference of two values (10.5 points = 0.419 − 0.314); and 42.5% = 0.425 (matched after percent conversion with one decimal) |
| 4 | 63 | 31 | 32 | Versions, hardware, test counts (verified in `pytest_2026-10-30.txt`), Chapter 3 equation and section numbers, comparison counts (verified in the comparison files) |
| 6 | 31 | 30 | 1 | 193 tests (verified) |
| 1 | 6 | 2 | 4 | Section numbers |

**Corrected in R3:** Chapter 5 R2 gave the median memory as 2.9 KB, citing `results/pilot_R2/latency_memory_profile.json`. That file records 4,364 bytes; 2.9 KB came from the R1 file. The text now gives 4.4 KB, labels 2.9 KB as the R1 value, and states that the re-run reproduced 4.4 KB.

## 5. Tables and figures and their source data

| Item | Source file |
|---|---|
| Tables 5.2–5.4 | `e0_pilot.json`, `e1_crossfit.json` |
| Tables 5.5, 5.6 | `e2_e5_e6_observe_only.json`, `r2_breakdowns.json`, `benign_release_breakdown.json` |
| Tables 5.7–5.10 | `e4_e5_enforcement_replay.json`, `r2_breakdowns.json` |
| Table 5.11 | `e1_crossfit.json`, `e2_e5_e6_observe_only.json`, `e4_e5_enforcement_replay.json` |
| §5.8 | `e3_a2_cusum_observe_only.json` |
| §5.9 | `e2_e5_e6_observe_only.json` (`e6_grid`) |
| §5.10 | `sensitivity_post_hoc_exclude_user_task_15.json`; `label_audit_*` |
| §5.11 | `e4_cross_template_and_defenses.json` |
| Figure 5.1 | Generated by `experiments/pilot/figures.py` from `e1_crossfit.json` |
| Figure 5.2 | Generated by `experiments/pilot/figures.py` from `e4_e5_enforcement_replay.json` |

Both figures were regenerated in the re-run.

## 6. Statements the evidence does not support

These are not made in the thesis, and they must not be added:
- that REM reduces attack success for live or adaptive agents;
- any causal effectiveness claim;
- statistical significance;
- superiority over the baseline or over published defenses;
- production readiness;
- any per-backbone conclusion;
- that the labels are correct, because the human label audit has not been performed.

**Paired differences** (Table 5.8) are reported with grouped-bootstrap intervals over nine injection-task groups. No hypothesis test was performed, and no correction for multiple comparisons was applied.
