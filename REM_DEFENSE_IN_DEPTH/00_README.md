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
| `code/did1_coverage.py`, `code/did2_replay.py` | Analysis code; `rem/` and `experiments/` unchanged |
| `results/did1_results.json`, `results/did2_results.json` | Raw outputs |

**Reproduce**, from the repository root. AgentDojo 0.1.35 must be installed, and the AgentDojo runs must be at commit 089ed468 in `/home/user/ethz-spylab/agentdojo/runs`.

    export PILOT_RESULTS_DIR=$PWD/REM_DEFENSE_IN_DEPTH/work/pilot
    (cd experiments/pilot && python3 build_dataset.py && python3 e0_pilot.py && python3 run_main.py crossfit rmod observe)
    python3 REM_DEFENSE_IN_DEPTH/code/did1_coverage.py
    python3 REM_DEFENSE_IN_DEPTH/code/did2_replay.py

`work/` holds regenerated intermediate files. It is not committed; it is rebuilt by the commands above.
