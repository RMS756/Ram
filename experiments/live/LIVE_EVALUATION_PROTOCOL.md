# Live Enforcing-Mode Evaluation: Procedure (R4, 1 November 2026)

**STATUS: NOT EXECUTED.** No live agent has been run with REM enforcing. No result in the thesis comes from this procedure.

## 1. Purpose

The thesis's central practical claim is that tier-indexed expected-loss verdicts reduce attack success at acceptable utility cost. That claim needs evidence from agents that can react to REM's refusals. The recorded-trace replay cannot provide it (assumption NO-ADAPT, Chapter 5 §5.6). This procedure states how such an experiment would use the existing design and code.

## 2. Unresolved inputs (the run must not start until each is decided and recorded)

`live_config_TEMPLATE.yaml` lists them; `check_live_config.py` refuses to pass while any is missing (16 items in the template).

| Input | Decision | Why it is needed |
|---|---|---|
| Authorization for paid API use, budget, credentials | D-15 | Live runs call commercial LLM APIs |
| Pre-registration (hypotheses, primary metrics, comparisons, analysis) | D-15 | Prevents analysis choices after seeing results |
| Backbones and exact model versions; decoding parameters | D-15 | Results depend on the model and its sampling |
| Repeats per configuration (Chapter 3: at least three, pending approval) | D-15 | Live runs are stochastic; the replay was not |
| Suite version | D-6, OI-14 | user_task_15 changed at v1.1.1 |
| Mitigation semantics | D-2 / SC-1 | Step-level and episode-level give different results even without adaptation (Chapter 5, Table 5.11) |
| Costs, tiers, predicates | D-9 | Decide the verdicts |
| Feature set, including the x_ctx1 classifier | D-8 | Classifier is absent from the current implementation |
| Label rule | D-6 | Human audit not yet performed |
| Reviewer model for Escalate | D-7 | Only two bounds exist |
| Frozen fitted parameters | — | The live run must use parameters fitted before it, never refitted on live data |

## 3. Procedure (using existing components)

1. **Environment.** AgentDojo 0.1.35 provides `AgentPipeline`, `SystemMessage`, `InitQuery`, `ToolsExecutionLoop`, `ToolsExecutor` and provider LLM elements (`OpenAILLM`, `AnthropicLLM`, `GoogleLLM`, `CohereLLM`, `LocalLLM`), verified by import on 1 Nov 2026.
2. **Guard placement.** Build the pipeline as `replay_episode` does (`rem/integration/agentdojo_replay.py`), with the recorded-trace `ReplayLLM` replaced by the chosen provider LLM element, and REM's `GuardedToolsExecutor` as the tool executor. The agent's model, prompts and tools are not modified.
3. **Configurations.** B0 (no guard), B1, REM and REM without expected-loss Escalate, under the approved mitigation semantics (and, if approved, the other semantics as a sensitivity analysis), each with the approved reviewer treatment.
4. **Runs.** Every (backbone, user task, injection task, attack) cell for the pre-registered number of repeats, plus benign runs without injection. Record the AgentDojo run logs, REM's audit records and both timers (`rem_latency_ms`, `rem_latency_full_ms`).
5. **Metrics.** ASR, benign utility and utility under attack (Chapter 3 §3.12), retries and alternative routes after a refusal (counted from the audit records), residual success after Modify, escalation rate, complete-call latency.
6. **Analysis.** Grouped bootstrap by injection task and user task, as in Chapter 5, with repeats nested inside cells. Any test or multiplicity correction as pre-registered.
7. **Reporting.** Live results are reported separately from the recorded-trace results; neither substitutes for the other.

## 4. What is ready and what is not

| Ready | Not ready |
|---|---|
| Guard, decision rule, mitigation (both semantics), audit record, timers | Every input in Section 2 |
| Pipeline integration (exercised in replay; 3,313 of 3,334 all-Allow replays reproduce the record) | Integration with a live LLM element has not been run |
| Fail-closed configuration check | Pre-registration document |
