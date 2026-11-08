# Experiment provenance

| ID | Experiment | Who ran it | Code | Data | Kind | Reproduced here? |
|---|---|---|---|---|---|---|
| E-PRIM | Original REM, B0, B1, REMnoEsc, idealized reviewer | Claude, earlier sessions; rerun in this audit | `9fddfa7` ≡ `cfb4f40` | 3,313 eligible recorded episodes (AgentDojo runs `089ed468`) | offline recorded-trace replay, step-level | **Yes**, exact |
| E-2x2 | Request cue × {expected loss, no-discretionary Escalate} | Codex | not provided | same corpus | offline replay | No (code missing) |
| E-UT | Leave-whole-user-task-out sensitivity | Codex | not provided | same corpus, user-task folds | offline replay | No (code missing; the repo has user-task grouping for probabilistic metrics only) |
| E-PARSER | "Exact numeric provenance (complete English Decimal amounts)" | Codex | reported `bb4218d` | same corpus | offline replay, post hoc | No |
| E-GATE | Suppress privilege-rise / transition-novelty contributions without corroborating context/action evidence | Codex | reported `bb4218d` | same corpus | offline replay, post hoc | No |
| E-FIX1 | Fixture set 1 (8 substitution probes) | Codex scored; Claude re-ran original REM | frozen bundle `983c5b0d…` | `../fixtures/set1_substitution_fixtures.json` | synthetic call-level probes | Original REM: yes (same pattern: 0/8 legitimate, 0/8 unsafe released) |
| E-FIX2 | Fixture set 2 (P1–P6, R1–R2) | Codex scored; Claude re-ran original REM | frozen bundle | `../fixtures/set2_fresh_fixtures.json` | synthetic call-level probes | Original REM: yes (only the two `get_balance` calls released) |
| E-AE | Logical cases A–E | this audit | frozen bundle | `../fixtures/logical_cases_A_to_E.json` | synthetic probes | n/a (new diagnostic) |

## Fixture provenance and limits

- Both fixture sets were written by one author (Claude) who knew the purpose of the test. They are copied verbatim from this project's conversation.
- Codex's copies may differ in serialisation, and Codex's harness context (system prompt, file name in `read_file`, number formatting of `amount`) is not available.
- The harness used here is declared in `../tools/trace_fixtures.py` (H-1 to H-5).
- They are 16 diagnostic probes. They are **not** an independent, representative or blind validation set. Report counts only, with no rates or confidence intervals.

## Run records kept

| What | Where |
|---|---|
| Commands | `REM_BASELINE_REPRODUCTION.md` |
| Commit SHA | `../logs/trace_meta.json` (`rem_commit`) and the replay provenance in `../logs/reproduced_e4_e5_enforcement_replay_summary.json` |
| Python and dependency versions | as above |
| Input hashes (fixtures, bundle) | `../logs/trace_meta.json` |
| Configuration hashes | `REM_SCORED_COMMIT_AUDIT.md` |
| Seed | pilot_e0 `meta.seed` = 20261027 |
| Execution logs | `../logs/` |
| Failures | the first reproduction attempt stopped because `e0_pilot.json` had not been produced (crossfit reads it). It was rerun with `e0_pilot.py` first. No other failure. |
