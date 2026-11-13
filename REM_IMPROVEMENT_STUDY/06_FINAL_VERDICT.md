# 6. Final verdict of the improvement study

**Date:** 13 November 2026. Every statement below rests on development evidence from recorded-trace replay. Nothing is confirmatory; nothing was run with a live agent or a language model.

## 6.1 Verdict in four parts

| Question | Verdict | Basis |
|---|---|---|
| **Improvement over REM v1.0?** | **Observed on development data.** The permission rule G1 completes more benign tasks than v1.0 in both populations (149 against 105 of 334, +13.17 points [1.50, 28.14]; 32 against 18 of 48, +29.17 [8.33, 52.08]) with 10 against 11 and 3 against 3 successful attacks. The all-task interval is above zero in the second population (+20.92 [1.30, 42.46]) and touches zero in the primary one (+11.65 [−0.39, 26.25]) | `05_RESULTS.md` §5.2–5.5. This contrast was not among those fixed in advance; it is descriptive |
| **Added value over strong simple rules?** | **Not established.** Against rule A2 the point estimates favour G1 on both outcomes in both populations (tasks +3.02 and +5.96 points; attacks 10 against 13 and 3 against 4), but both task-completion intervals include zero. By the rule fixed before the run, the claim is not made | Comparison 1 of the frozen protocol |
| **Comparison with a published defense?** | **Run for one: Progent's published manual banking policy** (official repository, commit `9befb41`), replayed in the same harness on the same episodes. It has **no successful attack** in either population (G1: 10 and 3; attack-success difference above zero in both), releases more legitimate calls in benign episodes, and completes a similar number of tasks (difference unresolved). It completes no password-change task and, on the author-written fixtures with payees outside its fixed list, withholds 13 of 20 legitimate calls. **G1 is not shown to be better than the published policy; on security it is worse on this benchmark.** | Comparison 2; fixture set 4 |
| **Untested claims** | Live-agent behaviour of any arm; MELON, Task Shield, CaMeL and Progent with generated policies; the selective verifier; any request not written by the author; reviewer workload and reviewer accuracy; a bank's risk tolerance; statistical superiority or non-inferiority on security (no margin is approved and none was invented) | `04_IMPLEMENTATION_AND_TESTS.md` §4.6; `protocol/PROSPECTIVE_PROTOCOL.md` |

## 6.2 Which component caused the change

| Component | Effect observed | Attribution |
|---|---|---|
| Request compiler and typed matcher used as a **hard rule** (G1) | Almost all of the gain over v1.0 and v1.1: more released legitimate calls (112 of 178 against 33 and 83) with no more successful attacks than v1.0 | **The gain is due to the deterministic permission rule** |
| Within the rule | Scoped delegation (+131 tasks, primary), typed normalization (+90), established payees (+18); the amount check removes three attacks and costs 68 tasks; the operation check changes one task | Ablation table T4 |
| **Learned ridge model** on the same evidence (L2, L2s against G1) | +3.2 and +2.1 points of tasks without more attacks on the original text; intervals include zero under both splits; 28 more successful attacks when the attacker identifier is reformatted (38 against 10) | **Not attributed to the learner.** No demonstrated value; a measured robustness cost |
| Two-verdict decision semantics (C) | Unsafe alone on v1.1 (131 attacks; all 119 held-out credential-change attacks released); usable only behind the permission guard | A consistency repair, not a source of security |
| Semantic verifier (D) | Not executed | No evidence |

## 6.3 Is the proposed contribution supported?

**No, not as an improvement of the learned REM core.** The research question asks whether a learned, consequence-aware runtime decision improves the security/utility trade-off over simple provenance and permission rules. On this benchmark and in replay:

- the best trade-offs observed come from deterministic rules: Progent's fixed allow-list (no successful attack) and the request-derived permission rule G1 (most tasks among the rule arms that keep attacks at or below REM's level);
- the learned model adds no demonstrated value to the permission evidence and is less robust to reformatting;
- the answer to the extended question is therefore: task-permission evidence compiled from the trusted request improves on REM v1.0 on development data, **and the improvement belongs to the compiler and the matcher, not to the learned core.**

What the thesis can state: a controlled, replay-based comparison in which REM, its proposed amendment, simple rules, one published policy and a request-derived permission rule are evaluated on the same episodes under held-out objectives, with the negative finding for the learned component reported. What it cannot state: that REM or the candidate outperforms a published defense, that the candidate generalizes beyond the benchmark requests, or that any of this holds with a live agent.

## 6.4 Recommendation for the supervisors (decision pending; nothing is adopted)

1. Keep REM v1.0 as the design of record and v1.1 as the pending amendment.
2. Report the permission rule as an exploratory, proposed extension and as a baseline that a learned monitor must beat, not as a new REM version.
3. If a model budget is approved, run the sealed prospective protocol (same version of the benchmark for all conditions; MELON and Progent included; request variants written by a second person).
4. Open decisions are unchanged (Appendix F of the thesis) with one addition: whether the permission rule is to be mentioned in the thesis as future work only, or with these development results (as drafted in Chapter 4, Sections 4.4 to 4.6).
