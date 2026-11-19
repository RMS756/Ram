"""Per-group tables of the held-out probe suites from the stored rows (no re-run). Output: results/probe_group_tables.json"""
import collections
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / "REM_B_HARDENING_VALIDATION_2026_11_19" / "results"
res = {}
for name, f in (("probes_v2", "suite3_heldout_probes2.json"), ("probes_v3", "suite3_heldout_probes3.json"),
                ("probes_v2_frozen_round", "suite_heldout_probes2.json")):
    rows = json.loads((OUT / f).read_text())["rows"]
    t = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for r in rows:
        t[r["arm"]][r["group"]][(r["ref"], r["released"])] += 1
    res[name] = {a: {g: {"authorized": f"{c[('authorized', True)]}/{c[('authorized', True)] + c[('authorized', False)]}",
                         "unauthorized_released": f"{c[('unauthorized', True)]}/{c[('unauthorized', True)] + c[('unauthorized', False)]}",
                         "ambiguous_released": f"{c[('ambiguous', True)]}/{c[('ambiguous', True)] + c[('ambiguous', False)]}"}
                     for g, c in sorted(gs.items())} for a, gs in t.items()}
(OUT / "probe_group_tables.json").write_text(json.dumps(res, indent=1))
for a in ("REM_B", "REM_B2", "REM_B3", "PG", "C1"):
    for n in ("probes_v2", "probes_v3"):
        print(n, a, {g: (v["authorized"], v["unauthorized_released"], v["ambiguous_released"]) for g, v in res[n].get(a, {}).items()})
