"""Export the restricted calls proposed by the recorded agents of H2 (trace messages, independent of any REM arm), in the
format read by improvement_controlled/parity_recorded_calls.py (Progent hand-written policy vs upstream checker)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hard_run as HR  # noqa: E402


def main(out):
    d, aux, eps, folds = HR._populations()
    restricted = set(HR.common.make_setup().restricted)
    rows = [{"episode": e, "tool": t["function"], "args": dict(t["args"] or {})}
            for e, ep in sorted(eps["heldout2"].items()) for m in ep.raw_messages
            for t in ((m.get("tool_calls") or []) if m.get("role") == "assistant" else []) if t["function"] in restricted]
    Path(out).write_text(json.dumps({"rows": rows}, indent=1))
    print("H2 restricted calls", len(rows))


if __name__ == "__main__":
    main(sys.argv[1])
