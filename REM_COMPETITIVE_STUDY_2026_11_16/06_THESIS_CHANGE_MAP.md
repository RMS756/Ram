# Proposed thesis change map (compact; nothing applied)

**No thesis file was changed by this study.** The fourth edition (`REM_FINAL_SUBMISSION/thesis_r4/`) stands as it is. The changes below are proposals for after the design and the evidence are settled. Prof. Omar's six sections of Chapter 4 are kept.

## Corrections that the new evidence requires (wherever the extension is reported)

| Statement in the fourth edition | What the evidence now says | Where |
|---|---|---|
| The gain of the learned arm L4 over G3 is "in user tasks 2, 9 and 13, whose amounts or values the request delegates", with the learner's value "not established" | The same gain is obtained **without any model** by the authority guard used alone (GV). The ridge model of L4/HV blocked no call on any recording or fixture. Attribute the gain to the deterministic guard | Section 4.5.3; Section 4.6.9 verdict item 4; Section 4.6.10; Chapter 5 (RQ4 row, contributions row 8, recommendation table, conclusion) |
| Progent: "The paper was not read; the official code was" | Version 3 of the paper (17 pages) was read in full; the manual banking policy is an artefact of repository commit `9befb41` and is not a configuration of that version | Chapter 2, Table of closest works and the "reading of repositories" paragraph; Section 4.4.3; Section 4.4.5; threat 15 |
| Progent's formal property not described | Monotonic confinement, its scope, the auto-approve default, and the gap in the released subset check until 15 November 2026 | Section 4.4.5 (one paragraph) |

## By section of Chapter 4

| Section | Proposed addition (short) | Source |
|---|---|---|
| 4.1 Implementation tools and environment | One row: scikit-learn 1.9.1, SciPy 1.17.1, cedarpy 4.12.2, used only by the exploratory study | `EXPOSURE_AND_SPLIT_MANIFEST.json` |
| 4.2 Dataset preparation and training | One paragraph: the grouped half split inside each training portion for the two calibrated cutoffs; the nested selection of the boosted model | `PROTOCOL.md`, Section 5 |
| 4.3 Experimental setup and evaluation metrics | Rows in the arms table for GV, NP, CRC, GB, HVnc, HV4, GVc, GVp; the wording rules; the statement that no formal guarantee is claimed | `PROTOCOL.md`, Sections 4, 6, 10 |
| 4.4 Comparisons with existing models and defense frameworks | GV against PG in one sentence with the intervals; the three Progent settings and which one was run; Cedar parity in two sentences | `04_RESULTS_AND_INTERPRETATION.md`, Sections 3 and 5 |
| 4.5 Ablation studies | One table: guard alone against the learned variants (identical), calibration removed, four verdicts, NP, CRC, GB, provenance rule; the observation that every attack-labelled call is stopped by the front | `03_RESULTS_TABLES.md`, Tables 1, 5, 13 |
| 4.6 Results and discussion | Replace the attribution paragraph; add the limit that the benchmark's attacks do not reach the stage where a learner acts; keep "development evidence" | `04_RESULTS_AND_INTERPRETATION.md`, Sections 1 and 6 |

## Chapter 2, Chapter 3, Chapter 5

- **Chapter 2:** Progent entry rewritten from the full text; Cedar, FIDES and CaMeL mentioned selectively at the verification level of `11_RELATED_WORK_PROPOSALS.md`, Section 1. No statement taken from Progent's related-work section as a verified fact.
- **Chapter 3:** nothing in the specification of REM changes. Section 3.14 (extension) could gain three sentences defining GV and the direct-value constraint. The NP, CRC and boosted variants are **not** added to the methodology unless the supervisor wants negative results described there.
- **Chapter 5:** the answer to RQ4 becomes sharper (the measured change belongs to deterministic request-derived authorization; no learned component contributed behind it); future work gains the independent request set with open-amount cases and the live comparison.

## Decisions for the supervisor before any of this is written

1. Whether the exploratory extension stays in the thesis at all, and if so whether GV (guard alone) replaces L4/HV as the reported arm (SD-PERM).
2. Whether predicate D2 should apply behind the authority front (it withholds 55 and 62 request-supported calls).
3. Whether negative results on NP, CRC and boosted trees belong in Chapter 4 or in an appendix.
4. Page budget: the fourth edition has 281 pages; these additions should replace text, not add to it.
