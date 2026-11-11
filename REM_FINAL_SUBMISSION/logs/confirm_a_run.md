# Confirmatory run log (CONF-A)

- Date: 11 November 2026 (UTC). Protocol frozen at commit `19bd168` before the fresh recordings were opened.
- Commands: `PYTHONHASHSEED=0 PILOT_RESULTS_DIR=<pilot state> AUTHZ_STATE=<study state> python3 experiments/authz_study/confirm_a.py run` then `... report`.
- Files read: 2,162; excluded as ambiguous pairs (AM-1): 14; loaded: 2,148; eligible under AM-4: 2,113 (2,065 attacked, 48 benign).
- Replays: 17,184 (2,148 episodes x 8 arms); replay errors: 0.
- Bootstrap: grouped, 2,000 resamples, seed 20261027.
- Environment: Python 3.11.17, numpy 2.4.6, agentdojo 0.1.35, AgentDojo runs commit `089ed468cf3ed0322acc66b0211f26d9d90dbf60`.
- Output: `REM_FINAL_SUBMISSION/results/confirmatory_results.json` (sha256 `0c25582466669fbf5314cd52d4d25cccb2f91ed87444bf998736cf4cab127b2e`).
- Replay state (not committed, regenerable): `confirm_a.pkl` (sha256 `3d663addf66ade8d0e57f1db3f0796c11eba66b46bdd0ff3ca3ff47ff5f732c3`).
- Amendments to the protocol: none.
