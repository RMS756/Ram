"""Final QA of the five-chapter build. Run from the repository root:

    python3 REM_FINAL_THESIS/tools/qa_5ch.py

Writes to REM_FINAL_THESIS/final_five_chapters/audit/qa_logs/:
  docx_structure.txt          structural checks of the 6 DOCX files (same checks as R4)
  margin_overflow_scan.txt    ink in the outer 2.2 cm of the right margin; near-blank pages
  tracked_changes_comments.txt  w:ins / w:del / w:comment counts
  pdf_properties.txt          page count, page size, fonts, page-number labels sampled
Exit 1 on a structural failure, on margin ink, or on tracked changes/comments.
"""
import glob
import importlib.util
import os
import re
import subprocess
import sys
import tempfile
import zipfile

from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
FF = os.path.join(ROOT, 'REM_FINAL_THESIS', 'final_five_chapters')
LOGS = os.path.join(FF, 'audit', 'qa_logs')
os.makedirs(LOGS, exist_ok=True)
PDF = os.path.join(FF, 'REM_THESIS_5CH_FINAL.pdf')
DOCX = [os.path.join(FF, 'REM_THESIS_5CH_FINAL.docx')] + sorted(glob.glob(os.path.join(FF, 'chapters', '*.docx')))

spec = importlib.util.spec_from_file_location(
    'chk', os.path.join(ROOT, 'REM_FINAL_THESIS', 'verification', 'check_docx_structure_R4.py'))
failed = False

# ---------------------------------------------------------------- 1. DOCX structure
chk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chk)
ns = {'check': chk.check}
out = []
for p in DOCX:
    res = ns['check'](p)
    ok = all(v == 0 for k, v in res.items() if k not in ('runs', 'table_runs', 'idempotent')) and res.get('idempotent', True)
    failed |= not ok
    out.append(f"{'PASS' if ok else 'FAIL'} {os.path.basename(p)} {res}")
open(os.path.join(LOGS, 'docx_structure.txt'), 'w').write('\n'.join(out) + '\n')

# ---------------------------------------------------------------- 2. tracked changes / comments
tc = []
for p in DOCX:
    with zipfile.ZipFile(p) as z:
        doc = z.read('word/document.xml').decode('utf-8')
        com = z.read('word/comments.xml').decode('utf-8') if 'word/comments.xml' in z.namelist() else ''
    n_ins, n_del = len(re.findall(r'<w:ins\b', doc)), len(re.findall(r'<w:del\b', doc))
    n_com = len(re.findall(r'<w:comment\b', com))
    failed |= bool(n_ins or n_del or n_com)
    tc.append(f'{os.path.basename(p)}: w:ins {n_ins}; w:del {n_del}; w:comment {n_com}')
open(os.path.join(LOGS, 'tracked_changes_comments.txt'), 'w').write('\n'.join(tc) + '\n')

# ---------------------------------------------------------------- 3. margins and blank pages
with tempfile.TemporaryDirectory() as td:
    subprocess.run(['pdftoppm', '-r', '40', '-gray', PDF, os.path.join(td, 'p')], check=True)
    pages = sorted(glob.glob(os.path.join(td, 'p-*.pgm')))
    ink, blank = [], []
    for i, f in enumerate(pages, 1):
        im = Image.open(f)
        w_, h_ = im.size
        px_cm = w_ / 21.0
        strip = im.crop((int(w_ - 2.2 * px_cm), 0, w_, h_))
        if min(strip.getdata()) < 128:
            ink.append(i)
        body = im.crop((0, 0, w_, int(h_ - 2.5 * px_cm)))
        dark = sum(1 for v in body.getdata() if v < 128)
        if dark < 150:
            blank.append((i, dark))
failed |= bool(ink)
open(os.path.join(LOGS, 'margin_overflow_scan.txt'), 'w').write(
    f'pages scanned: {len(pages)} ; pages with ink inside the outer 2.2 cm of the right margin: {ink}\n'
    f'pages with almost no content above the footer (possible blank pages; (page, dark pixels at 40 dpi)): {blank}\n')

# ---------------------------------------------------------------- 4. PDF properties
info = subprocess.run(['pdfinfo', PDF], capture_output=True, text=True).stdout
fonts = subprocess.run(['pdffonts', PDF], capture_output=True, text=True).stdout.splitlines()[2:]
fams = sorted({re.sub(r'^[A-Z]{6}\+', '', l.split()[0]) for l in fonts if l.strip()})
labels = []
for pg in (1, 2, 5, 10, 20, 23, 24, 25, 60, 120, len(pages)):
    t = subprocess.run(['pdftotext', '-f', str(pg), '-l', str(pg), '-layout', PDF, '-'],
                       capture_output=True, text=True).stdout.rstrip().splitlines()
    last = next((l.strip() for l in reversed(t) if l.strip()), '')
    labels.append(f'physical page {pg}: last line "{last[:60]}"')
open(os.path.join(LOGS, 'pdf_properties.txt'), 'w').write(
    '\n'.join(l for l in info.splitlines() if l.split(':')[0] in ('Pages', 'Page size', 'Producer', 'Creator')) +
    '\nfonts embedded: ' + ', '.join(fams) + '\n' + '\n'.join(labels) + '\n')

print(open(os.path.join(LOGS, 'docx_structure.txt')).read())
print(open(os.path.join(LOGS, 'tracked_changes_comments.txt')).read())
print(open(os.path.join(LOGS, 'margin_overflow_scan.txt')).read())
print(open(os.path.join(LOGS, 'pdf_properties.txt')).read())
sys.exit(1 if failed else 0)
