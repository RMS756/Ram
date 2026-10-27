# Chapter 4: Audit Report and Traceability

**Chapter:** `CHAPTER4_IMPLEMENTATION_EXPERIMENTAL_DESIGN_RESULTS.md` / `.docx`
**Repository state:** HEAD `c22a97d` · **Date:** 24 September 2026
**Evidence files:** `evidence/E0`–`E6`

---

## 1. Audit result

| Check | Result |
|---|---|
| Content consistency with Chapters 2 and 3 (terminology) | Pass. The chapter uses the Chapter 3 terms throughout: layers, verdicts, p̃_t/p_t, SO-/AS-/TB- identifiers, B0/B1/B2, RQ1–RQ4. Where the code uses different labels (the code's layer labels; provenance categories), the difference is stated, not merged (SC-6; Table 4.6). |
| Architecture consistency | Pass. Exactly five layers. Calibration, attribution and offline fitting are not counted as layers. No sixth layer, feedback layer or operator node is introduced. |
| Algorithm consistency | Pass. Only the Chapter 3 algorithms are described. No algorithm is introduced. Differences between the code and Chapter 3 are reported as conflicts SC-1 to SC-6 or as IMPLEMENTATION NOT CONFIRMED. |
| Equation consistency | Pass. Five display equations (3.1, 3.3, 3.6, 3.7, 3.11) are reproduced verbatim from Chapter 3 with their Chapter 3 numbers. No new numbered equation. One elementary transformation is stated in text and justified: the penalty-scaling correspondence λ = λ_code/2 (Section 4.6.1), which Chapter 3 §3.7.1 itself covers. The verification status of Eqs. 3.1, 3.2, 3.3, 3.15 and 3.16 is kept as SOURCE NOT FULLY VERIFIED. |
| Reference consistency | Pass. Ten references, all reproduced exactly from the Chapter 3 reference list. Four sources cited only in code docstrings are named and flagged SOURCE VERIFICATION REQUIRED; they are not added to the reference list. |
| Implementation consistency | Pass. Every implementation claim names a file or a test, and every named test exists in E1 with status PASSED. |
| Result consistency | Pass. Every number traces to E1–E6 (Table 4.14). No empirical result is reported. |
| Cross-reference consistency | Pass. Tables 4.1–4.17 are numbered consecutively and referenced in the text. Chapter 3 section, table and equation references were checked against the Chapter 3 working file. |
| No-hallucination audit | Pass. No performance, security, latency or real-time claim. No dataset or sample count beyond the Chapter 3 task counts, which are reported with Chapter 3's "to be re-confirmed" caveat. The fixture test is explicitly not presented as security evidence. |
| Supervisor issues visible | Pass. SC-1 is in §4.7 and Table 4.8; SC-2 in §4.6.4; SC-3 in §4.2.4 and Table 4.15; SC-4 in §4.6.2; SC-5 in Table 4.12; SC-6 in §4.2.3 and Table 4.4. All are marked SUPERVISOR DECISION REQUIRED, and none is presented as resolved. |
| Proposed / implemented / configured / measured separation | Pass (Table 4.1). |

**Chapter status:** COMPLETE AS DOCUMENTATION OF THE CURRENT STATE. The results sections are, correctly, empty of empirical results. The chapter cannot be finalized as a results chapter until the evidence listed in §4.16 exists.

## 2. Traceability table

| Chapter statement / section | Source | Evidence type | Verification status | Notes |
|---|---|---|---|---|
| §4.1.1 REM has not been executed on an agent, benchmark or dataset | `data/` empty; no results directory; E4; E5 | Repository inspection; run output | Verified | |
| §4.1.1 154 passing tests | E1, E2 | Test run | Verified | |
| §4.1.3 Placement at the tool-execution boundary; AS-1, AS-10 | Chapter 3 §3.11.1, Table 3.3 | Chapter text | Verified against Chapter 3 | |
| §4.1.3 No adapter to AgentDojo; AgentDojo not installed | E5, E6 | Environment and inventory | Verified | |
| §4.1.4 Governance by `CLAUDE.md`; fail-closed exceptions | `CLAUDE.md`; `rem/core/interfaces.py`; `rem/config/loader.py` | Code and contract | Verified | |
| §4.1.4 Implementation 19 Sep, Chapter 3 22 Sep | `git log`; file dates | Repository metadata | Verified | Commit `1c18cdf` (implementation); Chapter 3 working file dated 22 Sep |
| Table 4.2 Environment | E5; `pyproject.toml` | Environment capture | Verified | |
| Table 4.3 Code organization | E6; source files | Inventory | Verified | |
| §4.2.3 Five layers, no feedback or risk-score layer | `rem/core/pipeline.py`; tests `test_exactly_five_frozen_layers`, `test_there_is_no_feedback_layer`, `test_no_feedback_sink_exists_anywhere`, `test_pipeline_has_no_risk_score_layer` | Code and tests | Verified (E1) | |
| Table 4.4 Layer assignment differences | `rem/core/pipeline.py` comments; Chapter 3 §3.2, Table 3.5 | Code versus chapter | Verified | SC-6 |
| §4.2.4 Stage order; attribution after mitigation | `rem/core/pipeline.py`; `test_attribution_runs_after_the_verdict` | Code and test | Verified | |
| §4.2.4 Causal evaluation | `Trajectory.prefix`; `test_evaluation_is_causal`, `test_prefix_is_causal` | Code and tests | Verified | |
| §4.2.4 Calibration ablation refused | `test_ablating_calibration_is_refused` | Test | Verified | SC-3 |
| §4.2.5, Table 4.5 Configuration counts | E3; `configs/*.yaml` | Run output; file inspection | Verified | 27 / 19 |
| §4.2.5 Four FROZEN-labeled parameters that Chapter 3 treats differently or defers | `configs/calibration.yaml`, `configs/experiment.yaml`; Chapter 3 §3.7.2, §3.12.2 | Configuration versus chapter | Verified | SC-4, SC-5 |
| Table 4.6 Input & Context status | `rem/agent/trajectory.py`; `rem/core/interfaces.py`; tests | Code and tests | Verified | |
| §4.4 Detection features not implemented | E6; `configs/detection.yaml`; Chapter 3 Table 3.8 | Inventory and configuration | Verified | |
| Table 4.7 Behavioral features not implemented | E6; Chapter 3 Table 3.9 | Inventory | Verified | |
| §4.6 19 operations, 0 equation IDs | E6; `docs/MATHEMATICAL_TRACEABILITY.md` | Generated report | Verified | |
| §4.6.1 Eq. 3.1 implementation; no threshold label; no imputation | `ridge_logistic.py`; `test_detector_emits_no_thresholded_label`, `test_detector_refuses_missing_features` | Code and tests | Verified. Eq. 3.1 source: IV (SOURCE NOT FULLY VERIFIED) | |
| §4.6.1 Penalty written as (λ/2)‖β‖²; λ required; λ = 0 rejected | `ridge_logistic.py` `_objective` and `fit`; tests | Code and tests | Verified | Rescaling equivalence: Chapter 3 §3.7.1 |
| §4.6.2 Eq. 3.3; γ₁ ≤ 0 rejected; logit required; calibrated-only decisions | `platt.py`; tests listed in text | Code and tests | Verified. Eq. 3.3 Platt attribution NC (OI-07) | |
| §4.6.2 Smoothed targets; single held-out split | `platt.py` `fit`; `configs/calibration.yaml` | Code | Verified | SC-4 |
| §4.6.3 Tiers and predicates not implemented; fail-closed behavior | `interfaces.py` placeholders; tests | Code and tests | Verified | |
| §4.6.4 Eqs. 3.6–3.7; loss-grid source and completeness checks; risk table recorded | `expected_loss.py`; tests listed in text | Code and tests | Verified. Elkan FV (Eq. 1 form); Chow IV | |
| §4.6.4 Tie raises `VerdictTieError` | `expected_loss.py`; `test_exact_tie_raises_rather_than_choosing` | Code and test | Verified | SC-2 |
| §4.6.4 Feasible set 𝒱(a_t) not applied | `argmin_verdict` iterates over all `Verdict` members | Code | Verified | |
| §4.6.5 Audit-record fields; 16-hex SHA-256 digests; append mode | `rem/core/audit.py` | Code | Verified | |
| §4.6.5 Eq. 3.11 base value; Eq. 3.12 test | `linear_shapley.py`; `test_local_accuracy_holds` | Code and test | Verified. Lundberg & Lee FV | |
| §4.6.6 Procedure 3.1 not implemented | E6 (no fold or cross-fitting code) | Inventory | Verified | |
| Table 4.8 Mitigation semantics | Chapter 3 Table 3.14, Algorithm 1; `rem/core/mitigation.py`; mitigation tests | Chapter text versus code | Verified | SC-1 |
| Table 4.9 Environment status | Chapter 3 §3.11.1–3.11.2; `configs/experiment.yaml`; E5 | Chapter, configuration, environment | Verified | |
| §4.9 Task counts 16 / 9 / 11; 144 combinations | Chapter 3 §3.11.2 | Chapter text | As reported in Chapter 3 (OI-14: counts confirmed from package source; version not pinned) | Carried with Chapter 3's re-confirmation caveat |
| Table 4.11 Baselines not implemented | E6 (no threshold-policy code) | Inventory | Verified | |
| Table 4.12 Metric implementation status | `rem/evaluation/*`; E6 | Code and inventory | Verified | |
| Table 4.13 No results for RQ1–RQ4 | E3, E4, E6 | Absence of artifacts | Verified | RQs [PD] |
| Table 4.14 Every number | E1–E6 | Artifacts | Verified | See §3 below |
| Table 4.15 Ablation support | `AblationSpec`; `experiments/run_experiment.py` `ablations()`; `test_ablating_attribution_leaves_the_verdict_unchanged` | Code and test | Verified | |
| Table 4.16 Defects D1–D3 | `STAGE2_FINAL_ALGORITHM_MATHEMATICAL_DECISION_REPORT.md` §14–16; `STAGE3_IMPLEMENTATION_AUDIT.md` N.1 | Project records | Verified against records | |
| Table 4.16 F-10 (139 vs 20) | `STAGE2_5_BASELINE_TEST_RECONCILIATION.md` §3 | Project record | Verified (E1 reproduces 20) | |
| §4.15 No latency measured | E6; absence of artifacts | Inventory | Verified | |

## 3. Result traceability (Chapter 4 numerical values)

| Result | Artifact / file | Exact source | Reproducible? | Notes |
|---|---|---|---|---|
| 154 tests collected | `evidence/E2_pytest_collection.txt` | `154 tests collected in 0.14s` | Yes | |
| 154 passed | `evidence/E1_pytest_verbose_run.txt` | `154 passed in 0.47s` | Yes | Duration is not REM latency |
| Per-file counts 43/25/21/20/15/12/9/9 | `evidence/E1_pytest_verbose_run.txt` | `grep -c "test_<file>.py::.*PASSED"` | Yes | |
| 27 FROZEN; 19 unresolved | `evidence/E3_dry_run/evidence-dryrun/readiness.json` | `frozen_parameters`, `unresolved_parameters` | Yes | |
| Per-file FROZEN/unresolved split (Table 4.5) | `configs/*.yaml` | `status` fields | Yes | Sums 27 / 19 |
| 7 unattached components | `readiness.json` | `unattached_components` | Yes | |
| Exit code 1, DESIGN BLOCKED | `evidence/E4_full_run_stdout.txt` | last lines | Yes | |
| 19 operations, 0 IDs | `evidence/E6_implementation_inventory.txt` | `count 19` | Yes | |
| 16-hex-character digests | `rem/core/audit.py` `content_digest` | `hexdigest()[:16]` | Yes | Code constant |
| Chapter 3 counts 16, 9, 11, 144 | Chapter 3 §3.11.2 | text | N/A (Chapter 3 inspection) | Not REM results |
| Seed 42 | `configs/experiment.yaml` | `random_seed.value` | Yes | Engineering convention |
| Python 3.11.15, NumPy 2.4.6, PyYAML 6.0.1, pytest 9.1.1, 4 processors, 15 GiB | `evidence/E5_environment.txt` | lines 1–9 | Yes, on the same image | |

## 4. Citation tracking

| Citation key | Source title | Source type | Verification status (Stage 1/2) | Where used | Claim supported |
|---|---|---|---|---|---|
| Chow (1970) | On optimum recognition error and reject tradeoff | Journal article | PARTIALLY VERIFIED (REF-011); equation code IV (OI-13) | §4.6.4 | Conceptual support for escalation (as in Chapter 3) |
| Cox (1958) | The regression analysis of binary sequences | Journal article | PARTIALLY VERIFIED (REF-012); IV (OI-12) | §4.6.1 | Source of Eq. 3.1 (as in Chapter 3) |
| Debenedetti et al. (2024) | AgentDojo | Preprint | VERIFIED (REF-014) | §4.8 | Benchmark named in Chapter 3 |
| Elkan (2001) | The foundations of cost-sensitive learning | Conference paper | VERIFIED (REF-017); FV Eq. 1 form | §4.6.4 | Expected-cost criterion behind Eq. 3.6 |
| Fawcett (2006) | An introduction to ROC analysis | Journal article | PARTIALLY VERIFIED (REF-018); CF-03 metadata only | §4.11 | Named as the code's citation for confusion-matrix definitions |
| Guo et al. (2017) | On calibration of modern neural networks | Conference paper | VERIFIED (REF-020); FV | §4.6.2 | Eq. 3.3 form and Eq. 3.4 |
| Kull et al. (2017) | Beta calibration | Conference paper | VERIFIED (REF-027); FV | §4.6.2 | Monotonicity condition of Eq. 3.3 |
| le Cessie & van Houwelingen (1992) | Ridge estimators in logistic regression | Journal article | PARTIALLY VERIFIED (REF-004); IV, penalty constant pending (OI-10) | §4.6.1 | Eq. 3.2 |
| Lundberg & Lee (2017) | A unified approach to interpreting model predictions | Conference paper | VERIFIED (REF-034); FV | §4.6.5 | Eq. 3.11 |
| Platt (1999) | Probabilistic outputs for support vector machines … | Book chapter | PARTIALLY VERIFIED (REF-041); NC; UNRESOLVED CITATION CONFLICT (OI-07) | §4.6.2 | Named as the Chapter 3 and code attribution of the calibration method; conflict preserved |
| Hastie, Tibshirani & Friedman (2009) | The Elements of Statistical Learning | Book | **No project record: SOURCE VERIFICATION REQUIRED** | §4.6.1 (code citation only) | Not relied upon; named as the code's citation |
| Shapley (1953) | A value for n-person games | Book chapter | **No project record: SOURCE VERIFICATION REQUIRED** | §4.6.5 (code citation only) | Not relied upon |
| van Rijsbergen (1979) | Information Retrieval | Book | **No project record: SOURCE VERIFICATION REQUIRED** | §4.11 (code citation only) | Not relied upon |
| Hyndman & Fan (1996) | Sample quantiles in statistical packages | Journal article | **No project record: SOURCE VERIFICATION REQUIRED** | Table 4.12 (named as "Hyndman & Fan definition 7") | Not relied upon |

## 5. Items the chapter could not complete (evidence required)

1. All empirical results (RQ1–RQ4; Tables 4.11–4.13, 4.15). RESULT NOT AVAILABLE.
2. Demonstration of AS-1 (interception without modifying the agent).
3. Experimental hardware.
4. Latency on declared hardware.
5. Pinned AgentDojo version and re-confirmed task counts (OI-14).
6. Decisions SC-1 to SC-6, SD-FREEZE and SD-STRUCT.
