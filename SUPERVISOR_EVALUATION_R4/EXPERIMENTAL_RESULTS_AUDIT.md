# Experimental Results Audit

**Scope:** Chapter 5 (R4) and the result sets that feed it:
- `results/pilot_R2/` (analytical values);
- `results/pilot_R4/` (complete-call timing; full re-execution from `ea621c3`);
- the scripts in `experiments/pilot/`.

**Checks performed on 1 Nov 2026:**
- reading of the result files;
- an independent NumPy recomputation of AUC, ECE and log-loss from the R4 re-execution state, `repro_R4c/state/crossfit.pkl` and `data.steps`. That state is in the session scratchpad, not in the repository; to repeat the check, re-run `experiments/pilot/run_all.sh` with `PILOT_RESULTS_DIR` set;
- an examiner diagnostic with a simple provenance rule. It is observe-only and is *not* part of the thesis.

## 1. Provenance of each kind of evidence

| Kind of evidence | Present | Source | Real / simulated | Assessment |
|---|---|---|---|---|
| Live enforcing runs (REM protecting a running LLM agent) | **None** | `experiments/live/LIVE_EVALUATION_PROTOCOL.md` (NOT EXECUTED) | — | The central practical claim has no direct evidence (C-1) |
| Recorded benchmark outcomes | Yes | AgentDojo `runs/` at commit `089ed468`; 21 backbones; `important_instructions` attack | Real agent behaviour, recorded by third parties | Valid input data. One run per (backbone, task pair); not independent rows |
| Held-out predictions (RQ1) | Yes | `e1_crossfit.json` | Recomputed from real traces with nested grouped cross-fitting | **Reproduced by the evaluator:** AUC 0.938288, ECE 0.043761, log-loss 0.201344 |
| Observe-only verdicts (RQ2, RQ4) | Yes | `e2_e5_e6_observe_only.json`, `r2_breakdowns.json` | Computed, not enforced | Valid as decision analysis; shows nothing about effects |
| Replay under NO-ADAPT (RQ3) | Yes | `e4_e5_enforcement_replay.json` | Simulated counterfactual: the agent repeats its recorded calls regardless of refusals | Sensitivity analysis only; outside the approved methodology (D-1) |
| Uncontrolled distributed defences | Yes | `e4_cross_template_and_defenses.json` | Recorded by AgentDojo authors (gpt-4o only) | Not comparable; correctly not used as a comparison |
| Latency / memory | Yes | `results/pilot_R4/` | Measured on a 4-vCPU Xeon | Real but tiny (sub-millisecond); excludes any classifier |
| Label audit | AI-only inspection of 30 episodes; human package of 145 items with **0 annotations** | `label_audit_*` | — | Labels unvalidated (C-3) |

**Reproducibility.**
- Two full re-executions gave 0 analytical differences in 6,057 shared values (`reproduction_all_differences_R4.json`).
- The headline metrics were reproduced by the evaluator with independent code.
- The results are therefore **reproducible as computations**. Whether they are **valid as evidence of protection** is a separate question, assessed below.

## 2. Key results and what they show

| RQ | Main result (Ch. 5) | What it supports | What it does not support |
|---|---|---|---|
| RQ1 | Pooled ROC-AUC 0.938 [0.908, 0.961]; AP 0.719; ECE 0.044 (uncalibrated 0.042); fold 7 (credential change) ECE 0.189; leave-one-backbone-out AUC 0.736–1.000 | Argument-provenance features separate the reference-labelled attack calls well in this benchmark | Calibration benefit (none measured); generalisation to unseen attack categories (fold 7 fails); label correctness |
| RQ2 | Observe-only: REM intervenes on 97.3% of y = 1 and 22.7% of y = 0 steps; B1 74.0% / 5.6%. REM intervenes on **93.2% of legitimate tier-3 transfers ≤ 1000**; releases 33 of 180 benign state-changing steps (B1: 132) | Lower tier-4 thresholds make REM intervene far more often | That the trade-off is favourable: no cost elicitation and no utility valuation |
| RQ3 | Replay, step-level: ASR B0 0.226, B1 0.055, REM 0.004. Benign utility without reviewer: REM 0.314 vs B1 0.509 (Δ −0.195 [−0.341, −0.074]). State-changing benign utility REM 0.168 vs B0 0.472 | Under NO-ADAPT, withholding more calls prevents more recorded attack effects | Protection for live or adaptive agents. ASR ≈ 0 and r_mod ≈ 0 are consequences of NO-ADAPT (stated) |
| RQ4 | Only action evidence matters (AUC 0.938 → 0.799 without it); context indicator: no effect; behavioural features hurt utility; calibration: no effect; predicates: no effect | The effective mechanism is argument provenance plus tier-scaled thresholds | Any value added by the other three layers |
| Latency | Complete-call median 0.21–0.28 ms; p95 0.49–0.70 ms; 4.4 KB per step | The decision computation is cheap | Overhead with an injection classifier, which is absent |
| CUSUM | Observe-only; benign false-alarm rate 0.106 against a 0.05 target | Not part of the verdict | — |

## 3. Examiner diagnostic: a missing simple baseline

The rules below have no fitted parameters, so no cross-fitting is needed. They were applied to all 6,762 steps, observe-only.

| Rule | y = 1 steps intervened | y = 0 steps intervened | Benign state-changing steps released |
|---|---:|---:|---:|
| Intervene on tier ≥ 2 call iff x_act1 = 1 | 0.971 | 0.147 | 92/180 |
| … iff x_act1 ∨ x_act2 | 0.971 | 0.153 | 89/180 |
| … iff x_act1 ∨ x_act2 ∨ x_act3 | 0.974 | 0.153 | 89/180 |
| REM (thesis, observe-only) | 0.973 | 0.227 | 33/180 |
| B1 (thesis, observe-only) | 0.740 | 0.056 | 132/180 |

**Interpretation.**
- In this benchmark, a one-line provenance rule matches REM's attack interception.
- It intervenes on fewer legitimate steps, and it releases 2.8 times more benign state-changing steps.
- The value added by the estimator, calibration and expected-loss layers is therefore **not demonstrated** (C-2).

**Caveats.**
- This is observe-only and was not replayed.
- It reflects a benchmark in which the attacker's destination appears only in injected content.
- It is an examiner check, not a thesis result, and must not be reported as one.

## 4. Validity threats

| Threat | Status | Effect |
|---|---|---|
| Label validity (proxy labels; the user_task_15 collision affects 16/21 backbones; no human audit) | Open | Every metric depends on it. All of REM's residual ASR comes from ambiguous UT15 episodes |
| Non-independence (16 user × 9 injection templates; one attacker account; one run) | Disclosed | The intervals rest on 9 groups. Percentile-bootstrap coverage is uncertain |
| Concentration (ASR differences driven by two single-task categories: credential change and payment modification) | Disclosed | The REM vs B1 difference rests on n = 1 injection task per category |
| Design values (costs, tiers) not elicited or approved | Disclosed | The decision results are conditional on arbitrary values |
| Structural benchmark artefact (attacker IBAN only in injected content) | Partly disclosed (Ch. 6 Table 6.1) | x_act1 is nearly an oracle; external validity is low |
| NO-ADAPT replay | Disclosed | Overstates protection against adaptive agents |
| Circular r_mod; Modify ≡ Block in step-level replay | **Not stated as such** | RQ3's Modify results are uninformative |
| Pre-registration (first execution log not preserved) | Disclosed | The ordering of amendments relative to the results cannot be fully evidenced |
| Multiple comparisons | Not corrected | Inflates the apparent strength of the many paired contrasts |
| Repeated runs (AS-9, §3.11.9) | Unmet | LLM non-determinism is not measured |

## 5. Are the results sufficient for a master's thesis?

**No, not in their current form, for the claims the thesis makes.**

They are sufficient for a *well-reported exploratory pilot* that characterises how a cost-tiered policy behaves on recorded traces. They are not sufficient to show:
- that REM improves security over simple or published alternatives;
- that the components (calibration, behavioural features, expected loss) contribute;
- that the costs reflect any real financial setting.

## 6. Minimum additional evidence required

Listed in order of necessity:

1. **Simple baselines in replay:** the provenance rule (x_act1; x_act1 ∨ x_act2), and B2 detection-only. This is cheap, uses the existing harness, and directly addresses C-2.
2. **Human label audit:** at least the 145-item package, with a second annotator and κ reported. This addresses C-3.
3. **Approved or elicited design values.** Costs and tiers from the supervisor or a domain source, plus a sensitivity sweep reported as the primary analysis rather than as a single point.
4. **Live enforcing runs** on at least one open-weight backbone with ≥ 3 repeats, using the existing protocol in `experiments/live/`. This addresses C-1, AS-9 and §3.11.9.
5. **At least one controlled comparison with a published defence** on the same backbone and tasks (for example, a tool filter or a PI detector). This addresses O3.
6. **A second environment or attack family:** another AgentDojo attack, or an adaptive attack that paraphrases or splits destinations so that x_act1 is not guaranteed to fire. This bounds the benchmark artefact.
7. **A cost-independent decision-quality metric:** regret against an oracle policy, or a utility–ASR frontier across the cost grid.

If items 4 and 5 cannot be done (D-15: no LLM access), the thesis must be **re-scoped** to an offline decision-analysis study and its title and claims reduced accordingly.
