#!/usr/bin/env bash
# Build the R2 revised chapters: per-chapter DOCX, full DOCX, and a LibreOffice PDF rendering of each DOCX
# (the PDF shows how Word-format files render; it is used for the formatting review).
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=revision_R2/build
mkdir -p "$OUT/render"
FMT=markdown+lists_without_preceding_blankline
CH=(CHAPTER1_INTRODUCTION_R2 CHAPTER2_LITERATURE_REVIEW_R2 CHAPTER3_METHODOLOGY_R2 CHAPTER4_IMPLEMENTATION_R2 CHAPTER5_RESULTS_R2 CHAPTER6_DISCUSSION_CONCLUSION_R2)
for c in "${CH[@]}"; do
  pandoc -f "$FMT" "revision_R2/chapters_md/$c.md" --resource-path=. -o "$OUT/$c.docx"
done
pandoc -f "$FMT" revision_R2/FRONT_MATTER_R2.md $(printf 'revision_R2/chapters_md/%s.md ' "${CH[@]}") --resource-path=. --toc --toc-depth=2 -o "$OUT/REM_THESIS_R2_FULL.docx"
for f in "$OUT"/*.docx; do soffice --headless --convert-to pdf --outdir "$OUT/render" "$f" >/dev/null 2>&1; done
ls -la "$OUT" "$OUT/render"
# Visually verifiable PDF of the full thesis (MathML equations rendered by Chromium).
pandoc -f "$FMT" revision_R2/FRONT_MATTER_R2.md $(printf 'revision_R2/chapters_md/%s.md ' "${CH[@]}") --resource-path=. --toc --toc-depth=2 \
  -s --mathml --embed-resources --css thesis/thesis.css --metadata lang=en -o "$OUT/REM_THESIS_R2_FULL.html"
node -e '
const { chromium } = require("playwright");
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  await p.goto("file://" + require("path").resolve(process.argv[1]), { waitUntil: "load" });
  await p.pdf({ path: process.argv[2], format: "A4", printBackground: true, displayHeaderFooter: true,
    headerTemplate: "<span></span>",
    footerTemplate: "<div style=\"font-size:8px;width:100%;text-align:center;\">REM thesis — revised draft R2 — <span class=pageNumber></span></div>",
    margin: { top: "22mm", bottom: "22mm", left: "28mm", right: "20mm" } });
  await b.close(); })();' "$OUT/REM_THESIS_R2_FULL.html" "$OUT/REM_THESIS_R2_FULL.pdf"
rm -f "$OUT/REM_THESIS_R2_FULL.html"
