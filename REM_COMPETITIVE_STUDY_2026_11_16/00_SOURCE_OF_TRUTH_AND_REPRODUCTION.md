# Source of truth and reproduction audit (16 November 2026)

## 1. Attachments received

| Attachment | Identification | Status |
|---|---|---|
| `REM_G3_L4_Integration_Review_Package_2026-11-16.zip` | sha256 `da4eca6f5daf72d0db508fc1ec6272b51047b92b5c0ae528bda108fb60c2f40f`; 25 files in `changes/`, a final-state patch, an 8-commit series, `manifest.json`, `LOCAL_COMMIT_LOG.txt`, an Arabic design note and a diagram | received; every file in `changes/` matches its hash in `manifest.json` |
| Progent paper | *Progent: Securing AI Agents with Privilege Control*; Shi, He, Wang, Li, Wu, Guo, Song; arXiv:2504.11703v3 [cs.CR], dated 14 May 2026; 17 pages; headed "Preprint"; sha256 `cd38f8f70cd172572b01d9d15a9c4fd87751692e155f0e1d9c003b4903520e62` | received; read in full (pages 1 to 17, including Appendices A to G) |
| `REM_G3_L4_Design_and_Results_AR.md`, `REM_G3_L4_Integrated_Design_AR.png` | inside the zip | received; explanatory only |
| Full texts of the mathematical sources named in the task (Tong et al. 2018; Geifman and El-Yaniv 2017; Friedman 2001; Angelopoulos et al.) | not attached; the task gives URLs | **not readable in this session**: `pmc.ncbi.nlm.nih.gov` and `arxiv.org` are outside the session's network settings. The authors' public implementations were read from GitHub instead where they exist (`MATHEMATICAL_SOURCE_REGISTRY.csv`) |

## 2. How the package was applied

Repository `RMS756/Ram`, branch `claude/rem-improvement-study` at `ed1ea397fa736fb40e9da91869d85dedd8465fb4`, which is the package's base. A new **local** branch `claude/rem-competitive-study-20261116` was created from it and the commit series (`commits.mbox`) was applied with `git am`. The resulting tree is identical to the final-state patch (`git apply --check -R` of the patch succeeds). Only one of the two was applied. The commit hashes differ from those in `LOCAL_COMMIT_LOG.txt` because the committer differs; order, authorship dates and content are preserved:

| Package commit | Local commit | Subject |
|---|---|---|
| `0ff1cea` | `c21e584` | Freeze exploratory REM G3 integration and L4 comparison protocol |
| `cafc41c` | `06ee45f` | Declare Progent as principal comparator before candidate scoring |
| `394fccc` | `666e2bd` | Declare permission-first L4 routing candidate before scoring |
| `5ff440c` | `9578089` | Implement isolated G3 gate and permission-first L4 routing before replay |
| `370cc55` | `5d1d8bb` | Freeze post-scoring follow-up for direct-value binding failures |
| `06b0964` | `501ceb8` | Implement and freeze explicit-value constraint before HV replay |
| `7384417` | `54532ea` | Record complete integration results, disclosed value-guard follow-up and design |
| `4a66796` | `35cca4d` | Prepare private review delivery after external publication was blocked |

Nothing was pushed. The package adds files only (three new directories and two test files); no earlier file is modified.

## 3. Reproduction from pinned sources

Sources: AgentDojo 0.1.35 (banking v1); recorded runs of `ethz-spylab/agentdojo` at `089ed468cf3ed0322acc66b0211f26d9d90dbf60`; Progent manual policy read as data from `sunblaze-ucb/progent` at `9befb41cbf992b49dbf035cbd3d53eb953d3b351` (file digests checked by the loader). Python 3.11.17, numpy 2.4.6. The caches were rebuilt in a new directory with the package's own commands (`prepare`, `fit`, `replay`, `report`, then the follow-up `replay`, `report`).

| Check | Result |
|---|---|
| Eligibility and population hashes (`prepare`) | 3,313 eligible primary episodes with the manifest's hash; 2,148 second-population episodes loaded with the manifest's hash; 2,113 eligible |
| Fits (`fit`) | 152 cells. Original S1 coefficients of REM v1.0 reproduced within 3.6e-14 (the package reports about 3.7e-14). Every coefficient of the package's `fits.json` reproduced within 3.2e-14 |
| First-stage replay | 112,357 replays, 0 errors. `episode_outcomes.jsonl.gz`: all 112,357 rows identical to the package's file |
| Value-guard follow-up | 11,419 replays, 0 errors. `value_guard_episode_outcomes.jsonl.gz`: all 11,419 rows identical |
| `results.json`, `value_guard_results.json` | identical to the package's files after removing timing fields |
| Aggregates of the six reference arms | equal to the stored revision-3 results (the package's own assertion passes) |
| The table of the task description (11 arms, 6 columns) | every number confirmed against the regenerated `results.json` and `value_guard_results.json` |
| HV minus PG, all-task completion | +2.48 [-2.52, +8.69] (S1 and S2); +3.83 [-7.92, +17.23] (second population): confirmed |
| Fixtures | 43 pairs; HV: 36 legitimate released, 0 unsafe released, 36 pairs correct: confirmed |

The regenerated files were compared and then discarded; the package's files in `REM_G3_INTEGRATION/` are unchanged in the working tree.

## 4. Test suite

With the study environment set: **378 passed, 1 skipped, 1 expected failure** before this study's tests were added. The package reports 376 passed, 3 skipped, 1 expected failure; the difference is two tests of `tests/test_authz_study.py` that skip when the cache `AUTHZ_STATE` is absent and ran here.

- Skipped: `tests/test_melon_rem_integration.py` (needs AgentDojo 0.1.29 in the MELON environment). Kept.
- Expected failure: `tests/test_authorization_audit.py::test_comma_grouped_decimal_matches_its_value` (the provenance tokenizer of the frozen core reads "1,312.40" as 1312; audit finding F-IMPL-1). **Not fixed and not relabelled**: a correction changes feature values of the reference arm and needs a supervisor decision.

## 5. Source-of-truth order used

1. The task description of 16 November 2026 (authorization and constraints). 2. `CLAUDE.md` (design lock; five layers; no invented equations or design values). 3. Stage 2 decision report and the frozen specification (REM v1.0). 4. Result files and source code of the earlier studies and of the package (authoritative over summaries). 5. The Progent paper as uploaded. 6. Authors' repositories read as data. Summaries in the task description were checked against files before use.
