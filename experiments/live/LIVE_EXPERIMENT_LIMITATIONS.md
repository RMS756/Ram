# Live Experiment: Limitations

1. **Not executed.** There is no credential and the design inputs are undecided. Every statement about live behaviour remains a hypothesis.
2. **Frozen parameters from one fold.** The live path uses one outer fold's fit, and which fold is a design decision. No fit uses all recorded data, and refitting on live data is excluded by design.
3. **Same features as the pilot.** x^ctx^₁ (the injection classifier) is absent, and x_act1 remains close to an oracle for the attacker IBAN of this benchmark. Live agents do not change that structure, because the injection text is the benchmark's.
4. **Reviewer.** Only the two bounds are available. A live human reviewer is not modelled.
5. **Labels.** Reference matching (v1 references) carries the user_task_15 issue of older suite versions only if such a version is chosen. The human audit is still pending.
6. **AgentDojo re-query behaviour** (L-1) can repeat the episode loop up to three times. This is benchmark behaviour, recorded rather than altered.
7. **Adaptation counts** are descriptive (L-2). A replan is not necessarily a deliberate evasion.
8. **Statistical dependence.** Repeats of one cell are not independent observations. The bootstrap groups by injection task and user task.
9. **Smoke test.** The scripted ground-truth agent never adapts and is not a model of an LLM agent. Its counts are not results.
10. **Sandbox only.** Production payment systems, latency of the LLM call and real users are outside the scope.
