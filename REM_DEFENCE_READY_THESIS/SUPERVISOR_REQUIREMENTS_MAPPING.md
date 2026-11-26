# Supervisor requirements and where the defence-ready edition meets them

Thesis: `REM_Master_Thesis_Defence_Ready.docx` / `.pdf` (26 November 2026). Section, table and figure numbers below are those of this edition.

This document maps requirements to text. It does not record any approval: the thesis has **not** been formally approved, and the research questions and design values remain unapproved.

## The two supervisor requirements

| Requirement | Where | Status |
|---|---|---|
| **1. Ablation study of the individual contribution of REM's layers** | Section 4.5 (4.5.1–4.5.12) | Done with recorded episodes (offline replay); no live experiment was needed or claimed |
| **2. Comparison of REM with existing security frameworks (Progent, DRIFT, MELON and other relevant frameworks)** | Section 4.4 (4.4.1–4.4.11) | Done: quantitative for Progent's published policy and the defenses distributed with AgentDojo; architectural and code-level for DRIFT and MELON; literature-level for the rest |
| No live-model experiments or real-world deployment required | Throughout: every result is labelled as replay or as recorded runs (Section 4.1.4, Table 4.3) | No live run was executed or claimed. Live evaluation is future work (Section 5.7), not a blocking limitation. |

## Ablation study (Part 3)

| Item requested | Where | Notes |
|---|---|---|
| Introduction | 4.5.1 | |
| Motivation | 4.5.2 | |
| Experimental design | 4.5.3 | Two pre-registered studies (19 and 21 November 2026); NO-ADAPT replay; same fitted state; cross-study identity on 3,313 / 3,313 episodes for every shared arm |
| Layer-to-implementation mapping | 4.5.4, Table 4.24, Figure 4.4 | Follows Chapter 3 (Table 3.6): the action features belong to Behavioral Analysis, and Input & Context computes no evidence |
| Variants A1–A5 with status | 4.5.5, Table 4.25 | See the status table below |
| Metrics | 4.5.6 | Episode is the primary unit; calls are secondary and not treated as independent |
| Results | 4.5.7, Tables 4.26–4.29, Figure 4.5; detail of 19 Nov in Tables 4.30–4.34 | All recomputed from the stored per-episode records (`audit/`) |
| Statistical analysis | 4.5.9 | Paired exact McNemar tests; grouped bootstrap (9 attack and 16 task clusters, described as descriptive); no multiplicity correction, stated |
| Discussion | 4.5.10 | Separates "no measurable effect", "evidence of ineffectiveness" and "evidence of being unnecessary" |
| Limitations | 4.5.11 | |
| Conclusion | 4.5.12 | |

**Status of each variant:**

| Variant | Status |
|---|---|
| A1 (Input & Context labelling) | Not independently isolatable; observed indirectly through A3b |
| A1h (hygiene) | Not exercised (0 of 16,727 outputs changed) |
| A2a, A2b (Detection; A2b coupled) | Implemented and evaluated |
| A2c (injection classifier) | Not isolatable: absent (D-8) |
| A3a, A3b (Behavioral and action/provenance evidence) | Implemented and evaluated |
| A4a–A4e (learned decision, predicates, calibration, thresholds, Modify) | Implemented and evaluated |
| A5 (enforcement / shadow mode) | Implemented and evaluated |
| SHAP | Not ablated: audit only |

**Negative findings, as reported:**
- Behavioral evidence lowers task completion, with no measurable security effect.
- Detection, the predicates, calibration and Modify show no measurable effect. This is stated as "no measurable effect here", not as "ineffective" or "unnecessary".

## Framework comparison (Part 4)

| Item requested | Where | Notes |
|---|---|---|
| Introduction | 4.4.1 | |
| Selection criteria | 4.4.2, Table 4.10 | Third-party Progent re-implementation excluded; AgentDyn identified as a benchmark, not a comparator |
| Framework descriptions | 4.4.3 | |
| Architecture comparison, 15 dimensions | 4.4.4, Table 4.12, Figure 4.1 | Each entry marked P (paper), I (implementation) or M (measured here); "Not measured here" or "Not reported" where unknown |
| Mechanism comparison | 4.4.5 | |
| Experimental design | 4.4.6, Table 4.13 | |
| Quantitative results | 4.4.7, Tables 4.14–4.23, Figures 4.2–4.3 | Progent's banking policy decided by **Progent's own checker** on three populations, with the earlier rule baselines and distributed defenses. DRIFT: scripted integration only, with modules on and off (Table 4.23). MELON: status only. |
| Fairness | 4.4.8 | Oracle caveat: two of Progent's permitted recipients come from task solutions, and the attacker's account is excluded, so the policy blocks every injection task by construction |
| Discussion, limitations, conclusion | 4.4.9–4.4.11 | States that REM is **not** better than Progent's policy offline; no ranking against DRIFT or MELON |

## Parts 5–12

| Part | Where | Status |
|---|---|---|
| 5. Coherent evaluation: unit of analysis and denominators; no duplication | Units: 4.3.3, 4.5.6. Every count carries its denominator in tables. | Earlier units are kept inside the new sections, as the user chose ("keep them in Chapter 4"). Some arms therefore appear twice: in the new layer tables and in the detailed 19-November tables. The repetition is labelled. See UNRESOLVED_ISSUES.md. |
| 6. Alignment: RQs derived from objectives and not approved; no generalisation | 1.7 (RQs labelled [PD]), 5.2 | Unchanged from R8 apart from RQ4's answer; every new conclusion is bounded to one benchmark and to replay |
| 7. References verified, none fabricated | References | DRIFT and AgentDyn added from verified bibliographic records. Status notes are inside the entries (full text not read). See UNRESOLVED_ISSUES.md. |
| 8. Figures and tables: numbering, captions, acronyms, no invented equations | Chapter 4 numbered sequentially; LoT and LoF regenerated | Abbreviations added. Equation set checked unchanged. No new equation and no EQUATION_ID. |
| 9. Limitations | 4.4.10, 4.5.11, 4.6.11 (threats 1–22), 5.6 (items 1–12) | Not called a real-world deployment. Live experiments are future work, not a blocking limitation. |
| 10. Conclusions and future work without overstatement | 5.8, 5.7 | 5.8 says the findings do not rank REM against any published defense |
| 11. Deliverables | `REM_Master_Thesis_Defence_Ready.docx` and `.pdf`; THESIS_REVISION_LOG.md; this file; UNRESOLVED_ISSUES.md; DEFENCE_PREPARATION.md | The original R8 files are not overwritten. No approval is claimed. |
| 12. QC | `audit/qc_checks.txt`, `audit/thesis_number_check.json` | 191 printed cells match the raw records. Citations two-way complete. Page references checked. Rendered pages inspected. |

## Design lock (CLAUDE.md)

- No design value, threshold, cost, label, feature or benchmark version was chosen or changed.
- REM keeps exactly five layers; no sixth layer was added.
- CUSUM remains observe-only and SHAP audit-only.
- No equation was added.
- The ablation variants are configurations of the frozen harness. They are not design changes.
