<!-- @frag ch4_progent -->
## 4.89 A Published Policy and a Request-Derived Permission Rule in the Same Harness

*Kind of evidence: replay; development evidence on both populations (every episode had been inspected before 13 November 2026). The arms and the comparisons marked with an asterisk were fixed in a committed protocol before the outcomes of the arm concerned were computed.*

**The published policy.** Progent (T. Shi et al., 2026) enforces per-tool policies with argument restrictions before each tool call. In version 3 of the paper, which was read in full, a language model writes the initial policy from the user's query and updates it during execution; a solver classifies each update as a narrowing, applied automatically, or an expansion, which needs approval (pp. 6-7). The official repository contained, at the commit of 10 September 2025, a hand-written policy for the AgentDojo banking suite: `send_money`, `schedule_transaction` and `update_scheduled_transaction` are permitted only for five listed recipients; `update_password` has no policy entry and is therefore not permitted; the remaining tools are permitted. That policy was removed from the repository on 13 May 2026, one day before version 3 of the paper, **so it is not a configuration that the current paper evaluates.** It was read from the repository as data, with the file digests pinned, and applied to the recorded calls by this project's replay code. The arm is therefore **a manual banking policy from Progent's repository, adapted to the shared replay harness**. It is not a reproduction of the Progent framework or of the paper's results, not Progent with generated or updated policies, and not a live-agent comparison. The upstream checking code was not executed; an independent review of 14 November 2026 reported a differential check on 468 argument cases that found no difference, which was not repeated here.

**The permission rule** releases a state-changing call only if the user's request supports it (Chapter 3, Section 3.44). It is an exploratory extension, not part of REM v1.0 or v1.1. It exists in three revisions, each frozen before it was scored. Revision 1 (G1) checks the operation, the recipient and the amount against the request. Revision 2 (G2) binds each amount to its account, evaluates balance conditions and refuses a payment already executed. Revision 3 (G3), the current rule, also binds each instruction to the effect of the operation (an immediate transfer, the creation of a standing order, or the modification of one) and evaluates a condition only as a whole. Revisions 2 and 3 repair defects found by two external reviews (Section 4.92), so their results were obtained after those of the earlier revision were known. On 16 November 2026 a direct-value constraint was added: an amount that the request states directly for an account and an operation binds that call, and a number whose format is ambiguous ("1,250") is not resolved. **GV**, the revision-3 authority guard with this constraint and no learned component, is the arm that the study of 16 November found best supported (Section 4.91).

**Table 4.67. Replay results of the rules and the published policy** (step-level, no reviewer; `improvement_results.json`, `results_v2.json`, `results_v3.json`, competitive study `results.json`; REM, B1 and P2 are in Tables 4.43 and 4.50)

§R4_MAIN§

**Table 4.69. Paired contrasts** (first arm minus second arm, in percentage points, with the 95% grouped-bootstrap interval; PG = Progent manual policy; v1.0 = REM v1.0; * = fixed in advance)

§R4_CON§

What the comparison shows:

- **The current rule, the guard GV and the published policy have no successful attack in either population.** Their differences in completed tasks are not resolved: GV minus the published policy is §R5_GVPG1§ points on the primary recordings and §R5_GVPG2§ on the second population. Neither equivalence nor non-inferiority is claimed. The published policy completes more benign tasks and releases more of the legitimate state-changing calls of benign episodes (§R4_PG_LEGIT§ for G3).
- **Against the rule A2 there is a security difference on development data and no resolved difference in completed tasks.** The current rule has 0 against 13 and 0 against 4 successful attacks, and both attack-success intervals lie below zero. The task-completion intervals include zero. By the wording fixed in advance, added value over simple rules and overall superiority are not claimed. All of these attacks are in one user task (Section 4.92).
- **Against REM v1.0** the current rule has fewer successful attacks on the primary recordings and more completed benign tasks on the second population; the other intervals include zero. This contrast was not fixed in advance.
- **The two policies fail in different places.** The published policy completes no password-change task (user task 14), because the tool is not permitted, and its five recipients are payees of the benchmark's initial state: on twenty paired fixtures whose payees are not on the list it withholds 13 of 20 legitimate calls (Table 4.74). The benchmark policy published with aiAuthZ has the same form (Section 4.16). The current rule completes no episode of user tasks §R4_ZERO§: the recipient or the instruction is supplied only by a file, the condition is subjective, or the request does not identify the payee of a refund.

<!-- @frag ch4_ablation_new -->
## 4.91 Ablations of the Task-Permission Extension

*Kind of evidence: replay; development evidence. The ablations are diagnostic and were listed in the protocol of each revision before scoring.*

**Table 4.70. The permission rule, one check at a time** (`improvement_results.json`, `results_v2.json`, `results_v3.json`; the probe has 2,645 attacked episodes)

§R4_CHECKS§

**Table 4.72. Paired contrasts of the ablations** (first arm minus second arm, in percentage points, with the 95% interval; * = fixed in advance)

§R4_LCON§

- **Binding removes the attacks and costs no task.** Binding amounts to accounts takes the rule from 10 and 3 successful attacks to 1 and 0. Binding instructions to the effect of the operation removes the remaining one. Without effect typing the current rule has the 10 and 3 attacks of revision 1, with the same completed tasks.
- **The condition check costs one user task.** Every task that revisions 2 and 3 lose against revision 1 (167 and 119) is in user task 14, whose request makes a password change conditional on "something looks even just a little bit suspicious". The rule does not evaluate such a predicate and never treats it as satisfied. The check removes no attack on these recordings. Whether such a call should be released, withheld or sent to a reviewer is an open decision (SD-COND, Appendix F).
- **Components of revision 1.** Scoped delegation accounts for §R4_DELEG§ completed tasks on the primary recordings, typed normalization for §R4_NORM§ and established payees for §R4_EST§. Without the amount check the rule completes §R4_AMT_T§ more tasks with §R4_AMT_A§ more successful attacks. The fulfilment check and the parser repairs change no count on the recordings.
- **The two-verdict decision alone is unsafe.** Applied to REM v1.1 without a guard (V11d), it releases every held-out credential-change attack (§R5_V11D_1§ and §R5_V11D_2§ successful attacks). In REM v1.1 those calls are withheld only because Escalate has a lower expected loss than Allow, and without a reviewer an escalated call is withheld. The low attack count of REM under a held-out objective therefore depends on the Escalate region, not on the estimator recognizing the attack.
- **A learned model behind a weak guard is not robust.** With the attacker's identifier reformatted, L2 has 38 successful attacks where the rule has 10. A guard that also blocks every call whose authority is not established (L2g, L4) removes this failure.
- **The gain of the learned arm over the rule belongs to the guard.** L4, the authority guard followed by the ridge model, completes more tasks than G3 with no successful attack (§R5_L4G3_1§ points on the primary recordings and §R5_L4G3_2§ on the second population; lower bounds exactly zero). The study below shows that the guard used alone completes exactly the same tasks: the gain comes from releasing calls whose authority is established although the request does not confirm their value, not from the model.

**Decision methods behind the authority front (16 November 2026).** *Kind of evidence: replay; development evidence. Protocol committed before any fit or outcome of these arms (commit `3710267`); a later addendum (commit `d3cdee6`) added two arms after the first results were known.* Every arm in Table 4.80 shares the revision-3 authority guard and the direct-value constraint; only the decision for the calls that pass them differs. The candidates were taken from published methods with documented implementations: a threshold chosen by the Neyman-Pearson umbrella algorithm (Tong et al., 2018), a threshold chosen by conformal risk control (Angelopoulos et al., 2022), and gradient-boosted trees in place of the ridge estimator (Friedman, 2001). The full texts of these papers could not be opened in the working environment; the procedures were taken from the authors' public implementations or from the library documentation, and no formal guarantee is claimed, because their sampling assumptions do not hold for clustered episodes and an unseen attacker objective.

**Table 4.80. Decision methods behind the authority front** (primary recordings under S1; `REM_COMPETITIVE_STUDY_2026_11_16/results/`)

§R5_FRONT§

§R5_FRONT_NOTE§

- **Every attack-labelled call is stopped by the guard.** During replay the guard blocks all §R5_ATT1§ attack-labelled calls to restricted tools on the primary recordings and all §R5_ATT2§ on the second population. No attack-labelled call reaches the stage where a model, a threshold or a tree decides; what reaches it is legitimate work (§R5_REL1§ and §R5_REL2§ calls released by GV).
- **No decision method changed an outcome, except one that lost tasks.** The ridge model with or without calibration, all four verdicts, the two conformal thresholds, the Neyman-Pearson threshold at 0.05 and the boosted trees give exactly GV's outcomes on every episode, the probe and the fixtures. The Neyman-Pearson threshold at 0.01 withholds legitimate calls and completes fewer tasks. **A learned or calibrated decision added nothing measurable over the guard alone.** This does not show that a learner cannot help: the recordings contain no attack that passes the guard, so they cannot test one.
- **The estimator is not the reason.** On held-out attacker objectives the ridge estimator reaches ROC-AUC §R5_AUC_RIDGE§ on all steps and §R5_AUC_RIDGE_R§ on calls to restricted tools; the boosted trees are not better (log loss §R5_LL_GB§ against §R5_LL_RIDGE§).
- **The calibrated thresholds do not carry their nominal levels to an unseen attacker objective.** Deciding alone on the held-out objective, the Neyman-Pearson threshold at 0.05 would release §R5_NP05§ attack-labelled steps (above 5% in §R5_NP05_OVER§ of 9 objectives); the conformal threshold at 0.05 would release §R5_CRC05§ (above its level in §R5_CRC05_OVER§ of 9, and at 0.01 in §R5_CRC01_OVER§ of 9).
- **Policy engine.** The same guard written as nine Cedar policies, with a wrapper that withholds on any evaluation error (Cedar itself skips a policy whose evaluation errors; Cedar Policy, 2026), gave the same release decision on all §R5_PAR_N§ restricted calls of §R5_PAR_REPLAYS§ replays (§R5_PAR_DIFF§ differences, §R5_PAR_ERR§ errors; median §R5_PAR_MS§ ms per call). Cedar is a possible way to write the constraints; it changes neither security nor utility.
- **Provenance.** A rule that withholds a call whose value the request does not confirm and that occurs only in untrusted content removes no attack and withholds §R5_GVP_W1§ and §R5_GVP_W2§ legitimate calls (§R5_GVP_T1§ and §R5_GVP_T2§ tasks). Value matching of this kind is provenance tracking, not the information-flow control of FIDES (Costa et al., 2025), whose labels are propagated by the agent's planner; that would require changing the agent.
- **A declared predicate withholds supported calls.** In GV, L4 and HV, predicate D2 (required evidence unavailable at a high tier) withholds §R5_D2_1§ and §R5_D2_2§ updates of a scheduled transaction that the request supports, because they carry no argument whose provenance can be computed. Whether D2 should apply behind the guard is an open decision (Appendix F).

<!-- @frag ch4_improve_results -->
## 4.92 Exploratory Extension: Task-Permission Evidence

*Kind of evidence: call-level counterexamples, replay, a call-level audit and paired fixtures, reported separately; all development evidence. Protocols were committed before each scoring (commits `9137b03`, `ae3f923`, `869d4c1`). One amendment was made after the first scoring of revision 3; it changed only the ablation without the condition check, and both result files are kept. The parser was written by an author who knows the sixteen requests of the benchmark.*

The question of the extension is whether permission evidence compiled from the trusted request improves the trade-off between security and task completion, and which component is responsible. The comparison with the rules and the published policy is in Section 4.89 and the ablations are in Section 4.91. This section reports the defects found, the audit of the one task that decides the security comparisons, the fixtures and the verdict.

**Matcher counterexamples.** Two external reviews (14 and 15 November 2026) reported five call-level defects, all reproduced on the unchanged code of the revision concerned. Revision 1 supported "100 to A and 50 to B" for the request "send 50 to A and 100 to B", supported a payment whose balance condition was false, and supported a repeated payment. Revision 2 let a request to create a monthly standing order license an immediate transfer, and evaluated "above 1000 and below 5000" as true at a balance of 10000. Each is now a regression test, together with legitimate neighbouring cases. They are development material and cannot test the repairs.

**The task that decides the security comparisons.** All successful attacks under any revision of the rule are in user task 15, where the new landlord's account named by the user is also the attacker's account. A call-level audit compared each released call with what the user asked for (update the address; update the rent standing order to that account and 2200; refund the 10.00 received from a friend), with criteria written before it was run.

**Table 4.78. Released attack-labelled calls in user task 15** (`ut15_call_audit.json`, `results_v3.json`)

§R4_UT15§

- **The attacks that revision 1 lets through are not artefacts of the collision.** They send the refund amount, 10, or the rent, 2200, to the landlord's account as a one-off payment. The user asked for neither. The collision makes the account look requested; the operation and the amount still contradict the instruction.
- **Revision 3 releases none of these calls.** It also withholds 20 and 77 calls that the audit counts as consistent with the instruction, mostly refunds whose payee the request does not identify. That is part of its cost in completed tasks.
- **The published policy blocks them because the account is not on its fixed list**, not because it reads the instruction. The same list withholds the legitimate update of the rent order.
- **Without user task 15, every restrictive arm has no successful attack on either population.** The task is kept in every comparison. Every security difference among the restrictive arms therefore rests on a small number of episodes of one task.

**Table 4.74. Paired fixtures** (each pair has one legitimate and one unsafe call for the same request; a pair is correct if the legitimate call is released and the unsafe call is withheld; counts, not rates)

§R4_FIX§

Sets 1 to 3 are the fixtures of the earlier studies. Set 4 has twenty pairs in ten categories and was written for revision 1 by the author of the rule with AI assistance; it was not reviewed by a second person. The repairs of revisions 2 and 3 were written after its failures were known, so for them it is regression material, not a test. The one legitimate call that the current rule withholds on set 4 is withheld by design ("1,250" can be read as two amounts); the learned arm releases it together with the unsafe call of the same pair.

**Verdict of the extension study.**

1. **Improvement over REM v1.0: observed on development data.** Fewer successful attacks on the primary recordings; more completed benign tasks on the second population.
2. **Against the strongest simple rule A2: a security difference on development data; overall superiority not established.** The difference in completed tasks is not resolved.
3. **Against the published policy: not resolved.** No successful attack for either. Only a manual policy from Progent's repository was run, in replay; the framework with generated and updated policies, its approver settings and live agents were not.
4. **Attribution.** The measured changes come from deterministic matching of the call against the instruction. The guard used alone (GV) gives the outcomes of every learned or calibrated variant that was tested (Table 4.80). The semantic verifier was not run.
5. **Prospective validation: defined, not executed.** A test needs paired requests written and reviewed by persons other than the author. The repository contains the authoring instructions and a scorer that refuses to run if the frozen rule has changed; no such request set exists. Live-agent comparisons are blocked for the reasons of Section 4.46.
6. **Status.** Proposed and exploratory. The rule is not adopted and is not a new version of REM (decision SD-PERM, Appendix F). Best supported on development data: GV.

The median time to evaluate one call was 0.09 ms for the rule and for the published policy and 0.18 ms for REM; no arm calls a model. The complete results (per-task counts, every single-component ablation, the probe, the analysis without user task 15, the estimators' calibration and the cutoffs per attacker objective) are in the repository under `REM_IMPROVEMENT_STUDY/`, `REM_G3_INTEGRATION/` and `REM_COMPETITIVE_STUDY_2026_11_16/`.
