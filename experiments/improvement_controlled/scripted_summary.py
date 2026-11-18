"""Summary of results/scripted_closed_loop.json (counts and percentages per arm and mode)."""
import json
from pathlib import Path

D = Path(__file__).resolve().parents[2] / "REM_IMPROVEMENT_CONTROLLED_STUDY_2026_11_18" / "results"
rows = json.load(open(D / "scripted_closed_loop.json"))["rows"]
out = {}
for a in sorted({r["arm"] for r in rows}):
    ben = [r for r in rows if r["arm"] == a and r["mode"] == "benign"]
    s = {"benign_completed": sum(r["utility"] for r in ben), "benign_n": len(ben),
         "benign_all_reference_calls_released": sum(r["all_released"] for r in ben),
         "benign_failed": sorted(r["user_task"] for r in ben if not r["utility"])}
    for m in ("user_first", "injection_first", "injection_after_first_read"):
        rr = [r for r in rows if r["arm"] == a and r["mode"] == m]
        s[m] = {"n": len(rr), "injection_goal_reached": sum(r["security"] for r in rr), "user_task_done": sum(r["utility"] for r in rr),
                "breaches": sorted(f"{r['user_task']}x{r['injection_task']}" for r in rr if r["security"]) if a != "B0" else "all but listed in json"}
    out[a] = s
(D / "scripted_summary.json").write_text(json.dumps(out, indent=1))
for a, s in out.items():
    print(a, s["benign_completed"], "/", s["benign_n"], {m: (s[m]["injection_goal_reached"], s[m]["user_task_done"]) for m in ("user_first", "injection_first", "injection_after_first_read")})
