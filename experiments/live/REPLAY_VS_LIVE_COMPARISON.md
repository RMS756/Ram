# Replay vs Live: Comparison

**No comparison of results is possible:** no live result exists (`LIVE_EXPERIMENT_RESULTS.md`). This file records how the two designs differ, so that a future comparison is interpreted correctly.

| Aspect | Recorded-trace replay (results in Ch. 4) | Live closed loop (implemented, not run) |
|---|---|---|
| Agent | Recorded assistant messages, replayed in order (`ReplayLLM`) | A provider LLM element generating each turn |
| Reaction to refusals | None: the next recorded message is replayed (NO-ADAPT) | The agent sees the "REM:" refusal and may retry, replan or stop |
| What ASR measures | Whether the recorded attack calls would have been withheld | Whether the attack succeeds despite the agent's adaptation |
| r_mod, residual success after Modify | ≈ 0 by construction (step-level Modify withholds the call; residual comes only from unlabelled routes) | Observable: retries and alternative tools can reach the goal |
| Stochasticity | Deterministic; bit-identical re-runs | Stochastic; needs repeats |
| Backbones | 21 historical recorded backbones | Undecided (D-15) |
| Suite version | Labels from v1 references; traces from several versions | A single declared version |
| Cost | No API cost | Paid API calls |

**Reporting rule.** Replay ASR and live ASR are different estimands and must be reported in separate tables. A live ASR higher than the replay ASR would be expected wherever agents adapt; it would not by itself be evidence of a defect in either analysis.
