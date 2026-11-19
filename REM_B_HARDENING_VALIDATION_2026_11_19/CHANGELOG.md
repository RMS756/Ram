# Change log: REM-B hardening study

All changes are additive. No file in `rem/`, in earlier experiment folders or in earlier study folders was modified.

| Commit | Change |
|---|---|
| `8a9e6a2` | baseline verification; HO4 trace; benign-failure analysis (development populations); **probes v2** and **H2 rule**, before any candidate code |
| `f6d885b` | `remb2.py` (R1, R2, R3, hybrids HR / HW, environment-capture replay); `hard_run.py`; `export_calls.py`; tests; documents 01–05; **frozen protocol 06** + hashes |
| `f74d6e3` | frozen suite and fixture results; **amendment protocol 06a** + probes v3 (before amendment code; no H2 result existed yet) |
| `37f0157` | `remb3.py` (F1a, F1b, F2) and amendment tests (additions only), hashed |
| final | replays, reports, scripted, cost, Progent parity on H2, tables, figure, documents 06b–16, manifest |

## Known issues (reported, not hidden)

- **H2a has no banking runs.** H2 is only the previously loaded gpt-4o cross-template set, with no benign episodes (`06b` D1).
- **Probes v2 barely exercised object binding**, because of compiler wording coverage (`06b` D2).
- **Every REM-B variant fails held-out probes** because of request-compiler errors (`12`).
- **R3 changes conditional-authority semantics** and needs supervisor approval.
