# Change Log — R3 (final verification pass, 30 October 2026)

Base: `revision_R2/chapters_md/*_R2.md` (commit `3b15dc8`). Every change below was applied by `REM_FINAL_THESIS/tools/make_r3.py` as an exact replacement that must match once. Content not listed is unchanged from R2.

| Chapter | Change | Reason |
|---|---|---|
| 1 | RQ status | Restores the [PD] status recorded in Chapter 3 §3.1.3 and the decision register; R2 had dropped it (CLAUDE.md § RESEARCH-QUESTION LOCK). |
| 1 | new prior art | Discloses prior-art records found in the 30 Oct 2026 update (Chapter 2 §2.13.6). |
| 2 | §2.13.6 | Adds the documented currency update of 30 Oct 2026 (outside the PRISMA flow). |
| 3 | SC-1 status | Makes the pending status of the mitigation-semantics decision visible in Chapter 3; R2 stated the reference without it. |
| 4 | Table 4.1 | Records the environment of the independent re-execution. |
| 4 | §4.11.2 R1–R2 | Independent re-check of the R1–R2 comparison; counts differ with the matching method, the conclusion does not. |
| 4 | §4.11.2 | Adds the independent re-execution and its exact outcome. |
| 5 | §5.1 provenance | States the independent reproduction. |
| 5 | §5.6 limits | Adds the closed-loop identifiability limit and the published precedent for offline replay (Chapter 2 §2.13.6). |
| 5 | §5.6 memory | Corrects a number that did not match its cited artifact: results/pilot_R2/latency_memory_profile.json records a median of 4,364 bytes; 2.9 KB was the R1 value. |
| 5 | §5.6 latency | Records that the third execution stays within the reported range (REM configurations: median 0.137–0.156 ms, p95 0.400–0.476 ms; reproduction_comparison.json). |
| 5 | Ch5 title | Aligns the chapter title with the six-chapter structure requested by the author while keeping its exploratory status in the title. |
| 6 | §6.3 new prior art | Adds the closest records from the currency update. |
| 6 | §6.5 limitation | Adds the literature-currency limitation. |
| 6 | §6.6 classifier | Grounds the classifier-selection future work in the update record. |
| 2 | §2.2.5 reviewer | Aligns the text with the review record, which names AI assistance; the chapter did not disclose it. |
| 2 | §2.13.4 item 5 | Same correction in the limitations; "one person" did not state the AI assistance recorded in the review files. |
| 5 | §5.2 intervals | States that percentile intervals over nine groups need not reach nominal coverage (examiner review finding). |
| 2 | Eq. 2.3 encoding | Same mathematics; the superscript asterisk is encoded so that it renders in both Word and LibreOffice. |
| 3 | Eq. 3.9 encoding | Same mathematics; rendering fix as for Eq. 2.3. |
| 3 | Eq. 3.20 encoding | Same mathematics; absolute-value bars encoded so that they render in LibreOffice. |
| All | Per-chapter reference lists replaced by one consolidated list (113 entries; `chapters/REFERENCES.md`) | Removes 21 cross-chapter formatting inconsistencies; Chapter 2 entries, which passed the review's metadata verification, are preferred where versions differ |
