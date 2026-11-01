# Correction Log R4: Independent Review of 1 November 2026

**Review:** `REM_R3_Independent_Review_2026-11-01.md`, for reviewed commit `181a38c`.
**R4 branch:** `claude/rem-r4-corrections-3ktvze`, branched from `181a38c`. The R3 files, the R2 and R3 result sets, and every historical document are unchanged.

**Status values:**
- **FIXED AND VERIFIED:** corrected, and the correction checked by a test, a script or a re-execution.
- **PARTIALLY ADDRESSED:** what could be done was done; the rest is stated.
- **OPEN:** needs a person, a decision or access that this work does not have.

Every chapter edit is made by `tools/make_r4.py` from the R3 sources and logged in `CHANGE_LOG_R4.md`, so a rebuild cannot restore the errors.

## 1. Review findings

| # | Finding | Changed files / sections | Evidence and validation | Status |
|---|---|---|---|---|
| F1 | Step-level and episode-level mitigation were said to be identical under replay | Ch. 3 §3.8; Ch. 4 §4.8, Table 4.5; Ch. 5 §5.6, new Table 5.11 (old 5.11–5.12 renumbered 5.12–5.13), Table 5.13 RQ2 row; Ch. 6 Table 6.1 row 5, §6.6; abstract; `UNRESOLVED_ITEMS…` D-2; `METHODOLOGY_CODE_TRACEABILITY.md` SC-1 | Stored replay results (`results/pilot_R2/e4_e5_enforcement_replay.json`, `configs.*`): B1 ASR 0.0551 (step) vs 0.0463 (episode); utility under attack lower for every configuration under episode-level semantics; benign utility identical. Code: `RemGuard._mitigate` adds 𝒯_R to the restriction set on an episode-level Block. New test `tests/test_mitigation_semantics.py` (4 tests): Block `send_money`, then Allow `update_password` → released (step-level), `refuse_restricted` (episode-level). Neither policy changed. All 36 cells of Table 5.11 traced to their named fields | **FIXED AND VERIFIED** |
| F2 | Latency described as including attribution and audit construction; the timer stopped before them | `rem/integration/agentdojo_replay.py` (complete-call timer `rem_latency_full_ms` added; the partial timer `rem_latency_ms` unchanged); `experiments/pilot/run_main.py` (summary fields `latency_full_ms_*`, `latency_steps`); Ch. 4 §4.14 rewritten with Table 4.8 (boundaries); Ch. 5 §5.6 processing time; Table 5.13 RQ3 row | `tests/test_latency_instrumentation.py` (2 tests, fake clock and ordered event log: the partial stop precedes attribution, audit and history; the full stop follows them). New measurement from the clean re-execution (§2). Old values relabelled as partial. No complete-call value was estimated from partial values | **FIXED AND VERIFIED** |
| — | Equation-check count: 21 PASS lines, not 22 | `EQUATION_VERIFICATION_REPORT.md`, `EXPERIMENT_REPRODUCTION_GUIDE.md`, R4 readiness report | `verification/verify_equations_output_R4.txt`: 21 `PASS` lines + `ALL PASS` | **FIXED AND VERIFIED** |
| — | Ch. 5 §5.1 said only time and memory differed in the R3 reproduction | Ch. 5 §5.1 | `verification/reproduction_all_differences.json`: 100 latency, 13 commit, 1 file path; no memory value | **FIXED AND VERIFIED** |
| — | `check_chapter_numbers.py` accepts a number found anywhere in the results | New `verification/trace_cells_R4.py` → `trace_cells_R4.txt` | Each of 116 cell and sentence entries (126 checks in total after the independent check) names table, row, column and one JSON field (file, configuration, semantics, reviewer, metric); interval cells check point and both bounds. 116 PASS. Planted swap of the episode-level B1 ASR into the step-level cell → detected (1 FAIL); the old checker would accept it. Coverage: Tables 5.3, 5.5, 5.7, 5.8, 5.11, 5.12 and the abstract's numbers. Other tables (5.2, 5.4, 5.6, 5.9, 5.10, Ch. 6 text) remain checked by the older occurrence check only | **PARTIALLY ADDRESSED** (principal tables traced; not every number in the thesis) |
| — | Architecture figure drew Detection → Behavioral Analysis in sequence; Ch. 3 said "in parallel" | `experiments/pilot/figures.py` (figure redrawn: Layers 2 and 3 as independent branches from Layer 1 into Layer 4, labelled "independent computations; run in sequence"; no EXPLORATORY stamp on the design diagram); Ch. 3 §3.2.2 text; Figure 3.1 now from `results/pilot_R4/figures/` | Code check: `EpisodeTracker.features` computes the Layer-2 and Layer-3 features one after the other; no behavioral feature reads x_ctx2 (they share the declared pattern set). Five layers; no layer added | **FIXED AND VERIFIED** |
| — | Narrow table headers split inside words; tables continuing with a single row (PDF pp. 183, 191 of R3) | `tools/build_thesis.py` (R4 mode: column widths from a character budget per column; 10-pt left-aligned table text; rows not split; tables of ≤ 25 rows kept with their caption) | Rendered and inspected (§4); Table 5.4 on one page; no headers split inside words on the inspected pages | **FIXED AND VERIFIED** (on the inspected pages) |
| — | Title page combines title and abstract; name placeholder | Abstract moved to its own page (R4 build). Name placeholder retained | Official name, title and template not supplied | **PARTIALLY ADDRESSED** (layout); **OPEN** (official content) |
| — | RemPipeline vs evaluation path; x_ctx1 absent | Unchanged disclosures (Ch. 4 §4.3, §4.5, Table 4.7) | Re-read in R4 | **FIXED AND VERIFIED** (already disclosed; retained) |
| — | Platt 1999/2000 | Platt entry and every in-text "Platt (1999)" in Ch. 1–3 | The entry cites the MIT Press chapter (editors, pp. 61–74); Crossref (1 Nov) registers that chapter as 2000, DOI 10.7551/mitpress/1113.003.0008, title "Probabilities for SV Machines". Year corrected, DOI added, title discrepancy disclosed in the entry. The chapter was never read, so Eq. 3.3's source code stays NC | **PARTIALLY ADDRESSED** (year resolved by record; printed title and content not checked) |
| — | Close prior work and equation sources in full | `SOURCE_VERIFICATION_LOG_R4.md`; Ch. 2 §2.8.4, §2.9.3; Ch. 6 Table 6.3 | arXiv, Crossref API, OpenAlex API and publisher hosts refused in this session (curl and WebFetch). Only raw.githubusercontent.com reachable: the NEXUS README supports the cascade, the λ-loss threshold selection and the ECE figures (level R); its headline figures differ from the abstract (recorded, not resolved). No full text read | **PARTIALLY ADDRESSED** |
| — | Live enforcement | `experiments/live/LIVE_EVALUATION_PROTOCOL.md`, `live_config_TEMPLATE.yaml`, `check_live_config.py` (fail-closed: 16 inputs REQUIRED_FROM_DESIGN → exit 2) | No live run; no credentials used; nothing spent | **OPEN** (NOT EXECUTED) |
| — | Label validity | Ch. 5 §5.10 package description corrected | `verification/label_audit_package_check_R4.json`: 145 items; random stratum = 30 drawn episodes, 25 with proposed calls, 70 items (matches the generator); **0 human annotations** | **OPEN** |
| — | Design decisions (costs, tiers, features, predicates, replay scope, semantics) | Register updated (D-2 effect corrected); no decision invented | No supervisor decision on record | **OPEN** |
| — | Comparators: O3 partly achieved; no superiority claims | Unchanged (Ch. 6 Table 6.2, §6.4) | Re-read | **FIXED AND VERIFIED** (already stated) |
| — | Official front-matter material | Unchanged placeholders | Not supplied | **OPEN** |

## 2. Executions in R4 (all on 1 November 2026; Python 3.11.17, NumPy 2.4.6, AgentDojo 0.1.35, Intel Xeon @ 2.80 GHz, 4 vCPU)

| Check | Command | Result | Record |
|---|---|---|---|
| Test suite | `python3 -m pytest -o addopts="" -q` | **205 passed**, 0 failed, 0 skipped (pytest 9.2.0; 199 at `6fc0952`, + 6 Word-transformation tests) | `verification/pytest_R4.txt`, `pytest_per_file_R4.txt` |
| Equation checks | `python3 REM_FINAL_THESIS/verification/verify_equations.py` | 21 PASS lines, then ALL PASS; exit 0 | `verification/verify_equations_output_R4.txt` |
| Full pilot re-execution | `PILOT_RESULTS_DIR=… bash experiments/pilot/run_all.sh` from commit `ea621c3` | Exit 0; 11 min 6 s; outputs in `results/pilot_R4/` (state files not committed). A first run from the uncommitted working tree gave the same analytical values and was discarded for provenance reasons | `verification/pilot_R4_run.log`; `results/pilot_R4/PROVENANCE_R4.md` |
| R4 vs reported R2 results | `compare_reproduction.py` + per-value listing | 6,057 shared values: 5,942 identical; **0 analytical differences**; 115 differing values = 50 `latency_ms_median`, 50 `latency_ms_p95`, 13 `rem_commit`, 1 `file`, 1 `peak_bytes_per_step_median` (4,364 → 4,349 bytes, reported in Ch. 5); 150 new fields (`latency_full_ms_*`, `latency_steps`) | `verification/reproduction_comparison_R4.json`, `reproduction_all_differences_R4.json` |
| Complete-call timing (new) | from the run above | Across the 8 REM configurations, 6,684 steps each: complete call median 0.21–0.28 ms, p95 0.49–0.70 ms; partial timer in the same run median 0.18–0.24 ms, p95 0.46–0.64 ms | `results/pilot_R4/e4_e5_enforcement_replay.json` (`latency_full_ms_*`, `latency_ms_*`) |
| Cell-level traceability | `python3 REM_FINAL_THESIS/verification/trace_cells_R4.py` | **126 PASS, 0 FAIL** (116 table cells and abstract sentences, 4 timing ranges, 6 sentences on the semantics comparison added after the independent check); negative control detected | `verification/trace_cells_R4.txt` |
| PRISMA reconstruction | `build_slr.py` on a copy of `chapter2/` | `prisma_counts.json` identical (320 identified, 101 duplicates, 219 screened, 71 included) | `verification/prisma_reconstruction_R4.txt` |
| Label-audit package | `check_label_audit_package_R4.py` | 145 items; 0 human annotations; random stratum matches its generator | `verification/label_audit_package_check_R4.json` |
| Citations | `check_citations.py` on the R4 chapters | Every citation resolves (same six parser artifacts as R3) | `verification/citation_check_R4.txt` |
| Live-evaluation config | `check_live_config.py live_config_TEMPLATE.yaml` | Exit 2: 16 inputs REQUIRED_FROM_DESIGN | — |

## 3. Items newly recorded in R4

| Item | Note |
|---|---|
| Timing values vary by run and host | R1/R2 partial medians 0.14–0.20 ms; the R4 hosts gave higher partial values. Timing is reported per run with its conditions, never pooled across hosts |
| NEXUS figures differ between abstract and README | Recorded in Ch. 2 §2.9.3; needs a version-specific full-text check |
| Platt chapter title | Registered title differs from the cited title; printed title not checked |

## 4. Rendering (R4 build)

- **Build:** `REM_VERSION=R4 python3 REM_FINAL_THESIS/tools/build_thesis.py` produces `R4/REM_THESIS_R4.docx`, `R4/REM_THESIS_R4.pdf` (212 pages A4) and the six chapter DOCX files.
- **Generated lists:** contents; 4 figures and 53 tables, each with a page number.
- **Schema validation:** all 7 DOCX files pass the Office XML validator (`verification/docx_validation_R4.txt`). Three defects found during validation were fixed in the build: duplicate run properties from the table post-processing (introduced and fixed in R4); the position of `updateFields` in settings.xml and the incompatible `m:nor`/`m:sty` pair in equations (both inherited from R3); and missing page-margin attributes.
- **PDF text:** 0 U+FFFD and 0 "¿" characters; no "cannot differ" and no "Platt (1999)".
- **Pages inspected visually:**
  - 1–3: title page; the abstract now on its own page — pandoc's default abstract style chained the paragraphs and pushed half the abstract to the next page, so it was restyled to body size;
  - 8: list of figures;
  - 113: Figure 3.1, redrawn;
  - 126: Eqs. 3.6–3.8;
  - 149: Table 3.17 — equation numbers no longer split;
  - 167: Table 4.8;
  - 175: Table 5.4 — on one page, headers no longer split inside words;
  - 180: Tables 5.8–5.10;
  - 182: Table 5.11;
  - 184: Table 5.12.
- **Inspection limits:** the inspection was a sample, not a certification of every page. Word recomputes page fields when the file is opened.

## 5. Independent check of checkpoint `b943843` (1 November 2026)

The check reviewed the checkpoint `b943843`. The branch head at the time of these corrections was `6fc0952`, which already contained most of the files reported missing. Each finding was re-verified against the current files before acting.

| # | Finding | What was found at `6fc0952` | Change | Evidence | Status |
|---|---|---|---|---|---|
| 1 | R4 deliverables absent from GitHub | Present at `6fc0952`: `chapters_R4/` (8 files), `R4/REM_THESIS_R4.docx` and `.pdf`, six chapter DOCX files, `results/pilot_R4/` (19 files), `verification/reproduction_all_differences_R4.json`. `CORRECTION_LOG_R4_RUNS.md` was never created: the draft reference to it was replaced by §2 and §4 of this log before `6fc0952`, and no file refers to it | Deliverables rebuilt from the canonical generators. The remote tree was checked after the push, and a fresh clone was verified (§6) | `git ls-tree` of the pushed commit; §6 | **FIXED AND VERIFIED** |
| 2 | Word table transformation duplicated run-property containers (328 runs at `b943843`) | Pushed DOCX files at `6fc0952` had 0 such runs: a regex look-ahead fix had been made before that build. It was still regex-based | Replaced by an XML-aware module, `tools/docx_tables.py` (lxml): an existing `w:rPr` is updated; one is created only when absent; size elements are placed in schema order and never repeated; hyperlinks kept; equation runs untouched; an existing duplicate is repaired, not multiplied; repeated application changes nothing. Two regexes in the list-filling step assumed pandoc's serialization and were made serialization-independent (the first rebuild failed on them, exit 1; caught from the build log and fixed) | `tests/test_docx_tables.py` (6 tests, including idempotence and a repaired duplicate). `verification/check_docx_structure_R4.py` on the 7 rebuilt DOCX files: 0 runs with more than one `w:rPr`; 0 repeated sizes; every table run 10 pt; run and paragraph properties in schema order; 0 `m:nor`+`m:sty` pairs; idempotent (canonical XML) — `verification/docx_structure_R4.txt`. Schema validator: 7/7 pass (`docx_validation_R4.txt`). Build log: `verification/build_R4.log` (exit 0) | **FIXED AND VERIFIED** |
| 3 | Table 5.11 caption said "same verdicts" | Confirmed: REM, no reviewer, y = 0: Modify 239 vs 241, Escalate 1,049 vs 1,047 (`configs.REM_<semantics>_no_reviewer.verdict_rates.0`); idealized: 239/1,050 vs 241/1,048; B1 counts identical | Caption now lists what is fixed (episodes, fitted parameters, costs, predicates, thresholds, reviewer treatment) and what varies (mitigation semantics), and says verdict sequences are not fixed. A new note reports the verdict counts and why later evidence can differ. The generator asserts the counts differ before writing the text | Trace entries `ch5-verdicts-no-reviewer`, `ch5-verdicts-idealized` (PASS) | **FIXED AND VERIFIED** |
| 4 | Existing episode-level paired interval described as unavailable | Confirmed: `paired_differences.REM_episode_level_no_reviewer_minus_B1_episode_level_no_reviewer.ASR` = −0.04263 [−0.12211, −0.00134]; idealized entry equal to three decimals | Ch. 5 now reports REM − B1 ASR within each semantics: −0.051 [−0.130, −0.007] (step-level) and −0.043 [−0.122, −0.001] (episode-level). It states that these are within-semantics contrasts, that no interval for their difference was computed, and repeats the nine-group coverage caveat. Ch. 6 Table 6.1 row 5 updated the same way | Trace entries `ch5-paired-step`, `ch5-paired-episode`, `ch5-paired-episode-ideal`, `ch6-paired-episode` (PASS); a planted swap was detected | **FIXED AND VERIFIED** |
| — | Earlier valid corrections | Both timers, their boundaries, the semantics and timer tests, the step-level reference with D-2 pending, the five layers, audit-only attribution and observe-only CUSUM | Unchanged | Tests pass; Ch. 4 §4.14 unchanged | Retained |

No new pilot run was needed: `results/pilot_R4/` (from commit `ea621c3`) is unchanged, and the code changed after it touches only the thesis build (`REM_FINAL_THESIS/tools/`) and tests.

## 6. Fresh-clone verification (1 November 2026, commit `4e44e24`)

The branch was cloned afresh from GitHub (`git clone --branch claude/rem-r4-corrections-3ktvze`) into an empty directory, and these checks were run there:

| Check | Result |
|---|---|
| Advertised files present | All present: `R4/REM_THESIS_R4.docx`, `.pdf`, the six chapter DOCX files, `chapters_R4/` (8 files), `results/pilot_R4/` (17 files + 3 figures), this log, the readiness report, the verification records |
| Committed DOCX/PDF | Byte-identical to the local build (SHA-256 `6c57d994…bf3e4` DOCX, `b4281ff3…6186c` PDF, at `4e44e24`) |
| `pytest` | 205 passed |
| `make_r3.py` then `make_r4.py` | Regenerated `chapters/`, `chapters_R4/` and the change logs identical to the committed files (`git status` clean) |
| `trace_cells_R4.py` | 126 PASS, 0 FAIL |
| `verify_equations.py` | 21 PASS, ALL PASS |
| `REM_VERSION=R4 build_thesis.py` | Exit 0; 212 pages; extracted PDF text identical to the committed PDF; `check_docx_structure_R4.py` 7/7 PASS on the rebuilt files |

**External input.** The pilot re-execution and the three replay tests also need the public AgentDojo repository `runs/` at commit `089ed468cf3ed0322acc66b0211f26d9d90dbf60` (about 525 MB, not stored in this repository; `EXPERIMENT_REPRODUCTION_GUIDE.md` §2). It was present at `/home/user/ethz-spylab/agentdojo/runs` for these checks. Without it the replay tests skip, and the thesis can still be regenerated and built from the committed results.
