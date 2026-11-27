"""Human label audit: agreement, adjudication check and sensitivity re-scoring.
Runs ONLY on completed human sheets; it refuses to run on empty sheets (no simulated annotations).

usage: python3 agreement_and_sensitivity.py
"""
import collections
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    return {r["blind_id"]: r for r in csv.DictReader(open(os.path.join(HERE, name)))}


def kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = collections.Counter(a), collections.Counter(b)
    pe = sum(pa[k] / n * pb[k] / n for k in set(pa) | set(pb))
    return None if pe == 1 else (po - pe) / (1 - pe)


def main():
    A, B = load("blind_annotation_sheet_annotator_A.csv"), load("blind_annotation_sheet_annotator_B.csv")
    done = [k for k in A if A[k]["label_0_1"] in ("0", "1") and B[k]["label_0_1"] in ("0", "1")]
    if not done:
        sys.exit("No completed human annotations found. This script never fabricates labels.")
    key = load("SEALED_KEY_do_not_open_before_annotation.csv")
    adj = load("adjudication_sheet.csv")
    la, lb = [int(A[k]["label_0_1"]) for k in done], [int(B[k]["label_0_1"]) for k in done]
    final = {k: int(adj[k]["final_label"]) if adj[k]["final_label"] in ("0", "1")
             else (la[i] if la[i] == lb[i] else None) for i, k in enumerate(done)}
    out = {"items_annotated_by_both": len(done), "cohen_kappa": kappa(la, lb),
           "raw_agreement": sum(x == y for x, y in zip(la, lb)) / len(done),
           "unadjudicated_disagreements": sum(v is None for v in final.values()), "by_stratum": {}}
    for s in sorted({key[k]["sample_stratum"] for k in done}):
        ks = [k for k in done if key[k]["sample_stratum"] == s and final[k] is not None]
        dis = sum(final[k] != int(key[k]["assigned_label"]) for k in ks)
        out["by_stratum"][s] = {"n": len(ks), "disagree_with_assigned_label": dis}
    # Sensitivity: list the episodes whose label changes; re-scoring must re-run the affected analyses with the
    # corrected labels (the analysis scripts take a label-override file: label_overrides.json).
    changed = {key[k]["episode_id"] + "#" + A[k]["step_index"]: final[k] for k in done
               if final[k] is not None and final[k] != int(key[k]["assigned_label"])}
    json.dump(changed, open(os.path.join(HERE, "label_overrides.json"), "w"), indent=1)
    json.dump(out, open(os.path.join(HERE, "agreement_report.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
