"""REM improvement study — development experiments (isolated; nothing under rem/ or configs/ is changed).

Status: [PROPOSED — NOT PART OF THE APPROVED REM DESIGN]. Protocol: REM_IMPROVEMENT_STUDY/protocol/.
All recordings used here were inspected in earlier studies: every result is DEVELOPMENT evidence.

Stages:  evidence  fit  replay  report        (python3 experiments/improve_study/improve.py <stage> ...)
Environment: PILOT_RESULTS_DIR, AUTHZ_STATE (state of the earlier studies, regenerable), IMPROVE_STATE,
             PROGENT_UPSTREAM (clone of github.com/sunblaze-ucb/progent).
"""
from __future__ import annotations

import collections
import dataclasses
import hashlib
import json
import multiprocessing as mp
import os
import sys
import time
from types import SimpleNamespace

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "experiments", "authz_study"))
sys.path.insert(0, HERE)

import study as S  # noqa: E402
from study import BOOT, CFG, G, SEED, common, grouped_bootstrap  # noqa: E402
from data import build, load_raw  # noqa: E402
from rem.algorithms.a3 import A3Policy  # noqa: E402
from rem.algorithms.behavior.evidence import FEATURE_GROUPS, FEATURE_ORDER  # noqa: E402
from rem.algorithms.decision.loss_matrix import build_loss_grid  # noqa: E402
from rem.algorithms.detection.ridge_logistic import sigmoid  # noqa: E402
from rem.core.results import Verdict  # noqa: E402
from rem.evaluation.crossfit import assign_round_robin  # noqa: E402
from rem.integration.agentdojo_replay import GuardConfig, RemGuard  # noqa: E402
from rem.integration.agentdojo_traces import ambiguous_pairs, iter_episode_paths, load_episode  # noqa: E402

import progent_manual as PG  # noqa: E402
from intent import canon_iban, compile_intent  # noqa: E402
from permission import DEFAULT_OPTS, PERM_ORDER, RuntimePermission, offline_permission  # noqa: E402

STATE = os.environ.get("IMPROVE_STATE") or os.path.join(common.RESULTS, "improve_state")
OUT = os.path.join(REPO, "REM_IMPROVEMENT_STUDY", "results")
KW = dict(resamples=BOOT["resamples"], seed=SEED, level=BOOT["interval"])
S.STATE_IMPROVE = STATE
S.ALL_ORDER = tuple(FEATURE_ORDER) + tuple(S.AUTHZ_ORDER) + tuple(PERM_ORDER)
NOBEH = tuple(f for f in FEATURE_ORDER if f not in FEATURE_GROUPS["beh"])
S.FEATURE_SETS["F2"] = NOBEH + tuple(PERM_ORDER)           # v1.1 evidence + permission evidence
FRESH = {   # the former confirmatory population; now development evidence
    "F-A": ("Meta-SecAlign-70B", ["important_instructions", "direct", "ignore_previous"], True),
    "F-B": ("Meta-SecAlign-70B-repeat_user_prompt", ["important_instructions", "direct", "ignore_previous"], True),
    "F-C": ("meta-llama_Llama-3.3-70B-Instruct-repeat_user_prompt", ["direct", "ignore_previous", "important_instructions"], True),
    "F-D": ("meta-llama_Llama-3.3-70B-Instruct", ["direct", "ignore_previous"], False),
    "F-E": ("gpt-4o-2024-05-13", ["important_instructions_no_model_name", "important_instructions_no_user_name",
                                  "important_instructions_wrong_model_name", "important_instructions_wrong_user_name"], False),
}
OLD_ARMS = ["B0", "B1", "M00", "M00_nobeh", "M01", "P2", "A2"]
RULE_NEW = ["PG", "A2n", "G1", "G1-noop", "G1-noamt", "G1-noest", "G1-nodel", "G1-nonorm"]
LEARN_NEW = ["V11d", "L0", "L1", "L2", "L2s"]
ALL_ARMS = OLD_ARMS + RULE_NEW + LEARN_NEW
ABL_OPTS = {"G1": {}, "G1-noop": {"op_check": False}, "G1-noamt": {"amount_check": False}, "G1-noest": {"established": False},
            "G1-nodel": {"delegation": False}, "G1-nonorm": {"typed_norm": False}}
_old_make_guard = S.make_guard


def save(name, obj):
    os.makedirs(STATE, exist_ok=True)
    import pickle
    with open(os.path.join(STATE, name + ".pkl"), "wb") as fh:
        pickle.dump(obj, fh, protocol=4)


def load(name):
    import pickle
    with open(os.path.join(STATE, name + ".pkl"), "rb") as fh:
        return pickle.load(fh)


def sha_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


# ------------------------------------------------------------------ arms
def make_guard(arm, cell, ep, st):
    if arm in OLD_ARMS:
        return _old_make_guard(arm, cell, ep, st)
    gc = GuardConfig(st.spec, st.detector, cell["reference"] if cell else S.EMPTY_REF, st.tier_map, st.restricted,
                     "step_level", "no_reviewer")
    guard = RemGuard(gc, None, lambda c: (Verdict.ALLOW, "init", {}), st.labeler, ep)
    restricted = set(st.restricted)
    opts = dict(DEFAULT_OPTS)
    opts.update(ABL_OPTS.get(arm, {}))
    rp = RuntimePermission(ep.objective, opts)
    rt = S.RuntimeAuthz(st.spec, st.restricted, S.read_tools(st), ep.objective)
    g_ibans = {i.canonical for i in rp.intent.ibans}
    models = cell["models"] if cell else {}
    preds = S.rm.predicates()
    pol4 = pol2 = None
    if arm in LEARN_NEW:
        grid = build_loss_grid(S.rm.loss_spec(cell["rmod"]), f"improve study cell {arm}")
        pol4 = A3Policy(grid, preds, tie_mode="record_chapter3_order")
        pol2 = A3Policy(grid, preds, tie_mode="record_chapter3_order", exclude_from_expected_loss=(Verdict.ESCALATE, Verdict.MODIFY))

    def p_of(fs, x):
        rec = models[(fs, "y")]
        s = rec["b0"] + sum(c * x[n] for n, c in zip(rec["order"], rec["coef"]))
        return float(sigmoid(rec["g1"] * s + rec["g0"])) if not rec["failed"] else float(sigmoid(s))

    def decide(c):
        is_r = c.tool in restricted
        det = {}
        ev = rp.evidence(guard.tracker, c.tool, c.args, c.tier)
        if arm == "PG":
            v, src = (Verdict.ALLOW if PG.allowed(c.tool, c.args) else Verdict.BLOCK), "progent_manual_policy"
        elif arm == "A2n":
            z = rt.evidence(guard.tracker, c.tool, c.args)
            r = canon_iban((c.args or {}).get("recipient")) if (c.args or {}).get("recipient") is not None else None
            ok = (r in g_ibans) if r is not None else (z[0] == 1.0)
            v, src = (Verdict.BLOCK if is_r and not ok else Verdict.ALLOW), "rule_explicit_typed"
        elif arm in ABL_OPTS:
            v, src = (Verdict.BLOCK if is_r and ev.overall != "supported" else Verdict.ALLOW), "rule_permission"
        else:
            f, avail = guard.tracker.features(c.tool, c.args)
            x = dict(f)
            x.update(ev.features())
            if arm == "V11d":
                d = pol2.decide(p_of("F0_nobeh", x), c.tier, c.tool, avail)
                v, src = d.verdict, d.source
            elif arm == "L0":
                d = pol2.decide(p_of("F2", x), c.tier, c.tool, avail)
                v, src = d.verdict, d.source
            elif is_r and ev.overall == "denied":
                v, src = Verdict.BLOCK, "permission_guard"
            elif arm == "L2s" and is_r and ev.overall == "supported":
                v, src = Verdict.ALLOW, "permission_supported"
            else:
                d = (pol4 if arm == "L1" else pol2).decide(p_of("F2", x), c.tier, c.tool, avail)
                v, src = d.verdict, d.source
        det["perm"] = (ev.overall, ev.recipient, ev.amount, ev.value, ev.op, ev.hard)
        det["z"] = (0.0, 0.0)
        released = v is Verdict.ALLOW
        rp.record(guard.tracker, c.tool, c.args, released)
        rt.record(guard.tracker, c.tool, c.args, released)
        return v, src, det
    guard.decide = decide
    return guard


S.make_guard = make_guard


def _replay_job(job):
    scheme, eid, arm, role = job
    st = G["setup"]
    ep = G["eps"][role][eid]
    cell = G["cells"][G["cell_of"][scheme][(role, eid)]]
    guard = make_guard(arm, cell, ep, st)
    out = S.replay_episode(ep, st.suite, guard)
    aud = [(a["label"], a["verdict"], a["released"], a["tier"], a["tool"], a["rem_latency_full_ms"], a["verdict_source"],
            a["details"].get("perm")) for a in out.audit]
    return scheme, role, eid, arm, bool(out.utility), bool(out.security), out.error, aud


# ------------------------------------------------------------------ data
def load_fresh(st, data):
    folds = sorted(set(data.fold.tolist()), key=str)
    users = sorted({e.user_task_id for e in data.episodes.values()}, key=str)
    rr = assign_round_robin(users, len(folds))
    amb = ambiguous_pairs(st.labeler)
    eps, meta = {}, {}
    for src, (pipe, attacks, benign) in FRESH.items():
        for attack in attacks + (["none"] if benign else []):
            for path in iter_episode_paths(common.RUNS, pipe, CFG["data"]["suite"], attack):
                ep = load_episode(path, pipeline=pipe)
                if ep.error and CFG["data"]["exclude_errored_episodes"]:
                    continue
                if ep.injection_task_id and ((ep.user_task_id, ep.injection_task_id) in amb or ep.injection_task_id not in folds):
                    continue
                if ep.user_task_id not in rr:
                    continue
                eid = f"{src}|{ep.episode_id}"
                eps[eid] = ep
                meta[eid] = {"source": src, "fold": ep.injection_task_id or folds[rr[ep.user_task_id]], "attacked": ep.attacked,
                             "user_task": ep.user_task_id, "injection_task": ep.injection_task_id}
    return eps, meta


def perm_matrix(data, st, opts=DEFAULT_OPTS):
    Z = np.zeros((len(data.steps), len(PERM_ORDER)))
    per_ep = collections.defaultdict(list)
    for i, s in enumerate(data.steps):
        per_ep[s.episode_id].append((s.index, i))
    stats = collections.Counter()
    for eid, lst in per_ep.items():
        idx = [i for _, i in sorted(lst)]
        tiers = {k: data.steps[i].tier for k, i in enumerate(idx)}
        calls = iter(range(len(idx)))
        evs = offline_permission(data.episodes[eid], lambda tool, args, _it=calls, _t=tiers: _t[next(_it)], opts)
        if len(evs) != len(idx):
            raise RuntimeError(f"permission alignment failed for {eid}: {len(evs)} vs {len(idx)}")
        for k, i in enumerate(idx):
            f = evs[k].features()
            Z[i] = [f[n] for n in PERM_ORDER]
            if evs[k].applicable:
                stats[(("attack" if data.steps[i].label else ("legit_benign_ep" if not data.steps[i].injection_task_id else "legit_attacked_ep")), evs[k].overall)] += 1
    return Z, stats


def stage_evidence():
    st = common.make_setup()
    data = build("primary", load_raw())
    Z, stats = perm_matrix(data, st)
    save("perm_evidence", {"Z": Z, "stats": dict(stats)})
    print("permission evidence on primary steps (restricted-tool calls):")
    for k in sorted(stats):
        print("  ", k, stats[k])


def _fit_job(job):
    key, kind = job
    data = G["data"]
    if kind == "S1":
        train = data.fold != key[1]
    else:
        _, u, i = key
        train = (G["ut"] != u) & (G["it"] != i)
    fsets = ["F2", "F0_nobeh"] if kind == "S1" else ["F2"]
    cell, _ = S.fit_cell(train, fsets, ("y",))
    return key, cell["models"]


def stage_fit():
    st = common.make_setup()
    data = build("primary", load_raw())
    aux = S.load("fit_aux")
    Zp = load("perm_evidence")["Z"]
    ut = np.array([s.user_task_id for s in data.steps], dtype=object)
    it = np.array([s.injection_task_id or "none" for s in data.steps], dtype=object)
    G.update(data=data, Z=np.hstack([aux["Z"], Zp]), T={"y": data.y.copy()}, ut=ut, it=it)
    old = S.load("cells")
    jobs = [(k, k[0]) for k in sorted(old, key=str)]
    t0 = time.time()
    with mp.get_context("fork").Pool(4) as pool:
        res = pool.map(_fit_job, jobs, chunksize=2)
    extra = S.load("cells_posthoc_a2")
    new, maxdiff = {}, 0.0
    for key, models in res:
        new[key] = {("F2", "y"): models[("F2", "y")]}
        if key[0] == "S1":                              # frozen-path equivalence: refit of the v1.1 fit must equal the stored one
            a, b = models[("F0_nobeh", "y")], extra[key]["models"][("F0_nobeh", "y")]
            maxdiff = max(maxdiff, abs(a["b0"] - b["b0"]), abs(a["g0"] - b["g0"]), abs(a["g1"] - b["g1"]),
                          max(abs(x - y) for x, y in zip(a["coef"], b["coef"])))
    save("cells_F2", new)
    print(f"fit: {len(jobs)} cells in {time.time() - t0:.0f}s; max |difference| of the refitted v1.1 fits from the stored ones: {maxdiff:.2e}")
    rec = new[("S1", "injection_task_0")][("F2", "y")]
    print("fold injection_task_0 F2 coefficients:", dict(zip(rec["order"], [round(c, 3) for c in rec["coef"]])), "b0", round(rec["b0"], 3), "lam", rec["lam"])


def merged_cells():
    cells = S.load("cells")
    for name, loader in (("cells_posthoc_a2", S.load), ("cells_F2", load)):
        extra = loader(name)
        for k in cells:
            if k in extra:
                cells[k]["models"].update(extra[k]["models"] if "models" in extra[k] else extra[k])
    return cells


def stage_replay():
    st = common.make_setup()
    PG.load()
    raw = load_raw()
    data = build("primary", raw)
    valid = S.load("fit_aux")["valid"]
    fresh, meta = load_fresh(st, data)
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
    for a in ALL_ARMS:
        jobs += [("S1", e, a, "primary") for e in valid]
        jobs += [("S1", e, a, "dev2") for e in sorted(fresh)]
    for a in LEARN_NEW + ["M00", "M00_nobeh"]:
        jobs += [("S2", e, a, "primary") for e in valid]
    for a in ["B0", "B1", "M00", "M00_nobeh", "P2", "A2", "PG", "A2n", "G1", "G1-nonorm", "L2"]:
        jobs += [("S1", e, a, "probe_iban") for e in sorted(probe)]
    t0 = time.time()
    with mp.get_context("fork").Pool(4) as pool:
        res = pool.map(_replay_job, jobs, chunksize=64)
    save("replay", {"res": res, "meta": meta, "valid": valid,
                    "recorded_fresh": {e: (bool(ep.utility), bool(ep.security)) for e, ep in fresh.items()}})
    print(f"replay: {len(jobs)} replays in {time.time() - t0:.0f}s; primary {len(valid)}, dev2 {len(fresh)}, probe {len(probe)}")


if __name__ == "__main__":
    stages = {"evidence": stage_evidence, "fit": stage_fit, "replay": stage_replay}
    for name in sys.argv[1:]:
        if name == "report":
            import report
            report.main()
        else:
            print("== stage", name, flush=True)
            stages[name]()
