# 14 Final execution status (19 November 2026)

| Phase | Status |
|---|---|
| 1 Verify R8 and REM v1.0 | **DONE.** `f4ff23f`, `9fddfa7`, `ea621c3`, `48bef90` verified; R8 unchanged (`01`). |
| 2 Verify original MELON | **DONE.** Paper and both repositories pinned; identical implementation; `ContrastPIDetector` README error confirmed; real class `MELON` (`02`). |
| 3 Compute resources | **DONE.** 4 CPU, 15.7 GiB RAM, no GPU, 15 GB disk. **No model source, model endpoint, embedding endpoint or price list reachable** (`03`). |
| 4 Fair design | **DONE** (`04`) |
| 5 Live closed-loop execution | **NOT EXECUTED** (blockers below) |
| 6 Pilot | **Live pilot NOT EXECUTED.** **Scripted integration pilot DONE:** 480 episodes, 0 errors, all mechanisms active, unmodified MELON (`05`). |
| 7 Protocol freeze | **DONE**, committed at `a1db36a` with hashes before any scored episode (`06`) |
| 8 Full comparison | **NOT EXECUTED** |
| 9 Statistics | **Plan implemented** (`analyze_live.py`); **no outcome analysed** (`09`) |
| 10 Secondary replay analysis | **NOT EXECUTED: not supported by MELON's algorithm**, which needs fresh masked re-executions (`08`) |
| 11 Figures | Planning workload figure only. Result figures are **NOT GENERATED**, because no live data exist. |
| 12 Thesis integration | Feasibility subsection drafted (`12`); **R8 unchanged; no R9** |

## Blockers, all external to the code

| # | Blocker | What removes it |
|---|---|---|
| B1 | No model weights reachable: huggingface.co and all mirrors are blocked by this session's network policy | Allow `huggingface.co` (and `cdn-lfs.huggingface.co`) in the repository's environment ("ram-thesis-research") and start a new session there. Even then, CPU-only inference for about 2,248 calls is slow and was not measured. |
| B2 | No model API: api.openai.com is blocked, no credential is configured, and no spending authorisation exists | Supervisor decision D-15: provider, model, cap, an API key added as a network secret, and the host allowed |
| B3 | **MELON's published configuration requires OpenAI `text-embedding-3-large`** | Same as B2 for the embeddings host. A local embedding model gives "MELON-ADAPTED-EMBEDDINGS" only. |
| B4 | Prices not verifiable (provider pages unreachable) | The operator enters the run-day prices in the config |
| B5 | Model id, decoding, repeats, timeout and retries not fixed (design lock) | Supervisor or author decision before stage 1 |

## Answers to the twelve final questions

1. **Was the original MELON implementation installed and executed?** It was installed and pinned. Its unmodified `MELON` class was executed inside AgentDojo banking, but **only with a scripted agent and a stand-in embedding function**. It was **not** executed with a real LLM or with `text-embedding-3-large`.
2. **Was a real language model used?** **No.**
3. **How many AgentDojo banking episodes completed?** **0 live episodes.** 480 scripted integration episodes completed (160 cases × 3 arms), and they are not results.
4. **Were identical episodes evaluated under all arms?** In the scripted pilot, yes: paired triples on identical cases and payloads. In a live run, the frozen protocol enforces it. No live episode exists.
5. **REM's and MELON's observed ASR?** **NOT EXECUTED**: there is no observed live ASR for either.
6. **Their legitimate-task completion rates?** **NOT EXECUTED.**
7. **Which defence caused more false-positive interventions?** **Unknown.** Not measured live.
8. **Latency and inference costs?**
   - **REM:** 0.272 ms median and 0.524 ms p95 per call (CPU), with zero model calls.
   - **MELON:** a planning estimate of about +442 model calls (+73%), +4.87 M input characters (+138%) and up to 884 embedding calls per 160 episodes.
   - **Dollar cost:** not estimated, because prices could not be verified.
9. **Are observed differences statistically distinguishable?** **No observed differences exist.**
10. **Can these results be included in Chapter 4?** **Only as a feasibility and implementation subsection** (`12`). No comparative result may be included.
11. **Is R8 still the valid thesis version?** **Yes. R8 remains valid; an R9 is not justified** until a live comparison is completed.
12. **Remaining limitations and blockers?**
    - **Blockers:** B1–B5.
    - **Limitations for a future live run:** familiar tasks (not an independent holdout); a different AgentDojo version from R8 (0.1.29); the different intervention semantics of the two defences; few clusters.
