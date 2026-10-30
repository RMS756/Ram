# Final Thesis Quality Report — 27 October 2026

Branch `claude/rem-thesis-lit-review-merge-j1px4f`. This report checks the deliverables against the master prompt and its integrity rules, and says plainly what is not finished.

## 1. Bottom line

- The **thesis is a complete six-chapter draft for supervisor review**, not a submission-ready thesis.
- Chapter 5 reports an **exploratory pilot**. The confirmatory evaluation of Chapter 3 is **pending**, for three reasons:
  - the design values await approval (SD-FREEZE);
  - live LLM enforcing-mode runs are impossible in this environment;
  - the replay-based enforcement results conflict with the Chapter 3 scope (SC-7).

## 2. Deliverables

| Deliverable (master prompt Part 12) | Location | Status |
|---|---|---|
| Thesis, full DOCX + PDF | `thesis/build/REM_THESIS_FULL.docx`, `.pdf` (≈95 pages, A4) | DRAFT — REQUIRES REVIEW; provisional formatting (template BLOCKED — MISSING SOURCE) |
| Separate chapter files | `thesis/CHAPTER1..6*.md`; `thesis/build/CHAPTER*.docx` | DRAFT — REQUIRES REVIEW |
| Novelty audit | `RESEARCH_GAP_AND_NOVELTY_AUDIT.md` | COMPLETE (bounded by the Chapter 2 search) |
| Supervisor-review document | `defense/SUPERVISOR_REVIEW_BRIEF.md` | COMPLETE |
| Defense outline; Q&A guide | `defense/DEFENSE_PRESENTATION_OUTLINE.md`, `defense/DEFENSE_QA_GUIDE.md` | DRAFT |
| Code and tests | `rem/`, `tests/` (192 passed) | IMPLEMENTED — VERIFIED BY TESTS |
| Figures, results tables, audit logs | `results/pilot/` | COMPLETE (EXPLORATORY) |
| Reproducibility instructions | `docs/REPRODUCIBILITY.md`, `experiments/pilot/run_all.sh`, `thesis/build.sh` | COMPLETE; reproduction verified |
| `PROJECT_AUDIT.md` | root | COMPLETE |
| `SOURCE_VERIFICATION_REPORT.md` | root | COMPLETE for metadata; full-text checks BLOCKED |
| `EQUATION_PROVENANCE_AUDIT.md` | root | COMPLETE; equation IDs BLOCKED (registry missing) |
| `EXPERIMENT_VALIDITY_REPORT.md` | root | COMPLETE |
| `SUPERVISOR_DECISIONS_REQUIRED.md` | root (consolidated) | COMPLETE; every item open |
| `REFERENCE_VERIFICATION_MATRIX.xlsx`, `CLAIM_EVIDENCE_MATRIX.xlsx`, `REFERENCES.bib` | root | COMPLETE for the foundational set (21 works); Chapter 2 corpus verified separately |
| `PROJECT_PROGRESS.md` | root | Updated through Phase 7 |

## 3. Integrity rules (master prompt Part 14)

| # | Rule | Check |
|---|---|---|
| 1 | No fabricated papers or citations | Foundational sources re-checked (13 Crossref-verified; discrepancies reported). No new citation was added without a lookup |
| 2 | No invented measurements | Every Chapter 5 number comes from `results/pilot/*.json`. An automated cross-check of 55 headline numbers in Chapter 5 found no mismatch |
| 3 | No untested claims of testing | Test counts are from executed runs (192 passed) |
| 4 | No invented datasets | Data are AgentDojo's recorded traces, unmodified. Synthetic data are used only in unit tests |
| 5 | No unrecorded systematic review | The Chapter 2 PRISMA record exists; no new review is claimed |
| 6 | Synthetic data not presented as results | Correct; none presented |
| 7 | Established algorithms not claimed as original | Table 3.16; novelty audit |
| 8 | Methodology not silently modified | Chapter 3 is unchanged. Interpretations (I-1 to I-8) and amendments (AM-1 to AM-4) are recorded. **One violation found and disclosed: trajectory replay (SC-7) was used although Chapter 3 excludes it.** It was identified after the runs and reported in every affected document |
| 9 | Originals recoverable | Original chapters untouched; the new versions are in `thesis/` |
| 10 | No assumed files | Missing items are marked BLOCKED (template, registry, proposal, full texts, classifier) |
| 11 | No claim of full bibliography verification | Stated explicitly: metadata only, 13/21 |
| 12 | Calibration ≠ prevention | Stated; calibration gave no measurable gain |
| 13 | Mitigation effectiveness tested | Residual ASR was measured. It is assumption-bound (NO-ADAPT) and labelled as such |
| 14 | No invented institutional policies | Costs are labelled declared exploratory values, not institutional policy |
| 15 | Negative results not suppressed | Reported in Ch. 5–6: calibration, context group, behavioural group, CUSUM, utility cost |
| 16 | No secrets or real banking credentials | None used. AgentDojo sandbox only |
| 17 | No unauthorised public push | Push authorised by the user (27 Oct 2026) |
| 18 | No placeholder presented as finished | Blocked components are marked |
| 19 | Audit trail | Each JSON carries the commit, configuration hash and versions; reproduction script provided |
| 20 | Pending decisions separated from requirements | `SUPERVISOR_DECISIONS_REQUIRED.md`; [PD] RQs; EXPLORATORY labels |

## 4. Corrections made during the final audit

1. The user_task_15 / attacker-IBAN collision was first described as a new benchmark finding. A check of later suite versions showed it was fixed upstream in v1.1.1. It was reclassified, in all documents, as a known issue of mixing trace versions.
2. The C5-9 claim (benign state-changing releases) initially had no committed result file. `benign_release_breakdown.py` was added to the reproduction script.
3. A claim that REM beats B1 under misspecified costs was verified cell by cell (36/36 cells). The check also showed that matched costs beat misspecified costs in only 34/36 cells, which is now reported.

## 5. Known weaknesses a reviewer will find

- Formatting does not follow the university template.
- The PDF TOC has links but no page numbers.
- Chapter 2 (23.6k words) dominates the length. Chapters 4–6 are concise.
- Only one benchmark; nine attacked groups; one run per configuration.
- The label audit was performed by an AI assistant.
- Unresolved citation issues: Platt and Kull (`SOURCE_VERIFICATION_REPORT.md`).
- The title wording "behavior-aware" is weakened by the pilot (novelty audit, C4).
