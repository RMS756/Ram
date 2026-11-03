# AgentDojo Closed-Loop Integration: Design

**Status:** implemented and tested with scripted test agents; **not executed with a language model**.

## 1. Defended pipeline

```
SystemMessage(system prompt) → InitQuery(user task prompt) → LLM
   → ToolsExecutionLoop( [ GuardedToolsExecutor(RemGuard) , LLM ], max_iters = 15 )
   → Recorder (captures the final message list for the run log)
```

The flow for each proposed call `a_t = (tool, args)` in an assistant message:

1. `GuardedToolsExecutor` opens a decision point and calls `RemGuard.evaluate(tool, args)` **before** any execution.
2. `RemGuard` computes x_t from the episode history and the proposed arguments, the tier k_t, the logit s_t and the calibrated p_t (frozen fold), and the verdict from the configured decision function (B0 allow-all, B1, REM or REMnoEsc).
3. `_mitigate` applies the configured semantics:
   - **step-level:** Allow releases the call; Modify, Block and an unapproved Escalate withhold it;
   - **episode-level:** in addition, Modify restricts the tool class and Block restricts 𝒯_R.
4. A released call goes to `runtime.run_function`. A withheld call returns a tool message carrying the **same `tool_call_id`**, empty content and `error = "REM: …"`, so the agent sees the refusal.
5. The result or refusal is ingested as untrusted context, and the LLM is queried again. It may answer, retry, replan or stop.
6. `run_task_with_pipeline` scores utility and security on the post-environment.

## 2. Controlled variables across B0, B1 and REM

The same suite version, task pair, injection text, system prompt, backbone and decoding settings, `max_iters` and frozen fold are used in every condition.

- B1 and REM use the **same scorer** (β, γ) and predicates. They differ only in the verdict rule (Eq. 3.14 thresholds vs Eqs. 3.6–3.7 expected loss).
- REMnoEsc removes expected-loss Escalate, giving REM the same escalation opportunity as B1.

## 3. Interpretations

| ID | Interpretation |
|---|---|
| L-1 | AgentDojo re-queries the pipeline up to three times when no final text is produced. The same guard (episode history) persists across re-queries |
| L-2 | Adaptation counts come from the audit record: retry = the same tool and argument digest as an earlier withheld call; replan = a different restricted tool after a withheld call; y = 1 released after a refusal |
| L-3 | B0 runs through the same guarded executor with an allow-all decision, so that audit records (labels, features, timers) exist for B0 too. Execution is identical to AgentDojo's own `ToolsExecutor`: the string-list argument conversion and invalid-tool handling are the same |
| L-4 | The label y_t is computed for the audit record and the idealised reviewer only. A test verifies that REM verdicts are unchanged when labels are flipped |

## 4. Safety precautions

- All tools act on AgentDojo's simulated banking environment. No real account, payment system or external service is touched.
- REM never initiates a call.
- The runner aborts before any API call if a design input or credential is missing.
- Message logs store at most 500 characters per message, and argument values only as digests in the audit record.
