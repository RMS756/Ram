# Unresolved Items and Supervisor Decisions (R3, 30 October 2026)

This register merges, without resolving any item:
- `SUPERVISOR_DECISIONS_REQUIRED.md` (root; consolidated 27 Oct);
- the R2 memo `revision_R2/reports_ar/05_مذكرة_قرارات_المشرف.md` (D-1 to D-15, 28 Oct);
- the open source items OI-01 to OI-14 and CF-01 to CF-09 (`REM_STAGE2_INPUT_PACKAGE/THESIS_READING_INDEX.md`);
- the items found in R3.

**No record of any supervisor decision was found in the repository.** Where the thesis text needed a wording, the R2 recommended option is used and labelled "pending supervisor approval". That wording is a proposal, not a decision.

Severity for formal submission:
- **CRITICAL:** determines what the thesis may claim;
- **MAJOR:** changes numbers or required content;
- **MINOR:** wording, presentation or citation detail.

## 1. Supervisor decisions

| ID | Item | Old codes | Options (R2 memo) | Current text | Effect on results if changed | Severity |
|---|---|---|---|---|---|---|
| **D-1** | Recorded-trace replay versus the Chapter 3 scope, which excluded replay-based estimation | SC-7 | (a) keep replay as a labelled NO-ADAPT sensitivity analysis and amend §3.1.4; (b) drop replay results; (c) run live experiments | (a), proposed amendment §3.11.11, labelled pending | (b) removes every ASR, utility and r_mod number in Ch. 5 §5.6 and the observe-only numbers that use r_mod through Eq. 3.5 | **CRITICAL** |
| **D-2** | Mitigation semantics: step-level (`CLAUDE.md` lock) versus episode-level (original Ch. 3) | SC-1, SD-3, AM-3 | (a) step-level reference, episode-level as a separate experimental policy; (b) episode-level | (a), stated as awaiting confirmation | None under NO-ADAPT replay (both give the same numbers); changes the justification of the restrictiveness and tie orders | **CRITICAL** (design meaning) |
| **D-3** | Calibration fitting target: labels (Eq. 3.4) versus Platt smoothed targets | SC-4 | (a) labels; (b) Platt targets | Both reported (Table 5.3) | ECE 0.0438 vs 0.0436 | MAJOR (spec–code conflict), negligible numerically |
| **D-4** | Tie rule: Ch. 3 order versus `VerdictTieError` in the frozen code | SC-2 | (a) Ch. 3 order with tie counts; (b) refuse ties | 0 ties in 6,762 steps reported | None in the pilot | MINOR |
| D-5 | Features unavailable under k_D2 (set to 0 with an audit flag) | — | (a) keep; (b) escalate; (c) fitting mean | (a), with counts | (b) raises escalation | MINOR |
| **D-6** | Label rule: user_task_15 collision; alternative attacker routes | LABEL-UT15, LABEL-ROUTE | (a) keep with post-hoc exclusion analysis; (b) redefine and re-run everything; (c) human audit first | (a) with the sensitivity analysis | (b) changes every number | **CRITICAL** (labels unaudited) |
| D-7 | Reviewer model for Escalate | REVIEWER | (a) two bounds; (b) declared error-rate model | (a) | (b) adds an intermediate estimate | MAJOR |
| D-8 | Feature set and injection classifier x_ctx1 | SD-FEAT, SD-DET | (a) report the current set, restrict conclusions to the pattern indicator; (b) choose a classifier and re-run | (a); no classifier chosen | (b) changes numbers | MAJOR |
| **D-9** | Costs C_miss, C_FA, C_mod, C_esc; tier map κ; predicates | SD-1, SD-2, SD-4 | (a) declared exploratory values; (b) elicited, pre-registered values and a re-run | (a), labelled exploratory | (b) changes observe-only and replay numbers | **CRITICAL** |
| D-10 | Research question wording | RQ-CONFIRM | approve or amend | RQ1–RQ4 marked [PD] in Ch. 1 and Ch. 3 | Chapter text | MAJOR |
| D-11 | Five or six chapters | SD-STRUCT | — | Six chapters (author's request in the master prompt; matches Ch. 3 Table 3.1). Recorded as an **author decision** pending supervisor acknowledgement | None | MINOR |
| D-12 | Title | TITLE | (a) keep; (b) drop "behavior-aware"; (c) "with behavioral evidence" | Working title supplied by the author, marked on the title page as not approved | None | MAJOR (formal) |
| D-13 | Citation choices: Platt 1999 vs 2000; which Kull 2017; λ convention | OI-07, REF-PLATT, REF-KULL, M1, OI-10 | Platt 2000 chapter recommended; Kull per the sentence supported; λ‖β‖² with λ = λ_impl/2 | Platt marked CONFLICT; Kull PARTIAL; λ on both scales | None | MINOR |
| D-14 | α grid cell α_blk = α_mod = 0.05 violates α_mod > α_blk | GRID-ALPHA | (a) report as not evaluable; (b) change the grid (post-hoc) | (a) | None | MINOR |
| **D-15** | Authorization and resources for live enforcing-mode experiments | BLOCKED (live) | API keys, budget, models, repeats, new pre-registration, simulated-attack scope | Not executed; stated as the decisive missing experiment | Required for the central claim | **CRITICAL** |

## 2. Other open register items (no R2 memo number)

| ID | Item | Current handling | Severity |
|---|---|---|---|
| SD-FREEZE | Whether the Chapter 3 specifications (provenance rule, feature set, predicates, Modify mechanism, grouping, labels, λ selection) are approved as the frozen specification | Implemented as specified and labelled; not claimed as frozen | **CRITICAL** (with D-9) |
| PILOT-AUTH | Whether pilot results may appear in the thesis, and with what label | Every Ch. 5 result is labelled EXPLORATORY | **CRITICAL** |
| AM-1 to AM-4 | Pilot amendments committed before held-out predictions (`7a707a7`) | Disclosed in Ch. 4–5 | MAJOR |
| SC-3 | Calibration-removed ablation refused by the frozen pipeline; run in the evaluation path | Disclosed in Ch. 5 Table 5.11 | MINOR |
| SC-5 | Brier score: Ch. 3 defers it (OI-09); code computes it | Reported with the binary convention stated | MINOR |
| SC-6 | Layer label of the estimator in code comments (L2) vs Ch. 3 (L4) | Disclosed in Ch. 4 §4.3; no computational effect | MINOR |
| SD-5 | Banking-only scope versus O1 (financial and task-automation agents) | O1 achieved for banking only (Ch. 6 Table 6.2) | MAJOR |
| A2-Q1 | CUSUM post-change rate; false-alarm rate above target | Reported as observe-only | MINOR |
| A2-ENFORCE, A3+A2 | CUSUM-driven enforcement variants named in an earlier prompt | Not implemented; conflict with `CLAUDE.md` | MINOR (closed unless the supervisor reopens it) |
| Repeats | ≥ 3 repeated runs (Ch. 3 §3.11.9) | The recorded traces contain one run per configuration | MAJOR |
| x_beh3 | Privilege-escalation feature fires on 92% of benign steps | Discussed in Ch. 6 §6.1.3 | MINOR (part of D-8) |
| RG-1 | Authoritative equation registry | Missing; no EQUATION_ID created | MAJOR (traceability) |

## 3. Source verification items

| ID | Item | Affects | Severity |
|---|---|---|---|
| OI-01 to OI-06 | NEXUS claims based on a Stage 1 reading, not reproducible | Ch. 2, Ch. 6 Table 6.3 (marked U) | MAJOR (closest prior work) |
| OI-07 | Platt citation conflict | Eq. 3.3 | MINOR (D-13) |
| OI-08 | Jackson (2025), content | Ch. 2 | MINOR |
| OI-09 | Brier convention | SC-5 | MINOR |
| OI-10 to OI-13 | le Cessie & van Houwelingen; Elkan; Cox; Chow: printed formulations not read | Eqs. 3.1, 3.2, 3.9, 3.10 | MAJOR (equation sources) |
| OI-14 | AgentDojo version | Resolved for the pilot as package 0.1.35 and repository commit `089ed468…`, recorded in every result file. Not approved as the frozen benchmark version | MINOR |
| CF-01 to CF-08 | Content not read for background sources | Ch. 2–3 | MINOR |
| CF-09 | EU AI Act articles read on a secondary host | Ch. 2 | MINOR |
| Full texts | No full text read in the 25 Sep, 27 Oct, 28 Oct or 30 Oct sessions | All of Ch. 2 | MAJOR |

## 4. Missing materials (cannot be produced by the author's assistant)

| Item | Status | Where the thesis shows it |
|---|---|---|
| Student name | Not supplied | Title page: "[NAME NOT SUPPLIED]" |
| Approved title | Not on record (D-12) | Title page subtitle |
| Approved proposal | Not in the repository | Objectives quoted from Ch. 3 §3.1.2 only |
| University thesis template and formatting rules | Not available | Formatting is provisional (A4, Times New Roman 12, 1.5 spacing) |
| Examination committee, approval page, declaration, acknowledgements, dates | Not supplied | Omitted rather than invented (front matter, "Status of This Document") |
| Arabic abstract (if the university requires one) | Not supplied; requirement unknown | Not included |
| Declaration of AI use (if the university requires one) | Only the author can make it. The project used an AI coding assistant for screening records, code, analyses, the AI-only label inspection and drafting (repository history; `chapter2/CHAPTER2_SYSTEMATIC_SEARCH_STRATEGY.md`) | Factual note in the front matter ("Status of This Document"); Ch. 2 §2.2.5 and §2.13.4 corrected in R3 to state the AI assistance the review record names |
| Human label audit | Package prepared (`results/pilot_R2/label_audit_human_package.csv`); no annotators | Ch. 5 §5.10; Ch. 6 §6.5 item 4 |
| Live LLM access | None | Ch. 5 §5.1; Ch. 6 §6.4 |
| Injection classifier x_ctx1 | Not chosen; model host unreachable earlier | Ch. 4 §4.5 and Table 4.6; Ch. 5 |

## 5. Items found in R3 and their handling

| Item | Handling |
|---|---|
| Memory figure in Ch. 5 R2 (2.9 KB) did not match its cited file (4,364 bytes) | **Corrected** (CHANGE_LOG_R3) |
| RQs in Ch. 1 not marked [PD] | **Corrected** |
| Close prior work published after the review (PROVISO, TapGuard, Kekatos et al., Ray, Z. Liu) | **Added** as a separate currency update outside the PRISMA flow (Ch. 2 §2.13.6), and discussed in Ch. 1, 5 and 6 |
| Hevner and Peffers cited without reference entries | **Added** after Crossref verification |
| RQ wording in Ch. 1 is a shortened form of the Ch. 3 wording (RQ2 lists fewer metrics; RQ3 says "processing time" for "latency") | **Not changed**: the wording is under D-10. Recorded as a MINOR finding in `EXAMINER_REVIEW.md` |
| Architecture figure draws L2 → L3 sequentially; Ch. 3 describes them as parallel. The figure carries an "EXPLORATORY" footer | Not changed (figure regeneration would need a design decision on the depiction). MINOR |
| Chapter 2 length (about 21,700 of the 48,300 words of Chapters 1–6, 45%) | Not shortened: shortening a systematic review needs the supervisor's view of the required depth. MINOR |

## 6. Minimum path to formal submission

1. Decisions D-1, D-2, D-6, D-9, D-15, SD-FREEZE and PILOT-AUTH (they determine what may be claimed).
2. Human label audit, then D-6.
3. Either live enforcing-mode runs (D-15) or an explicit supervisor decision that the thesis is submitted as an exploratory study without them, with the title and abstract adjusted accordingly.
4. Title (D-12), student name, template, committee and approval pages from official records.
5. Full-text checks for the equation sources (OI-07, OI-10 to OI-13) and the closest prior work (OI-01 to OI-06).
