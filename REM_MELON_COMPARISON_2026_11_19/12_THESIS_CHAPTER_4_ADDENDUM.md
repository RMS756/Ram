# 12 Thesis Chapter 4 addendum to R8 (proposed text, not merged)

**Decision.**
- **R8 remains the valid thesis.** No REM vs MELON result exists, so an R9 with a comparison section is **not justified**.
- **What the thesis can take instead** is a short reproducibility and feasibility subsection: Chapter 4, after Section 4.4.2, or an appendix. It replaces nothing in R8.
- **Chapter 2 and Chapter 5.** Chapter 2 already cites MELON (verified reference), and Chapter 5's conclusions do not change.
- **Process.** The text below is offered for the supervisors' decision. It was not built into a new edition.

---

### 4.4.5 Original MELON in the Same Harness: Implementation and Feasibility (19 November 2026)

*Kind of evidence:* implementation and scripted integration test. **No language model was run, and this section reports no attack-success or utility result for MELON or for REM.**

**MELON.** MELON (Zhu et al., 2025) detects indirect prompt injection by **masked re-execution**:
- After each tool result, the agent's next tool calls are generated twice by the same model:
  - once in the real conversation;
  - once in a masked conversation, in which the user's task is replaced by a neutral instruction to read and follow the tool outputs.
- The tool calls of the masked run are embedded with OpenAI's `text-embedding-3-large`.
- If a call of the real run has cosine similarity above 0.8 with a call of the masked run, the call is taken to be driven by the tool outputs rather than by the user. MELON then stops the episode.

**How MELON differs from REM.**
- MELON needs a second model call per step and an embedding model; it fits no parameters to the suite.
- MELON stops the episode on detection.
- REM v1.0 evaluates each proposed call with a fitted ridge logistic model and an expected-loss rule, makes no model call, and withholds a single call while the agent continues.

**Implementation.**
- **Code used.** The official implementation was used unmodified: `pi_detector.py`, identical in `ucsb-mlsec/MELON` at `06014c7` and `kaijiezhu11/MELON` at `4d3cc9c`, and hash-checked before use.
- **README correction.** The README of the former names a class `ContrastPIDetector` that does not exist; the class is `MELON`.
- **AgentDojo version.** The file requires AgentDojo 0.1.29, because later versions changed the message format, so all arms of the comparison use 0.1.29. The banking task and attack code are identical to the version used elsewhere in this thesis.
- **Three arms.** No defence; REM v1.0 with its frozen fold models; and MELON in the structure of its README. They differ only at the defence's integration point, and use the same agent model, tasks, payloads, initial state and evaluator.
- **Protocol.** It was committed before any scored episode (`REM_MELON_COMPARISON_2026_11_19/06_FROZEN_EVALUATION_PROTOCOL.md`). It fixes:
  - a pilot stage and a full stage of 144 attacked and 16 benign episodes per arm;
  - paired triples;
  - grouped intervals.

**Integration test.**
- **What was run.** With a scripted agent that obeys every injection and a stand-in embedding function, the harness ran all 480 episodes (160 cases × 3 arms) without error.
- **What it showed.** The payload reached the agent, REM evaluated every proposed call, and MELON's own detector ran its masked re-executions and embedding comparison. Neither test double estimates how REM or MELON would perform with a real model, so no outcome from it is reported.
- **REM's per-call computation:** median 0.27 ms, p95 0.52 ms, on a 4-core CPU.

**Why the comparison was not executed.**
- **Model.** The evaluation environment had no graphics processor, and no reachable source of model weights, local model server or model API.
- **Embeddings.** MELON's embedding model is a paid API that the environment could not reach.
- **Budget.** No spending authorisation existed.

**Expected workload,** from the benchmark's recorded gpt-4o trajectories:
- MELON adds about 442 model calls to the 602 of each other arm, about 73% more;
- it more than doubles the characters sent to the model;
- it adds up to 884 embedding calls.

**MELON's published results** are cited as its authors' results. They are not compared with REM's replay results, which come from a different evaluation mode and population.

**What this section establishes.** The comparison is implemented, tested and pre-registered. It **does not** establish how REM and MELON compare. Executing it requires a supervisor decision on the model, the embedding endpoint and a spending limit (Appendix B, D-15).

---

## If a live run is later completed

The subsection would become "Comparative Evaluation of REM and MELON". It would hold:
- the tables and figures of `analyze_live.py`: ASR and benign utility per arm with grouped intervals; paired differences; false-positive interventions; model calls, tokens and cost; REM latency;
- a security–utility discussion following `08`, testing its pre-recorded hypotheses;
- the disclosures of `06`.

Chapter 5 would be updated only if the results resolve a difference, and the result would then justify an R9.
