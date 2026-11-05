# REM Deployment Simulation

**What this is:** REM deployed as a separate network service, the **REM gateway**, at the tool-execution boundary of a banking agent. It sits in front of a separate **simulated banking API**. The traffic is the recorded behaviour of **21 real LLM agents**: 3,334 AgentDojo banking episodes, attacked with `important_instructions` and benign, replayed turn by turn over HTTP.

**What it is not:**
- not a live or adaptive agent: the recorded agents do not react to refusals (NO-ADAPT, as in the thesis's replay, §4.6);
- not a real bank or real money;
- not a production deployment.

The design values are the exploratory pilot values (not supervisor-approved).

## Architecture

```
 recorded agent (AgentDojo pipeline + ReplayLLM)        REM gateway (rem/deployment/gateway.py)        simulated banking API
 replay_client.py: RemoteExecutor  --HTTP/JSON-->  per call: RemGuard.evaluate  --released only-->  bank_backend.py
   (one request per assistant turn,                  (frozen estimator, calibration, tiers,          (AgentDojo banking v1 env
    all calls in order, ids kept)                     predicates, expected-loss verdict, audit)        per episode; AgentDojo's
                                   <-- results / refusals ("REM: ...") with the same call ids --       own utility/security checks)
```

- **Separation:** three operating-system processes (client, gateway, backend). The gateway and the backend are multi-threaded HTTP servers. One REM guard and one environment per episode; per-episode locks; episodes run concurrently.
- **Frozen components** (`serve_gateway.py`): built from the frozen cross-fit state exactly as in the thesis's replay. The fold per episode is the held-out cross-fit assignment. Configurations, all with step-level mitigation and no reviewer:
  - **B0:** REM disabled; allow-all;
  - **B1:** consequence-independent baseline on the same estimator;
  - **REM:** expected-loss verdict.
- **Fail-closed:**
  - an internal REM error withholds the call;
  - unknown or malformed requests get a 4xx response and nothing executes;
  - a backend failure is an infrastructure error, not a decision.

## What is measured

1. **Parity:** every episode outcome (utility, security, error status) and every per-call (label, verdict, released, tier, tool) is compared with the thesis's in-process replay (`state/replay_main.pkl`). Deployment must not change any decision.
2. **Outcomes:** ASR, utility under attack and benign utility on the 3,313 valid episodes, as in §4.6.
3. **Latency:**
   - REM decision time per call, inside the gateway;
   - backend execution time;
   - end-to-end round trip per agent turn (client → gateway → backend → client);
   - episode wall time.
4. **Throughput** under 1, 2, 4, 8 and 16 concurrent episodes (REM configuration; 400 fixed episodes).
5. **Audit completeness:** one audit record per evaluated call; the backend's execution log equals the released calls; no withheld call reached the backend.
6. **Fail-closed probes:** unknown episode, malformed JSON, unknown configuration.

## Reproduce

```bash
PILOT_RESULTS_DIR=<frozen pilot state> python3 experiments/deployment_sim/run_deployment_sim.py \
    --out results/deployment_sim/<run_id>
python3 -m pytest -o addopts="" tests/test_deployment_gateway.py       # 6 gateway tests
```

## Results (run `results/deployment_sim/2026-11-05_full`, 5 Nov 2026; full tables in its `RESULTS.md`)

**Setting:** 4 vCPU; client, gateway and backend on one machine (localhost); 3,334 episodes × 3 configurations at 4 concurrent episodes; the sweep uses 400 fixed episodes.

| Check | Result |
|---|---|
| **Parity with the thesis's in-process replay** | **0 mismatches** in 3,334 episodes × 3 configurations (utility, security, error status, and every per-call label / verdict / release / tier / tool) |
| **Outcomes on the 3,313 valid episodes** (identical to §4.6) | ASR: B0 0.226, B1 0.055, REM 0.004. Utility under attack: 0.492 / 0.514 / 0.364. Benign utility: 0.524 / 0.509 / 0.314 |
| **Calls evaluated per configuration** | 6,756, withheld: B0 0, B1 1,016, REM 2,218. (The data set counts 6,762 recorded steps; 6 episodes recorded a 16th call beyond AgentDojo's 15-iteration tool loop, which the replay, offline and deployed alike, never reaches.) |
| **Enforcement** | Backend executed exactly the 17,034 released calls; **none of the 3,234 withheld calls**; 0 episodes where the backend log differs from the released calls |
| **REM decision time per call** (inside the gateway) | median 0.19 ms, p95 0.40 ms (B0 pass-through: 0.09 / 0.30 ms) |
| **Agent-turn round trip** (client → gateway → backend → client, 4 concurrent) | median 4.8 ms, p95 12.2 ms (REM); 5.6 / 13.0 ms (B0). REM's own time is a few percent of the round trip; the remaining difference between configurations is noise |
| **Throughput** (REM, 1 / 2 / 4 / 8 / 16 concurrent episodes) | 99.7 / 110.6 / 138.4 / 166.2 / 152.0 episodes/s; peak about 348 calls/s at 8, then saturation (Python servers sharing 4 vCPU). p95 round trip rises from 2.8 ms (1) to 43.8 ms (16) |
| **Errors / fail-closed** | 0 errors; 0 fail-closed events, 0 backend errors. Probes: unknown episode → 404, malformed JSON → 400, unknown configuration → 400, nothing executed |

A first run had identical decisions but invalid latency figures (Nagle/delayed-ACK stall in the prototype servers); see `results/deployment_sim/superseded_run1_nagle/README.md`.

**Limits:**
- NO-ADAPT recorded agents;
- a simulated bank on one machine, without real network distance or a production web server;
- exploratory REM design values;
- single-process Python prototype servers, so the throughput figures describe this prototype, not an optimised deployment.

The simulation shows that REM can run as a separate service at the tool boundary **without changing any decision**, with sub-millisecond decision time. It does not show protection of adaptive agents.
