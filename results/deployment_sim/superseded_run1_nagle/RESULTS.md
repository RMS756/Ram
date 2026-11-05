# Deployment simulation — results

Run: `results/deployment_sim/2026-11-05_full`; REM commit `adadff4`; 3334 recorded episodes; 4 vCPU; main concurrency 4.

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
| B0 | 21.7 | 6756 | 0.11 / 0.31 | 43.9 / 49.9 | 0.75 | 0 |
| B1 | 21.8 | 6756 | 0.20 / 0.42 | 43.9 / 48.7 | 0.91 | 0 |
| REM | 21.9 | 6756 | 0.22 / 0.43 | 43.9 / 48.5 | 1.24 | 0 |

## 4. Concurrency sweep (REM; same 400 episodes)

| Concurrent episodes | Episodes/s | Calls/s | Turn round trip median / p95 (ms) | REM time per call median / p95 (ms) | Errors |
|---:|---:|---:|---:|---:|---:|
| 1 | 5.5 | 11.5 | 43.9 / 47.9 | 0.27 / 0.50 | 0 |
| 2 | 10.9 | 22.9 | 43.9 / 47.9 | 0.24 / 0.45 | 0 |
| 4 | 21.5 | 45.1 | 43.9 / 49.9 | 0.24 / 0.45 | 0 |
| 8 | 40.6 | 85.1 | 44.2 / 55.7 | 0.21 / 0.41 | 0 |
| 16 | 74.9 | 157.0 | 47.3 / 65.7 | 0.19 / 0.42 | 0 |

## 5. Audit completeness and enforcement

- Episodes: 10002; calls released: 17034; calls withheld: 3234.
- Calls executed by the backend: 17034; episodes where the backend log differs from the released calls: 0.

## 6. Fail-closed probes

- unknown_episode_calls: 404
- malformed_json: 400
- unknown_configuration: 400
- backend_open_episodes_after_probes: 0

Gateway counters: `{"episodes_opened": 12002, "calls": 24458, "released": 19814, "withheld": 4644, "fail_closed": 0, "backend_errors": 0}`; gateway start-up (loading frozen components): 3 s.
