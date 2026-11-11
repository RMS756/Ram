# REM and the latest prior art: comparison

**Date:** 11 November 2026. **Rule applied:** a statement about a paper's method, equations or limitations is made only where the full text was read. Abstract-level entries are marked **[ABSTRACT ONLY]** and say nothing about what the full text does or does not contain. For NEXUS the authors' repository README (stored in `REM_FINAL_THESIS/verification/sources_R4/`, retrieved 1 November) is a second source below the level of the paper.

## 1. Reading status

| # | Work | Venue or identifier | Reading |
|---|---|---|---|
| 1 | NEXUS: Structured Runtime Safety for Tool-Using LLM Agents | Findings of AACL 2026, DOI 10.18653/2026.findings-aacl.112 (earlier arXiv:2607.19356) | **[ABSTRACT + REPOSITORY README]**; paper not read |
| 2 | MELON (Zhu et al.) | ICML 2025, PMLR 267 | Full text |
| 3 | Task Shield (Jia et al.) | ACL 2025, long paper 1435 | Full text |
| 4 | aiAuthZ (Kodathala) | arXiv:2607.05518 | **[ABSTRACT ONLY]** |
| 5 | PROVISO (Yan, Zhang, Kan, Suya, Wang) | arXiv:2610.27115v1 | Full text |
| 6 | AgentBoundary (Yang et al.) | arXiv:2609.33658v1 | Full text |
| 7 | CASEL (Zhang, Shen, Yan, Zhang) | arXiv:2610.36570v1 | Full text |
| 8 | Calibration Is Not Control (Zhang et al.) | arXiv:2606.21399v2; NeurIPS 2026 per its header | Full text; code repository not accessed |
| 9 | Kairos (Hempel, Loose, Cavallaro et al.) | arXiv:2610.18457 | **[ABSTRACT ONLY]** |
| 10 | "Approve What, Exactly?" (step-up authorization) | arXiv:2610.21063 | **[ABSTRACT ONLY]** |
| 11 | SentryBench; DelegationBench | arXiv:2610.34535; arXiv:2610.05532 | **[ABSTRACT ONLY]** |

Detailed extraction of the six full-text papers, with equation numbers: `REM_Authorization_Generalization_Study/02_PAPER_AND_ALGORITHM_EVIDENCE_MATRIX.md`.

## 2. Comparison of the closest systems

| Dimension | REM (this thesis) | NEXUS [ABSTRACT + README] | MELON | Task Shield | aiAuthZ [ABSTRACT ONLY] | PROVISO | CASEL |
|---|---|---|---|---|---|---|---|
| Decision point | each proposed tool call | a structured plan; one intervention per plan | each tool-call step | each instruction and tool call | each tool call, at an off-host gateway | commitment point, after proposal and before execution | each action |
| Language model in the decision path | no | none described (rules, argument inspector, logistic-regression scorer) | yes (masked re-execution, embedding similarity) | yes (LLM scoring of ContributesTo) | not indicated | no LLM; a frozen encoder and a trained controller of 17.40M parameters | no (simulation) |
| Evidence used | provenance of arguments, behavioural counters, action features | deterministic rules, argument inspection, calibrated score | agreement of tool calls with and without the user prompt | task instructions extracted per privilege level | identity-bound, argument-level policy | provenance-typed memory of trusted and external observations | failure probability and consequence |
| Risk estimate | ridge logistic regression, calibrated on the logit | calibrated logistic regression | none | LLM contribution score in [0, 1] | none indicated | learned value V̂(x, a) | assumed p̂ |
| Decision rule | expected-loss minimum over four verdicts, costs by consequence tier | rule-first cascade with two score thresholds chosen once on a safety–utility loss (README) | block when similarity exceeds 0.8 | misaligned iff total contribution score is 0 | policy match | U = V̂ − τ_a, argmax (Eq. 7) | per-mode cost argmin (Eq. 2); finite-sample threshold (Eq. 5) |
| Actions | Allow, Modify, Escalate, Block | allow, block, request confirmation, request revision | continue or stop | allow or feedback | allow or deny | commit proposed or alternative | direct, verify, sandbox, clarify, approve, abstain |
| Consequence awareness | four tiers set by operation and amount | through rule severities and irreversible-action rules (README) | none | none | not indicated | none explicit | continuous consequence c in [0, 1] |
| Evaluation data | AgentDojo banking recordings (5,426 eligible episodes over two populations) | synthetic plans (128-instance test split), an injection set, a stress set, R-Judge, AgentHarm | AgentDojo, four suites, live | AgentDojo, four suites, live | AgentDojo banking (per the abstract) | AgentDojo four suites; other benchmarks fitted separately; a controlled payment task | simulation only |
| Evaluation mode | recorded-trace replay; no live agent | label-based scoring of plans | live agents | live agents | not established | restored-environment rollouts | simulated actions |
| Held-out attack objective | yes (nine folds; double holdout) | not established | not applicable (no fitting) | not applicable | not applicable | no (folds by user task) | not applicable |
| Comparison with rule baselines on the same trajectories | yes (P1, P2, A2, B1) | abstract reports a gain over "rule-only intervention selection" | no | no | not established | ablations of its own components | product-score gate (and reports no gain over it) |
| Headline figures reported by the authors | see `REM_EXPERIMENTAL_RESULTS_VERIFIED.md` | F1 0.949; four-class intervention accuracy 0.6406; median latency 0.38 ms | GPT-4o, all suites: benign utility 68.04, utility under attack 32.91, ASR 0.95 | GPT-4o, banking: clean utility 81.25, utility under attack 82.64, ASR 6.25 | banking: blocks all seven attacker-directed calls "at the cost of one legitimate first-time payment" | AgentDojo: benign utility 87.63, utility under attack 85.41, targeted ASR 0.28 | none on a benchmark |
| Limitation most relevant here (quoted where it is the authors' statement) | replay only; no reviewer; one benchmark | not established | reported benign utility with GPT-4o falls from 80.41 to 68.04; the detector needs an embedding model | the decision depends on language-model judgments | not established | "fitted separately for each benchmark … we do not study transfer" | "Intervention effectiveness is assumed, not measured" |

**The figures in the last-but-one row are not comparable with one another or with REM.** They come from different agents, suites, attack sets and evaluation modes. They are listed to show what each paper reports, not to rank.

Kairos **[ABSTRACT ONLY]**: a reference monitor at the isolation boundary with deferred effects; its abstract reports AgentDojo attack success falling from 47.0% to 2.7% with benign utility at the undefended level. It acts below the agent, on effects, and is complementary to a tool-call monitor.

## 3. What each work means for REM's claims

| Work | Consequence for the thesis |
|---|---|
| NEXUS | The combination "calibrated logistic regression + rules + argument inspection + four graduated actions" is published. REM cannot claim that combination as new. Detailed comparison: `REM_NEXUS_COMPARATIVE_STUDY.md`. |
| CASEL | A per-mode consequence-cost rule with the same structure as REM's expected-loss rule is published (later than REM's design; simulation only). REM cannot claim the decision form. CASEL's own finding that the per-mode cost "does not reduce harm beyond a product-score gate" parallels REM's finding that four verdicts add nothing measurable in replay. |
| Calibration Is Not Control | Explains REM's result that calibration changed no verdict, and that re-thresholding cannot recover a distinction the score lacks. Its intervention-value target was tested in this project and failed on a held-out objective. |
| AgentBoundary | Establishes over-defence as a general finding. REM's 33 of 178 released authorized calls is an instance of it. Its paired counterfactual design is the model for this project's fixture pairs. |
| PROVISO | Publishes provenance-typed action selection with far better reported utility than REM, using a much heavier learned controller and restored rollouts. Supports the gap through its stated limitation. |
| Task Shield, MELON | Published AgentDojo defences with a language model in the loop. Neither was run here. MELON integration is implemented and unevaluated (`REM_MELON_EXECUTION_STATUS.md`). |
| aiAuthZ, step-up authorization | Indicate that the root limitation found here (no trusted authorization record) is addressed in the literature by adding a trusted channel, which REM's threat model does not have. This is the thesis's principal future work. |
| Kairos | Enforcement at the system boundary reports low attack success without utility loss; a tool-call monitor that withholds calls cannot match that utility profile on the present evidence. To be discussed as an alternative placement. |

## 4. Position of REM after this comparison

REM is one transparent instance of a published family (calibrated risk score, consequence-dependent costs, graduated verdicts). Its defensible contribution is the controlled evaluation of that instance against rule baselines under held-out objectives and tasks, with a pre-registered confirmatory run and reported negative results. It is not a new mechanism and it is not shown to outperform any published defence.

## 5. Outstanding

Full texts of NEXUS, aiAuthZ and Kairos are needed to replace the **[ABSTRACT ONLY]** cells. Until then the thesis must describe these three works only at the level of their abstracts and say so.
