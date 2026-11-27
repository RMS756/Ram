# Humanization coverage report (Stage 1)

**Thesis:** *Runtime Evaluation and Mitigation (REM): A Security Framework for Financial AI Agents*

| Item | Location |
|---|---|
| Original (unchanged) | `REM_DEFENCE_READY_THESIS/REM_Master_Thesis_Defence_Ready.{docx,pdf}`, commit `7b50067`. A copy is in `REM_HUMANIZED_THESIS/original/`. |
| Revised | `REM_HUMANIZED_THESIS/REM_Master_Thesis_Humanized.{docx,pdf}` |

## Method

The original sources were snapshotted in `orig_src/` and are never modified. Every revision is an exact, logged replacement in `edits/*.txt`.

- **Applying edits:** `tools/apply_edits.py` applies them to the snapshot.
- **Fail-closed preservation check:** `tools/check_preservation.py` compares each revised file with its original and fails on any change to:
  - heading lines, table lines, figure lines or display equations;
  - inline mathematics, code spans or URLs;
  - the multiset of numbers in the prose;
  - experimental identifiers (A4c, D-8, RQ1, SD-ABL, x~act~ …);
  - the number of occurrences of any cited surname.

The check passes on the final text.

**Editing principles applied:**
- **Untouched by design:**
  - paragraphs that were already clear;
  - text whose wording is a pending supervisor decision (research-gap statements, RQ1–RQ4);
  - institutional or disclosure text: the committee page, declaration and AI-use note.
- **Main targets:** over-long, clause-stacked sentences, semicolon chains and dense enumerations, which were recast as shorter sentences or lists.
- **Other targets:** em-dashes in prose, ambiguous self-references, and two captions that said "this chapter" inside an appendix.

## Coverage, chapter by chapter

| Part | Read in full | Edits | Edit file | Not edited, and why |
|---|---|---|---|---|
| Front matter: committee page, declaration, AI-use note, dedication, acknowledgement | Yes | 0 | — | Institutional and disclosure text |
| Front matter: Status of This Draft | Yes | 5 | `00_front_abstract.txt` | — |
| English abstract | Yes | 9 | `00_front_abstract.txt` | Length is a Category C issue (U-H1) |
| Arabic abstract | Yes | 4 | `03_abstract_ar.txt` | Native-speaker review still required |
| Chapter 1 (1.1–1.11) | Yes | 9 | `01_ch1.txt` | Gap statement (1.4) and RQ1–RQ4 (1.7): pending decision D-10 |
| Chapter 2 (2.1–2.12) | Yes | 11 | `02_ch2.txt` | Gap statements 2.11.1 and 2.11.5; tables |
| Chapter 3 (3.1–3.15) | Yes | 14 | `04_ch3.txt` | Equations, symbol definitions, tables, Procedure 3.1, Algorithm 1 |
| Chapter 4, introduction and 4.1–4.3 | Yes | 10 | `07_ch4a.txt` | Tables |
| Chapter 4, 4.4 (framework comparison) | Yes | 10 | `08_ch4b.txt` | Tables; includes the single Category B correction |
| Chapter 4, 4.5.1–4.5.8 (first part) | Yes | 8 | `09_ch4c.txt` | Tables |
| Chapter 4, 4.5.8 (repair study) – 4.5.12 | Yes | 8 | `10_ch4d.txt` | Tables |
| Chapter 4, 4.6.1–4.6.12 | Yes | 12 | `11_ch4e.txt` | Tables; headings with em-dashes (headings are locked) |
| Chapter 4, second pass | Yes | 2 | `12_ch4f.txt` | — |
| Chapter 5 (5.1–5.8) | Yes | 10 | `05_ch5.txt` | Tables 5.1–5.3 |
| Appendices A and B | Yes | 6 | `06_appendices.txt`, `13_appendix_legend.txt` | Tables and equations |
| References | Yes | 0 | — | Bibliographic entries are not language-edited |
| **Total** | | **118** (117 A, 1 B) | | |

**Table cells.** The prose of every chapter was read in full. Table cells (86 tables) were not edited: the preservation check locks them. They were checked as follows:
- the 498 numeric cells of Tables 4.14–4.31 by the number checker (0 mismatches);
- in all other tables, by the identity of every table line with the original.

Table captions in the prose are covered by Stage 1.

## Measured effect

| Measure | Original | Revised |
|---|---:|---:|
| Prose sentences over 40 words, counted per paragraph line (chapters, appendices, English abstract, front matter) | 127 | 68 |
| Em-dashes in prose (headings excluded) | 10 | 3 |
| Words of prose (tables excluded; all files incl. references) | 61,702 | 61,819 |
| Pages | 272 | 272 |

**Remaining em-dashes:**
- two in the Arabic abstract, where the dash separates the names on the title line;
- one inside a published paper title in the references, which is kept verbatim.

**Remaining long sentences:** mostly bold-lead list items, figure and table captions, or "where …" clauses that define symbols. These are left intact deliberately.

**Stock AI vocabulary:** the original contained almost none (no instances of delve, tapestry, pivotal, showcase or seamless, for example). This is consistent with its eight earlier editions.

## Scope statement

Stage 1 was a complete reading of the prose of the whole thesis, not a sample. It was not a rewrite. Most paragraphs were already clear and were retained, as the brief requires. The revision is concentrated on sentence structure, where the measurable defects were.
