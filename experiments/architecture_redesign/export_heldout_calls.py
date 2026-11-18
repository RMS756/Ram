"""Export the restricted calls proposed by the recorded agents of the held-out population H (from the trace messages,
independently of any REM arm), in the format read by improvement_controlled/parity_recorded_calls.py."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arch_run as A  # noqa: E402


def main(out):
    d, aux, eps, folds = A._populations()
    st = A.common.make_setup()
    restricted = set(st.restricted)
    rows = []
    for e, ep in sorted(eps["heldout"].items()):
        for m in ep.raw_messages:
            for t in (m.get("tool_calls") or []) if m.get("role") == "assistant" else []:
                if t["function"] in restricted:
                    rows.append({"episode": e, "tool": t["function"], "args": dict(t["args"] or {})})
    Path(out).write_text(json.dumps({"rows": rows}, indent=1))
    print("held-out restricted calls", len(rows))


if __name__ == "__main__":
    main(sys.argv[1])
