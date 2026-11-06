# Experiment Readiness (5 Nov 2026)

| Configuration (supervisors' design) | Mode A: recorded traces | Mode B: live LLM agent in AgentDojo banking |
|---|---|---|
| No Defense | **Executed** (replay + deployment simulation) | Ready (`experiments/live/run_live.py`, B0); **not executed** |
| MELON | **Not possible.** MELON re-queries the agent's LLM (masked re-execution) and calls OpenAI embeddings; recorded traces cannot supply these | Ready (`experiments/melon_rem/run_melon_rem.py`, AgentDojo 0.1.29, upstream code unmodified); **not executed** |
| REM-Lite | **Executed** (offline held-out, replay, deployment simulation) | Needs one addition: REM-Lite as a policy option in the live and MELON runners (the policy object exists in `experiments/rem_lite/run_rem_lite.py`); **not executed** |
| Full REM | **Executed** | Ready; **not executed** |

## Blockers for Mode B

1. **Credentials:** no `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` in the environment.
2. **Network:** the environment's network policy denies `api.openai.com`. Even with a key, MELON's embedding calls and an OpenAI backbone cannot run here. Allow the host in the environment's network settings (https://code.claude.com/docs/en/cloud-environments#network-access).
3. **Spending authorisation and cap:** none exists. The runners refuse to make paid calls without one.
4. **Design inputs:** backbone and exact model id, decoding, repeats, timeout and retry policy, run order seed, REM fitted-parameter source (D-15, M-1 to M-3).
5. **Version matching:** MELON requires AgentDojo 0.1.29, so a matched four-way live comparison should run every configuration on 0.1.29. The banking v1 task and attack code are identical to 0.1.35, apart from one default injection-vector string.

## What was verified locally (no paid calls)

| Check | Result |
|---|---|
| MELON integration (scripted agents, fake embeddings, fake provider) | 30/30 tests pass |
| Live REM harness | 12 tests pass |
| Deployment gateway | 6 tests pass |
| REM-Lite | 2 unit tests pass, plus the real-data equivalence check |
| Full suite (main environment) | 233 pass |
