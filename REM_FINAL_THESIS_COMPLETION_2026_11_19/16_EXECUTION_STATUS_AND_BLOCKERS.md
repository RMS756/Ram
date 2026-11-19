# 16 Execution status and blockers (19 November 2026)

| Item | Status | Evidence / reason |
|---|---|---|
| Verify `bf36381`; locate the frozen REM v1.0 baseline | **DONE** | `01`. Baseline is `rem/` @ `9fddfa7` + pilot @ `ea621c3` + `pilot_e0.yaml` @ `48bef90`. |
| Fresh reproduction of REM v1.0 | **DONE, gate passed** | 11 / 2,979, 105 / 334, 1,083 / 2,979 (`results/reproduction_gate.json`) |
| Ablation A0–A7 (+ B0) | **DONE** (replay, development data) | `03`, `04`; protocol `02` frozen at `dc8407d` |
| Decision-reachability analysis | **DONE** | `04` §2.6 |
| Calibration, latency per arm | **DONE** | `04` §2.4–2.5 |
| External: recorded closed-loop outcomes of D0–D4 (gpt-4o) | **DONE** (read from the authors' runs) | `06`, `07` |
| External: REM v1.0 replay on D0, D1, D2, D4 traces | **DONE** (replay, NO-ADAPT) | `06`, `07` |
| External: REM v1.0 replay on D3 (tool_filter) traces | **NOT EXECUTABLE** with the frozen harness | 05a: the filter's message precedes every tool call |
| **Closed-loop REM v1.0 with an LLM** | **NOT EXECUTED** | Re-checked 19 Nov: 127.0.0.1:8000 and :11434 are not reachable, and no experiment API key variable is set. The session's own infrastructure variable (`ANTHROPIC_BASE_URL`) belongs to the coding assistant and was **not** used. There is no spending authorisation, and the backbone and decoding are not frozen. |
| Closed-loop runs of D1–D4 by this project | **NOT EXECUTED** | Same blocker. The recorded runs of the benchmark authors were used instead and are labelled as such. |
| MELON / MELON + REM | **NOT EXECUTED** | `08`. Needs an LLM, an embedding endpoint and a budget, plus AgentDojo ≤ 0.1.29. It cannot be replayed offline. |
| Statistical analysis | **DONE** | `09`; post-hoc sensitivity labelled |
| Figures (architecture, ablation, security–utility) | **DONE** | `figures/` |
| Thesis R8 (5 chapters, DOCX, PDF) | **DONE** | `CHAPTER_*_FINAL.md`, `REM_THESIS_FINAL.docx/.pdf` (230 pp.) |
| University template | **BLOCKED: MISSING SOURCE** | Not in the repository or the workspace. Assumed A4 layout, as in R2–R7 (Appendix B, N-9). |
| Approved proposal file | **MISSING** | Objectives are quoted in Ch. 1 from earlier documents; the file itself is absent. |
| Human label audit | **NOT EXECUTED** | Package prepared earlier; needs annotators |
| Automated tests | **DONE** | 798 passed, 17 skipped, 1 xfailed (existing), plus 8 new tests passed |
| Commit and push | **DONE** | branch `claude/rem-final-thesis-completion-20261119` |

## What would unblock the remaining experiments

**The supervisors decide; nothing was started without authorisation.**

1. **A model endpoint and a spending cap.** Either an approved API key for one backbone with a written limit, or a local model server. This unblocks:
   - closed-loop REM v1.0;
   - closed-loop D1–D4 under identical conditions;
   - MELON (which also needs an embedding endpoint).
   The prepared live harness (`experiments/live/`) refuses to run without these values.
2. **Frozen values** for backbone, temperature and number of repeats (design lock).
3. **A decision on the tool_filter replay.** Either accept it as not replayable, or authorise a separately labelled adapter that skips the filter's message. That adapter would be a new evaluation procedure.
