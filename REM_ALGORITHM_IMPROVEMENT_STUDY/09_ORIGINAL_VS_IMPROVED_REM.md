# Original versus proposed REM

[PROPOSED — SUPERVISOR APPROVAL REQUIRED]

The name “improved” is a research goal, not an established result. The implemented permission candidate does **not** improve the observed trade-off.

| Policy | Native replay ASR | Benign task success |
|---|---:|---:|
| B0 | 73/135 (54.07%) | 9/15 (60.00%) |
| B1 | 31/135 (22.96%) | 9/15 (60.00%) |
| REM_R4 | 5/135 (3.70%) | 6/15 (40.00%) |
| x_act1 | 0/135 (0.00%) | 7/15 (46.67%) |
| AA_REM | 0/135 (0.00%) | 5/15 (33.33%) |

Original R4 is preserved. The new comparison refits its original policy on the explicit-version cohort. It should not be compared numerically to mixed-version historical 0.37% ASR as if dataset composition and model fitting were identical.

AA_REM withholds every unverified mutation and so has lower replay ASR than the refitted REM, but also lower benign completion. A simpler x_act1 gate reaches the same observed zero ASR with higher completion. The Pareto plot `artifacts/security_utility.png` therefore gives no reason to prefer AA_REM. No security margin was declared and none is inferred from a zero-event cohort.

Original mitigation and proposed Modify have different semantics: original step-level Modify withholds; candidate Modify actually executes independently authorized replacement arguments. This is tested natively with synthetic contracts but never exercised on the legacy efficacy cohort. It cannot explain an empirical improvement that did not occur.

The useful engineering result is a testable contract/evidence interface. The scientific finding is that provenance detection scores and missing authorization evidence are not interchangeable with an authorization model. Independent permission acquisition and annotation are prerequisites to an adequate test of the proposed research question.
