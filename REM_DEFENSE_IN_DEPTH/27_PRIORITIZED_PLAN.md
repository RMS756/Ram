# Prioritized implementation plan (feasibility first; nothing merged into `rem/` without a decision)

**Order of work:** every item first gets a feasibility study under a committed protocol, run in an isolated experimental module as in earlier studies. Only after a supervisor decision does the item enter `rem/` as a versioned change.

| Priority | Item | Why first | Feasibility study (offline unless noted) | Decision gate |
|---|---|---|---|---|
| **F1** | Oracle TAE and constraints A1–A9 (4A) in front of REM v1.0's 4B | It addresses the largest measured weakness: authorization is not represented, and over-blocking follows | Replay on POP-P, POP-R and the second population. Arms: oracle-TAE 4A alone; oracle-TAE 4A + 4B; confirmed-draft TAE 4A (+ 4B); REM v1.0; P2; Progent's policy. Report attacks, benign tasks, legitimate calls released, and 4B's added value. Report user_task_15 separately. | Is the upper bound worth a trusted channel? |
| **F2** | Canonical value lineage (L1) | Removes the reformatting route; a specification already exists | Reformatting probe and DiD-2 rerun; lineage unit tests | Feature change (SD-FEAT) |
| **F3** | Deduplicate x~beh1~; credential-integrity evidence (L3) | It removes a correlation of 1.00 and a single-family dependency | Refit; DiD-1, DiD-2 and the probe on the new feature set; legitimate firing rates | Feature change |
| **F4** | Call-linked injection evidence and separated sub-signals (L2) | Detection currently adds no depth | SIG-1 and DiD-2 with the new signals; all five templates | Feature change |
| **F5** | Parameter-bound permits and fail-safe fault injection (L5) | Verifiable enforcement; no change to verdicts | Gateway tests (mutation, fault injection) | Low risk; still declared |
| **F6** | Measure 4B's value behind 4A, then decide 4B's role | Required by the task: do not assume the learned decision helps | Part of F1 | Supervisor |
| F7 | Injection classifier x~ctx1~ | Needs a model choice | Offline if a local model is approved; otherwise **R** | D-8 |
| F8 | Retry and alternative-route tracking; reviewer channel; Modify mechanism | Needs an adaptive agent or a reviewer | **R:** live runs; reviewer simulation | Supervisor, budget |
| F9 | Sequence model of legitimate workflows (replacing x~beh4~) | Needs data on legitimate complex workflows beyond 16 tasks | **R:** second benchmark | Supervisor |

**Stop rules:**
- If F1's oracle upper bound does not reduce over-blocking at equal security, the TAE direction is reported as not useful on this benchmark, and F6 is moot.
- If F2–F4 do not change DiD-2's family-evasion results, they are reported as such and not adopted.
- Every negative result is reported.
