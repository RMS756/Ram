# Chapter 5: Audit Report and Traceability

**Chapter:** `CHAPTER5_DISCUSSION_CONCLUSIONS.md` / `.docx`
**Built on:** the stabilized Chapter 4 (`CHAPTER4_IMPLEMENTATION_EXPERIMENTAL_DESIGN_RESULTS.md`)
**Date:** 24 September 2026

---

## 1. Audit result

| Check | Result |
|---|---|
| Evidence basis | Pass. Every finding in §5.1 traces to a Chapter 4 section and, through it, to code, tests or evidence files. There are no empirical findings, because Chapter 4 reports none. |
| Terminology consistency with Chapters 2–4 | Pass. |
| Architecture consistency | Pass. Five layers. SC-6 is noted, not resolved. |
| Algorithm and equation consistency | Pass. No equation is displayed or introduced. Chapter 3 equations are referred to by number. The source status of Eqs. 3.9 and 3.10 is stated as SOURCE NOT FULLY VERIFIED. |
| Objectives mapping | Pass. O1–O3 are quoted as in Chapter 3 §3.1.2. RQ1–RQ4 are marked [PD]. O2 and O3 are reported as not met. |
| Comparison with prior work | Pass. Design-level only, from Chapter 2. No ranking, and none of the words "best", "superior" or "state-of-the-art". The NEXUS distinction is preserved exactly: NEXUS *defines* an expected-loss objective with fixed costs, and its deployed policy is a rule cascade. The chapter does not state that NEXUS lacks expected loss. OI-01 to OI-05 are cited. |
| Demonstrated versus intended protection | Pass (Table 5.4). |
| Limitations | Pass. All required categories are covered: dataset size, threat coverage, external validity, implementation maturity, computational measurement, specification conflicts, reference verification, missing experiments. |
| Threats to validity | Pass. Limited to the verification study. The threats to the planned evaluation are referred to Chapter 3 §3.14, not restated as findings. |
| Practical implications | Pass. "Not ready for deployment" is stated. Every condition is traced to a Chapter 3 assumption or open item. |
| Future work | Pass. Each item follows from a §5.5 limitation. The out-of-scope extensions are those listed in Chapter 3 §3.1.4. |
| Conclusion | Pass. Limited to three demonstrated statements and one statement of what remains. |
| No-hallucination audit | Pass. No numerical claim other than the counts carried from Chapter 4 and Chapter 3 (37 references, 15 partially verified; 16/9 templates; 154 tests; Python and NumPy versions). |
| Supervisor issues visible | Pass. SC-1 to SC-6, SD-FREEZE and SD-STRUCT are named in §5.5, and RQ confirmation in §5.2. |

## 2. Traceability table

| Chapter statement / section | Source | Evidence type | Verification status | Notes |
|---|---|---|---|---|
| Intro: 154 passing tests; no empirical evaluation | Chapter 4 §4.1.1, §4.12; E1, E4 | Chapter 4 and artifacts | Verified | |
| §5.1.1 (1) Eqs. 3.1, 3.3, 3.6, 3.7 realized and hand-verified | Chapter 4 §4.6; `tests/test_frozen_math.py` | Tests | Verified | |
| §5.1.1 (2) Separation of quantities enforced | Chapter 4 §4.6.2–4.6.5; tests named there | Tests | Verified | |
| §5.1.1 (3) Refusal to substitute values | Chapter 4 §4.2.5, §4.14; E3, E4 | Run output | Verified | |
| §5.1.1 (4) Five layers in code | Chapter 4 §4.2.3 | Tests | Verified | |
| §5.1.2 Fixture test is not protection evidence | `tests/test_pipeline.py` module docstring | Code | Verified | |
| §5.1.3 Eqs. 3.8–3.10 derived; dominance check | Chapter 3 §3.7.5, Table 3.17 | Chapter text | DER; Eqs. 3.9–3.10 SOURCE NOT FULLY VERIFIED | |
| §5.1.3 Tie order at the equality case of Eq. 3.10 | Chapter 3 §3.7.5 ("at equality, ties resolve toward Block") | Chapter text | Verified | SC-2 |
| Table 5.1 O1–O3 wording | Chapter 3 §3.1.2 | Chapter text | Quoted | Approved proposal not on record |
| Table 5.1 RQ status [PD] | Chapter 3 §3.1.3 | Chapter text | Verified | |
| Table 5.2 SO-1 to SO-6 status | Chapter 3 §3.3.7; Chapter 4 Tables 4.6–4.8, 4.12 | Chapter text and code | Verified | |
| Table 5.3 NEXUS row | Chapter 2 §2.4.4, §2.10; OI-01 to OI-05 | Chapter 2; reading index | NEXUS reference PARTIALLY VERIFIED (REF-023); OI-01 open | The distinction is worded as in Chapter 2 |
| Table 5.3 AgentTrust row | Chapter 2 §2.4.4; Chapter 3 Table 3.16 | Chapter text | VERIFIED (REF-053) | |
| Table 5.3 SafeAgent row | Chapter 2 §2.4.4; `CLAUDE.md` (LLM arbitration excluded) | Chapter text; contract | VERIFIED (REF-032) | |
| Table 5.3 ProvenanceGuard row | Chapter 2 §2.6; Chapter 3 Tables 3.9, 3.16 | Chapter text | VERIFIED (REF-045) | |
| Table 5.3 H.-H. Chen row | Chapter 2 §2.6 | Chapter text | VERIFIED (REF-008) | |
| Table 5.3 FinHarness row | Chapter 2 §2.7 | Chapter text | VERIFIED (REF-025) | |
| Table 5.3 C. Zhang row | Chapter 2 §2.9; Chapter 3 §3.7.2, §3.14 | Chapter text | VERIFIED (REF-058) | |
| §5.3 "each mechanism has precedent" | Chapter 2 §2.13; Chapter 3 Table 3.16 | Chapter text | Verified | |
| Table 5.4 Demonstrated column | Chapter 4 §4.3, §4.6, §4.7 | Code and tests | Verified | |
| §5.5 Limitations | Chapter 4 Tables 4.16–4.17; Chapter 3 §§3.11.4, 3.11.9, 3.14; `SUPERVISOR_DECISIONS_REQUIRED.md`; reference records | Mixed | Verified against the sources named | 37 / 15 counts: `THESIS_READING_INDEX.md` |
| §5.6 Threats | Chapter 4 §4.12.2, Table 4.16 F-10; E5 | Chapter 4; artifacts | Verified | |
| §5.7 Conditions | Chapter 3 AS-1, AS-2, AS-3, §3.7.3, Table 3.12, §3.11.7; Chapter 2 §2.7 | Chapter text | Verified | |
| §5.8 Future work | §5.5; Chapter 3 §3.1.4 | Chapter text | Verified | |
| §5.9 Conclusion | §5.1; Chapter 4 | Derived | Verified | |

## 3. Citation tracking

| Citation key | Source title | Source type | Verification status | Where used | Claim supported |
|---|---|---|---|---|---|
| Hossain et al. (2026) | NEXUS | Preprint | PARTIALLY VERIFIED (REF-023); OI-01 to OI-06 open | Table 5.3 | Design of NEXUS as documented in Chapter 2 |
| C. Yang (2026) | AgentTrust | Preprint | VERIFIED (REF-053) | Table 5.3 | Design of AgentTrust as documented in Chapter 2 |
| H. Liu et al. (2026) | SafeAgent | Preprint | VERIFIED (REF-032) | Table 5.3 | Design of SafeAgent as documented in Chapter 2 |
| She et al. (2026) | ProvenanceGuard | Preprint | VERIFIED (REF-045) | Table 5.3 | Provenance question |
| H.-H. Chen (2026) | Insuring every action | Preprint | VERIFIED (REF-008) | Table 5.3 | Consequence pricing |
| Jia et al. (2026) | FinHarness | Preprint | VERIFIED (REF-025) | Table 5.3 | Financial runtime system |
| C. Zhang et al. (2026) | Calibration is not control | Preprint | VERIFIED (REF-058) | Table 5.3; §5.8 | Limits of calibration for control |

Reference-level "VERIFIED" follows the Stage 1/2 master workbook. For several preprints the check was at abstract level (`CHAPTER3_TECHNICAL_SUMMARY_FOR_SUPERVISOR.md`, References).

## 4. Items the chapter could not complete

- An interpretation of empirical findings: none exists. RESULT NOT AVAILABLE.
- An evidence-based comparison of outcomes with prior work: design level only.
- A final conclusion on O2, O3 and RQ1–RQ4: open.
