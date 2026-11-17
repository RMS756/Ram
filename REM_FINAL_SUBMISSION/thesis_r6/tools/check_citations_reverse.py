"""Reverse citation check: every author-year citation in the R6 text must match a reference entry (surname and year).

Patterns: "Surname (2026)", "Surname et al. (2026)", "Surname and Other (2026)", "(Surname, 2026)", "(Surname et al., 2026;
Other, 2025)", with an optional initial ("T. Shi et al. (2026)"). Writes audit/citation_reverse_check.json. Approximate by
design: a hit is reported for manual inspection, never fixed automatically.

usage: python3 REM_FINAL_SUBMISSION/thesis_r6/tools/check_citations_reverse.py [text dir] [reference file]
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.join(HERE, '..')
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(FIN, 'src')
ref = sys.argv[2] if len(sys.argv) > 2 else os.path.join(FIN, 'references', 'REFERENCES_FINAL.md')
files = sorted(glob.glob(os.path.join(src, '*.md'))) if os.path.isdir(src) else [src]
if os.path.isdir(src) and src.endswith('src'):
    files += sorted(glob.glob(os.path.join(FIN, 'text_front', '*.md')))
text = re.sub(r'\s+', ' ', '\n'.join(open(p, encoding='utf-8').read() for p in files))
text = re.sub(r'`[^`]*`', ' ', text)
refs = open(ref, encoding='utf-8').read()
have = set()
for b in refs.split('\n\n'):
    m = re.match(r'^([^,(]+?)[,.]? .*?\((\d{4}[a-z]?|n\.d\.)', b.strip())
    if m:
        have.add((m.group(1).strip().split(' & ')[0], m.group(2)))
surnames = {s for s, _ in have}
NAME = r"(?:[A-Z]\. )?([A-Z][A-Za-z'\-]+(?: [A-Z][a-z]+)?)"
cites = set()
for m in re.finditer(NAME + r"(?: et al\.| and [A-Z][A-Za-z'\-]+| & [A-Z][A-Za-z'\-]+)? \((\d{4}[a-z]?)[;,)]", text):
    cites.add((m.group(1), m.group(2)))
for par in re.findall(r'\(([^()]*\d{4}[a-z]?[^()]*)\)', text):
    for part in par.split(';'):
        m = re.search(NAME + r"(?: et al\.| and [A-Z][A-Za-z'\-]+| & [A-Z][A-Za-z'\-]+)?,? (\d{4}[a-z]?)\b", part.strip())
        if m and m.start() < 4:
            cites.add((m.group(1), m.group(2)))
missing = sorted((s, y) for s, y in cites if s in surnames and (s, y) not in have)
unknown = sorted((s, y) for s, y in cites if s not in surnames)
json.dump({'citations_found': len(cites), 'surname_known_year_missing': missing, 'surname_not_in_references': unknown},
          open(os.path.join(FIN, 'audit', 'citation_reverse_check.json'), 'w'), indent=1)
print('citations found', len(cites), '| known surname, year missing:', missing)
print('surnames not in the reference list (inspect; most are not citations):', unknown[:80])
