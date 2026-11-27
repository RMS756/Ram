# A1-10: Reassessment of D2 (transaction ledger) and D3 (failure-independence testing)

## D2: one transaction ledger across authorization, enforcement and reconciliation

### Adopted mechanisms, labelled [PA]

| Mechanism | Adopted from (level) | Established property |
|---|---|---|
| Grants bound to exact parameters, expiring, limited-use | AGATE (A), AIS (A), AgentCap (A), GuardRail (A) | A permit cannot authorize a different call, or the same call more times than granted |
| Repeated-request tracking | AGATE effect ledger (A/S: recent request keys per session); ScopeGate idempotency (A) | The same request is not executed twice |
| Token replay rejection | AIS (S: all four token replays rejected in their evaluation) | Replay of authority is refused |
| Exact economic terms checked before authority is issued | AIS (A) | Amount, recipient and rail are fixed by the intent |
| Execution-side verification independent of the inference layer | AIS EVM verifier (A), AgentCap tool-boundary validation (A), AGATE host adapters (A) | Enforcement does not trust the decision layer's output alone |
| Replayable assurance, forensic replay | AIS (A), AGATE (A) | Decisions can be reconstructed with execution evidence |
| Reserve, then commit or release | Standard transaction-processing practice | Concurrent operations cannot jointly exceed a shared limit. **A specific textbook reference must be selected and cited [REFERENCE NEEDED].** No new formulation is offered |

### Deduplication versus cumulative exposure (see A1-03 §2)

- **Deduplication** stops the *same* request from repeating.
- **Cumulative exposure limits** stop *many different* requests from together exceeding what the user declared.
- **AGATE, at the level read, provides the first.** The second is provided in REM-DiD as a per-authorization budget [DiD-T]. REM-X proposes extending it per recipient and per session [X-P].

### Established versus unverified

| Property | Status |
|---|---|
| Each adopted mechanism above works as published | Established in the cited works, at the stated evidence level; not re-verified by us |
| **One** ledger shared by 4A reservation, L5 permit issuance, the adapter's independent re-check and post-execution reconciliation, so the economic terms checked at each point are the same record | **Unverified integration property [X-P].** AIS's journal version states, at level S, that "reservation and consumption tracking is not integrated into the EVM gate". That suggests the integration is not trivial, but it does not make it new |
| Cumulative limits hold when calls are interleaved or concurrent | Unverified [X-P]; testable with deterministic fixtures |
| Reconciliation detects an adapter that executes different terms | Unverified [X-P]; testable by fault injection |

**Position.**
- D2 remains **engineering adoption**. It is included because the amount and split-transfer threats need it.
- **No contribution claim is made for it.**

## D3: removal versus evasion in failure-independence testing

### Prior-art support

| Source | What it shows (level) | Relation to D3 |
|---|---|---|
| "The Attacker Moves Second" (arXiv 2510.09023) | Adaptive attacks bypass 12 published defenses; on AgentDojo, prompting defenses rise from low to high attack success under search-based attacks (S) | Shows adaptive attacks defeat **individual** defenses. Not a layered, per-component evasion study |
| Progent | Approver ablations and adaptive attacks (F) | Removal-style ablation plus adaptive attacks on the whole system |
| AIS, CaMeL, ROPE | Mechanism or policy-mode ablations (A/R) | Removal-style |
| AGATE | Bypass through parameter rewriting observed in deployment (A/S) | An observed component failure, not a designed evasion matrix |
| Narisetty et al. | Adaptive evaluation of out-of-band defenses (earlier review, level A) | Closest in spirit; whether it fixes other components while evading one is n.d. |
| Multi-agent defense-architecture paper (arXiv 2609.22949) | Argues that layered controls raise the cost of adaptation (S) | Argument, not measurement |

**Assessment.**
- At the levels read, no source was found that measures each control's **evasion with all other controls held fixed** and compares it with **removal** of that control.
- **Absence at A/S level is not evidence of absence.** The search was limited, and full texts were not read.
- The idea also follows directly from standard adaptive-attack reasoning. **It is a methodological practice, not a novel method.**

### Position

- D3 is **retained as a proposed evaluation requirement** [PD]:
  - every defense-in-depth claim made for REM-X is tested by test-time evasion of each control with the others fixed, as well as by removal;
  - results are reported per threat class.
- **No novelty claim.** At most, the thesis may report that **on REM's own components** removal and evasion gave opposite conclusions:
  - DiD-2: 11 vs 11 attacks after removing the behavioral family; 653 vs 90 under evasion.
  - This is an empirical observation about REM, recorded in `REM_DEFENSE_IN_DEPTH/05`.
- The earlier "joint vs marginal miss rate" comparison and the "≥ 2 controls" pass criterion are **withdrawn** (A1-11). They are not replaced by any other formula.
- How resilience and independence are judged must be specified from an established reference, or by an explicit researcher/supervisor decision.
