"""Generate thesis_r4/text/ch4_r2.md for the condensed edition (R4).

Starts from the fragments of the second/third edition (ch4_r2_template.md via gen_ch4_r2), keeps the sections on tools,
training and setup, and REPLACES the five sections on the exploratory extension by three compact ones built on the
current rule (revision 3). Every table is generated from the result files of the three revisions.

usage: python3 REM_FINAL_SUBMISSION/thesis_r4/tools/gen_ch4_r4.py     (from the repository root)
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_ch4_r2 as G2  # noqa: E402  (fills the unchanged fragments; its output file is overwritten below)

ROOT = G2.ROOT
R3 = json.load(open(os.path.join(ROOT, 'REM_IMPROVEMENT_STUDY', 'followup_v3', 'results_v3.json')))
P, U15, n, iv = G2.P, G2.U15, G2.n, G2.iv
P3 = R3['populations']
NAME = dict(G2.NAME)
NAME.update({'G1': 'Permission rule, revision 1 (G1)', 'G2': 'Permission rule, revision 2 (G2)', 'G3': 'Permission rule, revision 3 (G3, current)',
             'G2-nobind': 'G2 without binding amounts to accounts', 'G3-noeffect': 'G3 without effect typing', 'G3-nocond': 'G3 without the condition check',
             'L2': 'Learned, guard on denied calls only (L2)', 'L2g': 'L2 with the authority guard (L2g)', 'L4': 'Authority guard, learned on revision-3 evidence (L4)',
             'V11d': 'REM v1.1 with the two-verdict decision (V11d)', 'A2': 'Rule A2', 'PG': 'Progent manual policy (replay adaptation)'})


def arm(pop, a):
    return P3[pop]['arms'][a] if a in P3[pop]['arms'] else P[pop]['arms'][a]


def con(pop, k):
    return P3[pop]['contrasts'][k] if k in P3[pop]['contrasts'] else P[pop]['contrasts'][k]


PROBE = dict(G2.R['probe_reformatted_identifier']['arms'])
PROBE.update(G2.R2['probe_reformatted_identifier']['arms'])
PROBE.update(R3['probe_reformatted_identifier']['arms'])


def t_main():
    L = ['| Arm | Primary: attacks / 2,979 | Primary: benign tasks / 334 | Primary: all tasks / 3,313 | Primary: legitimate calls released / 178 | Second: attacks / 2,065 | '
         'Second: all tasks / 2,113 | Second: legitimate calls released / 51 |', '|---|---|---|---|---|---|---|---|']
    for a in ['A2', 'PG', 'G1', 'G2', 'G3']:
        p, d = arm('primary_S1', a), arm('dev2', a)
        b = '**' if a in ('PG', 'G3') else ''
        L.append(f'| {b}{NAME[a]}{b} | {p["attacks_successful"]} | {p["benign_completed"]} | {n(p["all_tasks_completed"])} | {p["legit_calls_released_benign"]} | '
                 f'{d["attacks_successful"]} | {n(d["all_tasks_completed"])} | {d["legit_calls_released_benign"]} |')
    return '\n'.join(L)


def t_con(rows):
    L = ['| Contrast | Population | All-task completion | Benign task completion | Attack success | Tasks gained / lost | Attacks gained / lost |', '|---|---|---|---|---|---|---|']
    for key, lab, pops in rows:
        for pk, pl in pops:
            c = con(pk, key)
            L.append(f'| {lab} | {pl} | {iv(c["task_completion_all"])} | {iv(c["task_completion_benign"])} | {iv(c["attack_success"])} | '
                     f'{c["tasks_gained_lost"][0]} / {c["tasks_gained_lost"][1]} | {c["attacks_gained_lost"][0]} / {c["attacks_gained_lost"][1]} |')
    return '\n'.join(L)


def t_checks():
    L = ['| Rule | Primary: attacks / 2,979 | Primary: all tasks / 3,313 | Second: attacks / 2,065 | Second: all tasks / 2,113 | Probe: attacks, identifier reformatted |', '|---|---|---|---|---|---|']
    for a in ['G1', 'G2-nobind', 'G2', 'G3-noeffect', 'G3', 'G3-nocond']:
        p, d = arm('primary_S1', a), arm('dev2', a)
        L.append(f'| {NAME[a]} | {p["attacks_successful"]} | {n(p["all_tasks_completed"])} | {d["attacks_successful"]} | {n(d["all_tasks_completed"])} | {PROBE[a]["attacks_reformatted"]} |')
    return '\n'.join(L)


def t_learned():
    L = ['| Arm | S1: attacks / 2,979 | S1: all tasks / 3,313 | S2: all tasks | Second: attacks / 2,065 | Second: all tasks / 2,113 | Probe: attacks, identifier reformatted |', '|---|---|---|---|---|---|---|']
    for a in ['G3', 'V11d', 'L2', 'L2g', 'L4']:
        s1, d = arm('primary_S1', a), arm('dev2', a)
        s2 = P3['primary_S2']['arms'].get(a) or P['primary_S2']['arms'].get(a) or s1
        L.append(f'| {NAME[a]} | {s1["attacks_successful"]} | {n(s1["all_tasks_completed"])} | {n(s2["all_tasks_completed"])} | {d["attacks_successful"]} | {n(d["all_tasks_completed"])} | '
                 f'{PROBE[a]["attacks_reformatted"] if a in PROBE else "not run"} |')
    return '\n'.join(L)


def t_ut15():
    L = ['| Population | Arm | Successful attacks / attacked episodes | Released attack-labelled calls | Of these: 10 (the refund) to the landlord–attacker account | Of these: 2200 sent once to that account |',
         '|---|---|---|---|---|---|']
    for pop in ('primary', 'second'):
        for a in ('G1', 'PG', 'G2'):
            t = U15[pop][a]['tally']
            c10 = c22 = 0
            for ep in U15[pop][a]['episodes']:
                for x in ep['released_calls']:
                    if x['attempt_label'] and x['tool'] == 'send_money' and str(x['recipient']) == 'US133000000121212121212':
                        c10 += float(x['amount']) == 10
                        c22 += float(x['amount']) == 2200
            L.append(f'| {pop} | {NAME[a]} | {t["benchmark_attack_success"]} / {t["episodes"]} | {t.get("released attack-labelled", 0)} | {int(c10)} | {int(c22)} |')
        t = R3['user_task_15_G3'][pop]['tally']
        L.append(f'| {pop} | {NAME["G3"]} | {t["benchmark_attack_success"]} / {t["episodes"]} | {t.get("released attack-labelled", 0)} | 0 | 0 |')
        assert t.get('released attack-labelled', 0) == 0
    return '\n'.join(L)


def t_fix():
    f1, f2, f3 = G2.R['fixtures']['summary'], G2.R2['fixtures']['summary'], R3['fixtures']
    src = {'M00_nobeh': f1, 'A2': f1, 'PG': f1, 'G1': f1, 'G2': f2, 'G3': f3, 'L4': f3}
    L = ['| Arm | Sets 1–3: pairs correct / 23 | Sets 1–3: unsafe calls released | Set 4: pairs correct / 20 | Set 4: unsafe calls released |', '|---|---|---|---|---|']
    for a, f in src.items():
        s = lambda k: sum(f[x][a][k] for x in ('set1', 'set2', 'set3'))
        L.append(f'| {NAME[a]} | {s("pairs_correct")} | {s("unsafe_released")} | {f["set4"][a]["pairs_correct"]} | {f["set4"][a]["unsafe_released"]} |')
    return '\n'.join(L)


def zero_tasks(a):
    t = P3['primary_S1']['tasks_completed_by_user_task'][a]
    t2 = P3['dev2']['tasks_completed_by_user_task'][a]
    z = [u.split('_')[-1] for u in t if t[u][0] == 0 and t2[u][0] == 0]
    return ', '.join(z[:-1]) + ' and ' + z[-1]


p1 = lambda a: arm('primary_S1', a)
d2 = lambda a: arm('dev2', a)
g1 = G2.P['primary_S1']['arms']
VAL = {
    'R4_MAIN': t_main(),
    'R4_CON': t_con([('G3 minus A2', 'G3−A2*', [('primary_S1', 'primary'), ('dev2', 'second')]), ('G3 minus PG', 'G3−PG*', [('primary_S1', 'primary'), ('dev2', 'second')]),
                     ('G3 minus M00', 'G3−v1.0', [('primary_S1', 'primary'), ('dev2', 'second')])]),
    'R4_CHECKS': t_checks(), 'R4_LEARNED': t_learned(),
    'R4_LCON': t_con([('L4 minus G3', 'L4−G3*', [('primary_S1', 'primary, S1'), ('primary_S2', 'primary, S2'), ('dev2', 'second')]),
                      ('G3 minus G3-noeffect', 'G3−(no effect typing)*', [('primary_S1', 'primary'), ('dev2', 'second')]),
                      ('G3 minus G3-nocond', 'G3−(no condition check)*', [('primary_S1', 'primary'), ('dev2', 'second')])]),
    'R4_UT15': t_ut15(), 'R4_FIX': t_fix(), 'R4_ZERO': zero_tasks('G3'),
    'R4_DELEG': str(g1['G1']['all_tasks_completed'] - g1['G1-nodel']['all_tasks_completed']),
    'R4_NORM': str(g1['G1']['all_tasks_completed'] - g1['G1-nonorm']['all_tasks_completed']),
    'R4_EST': str(g1['G1']['all_tasks_completed'] - g1['G1-noest']['all_tasks_completed']),
    'R4_AMT_T': str(g1['G1-noamt']['all_tasks_completed'] - g1['G1']['all_tasks_completed']),
    'R4_AMT_A': str(g1['G1-noamt']['attacks_successful'] - g1['G1']['attacks_successful']),
    'R4_PG_LEGIT': f'{p1("PG")["legit_calls_released_benign"]} of 178 against {p1("G3")["legit_calls_released_benign"]}; {d2("PG")["legit_calls_released_benign"]} of 51 against {d2("G3")["legit_calls_released_benign"]}',
}
NEW = open(os.path.join(HERE, 'ch4_r4_extension.md'), encoding='utf-8').read()
for k, v in VAL.items():
    assert f'§{k}§' in NEW, k
    NEW = NEW.replace(f'§{k}§', v)
assert '§' not in NEW, re.findall(r'§[^§]*§', NEW)[:3]
base = open(os.path.join(HERE, '..', 'text', 'ch4_r2.md'), encoding='utf-8').read()      # written by gen_ch4_r2 on import


def fragments(text):
    out, cur = {}, None
    order = []
    for line in text.split('\n'):
        m = re.match(r'^<!-- @frag (\S+) -->\s*$', line)
        if m:
            cur = m.group(1)
            out[cur] = []
            order.append(cur)
        elif cur is not None:
            out[cur].append(line)
    return {k: '\n'.join(v).strip('\n') for k, v in out.items()}, order


old, order = fragments(base)
new, _ = fragments(NEW)
keep90 = old['ch4_ablation_new'].split('## 4.91 ')[0].rstrip()                        # the summary of REM's own ablations is kept
new['ch4_ablation_new'] = keep90 + '\n\n' + new['ch4_ablation_new']
final = []
for name in order:
    if name in ('ch4_ablation_v2', 'ch4_followup'):
        continue                                                                     # merged into the three compact sections
    final.append(f'<!-- @frag {name} -->\n' + (new.get(name) or old[name]) + '\n')
open(os.path.join(HERE, '..', 'text', 'ch4_r2.md'), 'w', encoding='utf-8').write('\n'.join(final))
print('written text/ch4_r2.md (R4),', sum(len(x.split()) for x in final), 'words')
