"""Check that every decimal number in a results chapter matches a value in the result files.
usage: check_chapter_numbers.py <chapter.md> <results_dir> [<results_dir2> ...]
A number shown with k decimals matches a JSON leaf v if round(v, k) equals it; percentages are
matched against 100*v; integers >= 10 are matched exactly against integer leaves and list lengths.
Numbers that do not match are printed with their line for manual tracing."""
import json, re, sys, glob, os
chap, dirs = sys.argv[1], sys.argv[2:]
vals, ints = [], set()
def walk(o):
    if isinstance(o, bool): return
    if isinstance(o, (int, float)):
        vals.append(float(o))
        if float(o).is_integer(): ints.add(int(o))
    elif isinstance(o, dict):
        for v in o.values(): walk(v)
        ints.add(len(o))
    elif isinstance(o, list):
        ints.add(len(o))
        for v in o: walk(v)
for d in dirs:
    for f in glob.glob(os.path.join(d, '*.json')):
        walk(json.load(open(f)))
text = open(chap, encoding='utf-8').read().split('## References')[0]
skip_ctx = re.compile(r'(Section|Sections|Table|Tables|Figure|Eq\.|Eqs\.|Equation|Equations|Chapter|commit|AM-|§)\s*$')
unmatched = []; n = 0
for ln, line in enumerate(text.split('\n'), 1):
    if line.startswith('#') or line.startswith('!['): continue
    for m in re.finditer(r'(?<![\w.\-/])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)(%?)', line):
        tok, pct = m.group(1), m.group(2)
        pre = line[:m.start()]
        if skip_ctx.search(pre[-12:]): continue
        if re.match(r'^(19|20)\d\d$', tok): continue
        x = float(tok.replace(',', ''))
        if '.' not in tok and x < 10 and not pct: continue          # small integers (counts like "two") not checked
        n += 1
        if pct:
            k = len(tok.split('.')[1]) if '.' in tok else 0
            ok = any(round(100*v, k) == x for v in vals) or any(round(100*(1-v), k) == x for v in vals)
        elif '.' in tok:
            k = len(tok.split('.')[1])
            ok = any(round(v, k) == x for v in vals) or any(round(-v, k) == x for v in vals)
        else:
            ok = int(x) in ints
        if not ok: unmatched.append((ln, tok + pct, line.strip()[:160]))
print(f'{chap}: {n} numbers checked, {len(unmatched)} without a direct match in the result files')
for u in unmatched: print('  L%d  %-10s %s' % u)
