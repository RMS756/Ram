# REM-B hardening, generalisation and final validation (19 November 2026)

**Branch.** `claude/rem-b-hardening-20261119`, from `31c146e`.

**Status.** `[PROPOSED - EXPLORATORY]`. The approved REM v1.0 design, the thesis objectives and all historical results are unchanged.

**Evidence base.** Offline replay (NO-ADAPT), author-written probe suites and a scripted closed loop. **No model was called.** Full Progent and live LLM: **NOT EXECUTED**.

## Outcome

| Question | Result |
|---|---|
| Earlier claims of `31c146e` | all six verified from raw outputs (`01`) |
| HO4 root cause | identifier token parsed as an object designator (`02`); fixed by R1 |
| REM-B2 (REM-B + R1 system-of-record evidence R2 + delegated judgement R3) | **NO-GO**. 0 attacks and no added violations, +83 tasks on held-out H2 (interval lower bound 0; gains only in ut14 and ut15), but it releases 3 unauthorised held-out probe proposals (swapped amounts; unrequested amount change). Frozen REM-B and C1 release the same 3. |
| Learned component (review ranking, learned withholding) | NULL / rejected |
| Amendment REM-B3 (post-hoc) | **NO-GO**. Closes those classes, but releases 1 unauthorised v3 probe (compiler mistypes "send now" as a standing order) and withholds 73 correct updates on H2. |
| vs Progent hand-written policy | far fewer value violations on recorded traces (11 vs 161), but both fail held-out probes; no significant utility difference; **no superiority claim** |
| Main scientific finding | the security of request-derived authorisation is limited by natural-language **intent compilation**: each of three held-out probe rounds found a new compiler error leading to an unauthorised release |

## Documents

| # | File |
|---|---|
| 01 | `01_BASELINE_VERIFICATION.md` |
| 02 | `02_HO4_ROOT_CAUSE.md` |
| 03 | `03_AUTHORIZATION_FIX.md` |
| 04 | `04_BENIGN_FAILURE_ANALYSIS.md` |
| 05 | `05_HYBRID_REDESIGN_ASSESSMENT.md` |
| 06 | `06_FROZEN_PROTOCOL.md` + `06_PROTOCOL_HASHES.sha256`; `06a_AMENDMENT_PROTOCOL.md` + hashes; `06b_PROTOCOL_DEVIATIONS_AND_NOTES.md` |
| 07 | `07_SECURITY_UTILITY_RESULTS.csv` (frozen and amendment rounds, with a `round` column) |
| 08 | `08_ABLATION_RESULTS.md` |
| 09 | `09_GENERALIZATION_REPORT.md` |
| 10 | `10_PROGENT_COMPARISON.md` |
| 11 | `11_LIVE_LLM_STATUS.md` |
| 12 | `12_FINAL_ARCHITECTURE_DECISION.md` |
| 13 | `13_RESEARCH_CONTRIBUTION_AUDIT.md` |
| 14 | `14_THESIS_READY_RESULTS.md` |
| 15 | `15_ARABIC_DETAILED_REPORT.md` |
| 16 | `16_REPRODUCIBILITY_MANIFEST.md` + `manifests/reproducibility_manifest.json` |

**Also here:** `CHANGELOG.md`, `results/`, `logs/`, `figures/`.

**Code:** `experiments/rem_b_hardening/`.

**Tests:** `tests/test_rem_b_hardening.py`.
