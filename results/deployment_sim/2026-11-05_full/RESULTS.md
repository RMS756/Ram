# Deployment simulation — results

Run: `results/deployment_sim/2026-11-05_full`; REM commit `c30ad8a`; 3334 recorded episodes; 4 vCPU; main concurrency 4.

## 1. Parity with the thesis's in-process replay

| Configuration | Episodes compared | Mismatches (utility / security / error / per-call verdicts) |
|---|---:|---|
| B0 | 3334 | 0 / 0 / 0 / 0 |
| B1 | 3334 | 0 / 0 / 0 / 0 |
| REM | 3334 | 0 / 0 / 0 / 0 |

## 2. Outcomes (valid episodes; NO-ADAPT)

| Configuration | ASR (deployed) | ASR (thesis §4.6) | Utility under attack | Benign utility |
|---|---:|---:|---:|---:|
| B0 | 0.226 | 0.226 | 0.492 | 0.524 |
| B1 | 0.055 | 0.055 | 0.514 | 0.509 |
| REM | 0.004 | 0.004 | 0.364 | 0.314 |

## 3. Latency and throughput (main run)

| Configuration | Episodes/s | Calls | REM time per call, median / p95 (ms) | Turn round trip, median / p95 (ms) | Backend per executed call, median (ms) | Errors |
|---|---:|---:|---:|---:|---:|---:|
| B0 | 135.3 | 6756 | 0.09 / 0.30 | 5.6 / 13.0 | 2.47 | 0 |
| B1 | 135.7 | 6756 | 0.17 / 0.37 | 5.3 / 12.7 | 2.66 | 0 |
| REM | 141.9 | 6756 | 0.19 / 0.40 | 4.8 / 12.2 | 3.06 | 0 |

## 4. Concurrency sweep (REM; same 400 episodes)

| Concurrent episodes | Episodes/s | Calls/s | Turn round trip median / p95 (ms) | REM time per call median / p95 (ms) | Errors |
|---:|---:|---:|---:|---:|---:|
| 1 | 99.7 | 208.9 | 1.5 / 2.8 | 0.17 / 0.37 | 0 |
| 2 | 110.6 | 231.8 | 2.9 / 7.6 | 0.20 / 0.41 | 0 |
| 4 | 138.4 | 289.9 | 5.0 / 12.7 | 0.19 / 0.41 | 0 |
| 8 | 166.2 | 348.1 | 8.3 / 24.0 | 0.18 / 0.38 | 0 |
| 16 | 152.0 | 318.4 | 13.4 / 43.8 | 0.19 / 0.42 | 0 |

## 5. Audit completeness and enforcement

- Episodes: 10002; calls released: 17034; calls withheld: 3234.
- Calls executed by the backend: 17034; episodes where the backend log differs from the released calls: 0.

## 6. Fail-closed probes

- unknown_episode_calls: 404
- malformed_json: 400
- unknown_configuration: 400
- backend_open_episodes_after_probes: 0

Gateway counters: `{"episodes_opened": 12002, "calls": 24458, "released": 19814, "withheld": 4644, "fail_closed": 0, "backend_errors": 0}`; gateway start-up (loading frozen components): 3 s.
