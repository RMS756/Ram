# SUPERVISOR DECISIONS REQUIRED

**Date:** 24 September 2026 · **Repository state:** HEAD `c22a97d`
**Status of every item below:** UNRESOLVED. No item was resolved during the preparation of Chapters 4, 5 and 1. No chapter, specification, configuration or code was changed to anticipate any decision.

Sources:
- `CLAUDE.md`
- `REM_STAGE2_INPUT_PACKAGE/working/Chapter3_working.md` (Ch3)
- `STAGE2_FINAL_ALGORITHM_MATHEMATICAL_DECISION_REPORT.md` §22 (SD-1 to SD-5)
- `STAGE3_IMPLEMENTATION_AUDIT.md` (Decision Register — Stage 3)
- `00_CURRENT_STATE_AUDIT.md`

---

## A. Specification conflicts (Chapter 3 versus the frozen lock or the implementation)

### SC-1 — Mitigation semantics
- **Chapter 3:** Modify removes the tool class of a_t for the rest of the episode. Block restricts every tool in 𝒯_R for the rest of the episode (Table 3.14; Algorithm 1, lines 29–33; §3.8 property 1).
- **Current frozen implementation:** step-level.
  - Allow releases the current action.
  - Modify applies one declared mechanism to the current action. The mechanism is undeclared, so Modify raises `DesignNotSpecifiedError`.
  - Escalate withholds the current action.
  - Block prevents execution of the current action.
  - Source: `CLAUDE.md` § MITIGATION LOCK; `rem/core/mitigation.py`; `configs/mitigation.yaml` (`scope: step_level`); `RECONCILIATION.md` C5–C7.
- **Consequence:**
  - The restrictiveness ordering (§3.8 property 1) and the tie order of Eq. 3.7 are justified in Chapter 3 by the episode-level semantics.
  - The residual rate r_mod(k) in Eq. 3.5 is defined for the Chapter 3 Modify mechanism.
- **Status:** UNRESOLVED — SUPERVISOR DECISION REQUIRED.

### SC-2 — Tie-breaking
- **Chapter 3:** ties are resolved toward Block ⪰ Escalate ⪰ Modify ⪰ Allow (Eq. 3.7). Chapter 3 classes this as a design definition.
- **Prototype:** an exact tie raises `VerdictTieError` (`rem/algorithms/decision/expected_loss.py`; `test_exact_tie_raises_rather_than_choosing`). `configs/decision.yaml` records `tie_breaking_rule: REQUIRED_FROM_DESIGN`.
- **Status:** UNRESOLVED — SUPERVISOR DECISION REQUIRED.

### SC-3 — Calibration ablation *(identified in this audit; recorded earlier as Defect D2 / ED-4)*
- **Chapter 3 §3.11.7, ablation 4:** "Calibration removed (p̃_t used in Equation 3.6)".
- **Implementation:** the pipeline refuses `REM − Calibration` with `DesignNotSpecifiedError` (`rem/core/pipeline.py`; `test_ablating_calibration_is_refused`; `docs/EXPERIMENT_GUIDE.md` § Ablations).
- **Status:** UNRESOLVED — SUPERVISOR DECISION REQUIRED.

### SC-4 — Calibration fitting objective and protocol *(identified in this audit; recorded earlier as Defect D3 / ED-5)*
- **Chapter 3:** Eq. 3.4 is the NLL on the labels y_i, fitted on out-of-fold logits from nested grouped cross-fitting (Procedure 3.1, line 5). Source: Guo et al. (2017), status FV.
- **Implementation:** NLL against Platt's smoothed targets t₊ = (N₊+1)/(N₊+2) and t₋ = 1/(N₋+2), fitted on a single held-out split (`configs/calibration.yaml`: `target_smoothing`, `fitting_split: validation`).
- The code attributes the smoothed targets to Platt (1999), Section 2. That citation is under the unresolved conflict OI-07, and its verification code in Chapter 3 is NC.
- **Status:** UNRESOLVED — SUPERVISOR DECISION REQUIRED.

### SC-5 — Brier score *(identified in this audit)*
- **Chapter 3 §3.12.2:** "The Brier score is not reported until the convention of its original source (Brier, 1950) has been confirmed" (OI-09).
- **Implementation:** `configs/calibration.yaml` records `evaluation_metric: brier_score` with status FROZEN, and `brier_score` is implemented.
- **Status:** UNRESOLVED — SUPERVISOR DECISION REQUIRED.

### SC-6 — Component-to-layer mapping *(identified in this audit)*
- **Chapter 3:**
  - L2 Detection = injection-classifier score and instruction-pattern indicator.
  - L3 = history, behavioral and action features.
  - L4 = estimation, calibration, tier, predicates, verdict, audit (§3.2.1, Table 3.5, §3.5–3.7).
- **Implementation:**
  - Ridge logistic regression is labeled "L2 Detection".
  - Calibration is labeled "cross-cutting".
  - The L1 `ContextProcessor` produces the whole evidence vector.
  - Source: `rem/core/pipeline.py` comments and `Layer` constants.
- **Consequence:** the five-layer count and the pipeline order agree. The assignment of components to layers does not.
- **Status:** UNRESOLVED — SUPERVISOR DECISION REQUIRED (confirmation of the mapping the thesis reports).

## B. Scope and structure decisions

### SD-FREEZE — Status of the Chapter 3 specifications
- Chapter 3 (22 September 2026) specifies items that `CLAUDE.md` lists as unresolved "unless explicitly frozen":
  - the provenance rule;
  - the feature set (Tables 3.8–3.9);
  - predicates D1/D2;
  - the tool-restriction Modify mechanism;
  - the grouping scheme;
  - label construction;
  - λ selection.
- Under the `CLAUDE.md` source-of-truth order, a chapter ranks below the Stage 2 report and the reconciled specification. No record shows that these Chapter 3 items were frozen.
- **Decision needed:** whether the Chapter 3 specifications (other than SC-1 to SC-6) are approved as the frozen specification that the implementation must follow.
- **Status:** UNRESOLVED — SUPERVISOR DECISION REQUIRED.

### SD-STRUCT — Thesis chapter structure *(identified in this audit)*
- **Chapter 3 assumes six chapters:**
  - Table 3.1 places Demonstration in Chapter 4, Evaluation in "Sections 3.11–3.12; Chapter 5", and Communication in "Chapter 6";
  - AS-1 is "to be demonstrated … (Chapter 4)";
  - §3.16 ends "Chapter 4 describes the implementation".
- **Requested structure:** Chapter 4 = Implementation, Experimental Design, and Results; Chapter 5 = Discussion, Conclusions, Limitations, and Future Work.
- The new chapters follow the requested structure. Chapter 3 was not changed. If the five-chapter structure is confirmed, the Chapter 3 cross-references need an authorized correction.
- **Status:** UNRESOLVED — SUPERVISOR DECISION REQUIRED.

### RQ-CONFIRM — Research questions
- Chapter 3 §3.1.3: "The approved proposal does not state research questions. The following questions are derived from the objectives and are presented for supervisor confirmation."
- RQ1–RQ4 remain [PD].
- **Status:** UNRESOLVED — SUPERVISOR DECISION REQUIRED.

### SD-5 — Project scope confirmation (Stage 2 register)
- Financial (banking) scope. Chapter 3 §3.1.2 restricts the evaluation to a banking environment. O1 names "financial AI agents' and task automation agents'" security, and task-automation environments are "outside the evaluation scope unless approved as an extension".
- **Status:** UNRESOLVED per records.

### TITLE — Thesis title
- Three different wordings appear in the project records (`README.md` line 1; `STAGE2_FINAL_…` line 3; `stage1_audits/10_MASTER_AUDIT_REPORT.md` line 3). No approved title is on record.
- **Status:** UNRESOLVED.

## C. Design values pending approval (named in Chapter 3 or listed as unresolved in `CLAUDE.md`)

| ID | Item | Chapter 3 location | Config parameter |
|---|---|---|---|
| SD-1 | Loss values C_miss(k), C_FA(k), C_mod(k), C_esc and the loss grid | Table 3.13; §3.12.3 | `decision.loss_grid` |
| SD-2 | Consequence tier map κ and amount limits | Table 3.11 ("policy pending supervisor approval") | `decision.consequence_tiers` |
| SD-3 | Modify mechanism | Table 3.14 (tool restriction), subject to SC-1 | `mitigation.modify_mechanism` |
| SD-4 | Policy predicates: Π, k_D2, required evidence per tier | §3.7.4 | `decision.policy_predicates` |
| SD-DET | Injection classifier | Table 3.8 ("classifier choice pending supervisor approval") | `detection.injection_classifier` |
| SD-FEAT | Final feature set (frozen after pilot E0) | Tables 3.8–3.9; §3.6.2 rule 3 | `detection.feature_set`, `behavior.behavioral_evidence_features` |
| — | Instruction-pattern set, privilege map, n_max, benign transition set | §3.5, Table 3.9 | none |
| — | Labeling of attacker-induced read steps | §3.11.3 ("pending supervisor decision") | `detection.attacker_induced_read_labeling` |
| — | LLM backbones and attack templates | §3.11.1 | `experiment.llm_backbones` |
| — | AgentDojo version or commit (OI-14) | §3.11.2 | `experiment.agentdojo_version`, `experiment.dataset` |
| — | Number of repeated runs ("at least three … pending supervisor approval") | §3.11.9 | `experiment.number_of_repeats` |
| — | Grouping sensitivity analysis by user task | §3.11.5 | `experiment.grouping_scheme` |
| — | Baseline B2 (detection-only) and distributed defenses | §3.11.7 | `experiment.external_benchmarks` |
| — | False-positive targets α_blk and α_mod | §3.7.7 | none |
| — | Pilot E0 decision values | §3.11.8 | none |
| — | Optional CUSUM analysis and its indicator set | §3.11.10 | `behavior.optional_cusum_scenarios` |
| — | Ridge penalty λ (Chapter 3 specifies selection by grouped CV; no value exists) | §3.7.1, §3.9 | `detection.ridge_penalty_lambda` |
| — | Train/validation/test proportions (Chapter 3 replaces fixed splits with grouped cross-fitting) | §3.11.4–3.11.5 | `experiment.splits` |
| — | Attribution background mean x̄ (estimated on benign fitting data) | §3.7.6 | `attribution.background_mean` |

## D. Earlier register items carried forward without change

| ID | Item | Record | Present position |
|---|---|---|---|
| Conflict 1 | Beta calibration | `STAGE3_IMPLEMENTATION_AUDIT.md` | Chapter 3 does not adopt beta calibration; `CLAUDE.md` forbids it as the adopted calibrator. No change proposed. |
| Conflict 2 | CUSUM as an evidence feature | `STAGE3_IMPLEMENTATION_AUDIT.md` | Chapter 3 and `CLAUDE.md` both treat CUSUM as optional and observe-only. No record of a supervisor decision exists. Not reopened here. |
| Conflict 3 | SHAP status | `STAGE3_IMPLEMENTATION_AUDIT.md` | Chapter 3 and `CLAUDE.md` both treat linear attribution as audit-only. |
| RG-1 | Authoritative equation registry | `README.md`; `RECONCILIATION.md` | Missing. |
