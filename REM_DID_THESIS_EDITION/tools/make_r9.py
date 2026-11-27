"""Assemble the defence-ready edition (R9, 26 November 2026) from the eighth edition (R8) plus new text.

usage: python3 REM_DEFENCE_READY_THESIS/tools/make_r9.py        (from any directory)

Base (read only): REM_FINAL_SUBMISSION/thesis_r8/src/*.md, thesis_r8/text_front/*.md, thesis_r8/references/REFERENCES_FINAL.md
New text        : REM_DEFENCE_READY_THESIS/text/ch4_44.md (Section 4.4) and ch4_45.md (Section 4.5)
Spec            : spec_r9.py (PRE_EDITS on R8 numbering, POST_EDITS on R9 numbering, FRONT_EDITS, REF_ADD)
Output          : REM_DEFENCE_READY_THESIS/src/*.md, text_front/*.md, references/REFERENCES_FINAL.md,
                  audit/r9_renumbering.json, audit/r9_check.txt

Steps (in this order):
 1. PRE_EDITS are applied to the R8 text (R8 section numbers).
 2. The bodies of the R8 units 4.4.1-4.4.4 and 4.5.1-4.5.6 are extracted (heading removed, internal headings demoted
    by one level). The body of 4.5.5 has its 19-November arm labels relabelled to the variant names of the new
    Table 4.N8 in one pass.
 3. Section references are remapped from the R8 to the R9 numbering in every R8 text and extracted body:
    4.4.1/4.4.2/4.4.3 -> 4.4.7, 4.4.4 -> 4.4.3, 4.5.1/4.5.2/4.5.5 -> 4.5.7, 4.5.3/4.5.4/4.5.6 -> 4.5.8.
    References to the supplement ("S-...") are never touched.
 4. The R8 units "## 4.4" and "## 4.5" are replaced by the new text; @@OLD[...]@@ placeholders take the bodies.
 5. POST_EDITS (R9 numbering); duplicate entries in reference lists ("Sections 4.4.7 and 4.4.7") are merged.
 6. Tables and figures of Chapter 4 are renumbered sequentially in order of appearance, and every reference of the
    form "Table(s) 4.x" / "Figure(s) 4.x" in every file is rewritten through the map (stored in the audit).
 Equations are not touched (checked).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import spec_r9 as SP  # noqa: E402

D = os.path.abspath(os.path.join(HERE, '..'))
ROOT = os.path.abspath(os.path.join(D, '..'))
R8 = os.path.join(ROOT, 'REM_FINAL_SUBMISSION', 'thesis_r8')
FILES = ['CHAPTER_01_FINAL', 'CHAPTER_02_FINAL', 'CHAPTER_03_FINAL', 'CHAPTER_04_FINAL', 'CHAPTER_05_FINAL', 'APPENDICES_FINAL']
PROBLEMS = []

text = {f: open(os.path.join(R8, 'src', f + '.md'), encoding='utf-8').read() for f in FILES}
base_eq = sorted(set(re.findall(r'\((\d+\.\d+)\)\s*\$\$', '\n'.join(text.values()))))


def edit_one(t, old, new, label, where):
    """Replace one exact occurrence; an `old` of the form 'LINE:<prefix>' replaces the whole line that starts with <prefix>."""
    if old.startswith('LINE:'):
        pre = old[5:]
        L = t.split('\n')
        idx = [i for i, l in enumerate(L) if l.startswith(pre)]
        if len(idx) != 1:
            PROBLEMS.append(f'{label} line matches {len(idx)} times in {where}: {pre[:90]!r}')
            return t
        L[idx[0]] = new
        return '\n'.join(L)
    n = t.count(old)
    if n != 1:
        PROBLEMS.append(f'{label} matches {n} times in {where}: {old[:90]!r}')
        return t
    return t.replace(old, new, 1)


def apply_edits(edits, label):
    for f, old, new in edits:
        text[f] = edit_one(text[f], old, new, label, f)


# 1 ---------------------------------------------------------------- edits in R8 numbering
apply_edits(SP.PRE_EDITS, 'PRE_EDIT')


# 2 ---------------------------------------------------------------- extract unit bodies
def unit(f, heading_prefix):
    L = text[f].split('\n')
    idx = [i for i, l in enumerate(L) if l.startswith(heading_prefix)]
    if len(idx) != 1:
        PROBLEMS.append(f'unit anchor not unique: {heading_prefix} ({len(idx)})')
        return None, None, ''
    i = idx[0]
    lvl = len(heading_prefix.split(' ')[0])
    j = i + 1
    while j < len(L) and not re.match(r'^#{1,%d} ' % lvl, L[j]):
        j += 1
    return i, j, '\n'.join(L[i + 1:j]).strip('\n')


def demote(body):
    return re.sub(r'^(#{2,5}) ', lambda m: '#' + m.group(1) + ' ', body, flags=re.M)


ARM_MAP = {'1': 'A3a', '2': 'A4c', '3': 'A4d', '4a': 'A2a', '4b': 'A3b', '5': 'A4e', '6': 'A4a', '7': 'A4b', '0': 'A0'}
OLD = {}
for h in ('### 4.4.1 ', '### 4.4.2 ', '### 4.4.3 ', '### 4.4.4 ', '### 4.5.1 ', '### 4.5.2 ', '### 4.5.3 ', '### 4.5.4 ',
          '### 4.5.5 ', '### 4.5.6 '):
    _, _, body = unit('CHAPTER_04_FINAL', h)
    OLD[h] = demote(body)
b = OLD['### 4.5.5 ']
n_before = len(re.findall(r'\bA(?:0|1|2|3|4a|4b|5|6|7)\b', b))
OLD45 = re.sub(r'\bA(0|1|2|3|4a|4b|5|6|7)\b', lambda m: ARM_MAP[m.group(1)], b)
relabel_count = n_before

# 3 ---------------------------------------------------------------- remap section references (R8 -> R9)
SEC = {'4.4.1': '4.4.7', '4.4.2': '4.4.7', '4.4.3': '4.4.7', '4.4.4': '4.4.3',
       '4.5.1': '4.5.7', '4.5.2': '4.5.7', '4.5.5': '4.5.7', '4.5.3': '4.5.8', '4.5.4': '4.5.8', '4.5.6': '4.5.8'}
SECRE = re.compile(r'(?<![\d.\-])(4\.[45]\.[1-6])(?![\d])')
remapped = {'n': 0}


def remap(t):
    def r(m):
        remapped['n'] += 1
        return SEC[m.group(1)]
    # never touch headings of the units that are replaced anyway, nor supplement references (the lookbehind excludes "S-")
    return SECRE.sub(lambda m: r(m) if m.group(1) in SEC else m.group(1), t)


for f in FILES:
    L = text[f].split('\n')
    text[f] = '\n'.join(l if re.match(r'^#{2,4} 4\.[45]', l) else remap(l) for l in L)
OLD = {k: remap(v) for k, v in OLD.items()}
OLD45 = remap(OLD45)

# 4 ---------------------------------------------------------------- replace units 4.4 and 4.5 with the new text


def fill(t):
    def sub(m):
        f, h = m.group(2), m.group(3)
        key = h if h.endswith(' ') else h + ' '
        if m.group(1) == 'OLD45':
            return OLD45
        if key not in OLD:
            PROBLEMS.append(f'unknown placeholder {m.group(0)}')
            return m.group(0)
        return OLD[key]
    return re.sub(r'@@(OLD45|OLD)\[([A-Z0-9_]+)\|(#+ [0-9.]+ ?)\]@@', sub, t)


new44 = fill(open(os.path.join(D, 'text', 'ch4_44.md'), encoding='utf-8').read().strip('\n'))
new45 = fill(open(os.path.join(D, 'text', 'ch4_45.md'), encoding='utf-8').read().strip('\n'))
for h, new in (('## 4.4 ', new44), ('## 4.5 ', new45)):
    i, j, _ = unit('CHAPTER_04_FINAL', h)
    if i is None:
        continue
    L = text['CHAPTER_04_FINAL'].split('\n')
    text['CHAPTER_04_FINAL'] = '\n'.join(L[:i] + new.split('\n') + [''] + L[j:])
if '@@OLD' in '\n'.join(text.values()):
    PROBLEMS.append('placeholder left unfilled')

# 5 ---------------------------------------------------------------- edits in R9 numbering, then merge duplicates
apply_edits(SP.POST_EDITS, 'POST_EDIT')
for f, pa, pb in SP.SWAP_LINES:
    L = text[f].split('\n')
    ia = [i for i, l in enumerate(L) if l.startswith(pa)]
    ib = [i for i, l in enumerate(L) if l.startswith(pb)]
    if len(ia) != 1 or len(ib) != 1:
        PROBLEMS.append(f'SWAP anchors in {f}: {len(ia)}, {len(ib)}')
        continue
    L[ia[0]], L[ib[0]] = L[ib[0]], L[ia[0]]
    text[f] = '\n'.join(L)
apply_edits(SP.AFTER_SWAP_EDITS, 'AFTER_SWAP_EDIT')


def merge_columns(f, caption, groups, headers, joins):
    """Rewrite the pipe table under `caption` with fewer columns: each group of old columns becomes one column,
    joined by the corresponding format string (cell text is never changed, only joined)."""
    L = text[f].split('\n')
    ci = [i for i, l in enumerate(L) if l.startswith(caption)]
    if len(ci) != 1:
        PROBLEMS.append(f'MERGE caption matches {len(ci)} in {f}: {caption}')
        return
    i = ci[0] + 1
    while not L[i].startswith('|'):
        i += 1
    j = i
    while j < len(L) and L[j].startswith('|'):
        j += 1
    rows = [[c.strip() for c in r.strip().strip('|').split(' | ')] for r in L[i:j]]
    out = ['| ' + ' | '.join(headers) + ' |', '|' + '---|' * len(headers)]
    for r in rows[2:]:
        if len(r) != len(rows[0]):
            PROBLEMS.append(f'MERGE row has {len(r)} cells in {caption}')
            return
        cells = []
        for g, jn in zip(groups, joins):
            vals = [r[k].rstrip('.') if n < len(g) - 1 else r[k] for n, k in enumerate(g)]
            cells.append(jn.format(*vals))
        out.append('| ' + ' | '.join(cells) + ' |')
    text[f] = '\n'.join(L[:i] + out + L[j:])


for args in SP.MERGE_TABLES:
    merge_columns(*args)
TOKS = r'(?:S-)?\d+\.\d+(?:\.\d+)?'
LIST = re.compile(r'\b(Sections?) (' + TOKS + r'(?:(?:, |, and | and )' + TOKS + r')+)')
merged = []


def merge(m):
    toks = re.split(r', and |, | and ', m.group(2))
    uniq = list(dict.fromkeys(toks))
    if len(uniq) == len(toks):
        return m.group(0)
    merged.append(m.group(0))
    word = 'Section' if len(uniq) == 1 else 'Sections'
    body = uniq[0] if len(uniq) == 1 else ', '.join(uniq[:-1]) + ' and ' + uniq[-1]
    return f'{word} {body}'


for f in FILES:
    text[f] = LIST.sub(merge, text[f])

# 6 ---------------------------------------------------------------- renumber Chapter 4 tables and figures sequentially
TOK = r'4\.(?:N\d+|\d+[a-z]?)'
maps = {}
for kind, cap in (('Table', r'^\*\*Table (' + TOK + r')\.'), ('Figure', r'^!\[Figure (' + TOK + r')\.')):
    found = re.findall(cap, text['CHAPTER_04_FINAL'], flags=re.M)
    if len(found) != len(set(found)):
        PROBLEMS.append(f'duplicate {kind} caption numbers: {[x for x in found if found.count(x) > 1]}')
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
# Every remaining Chapter-4 section reference must exist as a heading.
heads = set(re.findall(r'^#{2,3} (4\.\d+(?:\.\d+)?) ', text['CHAPTER_04_FINAL'], flags=re.M))
for f in FILES:
    for m in re.finditer(r'(?<![\d.\-])(4\.\d\.\d+)(?![\d.])', text[f]):
        ctx = text[f][max(0, m.start() - 12):m.start()]
        if 'Section' in ctx or 'Sections' in text[f][max(0, m.start() - 40):m.start()]:
            if m.group(1) not in heads:
                PROBLEMS.append(f'section {m.group(1)} referenced in {f} but no such heading')

# ---------------------------------------------------------------- US spelling (the body is in US English; R8 mixed a few British forms)
US = [(r'\bbehaviour', 'behavior'), (r'\bBehaviour', 'Behavior'), (r'\blabelled\b', 'labeled'), (r'\blabelling\b', 'labeling'),
      (r'\bLabelled\b', 'Labeled'), (r'\bLabelling\b', 'Labeling'), (r'\banalysed\b', 'analyzed'), (r'\banalyse\b', 'analyze'), (r'\banalysing\b', 'analyzing'),
      (r'\boptimis(e|ed|es|ing|ation)\b', r'optimiz\1'), (r'\brecognis(e|ed|es|ing)\b', r'recogniz\1'), (r'\blicence\b', 'license'),
      (r'\bartefact(s?)\b', r'artifact\1'), (r'\bjudgement(s?)\b', r'judgment\1'), (r'\brealis(e|ed|es|ing)\b', r'realiz\1')]
PROTECT = re.compile(r'`[^`]*`|https?://\S+|\]\([^)]*\)|\$[^$]*\$')
us_changes = {}


def us_spelling(t):
    parts, last = [], 0
    for m in PROTECT.finditer(t):
        parts.append((t[last:m.start()], True))
        parts.append((m.group(0), False))
        last = m.end()
    parts.append((t[last:], True))
    out = []
    for seg, edit in parts:
        if edit:
            for pat, rep in US:
                seg, n = re.subn(pat, rep, seg)
                if n:
                    us_changes[pat] = us_changes.get(pat, 0) + n
        out.append(seg)
    return ''.join(out)


for f in FILES:
    text[f] = us_spelling(text[f])

# ---------------------------------------------------------------- write
for sub_dir in ('src', 'text_front', 'references', 'audit'):
    os.makedirs(os.path.join(D, sub_dir), exist_ok=True)
for f in FILES:
    open(os.path.join(D, 'src', f + '.md'), 'w', encoding='utf-8').write(re.sub(r'\n{3,}', '\n\n', text[f]).strip('\n') + '\n')
for name in ('front_matter.md', 'abstract_en.md', 'abstract_ar.md'):
    t = open(os.path.join(R8, 'text_front', name), encoding='utf-8').read()
    for fn, old, new in SP.FRONT_EDITS:
        if fn == name:
            t = edit_one(t, old, new, 'FRONT_EDIT', name)
    if name != 'abstract_ar.md':
        t = us_spelling(t)
    open(os.path.join(D, 'text_front', name), 'w', encoding='utf-8').write(t)
refs = open(os.path.join(R8, 'references', 'REFERENCES_FINAL.md'), encoding='utf-8').read()
for after, entry in SP.REF_ADD:
    if refs.count(after) != 1:
        PROBLEMS.append(f'REF anchor matches {refs.count(after)} times: {after[:60]!r}')
        continue
    k = refs.index(after)
    e = refs.index('\n', k)
    refs = refs[:e] + '\n\n' + entry + refs[e:]
for old, new in getattr(SP, 'REF_EDITS', []):
    refs = edit_one(refs, old, new, 'REF_EDIT', 'REFERENCES_FINAL.md')
open(os.path.join(D, 'references', 'REFERENCES_FINAL.md'), 'w', encoding='utf-8').write(refs)
json.dump({'tables': maps['Table'], 'figures': maps['Figure'], 'sections_R8_to_R9': SEC,
           'arm_relabel_19_Nov_to_variant': {('A' + k): v for k, v in ARM_MAP.items()},
           'arm_labels_relabelled_in_old_4_5_5': relabel_count, 'us_spelling_changes': us_changes, 'section_references_remapped': remapped['n'],
           'reference_lists_merged': merged},
          open(os.path.join(D, 'audit', 'r9_renumbering.json'), 'w'), indent=1, ensure_ascii=False)
open(os.path.join(D, 'audit', 'r9_check.txt'), 'w').write('\n'.join(PROBLEMS) + ('\n' if PROBLEMS else 'no problems\n'))
words = {f: len(re.sub(r'[|#*`$\\{}]', ' ', text[f]).split()) for f in FILES}
print('words', words, 'total', sum(words.values()), '| tables ch4', len(maps['Table']), 'figures ch4', len(maps['Figure']),
      '| section refs remapped', remapped['n'], '| lists merged', len(merged), '| problems', len(PROBLEMS))
for p in PROBLEMS[:40]:
    print('  ', p)
