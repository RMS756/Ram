# Appendix — Experiment Reproduction

This appendix lists the commands that regenerate every number, test result and document of the
five-chapter thesis. Run them from the repository root on branch `claude/rem-r4-corrections-3ktvze`.
They were executed in this project as recorded in the logs cited. The full guide with background is
`REM_FINAL_THESIS/reports/EXPERIMENT_REPRODUCTION_GUIDE.md`.

## 1. Environment

```bash
python3 -m pip install -e ".[dev]" agentdojo==0.1.35 matplotlib
git clone https://github.com/ethz-spylab/agentdojo.git /home/user/ethz-spylab/agentdojo
git -C /home/user/ethz-spylab/agentdojo checkout 089ed468cf3ed0322acc66b0211f26d9d90dbf60
```

The AgentDojo version (package 0.1.35, repository commit `089ed468…`) is the one used for the
pilot. It is **not** approved as the frozen benchmark version (OI-14).

## 2. Tests

```bash
python3 -m pytest -o addopts="" -q            # expected: 217 passed (205 pre-live + 12 live-integration)
```

Log of the last run: `experiments/live/smoke_output/pytest_full_with_live.log` (217 passed,
3 Nov 2026). The 205-test R4 run reported in Table 3.22: `REM_FINAL_THESIS/verification/pytest_R4.txt`.

## 3. Recorded-trace evaluation (Chapter 4, §4.1–4.11)

```bash
# write OUTSIDE the repository so committed results are not overwritten
PILOT_RESULTS_DIR=/path/to/rerun PYTHON=python3 \
AGENTDOJO_RUNS=/home/user/ethz-spylab/agentdojo/runs bash experiments/pilot/run_all.sh

# compare with the committed result set (expected: 0 analytical differences)
python3 REM_FINAL_THESIS/verification/compare_reproduction.py /path/to/rerun results/pilot_R2 /path/to/comparison.json

# mathematical checks of the derived equations (expected: ALL PASS)
python3 REM_FINAL_THESIS/verification/verify_equations.py
```

All randomness is seeded (20261027). Analytical values were identical in every re-execution
(`REM_FINAL_THESIS/verification/reproduction_comparison_R4.json`); wall-clock time and, between
some runs, memory vary. These re-executions were made by this project; no external replication
exists.

## 4. Scripted-agent harness checks of the live integration (not results)

```bash
python3 -m pytest -o addopts="" -q -p no:cacheprovider tests/test_live_integration.py      # 12 passed
PILOT_RESULTS_DIR=results/pilot_R2 python3 experiments/live/smoke_scripted.py injection_task_0 smoke.json
#   expected: 480 episodes (160 per condition B0, B1, REM), 0 errors
```

The live run with a language model is **not executed**; its commands and blockers are in
`LIVE_AGENTDOJO_DETAILS.md` (this folder).

## 5. The five-chapter thesis

```bash
python3 REM_FINAL_THESIS/tools/figures_5ch.py     # 6 new figures (diagrams; Fig 3.2 from equations; Fig 4.3 from results/pilot_R2)
python3 REM_FINAL_THESIS/tools/make_5ch.py        # five chapters from chapters_R5 (R5 is read, never written)
python3 REM_FINAL_THESIS/tools/build_5ch.py       # DOCX + PDF (needs pandoc and LibreOffice)
python3 REM_FINAL_THESIS/tools/check_5ch.py       # content preservation vs R5
python3 REM_FINAL_THESIS/tools/qa_5ch.py          # structure, tracked changes, margins, blank pages, PDF properties
python3 REM_FINAL_THESIS/tools/source_map_5ch.py  # audit/THESIS_SOURCE_MAP.md
python3 REM_FINAL_THESIS/tools/tables_5ch.py      # tables/*.csv from the result JSON files
```

## 6. What cannot be reproduced here

- The live closed-loop experiment (needs D-15 decisions and an LLM credential).
- The human label audit (package prepared: `results/pilot_R2/label_audit_human_package.csv`).
- The first R1 execution before commit `aa66f22` (its log was not preserved).
