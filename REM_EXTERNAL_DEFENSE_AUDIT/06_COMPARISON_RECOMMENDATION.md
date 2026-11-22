# 06 Comparison recommendation (22 November 2026)

## 1 Criteria applied

| # | Criterion |
|---|---|
| 1 | same threat model |
| 2 | same banking tasks |
| 3 | comparable attacks |
| 4 | same agent and LLM |
| 5 | same tools and permissions |
| 6 | reproducible official code |
| 7 | feasible requirements |
| 8 | a meaningfully different mechanism |

## 2 Decision per candidate

| Arm | Candidate | Criteria met | Decision | Kind of comparison |
|---|---|---|---|---|
| D0 | AgentDojo native agent, no defence | all | **include** | reference |
| D1 | REM v1.0 (frozen, step-level, no reviewer) | all | **include** | – |
| D3a | **Progent, authors' manual banking policy** (`9befb41`, unmodified; enforcement code `3e79753`) | 1–8. Same native agent and same tool boundary as REM; deterministic; no extra model. | **include, primary external comparator** | **direct** |
| D3b | Progent, LLM-generated policy with updates (paper default) | 1–6, 8; 7 needs a policy model | **include if a model is authorised** | direct (the policy model must equal the agent model) |
| D2 | DRIFT, all three modules (official CLI, `--benchmark_version v1`) | 1–3, 5–8. **4 fails**: DRIFT replaces the agent with its own prompting scaffold. | **include with control arm D2c** | **direct on episode outcomes; mechanism attribution only relative to D2c** |
| D2c | DRIFT scaffold, no modules (official CLI, no flags) | control | **include together with D2** | control |
| D4 | MELON (official file, `text-embedding-3-large`) | 1–6, 8; 7 blocked (OpenAI embeddings; AgentDojo 0.1.29) | **conditional**; NO-GO now | direct on outcomes, with a documented environment difference |
| N1 | AgentDojo `tool_filter` | all with an OpenAI model | **optional live**; descriptive from recorded runs already in R8 | recorded: descriptive |
| N2 | `transformers_pi_detector` | needs a Hugging Face download | **descriptive only** (recorded runs in R8) | descriptive |
| – | spotlighting, repeat_user_prompt | low value | **exclude** from new runs (already reported descriptively in R8) | – |
| – | `Agentic-AI-Risk-Mitigation/progent` | fails 6: not the authors' implementation | **exclude** | – |
| – | AgentDyn as a defence | it is not a defence | **exclude as an arm** | infrastructure; secondary cross-check only |
| – | CaMeL | it redesigns the agent (code-generating interpreter), a different system architecture; not requested | **exclude** (could be cited as related work) | – |

## 3 Smallest scientifically meaningful design

**Core design, which runs without any paid model.**
- **What is compared:** REM v1.0 and Progent with the authors' manual policy (D3a), both deterministic.
- **Where:** at the same tool boundary, on the same calls.
- **On what:**
  1. AgentDojo's reference solutions. Executed here: Progent in `02` §4.
  2. The recorded AgentDojo traces, by offline replay: REM is already replayed on them. Progent's checker was replayed on them in the 18 Nov study (`REM_PROGENT_COMPETITIVE_2026_11_18`).
- **Status:** descriptive, offline evidence. It answers "what does each decision rule withhold on identical proposed calls?". It does **not** give an ASR.

**Smallest live design** (needs authorisation):
- arms D0, D1 (REM), D3a (Progent-manual), D2 (DRIFT) and D2c (DRIFT scaffold);
- banking v1, all 144 attacked pairs and 16 benign tasks;
- one agent model shared by all arms;
- repeats as decided by the supervisors.

Add D3b and D4 when a policy model and OpenAI embeddings are authorised.

**Why these arms.**
- **Progent:** the closest mechanism-level rival. It works at the same tool boundary, under the same threat model and with the same agent. It is deterministic and needs no model in its manual form. It gives the most interpretable direct comparison.
- **DRIFT:** the strongest *system-level* rival in the same benchmark version (0.1.35), with NeurIPS 2025 peer review. Because it changes the agent, its comparison is about outcomes. The scaffold control prevents attributing scaffold effects to its defence.
- **MELON:** a third mechanism, detection by masked re-execution, with a harness already frozen. It is kept but conditional.

## 4 What cannot be claimed under any of these designs

- Superiority of REM over a defence that has not been run under the same agent, model and repeats.
- Generality beyond the AgentDojo banking suite.
- Comparability with the authors' published numbers: DRIFT's are on v1.2 with gpt-4o-mini; Progent's are aggregated over suites with gpt-4o.
