"""List prose sentences longer than N words (default 38) in a source file, with line numbers."""
import re, sys
f, n = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 38
for i, line in enumerate(open(f, encoding='utf-8'), 1):
    s = line.strip()
    if not s or s[0] in '#|!$' or s.startswith('$$'):
        continue
    for sent in re.split(r'(?<=[.;])\s+(?=[A-Z*(])', s):
        if len(sent.split()) > n:
            print(f'{i}: [{len(sent.split())}] {sent}')
