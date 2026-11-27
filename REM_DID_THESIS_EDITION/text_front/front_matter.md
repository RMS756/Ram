@@TITLE_PAGE@@

# Committee Decision {.unnumbered}

**This thesis has not yet been defended.** The decision of the examination committee on the thesis *Runtime Evaluation and Mitigation (REM): A Security Framework for Financial AI Agents*, the date of the defense and the signatures are to be completed by the university after the defense.

| Examination Committee | Role | Signature |
|---|---|---|
| [Name and title as officially recorded] | Supervisor | [not signed] |
| [Name and title as officially recorded] | Co-Supervisor | [not signed] |
| [Name and title as officially recorded] | Internal Member | [not signed] |
| [Name and title as officially recorded] | External Member | [not signed] |

*Placeholder page. The committee, the decision and the signatures are to be completed by Al-Balqa Applied University; nothing on this page has been completed or approved.*

# Declaration of Authorship and Originality {.unnumbered}

*[Placeholder. The declaration in the university's prescribed wording is to be completed and signed by the student. It has not been completed or signed in this draft.]*

*Factual note on the use of AI assistance (not a declaration).* An AI coding assistant was used in this project, as recorded in the project files and the repository history. It assisted with the literature screening records, the software and tests, the execution of the analyses, the AI-only label inspection (Chapter 4, Section 4.2.2), the closed-loop and MELON integration code, the design and execution of the analyses of November 2026 including the paired test fixtures, and the drafting, restructuring and verification of this text. Any declaration of AI use required by the university must be completed by the student.

# Dedication {.unnumbered}

*[Placeholder for the student's dedication.]*

# Acknowledgement {.unnumbered}

*[Placeholder for the student's acknowledgement.]*

@@TOC@@

# List of Tables {.unnumbered}

@@LOT@@

# List of Figures {.unnumbered}

@@LOF@@

@@ABBREVIATIONS@@

# Abstract {.unnumbered}

@@ABSTRACT_EN@@

::: {dir=rtl lang=ar}
# الملخص {.unnumbered}

@@ABSTRACT_AR@@
:::

# Status of This Draft {.unnumbered}

This document is the **draft for supervisor review** dated 27 November 2026 (tenth edition: the ninth edition of 26 November 2026 unchanged except for the dated, clearly marked exploratory sections 2.11.6, 3.15, 4.6.12 and two additions in Chapter 5 on a Defense-in-Depth candidate, REM-DiD; ninth edition, revised after a final academic review: the eighth edition of 19 November 2026 with a comparison with existing security frameworks and an ablation study of REM's five layers at component level, both requested by the supervisors; the earlier editions are preserved unchanged). It is prepared for discussion. It has not been formally approved, and no approval is implied.

- **Condensation.** Units of the fifth edition that record the history of the analyses, the detail of the review process, the implementation and secondary tables are printed in an indexed supplement (`supplement/`), verbatim and with their fifth-edition numbers prefixed "S-". No result, equation or negative finding was removed from the record; the main text keeps the methods, the source equations, the main results, their uncertainty and the failure analyses.
- **New in this edition.** Section 4.4 is rewritten as a comparison with existing security frameworks: selection criteria, a fifteen-dimension architectural comparison, Progent's published banking policy decided by Progent's own code on three populations, and DRIFT and MELON at the level of architecture and code (DRIFT's official code executed with a scripted agent only). Section 4.5 is rewritten as an ablation study of the five layers, with a layer-to-implementation mapping, every variant compared with the full framework on the same episodes, and a statement of which layers could be isolated (only the Mitigation layer as a whole; the Input & Context layer only indirectly). All numbers of both sections were recomputed from the stored per-episode records. The units of the earlier Sections 4.4 and 4.5 are kept inside the new sections. Tables and figures of Chapter 4 are numbered sequentially; the correspondence with the eighth edition's numbers is listed in `REM_DEFENCE_READY_THESIS/THESIS_REVISION_LOG.md`, and the supplement's numbers are those of the fifth edition, as before. **New in the eighth edition.** A final ablation of REM v1.0 under a protocol committed before scoring (now in Section 4.5.7); a comparison with the four distributed defenses through their authors' recorded runs and REM's replay on the same task pairs (now in Section 4.4.7); and a summary of the exploratory redesign studies of 18 and 19 November 2026, which were not adopted (now in Section 4.5.8). **New in the seventh edition.** The second version of the amount verifier after an independent review (defects D3 and D4; corrected statement of the stage order) and a condensed Section 2.8.3. **New in the sixth edition.** The repair study of 17 November 2026 (typed verification of request-derived amounts, now in Section 4.5.8), corrections of statements about the guard and the learned decision, three close works of November 2026, and corrected references (NEXUS, MELON, PRISMA 2020, PRISMA-S).
- **Basis.** It revises the five-chapter draft of 3 to 6 November 2026. Verified text was kept; new sections report the literature read in full on 11 November 2026, the rule baselines, the generalization and robustness analyses, and a confirmatory run. The second edition reorganizes Chapter 4 into six sections requested by the supervisor, adds an exploratory extension study with one published policy replayed in the same harness, and corrects several statements of the first edition. The third edition adds the repair of three defects of the extension's permission rule found by an external review and a call-level audit of the one benchmark task where all remaining attacks occur. The fourth edition adds a third revision of that rule, which repairs two further defects, and is shorter: the extension study is reported in three compact sections, background material of the literature review that lies outside the evaluated threat model and the design text of the unexecuted live evaluations are no longer reproduced, and the table of contents lists two heading levels. Everything removed remains in the third edition and in the repository. The fifth edition adds the study of 16 November 2026: the Progent paper read in full, and learned, statistically calibrated and policy-engine decisions compared behind the permission guard, which show that the guard used alone gives the same outcomes. The changes are listed in the change log that accompanies the thesis files.
- **Design status.** The design values (costs, consequence tiers, predicates, feature set and label rule) are declared values, not approved ones. REM v1.1 is a proposed amendment; REM v1.0 remains the design of record until the supervisor decides. The open decisions are listed in Appendix B.
- **Evidence.** All results come from recorded trajectories replayed under the assumption that the agent does not adapt. No live-agent experiment was executed, and no defense that needs a language model was run. One policy from a published system's repository, which needs no model, was replayed on the recorded episodes. The extension study is development evidence: it is proposed, exploratory and not adopted.
- **Formatting.** The university's thesis template and formatting guide were not available. The layout is an assumed A4 university style, not a verified one.
- **Unverified metadata.** The faculty, department and degree title are carried over from earlier drafts and have not been verified against official records.
- **Arabic abstract.** The Arabic abstract is a draft translation of the English abstract; its wording and the Arabic spelling of the names require review by a native speaker.
- **Placeholders.** The committee decision, declaration, dedication and acknowledgement are placeholders for the university and the student to complete.

@@SECTION_BREAK@@
