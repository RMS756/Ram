# Claim audit of the third edition (14 November 2026)

## Method

1. **Numbers.** Every table of the extension study, of the follow-up and of training is generated from the result files (`gen_ch4_r2.py`). `audit_numbers_r2.py` checked the prose written for the second and third editions: of 394 distinct numbers, 15 are not found directly in the result files; each was checked by hand (versions, years, seed, resample count, replay count from the log, the 468 cases of the external differential check, two fixture amounts, the balance and threshold of counterexample C2 (500, 1000), and the postal code 10001 of user task 15).
2. **Cross-references:** 234 numbered headings, 98 tables, 10 figures, 25 equations; 0 unresolved.
3. **Page references:** 364 checked against the PDF, 0 mismatches (`page_reference_check.json`).
4. **Tests:** 307 passed, 1 skipped, 1 expected failure (14 November 2026), including 29 new regression tests of the follow-up.
5. **Equations:** 25 editable OMML equations in the DOCX.

## Claims of the follow-up and their support

| Claim | Status |
|---|---|
| The frozen rule G1 has the three reported defects | Reproduced (`followup/counterexamples_v1.json`); asserted in the regression tests |
| The repaired rule G2 removes 9 of G1's 10 successful attacks without losing tasks through the binding check | Measured (development evidence; written after G1's results were known) |
| G2 adds value over simple rules | **Not supported**: task-completion intervals against A2 include zero |
| G2 is better or worse than Progent's manual policy | **Not resolved** on either outcome |
| The authority guard removes L2's robustness failure | Measured: 38 → 10 attacks under reformatting, one task lost |
| The learned model adds value over the repaired rule | **Not established**: interval lower bounds are exactly zero |
| Typed provenance in the learner helps | **Not supported**: no measured effect |
| G1's attacks in user task 15 are artefacts of the account collision | **Contradicted** by the call-level audit: the released calls send amounts the user did not ask to send to that account |
| Any result generalizes beyond the benchmark's requests | **Not tested** |

## Literature

The full-text review packet named in the external review (`REM_Claude_Final_Review_Packet_2026-11-12.zip`) **was not supplied to this session**: the session's upload folder contains the six PDFs of 11 November and the review page of 14 November, nothing else. The publishers' sites (arXiv, ACL Anthology) are outside the session's network settings. NEXUS, aiAuthZ, Kairos, Progent and CaMeL therefore remain at the reading levels stated in Chapter 2; the NEXUS README's policy is no longer attributed to the published paper.

## Residual risks

As in the second edition, plus: the repairs and the user-task-15 audit criteria were written by an author who knew the earlier results; the audit's strict criteria classify agent errors without the attempt label as violations, which is reported separately from the security result.
