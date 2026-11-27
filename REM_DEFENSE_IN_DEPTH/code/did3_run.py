"""DiD-3 replay runner (protocol 50_PROTOCOL_DID3.md, frozen at commit 8678add). Writes results/did3_raw.jsonl.gz.

usage: python3 REM_DEFENSE_IN_DEPTH/code/did3_run.py
"""
from __future__ import annotations

import gzip
import json
import multiprocessing as mp
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import did3_common as D  # noqa: E402
from remdid.guard import DidConfig  # noqa: E402

fs = frozenset
FULL = fs({"AUTH", "PROV", "DET", "BEH", "LEARN", "ENF"})
EVID = ("PROV", "DET", "BEH", "LEARN")
ARMS = {
    "B0": DidConfig(fs()),
    "B1": DidConfig(fs({"LEARN"})),
    "B2": DidConfig(fs({"AUTH"}), "oracle"),
    "B2e": DidConfig(fs({"AUTH"}), "explicit"),
    "B3": DidConfig(fs({"PROV"})),
    "B4": DidConfig(fs({"DET"})),
    "B5": DidConfig(fs({"BEH"})),
    "B6": DidConfig(fs({"AUTH", "PROV"}), "oracle"),
    "B7": DidConfig(fs({"DET", "BEH"})),
    "B8": DidConfig(fs({"AUTH", "ENF"}), "oracle"),
    "B9": DidConfig(FULL, "oracle"),
    "B9p": DidConfig(FULL, "oracle", precedence="pinned_release"),
    "B9e": DidConfig(FULL, "explicit"),
    "B9n": DidConfig(FULL - {"LEARN"}, "oracle"),
    # idealized reviewer variants
    "B2e+R": DidConfig(fs({"AUTH"}), "explicit", reviewer="idealized"),
    "B3+R": DidConfig(fs({"PROV"}), reviewer="idealized"),
    "B4+R": DidConfig(fs({"DET"}), reviewer="idealized"),
    "B5+R": DidConfig(fs({"BEH"}), reviewer="idealized"),
    "B7+R": DidConfig(fs({"DET", "BEH"}), reviewer="idealized"),
    "B9e+R": DidConfig(FULL, "explicit", reviewer="idealized"),
    # bypass of AUTH (broad TAE) and of further controls
    "X0": DidConfig(FULL, "broad"),
    **{f"X-{c}": DidConfig(FULL, "broad", evade=fs({c})) for c in EVID},
    **{f"X-only-{c}": DidConfig(FULL, "broad", evade=fs(set(EVID) - {c})) for c in EVID},
    "X-all": DidConfig(FULL, "broad", evade=fs(EVID)),
    # failure injection (fail-safe unless stated)
    "F-DET": DidConfig(FULL, "oracle", fail=fs({"DET"})),
    "F-PROV": DidConfig(FULL, "oracle", fail=fs({"PROV"})),
    "F-BEH": DidConfig(FULL, "oracle", fail=fs({"BEH"})),
    "F-LEARN": DidConfig(FULL, "oracle", fail=fs({"LEARN"})),
    "F-AUTH": DidConfig(FULL, "oracle", fail=fs({"AUTH"})),
    "F-STORE": DidConfig(FULL, "oracle", fail=fs({"TAE_STORE"})),
    "F-GW": DidConfig(FULL, "oracle", fail=fs({"GATEWAY"})),
    "F-AUDIT": DidConfig(FULL, "oracle", fail=fs({"AUDIT"})),
    "F-AUTH-open": DidConfig(FULL, "oracle", fail=fs({"AUTH"}), fail_mode="open"),
    "F-DET-b": DidConfig(FULL, "broad", fail=fs({"DET"})),
    "F-DET-b-open": DidConfig(FULL, "broad", fail=fs({"DET"}), fail_mode="open"),
}
OTHER_POPS = {"POP-R": ("B0", "B1", "B3", "B4", "B9", "X0"), "POP-X": ("B0", "B1", "B3", "B4", "B9", "X0")}


def _job(job):
    pop, eid, arm = job
    ep = D.G["eps"][pop][eid]
    r = D.run_episode(ARMS[arm], ep)
    return {"pop": pop, "eid": eid, "arm": arm, **r}


def main():
    D.setup()
    jobs = [("POP-P", e, a) for a in ARMS for e in sorted(D.G["eps"]["POP-P"])]
    for pop, arms in OTHER_POPS.items():
        jobs += [(pop, e, a) for a in arms for e in sorted(D.G["eps"][pop])]
    t0 = time.time()
    out = os.path.join(D.REPO, "REM_DEFENSE_IN_DEPTH", "results", "did3_raw.jsonl.gz")
    n = 0
    with mp.get_context("fork").Pool(4) as pool, gzip.open(out, "wt") as fh:
        for rec in pool.imap_unordered(_job, jobs, chunksize=64):
            fh.write(json.dumps(rec, separators=(",", ":")) + "\n")
            n += 1
            if n % 20000 == 0:
                print(f"{n}/{len(jobs)} {time.time() - t0:.0f}s", flush=True)
    print(f"{n} replays in {time.time() - t0:.0f}s -> {out}")


if __name__ == "__main__":
    main()
