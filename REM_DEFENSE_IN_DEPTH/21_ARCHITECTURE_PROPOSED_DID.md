# B. Proposed strengthened architecture: REM-DiD (five layers, unchanged)

## Status and markers

**Everything in this document is a proposal.** Nothing here is implemented in `rem/`. No new mechanism may enter REM without:
- a supervisor decision (CLAUDE.md change control);
- a feasibility study under a committed protocol (see `27_PRIORITIZED_PLAN.md`).

Declared quantities are named but given no value. Each is marked **[DECLARE]** and must be fixed by the supervisor before implementation.

| Marker | Meaning |
|---|---|
| **[EXISTS]** | Present in REM v1.0 unchanged |
| **[MOD-P]** | Proposed modification of an existing mechanism |
| **[NEW-P]** | Proposed new mechanism inside an existing layer |

The architecture keeps exactly five layers and the frozen stage order. Audit, monitoring and offline recalibration stay cross-cutting.

## Design principles, derived from the measured weaknesses

| Principle | Evidence that motivates it |
|---|---|
| P1. **Separate authorization from risk.** "Is it allowed?" is answered deterministically. "Is it likely induced?" is answered by evidence. | The learned decision cannot tell an authorized payment from an unrequested one that uses the user's words (paired fixtures). Deterministic authority guards stop every attack-labeled call in replay (extension study, Progent's policy). |
| P2. **Non-compensatory hard constraints.** No probability can release a call that violates authorization. | The low-probability release of credential changes by the two-verdict rule (V11d) |
| P3. **Evidence must be complementary and call-specific.** Duplicated or episode-level signals do not count as depth. | x~ctx2~ ≡ x~beh1~ (correlation 1.00); detection marks the episode, not the call (SIG-1) |
| P4. **Depth is measured by evasion, not by counting layers.** | DiD-1 and DiD-2 |
| P5. **Fail-safe defaults.** Missing evidence, missing authorization or a failed component withholds the call; it never releases it. | Existing D2 and the gateway's fail-closed test; extended to the new inputs |

## Layer responsibilities

### Layer 1: Input & Context (provenance integrity and trusted authorization context)

| Mechanism | Marker | Responsibility |
|---|---|---|
| Segment provenance labels | [EXISTS] | Label each segment trusted, semi-trusted or untrusted. Derived content takes the least-trusted label. |
| Value lineage | [MOD-P] | For every security-sensitive value, record the set of source segments and the transformations applied: copy, reformatting, arithmetic, summarization by the agent. Values tracked: recipient and account identifiers, amounts, transaction references, tool arguments, external instructions and sensitive data. Lineage is preserved across tool calls. A value produced by the agent's own text inherits the labels of the segments it could have been derived from, never a higher one. |
| Canonical value forms | [MOD-P] | Compare identifiers and amounts in a declared canonical form [DECLARE: canonicalization rules per type], so that reformatting does not break lineage. Specified as future work item 7. Addresses the probe in which P1 rose from 12 to 191. |
| Trusted Authorization Envelope (TAE) | [NEW-P] | Capture, verify and hold the user's authorized operations from a trusted, authenticated interaction. Specification: `23_TRUSTED_AUTHORIZATION_ENVELOPE.md`. Layer 1 only verifies and represents the envelope; enforcement belongs to Layer 4. |

### Layer 2: Detection (complementary, call-linked signals)

| Mechanism | Marker | Responsibility |
|---|---|---|
| Instruction-pattern signal | [EXISTS], [MOD-P] | Keep, but report the sub-signals separately (imperative, override, role or delimiter markers, tool references) so that their correlation is visible. SIG-1 showed they collapse to one template fingerprint. |
| Instruction-aware injection classifier x~ctx1~ | [NEW-P] (designed, not implemented; D-8) | An independent, learned content signal [DECLARE: model and operating point]. It must be evaluated against the five benchmark templates, paraphrases and identifier transformations. |
| Call-linked injection evidence | [NEW-P] | Whether the arguments, operation or scope of *this* call appear inside detected injected content. This turns an episode-level detection into call-level evidence (SIG-1, part C). |
| Scope-change and override indicators | [NEW-P] | Injected content that requests an operation outside the TAE's scope, or that requests tool access the user did not grant. Defined against the TAE, so it is unavailable when no TAE exists. |
| Correlation control | [NEW-P] (process) | No detector enters the Decision Engine as a separate signal unless its correlation with existing signals is measured and reported. Two signals with correlation ≈ 1 count as one. |

Detection supplies evidence to Layer 4. It never authorizes and never releases a call.

### Layer 3: Behavioral Analysis (action and sequence integrity)

| Mechanism | Marker | Responsibility |
|---|---|---|
| Action evidence x~act1–3~ | [EXISTS], [MOD-P] | Keep. x~act1~ uses canonical value lineage from Layer 1. |
| Remove duplicated evidence | [MOD-P] | x~beh1~ is defined through x~ctx2~ (correlation 1.00). Either redefine it on the call-linked detection evidence, or drop it [DECISION]. |
| Credential-integrity evidence | [NEW-P] | Whether a credential value originates in untrusted content. Credential attacks currently depend on the behavioral family alone (DiD-2). |
| Divergence from the authorized task | [NEW-P] | The operation, recipient or amount differs from the TAE (or from the request, when no TAE exists). This is evidence, not enforcement. Enforcement is Layer 4A. |
| Retry, tool switching and alternative attempts after a refusal | [NEW-P] | The same objective sought again through another tool or reformatted arguments after a withheld call: the same recipient or amount via `schedule_transaction` after `send_money` was blocked. **Testable only with an agent that adapts.** Replay cannot exercise it. |
| Multi-step and state-changing sequence anomalies | [EXISTS] (x~beh4~), [MOD-P] | x~beh4~ fires more often on legitimate calls than on attacks (0.23 against 0.17). It needs a sequence model of legitimate complex workflows [DECLARE] before it can be retained. |
| Legitimate complex workflows | process | Every new behavioral signal is reported with its firing rate on legitimate state-changing calls. The current x~beh3~ fires on 71% of them. |

### Layer 4: Decision Engine (two coordinated decision functions)

**4A. Deterministic authorization enforcement** [NEW-P]. This extends the existing policy-predicate stage (D1, D2), so the frozen stage order is unchanged. Each constraint below is **non-compensatory**: when it fires, the verdict is fixed and the expected-loss rule is not consulted (as D1 and D2 already do).

| Constraint | Applies when | Verdict |
|---|---|---|
| A1 Prohibited operation | [EXISTS] as D1 | Block |
| A2 No authorization for a state-changing operation at tier ≥ [DECLARE] | No TAE entry covers the operation | Escalate (or Block with no reviewer) |
| A3 Unauthorized recipient | The recipient is not the one bound in the TAE entry | Block |
| A4 Amount outside the authorized range | The amount is not within the entry's bound | Block |
| A5 Expired authorization | The current time is after the entry's expiry | Block |
| A6 Reused one-time authorization | The entry is already consumed | Block |
| A7 Missing mandatory approval | The entry requires approval and none is attached | Escalate |
| A8 Outside the authorized scope | Wrong operation type, source account or currency | Block |
| A9 Missing required evidence | [EXISTS] as D2 | Escalate |

**4B. Consequence-aware risk decision** [EXISTS], applied only to calls that pass 4A:
- ridge estimate on the (revised) evidence;
- calibration;
- tier;
- expected loss.

**Requirement:** 4B's value beyond 4A must be measured and must not be assumed. The extension study found that it added no measured value behind a deterministic guard. If it again adds none, it should be reported as such, and possibly confined to the tiers or cases where 4A is unavailable.

**Ordering invariant:**
- 4A runs before 4B.
- 4B can tighten a verdict, for example turning a call that 4A allows into Escalate or Block.
- 4B can never loosen a 4A verdict.

### Layer 5: Mitigation (enforced and verifiable)

| Mechanism | Marker | Responsibility |
|---|---|---|
| Pre-execution mediation | [EXISTS] | Every call passes `evaluate()` before reaching the tool. The gateway test checks that a withheld call never reaches the backend. |
| Parameter-bound permits | [NEW-P] | A released call carries a permit bound to its exact tool and canonical arguments, and the tool adapter executes only an exactly matching permit. This prevents argument changes between the decision and execution. |
| Allow / Block | [EXISTS] | As now (step-level) |
| Escalate | [EXISTS] semantics; [NEW-P] reviewer channel | Withhold pending review. Release only on an authenticated approval, which is itself recorded as a TAE entry (one-time). Without a reviewer, Escalate equals Block, which is the current situation. |
| Modify | [EXISTS] semantics; **mechanism [DECISION]** | Exactly one declared mechanism (CLAUDE.md MITIGATION LOCK). **Never** change a recipient or an amount silently; a sensitive parameter change requires a new authorization (A3/A4 path). Candidate mechanisms are listed for the supervisor in `26_IMPLEMENTATION_REQUIREMENTS_AND_COMPATIBILITY.md`. |
| Fail-safe handling | [EXISTS] (gateway fail-closed), [MOD-P] | An unavailable detector, missing lineage, an unverifiable TAE or a policy error each lead to withholding plus an audit record, never to release. |

## Security decision flow (one proposed call)

1. **Layer 1.** Capture the call. Attach value lineage to each argument. Look up and verify TAE entries (signature, expiry, use count). Mark each item unavailable if it cannot be verified.
2. **Layer 2.** Compute detection sub-signals and call-linked injection evidence. Unavailable components are flagged.
3. **Layer 3.** Compute action, credential, divergence and sequence evidence, with deduplication applied.
4. **Layer 4A.** Evaluate constraints A1–A9 in a declared order. **If any fires, the verdict is fixed** and its reason code is recorded; go to step 6.
5. **Layer 4B.** Estimate the probability, calibrate, assign the tier and take the expected-loss verdict. 4B may only tighten.
6. **Layer 5.** Enforce. A released call gets a parameter-bound permit; a withheld call never reaches the tool.
7. **Cross-cutting.** Write the audit record: the inputs and their availability, every constraint evaluated, the probability, the verdict and its source, the permit identifier, and the attribution (after the verdict).

## Diagram

See `figures/fig_rem_did_proposed.png`. It has five layers and a cross-cutting band, and marks proposed mechanisms distinctly.
