# Thesis Supervisor Full Evaluation

**Thesis:** *Runtime Evaluation and Mitigation (REM): A Security Framework for Financial AI Agents*

**Version evaluated:** R4, repository `rms756/ram`, branch `claude/rem-r4-corrections-3ktvze`, commit `9ab3f9ed24600f1eb45d4eef8790268a8f18c55d` (1 Nov 2026)

**Date of evaluation:** 1 November 2026

**Recommendation:** **C, MAJOR REVISIONS REQUIRED.** The thesis is not ready for submission or defence in its current form. Estimated grade ≈ 59/100. This is not an official grade.

---

## 1. Conflict of interest and independence

The thesis text (R1–R4), the code, the experiments and the earlier verification reports were all produced in sessions of the **same AI assistant** that wrote this evaluation. All 47 commits in the repository are authored by "Claude".

This evaluation is therefore **not independent**. It has tried to be adversarial:
- every criticism is tied to a file and line, or to a command that was run;
- verified findings (V) are separated from disclosures by the thesis itself (D) and from concerns (C).

Nevertheless, **an independent human examination is required** before any academic decision.

## 2. Evidence inventory

### 2.1 Choosing the authoritative version

| Branch | Head | Content | Role in this evaluation |
|---|---|---|---|
| `claude/rem-r4-corrections-3ktvze` | `9ab3f9e` | R4 chapters, DOCX/PDF, R4 result set, correction log | **Evaluated.** It is the latest revision, made on the user's instruction to correct R3, and its readiness report targets supervisor review |
| `claude/rem-algorithm-implementation-3ktvze` | `181a38c` | R3 (30 Oct) | Baseline only; not merged with R4 |
| `claude/rem-thesis-revision-r2-j1px4f`, `claude/rem-thesis-lit-review-merge-j1px4f` | remote only | R2 / literature-review generations | Historical; not evaluated |

The R4 sources were not treated as authoritative because of their timestamp. They were treated as authoritative because:
- R4 is the explicit correction of the reviewed R3;
- the R4 correction log maps every R3 review finding to a change.

The design authority follows the CLAUDE.md order:
1. supervisor decisions (`SUPERVISOR_DECISIONS_REQUIRED.md`, which lists most items as still open);
2. the Stage 2 report;
3. the proposal, which is **absent**.

### 2.2 Files inspected (read in full unless noted)

| File | sha256 (12 characters) | Last commit | Words |
|---|---|---|---:|
| `REM_FINAL_THESIS/chapters_R4/FRONT_MATTER_R4.md` | e11bf52a38bf | 4e44e24 | 935 |
| `…/CHAPTER1_INTRODUCTION_R4.md` | b642284cede4 | 6fc0952 | 2,585 |
| `…/CHAPTER2_LITERATURE_REVIEW_R4.md` | 77dddfdcca0c | 6fc0952 | 21,892 |
| `…/CHAPTER3_METHODOLOGY_R4.md` | 11576259ecc8 | 6fc0952 | 13,394 |
| `…/CHAPTER4_IMPLEMENTATION_R4.md` | 26bf79a4a0e1 | 4e44e24 | 4,178 |
| `…/CHAPTER5_RESULTS_R4.md` | f50b10ddac2b | 4e44e24 | 5,450 |
| `…/CHAPTER6_DISCUSSION_CONCLUSION_R4.md` | b54b37002b41 | 4e44e24 | 2,492 |
| `…/REFERENCES_R4.md` (113 entries) | d0a634b1ccf1 | 6fc0952 | 3,737 |
| `REM_FINAL_THESIS/R4/REM_THESIS_R4.docx` | 6c57d9945b29 | 4e44e24 | — (structure checked; the text is built from the Markdown above) |
| `REM_FINAL_THESIS/R4/REM_THESIS_R4.pdf` (212 pages) | b4281ff3b2d8 | 4e44e24 | — (page count and build checked; content not re-read page by page) |
| `CLAUDE.md` | 6fef971e0d75 | 1c18cdf | 1,048 |
| `STAGE2_FINAL_ALGORITHM_MATHEMATICAL_DECISION_REPORT.md` | f528f0418887 | f46c126 | 10,326 |
| `SUPERVISOR_DECISIONS_REQUIRED.md` | 72203d3772af | b28d498 | 2,219 |
| `REM_FINAL_THESIS/REFERENCES_VERIFIED.md`, `reports/SOURCE_VERIFICATION_LOG_R4.md`, `reports/CORRECTION_LOG_R4.md`, `reports/RESULTS_PROVENANCE_REPORT.md`, `README.md` | — | ≤ 9ab3f9e | read |
| `REM_STAGE2_INPUT_PACKAGE/PAPER_READING_PACK/PAPER_DOWNLOAD_STATUS.md` | — | — | read in part |

**Code** (`rem/`, 44 files, 6,861 lines; last change `ea621c3`).
- Read in full: `detection/ridge_logistic.py`, `calibration/logit_nll.py`, `a3.py`, `evaluation/crossfit.py`, `integration/agentdojo_replay.py` (mitigation and guard), `behavior/evidence.py` (features), `integration/steps.py` (labelling).
- The other modules were surveyed by function signature and docstring.

**Tests** (`tests/`, 19 modules; last change `4e44e24`): executed.

**Experiments** (`experiments/pilot/`; last change `ea621c3`): scripts surveyed. `configs/exploratory/pilot_e0.yaml` (`48bef90`) read for design values.

**Results:**
- `results/pilot_R2/` (`0f45527`): the JSON files cited by Ch. 5 were read.
- `results/pilot_R4/` (`6fc0952`): provenance and timing were read.
- The R4 re-run state (`repro_R4c/state/crossfit.pkl`, `data.steps`) was used for the independent recomputation. It is the output of the R4 re-execution in the session scratchpad, **not committed** to the repository. Its committed counterparts are the JSON files in `results/pilot_R4/`

**Not accessed:**
- the approved thesis proposal (absent from the repository);
- the full text of any cited paper (blocked by network policy in every session);
- any similarity or plagiarism report (none exists);
- the university's thesis regulations and template.

### 2.3 Checks executed by the evaluator (1 Nov 2026)

| Check | Result |
|---|---|
| `python -m pytest -q` | 205 passed: 199 REM tests and 6 build-tooling tests |
| `REM_FINAL_THESIS/verification/verify_equations.py` | 21 PASS lines, then ALL PASS |
| `REM_FINAL_THESIS/verification/trace_cells_R4.py` | 126 of 126 pass |
| Independent recomputation of held-out metrics: NumPy Mann–Whitney AUC, own ECE and log-loss | AUC 0.938288 (raw 0.939334), ECE 0.043761, log-loss 0.201344, **identical to the thesis** |
| Leakage review of `nested_crossfit` | None found |
| Examiner diagnostic: provenance rule, observe-only, all 6,762 steps | x_act1 rule 97.1% / 14.7% / 92 of 180, against REM 97.3% / 22.7% / 33 of 180 (Experimental Results Audit §3) |
| Crossref spot-check of 6 references | 6/6 match |
| Rough citation ↔ reference-list consistency check | No mismatch found (approximate) |
| `grep` for residual errors | §3.11.11 line 821; Ch. 5 line 190 |

The evaluator did not re-run the full pilot pipeline. Reproduction relied on the committed re-execution records and on the independent recomputation above.

## 3. Summary assessment

### 3.1 What the thesis does well

- **Honesty and traceability.** The evidence kinds are labelled (§5.1). Ch. 6 §6.1.4 states what is not supported. The central practical claim is declared "unestablished". Every number traces to a file, and the results reproduce bit-for-bit.
- **Mathematics.** The mathematics is correct, and the decision-theoretic derivations (Eqs. 3.8–3.10) are clean.
- **Evaluation protocol.** Nested grouped cross-fitting is free of leakage, and the same-estimator baseline isolates the decision layer.
- **Negative findings are reported:**
  - no calibration benefit;
  - behavioural features hurt utility;
  - 93% intervention on legitimate transfers.
- **The design lock is respected.** No forbidden component was reintroduced, and the unresolved decisions are kept visible.

### 3.2 Why it is not ready

1. **C-2: Added value not demonstrated.** The machinery is not shown to beat a parameter-free provenance rule.
2. **C-1: No live evidence.** There is no enforcing-mode evidence. Replay under NO-ADAPT makes residual ASR and r_mod ≈ 0 by construction, and step-level Modify is a Block.
3. **C-3: Labels unaudited.** The labels are proxies; 0 of 145 human audit items are done.
4. **C-4: Design values unapproved.** Costs, tiers and features are unapproved exploratory values.
5. **C-5: Formal and integrity gaps.** No name, no template and no proposal. The formal declaration of AI use is outstanding, and no similarity check has been run.
6. **Narrow, partly semantic gap; O3 not achieved.** Literature reach is limited (one index, no full texts).
7. **Residual internal contradictions:**
   - Ch. 3 line 821;
   - Ch. 5 line 190;
   - the FV codes vs the reference register;
   - AS-9 vs one run.

## 4. Deliverables of this evaluation

| File | Content |
|---|---|
| `CHAPTER_BY_CHAPTER_EVALUATION.md` | Strengths, weaknesses and status per chapter |
| `CRITICAL_MAJOR_MINOR_ISSUES.md` | Issue register: C-1 to C-5, M-1 to M-13, m-1 to m-13 |
| `ALGORITHM_MATHEMATICAL_AUDIT.md` | Equation-by-equation verdicts; algorithmic contribution |
| `CODE_IMPLEMENTATION_AUDIT.md` | Methodology → code table; classification; findings CI-1 to CI-9 |
| `EXPERIMENTAL_RESULTS_AUDIT.md` | Provenance; validity; sufficiency; minimum experiments |
| `REFERENCES_VERIFICATION_REPORT.md` | Composition; status; spot-check; R-1 to R-9; integrity |
| `NOVELTY_AND_CONTRIBUTION_ASSESSMENT.md` | Ten novelty questions; gaps; claims to weaken |
| `RESEARCH_QUESTION_TRACEABILITY_MATRIX.md` | RQ and objective chain, with status |
| `THESIS_DEFENSE_30_QUESTIONS_AND_ANSWERS.md` | 30 questions with honest model answers |
| `FINAL_ACADEMIC_GRADE_AND_RECOMMENDATION.md` | Rubric; grade; verdict; the 10 answers; the 5 critical issues |
| `PRIORITIZED_CORRECTION_PLAN.md` | Phased correction plan |

**No thesis, code, result or configuration file was modified by this evaluation.**
