# PROJECT AUDIT — REM Master's Thesis

**Date:** 27 October 2026
**Branch:** `claude/rem-thesis-lit-review-merge-j1px4f`. It now contains the implementation branch `claude/rem-algorithm-implementation-3ktvze`, merged in commit `5e8cf3e`; the two branches had unrelated histories and disjoint paths, and no history was rewritten.
**Auditor:** Claude Code, acting under the master prompt of 27 October 2026 and `CLAUDE.md`, the hard design lock.

**User decisions recorded on 27 October 2026, in reply to three questions:**

1. **Pushing to the public repository** `RMS756/Ram` is authorised.
2. **An exploratory pilot is authorised.** It uses the values specified in Chapter 3 (pending SD-FREEZE), together with loss-grid sweeps. Every output is stamped EXPLORATORY and is not reported as a thesis result. The frozen configuration files remain fail-closed.
3. **A1/A2/A3 are mapped to the design lock:**
   - A3 is the frozen REM pipeline and the primary method.
   - A1 is the Chapter 3 baseline B1 (same estimator, threshold policy) and serves as comparator only.
   - A2 is the observe-only CUSUM analysis and has no mitigation.
   - A2-driven enforcement and an A3+A2 retrained variant are recorded as SUPERVISOR DECISION REQUIRED.

---

## 1. Files found

| Category | Files | Status |
|---|---|---|
| Design lock | `CLAUDE.md` | Authoritative |
| Stage 2 specification | `STAGE2_FINAL_ALGORITHM_MATHEMATICAL_DECISION_REPORT.md`, `STAGE2_BLOCKED_DECISIONS.md`, `STAGE2_EQUATION_TO_SOURCE_TRACEABILITY.md`, `STAGE2_5_*` | Present |
| Stage 3 records | `STAGE3_*` (prior art, Chapter 2/3 design, implementation audit) | Present |
| Reconciliation | `RECONCILIATION.md` (FROZEN / PD / UNVERIFIED / CONFLICT per item) | Present |
| Chapter 1 | `REM_STAGE2_OUTPUT/THESIS_COMPLETION/CHAPTER1_INTRODUCTION.md/.docx` | Draft (24 Sep 2026) |
| Chapter 2 | `chapter2/CHAPTER2_SYSTEMATIC_REVIEW.md/.docx` (PRISMA SLR, 25 Sep 2026) is current. Also present: `chapter2/CHAPTER2_LITERATURE_REVIEW_INTEGRATED.*` (narrative), `REM_STAGE2_INPUT_PACKAGE/working/Chapter2_working.md`, `reference_final/08_FINAL_CHAPTER_2_STAGE1.docx` | Current version: the systematic review |
| Chapter 3 | `REM_STAGE2_INPUT_PACKAGE/working/Chapter3_working.md` (22 Sep 2026); `reference_final/09_FINAL_CHAPTER_3_STAGE1.docx`; `REM_STAGE2_OUTPUT/CHAPTER3_TECHNICAL_SUMMARY_FOR_SUPERVISOR.*` | Current methodology (contains [PD] items) |
| Chapter 4 | `REM_STAGE2_OUTPUT/THESIS_COMPLETION/CHAPTER4_IMPLEMENTATION_EXPERIMENTAL_DESIGN_RESULTS.md/.docx` | Draft. States no empirical results. |
| Chapter 5 | `REM_STAGE2_OUTPUT/THESIS_COMPLETION/CHAPTER5_DISCUSSION_CONCLUSIONS.md/.docx` | Draft. Five-chapter structure (SD-STRUCT). |
| Supervisor decisions | `REM_STAGE2_OUTPUT/THESIS_COMPLETION/SUPERVISOR_DECISIONS_REQUIRED.md`, `SUPERVISOR_BRIEF_SC1_SC6_AR.md` (Arabic) | All items unresolved |
| Reference and equation audits | `REM_STAGE2_INPUT_PACKAGE/stage1_audits/*.xlsx`; `REM_STAGE2_OUTPUT/STAGE2_03/05/06_*.xlsx`; `REM_AUDIT_OUTPUT/PRE_SEEDED_REFERENCE_REGISTER.xlsx`; `chapter2/CHAPTER2_REFERENCE_EVIDENCE_MATRIX.md` | Present |
| Paper reading pack | `REM_STAGE2_INPUT_PACKAGE/PAPER_READING_PACK/` (claim-to-paper map; no PDFs retrievable) | Present |
| Python implementation | `rem/` (about 4,500 lines): ridge logistic, Platt-on-logit, expected-loss engine, linear Shapley, deterministic mitigation, audit log, metrics, config loader, traceability registry | Frozen core implemented; unresolved items fail closed |
| Tests | `tests/` (8 files) | **154 passed**, run 27 Oct 2026 with Python 3.11.17 and pytest 9.1.1 |
| Configuration | `configs/*.yaml` (7 files) | 19 parameters unresolved by design |
| Experiment runner | `experiments/run_experiment.py --dry-run` | Runs; reports 19 unresolved parameters and 7 unattached components |
| Benchmark | AgentDojo 0.1.35 (PyPI wheel, MIT licence), installed in an isolated virtual environment. The AgentDojo GitHub repository (commit `089ed468`) is cloned read-only at `/home/user/ethz-spylab/agentdojo`. | **New this session.** It includes `runs/` with **recorded real-LLM traces** for the banking suite (30 pipeline configurations, 7,214 banking JSON files). |

## 2. Files missing

| Item | Effect |
|---|---|
| Approved research proposal | RQs remain [PD]. Objectives O1–O3 are known only as quoted in Chapter 3. |
| University thesis template (Al-Balqa Applied University) | A provisional format must be used and labelled as such. |
| `REM_Proposed_Algorithms_Verified_References_Draft.docx` (named in the master prompt) | Not found. The A1/A2/A3 descriptions in the master prompt are taken as the user's specification, reconciled with `CLAUDE.md` as recorded above. |
| Decision Ledger | The Stage 2 report lists it as MISSING. |
| Authoritative equation-ID registry | `README.md` and `RECONCILIATION.md` say it was not supplied. Every operation is marked `AWAITING_REGISTRY_ID`. |
| Previous supervisor feedback (written) | None found beyond the decision registers. |
| LLM API credentials | None available. **Live agent runs are impossible.** The recorded AgentDojo traces are used instead. |
| Full texts of most references | Not retrievable: publisher hosts are blocked by the network policy. Metadata is verifiable through Crossref. |

## 3. Status summary

| Area | Status label |
|---|---|
| Thesis overall | DRAFT — REQUIRES REVIEW. Chapters 1, 3, 4 and 5 are drafts; Chapter 2 is a systematic review; Chapter 6 does not yet exist. |
| Research methodology (Chapter 3) | DRAFT — REQUIRES REVIEW. Complete specification, but SD-FREEZE is pending. |
| Algorithm specification | COMPLETE — VERIFIED for the frozen core math (`CLAUDE.md`). Policy values: SUPERVISOR DECISION REQUIRED. |
| Implementation | IMPLEMENTED — NOT YET VALIDATED for end-to-end use. The core is tested (154 tests). Feature extraction, tiers, predicates, B1, CUSUM and benchmark adapters were absent at audit time. |
| Reference verification | Partial. Chapter 2: 71 included studies, 62 FULLY and 9 PARTIALLY VERIFIED. Foundational references: metadata verified; formulations verified only where noted in Chapter 3 Table 3.17. |
| Experiments | None executed before this session (Chapter 4 §4.12.1 states "no empirical results"). |

## 4. Mathematical inconsistencies found

| ID | Location | Inconsistency | Severity | Action |
|---|---|---|---|---|
| M1 | Ridge penalty | Chapter 3 Eq. 3.2 penalises by λ‖β‖²; the code minimises NLL + (λ/2)‖β‖² | Low. A rescaling of λ, and λ is chosen by grouped CV. | Document in `EQUATION_PROVENANCE_AUDIT.md`. Report λ in code units. |
| M2 | Platt sign convention | Master prompt: p = 1/(1+exp(A s + B)). Chapter 3 and code: p = σ(γ₁ s + γ₀) with γ₁ > 0. | None (γ₁ = −A, γ₀ = −B) | Document; tested. |
| M3 | Calibration fit (SC-4) | Chapter 3 fits NLL on labels, using out-of-fold logits. The code uses Platt's smoothed targets on a single held-out split. | Medium | Implement both; the pilot reports both; SUPERVISOR DECISION REQUIRED. |
| M4 | Feasible verdict set | Chapter 3 restricts Modify to tools in 𝒯_R. The frozen engine minimises over all four verdicts. | Medium | Add an optional feasible set (default: all four) without changing frozen behaviour. |
| M5 | Predicates | Chapter 3 defines D1/D2 semantics. The frozen engine raises whenever a predicate fires and, when a policy object is supplied, never applies the predicate. | Medium | Implement the Chapter 3 predicate policy as a separate, explicitly labelled component. |
| M6 | Tie-breaking (SC-2) | Chapter 3: Block ⪰ Escalate ⪰ Modify ⪰ Allow. Code: VerdictTieError. | Unresolved | Count ties in the pilot. Do not resolve. |
| M7 | Mitigation duration (SC-1) | Chapter 3: episode-level restrictions. Code: step-level. | Unresolved | Run both semantics as variants in the scripted sandbox. Do not resolve. |
| M8 | Brier score (SC-5) | Chapter 3 withholds it; the code implements binary MSE. | Low | Report it as exploratory, with the convention stated (binary MSE, half of Brier's original two-class sum). |
| M9 | Calibration ablation (SC-3) | Chapter 3 ablation 4 uses p̃ in Eq. 3.6; the frozen pipeline refuses it. | Medium | Run the ablation in the exploratory harness only, labelled. |
| M10 | Layer mapping (SC-6) | The code labels ridge LR "L2 Detection". Chapter 3 places estimation in L4. | Documentation | Unchanged; reported. |

## 5. Supervisor decisions still required

Every item in `REM_STAGE2_OUTPUT/THESIS_COMPLETION/SUPERVISOR_DECISIONS_REQUIRED.md` remains open:

- SC-1 to SC-6;
- SD-FREEZE, SD-STRUCT and RQ-CONFIRM;
- SD-1 to SD-5, SD-DET and SD-FEAT;
- the title.

The master prompt adds three items:

- A2 enforcement policy;
- the A3+A2 retrained variant;
- the six-chapter structure (consistent with Chapter 3's assumption; conflicts with the five-chapter request recorded as SD-STRUCT).

All of these are carried into the updated `SUPERVISOR_DECISIONS_REQUIRED.md`.

## 6. Work that can proceed independently

| Work | Basis |
|---|---|
| Equation provenance audit; verification of foundational references (Crossref metadata) | Sources accessible as metadata |
| Implementation of Chapter 3 components as **explicitly labelled exploratory** modules: provenance labeller, entity extraction, features (Tables 3.8–3.9), tier map, D1/D2, feasible set, B1 baseline (A1), CUSUM (A2, observe-only), ECE, log-loss, ROC/PR-AUC, grouped cross-fitting, bootstrap | Chapter 3 text, with user authorisation for the pilot |
| AgentDojo adapters: (a) recorded real-LLM traces, observe-only; (b) scripted ground-truth agent in the real AgentDojo sandbox, for enforcement mechanics | AgentDojo 0.1.35 and the repository runs, MIT licence |
| Exploratory pilot E0 and experiments E1–E6, labelled EXPLORATORY | User decision 2 |
| Thesis writing: Chapter 4 (implementation as built), Chapter 5 (pilot results labelled), Chapter 6, and assembly | Implementation and results |

## 7. Tasks marked BLOCKED

| Task | Status |
|---|---|
| Confirmatory (non-exploratory) thesis results | SUPERVISOR DECISION REQUIRED (SD-FREEZE, SD-1 to SD-4) |
| Live LLM agent runs in enforcing mode (true ASR under REM) | BLOCKED — MISSING DATA (no LLM API access). Recorded traces support observe-only evaluation and trace-replay bounds only. |
| Injection classifier feature x^ctx₁ (PromptGuard 2 candidate) | BLOCKED — MISSING SOURCE until model download is shown to be possible, and SUPERVISOR DECISION REQUIRED (SD-DET) |
| University template compliance | BLOCKED — MISSING SOURCE |
| Equation IDs | BLOCKED — MISSING SOURCE (registry) |
| PDF of the full thesis | Depends on available converters; to be attempted |
