const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, LevelFormat, PageOrientation, Footer, Header, PageNumber,
  TableLayoutType, VerticalAlign,
} = require('docx');

const SRC = process.argv[2];
const OUT = process.argv[3];
const md = fs.readFileSync(SRC, 'utf8').split('\n');

const FONT = 'Times New Roman';
const BODY = 24;   // 12 pt
const TBL = 16;    // 8 pt
const TBL_WIDE = 15; // 7.5 pt

// Unicode renderings of the display equations (keyed by equation number)
const EQ = {
  '2.1': 'Pr(y = 1 | x) = 1 / (1 + exp(−(β₀ + βᵀx)))',
  '2.2': 'p̂ = Pr(y = 1 | s) = 1 / (1 + exp(A·s + B))',
  '2.3': 'ECE = Σₘ₌₁ᴹ (|Bₘ| / n) · |acc(Bₘ) − conf(Bₘ)|',
  '2.4': 'gₜ = max(0, gₜ₋₁ + sₜ),   sₜ = ln[ p₁(zₜ) / p₀(zₜ) ],   g₀ = 0',
  '2.5': 'a*(x) = arg minₐ  Σ_{y ∈ {0,1}}  Pr(y | x) · C(a, y)',
  '2.6': 'φⱼ = βⱼ · (xⱼ − E[xⱼ])',
};

// ---------- inline markdown -> TextRuns ----------
function runs(text, opts = {}) {
  const size = opts.size || BODY;
  const out = [];
  // tokens: **bold**, *italic*, <sub>..</sub>, `code`
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|<sub>.*?<\/sub>|`[^`]+`)/g;
  let last = 0, m;
  const push = (t, o = {}) => { if (t) out.push(new TextRun({ text: t, font: FONT, size, bold: opts.bold || o.bold, italics: opts.italics || o.italics, subScript: o.sub })); };
  while ((m = re.exec(text)) !== null) {
    push(text.slice(last, m.index));
    const tok = m[0];
    if (tok.startsWith('**')) {
      // allow nested *italic* inside bold
      const inner = tok.slice(2, -2);
      inner.split(/(\*[^*]+\*)/).forEach(p => {
        if (p.startsWith('*') && p.endsWith('*') && p.length > 2) push(p.slice(1, -1), { bold: true, italics: true });
        else push(p, { bold: true });
      });
    } else if (tok.startsWith('<sub>')) push(tok.slice(5, -6), { sub: true, italics: true });
    else if (tok.startsWith('`')) push(tok.slice(1, -1));
    else push(tok.slice(1, -1), { italics: true });
    last = m.index + tok.length;
  }
  push(text.slice(last));
  return out;
}
const clean = s => s.replace(/\\\|/g, '|');

// ---------- block parsing ----------
const sections = [];   // {landscape:bool, children:[]}
let cur = { landscape: false, children: [] };
sections.push(cur);
function newSection(landscape) {
  if (cur.children.length === 0) { cur.landscape = landscape; return; }
  cur = { landscape, children: [] };
  sections.push(cur);
}

let inRefs = false;
let i = 0;
let pendingCaption = null;

function para(text, o = {}) {
  return new Paragraph({
    children: runs(text, o),
    alignment: o.align || (inRefs ? AlignmentType.LEFT : AlignmentType.JUSTIFIED),
    spacing: { after: o.after ?? 120, line: o.line ?? 360 },
    indent: inRefs ? { left: 720, hanging: 720 } : o.indent,
    keepNext: o.keepNext,
  });
}

function buildTable(rows) {
  const header = rows[0];
  const ncol = header.length;
  const landscape = ncol >= 7;
  const total = landscape ? 13958 : 9026; // A4 text width (1" margins): portrait 9026, landscape 13958
  // weight columns by average text length (bounded)
  const lens = header.map((_, c) => {
    const vals = rows.map(r => (r[c] || '').length);
    const avg = vals.reduce((a, b) => a + b, 0) / vals.length;
    return Math.min(Math.max(avg, 6), 60);
  });
  const sum = lens.reduce((a, b) => a + b, 0);
  let widths = lens.map(l => Math.floor(total * l / sum));
  widths[widths.length - 1] += total - widths.reduce((a, b) => a + b, 0);
  const size = ncol >= 9 ? TBL_WIDE : TBL;
  const border = { style: BorderStyle.SINGLE, size: 4, color: '808080' };
  const borders = { top: border, bottom: border, left: border, right: border };
  const trs = rows.map((r, ri) => new TableRow({
    tableHeader: ri === 0,
    cantSplit: true,
    children: widths.map((w, ci) => new TableCell({
      width: { size: w, type: WidthType.DXA },
      borders,
      verticalAlign: VerticalAlign.TOP,
      margins: { top: 40, bottom: 40, left: 70, right: 70 },
      shading: ri === 0 ? { fill: 'D9E2F3', type: ShadingType.CLEAR, color: 'auto' } : undefined,
      children: [new Paragraph({
        children: runs(clean(r[ci] || ''), { size, bold: ri === 0 }),
        spacing: { after: 0, line: 240 },
        alignment: AlignmentType.LEFT,
      })],
    })),
  }));
  return { table: new Table({ width: { size: total, type: WidthType.DXA }, columnWidths: widths, layout: TableLayoutType.FIXED, rows: trs }), landscape };
}

while (i < md.length) {
  let line = md[i];
  if (/^---\s*$/.test(line)) { i++; continue; }
  if (/^\s*$/.test(line)) { i++; continue; }

  // headings
  let h;
  if ((h = line.match(/^(#{1,3}) (.*)$/))) {
    const level = h[1].length;
    const txt = h[2];
    if (txt === 'References') inRefs = true;
    if (level === 1) {
      cur.children.push(new Paragraph({ heading: HeadingLevel.TITLE, alignment: AlignmentType.CENTER, children: [new TextRun({ text: txt, font: FONT, size: 32, bold: true })], spacing: { after: 120 } }));
    } else {
      const hl = level === 2 ? HeadingLevel.HEADING_1 : HeadingLevel.HEADING_2;
      cur.children.push(new Paragraph({ heading: hl, keepNext: true, children: [new TextRun({ text: txt, font: FONT, size: level === 2 ? 28 : 24, bold: true, italics: level === 3 })], spacing: { before: level === 2 ? 360 : 240, after: 120 } }));
    }
    i++; continue;
  }

  // display equation
  if (line.startsWith('$$')) {
    const num = (line.match(/\((2\.\d)\)\s*\$\$\s*$/) || [])[1];
    cur.children.push(new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { before: 120, after: 160 },
      children: [new TextRun({ text: EQ[num] || line, font: 'Cambria Math', size: BODY }), new TextRun({ text: `\t(${num})`, font: FONT, size: BODY })],
      tabStops: [{ type: 'right', position: 9026 }],
    }));
    i++; continue;
  }

  // table
  if (line.startsWith('|')) {
    const rows = [];
    while (i < md.length && md[i].startsWith('|')) {
      const raw = md[i].trim();
      if (!/^\|[\s|:\-]+\|$/.test(raw)) {
        const cells = raw.slice(1, -1).split(/(?<!\\)\|/).map(c => c.trim());
        rows.push(cells);
      }
      i++;
    }
    const { table, landscape } = buildTable(rows);
    if (landscape) newSection(true);
    if (pendingCaption) { cur.children.push(pendingCaption); pendingCaption = null; }
    cur.children.push(table);
    cur.children.push(new Paragraph({ children: [], spacing: { after: 120 } }));
    // collect note lines immediately following (e.g., footnote ᵃ)
    while (i < md.length && /^\s*$/.test(md[i])) i++;
    if (i < md.length && md[i].startsWith('ᵃ')) { cur.children.push(para(md[i], { size: 18, after: 200 })); i++; }
    if (landscape) newSection(false);
    continue;
  }

  // table caption (bold "Table 2.x." line) -> hold until table
  if (/^\*\*Table 2\.\d+\./.test(line)) {
    pendingCaption = new Paragraph({ children: runs(line), keepNext: true, spacing: { before: 200, after: 80 } });
    i++; continue;
  }

  // block quote
  if (line.startsWith('> ')) {
    let q = [];
    while (i < md.length && md[i].startsWith('>')) { q.push(md[i].replace(/^>\s?/, '')); i++; }
    cur.children.push(new Paragraph({ children: runs(q.join(' '), { italics: false }), indent: { left: 720, right: 720 }, alignment: AlignmentType.JUSTIFIED, spacing: { before: 120, after: 160, line: 300 },
      border: { left: { style: BorderStyle.SINGLE, size: 12, color: '4472C4', space: 8 } } }));
    continue;
  }

  // lists
  if (/^(\s*)- /.test(line)) {
    const m2 = line.match(/^(\s*)- (.*)$/);
    const lvl = m2[1].length >= 2 ? 1 : 0;
    cur.children.push(new Paragraph({ numbering: { reference: 'bullets', level: lvl }, children: runs(m2[2]), alignment: AlignmentType.JUSTIFIED, spacing: { after: 80, line: 360 } }));
    i++; continue;
  }
  if (/^\d+\. /.test(line)) {
    const m3 = line.match(/^\d+\. (.*)$/);
    cur.children.push(new Paragraph({ numbering: { reference: 'numbers', level: 0 }, children: runs(m3[1]), alignment: AlignmentType.JUSTIFIED, spacing: { after: 80, line: 360 } }));
    i++; continue;
  }
  // indented continuation lines inside list items (e.g., under a bullet)
  if (/^\s{2,}\S/.test(line)) {
    cur.children.push(para(line.trim(), { indent: { left: 720 } }));
    i++; continue;
  }

  // paragraph (join consecutive non-blank lines)
  let p = [line];
  i++;
  while (i < md.length && md[i].trim() && !/^(#|\||>|\$\$|- |\d+\. |---)/.test(md[i]) && !/^\s{2,}\S/.test(md[i])) { p.push(md[i]); i++; }
  cur.children.push(para(p.join(' ')));
}

const footer = new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 20 })] })] });
const header = new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: 'Chapter 2 — Literature Review', font: FONT, size: 18, italics: true, color: '595959' })] })] });

const doc = new Document({
  creator: 'REM thesis',
  title: 'Chapter 2 — Literature Review (Integrated)',
  styles: {
    default: { document: { run: { font: FONT, size: BODY } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 28, bold: true, color: '000000' }, paragraph: { spacing: { before: 360, after: 120 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 24, bold: true, italics: true, color: '000000' }, paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 } },
      { id: 'Title', name: 'Title', basedOn: 'Normal', run: { font: FONT, size: 32, bold: true, color: '000000' } },
    ],
  },
  numbering: {
    config: [
      { reference: 'bullets', levels: [
        { level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
        { level: 1, format: LevelFormat.BULLET, text: '◦', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1440, hanging: 360 } } } },
      ] },
      { reference: 'numbers', levels: [
        { level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
      ] },
    ],
  },
  sections: sections.map(s => ({
    properties: { page: { size: { width: 11906, height: 16838, orientation: s.landscape ? PageOrientation.LANDSCAPE : PageOrientation.PORTRAIT }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    headers: { default: header }, footers: { default: footer },
    children: s.children,
  })),
});

Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log('wrote', OUT, 'sections:', sections.length); });
