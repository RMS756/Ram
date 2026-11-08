# Proposed thesis change log (none applied)

| ID | Chapter | Change | Evidence | Requires supervisor decision? |
|---|---|---|---|---|
| M-1 | 3 | Add the runtime-context statement (what REM does and does not observe) | `03_AUTHORIZATION/REM_ARGUMENT_INTEGRITY_ANALYSIS.md` | No (descriptive) |
| M-2 | 3 | Define provenance, authorization and integrity separately | same | No |
| M-3 | 3 | State the number-matching behaviour and the comma-grouped decimal deviation | `tests/test_authorization_audit.py` (xfail), corpus check (0 / 825 texts) | No to describe; **Yes** to correct |
| M-4 | 3 | Note that x^beh_3 encodes action type | `logs/corpus_diagnostics.json` (85% / 84%) | No |
| M-5 | 3 | Closed-form Allow boundary C_esc / C_miss(k); Block unreachable at tier 3 | `logs/decision_regions_fold0.txt` | No |
| M-6 | 3 | Escalate vs Block reporting rule | `02_DECISION_TRACING/REM_VERDICT_SEMANTICS.md` | No |
| M-7 | 3 | Limitation: unrequested or invented arguments | `03_AUTHORIZATION/REM_AUTHORIZATION_MATRIX.md` | No |
| I-1–I-5 | Impl. | Exact commit and hashes, tracer, harness, reproduction commands, status of the candidate arms | `01_VERSION_AND_REPRODUCTION/*` | No |
| R-1 | 4/5 | Reproduced counts table incl. idealized-reviewer bound | `logs/reproduced_e4_e5_enforcement_replay_summary.json` | No |
| R-2 | 4/5 | Where legitimate actions are withheld | `logs/corpus_diagnostics.json` | No |
| R-3 | 4/5 | Fixture counts (no rates) | `03_AUTHORIZATION/REM_16_FIXTURE_RESULTS.csv` | No |
| R-4/R-5 | 4/5 | Candidate and sensitivity results, marked implementer-reported | Codex report | No (reporting); **Yes** for any adoption |
| D-1–D-6 | 5/6 | Discussion of withholding, authorization, substitution, provenance, usability, validity | all of the above | No |

**Wording to remove or avoid anywhere in the thesis:**
- "REM blocks argument substitution";
- "REM distinguishes authorized from unauthorized payments";
- "the parser / gating improved REM";
- any MELON result;
- "live";
- "validated on blind or independent test cases";
- "Platt calibration" without the label-NLL qualifier.
