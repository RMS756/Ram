# 05a Amendments after the freeze (dated)

## Amendment 1 (18 November 2026): runner bug in the fixtures stage
- **Defect.** `ctl_run.py stage_fixtures` (as frozen in `7f57865`) monkeypatched `repaired_arms_v2.make_guard` and `.ARMS`. Because `arms.build_cell` itself calls `repaired_arms_v2.make_guard`, the patch recursed (`RecursionError`). No fixture result was produced by the frozen version.
- **Change.** `stage_fixtures` now contains the loop of `rs_run_v2.fixtures`, line for line, with the arm factory passed in instead of patched.
  - The diff against `rs_run_v2.fixtures` was inspected: only variable names, the loop over this study's arms, and the output writing differ.
  - No decision logic, arm, case, label, metric or criterion changed.
- **Check.** The fixture counts for the frozen arms equal those of the earlier studies: GV_math2 7/0, 6/0, 3/0, 18/0; C1 7/0, 7/0, 3/0, 19/0; PG 0/0, 2/0, 1/0, 7/0 per set.
- **Hash.** `ctl_run.py` therefore differs from `05_PROTOCOL_HASHES.sha256`. Every other hashed file verifies (`logs/hash_check_after_runs.log`).

## Amendment 2 (18 November 2026): correction to the earlier closed-loop protocol (documentation only)
- `REM_PROGENT_COMPETITIVE_2026_11_18/05_CLOSED_LOOP_PROTOCOL.md` and `progent_upstream.CONFIGS` describe "P0_manual" in the fork at 0d7ea07 as Progent's manual banking policy ("PG historical").
- **This is incorrect.** Between 9befb41 and 0d7ea07 the manual-policy block was removed from `agentdojo/src/agentdojo/default_suites/v1/banking/task_suite.py` (29 lines; `git diff --stat 9befb41 0d7ea07`). In the pinned fork, SECAGENT_GENERATE=False therefore installs **no** policy, and upstream `check_tool_call` then allows every call with a warning.
- A faithful "PG historical" arm needs the 9befb41 policy installed explicitly, as `parity_upstream.py` and `parity_recorded_calls.py` do with upstream's own `update_security_policy`.
- The frozen files of the earlier study are not edited; this record supersedes their description.
