# References Verification Report

**Reference list evaluated:** `REM_FINAL_THESIS/chapters_R4/REFERENCES_R4.md`, at commit `9ab3f9e`. It has 113 entries, and its status register is in `REM_FINAL_THESIS/REFERENCES_VERIFIED.md`.

**What the evaluator did on 1 Nov 2026:**
1. Read the status register and the R4 source-verification log.
2. Spot-checked six entries against Crossref through the literature connector.
3. Ran a rough cross-check that every reference is cited and every citation is listed. This used regex matching of surname and year, so it is not exhaustive.
4. Searched the front matter for the declaration of AI use.

**What the evaluator did not do:**
- read full texts;
- run any similarity or plagiarism check.

## 1. Composition

| Type | Entries |
|---|---:|
| Peer-reviewed article or book | 71 |
| Preprint | 38 |
| Withdrawn preprint | 1 |
| Official source (EU AI Act, OWASP) | 2 |
| Working paper | 1 |
| **Total** | **113** |

About a third of the entries (38 of 113) are preprints. This is normal for a 2025–26 agent-security topic. It does, however, raise the share of evidence that is not peer-reviewed, and Chapter 2 grades the evidence levels accordingly.

## 2. Verification status (thesis's own register)

| Status | Entries | Meaning |
|---|---:|---|
| RECORDED | 90 | Metadata confirmed against Crossref or OpenAlex; claims checked at abstract or record level |
| PARTIAL | 21 | At least one detail is unconfirmed: venue, pages, year or author order |
| CONFLICT / WITHDRAWN | 2 | Platt (title and year conflict); FinVault (withdrawn preprint) |

**No entry was verified against its full text.** The thesis states this openly (Ch. 2 §2.2.6; `REFERENCES_VERIFIED.md`). Every claim attributed to a source therefore rests at best on its abstract or record. That includes method details, numbers and equation forms.

## 3. The evaluator's spot-check

| Reference | Crossref result | Match |
|---|---|---|
| Greshake et al. (2023), AISec, pp. 79–90 | Found; metadata agree | ✓ |
| Calboreanu (2026), *Front. AI* 9:1800407 | Found | ✓ |
| She et al. (2026), ASE, pp. 3036–3048 (ProvenanceGuard) | Found, peer-reviewed | ✓. **However, Ch. 2 line 571 calls it a "preprint"** (m-3) |
| S. Wang (2026), *Electronics* 15(13):2829 | Found | ✓ |
| Castro-Maldonado et al. (2026), *AI* 7(3):80 | Found | ✓ |
| Chow (1970), *IEEE TIT* 16(1):41–46 | Found | ✓ |

All 6 sampled entries exist with matching metadata. **No fabricated reference was found in the sample.** A sample of 6 out of 113 cannot exclude errors elsewhere. The 21 PARTIAL entries should be completed.

## 4. Specific problems

| ID | Problem | Severity |
|---|---|---|
| R-1 | **Platt (2000).** Crossref registers the chapter as "Probabilities for SV Machines" (pp. 61–74), while the thesis prints the commonly cited title. The note in the list says so, and the printed chapter was never inspected (D-13). Platt is the source of the adopted calibrator, but its formulation is coded NC (never read). | MAJOR (for the core method) |
| R-2 | **FinVault (Yang et al., 2026)** is a withdrawn preprint. It is cited and marked as withdrawn. Nothing should rest on it; Ch. 2 uses it only as context. | MINOR, if it stays context only |
| R-3 | **Seven equation sources** are coded IV or NC (Ch. 3 Table 3.17): Cox, le Cessie & van Houwelingen, Platt, Elkan (printed threshold form), Chow and Page. The equations are standard and were verified by derivation, so the risk lies in attribution, not correctness. | MAJOR (M-12) |
| R-4 | **ProvenanceGuard** is called a "preprint" in the text, although the peer-reviewed version is the one cited. | MINOR (m-3) |
| R-5 | **Basseville & Nikiforov:** the year (1993 vs a 1996 printing) is not confirmed from a primary record. | MINOR |
| R-6 | **Arp et al. (USENIX 2022):** venue and pages are not confirmed (USENIX issues no DOIs). | MINOR |
| R-7 | **Literature reach.** One index was searched, the top 24–25 records per query were screened, and recall of the named prior art was 3/13 (M-4). The reference list is authentic but **not demonstrably complete**. | MAJOR |
| R-9 | **The verification statements conflict.** Ch. 3 Table 3.17 codes Guo, Kull, Elkan (Eq. 1 form), Lundberg & Lee, Basseville & Nikiforov and Naeini as **FV**, which its legend (line 1001) defines as "formulation checked against the source". This is contradicted elsewhere: `REFERENCES_VERIFIED.md` says that "no entry is verified against its full text: full texts were unreachable in every session", and `SOURCE_VERIFICATION_LOG_R4.md` says "No source reached level F in R3 or R4". The FV codes seem to go back to September session records (for example, the "25 Sep upgrade via a hosted copy" for Lundberg & Lee in `chapter2/CHAPTER2_PARTIAL_SOURCES_REVIEW.md`). For Elkan, `REM_STAGE2_INPUT_PACKAGE/PAPER_READING_PACK/PAPER_DOWNLOAD_STATUS.md` says that the author-hosted copy was "read in Stage 1". However, the repository holds no stored copy, excerpt or hash of any FV source: `PAPER_READING_PACK/papers/` contains only a README. **Basis:** C (concern; these earlier-session checks cannot be verified from the repository) | MAJOR (consistency of the verification record) |
| R-8 | **Citation and list consistency.** The rough regex check found no cited surname–year pair missing from the list, and both official sources are cited. The check is approximate: it does not handle all name formats. | Information |

## 5. Academic integrity

| Item | Status |
|---|---|
| Fabricated references | None found in the 6-entry sample. The thesis's register reports 90 records with confirmed metadata |
| Misattributed claims | Cannot be excluded: no full texts were read. Claims are limited to abstract level, as the text says |
| Citation of withdrawn work | FinVault, flagged in the list |
| **Plagiarism or similarity check** | **Not performed.** No Turnitin or iThenticate report exists in the repository. **Plagiarism has not been excluded** |
| **Declaration of AI use** | **Incomplete.** The front matter (line 46) gives a factual note that an AI coding assistant assisted with screening records, the software, the analyses, the AI-only label inspection and "the drafting and verification of this text". It states explicitly that it is not the university's declaration. The author must complete that declaration and the institution's AI policy must be checked. Given how much of the text was drafted by AI, this is a **critical precondition for submission** (C-5) |
| Authorship | No student name is supplied ("[NAME NOT SUPPLIED]"). The student's own intellectual contribution is not separable from the assistant's in the repository record |

## 6. Verdict

**The references appear authentic.** The sampled entries matched, and the register is transparent.

**They are not verified to examination standard:**
- no full text was read;
- the core calibration source was never inspected;
- 21 entries are partial.

**Integrity checks** are outstanding:
- the similarity report;
- the formal declaration of AI use;
- confirmation of authorship.

**Required:**
- obtain and read the full texts of at least every source that underpins an equation or a quantitative comparison;
- complete the 21 partial records;
- fix R-4;
- run the institution's similarity check;
- make the formal declaration of AI use.
