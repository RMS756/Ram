"""Assemble the sixth, condensed editorial edition (R6) from the assembled fifth edition (R5) plus dated new text.

usage: python3 REM_FINAL_SUBMISSION/thesis_r6/tools/make_r6.py          (from any directory)

Base (read only) : REM_FINAL_SUBMISSION/thesis_r5/src/*.md (assembled R5; not changed)
Spec             : spec_r6.py  (EDITS applied to the base text, units MOVED to the supplement, units whose body is REPLACED
                   by a shorter text, new units INSERTED)
New text         : REM_FINAL_SUBMISSION/thesis_r6/text_r6/*.md (written with unused temporary numbers x.90+ / Table x.90+)
Output           : thesis_r6/src/*.md (main text), thesis_r6/supplement/SUPPLEMENT_R6.md, audit/r6_source_map.json,
                   audit/r6_crossref_check.txt

Selection is at the level of whole numbered or unnumbered units; kept base text is copied verbatim except for the dated
EDITS listed in the spec. Sections, tables and figures are renumbered in order of appearance, and every cross-reference
is rewritten through explicit maps. A reference to a unit that moved to the supplement becomes "S-<R5 number>". The
supplement keeps R5 numbers with the prefix "S-" and contains a correspondence table. Unresolved references are listed;
equations are never moved or renumbered (checked).
"""
import json
import os
import re
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import spec_r6 as SP  # noqa: E402

TH = os.path.abspath(os.path.join(HERE, '..'))
R5 = os.path.join(TH, '..', 'thesis_r5', 'src')
TXT = os.path.join(TH, 'text_r6')
FILES = ['CHAPTER_01_FINAL', 'CHAPTER_02_FINAL', 'CHAPTER_03_FINAL', 'CHAPTER_04_FINAL', 'CHAPTER_05_FINAL', 'APPENDICES_FINAL']
HEAD = re.compile(r'^(#{1,4}) (.*)$')
NUMH = re.compile(r'^((?:[A-F]|\d+)(?:\.\d+)+) (.*)$')
APPH = re.compile(r'^Appendix ([A-F]): (.*)$')
PROBLEMS, LOG = [], []


def frag(name):
    return open(os.path.join(TXT, name), encoding='utf-8').read().strip('\n')


def parse(text):
    """Blocks: dict(level, id, title, lines). Preamble lines (before the first unit heading) form block id ''."""
    blocks, cur, fence, parents = [], {'level': 0, 'id': '', 'title': '', 'lines': []}, False, {}
    for line in text.split('\n'):
        if line.startswith('```'):
            fence = not fence
        m = None if fence else HEAD.match(line)
        if m and not line.startswith('# CHAPTER') and not (len(m.group(1)) == 1 and not APPH.match(m.group(2))):
            lvl, rest = len(m.group(1)), m.group(2)
            ma, mn = APPH.match(rest), NUMH.match(rest)
            if lvl == 1 and ma:
                bid, title = 'App-' + ma.group(1), ma.group(2)
            elif mn:
                bid, title = mn.group(1), mn.group(2)
            else:
                title = re.sub(r'\s*\{[^}]*\}\s*$', '', rest)
                bid = parents.get(lvl - 1, '?') + '#' + title
            parents[lvl] = bid
            blocks.append(cur)
            cur = {'level': lvl, 'id': bid, 'title': title, 'lines': [line]}
        else:
            cur['lines'].append(line)
    blocks.append(cur)
    return blocks


def subtree(blocks, i):
    j = i + 1
    while j < len(blocks) and blocks[j]['level'] > blocks[i]['level']:
        j += 1
    return j


# ------------------------------------------------------------------------------------------------ assemble
base = {f: open(os.path.join(R5, f + '.md'), encoding='utf-8').read() for f in FILES}
for f, old, new in SP.EDITS:
    n = base[f].count(old)
    if n != 1:
        PROBLEMS.append(f'EDIT not applied exactly once ({n}x) in {f}: {old[:80]!r}')
        continue
    base[f] = base[f].replace(old, new)
    LOG.append(('edit', f, old[:60]))

main, supp, srcmap = {}, [], OrderedDict()
used = set()
for f in FILES:
    blocks = parse(base[f])
    out, i = [], 0
    while i < len(blocks):
        b = blocks[i]
        j = subtree(blocks, i)
        if b['id'] in SP.MOVE:
            used.add(b['id'])
            for k in range(i, j):
                supp.append((f, blocks[k]))
                srcmap[blocks[k]['id']] = 'supplement'
            i = j
            continue
        if b['id'] in SP.REPLACE:
            used.add(b['id'])
            out.append(b['lines'][0] + '\n\n' + frag(SP.REPLACE[b['id']]) + '\n')
            orig = [dict(b, lines=[b['lines'][0] + ' (full text of R5)'] + b['lines'][1:])] + blocks[i + 1:j]
            for k, x in enumerate(orig):
                supp.append((f, x))
                srcmap[x['id']] = 'replaced; full text in supplement' if k == 0 else 'supplement'
            i = j
        else:
            out.append('\n'.join(b['lines']))
            srcmap.setdefault(b['id'], 'main')
            i += 1
    main[f] = out

# insertions after units that have children: place after the subtree end (second pass on text)
def place_after_subtree(f, anchor, text):
    blocks = parse('\n'.join(main[f]))
    for i, b in enumerate(blocks):
        if b['id'] == anchor:
            j = subtree(blocks, i)
            new = ['\n'.join(x['lines']) for x in blocks[:j]] + [text + '\n'] + ['\n'.join(x['lines']) for x in blocks[j:]]
            main[f] = new
            return True
    return False


inserted = set()
for anchor, name in SP.INSERT_AFTER:
    f = next((g for g in FILES if any(b['id'] == anchor for b in parse('\n'.join(main[g])))), None)
    if f and place_after_subtree(f, anchor, frag(name)):
        inserted.add(anchor)
        LOG.append(('insert_after_subtree', anchor, name))
for x in list(SP.MOVE) + list(SP.REPLACE) + [a for a, _ in SP.INSERT_AFTER]:
    if x not in used and x not in inserted:
        PROBLEMS.append(f'spec id not found: {x}')

text = {f: re.sub(r'\n{3,}', '\n\n', '\n'.join(main[f])) for f in FILES}
for f in FILES:
    for blk in supp:
        if blk[0] == f and '$$' in '\n'.join(blk[1]['lines']) and blk[1]['id'] not in getattr(SP, 'ALIAS', {}):
            PROBLEMS.append(f'moved unit contains an equation: {blk[1]["id"]}')

# ------------------------------------------------------------------------------------------------ renumber
SEC, TAB, FIG = {}, {}, {}
APPMAP = dict(SP.APPENDIX_RENAME)
for letter in 'ABCDEF':
    if letter not in APPMAP:
        APPMAP[letter] = 'S-' + letter


def renumber(f, t):
    out = []
    ch = None
    cnt = [0, 0, 0]
    tcount, fcount = {}, {}
    fence = False
    for line in t.split('\n'):
        if line.startswith('```'):
            fence = not fence
        m = None if fence else HEAD.match(line)
        if m:
            lvl, rest = len(m.group(1)), m.group(2)
            ma, mn = APPH.match(rest), NUMH.match(rest)
            if lvl == 1 and ma:
                ch = APPMAP[ma.group(1)]
                cnt = [0, 0, 0]
                line = f'# Appendix {ch}: {ma.group(2)}'
            elif mn and lvl in (2, 3):
                old = mn.group(1)
                if ch is None:
                    ch = old.split('.')[0]
                if lvl == 2:
                    cnt[0] += 1
                    cnt[1] = 0
                    new = f'{ch}.{cnt[0]}'
                else:
                    cnt[1] += 1
                    new = f'{ch}.{cnt[0]}.{cnt[1]}'
                if old in SEC and SEC[old] != new:
                    PROBLEMS.append(f'section number {old} seen twice')
                SEC[old] = new
                line = f'{m.group(1)} {new} {mn.group(2)}'
        mt = re.match(r'^(\*\*Table )((?:[A-F]|\d+)\.\d+)(\.)', line)
        if mt:
            old = mt.group(2)
            pre = old.split('.')[0]
            key = APPMAP.get(pre, pre) if pre.isalpha() else pre
            tcount[key] = tcount.get(key, 0) + 1
            TAB[old] = f'{key}.{tcount[key]}'
            line = mt.group(1) + TAB[old] + line[mt.end(2):]
        mf = re.match(r'^(!\[Figure )(\d+\.\d+)(\.)', line)
        if mf:
            old = mf.group(2)
            pre = old.split('.')[0]
            fcount[pre] = fcount.get(pre, 0) + 1
            FIG[old] = f'{pre}.{fcount[pre]}'
            line = mf.group(1) + FIG[old] + line[mf.end(2):]
        out.append(line)
    return '\n'.join(out)


text = {f: renumber(f, text[f]) for f in FILES}
moved_ids = {b['id'] for _, b in supp}
moved_tabs = set()
for _, b in supp:
    for line in b['lines']:
        mt = re.match(r'^\*\*Table ((?:[A-F]|\d+)\.\d+)\.', line)
        if mt:
            moved_tabs.add(mt.group(1))

TOK = r'(?:[A-F](?:\.\d+)*(?![A-Za-z])|\d+(?:\.\d+)+)'
SEP = r'(?:,\s+and\s+|,\s+or\s+|,\s*|\s+and\s+|\s+or\s+|\s*[–-]\s*|\s+to\s+)'
REF = re.compile(r'\b(Sections?|Tables?|Figures?|Appendix|Appendices|Eqs?\.|Equations?)(\s+)(' + TOK + r'(?:' + SEP + TOK + r')*)(?![\d])')


def map_token(kind, tok):
    if kind.startswith('Eq'):
        return tok
    if kind.startswith('Figure'):
        if tok in FIG:
            return FIG[tok]
        PROBLEMS.append(f'unresolved figure {tok}')
        return tok
    if kind.startswith('Table'):
        if tok in TAB:
            return TAB[tok]
        if tok in moved_tabs:
            return 'S-' + tok
        PROBLEMS.append(f'unresolved table {tok} in: {CTX[0][:120]}')
        return tok
    tok = getattr(SP, 'ALIAS', {}).get(tok, tok)
    if re.fullmatch(r'[A-F]', tok):
        return APPMAP[tok]
    if tok in SEC:
        return SEC[tok]
    if tok in moved_ids or tok.split('.')[0] in ('A', 'B', 'D', 'E'):
        return 'S-' + tok
    if re.fullmatch(r'\d+', tok.split('.')[0]) and tok.count('.') == 0:
        return tok
    PROBLEMS.append(f'unresolved section {tok} ({kind})')
    return tok


CTX = ['']


def rewrite(t):
    def sub(m):
        CTX[0] = m.string[max(0, m.start() - 60):m.end() + 40]
        kind, sp, lst = m.group(1), m.group(2), m.group(3)
        parts = re.split('(' + SEP + ')', lst)
        return kind + sp + ''.join(p if re.fullmatch(SEP, p) else map_token(kind, p) for p in parts)
    out = []
    for line in t.split('\n'):
        if HEAD.match(line) or line.startswith('**Table') or line.startswith('![Figure'):
            # captions and headings were renumbered above; references inside a caption are still rewritten
            if line.startswith('**Table') or line.startswith('![Figure'):
                head, rest = line.split('.', 2)[:2], line.split('.', 2)[2:]
                line = '.'.join(head) + ('.' + REF.sub(sub, rest[0]) if rest else '')
            out.append(line)
        else:
            out.append(REF.sub(sub, line))
    return '\n'.join(out)


text = {f: rewrite(text[f]) for f in FILES}
for f in FILES:
    open(os.path.join(TH, 'src', f + '.md'), 'w', encoding='utf-8').write(text[f].strip('\n') + '\n')
EQ = re.compile(r'\((\d+\.\d+)\)\s*\$\$')
eq5 = sorted(set(EQ.findall('\n'.join(base.values()))), key=lambda x: [int(y) for y in x.split('.')])
eq6 = sorted(EQ.findall('\n'.join(text.values())), key=lambda x: [int(y) for y in x.split('.')])
if eq5 != eq6:
    PROBLEMS.append(f'equation set changed: R5 {eq5} R6 {eq6}')
LOG.append(('equations', len(eq6)))

# ------------------------------------------------------------------------------------------------ supplement
S = ['# Supplement to the Sixth Edition (R6) {.unnumbered}', '',
     'This supplement holds the units of the fifth edition (R5, 17 November 2026) that the condensed sixth edition does not '
     'print, verbatim. Numbers inside it are **R5 numbers** with the prefix **S-**; the main text of R6 refers to these units '
     'as "Section S-x", "Table S-x" or "Supplement S-A". Cross-references inside a supplement unit use R5 numbers; the '
     'correspondence table below gives the R6 number of every R5 section and table that stayed in the main text. The '
     'complete R5 (`REM_FINAL_SUBMISSION/thesis_r5/`) is preserved unchanged.', '',
     '## Index of supplement units {.unnumbered}', '', '| Unit (R5 number) | Title | From |', '|---|---|---|']
for f, b in supp:
    if b['level'] in (1, 2, 3) and b['id'] and '#' not in b['id']:
        S.append(f"| S-{b['id'].replace('App-', '')} | {b['title'][:90]} | {f.replace('_FINAL', '').title()} |")
S += ['', '## Correspondence of R5 and R6 numbers (units kept in the main text) {.unnumbered}', '', '| R5 | R6 |', '|---|---|']
for o, n in SEC.items():
    if o != n:
        S.append(f'| Section {o} | Section {n} |')
for o, n in TAB.items():
    if o != n:
        S.append(f'| Table {o} | Table {n} |')
for o, n in FIG.items():
    if o != n:
        S.append(f'| Figure {o} | Figure {n} |')
S.append('')
for f, b in supp:
    lines = list(b['lines'])
    m = HEAD.match(lines[0])
    if m:
        lvl, rest = len(m.group(1)), m.group(2)
        ma, mn = APPH.match(rest), NUMH.match(rest)
        if lvl == 1 and ma:
            lines[0] = f'# Supplement S-{ma.group(1)}: {ma.group(2)} {{.unnumbered}}'
        elif mn:
            lines[0] = f"{'#' * max(lvl, 2)} S-{mn.group(1)} {mn.group(2)} {{.unnumbered}}"
        else:
            lines[0] = re.sub(r'\s*\{[^}]*\}\s*$', '', lines[0]) + ' {.unnumbered}'
    lines = [re.sub(r'^\*\*Table ((?:[A-F]|\d+)\.\d+)\.', r'**Table S-\1.', x) for x in lines]
    lines = [re.sub(r'^!\[Figure (\d+\.\d+)\.', r'![Figure S-\1.', x) for x in lines]
    S.append('\n'.join(lines))
open(os.path.join(TH, 'supplement', 'SUPPLEMENT_R6.md'), 'w', encoding='utf-8').write(re.sub(r'\n{3,}', '\n\n', '\n'.join(S)))

json.dump({'source_units': srcmap, 'sections': SEC, 'tables': TAB, 'figures': FIG, 'appendices': APPMAP, 'log': LOG},
          open(os.path.join(TH, 'audit', 'r6_source_map.json'), 'w'), indent=1, ensure_ascii=False)
open(os.path.join(TH, 'audit', 'r6_crossref_check.txt'), 'w').write('\n'.join(PROBLEMS) + ('\n' if PROBLEMS else 'no problems\n'))
words = {f: len(re.sub(r'[|#*`$\\{}]', ' ', text[f]).split()) for f in FILES}
print('words', words, 'total', sum(words.values()))
print('supplement units', len(supp), 'problems', len(PROBLEMS))
for p in PROBLEMS[:40]:
    print('  ', p)
