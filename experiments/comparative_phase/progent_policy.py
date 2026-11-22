"""Load Progent's published manual banking policy VERBATIM from the authors' repository.

Source: github.com/sunblaze-ucb/progent, commit 9befb41cbf992b49dbf035cbd3d53eb953d3b351,
file agentdojo/src/agentdojo/default_suites/v1/banking/task_suite.py, block "# manual policies"
(applied by the repository when SECAGENT_GENERATE=False). The block is read from git and executed in an empty
namespace; nothing is retyped or edited here. The enforcement code is the authors' `secagent` at the commit
recorded in REM_EXTERNAL_DEFENSE_AUDIT/results/upstream_pins.json (3e79753).
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys

PROGENT_REPO = os.environ.get("PROGENT_REPO", "/home/user/upstream/sunblaze-ucb_progent")
PROGENT_EXPORT = os.environ.get("PROGENT_UPSTREAM", "/home/user/upstream/progent_3e79753")
POLICY_COMMIT = "9befb41cbf992b49dbf035cbd3d53eb953d3b351"
POLICY_PATH = "agentdojo/src/agentdojo/default_suites/v1/banking/task_suite.py"

SECAGENT_TOOL_SHA256 = None       # filled from upstream_pins.json by load_secagent()
GENERIC_ALWAYS_ALLOWED = (["get_most_recent_transactions"], True)   # update_always_allowed_tools(..., allow_all_no_arg_tools=True)


def policy_source() -> str:
    return subprocess.run(["git", "-C", PROGENT_REPO, "show", f"{POLICY_COMMIT}:{POLICY_PATH}"],
                          check=True, capture_output=True, text=True).stdout


def policy_block(src: str) -> str:
    m = re.search(r"(        trusted_recipient_list = \[.*?\n        \}\n)\s*update_security_policy\(policies\)", src, re.S)
    if not m:
        raise RuntimeError("manual policy block not found at the pinned commit (fail closed)")
    return m.group(1)


def load_policy():
    src = policy_source()
    block = policy_block(src)
    ns: dict = {}
    exec(compile("\n".join(line[8:] for line in block.splitlines()), "<progent-9befb41-manual-policy>", "exec"), {}, ns)
    meta = {"commit": POLICY_COMMIT, "path": POLICY_PATH,
            "file_sha256": hashlib.sha256(src.encode()).hexdigest(),
            "block_sha256": hashlib.sha256(block.encode()).hexdigest(),
            "trusted_recipient_list": ns["trusted_recipient_list"], "tools_with_rules": sorted(ns["policies"])}
    return ns["policies"], meta, src, block


def load_secagent(pins_path: str):
    """Import the authors' secagent from the clean export and check its hash against the recorded pin."""
    import json
    pins = json.load(open(pins_path))["Progent_official"]
    want = pins["sha256"]["tool.py"]
    got = hashlib.sha256(open(os.path.join(PROGENT_EXPORT, "secagent", "tool.py"), "rb").read()).hexdigest()
    if got != want:
        raise RuntimeError(f"secagent/tool.py hash {got} != pinned {want} (fail closed)")
    os.environ["SECAGENT_GENERATE"] = "False"
    os.environ["SECAGENT_UPDATE"] = "False"
    if PROGENT_EXPORT not in sys.path:
        sys.path.insert(0, PROGENT_EXPORT)
    import secagent
    return secagent, pins["commit"], got


def install_policy(secagent, raw_tools, policies):
    """The repository's own initialisation sequence for the banking suite with SECAGENT_GENERATE=False."""
    import copy
    secagent.apply_secure_tool_wrapper(list(raw_tools))          # registers the tools (available_tools)
    secagent.update_always_allowed_tools(GENERIC_ALWAYS_ALLOWED[0], allow_all_no_arg_tools=GENERIC_ALWAYS_ALLOWED[1])
    secagent.update_security_policy(copy.deepcopy(policies))


def banking_raw_tools():
    from agentdojo.default_suites.v1.tools.banking_client import (get_balance, get_iban, get_most_recent_transactions,
                                                                  get_scheduled_transactions, schedule_transaction,
                                                                  send_money, update_scheduled_transaction)
    from agentdojo.default_suites.v1.tools.file_reader import read_file
    from agentdojo.default_suites.v1.tools.user_account import get_user_info, update_password, update_user_info
    return [get_iban, send_money, schedule_transaction, update_scheduled_transaction, get_balance,
            get_most_recent_transactions, get_scheduled_transactions, read_file, get_user_info, update_password,
            update_user_info]
