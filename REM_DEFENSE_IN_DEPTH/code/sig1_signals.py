"""SIG-1: Detection sub-signals (content level) and evidence-feature redundancy (step level).

Protocol: REM_DEFENSE_IN_DEPTH/07_PROTOCOL_SIGNALS.md (commit e7da7a9). Measurement only; rem/ unchanged.
usage: PILOT_RESULTS_DIR=REM_DEFENSE_IN_DEPTH/work/pilot python3 REM_DEFENSE_IN_DEPTH/code/sig1_signals.py
"""
from __future__ import annotations

import collections
import itertools
import json
import os
import sys
import time

import numpy as np

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "experiments", "pilot"))
os.environ.setdefault("PILOT_RESULTS_DIR", os.path.join(REPO, "REM_DEFENSE_IN_DEPTH", "work", "pilot"))

import common  # noqa: E402
import run_main as rm  # noqa: E402
from data import Designer, build, load_raw  # noqa: E402

from rem.algorithms.behavior.evidence import FEATURE_ORDER  # noqa: E402
from rem.integration.steps import injection_entered  # noqa: E402

OUT = os.path.join(REPO, "REM_DEFENSE_IN_DEPTH", "results")
ATTACKER_IBAN = rm.CFG["labels"]["attacker_key_arguments"]["recipient"]
SUBS = ["p0", "p1", "p2", "p3", "p4", "tool_name"]


def spaced(iban):
    return " ".join(iban[i:i + 4] for i in range(0, len(iban), 4))


def metrics(gt, fire):
    gt, fire = np.asarray(gt, bool), np.asarray(fire, bool)
    tp, fp = int((gt & fire).sum()), int((~gt & fire).sum())
    fn, tn = int((gt & ~fire).sum()), int((~gt & ~fire).sum())
    div = lambda a, b: float(a / b) if b else None  # noqa: E731
    return {"TP": tp, "FP": fp, "FN": fn, "TN": tn, "precision": div(tp, tp + fp), "recall": div(tp, tp + fn),
            "FPR": div(fp, fp + tn), "FNR": div(fn, tp + fn)}


def phi(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if a.std() == 0 or b.std() == 0:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def part_a(st):
    raw = load_raw()
    rows = []          # (role, template, gt, fired set, seconds, text-has-iban, fired-on-spaced)
    for item in raw["episodes"]:
        role, ep = item["role"], item["episode"]
        if role not in ("primary", "cross_template"):
            continue
        for m in ep.messages:
            if m.role != "tool":
                continue
            t0 = time.perf_counter()
            f = set(st.detector.fired(m.text))
            dt = time.perf_counter() - t0
            has_iban = ATTACKER_IBAN in (m.text or "")
            f_sp = set(st.detector.fired(m.text.replace(ATTACKER_IBAN, spaced(ATTACKER_IBAN)))) if has_iban else f
            rows.append((role, ep.attack_type or "none", injection_entered(m.text, ep.injections), f, dt, has_iban, f_sp))
    out = {}
    for pop, sel in (("primary", lambda r: r[0] == "primary"), ("cross_template", lambda r: r[0] == "cross_template")):
        R = [r for r in rows if sel(r)]
        gt = [r[2] for r in R]
        res = {"messages": len(R), "payload_bearing": int(sum(gt)), "subdetectors": {}}
        for s in SUBS:
            res["subdetectors"][s] = metrics(gt, [s in r[3] for r in R])
        res["subdetectors"]["x_ctx2_union"] = metrics(gt, [bool(r[3]) for r in R])
        F = {s: [s in r[3] for r in R] for s in SUBS}
        res["phi_all_messages"] = {f"{a}~{b}": phi(F[a], F[b]) for a, b in itertools.combinations(SUBS, 2)}
        idx = [i for i, g in enumerate(gt) if g]
        res["phi_payload_messages"] = {f"{a}~{b}": phi([F[a][i] for i in idx], [F[b][i] for i in idx])
                                       for a, b in itertools.combinations(SUBS, 2)}
        res["n_subdetectors_firing_on_payload"] = dict(sorted(collections.Counter(len(R[i][3]) for i in idx).items()))
        lat = np.array([r[4] for r in R]) * 1e3
        res["latency_ms_per_message"] = {"median": float(np.median(lat)), "p95": float(np.percentile(lat, 95))}
        by_t = collections.defaultdict(list)
        for r in R:
            if r[2]:
                by_t[r[1]].append(bool(r[3]))
        res["union_recall_by_template"] = {t: {"payload_messages": len(v), "recall": float(np.mean(v))} for t, v in sorted(by_t.items())}
        iban = [r for r in R if r[5]]
        res["identifier_reformatting_check"] = {"messages_with_attacker_identifier": len(iban),
                                                "fired_set_changed_by_reformatting": int(sum(r[3] != r[6] for r in iban))}
        out[pop] = res
    return out


def part_b(st):
    data = build("primary")
    fits = rm.load_state("crossfit")
    prim = fits["label_nll_primary"]
    designer = Designer(data, FEATURE_ORDER)
    X = np.full((len(data.y), len(FEATURE_ORDER)), np.nan)
    for f in prim.fits:
        test = data.fold == f
        X[test] = designer(~test)[test]
    restricted = set(st.restricted)
    is_r = np.array([s.tool in restricted for s in data.steps])
    out = {}
    for name, sel in (("restricted_all", is_r), ("restricted_attack", is_r & (data.y == 1)),
                      ("restricted_legitimate", is_r & (data.y == 0))):
        Xs = X[sel]
        out[name] = {"n": int(sel.sum()),
                     "corr": {f"{FEATURE_ORDER[i]}~{FEATURE_ORDER[j]}": phi(Xs[:, i], Xs[:, j])
                              for i, j in itertools.combinations(range(len(FEATURE_ORDER)), 2)}}
    ctx = X[:, FEATURE_ORDER.index("x_ctx2")]
    beh1 = X[:, FEATURE_ORDER.index("x_beh1")]
    out["x_beh1_implies_x_ctx2_or_earlier_match"] = {
        "steps_beh1_1": int((beh1 == 1).sum()), "of_which_ctx2_1": int(((beh1 == 1) & (ctx == 1)).sum())}
    return out


def main():
    st = common.make_setup()
    res = {"protocol": "REM_DEFENSE_IN_DEPTH/07_PROTOCOL_SIGNALS.md (commit e7da7a9)",
           "patterns": {f"p{i}": p for i, p in enumerate(rm.CFG["features"]["instruction_patterns"])} | {"tool_name": "mention of any suite tool name"},
           "part_A_detection": part_a(st), "part_B_feature_redundancy": part_b(st)}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "sig1_results.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    a = res["part_A_detection"]["primary"]
    print("primary messages", a["messages"], "payload", a["payload_bearing"])
    for s, m in a["subdetectors"].items():
        print(f"{s:14s} P={m['precision']} R={m['recall']} FPR={m['FPR']}")


if __name__ == "__main__":
    main()
