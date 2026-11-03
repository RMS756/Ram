# REFERENCES AUDIT — five-chapter thesis

**Reference list used in the build:** `REM_FINAL_THESIS/chapters_R5/REFERENCES_R5.md`
(unchanged from R5; inserted by `tools/build_5ch.py` as the unnumbered "References" section).
**No reference was added, removed or edited for the five-chapter version.** No DOI was created
or altered. The restructuring did not change any in-text citation; it changed only section, table
and figure numbers.

## 1. Counts

| Item | Value | Source |
|---|---|---|
| Entries in the reference list | **114** (R4: 113, plus Kanaker et al., 2026 added in R5) | paragraph count of `REFERENCES_R5.md` |
| Entries counted by the citation parser | 113 | `tools/check_5ch.py` → `audit/qa_logs/content_preservation.txt` (one entry is merged by the parser's regex; the same as in R5) |
| Distinct in-text author–year keys resolved to an entry | 92 | same log; identical to R5 (`verification/citation_check_R5.txt`) |
| "Unresolved" in-text citations reported by the parser | 6, **all parser false positives**, identical to R5 | see §3 |
| Entries never matched by an in-text citation | 3, **all parser false positives** | see §3 |
| Entry types (verification table, 113 rows) | 71 peer-reviewed/book; 38 preprints; 2 official sources; 1 working paper; 1 withdrawn preprint | `REM_FINAL_THESIS/REFERENCES_VERIFIED.md` |

## 2. Verification status (from `REFERENCES_VERIFIED.md`, 30 Oct 2026, plus the R5 addition)

| Status | Entries | Meaning |
|---|---:|---|
| RECORDED | 90 + 1 (Kanaker et al., 2026) | metadata confirmed against Crossref/OpenAlex/arXiv; review claims checked against the abstract or record |
| PARTIAL | 21 | at least one detail unconfirmed (venue pages, year of printing, author list, body-text claims) |
| CONFLICT / WITHDRAWN | 2 | Platt (unresolved citation conflict, D-13 / REF-PLATT); Yang et al. 2026 *FinVault* (withdrawn preprint, cited as withdrawn) |

**No entry is verified against its full text.** Full texts were unreachable under the session
network policy in every session. All literature evidence is therefore record-level (metadata and
abstract). This applies to Kanaker et al. (2026) as well: described at abstract level only
(`reports/KANAKER_2026_UNRESOLVED_CLAIM_ISSUES.md`, U-5).

### PARTIAL entries (21)

Arp et al. 2022; Basseville & Nikiforov 1993; Elkan 2001; Guo et al. 2017; Hossain et al. 2026
(NEXUS); Jackson 2025; Kull et al. 2017; le Cessie & van Houwelingen 1992; J. Lin et al. 2026
(VIGIL); W. Lin et al. 2026 (DreamGuard); Liu et al. 2026 (SafeAgent); Lorden 1971; Lundberg & Lee
2017; Niculescu-Mizil & Caruana 2005; She et al. 2026; C. L. Wang et al. 2025 (MI9); H. Wang et al.
2025 (ProbGuard); Z. Wang et al. 2025 (AgentVigil); C. Yang 2026 (AgentTrust); Yuan et al. 2024
(R-Judge); C. Zhang et al. 2026. The unconfirmed detail of each is stated in the "Verification
record" column of `REFERENCES_VERIFIED.md`.

Several of these support core methodology (Elkan, Guo, le Cessie & van Houwelingen, Lundberg & Lee,
Basseville & Nikiforov). For each, the existence and the attributed content were confirmed at
record level; what is unconfirmed is a bibliographic detail (pages, venue year), not the existence
of the work. These should be checked against the publishers' pages before submission.

### Known discrepancy between the verification table and the reference list

`REFERENCES_VERIFIED.md` (30 Oct) lists Platt as **1999**. The reference list and all in-text
citations use **2000** with the DOI `10.7551/mitpress/1113.003.0008` registered by Crossref
(R4 correction). The year question remains the open item D-13 / REF-PLATT. The thesis text is
internally consistent (year 2000 in all 7 year-bearing citations: Chapter 1 ×1, Chapter 2 ×3, Chapter 3 ×3; no occurrence of 1999).

## 3. Parser false positives (carried over unchanged from R5)

| Reported item | Why it is not an error |
|---|---|
| ("Houwelingen", 1992) | second-author surname of "le Cessie & van Houwelingen, 1992" |
| ("Lee", 2017) | "Lundberg and Lee (2017)" |
| ("Nikiforov", 1993) | "Basseville and Nikiforov (1993)" |
| ("Project", 2025) | corporate author "OWASP Gen AI Security Project, 2025" |
| ("Stoumbos", 1999) | "Reynolds and Stoumbos (1999)" |
| ("Union", 2024) | corporate author "European Parliament & Council of the European Union, 2024" |
| entry ("Chandola", 2012) never matched | cited as "Chandola et al. (2009, 2012)" (2 occurrences, Chapter 2); the parser reads only the first year |
| entries ("Project.", 2025), ("Union.", 2024) never matched | corporate authors; matched by hand above |

## 4. Rules applied

- No reference or DOI was fabricated; none was changed in this version.
- Preprints are labelled as preprints; the withdrawn preprint is labelled as withdrawn.
- Elkan (2001) and Chow (1970) are cited as support for the expected-cost principle and the
  reject option respectively; the thesis does not present either as the source of REM's four-action
  architecture (§1.8, §3.7, §3.13).
- Kanaker et al. (2026) is cited only as a source and comparison (§2.9.1, §2.13.7, §3.7.3, §3.7.5,
  §4.15). A co-author of that paper (Dr. Husam Fakhouri) is named on the title page as
  Co-Supervisor; the potential conflict of interest is noted for the supervisor
  (UNRESOLVED_SUPERVISOR_DECISIONS.md, N-6).

## 5. Before formal submission

1. Resolve D-13 (Platt year) and REF-KULL.
2. Check the 21 PARTIAL entries against publisher pages; complete abbreviated author lists
   (Fu et al. 2024; X. Jia et al. 2026 are marked "author list abbreviated").
3. Read the full text of every source used for a methodological or numerical claim (Chapter 3
   Table 3.16 sources first).
4. Confirm the citation style required by Al-Balqa Applied University (APA 7 is assumed).
