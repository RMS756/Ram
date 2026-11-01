"""XML-aware post-processing of the R4 Word files (tables and equation run properties).

Used by build_thesis.py in R4 mode; tested by tests/test_docx_tables.py; checked on the built files
by verification/check_docx_structure_R4.py.

What it does, inside every table (w:tbl) of word/document.xml:
  * every text run (w:r, including runs inside hyperlinks) gets exactly one run-property container
    (w:rPr): an existing container is updated, a new one is created only when absent; font size is
    set to 10 pt (w:sz, w:szCs), replacing any earlier size, at its schema position;
  * every paragraph is left-aligned (w:jc) unless it already has an alignment;
  * every row gets w:cantSplit; in tables of at most KEEP_ROWS rows, every paragraph except those of
    the last row gets w:keepNext, so short tables stay on one page.
Everywhere: an OMML run-property container holding both m:nor and m:sty keeps m:nor only (the
schema allows one; pandoc writes both for \\text{}). Equation runs (m:r) are otherwise untouched.
Applying the transformation twice gives the same bytes as applying it once.
"""
import zipfile

from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
w = lambda t: f'{{{W}}}{t}'
m = lambda t: f'{{{M}}}{t}'
SIZE = '20'          # half-points: 10 pt
KEEP_ROWS = 25

# schema (ECMA-376 CT_RPr / CT_PPr) child order, used to insert new children at a valid position
RPR_ORDER = ['rStyle', 'rFonts', 'b', 'bCs', 'i', 'iCs', 'caps', 'smallCaps', 'strike', 'dstrike', 'outline', 'shadow',
             'emboss', 'imprint', 'noProof', 'snapToGrid', 'vanish', 'webHidden', 'color', 'spacing', 'w', 'kern',
             'position', 'sz', 'szCs', 'highlight', 'u', 'effect', 'bdr', 'shd', 'fitText', 'vertAlign', 'rtl', 'cs',
             'em', 'lang', 'eastAsianLayout', 'specVanish', 'oMath', 'rPrChange']
PPR_ORDER = ['pStyle', 'keepNext', 'keepLines', 'pageBreakBefore', 'framePr', 'widowControl', 'numPr',
             'suppressLineNumbers', 'pBdr', 'shd', 'tabs', 'suppressAutoHyphens', 'kinsoku', 'wordWrap',
             'overflowPunct', 'topLinePunct', 'autoSpaceDE', 'autoSpaceDN', 'bidi', 'adjustRightInd', 'snapToGrid',
             'spacing', 'ind', 'contextualSpacing', 'mirrorIndents', 'suppressOverlap', 'jc', 'textDirection',
             'textAlignment', 'textboxTightWrap', 'outlineLvl', 'divId', 'cnfStyle', 'rPr', 'sectPr', 'pPrChange']


def _local(el):
    return etree.QName(el).localname if isinstance(el.tag, str) else None


def _insert_ordered(parent, child, order):
    """Insert child before the first existing sibling that the schema places after it."""
    k = order.index(_local(child))
    for i, c in enumerate(parent):
        name = _local(c)
        if name in order and order.index(name) > k:
            parent.insert(i, child)
            return child
    parent.append(child)
    return child


def _first_child(parent, tag, create_at=0):
    """Return the single child `tag`, creating it at position create_at when absent."""
    found = parent.find(tag)
    if found is None:
        found = etree.Element(tag)
        parent.insert(create_at, found)
    return found


def _set(parent, name, order, value=None):
    """Ensure exactly one child `name` (optionally with w:val=value) at its schema position."""
    old = parent.findall(w(name))
    if len(old) == 1 and (value is None or old[0].get(w('val')) == value):
        return old[0]
    for o in old:
        parent.remove(o)
    el = etree.Element(w(name))
    if value is not None:
        el.set(w('val'), value)
    return _insert_ordered(parent, el, order)


def _run(r):
    rpr = _first_child(r, w('rPr'))          # w:rPr is the first child of w:r
    for extra in r.findall(w('rPr'))[1:]:     # repair, never create, a second container
        r.remove(extra)
    _set(rpr, 'sz', RPR_ORDER, SIZE)
    _set(rpr, 'szCs', RPR_ORDER, SIZE)


def _paragraph(p, keep_next):
    ppr = _first_child(p, w('pPr'))
    if ppr.find(w('jc')) is None:
        _set(ppr, 'jc', PPR_ORDER, 'left')
    if keep_next:
        _set(ppr, 'keepNext', PPR_ORDER)


def _table(tbl):
    rows = [r for r in tbl if _local(r) == 'tr']
    for i, tr in enumerate(rows):
        trpr = tr.find(w('trPr'))
        if trpr is None:
            trpr = etree.Element(w('trPr'))
            k = 1 if (len(tr) and _local(tr[0]) == 'tblPrEx') else 0
            tr.insert(k, trpr)
        if trpr.find(w('cantSplit')) is None:
            trpr.insert(0, etree.Element(w('cantSplit')))
        keep = len(rows) <= KEEP_ROWS and i < len(rows) - 1
        for p in tr.iter(w('p')):
            _paragraph(p, keep)
    for r in tbl.iter(w('r')):
        _run(r)


def _math(root):
    for rpr in root.iter(m('rPr')):
        if rpr.find(m('nor')) is not None:
            for sty in rpr.findall(m('sty')):
                rpr.remove(sty)


def transform(xml: bytes) -> bytes:
    """Transform word/document.xml; the XML declaration is kept as written."""
    head = xml[:xml.index(b'?>') + 2] if xml.startswith(b'<?xml') else b''
    root = etree.fromstring(xml)
    for tbl in root.iter(w('tbl')):
        _table(tbl)
    _math(root)
    return head + etree.tostring(root, encoding='UTF-8', xml_declaration=False)


def process_docx(path):
    """Rewrite one DOCX in place: document.xml transformed, png declared as a default content type."""
    z = zipfile.ZipFile(path)
    files = {n: z.read(n) for n in z.namelist()}
    z.close()
    files['word/document.xml'] = transform(files['word/document.xml'])
    ct = files['[Content_Types].xml'].decode()
    if 'Extension="png"' not in ct:
        ct = ct.replace('<Default Extension="xml"', '<Default Extension="png" ContentType="image/png" /><Default Extension="xml"', 1)
    files['[Content_Types].xml'] = ct.encode()
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as zo:
        for n in sorted(files, key=lambda n: (n != '[Content_Types].xml', n)):
            zo.writestr(n, files[n])
