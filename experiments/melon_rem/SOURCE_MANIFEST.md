# Source and Dependency Manifest — MELON vs MELON + REM

| Component | Source | Pin |
|---|---|---|
| MELON implementation | https://github.com/kaijiezhu11/MELON | commit `4d3cc9c0175cc26332aac696ac5556c3f85a5e8e`; `pi_detector.py` sha256 `5a7f6b28228545e0d4ad9e98c9080ad819bb1cf471a67a31c8c4466b199a9017` (no licence file: not vendored) |
| MELON paper | arXiv:2502.05174; ICML 2025 | — |
| AgentDojo (MELON environment) | PyPI `agentdojo==0.1.29` (2025-02-24) | wheel sha256 `da5468b06343cb69a29b04320188c46282384bf7d0c97fc514ea7cef4b8d0755` |
| AgentDojo (REM main environment, fitting traces) | PyPI `agentdojo==0.1.35`; runs repository commit `089ed468cf3ed0322acc66b0211f26d9d90dbf60` | unchanged |
| Python (MELON environment) | Python 3.11.17 | venv `/home/user/venvs/melon029` |
| Key packages (MELON environment) | numpy==2.4.6 openai==3.46.0 pydantic==2.14.2 PyYAML==6.0.3 torch==2.9.1 transformers==5.22.1  | full list: `verification/pip_freeze_melon_env.txt` |
| Frozen REM bundle | `frozen/frozen_rem_bundle.pkl` | sha256 `983c5b0d54de01cdb37467526f3aea2c4065f888f59c140ea6714ec1b0d3e2c5`; inputs in `frozen/frozen_rem_bundle.pkl.json` |
| REM pilot configuration | `configs/exploratory/pilot_e0.yaml` | sha256 `8e1aa107cf3ea0ba5eecbb92bc90a2463202cdde476cfe8a98047ffad74e11d0` |

## Recreate the MELON environment
```bash
git clone https://github.com/kaijiezhu11/MELON.git /home/user/upstream/MELON
git -C /home/user/upstream/MELON checkout 4d3cc9c0175cc26332aac696ac5556c3f85a5e8e
python3 -m venv /home/user/venvs/melon029
/home/user/venvs/melon029/bin/pip install -r experiments/melon_rem/verification/pip_freeze_melon_env.txt
# (the PyTorch CPU index was blocked by the network policy; the PyPI torch==2.9.1 build was installed)
```

## Regenerate the frozen REM bundle (main environment)
```bash
PILOT_RESULTS_DIR=<re-execution of experiments/pilot/run_all.sh> \
  python3 experiments/melon_rem/export_frozen_rem.py experiments/melon_rem/frozen/frozen_rem_bundle.pkl
# deterministic (PYTHONHASHSEED=0 is enforced); expected sha256 as above
```
