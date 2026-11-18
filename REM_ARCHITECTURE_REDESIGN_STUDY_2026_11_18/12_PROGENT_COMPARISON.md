# 12 Comparison with Progent

## What was and was not executed

| Item | Status | Evidence |
|---|---|---|
| Progent paper (Shi et al., 2025, arXiv 2504.11703; preprint) | read; verification record in `results/literature_verification.json` | `02` |
| Official implementation, pinned `0d7ea074d5e4b106997ebd56dfa1104c39945c03` | present at `/home/user/upstream/sunblaze-ucb_progent`; **not installed** in the main environment | – |
| **PG arm** | Progent's **manual** banking policy of commit `9befb41` (an allow-list of 5 recipient IBANs for `send_money`, `schedule_transaction`, `update_scheduled_transaction`; other tools allowed), evaluated by REM's replay checker | `experiments/progent_competitive/` |
| **Parity of PG with the upstream engine** | upstream `check_tool_call` at 0d7ea07, with the 9befb41 policy installed through upstream's own `update_security_policy` (isolated venv, `SECAGENT_POLICY_MODEL=none`) | earlier: 2,551 recorded primary calls, **0 disagreements**; this study: **662 held-out H restricted calls, 0 disagreements** (`results/progent_parity_heldout_calls.json`, `logs/progent_parity_heldout.log`) |
| **Full Progent** (LLM-generated policies, policy updates, Auto-Deny / Auto-Approve) | **NOT EXECUTED.** No model endpoint and no authorised spending cap (`13`). | – |

**Consequences.**
- PG reproduces **Progent's manual-policy configuration** exactly on every recorded call checked: 3,213 calls in total.
- PG is **not** the complete Progent system.
- The pinned fork at 0d7ea07 no longer contains the manual policy, so the 9befb41 policy is installed explicitly (correction recorded in `REM_IMPROVEMENT_CONTROLLED_STUDY_2026_11_18/05a`).

## Equal-condition comparison (same recorded calls, same evaluator, same metrics)

| Measure | C1 | REM-B | PG (manual Progent) |
|---|---|---|---|
| Primary: attacks / benign (of 334) / all tasks (of 3,313) | 0 / 138 / 1,437 | 0 / 139 / 1,457 | 0 / **154** / 1,450 |
| Primary: audited value/object violations released | 11 | 11 | **161** |
| Primary: FP intervention rate | 0.596 | 0.590 | **0.236** |
| dev2: attacks / benign (of 48) / all tasks (of 2,113) | 0 / 28 / 1,227 | 0 / 33 / **1,363** | 0 / **35** / 1,305 |
| dev2: violations | 0 | 0 | **36** |
| H: attacks / benign (of 53) / all tasks (of 522) | 0 / 27 / 245 | 0 / 27 / 249 | 0 / **33** / **280** |
| H: violations | 0 | 0 | 0 |
| H: FP intervention rate | 0.636 | 0.636 | **0.159** |
| Probe population (2,645 episodes): attacks | 0 | 0 | 0 |
| Scripted: benign of 16 / ut15×it4 goals in the 4 attacked orders | 10 / 0, 0, 1, 1 | 11 / **0, 0, 0, 0** | **13** / **0, 0, 0, 0** |
| Development scenarios: authorised released / unauthorised / ambiguous | 6 / 4 / 0 | **12 / 0 / 0** | 0 / 0 / 0 |
| Held-out probes | 4 / 4 / 2 | **12 / 0 / 0** | 0 / 0 / 0 |
| Diagnostics: authorised released of 62 | 50 | 50 | 0 |
| Generalisation: authorised released of 14 | 0 | 4 | 0 |
| Fixtures: legitimate released / unsafe (of 43) | 36 / 0 | 36 / 0 | 10 / 0 |
| Latency per call: median / p95 (ms, 300 episodes) | 0.48 / 13.9 | 0.44 / 13.2 | 0.27 / 0.86 |

**Paired all-task contrasts, REM-B − PG.**

| Population | Difference [95% interval] | Tasks gained / lost |
|---|---|---|
| primary | +0.0021 [−0.0733, 0.0745] | 131 / 124 |
| dev2 | +0.0274 [−0.1060, 0.1652] | 172 / 114 |
| H | −0.0594 [−0.1711, 0.0229] | 8 / 39 |

**No direction is established.**

## Fairness analysis

| Factor | Favours | Note |
|---|---|---|
| PG's allow-list is written for the AgentDojo banking suite and contains the benchmark's own legitimate recipients | PG on replay | Its high benign utility depends on knowing the benchmark's recipients in advance; on author-written requests with other accounts, it releases nothing. |
| PG does not constrain amounts, objects or repetition | REM-B on value integrity | This explains PG's 161 / 36 audited violations (wrong amounts, wrong standing orders, repeated payments to allowed recipients). |
| REM-B parses supported English constructions of the request | PG on unsupported wording | HC2 (a tip worded outside the grammar) is withheld by REM-B. |
| REM-B escalates unresolved evidence; escalation withholds in deployment | PG on utility | REM-B's 105 unnecessary escalations of correct values on H would need a human reviewer. |
| Full Progent generates policies per task with an LLM | unknown | Not executed. Generated policies could narrow or widen PG's list; no claim either way. |
| Both evaluated by NO-ADAPT replay | neither | Real agents replan after refusals. Replay cannot show this (`13`). |

## Answer

**Not supported:**
- that REM-B is superior to Progent;
- that REM-B is inferior to full Progent.

**Supported (manual-policy configuration only):**
- PG has higher benign utility and a lower intervention rate on the recorded AgentDojo traces.
- REM-B is the only one of the two that keeps audited value/object integrity: 11 vs 161 violations in primary, and 0 vs 36 in dev2.
- REM-B also authorises requests whose recipients are not on a pre-written list.

These are different security properties, not a ranking.

## What a full comparison needs
- A model endpoint and an authorised spending cap, for policy generation and the agent.
- The harness `experiments/progent_competitive/closed_loop.py` (fail-closed; already written).
- Volumes in `REM_PROGENT_COMPETITIVE_2026_11_18/06_BUDGET_ESTIMATE.md`.
- At least the arms P0_manual, P0_generated, P0_update_autodeny and REM-B under the same agent.
- A priori counts of episodes and repeats.
