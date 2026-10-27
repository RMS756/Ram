#!/usr/bin/env bash
# Reproduce the EXPLORATORY pilot end to end (about 10 minutes on 4 cores).
# Requires: agentdojo==0.1.35 installed, AgentDojo repository runs/ at $AGENTDOJO_RUNS
# (default /home/user/ethz-spylab/agentdojo/runs, commit 089ed468cf3ed0322acc66b0211f26d9d90dbf60).
set -euo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-python}"
$PY build_dataset.py
$PY e0_pilot.py
$PY run_main.py crossfit rmod observe replay a2 xt
$PY sensitivity_ut15.py
$PY label_audit.py > /dev/null
$PY memory_profile.py
$PY figures.py
