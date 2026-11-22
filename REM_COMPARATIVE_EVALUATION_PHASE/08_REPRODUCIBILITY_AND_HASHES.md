# 08 Reproducibility and hashes

## Git

| Item | Value |
|---|---|
| Branch | `claude/rem-comparative-evaluation-20261122` |
| Start | `76ac629786c87259261ab1ff4f3b58af7630ebde` (external-defence audit); clean working tree at start |
| Protocol freeze | `09d49c0`: protocol, runners and `01_PROTOCOL_HASHES.sha256`, committed before any scored run |
| Amendment 1 | `01a_AMENDMENTS.md` + `01a_AMENDMENT_HASHES.sha256`: a report-key fix in `run_live_comparison.py`; no design change |
| Results commit | the commit after `09d49c0` on this branch |
| Unchanged | `rem/`, `configs/`, `experiments/pilot/`, `experiments/ablation_study/`, R8, `REM_MELON_COMPARISON_2026_11_19/`, `REM_ABLATION_STUDY/`, `REM_EXTERNAL_DEFENSE_AUDIT/` |

## Upstream code (not vendored; `REM_EXTERNAL_DEFENSE_AUDIT/results/upstream_pins.json`)

| Component | Pin |
|---|---|
| Progent enforcement | `sunblaze-ucb/progent@3e797539…`, exported to `/home/user/upstream/progent_3e79753`; `secagent/tool.py` sha256 `59b2cd64…` (checked at load) |
| Progent policy | `@9befb41`; file sha256 `43da7d0298bd5ec0de158c4fa3d7b59c4038dc290eb517762c4f39451fac0b6f`; block sha256 `b302d30195800de29ebbc366718c56c76a6a5cf08d4f14db6321e6258356a568` |
| DRIFT | `SaFo-Lab/DRIFT@6fd3df4763fad77398c3c273c2a4fe14dd50f7ea`; `prompts.py` `c988dded…`, `client.py` `e2b49f87…` |
| MELON | `ucsb-mlsec/MELON@06014c7`; `pi_detector.py` `5a7f6b28…a9017` |
| AgentDojo | PyPI 0.1.35 (0.1.29 for MELON); recorded runs `ethz-spylab/agentdojo@089ed468` |

## Fitted REM state (fresh run of 21 Nov 2026, reused)

| File | sha256 |
|---|---|
| `crossfit.pkl` | `27464b4d6c3752b5ad3be62e721b0264671c2ede85190fc611568cfe73b68b2e` |
| `rmod.pkl` | `29c2c78ea5628783825e18699f321bc8d3e308ae8723a533d11dd99e59a88ba7` |

Both are identical to the frozen export (`REM_ABLATION_STUDY/07_REPRODUCIBILITY_MANIFEST.md`).

## Environments

- `/home/user/venvs/rem_progent_replay`: system site packages plus Progent's dependencies (`results/pip_freeze_rem_progent_replay.txt`).
- `/home/user/venvs/drift`: `REM_EXTERNAL_DEFENSE_AUDIT/results/pip_freeze_drift.txt`.
- Hardware: 4 CPU cores, no GPU.
- `PYTHONHASHSEED=0`.

## Commands

```bash
S=<fresh frozen pilot state>; export PYTHONHASHSEED=0 AGENTDOJO_RUNS=/home/user/ethz-spylab/agentdojo/runs
PILOT_RESULTS_DIR=$S /home/user/venvs/rem_progent_replay/bin/python experiments/comparative_phase/run_offline_comparison.py   # O1, about 3 min
python3 experiments/comparative_phase/episode_level_ablation.py                                                               # O2
PILOT_RESULTS_DIR=$S /home/user/venvs/rem_progent_replay/bin/python experiments/comparative_phase/run_live_comparison.py --mode scripted --out REM_COMPARATIVE_EVALUATION_PHASE/results   # O4
(cd /tmp && DRIFT_UPSTREAM=/home/user/upstream/SaFo-Lab_DRIFT /home/user/venvs/drift/bin/python <repo>/experiments/comparative_phase/run_drift_arms.py --mode scripted --out <repo>/REM_COMPARATIVE_EVALUATION_PHASE/results)          # O5
python3 -m pytest -q tests/test_comparative_phase.py
```

## Outputs

- **Hashes:** `results/output_hashes.sha256`.
- **Logs:** `logs/o1_offline_comparison.log`, `logs/o2_episode_level_ablation.log`, `logs/o4_d0_d1_d2_scripted.log`, `logs/o5_drift_scripted.log`.

## Tests (executed 22 Nov 2026)

| Suite | Result |
|---|---|
| `tests/test_comparative_phase.py` | **6 passed** |
| Full repository suite | **823 passed, 27 skipped, 1 xfailed, 0 failed** (851 collected) |
