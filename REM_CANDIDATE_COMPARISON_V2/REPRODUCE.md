# Reproduction

[PROPOSED — SUPERVISOR APPROVAL REQUIRED]

Use the source branch `codex/rem-multiple-candidates-v2`. The preceding study documents installation and pinned AgentDojo trace extraction. This extension reuses the generated artifacts; it does not require a live model or bank.

```bash
# From repository root; paths here match the executed workspace layout.
export AGENTDOJO_RUNS=/workspace/work/agentdojo/runs
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
/workspace/work/venv/bin/python -u -m experiments.rem_candidates_v2.evaluate  --raw /workspace/work/reproduction/steps.pkl  --oracle-replays /workspace/work/aa_eval/fit/state/replay_rmod.pkl  --out /workspace/work/v2_eval_final
/workspace/work/venv/bin/python -u -m experiments.rem_candidates_v2.evaluate  --raw /workspace/work/reproduction/steps.pkl  --oracle-replays /workspace/work/aa_eval/fit/state/replay_rmod.pkl  --out /workspace/work/v2_eval_full_trace --complete-trace
/workspace/work/venv/bin/python -m experiments.rem_candidates_v2.diagnostics  --raw /workspace/work/reproduction/steps.pkl --results /workspace/work/v2_eval_final \
 --historical-rmod /workspace/work/reproduction/state/rmod.pkl
REM_STUDY_RAW=/workspace/work/reproduction/steps.pkl  REM_V2_RESULTS=/workspace/work/v2_eval_final REM_V2_FULL_RESULTS=/workspace/work/v2_eval_full_trace  /workspace/work/venv/bin/python -m pytest -o addopts='' -q -p no:cacheprovider  tests experiments/authorization_generalization/tests experiments/rem_candidates_v2/tests
```

Replace workspace paths on another machine. `steps.pkl` and the oracle replay pickle must be generated locally from the pinned upstream JSON; never load untrusted uploaded pickles. The original benchmark package is agentdojo 0.1.35 and the native suite here is v1.2.1. Python/NumPy were 3.12.14/2.3.5; the previous study archives the environment freeze. Original ridge grid and fitting code are unchanged; bootstrap seed is 20261112 (an explicit integer seed, not an execution date), 2,000 resamples, 95% intervals.

Artifacts include per-episode outcomes, source/protocol/input hashes, original-model coefficients/availability, actual split and residual-fitting memberships, paired metrics, task/objective strata, gzip-compressed decision audits, coverage diagnostics, full-trace sensitivity and test logs. The source hash manifest describes the code at its run; final source hashes are archived separately. Primary outputs use the original 15-round horizon. The full-trace sensitivity uses a trajectory-derived bound and reports any B0 record mismatch without silently dropping paired episodes.

Two engineering defects found before finalization were fixed and tested: no-tool episodes have no supervised fold and must not require an invented model; native backend receipt identity `me` must be resolved in the trusted adapter. The protocol's candidate decision rules were not tuned on outcome scores. Initial failure logs are retained for audit. The later complete-trace amendment is explicitly post-hoc and did not change any paired success outcome.

To reproduce the figure:

```bash
MPLCONFIGDIR=/workspace/work/mpl /workspace/work/venv/bin/python  -m experiments.rem_candidates_v2.figures  --metrics /workspace/work/v2_eval_final/metrics.json  --out /workspace/work/v2_frontier.png
```

The public artifacts omit the user's private pasted Claude transcript and contain only verified research findings/reconciliation. They preserve the original REM and previous AA study byte-for-byte.

Manifest metadata wording was corrected from `independent_episodes` to `distinct_episodes`; this changes no counts or outcomes and does not assert independent task pairings.
