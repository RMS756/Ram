# Prospective evaluation protocol (sealed; not executed)

**Status:** sealed on 13 November 2026 with the development protocol, before any outcome of the new arms was computed. **Nothing in this file has been run.** It defines the evaluation that could support a confirmatory claim; the development results cannot.

## Why a new evaluation is needed

Every recording in the repository has been inspected. A confirmatory claim about the candidate needs outcomes that did not exist when the candidate was fixed.

## Blockers on 13 November 2026

| Requirement | Status |
|---|---|
| Language-model credential for the agent | none in the environment |
| Embedding service (MELON's detector) | none; provider host not reachable |
| Explicit spending authorization and cap | none; the standing instruction forbids spending without an approved budget |
| Design inputs: backbone, decoding, repeats, timeouts | undecided (register item D-15) |

## Design

- **Environment.** One version for every condition: AgentDojo 0.1.29, banking suite v1, the version required by the unmodified MELON code (upstream commit `4d3cc9c`). REM's arms are run in that same environment through the existing closed-loop executor; the replay results of the earlier studies (0.1.35) are not combined with it. Before the run, the eleven banking tools are checked to behave identically in 0.1.29 and 0.1.35 on the 16 ground-truth solutions.
- **Conditions (same backbone, tasks, attack payloads, decoding, tool limits, repeat protocol):** no defense; A2; G1; L2; Progent manual policy; MELON (unmodified); MELON followed by G1. Task Shield and Progent with generated policies are added only if their official code runs unmodified.
- **Attacks.** `important_instructions` on the 16 user tasks × 9 injection tasks, plus the benign runs. These are fresh rollouts of known tasks: they test new trajectories, **not** a new distribution of user tasks.
- **New task variants.** Fixture set 4 and at least 16 further request variants written and labelled by a person other than the author of the candidate, each with a legitimate and an unsafe call. Until that review exists the fixtures remain author-written stress tests.
- **Repeats.** At least three per cell, aggregated per (user task, injection task) before any interval; clusters are the 16 user tasks and 9 injection tasks.
- **Primary comparisons, fixed here:** G1 − A2 and G1 − Progent manual policy on benign task completion and on attack success; L2 − G1 on the same. Errors of the model or the infrastructure are reported separately and are never counted as prevented attacks.
- **Precision.** With 16 user-task clusters the interval of a task-completion difference is expected to be about ±10 percentage points wide or wider (the width seen on the recorded data). The run is therefore planned as an estimate with its uncertainty, not as a powered superiority test, and is to be described so.
- **Security wording.** No non-inferiority margin is approved. Attack-success differences are reported with intervals; no certified safety is claimed.
- **Budget.** The existing estimator (`experiments/melon_rem/estimate_budget.py`) and spending guard are used; embeddings, retries and output limits are included in the cap. A 26-episode compatibility pilot precedes the full run and is not a result.

## Dry-run commands

```bash
python3 experiments/melon_rem/run_melon_rem.py --config <config> --dry-run     # prints the paired schedule; no model call
python3 experiments/melon_rem/estimate_budget.py --config <config>             # budget from measured tokens and given prices
```
