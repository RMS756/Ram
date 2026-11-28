# REM final scientific consolidation: executive summary (28 November 2026)

**Overall position.** REM v1.0 is retained unchanged as the evaluated artifact. The thesis is positioned as a controlled **empirical evaluation of whether a layered runtime defense for a financial agent achieves defense in depth**; it does not claim a novel architecture. The evidence supports *limited complementary protection within a shared learned decision and enforcement pathway*, on NO-ADAPT replay of AgentDojo banking recordings. It does not support robust operational defense in depth.

**Completion status: not complete.**

| Part | Status |
|---|---|
| Thesis integration | Done, in a separate working copy |
| Mathematical audit | Done |
| Full-text source verification | **Incomplete:** no full text could be opened from this session (01) |
| Six decisions | Belong to the supervisor (08) |

## 1. Authoritative baseline

| Item | Current authoritative version | Verification status |
|---|---|---|
| Thesis edition | **Humanized edition**: `REM_HUMANIZED_THESIS/src/*.md` → `REM_Master_Thesis_Humanized.docx` (sha256 `2524a849…`, commit `f59ff5c`; 272 pp.). DiD edition (`REM_DID_THESIS_EDITION/`, sha256 `0cc55a3d…`, commit `3749f99`) for its five insertions. Not the most recently modified file: the choice follows reconciliation 03 §3 | **Verified** (both editions derive from the defence-ready edition; the insertion points do not overlap; merge done) |
| REM implementation | **REM v1.0**: `rem/` tree `cd11e3232071…`; `configs/exploratory/pilot_e0.yaml` sha256 `8e1aa107…`; unchanged since `7c79883` | **Verified** at HEAD; reproduced exactly on 27 Nov 2026 (`ad81484`) |
| Scientific reconciliation | `REM_FINAL_SCIENTIFIC_RECONCILIATION_2026_11_28/`, commit `5d7828c` | **Verified**; no later reconciliation exists |
| Layered-framework review | `REM_LAYERED_FRAMEWORK_DESIGN_REVIEW/`, commit `6c52c90` | **Verified**. One correction: its 09 lists MELON at code level, whereas the thesis records a full-text reading (01) |
| Experimental protocols | Pilot configuration `pilot_e0.yaml` (27 Oct). Ablations `dc8407d` (19 Nov) and `93e6630` (21 Nov). DiD-2 `2547854` (post-hoc arms `e3e7488`). Confirmatory run of 11 Nov | **Verified**, except the confirmatory run's freeze commit, which is **not in this repository's history** (unresolved; 06) |
| Mathematical audit | `EQUATION_PROVENANCE_AUDIT.md` (27 Oct). Review 06 (`6c52c90`). **This 03** supersedes both for M1 and SC-2 | **Verified** against the code and stored results today |

## 2. What was verified, and what remains unresolved

| Verified | Unresolved |
|---|---|
| Bibliographic records and abstracts of all 12 works, BARBICAN and the CASCADE audit (Crossref and OpenAlex) | Full texts: **[SOURCE VERIFICATION INCOMPLETE]** for all except Progent and MELON (read earlier) |
| Two record corrections: Jang et al. is **2027** (issue year); TISC DOI still unregistered | CASCADE's own paper: not found |
| M1: text, code and grid consistent (Ch. 3 already converts λ) | Kull "prove" wording; Platt chapter content; Holm record |
| SC-4: Eq. 3.4 declared reference; configuration and runner agree | SC-4 approval; SC-2 adoption; α grid (supervisor) |
| SC-2: the evaluated policy applies the Ch. 3 order; 0 ties in all 217 stored tie counts | — |
| The working copy's numbers: 498 cells, 0 mismatches; DiD numbers verified; 120 references, all cited | — |

## 3. Answers to the ten final questions

**1. Which full texts were successfully accessed and verified?**

None in this task. Every academic host (arXiv, ACL Anthology, PMLR, MDPI, TechScience, Nature) was refused by the session's network policy:
- Scholar Gateway requires the user to sign in again;
- Elicit's plan has no API access;
- the saved environment that allows arXiv ("ram-thesis-research") cannot be used by this running session.

Full texts available from earlier sessions: **Progent** (v3) and **MELON**, as recorded in thesis Table 2.3.

**2. Which studies remain abstract-only or inaccessible?**
- **Abstract or record only:** NEXUS (also its repository), Agent-Sentry, CaMeL (repository only), AgentDojo (paper; the package was used directly), the Multilayer DiD framework, PromptGuard, the layered RAG framework, the CASCADE audit, Spotlight-Guard, AIS, BARBICAN.
- **Not found:** CASCADE's own paper. Details are in 01.

**3. Which A1–A7 recommendations were integrated?**

**All seven, as documentation**, in the working copy:

| Rec. | Location |
|---|---|
| A1 | Ch. 3 §3.4.2 |
| A2 | Ch. 3 §3.2.2 and Ch. 1 |
| A3 | Ch. 3 §3.8 and Ch. 4 §4.5.7. The gateway was previously absent from every edition |
| A4 | Ch. 3 §3.6.2 |
| A5 | Table 3.17 |
| A6 | Ch. 4 §4.3.3 |
| A7 | Ch. 2 new §2.11.7 |

B1–B7 remain future work. Mapping in 02.

**4. Which mathematical issues were resolved using evidence?**
- **M1:** already consistently documented in Chapter 3, with λ = λ_impl/2 and both scales reported.
- **SC-4:** consistent; Eq. 3.4 is the declared reference in the text, configuration and runner.
- **SC-2:** shown to affect no result that counts ties (0 of 217).
- **Kull:** the ambiguity is resolved at record level (the AISTATS 2017 paper is the one cited).
- **No equation was changed and no error was found.**

**5. Which mathematical issues remain open?**

| Issue | What is open |
|---|---|
| SC-2 | Adoption of the tie rule (supervisor) |
| SC-4 | Approval (supervisor) |
| Platt | Chapter title and content check |
| Kull | Whether the paper "proves" the identity and states the monotonicity condition (source check) |
| α grid | Lost cell (supervisor; no value proposed) |
| Holm | Uncited in the DiD sections; record not in Crossref |

**6. Final recommended research-gap formulation** (04 §3, [PD]):

> Layered runtime defenses against indirect prompt injection, combining content inspection, provenance-aware, behavioral, learned and rule-based controls, have been proposed and, in several cases, ablated layer by layer. Among the studies examined, most of them at abstract level, the evidence remains limited on three questions for a financial agent acting on an executable banking benchmark:
> - which components of such a defense actually carry its protection, and whether removing a component and suppressing its evidence at test time lead to the same assessment;
> - whether a learned, consequence-aware decision adds value over simple deterministic rules on the same proposed financial calls;
> - what the measured protection costs in legitimate financial task completion, including against a reference that executes no state-changing call.

It is narrower than the candidate. Layer ablations (Saleem et al.; Spotlight-Guard), a learned-versus-rules comparison (NEXUS) and the deletion-versus-substitution point (BARBICAN) are reported in the literature at abstract level.

**7. What are the final defensible research contributions?** (05)
- **A.** Limited complementary protection within one learned decision and one enforcement point: enforcement and the learned pathway are each necessary; action and behavioural evidence cover different attack classes; detection and predicates are null.
- **B.** Protocol-frozen, paired component-level ablations, with stated limits: the estimator is not isolated, and Input & Context is not removable on its own.
- **C.** Removal and idealized suppression disagree (exploratory).
- **D.** The security–utility cost, including the P1 identity with the withhold-all reference; that reference is not useful completion.
- **E.** The strengths and limits of replay as an evaluation method; not live, not an independent replication.
- **F.** Qualified negative findings.

The thesis claims no novel algorithm and no superiority over any framework.

**8. Are all research questions supported by actual evidence?**
- **Yes** for the proposed RQ1–RQ5 (06 §2). RQ2(d) and RQ4 are exploratory; RQ5's security difference is unresolved and is not non-inferiority.
- The **current** RQ3 (residual success after Modify) is **not answerable** by replay.
- The working copy keeps RQ1–RQ4 until the supervisor decides (D2).

**9. What changes were made to the separate thesis copy?**
- 85 logged changes:
  - the DiD insertions merged;
  - the reconciliation's corrections R1/R4;
  - the gap narrowing;
  - A1–A7;
  - Chapter 5 and abstract consistency;
  - "pre-registered" removed (15 occurrences);
  - three future-work items;
  - 14 references.
- Built to DOCX and PDF in the pinned environment, 291 pages.
- Change log in 10; full texts of every change in 07.
- The original thesis files are untouched.

**10. Which decisions must be referred to the supervisor?** (08)
- D1 title vs topic;
- D2 RQ1–RQ5;
- D3 framing as an empirical evaluation of defense in depth;
- D4 contribution wording;
- D5 gap wording;
- D6 M1 acknowledgement;
- D7 SC-4, Platt and Kull;
- D8 the tie rule;
- D9 the α grid and the Holm citation;
- D10 the DiD merge;
- D11 full-text verification before submission;
- D12 length (optional).

## 4. Recommended thesis direction

1. Review the working copy; 07 lists each edit with its reason.
2. Decide D1–D5 first, because they fix the framing.
3. Obtain full texts (D11) and re-check §2.11.6 and §2.11.7 before submission.
4. Resolve D7–D9 by source checks and decisions, not by new experiments. REM v1.0 stays unchanged.

## 5. Files

| File | Content |
|---|---|
| 01 | Full-text verification, study by study |
| 02 | A1–A7 integration |
| 03 | Mathematical integrity audit |
| 04 | Final research gap |
| 05 | Final contributions |
| 06 | RQ and methodology alignment |
| 07 | Thesis-ready replacement text (generated from the applied edits, plus gated text) |
| 08 | Supervisor decision register |
| 09 | Reference audit |
| 10 | Integration guide and change log |
| `thesis_working_copy/` | Revised working copy (DOCX, PDF, sources, tools, audit) |
