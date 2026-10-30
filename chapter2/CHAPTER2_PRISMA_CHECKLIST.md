# Chapter 2: PRISMA 2020 Checklist Mapping (with PRISMA-S notes)

**Scope.** This file maps the PRISMA 2020 checklist items to `CHAPTER2_SYSTEMATIC_REVIEW.md` for a thesis chapter.

**Status values:**
- **Yes:** the requirement is met by the process actually carried out.
- **Partial:** it is met with a stated limitation.
- **No:** it is not met.
- **Not Applicable:** the item does not apply (for example, meta-analysis items).

An item is marked Yes only when the underlying requirement was performed. Similar wording in the chapter is not sufficient.

| PRISMA Item | Requirement | Chapter Location | Evidence Present? | Notes |
|---|---|---|---|---|
| 1 Title | Identify the report as a systematic review | Chapter title | Yes | "A Systematic Review of Runtime Security for Tool-Using AI Agents" |
| 2 Abstract | Structured abstract (PRISMA for Abstracts) | — | No | A thesis chapter has no abstract. The thesis abstract, outside this chapter, should summarise the review. |
| 3 Rationale | Rationale in context of existing knowledge | §2.1 | Yes | Shift from model output to agent action; why runtime protection of financial agents needs review |
| 4 Objectives | Explicit objectives or questions | §2.2.1 | Yes | SRQ1–SRQ5 derived from approved objectives O1–O3. The thesis RQs are still [PD] (proposed). That inconsistency is recorded, not resolved. |
| 5 Eligibility criteria | Inclusion/exclusion criteria and grouping for synthesis | §2.2.4 | Yes | I1–I6 and the exclusion labels. The operational clarifications (the I1 LLM-integrated-application rule, the multi-agent-channel rule, the position-paper rule) are reported as fixed before eligibility assessment. They were articulated during screening, not in a registered protocol. |
| 6 Information sources | All databases and other sources, with dates | §2.2.2; Search Strategy §1 and §4 | Partial | One database searched (OpenAlex). Eleven named sources were DATABASE ACCESS UNAVAILABLE and are listed with the access-test log. |
| 7 Search strategy | Full search strategies for all databases | §2.2.3, Table 2.1; Search Strategy §3 | Yes | Exact strings, the strings as sent to the index, filters, pages and dates. Boolean blocks could not be run as Boolean because the interface does not support them. |
| 8 Selection process | Methods for deciding inclusion, number of reviewers, automation | §2.2.5; Screening Log | Partial | Single reviewer, no second screener; automated deduplication by DOI or normalized title. Eligibility was assessed on record-level evidence because full texts could not be retrieved. |
| 9 Data collection process | Methods for collecting data, number of reviewers, confirmation | §2.2.7; Evidence Matrix | Partial | Single reviewer. Data came from records and the prior verification register; authors were not contacted. |
| 10a Data items (outcomes) | Outcomes sought | §2.2.7 | Yes | Metrics, main result, attack success, utility, latency and calibration where reported |
| 10b Data items (other variables) | Other variables sought | §2.2.7 | Yes | 21 fields, including threat, entry point, runtime, context, behaviour, tool, multi-step, provenance, decision, mitigation, benchmark and financial context |
| 11 Study risk-of-bias assessment | Methods, tool, reviewers | §2.2.6; Quality Appraisal | Partial | Protocol checklist Q1–Q10 with a deterministic category rule. It is not a validated risk-of-bias tool, it was applied at record level, and there was a single appraiser. |
| 12 Effect measures | Effect measures used | §2.2.8 | Not Applicable | No effect measure is synthesised. Author-reported metrics are described per study. |
| 13a Synthesis methods (eligibility for synthesis) | Which studies went into each synthesis | §2.2.8; theme syntheses | Yes | All included studies contribute to the themes their extracted fields populate. Table 2.8 includes all 42 defense and design studies. |
| 13b Data preparation | Handling of missing data or conversions | §2.2.7 | Yes | Not Reported / Not Verified / Not Applicable codes; no imputation |
| 13c Tabulation/visual display | Methods to tabulate or display | §2.11 | Yes | Tables 2.3–2.12; Figure 2.1 |
| 13d Synthesis method | Method and rationale | §2.2.8 | Yes | Structured qualitative synthesis across 11 themes × 5 questions; meta-analysis rejected with reasons |
| 13e Heterogeneity exploration | Methods to explore heterogeneity | §2.2.8; §2.12 | Partial | Heterogeneity is described qualitatively ("what differs across studies") and not modelled statistically |
| 13f Sensitivity analyses | Sensitivity analyses | — | No | None performed. Findings are qualified by evidence level and verification status instead. |
| 14 Reporting bias assessment | Methods to assess bias from missing results | §2.13.4 (limitation 7) | Partial | Publication bias discussed qualitatively; no formal assessment |
| 15 Certainty assessment | Methods to assess certainty | §2.2.6; §2.2.8 | Partial | Evidence levels (HIGH/MODERATE/LIMITED) and verification status qualify claim strength. GRADE is not used. |
| 16a Study selection (results) | Numbers at each stage, with flow diagram | §2.2.5, Table 2.2, Figure 2.1 | Yes | Counts computed by script from stored output: 320 → 219 → 45 → 40, plus 31 via other methods = 71 |
| 16b Excluded studies | Studies that appeared eligible but were excluded, with reasons | §2.2.5; Screening Log | Yes | Five eligibility exclusions described with reasons; all exclusions logged |
| 17 Study characteristics | Cite each included study and present its characteristics | Tables 2.3, 2.4, 2.8, 2.9; Evidence Matrix | Yes | All 71 studies in the matrix; defense/design studies in Table 2.8 |
| 18 Risk of bias in studies | Present assessments for each study | Quality Appraisal §4 | Yes | Per-study Q1–Q10 codes and category. Record-level. |
| 19 Results of individual studies | Summary statistics for each study | Evidence Matrix ("Main Result") | Yes | Author-reported figures with setting; PV flagged |
| 20a Results of syntheses (characteristics/risk of bias) | Summarise characteristics and risk of bias of contributing studies | Theme syntheses; Table 2.10 | Yes | Evidence levels are cited alongside findings |
| 20b Results of statistical syntheses | Pooled estimates | — | Not Applicable | No statistical synthesis |
| 20c Results of heterogeneity investigations | Results of heterogeneity exploration | §2.12 (conflicting evidence) | Partial | Qualitative only |
| 20d Results of sensitivity analyses | — | — | Not Applicable | None performed (see 13f) |
| 21 Reporting biases | Assessments of bias due to missing results | §2.13.4 | Partial | Qualitative |
| 22 Certainty of evidence | Certainty for each outcome | Table 2.10; §2.13.1 | Partial | Expressed through evidence levels and single-study wording, not GRADE |
| 23a Discussion (interpretation) | Interpretation in context of other evidence | §2.12; §2.13 | Yes | |
| 23b Limitations of the evidence | Limitations of included evidence | §2.12; theme syntheses | Yes | Preprint share, self-built benchmarks, synthetic evaluations, withdrawn benchmark |
| 23c Limitations of the review processes | Limitations of the review | §2.13.4 | Yes | Nine limitations stated |
| 23d Implications | Implications for practice, policy and research | Theme syntheses ("implication for REM"); §2.13 | Yes | Implications stated for the thesis research. Practice and policy implications are limited to the regulatory motivation in §2.10.3. |
| 24a Registration | Registration information | — | No | The review was not registered (e.g., PROSPERO or OSF) |
| 24b Protocol access | Where the protocol can be accessed | Search Strategy; §2.2 | Partial | The protocol is the review specification supplied by the thesis author and summarised in §2.2. It was not published before the review. |
| 24c Protocol amendments | Amendments to the protocol | §2.2.4; Search Strategy §3 | Yes | Operational clarifications of I1 and I3, the retrieval cap and the page-2 retrieval are reported |
| 25 Support | Sources of financial or non-financial support | — | No | To be completed in the thesis front matter |
| 26 Competing interests | Declaration of competing interests | — | No | To be completed in the thesis front matter |
| 27 Availability of data, code and other materials | Which materials are publicly available | `chapter2/slr/` (raw search output, scripts); Screening Log; Evidence Matrix; Quality Appraisal | Yes | Raw JSON search output, deduplication and count script, decisions file, and generated CSV files are in the repository |

## PRISMA-S (search reporting) notes

| PRISMA-S item | Status | Notes |
|---|---|---|
| 1 Database name | Yes | OpenAlex, via the FastTrack Literature MCP `search_papers` tool |
| 2 Multi-database searching | Not Applicable / Partial | Only one database was searchable |
| 3 Study registries | No | Not applicable to this computer-security topic; none searched |
| 4 Online resources and browsing | Partial | Web search was used only to recover two missing abstracts, not to identify records |
| 5 Citation searching | Partial | Backward citation checking contributed to the prior reference list (other-methods stream). No forward citation searching was done in this pass. |
| 6 Contacts | No | Authors were not contacted |
| 7 Other methods | Yes | The previous chapter's verified reference list is reported as a separate stream |
| 8 Full search strategies | Yes | Search Strategy §3 |
| 9 Limits and restrictions | Yes | Years 2019–2026; retrieval cap of 24–25 records per page |
| 10 Search filters | Yes | No methodological filters |
| 11 Prior work | Yes | The previous chapter's search terms informed the concept blocks, as disclosed |
| 12 Updates | No | No update search yet; a pre-submission update is required |
| 13 Dates of searches | Yes | 25 September 2026 (UTC timestamps logged) |
| 14 Peer review of search | No | The search was not peer reviewed (e.g., no PRESS review) |
| 15 Total records | Yes | 320 records; 101 duplicates |
| 16 Deduplication | Yes | DOI or normalized-title matching, automated; one manual duplicate |

**Overall status.** The review satisfies the PRISMA 2020 items concerning:
- search transparency and reproducibility of the executed search;
- selection counts;
- per-study extraction;
- per-study appraisal;
- synthesis method.

It does **not** fully satisfy the items concerning:
- multi-database coverage (item 6);
- dual screening (items 8 and 9);
- a validated risk-of-bias instrument (item 11);
- sensitivity analysis (items 13f and 20d);
- registration (item 24a);
- support and competing interests (items 25 and 26, which belong in the thesis front matter).

These gaps are stated in §2.13.4 and are not concealed by the chapter's structure.
