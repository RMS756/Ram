# Deliverable 21: Journal manuscript development package (separate from the thesis)

**Working title (PI's framing):** *An Evidence-Driven Evaluation of Complementary Runtime Security Controls for Financial AI Agents Against Indirect Prompt Injection.*

## 1. Does the completed evidence support this framing?

| Element of the framing | Support | Required change |
|---|---|---|
| "Evidence-driven evaluation" | Yes: pre-registered protocols, raw records, gates, clustered statistics | — |
| "Complementary runtime security controls" | **Partly.** The controls each protect when authorization is bypassed, but are largely **redundant** (coverage Jaccard 0.84–0.99; 19 of 907 attack calls covered by one control only) | Say "layered" or "multiple" controls, and report redundancy as a finding. "Complementary" would overclaim |
| "for Financial AI Agents" | Simulated banking suite only (AgentDojo); no real financial system | "…in a Simulated Banking Agent" or "…on the AgentDojo Banking Suite" |
| "Against Indirect Prompt Injection" | Recorded attacks, non-adaptive replay | Add "under Non-Adaptive Replay" to the title or the abstract's first sentence |

**Suggested title:**
> *Removal Is Not Evasion: Measuring Layered Runtime Controls for a Banking Agent under Indirect Prompt Injection*

The subtitle names the evaluation (non-adaptive replay, AgentDojo banking).

## 2. Contribution statement (draft; [PD] until confirmed by the PI and supervisor)

1. **A measurement design.** Test-time evasion of individual controls and families, with the remaining controls fixed, distinguished from removal and refitting. Applied to a five-layer runtime mediator and to rule and authorization baselines on the same 3,313 recorded banking episodes, with failure injection under fail-safe and fail-open defaults.
2. **Findings:**
   - Removal-based ablation and evasion-based testing disagree on the same control. Refitting without the behavioral family loses no security (11 vs 11) but is 653 vs 90 under action-family evasion.
   - With authorization bypassed, four evidence controls together stop all attacks in replay, and each alone stops 92–98% (174 → 3–13). Their coverage is highly redundant.
   - Behind precise authorization, the learned consequence-aware decision adds no security and costs utility, across a 36-cell cost grid.
   - Detection signals designed as "diverse" are correlated (phi 0.92–0.98), fail together under paraphrase, and all fail under zero-width obfuscation.
3. **Artifacts:** code, protocols, raw records and hashes.

**Not claimed:**
- novelty of layered or DiD architectures, runtime mediation, capability authorization, provenance or financial constraints (AIS, AGATE, AgentCap, CaMeL, Progent);
- adaptive robustness;
- real-world banking validity.

## 3. Manuscript outline

1. Introduction: a DiD claim needs evasion evidence, not only ablation.
2. Background and related work (files 30–35, 40): layered and authorization defenses; adaptive evaluation (Narisetty et al.).
3. System under test: REM v1.0 and REM-DiD. The paper is about the measurement, not the system.
4. Threat model and evaluation design: populations, oracle authorization, modelled vs real evasion, failure injection, clustered statistics.
5. Results:
   - removal vs evasion (DiD-2);
   - detection signals (SIG-1/2);
   - controls alone and combined;
   - bypass and coverage;
   - failure injection;
   - cost grid.
6. Discussion: redundancy vs complementarity; the cost of depth; the `user_task_15` collision; when the learned layer matters.
7. Limitations: NO-ADAPT, oracle authorization, one benchmark, data reuse, no human labels.
8. Conclusion.

## 4. Gaps to close before submission (in order)

1. **Full-text check** of AgentCap, AIS, AGATE, Agent-Sentry, CaMeL and Fides for evasion-style analyses (file 35 §4). If one exists, narrow claim 2.
2. **One adaptive or live experiment,** even small (Narisetty et al.'s protocol), or an explicit scope statement that the paper is about non-adaptive evaluation methodology.
3. **Real evasion for behavioral evidence**, and a zero-width population in replay.
4. **Human label audit** (file 53), at least for the random stratum.
5. **A second population or benchmark** with argument-level financial tools.
6. **Confirmatory data:** a new recording set never used for design.

## 5. Venue considerations (no outcome is guaranteed)

| Venue type | Fit | Main risk |
|---|---|---|
| Security workshops (for example ACM AISec) | Good fit for a measurement-methodology paper | Novelty bar regarding layered defenses |
| Journals with an empirical-security focus | Possible after items 1–5 | Reviewers will ask for adaptive and live evaluation |

**Q1 publication cannot be promised.** The present evidence is exploratory, single-benchmark and non-adaptive.
