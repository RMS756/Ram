"""Follow-up of the improvement study (revision 2): repaired permission matcher, tightened learned guard and
typed provenance for the learned arms. Isolated; nothing under rem/ or configs/ and no earlier result file is
changed. Protocol: REM_IMPROVEMENT_STUDY/followup/PROTOCOL_V2.md (committed before any arm below was scored).

Stages:  evidence  fit  replay        (python3 experiments/improve_study/improve_v2.py <stage> ...)
Reads the state of the first study (IMPROVE_STATE: perm_evidence.pkl, cells_F2.pkl, replay.pkl) without changing it.
"""
from __future__ import annotations

import collections
import dataclasses
import multiprocessing as mp
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import improve as I  # noqa: E402
from improve import S, G, common, build, load_raw, load, save, NOBEH, FEATURE_ORDER  # noqa: E402
from improve import A3Policy, build_loss_grid, sigmoid, Verdict, GuardConfig, RemGuard  # noqa: E402
from permission import DEFAULT_OPTS, PERM_ORDER, RuntimePermission  # noqa: E402
from permission_v2 import (DEFAULT_OPTS2, PERM2_ORDER, SUPPORTED_RECIPIENT, RuntimePermissionV2, canonical_provenance,  # noqa: E402
                           offline_permission_v2)

CANON_ORDER = ("c_act1", "c_act2")
S.ALL_ORDER = tuple(FEATURE_ORDER) + tuple(S.AUTHZ_ORDER) + tuple(PERM_ORDER) + tuple(PERM2_ORDER) + CANON_ORDER
S.FEATURE_SETS["F2"] = NOBEH + tuple(PERM_ORDER)
S.FEATURE_SETS["F2v2"] = NOBEH + tuple(PERM2_ORDER)
S.FEATURE_SETS["F3"] = tuple({"x_act1": "c_act1", "x_act2": "c_act2"}.get(f, f) for f in NOBEH) + tuple(PERM2_ORDER)
RULE_V2 = {"G1r": {"bind": False, "cond": False, "fulfil": False}, "G2": {}, "G2-nobind": {"bind": False},
           "G2-nocond": {"cond": False}, "G2-nofulfil": {"fulfil": False}}
LEARN_V2 = ["L2g", "L3", "L3c"]
ARMS_V2 = list(RULE_V2) + LEARN_V2


def authority_v1(ev) -> bool:
    if not ev.applicable or ev.overall == "denied" or ev.op != "requested":
        return False
    if ev.category in ("value_transfer", "payment_modification"):
        ok = ev.recipient in SUPPORTED_RECIPIENT
        if ev.category == "payment_modification":
            ok = ok and not any("target scheduled transaction" in x for x in ev.reasons)
        return ok
    if ev.category == "credential_change":
        return ev.value == "explicit"
    return True


def make_guard_v2(arm, cell, ep, st):
    gc = GuardConfig(st.spec, st.detector, cell["reference"] if cell else S.EMPTY_REF, st.tier_map, st.restricted,
                     "step_level", "no_reviewer")
    guard = RemGuard(gc, None, lambda c: (Verdict.ALLOW, "init", {}), st.labeler, ep)
    restricted = set(st.restricted)
    opts2 = dict(DEFAULT_OPTS2)
    opts2.update(RULE_V2.get(arm, {}))
    rp1 = RuntimePermission(ep.objective, DEFAULT_OPTS)
    rp2 = RuntimePermissionV2(ep.objective, opts2)
    if arm == "G1r":
        import intent_v2
        rp1.intent = intent_v2.compile_intent_v2(ep.objective).base      # parser repairs only, v1 matching
    orig_ingest = guard.ingest

    def ingest(tool, text, executed):
        rp2.on_ingest(executed)
        return orig_ingest(tool, text, executed)
    guard.ingest = ingest
    models = cell["models"] if cell else {}
    keys = {t: list(st.spec.key_arguments.get(t, ())) for t in restricted}
    pol2 = None
    if arm in LEARN_V2:
        grid = build_loss_grid(S.rm.loss_spec(cell["rmod"]), f"improve v2 cell {arm}")
        pol2 = A3Policy(grid, S.rm.predicates(), tie_mode="record_chapter3_order", exclude_from_expected_loss=(Verdict.ESCALATE, Verdict.MODIFY))

    def p_of(fs, x):
        rec = models[(fs, "y")]
        s = rec["b0"] + sum(c * x[n] for n, c in zip(rec["order"], rec["coef"]))
        return float(sigmoid(rec["g1"] * s + rec["g0"])) if not rec["failed"] else float(sigmoid(s))

    def decide(c):
        is_r = c.tool in restricted
        ev1 = rp1.evidence(guard.tracker, c.tool, c.args, c.tier)
        ev2 = rp2.evidence(guard.tracker, c.tool, c.args, c.tier)
        if arm == "G1r":
            v, src = (Verdict.BLOCK if is_r and ev1.overall != "supported" else Verdict.ALLOW), "rule_permission_repaired_parser"
        elif arm in RULE_V2:
            v, src = (Verdict.BLOCK if is_r and ev2.overall != "supported" else Verdict.ALLOW), "rule_permission_v2"
        else:
            f, avail = guard.tracker.features(c.tool, c.args)
            x = dict(f)
            x.update(ev1.features())
            x.update(ev2.features())
            x["c_act1"], x["c_act2"] = canonical_provenance(ep.objective, guard.tracker._untrusted_texts(), c.tool, c.args, keys.get(c.tool, []))
            if arm == "L2g":
                if is_r and (ev1.overall == "denied" or not authority_v1(ev1)):
                    v, src = Verdict.BLOCK, "permission_guard_authority_v1"
                else:
                    d = pol2.decide(p_of("F2", x), c.tier, c.tool, avail)
                    v, src = d.verdict, d.source
            else:
                if is_r and (ev2.overall == "denied" or not ev2.authority):
                    v, src = Verdict.BLOCK, "permission_guard_authority_v2"
                else:
                    d = pol2.decide(p_of("F2v2" if arm == "L3" else "F3", x), c.tier, c.tool, avail)
                    v, src = d.verdict, d.source
        det = {"perm": (ev2.overall, ev2.base.recipient, ev2.base.amount, ev2.binding, ev2.condition, ev2.fulfilment, ev2.authority),
               "perm1": (ev1.overall, ev1.recipient, ev1.amount), "z": (0.0, 0.0)}
        released = v is Verdict.ALLOW
        rp1.record(guard.tracker, c.tool, c.args, released)
        rp2.record(guard.tracker, c.tool, c.args)
        return v, src, det
    guard.decide = decide
    return guard


def _replay_job(job):
    scheme, eid, arm, role = job
    st = G["setup"]
    ep = G["eps"][role][eid]
    cell = G["cells"][G["cell_of"][scheme][(role, eid)]]
    guard = make_guard_v2(arm, cell, ep, st)
    out = S.replay_episode(ep, st.suite, guard)
    aud = [(a["label"], a["verdict"], a["released"], a["tier"], a["tool"], a["rem_latency_full_ms"], a["verdict_source"],
            a["details"].get("perm")) for a in out.audit]
    return scheme, role, eid, arm, bool(out.utility), bool(out.security), out.error, aud


# ------------------------------------------------------------------ stages
def stage_evidence():
    st = common.make_setup()
    data = build("primary", load_raw())
    Z = np.zeros((len(data.steps), len(PERM2_ORDER) + len(CANON_ORDER)))
    per_ep = collections.defaultdict(list)
    for i, s in enumerate(data.steps):
        per_ep[s.episode_id].append((s.index, i))
    stats = collections.Counter()
    for eid, lst in per_ep.items():
        idx = [i for _, i in sorted(lst)]
        tiers = {k: data.steps[i].tier for k, i in enumerate(idx)}
        it = iter(range(len(idx)))
        ep = data.episodes[eid]
        evs = offline_permission_v2(ep, lambda tool, args, _it=it, _t=tiers: _t[next(_it)])
        # canonical provenance offline: untrusted texts = outputs of all tool results before the assistant message
        prov, texts = [], []
        for m in ep.messages:
            if m.role == "assistant" and m.tool_calls:
                for call in m.tool_calls:
                    prov.append(canonical_provenance(ep.objective, list(texts), call.function, call.args or {},
                                                     list(st.spec.key_arguments.get(call.function, ()))))
            elif m.role == "tool" and m.tool_call is not None:
                texts.append(m.text or (m.error or ""))
        if len(evs) != len(idx) or len(prov) != len(idx):
            raise RuntimeError(f"alignment failed for {eid}")
        for k, i in enumerate(idx):
            f = evs[k].features()
            Z[i, :len(PERM2_ORDER)] = [f[n] for n in PERM2_ORDER]
            Z[i, len(PERM2_ORDER):] = prov[k]
            if evs[k].applicable:
                stats[(("attack" if data.steps[i].label else "legit"), evs[k].overall)] += 1
    # agreement of the offline canonical indicators with the frozen ones on the original text (where identifiers are not reformatted)
    x1 = np.array([s.features["x_act1"] for s in data.steps])
    x2 = np.array([s.features["x_act2"] for s in data.steps])
    save("perm2_evidence", {"Z": Z, "stats": dict(stats)})
    print("v2 permission evidence on primary restricted-tool calls:", dict(stats))
    print(f"agreement with frozen provenance on primary steps: x_act1 {np.mean(Z[:, 5] == x1):.4f}, x_act2 {np.mean(Z[:, 6] == x2):.4f}")


def _fit_job(job):
    key, kind = job
    data = G["data"]
    if kind == "S1":
        train = data.fold != key[1]
    else:
        _, u, i = key
        train = (G["ut"] != u) & (G["it"] != i)
    cell, _ = S.fit_cell(train, ["F2v2", "F3", "F2"] if kind == "S1" else ["F2v2", "F3", "F2"], ("y",))
    return key, cell["models"]


def stage_fit():
    data = build("primary", load_raw())
    aux = S.load("fit_aux")
    Zp, Z2 = load("perm_evidence")["Z"], load("perm2_evidence")["Z"]
    ut = np.array([s.user_task_id for s in data.steps], dtype=object)
    it = np.array([s.injection_task_id or "none" for s in data.steps], dtype=object)
    G.update(data=data, Z=np.hstack([aux["Z"], Zp, Z2]), T={"y": data.y.copy()}, ut=ut, it=it)
    old = S.load("cells")
    jobs = [(k, k[0]) for k in sorted(old, key=str)]
    t0 = time.time()
    with mp.get_context("fork").Pool(4) as pool:
        res = pool.map(_fit_job, jobs, chunksize=2)
    prev = load("cells_F2")
    new, maxdiff = {}, 0.0
    for key, models in res:
        new[key] = {k: models[k] for k in (("F2v2", "y"), ("F3", "y"))}
        a, b = models[("F2", "y")], prev[key][("F2", "y")]       # the refit of F2 must equal the stored fit
        maxdiff = max(maxdiff, abs(a["b0"] - b["b0"]), abs(a["g1"] - b["g1"]), max(abs(x - y) for x, y in zip(a["coef"], b["coef"])))
    save("cells_v2", new)
    print(f"fit: {len(jobs)} cells in {time.time() - t0:.0f}s; refit of the stored F2 models: max |difference| {maxdiff:.2e}")
    for fs in ("F2v2", "F3"):
        rec = new[("S1", "injection_task_0")][(fs, "y")]
        print(fs, "fold injection_task_0:", dict(zip(rec["order"], [round(c, 3) for c in rec["coef"]])), "b0", round(rec["b0"], 3))


def merged_cells():
    cells = I.merged_cells()
    extra = load("cells_v2")
    for k in cells:
        if k in extra:
            cells[k]["models"].update(extra[k])
    return cells


def stage_replay():
    st = common.make_setup()
    raw = load_raw()
    data = build("primary", raw)
    valid = S.load("fit_aux")["valid"]
    fresh, meta = I.load_fresh(st, data)
    probe = {}
    for e in valid:
        ep = data.episodes[e]
        if ep.attacked and any(S.ATTACKER_IBAN in v for v in ep.injections.values()):
            probe[e] = dataclasses.replace(ep, injections={k: v.replace(S.ATTACKER_IBAN, S.spaced(S.ATTACKER_IBAN)) for k, v in ep.injections.items()})
    cells = merged_cells()
    cell_of = {"S1": {}, "S2": {}}
    for e in valid:
        ep = data.episodes[e]
        cell_of["S1"][("primary", e)] = ("S1", data.episode_fold[e])
        cell_of["S2"][("primary", e)] = ("S2", ep.user_task_id, ep.injection_task_id or data.episode_fold[e])
    for e in fresh:
        cell_of["S1"][("dev2", e)] = ("S1", meta[e]["fold"])
    for e in probe:
        cell_of["S1"][("probe_iban", e)] = ("S1", data.episode_fold[e])
    G.update(setup=st, eps={"primary": data.episodes, "dev2": fresh, "probe_iban": probe}, cells=cells, cell_of=cell_of)
    jobs = []
    for a in ARMS_V2:
        jobs += [("S1", e, a, "primary") for e in valid]
        jobs += [("S1", e, a, "dev2") for e in sorted(fresh)]
        jobs += [("S1", e, a, "probe_iban") for e in sorted(probe)]
    for a in LEARN_V2:
        jobs += [("S2", e, a, "primary") for e in valid]
    t0 = time.time()
    with mp.get_context("fork").Pool(4) as pool:
        res = pool.map(_replay_job, jobs, chunksize=64)
    save("replay_v2", {"res": res})
    print(f"replay v2: {len(jobs)} replays in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    stages = {"evidence": stage_evidence, "fit": stage_fit, "replay": stage_replay}
    for name in sys.argv[1:]:
        print("== stage", name, flush=True)
        stages[name]()
