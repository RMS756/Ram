# 03 DRIFT (D3) and the DRIFT-agent control (D4): implementation and results

**Kinds of evidence here.**
- E-STAT: static code observations.
- E-SCR: scripted integration.
- **No live DRIFT run exists, and no DRIFT security or utility result exists in this phase.**

## 1 Source and compatibility (E-STAT; integration tests VERIFIED by execution)

| Item | Finding |
|---|---|
| Repository | `github.com/SaFo-Lab/DRIFT` at `6fd3df4763fad77398c3c273c2a4fe14dd50f7ea`, MIT licence. Paper: NeurIPS 2025, DOI `10.52202/085713-2791`. |
| AgentDojo | `agentdojo==0.1.35` is DRIFT's own requirement, the same as REM's. It installs cleanly in `/home/user/venvs/drift`. |
| Banking v1 | `--benchmark_version v1` (DRIFT's default is v1.2). It runs with **no code modification**. |
| Compatibility modifications made | **none.** DRIFT is imported by path from the pinned checkout, which keeps a clean `git status`. |
| Evaluator | AgentDojo's `_check_task_result`. Banking scoring in DRIFT's environment is identical to PyPI 0.1.35 on reference solutions (audit fingerprint). |

## 2 What DRIFT changes in the agent (E-STAT)

| Element | D0/D1/D2 (AgentDojo native) | D3/D4 (DRIFT agent) |
|---|---|---|
| Tool calling | the provider's native tool calls | text `<function_call>[...]</function_call>`, parsed by AgentDojo's AST helper |
| System prompt | AgentDojo default (sha256 `a021a92b…`) | DRIFT's `TOOL_CALLING_PROMPT`, plus the tool list in the prompt, plus `ENVIRONMENT_GUIDELINES`. These contain the same Emma Johnson / Blue Sparrow Tech lines and add "Complete all tasks automatically without requesting user confirmation". |
| Decoding | as configured (temperature in AgentDojo's OpenAI element) | DRIFT's OpenAI client sends **no** temperature |
| Loop | `ToolsExecutionLoop`, 15 iterations | `DRIFTToolsExecutionLoop`, 15 iterations; the step stops above 20 messages |
| Redundant-call filter | none | it drops a call identical to an earlier one in the transcript |
| Episode retries | AgentDojo's (up to 3 when no final text) | DRIFT's own `run_task_with_pipeline` (up to 3) |

**Because of these differences, D4 is required, and D3 − D4 is the only valid estimate of DRIFT's modules.** D1 vs D3 compares two complete systems, agent included.

## 3 DRIFT's extra processing (E-STAT; counts from E-SCR)

**Modules** (with all flags on):
1. **Privilege assignment:** 11 LLM calls, once per `DRIFTLLM` instance. In the authors' command line, that is once per suite run.
2. **Plan and checklist:** 1 call per episode.
3. **Injection detector:** 1–2 calls per tool result.
4. **Agent:** 1 call per step.
5. **Checklist JSON formatting:** 1–3 calls per step.
6. **Alignment judge:** 1 call per deviating call that is not Read-only.

**Scripted integration on all 160 v1 episodes** (O5, `results/drift_scripted_integration.json`). The test-double client answers every sub-prompt; **its utility and security values are set by the script and are not results.**

| Arm and script setting | Episodes | Errors | Tool calls executed | DRIFT refusals | Model calls DRIFT made (total) | Per episode |
|---|---|---|---|---|---|---|
| D3, S1: detector finds nothing, judge says No | 160 | 0 | 330 | 77 | privilege 1,760 · plan 160 · detector 330 · agent 567 · checklist 490 · judge 77 | 21.15 |
| D3, S2: detector echoes the injected goal, judge says Yes | 160 | 0 | 330 | 0 | privilege 1,760 · plan 160 · detector 330 · agent 490 · checklist 490 · judge 0 | 20.19 |
| D4: no modules | 160 | 0 | 396 | 0 | agent 556 | 3.48 |

**Note on the privilege count.** This harness builds a new `DRIFTLLM` per episode, so privilege assignment appears 11 times per episode. Under the authors' command line it would be 11 per run. Excluding it, D3 makes about **9–10 model calls per episode against 3.5 for D4** in this script. Real counts depend on the model.

**What the scripted run shows.** The official code runs end to end on every v1 episode, every module path is reached, and AgentDojo scores the outputs. It shows nothing about protection.

## 4 Published numbers (not comparable)

The authors' cached banking runs are gpt-4o-mini on **v1.2**: 7/144 attack successes, 59/144 utility under attack, and no benign or no-defence runs. They are not comparable with v1 results and are not used.

## 5 Live execution path (prepared, fail-closed, not executed)

- **Runner:** `run_drift_arms.py --mode live` runs the authors' `pipeline_main.py` in a fresh `git archive` of the pin, once per repeat.
  - D3 uses the three module flags.
  - D4 uses none.
  - Both run with and without `--do_attack --attack_type important_instructions`, with `--benchmark_version v1`.
- **Refusals (exit codes):**
  - 2 without model, repeats, authorisation, provider-side hard cap or protocol-freeze commit;
  - 3 without the credential;
  - 4 if the checkout is not at the pin.
- **Spending control.** DRIFT's client cannot be wrapped by REM's spending guard without editing DRIFT, so a **provider-side hard cap** is required.
