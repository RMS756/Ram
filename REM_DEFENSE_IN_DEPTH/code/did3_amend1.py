"""Amendment DiD-3a: re-run X0 on POP-P/POP-R/POP-X with rule verdicts recorded; corrected coverage.
usage: python3 REM_DEFENSE_IN_DEPTH/code/did3_amend1.py"""
import collections, gzip, itertools, json, multiprocessing as mp, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import did3_common as D  # noqa: E402
from did3_run import ARMS  # noqa: E402

FAMS = ("PROV", "DET", "BEH", "LEARN")


def _job(job):
    pop, eid = job
    r = D.run_episode(ARMS["X0"], D.G["eps"][pop][eid])
    return {"pop": pop, "eid": eid, "arm": "X0", **r}


def coverage(recs):
    sets = []
    for r in recs:
        for c in r["calls"]:
            if c[0] == 1 and c[2]:
                sets.append(frozenset(code.split("_")[0] for code, v in c[6] if v != "allow" and code.split("_")[0] in FAMS))
    out = {"attack_sc_calls": len(sets), "covered_by_any": sum(bool(s) for s in sets), "uncovered": sum(not s for s in sets),
           "covered_by_two_or_more": sum(len(s) >= 2 for s in sets),
           "by_control": {f: sum(f in s for s in sets) for f in FAMS},
           "covered_by_exactly_one": {f: sum(s == {f} for s in sets) for f in FAMS}, "jaccard": {},
           "pattern_counts": {"+".join(sorted(k)) or "(none)": v for k, v in collections.Counter(sets).most_common()}}
    for a, b in itertools.combinations(FAMS, 2):
        i, u = sum(a in s and b in s for s in sets), sum(a in s or b in s for s in sets)
        out["jaccard"][f"{a}~{b}"] = round(i / u, 4) if u else None
    return out


def main():
    D.setup()
    jobs = [(p, e) for p in ("POP-P", "POP-R", "POP-X") for e in sorted(D.G["eps"][p])]
    with mp.get_context("fork").Pool(4) as pool:
        res = pool.map(_job, jobs, chunksize=64)
    with gzip.open(os.path.join(D.REPO, "REM_DEFENSE_IN_DEPTH", "results", "did3_raw_amend1.jsonl.gz"), "wt") as fh:
        for r in res:
            fh.write(json.dumps(r, separators=(",", ":")) + "\n")
    main_res = json.load(open(os.path.join(D.REPO, "REM_DEFENSE_IN_DEPTH", "results", "did3_results.json")))
    out = {"amendment": "50a_AMENDMENT_DID3_COVERAGE.md", "gate_X0_success_counts": {}, "coverage": {}}
    for p in ("POP-P", "POP-R", "POP-X"):
        R = [r for r in res if r["pop"] == p]
        out["gate_X0_success_counts"][p] = [sum(r["security"] for r in R if "|none|" not in r["eid"]),
                                            main_res["arms"][p]["X0"]["successful_attacks"]]
        out["coverage"][p] = coverage(R)
    json.dump(out, open(os.path.join(D.REPO, "REM_DEFENSE_IN_DEPTH", "results", "did3_coverage_amend1.json"), "w"), indent=1)
    print(json.dumps(out["gate_X0_success_counts"]), json.dumps(out["coverage"]["POP-P"], indent=0)[:900])


if __name__ == "__main__":
    main()
