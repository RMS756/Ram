# 05: Research contribution and novelty

**Novelty scale.**

| Label | Meaning |
|---|---|
| Strongly supported | Evidence and literature both support the claim as a contribution |
| Potentially novel but needs qualification | Supported by evidence; distinctness from prior work holds only with stated qualifications |
| Already established in prior work | The mechanism or finding exists in the literature |
| Not supported by current evidence | REM's own evidence does not show it |

**Defensibility** is judged for a master's thesis examination. It depends on:
- the evidence in 02;
- the literature in 03;
- the scope limits that cannot be removed: NO-ADAPT replay, one benchmark, recorded traces, no adaptive attacker, no live agent.

## 1. Level A: architectural contribution

| Proposed contribution | Prior work | REM evidence | Novelty strength | Defensibility |
|---|---|---|---|---|
| A1. A five-layer runtime framework (Input & Context → Detection → Behavioural Analysis → Decision Engine → Mitigation) for financial agents | NEXUS (rules + argument inspection + calibrated LR + four interventions; peer reviewed); Agent-Sentry (3 layers incl. behaviour and provenance); Spotlight-Guard (layered, peer reviewed); AGATE; AgentSandbox (DiD as principle) | Implemented and reproduced. But the ablation shows **all outcome effects come from one component** (the learned decision acting through enforcement); four of five layers change no attack outcome (`REM_ABLATION_STUDY/03` §1) | **Already established** | Defensible only as *the artifact studied*. **Not defensible as an architectural novelty** |
| A2. Expected-loss verdict selection with tier-indexed declared costs over Allow / Modify / Escalate / Block | Elkan (2001) cost-sensitive decisions; Chow (1970) reject option; NEXUS formal intervention policy; CASEL cost-weighted modes | Implemented as frozen. Replay: **Modify, Escalate and Block coincide** (thesis Ch. 4, verdict replacement changes 0 of 3,313 episodes). Expected loss vs consequence-independent threshold: 153 fewer attacks and 19.5 fewer benign points (`REM_FINAL_THESIS_COMPLETION_2026_11_19/README.md`); P3: 3 vs 67 attacks, 18 vs 36 benign (`REM_FINAL_SUBMISSION/results/confirmatory_results.json`) | **Already established** (principle). The banking instantiation is application work | Defensible as an *adaptation*, as the design lock already words it (CLAUDE.md "MATHEMATICAL LOCK") |
| A3. A financial consequence-tier model for banking tools | Consequence-aware control is published (thesis Ch. 2 Table 2.2) | Declared values are exploratory, not approved (`configs/exploratory/`; result files are labelled "EXPLORATORY — NOT THESIS RESULTS — SUPERVISOR DECISION REQUIRED") | Potentially novel but needs qualification: a domain instantiation, not a method | Weak. The values are not validated, and tiers have no measurable effect separate from the cost ratio |
| A4. Fail-closed implementation (an undeclared design value stops the software) | Engineering practice | Implemented and tested | Not a research contribution | Report as engineering quality only |

## 2. Level B: runtime security contribution

| Proposed contribution | Prior work | REM evidence | Novelty strength | Defensibility |
|---|---|---|---|---|
| B1. Intervention **before** execution of a harmful financial tool call | Every boundary defense (Progent, ROPE, CaMeL, AgentCap, ClawGuard, MELON) | Verified in code (`rem/integration/agentdojo_replay.py:236-259`) and in replay | **Already established** | Defensible as a property of REM, not as a contribution |
| B2. **Combining context evidence with behavioural evidence** improves decisions | Agent-Sentry, NEXUS, SIEVE | **Not supported:** context evidence changes no outcome; behavioural evidence lowers benign completion (−10.5 points on P1 replay [1.2, 22.6]; confirmatory +7.5 points when removed) | — | **Not supported by current evidence. Must not be claimed** |
| B3. Examining **action sequences** rather than isolated prompts | Agent-Sentry, AGATE, DRIFT | Behavioural features are sequence-based; no security benefit measured. REM-DiD retry and switch rules are inert in replay | — | **Not supported** |
| B4. A learned, calibrated, consequence-aware decision that prevents injected financial actions | NEXUS, PROVISO, CASEL | **Supported in replay with qualification:** removes 661 of 672 replay attack outcomes on P1, and 433 of 436 on P3. It does so by withholding nearly all state-changing calls: withhold precision 0.40; 81.5% of legitimate restricted calls withheld in benign P1 episodes; benign completion **identical, episode for episode, to withholding every state-changing call** (02 §1.3) | Already established (mechanism); the measured behaviour is REM-specific | Defensible **only** with that qualification. Otherwise it would mislead |

## 3. Level C: empirical contribution

| Proposed contribution | Prior work | REM evidence | Novelty strength | Defensibility |
|---|---|---|---|---|
| **C1. In a nominally five-layer runtime defense, protection is not layered: one component carries all of it, and the others are redundant or harmful.** Pre-registered ablation on three populations | Layer ablations exist (Spotlight-Guard, Progent, AIS) but report *contributions*, not an absence of depth | `REM_ABLATION_STUDY` (frozen `93e6630`): learned decision = all effect; D1/D2, context, calibration and Modify have no outcome effect; behaviour harms utility; context/provenance (AIC) contributes on P3 only. Recomputed in 02 §1 | **Potentially novel but needs qualification** (one system, one benchmark, replay) | **Strong.** Pre-registered, paired, three populations, raw data stored. **Directly on the thesis topic (defense in depth)** |
| **C2. A learned, consequence-aware decision adds no measurable security behind deterministic authorization, and simple rules match it** | NEXUS reports a gain of the risk score over rule-only on its own benchmarks; C. Zhang et al. (2026) report calibrated risk alone is insufficient | Rule baselines on the confirmatory population: P2 rule 4 attacks, A2 rule 4 attacks vs REM 3 (`confirmatory_results.json`). Behind request-derived guards no learned stage changed an outcome (competitive, controlled and redesign studies). Behind oracle authorization: 0 vs 0 attacks, −68 benign tasks (Holm p = 0.12; DiD-3) | **Potentially novel but needs qualification** (the evidence is replay; "behind authorization" is development data or oracle) | **Strong as a negative result**, provided the scope is stated |
| **C3. Methodological findings about NO-ADAPT replay evaluation of action-boundary defenses** | AutoDojo and Bhagwatkar et al. criticise static benchmarks generally | 02 §1.3: (i) the replay benign floor; (ii) the four verdicts collapse to two without a reviewer; (iii) all residual attacks are one benchmark collision (`user_task_15`); (iv) a published manual policy is an oracle allow-list of benchmark IBANs (`REM_COMPARATIVE_EVALUATION_PHASE/02` §2) | **Potentially novel but needs qualification** | **Good**: each finding is checkable from stored data |
| C4. Removal-based and evasion-based ablation can give opposite conclusions about a defense layer | Adaptive-attack literature (Zhan et al. 2025; "The Attacker Moves Second") | DiD-2: refit without behaviour 11 vs 11 attacks; with action-family evasion 653 vs 90 (`REM_DEFENSE_IN_DEPTH/05` §2). **Modelled evasion, post-hoc arm (DiD-2a)** | **Potentially novel but needs qualification** (exploratory; the evasion is simulated) | **Moderate.** Report as exploratory evidence, not a confirmed result |
| C5. Request-derived authorization of financial calls is limited by natural-language intent compilation | CapLite, ClawGuard, ROPE, Progent: request-derived or LLM-generated policies | REM-B hardening: each of three held-out probe rounds found a new compiler error leading to an unauthorized release (`REM_B_HARDENING_VALIDATION_2026_11_19/README.md`) | **Already established in direction**; REM adds concrete failure cases | **Moderate**: development evidence with author-written probes |
| C6. Removing behavioural evidence raises task completion (confirmatory) | — | +7.5 points [1.2, 16.0] on 2,113 unread episodes; 1 vs 3 successful attacks; pre-declared GO (`confirmatory_results.json` primary contrast; verdict). Pre-registration commit not in this repository's history | A within-system result | **Good for utility.** But the security effect is unresolved, and the evasion analysis (C4) shows a loss of depth. **Not a reason to adopt v1.1 without qualification** |

## 4. What REM genuinely contributes

1. **Algorithmic novelty: none.** The thesis already says so (Ch. 1 §1.11, "does not claim a new algorithm").
2. **Architectural novelty: none demonstrable.** The five-layer combination is established in prior work, and NEXUS is a close analogue of the decision engine.
3. **The defensible master's-level contribution is empirical and methodological.** It is a controlled, pre-registered evaluation showing that a calibrated, consequence-aware runtime decision layer for a banking agent:
   - provides replay security only by withholding almost every financial action;
   - is the sole effective layer of a nominally five-layer design;
   - adds nothing that simple deterministic rules do not already provide.

   It is supported by documented measurement pitfalls of replay-based evaluation (C1–C3, with C4–C6 as qualified secondary findings).

**This is a negative result. It is directly relevant to the topic "defense in depth":** it shows that nominal layering is not depth.
