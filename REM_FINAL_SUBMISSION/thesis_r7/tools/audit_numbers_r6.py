"""Number audit of the text that is new in R6 (text_r6/*.md and the new side of every EDIT in spec_r6.py).

Each number must occur in a source: the result files of the repair study, of the competitive study and of earlier studies
(as stored), the R5 text (for numbers restated from it), or the close-work and bibliography records of 17 November 2026.
Numbers that occur in none are listed for manual inspection. Writes audit/number_audit_r6.json.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import spec_r6 as SP  # noqa: E402

TH = os.path.abspath(os.path.join(HERE, '..'))
ROOT = os.path.abspath(os.path.join(TH, '..', '..'))
new = '\n'.join(open(p, encoding='utf-8').read() for p in sorted(glob.glob(os.path.join(TH, 'text_r6', '*.md'))))
new += '\n' + '\n'.join(n for _, _, n in SP.EDITS)
new += '\n' + open(os.path.join(TH, 'text_front', 'abstract_en.md'), encoding='utf-8').read()
src = ''
for p in (glob.glob(os.path.join(ROOT, 'REM_REPAIR_STUDY_2026_11_17', 'results', '*.json'))
          + glob.glob(os.path.join(ROOT, 'REM_REPAIR_STUDY_2026_11_17', '*.md'))
          + glob.glob(os.path.join(ROOT, 'REM_COMPETITIVE_STUDY_2026_11_16', 'results', '*.json'))
          + glob.glob(os.path.join(ROOT, 'REM_REPAIR_STUDY_2026_11_17', 'results_v2', '*.json'))
          + glob.glob(os.path.join(ROOT, 'REM_FINAL_SUBMISSION', 'thesis_r5', 'src', '*.md'))
          + glob.glob(os.path.join(ROOT, 'REM_FINAL_SUBMISSION', 'thesis_r5', 'text_front', '*.md'))):
    src += open(p, encoding='utf-8').read() + '\n'
src_n = set(re.findall(r'\d[\d,]*(?:\.\d+)?', src))
src_n |= {x.replace(',', '') for x in src_n}
for x in list(src_n):                                                     # 0.0287 in JSON appears as 2.87 points in text
    try:
        v = float(x.replace(',', ''))
        src_n.add(f'{100 * v:.2f}')
        src_n.add(f'{abs(100 * v):.2f}')
    except ValueError:
        pass
found = sorted(set(re.findall(r'(?<![\w.])\d[\d,]*(?:\.\d+)?', new)))
missing = [n for n in found if n not in src_n and n.replace(',', '') not in src_n]
json.dump({'distinct_numbers_in_new_text': len(found), 'not_found_in_sources': missing},
          open(os.path.join(TH, 'audit', 'number_audit_r6.json'), 'w'), indent=1)
print('distinct numbers in new text:', len(found), '| not found in any source:', missing)
