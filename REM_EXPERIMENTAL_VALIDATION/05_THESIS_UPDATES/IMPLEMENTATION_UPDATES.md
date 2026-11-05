# Implementation — update draft (for the "Implementation tools and environment" section)

| Item | Text to add (verified) |
|---|---|
| Environment | Python 3.11.17; NumPy 2.4.6 (main environment); AgentDojo 0.1.35 for REM's evaluation; a separate AgentDojo 0.1.29 environment for MELON (torch 2.9.1, transformers 5.22.1, openai 3.46.0); 4 vCPU cloud container |
| REM deployment gateway | `rem/deployment/gateway.py`: REM as an HTTP service at the tool boundary. Per-episode guard and lock; fail-closed on internal error, unknown or malformed requests; only released calls are forwarded to the tool backend; audit record per call |
| Simulated banking API | `experiments/deployment_sim/bank_backend.py`: AgentDojo banking v1 environment per episode; AgentDojo's own success checks; execution log |
| REM-Lite | `experiments/rem_lite/run_rem_lite.py` and gateway configuration `REMLITE` |
| MELON integration | `rem/integration/melon_rem.py`: hash-checked loading of the official file, which is not vendored (no licence); REM replaces only the tool executor in MELON's loop |
| Tests | 233 pass (main environment); 30 pass (MELON environment) |
