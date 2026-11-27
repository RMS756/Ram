# 03: Thesis alignment, title discrepancy and edition merge

## 1. Title and topic discrepancy [SUPERVISOR DECISION REQUIRED]

| Source | Wording |
|---|---|
| Printed title, every edition (`REM_HUMANIZED_THESIS/tools/build_h.py:69`; same in the defence-ready and DiD builds) | **"Runtime Evaluation and Mitigation (REM): A Security Framework for Financial AI Agents"** |
| Research topic stated by the researcher (instructions of 27–28 Nov 2026) | **"Defense in Depth for Financial AI Agents Against Indirect Prompt Injection"** |

**Observations.**
- The humanized and defence-ready texts contain no occurrence of "defense/defence in depth". The DiD edition introduces the term only in exploratory sections.
- The approved objectives O1–O3 (thesis Ch. 1 §1.6) name a "REM framework for financial AI agents' and task automation agents' security". They do not name defense in depth.

**Action.**
- **This reconciliation does not change the title.** The supervisor must confirm which wording is the approved title, against the official proposal or registration record.
- The scientific position in `02_CORRECTED_SCIENTIFIC_POSITION.md` is written so that it is valid under either wording:
  - REM is the evaluated artifact;
  - defense in depth is the property examined.

## 2. Differences between the humanized and DiD editions

**Common base.** Both derive from the defence-ready (ninth) edition. The humanized edition's `orig_src/` is byte-identical to `REM_DEFENCE_READY_THESIS/src/` for every chapter (checked 28 Nov).

| Aspect | Humanized edition (`REM_HUMANIZED_THESIS/`) | DiD edition (`REM_DID_THESIS_EDITION/`) |
|---|---|---|
| Nature of changes | 118 language edits across all chapters; numbers, citations, equations and identifiers preserved (its `reports/03_SCIENTIFIC_INTEGRITY_REPORT.md`) | Five dated insertions, labelled exploratory; no language edits |
| Changed lines vs base | Ch1 27, Ch2 26, Ch3 42, Ch4 138, Ch5 12, Appendices 12 | Ch1 0, Ch2 27 (insert after line 558), Ch3 37 (at line 912), Ch4 75 (at line 2033), Ch5 3 (after lines 88 and 120), Appendices 0 |
| New sections | None | §2.11.6 DiD and authorization prior art (Table 2.6); §3.15 REM-DiD proposed, not adopted (Table 3.16, Figure 3.5), so the summary becomes §3.16; §4.6.12 exploratory DiD evaluation (Tables 4.60, 4.61), so the summary becomes §4.6.13; one "Not confirmed" paragraph in §5.5; Future Work item 14 |
| References | 105 (as base) | 113 (+8: AIS, AgentCap, ScopeGate, Narisetty et al., Agent-Sentry, AgentSandbox, AGATE, RTBAS) |
| Front matter | Humanized | Base, plus an edition note |
| Pages | 272 | 278 |
| **Overlap of edited lines** | **None.** Every DiD insertion point lies on lines that the humanized edits do not touch. Closest: humanized edits at Ch3 lines 910 and 914 around the DiD replacement of line 912; humanized Ch4 edits at lines 2025, 2028 and 2043–2047 around line 2033 | — |

## 3. Recommended base edition and merge

**Recommended base: the humanized edition.** It contains the larger body of verified edits (118, numbers preserved) and was reviewed for integrity. The DiD material consists of a few self-contained insertions, which can be carried over without conflict.

**Merge plan.** No content of either edition is lost, apart from the corrections listed.

| # | Carry from the DiD edition into the humanized base | Action | Reason |
|---|---|---|---|
| M1 | §2.11.6 and Table 2.6 | Insert after the humanized §2.11.5 block (the base's line 558). **Edit:** add a row for Spotlight-Guard (Demirol & Aydoğan, 2026, *Applied Sciences* 16(15) 7662, peer reviewed, level A: layered IPI defense with a component ablation and an adaptive attack) | Its "not found" statement concerns evasion with other controls fixed, which remains accurate at abstract level. The layered, peer-reviewed precedent must be listed |
| M2 | §3.15 REM-DiD (proposed, not adopted), Table 3.16, Figure 3.5; renumber the summary to §3.16 | Insert unchanged | Clearly labelled; documents exploratory work. **It must not be presented as the evaluated artifact** |
| M3 | §4.6.12 Exploratory DiD evaluation (Tables 4.60, 4.61); renumber the summary to §4.6.13 | Insert, with the two edits in `04_PROPOSED_REPLACEMENT_PARAGRAPHS.md` R4-9 | The first block (evasion of REM v1.0's own controls) is **direct evidence for the primary contribution**. One interpretive sentence about REM-DiD "reaching" defense in depth must be qualified, because it rests on oracle or broad authorization |
| M4 | §5.5 "Not confirmed" paragraph; Future Work item 14 | Insert unchanged | Accurate and labelled |
| M5 | 8 references | Add to the humanized reference list. Add Spotlight-Guard if M1's row is accepted | Every inserted citation must resolve |
| M6 | Edition note (front matter) | Rewrite to describe the merged edition | — |
| M7 | DiD number checker (`REM_DID_THESIS_EDITION/tools/check_did_numbers.py`) | Run on the merged sources after the merge | Keeps the DiD numbers verified |

**Corrections in both editions** (from this reconciliation): the replacement paragraphs R1-1 to R1-6 and R4-1 to R4-9 in `04_PROPOSED_REPLACEMENT_PARAGRAPHS.md`.

**Consequential edits in Chapter 5,** to keep the thesis internally consistent. Exact replacements are not drafted here, because the instruction limits drafting to Chapters 1 and 4. Each needs the same correction as Chapter 4:

| Location (humanized source) | Current claim | Required change |
|---|---|---|
| `CHAPTER_05_FINAL.md` line 22 (Table 5.x, RQ4 row) | "every measured outcome effect comes from the Decision Engine's learned decision acting through the Mitigation layer's enforcement" | Use the joint-production wording of R4-7 |
| Line 136 (conclusion paragraph) | "accounts for all 661 attacks …"; "every measured outcome effect comes from that decision acting through enforcement" | Use R4-7 and add the P1 floor sentence of R4-5 |
| Line 51 (contribution 10) | "component-level ablation of the five-layer design" | Acceptable; add "within a layered architecture; protocol-frozen" |
| RQ wording throughout Ch5 | RQ1–RQ4 | Align with the final RQ1–RQ5 if the supervisor adopts them |

**Status of NEXUS in the text.**
- Chapter 2 §2.8.3 and the reference list already record NEXUS as published in *Findings of IJCNLP-AACL 2026*, pp. 2203–2232, DOI 10.18653/2026.findings-aacl.112.
- Chapter 1 §1.4 states only its reading level. R1-2 adds the publication status there.
- The 27 Nov audit's item U3, which said the thesis treats NEXUS only as abstract and repository, is **corrected**: the bibliography and Chapter 2 were already accurate.
