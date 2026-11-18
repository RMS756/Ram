# 02 Related work and novelty audit (Phase 2)

## Verification

Every entry below was checked in this session against Crossref (by DOI) or OpenAlex (by record id). The log is in `results/literature_verification.json`.

- Mechanism summaries rest on the full texts read in the earlier studies of this repository. Where a paper was only re-checked bibliographically now, that is stated.
- **CaMeL** did not appear in OpenAlex in this session. It is recorded as verified earlier from arXiv:2503.18813v2 and the official repository README, and **not re-confirmed now**.
- **Access limitation:** arxiv.org and the publishers' sites were not reachable from this session. No full text was re-read here.

## Directly relevant work

| Paper | Venue / status | Problem | Mechanism | Formal method / algorithm | Threat model | Evaluation | Relationship to REM | What REM can build on | What it does not support |
|---|---|---|---|---|---|---|---|---|---|
| **Progent** (Shi, He, Wang, Li, Wu, Guo, Song) | arXiv:2504.11703, **preprint** (v3 2026) | unauthorised tool calls from indirect injection | privilege control: symbolic per-tool argument policies; LLM-generated initial policy; LLM-proposed updates; an SMT check accepts narrowing updates automatically and needs approval for expansions | JSON-schema / regex argument rules; z3 subset check | attacker controls tool outputs; user and agent code trusted | AgentDojo, ASB; LangChain and OpenAI Agents SDK demos | closest prior art for tool-boundary authorisation | deterministic per-call checking; least privilege; monotonic confinement | stateful counts, object binding, amount derivation, conditions; no financial consequence model |
| **CaMeL** (Debenedetti et al.) | arXiv:2503.18813, **preprint** | prompt injection by design | privileged / quarantined LLM split; data flow with capabilities; policies on values with provenance | capability tags; interpreter-enforced policies | untrusted data never steers control flow | AgentDojo | provenance-tracked values are the principled version of REM's "trusted evidence" | value provenance; capability checks | REM does not rewrite the agent (CaMeL changes the agent's architecture; REM is non-invasive) |
| **AgentDojo** (Debenedetti et al.) | NeurIPS 2024 D&B, **peer-reviewed** | evaluating injection attacks and defences | executable suites, utility / security evaluators | – | injections in tool outputs | 97 tasks, 629 security cases | REM's evaluation environment | – | no notion of authorisation scope beyond the injection-task evaluator |
| **MELON** (Zhu, Yang, Wang, Guo, Wang) | ICML 2025, PMLR 267, **peer-reviewed** | detect hijacked tool calls | masked re-execution; compare tool calls of original and masked runs | similarity of tool-call sets | indirect injection | AgentDojo | a detector at the tool boundary (needs extra LLM calls) | non-invasive interception | authorisation semantics; no state |
| **Task Shield** (Jia, Wu, Qin, Squicciarini) | ACL 2025 Long, **peer-reviewed** | task alignment of actions | LLM checks whether each action serves user objectives | LLM judgement | indirect injection | AgentDojo | alignment check vs REM's explicit authorisation | – | deterministic guarantees |
| **AgentSpec** (Wang, Poskitt, Sun) | ICSE 2026, **peer-reviewed** | customisable runtime enforcement | DSL rules (trigger, predicate, enforcement) | rule DSL | unsafe agent actions | several domains | a rule-based enforcement layer like REM-B | rule triggers on tool calls | learned risk; banking authorisation |
| **ShieldAgent** (Chen, Kang, Li) | ICML 2025, PMLR 267, **peer-reviewed** | policy compliance of agent trajectories | rule circuits extracted from policy documents; probabilistic verification | probabilistic rule circuits | safety policy violations | ShieldAgent-Bench and others | combines rules and probabilities (cf. REM-C) | – | per-call authorisation from the user request |
| **ProvenanceGuard** (She, Liang, Kang) | ASE 2026, **peer-reviewed** | misaligned tool calls | provenance analysis: is a call supported by traceable evidence? | LLM-assisted provenance | indirect injection, misalignment | Agent-SafetyBench, others | provenance as a decision basis (cf. E1/E2) | evidence traceability | deterministic financial checks |
| **LlamaFirewall** (Chennabasappa et al.) | arXiv:2505.03574, **preprint** | guardrail system | PromptGuard 2 classifier, alignment checks, CodeShield | classifier + LLM auditor | injection, misalignment | various | a learned detector; complementary | – | authorisation |
| **Adaptive attacks** (Zhan, Fang, Panchal, Kang) | Findings NAACL 2025, **peer-reviewed** | robustness of defences | adaptive attacks bypass 8 defences | – | adaptive attacker | InjecAgent | REM's threat model must not rely on attack-template recognition | – | – |

**Authorisation foundations** (all peer-reviewed; verified by DOI):
- **Saltzer & Schroeder (1975):** least privilege, complete mediation, fail-safe defaults.
- **Dennis & Van Horn (1966):** capabilities designate objects and permitted operations.
- **Hardy (1988):** the confused deputy, where authority exercised on an object chosen by another party.

## Novelty audit

| Dimension | Progent | CaMeL | Task Shield / MELON / ProvenanceGuard | REM-B / REM-C (proposed) |
|---|---|---|---|---|
| Authorisation granularity | per tool and argument | per value (capabilities) | per action (judgement) | per user instruction × operation × object × beneficiary × amount |
| Tool-call enforcement | yes | yes (interpreter) | yes | yes (non-invasive interception) |
| Provenance | none for argument values | full data-flow provenance | evidence traceability (LLM) | restricted: structured bank fields of executed reads only |
| Policy generation | LLM (generated / updated) or manual | code by the planner LLM | none | compiled deterministically from the request (supported constructions) |
| Stateful permission tracking | no (stateless) | no counting | no | per-instruction, per-object ledger |
| Financial consequence sensitivity | no | no | no | consequence tiers in the frozen expected-loss engine (REM-A / REM-C) |
| Learned decision | no | no | LLM judgement | ridge + Platt + expected loss (REM-A / C) |
| Legitimate-task preservation | via the LLM policy | via planner capability | judgement | trusted-evidence resolution (E1 / E2h) |
| Runtime cost | policy LLM calls | two LLMs | extra LLM calls | sub-millisecond, no model call |

**Assessment.**
- **Not a REM contribution:** combining an authorisation check with a classifier. ShieldAgent and LlamaFirewall combine rules and models.
- **Already covered by prior work:** per-call deterministic authorisation (Progent) and provenance (CaMeL).
- **Candidate distinctions that can be tested here:**
  1. stateful authorisation bound to the banking object and to the user instruction, which fixes a confused-deputy pattern that count-only and static allow-list policies exhibit (§4 of `01`);
  2. deterministic financial evidence resolution (amount derivation and refund recipient) restricted to trusted structured records;
  3. a controlled measurement of whether a calibrated, consequence-aware learned stage adds decision value once (1)–(2) are enforced. This is the original research gap.

**What can be claimed.** These are claimable only as far as the experiments in this study support them: on AgentDojo banking and author-written probes, with no live LLM and no full-Progent comparison.
