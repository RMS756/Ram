# 03 AgentDyn audit (22 November 2026)

Labels as in `01`. **AgentDyn is treated as benchmark and evaluation infrastructure, not as a defence.**

## 1 What it is

| Item | Finding | Label |
|---|---|---|
| Paper | *AgentDyn: Are Your Agent Security Defenses Deployable in Real-World Dynamic Environments?*, Hao Li, Ruoyao Wen, Shanghao Shi, Ning Zhang, Yevgeniy Vorobeychik, Chaowei Xiao; arXiv:2602.03117 (2026), preprint | VERIFIED (OpenAlex W7127632747) |
| Kind | **A benchmark plus an evaluation harness.** It contributes 60 open-ended user tasks and 560 injection cases in three new suites (shopping, github, dailylife), plus wiring that runs third-party defences. It proposes no defence of its own. | PAPER-REPORTED (abstract); VERIFIED (code) |
| Repository | `github.com/SaFo-Lab/AgentDyn` at `5353cf7` (19 May 2026). The paper's abstract names `github.com/leolee99/AgentDyn`; that repository was not checked. | VERIFIED |
| Package | a **fork of AgentDojo** that installs as `agentdojo` version **0.1.35**. It replaces PyPI AgentDojo in any environment where it is installed. | VERIFIED |
| Licence | MIT; the licence file is AgentDojo's | VERIFIED |

## 2 Supported defences

| Defence | Source | Label |
|---|---|---|
| tool_filter, transformers_pi_detector, spotlighting_with_delimiting, repeat_user_prompt | AgentDojo's own | VERIFIED |
| piguard_detector, prompt_guard_2_detector | added; Hugging Face models | VERIFIED (construction fails here without `torch`/`transformers` and model downloads) |
| **drift** | vendored copy under `src/agentdojo/defenses/drift`; **differs from `SaFo-Lab/DRIFT@6fd3df4`** in `DRIFTLLM.py` (refusals sent as tool-error messages), `DRIFTToolsExecutionLoop.py` (error detection) and `prompts.py` (a changed adaptive-attack string) | VERIFIED (diff) |
| **progent** | vendored `secagent`; **differs from `sunblaze-ucb/progent`** (`policy_analysis.py`, `role_analyzer.py`, `tool.py`). AgentDyn wraps `runtime.run_function` with `check_tool_call` and **always calls `generate_security_policy(query)`**, so only the LLM-generated mode is available. The published manual banking policy is not used. | VERIFIED |
| **camel** | vendored CaMeL tree | VERIFIED (it constructs; not audited further, as it is out of scope here) |
| MELON | **not integrated** | VERIFIED |

**Construction test** (`results/itest_agentdyn.json`, no request sent, socket connects blocked during construction):
- **Built successfully:** no defence, repeat_user_prompt, spotlighting_with_delimiting, tool_filter, drift, progent, camel.
- **Failed:** the three transformer detectors, with an ImportError because `torch` and `transformers` are not installed.

VERIFIED.

## 3 Banking compatibility and semantic changes

| Question | Finding | Label |
|---|---|---|
| Original banking suite present | yes: `default_suites/v1/banking` and `data/suites/banking` are **byte-identical** to PyPI 0.1.35 | VERIFIED (diff, file hashes) |
| Same scoring on banking | on AgentDojo's reference solutions, all 16 benign tasks and 144 pairs are scored identically to PyPI 0.1.35, for v1 and v1.2 | VERIFIED (`results/fingerprint_agentdyn.json`) |
| Benchmark-semantics changes | (1) The **default system message** adds "Complete all tasks automatically without requesting user confirmation." This changes the agent's instructions for *every* suite, banking included, and differs from the system message under which REM's recorded population was produced. (2) `model_output_from_messages` uses the last assistant message instead of raising. (3) A `JSONDecodeError` during a run is **scored as utility = False and security = True** (counted as an attack success). (4) Model registry and OpenAI-client tolerance changes. | VERIFIED (diff) |
| Attack definitions | attack files unchanged (`attacks/important_instructions_attacks.py`, `baseline_attacks.py`: same hashes) | VERIFIED |
| Banking runs distributed | **none**; the `runs/` directory holds only shopping, github and dailylife | VERIFIED |
| Same tasks and attacks across defences | yes, within the fork: one command line, `--defense <name>` | VERIFIED (code) |
| Metrics | AgentDojo's utility and security per episode; no latency, call-count or cost instrumentation beyond AgentDojo's logs | VERIFIED |

## 4 Would it reduce duplicated work for REM?

**Partly, but it is not suitable as the primary harness.** Reasons, all VERIFIED:
1. It changes the agent's default system message and the error scoring. A REM comparison run inside it would not be on the authentic AgentDojo 0.1.35 benchmark used by REM's frozen evidence.
2. Its DRIFT and Progent are modified vendored copies, not the official revisions. Its Progent is generated-policy only.
3. REM is not one of its defences. Adding REM requires editing the fork's `DEFENSES` list and pipeline factory, which is a change to the benchmark harness.
4. It has no MELON, and the MELON comparison needs AgentDojo 0.1.29 anyway.

**Where it can help.** It can serve as a **secondary cross-check** for DRIFT and Progent numbers produced with the official repositories. If the two harnesses disagree, the disagreement is itself informative. It is also a future extension for "dynamic environments", but that is a new benchmark scope and needs supervisor approval (CLAUDE.md, external benchmarks unresolved).
