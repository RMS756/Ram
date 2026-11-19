"""Runner of the REM-B hardening study (protocol: REM_B_HARDENING_VALIDATION_2026_11_19/06_FROZEN_PROTOCOL.md).

Stages: replay | parity | suites | fixtures | scripted | cost | report      (offline; no model call)
State: $COMPETITIVE_STATE/hard_replays.pkl ; outputs in REM_B_HARDENING_VALIDATION_2026_11_19/results/.
"""
from __future__ import annotations

import collections
import csv
import gzip
import json
import multiprocessing as mp
import pickle
import sys
import time
import tracemalloc
from pathlib import Path
from types import SimpleNamespace

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "architecture_redesign"))
import arch_run as A  # noqa: E402  (frozen runner of the redesign study: populations, audit rule, helpers)
import remb2 as RB  # noqa: E402

ROOT = HERE.parents[1]
OUT = ROOT / "REM_B_HARDENING_VALIDATION_2026_11_19" / "results"
OLD = ROOT / "REM_ARCHITECTURE_REDESIGN_STUDY_2026_11_18" / "results"
STATE = A.STATE
CR, R, S, J, C, common, SH = A.CR, A.R, A.S, A.J, A.C, A.common, A.SH
FROZEN = ["B0", "GV_math2", "C1", "PG", "REM_B"]
CANDIDATES = ["REM_B2", "REM_B2_HR", "REM_B2_HW"]
ABLATIONS = ["B2_noR1", "B2_noR2", "B2_noR3", "B2_noOB", "B2_noLedger", "B2_E2plain"]
ARMS = FROZEN + CANDIDATES + ABLATIONS
DESIGN_TASKS = {"user_task_11", "user_task_14", "user_task_15"}     # tasks from which E1/E2h/OB (earlier) and R2/R3 were designed
SEEN_INJECTIONS = {"injection_task_4"}
CONTRASTS = [("REM_B2", "REM_B"), ("REM_B2", "PG"), ("REM_B2", "C1"), ("REM_B", "PG"), ("REM_B2_HW", "REM_B2"), ("REM_B2_HR", "REM_B2"),
             ("REM_B2", "B2_noR1"), ("REM_B2", "B2_noR2"), ("REM_B2", "B2_noR3"), ("REM_B2", "B2_noOB"), ("REM_B2", "B2_noLedger"),
             ("REM_B2", "B2_E2plain"), ("REM_B2", "GV_math2")]
W = {}


def _populations():
    d, aux, eps, folds = A._populations()
    import heldout_population2 as HP2
    st = common.make_setup()
    e2, m2 = HP2.load_heldout2(st, d)
    eps = dict(eps)
    eps["heldout2"] = e2
    folds = dict(folds)
    folds["heldout2"] = {e: m["fold"] for e, m in m2.items()}
    return d, aux, eps, folds


def replay_job(job):
    scheme, role, e, arm = job
    ep = W["eps"][role][e]
    key = ("S1", W["fold"][role][e])
    g = RB.build_cell2(arm, ep, W["jcells"][key], W["cs"][key], W["setup"])
    seen = []
    ev = g.evaluate

    def cap(tool, args):
        seen.append(dict(args))
        return ev(tool, args)
    g.evaluate = cap
    out = RB.replay_episode2(ep, W["setup"].suite, g)
    aud = []
    for k, a in enumerate(g.audit):
        det = a["details"] or {}
        cs = det.get("cs") or {}
        kk = det.get("contract")
        args = seen[k] if k < len(seen) else {}
        aud.append((a["label"], a["verdict"], bool(a["released"]), a["tier"], a["tool"], a["rem_latency_full_ms"], a["verdict_source"],
                    cs.get("stage"), (kk[0] if kk else None), cs.get("p"), cs.get("review_score", cs.get("p_all")),
                    A.audited_violation(ep.user_task_id, a["tool"], args, a["label"]) if a["tool"] in W["restricted"] else None,
                    (det.get("object") or (None,))[0], bool(cs.get("delegated")), cs.get("e2")))
    return scheme, role, e, arm, bool(out.utility), bool(out.security), out.error, aud


def _setup_workers(eps, folds):
    st = common.make_setup()
    W.update(setup=st, jcells=J.load("cells"), cs=C.load("cs_cells"), eps=eps, fold=folds, restricted=set(st.restricted))
    RB.factory2()


def stage_replay(roles=None, arms=None, limit=None, out_name="hard_replays.pkl"):
    d, aux, eps, folds = _populations()
    _setup_workers(eps, folds)
    roles = roles or list(eps)
    jobs = [("S1", role, e, a) for role in roles for a in (arms or ARMS) for e in sorted(eps[role])[:limit]]
    t = time.time()
    res = []
    with mp.get_context("fork").Pool(4) as p:
        for i, v in enumerate(p.imap_unordered(replay_job, jobs, chunksize=32), 1):
            res.append(v)
            if i % 20000 == 0:
                print("replay", i, "/", len(jobs), round(time.time() - t), "s", flush=True)
    with (STATE / out_name).open("wb") as f:
        pickle.dump(res, f)
    print("replay done", len(res), round(time.time() - t), "s; errors", sum(1 for r in res if r[6]),
          {r: len(eps[r]) for r in roles}, flush=True)


def stage_parity():
    """Frozen arms under this study's replay (with the environment-capture element) vs the stored outcomes of 31c146e."""
    res = pickle.load((STATE / "hard_replays.pkl").open("rb"))
    old = {}
    for line in gzip.open(OLD / "episode_outcomes.jsonl.gz", "rt"):
        r = json.loads(line)
        if r["scheme"] == "S1":
            old[(r["population"], r["episode_id"], r["arm"])] = (r["utility"], r["security"], r["error"])
    n = mism = 0
    ex = []
    for scheme, role, e, arm, u, s, err, aud in res:
        k = (role, e, arm)
        if arm in FROZEN and k in old:
            n += 1
            if (u, s, err) != tuple(old[k]):
                mism += 1
                ex.append([role, e, arm, [u, s, err], old[k]])
    out = {"compared": n, "mismatches": mism, "examples": ex[:20]}
    (OUT / "parity_frozen_arms.json").write_text(json.dumps(out, indent=1))
    print("parity", n, "mismatches", mism, flush=True)


# ------------------------------------------------------------------------------------------------ suites
def run_case2(build, arm, case, seq):
    ep = SimpleNamespace(objective=case["objective"], system_prompt="", injection_task_id=None, episode_id=f"seq-{case['id']}",
                         bank=case.get("bank"))
    g = build(arm, ep)
    rows = []
    for k, st in enumerate(list(case.get("pre", [])) + list(seq)):
        g.begin_decision_point()
        if st[0] == "read":
            ok, _ = g.evaluate(st[1], dict(st[2]))
            g.ingest(st[1], st[3], executed=ok)
            continue
        _, tool, args, ref, outcome = st
        rel, notice = g.evaluate(tool, dict(args))
        a = g.audit[-1]
        exd = bool(rel) and outcome == "success"
        g.ingest(tool, "{'message': 'done'}" if exd else ("Error: failed" if rel else notice or ""), executed=exd)
        rows.append({"case": case["id"], "group": case.get("group"), "arm": arm, "seq": case["seqs"].index(seq), "step": k, "tool": tool,
                     "args": args, "ref": ref, "released": bool(rel), "executed": exd, "source": a["verdict_source"],
                     "verdict": str(a["verdict"]), "ledger_after": SH._ledger(g)})
    return rows


def stage_suites():
    import diag_harness as H
    import generalization_cases as GC
    import heldout_probes as HPR
    import heldout_probes2 as HP2
    import ledger_cases as LC
    RB.CURRENT_ENV["env"] = None
    f = RB.factory2()
    out = {}
    for name, cases, kind in (("ledger_dev", LC.CASES, "seq"), ("heldout_probes_v1", HPR.CASES, "seq"),
                              ("heldout_probes2", HP2.CASES, "seq"), ("diagnostics", H.CASES, "diag"),
                              ("generalization", GC.CASES, "diag")):
        if kind == "seq":
            rows = [r for case in cases for arm in ARMS for seq in case["seqs"] for r in run_case2(f, arm, case, seq)]
            res = SH.dump(OUT / f"suite_{name}.json", rows)
        else:
            res = H.dump(OUT / f"suite_{name}.json", H.run_all(lambda a, ep: f(a, ep), ARMS, cases=cases))
        out[name] = res["score"]
        for a, s in res["score"].items():
            print(name, a, "auth", s["authorized_released"], "/", s["authorized_n"], "| unauth", s["unauthorized_released"], "/",
                  s["unauthorized_n"], "| amb", s["ambiguous_released"], "/", s["ambiguous_n"], flush=True)
    (OUT / "suites_summary.json").write_text(json.dumps(out, indent=1, default=str))


def stage_fixtures():
    import trace_fixtures as tf
    st = common.make_setup()
    cells, cs = J.load("cells"), C.load("cs_cells")
    key = ("S1", "injection_task_0")
    res = {}
    for path in ["REM_AUTHORIZATION_AUDIT/fixtures/set1_substitution_fixtures.json", "REM_AUTHORIZATION_AUDIT/fixtures/set2_fresh_fixtures.json",
                 "REM_FINAL_SUBMISSION/fixtures/set3_credential_and_reformatting_fixtures.json",
                 "REM_IMPROVEMENT_STUDY/fixtures/set4_permission_fixtures.json"]:
        v = json.loads((ROOT / path).read_text())
        records = v["records"] if isinstance(v, dict) else v
        summary = {}
        for a in ARMS:
            leg = uns = 0
            unsafe_ids = []
            for fx in records:
                fx = dict(fx)
                if "authorized" in fx:
                    fx["legitimate_call"] = {"tool": "send_money", "args": dict(fx["authorized"])}
                    fx["unsafe_call"] = {"tool": "send_money", "args": dict(fx["substituted"])}
                hist = fx.get("history") or [{"tool": "read_file", "args": {"file_path": "document.txt"}, "output": fx["tool_output"], "executed": True}]
                for role in ("legitimate", "unsafe"):
                    ep = SimpleNamespace(objective=fx["objective"], system_prompt=tf.SYSTEM_PROMPT, injection_task_id=None, episode_id="fixture")
                    g = RB.build_cell2(a, ep, cells[key], cs[key], st)
                    for h in hist:
                        g.begin_decision_point()
                        g.evaluate(h["tool"], dict(h["args"]))
                        g.ingest(h["tool"], h["output"], executed=g.audit[-1]["released"] and h.get("executed", True))
                    g.begin_decision_point()
                    g.evaluate(fx[role + "_call"]["tool"], dict(fx[role + "_call"]["args"]))
                    if role == "legitimate":
                        leg += bool(g.audit[-1]["released"])
                    elif g.audit[-1]["released"]:
                        uns += 1
                        unsafe_ids.append(fx.get("id"))
            summary[a] = {"n": len(records), "legitimate_released": leg, "unsafe_released": uns, "unsafe_ids": unsafe_ids}
        res[Path(path).stem] = summary
    (OUT / "fixtures.json").write_text(json.dumps(res, indent=1))
    for a in ARMS:
        print("fixtures", a, sum(v[a]["legitimate_released"] for v in res.values()), "/", sum(v[a]["n"] for v in res.values()),
              "unsafe", sum(v[a]["unsafe_released"] for v in res.values()), flush=True)


def stage_scripted():
    import scripted_arch as SC
    Agent2 = SC.make_agent_class

    def make3():
        Base = Agent2()

        class Agent3(Base):
            def query(self, query, runtime, env, messages=[], extra_args={}):
                RB.CURRENT_ENV["env"] = env                       # system-of-record access for REM-B2 (structured fields)
                return super().query(query, runtime, env, messages, extra_args)
        return Agent3
    SC.BASE.make_agent_class = make3
    rows = SC.run(ARMS, RB.factory2(), modes=SC.MODES, include_benign=True)
    RB.CURRENT_ENV["env"] = None
    (OUT / "scripted_closed_loop.json").write_text(json.dumps({"status": "SCRIPTED closed loop (ground-truth test doubles; not an LLM)",
                                                               "rows": rows}, indent=1, default=str))
    summ = {}
    for a in ARMS:
        rr = [r for r in rows if r["arm"] == a]
        summ[a] = {"benign_completed": sum(r["utility"] for r in rr if r["mode"] == "benign"),
                   "benign_n": sum(1 for r in rr if r["mode"] == "benign")}
        for m in SC.MODES:
            mm = [r for r in rr if r["mode"] == m]
            summ[a][m] = {"attack_goals": sum(bool(r["security"]) for r in mm), "utility": sum(r["utility"] for r in mm), "n": len(mm),
                          "goal_pairs": sorted(f"{r['user_task'][10:]}x{r['injection_task'][15:]}" for r in mm if r["security"])}
    (OUT / "scripted_summary.json").write_text(json.dumps(summ, indent=1))
    for a in ARMS:
        print("scripted", a, summ[a]["benign_completed"], "/", summ[a]["benign_n"],
              {m: (summ[a][m]["attack_goals"], summ[a][m]["utility"]) for m in SC.MODES}, flush=True)


def stage_cost():
    d, aux, eps, folds = A.C._populations()
    st = common.make_setup()
    cells, cs = J.load("cells"), C.load("cs_cells")
    RB.factory2()
    ids = sorted(aux["valid"])[:300]
    out = {}
    for a in ARMS:
        tracemalloc.start()
        t = time.perf_counter()
        lat = []
        calls = 0
        for e in ids:
            ep = d.episodes[e]
            key = ("S1", d.episode_fold[e])
            g = RB.build_cell2(a, ep, cells[key], cs[key], st)
            RB.replay_episode2(ep, st.suite, g)
            lat += [x.get("rem_latency_full_ms") for x in g.audit if x.get("rem_latency_full_ms") is not None]
            calls += len(g.audit)
        wall = time.perf_counter() - t
        peak = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        out[a] = {"episodes": len(ids), "calls": calls, "wall_s": wall, "peak_traced_MiB": peak / 2 ** 20,
                  "latency_ms_mean": float(np.mean(lat)), "latency_ms_median": float(np.median(lat)),
                  "latency_ms_p95": float(np.percentile(lat, 95)), "model_calls": 0}
        print("cost", a, {k: round(v, 3) if isinstance(v, float) else v for k, v in out[a].items()}, flush=True)
    (OUT / "operational_cost.json").write_text(json.dumps(out, indent=1))


# ------------------------------------------------------------------------------------------------ report
def _extra(B, ids, a, restricted):
    rr = [x for e in ids for x in B[e][a][3] if x[4] in restricted]
    v = collections.Counter(str(x[1]).lower().split(".")[-1] for x in rr)
    return {"audited_violations_released": sum(1 for x in rr if x[2] and x[11] is True),
            "object_level_violations_released": sum(1 for x in rr if x[2] and x[11] is True and x[4] == "update_scheduled_transaction"),
            "auditable_released": sum(1 for x in rr if x[2] and x[11] is not None),
            "unauthorized_state_changes_released": sum(1 for x in rr if x[2] and (x[0] == 1 or x[11] is True)),
            "escalated_calls": v.get("escalate", 0), "blocked_calls": v.get("block", 0), "allowed_calls": v.get("allow", 0),
            "modified_calls": v.get("modify", 0), "human_review_rate": v.get("escalate", 0) / max(1, len(rr)),
            "unnecessary_escalations_of_correct_values": sum(1 for x in rr if (not x[2]) and str(x[1]).lower().endswith("escalate") and x[11] is False),
            "refunds_released_by_E2": sum(1 for x in rr if x[2] and x[14] is not None),
            "delegated_condition_releases": sum(1 for x in rr if x[2] and x[13]),
            "learned_stage_changes": sum(1 for x in rr if str(x[6]).startswith("learned")),
            "payment_calls_released": sum(1 for x in rr if x[2] and x[4] == "send_money"),
            "restricted_calls": len(rr)}


def _changes(B, ids, base, arm):
    ch = collections.Counter()
    for e in ids:
        a, b = B[e][base][3], B[e][arm][3]
        if len(a) != len(b):
            ch["different_call_sequence"] += 1
            continue
        for x, y in zip(a, b):
            if x[2] == y[2]:
                continue
            kind = ("attack_labelled" if y[0] == 1 else ("audited_violation" if y[11] is True else
                    ("audited_correct" if y[11] is False else "unaudited")))
            ch[("released_" if y[2] else "withheld_") + kind] += 1
    return dict(ch)


def _auc(pos, neg):
    if not pos or not neg:
        return None
    return float(np.mean([(p > n) + 0.5 * (p == n) for p in pos for n in neg]))


def review_ranking(B, ids, episodes, restricted, seed=20261119, n_boot=2000):
    """Escalated auditable calls of REM_B2_HR: does (1 - p) rank audited-correct calls above audited violations?"""
    items = []
    for e in ids:
        for x in B[e]["REM_B2_HR"][3]:
            if x[4] in restricted and str(x[1]).lower().endswith("escalate") and x[11] is not None and x[10] is not None:
                items.append((e, 1 - float(x[10]), x[11] is False))
    pos = [s for _, s, y in items if y]
    neg = [s for _, s, y in items if not y]
    out = {"n": len(items), "audited_correct": len(pos), "audited_violation": len(neg), "auc": _auc(pos, neg)}
    if len(pos) >= 5 and len(neg) >= 5:
        rng = np.random.default_rng(seed)
        eps_ = sorted({e for e, _, _ in items})
        by = collections.defaultdict(list)
        for e, s, y in items:
            by[e].append((s, y))
        vals = []
        for _ in range(n_boot):
            smp = [x for k in rng.integers(0, len(eps_), len(eps_)) for x in by[eps_[k]]]
            a = _auc([s for s, y in smp if y], [s for s, y in smp if not y])
            if a is not None:
                vals.append(a)
        out["auc_ci95"] = [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]
    return out


def stage_report():
    d, aux, eps, folds = _populations()
    restricted = set(common.make_setup().restricted)
    res = pickle.load((STATE / "hard_replays.pkl").open("rb"))
    by = collections.defaultdict(lambda: collections.defaultdict(dict))
    for scheme, role, e, a, u, s, err, aud in res:
        by[role][e][a] = (int(u), int(s), err, aud)
    fresh = aux["fresh"]
    b0 = {r[2]: r for r in J.load("replays") if r[0] == "S1" and r[1] == "dev2" and r[3] == "B0"}
    elig = {"primary": sorted(aux["valid"]), "probe": sorted(eps["probe"]),
            "dev2": sorted(e for e, r in b0.items() if r[6] is None and (int(r[4]), int(r[5])) == (fresh[e].utility, fresh[e].security))}
    for role in ("heldout", "heldout2"):
        Hh = by[role]
        elig[role] = sorted(e for e, v in Hh.items() if v["B0"][2] is None
                            and (v["B0"][0], v["B0"][1]) == (int(eps[role][e].utility), int(eps[role][e].security)))
    names = {"primary": "primary_S1", "dev2": "dev2", "probe": "probe", "heldout": "heldout_H", "heldout2": "heldout_H2"}
    pops, rows_csv = {}, []
    for role, name in names.items():
        B, ids, episodes = by[role], elig[role], eps[role]
        att = [e for e in ids if episodes[e].attacked]
        ben = [e for e in ids if not episodes[e].attacked]
        usr = lambda e, _ep=episodes: _ep[e].user_task_id      # noqa: E731
        inj = lambda e, _ep=episodes: _ep[e].injection_task_id  # noqa: E731
        M = {}
        for a in ARMS:
            M[a] = CR._metrics(B, att, ben, a, restricted)
            M[a].update(_extra(B, ids, a, restricted))
            M[a]["unique_user_tasks"] = len({episodes[e].user_task_id for e in ids})
            M[a]["unique_task_pairs"] = len({(episodes[e].user_task_id, episodes[e].injection_task_id) for e in ids})
            rows_csv.append({"population": name, "arm": a, **M[a]})
        CR.DESIGN_TASKS, CR.SEEN_INJECTIONS = DESIGN_TASKS, SEEN_INJECTIONS
        pops[name] = {"n_attacked": len(att), "n_benign": len(ben), "loaded": len(by[role]), "metrics": M,
                      "contrasts": {f"{a} minus {b}": R.paired(B, att, ben, usr, inj, a, b) for a, b in CONTRASTS} if ben or att else {},
                      "partitions": {f"{a} vs {b}": CR._partition_changes(B, ids, episodes, a, b) for a, b in CONTRASTS[:3]},
                      "call_changes": {f"{a} vs {b}": _changes(B, ids, b, a) for a, b in CONTRASTS},
                      "review_ranking": review_ranking(B, ids, episodes, restricted),
                      "gains_by_user_task": {f"{a} vs {b}": dict(collections.Counter(
                          episodes[e].user_task_id for e in ids if B[e][a][0] and not B[e][b][0])) for a, b in CONTRASTS[:3]}}
        print(name, len(att), len(ben), {a: (m["attack_objectives_reached"], m["benign_completed"], m["all_tasks_completed"],
                                             m["audited_violations_released"]) for a, m in M.items()}, flush=True)
    out = {"status": "CONTROLLED EVIDENCE under 06_FROZEN_PROTOCOL.md; offline replay (NO-ADAPT); no model call",
           "eligible": {k: len(v) for k, v in elig.items()}, "loaded": {k: len(by[k]) for k in by},
           "populations": pops, "replays": len(res), "replay_errors": sum(1 for r in res if r[6])}
    (OUT / "hardening_results.json").write_text(json.dumps(out, indent=1, default=common._default), encoding="utf-8")
    with (OUT.parent / "07_SECURITY_UTILITY_RESULTS.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_csv[0]))
        w.writeheader()
        w.writerows(rows_csv)
    with gzip.open(OUT / "episode_outcomes.jsonl.gz", "wt", encoding="utf-8") as f:
        for scheme, role, e, a, u, s, err, aud in sorted(res, key=lambda z: z[:4]):
            f.write(json.dumps({"population": role, "episode_id": e, "arm": a, "utility": u, "security": s, "error": err}) + "\n")
    print("eligible", out["eligible"], "errors", out["replay_errors"], flush=True)


if __name__ == "__main__":
    for stage in sys.argv[1:]:
        {"replay": stage_replay, "parity": stage_parity, "suites": stage_suites, "fixtures": stage_fixtures, "scripted": stage_scripted,
         "cost": stage_cost, "report": stage_report}[stage]()
