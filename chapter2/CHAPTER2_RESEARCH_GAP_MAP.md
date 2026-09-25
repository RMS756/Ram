# Chapter 2: Research Gap Map (systematic review version, 25 September 2026)

This map replaces the gap map of the earlier integrated narrative review. The gap was rebuilt **after** screening, extraction, appraisal and synthesis (`CHAPTER2_SYSTEMATIC_REVIEW.md`, §2.13).

Each gap is traced through the chain: **Prior literature → Limitation → Evidence (study ID, evidence level, verification) → Gap → REM positioning.**

- **Study IDs** (P01–P71) refer to `CHAPTER2_SYSTEMATIC_EVIDENCE_MATRIX.csv`.
- **Evidence levels** are HIGH, MOD (moderate) and LIM (limited) (`CHAPTER2_QUALITY_APPRAISAL.md`).
- **PV** marks a PARTIALLY VERIFIED study.
- No gap depends solely on a PV detail.

The protocol's candidate gaps A–E were assessed against the evidence:

| Candidate gap | Decision |
|---|---|
| A. Integration | **Retained, narrowed** |
| B. Runtime action-boundary evaluation combining signals | **Not retained as stated** (contradicted by evidence); residue merged into A |
| C. Behavioral/provenance contribution | **Retained, narrowed** |
| D. Financial-agent evidence | **Retained** |
| E. Evaluation decomposition | **Retained, narrowed** |

---

## Gap A: Integration of a calibrated probability of adversarial induction with consequence-indexed losses at the action boundary

| Prior literature | Limitation relative to the REM problem | Evidence as reported | Level / verification |
|---|---|---|---|
| NEXUS (Hossain et al., 2026) [P65] | Calibrated LR score, four interventions and consequence annotations, all at the **plan** level on **author templates** (in-distribution results called upper bounds by the authors). Expected-loss objective uses **fixed** intervention costs to set thresholds in a **rule-first cascade**. | F1 0.949; 4-class accuracy 0.6406; ECE 0.085→0.013; median 0.205 ms; OOD F1 0.861/0.881 | MOD; PV (costs, cascade, ECE) |
| AgentTrust (C. Yang, 2026) [P64] | Pre-execution interception with four verdicts from rules and analysers plus an LLM judge; **no calibrated probability** reported; reversibility is one judge dimension | 95.0% verdict / 73.7% risk-level accuracy; ~1.72 ms (PV); 96.7% on 630 external scenarios (patched rules) | MOD; PV |
| LATTICE (Calboreanu, 2026) [P40] | Deterministic policy verdicts with confidence-based human escalation; **no probability of induction combined with consequence** | Confidence-threshold baseline false-allow 0.03–0.998 across planners; zero unsafe actions at an operating point that auto-allowed no action | HIGH |
| MCP policy-enforcement point (S. Wang et al., 2026) [P37] | Rules over cross-step provenance labels at the tool-call boundary; **binary** rule verdicts | ASR 40.0%→5.0%; task-level FP 30.0%; sub-ms | HIGH |
| H.-H. Chen (2026) [P67] | Deterministic consequence pricing; **no estimate of adversarial induction** | Design framework | LIM |
| SafeAgent (H. Liu et al., 2026) [P63] | Consequence modelling and arbitration by **LLM reasoning**; calibration not verifiable | Improves robustness on ASB and InjecAgent | LIM; PV |
| Jackson (2025) [P66] | Risk score to allow/deny/sanitize/escalate; **unrefereed; full text not accessed** | Qualitative | LIM; PV |
| Kaptein et al. (2026) [P19] | Formalises path-conditioned violation probability; **risk calibration left open**; not evaluated | Formal framework | LIM |
| Elkan (2001); Chow (1970) | Foundational decision theory; not evaluated for agent action gating | — | Foundational source |

**Gap A.** Among the 71 included studies, none reports selecting among graduated responses per proposed tool call by minimising expected loss that combines two things: a **calibrated probability of adversarial induction**, and **losses declared per consequence tier**.

**Why narrowed.** NEXUS combines calibration, costs and graduated responses. The difference therefore lies in the point of evaluation (per call during execution, not the plan), the loss structure (consequence-indexed, not fixed per intervention), and the setting (executable benchmark under indirect injection).

**REM positioning.** This is REM's Decision Engine. REM claims none of the individual elements: calibration, verdict set, expected-loss rule, consequence awareness or interception.

---

## Candidate Gap B (not retained as stated)

**Candidate.** "Limited evidence combining multiple signals at the point of action."

**Contrary evidence.** Several included studies combine signals at or near the tool call:

- AgentTrust [P64]: normalizer, analysers, rules, session chains and an LLM judge;
- MCP policy-enforcement point [P37]: rules with cross-step labels and audit;
- ToolSafe [P33]: request plus interaction history;
- DRIFT [P38]: plan, privilege and intent validation with injection isolation;
- SafeAgent [P63];
- FinHarness [P71].

**Decision.** The candidate is contradicted and is **not retained**. Its defensible residue, combining signals *into a calibrated probability*, is part of Gap A.

---

## Gap C: The contribution of behavioural and provenance evidence as inputs to a calibrated estimator under indirect injection

| Prior literature | Limitation | Evidence | Level / verification |
|---|---|---|---|
| AgentTrust session tracker [P64] | **Null** effect in the author's ablation | Disabling it left verdict accuracy unchanged | MOD; PV |
| MCP policy-enforcement point [P37] | **Positive** effect of cross-step labels, but inside a **rule-based** enforcer on a **controlled** dataset | Removing label propagation raised call-level false negatives by 26.4 points | HIGH |
| ProvenanceGuard [P58] | Provenance used as a **detector** producing interventions | Error 44.3%→2.1% (Agent-SafetyBench), 32.4%→18.7% (WorkBench) versus an LLM judge | MOD; PV (intervention rates, cost) |
| MI9 [P59]; ProbGuard [P61]; DreamGuard [P62] | Trajectory models evaluated on **synthetic** data (MI9) or in **non-financial** settings (ProbGuard, DreamGuard) | 99.81% on 1,033 synthetic scenarios (MI9, PV); up to 65.37% unsafe reduction (ProbGuard, embodied); ~25 ms per call (DreamGuard) | MOD |
| Constitutional monitors [P34] | Trajectory monitors **saturate** and overfit | Qualitative in the record | LIM |
| Forrest et al. (1996); Chandola et al. (2009, 2012); Sommer & Paxson (2010); Arp et al. (2022) | Classical requirements (benign workload, base rates, interpretation) applied unevenly | — | Foundational / methodological |

**Gap C.** The evidence on the contribution of behavioural and provenance evidence is **limited and conflicting**: a null effect for a session tracker, and a large effect for cross-step labels in a rule-based enforcer. No included study tests either kind of evidence as **input to a calibrated estimator**, and none tests it on **financial actions** under indirect injection.

**Why narrowed.** One HIGH-evidence study does separate a provenance component's contribution, but only for rule-based enforcement.

**REM positioning.** REM's Behavioral Analysis Layer uses action-provenance features as estimator inputs. REM claims neither provenance nor trajectory analysis. Its evaluation must report the contribution through ablation (RQ4 [PD]) and must show that the benchmark contains the targeted behaviour.

---

## Gap D: Verified financial-agent evidence in an open executable setting

| Prior literature | Limitation | Evidence | Level |
|---|---|---|---|
| AgentDojo [P44]; ASB [P27]; AgentHarm [P42]; ClawSafety [P15] | Finance is **one suite, scenario, category or domain** among several; no finance-specific analysis in the verified record | Banking suite; finance scenario; fraud category; finance domain | MOD / HIGH (ASB) |
| FinHarness [P71] | Closest financial runtime harness; **LLM-judge** routing; all figures on the **withdrawn** FinVault benchmark | ASR 38.3%→15.0%; benign approval 41.1%→39.3% (not usable as affirmative evidence) | LIM (override) |
| Castro-Maldonado et al. (2026) [P32] | Banking agentic-RAG chatbot firewall; threat model and results not verifiable from the record | — | LIM |
| Z. Chen, J. Chen, et al. (2025) [P70] | Position paper; audit of six agents on three tasks; no runtime defense | — | LIM |
| H.-H. Chen (2026) [P67] | Actuarial framing; no estimate of adversarial induction | — | LIM |
| FinVault (Z. Yang et al., 2026) | **Withdrawn**; cited only to record that status | — | Excluded (withdrawn) |
| Mao et al. (2026) | Systematisation of commerce threats; secondary study | — | Background source |

**Gap D.** All financial-context studies are LIMITED EVIDENCE, and the only quantitative financial runtime results rest on a withdrawn benchmark. There is limited verified evidence on runtime protection evaluated at the level of **individual financial actions and their consequences** in an open, executable environment.

**REM positioning.** REM is evaluated on AgentDojo's Banking suite (planned), with consequence tiers declared per financial action type. REM does not claim to be the first financial runtime protection.

---

## Gap E: Evaluation that separates the parts

| Prior literature | Limitation | Evidence | Level / verification |
|---|---|---|---|
| C. Zhang et al. (2026) [P69] | Calibration improved but **control did not** | ECE 0.463→0.006; regret unchanged at 0.318 | MOD; PV |
| LATTICE [P40] | A confidence threshold was **unstable across planners**; zero false-allow achieved only at an operating point that auto-allowed no action | 0.03–0.998 false-allow | HIGH |
| MCP policy-enforcement point [P37]; NEXUS [P65]; ToolSafe [P33] | Report several dimensions (ASR, false positives or negatives, utility, latency, calibration) but **not a same-estimator consequence-independent comparison** | See matrix | HIGH / MOD |
| M. Q. Li et al. (2026) [P45]; Y. Wang et al. (2026) [P46] | Benchmark results do not transfer; metric artefacts | No ranking concordance; an always-positive baseline outranks models | MOD |
| (None of the 71 included studies) | **No comparison** of a consequence-aware decision against a consequence-independent baseline sharing its estimator | — | Bounded negative over the included corpus |

**Gap E.** Calibration is reported for one deployed scorer, intervention rates by few studies, and no included study compares a consequence-aware decision with a **consequence-independent baseline that uses the same estimator**. That comparison is needed to attribute any effect to the use of consequences, with calibration reported separately from control.

**REM positioning.** REM's evaluation design (Chapter 3, §§3.11–3.12) reports attack success, benign utility, utility under attack, intervention rates, calibration and latency separately. It compares against baseline B1: the same estimator with a consequence-independent threshold policy. Losses are reported across a declared grid.

---

## Consolidated gap statement (as in §2.13.2)

> Among the 71 studies included in this systematic review (search date 25 September 2026), none reports an empirical evaluation of a non-invasive runtime layer for a financial tool-using agent that combines (i) provenance-based evidence about proposed financial actions, (ii) a calibrated per-step probability that the proposed action is adversarially induced, (iii) a decision that minimizes expected loss over Allow, Modify, Escalate and Block using losses declared per consequence tier, and (iv) deterministic mitigation whose effectiveness is measured and used in the loss structure. None reports attack success, benign utility, utility under attack, intervention behavior and latency separately, with calibration reported separately from control outcomes, and results compared against a consequence-independent baseline that uses the same estimator.

| Clause | Supported by | Closest prior art (not claimed by REM) |
|---|---|---|
| (i) provenance evidence | Gap C | ProvenanceGuard; MCP policy-enforcement point; CaMeL; ACE; RTBAS |
| (ii) calibrated per-step probability | Gap A | NEXUS (plan level) |
| (iii) expected loss over four responses with tier-indexed losses | Gap A | NEXUS objective; Jackson; AgentTrust verdicts; H.-H. Chen pricing; LATTICE escalation |
| (iv) deterministic mitigation, effectiveness measured and used in the loss structure | Gap E | Progent; AgentSpec; Cordon; GoEX |
| Financial tool-using agent; open executable benchmark | Gap D | FinHarness; AgentDojo Banking |
| Separate measurement; same-estimator baseline | Gap E | C. Zhang et al. (analysis); MCP policy-enforcement point and NEXUS ablations; LATTICE baseline |

**Nature of the gap.**
- **Integrative and empirical.** It concerns combining established mechanisms and evaluating them, not a missing mechanism.
- **Bounded.** By the search (one database, retrieval cap, a partly non-independent second stream) and by record-level appraisal.
- **Falsifiable.** A study reporting this combination and evaluation would require the contribution to be revised.

---

## Prior-art risks

1. **NEXUS.** Per-call evaluation on an executable benchmark, or consequence-dependent intervention losses, would largely close Gap A.
2. **AgentTrust.** Calibrated probabilities or consequence-weighted decisions would narrow Gap A. Do not confuse it with the different arXiv paper 2606.08539.
3. **MCP policy-enforcement point / LATTICE (HIGH).** A probabilistic extension would narrow Gaps A, C and E.
4. **FinHarness.** Re-evaluation on an open benchmark with a probabilistic decision layer would narrow Gap D.
5. **Jackson.** If the full text documents calibrated, consequence-weighted selection with evaluation, Gaps A and E narrow.
6. **Unsearched databases.** The libraries reported as DATABASE ACCESS UNAVAILABLE must be searched directly before submission.
