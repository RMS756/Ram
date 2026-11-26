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

out = {'cells_checked': len(checks), 'mismatches': bad}
(D / 'audit' / 'thesis_number_check.json').write_text(json.dumps(out, indent=1))
print('cells checked:', len(checks), '| mismatches:', len(bad))
for b in bad:
    print('  ', b)
sys.exit(1 if bad else 0)
