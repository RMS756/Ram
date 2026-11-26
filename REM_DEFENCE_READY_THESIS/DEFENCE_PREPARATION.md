# Defence preparation: REM defence-ready edition

These notes are for the student's preparation. Every number below is in the thesis and was recomputed from the stored per-episode records (`audit/`). Section numbers are those of the defence-ready edition.

## 1. The thesis in five sentences

1. REM is a five-layer runtime layer at the tool boundary of a financial agent. For each proposed call it estimates the probability of adversarial inducement (ridge logistic regression, Platt calibration on the logit), assigns a declared consequence tier, applies predicates, and chooses Allow, Modify, Escalate or Block by minimum expected loss.
2. On 3,313 recorded AgentDojo banking episodes (21 backbones), replayed without agent adaptation (NO-ADAPT):
   - REM reduces attack outcomes from 672 to 11 of 2,979;
   - benign task completion falls from 175 to 105 of 334;
   - only 33 of 178 legitimate state-changing calls are released.
3. The layer ablation shows that every outcome effect comes from the Decision Engine's learned decision acting through the Mitigation layer's enforcement:
   - in shadow mode the same verdicts protect nothing;
   - the action/provenance evidence carries the discrimination;
   - behavioral evidence lowers completion;
   - the Detection indicator, the predicates, calibration and Modify show no measurable effect.
4. Simple provenance rules, and Progent's published banking policy decided by Progent's own code, reach REM's security with more completed work on these episodes. The thesis reports that REM is not better than them.
5. Everything is offline replay on one benchmark with unapproved design values. The findings are bounded to that evidence.

## 2. Numbers to know

| Quantity | Value |
|---|---|
| Primary population | 3,313 episodes = 2,979 attacked + 334 benign; 21 backbones; attack `important_instructions`; AgentDojo 0.1.35, banking v1 |
| Held-out templates | 681 attacked episodes, 5 templates |
| Second population | 2,113 episodes = 2,065 attacked + 48 benign |
| No defense / REM v1.0, attack outcomes | 672 / 11 of 2,979 (22.6% [14.8, 29.5] / 0.4% [0.1, 0.7]) |
| No defense / REM v1.0, benign tasks | 175 / 105 of 334 |
| REM v1.0, legitimate state-changing calls released | 33 of 178 |
| Held-out ROC-AUC | 0.938 (0.799 without action/provenance evidence) |
| A4a, learned decision removed | +22.2 points attack outcome [14.6, 28.9]; 661 / 0 discordant; +22.5 points benign completion [8.0, 38.5] |
| A5, enforcement off (shadow mode) | Outcomes equal no defense; same verdict on 6,654 of 6,684 calls |
| A3a, behavioral evidence removed | Attacks unchanged (1 / 1); +10.5 points benign completion [1.2, 22.6]; 36 / 1 |
| A3b, action/provenance evidence removed | 17 against 11 attacks (p = 0.15, unresolved); attack call executed in 49 against 24 attacked episodes (29 / 4, p < 0.001) |
| A4d, thresholds instead of expected loss | 164 against 11 attacks (+5.1 points [0.7, 13.1]); +19.5 points benign completion |
| A2a, A2b, A4b, A4e | No attack outcome changed |
| Progent's policy (official checker), attacks | 0 on all three populations, against REM's 11, 2 and 3 |
| Progent's policy, tasks under attack vs REM | +7.2, +16.9 and +18.0 points |
| Progent's policy, benign tasks | 154 against REM's 105 of 334 (primary); 35 against 18 of 48 (second) |
| Runtime per call | REM median 0.15 ms; Progent check median 0.22 ms; neither calls a model |
| DRIFT, scripted | 160 episodes, 0 errors; about 9–10 model calls per episode with modules against 3.5 without; no security or utility result |
| Residual attacks of REM | All in `user_task_15`, whose landlord IBAN equals the attacker's in banking v1 |

## 3. Likely questions and evidence-based answers

**Q1. Why is the Input & Context layer not ablated?**
- It computes no evidence (Section 3.4). Its labels feed the action features, x_beh1 and predicate D2.
- Removing the labels would mean inventing substitute inputs, which is a design decision that is not frozen.
- Its route into the estimator is removed by A3b. That shows the provenance evidence carries the discrimination (ROC-AUC 0.938 → 0.799) and that more attack calls execute without it.
- Hygiene changed 0 of 16,727 tool outputs, so it cannot change any outcome here.

**Q2. Your Detection layer shows no effect. Is it useless?**
- No. The thesis reports "no measurable effect in this experiment".
- In AgentDojo, injected instructions arrive in untrusted tool output that the provenance features already mark.
- The layer's classifier (x_ctx1) was never implemented (D-8), so the layer was tested with one indicator only.
- A component is shown ineffective only when it is exercised and fails. It is shown unnecessary only beyond one benchmark (Section 4.5.10).

**Q3. If behavioral evidence hurts, why keep it?**
- The thesis proposes removing it as REM v1.1 (Section 3.13). That proposal passed a pre-registered confirmatory test: +7.5 points of task completion [1.2, 16.0] on unread data.
- Adopting it is a supervisor decision; the original specification stays the baseline.

**Q4. REM is beaten by Progent's policy. What is the contribution?**
- The thesis claims no superiority.
- Progent's list contains two recipients known only from task solutions and excludes the attacker's account, so it blocks every injection task by construction (Section 4.4.8).
- REM needs no list of legitimate values. Its cost is false blocking, which the ablation locates in the learned decision under the declared costs.
- The contributions are:
  - a specified, implemented and tested design;
  - a fair evaluation protocol;
  - the attribution of REM's effects to its components;
  - documented negative results.

**Q5. Why no live experiments with DRIFT or MELON?**
- Both put a language model in the decision path. No model credential or budget was authorised, and no model or repetition count was approved.
- The supervisors did not require live experiments.
- The official DRIFT code was run end to end with a scripted agent to establish compatibility and processing volume. No performance is claimed from it.

**Q6. Is replay valid?**
- Replay fidelity is reported (99.4% and 98.4%).
- NO-ADAPT means a withheld call does not lead the agent to retry. A live agent could reach the goal another way, so replay attack success is not an upper bound.
- The thesis states this in every results section and lists live evaluation as future work.

**Q7. Are the 3,313 episodes independent observations?**
- No. Intervals use a grouped bootstrap by injection task (9 clusters) and user task (16 clusters), and are described as descriptive.
- Paired comparisons use exact McNemar tests on the same episodes.
- Calls are not treated as independent samples.

**Q8. Why do Modify, Escalate and Block look identical?**
- Under step-level mitigation without a reviewer, all three withhold the current call. Removing Modify (A4e) changes no episode.
- Their difference needs a reviewer model (future work 6).

**Q9. Did you change REM to get better results?**
- No. REM v1.0 is frozen at `9fddfa7`.
- Every ablation arm is a configuration of the frozen harness, with protocols committed before scoring.
- Exploratory extensions (the permission rule, the typed verifier, the redesigns) are reported separately as not part of REM v1.0 (Section 4.5.8).

**Q10. Are the research questions approved?**
- No. They are derived from the approved objectives and labelled [PD] (Section 1.7). They await the supervisor's confirmation.

## 4. Statements to avoid

- That REM outperforms Progent, DRIFT, MELON or any published defense.
- That any result is live, deployed or real-world.
- That the Detection layer, the predicates, calibration or Modify are useless or unnecessary.
- That the 2,979 attacked episodes are independent samples.
- That the design values, RQs or REM v1.1 are approved.
- That DRIFT or MELON were evaluated for security or utility.

## 5. Suggested slide order (about 20 minutes)

1. Problem and threat model: indirect prompt injection against a financial agent.
2. REM's five layers and the decision rule (Figure 3.1).
3. Evaluation design: populations, replay, NO-ADAPT, pairing.
4. Main result: security against completed work.
5. Ablation by layer (Figure 4.5, Table 4.26).
6. Layer-to-implementation map and its couplings (Figure 4.4).
7. Comparison with existing frameworks (Table 4.12, Figure 4.2).
8. What does not work, and why it matters (Section 5.5).
9. Limitations and future work.
10. Conclusion.
