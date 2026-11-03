"""QA of the five-chapter assembly against R5: numbers, headings, words, citations. Writes audit/qa_logs/*.txt."""
import collections, os, re, shutil, subprocess, sys, tempfile
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
R5 = os.path.join(ROOT, 'REM_FINAL_THESIS', 'chapters_R5')
F5 = os.path.join(ROOT, 'REM_FINAL_THESIS', 'final_five_chapters')
LOG = os.path.join(F5, 'audit', 'qa_logs'); os.makedirs(LOG, exist_ok=True)
old = {f: open(os.path.join(R5, f), encoding='utf-8').read() for f in sorted(os.listdir(R5)) if f.startswith('CHAPTER')}
new = {f: open(os.path.join(F5, 'src', f), encoding='utf-8').read() for f in sorted(os.listdir(os.path.join(F5, 'src')))}
O, N = '\n'.join(old.values()), '\n'.join(new.values())
out = []
# 1. numerical values: decimals with >= 3 digits after the point, percentages, thousands with commas, signed differences
pat = re.compile(r'(?<![\w.])[−-]?\d+\.\d{3,}(?!\d)|(?<![\w.])\d+(?:\.\d+)?%|(?<![\w.])\d{1,3}(?:,\d{3})+(?!\d)')
co, cn = collections.Counter(pat.findall(O)), collections.Counter(pat.findall(N))
lost = {k: (v, cn.get(k, 0)) for k, v in co.items() if cn.get(k, 0) < v}
out.append(f'[numbers] distinct values in R5 Ch1-6: {len(co)}; occurrences {sum(co.values())}; in 5ch: {sum(cn.values())}')
out.append(f'[numbers] values with fewer occurrences in 5ch than in R5: {len(lost)} {lost if lost else ""}')
# 2. headings (titles without numbers)
def titles(t): return [re.sub(r'^\d+(?:\.\d+)*\s+', '', h).strip() for h in re.findall(r'^#{2,6} (.+)$', t, flags=re.M)]
to, tn = titles(O), set(titles(N))
missing = [t for t in to if t not in tn]
out.append(f'[headings] R5 headings: {len(to)}; not found verbatim in 5ch: {len(missing)}')
out += [f'    - {m}' for m in missing]
# 3. words
w = lambda t: len(re.findall(r'\S+', t))
out.append(f'[words] R5 Ch1-6: {w(O)}; 5ch Ch1-5: {w(N)} ({w(N) - w(O):+d})')
for f, t in new.items():
    out.append(f'    {f}: {w(t)} words')
# 4. citations
d = tempfile.mkdtemp()
for f, t in new.items():
    open(os.path.join(d, f.replace('.md', '_FINAL.md')), 'w', encoding='utf-8').write(t)
shutil.copy(os.path.join(R5, '..', 'chapters_R5', 'REFERENCES_R5.md'), os.path.join(d, 'REFERENCES.md'))
r = subprocess.run([sys.executable, os.path.join(ROOT, 'REM_FINAL_THESIS', 'verification', 'check_citations.py'), d], capture_output=True, text=True)
out.append('[citations]\n' + r.stdout.strip())
# 5. structure
RX = {'chapters': r'^# CHAPTER ', 'equations': r'qquad \(\d+\.\d+\)', 'tables': r'^\*\*Table ', 'figures': r'!\[Figure'}
cnt = {k: (len(re.findall(v, N, flags=re.M)), len(re.findall(v, O, flags=re.M))) for k, v in RX.items()}
out.append('[structure] ' + '; '.join(f'{k}: {a} (R5: {b})' for k, (a, b) in cnt.items()))
open(os.path.join(LOG, 'content_preservation.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))
