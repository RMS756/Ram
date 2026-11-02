"""Independent recomputation of headline results from the reproduction state (read-only).

Usage: PILOT_RESULTS_DIR=<reproduction dir> python3 CODE_AUDIT_R4/audit_checks/audit_results.py
Compares independently computed values with (a) the reproduced JSON and (b) the committed
results/pilot_R2 JSON that Chapter 5 cites.
"""

from __future__ import annotations

import collections
import json
import os
import pickle
import sys

import numpy as np

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO, "experiments", "pilot"))
sys.path.insert(0, REPO)
RES = os.environ["PILOT_RESULTS_DIR"]
from data import build  # noqa: E402

out = {}


def rec(name, ok, detail):
    tag = "INFO" if ok is None else ("PASS" if bool(ok) else "FAIL")
    print(f"[{tag}] {name}: {detail}")
    out[name] = {"status": tag, "detail": detail}


def J(d, f):
    return json.load(open(os.path.join(d, f)))


R2 = os.path.join(REPO, "results", "pilot_R2")
data = build("primary")
y = data.y
cf = pickle.load(open(os.path.join(RES, "state", "crossfit.pkl"), "rb"))["label_nll_primary"]
p = cf.p_cal
assert not np.isnan(p).any()


# ---- independent metric implementations -----------------------------------------------------
def auc_mw(y, s):
    pos, neg = s[y == 1], s[y == 0]
    gt = (pos[:, None] > neg[None, :]).sum()
    eq = (pos[:, None] == neg[None, :]).sum()
    return (gt + 0.5 * eq) / (pos.size * neg.size)


def ap_rank(y, s):
    """AP = sum over positives of precision at that positive's threshold (ties handled by grouping)."""
    order = np.argsort(-s, kind="mergesort")
    ys, ss = y[order], s[order]
    tp = np.cumsum(ys)
    k = np.arange(1, len(ys) + 1)
    # precision evaluated at the end of each tie block
    last = np.r_[ss[1:] != ss[:-1], True]
    prec_end = np.empty_like(tp, dtype=float)
    idx_end = np.flatnonzero(last)
    start = 0
    for e in idx_end:
        prec_end[start:e + 1] = tp[e] / k[e]
        start = e + 1
    return float(np.sum(prec_end[ys == 1]) / ys.sum())


def ece(y, s, M, right_closed=True):
    if right_closed:
        b = np.clip(np.ceil(s * M).astype(int) - 1, 0, M - 1)
    else:
        b = np.clip(np.floor(s * M).astype(int), 0, M - 1)
    return float(sum((b == m).mean() * abs(y[b == m].mean() - s[b == m].mean()) for m in range(M) if (b == m).any()))


e1r = J(RES, "e1_crossfit.json")["label_nll_primary"]["pooled_calibrated"]
e1c = J(R2, "e1_crossfit.json")["label_nll_primary"]["pooled_calibrated"]
mine = {"roc_auc": auc_mw(y, p), "average_precision": ap_rank(y, p), "ece": ece(y, p, 10),
        "log_loss": float(-np.mean(y * np.log(np.clip(p, 1e-6, 1 - 1e-6)) + (1 - y) * np.log(1 - np.clip(p, 1e-6, 1 - 1e-6)))),
        "brier_binary_SC5": float(np.mean((p - y) ** 2))}
for k, v in mine.items():
    rec(f"heldout_{k}", abs(v - e1c[k]) < 1e-9 and abs(v - e1r[k]) < 1e-12,
        f"independent {v:.6f} | reproduced {e1r[k]:.6f} | committed pilot_R2 {e1c[k]:.6f}")
rec("ece_binning_convention_sensitivity", None,
    f"right-closed bins (code, Eq.3.20 note) {ece(y, p, 10):.6f} vs left-closed {ece(y, p, 10, False):.6f}; "
    f"M=15: {ece(y, p, 15):.6f}; M=20: {ece(y, p, 20):.6f}")
rec("brier_conventions", None, f"binary mean (p-y)^2 = {mine['brier_binary_SC5']:.6f}; two-class sum = {2 * mine['brier_binary_SC5']:.6f}")
base_rate = y.mean()
rec("average_precision_baseline", None, f"AP of a random scorer = prevalence = {base_rate:.4f} (921/6762)")

# ---- replay: ASR, utility, denominators -------------------------------------------------------
rep = pickle.load(open(os.path.join(RES, "state", "replay_main.pkl"), "rb"))
agree = pickle.load(open(os.path.join(RES, "state", "rmod.pkl"), "rb"))["agree"]
by = collections.defaultdict(dict)
for eid, c, u, s, err, aud in rep:
    by[eid][c] = (u, s, err, aud)
valid = sorted(e for e, ok in agree.items() if ok)
att = [e for e in valid if data.episodes[e].attacked]
ben = [e for e in valid if not data.episodes[e].attacked]
e4r = J(RES, "e4_e5_enforcement_replay.json")["configs"]
e4c = J(R2, "e4_e5_enforcement_replay.json")["configs"]
rec("replay_denominators", None, {"episodes": len(by), "valid_AM4": len(valid), "attacked_valid": len(att), "benign_valid": len(ben),
                                  "excluded_by_AM4": len(by) - len(valid)})
for c in ("B0", "B1_step_level_no_reviewer", "REM_step_level_no_reviewer", "REM_step_level_idealized",
          "REM_episode_level_no_reviewer", "B1_episode_level_no_reviewer"):
    asr = float(np.mean([by[e][c][1] for e in att]))
    bu = float(np.mean([by[e][c][0] for e in ben]))
    ua = float(np.mean([by[e][c][0] for e in att]))
    ok = abs(asr - e4c[c]["ASR"][0]) < 1e-12 and abs(bu - e4c[c]["benign_utility"][0]) < 1e-12
    rec(f"replay_{c}", ok, f"ASR {asr:.4f} (= {sum(by[e][c][1] for e in att)}/{len(att)} attacked episodes, AgentDojo security=True), "
                           f"benign utility {bu:.4f} (= {sum(by[e][c][0] for e in ben)}/{len(ben)}), utility under attack {ua:.4f}; "
                           f"committed ASR {e4c[c]['ASR'][0]:.4f}, BU {e4c[c]['benign_utility'][0]:.4f}")

# ---- approval vs completion on benign episodes ------------------------------------------------
STATE_CHANGING = {"send_money", "schedule_transaction", "update_scheduled_transaction", "update_password", "update_user_info"}
c = "REM_step_level_no_reviewer"
appr, compl, both = 0, 0, 0
n_sc = 0
for e in ben:
    aud = by[e][c][3]
    sc = [a for a in aud if a[4] in STATE_CHANGING]
    if not sc:
        continue
    n_sc += 1
    a_ok = all(a[2] for a in sc)
    u_ok = bool(by[e][c][0])
    appr += a_ok
    compl += u_ok
    both += a_ok and u_ok
rec("benign_approval_vs_completion", None,
    f"{c}: of {n_sc} benign episodes with state-changing proposals, all such calls released in {appr}, "
    f"task completed (AgentDojo utility) in {compl}, both in {both}. Release is not completion.")

# ---- per-call vs per-episode ------------------------------------------------------------------
steps = [a for e in att for a in by[e][c][3]]
y1 = [a for a in steps if a[0] == 1]
rec("per_call_vs_per_episode", None,
    f"{c}: y=1 calls withheld {np.mean([not a[2] for a in y1]):.4f} (n={len(y1)} calls) vs episode ASR "
    f"{np.mean([by[e][c][1] for e in att]):.4f} (n={len(att)} episodes)")

# ---- latency boundaries -----------------------------------------------------------------------
lat = np.array([a[5] for e in valid for a in by[e][c][3]])
latf = np.array([a[8] for e in valid for a in by[e][c][3]])
rec("latency_reproduced", None,
    f"{c}: partial timer median {np.median(lat):.3f} ms p95 {np.percentile(lat, 95):.3f}; complete-call timer median "
    f"{np.median(latf):.3f} ms p95 {np.percentile(latf, 95):.3f}. Both start at RemGuard.evaluate entry; neither includes "
    "tool execution, sandbox I/O, LLM/API time, trace loading, or an injection classifier (absent). Both include the "
    "reference-label lookup (evaluation bookkeeping). Committed R4 complete-call median: "
    f"{J(os.path.join(REPO, 'results', 'pilot_R4'), 'e4_e5_enforcement_replay.json')['configs'][c]['latency_full_ms_median']:.3f} ms")

# ---- r_mod: what the oracle-Modify replay measures --------------------------------------------
rr = pickle.load(open(os.path.join(RES, "state", "replay_rmod.pkl"), "rb"))
byr = collections.defaultdict(dict)
for eid, cc, u, s, err, aud in rr:
    byr[eid][cc] = (u, s, err, aud)
resid = []
for e in byr:
    ep = data.episodes[e]
    if not ep.attacked or not agree.get(e):
        continue
    aud = byr[e]["oracle_modify_step_level"][3]
    if any(a[1] == "modify" for a in aud) and byr[e]["oracle_modify_step_level"][1]:
        resid.append((e, [(a[4], a[0], a[1]) for a in aud]))
rec("r_mod_residual_episodes", None,
    {"n": len(resid), "episodes": [r[0] for r in resid],
     "interpretation": "every y=1 call on a T_R tool is withheld by the oracle; residual success therefore arises only "
                       "from calls the label rule does not mark y=1 (label coverage), not from a weakness of a Modify mechanism",
     "first_episode_calls(tool,label,verdict)": resid[0][1] if resid else None})

json.dump(out, open(os.path.join(REPO, "CODE_AUDIT_R4", "logs", "audit_results.json"), "w"), indent=1, default=str)
