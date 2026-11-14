<!-- @frag ch5_all -->
## 5.41 Introduction

This chapter draws the conclusions of the thesis. Section 5.42 answers the research questions from the evidence of Chapter 4. Section 5.43 assesses the objectives. Section 5.44 lists the contributions with the precedent, code, experiment, result and limits of each. Section 5.45 records what was proposed and not confirmed, the variants that were rejected, and why the negative findings matter. Section 5.46 states the limitations, Section 5.47 the future work in order of priority, and Section 5.48 concludes.

Every conclusion is bounded in the same way. The evidence comes from recorded trajectories of real agents in one banking benchmark, replayed under the assumption that the agent does not adapt to a refusal. No live agent was run. The design values are declared and await approval.

## 5.42 Answers to the Research Questions

The research questions remain proposed wording, pending the supervisor's confirmation (Chapter 1, Section 1.7).

**Table 5.41. Answers to the research questions**

| RQ | Answer | Evidence and its kind | Not shown |
|---|---|---|---|
| RQ1, estimation | The ridge logistic estimator separates recorded attack attempts from legitimate calls well on attack objectives it has not seen: held-out ROC-AUC 0.938 [0.908, 0.961], average precision 0.719, ECE 0.044. Calibration left the probabilities almost unchanged and did not repair the one fold that was miscalibrated, the credential-change objective (ECE 0.189) | Offline prediction, nine folds by attack objective (Chapter 4, Section 4.4) | That the separation needs a model: one provenance feature alone has recall 0.971 at a false-positive rate of 0.147 |
| RQ2, decision | Compared with the consequence-independent baseline on the same estimator, the tier-indexed expected-loss rule lowers replay attack success from 5.5% to 0.4% and benign task completion from 51% to 31%. Compared with rules that use no estimator and no costs, it gives about the same number of successful attacks and lower task completion. A published fixed-list policy and an exploratory request-derived permission rule, both deterministic, complete more tasks than either REM version with no more successful attacks | Replay on the primary recordings (Chapter 4, Sections 4.6 and 4.42); confirmatory replay (Chapter 4, Section 4.45); development replay of the extension (Chapter 4, Section 4.89) | Any advantage of the cost-based rule over the simple rules; any result with a live agent |
| RQ3, mitigation and cost | Under replay a withheld call does not recur, so residual attack success after Modify is near zero by construction. Escalate is the most frequent non-Allow verdict (1,392 in the 2,113 episodes of the second population for v1.0). Modify, Escalate and Block have the same effect in this evaluation. A decision takes a median of 0.23 ms | Replay; observe-only analysis; runtime measurement (Chapter 4, Sections 4.6, 4.42 and 4.45) | Residual success against an agent that retries; the effect of a reviewer; any difference among the three verdicts |
| RQ4, component contribution | Action evidence carries the discrimination. The instruction-pattern context indicator showed no benefit. Behavioral evidence lowered task completion with no measured security benefit; the gain in task completion from removing it met the pre-declared decision rule on recordings unread until that run, while the security difference is not resolved. Removing calibration left the attack count unchanged and changed five benign outcomes; the predicates changed none. The tier map moves the trade-off. In the exploratory extension the deterministic permission rule carries the gain, and a learned model on the same evidence adds no demonstrated value | Ablations (Chapter 4, Sections 4.7, 4.90 and 4.91); confirmatory replay (Chapter 4, Section 4.45) | The value of the injection classifier, which was not available; behavior of these components in other environments |

## 5.43 Achievement of the Objectives

**Table 5.42. Objectives and how far they were achieved**

| Objective | Achieved | Not achieved |
|---|---|---|
| O1: design a REM framework for the security of financial and task-automation agents | A five-layer framework specified, implemented and tested for a banking agent | No task-automation environment was evaluated; the injection classifier of the Detection Layer is absent |
| O2: evaluate the framework against adversarial attacks | Evaluation on recorded trajectories of real agents under indirect prompt injection, with held-out attack objectives, a double holdout, robustness probes and one confirmatory run | Evaluation with live agents; adaptive attackers; a human reviewer; repeated runs |
| O3: compare performance with existing security approaches | Controlled comparison with a threshold baseline and three rule baselines on the same episodes; replay of one published policy (the manual banking policy of Progent) in the same harness; design-level comparison with the closest published systems | Experimental comparison with any published defense that needs a language model. The MELON integration is implemented and unevaluated |

O1 is achieved for the banking setting. O2 is achieved within recorded-trace replay. O3 is achieved for internal baselines and for one published deterministic policy in replay.

## 5.44 Contributions

**Table 5.43. Each contribution with its precedent, implementation, experiment, measured result and limits**

| Contribution | Literature source or precedent | Implemented in | Supporting experiment | Measured result | Scope and limits |
|---|---|---|---|---|---|
| 1. A specified and implemented runtime layer: provenance-based evidence, calibrated ridge logistic estimate, consequence tiers, predicates, four-verdict expected-loss rule, deterministic mitigation, audit record | Cox (1958); le Cessie & van Houwelingen (1992); Platt (2000); Guo et al. (2017); Elkan (2001); Chow (1970); Lundberg & Lee (2017). The same family of design is published: Hossain et al. (2026); Y. Zhang et al. (2026) | `rem/` (Chapter 3; Appendix B) | Software verification | 278 tests pass; replay fidelity 99.4% and 98.4%; exact re-execution | Not a new mechanism. One declared component absent |
| 2. An evaluation protocol that isolates the decision rule, holds out attack objectives and user tasks, includes model-free rule baselines, and reports outcome layers separately | Grouped evaluation and leakage control: Arp et al. (2022). Paired counterfactual design: T. Yang et al. (2026). Offline use of AgentDojo recordings: Kekatos et al. (2026) | `experiments/pilot/`, `experiments/authz_study/`, `experiments/improve_study/` | Chapters 3 and 4 | Protocols committed before outcomes; three post-hoc additions labelled | Replay only; one benchmark |
| 3. Measured security and its cost for REM v1.0 | — | as above | Replay, primary and second population | Attack success 22.6% to 0.4% and 21.1% to 0.15%; benign task completion 52% to 31%; 33 of 178 and 4 of 51 authorized calls released | NO-ADAPT; no reviewer; declared costs |
| 4. Evidence that the learned, cost-based decision adds no measured value over simple provenance rules on this benchmark | Concern raised for calibrated scores in general by C. Zhang et al. (2026) | `experiments/authz_study/` | Rule baselines; confirmatory replay | Rules: 12 to 13 attacks against 11, and 4 against 3; task completion equal or higher | A null finding on one benchmark, not a proof of equivalence |
| 5. A confirmed gain in task completion: REM without behavioral evidence (v1.1, proposed) | Cautions on behavioral anomaly evidence: Sommer & Paxson (2010) | the pilot's ablation fit; `confirm_a.py` | Confirmatory replay under a pre-committed protocol | +7.48 points task completion [1.17, 16.02]; 1 against 3 successful attacks of 2,065 | Security difference not resolved (14 against 11 under the double holdout); same benchmark tasks; not better than the rules; adoption awaits approval |
| 6. Four negative results (Section 5.45) | C. Zhang et al. (2026); F. Jia et al. (2025); Kekatos et al. (2026) | `experiments/authz_study/` | Double holdout; probes | 132 against 11 attacks; 313 attacks; 12 to 191 attacks | One benchmark; one objective class drives the first |
| 7. Identification of what limits provenance evidence: it does not represent what the user asked for | Yan et al. (2026); aiAuthZ at abstract and repository level | fixtures | Paired call fixtures | None of the arms tested up to 11 November gets every pair right; unrequested payments in the user's own words are released by every such arm that releases legitimate payments | Hand-written cases; mechanism, not prevalence; a statement about the tested features |
| 8. An exploratory extension and an attribution result: task-permission evidence compiled from the request, used as a deterministic rule (proposed, not adopted) | F. Jia et al. (2025); T. Shi et al. (2025); Debenedetti et al. (2025) | `experiments/improve_study/` | Development replay on both populations; ablations; one published policy replayed in the same harness | Benign tasks 149 against 105 of 334 and 32 against 18 of 48 with 10 against 11 and 3 against 3 successful attacks; not resolved against rule A2; the published policy has no successful attack; a learned model on the same evidence adds no demonstrated value and has 38 against 10 attacks under reformatting. After the repairs of 14 November: 1 and 0 successful attacks, one user task lost, still not resolved against A2 or the published policy; behind the authority guard the learned model loses its robustness failure and still adds no established value | Development evidence only; parser written with the benchmark's requests in view; fixtures not independently reviewed |

## 5.45 What Was Not Confirmed, What Was Rejected, and Why It Matters

**Proposed and not confirmed.**

- **That tier-indexed expected-loss verdicts reduce financial harm at acceptable cost in operation.** This was the central practical claim of the design. It needs enforcement with live agents, which was not run. It remains unestablished.
- **That the four verdicts are useful as four.** Modify, Escalate and Block coincide in replay without a reviewer.
- **That behavioral evidence helps.** It did not; removing it raised task completion, and that gain met the pre-declared decision rule.
- **That calibration improves decisions.** Removing it left the attack count unchanged and five more benign tasks were completed.
- **That consequence-aware learned decisions add value over simple rules.** No such value was measured, for REM or for a learned model given task-permission evidence.
- **That the two-verdict decision is safe by itself.** Applied to REM v1.1 without a guard it released every held-out credential-change attack.

**Rejected variants.**

| Variant | Result | Decision |
|---|---|---|
| Authorization-aware intervention-value policy (pre-declared candidate) | 132 successful attacks against 11; utility gain not established and almost absent under double holdout | Rejected |
| Outcome-supervised estimator | 76 attacks against 11, no utility gain | Rejected |
| Authorization features added to REM's estimator | 69 attacks against 11 | Rejected |
| Rule that trusts documents named by the user | 313 attacks | Rejected |
| Provenance rule on exact string match alone | 12 attacks, rising to 191 when the identifier is reformatted | Not recommended |
| Trusted authorization component | Not implemented: the benchmark has no trusted authorization record, so an evaluation would be tautological or would use an oracle | Future work |
| Selective-risk or conformal thresholds | Not implemented: they move the operating point of the same score and need a risk tolerance that nobody has approved | Not pursued |
| REM v1.1 with a two-verdict decision and no guard | 131 successful attacks against 11; all 119 held-out credential-change attacks released | Rejected |
| Learned model on task-permission evidence (with or without a guard) | No demonstrated gain over the permission rule; 38 against 10 attacks when the identifier is reformatted | Not recommended |
| Deterministic permission rule compiled from the request (G1) | More benign tasks than REM v1.0 with no more attacks, on development data; unresolved against rule A2; worse on security than a published fixed list; three defects found afterwards | Superseded by G2 for analysis; decision pending |
| Repaired permission rule (G2) | 1 and 0 successful attacks; one user task lost to an unevaluated condition; unresolved against A2 and the published policy | Exploratory; decision pending |
| Learned model behind the authority guard (L2g, L3, L3c) | The guard removes the reformatting failure; the gain over the rule has intervals with lower bound zero; typed provenance changes nothing | Not established |

**Why the negative findings matter.**

1. **They test published proposals under a condition their authors did not examine.** Supervision on intervention value improves control in the settings studied by C. Zhang et al. (2026). Here, with nine attack objectives and one of them held out, it removed protection against the held-out class. A method that depends on outcome labels inherits the coverage of those labels.
2. **They show what a strong security figure can hide.** REM v1.0's attack success of 0.4% coexists with the release of 4 of 89 legitimate transfers. Reported without the second figure, the first would describe a policy that withholds payments as if it were a policy that detects attacks. This is the over-defense that T. Yang et al. (2026) report in general.
3. **They place the difficulty in what the evidence represents.** With provenance evidence, a good estimator, a simple rule and an elaborate policy converge on the same frontier and fail the same paired cases. In the exploratory extension, a deterministic representation of the request moved the frontier on development data and a learned model on top of it did not. Effort on the estimator is therefore unlikely to help; a trusted statement of what the user authorized, or a validated way of compiling it from the request, might.
4. **They qualify provenance as evidence.** Exact-string provenance is removed by reformatting an identifier, and a document that the user names is exactly where an attacker writes.

## 5.46 Limitations and Threats to Validity

The limitations are discussed in Chapter 4, Section 4.17. In summary:

1. **Replay, not enforcement.** Every outcome assumes that the agent emits its recorded calls whatever is withheld. A live agent can retry or take another route. Replay attack success is not an upper bound on live attack success.
2. **One benchmark.** One environment, sixteen user tasks, nine attack objectives, one attacker account. The second population has new agents and templates and the same tasks. A few tasks decide each utility comparison.
3. **Design status.** Costs, tiers, predicates, the feature set and the label rule are declared values without approval. Every result is exploratory by label.
4. **Labels.** They are reference-matched attempt labels, ambiguous for one user task in early benchmark versions, and not audited by a human.
5. **No reviewer.** Escalation outcomes are bounded by an oracle and by no reviewer. No reviewer effectiveness is assumed or measured.
6. **Reuse and post-hoc analysis.** The primary recordings were examined many times. Only one contrast was tested on data unread at the time, and those data are development evidence since then. The extension study has no confirmatory part, and its request parser was written with the benchmark's requests in view.
7. **Statistics.** Nine attack groups and sixteen task groups; intervals are wide and need not reach nominal coverage; one run per configuration.
8. **Missing component.** No injection classifier was available for the Detection Layer.
9. **Literature.** The systematic review was conducted at record level. Six papers were read in full afterwards. Five close works are known only from abstracts or from their authors' repositories (NEXUS, aiAuthZ, Kairos, Progent, CaMeL).
10. **Limited external comparison.** One published deterministic policy was replayed on the recorded episodes. No defense that needs a language model was run.
11. **Fixtures and rules were written with knowledge of the benchmark and of REM's features.**

## 5.47 Future Work, in Order of Priority

1. **Supervisor decisions.** Approve or replace the declared design values, the label rule, the mitigation semantics, the replay amendment and the proposed amendment REM v1.1 (Appendix F).
2. **A trusted authorization input.** Specify how a structured statement of what the user authorized (operation, source account, recipient, amount, constraints) is captured by the trusted interface, and check proposed actions against it deterministically. It fits in the Input & Context Layer and as a policy predicate of the Decision Engine; no sixth layer is needed. It changes the threat model by adding a trusted channel, and its evaluation needs a benchmark that contains such records. The present thesis shows that the tested provenance features do not replace it. The exploratory permission rule of Chapter 4, Section 4.92, is a first step that compiles such a statement from the request text; it needs requests written by other people, an independent review of its test cases and the repair of the parser defects that the fixtures exposed.
3. **Live enforcing-mode evaluation.** Run the no-defense reference, B1, both REM versions and the rule baselines with live agents, with at least three repeated runs and fixed, recorded versions and decoding parameters. This measures adaptation after refusals and whether the four verdicts differ.
4. **Comparison with published defenses under the same conditions.** A sealed protocol fixes one benchmark version for all conditions and names the comparisons in advance. The MELON integration is ready and needs a model credential, MELON's embedding service and an approved spending limit; Progent with generated policies and Task Shield need a model as well. A comparison with NEXUS needs its full text, its code at a pinned commit and a justified adapter.
5. **Label audit.** Annotate the prepared package with at least one human annotator, preferably two, and report agreement.
6. **A reviewer model** with error rate and delay, so that the value of Escalate can be estimated between its two bounds.
7. **Provenance that survives reformatting,** by canonicalizing identifiers before matching. The extension applies a type-specific canonical form inside the permission rule; the provenance labeler of REM itself is unchanged, and adaptive variants were not tested.
8. **The injection classifier,** selected on the agent's own tool outputs at a low false-positive rate (Z. Liu, 2026).
9. **Full-text literature review,** including the three works known only from abstracts, and a search of the named databases.
10. **Further benchmarks,** with new user tasks, reported per benchmark.

## 5.48 Conclusion

This thesis set out to design a runtime framework that decides, for each tool call proposed by a financial AI agent, whether to allow, modify, escalate or block it. The decision minimizes expected loss under a calibrated probability of adversarial inducement and a declared consequence tier, and every verdict is recorded for audit. The framework was specified, implemented at the tool boundary of a benchmark agent, and evaluated on 5,426 recorded episodes of real agents in a banking environment: 3,313 used for fitting and cross-validated evaluation, and 2,113 held back for one confirmatory test and used as development evidence afterwards.

Four things were found.

**REM is safe in replay, and restrictive.** It withholds nearly all recorded attack attempts, on attack objectives, user tasks, agents and templates it has not seen. It does so largely by withholding state-changing calls, legitimate ones included.

**Its learned and cost-based parts are not shown to earn their place.** Rules that read one or two pieces of provenance evidence reach the same security with at least as much completed work. Within the framework, one change raises task completion, and that gain was confirmed on data unread at the time: removing behavioral evidence. That change brings REM to the level of the rules, not above it.

**The limit is what the evidence represents.** Every policy built on provenance evidence, simple or elaborate, fails when an unrequested payment uses the user's own words, and an elaborate policy trained on outcomes failed on an attack class it had not seen. These are findings about the tested features and policies, not a proof that the request text cannot supply the missing information.

**A deterministic representation of the request helps, and the learned core does not add to it.** In an exploratory extension, a rule that compiles the operation, recipient and amount the user asked for completes more benign tasks than REM with no more successful attacks on development data. A published fixed list of payees does better still on security. A learned model on the same evidence adds nothing that could be demonstrated. After an external review found three defects, a repaired rule removed nine of the ten remaining successful attacks without losing tasks, except in the one task whose condition it declines to guess; behind an authority guard the learned model no longer loses robustness, but its gain is still not established. The improvement that was observed belongs to the rule.

These findings come from recorded traces and from a replay that assumes the agent does not adapt. They do not show that REM protects a live agent, and they do not rank REM against any published defense. Their value is narrower and, within its bounds, firm: a transparent instance of a widely proposed design was built, compared fairly with the simplest alternatives, and found to be no better than them on the evidence available at the tool boundary. Where an improvement was observed, it came from a deterministic rule and not from the learned, consequence-aware decision that the thesis set out to evaluate. The thesis reports that result as it was measured.
