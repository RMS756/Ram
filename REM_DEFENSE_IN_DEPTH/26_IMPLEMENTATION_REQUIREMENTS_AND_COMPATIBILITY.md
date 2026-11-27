# Implementation requirements and compatibility with the existing REM code

## 1. Requirements (for each proposal, if approved)

| ID | Requirement | Fail-closed behavior required | Test |
|---|---|---|---|
| RQ-L1a | Value lineage: every extracted value carries its source-segment set and its transformation chain; lineage survives tool calls | Missing lineage means the value is treated as untrusted | Unit tests for copy, reformatting, arithmetic and splitting; reformatting probe |
| RQ-L1b | Canonical forms per value type [DECLARE] | An unparseable value is untrusted | Property-based tests |
| RQ-L1c | TAE store: verify integrity, expiry and use count; atomic use counter | An unverifiable entry is treated as absent | Forged, expired, replayed and over-scope entries |
| RQ-L2a | Detection sub-signals exposed separately; correlation report generated with every evaluation | Unavailable detector is flagged and treated as missing evidence (D2), never as "not fired" | SIG-1 extended |
| RQ-L2b | Call-linked injection evidence | As above | Fixtures: an injected request for the call's recipient, operation or amount |
| RQ-L3a | Deduplication of x~beh1~ against x~ctx2~ | — | Correlation audit |
| RQ-L3b | Credential-integrity evidence | Missing evidence is flagged | Credential fixtures; DiD-2 rerun |
| RQ-L4a | 4A constraints A1–A9 as predicates, evaluated before 4B; fixed verdicts recorded with reason codes | A constraint that cannot be evaluated withholds the call | Unit tests for each constraint; ordering invariant (4B never loosens 4A) |
| RQ-L4b | Measure 4B's added value over 4A | — | Paired replay, as in the extension study |
| RQ-L5a | Parameter-bound permits | A permit mismatch means the call is not executed | Mutation test |
| RQ-L5b | Reviewer channel for Escalate (approval becomes a one-time TAE entry) | No reviewer means withhold | Needs a reviewer simulation. Live use: R |
| RQ-X | Audit records extended with constraint reason codes, input availability and permit identifiers | — | Re-derivation test |

## 2. Compatibility with the existing code

| Proposal | Where it fits | Change needed | Breaks existing behavior? |
|---|---|---|---|
| Value lineage, canonical forms | `rem/algorithms/context/provenance.py`, entity extraction in `rem/algorithms/behavior/evidence.py` | Extend the extraction to keep lineage; add canonical comparison | **Yes, by design:** it changes x~act1~ under reformatting. Requires a version (REM v1.x) and a supervisor decision. The extension study's canonical matching (`experiments/improve_study/`) is a precedent. |
| TAE capture and verification | New module under `rem/algorithms/context/` (Layer 1); configuration of the integrity scheme | New input interface in `rem/core/interfaces.py` (ContextProcessor) | No, while disabled. Absent TAE preserves v1.0 behavior unless A2 is enabled. |
| Constraints A1–A9 | `rem/algorithms/decision/policy.py` (`PredicatePolicy`: D1 and D2 already have this form) | Add predicates; keep the frozen stage order (predicates before the expected-loss verdict) | No, while disabled. A1 = D1 and A9 = D2 already exist. |
| Detection sub-signals | `rem/algorithms/detection/instruction_patterns.py` (`fired()` already returns sub-signal identifiers) | Expose them as separate evidence; correlation reporting | Changes the feature set (SD-FEAT): decision needed |
| x~ctx1~ classifier | `rem/algorithms/detection/` | New component; D-8 | Feature-set change |
| Deduplication, credential and divergence evidence | `rem/algorithms/behavior/evidence.py` | Feature definitions | Feature-set change: decision needed; refit |
| Parameter-bound permits | `rem/core/mitigation.py`, `rem/deployment/gateway.py` | Permit issued at release; checked by the tool adapter | No change to verdicts |
| Reviewer channel | `rem/core/mitigation.py` (Escalate) | Approval path | Escalate semantics unchanged (withhold pending review) |
| Modify mechanism | `rem/core/mitigation.py` (`DesignNotSpecifiedError` if undeclared) | Exactly one mechanism to declare. Candidates for the supervisor: (i) the current per-call tool restriction; (ii) a confirmation request for the same call (no argument change); (iii) execution in a declared read-only or sandbox mode where the tool supports it. **Changing recipients or amounts is excluded.** | Decision needed |

**Tests that must keep passing:**
- `tests/test_contract_compliance.py`: five layers, no feedback layer, frozen verdicts, no equation IDs in code;
- `tests/test_mitigation*.py`;
- `tests/test_pipeline.py`.

The proposals are designed to keep them valid. Any change that cannot keep them valid needs a supervisor decision first.
