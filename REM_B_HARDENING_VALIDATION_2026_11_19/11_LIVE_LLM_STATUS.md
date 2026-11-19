# 11 Live LLM closed-loop experiment (Phase 9)

## Status: NOT EXECUTED

No language model was called in this study. "Scripted closed loop" results (`08`) come from AgentDojo's ground-truth test doubles. They are an implementation test of call orders, not a live experiment, and they are never called "live LLM".

## Why (checked 19 November 2026)

| Requirement | Status |
|---|---|
| Approved model endpoint | none. Local OpenAI-compatible server (127.0.0.1:8000) and Ollama (127.0.0.1:11434) are not running. No experiment API key is present; only the session's own infrastructure credentials exist, and they are not authorised for experiments. |
| Authorised spending cap | none ("Do not spend money using external APIs without explicit authorization") |
| Frozen design inputs | LLM backbones and number of repeats are listed as unresolved in the design lock (CLAUDE.md, data/evaluation lock) |

## Ready-to-run configuration (for when an endpoint and a budget are approved)

| Item | Value |
|---|---|
| Loop | user request → agent proposal → REM enforcement (`RemGuard` at AgentDojo's tool-execution boundary) → tool execution or refusal notice → agent continuation → final outcome |
| Code | `rem/integration/agentdojo_live.py` (live guard; fail-closed runner `experiments/live/run_live.py`); `experiments/progent_competitive/closed_loop.py` (REM arms and Progent manual / generated / update arms under one agent); guard factory `experiments/rem_b_hardening/remb2.py` (`factory2`). The system-of-record hook is the same environment-capture element as in replay (`replay_episode2`). |
| Suite | AgentDojo banking, installed 0.1.35. The exact version for the thesis is not frozen; supervisor confirmation needed. |
| Arms (minimum) | B0, C1, REM-B, REM-B2 (and REM-B2 without R3), PG, Progent with generated policies, Progent with Auto-Deny updates |
| Recorded per episode | actual model identifier and configuration, all tool-call proposals and defender decisions (audit record), retries and replans, final banking state, attack and benign outcomes, tokens, cost, latency |
| Volumes for budgeting | `REM_PROGENT_COMPETITIVE_2026_11_18/06_BUDGET_ESTIMATE.md` (measured trace volumes; prices to be entered by the operator) |
| Statistics | grouped by user task and injection task. Repeats of a task pairing are not independent observations. Counts, repeats and analysis frozen before the first call; spending guard (`budget.py`). |
| Banking environment | simulated only. No real account or banking API. |

## What the replay results cannot show
- **Adaptation.** A live agent sees REM's refusals and may retry, rephrase or replan. Retries can raise attack success, and re-reads can raise utility.
- **Model-specific value errors.** The audited violations depend on the agent model.
