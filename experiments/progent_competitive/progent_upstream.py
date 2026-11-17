"""Adapter to the pinned upstream Progent engine (arm P0 and the policy core of C2[gen]).

Status: [PROPOSED - EXPLORATORY]. IMPLEMENTED; NOT EXECUTED in the session that wrote it (running third-party code was
refused there, and no model backend was reachable). Nothing is copied from upstream: the engine is imported from a
checkout that must be at the pinned commit; this file only verifies the checkout, sets the documented environment
switches BEFORE import (upstream reads them at import time), and exposes a boolean view of upstream ``check_tool_call``.

Upstream: github.com/sunblaze-ucb/progent, commit 0d7ea074d5e4b106997ebd56dfa1104c39945c03, MIT licence
("Copyright (c) 2026 Progent"). See THIRD_PARTY_NOTICES.md and 03_SOURCE_TO_CODE_REGISTRY.md.

Upstream facts this adapter depends on (read at the pinned commit; line numbers refer to secagent/tool.py):
  * the policy model is the env variable SECAGENT_POLICY_MODEL (l.37); names starting with 'claude' use the Anthropic
    client, 'meta-llama/' and 'Qwen/' an OpenAI-compatible server at 127.0.0.1:8000/v1, anything else the OpenAI client
    (api_request, l.167-);
  * SECAGENT_GENERATE (l.40) switches generation on (default True); SECAGENT_UPDATE (agentdojo tool_execution.py l.121)
    switches the update after each tool batch; SECAGENT_ONLY_ALLOW_NARROW (l.468) enables the z3 subset check
    (Auto-Deny); SECAGENT_IGNORE_UPDATE_ERROR (l.38) ignores failed updates;
  * the published run script of the pinned commit (agentdojo/run.sh) sets SECAGENT_UPDATE=True,
    SECAGENT_IGNORE_UPDATE_ERROR=True and leaves SECAGENT_ONLY_ALLOW_NARROW commented out (Auto-Approve);
  * check_tool_call raises ValidationError when a call is not allowed and returns None otherwise (l.573-591); with no
    policy installed it only prints a warning and allows (l.575-578).
"""
from __future__ import annotations

import importlib
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Mapping, Optional

PINNED = "0d7ea074d5e4b106997ebd56dfa1104c39945c03"

# Progent configurations of the closed-loop comparison. None = leave unset. No configuration with a human reviewer is
# defined: there is no reviewer in this study.
CONFIGS: Dict[str, Dict[str, Optional[str]]] = {
    "P0_manual": {"SECAGENT_GENERATE": "False", "SECAGENT_UPDATE": "False", "SECAGENT_ONLY_ALLOW_NARROW": None,
                  "SECAGENT_IGNORE_UPDATE_ERROR": None},                  # manual banking policy of the fork ("PG historical")
    "P0_generated": {"SECAGENT_GENERATE": "True", "SECAGENT_UPDATE": "False", "SECAGENT_ONLY_ALLOW_NARROW": None,
                     "SECAGENT_IGNORE_UPDATE_ERROR": None},               # generated once from the user query, no update
    "P0_update_autodeny": {"SECAGENT_GENERATE": "True", "SECAGENT_UPDATE": "True", "SECAGENT_ONLY_ALLOW_NARROW": "True",
                           "SECAGENT_IGNORE_UPDATE_ERROR": "True"},        # updates accepted only if narrower (z3)
    "P0_update_autoapprove": {"SECAGENT_GENERATE": "True", "SECAGENT_UPDATE": "True", "SECAGENT_ONLY_ALLOW_NARROW": "False",
                              "SECAGENT_IGNORE_UPDATE_ERROR": "True"},     # the published run.sh setting
}


class UpstreamUnavailable(RuntimeError):
    """The pinned upstream checkout or its engine cannot be used (fail-closed)."""


def verify_checkout(path: str | Path) -> Path:
    p = Path(path).resolve()
    if not (p / "secagent" / "tool.py").is_file():
        raise UpstreamUnavailable(f"no secagent/tool.py under {p}")
    lic = (p / "LICENSE").read_text(encoding="utf-8", errors="replace") if (p / "LICENSE").is_file() else ""
    if "MIT License" not in lic:
        raise UpstreamUnavailable("upstream LICENSE is missing or is not the MIT licence")
    head = subprocess.run(["git", "-C", str(p), "rev-parse", "HEAD"], capture_output=True, text=True, check=False).stdout.strip()
    if head != PINNED:
        raise UpstreamUnavailable(f"upstream checkout is at {head or 'unknown'}, pinned {PINNED}")
    dirty = subprocess.run(["git", "-C", str(p), "status", "--porcelain", "--untracked-files=no"], capture_output=True, text=True,
                           check=False).stdout.strip()
    if dirty:
        raise UpstreamUnavailable("upstream checkout has local modifications")
    return p


def environment_for(config: str, policy_model: Optional[str]) -> Dict[str, Optional[str]]:
    if config not in CONFIGS:
        raise ValueError(f"unknown Progent configuration {config}")
    env = dict(CONFIGS[config])
    if env["SECAGENT_GENERATE"] == "True":
        if not policy_model:
            raise UpstreamUnavailable(f"{config} needs a policy model (SECAGENT_POLICY_MODEL); none is declared")
        env["SECAGENT_POLICY_MODEL"] = policy_model
    return env


def load_secagent(path: str | Path, config: str, policy_model: Optional[str] = None):
    """Import upstream secagent with the configuration's switches set. One configuration per process (upstream keeps
    module-level state and reads the switches at import)."""
    root = verify_checkout(path)
    if "secagent" in sys.modules:
        raise UpstreamUnavailable("secagent is already imported in this process; start a fresh process per configuration")
    for k, v in environment_for(config, policy_model).items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    sys.path.insert(0, str(root))
    return importlib.import_module("secagent")


def upstream_allowed(secagent, tool: str, kwargs: Mapping[str, Any]) -> bool:
    """Boolean view of upstream check_tool_call for already-bound arguments."""
    from secagent.tool import ValidationError  # noqa: WPS433 (upstream class)
    try:
        secagent.check_tool_call(tool, dict(kwargs))
        return True
    except ValidationError:
        return False


def install_manual_policy(secagent, policies: Mapping[str, Any]) -> None:
    """Install a manual policy dict (tool -> [(priority, effect, restrictions, fallback)]) with upstream's own setter."""
    secagent.update_security_policy({k: [tuple(x) for x in v] for k, v in policies.items()})
