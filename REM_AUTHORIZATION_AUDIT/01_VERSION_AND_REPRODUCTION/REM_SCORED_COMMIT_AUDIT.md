# REM scored-commit audit

Audit date: 8 November 2026. Auditor: Claude (code-grounded, read-only on all REM code). Audit branch: local `claude/rem-authorization-audit`, created from `cfb4f40`; not pushed.

## 1. Repository state at the start of the audit

| Item | Value |
|---|---|
| Branch checked out | `claude/melon-rem-extension` |
| HEAD | `cfb4f408b8d204a3015d5888d36fa59f65cd8e12` ("Review copy (6 Nov) …") |
| Working tree | clean (`git status --short` printed nothing) |
| Local branches | `claude/melon-rem-extension`, `claude/rem-algorithm-implementation-3ktvze`, `claude/rem-offline-validation-melon-prep` (squashed `d8799f9`, **push still pending your approval**), `claude/rem-r4-corrections-3ktvze` |
| Remote branches after `git fetch origin` | `claude/rem-algorithm-implementation-3ktvze` (181a38c), `claude/rem-r4-corrections-3ktvze` (9fddfa7), `claude/rem-thesis-lit-review-merge-j1px4f`, `claude/rem-thesis-revision-r2-j1px4f`, `codex/rem-ollama-pilot` (fca0319, new) |

Nothing was pushed, merged, rebased or force-pushed during this audit.

## 2. Commit `bb4218d`

**Not found.**
- `git cat-file -t bb4218d` fails ("Not a valid object name").
- `git log --all` does not contain the commit, and `git ls-remote origin` does not list it.
- The only Codex branch on GitHub, `codex/rem-ollama-pilot` (`fca0319`, 3 Nov 2026), is based on `9fddfa7`. It contains a local Ollama feasibility pilot and a refactor of `build_policies` into `build_fold_policies` in `experiments/pilot/run_main.py`. It has no request cue, no parser candidate and no gating code.

Consequences:
- The scored commit SHA for the request-cue, parser and gating arms **cannot be determined from evidence available to this audit**.
- Whether the parser-boundary unit-test correction happened after `bb4218d`, and whether it touched executable code or tests only, **cannot be verified**.
- Any claim that those arms were "frozen at `bb4218d`" rests only on Codex's report. Until the commit (or a bundle with its diff) is provided, the thesis should say "reported by the implementer; commit not available to the audit".

## 3. Exact commit of the original REM results (verified)

The original REM arm in this audit was reproduced at HEAD `cfb4f40` (working tree clean apart from new audit files).

`git diff --stat 9fddfa7 cfb4f40 -- rem/algorithms rem/core rem/integration/agentdojo_replay.py rem/integration/steps.py rem/integration/agentdojo_traces.py experiments/pilot configs` lists one file only: `experiments/pilot/ablation_minimal.py`, a new standalone script (+58 lines). It is not imported by the pipeline.

Every other file that defines features, the scorer, calibration, the decision rule, mitigation, replay or the configuration is byte-identical to `9fddfa7`. Between `9fddfa7` and `cfb4f40`, `rem/` gained `rem/deployment/gateway.py` and `rem/integration/melon_rem.py` (new files) and modified nothing.

## 4. Configuration and artifact hashes (sha256)

| Artifact | sha256 | Status |
|---|---|---|
| `configs/exploratory/pilot_e0.yaml` | `8e1aa107cf3ea0ba5eecbb92bc90a2463202cdde476cfe8a98047ffad74e11d0` | same as recorded in the frozen bundle |
| `configs/exploratory/pilot_e0_amendments.yaml` | `8c4f8fc07b4272189c137b1ecf4ae156c1c2297b8a7b3404f5d33bd03f34106f` | unchanged |
| `experiments/melon_rem/frozen/frozen_rem_bundle.pkl` | `983c5b0d54de01cdb37467526f3aea2c4065f888f59c140ea6714ec1b0d3e2c5` | **unchanged** (checked before and after; a test now pins it) |
| `state/crossfit.pkl` (fresh refit in this audit) | `27464b4d6c3752b5ad3be62e721b0264671c2ede85190fc611568cfe73b68b2e` | **byte-identical** to the hash the frozen bundle records |
| `state/rmod.pkl` (fresh in this audit) | `29c2c78ea5628783825e18699f321bc8d3e308ae8723a533d11dd99e59a88ba7` | **byte-identical** to the hash the frozen bundle records |
| `steps.pkl` (fresh in this audit) | `876211cdf4975568b0fe9b8f4fb1312471fd514c66f3dac283273ac28f792c5d` | — |
| `rem/algorithms/context/provenance.py` | `835949270ca8bce6fbe88acce44c724476ed2649dc1b8cfff81a5731e1d473ee` | identical to 9fddfa7 |
| `rem/algorithms/behavior/evidence.py` | `d4d14821aa12dabcb214c51331088ea5995bf8ac54554131f25dbbd2ed42f71a` | identical to 9fddfa7 |
| `rem/algorithms/a3.py` | `aeca631bb290e68b5ca5268cf9649f77cab0de8981c270ae2d38006745938678` | identical to 9fddfa7 |
| `rem/algorithms/decision/policy.py` | `9b95a75c656a8d97c4aa5903305b393d20083333ada0c9d0a4f1afc4d12638f7` | identical to 9fddfa7 |
| `rem/algorithms/decision/loss_matrix.py` | `7abda0ec1e00023e7404b778b174b4ac65ce8c7c5e1f5f5bdb4b93d8be4f0ffb` | identical to 9fddfa7 |
| `rem/algorithms/decision/expected_loss.py` | `896d00cf27d5ed4ad186445c1ddbeb01e057ceb64afba391d543ac7653d38287` | identical to 9fddfa7 |
| `rem/algorithms/decision/consequence.py` | `8c480d2a31f0274b3a33c64dcf18d5ee5eb266e8143abd08d69d55b57574e660` | identical to 9fddfa7 |
| `rem/integration/agentdojo_replay.py` | `3d545b4dcccf8982751b0b428b7022fc80892a4a1f6eb52c67d30bfda3b6849b` | identical to 9fddfa7 |
| `experiments/pilot/run_main.py` | `21acc3c5bbe823839f044aedfcb3872db7646fef243a2431b068c74aa456d3e2` | identical to 9fddfa7 |
| AgentDojo recorded runs | repository commit `089ed468cf3ed0322acc66b0211f26d9d90dbf60` | as declared in pilot_e0 |

## 5. Mapping of experiments to commits

| Experiment / arm | Code commit | Evidence | Status in this audit |
|---|---|---|---|
| Original REM, primary injection-task folds (11/2,979; 105/334) | `9fddfa7` ≡ `cfb4f40` for all executed files | fresh rerun; pickles byte-identical | **Reproduced** |
| REMnoEsc (no-discretionary-Escalate ablation; 11/2,979; 110/334) | same | fresh rerun | **Reproduced** |
| B0, B1, REM with idealized reviewer | same | fresh rerun | **Reproduced** |
| Request cue (2×2) | Codex, commit not provided | Codex report only | **Not reproducible here** (code unavailable) |
| Leave-whole-user-task-out enforcement counts (12/2,979, 110/334, etc.) | Codex, commit not provided | Codex report only | **Not reproducible here**. The repository computes user-task grouping only for discrimination and calibration metrics (`run_main.py:168-180`), not for enforcement replay. |
| Parser candidate | Codex, said to be `bb4218d` | Codex report only | **Not reproducible here**; see `../04_CANDIDATE_REVIEW/PARSER_CANDIDATE_REVIEW.md` |
| Gating candidate | Codex, said to be `bb4218d` | Codex report only | **Not reproducible here**. The fixture-level outcomes are *mechanistically consistent* with a simple re-expression (Exploratory Counterfactual, not adopted). |
| 16 diagnostic fixtures, original REM | frozen bundle `983c5b0d…` (exported at `9fddfa7`) | `tools/trace_fixtures.py` | **Re-run**; same release pattern as reported |

## 6. Evidence for the frozen-baseline claim

Supported for the original REM:
- the executable code is byte-identical to `9fddfa7`;
- the refit reproduces the frozen pickles bit for bit;
- 50 configurations of the enforcement replay match `results/pilot_R4/e4_e5_enforcement_replay.json` on every compared metric;
- the bundle hash is unchanged.

Not supported, and to be stated as such:
- any statement that the candidate arms ran on a byte-identical `bb4218d`;
- any statement that the parser-boundary fix was test-only.
