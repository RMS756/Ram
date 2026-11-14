# Change log: second edition (14 November 2026, commit `7940c8c`) → third edition (14 November 2026)

**Status:** draft for supervisor review; not approved; not submitted. **The first and second editions are preserved unchanged** in `REM_FINAL_SUBMISSION/thesis/` and `REM_FINAL_SUBMISSION/thesis_r2/`.

## Files

| Output | Path |
|---|---|
| Chapters (Markdown and Word) | `src/CHAPTER_0N_FINAL.md`, `docx/CHAPTER_0N_FINAL.docx`, appendices and references likewise |
| Combined thesis | `REM_THESIS_FINAL_R3.docx`, `REM_THESIS_FINAL_R3.pdf` (314 pages: preliminary i–xxvii; main text printed pages 1–183; Chapter 4 on 105–171; references from 184; appendices A–F from 199) |
| Audit | `audit/CHAPTER4_REQUIREMENT_MATRIX.md`, `audit/CLAIM_AUDIT_R3.md`, `audit/page_reference_check.json`, `audit/render_environment.json`, `audit/toc_entries.json`, `audit/final_crossref_check.txt` |

Rebuild from the repository root (the build stops if the rendering environment differs from the pinned one):

```bash
python3 REM_FINAL_SUBMISSION/thesis_r3/tools/gen_ch4_r2.py
python3 REM_FINAL_SUBMISSION/thesis_r3/tools/make_final.py
python3 REM_FINAL_SUBMISSION/thesis_r3/tools/build_final.py
python3 REM_FINAL_SUBMISSION/thesis_r3/tools/check_layout.py REM_FINAL_SUBMISSION/thesis_r3/REM_THESIS_FINAL_R3.pdf
python3 REM_FINAL_SUBMISSION/thesis_r3/tools/check_pages.py REM_FINAL_SUBMISSION/thesis_r3
```

## Rendering environment (pinned)

LibreOffice 24.2.7.2; pandoc 3.9 (the copy bundled with pypandoc); Times New Roman is not installed and is substituted by the metric-compatible Liberation Serif (`LiberationSerif-Regular.ttf`, SHA-256 recorded). Page counts differ in other environments (an external review obtained 299 pages for the second edition with a newer LibreOffice); the stored DOCX and PDF of this edition were produced together in the pinned environment, and **all 364 page references (table of contents, list of tables, list of figures) were checked against the PDF: 0 mismatches.**

## Content changes

| Where | Change | Reason |
|---|---|---|
| Ch. 4, §4.4.3 | Repaired rule G2 added to the tables and contrasts; rows already given in Tables 4.11 and 4.34 removed (A2 kept for reference); Progent arm described as "the published manual banking policy, adapted to the shared replay harness", with the external 468-case differential check reported as such | Review of 14 November: precise naming; reduce repetition |
| Ch. 4, §4.5.4 (new) | Ablations of the repaired rule and of the authority guard (Tables 4.21, 4.22) | Follow-up study |
| Ch. 4, §4.6.10 (new) | Defects of the permission rule; call-level audit of user task 15; sensitivity analysis without that task | Follow-up study |
| Ch. 4, §4.6.11 | Percentage table that repeated earlier counts removed; conclusions 10 and 11 updated; "not supported" list extended | Reduce repetition; follow-up |
| Ch. 4, §4.6.12–4.6.13 | Threat 17 (repairs after results); summary updated | Follow-up |
| Ch. 4, probe table | Rows given in Table 4.32 removed | Reduce repetition |
| Ch. 3, §3.7.4 | "an unavailable indicator … can only lower the estimated probability" replaced: the direction depends on the fitted coefficient; x^act^~1~, the only indicator that can be unavailable, has positive coefficients in every fold (1.33 to 2.36) | Review: the claim is not true in general (negative coefficients occur) |
| Ch. 3, §3.14 | Revision 2 of the extension (instructions, conditions, fulfilment, authority guard, typed provenance) | Follow-up |
| Ch. 2, §2.9.3 | The README's decision policy is labelled as repository documentation and not attributed to the published NEXUS; the different thresholds in other repository documents are stated | Review: do not mix the published policy with the README |
| Ch. 1, Ch. 5 | Contribution, rejected-variant and conclusion text updated for the follow-up | Follow-up |
| Abstracts (English, Arabic) | One sentence on the follow-up; final sentence limited to the methods tested | Review |
| Appendix F | SD-PERM extended; new SD-COND (whether a subjective condition may ever license an action) | Follow-up |
| Front matter | Status page and title page: third edition | — |

## Length

Main text 183 printed pages (second edition: 175); Chapter 4: 67 pages (61). The follow-up adds about eight pages; the removal of repeated tables saves about two. No material was moved to an appendix without a decision.

## Not changed

`rem/`, `configs/`, all earlier result files (including those of the development study of 13 November), the frozen v1 matcher, the first and second thesis editions. Placeholders and supervisor decisions remain pending.
