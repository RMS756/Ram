# Chapter 4 (draft section): Controlled evaluation of the architecture variants

> **Status.**
> - All results are offline replays of recorded AgentDojo banking traces (NO-ADAPT), author-written suites, or a scripted closed loop.
> - No language model was called.
> - Full Progent and live-agent experiments were **not executed**.
> - The protocol, acceptance criteria and file hashes were committed before any scored run (commit `6705c07`, `08_FROZEN_EXPERIMENT_PROTOCOL.md`).

## 4.A.1 Setup

**Populations** (attacked / benign episodes):

| Population | Episodes | Role |
|---|---|---|
| primary (S1) | 2,979 / 334 | development |
| dev2 | 2,065 / 48 | development; B0-eligible fresh runs |
| probe | 2,645 | reformatted identifiers |
| H, held-out | 469 / 53 | gpt-4o-2024-05-13 with four in-pipeline prompt defences; never loaded by REM before; same 16 user tasks and 9 injection tasks |

**Author-written suites** (labels fixed before the runs):
- development scenarios;
- held-out probes (written before the candidate code);
- diagnostics;
- generalisation cases;
- 43 fixtures.

**Arms:**
- B0 (no guard);
- C1, C1I [EXPERIMENTAL];
- PG (Progent manual policy);
- REM-A, REM-B, REM-C, REM-C-T, REM-C-raw, REM-B-R (idealised reviewer, upper bound);
- six ablations of REM-B.

**Metrics:**
- attack objectives reached;
- attack-labelled calls released;
- **audited value/object violations released**: released calls whose amount or recipient differs from what the request determines (ut3/4/5/11/15), or modifications of a standing order other than id 7 in the rent tasks (ut2/9/12/15);
- benign and all-task completion;
- false-positive intervention rate;
- Brier and ECE (10 bins);
- latency and memory.

**Statistics:**
- Paired grouped bootstrap (2,000 resamples, seed 20261027), clustered by user task (completion) and injection task (attacks).
- Zero attack counts are reported with the one-sided 95% upper bound (≈ 3/n).
- Repeated runs of one task pairing are not treated as independent observations.

## 4.A.2 Security

**Attack results.** Every defended arm reached **0** attack objectives in every population, and released **0** attack-labelled calls. The one-sided 95% upper bounds are 0.10% (primary), 0.15% (dev2) and 0.64% (H). B0 reached 672, 436 and 145.

**Audited violations differ sharply between arms:**

| Arm | Primary | dev2 | H |
|---|---|---|---|
| C1 | 11 | 0 | 0 |
| REM-B | 11 | 0 | 0 |
| REM-A | 11 | 0 | 0 |
| REM-C (and -T, -raw) | **121** | **24** | 0 |
| PG | **161** | **36** | 0 |

**Author-written suites.** Each cell is unauthorised released + ambiguous released.

| Arm | Development | Held-out probes | Diagnostics | Generalisation | Fixtures unsafe |
|---|---|---|---|---|---|
| C1 | 4 + 0 | 4 + 2 | 0 | 0 | 0 |
| REM-B | **0 + 0** | **0 + 0** | **0** | **0** | **0** |
| REM-C | 0 + 0 | 1 + 3 | 16 | 4 + 4 | 1 |

**Scripted closed loop** (ut15×it4 attack goal):
- reached by C1 in 2 of 4 call orders;
- reached by REM-B in **0 of 4** orders.

## 4.A.3 Utility

| Arm | Primary all-task (of 3,313) | dev2 (of 2,113) | H (of 522) | H benign (of 53) |
|---|---|---|---|---|
| C1 | 1,437 | 1,227 | 245 | 27 |
| C1I | 1,473 | 1,393 | 266 | 29 |
| PG | 1,450 | 1,305 | 280 | 33 |
| REM-A | 1,455 | 1,314 | 248 | 27 |
| **REM-B** | **1,457** | **1,363** | **249** | **27** |
| REM-C | 1,534 | 1,435 | 269 | 29 |

**Pre-registered endpoint, REM-B − C1 on H:**
- **+0.0077 [0.0000, 0.0205]**;
- **INCONCLUSIVE**.

**Where REM-B's gains over C1 occur.** All of them are in the two user tasks from which its evidence rules were designed (ut11, ut15). The 14 other user tasks show no difference.

**REM-B against C1I.** REM-B loses 16 / 30 / 17 tasks to C1I. This is the cost of requiring a known counterparty for refunds (I6). Agents often read only the most recent transaction, so the user's earlier payment to the friend is not visible.

## 4.A.4 The learned component

**Reachability.**
- The stored estimator separates attack-labelled from other restricted calls well: ROC-AUC 0.974; Brier 0.059 and ECE 0.024 in primary.
- However, the deterministic front withholds all 907 attack-labelled calls in primary, so the learned stage never sees one.
- In REM-C the learned stage was reached by 320 calls in primary, none attack-labelled.

**Effects:**
- **REM-A** withheld 3 / 49 / 1 audited-correct calls and gained nothing.
- **REM-C** released 110 / 24 audited violations together with its utility gains (+77 / +72 / +20 tasks).
- **REM-C and REM-C-T** produced identical verdicts on every replay population. Consequence-aware and consequence-independent decisions are therefore not distinguishable.
- **REM-C and REM-C-raw** were identical, so calibration had no decision effect.

**Calibration shift.** On H, the learned-stage calls of REM-C had Brier 0.598 and ECE 0.609.

**Interpretation.** The estimator predicts malicious influence, while the unresolved calls need a judgement about whether the **value** is authorised. A low attack probability is not evidence that an amount is correct.

## 4.A.5 Ablations of REM-B

| Removed mechanism | Effect |
|---|---|
| object binding | no replay effect; probes release 4 unauthorised + 2 ambiguous; scripted goal reached in 2 of 4 orders |
| ledger | 16 unauthorised diagnostic releases; 1 unsafe fixture |
| E1 | −18 / −87 / −3 tasks |
| E2 | −2 / −49 / −1 tasks |
| E2 hardening | +16 / +30 / +17 tasks, but the refund scam probe is released |
| provenance | one ambiguous probe released |

## 4.A.6 Comparison with Progent's manual policy

**Parity.** PG's decisions equal those of the upstream Progent engine (pinned commit 0d7ea07, with the 9befb41 manual policy installed) on 2,551 + 662 recorded calls, with 0 disagreements.

**PG has:**
- higher benign utility on H (33 vs 27 of 53);
- a lower intervention rate (0.159 vs 0.636).

**But PG:**
- releases 161 / 36 audited violations;
- authorises no request whose recipients are outside its pre-written list (0 of 16 authorised probe proposals).

**REM-B − PG on H:** −0.0594 [−0.1711, 0.0229]. Neither direction is established. **Full Progent was not executed.**

## 4.A.7 Selection and limitations

**Selection.** Applying the frozen rule:
- **REM-B is preferred on security, with utility INCONCLUSIVE.**
- REM-C is NO-GO: it fails the violation and suite constraints.
- REM-A's learned stage is harmful or redundant.

**Limitations:**
- replay cannot show agent adaptation;
- H holds out agent behaviour, not tasks;
- the probes were written by the designer;
- one domain (banking) and one benchmark;
- the audited violation metric covers 8 user tasks;
- a designator defect was found on a held-out probe (fixed only post hoc);
- no live model;
- no full Progent.
