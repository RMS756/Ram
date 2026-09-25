# Chapter 2: Research Gap Map

This file traces how each part of the research gap in §2.12 follows from the reviewed evidence, using the chain:

**Prior literature → Limitation → Evidence → Gap → REM positioning**

Verification status (from `CHAPTER2_REFERENCE_EVIDENCE_MATRIX.md`) is shown where a link in the chain rests on a PARTIALLY VERIFIED source. No gap depends *solely* on a partially verified detail.

---

## Gap 1: Integration of a calibrated probability with declared consequences at the action boundary

| Prior literature | Limitation relative to the REM problem | Evidence (as reported) | Verification |
|---|---|---|---|
| NEXUS (Hossain et al., 2026) | Calibrated LR score and four interventions, but evaluated at the **plan** level, mainly on **author-generated templates** (authors: in-distribution results are upper bounds). The expected-loss objective uses **fixed intervention costs** (0 / 0.1 / 0.3 / 1) to set score thresholds inside a **rule-first cascade**; the costs do not vary with the consequence of the particular action | F1 0.949; 4-class accuracy 0.6406; ECE 0.085 → 0.013; median 0.205 ms; OOD F1 0.861 / 0.881 | FULLY VERIFIED (primary HTML) |
| AgentTrust (C. Yang, 2026) | Pre-execution interception and four verdicts; verdicts from analyzer + rules (worst case over normalized variants) and an LLM judge; **no calibrated probability reported**; reversibility is one judge dimension | 95.0% verdict / 73.7% risk-level accuracy; ~1.72 ms; 96.7% on 630 external scenarios (patched rules) | FULLY VERIFIED |
| H.-H. Chen (2026) | Prices consequence deterministically; **does not estimate adversarial induction** | Actuarial Action Interface; Authority Frontier | Abstract verified; author given name PARTIALLY VERIFIED |
| SafeAgent (H. Liu et al., 2026) | Consequence modeling and arbitration realized by **LLM reasoning**; calibration reporting not verifiable | Improves robustness on ASB and InjecAgent; ablation over recovery confidence / policy weighting | FULLY VERIFIED (calibration/latency: NOT VERIFIED) |
| Jackson (2025) | Risk score → allow/deny/sanitize/escalate; **unrefereed; full text not accessible** | Qualitative claims only | PARTIALLY VERIFIED (abstract) |
| Elkan (2001); Chow (1970) | Established theory; not evaluated for agent action gating | — | FULLY VERIFIED |

**Gap 1.** The reviewed literature provides limited evidence on selecting among graduated responses by minimizing expected loss **per proposed tool call**, using a **calibrated probability of adversarial induction** together with **losses declared per consequence tier**.

**REM positioning.** This is REM's Decision Engine. REM claims no novelty for calibration, the verdict set, the expected-loss formulation, loss-optimal thresholds or consequence awareness (NEXUS, AgentTrust, Jackson, H.-H. Chen). The claim is limited to the combination at the action boundary (losses indexed by each action's declared consequence tier, per proposed tool call, on an executable benchmark) and its evaluation.

**Strength note (Rule 14, conflict C13).** Primary-source verification in the 25 September pass showed that NEXUS uses its expected-loss objective more directly than earlier drafts stated. It sets loss-optimal thresholds on the calibrated score. Gap 1 is therefore **narrower** than the July and early-September drafts implied, and it rests on three differences: per-tool-call evaluation during execution, consequence-indexed rather than fixed intervention losses, and an executable financial benchmark.

---

## Gap 2: The measured value of behavioral and provenance evidence under indirect injection

| Prior literature | Limitation | Evidence | Verification |
|---|---|---|---|
| AgentTrust session tracker (C. Yang, 2026) | Trajectory component with **no measurable effect** in the author's own ablation | Disabling it left verdict accuracy unchanged on both benchmarks | FULLY VERIFIED |
| MI9 (C. L. Wang et al., 2025) | Trajectory governance evaluated on **synthetic** scenarios; agent-level risk index | >1,000 synthetic scenarios | FULLY VERIFIED (abstract) |
| ProbGuard (H. Wang et al., 2025); DreamGuard (Lin et al., 2026) | Sequence-level models evaluated in **non-financial** settings (AV, embodied; general agent benchmarks) | ProbGuard: up to 65.37% unsafe reduction; DreamGuard: ~25 ms per call | FULLY VERIFIED |
| PRISM (F. Li, 2026); FinHarness (H. Jia et al., 2026) | **Heuristic** accumulation (TTL decay; cascade thresholds) | — | FULLY VERIFIED |
| ProvenanceGuard (She et al., 2026); Task Shield (F. Jia et al., 2025); MELON (Zhu et al., 2025) | Provenance and goal consistency used as **detectors producing interventions**, not as inputs to a calibrated estimator; not evaluated on financial actions | ProvenanceGuard error 44.3% → 2.1%, intervention 10.9% → 14.5%; Task Shield ASR 2.07%, utility 69.79% | FULLY VERIFIED |
| Forrest et al. (1996); Chandola et al. (2009, 2012); Sommer & Paxson (2010); Arp et al. (2022) | Classical requirements (benign workload, base rates, semantic interpretation) are **unevenly applied** in agent studies | — | FULLY VERIFIED |
| M. Q. Li et al. (2026); Y. Wang et al. (2026) | Benchmark results unstable; genuinely multi-step attacks may be scarce | No ranking concordance; small-panel artefacts | FULLY VERIFIED |

**Gap 2.** The reviewed literature provides limited evidence on how much **behavioral and action-provenance evidence contributes** to a runtime decision for a financial tool-using agent under indirect injection, when that evidence feeds a calibrated estimator rather than a detector verdict.

**REM positioning.** REM's Behavioral Analysis Layer uses action-provenance features as estimator inputs (Chapter 3, §3.6). REM claims no novelty for provenance or trajectory analysis. The chapter commits the evaluation to report the component's contribution rather than assume it (§2.6.5). CUSUM is reviewed as an established alternative for sequential accumulation (§2.7.4), not as a contribution.

---

## Gap 3: Financial execution

| Prior literature | Limitation | Evidence | Verification |
|---|---|---|---|
| ASB (H. Zhang et al., 2025); AgentDojo (Debenedetti et al., 2024) | Finance is **one scenario among many**; results reported in aggregate | ASB 10 scenarios incl. finance; AgentDojo Banking suite | FULLY VERIFIED |
| FinHarness (H. Jia et al., 2026) | Closest domain system; **LLM-judge** routing; evaluated on a **withdrawn** benchmark | ASR 38.3% → 15.0%; benign approval 41.1% → 39.3% | FULLY VERIFIED |
| FinVault (Z. Yang et al., 2026) | **Withdrawn**; cannot serve as evidence | — | Withdrawal FULLY VERIFIED |
| Z. Chen, J. Chen, et al. (2025) | Position paper; argues for risk-first evaluation; no runtime defense | Audit of six agents on three tasks | FULLY VERIFIED |
| Mao et al. (2026) | Systematization of commerce-agent threats; **no empirical evaluation** of a defense | Five dimensions; 12 attack vectors | FULLY VERIFIED (abstract) |
| H.-H. Chen (2026) | Actuarial consequence framing; no estimate of adversarial induction | — | PARTIALLY VERIFIED (name) |

**Gap 3.** The reviewed literature provides limited **verified** evidence on runtime protection evaluated at the level of **individual financial actions and their consequences** in an open, executable environment.

**REM positioning.** REM is evaluated on AgentDojo's Banking environment (planned), with consequence tiers declared per financial action type. REM does not claim to be the first runtime protection for financial agents (FinHarness).

---

## Gap 4: Evaluation that separates the parts

| Prior literature | Limitation | Evidence | Verification |
|---|---|---|---|
| C. Zhang et al. (2026) | Calibration improves prediction but **not control**; the two must be measured separately | ECE 0.463 → 0.006 while regret unchanged at 0.318 | FULLY VERIFIED |
| Table 2.7 (all systems) | Latency, benign utility, calibration and intervention behavior reported **unevenly** | Latency reported by AgentSpec, AgentTrust, NEXUS and DreamGuard; not reported or not verified for most others | Per-row labels |
| M. Q. Li et al. (2026); Y. Wang et al. (2026); Arp et al. (2022) | Results must be reported per benchmark, with benign workloads | — | FULLY VERIFIED |
| (No reviewed study) | No comparison of a consequence-aware decision against a **consequence-independent baseline that uses the same estimator** | — | Bounded negative over the reviewed corpus |

**Gap 4.** Few reviewed studies report attack success, benign utility, intervention behavior, calibration and latency **separately**, and none reviewed compares a consequence-aware decision with a consequence-independent baseline that shares its estimator. That comparison is needed to attribute any effect to the use of consequences.

**REM positioning.** REM's evaluation design (Chapter 3, §§3.11–3.12) reports these quantities separately, together with the same-estimator baseline. Losses are reported across a declared grid rather than as fixed truths.

---

## Consolidated gap (as stated in §2.12.2)

> Among the studies reviewed in this chapter, none reports an empirical evaluation of a non-invasive runtime layer for a financial tool-using agent that combines (i) provenance-based evidence about proposed financial actions, (ii) a calibrated per-step probability that the proposed action is adversarially induced, (iii) a decision that minimizes expected loss over Allow, Modify, Escalate and Block using losses declared per consequence tier, and (iv) deterministic mitigation, with attack success, benign utility, intervention behavior, calibration and latency measured separately and compared against a consequence-independent baseline that uses the same estimator.

| Clause | Supported by gap | Closest prior art (not claimed by REM) |
|---|---|---|
| (i) provenance evidence | Gap 2 | ProvenanceGuard; Task Shield; MELON |
| (ii) calibrated per-step probability | Gap 1 | NEXUS (plan-level) |
| (iii) expected loss over four responses with tier-indexed losses | Gap 1 | NEXUS objective; Jackson; AgentTrust verdicts; H.-H. Chen pricing |
| (iv) deterministic mitigation | — (adopted) | Progent; AgentSpec; Cordon |
| financial tool-using agent; open executable benchmark | Gap 3 | FinHarness; AgentDojo Banking |
| separate measurement + same-estimator baseline | Gap 4 | C. Zhang et al. (analysis); AgentTrust/NEXUS ablations |

**Nature of the gap.** Integrative and empirical, bounded by the reviewed corpus and the September 2026 verification pass. It is falsifiable: a study reporting this combination and evaluation would require the thesis contribution to be revised.

---

## Remaining prior-art risks to monitor

1. **NEXUS**: the cascade and fixed-cost threshold design are now verified. If a later version evaluates per tool call on an executable benchmark, or makes intervention losses depend on the consequence of each action, Gap 1 largely closes.
2. **AgentTrust**: if a later version adds calibrated probabilities or consequence-weighted decisions, Gap 1 narrows. Note the name collision with arXiv 2606.08539.
3. **FinHarness**: if re-evaluated on an open executable benchmark with a probabilistic decision layer, Gap 3 narrows.
4. **Jackson (2025)**: the full text was not accessible. If it documents calibrated, consequence-weighted selection with evaluation, Gaps 1 and 4 narrow.
5. **Rapid preprint turnover** (2026 preprints: DreamGuard, SafeAgent, Cordon, ProvenanceGuard, C. Zhang et al.): re-run the search immediately before submission.
