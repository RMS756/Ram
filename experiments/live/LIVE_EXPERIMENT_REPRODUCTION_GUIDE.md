# Live Experiment: Reproduction Guide

## 1. Prerequisites (verified on 3 November 2026 unless marked)

```bash
python3 -m pip install -e ".[dev]" agentdojo==0.1.35 anthropic openai     # installed: anthropic 2.3.0, openai 3.41.0
git clone https://github.com/ethz-spylab/agentdojo.git /home/user/ethz-spylab/agentdojo
git -C /home/user/ethz-spylab/agentdojo checkout 089ed468cf3ed0322acc66b0211f26d9d90dbf60
```

## 2. Freeze the offline fit (verified; about 11 minutes)

```bash
export PILOT_RESULTS_DIR=/path/to/frozen_pilot      # outside the repository
PYTHON=python3 AGENTDOJO_RUNS=/home/user/ethz-spylab/agentdojo/runs bash experiments/pilot/run_all.sh
```

## 3. Tests and smoke run (verified)

```bash
python3 -m pytest -o addopts="" -q -p no:cacheprovider tests/test_live_integration.py           # 12 passed
PILOT_RESULTS_DIR=$PILOT_RESULTS_DIR python3 experiments/live/smoke_scripted.py injection_task_0 smoke.json   # 480 episodes, 0 errors
```

## 4. Live run (NOT EXECUTED: needs decisions and a credential)

```bash
cp experiments/live/live_config_TEMPLATE.yaml experiments/live/live_config.yaml
#   replace every REQUIRED_FROM_DESIGN value with the recorded decision (see LIVE_EXPERIMENT_PROTOCOL.md §3)
python3 experiments/live/check_live_config.py experiments/live/live_config.yaml     # must exit 0
export ANTHROPIC_API_KEY=...        # or OPENAI_API_KEY / GOOGLE_API_KEY, matching models.backbones
PILOT_RESULTS_DIR=$PILOT_RESULTS_DIR AGENTDOJO_RUNS=/home/user/ethz-spylab/agentdojo/runs \
  python3 experiments/live/run_live.py --config experiments/live/live_config.yaml --out results/live_<date>
python3 experiments/live/analyze_live.py results/live_<date>/episodes.jsonl results/live_<date>/summary.json
```

Exit codes of `run_live.py`:

| Code | Meaning |
|---|---|
| 2 | A design input is missing |
| 3 | The credential is missing |
| 4 | Unsupported value |

**Cost and duration estimate:** not computed, because they depend on the undecided backbone, number of repeats and cells. A full grid over all task pairs is 160 cells × conditions × semantics × reviewer models × repeats × backbones episodes.
