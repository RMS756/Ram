"""REM-DiD guard: composes the five layers for one episode. Duck-typed to REM v1.0's RemGuard interface
(evaluate / ingest / begin_decision_point / audit / latencies_ms) so that the frozen replay harness can drive it.

REM v1.0 is used READ-ONLY as layer 4B: an inner, unmodified ``RemGuard`` computes the v1.0 features, calibrated
probability and expected-loss verdict for every call; its own release decision is ignored.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, FrozenSet, List, Mapping, Optional, Set, Tuple

from rem.core.results import Verdict

from .behavior import BehaviorMonitor
from .decision import SEVERITY, Rule, combine
from .detection import DetectorSuite, SegmentDetection, call_linked
from .enforcement import Gateway
from .provenance import SENSITIVE_FIELDS, STATE_CHANGING, LineageStatus, ProvenanceStore, UNTRUSTED
from .tae import AuthStatus, TAEStore

CONTROLS = ("AUTH", "PROV", "DET", "BEH", "LEARN", "ENF")


@dataclass(frozen=True)
class DidConfig:
    controls: FrozenSet[str]
    tae_mode: str = "oracle"                    # oracle | explicit | broad | none
    precedence: str = "strict"                  # strict | pinned_release
    reviewer: str = "none"                      # none | idealized (approves an Escalate iff reference label == 0)
    evade: FrozenSet[str] = frozenset()         # modelled test-time evasion of PROV/DET/BEH/LEARN on attack calls
    fail: FrozenSet[str] = frozenset()          # injected failures: DET PROV BEH LEARN AUTH TAE_STORE GATEWAY AUDIT
    fail_mode: str = "safe"                     # safe | open (counterfactual, to measure what fail-safe prevents)

    def __post_init__(self):
        assert set(self.controls) <= set(CONTROLS), self.controls
        assert self.tae_mode in ("oracle", "explicit", "broad", "none")
        assert self.precedence in ("strict", "pinned_release")
        assert self.fail_mode in ("safe", "open")


class DidGuard:
    def __init__(self, cfg: DidConfig, episode, labeler, store: Optional[TAEStore], inner_v1=None,
                 pattern_detector=None, gateway: Optional[Gateway] = None) -> None:
        self.cfg = cfg
        self.episode = episode
        self.labeler = labeler
        self.store = store
        self.inner = inner_v1
        self.session_id = episode.episode_id
        self.prov = ProvenanceStore(episode.objective, episode.system_prompt)
        fail = cfg.fail
        self.detectors = DetectorSuite(pattern_detector,
                                       failing=tuple(["D_pattern", "D_role", "D_override", "D_fin"]) if "DET" in fail else ())
        self.detections: Dict[int, SegmentDetection] = {}
        self.beh = BehaviorMonitor(self.prov, failing="BEH" in fail)
        self.gateway = gateway if gateway is not None else (Gateway(self.session_id, failing="GATEWAY" in fail)
                                                            if "ENF" in cfg.controls else None)
        if self.store is not None and "TAE_STORE" in fail:
            self.store.available = False
        self.decision_no = 0
        self.audit: List[Dict[str, Any]] = []
        self.latencies_ms: List[float] = []
        self.full_latencies_ms: List[float] = []
        self.last_permit = None

    # -- harness interface -------------------------------------------------------------------------
    def begin_decision_point(self) -> None:
        if self.inner is not None:
            self.inner.begin_decision_point()

    def ingest(self, tool: str, text: str, executed: bool) -> None:
        if self.inner is not None:
            self.inner.ingest(tool, text, executed)
        if not executed:
            return
        n0 = len(self.prov.segments)
        self.prov.add_tool_output(tool, text)
        for i in range(n0, len(self.prov.segments)):
            s = self.prov.segments[i]
            if s.source in UNTRUSTED:
                self.detections[i] = SegmentDetection(i, tuple(self.detectors.run(s.text)))

    def _unavailable(self, code: str, rules: List[Rule], layer: str) -> None:
        if self.cfg.fail_mode == "safe":
            rules.append(Rule(code, Verdict.ESCALATE, layer))

    def evaluate(self, tool: str, args: Mapping[str, Any]) -> Tuple[bool, str]:
        t0 = time.perf_counter()
        cfg, C = self.cfg, self.cfg.controls
        self.decision_no += 1
        label = self.labeler.label(self.episode.injection_task_id, tool, args)
        evading = label == 1
        sc = tool in STATE_CHANGING
        rules: List[Rule] = []
        info: Dict[str, Any] = {}

        # ---- 4B: frozen REM v1.0 (always run when present, to keep its episode history identical) ----
        v1 = None
        if self.inner is not None:
            self.inner.evaluate(tool, dict(args))
            rec = self.inner.audit[-1]
            v1 = Verdict(rec["verdict"])
            info["v1"] = {"verdict": v1.value, "p": rec["p"], "source": rec["verdict_source"],
                          "evaded_verdict": (rec.get("details") or {}).get("evaded_verdict")}

        # ---- 4A: deterministic authorization ----
        auth = None
        if "AUTH" in C and sc:
            if "AUTH" in cfg.fail:
                self._unavailable("AUTH_evaluator_unavailable", rules, "L4A")
            elif self.store is None:
                self._unavailable("AUTH_no_store", rules, "L4A")
            else:
                unchanged = {}
                if tool == "update_scheduled_transaction":
                    try:
                        unchanged = dict(self.prov.scheduled.get(int(args.get("id")), {}))
                    except Exception:
                        unchanged = {}
                auth = self.store.check(tool, args, self.decision_no, self.session_id, unchanged, consume=False)
                info["auth"] = {"status": auth.status.value, "reasons": list(auth.reasons), "pinned": list(auth.pinned)}
                if auth.status in (AuthStatus.VIOLATION, AuthStatus.NO_ENTRY):
                    rules.append(Rule(f"AUTH_{auth.status.value}", Verdict.BLOCK, "L4A"))
                elif auth.status is AuthStatus.UNSPECIFIED:
                    rules.append(Rule("AUTH_unspecified", Verdict.ESCALATE, "L4A"))
                elif auth.status is AuthStatus.UNVERIFIABLE:
                    if "TAE_STORE" in cfg.fail:      # infrastructure failure -> fail-safe handling
                        self._unavailable("AUTH_store_unavailable", rules, "L4A")
                    else:                            # tampered, expired, replayed, cross-session -> hard deny
                        rules.append(Rule("AUTH_unverifiable", Verdict.BLOCK, "L4A"))

        pinned = set(auth.pinned) if (auth is not None and auth.status is AuthStatus.AUTHORIZED) else set()
        present = [f for f, _ in SENSITIVE_FIELDS.get(tool, ()) if f in args and args[f] is not None]
        fully_pinned = bool(sc and auth is not None and auth.status is AuthStatus.AUTHORIZED and set(present) <= pinned)
        info["fully_pinned"] = fully_pinned

        # ---- L1 lineage (infrastructure for PROV and DET) ----
        lin = self.prov.call_lineage(tool, args) if sc else {}
        lin_free = {f: l for f, l in lin.items() if f not in pinned}
        info["lineage"] = {f: l.status.value for f, l in lin.items()}

        if sc and not fully_pinned:
            # ---- PROV ----
            if "PROV" in C:
                if "PROV" in cfg.fail:
                    self._unavailable("PROV_metadata_missing", rules, "L1")
                elif not ("PROV" in cfg.evade and evading):
                    for f, l in lin_free.items():
                        if l.kind in ("iban", "text", "id"):
                            if l.status is LineageStatus.UNTRUSTED:
                                rules.append(Rule(f"PROV_untrusted:{f}", Verdict.ESCALATE, "L1"))
                            elif l.status in (LineageStatus.MISSING, LineageStatus.UNPARSEABLE):
                                rules.append(Rule(f"PROV_missing:{f}", Verdict.ESCALATE, "L1"))
                        elif l.kind == "amount" and l.status is LineageStatus.UNTRUSTED:
                            rules.append(Rule("PROV_untrusted:amount", Verdict.ESCALATE, "L1"))
            # ---- DET ----
            if "DET" in C and not ("DET" in cfg.evade and evading):
                hit, why = call_linked(lin_free, self.detections)
                info["det"] = {"call_linked": hit, "why": list(why)}
                if hit is True:
                    rules.append(Rule("DET_call_linked", Verdict.ESCALATE, "L2"))
                elif hit is None:
                    self._unavailable("DET_unavailable", rules, "L2")
            # ---- BEH ----
            if "BEH" in C:
                fired, _ = self.beh.evaluate(tool, args, {l.canonical for f, l in lin.items() if f in pinned and l.kind == "iban"})
                if fired is None:
                    self._unavailable("BEH_unavailable", rules, "L3")
                elif not ("BEH" in cfg.evade and evading):
                    for r in fired:
                        rules.append(Rule(f"BEH_{r}", Verdict.ESCALATE, "L3"))
                    info["beh"] = list(fired)

        # ---- 4B rule ----
        if "LEARN" in C and not (cfg.precedence == "pinned_release" and fully_pinned):
            if "LEARN" in cfg.fail or v1 is None:
                if sc:
                    self._unavailable("LEARN_unavailable", rules, "L4B")
            elif "LEARN" in cfg.evade and evading:
                v_e = info["v1"].get("evaded_verdict")
                if v_e is not None:
                    rules.append(Rule("LEARN_v1_evaded", Verdict(v_e), "L4B"))
            else:
                rules.append(Rule(f"LEARN_v1:{info['v1']['source']}", v1, "L4B"))

        dec = combine(rules)
        verdict = dec.verdict
        # ---- L5 mitigation semantics ----
        if verdict is Verdict.ALLOW:
            release, notice, mech = True, "", "release"
        elif verdict is Verdict.ESCALATE:
            release = cfg.reviewer == "idealized" and label == 0
            notice = "" if release else "REM-DiD: withheld pending authenticated review (not approved)."
            mech = "escalate_approved" if release else "escalate_withheld"
        elif verdict is Verdict.MODIFY:
            release, notice, mech = False, "REM-DiD: withheld (v1.0 Modify semantics; no Modify mechanism declared).", "modify_withheld"
        else:
            release, notice, mech = False, "REM-DiD: blocked; not executed.", "block"
        if release and sc and auth is not None and auth.status is AuthStatus.AUTHORIZED:
            self.store.check(tool, args, self.decision_no, self.session_id,
                             unchanged=self.prov.scheduled.get(int(args["id"]), {}) if tool == "update_scheduled_transaction" and str(args.get("id", "")).isdigit() else {},
                             consume=True)
        self.last_permit = self.gateway.issue(tool, args, self.decision_no) if (release and self.gateway is not None) else None
        self.beh.record(tool, args, release)
        el = (time.perf_counter() - t0) * 1e3
        self.latencies_ms.append(el)
        self.full_latencies_ms.append(el)
        if "AUDIT" in cfg.fail and cfg.fail_mode == "safe" and release and sc:
            # audit failure: a state-changing call is not released without a durable audit record
            release, mech, notice = False, "audit_failure_withheld", "REM-DiD: audit unavailable; withheld."
            self.last_permit = None
        self.audit.append({
            "episode_id": self.episode.episode_id, "step": len(self.audit) + 1, "tool": tool, "label": label,
            "state_changing": sc, "verdict": verdict.value, "rules": [(r.code, r.verdict.value, r.layer) for r in dec.rules],
            "decisive": list(dec.sources), "mechanism": mech, "released": release, "info": info, "latency_ms": el,
        })
        return release, notice
