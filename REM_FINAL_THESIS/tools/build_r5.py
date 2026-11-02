"""Build the R5 thesis (chapters_R5/ -> REM_FINAL_THESIS/R5/) with the unchanged R4 toolchain.

usage: python3 REM_FINAL_THESIS/tools/build_r5.py   (from the repository root, after make_r5.py)

`build_thesis.py` is NOT modified. This wrapper reads its source, substitutes only the version-specific
paths and names (R4 -> R5, with the R4 layout options kept), checks that every substitution applies
exactly as often as expected, and executes the result. R3 and R4 outputs are untouched.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'build_thesis.py')
code = open(SRC, encoding='utf-8').read()

SUBS = [
    ("VERSION = os.environ.get('REM_VERSION', 'R3')", "VERSION = 'R5'", 1),
    ("R4 = VERSION == 'R4'", "R4 = True   # R4 layout options, applied to the R5 sources", 1),
    ("'chapters_R4' if R4 else 'chapters'", "'chapters_R5'", 1),
    ("os.path.join(ROOT, 'REM_FINAL_THESIS', 'R4') if R4 else", "os.path.join(ROOT, 'REM_FINAL_THESIS', 'R5') if R4 else", 1),
    ("SUF = '_R4' if R4 else '_FINAL'", "SUF = '_R5'", 1),
    ("'FRONT_MATTER' + ('_R4' if R4 else '')", "'FRONT_MATTER_R5'", 1),
    ("'REFERENCES' + ('_R4' if R4 else '')", "'REFERENCES_R5'", 1),
    ("'REM_THESIS_R4.docx' if R4 else", "'REM_THESIS_R5.docx' if R4 else", 1),
]
for old, new, n in SUBS:
    if code.count(old) != n:
        sys.exit(f'build_r5: expected {n} occurrence(s) of {old!r}, found {code.count(old)}')
    code = code.replace(old, new)

sys.path.insert(0, HERE)
exec(compile(code, SRC + ' [R5 paths]', 'exec'), {'__file__': SRC, '__name__': '__main__'})
