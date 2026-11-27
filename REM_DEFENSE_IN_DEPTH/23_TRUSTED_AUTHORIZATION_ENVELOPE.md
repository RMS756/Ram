# Trusted Authorization Envelope (TAE): specification (proposed, not implemented)

**Placement:**
- **Layer 1 (Input & Context):** captures, verifies and represents envelopes.
- **Layer 4A:** enforces them.
- **Not a sixth layer.**

**Status:** [NEW-P]. Requires a supervisor decision and a feasibility study (`27_PRIORITIZED_PLAN.md`, F1).

**Fields:** all marked [DECLARE] are named but have no value.

## 1. Purpose

REM v1.0's only trusted input is the request text. Every attempt to infer authorization from text has had defects found by review (three revisions of the request compiler, two amount-verifier defects), and the request text can itself repeat attacker values (the paired fixtures).

The TAE moves "what did the user authorize?" out of text interpretation and into a structured record. Its origin is an authenticated user interaction or an explicit approval.

## 2. Origin rule (non-negotiable)

An entry is valid only if it was produced by a trusted interface. Examples are an application form, a banking confirmation screen, or a reviewer's approval of an escalation. It must be bound to an authenticated principal.

**Never valid sources:**
- tool outputs or retrieved content;
- the agent's own messages;
- an LLM-generated summary of the request.

Text parsing of the user's request (the extension study's compiler) **may propose** a draft envelope that the user confirms through the trusted interface. The draft itself is never trusted.

## 3. Schema (one entry per authorized operation)

| Field | Type | Meaning |
|---|---|---|
| `entry_id` | unique identifier | — |
| `principal` | authenticated user identifier | — |
| `operation` | enumerated: value_transfer, schedule_create, schedule_modify, credential_change, profile_change | Mapped onto the tool categories of Table 3.4 |
| `source_account` | canonical account identifier, or *any of the principal's* | — |
| `recipient` | canonical identifier, or a declared list | Absent for operations without a recipient |
| `amount` | exact decimal, or a range [min, max] | Absent when not applicable |
| `currency` | ISO 4217 code | — |
| `constraints` | declared predicates, for example "only if balance ≥ X" or a schedule date | Evaluated by Layer 4A on trusted state only |
| `valid_from`, `expires_at` | timestamps | — |
| `use_limit` | integer ≥ 1 (one-time = 1) | — |
| `uses` | counter maintained by REM | — |
| `approval_required` | boolean | If true, a second authenticated approval must be attached before use |
| `approval` | record of the approver, time and method | — |
| `auth_method`, `issued_at` | metadata of the authenticating interaction | — |
| `integrity` | a signature or MAC by the trusted interface over all fields | [DECLARE: scheme and key management] |

## 4. Matching (Layer 4A)

A proposed call **c** matches entry **e** if all of the following hold:
- the operation of **c** equals `e.operation`;
- the canonical recipient of **c** is `e.recipient` (or in its list);
- the amount of **c** is within `e.amount`, compared as exact decimals;
- the currency and source account match;
- the time is within `[valid_from, expires_at]`;
- `uses < use_limit`;
- each constraint holds on trusted state;
- the approval is present if required.

**On release, `uses` is incremented atomically.** Partial matches do not count. Neither does matching on any other entry. This is the "binding" lesson of the extension study's revision 2.

## 5. Threats to the envelope, and their controls

| Threat | Control |
|---|---|
| Forged or altered entry | Integrity check in Layer 1; failure means no entry |
| Replay of a consumed entry | `use_limit` and `uses`, kept by REM, not by the agent |
| Injected text claiming authorization | The origin rule: text is never an entry |
| Over-broad entries (any recipient, any amount) | Breadth is reported in the audit; a range is enforced as given. Policy on breadth: [DECLARE] |
| Benchmark-specific allow-lists presented as authorization | Entries are per principal and per operation, not a static list. This is the difference from Progent's policy. |
| Unavailability of the trusted interface | A state-changing call at tier ≥ [DECLARE] is withheld (A2), as a fail-safe |

## 6. Relation to existing work (not claimed as new)

The TAE combines:
- trusted authorization records (aiAuthZ, abstract level);
- per-call argument policies (Progent);
- origin-bound admission (CapLite, ROPE, PACT, abstract level).

It is not a contribution in itself. **What is new is REM's evaluation of whether the learned decision adds anything once such a record exists.**

**Prior-art update (27 November 2026; see `35_GAP_OVERLAP_NOVELTY.md`).** The search for the prior-art task found that most of the TAE's individual mechanisms are already published. All of the following are at abstract level, except where stated:

- **AGATE** (Zhang et al., 2026; preprint): grants bound to exact parameters that expire and allow a limited number of uses; an effect ledger for repeated requests; authorization grounded in operator declarations and host approval events.
- **AIS** (Gong, Samawi & Medda, 2026; *Systems* 14(10), 1329, peer reviewed): a typed financial action intent checked against mandate, policy, state, approvals and exact economic terms before single-use authority is issued.
- **GuardRail** (Karnawat et al., 2026; Zenodo report): semantic risk signals "can never override a deterministic refusal" (REM-DiD's ordering invariant), and an approval bound to the hash of the exact action (REM-DiD's parameter-bound permit). It reports no quantitative results.
- **AgentCap** (Suresh & Gao, 2026; preprint): short-lived, budget-bounded capability tokens validated at the tool boundary.
- **ScopeGate** (Mellafe Zuvic, 2026; preprint): money ceiling and idempotency checks before a payment call.

The TAE, A1–A9, the ordering invariant and parameter-bound permits are therefore **adopted designs**, and the thesis must cite them as such. The evaluation question in the paragraph above is unchanged. It must also be checked against the full texts of AIS and AGATE, which could not be read here.

## 7. Evaluation feasibility in AgentDojo

AgentDojo has no trusted authorization channel. Two evaluations are possible offline, and both are proposed (`27_PRIORITIZED_PLAN.md`, F1):

- **Oracle TAE.** Entries derived from each user task's ground-truth solution: operation, recipient and amount. This gives an upper bound on what authorization enforcement can achieve. It is not a deployable configuration, and it must be reported as an oracle.
- **Confirmed-draft TAE.** Drafts compiled from the request by the existing request compiler, treated as if the user confirmed them. This measures the residual error of drafting. A real confirmation step needs a user study.

**Known limitation.** In banking v1, user_task_15's legitimate payee is the attacker's account. An oracle entry would authorize that recipient. Whether 4A then stops the attack depends on whether the attack's operation and amount differ from the entry. This must be reported, not hidden.
