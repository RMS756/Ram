# Equation Verification Report (R3, 30 October 2026)

**Scope:**
- the 22 numbered equations of Chapter 3 (Eqs. 3.1–3.22);
- the three equations Chapter 2 reproduces from sources (Eqs. 2.1–2.3), which restate Eqs. 3.1, 3.3 and the expected-cost rule of Eq. 3.6;
- the derived quantities quoted in Chapters 5 and 6.

**Three kinds of verification, reported separately:**

| Kind | Meaning | Evidence |
|---|---|---|
| **M: mathematical** | The derivation or identity is correct, checked symbolically or numerically | `verification/verify_equations.py`, run 30 Oct 2026: **22 checks, all PASS** (`verify_equations_output.txt`) |
| **I: implementation** | The code computes the printed formula, and a test executes it | `EQUATION_PROVENANCE_AUDIT.md` (27 Oct) and the test run of 30 Oct (193 passed); for Eqs. 3.14, 3.20 and 3.21, also a direct comparison of the code with a transcription of the formula in `verify_equations.py` |
| **S: source** | The cited source states what is attributed to it | Chapter 3 Table 3.17 codes: FV = checked against the source; IV = identity only; NC = not accessed; DER = derived; DEF = definition. Metadata re-checked 27–30 Oct. **No full text was read in any 27–30 October session, so no S code was upgraded** |

No equation identifiers (EQUATION_ID) were created. The authoritative registry is missing (RG-1), and `CLAUDE.md` § EQUATION-ID LOCK forbids provisional identifiers. Equation numbers are document references only.

## 1. Equation-by-equation result

| Eq. | Content | M (30 Oct) | I | S (Table 3.17) | Notation and dimensions | Open issue |
|---|---|---|---|---|---|---|
| 3.1 | s_t = β₀ + βᵀx_t; p̃_t = σ(s_t) | Definition | Yes | IV — **SOURCE NOT FULLY VERIFIED** (Cox 1958; OI-12) | x_t ∈ [0,1]^d, β ∈ ℝ^d, so s_t ∈ ℝ and p̃_t ∈ (0,1) | — |
| 3.2 | Ridge-penalized log-likelihood | Scale correspondence λ = λ_impl/2: PASS | Yes | IV, penalty constant pending — **SOURCE NOT FULLY VERIFIED** (OI-10, M1) | Penalty on β only, consistent with "intercept not penalized" | Reported on both scales in Ch. 4–5 |
| 3.3 | p_t = σ(γ₁s_t + γ₀), γ₁ > 0 | dp/ds = γ₁p(1−p) > 0: PASS; Kull equal-shape beta = logistic on log-odds: PASS | Yes; γ₁ ≤ 0 rejected | Platt NC (citation conflict OI-07); Guo FV; Kull FV with disambiguation pending — **SOURCE NOT FULLY VERIFIED** | Scalar; monotone in s_t | D-13 (Platt, Kull) |
| 3.4 | Calibration fit by NLL on labels | Definition | Yes (`LabelNLLLogitCalibrator`) | FV (Guo 2017) | — | SC-4: the frozen calibrator uses Platt targets; both are reported (Table 5.3) |
| 3.5 | L(Modify,1,k) = r_mod(k)·C_miss(k) | PASS (total expectation under A-Mod) | Yes | DER | r_mod ∈ [0,1]; same units as C_miss | r_mod measured only under NO-ADAPT replay |
| 3.6 | R_t(v) = (1−p_t)L(v,0,k_t) + p_tL(v,1,k_t) | Affine in p: PASS | Yes | FV (Elkan, Eq. 1 form) | Costs in common relative units | — |
| 3.7 | v_t = argmin over 𝒱(a_t); tie order | — | Yes (feasible set; `tie_mode`) | FV; tie order DEF | — | SC-2 / D-4 (no ties occurred in the pilot) |
| 3.8 | π_{v,v′} = Δ₀/(Δ₀+Δ₁) | PASS (solve and sign rule) | Yes | DER | Dimensionless | — |
| 3.9 | p*_k = C_FA/(C_FA + C_miss) | PASS; 1/11 and 1/21 for the pilot costs: PASS | Yes | DER — **SOURCE NOT FULLY VERIFIED** for the Elkan correspondence (OI-11) | Dimensionless | — |
| 3.10 | C_esc < C_FA·C_miss/(C_FA + C_miss) | Peak of min(R_A, R_B): PASS; iff on 2,000 random structures: PASS; symmetric case C/2: PASS | Yes | DER; Chow conceptual — **SOURCE NOT FULLY VERIFIED** (OI-13) | Cost units | — |
| §3.7.5 | R(Mod) − R(Block) = (1−p)(C_mod − C_FA) + p·r·C_miss | PASS | Yes (`reachable_verdicts`) | DER | — | — |
| 3.11 | φ_{t,i} = β_i(x_{t,i} − x̄_i); φ₀ = β₀ + βᵀx̄ | Definition | Yes | FV (Lundberg & Lee) | Logit units | Audit-only |
| 3.12 | φ₀ + Σφ = s_t | PASS (symbolic, d = 5) | Yes; additivity error logged per replayed step | FV + DER | — | — |
| 3.13 | Group sums | Definition | Yes | DEF | — | — |
| 3.14 | θ(α) = min{θ : FPR_val(θ) ≤ α} | Code against formula (α = 0.01, 0.05, 0.2): PASS | Yes | DEF | — | D-14: α grid cell 0.05 not evaluable |
| 3.15 | Bernoulli log-likelihood ratio | PASS (e = 0, 1) | Yes | DER; R&S IV — **SOURCE NOT FULLY VERIFIED** | — | Observe-only |
| 3.16 | G_t = max(0, G_{t−1} + ℓ_t) | Definition | Yes | Established; Page IV — **SOURCE NOT FULLY VERIFIED** (CF-06) | — | — |
| 3.17 | T_A = min{t : G_t ≥ h_G} | Definition | Yes | FV | — | — |
| 3.18–3.19 | False-alarm rate; delay | Definition | Yes | DEF | — | — |
| 3.20 | ECE with equal-width bins | Code against formula (M = 10, p = 0 in bin 1): PASS | Yes | FV (Naeini; Guo) | Dimensionless | Encoding changed for rendering only (R3 change log) |
| 3.21 | Log-loss with declared clip | Code against formula (clip 10⁻⁶): PASS | Yes | DER | Nats | — |
| 3.22 | Realized loss | Definition | Yes (script) | DEF | Cost units | Favours REM by construction (stated in Ch. 3 and 5) |

The seven equations whose source attribution remains incomplete are 3.1, 3.2, 3.3, 3.9, 3.10, 3.15 and 3.16. Their status is shown in Chapters 3–6 as SOURCE NOT FULLY VERIFIED and was not upgraded.

## 2. Notation consistency

- The symbols of Table 3.4 are used unchanged in Chapters 4–6.
- Inline symbols were converted to Word sub- and superscript markup in revision R2, and the R3 build renders them.
- Three display equations (2.3, 3.9, 3.20) were re-encoded in R3, because LibreOffice drew placeholder glyphs for `^{*}` and `|·|`. The mathematics is unchanged.
- The rendered PDF was scanned for placeholder glyphs after the rebuild: 0 found.

## 3. Forbidden constructs

None of the constructs excluded by `CLAUDE.md` is present in any chapter or in the code:
- `risk = p × S` as a defined equation;
- confidence Σ|β|;
- the persistence variable ρ;
- risk-based CUSUM;
- SPRT as a required method;
- beta, isotonic or temperature scaling as the adopted calibrator;
- SHAP as a decision input.

The contract test `test_forbidden_components_are_absent_from_the_codebase` passed on 30 October.

## 4. What remains

- Full-text checks of every IV or NC attribution: OI-07, OI-10 to OI-13, CF-06 and CF-07.
- The authoritative equation registry (RG-1).
- Decisions SC-2 and SC-4. The mathematics does not depend on them; the reported numbers do only through the calibration fit, and both fits are reported.
