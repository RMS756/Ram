"""Authorization evidence z_exp, z_del (protocol section 4) — isolated study module.

Status: [PROPOSED — SUPERVISOR APPROVAL REQUIRED]. Not part of the approved REM design; nothing in
``rem/`` is changed. Deterministic; no fitted or tuned quantity. Occurrence uses REM's own
``value_occurs_in`` unchanged.

Definitions (protocol 06, section 4). For a proposed call to a restricted tool (T_R):
  K      declared key arguments present in the call (non-None);
  K_id   K without ``amount``;  K_ref = K_id if non-empty else K;
  g      the user objective (trusted user text);
  user-named source: output of an earlier executed read-category call having at least one string
         argument value (length >= 3) that occurs in g.
  z_exp = 1 iff K_ref non-empty and every value in K_ref occurs in g;
  z_del = 1 iff K_ref non-empty, not every value occurs in g, and every value not in g occurs in a
          user-named source.
Both are 0 for tools outside T_R.
"""
from __future__ import annotations

from typing import Any, List, Mapping, Optional, Sequence, Tuple

from rem.algorithms.context.provenance import strip_invisible, value_occurs_in

AUTHZ_ORDER: Tuple[str, ...] = ("z_exp", "z_del")

#: history entry: (tool, args, output_text, executed)
History = Sequence[Tuple[str, Mapping[str, Any], str, bool]]


def named_sources(objective: str, history: History, read_tools: Sequence[str]) -> List[str]:
    """Outputs of earlier executed read calls whose own string argument occurs in the objective."""
    out: List[str] = []
    for tool, args, text, executed in history:
        if not executed or tool not in read_tools:
            continue
        for v in (args or {}).values():
            if isinstance(v, str) and len(v.strip()) >= 3 and value_occurs_in(v, [objective]):
                out.append(strip_invisible(text or ""))
                break
    return out


def authz_evidence(
    *,
    key_arguments: Mapping[str, Sequence[str]],
    restricted_tools: Sequence[str],
    read_tools: Sequence[str],
    objective: str,
    history: History,
    tool: str,
    args: Mapping[str, Any],
) -> Tuple[float, float]:
    """Return (z_exp, z_del) for one proposed call."""
    if tool not in restricted_tools:
        return 0.0, 0.0
    keys = [k for k in key_arguments.get(tool, ()) if k in args and args.get(k) is not None]
    k_id = [k for k in keys if k != "amount"]
    k_ref = k_id if k_id else keys
    if not k_ref:
        return 0.0, 0.0
    explicit = {k: value_occurs_in(args[k], [objective]) for k in k_ref}
    if all(explicit.values()):
        return 1.0, 0.0
    sources = named_sources(objective, history, read_tools)
    rest = [k for k in k_ref if not explicit[k]]
    if sources and all(value_occurs_in(args[k], sources) for k in rest):
        return 0.0, 1.0
    return 0.0, 0.0


def offline_authz(episode, spec, restricted_tools: Sequence[str], read_tools: Sequence[str]) -> List[Tuple[float, float]]:
    """(z_exp, z_del) per proposed call of a recorded episode, in the order of ``build_steps``.

    Mirrors ``rem.integration.steps.build_steps``: all calls of one assistant message are scored
    before that message's tool results are ingested.
    """
    out: List[Tuple[float, float]] = []
    history: List[Tuple[str, Mapping[str, Any], str, bool]] = []
    for m in episode.messages:
        if m.role == "assistant" and m.tool_calls:
            for call in m.tool_calls:
                out.append(authz_evidence(key_arguments=spec.key_arguments, restricted_tools=restricted_tools,
                                          read_tools=read_tools, objective=episode.objective, history=history,
                                          tool=call.function, args=call.args))
        elif m.role == "tool" and m.tool_call is not None:
            history.append((m.tool_call.function, dict(m.tool_call.args or {}), m.text or "", m.error is None))
    return out


class RuntimeAuthz:
    """Per-episode runtime state for authorization evidence inside a decide function.

    The decide function is called by ``RemGuard.evaluate`` before the call is executed and before its
    result is ingested; the result of call j is therefore the tracker segment with index
    ``len(tracker.segments)`` observed at decide time. A call counts as executed if this policy
    released it (runtime errors of released reads are not visible here; their error text is the
    segment text).
    """

    def __init__(self, spec, restricted_tools: Sequence[str], read_tools: Sequence[str], objective: str) -> None:
        self.spec, self.restricted, self.read_tools, self.objective = spec, tuple(restricted_tools), tuple(read_tools), objective
        self._calls: List[Tuple[str, Mapping[str, Any], int, Optional[bool]]] = []

    def evidence(self, tracker, tool: str, args: Mapping[str, Any]) -> Tuple[float, float]:
        history = []
        for t, a, seg, released in self._calls:
            if seg < len(tracker.segments):
                history.append((t, a, tracker.segments[seg].text, bool(released)))
        return authz_evidence(key_arguments=self.spec.key_arguments, restricted_tools=self.restricted,
                              read_tools=self.read_tools, objective=self.objective, history=history, tool=tool, args=args)

    def record(self, tracker, tool: str, args: Mapping[str, Any], released: bool) -> None:
        self._calls.append((tool, dict(args), len(tracker.segments), released))
