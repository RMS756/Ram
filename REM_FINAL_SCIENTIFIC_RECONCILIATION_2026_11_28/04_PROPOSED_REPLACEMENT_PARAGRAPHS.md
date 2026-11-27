# 04: Proposed replacement paragraphs for Chapters 1 and 4 [PD]

**What this file is.**
- Locations refer to the **humanized edition** sources (`REM_HUMANIZED_THESIS/src/`), the recommended base (03 §3), at the state of commit `ad81484`.
- Each item gives the location, the current text (quoted or identified by its opening words) and the proposed replacement.
- **Nothing has been applied to the thesis.**
- Numbers are taken from the stored results listed in `01_RECONCILIATION_OF_FINDINGS.md`.

## Chapter 1

### R1-1 · §1.2 Problem Statement: last paragraph (line 52)

**Current:**

> "The problem addressed in this thesis is the runtime compromise of tool-using financial agents through indirect prompt injection. The thesis designs a decision layer at the action boundary and evaluates it on recorded agent behavior in a banking environment, against threshold and rule baselines."

**Replace with:**

> The problem addressed in this thesis is the runtime compromise of tool-using financial agents through indirect prompt injection, and the question of whether a layered defense at the action boundary actually protects in depth. Such defenses are commonly organized as several layers — content inspection, behavioral analysis, action evidence, a risk-informed decision and enforcement — but layering is a property of the design, whereas defense in depth is a property of the protection: it holds only if more than one component contributes protection and the loss of one is covered by another. The thesis designs such a five-layer framework, REM, and evaluates on recorded agent behavior in a banking environment which of its components actually carry protection, at what cost to legitimate financial work, and how it compares with threshold and simple rule baselines.

### R1-2 · §1.4 Research Gap: the NEXUS bullet (line 71), the reading-status paragraph (line 78) and the gap statement (line 82)

**(a) Current NEXUS bullet** (begins "**NEXUS** is a structured-plan safety monitor…"). **Replace with:**

> - **NEXUS**, published in the Findings of IJCNLP-AACL 2026, is a structured-plan safety monitor that applies a formal intervention policy to choose among allow, block, request confirmation and request revision. It combines deterministic rules, argument-level inspection and a calibrated logistic-regression risk score (Hossain et al., 2026). It is the closest published analogue of REM's Decision Engine.

**(b) Current paragraph** (begins "The systematic review of Chapter 2 was conducted at record level…"). **Replace with:**

> The systematic review of Chapter 2 was conducted at record level in September 2026. Six of the papers above were read in full in November 2026, outside that review (Chapter 2, Section 2.11.4), and the Progent paper (version 3) on 16 November 2026. NEXUS is a peer-reviewed publication; its full text was not read, and statements about it rest on its abstract and its authors' repository documentation. Several later works with layered or authorization-based designs (Chapter 2, Sections 2.11.4 and 2.11.6) are known only from their abstracts. Substantial prior-art overlap therefore exists for every component of REM and for layered combinations of them, and this thesis does not claim an architectural or mechanism novelty. The review is not exhaustive, and no claim is made that every possible combination has been published.

**(c) Current block quote** (begins "> Runtime defenses for tool-using agents now combine…"). **Replace with:**

> > Runtime defenses for tool-using agents now combine content inspection, behavioral and provenance evidence, risk scoring and graduated interventions, and are often presented as layered. Among the works reviewed, at the levels at which they were read, limited controlled evidence establishes, for a banking agent on an executable benchmark, which components of such a layered defense actually carry its protection; whether removing a component and suppressing it at test time lead to the same assessment; and whether a learned, consequence-aware decision adds value over simple provenance and authorization rules on the same proposed calls, and at what cost in legitimate task completion.

### R1-3 · §1.5 Research Aim: second paragraph (line 90, begins "The aim of this research is…")

**Replace with:**

> The aim of this research is to design a runtime evaluation and mitigation framework for the security of financial AI agents, to evaluate it against adversarial attacks, and to compare it with existing security approaches. Within this aim, the evaluation focuses on one question: whether the framework's five-layer organization produces defense in depth, that is, which of its components contribute protection against indirect prompt injection, what that protection costs in legitimate task completion, and how it compares with simple deterministic rules.

**Note.** The first sentence is the current, objective-derived aim, unchanged. The second sentence is [PD].

### R1-4 · §1.7 Research Questions: the list (lines 106–109) and the paragraph after it (line 111)

**Replace the four bullets RQ1–RQ4 with:**

> - **RQ1 (estimation).** How well does a ridge logistic regression estimator, using provenance, context, behavioral and action evidence at the tool-call boundary, discriminate attack-induced proposed calls when whole attack objectives are held out, and how well calibrated are its probabilities under grouped cross-fitting? *Evidence:* offline classification of recorded calls (development data).
> - **RQ2 (protection and cost).** In recorded-trace replay, how do REM v1.0's attack outcomes, benign task completion and task completion under attack compare with no defense, with a consequence-independent threshold policy on the same estimator, and with simple deterministic rules; and, on the primary population, with withholding every state-changing call? *Evidence:* replay on three populations; rule baselines declared in the protocol of 11 November 2026; a re-analysis on the primary population only.
> - **RQ3 (layering and depth).** Which components of REM v1.0's layered architecture are necessary for its replay protection, and which add only cost, under protocol-frozen paired component-level ablation? *Evidence:* two protocol-frozen ablations on three populations of recordings that had been examined before.
> - **RQ4 (removal versus suppression; exploratory).** Does REM v1.0's protection persist when one evidence family is suppressed at test time rather than removed, and do the two kinds of test agree? *Evidence:* modelled suppression in replay on the primary population.
> - **RQ5 (confirmatory).** Does removing the behavioral evidence group increase task completion without a security regression on recordings unread before the run? *Evidence:* the confirmatory replay of 11 November 2026.

**Replace the paragraph that follows** (begins "No research question was added after the pilot.") **with:**

> RQ1 and RQ2(a)–(b) correspond to the original RQ1 and RQ2. The original RQ3 on mitigation is answered in part under RQ2 (per-call processing time) and RQ3 (the equivalence of Modify, Escalate and Block without a reviewer); residual attack success against an adapting agent cannot be answered with replay and is not posed. RQ3 and RQ4 refine the original RQ4. RQ5 states the question of the confirmatory evaluation reported in Chapter 4, Section 4.6.8. RQ2(d), RQ3 and RQ4 were posed after the pilot; the analyses that answer them were run under protocols committed before their arms were scored, on data examined during development, and are reported as such.

### R1-5 · §1.11 Contributions: insert a new paragraph before "**What the thesis demonstrates**" (line 178)

**Insert:**

> **Primary empirical contribution.** The thesis examines whether REM's five-layer architecture produces defense in depth, rather than assuming that it does. On recorded AgentDojo banking traces, protocol-frozen paired component-level ablations and an exploratory comparison of removal with test-time suppression show that it does so only narrowly. Enforcement and the combined learned scoring-and-decision pathway are each necessary for the measured protection. That protection rests on two evidence families that cover different attack classes: action/provenance evidence, whose removal measurably lowers the withholding of attack calls on one population, and behavioral evidence, which under modelled suppression is the only evidence that stops the credential-change objective. Context detection and the deterministic predicates show no measurable effect. The protection is obtained with low specificity: on the primary population, REM v1.0 completes exactly the benign tasks that withholding every state-changing call completes. All results are replay results on data examined during development.

### R1-6 · §1.11 Contributions: items 3 and 8 (lines 182 and 187)

**Replace item 3 with:**

> 3. **Measured security and its cost.** In replay, REM v1.0 reduces attack success from 22.6% to 0.4% on the primary recordings and from 21.1% to 0.15% on the second population. It completes 31% of benign tasks where the undefended agent completes 52%. On the primary recordings, the 105 benign tasks it completes are exactly those completed when every state-changing call is withheld, so in replay it completes no benign task that requires a payment, payment change or credential change. It completes 94 more tasks under attack than that reference and lets 11 attacks through, all in one task whose request names the attacker's account. This identity is established on the primary recordings only (Chapter 4, Sections 4.6.3 and 4.6.8).

**Replace item 8 with:**

> 8. **Protocol-frozen component-level ablations within the layered architecture, and a comparison with existing frameworks (19 to 22 November 2026).** With protocols committed before any arm was scored, on recordings that had been examined during development, the ablations show how REM v1.0's protection is produced:
>    - enforcement and the combined learned pathway — estimator, calibration and expected-loss selection, removed together — are each necessary: without either, attack outcomes return to the no-defense level;
>    - on the primary population, removing calibration alone changes no attack outcome, and replacing expected-loss selection by consequence-independent thresholds raises successful attacks from 11 to 164;
>    - removing the action/provenance evidence lowers attack-call withholding measurably on the second population (−9.1 points, 95% interval −23.5 to −0.7) and increases the episodes in which an attack call is executed, while its effect on final attack outcomes is not resolved on any population;
>    - removing behavioral evidence raises task completion with no measured security change, whereas suppressing it at test time (exploratory) lets the credential-change objective succeed;
>    - context detection, the predicates and Modify show no measurable effect;
>    - provenance labelling and the Detection layer's classifier could not be ablated (the first is a dependency of later features, the second does not exist), and the context-hygiene step was not exercised by the recorded data.
>
>    The four defenses distributed with the benchmark are compared descriptively through their authors' recorded runs. Progent's published banking policy, decided by its authors' code on the same episodes, admits no attack and completes more tasks than REM; its list of permitted recipients is specific to the benchmark. DRIFT and MELON are compared at the level of architecture and code only (Chapter 4, Sections 4.4, 4.5 and 4.6.12).

## Chapter 4

### R4-1 · §4.5.1 Introduction: the paragraph "**What can be isolated.**" and its bullet "Decision Engine: every component removed separately." (lines 851–853)

**Replace the paragraph's first sentence and the Decision Engine bullet with:**

> **What can be isolated.** The five layers are design units, not five independently removable software modules (Section 4.5.4). The study is therefore a **component-level ablation within a layered architecture**: it removes components, not whole layers.
> - **Decision Engine:** the learned pathway — estimator, calibration and expected-loss selection — is removed as one block, because no non-predicate verdict exists without the estimator; the estimator is therefore never isolated. On the primary population only, calibration is removed separately, expected-loss selection is replaced by consequence-independent thresholds on the same estimator, and Modify and the predicates are removed separately.

### R4-2 · §4.5.3 Experimental Design: the bullet "*Status:* development evidence, because the primary recordings were used to design and fit REM v1.0." (line 907)

**Replace with:**

> - *Status and data history:* these are **protocol-frozen paired ablations**, not validations on untouched data. The primary recordings were used to design and fit REM v1.0, and the outcomes of six arms on them had been reported before the protocol of 21 November was frozen; the held-out-template recordings were examined in revision R2; the second population has been development data since the confirmatory run of 11 November 2026. The protocols were committed before any arm was scored (commits `dc8407d` and `93e6630`), and the repository's history and hashes support that order.

### R4-3 · §4.5.7 Results, "Decision Engine in detail": the bullet "accounts for all 661 attacks that REM v1.0 prevents (of 672 reached without defense)." and the sentence after the list (lines 1255–1257)

**Replace the bullet with:**

> - is necessary for the prevention of 661 of the 672 attacks reached without defense: removing the pathway returns the attack outcomes to the no-defense level, while the predicates alone withhold no attack-labeled call. It is not the sole cause of that prevention: it decides on the action/provenance and behavioral evidence it is given, and it protects nothing without enforcement (Sections 4.5.10 and 4.6.12).

### R4-4 · §4.5.10 Discussion: end of the paragraph "**Why behavioral evidence lowers completion without measurable security benefit.**" (lines 1507–1511; append after line 1511)

**Append:**

> This is a result of removal and refitting. Suppressing the behavioral family at test time, with everything else fixed, gives a different picture (Section 4.6.12, exploratory): 131 instead of 11 successful attacks, 119 of the 120 additional ones in the only credential-change objective, which has no recipient for the action evidence to examine. After the family is removed, suppressing the action evidence lets 653 attacks succeed, against 90 when the behavioral family is present. Removal and suppression therefore lead to opposite assessments of this family; the suppression is modelled and idealized.

### R4-5 · §4.6.3 Replay Sensitivity Analysis: insert after Table 4.47, immediately before the caption of Table 4.48 (line 1699)

**Insert:**

> **Benign completion and the withhold-everything reference (primary population only).** A re-analysis of the stored per-episode records of the exploratory evaluation of Section 4.6.12 compares REM v1.0 with a reference arm in which no state-changing call is executed. On the primary population, the 105 benign episodes that REM v1.0 completes are exactly the 105 that the reference completes: no episode differs in either direction. REM v1.0 completes 94 more episodes under attack than the reference (1,083 against 989), and the reference has no successful attack where REM v1.0 has 11, all in user_task_15. In replay, REM v1.0's benign completion is therefore the completion attainable without any state change. This was established on the primary population only; no such reference arm exists for the other populations. These are replay quantities, not the performance of an agent that reacts to refusals.

### R4-6 · §4.5.12 Conclusion of the Ablation Study: rows of the table and the paragraph "**Which components showed measurable contributions.**" (lines 1555–1569)

**Replace the rows "Decision Engine | Learned decision", "Behavioral Analysis | Behavioral evidence" and "Input & Context" with:**

> | Decision Engine | Learned pathway (estimator, calibration, expected loss; removed as one block) | Necessary for the prevention of 661 of 672 attacks on the primary population, and for nearly all prevention on the others; carries most of the false blocking; not the sole cause (it acts on the evidence below and through enforcement) |
> | Behavioral Analysis | Behavioral evidence | Removal: lowers completed tasks with no measured security change. Test-time suppression (exploratory): the only evidence that stops the credential-change objective |
> | Input & Context | Provenance labelling (not removable); hygiene (not exercised) | Contributes through the action/provenance evidence built on its labels: removing that evidence lowers attack-call withholding on the second population (−9.1 points [−23.5, −0.7]); effect on final attack outcomes not resolved |

**Replace the paragraph "Which components showed measurable contributions." with:**

> **Which components showed measurable contributions.** On this benchmark, protection is produced jointly by enforcement, the learned pathway, and the two evidence families the pathway consumes: action/provenance evidence, built on the Input & Context labels, and — under test-time suppression — behavioral evidence. Context detection, the predicates, calibration and Modify show no measurable effect. The architecture therefore has depth only within the evidence that one decision and one enforcement point use; the Detection layer and the predicates contribute no measured protection, and the Input & Context layer contributes only through the action evidence built on its labels. This is a finding about the evaluated configuration on replayed recordings, not grounds by itself for removing any layer.

### R4-7 · §4.6.10 Interpretation, Table "What the evidence supports": row 14 (line 2015)

**Replace the claim cell of row 14 with:**

> Of REM's five layers, enforcement and the learned pathway are each necessary for the measured outcome effects; the action/provenance evidence carries most of the discrimination and measurably raises attack-call withholding on one population; behavioral evidence lowers task completion when removed but covers one attack class under test-time suppression (exploratory); the Detection layer's indicator, the predicates, calibration and Modify have no measurable effect.

**Add to its limits cell:** "protocol-frozen, on data examined during development; the estimator is not isolated; suppression is modelled".

### R4-8 · §4.6.12 Chapter Summary (renumbered §4.6.13 after the merge): the bullet "**Ablation of the five layers (19 and 21 November 2026, pre-registered).**" (line 2087)

**Replace with:**

> - **Component-level ablation within the layered architecture (19 and 21 November 2026, protocol-frozen; data examined during development).** Enforcement and the learned pathway — estimator, calibration and expected-loss selection, removed together — are each necessary: without either, attack outcomes return to the no-defense level, and in shadow mode the same verdicts protect nothing. The pathway acts on two evidence families. Removing the action/provenance evidence lowers attack-call withholding on the second population and raises the number of episodes in which an attack call is executed; its effect on final outcomes is not resolved. Removing behavioral evidence raises task completion with no measured security change, but suppressing it at test time lets the credential-change objective succeed (exploratory). The Detection layer's indicator, the predicates, calibration and Modify have no measurable effect; provenance labelling could not be removed on its own and the classifier does not exist. On the primary population, the consequence-aware rule admits 153 fewer attacks than consequence-independent thresholds and completes fewer tasks, and REM v1.0's benign completions coincide with those of withholding every state-changing call.

### R4-9 · Merged §4.6.12 (from the DiD edition): two edits to the inserted text

**(a)** In the inserted §4.6.12, the first bullet under "**Interpretation.**" currently reads: "In this replay, REM-DiD reaches Defense-in-Depth in the sense that independent controls protect when authorization is bypassed." **Replace with:**

> - In this replay, with authorization bypassed by a broad envelope, REM-DiD's remaining controls stopped every replayed attack, individually reducing attacks and jointly removing them. The authorization itself was issued by an oracle or modelled as bypassed, so this shows residual coverage of the remaining controls, not defense in depth of a deployable system.

**(b)** Add at the end of the block "**Evasion of REM v1.0's own controls.**":

> - These evasion results concern REM v1.0 itself and are used in Sections 4.5.10 and 4.5.12 to qualify the removal-based ablation. The suppression is idealized: it sets a family's features to their not-fired values on attack-labeled calls and does not model how an attacker would achieve this.
