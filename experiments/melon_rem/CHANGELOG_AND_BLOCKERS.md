# MELON vs MELON + REM — Change Log and Remaining Blockers

**Branch:** `claude/melon-rem-extension`, created from `claude/rem-r4-corrections-3ktvze` at `9fddfa7`. Committed locally; **not pushed, merged or published**, as instructed.

## Change log (5 Nov 2026)

| Area | Change |
|---|---|
| Upstream | Cloned `kaijiezhu11/MELON` at `4d3cc9c` into `/home/user/upstream/MELON` (outside the repository; unmodified; no licence file, so not vendored) |
| Environment | New virtual environment `/home/user/venvs/melon029` with AgentDojo 0.1.29 (required by the upstream code), torch 2.9.1 and transformers 5.22.1 (imported by the upstream file); `verification/pip_freeze_melon_env.txt` |
| Code (new) | `rem/integration/melon_rem.py`: hash-checked loader; README-identical MELON construction; REM-gated executor (AgentDojo 0.1.29 `ToolsExecutor` logic plus the REM gate); pipelines that differ only in the executor; per-episode `extra_args`; error classes |
| Code (new) | `experiments/melon_rem/`: `export_frozen_rem.py`, `run_melon_rem.py` (fail-closed, paired, interleaved, seed-controlled), `spending_guard.py`, `estimate_budget.py`, `analyze_melon_rem.py`, `melon_rem_config_TEMPLATE.yaml` |
| Frozen artefact (new) | `experiments/melon_rem/frozen/frozen_rem_bundle.pkl` (+ `.json`), sha256 `983c5b0d…`, exported deterministically from the frozen cross-fit state. **Nothing refitted.** |
| Tests (new) | `tests/test_melon_rem_integration.py` (22; MELON environment) and `tests/test_melon_rem_offline.py` (8; both environments) |
| Existing REM code | **Unchanged** (`rem/` core, `agentdojo_replay.py`, `agentdojo_live.py`, pilot, configs, results) |
| Docs (new) | `MELON_REM_INTEGRATION.md`, `MELON_REM_EXPERIMENT_PROTOCOL.md`, `LOCAL_VERIFICATION_REPORT.md`, `SOURCE_MANIFEST.md`, this file |
| Thesis | One new subsection in Chapter 4, §4.14 "Controlled Evaluation of MELON with and without REM", with Table 4.15 (every cell "not executed") (source `REM_FINAL_THESIS/tools/text_5ch/ch4_melon_rem.md`). |
| Thesis: knock-on edits | Old §4.14–4.17 renumbered to §4.15–4.18 and Tables 4.15–4.16 to 4.16–4.17 through `make_5ch.py` (0 unresolved references). One sentence added to §1.12 and one bullet to the §4.18 summary. **No result, conclusion or abstract text changed.** |
| Thesis: rebuild | DOCX and PDF rebuilt: 241 pages. All 360 numerical values from R5 are preserved. No margin overflow, no blank pages, no tracked changes. Audit files updated. |
| Not done (by design) | No paid call; no change to the abstract or conclusions; no new benchmark, classifier or defence; no novelty claim |

## Findings worth recording

1. **Version incompatibility.** The upstream MELON code requires string message content, i.e. AgentDojo ≤ 0.1.29. It cannot run unmodified on 0.1.35.
2. **Unused threshold.** `MELON(llm, threshold=0.1)` stores a threshold that the detector never uses. Detection uses cosine > 0.8 on `text-embedding-3-large`, hard-coded.
3. **Cross-episode state leak (upstream).** MELON keeps its masked-call bank in `extra_args`, and AgentPipeline's mutable default `extra_args={}` makes it persist across episodes in one process. This study resets it per episode in both conditions (C-2); a test demonstrates the leak.
4. **Temperature not sent.** AgentDojo 0.1.29 sends no temperature when it is 0.0.
5. **Same immediate effect.** Under step-level semantics, Modify, Block and Escalate without a reviewer all withhold the current call.

## Remaining blockers

| # | Blocker | Kind |
|---|---|---|
| B-1 | No spending authorisation or cap, and no provider prices, in this session (M-1) | **Spending decision** |
| B-2 | No `OPENAI_API_KEY` in the environment (MELON's detector always needs the OpenAI embeddings API) | Credential |
| B-3 | Backbone id, temperature, repeats, timeout and retries (M-2); REM fitted-parameter source (M-3); run id; order seed | Design inputs (runner exits 2) |
| B-4 | REM's costs and tiers are exploratory and not supervisor-approved (D-9); tie rule (D-4) and calibration target (D-3) open; no injection classifier (D-8) | Inherited supervisor decisions |
| B-5 | Real-provider compatibility of AgentDojo 0.1.29 with OpenAI SDK 3.46.0 is untested (fake provider only). The pilot is the test | Technical, resolved by the pilot |
| B-6 | Training-provenance overlap: familiar tasks; attacker objectives held out only via the fold rule | Scope limitation (reported, not removable) |
