"""Exploratory G3 gate inside REM's decision layer; frozen components unchanged.

This adapter consumes request-derived permission evidence only. It never consults
evaluation labels or outcomes. Unknown is Escalate; this experiment has no reviewer.
"""
from __future__ import annotations

import dataclasses
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'experiments' / 'improve_study'))
from permission_v3 import RuntimePermissionV3
from rem.core.results import Verdict


def attach_permission_gate(guard, *, mode='strict', predicates=None):
    """Wrap an existing RemGuard in place, preserving its scorer and mitigation."""
    cfg = guard.config
    if mode not in ('strict', 'routed') or (mode == 'routed' and predicates is None):
        raise ValueError('Routing requires the declared REM predicates')
    if cfg.observe_only or cfg.mitigation_variant != 'step_level' or cfg.escalation_model != 'no_reviewer':
        raise ValueError('This exploratory adapter specifies step-level enforcement without a reviewer only')
    permission = RuntimePermissionV3(guard.episode.objective)
    restricted = frozenset(cfg.restricted_tools)
    base_decide, base_ingest, base_evaluate = guard.decide, guard.ingest, guard.evaluate
    if mode == 'routed':
        base_features = guard.tracker.features
        def features(tool, args):
            values, available = base_features(tool, args)
            evidence = permission.evidence(guard.tracker, tool, args, cfg.tier_map.tier(tool, args))
            return {**values, **evidence.features()}, available
        guard.tracker.features = features

    def decide(context):
        evidence = permission.evidence(guard.tracker, context.tool, context.args, context.tier)
        permission.record(guard.tracker, context.tool, context.args)
        extra = {'permission': dataclasses.asdict(evidence), 'rem_consulted': False}
        if context.tool in restricted and evidence.overall == 'denied':
            return Verdict.BLOCK, 'g3_denied', extra
        if context.tool in restricted and evidence.overall != 'supported' and (mode == 'strict' or not evidence.authority):
            return Verdict.ESCALATE, 'g3_unknown', extra
        if mode == 'routed':
            forced = predicates.evaluate(context.tool, context.tier, context.available)
            if forced.verdict is not None:
                return forced.verdict, forced.source, extra
            if context.tool in restricted and evidence.overall == 'supported':
                return Verdict.ALLOW, 'g3_supported', extra
        verdict, source, details = base_decide(context)
        return verdict, source, {**details, **extra, 'rem_consulted': True}

    def ingest(tool, text, executed):
        permission.on_ingest(executed)
        return base_ingest(tool, text, executed)

    def evaluate(tool, args):
        start = time.perf_counter()
        result = base_evaluate(tool, args)
        row = guard.audit[-1]
        if row['verdict_source'] in ('g3_denied', 'g3_unknown', 'g3_supported'):
            row['probability_used_for_verdict'] = False
            row['risk_table'] = 'not_applicable'
        elapsed = (time.perf_counter() - start) * 1000
        row['rem_latency_full_ms'] = elapsed
        guard.full_latencies_ms[-1] = elapsed
        return result

    guard.decide, guard.ingest, guard.evaluate = decide, ingest, evaluate
    guard.permission_gate = permission
    return guard
