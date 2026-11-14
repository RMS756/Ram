"""Number audit of the text written for the second edition: every number in text/ch4_r2.md and in the new Chapter 3
fragment is looked up among the numbers of the result files. Unmatched numbers are printed for checking by hand."""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
SOURCES = ['REM_IMPROVEMENT_STUDY/results/improvement_results.json', 'REM_IMPROVEMENT_STUDY/results/failure_analysis.json', 'results/pilot_R4/e1_crossfit.json',
           'REM_FINAL_SUBMISSION/results/confirmatory_results.json', 'REM_Authorization_Generalization_Study/results/study_results.json',
           'REM_IMPROVEMENT_STUDY/protocol/SPLIT_MANIFEST.json', 'REM_IMPROVEMENT_STUDY/followup/results_v2.json', 'REM_IMPROVEMENT_STUDY/followup/ut15_call_audit.json']
pool = set()


def walk(o):
    if isinstance(o, dict):
        for v in o.values():
            walk(v)
    elif isinstance(o, (list, tuple)):
        for v in o:
            walk(v)
    elif isinstance(o, bool):
        return
    elif isinstance(o, int):
        pool.add(str(o))
    elif isinstance(o, float):
        for k in (1, 2, 3):
            pool.add(f'{abs(o):.{k}f}')
            pool.add(f'{abs(100 * o):.{k}f}')
        pool.add(f'{abs(o):g}')


for s in SOURCES:
    walk(json.load(open(os.path.join(ROOT, s))))
text = open(os.path.join(ROOT, 'REM_FINAL_SUBMISSION/thesis_r3/text/ch4_r2.md'), encoding='utf-8').read()
ch3 = open(os.path.join(ROOT, 'REM_FINAL_SUBMISSION/thesis_r3/text/ch3.md'), encoding='utf-8').read()
text += ch3[ch3.index('<!-- @frag ch3_permission -->'):]
text = re.sub(r'`[^`]*`', ' ', text)                                   # file names, commits
text = re.sub(r'(Sections?|Tables?|Equations?|Chapter|Procedure|Appendix|Figure)\s[\d.]+(?:(?:\s?[–-]\s?|,\s|\sand\s|\sto\s)[\d.]+)*', ' ', text)
text = re.sub(r'^#+ .*$|^\*\*Table [\d.]+\.', ' ', text, flags=re.M)
nums = re.findall(r'(?<![\w.])\d[\d,]*(?:\.\d+)?(?![\w])', text)
seen, miss = set(), []
for n in nums:
    c = n.replace(',', '').rstrip('.')
    if c in seen:
        continue
    seen.add(c)
    if c in pool or (c.isdigit() and int(c) <= 23):
        continue
    miss.append(c)
print('distinct numbers:', len(seen), '| not matched directly:', len(miss))
print(miss)
