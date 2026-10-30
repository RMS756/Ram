"""Build REFERENCES_VERIFIED.md: one row per consolidated reference with its verification record.
Sources of status (no status is assigned without a record):
  REFERENCE_VERIFICATION_MATRIX.xlsx (foundational works, 27 Oct)
  revision_R2/evidence/included_register_R2.csv (71 included studies, record level)
  chapter2/CHAPTER2_REFERENCE_EVIDENCE_MATRIX.md (Sept. evidence matrix, 70 sources)
  R3 checks of 30 Oct (Crossref / OpenAlex records through the literature connector)."""
import csv, json, os, re, openpyxl
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
refs = json.load(open(os.path.join(ROOT, 'REM_FINAL_THESIS/verification/consolidated_references.json')))

def key(author_field, year):
    a = author_field.strip()
    sur = re.split(r'[,\s]', a.replace('le Cessie', 'Cessie'))[0] if not a.startswith('le ') else 'Cessie'
    return (sur.lower(), year)

found = {}
ws = openpyxl.load_workbook(os.path.join(ROOT, 'REFERENCE_VERIFICATION_MATRIX.xlsx')).active
for r in list(ws.values)[1:]:
    m = re.match(r'(.+?)\s\((\d{4})', r[1] or '')
    if m:
        found.setdefault(key(m.group(1), m.group(2)), []).append(
            f'Foundational record (27 Oct): metadata {r[4]}; formulation {r[5]}')
for r in csv.DictReader(open(os.path.join(ROOT, 'revision_R2/evidence/included_register_R2.csv'))):
    m = re.match(r'(?:[A-Z]\.(?:-[A-Z]\.)?\s(?:[A-Z]\.\s)?)?([A-Za-z\-]+).*\((\d{4})\)', r['Study'])
    if m:
        found.setdefault((m.group(1).lower(), m.group(2)), []).append(
            f"Included study {r['ID']} (record-level review): {r['Verification']}; {r['Evidence level']}")
for line in open(os.path.join(ROOT, 'chapter2/CHAPTER2_REFERENCE_EVIDENCE_MATRIX.md'), encoding='utf-8'):
    if not line.startswith('| S') and not re.match(r'^\| [A-Z]?\d', line):
        continue
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    if len(cells) < 14:
        continue
    paper, year, ver = cells[1], cells[2], cells[-1]
    m = re.match(r'(?:[A-Z]\.(?:-[A-Z]\.)?\s(?:[A-Z]\.\s)?)?([A-Za-z\-]+)', paper)
    if m and re.match(r'\d{4}', year):
        found.setdefault((m.group(1).lower(), year[:4]), []).append(f'Sept. evidence matrix: {ver}')
R3 = {('kekatos', '2026'): 'R3 (30 Oct): Crossref DOI registered; title, 8 authors, proceedings, pp. 129–142 match. Abstract read via OpenAlex (level A)',
      ('liu', '2026b'): '', ('ray', '2026'): 'R3 (30 Oct): OpenAlex record; 1 author; abstract read (level A); preprint',
      ('xin', '2026'): 'R3 (30 Oct): Crossref DOI registered; journal, vol 2(2), 1 author match. Abstract read via OpenAlex (level A)',
      ('yan', '2026'): 'R3 (30 Oct): OpenAlex record; 5 authors, 3 listed in the record (list abbreviated); abstract read (level A); preprint'}
rows = []; counts = {}
for e in refs:
    ent = e['entry']
    m = re.match(r'(.+?)\s\((\d{4})', ent)
    k = key(m.group(1), m.group(2))
    recs = list(dict.fromkeys(found.get(k, [])))
    if k in R3 and 'R3' in e['chapters']:
        recs = [R3[k]]
    if k == ('liu', '2026') and 'R3' in e['chapters']:
        recs = ['R3 (30 Oct): OpenAlex record; 1 author; abstract read (level A); preprint']
    if 'Withdrawn' in ent:
        recs.append('WITHDRAWN PREPRINT (withdrawal recorded 25 Sep 2026; not re-confirmable 28–30 Oct)')
    if 'Platt' in ent:
        recs.append('UNRESOLVED CITATION CONFLICT (OI-07 / D-13): Crossref registers the 2000 chapter "Probabilities for SV machines"')
    if 'Kull' in ent:
        recs.append('Disambiguation pending (D-13): AISTATS 2017 entry not re-confirmed; a different 2017 Kull et al. paper exists')
    status = ('NO INDIVIDUAL RECORD FOUND — REQUIRES SOURCE VERIFICATION' if not recs else
              'CONFLICT / WITHDRAWN' if any(t in ' '.join(recs) for t in ('CONFLICT', 'WITHDRAWN')) else
              'PARTIAL' if any(t in ' '.join(recs) for t in ('PARTLY', 'PARTIALLY', 'EXISTS', 'not re-confirmed', 'NOT RE-CONFIRMED', 'pending')) else 'RECORDED')
    counts[status] = counts.get(status, 0) + 1
    typ = ('Withdrawn preprint' if 'Withdrawn' in ent else 'Official source' if 'Official source' in ent or 'OWASP' in ent or 'Regulation (EU)' in ent else
           'Preprint' if 'Preprint' in ent or 'arXiv:' in ent else 'Working paper' if 'Working paper' in ent else 'Peer-reviewed / book')
    rows.append((ent, typ, ', '.join(e['chapters']), status, ' | '.join(recs) if recs else '—'))
out = ['# REFERENCES — VERIFICATION STATUS', '',
       '**Date:** 30 October 2026. One row per entry of the consolidated reference list (`chapters/REFERENCES.md`).',
       '', '**What the statuses mean.**',
       '- **RECORDED:** a verification record exists for the entry (metadata confirmed against Crossref or an OpenAlex record, and, for review studies, the claims used checked against the abstract or record). **No entry is verified against its full text**: full texts were unreachable in every session (network policy).',
       '- **PARTIAL:** the record leaves at least one detail unconfirmed (see the record column).',
       '- **CONFLICT / WITHDRAWN:** an unresolved citation conflict or a withdrawn preprint.',
       '- **NO INDIVIDUAL RECORD FOUND:** the matcher found no per-entry record. Such entries are listed for checking; they are not asserted to be wrong.',
       '', '| Status | Entries |', '|---|---:|'] + [f'| {k} | {v} |' for k, v in sorted(counts.items())] + ['', '| # | Reference | Type | Chapters | Status | Verification record |', '|---|---|---|---|---|---|']
for i, (ent, typ, ch, st, rec) in enumerate(rows, 1):
    out.append(f'| {i} | {ent.replace("|", "/")} | {typ} | {ch} | {st} | {rec.replace("|", "/") if rec != "—" else rec} |')
open(os.path.join(ROOT, 'REM_FINAL_THESIS/REFERENCES_VERIFIED.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(counts)
for r in rows:
    if r[3].startswith('NO'): print('  NO RECORD:', r[0][:120])
