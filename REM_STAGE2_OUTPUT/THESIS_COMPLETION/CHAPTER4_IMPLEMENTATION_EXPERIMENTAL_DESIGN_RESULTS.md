# CHAPTER FOUR

# IMPLEMENTATION, EXPERIMENTAL DESIGN, AND RESULTS

## 4.1 Implementation Overview

### 4.1.1 Purpose and status of this chapter

This chapter reports what has been built of the Runtime Evaluation and Mitigation (REM) framework specified in Chapter 3, what experimental design has been specified for evaluating it, and what evidence currently exists. It is written from the repository state at commit `c22a97d` (branch `claude/rem-algorithm-implementation-3ktvze`). Every statement about the implementation refers to a file in that repository. Every number refers to an evidence file (E0–E6) produced from that commit and listed in Table 4.14.

The central finding is stated first, so that no later section is read as implying more than it shows. **At the time of writing, REM has not been executed on an agent, on the AgentDojo banking environment, or on any dataset.** No attack success rate, utility, calibration, discrimination, intervention or latency result exists. What exists is:

- a Python implementation of the mathematical core of the Decision Engine and of step-level mitigation;
- a configuration layer that refuses to run while design inputs are unresolved;
- a test suite of 154 passing tests that verifies properties of the code.

The experimental design of Chapter 3 is reported here as **PLANNED — NOT EXECUTED**, and every result it would produce is reported as **RESULT NOT AVAILABLE**.

### 4.1.2 Four kinds of statement

Chapter 3 specifies a design, and this chapter reports on an implementation of part of it. Four kinds of statement are therefore kept apart (Table 4.1). A design intention is never reported as an implementation result, and a software test is never reported as evidence of security effectiveness.

Table: Table 4.1. Kinds of statement and evidence labels used in this chapter

| Kind of statement | Meaning | Evidence required | Label used when the evidence is absent |
|---|---|---|---|
| Proposed architecture | What Chapter 3 specifies | A Chapter 3 section, table or equation | — |
| Implemented prototype | What the code at commit `c22a97d` contains | A file and, where possible, a passing test | IMPLEMENTATION NOT CONFIRMED |
| Experimental configuration | What an experiment would run: environment, tasks, baselines, metrics, parameters | A configuration file or Chapter 3 section | PLANNED — NOT EXECUTED |
| Measured evidence | A value obtained by executing code | An evidence file with the exact value | RESULT NOT AVAILABLE; EVIDENCE REQUIRED |

Two further labels carry over from earlier chapters and project records:

- **SOURCE NOT FULLY VERIFIED** marks an equation or claim whose source attribution is incomplete (Chapter 3, Table 3.17).
- **SUPERVISOR DECISION REQUIRED** marks an unresolved conflict between Chapter 3 and the implementation or the design lock.

### 4.1.3 Non-invasive placement

Chapter 3 places REM at the tool-execution boundary of the agent loop (Section 3.11.1). There, REM intercepts each proposed tool call before execution and each tool result on its return, without modifying the agent's internals (assumption AS-1). The implementation realizes the evaluation side of this placement. `RemPipeline.evaluate_step` receives one step of a recorded or live trajectory and returns a verdict, a mitigation outcome and an audit record for that step. The pipeline reads only what a step object carries:

- the context items with provenance slots;
- the proposed tool call and its arguments;
- the observation returned;
- the agent's observed lifecycle state.

The pipeline has no access to model parameters or internal reasoning, which is consistent with AS-10.

The interception side, a connection between this pipeline and an executing agent, has not been built. No adapter to AgentDojo or to any other agent framework exists in the repository, and AgentDojo is not installed in the environment in which the implementation was verified (E5). **AS-1 has therefore not been demonstrated (IMPLEMENTATION NOT CONFIRMED).** The prototype is currently a mediation library, not a deployed interception layer.

### 4.1.4 Governance of the implementation

The implementation is governed by the project design lock `CLAUDE.md`. The lock fixes the following:

- the five layers;
- the pipeline order;
- the four verdicts;
- the estimator, calibrator and decision rule;
- the audit-only status of attribution;
- step-level mitigation semantics.

It requires the software to refuse to run, rather than substitute defaults, when a design input is missing. The code enforces this through a single exception type, `DesignNotSpecifiedError`, and through a configuration loader that raises an `UnspecifiedParameterError` carrying a "DESIGN BLOCKED" report for any parameter whose value is still `REQUIRED_FROM_DESIGN`.

The implementation (19 September 2026) predates the current Chapter 3 (22 September 2026). It was built from the lock alone. The lock lists as unresolved several items that Chapter 3 now specifies, such as the feature set, the predicates, the tier map and the Modify mechanism. No record shows that these Chapter 3 specifications have been approved as frozen (decision SD-FREEZE in the supervisor decision register). They have therefore not been implemented, and the implementation contains no invented substitute for them.

## 4.2 System Architecture

### 4.2.1 Software environment

Table 4.2 reports the environment in which the implementation was verified. It is the environment of the verification runs E1–E4, not an experimental platform. No experiment has been run on it.

Table: Table 4.2. Software environment of the verification runs (E5; `pyproject.toml`)

| Item | Value | Source |
|---|---|---|
| Package | `rem-framework` 0.2.0 | `pyproject.toml`; E5 |
| Python requirement | ≥ 3.10 | `pyproject.toml` |
| Python used | 3.11.15 | E5 |
| Runtime dependencies | NumPy (installed 2.4.6), PyYAML (installed 6.0.1) | `pyproject.toml`; E5 |
| Test framework | pytest 9.1.1 | E5 |
| Machine-learning framework | None pinned | `pyproject.toml` |
| AgentDojo | Not installed | E5 |
| Operating system; processors; memory | Linux 6.18 x86_64; 4 processors; 15 GiB | E5 |
| LLM backbone | None; RESULT NOT AVAILABLE (backbone pending supervisor approval, Section 3.11.1) | `configs/experiment.yaml` |
| GPU | None used | — |

Hardware for the planned experiments is not specified in Chapter 3 or in the configuration (EVIDENCE REQUIRED).

### 4.2.2 Code organization

The package is organized by architectural concern (Table 4.3). The mathematical operations live in `rem/algorithms/`, one sub-package per concern. The runtime sequencing, the contracts between layers and the mitigation mechanism live in `rem/core/`. Evaluation metrics live in `rem/evaluation/`. Two algorithm sub-packages, `context` and `behavior`, contain only package markers and no implementation (E6).

Table: Table 4.3. Code organization at commit `c22a97d` (E6)

| Path | Content | Implementation status |
|---|---|---|
| `rem/agent/trajectory.py` | Trajectory data model: steps, content items with provenance slots, tool calls, observations, evidence items, causal prefixes | Implemented |
| `rem/core/interfaces.py` | Abstract contracts for every pipeline component; fail-closed placeholders for unresolved components; `DesignNotSpecifiedError` | Implemented |
| `rem/core/pipeline.py` | `RemPipeline`: stage order, ablation switches, audit writing | Implemented |
| `rem/core/results.py` | Result types; the four verdicts; score semantics (uncalibrated or calibrated) | Implemented |
| `rem/core/mitigation.py` | Canonical verdict-to-mechanism mapping at step level | Implemented; Modify fails closed |
| `rem/core/audit.py` | Per-step audit record, JSON Lines output | Implemented |
| `rem/algorithms/detection/ridge_logistic.py` | Ridge logistic regression | Implemented |
| `rem/algorithms/calibration/platt.py` | Logistic calibration on the logit | Implemented (see SC-4) |
| `rem/algorithms/decision/expected_loss.py` | Loss grid container; conditional risk; argmin verdict | Implemented (see SC-2) |
| `rem/algorithms/attribution/linear_shapley.py` | Linear attribution, audit-only | Implemented |
| `rem/algorithms/context/` | Intended for context and action evidence | Empty |
| `rem/algorithms/behavior/` | Intended for behavioral evidence | Empty |
| `rem/evaluation/metrics.py`, `runtime.py` | Confusion-matrix metrics, Brier score, latency statistics, throughput | Implemented (see Section 4.11) |
| `rem/config/loader.py`, `configs/*.yaml` | Parameter records with value, meaning, source, justification and status | Implemented |
| `rem/traceability/registry.py`, `scripts/generate_traceability.py` | Formula-to-citation records; refusal to create equation identifiers without the authoritative registry | Implemented |
| `rem/utils/reproducibility.py` | Seeding and environment manifest | Implemented |
| `experiments/run_experiment.py` | Readiness check and fail-closed runner | Implemented; runs no experiment |

### 4.2.3 The five layers in the implementation

The code declares exactly five architectural layers: context, detection, behavior, decision and mitigation (`Layer.FROZEN_LAYERS` in `rem/core/pipeline.py`). A contract test asserts that there are five (`test_exactly_five_frozen_layers`). Further tests assert that no feedback layer, feedback sink or separate risk-score layer exists (`test_there_is_no_feedback_layer`, `test_no_feedback_sink_exists_anywhere`, `test_pipeline_has_no_risk_score_layer`). Calibration and attribution appear as switchable elements for ablation, but they are not counted as layers. The five-layer architecture of Chapter 3 (Section 3.2.1) is therefore preserved.

The assignment of components to layers is not the same in the code and in Chapter 3 (Table 4.4). Chapter 3 places the following in the Decision Engine (Layer 4): probability estimation, calibration, the consequence tier, the policy predicates, the verdict and the audit record. It reserves the Detection Layer (Layer 2) for the injection-classifier score and the instruction-pattern indicator. In the code, ridge logistic regression is labeled as the Detection layer, calibration is labeled cross-cutting, and a single Layer 1 component (`ContextProcessor`) is expected to produce the whole evidence vector. The computation order is the same in both. The labels differ. This chapter reports the implementation under the Chapter 3 layer names and records the difference as specification conflict SC-6 (**SUPERVISOR DECISION REQUIRED**).

Table: Table 4.4. Component-to-layer assignment in Chapter 3 and in the implementation (SC-6)

| Component | Chapter 3 layer | Layer label in the code | Implemented |
|---|---|---|---|
| Context capture, provenance labeling, entity extraction | L1 Input & Context | L1 (`ProvenanceLabeler`, `ContextProcessor`) | Contract only; fails closed |
| Injection-classifier score, instruction-pattern indicator | L2 Detection | none | No |
| History tracking, behavioral and action features | L3 Behavioral Analysis | L3 (`BehaviorModel`); features expected from L1 `ContextProcessor` | History representation only |
| Ridge logistic estimation (Eqs. 3.1–3.2) | L4 Decision Engine | L2 "Detection" | Yes |
| Calibration on the logit (Eqs. 3.3–3.4) | L4 at runtime; fitting cross-cutting | "Cross-cutting" | Yes (fitting differs; SC-4) |
| Consequence tier, policy predicates | L4 | L4 | Contract only; fails closed |
| Expected-loss verdict (Eqs. 3.6–3.7) | L4 | L4 | Yes (no tie order; SC-2) |
| Audit record and linear attribution (Eqs. 3.11–3.12) | L4 | Audit stage after mitigation; attribution "audit-only" | Yes |
| Mechanisms for the four verdicts | L5 Mitigation | L5 | Step-level (SC-1) |

### 4.2.4 Runtime sequence

For one step, `RemPipeline.evaluate_step` performs the operations below in a fixed order. Each operation runs only if its component is attached and its element is enabled.

1. Provenance labeling of the step's content.
2. Behavioral analysis of the trajectory prefix strictly before the step.
3. Construction of the evidence vector x_t.
4. Computation of the logit s_t and the uncalibrated probability p̃_t.
5. Calibration to p_t.
6. Assignment of the consequence tier k_t.
7. Evaluation of the policy predicates.
8. Selection of the verdict.
9. Application of the mitigation mechanism.
10. Computation of the audit-only attribution.
11. Writing of the audit record.

This is the pipeline order of Chapter 3's Algorithm 1 and of the design lock, with one difference in presentation: attribution is computed after mitigation rather than before it. Chapter 3 states that attribution is an audit operation that does not affect the verdict (Algorithm 1, lines 24–25). Computing it later preserves that property by construction. A test checks that attribution runs after the verdict is final (`test_attribution_runs_after_the_verdict`).

Two structural safeguards are part of the sequence:

- **Causal evaluation.** Every component that analyzes history receives a truncated copy of the trajectory containing only the steps before the current one (`Trajectory.prefix`; `test_evaluation_is_causal`, `test_prefix_is_causal`). A step therefore cannot be scored with information from its own future.
- **Calibration cannot be bypassed.** If the decision engine is enabled and calibration is disabled, the pipeline raises instead of passing the uncalibrated probability to the decision rule (`test_ablating_calibration_is_refused`). Section 4.13 discusses how this interacts with the ablations planned in Chapter 3 (SC-3).

### 4.2.5 Configuration and fail-closed control

Every design parameter is recorded in one of seven configuration files, `configs/*.yaml`. Each parameter carries a value, a meaning, a source, a justification and a status. The loader rejects a parameter that lacks any of these fields (`test_parameter_without_source_is_rejected`, `test_parameter_without_justification_is_rejected`). A value of `REQUIRED_FROM_DESIGN` cannot be read: reading it raises an error that reports the item as design-blocked (`test_unresolved_value_reports_design_blocked`).

The readiness run of the experiment runner (E3) reports 27 parameters with status FROZEN and 19 unresolved, and seven unattached pipeline components. Table 4.5 gives the distribution by file. The status FROZEN in these files is the configuration's own label. For four of the 27, Chapter 3 either specifies something different or defers the item: the calibration target smoothing and fitting split (SC-4), the Brier score (SC-5), and the random seed of 42, which the file itself describes as an engineering convention rather than a modeling parameter.

Table: Table 4.5. Configuration parameters by status (E3; `configs/*.yaml`)

| File | FROZEN | Unresolved | Unresolved parameters |
|---|---|---|---|
| `attribution.yaml` | 3 | 1 | background mean x̄ |
| `behavior.yaml` | 2 | 2 | behavioral evidence features; optional CUSUM scenarios |
| `calibration.yaml` | 6 | 0 | — |
| `decision.yaml` | 4 | 4 | loss grid; consequence tiers; policy predicates; tie-breaking rule |
| `detection.yaml` | 4 | 4 | ridge penalty λ; feature set; injection classifier; labeling of attacker-induced reads |
| `experiment.yaml` | 3 | 7 | dataset; AgentDojo version; grouping scheme; LLM backbones; number of repeats; external benchmarks; splits |
| `mitigation.yaml` | 5 | 1 | Modify mechanism |
| **Total** | **27** | **19** | |

A full run of the experiment runner writes an environment manifest and a readiness report, then stops with a "DESIGN BLOCKED" message and exit code 1 (E4). This is the fail-closed behavior required by the design lock, not a malfunction.

## 4.3 Input and Context Processing

Chapter 3 assigns four operations to the Input & Context Layer (Section 3.4):

- capture of the objective, messages, tool results and the proposed action;
- removal of invisible and formatting characters from untrusted text;
- provenance labeling under a least-trusted inheritance rule;
- extraction of security-relevant entities with their provenance.

The implementation provides the data model on which these operations would act. It does not implement the operations themselves (Table 4.6).

Table: Table 4.6. Input & Context Layer: Chapter 3 specification and implementation status

| Chapter 3 element (Section 3.4) | Implementation | Status |
|---|---|---|
| Representation of steps, context, proposed action, observation | `TrajectoryStep`, `ContentItem`, `ToolCall`, `Observation` in `rem/agent/trajectory.py` | Implemented |
| Content carried verbatim for inspection | `ContentItem.content` is never altered by the data model (`test_prompt_injection_content_is_carried_verbatim`) | Implemented |
| Provenance labels trusted ≻ semi-trusted ≻ untrusted | The code enumerates origins, not trust levels: `SYSTEM`, `USER`, `TOOL_OUTPUT`, `MODEL`, and a default `UNLABELLED` | Categories differ from Chapter 3; mapping IMPLEMENTATION NOT CONFIRMED |
| Least-trusted inheritance rule | `UnspecifiedProvenanceLabeler` raises `DesignNotSpecifiedError` | IMPLEMENTATION NOT CONFIRMED |
| Removal of invisible and formatting characters | None | IMPLEMENTATION NOT CONFIRMED |
| Entity extraction (account identifiers, amounts, credentials, profile values, tool names) with provenance | `Evidence` records can hold named values; no extractor exists | IMPLEMENTATION NOT CONFIRMED |
| Interception of live tool calls and tool results (AS-1) | None | IMPLEMENTATION NOT CONFIRMED |

The data model has two properties that Chapter 3 relies on:

- **Provenance defaults to unlabeled** (`test_provenance_defaults_to_unlabelled`). Content is never treated as trusted merely because no rule has examined it.
- **An evidence item carries no weight or severity** (`test_evidence_carries_no_weight`, `test_evidence_carries_no_weight_or_severity`). Evidence records only what was observed, and its combination into a score is left to the fitted estimator. This agrees with Chapter 3's separation of evidence from decision (Section 3.2.3).

## 4.4 Detection

The Detection Layer specified in Chapter 3 computes two context-evidence features from untrusted segments (Table 3.8):

- $x^{\text{ctx}}_{1}$, the maximum score of a fixed, pre-trained prompt-injection classifier;
- $x^{\text{ctx}}_{2}$, an indicator for a declared instruction-pattern set.

Neither feature is implemented. The choice of classifier is pending supervisor approval (Table 3.8; configuration parameter `detection.injection_classifier`). The instruction-pattern set has not been declared. The `rem/algorithms/context/` package is empty (E6). **The Detection Layer of Chapter 3 is therefore not implemented (IMPLEMENTATION NOT CONFIRMED).**

The relation of this layer to the threat model is unchanged from Chapter 3. Both features target indirect prompt injection arriving through trust boundary TB-2 (security objective SO-1). Chapter 3 states that both are individually evadable and that the layer is not relied upon to be decisive (Section 3.5). No detection performance of any kind has been measured (RESULT NOT AVAILABLE).

The component that the code labels "Detection", ridge logistic regression, is the estimator that Chapter 3 places in the Decision Engine. It is described in Section 4.6.

## 4.5 Behavioral Analysis

Chapter 3 specifies step tracking and seven binary or bounded features (Table 3.9). Four are behavioral:

- post-observation shift;
- repeated calls;
- privilege escalation;
- transition deviation.

Three are action evidence:

- argument provenance;
- destination novelty;
- sensitive egress.

Chapter 3 does not specify an anomaly-detection model, a goal-drift detector or a loop detector beyond the repeated-call feature $x^{\text{beh}}_{2}$.

The implementation status is reported in Table 4.7.

Table: Table 4.7. Behavioral Analysis Layer: Chapter 3 specification and implementation status

| Chapter 3 element (Section 3.6) | Implementation | Status |
|---|---|---|
| Step tracking: history H_t of actions, arguments, verdicts and results, reset per episode | `Trajectory` holds steps in order, records observed state transitions and provides causal prefixes; each trajectory is a separate object | Representation implemented; argument provenance within H_t IMPLEMENTATION NOT CONFIRMED |
| $x^{\text{beh}}_{1}$ post-observation shift | None | IMPLEMENTATION NOT CONFIRMED |
| $x^{\text{beh}}_{2}$ repeated calls (loop behavior) | None | IMPLEMENTATION NOT CONFIRMED |
| $x^{\text{beh}}_{3}$ privilege escalation (privilege map declared) | None | IMPLEMENTATION NOT CONFIRMED |
| $x^{\text{beh}}_{4}$ transition deviation (benign reference transition set) | None | IMPLEMENTATION NOT CONFIRMED |
| $x^{\text{act}}_{1}$ argument provenance | None | IMPLEMENTATION NOT CONFIRMED |
| $x^{\text{act}}_{2}$ destination novelty | None | IMPLEMENTATION NOT CONFIRMED |
| $x^{\text{act}}_{3}$ sensitive egress | None | IMPLEMENTATION NOT CONFIRMED |
| Optional observe-only CUSUM analysis (Eqs. 3.15–3.19) | None; `configs/behavior.yaml` records CUSUM as optional and observe-only | Not implemented; approval pending (Section 3.11.10) |

The `BehaviorModel` contract requires any observe-only signal to be flagged as such, and the decision engine refuses flagged inputs. Neural trajectory models are excluded (`configs/behavior.yaml`, `trajectory_model: none`), consistent with Chapter 3, which specifies none.

Goal drift and abnormal tool use are named in the task brief for this chapter, but Chapter 3 does not specify them as separate mechanisms. They are not reported as implemented, and no mechanism for them is proposed here.

## 4.6 Decision Engine

The Decision Engine is the most complete part of the implementation. Its mathematical operations are implemented, and each is recorded with a citation by a `@derivation` decorator. The generated file `docs/MATHEMATICAL_TRACEABILITY.md` lists 19 such operations. None carries an equation identifier, because the authoritative equation registry has not been supplied and the design lock forbids provisional identifiers (E6). The equations below are reproduced from Chapter 3 with their Chapter 3 numbers and verification status. No equation is introduced in this chapter.

### 4.6.1 Probability estimation

The runtime score and uncalibrated probability are those of Equation 3.1 (Cox, 1958; verification IV; **SOURCE NOT FULLY VERIFIED**):

$$ s_{t} = \beta_{0} + \beta^{\top} x_{t}, \qquad \tilde{p}_{t} = \sigma(s_{t}) \qquad\qquad (3.1) $$

`RidgeLogisticRegression.decision_function` computes s_t for an evidence vector in a fixed, named feature order. `uncalibrated_probability` computes p̃_t with a numerically stable form of the logistic function. The detector emits no class label. Its output is marked "unthresholded", so no implicit 0.5 threshold can act as a hidden operating point (`test_detector_emits_no_thresholded_label`). A missing feature raises an error rather than being imputed (`test_detector_refuses_missing_features`).

The coefficients are fitted by penalized maximum likelihood with an unpenalized intercept. This is Equation 3.2 of Chapter 3 (le Cessie & van Houwelingen, 1992; verification IV, penalty constant pending, OI-10; **SOURCE NOT FULLY VERIFIED**). The implementation writes the penalty as (λ/2)‖β‖² where Equation 3.2 writes λ‖β‖². The two differ only by the positive factor 2 on λ: a value λ_code in the implementation corresponds to λ = λ_code/2 in Equation 3.2. Chapter 3 states that rescaling the penalty by a positive constant changes the selected value of λ and not the set of attainable solutions (Section 3.7.1). The fit uses Newton–Raphson iterations.

The code documents this procedure by citing a statistical-learning textbook (Hastie, Tibshirani & Friedman, 2009). That source is not in the thesis reference lists and has no project verification record (**SOURCE VERIFICATION REQUIRED**). λ has no default: fitting without it raises `DesignNotSpecifiedError`, and a zero penalty is rejected as not being ridge regression (`test_fit_without_penalty_is_design_blocked`, `test_zero_penalty_is_not_ridge`). The grouped cross-validation that Chapter 3 specifies for selecting λ (Sections 3.7.1, 3.9) is not implemented (IMPLEMENTATION NOT CONFIRMED).

### 4.6.2 Calibration on the logit

The calibrated probability is that of Equation 3.3 (verification: Platt NC; Guo et al., 2017, FV; Kull et al., 2017, FV; **SOURCE NOT FULLY VERIFIED** for the Platt attribution, which is under citation conflict OI-07):

$$ p_{t} = \sigma(\gamma_{1} s_{t} + \gamma_{0}), \qquad \gamma_{1} > 0 \qquad\qquad (3.3) $$

`PlattLogitCalibrator.calibrate` computes Equation 3.3 from the logit, never from p̃_t. It refuses a detection result that carries no logit (`test_transform_requires_a_logit`). A fitted slope γ₁ ≤ 0 raises `MonotonicityViolationError` (`test_platt_rejects_an_inverted_detector`). This corresponds to Chapter 3's requirement that a non-positive slope be rejected and reported (Section 3.7.2, property 1). Every score carries a semantic tag, uncalibrated or calibrated. The decision engine reads only a calibrated probability and raises on anything else (`test_decide_requires_a_calibrated_probability`, `test_only_calibrated_scores_are_calibrated`). Beta, isotonic and temperature calibration are absent (`test_forbidden_components_are_absent_from_the_codebase`), in agreement with Chapter 3, which adopts neither beta nor isotonic calibration (Section 3.7.2, property 2).

The fitting of γ₀ and γ₁ differs from Chapter 3:

- **Chapter 3.** Equation 3.4 minimizes the negative log-likelihood of the observed labels y_i on out-of-fold logits obtained by nested grouped cross-fitting (Procedure 3.1).
- **Implementation.** It minimizes the negative log-likelihood against smoothed targets, t₊ = (N₊+1)/(N₊+2) for positive and t₋ = 1/(N₋+2) for negative examples, on one held-out split supplied by the caller. The configuration names the validation split. The code attributes the smoothed targets to Platt (1999), which is the source under conflict OI-07.

This difference is recorded as SC-4 (**SUPERVISOR DECISION REQUIRED**).

### 4.6.3 Consequence tiers and policy predicates

The consequence descriptors and tier map κ (Tables 3.10–3.11) and the predicates D1 (prohibited action) and D2 (missing required evidence) (Section 3.7.4) are not implemented. The tier map is marked in Chapter 3 as "policy pending supervisor approval", and the prohibited set Π, the tier threshold k_D2 and the required evidence per tier are declared policy with no declared values.

The pipeline accepts a `ConsequenceTierAssigner` and a `PolicyPredicate`. The shipped placeholders for both raise `DesignNotSpecifiedError`. The decision engine refuses to decide without a tier (`test_decide_requires_a_consequence_tier`). If a predicate fires while no predicate policy has been declared, the engine raises rather than ignoring it (`test_firing_predicate_without_policy_is_design_blocked`). Chapter 3 gives D1 and D2 precedence over the expected-loss rule. That precedence cannot yet be exercised because no predicate policy exists (IMPLEMENTATION NOT CONFIRMED).

### 4.6.4 Expected-loss verdict selection

For a calibrated probability p_t and a tier k_t, the engine computes the conditional risk of each verdict by Equation 3.6 and selects the verdict of minimum risk by Equation 3.7 (Elkan, 2001, FV for the Equation 1 form; Chow, 1970, IV, conceptual support for escalation):

$$ R_{t}(v) = (1 - p_{t})\, L(v, 0, k_{t}) + p_{t}\, L(v, 1, k_{t}) \qquad\qquad (3.6) $$

$$ v_{t} = \arg\min_{v} R_{t}(v) \qquad\qquad (3.7) $$

The loss function is supplied as a `LossGrid`. The grid must name its source, must be non-empty, and must cover every combination of verdict, label and tier that it mentions (`test_loss_grid_requires_a_source`, `test_incomplete_loss_grid_is_rejected`). Without a grid the engine cannot be constructed (`test_engine_without_loss_grid_is_design_blocked`). The full table R_t(·) is attached to every decision so that the argmin can be rechecked from the audit record (`test_decision_records_the_full_risk_table`, `test_audit_record_permits_rechecking_the_argmin`). No loss values exist: the costs C_miss(k), C_FA(k), C_mod(k) and C_esc of Table 3.13 are declared policy with no declared values (SD-1). The tests use a loss grid that the test file declares is "not a REM design value".

The implementation differs from Chapter 3 in four respects:

1. **Tie-breaking (SC-2).** Chapter 3 resolves ties toward the more restrictive verdict in the order Block ⪰ Escalate ⪰ Modify ⪰ Allow. The implementation raises `VerdictTieError` on an exact tie (`test_exact_tie_raises_rather_than_choosing`), because no tie rule was frozen in the design lock. This conflict is unresolved, and no tie-breaking policy is reported here as adopted (**SUPERVISOR DECISION REQUIRED**).
2. **Feasible verdict set.** Chapter 3 minimizes over 𝒱(a_t), which contains Modify only for tools in 𝒯_R. The implementation minimizes over all four verdicts for every action (IMPLEMENTATION NOT CONFIRMED).
3. **Loss structure and dominance check.** The tier-indexed structure of Table 3.13, the adversarial Modify loss of Equation 3.5 and the dominance check of Section 3.7.5 are not implemented. The `LossGrid` container checks completeness, not coherence (IMPLEMENTATION NOT CONFIRMED).
4. **Derived thresholds.** Equations 3.8–3.10 are analytical consequences of Equation 3.6 and are not needed to compute a verdict. They are not implemented as runtime operations.

### 4.6.5 Audit record and attribution

For every evaluated step the pipeline writes one audit record. When a file path is configured, the record is appended as one JSON line. It contains:

- the timestamp, trajectory identifier and step index;
- digests of the prompt, model output and tool arguments (the first 16 hexadecimal characters of a SHA-256 hash; verbatim payloads only when explicitly enabled);
- the evidence items;
- the calibrated and uncalibrated detector summaries, including s_t, p̃_t and p_t;
- the tier, the predicate outcomes and the conditional-risk table;
- the verdict and its rationale;
- the mitigation outcome;
- the audit-only attribution;
- code and configuration versions.

Compared with Section 3.7.6:

- The record lacks the "source of the verdict (D1, D2, or expected-loss rule)", because predicates are not implemented.
- It lacks the group sums Φ_J of Equation 3.13, which are not implemented.
- The log is written in append mode but is not tamper-evident. Chapter 3 treats the protection of REM's logs as an assumption (AS-3).

The attribution follows Equation 3.11 with base value φ₀ = β₀ + βᵀx̄ (Lundberg & Lee, 2017; verification FV):

$$ \phi_{t,i} = \beta_{i} (x_{t,i} - \overline{x}_{i}), \quad i = 1, \dots, d; \qquad \phi_{0} = \beta_{0} + \beta^{\top} \overline{x} \qquad\qquad (3.11) $$

A test confirms the completeness identity of Equation 3.12, φ₀ + Σᵢ φ_{t,i} = s_t, on fixture values (`test_local_accuracy_holds`). The attribution result is flagged audit-only, and the decision engine raises if such a result reaches it (`test_attribution_cannot_reach_the_decision_engine`). The `decide` method has no attribution parameter (`test_decision_engine_signature_excludes_attribution`). The background mean x̄ has no value (configuration parameter `attribution.background_mean`), because it must be estimated on benign fitting data that do not yet exist. The code also cites Shapley (1953), which is not in the thesis reference lists (**SOURCE VERIFICATION REQUIRED**).

### 4.6.6 Offline fitting

Procedure 3.1 of Chapter 3 is not implemented (IMPLEMENTATION NOT CONFIRMED). It covers:

- nested grouped cross-fitting over nine leave-one-injection-task-out outer folds;
- λ selection by inner grouped cross-validation;
- out-of-fold calibration;
- baseline threshold selection;
- estimation of r_mod(k);
- the dominance check;
- version freezing.

The implemented estimator and calibrator can each be fitted on arrays supplied by a caller. No code partitions data into groups or folds (E6).

## 4.7 Mitigation

The Mitigation Layer is implemented as a fixed, immutable mapping from each verdict to one mechanism (`CANONICAL_MECHANISM` in `rem/core/mitigation.py`). Contract tests assert this mapping and its immutability (`test_canonical_mitigation_mapping_is_the_frozen_one`, `test_canonical_mapping_is_immutable`). The mechanisms act on the current step only, and a test asserts that no mechanism sets an episode-level flag (`test_no_mechanism_sets_an_episode_level_flag`). This follows the Mitigation Lock of `CLAUDE.md`. It does not follow Table 3.14 of Chapter 3, which specifies episode-level restrictions for Modify and Block.

The difference is specification conflict SC-1. It is unresolved, and this chapter does not choose between the two readings. Table 4.8 sets them side by side.

Table: Table 4.8. Mitigation semantics: Chapter 3 description and current implementation semantics (SC-1; SUPERVISOR DECISION REQUIRED)

| Verdict | CHAPTER 3 DESCRIPTION (Table 3.14; Algorithm 1) | CURRENT IMPLEMENTATION SEMANTICS (`rem/core/mitigation.py`) | Test |
|---|---|---|---|
| Allow | Release a_t across TB-3; log the event | Release the current action unchanged | `test_allow_releases_the_action` |
| Modify | Tool restriction: a_t is not executed; the tool class of a_t is removed for the rest of the episode; a structured notice is returned; applies only to tools in 𝒯_R | Apply ONE declared modification mechanism to the current action only. No mechanism is declared, so a Modify verdict raises `DesignNotSpecifiedError` | `test_modify_without_a_declared_mechanism_is_design_blocked`, `test_modify_uses_the_declared_mechanism` |
| Escalate | Withhold a_t; present the audit record to a human reviewer; release only on approval | Withhold the current action by marking it as awaiting review. No reviewer workflow and no release-on-approval path exist | `test_escalate_withholds_pending_review` |
| Block | a_t is not executed; every tool in 𝒯_R is restricted for the rest of the episode; a structured refusal is returned | Prevent execution of the current action only (the proposed tool call is removed from the step). No episode-level restriction | `test_block_prevents_execution_of_this_step_only` |

Two consequences follow for later chapters:

- Chapter 3 derives its restrictiveness ordering and its tie order from the episode-level reading (Section 3.8, property 1). Under the implemented reading that justification does not hold in the same form.
- The residual rate r_mod(k) in Equation 3.5 is defined for the Chapter 3 Modify mechanism. It cannot be measured until SC-1 and the Modify mechanism (SD-3) are decided.

No structured notice to the agent, no safe-fallback message and no human-reviewer interface are implemented (IMPLEMENTATION NOT CONFIRMED).

## 4.8 Experimental Environment

Chapter 3 specifies the experimental environment as the banking suite of AgentDojo (Debenedetti et al., 2024). REM would be placed at the tool-execution boundary and run in two modes: observe-only, for collecting fitting data, and enforcing, for executing verdicts (Section 3.11.1). For every run, Chapter 3 requires the following to be recorded:

- the AgentDojo release or commit, the suite version and the attack template;
- the LLM backbone with version, access date and decoding parameters;
- REM's model, calibration and policy versions.

None of these runs has been performed. Table 4.9 gives the status of each element of the environment.

Table: Table 4.9. Experimental environment: specified and actual status

| Element | Chapter 3 specification | Actual status |
|---|---|---|
| Benchmark | AgentDojo banking suite (Section 3.11.1) | PLANNED — NOT EXECUTED; AgentDojo not installed (E5) |
| Benchmark version or commit | To be pinned (Section 3.11.2; OI-14) | Not pinned (`experiment.agentdojo_version` unresolved) |
| LLM backbone(s), decoding parameters | Pending supervisor approval (Section 3.11.1) | Not selected |
| Attack templates | Pending supervisor approval (Section 3.11.1) | Not selected |
| Observe-only and enforcing modes | Specified (Section 3.11.1) | Not implemented |
| Run records (versions, dates, parameters) | Specified (Section 3.11.1) | Manifest mechanism implemented (`EnvironmentManifest`: seed, configuration digests, `CLAUDE.md` digest, dependencies, git commit and state); no experimental run recorded |
| Random seed | Not specified in Chapter 3 | 42 in `configs/experiment.yaml`, described there as an engineering convention |
| Hardware | Not specified | EVIDENCE REQUIRED |

## 4.9 Dataset and Evaluation Tasks

No dataset or trace has been produced or used. `data/` is empty, and no experiment output exists in the repository. The evaluation tasks can therefore be described only as Chapter 3 specifies them.

Chapter 3 reports the banking suite definition it inspected: suite v1, AgentDojo repository main branch, accessed September 2026 (Section 3.11.2). It notes that the counts "must be re-confirmed against the benchmark version pinned for the experiments". The suite contains:

- 16 user tasks;
- 9 injection tasks, eight directing money or a recurring payment to one shared attacker account identifier and one changing the account password;
- 11 tools.

Table 4.10 classifies the evaluation categories that Chapter 3 defines. No other category exists in the project records. No sample count is reported, because the number of traces depends on the backbones, attack templates and repeats, none of which is fixed (Section 3.11.2, marked "[DATA COUNT REQUIRES VERIFICATION]").

Table: Table 4.10. Evaluation categories specified in Chapter 3 (PLANNED — NOT EXECUTED)

| Category | Definition in Chapter 3 | Source | Count |
|---|---|---|---|
| Benign (no-injection) episodes | Episodes of the 16 user tasks without injection; every step labeled y_t = 0 | Sections 3.11.2–3.11.3 | 16 task templates (to be re-confirmed); traces RESULT NOT AVAILABLE |
| Attack (injection) episodes | Combinations of user tasks and injection tasks; 144 combinations, which Chapter 3 states are not independent samples | Section 3.11.2 | 9 injection-task templates (to be re-confirmed); traces RESULT NOT AVAILABLE |
| Adversarially induced steps (y_t = 1) | Proposed calls that match the injection task's reference solution on tool name and attacker-controlled key argument | Section 3.11.3 | RESULT NOT AVAILABLE |
| Induced read steps | Read calls in the injection reference solution; labeling pending supervisor decision | Section 3.11.3 | Not labeled |
| Financial tool-use actions | 11 tools in five categories: read, value transfer, payment modification, credential change, profile change | Table 3.7 | 11 tools (to be re-confirmed) |

## 4.10 Baselines

No baseline has been implemented or evaluated. Chapter 3 specifies the configurations in Table 4.11. The operating-point threshold policy is a baseline only, not a second primary method (design lock; Chapter 3, Section 3.7.7). No system from the literature has been reproduced, and no system discussed in Chapter 2 is used as an experimental baseline.

Table: Table 4.11. Configurations and baselines specified in Chapter 3

| Configuration | Specification | Implementation status | Result |
|---|---|---|---|
| B0, no defense | Agent without REM (Section 3.11.7) | Requires the AgentDojo integration; IMPLEMENTATION NOT CONFIRMED | RESULT NOT AVAILABLE |
| B1, consequence-independent baseline | Same estimator and calibration; thresholds θ(α) selected by Equation 3.14 on benign validation steps; primary comparator for RQ2 | Equation 3.14 and the threshold rule are not implemented; α_blk and α_mod are not declared | RESULT NOT AVAILABLE |
| REM | Expected-loss verdict selection (Section 3.7.5) | Decision core implemented; features, tiers, predicates, losses and Modify mechanism missing | RESULT NOT AVAILABLE |
| B2, detection-only | Pending supervisor approval | Not implemented | RESULT NOT AVAILABLE |
| Distributed defenses | Pending supervisor approval | Not implemented | RESULT NOT AVAILABLE |

## 4.11 Evaluation Metrics

Chapter 3 defines primary metrics that do not depend on declared costs (Table 3.15) and secondary metrics (Section 3.12.2): ROC-AUC, PR-AUC, ECE (Equation 3.20), log-loss (Equation 3.21), and realized loss across a declared grid (Equation 3.22). Table 4.12 reports which of these are implemented. None has been computed on data.

Table: Table 4.12. Metrics specified in Chapter 3 and implementation status

| Metric (Chapter 3) | Level | Implemented | Computed on data |
|---|---|---|---|
| Attack success rate (ASR) | Episode | No (requires benchmark security checks) | No |
| Benign utility | Episode | No (requires benchmark utility checks) | No |
| Utility under attack | Episode | No | No |
| Intervention rates per verdict, by label | Step | No | No |
| Step false-positive rate | Step | The confusion-matrix function `false_positive_rate` exists; the Chapter 3 definition (interventions on y = 0 steps) is not wired to verdicts | No |
| Residual ASR under Modify | Episode | No | No |
| Escalation rate, under the idealized reviewer and the no-reviewer bound | Step | No | No |
| Latency, median and 95th percentile, excluding LLM and tool time | Step | Mean, sample quantile (Hyndman & Fan definition 7) and a latency recorder exist | No |
| ROC-AUC; PR-AUC | Step | No | No |
| ECE (Eq. 3.20) | Step | No | No |
| Log-loss (Eq. 3.21) | Step | No | No |
| Brier score | Step | Implemented, but deferred by Chapter 3 until its convention is confirmed (SC-5; OI-09) | No |
| Realized loss across a declared grid (Eq. 3.22) | Step | No | No |

The implementation also contains precision, recall (named "attack detection rate"), F1, false-negative rate, accuracy and throughput. These are not among the metrics that Chapter 3 specifies. The code cites Fawcett (2006) for the confusion-matrix definitions and van Rijsbergen (1979) for precision and F1; the latter is not in the thesis reference lists (**SOURCE VERIFICATION REQUIRED**).

Undefined values are returned as not-a-number rather than zero (`test_undefined_metrics_are_nan_not_zero`). The Brier function refuses uncalibrated input (`test_brier_score_rejects_uncalibrated_results`). These functions are verified against hand-computed values in the test suite. That verifies the arithmetic only.

## 4.12 Experimental Results

### 4.12.1 Empirical results

No empirical result exists for any metric in Table 4.12, any configuration in Table 4.11 or any research question of Chapter 3. Table 4.13 records this explicitly for each research question, so that the absence cannot be mistaken for an omission in reporting.

Table: Table 4.13. Empirical results for the research questions of Chapter 3

| Research question (Section 3.1.3; [PD], pending supervisor confirmation) | Principal metrics (Table 3.2) | Result | Evidence required |
|---|---|---|---|
| RQ1, estimation | ROC-AUC, PR-AUC, ECE, log-loss | RESULT NOT AVAILABLE | Features, labeled traces, Procedure 3.1, metric implementations |
| RQ2, decision | ASR, benign utility, utility under attack, intervention rates, realized loss | RESULT NOT AVAILABLE | Integration with AgentDojo; B1; tiers and loss grid (SD-1, SD-2); SC-2 decision |
| RQ3, mitigation and cost | Residual ASR under Modify, escalation rate, latency | RESULT NOT AVAILABLE | SC-1 and SD-3 decisions; Modify mechanism; enforcing-mode runs; latency measurement |
| RQ4, component contribution | Change in the metrics above under ablation | RESULT NOT AVAILABLE | All of the above; SC-3 decision |

### 4.12.2 Software-verification evidence

The evidence that does exist concerns the correctness of the implemented code. Table 4.14 lists every numerical value reported in this chapter with its source artifact. The values are exact and unrounded as they appear in the artifacts.

These values describe the software, not the security of an agent. The pipeline tests exercise the implemented stage order end to end, but they do so on fixture components that the test file declares "not REM design values":

- two toy features;
- a single tier labeled `t1`;
- a hand-written loss grid;
- eight training rows.

A fixture test named `test_exfiltration_after_injection_is_not_allowed` shows that the pipeline, wired with those fixtures, does not return Allow for a fixture step. It is not evidence that REM prevents exfiltration by an agent, and it is not reported as such.

Table: Table 4.14. Values reported in this chapter and their evidence trail

| Result | Artifact / file | Exact source | Reproducible? | Notes |
|---|---|---|---|---|
| 154 tests collected | `evidence/E2_pytest_collection.txt` | Last line: `154 tests collected in 0.14s` | Yes: `python3 -m pytest -o addopts="" --collect-only -q` at `c22a97d` | Matches `STAGE2_5_BASELINE_TEST_RECONCILIATION.md` §3 |
| 154 tests passed, 0 failed | `evidence/E1_pytest_verbose_run.txt` | Last line: `154 passed in 0.47s` | Yes: `python3 -m pytest -o addopts="" -v` | The duration measures the test run, not REM latency |
| Tests per file: frozen math 43, metrics 25, pipeline 21, contract compliance 20, configuration 15, trajectory 12, reproducibility 9, mitigation 9 | `evidence/E1_pytest_verbose_run.txt` | Per-file node IDs | Yes | The historical figure of 139 contract-compliance tests was incorrect (Stage 2.5 audit) |
| 27 FROZEN parameters; 19 unresolved | `evidence/E3_dry_run/evidence-dryrun/readiness.json`; `evidence/E3_dry_run_stdout.txt` | `"frozen_parameters": 27`; 19 entries in `unresolved_parameters` | Yes: `python3 experiments/run_experiment.py --dry-run` | Distribution in Table 4.5 |
| 7 unattached components | same | `"unattached_components"`: context, detection, behavior, decision, mitigation, calibration, attribution | Yes | The runner attaches no component while design inputs are unresolved |
| Full run stops with DESIGN BLOCKED, exit code 1 | `evidence/E4_full_run_stdout.txt` | `## DESIGN BLOCKED`; `full-run exit: 1` | Yes: `python3 experiments/run_experiment.py` | Designed fail-closed behavior |
| 19 cited mathematical operations; 0 equation identifiers | `evidence/E6_implementation_inventory.txt`; `docs/MATHEMATICAL_TRACEABILITY.md` | `count 19`; every status `awaiting_registry_id` | Yes: `python3 scripts/generate_traceability.py` | Registry not supplied |
| `context` and `behavior` algorithm packages empty | `evidence/E6_implementation_inventory.txt` | "only `__init__.py`" | Yes | |
| Environment (Python 3.11.15, NumPy 2.4.6, PyYAML 6.0.1, pytest 9.1.1, 4 processors, 15 GiB) | `evidence/E5_environment.txt` | Lines 1–9 | Yes, on the same container image | Verification environment only |

## 4.13 Ablation and Component Analysis

No ablation has been run, and no component contribution has been measured (RESULT NOT AVAILABLE). Chapter 3 specifies seven ablations (Section 3.11.7). The implementation provides an ablation switch (`AblationSpec`) for its seven elements (context, detection, behavior, decision, mitigation, calibration, attribution), and the experiment runner lists five planned configurations: Full REM, and REM without context, behavior, attribution or mitigation. Table 4.15 compares the two.

Table: Table 4.15. Ablations specified in Chapter 3 and support in the implementation

| Chapter 3 ablation (Section 3.11.7) | Support in the implementation | Result |
|---|---|---|
| 1. Context evidence removed | Switch exists (`context`); in the code this element also produces behavioral and action features (SC-6), so it would remove more than context evidence | RESULT NOT AVAILABLE |
| 2. Behavioral evidence removed | Switch exists (`behavior`) | RESULT NOT AVAILABLE |
| 3. Action evidence removed | No separate switch | RESULT NOT AVAILABLE |
| 4. Calibration removed (p̃_t used in Eq. 3.6) | Refused by the pipeline (SC-3; SUPERVISOR DECISION REQUIRED) | RESULT NOT AVAILABLE |
| 5. Consequence tiers removed (one tier for all actions) | No switch; tiers not implemented | RESULT NOT AVAILABLE |
| 6. Predicates D1 and D2 disabled | No switch; predicates not implemented | RESULT NOT AVAILABLE |
| 7. Observe-only (no mitigation) | Switch exists (`mitigation`) | RESULT NOT AVAILABLE |
| Not in Chapter 3: attribution removed | Switch exists (`attribution`) | Fixture test only (see below) |

One software property related to ablation is verified. On fixture inputs, disabling attribution leaves every verdict unchanged (`test_ablating_attribution_leaves_the_verdict_unchanged`). This checks the audit-only status of attribution required by Chapter 3 (Section 3.7.6). It is not an empirical ablation result.

## 4.14 Error and Failure Analysis

No false positives, false negatives or agent-level failures can be analyzed, because no evaluation has been executed (RESULT NOT AVAILABLE). Every test in the verification run passed (E1). Table 4.16 records the failures and defects that are documented, observed in the verification runs, or evident from comparing the code with Chapter 3.

Table: Table 4.16. Observed and documented failures, defects and gaps

| ID | Observation | Evidence | Type |
|---|---|---|---|
| F-1 | The experiment runner stops with DESIGN BLOCKED; no experiment can run | E4 | Designed fail-closed behavior |
| F-2 | The Chapter 3 Detection Layer features and the Behavioral Analysis features are absent | E6 | Implementation gap |
| F-3 | No interface to an executing agent; AS-1 undemonstrated | E5, E6 | Implementation gap |
| F-4 | Modify cannot be executed; no mechanism is declared | `rem/core/mitigation.py`; test | Designed fail-closed behavior (SD-3; SC-1) |
| F-5 | An exact tie stops the engine | `rem/algorithms/decision/expected_loss.py`; test | Specification conflict (SC-2) |
| F-6 | The calibration ablation is refused | `rem/core/pipeline.py`; test | Specification conflict (SC-3) |
| F-7 | The calibration fitting objective and protocol differ from Eq. 3.4 and Procedure 3.1 | `rem/algorithms/calibration/platt.py` | Specification conflict (SC-4; earlier Defect D3) |
| F-8 | The loss grid is checked for completeness, not coherence or dominance | `rem/algorithms/decision/expected_loss.py` | Gap relative to Section 3.7.5 (earlier Defect D1) |
| F-9 | The feasible verdict set 𝒱(a_t) is not applied | same | Gap relative to Section 3.7.5 |
| F-10 | The historical project report of 139 contract-compliance tests was wrong; the verified number is 20 | `STAGE2_5_BASELINE_TEST_RECONCILIATION.md` | Reporting error, corrected |
| F-11 | The code cites four sources that are not in the thesis reference lists and have no verification record | E6 | SOURCE VERIFICATION REQUIRED |

## 4.15 Computational Cost

No latency, overhead or throughput of REM has been measured (RESULT NOT AVAILABLE). The functions for recording latency and computing its mean and sample quantiles exist (`rem/evaluation/runtime.py`) and are tested on fixed inputs. They have not been applied to REM processing an agent step. The 0.47-second duration of the test run (E1) measures the execution of 154 tests and is not a latency result.

Chapter 3 requires per-step latency, excluding LLM inference and tool execution, reported as median and 95th percentile (Table 3.15; security objective SO-6). This remains EVIDENCE REQUIRED. The latency of REM in its specified form will depend on the fixed prompt-injection classifier, which has not been chosen. No claim is made that REM operates in real time.

## 4.16 Alignment Between Chapter 3 and the Implementation

Table 4.17 summarizes the status of the main elements of Chapter 3. The specification conflicts SC-1 to SC-6 and the decisions they depend on are listed in the supervisor decision register that accompanies this chapter (`SUPERVISOR_DECISIONS_REQUIRED.md`). None has been resolved in this chapter.

Table: Table 4.17. Summary of implementation status against Chapter 3

| Chapter 3 element | Status |
|---|---|
| Five-layer architecture; no sixth layer | Implemented (layer labels differ, SC-6) |
| L1 provenance labeling, hygiene, entity extraction | IMPLEMENTATION NOT CONFIRMED |
| L2 context evidence (Table 3.8) | IMPLEMENTATION NOT CONFIRMED |
| L3 behavioral and action evidence (Table 3.9) | IMPLEMENTATION NOT CONFIRMED |
| Eq. 3.1 | Implemented (SOURCE NOT FULLY VERIFIED) |
| Eq. 3.2 | Implemented up to the penalty scaling constant (SOURCE NOT FULLY VERIFIED); λ selection IMPLEMENTATION NOT CONFIRMED |
| Eq. 3.3 | Implemented (SOURCE NOT FULLY VERIFIED) |
| Eq. 3.4 and out-of-fold calibration | Implemented differently (SC-4) |
| Tiers, predicates, loss structure, Eq. 3.5 | IMPLEMENTATION NOT CONFIRMED |
| Eqs. 3.6–3.7 | Implemented; tie order not implemented (SC-2); feasible set not applied |
| Eqs. 3.8–3.10 | Analytical; not runtime operations |
| Eqs. 3.11–3.12 | Implemented, audit-only |
| Eq. 3.13 | IMPLEMENTATION NOT CONFIRMED |
| Eq. 3.14, baseline B1 | IMPLEMENTATION NOT CONFIRMED |
| Eqs. 3.15–3.19, optional CUSUM | Not implemented; approval pending (SOURCE NOT FULLY VERIFIED for Eqs. 3.15–3.16) |
| Eqs. 3.20–3.22 | IMPLEMENTATION NOT CONFIRMED |
| Mitigation (Table 3.14) | Step-level only (SC-1) |
| Procedure 3.1, offline fitting | IMPLEMENTATION NOT CONFIRMED |
| AgentDojo integration; observe-only and enforcing modes | IMPLEMENTATION NOT CONFIRMED |
| Experiments, baselines, ablations, metrics on data | PLANNED — NOT EXECUTED; RESULT NOT AVAILABLE |

The evidence required before any result of Chapter 3's evaluation can be reported is, in dependency order:

1. Supervisor decisions on SD-FREEZE, SC-1 to SC-6 and the pending design values (SD-1 to SD-4, the classifier, the backbones, the benchmark version).
2. Implementation of the Input & Context, Detection and Behavioral Analysis evidence, the tier map, the predicates and the declared Modify mechanism.
3. Integration with a pinned AgentDojo version and a demonstration of AS-1.
4. Observe-only runs, label construction and its audit, and pilot E0.
5. Procedure 3.1 and the metric implementations.
6. Enforcing-mode runs for REM, B0 and B1, and the ablations.
7. Latency measurement on declared hardware.

## 4.17 Chapter Summary

This chapter reported the implementation of REM at commit `c22a97d` and the status of its evaluation. The implemented prototype preserves the five-layer architecture and the pipeline order of Chapter 3. It implements the following exactly as specified, with citations recorded in code:

- ridge logistic estimation (Equation 3.1);
- calibration on the logit with a positive slope (Equation 3.3);
- the conditional risk and argmin verdict (Equations 3.6–3.7);
- the audit-only linear attribution (Equations 3.11–3.12).

It refuses to run whenever a design input is missing, and 154 tests pass that verify these properties on fixture inputs.

The Input & Context, Detection and Behavioral Analysis evidence of Chapter 3 is not implemented. The consequence tiers, policy predicates, loss values and Modify mechanism are not implemented, and no connection to an executing agent exists. Six specification conflicts between Chapter 3 and the implementation remain open for supervisor decision:

- SC-1: mitigation semantics;
- SC-2: tie-breaking;
- SC-3: the calibration ablation;
- SC-4: the calibration fitting;
- SC-5: the Brier score;
- SC-6: the layer mapping.

The experimental design of Chapter 3 has not been executed. Consequently, this chapter reports no attack-success, utility, calibration, discrimination, intervention or latency result, and none of the research questions has been answered. Chapter 5 interprets this evidence within these limits.

## References

Chow, C. K. (1970). On optimum recognition error and reject tradeoff. *IEEE Transactions on Information Theory, 16*(1), 41–46. https://doi.org/10.1109/TIT.1970.1054406

Cox, D. R. (1958). The regression analysis of binary sequences. *Journal of the Royal Statistical Society: Series B (Methodological), 20*(2), 215–232. https://doi.org/10.1111/j.2517-6161.1958.tb00292.x

Debenedetti, E., Zhang, J., Balunović, M., Beurer-Kellner, L., Fischer, M., & Tramèr, F. (2024). *AgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents* (arXiv:2406.13352). arXiv. https://arxiv.org/abs/2406.13352

Elkan, C. (2001). The foundations of cost-sensitive learning. In *Proceedings of the Seventeenth International Joint Conference on Artificial Intelligence (IJCAI-01)*. https://cseweb.ucsd.edu/~elkan/rescale.pdf

Fawcett, T. (2006). An introduction to ROC analysis. *Pattern Recognition Letters, 27*(8), 861–874. https://doi.org/10.1016/j.patrec.2005.10.010

Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. In *Proceedings of the 34th International Conference on Machine Learning* (Vol. 70, pp. 1321–1330). PMLR. https://proceedings.mlr.press/v70/guo17a.html

Kull, M., Silva Filho, T., & Flach, P. (2017). Beta calibration: A well-founded and easily implemented improvement on logistic calibration for binary classifiers. In *Proceedings of the 20th International Conference on Artificial Intelligence and Statistics* (Vol. 54, pp. 623–631). PMLR. https://proceedings.mlr.press/v54/kull17a.html

le Cessie, S., & van Houwelingen, J. C. (1992). Ridge estimators in logistic regression. *Applied Statistics, 41*(1), 191–201. https://doi.org/10.2307/2347628

Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. In *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1705.07874

Platt, J. C. (1999). Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. In A. J. Smola, P. Bartlett, B. Schölkopf, & D. Schuurmans (Eds.), *Advances in large margin classifiers* (pp. 61–74). MIT Press.

*Note on sources cited in the implementation.* The code documentation also cites Hastie, Tibshirani and Friedman (2009), van Rijsbergen (1979), Hyndman and Fan (1996) and Shapley (1953). They are not in the thesis reference lists and have no project verification record, so they are not listed above. SOURCE VERIFICATION REQUIRED. The Platt (1999) entry is reproduced exactly as it appears in Chapter 3 and remains subject to citation conflict OI-07.
