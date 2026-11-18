# 09 Comparison with Progent (Phase 8)

## What "Progent" means in each result

| Item | Status |
|---|---|
| **Official implementation** | github.com/sunblaze-ucb/progent, pinned `0d7ea074d5e4b106997ebd56dfa1104c39945c03` (2026-11-15), MIT licence ("Copyright (c) 2026 Progent"). Engine `secagent/` (needs pydantic, jsonschema, docstring_parser and z3-solver for the subset check); AgentDojo fork at version 0.1.29. The policy model is selected by `SECAGENT_POLICY_MODEL` and runs on OpenAI, Anthropic, or a local OpenAI-compatible server at 127.0.0.1:8000 for `meta-llama/` and `Qwen/` names. |
| **PG arm** (A7) | Progent's **manual** banking policy of commit `9befb41`, read as data and evaluated by REM's replay checker on recorded calls, with no generation and no update |
| **Executed upstream engine** (this study) | The 9befb41 manual policy was installed with upstream's own `update_security_policy` into the **upstream engine at 0d7ea07** (isolated venv, explicit authorisation), and upstream `check_tool_call` was called on (a) 38 synthetic parity cases and (b) **all 2,551 restricted calls proposed by the recorded agents** in the primary population. **0 disagreements** with REM's replay checker. Files: `logs/progent_parity.log`, `results/progent_parity_recorded_calls.json`. |
| **Full Progent** (LLM-generated policies, updates, Auto-Deny / Auto-Approve) | **Not executed.** No model endpoint exists in this session (`10`). No result is reported for it. |

**Consequence.** On every recorded call, PG's decisions equal upstream Progent's checker running its own manual policy. PG is therefore a faithful execution of **Progent's manual-policy configuration of 9befb41**. It is **not** an execution of the complete Progent system.

**Correction (amendment 2, `05a`).** The pinned fork at 0d7ea07 no longer contains that manual policy. "Progent without generation" in the pinned fork installs no policy and allows everything. A future closed-loop comparison must install the 9befb41 policy explicitly.

## Comparison under equal conditions (same tasks, recorded calls, same evaluator)

| Measure | C1 | C1I | PG (manual Progent) |
|---|---|---|---|
| Replay primary: attacks / benign / all tasks | 0 / 138 / 1,437 | 0 / 141 / 1,473 | 0 / **154** / 1,450 |
| Replay dev2: attacks / benign / all tasks | 0 / 28 / 1,227 | 0 / 33 / **1,393** | 0 / **35** / 1,305 |
| FP intervention rate (benign, primary) | 0.596 | 0.579 | **0.236** |
| Scripted benign / 16 | 10 | 11 | **13** |
| Scripted breaches (3 orders) | 0 / 0 / 1 | 0 / 0 / 1 | **0 / 0 / 0** |
| Author-written suites (authorised released) | 50 / 62, 0 / 14 | 50 / 62, 8 / 14 | 0 / 62, 0 / 14 |
| Fixtures legitimate / unsafe | 36 / 0 | 36 / 0 | 10 / 0 |
| Expresses amount, condition, repetition | yes | yes | no |
| Operational assumption | request parsing (supported English constructions), trusted structured bank fields | same + trusted record recipient field | a hand-written list of the benchmark's own recipients |

**Paired contrasts (primary).**
- C1 − PG all tasks: −0.004 [−0.081, 0.069].
- C1I − PG: +0.007 [−0.071, 0.080].

Neither direction is established.

## Answer
- **No claim of superiority over Progent is supported.**
- On AgentDojo, Progent's manual policy has higher benign utility, a lower intervention rate and the only order-robust protection for ut15×it4.
- On author-written requests with accounts outside its list, it refuses all legitimate work, whereas C1 and C1I release most of it while refusing every unauthorised and ambiguous proposal.
- A fair comparison with **full** Progent, with generated and updated policies, remains open and needs a model endpoint (`10`, earlier harness `experiments/progent_competitive/closed_loop.py`).
