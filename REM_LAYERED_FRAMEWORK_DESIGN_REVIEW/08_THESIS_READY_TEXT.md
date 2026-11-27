# 08: Thesis-ready text [PD]

**How to use this text.**
- These are proposed passages. Insert them only after the supervisor reviews them.
- They are consistent with `REM_FINAL_SCIENTIFIC_RECONCILIATION_2026_11_28/02` and `04`.
- Citations use the verified records in `09`. Where a work was read only at abstract level, the text says "report" or "describe".

---

## A. Related Work: layered defenses for LLM systems and agents (Chapter 2)

Layered defenses against prompt injection have been proposed for systems that protect different targets, and their layers do different work. Several frameworks protect language-model applications and retrieval-augmented chatbots. PromptGuard combines input gatekeeping, structured prompt formatting, semantic output validation and response refinement (Alzahrani, 2026). A three-layer framework for RAG chatbots screens user input, enforces a provenance-based instruction hierarchy during context assembly so that retrieved content cannot override operator policy, and audits model output (Saleem et al., 2026, preprint). A five-layer framework for local models in air-gapped networks, grounded in MITRE ATLAS, compares a policy-approved initial intent with the trajectory of observed events, including tool calls and their arguments (Jang et al., 2026/2027). Spotlight-Guard layers spotlighting, LLM-based detection and quarantine, and HMAC-based instruction integrity, and reports a component ablation and an adaptive attack (Demirol & Aydoğan, 2026). These works protect the text that a model reads or writes; none of them, at the level described in their abstracts, authorizes the arguments of a state-changing tool call.

A second group protects tool-using agents at, or before, the tool-call boundary. NEXUS monitors an agent's structured plan before tool execution and chooses among allow, block, request confirmation and request revision by combining deterministic rules, argument-level inspection and a calibrated logistic-regression risk score (Hossain et al., 2026). Progent enforces symbolic privilege policies over tool names and arguments deterministically (Shi et al., preprint). Agent-Sentry bounds an agent's executions by combining a classifier over action sequences and argument provenance with a provenance-aware allow-list and an LLM judge for residual cases (Sequeira et al., preprint). MELON detects indirect injection by re-executing the agent with a masked user prompt and comparing the resulting tool calls (Zhu et al., 2025). CaMeL replaces the agent's control flow with a planner, a quarantined parser and an interpreter that propagates capabilities (Debenedetti et al., preprint). In the financial domain, AIS separates model inference from execution authority, validating a typed financial intent against mandate, policy and exact economic terms before issuing single-use authority (Gong et al., 2026).

Two recent studies question how such layered defenses are evaluated. A record-level audit of CASCADE, a layered defense for the Model Context Protocol, shows that the convention by which "review" verdicts are counted, and the construction of the test corpus, determine the reported false-positive rate (Abasıkeleş-Turgut & Gümüş, preprint). A study of a layered gateway shows that deleting a stage and substituting its verdicts attribute contributions very differently (Abasıkeleş Turgut & Gümüş, preprint). Neither concerns financial agents, but both bear directly on how the contribution of a layer should be measured.

## B. Architecture justification (Chapter 3)

REM places its controls at the tool-call boundary of an opaque banking agent. The boundary is where an induced financial action becomes a concrete call with concrete arguments, and where it can still be withheld.

**Trust boundary.** REM labels every context segment as trusted (system prompt), semi-trusted (user request) or untrusted (tool output). Derived content inherits the least-trusted label of its inputs, and no processing promotes content to a more trusted label. The action evidence compares each sensitive argument with these segments. The principle that untrusted content must not acquire the authority of an instruction is shared with instruction-hierarchy and capability-based designs (Saleem et al.; Debenedetti et al.); REM applies it to the arguments of proposed actions rather than to prompt assembly.

**Detection, decision and authorization.** REM separates the estimation of whether a proposed call was induced by injected content from the choice of an intervention. It does not authorize actions: it has no representation of what the user permitted beyond whether a recipient appears in the request. This distinguishes REM from defenses that enforce deterministic rules or policies on arguments (NEXUS, Progent, CaMeL) and from financial authority separation (AIS), and it explains why its evidence cannot separate an authorized payment from an unrequested one whose details appear in the user's own words.

**Enforcement.** The Mitigation layer is realized as a gateway in front of the tool backend: withheld calls never reach it, and any failure during evaluation withholds the call. In a deployment simulation on 3,334 recorded episodes, the gateway reproduced the in-process replay exactly. It has not been operated with a live agent.

## C. Research gap (Chapter 1 / Chapter 2)

Layered defenses for language-model applications and tool-using agents are numerous, and several combine content inspection, behavioral or provenance evidence, risk scoring, graduated interventions and enforcement. Substantial prior-art overlap therefore exists for every component of REM and for layered combinations of them. Among the works reviewed, most of which were read at abstract level, the evidence on whether such layering provides defense in depth for a financial agent is limited: layers are usually evaluated by deleting them, a practice recent work shows can misattribute contributions, and few evaluations distinguish removing a component from suppressing it while the others remain. This thesis addresses that evidence gap for one layered framework on an executable banking benchmark, and claims no architectural novelty.

## D. Discussion (Chapter 4 / Chapter 5)

Compared with the frameworks reviewed, REM's evaluation shows where its layering provides protection and where it does not. Its protection depends on enforcement and on the learned decision, and within that decision on two evidence families that cover different attack classes. Its content detector and its deterministic predicates showed no measurable effect. Defenses that authorize arguments independently of a model, as in Progent's policies or AIS's execution authority, address the limitation that REM's evidence cannot cross. In this thesis's own exploratory studies, however, deriving such authorization from natural-language requests failed on requests phrased in new ways. The audit of CASCADE and the study of deletion-based ablation in a layered gateway support the methodological lesson of this thesis: a defense's layer count, and the contributions found by deleting layers, are not evidence of defense in depth. Each component's contribution must be measured under conditions in which the other components are present, and the conventions behind each reported number must be stated.

## E. Future work (Chapter 5)

1. **Canonical identifiers and field-level provenance.** Compare canonical identifiers and record the source field of every value, so that reformatted identifiers and free-text fields do not weaken the provenance evidence (as in ROPE's origin labels). This must be evaluated by paired replay on the existing populations.
2. **Model-independent authorization of financial arguments.** Authorize recipient, amount and operation from a trusted authorization channel, in the manner of Progent's policies or AIS's typed financial intents, and evaluate it on requests written by others and with live agents.
3. **A reviewer for Escalate.** Evaluate the four-verdict design with a human reviewer under an approved protocol, including well-formed forged payment details.
4. **Economic limits.** Add per-call, per-payee and cumulative limits, evaluated on financial scenarios that the benchmark does not contain.
5. **Adaptive and closed-loop evaluation.** Evaluate every component against an agent that reacts to refusals and against adaptive attacks, separating closed-loop from replay results.
6. **Component reachability.** Test whether each component's verdicts can reach an outcome by substituting constant verdicts, in addition to removal.
