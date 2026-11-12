<!-- @frag app_a_intro -->
This appendix holds material of the systematic review that Chapter 2 summarizes: the comparative evidence matrix of the 42 defense and design studies, and three supporting tables. The tables are reproduced unchanged from the review record of September and October 2026.

<!-- @frag app_b_intro -->
This appendix gives the implementation details that Chapter 3, Section 3.42, summarizes. It is reproduced from the thesis draft of 3 to 5 November 2026 without change of content. Test counts in this appendix are those of 1 November 2026 (205 tests); the count on 11 November 2026, after the integration, deployment-simulation and study tests were added, is 241 passed, 3 skipped and 1 expected failure.

<!-- @frag app_d_intro -->
This appendix records the design and status of two evaluations that were implemented and **not executed with a language model**: the closed-loop evaluation of REM with live agents, and the controlled evaluation of MELON with and without REM. Nothing in this appendix is an experimental result. The checks it reports use scripted agents and simulated providers and establish only that the integrations are mechanically correct. The text is reproduced from the thesis drafts of 3 to 6 November 2026.

<!-- @frag app_e_intro -->
This appendix reports the replay results of Chapter 4, Section 4.6, under both mitigation semantics. Step-level semantics is the declared reference, pending the supervisor's decision on conflict SC-1. The episode-level rows are a sensitivity analysis.

<!-- @frag app_decisions -->
**No supervisor decision is recorded in the project repository.** Every item below is open. Where the thesis needed a wording, it uses the option marked "handling", labelled as pending. The full register, with options and effects, is kept with the project records (`SUPERVISOR_DECISIONS_REQUIRED.md` and the register of the five-chapter draft).

**Table 5.44. Open decisions that determine what the thesis may claim**

| ID | Item | Handling in this thesis | Decision needed |
|---|---|---|---|
| SD-FREEZE | Approval of the Chapter 3 specification as frozen | Implemented as specified; values declared | Approve or amend |
| SD-FEAT | Feature set; **proposed amendment REM v1.1** (behavioral evidence removed) | v1.0 is the design; v1.1 is reported beside it as a confirmed ablation | Approve v1.1, or keep v1.0 |
| D-9 | Costs, tier map and predicates | Declared exploratory values | Approve, or elicit new values |
| SC-1 / D-2 | Mitigation semantics: step-level or episode-level | Step-level reference; episode-level in Appendix E | Confirm |
| SC-2 / D-4 | Tie rule | Chapter 3 order, with ties counted; no tie occurred in any run | Confirm |
| SC-3 | Calibration-removed ablation run in the evaluation path | Reported | Confirm |
| SC-4 / D-3 | Calibration fitting target: labels or Platt's smoothed targets | Both implemented; label fit is the reference | Confirm |
| SC-5 | Brier score convention | Binary convention reported, with the convention stated | Confirm |
| SC-6 | Layer label of the estimator in code comments | Decision Engine in the thesis; code comment differs | Confirm |
| SC-7 / D-1 | Recorded-trace replay against the original scope, which excluded replay-based estimation | Kept as a labelled NO-ADAPT analysis | Keep, drop, or replace by live runs |
| D-6 | Label rule; the user_task_15 collision; no human label audit | Rule kept; collision reported; audit package prepared, not annotated | Keep or redefine; audit |
| D-7 | Reviewer model for Escalate | Two bounds; headline results use no reviewer | Confirm |
| D-8 / SD-DET | Injection classifier of the Detection Layer | Absent; not replaced | Choose a classifier, or record its absence as final |
| D-10 | Wording of the research questions | Marked proposed | Confirm |
| D-12 | Thesis title | As supplied by the author | Confirm |
| D-15 | Live closed-loop experiment and the MELON comparison: backbone, decoding, repeats, budget, credentials | Not run | Authorize with a spending limit, or accept submission without them |
| SD-5 | Banking-only evaluation against objective O1, which also names task-automation agents | O1 achieved for banking only | Accept or extend |
| GAP | Research-gap wording of Chapter 2, Section 2.13.42 | Proposed wording | Confirm |
| RULES | Rule baselines P1, P2 and A2 as mandatory comparators | Included | Confirm |
| RG-1 | Authoritative equation registry | Missing; no equation identifier was created | Provide, or accept the provenance table of Appendix C |
| OI-01 to OI-06 | Statements about NEXUS | Abstract and repository documentation only; full text not read | Supply the full text |
| FULLTEXT | Full texts of aiAuthZ and Kairos; full-text screening of the systematic review | Abstract level; six papers read in full in November 2026 | Supply; decide on a full-text update |
| N-1, N-2 | Supervisor roles on the title page; faculty, department and degree | As in the latest instruction; not verified against official records | Confirm |
| N-3 | Arabic abstract and Arabic spellings of names | Draft translation | Review |
| N-6 | The co-supervisor is a co-author of one cited study (Kanaker et al., 2026) | Cited as a source only; evidence level stated | Decide whether a disclosure is required |
| N-8 | Committee page, declaration (including any declaration on the use of AI tools), dedication, acknowledgement | Placeholders | Complete with the university's wording |
| N-9 / TEMPLATE | University thesis template and formatting rules | **Not available**; an assumed A4 thesis layout is used | Provide; re-check the layout |

Smaller items (the Platt reference year, the regularization convention, one cell of the false-positive grid, and the optional sequential analysis) are listed in the project register and do not affect any reported result.
