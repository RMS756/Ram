# Deliverable 4: Security invariants and threat-coverage matrix (REM-X, proposed)

## 1. Invariants

Each invariant must hold on **every** test case. The verification column names the test that would falsify it.
- "DiD" in the status column means a mechanism already exists in REM-DiD with that test.
- "X" means the test must be written.

| ID | Layer(s) | Invariant | Enforcement point | Failure mode | Verification test | Status |
|---|---|---|---|---|---|---|
| I-1.1 | L1 | No sensitive financial argument is executed unless its value is (a) pinned by a verified FAR, or (b) admitted by a DELEGATED rule, or (c) escalated and approved. Untrusted-only or missing lineage alone never releases it | 4A plus the PROV rule | Lineage inferred wrongly (collision; paraphrase laundering) | Lineage unit tests; collision fixture (user_task_15-type); paraphrase-laundering fixture | DiD (a, c); X (b) |
| I-1.2 | L1 | No value's trust status is upgraded because a model repeated, summarized or explained it | Lineage computation | Agent summary matched to a trusted segment by coincidence | Unit test: value present only in the agent's own text → MISSING | DiD |
| I-1.3 | L1 | The FAR is written only by the trusted issuer; model text and tool output can never create or widen an entry | FAR store (origin rule, MAC) | Key compromise (assumption AS-3) | Origin-rule test; tamper test | DiD |
| I-1.4 | L1 | A DELEGATED value is admitted only if extracted deterministically from the named source's data fields **and** that source segment has no detector firing **and** caps hold | 4A delegation check | Parser fooled by structure-mimicking injection | Adaptive fixtures: injected fake bill line; duplicate payee lines; payee in free text only | X |
| I-2.1 | L2 | Detection never authorizes; it can only escalate | Precedence | — | Property test: removing all L2 rules never releases a call that 4A denied | DiD |
| I-2.2 | L2 | An unavailable or timed-out detector is "unknown", never "not fired"; unknown on a relevant segment escalates a state-changing call | Detection suite; precedence | Silent detector crash treated as clean | Fault injection (F-DET) | DiD |
| I-3.1 | L3 | Behavioral rules use only actions, arguments and ledger state, never content text (no duplication of L2) | Code separation | Hidden coupling (as x~beh1~ ≡ x~ctx2~ in v1.0) | Static dependency check; signal-correlation audit (phi < 1 with every L2 signal) | X |
| I-3.2 | L3 | Retry, tool switching or splitting toward a recipient of a withheld call is always flagged | Behavior monitor | Recipient written differently | Canonicalized-recipient fixtures | DiD (DiD-T) |
| I-4.1 | L4 | No model-generated explanation, probability or justification can grant financial authority or loosen a denial | Precedence (maximum severity) | — | Property test over all rule combinations | DiD |
| I-4.2 | L4 | No transaction exceeds its approved economic parameters (exact amount, per-call, per-recipient, per-session limits, currency) | 4A plus the adapter re-check (I-5.2) | Limits not declared for the operation | Amount, currency, split and cumulative fixtures | DiD (exact, budget); X (per-recipient, per-session) |
| I-4.3 | L4 | Cumulative limits are enforced atomically: sum(committed) + sum(reserved) ≤ limit at every point, including interleaved or parallel calls | Ledger reservation (reserve → commit or release) | Race between two calls | Concurrency test with interleaved and parallel calls; crash between reserve and commit (the reservation must expire or release) | X |
| I-4.4 | L4 | No layer overrides an independent denial from the authorization path or the enforcement path | Precedence; adapter independence | — | Property test; mutation test (decision record altered after denial) | DiD (precedence); X (adapter) |
| I-5.1 | L5 | No authorization token or permit can be reused or transferred to another session or call | Gateway (MAC, session, digest, budget = 1) | — | Reuse, cross-session, TOCTOU and expiry tests | DiD |
| I-5.2 | L5 | The tool adapter independently re-checks the FAR's economic terms with its own key before execution | Adapter | Adapter shares a key or trust domain with the decision engine | Test: forged decision with a valid permit but out-of-envelope terms → refused | X |
| I-5.3 | L5 | Every executed state change is reconciled against the approved action. A deviation halts further state-changing calls in the session and is recorded | Post-execution reconciliation | System of record unavailable → reconciliation "unknown" → halt (fail-safe) | Fault injection: adapter executes a different amount or recipient | X |
| I-5.4 | L5 | Mandatory checks fail closed for state-changing calls; read-only calls degrade per declared policy | Gateway; precedence | Fail-open configuration | Failure-injection arms (all components, singly and in pairs) | DiD (singly); X (pairs) |
| I-C.1 | Cross-cutting | Every decision has an audit record and every execution a ledger entry; chains are verifiable | Audit and ledger | Audit store down → state-changing calls withheld | Chain verification; F-AUDIT | DiD (audit); X (ledger) |
| I-C.2 | Cross-cutting | Failure independence: every attack class in §2 is covered by ≥ 2 controls with different inputs | Design review plus evaluation | Controls share inputs (DiD-3: PROV and DET Jaccard 0.99) | Coverage and evasion matrix (file 08) | X (requirement) |

## 2. Threat-coverage matrix

**Cell values:** P = primary; S = secondary; — = none.

**Inputs** name the evidence each control reads, to check I-C.2:
- AUTH: FAR;
- DELEG: named source + extraction;
- PROV: lineage;
- DET: text;
- BEH: actions and ledger;
- LEDGER: cumulative state;
- ENF: permit and adapter;
- RECON: system of record.

| Threat | AUTH | DELEG | PROV | DET | BEH | LEDGER | ENF | RECON | ≥2 independent inputs? |
|---|---|---|---|---|---|---|---|---|---|
| Beneficiary substitution | P | P | S | S | S | — | — | S | Yes |
| Identifier reformatting | P | P | S | — | S | — | — | — | Yes |
| Amount escalation (trusted recipient) | P | S (cap) | — | — | — | S | S (adapter re-check) | S | **Yes in REM-X** (no in REM-DiD: AUTH only) |
| Currency substitution | P | — | — | — | — | — | S | S | Yes, if the tool exposes currency |
| Source-account change | P | — | — | — | — | — | S | S | Same |
| Repeated attempts | P (uses) | — | — | — | P | S | P (single use) | — | Yes |
| Split transfer | P (budget) | S (cap) | — | — | S | P | S | — | Yes |
| Expired or reused authorization | P | — | — | — | — | — | P | — | Yes |
| Cross-session reuse | P | — | — | — | — | — | P | — | Yes |
| Tool switching after denial | P | — | S | S | P | — | — | — | Yes |
| Multi-step redirect (standing order) | P | — | S | S | P | — | — | S | Yes |
| Legitimate document with malicious instruction | P (if pinned) | **P** | S | S | S | S | — | — | Yes |
| Conflicting trusted / untrusted data | P | S | P | S | S | — | — | — | Yes |
| Attacker value in the user's own request (collision) | — (authorized) | — | — | — | P | S (caps) | — | — | **No.** BEH plus caps only; a residual risk |
| Data exfiltration through the payment subject | S (if subject pinned) | — | S | S | — | — | — | — | **Weak.** Needs a subject/readers rule (CaMeL-style); proposed as an optional extension |
| Missing provenance | — | — | P | — | S | — | — | — | Partly |
| Policy-engine failure | fail-safe | — | S | S | S | — | P (adapter re-check) | — | Yes in REM-X |
| Adapter or tool deviation | — | — | — | — | — | — | P | P | Yes |
| Adaptive structure-mimicking document injection | S | **at risk** | S | S (if detectors see it) | S | S (caps) | — | — | To be measured (adaptive suite, file 07) |
