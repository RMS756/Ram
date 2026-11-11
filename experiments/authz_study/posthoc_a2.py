"""POST HOC (protocol amendment A-2, made AFTER results were seen) — not part of the frozen protocol.

Reason: the original study's own reproduced ablation "behavioural evidence removed" (abl_no_beh) has 11
successful attacks and 140 benign successes under the primary folds, which is at least as good as every arm
of this study. It had never been evaluated under double holdout, on held-out templates, under the
reformatted-identifier probe or on the fixtures. This script does that with REM's unchanged rule (arm
M00_nobeh). It is exploratory; nothing is selected from it.
"""
from __future__ import annotations

import dataclasses
import multiprocessing as mp
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import study as S  # noqa: E402
from study import G, common, pilot_state  # noqa: E402
from data import build, load_raw  # noqa: E402

ARM = "M00_nobeh"


def _fit(key):
    data = G["data"]
    if key[0] == "S1":
        train = data.fold != key[1]
    else:
        train = (G["ut"] != key[1]) & (G["it"] != key[2])
    cell, _ = S.fit_cell(train, ["F0_nobeh"], ("y",))
    return key, cell["models"]


def main():
    st = common.make_setup()
    raw = load_raw()
    data = build("primary", raw)
    xt = build("cross_template", raw)
    aux = S.load("fit_aux")
    cells = S.load("cells")
    ut = np.array([s.user_task_id for s in data.steps], dtype=object)
    it = np.array([s.injection_task_id or "none" for s in data.steps], dtype=object)
    G.update(data=data, Z=aux["Z"], T=aux["T"], ut=ut, it=it)
    with mp.get_context("fork").Pool(4) as pool:
        for key, models in pool.map(_fit, sorted(cells), chunksize=4):
            cells[key]["models"].update(models)
    S.save("cells_posthoc_a2", {k: {"models": {("F0_nobeh", "y"): v["models"][("F0_nobeh", "y")]}} for k, v in cells.items()})
    # sanity: the S1 fit must equal the original study's stored no_beh fit
    orig = pilot_state("crossfit")["no_beh"].fits
    mx = max(max(abs(a - b) for a, b in zip(cells[("S1", f)]["models"][("F0_nobeh", "y")]["coef"], ff.coefficients))
             for f, ff in orig.items())
    print("max |coef difference| vs original no_beh fits:", mx)
    valid = aux["valid"]
    probe = {}
    for e in valid:
        ep = data.episodes[e]
        if ep.attacked and any(S.ATTACKER_IBAN in v for v in ep.injections.values()):
            probe[e] = dataclasses.replace(ep, injections={k: v.replace(S.ATTACKER_IBAN, S.spaced(S.ATTACKER_IBAN))
                                                           for k, v in ep.injections.items()})
    cell_of = {"S1": {}, "S2": {}}
    for e in valid:
        ep = data.episodes[e]
        cell_of["S1"][("primary", e)] = ("S1", data.episode_fold[e])
        cell_of["S2"][("primary", e)] = ("S2", ep.user_task_id, ep.injection_task_id or data.episode_fold[e])
    for e, ep in xt.episodes.items():
        cell_of["S1"][("cross_template", e)] = ("S1", ep.injection_task_id)
    for e in probe:
        cell_of["S1"][("probe_iban", e)] = ("S1", data.episode_fold[e])
    G.update(setup=st, eps={"primary": data.episodes, "cross_template": xt.episodes, "probe_iban": probe}, cells=cells, cell_of=cell_of)
    jobs = ([("S1", e, ARM, "primary") for e in valid] + [("S2", e, ARM, "primary") for e in valid]
            + [("S1", e, ARM, "cross_template") for e in sorted(xt.episodes)] + [("S1", e, ARM, "probe_iban") for e in sorted(probe)])
    with mp.get_context("fork").Pool(4) as pool:
        res = pool.map(S._replay_job, jobs, chunksize=64)
    S.save("replay_posthoc_a2", res)
    att = [e for e in valid if data.episodes[e].attacked]
    ben = [e for e in valid if not data.episodes[e].attacked]
    for scheme, role, ids in (("S1", "primary", valid), ("S2", "primary", valid), ("S1", "probe_iban", sorted(probe))):
        by = {r[2]: r for r in res if r[0] == scheme and r[1] == role}
        a = [e for e in ids if e in set(att)]
        b = [e for e in ids if e in set(ben)]
        print("POST HOC", scheme, role, ARM, "attacks", sum(by[e][5] for e in a), "/", len(a),
              "benign", sum(by[e][4] for e in b), "/", len(b),
              "USCR", sum(1 for e in a if any(x[0] == 1 and x[2] for x in by[e][7])))


if __name__ == "__main__":
    main()
