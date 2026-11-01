# Research-Question Traceability Matrix

**Basis:**
- RQs as worded in Ch. 1 §1.7 (R4). All are marked [PD], and the Ch. 3 §3.1.3 wording differs slightly (m-8).
- Objectives O1–O3 from Ch. 1 §1.5. They are quoted from an approved proposal that is not in the repository.
- Code and results at commit `9ab3f9e`.

**Status codes:**
- **SUPPORTED**: the evidence answers the question as worded.
- **PARTIAL**: it answers a narrower version.
- **UNSUPPORTED**: there is no adequate evidence.

## 1. Research questions

| RQ | Literature gap | Proposed method | Code evidence | Experimental evidence | Conclusion (Ch. 5/6; paraphrased, not quoted) | Status |
|---|---|---|---|---|---|---|
| **RQ1:** How well does ridge LR on context, behavioural and action evidence discriminate adversarially induced actions, and how well calibrated is it under grouped cross-fitting? | Gap A (weak); Ch. 2 §2.8 on calibration | Eqs. 3.1–3.4; nested grouped cross-fitting (Proc. 3.1); Eqs. 3.20–3.21 | `ridge_logistic.py`, `logit_nll.py`, `crossfit.py`, `evidence.py`; tests pass; no leakage found | `e1_crossfit.json`: AUC 0.938 [0.908, 0.961], ECE 0.044, fold 7 ECE 0.189, LOBO 0.736–1.000. **Recomputed independently: match** | Table 6.1 rows 2–3 (paraphrase): boundary evidence separates attack attempts on unseen objectives, templates and backbones; action evidence carries most of it. Limits stated: one benchmark, proxy labels | **PARTIAL.** Answered for proxy labels in one benchmark. Labels not audited (C-3). x_ctx1 absent, so "context evidence" is untested. x_act1 is nearly an oracle here (M-6) |
| **RQ2:** Against a consequence-independent threshold policy with the same estimator, how does tiered expected-loss selection change intervention, ASR and utility across a declared range of loss structures? | Gap E (narrow, most defensible) | Eqs. 3.5–3.10 vs Eq. 3.14 (B1); E6 cost grid | `a3.py`, `expected_loss.py`, `loss_matrix.py`, `a1.py`; tests pass | Observe-only: REM 97.3% / 22.7% vs B1 74.0% / 5.6%; 93.2% intervention on legitimate tier-3 transfers. Replay: ASR 0.004 vs 0.055; benign utility 0.314 vs 0.509. Cost grid in `e6_grid` | Table 6.1 rows 4–5 (paraphrase): with the pre-registered costs, REM intervenes on far more legitimate state-changing actions than B1, and within the replay assumption withholds more attacks (ΔASR −0.051 [−0.130, −0.007]) at a utility cost | **PARTIAL.** Answered descriptively for unapproved costs. "A declared range" is a small exploratory grid, not elicited. REM and B1 differ in both thresholds and escalation. **No simple provenance-rule baseline**, and that rule matches REM (C-2) |
| **RQ3:** Residual ASR after Modify, escalation frequency, per-step processing time | Gap D (semantic); Gap C | Eq. 3.5 (r_mod); §3.10 mitigation; §3.11.11 replay | `agentdojo_replay.py` (`RemGuard`); `runtime.py`; the timer is tested | r_mod 0.000 / 0.010; Modify chosen for 615/907 attack steps; escalation rates per configuration; latency median 0.21–0.28 ms, p95 0.49–0.70 ms | Ch. 5 §5.6 and Ch. 6 (paraphrase): residual ASR and r_mod near zero are consequences of the NO-ADAPT assumption; per-step processing time is sub-millisecond | **PARTIAL to UNSUPPORTED.** Residual ASR and r_mod are **circular**: Modify is a withheld call under NO-ADAPT (M-2, CI-1). Escalation frequency: answered. Latency: answered, but without a classifier. Live residual success: not measured (stated) |
| **RQ4:** Marginal contribution of each evidence group, of calibration and of tiers, by ablation | — | Ablation design, §3.11.8 | Ablation configuration in `pilot_e0.yaml`; `run_main.py` | Table 5.12: action evidence decisive (AUC 0.938 → 0.799); context, behaviour, calibration and predicates show no gain; behaviour costs 10.5 points of utility; tiers move the trade-off | Table 6.1 row 3 (paraphrase): action evidence carries most of the separation | **SUPPORTED** (as an exploratory ablation). The answer is largely negative for the design. That is a valid finding, but it undercuts the framework claim |

## 2. Objectives

| Objective | Method / evidence | Thesis's self-assessment (Ch. 6 Table 6.2) | Examiner status |
|---|---|---|---|
| O1: Design a REM framework for financial **and task-automation** agents | Ch. 3 design; Ch. 4 implementation | Achieved for the banking setting | **PARTIAL.** Designed and implemented, but evaluated for banking only. x_ctx1 and the reviewer are absent. The frozen pipeline is not the evaluated path |
| O2: Evaluate the framework against adversarial attacks | Ch. 5: one attack family (`important_instructions`), recorded traces, replay | Partly achieved | **PARTIAL.** No live, adaptive or second attack family |
| O3: Compare performance with existing security approaches | B1 (internal); distributed defences (uncontrolled) | Partly achieved | **NOT ACHIEVED.** B1 is an internal same-estimator baseline, not an existing approach. No published defence was run under controlled conditions. B2 was not run |

## 3. Cross-chapter consistency defects affecting traceability

| Defect | Chapters | Effect |
|---|---|---|
| Ch. 3 §3.11.11 (line 821): replay "cannot distinguish step-level from episode-level semantics". This is contradicted by Ch. 3 §3.8 and Ch. 5 Table 5.11 | 3 ↔ 5 | Misstates what RQ3's evidence can show (M-3) |
| Ch. 5 §5.6 points to "Table 5.12" for the semantics comparison; the correct table is 5.11 | 5 | Broken trace (m-1) |
| AS-9 / §3.11.9 promise repeated runs; only one run exists | 3 ↔ 5 | RQ1–RQ3 variance is not measured (M-7) |
| §3.12.1 defines ASR "(enforcing mode)", but only replay ASR exists | 3 ↔ 5 | The definition does not match the evidence (m-6) |
| §3.12.2 withholds the Brier score; Table 5.3 reports it | 3 ↔ 5 | m-6 / SC-5 |
| RQ2 and RQ3 wording differs between §1.7 and §3.1.3 | 1 ↔ 3 | m-8 |
| The objectives cite an approved proposal that is absent | 1, 3 | The objectives cannot be verified (C-5) |

## 4. Summary

| | SUPPORTED | PARTIAL | UNSUPPORTED / NOT ACHIEVED |
|---|---:|---:|---:|
| RQs (4) | 1 (RQ4) | 2 (RQ1, RQ2) + RQ3 partial to unsupported | — |
| Objectives (3) | 0 | 2 (O1, O2) | 1 (O3) |

The chain from RQ to conclusion is **traceable**: every number traces to a file, and 126 printed cells were checked by script. It is, however, **thin in evidential strength**. No RQ is answered beyond an exploratory, replay-or-offline, proxy-label level.
