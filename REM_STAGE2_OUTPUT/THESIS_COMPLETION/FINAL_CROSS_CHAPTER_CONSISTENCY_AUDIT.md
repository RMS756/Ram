# FINAL CROSS-CHAPTER CONSISTENCY AUDIT — Chapters 1–5

**Date:** 24 September 2026 · **Repository state:** HEAD `c22a97d` plus the files in this folder
**Chapters audited:**
- Chapter 1: `CHAPTER1_INTRODUCTION.md`
- Chapter 2: `REM_STAGE2_INPUT_PACKAGE/working/Chapter2_working.md` (unchanged)
- Chapter 3: `REM_STAGE2_INPUT_PACKAGE/working/Chapter3_working.md` (unchanged)
- Chapter 4: `CHAPTER4_IMPLEMENTATION_EXPERIMENTAL_DESIGN_RESULTS.md`
- Chapter 5: `CHAPTER5_DISCUSSION_CONCLUSIONS.md`

---

## 1. Integrity of protected artifacts

| Artifact | SHA-256 prefix now | Reference value | Result |
|---|---|---|---|
| Chapter 2 working file | `1e59d4a74d9205a2` | `PACKAGE_SHA256SUMS.txt`: `1e59d4a74d9205a2` | Unchanged |
| Chapter 3 working file | `5085e11732dee82f` | `PACKAGE_SHA256SUMS.txt`: `5085e11732dee82f` | Unchanged |
| `CLAUDE.md` | `6fef971e0d752eb9` | Contract digest in `evidence/E3_…/manifest.json`: `6fef971e0d752eb9…` | Unchanged |
| Code, configuration, tests, decision records | — | `git status`: only `REM_STAGE2_OUTPUT/THESIS_COMPLETION/` is new | Unchanged |

**Chapter 2 was not modified. Chapter 3 was not modified. `CLAUDE.md`, the implementation and the existing decision records were not modified.**

## 2. Cross-chapter checks

| Dimension | Ch1 | Ch2 | Ch3 | Ch4 | Ch5 | Consistent? |
|---|---|---|---|---|---|---|
| Research problem | Runtime compromise of tool-using financial agents through indirect prompt injection (§1.2) | §§2.2–2.3, 2.6 | Table 3.1 | §4.1.3 | §5.9 | Yes |
| Objectives | O1–O3 verbatim | — | §3.1.2 (source) | Table 4.13 via RQs | Table 5.1 | Yes |
| Research questions | RQ1–RQ4, [PD] | — | §3.1.3, "for supervisor confirmation" | Table 4.13, [PD] | Table 5.1, [PD] | Yes |
| Research aim | Derived from O1–O3, flagged | — | Not stated | — | §5.9 restates the design-and-evaluate purpose | Yes (flagged) |
| Methodology | Design science; grouped cross-fitting | — | §3.1.1, §3.11 | §4.8–4.11 as PLANNED | §5.6 | Yes |
| Architecture | Five layers; cross-cutting fitting; audit-only attribution | §2.15 | §3.2.1 | §4.2.3; SC-6 on layer labels | §5.1.1 (4) | Yes. Five layers everywhere; no sixth layer; the SC-6 mapping difference is disclosed |
| Algorithms | Ridge LR, logit calibration, expected-loss verdict, linear attribution | §§2.9–2.11 | §3.7 | §4.6 | §5.1 | Yes. No algorithm is added in Ch1, Ch4 or Ch5 |
| Beta, isotonic, temperature calibration | Not mentioned | §2.9 | Not adopted (§3.7.2) | Absent from code (§4.6.2) | Not mentioned | Yes |
| CUSUM | Not mentioned | §2.5 | Optional, observe-only (§3.11.10) | Not implemented; approval pending | Not claimed | Yes |
| Equations | None displayed | — | 3.1–3.22 | 3.1, 3.3, 3.6, 3.7, 3.11 reproduced; none new | None displayed | Yes |
| Equation source status | §1.8 cites the Ch3 sources | — | Table 3.17 | 3.1, 3.2, 3.3, 3.15, 3.16 SOURCE NOT FULLY VERIFIED | 3.9, 3.10 SOURCE NOT FULLY VERIFIED | Yes. All seven are covered across Ch4–Ch5, and none is presented as verified |
| Experiments | Not executed (§1.12) | — | Specified (§3.11) | PLANNED — NOT EXECUTED | Not executed (§5.5) | Yes |
| Results | None claimed | — | — | RESULT NOT AVAILABLE; verification evidence E1–E6 only | None interpreted as security evidence | Yes |
| Conclusions | — | — | — | — | Limited to demonstrated software properties | Yes |
| Limitations | §1.10 scope; §1.12 status | §2.14 bound | §3.14 | §4.16 | §5.5 | Yes |
| Novelty | Empirical and integrative; "not claimed" list | §2.14 | §3.13 | No claim | §5.3: composition only, not evaluated | Yes. No "novel algorithm", "first", "state-of-the-art", "best", "superior" or "guaranteed" claim (automated scan: only "any prevention guarantee" in the not-claimed list) |
| NEXUS distinction | Expected-loss objective defined; deployed rule cascade | §2.4.4, §2.10 (source) | Table 3.16 | — | Table 5.3 with OI-01 to OI-05 | Yes. No chapter states that NEXUS lacks expected loss |
| Mitigation semantics (SC-1) | Named in §1.12 | — | Episode-level (Table 3.14) | Side by side, Table 4.8 | §5.5 | Yes. Unresolved everywhere |
| Tie-breaking (SC-2) | Named in §1.12 | — | Block ⪰ Escalate ⪰ Modify ⪰ Allow | `VerdictTieError`; §4.6.4 | §5.1.3, §5.5 | Yes. Unresolved everywhere |
| SC-3 to SC-6 | Named in §1.12 | — | — | §§4.2.3, 4.2.4, 4.6.2, Table 4.12 | §5.5 | Yes |
| Chapter structure | Five chapters; SD-STRUCT disclosed | — | Refers to Chapters 4, 5, 6 | — | — | **Inconsistent by construction. SUPERVISOR DECISION REQUIRED (SD-STRUCT)**; disclosed in Ch1 §1.13 |
| References | 26 entries, verbatim from Ch2/Ch3 | 47 | 37 | 10 verbatim; 4 code-only sources flagged | 7 verbatim | Yes. Checked automatically; no new reference; Platt OI-07 preserved |
| Terminology | Checked | — | Source | Checked | Checked | Yes (verdict names, layer names, p̃_t/p_t, SO/AS/TB identifiers) |

## 3. No-hallucination audit (Chapters 1, 4, 5)

| Category | Finding |
|---|---|
| Numerical claims | Chapter 4: only E1–E6 values and Chapter 3 task counts, with the Ch3 caveat. Chapter 5: counts carried from Ch3/Ch4. Chapter 1: structural counts and 154 tests. No benchmark rate from the literature is quoted in Ch1, Ch4 or Ch5. |
| Performance claims | None. |
| Security claims | Only software-level properties, labeled as such. Protection is stated as intended and not demonstrated (Table 5.4). |
| Citations | Every citation resolves to a Ch2/Ch3 reference entry, except four code-docstring sources, which are named and flagged SOURCE VERIFICATION REQUIRED in Ch4. |
| Algorithms | None added. |
| Datasets | None claimed as used. |
| Experiments | None claimed as executed. |
| Latency / real-time | No measurement claimed; "real time" is explicitly not claimed (Ch4 §4.15). |

## 4. Markdown–DOCX parity

The DOCX files are generated from the Markdown files by pandoc with a reference template. They use native Word equations and tables. Plain-text token counts and word sets match:
- Chapter 1: identical;
- Chapter 5: identical apart from four table-layout tokens;
- Chapter 4: identical apart from the TeX command names `\dots` and `\qquad` inside one equation's plain-text fallback.

Rendering checks through LibreOffice found no broken equations:

| Chapter | Pages | Tables | Display equations |
|---|---|---|---|
| Chapter 1 | 8 | 0 | 0 |
| Chapter 4 | 22 | 17 | 5 |
| Chapter 5 | 10 | 4 | 0 |

## 5. Residual issues (not resolved by this work)

1. SC-1 to SC-6, SD-FREEZE, SD-STRUCT, RQ-CONFIRM, SD-5, TITLE and the design values in `SUPERVISOR_DECISIONS_REQUIRED.md` §C.
2. All empirical evidence for O2, O3 and RQ1–RQ4.
3. OI-01 to OI-07, OI-09 to OI-14, CF-01 to CF-09, and the source verification of Equations 3.1, 3.2, 3.3, 3.9, 3.10, 3.15 and 3.16.
4. Four code-cited sources with no verification record.
5. Missing records: approved proposal, decision ledger, equation registry.

**The thesis is not complete.** Chapters 1, 4 and 5 now exist and document the current state accurately. The results that Chapter 4 is designed to report, and the conclusions that Chapter 5 would draw from them, depend on the decisions and experiments listed above.
