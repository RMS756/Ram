"""Structural regression checks for the R4 Word table transformation (independent check of 1 Nov 2026, Finding 2).

The reviewed checkpoint inserted a second run-property container into runs that already had one.
These tests fix the required behaviour on a synthetic document; verification/check_docx_structure_R4.py
applies the same checks to the built thesis files.
"""
import importlib.util
import os

from lxml import etree

_p = os.path.join(os.path.dirname(__file__), '..', 'REM_FINAL_THESIS', 'tools', 'docx_tables.py')
_spec = importlib.util.spec_from_file_location('docx_tables', _p)
dt = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dt)

W, M = dt.W, dt.M
w = lambda t: f'{{{W}}}{t}'
NS = f'xmlns:w="{W}" xmlns:m="{M}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'

DOC = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document {NS}><w:body>
<w:p><w:r><w:t>outside table</w:t></w:r></w:p>
<w:tbl><w:tblPr/><w:tblGrid/>
<w:tr><w:trPr><w:tblHeader/></w:trPr>
<w:tc><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t>plain</w:t></w:r></w:p></w:tc>
<w:tc><w:p><w:pPr><w:pStyle w:val="Compact"/><w:jc w:val="center"/></w:pPr>
<w:r><w:rPr><w:b/><w:vertAlign w:val="subscript"/></w:rPr><w:t>bold sub</w:t></w:r></w:p></w:tc></w:tr>
<w:tr>
<w:tc><w:p><w:r><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr><w:t>sized</w:t></w:r></w:p></w:tc>
<w:tc><w:p><w:hyperlink r:id="rId9"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t>link</w:t></w:r></w:hyperlink>
<m:oMath><m:r><m:rPr><m:nor/><m:sty m:val="p"/></m:rPr><w:rPr><w:rFonts w:ascii="Cambria Math"/></w:rPr><m:t>x</m:t></m:r></m:oMath></w:p></w:tc></w:tr>
</w:tbl></w:body></w:document>'''.encode()


def _runs(root):
    return list(root.iter(w('r')))


def _names(el):
    return [etree.QName(c).localname for c in el]


def test_every_table_run_has_exactly_one_property_container_with_one_size():
    root = etree.fromstring(dt.transform(DOC))
    tbl = root.find(f'.//{w("tbl")}')
    runs = list(tbl.iter(w('r')))
    assert len(runs) == 4
    for r in runs:
        rprs = r.findall(w('rPr'))
        assert len(rprs) == 1 and r[0] is rprs[0]
        assert [e.get(w('val')) for e in rprs[0].findall(w('sz'))] == ['20']
        assert [e.get(w('val')) for e in rprs[0].findall(w('szCs'))] == ['20']


def test_existing_properties_are_kept_and_size_is_in_schema_order():
    root = etree.fromstring(dt.transform(DOC))
    bold = [r for r in _runs(root) if r.findtext(w('t')) == 'bold sub'][0]
    names = _names(bold.find(w('rPr')))
    assert names == ['b', 'sz', 'szCs', 'vertAlign']
    link = [r for r in _runs(root) if r.findtext(w('t')) == 'link'][0]
    assert _names(link.find(w('rPr'))) == ['rStyle', 'sz', 'szCs']
    assert link.getparent().tag == w('hyperlink')


def test_runs_outside_tables_and_equation_runs_are_not_resized():
    root = etree.fromstring(dt.transform(DOC))
    outside = [r for r in _runs(root) if r.findtext(w('t')) == 'outside table'][0]
    assert outside.find(w('rPr')) is None
    mr = root.find(f'.//{{{M}}}r')
    assert _names(mr.find(w('rPr'))) == ['rFonts']          # math run's Word properties untouched
    assert _names(mr.find(f'{{{M}}}rPr')) == ['nor']         # m:sty removed beside m:nor


def test_paragraph_and_row_properties():
    root = etree.fromstring(dt.transform(DOC))
    rows = root.findall(f'.//{w("tr")}')
    for tr in rows:
        assert len(tr.find(w('trPr')).findall(w('cantSplit'))) == 1
    first_row_ppr = rows[0].find(f'.//{w("pPr")}')
    assert _names(first_row_ppr) == ['pStyle', 'keepNext', 'jc']
    centred = rows[0].findall(f'.//{w("pPr")}')[1]
    assert centred.find(w('jc')).get(w('val')) == 'center'      # existing alignment kept
    last_row = rows[-1].findall(f'.//{w("pPr")}')
    assert all(p.find(w('keepNext')) is None for p in last_row)


def test_transformation_is_idempotent():
    once = dt.transform(DOC)
    assert dt.transform(once) == once
    assert dt.transform(dt.transform(once)) == once


def test_existing_duplicate_container_is_repaired_not_multiplied():
    bad = DOC.replace(b'<w:r><w:t>plain</w:t></w:r>',
                      b'<w:r><w:rPr><w:i/></w:rPr><w:rPr><w:b/></w:rPr><w:t>plain</w:t></w:r>')
    root = etree.fromstring(dt.transform(bad))
    plain = [r for r in _runs(root) if r.findtext(w('t')) == 'plain'][0]
    assert len(plain.findall(w('rPr'))) == 1
