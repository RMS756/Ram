# 10: Final thesis integration guide and change log

## 1. What exists

| Path | Content |
|---|---|
| `thesis_working_copy/REM_Master_Thesis_Consolidated_Working_Copy.docx` and `.pdf` | **Separate revised working copy** (291 pages). Title page: "Consolidated working copy for supervisor review (28 November 2026) — not yet defended or approved; not for submission" |
| `thesis_working_copy/src/`, `text_front/`, `references/` | Markdown sources of the working copy (generated; do not hand-edit, regenerate instead) |
| `thesis_working_copy/docx/` | Per-chapter DOCX files |
| `thesis_working_copy/tools/make_working_copy.py` | Copies the humanized edition, merges the DiD insertions, applies all 85 logged changes by exact anchor (fails if an anchor is not unique) |
| `thesis_working_copy/tools/build_wc.py` | The humanized edition's build: same pinned environment (LibreOffice 24.2.7.2, pandoc 3.9, Liberation Serif), same layout. Only the paths, output name and title-page draft line differ |
| `thesis_working_copy/tools/make_07.py`, `07_gated_section.md` | Generate 07 from the edit log |
| `thesis_working_copy/tools/check_*.py` | Number, citation and DiD checks (copies with paths adapted) |
| `thesis_working_copy/audit/edit_log.json` | Every change: id, file, kind, full old and new text |

**Untouched originals** (`git status` shows no change outside `REM_FINAL_THESIS_CONSOLIDATION/`):
- `REM_HUMANIZED_THESIS/`, `REM_DID_THESIS_EDITION/`, `REM_DEFENCE_READY_THESIS/`;
- the completed review `REM_LAYERED_FRAMEWORK_DESIGN_REVIEW/`;
- the reconciliation;
- `rem/`, `experiments/`, `configs/`, `results/`.

## 2. Reproduce

From the repository root, with `pip install pypandoc_binary python-docx`; the build refuses to run in another rendering environment:

    python3 REM_FINAL_THESIS_CONSOLIDATION/thesis_working_copy/tools/make_working_copy.py
    python3 REM_FINAL_THESIS_CONSOLIDATION/thesis_working_copy/tools/build_wc.py
    python3 REM_FINAL_THESIS_CONSOLIDATION/thesis_working_copy/tools/check_thesis_numbers.py
    python3 REM_FINAL_THESIS_CONSOLIDATION/thesis_working_copy/tools/check_citations.py
    python3 REM_FINAL_THESIS_CONSOLIDATION/thesis_working_copy/tools/check_citations_reverse.py
    python3 REM_FINAL_THESIS_CONSOLIDATION/thesis_working_copy/tools/check_did_numbers.py
    python3 REM_FINAL_THESIS_CONSOLIDATION/thesis_working_copy/tools/make_07.py

## 3. Quality-control results (28 November 2026)

| Check | Result |
|---|---|
| Anchors | 85 changes applied (5 DiD merges, 66 text edits, 14 references); every anchor unique |
| Residual phrases | 0 occurrences of "accounts for all 661", "every measured outcome effect comes from", "pre-registered", "REM-DiD reaches Defense-in-Depth" in the sources |
| Numbers (Ch. 4 tables vs raw-record recomputation) | **498 cells, 0 mismatches** |
| DiD numbers | All verified |
| Citations | 120 entries, all cited; 0 citations with a missing entry. Reverse-check flags are identical to the DiD edition's false positives |
| Build | 77 TOC entries; 192 headings matched (0 unmatched); 18 figures, 91 tables; every caption has a page |
| Visual check | Pages with §2.11.7 and Table 3.17 rendered and inspected |
| Length | 291 pages. Humanized edition 272; DiD edition 278; this task's additions about 13 pages |
| REM v1.0 | `rem/` tree `cd11e32…` unchanged; no experiment run |

**What the build does not establish:**
- The generated DOCX is not a tracked-changes document. Use 07 or `edit_log.json` to review each change.
- Word's own pagination may differ from the LibreOffice-rendered PDF, as for every earlier edition.

## 4. Change log

**Merge of the DiD edition into the humanized base** (reconciliation 03, M1–M5):

| Id | Location | Change |
|---|---|---|
| `M-02-1` | Ch. 2 §2.11.6, Table 2.6 | Inserted unchanged |
| `M1a` | Table 2.6 | Spotlight-Guard row added |
| `M1b` | §2.11.6 | "Not found" statement qualified with BARBICAN |
| `M-03-1` | Ch. 3 §3.15 (REM-DiD, not adopted), Table 3.16, Figure 3.5 | Inserted; summary renumbered §3.16 |
| `M-04-1` | Ch. 4 §4.6.12, Tables 4.60–4.61 | Inserted; summary renumbered §4.6.13 |
| `R4-9a/b` | §4.6.12 | Interpretation qualified |
| `M-05-1`, `M-05-2` | Ch. 5 §5.5 "Not confirmed", Future Work 14 | Inserted |
| `REF+` | References | 8 DiD references |

**Corrections from the reconciliation (`5d7828c`, 04):**

| Id | Location | Change |
|---|---|---|
| `R1-1` | Ch. 1 §1.2 | Problem statement |
| `R1-2a`, `R1-2b` | Ch. 1 §1.4 | NEXUS status; reading levels |
| `R1-3` | Ch. 1 §1.5 | Proposed focus [PD] |
| `R1-5` | Ch. 1 §1.11 | Primary contribution |
| `R1-6a`, `R1-6b` | Ch. 1 §1.11 | Items 3 and 8 |
| `R4-1a`, `R4-1b` | Ch. 4 §4.5.1 | Component-level ablation |
| `R4-2` | §4.5.3 | Data history |
| `R4-3` | §4.5.7 | Joint production |
| `R4-4` | §4.5.10 | Removal vs suppression |
| `R4-5` | §4.6.3 | P1 withhold-all identity |
| `R4-6a–d` | §4.5.12 | Joint production |
| `R4-7a/b` | Table "What the evidence supports", row 14 | Claim and limits |
| `R4-8` | §4.6.13 | Summary bullet |

**Research gap (04):**

| Id | Location |
|---|---|
| `C-GAP1`, `C-GAP1b` | Ch. 1 §1.4 |
| `A7` | Ch. 2 new §2.11.7 |
| `C-GAP2` | §2.11.5 |
| `C-GAP3` | Ch. 2 summary |

**A1–A7 documentation (02):**

| Id | Location |
|---|---|
| `A1` | Ch. 3 §3.4.2 |
| `A2` | Ch. 3 §3.2.2 |
| `A2-ch1` | Ch. 1 "does not claim" |
| `A3` | Ch. 3 §3.8 |
| `A3-ch4` | Ch. 4 §4.5.7 |
| `A4` | Ch. 3 §3.6.2 |
| `A5` | Ch. 3 Table 3.17 |
| `A6` | Ch. 4 §4.3.3 |
| `A7` | Ch. 2 §2.11.7 |

**Consistency and terminology:**

| Id | Location | Change |
|---|---|---|
| `C-NEG1` | Ch. 1 item 5 | Negative result qualified |
| `C5-1` … `C5-10` | Ch. 5 | RQ answer table, contributions table, conclusion |
| `C5-11` | Ch. 5 limitation 9 | Literature limits |
| `FW` | Ch. 5 Future Work 15–17 | B2, B5, B7 |
| `T1`–`T10` | Chs. 3, 4, Appendix B | "Pre-registered" replaced |
| `AB-1` … `AB-6` | English and Arabic abstracts | Same corrections as the chapters |
| `REF+` | References | 6 new references (09 §2) |

## 5. Not applied (supervisor first)

- **Title** (08 D1).
- **RQ1–RQ5** (D2; text in 07 §2.1).
- **Kull "prove"** (D7; 07 §2.3).
- **Holm citation** (D9; 07 §2.4).
- **Any change to the α grid, the tie rule or the calibration target** (D7–D9).

These need no code change in REM v1.0. Any code alignment, for example of the tie rule, would be a new, approved version.

## 6. How to integrate after the supervisor decides

1. **For each rejected edit:** delete its `replace(...)` or `insert_*` call in `make_working_copy.py` by its id, then rerun the reproduce steps (§2). Anchors are exact, so the remaining edits are unaffected.
2. **If D2 (RQs) is approved:** apply 07 §2.1 and the renumbering in 06 §4 as new edits in the same script, then rebuild.
3. **If D1 changes the title:** change `TITLE` in `build_wc.py` and the committee page in `text_front/front_matter.md` (through the script), then rebuild.
4. **After full-text access (D11):** update 01 and 09, and re-check every A-level sentence of §2.11.7 and §2.11.6 against the full texts before submission.
