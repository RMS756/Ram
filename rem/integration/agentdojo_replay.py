"""Recorded-trace replay with REM enforcement in AgentDojo (EXPLORATORY).

Method. A recorded episode is re-executed in AgentDojo's own sandbox: a replay
element emits the recorded assistant messages in order, AgentDojo's
``FunctionsRuntime`` executes the tool calls against a fresh banking
environment, and ``TaskSuite.run_task_with_pipeline`` computes the benchmark's
own utility and security checks. REM sits at the tool-execution boundary as a
guarded ``ToolsExecutor``: every proposed call is evaluated before execution
and every result is ingested on return (Chapter 3 Sec. 3.11.1).

Stated assumption (NO-ADAPT): the replayed agent does not adapt to a refusal;
it emits the calls it emitted in the recorded run. A real agent might retry or
take another route, so ASR under replay is a lower-bound-type estimate for
adaptive agents and must be reported with this assumption. No live LLM is
called (none is available in this environment).

Mitigation variants (SC-1, UNRESOLVED; both run, neither adopted):
  step_level     CLAUDE.md MITIGATION LOCK. Allow releases a_t; Block and
                 Escalate (when not approved) withhold a_t only. Modify applies
                 the one EXPLORATORY DECLARED mechanism "withhold a_t and
                 return a tool-restriction notice, with no persistence"; under
                 NO-ADAPT its environment effect equals a step-level Block.
  episode_level  Chapter 3 Table 3.14 / Algorithm 1 lines 29-33: a call to a
                 tool restricted in S is refused; Modify withholds a_t and adds
                 the tool class of a_t to S; Block withholds a_t and adds every
                 tool in T_R to S. "Tool class" is read as the Table 3.7 action
                 category of the tool (interpretation I-8).
Escalation (Chapter 3 Sec. 3.11.7): ``idealized`` releases a_t iff y_t = 0;
``no_reviewer`` treats every escalation as Block for a_t.

Sandbox only: every call runs against AgentDojo's simulated environment; REM
never initiates a call of its own.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Set, Tuple

import numpy as np

from rem.algorithms.attribution.linear_shapley import LinearShapleyAttributor
from rem.algorithms.behavior.evidence import BenignReference, EpisodeTracker, EvidenceSpec
from rem.algorithms.decision.consequence import ConsequenceTierMap
from rem.algorithms.detection.instruction_patterns import InstructionPatternDetector
from rem.algorithms.detection.ridge_logistic import sigmoid
from rem.core.audit import content_digest
from rem.core.results import Verdict
from rem.integration.agentdojo_traces import Episode, ReferenceLabeler

__all__ = [
    "FrozenScorer",
    "StepContext",
    "GuardConfig",
    "RemGuard",
    "ReplayOutcome",
    "replay_episode",
    "MITIGATION_VARIANTS",
    "ESCALATION_MODELS",
]

MITIGATION_VARIANTS = ("step_level", "episode_level")
ESCALATION_MODELS = ("idealized", "no_reviewer")


@dataclass(frozen=True)
class FrozenScorer:
    """Frozen fold parameters: s = b0 + b^T x, p = sigma(g1 s + g0).

    ``gamma_1 = 1, gamma_0 = 0`` is used only for the "calibration removed"
    ablation, where p~ enters Eq. 3.6.
    """

    feature_order: Tuple[str, ...]
    intercept: float
    coefficients: Tuple[float, ...]
    gamma_0: float
    gamma_1: float
    xbar: Tuple[float, ...]

    def __post_init__(self) -> None:
        if not self.gamma_1 > 0:
            raise ValueError("gamma_1 > 0 is required (monotone calibration).")

    def logit(self, feats: Mapping[str, float]) -> float:
        return self.intercept + sum(c * float(feats[n]) for n, c in zip(self.feature_order, self.coefficients))

    def attributor(self) -> LinearShapleyAttributor:
        return LinearShapleyAttributor(
            self.feature_order, self.coefficients, self.intercept, dict(zip(self.feature_order, self.xbar))
        )


@dataclass(frozen=True)
class StepContext:
    p: float
    p_raw: float
    logit: float
    tier: int
    tool: str
    args: Mapping[str, Any]
    available: Mapping[str, bool]
    label: int


#: decide(ctx) -> (verdict, source, details)
DecideFn = Callable[[StepContext], Tuple[Verdict, str, Mapping[str, Any]]]


@dataclass(frozen=True)
class GuardConfig:
    spec: EvidenceSpec
    detector: InstructionPatternDetector
    reference: BenignReference
    tier_map: ConsequenceTierMap
    restricted_tools: Tuple[str, ...]
    mitigation_variant: str
    escalation_model: str
    observe_only: bool = False
    single_tier: Optional[int] = None   # ablation 5: one tier for every action

    def __post_init__(self) -> None:
        if self.mitigation_variant not in MITIGATION_VARIANTS:
            raise ValueError(f"Unknown mitigation variant {self.mitigation_variant!r}.")
        if self.escalation_model not in ESCALATION_MODELS:
            raise ValueError(f"Unknown escalation model {self.escalation_model!r}.")


@dataclass
class RemGuard:
    """Per-episode REM state: tracker, restriction set S, audit records."""

    config: GuardConfig
    scorer: Optional[FrozenScorer]
    decide: DecideFn
    labeler: ReferenceLabeler
    episode: Episode
    tracker: EpisodeTracker = field(init=False)
    restricted: Set[str] = field(default_factory=set)
    audit: List[Dict[str, Any]] = field(default_factory=list)
    latencies_ms: List[float] = field(default_factory=list)
    _attr: Optional[LinearShapleyAttributor] = field(default=None, init=False)

    def __post_init__(self) -> None:
        self.tracker = EpisodeTracker(
            objective=self.episode.objective,
            trusted_texts=[self.episode.system_prompt],
            spec=self.config.spec,
            detector=self.config.detector,
            reference=self.config.reference,
        )
        if self.scorer is not None:
            self._attr = self.scorer.attributor()

    # -- per-step evaluation ---------------------------------------------------

    def evaluate(self, tool: str, args: Mapping[str, Any]) -> Tuple[bool, str]:
        """Return (release?, notice) for one proposed call and write its audit record."""
        t0 = time.perf_counter()
        cfg = self.config
        feats, avail = self.tracker.features(tool, args)
        tier = cfg.tier_map.tier(tool, args) if cfg.single_tier is None else int(cfg.single_tier)
        label = self.labeler.label(self.episode.injection_task_id, tool, args)
        if self.scorer is not None:
            s = self.scorer.logit(feats)
            p_raw = float(sigmoid(s))
            p = float(sigmoid(self.scorer.gamma_1 * s + self.scorer.gamma_0))
        else:
            s, p_raw, p = float("nan"), float("nan"), float("nan")
        ctx = StepContext(p, p_raw, s, tier, tool, dict(args), avail, label)
        verdict, source, details = self.decide(ctx)

        release, notice, mech = self._mitigate(verdict, tool, label)
        if cfg.observe_only:
            release, notice, mech = True, "", "observe_only_release"
        elapsed = (time.perf_counter() - t0) * 1e3
        self.latencies_ms.append(elapsed)

        phi = {}
        phi0 = None
        additivity = None
        if self._attr is not None:
            phi = {n: self._attr.shapley_value(i, feats[n]) for i, n in enumerate(self.scorer.feature_order)}
            phi0 = self._attr.base_value()
            additivity = abs(phi0 + sum(phi.values()) - s)
        forced = source in ("D1", "D2")
        self.audit.append(
            {
                "episode_id": self.episode.episode_id,
                "step": len(self.tracker.proposed) + 1,
                "decision_point": self.tracker.decision_point,
                "tool": tool,
                # Identity of the proposed action is kept even when it is not
                # released: digest only, raw argument values are not logged.
                "arguments_digest": content_digest(dict(args) or None),
                "argument_keys": sorted(args),
                "features": feats,
                "available": dict(avail),
                "logit": s,
                "p_raw": p_raw,
                "p": p,
                "tier": tier,
                "label": label,
                "verdict": verdict.value,
                "verdict_source": source,
                # When D1 or D2 fixes the verdict, p is computed for the record
                # but is not used, and no risk table exists (not applicable).
                "probability_used_for_verdict": not forced and source != "allow_all",
                "risk_table": (dict(details.get("risks", {})) if not forced else "not_applicable"),
                "details": dict(details),
                "mechanism": mech,
                "released": release,
                "restricted_after": sorted(self.restricted),
                "phi0": phi0,
                "phi": phi,
                "additivity_error": additivity,
                "rem_latency_ms": elapsed,
            }
        )
        self.tracker.record_proposal(tool, args)
        return release, notice

    def _mitigate(self, verdict: Verdict, tool: str, label: int) -> Tuple[bool, str, str]:
        cfg = self.config
        episode_level = cfg.mitigation_variant == "episode_level"
        if episode_level and tool in self.restricted:
            return False, f"REM: tool '{tool}' is restricted for the rest of this episode.", "refuse_restricted"
        if verdict is Verdict.ALLOW:
            return True, "", "release"
        if verdict is Verdict.ESCALATE:
            approved = cfg.escalation_model == "idealized" and label == 0
            if approved:
                return True, "", "escalate_approved"
            return False, "REM: this action was withheld pending human review and was not approved.", "escalate_withheld"
        if verdict is Verdict.MODIFY:
            if episode_level:
                category = cfg.tier_map.category_of(tool)
                cls = set(cfg.tier_map.categories[category]) & set(cfg.restricted_tools)
                self.restricted |= cls or {tool}
            return False, f"REM: tool '{tool}' is restricted; continue with the remaining tools.", "modify_tool_restriction"
        if verdict is Verdict.BLOCK:
            if episode_level:
                self.restricted |= set(cfg.restricted_tools)
            return False, "REM: this action was blocked and not executed.", "block"
        raise AssertionError(verdict)

    def ingest(self, tool: str, text: str, executed: bool) -> None:
        self.tracker.add_tool_result(tool, text, executed=executed)

    def begin_decision_point(self) -> None:
        self.tracker.begin_decision_point()


@dataclass
class ReplayOutcome:
    episode_id: str
    utility: bool
    security: bool
    recorded_utility: bool
    recorded_security: bool
    audit: List[Dict[str, Any]]
    latencies_ms: List[float]
    error: Optional[str] = None


def _agentdojo_elements():
    """Build the AgentDojo pipeline element classes lazily (optional dependency)."""
    from ast import literal_eval

    from agentdojo.agent_pipeline import AgentPipeline, InitQuery, SystemMessage, ToolsExecutionLoop, ToolsExecutor
    from agentdojo.agent_pipeline.base_pipeline_element import BasePipelineElement
    from agentdojo.agent_pipeline.tool_execution import is_string_list, tool_result_to_str
    from agentdojo.functions_runtime import FunctionCall
    from agentdojo.types import ChatToolResultMessage, text_content_block_from_string

    class ReplayLLM(BasePipelineElement):
        name = "rem_replay"

        def __init__(self, episode: Episode) -> None:
            self.rec = [m for m in episode.raw_messages if m.get("role") == "assistant"]
            self.i = 0

        def query(self, query, runtime, env, messages=[], extra_args={}):
            if self.i < len(self.rec):
                m = self.rec[self.i]
                self.i += 1
            else:
                m = {"role": "assistant", "content": "", "tool_calls": None}
            tcs = m.get("tool_calls")
            tcs = [FunctionCall(function=t["function"], args=dict(t["args"] or {}), id=t.get("id")) for t in tcs] if tcs else None
            content = m.get("content")
            if content is None or isinstance(content, str):
                content = [text_content_block_from_string(content)] if content is not None else None
            out = {"role": "assistant", "content": content, "tool_calls": tcs}
            return query, runtime, env, [*messages, out], extra_args

    class GuardedToolsExecutor(ToolsExecutor):
        """AgentDojo's ToolsExecutor with REM evaluating each call first."""

        def __init__(self, guard: RemGuard) -> None:
            super().__init__()
            self.guard = guard

        def query(self, query, runtime, env, messages=[], extra_args={}):
            if not messages or messages[-1]["role"] != "assistant" or not messages[-1]["tool_calls"]:
                return query, runtime, env, messages, extra_args
            self.guard.begin_decision_point()
            results = []
            names = {t.name for t in runtime.functions.values()}
            for call in messages[-1]["tool_calls"]:
                for k, v in call.args.items():
                    if isinstance(v, str) and is_string_list(v):
                        call.args[k] = literal_eval(v)
                if call.function not in names:
                    err = f"Invalid tool {call.function} provided."
                    results.append(ChatToolResultMessage(role="tool", content=[text_content_block_from_string("")],
                                                         tool_call_id=call.id, tool_call=call, error=err))
                    self.guard.ingest(call.function, "", executed=False)
                    continue
                release, notice = self.guard.evaluate(call.function, dict(call.args))
                if release:
                    res, err = runtime.run_function(env, call.function, call.args)
                    text = self.output_formatter(res)
                    executed = err is None
                else:
                    text, err, executed = "", notice, False
                results.append(ChatToolResultMessage(role="tool", content=[text_content_block_from_string(text)],
                                                     tool_call_id=call.id, tool_call=call, error=err))
                self.guard.ingest(call.function, text if executed else (err or ""), executed=executed)
            return query, runtime, env, [*messages, *results], extra_args

    return AgentPipeline, SystemMessage, InitQuery, ToolsExecutionLoop, ReplayLLM, GuardedToolsExecutor


def replay_episode(episode: Episode, suite: Any, guard: RemGuard) -> ReplayOutcome:
    """Re-execute ``episode`` in ``suite`` with ``guard`` at the tool boundary."""
    AgentPipeline, SystemMessage, InitQuery, ToolsExecutionLoop, ReplayLLM, Guarded = _agentdojo_elements()
    llm = ReplayLLM(episode)
    pipe = AgentPipeline(
        [SystemMessage(episode.system_prompt), InitQuery(), llm, ToolsExecutionLoop([Guarded(guard), llm])]
    )
    pipe.name = "rem_replay"
    ut = suite.get_user_task_by_id(episode.user_task_id)
    it = suite.get_injection_task_by_id(episode.injection_task_id) if episode.injection_task_id else None
    err = None
    try:
        utility, security = suite.run_task_with_pipeline(pipe, ut, it, dict(episode.injections))
    except Exception as exc:  # recorded as an error, never silently dropped
        utility, security, err = False, False, repr(exc)[:300]
    return ReplayOutcome(
        episode_id=episode.episode_id,
        utility=bool(utility),
        security=bool(security),
        recorded_utility=episode.utility,
        recorded_security=episode.security,
        audit=guard.audit,
        latencies_ms=guard.latencies_ms,
        error=err,
    )
