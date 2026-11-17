# Closed-loop comparison with the complete Progent framework (protocol; NOT EXECUTED)

Status: `[PROPOSED - EXPLORATORY]`. Harness: `experiments/progent_competitive/closed_loop.py`. Upstream adapter: `progent_upstream.py`.

## Why it was not run in this session
1. **No model backend.** Model hosts were refused by the session's network: ollama.com, registry.ollama.ai, huggingface.co (connect_rejected); platform.openai.com did not resolve.
2. **No spending authorisation.** There is no credential and no approved paid-model cap. The 18 November prompt states that it supplies no paid-model spending cap.
3. **Upstream execution refused.** The session's safety classifier refused execution of the upstream Progent code (even locally, in an isolated venv). That code is therefore implemented and tested only up to the import boundary. Parity of REM's replay checker with upstream `check_tool_call` is gated behind `REM_ALLOW_UPSTREAM_EXECUTION=1`.

## Roles (recorded separately)

| Role | In this study |
|---|---|
| coding assistant | wrote the code and documents; not part of any arm |
| experimental agent model | to be declared (AgentDojo `--model`); the same for every arm |
| policy-generation model | to be declared (`SECAGENT_POLICY_MODEL`); the same for every P0/C2[gen] arm |
| risk estimator | stored ridge F4 + Platt (C3 only); no model call |

## Arms (all inside Progent's AgentDojo fork at 0d7ea07, banking suite)

| Arm | Boundary |
|---|---|
| P0_manual | upstream engine with the fork's manual banking policy ("PG historical"; the policy at 0d7ea07, which should be diffed against 9befb41 before the run) |
| P0_generated | upstream: policy generated once from the user query; no update |
| P0_update_autodeny | upstream: generated + updated after each tool batch; an update is kept only if the z3 subset check proves it narrower |
| P0_update_autoapprove | upstream: generated + updated; every update accepted (the published `run.sh` setting) |
| C1 | REM contract guard only; fork tools not wrapped (`SECAGENT_SUITE` unset) |
| C2gen_<P0 config> | REM contract guard first, then the upstream engine inside the tool |
| C3gen_<P0 config> | C2gen + stored learner |
| human approval | **not run**: no reviewer exists |

## Matching

All arms use the same:
- tasks: 16 user tasks × 9 injection tasks with the `important_instructions` attack, plus the 16 benign tasks;
- agent model, decoding and seed policy;
- number of repeats.

The arm order is randomised per repeat. One process per arm configuration, because upstream keeps module-level policy state.

## Outcomes

- **Core measures:** utility under attack, benign utility and attack success (AgentDojo's own evaluators), plus REM's audit.
- **Progent policy logs:** generated policies, updates accepted and updates rejected.
- **Adaptation counts:** retry and replan, as in `rem/integration/agentdojo_live.py`.
- **Paired episode-level contrasts:** C2gen−P0 for the same config, C1−P0_*, and C3gen−C2gen.
- **Independence.** Repeats of the same task pair are **not** independent observations. Intervals are grouped by user task.

## Implementation test available without a model
AgentDojo's `GroundTruthPipeline` can drive the fork with the reference solutions of the user tasks. Paired with P0_manual and C1, it checks the wiring, but only once upstream execution is permitted. It is not a security result.

## Preflight (fail-closed, enforced by `closed_loop.preflight`)
The run does not start without all of the following:
- the pinned checkout, clean;
- both models declared;
- for any hosted model, an operator-declared cap and a `budget.py` estimate below it;
- tasks, attack and repeats;
- no human-approval arm.

## Concrete next action for the user
Either:
- **Locally (no spending):** run a local OpenAI-compatible server at 127.0.0.1:8000/v1 with a `Qwen/` or `meta-llama/` model. Upstream routes these names there; see the earlier Ollama pilot guide on branch `codex/rem-ollama-pilot`.
- **Hosted:** provide an approved spending cap and credentials through the environment's secret settings (never in chat).

Then run the gated parity test, followed by the arms above.
