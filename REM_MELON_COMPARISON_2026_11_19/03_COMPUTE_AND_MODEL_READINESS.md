# 03 Compute and model readiness (inspected 19 November 2026; no credential value was read or printed)

## Machine

| Item | Finding |
|---|---|
| OS | Linux 6.18 x86_64 (cloud container) |
| CPU | 4 × Intel Xeon @ 2.10 GHz, 1 thread per core |
| RAM | 15.7 GiB total, about 15 GiB free; no swap |
| GPU | **none** (`nvidia-smi` absent; no CUDA device) |
| Disk | 15 GB available on `/` (a per-session allowance) |
| Python | 3.11.17 |
| Main environment | AgentDojo 0.1.35, NumPy 2.4.6, SciPy 1.17.1, scikit-learn 1.9.1; **no torch or transformers** (`manifests/pip_freeze_main.txt`) |
| MELON environment | `/home/user/venvs/melon029`: AgentDojo 0.1.29, openai 3.46.0, torch 2.9.1 (CPU), transformers 5.22.1 (`manifests/pip_freeze_melon029.txt`) |

## Model serving and endpoints

| Item | Finding |
|---|---|
| Ollama, vLLM, llama.cpp server binaries | not installed |
| Local OpenAI-compatible endpoints (127.0.0.1:8000, :11434) | not reachable |
| Hugging Face model cache | absent (`~/.cache/huggingface` does not exist) |
| Model-provider credential variables | **none set** for OpenAI or other providers. The session's own `ANTHROPIC_BASE_URL` belongs to the coding assistant's infrastructure and was not used. |
| Embedding endpoint | none |

## Network (this session's environment: "Default", limited, package registries only)

| Host | Result | Needed for |
|---|---|---|
| pypi.org | reachable | software only; no model weights |
| huggingface.co, cdn-lfs.huggingface.co | **blocked** (proxy 403) | open-weight models (e.g. Qwen2.5 / Llama 3.x instruct GGUF) |
| modelscope.cn, hf-mirror.com, registry.ollama.ai, ollama.com, gpt4all.io | **blocked** | alternative model sources |
| api.openai.com | **blocked** | agent model and **MELON's hard-coded `text-embedding-3-large`** |
| platform.openai.com, openai.com/api/pricing | **blocked** (also from the web-fetch tool) | documented prices |
| openaipublic.blob.core.windows.net | **blocked** | tiktoken tokenizer files, needed for exact token counts |
| github.com (anonymous git) | reachable for public repositories via the git proxy | MELON source (cloned) |

**Can the network be widened from inside this session?**
- This session runs on the user's **Default** environment.
- The environment saved for this repository, **"ram-thesis-research"** (allowed host: arxiv.org), cannot be switched to while the session runs.
- Allowing a host for one repository on the shared Default environment is outside what this session may propose.
- **Therefore no network change was requested.**

## Feasibility of a zero-cost local configuration

| Requirement | Status |
|---|---|
| Open-weight instruction model with tool calling | **cannot be obtained** (all model hosts blocked) |
| CPU inference capacity | 4 cores and 15 GiB RAM fit a quantised 7–8B model in memory, but **throughput could not be measured without weights**. The workload is 2,248 model calls and about 15.4 million prompt characters for one repeat of the full design (`results/workload_estimate.json`). On a 4-core CPU this is expected to take many hours to days, but **no figure is given because none was measured**. |
| MELON embeddings | the published configuration needs OpenAI `text-embedding-3-large`; **blocked**. A local embedding model would make the arm "MELON-ADAPTED-EMBEDDINGS", not MELON. The runner supports it only under that label. |

## Paid-API cost

- **Not authorised and not estimated in dollars.** No provider price page is reachable to verify current prices, and the task forbids guessing them.
- **What is measured** (`results/workload_estimate.json`, from the 160 recorded gpt-4o banking trajectories):

  | Workload | Value |
  |---|---|
  | Agent calls per arm | 602 |
  | Agent input characters per arm | 3.52 M |
  | Agent output characters per arm (lower bound) | 0.076 M |
  | MELON extra masked calls | 442 |
  | MELON extra masked input characters | 4.87 M |
  | MELON embedding calls (upper bound) | 884 |
  | Full design, one repeat: model calls | 2,248 |
  | Full design, one repeat: input characters | 15.4 M |

- **Dollar formula** (`10`): cost = Σ input tokens × input price + Σ output tokens × output price + Σ embedding tokens × embedding price. The tokens come from a tokenizer applied to the logged requests, or from the provider's reported usage. The prices come from the provider's list on the run day. The runner's spending guard enforces a cap.

## Verdict

**The primary closed-loop comparison is BLOCKED in this session.** There is:
- no model, local or remote;
- no embedding endpoint;
- no spending authorisation;
- no network path to obtain either.

Everything else was completed:
- the harness and fail-closed runner;
- the scripted integration pilot of all three arms with **unmodified official MELON**;
- tests;
- the frozen protocol;
- the workload measurement.
