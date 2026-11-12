"""Assemble the FINAL five chapters from the verified five-chapter draft plus new, dated text.

usage: python3 REM_FINAL_SUBMISSION/thesis/tools/make_final.py          (from the repository root)

Base (read only): REM_FINAL_THESIS/final_five_chapters/src/*.md  (five-chapter draft of 3-5 November 2026)
New text        : REM_FINAL_SUBMISSION/thesis/text/*.md          (fragments, written in the base numbering extended
                  with unused numbers: new sections x.41+, new tables x.41+, new figures x.41+)
Spec            : spec_final.py (which base units are kept, which paragraphs are dropped, what moves to an appendix)
Output          : REM_FINAL_SUBMISSION/thesis/src/CHAPTER_0N_FINAL.md, APPENDICES_FINAL.md,
                  audit/final_source_map.json, audit/final_crossref_check.txt

Kept base text is copied verbatim (selection at the level of whole paragraphs, tables and subsections); every
section, table and figure number is then reassigned in order of appearance and every cross-reference is rewritten
through explicit maps. Unresolved references are listed, never silently left. No number, result or equation of the
base text is changed by this script.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from view import load, split_blocks  # noqa: E402
import spec_final as SP  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
TH = os.path.join(ROOT, 'REM_FINAL_SUBMISSION', 'thesis')
TEXT = os.path.join(TH, 'text')
OUT = os.path.join(TH, 'src')
AUD = os.path.join(TH, 'audit')
for d in (OUT, AUD):
    os.makedirs(d, exist_ok=True)
TITLES = {1: ('CHAPTER ONE', 'INTRODUCTION'),
          2: ('CHAPTER TWO', 'LITERATURE REVIEW: A RECORD-LEVEL SYSTEMATIC REVIEW OF RUNTIME SECURITY FOR TOOL-USING AI AGENTS'),
          3: ('CHAPTER THREE', 'RESEARCH METHODOLOGY, DESIGN AND IMPLEMENTATION OF THE REM FRAMEWORK'),
          4: ('CHAPTER FOUR', 'EXPERIMENTAL RESULTS AND DISCUSSION'),
          5: ('CHAPTER FIVE', 'CONCLUSIONS AND FUTURE WORK')}
LOG, PROBLEMS = [], []


# ------------------------------------------------------------------ fragments
def fragments():
    fr = {}
    for fn in sorted(os.listdir(TEXT)):
        if not fn.endswith('.md'):
            continue
        cur = None
        for line in open(os.path.join(TEXT, fn), encoding='utf-8').read().split('\n'):
            m = re.match(r'^<!-- @frag (\S+) -->\s*$', line)
            if m:
                cur = m.group(1)
                assert cur not in fr, f'duplicate fragment {cur}'
                fr[cur] = []
            elif cur is not None:
                fr[cur].append(line)
    return {k: '\n'.join(v).strip('\n') for k, v in fr.items()}


FR = fragments()


def frag(name):
    if name not in FR:
        sys.exit(f'missing fragment: {name}')
    return FR[name]


# ------------------------------------------------------------------ base text as a tree
def tree(ch):
    """{sec_num: {'title', 'pre': [blocks], 'subs': [(num, title, [blocks])]}} in order."""
    text = load(ch)
    parts = re.split(r'^(## .+)$', text, flags=re.M)
    out = {}
    for i in range(1, len(parts), 2):
        h = parts[i][3:].strip()
        m = re.match(r'(\d+\.\d+|Appendix \d+[A-Z])\.?\s+(.*)', h)
        num, title = (m.group(1), m.group(2)) if m else (h, h)
        sp = re.split(r'^(### .+)$', parts[i + 1], flags=re.M)
        subs = []
        for j in range(1, len(sp), 2):
            hh = sp[j][4:].strip()
            mm = re.match(r'(\d+(?:\.\d+)+)\s+(.*)', hh)
            subs.append((mm.group(1), mm.group(2), split_blocks(sp[j + 1])) if mm else (hh, hh, split_blocks(sp[j + 1])))
        out[num] = {'title': title, 'pre': split_blocks(sp[0]), 'subs': subs}
    return out


TREE = {c: tree(c) for c in (1, 2, 3, 4, 5)}


def clean(blocks, drop, where):
    keep = []
    for k, b in enumerate(blocks):
        if b.strip() == '---':
            continue
        if k in drop:
            continue
        keep.append(b)
    bad = [k for k in drop if k >= len(blocks)]
    if bad:
        sys.exit(f'drop index out of range in {where}: {bad}')
    return keep


def render_keep(ch, e):
    """e: dict(num, title=None, drop={unit: [idx]}, omit=[sub], repl={sub: frag}, after={unit: frag}, add={unit: frag}, before={unit: frag})."""
    num = e['num']
    if num not in TREE[ch]:
        sys.exit(f'base section {num} not found')
    s = TREE[ch][num]
    drop, omit = e.get('drop', {}), set(e.get('omit', []))
    repl, after, add, before = e.get('repl', {}), e.get('after', {}), e.get('add', {}), e.get('before', {})
    known = {num} | {x[0] for x in s['subs']}
    for d in (drop, repl, after, add, before):
        for k in d:
            if k not in known:
                sys.exit(f'unknown unit {k} in spec of {num}')
    for k in omit:
        if k not in known:
            sys.exit(f'unknown omitted unit {k} in spec of {num}')
    out = [f"## {num} {e.get('title') or s['title']}"]
    out += clean(s['pre'], set(drop.get(num, [])), num)
    if num in add:
        out.append(frag(add[num]))
    if num in after:
        out.append(frag(after[num]))
    LOG.append({'chapter': ch, 'base': num, 'action': 'kept', 'dropped_paragraphs': drop.get(num, [])})
    for sn, st, blocks in s['subs']:
        if sn in before:
            out.append(frag(before[sn]))
        if sn in omit:
            LOG.append({'chapter': ch, 'base': sn, 'action': 'omitted'})
            if sn in after:
                out.append(frag(after[sn]))
            continue
        if sn in repl:
            out.append(frag(repl[sn]))
            LOG.append({'chapter': ch, 'base': sn, 'action': 'replaced by new text', 'fragment': repl[sn]})
        else:
            out.append(f"### {sn} {e.get('subtitles', {}).get(sn) or st}")
            out += clean(blocks, set(drop.get(sn, [])), sn)
            if sn in add:
                out.append(frag(add[sn]))
            LOG.append({'chapter': ch, 'base': sn, 'action': 'kept', 'dropped_paragraphs': drop.get(sn, [])})
        if sn in after:
            out.append(frag(after[sn]))
    return '\n\n'.join(out)


def build_chapter(ch):
    parts = [f'# {TITLES[ch][0]}\n\n# {TITLES[ch][1]}']
    for e in SP.CHAPTERS[ch]:
        if 'new' in e:
            parts.append(frag(e['new']))
            LOG.append({'chapter': ch, 'base': None, 'action': 'new section', 'fragment': e['new']})
        else:
            parts.append(render_keep(ch, e))
    t = '\n\n'.join(parts) + '\n'
    for a, b in SP.REPLACE.get(ch, []):
        if a not in t:
            sys.exit(f'replacement anchor missing in chapter {ch}: {a[:70]!r}')
        t = t.replace(a, b)
    return t


def unit_blocks(ch, unit):
    sec = '.'.join(unit.split('.')[:2]) if not unit.startswith('Appendix') else unit
    s = TREE[ch][sec]
    if unit == sec:
        return s['title'], s['pre'], s['subs']
    for sn, st, blocks in s['subs']:
        if sn == unit:
            return st, blocks, []
    sys.exit(f'unit {unit} not found')


def build_appendices():
    parts, amap = [], {}
    for letter, title, items in SP.APPENDICES:
        parts.append(f'# Appendix {letter}: {title}')
        k = 0
        for it in items:
            if it[0] == 'frag':
                parts.append(frag(it[1]))
                continue
            k += 1
            if it[0] == 'unit':                       # ('unit', ch, base_num, title or None)
                _, ch, unit, ttl = it
                t0, blocks, subs = unit_blocks(ch, unit)
                parts.append(f'## {letter}.{k} {ttl or t0}')
                parts += clean(blocks, set(), unit)
                amap[unit] = f'{letter}.{k}'
                for j, (sn, st, bl) in enumerate(subs, 1):
                    parts.append(f'### {letter}.{k}.{j} {st}')
                    parts += clean(bl, set(), sn)
                    amap[sn] = f'{letter}.{k}.{j}'
                LOG.append({'chapter': ch, 'base': unit, 'action': f'moved to Appendix {letter}.{k}'})
            elif it[0] == 'block':                    # ('block', ch, unit, [idx, ...], title)
                _, ch, unit, idxs, ttl = it
                _, blocks, _ = unit_blocks(ch, unit)
                parts.append(f'## {letter}.{k} {ttl}')
                for idx in idxs:
                    parts.append(blocks[idx])
                LOG.append({'chapter': ch, 'base': f'{unit}{idxs}', 'action': f'moved to Appendix {letter}.{k}'})
    return '\n\n'.join(parts) + '\n', amap


# ------------------------------------------------------------------ assemble
CH = {c: build_chapter(c) for c in (1, 2, 3, 4, 5)}
APP, AMAP = build_appendices()
for a_, b_ in SP.GLOBAL_PRE:
    for c in CH:
        CH[c] = CH[c].replace(a_, b_)
    APP = APP.replace(a_, b_)
STRIP4 = lambda s: re.sub(r'^(#{4,6}) \d+(?:\.\d+)+\s+', r'\1 ', s, flags=re.M)   # deeper headings lose their old numbers
CH = {c: STRIP4(v) for c, v in CH.items()}
APP = STRIP4(APP)

# ------------------------------------------------------------------ renumber
SEC, TAB, FIG = {}, {}, {}
for c in (1, 2, 3, 4, 5):
    i = j = 0
    for m in re.finditer(r'^(#{2,3}) (\d+(?:\.\d+)+)\s', CH[c], flags=re.M):
        old = m.group(2)
        if len(m.group(1)) == 2:
            i += 1
            j = 0
            new = f'{c}.{i}'
        else:
            j += 1
            new = f'{c}.{i}.{j}'
        if old in SEC:
            sys.exit(f'duplicate heading number {old}')
        SEC[old] = new
    for k, m in enumerate(re.finditer(r'^\*\*Table (\d+\.\d+)\.', CH[c], flags=re.M), 1):
        if m.group(1) in TAB:
            sys.exit(f'duplicate table number {m.group(1)}')
        TAB[m.group(1)] = f'{c}.{k}'
    for k, m in enumerate(re.finditer(r'!\[Figure (\d+\.\d+)\.', CH[c]), 1):
        FIG[m.group(1)] = f'{c}.{k}'
for old, new in AMAP.items():
    SEC[old] = new
for old, tgt in SP.OVERRIDE.items():
    SEC[old] = SEC[tgt]
for letter, _, _ in SP.APPENDICES:
    seg = APP.split(f'# Appendix {letter}:', 1)[1]
    seg = re.split(r'^# Appendix [A-Z]:', seg, flags=re.M)[0]
    for k, m in enumerate(re.finditer(r'^\*\*Table (\d+\.\d+)\.', seg, flags=re.M), 1):
        TAB[m.group(1)] = f'{letter}.{k}'
    for k, m in enumerate(re.finditer(r'!\[Figure (\d+\.\d+)\.', seg), 1):
        FIG[m.group(1)] = f'{letter}.{k}'
for old, tgt in SP.REDIRECT.items():                  # dropped units -> a surviving base number
    if old not in SEC:
        if tgt not in SEC:
            sys.exit(f'redirect target {tgt} for {old} not in the final text')
        SEC[old] = SEC[tgt]
for old, tgt in SP.REDIRECT_TABLES.items():
    if old not in TAB:
        TAB[old] = TAB[tgt]

NUM = r'\d+(?:\.\d+)*[A-Z]?'
SEPS = r'(?:\s?[–-]\s?|,\s(?:and\s)?|\sand\s|\sto\s)'
LIST = rf'{NUM}(?:{SEPS}{NUM})*'
KW = r'(?:Sections?|Sec\.|§§?|Tables?|Figures?)'
PAT = re.compile(rf'(?P<combo>Chapters?\s(?P<cn>\d),?\s(?P<ikw>{KW})\s?(?P<inums>{LIST}))|(?P<simple>(?P<kw>{KW})(?P<sp>\s?)(?P<nums>{LIST}))')


def kind(kw):
    return 'tab' if kw.startswith('Table') else 'fig' if kw.startswith('Figure') else 'sec'


def map_list(k, nums, where):
    table = {'sec': SEC, 'tab': TAB, 'fig': FIG}[k]
    toks = re.split(rf'({SEPS})', nums)
    out = []
    for i, t in enumerate(toks):
        if i % 2:
            out.append(t)
        elif t in table:
            out.append(table[t])
        elif not re.match(r'^\d+\.\d+', t):
            out.append(t)                              # "Section 3", "Table 2" etc. are not numbered objects
        else:
            PROBLEMS.append(f'UNMAPPED {k} {t} in {where}: …{nums}')
            out.append(t)
    return ''.join(out), [o for i, o in enumerate(out) if i % 2 == 0]


def rewrite(text, home, where):
    def repl(m):
        if m.group('combo'):
            k = kind(m.group('ikw'))
            s, items = map_list(k, m.group('inums'), where)
            if k == 'sec' and all(re.match(r'^[A-Z]\.', x) for x in items):
                return 'Appendix ' + s
            if k == 'sec' and any(re.match(r'^[A-Z]\.', x) for x in items):
                PROBLEMS.append(f'MIXED appendix/section list in {where}: {m.group(0)}')
            first = items[0].split('.')[0]
            if first.isdigit() and int(first) == home:
                return f"{m.group('ikw')} {s}"
            return f"Chapter {first}, {m.group('ikw')} {s}" if first.isdigit() else f"{m.group('ikw')} {s}"
        k = kind(m.group('kw'))
        s, items = map_list(k, m.group('nums'), where)
        if k == 'sec' and all(re.match(r'^[A-Z]\.', x) for x in items):
            return 'Appendix ' + s
        if k == 'sec' and any(re.match(r'^[A-Z]\.', x) for x in items):
            PROBLEMS.append(f'MIXED appendix/section list in {where}: {m.group(0)}')
        return f"{m.group('kw')}{m.group('sp')}{s}"
    # headings first (their numbers are definitions, not references)
    text = re.sub(r'^(#{2,3}) (\d+(?:\.\d+)+)(\s)', lambda m: f'{m.group(1)} {SEC[m.group(2)]}{m.group(3)}', text, flags=re.M)
    lines = []
    for line in text.split('\n'):
        lines.append(line if re.match(r'^#{1,6} ', line) else PAT.sub(repl, line))
    return '\n'.join(lines)


FINAL = {c: rewrite(CH[c], c, f'chapter {c}') for c in (1, 2, 3, 4, 5)}
APPF = rewrite(APP, 0, 'appendices')
for a, b in SP.POST:
    hit = False
    for c in FINAL:
        if a in FINAL[c]:
            FINAL[c] = FINAL[c].replace(a, b)
            hit = True
    if a in APPF:
        APPF = APPF.replace(a, b)
        hit = True
    if not hit:
        sys.exit(f'post-replacement anchor missing: {a[:80]!r}')
for c in FINAL:
    FINAL[c] = re.sub(r'\n{3,}', '\n\n', FINAL[c])
    open(os.path.join(OUT, f'CHAPTER_0{c}_FINAL.md'), 'w', encoding='utf-8').write(FINAL[c])
APPF = re.sub(r'\n{3,}', '\n\n', APPF)
open(os.path.join(OUT, 'APPENDICES_FINAL.md'), 'w', encoding='utf-8').write(APPF)

# ------------------------------------------------------------------ checks
allt = '\n'.join(FINAL.values()) + '\n' + APPF
heads = set(re.findall(r'^#{2,3} ((?:\d+|[A-Z])(?:\.\d+)+)\s', allt, flags=re.M))
tabs = set(re.findall(r'^\*\*Table ((?:\d+|[A-Z])\.\d+)\.', allt, flags=re.M))
figs = set(re.findall(r'!\[Figure ((?:\d+|[A-Z])\.\d+)\.', allt))
eqs = set(re.findall(r'\\qquad \((\d+\.\d+)\)', allt))
bad = []
XN = r'(?:\d+|[A-Z])(?:\.\d+)+'
for m in re.finditer(rf'(Sections?|§§?|Tables?|Figures?|Appendix)\s?({XN}(?:{SEPS}{XN})*)', allt):
    kw = m.group(1)
    for n in re.split(SEPS, m.group(2)):
        ok = n in (tabs if kw.startswith('Table') else figs if kw.startswith('Figure') else heads)
        if not ok:
            bad.append((m.group(0), allt[max(0, m.start() - 70):m.start()].replace('\n', ' ')))
for m in re.finditer(r'(?:Equations?|Eqs?\.)\s?(' + LIST + ')', allt):
    for n in re.split(SEPS, m.group(1)):
        if re.match(r'^\d+\.\d+$', n) and n not in eqs:
            bad.append((m.group(0), allt[max(0, m.start() - 70):m.start()].replace('\n', ' ')))
words = {c: len(FINAL[c].split()) for c in FINAL}
with open(os.path.join(AUD, 'final_crossref_check.txt'), 'w', encoding='utf-8') as fh:
    fh.write(f'words per chapter: {words}; total {sum(words.values())}; appendices {len(APPF.split())}\n')
    fh.write(f'numbered headings: {len(heads)}; tables: {len(tabs)}; figures: {len(figs)}; equations: {len(eqs)}\n')
    fh.write(f'problems during rewriting: {len(PROBLEMS)}\n')
    for p in PROBLEMS:
        fh.write(f'  {p}\n')
    fh.write(f'unresolved references in the output: {len(bad)}\n')
    for b in bad:
        fh.write(f'  UNRESOLVED {b[0]!r} … {b[1]!r}\n')
json.dump({'log': LOG, 'section_map': SEC, 'table_map': TAB, 'figure_map': FIG},
          open(os.path.join(AUD, 'final_source_map.json'), 'w'), indent=1)
print(open(os.path.join(AUD, 'final_crossref_check.txt')).read()[:6000])
