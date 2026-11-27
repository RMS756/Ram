# REM Defense-in-Depth track (started 27 November 2026)

| File | Content |
|---|---|
| `01_AUDIT.md` | Audit of thesis, code, protocols and records; status class of every control; reproduction checks |
| `02_PROTOCOL_DID1.md` (+ `.sha256`) | Protocol DiD-1, committed before analysis (`a3e30c1`) |
| `03_PROTOCOL_DID2.md` (+ `.sha256`) | Protocol DiD-2, committed before the run (`2547854`) |
| `03a_AMENDMENT_DID2.md` | Post-hoc arms, committed before their run (`e3e7488`) |
| `04_DID_CONTROL_MODEL.md` | Threat and control model (attack chain × controls × layers) |
| `05_DID_RESULTS.md` | Results of DiD-1 and DiD-2 |
| `06_IMPLICATIONS_AND_PLAN.md` | Thesis implications (not applied), decisions required, proposed enhancements, next experiments, journal track |
| `07_PROTOCOL_SIGNALS.md` (+ `.sha256`) | Protocol SIG-1 (detection signals and feature correlation), committed before the run |
| `08_SIG1_RESULTS.md` | SIG-1 results |
| **Task 2: strengthened architecture (proposals; nothing below is implemented)** | |
| `20_ARCHITECTURE_CURRENT_V1_0.md` | Specification A: REM v1.0 as implemented |
| `21_ARCHITECTURE_PROPOSED_DID.md` | Specification B: proposed REM-DiD (layer responsibilities, 4A/4B, decision flow) |
| `22_CURRENT_VS_PROPOSED.md` | Comparison, with the status of each proposal |
| `23_TRUSTED_AUTHORIZATION_ENVELOPE.md` | TAE specification |
| `24_CROSS_LAYER_PROPERTIES.md` | Cross-layer properties: implementation, assumptions, test, acceptance criterion |
| `25_ASSUMPTIONS_AND_LIMITATIONS.md` | Security assumptions and limitations |
| `26_IMPLEMENTATION_REQUIREMENTS_AND_COMPATIBILITY.md` | Requirements and fit with the existing `rem/` code |
| `27_PRIORITIZED_PLAN.md` | Feasibility-first plan with decision gates |
| `figures/fig_rem_v1_0_current.png`, `figures/fig_rem_did_proposed.png` | Five-layer diagrams (`code/fig_architecture.py`) |
| **Prior-art investigation (27 Nov 2026; full texts not reachable in this session, so every entry carries an evidence level)** | |
| `30_PUBLICATION_STATUS_AND_EVIDENCE_LEVELS.md` | Access limits, evidence levels, publication-status verification |
| `31_PRIOR_ART_LITERATURE_MATRIX.md` | Literature matrix (mandatory works and related work) |
| `32_SYSTEM_ARCHITECTURE_COMPARISON.md` | 18-attribute comparison: RTBAS, CaMeL, Progent, AgentCap, Fides, REM |
| `33_REM_FIVE_LAYER_MAPPING.md` | Mapping of prior mechanisms to REM's five layers |
| `34_FINANCIAL_DOMAIN_EVIDENCE.md` | Financial evidence categories; beneficiary, amount, limits, approvals, repetition |
| `35_GAP_OVERLAP_NOVELTY.md` | Established vs untested; overlap; revised contribution statement [PD] |
| `36_CHAPTER_REFERENCES_AND_EXPERIMENTS.md` | References per chapter; experiments E0–E8 with decision gates |
| `code/did1_coverage.py`, `code/did2_replay.py`, `code/sig1_signals.py` | Analysis code; `rem/` and `experiments/` unchanged |
| `results/did1_results.json`, `results/did2_results.json`, `results/sig1_results.json` | Raw outputs |

**Reproduce**, from the repository root. AgentDojo 0.1.35 must be installed, and the AgentDojo runs must be at commit 089ed468 in `/home/user/ethz-spylab/agentdojo/runs`.

    export PILOT_RESULTS_DIR=$PWD/REM_DEFENSE_IN_DEPTH/work/pilot
    (cd experiments/pilot && python3 build_dataset.py && python3 e0_pilot.py && python3 run_main.py crossfit rmod observe)
    python3 REM_DEFENSE_IN_DEPTH/code/did1_coverage.py
    python3 REM_DEFENSE_IN_DEPTH/code/did2_replay.py

`work/` holds regenerated intermediate files. It is not committed; it is rebuilt by the commands above.

## Task 3: REM-DiD research development (27 November 2026)

**REM-DiD is an exploratory research candidate. REM v1.0 is unchanged.**

| File | Deliverable |
|---|---|
| `40_PRIOR_ART_COMPARATIVE_MATRIX.md` | 1 Prior-art comparison (code-level for CaMeL, Progent, Fides, AgentDojo, ASB); origin of every mechanism |
| `48_REM_V1_0_AUDIT.md` | 2 REM v1.0 audit |
| `47_REM_DID_ARCHITECTURE.md` | 3 Strengthened five-layer architecture |
| `42_TAE_SPEC_IMPLEMENTED.md` | 4 TAE specification (as implemented) |
| `41_DATA_PROVENANCE_AND_LINEAGE_SPEC.md` | 5 Provenance and lineage |
| `43_DETECTION_SPEC.md` | 6 Detection (with SIG-2 results) |
| `45_BEHAVIOR_SPEC.md` | 7 Behavioral Analysis |
| `44_DECISION_SPEC.md` | 8 Authorization and learned-risk decision |
| `46_MITIGATION_ENFORCEMENT_SPEC.md` | 9 Mitigation and enforcement |
| `49_THREAT_CONTROL_MATRIX_AND_PROPERTIES.md` | 10 Threat/control matrix; 11 properties and test criteria |
| `figures/fig_rem_v1_0_current.png`, `fig_rem_did_implemented.png`, `fig_rem_did_proposed.png`, `fig_did3_cost_grid.png` | 12 Diagrams |
| `55_IMPLEMENTATION_AND_TEST_REPORT.md`, `tests/`, `code/did3_scenarios.py` | 13 Bypass and failure-injection suite; 18 implementation and tests |
| `50_PROTOCOL_DID3.md` (+ `.sha256`), `50a_AMENDMENT_DID3_COVERAGE.md`, `51_DID3_RESULTS.md` | 14 Individual and combined-control protocol and results |
| `52_COST_SENSITIVITY_PROTOCOL.md` | 15 Cost sensitivity (protocol and results) |
| `53_HUMAN_LABEL_AUDIT_PACKAGE.md`, `label_audit/` | 16 Human label-audit package (not performed) |
| `54_STATISTICAL_ANALYSIS_REPORT.md` | 17 Statistics |
| `56_REPRODUCIBILITY_PACKAGE.md`, `results/did3_manifest.sha256` | 19 Reproducibility |
| `../REM_DID_THESIS_EDITION/` | 20 Revised thesis DOCX/PDF (tenth edition) |
| `58_JOURNAL_MANUSCRIPT_PACKAGE.md` | 21 Journal package |
| `57_LIMITATIONS_AND_MISSING_RESOURCES.md` | 22 Limitations and missing resources |
| `remdid/` | Code (L1–L5) |
