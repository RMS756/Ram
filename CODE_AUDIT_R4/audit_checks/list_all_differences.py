"""List every differing numeric/string leaf between a reproduced result dir and a committed one."""
import collections, json, os, sys
a, b = sys.argv[1], sys.argv[2]
def leaves(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items(): yield from leaves(v, f"{p}/{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from leaves(v, f"{p}[{i}]")
    else: yield p, o
c, n, examples = collections.Counter(), 0, {}
for f in sorted(os.listdir(b)):
    if not f.endswith(".json"): continue
    A = dict(leaves(json.load(open(os.path.join(a, f))))); B = dict(leaves(json.load(open(os.path.join(b, f)))))
    for k in set(A) & set(B):
        if A[k] != B[k]:
            n += 1; key = k.split("/")[-1].split("[")[0]; c[key] += 1; examples.setdefault(key, f"{f}:{k}")
print("differing shared leaves:", n); print(dict(c)); print(examples)
