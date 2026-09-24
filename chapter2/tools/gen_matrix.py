from sources import S
from collections import Counter
def esc(x): return str(x).replace('|','\\|')
L=[]
L.append("# Chapter 2: Reference Evidence Matrix\n")
L.append("**Purpose.** This matrix is the evidence-control record for every source retained in `CHAPTER2_LITERATURE_REVIEW_INTEGRATED.md`. Each row records what the source contributes to Chapter 2 and how it was verified.\n")
L.append("**Verification labels.**\n")
L.append("- **FULLY VERIFIED:** identity, authors, year, title and venue confirmed, and the specific claim or number used in Chapter 2 confirmed against the primary source's abstract, a proceedings page or a retrieved passage.")
L.append("- **PARTIALLY VERIFIED:** identity confirmed, but at least one detail used in Chapter 2 was not re-confirmed against the primary source in the September 2026 pass. The chapter text flags these details.")
L.append("- **SOURCE NOT FULLY VERIFIED:** no retained source has this status. Such sources were removed; see the change log.\n")
L.append("**Cell labels.** `NOT REPORTED` means the source does not report the capability. `NOT APPLICABLE` means the capability does not apply to this kind of source. `NOT VERIFIED` means it was described in an earlier draft but not confirmed against the primary source.\n")
L.append("**Origin codes.** B = in both earlier drafts (v2.0 and September DOCX); E = v2.0 only; D = DOCX only; N = newly added in this merge.\n")
c=Counter(s['origin'] for s in S); v=Counter('PARTIAL' if s['verif'].startswith('PARTIALLY') else 'FULL' for s in S)
typ=Counter()
for s in S:
    t=s['type']
    if 'OFFICIAL' in t: typ['Official source']+=1
    elif 'Withdrawn' in t: typ['Withdrawn preprint']+=1
    elif 'Working paper' in t: typ['Working paper']+=1
    elif t.startswith('Preprint') or 'Preprint' in t: typ['Preprint']+=1
    elif 'Book' in t: typ['Book / book chapter']+=1
    else: typ['Peer-reviewed']+=1
L.append("## Summary\n")
L.append("| Measure | Count |\n|---|---:|")
L.append(f"| Retained sources (total) | {len(S)} |")
L.append(f"| Academic sources (excluding 2 official sources) | {len(S)-typ['Official source']} |")
for k in ['Peer-reviewed','Book / book chapter','Preprint','Working paper','Withdrawn preprint','Official source']:
    L.append(f"| {k} | {typ[k]} |")
L.append(f"| FULLY VERIFIED | {v['FULL']} |")
L.append(f"| PARTIALLY VERIFIED | {v['PARTIAL']} |")
L.append(f"| Origin: both earlier drafts (B) | {c['B']} |")
L.append(f"| Origin: v2.0 only (E) | {c['E']} |")
L.append(f"| Origin: DOCX only (D) | {c['D']} |")
L.append(f"| Origin: new in this merge (N) | {c['N']} |")
L.append("")
L.append("## Part A: Evidence matrix\n")
L.append("| ID | Paper | Year | Threat | Defense | Runtime | Behavior | Tool Use | Multi-Step | Mitigation | Financial | Key Result | Limitation | Verification |")
L.append("|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|")
for s in S:
    L.append("| "+" | ".join(esc(x) for x in [s['id'],s['cite']+" — "+s['title'],s['year'],s['threat'],s['defense'],s['runtime'],s['behavior'],s['tool'],s['multi'],s['mit'],s['fin'],s['key'],s['lim'],s['verif']])+" |")
L.append("\n## Part B: Source register (bibliographic identity and purpose)\n")
L.append("Each row answers the retention question: *what exact sentence, table entry, algorithm, result or argument in Chapter 2 does this source support?*\n")
L.append("| ID | Authors | Venue / source | Identifier | Source type | Origin | Chapter 2 sections | Exact contribution used in Chapter 2 |")
L.append("|---|---|---|---|---|---|---|---|")
for s in S:
    L.append("| "+" | ".join(esc(x) for x in [s['id'],s['authors'],s['venue'],s['ident'],s['type'],s['origin'],s['sec'],s['use']])+" |")
open('/home/user/Ram/chapter2/CHAPTER2_REFERENCE_EVIDENCE_MATRIX.md','w').write("\n".join(L)+"\n")
print(len(S),c,v,typ)
