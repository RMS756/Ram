"""Workload of the planned live comparison, MEASURED in characters from AgentDojo's recorded gpt-4o banking runs.

No tokenizer file and no price list are reachable from the session that wrote this (openaipublic.blob.core.windows.net
and platform.openai.com are outside its network), so this script reports characters and call counts only. Tokens and
dollars follow once a tokenizer and the provider's price list of the run day are supplied (see 10_LATENCY_AND_COST_ANALYSIS.md).

Model of the three arms (from the code, not assumed):
  D0, D1  agent calls = recorded assistant turns; each call sends the conversation so far + the tool schemas.
          REM adds no model call (its per-call cost is CPU only).
  D2      the original-run agent calls as above, plus ONE masked re-execution per agent call made after a tool result
          (MELON.query runs after every tool turn), whose context is: system message + upstream's fixed few-shot dialogue
          + one fake read_file result holding ALL tool outputs so far; plus embedding calls (one per new masked tool call
          and one per original tool call when the masked bank is non-empty).
Upper/lower bounds: under attack MELON may stop an episode early (fewer calls), REM refusals may change the trajectory;
the recorded undefended trajectory is used for all arms, so the figures are planning estimates, not measurements of the arms.

usage: python3 experiments/rem_vs_melon/estimate_volume.py <out.json>
"""
import glob
import json
import os
import sys

RUNS = os.environ.get("AGENTDOJO_RUNS", "/home/user/ethz-spylab/agentdojo/runs")
PIPE = "gpt-4o-2024-05-13"


def text(m):
    c = m.get("content")
    if isinstance(c, list):
        return "".join(str(b.get("content", "")) for b in c if isinstance(b, dict))
    return c or ""


def msg_chars(m):
    n = len(text(m))
    for tc in m.get("tool_calls") or []:
        n += len(json.dumps(tc.get("args", {}))) + len(tc.get("function", ""))
    return n


def tool_schema_chars():
    try:
        from agentdojo.task_suite.load_suites import get_suites
        s = get_suites("v1")["banking"]
        return sum(len(t.name) + len(t.description or "") + len(json.dumps(t.parameters.model_json_schema())) for t in s.tools)
    except Exception:
        return None


def melon_fixed_chars():
    try:
        sys.path.insert(0, "/home/user/ucsb-mlsec/melon")
        src = open("/home/user/ucsb-mlsec/melon/pi_detector.py", encoding="utf-8").read()
        a = src.index("sample_general_instruction_messages = [")
        b = src.index("masked_messages += sample_general_instruction_messages")
        return len(src[a:b]) + 600       # few-shot block (source length, an upper bound) + general instruction text
    except Exception:
        return None


def main(out):
    tools = tool_schema_chars()
    fixed = melon_fixed_chars()
    rows = []
    for f in sorted(glob.glob(f"{RUNS}/{PIPE}/banking/user_task_*/*/*.json")):
        atk = f.split("/")[-2]
        if atk not in ("important_instructions", "none"):
            continue
        d = json.load(open(f))
        msgs = d["messages"]
        agent_calls = in_chars = masked_calls = masked_chars = 0
        ctx = 0
        tool_out = 0
        sys_chars = len(text(msgs[0])) if msgs and msgs[0].get("role") == "system" else 0
        for k, m in enumerate(msgs):
            if m.get("role") == "assistant":
                agent_calls += 1
                in_chars += ctx + (tools or 0)
                if k > 0 and msgs[k - 1].get("role") == "tool":
                    masked_calls += 1
                    masked_chars += sys_chars + (fixed or 0) + tool_out + (tools or 0)
            if m.get("role") == "tool":
                tool_out += len(text(m)) + 120
            ctx += msg_chars(m)
        out_chars = sum(msg_chars(m) for m in msgs if m.get("role") == "assistant")
        rows.append({"attacked": atk != "none", "agent_calls": agent_calls, "agent_input_chars": in_chars,
                     "agent_output_chars": out_chars, "melon_masked_calls": masked_calls, "melon_masked_input_chars": masked_chars})
    tot = lambda k, att=None: sum(r[k] for r in rows if att is None or r["attacked"] == att)   # noqa: E731
    per_arm = {"episodes": len(rows), "attacked": sum(r["attacked"] for r in rows),
               "agent_calls": tot("agent_calls"), "agent_input_chars": tot("agent_input_chars"),
               "agent_output_chars": tot("agent_output_chars")}
    res = {"status": "PLANNING ESTIMATE from recorded undefended gpt-4o trajectories (characters, not tokens; no prices)",
           "tool_schema_chars_per_call": tools, "melon_fixed_masked_prefix_chars_upper_bound": fixed,
           "per_arm_D0_or_D1": per_arm,
           "D2_extra": {"melon_masked_calls": tot("melon_masked_calls"), "melon_masked_input_chars": tot("melon_masked_input_chars"),
                        "embedding_calls_upper_bound": 2 * tot("melon_masked_calls")},
           "design_full_one_repeat": {"episodes": 3 * len(rows),
                                      "model_calls": 3 * tot("agent_calls") + tot("melon_masked_calls"),
                                      "input_chars": 3 * tot("agent_input_chars") + tot("melon_masked_input_chars"),
                                      "output_chars_lower_bound": 3 * tot("agent_output_chars")}}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
