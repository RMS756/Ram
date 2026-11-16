# Claim audit and change log

## 1. Claim audit

Status words: **IMPLEMENTED** (code exists and is tested), **EXECUTED** (run in this study), **REPRODUCED** (earlier evidence re-run and matched), **DEVELOPMENT-ONLY** (evidence from exposed data), **PROPOSED**, **BLOCKED**, **NOT ESTABLISHED**.

| # | Claim | Status | Evidence |
|---|---|---|---|
| 1 | The integration package of 16 November reproduces from pinned sources | REPRODUCED | `00_SOURCE_OF_TRUTH_AND_REPRODUCTION.md`: 123,776 replays, per-episode outcomes identical; fits within 3.2e-14 |
| 2 | The table of earlier results in the task description is correct | REPRODUCED | regenerated `results.json`, `value_guard_results.json` |
| 3 | The Progent paper (v3) was read in full | EXECUTED | `01_PROGENT_READING_NOTE.md`, page anchors |
| 4 | The manual banking policy (PG) is not a configuration of paper v3 | EXECUTED (code inspection) | repository commits `9befb41`, `8a8eb89` |
| 5 | Progent's released subset check had a gap until 15 November 2026 | EXECUTED (code inspection; not reproduced by execution) | commit `0d7ea07`, message and diff |
| 6 | Three new candidate families were implemented behind the unchanged front: NP cutoff, CRC cutoff, gradient-boosted estimator | IMPLEMENTED, EXECUTED | `experiments/competitive_study/`; 107 + 15 tests |
| 7 | The protocol was committed before any fit or outcome of the new arms | EXECUTED | commit `3710267` precedes `11de6a4` |
| 8 | The guard alone (GV) has the same outcomes as HV and as NP05, CRC05, CRC01, GB, HVnc, HV4 on all three evaluations, the probe and the fixtures | EXECUTED, DEVELOPMENT-ONLY | `03_RESULTS_TABLES.md`, Tables 1-7 |
| 9 | Every attack-labelled restricted call is stopped by the authority front (907 and 559) | EXECUTED, DEVELOPMENT-ONLY | Table 5 |
| 10 | The learned model of L4/HV adds value over the deterministic guard | **NOT ESTABLISHED**; matched by GV. Not evidence that a learner cannot help | Tables 4, 5, 6 |
| 11 | GV improves on REM v1.0 | EXECUTED, DEVELOPMENT-ONLY (interval above zero on all three evaluations for completion; attack interval below zero on the primary recordings) | Table 4 |
| 12 | GV adds value over the strict rule G3 | **NOT ESTABLISHED** (lower bounds exactly zero) | Table 4 |
| 13 | Any arm is better than, equivalent to or non-inferior to PG | **NOT ESTABLISHED**; no margin exists | Table 4 |
| 14 | Any statement about Progent with generated or updated policies, its approvers or live agents | **BLOCKED** (no model credential, no spending limit); nothing run | `08_PROGENT_FULL_FRAMEWORK_PLAN.md` |
| 15 | The NP or CRC cutoff carries a formal guarantee for REM | **NOT CLAIMED**; assumptions not met | `PROTOCOL.md`, Section 6; Table 10 |
| 16 | The CRC cutoff transfers to an unseen attacker objective | Contradicted on development data (above its level in 7 and 5 objectives of 9) | Table 10 |
| 17 | Gradient boosting predicts better than the ridge estimator | Contradicted on development data | Table 9 |
| 18 | Gradient boosting keeps REM's linear attribution | **NOT CLAIMED**; no explanation method implemented for it | registry |
| 19 | Cedar can carry the front's constraints with decision parity | EXECUTED, DEVELOPMENT-ONLY (7,098 calls, 0 differences) | Table 13 |
| 20 | Cedar improves security or utility, or provides a guarantee about expansion | **NOT CLAIMED** | `11_RELATED_WORK_PROPOSALS.md` |
| 21 | A provenance rule on value-unconfirmed calls adds value | **NOT ESTABLISHED** (no attack reaches that stage; 27 and 6 legitimate calls withheld) | Table 13 |
| 22 | REM implements FIDES, CaMeL or IsolateGPT | **NOT CLAIMED**; none implemented | `11_RELATED_WORK_PROPOSALS.md` |
| 23 | Selective classification with guaranteed risk was evaluated | NOT IMPLEMENTED (source unreadable; no official code found) | registry |
| 24 | The mathematical sources were read in full | **NOT DONE** for the four method papers (hosts blocked); authors' or library implementations were read instead | registry, last column |
| 25 | Prospective validation on independently authored requests | PROPOSED, **NOT EXECUTED** | `07_PROSPECTIVE_VALIDATION_KIT.md` |
| 26 | Results generalize beyond the benchmark's 16 requests and 9 attacker objectives | **NOT ESTABLISHED** | all exposed data |
| 27 | Zero observed attacks means zero risk | **NOT CLAIMED** | |
| 28 | Anything was pushed, published or merged | Not done; local commits only | `git log` of branch `claude/rem-competitive-study-20261116` |

## 2. Equation-to-code mapping

| Published procedure | Source read | Code | Test |
|---|---|---|---|
| NP umbrella rank: smallest k with P(Bin(n, 1 − alpha) ≥ k) ≤ delta; cutoff = k-th order statistic of the left-out controlled-class scores | nproc 2.1.5, `R/npfuns.R`, `npc.core`, lines 92-96 | `candidates.np_order_index`, `candidates.np_release_cutoff` | `test_np_order_index_is_the_nproc_rule`, `test_np_minimum_sample_size...`, `test_np_violation_rate_on_independent_data_is_within_delta` |
| CRC index: last grid point before (n/(n+1)) · mean loss + B/(n+1) ≥ alpha | `conformal-risk`, `core/get_lhat.py` | `candidates.crc_release_cutoff`; verbatim port `get_lhat_reference` | `test_crc_cutoff_equals_the_official_get_lhat` |
| Gradient boosting with logistic loss | scikit-learn 1.9.1 `GradientBoostingClassifier` (library unmodified) | `fitting.fit_gb` | arm-level tests of the front |
| Calibration on the logit; expected-loss verdict; Allow-Block threshold | thesis Equations 3.3-3.9 (unchanged code in `rem/`) | `guards.make_guard` | equivalence check: 11,419 replays identical to the stored HV arm |
| Cedar authorization (default deny; forbid overrides permit; skip on error) | cedar-docs `4091567` | `cedar_front.py` (cedarpy 4.12.2) | `tests/test_competitive_study_s11.py` |

No equation identifier was created. Engineering predicates (authority front, direct-value constraint, provenance rule, fail-closed wrapper) are design choices of this project, not published mathematics.

## 3. Change log (all local; newest last)

| Local commit | What | Known before it |
|---|---|---|
| `c21e584` … `35cca4d` (8 commits) | Integration package of 16 November applied as a commit series on a new local branch from `ed1ea39` | package contents |
| `3710267` | **Freeze:** protocol, source registry, feasibility table, exposure manifest, frozen-input hashes, candidate code and tests. No fit or outcome of the new arms existed | all earlier results; design-time label counts |
| `11de6a4` | Fits (152 cells), 99,458 replays, results; Progent reading note, prospective kit, full-framework plan | — |
| `d3cdee6` | **Section 11 addendum freeze:** protocol addendum, Cedar front, provenance rule, tests. Written after the main results were read | all main results |
| final commit of this study | 16,212 replays of the addendum arms; generated tables; interpretation; related-work assessment; Arabic report; change map; this audit; decision table | — |

Corrections made during the work, kept visible:

- An informational field of the NP function (`left_out_released_fraction`) was wrong in the first draft and was fixed **before** the freeze commit (found by a unit test); the cutoff itself was not affected.
- The runner was renamed from `run.py` to `cs_run.py` before the freeze to avoid a module-name clash with the package's `run.py`.
- Two sentences of `04_RESULTS_AND_INTERPRETATION.md` (decision times; where GV and PG differ) were corrected against the generated tables before the final commit.
- No amendment to `PROTOCOL.md` was needed after scoring. Hypothesis outcomes that were not as expected (GV, GB, HV4) are reported as such.

Unchanged: `rem/`, all configurations, every earlier study directory and result file, all four thesis editions, the skipped MELON test and the expected failure of the original tokenizer (93 frozen input files are hash-checked by a test).
