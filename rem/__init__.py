"""REM — Runtime Evaluation and Mitigation Framework for Securing LLM-based AI Agents.

Implementation of the FROZEN design fixed by ``CLAUDE.md`` (REM Claude Code
Hard Design Lock). The frozen runtime pipeline is::

    provenance labeling
    -> context / behavioral / action evidence
    -> ridge logistic regression
    -> Platt calibration on the logit
    -> consequence tier
    -> policy predicates
    -> expected-loss Bayes verdict
    -> deterministic mitigation
    -> audit record

Architecture is exactly five layers (Input & Context, Detection, Behavioral
Analysis, Decision Engine, Mitigation), with offline fitting and recalibration
cross-cutting. There is no sixth layer and no feedback-loop layer.

Items that ``CLAUDE.md`` leaves unresolved (feature set, loss grid, consequence
tiers, ridge penalty, Modify mechanism, benchmark version) are fail-closed:
invoking them raises ``DesignNotSpecifiedError`` rather than defaulting.
"""

from rem.version import __version__

__all__ = ["__version__"]
