# 07 Algorithm selection (Phase 4)

## Prediction targets are distinct

| Target | Definition | Available labels | Used by |
|---|---|---|---|
| T1 malicious influence | the call serves the injection task (AgentDojo-derived reference labeller) | yes: 907 positives / 2,551 restricted calls (primary) | stored ridge + Platt estimator |
| T2 authorisation uncertainty | the call's value equals what the request determines | only through the audited reference table (6 user tasks); too few and too task-specific to train on without leaking evaluation tasks | **no model**: resolved deterministically (contract witness, E1, E2h, object binding) or escalated |
| T3 adverse consequence | the financial impact class of the operation | declared consequence tiers (frozen tier map) | expected-loss engine |

## Choices

| Mechanism | Choice | Justification | Rejected alternatives and why |
|---|---|---|---|
| Authorisation | deterministic front + contracts + **object binding** + ledger | least privilege, complete mediation, fail-safe defaults (Saltzer & Schroeder, 1975); capabilities designate objects (Dennis & Van Horn, 1966); fixes the confused-deputy pattern (Hardy, 1988) | LLM-generated policies (Progent, full): need a model and are not executable here; static allow-lists: cannot express amounts and objects (`01` §4) |
| Provenance | structured fields of executed bank reads only | the AgentDojo injection vectors are free text (subjects, files) | full data-flow tracking (CaMeL): requires changing the agent |
| Estimator (T1) | **stored** ridge logistic regression on F4 (unchanged) | interpretable; ROC-AUC 0.974; trained fits already exist (no refit, so no new leakage) | gradient boosting (an earlier competitive study's `GB` arm) gave no decision benefit there; deep models not justified by data size; **no model is retrained in this study**, because the bottleneck is reachability and target mismatch, not model family |
| Calibration | Platt on the logit (stored) | Brier 0.059, ECE 0.024 | isotonic, beta, temperature: excluded by the design lock |
| Decision | frozen expected-loss engine (Elkan, 2001); two-verdict in REM-A, three-verdict on eligible calls in REM-C | no new loss function | – |
| Consequence-independent comparator | frozen B1 operating threshold (Eq. 3.14) at frozen α_blk = 0.01, fitted on development scores only | the existing baseline of the approved design | a threshold tuned on held-out data: forbidden |
| Escalation | frozen escalation models: no reviewer (deployment) and idealised (upper bound) | Ch. 3 §3.11.7 | – |

No new equation is introduced:
- E1 evaluates the user's explicit arithmetic exactly, with rationals.
- Object binding is set membership over trusted fields.
- The decision rules are the frozen ones.
