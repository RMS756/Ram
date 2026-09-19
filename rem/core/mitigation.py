"""Deterministic mitigation — L5, canonical semantics.

``CLAUDE.md`` § MITIGATION LOCK fixes the meaning of each verdict::

    Allow:    release the current action.
    Modify:   apply ONE declared modification mechanism to the current action
              or execution context.
    Escalate: withhold the current action pending review.
    Block:    prevent execution of the current proposed action.

    Do NOT silently redefine Block as disabling all state-changing tools for
    the rest of the episode.
    Do NOT silently redefine Modify as removing a tool class for the rest of
    the episode.
    Any episode-level restriction is a separate experimental policy requiring
    explicit specification.

The verdict-to-mechanism mapping is therefore **not configurable**: it is part
of the frozen design. Only the Modify mechanism is a free choice, and it is
unresolved, so the engine refuses to construct one.

Mitigation is enforcement, not inference. This module contains no mathematics
and never decides whether something is malicious.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Any, Callable, Mapping, Optional

from rem.agent.trajectory import TrajectoryStep
from rem.core.interfaces import DesignNotSpecifiedError, MitigationEngine
from rem.core.results import Decision, MitigationAction, MitigationOutcome, Verdict

__all__ = ["CANONICAL_MECHANISM", "DeterministicMitigationEngine"]

#: The frozen verdict-to-mechanism mapping. Immutable by construction, because
#: changing it would redefine the mitigation semantics fixed by the contract.
CANONICAL_MECHANISM: Mapping[Verdict, MitigationAction] = MappingProxyType(
    {
        Verdict.ALLOW: MitigationAction.RELEASE_ACTION,
        Verdict.MODIFY: MitigationAction.MODIFY_ACTION,
        Verdict.ESCALATE: MitigationAction.WITHHOLD_PENDING_REVIEW,
        Verdict.BLOCK: MitigationAction.PREVENT_EXECUTION,
    }
)


class DeterministicMitigationEngine(MitigationEngine):
    """Applies the canonical mechanism for a verdict, at step level.

    Args:
        modification_mechanism: The ONE declared modification applied under the
            Modify verdict, as a callable ``(step) -> replacement``. Unresolved
            in the design, so ``None`` means a Modify verdict is a blocked
            condition rather than a silently skipped one.
        modification_name: Human-readable name of that mechanism, for audit.
    """

    name = "deterministic_mitigation"

    def __init__(
        self,
        *,
        modification_mechanism: Optional[Callable[[TrajectoryStep], Any]] = None,
        modification_name: str = "",
    ) -> None:
        self.modification_mechanism = modification_mechanism
        self.modification_name = modification_name

    def apply(self, decision: Decision, step: TrajectoryStep) -> MitigationOutcome:
        """Apply the canonical mechanism for ``decision`` to ``step``.

        Args:
            decision: The verdict to enforce.
            step: The step being mitigated; mutated in place when the mechanism
                changes what the agent may do.

        Returns:
            The outcome, also attached to ``step.mitigation``.

        Raises:
            DesignNotSpecifiedError: On a Modify verdict with no declared
                modification mechanism.
        """
        action = CANONICAL_MECHANISM[decision.verdict]
        outcome = self._dispatch(action, step)
        step.mitigation = outcome
        return outcome

    def _dispatch(
        self, action: MitigationAction, step: TrajectoryStep
    ) -> MitigationOutcome:
        if action is MitigationAction.RELEASE_ACTION:
            return MitigationOutcome(
                action,
                applied=False,
                producer=self.name,
                detail="Allow: current action released unchanged.",
            )

        if action is MitigationAction.PREVENT_EXECUTION:
            target = step.tool_call.name if step.tool_call else (step.action or "step")
            step.tool_call = None
            step.action = None
            step.metadata["rem_blocked_step"] = True
            return MitigationOutcome(
                action,
                applied=True,
                producer=self.name,
                detail=(
                    f"Block: prevented execution of {target!r} at this step. "
                    "Step-level only; no episode-level restriction applied."
                ),
            )

        if action is MitigationAction.WITHHOLD_PENDING_REVIEW:
            step.metadata["rem_awaiting_review"] = True
            return MitigationOutcome(
                action,
                applied=True,
                producer=self.name,
                detail="Escalate: current action withheld pending review.",
            )

        if action is MitigationAction.MODIFY_ACTION:
            if self.modification_mechanism is None:
                raise DesignNotSpecifiedError(
                    self.name,
                    "the ONE declared Modify mechanism (listed as unresolved in "
                    "CLAUDE.md DATA / EVALUATION LOCK). Rewriting an agent "
                    "action changes system behaviour and may not be improvised",
                )
            replacement = self.modification_mechanism(step)
            step.metadata["rem_modified_step"] = True
            return MitigationOutcome(
                action,
                applied=True,
                producer=self.name,
                detail=(
                    "Modify: applied the declared mechanism "
                    f"{self.modification_name or '<unnamed>'!r} to the current "
                    "action. Step-level only; no tool class removed."
                ),
                replacement=replacement,
            )

        raise AssertionError(f"Unhandled canonical mechanism: {action!r}")
