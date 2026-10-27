#!/usr/bin/env bash
# Build per-chapter DOCX, the full-thesis DOCX, and the full-thesis PDF (HTML -> Chromium) from thesis/*.md.
# Provisional formatting: the university template was not available (BLOCKED — MISSING SOURCE).
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=thesis/build
mkdir -p "$OUT"
FMT=markdown+lists_without_preceding_blankline
CH=(thesis/CHAPTER1_INTRODUCTION.md thesis/CHAPTER2_LITERATURE_REVIEW.md thesis/CHAPTER3_METHODOLOGY.md
    thesis/CHAPTER4_IMPLEMENTATION.md thesis/CHAPTER5_RESULTS.md thesis/CHAPTER6_DISCUSSION_CONCLUSION.md)
for f in "${CH[@]}"; do
  pandoc -f "$FMT" "$f" --resource-path=. -o "$OUT/$(basename "${f%.md}").docx"
done
pandoc -f "$FMT" thesis/FRONT_MATTER.md "${CH[@]}" --resource-path=. --toc --toc-depth=2 -o "$OUT/REM_THESIS_FULL.docx"
pandoc -f "$FMT" thesis/FRONT_MATTER.md "${CH[@]}" --resource-path=. --toc --toc-depth=2 -s --embed-resources \
  --css thesis/thesis.css --metadata lang=en -o "$OUT/REM_THESIS_FULL.html"
node -e '
const { chromium } = require("playwright");
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto("file://" + require("path").resolve(process.argv[1]), { waitUntil: "load" });
  await p.pdf({ path: process.argv[2], format: "A4", printBackground: true, displayHeaderFooter: true,
    headerTemplate: "<span></span>",
    footerTemplate: "<div style=\"font-size:8px;width:100%;text-align:center;\">REM thesis — draft for supervisor review — <span class=pageNumber></span></div>",
    margin: { top: "22mm", bottom: "22mm", left: "28mm", right: "20mm" } });
  await b.close();
})();' "$OUT/REM_THESIS_FULL.html" "$OUT/REM_THESIS_FULL.pdf"
rm -f "$OUT/REM_THESIS_FULL.html"
ls -la "$OUT"
