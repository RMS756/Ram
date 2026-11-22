# 01a Amendments to the frozen protocol and runners

## Amendment 1 (22 Nov 2026, after the freeze at `09d49c0`)

**What happened.** The first execution of O4 (`run_live_comparison.py --mode scripted`) crashed in arm D1 with `KeyError: 'tool_call'` before writing any output.

**Cause.** The runner read REM's live message records with the key `tool_call`. `rem/integration/agentdojo_live._message_record` stores the called function under the key `function`.

**Fix.** One line in `run_live_comparison.py` changes `m["tool_call"]["function"]` to `m["function"]`. It only affects counting executed tool calls for the report.

**What is unchanged.**
- No arm, no defence configuration, no metric and no analysis.
- No REM file.

**Results seen before the fix.** O1, O2 and O5 had already run. O4 had produced no result.
