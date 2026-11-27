# 02: Corrected scientific position (for supervisor review)

**Status.**
- Proposed wording [PD].
- It supersedes `REM_INDEPENDENT_AUDIT_2026_11_27/08` and the corresponding parts of its file 00.
- Evidence and terms are as defined in `01_RECONCILIATION_OF_FINDINGS.md`.
- Every result below is a **NO-ADAPT replay** result unless stated. Replay results are not closed-loop agent performance.

## 1. Final research problem

**The setting.**
- A tool-using financial agent processes untrusted content in the same context as its user's instructions: transaction subjects, files, notices.
- Indirect prompt injection in that content can induce payments, payment changes or credential changes that the user did not request.
- Runtime defenses at the tool-call boundary are often organized as several layers: content inspection, behavioural analysis, action evidence, a risk-informed decision and enforcement.
- Such organization is commonly presented as defense in depth.

**The problem.** Layering is a design property; defense in depth is a property of protection. A layered defense has depth only if:
- more than one of its components contributes protection;
- the loss of one component is covered by another.

Whether a given layered boundary defense for a financial agent has that property, and at what cost to legitimate financial work, must be measured. It cannot be assumed from the architecture.

## 2. Defensible research gap

**Prior-art overlap.** Substantial prior-art overlap exists:
- Every component of a layered boundary defense has published precedents, and so do layered combinations.
- Examples:
  - NEXUS: rules, argument inspection and a calibrated logistic-regression risk score choosing among four interventions; peer reviewed, Findings of AACL 2026;
  - Spotlight-Guard: a layered IPI defense with a component ablation; peer reviewed, *Applied Sciences* 2026;
  - Agent-Sentry; AGATE; Progent; ROPE; CaMeL (preprints);
  - AIS: financial authority separation; peer reviewed, *Systems* 2026.
- An architectural or mechanism gap is therefore **not** claimed.

**The evidence gap that remains.** Among the works reviewed (most at abstract level, a few at code or full-text level), no controlled, component-level analysis was found, on an executable banking benchmark, of:
- which components of a layered boundary defense actually carry its protection;
- whether removing a component and suppressing it at test time lead to the same assessment;
- how its learned decision compares with simple deterministic rules on the same proposed calls.

This gap statement is bounded by the review's coverage and reading level. It is **not** a claim that no such analysis exists.

## 3. Research aim

To determine, for the five-layer runtime framework REM v1.0 placed at the tool-call boundary of a banking agent, whether its architectural layering produces defense in depth against indirect prompt injection. The aim is pursued by measuring:
- which of its components contribute protection;
- what that protection costs in legitimate task completion;
- how it compares with simple deterministic rules.

All measurements are on recorded AgentDojo banking traces.

**Relation to the approved objectives.** The aim is derived from O1–O3 (design the framework, evaluate it against adversarial attacks, compare it with existing approaches) and narrows their evaluation focus. It adds no new objective.

## 4. Research objectives

| Objective | Wording | Measurable output (exists) |
|---|---|---|
| O1 | Specify and implement REM v1.0's five layers with a fail-closed configuration | Implemented code; pilot reproduced exactly from public inputs (27 Nov audit, 02 §1.1) |
| O2 | Evaluate REM v1.0 against indirect prompt injection on recorded banking traces | Replay attack outcomes, benign completion and completion under attack on P1, P2, P3 |
| O3a | Compare REM v1.0 with existing approaches available in the same harness | Consequence-independent threshold baseline; rules P1, P2, A2; Progent's manual policy (oracle allow-list, labelled as such); AgentDojo's distributed defenses (descriptive only) |
| O3b | Determine whether REM v1.0's layering yields defense in depth | Protocol-frozen paired component-level ablation (P1–P3); exploratory modelled suppression (DiD-2, P1) |

## 5. Final research questions [PD]

Each RQ has an existing experiment and metric. The status column distinguishes confirmatory from development and exploratory evidence.

| RQ | Question | Experiment and metric | Status |
|---|---|---|---|
| **RQ1** | How well does the ridge logistic estimator, using provenance, context, behavioural and action evidence at the tool-call boundary, discriminate attack-induced proposed calls when whole attack objectives are held out, and how well is it calibrated? | Nested grouped cross-fitting on P1; ROC-AUC, PR-AUC, ECE (`results/pilot/e1_crossfit.json`, reproduced 27 Nov) | Development (P1) |
| **RQ2** | In replay, how do REM v1.0's replay attack outcomes, benign completion and completion under attack compare with:<br>(a) no defense;<br>(b) a consequence-independent threshold policy on the same estimator;<br>(c) simple deterministic rules?<br>On **P1 only**: (d) how do they compare with withholding every state-changing call? | (a)–(b): P1 replay (thesis Table 4.46), P2/P3 ([A21]).<br>(c): rules P1/P2/A2 on P3 (`confirmatory_results.json`).<br>(d): DiD-3 arms B1 vs F-GW, episode-set identity | (a)–(b) development. (c) baselines declared in the 11 Nov protocol. (d) exploratory re-analysis, **P1 only**; P2/P3 would need one offline arm that was **not run** |
| **RQ3** (primary) | Which components of REM v1.0 are necessary for its replay protection, and which add cost, under component-level ablation within the layered architecture? | Protocol-frozen paired ablations [A19] (`dc8407d`, P1) and [A21] (`93e6630`, P1–P3). Metrics: attack-call withholding, benign-call blocking, attacked episodes with an attack call executed, replay attack outcomes, benign completion, completion under attack. Paired grouped-bootstrap intervals; exact McNemar (unclustered) | Protocol-frozen, on previously examined data (P1 development; P2, P3 examined earlier) |
| **RQ4** | Does REM v1.0's protection persist when one evidence family is suppressed at test time rather than removed, and do removal and suppression give the same assessment? | DiD-2 (`2547854`; post-hoc arms `e3e7488`), P1 and the real-reformatting population. Metric: replay attack outcomes | **Exploratory**; suppression is idealized and modelled |
| **RQ5** | Does removing the behavioural evidence group increase task completion without a security regression on recordings unread before the run? | Confirmatory run of 11 Nov (P3, 2,113 episodes); pre-declared rule | **Confirmatory.** Freeze commit not in this repository's history |

**Mapping to the thesis's current RQ1–RQ4.**

| Current | Final |
|---|---|
| RQ1 | RQ1 |
| RQ2 | RQ2 |
| RQ3 (mitigation and cost) | Partly RQ2 (per-call time) and RQ3 (Modify / Escalate / Block equivalence). Residual success against an adapting agent is **not answerable**, and is removed from the RQs |
| RQ4 | RQ3 and RQ4 |
| — | RQ5 is the existing confirmatory evaluation (thesis §4.6.8) |

## 6. Primary empirical contribution

**Question examined:** does REM v1.0's nominal five-layer layering produce actual defense in depth?

**Answer from the evidence (replay; one benchmark):** *only narrowly.*

1. **Enforcement is necessary** for every outcome effect. In shadow mode the same verdicts protect nothing.
2. **The combined learned scoring-and-decision pathway is necessary** for essentially all protection on all three populations. Without it, the predicates alone withhold no attack-labelled call.
   - Ridge LR, calibration and expected-loss selection are removed together.
   - On P1, calibration's separate removal changes no attack outcome.
   - Replacing expected-loss selection with consequence-independent thresholds raises attack outcomes from 11 to 164.
   - The estimator itself is not isolated.
3. **The pathway's protection rests on two evidence families that cover different attack classes:**
   - **Action/provenance evidence:** its removal measurably lowers attack-call withholding on P3 (−9.12 pp [−23.45, −0.74]) and increases episodes with an executed attack call. Its effect on final attack outcomes is not resolved on any population.
   - **Behavioural evidence:** its removal costs no measured security and raises completion. Under modelled test-time suppression, it is the only evidence that stops the credential-change objective (exploratory).
4. **Context detection and the deterministic predicates show no measurable effect** on these data. The context indicator is template-matched and coupled to a behavioural feature; the classifier component does not exist.
5. **Removal and suppression disagree** (exploratory). The amendment that removes behavioural evidence improves completion. But after removal, suppressing the action family returns attack outcomes to near the no-defense level: 653 vs 90 with the behavioural family present.
6. **The depth that exists is bought with low specificity.** On P1:
   - REM v1.0 withholds 81.5% of legitimate restricted calls in benign episodes;
   - its benign completion is exactly that of withholding every state-changing call.

**Summary.** Depth in REM v1.0 is confined to partially redundant evidence families inside one learned decision and one enforcement point. One of the five nominal layers (Detection) and one Decision Engine component (the predicates) contribute no measured protection; the Input & Context layer contributes only through the action evidence built on its labels. The layered architecture, by itself, did not deliver general defense in depth.

## 7. Qualified secondary contributions

| # | Contribution | Qualification |
|---|---|---|
| S1 | **Learned decision vs simple rules.** On the 11 Nov population, simple rules give comparable replay security with equal or higher task completion: P2 rule 4 attacks, A2 rule 4, REM v1.0 3. Over all 2,113 episodes (benign and attacked), A2 completes 1,232 user tasks against REM v1.0's 916. The interval for v1.1 − A2 includes 0 | Replay; one benchmark; differences in task completion not resolved; the rules were baselines declared before that run |
| S2 | **Replay-evaluation observations** for action-boundary defenses:<br>(i) the P1 benign floor;<br>(ii) four verdicts acting as two without a reviewer;<br>(iii) all residual P1 attacks in one benchmark collision task (`user_task_15`);<br>(iv) a published manual policy that is an allow-list of benchmark-specific IBANs | Observations about this benchmark and harness. (i) holds on P1 only |
| S3 | **Confirmed utility effect of removing behavioural evidence** (RQ5): +7.5 pp [1.2, 16.0] task completion; 1 vs 3 attacks | The security difference is not resolved. RQ4's exploratory result indicates a loss of coverage under suppression. **Not a recommendation to adopt REM v1.1** |

## 8. Conservative novelty statement

> This thesis proposes no new detection method, decision rule or architecture. Each REM component, and their layered combination, has precedents; substantial overlap exists with NEXUS, Agent-Sentry, Spotlight-Guard, Progent, ROPE, AGATE and AIS, among others. An independent architectural novelty claim is therefore not made. The thesis contributes controlled empirical evidence on whether one layered boundary defense for a banking agent achieves defense in depth. It uses protocol-frozen paired component-level ablations, an exploratory comparison of removal and test-time suppression, and comparisons with simple rules, on recorded AgentDojo traces. The findings are bounded by NO-ADAPT replay, one benchmark, data examined during development, and a literature review conducted mostly at abstract level.

## 9. Exact REM v1.0 architecture (the evaluated artifact, unchanged)

**Version pinning:**
- code `rem/`, tree `cd11e3232071a4545e89d0259b75267c295aca5f`;
- pipeline `experiments/pilot/`, tree `b05d33ae754416858b1051952c432cf0e0d72197`;
- configuration `configs/exploratory/pilot_e0.yaml`, sha256 `8e1aa107cf3ea0ba5eecbb92bc90a2463202cdde476cfe8a98047ffad74e11d0`.

These are identical in every commit from `7c79883` to the present.

**Inputs:** AgentDojo 0.1.35, banking v1; recorded runs at `089ed468`.

| Layer | As implemented |
|---|---|
| 1 Input & Context | Context capture; hygiene (`strip_invisible`, not exercised by the data); provenance labels (trusted / semi-trusted / untrusted, least-trusted inheritance); entity extraction (IBANs, amounts, credentials, profile values). `rem/algorithms/context/provenance.py` |
| 2 Detection | `x_ctx2`: instruction-pattern indicator over untrusted segments added since the last decision point. `x_ctx1` (classifier) **not implemented**. `rem/algorithms/detection/instruction_patterns.py` |
| 3 Behavioural Analysis | Behavioural features `x_beh1`–`x_beh4` (`x_beh1` defined through `x_ctx2`). Action features `x_act1` (argument occurs in untrusted and not trusted text), `x_act2` (recipient not in the objective), `x_act3` (sensitive egress). `rem/algorithms/behavior/evidence.py` |
| 4 Decision Engine | Ridge logistic regression; Platt-type calibration on the logit; declared consequence tier; predicates D1 (prohibited tool → Block), D2 (high tier with missing evidence → Escalate); verdict by minimum expected loss over Allow / Modify / Escalate / Block with tier-indexed declared costs; linear attribution in the audit record only |
| 5 Mitigation | Step-level: Allow releases; Modify, Escalate and Block withhold the current call (no reviewer; no Modify mechanism exercised) |
| Cross-cutting | Audit record; CUSUM observe-only; offline fitting and recalibration |

**Design values.** The configuration is the exploratory declared configuration. The result files carry the label "SUPERVISOR DECISION REQUIRED".

**Why REM v1.0 is retained unchanged.**
- It is the only configuration that is frozen, evaluated across all analyses and reproduced.
- The primary contribution is a finding *about* it.
- No existing evidence compels a change:
  - REM v1.1's gain is in utility only, with an unresolved security effect and an exploratory loss of coverage;
  - REM-DiD depends on an oracle authorization channel;
  - REM-X is unimplemented.

## 10. Experimental findings mapped to contributions

| Contribution | Finding | Source |
|---|---|---|
| Primary (6.1) | Shadow mode = no defense (672 / 174 / 436) | [A21] A4; thesis Table 4.26 / 4.28 |
| Primary (6.2) | Pathway removed: 672 / 174 / 435 attacks. P1: calibration removed 11; thresholds 164 | [A21] A3; [A19] A2, A3, A6 |
| Primary (6.3) | Action evidence: P3 withholding −9.12 pp [−23.45, −0.74]; executed attack calls 34 vs 3 (P3), 49 vs 24 (P1); attack outcomes 8 vs 3, 17 vs 11 (not resolved) | [A21] AIC; thesis Tables 4.26–4.28 |
| Primary (6.3) | Behavioural suppression: 131 vs 11; 119 of 120 added in `injection_task_7` | [D2] |
| Primary (6.4) | Context and predicates: no change (A1a, A1b, A3P; suppression 11 vs 11) | [A21]; [D2] |
| Primary (6.5) | v1.1 with action suppression 653 vs v1.0 90 | [D2] post-hoc arm |
| Primary (6.6) | P1 floor identity; 81.5% benign-call blocking | DiD-3 raw (recomputed 27 Nov); [A21] |
| S1 | Rule arms on P3 | `REM_FINAL_SUBMISSION/results/confirmatory_results.json` |
| S2 | Verdict equivalence; collision; Progent list content | Thesis Ch. 4 §4.5.7, §4.2.2; `REM_COMPARATIVE_EVALUATION_PHASE/02` §2 |
| S3 | Confirmatory contrast and verdict | `confirmatory_results.json` |
| RQ1 | ROC-AUC 0.938, ECE 0.044 | `results/pilot/e1_crossfit.json` (reproduced) |

## 11. Limitations

1. **NO-ADAPT replay.**
   - No live agent and no adaptive attacker.
   - A withheld call cannot redirect the agent.
   - Benign completion is insensitive to read-only tasks.
   - Replay outcomes are not closed-loop performance.
2. **One benchmark and domain:**
   - AgentDojo banking v1 (16 user tasks, 9 injection tasks);
   - 8 of 9 attacker objectives share one IBAN;
   - one collision task holds every residual P1 attack;
   - no currency, source-account or exfiltration evaluation.
3. **Data history.**
   - P1 is development data. P2 was examined in R2. P3 has been development data since 11 Nov.
   - Only the 11 Nov run is confirmatory.
   - Pre-registration claims older than 17 Nov are not verifiable from this repository's git history.
4. **Ablation granularity:**
   - provenance labelling not removable;
   - estimator not isolable;
   - detection and behavioural features coupled;
   - hygiene not exercised;
   - classifier absent;
   - Modify and Escalate not exercised as designed.
5. **Suppression is modelled and idealized** (exploratory). It shows potential coverage, not attacker feasibility.
6. **Statistics.**
   - Few clusters: 16 user tasks, 9 attack objectives.
   - Exact McNemar values ignore clustering.
   - Several effects are unresolved; they are reported as such.
7. **Design values are exploratory**, not supervisor-approved.
8. **Labels.** Reference-match labels drive fitting and call-level metrics. The human label audit was not executed. Final attack outcomes use AgentDojo's checks.
9. **Literature.** Mostly abstract-level. NEXUS, AGATE, AgentCap, Agent-Sentry and AIS full texts were not read.
10. **No controlled comparison with MELON, DRIFT, ROPE or full Progent was run.** No superiority or inferiority claim is made.

## 12. Ten examiner questions and accurate answers

**1. "What is new? NEXUS combines rules, inspection and a calibrated LR over four interventions."**
- No mechanism is new, and the thesis says so.
- What the thesis adds is evidence that a design of this shape need not provide depth. On executable banking traces, protocol-frozen component-level ablation shows:
  - the Detection layer and the predicates contribute no measured protection;
  - the rest act through one decision pathway and one enforcement point.
- NEXUS was read at abstract level only. No comparison of results is made.

**2. "Your attack success falls from 22.6% to 0.4%. Isn't that just blocking everything?"**
- **On P1, largely, as far as benign work is concerned.** Its benign completions are exactly those of withholding every state-changing call.
- It differs from withholding everything in two ways:
  - it completes 94 more tasks under attack;
  - it lets 11 attacks through, all in one task whose user request names the attacker's account.
- This identity is shown on P1 only.

**3. "So does all protection come from the learned decision?"**
- **No.** The learned pathway is necessary, but it decides on evidence and acts through enforcement:
  - removing enforcement removes all effect;
  - removing action evidence measurably lowers attack-call withholding on P3;
  - suppressing behavioural evidence lets the credential-change attack through (exploratory).
- The pathway's parts (estimator, calibration, expected loss) were removed together in the 21 Nov protocol. On P1, calibration and the expected-loss rule were varied separately.

**4. "Did you ablate the five layers?"**
- **No: component-level ablation within a layered architecture.**
- Provenance labelling cannot be removed without fabricating the inputs of later features, so only its evidence was removed from the estimator.
- The detection classifier does not exist.
- Hygiene was never exercised by the data.
- Detection and behavioural features are coupled.

**5. "Why should replay results say anything about real agents?"**
- They measure what withholding recorded actions does when the agent does not react. They do not measure closed-loop attack success or task completion.
- The thesis claims neither live nor adaptive robustness.

**6. "Was the ablation tested on unseen data?"**
- **No.** It is a protocol-frozen paired ablation:
  - the protocols were committed before any arm was scored;
  - the data had been examined before (P1 development; P2 in R2; P3 since 11 Nov), and six arms' P1 outcomes were already known.
- Its value is the paired comparison on identical episodes, not out-of-sample validation.
- The only confirmatory result is the 11 Nov run.

**7. "Behavioural evidence: helpful or harmful?"**
- Both, depending on the test:
  - **Removing it** costs no measured security and raises task completion; this is confirmatory for completion.
  - **Suppressing it at test time** (exploratory, modelled) lets 120 more attacks succeed, almost all of them the credential-change objective.
  - **After removing it,** suppressing the action evidence lets 653 attacks succeed, against 90 with it present.
- This disagreement between removal and suppression is a finding in its own right.

**8. "Progent's policy has no successful attack and completes more tasks. Isn't REM worse?"**
- The published manual policy is an allow-list of this benchmark's legitimate IBANs that excludes the attacker's. Its result reflects knowledge of the benchmark.
- No controlled comparison with Progent's generated policies, ROPE, MELON or DRIFT was run. No ranking is claimed in either direction.

**9. "Your detector matches 'important message'. Is that leakage?"**
- It encodes the benchmark's injection template, and this is disclosed.
- Its removal changes no outcome on any population, so no reported protection depends on it.

**10. "Why keep REM v1.0 when v1.1 completes more tasks?"**
- v1.1's gain is confirmed for completion only:
  - its security difference is unresolved;
  - the exploratory suppression analysis indicates that it loses coverage of one attack class.
- v1.0 is the frozen, fully evaluated and reproduced artifact. Adopting v1.1 is a supervisor decision that the thesis presents with both sides of the evidence.
