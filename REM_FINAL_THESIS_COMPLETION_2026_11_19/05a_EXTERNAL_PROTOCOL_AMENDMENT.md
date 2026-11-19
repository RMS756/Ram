# 05a Amendment to the external comparison protocol (19 November 2026, after the first run crashed and before any outcome was read)

## What happened

1. The first execution of `external_run.py` (commit `dc8407d`) stopped with an `IndexError` while computing the latency percentile.
   - **Cause:** the replay of the `tool_filter` traces (D3) produced an empty list of REM-evaluated calls.
   - **Seen before the crash:** only the number of eligible episodes per set (D0 149, D1 151, D2 151, D3 66, D4 154 of 159) and the number of replayed calls. No ASR, utility or contrast was computed or read.
2. Diagnosis: **the frozen replay harness cannot replay D3 traces.**
   - The harness (`rem/integration/agentdojo_replay.py`, `ReplayLLM`) feeds back the recorded assistant messages in order.
   - In a `tool_filter` trace, the first assistant message is the **tool filter's own output** (e.g. `read_file,send_money`), which has no tool call. AgentDojo's loop therefore ends at once.
   - So every one of the 159 D3 replays has zero tool calls: 0 calls in all 159, not just the 66 "eligible".
   - The 66 that pass the AM-4 outcome check pass only because the recorded run happened to end with the same utility and security values. They are not faithful reproductions.

## Amendment

| # | Change | Why |
|---|---|---|
| E1 | The layered replay "D3 tool_filter + REM v1.0" is **not reported**; its status is `NOT REPLAYABLE WITH THE FROZEN HARNESS`. The runner checks the condition and records it: zero REM-evaluated calls across all D3 replays. | A replay with no tool calls does not evaluate REM. The frozen harness is not modified, because it is part of REM v1.0's evaluation code. |
| E2 | A replay set whose eligible episodes contain no evaluated call reports latency as `null` instead of crashing. | The crash fix. It changes no metric definition. |

## What is unaffected

- The D3 **recorded** closed-loop outcomes (read from the run files).
- The descriptive cross-kind contrast "REM replay on undefended traces − D3 recorded", which uses D0 replays and is unaffected by D3 replays.

## Not done

Building a D3-specific replay adapter that skips the filter message would be a new, post-hoc evaluation procedure. It is not done here.
