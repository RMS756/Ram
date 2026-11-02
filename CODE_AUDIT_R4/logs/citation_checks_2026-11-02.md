# Citation checks, 2 Nov 2026 (FastTrack Literature connector: Crossref verify_reference, OpenAlex get_paper; WebFetch)

| Source (as in REFERENCES_R4.md) | Route | Result | Evidence level reached |
|---|---|---|---|
| le Cessie & van Houwelingen (1992), Applied Statistics 41(1), 191 | Crossref, DOI 10.2307/2347628 | Registered; title, authors, vol/issue, first page 191 match (Crossref gives first page only) | Metadata |
| Platt (2000), MIT Press, pp. 61-74, DOI 10.7551/mitpress/1113.003.0008 | Crossref | Registered as "Probabilities for SV Machines" (2000, pp. 61-74). Printed title in thesis differs from registered title (disclosed in the reference note) | Metadata; chapter text NOT read |
| Guo et al. (2017), ICML / PMLR 70 | Crossref (no PMLR DOIs; no match); OpenAlex arXiv record W2626967530 | Exists (arXiv 1706.04599). Abstract: "temperature scaling -- a single-parameter variant of Platt Scaling" | Abstract only |
| Kull, Silva Filho & Flach (2017), AISTATS, PMLR 54, 623-631 | Crossref | No PMLR record; Crossref returns the related EJS 11(2) 2017 paper by the same authors (different work) | Not confirmed by registry |
| Elkan (2001), IJCAI-01, 973-978 | Crossref | No record (IJCAI-01 proceedings carry no Crossref DOI) | Not confirmed by registry |
| Lundberg & Lee (2017), NIPS 30, 4765-4774 | Crossref | No record (NIPS 2017 has no Crossref DOI) | Not confirmed by registry |
| Any full text (arxiv.org) | WebFetch https://arxiv.org/abs/1706.04599 | getaddrinfo ENOTFOUND: host outside the session's allowed network domains | Full text unavailable |

No source's full text was read in this audit. The reading guide in REM_STAGE2_INPUT_PACKAGE/PAPER_READING_PACK and earlier AI summaries were not treated as substitutes.
