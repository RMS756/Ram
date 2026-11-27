# Prior-art investigation: publication status and evidence levels (27 November 2026)

## 0. What could and could not be read in this session

**Full texts were not accessible in this session.** The session's network policy refuses `arxiv.org` (HTTP 403 from the egress proxy). Through the web-fetch tool, `arxiv.org`, `alphaxiv.org`, `openreview.net`, `dblp.org`, `neurips.cc`, `satml.org`, `css.csail.mit.edu` and `pdl.cmu.edu` all failed DNS resolution. No workaround was attempted.

The user's saved environment `ram-thesis-research` allows `arxiv.org`, but a running session cannot be moved onto it. A new session started in that environment can read the arXiv full texts. That is the first item of `36_CHAPTER_REFERENCES_AND_EXPERIMENTS.md` §2.

Every statement in files 30–36 therefore carries one of these evidence levels:

| Level | Meaning |
|---|---|
| **F** | Full text read, in this project, from a PDF whose SHA-256 is recorded (dates given) |
| **R** | Authors' official code repository read at a fixed commit (not executed), in an earlier task of this project |
| **W** | Authors' institutional publication page read in this session |
| **C** | Crossref record checked in this session (DOI registered; metadata) |
| **A** | Abstract and metadata from the OpenAlex index, retrieved in this session |
| **S** | Search-engine excerpt of the full text, retrieved in this session. **Unverified.** Numbers at level S must not be cited in the thesis until checked against the full text |
| **L** | Local inspection of the installed AgentDojo 0.1.35 package (primary evidence about the benchmark) |

**Rule used:** a mechanism is attributed to a paper only if it appears at level F, R, W or A. Level-S material is labelled every time it is used. Where the abstract is silent, the entry reads "not determined (full text not read)", never "absent".

## 1. Publication-status verification of the ten mandatory works

| # | Work as named in the task | Verified bibliographic status | Peer reviewed? | Level | Discrepancies and notes |
|---|---|---|---|---|---|
| 1 | Greshake et al. (2023) | Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., & Fritz, M. *Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection.* Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security (AISec '23), pp. 79–90. DOI 10.1145/3605764.3623985 | Yes (ACM workshop) | A, plus the existing thesis entry | None |
| 2 | Debenedetti et al. (2024), AgentDojo | Debenedetti, E., Zhang, J., Balunović, M., Beurer-Kellner, L., Fischer, M., & Tramèr, F. NeurIPS 2024, Datasets and Benchmarks Track. Index DOI 10.52202/079017-2636 | Yes | A, L | The abstract counts 97 tasks and 629 security test cases over all suites. Banking v1 in 0.1.35: 16 user tasks, 9 injection tasks, 11 tools (L) |
| 3 | Zhang et al. (2025), ASB | Zhang, H., Huang, J., Mei, K., Yao, Y., Wang, Z., Zhan, C., Wang, H., & Zhang, Y. *Agent Security Bench (ASB)…* ICLR 2025. arXiv 2410.02644 | Yes (ICLR) | A | None |
| 4 | Zhong et al. (2025), RTBAS | Zhong, P. Y., Chen, S., Wang, R., et al. (7 authors). arXiv 2502.08966 | **No: preprint** | A; S for one figure | Full author list not verified. No venue found |
| 5 | Debenedetti et al. (2025/2026), CaMeL, "including its published SaTML 2026 version" | Debenedetti, E., Shumailov, I., Fan, T., Hayes, J., Carlini, N., Fabian, D., Kern, C., Shi, C., Terzis, A., & Tramèr, F. *Defeating prompt injections by design.* arXiv 2503.18813 (v2, 24 June 2025, per the PDF header quoted in a search excerpt) | **Not confirmed.** Treat as preprint | R (repository, 13 Nov 2026); S | **SaTML 2026 publication could not be confirmed.** No reachable page (SaTML, OpenReview, DBLP, arXiv) and no search result confirms it. Cite the arXiv v2 until the SaTML proceedings record is seen. The task's premise is unverified, not refuted |
| 6 | Shi et al. (2025), "Progent: Programmable Privilege Control for LLM Agents" | Shi, T., He, J., Wang, Z., Li, H., Wu, L., Guo, W., & Song, D. *Progent: Securing AI agents with privilege control.* arXiv 2504.11703**v3**, 14 May 2026 | **No: preprint**. Every page of v3 is headed "Preprint" | **F** (v3, read in full 16 Nov 2026), R | **Title mismatch:** the title in the task differs from v3's title. It may be an earlier version's title; arXiv's version history could not be checked here. Cite the version actually read |
| 7 | Suresh & Gao (2026), AgentCap | Kabbinamakki Suresh, A. K., & Gao, P. *AgentCap: Capability-based runtime authorization for secure LLM agent execution.* arXiv 2611.00729 (listed in cs.CR on 3 Nov 2026) | **No: preprint** | A; S | The first author's full name is "Aravinda Kashyap Kabbinamakki Suresh"; the surname form for citation must be checked on the paper |
| 8 | Narisetty et al. (2026) | Narisetty, P., Kore, S. N. B., Kattamanchi, U. K. R., & Kumarapu, J. *Adaptive evaluation of out-of-band defenses against prompt injection in LLM agents.* arXiv 2606.26479 | **No: preprint** | A | The abstract calls its result "one small-scale data point" |
| 9 | Costa et al., "verify actual publication status and date" | Costa, M., Köpf, B., Kolluri, A., Paverd, A., Russinovich, M., Salem, A., Tople, S., Wutschitz, L., & Zanella-Béguelin, S. *Securing AI agents with information-flow control.* arXiv 2505.23643 (v1 29 May 2025; v2 3 Sep 2025, per search excerpt). System name: Fides | **Accepted at NeurIPS 2026 according to the authors' institution**; proceedings record not verified | W (Microsoft Research page: "Neural Information Processing Systems (NeurIPS)", December 2026), A | The NeurIPS virtual-site poster page (2026, poster 152696) appeared in search but could not be opened. Recommended citation: the NeurIPS 2026 paper once the proceedings record is verified; until then, the arXiv preprint with a note "to appear, NeurIPS 2026". The thesis currently cites it as a preprint, "full text not read" |
| 10 | Other relevant work | See `31_PRIOR_ART_LITERATURE_MATRIX.md`, Part B | Mixed | A, C, F | Kept to works found in this session or already in the thesis |

## 2. Other works whose status matters for positioning

| Work | Status | Level |
|---|---|---|
| Gong, H., Samawi, M., & Medda, F. (2026). *Authority–inference separation in agentic finance: Intent-bound control, EVM enforcement, and replayable assurance.* **Systems, 14(10), 1329.** DOI 10.3390/systems14101329 | **Peer-reviewed journal article** (MDPI), Crossref-registered. An earlier arXiv version (2608.30519, 31 Aug 2026) has a different subtitle ("First-Line Control, Blockchain Enforcement, and Replayable Assurance") | C, A, S |
| She, Y., Liang, Y., & Kang, E. (2026). ProvenanceGuard. *IEEE/ACM ASE 2026*. DOI 10.1145/3832783.3837535 | Peer reviewed (the thesis cites it as a preprint, so that entry needs updating) | A |
| Li, H., Liu, X., Chiu, C., et al. (2025). DRIFT. NeurIPS 2025. DOI 10.52202/085713-2791 | Peer reviewed | A |
| Kim, M., Parmar, M., Wallis, P., et al. (2026). CausalArmor. ICML 2026 (PMLR v306) | Peer reviewed | A |
| Wang, C., Zhang, J., Zhang, Z., et al. (2026). AdapTools. EMNLP 2026. DOI 10.18653/2026.emnlp-main.2055 | Peer reviewed | A |
| PACT (Fan et al., 2026), AuthGraph (P. Wang, Li & Tian, 2026), AGATE (X. Zhang et al., 2026), Agent-Sentry (Sequeira et al., 2026), AIRGuard (Qin et al., 2026), ScopeGate (Mellafe Zuvic, 2026), ToolFence (Y. Li et al., 2026), APPA (Kravchenko et al., 2026), AgentTrust (C. Yang, 2026), PRISM (2026), AgentSandbox (K. Zhang et al., 2025) | Preprints (arXiv) | A |
| GuardRail (Karnawat, Patil & Chaudhari, 2026); CAGE (Gul et al., 2026) | Zenodo reports or software; **not peer reviewed**; GuardRail reports no quantitative result | A |
| Eltayeb & Alhalangy (2026), *Scholar Journal for Sciences & Technology*; "A Scenario-Based Benchmark for Evaluating AI Safety Controls in Banking Operations" (2024), *IJFIST* | Journal articles; venue quality not assessed; abstract level only | A |
