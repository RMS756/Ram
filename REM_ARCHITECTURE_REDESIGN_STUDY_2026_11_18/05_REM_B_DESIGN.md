# 05 REM-B: authorization-first architecture (deterministic)

Status: `[PROPOSED - EXPLORATORY]`. Written before implementation.

REM-B is the deterministic base. REM-A (`04`) and REM-C (`06`) add a learned stage to it in different positions.

## Pipeline (five layers; no sixth layer)

```mermaid
flowchart LR
  U[User request] --> IC[1 Input & context: request compiler; contracts; designators]
  T[Executed tool results] --> PV[1 Provenance: structured bank fields of executed reads only]
  A[Agent proposes a call] --> F
  IC --> F[4 Authority front: operation, effect, beneficiary, condition]
  PV --> F
  F -- denied / no authority --> E2h{E2h refund licence?}
  E2h -- no --> BLK[5 Block]
  E2h -- yes --> P
  F -- authorised --> P[4 Predicates D1/D2]
  P -- forced --> ESC[5 Escalate / Block]
  P --> OB[3+4 Object binding I3]
  OB -- not designated --> BLK
  OB -- designation missing or ambiguous --> ESC
  OB --> W[4 Contract witness: amount (E1), condition, allowance per object]
  W -- mismatch / exhausted --> BLK
  W -- unresolved --> ESC
  W -- verified / unconstrained --> REL[5 Allow; reserve (instruction, object)]
  REL --> L[3 Ledger: commit on execution success, release on failure]
```

## Mechanisms

1. **Authority front.** Frozen revision 3, options `effect`, `cond`; `bind=False`, `fulfil=False`.
2. **Object binding (OB), new.** Applies to `update_scheduled_transaction`.
   - **Objects.** The scheduled transactions in executed `get_scheduled_transactions` results (latest read). If the call's `id` was never read, the call is unresolved and withheld.
   - **Designators.** The content words (alphabetic, ≥ 3 letters, outside a fixed generic stop-list of banking and function words) of every clause of the request that the compiler maps to the `schedule_modify` effect.
   - **Designated objects.** An object is designated if a word of its own `subject` is a designator.
   - **No designator.** If no designator exists and exactly one object was read, that object is designated.
   - **Number.** A clause with a plural object noun (`orders`, `payments`, `transfers`, `subscriptions`) makes the reference plural. Otherwise it is singular, and a singular reference with more than one designated object is ambiguous: unresolved, withheld.
   - **Verdicts.** If the call's `id` is not designated, the call is blocked (`object_not_designated`).
   - **Allowance.** It is consumed per (instruction, object): each designated object can be modified up to the instruction's count.
3. **E1.** Unchanged from `REM_IMPROVEMENT_CONTROLLED_STUDY_2026_11_18/04` (explicit "P% of the amount (we|I) paid [+ fee]", single executed outgoing record).
4. **E2h (hardened refund licence), new.**
   - **Which sentences.** A refund sentence of the request with a received-money phrase and exactly one stated amount L.
   - **Clause scope.** Accounts are checked **in the refund clause only**, which ends at a following "and/also + payment verb".
   - **What it licenses.** One `send_money` of exactly L to the single sender S of an executed incoming record with amount L.
   - **Counterparty requirement (I6).** S must also be the recipient of an executed **outgoing** record, i.e. a counterparty the user has paid before.
5. **Ledger.** Reserve on release; commit on a successful execution signal; release on refusal or error.
6. **Mitigation.** Step-level; Escalate withholds (no reviewer). The idealised reviewer is reported only as an upper bound.

## Evaluation of the threat classes (to be measured)

| Threat class | Mechanism expected to stop it | Where tested |
|---|---|---|
| Unauthorised payment, beneficiary substitution | front | replay attacks, diagnostics, fixtures |
| Amount modification | contract witness | diagnostics F1, F2, fixtures |
| Standing-order manipulation | object binding | L-cases, HO-cases, scripted ut15×it4 in 4 orders |
| Tool-output / file injection | provenance (front + I4) | replay, injected variants, HE5 / HC4 |
| Repeated unauthorised operations | ledger | L3, HO1, HE2 |
| Authorisation consumption | object-bound ledger | L2, L3, L5, HO1, HO7 |
| Legitimate multi-step workflows | plural designation; separate contracts | L6, HO2, HE4, replay utility |
| Refund scam | E2h counterparty requirement | HE1 |
