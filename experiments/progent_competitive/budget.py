"""Token-volume and cost estimator for the closed-loop comparison (06_BUDGET_ESTIMATE.md). No model call, no network.

Measured (exact character counts):
  * agent side: for each stored AgentDojo banking run of a given pipeline, the characters an agent model receives and
    emits. Each assistant turn re-sends the whole conversation so far plus the tool schemas of the banking suite;
  * Progent side: the characters of the upstream policy prompts. These are the string constants of get_SYS_PROMPT,
    get_SYS_PROMPT_2 and SYS_PROMPT_UPDATE in secagent/tool.py at the pinned commit, read by parsing the file, never
    by importing it. Added to them: the tools JSON, the user query and, for updates, the tool call and its result.
Not measurable here: the length of the policy model's outputs (no Progent run is stored). Its value must be declared in
the prices file, or the cost of the Progent calls is reported as "not computed".
Characters are converted to tokens with an explicit chars-per-token ratio. Both 3 and 4 are reported as a sensitivity
range: no tokenizer is available offline, so this is an APPROXIMATION.

Prices are NOT built in. The operator copies them from the provider's official pricing page into a JSON file
(see prices_TEMPLATE.json). Without prices, only volumes are reported.

usage: python3 budget.py --runs <agentdojo runs dir> --pipeline <stored pipeline used as the trace-length proxy>
                         --upstream <progent checkout> [--prices prices.json] [--repeats 1]
"""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Dict, List, Optional

BANKING_USER_TASKS = 16
BANKING_INJECTION_TASKS = 9


def _strings_in(node) -> int:
    n = 0
    for x in ast.walk(node):
        if isinstance(x, ast.Constant) and isinstance(x.value, str):
            n += len(x.value)
    return n


def upstream_prompt_chars(upstream: Path) -> Dict[str, int]:
    """Lengths of the policy prompts, resolved statically from the module-level assignments (f-strings and names are
    followed; ``str.replace`` is counted at the length of its base string, a difference of a few characters). The output
    formatter that get_SYS_PROMPT / get_SYS_PROMPT_2 append depends on the model; its longest variant is added (upper bound)."""
    tree = ast.parse((upstream / "secagent" / "tool.py").read_text(encoding="utf-8"))
    env = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            env[node.targets[0].id] = node.value

    def length(n) -> int:
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            return len(n.value)
        if isinstance(n, ast.JoinedStr):
            return sum(length(v) for v in n.values)
        if isinstance(n, ast.FormattedValue):
            return length(n.value)
        if isinstance(n, ast.Name) and n.id in env:
            return length(env[n.id])
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "replace":
            return length(n.func.value)
        raise ValueError(f"cannot resolve prompt part {ast.dump(n)[:80]}")

    fmt = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in ("get_SYS_PROMPT", "get_SYS_PROMPT_2"):
            fmt[node.name] = max((len(x.value) for x in ast.walk(node) if isinstance(x, ast.Constant) and isinstance(x.value, str)
                                  and x.value.startswith((" ", "\n"))), default=0)
    return {"get_SYS_PROMPT": length(env["SYS_PROMPT"]) + fmt["get_SYS_PROMPT"],
            "get_SYS_PROMPT_2": length(env["SYS_PROMPT_2"]) + fmt["get_SYS_PROMPT_2"],
            "SYS_PROMPT_UPDATE": length(env["SYS_PROMPT_UPDATE"])}


def _text(m) -> str:
    c = m.get("content")
    if isinstance(c, list):
        return "".join(str(b.get("content", "")) if isinstance(b, dict) else str(b) for b in c)
    s = "" if c is None else str(c)
    if m.get("tool_calls"):
        s += json.dumps(m["tool_calls"], default=str)
    return s


def episode_volumes(run: dict, tools_chars: int) -> Dict[str, int]:
    msgs = run["messages"]
    agent_in = agent_out = 0
    tool_batches = []
    ctx = 0
    for i, m in enumerate(msgs):
        if m.get("role") == "assistant":
            agent_in += ctx + tools_chars
            agent_out += len(_text(m))
        if m.get("role") == "tool":
            tool_batches.append((json.dumps(m.get("tool_call"), default=str), len(_text(m))))
        ctx += len(_text(m))
    query = next((len(_text(m)) for m in msgs if m.get("role") == "user"), 0)
    return {"agent_in": agent_in, "agent_out": agent_out, "query": query, "tool_results": len(tool_batches),
            "tool_call_chars": sum(len(c) for c, _ in tool_batches), "tool_result_chars": sum(r for _, r in tool_batches),
            "assistant_turns": sum(1 for m in msgs if m.get("role") == "assistant")}


def collect(runs: Path, pipeline: str) -> List[Dict[str, int]]:
    base = runs / pipeline / "banking"
    vols = []
    for f in sorted(base.glob("user_task_*/**/*.json")):
        try:
            vols.append(episode_volumes(json.loads(f.read_text(encoding="utf-8")), TOOLS_CHARS))
        except (KeyError, json.JSONDecodeError):
            continue
    return vols


TOOLS_CHARS = 4854   # json of the 11 banking tool schemas (name, description, parameters), measured with AgentDojo's suite


def progent_volumes(v: Dict[str, int], prompts: Dict[str, int], config: str) -> Dict[str, int]:
    """Input characters of the policy model for one episode (generation once; per tool batch, the update decision and,
    at most, one update)."""
    gen = prompts["get_SYS_PROMPT"] + TOOLS_CHARS + v["query"] if config != "P0_manual" else 0
    upd_in = 0
    if config in ("P0_update_autodeny", "P0_update_autoapprove"):
        per = TOOLS_CHARS + v["query"]
        decide = v["tool_results"] * (prompts["SYS_PROMPT_UPDATE"] + per) + v["tool_call_chars"]
        update = v["tool_results"] * (prompts["get_SYS_PROMPT_2"] + per) + v["tool_call_chars"] + v["tool_result_chars"]
        upd_in = decide + update                 # upper bound: every decision answers "yes"
    return {"policy_in": gen + upd_in, "policy_calls": (1 if gen else 0) + (2 * v["tool_results"] if upd_in else 0)}


def estimate(runs: Path, pipeline: str, upstream: Path, prices: Optional[dict], repeats: int, arms: List[str]) -> dict:
    vols = collect(runs, pipeline)
    if not vols:
        raise SystemExit(f"no stored banking runs for {pipeline}")
    prompts = upstream_prompt_chars(upstream)
    n_eps = (BANKING_USER_TASKS * BANKING_INJECTION_TASKS + BANKING_USER_TASKS) * repeats   # attacked + benign, per arm
    mean = {k: sum(v[k] for v in vols) / len(vols) for k in vols[0]}
    out = {"status": "ESTIMATE (approximate tokens; prices from the operator's file); not a measured cost",
           "trace_proxy": {"pipeline": pipeline, "episodes_read": len(vols), "mean_per_episode": mean},
           "upstream_prompt_chars": prompts, "episodes_per_arm": n_eps, "arms": {}}
    for arm in arms:
        cfg = arm.split("_", 1)[1] if arm.startswith(("C2gen_", "C3gen_")) else arm
        pv = [progent_volumes(v, prompts, cfg) for v in vols] if cfg.startswith("P0_") else [{"policy_in": 0, "policy_calls": 0}] * len(vols)
        a_in = mean["agent_in"] * n_eps
        a_out = mean["agent_out"] * n_eps
        p_in = sum(p["policy_in"] for p in pv) / len(pv) * n_eps
        p_calls = sum(p["policy_calls"] for p in pv) / len(pv) * n_eps
        rec = {"agent_input_chars": round(a_in), "agent_output_chars": round(a_out), "policy_input_chars": round(p_in),
               "policy_calls": round(p_calls)}
        for cpt in (3.0, 4.0):
            rec[f"tokens_at_{cpt:g}_chars_per_token"] = {"agent_in": round(a_in / cpt), "agent_out": round(a_out / cpt),
                                                         "policy_in": round(p_in / cpt)}
        if prices:
            rec["cost_usd"] = _cost(rec, prices, p_calls)
        out["arms"][arm] = rec
    return out


def _cost(rec: dict, prices: dict, p_calls: float) -> dict:
    ag, po = prices.get("agent_model") or {}, prices.get("policy_model") or {}
    res = {}
    for cpt in (3.0, 4.0):
        t = rec[f"tokens_at_{cpt:g}_chars_per_token"]
        agent = None
        if ag.get("input_usd_per_1m") is not None and ag.get("output_usd_per_1m") is not None:
            agent = (t["agent_in"] * ag["input_usd_per_1m"] + t["agent_out"] * ag["output_usd_per_1m"]) / 1e6
        policy = None
        if t["policy_in"] == 0:
            policy = 0.0
        elif po.get("input_usd_per_1m") is not None and po.get("output_usd_per_1m") is not None and po.get("output_tokens_per_call") is not None:
            policy = (t["policy_in"] * po["input_usd_per_1m"] + p_calls * po["output_tokens_per_call"] * po["output_usd_per_1m"]) / 1e6
        res[f"at_{cpt:g}_chars_per_token"] = {"agent": agent, "policy": policy,
                                              "total": None if agent is None or policy is None else agent + policy}
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True)
    ap.add_argument("--pipeline", required=True)
    ap.add_argument("--upstream", required=True)
    ap.add_argument("--prices")
    ap.add_argument("--repeats", type=int, default=1)
    ap.add_argument("--arms", default="P0_manual,P0_generated,P0_update_autodeny,P0_update_autoapprove,C1,"
                                      "C2gen_P0_generated,C2gen_P0_update_autodeny,C2gen_P0_update_autoapprove")
    ap.add_argument("--out")
    a = ap.parse_args()
    prices = json.loads(Path(a.prices).read_text()) if a.prices else None
    res = estimate(Path(a.runs), a.pipeline, Path(a.upstream), prices, a.repeats, a.arms.split(","))
    text = json.dumps(res, indent=1)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
