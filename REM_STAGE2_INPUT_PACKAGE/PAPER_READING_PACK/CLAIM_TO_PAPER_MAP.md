# CLAIM TO PAPER MAP — Chapters 2 and 3

Read-only. Every thesis sentence that depends on one of the 18 papers in this reading pack, traced to the paper and to the audit record for that sentence. The thesis text is quoted exactly from `working/Chapter2_working.md` and `working/Chapter3_working.md`; nothing was edited.

## What counts as a claim here

A sentence is included when it:

1. **cites** one of the 18 papers in author–date form; or
2. **follows** such a citation in the same paragraph and makes a statement about that paper, such as "Its authors report…"; or
3. **names** one of the 18 systems without a citation, in a paragraph that contains citations (for example, the comparative synthesis in Ch2 §2.13); or
4. is the **status line** of an equation whose source is one of the 18.

Comparative table rows (Ch2 §2.12–§2.13; Ch3 §3.13 and §3.15) are included as whole rows.

## How to read the status

| Status | Meaning |
| --- | --- |
| **SUPPORTED IN STAGE 1 RECORD — source text read** | A Stage 1 audit row checked this sentence against the paper's text. That reading was done in Stage 1 and cannot be reproduced here. |
| **SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED** | A Stage 1 audit row checked this sentence against the paper's abstract or metadata only. |
| **PARTIALLY SUPPORTED — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (metadata only…)** | The paper's record was confirmed but its text was not read, so the specific content is not verified. |
| **PARTLY SUPPORTED — specific passage not inspected** | The paper was read, but not the passage this sentence relies on. |
| **UNVERIFIED** | A Stage 1 record says the figure was not found in the source, or the source could not be opened. |
| **NOT AUDITED AT CLAIM LEVEL** | No audit record checks this sentence. Only the reference-level record exists, and it is shown. This is **not** evidence either way. |

"Evidence location in paper" is taken only from the audit records. Where they record none, the entry says so.

## Summary

- **Claims mapped:** 133 sentences or table rows (79 in Chapter 2, 54 in Chapter 3)
- **Claim–paper links:** 157 (a claim can depend on several papers)
  - SUPPORTED IN STAGE 1 RECORD: 66 links
  - PARTIALLY SUPPORTED: 12 links
  - PARTLY SUPPORTED: 2 links
  - UNVERIFIED: 7 links
  - NOT AUDITED AT CLAIM LEVEL: 70 links

**Figures that no Stage 1 record checks individually:** C. Zhang et al.'s ALFWorld figures (ECE 0.463 → 0.006; regret 0.318; Ch2 L126); NEXUS's 0.205 ms median latency (Ch2 L65); FinHarness's "4.7 times fewer calls" (Ch2 L97; the sentence's other two figures are audited in N049–N050).

---

## Chapter 2

### CM-001 · Ch2 §2.3 Prompt Injection and Indirect Prompt Injection · L31

**THESIS CLAIM**

> Greshake et al. (2023) demonstrated that adversarial instructions placed in data that an LLM-integrated application retrieves can compromise the application remotely, without direct access to its interface.

- **→ CITED PAPER:** [PAPER_03 — Greshake et al. (2023)](PAPER_03.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.3 Prompt Injection and Indirect Prompt Injection, line 31
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-019): "Crossref metadata and arXiv abstract"; reference status VERIFIED.

### CM-002 · Ch2 §2.3 Prompt Injection and Indirect Prompt Injection · L33

**THESIS CLAIM**

> AgentDojo (Debenedetti et al., 2024) provides 97 realistic tasks and 629 security test cases across environments that include e-banking, and it measures both utility and security.

- **→ CITED PAPER:** [PAPER_17 — Debenedetti et al. (2024) — AgentDojo](PAPER_17.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.3 Prompt Injection and Indirect Prompt Injection, line 33
  - **→ EVIDENCE LOCATION IN PAPER:** arXiv abstract; banking suite read in the public repository; figure read in source (Stage 1)
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
    - Stage 1 claim audit **Ch2-C004**: VERIFIED (support: Full). Evidence: arXiv abstract; banking suite read in the public repository.
    - Stage 1 numerical audit **N015** (figure 97): VERIFIED; figure read in source: Yes.
    - Stage 1 numerical audit **N016** (figure 629): VERIFIED; figure read in source: Yes.

### CM-003 · Ch2 §2.3 Prompt Injection and Indirect Prompt Injection · L33

**THESIS CLAIM**

> Its authors report that current models fail many tasks even without attacks and that existing attacks break some security properties but not all.

- **→ CITED PAPER:** [PAPER_17 — Debenedetti et al. (2024) — AgentDojo](PAPER_17.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.3 Prompt Injection and Indirect Prompt Injection, line 33
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-014): "arXiv abstract; banking suite read in the public repository"; reference status VERIFIED.

### CM-004 · Ch2 §2.4.4 Integrated runtime layers · L61

**THESIS CLAIM**

> **SafeAgent** (H. Liu et al., 2026) consists of a runtime controller that mediates actions in the agent loop and a context-aware decision core over persistent session state.

- **→ CITED PAPER:** [PAPER_06 — H. Liu et al. (2026) — SafeAgent](PAPER_06.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.4.4 Integrated runtime layers, line 61
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-032): "Full HTML text read"; reference status VERIFIED.

### CM-005 · Ch2 §2.4.4 Integrated runtime layers · L61

**THESIS CLAIM**

> The core's operators for risk encoding, advantage–cost modeling, consequence simulation, and policy arbitration are realized through LLM reasoning rather than formal equations.

- **→ CITED PAPER:** [PAPER_06 — H. Liu et al. (2026) — SafeAgent](PAPER_06.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.4.4 Integrated runtime layers, line 61
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-032): "Full HTML text read"; reference status VERIFIED.

### CM-006 · Ch2 §2.4.4 Integrated runtime layers · L61

**THESIS CLAIM**

> The action space includes context sanitization, replanning, rollback, session termination, tool-argument rewriting, and human approval.

- **→ CITED PAPER:** [PAPER_06 — H. Liu et al. (2026) — SafeAgent](PAPER_06.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.4.4 Integrated runtime layers, line 61
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-032): "Full HTML text read"; reference status VERIFIED.

### CM-007 · Ch2 §2.4.4 Integrated runtime layers · L61

**THESIS CLAIM**

> SafeAgent was evaluated on ASB and InjecAgent using attack success rate and performance under no attack.

- **→ CITED PAPER:** [PAPER_06 — H. Liu et al. (2026) — SafeAgent](PAPER_06.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.4.4 Integrated runtime layers, line 61
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-032): "Full HTML text read"; reference status VERIFIED.

### CM-008 · Ch2 §2.4.4 Integrated runtime layers · L61

**THESIS CLAIM**

> Its ablations show that a policy-weighting setting moves the system between safety-first and task-first operating points.

- **→ CITED PAPER:** [PAPER_06 — H. Liu et al. (2026) — SafeAgent](PAPER_06.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.4.4 Integrated runtime layers, line 61
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-032): "Full HTML text read"; reference status VERIFIED.

### CM-009 · Ch2 §2.4.4 Integrated runtime layers · L61

**THESIS CLAIM**

> The paper does not address probability calibration and does not report latency, which its authors acknowledge as a limitation in terms of computational overhead.

- **→ CITED PAPER:** [PAPER_06 — H. Liu et al. (2026) — SafeAgent](PAPER_06.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.4.4 Integrated runtime layers, line 61
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-032): "Full HTML text read"; reference status VERIFIED.

### CM-010 · Ch2 §2.4.4 Integrated runtime layers · L63

**THESIS CLAIM**

> **AgentTrust** (C. Yang, 2026) intercepts agent tool use through a pipeline of command normalization, pattern-based feature extraction, 170 configurable policy rules, analyzer-based risk scoring, session-based chain detection, and optional LLM judgment.

- **→ CITED PAPER:** [PAPER_08 — C. Yang (2026) — AgentTrust](PAPER_08.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.4.4 Integrated runtime layers, line 63
  - **→ EVIDENCE LOCATION IN PAPER:** figure read in source (Stage 1)
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 numerical audit **N033** (figure 170): VERIFIED; figure read in source: Yes.

### CM-011 · Ch2 §2.4.4 Integrated runtime layers · L63

**THESIS CLAIM**

> Risk is aggregated by taking the maximum severity over the signals that fire, and the system returns one of four verdicts: allow, warn, block, or review.

- **→ CITED PAPER:** [PAPER_08 — C. Yang (2026) — AgentTrust](PAPER_08.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.4.4 Integrated runtime layers, line 63
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-053): "Full HTML text read"; reference status VERIFIED.

### CM-012 · Ch2 §2.4.4 Integrated runtime layers · L63

**THESIS CLAIM**

> Confidence is assigned by a step function of evidence strength rather than by probabilistic calibration.

- **→ CITED PAPER:** [PAPER_08 — C. Yang (2026) — AgentTrust](PAPER_08.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.4.4 Integrated runtime layers, line 63
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-053): "Full HTML text read"; reference status VERIFIED.

### CM-013 · Ch2 §2.4.4 Integrated runtime layers · L63

**THESIS CLAIM**

> The authors report component ablations with verdict accuracy, false-negative rate, and latency; a rule-only configuration reached 95.0% verdict accuracy and 73.7% risk-level accuracy at low-millisecond latency, and verdict accuracy was 96.7% on an external set of 630 scenarios.

- **→ CITED PAPER:** [PAPER_08 — C. Yang (2026) — AgentTrust](PAPER_08.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.4.4 Integrated runtime layers, line 63
  - **→ EVIDENCE LOCATION IN PAPER:** figure read in source (Stage 1)
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 numerical audit **N034** (figure 95.0%): VERIFIED; figure read in source: Yes.
    - Stage 1 numerical audit **N035** (figure 73.7%): VERIFIED; figure read in source: Yes.
    - Stage 1 numerical audit **N036** (figure 96.7%): VERIFIED; figure read in source: Yes.
    - Stage 1 numerical audit **N037** (figure 630): VERIFIED; figure read in source: Yes.

### CM-014 · Ch2 §2.4.4 Integrated runtime layers · L63

**THESIS CLAIM**

> Reversibility is part of the labeling rubric.

- **→ CITED PAPER:** [PAPER_08 — C. Yang (2026) — AgentTrust](PAPER_08.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.4.4 Integrated runtime layers, line 63
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-053): "Full HTML text read"; reference status VERIFIED.

### CM-015 · Ch2 §2.4.4 Integrated runtime layers · L65

**THESIS CLAIM**

> **NEXUS** (Hossain et al., 2026) evaluates the plan an agent proposes before execution.

- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.4.4 Integrated runtime layers, line 65
  - **→ EVIDENCE LOCATION IN PAPER:** Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) · reference metadata conflict (OI-06)**
    - Stage 1 claim audit **Ch2-C010**: METADATA ERROR (support: Full). Evidence: Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date.
- **Open item(s):** OI-06 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-016 · Ch2 §2.4.4 Integrated runtime layers · L65

**THESIS CLAIM**

> It combines deterministic safety rules, argument-level inspection, and a logistic-regression risk score over 99 plan features, including an irreversibility indicator and estimated cost.

- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.4.4 Integrated runtime layers, line 65
  - **→ EVIDENCE LOCATION IN PAPER:** figure not located in source
  - **→ VERIFICATION STATUS:** **UNVERIFIED — figure not read in source**
    - Stage 1 numerical audit **N038** (figure 99): UNVERIFIED; figure read in source: No.
- **Open item(s):** OI-02 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-017 · Ch2 §2.4.4 Integrated runtime layers · L65

**THESIS CLAIM**

> The score is calibrated by Platt scaling, with isotonic regression also evaluated.

- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.4.4 Integrated runtime layers, line 65
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-023): "Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date"; reference status PARTIALLY VERIFIED.

### CM-018 · Ch2 §2.4.4 Integrated runtime layers · L65

**THESIS CLAIM**

> On a 128-instance held-out test set the expected calibration error fell from 0.085 for the raw model to 0.013 after Platt scaling, using a 60-instance calibration split.

- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.4.4 Integrated runtime layers, line 65
  - **→ EVIDENCE LOCATION IN PAPER:** figure not located in source
  - **→ VERIFICATION STATUS:** **UNVERIFIED — figure not read in source**
    - Stage 1 numerical audit **N039** (figure 128): UNVERIFIED; figure read in source: No.
    - Stage 1 numerical audit **N040** (figure 60): UNVERIFIED; figure read in source: No.
- **Open item(s):** OI-03, OI-04 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-019 · Ch2 §2.4.4 Integrated runtime layers · L65

**THESIS CLAIM**

> The deployed policy selects among four interventions (allow, block, request confirmation, or request revision) through a rule cascade in which the calibrated score gates certain cases.

- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.4.4 Integrated runtime layers, line 65
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-023): "Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date"; reference status PARTIALLY VERIFIED.
- **Open item(s):** OI-01 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-020 · Ch2 §2.4.4 Integrated runtime layers · L65

**THESIS CLAIM**

> The paper also defines an expected-loss objective with fixed costs for each intervention.

- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.4.4 Integrated runtime layers, line 65
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-023): "Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date"; reference status PARTIALLY VERIFIED.
- **Open item(s):** OI-01 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-021 · Ch2 §2.4.4 Integrated runtime layers · L65

**THESIS CLAIM**

> The authors report a median decision latency of 0.205 ms and caution that results on their author-generated templates should be read as upper bounds rather than deployment estimates.

- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.4.4 Integrated runtime layers, line 65
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-023): "Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date"; reference status PARTIALLY VERIFIED.

### CM-022 · Ch2 §2.5 Stateful and Trajectory-Aware Protection · L73

**THESIS CLAIM**

> FinHarness (Jia et al., 2026) tracks user intent across multiple interactions in its Query Monitor.

- **→ CITED PAPER:** [PAPER_18 — Jia et al. (2026) — FinHarness](PAPER_18.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.5 Stateful and Trajectory-Aware Protection, line 73
  - **→ EVIDENCE LOCATION IN PAPER:** arXiv abstract (components and numbers)
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
    - Stage 1 claim audit **Ch2-C011**: VERIFIED (support: Full). Evidence: arXiv abstract (components and numbers).

### CM-023 · Ch2 §2.5 Stateful and Trajectory-Aware Protection · L73

**THESIS CLAIM**

> SafeAgent treats security as a stateful decision problem over evolving interaction trajectories (H. Liu et al., 2026).

- **→ CITED PAPER:** [PAPER_06 — H. Liu et al. (2026) — SafeAgent](PAPER_06.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.5 Stateful and Trajectory-Aware Protection, line 73
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-032): "Full HTML text read"; reference status VERIFIED.

### CM-024 · Ch2 §2.5 Stateful and Trajectory-Aware Protection · L77

**THESIS CLAIM**

> AgentTrust's own ablation found that its session tracker had no measurable effect on either of its benchmarks (C. Yang, 2026), which suggests that single-action signals dominated the scenarios tested.

- **→ CITED PAPER:** [PAPER_08 — C. Yang (2026) — AgentTrust](PAPER_08.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.5 Stateful and Trajectory-Aware Protection, line 77
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-053): "Full HTML text read"; reference status VERIFIED.

### CM-025 · Ch2 §2.6 Tool-Use and Action-Boundary Security · L85

**THESIS CLAIM**

> ProvenanceGuard (She et al., 2026) formulates misalignment detection as the question of whether a proposed tool call is supported by traceable evidence in the agent's context.

- **→ CITED PAPER:** [PAPER_07 — She et al. (2026) — ProvenanceGuard](PAPER_07.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.6 Tool-Use and Action-Boundary Security, line 85
  - **→ EVIDENCE LOCATION IN PAPER:** arXiv abstract (44.3% to 2.1%)
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
    - Stage 1 claim audit **Ch2-C015**: VERIFIED (support: Full). Evidence: arXiv abstract (44.3% to 2.1%).

### CM-026 · Ch2 §2.6 Tool-Use and Action-Boundary Security · L85

**THESIS CLAIM**

> Compared with an LLM-as-a-judge baseline on Agent-SafetyBench, it reduced the error rate on misaligned traces from 44.3% to 2.1%.

- **→ CITED PAPER:** [PAPER_07 — She et al. (2026) — ProvenanceGuard](PAPER_07.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.6 Tool-Use and Action-Boundary Security, line 85
  - **→ EVIDENCE LOCATION IN PAPER:** figure read in source (Stage 1)
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
    - Stage 1 numerical audit **N041** (figure 44.3%): VERIFIED; figure read in source: Yes.
    - Stage 1 numerical audit **N042** (figure 2.1%): VERIFIED; figure read in source: Yes.

### CM-027 · Ch2 §2.6 Tool-Use and Action-Boundary Security · L87

**THESIS CLAIM**

> The Actuarial Action Interface of H.-H. Chen (2026) takes a consequence-pricing view: agent actions are priced deterministically against reserved capital, and an Authority Frontier measures how much operational authority an agent receives at different budget levels.

- **→ CITED PAPER:** [PAPER_04 — H.-H. Chen (2026)](PAPER_04.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.6 Tool-Use and Action-Boundary Security, line 87
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-008): "arXiv abstract"; reference status VERIFIED.

### CM-028 · Ch2 §2.6 Tool-Use and Action-Boundary Security · L89

**THESIS CLAIM**

> H.-H. Chen (2026) in particular establishes that pricing the consequence of an agent action before execution is not new.

- **→ CITED PAPER:** [PAPER_04 — H.-H. Chen (2026)](PAPER_04.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.6 Tool-Use and Action-Boundary Security, line 89
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-008): "arXiv abstract"; reference status VERIFIED.

### CM-029 · Ch2 §2.6 Tool-Use and Action-Boundary Security · L89

**THESIS CLAIM**

> What that work does not model is an estimated probability that a specific action was induced by an adversary.

- **→ CITED PAPER:** [PAPER_04 — H.-H. Chen (2026)](PAPER_04.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.6 Tool-Use and Action-Boundary Security, line 89
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-008): "arXiv abstract"; reference status VERIFIED.

### CM-030 · Ch2 §2.6 Tool-Use and Action-Boundary Security · L89

**THESIS CLAIM**

> It prices the action's consequence irrespective of how the action arose.

- **→ CITED PAPER:** [PAPER_04 — H.-H. Chen (2026)](PAPER_04.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.6 Tool-Use and Action-Boundary Security, line 89
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-008): "arXiv abstract"; reference status VERIFIED.

### CM-031 · Ch2 §2.7 Financial-Agent Security Requirements · L95

**THESIS CLAIM**

> Z. Chen, J. Chen, et al. (2025) argue that conventional evaluation of financial LLM agents, based on accuracy and return metrics, gives an illusion of reliability while overlooking vulnerabilities such as hallucinated facts, stale data, and adversarial prompt manipulation.

- **→ CITED PAPER:** [PAPER_16 — Z. Chen, J. Chen, et al. (2025)](PAPER_16.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.7 Financial-Agent Security Requirements, line 95
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-006): "arXiv abstract (v2 title and argument)"; reference status VERIFIED.

### CM-032 · Ch2 §2.7 Financial-Agent Security Requirements · L95

**THESIS CLAIM**

> They recommend auditing risk-aware metrics and treating a safety budget as a primary success criterion.

- **→ CITED PAPER:** [PAPER_16 — Z. Chen, J. Chen, et al. (2025)](PAPER_16.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.7 Financial-Agent Security Requirements, line 95
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-006): "arXiv abstract (v2 title and argument)"; reference status VERIFIED.

### CM-033 · Ch2 §2.7 Financial-Agent Security Requirements · L97

**THESIS CLAIM**

> FinHarness (Jia et al., 2026) is the closest domain-specific runtime system.

- **→ CITED PAPER:** [PAPER_18 — Jia et al. (2026) — FinHarness](PAPER_18.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.7 Financial-Agent Security Requirements, line 97
  - **→ EVIDENCE LOCATION IN PAPER:** arXiv abstract (components and numbers)
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
    - Stage 1 claim audit **Ch2-C017**: VERIFIED (support: Full). Evidence: arXiv abstract (components and numbers).

### CM-034 · Ch2 §2.7 Financial-Agent Security Requirements · L97

**THESIS CLAIM**

> It combines a Query Monitor that tracks intent across interactions, a Tool Monitor that assesses each proposed action, and a Cascade that routes verification between lighter and more capable judges.

- **→ CITED PAPER:** [PAPER_18 — Jia et al. (2026) — FinHarness](PAPER_18.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.7 Financial-Agent Security Requirements, line 97
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-025): "arXiv abstract (components and numbers)"; reference status VERIFIED.

### CM-035 · Ch2 §2.7 Financial-Agent Security Requirements · L97

**THESIS CLAIM**

> Its authors report that the routed configuration reduced attack success from 38.3% to 15.0% while largely preserving benign approval, with 4.7 times fewer calls to the advanced judge.

- **→ CITED PAPER:** [PAPER_18 — Jia et al. (2026) — FinHarness](PAPER_18.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.7 Financial-Agent Security Requirements, line 97
  - **→ EVIDENCE LOCATION IN PAPER:** figure read in source (Stage 1)
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
    - Stage 1 numerical audit **N049** (figure 38.3%): VERIFIED; figure read in source: Yes.
    - Stage 1 numerical audit **N050** (figure 15.0%): VERIFIED; figure read in source: Yes.

### CM-036 · Ch2 §2.7 Financial-Agent Security Requirements · L110

**THESIS CLAIM**

> FinHarness addresses it directly, and consequence pricing has been proposed by H.-H. Chen (2026).

- **→ CITED PAPER:** [PAPER_04 — H.-H. Chen (2026)](PAPER_04.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.7 Financial-Agent Security Requirements, line 110
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-008): "arXiv abstract"; reference status VERIFIED.
- **→ CITED PAPER:** [PAPER_18 — Jia et al. (2026) — FinHarness](PAPER_18.md) — named without a citation, in a paragraph that contains citations
  - **→ CHAPTER/SECTION:** Chapter 2, §2.7 Financial-Agent Security Requirements, line 110
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-025): "arXiv abstract (components and numbers)"; reference status VERIFIED.

### CM-037 · Ch2 §2.8 Detection and Classification Approaches · L114

**THESIS CLAIM**

> Rule- and pattern-based detectors, such as AgentTrust's regular-expression features and policies (C. Yang, 2026), are fast and inspectable but bounded by their rule coverage.

- **→ CITED PAPER:** [PAPER_08 — C. Yang (2026) — AgentTrust](PAPER_08.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.8 Detection and Classification Approaches, line 114
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-053): "Full HTML text read"; reference status VERIFIED.

### CM-038 · Ch2 §2.8 Detection and Classification Approaches · L114

**THESIS CLAIM**

> Provenance analysis asks whether an action is supported by evidence (She et al., 2026).

- **→ CITED PAPER:** [PAPER_07 — She et al. (2026) — ProvenanceGuard](PAPER_07.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.8 Detection and Classification Approaches, line 114
  - **→ EVIDENCE LOCATION IN PAPER:** arXiv abstract (44.3% to 2.1%)
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
    - Stage 1 claim audit **Ch2-C020**: VERIFIED (support: Full). Evidence: arXiv abstract (44.3% to 2.1%).

### CM-039 · Ch2 §2.9 Probability Calibration · L122

**THESIS CLAIM**

> Guo et al. (2017) define perfect calibration as agreement between predicted confidence and the probability of being correct, and measure deviation with the expected calibration error (ECE), a weighted average of the gap between accuracy and confidence over equal-width probability bins.

- **→ CITED PAPER:** [PAPER_12 — Guo et al. (2017)](PAPER_12.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.9 Probability Calibration, line 122
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-020): "ar5iv full text: calibration definition, ECE bins, Platt form, NLL fit"; reference status VERIFIED.

### CM-040 · Ch2 §2.9 Probability Calibration · L124

**THESIS CLAIM**

> Platt (1999) fitted a sigmoid to support-vector-machine outputs.

- **→ CITED PAPER:** [PAPER_15 — Platt (1999)](PAPER_15.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.9 Probability Calibration, line 124
  - **→ EVIDENCE LOCATION IN PAPER:** Hosting site certificate error; chapter and pages not confirmed
  - **→ VERIFICATION STATUS:** **UNVERIFIED — source could not be opened**
    - Stage 1 claim audit **Ch2-C022**: UNVERIFIED (support: None). Evidence: Hosting site certificate error; chapter and pages not confirmed.
- **Open item(s):** OI-07 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-041 · Ch2 §2.9 Probability Calibration · L124

**THESIS CLAIM**

> Guo et al. (2017) describe Platt scaling for the binary case as a logistic transformation of the model's score with two parameters fitted by negative log-likelihood on a validation set, a transformation that preserves the ranking of predictions, and they introduce temperature scaling as a one-parameter variant.

- **→ CITED PAPER:** [PAPER_12 — Guo et al. (2017)](PAPER_12.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.9 Probability Calibration, line 124
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-020): "ar5iv full text: calibration definition, ECE bins, Platt form, NLL fit"; reference status VERIFIED.

### CM-042 · Ch2 §2.9 Probability Calibration · L124

**THESIS CLAIM**

> Kull et al. (2017) point out that logistic calibration applied to raw scores in the unit interval cannot represent the identity map and propose beta calibration.

- **→ CITED PAPER:** [PAPER_13 — Kull et al. (2017)](PAPER_13.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.9 Probability Calibration, line 124
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-027): "PMLR PDF text: monotonicity constraint and Proposition 1"; reference status VERIFIED.

### CM-043 · Ch2 §2.9 Probability Calibration · L126

**THESIS CLAIM**

> NEXUS calibrates its logistic-regression risk score with Platt scaling and reports ECE and Brier scores with a reliability diagram (Hossain et al., 2026).

- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.9 Probability Calibration, line 126
  - **→ EVIDENCE LOCATION IN PAPER:** Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) · reference metadata conflict (OI-06)**
    - Stage 1 claim audit **Ch2-C023**: METADATA ERROR (support: Full). Evidence: Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date.

### CM-044 · Ch2 §2.9 Probability Calibration · L126

**THESIS CLAIM**

> C. Zhang et al. (2026) argue that oversight based on a scalar risk score routed through a threshold targets the wrong quantity: what matters for control is the *intervention advantage*, the expected utility gain from intervening rather than continuing.

- **→ CITED PAPER:** [PAPER_09 — C. Zhang et al. (2026) — Calibration is not control](PAPER_09.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.9 Probability Calibration, line 126
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-058): "Full HTML text read"; reference status VERIFIED.

### CM-045 · Ch2 §2.9 Probability Calibration · L126

**THESIS CLAIM**

> Two trajectory states can share a risk estimate while differing in whether they are recoverable.

- **→ CITED PAPER:** [PAPER_09 — C. Zhang et al. (2026) — Calibration is not control](PAPER_09.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.9 Probability Calibration, line 126
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-058): "Full HTML text read"; reference status VERIFIED.

### CM-046 · Ch2 §2.9 Probability Calibration · L126

**THESIS CLAIM**

> In their experiments on ALFWorld, Platt scaling reduced the ECE of a confidence score from 0.463 to 0.006 while control regret under threshold routing remained unchanged at 0.318.

- **→ CITED PAPER:** [PAPER_09 — C. Zhang et al. (2026) — Calibration is not control](PAPER_09.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.9 Probability Calibration, line 126
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-058): "Full HTML text read"; reference status VERIFIED.

### CM-047 · Ch2 §2.9 Probability Calibration · L126

**THESIS CLAIM**

> They propose an action-conditioned controller trained by replaying the agent from identical decision states and executing alternative actions.

- **→ CITED PAPER:** [PAPER_09 — C. Zhang et al. (2026) — Calibration is not control](PAPER_09.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.9 Probability Calibration, line 126
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-058): "Full HTML text read"; reference status VERIFIED.

### CM-048 · Ch2 §2.10 Runtime Decision and Mitigation · L132

**THESIS CLAIM**

> The reviewed systems turn evidence into action in several ways: by rule verdicts with maximum-severity aggregation (C. Yang, 2026), by thresholds on a predicted probability (H. Wang et al., 2025), by a rule cascade gated by a calibrated score (Hossain et al., 2026), by routing verification between judges (Jia et al., 2026), by LLM-based arbitration over candidate recoveries (H. Liu et al., 2026), by deterministic pricing of action consequence (H.-H. Chen, 2026), and by action-conditioned value estimation (C. Zhang et al., 2026).

- **→ CITED PAPER:** [PAPER_08 — C. Yang (2026) — AgentTrust](PAPER_08.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.10 Runtime Decision and Mitigation, line 132
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-053): "Full HTML text read"; reference status VERIFIED.
- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.10 Runtime Decision and Mitigation, line 132
  - **→ EVIDENCE LOCATION IN PAPER:** Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) · reference metadata conflict (OI-06)**
    - Stage 1 claim audit **Ch2-C024**: METADATA ERROR (support: Full). Evidence: Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date.
- **→ CITED PAPER:** [PAPER_18 — Jia et al. (2026) — FinHarness](PAPER_18.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.10 Runtime Decision and Mitigation, line 132
  - **→ EVIDENCE LOCATION IN PAPER:** arXiv abstract (components and numbers)
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
    - Stage 1 claim audit **Ch2-C024**: METADATA ERROR (support: Full). Evidence: arXiv abstract (components and numbers). The row verdict (METADATA ERROR) covers every source cited in the row and reflects Hossain et al. (2026) — NEXUS, not this paper.
- **→ CITED PAPER:** [PAPER_06 — H. Liu et al. (2026) — SafeAgent](PAPER_06.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.10 Runtime Decision and Mitigation, line 132
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-032): "Full HTML text read"; reference status VERIFIED.
- **→ CITED PAPER:** [PAPER_04 — H.-H. Chen (2026)](PAPER_04.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.10 Runtime Decision and Mitigation, line 132
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-008): "arXiv abstract"; reference status VERIFIED.
- **→ CITED PAPER:** [PAPER_09 — C. Zhang et al. (2026) — Calibration is not control](PAPER_09.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.10 Runtime Decision and Mitigation, line 132
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-058): "Full HTML text read"; reference status VERIFIED.
- **Open item(s):** OI-01 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-049 · Ch2 §2.10 Runtime Decision and Mitigation · L134

**THESIS CLAIM**

> Elkan (2001) states that an example should be assigned the prediction with the lowest expected cost, computed from the conditional probability of each class and a cost matrix whose entries give the cost of each prediction for each true class.

- **→ CITED PAPER:** [PAPER_02 — Elkan (2001)](PAPER_02.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.10 Runtime Decision and Mitigation, line 134
  - **→ EVIDENCE LOCATION IN PAPER:** Author PDF: cost convention and Eq. (1) read; page numbers unverified
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch2-C026**: VERIFIED (support: Full). Evidence: Author PDF: cost convention and Eq. (1) read; page numbers unverified.

### CM-050 · Ch2 §2.10 Runtime Decision and Mitigation · L134

**THESIS CLAIM**

> Chow (1970) analyzed the tradeoff between recognition error and rejection, providing the classical basis for withholding an automatic decision.

- **→ CITED PAPER:** [PAPER_01 — Chow (1970)](PAPER_01.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.10 Runtime Decision and Mitigation, line 134
  - **→ EVIDENCE LOCATION IN PAPER:** Crossref metadata only; reject rule not read
  - **→ VERIFICATION STATUS:** **PARTIALLY SUPPORTED — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (metadata only; source text not read)**
    - Stage 1 claim audit **Ch2-C027**: PARTIALLY SUPPORTED (support: Partial). Evidence: Crossref metadata only; reject rule not read.
- **Open item(s):** OI-13 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-051 · Ch2 §2.10 Runtime Decision and Mitigation · L134

**THESIS CLAIM**

> NEXUS defines an expected-loss objective with fixed costs for allow, revise, confirm, and block (Hossain et al., 2026).

- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.10 Runtime Decision and Mitigation, line 134
  - **→ EVIDENCE LOCATION IN PAPER:** Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) · reference metadata conflict (OI-06)**
    - Stage 1 claim audit **Ch2-C028**: METADATA ERROR (support: Full). Evidence: Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date.
- **Open item(s):** OI-01 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-052 · Ch2 §2.10 Runtime Decision and Mitigation · L134

**THESIS CLAIM**

> Its deployed policy, however, is a rule cascade in which the learned score adjudicates particular cases, not a per-decision minimization of conditional risk.

- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 2, §2.10 Runtime Decision and Mitigation, line 134
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-023): "Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date"; reference status PARTIALLY VERIFIED.
- **Open item(s):** OI-01 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-053 · Ch2 §2.10 Runtime Decision and Mitigation · L136

**THESIS CLAIM**

> MI9 uses graduated containment (C. L. Wang et al., 2025); SafeAgent selects among sanitization, replanning, rollback, termination, argument rewriting, and human approval (H. Liu et al., 2026); AgentTrust distinguishes warn and review from allow and block (C. Yang, 2026); NEXUS requests confirmation or revision (Hossain et al., 2026); and Cordon stages effects before commitment (Z. Chen et al., 2026).

- **→ CITED PAPER:** [PAPER_06 — H. Liu et al. (2026) — SafeAgent](PAPER_06.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.10 Runtime Decision and Mitigation, line 136
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-032): "Full HTML text read"; reference status VERIFIED.
- **→ CITED PAPER:** [PAPER_08 — C. Yang (2026) — AgentTrust](PAPER_08.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.10 Runtime Decision and Mitigation, line 136
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-053): "Full HTML text read"; reference status VERIFIED.
- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.10 Runtime Decision and Mitigation, line 136
  - **→ EVIDENCE LOCATION IN PAPER:** Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) · reference metadata conflict (OI-06)**
    - Stage 1 claim audit **Ch2-C029**: METADATA ERROR (support: Full). Evidence: Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date.

### CM-054 · Ch2 §2.10 Runtime Decision and Mitigation · L138

**THESIS CLAIM**

> The second is how effective each intervention actually is: SafeAgent's ablations and the intervention-advantage argument of C. Zhang et al. (2026) both indicate that the value of an intervention depends on what it achieves, not only on the risk estimate that triggered it.

- **→ CITED PAPER:** [PAPER_06 — H. Liu et al. (2026) — SafeAgent](PAPER_06.md) — named without a citation, in a paragraph that contains citations
  - **→ CHAPTER/SECTION:** Chapter 2, §2.10 Runtime Decision and Mitigation, line 138
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-032): "Full HTML text read"; reference status VERIFIED.
- **→ CITED PAPER:** [PAPER_09 — C. Zhang et al. (2026) — Calibration is not control](PAPER_09.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.10 Runtime Decision and Mitigation, line 138
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-058): "Full HTML text read"; reference status VERIFIED.

### CM-055 · Ch2 §2.11 Explainability and Auditability · L142

**THESIS CLAIM**

> Lundberg and Lee (2017) unified such methods under Shapley values and showed that, for a linear model under an assumption of feature independence, the attribution of each feature is its coefficient multiplied by the feature's deviation from its expected value.

- **→ CITED PAPER:** [PAPER_14 — Lundberg & Lee (2017)](PAPER_14.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.11 Explainability and Auditability, line 142
  - **→ EVIDENCE LOCATION IN PAPER:** ar5iv full text: Properties 1-3, Theorem 1, Corollary 1
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch2-C030**: VERIFIED (support: Full). Evidence: ar5iv full text: Properties 1-3, Theorem 1, Corollary 1.

### CM-056 · Ch2 §2.11 Explainability and Auditability · L144

**THESIS CLAIM**

> NEXUS traces each decision to a named rule, an argument-inspector finding, or a calibrated threshold crossing (Hossain et al., 2026).

- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.11 Explainability and Auditability, line 144
  - **→ EVIDENCE LOCATION IN PAPER:** Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) · reference metadata conflict (OI-06)**
    - Stage 1 claim audit **Ch2-C031**: METADATA ERROR (support: Full). Evidence: Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date.

### CM-057 · Ch2 §2.11 Explainability and Auditability · L144

**THESIS CLAIM**

> AgentTrust reports the rules that fired (C. Yang, 2026).

- **→ CITED PAPER:** [PAPER_08 — C. Yang (2026) — AgentTrust](PAPER_08.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.11 Explainability and Auditability, line 144
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-053): "Full HTML text read"; reference status VERIFIED.

### CM-058 · Ch2 §2.11 Explainability and Auditability · L144

**THESIS CLAIM**

> ProvenanceGuard grounds decisions in traceable evidence (She et al., 2026).

- **→ CITED PAPER:** [PAPER_07 — She et al. (2026) — ProvenanceGuard](PAPER_07.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.11 Explainability and Auditability, line 144
  - **→ EVIDENCE LOCATION IN PAPER:** arXiv abstract (44.3% to 2.1%)
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
    - Stage 1 claim audit **Ch2-C032**: VERIFIED (support: Full). Evidence: arXiv abstract (44.3% to 2.1%).

### CM-059 · Ch2 §2.12 Evaluation Benchmarks and Datasets · L156

**THESIS CLAIM**

> | AgentDojo (Debenedetti et al., 2024) | 97 tasks and 629 security test cases across environments including e-banking; extensible to new tasks, defenses, and adaptive attacks | Yes | Open source; security and utility determined by checks on environment state; the banking suite is directly relevant to financial agents |

- **→ CITED PAPER:** [PAPER_17 — Debenedetti et al. (2024) — AgentDojo](PAPER_17.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 2, §2.12 Evaluation Benchmarks and Datasets, line 156
  - **→ EVIDENCE LOCATION IN PAPER:** arXiv abstract; banking suite read in the public repository; figure read in source (Stage 1)
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
    - Stage 1 claim audit **Ch2-C034**: VERIFIED (support: Full). Evidence: arXiv abstract; banking suite read in the public repository.
    - Stage 1 numerical audit **N055** (figure 97): VERIFIED; figure read in source: Yes.
    - Stage 1 numerical audit **N056** (figure 629): VERIFIED; figure read in source: Yes.

### CM-060 · Ch2 §2.12 Evaluation Benchmarks and Datasets · L161

**THESIS CLAIM**

> | NEXUS-Bench (Hossain et al., 2026) | 300/63/128 train/validation/test synthetic instances and further splits | — | Author-generated templates; results described by the authors as upper bounds |

- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 2, §2.12 Evaluation Benchmarks and Datasets, line 161
  - **→ EVIDENCE LOCATION IN PAPER:** Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date; figure not located in source
  - **→ VERIFICATION STATUS:** **UNVERIFIED — figure not read in source**
    - Stage 1 claim audit **Ch2-C039**: METADATA ERROR (support: Full). Evidence: Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date.
    - Stage 1 numerical audit **N067** (figure 128): UNVERIFIED; figure read in source: No.
- **Open item(s):** OI-05 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-061 · Ch2 §2.13 Comparative Synthesis · L182

**THESIS CLAIM**

> | ProvenanceGuard (She et al., 2026) | Evidence support for tool calls | — | — | — | — | — | — |

- **→ CITED PAPER:** [PAPER_07 — She et al. (2026) — ProvenanceGuard](PAPER_07.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 2, §2.13 Comparative Synthesis, line 182
  - **→ EVIDENCE LOCATION IN PAPER:** arXiv abstract (44.3% to 2.1%)
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
    - Stage 1 claim audit **Ch2-C046**: VERIFIED (support: Full). Evidence: arXiv abstract (44.3% to 2.1%).

### CM-062 · Ch2 §2.13 Comparative Synthesis · L183

**THESIS CLAIM**

> | FinHarness (Jia et al., 2026) | Monitors and judge cascade | — | — | — | ✓ (benign approval) | — | ✓ |

- **→ CITED PAPER:** [PAPER_18 — Jia et al. (2026) — FinHarness](PAPER_18.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 2, §2.13 Comparative Synthesis, line 183
  - **→ EVIDENCE LOCATION IN PAPER:** arXiv abstract (components and numbers)
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
    - Stage 1 claim audit **Ch2-C047**: VERIFIED (support: Full). Evidence: arXiv abstract (components and numbers).

### CM-063 · Ch2 §2.13 Comparative Synthesis · L184

**THESIS CLAIM**

> | H.-H. Chen (2026) | Deterministic pricing against reserved capital | — | ✓ | — | — | — | Partial (actuarial framing) |

- **→ CITED PAPER:** [PAPER_04 — H.-H. Chen (2026)](PAPER_04.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 2, §2.13 Comparative Synthesis, line 184
  - **→ EVIDENCE LOCATION IN PAPER:** arXiv abstract
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
    - Stage 1 claim audit **Ch2-C048**: VERIFIED (support: Full). Evidence: arXiv abstract.

### CM-064 · Ch2 §2.13 Comparative Synthesis · L185

**THESIS CLAIM**

> | NEXUS (Hossain et al., 2026) | Rules, argument inspection, calibrated logistic score in a cascade | ✓ | ✓ | ✓ | ✓ (paired benign cases) | ✓ | — |

- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 2, §2.13 Comparative Synthesis, line 185
  - **→ EVIDENCE LOCATION IN PAPER:** Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) · reference metadata conflict (OI-06)**
    - Stage 1 claim audit **Ch2-C049**: METADATA ERROR (support: Full). Evidence: Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date.

### CM-065 · Ch2 §2.13 Comparative Synthesis · L186

**THESIS CLAIM**

> | SafeAgent (H. Liu et al., 2026) | LLM-based operators and policy arbitration | — | ✓ (LLM consequence simulation) | ✓ | ✓ | — | — |

- **→ CITED PAPER:** [PAPER_06 — H. Liu et al. (2026) — SafeAgent](PAPER_06.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 2, §2.13 Comparative Synthesis, line 186
  - **→ EVIDENCE LOCATION IN PAPER:** Full HTML text read
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch2-C050**: VERIFIED (support: Full). Evidence: Full HTML text read.

### CM-066 · Ch2 §2.13 Comparative Synthesis · L187

**THESIS CLAIM**

> | AgentTrust (C. Yang, 2026) | Rules with maximum-severity aggregation | — (heuristic confidence) | ✓ (labeling rubric) | ✓ | — | ✓ | — |

- **→ CITED PAPER:** [PAPER_08 — C. Yang (2026) — AgentTrust](PAPER_08.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 2, §2.13 Comparative Synthesis, line 187
  - **→ EVIDENCE LOCATION IN PAPER:** Full HTML text read
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch2-C051**: VERIFIED (support: Full). Evidence: Full HTML text read.

### CM-067 · Ch2 §2.13 Comparative Synthesis · L188

**THESIS CLAIM**

> | C. Zhang et al. (2026) | Action-conditioned intervention value | Analyzed | — | — | Regret | — | — |

- **→ CITED PAPER:** [PAPER_09 — C. Zhang et al. (2026) — Calibration is not control](PAPER_09.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 2, §2.13 Comparative Synthesis, line 188
  - **→ EVIDENCE LOCATION IN PAPER:** Full HTML text read
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch2-C052**: VERIFIED (support: Full). Evidence: Full HTML text read.

### CM-068 · Ch2 §2.13 Comparative Synthesis · L191

**THESIS CLAIM**

> Calibrated logistic risk scoring and a four-way intervention set appear in NEXUS.

- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — named without a citation, in a paragraph that contains citations
  - **→ CHAPTER/SECTION:** Chapter 2, §2.13 Comparative Synthesis, line 191
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-023): "Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date"; reference status PARTIALLY VERIFIED.

### CM-069 · Ch2 §2.13 Comparative Synthesis · L191

**THESIS CLAIM**

> Consequence-dependent control appears in H.-H. Chen (2026), NEXUS, AgentTrust, and SafeAgent.

- **→ CITED PAPER:** [PAPER_04 — H.-H. Chen (2026)](PAPER_04.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.13 Comparative Synthesis, line 191
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-008): "arXiv abstract"; reference status VERIFIED.
- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — named without a citation, in a paragraph that contains citations
  - **→ CHAPTER/SECTION:** Chapter 2, §2.13 Comparative Synthesis, line 191
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-023): "Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date"; reference status PARTIALLY VERIFIED.
- **→ CITED PAPER:** [PAPER_08 — C. Yang (2026) — AgentTrust](PAPER_08.md) — named without a citation, in a paragraph that contains citations
  - **→ CHAPTER/SECTION:** Chapter 2, §2.13 Comparative Synthesis, line 191
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-053): "Full HTML text read"; reference status VERIFIED.
- **→ CITED PAPER:** [PAPER_06 — H. Liu et al. (2026) — SafeAgent](PAPER_06.md) — named without a citation, in a paragraph that contains citations
  - **→ CHAPTER/SECTION:** Chapter 2, §2.13 Comparative Synthesis, line 191
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-032): "Full HTML text read"; reference status VERIFIED.

### CM-070 · Ch2 §2.13 Comparative Synthesis · L191

**THESIS CLAIM**

> Human review appears in several systems, and latency and component ablation are reported by AgentTrust and NEXUS.

- **→ CITED PAPER:** [PAPER_08 — C. Yang (2026) — AgentTrust](PAPER_08.md) — named without a citation, in a paragraph that contains citations
  - **→ CHAPTER/SECTION:** Chapter 2, §2.13 Comparative Synthesis, line 191
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-053): "Full HTML text read"; reference status VERIFIED.
- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — named without a citation, in a paragraph that contains citations
  - **→ CHAPTER/SECTION:** Chapter 2, §2.13 Comparative Synthesis, line 191
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-023): "Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date"; reference status PARTIALLY VERIFIED.

### CM-071 · Ch2 §2.13 Comparative Synthesis · L191

**THESIS CLAIM**

> Financial runtime safety is addressed by FinHarness.

- **→ CITED PAPER:** [PAPER_18 — Jia et al. (2026) — FinHarness](PAPER_18.md) — named without a citation, in a paragraph that contains citations
  - **→ CHAPTER/SECTION:** Chapter 2, §2.13 Comparative Synthesis, line 191
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-025): "arXiv abstract (components and numbers)"; reference status VERIFIED.

### CM-072 · Ch2 §2.13 Comparative Synthesis · L191

**THESIS CLAIM**

> The limits of calibration for control are established by C. Zhang et al. (2026).

- **→ CITED PAPER:** [PAPER_09 — C. Zhang et al. (2026) — Calibration is not control](PAPER_09.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.13 Comparative Synthesis, line 191
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-058): "Full HTML text read"; reference status VERIFIED.

### CM-073 · Ch2 §2.13 Comparative Synthesis · L193

**THESIS CLAIM**

> NEXUS evaluates plans on author-generated templates and combines its calibrated score with rules through a cascade.

- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — named without a citation, in a paragraph that contains citations
  - **→ CHAPTER/SECTION:** Chapter 2, §2.13 Comparative Synthesis, line 193
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-023): "Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date"; reference status PARTIALLY VERIFIED.
- **Open item(s):** OI-01 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-074 · Ch2 §2.13 Comparative Synthesis · L193

**THESIS CLAIM**

> H.-H. Chen (2026) prices consequence without estimating adversarial induction.

- **→ CITED PAPER:** [PAPER_04 — H.-H. Chen (2026)](PAPER_04.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.13 Comparative Synthesis, line 193
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-008): "arXiv abstract"; reference status VERIFIED.

### CM-075 · Ch2 §2.13 Comparative Synthesis · L193

**THESIS CLAIM**

> FinHarness addresses the financial domain with monitors and judges rather than a calibrated probability and declared losses.

- **→ CITED PAPER:** [PAPER_18 — Jia et al. (2026) — FinHarness](PAPER_18.md) — named without a citation, in a paragraph that contains citations
  - **→ CHAPTER/SECTION:** Chapter 2, §2.13 Comparative Synthesis, line 193
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-025): "arXiv abstract (components and numbers)"; reference status VERIFIED.

### CM-076 · Ch2 §2.13 Comparative Synthesis · L193

**THESIS CLAIM**

> SafeAgent reasons about consequences through an LLM and does not report calibration or latency.

- **→ CITED PAPER:** [PAPER_06 — H. Liu et al. (2026) — SafeAgent](PAPER_06.md) — named without a citation, in a paragraph that contains citations
  - **→ CHAPTER/SECTION:** Chapter 2, §2.13 Comparative Synthesis, line 193
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-032): "Full HTML text read"; reference status VERIFIED.

### CM-077 · Ch2 §2.13 Comparative Synthesis · L193

**THESIS CLAIM**

> AgentTrust does not use a calibrated probability.

- **→ CITED PAPER:** [PAPER_08 — C. Yang (2026) — AgentTrust](PAPER_08.md) — named without a citation, in a paragraph that contains citations
  - **→ CHAPTER/SECTION:** Chapter 2, §2.13 Comparative Synthesis, line 193
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-053): "Full HTML text read"; reference status VERIFIED.

### CM-078 · Ch2 §2.15 Positioning of REM · L210

**THESIS CLAIM**

> - **Relation to C. Zhang et al. (2026).** REM does not claim that calibration improves control. It reports calibration quality and control outcomes separately, and it acknowledges that a scalar probability cannot represent whether an adversarial trajectory remains recoverable.

- **→ CITED PAPER:** [PAPER_09 — C. Zhang et al. (2026) — Calibration is not control](PAPER_09.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.15 Positioning of REM, line 210
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-058): "Full HTML text read"; reference status VERIFIED.

### CM-079 · Ch2 §2.15 Positioning of REM · L211

**THESIS CLAIM**

> - **Relation to H.-H. Chen (2026), SafeAgent, and AgentTrust.** REM does not claim consequence-aware control, human escalation, or component ablation with latency as new.

- **→ CITED PAPER:** [PAPER_04 — H.-H. Chen (2026)](PAPER_04.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 2, §2.15 Positioning of REM, line 211
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-008): "arXiv abstract"; reference status VERIFIED.
- **→ CITED PAPER:** [PAPER_06 — H. Liu et al. (2026) — SafeAgent](PAPER_06.md) — named without a citation, in a paragraph that contains citations
  - **→ CHAPTER/SECTION:** Chapter 2, §2.15 Positioning of REM, line 211
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-032): "Full HTML text read"; reference status VERIFIED.
- **→ CITED PAPER:** [PAPER_08 — C. Yang (2026) — AgentTrust](PAPER_08.md) — named without a citation, in a paragraph that contains citations
  - **→ CHAPTER/SECTION:** Chapter 2, §2.15 Positioning of REM, line 211
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-053): "Full HTML text read"; reference status VERIFIED.

## Chapter 3

### CM-080 · Ch3 §3.1.5 Assumptions · L77

**THESIS CLAIM**

> | AS-5 | Tool outputs and retrieved content are untrusted by default. | Scoping | Follows from the indirect injection threat (Greshake et al., 2023) |

- **→ CITED PAPER:** [PAPER_03 — Greshake et al. (2023)](PAPER_03.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.1.5 Assumptions, line 77
  - **→ EVIDENCE LOCATION IN PAPER:** Crossref metadata and arXiv abstract
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
    - Stage 1 claim audit **Ch3-C003**: VERIFIED (support: Full). Evidence: Crossref metadata and arXiv abstract.

### CM-081 · Ch3 §3.3.1 Protected system · L168

**THESIS CLAIM**

> The evaluation instance is an agent operating the AgentDojo banking environment (Debenedetti et al., 2024), described in Section 3.11.2.

- **→ CITED PAPER:** [PAPER_17 — Debenedetti et al. (2024) — AgentDojo](PAPER_17.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.3.1 Protected system, line 168
  - **→ EVIDENCE LOCATION IN PAPER:** arXiv abstract; banking suite read in the public repository
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
    - Stage 1 claim audit **Ch3-C004**: VERIFIED (support: Full). Evidence: arXiv abstract; banking suite read in the public repository.
- **Open item(s):** OI-14 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-082 · Ch3 §3.3.3 Trust boundaries and untrusted content · L185

**THESIS CLAIM**

> The observation boundary matters because content arriving there enters after the user's request, which is the route exploited by indirect prompt injection (Greshake et al., 2023; OWASP Gen AI Security Project, 2025).

- **→ CITED PAPER:** [PAPER_03 — Greshake et al. (2023)](PAPER_03.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.3.3 Trust boundaries and untrusted content, line 185
  - **→ EVIDENCE LOCATION IN PAPER:** Crossref metadata and arXiv abstract
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
    - Stage 1 claim audit **Ch3-C005**: VERIFIED (support: Full). Evidence: Crossref metadata and arXiv abstract.

### CM-083 · Ch3 §3.7.1 Ridge logistic estimation · L309

**THESIS CLAIM**

> The probability that the proposed action is adversarially induced is modeled by logistic regression (Cox, 1958):

- **→ CITED PAPER:** [PAPER_11 — Cox (1958)](PAPER_11.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.1 Ridge logistic estimation, line 309
  - **→ EVIDENCE LOCATION IN PAPER:** Crossref metadata only; model formulation not read; Paper not read; Crossref record only
  - **→ VERIFICATION STATUS:** **PARTIALLY SUPPORTED — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (metadata only; source text not read)**
    - Stage 1 claim audit **Ch3-C008**: UNVERIFIED (support: None). Evidence: Crossref metadata only; model formulation not read.
    - Stage 1 equation audit **Eq. 3.1** (Logistic model: logit and uncalibrated probability): UNVERIFIED (formulation). Location: Paper not read; Crossref record only.
- **Open item(s):** OI-12 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-084 · Ch3 §3.7.1 Ridge logistic estimation · L316

**THESIS CLAIM**

> *Status:* established from source (Cox, 1958).

- **→ CITED PAPER:** [PAPER_11 — Cox (1958)](PAPER_11.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.1 Ridge logistic estimation, line 316
  - **→ EVIDENCE LOCATION IN PAPER:** Crossref metadata only; model formulation not read; Paper not read; Crossref record only
  - **→ VERIFICATION STATUS:** **PARTIALLY SUPPORTED — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (metadata only; source text not read)**
    - Stage 1 claim audit **Ch3-C009**: PARTIALLY SUPPORTED (support: Partial). Evidence: Crossref metadata only; model formulation not read.
    - Stage 1 equation audit **Eq. 3.1** (Logistic model: logit and uncalibrated probability): UNVERIFIED (formulation). Location: Paper not read; Crossref record only.
- **Open item(s):** OI-12 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-085 · Ch3 §3.7.1 Ridge logistic estimation · L318

**THESIS CLAIM**

> The parameters are estimated offline by maximizing a ridge-penalized log-likelihood (le Cessie & van Houwelingen, 1992):

- **→ CITED PAPER:** [PAPER_10 — le Cessie & van Houwelingen (1992)](PAPER_10.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.1 Ridge logistic estimation, line 318
  - **→ EVIDENCE LOCATION IN PAPER:** Paper not read; Crossref record only
  - **→ VERIFICATION STATUS:** **PARTIALLY SUPPORTED — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (metadata only; source text not read)**
    - Stage 1 equation audit **Eq. 3.2** (Ridge-penalised log-likelihood): UNVERIFIED (formulation). Location: Paper not read; Crossref record only.
- **Open item(s):** OI-10 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-086 · Ch3 §3.7.1 Ridge logistic estimation · L325

**THESIS CLAIM**

> *Status:* established from source.

- **→ CITED PAPER:** [PAPER_10 — le Cessie & van Houwelingen (1992)](PAPER_10.md) — status line of the equation that cites it
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.1 Ridge logistic estimation, line 325
  - **→ EVIDENCE LOCATION IN PAPER:** Paper not read; Crossref record only
  - **→ VERIFICATION STATUS:** **PARTIALLY SUPPORTED — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (metadata only; source text not read)**
    - Stage 1 equation audit **Eq. 3.2** (Ridge-penalised log-likelihood): UNVERIFIED (formulation). Location: Paper not read; Crossref record only.
- **Open item(s):** OI-10 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-087 · Ch3 §3.7.1 Ridge logistic estimation · L329

**THESIS CLAIM**

> The exact scaling constant of the penalty in le Cessie and van Houwelingen (1992) is pending full-text verification.

- **→ CITED PAPER:** [PAPER_10 — le Cessie & van Houwelingen (1992)](PAPER_10.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.1 Ridge logistic estimation, line 329
  - **→ EVIDENCE LOCATION IN PAPER:** Paper not read; Crossref record only
  - **→ VERIFICATION STATUS:** **PARTIALLY SUPPORTED — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (metadata only; source text not read)**
    - Stage 1 equation audit **Eq. 3.2** (Ridge-penalised log-likelihood): UNVERIFIED (formulation). Location: Paper not read; Crossref record only.
- **Open item(s):** OI-10 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-088 · Ch3 §3.7.2 Calibration on the logit · L342

**THESIS CLAIM**

> The method is Platt scaling (Platt, 1999).

- **→ CITED PAPER:** [PAPER_15 — Platt (1999)](PAPER_15.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.2 Calibration on the logit, line 342
  - **→ EVIDENCE LOCATION IN PAPER:** Hosting site certificate error; chapter and pages not confirmed; Platt inaccessible
  - **→ VERIFICATION STATUS:** **UNVERIFIED — source could not be opened**
    - Stage 1 claim audit **Ch3-C010**: UNVERIFIED (support: None). Evidence: Hosting site certificate error; chapter and pages not confirmed.
    - Stage 1 equation audit **Eq. 3.3** (Two-parameter logistic calibration on the logit, slope > 0): VERIFIED (form) / UNVERIFIED (original). Location: Platt inaccessible.
- **Open item(s):** OI-07 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-089 · Ch3 §3.7.2 Calibration on the logit · L342

**THESIS CLAIM**

> The two-parameter logistic form with parameters fitted by negative log-likelihood on held-out data follows Guo et al. (2017).

- **→ CITED PAPER:** [PAPER_12 — Guo et al. (2017)](PAPER_12.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.2 Calibration on the logit, line 342
  - **→ EVIDENCE LOCATION IN PAPER:** Guo §4.1 read
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 equation audit **Eq. 3.3** (Two-parameter logistic calibration on the logit, slope > 0): VERIFIED (form) / UNVERIFIED (original). Location: Guo §4.1 read.

### CM-090 · Ch3 §3.7.2 Calibration on the logit · L342

**THESIS CLAIM**

> The monotonicity condition follows Kull et al. (2017), who require a non-negative slope for a non-decreasing map; REM requires a strictly positive slope so that the ranking of steps is preserved.

- **→ CITED PAPER:** [PAPER_13 — Kull et al. (2017)](PAPER_13.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.2 Calibration on the logit, line 342
  - **→ EVIDENCE LOCATION IN PAPER:** Kull §2.2 and Prop. 1 read
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 equation audit **Eq. 3.3** (Two-parameter logistic calibration on the logit, slope > 0): VERIFIED (form) / UNVERIFIED (original). Location: Kull §2.2 and Prop. 1 read.

### CM-091 · Ch3 §3.7.2 Calibration on the logit · L344

**THESIS CLAIM**

> The calibration parameters are fitted by minimizing the negative log-likelihood on held-out logits (Guo et al., 2017):

- **→ CITED PAPER:** [PAPER_12 — Guo et al. (2017)](PAPER_12.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.2 Calibration on the logit, line 344
  - **→ EVIDENCE LOCATION IN PAPER:** ar5iv full text: calibration definition, ECE bins, Platt form, NLL fit; Full text read
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C011**: VERIFIED (support: Full). Evidence: ar5iv full text: calibration definition, ECE bins, Platt form, NLL fit.
    - Stage 1 equation audit **Eq. 3.4** (Calibration fitted by negative log-likelihood on held-out logits): VERIFIED. Location: Full text read.

### CM-092 · Ch3 §3.7.2 Calibration on the logit · L350

**THESIS CLAIM**

> *Status:* established from source (Guo et al., 2017).

- **→ CITED PAPER:** [PAPER_12 — Guo et al. (2017)](PAPER_12.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.2 Calibration on the logit, line 350
  - **→ EVIDENCE LOCATION IN PAPER:** ar5iv full text: calibration definition, ECE bins, Platt form, NLL fit; Full text read
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C012**: VERIFIED (support: Full). Evidence: ar5iv full text: calibration definition, ECE bins, Platt form, NLL fit.
    - Stage 1 equation audit **Eq. 3.4** (Calibration fitted by negative log-likelihood on held-out logits): VERIFIED. Location: Full text read.

### CM-093 · Ch3 §3.7.2 Calibration on the logit · L355

**THESIS CLAIM**

> Kull et al. (2017) prove that beta calibration with equal shape parameters equals logistic calibration applied to the log-odds of a score.

- **→ CITED PAPER:** [PAPER_13 — Kull et al. (2017)](PAPER_13.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.2 Calibration on the logit, line 355
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-027): "PMLR PDF text: monotonicity constraint and Proposition 1"; reference status VERIFIED.

### CM-094 · Ch3 §3.7.2 Calibration on the logit · L356

**THESIS CLAIM**

> Calibrated logistic risk scores are already used in agent safety (Hossain et al., 2026).

- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.2 Calibration on the logit, line 356
  - **→ EVIDENCE LOCATION IN PAPER:** Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) · reference metadata conflict (OI-06)**
    - Stage 1 claim audit **Ch3-C013**: METADATA ERROR (support: Full). Evidence: Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date.

### CM-095 · Ch3 §3.7.2 Calibration on the logit · L357

**THESIS CLAIM**

> C. Zhang et al. (2026) show that recalibrating a scalar risk score can improve calibration error while leaving control regret under threshold routing unchanged, because a scalar probability does not represent whether an intervention would improve the outcome.

- **→ CITED PAPER:** [PAPER_09 — C. Zhang et al. (2026) — Calibration is not control](PAPER_09.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.2 Calibration on the logit, line 357
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-058): "Full HTML text read"; reference status VERIFIED.

### CM-096 · Ch3 §3.7.5 Expected-loss verdict selection · L426

**THESIS CLAIM**

> Elkan (2001) states that the optimal prediction is the one that minimizes expected cost, computed from the conditional probability of each class and the cost of each prediction for each true class.

- **→ CITED PAPER:** [PAPER_02 — Elkan (2001)](PAPER_02.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.5 Expected-loss verdict selection, line 426
  - **→ EVIDENCE LOCATION IN PAPER:** Author PDF: cost convention and Eq. (1) read; page numbers unverified; Elkan Eq. (1) read on page 1 of the author PDF
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C014**: VERIFIED (support: Full). Evidence: Author PDF: cost convention and Eq. (1) read; page numbers unverified.
    - Stage 1 equation audit **Eq. 3.6** (Conditional risk of a verdict): VERIFIED (criterion). Location: Elkan Eq. (1) read on page 1 of the author PDF.

### CM-097 · Ch3 §3.7.5 Expected-loss verdict selection · L432

**THESIS CLAIM**

> Elkan's criterion is stated for predictions of classes.

- **→ CITED PAPER:** [PAPER_02 — Elkan (2001)](PAPER_02.md) — status line of the equation that cites it
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.5 Expected-loss verdict selection, line 432
  - **→ EVIDENCE LOCATION IN PAPER:** Elkan Eq. (1) read on page 1 of the author PDF
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 equation audit **Eq. 3.6** (Conditional risk of a verdict): VERIFIED (criterion). Location: Elkan Eq. (1) read on page 1 of the author PDF.

### CM-098 · Ch3 §3.7.5 Expected-loss verdict selection · L440

**THESIS CLAIM**

> *Status:* adapted from source; the tie-breaking order is a design definition that makes the rule a function.

- **→ CITED PAPER:** [PAPER_02 — Elkan (2001)](PAPER_02.md) — status line of the equation that cites it
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.5 Expected-loss verdict selection, line 440
  - **→ EVIDENCE LOCATION IN PAPER:** Elkan Eq. (1)
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 equation audit **Eq. 3.7** (Bayes verdict with restrictive tie-breaking): VERIFIED (rule) / REM (tie order). Location: Elkan Eq. (1).

### CM-099 · Ch3 §3.7.5 Expected-loss verdict selection · L456

**THESIS CLAIM**

> It has the form of the standard two-class cost-sensitive threshold for zero-cost correct decisions, which Elkan (2001) obtains from the same expected-cost criterion; the printed threshold expression in that paper could not be inspected directly during verification, so the derivation above stands on Equation 3.8 alone.

- **→ CITED PAPER:** [PAPER_02 — Elkan (2001)](PAPER_02.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.5 Expected-loss verdict selection, line 456
  - **→ EVIDENCE LOCATION IN PAPER:** Author PDF: cost convention and Eq. (1) read; page numbers unverified; Elkan's printed threshold equation not extracted
  - **→ VERIFICATION STATUS:** **PARTLY SUPPORTED — source read, but the specific passage was not inspected**
    - Stage 1 claim audit **Ch3-C015**: VERIFIED (support: Full). Evidence: Author PDF: cost convention and Eq. (1) read; page numbers unverified.
    - Stage 1 equation audit **Eq. 3.9** (Allow-Block threshold p* = C_FA / (C_FA + C_miss)): PARTIALLY VERIFIED. Location: Elkan's printed threshold equation not extracted.
- **Open item(s):** OI-11 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-100 · Ch3 §3.7.5 Expected-loss verdict selection · L460

**THESIS CLAIM**

> Chow (1970) analyzed the tradeoff between recognition error and rejection, which is the classical basis for withholding an automatic decision.

- **→ CITED PAPER:** [PAPER_01 — Chow (1970)](PAPER_01.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.5 Expected-loss verdict selection, line 460
  - **→ EVIDENCE LOCATION IN PAPER:** Crossref metadata only; reject rule not read; Chow not read
  - **→ VERIFICATION STATUS:** **PARTIALLY SUPPORTED — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (metadata only; source text not read)**
    - Stage 1 claim audit **Ch3-C016**: PARTIALLY SUPPORTED (support: Partial). Evidence: Crossref metadata only; reject rule not read.
    - Stage 1 equation audit **Eq. 3.10** (Condition under which Escalate can ever be selected): VERIFIED as a derivation. Location: Chow not read.
- **Open item(s):** OI-13 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-101 · Ch3 §3.7.6 Explainability and audit record · L481

**THESIS CLAIM**

> The attribution follows the linear case of Shapley-value attribution given by Lundberg and Lee (2017):

- **→ CITED PAPER:** [PAPER_14 — Lundberg & Lee (2017)](PAPER_14.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.6 Explainability and audit record, line 481
  - **→ EVIDENCE LOCATION IN PAPER:** ar5iv full text: Properties 1-3, Theorem 1, Corollary 1; Corollary 1 and Property 1 read (ar5iv full text)
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C017**: VERIFIED (support: Full). Evidence: ar5iv full text: Properties 1-3, Theorem 1, Corollary 1.
    - Stage 1 equation audit **Eq. 3.11** (Linear attribution and base value): VERIFIED. Location: Corollary 1 and Property 1 read (ar5iv full text).

### CM-102 · Ch3 §3.7.6 Explainability and audit record · L487

**THESIS CLAIM**

> Lundberg and Lee (2017) state the linear case under feature independence with printed indices that do not match between the two sides of the expression and with base value equal to the model intercept.

- **→ CITED PAPER:** [PAPER_14 — Lundberg & Lee (2017)](PAPER_14.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.6 Explainability and audit record, line 487
  - **→ EVIDENCE LOCATION IN PAPER:** ar5iv full text: Properties 1-3, Theorem 1, Corollary 1; Corollary 1 and Property 1 read (ar5iv full text)
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C018**: VERIFIED (support: Full). Evidence: ar5iv full text: Properties 1-3, Theorem 1, Corollary 1.
    - Stage 1 equation audit **Eq. 3.11** (Linear attribution and base value): VERIFIED. Location: Corollary 1 and Property 1 read (ar5iv full text).

### CM-103 · Ch3 §3.7.6 Explainability and audit record · L493

**THESIS CLAIM**

> This is the local-accuracy property of Lundberg and Lee (2017) for a linear model, and REM checks it as a correctness invariant.

- **→ CITED PAPER:** [PAPER_14 — Lundberg & Lee (2017)](PAPER_14.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.6 Explainability and audit record, line 493
  - **→ EVIDENCE LOCATION IN PAPER:** ar5iv full text: Properties 1-3, Theorem 1, Corollary 1; Property 1 read
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C019**: VERIFIED (support: Full). Evidence: ar5iv full text: Properties 1-3, Theorem 1, Corollary 1.
    - Stage 1 equation audit **Eq. 3.12** (Completeness identity of the attribution): VERIFIED. Location: Property 1 read.

### CM-104 · Ch3 §3.7.6 Explainability and audit record · L506

**THESIS CLAIM**

> Auditable decision records are provided by several existing systems (Hossain et al., 2026; C. Yang, 2026).

- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.6 Explainability and audit record, line 506
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-023): "Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date"; reference status PARTIALLY VERIFIED.
- **→ CITED PAPER:** [PAPER_08 — C. Yang (2026) — AgentTrust](PAPER_08.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.6 Explainability and audit record, line 506
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-053): "Full HTML text read"; reference status VERIFIED.

### CM-105 · Ch3 §3.7.7 Consequence-independent baseline policy · L525

**THESIS CLAIM**

> This contrast is used in the ablation of Section 3.11.7 and is consistent with the finding of C. Zhang et al. (2026) that recalibration need not change threshold-routed control.

- **→ CITED PAPER:** [PAPER_09 — C. Zhang et al. (2026) — Calibration is not control](PAPER_09.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.7.7 Consequence-independent baseline policy, line 525
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-058): "Full HTML text read"; reference status VERIFIED.

### CM-106 · Ch3 §3.11.1 Environment and instrumentation · L645

**THESIS CLAIM**

> REM is evaluated in the banking environment of AgentDojo (Debenedetti et al., 2024), an open-source framework that evaluates both the utility and the security of LLM agents.

- **→ CITED PAPER:** [PAPER_17 — Debenedetti et al. (2024) — AgentDojo](PAPER_17.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.11.1 Environment and instrumentation, line 645
  - **→ EVIDENCE LOCATION IN PAPER:** arXiv abstract; banking suite read in the public repository
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
    - Stage 1 claim audit **Ch3-C021**: VERIFIED (support: Full). Evidence: arXiv abstract; banking suite read in the public repository.
- **Open item(s):** OI-14 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-107 · Ch3 §3.11.1 Environment and instrumentation · L645

**THESIS CLAIM**

> Security is determined by checks on the environment state before and after an episode, and utility by task-specific checks.

- **→ CITED PAPER:** [PAPER_17 — Debenedetti et al. (2024) — AgentDojo](PAPER_17.md) — follows the citation in the same paragraph
  - **→ CHAPTER/SECTION:** Chapter 3, §3.11.1 Environment and instrumentation, line 645
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-014): "arXiv abstract; banking suite read in the public repository"; reference status VERIFIED.

### CM-108 · Ch3 §3.12.2 Secondary metrics · L829

**THESIS CLAIM**

> For binary outcomes, calibration error is measured on the positive-class probability (Naeini et al., 2015) with M equal-width bins (Guo et al., 2017):

- **→ CITED PAPER:** [PAPER_12 — Guo et al. (2017)](PAPER_12.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.12.2 Secondary metrics, line 829
  - **→ EVIDENCE LOCATION IN PAPER:** ar5iv full text: calibration definition, ECE bins, Platt form, NLL fit; Both read in full text
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C029**: VERIFIED (support: Full). Evidence: ar5iv full text: calibration definition, ECE bins, Platt form, NLL fit.
    - Stage 1 equation audit **Eq. 3.20** (Binary expected calibration error with equal-width bins): VERIFIED. Location: Both read in full text.

### CM-109 · Ch3 §3.12.2 Secondary metrics · L835

**THESIS CLAIM**

> Naeini et al. (2015) supply the binary form; Guo et al. (2017) supply the equal-width binning.

- **→ CITED PAPER:** [PAPER_12 — Guo et al. (2017)](PAPER_12.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.12.2 Secondary metrics, line 835
  - **→ EVIDENCE LOCATION IN PAPER:** Both read in full text
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 equation audit **Eq. 3.20** (Binary expected calibration error with equal-width bins): VERIFIED. Location: Both read in full text.

### CM-110 · Ch3 §3.13 Contribution and Novelty Boundaries · L877

**THESIS CLAIM**

> | Logistic regression | Cox (1958) |

- **→ CITED PAPER:** [PAPER_11 — Cox (1958)](PAPER_11.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.13 Contribution and Novelty Boundaries, line 877
  - **→ EVIDENCE LOCATION IN PAPER:** Crossref metadata only; model formulation not read
  - **→ VERIFICATION STATUS:** **PARTIALLY SUPPORTED — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (metadata only; source text not read)**
    - Stage 1 claim audit **Ch3-C031**: PARTIALLY SUPPORTED (support: Partial). Evidence: Crossref metadata only; model formulation not read.
- **Open item(s):** OI-12 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-111 · Ch3 §3.13 Contribution and Novelty Boundaries · L878

**THESIS CLAIM**

> | Ridge regularization of logistic regression | le Cessie and van Houwelingen (1992) |

- **→ CITED PAPER:** [PAPER_10 — le Cessie & van Houwelingen (1992)](PAPER_10.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.13 Contribution and Novelty Boundaries, line 878
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-004): "Crossref metadata only; penalty formulation not read"; reference status PARTIALLY VERIFIED.
- **Open item(s):** OI-10 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-112 · Ch3 §3.13 Contribution and Novelty Boundaries · L879

**THESIS CLAIM**

> | Platt (logistic) calibration | Platt (1999); Guo et al. (2017); Kull et al. (2017) |

- **→ CITED PAPER:** [PAPER_15 — Platt (1999)](PAPER_15.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.13 Contribution and Novelty Boundaries, line 879
  - **→ EVIDENCE LOCATION IN PAPER:** Hosting site certificate error; chapter and pages not confirmed
  - **→ VERIFICATION STATUS:** **UNVERIFIED — source could not be opened**
    - Stage 1 claim audit **Ch3-C032**: UNVERIFIED (support: None). Evidence: Hosting site certificate error; chapter and pages not confirmed.
- **→ CITED PAPER:** [PAPER_12 — Guo et al. (2017)](PAPER_12.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.13 Contribution and Novelty Boundaries, line 879
  - **→ EVIDENCE LOCATION IN PAPER:** ar5iv full text: calibration definition, ECE bins, Platt form, NLL fit
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C032**: UNVERIFIED (support: None). Evidence: ar5iv full text: calibration definition, ECE bins, Platt form, NLL fit. The row verdict (UNVERIFIED) covers every source cited in the row and reflects Platt (1999), not this paper.
- **→ CITED PAPER:** [PAPER_13 — Kull et al. (2017)](PAPER_13.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.13 Contribution and Novelty Boundaries, line 879
  - **→ EVIDENCE LOCATION IN PAPER:** PMLR PDF text: monotonicity constraint and Proposition 1
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C032**: UNVERIFIED (support: None). Evidence: PMLR PDF text: monotonicity constraint and Proposition 1. The row verdict (UNVERIFIED) covers every source cited in the row and reflects Platt (1999), not this paper.
- **Open item(s):** OI-07 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-113 · Ch3 §3.13 Contribution and Novelty Boundaries · L880

**THESIS CLAIM**

> | Linear Shapley attribution | Lundberg and Lee (2017) |

- **→ CITED PAPER:** [PAPER_14 — Lundberg & Lee (2017)](PAPER_14.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.13 Contribution and Novelty Boundaries, line 880
  - **→ EVIDENCE LOCATION IN PAPER:** ar5iv full text: Properties 1-3, Theorem 1, Corollary 1
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C033**: VERIFIED (support: Full). Evidence: ar5iv full text: Properties 1-3, Theorem 1, Corollary 1.

### CM-114 · Ch3 §3.13 Contribution and Novelty Boundaries · L882

**THESIS CLAIM**

> | Expected-cost decisions; reject option | Elkan (2001); Chow (1970) |

- **→ CITED PAPER:** [PAPER_02 — Elkan (2001)](PAPER_02.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.13 Contribution and Novelty Boundaries, line 882
  - **→ EVIDENCE LOCATION IN PAPER:** Author PDF: cost convention and Eq. (1) read; page numbers unverified
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C035**: PARTIALLY SUPPORTED (support: Partial). Evidence: Author PDF: cost convention and Eq. (1) read; page numbers unverified. The row verdict (PARTIALLY SUPPORTED) covers every source cited in the row and reflects Chow (1970), not this paper.
- **→ CITED PAPER:** [PAPER_01 — Chow (1970)](PAPER_01.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.13 Contribution and Novelty Boundaries, line 882
  - **→ EVIDENCE LOCATION IN PAPER:** Crossref metadata only; reject rule not read
  - **→ VERIFICATION STATUS:** **PARTIALLY SUPPORTED — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (metadata only; source text not read)**
    - Stage 1 claim audit **Ch3-C035**: PARTIALLY SUPPORTED (support: Partial). Evidence: Crossref metadata only; reject rule not read.
- **Open item(s):** OI-13 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-115 · Ch3 §3.13 Contribution and Novelty Boundaries · L883

**THESIS CLAIM**

> | Calibrated logistic risk scores for agent safety; four-way intervention | Hossain et al. (2026) |

- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.13 Contribution and Novelty Boundaries, line 883
  - **→ EVIDENCE LOCATION IN PAPER:** Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) · reference metadata conflict (OI-06)**
    - Stage 1 claim audit **Ch3-C036**: METADATA ERROR (support: Full). Evidence: Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date.

### CM-116 · Ch3 §3.13 Contribution and Novelty Boundaries · L884

**THESIS CLAIM**

> | Distinction between calibration and control | C. Zhang et al. (2026) |

- **→ CITED PAPER:** [PAPER_09 — C. Zhang et al. (2026) — Calibration is not control](PAPER_09.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.13 Contribution and Novelty Boundaries, line 884
  - **→ EVIDENCE LOCATION IN PAPER:** Full HTML text read
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C037**: VERIFIED (support: Full). Evidence: Full HTML text read.

### CM-117 · Ch3 §3.13 Contribution and Novelty Boundaries · L885

**THESIS CLAIM**

> | Runtime interception; human review; graduated response | H. Liu et al. (2026); C. Yang (2026); C. L. Wang et al. (2025) |

- **→ CITED PAPER:** [PAPER_06 — H. Liu et al. (2026) — SafeAgent](PAPER_06.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.13 Contribution and Novelty Boundaries, line 885
  - **→ EVIDENCE LOCATION IN PAPER:** Full HTML text read
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C038**: VERIFIED (support: Full). Evidence: Full HTML text read.
- **→ CITED PAPER:** [PAPER_08 — C. Yang (2026) — AgentTrust](PAPER_08.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.13 Contribution and Novelty Boundaries, line 885
  - **→ EVIDENCE LOCATION IN PAPER:** Full HTML text read
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C038**: VERIFIED (support: Full). Evidence: Full HTML text read.

### CM-118 · Ch3 §3.13 Contribution and Novelty Boundaries · L886

**THESIS CLAIM**

> | Provenance analysis of tool calls | She et al. (2026); Debenedetti et al. (2025) |

- **→ CITED PAPER:** [PAPER_07 — She et al. (2026) — ProvenanceGuard](PAPER_07.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.13 Contribution and Novelty Boundaries, line 886
  - **→ EVIDENCE LOCATION IN PAPER:** arXiv abstract (44.3% to 2.1%)
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
    - Stage 1 claim audit **Ch3-C039**: VERIFIED (support: Full). Evidence: arXiv abstract (44.3% to 2.1%).

### CM-119 · Ch3 §3.13 Contribution and Novelty Boundaries · L887

**THESIS CLAIM**

> | Consequence-aware and consequence-priced control | H.-H. Chen (2026); Hossain et al. (2026); C. Yang (2026) |

- **→ CITED PAPER:** [PAPER_04 — H.-H. Chen (2026)](PAPER_04.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.13 Contribution and Novelty Boundaries, line 887
  - **→ EVIDENCE LOCATION IN PAPER:** arXiv abstract
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
    - Stage 1 claim audit **Ch3-C040**: METADATA ERROR (support: Full). Evidence: arXiv abstract. The row verdict (METADATA ERROR) covers every source cited in the row and reflects Hossain et al. (2026) — NEXUS, not this paper.
- **→ CITED PAPER:** [PAPER_05 — Hossain et al. (2026) — NEXUS](PAPER_05.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.13 Contribution and Novelty Boundaries, line 887
  - **→ EVIDENCE LOCATION IN PAPER:** Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) · reference metadata conflict (OI-06)**
    - Stage 1 claim audit **Ch3-C040**: METADATA ERROR (support: Full). Evidence: Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date.
- **→ CITED PAPER:** [PAPER_08 — C. Yang (2026) — AgentTrust](PAPER_08.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.13 Contribution and Novelty Boundaries, line 887
  - **→ EVIDENCE LOCATION IN PAPER:** Full HTML text read
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C040**: METADATA ERROR (support: Full). Evidence: Full HTML text read. The row verdict (METADATA ERROR) covers every source cited in the row and reflects Hossain et al. (2026) — NEXUS, not this paper.

### CM-120 · Ch3 §3.13 Contribution and Novelty Boundaries · L888

**THESIS CLAIM**

> | Component ablation with latency | C. Yang (2026) |

- **→ CITED PAPER:** [PAPER_08 — C. Yang (2026) — AgentTrust](PAPER_08.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.13 Contribution and Novelty Boundaries, line 888
  - **→ EVIDENCE LOCATION IN PAPER:** Full HTML text read
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C041**: VERIFIED (support: Full). Evidence: Full HTML text read.

### CM-121 · Ch3 §3.13 Contribution and Novelty Boundaries · L889

**THESIS CLAIM**

> | Runtime protection of financial agents | Jia et al. (2026) |

- **→ CITED PAPER:** [PAPER_18 — Jia et al. (2026) — FinHarness](PAPER_18.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.13 Contribution and Novelty Boundaries, line 889
  - **→ EVIDENCE LOCATION IN PAPER:** arXiv abstract (components and numbers)
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
    - Stage 1 claim audit **Ch3-C042**: VERIFIED (support: Full). Evidence: arXiv abstract (components and numbers).

### CM-122 · Ch3 §3.14 Threats to Validity · L936

**THESIS CLAIM**

> A scalar probability cannot represent whether an adversarial trajectory remains recoverable, so REM inherits the limitation identified by C. Zhang et al. (2026); estimating intervention value by counterfactual replay is outside the scope of this thesis.

- **→ CITED PAPER:** [PAPER_09 — C. Zhang et al. (2026) — Calibration is not control](PAPER_09.md) — cited in this sentence
  - **→ CHAPTER/SECTION:** Chapter 3, §3.14 Threats to Validity, line 936
  - **→ EVIDENCE LOCATION IN PAPER:** Not documented for this claim.
  - **→ VERIFICATION STATUS:** **NOT AUDITED AT CLAIM LEVEL**. Reference-level record only (Stage 1 master, REF-058): "Full HTML text read"; reference status VERIFIED.

### CM-123 · Ch3 §3.15 Equation Provenance Summary · L944

**THESIS CLAIM**

> | 3.1 | Logistic model | Established | Cox (1958) | IV |

- **→ CITED PAPER:** [PAPER_11 — Cox (1958)](PAPER_11.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.15 Equation Provenance Summary, line 944
  - **→ EVIDENCE LOCATION IN PAPER:** Crossref metadata only; model formulation not read; Paper not read; Crossref record only
  - **→ VERIFICATION STATUS:** **PARTIALLY SUPPORTED — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (metadata only; source text not read)**
    - Stage 1 claim audit **Ch3-C043**: PARTIALLY SUPPORTED (support: Partial). Evidence: Crossref metadata only; model formulation not read.
    - Stage 1 equation audit **Eq. 3.1** (Logistic model: logit and uncalibrated probability): UNVERIFIED (formulation). Location: Paper not read; Crossref record only.
- **Open item(s):** OI-12 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-124 · Ch3 §3.15 Equation Provenance Summary · L945

**THESIS CLAIM**

> | 3.2 | Ridge-penalized log-likelihood | Established | le Cessie & van Houwelingen (1992) | IV (penalty constant pending) |

- **→ CITED PAPER:** [PAPER_10 — le Cessie & van Houwelingen (1992)](PAPER_10.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.15 Equation Provenance Summary, line 945
  - **→ EVIDENCE LOCATION IN PAPER:** Paper not read; Crossref record only
  - **→ VERIFICATION STATUS:** **PARTIALLY SUPPORTED — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (metadata only; source text not read)**
    - Stage 1 equation audit **Eq. 3.2** (Ridge-penalised log-likelihood): UNVERIFIED (formulation). Location: Paper not read; Crossref record only.
- **Open item(s):** OI-10 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-125 · Ch3 §3.15 Equation Provenance Summary · L946

**THESIS CLAIM**

> | 3.3 | Logistic calibration on the logit, γ_{1} > 0 | Adapted | Platt (1999); Guo et al. (2017); Kull et al. (2017) | Platt NC; Guo FV; Kull FV |

- **→ CITED PAPER:** [PAPER_15 — Platt (1999)](PAPER_15.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.15 Equation Provenance Summary, line 946
  - **→ EVIDENCE LOCATION IN PAPER:** Hosting site certificate error; chapter and pages not confirmed; Platt inaccessible
  - **→ VERIFICATION STATUS:** **UNVERIFIED — source could not be opened**
    - Stage 1 claim audit **Ch3-C044**: UNVERIFIED (support: None). Evidence: Hosting site certificate error; chapter and pages not confirmed.
    - Stage 1 equation audit **Eq. 3.3** (Two-parameter logistic calibration on the logit, slope > 0): VERIFIED (form) / UNVERIFIED (original). Location: Platt inaccessible.
- **→ CITED PAPER:** [PAPER_12 — Guo et al. (2017)](PAPER_12.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.15 Equation Provenance Summary, line 946
  - **→ EVIDENCE LOCATION IN PAPER:** ar5iv full text: calibration definition, ECE bins, Platt form, NLL fit; Guo §4.1 read
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C044**: UNVERIFIED (support: None). Evidence: ar5iv full text: calibration definition, ECE bins, Platt form, NLL fit. The row verdict (UNVERIFIED) covers every source cited in the row and reflects Platt (1999), not this paper.
    - Stage 1 equation audit **Eq. 3.3** (Two-parameter logistic calibration on the logit, slope > 0): VERIFIED (form) / UNVERIFIED (original). Location: Guo §4.1 read.
- **→ CITED PAPER:** [PAPER_13 — Kull et al. (2017)](PAPER_13.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.15 Equation Provenance Summary, line 946
  - **→ EVIDENCE LOCATION IN PAPER:** PMLR PDF text: monotonicity constraint and Proposition 1; Kull §2.2 and Prop. 1 read
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C044**: UNVERIFIED (support: None). Evidence: PMLR PDF text: monotonicity constraint and Proposition 1. The row verdict (UNVERIFIED) covers every source cited in the row and reflects Platt (1999), not this paper.
    - Stage 1 equation audit **Eq. 3.3** (Two-parameter logistic calibration on the logit, slope > 0): VERIFIED (form) / UNVERIFIED (original). Location: Kull §2.2 and Prop. 1 read.
- **Open item(s):** OI-07 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-126 · Ch3 §3.15 Equation Provenance Summary · L947

**THESIS CLAIM**

> | 3.4 | Calibration fit by negative log-likelihood | Established | Guo et al. (2017) | FV |

- **→ CITED PAPER:** [PAPER_12 — Guo et al. (2017)](PAPER_12.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.15 Equation Provenance Summary, line 947
  - **→ EVIDENCE LOCATION IN PAPER:** ar5iv full text: calibration definition, ECE bins, Platt form, NLL fit; Full text read
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C045**: VERIFIED (support: Full). Evidence: ar5iv full text: calibration definition, ECE bins, Platt form, NLL fit.
    - Stage 1 equation audit **Eq. 3.4** (Calibration fitted by negative log-likelihood on held-out logits): VERIFIED. Location: Full text read.

### CM-127 · Ch3 §3.15 Equation Provenance Summary · L949

**THESIS CLAIM**

> | 3.6 | Conditional risk | Adapted | Elkan (2001) | FV (Eq. 1 form) |

- **→ CITED PAPER:** [PAPER_02 — Elkan (2001)](PAPER_02.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.15 Equation Provenance Summary, line 949
  - **→ EVIDENCE LOCATION IN PAPER:** Author PDF: cost convention and Eq. (1) read; page numbers unverified; Elkan Eq. (1) read on page 1 of the author PDF
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C046**: VERIFIED (support: Full). Evidence: Author PDF: cost convention and Eq. (1) read; page numbers unverified.
    - Stage 1 equation audit **Eq. 3.6** (Conditional risk of a verdict): VERIFIED (criterion). Location: Elkan Eq. (1) read on page 1 of the author PDF.

### CM-128 · Ch3 §3.15 Equation Provenance Summary · L950

**THESIS CLAIM**

> | 3.7 | Bayes verdict with tie-breaking | Adapted | Elkan (2001) | FV; tie order DEF |

- **→ CITED PAPER:** [PAPER_02 — Elkan (2001)](PAPER_02.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.15 Equation Provenance Summary, line 950
  - **→ EVIDENCE LOCATION IN PAPER:** Author PDF: cost convention and Eq. (1) read; page numbers unverified; Elkan Eq. (1)
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C047**: VERIFIED (support: Full). Evidence: Author PDF: cost convention and Eq. (1) read; page numbers unverified.
    - Stage 1 equation audit **Eq. 3.7** (Bayes verdict with restrictive tie-breaking): VERIFIED (rule) / REM (tie order). Location: Elkan Eq. (1).

### CM-129 · Ch3 §3.15 Equation Provenance Summary · L952

**THESIS CLAIM**

> | 3.9 | Allow–Block threshold | Derived | From Eq. 3.8; consistent with Elkan (2001) | DER |

- **→ CITED PAPER:** [PAPER_02 — Elkan (2001)](PAPER_02.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.15 Equation Provenance Summary, line 952
  - **→ EVIDENCE LOCATION IN PAPER:** Author PDF: cost convention and Eq. (1) read; page numbers unverified; Elkan's printed threshold equation not extracted
  - **→ VERIFICATION STATUS:** **PARTLY SUPPORTED — source read, but the specific passage was not inspected**
    - Stage 1 claim audit **Ch3-C048**: VERIFIED (support: Full). Evidence: Author PDF: cost convention and Eq. (1) read; page numbers unverified.
    - Stage 1 equation audit **Eq. 3.9** (Allow-Block threshold p* = C_FA / (C_FA + C_miss)): PARTIALLY VERIFIED. Location: Elkan's printed threshold equation not extracted.
- **Open item(s):** OI-11 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-130 · Ch3 §3.15 Equation Provenance Summary · L953

**THESIS CLAIM**

> | 3.10 | Escalation feasibility condition | Derived | From Eqs. 3.6, 3.7, 3.9; Chow (1970) conceptual basis | DER; Chow IV |

- **→ CITED PAPER:** [PAPER_01 — Chow (1970)](PAPER_01.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.15 Equation Provenance Summary, line 953
  - **→ EVIDENCE LOCATION IN PAPER:** Crossref metadata only; reject rule not read; Chow not read
  - **→ VERIFICATION STATUS:** **PARTIALLY SUPPORTED — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (metadata only; source text not read)**
    - Stage 1 claim audit **Ch3-C049**: PARTIALLY SUPPORTED (support: Partial). Evidence: Crossref metadata only; reject rule not read.
    - Stage 1 equation audit **Eq. 3.10** (Condition under which Escalate can ever be selected): VERIFIED as a derivation. Location: Chow not read.
- **Open item(s):** OI-13 — see `../THESIS_READING_INDEX.md` Section 6.

### CM-131 · Ch3 §3.15 Equation Provenance Summary · L954

**THESIS CLAIM**

> | 3.11 | Linear attribution | Adapted | Lundberg & Lee (2017) | FV |

- **→ CITED PAPER:** [PAPER_14 — Lundberg & Lee (2017)](PAPER_14.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.15 Equation Provenance Summary, line 954
  - **→ EVIDENCE LOCATION IN PAPER:** ar5iv full text: Properties 1-3, Theorem 1, Corollary 1; Corollary 1 and Property 1 read (ar5iv full text)
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C050**: VERIFIED (support: Full). Evidence: ar5iv full text: Properties 1-3, Theorem 1, Corollary 1.
    - Stage 1 equation audit **Eq. 3.11** (Linear attribution and base value): VERIFIED. Location: Corollary 1 and Property 1 read (ar5iv full text).

### CM-132 · Ch3 §3.15 Equation Provenance Summary · L955

**THESIS CLAIM**

> | 3.12 | Completeness identity | Derived | Lundberg & Lee (2017) local accuracy | FV + DER |

- **→ CITED PAPER:** [PAPER_14 — Lundberg & Lee (2017)](PAPER_14.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.15 Equation Provenance Summary, line 955
  - **→ EVIDENCE LOCATION IN PAPER:** ar5iv full text: Properties 1-3, Theorem 1, Corollary 1; Property 1 read
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C051**: VERIFIED (support: Full). Evidence: ar5iv full text: Properties 1-3, Theorem 1, Corollary 1.
    - Stage 1 equation audit **Eq. 3.12** (Completeness identity of the attribution): VERIFIED. Location: Property 1 read.

### CM-133 · Ch3 §3.15 Equation Provenance Summary · L963

**THESIS CLAIM**

> | 3.20 | Expected calibration error | Adapted | Naeini et al. (2015); Guo et al. (2017) | FV |

- **→ CITED PAPER:** [PAPER_12 — Guo et al. (2017)](PAPER_12.md) — cited in this table row
  - **→ CHAPTER/SECTION:** Chapter 3, §3.15 Equation Provenance Summary, line 963
  - **→ EVIDENCE LOCATION IN PAPER:** ar5iv full text: calibration definition, ECE bins, Platt form, NLL fit; Both read in full text
  - **→ VERIFICATION STATUS:** **SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment)**
    - Stage 1 claim audit **Ch3-C055**: VERIFIED (support: Full). Evidence: ar5iv full text: calibration definition, ECE bins, Platt form, NLL fit.
    - Stage 1 equation audit **Eq. 3.20** (Binary expected calibration error with equal-width bins): VERIFIED. Location: Both read in full text.

