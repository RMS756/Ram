# Change log: fifth edition, 17 November 2026

**Files:** `REM_THESIS_FINAL_R5.docx`, `REM_THESIS_FINAL_R5.pdf`. **Status:** draft for supervisor review; not approved; not submitted. The four earlier editions (`../thesis/`, `../thesis_r2/`, `../thesis_r3/`, `../thesis_r4/`) are unchanged.

This edition applies the change map of the competitive study of 16 November 2026 (`REM_COMPETITIVE_STUDY_2026_11_16/06_THESIS_CHANGE_MAP.md`). Every new number is generated from the result files of that study and of the integration study of 16 November (`tools/gen_ch4_r4.py`); none was typed by hand. Nothing in the specification of REM v1.0 or v1.1 changed.

## 1. Size

| Part | Fourth edition | Fifth edition |
|---|---|---|
| Total pages | 281 | 289 |
| Preliminary pages | 20 | 21 |
| Chapter 4 (printed pages) | 104–162 (59) | 104–167 (64) |
| Chapter 5 | 163–174 | 168–180 |
| References | 116 entries | 121 entries |
| Words, Chapters 1 to 5 | 56,094 | 58,005 |
| Tables / figures / numbered equations | 87 / 9 / 25 | 87 / 9 / 25 |

The additions replace text where they could: the table of learned arms on permission evidence and three contrast rows of the learned model, now superseded, were removed (their key numbers are in the text), and the new table has five columns, with the double-holdout and probe results stated below it.

## 2. Corrections that the new evidence requires

| Statement of the fourth edition | Fifth edition | Where |
|---|---|---|
| The learned model's value over the rule "is not established"; its gain is in user tasks whose values the request delegates | The gain of L4 over G3 is obtained without any model by the authority guard used alone (GV); every learned or calibrated decision tested behind the guard gives GV's outcomes, because every attack-labelled call is stopped before a model is consulted | 4.5.3; 4.6.9 verdict 4 and 6; 4.6.10 (interpretation, conclusions table row 10, "what the evidence does not support"); 4.6.12; Chapter 5 (RQ4, contribution 8, recommendations, conclusion); Chapter 1 (contribution 7); both abstracts |
| Progent: "The paper was not read; the official code was"; cited as T. Shi et al. (2025) | Version 3 of the paper (17 pages, 14 May 2026) read in full and cited as T. Shi et al. (2026); author order corrected to that of version 3 (Li before Wu) | Chapter 2 (table of closest works, reading paragraph); 4.4.3; 4.4.5; threat 15; references |
| The manual banking policy described as "the manual banking policy published in the Progent repository" without date or status | It is a policy of the repository at the commit of 10 September 2025, removed on 13 May 2026, and **not a configuration evaluated in version 3 of the paper** | 4.3.1; 4.4.3; 4.4.4; 4.4.5; 4.6.12; Chapters 1 and 5; abstracts; status page |
| Progent's formal property not described | One paragraph on monotonic confinement, its scope, the auto-approve default and the gap in the released narrowing check until 15 November 2026 | 4.4.5 |

## 3. Additions, by section of Chapter 4

| Section | Addition |
|---|---|
| 4.1 | Packages used only by the study of 16 November (SciPy, scikit-learn, cedarpy); the two new code folders; re-execution of the integration study prepared by another assistant (123,776 replays, identical outcomes); test suite of 16 November (500 passed, 1 skipped, 1 expected failure) |
| 4.2 | Training of the two half-split ridge models and of the boosted trees |
| 4.3 | Arms GV and the decision methods behind it; the sixth set of comparisons fixed in advance |
| 4.4 | GV in Table 4.13 and GV minus the published policy in Table 4.14; the status of the policy; Progent's guarantee |
| 4.5 | Table 4.19 (decision methods behind the guard: ridge with and without calibration, four verdicts, two Neyman-Pearson and two conformal thresholds, boosted trees, Cedar policies, a provenance rule) and seven findings, including the transfer of the thresholds to unseen attacker objectives, Cedar decision parity and predicate D2 |
| 4.6 | Verdict, interpretation, threats (new threat 18: the benchmark's attacks do not reach the decision behind the guard) and summary updated |

Chapter 3, Section 3.14, gains paragraph E (direct-value constraint; GV). Appendix F gains decision SD-D2 and updates SD-PERM and FULLTEXT. New references: Angelopoulos et al. (2022); Cedar Policy (2026); Costa et al. (2025); Friedman (2001); Tong et al. (2018). Their metadata were checked against Crossref or the authors' repositories; the full texts of the four papers were not read, and each entry says so.

## 4. Errata of the fourth edition

- **Title page.** The title page of the fourth edition read "third edition (14 November 2026)"; the status page was correct. Corrected here.
- **Progent author order.** The reference entry listed "Wu, L., Li, H."; version 3 lists Hongwei Li before Linyu Wu.

## 5. Verification

- Assembly: 0 problems, 0 unresolved cross-references (205 numbered headings, 87 tables, 9 figures, 25 equations).
- Page references: 201 entries of the table of contents and the lists of tables and figures checked against the PDF, 0 mismatches.
- Word file: 25 editable equations; table of contents stored (105 entries); rendering environment identical to the pinned one.
- Citations: 121 reference entries, each cited.
- Numbers: 288 distinct numbers in the rewritten text; the 20 not found directly in the result files are years, the seed, versions, test counts, the replay count of the re-execution, the 468 cases of the external differential check, and numbers inside quoted example requests.

## 6. Decisions still open (Appendix F)

SD-PERM (whether the extension stays, and GV as its reported arm), SD-COND (subjective conditions), SD-D2 (predicate D2 behind the guard), and all earlier ones. The fifth edition reports GV as the best supported arm on development data; it does not adopt it into REM.
