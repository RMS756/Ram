# Claim audit of the fourth edition (15 November 2026)

## Method

1. **Numbers.** Every table of the extension study and of training is generated from the result files (`tools/gen_ch4_r4.py`, which reuses `gen_ch4_r2.py`). `audit_numbers_r2.py` checked the prose of the rewritten sections: of 245 distinct numbers, 14 are not found directly in the result files; each was checked by hand (versions, years, seed, resample count, the 468 cases of the external differential check, and the numbers inside quoted example requests).
2. **Cross-references:** 205 numbered headings, 87 tables, 9 figures, 25 equations; 0 unresolved.
3. **Page references:** 201 checked against the PDF, 0 mismatches.
4. **Citations:** 116 reference entries, all cited.
5. **Tests:** 349 passed, 1 skipped, 1 expected failure, including the 42 regression tests of revision 3.
6. **Equations:** 25 editable equations in the Word file; none added, none removed.

## Kinds of evidence, kept apart in the text

| Kind | Where | Status |
|---|---|---|
| Matcher counterexamples (call-level probes) | Section 4.6.9, first paragraph; `followup/DEFECT_REPORT.md`, `followup_v3/DEFECT_REPORT_V3.md` | Reproduced on the unchanged code of the revision concerned; development material |
| Recorded-trace development replay | Sections 4.4.3, 4.5.3, 4.6.9 | Executed; development evidence on both populations |
| Call-level audit of user task 15 | Section 4.6.9 | Executed with criteria written before the audit |
| Paired fixtures | Section 4.6.9 | Regression material for revisions 2 and 3; not a test of them |
| Validation on independently authored requests | Section 4.6.9, verdict item 5 | **Defined, not executed** |
| Live-agent or model-based evaluation | Section 4.4.4; Appendix D | **Not executed** |

## Claims about the extension and their support

| Claim | Status |
|---|---|
| Revisions 1 and 2 of the rule have the five reported defects | Reproduced; asserted by regression tests on the unchanged scored code |
| The current rule has no successful attack on either population | Measured (development evidence; the last repair targeted a known attack, so this is a regression check) |
| The current rule has fewer successful attacks than rule A2 | Measured: 0 against 13 and 0 against 4; both intervals below zero; all in user task 15 |
| The current rule adds value over simple rules, or is better overall than A2 | **Not claimed**: task-completion intervals include zero |
| The current rule is equivalent or non-inferior to Progent's manual policy | **Not claimed**: no margin exists; completed tasks not resolved |
| Binding (amount to account; instruction to effect) removes the attacks without losing tasks | Measured by the ablations: 10 → 1 → 0 and 3 → 0 → 0; no task lost |
| The learned model adds value over the current rule | **Not established**: lower bounds exactly zero under S1, S2 and on the second population. The text states that this is not evidence of absence |
| Refusing a subjective condition is costless | **Contradicted**: 167 and 119 completed tasks, all in user task 14 |
| Any result generalizes beyond the benchmark's sixteen requests | **Not tested** |
| The Progent arm is the Progent framework | **Not claimed**: it is the published manual banking policy adapted to the shared replay harness; the upstream code was not executed |

## Literature

The full-text review packet named in the external reviews (`REM_Claude_Final_Review_Packet_2026-11-12.zip`) **was not supplied to this session**. arXiv and the ACL Anthology are outside the session's network settings. NEXUS, aiAuthZ, Kairos, Progent and CaMeL are therefore still described from abstracts or from their authors' repositories, at the verification level marked in Chapter 2; no statement about them was strengthened in this edition.

## Residual risks

- The shortening removed text, not claims; a reader who needs the removed tables must use the repository documents or the third edition.
- All security differences among the restrictive arms rest on user task 15.
- The parser was written by an author who knows the benchmark's requests; no independent request set exists.
- The university's template, page limits and abstract limit are unknown to this project.
