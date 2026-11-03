# FINAL SUBMISSION READINESS — five-chapter thesis

**Date:** 3 November 2026. **Branch:** `claude/rem-r4-corrections-3ktvze`.

## Verdict

| Question | Answer |
|---|---|
| Ready for **supervisor review**? | **YES**, as a draft clearly labelled "Draft for supervisor review — not approved" |
| Ready for **formal submission**? | **NO — BLOCKED** (Section 9) |

## 1. Was the thesis generated?

**Yes.**
- `final_five_chapters/REM_THESIS_5CH_FINAL.docx` (editable) and `REM_THESIS_5CH_FINAL.pdf`: 237 A4 pages. The preliminary pages run i–xxii; Chapters 1–5 and the References run 1–215.
- `chapters/CHAPTER1…5*.docx`: five separate chapter files.
- Source text: `final_five_chapters/src/*.md`.
- Build tools: `tools/make_5ch.py`, `figures_5ch.py`, `build_5ch.py`, `check_5ch.py`, `qa_5ch.py`, `tables_5ch.py`, `source_map_5ch.py`.

The R5 thesis (`chapters_R5/`, `R5/`) was read and **not modified** (`git diff` on those paths is empty).

## 2. Was the live experiment executed?

**No.** No episode with a language model was run, and no live result exists anywhere in the thesis or the repository.

What exists:
- the implemented closed-loop harness (`rem/integration/agentdojo_live.py`);
- the fail-closed runner and the analysis code (`experiments/live/`);
- 12 integration tests;
- a scripted-agent smoke run of 480 episodes with 0 errors. This run is a harness check, not a result.

Blockers:
1. There is no LLM credential in the environment.
2. The design inputs of D-15 are undecided: backbone, decoding, repeats, frozen-parameter source, cells, budget, authorisation and pre-registration.

The exact commands are in `EXPERIMENT_STATUS.md` §4 and `appendices/LIVE_AGENTDOJO_DETAILS.md` §6.

## 3. Which tests passed?

**217 / 217** passed on 3 Nov 2026, re-run after the final build:
- the 205 tests of the pre-live suite;
- the 12 live-integration tests.

The live-integration tests cover:
- allow execution;
- blocked calls not executed;
- Modify semantics (step-level and episode-level);
- Escalate bounds;
- multiple calls per turn;
- tool-result IDs;
- retry and replanning;
- no label leakage;
- no episode-state contamination;
- audit-based adaptation statistics;
- metrics on synthetic records;
- the fail-closed runner.

Logs are in `experiment_results/`.

## 4. Which results were reproduced?

All recorded-trace analyses of Chapter 4 (E0, E1, E2/E5/E6, E3/A2, E4, the replay, r_mod and the user_task_15 sensitivity) were re-executed from a clean state. They showed **0 analytical differences** (`verification/reproduction_comparison_R4.json`).

This is a re-execution by this project, **not an external or independent replication**. The thesis wording was corrected accordingly in six places (THESIS_SOURCE_MAP.md).

## 5. Which conclusions are justified?

The following conclusions are justified **as exploratory evidence** from one benchmark (AgentDojo banking), recorded traces of 21 agents, and declared exploratory design values:
- tool-boundary evidence discriminates attack attempts on unseen attacker objectives (ROC-AUC 0.938);
- no calibration benefit was observed;
- the behavioral features were not attack-specific in this benchmark;
- tier-indexed expected-loss verdicts intervene more than a same-estimator baseline, at a utility cost;
- in a **non-adaptive replay**, REM's attack success rate was lower than the baseline's (0.004 vs 0.055), with a 18–20-point utility cost without a reviewer.

The following are **not justified and not claimed**:
- protection of live or adaptive agents;
- superiority over published defences;
- a new algorithm;
- operational readiness.

The thesis itself states that the central practical claim remains unestablished (§5.4). Details are in `SCIENTIFIC_CLAIM_AUDIT.md`.

## 6. Formatting: verified versus inferred

**Verified** (by tooling and visual inspection):
- A4 page size;
- no text in the outer right margin;
- no blank pages;
- Roman page numbers, then Arabic page numbers from Chapter One;
- every caption listed with its page;
- TOC, List of Tables and List of Figures populated;
- 25 native equations;
- 57 tables and 10 figures;
- no tracked changes or comments;
- valid DOCX structure in all 6 files.

**Inferred / assumed (not verified against university rules):**
- margins of 3.0 / 2.5 cm;
- Times New Roman 12 pt with 1.5 line spacing;
- heading, caption and page-number placement;
- the order of the preliminary pages.

The layout reference `enas-thesis_2026 (1).pdf` and the university's formatting guide were **not available**. In the PDF, Times New Roman is rendered as Liberation Serif. Details are in `FORMATTING_AUDIT.md`.

## 7. Which decisions need the supervisor?

**CRITICAL:**
- PILOT-AUTH;
- SD-FREEZE;
- D-9 (costs and tiers);
- D-6 (labels and the human audit);
- D-15 (the live experiment, or the decision to submit without it);
- D-1 (replay);
- D-2 (mitigation semantics).

**Also open:**
- D-10 (research questions);
- D-12 (title);
- the MAJOR and MINOR register items.

**New items:**
- N-1: the supervisor/co-supervisor roles conflict with earlier drafts;
- N-2: faculty, department and degree are unverified;
- N-3: the Arabic abstract and the Arabic spellings of the names;
- N-4: the five-chapter structure needs acknowledgement;
- N-5: the placement of sections across chapters;
- N-6: the co-supervisor co-authored a cited and compared paper;
- N-7: the "independent" wording, which has been corrected;
- N-8: the front-matter placeholders;
- N-9: the formatting rules.

Details are in `UNRESOLVED_SUPERVISOR_DECISIONS.md`.

## 8. Integrity checklist

| Rule | Status |
|---|---|
| No fabricated results | ✔ All 360 R5 numerical values preserved and none added. The new chart reads the committed JSON |
| No fabricated references or DOIs | ✔ The reference list is unchanged from R5 |
| No invented statistical significance | ✔ No significance test is claimed |
| No claim that an experiment ran without logs | ✔ Live: NOT EXECUTED everywhere |
| Simulated runs not called live | ✔ The smoke run is labelled a harness check |
| No claim of independent validation | ✔ Six overclaiming phrases corrected |
| No claim of new established algorithms | ✔ §1.11, §3.13, §5.4 |
| No copied thesis text | ✔ The layout reference was unavailable and no text from any other thesis was used |
| No concealed negative results | ✔ The absence of a calibration benefit, the non-specific behavioral features, the utility cost and the label issues are all retained |
| R5 not overwritten | ✔ |
| No fictitious approvals or signatures | ✔ Placeholders only; nothing signed |
| No unverified margin/font claims | ✔ Stated as assumed |
| Five layers and chosen algorithms preserved; CUSUM observe-only; attribution audit-only | ✔ |

## 9. Why formal submission remains blocked

1. The supervisor decisions in Section 7 are open, including PILOT-AUTH, SD-FREEZE, D-9, D-6 and D-15.
2. The live closed-loop experiment has not been run, and no supervisor decision yet accepts an exploratory-only thesis.
3. There is no human label audit.
4. The front matter is incomplete: committee page, signed declaration (including any AI-use declaration), dedication and acknowledgement.
5. The official metadata is unverified: supervisor roles, faculty, department, degree and title (N-1, N-2, D-12).
6. The formatting has not been checked against the university's rules. The PDF must be re-exported with Times New Roman.
7. References: no full texts were read; there are 21 PARTIAL entries; the Platt year (D-13) and Kull are unresolved.
8. The "Status of This Draft" page must be removed from a submission version.
