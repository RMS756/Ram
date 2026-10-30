# CHAPTER FOUR

# IMPLEMENTATION OF THE REM FRAMEWORK

> **Status.** This chapter describes software that exists and has been executed. Every statement about behaviour is backed by a test or an executed run, which is named where it is made. Components fall into three classes:
>
> - **FROZEN:** the core fixed by the design lock;
> - **CH3-EXPLORATORY:** Chapter 3 specifications whose values or details await supervisor approval;
> - **HARNESS:** evaluation code that is not part of REM.
>
> Open conflicts with Chapter 3 are stated where they arise and collected in Section 4.13.

## 4.1 Purpose and Scope of the Chapter

Chapter 3 specified REM as a five-layer runtime framework that selects one of four verdicts (Allow, Modify, Escalate, Block) for each tool call proposed by an LLM agent.
- The verdict minimizes expected loss under a calibrated probability of adversarial inducement and a declared consequence tier.
- Every verdict is recorded for audit.

This chapter reports how that specification was realized in software. It covers three things:
1. the implementation of each layer;
2. the offline fitting procedure;
3. the integration with the AgentDojo banking environment (Debenedetti et al., 2024), which demonstrates assumption AS-1 (Chapter 3, Table 3.3).

The chapter makes no claim about security effectiveness; Chapter 5 reports the evaluation.

Three rules governed the implementation:
1. **Fail closed.** A design value that has not been declared stops the software (`DesignNotSpecifiedError`) instead of being replaced by a default.
2. **No silent resolution.** Where Chapter 3 and the design lock disagree, both alternatives are implemented, selected explicitly, and the disagreement is recorded (Section 4.13).
3. **Separation of decision and audit.** Attribution is computed only after the verdict and cannot reach the decision function (enforced by signature; Section 4.12).

## 4.2 Software Environment

**Table 4.1. Software and hardware environment of the reported runs**

| Item | Value |
|---|---|
| Language | Python 3.11.17 |
| Numerical library | NumPy 2.4.6 |
| Benchmark | AgentDojo 0.1.35 (PyPI), banking suite, suite version v1 for execution |
| Recorded traces | AgentDojo repository `runs/`, commit `089ed468cf3ed0322acc66b0211f26d9d90dbf60` |
| Test framework | pytest 9.1.1 |
| Hardware | 4 vCPU (Intel Xeon @ 2.80 GHz), 15 GB RAM, Linux container |
| REM code size | 6,806 lines (`rem/`), plus 1,298 lines of pilot scripts (`experiments/pilot/`) |
| Code version of reported results | git commit `aa66f22` |

No machine-learning framework is used. The estimator, the calibrator and every metric are implemented directly in NumPy, so that each operation can be traced to its equation in Chapter 3 (see `EQUATION_PROVENANCE_AUDIT.md`).

## 4.3 Code Organization

**Table 4.2. Code organization**

| Package | Content | Class |
|---|---|---|
| `rem/core/` | Pipeline skeleton, interfaces, step-level mitigation, append-only audit log, result types | FROZEN |
| `rem/algorithms/detection/` | Ridge logistic regression (Eqs. 3.1–3.2); instruction-pattern indicator x^ctx₂ | FROZEN / CH3-EXPLORATORY |
| `rem/algorithms/calibration/` | Platt calibration on the logit with Platt's smoothed targets; label-NLL fit (Eq. 3.4) | FROZEN / CH3-EXPLORATORY (SC-4) |
| `rem/algorithms/context/` | Provenance labelling, hygiene, entity extraction | CH3-EXPLORATORY |
| `rem/algorithms/behavior/` | Evidence features (Tables 3.8–3.9); Bernoulli CUSUM (observe-only) | CH3-EXPLORATORY |
| `rem/algorithms/decision/` | Expected-loss engine; consequence tiers; loss structure and dominance check; predicates and feasible set | FROZEN / CH3-EXPLORATORY |
| `rem/algorithms/a1.py`, `a2.py`, `a3.py` | B1 threshold baseline (A1); observe-only CUSUM analysis (A2); REM verdict (A3) | CH3-EXPLORATORY |
| `rem/algorithms/attribution/` | Linear Shapley attribution (audit-only) | FROZEN |
| `rem/evaluation/` | Discrimination, calibration and runtime metrics; grouped bootstrap; nested grouped cross-fitting | CH3-EXPLORATORY |
| `rem/integration/` | AgentDojo trace loader, labeller, step builder, replay harness | HARNESS |
| `configs/` | Frozen configuration (fail-closed); `configs/exploratory/` pilot design and amendments | — |
| `experiments/pilot/` | Pilot runner, figures, reproduction script | HARNESS |

The three names A1, A2 and A3 come from the project brief. They do **not** denote three independent methodologies, which the design lock excludes:
- **A3** is the REM verdict rule;
- **A1** is the consequence-independent baseline B1 of Chapter 3, Section 3.7.7;
- **A2** is the optional, observe-only CUSUM analysis of Chapter 3, Section 3.11.10.

## 4.4 Layer 1 — Input and Context

`rem/algorithms/context/provenance.py` implements the provenance rule of Chapter 3, Section 3.4.2:
- every context segment is labelled trusted (system), semi-trusted (user) or untrusted (tool output);
- derived content takes the least-trusted label of its inputs (`least_trusted`);
- model-generated content has no channel label and must be labelled by inheritance, so `trust_of(Provenance.MODEL)` raises an error instead of guessing.

Before any further processing, untrusted text is stripped of zero-width, bidirectional and other Unicode format characters (`strip_invisible`).

Entity extraction covers:
- account identifiers, by an IBAN pattern;
- numeric amounts.

A declared matching rule (`value_occurs_in`) links an argument value to the texts that contain it:
- numbers match numerically;
- strings match as case-insensitive substrings;
- strings shorter than three characters never match, so that trivial values cannot create provenance links.

## 4.5 Layer 2 — Detection

**x^ctx₂ (instruction-pattern indicator).** This is implemented by `InstructionPatternDetector`.
- The indicator fires if any declared regular expression, or the name of any tool, occurs in new untrusted segments.
- The pattern set is not a default: it is declared in the pilot configuration, and the detector refuses to run without one.
- The pilot declares five patterns covering three kinds of text:
  - imperatives addressed to an assistant;
  - "ignore previous instructions" phrasings;
  - role or delimiter markers.
- The configuration discloses that the author of the patterns knew the benchmark's templates. Chapter 5 tests this through the context ablation and the cross-template check.

**x^ctx₁ (pre-trained injection classifier) is not implemented.**
- The classifier choice is pending supervisor approval (SD-DET).
- The candidate model's host was unreachable from the execution environment.
- The feature is therefore absent from x_t, not replaced.

## 4.6 Layer 3 — Behavioral and Action Evidence

`rem/algorithms/behavior/evidence.py` implements the features of Chapter 3, Table 3.9:
- x^beh₁ to x^beh₄;
- x^act₁ to x^act₃.

An `EpisodeTracker` holds the episode history H_t. It is reset at each episode start and never changes REM's parameters. Chapter 3 leaves seven details open; each is resolved by a stated interpretation in the module, listed in Table 4.3 so that the reader can disagree with it.

**Table 4.3. Interpretations made where Chapter 3 is silent**

| ID | Question | Interpretation |
|---|---|---|
| I-1 | What is a "step" when the agent proposes several calls at once? | Each proposed call is a step; calls in one assistant message share one decision point |
| I-2 | Does x^beh₂ count refused calls? | Yes, because Chapter 3 states that retries raise x^beh₂ |
| I-3 | x^beh₃ at the first call | "Highest level so far" is the lowest level (0) |
| I-4 | x^beh₄ at the first call | Previous tool is a start symbol; start transitions belong to the reference set |
| I-5 | x^act₂ "transactions before first untrusted ingestion" | Observable only through untrusted tool outputs, so the feature reduces to "recipient not in the objective" |
| I-6 | x^act₃ "external recipient", "sensitive values" | Recipient differs from the user's own IBAN; sensitive values are identifiers and profile values from sensitive reads |
| I-7 | Availability of x^act₁ for predicate D2 | Unavailable when the tool has key arguments but the call carries none |

All declared quantities are supplied by the caller; the module has no defaults:
- n_max;
- the key arguments per tool;
- the privilege map;
- the sensitive-read tools;
- the benign reference transition set.

**The benign transition set must be estimated within each fold** (Chapter 3, Section 3.11.6). Each step record therefore stores its transition, and x^beh₄ is recomputed for every fold's reference (`rem/integration/steps.py`, `design_matrix`).

## 4.7 Layer 4 — Decision Engine

### 4.7.1 Estimation (FROZEN)

`RidgeLogisticRegression` computes s = β₀ + βᵀx and p̃ = σ(s) (Eq. 3.1). It is fitted by Newton–Raphson on the penalized negative log-likelihood, with the intercept unpenalized.
- The penalty λ has no default; fitting without it raises `DesignNotSpecifiedError`.
- **Mismatch M1.** The code minimizes NLL + (λ/2)‖β‖², whereas Chapter 3 Eq. 3.2 writes λ‖β‖². The two are equivalent under rescaling of λ. The pilot reports λ on the code's scale, and the alignment is a pending decision.

### 4.7.2 Calibration (FROZEN form; fitting target pending, SC-4)

Both calibrators compute p = σ(γ₁s + γ₀) and reject any fit with γ₁ ≤ 0 (`MonotonicityViolationError`), as required for the monotone interpretation. They differ only in the fitting targets:
- `PlattLogitCalibrator` (frozen) fits against Platt's smoothed targets;
- `LabelNLLLogitCalibrator` fits by the label negative log-likelihood of Chapter 3 Eq. 3.4, using damped Newton steps so that quasi-separable calibration sets do not diverge.

Neither is adopted. Chapter 5 reports both.

### 4.7.3 Consequence tiers, predicates and feasible set (CH3-EXPLORATORY)

**Tier map.** `ConsequenceTierMap` maps each tool to its action category (Chapter 3, Table 3.7) and the call's descriptors to a tier (Table 3.11).
- A value transfer whose amount is missing or unparseable receives the above-limit tier: an unknown amount is not treated as small.
- Consequence descriptors never enter the probability model.

**Predicates.** `PredicatePolicy` implements D1 (prohibited action → Block) and D2 (required evidence unavailable at tier ≥ k_D2 → Escalate).

**Feasible set.** The feasible set 𝒱(aₜ) contains Modify only for tools in 𝒯_R.

**Mismatch M4.** The frozen `argmin_verdict` ranges over all four verdicts. The feasible set is therefore enforced in A3 (Section 4.7.5), without editing the frozen engine.

### 4.7.4 Loss structure and dominance check

`build_loss_grid` constructs L(v, y, k) exactly as Chapter 3 Table 3.13, including the derived adversarial Modify entry r_mod(k)·C_miss(k) (Eq. 3.5). The same module implements:
- the indifference thresholds of Eq. 3.8;
- the Allow–Block threshold of Eq. 3.9;
- the escalation feasibility condition of Eq. 3.10;
- the dominance check of Section 3.7.5 (`reachable_verdicts`).

Because each conditional risk is affine in p, the dominance check tests the endpoints, every pairwise intersection and the midpoints between them. It reports any verdict that is never the unique minimizer.

### 4.7.5 Verdict selection (A3 = REM)

`A3Policy.decide` applies D1, then D2. If neither fires, it computes R(v) for every v ∈ 𝒱(aₜ) with the frozen `ExpectedLossDecisionEngine.conditional_risk` (Eq. 3.6) and returns the minimizer (Eq. 3.7).

Ties are the unresolved conflict SC-2. `tie_mode` makes the choice explicit:
- `"raise"` reproduces the frozen behaviour (`VerdictTieError`);
- `"record_chapter3_order"`, used only in the exploratory pilot, applies the Chapter 3 order Block ⪰ Escalate ⪰ Modify ⪰ Allow and marks the step as tied, so that ties can be counted.

The pilot recorded no ties (Chapter 5).

### 4.7.6 Baseline B1 (A1)

`operating_threshold` implements Eq. 3.14: the smallest threshold whose false-positive rate on benign validation probabilities does not exceed α. The candidate set includes a value just above the largest benign probability, so that α = 0 is attainable.

`A1Policy` uses the same estimator, calibration and predicates as REM, and ignores tiers by construction:
- Block above θ(α_blk);
- Modify between θ(α_mod) and θ(α_blk) where feasible, otherwise Block;
- Allow below θ(α_mod).

### 4.7.7 Audit record and attribution (FROZEN; audit-only)

For each step the audit record contains:
- the evidence vector and its availability;
- s, p̃, p and the tier;
- the risk table, the verdict and its source;
- the mitigation and the restriction set;
- the linear Shapley attributions φᵢ = βᵢ(xᵢ − x̄ᵢ) with base value φ₀;
- the additivity error |φ₀ + Σφᵢ − s|;
- REM's processing time.

x̄ is estimated on benign fitting data of the step's fold.

## 4.8 Layer 5 — Mitigation

**Frozen semantics.** The frozen `DeterministicMitigationEngine` implements step-level semantics:
- Allow releases the current action;
- Block prevents it;
- Escalate withholds it;
- Modify applies one declared mechanism. That mechanism is undeclared in the design lock, so Modify raises `DesignNotSpecifiedError` in the frozen pipeline.

**Episode-level semantics.** Chapter 3 specifies episode-level semantics (Table 3.14): Modify removes the tool class of aₜ for the rest of the episode, and Block restricts every tool in 𝒯_R. This is conflict SC-1. The design lock forbids redefining the frozen mechanisms silently, so the episode-level semantics exist only in the evaluation harness, as an explicitly named variant (Section 4.10). The frozen enumeration of mitigation actions is unchanged, and a contract test confirms this.

## 4.9 Offline Fitting (Procedure 3.1)

`rem/evaluation/crossfit.py` implements lines 1–9 of Procedure 3.1. For each outer fold f:
1. The design matrix is rebuilt with the benign reference estimated only on the fitting portion.
2. λ is selected from a declared grid by grouped inner cross-validation on held-out log-loss (ties go to the stronger penalty).
3. Out-of-fold logits from the inner fits with the selected λ are used to fit (γ₁, γ₀).
4. A fit with γ₁ ≤ 0 is recorded as a calibration failure for the fold.
5. The estimator is refitted on the whole fitting portion.
6. The B1 thresholds are selected on out-of-fold calibrated probabilities of y = 0 fitting steps.
7. The held-out fold is scored.

Inner folds re-estimate the benign reference without their held-out groups, so the out-of-fold logits used for calibration are not optimistically biased on x^beh₄.

A unit test confirms that held-out predictions are independent of held-out labels: flipping every label in one fold leaves that fold's predictions unchanged (`tests/test_crossfit.py`).

## 4.10 Integration with AgentDojo (HARNESS)

### 4.10.1 Recorded traces and labels

`rem/integration/agentdojo_traces.py` loads AgentDojo's recorded traces without modification. They are traces of real LLM agents, produced by the benchmark authors.

Labels follow the reference-match rule of Chapter 3 Section 3.11.3:
- y = 1 when the injection task's reference solution contains the proposed tool **and** the attacker's key argument matches;
- the reference solutions are read from the installed AgentDojo package, not hard-coded;
- induced read steps are labelled 0 in the primary analysis, with a flag for the sensitivity variant.

The function `ambiguous_pairs` finds task pairs whose legitimate solution satisfies the label rule. It found one, (user_task_15, injection_task_4): the user's own new payee is the attacker's account (amendment AM-1, Chapter 5).

### 4.10.2 Placement at the tool boundary (AS-1)

REM is inserted into AgentDojo's own agent pipeline as a subclass of the benchmark's `ToolsExecutor`. Every proposed call is evaluated before execution, and every tool result is ingested as untrusted content on return. Neither the agent, its prompts nor the benchmark's tools are modified. This demonstrates AS-1 on this platform.

All calls run against AgentDojo's simulated banking environment. REM never initiates a call of its own.

### 4.10.3 Recorded-trace replay and its conflict with Chapter 3

No LLM API is available in the execution environment, so live enforcing-mode runs (Chapter 3 Section 3.11.1) could not be executed. Instead, enforcement was estimated by **replaying** recorded trajectories:
- a replay element emits the recorded assistant messages in order;
- the benchmark executes them under REM;
- the benchmark's own utility and security checks score the result.

The replay assumes that the agent does not adapt to a refusal (NO-ADAPT).

**This method is listed as out of scope in Chapter 3 Section 3.1.4** ("Counterfactual estimation of intervention value by replaying agent trajectories"). The conflict was identified after the runs. It is recorded as SC-7 for supervisor decision, and every replay-derived result in Chapter 5 is labelled accordingly.

The replay itself is validated: with every call allowed, it reproduced the recorded utility and security outcomes of 3,313 of 3,334 episodes (99.4%).

## 4.11 Optional Sequential Analysis (A2)

`rem/algorithms/behavior/cusum.py` and `rem/algorithms/a2.py` implement the Bernoulli CUSUM of Chapter 3 Eqs. 3.15–3.19:
- q₀ is estimated on benign fitting steps, with a declared floor;
- q₁ is declared over a grid;
- the threshold is the smallest value meeting the per-episode false-alarm target on benign fitting episodes.

The module has no interface to the decision engine and returns no verdict; a test checks both properties.

An A2-driven enforcement policy and a retrained "A3+A2" variant, named in the project brief, are not implemented. Both would place CUSUM in the verdict path, which the design lock forbids; they are listed as supervisor decisions.

## 4.12 Verification

**Table 4.4. Test suite (executed 27 Oct 2026; 192 passed)**

| File | Tests | What is verified |
|---|---|---|
| `test_frozen_math.py` | 43 | Eqs. 3.1–3.3, 3.6; fail-closed fitting; γ₁ > 0; tie raises |
| `test_contract_compliance.py` | 20 | Five layers, no sixth; frozen mitigation mapping; no equation IDs; forbidden components absent; attribution excluded from decision signature |
| `test_metrics.py`, `test_probabilistic.py` | 25 + 5 | ROC-AUC against pairwise definition; AP; ECE binning of Eq. 3.20; log-loss; Brier conventions; grouped bootstrap |
| `test_pipeline.py`, `test_mitigation.py`, `test_trajectory.py`, `test_config.py`, `test_reproducibility.py` | 21 + 9 + 12 + 15 + 9 | Frozen pipeline, step-level mitigation, configuration fail-closed, seeds |
| `test_a3.py` | 9 | Table 3.13 rows; Eqs. 3.8–3.10; argmin over feasible set; D1/D2; ties raise or are recorded; dominance check |
| `test_a1.py` | 5 | Eq. 3.14 minimality; α = 0; invariance under monotone recalibration; verdict rule |
| `test_a2.py` | 5 | Eqs. 3.15–3.17; indicator set; false-alarm target; no verdict |
| `test_evidence.py` | 7 | Trust order; hygiene; features on an injected and a legitimate transfer; availability; tier map |
| `test_crossfit.py` | 2 | Procedure 3.1 outputs; held-out independence of held-out labels |
| `test_traces.py` | 2 | Label rule incl. induced reads and ambiguity; step records and fold-specific x^beh₄ |
| `test_replay.py` | 3 | All-Allow replay reproduces a recorded episode; oracle Block prevents the recorded attack; observe-only releases everything |

Two further properties were verified by execution rather than by unit test:
- **Determinism.** A complete second run of the pilot from commit `aa66f22` reproduced every reported number exactly.
- **Attribution additivity.** The audit record logs |φ₀ + Σφᵢ − s| for every replayed step.

## 4.13 Alignment Between Chapter 3 and the Implementation

**Table 4.5. Alignment status**

| Item | Chapter 3 | Implementation | Status |
|---|---|---|---|
| M1 | λ‖β‖² | (λ/2)‖β‖² | Equivalent under rescaling; decision pending |
| SC-1 | Episode-level Modify/Block | Frozen: step-level; harness: both variants | Both run; unresolved |
| SC-2 | Ties → Block ⪰ … ⪰ Allow | Frozen: raise; A3: explicit `tie_mode` | Unresolved; 0 ties in pilot |
| SC-3 | Calibration ablation uses p̃ | Frozen pipeline refuses; harness runs it | Unresolved |
| SC-4 | Eq. 3.4 label NLL | Frozen: smoothed targets; both implemented | Unresolved |
| SC-5 | Brier withheld | Binary and two-class reported with convention | Unresolved |
| SC-6 | Estimation in L4 | Frozen code labels estimator "L2 Detection" | Documentation; unresolved |
| SC-7 | Replay out of scope | Enforcement estimated by replay | **Conflict; unresolved** |
| M4 | Argmin over 𝒱(aₜ) | Frozen argmin over all verdicts; A3 restricts | Implemented in A3 |
| x^ctx₁ | Pre-trained classifier | Absent | BLOCKED (SD-DET; host unreachable) |
| I-1 to I-7, AM-2, AM-3 | Silent | Stated interpretations | Pending approval |

## 4.14 Chapter Summary

The full runtime procedure of Chapter 3 (Algorithm 1) is implemented, with two exceptions:
- the injection classifier is blocked;
- the episode-level mitigation semantics exist as a harness variant, pending SC-1.

The offline fitting of Procedure 3.1 is implemented, and REM was placed at AgentDojo's tool boundary without modifying the agent (AS-1). The software is verified by 192 tests and by an exact reproduction of the pilot.

Ten alignment items remain open, the most consequential being SC-7: enforcement was estimated by a replay method that Chapter 3 excludes. Chapter 5 reports what the implementation produced on recorded agent traces, under that label.

## References

Debenedetti, E., Zhang, J., Balunović, M., Beurer-Kellner, L., Fischer, M., & Tramèr, F. (2024). AgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents. In *Advances in Neural Information Processing Systems 37*. https://doi.org/10.52202/079017-2636

Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. In *Proceedings of the 34th International Conference on Machine Learning* (Vol. 70, pp. 1321–1330). PMLR.

le Cessie, S., & van Houwelingen, J. C. (1992). Ridge estimators in logistic regression. *Applied Statistics, 41*(1), 191–201. https://doi.org/10.2307/2347628

Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. In *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1705.07874

Page, E. S. (1954). Continuous inspection schemes. *Biometrika, 41*(1–2), 100–115. https://doi.org/10.1093/biomet/41.1-2.100
