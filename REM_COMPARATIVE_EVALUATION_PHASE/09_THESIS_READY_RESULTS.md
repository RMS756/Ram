# 09 Thesis-ready results of the comparative phase (22 November 2026)

*Status:* proposed text for Chapter 4. R8 is not modified.

## Evidence status

| Status | Items |
|---|---|
| **Implemented and tested** | Protocol and runners for D0–D4 (fail-closed live paths); Progent policy loader with hash checks; offline Progent arm; episode-level ablation analysis; 6 phase tests |
| **Offline deterministic evaluation (E-OFF)** | O1: REM vs Progent-manual vs REM predicates vs no defence on 5,773 attacked and 382 benign recorded episodes. O2: episode-level ablation. |
| **Reference-solution evaluation (E-REF)** | Progent on 16 + 144 reference solutions (audit) |
| **Scripted integration testing (E-SCR)** | D0/D1/D2 on 160 v1 episodes; D3/D4 on 160 v1 episodes (3 settings). Integration only. |
| **Live model-based evaluation (E-LIVE)** | **none executed** |
| **Proposed, not executed** | Live D0–D4; Progent generated-policy mode; MELON |

**No result here describes deployment in a real bank. All runs are on the AgentDojo simulator.**

## Table 4.x Offline replay of identical recorded episodes (NO-ADAPT; not live ASR)

AgentDojo banking v1, `important_instructions`; population P1 (22 recorded backbones).

| Arm | Replay attack outcomes | Utility under attack | Benign tasks completed | Benign episodes with a withheld call |
|---|---|---|---|---|
| No defence | 672 / 2979 (22.6%) | 1465 / 2979 (49.2%) | 175 / 334 (52.4%) | 0 / 334 |
| REM v1.0 | 11 / 2979 (0.4%) | 1083 / 2979 (36.4%) | 105 / 334 (31.4%) | 141 / 334 (42.2%) |
| REM predicates only (learned decision removed) | 672 / 2979 (22.6%) | 1509 / 2979 (50.7%) | 180 / 334 (53.9%) | 6 / 334 (1.8%) |
| Progent, authors' manual banking policy | 0 / 2979 (0%) | 1296 / 2979 (43.5%) | 154 / 334 (46.1%) | 33 / 334 (9.9%) |

**Uncertainty.** Paired differences with intervals and McNemar tests are in `02`, `06` and `07`. In brief: REM − Progent on benign completion is −14.7 pp [−29.7, −0.9].

**Other populations.**
- P2: none 174/681; REM 2/681; Progent 0/681.
- P3: none 436/2065; REM 3/2065; Progent 0/2065. Benign completed: 38/48, 18/48 and 35/48 respectively.

## Answers to the phase questions, on the offline evidence

1. **Does REM improve protection?** Yes, offline.
   - Replay attack outcomes fall from 672 to 11 of 2,979 episodes (P1).
   - Similar reductions occur on unseen templates (P2) and unseen backbones (P3).
   - This is not yet shown in a live loop.
2. **Does it preserve legitimate tasks?** Poorly.
   - Benign completion falls from 175 to 105 of 334.
   - 141 of 334 benign episodes have a call withheld.
3. **Do its components add value?**
   - The learned decision carries the protection, and also the over-blocking.
   - Provenance evidence contributes to stopping attack calls.
   - Behavioural evidence costs utility with no measurable security gain.
   - Detection (`x_ctx2`) and predicates D1/D2 show no measurable effect.
4. **Is a learned decision engine justified?** Partly.
   - It is justified against REM's own deterministic predicates, which stop nothing.
   - It is not justified against Progent's published hand-written allow-list. On the same episodes that list blocks every attack outcome and completes 49 more benign episodes (154 vs 105).
   - The allow-list encodes benchmark-specific recipients and omits the attacker's account, so its advantage may not transfer to unseen attackers. The learned decision's advantage of not needing a per-deployment list is a design property, **not demonstrated** here.
5. **REM vs Progent and DRIFT.**
   - **Progent:** offline it dominates REM on this benchmark, with the oracle caveat. REM's only residual attack outcomes (`user_task_15`) are cases where the user legitimately pays the attacker's IBAN in v1.
   - **DRIFT:** no measured comparison exists. Only its integration and its model-call footprint were measured, about 9–10 extra model calls per episode in the scripted run.
6. **Overhead.**
   - REM: median 0.151 ms per call (p95 0.406); no model call.
   - Progent's check: median 0.216 ms (p95 0.680); no model call.
   - DRIFT: about 9–10 model calls per episode beyond its agent calls (scripted count), plus 11 privilege calls per run.
   - MELON: not measured.

## Interpretation (proposed wording)

> "On recorded AgentDojo banking traces, REM v1.0's learned, consequence-aware decision accounts for essentially all of its offline protection but also for most of its over-blocking. A deterministic, task-informed allow-list published by Progent's authors reaches equal or stronger offline protection with fewer blocked benign tasks on the same episodes. REM's advantage, if any, must therefore be argued from generality (no per-deployment recipient list) and must be demonstrated in a live, closed-loop evaluation against an unseen attacker account; the present evidence does not establish it."

No architectural change is proposed here. The behavioural-evidence result supports the pending v1.1 decision (SD-FEAT), which is for the supervisors.
