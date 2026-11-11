# Reproduction guide

[PROPOSED — SUPERVISOR APPROVAL REQUIRED]

Use Python ≥3.10; this run used Python 3.12 and NumPy 2.3.5. Exact resolved packages: `artifacts/environment-freeze.txt`. Timing and bootstrap floating-point details can vary by platform. The editable package entry records this session's checkout path.

```bash
git clone https://github.com/RMS756/Ram.git Ram
cd Ram
git checkout codex/rem-authorization-generalization-experiment
python -m venv --system-site-packages ../venv
../venv/bin/python -m pip install -e '.[dev]' agentdojo==0.1.35 matplotlib
# Pin resolved versions from the recorded environment where needed.
git clone https://github.com/ethz-spylab/agentdojo.git ../agentdojo
git -C ../agentdojo checkout 089ed468cf3ed0322acc66b0211f26d9d90dbf60
mkdir -p ../reproduction
PILOT_RESULTS_DIR="$PWD/../reproduction" AGENTDOJO_RUNS="$PWD/../agentdojo/runs"  PYTHON="$PWD/../venv/bin/python" OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1  bash experiments/pilot/run_all.sh > ../reproduction/run.log 2>&1
PILOT_RESULTS_DIR="$PWD/../aa_eval/fit" AGENTDOJO_RUNS="$PWD/../agentdojo/runs"  OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1  ../venv/bin/python -u -m experiments.authorization_generalization.evaluate  --raw ../reproduction/steps.pkl --out ../aa_eval > ../aa_eval.log 2>&1
AGENTDOJO_RUNS="$PWD/../agentdojo/runs" REM_STUDY_RAW="$PWD/../reproduction/steps.pkl" ../venv/bin/python -m pytest  -o addopts='' -q -p no:cacheprovider tests experiments/authorization_generalization/tests
../venv/bin/python REM_FINAL_THESIS/verification/compare_reproduction.py  ../reproduction results/pilot_R4 ../comparison.json
```

These commands were executed in this session with `/workspace/work/venv/bin/python`, `/workspace/work/reproduction`, `/workspace/work/aa_eval` and `/workspace/work/agentdojo/runs`. Seeds: historical 20261027, new bootstrap 20261111. OOF fit assignment is deterministic as in the original code. This study is offline/stateful replay without a live model or bank connection.

`steps.pkl` is generated from pinned upstream JSON traces; only load the artifact you generated locally. Do not load untrusted uploaded pickles. Model fitting state is regenerated and is not required in the Git repository.

Outputs include dataset/split/version audits, original fold fitting state, r_mod replay diagnostics, episode outcomes, decision audits, native metrics, offline attempt-label proxies, authorization coverage, model metrics, strata, sensitivity, overhead and source/runtime manifests. The study directory contains the 11 requested reports and raw JSON/log evidence. Original `results/pilot_R4/` remains untouched.

Do not run repository audit scripts that overwrite committed audit logs if preservation is required. Use the isolated commands above instead. No API key is needed. Published-controller efficacy comparisons require additional real branch data/model access and are not produced by these commands.

Rebuild the plotted Pareto points from recorded outcomes:

```bash
MPLCONFIGDIR=../mpl ../venv/bin/python -m experiments.authorization_generalization.figures \
 --results REM_ALGORITHM_IMPROVEMENT_STUDY/artifacts/replay_metrics.json \
 --out REM_ALGORITHM_IMPROVEMENT_STUDY/artifacts/security_utility.png
```
