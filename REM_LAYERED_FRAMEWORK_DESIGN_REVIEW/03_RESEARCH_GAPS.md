# 03: Research gaps in the existing frameworks

**Source separation.**
- **V** marks verified limitations: stated by the authors, or shown by their evaluation or by a third-party audit, at the level read (`09`).
- **A** marks this review's analytical observations.
- An observation about something "not reported" refers only to what was read. Several works were read only at abstract level (O).

## 1. Per framework

| Framework | Limitations: verified (V) and analytical (A) | Financial transactions? | Real tool execution protected? | Legitimate task completion measured? | Adaptive attacks? | Layers evaluated separately? | Depends on the LLM's own reasoning? | Authorization independent of the model? |
|---|---|---|---|---|---|---|---|---|
| NEXUS | **V:** the main benchmark is synthetic (128 instances); it "matches rule-only on AgentHarm due to threat-model limits"; REVISE recall 0.500 on the stress set. **A:** plan-level, so values that appear only at execution time are judged on the plan; not shown on AgentDojo | n.d. | Yes (before tool execution) | P (allow rate on IPI) | n.d. | Yes, against rule-only | No (rules + LR) | Rules: yes |
| Progent | **V:** LLM policy generation and updates are trust points; the manual banking policy is benchmark-specific (oracle allow-list), so it refuses legitimate new payees. **A:** no amount semantics unless written by hand | Banking suite | Yes | Yes | Yes | Yes (approvers) | Partly (policy generation) | Yes, once the policy exists |
| Agent-Sentry | **V:** the bound is learned from prior benign executions; figures differ across versions. **A:** new legitimate workflows fall outside the bound; the LLM judge handles residual cases | Banking suite | Yes | Yes | n.d. | n.d. | Partly (judge) | Partly (allow-list) |
| MELON | **V (code):** extra LLM calls and an external embedding model per step; runs unmodified only on older AgentDojo versions. **A:** detects attacks whose next action is independent of the user task; data-only manipulations that keep the user's action but change an argument are a weaker case | Banking suite | Yes (stops the episode) | Yes | n.d. | Yes (design ablations) | Yes | No |
| CaMeL | **V:** needs a planner LLM; programs can fail to run (reported by CapLite for small models). **A:** strong guarantees, but requires replacing the agent's control flow | Banking policy | Yes | Yes | n.d. | P | Partly | Yes (interpreter policies) |
| AgentDojo | **V:** static injection distribution; AutoDojo and Bhagwatkar et al. report that static benchmarks overestimate defenses. **A:** 8 of 9 banking injection goals share one attacker IBAN, which favours allow-lists | Simulated | — | — | Possible, not default | — | — | — |
| Multilayer DiD (CMC) | **V:** the authors limit their findings to the evaluated benchmarks, configurations and observability conditions; recall drops from 84.0% to 59.0% as intermediate events are removed; it does not lead in every attack category. **A:** a detection framework over text and events; no evidence of argument authorization on tool calls | n.d. | n.d. | FPR reported | n.d. | Yes (observability study) | Partly (embeddings) | n.d. |
| PromptGuard | **A:** protects prompt-response text; no actions. Its output refinement layer does not apply to tool calls | No | No | P | n.d. | n.d. | Partly (critic) | — |
| RAG layered framework | **V:** reports complementary layers in ablation. **A:** no actions; its "semantic drift detector" and retraining loop are learned components with drift risk | No | No | FPR reported | n.d. | Yes | Partly | — |
| CASCADE (audit) | **V (third-party audit):**<br>- the headline false-positive rate depends on how "review" is counted (11.70% vs 1.51%);<br>- 68.5% of traffic is referred to a human;<br>- corpus wrappers identify the label;<br>- the published description does not match what ran;<br>- the LLM review changes no binary outcome | n.d. | Yes (MCP) | Yes (audited) | n.d. | Audited | Partly | Partly (rules) |
| Spotlight-Guard | **V:** small local 7B models; own testbed; adaptive ASR 6.7%. **A:** content-side defence; no action authorization | n.d. | n.d. | Yes | Yes | Yes | Partly (LLM detector) | — |
| AIS | **V (S):** model-in-the-loop tests blocked legitimate requests; reservation and consumption tracking are not integrated into the EVM gate. **A:** finance-specific and model-independent at execution, but tested on its own scenarios, not an IPI benchmark | Yes | Yes | Partly | n.d. | Yes (mechanism ablations, A) | No (at execution) | Yes |

## 2. Cross-cutting gaps

| Gap | Evidence | Relevant to REM? | Does REM address it? |
|---|---|---|---|
| **G1. Layered defenses are evaluated by deleting layers; deletion can misattribute contributions** | V: BARBICAN study ("Deletion is not substitution"); the CASCADE audit | **Yes, core** | **Partly, with evidence.** REM's DiD-2 shows removal and test-time suppression disagree on one evidence family (exploratory, modelled). It does not solve the gap in general |
| **G2. Decision conventions for graded verdicts (review, escalate) change the headline metrics** | V: CASCADE audit | Yes | REM documents that Modify, Escalate and Block coincide without a reviewer. This should be stated as a reporting convention (04, D6) |
| **G3. Financial-domain argument authorization (recipient and amount) independent of the model** | V: AIS, A-VIP exist; ROPE guards recipients but not amounts | Yes | **No.** REM v1.0 has no authorization. Exploratory studies (G1/GV) tried request-derived authorization and found intent-compilation failures. Future research only |
| **G4. Static benchmarks; no adaptive evaluation** | V: AutoDojo; Zhan et al. 2025 | Yes | **No.** REM has no adaptive evaluation. It must be stated as a limitation |
| **G5. Output and information-flow protection (exfiltration through arguments)** | V: CaMeL readers; Alizadeh et al. banking exfiltration | Partly | **No.** `x_act3` (sensitive egress) is a feature, not a flow control. Outside the current threat model's evaluation |
| **G6. Human escalation exists in designs but is rarely evaluated** | V: CASCADE audit (68.5% referral); NEXUS confirm; REM has no reviewer | Yes | **No.** It must be stated as a limitation |

**Gaps outside this thesis's scope:**
- multi-agent defenses;
- training-time defenses;
- standalone-LLM jailbreaks;
- RAG-chatbot output moderation;
- MCP tool-description poisoning (unless the topic is widened).

**No claim that REM solves any gap is supported beyond what G1 states.**
