# Claim audit of the fifth edition (17 November 2026)

Method as in the fourth edition (`../thesis_r4/audit/CLAIM_AUDIT_R4.md`): tables generated from result files; number audit of the rewritten text; cross-references, page references and citations checked by script. The claims below are those added or changed in this edition. The full audit of the study is `REM_COMPETITIVE_STUDY_2026_11_16/09_CLAIM_AUDIT_AND_CHANGE_LOG.md`.

| Claim in the thesis | Status | Evidence |
|---|---|---|
| The guard used alone (GV) has the outcomes of every learned or calibrated decision tested behind it, on both populations, under S1 and S2 (except NP at 0.01), on the probe and on the fixtures | Executed; development evidence | Competitive study, `results/results.json`; Table 4.19 |
| Every attack-labelled call to a restricted tool is stopped by the guard (907 and 559) | Executed; development evidence | same, `restricted_call_stages` |
| The gain of L4 over G3 belongs to the guard, not to the model | Executed (GV = L4 = HV on every episode) | same |
| A learner cannot help | **Not claimed**; the recordings contain no attack that passes the guard | Section 4.5.3; threat 18 |
| GV is better than, equivalent to or non-inferior to the published policy | **Not claimed**; +2.48 [−2.52, 8.69] and +3.83 [−7.92, 17.23] points of completed tasks | Table 4.14 |
| The Progent policy that was run is a configuration of the current paper | **Not claimed; stated to be false**: it is from a repository commit of September 2025 and was removed before version 3 | repository commits `9befb41`, `8a8eb89` |
| Progent's monotonic confinement constrains the policy, not intent; the released narrowing check had a gap until 15 November 2026 | Paper read in full; code read, not executed | paper Sections 6 and 9; commit `0d7ea07` |
| The Neyman-Pearson and conformal thresholds carry their guarantees here | **Not claimed**; assumptions not met; the conformal threshold exceeded its level in 7 of 9 held-out objectives | Section 4.5.3 |
| Cedar improves security or utility | **Not claimed**; decision parity on 7,098 calls | Section 4.5.3 |
| REM implements FIDES | **Not claimed**; value matching is provenance tracking, not information-flow control | Section 4.5.3 |
| Full texts of the method papers were read | **Not claimed**; each reference entry says so | references |
| The integration study prepared by another assistant reproduces | Executed: 123,776 replays with identical outcomes | Section 4.1.3 |
