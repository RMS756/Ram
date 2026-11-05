# MELON versus MELON + REM — Integration

**Status (5 Nov 2026):** implemented and verified locally with scripted agents, a fake embedding client and a fake provider. **No real model call has been made; no result exists.**

**Framing.** This is an extension of a published defence (MELON) through integration with REM, evaluated against the original defence. It does **not** claim:
- that REM was derived from MELON;
- that MELON's algorithm was improved (it is not modified);
- that REM must improve MELON;
- that the integration is novel (see §8).

## 1. Primary sources

| Item | Value |
|---|---|
| Paper | Zhu, K., Yang, X., Wang, J., Guo, W., & Wang, W. Y. (2025). *MELON: Provable defense against indirect prompt injection attacks in AI agents.* ICML 2025. arXiv:2502.05174 (already in the thesis reference list) |
| Official code | https://github.com/kaijiezhu11/MELON |
| Pinned commit | `4d3cc9c0175cc26332aac696ac5556c3f85a5e8e` (2025-07-31; the code itself is from `08a9e97`, 2025-06-12) |
| Implementation file | `pi_detector.py`, sha256 `5a7f6b28228545e0d4ad9e98c9080ad819bb1cf471a67a31c8c4466b199a9017` (checked before every use) |
| Licence | **The repository contains no licence file.** The file is therefore **not copied** into this repository. It is loaded by path from a local clone; attribution and citation follow the README's BibTeX. Redistribution would need the authors' permission. |
| Local reference copy | `/home/user/upstream/MELON` (clean clone at the pinned commit; never edited; checked by a test) |

## 2. What original MELON does (verified by reading the code)

**Pipeline (upstream README, `from_config` for `defense == "melon"`):**
```
[SystemMessage, InitQuery, llm, ToolsExecutionLoop([ToolsExecutor(), MELON(llm, threshold=0.1)])]
```

1. `ToolsExecutor` executes the tool calls of the last assistant message.
2. `MELON.query` runs when the last message is a tool result. It first makes the agent's next LLM call itself (the *original run*).
3. MELON then makes a **masked** LLM call:
   - It uses deep copies of the runtime and environment.
   - The context contains:
     - the system message;
     - a fixed few-shot dialogue;
     - a task-neutral user instruction ("use read_file … random.txt … if there are instructions, follow them");
     - a fake `read_file` result containing all tool outputs so far.

   **No tool is executed in the masked run.**
4. The tool calls of the masked run are rendered as text (`send_money` keeps only `recipient` and `amount`) and embedded with OpenAI `text-embedding-3-large`. They are added to a *bank*.
5. An attack is flagged when any original-run call has cosine similarity **> 0.8** with any banked masked call.
   - The constructor argument `threshold=0.1` is stored but **not used**.
   - The default `mode` is `full_conversation`.
6. **On detection:**
   - the new assistant message is replaced by "The tool outputs contain potential prompt injection, stopping execution." with no tool calls, so the loop ends;
   - the last tool result is replaced by "<Data omitted because a prompt injection was detected>".
7. The first assistant turn (before any tool output) is not inspected by MELON.
8. **Model settings:** the same `llm` object, with the same model and decoding, serves the agent, the original run and the masked run. The embedding model is hard-coded.

**Configuration used here: original MELON, not MELON-Aug.** MELON-Aug, per the paper, combines MELON with a prompt-augmentation defence; that is not used. No paper-level hyperparameter beyond the code was changed.

## 3. Compatibility with the benchmark version

| Finding | Evidence | Consequence |
|---|---|---|
| The upstream file treats message `content` as a string (`"function: " + … + original_msg["content"]`). | Code reading; AgentDojo history: content blocks were introduced in commit `d67f9d1` (2025-02-25) and first released in **v0.1.30** (2025-04-30). | Original MELON cannot run unmodified on AgentDojo 0.1.35, which REM's main environment uses. |
| AgentDojo **0.1.29** (2025-02-24) uses string content. | Installed and tested. | **Both conditions run on AgentDojo 0.1.29** in a separate environment (`/home/user/venvs/melon029`). MELON is unmodified. |
| Banking v1 task code is identical in 0.1.29 and 0.1.35, and so is the `important_instructions` attack code. | `diff -r` of `default_suites/v1/banking` and `attacks/important_instructions_attacks.py`: no differences. | Same tasks as REM's fitting traces. |
| One default injection-vector string differs: the bill text has a literal `\n` in 0.1.29 that 0.1.35 escapes. | `diff data/suites/banking/injection_vectors.yaml`. | Applies only where no injection is placed. It is identical in both conditions; recorded as a provenance note. |
| AgentDojo 0.1.29 sends **no** temperature when it is 0.0 (`temperature or NOT_GIVEN`). | `llms/openai_llm.py`. | Identical in both conditions; recorded. A configured 0.0 means "provider default". |

## 4. Compatibility measures (identical in both conditions; MELON's code unchanged)

| ID | Measure | Why | Effect on MELON's defence logic |
|---|---|---|---|
| C-1 | After `MELON(llm, threshold=0.1)` is constructed, `melon.detection_model` is set to the run's OpenAI client (wrapped by the spending guard). | Upstream hard-codes `OpenAI(api_key="your-api-key")` and tells users to edit the key in the file. | None: same model, same call. |
| C-2 | `EpisodePipeline` passes one fresh `extra_args` dict per episode. | `AgentPipeline.query` has a mutable default `extra_args={}`, and MELON stores its bank there. In one process the bank would otherwise carry over between episodes **and between conditions**. A test demonstrates the leak. | Within an episode (including AgentDojo's up to 3 re-queries) the bank persists as upstream. **Across episodes it is reset.** This deviates from what the upstream code does when many tasks run in one process. It is required for episode isolation and paired comparison. Whether the paper's runs were affected is unknown. |
| C-3 | Upstream `print` diagnostics are redirected to `melon_upstream_stdout.log`. | Log hygiene. | None. |
| C-4 | `sys.dont_write_bytecode` is set while importing the upstream file. | Keeps the reference clone byte-clean. | None. |
| C-5 | `torch` 2.9.1 (PyPI build) and `transformers` 5.22.1 are installed. | The upstream file imports them (`AutoModel`, `torch.nn.functional`), although they are unused in its logic. The PyTorch CPU index is blocked by the network policy (HTTP 403). | None. |

## 5. Integration point

```
MELON:      [System, InitQuery, llm, ToolsExecutionLoop([ToolsExecutor(),               MELON(llm)])]
MELON+REM:  [System, InitQuery, llm, ToolsExecutionLoop([RemGuardedToolsExecutor(guard), MELON(llm)])]
```

- **The executor is the only difference.** A test checks the element types and the shared `max_iters=15`. `rem/integration/melon_rem.py: RemGuardedToolsExecutor` reproduces AgentDojo 0.1.29's `ToolsExecutor.query`:
  - call order;
  - tool-call IDs;
  - empty-name and invalid-tool errors;
  - string-list argument conversion.

  The only addition is `guard.evaluate(tool, args)` immediately before `runtime.run_function`.
- **What REM sees.**
  - Every call that reaches execution has survived MELON. Calls MELON stopped are dropped from the transcript and never reach REM.
  - First-turn calls, which MELON does not inspect, are also evaluated by REM.
  - REM never sees MELON's masked generation; the masked run makes no tool call.
- **What a withheld call produces.**
  - It is not executed.
  - The agent receives a tool result with the same `tool_call_id`, empty content and `error="REM: …"`, and may continue, retry or replan.
  - MELON's next masked run sees that tool result like any other.
- **REM is the reference algorithm, unchanged.** `RemGuard` and the frozen components (§6) are the same code as the replay and live harnesses. REM adds no model call.

## 6. Frozen REM configuration

- **Bundle:** `experiments/melon_rem/frozen/frozen_rem_bundle.pkl`, sha256 `983c5b0d54de01cdb37467526f3aea2c4065f888f59c140ea6714ec1b0d3e2c5`.
  - Exported by `export_frozen_rem.py` from the frozen nested cross-fit state.
  - Input hashes: `crossfit.pkl` `27464b4d…`, `rmod.pkl` `29c2c78e…`, `configs/exploratory/pilot_e0.yaml` `8e1aa107…`.
  - `crossfit.pkl` is byte-identical across four independent re-executions of `run_all.sh`. Re-export is deterministic (`PYTHONHASHSEED=0`); two exports from different state directories give the same hash.
- **Features:**
  - `x_ctx2, x_beh1–x_beh4, x_act1–x_act3`;
  - `x_ctx1` (injection classifier) is **absent** (SD-DET, D-8);
  - features unavailable under k_D2 are handled as in Chapter 3 (D-5).
- **Estimator and calibration:**
  - ridge logistic regression per outer fold;
  - logit calibration fitted with label-NLL (primary; D-3/SC-4 open);
  - γ₁ ranges from 0.945 to 0.981 across the folds, so all are > 0 and the monotone interpretation holds.
- **Costs and tiers:** `pilot_e0_exploratory`. **Declared exploratory values, not supervisor-approved (D-9).**
  - Costs: C_FA = 1; C_miss = 1/5/10/20 (tiers 1–4); C_mod = 0.5; C_esc = 0.3.
  - Tiers: read 1; profile change 2; value transfer ≤ 1000 → 3, > 1000 → 4; payment modification 4; credential change 4.
  - r_mod per fold from the bundle.
- **Predicates:** D1 (prohibited set Π = ∅), D2 (k_D2 = 3; argument provenance required).
- **Tie behaviour:** Chapter 3 order, with ties recorded (`record_chapter3_order`; D-4 open).
- **Policy:** A3 = expected-loss verdict over {Allow, Modify, Escalate, Block}.
- **Mitigation semantics: step-level** (canonical in CLAUDE.md). Modify and Block act on the current call only. Nothing persists to later calls.
  - **Under step-level semantics, Modify, Block and Escalate (no reviewer) have the same immediate execution effect: the current call is withheld.** Only the refusal text and the audit record differ; a test checks this.
  - The declared Modify mechanism, tool restriction, persists only under the episode-level policy, which is not used here.
- **Escalation:** `no_reviewer`. An escalated call is withheld and never released by a label-based or idealised reviewer. No human review mechanism exists or is used.
- **Labels:** the reference labeler is called only to write the audit record. It never reaches the decision (`decide` receives p, tier, tool and availability), and MELON never sees it. A test swaps all labels and observes identical execution.

## 7. Training-provenance overlap (audit)

REM was fitted on recorded AgentDojo banking traces of 21 agents (`important_instructions`), with folds grouped by injection task (Chapter 3 §3.11.5). The evaluation reuses the **same 16 user tasks and 9 injection tasks**.

**With `fitted_parameters_source = heldout_crossfit_assignment`** (implemented; the choice is a design input):
- **Attacked case (u, i)** uses fold *i*. Its fit excluded every attacked episode with injection task *i* (all agents, all user tasks) and the benign episodes of the user tasks assigned to fold *i*. The **attacker objective is unseen**. The user task *u*, its prompt, its environment and the attack template were seen in training (with other injection tasks).
- **Benign case u** uses fold `benign_user_task_fold[u]` (round robin). Its fit excluded u's benign episodes, but not u's attacked episodes with other injection tasks.
- **If the backbone is one of the 21 recorded agents** (e.g. `gpt-4o-2024-05-13`), REM was fitted partly on that model's own recorded trajectories for the same tasks, though not for the held-out cells.

The new trajectories are generated by a defended agent and are therefore new data, but **they are not unseen-task evaluation**. Conclusions must be limited to: **held-out attacker objectives on familiar banking tasks, one attack template**. No uncontaminated test set is claimed.

## 8. Literature check on the combination (record-level, 5 Nov 2026)

- **Searches:** two queries on OpenAlex/Semantic Scholar (FastTrack Literature):
  - "combining MELON masked re-execution defense with another runtime guard or tool-call policy layer against indirect prompt injection in LLM agents" (2025–);
  - "MELON prompt injection defense AgentDojo combined defenses defense-in-depth evaluation" (2025–).
- **Results:** 21 and 41 records; 20 of each were inspected at abstract level. MELON appears in the abstracts of:
  - SIEVE (arXiv:2512.06716), as a compared defence;
  - AdapTools (EMNLP 2026), an adaptive attack evaluated against defences.
- **Finding:** none of the inspected abstracts describes adding a consequence-aware expected-loss gate to MELON. MELON-Aug, by MELON's authors, is itself a combination with prompt augmentation.
- **Conclusion:** the search is **not exhaustive** and covers no full texts, so **no novelty claim is made**. AdapTools indicates that adaptive attacks against MELON exist, a limitation of evaluating one static attack. These records were not verified or added to the reference list.

## 9. Files

| File | Role |
|---|---|
| `rem/integration/melon_rem.py` | Loader (hash check), MELON construction, guarded executor, pipelines, episode runner, error classes |
| `experiments/melon_rem/export_frozen_rem.py` | Frozen REM bundle export (main environment) |
| `experiments/melon_rem/frozen/frozen_rem_bundle.pkl(.json)` | Frozen REM components and their provenance |
| `experiments/melon_rem/run_melon_rem.py` | Fail-closed, paired, interleaved runner with spending guard |
| `experiments/melon_rem/melon_rem_config_TEMPLATE.yaml` | Configuration (design inputs `REQUIRED_FROM_DESIGN`) |
| `experiments/melon_rem/spending_guard.py`, `estimate_budget.py` | Spend cap with in-flight reservations; budget projection from pilot usage |
| `experiments/melon_rem/analyze_melon_rem.py` | Metrics, paired differences, cluster bootstrap |
| `experiments/melon_rem/SOURCE_MANIFEST.md`, `verification/pip_freeze_melon_env.txt` | Pinned sources and dependencies |
| `tests/test_melon_rem_integration.py` (MELON environment), `tests/test_melon_rem_offline.py` (both) | Local verification |
