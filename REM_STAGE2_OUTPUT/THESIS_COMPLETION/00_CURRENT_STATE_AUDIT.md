# CURRENT STATE AUDIT — REM Thesis, before Chapters 4, 5 and 1

**Date:** 24 September 2026
**Repository state audited:** branch `claude/rem-algorithm-implementation-3ktvze`, HEAD `c22a97d`, clean tree
**Scope:** Phase A of the Chapter 4 → 5 → 1 completion task. Read-only. No existing artifact was modified.

Evidence files referred to as E0–E6 are in `evidence/` next to this file.

---

## 1. What exists

| Item | Location | State |
|---|---|---|
| Chapter 1 (Introduction) | none | **Does not exist in any format.** A filesystem-wide search for chapter, introduction and proposal files found only the Chapter 2 and Chapter 3 Stage 1 DOCX files and the working Markdown files. |
| Chapter 2 (Literature Review) | `REM_STAGE2_INPUT_PACKAGE/working/Chapter2_working.md` | Present. Read in full. 47 references. |
| Chapter 3 (Methodology and REM design) | `REM_STAGE2_INPUT_PACKAGE/working/Chapter3_working.md` | Present. Read in full (1,057 lines). 37 references. SHA-256 prefix `5085e11732dee82f`, unchanged since Stage 2. |
| Design lock | `CLAUDE.md` | Present. Governs the implementation. |
| Approved thesis proposal | none | **Missing.** Chapter 3 §3.1.2 quotes the approved objectives O1–O3. That quotation is the only record of the approved objectives. |
| Decision ledger | none | **Missing.** Recorded as missing in `STAGE2_FINAL_ALGORITHM_MATHEMATICAL_DECISION_REPORT.md` §1 (row 11) and `REM_AUDIT_OUTPUT/00_WORKSPACE_INVENTORY.md`. Decision registers exist inside `STAGE2_FINAL_…` §22 (SD-1 to SD-5) and `STAGE3_IMPLEMENTATION_AUDIT.md` (Decision Register — Stage 3). |
| Authoritative equation registry | none | **Missing.** Every implemented operation is marked `AWAITING REGISTRY ID` (E6; `docs/MATHEMATICAL_TRACEABILITY.md`). |
| Algorithm-selection and mathematical documents | `STAGE2_FINAL_ALGORITHM_MATHEMATICAL_DECISION_REPORT.md`, `STAGE2_EQUATION_TO_SOURCE_TRACEABILITY.md`, `STAGE3_*`, `STAGE2_5_*`, `V1_NEXUS_DIRECT_VERIFICATION.md`, `RECONCILIATION.md` | Present. These records are dated 19–21 September 2026, before the current Chapter 3 (22 September 2026). |
| Reference verification records | `REM_STAGE2_INPUT_PACKAGE/stage1_audits/*.xlsx`, `REM_STAGE2_OUTPUT/STAGE2_*.xlsx`, `THESIS_READING_INDEX.md`, `PAPER_READING_PACK/` | Present. 58 unique references across Chapters 2 and 3. |
| Chapter 3 technical summary | `REM_STAGE2_OUTPUT/CHAPTER3_TECHNICAL_SUMMARY_FOR_SUPERVISOR.{md,docx}` | Present. |
| Implementation | `rem/`, `configs/`, `experiments/`, `scripts/`, `tests/` | Present. Package `rem-framework` 0.2.0. |
| Experiment outputs, datasets, logs | `data/` (empty); no `experiments/results/` directory in git | **None exist.** No run of REM on any agent, benchmark or dataset has been recorded. |

## 2. What is verified

| Claim | Evidence | Status |
|---|---|---|
| 154 tests are collected and all pass | E1 (`154 passed in 0.47s`), E2 (`154 tests collected`) | Verified on HEAD `c22a97d`, Python 3.11.15, NumPy 2.4.6, PyYAML 6.0.1, pytest 9.1.1 (E5) |
| Per-file test counts: 43 frozen-math, 25 metrics, 21 pipeline, 20 contract-compliance, 15 config, 12 trajectory, 9 reproducibility, 9 mitigation | E2; `STAGE2_5_BASELINE_TEST_RECONCILIATION.md` §3 | Verified. The historical figure of 139 contract-compliance tests was incorrect; the verified figure is 20. |
| The configuration declares 27 FROZEN and 19 unresolved parameters | E3 (`readiness.json`, dry-run stdout) | Verified |
| All seven pipeline components are unattached in the experiment runner | E3, E4 | Verified |
| A full (non-dry) run stops with `DESIGN BLOCKED`, exit code 1 | E4 | Verified. This is the designed fail-closed behavior. |
| 19 mathematical operations carry a citation. None carries an equation ID. | E6; `docs/MATHEMATICAL_TRACEABILITY.md` | Verified |
| The `context` and `behavior` algorithm packages contain only `__init__.py` | E6 | Verified |
| AgentDojo is not installed in the environment | E5 (`ModuleNotFoundError`) | Verified |

## 3. What is implemented

Chapter 3 is the technical source. Each Chapter 3 element is classified by what the code at HEAD `c22a97d` contains.

### 3.1 Implemented and consistent with Chapter 3

| Chapter 3 element | Code | Notes |
|---|---|---|
| Five layers; no sixth layer; no feedback layer | `rem/core/pipeline.py` (`Layer.FROZEN_LAYERS`), `tests/test_contract_compliance.py` | Test-enforced |
| Logit and uncalibrated probability (Eq. 3.1) | `rem/algorithms/detection/ridge_logistic.py` | Test-verified against hand-computed values |
| Ridge-penalized fit (Eq. 3.2), intercept unpenalized | same file; Newton–Raphson | The penalty is written as (λ/2)‖β‖², where Eq. 3.2 has λ‖β‖². Chapter 3 §3.7.1 states that rescaling the penalty changes only the selected λ. λ has no default and fitting raises without it. |
| Calibration on the logit (Eq. 3.3), γ₁ > 0 enforced | `rem/algorithms/calibration/platt.py` | A fitted γ₁ ≤ 0 raises `MonotonicityViolationError` |
| Conditional risk (Eq. 3.6) and argmin verdict (Eq. 3.7, without the tie order) | `rem/algorithms/decision/expected_loss.py` | The full risk table is recorded |
| Linear attribution (Eq. 3.11) with base value β₀ + βᵀx̄; completeness (Eq. 3.12) | `rem/algorithms/attribution/linear_shapley.py` | Audit-only; the decision engine rejects attribution input |
| Audit record per step (JSON Lines, digests by default) | `rem/core/audit.py` | The field set is partly different from §3.7.6 (see §3.3) |
| Causal evaluation (step t uses only the prefix before t) | `rem/agent/trajectory.py` (`prefix`) | Test-enforced |
| Fail-closed behavior on every unresolved input | `rem/core/interfaces.py`, `rem/config/loader.py` | Test-enforced |
| Reproducibility manifest (seed, config digests, `CLAUDE.md` digest, dependencies, git state) | `rem/utils/reproducibility.py` | Test-enforced |

### 3.2 Implemented differently from Chapter 3 (specification conflicts)

| ID | Chapter 3 | Implementation | Status |
|---|---|---|---|
| SC-1 | Modify removes the tool class for the rest of the episode. Block restricts every tool in 𝒯_R for the rest of the episode (Table 3.14; Algorithm 1, lines 29–33). | Step-level only (`rem/core/mitigation.py`). This follows the `CLAUDE.md` Mitigation Lock. | **SUPERVISOR DECISION REQUIRED** |
| SC-2 | Ties are resolved toward Block ⪰ Escalate ⪰ Modify ⪰ Allow (Eq. 3.7). | An exact tie raises `VerdictTieError`. | **SUPERVISOR DECISION REQUIRED** |
| SC-3 | Ablation 4: "Calibration removed (p̃_t used in Equation 3.6)" (§3.11.7). | The pipeline refuses `REM − Calibration` with `DesignNotSpecifiedError` (`test_ablating_calibration_is_refused`). Recorded earlier as Defect D2 / ED-4. | **SUPERVISOR DECISION REQUIRED** |
| SC-4 | Calibration parameters are fitted by NLL on the labels y_i, using out-of-fold logits from nested grouped cross-fitting (Eq. 3.4; Procedure 3.1). | Fitted with Platt's smoothed targets t₊ = (N₊+1)/(N₊+2) and t₋ = 1/(N₋+2), on one held-out split supplied by the caller. The source attribution for the smoothed targets rests on the Platt citation, which is under conflict OI-07. Recorded earlier as Defect D3 / ED-5. | **SUPERVISOR DECISION REQUIRED** |
| SC-5 | The Brier score is not reported until its source convention is confirmed (§3.12.2; OI-09). | `configs/calibration.yaml` marks `evaluation_metric: brier_score` as FROZEN, and `brier_score` is implemented. | **SUPERVISOR DECISION REQUIRED** |
| SC-6 | Estimation, calibration, tiering, predicates and verdict belong to the Decision Engine (L4). The Detection Layer (L2) holds the injection classifier and the instruction-pattern indicator (§3.2, §3.5, §3.7). | Code comments label ridge logistic regression as "L2 Detection" and calibration as "cross-cutting". The L1 `ContextProcessor` produces the whole evidence vector. | **SUPERVISOR DECISION REQUIRED**. This is a documentation and layer-mapping conflict; the computation order is the same. |

### 3.3 Specified in Chapter 3 but not implemented (IMPLEMENTATION NOT CONFIRMED)

Provenance labeling rule (§3.4.2); invisible-character removal (§3.4.1); entity extraction (§3.4.3); context features x^ctx₁–x^ctx₂ and the injection classifier (Table 3.8); behavioral and action features x^beh₁–x^beh₄ and x^act₁–x^act₃ (Table 3.9); consequence descriptors and tier map κ (Tables 3.10–3.11); predicates D1 and D2 (§3.7.4); feasible verdict set 𝒱(a_t) (the code always minimizes over all four verdicts); the loss structure of Table 3.13 and Eq. 3.5; the dominance check (§3.7.5); group attribution Φ_J (Eq. 3.13); the consequence-independent baseline and Eq. 3.14; the offline fitting Procedure 3.1 (nested grouped cross-fitting, λ selection, out-of-fold calibration); the AgentDojo integration and the observe-only and enforcing modes (§3.11.1); label construction (§3.11.3); pilot E0; bootstrap intervals; optional CUSUM (Eqs. 3.15–3.19); metrics ASR, benign utility, utility under attack, intervention rates, residual ASR, escalation rate, ROC-AUC, PR-AUC, ECE (Eq. 3.20), log-loss (Eq. 3.21) and realized loss (Eq. 3.22); the human-reviewer workflow for Escalate; the audit-record fields "verdict source (D1/D2/expected loss)" and "group sums Φ". Evidence: E6.

### 3.4 Implemented but not specified in Chapter 3

Precision, recall, F1, FPR, FNR, accuracy, the Brier score, mean and quantile latency, and throughput (`rem/evaluation/`). The code cites four sources that do not appear in the Chapter 2 or Chapter 3 reference lists and have no project verification record: Hastie, Tibshirani & Friedman (2009); van Rijsbergen (1979); Hyndman & Fan (1996); Shapley (1953). Status: **SOURCE VERIFICATION REQUIRED**.

## 4. What is experimentally demonstrated

**Nothing about security effectiveness, utility, calibration quality, decision quality or latency has been experimentally demonstrated.** No agent has been run with REM. No benchmark trace exists. No metric has been computed on data.

What exists is software-verification evidence:
- 154 unit and integration tests pass. The pipeline tests run on fixture features, fixture loss grids and fixture tiers that the test file declares are "not REM design values".
- A readiness dry-run shows that REM refuses to run with unresolved design inputs.

This evidence shows properties of the code. It does not show that REM protects an agent.

## 5. What remains unresolved

1. **Supervisor decisions.** SC-1 to SC-6 above, plus the items in `SUPERVISOR_DECISIONS_REQUIRED.md`, including:
   - thesis chapter structure (SD-STRUCT);
   - approval of Chapter 3's specifications as the frozen specification (SD-FREEZE);
   - RQ1–RQ4 confirmation;
   - SD-1 to SD-5;
   - the Chapter 3 items marked "pending supervisor approval".
2. **Design parameters.** The 19 unresolved configuration parameters (E3).
3. **Evidence issues.** OI-01 to OI-07, OI-09 to OI-14, and CF-01 to CF-09 (`THESIS_READING_INDEX.md` §6; `CHAPTER3_TECHNICAL_SUMMARY_FOR_SUPERVISOR.md` Table 75).
4. **Equations with incomplete source verification.** 3.1, 3.2, 3.3, 3.9, 3.10, 3.15 and 3.16.
5. **Missing records.** Approved proposal, decision ledger, equation registry.
6. **Thesis title.** Not confirmed; three different wordings appear in project records:
   - `README.md` line 1;
   - `STAGE2_FINAL_…` line 3;
   - `stage1_audits/10_MASTER_AUDIT_REPORT.md` line 3.

## 6. Consequence for the chapter work

- **Chapter 4** can document the implemented prototype, the experimental design specified in Chapter 3 (as PLANNED — NOT EXECUTED), the software-verification evidence, and the missing results (RESULT NOT AVAILABLE). It cannot report any empirical security, utility, calibration or latency result.
- **Chapter 5** can interpret only that evidence. It must state that objectives O2 and O3 and questions RQ1–RQ4 have not been answered empirically.
- **Chapter 1** can be written from Chapters 2 and 3 and from the evidence status established in Chapters 4 and 5.

None of these gaps makes a technically valid continuation impossible, so the chapter work proceeds. Every gap is labeled in the chapters.
