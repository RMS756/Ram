# Implementation chapter: proposed updates

## I-1 Exact evaluated code and artifacts (new table)

| Item | Value |
|---|---|
| REM code for all reproduced results | commit `9fddfa7`; byte-identical in every executed file at `cfb4f40` (only a standalone script was added) |
| Configuration | `configs/exploratory/pilot_e0.yaml`, sha256 `8e1aa107…` (exploratory declared values; not supervisor-approved) |
| Fitted state | `crossfit.pkl` sha256 `27464b4d…` and `rmod.pkl` sha256 `29c2c78e…`; a fresh refit on 8 Nov 2026 reproduced both byte for byte |
| Frozen bundle | `experiments/melon_rem/frozen/frozen_rem_bundle.pkl`, sha256 `983c5b0d…` (unchanged) |
| Environment | Python 3.11.17, numpy 2.4.6, agentdojo 0.1.35, AgentDojo runs `089ed468…`, seed 20261027 |

## I-2 Diagnostic instrumentation (new subsection)

> A read-only tracer (`REM_AUTHORIZATION_AUDIT/tools/trace_fixtures.py`) replays synthetic call-level fixtures through the frozen components without refitting: it records the feature vector, raw logit, raw and calibrated probability, tier, the conditional risk of every feasible verdict, the chosen verdict, its source (predicate or expected loss) and the enforcement effect, and recomputes logit, probability and argmin independently of the policy object (0 mismatches over 32 calls).

`REM_AUTHORIZATION_AUDIT/tools/corpus_diagnostics.py` recomputes the corpus counts from per-episode replay outcomes and profiles legitimate and attack value transfers.

## I-3 Fixture execution procedure (declared harness)

State harness assumptions H-1 to H-5 from the tracer's docstring:
- trusted context = system prompt + objective;
- `read_file` proposed first, its output ingested as untrusted;
- the legitimate and unsafe calls scored against the same state;
- step-level mitigation with no reviewer;
- fold `injection_task_0`, with all nine folds reported as a sensitivity check.

## I-4 Reproduction instructions

```bash
cd experiments/pilot
export PILOT_RESULTS_DIR=<dir> PYTHONHASHSEED=0
python3 build_dataset.py && python3 e0_pilot.py && python3 run_main.py crossfit rmod replay
cd ../..
PILOT_RESULTS_DIR=<dir> python3 REM_AUTHORIZATION_AUDIT/tools/corpus_diagnostics.py <out>
python3 REM_AUTHORIZATION_AUDIT/tools/trace_fixtures.py <out>
python3 -m pytest -q          # 236 passed, 1 skipped, 1 xfailed (8 Nov 2026)
```

## I-5 Candidate arms

> The request-cue, parser and gating arms were implemented and run by a separate implementer; their reported commit (bb4218d) was not available in the project repository at the time of the audit, so they are reported as implementer-reported exploratory results and were not reproduced.
