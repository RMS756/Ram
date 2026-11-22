# 08 Integration tests (executed 22 November 2026)

**What these tests do and do not show**
- No language model was called and no paid request was made.
- No test uses a scripted agent to measure defence effectiveness.
- Where a test double is used (DRIFT), the results file says so in its first field.

## Environments created

| venv (`/home/user/venvs/`) | Contents | AgentDojo |
|---|---|---|
| `drift` | `agentdojo==0.1.35` + DRIFT `requirements.txt` (installs cleanly, rc 0) | 0.1.35 |
| `progent` | `agentdojo==0.1.35` + `secagent` from `progent@3e79753` (editable, clean export) | 0.1.35 |
| `progent_fork` | Progent's bundled AgentDojo fork + `secagent` | 0.1.29 (fork) |
| `agentdyn` | AgentDyn (editable) | 0.1.35 (fork) |
| `melon029` | existing MELON environment (19 Nov) | 0.1.29 |

The package lists are in `results/pip_freeze_*.txt`.

## Tests and results

| # | Test | Script | Result | Output |
|---|---|---|---|---|
| T1 | Evaluator fingerprint: AgentDojo reference solutions, 16 benign tasks and 144 pairs × 2 outcomes, banking v1 and v1.2, in 5 environments | `experiments/external_defense_audit/suite_fingerprint.py` | **PASS.** All five environments (PyPI 0.1.35, DRIFT venv, AgentDyn fork, PyPI 0.1.29, Progent fork 0.1.29) give identical scores. Benign reference utility is 16/16. User-task references under injection: utility 144/144, security 0/144. Injection references: security 144/144. | `results/fingerprint_*.json` |
| T1a | File hashes of the banking suite | same | AgentDyn differs from PyPI only in `data/system_messages.yaml` and `task_suite/task_suite.py`. The 0.1.29 package differs in `injection_vectors.yaml` and `task_suite.py`. The banking task code is identical. | same |
| T1b | `TaskSuite.check()` | same | Every 0.1.35-based environment reports "The task is not injectable" for all 16 tasks; 0.1.29 reports OK. **Cause, verified:** in 0.1.35, `is_task_injectable` keeps only tool outputs whose `content` is a `str`, but 0.1.35 content is a list of blocks. This is a defect in AgentDojo's self-check, not in scoring (T1 is unaffected). | same |
| T2 | DRIFT on 0.1.35 banking v1/v1.2, official code unmodified, **test-double client** (six cases) | `itest_drift.py` | **PASS (interface).** All modules are reached: privilege assignment (11 calls), planning, detector, checklist formatting, alignment judge. AgentDojo scores DRIFT's message format. With a "No" judge, the off-plan `update_password` is refused (`[CALL ERROR]`). With an echoing detector, the injected sentence is masked and the obedient double no longer sees it. With a detector that finds nothing, the injected `send_money` passes, because it uses a planned tool and the checklist leaves the recipient open. **Every outcome is set by the scripted answers; none is a security result.** | `results/itest_drift.json`, `logs/itest_drift.log` |
| T3 | Progent's official `secagent` (`3e79753`) on PyPI 0.1.35 with the manual policy of `9befb41`; reference solutions | `itest_progent.py` | **PASS (enforcement).** v1: benign references 13/16 solved (16/16 without Progent); injection references 0/144 goals reached (144/144 without). v1.2: 14/16 and 0/144. Blocked legitimate calls: `update_password` (no rule), `send_money` in `user_task_5` and `_11`, and in v1 `user_task_15` (landlord IBAN = attacker IBAN). **These are reference-solution counts, NOT an ASR.** | `results/itest_progent.json`, `logs/itest_progent.log` |
| T4 | AgentDyn: import, defence list, banking v1 loads, pipeline construction with no request (socket connects blocked) | `itest_agentdyn.py` | **PASS** for none, repeat_user_prompt, spotlighting, tool_filter, drift, progent, camel. **FAIL** for transformers_pi_detector, piguard_detector and prompt_guard_2_detector: `torch` and `transformers` are not installed, and huggingface.co is unreachable. | `results/itest_agentdyn.json` |
| T5 | MELON harness tests (existing) | `tests/test_rem_vs_melon.py` in `melon029` | **9 passed** | console |
| T6 | Test of this audit's outputs; full repository suite | `tests/test_external_defense_audit.py`; `pytest` | **4 passed**; full suite **817 passed, 27 skipped, 1 xfailed, 0 failed** | – |

**Not executed:** a live MELON run, which needs OpenAI embeddings and an agent model.

## Failures and dependency conflicts

- **Transformer-based detectors:** they cannot be built without `torch`/`transformers` and model downloads, and Hugging Face is blocked.
- **The DRIFT venv** must not share an environment with AgentDyn: both install a package named `agentdojo`.
- **The Progent fork** (0.1.29) and PyPI 0.1.35 cannot coexist in one venv.
- **MELON** requires 0.1.29, so it needs its own venv.

## Remaining blockers for live tests

| Blocker | Evidence |
|---|---|
| No agent model endpoint: api.openai.com and openrouter.ai give no response | `results/environment_check.json` |
| Hosts reachable but unused: generativelanguage.googleapis.com and api.anthropic.com return 404 at the root | same |
| No provider key variable | same |
| No local model server (ports 8000, 8080, 11434 closed), no GPU, and model downloads blocked | same |
| No spending authorisation and no price list | – |

The reachable hosts would still need an account, a key and spending authorisation. Using them is a supervisor decision (`07` §9).
