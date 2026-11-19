# 14 Thesis-ready results section (draft)

> **Status labels.**
> - [APPROVED] = REM v1.0.
> - [PROPOSED - EXPLORATORY] = the authorisation-first variants REM-B, REM-B2 and REM-B3.
>
> All results are offline replays of recorded AgentDojo banking traces under the NO-ADAPT assumption, author-written probe suites, or a scripted closed loop. No language model was called. Full Progent and live-agent experiments were not executed.

## 4.B.1 Setup

Three repairs were added to the authorisation-first variant REM-B. Each was derived from a root-cause analysis of the development populations.

| Repair | What it does |
|---|---|
| R1 | Object designators exclude identifier tokens |
| R2 | Evidence resolution reads the bank's structured records at decision time |
| R3 | Credential and profile changes whose values the user fixed are released under a judgement condition the user delegates to the agent |

The result is REM-B2. Two hybrids were tested alongside it: one that only ranks the human-review queue, and one that can only withhold. Protocol, criteria and file hashes were committed before any scored run.

**Held-out material:**

| Material | Contents |
|---|---|
| Recorded traces H2 | 681 attacked episodes of gpt-4o-2024-05-13 under five attack phrasings not used in design (previously loaded once for older arms) |
| Probes v2 | 26 author-written cases, 73 labelled calls, labelled before the repairs were implemented |

A post-hoc amendment (REM-B3) was evaluated on a further 11 author-written cases (probes v3), labelled before its code.

## 4.B.2 Security

**Attacks.** No defended arm reached an attack objective in any replayed population. The one-sided 95% upper bounds are:

| Population | Attacked episodes | Upper bound |
|---|---|---|
| primary | 2,979 | 0.10% |
| dev2 | 2,065 | 0.15% |
| probe | 2,645 | 0.11% |
| H | 469 | 0.64% |
| H2 | 681 | 0.44% |

The undefended agent reached 672, 436, 553, 145 and 174.

**Value integrity on recorded traces.**

| Arm | Audited value / object violations (primary, dev2, probe) |
|---|---|
| REM-B2 | 11 / 0 / 9 |
| REM-B | 11 / 0 / 9 |
| Progent's hand-written policy | 161 / 36 / 125 |

**Held-out probes.** REM-B2, REM-B and C1 released 3 of 33 unauthorised proposals on probes v2:
- amounts swapped between two named payees;
- an unrequested amount change on the correct standing order.

The amendment REM-B3 closed those classes, but released 1 of 23 unauthorised proposals on probes v3: the request compiler typed an immediate payment as a standing order.

Progent's policy released 3 and 4 unauthorised proposals on probes v2 and v3, of other kinds: an address change, unrequested amount changes, an unrequested operation.

**Scripted loop.** In the scripted closed loop, REM-B2 reached the attack goal in 0 of 4 call orders; removing object binding brought it back in 2.

## 4.B.3 Utility

| Arm | H2 tasks completed under attack (of 681) | Primary tasks (of 3,313) |
|---|---|---|
| C1 | 392 | 1,437 |
| REM-B | 393 | 1,457 |
| PG | 417 | 1,450 |
| **REM-B2** | **476** | **1,640** |
| REM-B3 | 404 | 1,555 |
| Original REM v1.0 | – | 1,188 |

**Pre-registered endpoint.** REM-B2 − REM-B on H2 = **+0.122 [0.000, 0.305]**. All 83 gained episodes are in two user tasks: ut14 through R3, and ut15 through R2. The other 14 tasks are unchanged, so the cluster-bootstrap lower bound is 0.

REM-B2 − PG on H2 = +0.087 [−0.141, 0.318].

The amendment's field-scope rule withheld 73 audited-correct standing-order updates on H2 and prevented no recorded violation.

## 4.B.4 Learned components

| Variant | Result |
|---|---|
| Withholding hybrid | Changed no verdict |
| Review-ranking hybrid | No defined endpoint on H2 (all escalated auditable calls were correct). On development data the stored score's ranking was worse than chance in two populations (AUC 0.23, 0.22) and better in one (0.60). |

No learned component was retained.

## 4.B.5 Decision

| Candidate | Decision |
|---|---|
| REM-B2 | **NO-GO** under the frozen rules (held-out probe constraint failed) |
| REM-B3 | **NO-GO** (post-hoc; held-out probe constraint failed, utility regression) |
| Hybrids | NULL / rejected |

No claim of superiority over Progent is supported.

## 4.B.6 Interpretation

- **What works.** Deterministic mediation at the tool boundary stops every recorded attack, and the REM-B family preserves value integrity on recorded traces far better than an allow-list.
- **What limits it.** Its security on *new* requests is limited by the correctness of the natural-language request compiler that derives the authorisation. Three successive held-out probe sets each exposed a new compiler error that led to an unauthorised release.
- **What it means.** This identifies verified intent compilation, not risk estimation, as the open problem for request-derived authorisation of financial agents.

## 4.B.7 Limitations

- Offline replay (no adaptation).
- One benchmark and one domain.
- H2 is not pristine and has no benign episodes.
- All probes were written by the designer; no independent validation.
- The audited-violation metric covers 8 user tasks.
- No live model.
- No full Progent.
