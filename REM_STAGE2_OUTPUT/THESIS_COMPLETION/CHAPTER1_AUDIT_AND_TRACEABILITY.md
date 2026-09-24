# Chapter 1: Audit Report and Traceability

**Chapter:** `CHAPTER1_INTRODUCTION.md` / `.docx`
**Written after:** Chapters 4 and 5 were stabilized, as the task required
**Date:** 24 September 2026

---

## 1. Audit result

| Check | Result |
|---|---|
| Built from Chapters 2–5 | Pass. Every section cites the Chapter 2, 3, 4 or 5 section it summarizes. |
| Research direction unchanged | Pass. The problem, gap, objectives and approach are those of Chapters 2 and 3. |
| No new objective | Pass. O1–O3 are quoted verbatim from Chapter 3 §3.1.2. |
| Research aim | Flagged. No approved aim statement is on record. §1.5 states that the aim is *derived* from O1–O3 and adds nothing to them. SUPERVISOR CONFIRMATION RECOMMENDED. |
| Research questions | Pass. RQ1–RQ4 are quoted verbatim from Chapter 3 §3.1.3 and marked [PD] pending supervisor confirmation. |
| Research variables | Pass. No research variables are defined or introduced. The chapter adds no variable beyond the quantities of Chapter 3. |
| Architecture | Pass. Exactly five layers. Offline fitting and recalibration are cross-cutting, not a layer. Attribution is audit-only. |
| Novelty wording | Pass. The contribution is stated as "empirical and integrative", and the "not claimed" list is carried from Chapter 3 §3.13. None of the prohibited terms appears ("first-ever", "novel algorithm", "state-of-the-art", "best", "superior", "guaranteed", "solves prompt injection"). |
| Prior-art collision visible | Pass. NEXUS, AgentTrust, H.-H. Chen, FinHarness and C. Zhang et al. are named in §1.4. The NEXUS distinction is worded as in Chapter 2: an expected-loss objective is defined, and the deployed policy is a rule cascade. |
| Financial specialization | Pass. The financial execution context is kept throughout (§§1.1–1.3, 1.6, 1.10). Task automation is noted as outside the evaluation scope, as in Chapter 3. |
| Evidence status stated | Pass. §1.12 reports that the evaluation has not been executed and that O2, O3 and RQ1–RQ4 have no empirical results. It names the six specification conflicts. |
| Thesis organization | Flagged. The five-chapter structure follows the task instruction. §1.13 discloses that Chapter 3's cross-references assume a six-chapter structure (SD-STRUCT; SUPERVISOR DECISION REQUIRED). |
| Equations | Pass. None. |
| Numerical claims | Pass. No benchmark rates or performance figures are quoted. The only numbers are structural: five layers, four verdicts, 154 tests (from Chapter 4, E1). |
| References | Pass. All 26 entries are reproduced verbatim from the Chapter 2 or Chapter 3 reference lists (checked automatically), and every entry is cited in the text. |
| No "you/your"; formal register | Pass. |

## 2. Traceability table

| Chapter statement / section | Source | Evidence type | Verification status | Notes |
|---|---|---|---|---|
| §1.1 Agent definition; ReAct loop | Chapter 2 §2.2; L. Wang et al. (2024); Yao et al. (2023) | Chapter 2; literature | L. Wang PARTIALLY VERIFIED (REF-047); Yao VERIFIED (REF-055) | |
| §1.1 Financial tool effects; say versus do | Chapter 2 §2.1 | Chapter text | Verified | |
| §1.2 Input channels; indirect injection definition | Chapter 2 §§2.2–2.3; OWASP (2025); Greshake et al. (2023) | Chapter 2; literature | OWASP VERIFIED (REF-042); Greshake VERIFIED (REF-019) | |
| §1.2 Benchmarks establish the threat; rates not poolable | Chapter 2 §2.3; Debenedetti et al. (2024); Zhan et al. (2024); H. Zhang et al. (2025) | Chapter 2; literature | VERIFIED (REF-014, REF-056, REF-057) | No rates quoted |
| §1.2 Action boundary as the last preventable point | Chapter 2 §2.6 | Chapter text | Verified | |
| §1.2 Two open questions | Chapter 2 §2.10 synthesis | Chapter text | Verified | |
| §1.2 Problem statement | Chapter 3 Table 3.1 ("Runtime compromise of tool-using financial agents through indirect prompt injection") | Chapter text | Verified | |
| §1.3 Financial consequences; evaluation illusion | Chapter 2 §2.7; Z. Chen, J. Chen, et al. (2025) | Chapter 2; literature | VERIFIED (REF-006) | |
| §1.3 EU regulation, Articles 12 and 14 (as motivation only) | Chapter 2 §2.7; European Parliament & Council (2024) | Chapter 2; regulation | PARTIALLY VERIFIED (REF-039) | High-risk status of an agent not assessed, as in Chapter 2 |
| §1.3 Evaluation fragility | Chapter 2 §2.8; Arp et al. (2022); Y. Wang et al. (2026); M. Q. Li et al. (2026) | Chapter 2; literature | VERIFIED (REF-001, REF-051, REF-029) | |
| §1.4 Gap statement and bounds | Chapter 2 §2.14 | Chapter text | Verified; bound to the September 2026 update | |
| §1.4 NEXUS description | Chapter 2 §2.4.4, §2.10; Hossain et al. (2026) | Chapter 2; literature | PARTIALLY VERIFIED (REF-023); OI-01 open | Distinction preserved; no NEXUS numbers quoted |
| §1.4 AgentTrust, H.-H. Chen, FinHarness, C. Zhang | Chapter 2 §§2.4.4, 2.6, 2.7, 2.9 | Chapter 2; literature | VERIFIED (REF-053, REF-008, REF-025, REF-058) | |
| §1.5 Aim | Derived from O1–O3 (Chapter 3 §3.1.2) | Derived | Stated as derived | No approved aim on record |
| §1.6 O1–O3 | Chapter 3 §3.1.2 | Quotation | Verified (approved proposal itself not on record) | |
| §1.7 RQ1–RQ4 | Chapter 3 §3.1.3 | Quotation | [PD] | |
| §1.8 Five layers; opaque agent | Chapter 3 §3.2.1, §3.3.1 | Chapter text | Verified | |
| §1.8 Estimator, calibration, decision sources | Chapter 3 §3.7; Cox (1958); le Cessie & van Houwelingen (1992); Platt (1999); Guo et al. (2017); Elkan (2001); Chow (1970); Lundberg & Lee (2017) | Chapter 3; literature | Cox, le Cessie, Chow PARTIALLY VERIFIED; Platt PARTIALLY VERIFIED with UNRESOLVED CITATION CONFLICT (OI-07); Guo, Elkan, Lundberg VERIFIED | Attribution as in Chapter 3 |
| §1.8 Thresholds as consequences of costs | Chapter 3 §3.7.5 (Eqs. 3.8–3.9) | Chapter text | DER; Eq. 3.9 SOURCE NOT FULLY VERIFIED | Stated in words; no equation displayed |
| §1.9 Design science; Peffers activities | Chapter 3 §3.1.1; Hevner et al. (2004); Peffers et al. (2007) | Chapter 3; literature | PARTIALLY VERIFIED (REF-021, REF-040; metadata only, CF-04, CF-05) | |
| §1.9 Baseline logic; grouped cross-fitting | Chapter 3 §3.1.1, §§3.11.4–3.11.5 | Chapter text | Verified | |
| §1.10 Scope lists; AS-1, AS-3, AS-6 | Chapter 3 §3.1.4, Table 3.3 | Chapter text | Verified | |
| §1.11 Contribution and "not claimed" list | Chapter 3 §3.13, Table 3.16 | Chapter text | Verified | |
| §1.12 Current status | Chapter 4 §§4.6, 4.7, 4.12, 4.16; Chapter 5 §5.2; E1 | Chapters 4–5; artifacts | Verified | |
| §1.13 Organization; six-chapter references in Chapter 3 | Chapter 3 Table 3.1, §3.16 | Chapter text | Verified | SD-STRUCT |

## 3. Items requiring supervisor confirmation

1. The derived aim statement (§1.5).
2. RQ1–RQ4 (§1.7).
3. The five-chapter structure versus the Chapter 3 cross-references (SD-STRUCT).
4. The thesis title. No title is given in Chapter 1, because none is approved on record (`SUPERVISOR_DECISIONS_REQUIRED.md`, TITLE).
