# Final academic compliance audit: REM defence-ready thesis

| Item | Value |
|---|---|
| Date | 26 November 2026 |
| Branch | `claude/rem-defence-ready-thesis-20261126` |
| Audited commit | `5f9682e` |
| Corrections | in the commit that adds this file |
| R8 source | Unchanged: `git diff 557af37 HEAD -- REM_FINAL_SUBMISSION` is empty. REM code, configs and earlier study folders are also unchanged. |
| Thesis after corrections | `REM_Master_Thesis_Defence_Ready.docx` / `.pdf`, 272 pages (24 preliminary + 248 numbered), A4 |
| Live experiments | None initiated. No new experiment was run. |
| Tests after corrections | `tests/test_defence_ready_thesis.py` (5 tests, including a regression test for the corrected wording and the 21-backbone count); full suite 828 passed, 27 skipped, 1 xfailed, 0 failed |
| Companion documents | `ABLATION_LAYER_COVERAGE_MATRIX.md`, `FRAMEWORK_COMPARISON_VALIDATION.md`, `FINAL_SUBMISSION_CHECKLIST.md` |

## Verdict

| Question | Verdict |
|---|---|
| Are the supervisor's two requirements addressed? | **Yes.** Both are addressed in dedicated, complete sections (4.4 and 4.5), with the limits of each stated. |
| Is the ablation study defensible despite the inability to isolate every layer? | **Yes, as a component-level ablation of the five-layer design.** It is not a complete layer-level ablation, and after the corrections below the thesis no longer implies that it is. |
| Are the framework comparisons academically fair? | **Yes.** The one quantitative comparator (Progent's manual policy, decided by Progent's own code) outperforms REM offline, and the thesis says so. Its benchmark-specific list is disclosed. DRIFT and MELON are explicitly not measured for security. |
| Are the numerical results consistent? | **Yes, after one semantic correction.** 466 printed cells match a fresh recomputation from the raw records. One inherited R8 phrase misdescribed what the counts meant ("661 of the 672 prevented attacks") and was corrected in six places. |

## 1. Requirement-to-evidence matrix

Page numbers are printed page numbers of the corrected PDF.

| Supervisor requirement | Where addressed | Evidence | Status |
|---|---|---|---|
| **R1. Ablation study of the REM design layers** | Section 4.5 (pp. 141–178): 4.5.1 introduction with an explicit statement of what can be isolated; 4.5.2 motivation; 4.5.3 design; 4.5.4 layer-to-implementation mapping (Table 4.24, Figure 4.4); 4.5.5 variants and status (Table 4.25); 4.5.6 metrics; 4.5.7 results (Tables 4.26–4.34, Figure 4.5); 4.5.8 exploratory extensions; 4.5.9 statistics; 4.5.10 discussion; 4.5.11 limitations; 4.5.12 conclusion | Two pre-registered studies (19 and 21 Nov) on the same 3,313 episodes, identical on every shared arm. Secondary populations: 681 and 2,113 episodes. Every variant is paired with the full framework (McNemar test, grouped bootstrap). | **Addressed**, with isolation limits stated (see the coverage matrix) |
| R1, carried into the conclusions | Table 4.59, row 14; 4.6.11, threat 21; 4.6.12; Table 5.1, RQ4; Table 5.3, row 10; 5.6, item 12; 5.8; abstract | Consistent with Section 4.5 | Addressed |
| **R2. Comparison of REM with existing frameworks (Progent, DRIFT, MELON, others)** | Section 4.4 (pp. 109–140): 4.4.1 scope and kinds of evidence; 4.4.2 selection (Table 4.10); 4.4.3 frameworks; 4.4.4 15-dimension architecture comparison (Table 4.12, Figure 4.1); 4.4.5 mechanism; 4.4.6 design (Table 4.13); 4.4.7 quantitative results (Tables 4.14–4.23, Figures 4.2–4.3); 4.4.8 fairness; 4.4.9 discussion; 4.4.10 limitations; 4.4.11 conclusion | Progent: quantitative offline replay with the authors' code. DRIFT: code-level comparison plus a scripted integration test. MELON: paper- and code-level comparison plus a scripted integration test. Defenses distributed with AgentDojo: descriptive comparison with recorded runs. Others: literature level (Table 4.11). | **Addressed**, with the kinds of evidence kept apart |
| R2, carried into the conclusions | Table 4.59, rows 13 and 15; threats 16 and 22; Table 5.2, O3; 5.6, item 10; 5.7, item 4; 5.8; abstract | No superiority claim anywhere | Addressed |
| No live experiments required | 4.1.4, 4.4.1, 4.4.10; Chapter 5 | No live result is claimed. Live evaluation is future work, not a blocking limitation. | Complied |

## 2. Five-layer ablation coverage (summary; details in `ABLATION_LAYER_COVERAGE_MATRIX.md`)

| Layer | Classification |
|---|---|
| Input & Context | **Indirect evaluation only.** It computes no evidence; its labels reach the decision only through A3b and D2. Hygiene changed 0 of 16,727 outputs. |
| Detection | **Partial component-level.** x_ctx2 alone (A2a) and with x_beh1 (A2b, which removes all of the implemented signal); classifier x_ctx1 not implemented. |
| Behavioral Analysis | **Partial component-level.** Its behavioral group (A3a) and its action group (A3b) are removed separately, never together. |
| Decision Engine | **Partial component-level, with every component covered** (A4a–A4e). Whole-layer removal is the no-defense reference by construction. |
| Mitigation | **Complete layer-level** (A5, shadow mode) |

**Defensibility.** The study can be presented as an ablation study of the REM design because:
- every implemented component that can affect a verdict was removed at least once;
- each removal is paired on identical episodes;
- the one layer that can be removed without inventing inputs was removed whole;
- the architectural reasons for the remaining limits come from Chapter 3 itself and are stated.

## 3. Corrections made in this audit (each justified by evidence)

| # | Location | Problem | Evidence | Correction |
|---|---|---|---|---|
| 1 | Abstract (EN, AR); 1.11 item 8; 4.5.7 (relabelled 19-Nov text); 4.6.12; Table 5.1, RQ4; 5.8 | "The learned decision prevents 661 of the **672 prevented** attacks". REM prevents 661 (672 without defense − 11 with REM); 672 is the no-defense count. Inherited from R8. | `number_verification.json`: B0 672, A0 11, A4a 672; 661 / 0 discordant | "accounts for all 661 attacks that REM v1.0 prevents (of 672 reached without defense)". Table 4.59, row 12 was already correct and is unchanged. |
| 2 | 4.5.5 coverage paragraph | Said the Decision Engine is "ablated as a whole functional unit". A4a keeps the predicates. | Table 4.25 | States that only the Mitigation layer is ablated whole, and that the Decision Engine is ablated component by component |
| 3 | 4.5.1 | The isolation limits appeared only from 4.5.4 onwards | — | A "What can be isolated" paragraph added at the start |
| 4 | Abstract (EN, AR); 1.11 item 8; Table 5.3, row 10; status page | "Layer-wise ablation" / "complete ablation study" overstated the coverage | Coverage matrix | "Ablation of the components of the five layers" / "component-level ablation", with the limits stated |
| 5 | Status page | "Complete comparison" | DRIFT and MELON have no outcome measurement | "Comparison" |
| 6 | Table 4.12, row 15 (REM) | "Detection and behavioral evidence add nothing measurable" | A3a: benign completion +10.5 [1.2, 22.6] | "The detection indicator has no measurable effect, and behavioral evidence lowers task completion" |
| 7 | 4.4.7, "They lose different tasks" | Progent fails "user tasks 14 and 15". True for the primary population only. | Raw records: second population zero-completion tasks are ut9 and ut14 | Population-specific statement |
| 8 | Table 4.12, row 10 (DRIFT) | "per two-step episode" | Mean of 2.06 executed tool calls, from 1 to 5 | "per episode (about two tool calls per episode)" |
| 9 | 4.4.9 | DRIFT adds calls "to each step" | Measured per episode | "to each episode (about six to seven more …)" |
| 10 | 4.4.9 | Progent "reaches the same protection" | 0 against 11 attack goals | "at least the same protection" |
| 11 | 4.4.5 layer table | REM "All five layers" | Detection classifier not implemented | "as designed (the Detection layer's classifier is not implemented)" |
| 12 | 4.4.7 (R8 text on the distributed defenses) | "MELON was not executed" | Official code executed with a scripted agent on 19 Nov | "not executed with a language model; its official code ran only with a scripted agent" |
| 13 | 4.3.4 | 19-Nov study described as "nine arms" | 8 ablation arms + no-defense reference + REM | "eight ablation arms and the no-defense reference" |
| 14 | References: DRIFT | No page range; author provenance not stated | Crossref: pp. 92825–92853; Crossref registers the third author as "CHIU Chun", while the official README gives "Hung-Chun Chiu" | Pages added; provenance stated in the entry |
| 15 | References: AgentDyn | Provenance of the author list | OpenAlex lists 6 authors and shows 3; the repository README gives all 6 | Provenance stated |
| 16 | References: Progent | "Official code repository read, not executed" | The enforcement code at `3e79753` was executed as a decision rule on 22 Nov | Note updated |
| 17 | `tools/verify_numbers.py` | The 19-Nov call-level numbers came from a one-off step, not from the script | Fresh re-run lacked the block | Folded into the script; reproduces the earlier values exactly and adds the remaining arms |

None of these changes alters a result, a design value, the title, the scope or the five-layer architecture.

## 4. Numerical verification

Verified by a fresh run of `verify_numbers.py` from the raw records (about 4.5 min), then `check_thesis_numbers.py`:

| Item | Value |
|---|---|
| REM attack goals reached | 11 / 2,979, ASR 0.37% [0.10, 0.68] |
| REM benign tasks completed | 105 / 334 |
| Progent attack goals reached (offline replay, own checker) | 0 / 2,979 |
| Progent benign tasks completed | 154 / 334 |
| Backbones, primary population | **21**. "22" occurs nowhere in the thesis (Markdown sources, front matter and PDF text searched). The three earlier phase documents that say 22 are recorded as errata in `UNRESOLVED_ISSUES.md`. |
| Printed cells cross-checked | **466, 0 mismatches.** Counts in Tables 4.14, 4.26, 4.28, 4.29 and 4.30; point estimates, 95% intervals, discordant counts and McNemar p in Tables 4.15, 4.27 and 4.31. Tolerance is 0.05 for one-decimal rounding of values stored to two decimals; two cells are exact half-ties (−55.15, −12.35). |
| Cross-study identity | 7 shared arms × 3,313 episodes identical. The 22-Nov records equal the 21-Nov records on every shared arm. |

**Units.** Tables and their headers keep the four units apart:
- **attack goals reached:** "attack outcomes", the benchmark's security check, per attacked episode;
- **attacked episodes with an attack-labelled call executed;**
- **attack-labelled calls withheld:** per call, of 907 / 202 / 559;
- **benign tasks completed:** per benign episode.

The text uses "attacks", "successful attacks" and "attack outcomes" for the same episode-level quantity (R8 wording). That is a stylistic inconsistency, not a mixing of units: no sentence counts calls as episodes or the reverse. The one unit error found (correction 1) has been fixed.

## 5. Research questions and objectives

- **RQ status.** Section 1.7 states that the RQs are derived from the approved objectives, that the proposal contains none, and that they remain proposed ([PD], D-10). Section 5.2 repeats this. They are nowhere called approved.
- **Answerability.** Each RQ is answerable by the methodology used:

| RQ | Answered by |
|---|---|
| RQ1 | Offline held-out prediction |
| RQ2 | Observe-only analysis and replay against B1 |
| RQ3 | Replay, observe-only analysis and timing; the limit of residual success under NO-ADAPT is stated |
| RQ4 | Ablations. RQ4 names evidence groups, calibration and tiers; the layer-level framing added for the supervisor's requirement extends it without changing its wording. |

- **Objectives (Table 5.2).** O1–O3 are each answered with "achieved" and "not achieved" columns. O3 now names the Progent replay, the 15-dimension comparison and the DRIFT and MELON limits.
- **Chapter 5 claims.** No claim beyond the evidence: 5.8 states that the findings "do not show that REM protects a live agent, and … do not rank REM against any published defense".
- **Design values.** They remain declared, not approved (status page, Chapter 3, Appendix B, threat 1).

## 6. Reference audit (new and directly affected entries)

| Reference | Classification | Basis |
|---|---|---|
| H. Li et al. (2025), DRIFT, NeurIPS 2025 | **Official repository verified; metadata verified; full paper not verified (abstract only)** | Crossref and OpenAlex re-checked on 26 Nov (DOI registered; title, venue, pages, 6 authors); README author list; code read and executed |
| H. Li et al. (2026), AgentDyn, arXiv:2602.03117 | **Metadata verified; official repository verified; abstract only** | OpenAlex (title, year, ID, 6 authors, first 3 shown); repository README (all 6). The arXiv DOI is not registered with Crossref (it is a DataCite DOI); DataCite was not reachable. |
| T. Shi et al. (2026), Progent v3 | **Full paper verified; official repository verified** | Read in full on 16 Nov; enforcement code executed |
| Zhu, Yang, et al. (2025), MELON, ICML | **Full paper verified; official repository verified** | Full text read on 11 Nov; PMLR pages; code hash-pinned |
| Debenedetti et al. (2024), AgentDojo | **Full paper and official repository verified** (R8 status) | Earlier R8 verification; package in use |
| Debenedetti et al. (2025), CaMeL | **Official repository verified; full paper not verified** | README only (R8 note) |
| NEXUS, aiAuthZ, Kairos, PACT, ROPE, CapLite | **Abstract only** (NEXUS and aiAuthZ also repository) | R8 notes; threats 15 and 20 |

All 105 entries are cited and every citation has an entry. No bibliographic detail was invented. Two items still **require manual verification** against the published PDFs: the DRIFT third author's name form, and the full AgentDyn author list.

## 7. Document quality

| Check | Result |
|---|---|
| Table numbering | Sequential, 4.1–4.59. No lettered or placeholder numbers remain. Every "Table x.y" reference points to an existing caption. |
| Figure numbering | Sequential, 4.1–4.11; every reference resolves |
| Cross-references | 99 R8 section references remapped. Every remaining Chapter-4 section reference resolves to a heading. Duplicates in lists merged. |
| Citations | 105 / 105 cited; no orphan citation |
| Table of contents, LoT, LoF | 179 page references checked. One reported mismatch is a checker false positive ("5.1 Introduction" also matches "4.5.1 Introduction"). |
| Broken tables | Three over-wide tables were restructured earlier; the corrected pages were re-rendered and inspected. Some inherited R8 numeric tables wrap cells but are readable. |
| Repeated content | Kept by the user's choice: the R8 units inside 4.4.7 and 4.5.7, and Table 4.11 (which lists Progent and MELON again). The figures are identical where repeated. Could be trimmed if the supervisor asks. |
| Terminology | "defense" (US spelling) throughout the body; the title-page edition line says "Defence-ready". Cosmetic; left. Variant labels and rule labels A1/A2 are disambiguated in 4.5.5. |
| Abstract accuracy | Every number checked; corrections 1 and 4 applied |
| Title, scope, five-layer architecture | Unchanged. No sixth layer; no new chapter. Equation set unchanged (checked by `make_r9.py`). |
| Approval claims | None. Status page: "It has not been formally approved, and no approval is implied." |

## 8. What must be corrected before sending, and what may remain as a stated limitation

**Must be corrected:** all items found by this audit were corrected (Section 3). Before sending, the student must also do the following (not changeable by this audit):
1. Open the DOCX in Word with Times New Roman installed and update all fields (TOC, LoT, LoF). Check the page breaks of Tables 4.12, 4.25 and 5.3.
2. Have the new Arabic abstract paragraphs checked by a native speaker.
3. Check the DRIFT and AgentDyn author lists against the published PDFs.
4. Leave the committee, declaration, dedication and acknowledgement pages for the university or complete them as required.

**May remain as stated limitations:**
- The Input & Context layer is not independently isolatable (architectural).
- The Detection classifier is absent.
- The Behavioral Analysis groups are never removed together.
- Offline replay (NO-ADAPT), one benchmark, development data, few clusters.
- DRIFT and MELON are not measured for security; the DRIFT paper was read at abstract level only.
- Progent's policy is benchmark-informed.
- RQs and design values are not approved.
- Content repeated by the user's choice.
