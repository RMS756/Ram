# REM HARD-LOCK START PROMPT

Before doing ANY code change, read `CLAUDE.md` and enforce it as a fail-closed research-design contract.

You are not authorized to select missing thesis design parameters.

Your job is to implement the CURRENT FROZEN REM DESIGN, not to redesign it.

## MUST DO FIRST

1. Read `CLAUDE.md`.
2. Read the supplied Stage 2 Final Algorithm & Mathematical Decision Report.
3. Read the approved proposal.
4. Read the Equation-to-Source verification material.
5. Read the current implementation specification, if present.
6. Produce a reconciliation table:
   - item
   - current value
   - source
   - status: FROZEN / PD / UNVERIFIED / CONFLICT
7. DO NOT code until this table has been produced.

## ABSOLUTE PROHIBITIONS

Do NOT:
- select a new algorithm;
- choose a missing parameter;
- invent an equation;
- invent an equation ID;
- invent a threshold;
- invent a loss;
- invent a research question;
- invent a benchmark version;
- restore A1/A2/A3 as three methodologies;
- restore CARE-EL as the official algorithm name;
- move CUSUM into the verdict path;
- redefine Block or Modify silently;
- introduce a sixth layer;
- add a new neural trajectory model;
- add counterfactual control;
- add beta/isotonic/temperature calibration;
- treat SHAP as a decision input.

## FROZEN CORE

Primary pipeline:

provenance
→ evidence
→ ridge logistic regression
→ Platt-on-logit
→ consequence tier
→ policy predicates
→ expected-loss Bayes verdict
→ deterministic mitigation
→ audit

Architecture:

L1 Input & Context
L2 Detection
L3 Behavioral Analysis
L4 Decision Engine
L5 Mitigation

Offline fitting/recalibration is cross-cutting.

## FAIL-CLOSED

If anything required is missing:

STOP.

Report:

[DESIGN BLOCKED]
Item:
Why required:
Source/document needed:
Supervisor decision required? YES/NO

Do not choose a substitute.

## IMPLEMENTATION RULE

Only implement FROZEN items.

PD / UNVERIFIED / CONFLICT items must remain unresolved and must not be converted into code defaults.

A failed run is acceptable.
An invented scientific decision is not.
