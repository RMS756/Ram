# EXPERIMENT STATUS — what was run, what was reproduced, what was not run

**Date:** 3 November 2026. **Status key:** EXECUTED (logs and result files exist) · REPRODUCED
(re-executed from a clean state with 0 analytical differences) · NOT EXECUTED · NOT DONE.

All executed analyses use the declared **exploratory** design values (`pilot_e0_exploratory`:
C_FA = 1; C_miss = 1/5/10/20 for tiers 1–4; C_mod = 0.5; C_esc = 0.3; feature set retained in E0;
label rule `reference_match_pilot_e0`). These values are **not supervisor-approved** (PILOT-AUTH,
SD-FREEZE). Every result file carries the label "EXPLORATORY — NOT THESIS RESULTS — SUPERVISOR
DECISION REQUIRED".

## 1. Recorded-trace evaluation (Chapter 4, §4.1–4.11)

Data: recorded AgentDojo banking traces of 21 real LLM agents (3,334 episodes; 6,762 proposed tool
calls), `important_instructions` attack; plus cross-template and recorded-defense traces for one
backbone. Code: `experiments/pilot/`; driver `experiments/pilot/run_all.sh`.

| Experiment | Thesis | Kind of evidence | Result file (`results/pilot_R2/`) | Status |
|---|---|---|---|---|
| E0 pilot: feasibility, feature retention | §4.3 | in-fold fitting | `e0_pilot.json` | EXECUTED · REPRODUCED |
| E1 nested grouped cross-fitting (9 outer folds by injection task × 4 inner) | §4.4, §4.7 | held-out predictions | `e1_crossfit.json` | EXECUTED · REPRODUCED |
| E2/E5/E6 observe-only verdicts (REM, B1, REM-noEsc; ablations) | §4.5, §4.7, §4.9 | observe-only decisions on held-out predictions | `e2_e5_e6_observe_only.json` | EXECUTED · REPRODUCED |
| E3 / A2 CUSUM | §4.8 | **observe-only**; never in the verdict path | `e3_a2_cusum_observe_only.json` | EXECUTED · REPRODUCED |
| E4 cross-template and recorded defenses | §4.4, §4.11 | held-out predictions; recorded outcomes of 4 distributed defenses (not run by REM) | `e4_cross_template_and_defenses.json` | EXECUTED · REPRODUCED |
| E4/E5 enforcement replay (B0, B1, REM, REM-noEsc; step- and episode-level semantics; two reviewer bounds) | §4.6 | **NO-ADAPT replay** in the AgentDojo sandbox | `e4_e5_enforcement_replay.json` | EXECUTED · REPRODUCED (analytical values; latency values volatile) |
| r_mod and replay validity | §4.6 | oracle-Modify replays within fitting folds | `e4_rmod_and_replay_validity.json` | EXECUTED · REPRODUCED |
| Post-hoc sensitivity: exclude user_task_15 | §4.10 | sensitivity | `sensitivity_post_hoc_exclude_user_task_15.json` | EXECUTED · REPRODUCED |
| Complete-call processing time (R4 timer) | §3.16.14, Table 3.25 | runtime measurement | `results/pilot_R4/e4_e5_enforcement_replay.json`, `latency_memory_profile.json` | EXECUTED (R4, 1 Nov 2026); values vary between runs by nature |

**Reproduction.** `verification/reproduction_comparison_R4.json` and
`verification/reproduction_all_differences_R4.json`: `diff_analytical = 0` in every result file;
differences are limited to volatile fields (timestamps, commit hashes, latency). This is a
re-execution of the same code from a clean state within the project, **not an independent
replication by another team**.

## 2. Labels

| Item | Status |
|---|---|
| Automatic label rule (`reference_match_pilot_e0`) | EXECUTED; exploratory, not approved |
| AI-only label inspection | EXECUTED (Section 4.10); not a human audit |
| Human label audit (package `results/pilot_R2/label_audit_human_package.csv`) | **NOT DONE** (needs a human annotator; D-series item) |
| Labeling of attacker-induced read operations | **Unresolved** design item (CLAUDE.md data lock) |

## 3. Software verification

| Item | Status |
|---|---|
| Full test suite | **217 passed** on 3 Nov 2026 (`experiments/live/smoke_output/pytest_full_with_live.log`) = 205 pre-live tests (Table 3.22; R4 run 1 Nov 2026, `verification/pytest_R4.txt`) + 12 live-integration tests |
| Equation verification | `verification/verify_equations_output_R4.txt` (unchanged) |

## 4. Live closed-loop experiment (Deliverable A)

| Item | Status |
|---|---|
| Integration module `rem/integration/agentdojo_live.py` | IMPLEMENTED |
| Fail-closed runner `experiments/live/run_live.py` (exit 2 design inputs missing; 3 credential missing; 4 unsupported value) | IMPLEMENTED; verified to exit 2 on the template config |
| Analysis `experiments/live/analyze_live.py` (ASR, benign utility, utility under attack, intervention, adaptation, latency; grouped bootstrap) | IMPLEMENTED; exercised only on synthetic records in a unit test (`test_analysis_on_synthetic_records`) |
| Integration tests `tests/test_live_integration.py`: allow executes; blocked calls not executed; Modify semantics; Escalate withholds; multiple calls per turn; tool-result IDs preserved; retry; replanning; no label leakage into the agent; no episode-state contamination; audit records; metrics; fail-closed runner | **12 / 12 PASS** |
| Scripted ground-truth smoke run (B0/B1/REM, fold `injection_task_0`, 160 episodes each) | EXECUTED; 480 episodes, 0 errors; **harness check only — not a result** |
| **Live run with a language model** | **NOT EXECUTED. NO LIVE RESULT EXISTS.** |

**Blockers.**
1. No LLM API credential in the environment (`api.anthropic.com` returned HTTP 401 without a key;
   other provider and model-weight hosts refused by the network policy).
2. Undecided design inputs (D-15): LLM backbone(s) and decoding settings; number of repeats; which
   frozen fitted parameters to use (fold or refit on all data); authorisation of the run;
   pre-registration of the analysis.

**Exact commands once unblocked** (from `experiments/live/LIVE_EXPERIMENT_REPRODUCTION_GUIDE.md`):

```bash
cp experiments/live/live_config_TEMPLATE.yaml experiments/live/live_config.yaml
#   replace every REQUIRED_FROM_DESIGN value with the recorded decision (LIVE_EXPERIMENT_PROTOCOL.md §3)
python3 experiments/live/check_live_config.py experiments/live/live_config.yaml     # must exit 0
export ANTHROPIC_API_KEY=...        # or OPENAI_API_KEY / GOOGLE_API_KEY, matching models.backbones
PILOT_RESULTS_DIR=$PILOT_RESULTS_DIR AGENTDOJO_RUNS=/home/user/ethz-spylab/agentdojo/runs \
  python3 experiments/live/run_live.py --config experiments/live/live_config.yaml --out results/live_<date>
python3 experiments/live/analyze_live.py results/live_<date>/episodes.jsonl results/live_<date>/summary.json
```

## 5. Not run in this thesis

- Live / adaptive-agent enforcement (above).
- Any controlled comparison with a published defense on a shared protocol.
- Other AgentDojo suites (workspace, travel, Slack) and other benchmarks.
- Repeated runs of the same task pairing (the recorded traces contain one run per pairing per agent).
- Confirmatory evaluation under supervisor-approved design values.
- Optional CUSUM scenarios beyond the observe-only analysis.

## 6. Extension study: original MELON vs MELON + REM (added 5 Nov 2026; thesis §4.14)

| Item | Status |
|---|---|
| Upstream MELON | Pinned at `kaijiezhu11/MELON@4d3cc9c`; `pi_detector.py` sha256-checked; not vendored (no licence file) |
| Environment | AgentDojo 0.1.29 (required by the upstream code); separate virtual environment |
| Integration (`rem/integration/melon_rem.py`) | IMPLEMENTED. REM replaces only the tool executor inside MELON's loop |
| Frozen REM bundle | EXPORTED (`experiments/melon_rem/frozen/`, sha256 `983c5b0d…`); deterministic |
| Local verification | **30/30 pass** in the MELON environment (scripted agents, fake embeddings, fake provider); 225 passed + 1 skipped in the main environment |
| Pilot (26 episodes) and final run (up to 320 × repeats) | **NOT EXECUTED.** No spending authorisation or cap and no credential in this session; design inputs open (`MELON_REM_EXPERIMENT_PROTOCOL.md` §7) |
| Results | **None.** Table 4.15 reads "not executed" in every cell |
