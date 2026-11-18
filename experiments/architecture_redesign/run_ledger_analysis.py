"""Phase 1: run the development ledger scenarios on the frozen arms (analysis before C1B exists)."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "improvement_controlled"))
import arms as AR  # noqa: E402
import ledger_cases as LC  # noqa: E402
import seq_harness as SH  # noqa: E402


def main(out, arms):
    f = AR.factory()
    rows = SH.run_all(lambda a, ep: f(a, ep), arms, LC.CASES)
    res = SH.dump(out, rows)
    for a, s in res["score"].items():
        print(a, "auth", s["authorized_released"], "/", s["authorized_n"], "| unauth", s["unauthorized_released"], "/", s["unauthorized_n"],
              s["unauthorized_released_cases"], "| amb", s["ambiguous_released"], "/", s["ambiguous_n"], "| auth withheld", s["authorized_withheld_cases"])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2].split(","))
