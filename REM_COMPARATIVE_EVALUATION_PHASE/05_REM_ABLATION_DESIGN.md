# 05 REM ablation design (verified against the current code, 22 November 2026)

**Reference arm: A0, full REM v1.0** (`rem/` at `9fddfa7`, frozen pilot state; step-level mitigation, no reviewer).

**No new ablation arm is created in this phase.** The arms below are those of the ablation protocol frozen at `93e6630` (`REM_ABLATION_STUDY/01_ABLATION_PROTOCOL.md`), whose outputs are hash-checked. This file re-states each arm in the form required here.

**Code-level mechanism of every arm.** A different configuration dictionary is passed to the frozen replay job (`experiments/pilot/run_main._replay_job`): a different decide function, scorer, feature order or `observe_only` flag. **No REM source file is edited.**

## Layer map (from the code)

| Layer | Implemented responsibility | Module |
|---|---|---|
| 1 Input & Context | hygiene (`strip_invisible`), provenance labels (trusted / semi-trusted / untrusted), entity extraction | `rem/algorithms/context/provenance.py`; `EpisodeTracker` |
| 2 Detection | `x_ctx2` instruction-pattern indicator; `x_ctx1` classifier **absent** (decision D-8) | `rem/algorithms/detection/instruction_patterns.py` |
| 3 Behavioural Analysis | `x_beh1`–`x_beh4`; also computes `x_act1`–`x_act3` from Layer-1 labels | `rem/algorithms/behavior/evidence.py` |
| 4 Decision Engine | ridge LR, Platt calibration on the logit, consequence tier, predicates D1/D2, expected-loss verdict | `ridge_logistic.py`, `logit_nll.py`, `decision/*`, `a3.py` |
| 5 Mitigation | step-level: Allow releases; Modify, Escalate (no reviewer) and Block withhold the current call | `agentdojo_replay.RemGuard._mitigate` |

## Arms

| Arm | Component disabled | Code-level change | Affects other components? | Hypothesis: security (not a result) | Hypothesis: benign utility | Hypothesis: runtime | Test confirming the arm |
|---|---|---|---|---|---|---|---|
| A1a | Detection feature `x_ctx2` | estimator refit without `x_ctx2` (existing fit `no_ctx`) | `x_beh1` keeps the detector's signal | no change | no change | ≈ | `test_configurations_change_only_the_ablated_component` (ablation tests) |
| A1b | Detection layer (`x_ctx2` and `x_beh1`, which is defined through it) | new refit with the frozen nested cross-fit, only the feature order changed | Behavioural evidence loses `x_beh1`: a **coupled** removal, stated | small or no change | no change | ≈ | same test (`ORDER_A1B`) |
| A2 | Behavioural evidence `x_beh1`–`x_beh4` | refit `no_beh` | none | small loss | gain (fewer false positives) | ≈ | same test |
| AIC | Provenance/action evidence `x_act1`–`x_act3` | refit `no_act`; predicate D2 still reads availability | D2 unchanged | loss | uncertain | ≈ | same test |
| A3 | **Learned decision** (estimator, calibration, expected loss) | decide = predicates D1/D2 only, otherwise Allow; no scorer | none | large loss if the learned decision carries the protection | gain | lower | `test_predicate_arms_isolate_the_deterministic_controls` |
| A3P | Deterministic predicates D1/D2 | policy `A3_nopred` | none | no change | no change | ≈ | same test |
| A4 | Mitigation enforcement (shadow mode) | `observe_only=True` | verdicts are computed but every call is released | equals no defence | equals no defence | ≈ A0 | `test_shadow_mode_and_no_defence_never_withhold` |

## Not cleanly isolatable (not run as ablations)

- **Provenance labelling itself.** It feeds `x_act*`, `x_beh1` and D2; removing it would leave them without inputs, so the arm would have to fabricate signals.
- **The `x_ctx1` classifier.** It does not exist in the code.
- **Hygiene.** It changes 0 of 16,727 tool outputs in these data, so the data cannot exercise it.

## Method rules

- **Removals:** one per arm, except A1b, which is labelled as coupled.
- **No change** to thresholds, losses or algorithms.
- **Episodes and pairing:** identical episodes and call positions, with paired comparisons.
- **Unit:** the episode-level analysis in this phase (`06`) is primary; call-level results are in `REM_ABLATION_STUDY`.
- **What is tested:** "the learned Decision Engine versus deterministic rules" is tested in two ways:
  1. A3 vs A0, against REM's own rules;
  2. PG vs A0 (`02`), against Progent's published hand-written rules.
