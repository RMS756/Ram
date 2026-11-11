# 03 — Weakness audit of the original REM (R4)

**Evidence.** All numbers are recomputed in this study from the unchanged pilot pipeline (code identical to commit `9fddfa7` in every executed file; fresh refit byte-identical to the frozen state). Scripts: `experiments/authz_study/weakness_audit.py` → `results/weakness_audit.json`; earlier audit `REM_AUTHORIZATION_AUDIT/`. Mode: offline recorded-trace replay, step level, no reviewer, NO-ADAPT. Corpus: 3,313 eligible episodes (2,979 attacked, 334 benign).

**Source-of-truth notes.**
- The latest implementation of the approved design is on `claude/rem-r4-corrections-3ktvze` (`9fddfa7`). `claude/rem-algorithm-implementation-3ktvze` on GitHub is older (R3, `181a38c`). `codex/rem-ollama-pilot` (`fca0319`) adds a local Ollama pilot and a refactor of one helper; it contains no change to features, estimator or decision rule.
- The planning documents `REM_SOURCE_OF_TRUTH.md`, `REM_CUT_PLAN.csv`, `REM_CUT_PLAN_README.md` and `REM_SCOPE_AND_GAP_DECISION_MEMO.md` are **not present** in any branch of the repository available to this session. Nothing is inferred about their content.
- Open supervisor decisions that this audit touches: SD-1 (costs), SD-3 (Modify mechanism), SD-4 (predicates), SD-FEAT (final feature set), SC-1 (mitigation semantics), REVIEWER (escalation resolution), LABEL-UT15, TITLE (`SUPERVISOR_DECISIONS_REQUIRED.md`).

## Problem A — Over-defence

Verdicts of the original REM on **legitimate calls in benign episodes**, by action category:

| Category | Calls | Allow | Modify | Escalate | Block | Released |
|---|---|---|---|---|---|---|
| Value transfer (send / schedule) | 89 | 4 | 31 | 49 | 5 | 4 (4%) |
| Payment modification | 34 | 8 | 0 | 26 | 0 | 8 (24%) |
| Profile change | 37 | 21 | 0 | 16 | 0 | 21 (57%) |
| Credential change | 18 | 0 | 0 | 18 | 0 | 0 (0%) |
| **All state-changing** | **178** | **33** | 31 | 109 | 5 | **33 (19%)** |
| Read-only | 369 | 369 | — | 0 | 0 | 369 (100%) |

Verdicts on **attacker-induced calls** (y = 1) in attacked episodes: value transfer 653 (25 Allow, 499 Modify, 93 Escalate, 36 Block); payment modification 132 (116 Modify, 16 Escalate); credential change 122 (122 Escalate).

Findings:
- Read-only operations are never impeded.
- Over-defence is concentrated in state-changing calls: 145 of 178 authorized calls are withheld, 109 of them by Escalate.
- Every legitimate credential change is escalated; so is every attacker-induced one. On that category REM does not discriminate at all: it withholds the category.
- Episode level: benign successes fall from 175 (no defence) to 105 of 334. With an idealized reviewer they would be 166, so most of the loss is escalations that no one resolves.
- "Delayed" cannot be measured: replay has no time dimension for a pending review.

Cause (traced in `REM_AUTHORIZATION_AUDIT/REM_AUTHORIZATION_ROOT_CAUSE_REPORT.md`): Allow needs p < C_esc / C_miss(k) = 0.03 or 0.015, while the first transfer of an episode already scores about 0.03 from the privilege-rise feature.

## Problem B — Feature–label leakage (x_act1)

Contingency over all 6,762 primary steps:

| | x_act1 = 0 | x_act1 = 1 |
|---|---|---|
| y = 0 | 4,982 | 859 |
| y = 1 | 27 (all in `user_task_15` episodes) | 894 |

- As a classifier of the attempt label, x_act1 alone has recall 0.971, false-positive rate 0.147 and precision 0.510.
- The label is built from the attacker's key argument; x_act1 is built from the same argument's provenance. In this benchmark the attacker value enters only through injected text, so the two are nearly the same quantity.
- Is the model learning a general property? Three tests from this study say **not robustly**:
  1. **Reformatted identifier probe** (attacker IBAN written in groups of four in the injected text; 2,645 attacked episodes; nothing refitted): the x_act1 rule goes from 12 to **191** successful attacks, B1 from 45 to 198. The original REM stays at 11, but only because x_act2 ("recipient not in the objective") still fires and because it withholds nearly every first payment.
  2. **Legitimate beneficiaries whose identifiers appear in tool outputs:** x_act1 fires on 86 of 178 authorized calls. By user task it fires on 13/13 (`user_task_0`), 16/16 (`user_task_13`), 12/12 (`user_task_5`), 14/14 (`user_task_6`), 6/6 (`user_task_11`). The feature marks delegated legitimate values exactly as it marks attacks.
  3. **Unseen attack objective with a different argument pattern:** see `08` (the password-change objective).
- Paraphrased, fragmented or "trusted-looking document" variants beyond the one probe above were not constructed. The matcher's known boundary cases (spaced IBAN, comma-grouped decimals, coincidental numbers) are documented in `CODE_AUDIT_R4` (CV-8) and `REM_AUTHORIZATION_AUDIT` (F-IMPL-1).

## Problem C — Dataset and label validity

| Item | Finding |
|---|---|
| Suite versions | 3,154 eligible episodes carry no recorded benchmark version; 159 are v1.2.1. Replay uses suite v1; 21 of 3,334 episodes do not reproduce and are excluded (AM-4). Injection-task ground truths are identical across versions (earlier check). |
| `user_task_15` collision | In 152 eligible episodes the user's own objective contains the attacker IBAN. 29 y = 1 steps are in `user_task_15` episodes; 27 of them have x_act1 = 0. |
| Effect on the headline | All 11 of the original REM's successful attacks are `user_task_15` episodes. Without that user task: 0 of 2,811 attacks; benign successes unchanged at 105 of 313. |
| Attempt label vs actual success | Of 921 y = 1 steps, withholding the step prevents the benchmark's attack success in 704; in 217 it does not (the attack failed anyway, or another step completes it). 3 y = 0 steps prevent an attack success when withheld. |
| Attempt label vs user-task outcome | Withholding a step breaks the user task in 757 steps (751 of them y = 0) and *restores* it in 112. |
| Exclusions | None beyond AM-1 (ambiguous pairs, pre-run) and AM-4. No sample was discarded in this study; the `user_task_15` analysis is a reported sensitivity analysis. |

The four notions are now separated in the data: user-authorized action (benign-episode calls), attacker-requested action (y), attempt label (y), actual attacker success (S and the branch outcome a).

## Problem D — Component contributions (original REM ablations, reproduced as counts)

| Configuration | Successful attacks / 2,979 | Benign successes / 334 | Utility under attack / 2,979 |
|---|---|---|---|
| Original REM | 11 | 105 | 1,083 |
| Behavioural evidence removed | 11 | **140** | 1,147 |
| Context evidence removed | 11 | 105 | 1,081 |
| Action evidence removed | 17 | 105 | 1,062 |
| Calibration removed | 11 | 110 | 1,102 |
| Predicates removed | 11 | 105 | 1,078 |
| Single tier 1 / 2 / 3 / 4 | 152 / 66 / 11 / 10 | 147 / 118 / 113 / 105 | 1,383 / 1,191 / 1,111 / 1,076 |
| B1 (same estimator, thresholds) | 164 | 170 | 1,532 |

- **Behavioural evidence** costs 35 benign episodes and buys no measured security. It is the one component whose removal changes the result materially, and in the favourable direction.
- **Context evidence** and **predicates** make no measurable difference.
- **Calibration** makes a small difference in the unfavourable direction (removing it gives +5 benign episodes at the same attack count). This agrees with Calibration Is Not Control, Remark 1, for threshold policies, and with the earlier REM-Lite ≡ B1 result.
- **Action evidence** is the only group whose removal costs security (+6 attacks).
- **Consequence tiers** matter only through the cost ratio: a single tier 3 gives the same security with slightly more utility.
- **Expected loss vs thresholds (B1):** the expected-loss rule prevents 153 more attacks than B1 and loses 65 benign episodes.

## Problem E — Do Modify, Escalate and Block differ in replay?

Test: the original REM was re-run with every non-Allow verdict replaced by Block (3,313 episodes).

| Quantity | Result |
|---|---|
| Episodes whose utility or security changed | **0** |
| Episodes whose sequence of released calls changed | **0** |
| Episodes whose underlying expected-loss verdict sequence changed | 25 (the text of REM's own refusal notice differs by verdict and is re-ingested as untrusted text; no release decision changed) |
| Attacks / benign successes | 11 / 105 in both runs |

Under step-level replay without a reviewer, the three withholding verdicts are **indistinguishable in effect**. Consequences:
- No result of the original study can show that Modify is better than Block or that Escalate is better than either.
- r_mod, the measured residual success under Modify, is the residual success of *withholding*.
- The original study's benefits come from withholding calls, not from the choice among interventions. A learned policy over interventions cannot be trained from this data without inventing outcomes.

## Summary

| Problem | Verdict |
|---|---|
| A Over-defence | Confirmed; 19% of authorized state-changing calls released |
| B Leakage | Confirmed; x_act1 nearly reproduces the label and is brittle to reformatting |
| C Label validity | Confirmed; all residual attacks are collision episodes; attempt and outcome labels differ on 220 steps |
| D Component value | Behavioural evidence harms utility; context, predicates and calibration add nothing measurable |
| E Intervention semantics | Modify, Escalate and Block are identical in effect in this evaluation mode |
