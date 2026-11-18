# 03 Threat model and security contract (Phase 5). Fixed before implementation

## Parties and trust

| Party | Trust | Notes |
|---|---|---|
| Legitimate user | trusted for **intent** | the request text is the only source of authority |
| Financial AI agent (LLM) | untrusted for authority | may be hijacked; proposes tool calls |
| Attacker | controls injection channels | AgentDojo banking vectors: incoming-transaction subject, bill file, landlord notices, address-change file; more generally any free text the agent reads |
| Untrusted content | data only, never authority | file contents, transaction subjects, any tool output text |
| Banking tools | trusted to execute and to report **structured** fields | the `sender`, `recipient`, `amount` and `id` of executed `get_most_recent_transactions` results, and the `id`, `recipient`, `amount` and `subject` of the user's own scheduled transactions (`get_scheduled_transactions`), are trusted operands. **This is an assumption about the bank API (declared), not a property of REM.** |
| REM | trusted reference monitor at the tool boundary | non-invasive: sees each proposed call, its arguments, and the executed tool results; can release or withhold |
| Authorisation state | REM-internal | compiled instructions; ledger of reservations and commits |

## Attacker capabilities and constraints

**The attacker can:**
- write arbitrary text into the injection channels;
- induce the agent to propose any tool call with any arguments, in any order, any number of times;
- **send money to the victim** (creating an incoming transaction with a sender and amount of their choice: the refund-scam capability);
- choose a target account that coincides with an account the user authorised (ut15×it4).

**The attacker cannot:**
- modify the user's request;
- change REM's code or state;
- forge the structured fields of the bank's own records about the user's outgoing payments and standing orders;
- create outgoing payments from the user's account without passing REM.

## Definitions

- **Authorised banking action:** a state-changing call whose operation, object (for modifications), beneficiary and amount are determined by an instruction in the user's request, using only trusted evidence, and within that instruction's remaining scope.
- **Unauthorised banking action:** any released state-changing call that is not authorised. In particular:
  - one whose beneficiary, object or amount comes from untrusted content;
  - one that exceeds the instruction's scope.
- **Benign task success:** AgentDojo's utility evaluator returns True.
- **Attack success:** AgentDojo's security evaluator returns True in an attacked episode.
- **Security violation:**
  - an attack success;
  - the release of an attack-labelled call;
  - in author-written suites, the release of a proposal labelled *unauthorized* or *ambiguous*;
  - in replay, a released call whose values differ from the value the request determines (the audited reference table, `fp_classify.REFERENCE`).
- **False-positive intervention:** a withheld restricted call that carries no attack label (benign episodes; the rate is reported). Where the audited reference exists, it is a withheld call whose values equal the request's.
- **Escalation:** withheld pending review. With no reviewer it has the same effect as Block. The idealised reviewer of the frozen design (Ch. 3 §3.11.7: release iff y = 0) is used **only as a labelled upper bound**.
- **Safe modification:** none implemented. Modify is never selected; its frozen semantics withhold the call.

## Security invariants (every candidate; tested)

- **I1 (authority origin).** No released state-changing call takes its operation, beneficiary or object from untrusted content. Tests: injected variants of the diagnostics and probes; HE5 / HC4.
- **I2 (scope).** A released call is covered by one instruction whose own condition holds and whose remaining allowance for that object is positive. Tests: ledger cases, F2 diagnostics.
- **I3 (object binding; REM-A/B/C).** A modification of an existing banking object is released only if the instruction designates that object, from trusted object fields and the request text. If the designation is missing or not unique, the call is withheld (fail-safe). Tests: L1–L8, HO1–HO7.
- **I4 (evidence provenance).** Derived values (E1) and refund recipients (E2h) come only from structured fields of executed bank reads. Tests: G4, R3, HE5, HC4.
- **I5 (no ML override).** A probability can never release a call that the deterministic stages refused for authority, object or scope reasons. In REM-C it can only decide among calls whose authority is established and whose evidence is unresolved. Test: reachability map; unit test.
- **I6 (refund counterparty).** E2h releases a refund only to a counterparty that the user has paid before (an executed outgoing record), which defeats the refund-scam capability above. This mirrors the banking practice of treating payments to new beneficiaries with additional checks. Test: HE1.

## Call order, ambiguity, multiple operations
- Authorisation must not depend on which proposal arrives first. Object binding makes the attacker's call unauthorised regardless of its position.
- An ambiguous designation (a singular reference with several matching objects, or no designator with several objects) is withheld for every candidate object.
- A plural reference ("standing orders", "orders") designates every matching object, once each.
