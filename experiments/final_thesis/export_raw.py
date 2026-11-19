"""Export the raw per-episode and per-call replay outputs of this study (pickles in $PILOT_RESULTS_DIR/state) to compressed CSV.

Output: REM_FINAL_THESIS_COMPLETION_2026_11_19/results/raw/{ablation,external}_{episodes,calls}.csv.gz
Call columns are the audit tuple of the frozen runner: label, verdict, released, tier, tool, rem_latency_ms, tie,
verdict_source, rem_latency_full_ms (raw argument values are never logged).
"""
import csv
import gzip
import os
import pickle
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "pilot"))
import run_main as RM  # noqa: E402

OUT = ROOT / "REM_FINAL_THESIS_COMPLETION_2026_11_19" / "results" / "raw"
OUT.mkdir(parents=True, exist_ok=True)
CALL = ["label", "verdict", "released", "tier", "tool", "rem_latency_ms", "tie", "verdict_source", "rem_latency_full_ms"]


def write(name, rows_ep, rows_call):
    with gzip.open(OUT / f"{name}_episodes.csv.gz", "wt", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["set", "episode_id", "arm", "utility", "security", "error", "n_calls"])
        w.writerows(rows_ep)
    with gzip.open(OUT / f"{name}_calls.csv.gz", "wt", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["set", "episode_id", "arm", "step"] + CALL)
        w.writerows(rows_call)


abl = pickle.load(open(os.path.join(RM.STATE, "final_ablation_replays.pkl"), "rb"))
ep, ca = [], []
for eid, c, u, s, err, aud in abl:
    ep.append(["primary", eid, c, int(bool(u)), int(bool(s)), err or "", len(aud)])
    ca.extend(["primary", eid, c, i] + list(x) for i, x in enumerate(aud))
write("ablation", ep, ca)
ext = pickle.load(open(os.path.join(RM.STATE, "final_external_replays.pkl"), "rb"))
ep, ca = [], []
for k, by in ext.items():
    for eid, arms in by.items():
        for c, (u, s, err, aud) in arms.items():
            ep.append([k, eid, c, int(bool(u)), int(bool(s)), err or "", len(aud)])
            ca.extend([k, eid, c, i] + list(x) for i, x in enumerate(aud))
write("external", ep, ca)
print("exported to", OUT)
