# Status table (study of 18 November 2026)

Branch `claude/rem-progent-competitive-20261118`, created from `d52baa1`.

Commits:
- `bdde9d0`: design, code, tests and protocol frozen **before** scoring;
- `0009d09`: results and documents;
- `5e91233`: amendment 1 frozen before it was run;
- the following commit: amendment 1 results.

Environment: the study's `env.sh` (PYTHONHASHSEED=0; stored caches in the session scratchpad). No model call was made.

| Item | Implemented | Implementation-tested | Development replay | Independent validation | Live comparison | Notes / blocker |
|---|---|---|---|---|---|---|
| F1/F2/F3 reproduction on frozen v2 | yes | – | diagnostics (`results/f_before_v2.json`) | – | – | 8/58 unauthorized released by v2 arms |
| C1 contract guard (scope, witness, ledger, merge) | yes | yes (`tests/test_progent_competitive.py`) | yes | not executed | not executed | diagnostics 0/58 unauthorized, 50/62 authorized; AgentDojo identical to GV_math2 |
| C2[PG] | yes | yes | yes | not executed | not executed | = C1 on outcomes; 72 extra refusals |
| C3[PG] | yes | yes | yes (S1, S2) | not executed | not executed | = C2[PG] |
| P0 (full Progent: manual / generated / Auto-Deny / Auto-Approve) | adapter + configs | config/refusal tests only | – | – | **not executed** | upstream execution refused in session; no model backend; no spending cap |
| C2[gen], C3[gen] | harness | preflight tests | – | – | **not executed** | same blockers |
| Scripted closed loop (amendment 1; AgentDojo 0.1.35; ground-truth test doubles; no LLM) | yes (`closed_loop_scripted.py`, frozen in `5e91233`) | yes (`tests/test_progent_competitive_amend1.py`) | – | – | **implementation test only** | benign reference solutions 8/14 (PG 11/14); obedient-agent injection goals: C1 0/144, GV_math2 1/144, PG 0/144 (`11_SCRIPTED_CLOSED_LOOP_RESULTS.md`) |
| Human-approval configuration | – | – | – | – | **not established** | no reviewer exists |
| Parity of REM's replay checker with upstream `check_tool_call` | yes (`parity_upstream.py`) | gated test (skipped) | – | – | – | needs `REM_ALLOW_UPSTREAM_EXECUTION=1` where running upstream code is permitted |
| Validation kit (schema, sealed manifest, executable scorer) | yes | selftest + refusal path | – | **not executed** | – | no independent authors or reviewers |
| Budget | volumes measured | – | – | – | – | prices not computed: official pricing page unreachable; operator fills `prices_TEMPLATE.json` |
| MCP / LangChain portability | – | – | – | – | – | **not established** (optional; not attempted) |
| Superiority over full Progent | – | – | – | – | – | **not established** |
| Thesis draft for the candidate | – | – | – | – | – | **deferred**: no candidate is stable and evaluated in the closed loop; R1–R7 untouched |

## Commands

```
source env.sh                                   # PYTHONHASHSEED=0, PROGENT_UPSTREAM, caches
python3 experiments/progent_competitive/reproduce_f.py
python3 experiments/progent_competitive/cp_run.py replay
python3 experiments/progent_competitive/cp_run.py diag
python3 experiments/progent_competitive/cp_run.py report
python3 experiments/progent_competitive/budget.py --runs <agentdojo>/runs --pipeline gpt-4o-2024-05-13 --upstream <progent> --out REM_PROGENT_COMPETITIVE_2026_11_18/results/budget_volumes.json
python3 experiments/progent_competitive/validation_scorer.py --selftest
python3 -m pytest -q tests/test_progent_competitive.py   # 57 passed, 1 skipped (gated parity)
python3 experiments/progent_competitive/closed_loop_scripted.py REM_PROGENT_COMPETITIVE_2026_11_18/results/closed_loop_scripted.json
python3 -m pytest -q tests/test_progent_competitive_amend1.py   # 2 passed
sha256sum -c REM_PROGENT_COMPETITIVE_2026_11_18/02_PROTOCOL_HASHES.sha256   # all OK after scoring
```

## Full test suite

| Condition | Tests | Failures | Errors | Skipped (incl. xfail) |
|---|---|---|---|---|
| Without the study's state variables | 767 | 0 | 0 | 18 |
| With `env.sh` sourced | – | 1 | – | – |

With `env.sh` sourced, `tests/test_authz_study.py::test_intervention_value_rule_and_original_arm_on_a_direct_transfer` fails (`improve.py:141`, a missing loss policy). It passes on its own, and it fails identically with this study's test file excluded. It is a pre-existing interaction between that test and the cached state, not caused by this study, and it is not fixed here (frozen study code).

## Integrity checks
- Every file in `02_PROTOCOL_HASHES.sha256` verifies after scoring.
- `git diff d52baa1 -- rem/ configs/ REM_REPAIR_STUDY_2026_11_17/ REM_FINAL_SUBMISSION/ experiments/repair_study experiments/improve_study` is empty.

## Items for a later thesis edition (not applied; R7 untouched)
- **CLAIM_AUDIT_R7:** its title still says "sixth edition".
- **Section 4.5.4:** its opening describes the v1 stage order reversed.
- **PACT:** full author list "Fan, L., Li, Z., Tian, Y., Wang, Y., Li, R., & Wang, X. (2026)", as supplied in the review.
- **MELON:** PMLR vol. 267, pp. 80310–80329, confirmed in the review.
