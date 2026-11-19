"""DEVELOPMENT smoke check before freezing (primary S1 only; H, H2 and the new probes are not loaded): crashes, parity of
frozen REM-B under replay_episode2 with the stored outcomes, and whether R2/R3 act. Output: results/dev_smoke.json"""
import collections
import gzip
import json
import multiprocessing as mp
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hard_run as HR  # noqa: E402

d, aux, eps, folds = HR.A._populations()
eps = {"primary": eps["primary"]}
HR._setup_workers(eps, folds)
arms = ["REM_B", "REM_B2"]
jobs = [("S1", "primary", e, a) for a in arms for e in sorted(eps["primary"])]
with mp.get_context("fork").Pool(4) as p:
    res = list(p.imap_unordered(HR.replay_job, jobs, chunksize=32))
old = {}
for line in gzip.open(HR.OLD / "episode_outcomes.jsonl.gz", "rt"):
    r = json.loads(line)
    if r["scheme"] == "S1" and r["population"] == "primary" and r["arm"] == "REM_B":
        old[r["episode_id"]] = (r["utility"], r["security"], r["error"])
by = collections.defaultdict(dict)
for s, role, e, a, u, sec, err, aud in res:
    by[e][a] = (u, sec, err, aud)
par = sum(1 for e in by if (by[e]["REM_B"][0], by[e]["REM_B"][1], by[e]["REM_B"][2]) != tuple(old[e]))
out = {"status": "DEVELOPMENT (primary S1)", "errors": sum(1 for r in res if r[6]), "rem_b_parity_mismatches": par,
       "tasks": {a: sum(by[e][a][0] for e in by) for a in arms}, "attacks": {a: sum(by[e][a][1] for e in by if eps["primary"][e].attacked) for a in arms},
       "gained_by_task": dict(collections.Counter(eps["primary"][e].user_task_id for e in by if by[e]["REM_B2"][0] and not by[e]["REM_B"][0])),
       "lost_by_task": dict(collections.Counter(eps["primary"][e].user_task_id for e in by if by[e]["REM_B"][0] and not by[e]["REM_B2"][0])),
       "sources_REM_B2_released_changed": dict(collections.Counter(y[6] for e in by for x, y in zip(by[e]["REM_B"][3], by[e]["REM_B2"][3]) if x[2] != y[2])),
       "violations": {a: sum(1 for e in by for x in by[e][a][3] if x[2] and x[11] is True) for a in arms}}
(HR.OUT / "dev_smoke.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
