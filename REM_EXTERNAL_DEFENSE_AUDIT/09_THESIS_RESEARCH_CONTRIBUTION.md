# 09 How external comparisons can establish REM's research value (22 November 2026)

This file proposes a role for the comparisons in the thesis. It makes **no claim of superiority**. No live comparison has been run.

## 1 What each comparison can and cannot show

| Comparison | Question it answers | Can support | Cannot support |
|---|---|---|---|
| REM vs Progent-manual (same agent, same tool boundary) | On identical proposed calls, how does a learned, calibrated, consequence-aware decision compare with an exact hand-written allow-list? | A mechanism-level contrast. Progent-manual needs a per-suite list of legitimate recipients (it blocks 3–4 benign reference tasks and all 9 injection references), while REM needs fitted data and calibration. Their errors may fall on different tasks. | A general claim about Progent, because its main mode is LLM-generated policies |
| REM vs Progent-generated | Does REM's no-extra-model decision reach comparable protection without a policy LLM? | Security, utility and cost trade-offs (model calls: REM 0) | Anything before it is run with the same model |
| REM vs DRIFT (+ scaffold control) | How does a lightweight tool-boundary gate compare with a full LLM-based planning, validation and isolation system? | Outcome and cost comparison of two complete systems; DRIFT's module effect via D2 vs D2c | Attributing differences to REM's components (the agents differ) |
| REM vs MELON (conditional) | Detection by masked re-execution vs a learned gate | Outcome and cost comparison | Anything unless OpenAI embeddings are authorised |
| REM vs native AgentDojo defences (recorded) | How REM's offline replay compares with published closed-loop runs | Descriptive context (already in R8 `07`) | A paired closed-loop comparison (REM was not in that loop) |

## 2 Defensible framing for Chapters 2 and 4

1. **Positioning.** Use the matrix in `05`. REM is the only one of the four defences that:
   - makes **no additional model calls** at decision time;
   - uses **calibrated probabilities with an explicit loss matrix**;
   - records an **audit record** per call.

   These are design properties, verified in the code. They are not performance claims.
2. **The cost dimension is measurable without a model:**
   - REM: 0 extra calls, median 0.151 ms per call offline;
   - Progent-manual: 0 extra calls;
   - DRIFT: about 20 calls for a two-call benign task (test-double count);
   - MELON: a masked re-execution per step, plus embeddings.

   Present this as overhead by construction, labelled as counts, not prices.
3. **Security and utility claims wait for the live run** in `07`. When reported, state them as paired differences with intervals, on banking v1, for the chosen model, with the scaffold caveat for DRIFT.
4. **Negative or mixed outcomes are results.** Recent work reports over-defence as a deployment barrier (AgentDyn's abstract), and REM's own ablation found low withholding precision (0.25–0.40). So the utility comparison may not favour REM. The thesis should report it either way.

## 3 What would most strengthen the contribution

**The REM vs Progent-generated vs DRIFT live comparison, on the same model, banking v1, with paired episodes.** Three reasons:
- It tests REM against the two most-cited recent tool-boundary and system-level defences (OpenAlex: 381 and 106 citations).
- It covers both the deterministic-policy family and the LLM-validator family.
- Progent-manual serves as a deterministic upper reference for allow-list enforcement.

## 4 Changes to the thesis

None proposed now. R8 and the frozen design are untouched. Any new section waits for results and supervisor approval.
