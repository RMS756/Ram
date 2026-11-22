# 05 Compatibility matrix (22 November 2026)

**Evidence labels**

| Label | Meaning | How it was obtained here |
|---|---|---|
| **V** = VERIFIED | confirmed from code or executed tests | this project, 22 Nov 2026 unless dated otherwise |
| **P** = PAPER-REPORTED | stated in the paper | — |
| **D** = DOCUMENTED | stated in the official repository documentation | — |
| **NV** = NOT VERIFIED | not established | — |
| **NS** = NOT SUPPORTED | incompatible or unavailable | — |

For the four defences:
- REM: `rem/` at `9fddfa7`.
- DRIFT: `SaFo-Lab/DRIFT@6fd3df4`.
- Progent: `sunblaze-ucb/progent@3e79753`, with the manual policy from `9befb41`.
- MELON: `ucsb-mlsec/MELON@06014c7`.

| Criterion | REM v1.0 | DRIFT | Progent | MELON |
|---|---|---|---|---|
| Runtime protection | yes: per-call gate before execution (V) | yes: inside the agent step (V) | yes: tool wrapper before execution (V) | yes: per-step detector around the agent LLM (V) |
| Indirect prompt-injection defence | yes (V; design) | yes (V; P) | yes (V; P §3.2) | yes (V; P) |
| Context / provenance evidence | yes: provenance labels; `x_act1` argument provenance; `x_ctx2` pattern detector (V) | partial: an LLM detects "conflicting instructions" in tool results; no value provenance (V) | no: rules see only the current call's arguments (V; P Fig. 2b) | no explicit provenance; it compares behaviour with tool outputs masked (V) |
| Behavioural analysis | yes: `x_beh1`–`x_beh4` over the episode history (V) | plan-deviation tracking against an LLM-made trajectory (V) | none in the rules; LLM policy updates use the call history (V) | masked re-execution similarity per step (V) |
| Tool-call enforcement | yes: the call is withheld and the refusal returned (V) | yes: the call is removed and a `[CALL ERROR]` message sent (V) | yes: `ValidationError` returned as a tool error (V) | yes: the run stops on detection (V; earlier audit) |
| Tool authorisation | learned expected-loss verdict plus predicates D1/D2 (V) | Read/Write/Execute privileges from the LLM; LLM alignment judge (V) | symbolic allow/forbid rules per tool and argument (V) | none: detection only (V) |
| Mitigation actions | Allow / Modify / Escalate / Block. With step-level semantics and no reviewer, the last three all withhold (V) | refuse and continue; mask the injected text (V) | block with a message, terminate, or ask the user; the paper default is the message (V; P) | stop the agent (V) |
| AgentDojo compatibility | 0.1.35 offline replay (V); live harness built in 0.1.29 and tested with a scripted agent only (V); live: NV | 0.1.35, no patch (V) | official: a 0.1.29 fork (V); wrapper on PyPI 0.1.35 (V, this audit) | 0.1.29 only (V) |
| Banking task compatibility | banking v1, all 16 × 9 (V) | v1 and v1.2 via flag (V); authors' runs are on v1.2 (V) | v1 and v1.2 (V). The manual policy blocks 4 benign v1 reference tasks (3 in v1.2) (V) | v1 (V, scripted pilot) |
| Requires an external LLM (besides the agent) | **no** (V) | **yes**: every module is LLM-based, and DRIFT replaces the agent LLM element (V) | manual policy: **no** (V); generated policy: **yes** (V) | uses the agent LLM for re-execution: **yes** (V) |
| Requires an embedding model | no (V) | no (V) | no (V) | **yes**: `text-embedding-3-large` (V) |
| Additional model calls per episode | 0 (V) | measured with a test double: 20 calls for a 2-call benign task, 11 of them once per agent instance (V); tokens: median 15,124 per attacked episode in the authors' runs (D) | manual: 0 (V); generated: ≥ 1 per task plus updates (V for code paths; counts NV) | about one masked re-execution per agent step, plus embeddings per tool call (V, earlier audit; counts NV live) |
| CPU execution feasibility | yes: median 0.151 ms per call in offline replay (V, ablation study 21 Nov) | defence logic yes; all model calls remote (V) | manual: yes (V); generated: remote model (V) | defence logic yes; embeddings and LLM remote (V) |
| Estimated integration complexity | done (frozen harness) | low: official CLI, plus a results adapter and a scaffold-control arm | low (manual, wrapper route verified) to medium (generated mode, fork route) | done (frozen harness); blocked by its requirements |
| Official reproducible implementation | yes, this repository (V) | yes, MIT (V) | yes, `sunblaze-ucb/progent`, MIT (V). `Agentic-AI-Risk-Mitigation/progent` is a third-party re-implementation (V) | yes, but no licence file (V) |
| Live closed-loop result available here | **NOT EXECUTED** | **NOT EXECUTED** | **NOT EXECUTED** | **NOT EXECUTED** |

## Native AgentDojo defences (0.1.35)

| Defence | Mechanism | Extra requirement | Recorded runs available | Fit for comparison |
|---|---|---|---|---|
| tool_filter | an LLM picks the tools before the run | OpenAI model (V) | gpt-4o-2024-05-13, 144 + 16 (V; analysed in R8 `07`) | yes: strongest recorded native baseline (16 / 144 attack successes) |
| transformers_pi_detector | DeBERTa classifier on each tool output; it stops the run | `torch`, `transformers`, a Hugging Face download (V); huggingface.co unreachable (V) | yes (V) | yes, descriptive (recorded) |
| spotlighting_with_delimiting | delimiters plus a system-prompt warning | none beyond the agent (V) | yes (V) | low value: 89 / 144 vs 90 / 144 undefended (R8) |
| repeat_user_prompt | re-inserts the query after each tool call | none (V) | yes (V) | low value as a security baseline |

## AgentDyn (infrastructure, not a defence)

- **Fork:** AgentDojo 0.1.35, with banking files byte-identical and banking scoring identical on reference solutions (V).
- **Changes:** the default system message, error scoring, and its own copies of DRIFT and Progent (V).
- **Recommended role:** secondary cross-check only (`03`).
