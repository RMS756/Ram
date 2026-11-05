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
