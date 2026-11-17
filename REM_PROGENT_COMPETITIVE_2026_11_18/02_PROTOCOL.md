# Protocol: development replay of C1, C2[PG], C3[PG] (frozen 18 November 2026, before scoring)

Status: `[PROPOSED - EXPLORATORY - NOT PART OF THE APPROVED REM DESIGN]`. Design: `01_DESIGN_DECISION_RECORD.md`. Code hashes: `02_PROTOCOL_HASHES.sha256` (frozen together with this file, in the same local commit). A change to any hashed file after this commit is reported as a dated amendment. Its effect is reported next to the frozen result, never instead of it.

## What was seen before freezing (disclosed)

- **Diagnostics.**
  - The reference-labelled sequence diagnostics (`diag_harness.CASES`, labels fixed before any arm was run) were run on the frozen v2 arms (`results/f_before_v2.json`).
  - During development they were also run on C1. C1 released 0/58 unauthorized proposals and 50/62 authorized proposals; the 12 withheld were all compound totals of 60.
  - They were also run on C2[PG] and C3[PG]. Both withheld everything, because of the manual policy's recipient list.
  - The C1 numbers are therefore development results, not tests of a frozen prediction.
- **Populations.** The populations, fixtures and probe were inspected in earlier studies. No AgentDojo replay of any candidate has been run before this commit.
- **Upstream code.** The upstream Progent code was read but not executed.

## Arms

| Arm | Content | Run here |
|---|---|---|
| C1 | front (`effect, cond`; `bind=False, fulfil=False`) → predicates D1/D2 → contract witness with ledger | replay, diagnostics, fixtures |
| C2PG | C1 with Progent's manual banking policy (commit 9befb41, REM's replay checker) after the front | replay, diagnostics, fixtures |
| C3PG | C2PG + stored ridge F4 / Platt / two-verdict expected loss after the witness (may only withhold) | replay (S1 and S2), diagnostics, fixtures |
| references | REM10, PG, G3, GV, HV (stored), GV_math2, HV_math2, GV_math2x, HV_math2x (stored v2 replays) | stored |
| P0, C2[gen], C3[gen] | full Progent with generated or updated policies, alone and composed | **not run** (see `05_CLOSED_LOOP_PROTOCOL.md`) |

## Populations and procedure

The populations, folds, cells and statistics are the same as in the repair study (`rs_run.py`, `rs_run_v2.py`):
- primary S1 and S2;
- the second population (dev2, eligibility as before);
- the reformatted-identifier probe;
- the four fixture sets (43 fixtures);
- paired grouped bootstrap with 2,000 resamples and seed 20261027 (via `R.paired`).

Execution is offline replay of recorded calls (NO-ADAPT): the recorded agent does not react to refusals.

Commands (environment of the competitive study):

```
python3 experiments/progent_competitive/cp_run.py replay
python3 experiments/progent_competitive/cp_run.py diag
python3 experiments/progent_competitive/cp_run.py report
```

## Outcomes reported (all of them, whatever their direction)

- **Per population and arm:** attacks successful / attacked episodes; benign tasks completed / benign; all tasks completed; replay errors.
- **Paired contrasts:**
  - C2PG−C1 (Progent's manual policy added to the contract);
  - C2PG−PG (contract added to Progent's manual policy);
  - C3PG−C2PG (learner);
  - C1−GV_math2, C1−GV_math2x, C1−PG, C1−REM10;
  - C2PG−GV_math2x and C3PG−HV_math2x.
- **Episode-level outcome changes** for each contrast, by user task.
- **Restricted-call stage counts** by attack label, plus the contract reasons.
- **Fixtures:** legitimate released, unsafe released, pairs correct.
- **Diagnostics:** authorized released / n, unauthorized released / n and ambiguous released / n, with the withheld reasons.

No adoption criterion is set in this study. Adoption of any candidate is a separate supervisor decision.

## Interpretation limits fixed in advance

- **Development evidence only.** The populations were seen before. This is not independent validation.
- **The diagnostic cases are author-written.** They test the defects they were written for; they are not an attack-success rate.
- **Offline replay understates refusal costs.** It cannot show an agent's recovery after a refusal (retry, replan), nor an attacker's adaptation.
- **C2PG is not full Progent.** It uses only Progent's manual policy. The comparison with full Progent (generation, update, Auto-Deny/Auto-Approve) requires the closed loop and a model.
- **Declared assumption (evidence integrity).** `get_balance` and the structured transaction fields are trusted operands (`01_DESIGN_DECISION_RECORD.md`).
