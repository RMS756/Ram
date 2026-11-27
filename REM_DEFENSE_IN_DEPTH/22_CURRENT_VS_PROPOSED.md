# Current REM v1.0 compared with the proposed REM-DiD

The proposed column is not implemented. Its status is given in the last column.

| Layer | Current REM v1.0 (exists, measured) | Proposed REM-DiD | Why (evidence) | Status of the proposal |
|---|---|---|---|---|
| 1 Input & Context | Segment labels; exact-string entity matching | Value lineage across tools and transformations; canonical value forms; TAE capture and verification | Reformatting defeats exact matching (P1 rises from 12 to 191); no trusted authorization input | Lineage and canonical forms: specified, offline-testable. TAE: needs a trusted channel; offline oracle feasibility only. |
| 2 Detection | One feature x~ctx2~, the union of 6 patterns | Sub-signals reported separately; injection classifier x~ctx1~; call-linked injection evidence; scope-change and override indicators against the TAE; correlation control | x~ctx2~ is a template fingerprint (recall 1.00 on one template, 0.00 on two others); episode-level only; no contribution to outcomes | x~ctx1~ needs a model choice (D-8). Call-linked evidence and indicators can be designed and tested offline. |
| 3 Behavioral Analysis | 4 history and 3 action features; x~beh1~ duplicates x~ctx2~ | Deduplicated features; credential-integrity evidence; divergence from the TAE; retry and alternative-route tracking; sequence model of legitimate workflows | Duplication (correlation 1.00); credential attacks rely on one family; x~beh4~ fires more on legitimate calls | Deduplication and credential evidence are offline-testable. Retry tracking needs a live, adaptive agent. |
| 4 Decision Engine | Predicates D1 and D2, then a learned expected-loss verdict | 4A: non-compensatory authorization constraints A1–A9 (extending the predicate stage). 4B: learned expected loss only for calls that pass 4A, which may tighten but never loosen. | The learned decision cannot represent authorization; deterministic guards stop every attack-labeled call in replay | 4A: offline-testable with an oracle or draft TAE. Measuring 4B's added value is mandatory. |
| 5 Mitigation | Step-level Allow/Block; Escalate and Modify withhold and coincide without a reviewer | Parameter-bound permits; Escalate through an authenticated reviewer channel (approvals become one-time TAE entries); one declared Modify mechanism that never changes recipients or amounts silently; fail-safe for unavailable inputs | Without a reviewer the four verdicts are two in effect | Permits and fail-safe: offline-testable. Reviewer and Modify need a decision; their effectiveness needs live runs. |
| Cross-cutting | Audit, offline fitting, observe-only CUSUM | Audit extended with constraint reason codes, permit identifiers and input availability | Auditability of the new decisions | Offline-testable |

**What stays fixed:**
- five layers;
- the frozen stage order (4A extends "policy predicates");
- ridge logistic estimation and Platt calibration;
- the expected-loss verdict for 4B;
- step-level mitigation semantics;
- CUSUM observe-only;
- attribution audit-only.
