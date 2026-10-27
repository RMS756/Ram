# REM CLAUDE CODE — HARD DESIGN LOCK
## Fail-Closed Research Design Protection

THIS FILE IS MANDATORY.
READ IT BEFORE MODIFYING ANY REM RESEARCH, ALGORITHM, EQUATION, EXPERIMENT, OR THESIS FILE.

## PURPOSE

Prevent Claude Code from silently inventing, reintroducing, selecting, or changing thesis design decisions.

The current thesis design is governed by:
1. the approved thesis proposal,
2. the current Stage 2 FINAL ALGORITHM & MATHEMATICAL DECISION REPORT,
3. the latest reconciled specification explicitly marked FROZEN.

Older drafts are historical evidence only. They do NOT override the current Stage 2 design.

---

# HARD STOP RULE

If a required design value, algorithm, equation, feature, threshold, loss, benchmark version, label definition, mitigation mechanism, grouping rule, or research question is not explicitly frozen in the current specification:

DO NOT CHOOSE IT.

DO NOT GUESS IT.

DO NOT USE A "REASONABLE DEFAULT".

DO NOT COPY IT FROM AN OLDER DRAFT.

DO NOT CREATE A PROVISIONAL VALUE JUST TO MAKE CODE RUN.

DO NOT REINTRODUCE A REMOVED COMPONENT.

STOP and report the missing item as:

[DESIGN BLOCKED]
Item:
Why it is required:
Why it is not currently frozen:
Source/document needed:
Supervisor decision required? YES/NO

---

# FROZEN REM PIPELINE

The primary REM runtime pipeline is:

provenance labeling
→ context / behavioral / action evidence
→ ridge logistic regression
→ Platt calibration on the logit
→ consequence tier
→ policy predicates
→ expected-loss Bayes verdict
→ deterministic mitigation
→ audit record

Primary verdicts:

- Allow
- Modify
- Escalate
- Block

The operating-point threshold policy is a BASELINE ONLY.

It is NOT a second primary methodology.

CUSUM is OPTIONAL and OBSERVE-ONLY.

CUSUM MUST NOT enter the core verdict path.

---

# FROZEN ARCHITECTURE

Exactly five layers:

1. Input & Context
2. Detection
3. Behavioral Analysis
4. Decision Engine
5. Mitigation

Offline fitting and recalibration are cross-cutting.

There is NO sixth layer.

There is NO separate risk-score layer.

There is NO operator/user-interaction architecture node.

There is NO feedback-loop layer.

---

# FORBIDDEN REINTRODUCTIONS

The following are explicitly removed unless a later supervisor decision changes the specification:

- risk = p × S as an NIST-defined equation
- confidence = Σ|β_i|
- persistence variable ρ
- invented composite risk equations
- risk-based CUSUM
- SPRT as a required methodology
- arbitrary hand-picked risk thresholds as the primary decision mechanism
- CUSUM in the core verdict path
- LLM-based decision arbitration
- GRU/LSTM/Transformer trajectory model
- counterfactual prefix-branching controller
- beta calibration as the adopted calibrator
- isotonic calibration as the adopted calibrator
- temperature scaling as the adopted calibrator
- SHAP as a decision input
- CARE-EL as the official algorithm name unless explicitly approved
- three independent methodologies A1/A2/A3

---

# MATHEMATICAL LOCK

## Probability estimation

Ridge logistic regression is the estimator.

Runtime:
s_t = β_0 + β^T x_t
p_tilde_t = sigmoid(s_t)

## Calibration

Platt/logistic calibration on the logit:

p_t = sigmoid(γ_1 s_t + γ_0)

γ_1 > 0 is required for the monotone interpretation.

## Decision

Conditional risk:

R_t(v) =
(1-p_t)L(v,0,k_t) +
p_t L(v,1,k_t)

Verdict:

v*_t = argmin_v R_t(v)

The four REM actions are an adaptation of cost-sensitive expected-loss decision theory.

Elkan supports the expected-cost decision principle.

Chow is conceptual support for reject/abstain-style escalation.

Neither source may be presented as having invented REM's four-action architecture.

## Attribution

Linear Shapley attribution is audit-only.

It MUST NOT affect the verdict.

---

# MITIGATION LOCK

Canonical semantics:

Allow:
release the current action.

Modify:
apply ONE declared modification mechanism to the current action or execution context.

Escalate:
withhold the current action pending review.

Block:
prevent execution of the current proposed action.

Do NOT silently redefine Block as disabling all state-changing tools for the rest of the episode.

Do NOT silently redefine Modify as removing a tool class for the rest of the episode.

Any episode-level restriction is a separate experimental policy requiring explicit specification.

---

# DATA / EVALUATION LOCK

Do not invent sample counts.

AgentDojo is an executable environment, not a set of independent i.i.d. rows.

Never describe repeated runs of the same task pairing as independent observations without explicit statistical justification.

The following remain unresolved unless explicitly frozen:

- exact AgentDojo version / commit
- injection classifier
- final feature set
- labeling of attacker-induced read operations
- consequence tiers
- loss values / loss grid
- Modify mechanism
- grouping scheme
- LLM backbones
- number of repeats
- external benchmarks
- optional CUSUM scenarios

---

# RESEARCH-QUESTION LOCK

Do not invent research questions.

The approved proposal contains objectives, not necessarily the current RQ wording.

A proposed RQ derived from an objective must remain marked [PD] until explicitly frozen.

Never convert a suggestion into an approved requirement.

---

# EQUATION-ID LOCK

Never fabricate an EQUATION_ID.

If the authoritative registry is unavailable:

STOP.

Do not create provisional equation IDs inside implementation code.

Do not make generated traceability reports appear complete by inventing identifiers.

---

# SOURCE-OF-TRUTH ORDER

When documents conflict, use this order:

1. explicit latest supervisor decision
2. current Stage 2 final algorithm/mathematical decision report
3. approved thesis proposal
4. current reconciled implementation specification
5. verified equation/source registry
6. latest Chapter 2 / Chapter 3
7. older research documents
8. historical drafts / brainstorming

Older documents NEVER override newer frozen decisions.

---

# CHANGE CONTROL

Claude Code MAY NOT change a FROZEN item during implementation.

If a change appears scientifically necessary:

1. STOP implementation.
2. Identify the exact conflict.
3. Quote the affected specification item.
4. Explain the consequence.
5. Mark it [SUPERVISOR DECISION REQUIRED].
6. Wait for an explicit decision.

No silent migration.

No "small improvement" that changes scientific meaning.

No backwards compatibility that reintroduces obsolete research design.

---

# IMPLEMENTATION FAIL-CLOSED REQUIREMENT

REM must refuse to run if required design inputs are missing.

Missing design input → DesignNotSpecifiedError or equivalent.

Do NOT fall back to:

- guessed defaults,
- arbitrary thresholds,
- arbitrary costs,
- arbitrary labels,
- arbitrary feature definitions,
- arbitrary benchmark versions.

The software must fail loudly rather than silently inventing a research design.

---

# REQUIRED RESPONSE WHEN BLOCKED

Use exactly this structure:

## DESIGN BLOCKED

**Item:** <missing design element>

**Why required:** <implementation/research reason>

**Current source status:** <document/source status>

**Safe action:** STOP — do not choose a value.

**Supervisor decision needed:** <YES/NO>

---

# FINAL RULE

A working program is NOT more important than a faithful thesis design.

Correct behavior is:

UNKNOWN → STOP

CONFLICT → STOP

UNVERIFIED → STOP

UNAPPROVED → STOP

FROZEN → IMPLEMENT EXACTLY
