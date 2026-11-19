# 08 MELON: feasibility report (status: NOT EXECUTED)

## Verified facts (19 November 2026)

| Item | Finding |
|---|---|
| Paper | Zhu, Yang, Wang, Guo, Wang. *MELON: Provable Defense Against Indirect Prompt Injection Attacks in AI Agents.* ICML 2025, PMLR 267, pp. 80310–80329 (arXiv:2502.05174). Verified earlier by OpenAlex and PMLR (`REM_ARCHITECTURE_REDESIGN_STUDY_2026_11_18/results/literature_verification.json`). |
| Official implementation | `kaijiezhu11/MELON`, commit `4d3cc9c` (README + `pi_detector.py`). Present in this container at `/home/user/upstream/MELON`, unmodified, outside the repository. |
| Mechanism | Masked re-execution: the agent is run a second time with the user task replaced by a neutral task, and the tool calls of the two runs are compared by embedding similarity. A call that also appears under the masked task is treated as injection-driven, and the run is stopped. |
| Requirements | An LLM for the agent; a **second agent run per step** (the masked run); an embedding model (`text-embedding-3-large` in the README); AgentDojo ≤ 0.1.29. REM's evaluation uses 0.1.35. |
| Integration in this project | `rem/integration/melon_rem.py`: MELON constructed as in its README, plus a MELON+REM variant in which REM gates the calls MELON lets through. It was tested on 5 November with scripted agents, a fake embedding client and a fake provider: 30 tests passed in the MELON environment (`/home/user/venvs/melon029`, AgentDojo 0.1.29). |
| Recorded runs | AgentDojo's `runs/` contains **no** MELON pipeline. No recorded outcome exists to read. |

## Why it was not executed

| Requirement | Status today |
|---|---|
| Model endpoint for the agent | none. 127.0.0.1:8000 and 127.0.0.1:11434 are not running, and no experiment key is configured. |
| Embedding endpoint | none |
| Authorised spending cap | none ("do not spend money using external APIs without explicit authorization") |
| Backbone, temperature, repeats | not frozen (design lock) |

**MELON cannot run offline on recorded traces.** Its decision needs a *new* masked agent run, which a replay cannot produce. A replay-based "MELON" would therefore be a different method, and it is not built under MELON's name.

## Cost implications (for a future authorised run)

- **Model calls.** MELON roughly doubles agent model calls: the original plus the masked run at every step, plus one embedding call per tool call.
- **Experiment size and budget.**
  - A paired experiment needs B0, REM, MELON and MELON+REM on 144 attacked and 16 benign banking episodes, i.e. 4 × 160 episodes per repeat.
  - Token volumes per episode are measured in `REM_PROGENT_COMPETITIVE_2026_11_18/06_BUDGET_ESTIMATE.md` (about 21.5 k input characters per gpt-4o episode).
  - Prices must be entered by the operator. No price is assumed here.

## How MELON appears in the thesis

- The published MELON results (the authors' conditions: GPT-4o, all AgentDojo suites) are cited as the authors' results. They are **not** placed in a table with this project's measurements.
- The integration is described as implemented and tested with scripted agents, and **unevaluated**.

## Decision required `[SUPERVISOR DECISION REQUIRED]`

Either authorise a model endpoint, an embedding endpoint and a spending cap for the paired pilot (`experiments/melon_rem/MELON_REM_EXPERIMENT_PROTOCOL.md`), or accept the thesis with MELON NOT EXECUTED.
