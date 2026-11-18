"""Phase 2 audit: benchmark collisions and order dependence (exploratory audit; not a scored experiment).

(a) user_only: the user task's ground truth alone, in the INJECTED environment, no defence (B0). If AgentDojo's security
    evaluator reports the injection goal as reached, the user's own legitimate work collides with the attacker's goal.
(b) order: the obedient agent with 'user_first', 'injection_first' and 'injection_after_first_read' orders for B0, GV_math2, C1, PG.
usage: python3 collision_audit.py <out.json>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scripted as SC  # noqa: E402
import arms as AR  # noqa: E402


def main(out):
    f = AR.factory()
    rows = SC.run(["B0"], f, modes=("user_only",), include_benign=False)
    collisions = [(r["user_task"], r["injection_task"]) for r in rows if r["security"]]
    order = SC.run(["B0", "PG", "GV_math2", "C1"], f, modes=("user_first", "injection_first", "injection_after_first_read"), include_benign=False)
    summ = {}
    for arm in ("B0", "PG", "GV_math2", "C1"):
        for mode in ("user_first", "injection_first", "injection_after_first_read"):
            rr = [r for r in order if r["arm"] == arm and r["mode"] == mode]
            summ[f"{arm}|{mode}"] = {"n": len(rr), "injection_goal_reached": sum(r["security"] for r in rr),
                                     "user_task_done": sum(r["utility"] for r in rr),
                                     "breaches": sorted(f"{r['user_task']}x{r['injection_task']}" for r in rr if r["security"])}
    out_d = {"status": "EXPLORATORY AUDIT (scripted ground-truth agents; no LLM)", "user_only_collisions": collisions,
             "n_user_only": len(rows), "order_summary": summ, "order_rows": order}
    Path(out).write_text(json.dumps(out_d, indent=1, default=str), encoding="utf-8")
    print("collisions (user ground truth alone reaches the injection goal):", collisions)
    for k, v in summ.items():
        print(k, v["n"], v["injection_goal_reached"], v["user_task_done"], v["breaches"])


if __name__ == "__main__":
    main(sys.argv[1])
