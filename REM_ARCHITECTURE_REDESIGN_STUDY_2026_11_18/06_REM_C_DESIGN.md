# 06 REM-C: hybrid authorisation and risk architecture

Status: `[PROPOSED - EXPLORATORY]`. Written before implementation.

**Question.** Does learned risk estimation add measurable value once explicit authorisation and provenance are enforced?

## Role of the learned component (testable)

- **Deterministic rules are sufficient whenever they reach a definite verdict:**
  - authority denied → Block;
  - object not designated → Block;
  - amount mismatch → Block;
  - allowance exhausted → Block;
  - fully verified or unconstrained → Allow.
- **The learned component is invoked only for *eligible unresolved* calls.** These are calls whose authority, object and scope are established, but whose amount or condition evidence is unresolved (`contract_unresolved`). In REM-B these are escalated.
- **Uncertainty estimated.** The stored estimator predicts **malicious influence** (target: the AgentDojo-derived attack label of the call). It does not predict whether an unresolved amount is the correct one. This mismatch is a known limitation, and the experiment measures its consequence through the audited value-violation metric (`03`).
- **Calibration.** Platt on the logit (stored fits).
- **Consequence.** The frozen expected-loss engine over {Allow, Escalate, Block} (Modify excluded; its semantics withhold), using the frozen loss grid of the stored cell and the call's consequence tier. The verdict is argmin of the conditional risk (frozen equation; no new mathematics).
- **Human escalation.** Escalate withholds (no reviewer). Separately, the idealised reviewer is reported as an upper bound.
- **Execution feedback.** The ledger commits or releases on the execution signal, as in REM-B. The learned stage has no state.
- **Invariant I5.** The learned stage can release only eligible unresolved calls. It can never release a call refused for authority, object or scope reasons.

## Comparators within the hypothesis

- **REM-C-T (consequence-independent threshold).** Same estimator and same eligible calls. Allow iff p < θ, where θ = the operating threshold of the frozen baseline B1 (Ch. 3 Eq. 3.14, `rem.algorithms.a1.operating_threshold`) at the frozen α_blk = 0.01 (`configs/exploratory/pilot_e0.yaml`). It is fitted only on **development** scores: the learned scores of restricted calls without an attack label in benign episodes of the primary population, stored by the controlled study. It is never fitted on held-out data.
- **REM-C-raw.** As REM-C, with the raw logistic probability (no Platt), which isolates calibration.
- **REM-B-R (upper bound).** REM-B with the frozen idealised reviewer resolving every escalation.

## Expected risk of this design (stated in advance)
On the replay populations the eligible unresolved calls carry no attack labels. REM-C can therefore show a utility gain with no measured attack cost, while releasing **wrong amounts** (about 83 agent-error amounts in the calculation-cue group of `REM_IMPROVEMENT…/03`). The audited value-violation metric is a primary security measure for exactly this reason.
