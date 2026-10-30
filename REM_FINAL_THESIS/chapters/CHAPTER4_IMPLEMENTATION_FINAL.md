# CHAPTER FOUR

# IMPLEMENTATION OF THE REM FRAMEWORK

## 4.1 Purpose and Scope of the Chapter

Chapter 3 specified REM as a five-layer runtime framework that selects one of four verdicts (Allow, Modify, Escalate, Block) for each tool call proposed by an LLM agent. The verdict minimizes expected loss under a calibrated probability of adversarial inducement and a declared consequence tier, and every verdict is recorded for audit.

This chapter reports how that specification was realized in software, how the software reaches the benchmark, and how it was verified. It distinguishes three kinds of verification throughout:
- **Unit verification:** a function computes what its equation states, on constructed inputs.
- **Integration verification:** the components operate together inside the benchmark's execution loop, and the benchmark's own checks behave as expected.
- **Security effectiveness:** whether REM reduces attack success at acceptable cost.

**This chapter establishes only the first two.** Chapter 5 reports the evidence on the third, and its limits.

Three rules governed the implementation:
1. **Fail closed.** A design value that has not been declared stops the software (`DesignNotSpecifiedError`) instead of being replaced by a default.
2. **No silent resolution.** Where Chapter 3 and the design decisions of Stage 2 disagree, both alternatives are implemented and selected explicitly. The correspondence is recorded in Section 4.12.
3. **Separation of decision and audit.** Attribution is computed after the verdict and cannot reach the decision function; this is enforced by the function's signature and checked by a test.

## 4.2 Software Environment

**Table 4.1. Software and hardware environment of the reported runs**

| Item | Value |
|---|---|
| Language | Python 3.11.17 |
| Numerical library | NumPy 2.4.6 |
| Benchmark | AgentDojo 0.1.35 (PyPI), banking suite; suite version v1 for execution |
| Recorded traces | AgentDojo repository `runs/`, commit `089ed468cf3ed0322acc66b0211f26d9d90dbf60` |
| Test framework | pytest 9.1.1 |
| Hardware | Linux container, 4 vCPU (Intel Xeon @ 2.80 GHz), 15 GB RAM |
| Independent re-execution (R3) | 30 Oct 2026, merged repository state, Python 3.11.17, NumPy 2.4.6, AgentDojo 0.1.35, Intel Xeon @ 2.10 GHz, 4 vCPU; see Section 4.11.2 |
| Code version of the reported results | git commit `84a8c21` (revision R2). The first run (commit `aa66f22`) gave identical analytical results; see Section 4.11 |

No machine-learning framework is used. The estimator, the calibrators and every metric are implemented directly in NumPy, so that each operation can be traced to its equation (Table 4.6).

## 4.3 Code Organization and Execution Paths

**Table 4.2. Code organization**

| Package | Content |
|---|---|
| `rem/core/` | Frozen pipeline skeleton (`RemPipeline`), interfaces, step-level mitigation engine, append-only audit log, result types |
| `rem/algorithms/detection/` | Ridge logistic regression (Eqs. 3.1–3.2); instruction-pattern indicator x^ctx₂ |
| `rem/algorithms/calibration/` | Platt calibration on the logit: smoothed-target fit (`PlattLogitCalibrator`) and label-NLL fit (`LabelNLLLogitCalibrator`, Eq. 3.4) |
| `rem/algorithms/context/` | Provenance labels, hygiene, entity extraction |
| `rem/algorithms/behavior/` | Evidence features (Tables 3.8–3.9); Bernoulli CUSUM (observe-only) |
| `rem/algorithms/decision/` | Expected-loss engine; consequence tiers; loss structure and dominance check; predicates and feasible set |
| `rem/algorithms/a3.py`, `a1.py`, `a2.py` | REM verdict rule; baseline B1; observe-only CUSUM analysis |
| `rem/evaluation/` | Discrimination and calibration metrics; grouped bootstrap; nested grouped cross-fitting |
| `rem/integration/` | AgentDojo trace loader, labeller, step builder, replay harness with the REM guard |
| `experiments/pilot/` | Experiment scripts and the reproduction script `run_all.sh` |

The names A1, A2 and A3 come from the project brief and do not denote three methodologies:
- **A3** is the REM verdict rule;
- **A1** is the consequence-independent baseline B1 (Chapter 3, Section 3.7.7);
- **A2** is the optional observe-only CUSUM (Chapter 3, Section 3.11.10).

**Layer of the estimator.** In this thesis the ridge estimator and the calibration map belong to the Decision Engine (Layer 4), as in Chapter 3 and Figure 3.1. The comments and layer constants of the frozen pipeline's code label the estimator as part of Detection (Layer 2). The label does not affect any computation, and the frozen code was not edited to change it.

**Two execution paths exist, and the experiments use only one of them.**

1. **The frozen pipeline** (`rem/core/pipeline.py`, `RemPipeline.evaluate_step`) chains injected components through the five layers. It is exercised by unit and contract tests. It is **not** the path that produced any result in Chapter 5.
2. **The evaluation path** (`rem/integration/agentdojo_replay.py`, `RemGuard.evaluate`, together with `rem/algorithms/a3.py`, `A3Policy.decide`) is the path used in every experiment. It calls the frozen components:
   - the fitted ridge coefficients;
   - the calibration map;
   - `ExpectedLossDecisionEngine.conditional_risk` for Eq. 3.6;
   - `LinearShapleyAttributor` for Eq. 3.11.

   It adds the Chapter 3 components the frozen pipeline lacks: features, tiers, predicates, feasible set and both mitigation semantics. Mitigation is implemented in `RemGuard._mitigate`, not in the frozen `DeterministicMitigationEngine`.

**Table 4.3. Entry points and call paths of each experiment**

| Experiment (Chapter 5) | Entry point | Call path |
|---|---|---|
| Dataset | `experiments/pilot/build_dataset.py` | `load_episode` → `build_steps` → `EpisodeTracker.features` → `ReferenceLabeler.label` → `ConsequenceTierMap.tier` |
| Pilot E0 | `e0_pilot.py` | `nested_crossfit` on each fold's fitting portion → `roc_auc` |
| E1 discrimination and calibration; ablation refits; grouping sensitivity | `run_main.py crossfit` | `Designer` (fold-specific x^beh₄) → `nested_crossfit` → `RidgeLogisticRegression.fit` → calibrator `fit` → `A1Thresholds.fit` |
| r~mod~ and replay validity | `run_main.py rmod` | `replay_episode` → `GuardedToolsExecutor.query` → `RemGuard.evaluate` (oracle Modify) |
| E2, E5 and E6 observe-only | `run_main.py observe` | `A3Policy.decide` / `A1Policy.decide` on held-out recorded steps |
| E4, E5 replay | `run_main.py replay` | `replay_episode` → `RemGuard.evaluate` → `A3Policy.decide` → `RemGuard._mitigate` |
| E3 CUSUM | `run_main.py a2` | `fit_a2` → `evaluate_episode` |
| Cross-template; recorded defenses | `run_main.py xt` | as E1 scoring, and as E4 replay |
| Breakdowns, replay failures, label-audit package | `r2_analyses.py` | stored state from the stages above |
| All of the above | `run_all.sh` | in order; writes `results/pilot_R2/` when `PILOT_RESULTS_DIR` is set |

## 4.4 Layer 1 — Input and Context

`rem/algorithms/context/provenance.py` implements the provenance rule of Chapter 3, Section 3.4.2:
- every segment is labelled trusted (system), semi-trusted (user) or untrusted (tool output);
- derived content takes the least-trusted label of its inputs;
- model-generated content has no channel label, so asking for one raises an error rather than guessing.

**Hygiene.** Zero-width, bidirectional and other Unicode format characters are removed from REM's copy of untrusted text (`strip_invisible`). The text the agent receives is not altered.

**Entity extraction** is partly implemented:

| Entity (Chapter 3, Section 3.4.3) | Status |
|---|---|
| Account identifiers | Implemented (IBAN pattern) |
| Monetary amounts | Implemented (numeric tokens) |
| User-profile values | Implemented for the values returned by the profile read |
| Tool names mentioned in text | Implemented, through the instruction-pattern indicator |
| Credential values | Not extracted as entities; a password argument is still traced to its source through argument provenance |
| Phone numbers and other profile identifiers | Not implemented separately |

A declared matching rule (`value_occurs_in`) links an argument value to the texts that contain it:
- numbers match numerically;
- strings match as case-insensitive substrings;
- strings shorter than three characters never match.

## 4.5 Layer 2 — Detection

**x^ctx₂ (instruction-pattern indicator)** is implemented by `InstructionPatternDetector`. It fires if a declared regular expression, or the name of a tool, occurs in new untrusted segments. The pattern set is declared in the pilot configuration, and the detector refuses to run without one. The configuration discloses that the author of the patterns knew the benchmark's templates.

**x^ctx₁ (pre-trained injection classifier) is not implemented.** The classifier choice is pending, and the candidate model's host was unreachable from the execution environment. The feature is absent from x~t~; it is not replaced by a substitute. The context evidence tested in Chapter 5 is therefore the instruction-pattern indicator only.

## 4.6 Layer 3 — Behavioral and Action Evidence

`rem/algorithms/behavior/evidence.py` implements x^beh₁–x^beh₄ and x^act₁–x^act₃ (Chapter 3, Table 3.9). An `EpisodeTracker` holds the episode history; it is reset at each episode start and never changes REM's parameters. Where Chapter 3 is silent, the module states an interpretation (Table 4.4), so that the reader can disagree with it.

**Table 4.4. Interpretations made where Chapter 3 is silent**

| ID | Question | Interpretation |
|---|---|---|
| I-1 | What is a "step" when the agent proposes several calls at once? | Each proposed call is a step; calls in one assistant message share one decision point |
| I-2 | Does x^beh₂ count refused calls? | Yes, because Chapter 3 states that retries raise x^beh₂ |
| I-3 | x^beh₃ at the first call | "Highest level so far" is the lowest level (0) |
| I-4 | x^beh₄ at the first call | Previous tool is a start symbol; start transitions belong to the reference set |
| I-5 | x^act₂ "transactions before first untrusted ingestion" | Observable only through untrusted tool outputs, so it reduces to "recipient not in the objective" |
| I-6 | x^act₃ "external recipient", "sensitive values" | Recipient differs from the user's own IBAN; sensitive values are identifiers and profile values from sensitive reads |
| I-7 | Availability of x^act₁ for predicate D2 | Unavailable when the tool has key arguments but the call carries none |
| I-8 | "Tool class" in episode-level Modify | The tool's action category (Table 3.7) within 𝒯~R~ |
| I-9 | Unavailable feature below k~D2~ | Takes the value 0 ("not observed") and is flagged in the audit record |

The benign transition set used by x^beh₄ must be estimated within each fold (Chapter 3, Section 3.11.6). Each step record therefore stores its transition, and x^beh₄ is recomputed for every fold's reference.

## 4.7 Layer 4 — Decision Engine

**Estimation.** `RidgeLogisticRegression` computes s = β₀ + βᵀx and p̃ = σ(s) (Eq. 3.1), fitted by Newton–Raphson with the intercept unpenalized. Fitting without a declared λ raises `DesignNotSpecifiedError`. The implementation minimizes NLL + (λ~impl~/2)‖β‖², so λ on the scale of Eq. 3.2 is λ~impl~/2 (Chapter 3, Section 3.7.1). Selected values are reported on both scales.

**Calibration.** Both calibrators compute p = σ(γ₁s + γ₀) and reject a fit with γ₁ ≤ 0. They differ only in the fitting target: labels (Eq. 3.4, the reference) or Platt's smoothed targets (sensitivity).

**Consequence tiers, predicates and feasible set.**
- `ConsequenceTierMap` maps each tool to its category and the call to a tier. A transfer with a missing or unparseable amount receives the above-limit tier.
- `PredicatePolicy` implements D1 and D2, and the feasible set (Modify only for tools in 𝒯~R~).
- `A3Policy.decide` applies D1 and D2 before the expected-loss rule. When a predicate applies, the risk table is recorded as *not applicable* and p is marked as not used.

**Verdict.** `A3Policy` computes R(v) for v ∈ 𝒱(aₜ) through the frozen `conditional_risk` and returns the minimizer. Ties are handled by an explicit `tie_mode`:
- `"raise"` reproduces the frozen behavior;
- `"record_chapter3_order"` applies the Chapter 3 order and marks the step as tied.

An option `exclude_from_expected_loss=(Escalate,)` produces the comparison configuration "REM without expected-loss Escalate" (Chapter 3, Section 3.7.7).

**Loss structure and dominance check.** `build_loss_grid` constructs Table 3.13 including Eq. 3.5, and `reachable_verdicts` reports any verdict that is never the unique minimizer.

**Baseline B1.** `operating_threshold` implements Eq. 3.14, and `A1Policy` applies it with the same estimator, calibration and predicates.

**Audit record.** For each step, `RemGuard.evaluate` writes:
- the tool name and a SHA-256 digest of its arguments, with the argument keys;
- the evidence vector and its availability;
- s, p̃ and p, and whether p was used;
- the tier, and the risk table or *not applicable*;
- the verdict, its source and the mitigation;
- the linear attributions with their additivity error;
- REM's processing time.

Raw argument values are not written.

## 4.8 Layer 5 — Mitigation, and What Happens at the Tool Boundary

Mitigation is applied before any tool executes. In `GuardedToolsExecutor.query`, each proposed call is evaluated by `RemGuard.evaluate`. If the call is released, `runtime.run_function` executes it. Otherwise it is not executed, and a tool-result message carrying the refusal or restriction notice is returned to the agent in its place. The replay tests check this directly: an oracle that blocks every labelled step leaves the benchmark's security check false, and the withheld steps appear in the audit record with their tool and argument digest.

**Both mitigation semantics are implemented** (Chapter 3, Table 3.14). Step-level semantics is the reference; the episode-level variant maintains a restriction set S for the episode. Under step-level semantics, Modify and Block have the same effect on the current call. Under the replay used in Chapter 5, the two semantics cannot differ, because a non-adaptive agent does not retry.

**Escalate.** No reviewer exists. Escalation is resolved by one of two bounds:
- an idealized reviewer, which releases the call if and only if its label is 0;
- no reviewer, in which the call is withheld.

**Correction made in revision R2.** In the frozen pipeline, the Block mechanism cleared the step's tool call before the audit record was written. The record therefore lost the identity of the blocked action. A test now reproduces the defect, and the fix keeps the tool name and argument digest in the step's metadata, without raw arguments. The audit record uses them. The fix does not change any verdict or mitigation, and it does not affect any result in Chapter 5, because the experiments use the evaluation path, in which mitigation never alters the proposed call, so the tool's identity was always recorded; the argument digest was added to that record in this revision.

## 4.9 Non-Invasive Placement and Its Limits

"Non-invasive" means here that **the agent's model, prompts and tools are not modified**: REM observes the messages the agent produces and the results the tools return. The placement has limits:
- **REM replaces the executor.** It must be inserted into the agent's execution loop, here as a subclass of the benchmark's `ToolsExecutor`. A framework in which tools are executed by a component REM cannot wrap is not covered.
- **Only executor calls are mediated.** Effects that do not pass through the tool executor (for example, a tool with side effects inside its own implementation, or a second agent) are outside REM's view.
- **Refusals are visible to the agent.** They are returned as tool-result messages. The agent's reaction to them is part of the system's behavior, and the replay analysis does not observe it.
- **Some context is inferred, not received.** In the evaluation, REM receives the objective and system prompt from the recorded trace. A deployment must supply them through the same channel.

## 4.10 Optional Sequential Analysis (A2)

`rem/algorithms/behavior/cusum.py` and `rem/algorithms/a2.py` implement the Bernoulli CUSUM of Chapter 3 (Eqs. 3.15–3.19). The module has no interface to the decision engine and returns no verdict; a test checks both properties.

An A2-driven enforcement policy and a retrained "A3 + A2" variant are not implemented, because they would place CUSUM in the verdict path.

## 4.11 Verification

### 4.11.1 Unit and contract verification

**Table 4.5. Test suite (executed on 28 Oct 2026: 193 passed with AgentDojo installed; 189 passed and 1 module skipped without it)**

| File | Tests | Verifies |
|---|---|---|
| `test_frozen_math.py` | 43 | Eqs. 3.1–3.3, 3.6; fail-closed fitting; γ₁ > 0; a tie raises |
| `test_contract_compliance.py` | 20 | Five layers, no sixth; frozen mitigation mapping; no equation IDs; forbidden components absent; attribution excluded from the decision signature |
| `test_metrics.py`, `test_probabilistic.py` | 25 + 5 | ROC-AUC against the pairwise definition; average precision; ECE binning (Eq. 3.20); log-loss; Brier conventions; grouped bootstrap |
| `test_pipeline.py` | 21 | Frozen pipeline order; step-level Block; **the blocked action's identity is kept in the audit record** (added in R2) |
| `test_mitigation.py`, `test_trajectory.py`, `test_config.py`, `test_reproducibility.py` | 9 + 12 + 15 + 9 | Step-level mitigation, configuration fail-closed, seeds |
| `test_a3.py` | 10 | Table 3.13; Eqs. 3.8–3.10; argmin over the feasible set; D1 and D2; ties; dominance check; **REM without expected-loss Escalate keeps D2** (added in R2) |
| `test_a1.py` | 5 | Eq. 3.14 minimality; α = 0; invariance under monotone recalibration; verdict rule |
| `test_a2.py` | 5 | Eqs. 3.15–3.17; indicator set; false-alarm target; no verdict |
| `test_evidence.py` | 7 | Trust order; hygiene; features on an injected and a legitimate transfer; availability; tier map |
| `test_crossfit.py` | 2 | Procedure 3.1 outputs; held-out predictions independent of held-out labels |
| `test_traces.py` | 2 | Label rule including induced reads and ambiguity; fold-specific x^beh₄ |
| `test_replay.py` | 3 | All-Allow replay reproduces a recorded episode; oracle Block prevents the recorded attack; **withheld calls keep tool and argument digest, and no raw attacker value appears in the audit record** (extended in R2); observe-only releases everything |

### 4.11.2 Integration verification

- **Replay fidelity.** With every call allowed, the replay reproduced the recorded utility and security outcome of 3,313 of 3,334 episodes (99.4%). The 21 exceptions are analyzed in Chapter 5.
- **Determinism and regression.** The complete pilot was run at commit `aa66f22` (R1) and again at commit `84a8c21` (R2), after the corrections of this revision. An automated comparison of the 5,121 values the two runs share found 93 differences, all of them wall-clock time or memory measurements; every analytical value was identical.
- **Independent re-execution (R3, 30 October 2026).** The complete pipeline (`run_all.sh`) was executed again, from the merged repository state, on a different processor and with the AgentDojo repository obtained afresh at commit `089ed468`. Of the 6,057 numeric values that the re-run shares with `results/pilot_R2/`, 5,943 were identical. The 114 that differed are all time or memory measurements, and 0 analytical values differed (`RESULTS_PROVENANCE_REPORT.md`).
- **Attribution additivity.** The audit record carries |φ₀ + Σφᵢ − s| for every replayed step.

### 4.11.3 What is not verified here

Security effectiveness against live agents is not verified; Chapter 5 states what the recorded-trace analyses can and cannot show.

## 4.12 Correspondence Between Requirements, Equations, Code, Tests and Results

**Table 4.6. Requirement → equation → function → test → result artifact**

| Requirement (Chapter 3) | Equation | Function | Test | Result artifact (`results/pilot_R2/`) |
|---|---|---|---|---|
| Logit and uncalibrated probability | 3.1 | `ridge_logistic.RidgeLogisticRegression.decision_function` | `test_frozen_math` | `e1_crossfit.json` (`pooled_uncalibrated`) |
| Ridge fit (λ = λ~impl~/2) | 3.2 | `RidgeLogisticRegression.fit` | `test_frozen_math` | `e1_crossfit.json` (`per_fold.*.lambda`, `lambda_chapter3_eq3_2_scale`) |
| Calibration map, γ₁ > 0 | 3.3 | `PlattLogitCalibrator.calibrate` | `test_frozen_math` | `e1_crossfit.json` (`gamma_1`) |
| Calibration fit on labels | 3.4 | `logit_nll.LabelNLLLogitCalibrator.fit` | `test_crossfit` | `e1_crossfit.json` (`label_nll_primary`) |
| Adversarial Modify loss | 3.5 | `loss_matrix.build_loss_grid` | `test_a3` | `e4_rmod_and_replay_validity.json` (r~mod~) |
| Conditional risk | 3.6 | `expected_loss.ExpectedLossDecisionEngine.conditional_risk` | `test_frozen_math`, `test_a3` | `e2_e5_e6_observe_only.json` |
| Verdict over 𝒱(aₜ), ties | 3.7 | `a3.A3Policy.decide` | `test_a3` | `e2_e5_e6_observe_only.json` (`ties`) |
| Thresholds, feasibility, dominance | 3.8–3.10 | `loss_matrix.*` | `test_a3` | `e2_e5_e6_observe_only.json` (`dominance`) |
| Attribution, additivity | 3.11–3.13 | `linear_shapley.LinearShapleyAttributor` | `test_frozen_math` | replay audit field `additivity_error` |
| Baseline thresholds | 3.14 | `a1.operating_threshold` | `test_a1` | `e1_crossfit.json` (`theta_blk`, `theta_mod`) |
| CUSUM | 3.15–3.19 | `cusum.BernoulliCusum`, `a2.*` | `test_a2` | `e3_a2_cusum_observe_only.json` |
| ECE, log-loss | 3.20–3.21 | `probabilistic.*` | `test_probabilistic` | `e1_crossfit.json` |
| Realized loss | 3.22 | `run_main.stage_observe` | — (script) | `e2_e5_e6_observe_only.json` (`e6_grid`) |
| D1/D2 before expected loss | — | `PredicatePolicy.evaluate`, `A3Policy.decide` | `test_a3` | `e2_e5_e6_observe_only.json` (`sources`) |
| Step- and episode-level mitigation | Table 3.14 | `RemGuard._mitigate` | `test_replay` | `e4_e5_enforcement_replay.json` |
| Audit identity of withheld actions | Section 3.7.6 | `RemGuard.evaluate`; `mitigation.py`, `audit.py` | `test_replay`, `test_pipeline` | — |

**Table 4.7. Components required, implemented and absent**

| Component (Chapter 3) | Status |
|---|---|
| Provenance labels, hygiene | Implemented |
| Entity extraction | Partly implemented (Section 4.4) |
| x^ctx₁ injection classifier | **Absent** |
| x^ctx₂, x^beh₁–₄, x^act₁–₃ | Implemented |
| Ridge estimator; both calibration fits | Implemented |
| Tiers, predicates, feasible set, loss structure, dominance check | Implemented |
| REM verdict; B1; REM without expected-loss Escalate | Implemented |
| Step-level and episode-level mitigation | Implemented (evaluation path) |
| Human reviewer | Absent; replaced by two bounds |
| Offline fitting (Procedure 3.1) | Implemented |
| CUSUM (observe-only) | Implemented |
| Live enforcing-mode execution | **Not executed** (no LLM access) |

## 4.13 Logging of Sensitive Values

- **Audit records.** The audit records of the evaluation path store argument digests and keys, not values. A test checks that neither the attacker's account identifier nor the attacker's password appears in any audit record of a replayed episode.
- **Frozen audit log.** It stores digests by default; raw payloads are written only if `record_payloads=True` is set explicitly.
- **Result files.** Two result files contain argument values copied from the benchmark's traces: the label-audit sample and the human label-audit package. These values are synthetic benchmark data (simulated IBANs and passwords), not real credentials.
- **Credentials.** No credential, API key or real account identifier is used by the code or written by it.

## 4.14 Runtime Measurement

REM's processing time is measured with `time.perf_counter` around `RemGuard.evaluate`. The measured interval **includes**:
- feature computation;
- scoring and calibration;
- the predicates and the verdict;
- the mitigation decision;
- audit-record construction with attribution.

It **excludes**:
- LLM inference (absent in replay);
- tool execution;
- benchmark environment set-up;
- pipeline overhead.

Measurements were taken in four parallel worker processes on the 4-vCPU container of Table 4.1, so they include contention between workers, and they vary between runs (Section 4.11.2). Memory is the peak allocation traced by `tracemalloc` during `RemGuard.evaluate`, measured on 300 episodes.

These figures describe the evaluated configuration: no injection classifier, no reviewer, and Python on this hardware. They do not describe a deployment that includes a neural classifier or a human review step.

## 4.15 Chapter Summary

The full runtime procedure of Chapter 3 is implemented in the evaluation path, except for the injection classifier, which is absent. The evaluation path inserts REM at the benchmark's tool boundary without modifying the agent. Its correspondence with the equations, tests and results is given in Table 4.6.

The frozen pipeline is verified by unit tests but is not the path used in the experiments. One defect in it, the loss of a blocked action's identity in the audit record, was corrected in this revision without effect on any result.

The software is verified by 193 tests and by an exact analytical reproduction of the pilot. Its security effectiveness is the subject of Chapter 5.
