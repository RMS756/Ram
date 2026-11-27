# REM layered-framework design review: executive summary (28 November 2026)

**Scope.** A design and literature review only:
- no implementation, experiment, REM version or thesis edit;
- no new equation, score, threshold or algorithm (06);
- REM v1.0 (`rem/` tree `cd11e32…`, configuration sha256 `8e1aa107…`) and the reconciliation of commit `5d7828c` are the baseline.

**Access limits.**
- Bibliographic records of all twelve requested works were verified through Crossref and OpenAlex.
- Full texts were not reachable from this session: DNS refused for arXiv, MDPI, TechScience, Nature, ACL Anthology and doi.org; a PubMed Central request was refused by the permission system.
- Code-level evidence exists for Progent, MELON, CaMeL and ROPE.
- Every mechanism is described at the level read (`09`).

## Main findings

1. **Not all the requested frameworks protect agents.**
   - PromptGuard and the layered RAG chatbot framework protect LLM text pipelines.
   - The Multilayer DiD framework protects local LLM applications but observes agentic events.
   - The others protect tool-using agents.
   - AIS (and the payment-protocol defense A-VIP) address agents executing financial operations.
2. **Two corrections to the request:**
   - arXiv 2604.17125 is a third-party **audit** of CASCADE, not CASCADE's paper;
   - DOI 10.62762/TISC.2026.712476 is not registered with Crossref (the arXiv version 2606.19660 exists).
3. **The most useful ideas for REM are not new layers. They are:**
   - (i) the explicit separation of detection from model-independent authorization (NEXUS rules, Progent, AIS);
   - (ii) explicit trust boundaries (instruction hierarchy, capabilities), which REM **already implements** as three trust labels;
   - (iii) an external, fail-closed enforcement point, which REM **already implements** as a gateway;
   - (iv) evaluation lessons:
     - deletion-based ablation misattributes contributions (BARBICAN study);
     - decision conventions set headline metrics (CASCADE audit).

   These lessons independently support the thesis's primary contribution.
4. **REM's real gap relative to agent defenses** is that it has no model-independent argument authorization. Closing it is future research: REM's own exploratory studies found intent-compilation failures, and AgentDojo has no trusted authorization channel.

## Recommended direction

- Keep REM v1.0 unchanged as the evaluated artifact.
- Strengthen the thesis by **documenting** what REM already does (A1–A7 in 05).
- Position REM against the agent-boundary frameworks.
- Reserve B1–B7 for future work.

## Final decision report

**1. Which frameworks are genuinely designed to protect AI agents?**
- NEXUS, Progent, Agent-Sentry, MELON, CaMeL, CASCADE (MCP tool calls), Spotlight-Guard (agents receiving tool content) and AIS (financial agents).
- Also ROPE, AgentCap, AGATE, ClawGuard, CapLite, SIEVE, DRIFT and A-VIP.
- AgentDojo is the agent benchmark.

**2. Which are only general LLM/RAG security references?**
- PromptGuard and the layered RAG chatbot framework.
- The Multilayer DiD framework is an intermediate case: an LLM application that observes tool events without authorizing them.

**3. Which framework provides the most useful architectural ideas for REM?**
- **NEXUS** for the decision layer: rules, argument inspection and a calibrated risk score with four interventions, the closest analogue.
- **AIS** for the financial principle: execution authority separated from inference.
- **Progent** for deterministic argument policies.
- For evaluation, the **BARBICAN** and **CASCADE-audit** studies.

**4. Which existing REM components should be retained?** All of REM v1.0:
- provenance labels and hygiene;
- context, behavioural and action evidence;
- ridge LR, calibration, tiers, predicates and expected-loss verdict;
- step-level mitigation and the gateway;
- audit;
- CUSUM observe-only.

Components without a measured effect are retained and **reported** as such.

**5. Which responsibilities need clearer separation (in the text)?**
- Detection versus decision versus authorization, stating that REM does not authorize.
- Trust-boundary labelling versus the evidence that uses it.
- The enforcement point (gateway) versus the verdict semantics.
- Implemented versus not-exercised controls.

**6. Which additional defensive mechanisms are worth considering?**
- Canonical identifiers and field-level provenance (B1, B2).
- Model-independent financial argument authorization (B3).
- A reviewer channel (B4).
- Economic limits (B5).

**7. Which improvements need no change to the mathematical model?** All documentation items A1–A7, and B1–B5 and B7. B6 (drift signals) would bring in its source authors' scores and is future research only.

**8. Which proposals would require new experiments?** All of B1–B7. A1–A7 require none.

**9. What should remain future work?**
- B1–B7, including authorization, reviewer studies, economic limits, drift signals, information-flow control and adaptive or closed-loop evaluation.

**10. Does the evidence justify changing any part of REM v1.0?**
- **No.** No reviewed framework provides evidence, on REM's setting, that a specific change would improve it without new experiments.
- The two implementation-level candidates (B1, B2) would create a new version and need supervisor approval and paired replay.

## Recommendations by label

| Recommendation | Label |
|---|---|
| A1 Trust boundary documented | Recommended for current thesis documentation |
| A2 Detection / decision / authorization separation stated | Recommended for current thesis documentation |
| A3 Gateway enforcement documented | Recommended for current thesis documentation |
| A4 Evidence dependencies and complementarity | Recommended for current thesis documentation |
| A5 Implemented vs conceptual control table | Recommended for current thesis documentation |
| A6 Reporting conventions | Recommended for current thesis documentation |
| A7 Ablation-methodology positioning (BARBICAN, CASCADE audit) | Recommended for current thesis documentation |
| B1 Canonical identifiers | Recommended for a future REM implementation |
| B2 Field-level provenance | Recommended for a future REM implementation |
| B3 Model-independent financial authorization | Recommended for future research only |
| B4 Reviewer channel | Recommended for future research only |
| B5 Economic limits | Recommended for future research only |
| B6 Drift or trajectory signals | Recommended for future research only (under 06's conditions) |
| B7 Reachability test | Recommended for future research only |
| Output moderation / response refinement | Not recommended |
| Sixth layer | Not recommended |
| LLM judge in the decision path | Not recommended (forbidden by the design lock) |

## Files

| File | Content |
|---|---|
| 01 | Classification |
| 02 | Architecture comparison |
| 03 | Research gaps |
| 04 | Improvement matrix |
| 05 | Proposals A and B |
| 06 | Mathematical integrity audit |
| 07 | Experimental requirements |
| 08 | Thesis-ready text |
| 09 | Reference verification |
