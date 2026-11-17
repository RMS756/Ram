"""Study of 18 November 2026: development replay and report of C1, C2[PG], C3[PG] (02_PROTOCOL.md). No model call.

Stages:
  replay  replay the candidates on the stored populations (primary S1 and S2, second population, probe)
  diag    reference-labelled sequence diagnostics (diag_harness) for the candidates and the frozen v2 arms
  report  tables, paired intervals, outcome changes, fixtures; reference arms are read from stored replays
Output: REM_PROGENT_COMPETITIVE_2026_11_18/results/
"""
from __future__ import annotations

import collections
import gzip
import json
import multiprocessing as mp
import pickle
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _p in ("experiments/progent_competitive", "experiments/repair_study"):
    sys.path.insert(0, str(ROOT / _p))
import rs_run as V1R              # noqa: E402  (populations, stores, helpers of the repair study)
import rs_run_v2 as V2R           # noqa: E402
import contract_arms as CA        # noqa: E402
import diag_harness as H          # noqa: E402

C, J, S, R, common = V1R.C, V1R.J, V1R.S, V1R.R, V1R.common
OUT = ROOT / "REM_PROGENT_COMPETITIVE_2026_11_18" / "results"
OUT.mkdir(parents=True, exist_ok=True)
STATE = V1R.STATE
REFS = V1R.BASELINES + ["GV_math2", "HV_math2", "GV_math2x", "HV_math2x"]
TABLE_ARMS = REFS + list(CA.ARMS)
CONTRASTS = [("C2PG", "C1"), ("C2PG", "PG"), ("C3PG", "C2PG"), ("C1", "GV_math2"), ("C1", "GV_math2x"), ("C1", "PG"),
             ("C1", "REM10"), ("C2PG", "GV_math2x"), ("C3PG", "HV_math2x")]
W = {}


def replay_job(job):
    scheme, role, e, arm = job
    ep = W["eps"][role][e]
    key = ("S1", W["fold"][role][e]) if scheme == "S1" else ("S2", ep.user_task_id, ep.injection_task_id or W["fold"][role][e])
    out = S.replay_episode(ep, W["setup"].suite, CA.make_guard(arm, W["jcells"][key], W["cs"][key], ep, W["setup"]))
    audit = [(a["label"], a["verdict"], bool(a["released"]), a["tier"], a["tool"], a["rem_latency_full_ms"], a["verdict_source"],
              a["details"].get("perm"), (a["details"].get("cs") or {}).get("stage"), a["details"].get("contract"))
             for a in out.audit]
    return scheme, role, e, arm, bool(out.utility), bool(out.security), out.error, audit


def stage_replay():
    d, aux, eps, folds = C._populations()
    W.update(setup=common.make_setup(), jcells=J.load("cells"), cs=C.load("cs_cells"), eps=eps, fold=folds)
    jobs = [("S1", role, e, a) for role, pop in eps.items() for a in CA.ARMS for e in sorted(pop)]
    jobs += [("S2", "primary", e, a) for a in CA.FITTED for e in aux["valid"]]
    t = time.time()
    res = []
    with mp.get_context("fork").Pool(4) as p:
        for v in p.imap_unordered(replay_job, jobs, chunksize=32):
            res.append(v)
    with (STATE / "cp_replays.pkl").open("wb") as f:
        pickle.dump(res, f)
    print("replay done", len(res), round(time.time() - t), "s; errors", sum(1 for r in res if r[6]), flush=True)


def _build_factory():
    import repaired_arms_v2 as RA2
    import reproduce_defects as RD
    st = common.make_setup()
    cells, cs = J.load("cells"), C.load("cs_cells")
    key = ("S1", "injection_task_0")

    def build(arm, ep):
        ep.system_prompt = RD.tf.SYSTEM_PROMPT
        mod = CA if arm in CA.ARMS else RA2
        return mod.make_guard(arm, cells[key], cs[key], ep, st)
    return build


def stage_diag():
    rows = H.run_all(_build_factory(), ["GV_math2", "HV_math2", "GV_math2x", "HV_math2x"] + list(CA.ARMS))
    out = H.dump(OUT / "diagnostics.json", rows, {"note": "C2PG and C3PG add Progent's MANUAL banking policy, whose trusted-recipient "
                                                           "list contains only AgentDojo accounts; on the synthetic accounts of the "
                                                           "diagnostics they therefore withhold every payment by design of that policy."})
    for arm, s in out["score"].items():
        print(arm, s["authorized_released"], "/", s["authorized_n"], "| unauthorized", s["unauthorized_released"], "/", s["unauthorized_n"],
              s["unauthorized_released_cases"], flush=True)


def stage_of(x):
    src = x[6]
    if src.startswith("contract_"):
        return src
    if src == "progent_policy":
        return "progent_policy_refused"
    if src == "permission_guard_authority_v3":
        return "front_blocked"
    if src in ("D1", "D2"):
        return "predicate_" + x[1]
    if src == "candidate_release":
        return "released_by_contract"
    return ("learned_released" if x[2] else "learned_withheld_" + x[1]) if x[8] == "learned" else ("other_" + src)


def fixtures():
    import repaired_arms_v2 as RA2
    saved = RA2.make_guard, RA2.ARMS
    try:
        RA2.make_guard, RA2.ARMS = CA.make_guard, CA.ARMS        # reuse the v2 fixture harness with the candidate factory
        return V2R.fixtures(J.load("cells"), C.load("cs_cells"))
    finally:
        RA2.make_guard, RA2.ARMS = saved


def stage_report():
    d, aux, eps, folds = C._populations()
    restricted = set(common.make_setup().restricted)
    with (STATE / "cp_replays.pkl").open("rb") as f:
        mine = pickle.load(f)
    with (STATE / "rs_replays_v2.pkl").open("rb") as f:
        v2 = pickle.load(f)
    stored = J.load("replays") + J.load("value_replays") + C.load("cs_replays")
    by = collections.defaultdict(lambda: collections.defaultdict(dict))
    for scheme, role, e, a, u, s, err, aud in stored:
        if a in V1R.BASELINES:
            by[(scheme, role)][e][a] = (int(u), int(s), err, aud)
    for scheme, role, e, a, u, s, err, aud in v2 + mine:
        if a in TABLE_ARMS:
            by[(scheme, role)][e][a] = (int(u), int(s), err, aud)
    fresh = aux["fresh"]
    b0 = {r[2]: r for r in J.load("replays") if r[0] == "S1" and r[1] == "dev2" and r[3] == "B0"}
    elig = sorted(e for e, r in b0.items() if r[6] is None and (int(r[4]), int(r[5])) == (fresh[e].utility, fresh[e].security))
    pops = {}
    for name, scheme, role, ids in [("primary_S1", "S1", "primary", aux["valid"]), ("primary_S2", "S2", "primary", aux["valid"]),
                                    ("dev2", "S1", "dev2", elig)]:
        B = by[(scheme, role)]
        if scheme == "S2":
            for e in ids:
                for a in TABLE_ARMS:
                    if a not in B[e]:
                        B[e][a] = by[("S1", "primary")][e][a]
        episodes = d.episodes if role == "primary" else fresh
        att = [e for e in ids if episodes[e].attacked]
        ben = [e for e in ids if not episodes[e].attacked]
        usr = lambda e: episodes[e].user_task_id      # noqa: E731
        inj = lambda e: episodes[e].injection_task_id  # noqa: E731
        mm = R.block(B, att, ben, TABLE_ARMS, restricted)
        stages, reasons = {}, {}
        for a in CA.ARMS:
            c, rs = collections.Counter(), collections.Counter()
            for e in ids:
                for x in B[e][a][3]:
                    if x[4] not in restricted:
                        continue
                    lab = "attack_labelled" if x[0] == 1 else "not_attack_labelled"
                    c[f"{lab}|{stage_of(x)}"] += 1
                    if x[6].startswith("contract_") and x[9]:
                        rs[f"{usr(e)}|{x[6]}|{str(x[9][2])[:70]}"] += 1
            stages[a], reasons[a] = dict(sorted(c.items())), dict(sorted(rs.items()))
        changed = {}
        for a, b in CONTRASTS:
            rows = [{"episode": e, "user_task": usr(e), "injection_task": inj(e), a: list(B[e][a][:2]), b: list(B[e][b][:2])}
                    for e in ids if B[e][a][:2] != B[e][b][:2]]
            changed[f"{a} vs {b}"] = {"episodes_with_different_outcome": len(rows),
                                     "utility_gained": sum(1 for r in rows if r[a][0] > r[b][0]),
                                     "utility_lost": sum(1 for r in rows if r[a][0] < r[b][0]),
                                     "attack_success_added": sum(1 for r in rows if r[a][1] > r[b][1]),
                                     "attack_success_removed": sum(1 for r in rows if r[a][1] < r[b][1]),
                                     "by_user_task": dict(collections.Counter(r["user_task"] for r in rows)), "rows": rows}
        pops[name] = {"n_attacked": len(att), "n_benign": len(ben), "arms": mm,
                      "contrasts": {a + " minus " + b: R.paired(B, att, ben, usr, inj, a, b) for a, b in CONTRASTS},
                      "restricted_call_stages": stages, "contract_reasons": reasons, "outcome_changes": changed}
        print(name, [(a, m["attacks_successful"], m["benign_completed"], m["all_tasks_completed"]) for a, m in mm.items()], flush=True)
    probe = by[("S1", "probe")]
    out = {"status": "EXPLORATORY DEVELOPMENT EVIDENCE (02_PROTOCOL.md): offline replay of recorded calls (NO-ADAPT); no live agent; "
                     "no model call; cohorts inspected in earlier studies; not independent validation",
           "populations": pops,
           "probe_reformatted_identifier": {"n": len(probe), "arms": {a: {"attacks": sum(v[a][1] for v in probe.values()),
                                                                           "replay_errors": sum(v[a][2] is not None for v in probe.values())}
                                                                       for a in TABLE_ARMS if all(a in v for v in probe.values())}},
           "replays": len(mine), "replay_errors": sum(1 for r in mine if r[6]),
           "fixtures": fixtures()}
    (OUT / "results.json").write_text(json.dumps(out, indent=1, default=common._default), encoding="utf-8")
    with gzip.open(OUT / "episode_outcomes.jsonl.gz", "wt", encoding="utf-8") as f:
        for scheme, role, e, a, u, s, err, aud in sorted(mine, key=lambda z: z[:4]):
            f.write(json.dumps({"scheme": scheme, "population": role, "episode_id": e, "arm": a, "utility": u, "security": s, "error": err}) + "\n")
    with gzip.open(OUT / "restricted_call_audit.jsonl.gz", "wt", encoding="utf-8") as f:
        for scheme, role, e, a, u, s, err, aud in sorted(mine, key=lambda z: z[:4]):
            for k, x in enumerate(aud):
                if x[4] in restricted:
                    f.write(json.dumps({"scheme": scheme, "population": role, "episode_id": e, "arm": a, "call": k, "tool": x[4],
                                        "attempt_label": x[0], "verdict": x[1], "released": x[2], "source": x[6], "stage": x[8],
                                        "contract": x[9]}, default=common._default) + "\n")


if __name__ == "__main__":
    for stage in sys.argv[1:]:
        {"replay": stage_replay, "diag": stage_diag, "report": stage_report}[stage]()
