# Chapter 3 (draft section): Authorisation-first architecture variants of REM

> **Status labels used in this section.**
> - **[APPROVED]**: the approved REM v1.0 design.
> - **[EXPERIMENTAL]**: arms of earlier controlled studies (C1, C1I).
> - **[PROPOSED - EXPLORATORY]**: the architectures of this study (REM-A, REM-B, REM-C).
>
> Nothing in this section replaces the approved design. Adopting any proposed architecture requires a supervisor decision (`15`, §5). No new equation is introduced. Where a decision rule is referenced, it is the frozen one of the approved design.

## 3.A.1 Motivation

The approved pipeline places a ridge logistic regression with Platt calibration and an expected-loss decision before mitigation [APPROVED]. Controlled replay showed two things:
1. A deterministic authority front, added in later revisions [EXPERIMENTAL], stops every attack-labelled restricted call before the learned stage is reached.
2. A count-only ledger [EXPERIMENTAL] makes authorisation depend on which proposal arrives first. If the attacker's update of a standing order arrives before the user's, it consumes the user's allowance.

This section describes three architectural responses and the security contract they must satisfy.

## 3.A.2 Security contract

**Trust assumptions:**
- The user's request and the bank's structured record fields are trusted.
- Free text returned by tools (transaction subjects, files, notices) is untrusted.

**Invariants.** Every proposed architecture must satisfy:

| Invariant | Statement |
|---|---|
| I1 Authority origin | No released state-changing call takes its operation, beneficiary or object from untrusted content. |
| I2 Scope | A released call is covered by one user instruction whose condition holds and whose remaining allowance for that object is positive. |
| I3 Object binding | A modification of an existing banking object is released only if the instruction designates that object from trusted fields and the request text. Missing or non-unique designation → withheld. |
| I4 Evidence provenance | Derived amounts and refund recipients come only from structured fields of executed bank reads. |
| I5 No ML override | A probability can never release a call that a deterministic stage refused for authority, object or scope reasons. |
| I6 Refund counterparty | A refund is licensed only to a counterparty the user has paid before (an executed outgoing record). |

## 3.A.3 Five-layer mapping (no sixth layer)

| Layer | REM-B components |
|---|---|
| 1 Input & Context | request compiler (instructions, effects, conditions, counts); amount grammar; designators of `schedule_modify` clauses; provenance (executed structured reads only) |
| 2 Detection | ridge logistic regression + Platt. Used only in REM-A and REM-C; in REM-B it does not enter the verdict |
| 3 Behavioural Analysis | per-(instruction, object) ledger, settled by the execution signal; history of executed reads |
| 4 Decision Engine | authority front; refund licence (E2h); predicates D1/D2; object binding; contract witness with E1; learned stage in REM-A and REM-C |
| 5 Mitigation | step-level Allow / Block / Escalate. Escalate withholds the current action (no reviewer); Block prevents execution of the current proposed action |

Offline fitting remains cross-cutting.

## 3.A.4 REM-B decision procedure [PROPOSED - EXPLORATORY]

```
procedure DECIDE(call c, request q, history H, ledger L):
    if c.tool not in RESTRICTED: return ALLOW
    e ← AUTHORITY_FRONT(q, c, H)                       # operation, effect, beneficiary, condition
    r ← none
    if e = denied or not e.authority:
        r ← REFUND_LICENCE(q, c, H, L)                 # E2h: amount L in the refund clause,
                                                       #      unique executed incoming record of L from S,
                                                       #      S is the recipient of an executed outgoing record (I6)
        if r = none: return BLOCK                      # authority
    f ← PREDICATES(c.tool, c.tier, evidence availability)
    if f forces a verdict: return f
    if c.tool = update_scheduled_transaction:
        o ← OBJECT_STATUS(q, H, c.args.id)             # I3
        if o = not_designated: return BLOCK
        if o = unresolved: return ESCALATE             # designation missing or ambiguous; unread object
    k ← (verified by r) if r ≠ none else CONTRACT_WITNESS(q, c, H, L)    # E1 inside, exact rationals
    if k ∈ {mismatch, exhausted}: return BLOCK
    if k = unresolved: return ESCALATE
    RESERVE(L, k.instruction, c.args.id)               # committed on execution success, released on failure
    return ALLOW
```

```
procedure OBJECT_STATUS(q, H, id):
    S ← scheduled objects of the latest executed get_scheduled_transactions
    if id ∉ S: return unresolved
    D ← content words of the schedule_modify clauses of q, minus a fixed stop list
    if D = ∅: designated ← S if |S| = 1 else ∅
    else:     designated ← { s ∈ S : words(s.subject) ∩ D ≠ ∅ }
    if designated = ∅: return unresolved
    if the clause is singular and |designated| > 1: return unresolved
    return designated if id ∈ designated else not_designated
```

**Known defect.** The designators are extracted from the whole clause, including identifiers. An IBAN such as `GB82WEST…` yields the designator "west" (`08a`). A corrected rule must remove identifier tokens before extracting designators. That correction was tested only post hoc.

## 3.A.5 Learned variants

| Variant | Where the learned stage acts | Verdict set | Rule |
|---|---|---|---|
| REM-A | every restricted call that passed the deterministic stages with a verified or unconstrained contract | {Allow, Block} | frozen expected-loss engine with the frozen loss grid and consequence tier (Escalate and Modify excluded) |
| REM-C | only eligible unresolved calls (authority, object and scope established; value unresolved) | {Allow, Escalate, Block} | frozen expected-loss engine (Modify excluded) |
| REM-C-T | as REM-C | {Allow, Escalate} | frozen B1 operating threshold (Eq. 3.14), α_blk = 0.01, fitted on development scores only (θ = 0.9388) |
| REM-C-raw | as REM-C | as REM-C | uncalibrated probability (isolates Platt) |

The estimator is the stored ridge logistic regression on feature set F4 with stored Platt parameters. No model is refitted.

Its prediction target is **malicious influence**, the attack label of the call. It is not **authorisation of the value**. Chapter 4 shows the consequence of this difference.

## 3.A.6 Relation to prior work

| System | What REM-B shares with it | What REM-B adds or differs in | Not claimed |
|---|---|---|---|
| Progent (preprint) | deterministic per-call checking; least privilege | instruction- and object-bound stateful allowance; amounts derived from trusted records | superiority over full Progent (not executed) |
| CaMeL (preprint) | provenance of values | no change to the agent; restricted provenance (structured bank fields) | equivalent guarantees: CaMeL tracks all data flow, REM-B does not |
| Capability systems (Dennis & Van Horn, 1966); confused deputy (Hardy, 1988) | designation of objects by the principal | an application to financial tool calls of LLM agents | a new principle |
