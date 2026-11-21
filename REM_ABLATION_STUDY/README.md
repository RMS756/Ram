# REM component ablation study (21 November 2026)

**What it is.** Offline, paired, pre-registered ablation of REM v1.0 on three populations of recorded AgentDojo banking episodes.
- **Branch:** `claude/rem-ablation-study-20261121`.
- **Protocol frozen at:** `93e6630`, before any arm was scored.
- **Frozen code:** REM v1.0, R8, the baselines and the MELON work are not modified.

| File | Content |
|---|---|
| `01_ABLATION_PROTOCOL.md` | Research question, hypotheses, arms, invalid ablations, populations, metrics, statistics, closed-loop feasibility, safety |
| `01_PROTOCOL_HASHES.sha256` | Hashes of the frozen protocol, runner and REM modules (checked by a test) |
| `02_IMPLEMENTATION_AUDIT.md` | Layer-to-module map, dependencies, validity of each requested ablation |
| `03_EXPERIMENT_RESULTS.md` | Results, the learned-decision questions, statistical notes, limitations |
| `04_RESULTS.csv` | One row per (population, arm) metric, with paired differences and intervals |
| `05_EPISODE_RESULTS.jsonl.gz` | 54,963 episode-arm records with every call's verdict, release, label and verdict source |
| `06_FIGURES/` | Five figures generated from `results/ablation_metrics.json` |
| `07_REPRODUCIBILITY_MANIFEST.md` | Commits, hashes, versions, commands, test counts |
| `08_THESIS_CHAPTER_4_SECTION.md` | Proposed Chapter 4 subsection (R8 not overwritten) |
| `09_ARABIC_SUMMARY.md` | Arabic summary |
| `results/`, `logs/` | Metrics JSON, generated tables, reproduction gate, hashes, package list, run logs |

**Code.**
- `experiments/ablation_study/`: `run_ablation.py`, `make_tables.py`, `make_figures.py`.
- Tests: `tests/test_rem_ablation_study.py`.

## Limits

- **Not an ASR.** Call-level withholding rates are not attack success rates.
- **No closed loop.** No live-LLM run was executed: there was no model, no network access to providers and no spending authorisation.
