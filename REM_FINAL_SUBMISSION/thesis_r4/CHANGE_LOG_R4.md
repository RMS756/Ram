# Change log: fourth edition (condensed), 15 November 2026

**Files:** `REM_THESIS_FINAL_R4.docx`, `REM_THESIS_FINAL_R4.pdf`. **Status:** draft for supervisor review; not approved; not submitted. The third edition (`../thesis_r3/`), the second (`../thesis_r2/`) and the first (`../thesis/`) are unchanged. Nothing was deleted from the repository: every passage removed here remains in the third edition and in the documents named below.

Two things were done: the thesis was shortened at the student's request, and the third revision of the exploratory permission rule (study records in `REM_IMPROVEMENT_STUDY/followup_v3/`) was reported.

## 1. Size

| Part | Third edition | Fourth edition |
|---|---|---|
| Preliminary pages (title to status page) | 27 | 20 |
| Chapters 1 to 5 | 183 | 174 |
| References | 15 (118 entries) | 14 (116 entries) |
| Appendices A to F | 89 | 73 |
| **Total pages** | **314** | **281** |
| Words, Chapters 1 to 5 | 58,696 | 56,094 |
| Words, appendices | 22,840 | 18,585 |
| Tables / figures / numbered equations | 98 / 10 / 25 | 87 / 9 / 25 |

Chapter 4 went from 67 to 59 pages and from 45 to 39 tables, and still has the six sections requested by the supervisor.

## 2. What was shortened, and where the removed text remains

| Change | Pages saved (approx.) | Where the removed material remains |
|---|---|---|
| Table of contents lists two heading levels instead of three (105 entries instead of 256). All headings are still numbered in the text | 6 | Third edition |
| Chapter 4: the five sections on the exploratory extension (former 4.4.3, 4.5.3, 4.5.4, 4.6.9 and 4.6.10; about 5,900 words and 13 tables) are now three sections (4.4.3, 4.5.3, 4.6.9; about 3,200 words and 7 tables) built on the current revision of the rule. Removed: the separate tables for the second population, the reformatted-identifier probe, the per-task counts, the single-component ablation table of revision 1, the analysis without user task 15 (stated in one sentence), and the learned variants L0, L1, L2s, L3 and L3c | 8 | `REM_IMPROVEMENT_STUDY/05_RESULTS.md`, `followup/RESULTS_V2.md`, `followup_v3/RESULTS_V3.md`; third edition, Sections 4.4.3, 4.5.3, 4.5.4, 4.6.9, 4.6.10 |
| Chapter 3, Section 3.14 (extension): rewritten around instructions; the table of arms was removed (the arms are in Table 4.8) | under 1 | Third edition, Section 3.14 |
| Appendix A: seven background units outside the evaluated threat model were removed (agent architecture; tool-channel threats; memory manipulation; multi-step drift; input-level protection; information-flow defenses; sequential evidence). The unit "Why logistic regression" was kept because it carries Equation 2.1 | 6 | Third edition, Appendix A.19 to A.26 |
| Appendix D: the design text of the two unexecuted evaluations (closed-loop harness; MELON with and without REM; 11 pages, 1 figure, 4 tables) was replaced by a status note of half a page | 10 | `experiments/live/`, `experiments/melon_rem/`; third edition, Appendix D |
| Tables of more than about ten lines may now break between rows (the header stays with the first row and the last row never stands alone). This removes half-empty pages before tables; no text changed | 3 | n/a |
| Two reference entries that were cited only in the removed background units (Schick et al., 2023; Yu et al., 2025) | under 1 | Third edition |

Nothing was removed from: the abstract's content, Chapters 1 and 2, the specification of REM in Chapter 3, the results of REM v1.0 and v1.1, the rule baselines, the generalization study, the confirmatory run, the threats to validity, the evidence matrix of the systematic review, the implementation appendix, or the register of open decisions.

## 3. New content: revision 3 of the permission rule

Reported in Chapter 3, Section 3.14, and Chapter 4, Sections 4.3.1, 4.3.4, 4.4.3, 4.5.3 and 4.6.9; summarized in the abstracts, Chapters 1 and 5 and Appendix F. All tables are generated from `improvement_results.json`, `results_v2.json`, `ut15_call_audit.json` and `results_v3.json` by `tools/gen_ch4_r4.py`.

- Two further defects reported by an external review of 15 November were reproduced on the unchanged revision-2 code and repaired in separate code under a protocol committed before scoring: a request to create a standing order licensed an immediate transfer; only the first comparison of a compound balance condition was evaluated.
- Current rule (G3), development evidence: no successful attack on either population (0 of 2,979; 0 of 2,065); 1,407 of 3,313 and 1,239 of 2,113 tasks completed.
- Against rule A2: a security difference (0 against 13 and 0 against 4 successful attacks; both intervals below zero) and an unresolved difference in completed tasks. Stated as such; neither added value over simple rules nor overall superiority is claimed.
- Against Progent's manual policy (replay adaptation): no successful attack for either; completed tasks not resolved; no equivalence or non-inferiority claimed.
- Learned model against the current rule under identical splits: interval lower bounds exactly zero; "not established", with the explicit statement that this is not evidence of no value.
- Cost of not treating a subjective condition as satisfied: 167 and 119 completed tasks, all in user task 14 (open decision SD-COND).
- Validation on requests written and reviewed by other persons: defined (authoring instructions and a sealed scorer in the repository), **not executed**. Live-agent and model-based comparisons: **not executed** (no credential, no spending authorization).

## 4. Corrections

| Item | Earlier editions | This edition |
|---|---|---|
| Cross-reference in Section 4.5.2 | The second and third editions read "Two ablations of Table D.2" and "(Table D.2: 0.329 against 0.314)". The reference was wrong: it should name the ablation table | "Table 4.16" (the ablation table) in both places |
| Section 4.6.10, frontier paragraph | "On the second population every arm with attack success below 0.5% completes at most 64.3% of tasks." The learned arms of the extension complete more (65.6% and 70.5%) | Scoped to the rules and policies of Tables 4.33 and 4.13, with the figures of each |
| Wording about the learned model | "adds no demonstrated value" | "value not established", with the statement that this does not show absence of value |
| Wording about rule A2 | "advantage over the strongest simple rule is not resolved" | A security difference on development data is stated; overall superiority is not claimed |
| Pointers from Chapter 2 to removed appendix units | "reviewed in Appendix A" | Rewritten; no pointer leads to removed text |

## 5. Verification of this edition

- Assembly: 0 problems, 0 unresolved cross-references (205 numbered headings, 87 tables, 9 figures, 25 equations).
- Page references: 201 entries of the table of contents and of the lists of tables and figures checked against the PDF, 0 mismatches (`audit/page_reference_check.json`).
- Word file: table of contents stored in the field result (105 entries); 25 editable equations; rendering environment identical to the pinned one (`audit/render_environment.json`).
- Numbers: the prose of the rewritten sections was checked against the result files (245 distinct numbers; the 14 not found directly are versions, years, the seed, the resample count, the 468 cases of the external differential check and the numbers of the quoted example requests).
- Citations: 116 reference entries, each cited in the text (`audit/citation_check.json`).
- Tests: 349 passed, 1 skipped, 1 expected failure (15 November 2026).

## 6. Further shortening that needs a decision

These were **not** done, because each removes material that a supervisor or examiner may expect. Page figures are from this edition.

| Option | Pages | Remark |
|---|---|---|
| Replace Appendix B (implementation details) by a one-page summary | about 15 | The code organization, the traceability table and the timer boundaries would remain only in the repository; Section 3.15 and Section 4.1 keep the overview |
| Remove the full text of the two literature updates (A.20, A.21) | about 6 | Their summary is in Chapter 2, Section 2.12 |
| Remove the literature background kept in Appendix A (A.12 to A.14, A.16) | about 5 | Chapter 2 summarizes each in a paragraph |
| Remove Appendix E (results under both mitigation semantics) and C.4 (equation provenance) | about 5 | E supports conflict SC-1; C.4 supports the statement that no equation is new |
| Shorten Section 2.12 (research gap and positioning, 10 pages) and Section 3.11 (experimental methodology, 13 pages) | 5 to 8 | Rewriting of verified text; needs a careful pass |
| Report the earlier studies of Section 4.6 (generalization, probes, confirmatory run; 16 pages) more briefly | 5 to 8 | These are results; shortening them moves evidence to the repository |
| Remove the comparative evidence matrix of the systematic review (A.5) | 12 | Not recommended: it is the evidence base of Chapter 2 |
| Shorten the abstract (about 650 words) to a university limit | under 1 | The limit of the university is not known to this project |
