"""Progent's published MANUAL banking policy as a comparator arm (``PG``).

Source: official repository github.com/sunblaze-ucb/progent, commit 9befb41 (10 September 2025), file
``agentdojo/src/agentdojo/default_suites/v1/banking/task_suite.py``, block "# manual policies" (installed
when SECAGENT_GENERATE=False, which is the default of the upstream ``agentdojo/run.sh`` at that commit).

No upstream code is executed or copied. The policy is read from the upstream file AS DATA: the two
literal assignments (``trusted_recipient_list`` and ``policies``) are parsed with ``ast.literal_eval``
after checking that they contain only literals. The pinned file hash is verified.

Decision function. For this policy every entry has the form (priority 1, effect 0 = allow, argument
restrictions, fallback 0). Upstream ``check_tool_call`` / ``_check_tool_call`` (secagent/tool.py at the
same commit) then reduce to:
  * a tool that has no entry in the policy is not allowed;
  * a tool with an entry is allowed iff every restricted argument PRESENT in the bound arguments
    validates against its JSON-schema restriction;
  * arguments are bound with the tool's defaults first (upstream ``secure_tool_wrapper``), so an omitted
    optional argument is checked as ``None``.
The restrictions used by the banking policy are ``{'type': 'string', 'enum': [...]}`` and
``{'anyOf': [that, {'type': 'null'}]}``; ``_validate`` below implements exactly these two JSON-schema
forms and refuses any other.

What this arm is NOT: Progent's LLM-generated or LLM-updated policies (they need a model; not run); a
live-agent run (decisions are replayed on recorded calls, NO-ADAPT); a reproduction of the paper's
numbers; an execution of Progent's own checker (the execution environment did not permit running
third-party code, so the equivalence above is by inspection of 60 lines of upstream code, not by test).
"""
from __future__ import annotations

import ast
import hashlib
import os
import subprocess

COMMIT = "9befb41cbf992b49dbf035cbd3d53eb953d3b351"
SUITE_FILE = "agentdojo/src/agentdojo/default_suites/v1/banking/task_suite.py"
TOOL_FILE = "secagent/tool.py"
PINS = {SUITE_FILE: "43da7d0298bd5ec0de158c4fa3d7b59c4038dc290eb517762c4f39451fac0b6f",
        TOOL_FILE: "4e2a0a6048409ab3a856a0a6d6d6559a957e8b188efa0a6660dbf19b87373635"}
#: defaults of optional arguments of the banking tools (AgentDojo banking suite v1), used for binding
DEFAULTS = {"update_scheduled_transaction": {"recipient": None, "amount": None, "subject": None, "date": None, "recurring": None},
            "update_user_info": {"first_name": None, "last_name": None, "street": None, "city": None},
            "get_most_recent_transactions": {"n": 100}}
_STATE = {}


def _show(up: str, rel: str) -> bytes:
    return subprocess.check_output(["git", "-C", up, "show", f"{COMMIT}:{rel}"])


def upstream_hashes(up: str) -> dict:
    return {rel: hashlib.sha256(_show(up, rel)).hexdigest() for rel in (SUITE_FILE, TOOL_FILE)}


def load(pins: dict = None):
    if _STATE:
        return _STATE
    up = os.environ.get("PROGENT_UPSTREAM")
    if not up or not os.path.isdir(up):
        raise RuntimeError("PROGENT_UPSTREAM must point to a clone of github.com/sunblaze-ucb/progent")
    hashes = upstream_hashes(up)
    for rel, want in (PINS if pins is None else pins).items():
        if want and hashes[rel] != want:
            raise RuntimeError(f"hash mismatch for upstream file {rel}")
    src = _show(up, SUITE_FILE).decode()
    lits = {}
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id in ("trusted_recipient_list", "policies"):
            lits[node.targets[0].id] = node.value
    if set(lits) != {"trusted_recipient_list", "policies"}:
        raise RuntimeError("manual policy block not found in the upstream banking suite")
    trusted = ast.literal_eval(lits["trusted_recipient_list"])

    class _Sub(ast.NodeTransformer):                 # the policy literal refers to the list by name
        def visit_Name(self, node):
            if node.id != "trusted_recipient_list":
                raise RuntimeError("unexpected name in the upstream policy block")
            return ast.copy_location(ast.List([ast.Constant(v) for v in trusted], ast.Load()), node)
    policies = ast.literal_eval(ast.fix_missing_locations(_Sub().visit(lits["policies"])))
    for tool, entries in policies.items():
        for e in entries:
            if not (len(e) == 4 and e[0] == 1 and e[1] == 0 and isinstance(e[2], dict) and e[3] == 0):
                raise RuntimeError(f"policy entry of {tool} is outside the form handled here")
    _STATE.update(policies=policies, trusted=list(trusted), hashes=hashes, commit=COMMIT)
    return _STATE


def _validate(value, schema) -> bool:
    if "anyOf" in schema:
        return any(_validate(value, s) for s in schema["anyOf"])
    t = schema.get("type")
    if t == "null" and set(schema) == {"type"}:
        return value is None
    if t == "string" and set(schema) <= {"type", "enum"}:
        return isinstance(value, str) and ("enum" not in schema or value in schema["enum"])
    raise NotImplementedError(f"JSON-schema form not handled: {schema}")


def allowed(tool: str, args) -> bool:
    """True iff the manual banking policy admits the call."""
    pol = load()["policies"]
    entries = pol.get(tool)
    if not entries:
        return False
    kwargs = dict(DEFAULTS.get(tool, {}))
    kwargs.update(args or {})
    for _prio, _effect, restrictions, _fallback in entries:
        if all(_validate(kwargs[a], r) for a, r in restrictions.items() if a in kwargs):
            return True
    return False
