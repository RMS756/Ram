"""Reproduce F1, F2 and F3 on the frozen version-2 arms (and version 1 for reference), with corrected scoring.

usage: python3 experiments/progent_competitive/reproduce_f.py   (environment of the competitive study)
output: REM_PROGENT_COMPETITIVE_2026_11_18/results/f_before_v2.json
F3: the historical file results/defects_d3_d4_after_v2.json is NOT overwritten; its labels ('unverifiable') and the
corrected labels here ('authorized' for the stated total 60) are listed side by side in the output.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "progent_competitive"))
import diag_harness as H  # noqa: E402
import reproduce_defects as RD  # noqa: E402
import repaired_arms as RA1  # noqa: E402
import repaired_arms_v2 as RA2  # noqa: E402

ARMS = ["GV_math", "HV_math", "G3_math2", "GV_math2", "HV_math2", "GV_math2x", "HV_math2x"]


def main():
    st = RD.C.common.make_setup()
    cells, cs = RD.C.J.load("cells"), RD.C.load("cs_cells")
    key = ("S1", "injection_task_0")

    def build(arm, ep):
        ep.system_prompt = RD.tf.SYSTEM_PROMPT
        mod = RA1 if arm in RA1.ARMS else RA2
        return mod.make_guard(arm, cells[key], cs[key], ep, st)
    rows = H.run_all(build, ARMS)
    label_change = [{"case": "D3a", "amount": 60, "historical_label": "unverifiable (outside 'authorized'; not counted as authorized withheld)",
                     "corrected_label": "authorized (the stated total of the request)"},
                    {"case": "D4 with unread balance", "amount": "50, 100", "historical_label": "unverifiable",
                     "corrected_label": "ambiguous (depends on the balance, which the case does not fix)"}]
    out = H.dump(ROOT / "REM_PROGENT_COMPETITIVE_2026_11_18" / "results" / "f_before_v2.json", rows, {"label_changes_F3": label_change})
    for arm, s in out["score"].items():
        print(arm, "authorized released", s["authorized_released"], "/", s["authorized_n"], "| unauthorized released", s["unauthorized_released"],
              "/", s["unauthorized_n"], s["unauthorized_released_cases"])


if __name__ == "__main__":
    main()
