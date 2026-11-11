# 10 — Thesis update plan (proposals only; the thesis was not modified)

**Status:** every item is `[PROPOSED — SUPERVISOR APPROVAL REQUIRED]`. Items marked ★ depend on a decision in `09`, section 8. Evidence for each item is in this folder; nothing below requires content that does not exist.

## Chapter 1 — Research problem, gap, objectives and questions

| # | Change | Depends on |
|---|---|---|
| 1.1 | Replace the gap statement by the narrowed wording (`01`, section 5): an evidence gap about transfer of learned decision policies and their value over simple rules, for monitors without a language model in the decision path. | D5 ★ |
| 1.2 | State that the gap is studied offline on recorded trajectories and does not depend on live deployment. | D5 ★ |
| 1.3 | Research questions, kept `[PD]` until approved, phrased as evaluation questions: RQ1 unnecessary intervention on legitimate banking actions; RQ2 transfer to unseen tasks and attack objectives; RQ3 security–utility trade-off; RQ4 component contributions. | D6 ★ |
| 1.4 | Remove or soften any sentence that promises an improved algorithm. The contribution list becomes: (a) the REM composition and its evaluation; (b) a double-holdout comparison with rule baselines and outcome-supervised variants, including negative results; (c) documented failure modes (argument substitution, unrequested actions, reformatted identifiers). | D1, D2 ★ |

## Chapter 2 — Literature review and comparative synthesis

| # | Change | Source |
|---|---|---|
| 2.1 | Add PROVISO, AgentBoundary and CASEL; extend the existing discussion of Calibration Is Not Control (already cited as C. Zhang et al., 2026) with Eq. (1), Proposition 1 and Remark 1. | `02` |
| 2.2 | Comparative table: decision input, whether a language model is in the decision path, what is fitted, what transfer is examined, what the authors state as limitations. Quote PROVISO's limitation on per-benchmark fitting verbatim. | `02` |
| 2.3 | Correct statement on PROVISO: it holds out user tasks on AgentDojo; it does not hold out attack objectives or test cross-benchmark transfer. | `01`, section 1 |
| 2.4 | Position CASEL as a structurally equivalent decision-cost rule evaluated only in simulation, and note its authors' finding that the per-mode cost did not reduce harm beyond a product-score gate. | `02` |
| 2.5 | Mark CaMeL, KAIROS and FinHarness as not read in this study unless full texts are obtained; do not cite details from them. | `02`, section 3 |

## Chapter 3 — Methodology and algorithms

| # | Change | Depends on |
|---|---|---|
| 3.1 | No change to the approved algorithm. | D2 ★ |
| 3.2 | Add to the evaluation design: the rule baselines P1, P2 and A2 with their one-line definitions; the double-holdout scheme S2; the reformatted-identifier probe; the fixture pairs (design after AgentBoundary). | D3 ★ |
| 3.3 | Add the limitation statements from the earlier audit (provenance is not authorization; Modify, Escalate and Block are indistinguishable in replay without a reviewer). | — |
| 3.4 | If D4 is approved: record the removal of the behavioural group as a declared amendment to SD-FEAT, with the pre- and post-amendment configurations both reported. | D4 ★ |
| 3.5 | Describe the tested candidate in an appendix or a "rejected alternatives" subsection, with its derivation labelled DERIVED and its outcome. Do not present it as part of REM. | D1 ★ |

## Chapter 4 — Implementation, evaluation and results

| # | Change | Source |
|---|---|---|
| 4.1 | Extend the main results table with P1, P2, A2 and M01 beside B0, B1 and REM (counts and grouped intervals). | `08`, section 2 |
| 4.2 | Add the double-holdout table and the per-injection-task table (the password-change failure of the outcome-supervised arms). | `08`, sections 2–3 |
| 4.3 | Add the per-category over-defence table for the original REM. | `03`, Problem A |
| 4.4 | Add the intervention-equivalence result (0 of 3,313 episodes differ). | `03`, Problem E |
| 4.5 | Add the reformatted-identifier probe and the fixture counts, in a separate subsection titled as perturbation probes. | `08`, section 7 |
| 4.6 | Report the published defences in a table of quoted numbers with a column stating why they are not comparable; keep recorded live AgentDojo defences in a separate table from replay results. | `08`, section 8 |
| 4.7 | Label every table with the evaluation mode: offline recorded-trace replay, step level, no reviewer, NO-ADAPT. | — |

## Chapter 5 — Discussion, limitations and conclusions

| # | Change | Source |
|---|---|---|
| 5.1 | Answer RQ1: unnecessary intervention is large for the original REM (33 of 178 authorized calls released) and is reduced by simple rules and by removing behavioural evidence, not by the proposed mechanism. | `08` |
| 5.2 | Answer RQ2: the outcome-supervised policy does not transfer to an unseen attack objective (119 of 119 password-change attacks released); the original REM and the parameter-free rules are stable under double holdout. | `08`, section 3 |
| 5.3 | Answer RQ3: no arm improves utility at no security cost in a way that is statistically established with 16 user tasks; report the non-dominated set and the intervals. | `08`, sections 2 and 4 |
| 5.4 | Answer RQ4: behavioural evidence costs utility without measured benefit; context evidence, predicates and calibration contribute nothing measurable; action evidence carries the security result and is brittle to reformatting. | `03`, Problem D; `08`, section 7 |
| 5.5 | Limitations: all of `08`, section 13. State explicitly that no claim is made about live agents, reviewers, other benchmarks or published defences. | `08` |
| 5.6 | Conclusion: the thesis's supported contribution is evaluative. REM as specified is secure on this benchmark at a high utility cost; simpler rules do as well on this benchmark; authorization cannot be established from text provenance alone. | `09` |
| 5.7 | Future work: a structured, trusted statement of user intent with a deterministic integrity check; evaluation with a non-ideal reviewer; an independent benchmark; equal-terms runs of Task Shield, MELON and PROVISO. | `09`, D8–D9 |

## Wording to avoid anywhere

"improved REM", "authorization-aware REM outperforms", "generalizes better", "validated", "live", "blind test set", "REM distinguishes authorized from unauthorized payments", any ranking against Task Shield, MELON or PROVISO, and any statement that the tested candidate or the removal of behavioural features is an approved part of the design.
