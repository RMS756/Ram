"""SIG-2: segment-level evaluation of REM-DiD's L2 sub-detectors (protocol 50_PROTOCOL_DID3.md §7, commit 8678add).

usage: python3 REM_DEFENSE_IN_DEPTH/code/sig2_detection.py  -> results/sig2_detection.json
"""
from __future__ import annotations

import collections
import itertools
import re
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import did3_common as D  # noqa: E402
from data import load_raw  # noqa: E402
from rem.integration.steps import injection_entered  # noqa: E402
from remdid.detection import DetectorSuite  # noqa: E402
from remdid.provenance import UNTRUSTED, segments_from_tool_output  # noqa: E402

NAMES = ["D_pattern", "D_role", "D_override", "D_fin"]


def zw(s: str) -> str:
    return "".join(ch + ("​" if (i % 3 == 2) else "") for i, ch in enumerate(s))


VARIANTS = {"original": lambda s: s, "paraphrase": D.paraphrase, "zero_width": zw, "upper": str.upper}


def metrics(gt, fire):
    gt, fire = np.asarray(gt, bool), np.asarray(fire, bool)
    tp, fp = int((gt & fire).sum()), int((~gt & fire).sum())
    fn, tn = int((gt & ~fire).sum()), int((~gt & ~fire).sum())
    d = lambda a, b: round(a / b, 4) if b else None  # noqa: E731
    return {"TP": tp, "FP": fp, "FN": fn, "TN": tn, "precision": d(tp, tp + fp), "recall": d(tp, tp + fn),
            "FPR": d(fp, fp + tn), "FNR": d(fn, tp + fn)}


def main():
    G = D.setup()
    st = G["setup"]
    f0 = sorted(G["refs"])[0]
    pattern = D.rm._guard_config(st, G["refs"][f0], "step_level", "no_reviewer").detector
    suite = DetectorSuite(pattern, budget_ms=1e9)
    raw = load_raw()
    rows = []
    fails = collections.Counter()
    lat = collections.defaultdict(list)
    for item in raw["episodes"]:
        role, ep = item["role"], item["episode"]
        if role not in ("primary", "cross_template"):
            continue
        tools = {}
        for m in ep.raw_messages:
            if m.get("role") == "assistant":
                for tc in (m.get("tool_calls") or []):
                    tools[tc.get("id")] = tc.get("function")
        for m in ep.raw_messages:
            if m.get("role") != "tool":
                continue
            text = m.get("content")
            if isinstance(text, list):
                text = " ".join(c.get("content", "") for c in text if isinstance(c, dict))
            tool = (m.get("tool_call") or {}).get("function") or tools.get(m.get("tool_call_id")) or "unknown"
            segs = [x for x in segments_from_tool_output(tool, text or "", 0) if x.source in UNTRUSTED]
            for sg in segs:
                gt = bool(injection_entered(sg.text, ep.injections))
                for var, fn in VARIANTS.items():
                    if var != "original" and not ep.injections:
                        continue
                    if var == "paraphrase" and ep.attack_type != "important_instructions":
                        continue
                    t = sg.text
                    if var != "original" and gt:
                        t2 = t
                        for v in ep.injections.values():
                            if not v:
                                continue
                            pat = re.compile(r"\s*".join(re.escape(w) for w in v.split()))
                            t2 = pat.sub(lambda m_, v_=v: fn(v_), t2)
                        if t2 == t:
                            fails[var] += 1
                            continue
                        t = t2
                    res = suite.run(t)
                    for r in res:
                        lat[r.name].append(r.latency_ms)
                    rows.append({"role": role, "template": ep.attack_type or "none", "variant": var, "tool": tool,
                                 "gt": gt, **{r.name: r.fired for r in res},
                                 "avail": all(r.available for r in res)})
    out = {"segments": len(rows), "by_variant": {}, "latency_ms": {}, "phi": {}, "legit_documents": {}}
    for var in VARIANTS:
        R = [r for r in rows if r["variant"] == var]
        if not R:
            continue
        gt = [r["gt"] for r in R]
        v = {"n": len(R), "positives": int(sum(gt)), "detectors": {n: metrics(gt, [r[n] for r in R]) for n in NAMES}}
        v["detectors"]["union"] = metrics(gt, [any(r[n] for n in NAMES) for r in R])
        v["detectors"]["union_without_pattern"] = metrics(gt, [any(r[n] for n in NAMES[1:]) for r in R])
        bt = {}
        for tpl in sorted({r["template"] for r in R if r["gt"]}):
            P = [r for r in R if r["gt"] and r["template"] == tpl]
            bt[tpl] = {"positives": len(P), **{n: round(sum(r[n] for r in P) / len(P), 4) for n in NAMES},
                       "union": round(sum(any(r[n] for n in NAMES) for r in P) / len(P), 4)}
        v["recall_by_template"] = bt
        out["by_variant"][var] = v
    R = [r for r in rows if r["variant"] == "original"]
    for a, b in itertools.combinations(NAMES, 2):
        x, y = np.array([r[a] for r in R], float), np.array([r[b] for r in R], float)
        out["phi"][f"{a}~{b}"] = None if x.std() == 0 or y.std() == 0 else round(float(np.corrcoef(x, y)[0, 1]), 4)
    L = [r for r in R if r["tool"] == "read_file" and not r["gt"]]
    out["legit_documents"] = {"n_segments": len(L), **{n: sum(r[n] for r in L) for n in NAMES},
                              "union": sum(any(r[n] for n in NAMES) for r in L)}
    for n, xs in lat.items():
        out["latency_ms"][n] = {"mean": round(float(np.mean(xs)), 4), "p95": round(float(np.percentile(xs, 95)), 4)}
    out["transform_failures"] = dict(fails)
    out["token_cost"] = 0
    out["all_available"] = all(r["avail"] for r in rows)
    p = os.path.join(D.REPO, "REM_DEFENSE_IN_DEPTH", "results", "sig2_detection.json")
    with open(p, "w") as fh:
        json.dump(out, fh, indent=1)
    for var, v in out["by_variant"].items():
        print(var, v["n"], v["positives"], {k: (m["recall"], m["FPR"]) for k, m in v["detectors"].items()})
    print("legit docs", out["legit_documents"])


if __name__ == "__main__":
    main()
