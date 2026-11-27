# Deliverable 7: Behavioral Analysis enhancement (Layer 3)

**Code:** `remdid/behavior.py`. **Status:** implemented, unit-tested, evaluated in replay (DiD-3).

REM v1.0's history features x~beh1–4~ remain inside 4B, unchanged. The new rules below are separate, deterministic, and do not repeat content detection: none of them reads text.

## 1. Rules

| Rule | Detects (task list item) | Uses | Observable under NO-ADAPT replay? |
|---|---|---|---|
| R_newpayee | Beneficiary never seen in trusted financial records, the user's request or a pinned TAE field (7.1 recipient changes; 7.2 beneficiary changes) | Recipient, L1 segments | Yes |
| R_redirect | A standing-order update that changes its stored recipient (7.2 multi-step state change) | id, recipient, stored schedule | Yes |
| R_repeat | Second or later transfer to the same recipient in the episode (7.2 repeated transfers; splitting) | Recipient history | Yes |
| R_retry | Re-proposal of a withheld call: same tool, same recipient or password (7.2 repeated calls after rejection) | Withheld list | **Only if the recorded agent happened to repeat**; adaptive retry needs live runs |
| R_switch | Another state-changing tool aimed at a withheld call's recipient (7.2 tool switching, alternative path) | Withheld list | Same |

**Not implemented:**
- sequence-model intent divergence (7.2 "divergence from task", "unusual ordering"): it needs more than 16 legitimate workflows to model;
- stale-authorization reuse, which is handled by 4A (uses, expiry);
- amount manipulation, which is handled by 4A (pinned amount, budget).

## 2. Transaction intent consistency (7.3)

- Intent consistency is decided by comparing canonical **parameters** with the TAE in 4A, not by semantic similarity of descriptions.
- Two "pay the bill" calls with different beneficiaries differ in the canonical recipient, giving 4A VIOLATION or R_newpayee.

## 3. False positives (7.4)

| Legitimate pattern | Behaviour |
|---|---|
| First payment to a new legitimate payee (bill in `user_task_0`) | R_newpayee fires → Escalate unless the recipient is pinned |
| Several payments to one recipient | R_repeat fires unless pinned |
| Retry after a technical failure | R_retry fires only after a **withheld** call, not after a tool error |

These costs are measured in DiD-3: B5 benign utility, and legitimate state-changing calls withheld.

## 4. Failure

A monitor failure is reported as unavailable. For a state-changing call this leads to Escalate (fail-safe), measured in arm F-BEH.
