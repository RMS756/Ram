# Supervisor Review Brief — 27 October 2026

For Dr. Husam Fakhouri. Two pages of what changed, what is new, and what needs a decision.

## What exists now

1. **Six-chapter thesis draft:**
   - `thesis/` holds the Markdown sources;
   - `thesis/build/` holds the per-chapter DOCX files, `REM_THESIS_FULL.docx` and `REM_THESIS_FULL.pdf`.

   Chapters 2 and 3 are reproduced unchanged. Chapter 1 has Sections 1.12–1.13 revised. Chapters 4–6 are new. The five-chapter drafts of 24 Sep are untouched.
2. **Implementation of the Chapter 3 components** (exploratory modules) with 192 passing tests.
3. **An executed exploratory pilot:**
   - real-agent AgentDojo traces;
   - 21 backbones;
   - 6,762 steps;
   - design pre-registered before any held-out prediction.

   Results: `results/pilot/`. Validity: `EXPERIMENT_VALIDITY_REPORT.md`.
4. **Audits:** `EQUATION_PROVENANCE_AUDIT.md`, `SOURCE_VERIFICATION_REPORT.md`, `RESEARCH_GAP_AND_NOVELTY_AUDIT.md`, `CLAIM_EVIDENCE_MATRIX.xlsx`, `REFERENCE_VERIFICATION_MATRIX.xlsx`.

## The five things to read first

1. **SC-7.** Enforcement results were obtained by trajectory replay, which Chapter 3 §3.1.4 excludes. Keep them as labelled sensitivity evidence, discard them, or amend the scope?
2. **The reviewer dependence.** With the pre-registered costs, REM's benign utility is 0.31 without a reviewer and 0.50 with an oracle reviewer, against 0.51 for B1. The value of Escalate needs a reviewer model.
3. **Negative results:**
   - calibration gave no measurable gain;
   - context evidence had no measurable effect;
   - behavioural evidence reduced utility.

   These bear on SD-FEAT and on the title wording ("behavior-aware").
4. **Label rule.** user_task_15 (attacker IBAN as the legitimate payee in suite v1/v1.1, fixed upstream from v1.1.1) and alternative attacker routes.
5. **Citation corrections:** Platt (1999 vs 2000 chapter title) and Kull et al. (2017, two works).

## Decisions requested (full list: `SUPERVISOR_DECISIONS_REQUIRED.md`)

- SC-1 to SC-7;
- SD-FREEZE;
- SD-STRUCT (five or six chapters);
- RQ-CONFIRM;
- SD-1 to SD-5, SD-DET, SD-FEAT;
- the reviewer model;
- the label rule;
- the title.
