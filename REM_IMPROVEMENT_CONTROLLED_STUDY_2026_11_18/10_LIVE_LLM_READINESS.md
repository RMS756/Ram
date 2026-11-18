# 10 Live LLM closed-loop readiness (Phase 9). NOT EXECUTED

## Three settings that must not be conflated

| Setting | What decides the next action | Status |
|---|---|---|
| Scripted closed loop | a test double replays AgentDojo's ground truth; it does not react to refusals | executed (`07` D) |
| Live LLM closed loop in a simulated bank (AgentDojo) | a language model reads REM's refusal or notice and chooses its next call | **not executed**: no endpoint |
| External banking sandbox | a real bank-like API | not prepared; out of scope (no real financial systems are used) |

An AgentDojo run, even with a live model, is a simulation. It is not deployment in a banking system.

## Endpoint check (this session; names only, no values printed)
- **No local model server.** Nothing serves on 127.0.0.1:8000 (the OpenAI-compatible route upstream Progent uses for `Qwen/` and `meta-llama/`), nothing on Ollama (127.0.0.1:11434), and there is no GPU.
- **No experimental credential.** No OpenAI key is present. The credentials that do exist belong to the session's infrastructure (cloud, GitHub, the coding assistant's own gateway). They are not authorised experimental endpoints and were not used.
- **No spending.** No paid call was made, and no spending cap has been authorised.

## Prepared and tested components
- **REM closed loop:** `rem/integration/agentdojo_live.py` (`run_defended_episode`). The agent's next turn sees REM's notice. It is tested with scripted reactive agents (`tests/test_live_integration.py`); the adaptation statistics are retry and replan.
- **Arms:** `experiments/improvement_controlled/arms.py` builds every arm of this study (A0–A7) for any episode.
- **Full-Progent comparison:** `experiments/progent_competitive/closed_loop.py`, with fail-closed preflight. It requires:
  - the pinned checkout;
  - separately declared agent and policy models;
  - a spending cap and an estimate for hosted models;
  - declared tasks and repeats;
  - no human-approval arm.
- **Faithful manual-policy arm.** Correction from `05a` amendment 2: in the 0d7ea07 fork the 9befb41 manual policy must be installed explicitly.
- **Budget:** `experiments/progent_competitive/budget.py` measures token volumes from the stored traces. Prices are entered from the official page.

## Loop to be run (per episode)
1. The user request.
2. The model proposes a call.
3. REM intercepts it (and, in Progent arms, the upstream check runs inside the tool).
4. The verdict.
5. The call executes, or is withheld with a notice.
6. The result or notice goes back to the model.
7. The model continues.
8. AgentDojo's utility and security evaluators run.

The structured trace is `LiveOutcome.messages` plus REM's audit record (argument digests, no secrets).

## Protocol placeholders (to be frozen before any run)
- **Design inputs (none decided here):** the model and decoding; repeats per task pair; the arms (minimum: B0, PG with the 9befb41 policy, C1, C1I, full Progent configurations).
- **Endpoints:** the same as `05`, plus adaptation counts. Clusters are tasks; repeats are not treated as independent.
- **Required before running:** an endpoint and, for a hosted model, an authorised cap. Credentials go into the environment's secret settings, never into chat or code.
