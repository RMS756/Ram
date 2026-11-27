# Deliverable 19: Reproducibility package (DiD-3)

**Environment.**
- Python 3.11.17; AgentDojo 0.1.35 (PyPI); NumPy 2.4.6; PyYAML 6.0.1.
- Recorded runs: AgentDojo repository at `089ed468`, in `/home/user/ethz-spylab/agentdojo/runs`.

**Commits.**

| Commit | Content |
|---|---|
| `8678add` | Code and protocol freeze |
| `0421c5f` | Cost protocol |
| `e432189` | Amendment 50a |

The final results commit is the one that adds this file.

**Seeds:** 20261027 (permutations, bootstrap); 20261127 (label-audit order).

**Hashes:** `results/did3_manifest.sha256` (SHA-256 of code, protocols, raw and derived results).

## Commands (from the repository root)

```bash
# 0. Regenerate REM v1.0 pilot state (identical to earlier DiD runs)
export PILOT_RESULTS_DIR=$PWD/REM_DEFENSE_IN_DEPTH/work/pilot
(cd experiments/pilot && python3 build_dataset.py && python3 e0_pilot.py && python3 run_main.py crossfit rmod observe)
# 1. Unit tests
python3 -m pytest REM_DEFENSE_IN_DEPTH/tests -q
# 2. Scenario suite
python3 REM_DEFENSE_IN_DEPTH/code/did3_scenarios.py
# 3. Detector evaluation (SIG-2)
python3 REM_DEFENSE_IN_DEPTH/code/sig2_detection.py
# 4. Replay arms (about 6 min on 4 cores; 169,577 replays)
python3 REM_DEFENSE_IN_DEPTH/code/did3_run.py
python3 REM_DEFENSE_IN_DEPTH/code/did3_analyze.py      # prints "gates passed: True"
# 5. Amendment 50a (coverage with rule verdicts)
python3 REM_DEFENSE_IN_DEPTH/code/did3_amend1.py
# 6. Cost sensitivity (36 cells x 3 arms)
python3 REM_DEFENSE_IN_DEPTH/code/did3_cost.py
# 7. Figures
python3 REM_DEFENSE_IN_DEPTH/code/fig_architecture.py
```

**Determinism.** Replay is deterministic. Re-running reproduces every count exactly. The gates check the REM v1.0 and B0 counts.

**Raw records.** `did3_raw.jsonl.gz` holds one line per (population, arm, episode), with these fields:
- utility and security;
- the per-call tuple (label, released, state-changing, verdict, decisive rules, rule codes);
- gateway counters;
- latencies.

`did3_raw_amend1.jsonl.gz` adds the rule verdicts.
