# 06: Mathematical integrity audit

## 1. Confirmation

**This review introduces no equation, score, weighting, threshold, probability expression, estimator or algorithm.**
- No existing REM equation is modified.
- Every proposal in 04 and 05 is a documentation, architectural, deterministic or policy-based change, except B6/N5. Those are marked future research and are not adopted (§3).

## 2. Existing REM mathematics: audit

**Basis.**
- `EQUATION_PROVENANCE_AUDIT.md` (27 Oct 2026) traces Chapter 3 equations 3.1–3.22 to source, code and test.
- In this review the core equations were re-checked against the current code, which is unchanged since `7c79883`:

| Code location | Equation checked |
|---|---|
| `ridge_logistic.py` `decision_function` | 3.1 |
| `platt.py`, which returns `sigmoid(γ₁·logit + γ₀)` | 3.3 |
| `expected_loss.py` `conditional_risk` | 3.6 |
| `policy.py` D1 / D2 | Predicates |

- The 27 Nov reproduction re-executed this code, with identical outputs.

| Eq. | Content (as in Chapter 3) | Original source (metadata status) | Purpose | Variables operational? | Implementation matches? | Unsupported assumptions / open items |
|---|---|---|---|---|---|---|
| 3.1 | s = β₀ + βᵀx; p̃ = σ(s) | Cox (1958), verified | Linear score and logistic probability | Yes: x = eight features computed per proposed call | Yes (`decision_function`, `sigmoid`) | — |
| 3.2 | Ridge-penalized log-likelihood | le Cessie & van Houwelingen (1992), verified | Fit β with shrinkage | Yes | Yes, with **M1**: the code minimizes NLL + (λ/2)‖β‖², whereas Chapter 3 writes λ‖β‖². These are equivalent up to rescaling λ; the pilot reports λ on the code's scale (`EQUATION_PROVENANCE_AUDIT.md`, Eq. 3.2) | **M1 unresolved** (supervisor) |
| 3.3 | p = σ(γ₁s + γ₀), γ₁ > 0 | Platt: **citation discrepancy** (1999 report title vs 2000 chapter); Guo et al. (2017); Kull et al. (2017), **ambiguous** (two works) | Calibration on the logit | Yes | Yes (`platt.py`) | **Platt citation** and **Kull citation** unresolved. **SC-4:** fitting targets (labels vs Platt's smoothed targets) unresolved |
| 3.4 | Calibration fitted by NLL on labels | Guo et al. (2017) | Calibrator fitting | Yes | Yes (`logit_nll.py`) | SC-4 |
| 3.5 | L(Modify,1,k) = r_mod(k)·C_miss(k) | Derived (law of total expectation) | Loss of Modify on attacks | r_mod measured only in NO-ADAPT replay, where it is near 0 by construction | Yes (`loss_matrix.py`) | **Assumption:** r_mod from replay does not represent an adapting agent. Modify mechanism not exercised |
| 3.6 | R(v) = (1−p)L(v,0,k) + pL(v,1,k) | Elkan (2001): expected-cost decision principle | Conditional risk of each verdict | Yes; L values are **exploratory declared costs** | Yes (`conditional_risk`) | Costs not supervisor-approved |
| 3.7 | v* = argmin R(v) over the feasible set; tie order | Elkan (2001); tie order is a design definition | Verdict | Yes | Code raises on exact ties | **SC-2** (tie rule) unresolved |
| 3.8–3.10 | Indifference thresholds; Allow–Block threshold; escalation feasibility | Derived from 3.6; Chow (1970), conceptual only | Explain verdict boundaries | Yes | Yes | Chow cited as conceptual support only (as required) |
| 3.11–3.12 | Linear attribution φᵢ = βᵢ(xᵢ − x̄ᵢ); additivity | Lundberg & Lee (2017) | **Audit only** | Yes | Yes; never enters the verdict (tested) | — |
| 3.13 | Feature-group sums | Definition | Reporting | Yes | Yes | — |
| 3.14 | Operating-point threshold θ(α) for the B1 baseline | Definition | Baseline only | Yes | Yes | **α grid inconsistency** noted (open item 7) |
| 3.15–3.19 | Bernoulli CUSUM increment, recursion, alarm, false-alarm rate, delay | Page (1954); Basseville & Nikiforov (1993); Reynolds & Stoumbos (1999) | **Observe-only** monitoring | Yes | Yes; no verdict path (tested) | Held-out false-alarm rate 0.106 against a fitting target of 0.05 (did not generalize) |
| 3.20 | Expected calibration error, equal-width bins | Naeini et al. (2015); Guo et al. (2017) | Calibration metric | Yes | Yes | — |
| 3.21 | Log-loss with clip | Derived | Metric | Yes | Yes | — |
| 3.22 | Mean realized loss | Definition | Policy evaluation | Yes | Yes | **Assumption:** matched-cost evaluation favours REM by construction (stated in the validity report) |

**Evaluation statistics used in Chapter 4:**

| Method | Reference | Status |
|---|---|---|
| Grouped (cluster) bootstrap | Field & Welsh (2007) | Crossref-verified 27 Nov |
| Exact McNemar | — | Unclustered; stated |
| Holm correction | Holm (1979) | **Not found in Crossref**; to verify against JSTOR |
| Jaccard index (DiD analyses) | Jaccard (1912) | Verified |

**No undetected mathematical error was found** in this review. The open items above are documented, unresolved supervisor decisions, not errors.

## 3. Mathematics in the reviewed frameworks: not adopted

| Framework | Mathematical element (as reported) | Verified against full text? | Adopted? | Conditions before any future use |
|---|---|---|---|---|
| NEXUS | Platt-calibrated logistic-regression risk score; formal intervention policy Π | **No** (abstract and search excerpt; repository earlier) | No. REM already has its own calibrated logistic estimator with its own sources (Eq. 3.1–3.4) | — |
| Multilayer DiD | Semantic drift score over Sentence-BERT embeddings of intent and trajectory | **No** (abstract) | No | Full text; the original definition copied exactly; data REM does not collect (embeddings of every event); a new experiment |
| MELON | Cosine similarity between embedded tool calls of original and masked runs; fixed threshold in code | Code read (R) | No | An embedding model and extra LLM calls per step; the threshold is the authors' and untested on REM's data |
| CASCADE | Embedding similarity with thresholds (audit) | No | No | — |
| PromptGuard | Classifier scores and critic validation | No | No | Not applicable to tool calls |

**Rule applied.**
- None of these elements is written into REM's design or thesis text.
- If the supervisor wants B6 investigated, the ten conditions of the task (source, exact equation, purpose, relevance, compatibility, data, collection, experiments, necessity) must first be satisfied from the full text. **That has not been possible from this session.**
