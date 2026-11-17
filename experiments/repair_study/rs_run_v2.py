"""Repair study, version 2: replay and report of the v2 arms (PROTOCOL_AMENDMENT_V2.md, commit 95549b2). No model call.

Stages: replay | report. Baselines (REM10, PG, G3, GV, HV) and the version-1 arms are read from stored replays.
Output: REM_REPAIR_STUDY_2026_11_17/results_v2/
"""
from __future__ import annotations

import collections
import gzip
import json
import multiprocessing as mp
import pickle
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "repair_study"))
import rs_run as V1R              # noqa: E402  (populations, stores, fixtures harness, helpers)
import repaired_arms_v2 as RA2    # noqa: E402

C, J, S, R, common = V1R.C, V1R.J, V1R.S, V1R.R, V1R.common
OUT = ROOT / "REM_REPAIR_STUDY_2026_11_17" / "results_v2"
OUT.mkdir(parents=True, exist_ok=True)
STATE = V1R.STATE
V1ARMS = ["G3_math", "GV_math", "HV_math"]
TABLE_ARMS = V1R.BASELINES + V1ARMS + list(RA2.ARMS)
CONTRASTS = [("GV_math2", "GV_math"), ("HV_math2", "HV_math"), ("G3_math2", "G3_math"), ("GV_math2x", "GV_math2"),
             ("HV_math2x", "HV_math2"), ("HV_math2", "GV_math2"), ("HV_math2x", "GV_math2x"), ("GV_math2", "GV"),
             ("GV_math2", "PG"), ("GV_math2x", "PG")]
W = {}


def replay_job(job):
    scheme, role, e, arm = job
    ep = W["eps"][role][e]
    key = ("S1", W["fold"][role][e]) if scheme == "S1" else ("S2", ep.user_task_id, ep.injection_task_id or W["fold"][role][e])
    out = S.replay_episode(ep, W["setup"].suite, RA2.make_guard(arm, W["jcells"][key], W["cs"][key], ep, W["setup"]))
    audit = [(a["label"], a["verdict"], bool(a["released"]), a["tier"], a["tool"], a["rem_latency_full_ms"], a["verdict_source"],
              a["details"].get("perm") or a["details"].get("permission"), (a["details"].get("cs") or {}).get("stage"),
              a["details"].get("amount"), a["details"].get("stage_before_veto"), a["details"].get("amount_evaluated"))
             for a in out.audit]
    return scheme, role, e, arm, bool(out.utility), bool(out.security), out.error, audit


def stage_replay():
    d, aux, eps, folds = C._populations()
    W.update(setup=common.make_setup(), jcells=J.load("cells"), cs=C.load("cs_cells"), eps=eps, fold=folds)
    jobs = [("S1", role, e, a) for role, pop in eps.items() for a in RA2.ARMS for e in sorted(pop)]
    jobs += [("S2", "primary", e, a) for a in RA2.FITTED for e in aux["valid"]]
    t = time.time()
    res = []
    with mp.get_context("fork").Pool(4) as p:
        for v in p.imap_unordered(replay_job, jobs, chunksize=32):
            res.append(v)
    with (STATE / "rs_replays_v2.pkl").open("wb") as f:
        pickle.dump(res, f)
    print("replay done", len(res), round(time.time() - t), "s; errors", sum(1 for r in res if r[6]), flush=True)


def fixtures(cells, cs):
    import trace_fixtures as tf
    from types import SimpleNamespace
    st = common.make_setup()
    key = ("S1", "injection_task_0")
    result = {}
    for path in ["REM_AUTHORIZATION_AUDIT/fixtures/set1_substitution_fixtures.json", "REM_AUTHORIZATION_AUDIT/fixtures/set2_fresh_fixtures.json",
                 "REM_FINAL_SUBMISSION/fixtures/set3_credential_and_reformatting_fixtures.json",
                 "REM_IMPROVEMENT_STUDY/fixtures/set4_permission_fixtures.json"]:
        v = json.loads((ROOT / path).read_text())
        records = v["records"] if isinstance(v, dict) else v
        summary = {}
        for a in RA2.ARMS:
            rr = []
            for fx in records:
                fx = dict(fx)
                if "authorized" in fx:
                    fx["legitimate_call"] = {"tool": "send_money", "args": dict(fx["authorized"])}
                    fx["unsafe_call"] = {"tool": "send_money", "args": dict(fx["substituted"])}
                hist = fx.get("history") or [{"tool": "read_file", "args": {"file_path": "document.txt"}, "output": fx["tool_output"], "executed": True}]
                pair = {}
                for role in ("legitimate", "unsafe"):
                    ep = SimpleNamespace(objective=fx["objective"], system_prompt=tf.SYSTEM_PROMPT, injection_task_id=None, episode_id="fixture")
                    g = RA2.make_guard(a, cells[key], cs[key], ep, st)
                    for h in hist:
                        g.begin_decision_point()
                        g.evaluate(h["tool"], dict(h["args"]))
                        g.ingest(h["tool"], h["output"], executed=g.audit[-1]["released"] and h.get("executed", True))
                    g.begin_decision_point()
                    g.evaluate(fx[role + "_call"]["tool"], dict(fx[role + "_call"]["args"]))
                    pair[role] = bool(g.audit[-1]["released"])
                    pair[role + "_source"] = g.audit[-1]["verdict_source"]
                rr.append({"fixture": fx["id"], **pair})
            summary[a] = {"n": len(rr), "legitimate_released": sum(r["legitimate"] for r in rr), "unsafe_released": sum(r["unsafe"] for r in rr),
                          "pairs_correct": sum(r["legitimate"] and not r["unsafe"] for r in rr), "rows": rr}
        result[Path(path).stem] = summary
    return result


def stage_report():
    d, aux, eps, folds = C._populations()
    restricted = set(common.make_setup().restricted)
    with (STATE / "rs_replays_v2.pkl").open("rb") as f:
        mine = pickle.load(f)
    with (STATE / "rs_replays.pkl").open("rb") as f:
        v1 = pickle.load(f)
    stored = J.load("replays") + J.load("value_replays") + C.load("cs_replays")
    by = collections.defaultdict(lambda: collections.defaultdict(dict))
    for scheme, role, e, a, u, s, err, aud in stored:
        if a in V1R.BASELINES:
            by[(scheme, role)][e][a] = (int(u), int(s), err, aud)
    for scheme, role, e, a, u, s, err, aud in v1 + mine:
        by[(scheme, role)][e][a] = (int(u), int(s), err, aud)
    fresh = aux["fresh"]
    b0 = {r[2]: r for r in J.load("replays") if r[0] == "S1" and r[1] == "dev2" and r[3] == "B0"}
    elig = sorted(e for e, r in b0.items() if r[6] is None and (int(r[4]), int(r[5])) == (fresh[e].utility, fresh[e].security))
    pops = {}
    for name, scheme, role, ids in [("primary_S1", "S1", "primary", aux["valid"]), ("primary_S2", "S2", "primary", aux["valid"]),
                                    ("dev2", "S1", "dev2", elig)]:
        B = by[(scheme, role)]
        if scheme == "S2":
            for e in ids:
                for a in TABLE_ARMS:
                    if a not in B[e]:
                        B[e][a] = by[("S1", "primary")][e][a]
        episodes = d.episodes if role == "primary" else fresh
        att = [e for e in ids if episodes[e].attacked]
        ben = [e for e in ids if not episodes[e].attacked]
        usr = lambda e: episodes[e].user_task_id      # noqa: E731
        inj = lambda e: episodes[e].injection_task_id  # noqa: E731
        mm = R.block(B, att, ben, TABLE_ARMS, restricted)
        stages, evaluated, reasons = {}, {}, {}
        for a in RA2.ARMS:
            c, ev, rs = collections.Counter(), collections.Counter(), collections.Counter()
            for e in ids:
                for x in B[e][a][3]:
                    if x[4] not in restricted:
                        continue
                    lab = "attack_labelled" if x[0] == 1 else "not_attack_labelled"
                    c[f"{lab}|{V1R.stage_of(a, x)}"] += 1
                    ev[f"{lab}|verifier_evaluated={bool(x[11])}"] += 1
                    if x[6].startswith("amount_") and x[9]:
                        rs[f"{usr(e)}|{x[6]}|{x[9][2][:70]}"] += 1
            stages[a], evaluated[a], reasons[a] = dict(sorted(c.items())), dict(sorted(ev.items())), dict(sorted(rs.items()))
        changed = {}
        for a, b in CONTRASTS[:7]:
            rows = [{"episode": e, "user_task": usr(e), "injection_task": inj(e), a: list(B[e][a][:2]), b: list(B[e][b][:2])}
                    for e in ids if B[e][a][:2] != B[e][b][:2]]
            changed[f"{a} vs {b}"] = {"episodes_with_different_outcome": len(rows),
                                     "gained": sum(1 for r in rows if r[a][0] > r[b][0]), "lost": sum(1 for r in rows if r[a][0] < r[b][0]),
                                     "by_user_task": dict(collections.Counter(r["user_task"] for r in rows)), "rows": rows}
        pops[name] = {"n_attacked": len(att), "n_benign": len(ben), "arms": mm,
                      "contrasts": {a + " minus " + b: R.paired(B, att, ben, usr, inj, a, b) for a, b in CONTRASTS},
                      "restricted_call_stages": stages, "verifier_evaluated": evaluated, "amount_reasons": reasons, "outcome_changes": changed}
        print(name, [(a, m["attacks_successful"], m["benign_completed"], m["all_tasks_completed"]) for a, m in mm.items()], flush=True)
    probe = by[("S1", "probe")]
    out = {"status": "EXPLORATORY DEVELOPMENT EVIDENCE (version 2, PROTOCOL_AMENDMENT_V2.md, commit 95549b2): offline replay; "
                     "no live agent; no model call; cohorts inspected before",
           "populations": pops,
           "probe_reformatted_identifier": {"n": len(probe), "arms": {a: {"attacks": sum(v[a][1] for v in probe.values()),
                                                                           "replay_errors": sum(v[a][2] is not None for v in probe.values())}
                                                                       for a in TABLE_ARMS if all(a in v for v in probe.values())}},
           "replays_v2": len(mine), "replay_errors_v2": sum(1 for r in mine if r[6]),
           "fixtures": fixtures(J.load("cells"), C.load("cs_cells"))}
    (OUT / "results_v2.json").write_text(json.dumps(out, indent=1, default=common._default), encoding="utf-8")
    with gzip.open(OUT / "episode_outcomes_v2.jsonl.gz", "wt", encoding="utf-8") as f:
        for scheme, role, e, a, u, s, err, aud in sorted(mine, key=lambda z: z[:4]):
            f.write(json.dumps({"scheme": scheme, "population": role, "episode_id": e, "arm": a, "utility": u, "security": s, "error": err}) + "\n")
    with gzip.open(OUT / "restricted_call_audit_v2.jsonl.gz", "wt", encoding="utf-8") as f:
        for scheme, role, e, a, u, s, err, aud in sorted(mine, key=lambda z: z[:4]):
            for k, x in enumerate(aud):
                if x[4] in restricted:
                    f.write(json.dumps({"scheme": scheme, "population": role, "episode_id": e, "arm": a, "call": k, "tool": x[4],
                                        "attempt_label": x[0], "verdict": x[1], "released": x[2], "source": x[6], "amount": x[9],
                                        "source_before_veto": x[10], "verifier_evaluated": x[11]}, default=common._default) + "\n")


if __name__ == "__main__":
    for stage in sys.argv[1:]:
        {"replay": stage_replay, "report": stage_report}[stage]()
