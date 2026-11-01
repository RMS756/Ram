# Thesis Defence: 30 Questions with Model Answers

These are the questions an examiner is likely to ask about the R4 thesis. The model answers are **honest**: they concede what the evidence does not support, rather than defending it.

Each answer cites the thesis location or the evaluation report that backs it. Where an answer needs work that has not yet been done, it says so.

---

### A. Problem, scope and contribution

**Q1. What exactly is your contribution, given that you say none of the elements is new?**

A composition of standard methods, plus an evaluation protocol and exploratory evidence. The composition is:
- argument-provenance evidence;
- a calibrated ridge estimator;
- consequence-tiered four-verdict expected loss;
- deterministic mitigation and an audit record.

The protocol isolates the decision layer, because REM and B1 share the estimator, the calibration and the predicates. The evidence comes from recorded AgentDojo banking traces. I do not claim a new learning, calibration or decision method (Ch. 1 §1.8; Ch. 6 §6.4).

*Concede:* the empirical part is exploratory. In this benchmark a one-feature provenance rule performs as well (see Q9).

**Q2. How is REM different from existing guardrails such as LlamaFirewall, Task Shield or CaMeL?**

These systems differ from REM in what they do:
- LlamaFirewall and PI detectors classify *content*.
- Task Shield checks whether an action aligns with the user's task, using an LLM.
- CaMeL enforces information flow *by construction*, through a privileged/quarantined split.

REM scores each *proposed tool call* with evidence available at the execution boundary. It then picks among four verdicts by expected loss indexed by consequence tier.

*Concede:* the difference is in design. It is not measured, because none of these systems was run under the same protocol (O3 is not achieved).

**Q3. Is the research problem significant if ASR is already near zero for several AgentDojo defences?**

The problem I address is the *cost-sensitive* choice of intervention for financial actions: when to allow, modify, escalate or block, given different stakes. Most defences report a single ASR–utility point. Whether tiered costs give a better trade-off is open.

*Concede:* my evidence does not show that they do. Under my exploratory costs, REM costs considerable utility.

**Q4. Your title says "a security framework for financial AI agents". Is that justified?**

Not fully. The evidence comes from:
- one benchmark suite (banking);
- one attack family;
- recorded traces from 21 backbones;
- replay under NO-ADAPT.

A more accurate title would describe an exploratory decision-analysis study on AgentDojo banking traces.

**Q5. Your objectives come from an approved proposal. Where is it, and did you meet O3?**

The proposal is not included in the submission package. It must be attached.

O3 (compare with existing security approaches) was **not achieved** in the controlled sense:
- B1 is an internal baseline that uses the same estimator;
- the distributed defences are recorded results for another backbone pool, and cannot be compared.

---

### B. Method and mathematics

**Q6. Why logistic regression rather than a neural network?**

Three reasons:
- I have eight mostly binary features and nine attacked groups. A low-variance model is appropriate.
- The logit is linear, so linear SHAP gives exact, auditable attributions.
- Ridge regression handles quasi-separation.

A neural model would add variance and opacity without a demonstrated need. Held-out AUC is already 0.938, and almost all of it comes from one action feature.

*Concede:* a richer model could matter with richer evidence, such as text from an injection classifier. That was not tested.

**Q7. Why Platt scaling, when logistic regression is already fitted by likelihood?**

As a safeguard. Ridge shrinkage and fold shift can miscalibrate probabilities, and the decision thresholds (1/2 down to 1/21) need calibrated probabilities. Platt calibration is a monotone two-parameter map: it preserves ranking, and it is cheap to refit.

*Concede:* in my data it brought **no measurable benefit*:
- ECE 0.044 with calibration, 0.042 without;
- γ₁ between 0.945 and 0.981;
- it did not fix fold 7 (ECE 0.189).

Its use is justified by design, not by evidence (Ch. 5 §5.4, §5.7).

**Q8. How reliable are your probabilities around the decision thresholds?**

Pooled ECE is 0.044. However:
- Reliability in the windows around each tier threshold (1/6, 1/11, 1/21) is **not reported separately**, although Ch. 3 §3.12.2 promised it.
- On the unseen credential-change category (fold 7), calibration failed (ECE 0.189).

The probabilities are therefore reliable only for attack types represented in fitting.

**Q9. Why use expected loss instead of a simple threshold, or a simple rule?**

Expected loss makes the threshold for each consequence tier follow from declared costs (p* = C_FA/(C_FA + C_miss)). It also makes Escalate's feasibility explicit (Eq. 3.10). This gives auditability and a principled link from stakes to action.

*Concede:* empirically:
- against a FPR threshold (B1), REM blocks more attacks in replay, but loses 19.5 points of benign utility without a reviewer;
- a parameter-free rule ("intervene on a state-changing call iff a key argument comes only from untrusted content") reaches 97.1% attack interception with 14.7% false intervention, against REM's 97.3% / 22.7%. This is the examiner's diagnostic, not a thesis result.

So, in this benchmark, I cannot show that the expected-loss layer adds value over provenance gating.

**Q10. Is the decision "Bayesian"?**

It is a plug-in Bayes decision rule: it minimises the posterior expected loss, with the posterior replaced by a calibrated frequentist estimate. There is no prior over parameters and no posterior predictive. "Bayesian" should be read only in the decision-theoretic sense.

**Q11. What happens when the classifier is confidently wrong?**

If p is low on an attack:
- the verdict is Allow;
- the attack proceeds, unless predicate D1 or D2 fires.

This is what happened to B1 on the 124 credential-change attacks. As far as I can tell, REM caught them because the tier-4 threshold is very low (1/21), not because the probability was well calibrated.

If p is high on a legitimate action, it is withheld. REM intervened on 93% of legitimate tier-3 transfers.

REM has no correction mechanism within an episode. CUSUM is observe-only and does not enter the verdict. The audit record allows errors to be reviewed after the fact.

**Q12. How were the costs chosen?**

They are **declared exploratory values** (Ch. 5 Table 5.1):
- C_FA = 1;
- C_miss = 1/5/10/20 by tier;
- C_mod = 0.5;
- C_esc = 0.3.

They were pre-registered before held-out results, as far as commit history shows. They were **not elicited** from domain experts and are **not approved** (D-9, SD-FREEZE). Every decision result is conditional on them. The E6 grid shows how sensitive the results are, but the grid points are also arbitrary.

**Q13. How do you estimate r_mod, and is it not circular?**

r_mod is estimated by replaying the oracle Modify under NO-ADAPT. Under NO-ADAPT a withheld call never recurs, and my declared Modify mechanism withholds the call. So r_mod ≈ 0 by construction. **Yes, it is circular.** The Modify verdict mix (Modify for 615 of 907 attack steps) therefore reflects an assumption, not a measurement.

**Q14. What does Modify actually do?**

Under step-level semantics: it withholds the call and returns a tool-restriction notice, with no persistence. In replay its effect on the environment equals a step-level Block. Modify and Block differ only in their cost entries.

A genuine Modify, such as substituting the argument from trusted context, is not implemented. It needs a supervisor decision.

**Q15. Step-level or episode-level mitigation: which is REM?**

Neither is adopted (D-2 / SC-1). Both are implemented and reported (Ch. 5 Table 5.11). The semantics change B1's ASR (0.055 → 0.046) and the utility under attack.

*Concede:* one sentence in Ch. 3 §3.11.11 still wrongly says that replay cannot distinguish them. It will be corrected.

---

### C. Evaluation and evidence

**Q16. What evidence shows that REM improves security?**

There is no direct evidence for live agents. What exists:
- under replay with NO-ADAPT, REM withheld more recorded attack calls than B1 (ΔASR −0.051 [−0.130, −0.007], step-level);
- held-out discrimination is strong (AUC 0.938).

The central practical claim, that REM reduces financial harm at acceptable utility cost, remains **unestablished** (Ch. 6 §6.4).

**Q17. Why not run live agents?**

There was no LLM access in the project environment (D-15). A protocol is ready in `experiments/live/`, but it has not been executed.

This is the single most important missing experiment.

**Q18. Are your episodes independent observations?**

No. There are:
- 16 user-task templates × 9 injection templates;
- one attacker account;
- 21 backbones, each with one run.

The intervals are percentile bootstraps over the 9 attacked groups. They are descriptive, and their coverage is uncertain. No significance test or multiplicity correction was applied.

**Q19. How do you know the labels are correct?**

I do not know it to an examination standard. Labels come from matching each call against the reference calls of the injection goal.

The user_task_15 collision affects 16 of 21 backbones, and all of REM's residual ASR comes from those episodes. The only inspection was by an AI assistant: 29 of 30 episodes agreed. A 145-item human audit package exists, with 0 annotations.

**Q20. Is your argument-provenance feature not an oracle in this benchmark?**

Very nearly, yes. In AgentDojo banking the attacker's IBAN appears only in injected content, and the label is defined on calls to the injection goal. So x_act1 and the label are structurally linked. This inflates discrimination and limits external validity.

Testing with paraphrased, split or encoded destinations, or with a second benchmark, is needed.

**Q21. Why did behavioural features hurt?**

x_beh3 (privilege escalation) fires on 92% of legitimate state-changing steps, because any first transfer is a privilege increase. x_beh4 fires on 43% of them, because held-out user tasks produce transitions that are unseen in the fitting portion. Removing behavioural evidence raised replay benign utility by 10.5 points (Ch. 5 Table 5.12).

As designed, the Behavioural Analysis layer contributes nothing in this benchmark.

**Q22. What did you compare against, and was the comparison fair?**

| Comparison | Fair? |
|---|---|
| B0 (no defence) | Yes |
| B1 (same estimator, FPR thresholds) | Fair as a decision-layer ablation, but confounded by escalation |
| REM without expected-loss Escalate | Partly controls the escalation confound |
| Distributed defences | Recorded for gpt-4o only; not comparable |

Missing: B2 (detection-only), a provenance rule, and any published defence under a shared protocol.

**Q23. How sensitive are the results to the costs?**

Strongly. The single-tier ablation spans:

| Single tier | Replay ASR | Benign utility |
|---|---|---|
| 1 | 0.051 | 0.440 |
| 4 | 0.003 | 0.314 |

The E6 grid shows that the REM-vs-B1 ordering depends on the costs. There is no cost-independent ranking.

**Q24. How does REM handle multi-action attacks?**

Each proposed call is scored with the episode's history:
- x_beh features use the history;
- x_act1 uses all untrusted content seen so far.

Under episode-level semantics, a Block restricts all state-changing tools for the rest of the episode.

Under replay, however, multi-step adaptation is not modelled. A live agent could split an attack across tools, or launder the attacker value through a trusted-looking channel. That was not tested.

**Q25. What is the latency overhead, and is it realistic?**

Median 0.21–0.28 ms per complete call; p95 0.49–0.70 ms; about 4.4 KB per step. This figure excludes an injection classifier, which would dominate in practice. The figure is realistic for the computation as implemented, but not for a full deployment.

**Q26. Did you pre-register the analysis?**

The design values were committed as declared exploratory values. Amendment AM-1, the exclusion of (user_task_15, injection_task_4), was committed before the held-out predictions (commit `7a707a7`).

*Concede:* the log of the first execution was not preserved. The order relative to the first results rests on commit times and the session record (Ch. 5 §5.2.3).

---

### D. Deployment, integrity and limitations

**Q27. Could REM be deployed in a real bank?**

Not as configured. Without a reviewer:
- it intervenes on 93% of legitimate transfers of 1,000 or less;
- state-changing benign utility falls from 0.47 to 0.17.

Deployment would need:
- elicited costs;
- a real Modify mechanism;
- an injection classifier;
- a review workflow;
- live validation.

**Q28. How much of this thesis was produced with AI assistance, and how was it verified?**

An AI coding assistant assisted with:
- literature screening records;
- the code and tests;
- running the analyses;
- the AI-only label inspection;
- drafting and verifying the text.

This is recorded in the front matter (line 46) and in the repository history.

Verification consisted of:
- 205 automated tests;
- scripted equation checks;
- reproduction of every result;
- cell-level tracing.

*Concede:* the formal declaration of AI use and a similarity check are still outstanding, and the student's own intellectual contribution must be made explicit.

**Q29. Have you read the sources you cite?**

The literature review is record-level: abstracts and metadata. No full text was read in the R3 or R4 sessions. Platt (2000), the source of the adopted calibrator, was never read. Several equation sources are coded IV or NC (Ch. 3 Table 3.17).

This must be remedied before final submission.

**Q30. What are the main limitations, and what would you do next?**

The main limitations are:
- no live runs;
- unaudited proxy labels;
- unapproved costs;
- one benchmark with a near-oracle provenance feature;
- one run per configuration;
- no controlled comparison with published defences;
- no simple-rule baseline;
- circular r_mod;
- record-level literature.

In order, next steps would be:
1. Add the provenance-rule and B2 baselines to the replay.
2. Complete the human label audit.
3. Have costs elicited or approved.
4. Run live enforcement with three or more repeats on one open-weight backbone.
5. Run a controlled comparison with one published defence.
6. Test robustness with adaptive or paraphrased destinations, or on a second benchmark.
