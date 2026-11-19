# REM final thesis completion (19 November 2026)

**Status:** thesis R8 is **ready for supervisor review**. It is **not approved**.

**Scope:** the evidence comes from offline replay and recorded closed-loop runs. **No language model was called** in this study.

## Start here

| Need | File |
|---|---|
| The thesis | `REM_THESIS_FINAL.pdf` / `.docx` (230 pp.); `CHAPTER_1..5_FINAL.md`; `APPENDICES_FINAL.md` |
| Supervisor summary (13 questions, EN + AR) | `13_SUPERVISOR_REVIEW_REPORT.md` |
| Detailed Arabic explanation | `14_ARABIC_THESIS_EXPLANATION.md` |
| What was run, what is blocked | `16_EXECUTION_STATUS_AND_BLOCKERS.md` |

## Key results

**Replay (NO-ADAPT), development data, primary population of 3,313 episodes**
- **REM v1.0 reproduced exactly:** 11 / 2,979 successful attacks; 105 / 334 benign tasks.
- **Learned decision:** prevents 661 of 672 attacks, admits 0, and costs 22.5 benign-utility points [8.0, 38.5].
- **Expected loss vs consequence-independent thresholds:** 153 fewer attacks, 19.5 fewer benign points.
- **Calibration, Modify, context evidence and predicates:** no attack outcome changes.
- **Behavioural evidence:** lowers benign utility by 10.5 points [1.2, 22.6].

**External defences**
- Recorded runs, gpt-4o, ASR on 144 runs:
  - none 62.5%;
  - repeat_user_prompt 46.5%;
  - spotlighting 61.8%;
  - tool_filter 11.1%;
  - pi_detector 0.7%.
- **REM replay on the same pairs:** 2 / 134 attacks, 5 / 15 benign tasks. This comparison is descriptive, not a ranking.
- **Not run:** tool_filter + REM is not replayable with the frozen harness, and MELON was not executed.

## Contents

| File | Content |
|---|---|
| `01_REPOSITORY_AND_EVIDENCE_AUDIT.md` | Baseline location, inventory, provenance table |
| `02_FROZEN_ABLATION_PROTOCOL.md`, `05_EXTERNAL_BASELINE_PROTOCOL.md`, `02_05_PROTOCOL_HASHES.sha256` | Protocols frozen before scoring (`dc8407d`) |
| `05a_EXTERNAL_PROTOCOL_AMENDMENT.md`, `05a_AMENDMENT_HASHES.sha256` | Amendment (`204f7ad`) |
| `03_ABLATION_RESULTS.csv`, `04_ABLATION_ANALYSIS.md` | Ablation |
| `06_EXTERNAL_BASELINE_RESULTS.csv`, `07_EXTERNAL_COMPARISON_ANALYSIS.md` | External comparison |
| `08_MELON_FEASIBILITY_OR_RESULTS.md` | MELON: NOT EXECUTED |
| `09_STATISTICAL_ANALYSIS.md` | Methods, limits, post-hoc sensitivity |
| `10_REPRODUCIBILITY_MANIFEST.md` | Commits, versions, commands, hashes |
| `11_CLAIM_AUDIT.md` | Claim audit of R8 |
| `12_LIMITATIONS_AND_THREATS_TO_VALIDITY.md` | Limitations |
| `15_FINAL_RESEARCH_CONTRIBUTIONS.md` | Contributions as supported |
| `17_FINAL_CHANGELOG.md` | Changes |
| `results/` | JSON results, generated tables, post-hoc files, reproduction gate, fresh pilot outputs, `raw/` per-episode and per-call CSV |
| `figures/` | Architecture; ablation security–utility, paired differences, calibration, latency, reachability; external security–utility |
| `logs/` | Reproduction, runs, tests, build |
| `manifests/output_hashes.sha256` | Output hashes |

## Code

| Location | Content |
|---|---|
| `experiments/final_thesis/` | Study code |
| `tests/test_final_thesis_completion.py` | Tests for this study |
| `REM_FINAL_SUBMISSION/thesis_r8/` | Thesis build |

**REM v1.0 itself (`rem/`, `experiments/pilot/`) was not modified.**
