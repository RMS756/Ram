"""Verify the page references of the built thesis: every table-of-contents entry stored in the DOCX and every
list-of-tables and list-of-figures entry must name the page (as printed) on which that heading or caption appears
in the PDF. Usage: python3 check_pages.py <thesis folder>"""
import json
import re
import subprocess
import sys
import os

d = sys.argv[1]
pdf = [os.path.join(d, f) for f in os.listdir(d) if f.endswith('.pdf')][0]
pages = [re.sub(r'\s+', ' ', p) for p in subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout.split('\f')]
start = next(i for i, p in enumerate(pages) if 'Artificial intelligence systems based on large language models' in p)
roman = {i: n for i, n in enumerate(['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi', 'xvii', 'xviii', 'xix', 'xx',
                                      'xxi', 'xxii', 'xxiii', 'xxiv', 'xxv', 'xxvi', 'xxvii', 'xxviii', 'xxix', 'xxx'])}
printed = {i: (str(i + 1 - start) if i >= start else roman.get(i, '?')) for i in range(len(pages))}
norm = lambda t: re.sub(r'\s+', ' ', t).strip()
toc = json.load(open(os.path.join(d, 'audit', 'toc_entries.json')))['entries']
lists = json.load(open(os.path.join(d, 'build', 'lists_pages.json')))
bad, checked = [], 0
listing = {i for i, p in enumerate(pages) if p.count('.....') >= 3}       # contents and list pages (dot leaders)
for title, pg in toc:
    key = norm(title)[:32]
    hits = [i for i in range(len(pages)) if i not in listing and key in pages[i]]
    if not hits:                                                      # the list pages themselves: the heading opens the page
        hits = [i for i in sorted(listing) if pages[i].strip().startswith(key)]
    checked += 1
    if not hits or printed[hits[0]] != pg:
        bad.append(('toc', title[:70], pg, printed[hits[0]] if hits else None))
for kind in ('LOT', 'LOF'):
    for cap, pg in lists[kind]:
        key = norm(cap)[:55]
        hits = [i for i in range(start, len(pages)) if i not in listing and key in pages[i]]
        checked += 1
        if not hits or printed[hits[0]] != str(pg):
            bad.append((kind, cap[:70], pg, printed[hits[0]] if hits else None))
print(f'page references checked: {checked}; mismatches: {len(bad)}')
for b in bad[:40]:
    print('  ', b)
json.dump({'checked': checked, 'mismatches': bad}, open(os.path.join(d, 'audit', 'page_reference_check.json'), 'w'), indent=1)
