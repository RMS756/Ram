# 08: Final thesis scientific position

**Status.**
- The wording below is proposed **[PD]** for the researcher and supervisor. It does not edit the thesis.
- It keeps the topic *"Defense in Depth for Financial AI Agents Against Indirect Prompt Injection"* as instructed.
- The printed title differs (01 §2). The supervisor must confirm which is official.
- The position below works under either wording: REM is the artifact; defense in depth is the property examined.

## A. Research problem

**Problem.**
- Tool-using financial agents read untrusted content (transaction subjects, files, notices) in the same context as the user's instructions.
- Indirect prompt injection in that content can induce financial actions the user never requested: transfers, payment changes, credential changes.
- Defenses placed at the tool-call boundary are commonly built as several layers: content inspection, behavioural monitoring, action assessment, a risk-informed decision and enforcement.
- They are commonly presented as defense in depth.

**What is not known.** Whether such layering actually provides independent protection, or whether one layer does all the work while the others add cost. It is also not known how a learned, risk-informed decision layer compares with simple deterministic rules on the same actions.

**Why it matters in finance.**
- Each wrongly released call can move money.
- Each wrongly withheld call blocks legitimate payments.

## B. Research gap (evidence-based)

**What is already published.** The individual mechanisms and their layered combination:
- context inspection, behavioural and sequence monitoring, and argument provenance;
- request-derived authorization;
- calibrated risk scores with graduated interventions;
- enforcement before execution.

Representative systems: NEXUS, Agent-Sentry, Spotlight-Guard, Progent, ROPE, AGATE, CaMeL, AIS (03 §2).

**Defense in depth** is advocated as a design principle for agents (AgentSandbox).

**What the records examined do not provide.** At the evidence levels read (mostly abstracts), they do not provide a controlled, component-level answer for a banking agent on an executable benchmark to:
- (i) how much of a layered boundary defense's protection each layer carries;
- (ii) whether the layers fail independently;
- (iii) whether a calibrated, consequence-aware learned decision adds anything over deterministic rules when user tasks and attack objectives are held out.

The thesis addresses this **evidence gap**, not a mechanism gap. The gap statement is bounded by:
- abstract-level reading of several close works;
- the absence of full-text access to AGATE, AgentCap, Agent-Sentry and AIS.

## C. Research aim

To evaluate whether a five-layer runtime framework at the tool-call boundary provides defense in depth for a financial AI agent against indirect prompt injection. The framework is REM: provenance, context and behavioural evidence; a calibrated, consequence-aware decision; and deterministic mitigation.

The evaluation is done on recorded agent behaviour in the AgentDojo banking environment, by:
- measuring each layer's contribution to security and its cost to legitimate tasks;
- comparing REM with simple deterministic rules.

## D. Research objectives (aligned with the approved O1–O3)

| Objective | Wording | Measurable output |
|---|---|---|
| O1 | Design and implement REM's five layers with a fail-closed specification | Implemented framework; reproduction of the pilot (done) |
| O2 | Evaluate REM against indirect prompt injection on recorded AgentDojo banking traces | Replay attack outcomes and benign / under-attack completion on P1, P2, P3, with the withhold-everything reference |
| O3a | Compare REM with existing approaches available in the same harness | Threshold baseline; three simple rules; AgentDojo's distributed defenses (descriptive); Progent's manual policy (with its oracle caveat) |
| O3b | Determine each layer's contribution, as the defense-in-depth question | Pre-registered ablation on three populations; exploratory removal-versus-evasion analysis |

## E. Research questions (answerable with existing evidence) [PD]

| RQ | Question |
|---|---|
| RQ1 | How well does a ridge logistic estimator over provenance, context, behavioural and action evidence discriminate injected financial actions under grouped cross-fitting, and how well is it calibrated? |
| RQ2 | In replay, how do REM v1.0's security and benign-task outcomes compare with:<br>(a) no defense;<br>(b) withholding every state-changing call;<br>(c) a consequence-independent threshold;<br>(d) simple deterministic rules? |
| RQ3 | Which of REM's five layers carries its protection, and which add only cost? Answered by pre-registered ablation |
| RQ4 (exploratory) | Do REM's evidence controls fail independently when one is evaded rather than removed? |

**Requirement for RQ2(b).** The P1 part is answerable from stored data. P2 and P3 need the small offline arm in 07 §2.1; otherwise RQ2(b) is answered on P1 only.

## F. Research contributions

**Primary contribution (empirical, defense in depth).**
- A pre-registered, paired, component-level evaluation shows that, in the five-layer REM framework on AgentDojo banking replays, protection is **not layered**:
  - the learned, consequence-aware decision acting through enforcement removes 661 of 672 replay attack outcomes on P1 (433 of 436 on P3);
  - the context, calibration, predicate and Modify components change no attack outcome;
  - the behavioural layer lowers benign completion.
- The protection is obtained by withholding almost every state-changing call. On P1 the benign tasks REM completes are exactly those completed when every state-changing call is withheld.

**Secondary contributions (only those supported):**
1. **Comparison with simple rules.**
   - Simple deterministic rules on the same calls attain comparable replay security: 4 vs 3 attacks on the confirmatory population.
   - They attain equal or higher task completion; differences are not statistically resolved.
   - The learned decision is therefore not shown to add value over rules.
2. **Evaluation-methodology findings for action-boundary defenses under NO-ADAPT replay:**
   - the benign-utility floor;
   - the collapse of four verdicts to two without a reviewer;
   - residual attacks concentrated in one benchmark collision task;
   - the oracle content of a published manual policy.
3. **(Exploratory) Removal versus evasion.**
   - Removal-based ablation and modelled test-time evasion can give opposite conclusions about the same layer.
   - Refitting without behavioural evidence lost no security, but the action-evidence family then became a single point of failure under modelled evasion (653 vs 90 attacks).

**One confirmed within-framework result** (reported, not a contribution claim): removing behavioural evidence raises task completion by 7.5 points [1.2, 16.0] on unread recordings, with an unresolved security difference.

## G. Novelty statement (conservative)

> This thesis does not propose a new detection algorithm, decision rule or architecture. Each component of REM, and their layering, has precedents in published work (NEXUS, Agent-Sentry, Spotlight-Guard, Progent, ROPE, AGATE and others). The contribution is evidence. It is a controlled, pre-registered, component-level evaluation of a layered runtime defense for a banking agent. It shows, on recorded AgentDojo traces, that nominal layering did not provide defense in depth: one learned component carried all measured protection, at the cost of withholding nearly all financial actions, and simple deterministic rules matched it. The results are limited to non-adaptive replay on one benchmark.

## H. Final architecture

**REM v1.0, unchanged** (06):
- Input & Context: provenance labels;
- Detection: context evidence;
- Behavioural Analysis: history evidence;
- Decision Engine: ridge LR → Platt on the logit → consequence tier → predicates → expected-loss verdict;
- Mitigation: step-level withhold or release;
- audit and CUSUM observe-only as cross-cutting services.

**Why chosen.**
- It is the only configuration that is frozen, fully evaluated and reproduced.
- Its measured lack of depth is the central finding.
- Changing it now would replace a defensible negative result with an unevaluated design.

REM v1.1, REM-DiD and REM-X are excluded from the artifact. Their roles are given in 06 §3.

## I. Experimental evidence per contribution

| Contribution | Evidence | Location |
|---|---|---|
| Primary (no depth) | Ablation, 9 arms × 3 populations, pre-registered at `93e6630` | `REM_ABLATION_STUDY/03`, `05_EPISODE_RESULTS.jsonl.gz`; this audit 02 §1.2 |
| Primary (floor) | REM v1.0 vs withhold-everything on P1, identical benign episode sets | `REM_DEFENSE_IN_DEPTH/results/did3_raw.jsonl.gz`; 02 §1.3 |
| Baseline reproducibility | Fresh re-run, identical outputs | 02 §1.1 |
| Secondary 1 (rules) | Confirmatory arms P1/P2/A2 vs M00 | `REM_FINAL_SUBMISSION/results/confirmatory_results.json`; 02 §2 |
| Secondary 2 (methodology) | Verdict-replacement test (thesis Ch. 4); collision analysis; Progent oracle analysis | Humanized Ch. 4; `REM_COMPARATIVE_EVALUATION_PHASE/02` §2 |
| Secondary 3 (removal vs evasion) | DiD-2 and DiD-2a | `REM_DEFENSE_IN_DEPTH/05`, `results/did2_results.json` |

## J. Limitations

1. **NO-ADAPT replay only.**
   - No live agent; no adaptive attacker.
   - A withheld call cannot change what the agent does next.
   - Benign utility is insensitive to read-only completions.
2. **One benchmark, one domain:**
   - AgentDojo banking v1 (16 user tasks, 9 injection tasks);
   - 8 of 9 attacker goals share one IBAN;
   - one collision task;
   - no currency, source-account or exfiltration evaluation by REM.
3. **Development reuse.** P1 designed the system; P2 and P3 were read before the ablation. Only the v1.1 confirmatory run used unread data.
4. **Exploratory design values.** Costs, tiers and thresholds are not supervisor-approved.
5. **No reviewer.** Escalate equals Block, so the four-verdict design is untested as designed.
6. **Labels.** Reference-match labels; the human label audit was not executed.
7. **Template-tuned context detector** (no outcome effect).
8. **Pre-registration before 17 Nov 2026** is not verifiable from this repository's history.
9. **Literature.** Several close works were read at abstract level only.

## K. Defense preparation: ten hard questions

**1. "What is new here? NEXUS already combines rules, inspection and a calibrated LR over four interventions."**
- Nothing in the mechanism is new, and the thesis says so.
- The contribution is a controlled, pre-registered component-level evaluation on an executable banking benchmark.
- That evaluation shows the learned layer carries all measured protection and the other layers carry none (05 C1).
- NEXUS reports a gain over rule-only on its own benchmarks. On held-out AgentDojo banking replays, REM found no gain of the learned decision over simple rules (02 §2).

**2. "Your 0.4% attack success is impressive. Isn't that just blocking everything?"**
- Largely, yes, and the thesis must say so.
- Withhold precision is 0.40. 81.5% of legitimate restricted calls in benign P1 episodes are withheld.
- REM's 105 benign completions are exactly those obtained by withholding every state-changing call (02 §1.3).
- REM's distinctive effect over withholding everything is +94 tasks under attack, at +11 attacks, all in one collision task.

**3. "Why should we believe replay results say anything about real agents?"**
- They say what a withheld action prevents when the agent does not react. They say nothing about an agent that retries or reroutes.
- The thesis claims no live or adaptive robustness.
- The closed-loop harness exists but was not run (no model endpoint).
- The conclusions are framed as properties of the defense's decisions on recorded behaviour.

**4. "Progent's policy beats REM on both security and utility. Why not just use Progent?"**
- The published manual policy is an allow-list of the benchmark's own IBANs that excludes the attacker's (02 §3). Its replay result reflects benchmark knowledge, not generalization.
- The fair reading is that a deterministic authorization rule informed by the user's legitimate payees outperforms a learned risk decision in replay.
- That supports the thesis's negative result about the learned layer.

**5. "Where is the defense in depth? Your ablation says four layers do nothing."**
- **That is the finding.**
- Defense in depth requires layers whose failures are not shared. REM's layers are nominal: their protective effect collapses onto one decision.
- The exploratory DiD-2 analysis shows how fragile this is. When a modelled attacker defeats the action-evidence family, REM v1.1 returns to 653 attacks, against 90 for v1.0.

**6. "Did you tune on your test data?"**
- P1 was development data, and P2 and P3 were read before the ablation, which the thesis states.
- The one confirmatory result (v1.1) used 2,113 episodes unread before the run, under a pre-declared rule.
- The ablation is pre-registered (`93e6630`). Its value is the paired structure, not out-of-sample performance.

**7. "Your detector contains the string 'important message'. Isn't that cheating?"**
- It encodes the benchmark's injection template, and this must be disclosed.
- It has no outcome effect: the ablation removing it changes no attack outcome. No headline number depends on it.

**8. "Why are Modify, Escalate and Block reported as different verdicts if they are the same?"**
- Without a reviewer and with step-level withholding, they produce the same action.
- Replacing all of them by Block changes none of 3,313 episodes.
- The four-verdict structure acts only by moving the Allow boundary. Its intended differences are untested.

**9. "How do you know your labels are right?"**
- Labels match calls to the injection task's reference solution on the attacker's key arguments.
- The **primary outcome does not use them**: replay attack success is AgentDojo's own state check.
- The labels affect fitting and call-level rates.
- A human label audit was prepared but not executed. It is a stated limitation.

**10. "Why did you build so many versions (REM-A/B/C, B2, B3, DiD, X) and then keep v1.0?"**
- They were pre-registered explorations. Each was decided by frozen criteria: several NO-GO, some INCONCLUSIVE.
- They consistently showed two things:
  - learned stages add nothing behind deterministic authorization;
  - request-derived authorization fails on held-out phrasing.
- Keeping v1.0 preserves the one fully evaluated and reproduced artifact. The later lines are reported as supporting exploratory evidence, not as the artifact.
