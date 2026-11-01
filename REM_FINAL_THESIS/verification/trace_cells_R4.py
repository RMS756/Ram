"""Cell-level traceability check for the R4 chapters (review of 1 Nov 2026: semantic tracing).

usage: python3 REM_FINAL_THESIS/verification/trace_cells_R4.py   (from the repository root)

Unlike check_chapter_numbers.py, which accepts a number if it occurs anywhere in the result
files, every entry here names one table cell (table, row, column) or one sentence, and the one
JSON field that must produce it: file, configuration, semantics, reviewer condition and metric.
The printed value must equal the field rounded to the printed precision. An interval cell
'a [b, c]' must match the point estimate and both bounds.
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CH = os.path.join(ROOT, 'REM_FINAL_THESIS', 'chapters_R4')
R2 = os.path.join(ROOT, 'results', 'pilot_R2')
R4 = os.path.join(ROOT, 'results', 'pilot_R4')
J = {}


def field(path):
    """'dir:file.json:a.b[0].c' -> value."""
    d, f, p = path.split(':')
    key = (d, f)
    if key not in J:
        J[key] = json.load(open(os.path.join({'R2': R2, 'R4': R4}[d], f), encoding='utf-8'))
    o = J[key]
    for part in re.findall(r'[^.\[\]]+|\[\d+\]', p):
        o = o[int(part[1:-1])] if part.startswith('[') else o[part]
    return o


def tables(md):
    out, lines = {}, md.split('\n')
    for i, l in enumerate(lines):
        m = re.match(r'^\*\*(Table \d+\.\d+)\.', l)
        if not m:
            continue
        j = i + 1
        while j < len(lines) and not lines[j].startswith('|'):
            j += 1
        rows = []
        while j < len(lines) and lines[j].startswith('|'):
            rows.append([c.strip() for c in lines[j].strip().strip('|').split('|')])
            j += 1
        out[m.group(1)] = rows
    return out


NUM = r'[+\-−]?\d+(?:\.\d+)?'


def nums(cell):
    return [float(x.replace('−', '-')) for x in re.findall(NUM, cell.replace(',', ''))]


def decimals(cell):
    m = re.search(r'\d+\.(\d+)', cell)
    return len(m.group(1)) if m else 0


# (id, table, row-substrings, column-header substring, kind, json path(s), semantics note)
S = 'step-level'
SPEC = [
    # Table 5.3: held-out discrimination and calibration (e1_crossfit.json)
    ('5.3-auc', 'Table 5.3', ['ROC-AUC'], 'label-NLL', 'ci', ['R2:e1_crossfit.json:label_nll_primary.ci_roc_auc'], 'pooled held-out, calibrated (label-NLL)'),
    ('5.3-auc-platt', 'Table 5.3', ['ROC-AUC'], 'Platt smoothed', 'point', ['R2:e1_crossfit.json:platt_smoothed_secondary.pooled_calibrated.roc_auc'], 'Platt targets'),
    ('5.3-auc-unc', 'Table 5.3', ['ROC-AUC'], 'Uncalibrated', 'point', ['R2:e1_crossfit.json:label_nll_primary.pooled_uncalibrated.roc_auc'], 'uncalibrated'),
    ('5.3-ap', 'Table 5.3', ['Average precision'], 'label-NLL', 'ci', ['R2:e1_crossfit.json:label_nll_primary.ci_average_precision'], ''),
    ('5.3-ece', 'Table 5.3', ['ECE'], 'label-NLL', 'ci', ['R2:e1_crossfit.json:label_nll_primary.ci_ece'], ''),
    ('5.3-ece-unc', 'Table 5.3', ['ECE'], 'Uncalibrated', 'point', ['R2:e1_crossfit.json:label_nll_primary.pooled_uncalibrated.ece'], ''),
    ('5.3-ll', 'Table 5.3', ['Log-loss'], 'label-NLL', 'ci', ['R2:e1_crossfit.json:label_nll_primary.ci_log_loss'], ''),
    ('5.3-brier', 'Table 5.3', ['Brier'], 'label-NLL', 'point', ['R2:e1_crossfit.json:label_nll_primary.pooled_calibrated.brier_binary_SC5'], 'binary convention (SC-5)'),
    # Table 5.5: observe-only verdicts (no enforcement, no semantics)
    ('5.5-y1-rem', 'Table 5.5', ['y = 1 steps'], 'REM', 'ci', ['R2:e2_e5_e6_observe_only.json:verdicts.REM_step_level.ci_intervention_y1'], 'observe-only'),
    ('5.5-y1-noesc', 'Table 5.5', ['y = 1 steps'], 'w/o expected-loss', 'point', ['R2:e2_e5_e6_observe_only.json:verdicts.REMnoEsc_step_level.intervention_rate_y1'], 'observe-only'),
    ('5.5-y1-b1', 'Table 5.5', ['y = 1 steps'], 'B1', 'ci', ['R2:e2_e5_e6_observe_only.json:verdicts.B1.ci_intervention_y1'], 'observe-only'),
    ('5.5-y0-rem', 'Table 5.5', ['y = 0 steps (step'], 'REM', 'ci', ['R2:e2_e5_e6_observe_only.json:verdicts.REM_step_level.ci_step_fpr'], 'observe-only'),
    ('5.5-y0-noesc', 'Table 5.5', ['y = 0 steps (step'], 'w/o expected-loss', 'point', ['R2:e2_e5_e6_observe_only.json:verdicts.REMnoEsc_step_level.step_fpr'], 'observe-only'),
    ('5.5-y0-b1', 'Table 5.5', ['y = 0 steps (step'], 'B1', 'ci', ['R2:e2_e5_e6_observe_only.json:verdicts.B1.ci_step_fpr'], 'observe-only'),
    ('5.5-esc-rem', 'Table 5.5', ['Escalate share'], 'REM', 'point', ['R2:e2_e5_e6_observe_only.json:verdicts.REM_step_level.escalation_rate'], ''),
    ('5.5-esc-b1', 'Table 5.5', ['Escalate share'], 'B1', 'point', ['R2:e2_e5_e6_observe_only.json:verdicts.B1.escalation_rate'], ''),
    ('5.5-ideal-rem', 'Table 5.5', ['idealized reviewer'], 'REM', 'point', ['R2:e2_e5_e6_observe_only.json:verdicts.REM_step_level.y0_withheld_idealized'], ''),
    ('5.5-ideal-b1', 'Table 5.5', ['idealized reviewer'], 'B1', 'point', ['R2:e2_e5_e6_observe_only.json:verdicts.B1.y0_withheld_idealized'], ''),
    ('5.5-d2', 'Table 5.5', ['D2'], 'REM', 'point', ['R2:e2_e5_e6_observe_only.json:verdicts.REM_step_level.sources.D2'], ''),
]
# Table 5.7: replay, step-level semantics (reference)
for row, cfg in (('B0, no defense (replay)', 'B0'), ('B1, no reviewer', 'B1_step_level_no_reviewer'), ('REM, no reviewer', 'REM_step_level_no_reviewer'),
                 ('REM w/o expected-loss Escalate, no reviewer', 'REMnoEsc_step_level_no_reviewer'),
                 ('REM, idealized reviewer', 'REM_step_level_idealized'),
                 ('REM w/o expected-loss Escalate, idealized reviewer', 'REMnoEsc_step_level_idealized')):
    SPEC += [(f'5.7-{cfg}-asr', 'Table 5.7', ['| ' + row + ' |'], 'ASR', 'ci', [f'R2:e4_e5_enforcement_replay.json:configs.{cfg}.ASR'], S),
             (f'5.7-{cfg}-bu', 'Table 5.7', ['| ' + row + ' |'], 'Benign utility', 'ci', [f'R2:e4_e5_enforcement_replay.json:configs.{cfg}.benign_utility'], S),
             (f'5.7-{cfg}-ua', 'Table 5.7', ['| ' + row + ' |'], 'Utility under attack', 'point', [f'R2:e4_e5_enforcement_replay.json:configs.{cfg}.utility_under_attack[0]'], S)]
# Table 5.8: paired differences (step-level)
for row, key in (('REM − B1, no reviewer', 'REM_step_level_no_reviewer_minus_B1_step_level_no_reviewer'),
                 ('REM w/o Esc. − B1, no reviewer', 'REMnoEsc_step_level_no_reviewer_minus_B1_step_level_no_reviewer'),
                 ('REM − B1, idealized reviewer', 'REM_step_level_idealized_minus_B1_step_level_idealized'),
                 ('REM − B0, no reviewer', 'REM_step_level_no_reviewer_minus_B0')):
    SPEC += [(f'5.8-{key}-asr', 'Table 5.8', ['| ' + row], 'ΔASR', 'ci', [f'R2:e4_e5_enforcement_replay.json:paired_differences.{key}.ASR'], S),
             (f'5.8-{key}-bu', 'Table 5.8', ['| ' + row], 'ΔBenign', 'ci', [f'R2:e4_e5_enforcement_replay.json:paired_differences.{key}.benign_utility'], S)]
# Table 5.11: both semantics, matched reviewer assumptions
for cfg, label in (('B1', 'B1'), ('REM', 'REM'), ('REMnoEsc', 'REM w/o expected-loss Escalate')):
    for rev, rl in (('no_reviewer', 'no reviewer'), ('idealized', 'idealized reviewer')):
        for sem, sl in (('step_level', 'step-level'), ('episode_level', 'episode-level')):
            for col, m in (('ASR', 'ASR'), ('Benign utility', 'benign_utility'), ('Utility under attack', 'utility_under_attack')):
                SPEC.append((f'5.11-{cfg}-{rev}-{sem}-{m}', 'Table 5.11', [f'| {label}, {rl} | {sl}'], col, 'ci',
                             [f'R2:e4_e5_enforcement_replay.json:configs.{cfg}_{sem}_{rev}.{m}'], f'{sem}, {rev}'))
# Table 5.12: ablations (observe-only: held-out; replay: step-level, no reviewer)
for row, auc, ver, rep in (('Full REM', 'label_nll_primary.pooled_calibrated', 'REM_step_level', 'REM_step_level_no_reviewer'),
                           ('− context evidence', 'ablation_refits.no_ctx.pooled_calibrated', 'abl_no_ctx_step_level', 'abl_no_ctx_step_level_no_reviewer'),
                           ('− behavioral evidence', 'ablation_refits.no_beh.pooled_calibrated', 'abl_no_beh_step_level', 'abl_no_beh_step_level_no_reviewer'),
                           ('− action evidence', 'ablation_refits.no_act.pooled_calibrated', 'abl_no_act_step_level', 'abl_no_act_step_level_no_reviewer'),
                           ('− calibration', None, 'abl_no_calibration_step_level', 'abl_no_calibration_step_level_no_reviewer'),
                           ('− predicates', None, 'abl_no_predicates_step_level', 'abl_no_predicates_step_level_no_reviewer')):
    if auc:
        SPEC.append((f'5.12-{ver}-auc', 'Table 5.12', ['| ' + row], 'Held-out ROC-AUC', 'point', [f'R2:e1_crossfit.json:{auc}.roc_auc'], 'held-out'))
    SPEC += [(f'5.12-{ver}-y0', 'Table 5.12', ['| ' + row], 'intervention, y = 0', 'point', [f'R2:e2_e5_e6_observe_only.json:verdicts.{ver}.step_fpr'], 'observe-only'),
             (f'5.12-{ver}-y1', 'Table 5.12', ['| ' + row], 'intervention, y = 1', 'point', [f'R2:e2_e5_e6_observe_only.json:verdicts.{ver}.intervention_rate_y1'], 'observe-only'),
             (f'5.12-{rep}-asr', 'Table 5.12', ['| ' + row], 'Replay ASR', 'point', [f'R2:e4_e5_enforcement_replay.json:configs.{rep}.ASR[0]'], S + ', no reviewer'),
             (f'5.12-{rep}-bu', 'Table 5.12', ['| ' + row], 'Replay benign', 'point', [f'R2:e4_e5_enforcement_replay.json:configs.{rep}.benign_utility[0]'], S + ', no reviewer')]
tiers = [f'abl_single_tier{k}_step_level' for k in (1, 2, 3, 4)]
SPEC += [('5.12-tiers-y0', 'Table 5.12', ['one tier for all'], 'intervention, y = 0', 'list', [f'R2:e2_e5_e6_observe_only.json:verdicts.{t}.step_fpr' for t in tiers], 'observe-only'),
         ('5.12-tiers-y1', 'Table 5.12', ['one tier for all'], 'intervention, y = 1', 'list', [f'R2:e2_e5_e6_observe_only.json:verdicts.{t}.intervention_rate_y1' for t in tiers], 'observe-only'),
         ('5.12-tiers-asr', 'Table 5.12', ['one tier for all'], 'Replay ASR', 'list', [f'R2:e4_e5_enforcement_replay.json:configs.{t}_no_reviewer.ASR[0]' for t in tiers], S + ', no reviewer'),
         ('5.12-tiers-bu', 'Table 5.12', ['one tier for all'], 'Replay benign', 'list', [f'R2:e4_e5_enforcement_replay.json:configs.{t}_no_reviewer.benign_utility[0]' for t in tiers], S + ', no reviewer')]

# sentences: (id, file, regex with one group per value, paths, scale, decimals)
TEXT = [
    ('abs-auc', 'FRONT_MATTER_R4.md', r'pooled ROC-AUC (\d\.\d+)', ['R2:e1_crossfit.json:label_nll_primary.pooled_calibrated.roc_auc'], 1, 3),
    ('abs-rates', 'FRONT_MATTER_R4.md', r'intervened on (\d+\.\d)% of attack steps and on (\d+\.\d)% of legitimate steps, against (\d+\.\d)% and (\d+\.\d)%',
     ['R2:e2_e5_e6_observe_only.json:verdicts.REM_step_level.intervention_rate_y1', 'R2:e2_e5_e6_observe_only.json:verdicts.REM_step_level.step_fpr',
      'R2:e2_e5_e6_observe_only.json:verdicts.B1.intervention_rate_y1', 'R2:e2_e5_e6_observe_only.json:verdicts.B1.step_fpr'], 100, 1),
    ('abs-asr', 'FRONT_MATTER_R4.md', r'attack success rate was (\d\.\d+), against (\d\.\d+) for the baseline \(step-level mitigation; (\d\.\d+)',
     ['R2:e4_e5_enforcement_replay.json:configs.REM_step_level_no_reviewer.ASR[0]', 'R2:e4_e5_enforcement_replay.json:configs.B1_step_level_no_reviewer.ASR[0]',
      'R2:e4_e5_enforcement_replay.json:configs.B1_episode_level_no_reviewer.ASR[0]'], 1, 3),
]


def check():
    md = {f: open(os.path.join(CH, f), encoding='utf-8').read() for f in os.listdir(CH) if f.endswith('_R4.md')}
    T = tables(md['CHAPTER5_RESULTS_R4.md'])
    res = []
    for sid, tab, keys, col, kind, paths, note in SPEC:
        rows = T.get(tab)
        status, printed, expect = 'FAIL', '', ''
        if rows:
            header = rows[0]
            ci_ = next((i for i, h in enumerate(header) if col in h), None)
            line = next((r for r in rows[2:] if all(k in '| ' + ' | '.join(r) + ' |' for k in keys)), None)
            if line is not None and ci_ is not None:
                printed = line[ci_]
                vals = [field(p) for p in paths]
                d = decimals(printed)
                got = nums(printed)
                if kind == 'ci':
                    want = [round(float(x), d) for x in vals[0]]
                elif kind == 'list':
                    want = [round(float(x), d) for x in vals]
                else:
                    want = [round(float(vals[0]), d)]
                expect = want
                status = 'PASS' if [round(g, d) for g in got[:len(want)]] == want and len(got) >= len(want) else 'FAIL'
        res.append((status, sid, tab, col, printed, expect, ' ; '.join(paths), note))
    for sid, f, rx, paths, scale, d in TEXT:
        m = re.search(rx, md[f].replace('\n', ' '))
        status, printed, expect = 'FAIL', '', [round(float(field(p)) * scale, d) for p in paths]
        if m:
            printed = ' / '.join(m.groups())
            status = 'PASS' if [round(float(g), d) for g in m.groups()] == expect else 'FAIL'
        res.append((status, sid, f, rx[:40], printed, expect, ' ; '.join(paths), ''))
    return res


if __name__ == '__main__':
    res = check()
    out = os.path.join(ROOT, 'REM_FINAL_THESIS', 'verification', 'trace_cells_R4.txt')
    with open(out, 'w', encoding='utf-8') as fh:
        fh.write('status\tid\ttable/file\tcolumn\tprinted\texpected (rounded field)\tJSON field(s)\tsemantics / condition\n')
        for r in res:
            fh.write('\t'.join(str(x) for x in r) + '\n')
    fails = [r for r in res if r[0] != 'PASS']
    print(f'{len(res)} cells/sentences traced; {len(res) - len(fails)} PASS; {len(fails)} FAIL')
    for r in fails:
        print('FAIL', r[1:6])
    sys.exit(1 if fails else 0)
