# 01 Repository and evidence audit (19 November 2026)

**Branch:** `claude/rem-final-thesis-completion-20261119`, created from `bf36381` (the last commit of the REM-B hardening study).

**Repository:** `RMS756/Ram`. Every commit below was checked with `git cat-file`, `git log` and `git diff` in this container.

## 1 Commit `bf36381c42a4669043d5b30072744fcc3024d66d`

- **The commit exists.** It is "REM-B hardening study: frozen and amendment results … decision (REM-B2 NO-GO; REM-B3 NO-GO post-hoc; learned components rejected) …", dated 19 November 2026.
- **It is not the REM v1.0 baseline.** It is the end of an exploratory study and adds only the study folder, `experiments/rem_b_hardening/` and tests. It touches nothing in `rem/` or `experiments/pilot/`.

## 2 The frozen REM v1.0 baseline (located independently)

| Item | Evidence |
|---|---|
| Design authority | `STAGE2_FINAL_ALGORITHM_MATHEMATICAL_DECISION_REPORT.md` (`f46c126`, 19 Sep 2026) and `CLAUDE.md` (the frozen pipeline: ridge LR → Platt on the logit → consequence tier → predicates → expected-loss Bayes verdict → deterministic mitigation → audit). |
| Pilot design declared before any run | `configs/exploratory/pilot_e0.yaml`, commit `48bef90` (27 Oct 2026, "Declare exploratory pilot E0 design (pre-registration, before any run)"). |
| Frozen pilot pipeline | `experiments/pilot/` at `ea621c3` (1 Nov 2026, the R4 complete-call timer). Since then only one file was **added**: `ablation_minimal.py` (`41a910d`, `2eca264`), a standalone script that the pipeline does not import. Nothing in the pipeline was modified. |
| `rem/` core | `git diff 9fddfa7 HEAD -- rem/` lists only three **added** files: `rem/deployment/__init__.py` (empty), `rem/deployment/gateway.py` (deployment simulation, 5 Nov) and `rem/integration/melon_rem.py` (MELON adapter, 5–6 Nov). None of them is imported by the decision path. The decision, estimator, calibration, predicate, mitigation and replay modules are byte-identical to `9fddfa7` (3 Nov 2026, five-chapter thesis). |
| Published REM v1.0 numbers | Thesis R7 (`REM_FINAL_SUBMISSION/thesis_r7`, last change `d52baa1`, 17 Nov), Table 4.10: 11 / 2,979 attacks, 105 / 334 benign, 1,083 / 2,979 tasks under attack, 33 / 178 legitimate calls released. Originally from `results/pilot_R4` (`6fc0952`, 1 Nov). |
| **Fresh reproduction today** | `build_dataset.py; e0_pilot.py; run_main.py crossfit rmod replay` into a new state directory: **11 / 105 / 1,083**, identical (`results/reproduction_gate.json`, log `logs/baseline_reproduction.log`, 7 min 46 s). |

**Conclusion.** The approved REM v1.0 is `rem/` as of `9fddfa7`, together with the pilot pipeline at `ea621c3` under `pilot_e0.yaml`. Its historical results reproduce exactly at this branch's base. None of them was modified.

## 3 Inventory

| Item | Location | Status |
|---|---|---|
| Approved research proposal | **not in the repository**. Its objectives O1–O3 are quoted in thesis Chapter 1, Section 1.6, from the supplement (S-3.1.2). | objectives available; proposal file MISSING |
| University thesis template | **not found** in the repository or in `/home/user` (searched for `*template*.docx` and `*.dotx`). Earlier audits record "BLOCKED — MISSING SOURCE" (`PROJECT_AUDIT.md` l. 114). | MISSING. The build uses the provisional layout of R2–R7 (A4, pinned fonts), stated in the thesis. |
| Current thesis | `REM_FINAL_SUBMISSION/thesis_r7/` (R7: `src/*.md`, `REM_THESIS_EDITORIAL_R7.docx`, supplement PDF) | base of R8; unchanged |
| REM v1.0 code | `rem/` (estimator `rem/algorithms`, decision `rem/algorithms/decision/policy.py` and `a3.py`, replay `rem/integration/agentdojo_replay.py`, statistics `rem/evaluation`) | frozen |
| Frozen protocols | `pilot_e0.yaml` (`48bef90`); Chapter 3 of the thesis; the protocol files of each later study (each committed before scoring) | – |
| AgentDojo | installed package 0.1.35 (PyPI, authentic). Recorded runs from `ethz-spylab/agentdojo` @ `089ed468`, at `/home/user/ethz-spylab/agentdojo/runs` (29 pipelines). The Progent fork is not used. | verified |
| Recorded episodes | primary population 3,313 eligible (2,979 attacked, 334 benign; 21 undefended backbones); defence pipelines 5 × 159 for gpt-4o | – |
| Partitions | scheme S1: the outer fold holds out one attacker objective; benign episodes go to folds by user task (round robin). Cross-fitted predictions. | – |
| Runners | `experiments/pilot/run_main.py` (frozen); `experiments/final_thesis/{ablation_run,external_run,make_figures,make_tables}.py` (this study) | – |
| Historical results | `results/pilot_R2` (`0f45527`), `results/pilot_R4` (`6fc0952`) | unchanged |
| Earlier ablations | pilot A1–A7 (R7 Section 4.5.1); the S-series ablations of 13–19 Nov (exploratory) | known before this study (disclosed in `02`) |
| Claim audits | `REM_FINAL_SUBMISSION/thesis_r7/audit/CLAIM_AUDIT_R7.md`, earlier `CLAIM_AUDIT_*` | read |
| Benchmark comparisons | R7 Section 4.4.2 (recorded defences, 143 runs); 4.4.3 (Progent policy replay, exploratory) | updated in R8 |

## 4 Provenance of the thesis's major results

Kinds of evidence:
- **APPROVED:** design;
- **FROZEN:** pre-declared result of REM v1.0;
- **EXPLORATORY:** later study, pre-registered per study but on development data;
- **POST-HOC:** analysis or repair after results were known;
- **NOT EXECUTED.**

| Claim / result (thesis location) | Kind | Source file | Experiment | Commit |
|---|---|---|---|---|
| Five-layer architecture; ridge LR; Platt on the logit; expected-loss verdict; SHAP audit-only (Ch. 3) | APPROVED | `STAGE2_FINAL_ALGORITHM_MATHEMATICAL_DECISION_REPORT.md`, `CLAUDE.md` | – | `f46c126` |
| Losses, tiers, features, folds, bootstrap settings (Ch. 3, 3.11) | FROZEN design values (declared, exploratory status, not supervisor-approved, decision register App. B) | `configs/exploratory/pilot_e0.yaml` | pilot E0 | `48bef90` |
| Held-out ROC-AUC 0.938, AP 0.719, ECE 0.044 (Ch. 4) | FROZEN | `results/pilot_R4/e1_crossfit.json`; re-computed today `results/fresh_pilot_e1_crossfit.json` (A0: 0.9383 / 0.7189 / 0.0438) | E1 | `6fc0952`; today |
| REM v1.0: 11 / 2,979; 105 / 334; 1,083; 33 / 178 (Table 4.10) | FROZEN | `results/pilot_R4/e4_e5_enforcement_replay.json`; today `results/fresh_pilot_e4_e5_enforcement_replay.json` | E4/E5 replay | `6fc0952`; today |
| B1 thresholds 164 / 170; no defence 672 / 175 (Table 4.10) | FROZEN | same | same | same |
| Pilot ablations (no_beh, no_ctx, no_act, no_calibration, single tier, no predicates) (R7 4.5.1) | FROZEN (pilot) | `results/pilot_R4/*` | E4 ablations | `6fc0952` |
| **Final ablation A0–A7, reachability, latency, calibration per arm** (R8 4.5.5) | **CONTROLLED, pre-registered; development data** | `results/ablation_results.json`, `03_…csv` | this study | protocol `dc8407d`; results `1643ce9` |
| Recorded defences D1–D4 (R7 4.4.2, 143 runs) | recorded (authors' runs) | `results/pilot_R2/e4_cross_template_and_defenses.json` | E4 cross-template | `0f45527` |
| **External comparison, recorded (144 runs) + REM replay on defence traces** (R8 4.4.2) | **CONTROLLED, pre-registered; amendment 05a** | `results/external_results.json`, `06_…csv` | this study | `dc8407d`, `204f7ad`, `1643ce9` |
| Second population, double holdout, confirmatory run (R7 4.6.8) | EXPLORATORY (confirmatory run pre-committed) | `REM_IMPROVEMENT_STUDY/`, `REM_Authorization_Generalization_Study/` | Nov 11–15 | `cca4968`…`afc42b4` |
| Request-derived permission rule G1–G3, GV, amount verifier (R7 3.14, 4.4.3, 4.5.3–4.5.4, 4.6.9) | EXPLORATORY with POST-HOC repairs (each repair frozen before scoring) | `REM_G3_INTEGRATION/`, `REM_COMPETITIVE_STUDY_2026_11_16/`, `REM_REPAIR_STUDY_2026_11_17/` | Nov 13–17 | `c21e584`…`d52baa1` |
| Progent banking policy replay (R7 4.4.3) | EXPLORATORY (policy from repository, not the framework) | `REM_PROGENT_COMPETITIVE_2026_11_18/` | Nov 17–18 | `bdde9d0`…`e876962` |
| REM-A/B/C redesign; REM-B2/B3 hardening (not in R7) | EXPLORATORY; REM-B2 NO-GO, REM-B3 NO-GO (post-hoc); learned components rejected | `REM_ARCHITECTURE_REDESIGN_STUDY_2026_11_18/`, `REM_IMPROVEMENT_CONTROLLED_STUDY_2026_11_18/`, `REM_B_HARDENING_VALIDATION_2026_11_19/` | Nov 18–19 | `31c146e`, `ff2399b`, `bf36381` |
| Deployment simulation (gateway, parity, latency) | EXPLORATORY engineering test | `REM_EXPERIMENTAL_VALIDATION/`, `rem/deployment/gateway.py` | Nov 5–6 | `b137837`…`cfb4f40` |
| Live closed-loop REM with an LLM | **NOT EXECUTED** (harness tested with scripted agents) | `experiments/live/` | – | `ea621c3`…`f9c3a5d` |
| MELON and MELON + REM | **NOT EXECUTED** (adapter tested with scripted agents) | `rem/integration/melon_rem.py`, `08` | – | `4cc0fc9`…`cfb4f40` |

## 5 Findings of the audit that change the thesis text

1. **R7 Section 4.4.2.** It gave the recorded defences on 143 runs without stating the exclusion. R8 gives both the full 144-run figures and the reason for the difference (AM-1 excludes user_task_15 × injection_task_4).
2. **R7 had no paired ablation intervals, no A5 (Modify) arm and no A6 (learned-decision) arm.** R8 adds them (Section 4.5.5).
3. **"The learned component changes zero decisions".** This was an observation of the exploratory REM-B family. It is **false for REM v1.0** (`04`, §4.1). R8 states this explicitly so that the two are not confused.
4. **The REM-B family (18–19 November) is not in R7.** R8 records it as exploratory and NO-GO (Section 4.5.6) and does not merge it into REM v1.0.
5. **No conflict was found** between the reproduced numbers and any number of R7.
