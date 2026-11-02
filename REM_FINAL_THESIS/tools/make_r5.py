"""R5: supplementary literature integration of Kanaker et al. (2026) into the R4 chapters.

usage: python3 REM_FINAL_THESIS/tools/make_r5.py   (from the repository root)

Reads   REM_FINAL_THESIS/chapters_R4/*_R4.md   (left unchanged)
Writes  REM_FINAL_THESIS/chapters_R5/*_R5.md   and reports/CHANGE_LOG_R5.md

Scope (user instruction of 2 Nov 2026, "IMPORTANT SCOPE CORRECTION"): cite and critically compare
the paper ONLY. No change to the topic, title, problem, objectives, research questions, scope,
architecture, algorithm, equations, assumptions, features, data, labels, splits, costs, tiers,
predicates, tie-breaking, mitigation semantics, code, configuration, experiments or results.
Authorised edits: Chapter 2 critical discussion and comparison table; Chapter 3 citations that support
an existing rationale; Chapter 6 related-work comparison; bibliography; local cross-references.

Evidence level for every statement about the paper: A (abstract and registry metadata).
Metadata: Crossref record of DOI 10.3390/computation14050098; abstract: OpenAlex W7160053090 and the
stored record in REM_FINAL_THESIS/verification/update_search_2026-10-30.json. Full text not accessed
(www.mdpi.com and doi.org refused by the network policy on 2 Nov 2026).
Every replacement must match exactly once, or the script stops.
"""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'REM_FINAL_THESIS', 'chapters_R4')
DST = os.path.join(ROOT, 'REM_FINAL_THESIS', 'chapters_R5')
os.makedirs(DST, exist_ok=True)

NAMES = ['FRONT_MATTER', 'CHAPTER1_INTRODUCTION', 'CHAPTER2_LITERATURE_REVIEW', 'CHAPTER3_METHODOLOGY',
         'CHAPTER4_IMPLEMENTATION', 'CHAPTER5_RESULTS', 'CHAPTER6_DISCUSSION_CONCLUSION', 'REFERENCES']
text = {n: open(os.path.join(SRC, n + '_R4.md'), encoding='utf-8').read() for n in NAMES}
log = []


def rep(name, old, new, where, why):
    n = text[name].count(old)
    if n != 1:
        sys.exit(f'[{name} | {where}] expected exactly 1 match, found {n}: {old[:90]!r}')
    text[name] = text[name].replace(old, new)
    log.append((name, where, why))


CITE = 'Kanaker et al., 2026'

# ------------------------------------------------------------------ Chapter 2
# (1) Section 2.9.1: one sentence after the existing human-participation evidence (approval fatigue).
rep('CHAPTER2_LITERATURE_REVIEW',
    'It also identified a trade-off between approval fatigue and uncontrolled autonomy (P. Wang et al., 2026; preprint).',
    'It also identified a trade-off between approval fatigue and uncontrolled autonomy (P. Wang et al., 2026; preprint). '
    'A simulation study added in the supplementary update of 2 November 2026 reports, at abstract level, that human-in-the-loop '
    f'approvals sharply reduce high-impact actions but degrade under user error and habituation ({CITE}; Section 2.13.7).',
    '§2.9.1 The space of runtime responses (end of the human-participation paragraph)',
    'Adds level-A evidence consistent with the approval-fatigue finding already reported; cross-reference to §2.13.7.')

# (2) New Section 2.13.7 with critical discussion and Table 2.13, before the chapter summary.
S2137 = f'''### 2.13.7 Supplementary literature update of 2 November 2026: Kanaker et al. (2026) (outside the PRISMA flow)

**Status of this addition.** Kanaker et al. (2026), *Securing Tool-Using AI Agents Against Injection and Authority Misuse* (*Computation*, 14(5), Article 98), is added on 2 November 2026 as a dated supplementary literature update. The record was returned by query Q7 of the currency update of 30 October 2026 (OpenAlex W7160053090, stored in `update_search_2026-10-30.json`) but was not among the five records selected at title screening in Section 2.13.6. It was not part of the registered search of 25 September 2026. **No count in Table 2.2 or Figure 2.1 changes, it is not added to the 71 included studies, and no screening record is created retrospectively.**

**Evidence level.** The bibliographic metadata were checked against the Crossref record of the DOI (10.3390/computation14050098): six authors in the order H. Kanaker, H. Fakhouri, N. Abdel Karim, M. Abuhamdeh, N. H. A. Ismail and S. Fakhouri; *Computation*, volume 14, issue 5, article 98; 2026. The abstract was read in the OpenAlex record. The full text could not be retrieved in this revision, because the publisher and DOI hosts were refused by the network policy. Every statement below is therefore at **level A**: it reports what the abstract states, not what the paper's methods or results sections contain. Parameter values, the number of simulation runs, uncertainty estimates and the exact definitions of the metrics were not read.

**What the study does (level A).** The study argues that large-scale testing of deployed agents is difficult, vendor-specific and ethically sensitive, and proposes a transparent, theoretical simulation framework for user-facing risk in tool-using agents. Its stated methodological contribution is a formal threat model that **separates compromise, harm and severity**, together with a Monte Carlo pipeline that maps architectural choices (permissions, retrieval, memory exposure and approvals) and defensive controls to comparable outcome metrics. It instantiates the framework for six threat scenarios and nine defense configurations, and reports attack success rate, benign task success, latency overhead and severity-weighted harm. Its abstract reports four findings:

- least-privilege tool design is the strongest single broad control;
- human-in-the-loop approvals sharply reduce high-impact actions and exports, but degrade under user error and habituation;
- retrieval allowlisting nearly eliminates indirect injection while leaving other channels largely unaffected;
- rate limiting reduces tail severity more than attack success rate.

**Critical assessment.**

- *Strengths visible in the record.* The threat model makes the distinction between whether an agent is compromised and how much harm follows explicit. The study reports more than attack success, including benign task success, latency and a severity-weighted outcome, and it compares architectural controls side by side. Its assumptions are declared rather than hidden.
- *Limits stated by the authors.* The results come from an assumption-explicit simulator, not from field measurements, and the authors present them as comparative design guidance rather than incident-rate estimates for any deployed product. They do not measure how a particular agent or language model behaves.
- *Limits of this review.* Whether the simulated risks are calibrated to observed agent behavior, how sensitive the rankings are to the simulator's parameters, and how severity is weighted could not be assessed without the full text.
- *Consistency with other evidence in this chapter.* The approval finding agrees with the approval-fatigue trade-off reported by P. Wang et al. (2026) (Section 2.9.1). The allowlisting finding concerns one injection channel, whereas the provenance-based defenses of Section 2.6.5 examine the content that actually reaches a proposed call. The rate-limiting finding illustrates why attack success rate alone can miss differences in the severity of outcomes.

**Bearing on the gap assessment (Table 2.11).** The study adds to the "evidence against" column of Gap E: another study reports security, benign success, latency and a severity-weighted outcome together, although in simulation. It does not, by its abstract, compare a consequence-aware decision with a consequence-independent baseline that shares its estimator, so the narrowed residue of Gap E is unchanged. For Gap D, the study evaluates transaction-capable tools in a simulator rather than in an open, executable benchmark, so the retained statement is not contradicted. For Gap A, the abstract describes no calibrated per-call probability and no selection among verdicts by expected loss. These conclusions have the same record-level limits as the rest of the review.

**Table 2.13. Kanaker et al. (2026) and REM compared (Kanaker et al.: level A, abstract and metadata only; REM: Chapters 3–5)**

| Dimension | Kanaker et al. (2026) | REM (this thesis) |
|---|---|---|
| Research question | How architectural choices and defensive controls change user-facing risk in tool-using agents, evaluated without testing deployed products | Whether consequence-tiered expected-loss verdicts at the tool-execution boundary change intervention, attack success and utility relative to a consequence-independent threshold with the same estimator (Section 1.7; [PD]) |
| Method | Formal threat model separating compromise, harm and severity; Monte Carlo evaluation pipeline over architectural choices and defenses | Provenance, behavioral and action evidence; ridge logistic regression; logistic calibration on the logit; consequence tiers; expected-loss verdict among Allow, Modify, Escalate and Block; deterministic mitigation; audit record |
| Data and evidence | Assumption-explicit simulation; six threat scenarios; nine defense configurations | Recorded AgentDojo banking traces of 21 language-model agents; held-out predictions, observe-only decisions and replay under a no-adaptation assumption; no live runs (Chapter 5) |
| Treatment of harm and severity | Severity separated from compromise in the threat model; severity-weighted harm reported as an outcome | Consequence tier k~t~ separated from the probability p~t~; severity enters the decision through tier-indexed declared losses (Eqs. 3.5–3.9); realized loss reported (Eq. 3.22) |
| Defensive mechanisms | Least-privilege tool design, human-in-the-loop approvals, retrieval allowlisting, rate limiting (abstract); the full set of nine configurations was not read | Per-call verdicts with step-level withholding of the current call, an episode-level restriction variant, and escalation evaluated under an idealized-reviewer and a no-reviewer bound |
| Reported outcomes | Attack success rate, benign task success, latency overhead, severity-weighted harm | Discrimination and calibration, intervention rates, attack success rate, benign utility, utility under attack, processing time, realized loss |
| Limitations | Simulator rather than field measurement; results are comparative design guidance, not incident-rate estimates (stated by the authors) | Exploratory pilot; recorded traces and replay only; unaudited proxy labels; declared, unapproved costs; one benchmark (Chapter 6, Section 6.5) |

**What is and is not taken from this study.** The study is cited where it is consistent with existing positions of this thesis: the separation of compromise from severity (Chapter 3, Section 3.7.3) and the optimism of a perfect-reviewer assumption (Chapter 3, Section 3.7.5). REM's design was fixed before this record was examined, and no REM mechanism, parameter or experiment is derived from it. Its simulation results are not used as evidence for REM's effectiveness, and REM's results are not used to assess its findings.

'''
rep('CHAPTER2_LITERATURE_REVIEW',
    '---\n\n## 2.14 Chapter Summary',
    S2137 + '---\n\n## 2.14 Chapter Summary',
    'New §2.13.7 (critical discussion; Table 2.13), inserted after §2.13.6 and before §2.14',
    'Authorised item 2: critical discussion and evidence-backed comparison table; dated supplementary update outside PRISMA.')

# (3) Chapter summary: one sentence recording the supplementary update.
rep('CHAPTER2_LITERATURE_REVIEW',
    '**Selection.** The search of OpenAlex on 25 September 2026 identified 320 records.',
    '**Selection.** The search of OpenAlex on 25 September 2026 identified 320 records. (A simulation study added in a '
    'supplementary update of 2 November 2026 is discussed separately at abstract level in Section 2.13.7; it does not change '
    'these counts.)',
    '§2.14 Chapter Summary, "Selection" paragraph',
    'Local cross-reference so that the summary does not imply the update changed the PRISMA counts.')

# ------------------------------------------------------------------ Chapter 3 (citations supporting existing rationale only)
rep('CHAPTER3_METHODOLOGY',
    'Consequence descriptors do not enter Equation 3.1; they affect the verdict only through the loss.',
    'Consequence descriptors do not enter Equation 3.1; they affect the verdict only through the loss. Keeping the likelihood '
    'that an action is adversarially induced separate from the consequence of executing it is consistent with threat models '
    f'that distinguish compromise from harm and its severity ({CITE}).',
    '§3.7.3 Consequence tiers, first paragraph',
    'Citation supporting the existing separation of p_t and k_t; the design and equations are unchanged and are not derived from the paper.')
rep('CHAPTER3_METHODOLOGY',
    'They are not tested in this thesis, because no reviewer is present.',
    'They are not tested in this thesis, because no reviewer is present. They are optimistic: a simulation study reports that '
    f'human-in-the-loop approvals reduce high-impact actions but degrade under user error and habituation ({CITE}).',
    '§3.7.5 Reviewer assumptions paragraph',
    'Citation supporting the existing statement that the perfect-reviewer assumption is untested and is bounded by two reviewer models; no reviewer model is added.')

# ------------------------------------------------------------------ Chapter 6 (related-work comparison)
rep('CHAPTER6_DISCUSSION_CONCLUSION',
    '| C. Zhang et al. (2026) | Calibration need not improve control (A) | REM\'s evaluation observed no calibration effect on decisions |',
    '| C. Zhang et al. (2026) | Calibration need not improve control (A) | REM\'s evaluation observed no calibration effect on decisions |\n'
    '| Kanaker et al. (2026) | Simulation framework with a threat model separating compromise, harm and severity; Monte Carlo comparison of '
    'architectural controls across six scenarios and nine defense configurations (A; supplementary update of 2 November 2026, '
    'Chapter 2, Section 2.13.7) | Shares the separation of compromise from severity and reports a similar set of outcomes. It '
    'compares design-time controls in a simulator; REM evaluates a per-call runtime decision on recorded traces. Neither study\'s '
    'results transfer to the other |',
    '§6.3 Table 6.3 (one row added)',
    'Authorised item 4: related-work comparison.')
rep('CHAPTER6_DISCUSSION_CONCLUSION',
    'Each mechanism in REM has precedent.',
    f'A simulation study examined in a supplementary update of 2 November 2026 ({CITE}; Chapter 2, Section 2.13.7; abstract level) '
    'relates to REM at a different level of the problem. It compares architectural controls in an assumption-explicit simulator, '
    'whereas REM selects a verdict for each proposed call and is evaluated on recorded traces. Three of its reported findings bear on '
    'the interpretation of REM\'s results without changing them:\n\n'
    '- its finding that human-in-the-loop approvals degrade under user error and habituation is consistent with treating REM\'s '
    'idealized-reviewer results as an upper bound and the no-reviewer bound as the conservative reference (Section 6.1.2);\n'
    '- its finding that rate limiting reduces tail severity more than attack success illustrates why REM reports a loss-weighted '
    'measure beside the attack success rate, although REM\'s realized loss favours REM by construction (Chapter 5, Section 5.9);\n'
    '- its finding that least-privilege tool design is the strongest single broad control concerns a design-time restriction of '
    'privileges, which REM does not evaluate; REM\'s restricted-tool set 𝒯~R~ is used only by its mitigation semantics.\n\n'
    'The two studies do not test each other\'s mechanisms. REM does not evaluate least privilege, retrieval allowlisting or rate '
    'limiting, and the simulation study does not, by its abstract, estimate a per-call probability or select among verdicts by '
    'expected loss. Its simulated results are not evidence about REM, and REM\'s results do not test its findings.\n\n'
    'Each mechanism in REM has precedent.',
    '§6.3 Comparison with Prior Work (paragraph and list inserted before the final paragraph)',
    'Authorised item 4: explains relation and difference; existing conclusions and limitations unchanged.')

# ------------------------------------------------------------------ References
rep('REFERENCES',
    'Kaptein, M., Khan, V.-J., & Podstavnychy, A. (2026).',
    'Kanaker, H., Fakhouri, H., Abdel Karim, N., Abuhamdeh, M., Ismail, N. H. A., & Fakhouri, S. (2026). Securing tool-using AI '
    'agents against injection and authority misuse. *Computation, 14*(5), Article 98. https://doi.org/10.3390/computation14050098\n\n'
    'Kaptein, M., Khan, V.-J., & Podstavnychy, A. (2026).',
    'Reference list (alphabetical, before Kaptein)',
    'Authorised item 5: bibliography; APA 7 as in the existing list; metadata from the Crossref record of the DOI.')

for n in NAMES:
    open(os.path.join(DST, n + '_R5.md'), 'w', encoding='utf-8').write(text[n])

with open(os.path.join(ROOT, 'REM_FINAL_THESIS', 'reports', 'CHANGE_LOG_R5.md'), 'w', encoding='utf-8') as fh:
    fh.write('# Change log R5: supplementary literature integration of Kanaker et al. (2026)\n\n')
    fh.write('Generated by `REM_FINAL_THESIS/tools/make_r5.py` from `chapters_R4/` (unchanged). Files without an entry are '
             'copied verbatim (only the `_R5` file name differs).\n\n')
    fh.write('| # | File | Location | Reason |\n|---|---|---|---|\n')
    for i, (n, where, why) in enumerate(log, 1):
        fh.write(f'| {i} | {n}_R5.md | {where} | {why} |\n')
print(f'{len(log)} edits applied; chapters written to {DST}')
