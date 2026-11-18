"""Parity of REM's replay checker (progent_manual.allowed) with upstream Progent's check_tool_call on every restricted call
proposed by the recorded agents (arguments from results/fp_audit_replay.json). Runs upstream code: requires
REM_ALLOW_UPSTREAM_EXECUTION=1 and PROGENT_UPSTREAM at the pinned commit; run in an isolated environment.
usage: python3 parity_recorded_calls.py <fp_audit_replay.json> <out.json>
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for p in ("experiments/progent_competitive", "experiments/improve_study"):
    sys.path.insert(0, str(ROOT / p))
import progent_manual as PGM  # noqa: E402
import progent_upstream as PU  # noqa: E402


def main(inp, out):
    if os.environ.get("REM_ALLOW_UPSTREAM_EXECUTION") != "1":
        raise SystemExit("set REM_ALLOW_UPSTREAM_EXECUTION=1")
    st = PGM.load()
    sec = PU.load_secagent(os.environ["PROGENT_UPSTREAM"], "P0_manual")
    PU.install_manual_policy(sec, st["policies"])
    rows = json.load(open(inp))["rows"]
    n, bad = 0, []
    for r in rows:
        kw = dict(PGM.DEFAULTS.get(r["tool"], {}))
        kw.update(r["args"] or {})
        a, b = PGM.allowed(r["tool"], r["args"] or {}), PU.upstream_allowed(sec, r["tool"], kw)
        n += 1
        if a != b:
            bad.append({"tool": r["tool"], "args": r["args"], "rem_replay_checker": a, "upstream": b})
    Path(out).write_text(json.dumps({"pinned_upstream": PU.PINNED, "calls": n, "disagreements": len(bad), "examples": bad[:50]}, indent=1))
    print("calls", n, "disagreements", len(bad))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
