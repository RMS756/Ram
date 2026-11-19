# 15 Final research contributions (as supported by the evidence, 19 November 2026)

These match thesis R8, Chapter 1 (Section 1.11) and Chapter 5 (Table 5.3). Every item names its evidence kind. None is described as a new algorithm.

## Confirmed contributions

| # | Contribution | Evidence | Kind |
|---|---|---|---|
| C1 | **A specified, implemented and tested runtime framework (REM v1.0).** It has five layers at the tool boundary: provenance-based evidence, ridge logistic estimate with Platt-type recalibration, consequence tiers, predicates, a four-verdict expected-loss decision, deterministic mitigation, and an audit record with audit-only linear SHAP. The software refuses to run with undeclared design values. | `rem/`; 806 passing tests (798 existing + 8 new); exact reproduction of the published counts on 19 Nov | Software + replay |
| C2 | **A controlled evaluation protocol for runtime agent defences on recorded executable episodes.** It uses grouped cross-fitting by attack objective, a double holdout, model-free rule baselines, NO-ADAPT replay with an eligibility check, pre-registered protocols committed with code hashes, and separate reporting of evidence kinds. | Ch. 3, Ch. 4; protocols `02`, `05` | Method |
| C3 | **Measured security and its cost for REM v1.0.** Replay ASR 22.6% → 0.4%; benign completion 52% → 31%; 33 / 178 legitimate state-changing calls and 4 / 89 legitimate payments released. | Pilot R4, reproduced today | Replay, development data |
| C4 | **A pre-registered decomposition of where REM v1.0's protection comes from:** <ul><li>the learned decision prevents 661 of 672 attacks and admits none, at −22.5 benign-utility points;</li><li>the consequence-aware rule prevents 153 attacks that thresholds admit, at −19.5 points;</li><li>calibration, context evidence, predicates and Modify change no attack outcome;</li><li>behavioural evidence lowers task completion with no security effect.</li></ul> | `04`; R8 Section 4.5.5 | Replay, development data, pre-registered |
| C5 | **A call-level reachability analysis.** It shows that the learned decision of REM v1.0 decides 6,626 of 6,684 calls and changes 2,129 releases. This corrects a reading of the later exploratory studies, in which learned components behind a deterministic guard changed nothing. | `04` §2.6 | Replay |
| C6 | **A comparison with the four defences distributed with AgentDojo, kept to two evidence kinds.** On the same task pairs, REM's replayed decisions leave fewer successful attacks than three recorded defences and about as many as the injection classifier, with lower benign completion. Layered on a defence's traces, REM removes almost every remaining success. | `07`; R8 Section 4.4.2 | Recorded closed loop vs replay; **descriptive** |
| C7 | **A confirmed gain within the framework.** Removing behavioural evidence (REM v1.1, proposed) gains +7.48 task-completion points [1.17, 16.02] on 2,113 episodes unread before the run. | R7/R8 Section 4.6.8 | Confirmatory replay |
| C8 | **Documented negative results:** <ul><li>outcome-supervised and authorisation-feature policies fail on a held-out objective;</li><li>trusting user-named documents is unsafe;</li><li>exact-string provenance breaks under reformatting;</li><li>calibration does not improve decisions;</li><li>the four verdicts act as two without a reviewer.</li></ul> | Ch. 4–5 | Replay, probes |
| C9 | **Identification of the limiting factor.** Provenance evidence does not represent what the user authorised. Exploratory deterministic request-derived rules move the frontier on development data, but failed held-out request probes. | Sections 4.4.3, 4.5.3–4.5.6, 4.6.7, 4.6.9 | Exploratory |

## Not claimed

- **Superiority over any published defence.** No closed-loop comparison was run, and MELON was not executed.
- **That the learned, consequence-aware decision gives a better security–utility trade-off than simple rules.** It does not, on the evidence available (Section 4.4.1).
- **Protection of live agents, robustness to adaptive attackers, or production readiness.**
- **That any exploratory redesign (G1–G3, GV, REM-A/B/C, REM-B2/B3) is a validated improvement of REM v1.0.**
- **Novelty of any constituent mechanism.**

## Relation to the approved objectives

| Objective | Status |
|---|---|
| O1 Design | Achieved for banking agents. The task-automation scope is not evaluated. |
| O2 Evaluate against adversarial attacks | Achieved within recorded-trace replay |
| O3 Compare with existing approaches | Achieved for: <ul><li>internal and rule baselines;</li><li>one published policy in replay;</li><li>four distributed defences, descriptively.</li></ul> Not achieved: closed loop and MELON. |

**The objectives were not changed.** Any change would need supervisor approval.
