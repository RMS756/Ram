"""Revised PRISMA 2020 flow diagram for Chapter 2 (R2).

Counts are read from chapter2/slr/prisma_counts.json, which build_slr.py
computes from the stored search output and the screening log. The revision
changes labels only: it separates records, reports and studies, and shows that
full-text reports were sought but not retrieved, so eligibility was assessed
on records.
"""

import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
c = json.load(open(os.path.join(ROOT, "chapter2", "slr", "prisma_counts.json"), encoding="utf-8"))
INK, INK2, EDGE, FILL, GREY = "#0b0b0b", "#52514e", "#2a78d6", "#eef4fc", "#f4f3f0"

fig, ax = plt.subplots(figsize=(9.2, 10.4))
ax.set_xlim(0, 100), ax.set_ylim(0, 112), ax.axis("off")


def box(x, y, w, h, text, fill=FILL, edge=EDGE, size=7.4):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=0.8", fc=fill, ec=edge, lw=1.1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, color=INK, wrap=True, linespacing=1.3)


def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1))


for y, lab in ((95, "Identification"), (62, "Screening"), (10, "Included")):
    ax.text(1, y, lab, rotation=90, va="center", fontsize=8.5, weight="bold", color=INK2)

ax.text(50, 110, "Identification of studies via databases", ha="center", fontsize=8.5, weight="bold", color=INK)
ax.text(86, 110, "Via other methods", ha="center", fontsize=8.5, weight="bold", color=INK)
box(5, 96, 34, 11, f"Records identified from OpenAlex\n(11 queries, 13 result pages,\n25 Sep 2026): n = {c['db_records_identified']}")
box(45, 96, 25, 11, f"Duplicate records removed\nbefore screening:\nn = {c['db_duplicates_removed']}", fill=GREY, edge=INK2)
box(74, 96, 25, 11, f"Records identified from the\nprevious chapter's reference\nlist: n = {c['om_records_identified']}")
arrow(39, 101.5, 45, 101.5)

box(5, 79, 34, 9, f"Records screened\n(title and abstract): n = {c['db_records_screened']}")
box(45, 79, 25, 9, f"Records excluded:\nn = {c['db_ta_excluded']}", fill=GREY, edge=INK2)
arrow(22, 96, 22, 88), arrow(39, 83.5, 45, 83.5)
box(74, 79, 25, 9, f"Same study as a database\nrecord: n = {c['om_cross_stream_duplicates']}", fill=GREY, edge=INK2)
arrow(86.5, 96, 86.5, 88)

box(5, 63, 34, 9, f"Reports sought for retrieval\n(full text): n = {c['db_reports_sought']}")
box(45, 63, 25, 9, f"Reports not retrieved\n(network policy):\nn = {c['db_reports_fulltext_not_retrieved']}", fill="#fdf1ec", edge="#eb6834")
arrow(22, 79, 22, 72), arrow(39, 67.5, 45, 67.5)
box(74, 63, 25, 9, f"Reports sought: n = {c['om_records_assessed']}\nNot retrieved: n = {c['om_fulltext_not_retrieved']}",
    fill="#fdf1ec", edge="#eb6834")
arrow(86.5, 79, 86.5, 72)

box(5, 43, 34, 13, f"Records assessed for eligibility\nat RECORD LEVEL (title, abstract,\nmetadata; no full-text report):\nn = {c['db_reports_assessed_record_level']}")
fr = c["db_ft_exclusion_reasons"]
box(45, 41, 25, 17, "Records excluded at eligibility:\n" + "\n".join(f"{k}: {v}" for k, v in fr.items()), fill=GREY, edge=INK2, size=6.5)
arrow(22, 63, 22, 56), arrow(39, 49.5, 45, 49.5)
box(74, 41, 25, 17, f"Records assessed at record\nlevel: n = {c['om_records_assessed']}\nExcluded: n = "
    f"{c['om_background'] + c['om_foundational'] + c['om_excluded_withdrawn']}\n(background {c['om_background']}, "
    f"foundational /\nmethodological {c['om_foundational']},\nwithdrawn {c['om_excluded_withdrawn']})", fill=GREY, edge=INK2, size=6.5)
arrow(86.5, 63, 86.5, 58)

box(5, 4, 94, 22, f"Studies included in the synthesis: n = {c['total_included_studies']} "
    f"({c['db_included']} via databases + {c['om_included']} via other methods)\n"
    "Each included study is represented by its index record (no full-text report was available).\n\n"
    "Eligibility, appraisal and extraction rest on records (title, abstract, index and Crossref metadata).\n"
    "No full-text screening was performed. A peer-reviewed report of one included study (ProvenanceGuard,\n"
    "ASE 2026) was identified on 28 Oct 2026, after the search date, and is cited but not counted.", size=7.2)
arrow(22, 43, 22, 26), arrow(86.5, 41, 86.5, 26)
fig.tight_layout()
out = os.path.join(ROOT, "revision_R2", "figures", "fig2_1_prisma_r2.png")
fig.savefig(out, dpi=180)
print(out)
