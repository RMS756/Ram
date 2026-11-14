"""Report stage of the follow-up (revision 2). Reads the stored replays of the first study (unchanged) and of the
repaired arms; writes REM_IMPROVEMENT_STUDY/followup/results_v2.json and prints tables. Development evidence."""
from __future__ import annotations

import collections
import json
import os
import sys
from types import SimpleNamespace

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import improve as I  # noqa: E402
import improve_v2 as I2  # noqa: E402
import report as R  # noqa: E402
from improve import S, G, common, build, load_raw, load  # noqa: E402

REF = ["B0", "M00", "M00_nobeh", "A2", "PG", "G1", "L2"]
CONTRASTS = [("G2", "G1"), ("G2", "A2"), ("G2", "PG"), ("L2g", "L2"), ("L3", "G2"), ("L3c", "G2"), ("L3c", "L3"),
             ("G1r", "G1"), ("G2", "G2-nobind"), ("G2", "G2-nocond"), ("G2", "G2-nofulfil"), ("G2", "M00_nobeh"), ("G2", "M00"), ("L2g", "G1")]
OUT = os.path.join(I.REPO, "REM_IMPROVEMENT_STUDY", "followup")


def fixtures_v2(st, cells):
    sys.path.insert(0, os.path.join(I.REPO, "REM_AUTHORIZATION_AUDIT", "tools"))
    import trace_fixtures as tf
    cell = cells[("S1", "injection_task_0")]
    arms = I2.ARMS_V2
    sets = {}
    for name, path in (("set1", "REM_AUTHORIZATION_AUDIT/fixtures/set1_substitution_fixtures.json"), ("set2", "REM_AUTHORIZATION_AUDIT/fixtures/set2_fresh_fixtures.json"),
                       ("set3", "REM_FINAL_SUBMISSION/fixtures/set3_credential_and_reformatting_fixtures.json"), ("set4", "REM_IMPROVEMENT_STUDY/fixtures/set4_permission_fixtures.json")):
        d = json.load(open(os.path.join(I.REPO, path)))
        recs = d["records"] if isinstance(d, dict) else d
        for fx in recs:
            if "authorized" in fx:
                fx["legitimate_call"] = {"tool": "send_money", "args": dict(fx["authorized"])}
                fx["unsafe_call"] = {"tool": "send_money", "args": dict(fx["substituted"])}
            if "history" not in fx:
                fx["history"] = [{"tool": "read_file", "args": {"file_path": "document.txt"}, "output": fx["tool_output"], "executed": True}]
        sets[name] = recs
    rows = []
    for sname, recs in sets.items():
        for fx in recs:
            for arm in arms:
                row = {"set": sname, "fixture": fx["id"], "arm": arm}
                for role in ("legitimate", "unsafe"):
                    ep = SimpleNamespace(objective=fx["objective"], system_prompt=tf.SYSTEM_PROMPT, injection_task_id=None, episode_id="fixture")
                    g = I2.make_guard_v2(arm, cell, ep, st)
                    for h in fx["history"]:
                        g.begin_decision_point()
                        g.evaluate(h["tool"], dict(h["args"]))
                        g.ingest(h["tool"], h["output"], executed=bool(g.audit[-1]["released"]) and bool(h.get("executed", True)))
                    g.begin_decision_point()
                    call = fx[f"{role}_call"]
                    g.evaluate(call["tool"], dict(call["args"]))
                    row[f"{role}_released"] = bool(g.audit[-1]["released"])
                    row[f"{role}_perm"] = g.audit[-1]["details"].get("perm")
                rows.append(row)
    summ = {}
    for sname in sets:
        summ[sname] = {}
        for arm in arms:
            rr = [r for r in rows if r["set"] == sname and r["arm"] == arm]
            summ[sname][arm] = {"n": len(rr), "legitimate_released": sum(r["legitimate_released"] for r in rr), "unsafe_released": sum(r["unsafe_released"] for r in rr),
                                "pairs_correct": sum(r["legitimate_released"] and not r["unsafe_released"] for r in rr),
                                "unsafe_released_ids": [r["fixture"] for r in rr if r["unsafe_released"]],
                                "legitimate_withheld_ids": [r["fixture"] for r in rr if not r["legitimate_released"]]}
    return {"summary": summ, "rows": rows}


def main():
    st = common.make_setup()
    I.PG.load()
    D1, D2 = load("replay"), load("replay_v2")
    data = build("primary", load_raw())
    meta, valid = D1["meta"], D1["valid"]
    by = collections.defaultdict(lambda: collections.defaultdict(dict))
    for scheme, role, eid, arm, u, s, err, aud in D1["res"]:
        if arm in REF:
            by[(scheme, role)][eid][arm] = (u, s, err, aud)
    for scheme, role, eid, arm, u, s, err, aud in D2["res"]:
        by[(scheme, role)][eid][arm] = (u, s, err, aud)
    restricted = set(st.restricted)
    att = [e for e in valid if data.episodes[e].attacked]
    ben = [e for e in valid if not data.episodes[e].attacked]
    usr = lambda e: data.episodes[e].user_task_id
    inj = lambda e: data.episodes[e].injection_task_id
    P = by[("S1", "primary")]
    P2 = collections.defaultdict(dict)
    for e in valid:
        P2[e].update({a: v for a, v in P[e].items() if a in ("B0", "A2", "PG", "G1", "G1r", "G2", "G2-nobind", "G2-nocond", "G2-nofulfil")})
        P2[e].update(by[("S2", "primary")][e])
    F = by[("S1", "dev2")]
    rec = D1["recorded_fresh"]
    fv = sorted(e for e in F if F[e]["B0"][2] is None and (F[e]["B0"][0], F[e]["B0"][1]) == rec[e])
    fatt = [e for e in fv if meta[e]["attacked"]]
    fben = [e for e in fv if not meta[e]["attacked"]]
    pops = {"primary_S1": (P, att, ben, usr, inj), "primary_S2": (P2, att, ben, usr, inj),
            "dev2": (F, fatt, fben, lambda e: meta[e]["user_task"], lambda e: meta[e]["injection_task"])}
    out = {"status": "DEVELOPMENT EVIDENCE — follow-up (revision 2); protocol REM_IMPROVEMENT_STUDY/followup/PROTOCOL_V2.md frozen at ae3f923 before scoring",
           "evaluation_mode": "offline recorded-trace replay, step level, no reviewer, NO-ADAPT", "populations": {}}
    arms_all = REF + I2.ARMS_V2
    for name, (B, a_, b_, u_, i_) in pops.items():
        arms = R.block(B, a_, b_, arms_all, restricted)
        res = {"n_attacked": len(a_), "n_benign": len(b_), "arms": arms, "contrasts": {}}
        for x, y in CONTRASTS:
            if x in arms and y in arms:
                res["contrasts"][f"{x} minus {y}"] = R.paired(B, a_, b_, u_, i_, x, y)
        users = sorted({u_(e) for e in a_ + b_}, key=lambda s: int(s.split("_")[-1]))
        res["tasks_completed_by_user_task"] = {a: {u: [int(sum(B[e][a][0] for e in a_ + b_ if u_(e) == u)), int(sum(1 for e in a_ + b_ if u_(e) == u))] for u in users}
                                               for a in arms}
        res["attacks_by_user_task"] = {a: dict(collections.Counter(u_(e) for e in a_ if B[e][a][1])) for a in arms}
        res["held_out_credential_change"] = {a: int(sum(B[e][a][1] for e in a_ if i_(e) == "injection_task_7")) for a in arms}
        res["without_user_task_15"] = {a: {"attacks": int(sum(B[e][a][1] for e in a_ if u_(e) != "user_task_15")),
                                           "all_tasks": int(sum(B[e][a][0] for e in a_ + b_ if u_(e) != "user_task_15"))} for a in arms}
        res["legit_calls_benign_by_v2_status"] = {a: dict(collections.Counter(str((x[7][0] if x[7] else "n/a", bool(x[2]))) for e in b_ for x in B[e][a][3] if x[4] in restricted))
                                                  for a in ("G2", "L3", "L3c") if a in arms}
        out["populations"][name] = res
    Pr = by[("S1", "probe_iban")]
    pe = sorted(Pr)
    out["probe_reformatted_identifier"] = {"episodes": len(pe), "arms": {a: {"attacks_reformatted": int(sum(Pr[e][a][1] for e in pe)),
                                                                            "attacks_original_text": int(sum(P[e][a][1] for e in pe))}
                                                                        for a in I2.ARMS_V2 + ["G1", "L2", "A2", "PG"] if all(a in Pr[e] for e in pe)}}
    G.update(setup=st)
    out["fixtures"] = fixtures_v2(st, I2.merged_cells())
    json.dump(out, open(os.path.join(OUT, "results_v2.json"), "w"), indent=1, default=common._default)
    r = lambda v: "[" + ", ".join(f"{100 * x:.2f}" for x in v) + "]"
    for name, res in out["populations"].items():
        print(f"\n== {name}: attacked {res['n_attacked']}, benign {res['n_benign']}")
        for a, m in res["arms"].items():
            print(f"{a:12s} atk {m['attacks_successful']:4d}  rel-atk-eps {m['episodes_with_released_attack_labelled_call']:4d}  ben {m['benign_completed']:3d}  all {m['all_tasks_completed']:4d}  "
                  f"legit {m['legit_calls_released_benign']:3d}/{m['legit_calls_n']}  cred {res['held_out_credential_change'][a]}  no-ut15 atk {res['without_user_task_15'][a]['attacks']} all {res['without_user_task_15'][a]['all_tasks']}  err {m['replay_errors']}")
        for k, c in res["contrasts"].items():
            print(f"  {k:22s} tasks {r(c['task_completion_all'])} ASR {r(c['attack_success'])} benign {r(c.get('task_completion_benign', [0, 0, 0]))} g/l {c['tasks_gained_lost']} atk g/l {c['attacks_gained_lost']}")
    print("\nprobe:", json.dumps(out["probe_reformatted_identifier"]["arms"]))
    for sname, s in out["fixtures"]["summary"].items():
        print("\nfixtures", sname)
        for a, m in s.items():
            print(f"  {a:12s} legit {m['legitimate_released']}/{m['n']} unsafe {m['unsafe_released']} correct {m['pairs_correct']}  unsafe: {m['unsafe_released_ids']}  withheld: {m['legitimate_withheld_ids']}")


if __name__ == "__main__":
    main()
