# Deliverable 4: Trusted Authorization Envelope as implemented (supersedes the proposal in file 23 where they differ)

**Code:** `remdid/tae.py`, `remdid/oracle.py`. **Tests:** TAE group in `tests/test_remdid_components.py`; scenarios 01–09 and 14.

**Status:** implemented and tested. **The trusted issuing interface does not exist in AgentDojo.** Entries are issued by evaluation oracles (§4), which stand in for an authenticated approval user interface.

## 1. Entry

| Field | Meaning |
|---|---|
| `operation` | Tool name of the authorized state-changing operation |
| `fields` | Per sensitive field: `specified` (pinned canonical value), `unspecified` (the user did not state it), or `any` (wildcard: over-broad authorization) |
| `amount_mode` | `exact` or `max` (a cumulative budget across uses) |
| `currency`, `source_account` | Checked when the call carries them; `not_applicable` for AgentDojo tools, which have neither |
| `max_uses` | One-time or limited use, with an atomic counter |
| `expires_at_decision`, `expires_at_wallclock` | Expiry |
| `session_id`, `nonce` | Binding to the session; uniqueness |
| `approval_evidence` | Must not start with `model`, `tool` or `llm`: the origin rule is enforced in code |
| `mac` | HMAC-SHA256 over the canonical JSON of all fields above; the key is held by the store only |

**Unspecified parameters are never invented.**
- An `unspecified` field leads to `AUTH_unspecified`, then Escalate (clarification or confirmation needed).
- A field the entry does not mention may not be changed. The exception is when the call sets it to its current stored value (for example, a standing order's current recipient).

## 2. Matching outcomes (Layer 4A)

| Outcome | Condition | Verdict (precedence P1/P2) |
|---|---|---|
| AUTHORIZED | All pinned fields equal; no unauthorized field change; within budget and uses | — (other layers decide) |
| VIOLATION | Pinned field mismatch (recipient, amount, currency, source account), unauthorized field change, budget exceeded | **Block** |
| NO_ENTRY | No entry for the operation | **Block** |
| UNSPECIFIED | Matching entry with an unspecified field | Escalate |
| UNVERIFIABLE | MAC mismatch, other session, expired, uses exhausted | **Block** |
| Store or evaluator unavailable | Infrastructure failure | Escalate (fail-safe) |

## 3. Integrity: what is and is not guaranteed

**Implemented and tested:**
- detection of any modification of a stored entry (MAC);
- cross-session rejection;
- logical and wall-clock expiry;
- one-time and limited use;
- cumulative amount budget (blocks split transfers beyond the budget: scenario 07).

**Not provided:**
- protection if the store process or key is compromised (assumption AS-3);
- key management or rotation;
- non-repudiation of the approving user;
- secure display: what the user sees when approving is outside REM.

**No cryptographic guarantee beyond HMAC integrity within one trusted process is claimed.**

## 4. Offline issuers (evaluation oracles, not deployable)

| Mode | Fields | Purpose |
|---|---|---|
| `oracle` | Every sensitive field of every ground-truth call pinned | Upper bound: user confirmed exact parameters |
| `explicit` | Pinned only if the canonical value occurs in the user's own request; otherwise unspecified | Cost of refusing to invent unstated parameters (no NL intent compilation; earlier compilation attempts were NO-GO) |
| `broad` | All fields `any`, unbounded uses | **Bypass model:** the attacker acts inside an authorized operation |
| `none` | No entries | Authorization unavailable |

**Benchmark caveat.** `user_task_15` legitimately pins the attacker IBAN as the new landlord (collision). Authorization cannot separate that case. It is reported separately.
