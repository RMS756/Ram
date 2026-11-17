# Response to the independent review of commit 621a271 (17 November 2026)

Review: `REM_Repair_R6_Independent_Review_AR_2026-11-17.md`. Each recommendation below is listed with the action taken and its status. The version-1 results and the thesis editions R5 and R6 are kept unchanged.

| # | Recommendation of the review | Action | Status |
|---|---|---|---|
| 1 | Keep the results of 17 November; reproduce the two new defects with positive and negative cases | `DEFECT_REPORT_D3_D4_2026-11-17.md`; `reproduce_defects_d3_d4.py v1` reproduces 24 unauthorized releases on the unchanged version-1 arms; version-1 code and results added to `FROZEN_INPUT_HASHES.json` | executed |
| 2 | Repair parsing of the whole calculation; bind every element of authority to one instruction; record as a dated amendment | `amount_verifier_v2.py` (coverage of the amount phrase; single witnessing instruction; conditions as in the frozen front); `PROTOCOL_AMENDMENT_V2.md` committed before scoring (`95549b2`); 104 tests | implementation-tested; D3/D4 diagnostics 24 → 0 |
| 3 | Separate grammar extension from the acceptance repair; measure each on correct tasks and attacks | separate arms (GV_math2 / GV_math2x and HV_math2 / HV_math2x); `13_V2_RESULTS_TABLES.md` | executed: acceptance repair changes no episode and loses fixture S1; extension changes no episode and recovers fixture P2 |
| 4 | Correct the description of the stage order and of the counts; compare guard and learner on an identical front | version 2 evaluates the verifier only after a release (`amount_evaluated` in the audit); 0 of 907 and 0 of 559 attack-labelled calls reached it; the version-1 wording is corrected in R7 (Section 4.5.4); HV_math2 = GV_math2 | executed; learned contribution **not established** |
| 5 | Complete the independent-validation tooling and the matched Progent comparison; do not turn plans into results | the kit and the protocol remain `NOT EXECUTED` (`07_…`, `08_…`). No person other than the developer has written requests, and no credential or budget is available | **not executed** |
| 6 | Update the thesis after the results stabilize; shorten history and repetition; complete missing reference data | R7 (`REM_FINAL_SUBMISSION/thesis_r7/`): version-2 results, corrected stage order, condensed Section 2.8.3. The PACT author list is still incomplete (3 of 6; arXiv not reachable from this session). The body is still far above the page target | partial |

What this response does **not** claim:
- that the verifier is complete: fixture S1 shows a new over-blocking failure of the coverage rule;
- that the learner adds value;
- superiority or equivalence with respect to Progent;
- independent validation.
