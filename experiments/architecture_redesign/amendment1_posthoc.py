"""POST-HOC amendment 1 (after the frozen held-out probe run): defect in object-binding designators.

Defect found in the held-out probe HO4: words() tokenised account identifiers (e.g. 'GB82WEST...' -> 'west'), so an IBAN in
the request created a spurious designator and an authorised update was withheld (fail-safe direction). Fix: remove account
identifiers before extracting designators. Arm REM_B_fix = REM_B with the fix. Results are EXPLORATORY and do NOT enter the
frozen decision (08_FROZEN_EXPERIMENT_PROTOCOL.md). rem_arch.py is not edited (its hash stays valid).
usage: python3 amendment1_posthoc.py <out.json>
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rem_arch as RA  # noqa: E402
import seq_harness as SH  # noqa: E402

IBAN = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{8,30}\b")


class ObjectBindingFix(RA.ObjectBinding):
    def __init__(self, contracts):
        clauses = sorted({IBAN.sub(" ", c.clause) for c in contracts if "schedule_modify" in c.effects})
        self.designators = set().union(*[RA.words(c) for c in clauses]) if clauses else set()
        self.plural = any(RA.PLURAL.search(c) for c in clauses)


def build_fix(arm, ep, cell, extra, st):
    if arm != "REM_B_fix":
        return RA.build_cell(arm, ep, cell, extra, st)
    saved = RA.ObjectBinding
    RA.ObjectBinding = ObjectBindingFix
    try:
        return RA.make_guard(dict(RA.BASE), cell, ep, st)
    finally:
        RA.ObjectBinding = saved


def main(out):
    import heldout_probes as HPR
    import ledger_cases as LC
    import rs_run as V1R
    st = V1R.common.make_setup()
    cells, cs = V1R.J.load("cells"), V1R.C.load("cs_cells")
    key = ("S1", "injection_task_0")
    f = lambda a, ep: build_fix(a, ep, cells[key], cs[key], st)  # noqa: E731
    res = {}
    for name, cases in (("ledger_dev", LC.CASES), ("heldout_probes", HPR.CASES)):
        res[name] = SH.score(SH.run_all(f, ["REM_B", "REM_B_fix"], cases))
        for a, s in res[name].items():
            print(name, a, "auth", s["authorized_released"], "/", s["authorized_n"], "| unauth", s["unauthorized_released"], "| amb",
                  s["ambiguous_released"], "| auth withheld", s["authorized_withheld_cases"])
    Path(out).write_text(json.dumps({"status": "POST-HOC EXPLORATORY (amendment 1); not part of the frozen decision", **res}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
