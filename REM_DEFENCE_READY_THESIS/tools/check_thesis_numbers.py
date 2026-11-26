"""Cross-check the counts printed in the new tables of Sections 4.4 and 4.5 against the raw-record recomputation
(audit/number_verification.json, audit/call_level_verification.json, both written by verify_numbers.py).

usage: python3 REM_DEFENCE_READY_THESIS/tools/check_thesis_numbers.py      -> audit/thesis_number_check.json
Exit status 1 if any printed cell differs from the recomputed value.
"""
import json
import re
import sys
from pathlib import Path

D = Path(__file__).resolve().parents[1]
V = json.loads((D / 'audit' / 'number_verification.json').read_text())
C = json.loads((D / 'audit' / 'call_level_verification.json').read_text())
ch4 = (D / 'src' / 'CHAPTER_04_FINAL.md').read_text(encoding='utf-8')
S21, S19, S22 = V['S21_episode_level_ablation'], V['S19_decision_engine_subablations']['arms'], V['S22_offline_comparison']


def table(caption_start):
    L = ch4.split('\n')
    i = next(k for k, l in enumerate(L) if l.startswith(caption_start))
    while not L[i].startswith('|'):
        i += 1
    rows = []
    while i < len(L) and L[i].startswith('|'):
        rows.append([c.strip().strip('*') for c in L[i].strip().strip('|').split(' | ')])
        i += 1
    return rows[2:]


def n(cell):
    return int(cell.split('/')[0].replace(',', '').strip())


checks, bad = [], []


def eq(where, printed, expected):
    checks.append(where)
    if printed != expected:
        bad.append((where, printed, expected))


# Table of episode-level outcomes, primary population (variant -> source arm)
P1 = {'No defense': ('S21', 'B0'), 'Full REM v1.0': ('S21', 'A0'), 'A2a': ('S21', 'A1a'), 'A2b': ('S21', 'A1b'),
      'A3a': ('S21', 'A2'), 'A3b': ('S21', 'AIC'), 'A4a': ('S21', 'A3'), 'A4b': ('S21', 'A3P'), 'A5': ('S21', 'A4'),
      'A4c': ('S19', 'A2'), 'A4d': ('S19', 'A3'), 'A4e': ('S19', 'A5')}
for r in table('**Table 4.26.'):
    key = r[0].split(' −')[0].strip()
    src, arm = P1[key]
    if src == 'S21':
        a = S21['P1_primary']['arms'][arm]
        eq(f'4.26 {key} attacks', n(r[1]), a['attacks'])
        eq(f'4.26 {key} attack-call eps', n(r[2]), a['attack_call_released_eps'])
        eq(f'4.26 {key} utility under attack', n(r[3]), a['utility_under_attack'])
        eq(f'4.26 {key} benign', n(r[4]), a['benign_completed'])
        eq(f'4.26 {key} benign FP eps', n(r[5]), a['benign_fp_eps'])
        eq(f'4.26 {key} legit released', n(r[6]), a['benign_legit_calls_released'])
    else:
        a = S19[arm]
        eq(f'4.26 {key} attacks', n(r[1]), a['attacks'])
        eq(f'4.26 {key} benign', n(r[4]), a['benign_completed'])
        cl = V.get('S19_call_level_valid_P1', {}).get(arm)
        if cl:
            for col, k in ((2, 'attack_call_released_eps'), (3, 'utility_under_attack'), (5, 'benign_fp_eps'), (6, 'legit_released')):
                if k in cl:
                    eq(f'4.26 {key} {k}', n(r[col]), cl[k])

# Held-out templates and second population
P23 = {'No defense': 'B0', 'Full REM v1.0': 'A0', 'A2a': 'A1a', 'A2b': 'A1b', 'A3a': 'A2', 'A3b': 'AIC', 'A4a': 'A3', 'A4b': 'A3P', 'A5': 'A4'}
for r in table('**Table 4.28.'):
    arm = P23[r[0]]
    p2, p3 = S21['P2_cross_template']['arms'][arm], S21['P3_second_population']['arms'][arm]
    eq(f'4.28 {r[0]} P2 attacks', n(r[1]), p2['attacks'])
    eq(f'4.28 {r[0]} P2 utility', n(r[2]), p2['utility_under_attack'])
    eq(f'4.28 {r[0]} P3 attacks', n(r[3]), p3['attacks'])
    eq(f'4.28 {r[0]} P3 utility', n(r[4]), p3['utility_under_attack'])
    eq(f'4.28 {r[0]} P3 benign', n(r[5]), p3['benign_completed'])
    eq(f'4.28 {r[0]} P3 FP eps', n(r[6]), p3['benign_fp_eps'])

# Attack-labelled calls withheld
W = {'Full REM v1.0': ['A0'], 'A3b': ['AIC'], 'A2a, A2b, A4b': ['A1a', 'A1b', 'A3P'], 'A3a': ['A2'], 'A4a': ['A3']}
for r in table('**Table 4.29.'):
    if r[0] not in W:
        continue
    for arm in W[r[0]]:
        for col, pop in ((1, 'P1_primary'), (2, 'P2_cross_template'), (3, 'P3_second_population')):
            eq(f'4.29 {r[0]} {arm} {pop}', n(r[col]), C[pop][arm]['withheld'])

# REM against Progent's policy
PG = {('Primary', 'No defense'): ('P1_primary', 'B0'), ('Primary', 'REM v1.0'): ('P1_primary', 'A0'),
      ('Primary', 'REM predicates only'): ('P1_primary', 'A3'), ('Primary', 'Progent policy'): ('P1_primary', 'PG'),
      ('Held-out templates', 'No defense'): ('P2_cross_template', 'B0'), ('Held-out templates', 'REM v1.0'): ('P2_cross_template', 'A0'),
      ('Held-out templates', 'Progent policy'): ('P2_cross_template', 'PG'),
      ('Second population', 'No defense'): ('P3_second_population', 'B0'), ('Second population', 'REM v1.0'): ('P3_second_population', 'A0'),
      ('Second population', 'Progent policy'): ('P3_second_population', 'PG')}
for r in table('**Table 4.14.'):
    pop, arm = PG[(r[0], r[1])]
    a = S22[pop]['arms'][arm]
    eq(f'4.14 {r[0]} {r[1]} attacks', n(r[2]), a['attacks'])
    eq(f'4.14 {r[0]} {r[1]} attack-call eps', n(r[3]), a['attack_call_released_eps'])
    eq(f'4.14 {r[0]} {r[1]} utility', n(r[4]), a['utility_under_attack'])
    if r[5] != '–':
        eq(f'4.14 {r[0]} {r[1]} benign', n(r[5]), a['benign_completed'])
        eq(f'4.14 {r[0]} {r[1]} FP eps', n(r[6]), a['benign_fp_eps'])

# ---------------------------------------------------------------- paired tables: point, interval, discordant counts, p
NUM = r'([+−-]?\d+\.\d+)'
PCELL = re.compile(NUM + r'(?: \[' + NUM + r', ' + NUM + r'\])?(?:; (\d+) / (\d+))?(?:; p (?:= ([\d.]+)|< ([\d.]+)))?$')


def f(x):
    return float(x.replace('−', '-'))


def paired_cell(where, cell, d, cmp_ci=True):
    cell = cell.replace('**', '').strip()
    m = PCELL.match(cell)
    if not m:
        bad.append((where, cell, 'unparsed'))
        return
    pt, lo, hi, a, b, peq, plt = m.groups()
    def close(where2, printed, stored):     # printed to 1 or 2 decimals from a value stored to 2 decimals
        checks.append(where2)
        if abs(printed - stored) > 0.05 + 1e-9:
            bad.append((where2, printed, stored))
    close(where + ' point', f(pt), d['diff_pp'][0])
    if lo is not None and cmp_ci:
        close(where + ' ci lo', f(lo), d['diff_pp'][1])
        close(where + ' ci hi', f(hi), d['diff_pp'][2])
    if a is not None:
        eq(where + ' discordant', (int(a), int(b)), (d['arm_only'], d['ref_only']))
    if peq is not None:
        pr = d['mcnemar_p']
        nd = len(peq.split('.')[1]) if '.' in peq else 0
        checks.append(where + ' p')
        if pr is None or abs(round(pr, nd) - float(peq)) > 10 ** -nd + 1e-12:
            bad.append((where + ' p', peq, pr))
    if plt is not None:
        checks.append(where + ' p<')
        if d['mcnemar_p'] is None or d['mcnemar_p'] >= float(plt):
            bad.append((where + ' p<', plt, d['mcnemar_p']))


S21P = S21['P1_primary']['paired_vs_A0']
S19P = V['S19_decision_engine_subablations']['paired_vs_A0']
V2S21 = {'A2a': 'A1a', 'A2b': 'A1b', 'A3a': 'A2', 'A3b': 'AIC', 'A4a': 'A3', 'A4b': 'A3P', 'A5': 'A4'}
V2S19 = {'A4c': 'A2', 'A4d': 'A3', 'A4e': 'A5'}
COLS = ['attack', 'attack_call_released', 'utility_under_attack', 'benign_completion', 'benign_fp']
for r in table('**Table 4.27.'):
    v = r[0]
    for k, key in enumerate(COLS, 1):
        cell = r[k].replace('**', '').strip()
        if v in V2S21:
            paired_cell(f'4.27 {v} {key}', cell, S21P[V2S21[v]][key])
        elif key in ('attack', 'benign_completion') and cell != '–':
            paired_cell(f'4.27 {v} {key}', cell, S19P[V2S19[v]][key])
        elif 'against' in cell:
            x, y = re.findall(r'(\d+) against (\d+)', cell)[0]
            CL = V['S19_call_level_valid_P1']
            k19 = {'attack_call_released': 'attack_call_released_eps', 'benign_fp': 'benign_fp_eps'}[key]
            eq(f'4.27 {v} {key}', (int(x), int(y)), (CL[V2S19[v]][k19], CL['A0'][k19]))

# REM minus Progent
POPS = {'Primary': 'P1_primary', 'Held-out templates': 'P2_cross_template', 'Second population': 'P3_second_population'}
for r in table('**Table 4.15.'):
    d = S22[POPS[r[0]]]['paired']['A0-PG']
    for k, key in ((1, 'attack'), (2, 'utility_under_attack'), (3, 'benign_completion')):
        if r[k].strip() != '–':
            paired_cell(f'4.15 {r[0]} {key}', r[k], d[key])

# 19-Nov tables (relabelled): counts, rate intervals and paired differences
R19 = {'no defense': 'B0', 'A0 REM v1.0': 'A0', 'A0': 'A0', 'A3a': 'A1', 'A4c': 'A2', 'A4d': 'A3', 'A2a': 'A4a', 'A3b': 'A4b', 'A4e': 'A5', 'A4a': 'A6', 'A4b': 'A7'}
S19A = V['S19_decision_engine_subablations']['arms']
for r in table('**Table 4.30.'):
    a = R19[r[0].split(' −')[0].split(' thresholds')[0].strip()]
    eq(f'4.30 {a} attacks', n(r[1]), S19A[a]['attacks'])
    eq(f'4.30 {a} benign', n(r[3]), S19A[a]['benign_completed'])
    eq(f'4.30 {a} all tasks', n(r[5]), S19A[a]['all_tasks'])
    if a in V['S19_call_level_valid_P1']:
        eq(f'4.30 {a} legit calls', n(r[6]), V['S19_call_level_valid_P1'][a]['legit_released'])
for r in table('**Table 4.31.'):
    a = R19[r[0]]
    # no defense minus A0 is taken from the 21-Nov records, whose episodes are identical (cross-study identity)
    d = S19P[a] if a != 'B0' else S21P['B0']
    paired_cell(f'4.31 {a} attack', r[1] + '; ' + r[2].replace('/', ' / ').replace('  ', ' '), d['attack'], cmp_ci=True)
    paired_cell(f'4.31 {a} benign', r[3].replace('**', ''), d['benign_completion'])

out = {'cells_checked': len(checks), 'mismatches': bad}
(D / 'audit' / 'thesis_number_check.json').write_text(json.dumps(out, indent=1))
print('cells checked:', len(checks), '| mismatches:', len(bad))
for b in bad:
    print('  ', b)
sys.exit(1 if bad else 0)
