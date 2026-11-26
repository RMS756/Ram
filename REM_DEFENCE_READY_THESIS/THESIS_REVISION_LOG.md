# Thesis revision log: defence-ready edition (R9, 26 November 2026)

## Source and output

| Item | Value |
|---|---|
| Source (not modified) | `REM_FINAL_SUBMISSION/thesis_r8/REM_THESIS_EDITORIAL_R8.docx` / `.pdf` (eighth edition, 19 November 2026, 230 pages). Its sources `thesis_r8/src/`, `text_front/`, `references/` are only read. |
| Output | `REM_DEFENCE_READY_THESIS/REM_Master_Thesis_Defence_Ready.docx` and `.pdf` (270 pages: 24 preliminary pages and 246 numbered pages; A4) |
| Chapter files | `REM_DEFENCE_READY_THESIS/docx/*.docx` |
| Assembly | `tools/make_r9.py` + `tools/spec_r9.py` (every edit is an exact, logged replacement); new text in `text/ch4_44.md` and `text/ch4_45.md` |
| Build | `tools/build_r9.py`: the R8 builder with new paths, output name, title-page edition line, abbreviations, and one column-width fix. Same pinned environment: LibreOffice 24.2.7.2, pandoc 3.9, Liberation Serif (sha256 `705903ae…`) substituted for Times New Roman. |
| Figures | `tools/make_figures.py` → `figures/` (generated only from `audit/number_verification.json` and the code structure) |
| Number verification | `tools/verify_numbers.py` (recomputes from the raw per-episode records) → `audit/number_verification.json`, `audit/call_level_verification.json`; `tools/check_thesis_numbers.py` → `audit/thesis_number_check.json` (191 printed cells, 0 mismatches) |
| QC record | `audit/qc_checks.txt` |

Reproduce from the repository root:

```bash
python3 REM_DEFENCE_READY_THESIS/tools/verify_numbers.py
python3 REM_DEFENCE_READY_THESIS/tools/make_figures.py
python3 REM_DEFENCE_READY_THESIS/tools/make_r9.py
python3 REM_DEFENCE_READY_THESIS/tools/build_r9.py
python3 REM_DEFENCE_READY_THESIS/tools/check_thesis_numbers.py
```

## What changed, by chapter

### Chapter 4: two sections rewritten, others amended

**Section 4.4, "Comparison with Existing Security Frameworks"** (new, replaces R8's 4.4). Subsections:
- 4.4.1 Introduction and scope;
- 4.4.2 Selection criteria (Table 4.10);
- 4.4.3 The compared frameworks (Progent, DRIFT, MELON, the defenses distributed with AgentDojo, other frameworks; R8's 4.4.4 is kept inside it);
- 4.4.4 Architecture comparison on 15 dimensions (Table 4.12; Figure 4.1);
- 4.4.5 Mechanism comparison;
- 4.4.6 Experimental design and kinds of evidence (Table 4.13);
- 4.4.7 Quantitative results: Progent's policy decided by Progent's own checker on three populations (Tables 4.14–4.15, Figure 4.2), and R8's 4.4.1–4.4.3 kept as sub-units; DRIFT scripted integration (Table 4.23); MELON status;
- 4.4.8 Fairness;
- 4.4.9 Discussion;
- 4.4.10 Limitations;
- 4.4.11 Conclusion.

**Section 4.5, "Ablation Study of the REM Layers"** (new, replaces R8's 4.5). Subsections:
- 4.5.1 Introduction;
- 4.5.2 Motivation;
- 4.5.3 Experimental design;
- 4.5.4 Layer-to-implementation mapping (Table 4.24, Figure 4.4);
- 4.5.5 Ablation configurations, with variants A1–A5 and their status (Table 4.25);
- 4.5.6 Metrics;
- 4.5.7 Results:
  - Tables 4.26–4.29 and Figure 4.5;
  - R8's 4.5.5, with its 19-November arm labels relabelled to the variant names;
  - R8's 4.5.1–4.5.2;
- 4.5.8 Ablations of exploratory extensions, which are not part of REM v1.0 (R8's 4.5.3, 4.5.4 and 4.5.6);
- 4.5.9 Statistical analysis;
- 4.5.10 Discussion;
- 4.5.11 Limitations;
- 4.5.12 Conclusion.

**Elsewhere in Chapter 4:**

| Place | Change |
|---|---|
| Introduction | New description of Sections 4.4 and 4.5 |
| 4.1.4 | Ten kinds of evidence instead of eight: added "replay with a published framework's own code" and "scripted integration"; source folders of the 21- and 22-November studies |
| 4.3.1 | Arms added: Progent policy decided by the official checker; ablation variants A1–A5. DRIFT added to the defenses that were not run with a model |
| 4.3.4 | Nine sets of comparisons fixed in advance instead of six, with three dated bullets for 19, 21 and 22 November |
| 4.6.10 | Conclusions 14 (layers) and 15 (Progent, official checker) added to Table 4.59; "does not support" now includes "that a component without a measurable effect is unnecessary" |
| 4.6.11 | Threat 16 rewritten; threats 21 (granularity of the layer ablation) and 22 (comparison with existing frameworks) added |
| 4.6.12 | Summary bullets for the layer ablation, DRIFT and MELON, and the official checker |

**Corrections of R8:**
- The reference "Sections 4.6.2 and 4.5.1–4.6.5" (a range across sections) now reads "Sections 4.6.2, 4.6.4, 4.6.5 and 4.5.7".
- "(Sections 4.2.1 and 4.2.1)" now reads "(Section 4.2.1)".

### Chapter 5

- **Table 5.1, RQ4:** layer-level answer added, with evidence from the ablations of the five layers.
- **Table 5.2, O3:** official-checker comparison, 15-dimension comparison and DRIFT integration added. The "Not achieved" column states that DRIFT and MELON were not run with a model.
- **Table 5.3:**
  - rows ordered 1–10; R8 printed 1–7, 9, 8;
  - contribution 10 added (layer-wise ablation and framework comparison);
  - printed with three columns instead of six (cell text unchanged, columns joined).
- **5.6:** item 10 rewritten; item 12 added.
- **5.7:** item 4 adds DRIFT.
- **5.8:** "A final ablation, pre-registered on the last day of the work" became "Two pre-registered ablations"; sentences on the layers and on Progent's official checker added.

### Chapter 1

- 1.11 item 8 retitled and extended.
- "Does not demonstrate" list: DRIFT and MELON not run with a model; "that a component without a measurable effect is unnecessary".
- 1.12: description of Chapter 4.

### Chapter 2

- Line 427: DRIFT is now cited (H. Li et al., 2025); R8 named it without a citation.

### Front matter

| Item | Change |
|---|---|
| Title page | Edition line: "Defence-ready edition prepared for discussion (26 November 2026) — not formally approved". R8's title page still carried the seventh-edition line; corrected. |
| Status page | Rewritten for this edition. R8 section numbers in the history are given with their new numbers. No approval is claimed. |
| Abstract (English) | Sentences on the layer ablation and on Progent's official checker; DRIFT added to the integrations not run with a model |
| Abstract (Arabic) | The same content added; remains a draft translation |
| List of Abbreviations | CI, CPU, IBAN, JSON, MIT, pp added; sorted |

### References

- Added: H. Li et al. (2025), DRIFT, NeurIPS 2025, DOI 10.52202/085713-2791.
- Added: H. Li et al. (2026), AgentDyn, arXiv:2602.03117.
- The list grows from 103 to 105 entries; every entry is cited, and every citation has an entry (`audit/qc_checks.txt`).

### Not changed

- Chapter 3, the appendices and the equations (the equation set is checked unchanged by `make_r9.py`).
- No result of R8 was changed.
- REM's design and code (`rem/` at `9fddfa7`), every frozen protocol and every earlier result folder are untouched.

## Layer assignment of the ablation variants

Chapter 3 (Table 3.6) places the action features x_act1–x_act3 in the **Behavioral Analysis** layer and states that the Input & Context layer computes no evidence (Section 3.4).

The ablation therefore follows Chapter 3:
- action/provenance evidence is variant **A3b**, not a Layer-1 variant;
- the Input & Context layer is reported as **not independently isolatable** (A1), and observed indirectly through A3b;
- hygiene (A1h) is reported as not exercised: it changes 0 of 16,727 tool outputs.

An earlier draft of the new section assigned the action features to Input & Context. That draft was corrected before the build, so that the architecture of Chapter 3 is not silently changed.

## Numbering correspondence, R8 → R9

Section numbers:

| R8 section | R9 location |
|---|---|
| 4.4.1, 4.4.2, 4.4.3 | 4.4.7 |
| 4.4.4 | 4.4.3 |
| 4.5.1, 4.5.2, 4.5.5 | 4.5.7 |
| 4.5.3, 4.5.4, 4.5.6 | 4.5.8 |

All 99 section references in the R8 text were remapped (`audit/r9_renumbering.json`). References to the supplement ("S-…") are unchanged.

Arm labels of the 19-November study, as relabelled in the R9 text:

| 19-Nov arm | Variant |
|---|---|
| A0 | Full REM v1.0 |
| A1 | A3a |
| A2 | A4c |
| A3 | A4d |
| A4a | A2a |
| A4b | A3b |
| A5 | A4e |
| A6 | A4a |
| A7 | A4b |

Arms of the 21-November study:

| 21-Nov arm | Variant |
|---|---|
| A1a | A2a |
| A1b | A2b |
| A2 | A3a |
| AIC | A3b |
| A3 | A4a |
| A3P | A4b |
| A4 | A5 |

Tables and figures of Chapter 4 are now numbered sequentially. R8 kept old table numbers and gave new tables lettered numbers. Unchanged numbers are omitted below. Tables 4.1–4.9 are unchanged.

| R8 number | R9 number |
|---|---|
| Table 4.14 | Table 4.11 |
| Table 4.10 | Table 4.16 |
| Table 4.11 | Table 4.17 |
| Table 4.11a | Table 4.18 |
| Table 4.11b | Table 4.19 |
| Table 4.11c | Table 4.20 |
| Table 4.12 | Table 4.21 |
| Table 4.13 | Table 4.22 |
| Table 4.21a | Table 4.30 |
| Table 4.21b | Table 4.31 |
| Table 4.21c | Table 4.32 |
| Table 4.21d | Table 4.33 |
| Table 4.21e | Table 4.34 |
| Table 4.15 | Table 4.35 |
| Table 4.16 | Table 4.36 |
| Table 4.17 | Table 4.37 |
| Table 4.18 | Table 4.38 |
| Table 4.19 | Table 4.39 |
| Table 4.20 | Table 4.40 |
| Table 4.21 | Table 4.41 |
| Table 4.22 | Table 4.42 |
| Table 4.23 | Table 4.43 |
| Table 4.24 | Table 4.44 |
| Table 4.25 | Table 4.45 |
| Table 4.26 | Table 4.46 |
| Table 4.27 | Table 4.47 |
| Table 4.28 | Table 4.48 |
| Table 4.29 | Table 4.49 |
| Table 4.30 | Table 4.50 |
| Table 4.31 | Table 4.51 |
| Table 4.32 | Table 4.52 |
| Table 4.33 | Table 4.53 |
| Table 4.34 | Table 4.54 |
| Table 4.35 | Table 4.55 |
| Table 4.36 | Table 4.56 |
| Table 4.37 | Table 4.57 |
| Table 4.38 | Table 4.58 |
| Table 4.39 | Table 4.59 |
| Figure 4.1 | Figure 4.3 |
| Figure 4.2 | Figure 4.6 |
| Figure 4.3 | Figure 4.7 |
| Figure 4.4 | Figure 4.8 |
| Figure 4.5 | Figure 4.9 |
| Figure 4.6 | Figure 4.10 |
| Figure 4.7 | Figure 4.11 |

| New in R9 | Number |
|---|---|
| Candidate frameworks and the selection decision | Table 4.10 |
| Architecture comparison (15 dimensions) | Table 4.12 |
| What was measured for each framework, and how | Table 4.13 |
| REM v1.0 and Progent's published banking policy on identical episodes | Table 4.14 |
| Paired differences, REM v1.0 minus Progent's policy | Table 4.15 |
| Scripted integration of the official DRIFT code | Table 4.23 |
| The five layers as implemented | Table 4.24 |
| Ablation variants, their exact change and their status | Table 4.25 |
| Episode-level outcomes of every ablation variant (primary population) | Table 4.26 |
| Paired differences from the full framework | Table 4.27 |
| Ablation variants on the held-out templates and the second population | Table 4.28 |
| Attack-labelled calls withheld, and shadow-mode agreement | Table 4.29 |
| Where each framework acts (integration points) | Figure 4.1 |
| Security–utility plane: REM, Progent policy, no defense | Figure 4.2 |
| Layer-to-implementation map with ablation variants | Figure 4.4 |
| Paired differences of each variant, by layer | Figure 4.5 |

The printed supplement (`thesis_r7/supplement/`) uses fifth-edition numbers with the prefix "S-", as in R8; it was not changed.

## Checks run on the final build (`audit/qc_checks.txt`)

| Check | Result |
|---|---|
| Assembly (`make_r9.py`) | 0 problems; every edit matched exactly once; no placeholder left; equation set unchanged; every section reference resolves to a heading |
| Printed numbers against raw-record recomputation | 191 cells, 0 mismatches |
| Citations | 105 of 105 entries cited; no citation without an entry |
| Table of contents, list of tables and list of figures | 179 page references checked. One reported mismatch is a false positive of the checker: "5.1 Introduction" also matches the text "4.5.1 Introduction". Chapter Five starts on the page that the TOC states (210). |
| Layout | Chapters start on new pages; no page ends with a caption. One short page (page 184) holds a table and a figure. |
| Visual inspection | Rendered pages of the title page, status page, abbreviations, both abstracts, every new table and figure, Tables 4.3, 4.7, 4.59 and 5.3. Three over-wide tables were restructured, with fewer columns and the same content, after the first inspection. |
| Tests | `tests/test_defence_ready_thesis.py` (4 tests: printed numbers against recomputation, assembly clean, section titles and the no-live statement, no approval claimed) passed; full repository suite **827 passed, 27 skipped, 1 xfailed, 0 failed** (26 November 2026) |
