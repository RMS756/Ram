# Deliverable 9: Research contribution statement for the master's thesis [PD]

**Status:**
- **Proposed wording, not approved.**
- Nothing in REM-X is implemented or evaluated.
- The thesis is not edited by this document.
- Every claim below is **conditional on experiments not yet run** (files 07, 08) and on full-text verification of the prior art (file 10).
- If those conditions fail, the conditional parts are dropped. They are not softened into vaguer claims.

## 1. What the thesis can already state (REM v1.0, evaluated)

The following is unchanged by REM-X:
- REM, a five-layer runtime evaluation and mitigation framework for financial AI agents;
- its frozen pipeline (ridge logistic regression, Platt calibration on the logit, consequence tier, expected-loss verdict);
- its evaluation on AgentDojo banking, as reported in the thesis.

## 2. Candidate contribution statement (if experiments confirm it)

> *This thesis presents REM, a five-layer runtime security framework for financial AI agents.*
>
> *Building on established mechanisms, REM-X adapts them to a black-box agent mediation setting:*
> - *field-level provenance (as in CaMeL, Fides and RTBAS);*
> - *exact-action, single-use authorization and execution-bound verification (as in AIS and AgentCap);*
> - *deterministic precedence over learned risk.*
>
> *Its specific contribution is **evidence-gated source delegation**, an integration in which:*
> - *the user may delegate named financial fields to a named document;*
> - *a delegated value is admitted only when it is deterministically extracted from that document's data fields, the document carries no detected injection, and declared economic limits hold.*
>
> *On [suite, version, agent phase], REM-X [preserved / did not preserve] benign task completion on document-delegated tasks relative to a strict-provenance policy and a parameter-provenance authorization baseline, at [equal / different] attack success, including attacks injected into the delegated documents themselves.*
>
> *The thesis further proposes and applies an evaluation method for defense-in-depth claims: **test-time evasion of each control with the others fixed**, in addition to removal ablation. On REM's own components, this method reversed a conclusion that removal ablation alone would have drawn.*

The bracketed parts are filled **only from frozen-protocol results**.

**Rules for filling them:**
- If H-AC1 fails, the delegation sentence is replaced by a negative-result sentence.
- If evidence-gated delegation turns out to exist in prior work (AgentCap, AIS or ROPE full texts), the word "contribution" is withdrawn for it. It is then described as an adoption, evaluated in the financial setting.

## 3. What is explicitly *not* claimed

1. **Not a new architecture class:**
   - not a new provenance, capability, authorization, ledger or reconciliation mechanism;
   - not "intent-bound authorization" (AIS);
   - not "first" anything.
2. **No superiority over systems not run under identical conditions:**
   - Agent-Sentry, RTBAS, Fides, AIS;
   - AgentCap itself: only a labelled class re-implementation is compared.
3. **No adaptive-robustness claim** from NO-ADAPT replay or from the scripted agent.
4. **No claim that the learned decision improves security behind authorization.** The preliminary evidence is against it (file 06).
5. **No novelty for the transaction ledger, atomic reservation, adapter re-check or reconciliation.** These are adopted engineering (D2).

## 4. Relationship to the original thesis objectives

- The title, topic and five-layer architecture are unchanged.
- REM-X is positioned as:
  - **"future work evaluated"**, if Phase A results are obtained and approved; or
  - **"future work proposed"**, otherwise.
- The choice between these is a supervisor decision.
- Any research question derived from REM-X stays marked **[PD]** until frozen.
