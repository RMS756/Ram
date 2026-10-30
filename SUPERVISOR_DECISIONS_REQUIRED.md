# SUPERVISOR DECISIONS REQUIRED — consolidated register

**Updated:** 27 October 2026. This file carries forward, unchanged, every item of
`REM_STAGE2_OUTPUT/THESIS_COMPLETION/SUPERVISOR_DECISIONS_REQUIRED.md` (24 Sep 2026; Sections A–D below). It adds the
items raised by the master prompt and by the exploratory pilot (Section E). No item has been resolved. No item is
anticipated in code, configuration or Chapter 3. The exploratory pilot runs both sides of open choices where that was
possible, and reports the results as evidence for the decision, not as the decision itself.


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


## E. Items added on 27 October 2026

### SC-7 — Recorded-trace replay versus the Chapter 3 scope *(new; conflict)*
- **Specification:** Chapter 3 §3.1.4 lists, as out of scope: "Counterfactual estimation of intervention value by replaying agent trajectories."
- **What was done:**
  - Live enforcing-mode runs (§3.11.1) are BLOCKED, because no LLM API is available.
  - Enforcement metrics (ASR, utility, residual ASR) and r_mod(k) were estimated by replaying recorded AgentDojo agent trajectories under REM, assuming the agent does not adapt (NO-ADAPT). This is the method §3.1.4 excludes.
- **Consequence:**
  - Every replay-derived number is outside the approved scope.
  - Observe-only verdicts use r_mod from replay through Eq. 3.5.
- **Options:**
  - (a) discard the replay results;
  - (b) report them only as an out-of-scope exploratory sensitivity analysis;
  - (c) amend §3.1.4.
- **Status:** UNRESOLVED — SUPERVISOR DECISION REQUIRED. `EXPERIMENT_VALIDITY_REPORT.md` §0.

### PILOT-AUTH — Status of the exploratory pilot
- The pilot uses the Chapter 3 values together with declared exploratory values (`configs/exploratory/pilot_e0.yaml`, committed before any run). Its results are labelled EXPLORATORY.
- **Decision needed:** whether any pilot result may appear in the thesis, and with what label. Chapter 5 of the six-chapter draft presents them as exploratory evidence only.
- **Status:** UNRESOLVED.

### AM-1 to AM-4 — Pilot amendments recorded before held-out predictions
- **AM-1:** the (user_task_15, injection_task_4) pair is excluded, because the user's own payee is the attacker IBAN.
- **AM-2:** the benign transition set comes from episodes without injection; B1 thresholds use the y = 0 steps.
- **AM-3:** "tool class" means the Table 3.7 category ∩ 𝒯_R. Step-level Modify withholds the call with a notice.
- **AM-4:** enforcement metrics use only episodes whose all-Allow replay reproduces the record.
- **Status:** each awaits approval. Source: `configs/exploratory/pilot_e0_amendments.yaml`.

### LABEL-UT15 — Post-hoc label ambiguity *(found after results)*
- user_task_15 places the attacker IBAN in the user's objective in suite versions v1 and v1.1. The benchmark fixed this from v1.1.1; 16 of the 21 recorded backbones predate the fix.
- 29 positive steps in its episodes are therefore ambiguous; 19 of them occur without injected content in context.
- A disclosed post-hoc sensitivity analysis (excluding user_task_15) is reported. The primary analysis keeps the pre-registered rule.
- **Decision needed:** exclude user_task_15 from the evaluation, redefine the label rule, or keep it as is.
- **Status:** UNRESOLVED.

### LABEL-ROUTE — Reference-match rule misses alternative attacker routes
- Example: an attacker-directed `schedule_transaction` or `send_money` under injection_task_4, whose reference tool is `update_scheduled_transaction`.
- **Decision needed:** keep strict reference matching, or label any state-changing call carrying the attacker's key argument.
- **Status:** UNRESOLVED.

### REVIEWER — Escalation resolution model
- Pilot outcomes depend on how escalations are resolved:
  - benign utility is 0.314 with no reviewer;
  - it is 0.497 with the idealized oracle reviewer.
- Chapter 3 reports both bounds.
- **Decision needed:** whether a realistic reviewer model (error rate, latency) should be specified, or the two bounds kept.
- **Status:** UNRESOLVED.

### SD-FEAT (update) — Feature-group retention after Pilot E0
- All three groups passed the pre-registered E0 rule (fitting-portion ROC-AUC ≥ 0.55; context 0.58).
- In the held-out ablations:
  - removing context evidence changed nothing measurable;
  - removing behavioural evidence *raised* benign utility by 10.5 points at equal ASR.
- **Decision needed:** whether the frozen feature set retains these groups.
- **Status:** UNRESOLVED.

### M1 — Ridge penalty constant
- Code: NLL + (λ/2)‖β‖². Chapter 3 Eq. 3.2: λ‖β‖².
- **Decision needed:** align one of the two. The values are equivalent under rescaling.
- **Status:** UNRESOLVED.

### GRID-ALPHA — Pre-registered grid inconsistency
- The E6 grid contains α_blk = 0.05 while α_mod = 0.05. Chapter 3 requires α_mod > α_blk, so that cell is reported as not evaluable.
- **Status:** UNRESOLVED.

### A2-Q1 — CUSUM post-change rate
- With q₁ = 0.3 the CUSUM is undefined, because the estimated q₀ ≈ 0.34 exceeds q₁. With q₁ ∈ {0.5, 0.7}, the held-out benign false-alarm rate is 0.106 against the 0.05 target.
- **Decision needed:** keep A2 optional, revise the indicator set, or drop it.
- **Status:** UNRESOLVED.

### A2-ENFORCE and A3+A2 — Master-prompt items
- An A2-driven enforcement policy and a retrained A3+A2 variant are named in the master prompt. Both conflict with `CLAUDE.md` ("CUSUM MUST NOT enter the core verdict path") and are not implemented.
- **Status:** SUPERVISOR DECISION REQUIRED.

### SD-STRUCT (update) — Five versus six chapters
- The master prompt requests six chapters, which is consistent with Chapter 3 Table 3.1. The 24 Sep drafts use five.
- Both exist: `REM_STAGE2_OUTPUT/THESIS_COMPLETION/` (five chapters, unchanged) and `thesis/` (six chapters, new).
- **Status:** UNRESOLVED.

### REF-PLATT and REF-KULL — Citation corrections
- **Platt:** cited as the 1999 report, but Crossref registers the 2000 chapter under a different title.
- **Kull et al. (2017):** two different 2017 works exist.
- Source: `SOURCE_VERIFICATION_REPORT.md`.
- **Status:** author decision.

### BLOCKED (not decisions; listed for completeness)
- Live LLM enforcing-mode runs (no API access).
- x_ctx1 injection classifier (model host unreachable; SD-DET).
- University thesis template (not available).
- Authoritative equation registry (RG-1).
- Repeated runs ≥ 3 (the recorded traces contain one run per configuration).
