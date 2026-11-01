# Novelty and Contribution Assessment

**Basis:**
- Ch. 1 §1.8 and §1.11;
- Ch. 2 §2.9, §2.13 (Tables 2.5, 2.9, 2.11) and the §2.13.6 currency update;
- Ch. 3 §3.13 (Table 3.16);
- Ch. 6 §6.3;
- the evaluator's diagnostic (Experimental Results Audit §3).

**Limits of the assessment.** The prior work is assessed at the level the thesis reached: abstract or record, plus level R for NEXUS. No full text of any prior work was read by the thesis or by the evaluator. Any novelty judgement is therefore provisional.

## 1. The ten novelty questions

| # | Question | Answer | Evidence |
|---|---|---|---|
| 1 | What exactly is new? | No mechanism. What is new is the **composition** for financial tool calls: argument-provenance and behavioural evidence → ridge LR → logit calibration → four verdicts by expected loss indexed by consequence tier → deterministic mitigation and audit record. Also new are an **evaluation design** (a same-estimator, consequence-independent baseline B1, and a variant with the same escalation opportunity) and an **exploratory characterisation** on recorded AgentDojo banking traces | Ch. 1 §1.8 ("None of these elements is new"); Ch. 3 Table 3.16 |
| 2 | What is adapted? | Elkan's cost-sensitive rule, extended to four actions with losses indexed by tier; Chow's reject option as conceptual support for Escalate; Platt calibration of a logistic model's logit; linear SHAP as an audit field; Bernoulli CUSUM, observe-only | Ch. 3 §3.7, §3.9, §3.10 |
| 3 | What is integrated? | All of the above. The integration is coherent: thresholds are derived from costs, and the feasibility of Escalate is explicit | Ch. 3 Eqs. 3.8–3.10 |
| 4 | What is only applied? | Ridge LR, Platt scaling, ECE, grouped bootstrap, CUSUM | — |
| 5 | Closest prior work? | **NEXUS** (Hossain et al., 2026): a cascade policy with a calibrated scorer and loss-weighted thresholds; Platt on a calibration split. **AgentTrust** (C. Yang, 2026): runtime interception of tool use. **PROVISO** (Yan et al.) and **TapGuard** (Xin): provenance and information-flow gating. **ProvenanceGuard** (She et al., ASE 2026): provenance analysis of misaligned actions. **Kekatos et al. (2026)**: offline monitors on recorded AgentDojo trajectories. **Chen (2026)**: actuarial, cost-based control of agent actions. **Zhang et al. (2026)**: "calibration is not control". Published defences on AgentDojo, including Banking: Progent, Task Shield, CaMeL, MELON, RTBAS | Ch. 2 §2.9.2–2.9.3, §2.13.6 |
| 6 | Measurable difference from the closest work? | Against NEXUS: tier-indexed losses and four verdicts, rather than threshold selection on a safety–utility grid. This is a design difference, **not measured**: NEXUS was not run. Against provenance gating (PROVISO, TapGuard, ProvenanceGuard): REM turns provenance into a calibrated probability and a cost-based verdict. **The evaluator's diagnostic suggests that, in this benchmark, the provenance indicator alone does as well or better** (§3 below) | Ch. 2 Table 2.9; diagnostic |
| 7 | Does the comparison against baselines favour REM? | Only against B1, and only in ASR under replay (0.004 vs 0.055). REM loses on benign utility (0.314 vs 0.509 without a reviewer). It was not compared with B2, with a provenance rule, or with any published defence under controlled conditions | Ch. 5 Tables 5.7–5.10 |
| 8 | Is there an algorithmic or mathematical contribution? | **No.** The derived results (indifference thresholds, Escalate feasibility, Modify dominance) are correct but elementary | Algorithm and Mathematical Audit §3 |
| 9 | Is there a methodological contribution? | **Modest.** Same-estimator baselines that isolate the decision layer, and explicit reporting of step-level vs episode-level semantics. Both are useful evaluation practice. The thesis states them as contributions, appropriately scoped | Ch. 1 §1.11; Ch. 6 §6.3 |
| 10 | Is there an empirical contribution? | **Exploratory only.** It characterises the trade-off between tiered thresholds and a FPR-matched threshold on recorded traces under NO-ADAPT. The results include a useful *negative* finding: as configured, REM intervenes on 93% of legitimate transfers, and three of its layers (context, behaviour, calibration) add nothing | Ch. 5 §5.5, §5.7 |

## 2. Gap assessment

| Gap (Ch. 2 Table 2.11) | Thesis's own verdict | Examiner verdict |
|---|---|---|
| A: calibrated, cost-based multi-action decision for agent tool calls | Weak | **Weak.** NEXUS, Chen (2026), PROVISO and TapGuard occupy much of it |
| B | Rejected | Agree |
| C | Narrowed | Agree |
| D: no verified quantitative evaluation of a runtime defence on financial actions in an open executable benchmark | Retained | **Largely semantic.** Several defences report AgentDojo results, and AgentDojo contains Banking. What is missing is a finance-specific breakdown. Kekatos et al. evaluate offline on AgentDojo traces (M-5) |
| E: same-estimator comparison of consequence-aware vs consequence-independent decisions | Narrowed | **Plausible but narrow.** This is the most defensible gap. However, the comparison is confounded, because REM differs from B1 in both thresholds and escalation, and the variant with the same escalation opportunity only partly separates the two |

## 3. The decisive diagnostic

The evaluator applied the rule "intervene on a tier ≥ 2 call iff x_act1 = 1". It has no parameters, so no cross-fitting is needed, and it was applied observe-only to all 6,762 steps.

| Rule | Attack steps intervened | Legitimate steps intervened | Benign state-changing steps released |
|---|---:|---:|---:|
| x_act1 rule | 97.1% | 14.7% | 92/180 |
| REM | 97.3% | 22.7% | 33/180 |

**What this implies.** Unless the thesis shows a setting where REM's added machinery helps, the contribution reduces to a statement that argument provenance is the useful signal. That statement is already the premise of the provenance-gating literature.

**Ways the thesis could recover a contribution:**
- showing that REM's calibrated probability and tier-indexed costs give a better trade-off than the rule **when x_act1 is unreliable**: paraphrased or split destinations, adaptive attacks, or a different benchmark;
- or showing that, for a fixed provenance signal, cost indexing yields a better utility–ASR frontier across elicited costs.

## 4. Overall judgement

**Type of contribution:** integrative (compositional) and empirical-exploratory. It is not algorithmic or theoretical.

**Strength:** **weak to modest** at master's level. The design is coherent, the reporting is transparent, and the reproducibility engineering is careful. However:
- the gap is narrow;
- the closest competitors were not run;
- the evidence does not show that the integrated design beats its own simplest component.

**Is it defensible as a master's contribution?**
- **Yes, conditionally,** if it is reframed as an empirical study: "Does consequence-tiered expected-loss decision-making add value over provenance gating and FPR thresholds for financial tool calls? An exploratory analysis on AgentDojo". The provenance-rule baselines must also be added.
- **Not as currently framed**, as "A Security Framework for Financial AI Agents".

## 5. Claims to weaken or remove

| Current claim or framing | Location | Required change |
|---|---|---|
| Title: "A Security Framework for Financial AI Agents" | Title page | Narrow it to an exploratory decision-analysis study on AgentDojo banking traces |
| Gap D as an open research gap | Ch. 1 §1.4; Ch. 2 §2.13.2 | Restate it as "no finance-specific breakdown", or drop it |
| O3 "partly achieved" | Ch. 6 Table 6.2 | State it as **not achieved**: no controlled comparison with an existing approach |
| "Expected-loss Bayesian decision" | User framing; Ch. 3 | Write "plug-in Bayes decision rule with a calibrated frequentist estimate" |
| Modify as a distinct mitigation | Ch. 3 §3.10; Ch. 5 RQ3 | State that Modify is, in step-level replay, a withheld call with a different cost entry |
| A five-layer architecture as evaluated | Ch. 3 §3.2; Ch. 4 | State that Detection (no classifier) and Behavioural Analysis (no measured contribution) are present only in form |
| Any implied security improvement | Ch. 1 §1.11; Ch. 6 | Keep the existing "remains unestablished" wording, and add the provenance-rule finding |
