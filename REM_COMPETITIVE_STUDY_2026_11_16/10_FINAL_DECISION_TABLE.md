# Final decision table and reproduction commands

## 1. Decision table

| Question | Answer | Basis | Remaining uncertainty |
|---|---|---|---|
| Best supported candidate (development data, pre-declared rule) | **GV: the request-derived authority front (revision 3) with the direct-value constraint, used alone, without a learned decision** | No unsafe fixture release; no successful attack on either population or the probe; 1,532 and 1,386 completed tasks; ties with HV and the learned arms and is the simplest | All evidence is from exposed recordings and author-written fixtures; nine attacker objectives, sixteen user tasks; no adaptation; parser written with the requests known |
| Does it improve the frozen REM baseline? | Yes on development data: 0 against 11 and 0 against 3 successful attacks; +10.4 and +22.2 points of completed tasks, intervals above zero | Table 4, GV − REM v1.0 | Not a confirmation; many rounds on the same data |
| Which component causes the gain? | The deterministic authority front and the direct-value constraint | GV equals HV on every episode and fixture; every attack-labelled call is stopped by the front | — |
| Does the learner add value? | **Not established; matched by the guard alone.** The ridge model, the NP and CRC cutoffs and boosted trees changed no outcome (NP at 0.01 lost tasks) | Tables 1, 4, 5 | The recordings contain no attack that passes the front, so they cannot show what a learner would do against one |
| Does it add value over the strict rule G3? | Not established: +125 and +147 tasks, no attack, interval lower bounds exactly zero | Table 4 | — |
| What Progent comparison actually ran? | **Only** the manual banking policy of repository commit `9befb41`, read as data and applied in replay (PG). It is not a configuration of paper v3 | `01_PROGENT_READING_NOTE.md`, Section 6 | Generated and updated policies, approver settings and live agents: not run |
| How does GV compare with PG? | Not resolved: +2.48 points [−2.52, +8.69] and +3.83 [−7.92, +17.23] in completed tasks; PG completes more benign tasks; no successful attack for either | Table 4 | No superiority, equivalence or non-inferiority |
| Do the NP and CRC guarantees apply? | No. Not claimed. Deciding alone, NP stayed near its level on unseen objectives; CRC did not | Protocol Section 6; Table 10 | Full texts unread |
| Section 11: Cedar | Decision parity on 7,098 calls; an implementation option with no security or utility effect; about 2.3 ms per restricted call | Table 13 | — |
| Section 11: provenance rule | No attack removed; 27 and 6 legitimate calls withheld; no benefit established | Table 13 | Needs cases the recordings do not contain |
| Independent evidence still needed | (1) Requests and attacks written and reviewed by other people, including open-amount cases and payees on PG's list; (2) a live, matched comparison with Progent's generated policies; (3) the four method papers in full text; (4) supervisor decisions on SD-PERM, SD-COND and on predicate D2 behind the front | `07_…`, `08_…`, `06_…` | — |

## 2. Reproduction

Requirements: Python 3.11; the project's dependencies; AgentDojo 0.1.35; numpy 2.4.6; SciPy 1.17.1; scikit-learn 1.9.1; cedarpy 4.12.2 (Section 11 only). No model API is called.

```bash
export AGENTDOJO_RUNS=<runs directory of ethz-spylab/agentdojo at 089ed468cf3ed0322acc66b0211f26d9d90dbf60>
export PROGENT_UPSTREAM=<clone of sunblaze-ucb/progent containing 9befb41cbf992b49dbf035cbd3d53eb953d3b351>   # two files are read as data
export PILOT_RESULTS_DIR=<new cache dir> AUTHZ_STATE=<cache dir> IMPROVE_STATE=<cache dir>
export INTEGRATION_STATE=<new cache dir> COMPETITIVE_STATE=<new cache dir> PYTHONHASHSEED=0

# 1. earlier evidence (integration package of 16 November)
python experiments/pilot/build_dataset.py
python experiments/g3_integration/run.py prepare
python experiments/g3_integration/run.py fit
python experiments/g3_integration/run.py replay
python experiments/g3_integration/run.py report
python experiments/g3_integration/followup.py replay
python experiments/g3_integration/followup.py report
git checkout -- REM_G3_INTEGRATION          # keep the package's stored files; the regenerated ones differ only in timing fields

# 2. this study
python experiments/competitive_study/cs_run.py fit        # 152 cells, about 2 minutes on 4 cores
python experiments/competitive_study/cs_run.py replay     # 99,458 replays, about 4 minutes
python experiments/competitive_study/cs_run.py report     # results/results.json and per-episode outcomes
python experiments/competitive_study/cs_run_s11.py replay # 16,212 replays (Cedar front, provenance rule)
python experiments/competitive_study/cs_run_s11.py report
python experiments/competitive_study/cs_tables.py         # 03_RESULTS_TABLES.md

# 3. tests
python -m pytest -o addopts="" -q                          # 500 passed, 1 skipped (MELON environment), 1 expected failure (original tokenizer)
```

Timing fields differ between runs; counts, intervals and per-episode outcomes do not (seeded bootstrap; deterministic fits).
