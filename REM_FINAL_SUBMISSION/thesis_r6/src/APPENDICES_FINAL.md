# Appendix A: Notation, Optional Sequential Analysis and Equation Provenance

## A.1 Notation

**Table A.1. Notation used in this chapter**

| Symbol | Meaning |
|---|---|
| t, T | Step index within an episode; episode length |
| g | User objective of the episode |
| c~t~ | Context at step t, as segments with provenance labels |
| a~t~ | Proposed action (tool name and arguments) at step t |
| H~t~ | Episode history up to step t |
| y~t~ ∈ {0, 1} | Latent label: 1 if a~t~ is adversarially induced |
| x~t~ ∈ [0, 1]^d^ | Evidence vector; groups x^ctx^, x^beh^, x^act^ with index sets I~ctx~, I~beh~, I~act~ |
| β~0~, β, λ | Logistic intercept, coefficient vector, ridge strength |
| s~t~ | Logit (linear predictor) |
| p̃~t~, p~t~ | Uncalibrated probability; calibrated probability |
| γ~1~, γ~0~ | Calibration slope and intercept |
| z~t~, k~t~, κ | Consequence descriptors; consequence tier; tier map |
| 𝒱 | Verdict set {Allow, Modify, Escalate, Block} |
| 𝒱(a~t~) | Verdicts feasible for a~t~ |
| v~t~ | Verdict issued at step t |
| L(v, y, k) | Loss of verdict v when the label is y and the tier is k |
| C~miss~(k), C~FA~(k), C~mod~(k), C~esc~ | Declared costs of a missed attack, a false intervention by Block, Modify on a legitimate action, and escalation |
| r~mod~(k) | Residual attack-success rate after Modify at tier k (measured) |
| R~t~(v) | Conditional risk of verdict v at step t |
| π~v,v′~(k), p^\*^~k~ | Indifference threshold between verdicts v and v′; Allow–Block threshold |
| σ(·) | Logistic function, σ(u) = 1 / (1 + exp(−u)) |
| Π, k~D2~ | Set of prohibited actions; minimum tier for predicate D2 |
| θ(α), α~blk~, α~mod~ | Baseline threshold for false-positive target α; targets for Block and Modify |
| 𝒯~R~ | Set of tools to which the Modify mechanism applies |

Symbols used only in the optional sequential analysis are defined in Appendix A.3. Symbols that appear in a single equation, such as Δ~0~, Δ~1~, B~m~, and the step sets D~fit~, D~cal~, and D~val~^benign^, are defined where they are used. Each symbol has one meaning throughout the chapter.

## A.2 Layer interfaces

**Table A.2. Layer interfaces**

| Layer | Consumes | Produces |
|---|---|---|
| L1 Input & Context | Objective, system prompt, user messages, tool results, proposed action | Labeled context c~t~; entities with provenance; held action a~t~ |
| L2 Detection | Untrusted segments of c~t~ | Context evidence x^ctx^ |
| L3 Behavioral Analysis | H~t~, a~t~, entities, benign reference transitions, privilege map | Behavioral evidence x^beh^; action evidence x^act^ |
| L4 Decision Engine | x~t~, consequence descriptors z~t~, frozen parameters, declared policy | p~t~, k~t~, R~t~(·), verdict v~t~, audit record |
| L5 Mitigation | v~t~, a~t~, episode restrictions | Released, restricted, withheld, or refused action |

The four functions are separated architecturally. Layers 2 and 3 produce evidence and issue no verdicts. Layer 4 performs probability estimation and decision. Layer 5 performs mitigation.

## A.3 Optional observe-only sequential analysis

Sequential change detection is not part of REM's verdict path. If the supervisor approves it for the thesis narrative, it is performed **offline** on the per-step indicators logged by the Behavioral Analysis Layer. It never influences a verdict.

For each step, a binary deviation indicator e~t~ ∈ {0, 1} is defined as 1 if at least one of x^beh^~1~, x^beh^~3~, x^beh^~4~, or x^act^~1~ equals 1, or if x^beh^~2~ = 1; otherwise 0 [indicator set pending supervisor approval]. Let q~0~ and q~1~, with 0 < q~0~ < q~1~ < 1, be the rates of e~t~ = 1 before and after an adversarial change.

The log-likelihood ratio of one observation, as defined by Basseville and Nikiforov (1993), specialized to Bernoulli observations, is:

$$ \ell_t = e_t \ln\frac{q_1}{q_0} + (1-e_t) \ln\frac{1-q_1}{1-q_0} \qquad (3.15) $$

*Status:* derived by substituting the Bernoulli probability mass function into the log-likelihood ratio of Basseville and Nikiforov (1993). A cumulative sum chart for Bernoulli observations is treated by Reynolds and Stoumbos (1999).

The cumulative sum statistic and alarm time are (Basseville & Nikiforov, 1993; Page, 1954):

$$ G_t = \max(0,\, G_{t-1} + \ell_t), \qquad G_0 = 0 \qquad (3.16) $$

$$ T_A = \min\{ t : G_t \ge h_G \} \qquad (3.17) $$

where h~G~ > 0 is the alarm threshold.

*Status:* established from source.

The per-episode false-alarm rate on benign episodes and the detection delay are defined as:

$$ \mathrm{FA}_{\mathrm{ep}}(h_G) = \frac{\left|\{ j \in E_{\mathrm{ben}} : \max_t G^{(j)}_t \ge h_G \}\right|}{\left|E_{\mathrm{ben}}\right|} \qquad (3.18) $$

$$ \tau_d = T_A - \nu, \qquad T_A \ge \nu \qquad (3.19) $$

where E~ben~ is the set of benign episodes in the fitting portion of a fold, G^(j)^~t~ is the statistic in benign episode j, τ~d~ is the detection delay, and ν is the first step at which injected content enters the context.

*Status:* design definitions.

The parameters are determined as follows:
- q~0~ is the empirical rate of e~t~ = 1 on benign fitting steps, floored at a declared minimum.
- q~1~ is declared and reported over a range, because the scarcity of multi-step attacks does not allow it to be estimated reliably.
- h~G~ is the smallest value for which Equation 3.18 does not exceed a declared target.

The procedure has known optimality properties in sequential change detection: Lorden (1971) proposed stopping rules that are asymptotically optimal in a defined sense, and Moustakides (1986) showed Page's stopping time to be optimal in a stronger sense. Both results are proved within a sequential-analysis model whose conditions could not be inspected during verification and are not claimed to hold for agent trajectories, where observations are neither independent nor drawn from known distributions. They therefore motivate the procedure and provide no guarantee in this setting. Given the short trajectories of Section 3.11.4, this analysis may have little to detect.

## A.4 Provenance of the equations of Chapter 3

**Table A.3. Provenance of the equations in this chapter**

| Eq. | Content | Status | Source | Verification |
|---|---|---|---|---|
| 3.1 | Logistic model | Established | Cox (1958) | IV |
| 3.2 | Ridge-penalized log-likelihood | Established | le Cessie & van Houwelingen (1992) | IV (penalty constant pending) |
| 3.3 | Logistic calibration on the logit, γ~1~ > 0 | Adapted | Platt (2000); Guo et al. (2017); Kull et al. (2017) | Platt NC; Guo FV; Kull FV |
| 3.4 | Calibration fit by negative log-likelihood | Established | Guo et al. (2017) | FV |
| 3.5 | Adversarial loss of Modify | Derived (assumption A-Mod) | Law of total expectation | DER |
| 3.6 | Conditional risk | Adapted | Elkan (2001) | FV (Eq. 1 form) |
| 3.7 | Bayes verdict with tie-breaking | Adapted | Elkan (2001) | FV; tie order DEF |
| 3.8 | Pairwise indifference threshold | Derived | From Eq. 3.6 | DER |
| 3.9 | Allow–Block threshold | Derived | From Eq. 3.8; consistent with Elkan (2001) | DER |
| 3.10 | Escalation feasibility condition | Derived | From Eqs. 3.6, 3.7, 3.9; Chow (1970) conceptual basis | DER; Chow IV |
| 3.11 | Linear attribution | Adapted | Lundberg & Lee (2017) | FV |
| 3.12 | Completeness identity | Derived | Lundberg & Lee (2017) local accuracy | FV + DER |
| 3.13 | Group attribution | Definition | — | DEF |
| 3.14 | Baseline operating-point threshold | Definition | — | DEF |
| 3.15 | Bernoulli log-likelihood ratio (optional) | Derived | Basseville & Nikiforov (1993); Reynolds & Stoumbos (1999) | FV; R&S IV |
| 3.16 | CUSUM recursion (optional) | Established | Basseville & Nikiforov (1993); Page (1954) | FV; Page IV |
| 3.17 | Alarm time (optional) | Established | Basseville & Nikiforov (1993) | FV |
| 3.18 | Per-episode false-alarm rate (optional) | Definition | — | DEF |
| 3.19 | Detection delay (optional) | Definition | — | DEF |
| 3.20 | Expected calibration error | Adapted | Naeini et al. (2015); Guo et al. (2017) | FV |
| 3.21 | Log-loss | Derived | From Eq. 3.2 | DER |
| 3.22 | Realized loss | Definition | — | DEF |

**Implementation conventions.** Four conventions in the implementation differ in form from the equations as printed; none changes their meaning:

- **Eq. 3.2:** the code's penalty is (λ~impl~/2)‖β‖², so λ = λ~impl~/2 (Section 3.7.1).
- **Eq. 3.4:** the label-NLL fit is the reference; Platt's smoothed targets are a sensitivity variant.
- **Eq. 3.14:** the candidate set includes a value just above the largest benign probability.
- **Eq. 3.20:** steps with p = 0 fall in the first bin.

These conventions are listed with the code location of each equation in the requirement–equation–function–test table of Section S-3.15.

*Verification codes:* FV — formulation checked against the source; IV — source identity confirmed, formulation to be checked against the full text; NC — source not accessible during this revision; DER — derived in this chapter; DEF — design definition. The codes are retained until final reference verification is complete.

## A.5 Why logistic regression

Logistic regression models the probability of a binary outcome as a logistic function of a linear score (Cox, 1958):

$$\Pr(y = 1 \mid x) = \frac{1}{1 + \exp\!\big(-(\beta_0 + \beta^\top x)\big)} \qquad (2.1)$$

**Why it suits a runtime layer.**

- Evaluation costs one inner product.
- Coefficients can be inspected.
- The output is intended as a probability, not as an arbitrary score.

**Limitations.**

- Interactions must be engineered into the features.
- A model fitted on one attack distribution can be miscalibrated on another.
- With scarce adversarial examples and binary indicators, the unpenalized estimate may not be finite. A ridge penalty addresses this (le Cessie & van Houwelingen, 1992).
- Naive Bayes is the generative counterpart with the same linear form. It may reach its (higher) asymptotic error with fewer examples (Ng & Jordan, 2002). It is an established alternative estimator and is not part of REM.

**Use in agent security.** Among the included studies, only NEXUS uses a logistic risk score for agent safety (Hossain et al., 2026). The choice of estimator family therefore has one direct precedent in agent security, and that precedent operates at the plan level.

*This section was Section A.5 in the fifth edition; it is printed here because it holds Equation 2.1.*

# Appendix B: Register of Open Supervisor Decisions

**No supervisor decision is recorded in the project repository.** Every item below is open. Where the thesis needed a wording, it uses the option marked "handling", labelled as pending. The full register, with options and effects, is kept with the project records (`SUPERVISOR_DECISIONS_REQUIRED.md` and the register of the five-chapter draft).

**Table B.1. Open decisions that determine what the thesis may claim**

| ID | Item | Handling in this thesis | Decision needed |
|---|---|---|---|
| SD-FREEZE | Approval of the Chapter 3 specification as frozen | Implemented as specified; values declared | Approve or amend |
| SD-FEAT | Feature set; **proposed amendment REM v1.1** (behavioral evidence removed) | v1.0 is the design; v1.1 is reported beside it as an ablation whose gain in task completion met the pre-declared decision rule; its effect on security is not resolved | Approve v1.1, or keep v1.0 |
| SD-PERM | **Exploratory extension: task-permission evidence** (request compiler, instruction matching, two-verdict decision and authority guard, in three revisions; Chapter 3, Section 3.14) | Reported as proposed and exploratory, with development results only; not part of REM v1.0 or v1.1. The guard used alone (GV) is reported as the arm best supported on development data, because every learned or calibrated decision behind it gave the same outcomes | Keep in the thesis as an exploratory result, move to future work, or authorize a prospective evaluation with independently written requests; confirm GV as the reported arm |
| SD-AMT | Typed verification of request-derived amounts (GV_math; Chapter 4, Section 4.5.4) | Reported as proposed and exploratory; the frozen GV keeps its defects | Adopt the verifier, extend its grammar after independent validation, or keep GV |
| SD-D2 | Whether the declared predicate D2 (required evidence unavailable at a high tier) applies to calls that the permission guard supports | Applied as declared; it withholds 55 and 62 request-supported updates of a scheduled transaction (Chapter 4, Section 4.5.3) | Keep D2 behind the guard, or exempt request-supported calls in a separately labelled variant |
| SD-COND | Whether a subjective condition in a request ("if something looks suspicious") may ever license an action | Never treated as satisfied; the call stays unknown and is withheld without a reviewer. This costs user task 14 (167 and 119 completed tasks) | Confirm, send such calls to a reviewer, or specify a verification mechanism |
| D-9 | Costs, tier map and predicates | Declared exploratory values | Approve, or elicit new values |
| SC-1 / D-2 | Mitigation semantics: step-level or episode-level | Step-level reference; episode-level in Appendix S-E | Confirm |
| SC-2 / D-4 | Tie rule | Chapter 3 order, with ties counted; no tie occurred in any run | Confirm |
| SC-3 | Calibration-removed ablation run in the evaluation path | Reported | Confirm |
| SC-4 / D-3 | Calibration fitting target: labels or Platt's smoothed targets | Both implemented; label fit is the reference | Confirm |
| SC-5 | Brier score convention | Binary convention reported, with the convention stated | Confirm |
| SC-6 | Layer label of the estimator in code comments | Decision Engine in the thesis; code comment differs | Confirm |
| SC-7 / D-1 | Recorded-trace replay against the original scope, which excluded replay-based estimation | Kept as a labelled NO-ADAPT analysis | Keep, drop, or replace by live runs |
| D-6 | Label rule; the user_task_15 collision; no human label audit | Rule kept; collision reported; audit package prepared, not annotated | Keep or redefine; audit |
| D-7 | Reviewer model for Escalate | Two bounds; headline results use no reviewer | Confirm |
| D-8 / SD-DET | Injection classifier of the Detection Layer | Absent; not replaced | Choose a classifier, or record its absence as final |
| D-10 | Wording of the research questions | Marked proposed | Confirm |
| D-12 | Thesis title | As supplied by the author | Confirm |
| D-15 | Live closed-loop experiment and the comparisons that need a language model (MELON, Task Shield, Progent with generated policies, the semantic verifier): backbone, decoding, repeats, budget, credentials | Not run; a sealed prospective protocol exists | Authorize with a spending limit, or accept submission without them |
| SD-5 | Banking-only evaluation against objective O1, which also names task-automation agents | O1 achieved for banking only | Accept or extend |
| GAP | Research-gap wording of Chapter 2, Section 2.11.5 | Proposed wording | Confirm |
| RULES | Rule baselines P1, P2 and A2 as mandatory comparators; Progent's manual banking policy as a published comparator in replay | Included | Confirm |
| RG-1 | Authoritative equation registry | Missing; no equation identifier was created | Provide, or accept the provenance table of Appendix A |
| OI-01 to OI-06 | Statements about NEXUS | Abstract and the authors' repository (read 13 November 2026) only; full text not read | Supply the full text |
| FULLTEXT | Full texts of aiAuthZ, Kairos and CaMeL, and of the three method papers tested behind the permission guard (Tong et al., 2018; Friedman, 2001; Angelopoulos et al., 2022); full-text screening of the systematic review | aiAuthZ: abstract and repository whitepaper; Kairos: abstract; CaMeL: official repository; Progent: version 3 read in full; method papers: authors' or library implementations; six other papers read in full in November 2026 | Supply; decide on a full-text update |
| N-1, N-2 | Supervisor roles on the title page; faculty, department and degree | As in the latest instruction; not verified against official records | Confirm |
| N-3 | Arabic abstract and Arabic spellings of names | Draft translation | Review |
| N-6 | The co-supervisor is a co-author of one cited study (Kanaker et al., 2026) | Cited as a source only; evidence level stated | Decide whether a disclosure is required |
| N-8 | Committee page, declaration (including any declaration on the use of AI tools), dedication, acknowledgement | Placeholders | Complete with the university's wording |
| N-9 / TEMPLATE | University thesis template and formatting rules | **Not available**; an assumed A4 thesis layout is used | Provide; re-check the layout |

Smaller items (the Platt reference year, the regularization convention, one cell of the false-positive grid, and the optional sequential analysis) are listed in the project register and do not affect any reported result.
