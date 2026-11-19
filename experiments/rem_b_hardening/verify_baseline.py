"""Phase 1: independent re-computation of the architecture-redesign study (commit 31c146e) from raw outputs.

Does NOT import the study's metric code. Sources:
  * results/episode_outcomes.jsonl.gz       (per-episode utility/security of every arm; written by the frozen runner)
  * AgentDojo recorded run files            (recorded utility/security -> eligibility of dev2 and H recomputed here)
  * results/suite_*.json rows               (author-written suites; labels from the case files)
  * results/scripted_closed_loop.json rows  (scripted closed loop)
  * $COMPETITIVE_STATE/arch_replays.pkl     (call-level records; the per-call audit flag was produced by the frozen runner)
Output: REM_B_HARDENING_VALIDATION_2026_11_19/results/baseline_verification.json
"""
import collections
import gzip
import json
import os
import pickle
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OLD = ROOT / "REM_ARCHITECTURE_REDESIGN_STUDY_2026_11_18" / "results"
OUT = ROOT / "REM_B_HARDENING_VALIDATION_2026_11_19" / "results" / "baseline_verification.json"
RUNS = Path(os.environ.get("AGENDOJO_RUNS_OVERRIDE", "/home/user/ethz-spylab/agentdojo/runs"))
ARMS = ["B0", "GV_math2", "C1", "C1I", "PG", "REM_A", "REM_B", "REM_C", "REM_C_T", "REM_C_raw", "REM_B_R"]
DESIGN_TASKS = {"user_task_11", "user_task_15"}


def parse(pop, eid):
    p = eid.split("|")
    if pop in ("dev2", "heldout"):
        p = p[1:]
    if len(p) == 5 or (pop == "primary" and len(p) == 4 and p[2] == "none"):
        pass
    pipe, ut = p[0], p[1]
    inj, atk = (p[2], p[3]) if len(p) >= 4 else (p[2], "none")
    attacked = inj != "none"
    return pipe, ut, (inj if attacked else None), atk, attacked


def recorded(pipe, ut, inj, atk):
    f = RUNS / pipe / "banking" / ut / (atk if inj else "none") / ((inj or "none") + ".json")
    d = json.loads(f.read_text())
    return d.get("utility"), d.get("security"), d.get("error") or ("missing utility" if "utility" not in d else None)


def main():
    by = collections.defaultdict(dict)
    for line in gzip.open(OLD / "episode_outcomes.jsonl.gz", "rt"):
        r = json.loads(line)
        if r["scheme"] != "S1" or r["population"] not in ("primary", "dev2", "heldout"):
            continue
        by[(r["population"], r["episode_id"])][r["arm"]] = (r["utility"], r["security"], r["error"])
    out = {"source_commit": "31c146e", "populations": {}}
    task_of = {}
    for pop in ("primary", "dev2", "heldout"):
        eps = [k[1] for k in by if k[0] == pop]
        elig = []
        for e in eps:
            pipe, ut, inj, atk, att = parse(pop, e)
            task_of[(pop, e)] = (ut, inj, att)
            b0 = by[(pop, e)]["B0"]
            if pop == "primary":
                elig.append(e)
                continue
            ru, rs, rerr = recorded(pipe, ut, inj, atk)
            if rerr is None and b0[2] is None and (bool(b0[0]), bool(b0[1])) == (bool(ru), bool(rs)):
                elig.append(e)
        att = [e for e in elig if task_of[(pop, e)][2]]
        ben = [e for e in elig if not task_of[(pop, e)][2]]
        m = {}
        for a in ARMS:
            m[a] = {"attacks": sum(1 for e in att if by[(pop, e)][a][1]),
                    "benign_completed": sum(1 for e in ben if by[(pop, e)][a][0]),
                    "all_completed": sum(1 for e in elig if by[(pop, e)][a][0]),
                    "errors": sum(1 for e in elig if by[(pop, e)][a][2])}
        gains = collections.Counter()
        for e in elig:
            ut = task_of[(pop, e)][0]
            b, c = by[(pop, e)]["REM_B"][0], by[(pop, e)]["C1"][0]
            if b and not c:
                gains[("gained", "design" if ut in DESIGN_TASKS else "other")] += 1
            if c and not b:
                gains[("lost", "design" if ut in DESIGN_TASKS else "other")] += 1
        out["populations"][pop] = {"loaded": len(eps), "eligible": len(elig), "attacked": len(att), "benign": len(ben),
                                   "arms": m, "REM_B_vs_C1_task_changes": {f"{k[0]}_{k[1]}_tasks": v for k, v in gains.items()}}
    # call-level records (audit flag from the frozen runner)
    st = Path(os.environ["COMPETITIVE_STATE"]) / "arch_replays.pkl"
    res = pickle.load(st.open("rb"))
    elig_ids = {(p, e) for p, d in out["populations"].items() for e in ([k[1] for k in by if k[0] == p])}
    viol = collections.Counter()
    att_rel = collections.Counter()
    for scheme, role, e, arm, u, s, err, aud in res:
        if scheme != "S1" or arm not in ARMS:
            continue
        for b in aud:
            if b[2] and b[12] is True:
                viol[(role, arm)] += 1
            if b[2] and b[0] == 1:
                att_rel[(role, arm)] += 1
    out["call_level_note"] = "counts over ALL loaded episodes of dev2/heldout (eligibility applied only to episode metrics)"
    out["audited_violations_released_all_loaded"] = {f"{r}|{a}": v for (r, a), v in sorted(viol.items())}
    out["attack_labelled_calls_released_all_loaded"] = {f"{r}|{a}": v for (r, a), v in sorted(att_rel.items())}
    # suites
    suites = {}
    for name in ("ledger_dev", "heldout_probes", "diagnostics", "generalization"):
        rows = json.load(open(OLD / f"suite_{name}.json"))["rows"]
        c = collections.defaultdict(collections.Counter)
        for r in rows:
            c[r["arm"]][(r["ref"], bool(r["released"]))] += 1
        suites[name] = {a: {"authorized_released": v[("authorized", True)], "authorized_n": v[("authorized", True)] + v[("authorized", False)],
                            "unauthorized_released": v[("unauthorized", True)], "ambiguous_released": v[("ambiguous", True)]}
                        for a, v in c.items() if a in ARMS}
    out["suites"] = suites
    sc = json.load(open(OLD / "scripted_closed_loop.json"))["rows"]
    g = collections.Counter()
    for r in sc:
        if r["arm"] in ARMS and r["user_task"] == "user_task_15" and r["injection_task"] == "injection_task_4" and r["security"]:
            g[(r["arm"], r["mode"])] += 1
    out["scripted_ut15_it4_goal_reached"] = {f"{a}|{m}": v for (a, m), v in sorted(g.items())}
    OUT.write_text(json.dumps(out, indent=1))
    for p, d in out["populations"].items():
        print(p, d["loaded"], d["eligible"], d["attacked"], d["benign"], {a: tuple(d["arms"][a].values()) for a in ("B0", "C1", "REM_B", "REM_C", "PG")},
              d["REM_B_vs_C1_task_changes"])
    print({k: v for k, v in out["audited_violations_released_all_loaded"].items() if k.split("|")[1] in ("C1", "REM_B", "REM_C", "PG")})
    print("attack-labelled released", out["attack_labelled_calls_released_all_loaded"])
    print("probes", {a: tuple(v.values()) for a, v in suites["heldout_probes"].items()})
    print("scripted", out["scripted_ut15_it4_goal_reached"])


if __name__ == "__main__":
    main()
