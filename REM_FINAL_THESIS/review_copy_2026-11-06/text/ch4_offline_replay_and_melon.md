This section summarises the offline replay evidence for the decision policy and states the status of the planned extension with MELON. The offline results (Table 4.15) and the planned MELON comparison are kept separate: no MELON condition has been run with a live language model, so no MELON result exists.

### 4.14.1 Offline replay evaluation

**Data and eligibility.** The replay uses the 3,334 recorded episodes of the 21 agents in the AgentDojo banking environment (Section 4.2). An episode is eligible when replaying it without any defence (B0) reproduces both of its recorded outcomes, user-task utility and attack success, without a replay error (amendment AM-4). This held for 3,313 episodes. The other 21 were excluded:
- 19 attacked and 2 benign episodes;
- in 20 of them the replayed utility differed from the record, and in 1 the attack outcome differed;
- none failed with an error.

**Denominators.** The attack success rate (ASR) and utility under attack are computed over the **2,979 eligible attacked episodes**; benign task success over the **334 eligible benign episodes**.

**Assumptions.** The replay assumes that the recorded agents **do not adapt** to refusals: their later turns are replayed as recorded. It also assumes **no reviewer**: an action that REM escalates is withheld, and an escalation is never counted as task completion. Mitigation acts on the current call only (step-level semantics).

**Table 4.15. Offline replay of recorded agents: no defence, the internal baseline B1 and Full REM (AgentDojo banking v1, `important_instructions`; no adaptation; no reviewer; 95% grouped bootstrap intervals)**

| Configuration | ASR (2,979 attacked) | Utility under attack (2,979 attacked) | Benign task success (334 benign) |
|---|---|---|---|
| B0, no defence | 22.6% [14.8, 29.5] | 49.2% [47.9, 50.3] | 52.4% [38.1, 67.6] |
| B1, consequence-independent baseline (same estimator) | 5.5% [1.1, 13.4] | 51.4% [50.1, 52.7] | 50.9% [33.4, 70.2] |
| Full REM | 0.4% [0.1, 0.7] | 36.4% [34.5, 38.9] | 31.4% [11.0, 54.8] |

**Results.**
- Full REM reduced replay ASR from 5.5% to 0.4%, while benign task success fell from 50.9% to 31.4%, relative to the internal baseline B1.
- The paired differences on the same episodes were −5.1 percentage points for ASR (95% interval −13.0 to −0.7) and −19.5 points for benign task success (−34.1 to −7.4).
- Against no defence, Full REM reduced ASR from 22.6% to 0.4%.

**Interpretation.** B1 and Full REM share the same features, fitted estimator, calibration and policy predicates. They differ only in the decision policy:
- B1 applies operating-point thresholds that ignore consequences;
- Full REM selects among Allow, Modify, Escalate and Block by minimising expected loss with consequence-tiered costs.

The difference between them is therefore attributed to the **decision policy as a whole**, not to any single element of it.

**Calibration sensitivity on the evaluated data.** As a sensitivity check, B1 was re-run with the uncalibrated probability of the same fitted model and with its two thresholds re-selected on the uncalibrated development probabilities. On these data this variant reproduced every B1 verdict on all 6,762 held-out steps and every B1 outcome in all 3,334 replay episodes. This is expected, because thresholds chosen by rank are unaffected by a strictly increasing calibration map. Calibration itself showed no improvement on this dataset: on the held-out steps the expected calibration error was 0.044 with calibration and 0.042 without, and the Brier score was 0.060 in both cases. These findings concern this dataset and these metrics only.

**Deployment check.** When REM was run as a separate gateway service in front of a simulated banking API, it reproduced every decision and outcome of this replay (0 differences over 3,334 episodes). Its median decision time was 0.18 ms per call, on one machine.

### 4.14.2 Planned extension: MELON with and without REM

**Purpose.** The supervisors' before/after study compares two conditions on the same live cases:
1. **original MELON** (Zhu, Yang, et al., 2025);
2. **MELON + REM**, in which REM evaluates each tool call that survives MELON's processing, immediately before execution.

**Implementation.** Both conditions are implemented with the official MELON code, which is unmodified and pinned by commit and file hash. They differ only in the tool executor. Local tests with scripted agents and a substitute embedding client verified, among other things, that a call MELON passes reaches REM and, when REM refuses it, leaves the environment unchanged.

**Status.** **Neither condition has been executed with a live language model, and no paired runs exist.** The study requires:
- access to a model API;
- an authorised spending limit;
- decisions on the backbone model, the number of repetitions and the parameter source.

Until paired runs exist, no comparative statement about MELON is made in this thesis.
