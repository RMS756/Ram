"""Per-cell fits of the competitive study: NP split fit, CRC split fit, gradient-boosted trees.

Status: [PROPOSED - EXPLORATORY]. Fitting uses the training portion of each cell only (S1: one attacker
objective held out; S2: one user task and one attacker objective held out). The ridge procedure is REM's
own (study.fit_cell, unchanged). No evaluation outcome is read here.

Split used by the NP and CRC fits (an adaptation, stated in the protocol): the training portion is divided
into a fit half A and a calibration half B by REM's own inner grouping (attacker objective for attacked
episodes, the benign grouping for benign ones), assigned round-robin over the sorted group names. The
nproc package splits the controlled class at random; a grouped split is used here because steps of one
attacker objective are not independent.
"""
from __future__ import annotations

import collections
import sys
from pathlib import Path

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "g3_integration"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import run as J  # noqa: E402  (integration package: data, caches, fitting globals)
from candidates import crc_release_cutoff, np_release_cutoff  # noqa: E402

S, I = J.S, J.I
ALPHAS = (0.05, 0.01)
DELTA = 0.05
GB_DEPTHS = (1, 2, 3)
GB_STAGES = (25, 50, 100, 200)
GB_LEARNING_RATE = 0.1
W = {}


def setup_globals():
    """Same preparation as the integration package's fit stage (permission indicators as extra columns)."""
    d = J.data()
    S.ALL_ORDER = tuple(I.FEATURE_ORDER) + tuple(J.PERM3_ORDER)
    S.FEATURE_SETS["F4"] = I.NOBEH + tuple(J.PERM3_ORDER)
    Z = np.zeros((len(d.steps), len(J.PERM3_ORDER)))
    groups = collections.defaultdict(list)
    for i, s in enumerate(d.steps):
        groups[s.episode_id].append((s.index, i))
    for e, g in groups.items():
        idx = [i for _, i in sorted(g)]
        tiers = iter(d.steps[i].tier for i in idx)
        ev = J.offline_permission_v3(d.episodes[e], lambda tool, args: next(tiers))
        assert len(ev) == len(idx)
        for i, v in zip(idx, ev):
            Z[i] = [v.features()[f] for f in J.PERM3_ORDER]
    S.G.update(data=d, Z=Z, T={"y": d.y.copy()})
    W.update(data=d, Z=Z,
             ut=np.array([s.user_task_id for s in d.steps], dtype=object),
             it=np.array([s.injection_task_id or "none" for s in d.steps], dtype=object),
             ep=np.array([s.episode_id for s in d.steps], dtype=object),
             tool=np.array([s.tool for s in d.steps], dtype=object))
    return d


def train_mask(key):
    d = W["data"]
    return (d.fold != key[1]) if key[0] == "S1" else ((W["ut"] != key[1]) & (W["it"] != key[2]))


def halves(train):
    d = W["data"]
    g, benign = d.inner_group, ~d.attacked
    tr = np.flatnonzero(train)
    att = S.assign_round_robin([g[i] for i in tr if not benign[i]], 2)
    ben = S.assign_round_robin([g[i] for i in tr if benign[i]], 2)
    half = np.full(len(d.steps), -1)
    for i in tr:
        half[i] = (ben if benign[i] else att)[g[i]]
    return train & (half == 0), train & (half == 1)


def scores(rec, X):
    return rec["b0"] + X[:, S._cols(rec["order"])] @ np.asarray(rec["coef"], dtype=float)


def fit_np(train):
    """Umbrella algorithm: the scorer is fitted without the left-out attack-labelled steps; the cutoff is an
    order statistic of their scores."""
    y = W["data"].y
    _a, b = halves(train)
    left_out = b & (y == 1)
    cell, X = S.fit_cell(train & ~left_out, ["F4"], ("y",))
    rec = cell["models"][("F4", "y")]
    s0 = scores(rec, X[left_out])
    return {"rec": rec, "cut": {str(a): np_release_cutoff(s0, a, DELTA) for a in ALPHAS}, "n_left_out": int(left_out.sum())}, X


def fit_crc(train):
    """The scorer is fitted on half A; the cutoff is calibrated on the episodes of half B."""
    y, ep = W["data"].y, W["ep"]
    a, b = halves(train)
    cell, X = S.fit_cell(a, ["F4"], ("y",))
    rec = cell["models"][("F4", "y")]
    s = scores(rec, X)
    units = sorted(set(ep[b].tolist()))
    mins = collections.defaultdict(lambda: float("inf"))
    for i in np.flatnonzero(b & (y == 1)):
        mins[ep[i]] = min(mins[ep[i]], float(s[i]))
    return {"rec": rec, "cut": {str(al): crc_release_cutoff(list(mins.values()), len(units), al) for al in ALPHAS},
            "n_units": len(units)}, X


def fit_gb(train, X_all):
    """Gradient-boosted trees on the F4 evidence with the same nested procedure as the ridge estimator:
    grouped inner folds, configuration chosen by inner out-of-fold log loss, calibration on the inner
    out-of-fold scores, refit on the whole training portion."""
    d, y = W["data"], W["data"].y
    order = S.FEATURE_SETS["F4"]
    X = X_all[:, S._cols(order)]
    n = len(d.steps)
    K = int(S.E["inner_folds"])
    g, benign = d.inner_group, ~d.attacked
    tr = np.flatnonzero(train)
    att = S.assign_round_robin([g[i] for i in tr if not benign[i]], K)
    ben = S.assign_round_robin([g[i] for i in tr if benign[i]], K)
    inner = np.full(n, -1)
    for i in tr:
        inner[i] = (ben if benign[i] else att)[g[i]]
    oof = {(dep, t): np.full(n, np.nan) for dep in GB_DEPTHS for t in GB_STAGES}
    for dep in GB_DEPTHS:
        for j in range(K):
            fit_mask, hold = train & (inner != j), train & (inner == j)
            if not hold.any():
                continue
            clf = GradientBoostingClassifier(n_estimators=max(GB_STAGES), max_depth=dep, learning_rate=GB_LEARNING_RATE,
                                             random_state=0).fit(X[fit_mask], y[fit_mask])
            for t, raw in enumerate(clf.staged_decision_function(X[hold]), 1):
                if t in GB_STAGES:
                    oof[(dep, t)][hold] = np.ravel(raw)
    loss = {cfg: float(S.log_loss(y[train], S.sigmoid(v[train]), S.E["probability_clip"])) for cfg, v in oof.items()}
    best = min(loss, key=lambda c: (loss[c], c[0], c[1]))
    cal, failed = S.LabelNLLLogitCalibrator(), False
    try:
        cal.fit(oof[best][train], y[train])
        g0, g1 = float(cal.gamma_0), float(cal.gamma_1)
    except S.MonotonicityViolationError:
        failed, g0, g1 = True, 0.0, 1.0
    clf = GradientBoostingClassifier(n_estimators=best[1], max_depth=best[0], learning_rate=GB_LEARNING_RATE,
                                     random_state=0).fit(X[train], y[train])
    leaves = int(sum(est[0].get_n_leaves() for est in clf.estimators_))
    return {"clf": clf, "order": tuple(order), "g0": g0, "g1": g1, "failed": failed, "max_depth": best[0], "n_estimators": best[1],
            "inner_logloss": {f"depth={c[0]},trees={c[1]}": v for c, v in loss.items()}, "n_leaves_total": leaves,
            "feature_importances": [float(v) for v in clf.feature_importances_], "ntrain": int(train.sum()), "npos": int(y[train].sum())}


def fit_job(key):
    train = train_mask(key)
    np_fit, X_np = fit_np(train)
    crc_fit, X_crc = fit_crc(train)
    X_all = np.hstack([S.design_matrix(W["data"].steps, S.reference_from_mask(W["data"], train), S.FEATURE_ORDER), W["Z"]])
    gb = fit_gb(train, X_all)
    out = {"np": np_fit, "crc": crc_fit, "gb": gb}
    if key[0] == "S1":                                    # held-out predictions, evaluated only in the report stage
        test = ~train
        ridge = W["jcells"][key]["models"][("F4", "y")]
        s_ridge = scores(ridge, X_all[test])
        raw_gb = np.ravel(gb["clf"].decision_function(X_all[test][:, S._cols(gb["order"])]))
        out["heldout"] = {"idx": np.flatnonzero(test), "s_ridge": s_ridge,
                          "p_ridge": S.sigmoid(ridge["g1"] * s_ridge + ridge["g0"]) if not ridge["failed"] else S.sigmoid(s_ridge),
                          "p_ridge_uncal": S.sigmoid(s_ridge), "raw_gb": raw_gb,
                          "p_gb": S.sigmoid(gb["g1"] * raw_gb + gb["g0"]) if not gb["failed"] else S.sigmoid(raw_gb),
                          "s_np": scores(np_fit["rec"], X_np[test]), "s_crc": scores(crc_fit["rec"], X_crc[test])}
    return key, out
