# 04 MELON reassessment (22 November 2026)

## 1 Earlier work verified directly

| Item | Check on 22 Nov 2026 | Result |
|---|---|---|
| Branch `claude/rem-melon-comparison-20261119` | exists locally and on `origin` | VERIFIED |
| Commits `a1db36a`, `780c6f8` | present; `780c6f8` is the parent of the ablation branch | VERIFIED |
| `REM_MELON_COMPARISON_2026_11_19/` | 14 documents, results, logs, manifests | VERIFIED |
| Frozen protocol hashes | `sha256sum -c 06_PROTOCOL_HASHES.sha256`: all 12 entries OK, including the frozen REM bundle and upstream `pi_detector.py` | VERIFIED |
| Three-arm harness | `experiments/rem_vs_melon/harness.py` (D0 none, D1 REM v1.0, D2 MELON) | VERIFIED |
| Scripted integration pilot | 480 episodes (144 attacked and 16 benign, × 3 arms), 0 errors (`05_PILOT_EXECUTION_LOG.md`). **This is an integration test with a scripted agent and is not a security result.** | VERIFIED |
| Live comparison | **NOT EXECUTED** (`14_FINAL_EXECUTION_STATUS.md`) | VERIFIED |
| Tests | `tests/test_rem_vs_melon.py` in the MELON venv: **9 passed**, rerun today | VERIFIED |

## 2 Upstream state

- **Code:** `ucsb-mlsec/MELON@06014c7` and `kaijiezhu11/MELON@4d3cc9c`. After fetching on 22 Nov 2026, both heads are unchanged.
- **The file:** `pi_detector.py`, sha256 `5a7f6b28…a9017`, identical in both repositories.
- **Licence:** neither repository has a licence file, so the file is loaded by path and not vendored.
- **Paper:** ICML 2025 (PMLR 267), per the earlier audit. The paper itself was not reread today.

All VERIFIED.

## 3 Requirements and limits

| Requirement | Status |
|---|---|
| AgentDojo **0.1.29**: MELON assumes string message content | VERIFIED in the earlier audit. The 0.1.29 venv scores banking identically to 0.1.35 on reference solutions (`results/fingerprint_pypi_0129_melon_env.json`). |
| Embedding model `text-embedding-3-large` (OpenAI) | VERIFIED in the code. **api.openai.com: no response today** (`results/environment_check.json`). |
| Agent LLM, plus one masked re-execution per agent step | VERIFIED in the code |
| Stand-in embeddings | not allowed: they would not be official MELON |

## 4 Comparison readiness

- MELON detects attacks by comparing the agent's next tool calls with those of a masked re-run, using embedding similarity.
- It is a different mechanism from REM's and Progent's call-level decisions, and from DRIFT's planning and isolation.
- Its harness, protocol and tests already exist and are frozen.

**Decision: retain MELON as a CONDITIONAL arm.**
- It runs only if OpenAI embeddings and an agent model are available with spending authorisation.
- Otherwise it stays **NO-GO**; no substitute embedding is used.
- Its arm runs in AgentDojo 0.1.29, while REM, Progent and DRIFT run in 0.1.35. The episode set, scoring and attack are identical across both versions (fingerprint above). However, the message representation differs, which affects only how the agent's context is serialised. Report MELON as **direct on outcomes, with a documented environment difference**.
