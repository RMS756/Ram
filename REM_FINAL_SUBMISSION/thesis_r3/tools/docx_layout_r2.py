"""Second-edition layout pass for tables (run after REM_FINAL_THESIS/tools/docx_tables.process_docx).

The first edition kept every table of at most 25 rows on one page (w:keepNext on every paragraph) and forbade
page breaks inside any row (w:cantSplit). For tables with long cells this pushed the whole table to the next
page and left a heading or a caption alone on a nearly empty page. This pass estimates the height of each
table from its text and column widths and, for tall tables only, lets the table break between rows; rows that
are themselves tall may break inside. Short tables are unchanged. Text, numbers and equations are not touched.
"""
import math
import zipfile

from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
w = lambda t: f'{{{W}}}{t}'
TWIPS_PER_CHAR = 105          # about 10 pt Times New Roman
TALL_TABLE_LINES = 26         # more than about half a page of 10 pt lines
TALL_ROW_LINES = 10


def _row_lines(tr, widths):
    lines = 1
    cells = [c for c in tr if c.tag == w('tc')]
    for k, tc in enumerate(cells):
        wd = widths[k] if k < len(widths) else (widths[-1] if widths else 1500)
        per_line = max(4, wd / TWIPS_PER_CHAR)
        n = 0
        for p in tc.iter(w('p')):
            chars = sum(len(t.text or '') for t in p.iter(w('t')))
            n += max(1, math.ceil(chars / per_line))
        lines = max(lines, n)
    return lines


def relax(xml: bytes):
    head = xml[:xml.index(b'?>') + 2] if xml.startswith(b'<?xml') else b''
    root = etree.fromstring(xml)
    changed = 0
    for tbl in root.iter(w('tbl')):
        grid = tbl.find(w('tblGrid'))
        widths = [int(g.get(w('w')) or 1500) for g in grid] if grid is not None else []
        if widths and sum(widths) < 6000:            # relative grid written by pandoc: scale to the text width
            scale = 8790 / max(1, sum(widths))
            widths = [x * scale for x in widths]
        rows = [r for r in tbl if r.tag == w('tr')]
        per_row = [_row_lines(r, widths) for r in rows]
        if sum(per_row) <= TALL_TABLE_LINES:
            continue
        changed += 1
        for tr, n in zip(rows, per_row):
            for ppr in tr.iter(w('pPr')):
                for kn in ppr.findall(w('keepNext')):
                    ppr.remove(kn)
            if n > TALL_ROW_LINES:
                trpr = tr.find(w('trPr'))
                if trpr is not None:
                    for cs in trpr.findall(w('cantSplit')):
                        trpr.remove(cs)
        lead = rows[:2] if len(rows) >= 5 else rows[:1]   # the caption keeps with the header; keep the header and the first body rows together
        for tr in lead:
            for ppr in tr.iter(w('pPr')):
                if ppr.find(w('keepNext')) is None:
                    ppr.insert(1 if len(ppr) and ppr[0].tag == w('pStyle') else 0, etree.Element(w('keepNext')))
    return head + etree.tostring(root, encoding='UTF-8', xml_declaration=False), changed


def relax_docx(path):
    z = zipfile.ZipFile(path)
    files = {n: z.read(n) for n in z.namelist()}
    z.close()
    files['word/document.xml'], changed = relax(files['word/document.xml'])
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as zo:
        for n in sorted(files, key=lambda n: (n != '[Content_Types].xml', n)):
            zo.writestr(n, files[n])
    return changed
