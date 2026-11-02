# CODE_AUDIT_R4: code verification and thesis-workflow audit (2 November 2026)

**Audited:** branch `claude/rem-r4-corrections-3ktvze`, head `bec4d1c` (code identical to the R4 thesis commit `9ab3f9e`).

**Not independent:** this audit was produced by the same AI assistant whose sessions wrote the code and the thesis.

**No research file was modified.** All outputs are in this directory.

| File | Content |
|---|---|
| `CODE_VERIFICATION_REPORT.md` | Findings ranked by severity (CV-1 to CV-19), with evidence, reproduction steps, impact and proposed fixes; verified-correct items; what remains unverified |
| `CODE_TO_THESIS_TRACEABILITY.md` | Component → file:line → chapter/equation → test/output → status |
| `THESIS_WRITING_PROCESS_AR.md` | Arabic account of the documented research and writing workflow; illustrative example; supervisor summary |
| `REPRODUCE_AND_RUN.md` | Commands actually executed, environment, inputs and hashes, expected artefacts, blockers |
| `audit_checks/` | `audit_invariants.py`, `audit_results.py`, `e2e_example.py`, `list_all_differences.py`: read-only checks added by this audit |
| `logs/` | Every execution log, the reproduction comparisons, the citation checks and the Git history |

## Correction to the earlier evaluation (`SUPERVISOR_EVALUATION_R4/`)

`SUPERVISOR_EVALUATION_R4/EXPERIMENTAL_RESULTS_AUDIT.md` §4 lists "Circular r_mod; Modify ≡ Block in step-level replay" as **"Not stated as such"**. This is partly wrong: Chapter 3 (R4) line 549 states that "Under step-level semantics, Modify and Block have the same effect on the current call". What remains unstated is that r_mod measures label coverage, and that Ch. 3 §3.8 property 3 and line 381 attribute r_mod to "enforcing-mode runs" (CV-3). The earlier file is left unchanged as a historical record, and this note supersedes that row.
