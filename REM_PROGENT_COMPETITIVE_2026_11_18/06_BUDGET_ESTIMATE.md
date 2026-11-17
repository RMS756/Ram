# Budget estimate for the closed-loop comparison (volumes measured; prices not available in this session)

Status: ESTIMATE, not a measured cost.
- Tool: `experiments/progent_competitive/budget.py`.
- Output: `results/budget_volumes.json`.
- Command: `python3 budget.py --runs <agentdojo runs> --pipeline gpt-4o-2024-05-13 --upstream <progent checkout> [--prices prices.json]`.

**Why no dollar figure.** The official pricing page (platform.openai.com) could not be reached from this session. The study does not use remembered or guessed prices. The operator copies the prices into `prices_TEMPLATE.json` (with URL and date) and re-runs the tool, which then computes the cost.

## Measured volumes (per arm, one repeat = 160 episodes: 144 attacked + 16 benign)

**Trace-length proxy.** 1,536 stored banking runs of `gpt-4o-2024-05-13`. Per episode these average:
- 3.37 assistant turns;
- 21,518 input characters (each turn re-sends the conversation plus the 4,854-character tool schemas);
- 611 output characters;
- 2.57 tool results.

**Policy prompts.** Resolved statically from the upstream constants at 0d7ea07:
- generation: 3,056 characters;
- update decision: 2,045 characters;
- update: 4,322 characters.

Tokens use 4 and 3 characters per token (approximation; no tokenizer offline):

| Arm | agent input tokens | agent output tokens | policy input tokens | policy calls |
|---|---|---|---|---|
| P0_manual, C1 | 0.86 M – 1.15 M | 24 k – 33 k | 0 | 0 |
| P0_generated, C2gen_P0_generated | 0.86 M – 1.15 M | 24 k – 33 k | 0.32 M – 0.43 M | 160 |
| P0_update_autodeny / _autoapprove, and their C2gen | 0.86 M – 1.15 M | 24 k – 33 k | 2.07 M – 2.75 M (upper bound: every update decision says yes) | 981 |

**Total for the 8 arms of `budget.py`'s default list, one repeat:**
- agent input about 6.9 M – 9.2 M tokens;
- policy input about 9.0 M – 12.0 M tokens;
- policy output tokens not measurable offline. They must be declared, for example from a pilot of a few episodes.

Multiply by the number of repeats. C3gen arms add their agent volume again.

## Caveats
- Refusals change the trajectories (agents retry or replan), so real volumes can be higher than the replay proxy.
- The proxy model's verbosity differs from that of the chosen agent model.
- A local backend (Qwen/Llama through 127.0.0.1:8000) has no token price; its cost is compute time.
