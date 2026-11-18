# REM improvement — controlled study (18 November 2026)

`[PROPOSED - EXPLORATORY - NOT PART OF THE APPROVED REM DESIGN]`. Branch `claude/rem-improvement-controlled-20261118`.

**Decision:**
- evidence-resolution candidate: **INCONCLUSIVE**;
- learned component: **NULL**, and harmful on top of the candidate.

| File | Content |
|---|---|
| `01_REPRODUCIBILITY_AUDIT.md` | frozen commits, installations, arms, exact reproduction, corrections |
| `02_BENCHMARK_COLLISION_AUDIT.md` | ut15×it4, collision scan, order dependence |
| `03_FALSE_POSITIVE_ROOT_CAUSE.md` | call-level audit of 934 withheld calls, ranked causes |
| `04_IMPROVEMENT_DESIGN.md` | E1, E2 (pre-registered before implementation) |
| `05_FROZEN_EXPERIMENT_PROTOCOL.md`, `05_PROTOCOL_HASHES.sha256`, `05a_AMENDMENTS.md` | protocol frozen before scoring; dated amendments |
| `06_ABLATION_RESULTS.csv` | per arm and population metrics (generated) |
| `07_SECURITY_UTILITY_COMPARISON.md` | replay, scripted loop, case suites, contrasts, partitions |
| `08_LEARNED_COMPONENT_CONTRIBUTION.md` | verdict changes, calibration, switch points, latency |
| `09_PROGENT_COMPARISON.md` | upstream engine parity; manual-policy comparison; full Progent not run |
| `10_LIVE_LLM_READINESS.md` | endpoint check, prepared components, protocol placeholders |
| `11_THESIS_READY_RESULTS.md` | draft text, labelled confirmed / exploratory / future |
| `12_ARABIC_EXECUTIVE_SUMMARY.md` | Arabic summary |
| `13_CLAIM_AUDIT_AND_LIMITATIONS.md` | claims checked; limitations |
| `14_FINAL_GO_NO_GO_DECISION.md` | decision under the frozen criteria |
| `results/`, `logs/`, `manifests/` | stored outputs, run logs, reproducibility manifests |

Code: `experiments/improvement_controlled/`. Tests: `tests/test_improvement_controlled.py`.

## Reproduction (environment of the study; PYTHONHASHSEED=0)

```
python3 experiments/improvement_controlled/manifest.py REM_IMPROVEMENT_CONTROLLED_STUDY_2026_11_18/manifests/manifest_final.json
python3 experiments/progent_competitive/closed_loop_scripted.py REM_IMPROVEMENT_CONTROLLED_STUDY_2026_11_18/results/repro_closed_loop_scripted.json
python3 experiments/improvement_controlled/collision_audit.py REM_IMPROVEMENT_CONTROLLED_STUDY_2026_11_18/results/collision_audit.json
python3 experiments/improvement_controlled/fp_audit.py REM_IMPROVEMENT_CONTROLLED_STUDY_2026_11_18/results/fp_audit_replay.json
python3 experiments/improvement_controlled/fp_classify.py REM_IMPROVEMENT_CONTROLLED_STUDY_2026_11_18/results/fp_audit_replay.json REM_IMPROVEMENT_CONTROLLED_STUDY_2026_11_18/results/fp_classification
python3 experiments/improvement_controlled/ctl_run.py replay scripted diag gen fixtures report
python3 experiments/improvement_controlled/scripted_summary.py
python3 experiments/improvement_controlled/make_figure.py
# upstream Progent (isolated venv with z3-solver, jsonschema, docstring_parser; REM_ALLOW_UPSTREAM_EXECUTION=1):
python experiments/progent_competitive/parity_upstream.py
python experiments/improvement_controlled/parity_recorded_calls.py REM_IMPROVEMENT_CONTROLLED_STUDY_2026_11_18/results/fp_audit_replay.json REM_IMPROVEMENT_CONTROLLED_STUDY_2026_11_18/results/progent_parity_recorded_calls.json
python3 -m pytest -q tests/test_improvement_controlled.py
```
