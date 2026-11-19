# 01 REM baseline verification (19 November 2026)

**Branch:** `claude/rem-melon-comparison-20261119`, created from `f4ff23f`, which is the tip of `claude/rem-final-thesis-completion-20261119`.

**Thesis status.** R8 is **unchanged** on this branch. `git diff f4ff23f HEAD -- REM_FINAL_THESIS_COMPLETION_2026_11_19 REM_FINAL_SUBMISSION` is empty.

## Commits (checked with `git log` and `git merge-base --is-ancestor`)

| Id | Full hash | Date | Role | Ancestor of this branch |
|---|---|---|---|---|
| `48bef90` | 48bef90b64bcf6f549aa4bce4e02c1e34529b647 | 2026-10-27 | Pilot design declared before any run (`configs/exploratory/pilot_e0.yaml`) | yes |
| `ea621c3` | ea621c379113c590db61d3eb9ece926c7c4602c2 | 2026-11-01 | Frozen pilot pipeline (complete-call timer) | yes |
| `9fddfa7` | 9fddfa748a4eb036f200206e874413147bf237b5 | 2026-11-03 | REM v1.0 code (`rem/`) as approved | yes |
| `dc8407d` | dc8407d2c74b3d6865607789d901c27e3b26f60f | 2026-11-19 | R8 protocols frozen; reproduction gate passed | yes |
| `f4ff23f` | f4ff23f0853e855f17b49295a2d8f4b2e63a63b9 | 2026-11-19 | R8 thesis and deliverables (reported commit verified) | yes |

## REM v1.0 code

**What changed since `9fddfa7`.** `git diff --stat 9fddfa7 f4ff23f -- rem/` reports three added files and no modified file:
- `rem/deployment/__init__.py` (empty);
- `rem/deployment/gateway.py`;
- `rem/integration/melon_rem.py`.

None of them is on REM's decision path.

**Reproduction.** On 19 November, a fresh run of the frozen pilot reproduced the published REM v1.0 counts exactly: 11 / 2,979, 105 / 334 and 1,083 / 2,979 (R8, `REM_FINAL_THESIS_COMPLETION_2026_11_19/results/reproduction_gate.json`).

## The REM artefact used in this comparison

A live closed-loop run cannot use the replay state directory. It uses the **frozen REM bundle**, `experiments/melon_rem/frozen/frozen_rem_bundle.pkl`:
- **sha256:** `983c5b0d54de01cdb37467526f3aea2c4065f888f59c140ea6714ec1b0d3e2c5`;
- **export:** exported on 5 Nov 2026 at commit `9fddfa7` from the frozen cross-fit state, with crossfit sha256 `27464b4d…` and rmod sha256 `29c2c78e…`, and with `pilot_e0.yaml` sha256 `8e1aa107…`, the same configuration hash as R8. Nothing was refitted.

The bundle holds, per outer fold:
- the ridge LR and calibration scorer;
- the benign reference;
- `A3_step_level`, the frozen expected-loss policy.

It also holds the predeclared assignment of each benign user task to a fold.

**Live policy.** For an attacked case, REM uses the fold that held out that case's injection task. This is the held-out cross-fit assignment, identical to the replay. A benign case uses the bundle's assignment. REM runs with step-level mitigation, no reviewer, and labels used for the audit only. This is REM v1.0 as frozen; **no algorithm, threshold or cost was changed.**

## What R8 already reports that matters here

- **External comparison** (R8, Section 4.4.2). The four distributed defences were compared through their recorded runs, against a replay of REM. That comparison is descriptive.
- **MELON in R8.** MELON was NOT EXECUTED, and R8 file 08 gives the reasons.
- **Reuse of the benchmark.** The primary banking population, 3,313 episodes, is **development data**: REM v1.0 was designed on it. A live run on the same 16 user tasks and 9 injection tasks is therefore **not an independent holdout**. That limitation is restated in `06`.
