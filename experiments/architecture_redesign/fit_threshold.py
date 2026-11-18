"""Development-only fit of the consequence-independent comparator threshold (REM-C-T).

theta = frozen B1 operating threshold (rem.algorithms.a1.operating_threshold, Ch.3 Eq. 3.14) at the frozen alpha_blk of
configs/exploratory/pilot_e0.yaml, fitted on the learned scores (Platt-calibrated, arm C1L) of restricted calls WITHOUT an
attack label in BENIGN episodes of the PRIMARY population, scheme S1, as stored by the controlled study (ctl_replays.pkl).
No held-out population (H, probes) is used.
"""
import json
import os
import pickle
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments" / "repair_study"))
from rem.algorithms.a1 import operating_threshold  # noqa: E402
import rs_run as V1R  # noqa: E402


def main(out):
    alpha = yaml.safe_load((ROOT / "configs/exploratory/pilot_e0.yaml").read_text())["baseline_B1"]["alpha_blk"]
    d, aux, eps, folds = V1R.C._populations()
    benign = {e for e, ep in eps["primary"].items() if not ep.attacked}
    res = pickle.load(open(Path(os.environ["COMPETITIVE_STATE"]) / "ctl_replays.pkl", "rb"))
    st = V1R.common.make_setup()
    restricted = set(st.restricted)
    p = [x[10] for sc, role, e, a, u, s, err, aud in res if sc == "S1" and role == "primary" and a == "C1L" and e in benign
         for x in aud if x[4] in restricted and x[0] != 1 and x[10] is not None]
    theta = operating_threshold(p, alpha)
    Path(out).write_text(json.dumps({"theta": theta, "alpha_blk": alpha, "n_scores": len(p), "source": "ctl_replays.pkl C1L primary S1 benign, label 0",
                                     "procedure": "rem.algorithms.a1.operating_threshold (Eq. 3.14)"}, indent=1))
    print("theta", theta, "alpha", alpha, "n", len(p))


if __name__ == "__main__":
    main(sys.argv[1])
