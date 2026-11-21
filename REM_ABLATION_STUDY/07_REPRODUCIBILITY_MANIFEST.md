# 07 Reproducibility manifest

## Git

| Item | Value |
|---|---|
| Branch | `claude/rem-ablation-study-20261121` |
| Base | `780c6f8` (MELON comparison), which contains R8 at `f4ff23f` |
| Protocol freeze | `93e6630`: protocol, implementation audit, runner and hashes, committed before any arm was scored |
| Results commit | the commit after `93e6630` on this branch (see `git log`) |
| Frozen REM v1.0 | `rem/` at `9fddfa7` (decision path unchanged); pilot pipeline `experiments/pilot/` at `ea621c3`; `configs/exploratory/pilot_e0.yaml` sha256 `8e1aa107…` |
| Untouched | R8 (`REM_FINAL_SUBMISSION/thesis_r8`, `REM_FINAL_THESIS_COMPLETION_2026_11_19`), the MELON comparison (`REM_MELON_COMPARISON_2026_11_19`), every earlier study folder and `results/` |

## Fitted state (fresh run, 21 Nov 2026)

**Command:**

```
build_dataset.py; e0_pilot.py; run_main.py crossfit rmod replay   (6 min 54 s)
```

| File | sha256 |
|---|---|
| `steps.pkl` | `876211cdf4975568b0fe9b8f4fb1312471fd514c66f3dac283273ac28f792c5d` |
| `state/crossfit.pkl` | `27464b4d6c3752b5ad3be62e721b0264671c2ede85190fc611568cfe73b68b2e`, **identical** to the hash recorded in the frozen REM bundle exported at `9fddfa7` |
| `state/rmod.pkl` | `29c2c78ea5628783825e18699f321bc8d3e308ae8723a533d11dd99e59a88ba7`, **identical** to the frozen value |

**Reproduction gate.** 11 / 2,979, 105 / 334, 1,083 / 2,979: PASSED (`results/reproduction_gate.json`).

**Protocol and code hashes.** `01_PROTOCOL_HASHES.sha256` covers the protocol, the audit, the runner, `run_main.py`, `data.py`, the REM replay, trace, policy, evidence, bootstrap and cross-fit modules, and the configuration. A test checks them.

**Outputs.**
- `results/output_hashes.sha256`.
- `05_EPISODE_RESULTS.jsonl.gz`: 54,963 lines, one per (population, episode, arm), with every call `[tool, verdict, released, label, verdict_source]`. It is gzip-compressed (28 MB uncompressed).

## Environment

- **Software:**
  - Python 3.11.17;
  - NumPy 2.4.6, SciPy 1.17.1, scikit-learn 1.9.1, Matplotlib 3.11.2;
  - AgentDojo 0.1.35 (PyPI);
  - recorded runs at `ethz-spylab/agentdojo@089ed468`.
- **Hardware:** 4 CPU cores, 15.7 GiB RAM, no GPU.
- **Seeds:** seed 20261027 and 2,000 bootstrap resamples, from the configuration; `PYTHONHASHSEED=0`.
- **Package list:** `results/pip_freeze.txt`.

## Commands

```bash
export S=<new state dir> PYTHONHASHSEED=0 AGENTDOJO_RUNS=/home/user/ethz-spylab/agentdojo/runs
(cd experiments/pilot && PILOT_RESULTS_DIR=$S python3 build_dataset.py && PILOT_RESULTS_DIR=$S python3 e0_pilot.py \
   && PILOT_RESULTS_DIR=$S python3 run_main.py crossfit rmod replay)
PILOT_RESULTS_DIR=$S python3 experiments/ablation_study/run_ablation.py      # about 7 min
python3 experiments/ablation_study/make_tables.py
python3 experiments/ablation_study/make_figures.py
PILOT_RESULTS_DIR=$S python3 -m pytest -q tests/test_rem_ablation_study.py
```

## Test results (executed 21 Nov 2026)

| Suite | Result |
|---|---|
| `tests/test_rem_ablation_study.py` with `PILOT_RESULTS_DIR` set | **8 passed** |
| Full repository suite (main environment, without `PILOT_RESULTS_DIR`) | **813 passed, 27 skipped, 1 xfailed** |
| `tests/test_rem_vs_melon.py` (MELON environment) | **9 passed** |

In the full repository suite:
- the ablation configuration test is skipped there, because it needs the state;
- the MELON-environment tests are skipped, because they need AgentDojo 0.1.29.

## Logs

- `logs/fresh_pilot_reproduction.log`
- `logs/ablation_run.log`
