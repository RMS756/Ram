# Literature checks — 28 October 2026 (revision R2)

Access:
- arxiv.org: refused by the session network policy (WebFetch: host not resolvable; curl: connection refused).
- Publisher sites: refused by the same policy.
- Full texts: none retrieved.
- Tools used:
  - OpenAlex records via the FastTrack connector (`get_paper`): title, authors, abstract, venue, retraction flag.
  - Crossref (`verify_reference`).

| Work (as cited in thesis) | Record found (28 Oct) | Abstract supports | Not supported by abstract (status) | Change |
|---|---|---|---|---|
| NEXUS, Hossain et al. 2026, arXiv:2607.19356 | OpenAlex W7170148714; preprint; 5 authors | Four actions (allow, block, request confirmation, request revision); "formal intervention policy"; deterministic rules, argument-level inspection, calibrated logistic-regression risk score "for graded escalation"; "structured-plan safety monitor"; 128-instance synthetic benchmark; R-Judge; AgentHarm; IPI 0% ASR; median latency 0.205 ms | "Expected-loss objective with fixed costs", "deployed policy is a rule cascade" — rest on the Stage 1 full-text reading (OI-01), not reproducible; **UNVERIFIED in this session** | Reword as unverified; keep abstract-supported facts |
| AgentTrust, C. Yang 2026, arXiv:2605.04785 | W7160539043; preprint; 1 author | Pre-execution interception; four verdicts (allow, warn, block, review); deobfuscation normalizer; SafeFix; RiskChain multi-step detection; LLM-as-judge; 300 + 630 scenario benchmarks; 95.0% / 96.7% verdict accuracy; low-ms latency | "Maximum-severity aggregation", "confidence by step function" — **not abstract-supported; UNVERIFIED** | Mark unverified |
| ProvenanceGuard, She et al. | **Peer-reviewed version exists:** Proc. 41st IEEE/ACM ASE 2026, pp. 3036–3048, doi:10.1145/3832783.3837535 (Crossref-registered, 3 authors) | Misalignment = proposed tool call not supported by traceable evidence in context; multi-stage pipeline before execution; AgentSafetyBench and WorkBench; 11 backbones | — | Update citation to ASE version |
| FinHarness, Jia et al. 2026, arXiv:2605.27333 | W7162582690; preprint; 13 authors | Query Monitor (intent + cross-turn drift); Tool Monitor per prospective call; Cascade between two LLM-judge tiers; ASR 38.3% → 15.0%; benign approval 41.1% → 39.3%; 4.7× fewer advanced-judge calls; evaluated on FinVault | — | Keep; reword the FinVault caveat (below) |
| FinVault, Z. Yang et al. 2026, arXiv:2601.07853 | W7124179260; OpenAlex shows no retraction flag; abstract available | Benchmark exists (31 scenarios, 107 vulnerabilities, 963 cases) | Withdrawal recorded on 25 Sep 2026 (`chapter2/CHAPTER2_VERIFICATION_LOG.md`: author withdrawal comment citing legal/IP/affiliation reasons). **Not re-confirmable on 28 Oct** (arXiv refused); OpenAlex carries no retraction flag (an arXiv withdrawal is not a journal retraction) | Treat as: withdrawn for stated non-scientific reasons (per 25 Sep record); figures measured on it are not shown to be invalid but are less confirmable |
| SafeAgent, H. Liu et al. 2026, arXiv:2604.17562 | W7155077488; preprint | Runtime controller + context-aware decision core over session state; operators for risk encoding, utility-cost evaluation, consequence modeling, policy arbitration; ASB and InjecAgent | "Operators realized through LLM reasoning" — **not abstract-supported; UNVERIFIED** | Reword |
| Calibration is not control, C. Zhang et al. 2026, arXiv:2606.21399 | W7165635812; **current title "Calibration Is Not Control: Intervention Value for LLM-Agent Oversight"** (thesis uses "…: Why LLM-agent oversight needs intervention") | Recalibration preserves threshold policy class; evaluates by **replaying agent prefixes and executing alternative actions from the same state**; ALFWorld regret 0.51 → 0.09 | — | Correct title (version change); note replay method relevance to SC-7 |
| H.-H. Chen 2026, arXiv:2605.25632 | W7162461037; preprint | Prices each side-effect action against a safe default; gates against reserve capital; four environments incl. tau-bench | — | Keep |
| AgentDojo, Debenedetti et al. 2024 | NeurIPS 2024 proceedings doi:10.52202/079017-2636 (confirmed 27 Oct) | — | — | Use proceedings citation |

No record above carries an OpenAlex retraction flag. Absence of a flag is not proof of non-retraction.
