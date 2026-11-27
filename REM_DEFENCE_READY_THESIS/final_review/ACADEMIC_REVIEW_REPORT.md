# Academic review report: final review before supervisor submission (27 November 2026)

| Item | Value |
|---|---|
| Thesis | *Runtime Evaluation and Mitigation (REM): A Security Framework for Financial AI Agents* |
| Files reviewed | `REM_Master_Thesis_Defence_Ready.docx` / `.pdf` at commit `06843a0` |
| Files corrected | Same names, in `REM_DEFENCE_READY_THESIS/`; now 271 pages |
| Approach | Every edit is an exact, logged replacement in `tools/spec_r9.py`, applied to the unchanged R8 sources and the new Sections 4.4 and 4.5. The thesis was not rewritten from scratch. |
| Preserved | Title, topic, scope, five-layer architecture and every verified result. No layer, objective, research question or experiment was added. |

## Overall assessment

- **Scientific substance.** The thesis is coherent and its evidence is honestly reported. Its central finding is preserved without softening: REM's learned decision protects in replay, at a large cost in legitimate work, and simple rules or a benchmark-informed policy match or exceed it.
- **What this review fixed.** It corrected the remaining factual and presentation defects named in the brief:
  - the committee page claimed a defense had taken place;
  - Figures 4.6–4.8 used the old arm labels;
  - Table 4.27 mixed raw counts into a percentage-point table;
  - the DOCX and PDF disagreed in pagination and TOC.
- **Other defects found and fixed:** see the chapter sections below and `CHANGE_LOG_FINAL_REVIEW.md`.

## Front matter

| Finding | Action |
|---|---|
| Committee page said the thesis "was successfully defended and approved". It has not been defended. | **Corrected.** It now opens "**This thesis has not yet been defended.**" Decision, date and signatures are left to the university. Placeholder table and note kept. |
| Title-page edition line read "Defence-ready edition … not formally approved" | **Corrected** to "Draft for supervisor review before the defense (26 November 2026) — not yet defended or approved" |
| Status page called the document the "defence-ready edition" | **Corrected** to "draft for supervisor review … revised after a final academic review" |
| The AI-use note named a product ("Claude Code") | **Product name removed.** The factual note itself is kept, because removing it would conceal an existing disclosure. Whether the university requires a formal declaration is flagged (unresolved U-1). |
| The status-page note on the Arabic abstract mentioned AI assistance | Reworded to "draft translation … requires review by a native speaker" |
| Declaration, dedication, acknowledgement | Placeholders kept. No official wording invented. |
| Faculty, department, degree title, supervisor titles | Not verified against official records. Flagged (U-6). |
| Abbreviations list | Complete for the terms used; sorted |

## Chapter 1: Introduction

| Check | Result |
|---|---|
| Problem → gap → aim → objectives → RQs → contributions | Logically connected. RQ1–RQ4 map onto the methodology (Section 1.7) and are answered in Table 5.1. |
| RQ status | Correct: "derived from the approved objectives … The approved proposal states no research questions … they remain proposed ([PD], decision D-10)". Not described as approved. |
| Objectives O1–O3 | Unchanged; each is assessed in Table 5.2 |
| Contributions (1.11) | Accurate after the earlier audit. Item 8 now says "component-level"; item 7 split into two sentences for readability. |
| Scope (1.10) | Preserves the banking/financial focus and states the exclusions (live deployment, adaptive attackers, other environments) |

## Chapter 2: Literature review

| Check | Result |
|---|---|
| Depth of the review | Correctly stated as a **record-level** systematic review ("No full-text screening was performed"); not described as exhaustive |
| Synthesis | The chapter already synthesises by theme (runtime monitors, consequence awareness, trajectory evidence, evaluation practice) and ends with a gap analysis that states what the evidence does **not** support. No restructuring was needed. |
| Gap and novelty | Not overstated: the gap is framed as an evidence question, and closely related designs are acknowledged (NEXUS, AgentTrust, DRIFT and others) |
| DRIFT | Now cited where it is named (H. Li et al., 2025) |
| Tool name in the methods paragraph | "AI coding assistant (Claude Code)" → "AI coding assistant". The fact that screening was AI-assisted is kept, because it bears on the reliability of the review. |

## Chapter 3: Methodology and REM framework

| Check | Result |
|---|---|
| Five layers and their roles | Preserved exactly (Sections 3.2–3.8); no sixth layer; offline fitting stays cross-cutting |
| Unimplemented feature presented as implemented | **Found and corrected.** Section 3.5 described the injection classifier x_ctx1 as in use ("The classifier is used with fixed inference"). It now states that no classifier was available and that in REM v1.0 the Detection Layer consists of x_ctx2 alone (D-8). Table 3.5 marks x_ctx1 "not implemented in REM v1.0". |
| Threat model, assumptions, decision rule, mitigation semantics | Consistent with the implementation (step-level mitigation, no reviewer, Escalate bounded) |
| Equations | Unchanged; every equation keeps its source in Appendix A.4. No equation was added and no EQUATION_ID invented. |
| Reproducibility | Commands and pinned versions given (S-3.15, Appendix S-B, the repository) |

## Chapter 4: Results

| Check | Result |
|---|---|
| Figures 4.6 and 4.7 (and 4.8) | **Corrected.** They used the 19-November arm labels (A1 = behavioral, A6 = learned decision, …), while Tables 4.25–4.31 use the remapped labels (A3a, A4a, …). The arm definitions were checked against the frozen protocol and the cross-study identity on 3,313 episodes. The figures were then regenerated from the same stored results with the Table 4.25 labels, behind a guard that compares the plotted counts with the raw-record recomputation. Figure 4.8's note now names "variant A4a (learned decision removed)". |
| Table 4.27 | **Corrected.** Three variants (A4c, A4d, A4e) had raw episode counts ("202 against 24 episodes", "127 against 141", "48 against 141") or dashes in a percentage-point table. The per-episode call records exist, so the paired differences, grouped-bootstrap intervals, discordant counts and McNemar p-values were computed from them. They agree exactly with the raw counts, e.g. (202 − 24) / 2,979 = 6.0 pp, 178 / 0. The caption now defines every cell type and points to Table 4.26 for raw counts. |
| All other numbers | 498 printed cells (counts, intervals, discordant counts, p-values) re-verified against a fresh recomputation from the raw records: 0 mismatches |
| Units | Attack goals reached, attacked episodes with an attack call executed, attack-labelled calls withheld and benign tasks completed are kept separate in every table header |
| Evidence kinds | Offline replay, recorded closed-loop runs, reference-solution checks and scripted integration are labelled; nothing is presented as live or deployed |
| Ablation terminology | "Component-level ablation of the five-layer REM design", with isolation limits in 4.5.1, 4.5.4, 4.5.5, 4.5.11 and threat 21 |
| Framework comparison | Fair. Progent's benchmark-specific allow-list is disclosed. DRIFT and MELON have no security result and none is implied. REM is not ranked above any framework. |
| Repetition | The R8 units kept inside 4.4.7 and 4.5.7 (a choice made earlier) repeat some figures; flagged for the supervisor (U-9) |
| One remaining tool-specific phrase | "prepared by another assistant in a separate checkout" → "prepared in a separate working copy of the repository". The AI label inspection (4.2.2) and the AI-assisted fixtures (4.6.9) are kept, because they bear on validity. |

## Chapter 5: Conclusions

| Check | Result |
|---|---|
| RQ answers | Each RQ is answered to the extent of the evidence; "Not shown" column kept |
| Claims beyond the evidence | None found. 5.8 states that the findings do not show protection of a live agent and do not rank REM against published defenses. |
| Readability | One 60-word sentence in 5.8 split |
| Future work | Realistic; ordered by priority; live evaluation listed as future work, not as a blocking omission |

## Appendices

- **Appendix A.** Unchanged.
- **Appendix B** (open supervisor decisions):
  - DRIFT added to D-15 (live comparisons);
  - two new entries: **SD-ABL** (acceptance of the component-level ablation) and **SD-CMP** (scope of the framework comparison);
  - no entry has been resolved by evidence, so none was closed.

## Language

| Change | Detail |
|---|---|
| Spelling normalised to the thesis's US convention | Outside code, URLs and reference titles: 52 "labelled" → "labeled", 3 "labelling" → "labeling", 5 "licence" → "license", 2 "judgement" → "judgment", 2 "artefact" → "artifact", 3 "realise" forms, 2 "recognise" forms, 1 "behaviour" (`audit/r9_renumbering.json`). The noun "analyses" is correctly left unchanged. |
| Over-long sentences | Five sentences of 59–92 words in the English abstract, Chapter 1 and Chapter 5 split without change of meaning |

**Scope of the language revision (stated plainly).**
- A full sentence-by-sentence rewrite of the 71,000-word text was **not** done. The text had already been edited in eight earlier editions, and the brief forbids unnecessary rewriting of correct passages.
- The revision targeted measurable defects: mixed spelling, over-long sentences, inaccurate wording and tool names.
- Chapters 3 and 4 still contain long technical sentences and many repository paths and dates. These serve reproducibility; the supervisor may ask to move some of them to an appendix (U-10).

## DOCX and PDF

| Finding (from the earlier review) | Cause | Action and verification |
|---|---|---|
| PDF 272 pages, DOCX re-export 270; TOC 4 pages against 2 | The build let LibreOffice regenerate the TOC, with its own spacing, before exporting the PDF. The DOCX stored a compact TOC. | The PDF is now a plain export of the stored DOCX. TOC, list-of-tables and list-of-figures page numbers are computed from that same PDF. **Verified:** an independent `soffice --convert-to pdf` of the DOCX gives 271 pages with identical text on every page, and the TOC, LoT and LoF start on the same pages. |
| Lists of tables and figures were plain text, not Word fields | — | Now Word TOC fields on the caption styles (`TOC \h \z \t "Table Caption,1"`, `"Image Caption,1"`), with the computed lists as cached results; F9 in Word updates them |
| Font | DOCX styles specify Times New Roman. It is not installed in the build environment, so the PDF uses the metric-compatible Liberation Serif. | Not fixable here. Opening the DOCX in Word with Times New Roman and updating fields (the document asks to update on opening) gives a TNR rendering; page numbers may shift slightly (U-5). |
| Page numbering | Roman for preliminary pages, Arabic from Chapter One | 179 page references checked. The one reported mismatch is a known false positive of the checker ("5.1 Introduction" also matches "4.5.1 Introduction"). |

**Not verified:** rendering in Microsoft Word itself. No copy of Word was available in this environment.
