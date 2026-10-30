# Experiment Reproduction Guide

These steps were executed in full on 30 October 2026 and reproduced every analytical value of `results/pilot_R2/` (see `RESULTS_PROVENANCE_REPORT.md` §3). Commands are given exactly as run.

## 1. Environment

| Requirement | Version used | Notes |
|---|---|---|
| OS | Linux x86_64 (container, 4 vCPU, 15 GB RAM) | Other platforms not tested |
| Python | 3.11.17 | Package requires ≥ 3.10 (`pyproject.toml`) |
| Python packages | numpy 2.4.6, PyYAML 6.0.1, pytest 9.1.1, agentdojo 0.1.35, matplotlib, pillow 13.0.0 | `pip install -e .[dev] agentdojo==0.1.35 matplotlib` |
| Benchmark traces | AgentDojo repository, commit `089ed468cf3ed0322acc66b0211f26d9d90dbf60`, directory `runs/` (≈ 525 MB) | Public GitHub repository `ethz-spylab/agentdojo` |
| Network | PyPI and github.com only | No LLM API key, no credentials. All tool calls run in AgentDojo's simulated banking environment |
| For the thesis build only | pandoc ≥ 3.5 (`pypandoc_binary`), python-docx, LibreOffice Writer **and** `libreoffice-math`, poppler-utils, sympy, openpyxl | Without `libreoffice-math`, LibreOffice renders Word equations as blank space |

## 2. Steps

```bash
# from the repository root, branch claude/rem-algorithm-implementation-3ktvze
python3 -m pip install -e ".[dev]" agentdojo==0.1.35 matplotlib

git clone https://github.com/ethz-spylab/agentdojo.git /home/user/ethz-spylab/agentdojo
git -C /home/user/ethz-spylab/agentdojo checkout 089ed468cf3ed0322acc66b0211f26d9d90dbf60

# 1. tests (expected: 193 passed; per-file counts in verification/pytest_per_file_2026-10-30.txt)
python3 -m pytest -o addopts="" -q

# 2. pilot, written OUTSIDE the repository so that committed results are not overwritten (about 12 minutes on 4 vCPU on 30 October)
PILOT_RESULTS_DIR=/path/to/rerun PYTHON=python3 \
AGENTDOJO_RUNS=/home/user/ethz-spylab/agentdojo/runs bash experiments/pilot/run_all.sh

# 3. compare with the committed result set (expected: 0 analytical differences)
python3 REM_FINAL_THESIS/verification/compare_reproduction.py /path/to/rerun results/pilot_R2 /path/to/comparison.json

# 4. check the numbers printed in the chapters against the result files
python3 REM_FINAL_THESIS/verification/check_chapter_numbers.py REM_FINAL_THESIS/chapters/CHAPTER5_RESULTS_FINAL.md results/pilot_R2

# 5. mathematical checks of the derived equations (expected: 22 PASS)
python3 REM_FINAL_THESIS/verification/verify_equations.py

# 6. Chapter 2 PRISMA counts (run on a copy; the script rewrites its outputs)
cp -r chapter2 /tmp/ch2 && (cd /tmp/ch2/slr/tools && python3 build_slr.py) && \
  diff <(python3 -m json.tool chapter2/slr/prisma_counts.json) <(python3 -m json.tool /tmp/ch2/slr/prisma_counts.json)

# 7. regenerate the final chapters from R2 and rebuild the thesis
python3 REM_FINAL_THESIS/tools/make_r3.py
python3 REM_FINAL_THESIS/tools/build_references_verified.py
python3 REM_FINAL_THESIS/tools/build_thesis.py
```

## 3. Determinism and what varies

- All randomness is seeded (20261027). Analytical values are identical across three runs: R1 at `aa66f22`, R2 at `84a8c21`, and R3 on 30 October from `4a286a5`.
- Wall-clock time varies between runs and machines (Chapter 4 §4.14). Memory varied between R1 and R2 and was identical between R2 and R3.
- Each JSON records the REM commit, the configuration and amendment hashes, the AgentDojo versions, and the Python and NumPy versions.

## 4. What cannot be reproduced here

- **Live enforcing-mode runs.** These need an LLM API and an authorization decision (D-15); they were never executed.
- **The human label audit.** The package is prepared in `results/pilot_R2/label_audit_human_package.csv`, but annotators are needed.
- **The first R1 execution before commit `aa66f22`.** Its log was not preserved (Chapter 5 §5.2.3).
