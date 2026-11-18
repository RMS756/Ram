"""Reproducibility manifest of the architecture-redesign study (18 November 2026).

Reuses experiments/improvement_controlled/manifest.py unchanged (packages, AgentDojo installations, banking task hashes,
state variable names only) with this study's code list, and adds: the commits of this study, the protocol-hash check, and
SHA-256 of every result, log and figure file of the study folder. No secret value is read or written.
usage: python3 manifest.py <out.json>
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "improvement_controlled"))
import manifest as M  # noqa: E402

STUDY = ROOT / "REM_ARCHITECTURE_REDESIGN_STUDY_2026_11_18"
M.CODE = ["experiments/architecture_redesign", "experiments/improvement_controlled", "experiments/progent_competitive",
          "experiments/repair_study", "experiments/improve_study", "experiments/competitive_study", "experiments/g3_integration",
          "experiments/pilot", "experiments/authz_study", "rem", "tests/test_architecture_redesign.py"]


def protocol_check():
    bad, n = [], 0
    for line in (STUDY / "08_PROTOCOL_HASHES.sha256").read_text().splitlines():
        if not line.strip():
            continue
        h, f = line.split(None, 1)
        f = f.strip().lstrip("*")
        n += 1
        p = ROOT / f
        if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest() != h:
            bad.append(f)
    return {"files": n, "mismatches": bad}


def main(out):
    M.main(out)
    d = json.loads(Path(out).read_text())
    d["generated_by"] = "experiments/architecture_redesign/manifest.py (wraps improvement_controlled/manifest.py)"
    git = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True).stdout.strip()  # noqa: E731
    d["git"]["frozen_commits_verified"] = {c: git("cat-file", "-t", c) == "commit" for c in ("56bf600", "6705c07", "ff2399b")}
    d["protocol_hashes_08"] = protocol_check()
    d["study_files_sha256"] = {str(p.relative_to(ROOT)): M.sha(p) for sub in ("results", "logs", "figures")
                               for p in sorted((STUDY / sub).rglob("*")) if p.is_file()}
    Path(out).write_text(json.dumps(d, indent=1), encoding="utf-8")
    print("protocol", d["protocol_hashes_08"], "study files", len(d["study_files_sha256"]))


if __name__ == "__main__":
    main(sys.argv[1])
