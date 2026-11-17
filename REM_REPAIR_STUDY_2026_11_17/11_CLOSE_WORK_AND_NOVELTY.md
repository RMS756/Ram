# Close work and what REM's experiments actually resolve (17 November 2026)

Network status of this session: arxiv.org, proceedings.mlr.press, api.openalex.org and chatpaper.com are **not reachable**. Metadata were checked through the scholarly index (OpenAlex records via the FastTrack connector) and Crossref. Two authors' repositories on GitHub were read as data and not executed. Reading levels are stated per work. **Metadata verification is not full-text reading.**

## 1. Works reviewed

| Work | Identity (verified against) | Publication status | Reading level | What it does | Overlap with REM |
|---|---|---|---|---|---|
| **Progent** (Shi, He, Wang, Li, Wu, Guo, Song) | arXiv:2504.11703v3 | preprint | **full text** (v3, 16 Nov 2026); code read, not executed | privilege-control policies over tool calls; manual or model-generated, optionally updated after tool results | argument-level allow/deny policies on recipients and other arguments. REM's PG arm is its static manual banking policy, adapted to replay |
| **CaMeL** (Debenedetti et al.) | arXiv:2503.18813v2 | preprint | official repository README; banking security policy file read in a third-party copy (ROPE repo) | privileged/quarantined LLMs, capability-tagged data flow, policies at tool calls | provenance of arguments; banking policy checks that recipients can read the amount |
| **Task Shield** (Jia, Wu, Qin, Squicciarini) | ACL 2025 Long Papers, aclanthology 2025.acl-long.1435 | peer-reviewed (ACL 2025) | **full text** (11 Nov 2026) | LLM-judged alignment of each action with user goals | per-call test of whether the action serves the request |
| **NEXUS** (Hossain, Nipu, Ornee, Rana, Yousefi) | Crossref: 10.18653/2026.findings-aacl.112, *Findings of the ACL: IJCNLP-AACL 2026*, pp. 2203–2232 | peer-reviewed (Findings) | abstract + authors' repository (commit 36d7e0b); full text **not** read | structured runtime safety layer for tool-using agents | runtime interception and structured checks |
| **PACT** (Fan, Li, Tian, et al.; 6 authors, 3 known to this session) | OpenAlex W7160999798; arXiv:2605.11039 | preprint | **index abstract only** | role-specific trust contracts per tool argument; cross-step provenance; AgentDojo, 5 models | argument-level authority binding: the closest conceptual match to REM's authority front |
| **ROPE** (Ma, Xiao, Yeoh, Zhang, Vorobeychik) | OpenAlex W7204855727; arXiv:2608.27496; author list from the authors' repository README (github.com/xhOwenMa/ROPE, commit ffe27c4) | preprint | abstract + repository README + banking parameter table | a value may reach a state-changing tool only if it traces to the user, a source the user named, or the user's own records; deterministic origin check; LLM router reads only the request | origin rule for values including "the user's own records" (cf. REM's `record_refund` rule). Its audited **banking floor guards `recipient` only, not `amount`** (`src/rope/scopes/_floor/banking.json`); per-task routers may add parameters, not inspected |
| **CapLite** (Xu, Liu, Nakayama) | OpenAlex W7226018652; arXiv:2611.17115 (November 2026) | preprint | **index abstract only** | policy derived from tool schemas; write calls committed before tool results are read; a write is admitted only if every argument deciding whom or what it affects (recipient, amount, object, destination) is **stated in the user's request** | almost the same admission rule as REM's front plus a literal-amount check. It reports zero attack success in 13,935 attacked AgentDojo episodes |

Also found in the same searches, abstracts only and not reviewed: PACE (arXiv:2610.01349), CXI (arXiv:2607.06000), SPILLWAY (arXiv:2611.07222), Conflux (arXiv:2611.08768). Each describes deterministic argument- or effect-level admission at the tool boundary.

## 2. Consequences for novelty claims

None of the following can be presented as unexplored:
- runtime interception at the tool-execution boundary;
- argument-level checks of recipients and amounts against the user's request;
- deterministic admission with an LLM restricted to the trusted request;
- record-based origin of values;
- financial specialization (AgentDojo banking is used by most of the works above);
- hybrid designs (rule plus learned or LLM component).

CapLite's stated rule ("no write reaches a recipient, amount, object or destination that the user did not state") overlaps directly with REM's authority front and the literal-amount part of the typed verifier.

## 3. A precise question REM's evidence can answer

**[PD — proposed wording, not an approved research question]** *On recorded AgentDojo banking trajectories, does a calibrated learned expected-loss decision placed after a deterministic request-derived authority front change attack outcomes or task completion? And what do exact verification of request-derived payment amounts, and its absence, cost and prevent?*

What the experiments resolve:
- In these recordings, every attack-labelled call stops at the deterministic front. The learned decision changes nothing measurable: HV = GV, HV_math = GV_math, and the threshold variants match except NP01, which loses tasks.
- The frozen front accepted unverified derived amounts (C1) and the lexical constraint misread coefficients (C2, R5). The typed verifier removes these at a cost of 95 and 159 tasks, whose amounts cannot be verified from the request.
- The comparison with Progent covers only its static manual policy in replay, and the intervals include zero.

What they do not resolve:
- live behaviour;
- generated Progent policies;
- comparison with PACT, ROPE or CapLite, none of which was run;
- adaptive attacks;
- the residual stage where the request delegates the amount (R1, R2b). No arm here protects that stage, and no labelled data for it exist.

Distinguishing features that remain, stated as design differences, **not** as demonstrated advantages:
- explicit typed amount bindings with exact rational arithmetic and an `unresolved` status that withholds instead of guessing;
- an audit-recorded verdict pipeline with cost-sensitive expected-loss semantics, frozen from the approved REM design;
- a measured null result for the learned stage behind a deterministic front, with stage accounting.
