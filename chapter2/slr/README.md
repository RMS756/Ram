# Chapter 2 systematic review: data and scripts

| Path | Content |
|---|---|
| `raw_search/Q*.json` | Output of every counted OpenAlex query, exactly as returned on 2026-09-25 (FastTrack Literature MCP `search_papers`) |
| `raw_search/search_call_log.tsv` | UTC timestamp and exact parameters of every search call, including the Elicit attempts and the uncounted pilot probe |
| `raw_search/database_access_test_2026-09-25.txt` | Proxy log showing that direct connections to the named digital libraries were refused |
| `dedup_records.json` | The 219 unique records after deduplication, numbered R001–R219 in order of first appearance |
| `search_meta.json` | Per-query index estimate and number of records returned |
| `tools/slr_data.py` | Screening decisions, the other-methods classification, and extraction and appraisal data for the 71 included studies |
| `tools/build_slr.py` | Recomputes deduplication and all counts. Writes the screening log, the evidence matrix, the PRISMA diagram, `prisma_counts.json`, `included_register.csv` and `quality_table.md` |

**To rebuild:**

```
cd chapter2/slr/tools && python3 build_slr.py
```

This requires `matplotlib`.
