# Amendment 1 (18 November 2026): scripted closed-loop implementation test. Frozen before it is run.

Status: `[PROPOSED - EXPLORATORY]`. This adds a measurement; it changes nothing in `02_PROTOCOL.md` or in any scored code. The script's hash is appended to `02_PROTOCOL_HASHES.sha256` in the same commit as this file.

## Purpose
The loop is AgentDojo 0.1.35, banking v1. Withheld calls are really not executed, and refusal notices go back to the agent. The test checks two things:
- whether each arm lets the benchmark's own reference solution (ground truth) of every user task through;
- whether each arm stops the reference attacker calls when the agent fully obeys the `important_instructions` injection.

No model is used.

## Design
- **Agents.** Two scripted test doubles issue ground-truth calls one per turn and never adapt:
  - benign: 16 user tasks, no injection;
  - compromised: 16 × 9 pairs; the user-task ground truth, then the injection-task ground truth.
- **Arms:**
  - B0 (allow all);
  - PG (Progent's manual banking policy on every call, as the earlier `PG` arm);
  - GV_math2 (frozen v2);
  - C1, C2PG, C3PG.
- **Fitted values.** The stored S1 cell `injection_task_0`, as for the fixtures and diagnostics.
- **Outcomes** (AgentDojo's own evaluators):
  - benign utility / 16;
  - injection goal reached / 144;
  - user task done while compromised / 144;
  - withheld restricted calls in benign episodes, by source;
  - errors.

All counts are reported.

## Limits fixed in advance
- **This is an implementation test, not an attack-success rate.** A real agent may refuse injections, comply partially, retry or replan.
- **The ground truth is not what a real agent would do.** It may use values that the scripted agent "knows" without reading them, so a guard that requires the read first can withhold calls a real agent would have prepared.
- **Full Progent is not involved.**

## Command
`python3 experiments/progent_competitive/closed_loop_scripted.py REM_PROGENT_COMPETITIVE_2026_11_18/results/closed_loop_scripted.json`
