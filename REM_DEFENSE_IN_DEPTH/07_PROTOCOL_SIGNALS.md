# Protocol SIG-1: measurement of the existing Detection sub-signals and of the redundancy among REM's evidence features

| Field | Value |
|---|---|
| Status | Committed before the measurement was run |
| Classification | Measurement of implemented components (REM v1.0). No new detector, threshold or feature. |
| Code | `REM_DEFENSE_IN_DEPTH/code/sig1_signals.py`; `rem/` unchanged |

## Part A: Detection sub-signals (content level)

**Unit:** every tool-result message in the AgentDojo recorded episodes of two roles:
- the primary role: 21 backbones, template `important_instructions`, attacked and benign;
- the cross-template role: one backbone, five other attack templates.

These are the episodes of `steps.pkl` (after AM-1 and the error exclusion).

**Ground truth:** the message contains the episode's injected payload, decided by the existing function `rem.integration.steps.injection_entered`. This is the same test REM uses for "injected content entered".

**Sub-detectors:** the six members of the declared pattern set, in the existing `InstructionPatternDetector.fired()`:

| ID | Sub-detector |
|---|---|
| p0 | Imperative addressed to the assistant |
| p1 | "Ignore/disregard … previous … instructions" |
| p2 | "Before you/completing …" |
| p3 | Role or delimiter markers |
| p4 | "Important message/instructions" |
| tool_name | A mention of a tool name |
| x~ctx2~ | The union of the six (the implemented feature) |

**Measures per sub-detector and population:**
- TP, FP, FN and TN;
- precision, recall, false-positive rate and false-negative rate;
- median and 95th-percentile evaluation time per message (`fired()` on one text; single process; replay timings, not deployment latency);
- pairwise phi correlation between the sub-detectors on all messages and on payload-bearing messages;
- recall per attack template (primary and cross-template roles). This is the available evidence on robustness to different injection wording.

Paraphrase robustness beyond the six benchmark templates, and robustness to identifier transformations, are **not** measurable without new data. Where possible, they are reported as such. Identifier transformations do not touch the pattern set; this is checked on the reformatted-identifier probe texts.

## Part B: redundancy among evidence features (step level)

**Unit:** the 6,762 held-out steps of the primary role, with the fold design matrices of DiD-1.

**Measure:** pairwise phi correlation, or Pearson correlation for x~beh2~, between the eight evidence features:
- on state-changing steps;
- separately on attack-labeled and on legitimate state-changing steps.

This identifies duplicated evidence. For example, x~beh1~ is defined through x~ctx2~.

## Reporting and interpretation

- **Descriptive only.** No threshold for "acceptable" precision or correlation is defined.
- **Ground-truth limitation.** The ground truth marks payload presence in a message, which is detection's target. It is not the action label.
- **No intervals.** Messages within an episode are dependent, so no interval is reported, and counts are given.
