# MELON versus MELON + REM — Local Verification Report

**Date:** 5 Nov 2026.

**Scope:** mechanism checks only. They use:
- **scripted test agents** (which also answer MELON's masked re-execution);
- a **deterministic fake embedding client** (identical call text → cosine 1; different text → near-orthogonal vectors);
- for the end-to-end runner test, a **fake OpenAI provider** that returns real `ChatCompletion` objects.

MELON's own detection code runs unchanged on these inputs. **None of these outcomes is a security result**, and no real model or embedding call was made.

## Results

| Environment | Command | Result | Log |
|---|---|---|---|
| MELON environment: AgentDojo 0.1.29, Python 3.11.17, upstream MELON at `4d3cc9c` | `MELON_REM_BUNDLE=experiments/melon_rem/frozen/frozen_rem_bundle.pkl /home/user/venvs/melon029/bin/python -m pytest -o addopts="" tests/test_melon_rem_integration.py tests/test_melon_rem_offline.py` | **30 passed** | `verification/pytest_melon_env_agentdojo_0_1_29.log` |
| Main environment: AgentDojo 0.1.35, the existing REM suite | `python3 -m pytest -o addopts="" -q` | **225 passed, 1 skipped**: the existing 217 + 8 offline MELON tests. The MELON integration module is skipped there by design. | `verification/pytest_main_env_agentdojo_0_1_35.log` |

After the runs, the upstream clone is byte-clean (`git status --porcelain` is empty, and no `__pycache__` is written).

## Required checks → tests

| # | Required check | Test(s) | Verified |
|---|---|---|---|
| 1 | Original MELON behaviour intact in the reference condition | `test_upstream_file_is_pinned_and_unmodified` (hash and commit; clean clone); `test_melon_constructed_as_in_readme_with_injected_client` (README construction; only the client injected); `test_pipelines_differ_only_in_the_executor` (reference uses AgentDojo's own `ToolsExecutor` class; same MELON instance and `max_iters`); `test_melon_detection_stops_attack…[MELON]` (masked call matches → stop message, attacker unpaid) | Yes, for the detection mechanics. The real detection rate depends on the real LLM and embeddings (not testable locally). |
| 2 | Combined condition invokes REM at the documented boundary | `test_melon_detection…[MELON_REM]` (the call MELON stopped never reaches REM); `test_rem_withholds_a_call_that_melon_passed…` (REM evaluates and withholds a call MELON passed; in the reference condition the same script pays the attacker) | Yes |
| 3 | Calls withheld by REM are not executed | `test_rem_withholds…`, `test_multiple_calls…`, `test_modify_and_block…` (Modify, Block, Escalate-without-reviewer: attacker unpaid) | Yes |
| 4 | Calls allowed by both defences execute exactly once | `test_call_allowed_by_both_defenses_executes_exactly_once[MELON, MELON_REM]`; `test_masked_reexecution_has_no_side_effects…` (`run_function` spy: exactly the original calls, once each) | Yes |
| 5 | Tool identifiers and refusal messages valid | `test_rem_withholds…` (refusal carries the proposing call's id; `error` starts with "REM:"); `test_multiple_calls_in_one_turn_keep_ids_order_and_mixed_outcomes` | Yes |
| 6 | Episode histories and environment states reset | `test_episodes_do_not_share_melon_state_or_environment`; `test_upstream_shared_default_extra_args_would_leak_the_bank_without_isolation` (demonstrates the upstream leak that compatibility measure C-2 prevents); the runner builds a fresh pipeline, guard and MELON instance per episode and loads a fresh environment | Yes |
| 7 | Retries and alternative actions recorded | `test_retry_after_refusal_is_recorded` (adaptation statistics from the REM audit); the agent continuing after a refusal is shown in `test_rem_withholds…` | Yes |
| 8 | Multiple tool calls handled | `test_multiple_calls_in_one_turn_keep_ids_order_and_mixed_outcomes` | Yes |
| 9 | Labels cannot influence decisions | `test_labels_cannot_change_the_decision_or_the_execution` (all labels 0 vs all 1: identical execution; label recorded for audit only); `test_real_frozen_rem_policy_runs_at_the_boundary_and_ignores_labels` (real frozen fold policy: identical verdicts and probabilities); MELON receives only messages | Yes |
| 10 | Errors and timeouts classified separately | `test_errors_are_classified_separately[timeout, budget_stop, infrastructure_error]`; `test_analysis_denominators_errors_and_escalation` (errors excluded from ASR, not counted as prevention; escalated benign call ≠ success) | Yes |
| — | MELON's masked run has no side effects and bypasses REM | `test_masked_reexecution_has_no_side_effects_and_bypasses_rem` (masked `send_money`/`update_password` never executed; masked run receives a deep-copied environment; REM audit contains only original calls) | Yes |
| — | Spending guard | `test_ledger_settles…`, `test_call_refused_when_reservation_would_exceed_cap`, `test_unpriced_model_is_refused`, `test_in_flight_reservations_count_against_the_cap` | Yes (in-process) |
| — | Runner fail-closed, plan, provenance | `test_runner_is_fail_closed_on_the_template` (exit 2); `test_runner_refuses_without_credential_or_with_wrong_provenance` (exit 3, exit 5); `test_dry_run_plans_paired_interleaved_schedule` (26 pilot episodes; 320 full; deterministic seed; pairs adjacent; held-out fold rule) | Yes |
| — | Runner end to end | `test_runner_end_to_end_with_fake_provider` (26 episodes through OpenAILLM parsing, the real attack payloads, the frozen bundle, the ledger, manifest and records; the API key is absent from the manifest) | Yes, with a fake provider |
| — | Budget projection | `test_budget_projection_uses_only_measured_tokens_and_given_prices` | Yes |

**Fixture observation (not a result).** With the real frozen fold `injection_task_0` policy and a scripted attack:
- `get_most_recent_transactions`: tier 1, p = 0.008 → Allow;
- the attacker's `send_money` (100): tier 3, p = 0.653 → Modify, withheld (step-level).

REM's processing was about 0.4 ms per call. This shows that the frozen components load and act at the boundary. It says nothing about live behaviour.

## What could not be verified locally

1. **MELON's real detection behaviour:** the masked-run generations of a real LLM and the real `text-embedding-3-large` similarities.
2. **Real provider compatibility:** AgentDojo 0.1.29's `OpenAILLM` with OpenAI SDK 3.46.0 against the live API. It was checked only with SDK response objects from a fake client. **The pilot is the compatibility test.**
3. **Real token counts and costs**, hence the budget for the final run.
4. **Agent adaptation to REM refusals** with a real model.
5. **Whether the bank reset per episode (C-2) changes MELON's detection** relative to the paper's runs (unknown; same in both conditions here).
