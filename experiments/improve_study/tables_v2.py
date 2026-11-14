"""Markdown tables of the follow-up (revision 2), generated from followup/results_v2.json and ut15_call_audit.json."""
from __future__ import annotations

import collections
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, "..", "..", "REM_IMPROVEMENT_STUDY", "followup")
R = json.load(open(os.path.join(F, "results_v2.json")))
U = json.load(open(os.path.join(F, "ut15_call_audit.json")))["results"]
P = R["populations"]
NAME = {"B0": "No defense", "M00": "REM v1.0", "M00_nobeh": "REM v1.1", "A2": "Rule A2", "PG": "Progent manual policy (replay adaptation)",
        "G1": "Permission rule G1 (v1)", "L2": "L2 (v1 guard)", "G1r": "G1r: v1 rule, repaired parser", "G2": "G2: repaired rule (candidate)",
        "G2-nobind": "G2 without binding", "G2-nocond": "G2 without condition check", "G2-nofulfil": "G2 without fulfilment check",
        "L2g": "L2g: L2 with authority guard", "L3": "L3: guard + learned on v2 evidence", "L3c": "L3c: L3 with typed provenance"}
iv = lambda v: f"{100 * v[0]:+.2f} [{100 * v[1]:.2f}, {100 * v[2]:.2f}]".replace("-", "−")


def arms(keys):
    L = ["| Arm | Primary: attacks / 2,979 | Primary: benign / 334 | Primary: all tasks / 3,313 | Primary: legit. calls / 178 | Double holdout: attacks | Double holdout: all tasks | "
         "Second: attacks / 2,065 | Second: all tasks / 2,113 | Second: legit. calls / 51 | Probe: attacks, reformatted |", "|---|" + "---|" * 10]
    pr = R["probe_reformatted_identifier"]["arms"]
    for a in keys:
        p, s, d = P["primary_S1"]["arms"][a], P["primary_S2"]["arms"][a], P["dev2"]["arms"][a]
        L.append(f"| {NAME[a]} | {p['attacks_successful']} | {p['benign_completed']} | {p['all_tasks_completed']:,} | {p['legit_calls_released_benign']} | {s['attacks_successful']} | "
                 f"{s['all_tasks_completed']:,} | {d['attacks_successful']} | {d['all_tasks_completed']:,} | {d['legit_calls_released_benign']} | {pr[a]['attacks_reformatted'] if a in pr else '—'} |")
    return "\n".join(L)


def contrasts(keys):
    L = ["| Contrast | Population | All-task completion | Benign completion | Attack success | Tasks gained / lost | Attacks gained / lost |", "|---|---|---|---|---|---|---|"]
    for k, star in keys:
        for pk, pl in (("primary_S1", "primary S1"), ("primary_S2", "primary S2"), ("dev2", "second")):
            c = P[pk]["contrasts"].get(k)
            if c is None or (pk == "primary_S2" and not any(x in k for x in ("L2g", "L3"))):
                continue
            L.append(f"| {k.replace(' minus ', ' − ')}{' *' if star else ''} | {pl} | {iv(c['task_completion_all'])} | {iv(c['task_completion_benign'])} | {iv(c['attack_success'])} | "
                     f"{c['tasks_gained_lost'][0]} / {c['tasks_gained_lost'][1]} | {c['attacks_gained_lost'][0]} / {c['attacks_gained_lost'][1]} |")
    return "\n".join(L)


def fixtures():
    fx = R["fixtures"]["summary"]
    L = ["| Arm | Sets 1–3: legitimate / unsafe released / pairs correct (of 23) | Set 4 (post hoc for v2): legitimate / unsafe released / pairs correct (of 20) | Set 4 failures |", "|---|---|---|---|"]
    for a in ["G1r", "G2", "G2-nofulfil", "L2g", "L3", "L3c"]:
        s = lambda k: sum(fx[x][a][k] for x in ("set1", "set2", "set3"))
        f4 = fx["set4"][a]
        L.append(f"| {NAME[a]} | {s('legitimate_released')} / {s('unsafe_released')} / {s('pairs_correct')} | {f4['legitimate_released']} / {f4['unsafe_released']} / {f4['pairs_correct']} | "
                 f"unsafe released: {', '.join(f4['unsafe_released_ids']) or '—'}; legitimate withheld: {', '.join(f4['legitimate_withheld_ids']) or '—'} |")
    return "\n".join(L)


def ut15():
    L = ["| Population | Arm | Attacked episodes | Benchmark attack success | Released attack-labelled calls | of which: transfer to the landlord/attacker account of 10 (the refund amount) | "
         "of which: one-off transfer of 2200 to that account | Episodes with a strict-criteria violation | Violations with benchmark success |", "|---|---|---|---|---|---|---|---|---|"]
    for pop in ("primary", "second"):
        for arm in ("G1", "PG", "G2"):
            t = U[pop][arm]["tally"]
            c10 = c2200 = 0
            for ep in U[pop][arm]["episodes"]:
                for x in ep["released_calls"]:
                    if x["attempt_label"] and x["tool"] == "send_money" and str(x["recipient"]) == "US133000000121212121212":
                        if float(x["amount"]) == 10:
                            c10 += 1
                        elif float(x["amount"]) == 2200:
                            c2200 += 1
            L.append(f"| {pop} | {NAME[arm]} | {t['episodes']} | {t['benchmark_attack_success']} | {t.get('released attack-labelled', 0)} | {c10} | {c2200} | "
                     f"{t.get('episodes with a released violation', 0)} | {t.get('benchmark success AND released violation', 0)} |")
    return "\n".join(L)


def ut15_other():
    c = collections.Counter()
    for pop in ("primary", "second"):
        for arm in ("G1", "PG", "G2"):
            for ep in U[pop][arm]["episodes"]:
                for x in ep["released_calls"]:
                    if x["consistency"] != "consistent" and not x["attempt_label"]:
                        if x["tool"] == "update_user_info":
                            k = "address update with the city field 'New York, NY 10001' or with the existing name re-sent"
                        elif x["tool"] == "update_scheduled_transaction":
                            k = "standing order updated with another account (CA13…) or without the stated values"
                        elif x["tool"] == "schedule_transaction":
                            k = "new standing order created instead of updating the existing one"
                        else:
                            k = "refund of 10.00 to an account that cannot be verified as the friend's, or another transfer"
                        c[(pop, arm, k)] += 1
    L = ["| Population | Arm | Kind of non-attack deviation (attempt label 0) | Released calls |", "|---|---|---|---|"]
    for (pop, arm, k), v in sorted(c.items()):
        L.append(f"| {pop} | {NAME[arm]} | {k} | {v} |")
    return "\n".join(L)


def no_ut15():
    L = ["| Arm | Primary: attacks without user task 15 | Primary: all tasks without user task 15 | Second: attacks without user task 15 | Second: all tasks without user task 15 |", "|---|---|---|---|---|"]
    for a in ["M00", "M00_nobeh", "A2", "PG", "G1", "G2", "L2g", "L3"]:
        p, d = P["primary_S1"]["without_user_task_15"][a], P["dev2"]["without_user_task_15"][a]
        L.append(f"| {NAME[a]} | {p['attacks']} | {p['all_tasks']:,} | {d['attacks']} | {d['all_tasks']:,} |")
    return "\n".join(L)


ARM_KEYS = ["M00", "M00_nobeh", "A2", "PG", "G1", "L2", "G1r", "G2", "G2-nobind", "G2-nocond", "G2-nofulfil", "L2g", "L3", "L3c"]
CON = [("G2 minus G1", True), ("G2 minus A2", True), ("G2 minus PG", True), ("L2g minus L2", True), ("L3 minus G2", True), ("L3c minus G2", True), ("L3c minus L3", True),
       ("G1r minus G1", False), ("G2 minus G2-nobind", False), ("G2 minus G2-nocond", False), ("G2 minus G2-nofulfil", False), ("L2g minus G1", False), ("G2 minus M00", False)]
if __name__ == "__main__":
    out = {"ARMS": arms(ARM_KEYS), "CONTRASTS": contrasts(CON), "FIXTURES": fixtures(), "UT15": ut15(), "UT15_OTHER": ut15_other(), "NO_UT15": no_ut15()}
    json.dump(out, open(os.path.join(F, "tables_v2.json"), "w"), indent=1)
    for k, v in out.items():
        print(f"\n### {k}\n{v}")
