# -*- coding: utf-8 -*-
"""Build the Chapter 2 systematic-review artefacts from recorded data.

Inputs : ../raw_search/*.json (search output as returned on 2026-09-25),
         ../dedup_records.json, slr_data.py, ../../tools/sources.py
Outputs: ../../CHAPTER2_SCREENING_LOG.csv
         ../../CHAPTER2_SYSTEMATIC_EVIDENCE_MATRIX.csv
         ../../CHAPTER2_PRISMA_FLOW_DIAGRAM.png
         ../prisma_counts.json, ../quality_table.md, ../included_register.csv
Every count is computed here; none is typed by hand.
"""
import csv, json, os, re, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SLR = os.path.dirname(HERE)
CH2 = os.path.dirname(SLR)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(CH2, "tools"))
import slr_data as D          # noqa: E402
import sources as SRC         # noqa: E402

QUERY_FILES = ["Q1", "Q1p2", "Q2", "Q2p2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11"]


def norm(t):
    return re.sub(r"[^a-z0-9]", "", t.lower())[:80]


# ---------------------------------------------------------------- dedup (recomputed)
hits, recs, order = [], {}, []
meta = []
for q in QUERY_FILES:
    blob = json.load(open(os.path.join(SLR, "raw_search", q + ".json")))
    t = json.loads(blob[0]["text"])
    meta.append(dict(file=q, total_estimate=t["total_estimate"], page=t["page"], returned=len(t["results"]),
                     query_used=t.get("query_used", {}).get("openalex_lane")))
    for rank, r in enumerate(t["results"], 1):
        key = (r.get("doi") or "").lower() or r["id"]
        tk = norm(r["title"])
        k = next((kk for kk, v in recs.items() if kk == key or v["tkey"] == tk), None)
        if k is None:
            recs[key] = dict(r, tkey=tk, queries=[q])
            order.append(key)
            hits.append((q, rank, r, None))
        else:
            recs[k]["queries"].append(q)
            hits.append((q, rank, r, k))
R = [recs[k] for k in order]
rnum = {k: i + 1 for i, k in enumerate(order)}
stored = json.load(open(os.path.join(SLR, "dedup_records.json")))
assert [s["title"] for s in stored] == [r["title"] for r in R], "dedup order changed"


def cit_db(r):
    a = r.get("authors") or ["(no author)"]
    first = a[0]
    more = " et al." if (r.get("author_count") or len(a)) > 1 else ""
    ven = (r.get("venue") or {}).get("name") or r.get("type", "")
    doi = r.get("doi") or ""
    return f"{first}{more} ({r.get('year')}). {r['title']}. {ven}. {('doi:' + doi) if doi else r['id']}"


# ---------------------------------------------------------------- screening log
rows = []
n_dupe_hits = 0
for q, rank, r, dupof in hits:
    if dupof is not None:
        n_dupe_hits += 1
        rows.append([f"{q}#{rank:02d}", cit_db(r), f"OpenAlex (FastTrack MCP) — {q}", f"Yes (duplicate of R{rnum[dupof]:03d})",
                     "Not screened (duplicate removed before screening)", "Not assessed", "duplicate", "Removed before screening"])
for i, r in enumerate(R, 1):
    ta, ft, reason, final, pid = D.DB.get(i, ("Exclude", "Not assessed", D.DEFAULT_TA_REASON, "Excluded", ""))
    if pid:
        final = f"Included ({pid})"
    rows.append([f"R{i:03d}", cit_db(r), "OpenAlex (FastTrack MCP) — " + ", ".join(r["queries"]), "No",
                 ta, ft, reason, final])

S = {s["id"]: s for s in SRC.S}
om_counts = Counter()
for sid in sorted(S):
    s = S[sid]
    cit = f"{s['cite']}. {s['title']}. {s['venue']}. {s['ident']}"
    src = "Other methods — previous integrated Chapter 2 reference list (known-item and citation checking)"
    if sid in D.OM_CROSS_DUP:
        rn = D.OM_CROSS_DUP[sid]
        rows.append([sid, cit, src, f"Yes (same study as database record R{rn:03d})", "Not screened (cross-stream duplicate)",
                     "Not assessed", "duplicate", f"Assessed via R{rn:03d}"])
        om_counts["cross_dup"] += 1
    elif sid in D.OM_INCLUDED:
        rows.append([sid, cit, src, "No", "Include", "Include", "", f"Included ({D.OM_INCLUDED[sid]})"])
        om_counts["included"] += 1
    elif sid in D.OM_BACKGROUND:
        rows.append([sid, cit, src, "No", "Exclude", "Not assessed", D.OM_BACKGROUND[sid], "Background source (not an included study)"])
        om_counts["background"] += 1
    elif sid in D.OM_FOUNDATIONAL:
        lab = "FOUNDATIONAL SOURCE" if s["year"] < 2019 else "METHODOLOGICAL SOURCE (within period, not agent-specific)"
        rows.append([sid, cit, src, "No", "Include (criterion I6: foundational/methodological)", "Include", "", lab])
        om_counts["foundational"] += 1
    elif sid in D.OM_EXCLUDED:
        rows.append([sid, cit, src, "No", "Include", "Exclude", D.OM_EXCLUDED[sid], "Excluded (discussed historically only)"])
        om_counts["excluded_ft"] += 1
    else:
        raise SystemExit(f"unclassified other-methods source {sid}")

with open(os.path.join(CH2, "CHAPTER2_SCREENING_LOG.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["ID", "Citation", "Database", "Duplicate?", "Title/Abstract Decision", "Full-Text Decision", "Exclusion Reason", "Final Status"])
    w.writerows(rows)

# ---------------------------------------------------------------- counts
db_ta = Counter(D.DB.get(i, ("Exclude",))[0] for i in range(1, len(R) + 1))
db_ft = Counter(v[1] for v in D.DB.values() if v[0] == "Include")
ft_ex_reasons = Counter(v[2].split(" (")[0] for v in D.DB.values() if v[0] == "Include" and v[1] == "Exclude")
def rkey(x):
    return "outside scope (multi-agent channel)" if x.startswith("outside scope (multi-agent") else x.split(" (")[0]


ta_ex_reasons = Counter(rkey((D.DB.get(i) or ("", "", D.DEFAULT_TA_REASON))[2])
                        for i in range(1, len(R) + 1) if D.DB.get(i, ("Exclude",))[0] == "Exclude")
included = D.STUDIES
inc_db = [s for s in included if s["src"].startswith("R")]
inc_om = [s for s in included if s["src"].startswith("S")]
assert len(inc_db) == db_ft["Include"], (len(inc_db), db_ft)
assert len(inc_om) == om_counts["included"]

counts = dict(
    search_date="2026-09-25",
    databases_searched=["OpenAlex (via FastTrack Literature MCP search_papers)"],
    query_pages=len(meta), query_meta=meta,
    db_records_identified=len(hits), db_duplicates_removed=n_dupe_hits, db_records_screened=len(R),
    db_ta_excluded=db_ta["Exclude"], db_ta_included=db_ta["Include"], db_ta_exclusion_reasons=dict(ta_ex_reasons),
    db_reports_sought=db_ta["Include"], db_reports_fulltext_not_retrieved=db_ta["Include"],
    db_reports_assessed_record_level=db_ta["Include"], db_ft_excluded=db_ft["Exclude"],
    db_ft_exclusion_reasons=dict(ft_ex_reasons), db_included=len(inc_db),
    om_records_identified=len(S), om_cross_stream_duplicates=om_counts["cross_dup"],
    om_records_assessed=len(S) - om_counts["cross_dup"], om_background=om_counts["background"],
    om_foundational=om_counts["foundational"], om_excluded_withdrawn=om_counts["excluded_ft"],
    om_included=len(inc_om), om_fulltext_not_retrieved=len(S) - om_counts["cross_dup"],
    total_included_studies=len(included),
    db_background=sum(1 for v in D.DB.values() if v[3].startswith("Background")),
)


# ---------------------------------------------------------------- appraisal
def category(s):
    q = s["q"].split()
    Q = {i + 1: q[i] for i in range(10)}
    if s.get("override"):
        return s["override"], "override: " + s["override_reason"]
    if Q[10] == "Y" and Q[9] == "Y" and Q[5] == "Y" and Q[7] in ("Y", "NA"):
        return "HIGH EVIDENCE", "peer-reviewed; benchmark/dataset reported; quantitative results reported; comparator reported or not applicable"
    if (Q[9] == "Y" and Q[10] in ("Y", "P")) or (Q[10] == "Y" and Q[5] == "Y"):
        return "MODERATE EVIDENCE", "quantitative results in a peer-reviewed or clearly labelled preprint record, or peer-reviewed evaluation without verifiable figures"
    return "LIMITED EVIDENCE", "no verifiable quantitative evaluation in the accessible record, or design/position/working paper"


for s in included:
    s["level"], s["level_basis"] = category(s)

cat = Counter(s["level"] for s in included)
peer = Counter("Peer-reviewed" if s["q"].split()[9] == "Y" else "Preprint/working paper" for s in included)
ver = Counter(("PARTIALLY VERIFIED" if s["verif"].startswith("PARTIALLY") else "FULLY VERIFIED") for s in included)
roles = Counter(s["role"] for s in included)
fin_yes = [s["id"] for s in included if str(s["fin"]).startswith("Yes")]
counts.update(evidence_levels=dict(cat), peer_review=dict(peer), verification=dict(ver), roles=dict(roles),
              financial_context_yes=fin_yes)
json.dump(counts, open(os.path.join(SLR, "prisma_counts.json"), "w"), indent=1)

# ---------------------------------------------------------------- evidence matrix
cols = ["ID", "Study", "Year", "Venue", "Agent Type", "Threat", "Attack Entry", "Runtime?", "Context", "Behavioral",
        "Tool/Action", "Multi-Step", "Provenance", "Decision", "Mitigation", "Benchmark", "Financial Context", "Metrics",
        "Main Result", "Limitation", "Evidence Level"]
with open(os.path.join(CH2, "CHAPTER2_SYSTEMATIC_EVIDENCE_MATRIX.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(cols)
    for s in included:
        w.writerow([s["id"], f"{s['cite']} — {s['title']}", s["year"], s["venue"], s["agent"], s["threat"], s["entry"],
                    s["runtime"], s["context"], s["behav"], s["tool"], s["multi"], s["prov"], s["dec"], s["mit"],
                    s["bench"], s["fin"], s["metrics"], s["result"], s["limit"], s["level"]])

with open(os.path.join(SLR, "included_register.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["ID", "Source record", "Study", "Role", "Observation unit", "Verification", "Q1-Q10", "Evidence level", "Basis"])
    for s in included:
        w.writerow([s["id"], s["src"], s["cite"], s["role"], s["obs"], s["verif"], s["q"], s["level"], s["level_basis"]])

# quality table (markdown fragment used by CHAPTER2_QUALITY_APPRAISAL.md)
lines = ["| ID | Study | Role | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 | Verification | Evidence level |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for s in included:
    q = s["q"].split()
    lines.append(f"| {s['id']} | {s['cite']} | {s['role']} | " + " | ".join(q) + f" | {s['verif']} | {s['level']} |")
open(os.path.join(SLR, "quality_table.md"), "w").write("\n".join(lines) + "\n")

# ---------------------------------------------------------------- PRISMA flow diagram
import matplotlib                      # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt        # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

c = counts
fig, ax = plt.subplots(figsize=(15, 13.5))
ax.set_xlim(0, 150); ax.set_ylim(0, 135); ax.axis("off")


def box(x, y, w, h, text, fc="#ffffff", fs=8.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0", fc=fc, ec="black", lw=1))
    ax.text(x + 1.2, y + h - 1.2, text, va="top", ha="left", fontsize=fs, wrap=True, family="DejaVu Sans")


def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", lw=1, color="black"))


ax.text(75, 133, "PRISMA 2020 flow diagram — Chapter 2 systematic review (search date 25 September 2026)",
        ha="center", va="top", fontsize=11, weight="bold")
ax.add_patch(FancyBboxPatch((2, 118), 96, 7, boxstyle="square,pad=0", fc="#fde9b8", ec="black"))
ax.text(50, 121.5, "Identification of studies via databases and registers", ha="center", va="center", fontsize=9.5, weight="bold")
ax.add_patch(FancyBboxPatch((101, 118), 47, 7, boxstyle="square,pad=0", fc="#d9d9d9", ec="black"))
ax.text(124.5, 121.5, "Identification of studies via other methods", ha="center", va="center", fontsize=9.5, weight="bold")

box(4, 96, 44, 20, f"Records identified from:\n  Databases (n = 1): OpenAlex, via\n  FastTrack MCP search_papers\n  11 queries, 13 result pages\n  (n = {c['db_records_identified']} records)\nRegisters (n = 0)")
box(52, 96, 44, 20, "Records removed before screening:\n"
    f"  Duplicate records removed\n  (n = {c['db_duplicates_removed']})\n  Records marked ineligible by\n  automation tools (n = 0)\n  Records removed for other\n  reasons (n = 0)")
arrow(48, 106, 52, 106)
box(4, 79, 44, 13, f"Records screened (title/abstract)\n(n = {c['db_records_screened']})")
box(52, 72, 44, 20, f"Records excluded (n = {c['db_ta_excluded']})\n" + "\n".join(
    f"  {k}: {v}" for k, v in sorted(c['db_ta_exclusion_reasons'].items(), key=lambda x: -x[1])), fs=7.6)
arrow(26, 96, 26, 92); arrow(48, 85, 52, 85)
box(4, 60, 44, 13, f"Reports sought for retrieval\n(n = {c['db_reports_sought']})")
box(52, 58, 44, 11, f"Reports not retrieved as full text\n(n = {c['db_reports_fulltext_not_retrieved']}; network policy) — all\nassessed on record-level evidence instead", fs=7.8)
arrow(26, 79, 26, 73); arrow(48, 66, 52, 64)
box(4, 40, 44, 15, f"Reports assessed for eligibility\n(record level: title, abstract,\nindexed metadata; search-engine\nabstract where index lacked one)\n(n = {c['db_reports_assessed_record_level']})", fs=8)
box(52, 36, 44, 18, f"Reports excluded (n = {c['db_ft_excluded']}):\n" + "\n".join(
    f"  {k}: {v}" for k, v in c['db_ft_exclusion_reasons'].items()), fs=7.4)
arrow(26, 60, 26, 55); arrow(48, 47, 52, 45)

box(103, 96, 43, 20, f"Records identified from:\n  Previous integrated Chapter 2\n  reference list (known-item and\n  citation checking, 16–25 Sep 2026)\n  (n = {c['om_records_identified']})\n  Same study as a database record\n  (n = {c['om_cross_stream_duplicates']})")
box(103, 60, 43, 30, f"Reports assessed for eligibility\n(n = {c['om_records_assessed']}; full text not\nretrieved; prior verification record)\n\nNot included as studies:\n  background sources: {c['om_background']}\n  foundational/methodological: {c['om_foundational']}\n  withdrawn preprint: {c['om_excluded_withdrawn']}\nIncluded studies: {c['om_included']}", fs=8)
arrow(124.5, 96, 124.5, 90)

ax.add_patch(FancyBboxPatch((2, 4), 146, 26, boxstyle="square,pad=0", fc="#dbe8f5", ec="black"))
box(4, 6, 92, 22, f"Studies included in review (n = {c['total_included_studies']})\n"
    f"  via databases: {c['db_included']}; via other methods: {c['om_included']}\n"
    f"  peer-reviewed: {c['peer_review'].get('Peer-reviewed', 0)}; preprint/working paper: {c['peer_review'].get('Preprint/working paper', 0)}\n"
    f"  HIGH / MODERATE / LIMITED EVIDENCE: {c['evidence_levels'].get('HIGH EVIDENCE', 0)} / {c['evidence_levels'].get('MODERATE EVIDENCE', 0)} / {c['evidence_levels'].get('LIMITED EVIDENCE', 0)}\n"
    f"  Synthesis: qualitative/structured (no meta-analysis)", fc="#ffffff", fs=8.6)
box(100, 6, 46, 22, f"Additionally cited, not synthesised\nas included studies:\n  foundational/methodological\n  sources: {c['om_foundational']}\n  background sources: {c['om_background'] + c['db_background']}\n  (incl. {c['db_background']} database records excluded\n   as secondary studies)", fc="#ffffff", fs=8)
arrow(26, 40, 26, 28); arrow(124.5, 60, 110, 28)
ax.text(1, 1.5, "Other databases named in the protocol (IEEE Xplore, ACM DL, Scopus, Web of Science, ScienceDirect, SpringerLink, ACL Anthology, NeurIPS/PMLR, "
        "ICLR/OpenReview, USENIX, arXiv): DATABASE ACCESS UNAVAILABLE (connections refused by network policy, 2026-09-25).", fontsize=7.2, va="bottom")
plt.savefig(os.path.join(CH2, "CHAPTER2_PRISMA_FLOW_DIAGRAM.png"), dpi=160, bbox_inches="tight")
print(json.dumps({k: v for k, v in counts.items() if k != "query_meta"}, indent=1))
