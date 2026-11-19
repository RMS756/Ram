"""Phase 2: exact trace of held-out probe HO4 under frozen REM-B (rem_arch, commit 6705c07). Output: results/ho4_trace.json"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for p in ("experiments/architecture_redesign", "experiments/improvement_controlled", "experiments/progent_competitive",
          "experiments/repair_study", "experiments/competitive_study", "experiments/g3_integration", "experiments/pilot",
          "experiments/improve_study", "tests"):
    sys.path.insert(0, str(ROOT / p))
import heldout_probes as HP  # noqa: E402
import rem_arch as RA  # noqa: E402
import seq_harness as SH  # noqa: E402
import contracts as K  # noqa: E402

case = next(c for c in HP.CASES if c["id"] == "HO4_no_designator_single")
contracts = RA.ER.compile_e1(case["objective"])
mod = [c for c in contracts if "schedule_modify" in c.effects]
ob = RA.ObjectBinding(contracts)
f = RA.factory()
rows = SH.run_all(f, ["REM_B"], [case])
out = {"objective": case["objective"],
       "contracts": [{"cid": c.cid, "clause": c.clause, "effects": sorted(c.effects), "count": c.count} for c in contracts],
       "schedule_modify_clauses": [c.clause for c in mod],
       "designators": sorted(ob.designators), "plural": ob.plural,
       "pre_reads": case["pre"],
       "rows": [{k: r[k] for k in ("step", "tool", "args", "ref", "released", "source", "ledger_after") if k in r} for r in rows]}
for w in sorted(ob.designators):
    out.setdefault("designator_origin", {})[w] = [tok for tok in case["objective"].split() if w in tok.lower()]
Path(ROOT / "REM_B_HARDENING_VALIDATION_2026_11_19/results/ho4_trace.json").write_text(json.dumps(out, indent=1, default=str))
print(json.dumps(out, indent=1, default=str)[:2500])
