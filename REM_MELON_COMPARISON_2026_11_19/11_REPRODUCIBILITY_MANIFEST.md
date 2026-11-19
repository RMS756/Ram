# 11 Reproducibility manifest

## Sources and revisions

| Item | Revision / hash |
|---|---|
| This repository | branch `claude/rem-melon-comparison-20261119`, from `f4ff23f` (R8). Protocol freeze commit `a1db36a`. |
| REM v1.0 | `rem/` at `9fddfa7` (decision path unchanged); frozen bundle `experiments/melon_rem/frozen/frozen_rem_bundle.pkl` sha256 `983c5b0d54de01cdb37467526f3aea2c4065f888f59c140ea6714ec1b0d3e2c5` |
| MELON | `ucsb-mlsec/MELON@06014c7c72d3e9a1f9a27b8742e8bf711689caad` and `kaijiezhu11/MELON@4d3cc9c0175cc26332aac696ac5556c3f85a5e8e`; `pi_detector.py` sha256 `5a7f6b28228545e0d4ad9e98c9080ad819bb1cf471a67a31c8c4466b199a9017` (identical in both; loaded by path, not vendored, because the repositories have no licence file) |
| AgentDojo | 0.1.29 in `/home/user/venvs/melon029`, as required by unmodified MELON; banking v1; attack `important_instructions` |
| Protocol and code hashes | `06_PROTOCOL_HASHES.sha256`: protocols 04 and 06, harness, runner, analysis, config template, spending guard, REM integration modules, REM bundle, MELON file |
| Lock files | `manifests/pip_freeze_melon029.txt` (MELON environment), `manifests/pip_freeze_main.txt` |

## Code (`experiments/rem_vs_melon/`)

| File | Purpose |
|---|---|
| `harness.py` | three-arm pipelines; LLM and embedding call counters; episode runner |
| `run_rem_vs_melon.py` + `config_TEMPLATE.yaml` | fail-closed live runner (paired triples; spending guard for paid providers; local OpenAI-compatible provider; MELON-ADAPTED label for non-original embeddings) |
| `analyze_live.py` | endpoints, grouped bootstrap, McNemar sensitivity, figures (live runs only; `--diagnostic` otherwise) |
| `pilot_scripted.py` | scripted integration pilot (test doubles stated) |
| `summarize_pilot.py` | pilot mechanism-activity table |
| `estimate_volume.py` | workload planning estimate from recorded trajectories |
| `make_figures.py` | planning figure |

## Tests

| Test file | Environment | Result |
|---|---|---|
| `tests/test_rem_vs_melon.py` (9 tests) | MELON env | **9 passed** |
| `tests/test_melon_rem_integration.py` | MELON env | 21 passed, 2 skipped, as before |
| Main environment | – | the new file is skipped (needs AgentDojo 0.1.29) |

## Commands

```bash
V=/home/user/venvs/melon029/bin/python
$V experiments/rem_vs_melon/pilot_scripted.py REM_MELON_COMPARISON_2026_11_19/results/scripted_pilot_full --cases full
python3 experiments/rem_vs_melon/summarize_pilot.py REM_MELON_COMPARISON_2026_11_19/results/scripted_pilot_full REM_MELON_COMPARISON_2026_11_19/results/scripted_pilot_summary.md
$V experiments/rem_vs_melon/estimate_volume.py REM_MELON_COMPARISON_2026_11_19/results/workload_estimate.json
python3 experiments/rem_vs_melon/make_figures.py
$V -m pytest -o addopts="" -q tests/test_rem_vs_melon.py tests/test_melon_rem_integration.py
# live run (when authorised): fill config_TEMPLATE.yaml, then
$V experiments/rem_vs_melon/run_rem_vs_melon.py --config <cfg> --out <dir> --dry-run
$V experiments/rem_vs_melon/run_rem_vs_melon.py --config <cfg> --out <dir>
python3 experiments/rem_vs_melon/analyze_live.py <dir> REM_MELON_COMPARISON_2026_11_19/results/live
```

## Raw outputs

**Scripted pilot:**
- `results/scripted_pilot_full/episodes.jsonl` (480 episodes, with full transcripts, REM verdicts and latencies, and MELON flags);
- `results/scripted_pilot_full/melon_upstream_stdout.log` (MELON's own printed similarities);
- `results/scripted_pilot_smoke/` (13-case smoke run 2).

**Live:** none exist.
