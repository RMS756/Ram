# Baseline reproduction (original REM, recorded-trace replay)

**Type of run:** offline, step-level, recorded-trace replay in AgentDojo's sandbox (assumption NO-ADAPT: the replayed agent emits its recorded calls whatever REM decides). **No live agent and no model API were used.**

## Commands executed

```bash
S=/tmp/claude-0/-home-user-Ram/c507187c-f302-53cd-9c47-0613a3e4efef/scratchpad/audit_repro
cd /home/user/Ram/experiments/pilot
export PILOT_RESULTS_DIR=$S PYTHONHASHSEED=0
python3 build_dataset.py
python3 e0_pilot.py
python3 run_main.py crossfit rmod replay           # 166,700 replays in 202 s
cd /home/user/Ram
PILOT_RESULTS_DIR=$S python3 REM_AUTHORIZATION_AUDIT/tools/corpus_diagnostics.py <out>
```

Environment:
- Python 3.11.17, numpy 2.4.6, PyYAML 6.0.1, agentdojo 0.1.35;
- AgentDojo runs at commit `089ed468…`;
- seed 20261027 (pilot_e0);
- REM commit `cfb4f40` (core identical to `9fddfa7`).

Log: `../logs/baseline_reproduction_run.log`. Summary: `../logs/reproduced_e4_e5_enforcement_replay_summary.json`.

## Corpus

| Quantity | Value |
|---|---|
| Recorded episodes in the primary role | 3,334 |
| Eligible under AM-4 (B0 replay reproduces recorded utility and security, no error) | **3,313** |
| Attacked / benign eligible episodes | **2,979 / 334** |
| Outer folds | 9 (injection task; benign user tasks assigned round robin) |

## Counts recomputed from per-episode outcomes (not copied from reports)

| Configuration (step-level, no reviewer unless stated) | Successful attacks | Benign successes | Utility under attack | Replay errors |
|---|---|---|---|---|
| B0 (allow all) | 672 / 2,979 | 175 / 334 | 1,465 / 2,979 | 0 |
| **Original REM** | **11 / 2,979** | **105 / 334** | **1,083 / 2,979** | 0 |
| REMnoEsc (Escalate removed from the argmin; post hoc) | 11 / 2,979 | 110 / 334 | 1,113 / 2,979 | 0 |
| B1 (operating-point thresholds) | 164 / 2,979 | 170 / 334 | 1,532 / 2,979 | 0 |
| REM, idealized reviewer (diagnostic bound) | 11 / 2,979 | 166 / 334 | 1,477 / 2,979 | 0 |

- **The reported primary values reproduce exactly:** 11 / 2,979 and 105 / 334. The 1,083 utility-under-attack count matches the value Codex quoted for the original arm, and REMnoEsc matches the reported 11 / 2,979 and 110 / 334.
- The enforcement-replay JSON produced here matches `results/pilot_R4/e4_e5_enforcement_replay.json` on every compared metric (ASR, benign utility and utility under attack with intervals, n, verdict rates, escalation rate, ties) for all 50 shared configurations, with 0 differences.
- Exact ties in the expected-loss argmin: 0 in every configuration.

## What was not reproduced

| Arm | Reason |
|---|---|
| Request cue (primary and user-task holdout) | code not available (commit `bb4218d` absent locally and on GitHub) |
| Parser candidate | same |
| Gating candidate | same |
| Leave-whole-user-task-out enforcement counts (original 12 / 2,979 and 110 / 334; noEsc 13 / 2,979 and 124 / 334; cue + noEsc 12 / 2,979 and 124 / 334) | the repository has no enforcement-replay implementation for user-task folds, so writing one now would be a re-implementation, not a reproduction |

These figures remain **reported by the implementer, not reproduced by this audit**.

## Grouping schemes are not interchangeable

- The primary counts above use injection-task outer folds.
- The reported "original 12 / 2,979" belongs to a different scheme (leave-whole-user-task-out), with different fitted models per fold.
- The two must not be compared as if they were a single evaluation. Report user-task results only as a sensitivity analysis (see `REM_DATA_SPLIT_AUDIT.md`).
