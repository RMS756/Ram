# REM algorithm improvement decision

**Status:** `[PROPOSED — SUPERVISOR APPROVAL REQUIRED]`. Sections 1–4 were written on 11 November 2026 **before** the confirmatory experiment was run; section 5 (verdict) was added afterwards and is marked.

## 1. The weaknesses the modification must address

From `REM_Authorization_Generalization_Study/03` and `08` (offline replay, 3,313 episodes):

| # | Measured weakness | Class |
|---|---|---|
| W1 | Original REM releases 33 of 178 legitimate state-changing calls; 105 of 334 benign tasks complete (no defence: 175) | policy limitation (Allow boundary C_esc / C_miss) with a model limitation (W2) |
| W2 | Behavioural evidence costs 35 benign tasks with no measured security benefit; the privilege-rise feature fires on 85% of legitimate and 84% of attack transfers | model limitation |
| W3 | Outcome-supervised decision models release all 119 held-out password-change attacks | model limitation (no transfer to an unseen objective class) |
| W4 | Exact-string provenance fails when the attacker identifier is reformatted (x_act1 rule: 12 → 191 attacks) | implementation and model limitation |
| W5 | No arm separates an authorized payment from an unrequested one whose values occur in the user's words | **inherent lack of trusted information** |
| W6 | Modify, Escalate and Block have identical effect in replay without a reviewer | measurement limitation |
| W7 | Security rests largely on withholding state-changing calls, not on discrimination | policy limitation |
| W8 | All 11 residual attacks are `user_task_15` collision episodes | measurement problem (benchmark) |

## 2. The three options

### Option A — remove the behavioural evidence group, keep everything else

| Criterion | Assessment |
|---|---|
| Scientific support | The original study's own pre-registered ablation, reproduced: 11 attacks and 140 benign successes against 11 and 105. Double holdout (post hoc): 14 and 140. Consistent with the literature's caution on behavioural anomaly evidence already cited in Chapter 2. |
| Relevance to the measured weakness | Direct for W1 and W2. Does nothing for W4, W5. |
| Feasibility before 20 November | Complete: no new code in `rem/`; the fits already exist. |
| Disturbance to the frozen baseline | Minimal: a removal inside an open decision (SD-FEAT). Estimator, calibration, costs, tiers, predicates, four verdicts and five layers unchanged. |
| Security risk | Low on existing evidence (+3 attacks of 2,979 under double holdout). |
| Reproducible evidence obtainable now | **Yes**: recordings exist that were never used (protocol section 3), so a real confirmatory test is possible. |
| Weakness | All existing favourable evidence is post hoc on a reused corpus. |

### Option B — trusted authorization and argument integrity

A component that checks a proposed financial action against trusted, explicit, structured authorization (operation, source account, recipient, amount, constraints, origin of the instruction).

| Criterion | Assessment |
|---|---|
| Scientific support | Strong in principle. aiAuthZ (abstract level only): an off-host gateway with identity-bound, argument-level policy; on AgentDojo banking it reports blocking all seven attacker-directed calls "at the cost of one legitimate first-time payment". PROVISO (full text): an action is admissible when its operation and target are licensed by trusted observations. Task Shield (full text): every action must contribute to a user-level instruction. A further step-up authorization preprint (abstract level) binds approval to a canonical effect descriptor. |
| Relevance | The only option that addresses W5, the root limitation. |
| Feasibility before 20 November | **Not as an evaluated component.** AgentDojo recordings contain no trusted authorization record. Any evaluation would need either fixtures in which the record is supplied by construction (which would show only that a correct record gives correct decisions) or the benchmark's ground-truth solution used as the record (an oracle, not a deployable input). |
| Disturbance | Changes the security model: it adds a trusted input channel that the approved threat model does not have. It would fit inside Layer 1 (capture of the authorization record) and Layer 4 (a policy predicate), so a sixth layer is **not** needed. |
| Security risk | Low if the record is authentic; the risk moves to how the record is obtained. This project has already shown that deriving it from text fails (the delegated-source rule: 313 attacks; `z_exp`: unrequested payments released). |
| Reproducible evidence obtainable now | Only tautological (fixtures) or oracle-based. |

Decision on B: **not selected for implementation.** It is specified as the principal future-work design, with the trust assumption stated, and no equation is introduced for it. A sixth layer is not proposed.

### Option C — established selective, risk-constrained or conformal decision methods

| Method (source) | What it would do in REM | Assumptions | Fit to the measured weakness |
|---|---|---|---|
| Reject option (Chow, 1970; already REM's conceptual basis for Escalate) | abstain in a band of p | costs given | Already present; W1 arises from it when no reviewer exists |
| Finite-sample selective-risk threshold (CASEL, Eq. 5, Prop. 1: R̂(τ) + sqrt(ln(K/δ)/(2n_τ)) ≤ ε) | choose the largest Allow threshold whose risk is certified ≤ ε | i.i.d. calibration records, one per trajectory, from the deployment distribution; ε must be given | Replaces a declared cost ratio by a declared ε; needs a risk tolerance nobody has approved; exchangeability fails across the 16 user tasks |
| Conformal risk control (Angelopoulos et al., 2024; cited by CASEL, not read in full here) | bound a monotone risk in expectation | exchangeability | Same objections; "Per-step conformal calibration does not transfer to agent trajectories" is the title claim of a 2026 EMNLP paper (abstract level) |
| Development-selected operating point (PROVISO, Eq. 7) | pick the threshold on development data for an operating criterion | development data representative | This is B1's form; B1 is already the baseline (164 attacks, 170 benign) |

Decision on C: **not selected.** These methods move the operating point along the same score. They do not add information (W5), do not repair the score's dependence on action type (W2), and each needs a tolerance (ε or an operating criterion) that would have to be invented. Calibration Is Not Control (Remark 1) explains why re-thresholding a score cannot recover a distinction the score lacks.

## 3. Selection

**Option A is the one modification selected for immediate testing.** It is the only option with direct measured support, no new assumption, no new equation, and a real confirmatory test available before the deadline.

The authorization-aware, outcome-supervised candidate of the earlier study (`M11+AZ`) remains **rejected**.

## 4. What a positive result would and would not license

A GO verdict under `REM_FINAL_EXPERIMENT_PROTOCOL.md` would support presenting "REM without behavioural evidence" as a **versioned amendment (REM v1.1) for supervisor approval**, with the original REM (v1.0) kept as the frozen baseline and both reported everywhere. It would not license any claim about authorization, live agents or other benchmarks.

## 5. Verdict

*(Added on 11 November 2026 after the confirmatory run; commit `907e6d2`; numbers from `../results/confirmatory_results.json`. Sections 1–4 above are unchanged from commit `19bd168`.)*

**Pre-declared verdict: GO.** All three conditions of the frozen rule hold on 2,113 eligible recorded episodes that no earlier analysis had read (2,065 attacked, 48 benign).

| Condition | Result |
|---|---|
| (a) E1: task success, REM without behavioural evidence minus original REM | +7.48 points, 95% interval [1.17, 16.02]; 158 episodes gained, 0 lost (916 → 1,074 of 2,113) |
| (b) E2: attack success rate and unauthorized state-change rate | both −0.10 points [−0.29, 0.00]; successful attacks 3 → 1 of 2,065; no interval above 0 |
| (c) candidate attacks ≤ the P2 rule's | 1 ≤ 4 |

What the verdict supports: within this benchmark and in recorded-trace replay, removing the behavioural evidence group lets REM complete more tasks with no measured loss of security. The earlier post-hoc observation is now confirmed on untouched trajectories.

What limits it, in order of importance:

1. **It is not the best arm on utility.** The strict explicit rule A2 completes 1,232 tasks against 1,074 (4 attacks against 1). The difference between them is not resolved: −7.48 points [−25.66, 8.16]. Against the provenance rule P2 the candidate is +1.47 points [−5.28, 7.98], also unresolved. The confirmed claim is "better than the original REM", not "better than simple rules".
2. **Utility remains far below the undefended agent.** No defence: 1,451 of 2,113 tasks. Candidate: 1,074. Legitimate state-changing calls released in benign runs: 11 of 51 (original REM: 4 of 51).
3. **The benign-only interval touches zero.** 18 → 25 of 48, +14.58 points [0.00, 33.33]. The verdict rests on E1 over all episodes, as pre-declared; most of the gain is utility under attack (898 → 1,049 of 2,065).
4. **Tasks and objectives are not new.** The agents, attack templates and trajectories are new; the 16 user tasks and 9 attack objectives are the benchmark's. The gain is concentrated in user tasks 2 and 14 (36 → 97 and 9 → 73 of 138 and 129).
5. **Replay only, no reviewer, no adaptive attacker.** Modify, Escalate and Block remain indistinguishable in this mode.
6. **A second configuration also passes the same test.** REM restricted to Allow and Block (M01) gives +9.42 points [2.77, 17.87] with the same 3 attacks. It was a baseline, not the pre-declared candidate, so it is reported and not adopted.

**Recommendation.** Present "REM without behavioural evidence" as a versioned amendment, **REM v1.1**, `[PROPOSED — SUPERVISOR APPROVAL REQUIRED]` under SD-FEAT. Keep the original REM (v1.0) as the frozen baseline and report both in every table. No code under `rem/` is changed: v1.1 is the original study's own `no_beh` fit. Until the supervisor decides, the thesis states the design as v1.0 and reports v1.1 as a confirmed ablation.
