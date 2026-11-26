# Unresolved issues of the defence-ready edition (26 November 2026)

None of these issues blocks discussion of the thesis. Each needs a decision or a manual check by the student or the supervisors.

## 1. Approvals that do not exist

| Item | Status | Where stated |
|---|---|---|
| Formal approval of the thesis | **Not given.** The committee page, declaration, dedication and acknowledgement are placeholders. | Front matter; Status page |
| Research questions | Derived from the approved objectives and labelled [PD]; not confirmed by the supervisor | Section 1.7; Section 5.2 |
| Design values: costs and loss grid, consequence tiers, predicates, feature set, label rule | Declared, not approved. Every result is exploratory by label. | Chapter 3; Section 4.6.11 (threat 1); Appendix B |
| REM v1.1 (without behavioral evidence) | Proposed amendment; not adopted | Sections 3.13, 4.6.8 |
| Mitigation semantics, replay amendment (NO-ADAPT) | Pending supervisor decision | Appendix B |
| University template, faculty, department and degree title | Not verified against official records; the layout is an assumed A4 style | Status page |
| Arabic abstract | Draft translation prepared with AI assistance. The new paragraph on the ablation and on Progent needs a native-speaker check. | Status page |

## 2. References that need manual verification

| Reference | What was verified | What was not |
|---|---|---|
| H. Li et al. (2025), DRIFT, NeurIPS 2025, DOI 10.52202/085713-2791 | Bibliographic record and abstract (OpenAlex W4415110937); official code `SaFo-Lab/DRIFT@6fd3df4` read and executed with a scripted agent | **Full text not read** (not reachable from the working environment). Check the author list, title capitalisation and proceedings volume against the published PDF. |
| H. Li et al. (2026), AgentDyn, arXiv:2602.03117 | Bibliographic record (OpenAlex W7127632747); repository read | Full text not read; check authors and title |
| NEXUS, aiAuthZ, Kairos | Abstracts; repositories for NEXUS and aiAuthZ | Full texts not read (Section 4.6.11, threat 15) |
| PACT, ROPE, CapLite (November 2026) | Abstracts; ROPE repository | Full texts not read (threat 20) |
| CaMeL | Official repository and arXiv record | Not read in full |
| MELON (Zhu, Yang, et al., 2025) | Paper and code audited on 19 November 2026; code re-checked against the pinned hash | — |
| Progent (T. Shi et al., 2026), version 3 | Read in full on 16 November 2026 | The paper evaluates generated policies; the replayed manual policy is not a configuration of the paper (stated) |

The citation checkers found every reference cited and every citation listed (105 entries). They do not verify the bibliographic fields themselves.

## 3. Errata in earlier repository documents (not changed here; recorded)

**Backbone count.** `REM_COMPARATIVE_EVALUATION_PHASE/02_PROGENT_IMPLEMENTATION_AND_RESULTS.md` (line 69), `06_ABLATION_RESULTS.md` (line 16) and `09_THESIS_READY_RESULTS.md` (line 20) state that population P1 has **22** backbones. Recomputation from the raw records gives **21** (`audit/number_verification.json`, `S21_episode_level_ablation.P1_primary.backbones`).

- The thesis uses 21.
- None of those documents' counts or statistics depends on this number.
- The documents are committed deliverables of an earlier phase and were left unchanged. This entry is the erratum.

**MELON threshold.** Earlier phase documents described MELON's detection threshold as 0.1, from the README. The code compares cosine similarity with a hard-coded **0.8**, and the README value is unused. The thesis (Section 4.4.3, Table 4.12) uses the code's value.

## 4. Scope of the evidence (stated in the thesis; may be raised by the committee)

1. **The Input & Context layer is not independently ablated.** It computes no evidence (Chapter 3, Section 3.4), and removing its labels would leave the action features, x_beh1 and predicate D2 without inputs. Its contribution is seen only through variant A3b. If the committee requires a direct Layer-1 ablation, it needs a design decision on what a "no-provenance" input would be. **That would be a design change and needs a supervisor decision.**
2. **The Detection layer's classifier x_ctx1 is absent** (decision D-8). The only Detection component is the instruction-pattern indicator.
3. **Some arms appear twice in Section 4.5.7.** The earlier units were kept inside the new sections, by the user's choice. Some arms therefore appear both in the new layer tables (4.26–4.29) and in the detailed tables of the 19-November study (4.30–4.34), under the same variant names. The figures are identical, because the cross-study identity was verified on every episode. The repetition can be removed if the supervisors prefer a shorter chapter.
4. **DRIFT and MELON have no security or utility result.** Both need a language model. No credential, budget or model choice was authorised, and none was assumed.
5. **Progent's policy is benchmark-informed.** Two of its permitted recipients come from task solutions, and the attacker's account is excluded by construction (Section 4.4.8). Its zero attacks are not evidence about other attackers.
6. **Single benchmark, replay only (NO-ADAPT), development data, few clusters** (9 attack and 16 task clusters).

## 5. Formatting

| Item | Status |
|---|---|
| Page-reference checker | Reports one mismatch for "5.1 Introduction". It is a false positive: the string also matches "4.5.1 Introduction". The TOC page, 210, is correct (`audit/qc_checks.txt`). |
| Page 184 | Holds only a table and a figure, as in R8's layout of that unit |
| Wide tables | Some inherited R8 tables with many numeric columns still wrap cell contents onto several lines; they are readable. Table 5.3 is printed with three columns instead of six, with the same cell text. |
| Supplement | Keeps its fifth-edition numbers ("S-"). The R8→R9 numbering correspondence is in THESIS_REVISION_LOG.md. |
| Fonts | Times New Roman is not installed in the build environment; the metric-compatible Liberation Serif is used. Before submission, open the DOCX in Word with Times New Roman and update all fields (TOC, LoT, LoF); page numbers may shift slightly. |
