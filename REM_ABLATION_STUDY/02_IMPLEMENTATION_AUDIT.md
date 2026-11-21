# 02 Implementation audit: REM's five layers in the code (REM v1.0, `rem/` at `9fddfa7`)

## Layer to module map

| Layer (Chapter 3) | What it does | Implementation | Output consumed by |
|---|---|---|---|
| 1 Input & Context | Captures the context; hygiene (strip invisible and format characters); provenance labels (trusted, semi-trusted, untrusted); entity extraction (IBANs, amounts, credentials, profile values) | `rem/algorithms/context/provenance.py` (`strip_invisible`, `Segment`, `TrustLevel`, `extract_ibans`, `value_occurs_in`); used by `EpisodeTracker` in `rem/algorithms/behavior/evidence.py` | Layer 3 features `x_act1`–`x_act3` and `x_beh1`; availability flags for predicate D2 |
| 2 Detection | `x_ctx1`: injection classifier score (**absent**, D-8). `x_ctx2`: instruction-pattern indicator over untrusted segments added since the previous step. | `rem/algorithms/detection/instruction_patterns.py` (`InstructionPatternDetector`) | estimator (`x_ctx2`); Layer 3 (`x_beh1` uses `x_ctx2 = 1`) |
| 3 Behavioural Analysis | Episode history `H_t`. `x_beh1` post-observation shift, `x_beh2` repeated calls, `x_beh3` privilege escalation, `x_beh4` transition deviation (benign reference). It also computes the action evidence `x_act1` argument provenance, `x_act2` destination novelty and `x_act3` sensitive egress from Layer-1 labels. | `rem/algorithms/behavior/evidence.py` (`EpisodeTracker`, `BenignReference`, `FEATURE_GROUPS`) | estimator |
| 4 Decision Engine | Ridge LR score; Platt-type calibration on the logit; consequence tier; predicates D1 and D2; minimum expected loss over Allow / Modify / Escalate / Block | `rem/algorithms/detection/ridge_logistic.py` (estimator; the file name is historical; decision SC-6); `rem/algorithms/calibration/logit_nll.py`; `rem/algorithms/decision/{consequence,loss_matrix,expected_loss,policy}.py`; `rem/algorithms/a3.py` (`A3Policy`) | Layer 5 |
| 5 Mitigation | Step-level: Allow releases the call; Modify, Escalate (no reviewer) and Block withhold it, and the refusal is returned to the agent | `rem/integration/agentdojo_replay.py` (`RemGuard._mitigate`); `rem/core/mitigation.py` | environment |
| Audit (cross-cutting) | Per-call record; linear SHAP (audit only) | `rem/core/audit.py`; `rem/algorithms/attribution/linear_shapley.py`; audit tuple in `RemGuard.evaluate` | logs |

**Where the experiment runs.** The replay harness is `RemGuard` and `replay_episode` (`rem/integration/agentdojo_replay.py`), driven by the frozen pilot pipeline `experiments/pilot/run_main.py`. Each arm is a configuration dictionary passed to its `_replay_job`: decide function, scorer, variant, reviewer model, `observe_only`. **No REM file is changed.**

## Dependencies that constrain ablation

1. **`x_beh1` depends on `x_ctx2`.** It is 1 only if the most recent untrusted tool result had `x_ctx2 = 1`.
   - Removing only `x_ctx2` from the estimator (A1a) leaves Detection's signal inside `x_beh1`.
   - Removing the Detection layer requires removing both (A1b).
2. **Action evidence and D2 depend on Layer-1 provenance labels.**
   - Ablating the labelling would leave `x_act*`, `x_beh1` and D2 without inputs.
   - So the labelling layer cannot be removed without fabricating signals: **not valid**.
   - Its evidence can be removed from the estimator (AIC) while D2 keeps its availability check.
3. **`x_ctx1` does not exist** (no classifier), so "Detection" in REM v1.0 means `x_ctx2` alone.
4. **The learned decision is one block.** Estimator, calibration and expected loss together produce the non-predicate verdicts. Bypassing it (A3) leaves only D1 and D2, which exist independently in `PredicatePolicy`.
5. **Mitigation semantics.** Under step-level semantics without a reviewer, Modify, Escalate and Block all withhold the call (R8 A5). Shadow mode (A4) is the existing `observe_only` switch of `GuardConfig`: verdicts computed, all calls released.
6. **History coupling.**
   - Tool results of withheld calls are empty, so later features (e.g. `x_beh1`) can differ between arms even under NO-ADAPT replay.
   - The recorded call sequence is the same in every arm; this is checked per episode (`episodes_with_different_call_count`).

## Validity of each requested configuration

| Requested | Implemented as | Valid? |
|---|---|---|
| A0 Full REM | A0 | yes |
| A1 without Detection contribution | A1a (feature) and A1b (layer) | yes, with the coupling stated |
| A2 without Behavioural Analysis | A2 | yes |
| A3 without learned decision | A3 (predicates only); complement A3P (learned only) | yes |
| A4 Mitigation in shadow mode | A4 (`observe_only`, step level) | yes, offline only |
| Input & Context provenance / context integrity | AIC (provenance evidence); hygiene check | partially: labelling itself not removable; hygiene tested for exercise |
| Detection classifier `x_ctx1` | – | **not valid** (absent) |

## Limits of offline replay for these ablations

**NO-ADAPT.** A withheld call does not change what the recorded agent proposes next. Withholding can still change the replayed environment state and therefore the AgentDojo outcome, but it cannot capture retries or re-planning. The replay outcomes are thus **not closed-loop ASR or task completion**.
