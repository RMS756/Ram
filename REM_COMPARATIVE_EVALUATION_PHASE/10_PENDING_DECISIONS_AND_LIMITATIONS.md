# 10 Pending decisions and limitations

## Decisions required before any live execution

### DESIGN BLOCKED

**Item:** agent backbone and exact model version, shared by D0–D4 and used inside DRIFT.

**Why required:** every live arm.

**Current source status:** CLAUDE.md lists "LLM backbones" as unresolved. No credential exists.

**Safe action:** STOP — do not choose a value.

**Supervisor decision needed:** YES

### DESIGN BLOCKED

**Item:** number of repeats.

**Why required:** variance; DRIFT's client sends no temperature.

**Current source status:** Chapter 3 §3.11.9 says "at least three, pending approval".

**Safe action:** STOP — do not choose a value.

**Supervisor decision needed:** YES

### DESIGN BLOCKED

**Item:** which cross-fit fold's frozen REM parameters D1 uses live (`rem.fitted_parameters_source`).

**Why required:** live REM needs one fitted model.

**Current source status:** a design input of `experiments/live/live_config_TEMPLATE.yaml`, undecided. The scripted test used `injection_task_0` for plumbing only.

**Safe action:** STOP — do not choose a value.

**Supervisor decision needed:** YES

### DESIGN BLOCKED

**Item:** spending authorisation, budget cap, and a provider-side hard cap for DRIFT.

**Why required:** paid calls.

**Current source status:** none exist.

**Safe action:** STOP — do not run.

**Supervisor decision needed:** YES

### DESIGN BLOCKED

**Item:** confirmation of the bootstrap clustering (injection task / user task).

**Why required:** intervals.

**Current source status:** declared in `pilot_e0.yaml`; CLAUDE.md lists the grouping scheme as unresolved.

**Safe action:** report under the declared scheme, marked [PD].

**Supervisor decision needed:** YES

### Optional, for the supervisors

- **Progent's generated-policy mode (D2b):** add it as an arm or not. It needs a policy model, and it is the paper's main configuration.
- **MELON:** add it when OpenAI embeddings are authorised (`04`).

## Limitations of the evidence produced in this phase

1. **No live evaluation.** Every security and utility number is offline replay (NO-ADAPT) or reference-solution evaluation. A live agent can retry, replan or stop after a refusal, which may raise or lower both security and utility. The numbers are not ASRs.
2. **Development data.** REM was cross-fitted on P1. Progent's manual policy was written by its authors for this benchmark. Neither side is evaluated on data unseen by its designers.
3. **Progent's oracle advantage.**
   - Its static allow-list contains two recipients known only from task solutions or a later benchmark version (`UK123…`, `CA133…`), and it omits the attacker IBAN.
   - Every banking injection task targets that IBAN or the password, so the policy blocks all injection tasks by construction.
   - Its 0 replay attack outcomes are a property of this benchmark's fixed attacker account, not evidence about unseen attackers.
4. **The v1 `user_task_15` collision.**
   - REM's only residual replay attack outcomes (11 in P1, 2 in P2, 3 in P3) are all in `user_task_15`, where the user legitimately pays the attacker's IBAN.
   - The REM vs Progent security difference is confined to this ambiguous task.
5. **REM's over-blocking.**
   - REM completes none of the 21 recorded benign episodes for 10 of 16 user tasks in P1.
   - This is the largest utility cost observed, and it comes from the learned decision (A3 vs A0).
6. **Agent architecture.** DRIFT replaces the agent. Only D3 − D4 isolates its modules, and no DRIFT outcome has been measured.
7. **Recording conditions of P3.** The recorded runs carry no benchmark-version field, so the version under which they were produced is not recorded. The replay scores them under v1, and the AM-4 rule removes episodes whose no-defence replay disagrees with the recording.
8. **Clusters and benign sample size.** Few clusters (9 or 16) and few benign episodes (334, 48) give wide intervals for utility.
9. **Timing.** Timings are replay measurements in one container, not deployment latency. Progent's check time was timed separately from REM's per-call timer.
