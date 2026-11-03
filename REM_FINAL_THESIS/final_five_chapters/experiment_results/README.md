# Experiment results used by the five-chapter thesis

**No live-agent result exists. The live closed-loop experiment was not executed.**

## Authoritative result files (not copied; cited by path in the thesis)

| Thesis | Files | Kind |
|---|---|---|
| Chapter 4, §4.1–4.11; Chapter 5 Table 5.1 | `results/pilot_R2/*.json` (commit `84a8c21`, `experiments/pilot/run_all.sh`) | Exploratory recorded-trace analyses (held-out predictions; observe-only decisions; NO-ADAPT replay). Every file is labelled "EXPLORATORY — NOT THESIS RESULTS — SUPERVISOR DECISION REQUIRED" |
| §3.16.14 Table 3.25; §4.6 processing time | `results/pilot_R4/e4_e5_enforcement_replay.json`, `results/pilot_R4/latency_memory_profile.json` | R4 re-execution with the complete-call timer (1 Nov 2026) |
| Reproduction | `REM_FINAL_THESIS/verification/reproduction_comparison_R4.json`, `reproduction_all_differences_R4.json` | 0 analytical differences in every file; re-execution by this project, not an external replication |
| Figure 4.3 | `results/pilot_R2/e4_e5_enforcement_replay.json` read by `REM_FINAL_THESIS/tools/figures_5ch.py` | Chart of existing replay values |

## Copies in this folder (from the live-integration work, 3 Nov 2026)

| File | Content | Status |
|---|---|---|
| `pytest_full_with_live.log` | Full test suite: **217 passed** | Software verification |
| `pytest_live_integration.log` | Live-integration tests: **12 passed** | Software verification |
| `live_harness_smoke_summary.json` | Summary of the scripted ground-truth smoke run: 480 episodes (B0/B1/REM × 160), 0 errors | **Harness check only — scripted non-adaptive agent, not an LLM. Must not be cited as an attack-success, utility or effectiveness result.** Full per-episode file: `experiments/live/smoke_output/smoke_scripted_ground_truth.json` |
