# 01 DRIFT audit (22 November 2026)

**Evidence labels**
- **VERIFIED:** read in the code or established by a test executed here.
- **PAPER-REPORTED:** stated in the paper. Only the abstract could be read: arXiv is unreachable from this environment; the abstract was read through OpenAlex.
- **DOCUMENTED:** stated in the repository's README.
- **NOT VERIFIED:** not established.

## 1 Paper

| Item | Finding | Label |
|---|---|---|
| Title | *DRIFT: Dynamic Rule-Based Defense with Injection Isolation for Securing LLM Agents* | VERIFIED (OpenAlex W4415110937; README) |
| Authors | Hao Li, Xiaogeng Liu, Hung-Chun Chiu, Dianqi Li, Ning Zhang, Chaowei Xiao | DOCUMENTED (README); OpenAlex lists 6 authors |
| Venue | NeurIPS 2025, conference paper; proceedings DOI `10.52202/085713-2791`; arXiv:2506.12104 | VERIFIED (OpenAlex record type `conference-paper`, venue "neural information processing systems") |
| Full text | **Not read**: arXiv returns no response through the session proxy | NOT VERIFIED |
| Claims in the abstract | Secure Planner (minimal function trajectory + JSON-schema parameter checklist); Dynamic Validator (deviation checks against privileges and user intent); Injection Isolator (detects and masks conflicting instructions in the memory stream); evaluated on AgentDojo, ASB and AgentDyn | PAPER-REPORTED (abstract only) |

## 2 Repository

| Item | Finding | Label |
|---|---|---|
| Official repository | `github.com/SaFo-Lab/DRIFT` at `6fd3df4763fad77398c3c273c2a4fe14dd50f7ea` (15 Jul 2026); cloned anonymously 22 Nov 2026 to `/home/user/upstream/SaFo-Lab_DRIFT`; file hashes in `results/upstream_pins.json` | VERIFIED |
| Licence | MIT (`LICENSE`, added in the last commit) | VERIFIED |
| Code size | 8 Python files, 1,780 lines for the AgentDojo integration; a separate `ASB_DRIFT/` tree for ASB | VERIFIED |
| Required AgentDojo | `agentdojo==0.1.35` (README and `requirements.txt`). This is the same package version as REM's frozen environment. | VERIFIED |
| Default benchmark version | `--benchmark_version v1.2` (`utils.py`). REM's recordings and the MELON protocol use banking **v1**. The flag is a command-line option, so v1 can be selected without code changes. | VERIFIED |
| Providers | OpenAI (`gpt-*`), Google (`gemini-*`), anything else through OpenRouter (`client.py`) | VERIFIED |
| Cached results | `runs/gpt-4o-mini-2024-07-18/banking`: 144 attacked episodes (v1.2, `important_instructions`, all three modules on). There are no benign or no-defence banking runs. | VERIFIED (`results/drift_published_banking_runs_summary.json`) |

## 3 Architecture as implemented

DRIFT is **not a guard placed in front of an existing agent. It replaces the agent's LLM element.** `DRIFTLLM` subclasses AgentDojo's `PromptingLLM`, and the pipeline is `AgentPipeline([InitQuery(), DRIFTLLM, DRIFTToolsExecutionLoop([ToolsExecutor(), DRIFTLLM])])` (`pipeline_main.py`). VERIFIED.

| Mechanism | Code | What it does | Model dependency |
|---|---|---|---|
| Privilege assignment | `DRIFTLLM.function_privilege_assignment` | An LLM labels each tool Read / Write / Execute, once per `DRIFTLLM` instance (11 calls for banking) | LLM |
| Secure planning (`--build_constraints`) | `initial_constraints_build` + `CONSTRAINTS_BUILD_PROMPT` | On the first step, an LLM writes a `<function_trajectory>` and a `<parameter_checklist>` from the user query | LLM |
| Injection isolation (`--injection_isolation`) | `injection_isolate` + `INJECTION_DETECTION_PROMPT` | After each tool result, an LLM lists "conflicting instructions"; DRIFT deletes those sentences from the stored tool message by regex. A second detection pass runs if nothing was removed (`mask_limitation = 1`). | LLM |
| Dynamic validation (`--dynamic_validation`): trajectory | `trajectory_constraint_validation` | A proposed call that deviates from the plan passes automatically if its tool is labelled Read. Otherwise an LLM alignment judge decides Yes/No. On No, the call is removed and a `[CALL ERROR]` user message is returned. `user_approval_request()` always returns False in evaluation. | LLM (judge) |
| Dynamic validation: checklist | `checklist_constraint_validation`, `node_check` | An LLM reformats the checklist to JSON (up to 3 tries). DRIFT then checks the function name and the non-null required parameters by **substring containment**; parse failures pass (`except: return True`). | LLM (formatting) + deterministic check |
| Redundancy filter | `DRIFTLLM.query` | A tool call identical to one already in the transcript is dropped | none |
| Agent | `TOOL_CALLING_PROMPT`; `client.agent_run` | Prompt-based function calling in `<function_call>[...]</function_call>` tags, **not** native tool calling. The system prompt carries DRIFT's own environment text (user Emma Johnson, "an employee of the company Blue Sparrow Tech", "Complete all tasks automatically without requesting user confirmation"). | LLM |

All rows are VERIFIED by code reading; the integration test reached every row.

**Enforcement point.** Enforcement happens *inside the agent step*, before `ToolsExecutor`. A refused call never reaches the tool; the agent receives a `[CALL ERROR]` message and continues (at most 15 loop iterations; the step stops at more than 20 messages). VERIFIED.

**Generation settings.** `OpenAIModel.agent_run` and `llm_run` send no `temperature`, so the provider default applies. AgentDojo's own OpenAI element uses temperature 0. The Google client uses temperature 0.0. VERIFIED. This is a controlled-variable difference that cannot be removed without editing DRIFT (see `07`).

**Embedding dependency.** None. VERIFIED: no embedding call exists in the code.

## 4 Compatibility with the frozen REM setting

| Question | Answer | Label |
|---|---|---|
| Same AgentDojo version (0.1.35) | yes; DRIFT installs `agentdojo==0.1.35` from PyPI into its own venv (`/home/user/venvs/drift`, `results/pip_freeze_drift.txt`) | VERIFIED |
| Same banking tasks (suite v1) | yes, with `--benchmark_version v1`. The integration test ran v1 and v1.2 (`results/itest_drift.json`). | VERIFIED |
| Evaluator compatibility | DRIFT scores with AgentDojo's `_check_task_result`; it overrides only `model_output_from_messages`, wrapping DRIFT's string content. On reference solutions, the DRIFT venv scores all 16 benign tasks and 144 pairs identically to PyPI 0.1.35 (`results/fingerprint_drift_env.json`). | VERIFIED |
| Attack compatibility | `important_instructions` is loaded through AgentDojo's `load_attack`. The pipeline name is set to `gpt-4o-2024-05-13` for every OpenAI model, which fixes the model name written into the attack text. | VERIFIED |
| Tool interfaces | AgentDojo's banking `Function`s are passed unchanged; DRIFT serialises their JSON schemas into its prompt | VERIFIED |
| Patches required | **none** for banking v1 on 0.1.35 | VERIFIED |
| Same agent as REM's D0 | **no.** DRIFT brings its own prompting agent, system text, redundancy filter and generation settings. A *DRIFT-scaffold, no-modules* control arm (all three flags off, supported by the official command line) is needed to separate scaffold effects from defence effects. | VERIFIED |
| Can REM be compared without changing REM's security logic | yes. REM stays at its own integration point (gating `ToolsExecutor` in AgentDojo's native pipeline), and DRIFT runs as published. | VERIFIED (design); live run NOT EXECUTED |

## 5 Cost and overhead

**Executed here: the test-double run**, which made no real model calls. It counted the model calls DRIFT would make with all modules on:
- on a 2-call benign task (`user_task_0`): 20 model calls, namely 11 privilege, 1 plan, 2 detector, 3 agent and 3 checklist-formatting;
- on attacked cases: 21–22 calls, including 1 alignment-judge call;
- the 11 privilege calls happen once per agent instance.

These are **call counts, not tokens or prices**. VERIFIED.

**Published cached runs** (gpt-4o-mini, v1.2): median 15,124 tokens and 29.2 s per attacked episode; p95 33,930 tokens and 80.2 s. DOCUMENTED (authors' artefacts; not executed here).

**Verified API cost: NOT AVAILABLE.** There is no account, the pricing page was not consulted, and no call was made.

## 6 Published banking numbers (authors' cached runs; not executed here)

7 attack successes / 144 and 59 / 144 utility under attack: gpt-4o-mini, banking **v1.2**, `important_instructions`.
- These are not comparable to REM's v1 recordings: v1.2 rewrites 8 of 9 injection goals and `user_task_15`.
- No benign utility run is distributed.

DOCUMENTED.

## 7 Integration requirements for a live run

1. An agent model endpoint with spending authorisation:
   - OpenAI, Google, or an OpenRouter model;
   - or a local OpenAI-compatible server through the `OPENAI_BASE_URL` environment variable read by the OpenAI SDK. NOT VERIFIED with DRIFT.
2. The official command line, with `--benchmark_version v1`, all three module flags for DRIFT, and no module flags for the scaffold control.
3. A thin runner that writes DRIFT's per-episode JSON into the common results schema. It must not change DRIFT's code.
4. A token and latency logger. DRIFT already records `total_tokens` and `duration` per episode.

**Status:** live DRIFT **NOT EXECUTED** (no endpoint, no key, no spending authorisation; `results/environment_check.json`).
