"""Verify every DiD number inserted by make_did_edition.py against REM_DEFENSE_IN_DEPTH/results/*.json."""
import json, os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
R = lambda f: json.load(open(os.path.join(ROOT, "REM_DEFENSE_IN_DEPTH", "results", f)))  # noqa: E731
d, c, s, cost, d2 = R("did3_results.json"), R("did3_coverage_amend1.json"), R("sig2_detection.json"), R("did3_cost.json"), R("did2_results.json")
A = d["arms"]["POP-P"]
rows = {"No defense": "B0", "REM v1.0": "B1", "Authorization only (oracle)": "B2", "Authorization only (explicit parameters)": "B2e",
        "Provenance only": "B3", "Detection only": "B4", "Behavioral rules only": "B5", "Detection + behavioral": "B7",
        "Full REM-DiD": "B9", "Full REM-DiD without the learned decision": "B9n", "Full REM-DiD, learned decision only for unpinned calls": "B9p"}
ch4 = open(os.path.join(ROOT, "REM_FINAL_THESIS_CONSOLIDATION", "thesis_working_copy", "src", "CHAPTER_04_FINAL.md"), encoding="utf-8").read()
bad = []
for label, arm in rows.items():
    m = A[arm]
    want = f"| {label} | {m['successful_attacks']} | {m['benign_tasks_completed']} | {m['legit_sc_calls_withheld']:,} |"
    if want not in ch4:
        bad.append(want)
x = {"None": "X-all", "Provenance only": "X-only-PROV", "Detection only": "X-only-DET", "Behavioral rules only": "X-only-BEH",
     "Learned decision only": "X-only-LEARN", "All four": "X0", "All but provenance": "X-PROV", "All but detection": "X-DET",
     "All but behavioral rules": "X-BEH", "All but learned decision": "X-LEARN"}
for label, arm in x.items():
    if f"| {label} | {A[arm]['successful_attacks']} |" not in ch4:
        bad.append(label)
cov = c["coverage"]["POP-P"]
P2 = d2["populations"]["POP-P"]
checks = {
    "907 attack-labeled": cov["attack_sc_calls"] == 907, "888 by two": cov["covered_by_two_or_more"] == 888,
    "17 BEH only": cov["covered_by_exactly_one"]["BEH"] == 17,
    "68 benign cost": d["declared_contrasts"]["B9 vs B9n (ben)"]["A_minus_B"] == -68,
    "p 0.014": round(d["declared_contrasts"]["B9 vs B9n (ben)"]["p_signflip_cells"], 3) == 0.014,
    "cost 0 attacks all cells": all(r["successful_attacks"] == 0 for r in cost["rows"] if r["arm"] == "B9"),
    "cost max 124": max(r["benign_tasks_completed"] for r in cost["rows"] if r["arm"] == "B9") == 124,
    "DiD-2 131/90/669": (P2["REM-e:beh"]["successful_attacks"], P2["REM-e:act"]["successful_attacks"], P2["REM-e:beh+act"]["successful_attacks"]) == (131, 90, 669),
    "DiD-2 v1.1 653": P2["REM-t:no_beh+e:act"]["successful_attacks"] == 653,
    "legit docs 19/81": (s["legit_documents"]["D_fin"], s["legit_documents"]["n_segments"]) == (19, 81),
    "zero-width 0.0055": s["by_variant"]["zero_width"]["detectors"]["union"]["recall"] == 0.0055,
}
bad += [k for k, ok in checks.items() if not ok]
print("all DiD numbers verified" if not bad else f"MISMATCH: {bad}")
sys.exit(1 if bad else 0)
