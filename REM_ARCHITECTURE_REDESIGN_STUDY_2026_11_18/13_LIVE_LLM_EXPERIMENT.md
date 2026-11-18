# 13 Live LLM experiment (Phase 10)

## Status: NOT EXECUTED

No language model was called in this study. Every result in `09`–`12` is an offline replay of recorded agent traces (NO-ADAPT), an author-written suite, or the scripted closed loop with AgentDojo's ground-truth doubles (scripted agents, not models).

## Blockers (checked 18 November 2026)

| Requirement | Status |
|---|---|
| Local OpenAI-compatible endpoint (127.0.0.1:8000, used by Progent for `meta-llama/` and `Qwen/` names) | not running (connection refused) |
| Local Ollama (127.0.0.1:11434) | not running |
| An experiment API key explicitly provided for this research, with an **authorised spending cap** | none. Only the session's own infrastructure credentials exist in the container. They are not authorised for experiments, and using them would breach the standing rule "Do not use paid APIs without authorization". Values were not printed. |
| Approved backbone list, decoding, number of repeats | not frozen (CLAUDE.md data/evaluation lock: "LLM backbones", "number of repeats" unresolved) |

**This blocker is a decision, not a technical fault.** Under the design lock it requires a **supervisor decision**: backbones, repeats, and a budget.

## What is ready to run (implemented and tested with scripted agents only)

| Component | Path | State |
|---|---|---|
| Live REM guard at AgentDojo's tool-execution boundary | `rem/integration/agentdojo_live.py` | tested with scripted agents; refuses to start while any design input is undecided (`experiments/live/run_live.py`) |
| Closed-loop harness for REM arms and Progent (manual / generated / update) | `experiments/progent_competitive/closed_loop.py` | fail-closed; needs an endpoint and a cap |
| Volumes per arm for budgeting | `REM_PROGENT_COMPETITIVE_2026_11_18/06_BUDGET_ESTIMATE.md` | measured volumes; prices to be entered by the operator |
| REM-B as a guard factory | `experiments/architecture_redesign/rem_arch.py` (`factory`) | the same object used in replay |

## Why the replay results do not substitute for a live run
- **Replay cannot adapt.** A recorded agent does not see REM's refusal. A live agent may retry, replan or stop.
  - Retries could raise attack success (an attacker's call rephrased after a refusal).
  - Retries could also raise utility (the agent re-reads the full transaction history, which would let E2h find the known counterparty).
- **Agent-error amounts differ by model.** The audited violations depend on them.
- The scripted closed loop tests **implementation correctness** under call orders. It does not measure the attack success rate of a real model.

## Minimum protocol if authorised (proposal; not frozen)

- **Arms:**
  - B0 (no guard);
  - C1;
  - REM-B;
  - PG (manual, 9befb41 policy installed);
  - P0_generated / P0_update_autodeny (full Progent), on the same backbone.
- **Suite:** AgentDojo banking, the version pinned in the repository (0.1.35). This is not frozen in the thesis specification; supervisor confirmation is needed.
- **Endpoints:** attack success, benign utility, utility under attack, audited violations, retries and replans (counted from the audit record).
- **Statistics:** the same grouped bootstrap. Repeats of a task pairing are **not** independent observations; they are clustered by user task and injection task.
- **Freezing:** counts, repeats and the analysis are frozen before the first call, and a spending guard is applied (`budget.py`).
