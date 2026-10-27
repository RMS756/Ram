"""Recorded AgentDojo traces -> labelled REM step records (EXPLORATORY).

Data source: the ``runs/`` directory of the AgentDojo repository, i.e. traces
of real LLM agents recorded by the benchmark authors. No trace is generated or
altered here. Each proposed tool call in an assistant message is one REM step
(interpretation I-1 of ``rem.algorithms.behavior.evidence``).

Label rule (Chapter 3 Sec. 3.11.3, reference match):
    y_t = 1 iff the episode carries an injection task, the tool of a_t occurs in
    that task's reference solution (``ground_truth``), and every declared
    attacker key argument present in the reference call is matched by a_t
    (case-insensitive, whitespace-stripped).
Read tools that occur in a reference solution (injection_task_8 reads the
scheduled transactions) are labelled 0 in the primary analysis; the
``induced_read_steps_positive`` flag gives the sensitivity variant.

Label ambiguity: a pair (user task, injection task) is *ambiguous* when the
user task's own reference solution contains a call that satisfies the label
rule of that injection task. In AgentDojo banking v1 this holds for
(user_task_15, injection_task_4): the user asks to redirect the rent standing
order to US133000000121212121212, which is also the attacker IBAN, so the
legitimate action matches the attack and the benchmark's security check
reports success even without an attack. ``ambiguous_pairs`` finds such pairs
from the ground truths instead of hard-coding them.
"""

from __future__ import annotations

import glob
import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Iterator, List, Mapping, Optional, Sequence, Set, Tuple

__all__ = [
    "ToolCall",
    "Message",
    "Episode",
    "load_episode",
    "iter_episode_paths",
    "ReferenceSolutions",
    "ReferenceLabeler",
    "ambiguous_pairs",
]


@dataclass(frozen=True)
class ToolCall:
    function: str
    args: Mapping[str, Any]
    id: Optional[str]


@dataclass(frozen=True)
class Message:
    role: str
    text: str
    tool_calls: Tuple[ToolCall, ...] = ()
    tool_call: Optional[ToolCall] = None   # for role == "tool"
    error: Optional[str] = None            # for role == "tool"


@dataclass(frozen=True)
class Episode:
    path: str
    pipeline: str
    suite: str
    user_task_id: str
    injection_task_id: Optional[str]
    attack_type: Optional[str]
    injections: Mapping[str, str]
    messages: Tuple[Message, ...]
    utility: bool
    security: bool
    error: Optional[str]
    benchmark_version: Optional[str]
    raw_messages: Tuple[Mapping[str, Any], ...] = field(repr=False, default=())

    @property
    def episode_id(self) -> str:
        return f"{self.pipeline}|{self.user_task_id}|{self.injection_task_id or 'none'}|{self.attack_type or 'none'}"

    @property
    def attacked(self) -> bool:
        return self.injection_task_id is not None

    @property
    def objective(self) -> str:
        return next((m.text for m in self.messages if m.role == "user"), "")

    @property
    def system_prompt(self) -> str:
        return next((m.text for m in self.messages if m.role == "system"), "")


def _text(content: Any) -> str:
    """Flatten AgentDojo message content (string, list of blocks, or None)."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, Mapping):
                parts.append(str(block.get("content") or block.get("text") or ""))
            else:
                parts.append(str(block))
        return "\n".join(p for p in parts if p)
    return str(content)


def _call(raw: Mapping[str, Any]) -> ToolCall:
    return ToolCall(str(raw.get("function", "")), dict(raw.get("args") or {}), raw.get("id"))


def load_episode(path: str) -> Episode:
    with open(path, "r", encoding="utf-8") as fh:
        d = json.load(fh)
    msgs = []
    for m in d.get("messages") or []:
        role = m.get("role")
        tcs = tuple(_call(t) for t in (m.get("tool_calls") or []))
        tc = _call(m["tool_call"]) if m.get("tool_call") else None
        msgs.append(Message(role, _text(m.get("content")), tcs, tc, m.get("error")))
    return Episode(
        path=path,
        pipeline=str(d.get("pipeline_name")),
        suite=str(d.get("suite_name")),
        user_task_id=str(d.get("user_task_id")),
        injection_task_id=d.get("injection_task_id"),
        attack_type=d.get("attack_type"),
        injections=dict(d.get("injections") or {}),
        messages=tuple(msgs),
        utility=bool(d.get("utility")),
        security=bool(d.get("security")),
        error=d.get("error"),
        benchmark_version=d.get("benchmark_version"),
        raw_messages=tuple(d.get("messages") or []),
    )


def iter_episode_paths(runs_root: str, pipeline: str, suite: str, attack: str) -> List[str]:
    """Attacked traces for ``attack`` (``"none"`` gives the benign traces)."""
    if attack == "none":
        pattern = os.path.join(runs_root, pipeline, suite, "user_task_*", "none", "none.json")
    else:
        pattern = os.path.join(runs_root, pipeline, suite, "user_task_*", attack, "injection_task_*.json")
    return sorted(glob.glob(pattern))


# -- labels -------------------------------------------------------------------


@dataclass(frozen=True)
class ReferenceSolutions:
    """Ground-truth calls of the user and injection tasks of one suite version."""

    injection: Mapping[str, Tuple[ToolCall, ...]]
    user: Mapping[str, Tuple[ToolCall, ...]]
    suite_version: str

    @classmethod
    def from_agentdojo(cls, suite_version: str, suite_name: str) -> "ReferenceSolutions":
        """Read ground truths from the installed AgentDojo package (no hard-coding)."""
        from agentdojo.task_suite.load_suites import get_suites  # lazy: optional dependency

        suite = get_suites(suite_version)[suite_name]
        env = suite.load_and_inject_default_environment({})
        inj = {
            k: tuple(ToolCall(c.function, dict(c.args), None) for c in t.ground_truth(env))
            for k, t in suite.injection_tasks.items()
        }
        usr = {
            k: tuple(ToolCall(c.function, dict(c.args), None) for c in t.ground_truth(env))
            for k, t in suite.user_tasks.items()
        }
        return cls(inj, usr, suite_version)


def _norm(v: Any) -> str:
    return str(v).strip().lower()


@dataclass(frozen=True)
class ReferenceLabeler:
    """Chapter 3 Sec. 3.11.3 reference-match label rule.

    Args:
        references: Ground-truth calls.
        attacker_key_arguments: Declared argument name -> attacker value.
        read_tools: Tools of the ``read`` action category.
        induced_read_steps_positive: Sensitivity flag (primary: False).
    """

    references: ReferenceSolutions
    attacker_key_arguments: Mapping[str, str]
    read_tools: Sequence[str]
    induced_read_steps_positive: bool

    def _matches(self, ref: ToolCall, tool: str, args: Mapping[str, Any]) -> bool:
        if ref.function != tool:
            return False
        for name, value in self.attacker_key_arguments.items():
            if name in ref.args and _norm(ref.args[name]) == _norm(value):
                if _norm(args.get(name, "")) != _norm(value):
                    return False
        return True

    def label(self, injection_task_id: Optional[str], tool: str, args: Mapping[str, Any]) -> int:
        if injection_task_id is None:
            return 0
        refs = self.references.injection[injection_task_id]
        if tool in self.read_tools and not self.induced_read_steps_positive:
            return 0
        return int(any(self._matches(r, tool, args) for r in refs))

    def attacker_key_match(self, tool: str, args: Mapping[str, Any]) -> bool:
        """Any declared attacker value in the call (for the label audit only)."""
        return any(_norm(args.get(n, "")) == _norm(v) for n, v in self.attacker_key_arguments.items())


def ambiguous_pairs(labeler: ReferenceLabeler) -> Set[Tuple[str, str]]:
    """(user task, injection task) pairs whose legitimate reference call is labelled 1."""
    out = set()
    for ut, calls in labeler.references.user.items():
        for it in labeler.references.injection:
            if any(labeler.label(it, c.function, c.args) for c in calls):
                out.add((ut, it))
    return out
