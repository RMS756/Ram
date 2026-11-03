# Appendix — Live AgentDojo Closed-Loop Integration: Details

**Status: IMPLEMENTED AND TESTED WITH SCRIPTED TEST AGENTS. NOT EXECUTED WITH A LANGUAGE MODEL.
NO LIVE RESULT EXISTS.** (Thesis §3.17, §4.12, §4.13.)

Detailed documents (in `experiments/live/`):
`LIVE_EXPERIMENT_CODE_AUDIT.md`, `AGENTDOJO_INTEGRATION_DESIGN.md`, `LIVE_EXPERIMENT_PROTOCOL.md`,
`LIVE_EXPERIMENT_RESULTS.md`, `LIVE_EXPERIMENT_TEST_REPORT.md`, `LIVE_EXPERIMENT_REPRODUCTION_GUIDE.md`,
`REPLAY_VS_LIVE_COMPARISON.md`, `LIVE_EXPERIMENT_LIMITATIONS.md`.

## 1. Architecture

The defended pipeline replaces AgentDojo's tool executor by REM's guarded executor; nothing else
in the agent, its prompts or its tools is changed:

```
SystemMessage → InitQuery → LLM → ToolsExecutionLoop([GuardedToolsExecutor(RemGuard), LLM], max_iters=15) → recorder
```

- `rem/integration/agentdojo_live.py`: `run_defended_episode(...)` builds the pipeline and calls
  AgentDojo's `run_task_with_pipeline` (AgentDojo 0.1.35). The guard (`RemGuard`) and the guarded
  executor are the same code used in the replay; they are reused unchanged.
- A released call is executed by AgentDojo as usual. A withheld call (Block, Escalate without an
  approving reviewer, or Modify where the declared mechanism withholds it) is **not executed**; the
  agent receives a tool result with the **same `tool_call_id`** and an error text beginning "REM:".
  The agent may then retry, replan or stop.
- Every proposal produces an audit record (verdict, calibrated probability, tier, predicates,
  conditional risks, audit-only attribution).
- Conditions: **B0** (no defence), **B1** (same frozen estimator and calibration, consequence-
  independent threshold baseline), **REM** (expected-loss verdict), and REM-noEsc. Semantics:
  step-level (reference) and episode-level (separate experimental policy). Reviewer: idealised or
  none. CUSUM is not used.

## 2. Fail-closed runner

`experiments/live/run_live.py --config <yaml> --out <dir>` refuses to run unless every design input
is supplied: exit **2** design input missing (template values `REQUIRED_FROM_DESIGN`), **3** credential
missing, **4** unsupported value. Frozen parameters are loaded from the pilot state of the fold named
in `fitted_parameters_source: "fold:<id>"`; nothing is refitted on live data. Outputs:
`manifest.json` and `episodes.jsonl`.

## 3. Metrics (computed by `experiments/live/analyze_live.py`)

Attack success rate; benign utility; utility under attack; intervention rates by verdict;
adaptation statistics (retries after a refusal, replans, attacker-goal calls released after a
refusal); per-step guard latency; grouped bootstrap intervals by task pair. Repeated runs of the
same pair are **not** treated as independent observations.

## 4. Tests (all pass)

| Test | Checks |
|---|---|
| `test_allow_executes_the_call` | Allow → the call executes and changes the environment |
| `test_withheld_call_is_not_executed_and_agent_sees_refusal` (Block, Modify) | Withheld calls never execute; the agent sees the refusal with the same id |
| `test_step_level_modify_does_not_persist_but_episode_level_does` | Modify semantics |
| `test_escalate_bounds` | Escalate under the idealised reviewer and with no reviewer |
| `test_multiple_calls_in_one_message_keep_ids_and_order` | Multiple calls per turn; tool-result IDs and order |
| `test_retry_and_replan_are_observed_and_counted` | Retry and replanning after a refusal |
| `test_episode_state_is_not_shared` | No episode-state contamination |
| `test_rem_decision_does_not_depend_on_the_label` | No label leakage into the decision |
| `test_adaptation_statistics_unit` | Audit-based adaptation counts |
| `test_runner_is_fail_closed_on_the_template` | Runner exits 2 on the template |
| `test_analysis_on_synthetic_records` | Metrics and bootstrap on synthetic records |

Log: `experiments/live/smoke_output/pytest_live_integration.log` (12 passed).

## 5. Scripted smoke run (harness check, not a result)

A scripted agent that executes the ground-truth calls of the user task and then of the injection
task, and never adapts, was run through B0, B1 and REM on all 144 attacked pairs and 16 benign tasks
with the real `important_instructions` injections, using the frozen parameters of fold
`injection_task_0` (an arbitrary fold, not a design decision): 480 episodes, 0 errors; withheld calls
never executed. Counts: `experiments/live/smoke_output/smoke_scripted_ground_truth.json`. These
counts describe a non-adaptive script and **must not be cited as security or utility results**.

## 6. Why it was not executed, and what is needed

1. **Credential:** no LLM API key in the environment (HTTP 401 from the Anthropic endpoint; other
   providers and model hosts blocked by the network policy).
2. **Design inputs (D-15):** backbone(s), decoding, repeats, frozen-parameter source, task cells,
   budget, authorisation, pre-registration.

Commands once both are resolved:

```bash
cp experiments/live/live_config_TEMPLATE.yaml experiments/live/live_config.yaml
#   replace every REQUIRED_FROM_DESIGN value with the recorded decision
python3 experiments/live/check_live_config.py experiments/live/live_config.yaml     # must exit 0
export ANTHROPIC_API_KEY=...        # or OPENAI_API_KEY / GOOGLE_API_KEY
PILOT_RESULTS_DIR=$PILOT_RESULTS_DIR AGENTDOJO_RUNS=/home/user/ethz-spylab/agentdojo/runs \
  python3 experiments/live/run_live.py --config experiments/live/live_config.yaml --out results/live_<date>
python3 experiments/live/analyze_live.py results/live_<date>/episodes.jsonl results/live_<date>/summary.json
```
