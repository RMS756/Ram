# Code and Implementation Audit

**Code evaluated:**
- the `rem/` package: 44 Python files, 6,861 lines;
- the experiment scripts in `experiments/pilot/`;
- the tests in `tests/` (19 test modules).

**Revision:** commit `9ab3f9e`, branch `claude/rem-r4-corrections-3ktvze`.

**Checks performed on 1 Nov 2026 (read-only):**
- `python -m pytest -q`: 205 passed;
- `verify_equations.py`: 21 PASS lines, then ALL PASS;
- `trace_cells_R4.py`: 126 of 126 pass;
- line-by-line reading of the modules named below;
- an independent NumPy recomputation of the headline held-out metrics from the R4 re-run state.

No code was modified.

## 1. Methodology → code mapping

| Method element (Ch. 3) | Code location | Present? | Faithful? | Tested? | Used in results? | Notes |
|---|---|---|---|---|---|---|
| Provenance labelling, trust levels | `rem/algorithms/context/provenance.py` (`TrustLevel`, `trust_of`, `value_occurs_in`, `extract_ibans`) | Yes | Yes | Yes (`test_evidence`) | Yes | Value matching is string- and number-based. Entity extraction is partial: credentials and phone numbers are not handled (Ch. 4) |
| x_ctx1, injection classifier | — | **No** | — | — | — | Absent: no classifier was chosen (D-list). The Detection layer therefore reduces to a regex indicator |
| x_ctx2, instruction-pattern indicator | `detection/instruction_patterns.py` | Yes | Yes | Yes | Yes | The pattern set was written with knowledge of the benchmark's injection templates. Its group ROC is 0.582 (Ch. 5 E0) |
| x_beh1–x_beh4 | `behavior/evidence.py` `EpisodeTracker.features` | Yes | Yes, with interpretations I-2 to I-4 | Yes | Yes | x_beh3 (privilege escalation) fires on 92% of legitimate state-changing steps (Ch. 5 §5.7) |
| x_act1, argument provenance | `evidence.py` lines 238–247 | Yes | Yes | Yes | Yes | Fires when a key argument occurs in untrusted text and not in trusted text. **This is the dominant feature** (C-2) |
| x_act2, destination novelty | `evidence.py` lines 249–251 | Yes | **Weakened** | Yes | Yes | Implemented as "recipient not in the user objective" (I-5). This is not the novelty against benign history specified in Ch. 3 §3.6.2 (M-6) |
| x_act3, sensitive egress | `evidence.py` lines 253–257 | Yes | Yes, with interpretation I-6 | Yes | Yes | — |
| Ridge LR (Eqs. 3.1–3.2) | `detection/ridge_logistic.py` | Yes | Yes | Yes (`test_frozen_math`) | Yes | Newton method. The intercept is unpenalized and λ = λ_impl/2. **No line search, and the `converged` flag is never checked by any caller** (m-11) |
| Platt / logit calibration (Eqs. 3.3–3.4) | `calibration/platt.py`, `calibration/logit_nll.py` | Yes | Yes | Yes | Yes | Rejects γ₁ ≤ 0. Backtracking Newton. Platt targets vs label NLL is SC-4; both are reported |
| Consequence tiers, tier map | `decision/consequence.py` | Yes | Exploratory values | Yes | Yes | The tier map is not approved (C-4) |
| Predicates D1/D2 | `decision/policy.py`, `a3.py` | Yes | Yes | Yes | Yes | Π is empty. D2 (missing evidence → Escalate) fired on 58 steps |
| Loss grid, Eq. 3.5 | `decision/loss_matrix.py` `build_loss_grid` | Yes | Yes | Yes | Yes | r_mod comes from oracle replay (M-2) |
| Expected-loss verdict (Eqs. 3.6–3.7) | `decision/expected_loss.py`, `a3.py` `A3Policy.decide` | Yes | Yes | Yes | Yes | Exact-equality tie detection. `tie_mode` follows Ch. 3, whereas the frozen interface raises `VerdictTieError` (SC-2); 0 ties occurred |
| Thresholds and feasibility (Eqs. 3.8–3.10) | `expected_loss.py` | Yes | Yes | Yes | In reports | — |
| Linear SHAP, audit-only (Eqs. 3.11–3.13) | `attribution/linear_shapley.py` | Yes | Yes | Yes (`test_contract_compliance`: the verdict is unchanged when attribution is perturbed) | Audit field only | Consistent with the CLAUDE.md lock |
| B1 operating-threshold baseline (Eq. 3.14) | `a1.py`; thresholds in `crossfit.py` | Yes | Yes | Yes | Yes | Chosen on out-of-fold calibrated y = 0 steps of the fitting portion |
| CUSUM, observe-only (Eqs. 3.15–3.19) | `a2.py`, `behavior/cusum.py` | Yes | Yes | Yes | Observe-only | Not in the verdict path (verified) |
| Nested grouped cross-fitting (Proc. 3.1) | `evaluation/crossfit.py` `nested_crossfit` | Yes | Yes | Yes (`test_crossfit`) | Yes | **No leakage found.** Reference sets, λ, calibrator and B1 thresholds are all fitted on the fitting portion only |
| Grouped bootstrap | `evaluation/bootstrap.py` | Yes | Yes | Yes | Yes | 2,000 resamples, seed 20261027, over 9 attacked groups |
| Metrics (Eqs. 3.20–3.22) | `evaluation/metrics.py`, `probabilistic.py` | Yes | Yes | Yes | Yes | AUC, ECE and log-loss recomputed independently and matching |
| Mitigation, step-level | `integration/agentdojo_replay.py` `RemGuard._mitigate` | Yes | Mostly (see §3) | Yes (`test_replay`, `test_mitigation_semantics`) | Yes (reference) | Under step-level semantics, **Modify withholds the call**: its environment effect equals a step-level Block |
| Mitigation, episode-level | same file | Yes | Yes (Ch. 3 Table 3.14) | Yes | Yes (sensitivity, Table 5.11) | Block adds all of 𝒯_R to the restricted set |
| Frozen `DeterministicMitigationEngine` | `rem/core/mitigation.py` | Yes | Yes | Unit-tested | **No** | Not used in the evaluated path |
| Frozen five-layer `RemPipeline` | `rem/core/pipeline.py` | Yes | Yes | Unit-tested (`test_pipeline`) | **No** | All results come from `RemGuard` / `A3Policy` / `crossfit`. Two execution paths exist (disclosed, Ch. 4) |
| Audit record | `rem/core/audit.py`; `RemGuard` | Yes | Yes | Yes | Latency only | — |
| Human reviewer | — | **No** | — | — | Simulated | "Idealized" approves exactly the y = 0 steps; "no reviewer" turns escalations into Block |
| Live enforcing agent | `experiments/live/` (protocol only) | **No** | — | — | — | NOT EXECUTED |
| Labelling (reference match) | `integration/steps.py` `injection_entered`, `build_steps` | Yes | Proxy | Yes | Yes | Not audited by a human (C-3) |

## 2. Classification

The implementation is a **functional experimental implementation, evaluated offline and by replay.** It is **not a tested end-to-end security framework.**

| Classification level | Applies? | Reason |
|---|---|---|
| Conceptual | Exceeded | — |
| Prototype | Exceeded | — |
| Functional experimental implementation | **Yes** | Every analytical component runs and is tested. Results reproduce bit-for-bit across two re-executions (0 analytical differences in 6,057 values) |
| Tested end-to-end framework | **No** | No live agent was protected. The injection classifier and the human reviewer are absent. The frozen pipeline is not the evaluated path |
| Production-ready | **No** | The thesis does not claim it (Ch. 6 §6.1.4) |

## 3. Detailed findings

| ID | Finding | Severity | Basis |
|---|---|---|---|
| CI-1 | **Step-level Modify is operationally a Block.** The declared exploratory Modify mechanism ("withhold a_t and return a tool-restriction notice, no persistence") does not change the action. Under NO-ADAPT its effect on the environment is identical to a step-level Block (docstring, `agentdojo_replay.py` lines 18–22). Consequences: r_mod ≈ 0 is guaranteed (M-2), and the four-verdict architecture collapses in replay to {release, withhold}, with Modify vs Block distinguished only by a cost entry. The thesis should state this plainly wherever Modify results are interpreted | MAJOR | V (code) |
| CI-2 | `converged` is returned by the ridge and calibrator solvers but never checked. A non-converged fit would pass silently. The risk is low here (8 well-conditioned features and the penalty), but the fail-closed principle in CLAUDE.md implies a check | MINOR | V |
| CI-3 | Two execution paths. `RemPipeline` (frozen, five layers) is unit-tested only; the results come from `RemGuard` and `A3Policy` with cross-fit parameters. The equivalence of the two paths is not tested | MAJOR (for the "framework" claim) | D, V |
| CI-4 | x_act2 is reduced to "recipient not in objective". In this benchmark, attack recipients are the attacker IBAN, which appears only in injected content, so x_act1 and x_act2 nearly coincide with the label-generating mechanism | MAJOR (validity) | V |
| CI-5 | The labelling rule and x_act1 both rely on value occurrence in untrusted content. The label (reference match on the injection goal) and the decisive feature are related by construction. This does not count as leakage in the strict sense, because no held-out label is used, but it inflates apparent discrimination | MAJOR (construct validity) | V, C |
| CI-6 | The tests are good unit and contract tests (verdict invariance to attribution; fail-closed configuration; equation identities). There is no adversarial test (for example, attacker values paraphrased or split so that x_act1 does not fire) | MAJOR (security evaluation) | V |
| CI-7 | "205 tests" includes 6 tests of the thesis-build tooling (`test_docx_tables.py`); 199 test REM. Ch. 4 Table 4.1 says pytest 9.1.1, but 9.2.0 ran | MINOR | V |
| CI-8 | Fail-closed configuration: missing design inputs raise errors (`config/loader.py`, `test_config`). This is consistent with CLAUDE.md | Positive | V |
| CI-9 | Reproducibility is strong. Seeds are fixed, the environment is recorded, and there are two full re-executions with 0 analytical differences | Positive | V |

## 4. Is the code faithful to the methodology?

**Yes for the estimator, calibration, decision rule, attribution and evaluation protocol.** These were verified by reading the code and by recomputing the metrics independently.

**Partly for the features.** x_act2 is weakened; x_ctx1 is absent.

**Partly for mitigation.** Step-level Modify is equivalent to Block; the frozen engine is unused.

**No for the claim of a deployed runtime framework.** There is no live enforcement and no reviewer.

## 5. Changes required (by the student)

1. Either declare a real Modify mechanism that changes the action (for example, argument substitution from trusted context), or state that Modify is, in replay, a costed variant of Block. Then re-interpret RQ3 accordingly.
2. Add the simple provenance-rule baselines (x_act1; x_act1 ∨ x_act2) to the replay harness. This needs no new infrastructure.
3. Test the equivalence of `RemPipeline` and the evaluated path on a sample of steps, or retire one of the paths from the thesis claims.
4. Check `converged` and fail closed when a fit does not converge.
5. Add adversarial robustness tests for x_act1 (encoded, split or paraphrased destinations), so that the dependence on a benchmark artefact can be bounded.
