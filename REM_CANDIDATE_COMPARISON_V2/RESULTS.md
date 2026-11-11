# Actual candidate comparison results

[PROPOSED — SUPERVISOR APPROVAL REQUIRED]

## Primary: held-out attack objectives

Same explicit-version AgentDojo v1.2.1 cohort as the previous study, excluding task 15: 135 attacked episodes, 15 benign episodes, one recorded Llama-3.3-70B pipeline. All B0 outcome checks agree with records. This is stateful simulator replay under NO-ADAPT, not a live or adaptive agent test.

| Policy | ASR (135 attacked) | Benign success (15 tasks) | Utility under attack |
|---|---:|---:|---:|
| B0 | 73/135 (54.07%) | 9/15 (60.00%) | 84/135 (62.22%) |
| B1 | 31/135 (22.96%) | 9/15 (60.00%) | 76/135 (56.30%) |
| REM_R4 | 5/135 (3.70%) | 6/15 (40.00%) | 60/135 (44.44%) |
| x_act1 | 0/135 (0.00%) | 7/15 (46.67%) | 66/135 (48.89%) |
| AA_REM_previous | 0/135 (0.00%) | 5/15 (33.33%) | 54/135 (40.00%) |
| C1_action_model | 9/135 (6.67%) | 7/15 (46.67%) | 61/135 (45.19%) |
| C2_canonical_provenance | 0/135 (0.00%) | 7/15 (46.67%) | 65/135 (48.15%) |
| C3_target_only | 0/135 (0.00%) | 7/15 (46.67%) | 72/135 (53.33%) |
| C4_verified_refund | 0/135 (0.00%) | 7/15 (46.67%) | 65/135 (48.15%) |

C2 versus original REM: benign completion +6.67 percentage points (paired task-bootstrap 95% interval [0.00,20.00]); ASR −3.70 points (objective-bootstrap interval [−11.11,0.00]). Fifteen benign tasks and nine objectives give weak precision. This is a promising observed point relative to REM, not a demonstrated generalizable improvement.

C2 versus x_act1: identical benign success and ASR, but one fewer attacked task succeeds (65 versus 66). The difference is a legitimate `update_scheduled_transaction(id='7', amount='1200.0')` refused by C2's stricter ID schema, though the native backend accepts that representation. This trade-off is retained and disclosed; no post-test tuning is hidden.

C1 increases benign completion from 6/15 to 7/15, but raises successful attacks from 5/135 to 9/135. It therefore does not preserve primary security performance. C3 improves attacked-task utility but fails the independent amount-only stress case and cannot be recommended from these outcome scores.

## Secondary: held-out user tasks

| Policy | ASR (135 attacked) | Benign success (15 tasks) | Utility under attack |
|---|---:|---:|---:|
| B0 | 73/135 (54.07%) | 9/15 (60.00%) | 84/135 (62.22%) |
| B1 | 37/135 (27.41%) | 9/15 (60.00%) | 78/135 (57.78%) |
| REM_R4 | 0/135 (0.00%) | 5/15 (33.33%) | 58/135 (42.96%) |
| x_act1 | 0/135 (0.00%) | 7/15 (46.67%) | 66/135 (48.89%) |
| AA_REM_previous | 0/135 (0.00%) | 5/15 (33.33%) | 54/135 (40.00%) |
| C1_action_model | 0/135 (0.00%) | 7/15 (46.67%) | 66/135 (48.89%) |
| C2_canonical_provenance | 0/135 (0.00%) | 7/15 (46.67%) | 65/135 (48.15%) |
| C3_target_only | 0/135 (0.00%) | 7/15 (46.67%) | 72/135 (53.33%) |
| C4_verified_refund | 0/135 (0.00%) | 7/15 (46.67%) | 65/135 (48.15%) |

The original REM changes to 0/135 ASR and 5/15 benign success; C1 changes to 0/135 and 7/15. This dependence on splitting is material. It is misleading to select only the grouping that makes a candidate look best. No learned candidate establishes stable dominance over simple provenance across both groupings.

Statistical fitting excludes every test task from training/calibration/residual fitting in this secondary analysis. Policy design still used previously seen task text, so this is model task holdout, not an unseen domain for the researcher.

## C4 coverage and ablations

Ten recordings match the bounded refund request, but **all ten have zero tool proposals**. Therefore actual backend accesses and verified repairs are both zero. With a fixed recorded actor, a defense cannot complete a task whose agent never proposes an operation. C4 and the four ablations have identical primary outcomes because their new capability is never exercised. This is not evidence of component effectiveness or irrelevance in a covered workload.

Synthetic native integration tests do verify actual repaired execution and withholding when verification is unavailable. Their results are correctness evidence, not benchmark effectiveness data. These fixtures never become training or empirical comparison rows.

## Complete-trace validity sensitivity

The original AgentDojo execution loop has a 15-round default. A retained trajectory records 16 proposals but evaluates only 15 under that inherited limit. A post-hoc sensitivity, declared separately before its outcomes, derives the loop bound from the complete recorded tool-bearing assistant messages. The same 150 episodes and frozen policies were rerun; **no paired security or task-success outcomes changed** and B0 agreement remained intact. All recorded proposals were evaluated in this sensitivity. Primary figures remain comparable to the previous 15-round harness, with the truncation disclosed.

There are 2,400 native runs per horizon. The secondary grouping reuses 1,500 fixed-policy outcome rows within each horizon instead of pretending they are new executions or samples. Paired rows total 3,900 per horizon; distinct episodes remain 150.

## Decision diagnostics

`artifacts/diagnostics.json` reports per-objective native-prefix calibration/attempt-release diagnostics and C4 coverage. It does not invent a “high confidence” cutoff or claim that low-risk mistakes are solved. Reference-positive attempts are not independent permission labels; native outcomes are reported separately. Historical password-positive counts were independently checked: 124 over all original primary steps, 122 over the original AM4 replay-valid subset; neither is a count for the new small cohort.

No inference is drawn that requires a real bank or mandatory live testing. A fresh task/objective-disjoint controlled dataset, including legitimate external arguments and amount-only threats, is needed before an improvement claim.
