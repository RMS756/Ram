"""Compare the humanized sources with the snapshot of the defence-ready thesis and fail on any change of content
that humanization must not touch. Writes audit/preservation_check.json and audit/style_metrics.json.

Checked per file, original against humanized:
  structure : heading lines, table lines, figure lines, display equations ($$...$$), inline math, code spans,
              URLs and DOIs -- identical sequences (multisets for inline items);
  content   : multiset of numeric tokens in prose; multiset of identifiers (A4c, D-8, RQ1, AS-6, SD-ABL, x_ctx2 ...);
              number of occurrences of every reference surname (citations);
  terms     : occurrences of the protected technical terms (reported; a decrease is flagged).
Edits listed in ALLOW (file, kind, reason) are exempted and reported.
"""
import collections
import glob
import json
import os
import re
import sys

H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(H, 'orig_src')
ALLOW = []  # (file, kind, reason): evidence-based exceptions, each documented in the change log

TERMS = ['indirect prompt injection', 'financial AI agent', 'Runtime Evaluation and Mitigation', 'REM',
         'Input & Context', 'Detection', 'Behavioral Analysis', 'Decision Engine', 'Mitigation',
         'tool-call boundary', 'offline replay', 'scripted integration', 'ablation', 'attack success rate', 'ASR',
         'utility', 'provenance', 'Platt', 'expected loss', 'Allow', 'Modify', 'Escalate', 'Block', 'CUSUM',
         'observe-only', 'shadow', 'Progent', 'DRIFT', 'MELON', 'AgentDojo', 'NO-ADAPT', 'calibrat']
AI_WORDS = ['delve', 'underscore', 'intricate', 'tapestry', 'testament', 'pivotal', 'showcase', 'foster', 'leverage',
            'realm', 'seamless', 'crucial', 'notably', 'moreover', 'furthermore', 'additionally', 'comprehensive',
            'robust', 'novel', 'paves the way', 'sheds light', 'it is worth noting', 'it should be noted', 'importantly',
            'in order to', 'a wide range of', 'extensive', 'significantly', 'demonstrate', 'prove', 'landscape',
            'holistic', 'cutting-edge', 'state-of-the-art', 'utilize', 'utilise', 'facilitate']

surnames = sorted({m.group(1) for m in re.finditer(r'^([A-Z][A-Za-z\'\-]+(?: [A-Z][a-z]+)?),', open(
    os.path.join(ORIG, 'references', 'REFERENCES_FINAL.md'), encoding='utf-8').read(), re.M)})


def split(t):
    """Separate structural lines from prose."""
    heads, tables, figs, eqs, prose = [], [], [], [], []
    in_eq = False
    for line in t.split('\n'):
        s = line.strip()
        if in_eq or s.startswith('$$'):
            eqs.append(line)
            in_eq = (in_eq or s.startswith('$$')) and not (s.endswith('$$') and (len(s) > 2 or in_eq))
            if s == '$$' and not in_eq and len(eqs) and eqs[-1] == line:
                pass
            continue
        if s.startswith('#'):
            heads.append(line)
        elif s.startswith('|'):
            tables.append(line)
        elif s.startswith('!['):
            figs.append(line)
        else:
            prose.append(line)
    return heads, tables, figs, eqs, '\n'.join(prose)


NUM = re.compile(r'(?<![A-Za-z_])[−\-+]?\d(?:[\d,]*\d)?(?:\.\d+)?(?:[eE×][−\-]?\d+)?%?')
IDENT = re.compile(r'\b(?:[A-Z]{1,6}-?\d+[a-z]?(?:\.\d+)*|SD-[A-Z]+|[A-Z]{2,}-[A-Z0-9]+|x_[a-z]+\d*|x~[a-z]+\d*~)\b')
INLINE_MATH = re.compile(r'(?<!\$)\$[^$\n]+\$(?!\$)')
CODE = re.compile(r'`[^`\n]+`')
URL = re.compile(r'https?://\S+|doi\.org/\S+|10\.\d{4,9}/\S+')


def profile(t):
    heads, tables, figs, eqs, prose = split(t)
    p = prose
    inline = INLINE_MATH.findall(p)
    codes = CODE.findall(p)
    urls = URL.findall(p)
    q = INLINE_MATH.sub(' ', CODE.sub(' ', p))
    return {
        'headings': heads, 'tables': tables, 'figures': figs, 'equations': eqs,
        'inline_math': collections.Counter(inline), 'code': collections.Counter(codes),
        'urls': collections.Counter(urls),
        'numbers': collections.Counter(NUM.findall(URL.sub(' ', q))),
        'identifiers': collections.Counter(IDENT.findall(q)),
        'citations': collections.Counter({s: len(re.findall(r'\b' + re.escape(s) + r'\b', t)) for s in surnames}),
        'terms': collections.Counter({k: len(re.findall(re.escape(k), t, re.I if k[0].islower() else 0)) for k in TERMS}),
        'prose': p,
    }


def metrics(prose):
    words = len(re.findall(r'\b\w+\b', prose))
    sents = [s for s in re.split(r'(?<=[.!?])\s+(?=[A-Z])', re.sub(r'\s+', ' ', prose)) if len(s.split()) > 3]
    long40 = sum(1 for s in sents if len(s.split()) > 40)
    long30 = sum(1 for s in sents if len(s.split()) > 30)
    ai = {w: len(re.findall(r'\b' + re.escape(w) + r'(?:s|d|ed|es|ing|ly)?\b', prose, re.I)) for w in AI_WORDS}
    return {'words': words, 'sentences': len(sents), 'sentences_over_30_words': long30,
            'sentences_over_40_words': long40, 'em_dashes': prose.count('—'),
            'ai_vocabulary': {k: v for k, v in ai.items() if v}}


def diffc(a, b):
    out = {}
    for k in set(a) | set(b):
        if a.get(k, 0) != b.get(k, 0):
            out[k] = [a.get(k, 0), b.get(k, 0)]
    return out


report, fail, mets = {}, False, {}
for po in sorted(glob.glob(os.path.join(ORIG, '*', '*.md'))):
    f = os.path.relpath(po, ORIG)
    a = profile(open(po, encoding='utf-8').read())
    b = profile(open(os.path.join(H, f), encoding='utf-8').read())
    r = {}
    for k in ('headings', 'tables', 'figures', 'equations'):
        if a[k] != b[k]:
            r[k] = [x for x in b[k] if x not in a[k]][:5] or ['(order or removal)']
    for k in ('inline_math', 'code', 'urls', 'numbers', 'identifiers', 'citations'):
        d = diffc(a[k], b[k])
        if d:
            r[k] = d
    allowed = {kind for (ff, kind, _) in ALLOW if ff == f}
    hard = {k: v for k, v in r.items() if k not in allowed}
    td = {k: v for k, v in diffc(a['terms'], b['terms']).items() if v[1] < v[0]}
    if td:
        r['terms_decreased (inspect)'] = td
    report[f] = r
    if hard:
        fail = True
    mets[f] = {'original': metrics(a['prose']), 'humanized': metrics(b['prose'])}

json.dump({'files': report, 'allowed_exceptions': ALLOW, 'pass': not fail},
          open(os.path.join(H, 'audit', 'preservation_check.json'), 'w'), indent=1, ensure_ascii=False)
json.dump(mets, open(os.path.join(H, 'audit', 'style_metrics.json'), 'w'), indent=1, ensure_ascii=False)
for f, r in report.items():
    if r:
        print(f, json.dumps(r, ensure_ascii=False)[:1500])
tot = lambda key, side: sum(m[side][key] for m in mets.values())
print('PASS' if not fail else 'FAIL', '| sentences >40 words:', tot('sentences_over_40_words', 'original'), '->',
      tot('sentences_over_40_words', 'humanized'), '| >30:', tot('sentences_over_30_words', 'original'), '->',
      tot('sentences_over_30_words', 'humanized'), '| em-dashes:', tot('em_dashes', 'original'), '->', tot('em_dashes', 'humanized'))
sys.exit(1 if fail else 0)
