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

*(Added after the confirmatory run; see `REM_EXPERIMENTAL_RESULTS_VERIFIED.md`.)*
