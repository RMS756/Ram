"""List reference entries that are not cited in the assembled thesis text (chapters, appendices, front matter).

A reference counts as cited if the surname of its first author occurs within 80 characters before its year
(with an optional letter suffix) anywhere in the text. Writes audit/citation_check.json.

usage: python3 REM_FINAL_SUBMISSION/thesis_r6/tools/check_citations.py [--prune]
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.join(HERE, '..')
REF = os.path.join(FIN, 'references', 'REFERENCES_FINAL.md')
text = ''
for p in sorted(glob.glob(os.path.join(FIN, 'src', '*.md'))) + sorted(glob.glob(os.path.join(FIN, 'text_front', '*.md'))):
    text += open(p, encoding='utf-8').read() + '\n'
text = re.sub(r'\s+', ' ', text)
blocks = open(REF, encoding='utf-8').read().split('\n\n')
entries = [(i, b) for i, b in enumerate(blocks) if re.match(r'^[^\W\d_*#]', b.strip()) and re.search(r'\((\d{4}[a-z]?|n\.d\.)[^)]*\)', b)]
uncited, cited = [], []
for i, b in entries:
    b1 = b.strip()
    sur = re.split(r',|\. \(', b1, 1)[0].strip()
    sur = {'European Parliament & Council of the European Union': 'European Parliament', 'OWASP Gen AI Security Project': 'OWASP'}.get(sur, sur)
    y = re.search(r'\((\d{4}[a-z]?|n\.d\.)', b1).group(1)
    pat = re.escape(sur) + r'.{0,80}?' + re.escape(y)
    (cited if re.search(pat, text) else uncited).append((i, sur, y, b1[:110]))
json.dump({'entries': len(entries), 'cited': len(cited), 'uncited': [u[1:] for u in uncited]},
          open(os.path.join(FIN, 'audit', 'citation_check.json'), 'w'), indent=1, ensure_ascii=False)
print('reference entries:', len(entries), 'cited:', len(cited), 'not cited:', len(uncited))
for u in uncited:
    print('  ', u[1], u[2], '|', u[3][:90])
if '--prune' in sys.argv and uncited:
    drop = {u[0] for u in uncited}
    open(REF, 'w', encoding='utf-8').write('\n\n'.join(b for i, b in enumerate(blocks) if i not in drop))
    print('pruned', len(drop), 'entries')
