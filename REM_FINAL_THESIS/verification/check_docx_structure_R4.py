"""Structural checks of the built R4 Word files (independent check of 1 Nov 2026, Finding 2).

usage: python3 REM_FINAL_THESIS/verification/check_docx_structure_R4.py   (from the repository root)
For every DOCX in REM_FINAL_THESIS/R4/: runs with more than one w:rPr; w:rPr with repeated w:sz or
w:szCs; table runs without a 10-pt size; run and paragraph properties out of schema order; OMML
run properties holding both m:nor and m:sty; and whether applying the transformation again changes
the document (it must not). Writes verification/docx_structure_R4.txt; exit 1 on any finding.
"""
import glob
import importlib.util
import os
import sys
import zipfile

from lxml import etree

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
spec = importlib.util.spec_from_file_location('docx_tables', os.path.join(ROOT, 'REM_FINAL_THESIS', 'tools', 'docx_tables.py'))
dt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dt)
w = lambda t: f'{{{dt.W}}}{t}'
m = lambda t: f'{{{dt.M}}}{t}'


def ordered(el, order):
    idx = [order.index(etree.QName(c).localname) for c in el if etree.QName(c).localname in order]
    return idx == sorted(idx)


def check(path):
    xml = zipfile.ZipFile(path).read('word/document.xml')
    root = etree.fromstring(xml)
    runs = list(root.iter(w('r')))
    multi = sum(1 for r in runs if len(r.findall(w('rPr'))) > 1)
    dup_sz = sum(1 for p in root.iter(w('rPr')) if len(p.findall(w('sz'))) > 1 or len(p.findall(w('szCs'))) > 1)
    trs = [r for t in root.iter(w('tbl')) for r in t.iter(w('r'))]
    unsized = sum(1 for r in trs if r.find(w('rPr')) is None or r.find(w('rPr')).find(w('sz')) is None
                  or r.find(w('rPr')).find(w('sz')).get(w('val')) != dt.SIZE)
    bad_rpr = sum(1 for p in root.iter(w('rPr')) if p.getparent().tag == w('r') and not ordered(p, dt.RPR_ORDER))
    bad_ppr = sum(1 for p in root.iter(w('pPr')) if not ordered(p, dt.PPR_ORDER))
    norsty = sum(1 for p in root.iter(m('rPr')) if p.find(m('nor')) is not None and p.find(m('sty')) is not None)
    c14n = lambda b: etree.tostring(etree.fromstring(b), method='c14n')   # compare content, not serialization style
    idem = c14n(dt.transform(xml)) == c14n(xml)
    return dict(runs=len(runs), table_runs=len(trs), multi_rPr=multi, repeated_size=dup_sz, table_runs_not_10pt=unsized,
                rPr_out_of_order=bad_rpr, pPr_out_of_order=bad_ppr, math_nor_and_sty=norsty, idempotent=idem)


if __name__ == '__main__':
    lines, bad = [], False
    for f in sorted(glob.glob(os.path.join(ROOT, 'REM_FINAL_THESIS', 'R4', '*.docx'))):
        r = check(f)
        fail = any(r[k] for k in ('multi_rPr', 'repeated_size', 'table_runs_not_10pt', 'rPr_out_of_order', 'pPr_out_of_order', 'math_nor_and_sty')) or not r['idempotent']
        bad |= fail
        lines.append(f"{'FAIL' if fail else 'PASS'} {os.path.basename(f)} {r}")
    out = os.path.join(ROOT, 'REM_FINAL_THESIS', 'verification', 'docx_structure_R4.txt')
    open(out, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))
    sys.exit(1 if bad else 0)
