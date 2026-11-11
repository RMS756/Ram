"""POST HOC (protocol amendment A-1, made AFTER results were seen) — not part of the frozen protocol.

Reason: the pre-declared S1 ablation "action evidence removed from M11+AZ" gave 12 attacks and 140 benign
successes, better than the candidate itself. The protocol ran ablations under S1 only. To avoid leaving an
S1-only number that could be over-read, the same arm is evaluated under S2 (double holdout). Nothing is
selected from this result; it is reported as exploratory and labelled post hoc.

Also measures peak Python memory of one guard decision loop (tracemalloc) for M00, P1 and M11+AZ.
"""
from __future__ import annotations

import multiprocessing as mp
import os
import sys
import tracemalloc

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import study as S  # noqa: E402
from study import G, common, pilot_state  # noqa: E402
from data import build, load_raw  # noqa: E402
from rem.integration.agentdojo_replay import replay_episode  # noqa: E402

ARM = "M11+AZ_noact"


def _fit(key):
    _, u, i = key
    train = (G["ut"] != u) & (G["it"] != i)
    cell, _ = S.fit_cell(train, ["F1_noact"], ("a", "b", "am", "bm"))
    return key, cell["models"]


def main():
    st = common.make_setup()
    raw = load_raw()
    data = build("primary", raw)
    aux = S.load("fit_aux")
    cells = S.load("cells")
    ut = np.array([s.user_task_id for s in data.steps], dtype=object)
    it = np.array([s.injection_task_id or "none" for s in data.steps], dtype=object)
    G.update(data=data, Z=aux["Z"], T=aux["T"], ut=ut, it=it)
    keys = sorted(k for k in cells if k[0] == "S2")
    with mp.get_context("fork").Pool(4) as pool:
        for key, models in pool.map(_fit, keys, chunksize=4):
            cells[key]["models"].update(models)
    valid = aux["valid"]
    cell_of = {"S2": {("primary", e): ("S2", data.episodes[e].user_task_id, data.episodes[e].injection_task_id or data.episode_fold[e])
                      for e in valid}}
    G.update(setup=st, eps={"primary": data.episodes}, cells=cells, cell_of=cell_of)
    jobs = [("S2", e, ARM, "primary") for e in valid]
    with mp.get_context("fork").Pool(4) as pool:
        res = pool.map(S._replay_job, jobs, chunksize=64)
    S.save("replay_posthoc_a1", res)
    att = [e for e in valid if data.episodes[e].attacked]
    by = {r[2]: r for r in res}
    print("POST HOC S2", ARM, "attacks", sum(by[e][5] for e in att), "/", len(att),
          "benign", sum(by[e][4] for e in valid if not data.episodes[e].attacked), "/", len(valid) - len(att))
    # memory: peak traced allocation while building a guard and replaying one multi-step episode
    eid = max(valid, key=lambda e: len([m for m in data.episodes[e].messages if m.role == "tool"]))
    mem = {}
    for arm in ("M00", "P1", "M11+AZ"):
        cell = cells[("S1", data.episode_fold[eid])]
        tracemalloc.start()
        g = S.make_guard(arm, cell, data.episodes[eid], st)
        replay_episode(data.episodes[eid], st.suite, g)
        mem[arm] = tracemalloc.get_traced_memory()[1] / 1024.0
        tracemalloc.stop()
    S.save("memory_kib", {"episode": eid, "peak_kib_including_agentdojo_replay": mem})
    print("peak traced KiB (guard + replay of one episode):", {k: round(v) for k, v in mem.items()})


if __name__ == "__main__":
    main()
