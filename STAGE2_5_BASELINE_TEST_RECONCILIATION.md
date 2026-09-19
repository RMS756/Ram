# STAGE 2.5 — BASELINE TEST RECONCILIATION

**Date:** 2026-09-19 · **Baseline:** `78cb0e3` · **Runner:** pytest 9.1.1, Python 3.11.15
**Read-only audit.** No test added, deleted, renamed or modified; no pytest
configuration changed; no source altered.

---

## 1. The stated inconsistency

Previous project reporting stated:

```text
 43 frozen-math tests
139 contract-compliance tests
154 tests total

 43 + 139 = 182 ≠ 154        excess = 28
```

§20 requires that the **current repository** be treated as authoritative, that
the counts be verified directly, and that the historical numbers **not** be made
to fit.

---

## 2. Configuration established first

| Fact | Finding |
| ---- | ------- |
| Test files | 8 `test_*.py` under `tests/` |
| `conftest.py` | **None in the repository** |
| `pytest.ini` / `tox.ini` / `setup.cfg` | **None** |
| Config source | `pyproject.toml` → `[tool.pytest.ini_options]` |
| `testpaths` | `["tests"]` |
| `addopts` | `-q --strict-markers` |
| Registered custom markers | **None** |
| Marker usage | One `@pytest.mark.parametrize` in `test_pipeline.py` |
| CI configuration | **None** |

**Consequence.** With `--strict-markers` active and no markers registered,
**no marker-based selection exists**. No reported figure can have come from
`-m <marker>`. Category membership is determined **by file**.

**Method note.** `addopts` already contains `-q`, so `--collect-only -q`
compounds to double-quiet and prints a per-file summary instead of node IDs. All
counts below use `-o addopts=""`, a **command-line override that modifies no
configuration file**.

---

## 3. Verified counts — current baseline

### A. Total unique tests

```console
$ python3 -m pytest -o addopts="" --collect-only -q
154 tests collected in 0.21s

$ python3 -m pytest -o addopts="" --collect-only -q | grep "::" | sort -u | wc -l
154
```

**154 collected; 154 unique node IDs after deduplication.** The two agree, so no
node is collected twice.

### Per-file distribution

| File | Tests |
| ---- | ----: |
| `tests/test_frozen_math.py` | 43 |
| `tests/test_metrics.py` | 25 |
| `tests/test_pipeline.py` | 21 |
| `tests/test_contract_compliance.py` | 20 |
| `tests/test_config.py` | 15 |
| `tests/test_trajectory.py` | 12 |
| `tests/test_reproducibility.py` | 9 |
| `tests/test_mitigation.py` | 9 |
| **Total** | **154** |

`43 + 25 + 21 + 20 + 15 + 12 + 9 + 9 = 154` ✓

### B. Frozen-math

```console
$ python3 -m pytest -o addopts="" tests/test_frozen_math.py
43 passed in 0.14s
```

**43 — matches the historical figure exactly.**

### C. Contract-compliance

```console
$ python3 -m pytest -o addopts="" tests/test_contract_compliance.py
20 passed in 0.11s
```

**20 — does NOT match the historical figure of 139.**

### D. Overlap

**Zero.** Two independent checks:

1. Node IDs are file-qualified (`tests/<file>.py::<test>`), so a test in one file
   cannot be a member of another. The per-file counts sum to exactly the
   deduplicated total, which is only possible if the partitions are disjoint.
2. Stripping file prefixes from all 154 node IDs and searching for repeats
   returns **no duplicates** — not even a same-named test in two files.

`43 + 20 = 63`; the other six files hold the remaining **91**. Frozen-math,
contract-compliance and "everything else" form a genuine partition of 154.

### E–F. Collection vs execution

```console
$ python3 -m pytest -o addopts="" -rA
154 passed in 0.49s
```

Outcome tally parsed from the `-rA` summary: **154 PASSED**; no `FAILED`,
`SKIPPED`, `XFAIL`, `XPASS` or `ERROR` lines.

| Category | Collected | Executed | Passed | Failed | Skipped | XFail | Command |
| -------- | --------: | -------: | -----: | -----: | ------: | ----: | ------- |
| Frozen-math | 43 | 43 | 43 | 0 | 0 | 0 | `pytest -o addopts="" tests/test_frozen_math.py` |
| Contract-compliance | 20 | 20 | 20 | 0 | 0 | 0 | `pytest -o addopts="" tests/test_contract_compliance.py` |
| **Full suite** | **154** | **154** | **154** | **0** | **0** | **0** | `pytest -o addopts="" -rA` |
| *(reference)* Suite − `test_config.py` | 139 | 139 | 139 | 0 | 0 | 0 | `pytest -o addopts="" --ignore=tests/test_config.py` |

Collected equals executed in every row — nothing is deselected or skipped.

---

## 4. How 154 relates to 43 and 139

### The 139 figure is reproducible, but not as a category

```console
$ python3 -m pytest -o addopts="" --ignore=tests/test_config.py
139 passed in 0.32s
```

**139 is exactly the full suite minus `tests/test_config.py` (15 tests).**
`154 − 15 = 139`.

### The decomposition is unique

An exhaustive search over all 255 non-empty subsets of the eight test files found
**exactly one** summing to 139: the seven files excluding `test_config.py`. This
follows necessarily from `154 − 139 = 15` and `test_config.py` being the only
file with 15 tests — no combination of the others sums to 15.

### Why 43 + 139 ≠ 154

**139 is a superset of 43, not a sibling category.** The 139-test set is the
whole suite minus one file, and it *contains* all 43 frozen-math tests. Adding
the two therefore double-counts:

```text
  43 + 139                                              = 182
  minus the true total                                  = 154
  excess                                                =  28

  frozen-math counted twice (alone, and inside the 139)  = +43
  test_config.py absent from the 139-test selection      = −15
  net                                                    =  28   ✓ exact, no residual
```

### What the historical error was

The figure **139** was labelled *"contract-compliance tests"*. It is not. It is a
**full-suite pass count** from a working state in which `tests/test_config.py`
did not yet exist. The contract-compliance suite has always contained **20**.

### Provenance

| Question | Finding |
| -------- | ------- |
| Does 139 match any committed state? | **No.** Every commit contains all eight test files and yields 154 |
| Different pytest version? | **No.** The same runner (9.1.1) reproduces 139 under the file exclusion |
| Marker-based selection? | **Impossible.** No markers registered; `--strict-markers` active |
| Most consistent account | 139 was the whole-suite count in an **uncommitted intermediate working state**, recorded before `test_config.py` (15 tests) was written, then mislabelled as a contract-compliance figure |

That account is supported by the exact and unique arithmetic reconstruction. It
is offered as the most consistent explanation of the evidence, not as an observed
event — no commit, log or CI record of that intermediate state exists.

### Counts at every commit

Each commit was extracted with `git archive` into a scratch directory
(read-only with respect to the repository) and the suite run there:

| Commit | Collected | Passed |
| ------ | --------: | -----: |
| `1c18cdf` | 154 | 154 |
| `afc1137` | 154 | 154 |
| `f45ac2e` | 154 | 154 |
| `f46c126` | 154 | 154 |
| `78cb0e3` (HEAD) | 154 | 154 |

---

## 5. Correction to the previous report

| Figure | Previously reported | **Verified from the current baseline** |
| ------ | ------------------- | -------------------------------------- |
| Full suite | 154 | **154** ✓ confirmed |
| Frozen-math | 43 | **43** ✓ confirmed |
| Contract-compliance | 139 | **20** ✗ **corrected** |
| — | — | *(139 = full suite − `test_config.py`; a full-suite count, not a category)* |

**Correct composition:** **43 frozen-math + 20 contract-compliance + 91 other =
154.**

---

## 6. Integrity confirmation

- [x] No test added, deleted, renamed or modified — 8 files before and after
- [x] No pytest configuration changed — `-o addopts=""` is a command-line override only
- [x] No source altered
- [x] Historical states inspected via `git archive` into a scratch directory, never by checkout
- [x] Counts were **not** adjusted to fit the historical report
- [x] `git status --porcelain` shows only the new Stage 2.5 documents

---

## 7. Verdict

### BASELINE CONFIRMED — 154 / 154

The current repository confirms **154 collected, 154 executed, 154 passed, 0
failed, 0 skipped, 0 xfailed**, composed of **43 frozen-math + 20
contract-compliance + 91 other**.

The historical trio reconciles exactly: **43** and **154** are confirmed; **139**
is reproducible and uniquely decomposable, but is a **full-suite** count, never a
contract-compliance count. `43 + 139` exceeds the total by exactly 28 because the
139-test set **contains** the 43 frozen-math tests (`+43`) while omitting
`test_config.py` (`−15`).

**The previous label "139 contract-compliance tests" is corrected to 20.** No
test-suite defect was found.
