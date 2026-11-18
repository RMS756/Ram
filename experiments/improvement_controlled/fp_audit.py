"""Phase 3: call-level audit of the restricted calls C1 withholds on the offline AgentDojo replay (exploratory audit).

Replays C1 (frozen) on the primary population, scheme S1, with the harness capturing the (synthetic, benchmark) arguments
of every restricted call. For each withheld call it records: episode, user task, attacked or benign episode, the user
request, tool and arguments, attack label of the call (AgentDojo-derived reference labeller; NOT read by the guard), the
verdict source, the front's evidence tuple, the contract status and reason, the consequence tier, and the preceding tool
results that could serve as provenance (tool names only). Output is a JSON list plus an aggregate by
(user task, tool, source, reason).
usage: python3 fp_audit.py <out.json>
"""
import collections
import json
import multiprocessing as mp
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arms as AR  # noqa: E402
import rs_run as V1R  # noqa: E402

W = {}


def job(e):
    ep = W["eps"][e]
    key = ("S1", W["fold"][e])
    g = AR.build_cell("C1", ep, W["cells"][key], W["cs"][key], W["st"])
    seen, tools = [], []
    ev, ing = g.evaluate, g.ingest

    def cap(tool, args):
        seen.append((tool, dict(args), list(tools)))
        return ev(tool, args)

    def ing2(tool, text, executed):
        if executed:
            tools.append(tool)
        return ing(tool, text, executed)
    g.evaluate, g.ingest = cap, ing2
    out = V1R.S.replay_episode(ep, W["st"].suite, g)
    rows = []
    for k, a in enumerate(g.audit):
        if a["tool"] not in W["restricted"]:
            continue
        tool, args, before = seen[k]
        rows.append({"episode": e, "user_task": ep.user_task_id, "injection_task": ep.injection_task_id, "attacked": bool(ep.attacked),
                     "tool": tool, "args": args, "label": a["label"], "released": bool(a["released"]), "source": a["verdict_source"],
                     "tier": a["tier"], "perm": a["details"].get("perm"), "contract": a["details"].get("contract"),
                     "executed_before": before})
    return {"episode": e, "utility": bool(out.utility), "security": bool(out.security), "rows": rows}


def main(out):
    d, aux, eps, folds = V1R.C._populations()
    st = V1R.common.make_setup()
    W.update(eps=eps["primary"], fold=folds["primary"], cells=V1R.J.load("cells"), cs=V1R.C.load("cs_cells"), st=st,
             restricted=set(st.restricted))
    ids = sorted(aux["valid"])
    with mp.get_context("fork").Pool(4) as p:
        res = list(p.imap_unordered(job, ids, chunksize=32))
    prompts = {u: st.suite.get_user_task_by_id(u).PROMPT for u in st.suite.user_tasks}
    rows = [r for x in res for r in x["rows"]]
    withheld = [r for r in rows if not r["released"]]
    agg = collections.Counter((r["user_task"], r["tool"], r["source"], (r["contract"] or [None, None, ""])[2] if r["contract"] else "",
                               "attack_label" if r["label"] == 1 else "no_attack_label", "attacked" if r["attacked"] else "benign")
                              for r in withheld)
    Path(out).write_text(json.dumps({"status": "EXPLORATORY AUDIT: offline replay, C1 frozen, primary S1", "n_episodes": len(res),
                                     "episode_outcomes": {x["episode"]: [x["utility"], x["security"]] for x in res},
                                     "prompts": prompts, "rows": rows,
                                     "aggregate_withheld": [list(k) + [v] for k, v in agg.most_common()]}, indent=1, default=str),
                         encoding="utf-8")
    print("episodes", len(res), "restricted calls", len(rows), "withheld", len(withheld),
          "withheld without attack label", sum(r["label"] != 1 for r in withheld))


if __name__ == "__main__":
    main(sys.argv[1])
