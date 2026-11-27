# Scientific integrity report: humanization and final correction

Each check below compares the revised thesis with the defence-ready original (commit `7b50067`). The checks were run on the final sources and on the built files.

## 1. Preservation of content

All checks are automated and fail closed. They are run by `tools/check_preservation.py`; the result is in `audit/preservation_check.json`.

| Element | Method | Result |
|---|---|---|
| Headings (structure, numbering, order) | Identical sequence of heading lines per file | Identical |
| Tables (86) | Identical sequence of table lines per file | Identical: no cell, label or unit changed |
| Figures (17) and captions | Identical figure lines | Identical |
| Display equations | Identical `$$…$$` blocks | Identical |
| Inline mathematics, code spans, URLs and DOIs | Identical multisets | Identical |
| Numbers in prose | Identical multiset of numeric tokens per file (counts, percentages, intervals, p-values, dates, section and table numbers) | Identical |
| Experimental identifiers | Identical multiset (A4c, A2b, D-8, SD-ABL, RQ1, AS-6, U-labels, x~act~ …) | Identical |
| Citations | Identical count of every cited first-author surname per file | Identical |
| Protected terms | Counts of the five layer names, offline replay, scripted integration, ablation, attack success rate and others | No decrease, except where a sentence was split, and those were re-checked |

## 2. Agreement with the experimental records

- **Number checker.** `tools/check_thesis_numbers.py` compares 498 printed cells (counts, intervals, discordant counts and McNemar p-values in Tables 4.14–4.31) with the recomputation from per-episode records (`audit/number_verification.json`). Result: **0 mismatches**.
- **Citation checkers.** 106 reference entries, 106 cited. Every author–year citation matches an entry.
- **Headline values, unchanged:**
  - REM v1.0: 11 of 2,979 attack goals reached and 105 of 334 benign tasks;
  - Progent's policy (own checker): 0 of 2,979 and 154 of 334;
  - the learned decision accounts for all 661 attacks REM v1.0 prevents (672 without defense);
  - 21 recorded backbones;
  - REM v1.1 on the second population: +7.5 points [1.2, 16.0], 1 against 3 of 2,065.

## 3. REM architecture and evidence status

- **Five layers unchanged:** Input & Context, Detection, Behavioral Analysis, Decision Engine, Mitigation. No sixth layer. Offline fitting stays cross-cutting.
- **The unimplemented injection classifier** is still described as not implemented in REM v1.0 (D-8).
- **CUSUM** remains optional and observe-only. **Linear attribution** remains audit-only.
- **The ablation** is still described as component-level. The isolation limits (Input & Context not removable; classifier absent) are kept in Sections 4.5.1, 4.5.4, 4.5.5, 4.5.11 and threat 21.
- **Offline replay** is never described as live evaluation, and **scripted integration** is never described as deployment or as a security result.
- **Negative findings** are unchanged:
  - the rules match REM;
  - Progent's policy outperforms REM offline;
  - behavioral evidence lowers task completion;
  - the rejected candidate admitted 132 attacks against 11.

## 4. The one scientific correction (Category B)

**Location:** Section 4.4.7, the paragraph on the published policy in the exploratory-extension comparison.

| | Text |
|---|---|
| **Before** | "The upstream checking code was not executed; an independent review of 14 November 2026 reported a differential check …" |
| **After** | "In that study the upstream checking code was not executed. … The authors' checker was executed later, for the comparison at the start of this section, and gave the same counts." |

**Evidence:**
- Table 4.14 and the paragraph "Independent confirmation of the earlier replay" in the same section;
- the records `REM_COMPARATIVE_EVALUATION_PHASE/results/` of 22 November 2026.

No number changed.

## 5. What was not touched

- **Institutional and disclosure text:** the committee page, the declaration placeholder and the factual note on AI assistance. That note was kept as it was, to avoid concealing an existing disclosure.
- **Supervisor-pending wording:** the research-gap statements and RQ1–RQ4.
- **The reference list:** no entry was added, removed or reformatted.
- **AI tools:** no name of an AI writing or editing tool was introduced, and no statement about the humanization process was added to the thesis.

## 6. Files

| File | Content |
|---|---|
| `REM_Master_Thesis_Humanized.docx` / `.pdf` | Revised thesis (272 pages, as before) |
| `original/` | The unchanged original DOCX and PDF |
| `orig_src/` | The original sources |
| `src/`, `text_front/`, `references/` | Revised sources |
| `edits/` | Every edit |
| `reports/EDIT_LIST.md` | Every edit with before and after |
| `audit/` | Check outputs |
