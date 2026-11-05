# Research Gap Validation

**Gap as stated in the thesis** (§1.4, §2.13): no prior work evaluates the following together, on an open, executable banking benchmark under indirect prompt injection, against a same-estimator baseline:
- a calibrated per-call probability of adversarial inducement;
- consequence-tiered expected-loss verdicts over four actions;
- deterministic mitigation;
- an audit record.

| Element | Prior work that has it | Validated? |
|---|---|---|
| Runtime interception at the tool boundary | Many (Task Shield, MELON, ProvenanceGuard, AgentTrust, NEXUS, FinHarness …; thesis Table 2.5) | Not a gap |
| Financial domain, inline per-step monitoring | FinHarness [P] | Not a gap |
| Calibrated risk score with loss-optimal thresholds | NEXUS [P, partly verified] | Not a gap in isolation |
| Graded verdicts including escalation | FinHarness (to an LLM judge), AgentTrust, LATTICE (to a human) [P] | Not a gap in isolation |
| **The combination**, on an **open** banking benchmark, with a **same-estimator** comparison isolating the decision rule | None found at record level (systematic review plus two searches on 5 Nov 2026) | **Plausible but narrow.** Not exhaustive; no full texts read |

**Conclusion.** The defensible gap is a *combination and evaluation* gap, as the thesis already states. It is not a mechanism gap and not a "first framework" gap. The new evidence of 5 Nov 2026 strengthens the internal part of the claim:
- the decision rule, not calibration, drives REM's difference from a threshold policy on the same estimator (REM-Lite ≡ B1);
- REM runs as a separate service without changing any decision.

It does not strengthen the external part (comparison with published defences), because MELON was not executed.
