# REM-X Design Amendment 01: critical revision and prior-art validation

**Status.**
- Design and documentation only.
- **No implementation, no experiments, no benchmark runs.**
- REM v1.0, REM-DiD, the thesis and its editions, frozen protocols, results, `did3_common.py` and the test file are **unchanged**.
- `REM_X_DESIGN/` (commit `1e7dadb`) is kept as the historical record. This package supersedes it where they differ.
- Phase 0 and Phase A are **not started**.

**Researcher instruction applied throughout (27 Nov 2026):**
- no new equations, scores, thresholds or statistical expressions;
- requirements stated in words;
- established methods cited with verified references;
- every unsourced mathematical item in the earlier REM-X documents flagged in A1-11.

**Status markers:**

| Marker | Meaning |
|---|---|
| [V1] | REM v1.0, evaluated |
| [DiD-I] / [DiD-T] | REM-DiD, implemented; exploratory replay / unit-tested |
| [PA] | Adopted from prior art |
| [X-P] | Proposed REM-X, not implemented |
| [PD] | Proposed wording or decision, not approved |

**Evidence levels:**

| Level | Meaning |
|---|---|
| F | Full text read |
| R | Repository (and, for ROPE, the authors' run logs) read; nothing executed |
| A | Abstract |
| S | Search excerpt of the full text |
| C | Crossref record |

## Deliverables

| # | File | Content |
|---|---|---|
| 1 | `01_UPDATED_PRIOR_ART_MATRIX.md` | Updated evidence status; main matrix including ROPE and AGATE |
| 2 | `02_ROPE_VS_REM_X.md` | ROPE at code and log level: delegated sources, authenticated origins, file bodies, recipients, amounts, fail-closed losses; research question |
| 3 | `03_AGATE_VS_REM_X.md` | AGATE at A/S level: registration, grants, effect ledger, adapters, parameter rewriting, utility losses; deduplication vs cumulative exposure; research question |
| 4 | `04_D1_SECURITY_AND_TRUST_ASSUMPTIONS.md` | Why detector silence is not evidence; nine attack cases; five-outcome model (O1–O5) based on affirmative evidence |
| 5 | `05_D1_NOVELTY_ASSESSMENT.md` | D1 element by element; verdict: implementation variant |
| 6 | `06_FINANCIAL_THREAT_COVERAGE.md` | Revised threat coverage (prevent / bound / reviewer-dependent) |
| 7 | `07_FAIR_COMPARISON_PROTOCOL.md` | ROPE as released, AgentCap-class, deduplication-class, CaMeL, Progent; legitimate and forged document fixtures; cited statistics |
| 8 | `08_CONTRIBUTION_STATEMENT.md` | Withdrawn claims; claims defensible now; conditional wording |
| 9 | `09_GO_NO_GO_AND_FINAL_DECISION.md` | Revised recommendation; design-blocked items; answers to the six final questions |
| — | `10_D2_D3_REASSESSMENT.md` | D2 adopted mechanisms and unverified integration properties; D3 prior-art support |
| — | `11_MATHEMATICAL_TRACEABILITY_AUDIT.md` | 12 items flagged in `REM_X_DESIGN`, with replacement wording |

## Sources consulted in this amendment

- ROPE repository, commit `ffe27c4`: <https://github.com/xhOwenMa/ROPE> (code and run logs read in a scratch clone outside the repository; nothing executed).
- AGATE, arXiv 2609.30830: <https://arxiv.org/abs/2609.30830v1> (abstract via OpenAlex record W7214603931; full text not reachable).
- AgentCap, arXiv 2611.00729: <https://arxiv.org/abs/2611.00729>
- Agent-Sentry, arXiv 2603.22868: <https://arxiv.org/abs/2603.22868>
- AIS, *Systems* 14(10) 1329: <https://www.mdpi.com/2079-8954/14/10/1329>; earlier version arXiv 2608.30519: <https://arxiv.org/abs/2608.30519>
- AutoDojo, arXiv 2606.15057: <https://arxiv.org/pdf/2606.15057>
- "The Attacker Moves Second", arXiv 2510.09023: <https://arxiv.org/pdf/2510.09023>
- MAS, Safeguards for Agentic Finance at Runtime v1.1: <https://www.mas.gov.sg/-/media/mas-media-library/development/fintech/ai-safr/safr-v1-1.pdf>

**Access limits.** Full-text access was blocked from this session: DNS failure for `arxiv.org`, `www.mdpi.com` and `www.alphaxiv.org`. No workaround was attempted.
