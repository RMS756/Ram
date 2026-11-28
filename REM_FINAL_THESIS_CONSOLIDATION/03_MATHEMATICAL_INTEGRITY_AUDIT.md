# 03: Mathematical and statistical integrity audit (28 November 2026)

## 1. Confirmation

**Nothing was changed:**
- no equation, model, estimator, coefficient, threshold, grid, tie rule or calibration target was created, changed or chosen in this task;
- the REM code was not modified: `rem/` tree `cd11e32…` at HEAD, unchanged since `7c79883`;
- the working copy changes no equation of Chapter 3 and no number of Chapter 4 (498 table cells re-verified, 0 mismatches; 09 §1).

**Sources examined for every item below:**
- thesis text: humanized edition, Chapter 3;
- code: `rem/algorithms/detection/ridge_logistic.py`, `calibration/platt.py`, `calibration/logit_nll.py`, `decision/expected_loss.py`, `a1.py`, `a3.py`;
- protocol: `configs/exploratory/pilot_e0.yaml`, sha256 `8e1aa107…`;
- runner: `experiments/pilot/run_main.py`;
- stored results: `results/pilot*`, `results/rem_lite`;
- `EQUATION_PROVENANCE_AUDIT.md`.

## 2. The six open items

| Issue | Thesis location | Existing implementation | Original source | Verification | Kind | Can existing evidence resolve it? | Required action | Supervisor approval required? |
|---|---|---|---|---|---|---|---|---|
| **M1** Regularisation factor | Ch. 3 Eq. 3.2 (maximize LL − λ‖β‖²). Ch. 3 §3.7.1, paragraph "Reference parameterization of λ". Ch. 4 Table 4.4 and the fold tables, which report λ on both scales | `ridge_logistic.py` minimizes NLL + (λ_impl/2)‖β‖², gradient g = Xᵀ(p − y) + λb; intercept unpenalized. Grid λ_impl ∈ {0.01, 0.1, 1, 10, 100} (`pilot_e0.yaml`, `estimation.lambda_grid`) | le Cessie & van Houwelingen (1992), record verified. Its scaling constant was **not checked** against the full text | The text and the code are **consistent**. Chapter 3 states λ = λ_impl/2, converts the grid to {0.005, 0.05, 0.5, 5, 50}, and reports every selected value on both scales. Equivalence holds because the grid is converted, not assumed | Documentation (already resolved in the text) | **Yes.** The humanized Chapter 3 already resolves the 27 Oct audit's M1; that audit predates the paragraph | None in the thesis. Optional: verify the le Cessie scaling against the full text [SOURCE VERIFICATION INCOMPLETE]; it does not affect the method | **Acknowledgement only:** the supervisor should confirm Eq. 3.2's scale as the reference (it is the only scale the thesis reports as primary) |
| **SC-2** Tie rule | Ch. 3 Eq. 3.7: ties resolved toward Block ⪰ Escalate ⪰ Modify ⪰ Allow; "Ties are counted and reported". §3.7.5: at equality in Eq. 3.10, ties resolve toward Block. Table 3.9 lists the "tie-breaking order" as a declared policy quantity | **Two paths.** (a) The frozen core `ExpectedLossDecisionEngine.argmin_verdict` raises `VerdictTieError`: no rule frozen. (b) The evaluated policy `A3Policy` is built in `run_main.py` with `tie_mode="record_chapter3_order"`: it applies Chapter 3's order and records ties. `pilot_e0.yaml`: `tie_breaking: count_and_report` | Elkan (2001) for the argmin. The tie order is a design definition (no source) | The evaluated configuration **implements Chapter 3's order**. **Every stored run that counts ties records 0:** 217 tie counts in `results/pilot`, `pilot_R2`, `pilot_R4` and `rem_lite`. The ablation runs of 19–21 November store no tie count and were not checked | Design decision (not frozen) and implementation (the frozen module differs from the evaluated policy) | **Partly.** No result that counts ties depends on the tie rule (0 ties). Whether the order is the adopted rule cannot be settled by evidence | Keep the text. If the supervisor adopts the order, the frozen module's behaviour should be aligned in a **new, approved** code version; REM v1.0 stays unchanged. If not adopted, add one sentence to Ch. 3: "No exact tie occurred in any run in which ties were counted." | **SUPERVISOR DECISION REQUIRED**: adopt the Chapter 3 order as the frozen rule, or keep "raise" |
| **SC-4** Calibration targets | Ch. 3 Eq. 3.4 (NLL on labels) and the paragraph "Fitting target": Eq. 3.4 is the reference, and Platt's smoothed targets t₊ = (N₊+1)/(N₊+2), t₋ = 1/(N₋+2) form a sensitivity analysis | `LabelNLLLogitCalibrator` (primary) and `PlattLogitCalibrator` (smoothed targets; secondary). `pilot_e0.yaml`: `calibration_primary: nll_on_labels_out_of_fold`, `calibration_secondary: platt_smoothed_targets`. `run_main.py` runs both | Guo et al. (2017) for fitting by NLL; Platt (2000) for smoothed targets | The text, configuration and runner are **consistent**. The pilot difference is negligible: ECE 0.0438 vs 0.0436 (`EQUATION_PROVENANCE_AUDIT.md`). The 27 Oct remark "neither adopted" is out of date: the thesis declares Eq. 3.4 the reference | Methodological choice (documented) | **Yes** for consistency. The attribution of the smoothed-target formula to Platt is not checked against the full text | None in the thesis. Verify the target formula in Platt's chapter [SOURCE VERIFICATION INCOMPLETE] | **YES (approval of a declared choice):** Eq. 3.4 as the reference target is the author's declaration; CLAUDE.md fixes only the Platt form on the logit |
| **Platt citation** | Ch. 3 §3.7.2 "Status": "The method is Platt scaling (Platt, 2000)". Reference entry Platt (2000) with a note on the title | — | Crossref: J. C. Platt, "Probabilities for SV Machines", *Advances in Large-Margin Classifiers*, MIT Press, 2000, pp. 61–74, DOI 10.7551/mitpress/1113.003.0008 (re-checked 28 Nov 2026) | **Record verified.** The entry's long title ("Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods") differs from the Crossref title; the entry already says so. No 1999 record exists in Crossref | Documentation (citation) | **Partly.** Record yes; printed title and content no | Keep the entry with its note, or adopt the Crossref title. Check the printed chapter for the logistic form and the smoothed targets [SOURCE VERIFICATION INCOMPLETE] | YES (citation form): which title to print |
| **Kull citation** | Ch. 3 §3.7.2: "monotonicity condition follows Kull et al. (2017), who require a non-negative slope for a non-decreasing map"; property 2: "Kull et al. (2017) **prove** that beta calibration with equal shape parameters equals logistic calibration applied to the log-odds of a score" | `platt.py` rejects γ₁ ≤ 0 (`MonotonicityViolationError`); pilot γ₁ ∈ [0.945, 0.981] | The entry names the **AISTATS 2017** paper (PMLR 54, 623–631). OpenAlex W2725875209 confirms the record; the *EJS* 2017 paper (DOI 10.1214/17-EJS1338SI) is a different work | **Ambiguity resolved at record level:** the thesis cites the AISTATS paper. Whether that paper (i) states the non-negativity condition and (ii) presents the equal-shape-parameter identity as a proof (not only a remark) is **not verified**. The abstract mentions neither | Documentation (attribution) | **No.** Needs the full text (PMLR PDF, open access) | Read the PMLR paper. If the identity is stated but not proved, change "prove" to "show". If either statement is in the *EJS* paper only, cite that. **Not changed in the working copy**, because the correct wording cannot be decided without the text | YES, after the source check |
| **α grid** | Ch. 3 §3.7.7: α_mod > α_blk is required. Ch. 4 Table 4.4: α_blk = 0.01, α_mod = 0.05. Ch. 4 §4.6 (sensitivity): "The grid cell α_blk = 0.05 is not evaluable" | `pilot_e0.yaml`: `baseline_B1` α_blk 0.01, α_mod 0.05; `grid.alpha_blk` [0.005, 0.01, 0.05]. `a1.py` `operating_threshold` | Definition (Eq. 3.14); no source | The inconsistency is **real and already reported** in the thesis: one cell of a declared grid violates a constraint of the same chapter. The baseline's operating point (0.01, 0.05) satisfies the constraint; only one sensitivity cell is lost | Methodological (grid design) | **No.** A replacement grid would be a new design value | Keep the statement. Do **not** invent a replacement grid or value | **SUPERVISOR DECISION REQUIRED**: accept the lost cell, or declare a corrected grid for a future, protocol-frozen rerun |

## 3. Equations 3.1–3.22: traceability

Unchanged from `REM_LAYERED_FRAMEWORK_DESIGN_REVIEW/06` §2, which was checked against the current code. The status column is updated with today's findings.

| Eq. | Content | Source (status) | Code | Status |
|---|---|---|---|---|
| 3.1 | s = β₀ + βᵀx; p̃ = σ(s) | Cox (1958), verified | `ridge_logistic.py` | Consistent |
| 3.2 | Ridge-penalized log-likelihood | le Cessie & van Houwelingen (1992), verified | `fit` | **M1 documented in Ch. 3**; consistent |
| 3.3 | p = σ(γ₁s + γ₀), γ₁ > 0 | Platt (2000) record verified; Guo et al. (2017); Kull et al. (2017, AISTATS) record verified | `platt.py`, `logit_nll.py` | Consistent; **Kull wording** unverified |
| 3.4 | Calibration by NLL on labels | Guo et al. (2017) | `logit_nll.py` | **SC-4 documented**; approval of the declared reference pending |
| 3.5 | L(Modify,1,k) = r_mod(k)·C_miss(k) | Derived | `loss_matrix.py` | Assumption: r_mod from NO-ADAPT replay |
| 3.6 | R(v) = (1−p)L(v,0,k) + pL(v,1,k) | Elkan (2001) | `conditional_risk` | Consistent; costs declared, not approved |
| 3.7 | argmin over the feasible set; tie order | Elkan (2001); order a definition | `A3Policy` (evaluated); frozen module raises | **SC-2**; 0 ties wherever ties were counted |
| 3.8–3.10 | Indifference thresholds; escalation feasibility | Derived; Chow (1970) conceptual only | `loss_matrix.py` | Consistent |
| 3.11–3.12 | Linear attribution, additivity | Lundberg & Lee (2017) | audit only (tested) | Consistent; never in the verdict |
| 3.13 | Feature-group sums | Definition | reporting | Consistent |
| 3.14 | θ(α) operating threshold, baseline only | Definition | `a1.py` | **α-grid cell** not evaluable (reported) |
| 3.15–3.19 | Bernoulli CUSUM (observe-only) | Page (1954); Basseville & Nikiforov (1993); Reynolds & Stoumbos (1999) | observe-only (tested) | Held-out false-alarm rate 0.106 against a 0.05 target (reported in Ch. 4) |
| 3.20 | ECE, equal-width bins | Naeini et al. (2015); Guo et al. (2017) | metric | Consistent |
| 3.21 | Clipped log-loss | Derived | metric | Consistent |
| 3.22 | Mean realized loss | Definition | metric | Matched-cost evaluation favours REM by construction (stated) |

**Statistical methods in Chapter 4 and the merged DiD sections:**

| Method | Source | Status |
|---|---|---|
| Grouped bootstrap | Field & Welsh (2007) | Re-verified on Crossref |
| Exact McNemar | Unclustered | As stated in Ch. 4 |
| Clustered sign-flip permutation, with Holm correction (DiD Sections 3.15 and 4.6.12) | Holm (1979) | **Not cited** in the DiD text and **not found in Crossref**. [SOURCE VERIFICATION INCOMPLETE]. A citation should be added once the JSTOR record is checked (08, D9) |
| Jaccard index | Jaccard (1912) | Verified earlier |

## 4. Mathematics of the reviewed frameworks

**None is adopted.**
- NEXUS's Platt-calibrated risk score;
- the Multilayer DiD drift score;
- MELON's embedding similarity;
- CASCADE's thresholds;
- Saleem et al.'s semantic drift detector.

These appear in the thesis text only as descriptions of what those authors report, never as equations.

## 5. Result

- **Resolved by existing evidence (documentation already consistent):** M1 and SC-4, as consistency between text, code and protocol.
- **Shown to have no effect on any result that counts ties:** SC-2 (0 ties in 217 counts; the later ablation runs do not count ties).
- **Open:**
  - SC-2 adoption (supervisor);
  - SC-4 approval (supervisor);
  - the Platt title and content check;
  - the Kull wording ("prove"; source check);
  - the α grid (supervisor);
  - the Holm citation (source check).
- **No mathematical error** was found.
