# Live Experiment: Code Audit (3 November 2026)

**Scope.** This audit covers what was inspected before the closed-loop integration was implemented: the installed AgentDojo APIs and the existing REM code.

**Environment.** AgentDojo 0.1.35 at `/usr/local/lib/python3.11/dist-packages/agentdojo`; Python 3.11.17.

## 1. AgentDojo: verified APIs

| Need | Verified API (file) | Finding |
|---|---|---|
| Pipeline composition | `AgentPipeline`, `SystemMessage`, `InitQuery`, `ToolsExecutionLoop` (`agent_pipeline/agent_pipeline.py`, `basic_elements.py`, `tool_execution.py`) | `ToolsExecutionLoop(elements, max_iters=15)` repeats `[executor, llm]` while the last assistant message contains tool calls |
| Tool execution point | `ToolsExecutor.query` (`tool_execution.py`, lines 46–115) | Tools run through `runtime.run_function(env, function, args)`. Interception is possible by replacing the executor element. **No AgentDojo source was modified** |
| Real LLM agents | `AnthropicLLM(client, model, temperature)`, `OpenAILLM(client, model, …)`, `GoogleLLM`, `CohereLLM`, `LocalLLM` (`agent_pipeline/llms/`) | Each provider element needs a provider credential |
| Banking suite | `get_suites("v1")["banking"]` | 16 user tasks, 9 injection tasks; `user_tasks`, `injection_tasks`, `tools` |
| Attacks | `load_attack(name, suite, target_pipeline)` (`attacks/attack_registry.py`) | `important_instructions` names the model, taken from `target_pipeline.name` (`get_model_name_from_pipeline`) |
| Episode execution and scoring | `TaskSuite.run_task_with_pipeline(pipeline, user_task, injection_task, injections, environment=None)` (`task_suite/task_suite.py`, lines 339–420) | Returns (utility, security). `security = True` means the injection goal was reached. The pipeline is **re-queried up to three times** if the agent produces no final text (interpretation L-1) |
| Default system prompt | `load_system_message(None)` (`agent_pipeline.py`, line 52) | Used by the runner |

## 2. REM: reused components (unchanged)

| Component | Location | Role in the live path |
|---|---|---|
| `RemGuard.evaluate` / `_mitigate` | `rem/integration/agentdojo_replay.py:131-264` | Features, frozen scoring, decision, mitigation (both semantics, both reviewer bounds), audit record, timers. Evaluated before execution |
| `GuardedToolsExecutor` | `agentdojo_replay.py:310-343` (returned by `_agentdojo_elements()`) | Replaces `ToolsExecutor`; executes only released calls |
| `FrozenScorer` | `agentdojo_replay.py:67-92` | s = β₀ + βᵀx; p = σ(γ₁s + γ₀) |
| `A3Policy`, `A1Policy`, predicates, loss grid | `rem/algorithms/a3.py`, `a1.py`, `decision/` | REM, REMnoEsc, B1 |
| Frozen fold parameters | pilot state `crossfit.pkl`, `rmod.pkl` (from `experiments/pilot/run_all.sh`) | No refit on live data |
| `build_policies` | `experiments/pilot/run_main.py:323-339` | The same per-fold policies as in the recorded-trace study |

## 3. Added code

| File | Purpose |
|---|---|
| `rem/integration/agentdojo_live.py` | `run_defended_episode` (real or scripted LLM element plus `GuardedToolsExecutor`); `live_episode_stub`; `adaptation_statistics` |
| `experiments/live/run_live.py` | Fail-closed runner (configuration, credentials, frozen fold) |
| `experiments/live/analyze_live.py` | Metrics with grouped bootstrap |
| `experiments/live/smoke_scripted.py` | Harness smoke test with a scripted ground-truth agent |
| `tests/test_live_integration.py` | 12 tests (see `LIVE_EXPERIMENT_TEST_REPORT.md`) |

No REM algorithm, parameter, configuration or existing result was changed. A `git diff` of `rem/algorithms`, `rem/core`, `rem/evaluation`, `rem/integration/agentdojo_replay.py`, `configs/` and `results/` is empty.

## 4. Missing components and specification conflicts

| Item | Status | Consequence |
|---|---|---|
| LLM credential | **Absent** (no `ANTHROPIC_API_KEY`, `OPENAI_API_KEY` or `GOOGLE_API_KEY`). `api.anthropic.com` answers 401; Hugging Face and Ollama are refused by the network policy | **The live experiment cannot be executed here** |
| Backbone, decoding, repeats, authorisation, budget, pre-registration | Undecided (D-15; CLAUDE.md data and evaluation lock) | The runner exits with code 2 until they are decided |
| Fitted-parameter source for live runs | Undecided. The pilot has nine fold fits and no full-data fit | The runner requires `fold:<id>`; no fold is chosen here |
| Injection classifier x^ctx^₁ | Absent (D-8) | The live path uses the same eight features as the pilot |
| Human reviewer | Absent (D-7) | Escalate is resolved by the two bounds only (idealised; no reviewer) |
| Mitigation semantics and tie rule | Unresolved (SC-1, SC-2) | Both semantics are run if configured; ties are counted (Chapter 3 order applied) |
| Suite version | Undecided (D-6). The recorded traces span several versions; labels use v1 references | Configuration value `suite_version` |
| Label rule for live runs | The reference match of the pilot (`reference_match_pilot_e0`) is the only implemented rule | The human audit is still pending |
