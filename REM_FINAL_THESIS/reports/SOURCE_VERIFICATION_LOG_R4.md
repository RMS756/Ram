# Source Verification Log, R4 (1 November 2026)

This log adds to `SOURCE_VERIFICATION_LOG.md` (R3, 30 Oct). It records what could be accessed in the R4 session, what was checked, and at which level.

## 1. Access in this session (1 November 2026)

| Host or route | Result |
|---|---|
| arxiv.org, export.arxiv.org (curl through the session proxy) | Refused (connection rejected) |
| arxiv.org (WebFetch tool) | Refused: host not resolvable from this session |
| api.crossref.org, api.openalex.org, doi.org | Refused |
| Publisher hosts tested (wr-publishing.org, link.springer.com via doi.org, usenix.org, openreview.net, citeseerx) | Refused |
| github.com | Refused (HTTP 403) |
| raw.githubusercontent.com | **Reachable** |
| FastTrack literature connector (Crossref `verify_reference`; OpenAlex `get_paper`) | Reachable: metadata and abstracts only |

**Consequence.** No paper's full text could be retrieved in this session. Full-text reading of the closest prior work and of the foundational equation sources remains **NOT DONE**. To enable it, arxiv.org and the publisher hosts must be allowed in the environment's network settings.

## 2. Verification levels used

| Level | Meaning |
|---|---|
| **M** | Metadata confirmed against a registry record (Crossref or OpenAlex) |
| **A** | Claim supported by the abstract in an index record |
| **R** | Claim supported by the authors' own public repository documentation. The repository may describe a different version from the cited paper |
| **F** | Claim checked against the full text. **No source reached level F in R3 or R4** |
| **U** | Not supported by any record accessed in these sessions |

## 3. Checks made on 1 November 2026

| Work | Source accessed | Version / identifier | Result | Level reached | Effect on the thesis |
|---|---|---|---|---|---|
| NEXUS (Hossain et al., 2026) | Authors' repository README, `raw.githubusercontent.com/eliashossain001/nexus/main/README.md`, retrieved 1 Nov 2026; 14,406 bytes; SHA-256 `a48e7de8…ed9205`; copy in `verification/sources_R4/nexus_README.md` | Main branch at retrieval time; the README says it describes a retrained 9-feature scorer | **Supports:** the cascade policy Π, stated explicitly; threshold selection (τ_b, τ_c) = (0.75, 0.70) on a λ-weighted safety–utility loss over a 5×5 grid; Platt scaling on a 60-instance calibration split; ECE 0.085 → 0.013 on the 128-instance test split. **Does not support:** the specific cost values (0, 0.1, 0.3, 1); the isotonic comparison. **Differs:** headline F1 and accuracy figures differ from the abstract figures in the thesis | R for the supported items; open items stay U | Ch. 2 §2.8.4, §2.9.3; Ch. 6 Table 6.3: level R added; the abstract figures kept; the discrepancy recorded. OI-01, OI-03 and OI-04 partly addressed at level R; OI-02 (feature count) is answered by the README for its current version (9 features); OI-05 and OI-06 remain open |
| Platt (cited as 1999) | Crossref record for DOI 10.7551/mitpress/1113.003.0008 (connector) | MIT Press chapter, *Advances in Large-Margin Classifiers*, pp. 61–74, issued and printed 2000, title registered as "Probabilities for SV Machines" | The thesis entry cites the edited-volume chapter (editors, pp. 61–74). The registered year of that chapter is 2000 | M | Year corrected to 2000 throughout; DOI added; title discrepancy disclosed in the entry. The project never read the chapter (Stage 2 record: "Not read"), so the source status of Eq. 3.3 stays NC |
| Lin, Lin & Weng (2007), *Machine Learning* 68(3), 267–276 | Crossref (connector), DOI 10.1007/s10994-007-5018-6 | — | Exists; the review named it as a secondary source on Platt's method | M | Not cited in the thesis; recorded only as the reviewer's evidence |
| Kekatos et al. (2026) | OpenAlex record via the connector (the arXiv DOI 10.48550/arXiv.2610.09793 resolves to the same work, merged with the ACM record 10.1145/3847353.3847499) | ACM CPSIoTSec 2026; arXiv preprint 2610.09793 | Abstract retrieved: offline MFOTL monitoring of AgentDojo, STAC and R-Judge recorded trajectories with MonPoly; obligations flag 70.1% of successful AgentDojo attacks and fire on 29.3% of benign runs | A | Unchanged in the thesis (already cited at abstract level) |
| PROVISO, TapGuard, AgentTrust, ProvenanceGuard, FinHarness | No new route available | — | Not re-checked; status as in the R3 log | A or M | Unchanged |
| Cox (1958); le Cessie & van Houwelingen (1992); Guo et al. (2017); Elkan (2001); Chow (1970); Lundberg & Lee (2017) | No full-text route | — | Not re-checked | M | Equation-source codes in Ch. 3 Table 3.17 unchanged |

## 4. What remains

- Full-text reading (level F) of NEXUS, AgentTrust, ProvenanceGuard, FinHarness, PROVISO, TapGuard and Kekatos et al., and of the sources of Eqs. 3.1–3.3, 3.6, 3.9–3.12, 3.15 and 3.16.
- The printed title of the Platt chapter, and the version a reader would actually consult.
- Any expansion of the literature search. None was run in R4, so the PRISMA counts are unchanged; the October currency records stay outside the PRISMA flow.
