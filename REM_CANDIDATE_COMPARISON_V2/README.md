# Four REM candidates — comparison v2

[PROPOSED — SUPERVISOR APPROVAL REQUIRED]

Implemented four distinct candidates and four C4 component ablations, in isolation from original REM and the preceding AA study. **333 tests pass with no skips.** The primary run executes 2,400 native replays; a complete-trace sensitivity executes another 2,400. Both reuse the **same 150 previously studied episodes**, not 4,800 independent samples. Results are development evidence, not final independent validation.

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

C2 improves the observed original REM point but does not outperform the simple x_act1 baseline. C1's safety changes substantially with the holdout grouping. C3's zero benchmark ASR conceals an amount-only attack vulnerability caught by tests; do not recommend it. C4's verification path has no empirical coverage because all ten recognized refund recordings contain no tool proposals.

Read `RESULTS.md`, `DESIGN_AND_SOURCES.md`, `VALIDITY_AND_REVIEW.md`, and `CLAUDE_REVIEW_RECONCILIATION.md`. Code is in `../experiments/rem_candidates_v2/`; commands are in `REPRODUCE.md`. No official thesis chapter, cost, feature specification or baseline result was changed.
