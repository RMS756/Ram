# Supervisor decision memo: final REM specification, research gap and thesis claims

**To:** Prof. Omar Ahmad Alzubi (Supervisor), Dr. Husam Fakhouri (Co-Supervisor)
**From:** Rawan Al-Lahham
**Date:** 11 November 2026
**Deadline:** thesis submission 20 November 2026; decisions needed by **15 November**

**Draft prepared with AI assistance (Claude Code) for the candidate to check and edit before sending.** It supersedes the memo of the same date in `REM_Authorization_Generalization_Study/09`, which was written before the confirmatory experiment.

Everything below is offline recorded-trace replay on AgentDojo banking. No live agent was run. Nothing in the approved REM design or code has been changed.

## 1. Bottom line

1. **One modification to REM is now confirmed on untouched data: removing the behavioural evidence group.** On 2,113 recorded episodes that no earlier analysis had read, it completes more tasks than the original REM (1,074 against 916; +7.5 points, 95% interval [1.2, 16.0]) with fewer successful attacks (1 against 3 of 2,065). The test and its pass rule were committed before the data were opened.
2. **REM is still not better than simple rules.** A one-line strict rule ("withhold a state-changing call unless its recipient or credential appears in the user's request") completes 1,232 tasks with 4 attacks. The difference from the amended REM is not statistically resolved in either direction.
3. **The authorization-aware candidate remains rejected** (132 attacks against 11 on the primary data).
4. **No method tested can tell an authorized payment from an unrequested one whose details appear in the user's words.** This is a limit of the available information, not of the model.

## 2. Decisions requested

| # | Decision | Recommendation | If not decided by 15 November |
|---|---|---|---|
| S1 | **SD-FEAT.** Adopt "REM without behavioural evidence" as the final feature set (REM v1.1)? | **Yes**, as a declared, versioned amendment. Original REM (v1.0) stays in every table as the frozen baseline. | The thesis states v1.0 as the design and reports v1.1 as a confirmed ablation. |
| S2 | Research gap wording (`REM_FINAL_RESEARCH_GAP.md`, Section 3) | Adopt. It is an evidence gap, answered with largely negative results. | Used as proposed wording, marked pending. |
| S3 | Rule baselines P1, P2, A2 as mandatory comparators in Chapter 4 | **Yes.** The thesis is not defensible without them. | Included, marked as added after the pilot. |
| S4 | Thesis title: keep "Security Framework" without "behaviour-aware" wording | Keep the present title; remove "behaviour-aware" from the abstract and contributions if S1 is approved. | Title unchanged. |
| S5 | Research questions RQ1–RQ4 (still marked proposed) | Approve as evaluation questions. | Remain marked proposed. |
| S6 | Declared costs, tiers and predicates (D-9) | Approve as declared exploratory values; no claim that they are calibrated to a bank's risk appetite. | Remain marked exploratory. |
| S7 | Mitigation semantics (SC-1): step-level as reference | Confirm. | Step-level reference; episode-level reported as a separate policy. |
| S8 | Recorded-trace replay as the evaluation mode (SC-7 / D-1) | Accept, with the limits stated in every results section. | Same, marked pending. |
| S9 | Label rule and the `user_task_15` collision (D-6); no human label audit | Keep the rule; report the collision; state that no human audit exists. | Same. |
| S10 | Live or published-defence comparison (MELON pilot: needs a credential and a spending cap) | Not before submission. State plainly that no equal-terms comparison with any published defence exists. | Same. |
| S11 | University thesis template and formatting guide | **Needed from the university or supervisor.** The repository has none; the current layout is an assumed A4 thesis style. | Formatting cannot be certified. |
| S12 | Full texts of NEXUS, aiAuthZ and Kairos | Needed to upgrade three related-work entries from abstract level. | These three are described at abstract level and labelled so. |

SC-2 (tie-breaking; 0 ties occurred in any run), SC-3 to SC-6 and the remaining register items are unchanged and stay listed in the thesis decision register.

## 3. Evidence for S1 in one table

| | Original REM | REM without behavioural evidence | Provenance rule P2 | Strict rule A2 | No defence |
|---|---|---|---|---|---|
| Primary data: attacks / 2,979 | 11 | 11 | 12 | 13 | 672 |
| Primary data: benign tasks / 334 | 105 | 140 | 134 | 140 | 175 |
| Unseen task and objective: attacks; benign | 11; 105 | 14; 140 | 12; 134 | 13; 140 | — |
| **Untouched data: attacks / 2,065** | 3 | **1** | 4 | 4 | 436 |
| **Untouched data: all tasks / 2,113** | 916 | **1,074** | 1,043 | 1,232 | 1,451 |
| Untouched data: authorized calls released / 51 | 4 | 11 | 12 | 27 | 51 |
| Reformatted account number: attacks unchanged? | yes | yes | yes | yes | — |

## 4. What the thesis can and cannot claim

Can claim:
- a complete, tested, reproducible implementation of the five-layer REM design;
- a controlled evaluation against threshold and rule baselines under held-out attack objectives and held-out user tasks, with one pre-registered confirmatory run;
- that REM reduces attack success from about 21–23% to under 0.5% in replay, at a large cost in completed tasks;
- that removing behavioural evidence reduces that cost without a measured security loss;
- four documented negative results (behavioural evidence; outcome-supervised intervention value; delegated-source rule; exact-string provenance under reformatting);
- the identification of missing trusted authorization as the limiting factor.

Cannot claim:
- a novel algorithm (NEXUS and CASEL publish the same structure);
- that REM outperforms simple rules, or any published defence;
- anything about live agents, human reviewers, adaptive attackers or other domains;
- that the four verdicts differ in effect (they do not, in this evaluation);
- that authorization can be established from text.

## 5. Risks to submission on 20 November

| Risk | Status |
|---|---|
| No recorded supervisor decision on any register item | Open; this memo requests them |
| University template absent | Open (S11) |
| Three related works known only at abstract level | Open (S12) |
| No live experiment | Accepted limitation; stated throughout |
| All results exploratory by label | Depends on S6 |

## 6. Evidence

`REM_FINAL_SUBMISSION/research/` (protocol, decision, results register, analysis); `REM_FINAL_SUBMISSION/results/confirmatory_results.json`; protocol commit `19bd168`, results commit `907e6d2`.
