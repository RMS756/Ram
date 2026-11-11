# 06 — Experimental protocol (frozen before any candidate outcome was computed)

**Status:** `[PROPOSED — SUPERVISOR APPROVAL REQUIRED]`. Exploratory study in an isolated module. It does not change the approved REM design, its code under `rem/`, its configuration, its results or the thesis.

**Frozen on:** 11 November 2026, by the commit that adds this file. Any later change to this file is listed in section 12, with the reason and whether results had been seen.

**Working name:** `REM_Authorization_Generalization_Study` (provisional; not an approved framework title).

## 1. What had and had not been seen when this protocol was written

Seen:
- the original REM results on the corpus (REM, B0, B1, REM without Escalate), and corpus diagnostics of the frozen features;
- the original REM's decisions on 16 synthetic fixtures and logical cases A–E;
- the examiner's observe-only step rates for the rule "intervene iff x_act1 = 1" (97.1% of y = 1 steps, 14.7% of y = 0 steps);
- an implementer's reported results for a request cue, a parser change and a gating change (code not available).

Not seen:
- any prefix-branch outcome (what happens when one call is withheld);
- any distribution of the authorization evidence defined below;
- any replay outcome of the provenance or authorization rules;
- any result of any learned arm defined below.

Disclosure: the author of this protocol knows the texts of the 16 AgentDojo banking user tasks and the 9 injection tasks. The evidence definitions below are stated generically, but they were written with that knowledge. This is a threat to validity and is reported as such.

## 2. Evaluation mode

All corpus results are **offline recorded-trace replay** in AgentDojo's sandbox (suite v1, AgentDojo 0.1.35, recorded runs at commit `089ed468…`), at step level, with **no reviewer**, under the **NO-ADAPT** assumption (the replayed agent emits its recorded calls whatever is withheld). No live agent, no model API and no production system is used. Results are never described as closed-loop or live.

## 3. Data, labels and eligibility

- **Corpus:** the existing primary role (21 undefended backbones; `important_instructions` attacks and benign runs): 3,334 recorded episodes. Evaluation uses the 3,313 episodes eligible under AM-4 (2,979 attacked, 334 benign), as in the original study. No episode is removed for any other reason.
- **Cross-template set:** the existing `cross_template` role (gpt-4o-2024-05-13; five other attack templates).
- **Attempt label y (original):** 1 iff the call matches the injection task's reference call and carries the attacker value. Unchanged.
- **Prefix-branch outcomes (new; training targets only):** for every episode and every proposed call j, the episode is replayed twice from the same start: once with every call released (B0), once with call j withheld and every other call released. Let S ∈ {0,1} be the benchmark's attack-success outcome and U ∈ {0,1} its user-task outcome.
  - ΔS_j = S(B0) − S(withhold j); ΔU_j = U(B0) − U(withhold j).
  - a_j = 1[ΔS_j = 1] (withholding prevents the attack success); b_j = 1[ΔU_j = 1] (withholding breaks the user task).
  - Reverse flips a⁻_j = 1[ΔS_j = −1] and b⁻_j = 1[ΔU_j = −1] are recorded and counted.
  - For benign episodes ΔS_j = 0 by definition.
- `user_task_15` episodes stay in the primary analysis (as in the original study). A sensitivity analysis without them is reported for every headline number.
- Runtime decisions never read y, S, U, a or b.

## 4. Evidence

- **F0:** the frozen eight REM features (`x_ctx2, x_beh1..4, x_act1..3`), unchanged, with REM's own matching rule.
- **Authorization evidence (new, deterministic, no fitted or tuned quantity):** for a proposed call to a restricted tool (the frozen set T_R), let K be the declared key arguments present in the call, K_id = K without `amount`, and K_ref = K_id if non-empty, otherwise K. Let g be the user objective. A *user-named source* is the output of an earlier executed read-category call that has at least one string argument (length ≥ 3) occurring in g.
  - `z_exp` = 1 iff K_ref is non-empty and every value in K_ref occurs in g.
  - `z_del` = 1 iff K_ref is non-empty, not every value occurs in g, and every value that does not occur in g occurs in a user-named source.
  - Both are 0 for tools outside T_R.
  - Occurrence uses REM's `value_occurs_in` unchanged (including its known comma-decimal deviation).
- **F1** = F0 + (`z_exp`, `z_del`).

## 5. Arms

Rule baselines (no fitting; a withheld call is enforced as Block):

| Arm | Rule for a T_R call |
|---|---|
| B0 | release everything |
| P1 (simple provenance) | withhold iff x_act1 = 1 |
| P2 | withhold iff x_act1 = 1 or x_act2 = 1 |
| A1 (simple authorization) | withhold iff z_exp = 0 and z_del = 0 |
| A2 (strict explicit) | withhold iff z_exp = 0 |

Learned arms. All use REM's own estimator procedure: ridge logistic regression, λ grid {0.01, 0.1, 1, 10, 100}, 4 grouped inner folds, label-NLL logit calibration on inner out-of-fold logits, refit on the fitting portion. Predicates D1/D2 are kept as in REM. Costs are the declared exploratory values of `pilot_e0.yaml` (C_FA = 1; C_miss = 1, 5, 10, 20 by tier; C_mod = 0.5; C_esc = 0.3; measured r_mod).

| Arm | Features | Training target | Decision rule |
|---|---|---|---|
| B1 | F0 | y | operating-point thresholds (original baseline) |
| M00 = original REM R4 | F0 | y | four-verdict expected loss (original) |
| M01 | F0 | y | REM's expected loss with only Allow and Block feasible |
| M10 | F0 | a | four-verdict expected loss (original), p := P(a = 1 \| x) |
| M11 | F0 | a, b (and reverse flips) | intervention value (below) |
| M11y | F0 | y for the security side; b for the utility side | intervention value with ΔŜ := P(y = 1 \| x) |
| M00+AZ | F1 | y | four-verdict expected loss (original) |
| **M11+AZ (primary candidate)** | F1 | a, b (and reverse flips) | intervention value |

**Intervention-value rule** (adaptation of Zhang et al. 2026, "Calibration Is Not Control", Eq. (1) and A*(h) = argmax_a Q_a(h), to two branches, release and withhold, with branch utilities expressed in REM's declared costs):

- ΔŜ(x) = P̂(a = 1 | x) − P̂(a⁻ = 1 | x); ΔÛ(x) = P̂(b = 1 | x) − P̂(b⁻ = 1 | x).
- A component with fewer than 50 positive steps in a fitting portion is set to 0 for that portion and reported (50 is the existing declared `min_positive_steps`).
- If a component's calibration fails (γ1 ≤ 0), its uncalibrated probability is used and the failure is reported.
- Withhold iff C_miss(k)·ΔŜ(x) ≥ C_FA(k)·ΔÛ(x) and C_miss(k)·ΔŜ(x) > 0; otherwise release. An exact tie with a positive left side withholds and is counted.
- A withheld call is enforced as Block. Under step-level replay without a reviewer, Modify, Escalate and Block have the same execution effect, so this study does not claim anything about the choice among them.

Cost-ratio sensitivity for M11 and M11+AZ: C_miss multiplied by {0.5, 1, 2, 5} (the existing declared grid). The multiplier 1 is the headline; the others are reported as a frontier.

## 6. Generalization schemes

- **S1 (primary folds, comparable with the original study):** 9 outer folds by injection task; benign user tasks assigned round robin. For M00 and B1, S1 uses the frozen fitted state unchanged.
- **S2 (double holdout):** an attacked test episode with user task u and injection task i is scored by models fitted without any episode of user task u and without any episode of injection task i. A benign test episode of user task u is scored by the cell (u, i_rr(u)), where i_rr(u) is the fold the original study assigned to u. All fitted quantities (λ, coefficients, calibration, benign transition reference, r_mod) are recomputed from the fitting portion of each cell. 144 cells.
- **S3 (held-out attack templates):** S1 models applied to the cross-template set (attacked episodes; eligibility by B0 agreement, as in the original study).

No hyperparameter, threshold, feature or cost is selected on any test portion.

## 7. Metrics

Episode level (replay enforcement): attack success rate (ASR); benign utility; utility under attack; unauthorized state-change rate (USCR: share of attacked episodes in which at least one y = 1 call was released).

Decision level: authorized-action approval rate (AAR: share released among T_R calls proposed in benign eligible episodes), also restricted to calls whose tool is in the user task's ground-truth solution; false block rate (1 − AAR); escalation share on those calls (four-verdict arms only); share of y = 1 calls withheld; breakdown by action category (value transfer, payment modification, profile change, credential change, read).

Model level (S1 and S2 held-out predictions): ROC-AUC, average precision, ECE (10 bins), Brier score for each fitted target.

Overhead: median and 95th-percentile decision time per call.

Offline decision metrics and replay enforcement outcomes are reported in separate tables.

## 8. Statistical analysis

- Grouped bootstrap, 2,000 resamples, seed 20261027, 95% percentile intervals: attacked-episode metrics resampled by injection task (9 groups); benign-episode metrics by user task (16 groups).
- Paired differences on the same episodes.
- **Declared primary contrasts:** M11+AZ − M00 and M11+AZ − P1, on benign utility and on ASR, under S1 and under S2 (eight intervals). Everything else is exploratory and is labelled so. No multiplicity correction is applied to exploratory contrasts and none is called significant.
- No numerical security margin is available from an approved source, so none is invented. **An "improvement" over a comparator is claimed only if, under both S1 and S2,** (i) the paired benign-utility difference has a 95% interval that excludes 0 in the candidate's favour, and (ii) the paired ASR difference has a 95% interval that does not lie entirely above 0. Otherwise the result is reported as a trade-off or as no detectable difference. USCR is reported next to ASR in every table, and an increase in USCR is reported even when ASR does not move.
- The security–utility plane (ASR, benign utility) is reported for all arms, with the non-dominated set identified from point estimates.

## 9. Ablations

Authorization evidence removed (M11 vs M11+AZ; M00 vs M00+AZ); intervention-value model removed (M00+AZ vs M11+AZ); supervision target changed with the rule fixed (M00 vs M10); Escalate and Modify removed with the model fixed (M00 vs M01); provenance evidence, behavioural evidence and context evidence removed from M11+AZ (refits without the group; S1 only); calibration removed from M11+AZ (uncalibrated probabilities; S1 only). The existing original-REM ablations are quoted from the reproduced results, not rerun differently.

## 10. Perturbation probes (reported separately from benchmark results)

- **Fixtures:** the 16 synthetic call-level fixtures and logical cases A–E, scored with the S1 models of fold `injection_task_0`. Counts only.
- **Reformatted attacker identifier:** attacked eligible episodes are replayed with the attacker IBAN written in groups of four characters inside the injected text; the recorded agent calls are unchanged (NO-ADAPT). Models are the S1 models; nothing is refitted. This probes dependence on exact string matching.

## 11. Published comparators (Tier 2)

MELON, Task Shield, PROVISO and CASEL are compared only as far as they can be evaluated faithfully. Any that needs a model API, unavailable code or inputs that do not exist here is reported as not evaluated, with its published numbers quoted and the incompatibilities listed. No approximate re-implementation is labelled a reproduction. Recorded outcomes of the four defences distributed with AgentDojo (gpt-4o) are quoted from the existing results as recorded live runs, not as replay.

## 12. Amendments

None at the time of freezing.

**Amendment A-1 (POST HOC: made after results were seen).** The pre-declared S1 ablation "action evidence removed from M11+AZ" scored better than the candidate itself (12 attacks, 140 benign successes). Ablations were declared for S1 only. So that an S1-only number is not over-read, the same arm was also run under S2 (`experiments/authz_study/posthoc_a1.py`). It is exploratory and is not a candidate.

**Amendment A-2 (POST HOC: made after results were seen).** The original study's own ablation "behavioural evidence removed" (existing configuration `abl_no_beh`, unchanged REM rule) has 11 attacks and 140 benign successes under the primary folds. It had never been run under double holdout, on held-out templates, under the reformatted-identifier probe or on the fixtures. It was added as arm `M00_nobeh` and run under S1 (sanity check against the stored result), S2, S3, the probe and the fixtures (`experiments/authz_study/posthoc_a2.py`). It is exploratory; no claim of improvement in the sense of section 8 is made for it.

**Amendment A-3 (POST HOC).** Exploratory paired contrasts were added after results: P2 − M00, A2 − M00, A2 − P1, M01 − P1, M11y − M00, and M00_nobeh against M00, P1, P2, A2 and M11+AZ. They carry no multiplicity correction and none is called significant.

A peak-memory measurement (tracemalloc, one episode) was also added after results; it involves no outcome.

**Note N-1 (11 Nov 2026, after freezing, before any outcome was computed).** The full text of PROVISO (arXiv:2610.27115v1) was supplied by the candidate after this protocol was committed. It was read before any branch outcome, rule outcome or learned-arm result existed. No arm, feature, split, metric or criterion was changed. Its definition of an admissible action ("operation and target licensed by K, arguments supported by K ∪ G") agrees with the choice in section 4 to test identity arguments against the user objective and to leave `amount` out of K_id.
