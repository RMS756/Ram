# Implementation and tests

[PROPOSED — SUPERVISOR APPROVAL REQUIRED]

All code lives under `experiments/authorization_generalization/`.

| File | Responsibility | Classification |
|---|---|---|
| authorization.py | Grant schema, immutable snapshots, exact Decimal amounts, limited IBAN canonicalization | Engineering logic |
| provenance.py | Raw-source digest and delegated JSON-field lookup | Engineering policy inspired by published capability/provenance work |
| candidate_policy.py | Three-state evidence, four verdicts, safe repair, single-use reservation | Proposed engineering candidate A |
| baseline_adapters.py | Call existing B0/B1/A3 policies and original runtime tracker; add x_act1-only rule | Reuse and explicitly simple baseline |
| replay_adapter.py | Reuse recorded actor/native scorer; execute actual replacement arguments | Engineering adapter; NO-ADAPT |
| dataset_audit.py | Label-shortcut and grouping checks | Evaluation logic |
| evaluate.py | Version filter, original OOF refits, native replay, paired metrics, ablations and cost sensitivity | Experimental protocol |
| tests/test_candidate.py | Synthetic and actual-data integration tests | Correctness tests, not effectiveness data |

Before experimental changes: 221 passed, 3 skipped. Final combined suite: **275 passed, no skips** (224 baseline and 51 additional tests). The test log records one dependency deprecation warning. The three baseline replay tests initially skipped due to their default dataset path were enabled using AGENTDOJO_RUNS and passed.

Tests cover malicious recipient changes, direct user authorization of a recipient also in an external artifact, unseen beneficiaries, whitespace/hyphen/zero-width IBAN fragments, alternate tools, incomplete/untrusted grants, failed/missing/conflicting external evidence, changed subjects/dates, NaN/infinity/negative amounts, one-use retries, and ablations. Native AgentDojo integration proves that Modify executes the authorized replacement and that Escalate executes nothing. Synthetic grant fixtures are explicitly excluded from reported benchmark results.

The policy API accepts only tool/arguments and trusted policy state. It does not accept attack labels, task IDs or reference solutions. Baseline oracle labels are used only for the inherited offline fitting residual calculation and audit bookkeeping; the primary reviewer setting is no-reviewer. No label is supplied to candidate runtime decisions.

No `rem/`, original tests, configuration, result, thesis or guard file is changed. A protocol snapshot was committed before candidate outcomes. A later optional contract-injection argument was added to the replay adapter solely to test native Modify; default legacy replay semantics remain the empty-contract path and were checked by the final tests.
