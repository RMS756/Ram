# 04 MELON: status and compatibility (22 November 2026) — PENDING

| Item | Finding | Evidence |
|---|---|---|
| Official implementation | `ucsb-mlsec/MELON@06014c7` and `kaijiezhu11/MELON@4d3cc9c`, with identical `pi_detector.py` (sha256 `5a7f6b28…a9017`). Both heads were unchanged when fetched on 22 Nov 2026. No licence file, so the file is loaded by path and not vendored. | VERIFIED |
| Paper | ICML 2025 (PMLR 267), arXiv:2502.05174 (`third_party/MELON_PIN.json`) | as recorded on 5–6 Nov |
| Supported benchmark version | AgentDojo **0.1.29**: MELON assumes string message content. Its banking scoring is identical to 0.1.35 on reference solutions. | VERIFIED (audit fingerprint) |
| Required embedding model | OpenAI `text-embedding-3-large` | VERIFIED (code) |
| API and model dependencies | the agent LLM, which also performs one masked re-execution per step; OpenAI embeddings per tool call | VERIFIED (code) |
| Faithfulness of the existing integration | the upstream `MELON` class is used unmodified (hash checked by `test_upstream_melon_file_is_the_official_unmodified_one`), with the README pipeline structure and threshold 0.1. The README's `ContrastPIDetector` does not exist; the class is `MELON`. | VERIFIED; tests 9/9 passed on 22 Nov |
| Scripted pilot (19 Nov) | 480 episodes, 0 errors: an **integration test, not a result** | VERIFIED |

## What is missing

1. An agent model endpoint and credential.
2. OpenAI embedding access: `api.openai.com` gives no response from this environment.
3. Spending authorisation.

MELON stays **pending**. No other embedding model is substituted, and no result will be labelled MELON without the official model.

The other arms do not depend on MELON.
