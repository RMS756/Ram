"""Generate thesis_r3/text/ch4_r2.md: the new text of Chapter 4 for the second edition.

Prose is in the template below. Every table of the extension study and the training table are generated from
the result files (REM_IMPROVEMENT_STUDY/results/improvement_results.json, results/pilot_R4/e1_crossfit.json);
no result number in a table is typed by hand. Numbers are in the base numbering extended with unused numbers
(sections 4.61-4.66 and 4.81-4.92, tables 4.61-4.75); make_final.py renumbers them.

usage: python3 REM_FINAL_SUBMISSION/thesis_r3/tools/gen_ch4_r2.py     (from the repository root)
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
R = json.load(open(os.path.join(ROOT, 'REM_IMPROVEMENT_STUDY', 'results', 'improvement_results.json')))
E1 = json.load(open(os.path.join(ROOT, 'results', 'pilot_R4', 'e1_crossfit.json')))
R2 = json.load(open(os.path.join(ROOT, 'REM_IMPROVEMENT_STUDY', 'followup', 'results_v2.json')))
U15 = json.load(open(os.path.join(ROOT, 'REM_IMPROVEMENT_STUDY', 'followup', 'ut15_call_audit.json')))['results']
P = R['populations']
for _k, _pop in R2['populations'].items():               # merge the follow-up arms and contrasts (earlier arms are identical)
    for _a, _m in _pop['arms'].items():
        P[_k]['arms'].setdefault(_a, _m)
    for _c, _v in _pop['contrasts'].items():
        P[_k]['contrasts'].setdefault(_c, _v)
    for _a, _v in _pop['held_out_credential_change'].items():
        P[_k]['held_out_credential_change'].setdefault(_a, {'attacks': _v})
NAME = {'B0': 'No defense', 'B1': 'B1', 'M00': 'REM v1.0', 'M00_nobeh': 'REM v1.1', 'M01': 'REM, Allow and Block only', 'P2': 'P2', 'A2': 'A2',
        'PG': 'Progent manual policy', 'A2n': 'A2 with typed normalization', 'G1': 'Permission rule G1', 'G1-noop': 'G1 without the operation check',
        'G1-noamt': 'G1 without the amount check', 'G1-noest': 'G1 without established payees', 'G1-nodel': 'G1 without scoped delegation',
        'G1-nonorm': 'G1 without typed normalization', 'V11d': 'REM v1.1 with the two-verdict decision (V11d)',
        'L0': 'Learned on permission evidence, no guard (L0)', 'L1': 'Guard, then learned, four verdicts (L1)',
        'L2': 'Guard, then learned, two verdicts (L2)', 'L2s': 'Guard; learned decides unknown calls only (L2s)',
        'G1r': 'G1 with the repaired parser (G1r)', 'G2': 'Repaired permission rule G2', 'G2-nobind': 'G2 without the binding check',
        'G2-nocond': 'G2 without the condition check', 'G2-nofulfil': 'G2 without the fulfilment check', 'L2g': 'L2 with the authority guard (L2g)',
        'L3': 'Authority guard, learned on v2 evidence (L3)', 'L3c': 'L3 with typed provenance (L3c)'}


def n(x):
    return f'{x:,}'


def iv(v):
    f = lambda x: f'{100 * x:.2f}'.replace('-', '−')
    p = f'{100 * v[0]:+.2f}'.replace('-', '−')
    return f'{p} [{f(v[1])}, {f(v[2])}]'


def main_table(key, arms):
    res = P[key]
    a_, b_ = res['n_attacked'], res['n_benign']
    L = [f'| Arm | Successful attacks / {n(a_)} | Episodes with a released attack-labelled call | Benign tasks completed / {b_} | All tasks completed / {n(a_ + b_)} | '
         f'Legitimate state-changing calls released / {res["arms"]["B0"]["legit_calls_n"]} |', '|---|---|---|---|---|---|']
    for a in arms:
        m = res['arms'][a]
        bold = '**' if a in ('G1', 'PG', 'G2') else ''
        L.append(f'| {bold}{NAME[a]}{bold} | {m["attacks_successful"]} | {m["episodes_with_released_attack_labelled_call"]} | {m["benign_completed"]} | '
                 f'{n(m["all_tasks_completed"])} | {m["legit_calls_released_benign"]} |')
    return '\n'.join(L)


def contrast_table(rows):
    L = ['| Contrast | Population | All-task completion | Benign task completion | Attack success | Tasks gained / lost | Attacks gained / lost |', '|---|---|---|---|---|---|---|']
    for key, lab, pops in rows:
        for pk, pl in pops:
            c = P[pk]['contrasts'][key]
            L.append(f'| {lab} | {pl} | {iv(c["task_completion_all"])} | {iv(c["task_completion_benign"])} | {iv(c["attack_success"])} | '
                     f'{c["tasks_gained_lost"][0]} / {c["tasks_gained_lost"][1]} | {c["attacks_gained_lost"][0]} / {c["attacks_gained_lost"][1]} |')
    return '\n'.join(L)


def ablation_table():
    L = ['| Rule | Primary: attacks / 2,979 | Primary: all tasks / 3,313 | Primary: legitimate calls released / 178 | Second: attacks / 2,065 | Second: all tasks / 2,113 | '
         'Second: legitimate calls released / 51 |', '|---|---|---|---|---|---|---|']
    for a in ['A2', 'A2n', 'G1', 'G1-noop', 'G1-noamt', 'G1-noest', 'G1-nodel', 'G1-nonorm']:
        p, d = P['primary_S1']['arms'][a], P['dev2']['arms'][a]
        L.append(f'| {NAME[a]} | {p["attacks_successful"]} | {n(p["all_tasks_completed"])} | {p["legit_calls_released_benign"]} | {d["attacks_successful"]} | '
                 f'{n(d["all_tasks_completed"])} | {d["legit_calls_released_benign"]} |')
    return '\n'.join(L)


def learned_table():
    pr = R['probe_reformatted_identifier']['arms']
    L = ['| Arm | S1: attacks / 2,979 | S1: all tasks / 3,313 | S2: attacks | S2: all tasks | Second population: attacks / 2,065 | Second population: all tasks / 2,113 | '
         'Held-out credential-change attacks, S1 / 334 |', '|---|---|---|---|---|---|---|---|']
    for a in ['M00_nobeh', 'V11d', 'G1', 'L0', 'L1', 'L2', 'L2s']:
        s1, s2, d = P['primary_S1']['arms'][a], P['primary_S2']['arms'][a], P['dev2']['arms'][a]
        L.append(f'| {NAME[a]} | {s1["attacks_successful"]} | {n(s1["all_tasks_completed"])} | {s2["attacks_successful"]} | {n(s2["all_tasks_completed"])} | '
                 f'{d["attacks_successful"]} | {n(d["all_tasks_completed"])} | {P["primary_S1"]["held_out_credential_change"][a]["attacks"]} |')
    return '\n'.join(L)


def probe_table():
    pr = dict(R['probe_reformatted_identifier']['arms'])
    pr.update(R2['probe_reformatted_identifier']['arms'])
    L = ['| Arm | Original text | Identifier reformatted |', '|---|---|---|']
    for a in ['PG', 'G1', 'G1-nonorm', 'L2', 'G2', 'L2g', 'L3', 'L3c']:
        L.append(f'| {NAME[a]} | {pr[a]["attacks_original_text"]} | {pr[a]["attacks_reformatted"]} |')
    return '\n'.join(L)


def fixture_table():
    fx = R['fixtures']['summary']
    L = ['| Arm | Sets 1–3: legitimate calls released / 23 | Sets 1–3: unsafe calls released / 23 | Sets 1–3: pairs correct / 23 | Set 4: legitimate released / 20 | '
         'Set 4: unsafe released / 20 | Set 4: pairs correct / 20 |', '|---|---|---|---|---|---|---|']
    for a in ['M00', 'M00_nobeh', 'B1', 'A2', 'PG', 'G1', 'G1-noamt', 'L0', 'L2']:
        s = lambda k: sum(fx[x][a][k] for x in ('set1', 'set2', 'set3'))
        L.append(f'| {NAME[a]} | {s("legitimate_released")} | {s("unsafe_released")} | {s("pairs_correct")} | {fx["set4"][a]["legitimate_released"]} | '
                 f'{fx["set4"][a]["unsafe_released"]} | {fx["set4"][a]["pairs_correct"]} |')
    assert sum(fx[x]['G1']['n'] for x in ('set1', 'set2', 'set3')) == 23 and fx['set4']['G1']['n'] == 20
    return '\n'.join(L)


def v2_table():
    pr = R2['probe_reformatted_identifier']['arms']
    L = ['| Arm | Primary: attacks / 2,979 | Primary: all tasks / 3,313 | Double holdout: all tasks | Second: attacks / 2,065 | Second: all tasks / 2,113 | Probe: attacks, identifier reformatted |',
         '|---|---|---|---|---|---|---|']
    for a in ['G1', 'G1r', 'G2', 'G2-nobind', 'G2-nocond', 'G2-nofulfil', 'L2', 'L2g', 'L3', 'L3c']:
        s1, d = P['primary_S1']['arms'][a], P['dev2']['arms'][a]
        s2 = P['primary_S2']['arms'].get(a, s1)
        prv = pr[a]['attacks_reformatted'] if a in pr else R['probe_reformatted_identifier']['arms'][a]['attacks_reformatted']
        L.append(f'| {NAME[a]} | {s1["attacks_successful"]} | {n(s1["all_tasks_completed"])} | {n(s2["all_tasks_completed"])} | {d["attacks_successful"]} | {n(d["all_tasks_completed"])} | {prv} |')
    return '\n'.join(L)


def ut15_table():
    L = ['| Population | Arm | Successful attacks / attacked episodes | Released attack-labelled calls | Of these: 10 (the refund) to the landlord–attacker account | Of these: 2200 sent once to that account |',
         '|---|---|---|---|---|---|']
    for pop, pl in (('primary', 'primary'), ('second', 'second')):
        for arm in ('G1', 'PG', 'G2'):
            t = U15[pop][arm]['tally']
            c10 = c22 = 0
            for ep in U15[pop][arm]['episodes']:
                for x in ep['released_calls']:
                    if x['attempt_label'] and x['tool'] == 'send_money' and str(x['recipient']) == 'US133000000121212121212':
                        c10 += float(x['amount']) == 10
                        c22 += float(x['amount']) == 2200
            L.append(f'| {pl} | {NAME[arm]} | {t["benchmark_attack_success"]} / {t["episodes"]} | {t.get("released attack-labelled", 0)} | {int(c10)} | {int(c22)} |')
    return '\n'.join(L)


def no_ut15_table():
    L = ['| Arm | Primary: attacks | Primary: all tasks | Second: attacks | Second: all tasks |', '|---|---|---|---|---|']
    for a in ['M00', 'M00_nobeh', 'A2', 'PG', 'G1', 'G2', 'L3']:
        p, d = R2['populations']['primary_S1']['without_user_task_15'][a], R2['populations']['dev2']['without_user_task_15'][a]
        L.append(f'| {NAME[a]} | {p["attacks"]} | {n(p["all_tasks"])} | {d["attacks"]} | {n(d["all_tasks"])} |')
    return '\n'.join(L)


def user_table():
    arms = ['B0', 'M00', 'M00_nobeh', 'A2', 'PG', 'G1', 'L2']
    t = P['primary_S1']['tasks_completed_by_user_task']
    L = ['| User task | Episodes | ' + ' | '.join(NAME[a] if a != 'L2' else 'L2' for a in arms).replace('Permission rule G1', 'G1').replace('Progent manual policy', 'Progent') + ' |',
         '|---|---|' + '---|' * len(arms)]
    for u in t['B0']:
        vals = [t[a][u][0] for a in arms]
        if len(set(vals[3:])) == 1 and vals[3] == vals[0]:      # A2, Progent, G1, L2 all equal to the undefended agent: omitted
            continue
        L.append(f'| {u.split("_")[-1]} | {t["B0"][u][1]} | ' + ' | '.join(str(v) for v in vals) + ' |')
    return '\n'.join(L)


def training_table():
    pf = E1['label_nll_primary']['per_fold']
    L = ['| Held-out attacker objective | Positive steps in the fitting portion | Selected λ (scale of Eq. 3.2) | Intercept β~0~ | γ~1~ | γ~0~ | Held-out steps | Held-out ROC-AUC | Held-out ECE |',
         '|---|---|---|---|---|---|---|---|---|']
    for k, v in pf.items():
        L.append(f'| {k.replace("injection_task_", "")} | {v["n_train_pos"]} | {v["lambda_chapter3_eq3_2_scale"]:g} | {v["intercept"]:.2f} | {v["gamma_1"]:.3f} | {v["gamma_0"]:.3f} | '
                 f'{v["n"]} | {v["roc_auc"]:.3f} | {v["ece"]:.3f} |'.replace('-', '−'))
    return '\n'.join(L)


p1, d2 = P['primary_S1']['arms'], P['dev2']['arms']
VAL = {
    'T_PRIMARY': main_table('primary_S1', ['A2', 'PG', 'G1', 'G2']),
    'T_SECOND': main_table('dev2', ['A2', 'PG', 'G1', 'G2']),
    'T_CONTRAST': contrast_table([('G1 minus A2', 'G1−A2*', [('primary_S1', 'primary'), ('dev2', 'second')]),
                                  ('G1 minus PG', 'G1−PG*', [('primary_S1', 'primary'), ('dev2', 'second')]),
                                  ('PG minus A2', 'PG−A2', [('primary_S1', 'primary'), ('dev2', 'second')]),
                                  ('G1 minus M00_nobeh', 'G1−v1.1*', [('primary_S1', 'primary'), ('dev2', 'second')]),
                                  ('G1 minus M00', 'G1−v1.0', [('primary_S1', 'primary'), ('dev2', 'second')]),
                                  ('G2 minus A2', 'G2−A2*', [('primary_S1', 'primary'), ('dev2', 'second')]),
                                  ('G2 minus PG', 'G2−PG*', [('primary_S1', 'primary'), ('dev2', 'second')])]),
    'T_ABLATION': ablation_table(),
    'T_LEARNED': learned_table(),
    'T_LCONTRAST': contrast_table([('L2 minus G1', 'L2−G1*', [('primary_S1', 'primary, S1'), ('primary_S2', 'primary, S2'), ('dev2', 'second')]),
                                   ('L2s minus G1', 'L2s−G1*', [('primary_S1', 'primary, S1'), ('primary_S2', 'primary, S2'), ('dev2', 'second')]),
                                   ('V11d minus M00_nobeh', 'V11d−v1.1*', [('primary_S1', 'primary, S1'), ('primary_S2', 'primary, S2'), ('dev2', 'second')]),
                                   ('L0 minus L2', 'L0−L2*', [('primary_S1', 'primary, S1'), ('primary_S2', 'primary, S2'), ('dev2', 'second')])]),
    'T_PROBE': probe_table(), 'T_V2': v2_table(), 'T_UT15': ut15_table(), 'T_NOUT15': no_ut15_table(),
    'T_V2CONTRAST': contrast_table([('G2 minus G1', 'G2−G1*', [('primary_S1', 'primary'), ('dev2', 'second')]),
                                    ('G2 minus G2-nobind', 'G2−(no binding)', [('primary_S1', 'primary'), ('dev2', 'second')]),
                                    ('G2 minus G2-nocond', 'G2−(no condition)', [('primary_S1', 'primary'), ('dev2', 'second')]),
                                    ('L2g minus L2', 'L2g−L2*', [('primary_S1', 'primary, S1'), ('primary_S2', 'primary, S2'), ('dev2', 'second')]),
                                    ('L3 minus G2', 'L3−G2*', [('primary_S1', 'primary, S1'), ('primary_S2', 'primary, S2'), ('dev2', 'second')]),
                                    ('L3c minus L3', 'L3c−L3*', [('primary_S1', 'primary, S1'), ('dev2', 'second')])]), 'T_FIXTURES': fixture_table(), 'T_USER': user_table(), 'T_TRAINING': training_table(),
}

TEMPLATE = open(os.path.join(HERE, 'ch4_r2_template.md'), encoding='utf-8').read()
out = TEMPLATE
for k, v in VAL.items():
    assert f'§{k}§' in out, k
    out = out.replace(f'§{k}§', v)
assert '§' not in out, 'unfilled placeholder'
open(os.path.join(HERE, '..', 'text', 'ch4_r2.md'), 'w', encoding='utf-8').write(out)
print('written text/ch4_r2.md,', len(out.split()), 'words')
