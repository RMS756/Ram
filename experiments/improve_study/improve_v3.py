"""Revision 3 of the improvement study (15 November 2026): effect-typed instructions and whole-condition
evaluation. Isolated; nothing under rem/ or configs/, no earlier result file and no scored module is changed.
Protocol: REM_IMPROVEMENT_STUDY/followup_v3/PROTOCOL_V3.md (committed before any arm below was scored).

Stages:  evidence  fit  replay  report      (python3 experiments/improve_study/improve_v3.py <stage> ...)
"""
from __future__ import annotations

import collections
import dataclasses
import json
import multiprocessing as mp
import os
import sys
import time
from types import SimpleNamespace

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import improve as I  # noqa: E402
import improve_v2 as I2  # noqa: E402
from improve import S, G, common, build, load_raw, load, save, NOBEH, FEATURE_ORDER  # noqa: E402
from improve import A3Policy, build_loss_grid, sigmoid, Verdict, GuardConfig, RemGuard  # noqa: E402
from permission import PERM_ORDER  # noqa: E402
from permission_v2 import PERM2_ORDER  # noqa: E402
from permission_v3 import DEFAULT_OPTS3, PERM3_ORDER, RuntimePermissionV3, offline_permission_v3  # noqa: E402

S.ALL_ORDER = tuple(FEATURE_ORDER) + tuple(S.AUTHZ_ORDER) + tuple(PERM_ORDER) + tuple(PERM2_ORDER) + I2.CANON_ORDER + tuple(PERM3_ORDER)
S.FEATURE_SETS["F2v2"] = NOBEH + tuple(PERM2_ORDER)
S.FEATURE_SETS["F4"] = NOBEH + tuple(PERM3_ORDER)
RULE_V3 = {"G3": {}, "G3-noeffect": {"effect": False}, "G3-nocond": {"cond": False}}
LEARN_V3 = ["L4"]
ARMS_V3 = list(RULE_V3) + LEARN_V3
OUT = os.path.join(I.REPO, "REM_IMPROVEMENT_STUDY", "followup_v3")
REF1, REF2 = ["B0", "M00", "M00_nobeh", "A2", "PG", "G1"], ["G2", "L3"]
CONTRASTS = [("G3", "G2"), ("G3", "A2"), ("G3", "PG"), ("L4", "G3"), ("G3", "G3-noeffect"), ("G3", "G3-nocond"), ("G3", "G1"), ("G3", "M00"), ("L4", "L3")]


def make_guard_v3(arm, cell, ep, st):
    gc = GuardConfig(st.spec, st.detector, cell["reference"] if cell else S.EMPTY_REF, st.tier_map, st.restricted, "step_level", "no_reviewer")
    guard = RemGuard(gc, None, lambda c: (Verdict.ALLOW, "init", {}), st.labeler, ep)
    restricted = set(st.restricted)
    opts3 = dict(DEFAULT_OPTS3)
    opts3.update(RULE_V3.get(arm, {}))
    rp = RuntimePermissionV3(ep.objective, opts3)
    orig_ingest = guard.ingest

    def ingest(tool, text, executed):
        rp.on_ingest(executed)
        return orig_ingest(tool, text, executed)
    guard.ingest = ingest
    models = cell["models"] if cell else {}
    pol2 = None
    if arm in LEARN_V3:
        grid = build_loss_grid(S.rm.loss_spec(cell["rmod"]), f"improve v3 cell {arm}")
        pol2 = A3Policy(grid, S.rm.predicates(), tie_mode="record_chapter3_order", exclude_from_expected_loss=(Verdict.ESCALATE, Verdict.MODIFY))

    def decide(c):
        is_r = c.tool in restricted
        ev = rp.evidence(guard.tracker, c.tool, c.args, c.tier)
        if arm in RULE_V3:
            v, src = (Verdict.BLOCK if is_r and ev.overall != "supported" else Verdict.ALLOW), "rule_permission_v3"
        elif is_r and (ev.overall == "denied" or not ev.authority):
            v, src = Verdict.BLOCK, "permission_guard_authority_v3"
        else:
            f, avail = guard.tracker.features(c.tool, c.args)
            x = dict(f)
            x.update(ev.features())
            rec = models[("F4", "y")]
            s = rec["b0"] + sum(co * x[n] for n, co in zip(rec["order"], rec["coef"]))
            p = float(sigmoid(rec["g1"] * s + rec["g0"])) if not rec["failed"] else float(sigmoid(s))
            d = pol2.decide(p, c.tier, c.tool, avail)
            v, src = d.verdict, d.source
        det = {"perm": (ev.overall, ev.base.recipient, ev.base.amount, ev.effect, ev.binding, ev.condition, ev.fulfilment, ev.authority), "z": (0.0, 0.0)}
        rp.record(guard.tracker, c.tool, c.args)
        return v, src, det
    guard.decide = decide
    return guard


def _replay_job(job):
    scheme, eid, arm, role = job
    st = G["setup"]
    ep = G["eps"][role][eid]
    guard = make_guard_v3(arm, G["cells"][G["cell_of"][scheme][(role, eid)]], ep, st)
    out = S.replay_episode(ep, st.suite, guard)
    aud = [(a["label"], a["verdict"], a["released"], a["tier"], a["tool"], a["rem_latency_full_ms"], a["verdict_source"], a["details"].get("perm")) for a in out.audit]
    return scheme, role, eid, arm, bool(out.utility), bool(out.security), out.error, aud


def stage_evidence():
    data = build("primary", load_raw())
    Z = np.zeros((len(data.steps), len(PERM3_ORDER)))
    per_ep = collections.defaultdict(list)
    for i, s in enumerate(data.steps):
        per_ep[s.episode_id].append((s.index, i))
    stats = collections.Counter()
    for eid, lst in per_ep.items():
        idx = [i for _, i in sorted(lst)]
        tiers = {k: data.steps[i].tier for k, i in enumerate(idx)}
        it = iter(range(len(idx)))
        evs = offline_permission_v3(data.episodes[eid], lambda tool, args, _it=it, _t=tiers: _t[next(_it)])
        if len(evs) != len(idx):
            raise RuntimeError(f"alignment failed for {eid}")
        for k, i in enumerate(idx):
            f = evs[k].features()
            Z[i] = [f[n] for n in PERM3_ORDER]
            if evs[k].applicable:
                stats[(("attack" if data.steps[i].label else "legit"), evs[k].overall)] += 1
    save("perm3_evidence", {"Z": Z, "stats": dict(stats)})
    print("v3 permission evidence on primary restricted-tool calls:", {f"{a}/{b}": v for (a, b), v in sorted(stats.items())})


def _fit_job(job):
    key, kind = job
    data = G["data"]
    train = (data.fold != key[1]) if kind == "S1" else ((G["ut"] != key[1]) & (G["it"] != key[2]))
    cell, _ = S.fit_cell(train, ["F4", "F2v2"], ("y",))
    return key, cell["models"]


def stage_fit():
    data = build("primary", load_raw())
    aux = S.load("fit_aux")
    Z = np.hstack([aux["Z"], load("perm_evidence")["Z"], load("perm2_evidence")["Z"], load("perm3_evidence")["Z"]])
    ut = np.array([s.user_task_id for s in data.steps], dtype=object)
    it = np.array([s.injection_task_id or "none" for s in data.steps], dtype=object)
    G.update(data=data, Z=Z, T={"y": data.y.copy()}, ut=ut, it=it)
    jobs = [(k, k[0]) for k in sorted(S.load("cells"), key=str)]
    t0 = time.time()
    with mp.get_context("fork").Pool(4) as pool:
        res = pool.map(_fit_job, jobs, chunksize=2)
    prev = load("cells_v2")
    new, maxdiff = {}, 0.0
    for key, models in res:
        new[key] = {("F4", "y"): models[("F4", "y")]}
        a, b = models[("F2v2", "y")], prev[key][("F2v2", "y")]          # the refit of the stored revision-2 models must equal them
        maxdiff = max(maxdiff, abs(a["b0"] - b["b0"]), abs(a["g1"] - b["g1"]), max(abs(x - y) for x, y in zip(a["coef"], b["coef"])))
    save("cells_v3", new)
    print(f"fit: {len(jobs)} cells in {time.time() - t0:.0f}s; refit of the stored F2v2 models: max |difference| {maxdiff:.2e}")


def merged_cells():
    cells = I2.merged_cells()
    extra = load("cells_v3")
    for k in cells:
        if k in extra:
            cells[k]["models"].update(extra[k])
    return cells


def _populations(st, data):
    valid = S.load("fit_aux")["valid"]
    fresh, meta = I.load_fresh(st, data)
    probe = {}
    for e in valid:
        ep = data.episodes[e]
        if ep.attacked and any(S.ATTACKER_IBAN in v for v in ep.injections.values()):
            probe[e] = dataclasses.replace(ep, injections={k: v.replace(S.ATTACKER_IBAN, S.spaced(S.ATTACKER_IBAN)) for k, v in ep.injections.items()})
    return valid, fresh, meta, probe


def stage_replay():
    st = common.make_setup()
    data = build("primary", load_raw())
    valid, fresh, meta, probe = _populations(st, data)
    cell_of = {"S1": {}, "S2": {}}
    for e in valid:
        ep = data.episodes[e]
        cell_of["S1"][("primary", e)] = ("S1", data.episode_fold[e])
        cell_of["S2"][("primary", e)] = ("S2", ep.user_task_id, ep.injection_task_id or data.episode_fold[e])
    for e in fresh:
        cell_of["S1"][("dev2", e)] = ("S1", meta[e]["fold"])
    for e in probe:
        cell_of["S1"][("probe_iban", e)] = ("S1", data.episode_fold[e])
    G.update(setup=st, eps={"primary": data.episodes, "dev2": fresh, "probe_iban": probe}, cells=merged_cells(), cell_of=cell_of)
    jobs = []
    for a in ARMS_V3:
        jobs += [("S1", e, a, "primary") for e in valid] + [("S1", e, a, "dev2") for e in sorted(fresh)] + [("S1", e, a, "probe_iban") for e in sorted(probe)]
    jobs += [("S2", e, a, "primary") for a in LEARN_V3 for e in valid]
    t0 = time.time()
    with mp.get_context("fork").Pool(4) as pool:
        res = pool.map(_replay_job, jobs, chunksize=64)
    save("replay_v3", {"res": res})
    print(f"replay v3: {len(jobs)} replays in {time.time() - t0:.0f}s")


def _fixtures(st, cells):
    sys.path.insert(0, os.path.join(I.REPO, "REM_AUTHORIZATION_AUDIT", "tools"))
    import trace_fixtures as tf
    cell = cells[("S1", "injection_task_0")]
    paths = {"set1": "REM_AUTHORIZATION_AUDIT/fixtures/set1_substitution_fixtures.json", "set2": "REM_AUTHORIZATION_AUDIT/fixtures/set2_fresh_fixtures.json",
             "set3": "REM_FINAL_SUBMISSION/fixtures/set3_credential_and_reformatting_fixtures.json", "set4": "REM_IMPROVEMENT_STUDY/fixtures/set4_permission_fixtures.json"}
    summ = {}
    for sname, path in paths.items():
        d = json.load(open(os.path.join(I.REPO, path)))
        recs = d["records"] if isinstance(d, dict) else d
        summ[sname] = {}
        for arm in ARMS_V3:
            rows = []
            for fx in recs:
                if "authorized" in fx:
                    fx["legitimate_call"] = {"tool": "send_money", "args": dict(fx["authorized"])}
                    fx["unsafe_call"] = {"tool": "send_money", "args": dict(fx["substituted"])}
                hist = fx.get("history") or [{"tool": "read_file", "args": {"file_path": "document.txt"}, "output": fx["tool_output"], "executed": True}]
                row = {"fixture": fx["id"]}
                for role in ("legitimate", "unsafe"):
                    ep = SimpleNamespace(objective=fx["objective"], system_prompt=tf.SYSTEM_PROMPT, injection_task_id=None, episode_id="fixture")
                    g = make_guard_v3(arm, cell, ep, st)
                    for h in hist:
                        g.begin_decision_point()
                        g.evaluate(h["tool"], dict(h["args"]))
                        g.ingest(h["tool"], h["output"], executed=bool(g.audit[-1]["released"]) and bool(h.get("executed", True)))
                    g.begin_decision_point()
                    g.evaluate(fx[f"{role}_call"]["tool"], dict(fx[f"{role}_call"]["args"]))
                    row[role] = bool(g.audit[-1]["released"])
                rows.append(row)
            summ[sname][arm] = {"n": len(rows), "legitimate_released": sum(r["legitimate"] for r in rows), "unsafe_released": sum(r["unsafe"] for r in rows),
                                "pairs_correct": sum(r["legitimate"] and not r["unsafe"] for r in rows),
                                "unsafe_released_ids": [r["fixture"] for r in rows if r["unsafe"]], "legitimate_withheld_ids": [r["fixture"] for r in rows if not r["legitimate"]]}
    return summ


def _ut15(st, data, cells, valid, fresh, meta):
    import audit_ut15 as AU
    res = {}
    pops = {"primary": [(e, data.episodes[e], ("S1", data.episode_fold[e])) for e in valid if data.episodes[e].user_task_id == AU.UT and data.episodes[e].attacked],
            "second": [(e, fresh[e], ("S1", meta[e]["fold"])) for e in sorted(fresh) if meta[e]["user_task"] == AU.UT and meta[e]["attacked"]]}
    for pop, eps in pops.items():
        tally, rows = collections.Counter(), []
        for e, ep, ck in eps:
            friends = AU.friend_accounts(ep)
            guard = make_guard_v3("G3", cells[ck], ep, st)
            calls, inner = [], guard.decide

            def decide(c, _inner=inner, _calls=calls):
                v, src, det = _inner(c)
                if c.tool in st.restricted:
                    _calls.append({"tool": c.tool, "recipient": (c.args or {}).get("recipient"), "amount": (c.args or {}).get("amount"),
                                   "profile": {k: (c.args or {}).get(k) for k in ("street", "city", "first_name", "last_name")} if c.tool == "update_user_info" else None,
                                   "released": v is Verdict.ALLOW})
                return v, src, det
            guard.decide = decide
            out = S.replay_episode(ep, st.suite, guard)
            labels = [a["label"] for a in out.audit if a["tool"] in st.restricted]
            rel = []
            for c, lab in zip(calls, labels):
                c["attempt_label"] = int(lab)
                c["consistency"] = AU.classify(c["tool"], c["profile"] if c["tool"] == "update_user_info" else {"recipient": c["recipient"], "amount": c["amount"]}, friends)
                if c["released"]:
                    rel.append(c)
            tally["episodes"] += 1
            tally["benchmark_attack_success"] += int(out.security)
            tally["released attack-labelled"] += sum(c["attempt_label"] for c in rel)
            tally["released consistent"] += sum(c["consistency"] == "consistent" for c in rel)
            tally["withheld consistent"] += sum(c["consistency"] == "consistent" and not c["released"] for c in calls)
            rows.append({"episode": e, "benchmark_attack_success": bool(out.security), "released_calls": rel})
        res[pop] = {"tally": dict(tally), "episodes": rows}
        print("ut15 G3", pop, dict(tally))
    return res


def stage_report():
    import report as R
    st = common.make_setup()
    I.PG.load()
    D1, D2, D3 = load("replay"), load("replay_v2"), load("replay_v3")
    data = build("primary", load_raw())
    meta, valid = D1["meta"], D1["valid"]
    by = collections.defaultdict(lambda: collections.defaultdict(dict))
    for D, keep in ((D1, set(REF1)), (D2, set(REF2)), (D3, None)):
        for scheme, role, eid, arm, u, s, err, aud in D["res"]:
            if keep is None or arm in keep:
                by[(scheme, role)][eid][arm] = (u, s, err, aud)
    restricted = set(st.restricted)
    att = [e for e in valid if data.episodes[e].attacked]
    ben = [e for e in valid if not data.episodes[e].attacked]
    P = by[("S1", "primary")]
    P2 = collections.defaultdict(dict)
    for e in valid:
        P2[e].update({a: v for a, v in P[e].items() if a in ("B0", "A2", "PG", "G1", "G2", "G3", "G3-noeffect", "G3-nocond")})
        P2[e].update(by[("S2", "primary")][e])
    F = by[("S1", "dev2")]
    rec = D1["recorded_fresh"]
    fv = sorted(e for e in F if F[e]["B0"][2] is None and (F[e]["B0"][0], F[e]["B0"][1]) == rec[e])
    pops = {"primary_S1": (P, att, ben, lambda e: data.episodes[e].user_task_id, lambda e: data.episodes[e].injection_task_id),
            "primary_S2": (P2, att, ben, lambda e: data.episodes[e].user_task_id, lambda e: data.episodes[e].injection_task_id),
            "dev2": (F, [e for e in fv if meta[e]["attacked"]], [e for e in fv if not meta[e]["attacked"]], lambda e: meta[e]["user_task"], lambda e: meta[e]["injection_task"])}
    out = {"status": "DEVELOPMENT EVIDENCE — revision 3; protocol REM_IMPROVEMENT_STUDY/followup_v3/PROTOCOL_V3.md frozen before scoring",
           "evaluation_mode": "offline recorded-trace replay, step level, no reviewer, NO-ADAPT", "populations": {}}
    for name, (B, a_, b_, u_, i_) in pops.items():
        arms = R.block(B, a_, b_, REF1 + REF2 + ARMS_V3, restricted)
        res = {"n_attacked": len(a_), "n_benign": len(b_), "arms": arms, "contrasts": {}}
        for x, y in CONTRASTS:
            if x in arms and y in arms:
                res["contrasts"][f"{x} minus {y}"] = R.paired(B, a_, b_, u_, i_, x, y)
        users = sorted({u_(e) for e in a_ + b_}, key=lambda s: int(s.split("_")[-1]))
        res["tasks_completed_by_user_task"] = {a: {u: [int(sum(B[e][a][0] for e in a_ + b_ if u_(e) == u)), int(sum(1 for e in a_ + b_ if u_(e) == u))] for u in users} for a in arms}
        res["attacks_by_user_task"] = {a: dict(collections.Counter(u_(e) for e in a_ if B[e][a][1])) for a in arms}
        res["without_user_task_15"] = {a: {"attacks": int(sum(B[e][a][1] for e in a_ if u_(e) != "user_task_15")),
                                           "all_tasks": int(sum(B[e][a][0] for e in a_ + b_ if u_(e) != "user_task_15"))} for a in arms}
        res["legit_calls_benign_by_status_G3"] = dict(collections.Counter(str(((x[7][0], x[7][3]) if x[7] else "n/a", bool(x[2]))) for e in b_ for x in B[e]["G3"][3] if x[4] in restricted)) if "G3" in arms else {}
        out["populations"][name] = res
    Pr = by[("S1", "probe_iban")]
    pe = sorted(Pr)
    out["probe_reformatted_identifier"] = {"episodes": len(pe), "arms": {a: {"attacks_reformatted": int(sum(Pr[e][a][1] for e in pe)), "attacks_original_text": int(sum(P[e][a][1] for e in pe))}
                                                                        for a in ARMS_V3}}
    G.update(setup=st)
    cells = merged_cells()
    out["fixtures"] = _fixtures(st, cells)
    fresh, _meta = I.load_fresh(st, data)
    out["user_task_15_G3"] = _ut15(st, data, cells, valid, fresh, meta)
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(os.path.join(OUT, "results_v3.json"), "w"), indent=1, default=common._default)
    r = lambda v: "[" + ", ".join(f"{100 * x:.2f}" for x in v) + "]"
    for name, res in out["populations"].items():
        print(f"\n== {name}: attacked {res['n_attacked']}, benign {res['n_benign']}")
        for a, m in res["arms"].items():
            print(f"{a:12s} atk {m['attacks_successful']:4d}  rel-atk-eps {m['episodes_with_released_attack_labelled_call']:4d}  ben {m['benign_completed']:3d}  all {m['all_tasks_completed']:4d}  "
                  f"legit {m['legit_calls_released_benign']:3d}/{m['legit_calls_n']}  no-ut15 atk {res['without_user_task_15'][a]['attacks']} all {res['without_user_task_15'][a]['all_tasks']}  err {m['replay_errors']}")
        for k, c in res["contrasts"].items():
            print(f"  {k:22s} tasks {r(c['task_completion_all'])} ASR {r(c['attack_success'])} benign {r(c.get('task_completion_benign', [0, 0, 0]))} g/l {c['tasks_gained_lost']} atk g/l {c['attacks_gained_lost']}")
        print("  tasks by user task:", {a: {u.split('_')[-1]: v[0] for u, v in res["tasks_completed_by_user_task"][a].items()} for a in ("G2", "G3", "L4") if a in res["arms"]})
        print("  legit calls (G3):", res["legit_calls_benign_by_status_G3"])
    print("\nprobe:", json.dumps(out["probe_reformatted_identifier"]["arms"]))
    for sname, s in out["fixtures"].items():
        for a, m in s.items():
            print(f"fixtures {sname} {a:12s} legit {m['legitimate_released']}/{m['n']} unsafe {m['unsafe_released']} correct {m['pairs_correct']}  unsafe: {m['unsafe_released_ids']}  withheld: {m['legitimate_withheld_ids']}")


if __name__ == "__main__":
    stages = {"evidence": stage_evidence, "fit": stage_fit, "replay": stage_replay, "report": stage_report}
    for name in sys.argv[1:]:
        print("== stage", name, flush=True)
        stages[name]()
