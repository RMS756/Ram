"""07_SECURITY_UTILITY_RESULTS.csv = frozen round (as written by hard_run.py report, kept unchanged in
results/security_utility_frozen.csv) + amendment round (results/security_utility_amendment.csv), with a 'round' column.
Generated only from stored files."""
import csv
import shutil
from pathlib import Path

D = Path(__file__).resolve().parents[2] / "REM_B_HARDENING_VALIDATION_2026_11_19"
frozen = D / "results" / "security_utility_frozen.csv"
if not frozen.exists():
    shutil.copy(D / "07_SECURITY_UTILITY_RESULTS.csv", frozen)
rows = [dict(r, round="frozen_06") for r in csv.DictReader(frozen.open())]
rows += [dict(r, round="amendment_06a_posthoc") for r in csv.DictReader((D / "results" / "security_utility_amendment.csv").open())]
keys = ["round", "population", "arm"] + [k for k in rows[0] if k not in ("round", "population", "arm")]
with (D / "07_SECURITY_UTILITY_RESULTS.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
    w.writeheader()
    w.writerows(rows)
print("rows", len(rows))
