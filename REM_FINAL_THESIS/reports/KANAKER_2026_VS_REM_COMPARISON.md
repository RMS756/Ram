# Kanaker et al. (2026) and REM: evidence-based comparison

**Paper.** Kanaker, H., Fakhouri, H., Abdel Karim, N., Abuhamdeh, M., Ismail, N. H. A., & Fakhouri, S. (2026). Securing tool-using AI agents against injection and authority misuse. *Computation, 14*(5), Article 98. https://doi.org/10.3390/computation14050098

## Evidence base (checked on 2 November 2026)

| Element | Source | Result |
|---|---|---|
| DOI registration, title, authors and order, journal, volume, issue, article number, year | Crossref record of DOI 10.3390/computation14050098 (literature connector `verify_reference`) | Registered. Authors in order: Hasan Kanaker; Hussam Fakhouri; Nader Abdel Karim; Maher Abuhamdeh; Nurul Halimatul Asmak Ismail; Sandi Fakhouri. *Computation* (MDPI) 14(5), 98, 2026. No retraction flagged (this does not prove absence of retraction) |
| Abstract | OpenAlex W7160053090 (`get_paper`); identical to the record stored on 30 Oct 2026 in `REM_FINAL_THESIS/verification/update_search_2026-10-30.json` | Read in full |
| Version | Crossref lists one journal article; OpenAlex marks it open access with a PDF at `mdpi.com/…/pdf?version=1779695899` | The publisher's version string could not be opened. Whether corrections or later versions exist: **not verified** |
| Full text | `www.mdpi.com`, its PDF and `doi.org` | **Not accessed.** WebFetch: host not resolvable; curl through the proxy: HTTP 403 |

**Evidence level of every statement about the paper: A (abstract and metadata).**

## Comparison

| Dimension | Kanaker et al. (2026), level A | REM (thesis R5) | Relation |
|---|---|---|---|
| Research question | How architectural choices and controls change user-facing risk, without testing deployed products | Whether tiered expected-loss verdicts change intervention, ASR and utility relative to a same-estimator threshold ([PD]) | Different questions: design-time architecture vs a per-call runtime decision |
| Method | Threat model separating compromise, harm and severity; Monte Carlo pipeline | Evidence features → ridge LR → logit calibration → tiers → expected-loss verdict → deterministic mitigation → audit | Shared idea only: likelihood of compromise kept separate from severity. REM's separation predates this examination (Stage 2, 19 Sep 2026) and is not derived from the paper |
| Data | Simulator; 6 scenarios; 9 defense configurations | Recorded AgentDojo banking traces from 21 agents; replay; no live runs | Neither is a live field measurement. The paper is fully simulated; REM uses recorded real-agent behaviour |
| Harm and severity | Severity-weighted harm as an outcome | Tier-indexed declared losses in the decision; realized loss as an outcome | Comparable concern; different use (outcome metric vs decision input) |
| Defenses | Least privilege, human approvals, retrieval allowlisting, rate limiting (others not read) | Allow / Modify / Escalate / Block per call; two mitigation semantics; two reviewer bounds | Not tested against each other |
| Outcomes | ASR, benign task success, latency overhead, severity-weighted harm | Discrimination, calibration, intervention, ASR, benign utility, utility under attack, processing time, realized loss | Similar reporting breadth |
| Limitations | Simulator; comparative guidance, not incident rates (stated by the authors) | Exploratory; replay; proxy labels; unapproved costs; one benchmark | Results are not transferable in either direction |

## What the paper supports in REM, and what it does not

- **Supports, as consistency (cited in Ch. 3):**
  - keeping P(adversarially induced) separate from consequence (§3.7.3);
  - the perfect-reviewer assumption being optimistic (§3.7.5).
- **Supports, as interpretation (cited in Ch. 6):**
  - reading the idealized-reviewer results as an upper bound;
  - reporting a loss-weighted measure beside ASR.
- **Does not support:**
  - REM's effectiveness;
  - its originality;
  - its costs or tiers;
  - any of its numerical results.

  It also does not show that REM is preferable to least privilege or allowlisting, because neither study compares them.
- **Co-authorship.** One co-author supervises this thesis. Co-authorship is not treated as approval of REM's design.
