# REM Algorithm Improvement Study

[PROPOSED — SUPERVISOR APPROVAL REQUIRED]

Start with **07_EXPERIMENT_RESULTS.md**, then **10_SUPERVISOR_REVIEW.md**. The candidate was implemented and tested, but improvement was **not demonstrated**. It is not an approved thesis method.

| Policy | Native replay ASR | Benign task success |
|---|---:|---:|
| B0 | 73/135 (54.07%) | 9/15 (60.00%) |
| B1 | 31/135 (22.96%) | 9/15 (60.00%) |
| REM_R4 | 5/135 (3.70%) | 6/15 (40.00%) |
| x_act1 | 0/135 (0.00%) | 7/15 (46.67%) |
| AA_REM | 0/135 (0.00%) | 5/15 (33.33%) |

New cohort: 150 version-explicit AgentDojo v1.2.1 episodes, one recorded backbone; NO-ADAPT replay. Zero structured authorization contracts were available. x_act1 achieved the same observed zero ASR with higher benign completion than AA_REM. Software verification: 275 passed, no skips; fixture outcomes are never benchmark results.

Code: `../experiments/authorization_generalization/`. Reproduction: `11_REPRODUCTION_GUIDE.md`. Primary/raw evidence: `artifacts/`. Original research remains unchanged.
