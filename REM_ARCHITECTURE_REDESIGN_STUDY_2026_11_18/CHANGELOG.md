# Change log: architecture redesign study

All changes are additive. No frozen module (`rem/`), historical result or earlier study folder was modified.

## 18 November 2026

**Branch.**
- `claude/rem-architecture-redesign-20261118` was created from `ff2399b`.
- The interrupted study `REM_AUTHORIZATION_BINDING_VALIDATION_2026_11_18` was never committed and produced no result. Its empty folder was removed; its harness and development cases were moved into `experiments/architecture_redesign/` (`01`).

**`56bf600`: before implementation.** Audit; literature verification; ledger analysis of the frozen arms; threat model; REM-A/B/C designs; algorithm selection; held-out probes (`heldout_probes.py`); held-out population rule (`heldout_population.py`).

**`6705c07`: before any scored run.**
- `rem_arch.py`: object binding, object ledger, E2h, strict provenance, learned modes; candidate and ablation configurations.
- `seq_harness.py`, `ledger_cases.py`, `run_ledger_analysis.py`, `fit_threshold.py` (development data only), `arch_run.py`, `scripted_arch.py`.
- `tests/test_architecture_redesign.py` (15 tests).
- Frozen protocol `08` and `08_PROTOCOL_HASHES.sha256`.

**This commit: results and documents.**
- Results, logs and figures of the stages replay, scripted, suites, fixtures, cost and report.
- Progent parity on held-out calls: `export_heldout_calls.py`, run with `improvement_controlled/parity_recorded_calls.py`.
- `amendment1_posthoc.py`: POST-HOC designator fix, not used for decisions (`08a`, amendment 1).
- `endpoint_supplement.py`: the pre-specified REM-A − C1 endpoint omitted from the runner's contrast list (`08a`, Note 3).
- `make_figures.py`, `manifest.py`.
- Documents `08a` and `10`–`20`, `README.md`, this change log.

## Known defects (not fixed in the frozen code)

- **Object-binding designators.** Extracted from identifiers such as IBANs (`08a`, amendment 1).
- **Contrast list.** The runner's contrast list omitted REM-A − C1 (`08a`, Note 3).
- **Fixture identifiers.** `results/fixtures.json` stores counts only, so the unsafe fixture cannot be named (`08a`, Note 2).
