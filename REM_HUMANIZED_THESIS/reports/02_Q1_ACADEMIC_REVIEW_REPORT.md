# Independent academic review against the expectations of a strong international journal (Stage 2)

**Reviewer stance:**
- This review assesses the research, not the language. Better wording in Stage 1 does not change any finding below.
- No journal ranking, acceptance probability or readiness score is given.
- "Q1" is used only as shorthand for the expectations of strong peer-reviewed venues in AI security, such as computer-security journals and the security tracks of ML venues.
- **Basis:** the full text of the revised thesis, the repository's result files and audit records, and two literature checks made for this review.

## 1. Summary judgement

The thesis is an honest, carefully controlled evaluation of one runtime decision design for tool-using financial agents. Its strongest assets are:
- **Integrity of reporting:** negative results are kept, every number traces to stored per-episode records, and the claim boundaries are explicit.
- **Paired, pre-registered comparisons** against simple baselines, which much of the field omits.

Its principal weaknesses for a journal submission are external validity and the novelty of the artifact:
- one benchmark and one attacker account;
- offline replay of recorded trajectories under a no-adaptation assumption;
- a mechanism whose components are all published.

**The publishable contribution is the evaluation result, not the framework.** A carefully designed learned, consequence-aware runtime decision does not beat one-line provenance rules, and its protection comes with heavy over-blocking.

## 2. Originality and contribution

| Question | Assessment |
|---|---|
| Is the problem clearly defined? | **Yes.** Sections 1.2 and 3.3 define the threat (indirect prompt injection through tool outputs), the protected boundary (the proposed tool call) and the target event (adversarially induced action, y~t~ = 1). |
| Is the gap supported by the literature? | **Partly.** It is restated (Section 2.11.5) as an evidence gap, which is the defensible form. The support comes from a record-level review and six full-text readings, so a journal reviewer could find works that already contain parts of the comparison. |
| Is the contribution clear and proportionate? | **Yes.** The thesis lists what it does not claim (Section 1.11) and attributes every mechanism to its source (Table 2.2). No unsupported novelty claim was found in the revised text. |
| Is REM differentiated from existing approaches? | **Only narrowly**, and the thesis says so. NEXUS (calibrated logistic score, four interventions, loss-based thresholds), CASEL (per-mode expected cost) and AgentTrust (pre-execution interception, graduated verdicts) cover most of REM's design. What remains is the per-call, tier-indexed expected-loss rule and its evaluation on an executable banking benchmark. |
| More than an implementation exercise? | **Yes, as an evaluation.** Holding out attack objectives, testing a double holdout and running one confirmatory replay go beyond a typical implementation thesis. |

**Classification of the contributions:**
- **Engineering:** the five-layer implementation, the fail-closed configuration and the test suite.
- **Evaluation (the main contribution):**
  - the paired comparison with rules and with a published policy decided by its authors' code;
  - the component-level ablation;
  - the negative results.
- **Integration:** a combination of established mechanisms. No component is novel.
- **Methodological, minor:** the reachability analysis (which calls the learned decision actually decides) and the shadow-mode equivalence check.

## 3. Literature review and positioning

**Strengths.**
- The review is reported following PRISMA 2020 and PRISMA-S, with its limits stated: record-level only and a single database.
- Closely related systems are acknowledged rather than ignored, including NEXUS, AgentTrust, PROVISO, CASEL, Progent, PACT, ROPE and CapLite.

**Weaknesses a journal reviewer would raise.**
1. **No full-text screening, one database, a relevance-ranked cap.** The search recalled only 3 of 13 known prior-art studies (Section 2.2.3). That is a large gap for a systematic-review claim. For a journal paper the review would be replaced by a conventional related-work section built from full texts.
2. **Several of the closest works are known only from abstracts or repositories:** NEXUS, aiAuthZ, Kairos, CaMeL, PACT, ROPE, CapLite and DRIFT.
3. **Missing works.** The following were checked in this review. Their bibliographic records are verified; their relevance to the argument is a suggestion and was not assessed by reading the full texts.

| Work | Record | Why it matters |
|---|---|---|
| SecAlign (S. Chen et al., ACM CCS 2025, pp. 2833–2847, doi:10.1145/3719027.3744836) | Verified with Crossref | Model-level defense against prompt injection, the main alternative family to runtime mediation. StruQ, by the same group, is already cited. |
| PromptArmor (T. Shi et al., 2025, arXiv:2507.15219) | Verified with OpenAlex (preprint) | LLM-based detection and removal of injected content, with a reported attack success below 1% on AgentDojo. It is a strong baseline that a journal reviewer would expect to be discussed. |
| Design Patterns for Securing LLM Agents against Prompt Injections (Beurer-Kellner et al., 2025, arXiv:2506.08837) | Verified with OpenAlex (preprint) | Systematizes architectural patterns, such as plan-then-execute and action selection, that relate directly to REM's position. |
| The Instruction Hierarchy (Wallace et al., 2024) | Not verified here (no Crossref record found) | Training-time privilege ordering. Cite only after checking the record. |

**No reference was added to the thesis.** Adding literature changes the review's scope and is listed as a Category C item.

## 4. Methodology and experimental rigor

| Element | Assessment |
|---|---|
| Threat model | Clear (AD-1 evaluated, AD-2 design scope only), with assumptions AS-1 to AS-10 stated and typed |
| Design-science framing | Appropriate. The activities are mapped to the thesis (Table 3.1). |
| Benchmark | AgentDojo banking v1 only: 16 user tasks, 9 injection tasks, one attacker account. This is the largest limitation for generalization. The single attacker account makes recipient-based rules unusually strong, and the thesis states this. |
| Data | Recorded traces of 21 backbones distributed with the benchmark; a second population of 2,113 episodes from new pipelines. Episodes are correctly treated as dependent through grouped resampling. |
| Labels | Reference-matched attempt labels. A proxy, ambiguous for user_task_15 in early suite versions, inspected only by an AI assistant (30 episodes) and **not audited by a human**. A journal would require at least a human audit of a stratified sample with agreement. |
| Evaluation mode | Offline replay under NO-ADAPT. It cannot show protection against live or adaptive agents, and the thesis never claims it does. It also makes the four-verdict design untestable, because Modify, Escalate and Block coincide by construction. This affects RQ3. |
| Baselines | Strong for a thesis: no defense, a consequence-independent threshold policy sharing the same estimator, three model-free rules, and a published policy decided by its authors' own checker. Missing for a journal: any LLM-based defense run under the same conditions (MELON, DRIFT, Task Shield, PromptArmor). |
| Ablation | Component-level, pre-registered, paired. The isolation limits are stated (Input & Context not removable; classifier absent). |
| Statistics | Grouped percentile bootstrap with 9 and 16 clusters, plus exact McNemar tests. The thesis states correctly that the intervals are descriptive and need not reach nominal coverage. A journal reviewer would ask for a cluster-aware test, such as a permutation test over injection tasks, or a hierarchical model, and for a stated policy on multiplicity across the many arms. |
| Researcher degrees of freedom | High: many arms, several studies on the same development data, repairs written after results. The thesis discloses this (threats 11, 13, 17). Only one contrast is confirmatory. |
| Reproducibility | Very good: pinned versions, seeds, commit hashes, protocols committed before scoring, a number checker over 498 cells, and re-execution reproducing stored counts exactly. |

**Alternative explanations to discuss more explicitly.**
1. **The cost structure.** REM's over-blocking may be an artifact of the declared costs (C~esc~ = 0.3; C~miss~ = 10 and 20) rather than of the learned decision. A4d (thresholds) shows the trade-off moves, and the declared loss grid (Section 4.6.5) varies costs only in observe-only analysis. A replay sweep over costs would separate "the learned decision over-blocks" from "these declared costs over-block".
2. **The behavioral features.** They may fail because the benchmark's tasks are short (one to five calls), not because trajectory evidence is uninformative in general. The thesis notes short trajectories (Section 3.11.4); the conclusion should keep this caveat next to the finding.

## 5. Results and statistical interpretation

**Numerical consistency.**
- 498 printed cells match a recomputation from raw records (0 mismatches).
- The preservation check confirms that no number changed in Stage 1.
- The headline values are consistent across abstract, chapters and conclusion: 11 of 2,979, 105 of 334, 661 of 672, 0 of 2,979 and 154 of 334.

**Interpretation is appropriately cautious.**
- "Significant" is not used without a test.
- The confirmatory GO is described as the outcome of a decision rule, not a non-inferiority test.
- Unresolved intervals are called unresolved.

**Points that need attention:**
- **Units in nearby statements.** "33 of 180 state-changing steps" (observe-only, Section 4.6.2) and "33 of 178 authorized calls" (replay) are different units with the same numerator. A reader can confuse them; a one-line note would help (Category C, wording only).
- **Security significance against statistical resolution.** All residual attacks of the restrictive arms lie in one ambiguous user task. The thesis states this, but a journal paper should lead with it, because it reduces most security comparisons to a single task.
- **Practical significance.** A benign-task completion of 31% against 52% undefended, and 4 of 89 legitimate transfers released, is the practically decisive result. It is reported, and it should stay prominent.

## 6. Ablation study

- **Labels and interpretations agree** across Section 4.5.5 (Table 4.25), Tables 4.26–4.31, Figures 4.5–4.8 and the discussion. This was verified in the previous review; the figures were regenerated with the Table 4.25 labels.
- **The distinctions requested are kept:**
  - full-layer ablation (Mitigation only);
  - component-level ablation (Decision Engine);
  - evidence-group removal (Detection, Behavioral Analysis);
  - shadow-mode evaluation (A5).
- **Scientific value:** high for locating REM's protection in the learned decision acting through enforcement, and for showing that calibration, Modify, the predicates and the context indicator change no outcome on these data.
- **Additional test that is genuinely needed:** a replay sweep over the declared costs (see 4.1). It would show whether any cost setting attains rule-level utility with REM's security. Without it, the claim "the learned decision causes most false blocking" is conditional on the declared costs.

## 7. Comparison with existing frameworks

- **Kinds of evidence are kept distinct and labeled:** replay with the framework's own code (Progent), recorded closed-loop runs (the distributed defenses), scripted integration (DRIFT, MELON), and architecture and code (DRIFT, MELON).
- **Benchmark-specific conditions are disclosed.** Progent's allow-list contains benchmark payees and excludes the attacker account by construction.
- **No superiority claim is made**, and differences in conditions (versions, agent architecture, replay against closed-loop) are listed in Section 4.4.8.
- **One correction was made (Category B):** a sentence said that Progent's upstream checker "was not executed", which was true only of the earlier extension study. Section 4.4.7 reports that the checker was executed on 22 November 2026 and gave the same counts. The sentence is now scoped to that study.

## 8. Discussion and conclusions

- **The discussion explains why results occurred:**
  - over-blocking from the cost thresholds and the base probability of first transfers;
  - the behavioral features' firing rates on legitimate steps;
  - provenance carrying discrimination;
  - shadow mode.
- **It relates findings to prior work:** C. Zhang et al. on calibration and control, AgentBoundary on over-defense, and Kekatos et al. on provenance.
- **Negative findings are discussed rather than hidden.**
- **The conclusion answers the RQs within the evidence (Table 5.1).** RQ3 (residual success after Modify) can be answered only trivially under NO-ADAPT, and the thesis says so.
- **No overgeneralization was found** in the revised text.

## 9. Corrections made in Stage 3

| Category | Count | Content |
|---|---:|---|
| A (editorial) | 117 | Sentence splitting, list conversion, em-dash removal, two captions, ambiguous self-references, the count of followed-up ablations in Section 4.5.7 |
| B (evidence-based) | 1 | Scope of "the upstream checking code was not executed" (Section 4.4.7), supported by Table 4.14 and the 22 November 2026 records (`REM_COMPARATIVE_EVALUATION_PHASE/results/`) |
| C (supervisor or new work) | see `05_UNRESOLVED_ISSUES_REPORT.md` | Not implemented |
