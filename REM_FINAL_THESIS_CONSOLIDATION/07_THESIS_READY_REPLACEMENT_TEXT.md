# 07: Thesis-ready replacement and insertion text

**Base text.** The humanized edition (`REM_HUMANIZED_THESIS/src`, unchanged). The DiD insertions are merged by context (§1.1).

**How this file relates to the working copy.**
- §1 lists **exactly** what `thesis_working_copy/tools/make_working_copy.py` applied. It is generated from `audit/edit_log.json` by `make_07.py`.
- Each entry gives the location, the existing anchor and the complete new text.
- §2 holds text that is **not applied** because it needs a supervisor decision first.
- Numbers are unchanged; the working copy re-verifies 498 Chapter 4 table cells with 0 mismatches.

## 1. Applied in the working copy

### 1.1 DiD-edition insertions (merged unchanged; reconciliation 03, M1–M4)

| Edit | Location | Source text |
|---|---|---|
| `M-02-1` | Ch. 2 new §2.11.6 and Table 2.6 | `REM_DID_THESIS_EDITION/src/CHAPTER_02_FINAL.md` lines 559–585 |
| `M-03-1` | Ch. 3 new §3.15 (REM-DiD, proposed, not adopted), Table 3.16, Figure 3.5; the summary becomes §3.16 | DiD Ch. 3 lines 912–947 |
| `M-04-1` | Ch. 4 new §4.6.12 (exploratory DiD evaluation), Tables 4.60–4.61; the summary becomes §4.6.13 | DiD Ch. 4 lines 2033–2106 |
| `M-05-1` | Ch. 5 §5.5, paragraph "Not confirmed | resilient Defense-in-Depth": DiD Ch. 5 lines 89–90 |
| `M-05-2` | Ch. 5 §5.7, Future Work item 14 | DiD Ch. 5 line 123 |

Two edits then qualify the inserted text (`M1a`, `M1b`, `R4-9a`, `R4-9b`, below).

### 1.2 Edits

#### `M1a` · Chapter 2 · 2.11.6 Update of 27 November 2026: Defense-in-Depth and Authorization Prior Art (Outside the PRISMA Flow)

- **Kind:** replace
- **Existing text or anchor:** «| AgentSandbox (K. Zhang et al., 2025; preprint) |»
- **Reason:** Reconciliation 03, merge item M1: the peer-reviewed layered precedent must be listed; the "not found" statement is qualified by the substitution study
- **Changes scientific meaning?** No (adds a precedent; narrows a claim)
- **References:** Demirol & Aydoğan (2026); Abasıkeleş Turgut & Gümüş (2026b)
- **New text:**

> | Spotlight-Guard (Demirol & Aydoğan, 2026; *Applied Sciences*) | A | Spotlighting-based input isolation, an LLM detection-and-quarantine pipeline and HMAC-based instruction integrity, in one layered defense for agents that read tool content | Reports a component ablation that isolates each layer, an adaptive-attack evaluation and benign-task success, on locally hosted 7B-class models; not a financial agent |
> | AgentSandbox (K. Zhang et al., 2025; preprint) |

#### `M1b` · Chapter 2 · 2.11.6 Update of 27 November 2026: Defense-in-Depth and Authorization Prior Art (Outside the PRISMA Flow)

- **Kind:** replace
- **Existing text or anchor:** «- What was not found, at the level read, is a measurement of how much protection remains when one control is evaded while the others stay in place, as distinct from removing it. Section 4.6.12 reports such a measurement for REM. The statement is bounded by the abstract-level reading.»
- **Reason:** Reconciliation 03, merge item M1: the peer-reviewed layered precedent must be listed; the "not found" statement is qualified by the substitution study
- **Changes scientific meaning?** No (adds a precedent; narrows a claim)
- **References:** Demirol & Aydoğan (2026); Abasıkeleş Turgut & Gümüş (2026b)
- **New text:**

> - What was not found, at the level read, is a measurement of how much protection remains when one control is evaded while the others stay in place, as distinct from removing it. Section 4.6.12 reports such a measurement for REM. The statement is bounded by the abstract-level reading. The closest measurement found later replaces the verdicts of one stage of a layered tool-call gateway by constants (Abasıkeleş Turgut & Gümüş, 2026b; Section 2.11.7); it concerns verdict substitution in one stage of a Model Context Protocol gateway, not suppression of an evidence family for a financial agent.

#### `R4-9a` · Chapter 4 · 4.6.12 Exploratory Defense-in-Depth Evaluation (27 November 2026)

- **Kind:** replace
- **Existing text or anchor:** «- In this replay, REM-DiD reaches Defense-in-Depth in the sense that independent controls protect when authorization is bypassed.»
- **Reason:** Reconciliation 04, R4-9: the inserted DiD interpretation rested on oracle or broad authorization
- **Changes scientific meaning?** Yes: corrects an overclaim (residual coverage, not deployable defense in depth)
- **References:** —
- **New text:**

> - In this replay, with authorization bypassed by a broad envelope, REM-DiD's remaining controls stopped every replayed attack, individually reducing attacks and jointly removing them. The authorization itself was issued by an oracle or modelled as bypassed, so this shows residual coverage of the remaining controls, not defense in depth of a deployable system.

#### `R4-9b` · Chapter 4 · 4.6.12 Exploratory Defense-in-Depth Evaluation (27 November 2026)

- **Kind:** replace
- **Existing text or anchor:** «- **Removing a control and evading it can therefore give opposite assessments.**»
- **Reason:** Reconciliation 04, R4-9: the inserted DiD interpretation rested on oracle or broad authorization
- **Changes scientific meaning?** Yes: corrects an overclaim (residual coverage, not deployable defense in depth)
- **References:** —
- **New text:**

> - **Removing a control and evading it can therefore give opposite assessments.**
> - These evasion results concern REM v1.0 itself and are used in Sections 4.5.10 and 4.5.12 to qualify the removal-based ablation. The suppression is idealized: it sets a family's features to their not-fired values on attack-labeled calls and does not model how an attacker would achieve this.

#### `R1-1` · Chapter 1 · 1.2 Problem Statement

- **Kind:** replace
- **Existing text or anchor:** «The problem addressed in this thesis is the runtime compromise of tool-using financial agents through indirect prompt injection. The thesis designs a decision layer at the action boundary and evaluates it on recorded agent behavior in a banking environment, against threshold and rule baselines.»
- **Reason:** Reconciliation 04, R1-1: states the problem as whether layering yields defense in depth (the researcher's topic) [PD]
- **Changes scientific meaning?** Framing only; no result changes
- **References:** —
- **New text:**

> The problem addressed in this thesis is the runtime compromise of tool-using financial agents through indirect prompt injection, and the question of whether a layered defense at the action boundary actually protects in depth. Such defenses are commonly organized as several layers (content inspection, behavioral analysis, action evidence, a risk-informed decision and enforcement), but layering is a property of the design, whereas defense in depth is a property of the protection: it holds only if more than one component contributes protection and the loss of one is covered by another. The thesis designs such a five-layer framework, REM, and evaluates on recorded agent behavior in a banking environment which of its components actually carry protection, at what cost to legitimate financial work, and how it compares with threshold and simple rule baselines.

#### `R1-2a` · Chapter 1 · 1.4 Research Gap

- **Kind:** replace
- **Existing text or anchor:** «- **NEXUS** is a structured-plan safety monitor that applies a formal intervention policy to choose among allow, block, request confirmation and request revision. It combines deterministic rules, argument-level inspection and a calibrated logistic-regression risk score (Hossain et al., 2026).»
- **Reason:** Reconciliation 04, R1-2: NEXUS publication status and reading levels
- **Changes scientific meaning?** No (accuracy of status)
- **References:** Hossain et al. (2026)
- **New text:**

> - **NEXUS**, published in the Findings of IJCNLP-AACL 2026, is a structured-plan safety monitor that applies a formal intervention policy to choose among allow, block, request confirmation and request revision. It combines deterministic rules, argument-level inspection and a calibrated logistic-regression risk score, and its abstract reports a comparison with rule-only intervention selection on non-financial benchmarks (Hossain et al., 2026). It is the closest published analogue of REM's Decision Engine.

#### `R1-2b` · Chapter 1 · 1.4 Research Gap

- **Kind:** replace
- **Existing text or anchor:** «The systematic review of Chapter 2 was conducted at record level in September 2026. Six of the papers above were read in full in November 2026, outside that review (Chapter 2, Section 2.11.4), and the Progent paper (version 3) on 16 November 2026. NEXUS is known from its abstract and its authors' repository documentation; its full text was not read.»
- **Reason:** Reconciliation 04, R1-2: NEXUS publication status and reading levels
- **Changes scientific meaning?** No (accuracy of status)
- **References:** Hossain et al. (2026)
- **New text:**

> The systematic review of Chapter 2 was conducted at record level in September 2026. Six of the papers above were read in full in November 2026, outside that review (Chapter 2, Section 2.11.4), and the Progent paper (version 3) on 16 November 2026. NEXUS is a peer-reviewed publication; its full text was not read, and statements about it rest on its abstract and its authors' repository documentation. Several later works with layered or authorization-based designs (Chapter 2, Sections 2.11.4, 2.11.6 and 2.11.7) are known only from their abstracts. Substantial prior-art overlap therefore exists for every component of REM and for layered combinations of them, and this thesis does not claim an architectural or mechanism novelty. The review is not exhaustive, and no claim is made that every possible combination has been published.

#### `C-GAP1` · Chapter 1 · 1.4 Research Gap

- **Kind:** replace
- **Existing text or anchor:** «> Runtime defenses for tool-using agents now combine risk scoring, provenance and graduated interventions, and their authors report benchmark-specific fitting and unmeasured intervention effectiveness. Limited controlled evidence establishes whether a learned, consequence-aware runtime decision adds value over simple provenance and authorization rules for a banking agent when both the user task an […]»
- **Reason:** Final research gap (04): narrowed after the abstract-level evidence of Saleem et al., Spotlight-Guard, NEXUS and BARBICAN [PD]
- **Changes scientific meaning?** Yes: narrows the gap statement
- **References:** Saleem et al. (2026); Demirol & Aydoğan (2026); Hossain et al. (2026); Abasıkeleş Turgut & Gümüş (2026b)
- **New text:**

> > Layered runtime defenses against indirect prompt injection, combining content inspection, provenance-aware, behavioral, learned and rule-based controls, have been proposed and, in several cases, ablated layer by layer. Among the studies examined, most of them at abstract level, the evidence remains limited on three questions for a financial agent acting on an executable banking benchmark: which components of such a defense actually carry its protection, and whether removing a component and suppressing its evidence at test time lead to the same assessment; whether a learned, consequence-aware decision adds value over simple deterministic rules on the same proposed financial calls; and what the measured protection costs in legitimate financial task completion, including against a reference that executes no state-changing call.

#### `C-GAP1b` · Chapter 1 · 1.4 Research Gap

- **Kind:** replace
- **Existing text or anchor:** «Within these limits, the gap this thesis addresses is one of **evidence** (Chapter 2, Section 2.11.5):»
- **Reason:** Final research gap (04): narrowed after the abstract-level evidence of Saleem et al., Spotlight-Guard, NEXUS and BARBICAN [PD]
- **Changes scientific meaning?** Yes: narrows the gap statement
- **References:** Saleem et al. (2026); Demirol & Aydoğan (2026); Hossain et al. (2026); Abasıkeleş Turgut & Gümüş (2026b)
- **New text:**

> Within these limits, the gap this thesis addresses is one of **evidence** (Chapter 2, Sections 2.11.5 and 2.11.7):

#### `R1-3` · Chapter 1 · 1.5 Research Aim

- **Kind:** replace
- **Existing text or anchor:** «The aim of this research is to design a runtime evaluation and mitigation framework for the security of financial AI agents, to evaluate it against adversarial attacks, and to compare it with existing security approaches.»
- **Reason:** Reconciliation 04, R1-3: proposed evaluation focus, kept separate from the objective-derived aim [PD]
- **Changes scientific meaning?** Framing only
- **References:** —
- **New text:**

> The aim of this research is to design a runtime evaluation and mitigation framework for the security of financial AI agents, to evaluate it against adversarial attacks, and to compare it with existing security approaches.
>
> *Proposed focus, pending the supervisor's confirmation.* Within this aim, the evaluation focuses on one question: whether the framework's five-layer organization produces defense in depth, that is, which of its components contribute protection against indirect prompt injection, what that protection costs in legitimate task completion, and how it compares with simple deterministic rules.

#### `R1-5` · Chapter 1 · 1.11 Contributions: Proposed and Demonstrated

- **Kind:** insert before
- **Existing text or anchor:** «**What the thesis demonstrates**, with the evidence for each item (Chapter 5, Table 5.3 gives the precedent, code, experiment, result and limits of each):»
- **Reason:** Reconciliation 04, R1-5: primary empirical contribution (05 A)
- **Changes scientific meaning?** States the contribution precisely; no new result
- **References:** —
- **New text:**

> **Primary empirical contribution.** The thesis examines whether REM's five-layer architecture produces defense in depth, rather than assuming that it does. On recorded AgentDojo banking traces, protocol-frozen paired component-level ablations and an exploratory comparison of removal with test-time suppression show that it does so only narrowly. Enforcement and the combined learned scoring-and-decision pathway are each necessary for the measured protection. That protection rests on two evidence families that cover different attack classes: action/provenance evidence, whose removal measurably lowers the withholding of attack calls on one population, and behavioral evidence, which under modelled suppression is the only evidence that stops the credential-change objective. Context detection and the deterministic predicates show no measurable effect. The protection is obtained with low specificity: on the primary population, REM v1.0 completes exactly the benign tasks that withholding every state-changing call completes. All results are replay results on data examined during development.

#### `R1-6a` · Chapter 1 · 1.11 Contributions: Proposed and Demonstrated

- **Kind:** replace
- **Existing text or anchor:** «3. **Measured security and its cost.** In replay, REM v1.0 reduces attack success from 22.6% to 0.4% on the primary recordings and from 21.1% to 0.15% on the second population. It completes 31% of benign tasks where the undefended agent completes 52% (Chapter 4, Sections 4.6.3 and 4.6.8).»
- **Reason:** Reconciliation 04, R1-6: "accounts for all 661" and "every outcome effect" are overclaims; adds the P1 withhold-all identity
- **Changes scientific meaning?** Yes: corrects overclaims
- **References:** —
- **New text:**

> 3. **Measured security and its cost.** In replay, REM v1.0 reduces attack success from 22.6% to 0.4% on the primary recordings and from 21.1% to 0.15% on the second population. It completes 31% of benign tasks where the undefended agent completes 52%. On the primary recordings, the 105 benign tasks it completes are exactly those completed when every state-changing call is withheld, so in replay it completes no benign task that requires a payment, payment change or credential change. It completes 94 more tasks under attack than that reference and lets 11 attacks through, all in one task whose request names the attacker's account. This identity is established on the primary recordings only (Chapter 4, Sections 4.6.3 and 4.6.8).

#### `C-NEG1` · Chapter 1 · 1.11 Contributions: Proposed and Demonstrated

- **Kind:** replace
- **Existing text or anchor:** «Four are documented (Chapter 5, Section 5.5): behavioral evidence did not help;»
- **Reason:** Qualifies a negative result with the exploratory suppression result
- **Changes scientific meaning?** Qualifies a claim
- **References:** —
- **New text:**

> Four are documented (Chapter 5, Section 5.5): behavioral evidence, when removed and refitted, did not help (under exploratory test-time suppression it was the only evidence that stopped the credential-change objective; Chapter 4, Section 4.6.12);

#### `R1-6b` · Chapter 1 · 1.11 Contributions: Proposed and Demonstrated

- **Kind:** replace
- **Existing text or anchor:** «8. **Pre-registered ablations of the five layers and a comparison with existing frameworks (19 to 22 November 2026).** With protocols committed before scoring, the ablation shows where REM v1.0's protection comes from. The learned decision accounts for all 661 attacks that REM v1.0 prevents (of 672 reached without defense) and admits none, at a measurable cost in completed tasks. Calibration, cont […]»
- **Reason:** Reconciliation 04, R1-6: "accounts for all 661" and "every outcome effect" are overclaims; adds the P1 withhold-all identity
- **Changes scientific meaning?** Yes: corrects overclaims
- **References:** —
- **New text:**

> 8. **Protocol-frozen component-level ablations within the layered architecture, and a comparison with existing frameworks (19 to 22 November 2026).** With protocols committed before any arm was scored, on recordings that had been examined during development, the ablations show how REM v1.0's protection is produced:
>    - enforcement and the combined learned pathway (estimator, calibration and expected-loss selection, removed together) are each necessary: without either, attack outcomes return to the no-defense level;
>    - on the primary population, removing calibration alone changes no attack outcome, and replacing expected-loss selection by consequence-independent thresholds raises successful attacks from 11 to 164;
>    - removing the action/provenance evidence lowers attack-call withholding measurably on the second population (−9.1 points, 95% interval −23.5 to −0.7) and increases the episodes in which an attack call is executed, while its effect on final attack outcomes is not resolved on any population;
>    - removing behavioral evidence raises task completion with no measured security change, whereas suppressing it at test time (exploratory) lets the credential-change objective succeed;
>    - context detection, the predicates and Modify show no measurable effect;
>    - provenance labelling and the Detection layer's classifier could not be ablated (the first is a dependency of later features, the second does not exist), and the context-hygiene step was not exercised by the recorded data.
>
>    The four defenses distributed with the benchmark are compared descriptively through their authors' recorded runs. Progent's published banking policy, decided by its authors' code on the same episodes, admits no attack and completes more tasks than REM; its list of permitted recipients is specific to the benchmark. DRIFT and MELON are compared at the level of architecture and code only (Chapter 4, Sections 4.4, 4.5 and 4.6.12).

#### `A2-ch1` · Chapter 1 · 1.11 Contributions: Proposed and Demonstrated

- **Kind:** replace
- **Existing text or anchor:** «- that the tested features establish what the user authorized;»
- **Reason:** A2 (review 05): REM does not authorize; layer count is not evidence of depth
- **Changes scientific meaning?** No (documentation)
- **References:** —
- **New text:**

> - that the tested features establish what the user authorized, or that REM authorizes actions: it estimates and decides, and holds no representation of what the user permitted (Chapter 3, Section 3.2.2);
> - that the number of layers, or the contributions found by removing them, is by itself evidence of defense in depth;

#### `A7` · Chapter 2 · 2.11.7 Update of 28 November 2026: Layered Defenses and How Their Layers Are Evaluated (Outside the PRISMA Flow) (new)

- **Kind:** insert before
- **Existing text or anchor:** «## 2.12 Chapter Summary»
- **Reason:** A7 and review 08-A: related work on layered defenses and on how layers are evaluated
- **Changes scientific meaning?** No (documentation; narrows the gap)
- **References:** Alzahrani (2026); Saleem et al. (2026); Jang et al. (2027); Demirol & Aydoğan (2026); Hossain et al. (2026); T. Shi et al. (2026); Sequeira et al. (2026); Zhu, Yang, et al. (2025); Debenedetti et al. (2025); Gong et al. (2026); Abasıkeleş-Turgut & Gümüş (2026a, 2026b)
- **New text:**

> ### 2.11.7 Update of 28 November 2026: Layered Defenses and How Their Layers Are Evaluated (Outside the PRISMA Flow)
>
> *Status of this addition.* The bibliographic records of the works below were verified through Crossref and OpenAlex on 28 November 2026. Their full texts could not be opened from the working environment, so every statement is at abstract level (A), except where Table 2.3 records a full-text (F) or repository (R) reading. No count of the review changes.
>
> **Layered defenses for language-model applications.** Several frameworks protect the text that a model reads or writes. PromptGuard combines input gatekeeping, structured prompt formatting, semantic output validation and response refinement (Alzahrani, 2026). A three-layer framework for retrieval-augmented chatbots screens user input, enforces a provenance-based instruction hierarchy during context assembly so that retrieved content cannot override operator policy, and audits model output; its abstract reports an ablation in which the three layers provide complementary protection (Saleem et al., 2026, preprint). A five-layer framework for local models in air-gapped networks compares a policy-approved initial intent with the trajectory of observed events, including tool calls and their arguments (Jang et al., 2027). Spotlight-Guard layers spotlighting, LLM-based detection and quarantine, and HMAC-based instruction integrity, and reports a component ablation, an adaptive attack and benign-task success (Demirol & Aydoğan, 2026). At the level of their abstracts, none of these works authorizes the arguments of a state-changing financial tool call.
>
> **Layered defenses at the tool-call boundary.** NEXUS chooses among allow, block, request confirmation and request revision by combining deterministic rules, argument-level inspection and a calibrated logistic-regression risk score, and reports a comparison with rule-only intervention selection (Hossain et al., 2026). Progent enforces symbolic privilege policies over tool names and arguments deterministically (T. Shi et al., 2026). Agent-Sentry layers three checks: a classifier over action sequences and argument provenance, a deterministic allow-list over sensitive argument values, and an LLM judge for residual cases (Sequeira et al., 2026). MELON compares the tool calls of the agent with those of a re-execution under a masked user prompt (Zhu, Yang, et al., 2025). CaMeL separates control flow from untrusted data and propagates capabilities (Debenedetti et al., 2025). In the financial domain, AIS separates model inference from execution authority and validates a typed financial intent against mandate, policy and exact economic terms before single-use authority is issued (Gong et al., 2026).
>
> **How layers are evaluated.** Two recent studies of the same group question how the contribution of a layer is measured. A record-level audit of CASCADE, a local layered defense for the Model Context Protocol, reports that the convention by which "review" verdicts are counted, and the construction of the test corpus, determine the headline false-positive rate (Abasıkeleş-Turgut & Gümüş, 2026a). A study of a four-tier gateway for tool calls reports that deleting one stage credits it with contributions that differ by more than an order of magnitude depending on how deletion is defined, whereas substituting constant verdicts shows that the stage can change only a few inputs (Abasıkeleş Turgut & Gümüş, 2026b). Neither concerns financial agents. Both bear directly on how this thesis measures the contribution of REM's components: they are independent evidence that deletion-based ablation of a layered prompt-injection defense can misattribute contributions, which supports, but does not prove, the removal-versus-suppression finding of Chapter 4, Section 4.6.12.
>
> **What this update changes.**
> - A component- or layer-level ablation of a layered injection defense is published (Saleem et al., 2026; Demirol & Aydoğan, 2026), as is a comparison of a calibrated risk score with rule-only selection (Hossain et al., 2026). Neither is a gap.
> - The methodological point that deletion and substitution of a layer can disagree is published for a tool-call gateway (Abasıkeleş Turgut & Gümüş, 2026b). This thesis does not claim it.
> - What remains, at the level read, is narrower: evidence for a financial agent on an executable banking benchmark on which of a layered defense's components carry its protection, whether removing an evidence family and suppressing it at test time agree, and what the protection costs in legitimate financial task completion. The statement of Section 2.11.5 is narrowed accordingly, and Chapter 1, Section 1.4 uses the narrowed wording. It remains proposed wording, pending the supervisor's confirmation.

#### `C-GAP2` · Chapter 2 · 2.11.5 Revised statement of the research gap

- **Kind:** insert after
- **Existing text or anchor:** «**Bounds.** The gap is bounded by the record-level review, by the absence of a systematic search after 30 October 2026, and by the abstract-level knowledge of three close works. Three preprints of November 2026 (PACT, ROPE and CapLite; Section 2.11.4) check tool arguments against the request or agai»
- **Reason:** Final research gap (04): narrowed after the abstract-level evidence of Saleem et al., Spotlight-Guard, NEXUS and BARBICAN [PD]
- **Changes scientific meaning?** Yes: narrows the gap statement
- **References:** Saleem et al. (2026); Demirol & Aydoğan (2026); Hossain et al. (2026); Abasıkeleş Turgut & Gümüş (2026b)
- **New text:**

> **Further narrowing (28 November 2026).** Layer-level ablations of layered injection defenses and a comparison of a calibrated risk score with rule-only selection are reported at abstract level by later works (Section 2.11.7). The statement above is therefore narrowed in Section 2.11.7 to the evidence on which components carry protection for a financial agent, on removal against test-time suppression, and on the cost in legitimate financial task completion.

#### `C-GAP3` · Chapter 2 · 2.12 Chapter Summary

- **Kind:** replace
- **Existing text or anchor:** «Only the controlled evaluation, including its negative results, is offered by this thesis.»
- **Reason:** Final research gap (04): narrowed after the abstract-level evidence of Saleem et al., Spotlight-Guard, NEXUS and BARBICAN [PD]
- **Changes scientific meaning?** Yes: narrows the gap statement
- **References:** Saleem et al. (2026); Demirol & Aydoğan (2026); Hossain et al. (2026); Abasıkeleş Turgut & Gümüş (2026b)
- **New text:**

> Only the controlled evaluation, including its negative results, is offered by this thesis. A further update of 28 November 2026 (Section 2.11.7) narrowed the gap to which components of a layered defense carry protection for a financial agent, how removal and test-time suppression compare, and at what cost in legitimate financial task completion.

#### `A1` · Chapter 3 · 3.4.2 Provenance labeling

- **Kind:** insert after
- **Existing text or anchor:** «Each context segment receives one label from the ordered set trusted (system prompt) ≻ semi-trusted (user input) ≻ untrusted (tool output, retrieved content, memory). Content derived from several segments inherits the least-trusted label among them, and processing never promotes content to a more tr»
- **Reason:** A1 (review 05): where the trust boundary acts
- **Changes scientific meaning?** No (documentation)
- **References:** Saleem et al. (2026); Debenedetti et al. (2025)
- **New text:**

> **Where the trust boundary acts.** The labels are not used to filter or rewrite content. They are consumed by the action evidence x^act^~1~–x^act^~3~, by x^beh^~1~ and, through x^act^~1~, by predicate D2 (Sections 3.6.2 and 3.7.4), which compare the arguments of the proposed call with the trusted, semi-trusted and untrusted segments. REM therefore applies the principle that untrusted content must not acquire the authority of an instruction at the arguments of proposed actions, at boundary TB-3 of Table 3.3, and not during prompt assembly. The same principle appears as a provenance-based instruction hierarchy for retrieval-augmented chatbots (Saleem et al., 2026) and as capabilities attached to values (Debenedetti et al., 2025).

#### `A2` · Chapter 3 · 3.2.2 Topology and information flow

- **Kind:** insert after
- **Existing text or anchor:** «The inputs and outputs of each layer are listed in Appendix A. The four functions are separated architecturally: Layers 2 and 3 produce evidence and issue no verdicts; Layer 4 performs probability estimation and decision; Layer 5 performs mitigation.»
- **Reason:** A2 (review 05): detection, decision and authorization separated
- **Changes scientific meaning?** No (documentation)
- **References:** T. Shi et al. (2026); Debenedetti et al. (2025); Hossain et al. (2026); Gong et al. (2026)
- **New text:**

> **Detection, decision and authorization.** REM estimates whether a proposed call was induced by injected content (Layers 2–4), decides among four verdicts (Layer 4), and enforces the verdict (Layer 5). It does not authorize actions: it holds no representation of what the user permitted beyond whether a key argument of the call also occurs in the user's request or in trusted content (x^act^~1~). This distinguishes REM from defenses that enforce deterministic rules or policies on tool arguments, such as Progent (T. Shi et al., 2026), CaMeL (Debenedetti et al., 2025) and the rule component of NEXUS (Hossain et al., 2026), and from the separation of execution authority from model inference proposed for financial agents (Gong et al., 2026). It is also why REM's evidence cannot distinguish an authorized payment from an unrequested one whose details appear in the user's own words (Chapter 4, Section 4.6.7).

#### `A4` · Chapter 3 · 3.6.2 Behavioral and action evidence

- **Kind:** insert after
- **Existing text or anchor:** «3. **The feature set is frozen after pilot E0** (Section S-3.11.8), before any held-out predictions are examined.»
- **Reason:** A4 (review 05): dependencies and complementarity of the evidence families
- **Changes scientific meaning?** No (documentation)
- **References:** —
- **New text:**

> **Dependencies among the evidence families.** The families are not independent inputs. The action features x^act^~1~–x^act^~3~ depend on the provenance labels and entities of Layer 1, and predicate D2 depends on x^act^~1~; x^beh^~1~ depends on those labels and on the Detection Layer's indicator x^ctx^~2~. Removing an upstream component therefore also changes the features built on it, which is why the Input & Context layer cannot be ablated on its own (Chapter 4, Section 4.5.4). In the evaluation the families covered different attack classes: the action/provenance evidence carried most of the estimator's discrimination, while, under test-time suppression, the behavioral evidence was the only evidence against the credential-change objective, which has no recipient for the action evidence to examine (Chapter 4, Sections 4.5.7 and 4.6.12).

#### `A3` · Chapter 3 · 3.8 Mitigation Layer

- **Kind:** insert after
- **Existing text or anchor:** «4. **Retries are observed.** A restricted or blocked agent may retry. Retries raise x^beh^~2~, and calls to restricted tools are refused by the Mitigation Layer.»
- **Reason:** A3 (review 05): enforcement point (gateway)
- **Changes scientific meaning?** No (documentation)
- **References:** `rem/deployment/gateway.py`
- **New text:**

> **Enforcement point.** The Mitigation Layer is also implemented as an HTTP gateway in front of the tool backend (`rem/deployment/gateway.py`). The agent framework sends each proposed call to the gateway, which runs Layers 1–5 and forwards only released calls; withheld calls never reach the backend. The gateway fails closed: an exception while a call is evaluated withholds the call, and an unknown episode or a malformed request is rejected without executing anything. A deployment simulation that sent the recorded episodes through the gateway to a simulated banking backend reproduced the in-process replay exactly (Chapter 4, Section 4.5.7). The gateway has not been operated with a live agent or a real payment system, and the simulation inherits the non-adaptive assumption of the replay (Section 3.11.9).

#### `A5` · Chapter 3 · 3.16 Chapter Summary

- **Kind:** insert before
- **Existing text or anchor:** «**Implementation.** The specification is implemented with one declared absence, the injection classifier, and is verified by 278 tests, by replay fidelity checks and by exact re-execution. No live-agent experiment was executed. Security effectiveness, within the limits of recorded-trace replay, is t»
- **Reason:** A5 (review 05): implemented vs conceptual controls
- **Changes scientific meaning?** No (documentation)
- **References:** —
- **New text:**

> Table 3.17 states the status of every control, so that implemented, evaluated and merely specified controls are not confused.
>
> **Table 3.17. Implementation status of the controls of REM v1.0** (I = implemented; E = evaluated with a measured outcome; X = implemented, not exercised by the recorded data; S = specified, not implemented)
>
> | Control | Layer | Status | What the evaluation shows (Chapter 4) |
> |---|---|---|---|
> | Provenance labels with least-trusted inheritance | Input & Context | I; evaluated only through the features built on it | Not removable on its own (Section 4.5.4) |
> | Context hygiene | Input & Context | X | Not exercised (Section 4.5.5) |
> | Instruction-pattern indicator x^ctx^~2~ | Detection | I, E | No measurable effect (Section 4.5.7) |
> | Injection classifier x^ctx^~1~ | Detection | S | Not available (Section 3.5) |
> | Behavioral evidence x^beh^~1~–x^beh^~4~ | Behavioral Analysis | I, E | Removal: lower completion, no measured security change; suppression (exploratory): only evidence against the credential-change objective (Sections 4.5.7, 4.6.12) |
> | Action evidence x^act^~1~–x^act^~3~ | Behavioral Analysis | I, E | Carries most of the discrimination; removal lowers attack-call withholding on the second population (Section 4.5.7) |
> | Estimator, calibration and expected-loss verdict (learned pathway) | Decision Engine | I, E | Necessary for the measured protection; calibration alone changes no attack outcome (Section 4.5.7) |
> | Consequence tiers and costs | Decision Engine | I, E; declared values awaiting approval | Thresholds without tiers admit more attacks and complete more tasks (Section 4.5.7) |
> | Predicates D1, D2 | Decision Engine | I, E | No measurable effect (Section 4.5.7) |
> | Audit record and linear attribution | Decision Engine (audit only) | I | Attribution never enters the verdict (Section 3.7.6) |
> | Step-level withholding (Modify, Escalate, Block) | Mitigation | I, E | Necessary; without it REM equals no defense (Section 4.5.7) |
> | Modify mechanism (tool restriction) | Mitigation | I; effect equal to withholding in replay | No distinct effect exercised (Section 4.5.7) |
> | HTTP gateway, fail-closed | Mitigation | I; deployment simulation on recorded traffic | Exact parity with the replay (Section 4.5.7) |
> | Reviewer for Escalate | Outside REM | Not part of REM; bounded by an idealized reviewer and by no reviewer | Section 4.6.3 |
> | Sequential (CUSUM) monitor | Observe-only analysis | I; never in the verdict path | Held-out false-alarm rate above its fitting target (Section 4.6.4) |
> | Live, closed-loop enforcement | — | Harness implemented and tested with scripted agents; not executed with a language model | Section S-4.4.4 |

#### `R4-1a` · Chapter 4 · 4.5.1 Introduction

- **Kind:** replace
- **Existing text or anchor:** «The study therefore removes components, not always whole layers:»
- **Reason:** Reconciliation 04 (R4-1 to R4-8): component-level wording, data history, joint production of protection
- **Changes scientific meaning?** Yes: corrects overclaims; no number changes
- **References:** —
- **New text:**

> The study is therefore a **component-level ablation within a layered architecture**: it removes components, not whole layers:

#### `R4-1b` · Chapter 4 · 4.5.1 Introduction

- **Kind:** replace
- **Existing text or anchor:** «- **Decision Engine:** every component removed separately.»
- **Reason:** Reconciliation 04 (R4-1 to R4-8): component-level wording, data history, joint production of protection
- **Changes scientific meaning?** Yes: corrects overclaims; no number changes
- **References:** —
- **New text:**

> - **Decision Engine:** the learned pathway (estimator, calibration and expected-loss selection) is removed as one block, because no non-predicate verdict exists without the estimator; the estimator is therefore never isolated. On the primary population only, calibration is removed separately, expected-loss selection is replaced by consequence-independent thresholds on the same estimator, and Modify and the predicates are removed separately.

#### `R4-2` · Chapter 4 · 4.5.3 Experimental Design

- **Kind:** replace
- **Existing text or anchor:** «- *Status:* development evidence, because the primary recordings were used to design and fit REM v1.0.»
- **Reason:** Reconciliation 04 (R4-1 to R4-8): component-level wording, data history, joint production of protection
- **Changes scientific meaning?** Yes: corrects overclaims; no number changes
- **References:** —
- **New text:**

> - *Status and data history:* these are **protocol-frozen paired ablations**, not validations on untouched data. The primary recordings were used to design and fit REM v1.0, and the outcomes of six arms on them had been reported before the protocol of 21 November was frozen; the held-out-template recordings were examined in revision R2; the second population has been development data since the confirmatory run of 11 November 2026. The protocols were committed before any arm was scored (commits `dc8407d` and `93e6630`), and the repository's history and hashes support that order.

#### `R4-3` · Chapter 4 · Decision Engine in detail: the final ablation of 19 November 2026

- **Kind:** replace
- **Existing text or anchor:** «- accounts for all 661 attacks that REM v1.0 prevents (of 672 reached without defense).

What it does not do»
- **Reason:** Reconciliation 04 (R4-1 to R4-8): component-level wording, data history, joint production of protection
- **Changes scientific meaning?** Yes: corrects overclaims; no number changes
- **References:** —
- **New text:**

> - is necessary for the prevention of 661 of the 672 attacks reached without defense: removing the pathway returns the attack outcomes to the no-defense level, while the predicates alone withhold no attack-labeled call. It is not the sole cause of that prevention: it decides on the action/provenance and behavioral evidence it is given, and it protects nothing without enforcement (Sections 4.5.10 and 4.6.12).
>
> What it does not do

#### `A3-ch4` · Chapter 4 · Tool-call enforcement and runtime

- **Kind:** insert after
- **Existing text or anchor:** «**Runtime.** REM calls no model. Its complete per-call processing took a median of 0.149 ms (95th percentile 0.404 ms) over 6,684 calls, against 0.119 ms (0.367 ms) without the learned decision, in one CPU container during replay. These are replay timings, not deployment measurements.»
- **Reason:** A3 (review 05): documents the existing gateway and its deployment simulation
- **Changes scientific meaning?** No (documents existing evidence)
- **References:** `results/deployment_sim/2026-11-05_full/RESULTS.md`
- **New text:**

> **Enforcement through a gateway (deployment simulation of 5 November 2026).** The Mitigation layer is also implemented as a fail-closed HTTP gateway at the tool boundary (Chapter 3, Section 3.8). All 3,334 recorded episodes were sent through it to a simulated banking backend, as recorded traffic without adaptation. For REM, B1 and the no-defense reference, the per-call verdicts and the utility and security outcomes matched the in-process replay in every episode; the backend executed exactly the released calls; malformed and unknown requests were rejected without execution; and the median REM time per call was 0.19 ms (95th percentile 0.40 ms) on four virtual CPUs (`results/deployment_sim/2026-11-05_full/RESULTS.md`). The simulation ran at commit `c30ad8a`, before the last change to `rem/` (commit `7c79883`); its outcomes equal those of the replay reported here, which was re-executed with the current code on 27 November 2026. It simulates enforcement on recorded traffic; it is not an operation with a live agent or a real payment system.

#### `A6` · Chapter 4 · 4.3.3 Evaluation Metrics

- **Kind:** insert after
- **Existing text or anchor:** «**A released attack-labeled call is not the same as a committed unauthorized change of the bank state.** The label marks an attempt (Section 4.2.1). The effect of a released call on the state is not measured separately from the benchmark's security check. Earlier drafts headed this column "unauthori»
- **Reason:** A6 (review 05): reporting conventions
- **Changes scientific meaning?** No (documentation)
- **References:** Abasıkeleş-Turgut & Gümüş (2026a)
- **New text:**

> **Reporting conventions.** The headline numbers of a layered defense depend on how its verdicts are mapped to outcomes and on the population on which they are counted (Abasıkeleş-Turgut & Gümüş, 2026a). Four conventions therefore hold for every number in this chapter. First, Modify, Escalate and Block all withhold the current call, and an escalated call is released only where an idealized reviewer is stated. Second, each number names its population and that population's data history (Section 4.2.1). Third, each rate states its denominator: attacked episodes, benign episodes, attack-labeled calls or legitimate state-changing calls. Fourth, each number states which outcome it measures: the benchmark's attack outcome in replay, the execution of an attack-labeled call, or call-level withholding. These outcomes need not agree (Section 4.5.7).

#### `R4-4` · Chapter 4 · 4.5.10 Discussion

- **Kind:** insert after
- **Existing text or anchor:** «They therefore add probability mass to legitimate calls without separating attacks. The protection they might add is already provided by the provenance evidence. Removing them releases 50 more legitimate calls and completes 35 more benign tasks, with the same attack count.»
- **Reason:** Reconciliation 04 (R4-1 to R4-8): component-level wording, data history, joint production of protection
- **Changes scientific meaning?** Yes: corrects overclaims; no number changes
- **References:** —
- **New text:**

> This is a result of removal and refitting. Suppressing the behavioral family at test time, with everything else fixed, gives a different picture (Section 4.6.12, exploratory): 131 instead of 11 successful attacks, 119 of the 120 additional ones in the only credential-change objective, which has no recipient for the action evidence to examine. After the family is removed, suppressing the action evidence lets 653 attacks succeed, against 90 when the behavioral family is present. Removal and suppression therefore lead to opposite assessments of this family; the suppression is modelled and idealized.

#### `R4-5` · Chapter 4 · Results

- **Kind:** insert before
- **Existing text or anchor:** «**Table 4.48. Replay ASR by the attacker's target action** (`r2_breakdowns.json`)»
- **Reason:** Reconciliation 04 (R4-1 to R4-8): component-level wording, data history, joint production of protection
- **Changes scientific meaning?** Yes: corrects overclaims; no number changes
- **References:** —
- **New text:**

> **Benign completion and the withhold-everything reference (primary population only).** A re-analysis of the stored per-episode records of the exploratory evaluation of Section 4.6.12 compares REM v1.0 with a reference arm in which no state-changing call is executed. On the primary population, the 105 benign episodes that REM v1.0 completes are exactly the 105 that the reference completes: no episode differs in either direction. REM v1.0 completes 94 more episodes under attack than the reference (1,083 against 989), and the reference has no successful attack where REM v1.0 has 11, all in user_task_15. In replay, REM v1.0's benign completion is therefore the completion attainable without any state change. This was established on the primary population only; no such reference arm exists for the other populations. These are replay quantities, not the performance of an agent that reacts to refusals.

#### `R4-6a` · Chapter 4 · 4.5.12 Conclusion of the Ablation Study

- **Kind:** replace
- **Existing text or anchor:** «| Decision Engine | Learned decision | All of REM's attack prevention and most of its false blocking |»
- **Reason:** Reconciliation 04 (R4-1 to R4-8): component-level wording, data history, joint production of protection
- **Changes scientific meaning?** Yes: corrects overclaims; no number changes
- **References:** —
- **New text:**

> | Decision Engine | Learned pathway (estimator, calibration, expected loss; removed as one block) | Necessary for the prevention of 661 of 672 attacks on the primary population, and for nearly all prevention on the others; carries most of the false blocking; not the sole cause (it acts on the evidence below and through enforcement) |

#### `R4-6b` · Chapter 4 · 4.5.12 Conclusion of the Ablation Study

- **Kind:** replace
- **Existing text or anchor:** «| Behavioral Analysis | Behavioral evidence | Lowers completed tasks with no measurable security effect |»
- **Reason:** Reconciliation 04 (R4-1 to R4-8): component-level wording, data history, joint production of protection
- **Changes scientific meaning?** Yes: corrects overclaims; no number changes
- **References:** —
- **New text:**

> | Behavioral Analysis | Behavioral evidence | Removal: lowers completed tasks with no measured security change. Test-time suppression (exploratory): the only evidence that stops the credential-change objective |

#### `R4-6c` · Chapter 4 · 4.5.12 Conclusion of the Ablation Study

- **Kind:** replace
- **Existing text or anchor:** «| Input & Context | – (not isolatable; hygiene not exercised) | Indirectly, through the action/provenance evidence |»
- **Reason:** Reconciliation 04 (R4-1 to R4-8): component-level wording, data history, joint production of protection
- **Changes scientific meaning?** Yes: corrects overclaims; no number changes
- **References:** —
- **New text:**

> | Input & Context | Provenance labelling (not removable); hygiene (not exercised) | Contributes through the action/provenance evidence built on its labels: removing that evidence lowers attack-call withholding on the second population (−9.1 points [−23.5, −0.7]); effect on final attack outcomes not resolved |

#### `R4-6d` · Chapter 4 · 4.5.12 Conclusion of the Ablation Study

- **Kind:** replace
- **Existing text or anchor:** «**Which components showed measurable contributions.** On this benchmark, the components that do the work are:
- the learned decision;
- its expected-loss rule;
- the action/provenance evidence, built on the Input & Context labels;
- enforcement.»
- **Reason:** Reconciliation 04 (R4-1 to R4-8): component-level wording, data history, joint production of protection
- **Changes scientific meaning?** Yes: corrects overclaims; no number changes
- **References:** —
- **New text:**

> **Which components showed measurable contributions.** On this benchmark, protection is produced jointly by enforcement, the learned pathway, and the two evidence families the pathway consumes: action/provenance evidence, built on the Input & Context labels, and, under test-time suppression, behavioral evidence. Context detection, the predicates, calibration and Modify show no measurable effect. The architecture therefore has depth only within the evidence that one decision and one enforcement point use; the Detection layer and the predicates contribute no measured protection, and the Input & Context layer contributes only through the action evidence built on its labels. This is a finding about the evaluated configuration on replayed recordings, not grounds by itself for removing any layer.

#### `R4-7a` · Chapter 4 · What the evidence supports

- **Kind:** replace
- **Existing text or anchor:** «| 14 | Of REM's five layers, the Decision Engine's learned decision acting through the Mitigation layer's enforcement carries every measured outcome effect; the action/provenance evidence carries the discrimination; behavioral evidence lowers task completion; the Detection layer's indicator, the predicates, calibration and Modify have no measurable effect |»
- **Reason:** Reconciliation 04 (R4-1 to R4-8): component-level wording, data history, joint production of protection
- **Changes scientific meaning?** Yes: corrects overclaims; no number changes
- **References:** —
- **New text:**

> | 14 | Of REM's five layers, enforcement and the learned pathway are each necessary for the measured outcome effects; the action/provenance evidence carries most of the discrimination and measurably raises attack-call withholding on one population; behavioral evidence lowers task completion when removed but covers one attack class under test-time suppression (exploratory); the Detection layer's indicator, the predicates, calibration and Modify have no measurable effect |

#### `R4-7b` · Chapter 4 · What the evidence supports

- **Kind:** replace
- **Existing text or anchor:** «the Input & Context layer is not isolatable and the injection classifier is absent; no measurable effect is not evidence of no value |»
- **Reason:** Reconciliation 04 (R4-1 to R4-8): component-level wording, data history, joint production of protection
- **Changes scientific meaning?** Yes: corrects overclaims; no number changes
- **References:** —
- **New text:**

> the Input & Context layer is not isolatable and the injection classifier is absent; no measurable effect is not evidence of no value; protocol-frozen, on data examined during development; the estimator is not isolated; suppression is modelled |

#### `R4-8` · Chapter 4 · 4.6.13 Chapter Summary

- **Kind:** replace
- **Existing text or anchor:** «- **Ablation of the five layers (19 and 21 November 2026, pre-registered).** The learned decision of the Decision Engine accounts for all 661 attacks that REM v1.0 prevents (of 672 reached without defense) and admits none, at a cost of 22.5 points of benign utility. Only enforcement by the Mitigation layer turns its verdicts into outcomes: in shadow mode the same verdicts protect nothing. The acti […]»
- **Reason:** Reconciliation 04 (R4-1 to R4-8): component-level wording, data history, joint production of protection
- **Changes scientific meaning?** Yes: corrects overclaims; no number changes
- **References:** —
- **New text:**

> - **Component-level ablation within the layered architecture (19 and 21 November 2026, protocol-frozen; data examined during development).** Enforcement and the learned pathway (estimator, calibration and expected-loss selection, removed together) are each necessary: without either, attack outcomes return to the no-defense level, and in shadow mode the same verdicts protect nothing. The pathway acts on two evidence families. Removing the action/provenance evidence lowers attack-call withholding on the second population and raises the number of episodes in which an attack call is executed; its effect on final outcomes is not resolved. Removing behavioral evidence raises task completion with no measured security change, but suppressing it at test time lets the credential-change objective succeed (exploratory). The Detection layer's indicator, the predicates, calibration and Modify have no measurable effect; provenance labelling could not be removed on its own and the classifier does not exist. On the primary population, the consequence-aware rule admits 153 fewer attacks than consequence-independent thresholds and completes fewer tasks, and REM v1.0's benign completions coincide with those of withholding every state-changing call.

#### `T1` · Chapter 4 · EXPERIMENTAL RESULTS AND DISCUSSION

- **Kind:** replace
- **Existing text or anchor:** «the pre-registered ablations of 19 and 21 November»
- **Reason:** "Pre-registered" overstates what the record supports (protocols committed before scoring; no formal pre-registration)
- **Changes scientific meaning?** Yes: removes an overstatement; no result changes
- **References:** —
- **New text:**

> the protocol-frozen ablations of 19 and 21 November

#### `T2` · Chapter 4 · Protocol

- **Kind:** replace
- **Existing text or anchor:** «The **pre-registered values** are listed in Table 4.4.»
- **Reason:** "Pre-registered" overstates what the record supports (protocols committed before scoring; no formal pre-registration)
- **Changes scientific meaning?** Yes: removes an overstatement; no result changes
- **References:** —
- **New text:**

> The **values declared in advance** (committed before any held-out prediction was computed) are listed in Table 4.4.

#### `T3` · Chapter 4 · Protocol

- **Kind:** replace
- **Existing text or anchor:** «**Table 4.4. Pre-registered values**»
- **Reason:** "Pre-registered" overstates what the record supports (protocols committed before scoring; no formal pre-registration)
- **Changes scientific meaning?** Yes: removes an overstatement; no result changes
- **References:** —
- **New text:**

> **Table 4.4. Values declared in advance**

#### `T4` · Chapter 4 · 4.2.2 Labels, the user_task_15 Collision and Benchmark Versions

- **Kind:** replace
- **Existing text or anchor:** «All results above use the pre-registered label rule»
- **Reason:** "Pre-registered" overstates what the record supports (protocols committed before scoring; no formal pre-registration)
- **Changes scientific meaning?** Yes: removes an overstatement; no result changes
- **References:** —
- **New text:**

> All results above use the label rule declared in advance

#### `T5` · Chapter 4 · Decision Engine in detail: the final ablation of 19 November 2026

- **Kind:** replace
- **Existing text or anchor:** «The following report is that of the pre-registered study of 19 November 2026.»
- **Reason:** "Pre-registered" overstates what the record supports (protocols committed before scoring; no formal pre-registration)
- **Changes scientific meaning?** Yes: removes an overstatement; no result changes
- **References:** —
- **New text:**

> The following report is that of the protocol-frozen study of 19 November 2026.

#### `T6` · Chapter 4 · Exploratory redesign studies of 18–19 November 2026 (not adopted)

- **Kind:** replace
- **Existing text or anchor:** «Each study pre-registered its rules, but all used development data»
- **Reason:** "Pre-registered" overstates what the record supports (protocols committed before scoring; no formal pre-registration)
- **Changes scientific meaning?** Yes: removes an overstatement; no result changes
- **References:** —
- **New text:**

> Each study committed its rules before scoring, but all used development data

#### `T7` · Chapter 4 · 4.6.2 RQ2 — Observe-Only Decisions

- **Kind:** replace
- **Existing text or anchor:** «where the pre-registered costs put the Allow–Block indifference points»
- **Reason:** "Pre-registered" overstates what the record supports (protocols committed before scoring; no formal pre-registration)
- **Changes scientific meaning?** Yes: removes an overstatement; no result changes
- **References:** —
- **New text:**

> where the declared costs put the Allow–Block indifference points

#### `T8` · Chapter 4 · 4.6.5 Realized Loss across the Declared Grid

- **Kind:** replace
- **Existing text or anchor:** «because the pre-registered α~mod~ = 0.05 must exceed α~blk~»
- **Reason:** "Pre-registered" overstates what the record supports (protocols committed before scoring; no formal pre-registration)
- **Changes scientific meaning?** Yes: removes an overstatement; no result changes
- **References:** —
- **New text:**

> because the declared α~mod~ = 0.05 must exceed α~blk~

#### `T9` · Chapter 3 · 3.11.7 Configurations, baselines, and ablations

- **Kind:** replace
- **Existing text or anchor:** «A separately pre-registered study (Chapter 4, Section 4.5.7)»
- **Reason:** "Pre-registered" overstates what the record supports (protocols committed before scoring; no formal pre-registration)
- **Changes scientific meaning?** Yes: removes an overstatement; no result changes
- **References:** —
- **New text:**

> A separate protocol-frozen study (Chapter 4, Section 4.5.7)

#### `T10` · Appendices · Appendix B: Register of Open Supervisor Decisions

- **Kind:** replace
- **Existing text or anchor:** «NO-GO under its own pre-registered rules»
- **Reason:** "Pre-registered" overstates what the record supports (protocols committed before scoring; no formal pre-registration)
- **Changes scientific meaning?** Yes: removes an overstatement; no result changes
- **References:** —
- **New text:**

> NO-GO under its own rules, committed before scoring

#### `C5-1` · Chapter 5 · 5.2 Answers to the Research Questions

- **Kind:** replace
- **Existing text or anchor:** «pre-registered ablations of the five layers with paired intervals on three populations»
- **Reason:** Chapter 5 consistency with the corrected Chapter 4 (reconciliation 03, consequential edits)
- **Changes scientific meaning?** Yes: corrects overclaims
- **References:** —
- **New text:**

> protocol-frozen component-level ablations within the five-layer architecture, with paired intervals on three populations

#### `C5-2` · Chapter 5 · 5.2 Answers to the Research Questions

- **Kind:** replace
- **Existing text or anchor:** «the learned decision accounts for all 661 prevented attacks (of 672 reached without defense)»
- **Reason:** Chapter 5 consistency with the corrected Chapter 4 (reconciliation 03, consequential edits)
- **Changes scientific meaning?** Yes: corrects overclaims
- **References:** —
- **New text:**

> the learned pathway is necessary for the prevention of 661 of the 672 attacks reached without defense

#### `C5-3` · Chapter 5 · 5.2 Answers to the Research Questions

- **Kind:** replace
- **Existing text or anchor:** «Across the five layers, every measured outcome effect comes from the Decision Engine's learned decision acting through the Mitigation layer's enforcement: in shadow mode the same verdicts protect nothing.»
- **Reason:** Chapter 5 consistency with the corrected Chapter 4 (reconciliation 03, consequential edits)
- **Changes scientific meaning?** Yes: corrects overclaims
- **References:** —
- **New text:**

> Across the five layers, protection is produced jointly: enforcement and the learned pathway are each necessary, and the pathway acts on two evidence families that cover different attack classes (action/provenance evidence and, under test-time suppression, behavioral evidence); in shadow mode the same verdicts protect nothing.

#### `C5-4` · Chapter 5 · 5.2 Answers to the Research Questions

- **Kind:** replace
- **Existing text or anchor:** «Behavioral evidence lowered task completion with no measured security benefit;»
- **Reason:** Chapter 5 consistency with the corrected Chapter 4 (reconciliation 03, consequential edits)
- **Changes scientific meaning?** Yes: corrects overclaims
- **References:** —
- **New text:**

> Behavioral evidence, when removed and refitted, lowered task completion with no measured security benefit (under exploratory test-time suppression it was the only evidence that stopped the credential-change objective);

#### `C5-5` · Chapter 5 · 5.4 Contributions

- **Kind:** replace
- **Existing text or anchor:** «| 9. A pre-registered final ablation of REM v1.0»
- **Reason:** Chapter 5 consistency with the corrected Chapter 4 (reconciliation 03, consequential edits)
- **Changes scientific meaning?** Yes: corrects overclaims
- **References:** —
- **New text:**

> | 9. A protocol-frozen final ablation of REM v1.0

#### `C5-6` · Chapter 5 · 5.4 Contributions

- **Kind:** replace
- **Existing text or anchor:** «| 10. A layer-to-implementation mapping and a component-level ablation of the five-layer design,»
- **Reason:** Chapter 5 consistency with the corrected Chapter 4 (reconciliation 03, consequential edits)
- **Changes scientific meaning?** Yes: corrects overclaims
- **References:** —
- **New text:**

> | 10. A layer-to-implementation mapping and a protocol-frozen component-level ablation within the five-layer architecture,

#### `C5-7` · Chapter 5 · 5.4 Contributions

- **Kind:** replace
- **Existing text or anchor:** «| Every outcome effect from the learned decision acting through enforcement (shadow mode equals no defense);»
- **Reason:** Chapter 5 consistency with the corrected Chapter 4 (reconciliation 03, consequential edits)
- **Changes scientific meaning?** Yes: corrects overclaims
- **References:** —
- **New text:**

> | Enforcement and the learned pathway each necessary (shadow mode equals no defense), with protection produced jointly with the two evidence families the pathway consumes;

#### `C5-8` · Chapter 5 · 5.8 Conclusion

- **Kind:** replace
- **Existing text or anchor:** «Two pre-registered ablations settle where REM v1.0's own protection comes from.»
- **Reason:** Chapter 5 consistency with the corrected Chapter 4 (reconciliation 03, consequential edits)
- **Changes scientific meaning?** Yes: corrects overclaims
- **References:** —
- **New text:**

> Two protocol-frozen ablations show where REM v1.0's own protection comes from.

#### `C5-9` · Chapter 5 · 5.8 Conclusion

- **Kind:** replace
- **Existing text or anchor:** «it decides almost every call and accounts for all 661 attacks that REM v1.0 stops (of 672 reached without defense), with none admitted.»
- **Reason:** Chapter 5 consistency with the corrected Chapter 4 (reconciliation 03, consequential edits)
- **Changes scientific meaning?** Yes: corrects overclaims
- **References:** —
- **New text:**

> it decides almost every call and is necessary for the prevention of 661 of the 672 attacks reached without defense, with none admitted.

#### `C5-10` · Chapter 5 · 5.8 Conclusion

- **Kind:** replace
- **Existing text or anchor:** «Across the five layers, every measured outcome effect comes from that decision acting through enforcement.»
- **Reason:** Chapter 5 consistency with the corrected Chapter 4 (reconciliation 03, consequential edits)
- **Changes scientific meaning?** Yes: corrects overclaims
- **References:** —
- **New text:**

> Across the five layers, that protection is produced jointly by enforcement, the learned pathway and the two evidence families it consumes; on the primary population, REM v1.0 completes exactly the benign tasks that withholding every state-changing call completes.

#### `C5-11` · Chapter 5 · 5.6 Limitations and Threats to Validity

- **Kind:** replace
- **Existing text or anchor:** «9. **Literature.** The systematic review was conducted at record level.»
- **Reason:** Chapter 5 consistency with the corrected Chapter 4 (reconciliation 03, consequential edits)
- **Changes scientific meaning?** Yes: corrects overclaims
- **References:** —
- **New text:**

> 9. **Literature.** The systematic review was conducted at record level. The layered and authorization-based works added on 27 and 28 November 2026 (Chapter 2, Sections 2.11.6 and 2.11.7) are known only from their abstracts and bibliographic records; their full texts could not be opened from the working environment.

#### `FW` · Chapter 5 · 5.7 Future Work, in Order of Priority

- **Kind:** insert after
- **Existing text or anchor:** «14. **REM-DiD under adaptive attack.** Run the Defense-in-Depth candidate of Section 3.15 with live agents and an adaptive attacker (Narisetty et al., 2026). Use a trusted approval interface in place of the oracle authorization, and a benchmark with currency, source-account and approval parameters.»
- **Reason:** Future work B2, B5 and B7 of review 05 (not implemented)
- **Changes scientific meaning?** No
- **References:** Abasıkeleş Turgut & Gümüş (2026b)
- **New text:**

> 15. **Field-level provenance.** Record the source field of every value in a tool output, so that a typed bank field and a free-text field are not treated alike, and evaluate the effect by paired replay on the existing populations.
> 16. **Economic limits.** Add per-call, per-payee and cumulative limits, evaluated on financial scenarios that the benchmark does not contain (amount escalation to a trusted recipient, split transfers). The limit values are a supervisor decision.
> 17. **Component reachability by substitution.** Test whether each component's verdicts can reach an outcome by replacing them with constant verdicts, in addition to removing the component (Abasıkeleş Turgut & Gümüş, 2026b). Table 4.34 reports this for the learned decision only.

#### `AB-1` · Abstract (English) · Abstract

- **Kind:** replace
- **Existing text or anchor:** «and only 33 of 178 legitimate state-changing calls were released.»
- **Reason:** Abstract consistency with the corrected Chapters 1 and 4
- **Changes scientific meaning?** Yes: corrects overclaims
- **References:** —
- **New text:**

> and only 33 of 178 legitimate state-changing calls were released. On these episodes the benign tasks it completed were exactly those completed when every state-changing call is withheld.

#### `AB-2` · Abstract (English) · Abstract

- **Kind:** replace
- **Existing text or anchor:** «showed with paired intervals that the learned decision accounts for all 661 attacks that REM stops (672 succeed without any defense) and admits none.»
- **Reason:** Abstract consistency with the corrected Chapters 1 and 4
- **Changes scientific meaning?** Yes: corrects overclaims
- **References:** —
- **New text:**

> showed with paired intervals that the learned decision is necessary for the prevention of 661 of the 672 attacks that succeed without any defense, and admits none.

#### `AB-3` · Abstract (English) · Abstract

- **Kind:** replace
- **Existing text or anchor:** «Every outcome effect came from the learned decision acting through enforcement: in shadow mode the same verdicts protected nothing. Removing the action/provenance evidence let more attack calls execute,»
- **Reason:** Abstract consistency with the corrected Chapters 1 and 4
- **Changes scientific meaning?** Yes: corrects overclaims
- **References:** —
- **New text:**

> Enforcement and the learned decision were each necessary, and the decision acted on two evidence families that covered different attack classes: in shadow mode the same verdicts protected nothing, removing the action/provenance evidence let more attack calls execute, and suppressing the behavioral evidence at test time (exploratory) let the credential-change objective succeed,

#### `AB-4` · Abstract (English) · Abstract

- **Kind:** replace
- **Existing text or anchor:** «A final ablation, committed before scoring,»
- **Reason:** Abstract consistency with the corrected Chapters 1 and 4
- **Changes scientific meaning?** Yes: corrects overclaims
- **References:** —
- **New text:**

> A final ablation, with its protocol committed before scoring,

#### `AB-5` · Abstract (Arabic) · Abstract

- **Kind:** replace
- **Existing text or anchor:** «أن القرار المتعلَّم مسؤول عن منع جميع الهجمات الـ661 التي يوقفها الإطار (من أصل 672 هجوماً تنجح دون أي دفاع)»
- **Reason:** Abstract consistency with the corrected Chapters 1 and 4
- **Changes scientific meaning?** Yes: corrects overclaims
- **References:** —
- **New text:**

> أن القرار المتعلَّم ضروري لمنع 661 من أصل 672 هجوماً تنجح دون أي دفاع

#### `AB-6` · Abstract (Arabic) · Abstract

- **Kind:** replace
- **Existing text or anchor:** «أن كل أثر مقيس في النتائج يأتي من القرار المتعلَّم وهو يعمل من خلال التنفيذ في طبقة التخفيف.»
- **Reason:** Abstract consistency with the corrected Chapters 1 and 4
- **Changes scientific meaning?** Yes: corrects overclaims
- **References:** —
- **New text:**

> أن التنفيذ في طبقة التخفيف والقرار المتعلَّم ضروريان كلاهما، وأن القرار يعتمد على عائلتين من الأدلة تغطيان فئتين مختلفتين من الهجمات؛ إذ أدّى كبت الأدلة السلوكية وقت الاختبار (تحليل استكشافي) إلى نجاح هدف تغيير بيانات الاعتماد.

### 1.3 References added

- Gong, H., Samawi, M., & Medda, F. (2026). Authority–inference separation in agentic financ…
- Kabbinamakki Suresh, A. K., & Gao, P. (2026). *AgentCap: Capability-based runtime authoriz…
- Mellafe Zuvic, D. (2026). *Capability gates are not authorization: Confused-deputy failure…
- Narisetty, P., Kore, S. N. B., Kattamanchi, U. K. R., & Kumarapu, J. (2026). *Adaptive eva…
- Sequeira, R. X., Damianakis, S., Iqbal, U., et al. (2026). *Agent-Sentry: Bounding LLM age…
- Zhang, K., Su, Z., Chen, P.-Y., et al. (2025). *LLM agents should employ security principl…
- Zhang, X., Cheng, Z., Liu, K., et al. (2026). *AGATE: Provenance-based runtime defense aga…
- Zhong, P. Y., Chen, S., Wang, R., et al. (2025). *RTBAS: Defending LLM agents against prom…
- Abasıkeleş-Turgut, İ., & Gümüş, E. (2026a). *Evaluating a layered prompt-injection defence…
- Abasıkeleş Turgut, İ., & Gümüş, E. (2026b). *Deletion is not substitution: Component attri…
- Alzahrani, A. (2026). PromptGuard a structured framework for injection resilient language …
- Demirol, D., & Aydoğan, M. (2026). Balancing security and performance in LLM agents: Spotl…
- Jang, S., Lee, M., & Shon, T. (2027). Intelligent multilayer defense-in-depth framework fo…
- Saleem, G., Ahmed, N., Zaman, M. I., et al. (2026). *A layered security framework against …

Full entries: `thesis_working_copy/references/REFERENCES_FINAL.md`; verification in 09.

## 2. Not applied: text that needs a supervisor decision first

### 2.1 Research questions RQ1–RQ5 [SUPERVISOR DECISION REQUIRED] (08, D2)

**Location:** Ch. 1 §1.7, the bullets RQ1–RQ4 and the paragraph after them that begins "No research question was added after the pilot." The source is reconciliation 04, R1-4. RQ5 is worded so that it does not imply non-inferiority.

**Replace the four bullets with:**

> - **RQ1 (estimation).** How well does a ridge logistic regression estimator, using provenance, context, behavioral and action evidence at the tool-call boundary, discriminate attack-induced proposed calls when whole attack objectives are held out, and how well calibrated are its probabilities under grouped cross-fitting? *Evidence:* offline classification of recorded calls (development data).
> - **RQ2 (protection and cost).** In recorded-trace replay, how do REM v1.0's attack outcomes, benign task completion and task completion under attack compare with no defense, with a consequence-independent threshold policy on the same estimator, and with simple deterministic rules; and, on the primary population, with withholding every state-changing call? *Evidence:* replay on three populations; rule baselines declared in the protocol of 11 November 2026; a re-analysis on the primary population only.
> - **RQ3 (layering and depth).** Which components of REM v1.0's layered architecture are necessary for its replay protection, and which add only cost, under protocol-frozen paired component-level ablation? *Evidence:* two protocol-frozen ablations on three populations of recordings that had been examined before.
> - **RQ4 (removal versus suppression; exploratory).** Does REM v1.0's protection persist when one evidence family is suppressed at test time rather than removed, and do the two kinds of test agree? *Evidence:* modelled suppression in replay on the primary population.
> - **RQ5 (confirmatory).** Does removing the behavioral evidence group change task completion and replay attack outcomes on recordings that had not been read before the run? *Evidence:* the confirmatory replay of 11 November 2026, with a decision rule declared before the data were opened. The security difference is reported as an interval; it is not a test of non-inferiority or equivalence.

**Replace the paragraph that follows with:**

> RQ1 and RQ2 (first three comparisons) correspond to the original RQ1 and RQ2. The original RQ3 on mitigation is answered in part under RQ2 (per-call processing time) and RQ3 (the equivalence of Modify, Escalate and Block without a reviewer). Residual attack success against an adapting agent cannot be answered with replay and is not posed. RQ3 and RQ4 refine the original RQ4. RQ5 states the question of the confirmatory evaluation reported in Chapter 4, Section 4.6.8. RQ2 (the withhold-everything comparison), RQ3 and RQ4 were posed after the pilot. The analyses that answer them were run under protocols committed before their arms were scored, on data examined during development, and are reported as such.

**Consequential renumbering:** 06 §4 lists the locations.

| Old | New |
|---|---|
| Ch. 4 §4.6.1 "RQ1" | Unchanged |
| §4.6.2 "RQ2" | Unchanged |
| §4.6.3 "RQ2 and RQ3" | "RQ2" |
| "RQ3 quantities" (Ch. 4 §4.6.3) | "Quantities of the original RQ3 (per-call time; verdict equivalence)" |

Chapter 5 table: the RQ4 row splits into RQ3 (ablation: the C5-3 wording) and RQ4 (suppression: the DiD §4.6.12 result); a new RQ5 row takes the confirmatory result now in the RQ4 row ("the gain in task completion … met the pre-declared decision rule …; the security difference is not resolved").

### 2.2 Title [SUPERVISOR DECISION REQUIRED] (08, D1)

**No text is proposed.** The printed title stays: "Runtime Evaluation and Mitigation (REM): A Security Framework for Financial AI Agents". The researcher's stated topic is "Defense in Depth for Financial AI Agents Against Indirect Prompt Injection". The working copy's content is valid under either wording (05 A). The title is in the build scripts (`TITLE` in `build_wc.py`) and in the front matter's committee page.

### 2.3 Kull wording [after source check] (08, D7)

**Location:** Ch. 3 §3.7.2, property 2: "Kull et al. (2017) prove that beta calibration with equal shape parameters equals logistic calibration applied to the log-odds of a score."

If the AISTATS paper states the identity without a proof, replace "prove" with "show". Not applied, because the full text was not read.

### 2.4 Holm citation [after source check] (08, D9)

**Location:** the DiD-inserted §3.15 ("Clustered sign-flip permutation tests with Holm correction") and §4.6.12. Add "(Holm, 1979)" and its reference entry once the JSTOR record is verified. Not applied.

