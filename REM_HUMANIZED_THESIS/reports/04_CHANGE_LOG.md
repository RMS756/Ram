# Change log: humanization and final correction (27 November 2026)

**Base:** `REM_DEFENCE_READY_THESIS` at commit `7b50067`, 272 pages, which is unchanged.

**Result:** `REM_HUMANIZED_THESIS/REM_Master_Thesis_Humanized.{docx,pdf}`, 272 pages.

The complete list of the 118 edits, each with its before and after text, is in `EDIT_LIST.md`.

## Significant changes, by kind

| Kind | Count | Examples | Reason |
|---|---:|---|---|
| Over-long sentences split | most of the 118 | Abstract: the 60-word ablation sentence became three sentences. Chapter 2: the FinVault withdrawal sentence became three. Chapter 5: the shadow-mode sentence was split. | One idea per sentence. Prose sentences over 40 words fell from 127 to 68 (per paragraph line). |
| Semicolon chains and dense enumerations turned into lists | 13 | Section 1.11, "What the thesis does not claim" (eight items); Section 3.2.2, the layer execution order; Section 3.13, the REM v1.1 definition; Section 4.5.8, the three repaired arms; Section 4.6.10, the four kinds of trusted input | Scannability without change of content |
| Em-dashes removed from prose | 7 | The assumption A-Mod (Section 3.7.5); the verification-code legend (Appendix A.4) | House style; parenthetical dashes recast with colons or sentences |
| Wording precision | several | "a five-layer runtime layer" became "a runtime security framework of five layers" (abstract, Section 1.11). "confirmed, with paired intervals" became "showed with paired intervals" (abstract). "Two ablations of Table 4.35 were followed up" now names the two and the verdict-set change that the three bullets report. | Accuracy and verb strength |
| Ambiguous references | 4 | Two captions in Appendix A said "this chapter" and now say "the methodology chapter". Two self-references to "Section 4.5.8" inside Section 4.5.8 now point to the repair study within it. | Clarity |
| Arabic abstract | 4 | "طبقة تشغيلية من خمس طبقات" became "إطار أمني تشغيلي من خمس طبقات"; "وكلاء أحياء" became "تشغيل حيّ للوكلاء"; two sentences split | Accuracy; a native-speaker review is still required |
| Evidence-based correction (B) | 1 | Section 4.4.7: the scope of "the upstream checking code was not executed" | See `03_SCIENTIFIC_INTEGRITY_REPORT.md`, Section 4 |

## Not changed

- **Research identity:** title, topic, scope, objectives, research questions, research-gap statements and the five-layer architecture.
- **Content:** every number, table, figure, equation, citation and reference entry.
- **Institutional and disclosure text:** the committee page, the declaration and the AI-use note.
- **The original thesis and its reports** in `REM_DEFENCE_READY_THESIS/`.
