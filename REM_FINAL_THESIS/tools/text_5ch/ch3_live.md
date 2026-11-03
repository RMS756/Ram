**Status.** The closed-loop evaluation described in this section is **implemented and tested with scripted test agents, but has not been executed with a language model** (Section 4.12). Nothing in Chapter 4 is a live result.

### 3.17.1 Purpose

The replay sensitivity analysis (Section 3.11.11) re-executes recorded trajectories and assumes that the agent does not adapt to REM's refusals. It can therefore show whether a recorded attack call would have been withheld, but not what an agent does after a refusal: it cannot observe retries, rephrased calls or alternative tools. The closed-loop design removes that assumption. A running LLM agent receives REM's decision for each proposed call and may continue, retry, replan or stop, and the benchmark scores the outcome after the agent's own reaction.

### 3.17.2 Defended agent pipeline

The integration uses AgentDojo's own pipeline elements without modifying the benchmark (Figure 3.5). The pipeline consists of a system message, the user task's prompt, the LLM, and a tool-execution loop in which AgentDojo's tool executor is replaced by REM's guarded executor (Section 3.16.8). For each proposed call the defended process is:

1. the agent proposes a tool call with arguments;
2. REM intercepts the call **before** it is executed;
3. REM computes the evidence vector, the tier, the logit and the calibrated probability with frozen parameters (Sections 3.4–3.7);
4. the decision function selects Allow, Modify, Escalate or Block (Eqs. 3.6–3.7, or the baseline of Eq. 3.14);
5. the Mitigation Layer applies the declared semantics (Section 3.8, Table 3.14): a released call is executed in the sandbox; a withheld call returns a tool message with the same tool-call identifier and a refusal notice;
6. the result or refusal re-enters the agent's context as untrusted content, and the agent continues;
7. the benchmark evaluates utility and security on the final environment.

The decision code is the code of the recorded-trace study (`RemGuard`); only the source of the agent's messages changes, from a recorded trajectory to a live model. AgentDojo re-queries the pipeline up to three times when the agent produces no final answer; the same guard, and therefore the same episode history, persists across these re-queries.

![Figure 3.5. Closed-loop (live-agent) evaluation architecture. REM's guarded executor replaces AgentDojo's tool executor; the agent receives the result of a released call or the refusal of a withheld one and may retry, replan or stop. Implemented and tested with scripted test agents; not executed with a language model.](REM_FINAL_THESIS/final_five_chapters/figures/fig3_5_live_architecture.png){width=100%}

### 3.17.3 Conditions and controlled variables

Three primary conditions are defined, with the same pipeline, tasks, injections, system prompt, model, decoding settings and iteration limit:

- **B0:** no defense (every call released; REM records the step but never intervenes);
- **B1:** the consequence-independent operating-point baseline (Eq. 3.14) on the same frozen estimator, calibration and predicates;
- **REM:** the tier-indexed expected-loss verdict (Eqs. 3.6–3.7) on the same frozen estimator.

REM without expected-loss Escalate (Section 3.11.7) can be added as a fourth condition. The comparison B1 versus REM therefore isolates the decision rule, as in the recorded-trace study.

### 3.17.4 Frozen parameters

No parameter is fitted on live data. The estimator, calibration map, baseline thresholds, benign reference and r~mod~ are those of one outer fold of the recorded-trace cross-fitting (Procedure 3.1). Which fold is used is a design input; the pilot has no fit on all recorded data.

### 3.17.5 Design inputs required before execution

The runner refuses to start until each of the following has been decided and recorded (CLAUDE design lock; supervisor decision register D-2, D-6, D-7, D-8, D-9, D-15):

| Input | Status |
|---|---|
| Authorisation for paid model use, budget, pre-registration of hypotheses and analysis | Pending (D-15) |
| Backbone(s) with exact model versions; decoding parameters | Pending (D-15) |
| Number of repeats per configuration | Pending (Section 3.11.9 proposes at least three) |
| Suite version, attack templates, user and injection tasks | Pending (D-6) |
| Mitigation semantics (step-level and/or episode-level) | Pending (D-2) |
| Reviewer treatment (idealized and/or no-reviewer bound) | Pending (D-7) |
| Costs, tiers, predicates and feature set | Exploratory pilot values only (D-9, D-8) |
| Fitted-parameter source (outer fold) | Pending |

### 3.17.6 Metrics, statistics and logging

The metrics are those of Section 3.12, computed on live outcomes: attack success rate, benign utility and utility under attack from the benchmark's verdicts; intervention rates on y = 0 and y = 1 proposals; and processing time from the complete-call timer. Three descriptive adaptation counts are added, computed from REM's audit record: a *retry* is a later proposal of the same tool with the same argument digest as a withheld call; a *replan* is a later proposal of a different restricted tool after a withheld call; and a *release after refusal* is a reference-labelled attack call released after an earlier withheld call in the same episode. Uncertainty is estimated by the grouped bootstrap of Section 3.11.9, with repeats kept inside their injection-task or user-task group. Every episode is logged with its audit records, truncated messages and adaptation counts, together with a manifest of the commit, configuration hash and frozen fold.

### 3.17.7 Safety precautions

All tools act on the benchmark's simulated banking environment; no real account or payment system is reachable, and REM never initiates a call. Argument values are recorded only as digests in the audit record, and message logs are truncated.

### 3.17.8 Implementation and verification status

**Table 3.26. Implementation status of the closed-loop evaluation (3 November 2026)**

| Component | Location | Status |
|---|---|---|
| Defended live pipeline | `rem/integration/agentdojo_live.py` | Implemented; tested with scripted test agents |
| Guarded executor, decision and mitigation | `rem/integration/agentdojo_replay.py` (unchanged) | Implemented; used in the recorded-trace study |
| Runner with fail-closed configuration and credential checks | `experiments/live/run_live.py` | Implemented; verified to refuse the undecided template |
| Metrics with grouped bootstrap | `experiments/live/analyze_live.py` | Implemented; tested on synthetic records |
| Integration tests (interception, semantics, identifiers, retries and replans, episode isolation, label isolation) | `tests/test_live_integration.py` | 12 tests passed (full suite: 217 passed) |
| Harness smoke test with a scripted ground-truth agent on all 160 task combinations | `experiments/live/smoke_scripted.py` | Executed: 480 episodes, 0 errors (not an experimental result) |
| Execution with a language model | — | **Not executed**: no model credential; design inputs pending |
