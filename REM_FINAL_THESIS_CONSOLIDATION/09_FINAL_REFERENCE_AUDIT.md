# 09: Final reference audit (28 November 2026)

**Scope.** This audit covers the references that the working copy adds or relies on, and the mathematical sources in 03. The rest of the bibliography is carried unchanged from the humanized edition, whose citation checks passed (`REM_HUMANIZED_THESIS/audit/citation_check.json`).

**Method.**
- Records were checked through Crossref (DOI lookup or bibliographic match) and OpenAlex, using the literature connector on 28 November 2026.
- Full texts were not reachable (01).

## 1. Checks run on the working copy

| Check | Result |
|---|---|
| `check_citations.py`: every reference entry is cited | **120 entries, 120 cited, 0 uncited** |
| `check_citations_reverse.py`: every citation has an entry | **94 citations, 0 with a known surname and a missing year.** Flags: "Kabbinamakki Suresh" and "Mellafe Zuvic" (the entries exist; the checker splits two-word surnames), plus "Cedar Policy", "Houwelingen", "NeurIPS", months. These are **the same flags as the DiD edition**, so they are not new errors |
| `check_thesis_numbers.py`: Chapter 4 tables against the raw-record recomputation | **498 cells, 0 mismatches** |
| `check_did_numbers.py`: DiD figures against `REM_DEFENSE_IN_DEPTH/results` | **All DiD numbers verified** |

## 2. References added to the working copy

| Entry (as added) | Verified record | Status | Reading level | Note |
|---|---|---|---|---|
| Abasıkeleş-Turgut & Gümüş (2026a), arXiv 2604.17125 | OpenAlex W7155105389 | Preprint | Abstract | **The audit of CASCADE, not CASCADE's paper.** Author spelling with a hyphen, as indexed |
| Abasıkeleş Turgut & Gümüş (2026b), arXiv 2610.33198 | OpenAlex W7224019312 | Preprint | Abstract | Spelling without a hyphen, as indexed. The a/b suffixes are used because the two author strings denote the same authors |
| Alzahrani (2026), *Sci. Rep.* 16, 1277, DOI 10.1038/s41598-025-31086-y | Crossref: registered | Peer reviewed | Abstract | The Crossref title has no colon ("PromptGuard a structured framework…"); used as registered |
| Demirol & Aydoğan (2026), *Appl. Sci.* 16(15) 7662, DOI 10.3390/app16157662 | OpenAlex W7172250210 | Peer reviewed | Abstract | — |
| Jang, Lee & Shon (**2027**), *CMC* 90(1) 1–10, DOI 10.32604/cmc.2026.090355 | Crossref: registered; issued 2027, first appeared 2026 | Peer reviewed | Abstract | **Correction:** the earlier review wrote "2026/2027". APA uses the issue year: **2027** |
| Saleem, Ahmed, Zaman et al. (2026), arXiv 2606.19660 | OpenAlex W7165368329 | Preprint | Abstract | **DOI 10.62762/TISC.2026.712476: not registered with Crossref** (re-checked). Not cited |
| DiD-edition additions (8): Gong et al. 2026 (AIS); Kabbinamakki Suresh & Gao 2026; Mellafe Zuvic 2026; Narisetty et al. 2026; Sequeira et al. 2026; K. Zhang et al. 2025; X. Zhang et al. 2026; Zhong et al. 2025 | Verified in the DiD edition (Crossref / OpenAlex); Gong et al. re-checked on Crossref today | As marked in each entry | Abstract (AIS: abstract and Crossref) | Carried unchanged (merge M5) |

**Reference count:**
- 106 entries in the humanized edition, as counted by the checker (the reconciliation's 03 states 105);
- plus 8 from the DiD edition;
- plus 6 above;
- **120 in the working copy**, all cited.

## 3. Mathematical and statistical sources (see 03)

| Source | Crossref / OpenAlex result | Thesis entry | Status |
|---|---|---|---|
| Platt | Crossref: "Probabilities for SV Machines", *Advances in Large-Margin Classifiers*, MIT Press, 2000, pp. 61–74, DOI 10.7551/mitpress/1113.003.0008 | Platt (2000), with the long title and a note that Crossref registers the short title | **Record verified; title discrepancy documented in the entry.** The printed chapter title was not checked. No 1999 record exists in Crossref (the 1999 date belongs to the technical-report version, not verified) |
| Kull et al. (AISTATS 2017) | OpenAlex W2725875209: *Beta calibration: a well-founded and easily implemented improvement on logistic calibration for binary classifiers*, AISTATS 2017; PMLR v54 PDF. No DOI (PMLR) | Exactly this paper (PMLR 54, 623–631) | **Ambiguity resolved at record level:** the thesis cites the AISTATS paper, not the *EJS* paper (DOI 10.1214/17-EJS1338SI). Whether that paper states the properties Chapter 3 attributes to it is **SOURCE VERIFICATION INCOMPLETE** (03 §3.5) |
| le Cessie & van Houwelingen (1992) | Verified earlier (`EQUATION_PROVENANCE_AUDIT.md`) | Present | The penalty's scaling constant not checked against the full text (stated in Ch. 3) |
| Field & Welsh (2007), *JRSS-B* 69(3) 369–390, DOI 10.1111/j.1467-9868.2007.00593.x | Crossref: registered | Grouped bootstrap | Verified |
| Holm (1979), *Scand. J. Statist.* 6(2) 65–70 | **Not found in Crossref** (bibliographic match returned other papers; DOI 10.2307/4615733 not registered with Crossref) | **Not in the reference list.** "Holm correction" is used, uncited, in the DiD-inserted Sections 3.15 and 4.6.12 | **SOURCE VERIFICATION INCOMPLETE.** Do not add a Holm entry until the record is checked on JSTOR. The supervisor may accept citing it from the journal record (08, item D9) |

## 4. Citation rules carried forward

1. Cite peer-reviewed versions where they exist: NEXUS, MELON, AgentDojo, Spotlight-Guard, AIS, PromptGuard, the Multilayer DiD framework (2027), DRIFT.
2. Never cite arXiv 2604.17125 as "CASCADE".
3. Never cite DOI 10.62762/TISC.2026.712476.
4. Every A-level work is worded "reports" or "describes", and no equation from such a work appears in the thesis.
