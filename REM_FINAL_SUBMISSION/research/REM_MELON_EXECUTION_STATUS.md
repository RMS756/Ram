# MELON and MELON + REM: execution status

**Date:** 11 November 2026. **Status: implementation-verified, effectiveness-unevaluated.** No real-model experiment has been run.

## 1. What exists

| Item | Location | State |
|---|---|---|
| Upstream MELON | `kaijiezhu11/MELON` at commit `4d3cc9c`, cloned outside the repository on 5 November; unmodified; not vendored (no licence file) | Present in the current container at `/home/user/upstream/MELON` with its environment (`/home/user/venvs/melon029`); both are outside the repository and are lost when the container is reclaimed |
| Integration | `rem/integration/melon_rem.py` | MELON constructed as in its README; the two pipelines differ only in the tool executor (plain versus REM-gated) |
| Frozen REM | `experiments/melon_rem/frozen/frozen_rem_bundle.pkl`, sha256 `983c5b0d…` | Unchanged; re-checked today |
| Runner, spending guard, budget estimator, analysis | `experiments/melon_rem/` | Fail-closed: exits without a complete configuration, credential, or spending cap |
| Protocol | `experiments/melon_rem/MELON_REM_EXPERIMENT_PROTOCOL.md` | Paired, interleaved, seed-controlled; 26-episode pilot, 320-episode full run |
| Tests | `tests/test_melon_rem_integration.py` (22), `tests/test_melon_rem_offline.py` (8) | 30 passed on 5 November in the MELON environment (AgentDojo 0.1.29), with **scripted agents, a deterministic fake embedding client and a fake provider** |

## 2. What the tests show and do not show

They show that the integration is mechanically correct: MELON's code runs unchanged; REM is invoked only for calls MELON passes; withheld calls are not executed; allowed calls execute once; state does not leak between episodes; labels cannot influence decisions; errors are classified separately.

They show nothing about effectiveness. A scripted agent and a fake embedding client are not a language model. **No security or utility figure for MELON or MELON + REM exists in this project.**

## 3. Feasibility of a real-model run today

| Requirement | Status on 11 November |
|---|---|
| Model API credential | None in the environment |
| Embedding API (MELON's detector needs `text-embedding-3-large`) | None; `api.openai.com` is blocked in this session |
| Approved spending limit | None. The candidate's instruction: no spending on model APIs without an approved budget |
| Backbone, temperature, repeats, timeouts (design inputs M-2, M-3) | Not decided |
| Pinned versions | Available: AgentDojo 0.1.29 for MELON; upstream commit `4d3cc9c` |
| Common banking configuration for all conditions | Defined in the protocol |

**Verdict: not feasible.** Three independent blockers (credential, network, budget), two of which are decisions that only the candidate and supervisor can make.

## 4. Conditions that would be compared, if authorised

B0 (no defence), B1, original REM, original MELON, MELON + REM; same model, tasks, attack exposure and evaluation protocol; model calls, tokens and cost recorded by the spending guard.

Version constraint to resolve first: MELON's upstream code requires AgentDojo ≤ 0.1.29, while REM's replay results use 0.1.35. A live comparison would run every condition on 0.1.29.

## 5. How MELON is treated in the thesis

- Published MELON figures (ICML 2025; GPT-4o, all suites: benign utility 68.04, utility under attack 32.91, ASR 0.95) are cited as the authors' results under their conditions.
- They are **not** placed in a table or ranking with REM's replay numbers.
- The integration is described as implemented and verified with scripted agents, and as unevaluated.
- Recorded outcomes of other defences in the AgentDojo repository (Chapter 4, distributed defences) are reported as recorded by the benchmark authors, not as runs of this project.

## 6. Decision requested

Authorise a credential and a spending cap for the 26-episode pilot (decision D-15 and item D8 of the supervisor memo), or confirm that the thesis is submitted with MELON unevaluated. The thesis does not wait for this decision.
