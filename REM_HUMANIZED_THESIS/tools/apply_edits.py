"""Apply the humanization edit lists to the snapshot of the defence-ready thesis.

The snapshot in orig_src/ (copied from REM_DEFENCE_READY_THESIS at commit 7b50067) is never modified. Every edit is an
exact replacement (old must occur exactly once in the current text of its file) recorded in edits/*.py as
EDITS = [(file, old, new, category), ...], where file is a path relative to orig_src/ and category is
'A' (editorial) or 'B' (evidence-based correction). The edited files are written to src/, text_front/, references/.
"""
import glob
import importlib.util
import json
import os
import shutil
import sys

H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(H, 'orig_src')
texts = {}
for p in glob.glob(os.path.join(ORIG, '*', '*.md')):
    texts[os.path.relpath(p, ORIG)] = open(p, encoding='utf-8').read()

problems, counts, cats = [], {}, {}
def load(ef):
    """edits/*.py: EDITS list. edits/*.txt: blocks '@@@ <file> | <A|B>' / '<<<' old '===' new '>>>'."""
    if ef.endswith('.py'):
        spec = importlib.util.spec_from_file_location(os.path.basename(ef)[:-3], ef)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m.EDITS
    out, raw = [], open(ef, encoding='utf-8').read()
    for blk in raw.split('@@@ ')[1:]:
        head, rest = blk.split('\n', 1)
        f, cat = [x.strip() for x in head.split('|')]
        old = rest.split('<<<\n', 1)[1].split('\n===\n', 1)[0]
        new = rest.split('\n===\n', 1)[1].split('\n>>>', 1)[0]
        out.append((f, old, new, cat))
    return out


for ef in sorted(glob.glob(os.path.join(H, 'edits', '*.py')) + glob.glob(os.path.join(H, 'edits', '*.txt'))):
    for i, e in enumerate(load(ef)):
        f, old, new, cat = e
        if f not in texts:
            problems.append(f'{os.path.basename(ef)}#{i}: unknown file {f}')
            continue
        n = texts[f].count(old)
        if n != 1:
            problems.append(f'{os.path.basename(ef)}#{i}: {f}: old matches {n} times: {old[:70]!r}')
            continue
        texts[f] = texts[f].replace(old, new)
        counts[f] = counts.get(f, 0) + 1
        cats[cat] = cats.get(cat, 0) + 1

for f, t in texts.items():
    out = os.path.join(H, f)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(t)
json.dump({'edits_per_file': counts, 'edits_per_category': cats, 'problems': problems},
          open(os.path.join(H, 'audit', 'apply_edits.json'), 'w'), indent=1)
print('edits applied:', sum(counts.values()), counts, cats)
if problems:
    print('PROBLEMS:'); print('\n'.join(problems)); sys.exit(1)
