@@TITLE_PAGE@@

# Committee Decision {.unnumbered}

This thesis, *Runtime Evaluation and Mitigation (REM): A Security Framework for Financial AI Agents*, was successfully defended and approved on **[date to be completed by the university]**.

| Examination Committee | Role | Signature |
|---|---|---|
| [Name and title as officially recorded] | Supervisor | [not signed] |
| [Name and title as officially recorded] | Co-Supervisor | [not signed] |
| [Name and title as officially recorded] | Internal Member | [not signed] |
| [Name and title as officially recorded] | External Member | [not signed] |

*Placeholder page. The committee, the decision and the signatures are to be completed by Al-Balqa Applied University; nothing on this page has been completed or approved.*

# Declaration of Authorship and Originality {.unnumbered}

*[Placeholder. The declaration in the university's prescribed wording is to be completed and signed by the student. It has not been completed or signed in this draft.]*

*Factual note on the use of AI assistance (not a declaration).* An AI coding assistant (Claude Code) was used in this project, as recorded in the project files and the repository history. It assisted with the literature screening records, the software and tests, the execution of the analyses, the AI-only label inspection (Section 4.10), the closed-loop integration code, and the drafting, restructuring and verification of this text. Any declaration of AI use required by the university must be completed by the student.

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

This document is a **draft for supervisor review**, not a version for formal submission.

- **Restructuring.** It reorganizes the six-chapter R5 draft into five chapters. No numerical result, equation or design value was changed; the mapping is recorded in `final_five_chapters/audit/THESIS_SOURCE_MAP.md`.
- **Exploratory evidence.** The design values (costs, consequence tiers, predicates, feature set and label rule) are declared exploratory values, not approved ones. The evidence comes from recorded traces and from a replay that assumes the agent does not adapt.
- **Live-agent evaluation.** A closed-loop integration with live agents is implemented and tested with scripted test agents (Section 3.17), but it has **not** been executed with a language model (Section 4.12).
- **Formatting.** The university reference thesis and any official formatting guide were not available in the working environment. The layout is therefore an assumed A4 university style, not a verified one.
- **Unverified metadata.** The student name, supervisor and co-supervisor are as supplied by the student. The faculty, department and degree title are carried over from earlier drafts and have not been verified against official records.
- **Arabic abstract.** The Arabic abstract (الملخص) is a draft translation of the English abstract prepared with AI assistance; its wording and the Arabic spelling of the names require the student's review.
- **Review copy (6 November 2026).** Section 4.14 is replaced by "Offline Replay Evaluation and Planned MELON Extension" (one results table; MELON conditions not executed), and the benign-utility sentence is corrected in the abstract and Section 4.18. The main five-chapter draft is unchanged.
- **Placeholders.** The committee decision, declaration, dedication and acknowledgement are placeholders for the university and the student to complete.

@@SECTION_BREAK@@
