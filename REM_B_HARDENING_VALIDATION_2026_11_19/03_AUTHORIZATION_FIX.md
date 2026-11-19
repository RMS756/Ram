# 03 Authorisation fix and binding tests (Phase 2)

**Status.** `[PROPOSED - EXPLORATORY]`. Code: `experiments/rem_b_hardening/remb2.py`, which copies `make_guard` of the frozen `rem_arch.py` and puts each change behind a switch. Two parity checks:
- **Switches off.** REM-B2 reproduces frozen REM-B call by call on the development scenarios, probes v1, diagnostics and generalisation cases (`tests/test_rem_b_hardening.py`).
- **New replay path.** Frozen REM-B, run through this study's replay function (which adds the environment-capture element), reproduces its stored outcomes on all 3,313 primary episodes (`results/dev_smoke.json`: 0 mismatches).

## R1: identifier-free designators

| Item | Content |
|---|---|
| General rule | Object-binding designators come only from request tokens without digits. |
| Security rationale | A designator says *which* existing object the user means. Identifiers and amounts already have their own checks (front, contract). Using them as descriptions can only create spurious designations. |
| Trust assumptions | The user's request is trusted. Standing-order subjects come from the bank's records of the user's own orders, as in frozen REM-B. |
| Expected impact | HO4-type requests (a single standing order, the new account given only as an identifier) are released. Requests whose IBAN contains letters matching another object stop producing false designations. |
| Attack surface | None added: the set of designators can only shrink. Residual risk for digit-free identifiers (`02`). |
| Regression tests | `test_identifier_tokens_are_not_designators`, `test_r1_releases_ho4_and_keeps_two_object_ambiguity`. Held-out: probes PB2, PB5, PB6. |
| Research support | Designation of the object by the principal: capabilities (Dennis & Van Horn, 1966) and the confused-deputy problem (Hardy, 1988). R1 is an implementation correction, not a new principle. |

## Binding requirements tested (Phase 2 list)

A proposed call must match the **exact object and the permitted operation**. Sharing a beneficiary or an amount with a legitimate request is not enough.

| Threat | Mechanism in REM-B2 | Development tests (seen) | Held-out probes v2 (written before the code) |
|---|---|---|---|
| Beneficiary substitution | authority front (beneficiary bound to the request) | diagnostics F1, fixtures sets 1–2 | PB9 (attacker first), PB10 (swapped beneficiaries), PB12 (attacker beneficiary) |
| Amount substitution | contract witness (exact amount) | diagnostics F1/F2 | PB1 (999 on the right object), PB9 (500), PB13 (52), PB17 (15 instead of 9), PB24 (450) |
| Standing-order modification | object binding + per-object ledger | L1–L8, HO1–HO7 | PB1, PB3, PB4, PB8, PB25 (amount raised to 4,800) |
| Repeated authorisation consumption | per-(instruction, object) ledger | L3, HO1 | PB1 (repeat), PB3 (repeat), PB9 (repeat), PB13 (repeat) |
| Attacker-first order | object binding (order independent) | L2, HO1, HO7 | PB1, PB3, PB9, PB24 |
| Legitimate-first order | as above | L1 | PB1, PB3, PB9, PB24 |
| Interleaved operations | as above | L5 | PB8 |
| Multiple authorised operations | plural designation; separate contracts | L6, HO2 | PB3 (two insurances), PB10 (two payments, both orders) |
| Conflicting identifiers | front (account bound to an effect) + object binding | – | PB4 (new vs old account in the same sentence) |
| Ambiguous banking records | singular reference with several matches → withheld | HO3, HO5 | PB6, PB7 (a look-alike order planted by the attacker), PB15 (two senders), PB18 (two outgoing records) |
| Same beneficiary, different operation | effect-typed front | – | PB9 (schedule instead of send), PB26 (address and password changes under a payment request) |

The results are reported in `08` and `09`. Nothing in this table is a result.
