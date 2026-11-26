# Final submission checklist: REM defence-ready thesis

Status after the final compliance audit of 26 November 2026. **[x]** = verified in this repository. **[ ]** = must be done by the student or supervisor outside this environment.

## Files to send

- [x] `REM_Master_Thesis_Defence_Ready.pdf`: 272 pages, A4, rebuilt after the audit corrections
- [x] `REM_Master_Thesis_Defence_Ready.docx`: same content, editable
- [x] Optional companions for the supervisor:
  - `SUPERVISOR_REQUIREMENTS_MAPPING.md`
  - `FINAL_ACADEMIC_COMPLIANCE_AUDIT.md`
  - `ABLATION_LAYER_COVERAGE_MATRIX.md`
  - `FRAMEWORK_COMPARISON_VALIDATION.md`
- [x] Not for the supervisor (student's own preparation): `DEFENCE_PREPARATION.md`, `UNRESOLVED_ISSUES.md`

## Content

- [x] Requirement 1 (layer ablation) addressed in Section 4.5; isolation limits stated in 4.5.1, 4.5.4, 4.5.5 and 4.5.11 and in threat 21
- [x] Requirement 2 (framework comparison) addressed in Section 4.4. Kinds of evidence kept apart. No security result is claimed for DRIFT or MELON.
- [x] Progent's benchmark-informed policy disclosed (4.4.8); no superiority claim for REM anywhere
- [x] No live experiment claimed; offline replay labelled throughout
- [x] RQs labelled as derived and not approved (1.7, 5.2); design values labelled as declared
- [x] Title, scope and five-layer architecture unchanged; no sixth layer; no new chapter; equations unchanged
- [x] No claim of formal approval (title page, status page)

## Numbers

- [x] 11 / 2,979 and 105 / 334 (REM); 0 / 2,979 and 154 / 334 (Progent); 21 backbones; no "22 backbones" anywhere in the thesis
- [x] 466 printed cells, including intervals, discordant counts and p-values, match a fresh recomputation from the raw records (`audit/thesis_number_check.json`)
- [x] "661 of the 672 prevented attacks" error corrected in all six places (EN and AR abstracts included)

## References

- [x] 105 entries, all cited; no citation without an entry
- [x] DRIFT: DOI, venue and pages verified with Crossref; code verified
- [ ] DRIFT: check the third author's name form ("Hung-Chun Chiu" in the repository; "CHIU Chun" in Crossref) against the published PDF
- [ ] AgentDyn: check the full author list against the arXiv PDF
- [ ] Optional: read the DRIFT full text; the thesis currently states that it was read at abstract level

## Formatting (outside this environment)

- [ ] Open the DOCX in Microsoft Word with Times New Roman installed. Select all, update fields (F9), and check that TOC, LoT and LoF page numbers are current.
- [ ] Check the page breaks of the wide tables 4.12, 4.25 and 5.3 in Word
- [ ] Apply the university's official template if one exists. The current layout is an assumed A4 style.
- [ ] Verify faculty, department and degree title on the title page against official records

## Front matter (outside this environment)

- [ ] Committee decision page: completed by the university after the defense
- [ ] Declaration of authorship: university wording, signed by the student
- [ ] Dedication and acknowledgement: student
- [ ] Arabic abstract: native-speaker check, especially the two new paragraphs

## Supervisor decisions still open (stated in the thesis; not blocking discussion)

- [ ] Confirmation or rewording of RQ1–RQ4
- [ ] Approval of the declared design values (costs, tiers, predicates, feature set, label rule) and the replay amendment
- [ ] Decision on the proposed REM v1.1 (without behavioral evidence)
- [ ] Whether to trim the repeated R8 units inside Sections 4.4.7 and 4.5.7

## Reproducibility (in the repository)

- [x] `tools/verify_numbers.py` → `tools/make_figures.py` → `tools/make_r9.py` → `tools/build_r9.py` → `tools/check_thesis_numbers.py`
- [x] `tests/test_defence_ready_thesis.py` and the full test suite pass
- [x] R8 source unchanged; all previous commits preserved
