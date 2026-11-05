# Deployment simulation — results

Run: `results/deployment_sim/2026-11-05_four_configs`; REM commit `2f79a8b`; 3334 recorded episodes; 4 vCPU; main concurrency 4.

## 1. Parity with the thesis's in-process replay

| Configuration | Episodes compared | Mismatches (utility / security / error / per-call verdicts) |
|---|---:|---|
| B0 | 3334 | 0 / 0 / 0 / 0 |
| REMLITE | 3334 | 0 / 0 / 0 / 0 |
| B1 | 3334 | 0 / 0 / 0 / 0 |
| REM | 3334 | 0 / 0 / 0 / 0 |

## 2. Outcomes (valid episodes; NO-ADAPT)

| Configuration | ASR (deployed) | ASR (thesis §4.6) | Utility under attack | Benign utility |
|---|---:|---:|---:|---:|
| B0 | 0.226 | 0.226 | 0.492 | 0.524 |
| REMLITE | 0.055 | 0.055 | 0.514 | 0.509 |
| B1 | 0.055 | 0.055 | 0.514 | 0.509 |
| REM | 0.004 | 0.004 | 0.364 | 0.314 |

## 3. Latency and throughput (main run)

| Configuration | Episodes/s | Calls | REM time per call, median / p95 (ms) | Turn round trip, median / p95 (ms) | Backend per executed call, median (ms) | Errors |
|---|---:|---:|---:|---:|---:|---:|
| B0 | 122.8 | 6756 | 0.09 / 0.33 | 6.1 / 14.6 | 3.09 | 0 |
| REMLITE | 119.7 | 6756 | 0.17 / 0.42 | 6.0 / 15.0 | 3.45 | 0 |
| B1 | 120.4 | 6756 | 0.17 / 0.41 | 6.0 / 15.0 | 3.45 | 0 |
| REM | 124.2 | 6756 | 0.18 / 0.43 | 5.2 / 15.0 | 3.93 | 0 |

## 4. Concurrency sweep (REM; same 400 episodes)

| Concurrent episodes | Episodes/s | Calls/s | Turn round trip median / p95 (ms) | REM time per call median / p95 (ms) | Errors |
|---:|---:|---:|---:|---:|---:|

## 5. Audit completeness and enforcement

- Episodes: 13336; calls released: 22774; calls withheld: 4250.
- Calls executed by the backend: 22774; episodes where the backend log differs from the released calls: 0.

## 6. Fail-closed probes

- unknown_episode_calls: 404
- malformed_json: 400
- unknown_configuration: 400
- backend_open_episodes_after_probes: 0

Gateway counters: `{"episodes_opened": 13336, "calls": 27024, "released": 22774, "withheld": 4250, "fail_closed": 0, "backend_errors": 0}`; gateway start-up (loading frozen components): 4 s.
