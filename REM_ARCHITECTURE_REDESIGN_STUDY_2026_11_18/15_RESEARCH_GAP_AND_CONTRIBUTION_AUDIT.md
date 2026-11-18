# 15 Research gap and contribution audit (Phase 12)

The approved thesis objectives are **not** modified by this document. Every proposed change below is marked `[SUPERVISOR DECISION REQUIRED]`.

## 1. The research gap, re-examined

**Gap as it was stated.** Runtime evaluation and mitigation for financial AI agents that use a calibrated, consequence-aware learned risk estimate to choose among Allow, Modify, Escalate and Block.

| Part of the gap | Status after this study | Evidence |
|---|---|---|
| Runtime mediation of state-changing financial tool calls is needed | **still valid** | B0 (no guard): 672 / 2,979 attack objectives in primary, 436 / 2,065 in dev2, 145 / 469 in H |
| Existing tool-level defences do not express financial *values* (amount, object, repetition) | **supported, for the configuration tested** | Progent's manual policy (PG) releases 161 / 36 audited value/object violations (primary / dev2), against REM-B's 11 / 0 |
| A calibrated learned risk stage adds decision value at runtime | **not supported in this setting**: NULL reach under authorisation-first ordering; harmful when moved to unresolved calls | see §2 |
| Consequence-aware decisions (expected loss) beat a consequence-independent threshold | **not distinguishable**: identical verdicts on every replay population | REM-C vs REM-C-T |
| Calibration matters for the decision | **not shown**: Platt vs raw gives identical verdicts | REM-C vs REM-C-raw |

## 2. Negative and null findings (reported as findings, not hidden)

1. **Reachability.**
   - The stored estimator ranks attacks well: ROC-AUC 0.974; Brier 0.059 and ECE 0.024 on all restricted calls in primary.
   - Yet every attack-labelled restricted call (907 / 559 / 162 in primary / dev2 / H) is stopped by the deterministic authority front before any learned stage.
   - A good model placed after a complete deterministic gate has nothing left to decide on the attack side.
2. **Target mismatch.**
   - The calls left unresolved by the deterministic stages are unresolved because their **value** is not determined by trusted evidence, not because they look malicious.
   - A malicious-influence estimator gives them low risk, and the expected-loss rule releases them.
   - REM-C released 110 (primary) and 24 (dev2) audited value/object violations, and 16 unauthorised diagnostic proposals.
3. **Calibration does not transfer across agent pipelines.**
   - On H, the learned-stage calls of REM-C have Brier 0.598 and ECE 0.609 (n = 105, none attack-labelled).
   - On all restricted calls: dev2 0.222 / 0.213; H 0.174 / 0.148.
4. **An attack-label reviewer is not an authorisation upper bound.** REM-B-R releases the same violations as REM-C.
5. **REM-A's learned stage only removes correct releases:** 3 / 49 / 1 audited-correct calls withheld.

**Conclusion of this section.** In this setting, machine learning does not make a positive contribution to the verdict. This study does **not** force one. The result is specific to:
- this estimator and its target (attack label);
- AgentDojo banking;
- replay (no adaptation).

It is not a general statement about learned components.

## 3. What remains as a defensible contribution (candidate, needs supervisor approval)

| Candidate contribution | Compared with | Evidence | Strength |
|---|---|---|---|
| **C-a. Instruction- and object-bound stateful authorisation** for financial tool calls: a per-(instruction, object) ledger with object binding from trusted fields | Progent (stateless per-tool argument rules); CaMeL (capabilities on values; needs a planner/interpreter redesign); C1 (count-only ledger) | Removes the order dependence of C1: development 12/0/0 vs 6/4/0; held-out probes 0 unauthorised and 0 ambiguous vs C1's 4 + 2; scripted ut15×it4 in 0 of 4 orders vs 2 of 4. No effect on recorded replay populations. | **moderate, diagnostic.** The object-binding question is **INCONCLUSIVE** (HO4 defect). Shown on author-written cases, not on independent data. Related ideas exist (capabilities, Dennis & Van Horn 1966; confused deputy, Hardy 1988). The novelty is the application to financial agent tool calls, not the principle. |
| **C-b. Deterministic evidence resolution from trusted structured records** (E1 explicit arithmetic; E2h refund licence with a known-counterparty requirement) | CaMeL (data provenance), Progent (no value derivation) | E1 is the largest utility contributor (18 / 87 / 3 tasks). E2h blocks the refund scam that plain E2 releases, at a cost of 16 / 30 / 17 tasks. | **moderate, task-specific.** Gains occur only in the tasks the rules were designed from (§2 of `11`). |
| **C-c. A controlled negative result on learned risk stages behind authorisation** | ShieldAgent, LlamaFirewall (rule + model combinations, evaluated differently) | §2 above; frozen protocol; ablations REM-C / REM-C-T / REM-C-raw | **strong within the setting** (pre-registered criteria, three populations, suites). Limited by replay and a single estimator target. |
| **C-d. Audited value/object violation metric** next to attack success | standard AgentDojo security (attack goal only) | It reveals 161 PG and 121 REM-C releases that attack-success metrics report as 0 | **useful methodological point.** It is auditable only for 8 user tasks: `send_money` values for ut3/4/5/11/15, and the standing-order object (id 7) for the rent tasks ut2/9/12/15. Calls of other tasks are not audited. |

**Not claimable:**
- superiority over Progent (full Progent not executed; manual policy not dominated);
- live-agent security;
- generalisation to unseen tasks or other domains;
- a novel algorithm: no new equation is introduced, and the mechanisms are deterministic rules built on established principles;
- statistical utility improvement of REM-B over C1 (INCONCLUSIVE).

## 4. Conflicts with the current frozen specification (CLAUDE.md)

| Specification item (quoted) | Conflict | Consequence |
|---|---|---|
| "provenance labeling → context / behavioral / action evidence → ridge logistic regression → Platt calibration on the logit → consequence tier → policy predicates → expected-loss Bayes verdict → deterministic mitigation → audit record" | REM-B has **no** learned stage on the verdict path. The verdict is decided by authorisation, object binding, contracts and evidence rules. | Adopting REM-B as the primary architecture changes the primary methodology. |
| "Ridge logistic regression is the estimator." / "v*_t = argmin_v R_t(v)" | In REM-B the estimator is not used for the verdict. | It could remain as an audit-only score (like SHAP), which the specification currently does not provide for. |
| "Modify: apply ONE declared modification mechanism" | No candidate uses Modify (0%). The Modify mechanism is still unresolved in the specification. | No change proposed. |
| "Exactly five layers" | REM-B keeps the five layers (`05`). | No conflict. |

## 5. Supervisor change proposal `[SUPERVISOR DECISION REQUIRED]`

| Option | Description | Thesis objectives | Risk |
|---|---|---|---|
| **P1 (no change)** | Keep REM v1.0 as the approved primary design. Report REM-B and the negative learned-stage result as an exploratory extension in Chapter 4, with `[PROPOSED - EXPLORATORY]` labels. | unchanged | Low. The primary design's learned stage stays, with a documented reachability limitation. |
| **P2 (authorisation-first primary)** | Adopt REM-B as the primary verdict path. The ridge + Platt estimator becomes audit-only / monitoring; the expected-loss engine is kept as the baseline and as the documented negative result. | wording of the objectives unchanged; the methodology chapter changes | **Medium.** It changes the frozen pipeline and needs an explicit supervisor decision and a revised specification. |
| **P3 (re-target the learner)** | Keep a learned stage, but re-target it to authorisation uncertainty (target T2: is this value the authorised one). | unchanged | **High.** It needs labelled data that does not leak evaluation tasks, and a new frozen protocol. Not done here. |
| **Before any option** | Fix the designator defect (`08a`); obtain independently written probes; run a live-agent study with an approved budget. | – | – |

**Recommendation of this audit.**
- **P1 now**, with the negative result reported in full.
- **P2 considered** only after the supervisors approve the change and an independent validation exists.
- This is a recommendation; the decision belongs to the supervisors.
