# Chapter 4: requirement-to-section and evidence matrix

**Edition:** third edition of the thesis draft, 14 November 2026 (`REM_THESIS_FINAL_R3.docx/.pdf`; Chapter 4 on printed pages 105 to 171). **Status:** draft for supervisor review; not approved.

The chapter is organized in the six sections requested by Prof. Omar. Existing verified text was kept and placed under the section it belongs to (the assembly log `final_source_map.json` records every unit as kept, moved, replaced or new). "New" marks text written for this edition.

## 1. Requirement → section → evidence

| Supervisor's requirement | Section and subsections | Tables and figures | Evidence files | Status |
|---|---|---|---|---|
| **4.1 Implementation Tools and Environment** | 4.1.1 Software, hardware and benchmark environment (new) · 4.1.2 Implemented components (new) · 4.1.3 Reproducibility and software verification (new) · 4.1.4 Kinds of evidence and evaluation modes (kept, updated) | 4.1–4.3 | `results/*/provenance` blocks; `REM_IMPROVEMENT_STUDY/04_IMPLEMENTATION_AND_TESTS.md`; test log (278 passed, 1 skipped, 1 expected failure) | **Complete.** Hardware of the earlier runs was not recorded and this is stated |
| **4.2 Dataset Preparation and Training** | 4.2.1 Recorded data, fitting protocol and chronology, with the second population (kept, updated) · 4.2.2 Labels, the user_task_15 collision and benchmark versions (kept) · 4.2.3 Pilot E0: feasibility and feature retention (kept) · 4.2.4 Training of the risk estimator (new) | 4.4–4.7 | `dataset_summary.json`; `confirmatory_results.json`; `e0_pilot.json`; `e1_crossfit.json`; `SPLIT_MANIFEST.json` | **Complete** for recorded data. No data were collected for the thesis; no human label audit exists (stated) |
| **4.3 Experimental Setup and Evaluation Metrics** | 4.3.1 Compared arms · 4.3.2 Populations and generalization schemes · 4.3.3 Evaluation metrics · 4.3.4 Statistical procedure and comparisons fixed in advance (all new; definitions from Chapter 3) | 4.8–4.10 | Protocol commits `cca4968`, `19bd168`, `9137b03`; `DEVELOPMENT_PROTOCOL.md` | **Complete** |
| **4.4 Comparisons with Existing Models and Defense Frameworks** | 4.4.1 Rule baselines and an audit of REM's interventions (kept) · 4.4.2 Distributed defenses, recorded outcomes only (kept) · 4.4.3 A published policy and a request-derived permission rule in the same harness (new; repaired rule G2 added in R3; repeated rows removed) · 4.4.4 Live-agent and published-defense experiments: status (kept, updated) · 4.4.5 Comparison with prior work (kept, updated) | 4.11–4.16 | `study_results.json`; `e4_cross_template_and_defenses.json`; `improvement_results.json`; Progent repository at commit `9befb41` (file digests pinned) | **Partly complete.** Internal baselines, rules and **one published policy** (Progent's published manual banking policy adapted to the shared replay harness) are compared on the same episodes, with a call-level audit of the one task where all remaining attacks occur. **Not done:** any defense that needs a language model (MELON, Task Shield, CaMeL, Progent with generated policies); no live comparison |
| **4.5 Ablation Studies** | 4.5.1 Ablations of the components of REM v1.0 (kept; calibration statement corrected) · 4.5.2 Ablation of the behavioral evidence group and of the verdict set · 4.5.3 Ablations of the task-permission extension · 4.5.4 Ablations of the repaired rule and of the authority guard (new in R3) | 4.17–4.22 | `e2_e5_e6_observe_only.json`; `e4_e5_enforcement_replay.json`; `improvement_results.json` | **Complete** for the components that exist. The injection classifier is absent and could not be ablated (stated) |
| **4.6 Results and Discussion** | 4.6.1 RQ1 offline classification · 4.6.2 RQ2 observe-only decisions · 4.6.3 RQ2 and RQ3 replay · 4.6.4 Optional sequential analysis · 4.6.5 Realized loss · 4.6.6 Generalization and a rejected candidate · 4.6.7 Robustness probes · 4.6.8 Confirmatory evaluation of REM v1.1 (all kept, corrected) · 4.6.9 Exploratory extension: task-permission evidence · 4.6.10 Follow-up: defects of the permission rule and a call-level audit of user task 15 (new in R3) · 4.6.11 Interpretation (revised; repeated percentage table removed) · 4.6.12 Threats to validity · 4.6.13 Chapter summary | 4.23–4.45; Figures 4.1–4.3 | all result files above | **Complete** within replay. Every result is exploratory by label; the extension is development evidence |

## 2. Where the earlier Chapter 4 went

| Section of the first edition (12 November) | Section of this edition |
|---|---|
| 4.1 Purpose, status and kinds of evidence | chapter opening; 4.1.4 |
| 4.2 Data, protocol and chronology | 4.2.1 |
| 4.3 Pilot E0 | 4.2.3 |
| 4.4 RQ1; 4.5 RQ2 observe-only; 4.6 Replay | 4.6.1; 4.6.2; 4.6.3 |
| 4.7 Ablations | 4.5.1 |
| 4.8 CUSUM; 4.9 Realized loss | 4.6.4; 4.6.5 |
| 4.10 Labels and user_task_15 | 4.2.2 |
| 4.11 Distributed defenses | 4.4.2 |
| 4.12 Rule baselines and audit | 4.4.1 |
| 4.13 Generalization and rejected candidate; 4.14 Probes and fixtures; 4.15 Confirmatory evaluation | 4.6.6; 4.6.7; 4.6.8 |
| 4.16 Live and published-defense status | 4.4.4 |
| 4.17 Interpretation; 4.19 Threats; 4.20 Summary | 4.6.10; 4.6.11; 4.6.12 |
| 4.18 Comparison with prior work | 4.4.5 |

Subsections of the first edition are now unnumbered fourth-level headings inside these sections; every cross-reference was rewritten by script (0 unresolved).

## 3. What remains open for each requirement

| Requirement | Open item | Who can close it |
|---|---|---|
| 4.1 | University template and formatting rules (decision N-9) | Supervisor / faculty |
| 4.2 | Human label audit (D-6); approval of the label rule | Supervisor; annotators |
| 4.3 | Approval of costs, tiers and predicates (D-9); a security margin, if one is wanted | Supervisor |
| 4.4 | Model credential, embedding service and spending limit for MELON, Task Shield, Progent with generated policies and the live harness (D-15); full texts of NEXUS, aiAuthZ, Kairos, Progent and CaMeL | Supervisor; author |
| 4.5 | Injection classifier (D-8) | Supervisor |
| 4.6 | Decision on REM v1.1 (SD-FEAT) and on the exploratory extension (SD-PERM); a prospective evaluation on fresh outcomes | Supervisor |
