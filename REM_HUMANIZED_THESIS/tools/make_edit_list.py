"""Write reports/EDIT_LIST.md: every humanization edit, in order, with file, category, before and after."""
import glob, os, sys
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(H, 'tools'))
from apply_edits import load  # noqa: E402  (apply_edits runs on import; it is idempotent)
ns = {'load': load}
out = ['# Complete list of edits (humanization and corrections)', '',
       'Generated from `edits/*.txt` by `tools/make_edit_list.py`. Category A: editorial; B: evidence-based correction. '
       'Every edit is an exact, unique replacement applied to the snapshot `orig_src/` by `tools/apply_edits.py`.', '']
n = 0
for ef in sorted(glob.glob(os.path.join(H, 'edits', '*.txt'))):
    out += [f'## {os.path.basename(ef)}', '']
    for f, old, new, cat in ns['load'](ef):
        n += 1
        out += [f'### {n}. `{f}` (category {cat})', '', '**Before:**', '', '> ' + old.replace('\n', '\n> '), '',
                '**After:**', '', '> ' + new.replace('\n', '\n> '), '']
open(os.path.join(H, 'reports', 'EDIT_LIST.md'), 'w', encoding='utf-8').write('\n'.join(out))
print('edits listed:', n)
