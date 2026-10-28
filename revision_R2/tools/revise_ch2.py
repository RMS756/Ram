"""Produce the R2 revision of Chapter 2 from thesis/CHAPTER2_LITERATURE_REVIEW.md.

Every edit is an exact replacement that must match once; the script stops
otherwise. The original file is not modified.
"""
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
src = open(os.path.join(ROOT, "thesis", "CHAPTER2_LITERATURE_REVIEW.md"), encoding="utf-8").read()
s = src
log = []


def rep(old, new, tag, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"[{tag}] expected {count} match(es), found {n}: {old[:80]!r}")
    s = s.replace(old, new)
    log.append(tag)


# --- E1/E2 review type --------------------------------------------------------
rep("# LITERATURE REVIEW: A SYSTEMATIC REVIEW OF RUNTIME SECURITY FOR TOOL-USING AI AGENTS",
    "# LITERATURE REVIEW: A RECORD-LEVEL SYSTEMATIC REVIEW OF RUNTIME SECURITY FOR TOOL-USING AI AGENTS", "E1 title")
rep("This version is a **systematic literature review with qualitative, structured evidence synthesis**. It follows PRISMA 2020 for reporting and PRISMA-S for the search.",
    "This version is a **systematic review conducted at record level, with qualitative, structured evidence synthesis**. The search, screening, eligibility assessment, quality appraisal and data extraction followed a predefined protocol and are reported following PRISMA 2020 and PRISMA-S. Full-text reports could not be retrieved, so eligibility, appraisal and extraction rest on records: titles, abstracts and index metadata. **No full-text screening was performed**, and the chapter does not claim the depth of a full-text systematic review.",
    "E2 review type")

# --- E3 remove project-status notes about RQs ---------------------------------
rep("The proposal does not state research questions. Chapter 3 (Section 3.1.3) derives four questions, RQ1–RQ4, from these objectives. They concern estimation, decision, mitigation and cost, and component contribution, and they remain marked as proposed ([PD]) pending supervisor confirmation. This inconsistency between the proposal and the chapters is recorded here as found. It is not resolved.",
    "The proposal does not state research questions. Chapter 3 (Section 3.1.3) derives four questions, RQ1–RQ4, from these objectives. They concern estimation, decision, mitigation and cost, and component contribution.",
    "E3 RQ note")
rep("**Review questions.** The review is designed to supply the literature basis that O1–O3, and RQ1–RQ4 once confirmed, require.",
    "**Review questions.** The review is designed to supply the literature basis that O1–O3 and RQ1–RQ4 require.", "E3b")
rep("| O1; RQ1, RQ2 and RQ4 [PD] |", "| O1; RQ1, RQ2 and RQ4 |", "E3c")

# --- E4 PRISMA table: records / reports / studies -----------------------------
rep("""| Stage | Databases (OpenAlex) | Other methods |
|---|---:|---:|
| Records identified | 320 | 70 |
| Duplicates removed before screening | 101 | 11 (same study as a database record) |
| Records screened (title/abstract) | 219 | — |
| Records excluded at screening | 174 | — |
| Reports sought / full text not retrieved | 45 / 45 | 59 / 59 |
| Reports assessed for eligibility (record level) | 45 | 59 |
| Reports excluded at eligibility | 5 | 28 (6 background, 21 foundational/methodological, 1 withdrawn) |
| **Studies included** | **40** | **31** |
| **Total included studies** | **71** | |""",
"""| Stage | Unit | Databases (OpenAlex) | Other methods |
|---|---|---:|---:|
| Identified | records | 320 | 70 |
| Removed before screening (duplicates; same study as a database record) | records | 101 | 11 |
| Screened (title/abstract) | records | 219 | — |
| Excluded at screening | records | 174 | — |
| Sought for retrieval (full text) | reports | 45 | 59 |
| **Not retrieved** (network policy) | reports | **45** | **59** |
| Assessed for eligibility **at record level** (no full-text report available) | records | 45 | 59 |
| Excluded at eligibility | records | 5 | 28 (6 background, 21 foundational/methodological, 1 withdrawn) |
| **Included** | **studies** | **40** | **31** |
| **Total included studies** (each represented by its index record) | studies | **71** | |""",
    "E4 PRISMA table")
rep("""**Full texts were not retrieved.** The network policy that blocked the databases also blocked publisher and preprint servers. Every report sought for retrieval was therefore assessed for eligibility on **record-level evidence**: title, abstract, indexed metadata, Crossref metadata and, for two records without an indexed abstract (VIGIL and R-Judge), the abstract text returned by a web search. This departure from standard practice is shown explicitly in the PRISMA flow diagram (Figure 2.1).""",
"""**Full texts were not retrieved.** The network policy that blocked the databases also blocked publisher and preprint servers. All 104 reports sought for retrieval (45 database, 59 other-methods) were therefore *not retrieved*, and eligibility was assessed on **records**: title, abstract, indexed metadata, Crossref metadata and, for two records without an indexed abstract (VIGIL and R-Judge), the abstract text returned by a web search. PRISMA 2020 distinguishes records, reports and studies; in this review each included study is represented by a single index record, and no full-text report was assessed. This departure from standard practice is shown in the PRISMA flow diagram (Figure 2.1). A supplementary check on 28 October 2026 (Section 2.13.4) re-examined the records of the closest studies; it did not add full texts.""",
    "E4b full texts")

# --- E5 Figure 2.1 duplicate caption ------------------------------------------
rep("""![Figure 2.1. PRISMA 2020 flow diagram of study identification, screening and inclusion. All counts are computed from the screening log.](CHAPTER2_PRISMA_FLOW_DIAGRAM.png)

**Figure 2.1.** PRISMA 2020 flow diagram. Counts are computed by script from the stored search output and the screening log.""",
"""![Figure 2.1. PRISMA 2020 flow diagram of the record-level review. Full-text reports were sought but not retrieved; eligibility was assessed on records. Counts are computed by script from the stored search output and the screening log.](revision_R2/figures/fig2_1_prisma_r2.png){width=88%}""",
    "E5 figure caption")

# --- E6 appraisal labels: quality vs information available --------------------
rep("""**Categories.** No numeric score is computed. A fixed, published rule assigns each study to a category:

- **HIGH EVIDENCE:** peer reviewed, with benchmark, figures and comparator all reported;
- **MODERATE EVIDENCE:** quantitative results in a peer-reviewed or clearly labelled preprint record, or a peer-reviewed evaluation without verifiable figures;
- **LIMITED EVIDENCE:** everything else.""",
"""**Categories.** No numeric score is computed. A fixed, published rule assigns each study to a category of **record-visible evidence**:

- **HIGH EVIDENCE:** peer reviewed, with benchmark, figures and comparator all reported in the record;
- **MODERATE EVIDENCE:** quantitative results in a peer-reviewed or clearly labelled preprint record, or a peer-reviewed evaluation without verifiable figures;
- **LIMITED EVIDENCE:** everything else.

These categories describe **how much evidence the record makes visible**, which depends on how much information could be accessed. They are not a judgement of the study's intrinsic quality: a rigorous study with a terse abstract can fall into LIMITED EVIDENCE, and a full-text appraisal could move it.""",
    "E6 categories")
rep("""**Override.** One override is applied and documented. FinHarness is set to LIMITED EVIDENCE because all of its figures were measured on a withdrawn benchmark.""",
"""**Override.** One override is applied and documented. FinHarness is set to LIMITED EVIDENCE because all of its figures were measured on FinVault, whose preprint was recorded on 25 September 2026 as withdrawn by its authors with a comment citing legal, intellectual-property and affiliation reasons rather than a scientific error. The withdrawal does not show that FinHarness's measurements are wrong; it means they cannot be confirmed against a publicly maintained benchmark. The override reflects confirmability, not invalidity (Section 2.10.2).""",
    "E6 override")
rep("""- 62 are FULLY VERIFIED and 9 PARTIALLY VERIFIED. The metadata and cited contribution of each study were checked against its record. PARTIALLY VERIFIED means that some cited detail rests only on search-engine text.""",
"""- 62 are RECORD-VERIFIED and 9 PARTLY UNVERIFIED. RECORD-VERIFIED means that the bibliographic metadata and the cited contribution were checked against the study's index record (title, abstract, metadata); it does **not** mean that the full text was read. PARTLY UNVERIFIED means that at least one cited detail rests only on search-engine excerpts and is unverified.""",
    "E6 verification labels")
rep("""**What the categories measure.** Because full texts were unavailable, the categories measure **how much of each study's evidence could be verified from its record**, not the study's intrinsic quality (`CHAPTER2_QUALITY_APPRAISAL.md`). Items that depend on the full text (Q4 reproducibility, Q7 comparators, Q8 limitations) are most often Not Verified.""",
"""**Levels of claim verification.** Every claim this chapter makes about a study is at one of four levels:

| Level | Meaning |
|---|---|
| **M** — metadata verified | Title, authors, venue and year checked against Crossref or the index record |
| **A** — abstract-supported | The claim is stated in the study's abstract as indexed |
| **F** — full-text verified | The claim was checked against the full text |
| **U** — unverified | The claim rests on search-engine excerpts or an earlier reading that could not be reproduced |

**No claim in this chapter is at level F**, because no full text was retrieved. Claims at level U are marked "(unverified)" where they are used.

**What the categories measure.** Because full texts were unavailable, the categories measure **how much of each study's evidence could be verified from its record**, not the study's intrinsic quality (`CHAPTER2_QUALITY_APPRAISAL.md`). Items that depend on the full text (Q4 reproducibility, Q7 comparators, Q8 limitations) are most often Not Verified.""",
    "E6 levels")
rep("""**Coding values.** Each property is coded **Yes**, **No**, **Not Reported**, **Not Applicable** or **Not Verified**. "Yes" is never entered for a property that is merely absent from the record.""",
"""**Coding values.** Each property is coded **Yes**, **No**, **Not Reported**, **Not Applicable** or **Not Verified**. "Yes" is never entered for a property that is merely absent from the record. Conversely, **Not Reported is not evidence of absence**: a property that the record does not mention may still be present in the system. Counts of "Not Reported" cells therefore describe the records, not the systems, and are never used in this chapter to argue that a capability is missing from the literature.""",
    "E7 NR")
rep("Every included study also carries a verification label, FULLY VERIFIED or PARTIALLY VERIFIED, following the thesis rule that search-engine text cannot settle a primary claim.",
    "Every included study also carries a verification label, RECORD-VERIFIED or PARTLY UNVERIFIED, following the thesis rule that search-engine text cannot settle a primary claim.",
    "E6b")

# --- E8 step-level vs history -------------------------------------------------
rep("""Runtime monitors differ in the temporal scope of their judgment.

**Step-level monitors** judge each proposed action in its current context. Examples are Progent, AgentSpec, Task Shield, ProvenanceGuard and VIGIL. They are fast and interpretable, but by construction they cannot see an attack whose individual steps are each acceptable.""",
"""Runtime monitors differ along two dimensions that are easily conflated: **decision granularity** (whether a decision is taken for each proposed step, for a plan, or for an episode) and **evidence scope** (whether that decision uses only the current step or also the history that led to it). A step-level decision can be history-aware: it can be taken for each proposed call while conditioning on the episode so far.

**Step-level monitors with current-step evidence** judge each proposed action against a policy or the current context. Examples are Progent and AgentSpec. They are fast and interpretable, but a monitor that uses no history cannot see an attack whose individual steps are each acceptable.

**Step-level monitors with history-aware evidence** still decide per proposed action, but their evidence includes earlier context. Task Shield, ProvenanceGuard and VIGIL check a proposed call against the user's goal or against evidence accumulated in the context; REM (Chapter 3) belongs to this group, because its per-step features include repeated calls, privilege escalation, transition deviation and argument provenance computed over the episode.""",
    "E8 step-level")
rep("**Accumulating monitors** sit between the two.", "**Accumulating monitors** keep an explicit running state across steps.", "E8b")

# --- E9 AgentTrust verification levels ----------------------------------------
rep("""**Architecture and verdicts (verified at abstract level).** AgentTrust intercepts agent tool calls *before execution* and returns one of four verdicts: allow, warn, block or review. Its components are:

- a normalizer that deobfuscates shell input;
- an analyzer with 42 risk patterns;
- a policy engine with 170 rules;
- a SafeFix engine that proposes safer alternatives;
- a session tracker (RiskChain) with seven order-aware chain detectors;
- an LLM judge for ambiguous cases.

**Results (abstract level).** On its 300-scenario internal benchmark, a production-only rule set reached 95.0% verdict accuracy and 73.7% risk-level accuracy. On 630 external adversarial scenarios, the author reports 96.7% under a *patched* rule set, explicitly not zero-shot.

**Partially verified details.** The following could be confirmed only through search-engine excerpts:""",
"""**Architecture and verdicts (level A).** AgentTrust intercepts agent tool calls *before execution* and returns one of four verdicts: allow, warn, block or review. Its abstract names a shell deobfuscation normalizer, SafeFix suggestions of safer alternatives, RiskChain detection of multi-step attack chains, and a cache-aware LLM judge for ambiguous inputs.

**Results (level A).** On its 300-scenario internal benchmark, a production-only rule set reached 95.0% verdict accuracy and 73.7% risk-level accuracy. On 630 independently constructed adversarial scenarios, the author reports 96.7% under a *patched* rule set, explicitly not zero-shot.

**Unverified details (level U).** The following rest on search-engine excerpts and are not stated in the abstract retrieved on 28 October 2026: an analyzer with 42 risk patterns; a policy engine with 170 rules; seven order-aware chain detectors; and""",
    "E9 AgentTrust")
rep("""AgentTrust (C. Yang, 2026; preprint; MODERATE EVIDENCE; PARTIALLY VERIFIED) is among the closest prior art to REM.""",
    """AgentTrust (C. Yang, 2026; preprint; MODERATE EVIDENCE; PARTLY UNVERIFIED) is among the closest prior art to REM.""", "E9b")

# --- E10 NEXUS verification levels --------------------------------------------
rep("""NEXUS (Hossain et al., 2026; preprint; MODERATE EVIDENCE; PARTIALLY VERIFIED) is the closest prior art to REM's *decision* component.""",
    """NEXUS (Hossain et al., 2026; preprint; MODERATE EVIDENCE; PARTLY UNVERIFIED) is the closest prior art to REM's *decision* component.""", "E10a")
rep("""**Architecture (verified at abstract level).** NEXUS is a structured-plan safety monitor. It evaluates the plan an agent proposes *before execution* and selects among allow, block, request confirmation and request revision. It combines four components:

- deterministic rules;
- argument-level inspection;
- a logistic-regression risk score for graded escalation;
- a session manager for cross-turn state.

**Results (abstract level).** On a 128-instance held-out synthetic benchmark it reports:

- F1 of 0.949;
- four-class intervention accuracy of 0.6406, 27.3 percentage points above rule-only selection;
- median latency of 0.205 ms.

**Partially verified details.** The following could be confirmed only through search-engine excerpts:

- **Calibration.** Platt scaling reduced ECE from 0.085 to 0.013; isotonic regression was also evaluated.
- **Expected-loss objective.** The objective uses *fixed* intervention costs (0 allow, 0.1 revise, 0.3 confirm, 1 block) to set loss-optimal thresholds on the calibrated score.
- **Deployed policy.** The policy is a rule-first cascade. Multiple critical violations always block. With one critical violation the score decides between block and confirm. Otherwise, threshold crossings route plans to confirmation. With no rule firing, the policy has no signal for revision.
- **Consequence features.** Each planned tool call carries side-effect, irreversibility, sensitivity, permission and cost annotations, which the rules use.
- **Evaluation caveats.** The authors call the in-distribution results on their templates upper bounds. They report out-of-distribution F1 of 0.861 on R-Judge and 0.881 on a stress set.""",
"""**Architecture (level A).** NEXUS is a structured-plan safety monitor that "applies a formal intervention policy" to select among allow, block, request confirmation and request revision. It combines deterministic safety rules, argument-level inspection and a *calibrated* logistic-regression risk score used for graded escalation.

**Results (level A).** On a 128-instance synthetic benchmark it reports F1 of 0.949 and four-class intervention accuracy of 0.6406, 27.3 percentage points above rule-only selection. On R-Judge it reports F1 0.861 against 0.849 for rule-only; it matches rule-only on AgentHarm; it reports 0% ASR at 99% control allow on an indirect-injection set; F1 0.881 on its rule-blind stress set; and a median latency of 0.205 ms.

**Unverified details (level U).** The following rest on search-engine excerpts or on an earlier reading of the paper that could not be reproduced in the review environment:

- **Calibration figures.** Platt scaling reducing ECE from 0.085 to 0.013; isotonic regression also evaluated.
- **Expected-loss objective.** *Fixed* intervention costs (0 allow, 0.1 revise, 0.3 confirm, 1 block) setting loss-optimal thresholds on the calibrated score.
- **Deployed policy.** A rule-first cascade in which the score decides between block and confirm only in some rule states.
- **Consequence features.** Side-effect, irreversibility, sensitivity, permission and cost annotations on each planned tool call, used by the rules.
- **Session state.** A session manager for cross-turn state.""",
    "E10 NEXUS")
rep("""**What REM cannot claim.** NEXUS already provides:

- calibrated logistic risk scoring;
- a four-way intervention set with confirmation and revision routes;
- consequence information in its plan representation and rules;
- an expected-loss formulation with loss-optimal thresholds;
- sub-millisecond latency.

**Where the difference lies.** The defensible differences are:

- **Point of evaluation.** REM evaluates each proposed tool call during execution, not a pre-execution plan.
- **Threat model and setting.** REM addresses indirect injection in an executable banking environment, not synthetic plan templates.
- **Decision rule.** REM minimizes conditional expected loss per step, with losses indexed by each action's declared consequence tier. NEXUS uses fixed intervention costs to set thresholds inside a rule-first cascade.

Whether these differences change outcomes is an empirical question.""",
"""**What REM cannot claim.** NEXUS already provides (level A) calibrated logistic risk scoring, a formal policy over a four-way intervention set with confirmation and revision routes, and sub-millisecond latency; and, if the level-U description is accurate, consequence annotations used by rules and an expected-loss formulation with loss-optimal thresholds.

**Where the difference lies.** Two differences rest on level-A evidence:

- **Point of evaluation.** REM evaluates each proposed tool call during execution; NEXUS is described as a structured-*plan* monitor.
- **Threat model and setting.** REM is evaluated on indirect injection in an executable banking environment; NEXUS's headline results are on a synthetic benchmark, with R-Judge, AgentHarm and an indirect-injection set as additional evaluations.

A third difference, in the decision rule (per-step expected loss with tier-indexed losses in REM; fixed intervention costs inside a rule-first cascade in NEXUS), rests on level-U evidence and must be checked against the full text before it is relied on. Whether any of these differences changes outcomes is an empirical question.""",
    "E10 NEXUS diff")

# --- E11 SafeAgent ------------------------------------------------------------
rep("- SafeAgent realizes consequence modeling and arbitration through LLM reasoning (H. Liu et al., 2026; PARTIALLY VERIFIED).",
    "- SafeAgent's decision core instantiates operators for risk encoding, utility-cost evaluation, consequence modeling and policy arbitration over persistent session state (H. Liu et al., 2026; level A). Whether these operators are realized through LLM reasoning is unverified (level U).",
    "E11 SafeAgent")

# --- E12 remove project notes from synthesis ----------------------------------
rep("""REM's evaluation must report intervention rates and benign utility beside attack success. The operational semantics of Modify and Block, and tie-breaking between verdicts of equal expected loss, are specified in Chapter 3. Two conflicts there remain open and are marked SUPERVISOR DECISION REQUIRED:
  - **SC-1:** episode-level versus step-level mitigation semantics;
  - **SC-2:** the tie-breaking order versus the prototype's VerdictTieError.""",
"""REM's evaluation must report intervention rates and benign utility beside attack success. Because the meaning of Modify and Block differs across studies, Chapter 3 specifies their operational semantics and evaluates both a step-level and an episode-level reading.""",
    "E12 SC notes")

# --- E13 FinVault / FinHarness -----------------------------------------------
rep("""All of these figures were measured on **FinVault**, whose arXiv version has been **withdrawn** by its authors (Z. Yang et al., 2026). FinVault is mentioned only to record that withdrawal. FinHarness's figures are therefore not treated as affirmative evidence, and FinHarness is appraised LIMITED EVIDENCE by override.""",
"""All of these figures were measured on **FinVault** (Z. Yang et al., 2026). The review record of 25 September 2026 notes that FinVault's arXiv preprint was **withdrawn by its authors**, with a comment citing legal, intellectual-property and affiliation reasons rather than an error in the benchmark; its OpenAlex record carries no retraction flag, and the withdrawal notice could not be re-checked on 28 October 2026 because arXiv was unreachable. A withdrawal for non-scientific reasons does not invalidate measurements made on the benchmark. It does mean that FinHarness's figures cannot be confirmed against a publicly maintained version, so they are reported as author-reported results with that caveat, and FinHarness is appraised LIMITED EVIDENCE by override.""",
    "E13 FinVault")
s = s.replace("The only quantitative financial runtime results rest on a withdrawn benchmark.",
              "The only quantitative financial runtime results were measured on a benchmark whose preprint was withdrawn for non-scientific reasons, and cannot be independently confirmed.")
s = s.replace("key figures rest on a withdrawn benchmark", "key figures were measured on a benchmark withdrawn for non-scientific reasons and cannot be confirmed")
s = s.replace("financial focus in a judge cascade evaluated on a withdrawn benchmark (FinHarness).",
              "financial focus in a judge cascade evaluated on a benchmark that is no longer publicly maintained (FinHarness).")
s = s.replace("the only quantitative runtime results rest on a withdrawn benchmark;", "the only quantitative runtime results cannot be confirmed against a maintained benchmark;")
s = s.replace("One source (FinVault) has been withdrawn. Preprint results may change or be withdrawn.",
              "One source (FinVault) was recorded as withdrawn by its authors for non-scientific reasons. Preprint results may change or be withdrawn.")
s = s.replace("All financial-context evidence is LIMITED, and the only quantitative financial runtime results rest on a withdrawn benchmark.",
              "All financial-context evidence is LIMITED, and the only quantitative financial runtime results cannot be confirmed against a maintained benchmark.")
s = s.replace("| Yes (benign approval; withdrawn benchmark) |", "| Yes (benign approval; benchmark withdrawn for non-scientific reasons) |")
log.append("E13 withdrawn wording (global)")

# --- E14 move Table 2.8 to appendix -------------------------------------------
start = s.index("**Table 2.8. Comparative evidence for included defense and design studies (n = 42)**")
end = s.index("**Table 2.9. Decision mechanism, calibration, consequence and reported evaluation dimensions")
table28 = s[start:end].rstrip()
s = s[:start] + ("**Table 2.8** (42 defense and design studies × 13 properties) is reproduced in **Appendix 2A**. "
                 "In summary: 41 of the 42 studies operate at runtime, 34 code tool/action evidence, 21 multi-step handling, "
                 "17 behavioral evidence and 8 provenance evidence as present in the record; these counts describe what the "
                 "records report (Section 2.2.7), not what the systems lack.\n\n") + s[end:]
log.append("E14 Table 2.8 to Appendix 2A")
rep("- **Table 2.8** records what each study observes and does, using the columns specified in the review protocol.",
    "- **Table 2.8** (Appendix 2A) records what each study observes and does, using the columns specified in the review protocol.", "E14b")
rep("| **REM (investigated in this thesis; not a result)** | Calibrated per-step probability with consequence-tier losses in an expected-loss rule (Chapter 3) | Designed | Designed (declared tiers) | Designed (Escalate; Modify) | Planned | Planned | Planned (AgentDojo Banking) | — |",
    "| **REM (this thesis; design, Chapter 3)** | Calibrated per-step probability with consequence-tier losses in an expected-loss rule | Designed | Designed (declared tiers) | Designed (Escalate; Modify) | Exploratory evaluation (Chapter 5) | Measured (Chapter 5) | AgentDojo Banking | — |",
    "E14c REM row")
rep("*PV = figure or property PARTIALLY VERIFIED (search-engine excerpt only).*",
    "*PV = figure or property unverified (level U: search-engine excerpt only).*", "E14d")
rep("""- **No included study** reports all three of the following together:
  - a calibrated probability of adversarial induction per proposed tool call;
  - consequence-dependent losses used to select among graduated responses;
  - evaluation on an executable financial environment with utility, intervention behavior and latency reported.""",
"""- **No included record** reports all three of the following together:
  - a calibrated probability of adversarial induction per proposed tool call;
  - consequence-dependent losses used to select among graduated responses;
  - evaluation on an executable financial environment with utility, intervention behavior and latency reported.

  This observation concerns the *records* examined. A combination this specific is easy to miss in a record-level review and is weak evidence of originality on its own (Section 2.13.2).""",
    "E14e")

# --- E15 citations: ProvenanceGuard ASE; Zhang title --------------------------
pg_old = re.search(r"She, Y\., Liang, Y\., & Kang, E\. \(2026\)\.[^\n]*", s)
if not pg_old:
    raise SystemExit("ProvenanceGuard reference not found")
s = s.replace(pg_old.group(0),
              "She, Y., Liang, Y., & Kang, E. (2026). Safeguarding LLM agents from misalignment through provenance analysis. "
              "In *Proceedings of the 41st IEEE/ACM International Conference on Automated Software Engineering* (pp. 3036–3048). "
              "ACM. https://doi.org/10.1145/3832783.3837535 (earlier preprint: arXiv:2607.01236)")
log.append("E15 ProvenanceGuard ASE")
zh = re.search(r"Zhang, C\., Wan, Z\.[^\n]*", s)
if zh:
    s = s.replace(zh.group(0),
                  "Zhang, C., Wan, Z., Yu, X., Wu, J., Wen, Q., Zhou, P., Zhao, W., & Tsang, I. (2026). *Calibration is not control: "
                  "Intervention value for LLM-agent oversight* (arXiv:2606.21399) [Preprint]. arXiv. https://arxiv.org/abs/2606.21399 "
                  "(title as indexed on 28 Oct 2026; an earlier version was titled \"Calibration is not control: Why LLM-agent oversight needs intervention\")")
    log.append("E15 Zhang title")

# --- E16 gap: constrain to examined evidence ----------------------------------
rep("""| **A. Integration.** Capabilities exist across separate approaches | Tables 2.8–2.9: calibrated scoring (NEXUS), consequence pricing (H.-H. Chen), provenance (ProvenanceGuard; MCP policy-enforcement point), graduated verdicts (AgentTrust; LATTICE) are in different studies | NEXUS combines calibration, costs and graduated responses, at the plan level | **Retained, narrowed.** The integration not reported is a calibrated per-call probability of adversarial induction combined with consequence-indexed losses at the action boundary of an executing agent |""",
"""| **A. Integration.** Capabilities exist across separate approaches | Tables 2.8–2.9: calibrated scoring (NEXUS), consequence pricing (H.-H. Chen), provenance (ProvenanceGuard; MCP policy-enforcement point), graduated verdicts (AgentTrust; LATTICE) are in different studies | NEXUS combines calibration and graduated responses (level A) and, per level-U evidence, costs, at the plan level | **Retained only as a weak, record-bounded observation.** A calibrated per-call probability combined with consequence-indexed losses at the action boundary was not reported in the examined records. Because the combination is specific and the review is record-level, its absence is not treated as evidence of originality |""",
    "E16 gap A")
rep("""> Among the 71 studies included in this systematic review (search date 25 September 2026), none reports an empirical evaluation of a non-invasive runtime layer for a financial tool-using agent that combines (i) provenance-based evidence about proposed financial actions, (ii) a calibrated per-step probability that the proposed action is adversarially induced, (iii) a decision that minimizes expected loss over Allow, Modify, Escalate and Block using losses declared per consequence tier, and (iv) deterministic mitigation whose effectiveness is measured and used in the loss structure. None reports attack success, benign utility, utility under attack, intervention behavior and latency separately, with calibration reported separately from control outcomes, and results compared against a consequence-independent baseline that uses the same estimator.

**Nature of the gap.** The gap is **integrative and empirical**. It concerns the combination and evaluation of established mechanisms under indirect prompt injection, in a financial setting. It does not concern the absence of any single mechanism, and it does not concern a new learning algorithm.""",
"""> The gap supported by the examined evidence is **empirical**. In the records of the 71 included studies (search date 25 September 2026), the review found (a) limited and conflicting evidence on whether behavioral and provenance evidence improves runtime decisions, and none testing it as input to a calibrated estimator for financial actions (Gap C); (b) no verified quantitative evaluation of a runtime defense on financial actions in an open, executable benchmark (Gap D); and (c) no evaluation that compares a consequence-aware decision with a consequence-independent baseline sharing the same estimator, while reporting attack success, benign utility, intervention behavior, calibration and latency separately (Gap E).

**Nature of the gap.** The gap concerns *evidence*: how established mechanisms behave when combined at the action boundary of a financial agent under indirect prompt injection, measured against a baseline that isolates the decision rule. It does not concern the absence of any single mechanism, and it does not concern a new learning algorithm. The specific combination that REM implements (Gap A) was not found in the examined records, but the thesis does not rest its originality on that absence: a combination this specific is easy to miss in a record-level review, and closely related designs exist (NEXUS, AgentTrust, SafeAgent).""",
    "E16 gap statement")
rep("**Bounds.** The gap is bounded by the search, which covered one database with a retrieval cap and a partly non-independent other-methods stream. It is also bounded by record-level appraisal (Section 2.13.4).",
    "**Bounds.** The gap is bounded by the search, which covered one database with a retrieval cap and a partly non-independent other-methods stream. It is also bounded by record-level appraisal: no study was read in full, and several properties of the closest studies are unverified (Section 2.13.4).",
    "E16b")
rep("| **Combination of (i)–(iv) in Section 2.13.2 at the action boundary, under indirect injection, on an open executable banking benchmark** | Not reported among the 71 included studies | **Proposed by this thesis (integrative)** |",
    "| **Combination of provenance evidence, a calibrated per-step probability, tier-indexed expected-loss verdicts and deterministic mitigation at the action boundary, on an open executable banking benchmark** | Not reported in the examined records (record-level; weak evidence of absence) | **Proposed by this thesis (integrative design)** |",
    "E16c")
rep("| **Evaluation that separates attack success, benign utility, intervention behavior, calibration and latency, against a consequence-independent baseline with the same estimator** | Not reported among the 71 included studies | **Proposed by this thesis (empirical)** |",
    "| **Evaluation that separates attack success, benign utility, intervention behavior, calibration and latency, against a consequence-independent baseline with the same estimator** | Not reported in the examined records | **Proposed by this thesis (empirical)** |",
    "E16d")

# --- E21 remove duplicated relation sections in 2.13.3 ------------------------
start = s.index("**Relation to AgentTrust.** AgentTrust already provides:")
end = s.index("**Relation to other close studies.**")
s = s[:start] + ("**Relation to AgentTrust and NEXUS.** What REM cannot claim against AgentTrust and NEXUS, and the narrower "
                 "differences that remain, are set out in Sections 2.9.2 and 2.9.3 and are not repeated here. Several of "
                 "the properties on which those differences rest are unverified (level U).\n\n") + s[end:]
log.append("E21 dedupe relations")
start = s.index("**Open design conflicts.** The operational semantics of Modify and Block")
end = s.index("### 2.13.4 Limitations of this review")
s = s[:start] + s[end:]
log.append("E12b remove open-conflict notes")

# --- E17 limitations ----------------------------------------------------------
rep("4. **No full texts.** Eligibility, extraction and appraisal were performed on record-level evidence. Nine included studies are PARTIALLY VERIFIED. Appraisal items that depend on full text (reproducibility, comparators, limitations) are mostly Not Verified.",
    "4. **No full texts.** Eligibility, extraction and appraisal were performed on records; no full-text screening was performed and no claim is at level F. Nine included studies are PARTLY UNVERIFIED. Appraisal items that depend on full text (reproducibility, comparators, limitations) are mostly Not Verified. A supplementary record check on 28 October 2026 re-examined the closest studies (NEXUS, AgentTrust, ProvenanceGuard, FinHarness, FinVault, SafeAgent, C. Zhang et al., H.-H. Chen): it found a peer-reviewed version of ProvenanceGuard (ASE 2026), a changed title for C. Zhang et al., and several details of NEXUS and AgentTrust that are not supported by their current abstracts, which are now marked level U. Full texts remained unreachable.",
    "E17 limitations")

# --- E18 summary --------------------------------------------------------------
rep("This chapter reported a systematic literature review, following PRISMA 2020 and PRISMA-S, of runtime security for tool-using AI agents, with attention to financial execution.",
    "This chapter reported a record-level systematic review, reported following PRISMA 2020 and PRISMA-S, of runtime security for tool-using AI agents, with attention to financial execution. Full texts were not retrieved, so its findings rest on records.",
    "E18a")
rep("**The gap.** The research gap is accordingly **integrative and empirical**. It concerns the evaluation, on an open, executable banking benchmark, of a runtime layer that combines:",
    "**The gap.** The research gap supported by the examined records is **empirical**: it concerns the evaluation, on an open, executable banking benchmark, of a runtime layer that combines:",
    "E18b")
rep("Chapter 3 specifies the REM methodology through which the gap is addressed. SC-1 and SC-2 remain open, pending supervisor decision.",
    "Chapter 3 specifies the REM methodology through which the gap is addressed.", "E18c")
rep("Of these, 10 are HIGH, 36 MODERATE and 25 LIMITED EVIDENCE.",
    "Of these, 10 are HIGH, 36 MODERATE and 25 LIMITED record-visible evidence.", "E18d")

# --- Appendix 2A --------------------------------------------------------------
refs_at = s.index("\n## References")
appendix = ("\n\n---\n\n## Appendix 2A. Comparative Evidence Matrix of Defense and Design Studies\n\n"
            "Coding as in Section 2.11: Yes = reported in the verified record; NR = Not Reported (not evidence of absence); "
            "NV = Not Verified; NA = Not Applicable. Evidence levels refer to record-visible evidence (Section 2.2.6).\n\n"
            + table28 + "\n")
s = s[:refs_at] + appendix + s[refs_at:]
log.append("Appendix 2A added")

# drop the "Table: " duplicate-caption style if any, normalise Figure references
out = os.path.join(ROOT, "revision_R2", "chapters_md", "CHAPTER2_LITERATURE_REVIEW_R2.md")
open(out, "w", encoding="utf-8").write(s)
print(len(log), "edits;", len(src.split()), "->", len(s.split()), "words")
print("\n".join(log))
