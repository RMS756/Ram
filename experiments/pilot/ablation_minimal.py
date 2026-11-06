"""Minimal, self-contained re-run of TWO ablations (Chapter 3 Sec. 3.11.7):
  ablation 5 "consequence tiers removed": every step is given the SAME tier k (k = 1, 2, 3, 4);
  ablation 4 "calibration removed": the uncalibrated probability p~ = sigmoid(s) replaces the calibrated
             p = sigmoid(gamma_1 s + gamma_0) in the expected-loss rule (Eq. 3.6).

It takes the frozen held-out probabilities of every recorded step (nested grouped cross-fit; nothing is
refitted) and re-runs REM's expected-loss decision (A3, step-level). Each ablation changes ONE element;
estimator, predicates, losses and folds are fixed. It reports observe-only intervention rates on attack
steps (y = 1) and legitimate steps (y = 0), which must equal Table 4.12.

usage (main environment, repository root):
  PILOT_RESULTS_DIR=<dir with state/crossfit.pkl, state/rmod.pkl> python3 experiments/pilot/ablation_minimal.py
No model call, no cost; about a minute. EXPLORATORY design values (pilot_e0), as everywhere in Chapter 4.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from data import build  # noqa: E402
from run_main import build_policies, load_state  # noqa: E402


def main():
    data = build("primary")
    fits, rmod = load_state("crossfit"), load_state("rmod")["rmod"]
    pol = build_policies(fits, rmod)
    p = fits["label_nll_primary"].p_cal                 # frozen held-out calibrated probabilities
    p_raw = fits["label_nll_primary"].p_raw             # same logits, without the calibration map
    y = np.asarray(data.y)
    tiers = [s.tier for s in data.steps]

    def intervention_rates(single_tier=None, probs=None):
        probs = p if probs is None else probs
        hit = []
        for i, s in enumerate(data.steps):
            k = tiers[i] if single_tier is None else single_tier
            d = pol[data.fold[i]]["A3_step_level"].decide(float(probs[i]), int(k), s.tool, s.available)
            hit.append(d.verdict.value != "allow")
        hit = np.asarray(hit)
        return hit[y == 1].mean(), hit[y == 0].mean()

    print(f"steps: {len(y)} (y=1: {int((y == 1).sum())}, y=0: {int((y == 0).sum())})")
    print(f"{'configuration':<28}{'intervene y=1':>15}{'intervene y=0':>15}")
    a, b = intervention_rates()
    print(f"{'full REM (own tiers)':<28}{a:>15.3f}{b:>15.3f}")
    for k in (1, 2, 3, 4):
        a, b = intervention_rates(k)
        print(f"{f'one tier for all = {k}':<28}{a:>15.3f}{b:>15.3f}")
    a, b = intervention_rates(probs=p_raw)
    print(f"{'calibration removed (p~)':<28}{a:>15.3f}{b:>15.3f}")


if __name__ == "__main__":
    main()
