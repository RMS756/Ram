# Source Verification Log (R3, 30 October 2026)

This log records how the 113 entries of the consolidated reference list were checked, by whom and when, and what was **not** checked. The per-entry status is in `REFERENCES_VERIFIED.md`.

## 1. Access available in each session

| Session | Access | Full texts read |
|---|---|---|
| Stage 1 (before 22 Sep) | Mixed: some PDFs, search-retrieved excerpts | Some. Recorded in `REM_STAGE2_INPUT_PACKAGE/THESIS_READING_INDEX.md`; the open items OI-01 to OI-14 and CF-01 to CF-09 come from there |
| 25 Sep (Chapter 2 review) | OpenAlex search; Crossref; abstracts | None. The review is record-level (`chapter2/CHAPTER2_VERIFICATION_LOG.md`) |
| 27 Oct (foundational sources) | Crossref; OpenAlex records | None (`SOURCE_VERIFICATION_REPORT.md`) |
| 28 Oct (R2) | FastTrack literature connector: OpenAlex `get_paper`, Crossref `verify_reference`. arxiv.org refused; Elicit refused | None (`revision_R2/evidence/literature_checks_2026-10-28.md`) |
| 30 Oct (R3, this session) | FastTrack connector only. arxiv.org, api.crossref.org and api.openalex.org return HTTP 403 through the session proxy | **None** |

**Consequence.** No reference in the thesis is verified against its full text in the R3 session. A status of RECORDED means the bibliographic record and, where stated, the abstract support the use made of the work. It does not mean the cited passage was read.

## 2. Checks made on 30 October 2026

| Work | Tool | Result | Used for |
|---|---|---|---|
| Hevner, March, Park & Ram (2004), *MIS Quarterly* 28(1) | Crossref `verify_reference` | Matched; DOI 10.2307/25148625 | Added to the reference list (cited in Ch. 3 §3.1.1, previously without an entry) |
| Peffers, Tuunanen, Rothenberger & Chatterjee (2007), *JMIS* 24(3) | Crossref | Matched; DOI 10.2753/MIS0742-1222240302 | Same |
| Kekatos et al. (2026), ACM CPSIoTSec, pp. 129–142 | Crossref | Matched; DOI 10.1145/3847353.3847499 | Ch. 2 §2.13.6 (currency update); Ch. 5 §5.6; Ch. 6 §6.3 |
| Xin (2026), *IJMAT* 2(2), TapGuard | Crossref | Matched; DOI 10.51137/wrp.ijmat.1051 | Ch. 1, Ch. 2 §2.13.6, Ch. 6 §6.3 |
| Yan et al. (2026), PROVISO, arXiv:2610.27115 | OpenAlex record through the connector | Record and abstract found; the author list in the index record is abbreviated, marked "et al." | Same |
| Ray (2026), arXiv:2607.22868 | OpenAlex record | Record and abstract found | Ch. 2 §2.13.6; Ch. 5 §5.6 |
| Z. Liu (2026), arXiv:2610.03448 | OpenAlex record | Record and abstract found | Ch. 2 §2.13.6; Ch. 6 §6.6 |
| Update search (`verification/update_search_2026-10-30.json`) | Connector `search_papers`; 11 distinct queries recorded per record | 215 unique records, 200 not in the 25 Sep search record | Only the five records above were used. The search is **outside the PRISMA flow** and is reported separately in Ch. 2 §2.13.6. The connector returned publication years but no exact dates, so the records cannot be dated against the review's cut-off day |

No new reference was added from memory. Every added entry rests on a record returned by one of the tools above.

## 3. Known source problems (not resolved in R3)

| ID | Work | Problem | How the thesis handles it | Decision |
|---|---|---|---|---|
| OI-07 / REF-PLATT | Platt (1999) | Crossref registers the MIT Press chapter at the cited pages in 2000, under a different title | Marked CONFLICT in `REFERENCES_VERIFIED.md`; Eq. 3.3 source status NC | D-13 |
| REF-KULL | Kull, Silva Filho & Flach (2017) | Two different 2017 works exist; the AISTATS paper's record was not re-confirmed; the companion EJS paper was | PARTIAL | D-13 |
| — | Basseville & Nikiforov (1993) | Year not confirmed by a primary record; one book review cites a 1996 printing | PARTIAL | Author check |
| — | Arp et al. (2022) | USENIX venue and pages not confirmed (USENIX issues no DOIs) | PARTIAL | Author check |
| — | Elkan (2001); Guo et al. (2017); Lundberg & Lee (2017) | Proceedings pages not re-confirmed | PARTIAL | Author check |
| OI-09 | Brier (1950) | Scoring convention unconfirmed | Brier score withheld in Ch. 3, reported with its convention in Ch. 5 (SC-5) | Open |
| OI-10 | le Cessie & van Houwelingen (1992) | Penalty constant; Crossref gives the first page only | λ reported on both scales (M1) | D-13 |
| OI-11, OI-12, OI-13 | Elkan; Cox; Chow | Printed formulation not read | SOURCE NOT FULLY VERIFIED on Eqs. 3.1, 3.9, 3.10 | Full-text check |
| CF-01 to CF-08 | Davis & Goadrich; Efron; Fawcett; Hevner; Peffers; Page; Reynolds & Stoumbos; L. Wang et al. | Metadata only; content not read | Cited for background only | Full-text check |
| CF-09 | EU AI Act (Regulation 2024/1689), Arts. 12 and 14 | Read on a secondary host only | Marked [Official source] | Check against EUR-Lex |
| OI-01 to OI-06 | NEXUS (Hossain et al., 2026) | Claims resting on a Stage 1 full-text reading are not reproducible from the abstract | Marked U (unverified) in Ch. 2 and Ch. 6 Table 6.3 | Full-text check |
| — | FinVault (Z. Yang et al., 2026) | Preprint withdrawn by the authors for stated non-scientific reasons (record of 25 Sep); not re-confirmable on 28 or 30 Oct | Marked withdrawn; figures measured on it described as less confirmable | — |
| — | C. Zhang et al. (2026) | Title changed between versions | Current title used (R2) | — |

## 4. Limits of the verification tooling

1. **Matcher collisions in `REFERENCES_VERIFIED.md`.** The record column is joined by first-author surname and year. Where several entries share them (for example the four Chen 2025–2026 entries; Lin J. and Lin W. 2026; Wang C. L., H. and Z. 2025), the column lists the records of all of them. The **status** of each entry was checked by hand for the CONFLICT/WITHDRAWN and PARTIAL rows. The record text of colliding rows should be read with this in mind. This is a presentation limitation of the log, not a change in any entry.
2. **Citation resolution** (`verification/citation_check.txt`, re-run 30 Oct on the final chapters). Every in-text citation resolves to an entry. The six "unresolved" lines are parser artifacts: lower-case particles ("le Cessie"), two-author forms written in running text ("Lundberg and Lee"; "Basseville and Nikiforov"; "Reynolds and Stoumbos"), and corporate authors (OWASP; European Parliament). Each has a valid entry. The parser counts 112 entries because it skips the entry beginning with a lower-case particle; the list has 113.
3. **Retraction status.** OpenAlex flags were checked where records were retrieved. The absence of a flag is not proof of non-retraction, and an arXiv withdrawal is not a journal retraction.

## 5. What a full verification still requires

- Full-text reading of every source marked IV, NC or PARTIAL, starting with those that support an equation (Eqs. 3.1–3.3, 3.9, 3.10, 3.15, 3.16).
- Resolution of the Platt and Kull citation choices (D-13).
- Screening of full texts for the Chapter 2 review, and a dated update search in the named databases, if the supervisor requires a full-text systematic review.
