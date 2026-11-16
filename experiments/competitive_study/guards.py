"""Decision arms of the competitive study (16 November 2026), behind one common authority front.

Status: [PROPOSED - EXPLORATORY - NOT PART OF THE APPROVED REM DESIGN]. The frozen REM core, the revision-3
compiler and matcher, the L4 arm and the direct-value constraint (HV) are imported unchanged.

Every arm built here has the same front and the same last step as HV:

  1. request-derived permission evidence, revision 3 (RuntimePermissionV3, unchanged);
  2. a restricted call that is denied, or whose authority is not established, is blocked. No score, cutoff
     or fitted quantity is consulted for it;
  3. the arm's decision rule for the remaining calls (below);
  4. the direct-value constraint of HV (value_guard.attach_direct_value_guard, unchanged), which can only
     turn a release into a refusal.

Decision rule for the remaining calls, by arm:

  GV      no learner: release (after the declared predicates D1/D2).
  HVx     the L4/HV rule, rebuilt here; must reproduce the stored HV outcomes exactly (equivalence check).
  HVnc    as HVx without the calibration map: p = sigmoid(s).
  HV4     as HVx with the four-verdict expected-loss rule; Modify and Escalate withhold (no reviewer).
  NPa     ridge score of the NP fit; release iff s < the NP umbrella cutoff (alpha = a/100, delta = 0.05).
  CRCa    ridge score of the CRC fit; release iff s < the conformal-risk-control cutoff (alpha = a/100).
  GB      gradient-boosted trees in place of the ridge estimator; same calibration and two-verdict rule.

No task identifier, injection identifier, label, reference solution or outcome is read here.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
for _p in ("experiments/improve_study", "experiments/g3_integration", "experiments/authz_study", "experiments/pilot"):
    sys.path.insert(0, str(ROOT / _p))

import study as S  # noqa: E402
from permission_v3 import DEFAULT_OPTS3, RuntimePermissionV3  # noqa: E402
from value_guard import attach_direct_value_guard  # noqa: E402
from rem.algorithms.a3 import A3Policy  # noqa: E402
from rem.algorithms.decision.loss_matrix import build_loss_grid  # noqa: E402
from rem.algorithms.detection.ridge_logistic import sigmoid  # noqa: E402
from rem.core.results import Verdict  # noqa: E402
from rem.integration.agentdojo_replay import GuardConfig, RemGuard  # noqa: E402

ARMS = ("GV", "HVx", "HVnc", "HV4", "NP05", "NP01", "CRC05", "CRC01", "GB")
FITTED = ("HVx", "HVnc", "HV4", "NP05", "NP01", "CRC05", "CRC01", "GB")          # arms with a fitted quantity (also replayed under S2)
THRESHOLD_ARMS = {"NP05": ("np", "0.05"), "NP01": ("np", "0.01"), "CRC05": ("crc", "0.05"), "CRC01": ("crc", "0.01")}


def _linear(rec, x):
    return rec["b0"] + sum(co * x[n] for n, co in zip(rec["order"], rec["coef"]))


def make_guard(arm, cell, extra, ep, st, value_guard=True):
    """cell: fitted cell of the integration package (reference, models, rmod); extra: this study's fits."""
    if arm not in ARMS:
        raise ValueError(f"unknown arm {arm}")
    gc = GuardConfig(st.spec, st.detector, cell["reference"], st.tier_map, st.restricted, "step_level", "no_reviewer")
    guard = RemGuard(gc, None, lambda c: (Verdict.ALLOW, "init", {}), st.labeler, ep)
    restricted = set(st.restricted)
    rp = RuntimePermissionV3(ep.objective, dict(DEFAULT_OPTS3))
    orig_ingest = guard.ingest

    def ingest(tool, text, executed):
        rp.on_ingest(executed)
        return orig_ingest(tool, text, executed)
    guard.ingest = ingest
    predicates = S.rm.predicates()
    grid = build_loss_grid(S.rm.loss_spec(cell["rmod"]), f"competitive study {arm}")
    pol2 = A3Policy(grid, predicates, tie_mode="record_chapter3_order", exclude_from_expected_loss=(Verdict.ESCALATE, Verdict.MODIFY))
    pol4 = A3Policy(grid, predicates, tie_mode="record_chapter3_order")
    ridge = cell["models"][("F4", "y")]

    def decide(c):
        is_r = c.tool in restricted
        ev = rp.evidence(guard.tracker, c.tool, c.args, c.tier)
        info = {"stage": "front"}
        if is_r and (ev.overall == "denied" or not ev.authority):
            v, src = Verdict.BLOCK, "permission_guard_authority_v3"
        else:
            f, avail = guard.tracker.features(c.tool, c.args)
            x = dict(f)
            x.update(ev.features())
            info["stage"] = "rule"
            if arm in ("HVx", "HVnc", "HV4"):
                s = _linear(ridge, x)
                p = float(sigmoid(ridge["g1"] * s + ridge["g0"])) if (arm != "HVnc" and not ridge["failed"]) else float(sigmoid(s))
                d = (pol4 if arm == "HV4" else pol2).decide(p, c.tier, c.tool, avail)
                v, src = d.verdict, d.source
                info.update(s=float(s), p=p)
            elif arm == "GB":
                g = extra["gb"]
                raw = float(np.ravel(g["clf"].decision_function(np.asarray([[x[n] for n in g["order"]]], dtype=float)))[0])
                p = float(sigmoid(g["g1"] * raw + g["g0"])) if not g["failed"] else float(sigmoid(raw))
                d = pol2.decide(p, c.tier, c.tool, avail)
                v, src = d.verdict, d.source
                info.update(s=raw, p=p)
            else:
                forced = predicates.evaluate(c.tool, c.tier, avail)
                if forced.verdict is not None:
                    v, src = forced.verdict, forced.source
                    info["stage"] = "predicate"
                elif not is_r:
                    v, src = Verdict.ALLOW, "cs_unrestricted_release"
                elif arm == "GV":
                    v, src = Verdict.ALLOW, "cs_guard_only"
                else:
                    kind, alpha = THRESHOLD_ARMS[arm]
                    rec = extra[kind]["rec"]
                    cut = extra[kind]["cut"][alpha]["cutoff"]
                    s = float(_linear(rec, x))
                    v, src = (Verdict.ALLOW if s < cut else Verdict.BLOCK), f"cs_{kind}_threshold"
                    info.update(s=s, cut=cut)
        det = {"perm": (ev.overall, ev.base.recipient, ev.base.amount, ev.effect, ev.binding, ev.condition, ev.fulfilment, ev.authority),
               "cs": info, "z": (0.0, 0.0)}
        rp.record(guard.tracker, c.tool, c.args)
        return v, src, det
    guard.decide = decide
    return attach_direct_value_guard(guard) if value_guard else guard
