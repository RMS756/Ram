# REM final research-gap decision memo

**Status:** `[PROPOSED — SUPERVISOR APPROVAL REQUIRED]`. Date: 11 November 2026. This memo decides the gap wording before the thesis is revised. It is not a novelty claim.

## 1. Evidence base and its limits

| Source | Reading level |
|---|---|
| PROVISO, AgentBoundary, Calibration Is Not Control, CASEL, Task Shield, MELON | **Full text** (PDFs supplied by the candidate; hashes in `REM_Authorization_Generalization_Study/papers_provided/SHA256SUMS.txt`) |
| NEXUS (Findings of AACL 2026) | **Abstract and the authors' repository README** (stored copy, retrieved 1 November); paper not read |
| aiAuthZ (arXiv:2607.05518), Kairos (arXiv:2610.18457), "Approve What, Exactly?" (arXiv:2610.21063), SentryBench (arXiv:2610.34535), DelegationBench (arXiv:2610.05532) | **Abstract and index record only.** `arxiv.org` and `aclanthology.org` are blocked in this session. No claim about their equations, algorithms or limitations is made beyond their abstracts. |
| Original systematic review (search closed October 2026) | Record level, as documented in Chapter 2 |

No systematic search to 11 November was possible. Newer competing work may exist.

## 2. The candidate formulation

> Limited controlled empirical evidence establishes whether learned, consequence-aware runtime security decisions provide additional value over simpler authorization and provenance controls for financial tool-using agents under unseen user tasks and prompt-injection objectives, while preserving legitimate high-consequence task completion.

| Test | Verdict | Reason |
|---|---|---|
| Supported by recent literature | **Yes, with one caveat** | PROVISO states that its controller is "fitted separately for each benchmark" and that transfer is not studied; it holds out user tasks, not attack objectives. AgentBoundary reports that "high safety frequently coexists with poor authorized-task completion". Calibration Is Not Control shows a calibrated risk score is not sufficient for intervention decisions. CASEL states that "Intervention effectiveness is assumed, not measured". None of the six full-text papers compares a learned monitor with parameter-free provenance or authorization rules on the same trajectories. Caveat: for NEXUS, aiAuthZ and Kairos this is known only at abstract level. |
| Distinct from already published work | **Yes, as an evidence gap; no, as a mechanism gap** | Calibrated risk scoring with graduated actions (NEXUS), per-mode consequence costs (CASEL), provenance-typed decisions (PROVISO), task-alignment authorization (Task Shield), argument-level authorization gateways (aiAuthZ) and the insufficiency of risk scores (Calibration Is Not Control) are all published. What is not published, among the works examined, is a controlled comparison of a learned consequence-aware monitor against simple rules under held-out user tasks and held-out attack objectives for a banking agent. |
| Sufficiently specific | **Yes** | Names the system class (runtime monitors without a language model in the decision path), the domain (banking tool-using agent), the comparison (learned consequence-aware decisions versus rule controls), and the conditions (unseen tasks and objectives; legitimate task completion). |
| Answerable through experiments | **Yes, and answered here** | Recorded-trace replay with injection-task folds, double holdout, and a confirmatory run on untouched recordings. |
| Scientifically falsifiable | **Yes** | "The learned policy adds value over rule P2 or A2" is a paired contrast with an interval. The data could have shown a clear advantage; they did not. |
| Consistent with the REM experiments | **Yes** | The answer is largely negative: on the confirmatory population the original REM is not better than the simple rules, and REM without behavioural evidence is not distinguishable from them (`REM_SECURITY_UTILITY_ANALYSIS.md`). The formulation asks a question and does not presuppose a favourable answer. |

One wording change is needed. "Preserving legitimate high-consequence task completion" must not be read as something REM achieves. It is a criterion on which every arm is measured.

## 3. Decision

**Adopt the candidate formulation, in this final form:**

> Runtime defences for tool-using agents now combine risk scoring, provenance and graduated interventions, and their authors report benchmark-specific fitting and unmeasured intervention effectiveness. Limited controlled evidence establishes whether a learned, consequence-aware runtime decision adds value over simple provenance and authorization rules for a banking agent when both the user task and the attack objective are unseen, and at what cost in legitimate task completion. This thesis supplies that evidence for one transparent monitor (REM) on recorded AgentDojo banking trajectories, including the negative results.

It supersedes the wording of the 3 November draft (Section 2.13.2 there), which framed the gap as the absence of a combined calibrated, consequence-aware, four-verdict mechanism. That framing is no longer defensible: NEXUS and CASEL publish the same structure.

## 4. What the gap licenses and what it does not

| Claim | Licensed? |
|---|---|
| A controlled evaluation, with held-out objectives and tasks and a pre-registered confirmatory run, of a learned consequence-aware monitor against rule baselines on a banking benchmark | Yes |
| A documented set of negative results (behavioural evidence; outcome-supervised intervention value; delegated-source rule; exact-string provenance under reformatting) | Yes |
| A novel decision algorithm | No |
| Superiority over NEXUS, MELON, Task Shield, PROVISO or aiAuthZ | No: none was run under the same conditions |
| A solution to authorization of financial actions | No: no arm separates an authorized payment from an unrequested one whose values occur in the user's words |
| Any statement about live agents or reviewers | No |

## 5. Dependence on missing full texts

The decision does not depend on details of NEXUS, aiAuthZ or Kairos. Whatever their full texts contain, they would narrow the mechanism space further, which the gap already concedes. They could weaken the evidence gap only if one of them reports a held-out-objective comparison of a learned monitor with rule baselines on banking tasks; their abstracts do not indicate this. The full texts are requested from the candidate so that the related-work statements can be upgraded from abstract level before submission.
