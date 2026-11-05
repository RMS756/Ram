# Experiments — where the code lives (no functional code is duplicated here)

| Folder | Code | Status |
|---|---|---|
| MELON_INTEGRATION | `rem/integration/melon_rem.py`; `experiments/melon_rem/` (runner, spending guard, analysis, protocol, source manifest); tests `tests/test_melon_rem_*.py` | Implemented; 30 local checks pass; **not executed live** |
| REM_INTEGRATION | Live harness `rem/integration/agentdojo_live.py`, `experiments/live/`; deployment gateway `rem/deployment/gateway.py`, `experiments/deployment_sim/`; replay `rem/integration/agentdojo_replay.py` | Replay and deployment simulation **executed**; live **not executed** |
| REM_LITE | `experiments/rem_lite/run_rem_lite.py`; gateway configuration `REMLITE` in `experiments/deployment_sim/serve_gateway.py`; tests `tests/test_rem_lite.py` | **Executed** (Mode A) |
| CONFIGS | `full_rem.yaml`, `rem_lite.yaml` (records); `configs/exploratory/pilot_e0.yaml` (declared values); `experiments/melon_rem/melon_rem_config_TEMPLATE.yaml`; `experiments/live/live_config_TEMPLATE.yaml` | — |
| RUNNERS | Commands below | — |

## Runners

```bash
# Mode A: REM-Lite vs Full REM vs No Defense (offline held-out + NO-ADAPT replay)
PILOT_RESULTS_DIR=<frozen pilot state> python3 experiments/rem_lite/run_rem_lite.py results/rem_lite/<run>

# Mode A: deployment simulation, four configurations
PILOT_RESULTS_DIR=<frozen pilot state> python3 experiments/deployment_sim/run_deployment_sim.py \
    --out results/deployment_sim/<run> --configs B0,REMLITE,B1,REM --sweep ""

# Mode B (NOT EXECUTED; needs credentials, network access to api.openai.com, a spending cap and design inputs)
/home/user/venvs/melon029/bin/python experiments/melon_rem/run_melon_rem.py --config <cfg> --out <dir> [--dry-run]
python3 experiments/live/run_live.py --config <cfg> --out <dir>
```
