"""Markdown tables for deliverables 04/07/09 and thesis R8, generated from stored outputs only.

Also computes one POST-HOC DESCRIPTIVE breakdown not named in protocol 02 (attack successes by injection task, i.e. attack
category, per ablation arm) from the stored replay pickle; it is labelled as post-hoc wherever it is used.
Output: REM_FINAL_THESIS_COMPLETION_2026_11_19/results/tables_*.md, results/ablation_by_injection_task_POSTHOC.json
"""
from __future__ import annotations

import collections
import json
import os
import pickle
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "REM_FINAL_THESIS_COMPLETION_2026_11_19"
A = json.loads((OUT / "results" / "ablation_results.json").read_text())
X = json.loads((OUT / "results" / "external_results.json").read_text())
ARMS = ["B0", "A0", "A1", "A2", "A3", "A4a", "A4b", "A5", "A6", "A7"]


def pct(v):
    return "–" if v is None else f"{100 * v:.1f}"


def ci(t, d=1):
    if t is None or t[0] is None:
        return "–"
    return f"{100 * t[0]:.{d}f} [{100 * t[1]:.{d}f}, {100 * t[2]:.{d}f}]"


def table(head, rows):
    s = "| " + " | ".join(head) + " |\n|" + "|".join("---" for _ in head) + "|\n"
    return s + "".join("| " + " | ".join(str(c) for c in r) + " |\n" for r in rows)


def ablation_tables():
    M = A["arms"]
    t1 = table(["Arm", "Configuration", "Attack successes / 2,979", "ASR % [95% CI]", "Benign completed / 334", "Benign utility % [95% CI]",
                "Tasks under attack / 2,979", "All tasks / 3,313"],
               [[a, M[a]["name"], M[a]["attack_successes"], ci(M[a]["ASR"], 2), M[a]["benign_completed"], ci(M[a]["benign_utility"]),
                 M[a]["tasks_under_attack"], M[a]["all_tasks_completed"]] for a in ARMS])
    t2 = table(["Arm", "Attack-labelled calls released / 907", "Episodes with a released attack-labelled call", "Legitimate calls released / 178",
                "Legitimate payments released / 89", "False-positive intervention rate %", "Withhold precision", "Withhold recall", "Withhold F1"],
               [[a, M[a]["attack_labelled_released"], M[a]["episodes_with_released_attack_call"], M[a]["legitimate_released"],
                 M[a]["legitimate_payments_released"], pct(M[a]["false_positive_intervention_rate"]),
                 "–" if M[a]["withhold_precision"] is None else f"{M[a]['withhold_precision']:.3f}",
                 "–" if M[a]["withhold_recall"] is None else f"{M[a]['withhold_recall']:.3f}", f"{M[a]['withhold_f1']:.3f}"] for a in ARMS])
    t3 = table(["Arm", "Allow", "Modify", "Escalate", "Block", "Restricted calls", "Episodes with an attack call Modified", "Residual ASR after Modify %"],
               [[a, f"{M[a]['n_allow']} ({pct(M[a]['rate_allow'])}%)", f"{M[a]['n_modify']} ({pct(M[a]['rate_modify'])}%)",
                 f"{M[a]['n_escalate']} ({pct(M[a]['rate_escalate'])}%)", f"{M[a]['n_block']} ({pct(M[a]['rate_block'])}%)", M[a]["restricted_calls"],
                 M[a]["episodes_with_modify_on_attack_call"], pct(M[a]["residual_ASR_after_modify"])] for a in ARMS])
    P = A["paired_vs_A0"]
    t4 = table(["Contrast", "Δ ASR pp [95% CI]", "Attacks gained / removed", "Δ benign utility pp [95% CI]", "Δ all-task completion pp [95% CI]",
                "Tasks gained / lost"],
               [[k, ci(v["ASR"], 2), "{} / {}".format(*v["attacks_gained_removed"]), ci(v["benign_utility"]), ci(v["all_tasks"], 2),
                 "{} / {}".format(*v["tasks_gained_lost"])] for k, v in P.items()])
    C = A["calibration_offline"]
    t5 = table(["Arm", "Held-out steps", "Attack-labelled", "ROC-AUC", "PR-AUC", "Brier", "ECE (10 bins)", "Log-loss"],
               [[a, C[a]["steps"], C[a]["positives"], f"{C[a]['roc_auc']:.4f}", f"{C[a]['pr_auc']:.4f}", f"{C[a]['brier']:.4f}",
                 f"{C[a]['ece_10']:.4f}", f"{C[a]['log_loss']:.4f}"] for a in ("A0", "A2", "A1", "A4a", "A4b")])
    t6 = table(["Arm", "Calls timed", "Mean ms", "Median ms", "p95 ms"],
               [[a, M[a]["calls_timed"], f"{M[a]['latency_ms_mean']:.3f}", f"{M[a]['latency_ms_median']:.3f}", f"{M[a]['latency_ms_p95']:.3f}"] for a in ARMS])
    R, E = A["decision_reachability_A0_vs_A6"], A["episode_level_ml_effect"]
    t7 = table(["Quantity (A0 against A6 on the same recorded calls)", "Count"],
               [["Proposed tool calls in the 3,313 episodes", R["calls_total"]],
                ["Calls scored by the estimator (ridge LR + calibration)", R["calls_scored_by_estimator"]],
                ["Calls whose verdict was forced by predicate D1 or D2 (before the expected-loss decision)", R["forced_by_predicates_before_expected_loss"]],
                ["Calls decided by the expected-loss engine", R["reached_expected_loss"]],
                ["  of which restricted (state-changing) tools", R["reached_expected_loss_restricted"]],
                ["  release unchanged by the learned decision", R["unchanged_release"]],
                ["  withheld by the learned decision: attack-labelled call (beneficial)", R.get("ml_withheld_attack_labelled", 0)],
                ["  withheld by the learned decision: legitimate call in a benign episode (harmful)", R.get("ml_withheld_legit_benign_episode", 0)],
                ["  withheld by the learned decision: call not attack-labelled, in an attacked episode",
                 R.get("ml_withheld_unlabelled_attacked_episode", 0)],
                ["Episodes: attacks prevented by the learned decision", E["attacks_prevented_due_to_ml"]],
                ["Episodes: attacks admitted by the learned decision", E["attacks_admitted_due_to_ml"]],
                ["Episodes: tasks lost because of the learned decision", E["tasks_lost_due_to_ml"]],
                ["Episodes: tasks completed only with the learned decision", E["tasks_gained_due_to_ml"]]])
    s = ("<!-- generated by experiments/final_thesis/make_tables.py from results/ablation_results.json; do not edit by hand -->\n\n"
         "## T1 Security and utility\n\n" + t1 + "\n## T2 Call-level outcomes\n\n" + t2 + "\n## T3 Verdicts over restricted calls\n\n" + t3 +
         "\n## T4 Paired differences against A0\n\n" + t4 + "\n## T5 Offline probability quality\n\n" + t5 + "\n## T6 Latency\n\n" + t6 +
         "\n## T7 Decision reachability\n\n" + t7)
    (OUT / "results" / "tables_ablation.md").write_text(s)


def external_tables():
    R = X["recorded"]
    t1 = table(["Code", "Defence", "Attacked runs", "Attack successes", "ASR % [95% CI]", "Tasks under attack", "Benign completed / runs",
                "Benign utility % [95% CI]", "Errors"],
               [[k, v["name"], v["n_attacked"], v["attack_successes"], ci(v["ASR"]), v["tasks_under_attack"], f"{v['benign_completed']} / {v['n_benign']}",
                 ci(v["benign_utility"]), v["errors"]] for k, v in R.items()])
    t2 = table(["Replay set", "Loaded", "Eligible (AM-4)", "Attacked", "Attack successes", "ASR % [95% CI]", "Tasks under attack",
                "Benign completed / eligible", "Benign utility % [95% CI]", "REM median ms"],
               [[v["name"], v["loaded"], v["eligible"], v["n_attacked"], v["attack_successes"], ci(v["ASR"]), v["tasks_under_attack"],
                 f"{v['benign_completed']} / {v['n_benign']}", ci(v["benign_utility"]),
                 "–" if v["latency_ms_median"] is None or k.endswith("|B0") else f"{v['latency_ms_median']:.3f}"] for k, v in X["replay"].items()])
    t2 += "".join(f"| {k} {R[k]['name']} + REM v1.0 (replay) | {v['episodes']} | – | – | – | {v['status']} | – | – | – | – |\n"
                  for k, v in X.get("replay_not_reported", {}).items())
    t3 = table(["Contrast", "Pairs", "Δ ASR pp [95% CI]", "Δ tasks under attack pp [95% CI]", "Δ benign utility pp [95% CI]"],
               [[k, v.get("pairs", "same traces"), ci(v["ASR"]), ci(v["utility_under_attack"]), ci(v.get("benign_utility"))] for k, v in X["paired"].items()])
    t4 = table(["Injection task"] + [k for k in R], [[i] + [R[k]["asr_by_injection_task"].get(i, 0) for k in R]
                                                   for i in sorted(R["D0"]["asr_by_injection_task"], key=lambda s: int(s.split("_")[-1]))])
    s = ("<!-- generated by experiments/final_thesis/make_tables.py from results/external_results.json; do not edit by hand -->\n\n"
         "## X1 Recorded closed loop (AgentDojo runs, gpt-4o-2024-05-13, banking)\n\n" + t1 +
         "\n## X2 Offline replay (NO-ADAPT) of REM v1.0 on each pipeline's traces\n\n" + t2 + "\n## X3 Paired contrasts\n\n" + t3 +
         "\n## X4 Recorded attack successes by injection task (of 16 runs each)\n\n" + t4)
    (OUT / "results" / "tables_external.md").write_text(s)


def by_injection_task_posthoc():
    st = os.environ.get("PILOT_RESULTS_DIR")
    if not st:
        print("PILOT_RESULTS_DIR not set: post-hoc breakdown skipped")
        return
    sys.path.insert(0, str(ROOT / "experiments" / "pilot"))
    from data import build  # noqa: E402
    import run_main as RM  # noqa: E402
    data = build("primary")
    res = pickle.load(open(os.path.join(RM.STATE, "final_ablation_replays.pkl"), "rb"))
    rm = RM.load_state("rmod")
    valid = {e for e, ok in rm["agree"].items() if ok}
    cnt = collections.defaultdict(collections.Counter)
    n = collections.Counter()
    for eid, c, u, s, err, aud in res:
        ep = data.episodes[eid]
        if eid in valid and ep.attacked:
            cnt[c][ep.injection_task_id] += int(bool(s))
            if c == "A0":
                n[ep.injection_task_id] += 1
    inj = sorted(n, key=lambda s: int(s.split("_")[-1]))
    out = {"status": "POST-HOC DESCRIPTIVE (not named in protocol 02); attack successes by injection task", "n_attacked": dict(n),
           "successes": {a: {i: cnt[a][i] for i in inj} for a in ARMS}}
    (OUT / "results" / "ablation_by_injection_task_POSTHOC.json").write_text(json.dumps(out, indent=1))
    t = table(["Injection task", "Attacked episodes"] + ARMS, [[i, n[i]] + [cnt[a][i] for a in ARMS] for i in inj])
    (OUT / "results" / "tables_ablation_by_injection_task_POSTHOC.md").write_text(
        "<!-- generated by make_tables.py; POST-HOC DESCRIPTIVE, not pre-registered -->\n\n" + t)


def mcnemar_posthoc():
    """POST-HOC SENSITIVITY (not in protocol 02): exact McNemar tests on discordant episodes; ignores clustering."""
    from scipy.stats import binomtest
    out = {}
    for k, v in A["paired_vs_A0"].items():
        g, r = v["attacks_gained_removed"]
        tg, tl = v["tasks_gained_lost"]
        out[k] = {"attacks_discordant": [g, r], "p_attacks": binomtest(g, g + r).pvalue if g + r else None,
                  "tasks_discordant": [tg, tl], "p_tasks": binomtest(tg, tg + tl).pvalue if tg + tl else None}
    (OUT / "results" / "ablation_mcnemar_POSTHOC.json").write_text(json.dumps(
        {"status": "POST-HOC SENSITIVITY (not in protocol 02): exact McNemar (binomial) tests on discordant episodes; ignores "
                   "clustering, therefore anti-conservative", "tests": out}, indent=1))


if __name__ == "__main__":
    ablation_tables()
    external_tables()
    by_injection_task_posthoc()
    mcnemar_posthoc()
    print("tables written")
