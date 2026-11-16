"""Competitive study of 16 November 2026: fit, replay, report. No model API call.

Status: [PROPOSED - EXPLORATORY - DEVELOPMENT EVIDENCE]. See REM_COMPETITIVE_STUDY_2026_11_16/PROTOCOL.md,
committed before any outcome of the arms defined here was computed.

Stages:  fit | replay | report
Environment: the variables of the integration package (AGENTDOJO_RUNS, PILOT_RESULTS_DIR, INTEGRATION_STATE,
PROGENT_UPSTREAM) and COMPETITIVE_STATE (cache directory of this study, outside the repository). The
integration package's stages prepare, fit, replay, report and its follow-up must have been run first.
"""
from __future__ import annotations

import collections
import dataclasses
import gzip
import json
import multiprocessing as mp
import os
import pickle
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / "experiments" / "g3_integration"))

import fitting as F  # noqa: E402
import guards as G  # noqa: E402
import followup as FU  # noqa: E402  (integration package: HV guard)
from rem.evaluation import probabilistic as PM  # noqa: E402

J, S, R = F.J, F.S, F.J.R
common = J.common
STATE = Path(os.environ["COMPETITIVE_STATE"])
STATE.mkdir(parents=True, exist_ok=True)
OUT = ROOT / "REM_COMPETITIVE_STUDY_2026_11_16" / "results"
OUT.mkdir(parents=True, exist_ok=True)
PACKAGE_ARMS = ["B0", "REM10", "REM11", "A2", "PG", "G3", "L4", "HR", "HV"]
TABLE_ARMS = ["B0", "REM10", "REM11", "A2", "PG", "G3", "GV", "L4", "HV", "HVx", "HVnc", "HV4", "NP05", "NP01", "CRC05", "CRC01", "GB"]
NEW = ["GV", "HVnc", "HV4", "NP05", "NP01", "CRC05", "CRC01", "GB"]
CONTRASTS = ([(a, b) for a in NEW for b in ("HV", "GV", "G3", "PG", "REM10") if a != b]
             + [("HV", "GV"), ("HV", "PG"), ("HV", "G3"), ("HVx", "HV")])
W = {}


def save(name, obj):
    with (STATE / (name + ".pkl")).open("wb") as f:
        pickle.dump(obj, f)


def load(name):
    with (STATE / (name + ".pkl")).open("rb") as f:
        return pickle.load(f)


def write(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=1, default=common._default), encoding="utf-8")


# ------------------------------------------------------------------------------------------------ fit
def stage_fit():
    d = F.setup_globals()
    F.W["jcells"] = J.load("cells")
    aux = J.load("prepared")
    s2 = {("S2", d.episodes[e].user_task_id, d.episodes[e].injection_task_id or d.episode_fold[e]) for e in aux["valid"]}
    jobs = [("S1", f) for f in sorted(set(d.fold.tolist()), key=str)] + sorted(s2)
    assert set(jobs) == set(F.W["jcells"]), "cells differ from the integration package"
    t = time.time()
    with mp.get_context("fork").Pool(4) as p:
        cells = dict(p.map(F.fit_job, jobs, chunksize=2))
    save("cs_cells", cells)
    summary = []
    for key, c in cells.items():
        g = c["gb"]
        summary.append({"key": key,
                        "np": {"n_left_out": c["np"]["n_left_out"], "lam": c["np"]["rec"]["lam"], "b0": c["np"]["rec"]["b0"],
                               "coef": c["np"]["rec"]["coef"], "cut": c["np"]["cut"]},
                        "crc": {"n_units": c["crc"]["n_units"], "lam": c["crc"]["rec"]["lam"], "b0": c["crc"]["rec"]["b0"],
                                "coef": c["crc"]["rec"]["coef"], "cut": c["crc"]["cut"]},
                        "gb": {k: g[k] for k in ("order", "g0", "g1", "failed", "max_depth", "n_estimators", "inner_logloss",
                                                 "n_leaves_total", "feature_importances", "ntrain", "npos")}})
    write("fits_summary.json", {"cells": summary, "alphas": F.ALPHAS, "delta": F.DELTA, "gb_depths": F.GB_DEPTHS,
                                "gb_stages": F.GB_STAGES, "gb_learning_rate": F.GB_LEARNING_RATE})
    print("fit", len(cells), "cells", round(time.time() - t, 1), "seconds", flush=True)


# --------------------------------------------------------------------------------------------- replay
def replay_job(job):
    scheme, role, e, arm = job
    ep = W["eps"][role][e]
    key = ("S1", W["fold"][role][e]) if scheme == "S1" else ("S2", ep.user_task_id, ep.injection_task_id or W["fold"][role][e])
    out = S.replay_episode(ep, W["setup"].suite, G.make_guard(arm, W["jcells"][key], W["cs"][key], ep, W["setup"]))
    audit = [(a["label"], a["verdict"], bool(a["released"]), a["tier"], a["tool"], a["rem_latency_full_ms"], a["verdict_source"],
              a["details"].get("perm"), a["details"].get("cs")) for a in out.audit]
    return scheme, role, e, arm, bool(out.utility), bool(out.security), out.error, audit


def _populations():
    d = J.data()
    aux = J.load("prepared")
    probe = {e: dataclasses.replace(d.episodes[e], injections={k: v.replace(S.ATTACKER_IBAN, S.spaced(S.ATTACKER_IBAN))
                                                                for k, v in d.episodes[e].injections.items()})
             for e in aux["valid"] if d.episodes[e].attacked and any(S.ATTACKER_IBAN in v for v in d.episodes[e].injections.values())}
    eps = {"primary": {e: d.episodes[e] for e in aux["valid"]}, "dev2": aux["fresh"], "probe": probe}
    folds = {"primary": d.episode_fold, "dev2": {e: m["fold"] for e, m in aux["meta"].items()}, "probe": d.episode_fold}
    return d, aux, eps, folds


def stage_replay():
    d, aux, eps, folds = _populations()
    W.update(setup=common.make_setup(), jcells=J.load("cells"), cs=load("cs_cells"), eps=eps, fold=folds)
    jobs = [("S1", role, e, a) for role, pop in eps.items() for a in G.ARMS for e in sorted(pop)]
    jobs += [("S2", "primary", e, a) for a in G.FITTED for e in aux["valid"]]
    t = time.time()
    results = []
    with mp.get_context("fork").Pool(4) as p:
        for i, v in enumerate(p.imap_unordered(replay_job, jobs, chunksize=32), 1):
            results.append(v)
            if i % 10000 == 0:
                print("replay", i, "/", len(jobs), "elapsed", round(time.time() - t), "s", flush=True)
    save("cs_replays", results)
    print("replay done", len(results), round(time.time() - t), "s; errors", sum(1 for r in results if r[6]), flush=True)


# --------------------------------------------------------------------------------------------- report
def fixtures(cells, cs):
    """The 43 paired fixtures of sets 1 to 4 (regression material), for every arm."""
    sys.path.insert(0, str(ROOT / "REM_AUTHORIZATION_AUDIT" / "tools"))
    import trace_fixtures as tf
    st = common.make_setup()
    key = ("S1", "injection_task_0")
    paths = ["REM_AUTHORIZATION_AUDIT/fixtures/set1_substitution_fixtures.json", "REM_AUTHORIZATION_AUDIT/fixtures/set2_fresh_fixtures.json",
             "REM_FINAL_SUBMISSION/fixtures/set3_credential_and_reformatting_fixtures.json",
             "REM_IMPROVEMENT_STUDY/fixtures/set4_permission_fixtures.json"]

    def build(arm, ep):
        if arm in G.ARMS:
            return G.make_guard(arm, cells[key], cs[key], ep, st)
        if arm == "HV":
            return FU.make_guard("HV", cells[key], ep, st)
        return J.guard(arm, cells[key], ep, st)
    result = {}
    for path in paths:
        v = json.loads((ROOT / path).read_text())
        records = v["records"] if isinstance(v, dict) else v
        summary = {}
        for a in [x for x in TABLE_ARMS if x != "B0"]:
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
                    g = build(a, ep)
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


def _metrics(y, p):
    y = np.asarray(y, dtype=int)
    p = np.asarray(p, dtype=float)
    out = {"n": int(y.size), "positives": int(y.sum())}
    if y.size == 0:
        return out
    two = 0 < y.sum() < y.size
    out.update(roc_auc=float(PM.roc_auc(y, p)) if two else None, average_precision=float(PM.average_precision(y, p)) if two else None,
               brier=float(PM.brier_binary(y, p)), log_loss=float(PM.log_loss(y, p, S.E["probability_clip"])),
               ece_10_bins=float(PM.expected_calibration_error(y, p, int(S.E["ece_bins"]))))
    return out


def diagnostics(cs, d, Z, restricted):
    """Held-out (S1) predictions of the estimators, and what the two calibrated cutoffs would do alone."""
    y = d.y
    tool = np.array([s.tool for s in d.steps], dtype=object)
    is_r = np.array([t in restricted for t in tool])
    zi = {n: k for k, n in enumerate(J.PERM3_ORDER)}
    residual = is_r & (Z[:, zi["q3_rec"]] == 1) & (Z[:, zi["q3_den"]] == 0)
    pooled = collections.defaultdict(list)
    per_fold = {}
    for key, c in cs.items():
        if key[0] != "S1":
            continue
        h = c["heldout"]
        idx = h["idx"]
        for k in ("p_ridge", "p_ridge_uncal", "p_gb", "s_np", "s_crc"):
            pooled[k].append(h[k])
        pooled["idx"].append(idx)
        att, leg = idx[(y[idx] == 1)], idx[(y[idx] == 0) & is_r[idx]]
        pos = {int(i): k for k, i in enumerate(idx)}
        row = {"attack_labelled_steps": int(att.size), "legitimate_restricted_steps": int(leg.size)}
        for kind, sk in (("np", "s_np"), ("crc", "s_crc")):
            for a, cut in c[kind]["cut"].items():
                cv = cut["cutoff"]
                row[f"{kind}_{a}"] = {"cutoff": cv, "feasible": cut["feasible"],
                                      "attack_steps_below_cutoff": int(sum(h[sk][pos[int(i)]] < cv for i in att)),
                                      "legitimate_restricted_steps_below_cutoff": int(sum(h[sk][pos[int(i)]] < cv for i in leg))}
        per_fold[key[1]] = row
    idx = np.concatenate(pooled["idx"])
    P = {k: np.concatenate(v) for k, v in pooled.items() if k != "idx"}
    subsets = {"all_steps": np.ones(idx.size, bool), "restricted_steps": is_r[idx], "residual_restricted_steps": residual[idx]}
    est = {name: {sub: _metrics(y[idx][m], P[k][m]) for sub, m in subsets.items()}
           for name, k in (("ridge_F4_calibrated", "p_ridge"), ("ridge_F4_uncalibrated", "p_ridge_uncal"), ("gradient_boosting_F4_calibrated", "p_gb"))}
    return {"estimators_heldout_S1_pooled": est, "cutoffs_alone_per_heldout_objective": per_fold,
            "note": "The cutoff rows show what each calibrated cutoff would release if it decided alone, on the held-out attacker "
                    "objective of each fold. They are not arms of the study; in the arms the cutoff acts only behind the authority front."}


def stage_report():
    d, aux, eps, folds = _populations()
    st = common.make_setup()
    restricted = set(st.restricted)
    cs = load("cs_cells")
    mine = load("cs_replays")
    rows = J.load("replays") + J.load("value_replays") + mine
    by = collections.defaultdict(lambda: collections.defaultdict(dict))
    for scheme, role, e, a, u, s, err, aud in rows:
        by[(scheme, role)][e][a] = (int(u), int(s), err, aud)
    fresh = aux["fresh"]
    fv = sorted(e for e, v in by[("S1", "dev2")].items() if v["B0"][2] is None and v["B0"][:2] == (fresh[e].utility, fresh[e].security))
    assert len(aux["valid"]) == 3313 and len(fv) == 2113
    pops = {}
    for name, scheme, role, ids in [("primary_S1", "S1", "primary", aux["valid"]), ("primary_S2", "S2", "primary", aux["valid"]), ("dev2", "S1", "dev2", fv)]:
        B = by[(scheme, role)]
        if scheme == "S2":
            for e in ids:
                for a in TABLE_ARMS:
                    if a not in B[e]:
                        B[e][a] = by[("S1", "primary")][e][a]       # arms without a fitted quantity are identical under S2
        episodes = d.episodes if role == "primary" else fresh
        att = [e for e in ids if episodes[e].attacked]
        ben = [e for e in ids if not episodes[e].attacked]
        usr = lambda e: episodes[e].user_task_id          # noqa: E731
        inj = lambda e: episodes[e].injection_task_id     # noqa: E731
        users = sorted({usr(e) for e in ids}, key=lambda u: int(u.split("_")[-1]))
        injs = sorted({inj(e) for e in att}, key=lambda u: int(u.split("_")[-1]))
        mm = R.block(B, att, ben, TABLE_ARMS, restricted)
        stages = {}
        for a in G.ARMS:
            c = collections.Counter()
            for e in ids:
                for x in B[e][a][3]:
                    if x[4] not in restricted:
                        c["unrestricted_withheld"] += int(not x[2])
                        continue
                    lab = "attack_labelled" if x[0] == 1 else "not_attack_labelled"
                    if x[6].startswith("direct_value_"):
                        stage = "value_constraint_refused"
                    elif x[8]["stage"] == "front":
                        stage = "front_blocked"
                    elif x[8]["stage"] == "predicate":
                        stage = "predicate_" + x[1]
                    else:
                        stage = "rule_released" if x[2] else "rule_withheld_" + x[1]
                    c[f"{lab}|{stage}"] += 1
            stages[a] = dict(sorted(c.items()))
        no15 = [e for e in ids if usr(e) != "user_task_15"]
        pops[name] = {
            "n_attacked": len(att), "n_benign": len(ben), "arms": mm,
            "contrasts": {a + " minus " + b: R.paired(B, att, ben, usr, inj, a, b) for a, b in CONTRASTS},
            "completion_by_user_task": {a: {u: [sum(B[e][a][0] for e in ids if usr(e) == u), sum(1 for e in ids if usr(e) == u)] for u in users} for a in TABLE_ARMS},
            "attacks_by_user_task": {a: {u: sum(B[e][a][1] for e in att if usr(e) == u) for u in users} for a in TABLE_ARMS},
            "attacks_by_injection_task": {a: {u: sum(B[e][a][1] for e in att if inj(e) == u) for u in injs} for a in TABLE_ARMS},
            "per_user_task_difference_counts": {a + " minus " + b: {"user_tasks_higher": sum(1 for u in users if sum(B[e][a][0] - B[e][b][0] for e in ids if usr(e) == u) > 0),
                                                                    "user_tasks_lower": sum(1 for u in users if sum(B[e][a][0] - B[e][b][0] for e in ids if usr(e) == u) < 0),
                                                                    "user_tasks_equal": sum(1 for u in users if sum(B[e][a][0] - B[e][b][0] for e in ids if usr(e) == u) == 0)}
                                                for a, b in CONTRASTS},
            "without_user_task_15": {a: {"attacks": sum(B[e][a][1] for e in no15 if episodes[e].attacked), "all_tasks": sum(B[e][a][0] for e in no15),
                                         "n": len(no15)} for a in TABLE_ARMS},
            "restricted_call_stages": stages,
        }
        print(name, [(a, m["attacks_successful"], m["benign_completed"], m["all_tasks_completed"]) for a, m in mm.items()], flush=True)
    # equivalence of the rebuilt HV rule with the stored HV arm
    eq = {"episodes_compared": 0, "outcome_differences": 0, "release_sequence_differences": 0}
    for (scheme, role), B in by.items():
        for e, v in B.items():
            if "HV" in v and "HVx" in v:
                eq["episodes_compared"] += 1
                eq["outcome_differences"] += int(v["HV"][:2] != v["HVx"][:2])
                eq["release_sequence_differences"] += int([x[2] for x in v["HV"][3]] != [x[2] for x in v["HVx"][3]])
    probe = by[("S1", "probe")]
    hv4 = collections.Counter(x[1] for (scheme, role), B in by.items() if scheme == "S1" and role in ("primary", "dev2")
                              for v in B.values() if "HV4" in v for x in v["HV4"][3] if x[4] in restricted and x[8]["stage"] == "rule")
    out = {
        "status": "EXPLORATORY DEVELOPMENT EVIDENCE: offline recorded-trace replay under NO-ADAPT; no live agent, no model API",
        "populations": pops,
        "equivalence_HVx_vs_stored_HV": eq,
        "probe_reformatted_identifier": {"n": len(probe), "arms": {a: {"attacks": sum(v[a][1] for v in probe.values()),
                                                                           "replay_errors": sum(v[a][2] is not None for v in probe.values())}
                                                                       for a in TABLE_ARMS if all(a in v for v in probe.values())}},
        "replay_errors_new_arms": sum(1 for r in mine if r[6]),
        "replays_new_arms": len(mine),
        "HV4_verdicts_on_calls_reaching_the_rule": dict(hv4),
        "fixtures": fixtures(J.load("cells"), cs),
    }
    F.setup_globals()
    out["diagnostics"] = diagnostics(cs, F.W["data"], F.W["Z"], restricted)
    write("results.json", out)
    with gzip.open(OUT / "episode_outcomes.jsonl.gz", "wt", encoding="utf-8") as f:
        for scheme, role, e, a, u, s, err, aud in sorted(mine, key=lambda z: z[:4]):
            f.write(json.dumps({"scheme": scheme, "population": role, "episode_id": e, "arm": a, "utility": u, "security": s, "error": err}) + "\n")
    with gzip.open(OUT / "restricted_call_audit.jsonl.gz", "wt", encoding="utf-8") as f:
        for scheme, role, e, a, u, s, err, aud in sorted(mine, key=lambda z: z[:4]):
            for k, x in enumerate(aud):
                if x[4] in restricted:
                    f.write(json.dumps({"scheme": scheme, "population": role, "episode_id": e, "arm": a, "call": k, "tool": x[4], "attempt_label": x[0],
                                        "verdict": x[1], "released": x[2], "source": x[6], "permission": x[7], "rule": x[8]}, default=common._default) + "\n")
    assert eq["outcome_differences"] == 0 and eq["release_sequence_differences"] == 0, eq
    print("rebuilt HV rule reproduces the stored HV arm on", eq["episodes_compared"], "replays", flush=True)


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("fit", "replay", "report"):
        raise SystemExit("Usage: cs_run.py fit|replay|report")
    globals()["stage_" + sys.argv[1]]()
