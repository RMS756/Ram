# 00 — BASELINE CHECKSUMS

**Date:** 2026-09-21 · **HEAD:** `0f29ac3` · working tree clean

## Purpose and scope

§3 of the audit instruction requires a baseline snapshot before any chapter is
edited. **No chapter exists to baseline** (see `00_WORKSPACE_INVENTORY.md`).

What follows is therefore a baseline of the **project documents that do exist**,
so that if the audit proceeds later, any change to them is detectable. It is
**not** a chapter baseline and must not be read as one.

## Chapter baseline — NOT AVAILABLE

| Required field | Value |
| -------------- | ----- |
| Chapter 2 file name | **DOES NOT EXIST** |
| Chapter 2 hash | — |
| Chapter 2 word count | — |
| Chapter 2 section structure | — |
| Chapter 2 reference count | — |
| Chapter 2 equation count | — |
| Chapter 2 table/figure count | — |
| Chapter 3 file name | **DOES NOT EXIST** |
| Chapter 3 hash | — |
| Chapter 3 word count | — |
| Chapter 3 section structure | — |
| Chapter 3 reference count | — |
| Chapter 3 equation count | — |
| Chapter 3 table/figure count | — |

## Existing project documents — baselined

SHA-256, first 16 hex characters. Full digests reproducible with
`sha256sum <file>`.

| SHA-256 (16) | Words | Lines | File |
| ------------ | ----: | ----: | ---- |
| `6fef971e0d752eb9` | 1048 | 334 | `CLAUDE.md` |
| `2d9c8fe8516255da` | 929 | 156 | `README.md` |
| `0dee9343522fcb3a` | 2015 | 229 | `RECONCILIATION.md` |
| `d387a68e38b4e738` | 1347 | 244 | `STAGE2_5_BASELINE_TEST_RECONCILIATION.md` |
| `04a475493d476c80` | 4325 | 462 | `STAGE2_5_PRIOR_ART_RECONCILIATION.md` |
| `08920b74beafd3ce` | 1657 | 104 | `STAGE2_5_REM_VS_PRIOR_ART_MATRIX.md` |
| `4aa2f1d67953607f` | 3421 | 376 | `STAGE2_5_RESEARCH_GAP_OPTIONS.md` |
| `abfd3ca51803de49` | 3441 | 590 | `STAGE2_BLOCKED_DECISIONS.md` |
| `b1aefe54d026dc7d` | 2203 | 278 | `STAGE2_EQUATION_TO_SOURCE_TRACEABILITY.md` |
| `f528f0418887f0bf` | 10326 | 1301 | `STAGE2_FINAL_ALGORITHM_MATHEMATICAL_DECISION_REPORT.md` |
| `a3fa3bfc65df295f` | 2204 | 269 | `STAGE3_CHAPTER2_DESIGN.md` |
| `cf5d5715e0a291af` | 3317 | 415 | `STAGE3_CHAPTER3_DESIGN.md` |
| `a060b22acb51531f` | 1510 | 165 | `STAGE3_IMPLEMENTATION_AUDIT.md` |
| `a1e65afb7093ab91` | 3633 | 407 | `STAGE3_PRIOR_ART_AND_POSITIONING.md` |
| `786b0830c558d3d7` | 2170 | 249 | `V1_NEXUS_DIRECT_VERIFICATION.md` |
| `3391f4ebf08d9b38` | 997 | 186 | `docs/ARCHITECTURE.md` |
| `971926cf1433d43f` | 875 | 163 | `docs/EXPERIMENT_GUIDE.md` |
| `b6a17a481fea2489` | 1450 | 57 | `docs/MATHEMATICAL_TRACEABILITY.md` |
| `ea814591401554d5` | 59 | 9 | `docs/guard/README.md` |
| `6c52f52a730b3cc8` | 309 | 91 | `docs/guard/START_PROMPT.md` |

## Implementation baseline

| Item | Value |
| ---- | ----- |
| Python modules | 14 |
| Test files | 8 |
| Tests | **154 collected / 154 passed / 0 failed / 0 skipped** |
| Configuration files | 7 (46 parameters: 27 FROZEN, 19 UNVERIFIED) |
| Registered mathematical operations | 19, all `AWAITING REGISTRY ID` |

## Working directory

`REM_AUDIT_OUTPUT/` was created for derived copies. **No original file was
modified, moved or overwritten by this phase.**
