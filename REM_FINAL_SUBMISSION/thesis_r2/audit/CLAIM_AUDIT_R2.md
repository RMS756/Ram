# Claim audit of the second edition (14 November 2026)

**Object:** `REM_FINAL_SUBMISSION/thesis_r2/` (`REM_THESIS_FINAL_R2.docx/.pdf`, the five chapter files and the appendices). The audit of the first edition (`REM_FINAL_SUBMISSION/research/REM_FINAL_THESIS_CLAIM_AUDIT.md`) remains valid for text that was not changed.

## 1. Method

1. **Numbers.** The tables of the extension study and the training table are generated from the result files by `tools/gen_ch4_r2.py`; no result number in them is typed. The prose written for this edition was checked by `tools/audit_numbers_r2.py`: of 362 distinct numbers, 11 are not found directly in the result files, and each was checked by hand: a Python version (3.11), three years, SHA-256, the Ubuntu version, the bootstrap seed, the number of resamples (2,000), the number of replays (161,506, from `REM_IMPROVEMENT_STUDY/logs/fit_replay.log`), and two amounts quoted from fixture requests (36.40 and 1,250). Derived differences quoted in the text (for example 100 and 126 more tasks; 131, 90, 18, 68 and 101 tasks in the ablations) were recomputed from the generated tables.
2. **Cross-references.** `audit/final_crossref_check.txt`: 232 numbered headings, 95 tables, 10 figures, 25 equations; 0 problems during rewriting; 0 unresolved references.
3. **Citations.** No reference entry was added or removed. The new text cites only works already in the list (T. Shi et al., 2025; Debenedetti et al., 2025; F. Jia et al., 2025; Kodathala, 2026; Hempel et al., 2026; Hossain et al., 2026; Debenedetti et al., 2024).
4. **Tests.** `python3 -m pytest`: 278 passed, 1 skipped, 1 expected failure (13 November 2026).
5. **Documents.** The Word file's stored table of contents (254 entries) equals the contents of the PDF; python-docx opens the file; 25 equations are editable.

## 2. Rules of the brief and how the text meets them

| Rule | Status in this edition |
|---|---|
| No fabricated results | Every number of the extension is generated from `improvement_results.json`; the run logs are in the repository |
| No invented equations, citations, theorem guarantees or publication status | No equation was added. The extension is described as design choices, not as published formulas. Reading levels are stated for every work that was not read in full |
| A published defense must not be imitated under its name | Arm PG is Progent's own manual policy read from the pinned repository file; the text states that it is not the paper's result, not the generated-policy mode and not a live run, and that the upstream checker was not executed. Nothing is called MELON, Task Shield or CaMeL |
| Former confirmatory data are development evidence | Stated in Sections 4.1.4, 4.2.1, 4.3.2 and 4.6.8 and in Chapters 1, 3 and 5; "untouched" no longer occurs in the present tense |
| No novelty claim from implementing | Section 3.14 and Section 4.6.9 state that the extension combines published ideas and is not a new version of REM |
| The strongest simpler baseline must be evaluated | A2 (the strongest simple rule of the earlier studies) and Progent's manual policy are in every table of Section 4.4.3 |
| Gain must be attributed to the component that causes it | Sections 4.5.3 and 4.6.9, the abstract and Chapter 5 attribute the gain to the deterministic rule and state that the learned model adds no demonstrated value |
| No non-inferiority claim from an interval that includes zero; no invented margin | Sections 4.3.4, 4.4.3 and 4.6.8 |
| "Released attack-labelled call" is not "committed unauthorized bank state" | Renamed in Chapters 3 and 4; Section 4.3.3 explains the difference |
| Paid calls need authorization | None was made; Section 4.4.4 and Appendix F (D-15) state what is blocked |
| Placeholders and supervisor decisions stay pending | Unchanged; SD-PERM added to Appendix F |

## 3. Claims that the extension study does and does not support

| Claim | Supported? | Where it is worded |
|---|---|---|
| The permission rule improves on REM v1.0 | Observed on development data (benign completion intervals above zero in both populations; not a pre-declared contrast) | 4.4.3, 4.6.9 |
| The permission rule adds value over simple rules | **No**: point estimates favourable, task-completion intervals include zero; by the wording fixed in advance the claim is not made | 4.4.3, 4.6.9 |
| The permission rule is better than a published defense | **No**: Progent's manual policy has no successful attack; the attack-success difference is above zero in both populations | 4.4.3 |
| The learned model adds value | **No**: intervals include zero under both schemes; 38 against 10 attacks under reformatting | 4.5.3 |
| The two-verdict decision is an improvement | **No** by itself (131 attacks); only a consistency repair behind a guard | 4.5.3 |
| The rule generalizes to other requests | **Not tested**: 20 author-written pairs, not independently reviewed; two parser defects reported | 4.6.9, 4.6.11 |

## 4. Residual risks

1. NEXUS, aiAuthZ, Kairos, Progent and CaMeL were not read in full (publishers' sites not reachable; no review packet in the session). Statements about them rest on abstracts and on the authors' repositories and are labelled.
2. The equivalence of the replayed Progent policy with the upstream checker rests on reading about 60 lines of code, not on executing it.
3. The main text is 29 pages longer than in the first edition. No university page limit is known to this project.
4. Text kept from earlier editions relies on the earlier audits and was re-read only where a correction of Section 12 of the brief applied.
5. The Arabic abstract remains an AI-assisted draft and needs review by a native reader.
6. Layout is not verified against university rules (no template available).
