# 04 REM-A: corrected original architecture

Status: `[PROPOSED - EXPLORATORY]`. Written before implementation.

**Question.** Can the original REM concept become competitive with minimal corrections?

## What changes and what stays

- **Kept, unchanged:**
  - the frozen estimator (ridge logistic regression on the F4 evidence; stored cross-fitted cells);
  - Platt calibration on the logit;
  - the frozen two-verdict expected-loss decision (Allow vs Block). It is applied, as in the earlier learned arms, to **every restricted call that passes the deterministic witness**. That is the original REM position, where the probability decides each non-forced restricted call.
- **Corrected:** REM-A carries all REM-B corrections (`05`):
  - object binding;
  - the object-bound ledger;
  - E1;
  - the hardened refund licence E2h;
  - the provenance restriction.

**Flow:** front → predicates → object binding → contract witness → **learned stage (ridge + Platt + two-verdict expected loss)** → mitigation.

## What it answers
REM-A − REM-B measures the original learned stage on top of the corrected deterministic base.

The earlier evidence predicts **no gain and a possible utility cost**, because no attack-labelled call reaches the stage (`01` §3). That prediction is stated before the run so that it can be refuted.
