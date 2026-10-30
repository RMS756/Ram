"""Compare an independent re-run of the pilot with the committed results/pilot_R2.
usage: compare_reproduction.py <rerun_dir> <committed_dir> <out_json>
Every numeric leaf shared by both JSON trees is compared exactly. Keys that hold
wall-clock times, memory or provenance stamps are reported separately."""
import json, sys, os, glob, math
RUN, REF, OUT = sys.argv[1:4]
VOLATILE = ('latency', 'time', 'ms', 'seconds', 'memory', 'bytes', 'peak', 'kb', 'created', 'timestamp', 'commit', 'git', 'python', 'numpy', 'platform', 'hostname', 'duration', 'wall', 'sha', 'file')
def leaves(o, path=()):
    if isinstance(o, dict):
        for k, v in o.items(): yield from leaves(v, path + (str(k),))
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from leaves(v, path + (str(i),))
    else:
        yield path, o
report = {'files': {}, 'totals': {'shared': 0, 'equal': 0, 'diff_volatile': 0, 'diff_analytical': 0}}
for f in sorted(glob.glob(os.path.join(REF, '*.json'))):
    name = os.path.basename(f); g = os.path.join(RUN, name)
    if not os.path.exists(g):
        report['files'][name] = 'MISSING IN RE-RUN'; continue
    a = dict(leaves(json.load(open(f)))); b = dict(leaves(json.load(open(g))))
    shared = set(a) & set(b); diffs = []
    for k in shared:
        x, y = a[k], b[k]
        same = (x == y) or (isinstance(x, float) and isinstance(y, float) and math.isnan(x) and math.isnan(y))
        if not same:
            vol = any(t in '/'.join(k).lower() for t in VOLATILE)
            diffs.append({'path': '/'.join(k), 'committed': x, 'rerun': y, 'volatile': vol})
    nv = sum(d['volatile'] for d in diffs); na = len(diffs) - nv
    report['files'][name] = {'shared': len(shared), 'only_committed': len(set(a) - set(b)), 'only_rerun': len(set(b) - set(a)),
                             'diff_volatile': nv, 'diff_analytical': na, 'analytical_diffs': [d for d in diffs if not d['volatile']][:50]}
    t = report['totals']; t['shared'] += len(shared); t['equal'] += len(shared) - len(diffs); t['diff_volatile'] += nv; t['diff_analytical'] += na
json.dump(report, open(OUT, 'w'), indent=1, default=str)
print(json.dumps(report['totals']))
for n, r in report['files'].items():
    print(n, r if isinstance(r, str) else {k: r[k] for k in ('shared', 'diff_volatile', 'diff_analytical', 'only_committed', 'only_rerun')})
