# REM external-defence audit (22 November 2026)

**Location:** branch `claude/rem-external-defense-audit-20261122`, created from `355355a`.

**What it is:** an audit and the preparation of comparisons between REM v1.0 and DRIFT, Progent, MELON and AgentDojo's native defences. AgentDyn is audited as infrastructure.

**What it is not:**
- No live LLM run.
- No paid call.
- No change to `rem/`, to R8, or to any frozen protocol or earlier result.

## Reports

| File | Content |
|---|---|
| `01_DRIFT_AUDIT.md` | Paper, architecture, code, compatibility with AgentDojo 0.1.35 and banking v1 |
| `02_PROGENT_AUDIT.md` | Official vs third-party repository, mechanism, manual-policy enforcement test |
| `03_AGENTDYN_AUDIT.md` | Benchmark/harness audit, semantic changes, possible reuse |
| `04_MELON_REASSESSMENT.md` | Verification of the 19 Nov work and its requirements |
| `05_COMPATIBILITY_MATRIX.md` | Matrix with evidence labels |
| `06_COMPARISON_RECOMMENDATION.md` | Arms chosen and excluded, direct vs descriptive |
| `07_EXPERIMENTAL_PROTOCOL.md` | DRAFT protocol (not frozen) with the blocked design items |
| `08_INTEGRATION_TESTS.md` | Tests executed, results, failures, blockers |
| `09_THESIS_RESEARCH_CONTRIBUTION.md` | How the comparisons can support the thesis without superiority claims |
| `10_ARABIC_SUMMARY.md` | Arabic report |

## Code and data

- **Integration tests:** `experiments/external_defense_audit/`, run each in its own venv under `/home/user/venvs/`:
  - `suite_fingerprint.py`
  - `itest_drift.py`
  - `itest_progent.py`
  - `itest_agentdyn.py`
- **Checks of the stored results:** `tests/test_external_defense_audit.py`.
- **Results** (`results/`):
  - upstream pins and hashes;
  - environment check;
  - package lists;
  - fingerprints;
  - test outputs;
  - a summary of DRIFT's published banking runs.
- **Upstream code:** it is not vendored. It lives in `/home/user/upstream/`, at the commits recorded in `results/upstream_pins.json`.

## Reproduction

```bash
cd /tmp   # run outside the repository; each script takes an absolute output path
for v in /home/user/venvs/{drift,agentdyn,melon029,progent_fork}; do $v/bin/python <repo>/experiments/external_defense_audit/suite_fingerprint.py <out>; done
python3 <repo>/experiments/external_defense_audit/suite_fingerprint.py <out>                       # PyPI 0.1.35
DRIFT_UPSTREAM=/home/user/upstream/SaFo-Lab_DRIFT /home/user/venvs/drift/bin/python <repo>/experiments/external_defense_audit/itest_drift.py <out>
/home/user/venvs/progent/bin/python <repo>/experiments/external_defense_audit/itest_progent.py <out>
/home/user/venvs/agentdyn/bin/python <repo>/experiments/external_defense_audit/itest_agentdyn.py <out>
python3 -m pytest -q tests/test_external_defense_audit.py
```
