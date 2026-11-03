**The closed-loop evaluation with live agents was not executed.** This section therefore reports no attack success rate, utility, intervention statistic or adaptation behavior of a live agent, and no table or figure in this chapter contains a live result.

Two conditions prevented execution on 3 November 2026:

- **No model access.** No credential for a language-model provider was available in the execution environment; the provider endpoints that were reachable rejected unauthenticated requests, and model-weight repositories were not reachable, so no local model could be run.
- **Undecided design inputs.** The backbone, decoding parameters, number of repeats, fitted-parameter source, authorisation and pre-registration (Section 3.17.5) have not been decided. The runner refuses to start until they are.

What was executed concerns the correctness of the integration, not the effectiveness of REM:

**Table 4.13. Verification of the closed-loop integration (not experimental results)**

| Check | Agent | Outcome |
|---|---|---|
| Integration tests (12) | Scripted test double that proposes predetermined calls and retries or replans after a refusal | All passed: released calls execute; withheld calls (Block, Modify, unapproved Escalate) are not executed and the agent receives a refusal with the original call identifier; step-level Modify does not persist, episode-level Modify does; retries and replans are recorded; episode state is not shared; REM verdicts are unchanged when reference labels are flipped |
| Harness smoke test (B0, B1, REM; step-level, no reviewer; one frozen fold) | Scripted agent that executes the ground-truth calls of the user task and then of the injection task, without adapting | 480 episodes over all 144 attacked task pairs and 16 benign tasks with the benchmark's `important_instructions` injections; 0 execution errors; no withheld call was executed |

The smoke-test agent is not a model of an LLM agent: it never reads tool outputs or reacts to refusals. Its counts are therefore not reported as attack-success or utility results. The live evaluation remains the first item of future work (Section 5.6).
