# 01 — Research gap verification

**Status:** `[PROPOSED — SUPERVISOR APPROVAL REQUIRED]`. This verifies a *proposed* gap against the six supplied papers (`02`) and the project's earlier prior-art record. It is not a novelty claim.

**Sources and limits.** Full texts: PROVISO, AgentBoundary, Calibration Is Not Control, CASEL, Task Shield, MELON. Earlier project records: `RESEARCH_GAP_AND_NOVELTY_AUDIT.md`, `STAGE2_5_PRIOR_ART_RECONCILIATION.md`. No systematic search to 11 November 2026 was possible (the session cannot reach arXiv or publisher sites); an abstract-level index search confirmed the primary records and one further relevant preprint (DelegationBench). Newer competing work may exist and is not excluded.

## 1. The proposed gap, clause by clause

| Clause of the proposed statement | Verdict | Evidence |
|---|---|---|
| "recent runtime security frameworks have introduced risk-based, provenance-aware, and intervention-oriented mechanisms" | **Supported** | PROVISO (provenance-typed action selection); CASEL (consequence-aware intervention modes); MELON, Task Shield; earlier record: NEXUS, AgentTrust, ProvenanceGuard. |
| "reliably distinguishing authorized financial operations from attacker-induced actions while preserving benign-task utility remains challenging" | **Supported in general; only indirectly for finance** | AgentBoundary: "high safety frequently coexists with poor authorized-task completion" across 17 configurations (general agent tasks, not banking). MELON: benign utility on AgentDojo falls from 80.41% to 68.04% with GPT-4o. This project: the original REM releases 33 of 178 legitimate state-changing calls (`03`). None of the six papers studies financial authorization as such; PROVISO has one controlled payment task. |
| "recent provenance-informed approaches … reported limitations concerning benchmark-specific training, labeled outcome dependence" | **Supported by the authors' own words** | PROVISO, Limitations: "fitted separately for each benchmark and therefore requires labeled outcomes from the target setting; we do not study transfer of a single trained controller across tasks". |
| "insufficiently examined transfer across tasks" | **Supported, with a correction** | PROVISO does hold out *user tasks* on AgentDojo ("Five folds keep all attack variants of a user task together"). It does not hold out *attack objectives*, and it does not test transfer across benchmarks. The accurate wording is "transfer to unseen attack objectives and across benchmarks is not examined". |
| "whether an improved authorization-aware and provenance-informed decision mechanism can provide stronger generalization … while reducing unnecessary intervention" | **A question, legitimately open; this study's answer for the tested candidate is negative** | See `08`. |

## 2. Overlap that narrows the gap

1. **The decision-theoretic part is not open.** Calibration Is Not Control already formalizes that a risk score is insufficient for intervention decisions and that recalibration cannot repair it. CASEL already states a per-mode cost rule of the same structure as REM's. A thesis cannot claim either idea.
2. **The over-defence observation is not open.** AgentBoundary measures it at scale, with a counterfactual design, and trains a mitigation.
3. **Provenance-typed decisions are not open.** PROVISO does this with a learned controller; ProvenanceGuard (earlier record) does it at the tool boundary.
4. **Task-alignment authorization is not open.** Task Shield defines it formally and enforces it with an LLM.

What is left is narrow and empirical:

> For runtime monitors that decide on tool calls of a banking agent from provenance and behavioural evidence **without a language model in the decision path**, it has not been shown (i) how far learned decision policies transfer to unseen user tasks **and** unseen attack objectives, (ii) whether they outperform parameter-free provenance or authorization rules on the same recorded trajectories, and (iii) which failures remain for argument substitution and unrequested actions.

This is a gap in *evidence*, not in *mechanism*. It can be studied offline on recorded trajectories, so it does not depend on live or production experiments.

## 3. Does the gap depend on live experiments?

No. Generalization across held-out tasks and objectives, false blocks of authorized actions and the security–utility trade-off are all measurable by recorded-trace replay and call-level probes. The limits of that mode are stated wherever results are reported: no adaptive agent, no reviewer, benchmark success checks as outcomes.

## 4. Novelty statements that are and are not defensible

| Statement | Defensible? |
|---|---|
| "A novel authorization-aware decision algorithm" | **No.** The mechanisms tested here are published (intervention value) or declared rules (authorization evidence), and the learned candidate did not work. |
| "REM generalizes better than published defences" | **No.** No published defence could be run under the same conditions. |
| "A double-holdout replay evaluation (unseen user task and unseen attack objective) of learned and rule-based monitors for a banking agent, including negative results" | **Yes**, as an evaluation contribution, among the works examined. |
| "Evidence that outcome-supervised intervention-value policies do not transfer to an unseen attack objective on this benchmark" | **Yes**, as a measured, bounded finding (one benchmark, one objective class). |
| "Evidence that parameter-free provenance rules match the original REM's security with more utility, and how each rule fails" | **Yes**, as a measured finding; it confirms a concern raised in the R4 examination. |

## 5. Recommended wording of the gap (for supervisor decision)

> Published runtime defences for tool-using agents either rely on a language model in the decision path or are fitted per benchmark, and their authors report that transfer of a fitted controller is not studied. For monitors that decide from provenance and behavioural evidence alone, there is no evidence on whether learned decision policies transfer to unseen banking tasks and unseen attack objectives, nor on whether they add value over simple provenance or authorization rules. This thesis provides that evidence on recorded AgentDojo banking trajectories and documents the failure modes that remain.

The earlier, broader wording ("an improved … decision mechanism can provide stronger generalization") should not be used as a claim, because the improved mechanism tested here did not provide it.
