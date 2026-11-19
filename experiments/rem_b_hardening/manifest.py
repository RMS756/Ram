"""Reproducibility manifest of the REM-B hardening study. Wraps experiments/improvement_controlled/manifest.py (packages,
AgentDojo installation, banking task hashes, state-variable NAMES only) and adds: commits of this study, checks of the
protocol hash files 06 and 06a, and SHA-256 of every result, log and figure file. No secret value is read or written.
usage: python3 manifest.py <out.json>"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "improvement_controlled"))
import manifest as M  # noqa: E402

STUDY = ROOT / "REM_B_HARDENING_VALIDATION_2026_11_19"
M.CODE = ["experiments/rem_b_hardening", "experiments/architecture_redesign", "experiments/improvement_controlled",
          "experiments/progent_competitive", "experiments/repair_study", "experiments/improve_study", "experiments/competitive_study",
          "experiments/g3_integration", "experiments/pilot", "experiments/authz_study", "rem", "tests/test_rem_b_hardening.py"]


def check(fname):
    bad, n = [], 0
    for line in (STUDY / fname).read_text().splitlines():
        if line.strip():
            h, f = line.split(None, 1)
            n += 1
            p = ROOT / f.strip().lstrip("*")
            if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest() != h:
                bad.append(f.strip())
    return {"files": n, "mismatches": bad}


def main(out):
    M.main(out)
    d = json.loads(Path(out).read_text())
    d["generated_by"] = "experiments/rem_b_hardening/manifest.py (wraps improvement_controlled/manifest.py)"
    git = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True).stdout.strip()  # noqa: E731
    d["git"]["frozen_commits_verified"] = {c: git("cat-file", "-t", c) == "commit" for c in ("31c146e", "8a9e6a2", "f6d885b", "f74d6e3", "37f0157")}
    d["protocol_hashes_06"] = check("06_PROTOCOL_HASHES.sha256")
    d["protocol_hashes_06a"] = check("06a_PROTOCOL_HASHES.sha256")
    d["study_files_sha256"] = {str(p.relative_to(ROOT)): M.sha(p) for sub in ("results", "logs", "figures")
                               for p in sorted((STUDY / sub).rglob("*")) if p.is_file()}
    Path(out).write_text(json.dumps(d, indent=1), encoding="utf-8")
    print("06", d["protocol_hashes_06"], "06a", d["protocol_hashes_06a"], "study files", len(d["study_files_sha256"]))


if __name__ == "__main__":
    main(sys.argv[1])
