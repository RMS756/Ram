# Multiple REM research candidates (v2)

[PROPOSED — SUPERVISOR APPROVAL REQUIRED]

Four distinct candidates, not four names for the same empty-contract behavior:

- **C1_action_model:** original ridge/logit calibration/Bayes decision using only action features.
- **C2_canonical_provenance:** typed/schema-checked provenance gate with fragmented-IBAN matching.
- **C3_target_only:** diagnostic control that omits amount provenance; known unsafe for amount-only manipulation.
- **C4_verified_refund:** bounded trusted-request recognition and independent bank-ledger verification, exact repair and one-use reservation, falling back to C2 elsewhere.

The study reuses previously examined development recordings. It does not supply an untouched final test or establish a novel published algorithm. C4's additional trusted backend interface is a changed assumption, not free information.

Results and limitations: `../../REM_CANDIDATE_COMPARISON_V2/RESULTS.md`.
Commands: `../../REM_CANDIDATE_COMPARISON_V2/REPRODUCE.md`.
The original REM and the preceding AA study remain unchanged.
