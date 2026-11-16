# Progent with generated and updated policies: what would be run, and why it was not

**Status: NOT RUN.** No model credential is available in this session and no spending limit has been approved. Nothing below is a result. Scripted responses were not substituted for a model.

## 1. Three Progent settings, kept apart

| Setting | What it is | Status in this project |
|---|---|---|
| PG | The hand-written banking policy of repository commit `9befb41` (five permitted recipients; no entry for `update_password`), applied to recorded calls by this project's replay code | **Executed** (replay; development evidence). Not a configuration of paper v3 |
| Progent, generated initial policy, updates disabled ("Disable Update") | Policy written by the policy model from the query; fixed afterwards | Not run: needs a model |
| Progent, generated and updated policies with an approver ("Auto-Deny", "Auto-Approve", "Manual Approval") | The paper's default is Auto-Approve with gpt-4o as agent and policy model | Not run: needs a model; Manual Approval also needs a human |

## 2. Why a replay of the full framework is not possible

The framework changes the policy after each tool result by calling a model, and returns a message to the agent after a refusal so that the agent continues differently (paper, pp. 5-7). A recorded trajectory contains neither the policy model's outputs nor the agent's reaction to those messages. Only the static manual policy can be applied to recordings.

## 3. Matched live comparison (to be preregistered before any run)

- **Benchmark.** One AgentDojo version for every condition. The Progent repository bundles 0.1.29; REM's recordings are 0.1.35. A live comparison must fix one of them for all arms and state it.
- **Population.** Banking suite: 16 user tasks without attack, and 16 x 9 = 144 task pairs under the `important_instructions` attack, per agent model and per repeat.
- **Agent model and policy model.** The paper's default: `gpt-4o-2024-08-06` for both. The same agent model for every arm.
- **Arms.** No defense; Progent Auto-Approve (paper default); Progent Auto-Deny; Progent Disable Update; REM v1.0; HV; the arm named in `10_FINAL_DECISION_TABLE.md`; and a matched control that gives Progent the same financial constraints as a generic policy, to separate the effect of the constraints from the effect of a learner.
- **Information allowed.** Every arm sees the user's query and the tool results only. No arm sees task identifiers or labels.
- **Reviewer.** None for any arm (Auto-Approve and Auto-Deny are automatic; REM's Escalate withholds), or the same human protocol for all.
- **Budget.** The same `max_steps` and the same number of retries after a refusal for every arm. REM arms must return a refusal message to the agent, as Progent does; this needs REM's closed-loop harness (`experiments/live/`), which is implemented and was verified with scripted agents only.
- **Repeats.** At least 3 per condition, declared in advance; repeats of one task pair are not independent observations.

## 4. Launch commands (from the repository's README, for the paper's configuration)

To be run by a person with credentials, in an isolated environment, after the protocol is frozen. The repository's code has not been executed in this project.

```bash
git clone https://github.com/sunblaze-ucb/progent && cd progent && git checkout 0d7ea074d5e4b106997ebd56dfa1104c39945c03
pip install -e . && (cd agentdojo && pip install -e .)
export OPENAI_API_KEY=...            # entered by the user in a secure form, never in chat or in files
export SECAGENT_POLICY_MODEL="gpt-4o-2024-08-06" SECAGENT_UPDATE="True" SECAGENT_IGNORE_UPDATE_ERROR="True"
# Auto-Deny instead of Auto-Approve:  export SECAGENT_ONLY_ALLOW_NARROW="True"
cd agentdojo
SECAGENT_SUITE=banking python -m agentdojo.scripts.benchmark -s banking --model gpt-4o-2024-08-06 --logdir logs/update
SECAGENT_SUITE=banking python -m agentdojo.scripts.benchmark -s banking --model gpt-4o-2024-08-06 --attack important_instructions --logdir logs/update
```

Commit `0d7ea07` contains the fix of the subset check of 15 November 2026; a run at `8a8eb89` would reproduce the code state of the paper's date instead. The choice must be stated.

## 5. Cost-estimation plan (no figure is asserted)

1. Count calls: per episode, one agent call per step plus, for Progent, one policy-generation call and up to two policy calls per tool call (decide whether to update; generate the update).
2. Measure tokens on a smoke run of 3 task pairs per arm with the provider's usage field; do not estimate from memory.
3. Cost = (measured input tokens x input price + measured output tokens x output price) x 160 episodes x arms x repeats, with the provider's prices on the day, plus 20% margin.
4. Set that figure as the hard limit of the spending guard (`experiments/live/` refuses to start without one) and stop at the limit.

## 6. Later phase

Integration with LangChain or the OpenAI Agents SDK is a subsequent phase after a design is selected, with its own protocol. No such experiment has been run.
