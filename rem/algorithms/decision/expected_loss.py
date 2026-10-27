"""Expected-loss Bayes verdict — the FROZEN decision rule (L4 Decision Engine).

``CLAUDE.md`` § MATHEMATICAL LOCK → Decision::

    Conditional risk:

    R_t(v) = (1-p_t)L(v,0,k_t) + p_t L(v,1,k_t)

    Verdict:

    v*_t = argmin_v R_t(v)

    The four REM actions are an adaptation of cost-sensitive expected-loss
    decision theory.

    Elkan supports the expected-cost decision principle.
    Chow is conceptual support for reject/abstain-style escalation.

    Neither source may be presented as having invented REM's four-action
    architecture.

Purpose
    Select one of {Allow, Modify, Escalate, Block} by minimising conditional
    risk under the calibrated probability and the step's consequence tier.

Input
    ``p_t`` (calibrated), ``k_t`` (consequence tier), policy predicate outcomes.

Output
    A :class:`~rem.core.results.Decision` carrying the verdict and the full
    ``R_t(v)`` table, so the argmin can be re-checked from the audit record.

Mathematical foundation
    Frozen above. The rule is the standard Bayes decision rule under a loss
    function: choose the action minimising expected loss with respect to the
    posterior over the true label.

Academic reference
    Frozen equations: ``CLAUDE.md`` § MATHEMATICAL LOCK.
    Expected-cost decision principle: Elkan, C. (2001). "The Foundations of
    Cost-Sensitive Learning." *IJCAI 2001*, pp. 973–978.
    Reject/abstain tradeoff (conceptual support for Escalate): Chow, C. K.
    (1970). "On Optimum Recognition Error and Reject Tradeoff." *IEEE
    Transactions on Information Theory*, 16(1), 41–46.

Equation ID
    NOT ASSIGNED — see ``CLAUDE.md`` § EQUATION-ID LOCK.

Assumptions
    ``p_t`` is a calibrated probability of the positive (attack) class, and the
    loss grid is complete over {verdict} x {0,1} x {tiers in use}.

Limitations
    The **loss values / loss grid** and the **consequence tiers** are
    unresolved (``CLAUDE.md`` § DATA / EVALUATION LOCK). Without them no verdict
    can be produced, and this engine refuses to construct a default. The
    tie-breaking rule for an exact argmin tie is likewise not frozen, so ties
    raise rather than resolving arbitrarily.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional, Tuple

from rem.agent.trajectory import Trajectory, TrajectoryStep
from rem.core.interfaces import DecisionEngine, DesignNotSpecifiedError
from rem.core.results import AttributionResult, Decision, DetectionResult, Verdict
from rem.traceability.registry import derivation

__all__ = ["LossGrid", "ExpectedLossDecisionEngine", "VerdictTieError"]

_FROZEN_SOURCE = (
    "CLAUDE.md, MATHEMATICAL LOCK -> Decision (frozen specification). "
    "Expected-cost decision principle: Elkan, C. (2001), 'The Foundations of "
    "Cost-Sensitive Learning', IJCAI 2001, pp. 973-978. Reject/abstain "
    "tradeoff: Chow, C. K. (1970), 'On Optimum Recognition Error and Reject "
    "Tradeoff', IEEE Trans. Information Theory, 16(1), 41-46. Neither source "
    "invented REM's four-action architecture."
)


class VerdictTieError(RuntimeError):
    """Raised when two or more verdicts attain the minimum conditional risk.

    No tie-breaking rule is frozen. Picking one silently would be an invented
    decision policy, so REM stops instead.
    """


@dataclass(frozen=True)
class LossGrid:
    """The loss function ``L(v, y, k)``.

    Attributes:
        values: Mapping from ``(verdict, true_label, consequence_tier)`` to loss.
        source: Where these values come from. Required — an unsourced loss grid
            silently *is* REM's decision policy.

    Raises:
        ValueError: If ``source`` is empty, ``values`` is empty, or the grid is
            incomplete for any tier it mentions.
    """

    values: Mapping[Tuple[Verdict, int, Any], float]
    source: str

    def __post_init__(self) -> None:
        if not str(self.source).strip():
            raise ValueError(
                "A loss grid must declare its source. The loss values are the "
                "only free quantities in the frozen decision layer, so an "
                "unsourced grid is an invented decision policy."
            )
        if not self.values:
            raise ValueError("A loss grid may not be empty.")
        for key in self.values:
            if len(key) != 3:
                raise ValueError(f"Loss grid key {key!r} must be (verdict, label, tier).")
            verdict, label, _tier = key
            if not isinstance(verdict, Verdict):
                raise ValueError(f"Loss grid key {key!r} has a non-Verdict verdict.")
            if label not in (0, 1):
                raise ValueError(f"Loss grid key {key!r} has a label outside {{0, 1}}.")
        # Completeness: every tier mentioned must cover all verdicts x {0,1}.
        for tier in self.tiers():
            for verdict in Verdict:
                for label in (0, 1):
                    if (verdict, label, tier) not in self.values:
                        raise ValueError(
                            f"Loss grid is incomplete: no entry for verdict "
                            f"{verdict.value!r}, label {label}, tier {tier!r}. "
                            "REM does not infer missing losses."
                        )

    def tiers(self) -> Tuple[Any, ...]:
        """Consequence tiers this grid covers."""
        seen: list[Any] = []
        for _verdict, _label, tier in self.values:
            if tier not in seen:
                seen.append(tier)
        return tuple(seen)

    def loss(self, verdict: Verdict, label: int, tier: Any) -> float:
        """Return ``L(verdict, label, tier)``.

        Raises:
            DesignNotSpecifiedError: If the combination is absent.
        """
        try:
            return float(self.values[(verdict, label, tier)])
        except KeyError:
            raise DesignNotSpecifiedError(
                "loss_grid",
                f"the loss L({verdict.value}, {label}, {tier!r}) — the supplied "
                "grid does not cover this consequence tier",
            ) from None


class ExpectedLossDecisionEngine(DecisionEngine):
    """The frozen REM decision engine.

    Args:
        loss_grid: The loss function ``L``. There is deliberately no default.
        predicate_policy: How policy predicates modify the verdict. The frozen
            pipeline names policy predicates but never defines them, so this is
            unresolved; supplying ``None`` means a firing predicate is a blocked
            condition rather than a silently ignored one.

    Raises:
        DesignNotSpecifiedError: If ``loss_grid`` is ``None``.
    """

    name = "expected_loss_bayes"

    def __init__(
        self,
        loss_grid: Optional[LossGrid] = None,
        *,
        predicate_policy: Optional[Any] = None,
    ) -> None:
        if loss_grid is None:
            raise DesignNotSpecifiedError(
                self.name,
                "the loss grid L(v, y, k) and the consequence tiers k_t (listed "
                "as unresolved in CLAUDE.md DATA / EVALUATION LOCK)",
            )
        self.loss_grid = loss_grid
        self.predicate_policy = predicate_policy

    @derivation(
        statement="R_t(v) = (1 - p_t) * L(v, 0, k_t) + p_t * L(v, 1, k_t)",
        algorithm="Cost-sensitive expected-loss (Bayes) decision rule",
        source=_FROZEN_SOURCE,
        location="CLAUDE.md, MATHEMATICAL LOCK -> Decision (conditional risk).",
        notes=(
            "p_t must be the calibrated probability from Platt-on-logit. The "
            "posterior over the true label is (1 - p_t, p_t)."
        ),
    )
    def conditional_risk(
        self, verdict: Verdict, calibrated_probability: float, tier: Any
    ) -> float:
        """Compute ``R_t(v)`` for one verdict.

        Args:
            verdict: The candidate action.
            calibrated_probability: ``p_t``.
            tier: ``k_t``.

        Returns:
            The conditional risk.

        Raises:
            ValueError: If ``p_t`` lies outside [0, 1].
        """
        p = float(calibrated_probability)
        if not 0.0 <= p <= 1.0:
            raise ValueError(f"p_t must lie in [0, 1]; got {p}.")
        return (1.0 - p) * self.loss_grid.loss(verdict, 0, tier) + p * self.loss_grid.loss(
            verdict, 1, tier
        )

    @derivation(
        statement="v*_t = argmin_v R_t(v)",
        algorithm="Cost-sensitive expected-loss (Bayes) decision rule",
        source=_FROZEN_SOURCE,
        location="CLAUDE.md, MATHEMATICAL LOCK -> Decision (verdict).",
        notes=(
            "Minimised over exactly the four frozen verdicts. No tie-breaking "
            "rule is frozen, so an exact tie raises VerdictTieError rather than "
            "resolving arbitrarily."
        ),
    )
    def argmin_verdict(
        self, calibrated_probability: float, tier: Any
    ) -> Tuple[Verdict, Dict[str, float]]:
        """Select the minimum-risk verdict.

        Args:
            calibrated_probability: ``p_t``.
            tier: ``k_t``.

        Returns:
            The chosen verdict and the full risk table.

        Raises:
            VerdictTieError: If two or more verdicts attain the minimum.
        """
        risks = {
            verdict: self.conditional_risk(verdict, calibrated_probability, tier)
            for verdict in Verdict
        }
        minimum = min(risks.values())
        winners = [verdict for verdict, risk in risks.items() if risk == minimum]
        if len(winners) > 1:
            raise VerdictTieError(
                "Verdicts "
                + ", ".join(sorted(v.value for v in winners))
                + f" all attain the minimum conditional risk {minimum!r} at "
                f"p_t={calibrated_probability!r}, k_t={tier!r}. No tie-breaking "
                "rule is frozen in the REM design, so REM will not choose one."
            )
        return winners[0], {verdict.value: risk for verdict, risk in risks.items()}

    def decide(
        self,
        detection: DetectionResult,
        consequence_tier: Any,
        predicates: Mapping[str, bool],
        step: TrajectoryStep,
    ) -> Decision:
        """Return the verdict for ``step``.

        Args:
            detection: The calibrated detection result.
            consequence_tier: ``k_t``.
            predicates: Policy predicate outcomes.
            step: The step being decided.

        Returns:
            The decision, with the full risk table attached.

        Raises:
            TypeError: If ``detection`` is not calibrated, or if an attribution
                result is passed in — attribution is audit-only.
            DesignNotSpecifiedError: If ``consequence_tier`` is ``None``, or if a
                policy predicate fires while the predicate policy is unresolved.
        """
        if isinstance(detection, AttributionResult) or getattr(
            detection, "audit_only", False
        ):
            raise TypeError(
                "Attribution output reached the decision engine. Linear Shapley "
                "attribution is audit-only and MUST NOT affect the verdict "
                "(CLAUDE.md MATHEMATICAL LOCK; SHAP as a decision input is a "
                "forbidden reintroduction)."
            )
        # Raises TypeError unless the score came through Platt calibration.
        p_t = detection.calibrated_probability

        if consequence_tier is None:
            raise DesignNotSpecifiedError(
                self.name,
                "the consequence tier k_t for this step (listed as unresolved in "
                "CLAUDE.md DATA / EVALUATION LOCK)",
            )

        firing = sorted(name for name, fired in (predicates or {}).items() if fired)
        if firing and self.predicate_policy is None:
            raise DesignNotSpecifiedError(
                self.name,
                "the policy-predicate semantics — predicate(s) "
                f"{firing} fired, but the frozen pipeline names policy "
                "predicates without defining what they do. Ignoring a firing "
                "predicate would silently drop a policy control",
            )

        verdict, risks = self.argmin_verdict(p_t, consequence_tier)
        return Decision(
            verdict=verdict,
            producer=self.name,
            rationale=(
                f"argmin_v R_t(v) with p_t={p_t:.6g}, k_t={consequence_tier!r}; "
                f"R={{" + ", ".join(f"{k}: {v:.6g}" for k, v in risks.items()) + "}"
            ),
            conditional_risk=risks,
            calibrated_probability=p_t,
            consequence_tier=consequence_tier,
            source=_FROZEN_SOURCE,
        )
