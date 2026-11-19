# 12 Limitations and threats to validity (final, 19 November 2026)

The thesis states these in Chapter 4, Section 4.6.11 and Chapter 5, Section 5.6. This file consolidates them for the supervisors, with the limitations specific to the final experiments marked **[new]**.

## Internal validity

1. **Replay, not enforcement (NO-ADAPT).**
   - Every REM result assumes the agent emits its recorded calls whatever REM withholds. A live agent can retry, rephrase or route around a refusal.
   - Replay ASR is therefore not an upper bound on live ASR, and replay utility loss is not a measured live loss.
   - Residual attack success after Modify is close to zero by construction.
2. **Development data.**
   - The primary population (3,313 episodes) was used to design REM v1.0 and has been analysed many times.
   - The final ablation and the external replays are development evidence.
   - Only the confirmatory run of 11 November (2,113 episodes) was unread at the time.
3. **[new] Pilot outcomes known before the final ablation.** The outcomes of arms A1, A2, A3, A4a, A4b and A7 were known before the final protocol was written. Only A5, A6 and the reachability, latency and calibration analyses were new.
4. **[new] Amendment 05a.**
   - The external runner crashed on the tool_filter set.
   - The amendment was committed before any outcome was read.
   - It excludes a replay set rather than changing a metric.
5. **Labels.** They are reference-matched attempt labels, not audited by a human, and ambiguous for user_task_15 in early benchmark versions.
6. **Reviewer.** The headline results use no reviewer, which makes Escalate, Modify and Block release-equivalent. The value of a human reviewer is not measured.

## Construct validity

7. **Undesigned Detection Layer.** No injection classifier was available, so the Detection Layer's classifier input is absent.
8. **Proxy for state changes.** "Attack-labelled calls released" counts released calls. Unauthorised state change is measured only through AgentDojo's security check.
9. **[new] Precision of "withhold".** It counts withheld calls of the user's own task in attacked episodes as false positives. This is a conservative reading.
10. **Calibration metrics.** They are computed on dependent steps, without intervals.

## Statistical conclusion validity

11. **Few clusters.** 9 injection-task clusters and 16 user-task clusters. Percentile bootstrap intervals may under-cover, so "interval excludes 0" is a pre-registered decision rule, not a guaranteed-level test.
12. **Multiplicity.** No family-wise adjustment.
13. **One run per configuration.** Recorded runs and replays are single runs. No repeated stochastic runs exist.
14. **Zero events.** These are reported with the rule of three, never as "secure".

## External validity

15. **One benchmark.** AgentDojo banking: 16 user tasks, 9 injection tasks, one attacker account. The results may not transfer to other suites, domains or real banks.
16. **[new] External defences: one model, recorded once.**
    - They were recorded with gpt-4o in June 2024, and the run files carry no suite version.
    - REM was not run with that model in a closed loop.
    - The comparison is descriptive.
17. **[new] tool_filter not replayable with the frozen harness.** The layered "tool_filter + REM" result is missing.
18. **[new] MELON not executed.** It needs a model endpoint, an embedding endpoint and an authorised budget.
19. **Design status.** Costs, tiers, predicates, features and the label rule are declared values that await supervisor approval. All results are exploratory by label.

## Metrics that cannot be estimated reliably here

| Metric | Why |
|---|---|
| Live ASR / utility | No closed-loop run |
| Residual attack success after Modify against an adaptive agent | NO-ADAPT makes it about 0 by construction |
| Successful authorised refunds | The banking suite has no refund tool |
| Inference cost | REM calls no model; the cost of an LLM-based comparator was not measured |
| Deployment latency | Only replay timings in a shared container. They differ between runs (0.149 ms today vs 0.21–0.28 ms in R4, median). |
| Per-category ASR for REM | 0–4 successes per injection task: too few for rates |
