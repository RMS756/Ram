# 04 — Algorithm candidate comparison

**Status:** `[PROPOSED — SUPERVISOR APPROVAL REQUIRED]`. Sources: the six supplied papers (`02`), the repository at commit `cca4968` and later on branch `claude/rem-authz-generalization-study`.

This comparison was made **before** any candidate outcome was computed (it is the reasoning behind the frozen protocol `06`). What the experiments later showed is in `08`; the two are kept apart on purpose.

## 1. Candidates

| | Candidate A — provenance-informed authorization policy | Candidate B — action-conditioned intervention value | Candidate C — hybrid | Candidate D — deterministic authorization rule |
|---|---|---|---|---|
| Primary source | PROVISO (Yan et al., 2026) | Calibration Is Not Control (Zhang et al., 2026) | B's decision rule + authorization evidence motivated by PROVISO's admissibility statement and Task Shield's delegation remark | PROVISO's admissibility statement read as a rule; examiner's provenance rule from the R4 review |
| Core mechanism | Typed-memory controller valuing the proposed action against an alternative; commit argmax of calibrated value (Eq. 1–7) | Supervise on the outcome of each available action at the same state; choose argmax Q_a(h) (Eq. 1) | As B, with two deterministic authorization features added to REM's eight | Withhold a state-changing call when its identity arguments are not in the user's words (and variants) |
| Fitted parameters | 17.40M, per benchmark | Whatever estimator is used; here REM's ridge logistic (≤ 11 coefficients per target) | As B | None |
| Needs an LLM or encoder at run time | Yes (frozen ModernBERT-large; an LLM agent for recovery rollouts on AgentDojo) | No | No | No |
| Needs intervention-outcome data | Yes (native outcomes of both candidates) | Yes (branch outcomes) | Yes | No |
| Outcome data obtainable here | Not in PROVISO's form (no recovery trajectories) | **Yes**: REM's replay can withhold one call and re-run the rest of the recorded episode | Yes | n/a |

## 2. Criteria

| Criterion | A — PROVISO | B — intervention value | C — hybrid | D — rules |
|---|---|---|---|---|
| 1. Alignment with the gap (authorization, generalization, over-defence) | High in aim; its own limitation is per-benchmark fitting with no transfer studied | Medium: addresses over-defence through the utility side of the decision; says nothing about authorization | High | High for authorization; no learning, so no generalization question |
| 2. Mathematical traceability | Published equations, but the controller is a learned network that cannot be re-derived | **High**: two published equations; the adaptation is one substitution | High for the rule; the two features are declared definitions, not published formulas | High: no equation needed |
| 3. Published evidence | Four tasks; AgentDojo with all four suites, one agent | ALFWorld strong; small or null on two reasoning benchmarks; **no security benchmark** | None for the combination | The R4 examiner's observe-only table |
| 4. Original implementation available | Not named in the paper | Named, not accessed in this session | — | — |
| 5. Compatibility with REM's five layers | Would replace Layers 2–4 with a network | Keeps all five layers and REM's estimator; changes the training target and the decision rule | As B, plus Layer 1/2 evidence | Fits the existing policy-predicate stage |
| 6. Overfitting / leakage risk | High at this data size (17.40M parameters; 3,334 episodes; 16 user tasks) | Moderate: outcome labels depend on the benchmark's own success checks | Moderate; features written by an author who knows the tasks | Low for fitting; high for benchmark artefacts |
| 7. Generalization to held-out tasks | Not studied by its authors beyond user-task folds | Unknown: the hypothesis under test | Unknown: the hypothesis under test | Not applicable (nothing fitted) |
| 8. Preserving legitimate utility | Claimed on AgentDojo with a different agent and protocol | Plausible: the withhold branch is costed by what it actually breaks | Plausible | Depends on how many legitimate values come from documents |
| 9. Computational cost | Encoder forward pass per decision | Same order as REM | Same order as REM | Lowest |
| 10. Feasibility of reproducible evaluation here | **Not feasible** (no code named, encoder host blocked, no agent model for rollouts) | **Feasible** | **Feasible** | **Feasible** |

## 3. Why candidate A could not be implemented faithfully

1. No implementation is named in the supplied paper.
2. Its encoder (ModernBERT-large) must be downloaded from a host that this session's network policy blocks.
3. On AgentDojo it is a *candidate-selection* method: it chooses between the agent's trajectory and a recovery trajectory produced by an LLM agent. No model API is available, and recorded traces contain no recovery trajectories.
4. A 17.40M-parameter controller fitted on this corpus would not be the published system and would be at high risk of memorizing 16 user tasks.

A reduced "PROVISO-like" model would be an invention, not a reproduction. It was therefore **not built**. What is taken from PROVISO is its problem statement and its admissibility rule, both quoted in `02`.

## 4. Why candidate B fits REM's situation

- REM's four verdicts are costed by *declared* losses: every withheld legitimate action is assumed to cost C_FA, every escalation C_esc, whatever it actually does to the task.
- In step-level replay without a reviewer, Modify, Escalate and Block have the same execution effect (measured in `03`, Problem E: 0 of 3,313 episodes change when all three are replaced by Block).
- Calibration Is Not Control states the remedy formally: value each available action by its outcome at the same state. REM's replay harness already provides the required "prefix branching".
- Its Remark 1 is also the published explanation of an earlier finding of this project (thresholds re-selected on uncalibrated scores reproduce B1 exactly).

## 5. Selection made before the experiments

- **Primary candidate: C** (arm `M11+AZ`), because it is the only candidate that addresses authorization *and* over-defence, with B's published decision rule.
- **B alone** (arm `M11`) is its ablation with authorization evidence removed.
- **D** supplies the mandatory simple baselines: `P1` (x_act1), `P2` (x_act1 ∨ x_act2), `A1` (explicit or delegated), `A2` (explicit only).
- **A** is reported as not evaluable.

Evidence supporting the selection: published equations (B), a published admissibility statement (A), a measured property of REM's replay (Problem E), and feasibility.

Hypotheses still requiring test at that point: that outcome-supervised models transfer to held-out user tasks and attack objectives; that the two authorization features carry information beyond `x_act1` and `x_act2`; that the candidate improves benign utility without a detectable security cost.

**Outcome (see `08`):** the hypotheses were not supported. The selection above is recorded unchanged so that the reader can see what was expected before the data were examined.
