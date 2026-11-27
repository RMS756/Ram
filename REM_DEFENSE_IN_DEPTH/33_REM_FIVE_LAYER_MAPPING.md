# Mapping prior systems to REM's five layers

## Classification

| Code | Meaning |
|---|---|
| **DM** | Direct functional match: performs the same function as the REM layer |
| **PO** | Partial functional overlap: part of the function, or the same function by a different means |
| **CM** | Complementary mechanism: addresses the same threat where REM's layer does not, or in a way REM lacks |
| **NE** | No equivalent mechanism (stated in, or evident from, the source at the level read) |
| **NR** | Not reported at the level read (abstract or repository). This does **not** mean absent |
| **NIE** | Present, but its contribution to security is not independently evaluated in the source |

**Reading rules:**
- No one-to-one correspondence is forced. One mechanism can map to several layers, and one layer can hold several mechanisms.
- Levels are as in file 30. Progent is the only full-text reading.
- The REM layer functions referred to are those of REM v1.0. Proposed REM-DiD items are marked [P].

## Main matrix

| System | L1 Input & Context | L2 Detection | L3 Behavioral Analysis | L4 Decision Engine | L5 Mitigation |
|---|---|---|---|---|---|
| **RTBAS** | **DM**, stronger: IFC labels on tool outputs, against REM's segment labels (A) | **CM**: dependency screeners (LM judge, attention saliency) decide which inputs a call depends on; this is not injection detection (A) | **NR** | **PO**: a deterministic rule over labels (auto-execute or ask); no learned risk and no consequence tiers (A) | **PO**: user confirmation ≈ REM Escalate with a reviewer, which REM does not have (A) |
| **CaMeL** | **DM**, stronger: capabilities on every value, with data *and* control flow from the trusted query by construction; REM labels segments and matches strings (R) | **NE**: no detector by design (R) | **CM**: control flow is fixed by the privileged LLM, so sequence deviation is prevented rather than detected (R) | **PO**: deterministic policy check over capabilities ≈ REM's predicate stage / [P] 4A (R); no learned decision | **PO**: the call is stopped on violation (S); further handling NR |
| **Progent (v3)** | **NE**: no provenance in the policy language (F, Fig. 2b) | **NE** (F) | **NE**: no history term; the LLM may rewrite the policy (F) | **PO**: deterministic per-argument rules ≈ REM's predicates / [P] 4A; LLM-generated policies, SMT-checked updates, approver. No learned risk (F) | **PO**: the call is blocked, with a fallback message so the agent continues; terminate or ask-user fallbacks are available (F). REM withholds the step; REM has no fallback message |
| **AgentCap** | **PO**: provenance of security-sensitive arguments (A); declared intent per request (A). Whether the intent comes from a trusted source: NR | **NR** | **PO**: a per-agent trust score updated by suspicious requests and outcomes (S) ≈ REM's history evidence, as a running score rather than features; **NIE** (no ablation found) | **PO**: deterministic constraints (trust, prerequisites, mutually exclusive authority) plus a trust threshold (A/S) ≈ [P] 4A; no consequence-aware learned decision | **DM**: tokens validated at the tool boundary = [P] parameter-bound permits; revocation or sandbox (A/S) |
| **Fides** | **DM**, stronger: integrity and confidentiality labels with dynamic taint tracking (A) | **NE**: none stated (A) | **NR** | **PO**: deterministic policies (A) | **CM**: hiding primitives act on what the planner sees (A); this is not one of REM's four verdicts |
| **Narisetty et al.** | — | — | — | Evaluates Progent's L4-equivalent under an adaptive attack (A) | — |
| **AgentDojo** (benchmark) | — | **DM** as a baseline: `transformers_pi_detector` classifies tool outputs (L) | — | — | **PO**: `tool_filter` restricts the tool set before the run (L); a pre-run least-privilege baseline, not runtime mediation |
| **ASB** (benchmark) | — | **PO**: its 11 defenses include detection-type defenses (A; details NR) | — | — | — |
| **Greshake et al.** | Threat definition motivating L1 (A) | Threat definition | — | — | — |

## Other relevant systems (all at abstract level)

| System | L1 | L2 | L3 | L4 | L5 |
|---|---|---|---|---|---|
| **AIS** (*Systems*) | **DM** for [P] TAE: a typed financial action intent and mandate lineage | NE (abstract) | NR | **DM** for [P] 4A: deterministic checks on mandate, policy, state, approvals and economic terms | **DM** for [P] permits: single-use, execution-bound authority; EVM enforcement |
| **AGATE** | **DM** for [P] TAE and lineage: operator declarations, host approvals, source registration | NE (no LLM in the decision path) | **PO**: an effect ledger for repeated requests ≈ [P] retry tracking | **PO**: deterministic checks | **DM** for [P] permits: parameter-bound grants that expire and allow limited uses |
| **GuardRail** | PO: trusted registry | **PO**: a semantic risk layer | **PO**: forward taint over plans; detectors for seven multi-step chains | **DM** for the [P] 4A/4B ordering: risk "can never override a deterministic refusal"; **NIE** (no measurement) | **DM** for [P] permits: the Action Passport. Four verdicts including ESCALATE_TO_HUMAN |
| **Agent-Sentry** | PO: argument provenance features | PO: an LLM judge on the residual | **DM**: a structural classifier over action sequences, learned from benign executions | **PO**: three checks combined; a deterministic allow-list on sensitive values | NR |
| **AuthGraph** | **DM**: an authorization graph from a clean context, and execution provenance at parameter-source level | NE | PO: graph alignment over the trajectory | PO: alignment check | NR |
| **ScopeGate** | NE | NE | **PO**: an idempotency check (repeated payments) | **DM** for [P] 4A financial constraints: scope, authorization, money ceiling, default deny | PO: the policy enforcement point |
| **AIRGuard** | PO: source and target trust | NR | PO: cross-step risk audit | PO: step-level authority | PO: enforcement before execution; side-effect simulation |
| **PACT** | **DM**, stronger: role-specific provenance contracts for arguments | NE | PO: cross-step provenance | PO: contract check | NR |

## What the mapping shows

1. **Layer 1 is where prior work is strongest and REM weakest.** CaMeL, Fides, RTBAS, PACT and AuthGraph track provenance at value or argument level, by construction or by labels. REM v1.0 matches strings, and reformatting defeats it (DiD-2, POP-R).
2. **Layer 2 (injection detection) is usually absent by design** in system-level defenses. CaMeL, Progent and Fides do not detect: they confine. REM's detector adds nothing measurable (SIG-1). Detection's role in a layered design is therefore an open empirical question, not an established benefit.
3. **Layer 3 (behavioral analysis) is rare**, and where it exists its contribution is not isolated:
   - AgentCap's trust score: S, no ablation found;
   - Agent-Sentry's classifier: per-layer results not found;
   - AgentTrust's session tracker: a null result at level U.
4. **Layer 4: deterministic authorization dominates.** Learned risk sits behind or beside it only in GuardRail (unmeasured), Agent-Sentry (classifier), NEXUS and the thesis's own extension. **None of the reviewed works measures whether a calibrated, consequence-aware learned decision adds security or utility once deterministic authorization is in place.**
5. **Layer 5:**
   - Parameter-bound execution permits are published: AGATE, AIS, GuardRail, AgentCap.
   - Human confirmation is common.
   - REM's four verdicts collapse to two without a reviewer (TASK 2, file 25).
