# Chapter 2: Systematic Search Strategy (PRISMA 2020 / PRISMA-S record)

**Final search date:** 25 September 2026. All counted searches were executed between 17:53 and 17:57 UTC that day (timestamps in `slr/raw_search/search_call_log.tsv`).
**Reviewer:** single reviewer (the thesis author, assisted by Claude Code). There was no second screener.
**Raw output:** every counted search is stored verbatim, as returned, in `chapter2/slr/raw_search/Q*.json`.
**Processing:** `chapter2/slr/tools/build_slr.py` recomputes deduplication and all counts from those files.

---

## 1. Information sources actually searched

| # | Source | Interface | Status | Evidence |
|---|---|---|---|---|
| 1 | **OpenAlex** (about 250M scholarly records; indexes IEEE, ACM, ACL Anthology, Springer, Elsevier, MDPI, NDSS, arXiv and others) | FastTrack Literature MCP tool `search_papers` (lexical, relevance-ranked; year filters; page size up to 30) | **SEARCHED** | `Q1…Q11.json` |
| 2 | Crossref | FastTrack `verify_reference` | Used **only** to verify metadata of screened records (venue, pages, authors), not for identification | tool outputs cited in `slr_data.py` comments |
| 3 | Elicit (Lucene keyword mode) | Elicit MCP `search_papers` | **DATABASE ACCESS UNAVAILABLE**. Attempts 1–2 returned a server-side classifier error. Attempt 3 returned `api_access_denied` ("This Elicit account's plan doesn't include API access"). | `search_call_log.tsv` |
| 4 | IEEE Xplore | direct HTTPS | **DATABASE ACCESS UNAVAILABLE** (proxy answered 403 to CONNECT) | `database_access_test_2026-09-25.txt` |
| 5 | ACM Digital Library | direct HTTPS | **DATABASE ACCESS UNAVAILABLE** (403) | same |
| 6 | Scopus | direct HTTPS | **DATABASE ACCESS UNAVAILABLE** (403) | same |
| 7 | Web of Science | direct HTTPS | **DATABASE ACCESS UNAVAILABLE** (403) | same |
| 8 | ScienceDirect | direct HTTPS | **DATABASE ACCESS UNAVAILABLE** (403) | same |
| 9 | SpringerLink | direct HTTPS | **DATABASE ACCESS UNAVAILABLE** (403) | same |
| 10 | ACL Anthology | direct HTTPS | **DATABASE ACCESS UNAVAILABLE** (403) | same |
| 11 | NeurIPS proceedings / PMLR | direct HTTPS | **DATABASE ACCESS UNAVAILABLE** (403) | same |
| 12 | ICLR (OpenReview) | direct HTTPS | **DATABASE ACCESS UNAVAILABLE** (403) | same |
| 13 | USENIX | direct HTTPS | **DATABASE ACCESS UNAVAILABLE** (403) | same |
| 14 | arXiv (supplementary) | export API | **DATABASE ACCESS UNAVAILABLE** (403). arXiv records were reached only through the OpenAlex index. | same |
| 15 | Semantic Scholar API, DBLP, OpenAlex API (direct) | direct HTTPS | **DATABASE ACCESS UNAVAILABLE** (403) | same |

**What this means.** Items 4–15 were **not searched**. Their content is represented only to the extent that OpenAlex indexes it. The review therefore does **not** claim database-by-database coverage of the named digital libraries. Searching them directly before submission is listed as a required follow-up (§7).

---

## 2. Concept blocks (protocol) and how they were operationalised

The protocol defines three Boolean concept blocks plus a financial block:

- **Concept A — Agents:** ("LLM agent" OR "AI agent" OR "language model agent" OR "tool-using agent" OR "autonomous agent")
- **Concept B — Security:** ("security" OR "prompt injection" OR "indirect prompt injection" OR "tool misuse" OR "agent safety" OR "goal hijacking" OR "memory poisoning" OR "action manipulation")
- **Concept C — Runtime / behaviour / mitigation:** ("runtime monitoring" OR "runtime interception" OR "behavioral monitoring" OR "trajectory" OR "tool use" OR "provenance" OR "anomaly detection" OR "mitigation" OR "guardrail" OR "policy enforcement")
- **Financial:** ("financial agent" OR "banking agent" OR "financial AI agent" OR "financial tool" OR "financial transaction") AND (agent security OR prompt injection OR tool misuse OR runtime OR safety OR mitigation)

**Database-appropriate variant.** The only accessible database interface (OpenAlex through `search_papers`) is lexical and relevance-ranked. It does **not** accept Boolean operators, field tags or quoted phrases. The blocks were therefore run as eleven free-text queries, each combining at least one term from A, from B and from C. The financial block was run twice (Q7, Q8). The tool reports the exact string it sent to OpenAlex (`query_used.openalex_lane`), and both strings are recorded below. For Q5 and Q8 the tool dropped a stop-word ("and") or a repeated word ("agent").

The exact Boolean string was also submitted to Elicit (keyword mode), where access was unavailable (§1, item 3).

---

## 3. Search record (PRISMA-S item 8)

Filters for every OpenAlex query: `year_from = 2019`, `year_to = 2026`, `limit = 30`, no type filter, no open-access filter. Although `limit = 30` was requested, the tool returned at most 25 records per page. "Records retrieved" is the number actually returned and screened. "Index estimate" is OpenAlex's total hit estimate for the query.

| Source | Search date | Exact search string (as submitted) | String sent to index | Concept blocks | Filters | Page | Records retrieved | Index estimate | Notes |
|---|---|---|---|---|---|---:|---:|---:|---|
| OpenAlex | 2026-09-25 | `LLM agent indirect prompt injection runtime defense tool use` | same | A+B+C | 2019–2026 | 1 | 25 | 1,366 | Q1 |
| OpenAlex | 2026-09-25 | `LLM agent indirect prompt injection runtime defense tool use` | same | A+B+C | 2019–2026 | 2 | 25 | 1,366 | Q1p2 |
| OpenAlex | 2026-09-25 | `LLM agent security runtime monitoring guardrail tool call` | same | A+B+C | 2019–2026 | 1 | 24 | 1,123 | Q2 |
| OpenAlex | 2026-09-25 | `LLM agent security runtime monitoring guardrail tool call` | same | A+B+C | 2019–2026 | 2 | 25 | 1,123 | Q2p2 |
| OpenAlex | 2026-09-25 | `tool-using language model agent behavioral trajectory monitoring anomaly detection safety` | same | A+B+C | 2019–2026 | 1 | 24 | 5,572 | Q3 (high off-topic yield) |
| OpenAlex | 2026-09-25 | `LLM agent provenance goal alignment tool call misalignment detection` | same | A+B+C | 2019–2026 | 1 | 25 | 484 | Q4 |
| OpenAlex | 2026-09-25 | `prompt injection benchmark tool-integrated LLM agents attacks and defenses evaluation` | `prompt injection benchmark tool-integrated LLM agents attacks defenses evaluation` | A+B+C | 2019–2026 | 1 | 24 | 2,950 | Q5. Run twice with identical totals; the second output is stored. |
| OpenAlex | 2026-09-25 | `LLM agent memory poisoning goal hijacking multi-step attack` | same | A+B | 2019–2026 | 1 | 24 | 579 | Q6 |
| OpenAlex | 2026-09-25 | `financial LLM agent security prompt injection tool misuse` | same | Financial+A+B+C | 2019–2026 | 1 | 24 | 1,368 | Q7 (financial) |
| OpenAlex | 2026-09-25 | `banking agent safety benchmark financial transaction LLM agent` | `banking agent safety benchmark financial transaction LLM` | Financial+A+B | 2019–2026 | 1 | 25 | 536 | Q8 (financial) |
| OpenAlex | 2026-09-25 | `calibrated risk score intervention policy LLM agent runtime safety` | same | A+B+C (decision) | 2019–2026 | 1 | 25 | 880 | Q9 |
| OpenAlex | 2026-09-25 | `privilege control policy enforcement LLM agents tool calls prompt injection` | same | A+B+C | 2019–2026 | 1 | 25 | 1,380 | Q10 |
| OpenAlex | 2026-09-25 | `pre-execution action validation guardrail autonomous LLM agent unsafe actions` | same | A+B+C | 2019–2026 | 1 | 25 | 744 | Q11 |
| **Total** | | | | | | **13 pages** | **320** | — | 101 duplicates removed → **219 unique records** |
| Elicit | 2026-09-25 | `("prompt injection" OR "tool misuse" OR "goal hijacking") AND ("LLM agent" OR "tool-using agent" OR "agentic") AND ("runtime" OR "monitor" OR "guardrail" OR "defense")` | — | A+B+C | keyword mode | — | 0 | — | DATABASE ACCESS UNAVAILABLE (`api_access_denied`) |
| Elicit | 2026-09-25 | Full A AND B AND C Boolean string (see `search_call_log.tsv`) | — | A+B+C | keyword mode | — | 0 | — | Two attempts; classifier error; DATABASE ACCESS UNAVAILABLE |
| Other databases (§1, items 4–15) | 2026-09-25 | not run | — | — | — | — | 0 | — | DATABASE ACCESS UNAVAILABLE |

**Pilot probe (not counted).** A limit-5 probe of the Q1 string was run at 17:52:27 UTC to confirm the tool's behaviour. Its five records are a subset of Q1 and are not counted.

**Stopping rule.** The eleven queries covered every protocol concept block and both financial variants. Page 2 was retrieved for the two queries whose page-1 yield of eligible records was highest (Q1, Q2). Screening was **not** extended to every result of every query: index estimates run to thousands, and the relevance-ranked tail was dominated by off-topic surveys. This is a **retrieval cap**, and it is reported as a limitation. The review does not claim to have screened all records matching the concepts.

---

## 4. Other methods (PRISMA 2020 "identification via other methods")

| Source | Date | Method | Records | Notes |
|---|---|---|---:|---|
| Reference list of the previous integrated Chapter 2 (`tools/sources.py`, S01–S70) | verified 16–25 Sep 2026 | Known-item searching of the thesis corpus; backward citation checking; verification against Crossref and search-engine text | 70 | 11 are the same study as a database record and are counted once (cross-stream duplicates) |
| Prior-art list named in the review protocol (AgentTrust, NEXUS, ProvenanceGuard, FinHarness, AgentDojo, AgentHarm, Progent, AgentSpec, ShieldAgent, Task Shield, MELON, CaMeL, LlamaFirewall) | 2026-09-25 | Checked against both streams | 0 additional | All 13 were already among the 70. Three were also retrieved by the database search: Task Shield (R001), LlamaFirewall (R061) and, with corrupted metadata, AgentDojo (R016). All 13 passed through the same eligibility criteria. |

The other-methods stream is **not independent** of the author's prior reading. That is a source of selection bias, and it is disclosed as such (Chapter 2, §2.2.5 and §2.13.5).

---

## 5. Deduplication

Deduplication was automated in `build_slr.py`. Two records count as duplicates if their DOIs are identical (case-insensitive) or if the first 80 alphanumeric characters of their lower-cased titles are identical. This removed 101 of 320 hits.

One further duplicate was found manually during screening: the IsolateGPT preprint (R210) duplicates the NDSS version (R204). It is logged as a title/abstract exclusion with reason "duplicate".

Cross-stream duplicates (11) are matched by study identity. Where the database copy was a preprint of a peer-reviewed paper (for example ASB and ToolEmu), the study was screened on the database record and cited in its peer-reviewed version.

---

## 6. Search-quality observations

- **Recall of known prior art was low.** Of the 13 prior-art studies named in the protocol, the database queries retrieved only 3 (one with corrupted metadata). The other 10 entered through other methods. Lexical relevance ranking in OpenAlex surfaced highly cited general surveys ahead of specific 2025–2026 preprints, and several preprints (for example AgentTrust, NEXUS, Progent) did not rank within the retrieved pages.
- **One index record was corrupted.** OpenAlex record W4399912700 (R016) carries AgentDojo's arXiv DOI and author list with the title and abstract of an unrelated derived corpus ("AgentDojo-PROV"). It was excluded as a metadata conflict. AgentDojo was assessed via the other-methods record.
- **Fifteen** of the 219 unique records had no abstract in the index, or only an author list in its place. They were screened on title and venue. Where such a record passed title screening, the missing information was sought:
  - VIGIL (R031) and R-Judge (R157): abstract obtained through web search; the studies are labelled PARTIALLY VERIFIED.
  - AGrail (R214): assessed through its prior verification record (S30).
  - R218: excluded for insufficient information.

---

## 7. Reproduction and follow-up

1. Re-run each string in §3 through OpenAlex (`https://api.openalex.org/works?search=<string>&filter=from_publication_date:2019-01-01,to_publication_date:2026-12-31`), sorting by relevance. Result ranks may differ from the MCP tool's ranking, and index contents change over time.
2. Before submission, run the Boolean blocks of §2 **directly** in IEEE Xplore, ACM DL, Scopus or Web of Science, ACL Anthology and arXiv. Screen the new records with the same criteria and update the PRISMA diagram. Until this is done, PRISMA item 6 (information sources) and PRISMA-S items 1–3 are only partly satisfied.
3. Obtain full texts through institutional access for the 71 included studies, and re-appraise every item currently coded "Not Verified".
