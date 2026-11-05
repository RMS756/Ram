**Status.** This section describes an **implemented protocol for a planned evaluation**. The integration has been verified locally with scripted test agents and fake model clients only. **No run with a language model has been executed, and Table 4.15 contains no result.**

### 4.14.1 Why MELON is the reference

MELON (Zhu, Yang, et al., 2025) is a published runtime defence against indirect prompt injection that was evaluated on AgentDojo and has an official implementation. Chapter 2 reviews it among the goal–action consistency defences (Section 2.6.5; Table 2.5).

MELON re-executes the agent's next step with the user's request masked. It flags an attack when the actions proposed with and without the request are similar, and it then stops the agent. Its evidence is therefore behavioural and model-based. It does not weigh what a proposed action would do or how costly an error would be.

REM, by contrast, decides per action from a calibrated probability and consequence-tiered losses (Section 3.7). The study asks what changes when REM is added at the tool-execution boundary of MELON, compared with MELON alone. This is an **extension of a published defence through integration with REM**:
- MELON's algorithm is not modified;
- REM was not derived from MELON;
- no improvement is presumed;
- a record-level literature search found no evaluation of this combination, but the search was not exhaustive, so no novelty is claimed.

### 4.14.2 Integration point

MELON's official implementation places its detector after AgentDojo's tool executor:
- the loop is `[ToolsExecutor, MELON]`;
- MELON makes the agent's next model call itself, together with a masked model call that executes no tool;
- on detection, MELON replaces the agent's proposed calls with a stop message.

**In MELON + REM, the executor is the only element replaced:** REM evaluates each call that survived MELON immediately before execution. It also evaluates the first turn's calls, which MELON does not inspect.
- A withheld call never reaches the environment.
- The agent receives a refusal carrying the call's identifier and may continue.
- REM never sees MELON's masked generation.

The official MELON code requires an AgentDojo version with string message content. Both conditions therefore run on AgentDojo 0.1.29, whose banking v1 task and attack code are identical to those of REM's fitting traces. Two compatibility measures are applied identically in both conditions:
- the embedding client is supplied without editing the file;
- MELON's per-episode state is reset between episodes, since otherwise it would persist across episodes and conditions.

Each measure and its effect are documented in the integration notes of the study's repository.

### 4.14.3 Frozen settings and training provenance

REM runs with the frozen components of the nested cross-fit (Section 3.11). Nothing is refitted:
- **Estimator:** ridge estimator with logit calibration (γ₁ > 0 in every fold).
- **Predicates and loss structure:** the declared exploratory costs and consequence tiers of Section 3.7, which are not supervisor-approved.
- **Mitigation:** step-level semantics. Modify, Block and Escalate all withhold the current call; their immediate execution effect is the same.
- **Reviewer:** none. An escalated call is never released, and no label-based reviewer is used.

For an attacked case, the fold whose fit excluded that attacker objective is used. Because the 16 user tasks and their environment were seen in fitting, the evaluation covers **held-out attacker objectives on familiar tasks**, not unseen tasks.

### 4.14.4 Protocol

- **Conditions:** MELON and MELON + REM.
- **Benchmark:** AgentDojo banking v1 with the `important_instructions` attack only.
- **Held fixed:** backbone and decoding, MELON's internal settings, attack payloads, step limit and the evaluation checks.
- **Pilot:** 13 cases chosen by a coverage rule declared in advance (every injection task once and four benign tasks), to test compatibility and measure cost.
- **Final case set and repeats:** fixed from the pilot's measured cost; the full set (144 attacked and 16 benign cases) is preferred.
- **Pairing and order:** episodes are paired by case and repeat and run in randomised, interleaved order, each in a fresh environment.
- **Metrics:** attack success rate, utility under attack and benign utility, each over episodes without error. Errors and timeouts are reported separately and never counted as prevented attacks; escalation is never counted as task completion.
- **Uncertainty:** paired differences with cluster-bootstrap intervals over user tasks.

**Table 4.15. Controlled evaluation of MELON with and without REM (AgentDojo banking v1, `important_instructions`) — NOT EXECUTED**

| Metric | MELON | MELON + REM | Paired difference (95% cluster-bootstrap interval) |
|---|---|---|---|
| Attack success rate | not executed | not executed | not executed |
| Utility under attack | not executed | not executed | not executed |
| Benign utility | not executed | not executed | not executed |
| Additional calls withheld by REM | — | not executed | — |
| Escalate verdicts per evaluated call | — | not executed | — |
| Median end-to-end time per episode; REM time per call | not executed | not executed | not executed |
| Tokens and cost per episode | not executed | not executed | not executed |
| Errors and timeouts (by class) | not executed | not executed | — |

### 4.14.5 Interpretation limits

When the study is run, the following limits apply to any finding:
- **Protection.** If MELON has no successful attack in the sample, no further reduction in observed attack success can be demonstrated, and the comparison is about utility and overhead.
- **Utility.** Any additional protection must be reported together with its utility cost. Under no-reviewer semantics, every REM intervention withholds an action.
- **Overhead.** REM adds no model call; MELON roughly doubles the number of model calls of an undefended agent.
- **Scope.** The conclusions are limited to:
  - one attack template;
  - one backbone;
  - exploratory REM costs;
  - familiar tasks;
  - a simulated banking environment.

  Adaptive attacks against MELON are not evaluated.
