# 1. Source of truth and closest prior art

**Date:** 13 November 2026. **Status:** investigation record; nothing here changes the approved REM design.

## 1.1 Source of truth

| Item | Finding |
|---|---|
| Last reviewed state | Branch `claude/rem-final-thesis-nov20`, commit `1e84c141` (12 November 2026) |
| Newer work on the remote | None. `git fetch` on 13 November: the newest remote commits are `1e84c14` on `claude/rem-final-thesis-nov20` and on `claude/rem-algorithm-implementation-3ktvze` (same commit). The `codex/*` and `claude/rem-authz-generalization-study` branches are older (11 November) and are ancestors or were reviewed in the earlier study |
| Branch of this study | `claude/rem-improvement-study`, created from `1e84c14` |
| Frozen items kept intact | `rem/`, `configs/` (including `configs/exploratory/pilot_e0.yaml`), every earlier result file, the MELON bundle (`sha256 983c5b0d…`), the thesis edition of 12 November (`REM_FINAL_SUBMISSION/thesis/`) |
| New code | Only under `experiments/improve_study/` and `tests/test_improve_study.py`. No shared module was edited. The study imports the earlier study's fitting and replay routines unchanged |
| Equivalence of frozen paths | Checked by the run itself: the refit of the v1.1 feature set reproduces the stored fits (maximum absolute difference 0.00e+00), and the seven earlier arms reproduce the stored counts on both populations (`results/improvement_results.json`, key `frozen_path_equivalence`: all true) |
| Design status | REM v1.0 remains the design of record. REM v1.1 remains a proposed amendment (decision SD-FEAT pending). Everything in this folder is labelled proposed and exploratory |

Facts carried over unchanged from the reviewed state: v1.0 105 of 334 benign tasks and 11 of 2,979 attacks; v1.1 an ablation of v1.0; 916 against 1,074 of 2,113 (+7.48 points, interval 1.17 to 16.02); 18 against 25 of 48 benign tasks (interval touches zero); 3 against 1 of 2,065 attacks (not a statistical superiority); rule A2 1,232 of 2,113 with 4 attacks; double holdout 14 against 11 attacks for v1.1; the rejected candidate with 132 attacks; the delegated-document rule with 313 attacks (not reintroduced); M01 with 1,115 of 2,113 and 3 attacks (not a contribution). The 2,113 formerly confirmatory episodes are development evidence from now on.

## 1.2 What was read, and at what level

`arxiv.org`, `aclanthology.org` and `proceedings.mlr.press` are outside the network policy of this session. The full-text review packet for NEXUS, aiAuthZ and Kairos was not among the files uploaded to the session (the upload directory holds the six PDFs of 11 November only). Official code repositories on GitHub were reachable and were cloned read-only; nothing from them was executed.

| Work | Identifier | What was read in this project | Level |
|---|---|---|---|
| Task Shield (Jia et al.) | ACL 2025, long paper 1435 | PDF supplied 11 November | Full text |
| MELON (Zhu et al.) | ICML 2025, PMLR 267 | PDF supplied 11 November; official code `kaijiezhu11/MELON` at `4d3cc9c` (bundles AgentDojo 0.1.29) | Full text + code |
| PROVISO (Yan et al.) | arXiv:2610.27115v1 | PDF supplied 11 November | Full text |
| Calibration Is Not Control (Zhang et al.) | arXiv:2606.21399v2 | PDF supplied 11 November | Full text; code not accessed |
| AgentBoundary; CASEL | arXiv:2609.33658v1; arXiv:2610.36570v1 | PDFs supplied 11 November | Full text |
| Progent (Shi et al.) | arXiv:2504.11703 | Official code `sunblaze-ucb/progent` at `9befb41` (10 September 2025) and at HEAD `b02783b` (26 October 2026): README, `secagent/tool.py`, the banking suite file with the manual policy, `agentdojo/run.sh` | **Code only; paper not read** |
| CaMeL (Debenedetti et al.) | arXiv:2503.18813 | Official repository `google-research/camel-prompt-injection` at `f083b6b` (20 June 2025): README only | **Repository README only; paper not read in this session** |
| NEXUS (Hossain et al.) | Findings of AACL 2026, DOI 10.18653/2026.findings-aacl.112 | Published abstract; authors' repository `eliashossain001/nexus` at `36d7e0b` (25 July 2026): README (sha256 `a48e7de8…`, identical to the copy stored on 1 November) and the working documents `run_complete/paper_update_final.md` and `docs/reports/arr_mvr/day6_formalization.md` | **Abstract + repository; paper not read** |
| aiAuthZ (Kodathala) | arXiv:2607.05518 | Abstract; authors' repository `Sports-Vision-Inc/aiAuthZ` at `6eaac86` (6 July 2026): README, `docs/WHITEPAPER.md`, `docs/RELATED_WORK.md`, `experiments/agentdojo/aiauthz_defense.py` | **Abstract + repository whitepaper; arXiv text not read** |
| Kairos (Hempel et al.) | arXiv:2610.18457 | Abstract (index record) | **Abstract only** |
| XGBoost | optional in the brief | Not used; no learned comparison beyond ridge logistic regression was run | — |

Statements below about a work are limited to the level in this table. Repository documents are the authors' own material but are not the published paper; where a repository document and an abstract differ, both are given.

## 1.3 Closest-prior-art matrix for the candidate family

| Work | Mechanism (at the level read) | What the candidate borrows | What differs | What the work does not support here |
|---|---|---|---|---|
| **Task Shield** | Extracts task instructions per privilege level with a language model; an instruction or tool call is misaligned iff its total ContributesTo score against the user's instructions is 0 (Defs. 1–4, Eqs. 1–2) | The principle that an action is judged against what the user-level request asks for; the remark (Sec. 3.2) that a tool output may define subtasks when the user delegates | The candidate uses a deterministic parser and typed matching, with no model call; it checks material arguments (recipient, amount, credential), which the alignment score does not do explicitly | No evidence about deterministic parsing; its reported figures are live-agent GPT-4o results and are not comparable with replay |
| **Progent** (code) | Per-tool policies with argument restrictions in JSON-schema form, checked deterministically before each tool call (`secagent/tool.py`); policies are written by hand (commit `9befb41`, banking: allow-list of five recipients, no entry for `update_password`) or generated and updated by a language model (HEAD) | Least-privilege, argument-level, deterministic checking before execution; the manual banking policy is **run here as the published comparator (arm PG)** | The candidate derives the permitted recipient, amount and operation from each request at run time; Progent's manual policy is one fixed list for the suite | The paper's numbers are not reproduced; the generated-policy mode needs a model and was not run; the equivalence of this project's decision function to the upstream checker is by inspection, not by executing upstream code |
| **CaMeL** (README) | Separates control and data flow extracted from the trusted query; capabilities attached to values are enforced at tool-call time (as described in the README and in aiAuthZ's related-work note) | The principle that untrusted data must not grant operations | No interpreter, no capability tracking; the candidate is not called CaMeL and is not an adapter of it | Nothing was measured |
| **MELON** | Masked re-execution: compares tool calls with and without the user prompt by embedding similarity (threshold 0.8) | Nothing in the mechanism. Planned comparator in the sealed prospective protocol | No language model or embedding in the candidate | Not executed (no model, no embedding service) |
| **PROVISO** | Provenance-typed memory of trusted and external observations; a learned controller scores committing the proposed action against an alternative at the commitment point (Eq. 7) | Typed provenance of evidence; decision at the commitment point | No learned controller of that size; no restored rollouts | Its stated limitation ("fitted separately for each benchmark … we do not study transfer") leaves the transfer question open |
| **Calibration Is Not Control** | A calibrated score does not by itself give a good intervention decision | The verifier gate is defined on permission status, not on the predicted probability alone; the decision variant is evaluated by outcomes, not by calibration | — | Its intervention-value target was tested earlier in this project and failed on a held-out objective; it is not repeated |
| **NEXUS** (abstract + repository) | Rule-first cascade over structured plans: deterministic rules, an argument inspector and a calibrated logistic-regression scorer select allow, revise, confirm or block | Nothing new; it is the published form of "rules first, learned score second" | NEXUS scores whole plans on labelled plan sets; the candidate scores each call in replayed benchmark episodes against the user's request | The repository's working document reports that the scorer gives no binary detection gain over rules alone (McNemar p = 1.0) and that its contribution is to four-class intervention accuracy (0.6406 against 0.3672 for rules only). This is a repository document of 23 May 2026, not the paper |
| **aiAuthZ** (abstract + repository) | Off-host gateway: per-message HMAC identity, role allow-lists, argument-level constraints, rate limits, hash-chained audit, signed receipts | The idea of a "known payee" list; here established payees are read at run time from structured bank records that the user originated and count only when the request refers to them | aiAuthZ's trust comes from a signed identity channel outside the agent; the candidate has no such channel and uses the request text only | Its AgentDojo banking run (whitepaper §6.9: AgentDojo 0.1.35, 20 task pairs, one model, a fixed allow-list of five recipients, `update_password` denied) reports 0% attack success with 6 blocked attacker-directed calls and clean utility falling from 100% to 80% because one legitimate first-time payment was blocked. The arXiv abstract recorded on 11 November states seven blocked calls; the difference between versions is not resolved here. The whitepaper itself lists "a head-to-head on AgentDojo against CaMeL/Progent" as not yet done |
| **Kairos** (abstract) | Reference monitor at the isolation boundary with deferred effects | Nothing | Acts on effects below the agent | Not assessed beyond the abstract |

Two observations follow from the code that was read. First, both published deterministic policies for the AgentDojo banking suite (Progent's manual policy and aiAuthZ's benchmark policy) are fixed allow-lists of the payees that exist in the seeded environment, with password change denied. Second, neither derives permission from the individual request. That is the place of the candidate; it is an engineering combination of published ideas, and **no novelty is claimed for it**.

## 1.4 AgentDojo versions

| Component | Version |
|---|---|
| Recordings replayed in this project | AgentDojo 0.1.35, banking suite v1, runs commit `089ed468…` |
| Progent repository at `9befb41` | bundles AgentDojo 0.1.29 (`agentdojo/pyproject.toml`) |
| MELON repository at `4d3cc9c` | bundles AgentDojo 0.1.29 |
| aiAuthZ benchmark run | AgentDojo 0.1.35 (whitepaper §6.9) |

The mismatch matters for live runs, where the benchmark's agent pipeline is executed. It does not affect arm PG as run here: the manual policy is a function of the tool name and arguments only, and the eleven banking tools have identical parameter names and default values in both versions (checked on 13 November by parsing the tool source files of the bundled 0.1.29 and of the installed 0.1.35; the policy file itself was parsed as data and its hash pinned, `experiments/improve_study/progent_manual.py`). A live comparison must use one version for all conditions; the sealed prospective protocol fixes 0.1.29 for that reason.
