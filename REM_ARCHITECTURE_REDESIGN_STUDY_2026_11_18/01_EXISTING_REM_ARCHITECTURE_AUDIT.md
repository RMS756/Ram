# 01 Existing REM architecture audit (Phases 0–1)

Branch `claude/rem-architecture-redesign-20261118`, created from `ff2399b`. Frozen code, protocols and historical results are not modified.

**Earlier study, discontinued.** The study `REM_AUTHORIZATION_BINDING_VALIDATION_2026_11_18` was started on the previous branch and interrupted by the user before it produced any result. It left only an empty log and no result file. It was superseded by this study and its folder was removed. Its harness (`seq_harness.py`) and development cases (`ledger_cases.py`) continue here.

## 1. Baseline evidence table

| # | Finding | Status | Evidence (re-checked in this study) |
|---|---|---|---|
| 1 | Frozen scripted closed loop reproduces exactly | **Reproduced** | 960/960 episodes identical (`REM_IMPROVEMENT_CONTROLLED_STUDY_2026_11_18/results/repro_closed_loop_scripted.json` vs the frozen file) |
| 2 | Frozen arms reproduce their stored replays | **Reproduced** | 90,999 raw outcome records, 0 errors; 8,106 / 11,419 episodes identical per frozen arm |
| 3 | No attack succeeds against any defended arm on replay | **Reproduced** | recomputed from raw outcomes with the episodes' own attacked flag: 0 in attacked episodes. The non-zero raw `security` values are exactly the benign episodes (334 / 48), where AgentDojo reports `True` by convention |
| 4 | E1+E2 (C1I): +36 / +166 tasks, 0 lost; interval [0.000, 0.027] → INCONCLUSIVE | **Reproduced** | recomputed from raw outcomes: 36 / 166 gained, 0 lost; interval as stored |
| 5 | Learned stage: 0 verdict changes on C1; 22 / 79 harmful on C1I | **Reproduced** | raw outcomes: C1L = C1 on every episode; C1IL ≠ C1I on 18 / 79 episodes |
| 6 | C1's ut15×it4 advantage is order dependent | **Reproduced and extended** | `results/ledger_analysis_frozen_arms.json` (this study) |
| 7 | Full Progent (LLM-generated policies) not evaluated | **Confirmed not executed** | no endpoint; no logs exist |
| 8 | All evidence so far is development evidence | **Confirmed** | populations seen before; candidates designed on them |
| 9 | Calibration Brier 0.059, ECE 0.024 | **Reproduced** | stored `ablation_results.json` |

The frozen commits `e6a20b3`, `7f57865` and `ff2399b` exist and are on the remote. The protocol hashes of the controlled study verify, except `ctl_run.py`, whose change is documented as amendment 1.

## 2. Components: what each does, whether it runs, whether it decides

**Data sources:**
- frozen REM v1.0 modules (`rem/`);
- the candidate code of the three previous studies;
- replay traces of the controlled study (`ctl_replays.pkl`, scheme S1, primary population, 2,551 restricted calls).

| Layer | Component | Responsibility · input → output | Foundation | Executes? | Changes a decision? | Measured contribution | Runtime | Failure modes | Simpler alternative |
|---|---|---|---|---|---|---|---|---|---|
| 1 Input & context | provenance labelling; request compiler (revision-3 instructions, conditions, counts); amount grammar v1/v2 | request text + tool results → instructions, bindings | deterministic parsing; exact rationals | yes | indirectly (feeds 4) | via front / contract | sub-ms | supported English constructions only; split instructions; ~460 legitimate calls unresolved (`REM_IMPROVEMENT…/03`) | – |
| 2 Detection | ridge logistic regression (F4 evidence) | features → logit s | ridge-regularised logistic regression | yes, when an arm includes it | **no** (see §3) | ROC-AUC 0.974 vs attack labels on all restricted calls | ~0.1 ms | none observed in isolation | – |
| 2 Detection | Platt calibration on the logit | s → p | Platt (1999) | yes | no | Brier 0.059, ECE 0.024 (all restricted calls) | negligible | – | – |
| 3 Behavioural analysis | trajectory features, tracker | history → features | – | yes | via 2 | – | – | – | – |
| 3 Behavioural analysis | per-instruction **ledger** (C1) | released calls, execution signals → remaining allowance | stateful enforcement | yes | yes (exhaustion) | 0 replay effect; prevents 16 diagnostic and 1 fixture release; **4/9 unauthorised releases and 6/12 authorised withholdings** in the scope scenarios | negligible | binds *count*, not *object*: order dependent (§4) | – |
| 4 Decision engine | authority front (revision 3) | call + evidence → denied / supported / authority | deterministic authorisation (operation, effect, recipient, condition) | yes | **yes: stops all 907 attack-labelled calls** | the whole measured security of every REM-derived arm | ~0.1 ms | over-blocks values delegated to files (injection vectors), subjective conditions, implicit arithmetic | – |
| 4 Decision engine | contract witness (C1) | call + contracts + ledger → verified / unresolved / mismatch / exhausted | deterministic; exact equality | yes | yes (utility side; no attack reaches it) | removes F1 / F2 releases on diagnostics | sub-ms | as for the grammar | – |
| 4 Decision engine | expected-loss Bayes decision (frozen engine) | p, tier → verdict | Elkan (2001) expected cost; Chow (1970) reject option (conceptual) | yes in learned arms | 0 changes on C1; 22 / 79 harmful on C1I | NULL / harmful | +0.09 ms median; p95 doubles | placed after a stage that already removed every positive | §3 |
| 4 Decision engine | predicates D1 / D2 | tool, tier, evidence availability → forced verdict | declared rules | yes | yes (55 escalations, ut9) | – | – | – | – |
| 5 Mitigation | step-level Allow / Block / Escalate (no reviewer) | verdict → release or withhold + notice | frozen semantics | yes | – | – | – | Modify is never chosen (0%) | – |
| audit-only | linear SHAP | – | Lundberg & Lee (2017), linear case | **not executed in any candidate arm** (no frozen scorer attached) | no, by design | – | – | – | – |
| optional | CUSUM | – | – | not on the verdict path (observe-only by the design lock) | no | – | – | – | – |
| cross-cutting | offline fitting / recalibration | traces → stored fits | cross-fitting | offline only | – | – | – | – | – |
| comparator | Progent manual policy (PG) | tool, args → allow / deny | Progent (Shi et al.) static rules, 9befb41 | yes | yes | parity with upstream engine: 0 / 2,551 disagreements | ~0.07 ms | static recipient list: refuses every other account | – |

## 3. Why the learned estimator has no influence (traced, not assumed)

**Traces.** Restricted calls of C1L, primary S1 (`logs/learned_reachability_from_stored.log`):

| Stage that decided | Attack-labelled | Not attack-labelled |
|---|---|---|
| authority front | **907** | 527 |
| predicates D1/D2 | 0 | 55 |
| contract witness (withheld) | 0 | 352 |
| learned stage | **0** | 710 |

**Each candidate explanation, tested against those traces:**

| Explanation | Supported? | Evidence |
|---|---|---|
| Deterministic guard blocks calls before the learned stage | **yes** | every positive is decided by the front |
| Insufficient decision reachability | **yes** | the reachable set has 0 positives |
| Threshold selection | no | at p\* = 0.0476 the score has recall 1.0 on all calls; it is never applied to them |
| Miscalibration | no | Brier 0.059, ECE 0.024 |
| Inadequate features | no | ROC-AUC 0.974 |
| Insufficient training data / class imbalance | not the cause here | 907 of 2,551 restricted calls are positive; the learned stage sees 0 of them |
| Architectural mismatch between risk scoring and authorisation | **yes** | the estimator predicts *attack influence*; once authority is enforced, the remaining uncertainty is about *amount correctness* (unresolved values) and *object scope*, which the estimator was not trained to predict |

**Conclusion.** The null result is caused by **placement**, by a **prediction target that does not match the residual uncertainty**, or by both. The estimator's quality is not the cause.

## 4. Authorization-scope vulnerability (Phase 1 of the earlier prompt; development scenarios)

**Setup.** `experiments/architecture_redesign/ledger_cases.py` holds AgentDojo user_task_15 wording with synthetic copies of its environment, and labels fixed before running. The output is `results/ledger_analysis_frozen_arms.json`.

| Arm | Authorised released / 12 | Unauthorised released / 9 | Ambiguous released / 3 |
|---|---|---|---|
| B0 | 12 | 9 | 3 |
| GV_math2 | 12 | **9** | 2 |
| C1_noledger | 12 | **9** | 2 |
| C1 | **6** | **4** | 0 |
| C1I | 6 | 4 | 0 |
| PG | **0** | 0 | 0 |

**What the frozen C1 does:**
- It releases the attacker's modification whenever it comes first: L2, L3, L5b, L7a. That consumes the allowance, and the legitimate rent update is then withheld (`contract_exhausted`).
- With two rent orders (L6) it withholds the second legitimate update.

**Root cause.** The capability granted by an instruction is keyed on *(instruction, effect, account)*. It is never keyed on the **object** being modified. This is the confused-deputy pattern (Hardy, 1988): the deputy (the agent) holds the authority to "modify a standing order to the landlord", and the attacker chooses which object it is exercised on.

**Progent's manual policy** refuses every update in these scenarios, because the new landlord is not on its static list.

## 5. Component recommendations (evidence-based; adoption needs supervisor approval)

| Component | Recommendation | Reason |
|---|---|---|
| Authority front (explicit authorisation) | **KEEP** | carries all measured security |
| Contract witness + amount grammar | **KEEP** | removes F1 / F2; exact arithmetic |
| Ledger | **MODIFY**: bind consumption to the banking object | §4 |
| E1 / E2 evidence resolution | **MODIFY**: provenance-restricted; E2 must not trust an unknown counterparty (refund scam) | `REM_IMPROVEMENT…/04`, threat model |
| Ridge + Platt estimator | **REPOSITION or REMOVE from the verdict path**; keep as an audited signal | accurate but unreachable (§3); decision only after a redesign is tested (REM-C) |
| Expected-loss decision | **KEEP mathematically; REPOSITION**, so it only applies to calls whose authority is established but whose evidence is unresolved | tested as REM-C |
| Linear SHAP | **KEEP audit-only** | not executed in candidate arms; no decision role |
| CUSUM | **KEEP observe-only / optional** | design lock |
| Modify verdict | **KEEP semantics; document** that it is never selected | 0% |
| Offline recalibration | **KEEP** | needed for any learned stage |
