"""Assemble the eighth edition (R8, 19 November 2026) from the assembled seventh edition (R7) plus dated new text.

usage: python3 REM_FINAL_SUBMISSION/thesis_r8/tools/make_r8.py        (from any directory)

Base (read only): REM_FINAL_SUBMISSION/thesis_r7/src/*.md and thesis_r7/text_front/*.md (R7 is not changed)
New text        : thesis_r8/text_r8/*.md  (new tables/figures use placeholder numbers 4.N1, 4.N2, ...)
Spec            : spec_r8.py  (REPLACE_UNIT, INSERT_BEFORE, EDITS, FRONT_EDITS)
Output          : thesis_r8/src/*.md, thesis_r8/text_front/*.md, audit/r8_renumbering.json, audit/r8_check.txt

Section numbers of R7 do not change: the replaced unit keeps its number and the inserted units are new last subsections of
Section 4.5. Existing table numbers are kept (the supplement cites them) and new tables take lettered numbers (4.11a ...); figures of
Chapter 4 are renumbered in order of appearance; every reference of the form
"Table(s) 4.x" / "Figure(s) 4.x" in every file is rewritten through the map. References to the supplement ("S-...") are
never touched. Equations are not touched (checked).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import spec_r8 as SP  # noqa: E402

TH = os.path.abspath(os.path.join(HERE, '..'))
R7 = os.path.join(TH, '..', 'thesis_r7')
FILES = ['CHAPTER_01_FINAL', 'CHAPTER_02_FINAL', 'CHAPTER_03_FINAL', 'CHAPTER_04_FINAL', 'CHAPTER_05_FINAL', 'APPENDICES_FINAL']
PROBLEMS = []


def frag(name):
    return open(os.path.join(TH, 'text_r8', name), encoding='utf-8').read().strip('\n')


text = {f: open(os.path.join(R7, 'src', f + '.md'), encoding='utf-8').read() for f in FILES}
base_eq = sorted(set(re.findall(r'\((\d+\.\d+)\)\s*\$\$', '\n'.join(text.values()))))

# ------------------------------------------------------------------ replace whole units (heading line to next heading of level <= its own)
for f, heading_prefix, name in SP.REPLACE_UNIT:
    L = text[f].split('\n')
    idx = [i for i, l in enumerate(L) if l.startswith(heading_prefix)]
    if len(idx) != 1:
        PROBLEMS.append(f'REPLACE anchor not unique: {heading_prefix} ({len(idx)})')
        continue
    i = idx[0]
    lvl = len(heading_prefix.split(' ')[0])
    j = i + 1
    while j < len(L) and not (re.match(r'^#{1,%d} ' % lvl, L[j])):
        j += 1
    text[f] = '\n'.join(L[:i] + frag(name).split('\n') + [''] + L[j:])

# ------------------------------------------------------------------ insert new units before an anchor heading
for f, anchor, names in SP.INSERT_BEFORE:
    if text[f].count(anchor) != 1:
        PROBLEMS.append(f'INSERT anchor not unique: {anchor}')
        continue
    text[f] = text[f].replace(anchor, '\n\n'.join(frag(n) for n in names) + '\n\n' + anchor, 1)

# ------------------------------------------------------------------ dated exact edits
for f, old, new in SP.EDITS:
    n = text[f].count(old)
    if n != 1:
        PROBLEMS.append(f'EDIT matches {n} times in {f}: {old[:80]!r}')
        continue
    text[f] = text[f].replace(old, new, 1)

# ------------------------------------------------------------------ renumber Chapter 4 tables and figures
TOK = r'4\.(?:N\d+|\d+[a-z]?)'
maps = {}
for kind, cap in (('Table', r'^\*\*Table (' + TOK + r')\.'), ('Figure', r'^!\[Figure (' + TOK + r')\.')):
    found = re.findall(cap, text['CHAPTER_04_FINAL'], flags=re.M)
    if len(found) != len(set(found)):
        PROBLEMS.append(f'duplicate {kind} caption numbers: {found}')
    if kind == 'Table':
        # Existing table numbers are kept, because the printed supplement and earlier documents cite them; a new table
        # takes the number of the preceding existing table with a letter suffix (4.11a, 4.11b, ...).
        maps[kind], prev, k = {}, None, 0
        for old in found:
            if old.startswith('4.N'):
                k += 1
                maps[kind][old] = f'{prev}{"abcdefghij"[k - 1]}'
            else:
                maps[kind][old], prev, k = old, old, 0
    else:
        maps[kind] = {old: f'4.{k}' for k, old in enumerate(found, 1)}
REF = re.compile(r'\b(Tables?|Figures?)( )(' + TOK + r'(?:(?:, | and | to | or |–|-)' + TOK + r')*)')


def sub(m):
    kind = 'Table' if m.group(1).startswith('Table') else 'Figure'

    def one(t):
        if t not in maps[kind]:
            PROBLEMS.append(f'unresolved {kind} {t}: {m.string[max(0, m.start() - 50):m.end() + 20]!r}')
            return t
        return maps[kind][t]
    return m.group(1) + m.group(2) + re.sub(TOK, lambda x: one(x.group(0)), m.group(3))


for f in FILES:
    text[f] = REF.sub(sub, text[f])
left = re.findall(r'4\.N\d+', '\n'.join(text.values()))
if left:
    PROBLEMS.append(f'placeholders left: {sorted(set(left))}')
new_eq = sorted(set(re.findall(r'\((\d+\.\d+)\)\s*\$\$', '\n'.join(text.values()))))
if new_eq != base_eq:
    PROBLEMS.append(f'equation set changed {base_eq} -> {new_eq}')

os.makedirs(os.path.join(TH, 'src'), exist_ok=True)
os.makedirs(os.path.join(TH, 'text_front'), exist_ok=True)
os.makedirs(os.path.join(TH, 'audit'), exist_ok=True)
for f in FILES:
    open(os.path.join(TH, 'src', f + '.md'), 'w', encoding='utf-8').write(re.sub(r'\n{3,}', '\n\n', text[f]).strip('\n') + '\n')
for name in ('front_matter.md', 'abstract_en.md', 'abstract_ar.md'):
    t = open(os.path.join(R7, 'text_front', name), encoding='utf-8').read()
    for fn, old, new in SP.FRONT_EDITS:
        if fn == name:
            n = t.count(old)
            if n != 1:
                PROBLEMS.append(f'FRONT EDIT matches {n} times in {name}: {old[:60]!r}')
            t = t.replace(old, new, 1)
    open(os.path.join(TH, 'text_front', name), 'w', encoding='utf-8').write(t)
json.dump({k: v for k, v in maps.items()}, open(os.path.join(TH, 'audit', 'r8_renumbering.json'), 'w'), indent=1)
open(os.path.join(TH, 'audit', 'r8_check.txt'), 'w').write('\n'.join(PROBLEMS) + ('\n' if PROBLEMS else 'no problems\n'))
words = {f: len(re.sub(r'[|#*`$\\{}]', ' ', text[f]).split()) for f in FILES}
print('words', words, 'total', sum(words.values()), '| tables ch4', len(maps['Table']), 'figures ch4', len(maps['Figure']),
      '| problems', len(PROBLEMS))
for p in PROBLEMS[:30]:
    print('  ', p)
