# Published algorithm foundations and equation status

[PROPOSED — SUPERVISOR APPROVAL REQUIRED]

**No new numerical authorization score, loss, utility, confidence expression, or learned intervention estimator is introduced.** Candidate A is a nonnumeric rule implementation. Authoritative REM equation registry IDs remain unavailable and none is fabricated.

| Method | Original equation/location and variables | Assumptions and implementation status |
|---|---|---|
| PROVISO action values | v1 Eq. (1): conditional expected native outcome for instance x and candidate a; Eq. (7): action value minus development offset, followed by argmax | Verified in original full text. Requires native outcome supervision and candidate construction; calibration here selects an operating point, unlike Platt probability calibration. **Not implemented or adopted.** |
| Intervention-value learning | Calibration Is Not Control v2 Eq. (1): intervention advantage relative to continuation; Eq. (3): empirical regret relative to best observed branch | Verified in original full text. Requires outcomes of alternatives from the same state with fixed intervention semantics. **Not estimable here; not implemented.** |
| Consequence-aware selection | CASEL v1 Eq. (2): minimize residual failure probability × consequence plus compute/interaction costs over feasible modes | Verified in original full text. §IV-B uses residual-error ratios; simulation assumes intervention effectiveness. No measured banking ratios or comparable mode costs exist here. **Not adopted.** |
| Policy-based authorization | PROVISO §3.1 admissibility definition; CaMeL §5.2–5.3 policies and capabilities (not a numbered numeric authorization equation) | **Engineering adaptation only**: exact operation and argument grants, pinned external-field binding, no implicit trust promotion. No claim of exact CaMeL or PROVISO algorithm reproduction. |
| Original logistic/ridge model | Hastie, Tibshirani & Friedman (2009), *Elements of Statistical Learning*, §4.4/4.4.1 and §3.4.1; original repository traceability decorators | Reused baseline, unmodified. Original implementation combines logistic likelihood with L2 penalty, unpenalized intercept. Chapter-3 penalty convention differs by factor two from implementation lambda; inherited grid retained. Exact original-source equation-number certification was not completed in this session; no new source ID assigned. |
| Original sigmoid calibration | Platt (1999), §2; frozen REM transform is sign-flipped relative to Platt's A,B convention | Reused baseline. Primary historical pilot fits unsmoothed label NLL on OOF logits; secondary uses Platt-smoothed targets. This is an existing SC-4 conflict, not an exact reproduction silently asserted by this study. Exact original-source equation numbering remains unverified here. |
| Original expected-loss decision | Elkan (2001), *The Foundations of Cost-Sensitive Learning*, decision-theory principle; `CLAUDE.md` mathematical lock | Reused `ExpectedLossDecisionEngine` via original `A3Policy`. REM's four actions, tiers and losses are project adaptations, not Elkan's verbatim algorithm. Costs remain declared exploratory values, not elicited financial losses. |
| Uncertainty | Efron (1979), bootstrap resampling principle; `rem/evaluation/bootstrap.py` | Exact reuse of the existing grouped-percentile implementation: 2,000 group resamples with explicit seed. Cluster choices are study assumptions, not an independence theorem. |

The candidate adds only schema validation, Decimal equality, constrained IBAN normalization, source-digest/field lookup, categorical evidence and reservation bookkeeping. SHA-256 pins bytes; it does not prove that a document is authentic or that an operation is authorized. All delegated digests must be independently approved by trusted host code.

Published C code was not invented: the available [Calibration Is Not Control repository](https://github.com/bennidict23/calibration-is-not-control) was inspected at `9e3825b7eea89ee9dc88f1ccd11f277f8e10beb3`. `policy_learning.py` fits separate outcome/value models and consumes `continue_correct`, intervention outcomes and utility fields. Those labels are absent from REM logs. We neither relabel attack attempts as intervention utilities nor fit on manufactured branch data.

Candidate-selection decision: A is executable with explicit contracts; B and C need unavailable outcome data; CASEL additionally needs incomparable intervention parameters; D would compound unsupported assumptions and was not adopted. This is an engineering feasibility selection, not a claim that A outperforms B/C/D.

Scientific certification remains incomplete for inherited baseline equation numbering and original Platt full-text verification. This limits thesis readiness and is listed for supervisor review rather than hidden behind passing software tests.

## Published-defense reproduction feasibility

| Defense | Verified input/implementation evidence | Why no comparable score is reported |
|---|---|---|
| PROVISO | Full-text §3, Appendix C AgentDojo two-continuation recipe; reproducibility statement checked | No matching recovery trajectories, native paired outcomes, encoder/checkpoint or verified release URL in the inspected record. A provenance rule is not relabeled PROVISO. |
| Task Shield | Authoritative ACL full PDF; Appendix B Algorithm 1 and checker prompts | Needs real checker-model outputs and rethinking feedback. No model endpoint is configured; recorded trajectories cannot supply the missing judgments. |
| MELON | Official ICML PDF; official repository https://github.com/kaijiezhu11/MELON | Needs masked agent re-execution and resulting calls; these are absent from REM logs. |
| CASEL | Full text Eq. (2), §IV–VI | Its simulator modes/residuals/costs are not equivalent to REM's four-action banking interventions. Copying coefficients would manufacture comparability. |

No published benchmark score is inserted into the controlled comparison table. The absence of a configured LLM endpoint is a concrete local limit, not a claim that these methods are unreproducible in general.
