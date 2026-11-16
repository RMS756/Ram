"""Section 11 addendum arms (16 November 2026). The frozen guards.py is not modified.

  GVc   GV with the release decision of every restricted call taken by Cedar policies over the context that
        REM computes (cedar_front.py). Policy-engine implementation study: expected to be call-for-call
        identical to GV.
  GVp   GV plus one provenance rule: a restricted call that passes the front but whose value the request does
        not confirm (status 'unknown') is released only if REM's provenance indicator is available and does
        not fire, i.e. no key argument of the call occurs in untrusted content without also occurring in
        trusted content. Otherwise the call is withheld (Escalate; no reviewer). Calls whose value the request
        confirms or delegates (status 'supported') are unaffected: external content may supply data inside a
        workflow the request authorizes, and may not supply values otherwise.

The provenance indicator is REM's own x_act1 (frozen core): trust is assigned by the harness from the role of
each message, never from its text; origin is established by typed value matching, not by data-flow tracking.
"""
from __future__ import annotations

import guards as G
import cedar_front as CF
from intent_v3 import compile_intent_v3
from intent import canon_iban
from value_guard import value_verdict

S, Verdict = G.S, G.Verdict
ARMS = ("GVc", "GVp")


def make_guard(arm, cell, extra, ep, st):
    if arm not in ARMS:
        raise ValueError(arm)
    gc = G.GuardConfig(st.spec, st.detector, cell["reference"], st.tier_map, st.restricted, "step_level", "no_reviewer")
    guard = G.RemGuard(gc, None, lambda c: (Verdict.ALLOW, "init", {}), st.labeler, ep)
    restricted = set(st.restricted)
    rp = G.RuntimePermissionV3(ep.objective, dict(G.DEFAULT_OPTS3))
    intent3 = compile_intent_v3(ep.objective)
    predicates = S.rm.predicates()
    orig_ingest = guard.ingest

    def ingest(tool, text, executed):
        rp.on_ingest(executed)
        return orig_ingest(tool, text, executed)
    guard.ingest = ingest

    def decide(c):
        is_r = c.tool in restricted
        ev = rp.evidence(guard.tracker, c.tool, c.args, c.tier)
        f, avail = guard.tracker.features(c.tool, c.args)
        forced = predicates.evaluate(c.tool, c.tier, avail)
        info = {"stage": "front"}
        if arm == "GVp":
            if is_r and (ev.overall == "denied" or not ev.authority):
                v, src = Verdict.BLOCK, "permission_guard_authority_v3"
            elif forced.verdict is not None:
                v, src, info["stage"] = forced.verdict, forced.source, "predicate"
            elif not is_r:
                v, src, info["stage"] = Verdict.ALLOW, "cs_unrestricted_release", "rule"
            elif ev.overall != "supported" and not avail.get("x_act1", True):
                v, src, info["stage"] = Verdict.ESCALATE, "cs_provenance_unavailable", "rule"
            elif ev.overall != "supported" and f["x_act1"] == 1:
                v, src, info["stage"] = Verdict.ESCALATE, "cs_provenance_untrusted_value", "rule"
            else:
                v, src, info["stage"] = Verdict.ALLOW, "cs_guard_only", "rule"
        else:                                                   # GVc
            if not is_r:
                if forced.verdict is not None:
                    v, src, info["stage"] = forced.verdict, forced.source, "predicate"
                else:
                    v, src, info["stage"] = Verdict.ALLOW, "cs_unrestricted_release", "rule"
            else:
                dv = value_verdict(intent3, c.tool, c.args)
                ctx = {"authority": bool(ev.authority), "overall": ev.overall, "perm_effect": ev.effect, "binding": ev.binding,
                       "condition": ev.condition, "fulfilment": ev.fulfilment,
                       "direct_value": "ok" if dv is None else ("ambiguous" if dv is Verdict.ESCALATE else "mismatch"),
                       "predicate": "none" if forced.verdict is None else str(forced.source)}
                rid = canon_iban((c.args or {}).get("recipient")) if isinstance((c.args or {}).get("recipient"), str) else None
                allowed, decision, reasons, errors = CF.authorize(c.tool, rid or "none", ctx)
                v = Verdict.ALLOW if allowed else Verdict.BLOCK
                src = "cedar_allow" if allowed else "cedar_deny"
                info.update(stage="cedar", decision=decision, reasons=sorted(reasons), errors=errors, context=ctx)
        det = {"perm": (ev.overall, ev.base.recipient, ev.base.amount, ev.effect, ev.binding, ev.condition, ev.fulfilment, ev.authority),
               "cs": info, "z": (0.0, 0.0)}
        rp.record(guard.tracker, c.tool, c.args)
        return v, src, det
    guard.decide = decide
    return G.attach_direct_value_guard(guard) if arm == "GVp" else guard
