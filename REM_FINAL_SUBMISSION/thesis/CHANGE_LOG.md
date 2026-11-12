# Thesis change log: five-chapter draft (3–6 November 2026) → final draft (12 November 2026)

**Status:** draft for supervisor review; not approved; not submitted.

## Files

| Output | Path |
|---|---|
| Chapters (Markdown) | `src/CHAPTER_01_FINAL.md` … `src/CHAPTER_05_FINAL.md`, `src/APPENDICES_FINAL.md` |
| Chapters (Word) | `docx/CHAPTER_01_FINAL.docx` … `docx/CHAPTER_05_FINAL.docx`, `docx/APPENDICES_FINAL.docx`, `docx/REFERENCES_FINAL.docx` |
| Combined thesis | `REM_THESIS_FINAL.docx`, `REM_THESIS_FINAL.pdf` (284 pages: front matter i–xxvi; main text 146 pages, down from 205; references; appendices A–F) |
| References | `references/REFERENCES_FINAL.md` (118 entries) |
| Build | `tools/make_final.py` (assembly and renumbering), `tools/spec_final.py` (what is kept, moved or added), `tools/build_final.py` (DOCX/PDF), `text/` (new text), `text_front/` (front matter, abstracts) |
| Audit | `audit/final_source_map.json` (every base section: kept, moved or replaced), `audit/final_crossref_check.txt` |

Rebuild from the repository root: `python3 REM_FINAL_SUBMISSION/thesis/tools/make_final.py && python3 REM_FINAL_SUBMISSION/thesis/tools/build_final.py`.

## Principles

- Verified text of the previous draft was kept verbatim at the level of whole paragraphs, tables and subsections; nothing in it was reworded except the listed replacements in `spec_final.py`.
- Every number, table and figure was renumbered by script; 0 unresolved references.
- REM v1.0 is unchanged and remains the design of record. REM v1.1 is presented as a proposed amendment.

## Changes by chapter

| Chapter | Main-text pages (draft of 3–6 Nov → final) | Changes |
|---|---|---|
| 1 | 10 → 11 | New research gap (evidence gap); research-methodology section updated for rule baselines, double holdout and the confirmatory run; contributions split into demonstrated and not demonstrated, with measured results; REM v1.1 introduced as a proposed amendment |
| 2 | 89 (with its appendix) → 39 | Preserved: review methodology, PRISMA counts, Table 2.2, Figure 2.1, syntheses. Moved to Appendix A: eligibility criteria, appraisal and extraction details, agent background, tool-channel and memory threats, input/system defenses, learned guardrails, sequence monitors, anomaly-detection foundations, logistic-regression and CUSUM foundations, attribution, five large tables. NEXUS section rewritten from the published abstract and the authors' README. New dated sections outside the PRISMA flow: updates of 30 October and 2 November (condensed), full-text readings of 11 November (six papers) and three abstract-level works, revised research-gap statement with its assessment |
| 3 | 68 → 48 | Frozen specification unchanged. New: rule baselines and diagnostic arms; generalization schemes S1–S3; robustness probes and paired fixtures; confirmatory protocol; outcome layers and metrics; versioned amendment REM v1.1; implementation summary (details moved to Appendix B); added threats. Moved: notation, layer interfaces, optional CUSUM analysis and equation provenance to Appendix C |
| 4 | 32 → 38 | Pilot results kept. New: kinds-of-evidence table; confirmatory population and chronology; rule baselines and an audit of REM's interventions; generalization and the rejected candidate; robustness probes and fixtures; confirmatory evaluation with the pre-declared GO verdict and its limits; status of live and published-defense experiments; new interpretation (frontier; information as the limiting factor); comparison with recent work without mixing published numbers; added threats. Moved: live-agent and MELON design and status to Appendix D; mitigation-semantics sensitivity to Appendix E |
| 5 | 6 → 10 | Rewritten: answers to RQ1–RQ4; objectives; contribution table (precedent, code, experiment, result, limits); not confirmed / rejected variants / significance of negative findings; limitations; prioritized future work (trusted authorization input first after decisions); conclusion |
| Front matter | | New English and Arabic abstracts; status page updated; AI-assistance note extended |
| Appendices | | A review material; B implementation; C notation, CUSUM, equation provenance; D live and MELON design and status (not executed); E mitigation semantics; F open supervisor decisions |

## Not changed

`rem/`, `configs/`, `results/`, the MELON bundle, the previous thesis versions (R2–R5, five-chapter build, review copy).
