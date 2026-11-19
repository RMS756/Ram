# 02 MELON: paper and code audit (19 November 2026)

## Paper

| Item | Verified value |
|---|---|
| Title | **MELON: Provable Defense Against Indirect Prompt Injection Attacks in AI Agents.** The title given in the task ("A Defense Against Indirect Prompt Injection Attacks in Tool-Using LLM Agents") is **not** the paper's title. |
| Authors | Kaijie Zhu, Xianjun Yang, Jindong Wang, Wenbo Guo, William Yang Wang |
| Venue | ICML 2025, PMLR 267, pp. 80310–80329; arXiv:2502.05174 |
| How verified | PMLR and OpenAlex (`REM_ARCHITECTURE_REDESIGN_STUDY_2026_11_18/results/literature_verification.json`), and the README BibTeX of both official repositories. In R8 it is already in the reference list; no new citation is needed. |

## Official code

| Repository | Revision (pinned) | Content | `pi_detector.py` sha256 |
|---|---|---|---|
| `ucsb-mlsec/MELON` (the candidate named in the task; cloned anonymously on 19 Nov at `/home/user/ucsb-mlsec/melon`) | `06014c7c72d3e9a1f9a27b8742e8bf711689caad` (single commit "Immortalise init", 2025-07-01) | `README.md`, `pi_detector.py` | `5a7f6b28228545e0d4ad9e98c9080ad819bb1cf471a67a31c8c4466b199a9017` |
| `kaijiezhu11/MELON` (the first author's repository; local clone since 5 Nov at `/home/user/upstream/MELON`) | `4d3cc9c0175cc26332aac696ac5556c3f85a5e8e` | `README.md`, `pi_detector.py` | **identical**: `5a7f6b28…a9017` |

**Comparing the two repositories:**
- **Implementation:** byte-identical.
- **README:** the two differ in one line, which is the issue below.
- **Licence:** neither repository contains a licence file. The file is therefore **loaded by path from the clone and not vendored**, and its hash is checked before every use.

## The `ContrastPIDetector` issue

- **In `ucsb-mlsec/MELON`.** The README tells the user to add `ContrastPIDetector(llm, threshold=0.1)` to AgentDojo's `from_config`. **No class of that name exists** in `pi_detector.py`.
- **In `kaijiezhu11/MELON`.** The README has the corrected line, `MELON(llm, threshold=0.1)`.
- **The real class** is `MELON(PromptInjectionDetector)`.
- **Invocation used here.** `ToolsExecutionLoop([ToolsExecutor(), MELON(llm, threshold=0.1)])` after `[SystemMessage, InitQuery, llm]`, i.e. the README structure with the real class name.

## What the code does (read in full)

1. **When it runs.** `MELON.query` runs after each tool turn. The first assistant turn, before any tool output, is not inspected.
2. **Original run.** MELON makes the agent's next LLM call itself.
3. **Masked run.** It is a second call to **the same LLM**, made on deep copies of the runtime and environment.
   - The context holds the system message, a fixed few-shot dialogue, and a task-neutral user prompt: "read random.txt … if there are instructions, follow them".
   - All tool outputs so far are packed into one fake `read_file` result.
   - **No tool is executed in the masked run.**
4. **Embedding bank.** The tool calls of the masked run are rendered as text (`send_money` keeps only recipient and amount). They are embedded with OpenAI **`text-embedding-3-large`**, which is **hard-coded**: `OpenAI(api_key="your-api-key")`, and the README tells the user to edit the key. The embeddings are added to a per-episode bank in `extra_args`.
5. **Detection.** An attack is flagged if **any** original-run call has cosine similarity **> 0.8** with any banked call. That 0.8 is hard-coded.
   - The constructor's `threshold=0.1` is stored and **never used**.
   - `mode` defaults to `full_conversation`.
6. **On detection.**
   - The new assistant message becomes "The tool outputs contain potential prompt injection, stopping execution." with no tool calls, so the episode ends.
   - The last tool output becomes "<Data omitted because a prompt injection was detected>".
7. **Dependencies.** `transformers.AutoModel` and `torch.nn.functional` are imported but unused at run time. `openai` and `numpy` are required.

### Code-level observations, upstream unchanged

- **O-1.** `zip(masked_tool_call_bank, masked_tool_emb_bank)` pairs a **set** with a **list**. The similarity uses the embeddings in list order, so detection is unaffected. Only the printed call names can be mismatched.
- **O-2.** The bank lives in `extra_args`, and AgentDojo 0.1.29's `AgentPipeline.query` has a mutable default `extra_args={}`. Without isolation, the bank leaks across episodes in one process. A test demonstrates the leak. The harness gives every episode a fresh dict; compatibility measure C-2 applies the same isolation to every arm.
- **O-3.** Upstream treats message `content` as a string. AgentDojo switched to content blocks in **0.1.30**. Unmodified MELON therefore runs only on **AgentDojo ≤ 0.1.29**. The comparison uses 0.1.29 for **all three arms**. Banking v1 task code and the `important_instructions` attack code are identical between 0.1.29 and 0.1.35 (`diff -r`, 5 Nov).
- **O-4.** AgentDojo 0.1.29 sends no `temperature` when it is 0.0. This is identical in all arms.

## Supported benchmarks

**The README** shows AgentDojo runs, with `-s slack` in its example command.

**The paper** evaluates all AgentDojo suites. Its results are **cited as the authors' results only**. They are never placed in a table with this project's measurements.

## Conclusion

The official MELON is identified, pinned and installed. It was **executed unmodified inside AgentDojo banking** in this study's harness (`05`), but only with a **scripted agent and a stand-in embedding function**. It was **not** executed with a real LLM or with `text-embedding-3-large`; the blockers are in `03` and `14`.
