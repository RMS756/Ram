"""Check that every author–year citation in the chapters resolves to the consolidated reference list,
and list reference entries that no chapter cites.
usage: check_citations.py <chapters_dir>"""
import re, sys, glob, os, json
D = sys.argv[1]
refs = open(os.path.join(D, 'REFERENCES.md'), encoding='utf-8').read().split('\n')
ents = [l for l in refs if re.match(r'^[A-Z][^\n]*\(\d{4}', l)]
keyset = {}
for e in ents:
    m = re.match(r'(.+?)\s\((\d{4})', e)
    first = m.group(1).split(',')[0].strip()
    keyset.setdefault((first.split()[-1] if first.startswith(('European', 'OWASP')) else first, m.group(2)), []).append(e)
body = ''
for f in sorted(glob.glob(os.path.join(D, 'CHAPTER*_FINAL.md'))):
    body += open(f, encoding='utf-8').read() + '\n'
# author-year citations: "Surname (YYYY)", "Surname et al. (YYYY)", "(Surname, YYYY", "Surname & Other, YYYY"
pat = re.compile(r"((?:[A-Z]\.(?:-[A-Z]\.)?\s)?(?:[a-z]+\s)?[A-Z][A-Za-zÀ-ÿ'\-]+)(?:\s(?:et al\.|&\s[A-Z][A-Za-z'\-]+))?(?:,\s[A-Z][A-Za-z\-]+(?:,? &\s[A-Z][A-Za-z\-]+)?)?(?:,|\s\()\s?(\d{4})")
missing = {}; used = set()
STOP = {'Section', 'Sections', 'Table', 'Figure', 'Chapter', 'September', 'October', 'July', 'June', 'August', 'January', 'May', 'March', 'April', 'November', 'December', 'February', 'Eq', 'AM', 'Oct', 'Sep', 'Regulation', 'Article', 'Vol', 'Appendix', 'PRISMA', 'Q', 'In'}
for m in pat.finditer(body):
    name = m.group(1).split()[-1]; yr = m.group(2)
    if name in STOP or not (1940 <= int(yr) <= 2026): continue
    if (name, yr) in keyset: used.add((name, yr))
    else:
        cands = [k for k in keyset if k[0] == name]
        missing.setdefault((name, yr), body[max(0, m.start()-60):m.end()+5].replace('\n', ' '))
print('reference entries:', len(ents), '| distinct cited author-year keys resolved:', len(used))
print('UNRESOLVED citations:', len(missing))
for k, ctx in sorted(missing.items()): print('  ', k, '…', ctx[-110:])
unused = [k for k in keyset if k not in used]
print('reference keys never matched by an in-text citation:', len(unused))
for k in sorted(unused): print('  ', k)
