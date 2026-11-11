# 09 — Supervisor decision memo

**To:** Prof. Omar Ahmad Alzubi (Supervisor), Dr. Husam Fakhouri (Co-Supervisor)
**From:** Rawan Al-Lahham
**Date:** 11 November 2026
**Subject:** Test of an authorization-aware improvement to REM: result and decisions needed

**Draft for the candidate's review, prepared with AI assistance (Claude Code); to be checked and edited before it is sent.**

**Status of everything below:** exploratory, isolated from the approved design, offline recorded-trace replay only. Nothing in the approved REM, its results or the thesis has been changed.

## 1. Bottom line

**The proposed improvement does not work, and I recommend not adopting it.** On the same recorded trajectories it lets 132 attacks succeed where the original REM lets 11, and its gain in completed benign tasks disappears when both the user task and the attack objective are unseen (105 → 110 of 334).

The study did produce three findings that matter for the thesis:

1. **The original REM over-defends.** It releases 33 of 178 legitimate state-changing calls and completes 105 of 334 benign tasks (no defence: 175).
2. **A one-line provenance rule matches REM's security with more utility, but is fragile.** "Withhold a state-changing call whose argument was copied from untrusted text" gives 12 attacks and 134 benign successes. When the attacker's account number is merely written with spaces, its attacks rise from 12 to 191.
3. **The best configuration found inside the approved algorithm is REM *without* the behavioural features.** This is the original study's own ablation: 11 attacks and 140 benign successes on the primary folds, 14 and 140 when the user task and attack objective are both unseen, and unaffected by the spacing test. I examined it after seeing the results, so it is a hypothesis for your decision, not a validated improvement.

## 2. What the new research gap is

Proposed (narrowed) wording:

> Published runtime defences for tool-using agents either rely on a language model in the decision path or are fitted per benchmark, and their authors report that transfer of a fitted controller is not studied. For monitors that decide from provenance and behavioural evidence alone, there is no evidence on whether learned decision policies transfer to unseen banking tasks and unseen attack objectives, nor on whether they add value over simple provenance or authorization rules.

The broader wording I first proposed ("an improved authorization-aware mechanism can provide stronger generalization") cannot be kept as a claim: the mechanism I tested did not provide it. The gap does not depend on live experiments.

## 3. Which papers support it

| Support | Paper | Where |
|---|---|---|
| Per-benchmark fitting, labelled outcomes required, transfer not studied | PROVISO (Yan et al., 2026) | Limitations: "fitted separately for each benchmark and therefore requires labeled outcomes from the target setting; we do not study transfer of a single trained controller across tasks" |
| Over-defence of authorized actions is widespread | AgentBoundary (Yang et al., 2026) | Abstract and Table 2: "high safety frequently coexists with poor authorized-task completion" |
| A calibrated risk score is not sufficient for intervention decisions | Calibration Is Not Control (Zhang et al., 2026) | Eq. (1), Proposition 1, Remark 1 |
| Intervention effectiveness is usually assumed, not measured | CASEL (Zhang et al., 2026) | Abstract: "Intervention effectiveness is assumed, not measured" |

All four were read in full from the PDFs I supplied. One correction to my earlier wording: PROVISO does hold out user tasks on AgentDojo; what it does not examine is unseen attack objectives or transfer across benchmarks.

## 4. What was changed in the tested algorithm

Kept: the five layers; ridge logistic regression; logit calibration; the declared costs; the predicates; step-level mitigation.

Changed (in an isolated module only):
1. **Training target.** In place of "is this call an attack attempt?", the models were trained on measured outcomes: does withholding this call prevent the attack's success, and does it break the user's task? These were obtained by replaying each recorded episode with one call withheld.
2. **Decision rule.** Withhold a call when the expected security gain, weighted by C_miss, is at least the expected utility loss, weighted by C_FA.
3. **Two deterministic authorization features.** Whether the call's recipient (or credential) appears in the user's own words; whether it comes from a document the user named.

## 5. Where every formula comes from

| Formula | Source | Status |
|---|---|---|
| τ_i(h) = Q_i(h) − Q_continue(h); choose argmax_a Q_a(h) | Zhang et al. (2026), Eq. (1) | quoted |
| Utility = outcome score − costs | Zhang et al. (2026), App. C.1 | quoted (form) |
| s = β0 + βᵀx; p = σ(γ1 s + γ0) | REM mathematical lock | unchanged |
| C_miss(k), C_FA(k) | REM Table 3.13; declared exploratory values | unchanged |
| Withhold iff C_miss(k)·ΔŜ(x) ≥ C_FA(k)·ΔÛ(x) | **derived** in `05`, section 2, from the lines above | DERIVED — NOT DIRECTLY QUOTED |
| `z_exp`, `z_del` | declared definitions motivated by PROVISO's admissibility statement and Task Shield's delegation remark | not published formulas |

No equation was invented and none is attributed to a paper that does not contain it. PROVISO's own controller was not implemented: no implementation is named in the paper, and it needs an encoder and an agent model that are not available.

## 6. Does the algorithm improve REM?

**No.**

| | Original REM | Tested candidate | Provenance rule (x_act1) | Strict explicit rule | REM without behavioural features (post hoc) |
|---|---|---|---|---|---|
| Successful attacks / 2,979 (primary folds) | 11 | 132 | 12 | 13 | 11 |
| Benign successes / 334 (primary folds) | 105 | 127 | 134 | 140 | 140 |
| Successful attacks (unseen task and objective) | 11 | 132 | 12 | 13 | 14 |
| Benign successes (unseen task and objective) | 105 | 110 | 134 | 140 | 140 |
| Attacks when the attacker account is written with spaces (of 2,645) | 11 | 13 | **191** | 13 | 11 |
| Authorized calls released / 178 | 33 | 66 | 92 | 83 | 83 |

Pre-declared test: the candidate's benign-utility gain over the original REM is +6.6 points [0.0, 18.2] on the primary folds and +1.5 [0.0, 4.5] under double holdout; neither interval excludes zero. Its rate of released attacker calls rises by 4.2 points [0.03, 12.4].

Why it fails: when the password-change attack is held out of training, the candidate releases all 119 such attacks. It learned "an attack is a payment to a new recipient" and treats a password copied from a document as a normal document-driven update.

## 7. What the results do and do not demonstrate

They demonstrate, on recorded AgentDojo banking trajectories:
- the original REM's security is obtained largely by withholding state-changing calls, and Modify, Escalate and Block have identical effect in this evaluation (0 of 3,313 episodes differ);
- its learned and cost-based layers add no measured value over simple provenance rules on this benchmark, while the behavioural features cost 35 benign tasks;
- outcome-supervised decision policies and document-delegation rules do not solve the problem, and the first does not transfer to an unseen attack objective;
- no method tested, learned or rule-based, can tell an authorized payment from an unrequested one whose recipient and amount appear in the user's words.

They do not demonstrate:
- anything about live or adaptive agents, human reviewers, or production systems;
- anything about other benchmarks or domains;
- any ranking against Task Shield, MELON or PROVISO, none of which could be run under the same conditions;
- that removing the behavioural features is a validated improvement: that observation is post hoc, on a corpus used many times, with only 16 user tasks behind the utility figures.

## 8. Decisions requested

| # | Decision | My recommendation |
|---|---|---|
| D1 | Adopt the tested candidate (outcome-supervised rule with authorization features)? | **No.** |
| D2 | Thesis algorithm | Retain the approved REM. |
| D3 | Add the simple rule baselines (x_act1; x_act1 or x_act2; strict explicit) to the thesis results as mandatory comparators? | **Yes.** The R4 examination already asked for this; the thesis is not defensible without them. |
| D4 | SD-FEAT: remove the behavioural evidence group from the final feature set? | For your decision. Evidence: same attacks, +35 benign tasks on the primary folds; +3 attacks under double holdout. If approved, declare it as an amendment and report both configurations; ideally confirm on trajectories not yet used. |
| D5 | Research gap wording | Adopt the narrowed wording in section 2. |
| D6 | Research questions RQ1–RQ4 (still `[PD]`) | Approve as *evaluation* questions; their answers here are largely negative (`10`). |
| D7 | Thesis title wording "behaviour-aware" | Reconsider, given D4 and the earlier C4 finding. |
| D8 | Published-defence comparison | Either authorise model access for a small live comparison (MELON before/after is prepared), or state in the thesis that no equal-terms comparison exists. |
| D9 | Authorization-aware extension (a structured statement of the user's intent supplied by the trusted interface, checked deterministically) | Future work only. Nothing tested here can establish authorization from text provenance. |

## 9. Evidence

All numbers: `REM_Authorization_Generalization_Study/results/study_results.json` and `weakness_audit.json`, produced by `experiments/authz_study/` on 11 November 2026. Protocol frozen before any outcome: commit `cca4968`. Three post-hoc additions are labelled (`06`, section 12).
