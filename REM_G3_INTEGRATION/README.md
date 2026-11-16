# G3 and L4 inside REM: isolated integration experiment

This experiment keeps the original five-layer architecture and all frozen modules unchanged. `experiments/g3_integration/guard.py` composes request-derived permission evidence with an existing `RemGuard` decision callback. It uses no task identifier, injection identifier, evaluation label or recorded success outcome. These remain evaluation bookkeeping in the unchanged replay harness.

The protocol and its pre-scoring clarifications are in `PROTOCOL.md`, committed at `0ff1cea`, `cafc41c` and `394fccc`. The implementation was committed at `5ff440c` before replaying candidates. Baseline aggregate outcomes were already known. This is development evidence, not a new confirmatory study.

## Candidates

H10 and H11 require full G3 support, then consult the original REM v1.0 or v1.1 four-verdict engine. H11D retains that full permission gate but restricts expected-loss choices to Allow and Block, keeping D1/D2 overrides. These candidates test the cost of adding both barriers in series.

HR routes permission-supported calls to Allow, permission-denied calls to Block, and incomplete authority to Escalate. D1/D2 remain enforced. Only remaining value uncertainty with established authority can affect the decision through the same F4 model and two-verdict policy as L4. There is no second learned model, new equation, retuned threshold or new cost matrix. The model score is computed for audit on every call, but is not used to decide a permission override. SHAP is computed after the verdict and never changes it.

HR adapts the earlier L2s routing pattern to revision-3 permission evidence. No claim that the routing pattern or constituent algorithms are newly invented is made. Whether this measured composition supports a thesis contribution requires independent validation and supervisor review.

G3, L4, REM10, REM11, A2 and the pinned Progent manual banking policy are reproduced as comparators. PG is an adaptation of that policy; it is not the full LLM-generated/dynamically updated Progent framework and does not reproduce the paper's original experiment.

## Reproduction

Use Python with the project's dependencies, pytest, and AgentDojo 0.1.35. The fitting procedure and its numerical settings are imported unchanged from `experiments/authz_study/study.py` and `configs/exploratory/pilot_e0.yaml`.

Set `AGENTDOJO_RUNS` to the runs directory of ethz-spylab/agentdojo at `089ed468cf3ed0322acc66b0211f26d9d90dbf60`, with the primary pipelines and the former confirmatory recordings specified in the original protocols. Set `PROGENT_UPSTREAM` to a clone of sunblaze-ucb/progent containing `9befb41cbf992b49dbf035cbd3d53eb953d3b351`. Only the two pinned source files are read as data. Set `PILOT_RESULTS_DIR` and `INTEGRATION_STATE` to new cache directories outside the repository.

From the repository root, run:

```bash
python experiments/pilot/build_dataset.py
python experiments/g3_integration/run.py prepare
python experiments/g3_integration/run.py fit
python -m pytest tests/test_g3_integration.py
python experiments/g3_integration/run.py replay
python experiments/g3_integration/run.py report
```

`prepare` checks eligibility and the original population hashes; `fit` regenerates models without candidate-specific changes and checks the original S1 coefficients; `replay` executes every call sequentially in fresh simulated banking environments; `report` checks that all reference-arm aggregate outcomes reproduce the stored revision-3 results. No live LLM or paid API is invoked. The replayed agent follows recorded calls and does not adapt to refusals.

`fits.json` stores every fitted coefficient and calibration parameter. `results.json` stores counts, predeclared paired cluster intervals, per-user-task results, the identifier probe and known fixtures. `episode_outcomes.jsonl.gz` stores outcomes for every replay (gzip-compressed JSON Lines). Logs and `tests.xml` record execution and verification. Intermediate pickle files are locally generated caches and are not committed.

Latency is a local diagnostic that includes attribution/audit and evaluation bookkeeping, not a deployment benchmark or evidence that the candidate is faster than the full Progent framework. Fixture performance is regression evidence; all requests and their earlier defects were already known.

## Disclosed post-scoring value-guard follow-up

The complete first-stage results were examined before this follow-up. L4 and HR released unsafe calls in known fixtures SUB-A4 and F2. `FOLLOWUP_VALUE_GUARD_PROTOCOL.md` was committed at `370cc55`, and its implementation at `06b0964`, before HV replay. HV adds an independent limited-grammar direct amount constraint to the unchanged L4 decision, keeping its fits and costs. It refuses a doubled amount when the request directly specifies 27.35 and withholds an ambiguous 1,250 rather than choosing a locale. It preserves state tracking even when it vetoes a proposed release.

Run `python experiments/g3_integration/followup.py replay` and `python experiments/g3_integration/followup.py report` with the same environment. The separate outputs are `value_guard_results.json` and `value_guard_episode_outcomes.jsonl.gz`; the original results are retained. The final test log covers both stages and replaces earlier verification logs. See `RESULTS_AND_DESIGN.md` for all results, limitations and the negative superiority verdict. The HV callback uses the existing L4 scorer implementation; expanded SHAP attribution for HV was not enabled or evaluated. No interpretability improvement is claimed from this run.

## Published comparator context

[Progent v3, 14 May 2026](https://arxiv.org/html/2504.11703v3) uses deterministic tool-call policy enforcement, LLM-based policy generation/update, and SMT checks to distinguish privilege narrowing from expansion. This experiment implements no SMT proof and measures none of Progent's generated policy modes. The candidate's proposed focus is typed financial authorization with bounded learned decisions. A higher point estimate against the manual policy must not be described as superiority over the full framework.
