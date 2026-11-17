"""Parity of REM's replay checker (progent_manual.allowed) with upstream Progent's check_tool_call.

Runs in its own process (upstream keeps module-level state). Requires PROGENT_UPSTREAM at the pinned commit
0d7ea07 and REM_ALLOW_UPSTREAM_EXECUTION=1. NOT EXECUTED in the authoring session (running upstream code was refused there).

The manual banking policy is the one REM's PG arm replays (commit 9befb41, read as data); it is installed into the
upstream engine of 0d7ea07 with upstream's own update_security_policy, and both checkers are asked about the same
argument cases: every trusted recipient, synthetic recipients, None, and each banking tool with defaults bound.
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for p in ("experiments/progent_competitive", "experiments/improve_study"):
    sys.path.insert(0, str(ROOT / p))
import progent_manual as PGM  # noqa: E402
import progent_upstream as PU  # noqa: E402

TOOLS = ["send_money", "schedule_transaction", "update_scheduled_transaction", "update_password", "update_user_info",
         "get_balance", "get_iban", "read_file", "get_scheduled_transactions", "get_user_info", "get_most_recent_transactions"]


def cases(trusted):
    recips = list(trusted) + ["ZK52390800003316720548", "QB71046600002985413307", "", None, "US133000000121212121212"]
    for tool in TOOLS:
        base = dict(PGM.DEFAULTS.get(tool, {}))
        if tool in ("send_money", "schedule_transaction", "update_scheduled_transaction"):
            for r in recips:
                yield tool, {**base, "recipient": r, "amount": 10.0, "subject": "s", "date": "2022-01-01"}
        else:
            yield tool, base


def main():
    if os.environ.get("REM_ALLOW_UPSTREAM_EXECUTION") != "1":
        raise SystemExit("set REM_ALLOW_UPSTREAM_EXECUTION=1 to execute upstream code")
    st = PGM.load()
    sec = PU.load_secagent(os.environ["PROGENT_UPSTREAM"], "P0_manual")
    PU.install_manual_policy(sec, st["policies"])
    n, bad = 0, []
    for tool, kw in cases(st["trusted"]):
        n += 1
        a, b = PGM.allowed(tool, kw), PU.upstream_allowed(sec, tool, kw)
        if a != b:
            bad.append((tool, kw, a, b))
    print(f"cases {n}; disagreements {len(bad)}")
    for x in bad[:20]:
        print(x)
    if not bad:
        print("PARITY OK")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
