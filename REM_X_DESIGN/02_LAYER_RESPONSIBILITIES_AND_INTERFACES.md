# Deliverable 2: Five-layer responsibilities and interfaces (REM-X, proposed)

**Notation.** Interfaces are typed records passed between layers. Status markers are as in file 01. Every interface carries `available: bool`. An unavailable input is never read as "safe" (fail-safe rule, file 04).

## 1. Responsibilities

| Layer | Single question it answers | Owns | Must not do |
|---|---|---|---|
| 1 Input & Context | Where did each value come from, and what did the user authorize or delegate? | Segmentation and source labels [DiD-I]; canonical forms [DiD-I]; inferred lineage [DiD-I]; **Financial Authorization Record (FAR, the TAE plus delegation)** [X-P]; deterministic schema extraction for named sources [X-P] | Decide; upgrade trust because a model repeated a value |
| 2 Detection | Is there instruction-like adversarial content, and does it touch this call's values or a delegated source? | Sub-signals [DiD-I]; call-linked evidence [DiD-I]; **delegated-source screening** [X-P] | Authorize; treat "not fired" as "safe" when unavailable |
| 3 Behavioral Analysis | Is the sequence of actions consistent with the authorized task? | Rules: new payee, redirect, repeat, retry, switch [DiD-I/T]; ledger-derived sequence features (cumulative per recipient and session, read-then-pay chains) [X-P]; optional learned anomaly score, advisory only [X-P] | Read content text (that is L2); authorize |
| 4 Decision Engine | Authorized? Evidence of induction? Within the economic envelope? Which intervention? | 4A authorization against the FAR including delegation conditions [DiD-I + X-P]; **atomic reservation** [X-P]; precedence, most restrictive wins [DiD-I]; 4B learned risk, **advisory, tighten-only, unpinned or delegated fields only** [V1 model, X-P placement] | Let a probability or any explanation loosen a denial; emit Modify (no mechanism declared) |
| 5 Mitigation | Is exactly the decided call executed, once, and is its effect the approved one? | Exact-action single-use permits [DiD-I]; **independent adapter-side re-verification of economic terms** [X-P]; **post-execution reconciliation** [X-P]; fail-closed [DiD-I] | Change financial parameters silently; reverse transfers |
| Cross-cutting (not layers) | — | Hash-chained audit [DiD-I]; **transaction ledger** (reservations, permits, observed effects) [X-P]; monitoring (CUSUM observe-only) [V1]; offline fitting [V1] | Enter the verdict path (except the ledger, read through 4A and L5) |

## 2. Interfaces (record types)

| From → To | Record | Fields (minimum) |
|---|---|---|
| Trusted UI → L1 | `FAR` | operation; per sensitive field: PINNED(value) / UNSPECIFIED / DELEGATED(source_id, extractor_id) / ANY; economic envelope (exact, or max per call, per recipient, per session; currency); first-payee cap (declared, or none); uses; expiry; session; nonce; MAC |
| Tool output → L1 | `Segment` | text; source category; tool; field; step; canonical IBANs and amounts; source_id (for named documents) |
| L1 → L2, L3, L4 | `CallLineage` | per sensitive field: canonical value; sources; status (trusted / untrusted / mixed / missing); delegated-extraction result (match / mismatch / not extractable) |
| L2 → L4 | `DetectionEvidence` | per segment and signal: available, fired; call-linked: true / false / unknown; delegated-source screen: clean / flagged / unknown |
| L3 → L4 | `BehaviorEvidence` | fired rules; cumulative totals per recipient and session (from the ledger); available |
| L4B → L4 | `AdvisoryRisk` | p, tier, v1 verdict, available. Consulted only per the ML placement (file 06) |
| L4 → Ledger | `Reservation` | entry id; amount; recipient; state RESERVED |
| L4 → L5 | `Decision` | verdict; rule list with verdicts; decisive rules; reservation id |
| L5 → Adapter | `Permit` | session; tool; canonical-argument digest; reservation id; expiry; budget = 1; MAC (decision key) |
| Adapter → Ledger | `ExecutionCheck` | permit valid; independent FAR re-check (adapter key); executed or refused |
| Adapter → L5 → Ledger | `ObservedEffect` | state delta read from the system of record after execution; reconciliation result (conforms / deviates) |

## 3. Separation rules

1. L2 and L3 never consume each other's outputs. In REM v1.0, x~beh1~ duplicated x~ctx2~ (correlation 1.00), and REM-X forbids such duplication by construction.
2. The authorization record is written only by the trusted UI. L1 reads it; nothing else writes it.
3. The adapter's re-check uses the FAR and the ledger directly, not the decision record. This gives two independent paths to the same economic terms.
