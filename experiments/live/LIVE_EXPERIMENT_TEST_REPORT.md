# Live Integration: Test Report (3 November 2026)

**Command:** `python3 -m pytest -o addopts="" -q -p no:cacheprovider`

**Result:** **217 passed**: the original 205 plus 12 new tests in `tests/test_live_integration.py`. Per-test log: `smoke_output/pytest_live_integration.log`.

**Environment:** Python 3.11.17; agentdojo 0.1.35; anthropic 2.3.0; openai 3.41.0; numpy 2.4.6; PyYAML 6.0.1; pytest 9.2.0.

All tests use AgentDojo's real banking suite (v1) and environment. The agent is a scripted test double, not a language model.

| Required test | Test | What it asserts | Result |
|---|---|---|---|
| Allow execution | `test_allow_executes_the_call` | The released `send_money` creates the transaction | PASS |
| Blocked calls are not executed | `test_withheld_call_is_not_executed_and_agent_sees_refusal[BLOCK]` | No transaction; the refusal carries the original `tool_call_id` and the "REM:" error | PASS |
| Modify follows the declared semantics | `…[MODIFY]`; `test_step_level_modify_does_not_persist_but_episode_level_does` | Step-level: the call is withheld, a later call is released. Episode-level: the later call to the same tool class is refused (`refuse_restricted`) | PASS |
| Escalation handled safely | `test_escalate_bounds` | No reviewer: nothing executed. Idealised: the y = 0 call is released and the y = 1 call withheld | PASS |
| Multiple calls; tool-result ids | `test_multiple_calls_in_one_message_keep_ids_and_order` | Two calls in one message, ids preserved in order, the same decision point, only the released one executed | PASS |
| Agent retry; replanning | `test_retry_and_replan_are_observed_and_counted` | Retry of the identical call and a replan to `schedule_transaction` are both withheld and counted (retries = 1, replans = 1); no side effects | PASS |
| No episode-state contamination | `test_episode_state_is_not_shared` | The restriction set, audit and history of one guard are unaffected by another episode | PASS |
| No information leakage | `test_rem_decision_does_not_depend_on_the_label` | Flipping every reference label leaves REM verdicts identical; the attribution identity holds (error < 1e-9) | PASS |
| Correct audit records | (asserted within the tests above) | `released`, `mechanism`, `decision_point`, `label`, `additivity_error` | PASS |
| Correct metrics | `test_adaptation_statistics_unit`, `test_analysis_on_synthetic_records` | Adaptation counts; ASR, benign utility and intervention rates on synthetic records with known answers | PASS |
| Fail-closed runner | `test_runner_is_fail_closed_on_the_template` | `run_live.py` on the template exits 2 with "DESIGN BLOCKED" | PASS |
| Existing REM regression tests | the full suite | 205 original tests | PASS |

**Not tested:** behaviour with a real LLM element; provider error handling (rate limits, timeouts); the credential check against a live provider.
