"""Layout check of the built PDF: page counts, chapter starts, near-empty pages, captions at the foot of a page."""
import re
import subprocess
import sys

pdf = sys.argv[1]
txt = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout.split('\f')[:-1]
norm = lambda t: re.sub(r'\s+', ' ', t)
start = next(i for i, p in enumerate(txt) if 'Artificial intelligence systems based on large language models' in norm(p))
print('pages', len(txt), '| preliminary pages', start)
marks = {}
for i, p in enumerate(txt):
    for key in ('CHAPTER ONE:', 'CHAPTER TWO:', 'CHAPTER THREE:', 'CHAPTER FOUR:', 'CHAPTER FIVE:', 'References', 'Appendix A:', 'Appendix B:', 'Appendix C:',
                'Appendix D:', 'Appendix E:', 'Appendix F:'):
        if i >= start and key not in marks and re.search(r'^\s*' + re.escape(key), p, flags=re.M):
            marks[key] = i + 1 - start
print(marks)
ends = set(v - 1 for v in marks.values())            # last page of a chapter or appendix may be short
low, orphan = [], []
for i, p in enumerate(txt):
    lines = [l.strip() for l in p.split('\n') if l.strip()]
    body = lines[:-1] if lines and re.fullmatch(r'[ivxl\d]+', lines[-1]) else lines
    words = sum(len(l.split()) for l in body)
    no = i + 1 - start
    if i >= start and words < 90 and no not in ends:
        low.append((i + 1, no, words))
    if body and re.match(r'^(Table|Figure) (\d+|[A-F])\.\d+\.', body[-1]) and i >= start:
        orphan.append((i + 1, no, body[-1][:60]))
print('near-empty pages inside the text (pdf page, page number, words):', low)
print('pages that end with a caption (pdf page, page number, caption):', orphan)
