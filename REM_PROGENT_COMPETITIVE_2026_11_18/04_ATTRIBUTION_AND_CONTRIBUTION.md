# Attribution matrix, source-to-code registry and contribution map

Status: `[PROPOSED - EXPLORATORY]`. "Upstream" means Progent at the pinned commits (`THIRD_PARTY_NOTICES.md`). No equation identifier is created here; the frozen REM registry is unchanged.

## 1. Attribution matrix (idea → origin → where it appears)

| Element | Origin | Used in | Changed? |
|---|---|---|---|
| Per-tool argument policies; first satisfied allow rule; arguments checked only if present | Progent engine (`secagent/tool.py`, `_check_tool_call`) | P0, C2[gen] via `progent_upstream.upstream_allowed`; PG/C2PG via REM's replay checker | not changed |
| Manual banking policy (trusted recipient list) | Progent fork, banking `task_suite.py` at 9befb41 | PG, C2PG, C3PG | read as data |
| LLM policy generation from the user query; update after tool results; Auto-Deny subset check (z3) vs Auto-Approve | Progent engine and fork (`generate_security_policy`, `generate_update_security_policy`, `SECAGENT_ONLY_ALLOW_NARROW`) | P0 and C2[gen] configurations (`progent_upstream.CONFIGS`) | not changed; not executed |
| Authority front (operation, effect, recipient authority, condition) | REM revision 3 (`permission_v3`, frozen) | C1–C3 | options only (`bind=False, fulfil=False`) |
| Amount grammar (literal, percent, fractions, multiples, balance expressions); exact rational evaluation | REM repair study v1 / v2 (frozen) | C1–C3 | reused unchanged |
| Contract scope to the next payment verb; operator and stray-number check; appositive stated amount; merge of duplicate instructions | **new in this study** | `contracts.py` | – |
| Single complete witness with own condition, own amount, own remaining allowance | **new in this study** (the review's F2 requirement) | `contracts.decide` | – |
| Per-instruction ledger (reserve / commit / release on execution signal) | **new in this study** | `contracts.Ledger`, `contract_arms.ingest` | – |
| Ridge F4 + Platt + two-verdict expected loss | REM v1.0 math (frozen) and earlier HV arm | C3PG | reused unchanged |
| Expected-cost decision principle | Elkan (2001), as in the frozen design | C3PG learned stage | unchanged |

## 2. Source-to-code registry

| Code | Upstream source it depends on | Pinned | How |
|---|---|---|---|
| `experiments/progent_competitive/progent_upstream.py` | `secagent/tool.py` lines 37–40, 167–205, 415–506, 573–591; `agentdojo/run.sh`; `agentdojo/.../tool_execution.py` l.121 | 0d7ea07 | import from a verified checkout; env switches set before import |
| `experiments/progent_competitive/closed_loop.py` | `agentdojo/src/agentdojo/agent_pipeline/tool_execution.py` (`ToolsExecutor.query`), `basic_elements.py` (`InitQuery`), `benchmark.py` (`reset_security_policy`), banking `task_suite.py` (`apply_secure_tool_wrapper`) | 0d7ea07 | subclass of the fork's executor; mirrors its loop |
| `experiments/progent_competitive/parity_upstream.py` | `secagent.check_tool_call`, `update_security_policy` | 0d7ea07 | parity of REM's replay checker with the upstream checker; gated |
| `experiments/improve_study/progent_manual.py` (earlier) | banking `task_suite.py` manual policy block; `secagent/tool.py` checker semantics | 9befb41 | data read; checker re-implemented by inspection |
| `experiments/progent_competitive/budget.py` | `SYS_PROMPT`, `SYS_PROMPT_2`, `SYS_PROMPT_UPDATE` constants | 0d7ea07 | parsed, not imported |

## 3. Contract-scope map (which component answers which question)

| Question | C1 component | Progent counterpart |
|---|---|---|
| Is this operation on this account requested? | authority front (frozen revision 3) | allow-rule for the tool with a recipient restriction (manual list or generated) |
| Does the amount equal what the request determines? | contract binding + scope (`contracts.py`) | an optional argument restriction, if the policy writer or the LLM gives one |
| Does the instruction's own condition hold? | witness: `holds(condition, balance)` | not expressible in a static argument policy |
| Is the allowance still available? | ledger | none (policies are stateless) |
| Can untrusted text change the answer? | no: operands only from the request and two structured bank fields (declared assumption) | the update step reads tool results; Auto-Deny limits updates to narrowing |

## 4. Contribution map (what is new, what is reused, what is not claimed)

- **New:**
  - the financial contract (scope, single witness, ledger, duplicate merge);
  - reference-labelled diagnostics with state (failed attempts, retries, repetitions);
  - the composed arms C1–C3;
  - the closed-loop harness and preflight;
  - the volume-based budget estimator;
  - the executable validation scorer.
- **Reused unchanged:**
  - REM revision-3 front and compiler, the v1/v2 amount grammar, stored fits;
  - Progent's engine, configurations and manual policy.
- **Not claimed:**
  - superiority over full Progent (not run);
  - generality beyond the supported English constructions;
  - independent validation;
  - any change to the approved REM v1.0 design.
