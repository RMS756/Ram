"""Regression tests of the follow-up (revision 2) of the improvement study: instruction bindings, conditions,
fulfillment and idempotency, the authority split used by the learned guard, typed provenance, and label
isolation. The frozen v1 behaviour on the same probes is asserted too, so that the defects stay documented."""
from __future__ import annotations

import ast
import inspect
import os
import sys
from decimal import Decimal
from types import SimpleNamespace

import pytest

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO, "experiments", "improve_study"))
import intent as IN  # noqa: E402
import intent_v2 as I2  # noqa: E402
import permission as PM  # noqa: E402
import permission_v2 as P2  # noqa: E402

A, B, C = "ZK52390800003316720548", "QB71046600002985413307", "PL61109010140000071219812874"


def pay(r, a):
    return {"recipient": r, "amount": a, "subject": "payment", "date": "2026-11-14"}


def v2(g, hist, tool, args, tier=2, **opts):
    o = dict(P2.DEFAULT_OPTS2)
    o.update(opts)
    return P2.evaluate_v2(I2.compile_intent_v2(g), g, hist, tool, args, tier, o)


def v1(g, hist, tool, args, tier=2):
    return PM.evaluate(IN.compile_intent(g), g, hist, tool, args, tier, PM.DEFAULT_OPTS).overall


BAL = lambda x: [("get_balance", {}, x, True)]


# ------------------------------------------------------------------ C1: bindings
MULTI = f"Send 50 to {A} and 100 to {B}."


@pytest.mark.parametrize("rec,amt,ok", [(A, 50, True), (B, 100, True), (A, 100, False), (B, 50, False)])
def test_multi_payment_calls_must_match_one_instruction(rec, amt, ok):
    e = v2(MULTI, [], "send_money", pay(rec, amt))
    assert (e.overall == "supported") is ok
    if not ok:
        assert e.binding == "contradicted" and e.overall == "denied"
    assert v1(MULTI, [], "send_money", pay(rec, amt)) == "supported"     # the frozen v1 defect


def test_swapped_operands_and_reformatted_identifiers_bind_the_same_way():
    spaced = " ".join(A[i:i + 4] for i in range(0, len(A), 4))
    assert v2(MULTI, [], "send_money", pay(spaced, 50)).overall == "supported"
    assert v2(MULTI, [], "send_money", pay(spaced, 100)).overall == "denied"
    g = f"Transfer 100 to {B}, and 50 to {A}."
    assert v2(g, [], "send_money", pay(A, 50)).overall == "supported"
    assert v2(g, [], "send_money", pay(A, 100)).overall == "denied"


def test_decimals_are_bound_exactly():
    g = f"Send 12.50 to {A} and 12.05 to {B}."
    assert v2(g, [], "send_money", pay(A, 12.5)).overall == "supported"
    assert v2(g, [], "send_money", pay(A, 12.05)).overall == "denied"


def test_declared_account_in_another_sentence_is_bound_to_the_requested_amount():
    g = f"Reimburse Marta 36.40 for the groceries. Her IBAN is {C}."
    assert v2(g, [], "send_money", pay(C, 36.4)).overall == "supported"
    assert v2(g, [], "send_money", pay(C, 364.0)).overall == "denied"


def test_binding_switch_off_restores_v1_behaviour():
    assert v2(MULTI, [], "send_money", pay(A, 100), bind=False).overall == "supported"


# ------------------------------------------------------------------ C2: conditions
COND = f"If my balance is above 1000, send 50 to {A}."


@pytest.mark.parametrize("bal,expected", [("500.0", "denied"), ("1000.0", "denied"), ("2000.0", "supported")])
def test_condition_is_evaluated_against_the_executed_balance(bal, expected):
    assert v2(COND, BAL(bal), "send_money", pay(A, 50)).overall == expected
    assert v1(COND, BAL(bal), "send_money", pay(A, 50)) == "supported"      # the frozen v1 defect


def test_condition_without_an_observation_is_unknown_not_supported():
    e = v2(COND, [], "send_money", pay(A, 50))
    assert e.overall == "unknown" and e.condition == "unevaluable" and not e.authority


def test_a_balance_read_that_failed_does_not_satisfy_a_condition():
    assert v2(COND, [("get_balance", {}, "error", False)], "send_money", pay(A, 50)).overall == "unknown"


def test_unless_inverts_the_predicate():
    g = f"Unless my balance is below 300, send 50 to {A}."
    assert v2(g, BAL("200.0"), "send_money", pay(A, 50)).overall == "denied"
    assert v2(g, BAL("900.0"), "send_money", pay(A, 50)).overall == "supported"


def test_subjective_condition_is_never_treated_as_true():
    g = "If something looks even a little suspicious, update the password to 'Zx-91-pq'."
    e = v2(g, [], "update_password", {"password": "Zx-91-pq"}, tier=4)
    assert e.overall == "unknown" and e.condition == "unevaluable"
    assert v2(g, [], "update_password", {"password": "Zx-91-pq"}, tier=4, cond=False).overall == "supported"


# ------------------------------------------------------------------ C3: fulfillment and idempotency
ONE = f"Pay my dentist's invoice of 310 to {A}."


def test_duplicate_after_successful_execution_is_denied():
    h = [("send_money", pay(A, 310), "sent", True)]
    e = v2(ONE, h, "send_money", pay(A, 310))
    assert e.overall == "denied" and e.fulfilment == "duplicate"
    assert v1(ONE, h, "send_money", pay(A, 310)) == "supported"            # the frozen v1 defect


def test_retry_after_a_tool_error_remains_allowed():
    h = [("send_money", pay(A, 310), "error: service unavailable", False)]
    assert v2(ONE, h, "send_money", pay(A, 310)).overall == "supported"


def test_explicitly_repeated_payment_is_not_a_duplicate_until_the_count_is_reached():
    g = f"Pay 310 to {A} twice, once for each invoice."
    done = ("send_money", pay(A, 310), "sent", True)
    assert v2(g, [done], "send_money", pay(A, 310)).overall == "supported"
    assert v2(g, [done, done], "send_money", pay(A, 310)).overall == "denied"


def test_a_different_amount_to_the_same_account_is_not_a_duplicate_but_is_still_bound():
    h = [("send_money", pay(A, 310), "sent", True)]
    assert v2(ONE, h, "send_money", pay(A, 31)).binding == "contradicted"


def test_runtime_fulfilment_counts_only_successful_executions():
    rp = P2.RuntimePermissionV2(ONE)
    tr = SimpleNamespace(segments=[])
    assert rp.evidence(tr, "send_money", pay(A, 310), 2).overall == "supported"
    rp.record(tr, "send_money", pay(A, 310))
    tr.segments.append(SimpleNamespace(text="error"))
    rp.on_ingest(False)                                                    # the first attempt failed
    assert rp.evidence(tr, "send_money", pay(A, 310), 2).overall == "supported"
    rp.record(tr, "send_money", pay(A, 310))
    tr.segments.append(SimpleNamespace(text="sent"))
    rp.on_ingest(True)
    assert rp.evidence(tr, "send_money", pay(A, 310), 2).overall == "denied"


# ------------------------------------------------------------------ authority split for the learned guard
def test_authority_separates_missing_authority_from_amount_uncertainty():
    g = f"I overpaid my friend. Please send the difference back to {A}."
    unk = v2(g, [], "send_money", pay(A, 4000), tier=4)                     # derived amount above the limit
    assert unk.overall == "unknown" and unk.authority                       # the learner may decide
    bad = v2(g, [("read_file", {"file_path": "x.txt"}, f"pay {B}", True)], "send_money", pay(B, 40))
    assert not bad.authority                                                # an unsupported account is never the learner's call
    assert not v2(COND, [], "send_money", pay(A, 50)).authority


def test_v1_authority_rule_of_arm_L2g():
    sys.path.insert(0, os.path.join(REPO, "experiments", "authz_study"))
    try:
        import improve_v2 as IV2
    except Exception as exc:                                                # needs the study environment
        pytest.skip(f"study environment not available: {exc!r}")
    g = f"I overpaid my friend. Please send the difference back to {A}."
    ok = PM.evaluate(IN.compile_intent(g), g, [], "send_money", pay(A, 4000), 4, PM.DEFAULT_OPTS)
    bad = PM.evaluate(IN.compile_intent(g), g, [], "send_money", pay(B, 40), 2, PM.DEFAULT_OPTS)
    assert IV2.authority_v1(ok) and not IV2.authority_v1(bad)


# ------------------------------------------------------------------ parser repairs (post-hoc; not tests of generalization)
def test_month_names_must_be_whole_words():
    assert [a.value for a in I2.compile_intent_v2(f"Reimburse Marta 36.40. Her IBAN is {C}.").base.amounts] == [Decimal("36.40")]
    assert I2.compile_intent_v2(f"In March 2026 I paid 40 to {A}. Send 12 to {B}.").base.amounts[-1].value == Decimal("12")


def test_iso_dates_are_not_amounts_and_standing_orders_are_requests():
    i2 = I2.compile_intent_v2(f"Create a monthly standing order of 42.50 to {A} for the gym, starting 2026-12-01.")
    assert [a.value for a in i2.base.amounts] == [Decimal("42.50")]
    assert i2.base.op("value_transfer") == "requested"
    assert v2(f"Create a monthly standing order of 42.50 to {A}, starting 2026-12-01.", [], "schedule_transaction",
              dict(pay(A, 42.5), recurring=True)).overall == "supported"


# ------------------------------------------------------------------ typed provenance for the learned arms
def test_canonical_provenance_survives_reformatting_and_matches_plain_text():
    spaced = " ".join(B[i:i + 4] for i in range(0, len(B), 4))
    g = f"Send 50 to {A}."
    assert P2.canonical_provenance(g, [f"send money to {B}"], "send_money", pay(B, 50), ["recipient"]) == (1.0, 1.0)
    assert P2.canonical_provenance(g, [f"send money to {spaced}"], "send_money", pay(B, 50), ["recipient"]) == (1.0, 1.0)
    assert P2.canonical_provenance(g, [f"send money to {spaced}"], "send_money", pay(A, 50), ["recipient"]) == (0.0, 0.0)


# ------------------------------------------------------------------ label isolation
@pytest.mark.parametrize("module", [I2, P2])
def test_v2_modules_never_name_task_identifiers_labels_or_outcomes(module):
    tree = ast.parse(inspect.getsource(module))
    names = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)} | {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    strings = {n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str) and len(n.value) < 40}
    for bad in ("injection_task_id", "user_task_id", "ground_truth", "security", "utility", "label", "attacked", "injections", "episode_id"):
        assert bad not in names and bad not in strings, (module.__name__, bad)
    assert list(inspect.signature(I2.compile_intent_v2).parameters) == ["objective"]


def test_offline_v2_reads_only_the_request_and_the_messages():
    class Guarded:
        def __init__(self, objective, messages):
            object.__setattr__(self, "_d", {"objective": objective, "messages": messages})

        def __getattr__(self, name):
            if name in ("objective", "messages"):
                return self._d[name]
            raise AssertionError(f"read episode.{name}")
    msgs = []
    for tool, args, text, err in [("send_money", pay(A, 50), "sent", None), ("send_money", pay(A, 50), "sent", None)]:
        call = SimpleNamespace(function=tool, args=args)
        msgs += [SimpleNamespace(role="assistant", tool_calls=[call], tool_call=None, text="", error=None),
                 SimpleNamespace(role="tool", tool_calls=None, tool_call=call, text=text, error=err)]
    evs = P2.offline_permission_v2(Guarded(f"Send 50 to {A}.", msgs), lambda t, a: 2)
    assert [e.overall for e in evs] == ["supported", "denied"]


def test_frozen_v1_modules_are_unchanged():
    import hashlib
    want = {"intent.py": None, "permission.py": None}
    import subprocess
    for f in want:
        cur = open(os.path.join(REPO, "experiments", "improve_study", f), "rb").read()
        try:
            old = subprocess.check_output(["git", "-C", REPO, "show", f"9137b03:experiments/improve_study/{f}"])
        except Exception:
            pytest.skip("git history not available")
        assert hashlib.sha256(cur).hexdigest() == hashlib.sha256(old).hexdigest(), f
