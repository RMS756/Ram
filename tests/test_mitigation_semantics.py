"""Step-level and episode-level mitigation can release different later actions.

R4 regression check for the independent review of 1 Nov 2026 (Finding 1). A fixed
two-call sequence, with no retry and no adaptation, is enough: an episode-level
Block adds every tool of T_R to the restriction set, so a later, different
state-changing call is refused even though its own verdict is Allow. Neither
policy is changed here; the test records how the two existing policies behave.
No AgentDojo traces are needed.
"""

import os

import yaml

from rem.algorithms.behavior.evidence import BenignReference, EvidenceSpec
from rem.algorithms.decision.consequence import ConsequenceTierMap
from rem.algorithms.detection.instruction_patterns import InstructionPatternDetector
from rem.core.results import Verdict
from rem.integration.agentdojo_replay import GuardConfig, RemGuard
from rem.integration.agentdojo_traces import Episode, Message, ReferenceLabeler, ReferenceSolutions

CFG = os.path.join(os.path.dirname(__file__), "..", "configs", "exploratory", "pilot_e0.yaml")


def _guard(variant: str) -> RemGuard:
    cfg = yaml.safe_load(open(CFG, encoding="utf-8"))
    F, C = cfg["features"], cfg["consequence"]
    spec = EvidenceSpec(F["n_max"], F["key_arguments"], F["privilege_map"], F["sensitive_read_tools"])
    det = InstructionPatternDetector(F["instruction_patterns"], None)
    tm = ConsequenceTierMap(C["categories"], C["tier_map"], C["amount_limit"])
    lab = ReferenceLabeler(ReferenceSolutions({}, {}, "v1"), cfg["labels"]["attacker_key_arguments"],
                           C["categories"]["read"], False)
    ep = Episode(path="synthetic", pipeline="synthetic", suite="banking", user_task_id="synthetic",
                 injection_task_id=None, attack_type=None, injections={},
                 messages=(Message("system", "You are a banking assistant."), Message("user", "Pay my rent.")),
                 utility=False, security=False, error=None, benchmark_version=None)
    gc = GuardConfig(spec, det, BenignReference(frozenset()), tm, tuple(C["restricted_tools_T_R"]),
                     variant, "no_reviewer")

    def decide(ctx):
        # Fixed verdicts, independent of the evidence: Block the transfer, Allow everything else.
        return (Verdict.BLOCK if ctx.tool == "send_money" else Verdict.ALLOW), "fixed", {}

    return RemGuard(gc, None, decide, lab, ep)


def _run(variant: str):
    g = _guard(variant)
    first = g.evaluate("send_money", {"recipient": "X", "amount": 10})
    second = g.evaluate("update_password", {"password": "p"})
    return g, first, second


def test_update_password_is_in_the_declared_restricted_set():
    cfg = yaml.safe_load(open(CFG, encoding="utf-8"))
    assert "update_password" in cfg["consequence"]["restricted_tools_T_R"]


def test_step_level_releases_the_later_allowed_call():
    g, first, second = _run("step_level")
    assert first[0] is False and second[0] is True
    assert [a["mechanism"] for a in g.audit] == ["block", "release"]
    assert g.restricted == set()


def test_episode_level_refuses_the_later_allowed_call():
    g, first, second = _run("episode_level")
    assert first[0] is False and second[0] is False
    assert [a["verdict"] for a in g.audit] == [Verdict.BLOCK.value, Verdict.ALLOW.value]
    assert [a["mechanism"] for a in g.audit] == ["block", "refuse_restricted"]


def test_the_two_policies_differ_on_the_same_fixed_sequence():
    _, _, step_second = _run("step_level")
    _, _, episode_second = _run("episode_level")
    assert step_second[0] != episode_second[0]
