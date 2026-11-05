# Final Validation Report — REM Experimental Validation (5 Nov 2026)

## 1. What was done

| Phase | Outcome |
|---|---|
| 1 Audit | `01_AUDIT/`: current state, data leakage, readiness. Discrepancies recorded (no x^ctx₁ classifier; "Platt" = label-NLL logit calibration; Modify ≡ Block in immediate effect under step-level semantics; no real reviewer) |
| 2 MELON preparation | The official code from both repositories was inspected (identical implementation file, no licence). It runs unmodified on AgentDojo 0.1.29 in a separate environment. Integration verified with 30 local checks. **Live execution blocked** |
| 3 REM integration | REM intercepts calls before execution in the replay, live and MELON harnesses, and as a deployed HTTP gateway (0 parity mismatches; withheld calls never reach the bank) |
| 4 Ablation | **REM-Lite implemented** (uncalibrated p̃ + development-data operating-point thresholds); separate configuration files |
| 5 Smoke tests | Scripted-agent and fake-provider tests; not reported as results |
| 6 Final benchmark | **Mode A executed** for No Defense, REM-Lite and Full REM. **MELON and every Mode B (live) run: not executed** |
| 7 Analysis | `04_RESULTS/` (tables R1–R5; two figures; experiment report) |
| 8 Thesis | Update drafts in `05_THESIS_UPDATES/`. They are to be merged when the restructured Chapter 4 ("Real-World Deployment and Evaluation") is written. The thesis files themselves are unchanged in this step |

## 2. Main verified findings (Mode A, exploratory)

| Configuration | ASR | Benign utility | Defence time per call (median) |
|---|---:|---:|---:|
| No Defense | 0.226 | 0.524 | — |
| REM-Lite | 0.055 | 0.509 | 0.17 ms |
| Full REM | 0.004 | 0.314 | 0.18 ms |
| MELON | Not executed | Not executed | Not executed |

- **REM-Lite ≡ the thesis's B1**, verdict for verdict, so calibration does not drive the difference.
- **Full REM against REM-Lite:**
  - lower attack success: ΔASR −0.051 [−0.130, −0.007]; 153 vs 0 discordant episodes;
  - lower utility: Δ benign utility −0.195 [−0.341, −0.074].
- **Calibration:** no improvement (ECE 0.0438 calibrated against 0.0415 uncalibrated).
- **Deployment:** REM adds no LLM call. As a separate service it changed no decision.

## 3. Contribution validation (Part 12)

**Proposed contribution:** a non-invasive runtime security framework combining calibrated probabilistic risk estimation with cost-sensitive mitigation decisions for financial AI agents.

| Type | Status |
|---|---|
| Design contribution | **Yes.** Specified architecture (five layers), equations and decision rule (Chapter 3) |
| Implementation contribution | **Yes.** Tested code; evaluation path, live harness, MELON adapter and deployable gateway |
| Experimentally supported contribution | **Partly, exploratory, Mode A only** (table below) |

| Claim | Supported? |
|---|---|
| Security effectiveness | Only under NO-ADAPT replay of recorded agents; **not** for live or adaptive agents |
| Financial task utility | Measured; Full REM costs about 20 points of benign utility without a reviewer |
| Calibration | Measured: well calibrated (ECE 0.044), but **no benefit over uncalibrated** probabilities |
| Cost-sensitive decision quality | Lower realized loss under the declared costs. The costs are a declared preference, not validated financial loss; cost sensitivity in thesis §4.9 |
| Explainability | The linear attribution is computed per call and is audit-only (additivity tested). Its usefulness to humans was **not evaluated** |
| Runtime performance | Sub-millisecond decisions and no added model calls (prototype, one machine) |
| Applicability to financial workflows | Only to AgentDojo's simulated banking environment; no production banking |
| Comparison with MELON / FinHarness | **Not supported.** MELON not executed; FinHarness has no code |

**Novelty:**
- None of logistic regression, logistic/Platt calibration, Bayes expected-loss decisions or SHAP is new.
- The contribution is the integrated architecture, its implementation and its exploratory evaluation.
- It overlaps with FinHarness (financial domain, inline per-step monitoring, graded responses) and with MELON (runtime placement); see `02_RESEARCH_COMPARISON/`.

## 4. What remains to complete the supervisors' design

1. **Model access:** an API credential, and `api.openai.com` allowed in the environment's network settings (needed by MELON in every case).
2. **Spending:** an explicit authorisation and cap.
3. **Design inputs:** backbone, decoding, repeats and fold source (D-15, M-1 to M-3).
4. **REM-Lite in Mode B:** add it as a policy option to the live and MELON runners (small change).
5. **The run itself:** a matched four-way live run on AgentDojo 0.1.29; pilot first, then the full set.

## 5. Integrity checklist (Part 14)

| Rule | Status |
|---|---|
| No fabricated results or references | ✔ Every number comes from committed result files via scripts |
| No invented FinHarness code; no altered MELON presented as official | ✔ |
| Replay not called live; simulated bank not called production | ✔ |
| No tuning on test data | ✔ REM-Lite thresholds use development data only |
| No superiority claim without evidence | ✔ |
| Failed or superseded runs kept | ✔ Superseded deployment run kept with explanation |
| Historical results not overwritten | ✔ |
| REM-Lite not presented as calibration's isolated effect | ✔ Shown to isolate the decision rule |
| The four mitigation actions not presented as validated | ✔ Modify ≡ Block in immediate effect; no real reviewer |
