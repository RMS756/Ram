# Gap analysis, overlap and novelty, and a revised contribution statement

**Basis:** files 30–34; REM's own measurements (DiD-1, DiD-2, SIG-1: files 05 and 08); thesis Chapter 2 §2.11.

**Limit that applies to every conclusion below:** apart from Progent and six other papers read in full earlier, the prior work is known at abstract, repository or search-excerpt level. A full text could contain a bypass analysis that its abstract does not mention. Every "not found" below means *not found at the level read*. §4 lists the checks that would overturn it.

## 1. What is already established (REM must not claim it)

| Claim | Established by (level) |
|---|---|
| Indirect prompt injection is a practical threat to tool-using agents | Greshake et al. 2023 (A); AgentDojo (A); ASB (A) |
| Defense-in-depth, least privilege and complete mediation should be applied to agents | AgentSandbox position paper (A); classical security principles |
| Runtime mediation of every tool call, before execution | Progent (F); RTBAS, CaMeL, AgentCap, Fides, AIRGuard, GuardRail, AGATE, ScopeGate (A/R) |
| Capability- or token-based runtime authorization | AgentCap (A); AGATE (A); AIS (C/A); CaMeL capabilities (R) |
| Provenance or IFC at value or argument level | CaMeL (R); Fides (A); RTBAS (A); PACT, AuthGraph (A) |
| Deterministic financial constraints (recipient, ceiling, idempotency, exact economic terms, single-use authority) | AIS (C/A, peer reviewed); ScopeGate, AGATE (A); Progent manual banking policy (R) |
| Learned or semantic risk that may tighten but never override a deterministic refusal | GuardRail (A; no measurement) |
| Execution permits bound to exact parameters | AGATE, AIS, GuardRail, AgentCap (A) |
| Layered combinations of complementary checks at the tool boundary | Agent-Sentry (3 checks), AgentTrust, ToolSafe, DRIFT, FinHarness, MCP enforcement point (thesis §2.10), PRISM, Spotlight-Guard (A) |
| Component ablations (remove a component and re-measure) | Progent (F); PACT, AIRGuard, AIS, MCP enforcement point (A); CaMeL and Fides without policies (S) |
| Offline replay of recorded AgentDojo trajectories as an evaluation method | Kekatos et al. 2026 (thesis); ASC replays AgentDojo ground-truth traces (A) |
| Adaptive evaluation of an out-of-band defense | Progent App. E (F); Narisetty et al. (A) |
| Over-defense: safety bought with authorized-task failure | AgentBoundary (F); "Same Operation, Different Permission" (A); AgentPI SoK (A) |
| Comparison of defense configurations, in simulation | Kanaker et al. 2026 (A): nine configurations, six threat scenarios |

## 2. What remains untested, at the level read

| ID | Open question | Why prior work does not settle it | Can REM's existing data address it? |
|---|---|---|---|
| **G1** | **Residual protection when one control, or one evidence family, is evaded at test time while the others stay in place.** This differs from an ablation, which removes the control and refits or reconfigures the rest | The ablations found remove components. No abstract reports evasion of one control with the remaining controls unchanged. Kanaker et al. compare configurations in simulation, not on an executable benchmark | **Yes:** DiD-1 (single-control evasion), DiD-2 (family and pair evasion, plus one real evasion), offline and paired |
| **G2** | **Removal and evasion can give opposite answers about a control's value** | Not discussed in any abstract read | **Yes**, a measured instance. Refitting without the behavioral family (REM v1.1) loses no security (11 vs 11) and completes 35 more benign tasks, so an ablation would call the family redundant. Under action-family evasion, however, v1.1 lets 653 attacks through against 90 for v1.0. The behavioral family is the depth behind the action family |
| **G3** | **Whether signals counted as separate layers are actually independent** (correlation and duplication among detection and behavioral evidence) | Agent-Sentry and others combine signals; correlation audits are not reported at abstract level | **Yes:** SIG-1. The detector is a template fingerprint, duplicated by x~beh1~ (correlation 1.00), and contributes no measurable protection |
| **G4** | **The cost of depth:** whether the redundancy that tolerates evasion comes from low-specificity signals that also over-block | Over-defense is reported for whole defenses, not attributed to the controls that provide depth | **Yes**, partly. REM withholds 1,325 of 1,665 legitimate state-changing steps (P1: 859, P2: 893). Benign tasks: 105 of 334 for REM against 175 undefended |
| **G5** | **Does a calibrated, consequence-aware learned decision add security or utility once deterministic authorization exists?** | AIS, AGATE, ScopeGate and AgentCap have no learned decision. GuardRail's semantic layer is unmeasured. NEXUS's learned scorer reportedly gives no binary-detection gain (thesis §2.11.4, repository level) | **Not yet.** REM v1.0 has no authorization constraints beyond D1. The thesis's extension study measured a related question (largely negative, Ch. 4 §4.6.8). The TASK 2 study F1 (oracle TAE) is required |
| **G6** | **Banking-specific evidence on an open, executable benchmark** | Progent pools suites (F). Banking-only figures for CaMeL, Fides and AgentCap are not determined | **Yes**, banking only, but one suite, one attacker account, 16 user tasks |

**Not open, so not to be claimed:**
- that layering helps in general;
- that runtime authorization works;
- that provenance helps.

## 3. Overlap and novelty

| Element of REM or REM-DiD | Overlap | Novelty status |
|---|---|---|
| Five-layer architecture | Layered designs are common (PRISM, GuardRail, Agent-Sentry, the banking-chatbot DiD framework) | **Not novel.** REM is not "the first multi-layer framework" |
| L1 provenance by segment labels and exact matching | Weaker than CaMeL, Fides, RTBAS and PACT | Not novel; weaker than the state of the art |
| L2 pattern detector | AgentDojo ships a classifier baseline | Not novel; measured as ineffective (SIG-1) |
| L3 behavioral history features | AgentCap trust score (S); Agent-Sentry classifier (A); AgentTrust session tracker | Not novel as a mechanism |
| L4 ridge LR, Platt calibration, tiers, expected loss | NEXUS, CASEL (thesis §2.11.4) | Not novel as a mechanism; the thesis already says so |
| [P] TAE, A1–A9, 4A-before-4B ordering, parameter-bound permits | AIS, AGATE, GuardRail, AgentCap, ScopeGate | **Not novel.** Adopted designs (file 23 §6 updated) |
| **Evaluation of evasion-conditioned residual protection (G1, G2), signal redundancy (G3) and the cost of depth (G4) on a banking benchmark** | Ablation and robustness studies exist; this framing was not found at the level read | **Candidate empirical contribution**, conditional on §4 |

## 4. Checks that could overturn G1–G3 (must be done before the claim is finalized)

1. Read the full texts (a session in the `ram-thesis-research` environment can reach arXiv) of:
   - Agent-Sentry: per-layer evaluation;
   - AgentCap: ablations, and whether the trust score is evaluated;
   - AIS: mechanism ablations;
   - AGATE: bypass analysis;
   - CaMeL v2 and Fides: the no-policy rows;
   - RTBAS: screener ablations;
   - Kanaker et al.: whether configurations are evaluated under the failure of one control;
   - ToolGuardian: rule-removal ablations.
   For each, record whether it evaluates **test-time evasion with the other controls fixed**. If any does, on agents under injection, G1 is not open and the claim narrows to G2–G4 on banking.
2. Search the safety-engineering literature on independent protection layers and correlated failures (layer-of-protection analysis; common-cause failure). Cite it as the conceptual origin of G1 and G3, so the thesis does not present the concept as new.
3. Re-run the duplication search after the full-text reading, with the narrowed wording.

## 5. Assessment of the candidate contribution

> *Candidate:* "An evidence-driven evaluation of complementary runtime security controls for financial AI agents under indirect prompt injection, focusing on their incremental security contribution, resilience to individual-control bypass, and security–utility trade-offs."

| Part | Supported by the literature review? | Supported by REM's experiments? | Verdict |
|---|---|---|---|
| "complementary runtime security controls" | Yes: combinations are common, so the object of study is relevant | REM has five layers. Measured controls: provenance-derived action evidence, pattern detection, behavioral history evidence, predicates, learned decision | Supported, but these are REM's controls, not controls in general |
| "for financial AI agents" | Financial evidence in the literature is thin (file 34) | Simulated banking suite only | **Overstated** → "for a simulated banking agent (AgentDojo banking suite)" |
| "incremental security contribution" | Ablations are common, so this is not a gap by itself | Thesis Ch. 4 §4.5 ablations; DiD-2 refit arms | Supported as evidence; not novel as a question |
| "resilience to individual-control bypass" | Not found at level read (G1) | DiD-1 and DiD-2, offline; evasion mostly modeled; one real evasion | **Supported, with qualifiers** (modeled evasion, NO-ADAPT, development data) |
| "security–utility trade-offs" | Over-defense is well known | Benign tasks, withheld legitimate steps, cost of depth (G4) | Supported; the novel part is attributing over-blocking to the controls that provide depth |
| Interaction with **deterministic financial authorization** (in the task's list) | Authorization is published (AIS and others) | **Not measured:** REM v1.0 has no financial authorization | **Not supported yet.** Requires F1 (oracle-TAE replay) |
| Adaptive attacker | Narisetty et al. show its importance | None | Must be stated as out of scope |

## 6. Revised, evidence-supported contribution statement

Status: **[PD] proposed wording, pending supervisor decision** (CLAUDE.md research-question lock). It replaces nothing in the thesis until approved.

> **Empirical contribution.** An offline, paired evaluation on the AgentDojo banking suite (simulated banking agent, recorded runs, non-adaptive replay) of how the complementary runtime controls of an existing five-layer mediation framework behave under indirect prompt injection. It measures:
> - (i) the incremental contribution of each control and evidence family;
> - (ii) the residual protection when an individual control, or a whole evidence family, is evaded at test time while the other controls remain in place, as distinct from removing it and refitting;
> - (iii) the redundancy and correlation among the signals that supply that depth;
> - (iv) the cost of that depth in withheld legitimate actions.
>
> The evaluation shows that removal-based ablation and evasion-based testing can give opposite assessments of the same control. A defense-in-depth claim therefore needs the second.

**What the statement explicitly does not claim:**
- that REM is the first layered or defense-in-depth framework for agents;
- that runtime mediation, capability authorization, provenance tracking or financial authorization constraints are new;
- that the results hold for adaptive attackers, live agents, other benchmarks, real banking systems or deployed applications;
- that REM's learned decision adds value behind deterministic authorization (not measured; G5).

**Conditions:**
- the checks of §4;
- the experiments in file 36 §2, at least E1–E3, before the statement is used in the thesis abstract or conclusion.
