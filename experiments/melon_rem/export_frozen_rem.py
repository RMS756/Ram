"""Export the frozen REM components used by the MELON vs MELON+REM study (no fitting).

usage (main environment, AgentDojo 0.1.35, from the repository root):
  PILOT_RESULTS_DIR=<dir with state/crossfit.pkl and state/rmod.pkl> \
  python3 experiments/melon_rem/export_frozen_rem.py <out.pkl>

The bundle holds, for EVERY outer fold of the frozen nested cross-fit (Chapter 3, Sec. 3.11.5):
the frozen scorer (ridge coefficients, x-bar, logit-calibration gamma_0/gamma_1), the REM decision
policies A3_step_level / A3_episode_level (loss grid from the declared pilot_e0 exploratory costs and the
fold's r_mod; Chapter 3 tie order), and the benign transition reference fitted without that fold.
It also holds the shared evidence specification, instruction-pattern detector, consequence tier map,
restricted tool set and reference labeler (audit only), and the fold assignment of benign user tasks.

Nothing is fitted, tuned or changed: every object is loaded from the frozen state, or rebuilt from the
committed configuration exactly as experiments/live/run_live.py:frozen_components does. The output file
records sha256 hashes of its inputs. It is a pickle: load it only from this trusted pipeline.
"""
from __future__ import annotations

import hashlib
import json
import os
import pickle
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "experiments", "pilot"))


def sha256(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main(out: str) -> None:
    import common
    import run_main as rm
    from data import build, reference_from_mask
    from rem.algorithms.behavior.evidence import FEATURE_ORDER
    from rem.evaluation.crossfit import assign_round_robin
    from rem.integration.agentdojo_replay import FrozenScorer

    state = os.path.join(common.RESULTS, "state")
    cf, rmp = os.path.join(state, "crossfit.pkl"), os.path.join(state, "rmod.pkl")
    fits = pickle.load(open(cf, "rb"))
    rmod = pickle.load(open(rmp, "rb"))["rmod"]
    pol = rm.build_policies(fits, rmod)
    st = common.make_setup()
    data = build("primary")

    folds = {}
    for f, ff in fits["label_nll_primary"].fits.items():
        folds[str(f)] = {
            "scorer": FrozenScorer(tuple(FEATURE_ORDER), ff.intercept, tuple(ff.coefficients),
                                   ff.gamma_0, ff.gamma_1, tuple(ff.xbar)),
            "policies": {k: pol[f][k] for k in ("A3_step_level", "A3_episode_level")},
            "reference": reference_from_mask(data, data.fold != f),
            "gamma_1": float(ff.gamma_1),
        }
    inj = sorted({e.injection_task_id for e in data.episodes.values() if e.injection_task_id}, key=str)
    users = sorted({e.user_task_id for e in data.episodes.values()}, key=str)
    rr = assign_round_robin(users, len(inj))
    benign_fold = {u: inj[rr[u]] for u in users}

    cfg_path = os.path.join(REPO, "configs", "exploratory", "pilot_e0.yaml")
    commit = subprocess.check_output(["git", "-C", REPO, "rev-parse", "HEAD"], text=True).strip()
    import agentdojo, importlib.metadata as md  # noqa: E401
    bundle = {
        "status": "FROZEN REM COMPONENTS - EXPLORATORY DESIGN VALUES (pilot_e0), NOT SUPERVISOR-APPROVED",
        "provenance": {
            "rem_commit_at_export": commit,
            "crossfit_pkl_sha256": sha256(cf),
            "rmod_pkl_sha256": sha256(rmp),
            "pilot_config": os.path.relpath(cfg_path, REPO),
            "pilot_config_sha256": sha256(cfg_path),
            "agentdojo_version_at_export": md.version("agentdojo"),
        },
        "folds": folds,
        "benign_user_task_fold": benign_fold,
        "injection_tasks": inj,
        "rmod": json.loads(json.dumps(rmod, default=float)),
        "spec": st.spec,
        "detector": st.detector,
        "tier_map": st.tier_map,
        "restricted_tools": tuple(st.restricted),
        "labeler": st.labeler,
    }
    with open(out, "wb") as fh:
        pickle.dump(bundle, fh)
    meta = {k: bundle[k] for k in ("status", "provenance", "benign_user_task_fold", "injection_tasks", "rmod")}
    meta["bundle_sha256"] = sha256(out)
    meta["gamma_1_by_fold"] = {f: d["gamma_1"] for f, d in folds.items()}
    meta["restricted_tools"] = list(bundle["restricted_tools"])
    with open(out + ".json", "w") as fh:
        json.dump(meta, fh, indent=1)
    print(json.dumps(meta, indent=1))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    if os.environ.get("PYTHONHASHSEED") != "0":
        # Set iteration order (hence the pickle bytes, not the content) depends on string hashing:
        # re-execute with a fixed hash seed so that the bundle's sha256 is reproducible.
        os.execve(sys.executable, [sys.executable, *sys.argv], {**os.environ, "PYTHONHASHSEED": "0"})
    main(sys.argv[1])
