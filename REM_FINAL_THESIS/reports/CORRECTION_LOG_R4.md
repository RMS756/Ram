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
| — | `check_chapter_numbers.py` accepts a number found anywhere in the results | New `verification/trace_cells_R4.py` → `trace_cells_R4.txt` | Each of 116 entries names table, row, column and one JSON field (file, configuration, semantics, reviewer, metric); interval cells check point and both bounds. 116 PASS. Planted swap of the episode-level B1 ASR into the step-level cell → detected (1 FAIL); the old checker would accept it. Coverage: Tables 5.3, 5.5, 5.7, 5.8, 5.11, 5.12 and the abstract's numbers. Other tables (5.2, 5.4, 5.6, 5.9, 5.10, Ch. 6 text) remain checked by the older occurrence check only | **PARTIALLY ADDRESSED** (principal tables traced; not every number in the thesis) |
| — | Architecture figure drew Detection → Behavioral Analysis in sequence; Ch. 3 said "in parallel" | `experiments/pilot/figures.py` (figure redrawn: Layers 2 and 3 as independent branches from Layer 1 into Layer 4, labelled "independent computations; run in sequence"; no EXPLORATORY stamp on the design diagram); Ch. 3 §3.2.2 text; Figure 3.1 now from `results/pilot_R4/figures/` | Code check: `EpisodeTracker.features` computes the Layer-2 and Layer-3 features one after the other; no behavioral feature reads x_ctx2 (they share the declared pattern set). Five layers; no layer added | **FIXED AND VERIFIED** |
| — | Narrow table headers split inside words; tables continuing with a single row (PDF pp. 183, 191 of R3) | `tools/build_thesis.py` (R4 mode: column widths from cell content; 10-pt table text; rows not split; tables of ≤ 25 rows kept with their caption) | Rendered and inspected (§4) | See §4 |
| — | Title page combines title and abstract; name placeholder | Abstract moved to its own page (R4 build). Name placeholder retained | Official name, title and template not supplied | **PARTIALLY ADDRESSED** (layout); **OPEN** (official content) |
| — | RemPipeline vs evaluation path; x_ctx1 absent | Unchanged disclosures (Ch. 4 §4.3, §4.5, Table 4.7) | Re-read in R4 | **FIXED AND VERIFIED** (already disclosed; retained) |
| — | Platt 1999/2000 | Platt entry and every in-text "Platt (1999)" in Ch. 1–3 | The entry cites the MIT Press chapter (editors, pp. 61–74); Crossref (1 Nov) registers that chapter as 2000, DOI 10.7551/mitpress/1113.003.0008, title "Probabilities for SV Machines". Year corrected, DOI added, title discrepancy disclosed in the entry. The chapter was never read, so Eq. 3.3's source code stays NC | **PARTIALLY ADDRESSED** (year resolved by record; printed title and content not checked) |
| — | Close prior work and equation sources in full | `SOURCE_VERIFICATION_LOG_R4.md`; Ch. 2 §2.8.4, §2.9.3; Ch. 6 Table 6.3 | arXiv, Crossref API, OpenAlex API and publisher hosts refused in this session (curl and WebFetch). Only raw.githubusercontent.com reachable: the NEXUS README supports the cascade, the λ-loss threshold selection and the ECE figures (level R); its headline figures differ from the abstract (recorded, not resolved). No full text read | **PARTIALLY ADDRESSED** |
| — | Live enforcement | `experiments/live/LIVE_EVALUATION_PROTOCOL.md`, `live_config_TEMPLATE.yaml`, `check_live_config.py` (fail-closed: 16 inputs REQUIRED_FROM_DESIGN → exit 2) | No live run; no credentials used; nothing spent | **OPEN** (NOT EXECUTED) |
| — | Label validity | Ch. 5 §5.10 package description corrected | `verification/label_audit_package_check_R4.json`: 145 items; random stratum = 30 drawn episodes, 25 with proposed calls, 70 items (matches the generator); **0 human annotations** | **OPEN** |
| — | Design decisions (costs, tiers, features, predicates, replay scope, semantics) | Register updated (D-2 effect corrected); no decision invented | No supervisor decision on record | **OPEN** |
| — | Comparators: O3 partly achieved; no superiority claims | Unchanged (Ch. 6 Table 6.2, §6.4) | Re-read | **FIXED AND VERIFIED** (already stated) |
| — | Official front-matter material | Unchanged placeholders | Not supplied | **OPEN** |

## 2. Executions in R4

See §2 of `CORRECTION_LOG_R4_RUNS.md` (generated after the clean re-execution).

## 3. Items newly recorded in R4

| Item | Note |
|---|---|
| Timing values vary by run and host | R1/R2 partial medians 0.14–0.20 ms; the R4 hosts gave higher partial values. Timing is reported per run with its conditions, never pooled across hosts |
| NEXUS figures differ between abstract and README | Recorded in Ch. 2 §2.9.3; needs a version-specific full-text check |
| Platt chapter title | Registered title differs from the cited title; printed title not checked |

## 4. Rendering

See `CORRECTION_LOG_R4_RUNS.md` §4.
