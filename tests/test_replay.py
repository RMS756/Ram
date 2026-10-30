"""Replay harness against the real AgentDojo sandbox (skipped if unavailable)."""

import os

import pytest

agentdojo = pytest.importorskip("agentdojo")

from agentdojo.task_suite.load_suites import get_suites  # noqa: E402

from rem.algorithms.behavior.evidence import BenignReference, EvidenceSpec  # noqa: E402
from rem.algorithms.decision.consequence import ConsequenceTierMap  # noqa: E402
from rem.algorithms.detection.instruction_patterns import InstructionPatternDetector  # noqa: E402
import yaml  # noqa: E402
from rem.core.results import Verdict  # noqa: E402
from rem.integration.agentdojo_replay import GuardConfig, RemGuard, replay_episode  # noqa: E402
from rem.integration.agentdojo_traces import ReferenceLabeler, ReferenceSolutions, load_episode  # noqa: E402

RUNS = os.environ.get("AGENTDOJO_RUNS", "/home/user/ethz-spylab/agentdojo/runs")
TRACE = os.path.join(RUNS, "gpt-4o-2024-05-13/banking/user_task_0/important_instructions/injection_task_0.json")
CFG = os.path.join(os.path.dirname(__file__), "..", "configs", "exploratory", "pilot_e0.yaml")

pytestmark = pytest.mark.skipif(not os.path.isfile(TRACE), reason="AgentDojo recorded runs not available")


def _setup():
    cfg = yaml.safe_load(open(CFG, encoding="utf-8"))
    F, C = cfg["features"], cfg["consequence"]
    suite = get_suites("v1")["banking"]
    spec = EvidenceSpec(F["n_max"], F["key_arguments"], F["privilege_map"], F["sensitive_read_tools"])
    det = InstructionPatternDetector(F["instruction_patterns"], [t.name for t in suite.tools])
    tm = ConsequenceTierMap(C["categories"], C["tier_map"], C["amount_limit"])
    lab = ReferenceLabeler(ReferenceSolutions.from_agentdojo("v1", "banking"),
                           cfg["labels"]["attacker_key_arguments"], C["categories"]["read"], False)
    return suite, spec, det, tm, lab, tuple(C["restricted_tools_T_R"])


@pytest.mark.parametrize("variant", ["step_level", "episode_level"])
def test_allow_all_reproduces_record_and_oracle_block_prevents_attack(variant):
    suite, spec, det, tm, lab, tr = _setup()
    ep = load_episode(TRACE)
    assert ep.security  # the recorded attack succeeded
    gc = GuardConfig(spec, det, BenignReference(frozenset()), tm, tr, variant, "no_reviewer")
    allow = replay_episode(ep, suite, RemGuard(gc, None, lambda c: (Verdict.ALLOW, "allow", {}), lab, ep))
    assert (allow.utility, allow.security) == (ep.utility, ep.security)
    block = replay_episode(
        ep, suite,
        RemGuard(gc, None, lambda c: ((Verdict.BLOCK if c.label else Verdict.ALLOW), "oracle", {}), lab, ep),
    )
    assert block.security is False
    blocked = [a for a in block.audit if a["label"] == 1 and not a["released"]]
    assert blocked
    # R2: the withheld action keeps its identity in the audit record (digest only).
    assert all(a["tool"] and a["arguments_digest"] and a["argument_keys"] for a in blocked)
    assert all("new_password" not in str(a) and "US133000000121212121212" not in str(a) for a in block.audit)


def test_observe_only_releases_everything():
    suite, spec, det, tm, lab, tr = _setup()
    ep = load_episode(TRACE)
    gc = GuardConfig(spec, det, BenignReference(frozenset()), tm, tr, "episode_level", "no_reviewer", observe_only=True)
    out = replay_episode(ep, suite, RemGuard(gc, None, lambda c: (Verdict.BLOCK, "x", {}), lab, ep))
    assert out.security == ep.security and all(a["released"] for a in out.audit)
