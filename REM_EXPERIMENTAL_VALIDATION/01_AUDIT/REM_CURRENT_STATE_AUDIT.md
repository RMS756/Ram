# REM — Current State Audit (5 Nov 2026)

**Scope:**
- the repository on branch `claude/melon-rem-extension`, at commit `f79f271` before this report;
- the five-chapter thesis (`REM_FINAL_THESIS/final_five_chapters/`);
- every result file cited below.

**Method:** statements marked "verified" were checked against executable code, tests or re-executed results in this or earlier sessions of this project. Nothing is taken from the thesis text alone.

## 1. Repository structure (relevant parts)

| Path | Content |
|---|---|
| `rem/algorithms/` | `detection/ridge_logistic.py` (ridge LR); `calibration/logit_nll.py` (logit calibration, label-NLL, **primary**) and `calibration/platt.py` (Platt smoothed targets, secondary); `decision/expected_loss.py`, `loss_matrix.py`, `consequence.py`, `policy.py` (predicates D1/D2); `a3.py` (REM expected-loss policy); `a1.py` (operating-point threshold baseline); `a2.py` + `behavior/cusum.py` (optional CUSUM); `behavior/evidence.py` (features); `context/provenance.py`; `attribution/linear_shapley.py` |
| `rem/core/` | Frozen fail-closed reference pipeline (`pipeline.py`), mitigation, audit, results types |
| `rem/integration/` | AgentDojo trace loader, **evaluation path** `agentdojo_replay.py` (`RemGuard`, `GuardedToolsExecutor`), live harness `agentdojo_live.py`, MELON adapter `melon_rem.py` |
| `rem/deployment/gateway.py` | REM as an HTTP gateway service |
| `rem/evaluation/` | Nested grouped cross-fitting, metrics, calibration metrics, grouped bootstrap, runtime timing |
| `experiments/pilot/` | Exploratory pilot E0–E6 (`run_all.sh`) |
| `experiments/live/`, `experiments/melon_rem/` | Live-agent and MELON harnesses (implemented; never run with an LLM) |
| `experiments/deployment_sim/` | Deployment simulation (executed) |
| `experiments/rem_lite/` | REM-Lite ablation (executed, Mode A) |
| `configs/exploratory/pilot_e0.yaml` | All declared design values (exploratory, not supervisor-approved) |
| `tests/` | 25 test modules |
| `results/pilot_R2`, `pilot_R4`, `deployment_sim`, `rem_lite` | Committed result sets |

## 2. Implementation status against the intended architecture

| Intended component | Implemented? | Notes (verified) |
|---|---|---|
| L1 Input & Context (provenance labelling) | Yes | `context/provenance.py`, `EpisodeTracker` |
| L2 Detection | **Partly** | Instruction-pattern indicator x^ctx₂ only. **The injection classifier x^ctx₁ is not implemented** (no model chosen; D-8) |
| L3 Behavioral Analysis | Yes | x^beh₁–x^beh₄, action evidence x^act₁–x^act₃ |
| L4 Ridge logistic regression | Yes | Penalty selected by inner cross-validation |
| L4 "Platt calibration" | Yes, **with a caveat** | The primary calibrator is logistic calibration **on the logit** p = σ(γ₁s + γ₀), fitted by label NLL (`logit_nll.py`). Platt's smoothed-target variant exists as secondary (`platt.py`). Which one is the thesis's "Platt calibration" is open (D-3 / SC-4). γ₁ > 0 in every fold |
| L4 Expected-loss (Bayes) decision | Yes | `a3.py`: argmin of conditional risk over {Allow, Modify, Escalate, Block}, with feasible set, predicates and the Chapter 3 tie order (D-4 open) |
| L4 Linear SHAP attribution | Yes, audit-only | Written to the audit record; never used by the decision (tested) |
| L4 CUSUM | Yes, **observe-only** | Never in the verdict path |
| L5 Mitigation, four actions | **Partly validated** | Allow: releases the call. Block: withholds the call. Escalate: there is **no real reviewer**, only an idealised label-based bound and a no-reviewer bound. Modify: **no argument-rewriting mechanism**; under step-level semantics, Modify withholds the current call, **the same immediate effect as Block**; under episode-level semantics it restricts a tool class |
| Two execution paths | Yes | `rem/core/pipeline.py` is the frozen reference pipeline. **All experiments use the evaluation path** (`RemGuard`) |

## 3. Evaluation status

| Evaluation | Status | Evidence |
|---|---|---|
| Offline held-out classification and calibration (E1) | Executed and reproduced | `results/pilot_R2/e1_crossfit.json`; re-execution with 0 analytical differences |
| Observe-only decisions (E2/E5/E6), ablations, loss grid | Executed and reproduced | `results/pilot_R2/` |
| NO-ADAPT replay in the AgentDojo sandbox (B0/B1/REM …) | Executed and reproduced | `e4_e5_enforcement_replay.json` |
| Deployment simulation (gateway service + simulated bank API) | **Executed 5 Nov 2026** | `results/deployment_sim/`: 0 parity mismatches |
| REM-Lite ablation (Mode A) | **Executed 5 Nov 2026** | `results/rem_lite/2026-11-05/` |
| Live LLM agent (Mode B), any configuration | **Not executed** | No LLM credential; `api.openai.com` blocked by the network policy; no spending authorisation |
| MELON (any mode) | **Not executed** | MELON re-queries the LLM and calls OpenAI embeddings, so it cannot be evaluated on recorded traces, and live execution is blocked as above |
| Human label audit | Not done | — |

## 4. Reproducibility

- **Tests:** 233 pass in the main environment (AgentDojo 0.1.35) and 30 in the MELON environment (AgentDojo 0.1.29).
- **Frozen state:** the cross-fit state is byte-identical across four re-executions (sha256 `27464b4d…`).
- **Deployment simulation:** reproduces the in-process replay exactly, episode by episode and verdict by verdict.

## 5. Discrepancies between thesis wording and code (to be kept visible)

1. The core algorithm is often summarised as "Platt calibration"; the primary implementation is label-NLL logistic calibration on the logit (same functional form). See D-3.
2. The four actions are implemented as **decisions**, but only Allow and Block have operationally distinct, validated effects. Modify equals Block in immediate effect under step-level semantics, and Escalate has no real reviewer.
3. The Detection Layer lacks its classifier (x^ctx₁).
4. The identifier "B1" means the consequence-independent baseline in the thesis, but MELON in the supervisors' experiment design. In this validation package the configurations are named in full (No Defense, MELON, REM-Lite, Full REM) to avoid confusion.

## 6. Blockers and required changes before a live comparison

- LLM access and a spending decision.
- Network access to `api.openai.com` (MELON's detector always needs OpenAI embeddings).
- The open design inputs (D-15; M-1 to M-3).
- MELON needs AgentDojo 0.1.29, so a matched four-way live run must use that version for all configurations. REM's live harness is version-aware for this purpose (`rem/integration/melon_rem.py`).
