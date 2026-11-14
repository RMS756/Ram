"""Build the five-chapter thesis (DOCX + PDF) and the five chapter files.

usage: python3 REM_FINAL_THESIS/tools/make_5ch.py && python3 REM_FINAL_THESIS/tools/figures_5ch.py \
       && python3 REM_FINAL_THESIS/tools/build_5ch.py          (from the repository root)

Inputs : final_five_chapters/src/*.md (make_5ch.py), tools/text_5ch/{front_matter_5ch,abstract_en,abstract_ar}.md,
         chapters_R5/FRONT_MATTER_R5.md (abbreviations), chapters_R5/REFERENCES_R5.md, figures.
Outputs: final_five_chapters/REM_THESIS_5CH_FINAL.{docx,pdf}, final_five_chapters/chapters/*.docx, build/ (ignored).
Layout : A4; Times New Roman 12 pt, 1.5 spacing, justified; margins 3.0 cm left, 2.5 cm right/top/bottom; Roman page
         numbers in the preliminary pages and Arabic numbers from Chapter One. These are ASSUMED university-style
         values (the reference thesis PDF was not available); see audit/FORMATTING_AUDIT.md.
Requires pandoc >= 3.5 (pypandoc_binary), python-docx, lxml, LibreOffice (with libreoffice-math), poppler-utils.
"""
import html
import json
import os
import re
import subprocess
import sys
import time
import zipfile

import pypandoc
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(TOOLS, '..', '..', '..'))
FIN = os.path.join(ROOT, 'REM_FINAL_SUBMISSION', 'thesis_r3')
TEXT = os.path.join(FIN, 'text_front')
OUTNAME = 'REM_THESIS_FINAL_R3'
SRC = os.path.join(FIN, 'src')
BUILD = os.path.join(FIN, 'build')
CHDIR = os.path.join(FIN, 'docx')
for d in (BUILD, CHDIR):
    os.makedirs(d, exist_ok=True)
P = pypandoc.get_pandoc_path()

# ------------------------------------------------------------------ pinned rendering environment (third edition)
# Page numbers depend on the renderer and on the fonts. The build refuses to run in another environment, so the
# DOCX, the PDF and every page reference in them come from one known configuration. Times New Roman is not
# installed; fontconfig substitutes the metric-compatible Liberation Serif, which is recorded here.
PIN = {"libreoffice": "24.2.7.2", "pandoc": "3.9",
       "serif_font_file": "LiberationSerif-Regular.ttf",
       "serif_font_sha256": "705903ae1382f0150f115d6f10a30f5b2f3d6ade649c474afe6366c39174fb65"}


def render_environment():
    import hashlib
    lo = subprocess.run(['soffice', '--version'], capture_output=True, text=True).stdout.strip()
    pv_ = subprocess.run([P, '--version'], capture_output=True, text=True).stdout.split('\n')[0].split()[-1]
    font = subprocess.run(['fc-match', 'Times New Roman', '-f', '%{file}'], capture_output=True, text=True).stdout.strip()
    env = {"libreoffice": lo.split()[1] if len(lo.split()) > 1 else lo, "pandoc": pv_, "serif_font_file": os.path.basename(font),
           "serif_font_sha256": hashlib.sha256(open(font, 'rb').read()).hexdigest() if os.path.exists(font) else None}
    bad = {k: (env[k], v) for k, v in PIN.items() if env[k] != v}
    if bad:
        sys.exit(f'rendering environment differs from the pinned one: {bad}')
    return env


RENDER_ENV = render_environment()
FMT = 'markdown+lists_without_preceding_blankline'
CHAPTERS = ['CHAPTER_01_FINAL', 'CHAPTER_02_FINAL', 'CHAPTER_03_FINAL', 'CHAPTER_04_FINAL', 'CHAPTER_05_FINAL']
TITLE = 'Runtime Evaluation and Mitigation (REM): A Security Framework for Financial AI Agents'

# ------------------------------------------------------------------ reference document (styles)
ref0 = os.path.join(BUILD, 'pandoc_default_reference.docx')
open(ref0, 'wb').write(subprocess.run([P, '--print-default-data-file', 'reference.docx'], capture_output=True, check=True).stdout)
doc = Document(ref0)
FONT = 'Times New Roman'


def font(style, size, bold=None, italic=None):
    rpr = style.element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rpr.insert(0, rf)
    for a in list(rf.attrib):
        del rf.attrib[a]
    for a in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rf.set(qn(a), FONT)
    style.font.size = Pt(size)
    style.font.color.rgb = RGBColor(0, 0, 0)
    if bold is not None:
        style.font.bold = bold
    if italic is not None:
        style.font.italic = italic


st = doc.styles
for n in ('Normal', 'Body Text', 'First Paragraph', 'Compact'):
    try:
        font(st[n], 12)
        pf = st[n].paragraph_format
        pf.line_spacing = 1.5 if n != 'Compact' else 1.15
        pf.space_after = Pt(6)
        if n in ('Body Text', 'First Paragraph'):
            pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    except KeyError:
        pass
for n, sz in (('Heading 1', 16), ('Heading 2', 14), ('Heading 3', 12), ('Heading 4', 12), ('Heading 5', 12)):
    try:
        font(st[n], sz, bold=True, italic=(n in ('Heading 4', 'Heading 5')))
        st[n].paragraph_format.keep_with_next = True
        st[n].paragraph_format.space_before = Pt(18 if n == 'Heading 1' else 12)
        st[n].paragraph_format.space_after = Pt(8)
    except KeyError:
        pass
st['Heading 1'].paragraph_format.page_break_before = True
st['Heading 1'].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
for n in ('Table Caption', 'Image Caption', 'Caption'):
    try:
        font(st[n], 11, bold=(n == 'Table Caption'), italic=(n != 'Table Caption'))
    except KeyError:
        pass
st['Table Caption'].paragraph_format.keep_with_next = True
for n in ('TOC Heading',):
    try:
        font(st[n], 16, bold=True)
        st[n].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    except KeyError:
        pass
for n in ('Source Code', 'Verbatim Char'):
    try:
        st[n].font.size = Pt(9.5)
    except KeyError:
        pass
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
sec.left_margin = Cm(3.0)
sec.right_margin = Cm(2.5)
sec.top_margin = Cm(2.5)
sec.bottom_margin = Cm(2.5)
sec.header_distance = Cm(1.25)
sec.footer_distance = Cm(1.25)
sec.gutter = Cm(0)
fp = sec.footer.paragraphs[0]
fp.text = ''
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
for kind, txt in (('begin', None), ('instr', ' PAGE '), ('separate', None), ('text', '1'), ('end', None)):
    r = fp.add_run()
    if kind == 'instr':
        e = OxmlElement('w:instrText')
        e.set(qn('xml:space'), 'preserve')
        e.text = txt
        r._r.append(e)
    elif kind == 'text':
        r.text = txt
    else:
        e = OxmlElement('w:fldChar')
        e.set(qn('w:fldCharType'), kind)
        r._r.append(e)
doc.core_properties.title = TITLE
doc.core_properties.author = 'Rawan Al-Lahham'
REF = os.path.join(BUILD, 'reference.docx')
doc.save(REF)

# ------------------------------------------------------------------ sources
sys.path.insert(0, TOOLS)
sys.path.insert(0, os.path.join(ROOT, 'REM_FINAL_THESIS', 'tools'))


def prepare(md):
    """Merge '# CHAPTER X' + '# TITLE'; bold table titles above pipe tables become table captions; column widths."""
    md = re.sub(r'^# (CHAPTER [A-Z]+)\n\n?# (.+)$', lambda m: f'# {m.group(1)}: {m.group(2)}', md, count=1, flags=re.M)
    L = md.split('\n')
    out = []
    i = 0
    while i < len(L):
        m = re.match(r'^\*\*(Table (?:\d+|[A-Z])\.\d+\.?.*?)\*\*(.*)$', L[i])
        if m:
            j = i + 1
            while j < len(L) and not L[j].strip():
                j += 1
            if j < len(L) and L[j].startswith('|'):
                out.append(f'Table: {(m.group(1) + m.group(2)).strip()}')
                out.append('')
                i += 1
                continue
        out.append(L[i])
        i += 1
    return widths('\n'.join(out))


def widths(md):
    L = md.split('\n')
    i = 0
    while i < len(L):
        if L[i].startswith('|') and i + 1 < len(L) and re.match(r'^\|(\s*:?-+:?\s*\|)+\s*$', L[i + 1]):
            j = i + 2
            while j < len(L) and L[j].startswith('|'):
                j += 1
            rows = [[c.strip() for c in r.strip().strip('|').split('|')] for r in [L[i]] + L[i + 2:j]]
            n = len(rows[0])
            if n >= 2 and all(len(r) == n for r in rows):
                BUDGET = 88
                lo, floor, want = [], [], []
                for k in range(n):
                    cells = [r[k] for r in rows]
                    body, head = cells[1:], cells[0]
                    word = max((len(x) for c in cells for x in c.split()), default=1)
                    longest = max(len(c) for c in cells)
                    numeric = all(re.fullmatch(r'[\s\d.,\[\]+\-−–/%—()≈<>×]*', c) for c in body)
                    if numeric:
                        lo.append(max(max(len(c) for c in body), max((len(x) for x in head.split()), default=1)) + 2)
                        floor.append(word + 2)
                        want.append(0)
                    else:
                        lo.append(word + 2)
                        floor.append(word + 2)
                        want.append(max(min(longest, 60) - word, 0))
                over = sum(lo) - BUDGET
                if over > 0:
                    room = sum(l - f for l, f in zip(lo, floor))
                    if room:
                        lo = [l - (l - f) * min(1, over / room) for l, f in zip(lo, floor)]
                spare = max(BUDGET - sum(lo), 0)
                tw = sum(want) or 1
                w = [lo[k] + spare * want[k] / tw for k in range(n)]
                tot = sum(w)
                L[i + 1] = '|' + '|'.join('-' * max(3, round(100 * x / tot)) for x in w) + '|'
            i = j
        else:
            i += 1
    return '\n'.join(L)


def para(text, size=12, bold=False, italic=False, space_after=6, align='center'):
    rpr = f'<w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}"/>' + ('<w:b/>' if bold else '') + ('<w:i/>' if italic else '') + f'<w:sz w:val="{size * 2}"/><w:szCs w:val="{size * 2}"/>'
    return (f'<w:p><w:pPr><w:spacing w:after="{space_after * 20}" w:line="276" w:lineRule="auto"/><w:jc w:val="{align}"/></w:pPr>'
            f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{html.escape(text, quote=False)}</w:t></w:r></w:p>')


TITLE_PAGE = '```{=openxml}\n' + ''.join([
    para('Al-Balqa Applied University', 16, bold=True, space_after=4),
    para('Faculty of Artificial Intelligence — Department of Intelligent Systems', 12, space_after=60),
    para(TITLE, 18, bold=True, space_after=60),
    para('By', 12, italic=True, space_after=4),
    para('Rawan Al-Lahham', 14, bold=True, space_after=40),
    para('Supervisor', 12, italic=True, space_after=4),
    para('Prof. Omar Ahmad Alzubi', 13, bold=True, space_after=16),
    para('Co-Supervisor', 12, italic=True, space_after=4),
    para('Dr. Husam Fakhouri', 13, bold=True, space_after=60),
    para('A thesis submitted in partial fulfilment of the requirements for the degree of Master of Science in Cybersecurity', 12, space_after=40),
    para('Al-Balqa Applied University', 12, space_after=4),
    para('November 2026', 12, space_after=4),
    para('Draft for supervisor review, third edition (14 November 2026) — not approved', 10, italic=True, space_after=0),
]) + '\n```\n'
TOC = ('```{=openxml}\n<w:sdt><w:sdtPr><w:docPartObj><w:docPartGallery w:val="Table of Contents"/><w:docPartUnique/></w:docPartObj></w:sdtPr>'
       '<w:sdtContent><w:p><w:pPr><w:pStyle w:val="TOCHeading"/><w:pageBreakBefore/></w:pPr><w:r><w:t xml:space="preserve">Table of Contents</w:t></w:r></w:p>'
       '<w:p><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/><w:instrText xml:space="preserve">TOC \\o "1-3" \\h \\z \\u</w:instrText>'
       '<w:fldChar w:fldCharType="separate"/><w:fldChar w:fldCharType="end"/></w:r></w:p></w:sdtContent></w:sdt>\n```\n')


def marker(name):
    return '```{=openxml}\n<w:p><w:r><w:t>@@' + name + '@@</w:t></w:r></w:p>\n```\n'


fm = open(os.path.join(TEXT, 'front_matter.md'), encoding='utf-8').read()
r5fm = open(os.path.join(ROOT, 'REM_FINAL_THESIS', 'chapters_R5', 'FRONT_MATTER_R5.md'), encoding='utf-8').read()
abbr = r5fm[r5fm.index('# List of Abbreviations'):].strip()
abbr = abbr.replace('| AUC | Area under the curve |', '| AUC | Area under the curve |\n| API | Application programming interface |')
for k, v in {'@@TITLE_PAGE@@': TITLE_PAGE, '@@TOC@@': TOC, '@@LOT@@': marker('LOT'), '@@LOF@@': marker('LOF'),
             '@@ABBREVIATIONS@@': abbr, '@@SECTION_BREAK@@': marker('SECTION_BREAK'),
             '@@ABSTRACT_EN@@': open(os.path.join(TEXT, 'abstract_en.md'), encoding='utf-8').read().strip(),
             '@@ABSTRACT_AR@@': open(os.path.join(TEXT, 'abstract_ar.md'), encoding='utf-8').read().strip()}.items():
    assert k in fm, k
    fm = fm.replace(k, v)
tmp = os.path.join(BUILD, 'src')
os.makedirs(tmp, exist_ok=True)
srcs = []
REFS = open(os.path.join(FIN, 'references', 'REFERENCES_FINAL.md'), encoding='utf-8').read().replace('# REFERENCES', '# References {.unnumbered}', 1)
APPX = open(os.path.join(SRC, 'APPENDICES_FINAL.md'), encoding='utf-8').read()
APPX = re.sub(r'^# (Appendix [A-Z]: .*)$', r'# \1 {.unnumbered}', APPX, flags=re.M)
APPX = re.sub(r'^(#{2,4}) ([A-Z](?:\.\d+)+ .*)$', r'\1 \2 {.unnumbered}', APPX, flags=re.M)
for name, text in [('FRONT_MATTER', fm)] + [(c, open(os.path.join(SRC, c + '.md'), encoding='utf-8').read()) for c in CHAPTERS] + \
        [('REFERENCES', REFS), ('APPENDICES', APPX)]:
    p = os.path.join(tmp, name + '.md')
    open(p, 'w', encoding='utf-8').write(prepare(text))
    srcs.append(p)


def pandoc(inputs, out, extra=()):
    subprocess.run([P, '-f', FMT, *inputs, '--resource-path', ROOT, '--reference-doc', REF, '-M', 'lang=en-GB', '-o', out, *extra],
                   check=True, cwd=ROOT)


from docx_tables import process_docx as _process_docx  # noqa: E402
from docx_layout_r2 import relax_docx  # noqa: E402


def process_docx(path):
    _process_docx(path)
    return relax_docx(path)


for c, s in zip(CHAPTERS, srcs[1:6]):
    out = os.path.join(CHDIR, c + '.docx')
    pandoc([s, srcs[6]], out)
    process_docx(out)
out = os.path.join(CHDIR, 'APPENDICES_FINAL.docx')
pandoc([srcs[7]], out)
process_docx(out)
out = os.path.join(CHDIR, 'REFERENCES_FINAL.docx')
pandoc([srcs[6]], out)
process_docx(out)
FULL = os.path.join(FIN, OUTNAME + '.docx')
PDF = FULL[:-5] + '.pdf'
pandoc(srcs, FULL)
process_docx(FULL)


def read_docx():
    z = zipfile.ZipFile(FULL)
    F = {n: z.read(n) for n in z.namelist()}
    z.close()
    return F


def write_docx(F):
    with zipfile.ZipFile(FULL, 'w', zipfile.ZIP_DEFLATED) as zo:
        for n in sorted(F, key=lambda n: (n != '[Content_Types].xml', n)):
            zo.writestr(n, F[n])


# ------------------------------------------------------------------ sections: Roman preliminary pages, Arabic main text
F = read_docx()
X = F['word/document.xml'].decode()
body_sect = re.findall(r'<w:sectPr\b.*?</w:sectPr>', X, flags=re.S)[-1]
pre = re.sub(r'<w:pgNumType[^>]*/>', '', body_sect)
pre = pre.replace('</w:sectPr>', '<w:pgNumType w:fmt="lowerRoman" w:start="1"/><w:titlePg/></w:sectPr>')
pre = re.sub(r'<w:type [^>]*/>', '', pre)
main = re.sub(r'<w:pgNumType[^>]*/>', '', body_sect).replace('</w:sectPr>', '<w:pgNumType w:fmt="decimal" w:start="1"/></w:sectPr>')
mk = re.search(r'<w:p>(?:(?!<w:p>).)*?@@SECTION_BREAK@@.*?</w:p>', X, flags=re.S)
assert mk, 'section marker missing'
X = X[:mk.start()] + f'<w:p><w:pPr>{pre}</w:pPr></w:p>' + X[mk.end():]
X = X[:X.rindex(body_sect)] + main + X[X.rindex(body_sect) + len(body_sect):]
# the first chapter heading follows a next-page section break: no additional page break
h1 = X.find('<w:pStyle w:val="Heading1" />', X.index('@@') if '@@LOT@@' in X else 0)
ch1 = re.search(r'<w:p><w:pPr><w:pStyle w:val="Heading1" ?/>(?=(?:(?!</w:p>).)*CHAPTER ONE)', X, flags=re.S)
assert ch1, 'chapter one heading not found'
X = X[:ch1.end()] + '<w:pageBreakBefore w:val="0"/>' + X[ch1.end():]
s = F['word/settings.xml'].decode()
if 'w:updateFields' not in s:
    k = min((s.find(t) for t in ('<w:hdrShapeDefaults', '<w:footnotePr', '<w:endnotePr', '<w:compat', '<w:docVars', '<w:rsids',
                                 '<m:mathPr', '<w:attachedSchema', '<w:themeFontLang', '<w:clrSchemeMapping', '<w:decimalSymbol',
                                 '<w:listSeparator') if s.find(t) >= 0), default=s.index('</w:settings>'))
    s = s[:k] + '<w:updateFields w:val="true"/>' + s[k:]
F['word/settings.xml'] = s.encode()
ct = F['[Content_Types].xml'].decode()
if 'Extension="png"' not in ct:
    ct = ct.replace('<Default Extension="xml"', '<Default Extension="png" ContentType="image/png" /><Default Extension="xml"', 1)
F['[Content_Types].xml'] = ct.encode()


def captions(style):
    out = []
    for m in re.finditer(r'<w:p>(?:(?!</w:p>).)*?<w:pStyle w:val="%s" ?/>.*?</w:p>' % style, X, flags=re.S):
        out.append(html.unescape(''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', m.group(0)))).strip())
    return out


CAPS = {'LOF': captions('ImageCaption'), 'LOT': captions('TableCaption')}
TW = int((21.0 - 3.0 - 2.5) / 2.54 * 1440)

# ------------------------------------------------------------------ table of contents stored in the DOCX
# The TOC field of the first edition had an empty cached result: LibreOffice filled it only in memory for the PDF, so
# the DOCX opened with an empty contents page until the reader updated the field. The entries computed by LibreOffice
# (titles and displayed page numbers) are now written into the field result, as Word itself stores a table of contents.
HEADS = []
for _m in re.finditer(r'<w:p>(?:(?!</w:p>).)*?<w:pStyle w:val="Heading([123])" ?/>.*?</w:p>', X, flags=re.S):
    _t = html.unescape(''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', _m.group(0)))).strip()
    if _t:
        HEADS.append((int(_m.group(1)), _t))
_toc = re.search(r'<w:p>(?:(?!<w:p>).)*?TOC \\o "1-3".*?</w:p>', X, flags=re.S)
assert _toc, 'TOC field paragraph not found'
TOC_EMPTY = _toc.group(0)
X = X[:_toc.start()] + '<!--TOC-->' + TOC_EMPTY + '<!--/TOC-->' + X[_toc.end():]
TOC_LINES = None
_norm = lambda t: re.sub(r'\s+', ' ', t).strip()


def toc_xml(lines):
    """Field result paragraphs for the entries [(title, page)], with levels taken from the heading list."""
    if not lines:
        return TOC_EMPTY
    levels, k = [], 0
    for title, _pg in lines:                           # same order as the headings; match forward by text
        j = next((i for i in range(k, len(HEADS)) if _norm(HEADS[i][1]) == _norm(title)), None)
        if j is None:
            levels.append(1)
        else:
            levels.append(HEADS[j][0])
            k = j + 1
    begin = ('<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve">TOC \\o "1-3" \\h \\z \\u</w:instrText></w:r>'
             '<w:r><w:fldChar w:fldCharType="separate"/></w:r>')
    out = []
    for i, ((title, pg), lvl) in enumerate(zip(lines, levels)):
        rpr = '<w:rPr>' + ('<w:b/>' if lvl == 1 else '') + '<w:sz w:val="22"/></w:rPr>'
        out.append('<w:p><w:pPr><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="%d"/></w:tabs><w:spacing w:before="%d" w:after="40" w:line="240" w:lineRule="auto"/>'
                   '<w:ind w:left="%d" w:hanging="0"/><w:jc w:val="left"/></w:pPr>%s<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r><w:r><w:tab/></w:r><w:r>%s<w:t>%s</w:t></w:r></w:p>'
                   % (TW, 120 if lvl == 1 else 0, (lvl - 1) * 300, begin if i == 0 else '', rpr, html.escape(title, quote=False), rpr, html.escape(pg, quote=False)))
    out.append('<w:p><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>')
    return ''.join(out)



def fill(pages):
    global X
    for key in ('LOT', 'LOF'):
        paras = ''.join(
            '<w:p><w:pPr><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="%d"/></w:tabs><w:spacing w:after="60" w:line="240" w:lineRule="auto"/>'
            '<w:ind w:left="0" w:hanging="0"/></w:pPr><w:r><w:rPr><w:sz w:val="22"/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r><w:r><w:tab/></w:r>'
            '<w:r><w:rPr><w:sz w:val="22"/></w:rPr><w:t>%s</w:t></w:r></w:p>' % (TW, html.escape(c, quote=False), pg or '')
            for c, pg in zip(CAPS[key], pages[key]))
        start = X.index('<!--%s-->' % key) if ('<!--%s-->' % key) in X else None
        if start is None:
            m = re.search(r'<w:p>(?:(?!<w:p>).)*?@@%s@@.*?</w:p>' % key, X, flags=re.S)
            X = X[:m.start()] + '<!--%s-->' % key + paras + '<!--/%s-->' % key + X[m.end():]
        else:
            end = X.index('<!--/%s-->' % key)
            X = X[:start] + '<!--%s-->' % key + paras + X[end:]
    a_, b_ = X.index('<!--TOC-->'), X.index('<!--/TOC-->')
    X = X[:a_] + '<!--TOC-->' + toc_xml(TOC_LINES) + X[b_:]
    clean = re.sub(r'<!--/?(LOT|LOF|TOC)-->', '', X)
    F['word/document.xml'] = clean.encode()
    write_docx(F)


import uno  # noqa: E402
from com.sun.star.beans import PropertyValue  # noqa: E402


def pv(n, v):
    p = PropertyValue()
    p.Name = n
    p.Value = v
    return p


def export_pdf():
    prof = os.path.join(BUILD, 'lo_profile')
    proc = subprocess.Popen(['soffice', '-env:UserInstallation=file://' + prof, '--headless', '--invisible', '--norestore',
                             '--nologo', '--accept=socket,host=127.0.0.1,port=2019;urp;'],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=dict(os.environ, SAL_USE_VCLPLUGIN='svp'))
    local = uno.getComponentContext()
    res = local.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver', local)
    ctx = None
    for _ in range(90):
        try:
            ctx = res.resolve('uno:socket,host=127.0.0.1,port=2019;urp;StarOffice.ComponentContext')
            break
        except Exception:
            time.sleep(1)
    assert ctx is not None, 'LibreOffice did not start'
    desk = ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', ctx)
    d = desk.loadComponentFromURL('file://' + FULL, '_blank', 0, (pv('Hidden', True),))
    idx = d.getDocumentIndexes()
    for i in range(idx.getCount()):
        idx.getByIndex(i).update()
    d.refresh()
    for i in range(idx.getCount()):
        idx.getByIndex(i).update()
    toc = []
    if idx.getCount():
        for line in idx.getByIndex(0).getAnchor().getString().replace('\r', '').split('\n'):
            if '\t' in line:
                title, pg = line.rsplit('\t', 1)
                if title.strip() and pg.strip():
                    toc.append((title.strip(), pg.strip()))
    d.storeToURL('file://' + PDF, (pv('FilterName', 'writer_pdf_Export'),))
    d.close(True)
    try:
        desk.terminate()
    except Exception:
        pass
    proc.wait(timeout=60)
    return toc


def pages_of(caps):
    txt = subprocess.run(['pdftotext', '-layout', PDF, '-'], capture_output=True, text=True).stdout.split('\f')
    norm = lambda t: re.sub(r'\s+', ' ', t)
    pages = [norm(p) for p in txt]
    start = next(i for i, p in enumerate(pages) if 'Artificial intelligence systems based on large language models' in p)
    res = []
    for c in caps:
        key = norm(c)[:55]
        pg = next((i + 1 for i in range(start, len(pages)) if key in pages[i]), None)
        res.append(pg - start if pg else None)            # displayed Arabic page number (Chapter One starts at 1)
    return res


pages = {k: [None] * len(v) for k, v in CAPS.items()}
fill(pages)
toc_now = export_pdf()
for _ in range(5):
    new = {k: pages_of(v) for k, v in CAPS.items()}
    if new == pages and toc_now == TOC_LINES:
        break
    pages, TOC_LINES = new, toc_now
    fill(pages)
    toc_now = export_pdf()
assert TOC_LINES and toc_now == TOC_LINES, 'table of contents did not stabilize'
unmatched = [t for t, _ in TOC_LINES if _norm(t) not in {_norm(h[1]) for h in HEADS}]
json.dump({'entries': TOC_LINES, 'headings_levels_1_to_3': len(HEADS), 'entries_without_matching_heading': unmatched},
          open(os.path.join(FIN, 'audit', 'toc_entries.json'), 'w'), indent=1, ensure_ascii=False)
fonts = subprocess.run(['pdffonts', PDF], capture_output=True, text=True).stdout
json.dump({"pinned": PIN, "observed": RENDER_ENV, "pdf_fonts": [l.split()[0].split('+')[-1] for l in fonts.split('\n')[2:] if l.strip()]},
          open(os.path.join(FIN, 'audit', 'render_environment.json'), 'w'), indent=1)
print('table of contents stored in the DOCX:', len(TOC_LINES), 'entries;', len(HEADS), 'headings of levels 1-3; unmatched', len(unmatched))
missing = {k: sum(1 for p in v if not p) for k, v in pages.items()}
json.dump({k: list(zip(CAPS[k], v)) for k, v in pages.items()}, open(os.path.join(BUILD, 'lists_pages.json'), 'w'), indent=1)
print('built:', FULL, os.path.getsize(FULL), 'bytes; PDF', os.path.getsize(PDF), 'bytes; figures', len(CAPS['LOF']),
      'tables', len(CAPS['LOT']), 'captions without page', missing)
