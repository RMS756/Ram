# 11 Thesis-ready results (draft text; to be reviewed by the supervisors before use)

The text keeps three kinds of statement apart:
- **[CONFIRMED]**: reproduced from stored outputs;
- **[EXPLORATORY]**: development evidence under a frozen protocol, not independent validation;
- **[FUTURE WORK]**.

Nothing here changes the approved REM design or its contribution claims.

---

**[CONFIRMED] Reproducibility.**
- The frozen scripted closed-loop experiment of the previous study was re-executed from its hash-verified script and reproduced exactly (960 of 960 episodes).
- All frozen comparison arms reproduced their stored offline-replay outcomes episode by episode (B0, PG, GV_math2, C1, C2PG: 8,106 episodes each; C3PG: 11,419).

**[CONFIRMED] Correction of earlier statements.**
- The two benign reference solutions previously reported as failing AgentDojo's evaluator under no defence fail only because the scripted test double did not return the task's final answer. With the answer returned, all 16 complete.
- The previously reported advantage of the contract guard over the v2 verifier on ut15×it4 depends on the order in which the obedient test agent issues its calls. With the injected call placed after the user's first read, both guards release the injected redirect of a recurring payment.

**[EXPLORATORY] Sources of over-blocking.**
- A call-level audit of the 934 restricted calls that the contract guard withholds without an attack label found 463 whose values equal those the user's request determines.
- Of these, 210 require natural-language semantics that the guard does not implement. 167 depend on a subjective condition that needs a reviewer. 46 take their values from files that the benchmark uses as injection vectors.
- Only about 40 could be recovered without widening the user's authorised scope or trusting an untrusted channel.

**[EXPLORATORY] A narrow evidence-resolution extension.**
- Two rules were pre-registered before implementation:
  - E1: an explicit percentage of a past payment, plus a fee;
  - E2: a refund recipient taken from the unique trusted record with the stated amount.
- In the offline replay they recovered 36 tasks in the primary population (all tasks completed 43.4% → 44.5%) and 166 in a second population (58.1% → 65.9%).
- No security measure worsened in any population or suite: attacks reached, attack-labelled calls released, diagnostics, fixtures, generalisation cases, and the scripted loop in three call orders.
- All gains lie in the two user tasks from which the rules were designed. The pre-registered grouped-bootstrap criterion was therefore not met (difference +1.09 points, 95% interval [0.00, 2.73]), and the result is reported as **inconclusive**.

**[EXPLORATORY] The learned decision.**
- On the deterministic guard, the stored ridge/Platt estimator with the two-verdict expected-loss decision changed no verdict: 0 of 710 calls reaching it in the primary population, 0 of 617 in the second.
- No attack-labelled call reached it: the deterministic authority front had already withheld all 907.
- Its scores were well calibrated on all restricted calls (Brier 0.059, ECE 0.024, 10 bins). The learned-stage scores, however, never reached the decision rule's switch points (0.048–0.167). As a result, a consequence-aware and a consequence-independent threshold could not be distinguished on these data.
- Combined with the evidence-resolution extension, the learned stage withheld 22 and 79 legitimate refunds and removed no attack.
- The learned component therefore showed **no measurable decision value** in this setting.

**[EXPLORATORY] Comparison with Progent's manual policy.**
- Progent's hand-written banking policy was executed in the official engine (pinned commit) on all 2,551 recorded restricted calls. It agreed with the replay comparator in every case.
- On AgentDojo it completed more benign tasks than the contract guard (154 vs 138 of 334), with no attack success. It was the only arm that stopped the recurring-payment redirect in every call order.
- It refused all legitimate requests involving accounts outside its static list.
- The complete Progent system, with language-model-generated policies, was **not** evaluated.

**[FUTURE WORK]**
- A live language-model closed loop (no endpoint was available).
- The complete Progent system under matched conditions.
- Independently written requests to confirm E1/E2.
- Binding modification instructions to the objects they name.
- Placing any learned stage where deterministic authorisation leaves genuine uncertainty.
