"""Print a section of the base five-chapter source with paragraph indices (editing aid; no output files)."""
import os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
BASE = os.path.join(ROOT, 'REM_FINAL_THESIS', 'final_five_chapters', 'src')
FILES = {1: 'CHAPTER1_INTRODUCTION', 2: 'CHAPTER2_LITERATURE_REVIEW', 3: 'CHAPTER3_METHODOLOGY', 4: 'CHAPTER4_RESULTS_DISCUSSION', 5: 'CHAPTER5_CONCLUSIONS'}


def load(ch):
    return open(os.path.join(BASE, FILES[ch] + '.md'), encoding='utf-8').read()


def split_blocks(body):
    """Blocks separated by blank lines; a table caption is merged with its table; fenced/math blocks kept whole."""
    raw = [b for b in re.split(r'\n\s*\n', body.strip('\n')) if b.strip()]
    out = []
    for b in raw:
        if out and out[-1].lstrip().startswith('**Table') and b.lstrip().startswith('|'):
            out[-1] += '\n\n' + b
        else:
            out.append(b)
    return out


def units(text):
    """[(level, num, title, body)] for every heading of level 2-3 (body excludes deeper numbered headings of level 3)."""
    parts = re.split(r'^(#{2,3} .+)$', text, flags=re.M)
    res = []
    for i in range(1, len(parts), 2):
        h = parts[i]
        lvl = len(h.split(' ')[0])
        t = h[lvl + 1:].strip()
        m = re.match(r'((?:\d+|Appendix \d+[A-Z])(?:\.\d+)*)\.?\s+(.*)', t)
        res.append((lvl, m.group(1) if m else t, m.group(2) if m else t, parts[i + 1]))
    return res


if __name__ == '__main__':
    ch = int(sys.argv[1]); want = sys.argv[2:]
    full = '--full' in want
    want = [w for w in want if not w.startswith('--')]
    for lvl, num, title, body in units(load(ch)):
        if want and not any(num == w or num.startswith(w + '.') for w in want):
            continue
        print(f"\n{'#' * lvl} {num} {title}")
        for k, b in enumerate(split_blocks(body)):
            w = len(b.split())
            if b.lstrip().startswith(('|', '**Table')) and not full:
                rows = b.split('\n')
                b = '\n'.join(rows[:4]) + f'\n   … [{len(rows)} lines]'
            print(f"[{k}|{w}w] {b}")
