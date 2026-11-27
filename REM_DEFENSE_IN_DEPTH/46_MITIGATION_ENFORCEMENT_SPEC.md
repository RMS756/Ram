# Deliverable 9: Mitigation and enforcement (Layer 5)

**Code:** `remdid/enforcement.py`, `remdid/replay.py`. **Tests:** gateway group in `tests/test_remdid_components.py`; scenarios 09, 16, 17.

**Status:** implemented and tested; in the execution path of every ENF arm of DiD-3.

## 1. Gateway (independent enforcement boundary)

- **Permit.** A release decision produces a permit: HMAC-SHA256 over (session, tool, canonical arguments digest, nonce, expiry on the decision counter, budget).
- **Single execution path.** In `remdid/replay.py` the executor calls a tool **only** through `Gateway.execute`. There is no other code path to `runtime.run_function` in ENF arms (test: non-bypassability in the harness).
- **Re-validation immediately before execution**, against the **actual** arguments. This closes time-of-check/time-of-use (scenario 16 swaps the recipient after the decision and is refused). The gateway checks:
  - MAC;
  - session;
  - tool;
  - argument digest;
  - expiry;
  - budget (single use).
- **Fail-closed.** Any exception inside validation is a refusal (scenario 17; arm F-GW).
- **Attenuation.** Permits can be narrowed (budget, expiry) and never widened (`test_gateway_attenuation_never_widens`).
- **Audit.** Hash-chained append-only log of executions and refusals; the chain verification detects tampering (`test_audit_chain_detects_tampering`).

## 2. Verdict enforcement (9.3)

| Verdict | Enforcement | Verified by |
|---|---|---|
| Allow | Only the validated call executes, once | `test_gateway_binding_reuse_expiry_session_and_failure` |
| Escalate | Not executed; with the idealized reviewer, executed iff approved | DiD-3 reviewer arms |
| Block | Not executed | All AUTH scenarios |
| Modify | **No safe modification mechanism exists**, so it is identical to withholding. **No distinct benefit is claimed.** Sensitive financial parameters are never changed silently. | — |

## 3. Fail-safe degradation (9.4)

| Failure | Read-only call | State-changing call | Tested in |
|---|---|---|---|
| Missing authorization (TAE store or evaluator down) | Unaffected | Escalate | F-STORE, F-AUTH, scenario 15 |
| Missing provenance | Unaffected | Escalate | F-PROV |
| Detector timeout or unavailable | Unaffected | Escalate if the call's value is in an un-screened untrusted segment | F-DET |
| Invalid or unavailable learned score | v1.0 is skipped | Escalate | F-LEARN |
| Policy engine failure | — | Escalate | F-AUTH |
| Expired capability | — | Refused | Scenario 08; unit test |
| Tool adapter or gateway failure | **Refused (not executed)** | **Refused** | F-GW, scenario 17 |
| Audit failure | Unaffected | Withheld | F-AUDIT |

## 4. Transaction integrity (9.5)

| Property | Status |
|---|---|
| Duplicate-transfer prevention | Single-use permits and TAE uses (implemented) |
| Idempotency keys toward a real bank | Not applicable offline |
| Pending states, confirmation, reconciliation, recovery | **Not implemented.** AgentDojo executes immediately. |

**Executed transfers are not claimed to be reversible.** REM-DiD prevents; it does not recover.
