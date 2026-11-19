# 05 External defence comparison protocol (19 November 2026). Committed before any arm of this comparison was scored

## Benchmark and baselines (verified on 19 November 2026)

| Item | Value |
|---|---|
| Environment | AgentDojo 0.1.35, installed package, banking suite v1 (16 user tasks, 9 injection tasks). **The Progent fork is not used.** |
| Recorded runs | `ethz-spylab/agentdojo` repository, commit `089ed468`, `runs/<pipeline>/banking/` |
| Model of the recorded runs | gpt-4o-2024-05-13 (the only model with all four defences recorded) |
| Attack | `important_instructions`: 144 (user task, injection task) pairs per pipeline. Benign runs (`none`): the 16 user tasks. |

**Baselines:**

| Code | Defence | Integration point |
|---|---|---|
| D0 | No defence | – |
| D1 | `repeat_user_prompt` | the user prompt is repeated after every tool result |
| D2 | `spotlighting_with_delimiting` | tool outputs are wrapped in delimiters, with a system-prompt instruction to ignore instructions inside them |
| D3 | `tool_filter` | an LLM pre-selects the tools allowed for the task before execution |
| D4 | `transformers_pi_detector` | a classifier flags tool outputs as injections and stops the run |

**Recorded completeness:** 144 attacked and 16 benign runs per pipeline, 0 errors (checked from the run files). These are the defences AgentDojo distributes. Their source is the installed `agentdojo` package (`agent_pipeline`). They are named exactly as there, and nothing is substituted.

## Two kinds of evidence (never pooled)

| Kind | What | Agent sees the defence? |
|---|---|---|
| **Recorded closed loop** (D0–D4) | Outcomes of AgentDojo's own runs with a real model, read from the run files; nothing re-executed | yes |
| **Offline replay of REM v1.0** (NO-ADAPT) | The frozen REM v1.0 (A0 configuration, cross-fitted fold models of the fresh pilot run) replayed on (a) the D0 traces and (b) each defence's traces (defence + REM, layered) | no: the recorded agent never sees REM's refusals |

**No live model is called in this study:** there is no endpoint and no authorised budget (`16`). REM v1.0 was therefore **not** run in a closed loop with gpt-4o.

## Eligibility

- **Replays:** an episode is kept iff the replay without REM reproduces the recorded utility and security without error (AM-4).
- **Recorded outcomes:** all non-errored runs.

## Metrics

**Per arm:**
- ASR (successes / attacked runs);
- tasks completed under attack;
- benign utility (/16);
- ASR by injection task;
- REM decision latency (replay).

**Intervals:** grouped bootstrap of the pilot configuration. ASR is clustered by injection task; utility by user task.

**Paired contrasts:**
1. Within the replay kind: REM-replayed − not-REM-replayed on the same traces, for D0 and for each defence. This contrast is causal for REM under NO-ADAPT.
2. Across kinds, on identical (user, injection) pairs: REM on undefended traces (replay) − each defence (recorded closed loop). **Descriptive only.** Its evaluation modes differ: the defence's agent adapted, REM's did not.

## Interpretation rules (fixed now)

- **No claim "REM outperforms defence X"** may be made from contrast 2, whatever its interval. It may be described as "on the same task pairs, REM's replayed decisions left fewer / more attack successes than the defence's recorded closed-loop run".
- **Contrast 1** supports "adding REM to defence X removes (or does not remove) attack successes on its recorded traces, under NO-ADAPT".
- **Benign utility on 16 runs** is reported with its interval, and is not the basis of any claim.

## MELON (optional baseline)

- MELON is run only if its official implementation can be executed under equivalent conditions. This needs a model endpoint and an embedding model.
- Otherwise it is NOT EXECUTED, with a feasibility report (`08`).
- Published MELON numbers are never placed in a table as if measured here.

## Command

```
PILOT_RESULTS_DIR=<fresh state> python3 experiments/final_thesis/external_run.py
```
