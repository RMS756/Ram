# Claim audit: sixth edition (17 November 2026)

Each claim that is new or corrected in R6 is listed with its evidence and its status. Statuses:
- **executed**: run and measured here;
- **implementation-tested**: code exists and passes tests; not evaluated on data;
- **development evidence**: measured on data that were inspected before;
- **not executed**;
- **not established**.

| # | Claim in R6 | Where | Evidence | Status |
|---|---|---|---|---|
| 1 | The frozen guard (G3, GV, HV, Cedar, provenance arm) accepts any amount for "send half of 100 to A" (C1) | 4.5.4, Table 4.18 | `defects_before.json`, `defects_after.json`; root cause in `DEFECT_REPORT_C1_C2_2026-11-17.md` | executed (proposed-call diagnostics) |
| 2 | GV's direct-value constraint reads the coefficient 25 as the amount in "send 25 percent of 200 to A" (C2) | 4.5.4, Table 4.18 | same | executed (diagnostics) |
| 3 | The typed verifier repairs C1 and C2 in G3_math, GV_math and HV_math, with and without injected text | 4.5.4 | same; 103 unit and property tests | executed; implementation-tested |
| 4 | No successful attack for the repaired arms on both populations, S2 and the probe | 4.5.4, Table 4.19 | `results.json` of the repair study | development evidence |
| 5 | The repair costs 95 (primary) and 159 (second) completed tasks, all in user tasks 3 and 11 | 4.5.4 | `outcome_changes` in `results.json` | development evidence |
| 6 | Those tasks were completed before by releasing an amount the request does not verify | 4.5.4 | request texts; frozen acceptance of mode *derived* | executed (code trace); the correctness of those amounts is known only from the benchmark's check |
| 7 | HV_math has the outcomes of GV_math on every cohort; the learned decision adds no measured value | 4.5.4, 4.6.9 | contrasts in `results.json` | development evidence; a positive value is **not established** and is not shown to be zero |
| 8 | No benchmark-labelled attack call reached the amount verifier or the learned decision | 4.5.3, 4.5.4, threat 18 | stage accounting | development evidence |
| 9 | ~~"What reaches it is legitimate work"~~ removed. Not attack-labelled is not authorized | 4.5.3, threat 18 | review item 1 | correction |
| 10 | Every learned or calibrated decision behind the guard matches GV **except NP01**, which loses tasks (1,526 and 1,383 against 1,532 and 1,386) | 4.5.3, 4.6.9, 4.6.10, 4.6.12, Chapters 1 and 5, abstract | competitive-study `results.json` | development evidence; correction (review item 2) |
| 11 | Equal episode outcomes are not equal call decisions (NP05 withholds 3 calls, GB 1) | 4.5.3 | `restricted_call_stages` | development evidence |
| 12 | G3 completes 132 benign primary tasks; GV and HV 147 | 4.6.12, Chapter 5, abstract | Table 4.13 | development evidence; correction (review item 3) |
| 13 | Delegated amounts (bill in a file; "the amount I usually pay") are released from injected text by every non-strict arm | 4.5.4, Table 4.20 | `residual_stage_diagnostics.json` | executed (diagnostics); not a rate |
| 14 | One legitimate fixture (P2) is withheld by the verifier's grammar | 4.5.4 | fixtures in `results.json` | development evidence (over-blocking) |
| 15 | GV_math vs the replayed Progent policy: no superiority and no equivalence shown | 4.5.4 | contrasts | development evidence |
| 16 | Request-derived argument checks are published (PACT, ROPE, CapLite) and are not a gap | 2.11.4, 2.11.5, Table 4.14 | index abstracts; ROPE repository | literature at abstract level (A); ROPE also R |
| 17 | Independent validation of the verifier | 5.7 (item 11) | `07_INDEPENDENT_VALIDATION_KIT.md` | **not executed** |
| 18 | Progent with generated, or generated and updated, policies | Table 4.14; supplement S-4.4.4 | `08_PROGENT_THREE_CONFIGURATIONS.md` | **not executed** (no credential, no budget) |
| 19 | The verifier as part of REM | Appendix B (SD-AMT) | — | **not established**: proposed, exploratory, no supervisor decision |

Statements that R6 does **not** make:
- that GV, GV_math or HV_math verify financial amounts in general;
- that derived-amount support improves utility on AgentDojo (no request uses a supported expression);
- that a learner adds security;
- superiority over, or parity with, Progent, PACT, ROPE or CapLite;
- that any supervisor decision has been made.
