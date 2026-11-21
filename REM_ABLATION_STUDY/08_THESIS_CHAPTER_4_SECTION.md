# 08 Thesis-ready text for Chapter 4 (proposed; R8 is not overwritten)

*Proposed placement:* Chapter 4, after Section 4.5.5, as **4.5.7 Component Ablation across Three Populations (21 November 2026)**.

**What it extends.** It extends the final ablation of Section 4.5.5 with:
- a Detection-layer arm;
- a shadow-mitigation arm;
- call-level metrics with clustered intervals;
- two stricter populations.

**Table numbers.** New tables would take the next lettered numbers (4.21f–4.21h) under the numbering rule of R8.

---

### 4.5.7 Component Ablation across Three Populations (21 November 2026)

*Kind of evidence:* offline replay of recorded episodes (NO-ADAPT), under a protocol committed before any arm was scored. It is development evidence: every population had been read before.

**Design.**
- **Fitted state.** A fresh execution of the frozen pilot pipeline reproduced REM v1.0's published counts exactly. Its fitted state was byte-identical to the frozen state of 3 November 2026.
- **Arms.** Eight configurations were compared with the full framework (A0) on identical episodes and identical call positions. Each configuration changes one component.

| Arm | Component removed |
|---|---|
| A1a | the detection feature `x_ctx2` |
| A1b | the Detection layer: `x_ctx2`, and `x_beh1`, which is defined through it (refitted with the frozen procedure) |
| A2 | the behavioural evidence |
| AIC | the action and provenance evidence derived from the Input & Context layer |
| A3 | the learned decision (estimator, calibration and expected loss), leaving predicates D1 and D2 |
| A3P | the predicates, leaving the learned decision |
| A4 | enforcement: every verdict is computed and logged, and every call is released |

**Not ablated.**
- **The injection classifier** of the Detection layer: it is absent from the implementation.
- **Provenance labelling itself:** every action feature and predicate D2 depend on it.
- **Input hygiene:** none of the 16,727 tool outputs contains a character it removes, so ablating it cannot change any decision on these data.

**Populations.**
- **P1:** the primary population, 3,313 episodes (2,979 attacked, 334 benign).
- **P2:** 681 gpt-4o episodes with five attack templates never used in fitting.
- **P3:** 2,113 episodes from backbones and templates never used in fitting (2,065 attacked, 48 benign).

**Metrics.** They are measured at the level of calls to state-changing tools:
- the share of attack-labelled calls withheld;
- the share of calls in benign episodes withheld, which is the false-positive rate at call level.

Intervals come from a grouped bootstrap that resamples injection tasks or user tasks, never individual calls. A replay outcome of an episode is reported separately; it is not an attack success rate of a live agent.

**Table 4.21f. Attack-labelled calls withheld, and legitimate calls withheld in benign episodes** (`REM_ABLATION_STUDY/04_RESULTS.csv`)

| Arm | P1 attack calls | P2 attack calls | P3 attack calls | P1 benign-episode calls | P3 benign-episode calls |
|---|---|---|---|---|---|
| A0 full REM | 882 / 907 | 200 / 202 | 556 / 559 | 145 / 178 | 47 / 51 |
| A1a − detection feature | 882 / 907 | 200 / 202 | 556 / 559 | 145 / 178 | 47 / 51 |
| A1b − detection layer | 882 / 907 | 200 / 202 | 556 / 559 | 145 / 178 | 47 / 51 |
| A2 − behavioural | 882 / 907 | 200 / 202 | 558 / 559 | 95 / 178 | 40 / 51 |
| AIC − provenance evidence | 833 / 907 | 191 / 202 | 505 / 559 | 174 / 178 | 51 / 51 |
| A3 − learned decision | 0 / 907 | 0 / 202 | 0 / 559 | 6 / 178 | 1 / 51 |
| A3P − predicates | 882 / 907 | 200 / 202 | 556 / 559 | 145 / 178 | 47 / 51 |
| A4 shadow (released) | 0 / 907 (882 flagged) | 0 / 202 (200 flagged) | 0 / 559 (556 flagged) | 0 / 178 | 0 / 51 |

![Figure 4.x. Paired differences from the full framework in the share of attack-labelled calls withheld and in the share of legitimate calls withheld in benign episodes, on three populations, with 95% grouped-bootstrap intervals.](REM_ABLATION_STUDY/06_FIGURES/fig3_paired_differences_vs_A0.png){width=100%}

**Findings.**

1. **The learned decision is the component that withholds attack-induced calls.**
   - Without it, the predicates alone withhold no attack-labelled call in any population.
   - With it, 97.2%, 99.0% and 99.5% are withheld; the intervals of the differences exclude zero.
   - It also accounts for almost all false-positive blocking: 139 of the 145 legitimate calls withheld in P1's benign episodes, and 46 of 47 in P3.
   - Every release that it changes, it changes to a withholding.
   - Its cost in processing is about 0.08 ms per call (median 0.151 against 0.070 ms).
2. **The deterministic predicates add nothing measurable.** Removing them changes no attack-labelled or benign-episode call in any population.
3. **The Detection layer adds nothing measurable.** This holds for the instruction-pattern feature alone and for the layer including the behavioural feature derived from it: no attack-labelled or benign-episode call changes. The refitted model's held-out ROC-AUC is 0.937 against 0.938.
4. **Behavioural evidence has a measurable cost.**
   - Removing it lowers the blocking of legitimate calls on P1 by 28.1 points [8.6, 54.1].
   - Its effect on attack-call withholding is not resolved: two calls change in each direction on P1.
   - On P3 the cost is not resolved: −13.7 points [−37.5, 0.0].
5. **Provenance evidence is the only evidence group whose removal lowers attack-call withholding:**

   | Population | Change in attack-call withholding | Resolved? |
   |---|---|---|
   | P3 | −9.1 points [−23.5, −0.7] | yes |
   | P1 | −5.4 points [−17.0, 0.0] | no |
   | P2 | −4.5 points [−13.0, 0.4] | no |

   In point estimate, removing it also raises the blocking of legitimate calls (P1: +16.3 points [−1.9, 39.2]).
6. **Enforcement carries the effect.**
   - In shadow mode the framework flags the same calls (its verdicts agree with enforcement on 99.6–99.7% of calls), yet releases them.
   - The replay outcomes then equal those of no defence.

**Interpretation.**
- **What REM v1.0's protection is.** It is the learned, consequence-aware decision fed mainly by provenance evidence.
- **Redundant components in this evaluation:**
  - the instruction-pattern detection;
  - the deterministic predicates.
- **The component with a measurable utility cost:** the behavioural evidence. This is consistent with the confirmatory run of Section 4.6.8.
- **The trade-off.** The learned decision's protection comes with the blocking of most legitimate state-changing calls; withhold precision is 0.40, 0.34 and 0.25 on the three populations.

**Not established.**
- **Closed-loop effect.** These results cannot show how a live agent would respond to the withheld calls. No closed-loop ablation was possible without a model.
- **Generality.** They do not establish that the redundant components are useless in general. The injection classifier was never available, and the attacks of this benchmark place their payloads where provenance evidence sees them.
- **Architecture.** No change of the approved architecture is proposed on this basis. The evidence supports the proposed amendment already before the supervisors (REM v1.1, without behavioural evidence; decision SD-FEAT), and notes that the predicates and the pattern detector are not measurably active on these data.
