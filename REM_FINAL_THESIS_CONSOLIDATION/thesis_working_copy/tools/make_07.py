"""Write REM_FINAL_THESIS_CONSOLIDATION/07_THESIS_READY_REPLACEMENT_TEXT.md from audit/edit_log.json.

usage (from the repository root, after make_working_copy.py):
    python3 REM_FINAL_THESIS_CONSOLIDATION/thesis_working_copy/tools/make_07.py
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
WC = os.path.abspath(os.path.join(HERE, '..'))
OUT = os.path.join(WC, '..', '07_THESIS_READY_REPLACEMENT_TEXT.md')
LOG = json.load(open(os.path.join(WC, 'audit', 'edit_log.json'), encoding='utf-8'))['edits']

CH = {'CHAPTER_01_FINAL': 'Chapter 1', 'CHAPTER_02_FINAL': 'Chapter 2', 'CHAPTER_03_FINAL': 'Chapter 3',
      'CHAPTER_04_FINAL': 'Chapter 4', 'CHAPTER_05_FINAL': 'Chapter 5', 'APPENDICES_FINAL': 'Appendices',
      'abstract_en': 'Abstract (English)', 'abstract_ar': 'Abstract (Arabic)'}


def why(eid):
    rules = [
        ('M1', 'Reconciliation 03, merge item M1: the peer-reviewed layered precedent must be listed; the "not found" statement is qualified by the substitution study', 'No (adds a precedent; narrows a claim)', 'Demirol & Aydoğan (2026); Abasıkeleş Turgut & Gümüş (2026b)'),
        ('R4-9', 'Reconciliation 04, R4-9: the inserted DiD interpretation rested on oracle or broad authorization', 'Yes: corrects an overclaim (residual coverage, not deployable defense in depth)', '—'),
        ('R1-1', 'Reconciliation 04, R1-1: states the problem as whether layering yields defense in depth (the researcher\'s topic) [PD]', 'Framing only; no result changes', '—'),
        ('R1-2', 'Reconciliation 04, R1-2: NEXUS publication status and reading levels', 'No (accuracy of status)', 'Hossain et al. (2026)'),
        ('R1-3', 'Reconciliation 04, R1-3: proposed evaluation focus, kept separate from the objective-derived aim [PD]', 'Framing only', '—'),
        ('R1-5', 'Reconciliation 04, R1-5: primary empirical contribution (05 A)', 'States the contribution precisely; no new result', '—'),
        ('R1-6', 'Reconciliation 04, R1-6: "accounts for all 661" and "every outcome effect" are overclaims; adds the P1 withhold-all identity', 'Yes: corrects overclaims', '—'),
        ('R4-', 'Reconciliation 04 (R4-1 to R4-8): component-level wording, data history, joint production of protection', 'Yes: corrects overclaims; no number changes', '—'),
        ('C-GAP', 'Final research gap (04): narrowed after the abstract-level evidence of Saleem et al., Spotlight-Guard, NEXUS and BARBICAN [PD]', 'Yes: narrows the gap statement', 'Saleem et al. (2026); Demirol & Aydoğan (2026); Hossain et al. (2026); Abasıkeleş Turgut & Gümüş (2026b)'),
        ('C-NEG1', 'Qualifies a negative result with the exploratory suppression result', 'Qualifies a claim', '—'),
        ('A2-ch1', 'A2 (review 05): REM does not authorize; layer count is not evidence of depth', 'No (documentation)', '—'),
        ('A7', 'A7 and review 08-A: related work on layered defenses and on how layers are evaluated', 'No (documentation; narrows the gap)', 'Alzahrani (2026); Saleem et al. (2026); Jang et al. (2027); Demirol & Aydoğan (2026); Hossain et al. (2026); T. Shi et al. (2026); Sequeira et al. (2026); Zhu, Yang, et al. (2025); Debenedetti et al. (2025); Gong et al. (2026); Abasıkeleş-Turgut & Gümüş (2026a, 2026b)'),
        ('A3-ch4', 'A3 (review 05): documents the existing gateway and its deployment simulation', 'No (documents existing evidence)', '`results/deployment_sim/2026-11-05_full/RESULTS.md`'),
        ('A1', 'A1 (review 05): where the trust boundary acts', 'No (documentation)', 'Saleem et al. (2026); Debenedetti et al. (2025)'),
        ('A2', 'A2 (review 05): detection, decision and authorization separated', 'No (documentation)', 'T. Shi et al. (2026); Debenedetti et al. (2025); Hossain et al. (2026); Gong et al. (2026)'),
        ('A3', 'A3 (review 05): enforcement point (gateway)', 'No (documentation)', '`rem/deployment/gateway.py`'),
        ('A4', 'A4 (review 05): dependencies and complementarity of the evidence families', 'No (documentation)', '—'),
        ('A5', 'A5 (review 05): implemented vs conceptual controls', 'No (documentation)', '—'),
        ('A6', 'A6 (review 05): reporting conventions', 'No (documentation)', 'Abasıkeleş-Turgut & Gümüş (2026a)'),
        ('T', '"Pre-registered" overstates what the record supports (protocols committed before scoring; no formal pre-registration)', 'Yes: removes an overstatement; no result changes', '—'),
        ('C5-', 'Chapter 5 consistency with the corrected Chapter 4 (reconciliation 03, consequential edits)', 'Yes: corrects overclaims', '—'),
        ('FW', 'Future work B2, B5 and B7 of review 05 (not implemented)', 'No', 'Abasıkeleş Turgut & Gümüş (2026b)'),
        ('AB-', 'Abstract consistency with the corrected Chapters 1 and 4', 'Yes: corrects overclaims', '—'),
    ]
    for p, r, m, c in rules:
        if eid.startswith(p):
            return r, m, c
    return '', '', ''


def section(name, new):
    if name.startswith('abstract'):
        return 'Abstract'
    p = os.path.join(WC, 'src', name + '.md')
    t = open(p, encoding='utf-8').read()
    i = t.find(new[:200])
    first = new.strip().split('\n')[0]
    if first.startswith('#'):
        return first.lstrip('#').strip() + ' (new)'
    heads = [m for m in re.finditer(r'^(#{1,5}) (.+)$', t[:max(i, 0)], re.M)]
    return heads[-1].group(2).strip() if heads else '(chapter opening)'


L = []
w = L.append
w('# 07: Thesis-ready replacement and insertion text\n')
w('**Base text.** The humanized edition (`REM_HUMANIZED_THESIS/src`, unchanged). The DiD insertions are merged by context (§1.1).')
w('')
w('**How this file relates to the working copy.**')
w('- §1 lists **exactly** what `thesis_working_copy/tools/make_working_copy.py` applied. It is generated from `audit/edit_log.json` by `make_07.py`.')
w('- Each entry gives the location, the existing anchor and the complete new text.')
w('- §2 holds text that is **not applied** because it needs a supervisor decision first.')
w('- Numbers are unchanged; the working copy re-verifies 498 Chapter 4 table cells with 0 mismatches.')
w('')
w('## 1. Applied in the working copy\n')
w('### 1.1 DiD-edition insertions (merged unchanged; reconciliation 03, M1–M4)\n')
w('| Edit | Location | Source text |')
w('|---|---|---|')
src = {'M-02-1': 'Ch. 2 new §2.11.6 and Table 2.6: `REM_DID_THESIS_EDITION/src/CHAPTER_02_FINAL.md` lines 559–585',
       'M-03-1': 'Ch. 3 new §3.15 (REM-DiD, proposed, not adopted), Table 3.16, Figure 3.5; the summary becomes §3.16: DiD Ch. 3 lines 912–947',
       'M-04-1': 'Ch. 4 new §4.6.12 (exploratory DiD evaluation), Tables 4.60–4.61; the summary becomes §4.6.13: DiD Ch. 4 lines 2033–2106',
       'M-05-1': 'Ch. 5 §5.5, paragraph "Not confirmed: resilient Defense-in-Depth": DiD Ch. 5 lines 89–90',
       'M-05-2': 'Ch. 5 §5.7, Future Work item 14: DiD Ch. 5 line 123'}
for e in LOG:
    if e['id'] in src:
        w(f"| `{e['id']}` | {src[e['id']].split(':')[0]} | {src[e['id']].split(':', 1)[1].strip()} |")
w('')
w('Two edits then qualify the inserted text (`M1a`, `M1b`, `R4-9a`, `R4-9b`, below).\n')
w('### 1.2 Edits\n')
for e in LOG:
    if e['id'].startswith('M-') or e['id'] == 'REF+':
        continue
    reason, meaning, refs = why(e['id'])
    sec = section(e['file'], e['new'][len(e['old']):] if e['kind'] == 'insert_after' else e['new'])
    w(f"#### `{e['id']}` · {CH.get(e['file'], e['file'])} · {sec}\n")
    w(f"- **Kind:** {e['kind'].replace('_', ' ')}")
    old = e['old'] if e['kind'] == 'replace' else e['old'][:300]
    anchor = old if len(old) <= 400 else old[:400] + ' […]'
    w(f"- **Existing text or anchor:** «{anchor.strip()}»")
    w(f"- **Reason:** {reason}")
    w(f"- **Changes scientific meaning?** {meaning}")
    w(f"- **References:** {refs}")
    w('- **New text:**\n')
    if e['kind'] == 'insert_after':
        new = e['new'][len(e['old']):].strip()
    elif e['kind'] == 'insert_before':
        new = e['new'][:len(e['new']) - len(e['old'])].strip()
    else:
        new = e['new'].strip()
    for line in new.split('\n'):
        w('> ' + line if line.strip() else '>')
    w('')
w('### 1.3 References added\n')
for e in LOG:
    if e['id'] == 'REF+':
        w(f"- {e['entry']}…")
w('\nFull entries: `thesis_working_copy/references/REFERENCES_FINAL.md`; verification in 09.\n')
w(open(os.path.join(HERE, '07_gated_section.md'), encoding='utf-8').read())
open(OUT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('wrote', OUT, len(L), 'lines')
