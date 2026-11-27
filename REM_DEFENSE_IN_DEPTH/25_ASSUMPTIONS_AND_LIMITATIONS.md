# Security assumptions and limitations of the proposed REM-DiD

## Assumptions (each must hold for the corresponding property to hold)

| ID | Assumption | Properties that depend on it | Holds in AgentDojo replay? |
|---|---|---|---|
| AS-1 (existing) | REM intercepts every proposed call and every tool result | Complete mediation, non-bypassability | Yes, by construction of the harness. Not shown for a deployment. |
| AS-3 (existing) | REM's code, parameters, logs and TAE store are protected from the adversary | All | Assumed |
| AS-T1 (new) | A trusted, authenticated interface exists for creating TAE entries and approvals | Authorization integrity, least privilege | **No.** The benchmark has none, so only an oracle or a confirmed draft can be evaluated. |
| AS-T2 (new) | Entry integrity keys are held only by the trusted interface and REM | Authorization integrity | Not applicable offline |
| AS-T3 (new) | Users authorize what they intend. An over-broad entry is a user or policy error, not an attack REM can stop. | Least privilege | — |
| AS-L1 (new) | Every security-sensitive value can be traced to its source segments under the declared transformations | Provenance integrity | Partially. Exact copies and reformatting can be traced; free-form agent summarization cannot be proven. |
| AS-D1 (new) | Detection sub-signals are evaluated for correlation before they count as independent | Separation of concerns, resilience | Measurable (SIG-1) |
| AS-6 (existing) | The adversary does not adapt to REM | Every measured result | Replay holds the agent fixed. Adaptive evasion is not covered. |

## Limitations (stated before any evaluation of REM-DiD)

1. **A TAE cannot be tested end to end on AgentDojo.** The oracle TAE is an upper bound built from ground truth. The confirmed-draft TAE assumes a confirmation step that has not been studied with users.
2. **Retry, tool switching and alternative attempts need an adaptive agent.** Under NO-ADAPT these signals never fire on a withheld call's follow-ups. They remain untested until live runs are possible.
3. **The injection classifier is not available.** Detection depth cannot be shown until it is.
4. **One benchmark and one attacker account.** Recipient-based constraints are unusually strong here, and allow-lists succeed trivially.
5. **Authorization reduces the need for learned risk; it does not remove the need for evidence.** If the TAE is broad (for example, "pay any of my payees up to X"), the attacker can stay within it. Layer 4B and the detection evidence are then the only defense. Whether they help in that regime is an open question that must be measured.
6. **Over-blocking.** Strict authorization withholds anything not explicitly authorized. The utility cost depends on how complete the TAE is, and must be reported together with security.
7. **Modify and Escalate are meaningful only with a declared mechanism and a reviewer.** Without them, the four verdicts are two in effect.
8. **None of the proposals is approved.** Each changes a frozen element of the design (features, predicates, inputs) and needs a supervisor decision under CLAUDE.md change control.
