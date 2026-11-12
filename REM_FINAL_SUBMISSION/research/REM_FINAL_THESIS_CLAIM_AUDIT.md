# REM final thesis claim audit

**Date:** 12 November 2026. **Object:** the final five chapters and appendices in `REM_FINAL_SUBMISSION/thesis/src/` (built to `REM_THESIS_FINAL.docx/.pdf`).

## 1. Method

1. **Numbers.** Every number in the new text written for the final chapters (`thesis/text/*.md`) was extracted by script and matched against the numbers in the result files (`REM_FINAL_SUBMISSION/results/*.json`, `REM_Authorization_Generalization_Study/results/*.json`, `results/pilot_R2/*.json`, `results/pilot_R4/*.json`). Of 393 distinct numbers, 49 had no direct match. Each of the 49 was checked by hand: 21 are section, table or chapter numbers; 9 are negative interval bounds (the extractor drops the sign); 8 are figures quoted from papers (NEXUS 0.6406, 0.861, 0.897, 27.3; MELON 80.41, 68.04) or from the project records (205 tests on 1 November; 825 corpus texts); 7 are percentages or sums derived from result counts and recomputed by hand (7.8 = 4/51; 43.4 = 916/2,113; 70.6 = 36/51; 40 = 134/334; 2,162 = 448+448+402+288+576; 5,426 = 3,313+2,113; 28.30 = interval point); the remainder are the seed, the number of resamples and SHA-256. **No untraceable number was found.** Text kept from the draft of 3–6 November was audited in the earlier claim audit (`REM_FINAL_THESIS/final_five_chapters/audit/SCIENTIFIC_CLAIM_AUDIT.md`) and was not changed.
2. **References.** Every author–year citation in the chapters and appendices was matched by script against the final reference list; all resolve. Four entries were added (AgentBoundary, CASEL, aiAuthZ, Kairos), three were completed or updated (NEXUS to its published version; PROVISO full author list; reading level marked on the six full-text papers). Bibliographic data of the four new entries were checked against index records on 12 November 2026.
3. **Cross-references.** All section, table, figure, equation and appendix references resolve (`thesis/audit/final_crossref_check.txt`: 0 unresolved).
4. **Tests.** `python3 -m pytest`: 241 passed, 3 skipped, 1 expected failure (12 November 2026). No file under `rem/` or `configs/` was changed.

## 2. Claims checked against the Part 9 rules

| # | Rule | Status in the final text |
|---|---|---|
| 1 | No fabricated numerical results | Satisfied (Section 1) |
| 2 | No invented references | Satisfied; four new entries verified against index records |
| 3 | No untraceable formulas | No new equation. The intervention-value rule is described in words and labelled "derived, not quoted" (Ch. 3, §3.11.11). The authorization evidence is a declared definition, not a published formula |
| 4 | No silent changes to the frozen baseline | REM v1.0 unchanged and reported in every table; REM v1.1 presented as a proposed amendment (Ch. 3, §3.13; Appendix F, SD-FEAT) |
| 5 | No incompatible benchmarks presented head-to-head | Published figures appear only in Table 2.41 and are stated as not comparable; Table 4.56 explains why none was run |
| 6 | No claim that authorizations are identifiable from text | The opposite is a stated finding (Ch. 4, §4.14.2; Ch. 5) |
| 7 | No post-hoc presented as confirmatory | Post-hoc items labelled (Table 4.45; Table 4.49; Ch. 4 §4.13.1); only §4.15 is called confirmatory, with its procedural meaning stated |
| 8 | No invented human-review effectiveness | Escalation burden reported without any assumed reviewer accuracy |
| 9 | No replay reported as live | Every results section states its evidence kind; §4.16 states that no live run exists |
| 10 | No unsupported novelty claims | Novelty limited to an evaluation contribution; mechanism novelty explicitly disclaimed |
| 11 | No false claim of completed experiments | MELON and the live harness described as implemented and not executed |
| 12 | No hidden exclusion of unfavourable examples | All exclusions counted (AM-1, AM-4); fixtures failing for REM v1.1 reported; the rule A2's higher utility reported |
| 13 | No claims without code, measurement or literature | Contribution table (Table 5.3) links each claim to precedent, code, experiment and result |

## 3. Wording checked and corrected during assembly

| Location | Earlier wording | Final wording | Reason |
|---|---|---|---|
| Ch. 1, gap | absence of a combined calibrated, consequence-aware evaluation | evidence gap on value over simple rules under unseen tasks and objectives | NEXUS and CASEL publish the decision form |
| Ch. 2, NEXUS | "preprint"; preprint abstract figures | published version; figures of the published abstract; preprint and README figures given as differences | Published record checked 11 November |
| Ch. 4, verdicts | four graduated verdicts | in this evaluation the four verdicts act as two | Measured: 0 of 3,313 episodes change |
| Ch. 4, fixtures | "the user mentions a payee and an amount" | the user mentions a past payment and states that no payment is to be made | Matches the fixture text |
| Ch. 4, reformatting | both REM versions robust "because the novelty indicator keeps the score above the Allow region" | consistent with the narrow Allow region; per-feature contribution not examined | The causal claim was not tested |
| Ch. 4, tasks 9 and 10 | restrictive arms help because the attack diverts the agent | cause not examined call by call | Not tested |
| Ch. 5, conclusion | REM "reduces financial harm" | not established without live runs | Rule 9 |

## 4. Residual risks

1. Three close works (NEXUS, aiAuthZ, Kairos) are known from abstracts (NEXUS also from its README). Statements about them are labelled; they may change when the full texts are read.
2. Text kept from the draft of 3–6 November relies on the earlier audits; it was not re-verified line by line in this pass.
3. Layout is not verified against university rules (no template available).
4. The Arabic abstract is an AI-assisted draft.
