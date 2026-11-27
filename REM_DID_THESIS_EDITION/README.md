# REM thesis, tenth edition (DiD edition, 27 November 2026)

**This edition is the defence-ready (ninth) edition, unchanged, plus five dated and clearly marked exploratory additions:**
- §2.11.6 (DiD and authorization prior art);
- §3.15 (REM-DiD, proposed and not adopted; the former §3.15 Chapter Summary becomes §3.16);
- §4.6.12 (exploratory DiD evaluation; the former §4.6.12 Chapter Summary becomes §4.6.13);
- a "not confirmed" paragraph in §5.5;
- Future Work item 14 in §5.7;
- 8 references;
- the edition note in the front matter.

`REM_DEFENCE_READY_THESIS/` is not modified.

**Build:**
```bash
python3 REM_DID_THESIS_EDITION/tools/make_did_edition.py
python3 REM_DID_THESIS_EDITION/tools/build_r9.py
python3 REM_DID_THESIS_EDITION/tools/check_did_numbers.py
```

**Output:** `REM_Master_Thesis_DiD_Edition.docx` / `.pdf` (278 pages).

**Checks:**
- 114 references, all cited;
- all inserted DiD numbers verified against `REM_DEFENSE_IN_DEPTH/results/`;
- TOC: 77 entries, 0 unmatched.

**Status:** the REM-DiD sections are exploratory. No REM-DiD element is adopted without a supervisor decision (file `REM_DEFENSE_IN_DEPTH/57_LIMITATIONS_AND_MISSING_RESOURCES.md` §4).
