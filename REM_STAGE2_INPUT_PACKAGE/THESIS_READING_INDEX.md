# THESIS READING INDEX — Chapters 2 and 3

**Created:** 2026-09-22 · **Type:** read-only index. No chapter, citation, reference, algorithm or experiment was changed to produce it.

**Sources used (all in this repository):**

- `REM_STAGE2_INPUT_PACKAGE/working/Chapter2_working.md` — SHA-256 `1e59d4a74d9205a2`
- `REM_STAGE2_INPUT_PACKAGE/working/Chapter3_working.md` — SHA-256 `5085e11732dee82f`
- `REM_STAGE2_INPUT_PACKAGE/stage1_audits/` — Stage 1 workbooks 01, 03 and 06 (claims, reference master, numerical claims)
- `REM_STAGE2_OUTPUT/STAGE2_RESOLUTION_REPORT.md` and the Stage 2 workbooks
- `V1_NEXUS_DIRECT_VERIFICATION.md`

Both digests match the Stage 1 baseline. The chapters were read, not edited.

## How to read this index

**Reference numbers.** Both chapters use APA author–date citation and do not number their references. The number given for each entry is its **position in that chapter's reference list**, which is alphabetical. That order is preserved exactly. The Stage 1 `REF-nnn` identifier is also given, so one paper can be followed across both chapters and all audit files.

**"Cited in".** This lists every section containing a formal author–date citation of the entry, with line numbers in the working files, so each use can be found and read in place. A system named without a citation (for example, "NEXUS" on its own) is not counted.

**"Paper available locally".** No cited paper is stored in this repository. A search of the whole repository found **no PDF, PostScript, BibTeX or RIS file**. Stage 1 and Stage 2 read sources online (abstract pages, publisher and index records, and in a few cases full text) and did not save them. Every entry is therefore marked **No**.

**Verification status: one rule for every entry.**

| Status | Meaning |
| --- | --- |
| **VERIFIED** | The work exists, its cited metadata matches the record, and the content the chapter attributes to it was checked in the source. This may be full text or, where the specific claim appears there, the abstract. |
| **PARTIALLY VERIFIED** | The work exists and is identified, but either the content the chapter attributes to it was not checked in the source, or part of the cited metadata conflicts with the record. |
| **UNVERIFIED** | Neither the existence nor the metadata of the work, as cited, has been confirmed. |

Statuses come from the Stage 1 reference master, updated only where Stage 2 produced new evidence. The **Basis** field on each card says which, and how deep the check went. Many VERIFIED entries were checked **at abstract level only**, and the Basis field says so wherever that applies.

> **Label difference from the Stage 2 report.** The Stage 2 report labelled Brier (1950), Cox (1958), le Cessie & van Houwelingen (1992), Chow (1970) and Jackson (2025) "VERIFIED (T2 bibliographic)", meaning their records were confirmed against Crossref. Their text was not read. Stage 1 classified that same kind of evidence as PARTIALLY VERIFIED. This index applies the Stage 1 rule to all entries, so those five appear here as **PARTIALLY VERIFIED**. The evidence is the same; only the label differs.

---

## 1. Chapter 2 References

All 47 entries in the reference list of `working/Chapter2_working.md` (list starts at line 233), in the chapter's own order. Every entry is cited at least once in the text, and every in-text citation matches an entry.

#### 1. Dos and don'ts of machine learning in computer security

| Field | Value |
| --- | --- |
| Order in reference list | 1 |
| Stage 1 Ref ID | REF-001 |
| Authors | Arp, D., Quiring, E., Pendlebury, F., Warnecke, A., Pierazzi, F., Wressnegger, C., Cavallaro, L., & Rieck, K. |
| Year | 2022 |
| DOI / arXiv / URL | https://arxiv.org/abs/2010.09470 — confirmed (Stage 1 metadata check) |
| Cited in | §2.8 Detection and Classification Approaches (L116) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (claim used is in the abstract). |
| What the chapter uses | Cited as evidence that learning-based security systems have design and evaluation pitfalls that inflate performance estimates, as a caution for learned detectors. |

#### 2. Detection of abrupt changes: Theory and application

| Field | Value |
| --- | --- |
| Order in reference list | 2 |
| Stage 1 Ref ID | REF-002 |
| Authors | Basseville, M., & Nikiforov, I. V. |
| Year | 1993 |
| DOI / arXiv / URL | https://people.irisa.fr/Michele.Basseville/kniga/ — confirmed (Stage 1 metadata check) |
| Cited in | §2.5 Stateful and Trajectory-Aware Protection (L75) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: Author-hosted PDF text: eqs. 2.1.2, 2.2.8-2.2.10 read. |
| What the chapter uses | Cited as the detailed treatment of the properties of the CUSUM procedure. |

#### 3. Insuring every action: An authority frontier framework for runtime actuarial control of autonomous AI agents

| Field | Value |
| --- | --- |
| Order in reference list | 3 |
| Stage 1 Ref ID | REF-008 |
| Authors | Chen, H.-H. |
| Year | 2026 |
| DOI / arXiv / URL | arXiv:2605.25632 — confirmed (Stage 1 metadata check) |
| Cited in | §2.6 Tool-Use and Action-Boundary Security (L87, L89); §2.7 Financial-Agent Security Requirements (L110); §2.10 Runtime Decision and Mitigation (L132); §2.13 Comparative Synthesis (L184, L191, L193); §2.15 Positioning of REM (L211) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract. |
| What the chapter uses | Used as prior art showing that pre-execution pricing of an agent action's consequence (Actuarial Action Interface, Authority Frontier) already exists, and as a named comparison in REM's positioning. |

#### 4. Standard benchmarks fail — Auditing LLM agents in finance must prioritize risk

| Field | Value |
| --- | --- |
| Order in reference list | 4 |
| Stage 1 Ref ID | REF-006 |
| Authors | Chen, Z., Chen, J., Chen, J., & Sra, M. |
| Year | 2025 |
| DOI / arXiv / URL | arXiv:2502.15865 — confirmed (Stage 1 metadata check) |
| Cited in | §2.7 Financial-Agent Security Requirements (L95) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (v2 title and argument). |
| What the chapter uses | Used for the argument that evaluating financial LLM agents on accuracy and return metrics gives an illusion of reliability while missing vulnerabilities. |

#### 5. ShieldAgent: Shielding agents via verifiable safety policy reasoning

| Field | Value |
| --- | --- |
| Order in reference list | 5 |
| Stage 1 Ref ID | REF-007 |
| Authors | Chen, Z., Kang, M., & Li, B. |
| Year | 2025 |
| DOI / arXiv / URL | arXiv:2503.22738 — confirmed (Stage 1 metadata check) |
| Cited in | §2.4.3 Learned and LLM-based guardrails (L53); §2.11 Explainability and Auditability (L144); §2.13 Comparative Synthesis (L178) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (numbers used are in the abstract). |
| What the chapter uses | Used as an example of a guardrail that turns policy documents into verifiable probabilistic rule circuits, with its reported performance figures. |

#### 6. Cordon: Semantic transactions for tool-using LLM agents

| Field | Value |
| --- | --- |
| Order in reference list | 6 |
| Stage 1 Ref ID | REF-009 |
| Authors | Chen, Z., Liu, H., Xu, D., Dong, D., Li, J., Pu, B., & Zhai, J. |
| Year | 2026 |
| DOI / arXiv / URL | arXiv:2606.17573 — confirmed (Stage 1 metadata check) |
| Cited in | §2.6 Tool-Use and Action-Boundary Security (L87); §2.10 Runtime Decision and Mitigation (L136) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract. |
| What the chapter uses | Used as an example of a transactional runtime that stages and validates action effects before commitment. |

#### 7. AgentPoison: Red-teaming LLM agents via poisoning memory or knowledge bases

| Field | Value |
| --- | --- |
| Order in reference list | 7 |
| Stage 1 Ref ID | REF-005 |
| Authors | Chen, Z., Xiang, Z., Xiao, C., Song, D., & Li, B. |
| Year | 2024 |
| DOI / arXiv / URL | arXiv:2407.12784 — confirmed (Stage 1 metadata check) |
| Cited in | §2.3 Prompt Injection and Indirect Prompt Injection (L35) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (numbers used are in the abstract). |
| What the chapter uses | Used as an example of an attack that poisons agent memory or knowledge bases so that a trigger retrieves malicious demonstrations. |

#### 8. LlamaFirewall: An open source guardrail system for building secure AI agents

| Field | Value |
| --- | --- |
| Order in reference list | 8 |
| Stage 1 Ref ID | REF-010 |
| Authors | Chennabasappa, S., Nikolaidis, C., Song, D., Molnar, D., Ding, S., Wan, S., Whitman, S., Deason, L., Doucette, N., Montilla, A., Gampa, A., de Paola, B., Gabi, D., Crnkovich, J., Testud, J.-C., He, K., Chaturvedi, R., Zhou, W., & Saxe, J. |
| Year | 2025 |
| DOI / arXiv / URL | arXiv:2505.03574 — confirmed (Stage 1 metadata check) |
| Cited in | §2.4.3 Learned and LLM-based guardrails (L53); §2.8 Detection and Classification Approaches (L114) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (components). |
| What the chapter uses | Used to describe a guardrail built from PromptGuard 2, Agent Alignment Checks and CodeShield, and as the example of a classifier-based injection detector. |

#### 9. On optimum recognition error and reject tradeoff

| Field | Value |
| --- | --- |
| Order in reference list | 9 |
| Stage 1 Ref ID | REF-011 |
| Authors | Chow, C. K. |
| Year | 1970 |
| DOI / arXiv / URL | doi:10.1109/TIT.1970.1054406 — confirmed (Stage 1 metadata check) |
| Cited in | §2.10 Runtime Decision and Mitigation (L134) |
| Paper available locally | No |
| Verification status | **PARTIALLY VERIFIED** |
| Basis | Stage 1 and Stage 2: Crossref record matches every cited field. The reject rule was not read. |
| What the chapter uses | Used as the classical basis for withholding an automatic decision, through the error–reject tradeoff. |

#### 10. Defeating prompt injections by design

| Field | Value |
| --- | --- |
| Order in reference list | 10 |
| Stage 1 Ref ID | REF-015 |
| Authors | Debenedetti, E., Shumailov, I., Fan, T., Hayes, J., Carlini, N., Fabian, D., Kern, C., Shi, C., Terzis, A., & Tramèr, F. |
| Year | 2025 |
| DOI / arXiv / URL | arXiv:2503.18813 — confirmed (Stage 1 metadata check) |
| Cited in | §2.4.1 Defenses by construction (L45); §2.6 Tool-Use and Action-Boundary Security (L85); §2.13 Comparative Synthesis (L175) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (77% vs 84%). |
| What the chapter uses | Used as the defense-by-construction example (CaMeL), which enforces capability and data-flow policies so that untrusted data cannot change program behavior. |

#### 11. AgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents

| Field | Value |
| --- | --- |
| Order in reference list | 11 |
| Stage 1 Ref ID | REF-014 |
| Authors | Debenedetti, E., Zhang, J., Balunović, M., Beurer-Kellner, L., Fischer, M., & Tramèr, F. |
| Year | 2024 |
| DOI / arXiv / URL | arXiv:2406.13352 — confirmed (Stage 1 metadata check) |
| Cited in | §2.3 Prompt Injection and Indirect Prompt Injection (L33); §2.12 Evaluation Benchmarks and Datasets (L156) |
| Paper available locally | No (paper). During Stage 2 the agentdojo 0.1.35 package source was downloaded from PyPI into a temporary session directory; it is software, not the paper, and it is not in the repository. |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract; banking suite read in the public repository. |
| What the chapter uses | Used for the benchmark's scope (97 tasks, 629 security test cases, an e-banking environment) and for measuring utility and security together. |

#### 12. The foundations of cost-sensitive learning

| Field | Value |
| --- | --- |
| Order in reference list | 12 |
| Stage 1 Ref ID | REF-017 |
| Authors | Elkan, C. |
| Year | 2001 |
| DOI / arXiv / URL | Author PDF URL as cited (read in Stage 1). ACM DL record 10.5555/1642194.1642224 (Stage 2, index record). |
| Cited in | §2.10 Runtime Decision and Mitigation (L134) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: author PDF read (cost convention and Eq. 1). Stage 2: pp. 973–978 confirmed through dblp and ACM DL records. The printed threshold equation was not re-read; Chapter 3 says so itself. |
| What the chapter uses | Used for the principle that a prediction should minimize expected cost, computed from class probabilities and a cost matrix. |

#### 13. Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 laying down harmonised rules on artificial intelligence

| Field | Value |
| --- | --- |
| Order in reference list | 13 |
| Stage 1 Ref ID | REF-039 |
| Authors | European Parliament & Council of the European Union. |
| Year | 2024 |
| DOI / arXiv / URL | EUR-Lex URL as cited — UNVERIFIED: Stage 1 read the article text on a secondary host and did not confirm it against EUR-Lex. |
| Cited in | §2.7 Financial-Agent Security Requirements (L99); §2.11 Explainability and Auditability (L144) |
| Paper available locally | No |
| Verification status | **PARTIALLY VERIFIED** |
| Basis | Stage 1: Article text read on a secondary host; not confirmed against EUR-Lex. |
| What the chapter uses | Used for the regulatory requirements of automatic event logging (Art. 12) and effective human oversight, including intervention, in high-risk AI systems (Art. 14). |

#### 14. Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection

| Field | Value |
| --- | --- |
| Order in reference list | 14 |
| Stage 1 Ref ID | REF-019 |
| Authors | Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., & Fritz, M. |
| Year | 2023 |
| DOI / arXiv / URL | doi:10.1145/3605764.3623985 — confirmed (Stage 1 metadata check) |
| Cited in | §2.3 Prompt Injection and Indirect Prompt Injection (L31) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: Crossref metadata and arXiv abstract. |
| What the chapter uses | Used as the demonstration that instructions hidden in retrieved data can compromise LLM-integrated applications remotely (indirect prompt injection). |

#### 15. On calibration of modern neural networks

| Field | Value |
| --- | --- |
| Order in reference list | 15 |
| Stage 1 Ref ID | REF-020 |
| Authors | Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. |
| Year | 2017 |
| DOI / arXiv / URL | https://proceedings.mlr.press/v70/guo17a.html — confirmed (Stage 1 metadata check) |
| Cited in | §2.9 Probability Calibration (L122, L124) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: ar5iv full text: calibration definition, ECE bins, Platt form, NLL fit. |
| What the chapter uses | Used for the definition of calibration and ECE, and for describing Platt scaling as a two-parameter, ranking-preserving logistic map fitted by negative log-likelihood, alongside temperature scaling. |

#### 16. Defending against indirect prompt injection attacks with spotlighting

| Field | Value |
| --- | --- |
| Order in reference list | 16 |
| Stage 1 Ref ID | REF-022 |
| Authors | Hines, K., Lopez, G., Hall, M., Zarfati, F., Zunger, Y., & Kiciman, E. |
| Year | 2024 |
| DOI / arXiv / URL | arXiv:2403.14720 — confirmed (Stage 1 metadata check) |
| Cited in | §2.8 Detection and Classification Approaches (L114) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (>50% to <2%). |
| What the chapter uses | Used as the example of an input transformation (spotlighting) and its reported reduction of attack success from above 50% to below 2%. |

#### 17. NEXUS: Structured runtime safety for tool-using LLM agents

| Field | Value |
| --- | --- |
| Order in reference list | 17 |
| Stage 1 Ref ID | REF-023 |
| Authors | Hossain, E., Nipu, M. M. H., Ornee, T. N., Rana, R., & Yousefi, N. |
| Year | 2026 |
| DOI / arXiv / URL | arXiv:2607.19356 — identifier confirmed (Stage 1; Stage 2 index records). The submission date conflicts with it (Section 6). |
| Cited in | §2.4.4 Integrated runtime layers (L65); §2.9 Probability Calibration (L126); §2.10 Runtime Decision and Mitigation (L132, L134, L136); §2.11 Explainability and Auditability (L144); §2.12 Evaluation Benchmarks and Datasets (L161); §2.13 Comparative Synthesis (L185) |
| Paper available locally | No |
| Verification status | **PARTIALLY VERIFIED** |
| Basis | Stage 1: full HTML text read and claims marked supported, but the arXiv ID (2607 = July 2026) conflicts with the stated 25 May 2026 submission date (Stage 1 status CONFLICTED). Stage 2: title, five authors and ID confirmed in index records; full text not reachable in this environment. Four numerical claims and V-1 remain open (Section 6). |
| What the chapter uses | Used as the closest prior system: pre-execution plan checks that combine rules, argument inspection and a Platt-calibrated logistic risk score, a four-intervention policy run as a score-gated rule cascade, a defined expected-loss objective, and its reported benchmark figures. |

#### 18. Designing a policy engine for agentic AI systems: From governance requirements to runtime enforcement

| Field | Value |
| --- | --- |
| Order in reference list | 18 |
| Stage 1 Ref ID | REF-024 |
| Authors | Jackson, F. |
| Year | 2025 |
| DOI / arXiv / URL | doi:10.2139/ssrn.5904104 — registered, matches (Stage 2, Crossref). |
| Cited in | §2.10 Runtime Decision and Mitigation (L132) |
| Paper available locally | No |
| Verification status | **PARTIALLY VERIFIED** |
| Basis | Stage 2: DOI registered with Crossref; author, title, year and preprint status match. Full text not read (SSRN HTTP 403). (Stage 1: UNVERIFIED.) |
| What the chapter uses | Mentioned by title only, as a working paper that appears to address the same decision question; the chapter says its mechanism is not described and no claim rests on it. |

#### 19. FinHarness: An inline lifecycle safety harness for finance LLM agents

| Field | Value |
| --- | --- |
| Order in reference list | 19 |
| Stage 1 Ref ID | REF-025 |
| Authors | Jia, H., Liu, Y., Chong, B., Yang, Y., Chen, Y., Liang, J., Li, Q., Lu, H., Xu, K., Zheng, H., Zhang, C., Peng, H., & Yu, P. S. |
| Year | 2026 |
| DOI / arXiv / URL | arXiv:2605.27333 — confirmed (Stage 1 metadata check) |
| Cited in | §2.5 Stateful and Trajectory-Aware Protection (L73); §2.7 Financial-Agent Security Requirements (L97); §2.10 Runtime Decision and Mitigation (L132); §2.13 Comparative Synthesis (L183) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (components and numbers). |
| What the chapter uses | Used as the closest domain-specific (financial) runtime system, including its cross-interaction intent tracking and judge-routing decisions. |

#### 20. Think twice before you act: Enhancing agent behavioral safety with thought correction

| Field | Value |
| --- | --- |
| Order in reference list | 20 |
| Stage 1 Ref ID | REF-026 |
| Authors | Jiang, C., Zhang, W., Pan, X., Hong, G., & Yang, M. |
| Year | 2025 |
| DOI / arXiv / URL | arXiv:2505.11063 — confirmed (Stage 1 metadata check) |
| Cited in | §2.6 Tool-Use and Action-Boundary Security (L87) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract. |
| What the chapter uses | Used as an example of correcting unsafe intermediate thoughts before an action executes, with its reported safety improvement. |

#### 21. Beta calibration: A well-founded and easily implemented improvement on logistic calibration for binary classifiers

| Field | Value |
| --- | --- |
| Order in reference list | 21 |
| Stage 1 Ref ID | REF-027 |
| Authors | Kull, M., Silva Filho, T., & Flach, P. |
| Year | 2017 |
| DOI / arXiv / URL | https://proceedings.mlr.press/v54/kull17a.html — confirmed (Stage 1 metadata check) |
| Cited in | §2.9 Probability Calibration (L124) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: PMLR PDF text: monotonicity constraint and Proposition 1. |
| What the chapter uses | Used for the point that logistic calibration on unit-interval scores cannot represent the identity map, which motivates beta calibration. |

#### 22. OpenClaw PRISM: A zero-fork, defense-in-depth runtime security layer for tool-augmented LLM agents

| Field | Value |
| --- | --- |
| Order in reference list | 22 |
| Stage 1 Ref ID | REF-028 |
| Authors | Li, F. |
| Year | 2026 |
| DOI / arXiv / URL | arXiv:2603.11853 — confirmed (Stage 1 metadata check) |
| Cited in | §2.4.4 Integrated runtime layers (L57); §2.5 Stateful and Trajectory-Aware Protection (L73); §2.11 Explainability and Auditability (L144); §2.13 Comparative Synthesis (L180) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (40 benchmarks; W = 0.10). |
| What the chapter uses | Used as an integrated runtime layer with lifecycle hooks, heuristic and LLM scanning, decaying session-risk accumulation, and tamper-evident auditing. |

#### 23. Taxonomy and consistency analysis of safety benchmarks for AI agents

| Field | Value |
| --- | --- |
| Order in reference list | 23 |
| Stage 1 Ref ID | REF-029 |
| Authors | Li, M. Q., Fung, B. C. M., Li, B., Ismail, H., & Iqbal, F. |
| Year | 2026 |
| DOI / arXiv / URL | arXiv:2605.16282 — confirmed (Stage 1 metadata check) |
| Cited in | §2.8 Detection and Classification Approaches (L116); §2.12 Evaluation Benchmarks and Datasets (L163) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (hooks, TTL decay, preliminary results). |
| What the chapter uses | Used as evidence that the choice among 40 agent-safety benchmarks can produce contradictory safety conclusions. |

#### 24. DreamGuard: Efficient runtime guardrail for LLM agents via risk-aware world model

| Field | Value |
| --- | --- |
| Order in reference list | 24 |
| Stage 1 Ref ID | REF-030 |
| Authors | Lin, W., Yu, C., Lin, X., Cao, S., Chen, X., Xue, L., Yu, L., Sha, L., & Wu, C. |
| Year | 2026 |
| DOI / arXiv / URL | arXiv:2608.05695 — confirmed (Stage 1 metadata check) |
| Cited in | §2.5 Stateful and Trajectory-Aware Protection (L73) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (world model, ~25 ms). |
| What the chapter uses | Used as an example of detecting trajectory drift with a recurrent latent world model, with its reported per-evaluation latency. |

#### 25. SafeAgent: A runtime protection architecture for agentic systems

| Field | Value |
| --- | --- |
| Order in reference list | 25 |
| Stage 1 Ref ID | REF-032 |
| Authors | Liu, H., Ilyushin, E., Ni, J., & Zhu, M. |
| Year | 2026 |
| DOI / arXiv / URL | arXiv:2604.17562 — confirmed (Stage 1 metadata check) |
| Cited in | §2.4.4 Integrated runtime layers (L61); §2.5 Stateful and Trajectory-Aware Protection (L73); §2.10 Runtime Decision and Mitigation (L132, L136); §2.13 Comparative Synthesis (L186) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: Full HTML text read. |
| What the chapter uses | Used as a runtime controller that treats security as a stateful decision over session history and chooses among recovery actions by LLM-based arbitration. |

#### 26. Formalizing and benchmarking prompt injection attacks and defenses

| Field | Value |
| --- | --- |
| Order in reference list | 26 |
| Stage 1 Ref ID | REF-031 |
| Authors | Liu, Y., Jia, Y., Geng, R., Jia, J., & Gong, N. Z. |
| Year | 2024 |
| DOI / arXiv / URL | https://arxiv.org/abs/2310.12815 — confirmed (Stage 1 metadata check) |
| Cited in | §2.3 Prompt Injection and Indirect Prompt Injection (L31) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (5 attacks, 10 defences, 10 LLMs, 7 tasks). |
| What the chapter uses | Used as the framework that formalized prompt injection attacks and benchmarked five attacks and ten defenses. |

#### 27. A unified approach to interpreting model predictions

| Field | Value |
| --- | --- |
| Order in reference list | 27 |
| Stage 1 Ref ID | REF-034 |
| Authors | Lundberg, S. M., & Lee, S.-I. |
| Year | 2017 |
| DOI / arXiv / URL | https://arxiv.org/abs/1705.07874 — confirmed (Stage 1 metadata check) |
| Cited in | §2.11 Explainability and Auditability (L142) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: ar5iv full text: Properties 1-3, Theorem 1, Corollary 1. |
| What the chapter uses | Used for Shapley-value attribution and its linear-model case: coefficient times the feature's deviation from its expected value. |

#### 28. AGrail: A lifelong agent guardrail with effective and adaptive safety detection

| Field | Value |
| --- | --- |
| Order in reference list | 28 |
| Stage 1 Ref ID | REF-035 |
| Authors | Luo, W., Dai, S., Liu, X., Banerjee, S., Sun, H., Chen, M., & Xiao, C. |
| Year | 2025 |
| DOI / arXiv / URL | UNVERIFIED — the chapter cites no identifier and none is recorded in the repository. (Stage 1 checked the ACL Anthology page.) |
| Cited in | §2.4.3 Learned and LLM-based guardrails (L53) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: ACL Anthology page and arXiv abstract. |
| What the chapter uses | Used as a guardrail that keeps optimizing its safety checks after deployment. |

#### 29. Obtaining well calibrated probabilities using Bayesian binning

| Field | Value |
| --- | --- |
| Order in reference list | 29 |
| Stage 1 Ref ID | REF-037 |
| Authors | Naeini, M. P., Cooper, G., & Hauskrecht, M. |
| Year | 2015 |
| DOI / arXiv / URL | doi:10.1609/aaai.v29i1.9602 — confirmed (Stage 1 metadata check) |
| Cited in | §2.9 Probability Calibration (L122) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: PMC full text: ECE definition read. |
| What the chapter uses | Used for the binary-class definition of ECE. |

#### 30. LLM01:2025 Prompt injection

| Field | Value |
| --- | --- |
| Order in reference list | 30 |
| Stage 1 Ref ID | REF-042 |
| Authors | OWASP Gen AI Security Project. |
| Year | 2025 |
| DOI / arXiv / URL | https://genai.owasp.org/llmrisk/llm01-prompt-injection/ — confirmed (Stage 1 metadata check) |
| Cited in | §2.3 Prompt Injection and Indirect Prompt Injection (L29) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: Official page read. |
| What the chapter uses | Used for the distinction between direct and indirect prompt injection. |

#### 31. Continuous inspection schemes

| Field | Value |
| --- | --- |
| Order in reference list | 31 |
| Stage 1 Ref ID | REF-038 |
| Authors | Page, E. S. |
| Year | 1954 |
| DOI / arXiv / URL | doi:10.1093/biomet/41.1-2.100 — confirmed (Stage 1 metadata check) |
| Cited in | §2.5 Stateful and Trajectory-Aware Protection (L75) |
| Paper available locally | No |
| Verification status | **PARTIALLY VERIFIED** |
| Basis | Stage 1: Crossref metadata only. |
| What the chapter uses | Used as the origin of the CUSUM procedure. |

#### 32. Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods

| Field | Value |
| --- | --- |
| Order in reference list | 32 |
| Stage 1 Ref ID | REF-041 |
| Authors | Platt, J. C. |
| Year | 1999 |
| DOI / arXiv / URL | None cited. Stage 2 found the Crossref record 10.7551/mitpress/1113.003.0008 for the MIT Press chapter at pp. 61–74, titled "Probabilities for SV Machines" (2000). Its title and year differ from the citation. |
| Cited in | §2.9 Probability Calibration (L124) |
| Paper available locally | No |
| Verification status | **PARTIALLY VERIFIED** |
| Basis | Stage 2: Crossref locates a Platt chapter at pp. 61–74 of the MIT Press volume, but registered as "Probabilities for SV Machines" (2000), so the cited title and year do not match that record. Not read. (Stage 1: UNVERIFIED.) |
| What the chapter uses | Used as the origin of fitting a sigmoid to support-vector-machine outputs (Platt scaling). |

#### 33. Identifying the risks of LM agents with an LM-emulated sandbox

| Field | Value |
| --- | --- |
| Order in reference list | 33 |
| Stage 1 Ref ID | REF-044 |
| Authors | Ruan, Y., Dong, H., Wang, A., Pitis, S., Zhou, Y., Ba, J., Dubois, Y., Maddison, C. J., & Hashimoto, T. |
| Year | 2024 |
| DOI / arXiv / URL | arXiv:2309.15817 — confirmed (Stage 1 metadata check) |
| Cited in | §2.2 The AI-Agent Security Problem (L23); §2.12 Evaluation Benchmarks and Datasets (L159) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (36 toolkits, 144 cases, 23.9%, 68.8%). |
| What the chapter uses | Used as evidence that agents fail riskily even without an adversary (ToolEmu figures), and as a benchmark entry. |

#### 34. Safeguarding LLM agents from misalignment through provenance analysis

| Field | Value |
| --- | --- |
| Order in reference list | 34 |
| Stage 1 Ref ID | REF-045 |
| Authors | She, Y., Liang, Y., & Kang, E. |
| Year | 2026 |
| DOI / arXiv / URL | arXiv:2607.01236 — confirmed (Stage 1 metadata check) |
| Cited in | §2.6 Tool-Use and Action-Boundary Security (L85); §2.8 Detection and Classification Approaches (L114); §2.11 Explainability and Auditability (L144); §2.13 Comparative Synthesis (L182) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (44.3% to 2.1%). |
| What the chapter uses | Used as the approach that asks whether a proposed tool call is supported by traceable evidence in the agent's context. |

#### 35. Progent: Securing AI agents with privilege control

| Field | Value |
| --- | --- |
| Order in reference list | 35 |
| Stage 1 Ref ID | REF-046 |
| Authors | Shi, T., He, J., Wang, Z., Li, H., Wu, L., Guo, W., & Song, D. |
| Year | 2025 |
| DOI / arXiv / URL | arXiv:2504.11703 — confirmed (Stage 1 metadata check) |
| Cited in | §2.4.2 Deterministic policy enforcement (L49); §2.6 Tool-Use and Action-Boundary Security (L85); §2.13 Comparative Synthesis (L176) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract page (title, authors, mechanism). |
| What the chapter uses | Used as the example of explicit privilege-control policies over tool calls. |

#### 36. MI9: An integrated runtime governance framework for agentic AI

| Field | Value |
| --- | --- |
| Order in reference list | 36 |
| Stage 1 Ref ID | REF-048 |
| Authors | Wang, C. L., Singhal, T., Kelkar, A., & Tuo, J. |
| Year | 2025 |
| DOI / arXiv / URL | arXiv:2508.03858 — confirmed (Stage 1 metadata check) |
| Cited in | §2.4.4 Integrated runtime layers (L57); §2.5 Stateful and Trajectory-Aware Protection (L73); §2.10 Runtime Decision and Mitigation (L136); §2.13 Comparative Synthesis (L179) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (six components). |
| What the chapter uses | Used as a runtime governance framework with six components, including drift detection, conformance checking and graduated containment. |

#### 37. AgentSpec: Customizable runtime enforcement for safe and reliable LLM agents

| Field | Value |
| --- | --- |
| Order in reference list | 37 |
| Stage 1 Ref ID | REF-050 |
| Authors | Wang, H., Poskitt, C. M., & Sun, J. |
| Year | 2026 |
| DOI / arXiv / URL | https://arxiv.org/abs/2503.18666 — confirmed (Stage 1 metadata check) |
| Cited in | §2.4.2 Deterministic policy enforcement (L49); §2.6 Tool-Use and Action-Boundary Security (L85); §2.13 Comparative Synthesis (L177) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract page (numbers, journal reference). |
| What the chapter uses | Used as a domain-specific language of triggers, predicates and enforcement actions for tool-call policies. |

#### 38. ProbGuard: Proactive runtime monitoring for LLM agent safety via probabilistic prediction

| Field | Value |
| --- | --- |
| Order in reference list | 38 |
| Stage 1 Ref ID | REF-049 |
| Authors | Wang, H., Poskitt, C. M., Wei, J., & Sun, J. |
| Year | 2025 |
| DOI / arXiv / URL | arXiv:2508.00500 — confirmed (Stage 1 metadata check) |
| Cited in | §2.5 Stateful and Trajectory-Aware Protection (L73); §2.10 Runtime Decision and Mitigation (L132); §2.13 Comparative Synthesis (L181) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract page (DTMC prediction, venue). |
| What the chapter uses | Used as the example of modeling agent behavior as a discrete-time Markov chain and acting on thresholds over the predicted probability of reaching unsafe states. |

#### 39. A survey on large language model based autonomous agents

| Field | Value |
| --- | --- |
| Order in reference list | 39 |
| Stage 1 Ref ID | REF-047 |
| Authors | Wang, L., Ma, C., Feng, X., Zhang, Z., Yang, H., Zhang, J., Chen, Z., Tang, J., Chen, X., Lin, Y., Zhao, W. X., Wei, Z., & Wen, J. |
| Year | 2024 |
| DOI / arXiv / URL | doi:10.1007/s11704-024-40231-1 — confirmed (Stage 1 metadata check) |
| Cited in | §2.2 The AI-Agent Security Problem (L19) |
| Paper available locally | No |
| Verification status | **PARTIALLY VERIFIED** |
| Basis | Stage 1: Crossref metadata only. |
| What the chapter uses | Used for the definition of an LLM-based autonomous agent. |

#### 40. Safety, or just capability? A validity audit of agent-safety benchmarks

| Field | Value |
| --- | --- |
| Order in reference list | 40 |
| Stage 1 Ref ID | REF-051 |
| Authors | Wang, Y., Han, X., Shang, D., Tang, Y., & Liu, B. |
| Year | 2026 |
| DOI / arXiv / URL | arXiv:2607.28685 — confirmed (Stage 1 metadata check) |
| Cited in | §2.8 Detection and Classification Approaches (L116); §2.12 Evaluation Benchmarks and Datasets (L163) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract. |
| What the chapter uses | Used as evidence that metric flaws and small panels in agent-safety benchmarks produce inconsistent model rankings. |

#### 41. GuardAgent: Safeguard LLM agents by a guard agent via knowledge-enabled reasoning

| Field | Value |
| --- | --- |
| Order in reference list | 41 |
| Stage 1 Ref ID | REF-052 |
| Authors | Xiang, Z., Zheng, L., Li, Y., Hong, J., Li, Q., Xie, H., Zhang, J., Xiong, Z., Xie, C., Yang, C., Song, D., & Li, B. |
| Year | 2025 |
| DOI / arXiv / URL | arXiv:2406.09187 — confirmed (Stage 1 metadata check) |
| Cited in | §2.4.3 Learned and LLM-based guardrails (L53) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (98% and 83%). |
| What the chapter uses | Used as an example of converting safety requirements into executable guardrail code, with its reported accuracies. |

#### 42. AgentTrust: Runtime safety evaluation and interception for AI agent tool use

| Field | Value |
| --- | --- |
| Order in reference list | 42 |
| Stage 1 Ref ID | REF-053 |
| Authors | Yang, C. |
| Year | 2026 |
| DOI / arXiv / URL | arXiv:2605.04785 — confirmed (Stage 1 metadata check) |
| Cited in | §2.4.4 Integrated runtime layers (L63); §2.5 Stateful and Trajectory-Aware Protection (L77); §2.8 Detection and Classification Approaches (L114); §2.10 Runtime Decision and Mitigation (L132, L136); §2.11 Explainability and Auditability (L144); §2.13 Comparative Synthesis (L187) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: Full HTML text read. |
| What the chapter uses | Used as prior art for tool-use interception with rules and risk scoring, verdicts that include warn and review, rule-level audit output, and an ablation in which session tracking had no measurable effect. |

#### 43. FinVault: Benchmarking financial agent safety in execution-grounded environments

| Field | Value |
| --- | --- |
| Order in reference list | 43 |
| Stage 1 Ref ID | REF-054 |
| Authors | Yang, Z., Li, R., Qiang, Q., Wang, J., Lou, F., Li, M., Cheng, D., Xu, R., Lian, H., Zhang, S., Liang, X., Huang, X., Wei, Z., Liu, Z., Guo, X., Wang, H., Chen, R., & Zhang, L. |
| Year | 2026 |
| DOI / arXiv / URL | arXiv:2601.07853 — confirmed (Stage 1), including the withdrawal notice. |
| Cited in | §2.7 Financial-Agent Security Requirements (L95); §2.12 Evaluation Benchmarks and Datasets (L160) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract page including the withdrawal notice. |
| What the chapter uses | Described as an execution-grounded financial-agent benchmark whose arXiv version was withdrawn in July 2026; the chapter states it is not used in the thesis. |

#### 44. ReAct: Synergizing reasoning and acting in language models

| Field | Value |
| --- | --- |
| Order in reference list | 44 |
| Stage 1 Ref ID | REF-055 |
| Authors | Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. |
| Year | 2023 |
| DOI / arXiv / URL | https://arxiv.org/abs/2210.03629 — confirmed (Stage 1 metadata check) |
| Cited in | §2.2 The AI-Agent Security Problem (L19) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract page. |
| What the chapter uses | Used for the interleaved reasoning–action execution pattern that most of the reviewed systems assume. |

#### 45. InjecAgent: Benchmarking indirect prompt injections in tool-integrated large language model agents

| Field | Value |
| --- | --- |
| Order in reference list | 45 |
| Stage 1 Ref ID | REF-056 |
| Authors | Zhan, Q., Liang, Z., Ying, Z., & Kang, D. |
| Year | 2024 |
| DOI / arXiv / URL | https://arxiv.org/abs/2403.02691 — confirmed (Stage 1 metadata check) |
| Cited in | §2.3 Prompt Injection and Indirect Prompt Injection (L33); §2.12 Evaluation Benchmarks and Datasets (L157) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (1,054 cases; 24%). |
| What the chapter uses | Used for the composition of its indirect-injection test suite (1,054 cases, 17 user tools, 62 attacker tools). |

#### 46. Calibration is not control: Why LLM-agent oversight needs intervention

| Field | Value |
| --- | --- |
| Order in reference list | 46 |
| Stage 1 Ref ID | REF-058 |
| Authors | Zhang, C., Wan, Z., Yu, X., Wu, J., Wen, Q., Zhou, P., Zhao, W., & Tsang, I. |
| Year | 2026 |
| DOI / arXiv / URL | arXiv:2606.21399 — confirmed (Stage 1 metadata check) |
| Cited in | §2.9 Probability Calibration (L126); §2.10 Runtime Decision and Mitigation (L132, L138); §2.13 Comparative Synthesis (L188, L191); §2.15 Positioning of REM (L210) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: Full HTML text read. |
| What the chapter uses | Used for the argument that routing a scalar risk score through a threshold targets the wrong quantity (intervention advantage); REM's positioning states that it does not claim calibration improves control. |

#### 47. Agent Security Bench (ASB): Formalizing and benchmarking attacks and defenses in LLM-based agents

| Field | Value |
| --- | --- |
| Order in reference list | 47 |
| Stage 1 Ref ID | REF-057 |
| Authors | Zhang, H., Huang, J., Mei, K., Yao, Y., Wang, Z., Zhan, C., Wang, H., & Zhang, Y. |
| Year | 2025 |
| DOI / arXiv / URL | https://arxiv.org/abs/2410.02644 — confirmed (Stage 1 metadata check) |
| Cited in | §2.3 Prompt Injection and Indirect Prompt Injection (L33); §2.7 Financial-Agent Security Requirements (L97); §2.12 Evaluation Benchmarks and Datasets (L158) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (10 scenarios; 84.30%). |
| What the chapter uses | Used for its benchmark scope: 10 scenarios including finance, more than 400 tools, 27 attack and defense methods. |

## 2. Chapter 3 References

All 37 entries in the reference list of `working/Chapter3_working.md` (list starts at line 982), in the chapter's own order. Every entry is cited at least once in the text, and every in-text citation matches an entry.

#### 1. Dos and don'ts of machine learning in computer security

| Field | Value |
| --- | --- |
| Order in reference list | 1 |
| Stage 1 Ref ID | REF-001 |
| Authors | Arp, D., Quiring, E., Pendlebury, F., Warnecke, A., Pierazzi, F., Wressnegger, C., Cavallaro, L., & Rieck, K. |
| Year | 2022 |
| DOI / arXiv / URL | https://arxiv.org/abs/2010.09470 — confirmed (Stage 1 metadata check) |
| Cited in | §3.5 Detection Layer (L273); §3.11.6 Leakage controls (L709) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (claim used is in the abstract). |
| What the chapter uses | Supports the fragility of benchmark-based detector scores (§3.5) and motivates the leakage controls (§3.11.6). |

#### 2. Detection of abrupt changes: Theory and application

| Field | Value |
| --- | --- |
| Order in reference list | 2 |
| Stage 1 Ref ID | REF-002 |
| Authors | Basseville, M., & Nikiforov, I. V. |
| Year | 1993 |
| DOI / arXiv / URL | https://people.irisa.fr/Michele.Basseville/kniga/ — confirmed (Stage 1 metadata check) |
| Cited in | §3.11.10 Optional observe-only sequential analysis (L771, L775, L777); §3.13 Contribution and Novelty Boundaries (L881); §3.15 Equation Provenance Summary (L958, L959, L960) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: Author-hosted PDF text: eqs. 2.1.2, 2.2.8-2.2.10 read. |
| What the chapter uses | Source of the log-likelihood ratio, CUSUM statistic and alarm time in the optional observe-only sequential analysis (Eqs. 3.15–3.17). |

#### 3. Verification of forecasts expressed in terms of probability

| Field | Value |
| --- | --- |
| Order in reference list | 3 |
| Stage 1 Ref ID | REF-003 |
| Authors | Brier, G. W. |
| Year | 1950 |
| DOI / arXiv / URL | doi:10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2 — registered, matches (Stage 2, Crossref). |
| Cited in | §3.12.2 Secondary metrics (L845) |
| Paper available locally | No |
| Verification status | **PARTIALLY VERIFIED** |
| Basis | Stage 2: Crossref record matches every cited field. The paper was not read; Chapter 3 itself defers the Brier score until its convention is confirmed. (Stage 1: UNVERIFIED, publisher HTTP 403.) |
| What the chapter uses | Cited to say that the Brier score will not be reported until the original source's convention has been confirmed. |

#### 4. Insuring every action: An authority frontier framework for runtime actuarial control of autonomous AI agents

| Field | Value |
| --- | --- |
| Order in reference list | 4 |
| Stage 1 Ref ID | REF-008 |
| Authors | Chen, H.-H. |
| Year | 2026 |
| DOI / arXiv / URL | arXiv:2605.25632 — confirmed (Stage 1 metadata check) |
| Cited in | §3.13 Contribution and Novelty Boundaries (L887) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract. |
| What the chapter uses | Listed in the novelty-boundary table as prior art for consequence-aware and consequence-priced control. |

#### 5. LlamaFirewall: An open source guardrail system for building secure AI agents

| Field | Value |
| --- | --- |
| Order in reference list | 5 |
| Stage 1 Ref ID | REF-010 |
| Authors | Chennabasappa, S., Nikolaidis, C., Song, D., Molnar, D., Ding, S., Wan, S., Whitman, S., Deason, L., Doucette, N., Montilla, A., Gampa, A., de Paola, B., Gabi, D., Crnkovich, J., Testud, J.-C., He, K., Chaturvedi, R., Zhou, W., & Saxe, J. |
| Year | 2025 |
| DOI / arXiv / URL | arXiv:2505.03574 — confirmed (Stage 1 metadata check) |
| Cited in | §3.5 Detection Layer (L271) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (components). |
| What the chapter uses | Named as the source of a candidate injection classifier (PromptGuard 2) for the Detection Layer. |

#### 6. On optimum recognition error and reject tradeoff

| Field | Value |
| --- | --- |
| Order in reference list | 6 |
| Stage 1 Ref ID | REF-011 |
| Authors | Chow, C. K. |
| Year | 1970 |
| DOI / arXiv / URL | doi:10.1109/TIT.1970.1054406 — confirmed (Stage 1 metadata check) |
| Cited in | §3.7.5 Expected-loss verdict selection (L460); §3.13 Contribution and Novelty Boundaries (L882); §3.15 Equation Provenance Summary (L953) |
| Paper available locally | No |
| Verification status | **PARTIALLY VERIFIED** |
| Basis | Stage 1 and Stage 2: Crossref record matches every cited field. The reject rule was not read. |
| What the chapter uses | Conceptual basis for escalation as withholding an automatic decision (context of Eq. 3.10), and listed as prior art for the reject option. |

#### 7. The regression analysis of binary sequences

| Field | Value |
| --- | --- |
| Order in reference list | 7 |
| Stage 1 Ref ID | REF-012 |
| Authors | Cox, D. R. |
| Year | 1958 |
| DOI / arXiv / URL | doi:10.1111/j.2517-6161.1958.tb00292.x — confirmed (Stage 1 metadata check) |
| Cited in | §3.7.1 Ridge logistic estimation (L309, L316); §3.13 Contribution and Novelty Boundaries (L877); §3.15 Equation Provenance Summary (L944) |
| Paper available locally | No |
| Verification status | **PARTIALLY VERIFIED** |
| Basis | Stage 1 and Stage 2: Crossref record matches every cited field. The printed model formulation was not read. |
| What the chapter uses | Source of the logistic model (Eq. 3.1). |

#### 8. The relationship between precision-recall and ROC curves

| Field | Value |
| --- | --- |
| Order in reference list | 8 |
| Stage 1 Ref ID | REF-013 |
| Authors | Davis, J., & Goadrich, M. |
| Year | 2006 |
| DOI / arXiv / URL | doi:10.1145/1143844.1143874 — confirmed (Stage 1 metadata check) |
| Cited in | §3.12.2 Secondary metrics (L827) |
| Paper available locally | No |
| Verification status | **PARTIALLY VERIFIED** |
| Basis | Stage 1: Crossref metadata only. |
| What the chapter uses | Source for PR-AUC as a discrimination metric. |

#### 9. Defeating prompt injections by design

| Field | Value |
| --- | --- |
| Order in reference list | 9 |
| Stage 1 Ref ID | REF-015 |
| Authors | Debenedetti, E., Shumailov, I., Fan, T., Hayes, J., Carlini, N., Fabian, D., Kern, C., Shi, C., Terzis, A., & Tramèr, F. |
| Year | 2025 |
| DOI / arXiv / URL | arXiv:2503.18813 — confirmed (Stage 1 metadata check) |
| Cited in | §3.13 Contribution and Novelty Boundaries (L886) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (77% vs 84%). |
| What the chapter uses | Listed in the novelty-boundary table as prior art for provenance analysis of tool calls. |

#### 10. AgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents

| Field | Value |
| --- | --- |
| Order in reference list | 10 |
| Stage 1 Ref ID | REF-014 |
| Authors | Debenedetti, E., Zhang, J., Balunović, M., Beurer-Kellner, L., Fischer, M., & Tramèr, F. |
| Year | 2024 |
| DOI / arXiv / URL | arXiv:2406.13352 — confirmed (Stage 1 metadata check) |
| Cited in | §3.3.1 Protected system (L168); §3.11.1 Environment and instrumentation (L645) |
| Paper available locally | No (paper). During Stage 2 the agentdojo 0.1.35 package source was downloaded from PyPI into a temporary session directory; it is software, not the paper, and it is not in the repository. |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract; banking suite read in the public repository. |
| What the chapter uses | The evaluation environment: REM is evaluated on AgentDojo's banking suite. |

#### 11. Bootstrap methods: Another look at the jackknife

| Field | Value |
| --- | --- |
| Order in reference list | 11 |
| Stage 1 Ref ID | REF-016 |
| Authors | Efron, B. |
| Year | 1979 |
| DOI / arXiv / URL | doi:10.1214/aos/1176344552 — confirmed (Stage 1 metadata check) |
| Cited in | §3.11.9 Repeated runs and uncertainty (L761) |
| Paper available locally | No |
| Verification status | **PARTIALLY VERIFIED** |
| Basis | Stage 1: Crossref metadata only. |
| What the chapter uses | Source of the bootstrap resampling used for confidence intervals. |

#### 12. The foundations of cost-sensitive learning

| Field | Value |
| --- | --- |
| Order in reference list | 12 |
| Stage 1 Ref ID | REF-017 |
| Authors | Elkan, C. |
| Year | 2001 |
| DOI / arXiv / URL | Author PDF URL as cited (read in Stage 1). ACM DL record 10.5555/1642194.1642224 (Stage 2, index record). |
| Cited in | §3.7.5 Expected-loss verdict selection (L426, L456); §3.13 Contribution and Novelty Boundaries (L882); §3.15 Equation Provenance Summary (L949, L950, L952) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: author PDF read (cost convention and Eq. 1). Stage 2: pp. 973–978 confirmed through dblp and ACM DL records. The printed threshold equation was not re-read; Chapter 3 says so itself. |
| What the chapter uses | Source of the expected-cost criterion adapted into the conditional risk and Bayes verdict (Eqs. 3.6–3.7), and a consistency reference for the threshold form of Eq. 3.9. |

#### 13. An introduction to ROC analysis

| Field | Value |
| --- | --- |
| Order in reference list | 13 |
| Stage 1 Ref ID | REF-018 |
| Authors | Fawcett, T. |
| Year | 2006 |
| DOI / arXiv / URL | doi:10.1016/j.patrec.2005.10.010 — confirmed (Stage 1 metadata check) |
| Cited in | §3.12.2 Secondary metrics (L827) |
| Paper available locally | No |
| Verification status | **PARTIALLY VERIFIED** |
| Basis | Stage 1: Crossref metadata only. |
| What the chapter uses | Source for ROC-AUC as a discrimination metric. |

#### 14. Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection

| Field | Value |
| --- | --- |
| Order in reference list | 14 |
| Stage 1 Ref ID | REF-019 |
| Authors | Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., & Fritz, M. |
| Year | 2023 |
| DOI / arXiv / URL | doi:10.1145/3605764.3623985 — confirmed (Stage 1 metadata check) |
| Cited in | §3.1.5 Assumptions (L77); §3.3.3 Trust boundaries and untrusted content (L185) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: Crossref metadata and arXiv abstract. |
| What the chapter uses | Grounds the scoping assumption and the observation trust boundary in the indirect injection threat. |

#### 15. On calibration of modern neural networks

| Field | Value |
| --- | --- |
| Order in reference list | 15 |
| Stage 1 Ref ID | REF-020 |
| Authors | Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. |
| Year | 2017 |
| DOI / arXiv / URL | https://proceedings.mlr.press/v70/guo17a.html — confirmed (Stage 1 metadata check) |
| Cited in | §3.7.2 Calibration on the logit (L342, L344, L350); §3.12.2 Secondary metrics (L829, L835); §3.13 Contribution and Novelty Boundaries (L879); §3.15 Equation Provenance Summary (L946, L947, L963) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: ar5iv full text: calibration definition, ECE bins, Platt form, NLL fit. |
| What the chapter uses | Source of fitting calibration by negative log-likelihood (Eq. 3.4), the two-parameter logistic form in Eq. 3.3, and the equal-width binning for ECE (Eq. 3.20). |

#### 16. Design science in information systems research

| Field | Value |
| --- | --- |
| Order in reference list | 16 |
| Stage 1 Ref ID | REF-021 |
| Authors | Hevner, A. R., March, S. T., Park, J., & Ram, S. |
| Year | 2004 |
| DOI / arXiv / URL | doi:10.2307/25148625 — confirmed (Stage 1 metadata check) |
| Cited in | §3.1.1 Design science research (L9) |
| Paper available locally | No |
| Verification status | **PARTIALLY VERIFIED** |
| Basis | Stage 1: Crossref metadata only. |
| What the chapter uses | Source of the design science research framing of the thesis. |

#### 17. Defending against indirect prompt injection attacks with spotlighting

| Field | Value |
| --- | --- |
| Order in reference list | 17 |
| Stage 1 Ref ID | REF-022 |
| Authors | Hines, K., Lopez, G., Hall, M., Zarfati, F., Zunger, Y., & Kiciman, E. |
| Year | 2024 |
| DOI / arXiv / URL | arXiv:2403.14720 — confirmed (Stage 1 metadata check) |
| Cited in | §3.8 Mitigation Layer (L540) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (>50% to <2%). |
| What the chapter uses | Named as an input-sanitization alternative (spotlighting) that is not adopted as the primary mitigation mechanism. |

#### 18. NEXUS: Structured runtime safety for tool-using LLM agents

| Field | Value |
| --- | --- |
| Order in reference list | 18 |
| Stage 1 Ref ID | REF-023 |
| Authors | Hossain, E., Nipu, M. M. H., Ornee, T. N., Rana, R., & Yousefi, N. |
| Year | 2026 |
| DOI / arXiv / URL | arXiv:2607.19356 — identifier confirmed (Stage 1; Stage 2 index records). The submission date conflicts with it (Section 6). |
| Cited in | §3.7.2 Calibration on the logit (L356); §3.7.6 Explainability and audit record (L506); §3.13 Contribution and Novelty Boundaries (L883, L887) |
| Paper available locally | No |
| Verification status | **PARTIALLY VERIFIED** |
| Basis | Stage 1: full HTML text read and claims marked supported, but the arXiv ID (2607 = July 2026) conflicts with the stated 25 May 2026 submission date (Stage 1 status CONFLICTED). Stage 2: title, five authors and ID confirmed in index records; full text not reachable in this environment. Four numerical claims and V-1 remain open (Section 6). |
| What the chapter uses | Cited to say that calibrated logistic risk scores, four-way intervention and auditable decision records already exist and are therefore not claimed as contributions. |

#### 19. FinHarness: An inline lifecycle safety harness for finance LLM agents

| Field | Value |
| --- | --- |
| Order in reference list | 19 |
| Stage 1 Ref ID | REF-025 |
| Authors | Jia, H., Liu, Y., Chong, B., Yang, Y., Chen, Y., Liang, J., Li, Q., Lu, H., Xu, K., Zheng, H., Zhang, C., Peng, H., & Yu, P. S. |
| Year | 2026 |
| DOI / arXiv / URL | arXiv:2605.27333 — confirmed (Stage 1 metadata check) |
| Cited in | §3.13 Contribution and Novelty Boundaries (L889) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (components and numbers). |
| What the chapter uses | Listed as prior art for runtime protection of financial agents. |

#### 20. Beta calibration: A well-founded and easily implemented improvement on logistic calibration for binary classifiers

| Field | Value |
| --- | --- |
| Order in reference list | 20 |
| Stage 1 Ref ID | REF-027 |
| Authors | Kull, M., Silva Filho, T., & Flach, P. |
| Year | 2017 |
| DOI / arXiv / URL | https://proceedings.mlr.press/v54/kull17a.html — confirmed (Stage 1 metadata check) |
| Cited in | §3.7.2 Calibration on the logit (L342, L355); §3.13 Contribution and Novelty Boundaries (L879); §3.15 Equation Provenance Summary (L946) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: PMLR PDF text: monotonicity constraint and Proposition 1. |
| What the chapter uses | Source of the monotonicity condition, and of the proof that beta calibration with equal shape parameters equals logistic calibration on the log-odds (justification for Eq. 3.3). |

#### 21. Ridge estimators in logistic regression

| Field | Value |
| --- | --- |
| Order in reference list | 21 |
| Stage 1 Ref ID | REF-004 |
| Authors | le Cessie, S., & van Houwelingen, J. C. |
| Year | 1992 |
| DOI / arXiv / URL | doi:10.2307/2347628 — confirmed (Stage 1 metadata check) |
| Cited in | §3.7.1 Ridge logistic estimation (L318, L329); §3.13 Contribution and Novelty Boundaries (L878); §3.15 Equation Provenance Summary (L945) |
| Paper available locally | No |
| Verification status | **PARTIALLY VERIFIED** |
| Basis | Stage 1 and Stage 2: Crossref record matches (Crossref stores the first page only). The penalty formulation and its scaling constant were not read; Chapter 3 says so itself. |
| What the chapter uses | Source of the ridge-penalized log-likelihood (Eq. 3.2); the chapter notes that the penalty's scaling constant is pending full-text verification. |

#### 22. Taxonomy and consistency analysis of safety benchmarks for AI agents

| Field | Value |
| --- | --- |
| Order in reference list | 22 |
| Stage 1 Ref ID | REF-029 |
| Authors | Li, M. Q., Fung, B. C. M., Li, B., Ismail, H., & Iqbal, F. |
| Year | 2026 |
| DOI / arXiv / URL | arXiv:2605.16282 — confirmed (Stage 1 metadata check) |
| Cited in | §3.5 Detection Layer (L273); §3.14 Threats to Validity (L925) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (hooks, TTL decay, preliminary results). |
| What the chapter uses | Supports the fragility of benchmark-based detector scores and the threat that results may not transfer across benchmarks. |

#### 23. SafeAgent: A runtime protection architecture for agentic systems

| Field | Value |
| --- | --- |
| Order in reference list | 23 |
| Stage 1 Ref ID | REF-032 |
| Authors | Liu, H., Ilyushin, E., Ni, J., & Zhu, M. |
| Year | 2026 |
| DOI / arXiv / URL | arXiv:2604.17562 — confirmed (Stage 1 metadata check) |
| Cited in | §3.13 Contribution and Novelty Boundaries (L885) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: Full HTML text read. |
| What the chapter uses | Listed as prior art for runtime interception, human review and graduated response. |

#### 24. Procedures for reacting to a change in distribution

| Field | Value |
| --- | --- |
| Order in reference list | 24 |
| Stage 1 Ref ID | REF-033 |
| Authors | Lorden, G. |
| Year | 1971 |
| DOI / arXiv / URL | doi:10.1214/aoms/1177693055 — confirmed (Stage 1 metadata check) |
| Cited in | §3.11.10 Optional observe-only sequential analysis (L802) |
| Paper available locally | No |
| Verification status | **PARTIALLY VERIFIED** |
| Basis | Stage 1: Project Euclid abstract read 2026-09-22 (identity and asymptotic-optimality statement confirmed); independence and known-distribution assumptions not read. |
| What the chapter uses | Cited for the asymptotic optimality of CUSUM-type stopping rules. |

#### 25. A unified approach to interpreting model predictions

| Field | Value |
| --- | --- |
| Order in reference list | 25 |
| Stage 1 Ref ID | REF-034 |
| Authors | Lundberg, S. M., & Lee, S.-I. |
| Year | 2017 |
| DOI / arXiv / URL | https://arxiv.org/abs/1705.07874 — confirmed (Stage 1 metadata check) |
| Cited in | §3.7.6 Explainability and audit record (L481, L487, L493); §3.13 Contribution and Novelty Boundaries (L880); §3.15 Equation Provenance Summary (L954, L955) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: ar5iv full text: Properties 1-3, Theorem 1, Corollary 1. |
| What the chapter uses | Source of the linear Shapley attribution (Eq. 3.11) and the local-accuracy identity (Eq. 3.12) in the audit record; the chapter notes an index mismatch in the printed formula. |

#### 26. Optimal stopping times for detecting changes in distributions

| Field | Value |
| --- | --- |
| Order in reference list | 26 |
| Stage 1 Ref ID | REF-036 |
| Authors | Moustakides, G. V. |
| Year | 1986 |
| DOI / arXiv / URL | doi:10.1214/aos/1176350164 — confirmed (Stage 1 metadata check) |
| Cited in | §3.11.10 Optional observe-only sequential analysis (L802) |
| Paper available locally | No |
| Verification status | **PARTIALLY VERIFIED** |
| Basis | Stage 1: Project Euclid abstract read 2026-09-22 (identity confirmed; Page's stopping time shown optimal in a defined sense); assumptions not read. |
| What the chapter uses | Cited for the stronger optimality of Page's stopping time. |

#### 27. Obtaining well calibrated probabilities using Bayesian binning

| Field | Value |
| --- | --- |
| Order in reference list | 27 |
| Stage 1 Ref ID | REF-037 |
| Authors | Naeini, M. P., Cooper, G., & Hauskrecht, M. |
| Year | 2015 |
| DOI / arXiv / URL | doi:10.1609/aaai.v29i1.9602 — confirmed (Stage 1 metadata check) |
| Cited in | §3.12.2 Secondary metrics (L829, L835); §3.15 Equation Provenance Summary (L963) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: PMC full text: ECE definition read. |
| What the chapter uses | Source of the binary form of ECE (Eq. 3.20). |

#### 28. LLM01:2025 Prompt injection

| Field | Value |
| --- | --- |
| Order in reference list | 28 |
| Stage 1 Ref ID | REF-042 |
| Authors | OWASP Gen AI Security Project. |
| Year | 2025 |
| DOI / arXiv / URL | https://genai.owasp.org/llmrisk/llm01-prompt-injection/ — confirmed (Stage 1 metadata check) |
| Cited in | §3.3.3 Trust boundaries and untrusted content (L185); §3.3.5 Indirect injection and adversarially induced actions (L202) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: Official page read. |
| What the chapter uses | Source of the definition of indirect prompt injection and of the trust-boundary rationale. |

#### 29. Continuous inspection schemes

| Field | Value |
| --- | --- |
| Order in reference list | 29 |
| Stage 1 Ref ID | REF-038 |
| Authors | Page, E. S. |
| Year | 1954 |
| DOI / arXiv / URL | doi:10.1093/biomet/41.1-2.100 — confirmed (Stage 1 metadata check) |
| Cited in | §3.11.10 Optional observe-only sequential analysis (L777); §3.13 Contribution and Novelty Boundaries (L881); §3.15 Equation Provenance Summary (L959) |
| Paper available locally | No |
| Verification status | **PARTIALLY VERIFIED** |
| Basis | Stage 1: Crossref metadata only. |
| What the chapter uses | Source of the CUSUM recursion (Eq. 3.16). |

#### 30. A design science research methodology for information systems research

| Field | Value |
| --- | --- |
| Order in reference list | 30 |
| Stage 1 Ref ID | REF-040 |
| Authors | Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. |
| Year | 2007 |
| DOI / arXiv / URL | doi:10.2753/MIS0742-1222240302 — confirmed (Stage 1 metadata check) |
| Cited in | §3.1.1 Design science research (L9, L13) |
| Paper available locally | No |
| Verification status | **PARTIALLY VERIFIED** |
| Basis | Stage 1: Crossref metadata only. |
| What the chapter uses | Source of the six-activity design science research methodology that structures the research process (table in §3.1.1). |

#### 31. Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods

| Field | Value |
| --- | --- |
| Order in reference list | 31 |
| Stage 1 Ref ID | REF-041 |
| Authors | Platt, J. C. |
| Year | 1999 |
| DOI / arXiv / URL | None cited. Stage 2 found the Crossref record 10.7551/mitpress/1113.003.0008 for the MIT Press chapter at pp. 61–74, titled "Probabilities for SV Machines" (2000). Its title and year differ from the citation. |
| Cited in | §3.7.2 Calibration on the logit (L342); §3.13 Contribution and Novelty Boundaries (L879); §3.15 Equation Provenance Summary (L946) |
| Paper available locally | No |
| Verification status | **PARTIALLY VERIFIED** |
| Basis | Stage 2: Crossref locates a Platt chapter at pp. 61–74 of the MIT Press volume, but registered as "Probabilities for SV Machines" (2000), so the cited title and year do not match that record. Not read. (Stage 1: UNVERIFIED.) |
| What the chapter uses | Named as the origin of the Platt scaling method adapted in Eq. 3.3. |

#### 32. A CUSUM chart for monitoring a proportion when inspecting continuously

| Field | Value |
| --- | --- |
| Order in reference list | 32 |
| Stage 1 Ref ID | REF-043 |
| Authors | Reynolds, M. R., Jr., & Stoumbos, Z. G. |
| Year | 1999 |
| DOI / arXiv / URL | doi:10.1080/00224065.1999.11979900 — confirmed (Stage 1 metadata check) |
| Cited in | §3.11.10 Optional observe-only sequential analysis (L775); §3.15 Equation Provenance Summary (L958) |
| Paper available locally | No |
| Verification status | **PARTIALLY VERIFIED** |
| Basis | Stage 1: Crossref metadata only. |
| What the chapter uses | Cited for CUSUM charts on Bernoulli observations (context of Eq. 3.15). |

#### 33. Safeguarding LLM agents from misalignment through provenance analysis

| Field | Value |
| --- | --- |
| Order in reference list | 33 |
| Stage 1 Ref ID | REF-045 |
| Authors | She, Y., Liang, Y., & Kang, E. |
| Year | 2026 |
| DOI / arXiv / URL | arXiv:2607.01236 — confirmed (Stage 1 metadata check) |
| Cited in | §3.13 Contribution and Novelty Boundaries (L886) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (44.3% to 2.1%). |
| What the chapter uses | Listed as prior art for provenance analysis of tool calls. |

#### 34. MI9: An integrated runtime governance framework for agentic AI

| Field | Value |
| --- | --- |
| Order in reference list | 34 |
| Stage 1 Ref ID | REF-048 |
| Authors | Wang, C. L., Singhal, T., Kelkar, A., & Tuo, J. |
| Year | 2025 |
| DOI / arXiv / URL | arXiv:2508.03858 — confirmed (Stage 1 metadata check) |
| Cited in | §3.13 Contribution and Novelty Boundaries (L885) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract (six components). |
| What the chapter uses | Listed as prior art for runtime interception, human review and graduated response. |

#### 35. Safety, or just capability? A validity audit of agent-safety benchmarks

| Field | Value |
| --- | --- |
| Order in reference list | 35 |
| Stage 1 Ref ID | REF-051 |
| Authors | Wang, Y., Han, X., Shang, D., Tang, Y., & Liu, B. |
| Year | 2026 |
| DOI / arXiv / URL | arXiv:2607.28685 — confirmed (Stage 1 metadata check) |
| Cited in | §3.12.1 Primary metrics (L823); §3.14 Threats to Validity (L916) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: arXiv abstract. |
| What the chapter uses | Supports reporting utility alongside attack success rate, because a low attack success rate can reflect task failure. |

#### 36. AgentTrust: Runtime safety evaluation and interception for AI agent tool use

| Field | Value |
| --- | --- |
| Order in reference list | 36 |
| Stage 1 Ref ID | REF-053 |
| Authors | Yang, C. |
| Year | 2026 |
| DOI / arXiv / URL | arXiv:2605.04785 — confirmed (Stage 1 metadata check) |
| Cited in | §3.7.6 Explainability and audit record (L506); §3.13 Contribution and Novelty Boundaries (L885, L887, L888) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: Full HTML text read. |
| What the chapter uses | Cited to say that auditable decision records, consequence-aware control and component ablation with latency already exist. |

#### 37. Calibration is not control: Why LLM-agent oversight needs intervention

| Field | Value |
| --- | --- |
| Order in reference list | 37 |
| Stage 1 Ref ID | REF-058 |
| Authors | Zhang, C., Wan, Z., Yu, X., Wu, J., Wen, Q., Zhou, P., Zhao, W., & Tsang, I. |
| Year | 2026 |
| DOI / arXiv / URL | arXiv:2606.21399 — confirmed (Stage 1 metadata check) |
| Cited in | §3.7.2 Calibration on the logit (L357); §3.7.7 Consequence-independent baseline policy (L525); §3.13 Contribution and Novelty Boundaries (L884); §3.14 Threats to Validity (L936) |
| Paper available locally | No |
| Verification status | **VERIFIED** |
| Basis | Stage 1: Full HTML text read. |
| What the chapter uses | Used to state that recalibration need not change threshold-routed control, a limitation REM inherits, and listed as prior art for the calibration–control distinction. |

## 3. Shared References

**26 references appear in both chapters.** Ch2 lists 47, Ch3 lists 37 and 26 are shared, giving 47 + 37 − 26 = **58 unique references**. That matches the 58 rows of the Stage 1 reference master.

| Ref ID | Citation | Ch2 # | Ch3 # | Status | Chapter 2 sections | Chapter 3 sections |
| --- | --- | :---: | :---: | --- | --- | --- |
| REF-001 | Arp et al. (2022) | 1 | 1 | VERIFIED | §2.8 Detection and Classification Approaches | §3.5 Detection Layer; §3.11.6 Leakage controls |
| REF-002 | Basseville & Nikiforov (1993) | 2 | 2 | VERIFIED | §2.5 Stateful and Trajectory-Aware Protection | §3.11.10 Optional observe-only sequential analysis; §3.13 Contribution and Novelty Boundaries; §3.15 Equation Provenance Summary |
| REF-008 | H.-H. Chen (2026) | 3 | 4 | VERIFIED | §2.6 Tool-Use and Action-Boundary Security; §2.7 Financial-Agent Security Requirements; §2.10 Runtime Decision and Mitigation; §2.13 Comparative Synthesis; §2.15 Positioning of REM | §3.13 Contribution and Novelty Boundaries |
| REF-010 | Chennabasappa et al. (2025) | 8 | 5 | VERIFIED | §2.4.3 Learned and LLM-based guardrails; §2.8 Detection and Classification Approaches | §3.5 Detection Layer |
| REF-011 | Chow (1970) | 9 | 6 | PARTIALLY VERIFIED | §2.10 Runtime Decision and Mitigation | §3.7.5 Expected-loss verdict selection; §3.13 Contribution and Novelty Boundaries; §3.15 Equation Provenance Summary |
| REF-015 | Debenedetti et al. (2025) | 10 | 9 | VERIFIED | §2.4.1 Defenses by construction; §2.6 Tool-Use and Action-Boundary Security; §2.13 Comparative Synthesis | §3.13 Contribution and Novelty Boundaries |
| REF-014 | Debenedetti et al. (2024) | 11 | 10 | VERIFIED | §2.3 Prompt Injection and Indirect Prompt Injection; §2.12 Evaluation Benchmarks and Datasets | §3.3.1 Protected system; §3.11.1 Environment and instrumentation |
| REF-017 | Elkan (2001) | 12 | 12 | VERIFIED | §2.10 Runtime Decision and Mitigation | §3.7.5 Expected-loss verdict selection; §3.13 Contribution and Novelty Boundaries; §3.15 Equation Provenance Summary |
| REF-019 | Greshake et al. (2023) | 14 | 14 | VERIFIED | §2.3 Prompt Injection and Indirect Prompt Injection | §3.1.5 Assumptions; §3.3.3 Trust boundaries and untrusted content |
| REF-020 | Guo et al. (2017) | 15 | 15 | VERIFIED | §2.9 Probability Calibration | §3.7.2 Calibration on the logit; §3.12.2 Secondary metrics; §3.13 Contribution and Novelty Boundaries; §3.15 Equation Provenance Summary |
| REF-022 | Hines et al. (2024) | 16 | 17 | VERIFIED | §2.8 Detection and Classification Approaches | §3.8 Mitigation Layer |
| REF-023 | Hossain et al. (2026) | 17 | 18 | PARTIALLY VERIFIED | §2.4.4 Integrated runtime layers; §2.9 Probability Calibration; §2.10 Runtime Decision and Mitigation; §2.11 Explainability and Auditability; §2.12 Evaluation Benchmarks and Datasets; §2.13 Comparative Synthesis | §3.7.2 Calibration on the logit; §3.7.6 Explainability and audit record; §3.13 Contribution and Novelty Boundaries |
| REF-025 | Jia et al. (2026) | 19 | 19 | VERIFIED | §2.5 Stateful and Trajectory-Aware Protection; §2.7 Financial-Agent Security Requirements; §2.10 Runtime Decision and Mitigation; §2.13 Comparative Synthesis | §3.13 Contribution and Novelty Boundaries |
| REF-027 | Kull et al. (2017) | 21 | 20 | VERIFIED | §2.9 Probability Calibration | §3.7.2 Calibration on the logit; §3.13 Contribution and Novelty Boundaries; §3.15 Equation Provenance Summary |
| REF-029 | M. Q. Li et al. (2026) | 23 | 22 | VERIFIED | §2.8 Detection and Classification Approaches; §2.12 Evaluation Benchmarks and Datasets | §3.5 Detection Layer; §3.14 Threats to Validity |
| REF-032 | H. Liu et al. (2026) | 25 | 23 | VERIFIED | §2.4.4 Integrated runtime layers; §2.5 Stateful and Trajectory-Aware Protection; §2.10 Runtime Decision and Mitigation; §2.13 Comparative Synthesis | §3.13 Contribution and Novelty Boundaries |
| REF-034 | Lundberg & Lee (2017) | 27 | 25 | VERIFIED | §2.11 Explainability and Auditability | §3.7.6 Explainability and audit record; §3.13 Contribution and Novelty Boundaries; §3.15 Equation Provenance Summary |
| REF-037 | Naeini et al. (2015) | 29 | 27 | VERIFIED | §2.9 Probability Calibration | §3.12.2 Secondary metrics; §3.15 Equation Provenance Summary |
| REF-042 | OWASP Gen AI Security Project (2025) | 30 | 28 | VERIFIED | §2.3 Prompt Injection and Indirect Prompt Injection | §3.3.3 Trust boundaries and untrusted content; §3.3.5 Indirect injection and adversarially induced actions |
| REF-038 | Page (1954) | 31 | 29 | PARTIALLY VERIFIED | §2.5 Stateful and Trajectory-Aware Protection | §3.11.10 Optional observe-only sequential analysis; §3.13 Contribution and Novelty Boundaries; §3.15 Equation Provenance Summary |
| REF-041 | Platt (1999) | 32 | 31 | PARTIALLY VERIFIED | §2.9 Probability Calibration | §3.7.2 Calibration on the logit; §3.13 Contribution and Novelty Boundaries; §3.15 Equation Provenance Summary |
| REF-045 | She et al. (2026) | 34 | 33 | VERIFIED | §2.6 Tool-Use and Action-Boundary Security; §2.8 Detection and Classification Approaches; §2.11 Explainability and Auditability; §2.13 Comparative Synthesis | §3.13 Contribution and Novelty Boundaries |
| REF-048 | C. L. Wang et al. (2025) | 36 | 34 | VERIFIED | §2.4.4 Integrated runtime layers; §2.5 Stateful and Trajectory-Aware Protection; §2.10 Runtime Decision and Mitigation; §2.13 Comparative Synthesis | §3.13 Contribution and Novelty Boundaries |
| REF-051 | Y. Wang et al. (2026) | 40 | 35 | VERIFIED | §2.8 Detection and Classification Approaches; §2.12 Evaluation Benchmarks and Datasets | §3.12.1 Primary metrics; §3.14 Threats to Validity |
| REF-053 | C. Yang (2026) | 42 | 36 | VERIFIED | §2.4.4 Integrated runtime layers; §2.5 Stateful and Trajectory-Aware Protection; §2.8 Detection and Classification Approaches; §2.10 Runtime Decision and Mitigation; §2.11 Explainability and Auditability; §2.13 Comparative Synthesis | §3.7.6 Explainability and audit record; §3.13 Contribution and Novelty Boundaries |
| REF-058 | C. Zhang et al. (2026) | 46 | 37 | VERIFIED | §2.9 Probability Calibration; §2.10 Runtime Decision and Mitigation; §2.13 Comparative Synthesis; §2.15 Positioning of REM | §3.7.2 Calibration on the logit; §3.7.7 Consequence-independent baseline policy; §3.13 Contribution and Novelty Boundaries; §3.14 Threats to Validity |

**Chapter 2 only (21):** Z. Chen, J. Chen, et al. (2025); Z. Chen, Kang, & Li (2025); Z. Chen et al. (2026); Z. Chen et al. (2024); European Parliament & Council of the EU (2024); Jackson (2025); Jiang et al. (2025); F. Li (2026); Lin et al. (2026); Y. Liu et al. (2024); Luo et al. (2025); Ruan et al. (2024); Shi et al. (2025); H. Wang et al. (2026); H. Wang et al. (2025); L. Wang et al. (2024); Xiang et al. (2025); Z. Yang et al. (2026); Yao et al. (2023); Zhan et al. (2024); H. Zhang et al. (2025).

**Chapter 3 only (11):** Brier (1950); Cox (1958); Davis & Goadrich (2006); Efron (1979); Fawcett (2006); Hevner et al. (2004); le Cessie & van Houwelingen (1992); Lorden (1971); Moustakides (1986); Peffers et al. (2007); Reynolds & Stoumbos (1999).

---

## 4. Core Papers for REM

Papers grouped by the eight topics requested. **The groups are not ranked, and the order within each group is alphabetical by first author.** Each paper appears under one topic, the one that best matches how the chapters use it. That is not always the section where it is first cited: H.-H. Chen (2026) is first cited in §2.6, C. Zhang et al. (2026) in §2.9 and FinHarness in §2.5. Many papers are cited in several sections, and the cards in Sections 1–2 give the full list.

### 4.1 Runtime agent security

Integrated runtime layers and guardrails that sit between an agent and its actions (Ch2 §2.4.3–§2.4.4).

- **Z. Chen, Kang, & Li (2025)** — *ShieldAgent: Shielding agents via verifiable safety policy reasoning*. REF-007; Ch2 #5; VERIFIED.
- **Chennabasappa et al. (2025)** — *LlamaFirewall: An open source guardrail system for building secure AI agents*. REF-010; Ch2 #8 · Ch3 #5; VERIFIED.
- **Hossain et al. (2026)** — *NEXUS: Structured runtime safety for tool-using LLM agents*. REF-023; Ch2 #17 · Ch3 #18; PARTIALLY VERIFIED.
- **Jackson (2025)** — *Designing a policy engine for agentic AI systems: From governance requirements to runtime enforcement*. REF-024; Ch2 #18; PARTIALLY VERIFIED. Title-level mention only; Chapter 2 states that no claim rests on it.
- **F. Li (2026)** — *OpenClaw PRISM: A zero-fork, defense-in-depth runtime security layer for tool-augmented LLM agents*. REF-028; Ch2 #22; VERIFIED.
- **H. Liu et al. (2026)** — *SafeAgent: A runtime protection architecture for agentic systems*. REF-032; Ch2 #25 · Ch3 #23; VERIFIED.
- **Luo et al. (2025)** — *AGrail: A lifelong agent guardrail with effective and adaptive safety detection*. REF-035; Ch2 #28; VERIFIED.
- **C. L. Wang et al. (2025)** — *MI9: An integrated runtime governance framework for agentic AI*. REF-048; Ch2 #36 · Ch3 #34; VERIFIED.
- **Xiang et al. (2025)** — *GuardAgent: Safeguard LLM agents by a guard agent via knowledge-enabled reasoning*. REF-052; Ch2 #41; VERIFIED.
- **C. Yang (2026)** — *AgentTrust: Runtime safety evaluation and interception for AI agent tool use*. REF-053; Ch2 #42 · Ch3 #36; VERIFIED.

### 4.2 Prompt injection / indirect prompt injection

The attack class REM defends against, and defenses that act on the injected content (Ch2 §2.3, §2.4.1, §2.8).

- **Z. Chen et al. (2024)** — *AgentPoison: Red-teaming LLM agents via poisoning memory or knowledge bases*. REF-005; Ch2 #7; VERIFIED.
- **Debenedetti et al. (2025)** — *Defeating prompt injections by design*. REF-015; Ch2 #10 · Ch3 #9; VERIFIED.
- **Greshake et al. (2023)** — *Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection*. REF-019; Ch2 #14 · Ch3 #14; VERIFIED.
- **Hines et al. (2024)** — *Defending against indirect prompt injection attacks with spotlighting*. REF-022; Ch2 #16 · Ch3 #17; VERIFIED.
- **Y. Liu et al. (2024)** — *Formalizing and benchmarking prompt injection attacks and defenses*. REF-031; Ch2 #26; VERIFIED.
- **Zhan et al. (2024)** — *InjecAgent: Benchmarking indirect prompt injections in tool-integrated large language model agents*. REF-056; Ch2 #45; VERIFIED.
- **H. Zhang et al. (2025)** — *Agent Security Bench (ASB): Formalizing and benchmarking attacks and defenses in LLM-based agents*. REF-057; Ch2 #47; VERIFIED.

### 4.3 Tool-use security

Controls applied at the tool-call boundary (Ch2 §2.4.2, §2.6).

- **Z. Chen et al. (2026)** — *Cordon: Semantic transactions for tool-using LLM agents*. REF-009; Ch2 #6; VERIFIED.
- **Jiang et al. (2025)** — *Think twice before you act: Enhancing agent behavioral safety with thought correction*. REF-026; Ch2 #20; VERIFIED.
- **She et al. (2026)** — *Safeguarding LLM agents from misalignment through provenance analysis*. REF-045; Ch2 #34 · Ch3 #33; VERIFIED.
- **Shi et al. (2025)** — *Progent: Securing AI agents with privilege control*. REF-046; Ch2 #35; VERIFIED.
- **H. Wang et al. (2026)** — *AgentSpec: Customizable runtime enforcement for safe and reliable LLM agents*. REF-050; Ch2 #37; VERIFIED.

### 4.4 Behavioral analysis

Stateful or trajectory-level monitoring of agent behavior (Ch2 §2.5).

- **Lin et al. (2026)** — *DreamGuard: Efficient runtime guardrail for LLM agents via risk-aware world model*. REF-030; Ch2 #24; VERIFIED.
- **H. Wang et al. (2025)** — *ProbGuard: Proactive runtime monitoring for LLM agent safety via probabilistic prediction*. REF-049; Ch2 #38; VERIFIED.

### 4.5 Risk scoring / calibration

The estimator behind REM's probability and its calibration (Ch2 §2.9; Ch3 §3.7.1–§3.7.2, §3.12.2).

- **Brier (1950)** — *Verification of forecasts expressed in terms of probability*. REF-003; Ch3 #3; PARTIALLY VERIFIED. Chapter 3 defers the Brier score until its convention is confirmed.
- **le Cessie & van Houwelingen (1992)** — *Ridge estimators in logistic regression*. REF-004; Ch3 #21; PARTIALLY VERIFIED.
- **Cox (1958)** — *The regression analysis of binary sequences*. REF-012; Ch3 #7; PARTIALLY VERIFIED.
- **Guo et al. (2017)** — *On calibration of modern neural networks*. REF-020; Ch2 #15 · Ch3 #15; VERIFIED.
- **Kull et al. (2017)** — *Beta calibration: A well-founded and easily implemented improvement on logistic calibration for binary classifiers*. REF-027; Ch2 #21 · Ch3 #20; VERIFIED.
- **Naeini et al. (2015)** — *Obtaining well calibrated probabilities using Bayesian binning*. REF-037; Ch2 #29 · Ch3 #27; VERIFIED.
- **Platt (1999)** — *Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods*. REF-041; Ch2 #32 · Ch3 #31; PARTIALLY VERIFIED.

### 4.6 Sequential anomaly / change detection

CUSUM and its optimality results. In REM this is optional and observe-only (Ch2 §2.5; Ch3 §3.11.10).

- **Basseville & Nikiforov (1993)** — *Detection of abrupt changes: Theory and application*. REF-002; Ch2 #2 · Ch3 #2; VERIFIED.
- **Lorden (1971)** — *Procedures for reacting to a change in distribution*. REF-033; Ch3 #24; PARTIALLY VERIFIED.
- **Moustakides (1986)** — *Optimal stopping times for detecting changes in distributions*. REF-036; Ch3 #26; PARTIALLY VERIFIED.
- **Page (1954)** — *Continuous inspection schemes*. REF-038; Ch2 #31 · Ch3 #29; PARTIALLY VERIFIED.
- **Reynolds & Stoumbos (1999)** — *A CUSUM chart for monitoring a proportion when inspecting continuously*. REF-043; Ch3 #32; PARTIALLY VERIFIED.

### 4.7 Decision / mitigation mechanisms

Turning a probability and consequences into a verdict (Ch2 §2.9–§2.10; Ch3 §3.7.5).

- **H.-H. Chen (2026)** — *Insuring every action: An authority frontier framework for runtime actuarial control of autonomous AI agents*. REF-008; Ch2 #3 · Ch3 #4; VERIFIED.
- **Chow (1970)** — *On optimum recognition error and reject tradeoff*. REF-011; Ch2 #9 · Ch3 #6; PARTIALLY VERIFIED.
- **Elkan (2001)** — *The foundations of cost-sensitive learning*. REF-017; Ch2 #12 · Ch3 #12; VERIFIED.
- **C. Zhang et al. (2026)** — *Calibration is not control: Why LLM-agent oversight needs intervention*. REF-058; Ch2 #46 · Ch3 #37; VERIFIED.

### 4.8 Financial or banking agent security

The domain and its evaluation (Ch2 §2.7, §2.12; Ch3 §3.11).

- **Z. Chen, J. Chen, et al. (2025)** — *Standard benchmarks fail — Auditing LLM agents in finance must prioritize risk*. REF-006; Ch2 #4; VERIFIED.
- **Debenedetti et al. (2024)** — *AgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents*. REF-014; Ch2 #11 · Ch3 #10; VERIFIED. AgentDojo's banking suite is REM's evaluation environment.
- **Jia et al. (2026)** — *FinHarness: An inline lifecycle safety harness for finance LLM agents*. REF-025; Ch2 #19 · Ch3 #19; VERIFIED.
- **Z. Yang et al. (2026)** — *FinVault: Benchmarking financial agent safety in execution-grounded environments*. REF-054; Ch2 #43; VERIFIED. Withdrawn preprint; Chapter 2 states it is not used in the thesis.

### Not placed in a Section 4 topic (14)

These fall outside the eight requested topics, or are not papers. They are listed so that no reference silently disappears from this section.

- **Arp et al. (2022)** — machine-learning-in-security methodology. REF-001; Ch2 #1 · Ch3 #1.
- **Davis & Goadrich (2006)** — evaluation metric: PR-AUC. REF-013; Ch3 #8.
- **Efron (1979)** — statistics: bootstrap. REF-016; Ch3 #11.
- **European Parliament & Council of the EU (2024)** — a regulation, not a paper (EU AI Act). REF-039; Ch2 #13.
- **Fawcett (2006)** — evaluation metric: ROC-AUC. REF-018; Ch3 #13.
- **Hevner et al. (2004)** — research methodology (design science). REF-021; Ch3 #16.
- **M. Q. Li et al. (2026)** — consistency of agent-safety benchmarks. REF-029; Ch2 #23 · Ch3 #22.
- **Lundberg & Lee (2017)** — attribution, audit-only in REM. REF-034; Ch2 #27 · Ch3 #25.
- **OWASP Gen AI Security Project (2025)** — a web resource, not a paper (prompt-injection definition). REF-042; Ch2 #30 · Ch3 #28.
- **Peffers et al. (2007)** — research methodology (design science). REF-040; Ch3 #30.
- **Ruan et al. (2024)** — agent risk without an adversary (benchmark). REF-044; Ch2 #33.
- **L. Wang et al. (2024)** — background: definition of an LLM agent. REF-047; Ch2 #39.
- **Y. Wang et al. (2026)** — validity of agent-safety benchmarks. REF-051; Ch2 #40 · Ch3 #35.
- **Yao et al. (2023)** — background: the ReAct execution pattern. REF-055; Ch2 #44.

*Coverage check: 44 placed in topics + 14 not placed = 58 = all 58 unique references.*

---

## 5. Papers I Must Read First

The smallest set this index can identify as needed to understand the academic foundation of the thesis, meaning what REM's equations come from and which prior systems its novelty boundaries are drawn against. The papers are grouped, not ranked, and are alphabetical within each group. None is stored locally (Section 1), so each has to be obtained before it can be read.

### A. Foundations

**Chow (1970)** — *On optimum recognition error and reject tradeoff* (REF-011; Ch2 #9 · Ch3 #6; PARTIALLY VERIFIED)

> The Escalate verdict rests on this paper as its conceptual basis for withholding an automatic decision (Ch2 §2.10; Ch3 §3.7.5, Eq. 3.10 context). Stage 1 read only the metadata, not the reject rule itself.

**Elkan (2001)** — *The foundations of cost-sensitive learning* (REF-017; Ch2 #12 · Ch3 #12; VERIFIED)

> Chapter 3's conditional risk and Bayes verdict (Eqs. 3.6–3.7) are marked "Adapted" from this paper's expected-cost criterion, and Chapter 2 introduces decision theory through it. Reading it shows exactly what REM takes from Elkan (a two-class, cost-matrix decision rule) and what REM adds (four verdicts, consequence tiers). The threshold form of Eq. 3.9 is compared against this paper, and its printed threshold expression has not yet been inspected (Section 6).

**Greshake et al. (2023)** — *Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection* (REF-019; Ch2 #14 · Ch3 #14; VERIFIED)

> This paper defines the threat REM is scoped to. Chapter 3 grounds its scoping assumption (§3.1.5) and the observation trust boundary (§3.3.3) in the indirect-injection attack it demonstrates.

### B. Prior-art / competing approaches

**H.-H. Chen (2026)** — *Insuring every action: An authority frontier framework for runtime actuarial control of autonomous AI agents* (REF-008; Ch2 #3 · Ch3 #4; VERIFIED)

> Chapter 2 states it establishes that pricing an action's consequence before execution is not new. Chapter 3 lists it as prior art for consequence-priced control. It sets the boundary on what REM can claim about consequence tiers.

**Hossain et al. (2026)** — *NEXUS: Structured runtime safety for tool-using LLM agents* (REF-023; Ch2 #17 · Ch3 #18; PARTIALLY VERIFIED)

> This is the prior system closest to REM. It combines rules, argument inspection, a Platt-calibrated logistic risk score, four interventions and a defined expected-loss objective, and REM concedes several of these elements. Chapter 2 separates REM from it on one point: NEXUS's deployed policy is a score-gated rule cascade, not a per-decision minimization of conditional risk. That point cannot be re-checked in this environment (Section 6, OI-01), and four of the figures quoted from it are unverified (OI-02 to OI-05).

**H. Liu et al. (2026)** — *SafeAgent: A runtime protection architecture for agentic systems* (REF-032; Ch2 #25 · Ch3 #23; VERIFIED)

> Chapter 2 cites it for stateful decisions over session history and graduated recovery. Chapter 3 lists it as prior art for runtime interception, human review and graduated response.

**She et al. (2026)** — *Safeguarding LLM agents from misalignment through provenance analysis* (REF-045; Ch2 #34 · Ch3 #33; VERIFIED)

> Provenance-based checking of tool calls is prior art for the provenance labeling at the start of REM's pipeline (Ch2 §2.6, §2.8; Ch3 §3.13).

**C. Yang (2026)** — *AgentTrust: Runtime safety evaluation and interception for AI agent tool use* (REF-053; Ch2 #42 · Ch3 #36; VERIFIED)

> This is prior art for interception, verdicts that include review, auditable rule output, and component ablation with latency, all of which Chapter 3 says REM does not claim as new. Its ablation finding that session tracking had no measurable effect is cited in Chapter 2 §2.5.

**C. Zhang et al. (2026)** — *Calibration is not control: Why LLM-agent oversight needs intervention* (REF-058; Ch2 #46 · Ch3 #37; VERIFIED)

> Both chapters concede its central point: recalibrating a scalar risk score need not improve threshold-routed control. REM states it inherits this limitation (Ch3 §3.14). The argument has to be understood to understand what REM does not claim.

### C. Algorithms used in REM

**le Cessie & van Houwelingen (1992)** — *Ridge estimators in logistic regression* (REF-004; Ch3 #21; PARTIALLY VERIFIED)

> Source of the ridge-penalized log-likelihood, Eq. 3.2. Chapter 3 states that the penalty's scaling constant is pending full-text verification.

**Cox (1958)** — *The regression analysis of binary sequences* (REF-012; Ch3 #7; PARTIALLY VERIFIED)

> Source of Eq. 3.1, the logistic model that produces REM's logit and uncalibrated probability. Its printed formulation has not been read (Section 6).

**Guo et al. (2017)** — *On calibration of modern neural networks* (REF-020; Ch2 #15 · Ch3 #15; VERIFIED)

> This paper supplies three pieces: the two-parameter logistic calibration form and negative log-likelihood fit (Eqs. 3.3–3.4), the equal-width binning in the ECE metric (Eq. 3.20), and Chapter 2's definition of calibration. Stage 1 read its full text.

**Kull et al. (2017)** — *Beta calibration: A well-founded and easily implemented improvement on logistic calibration for binary classifiers* (REF-027; Ch2 #21 · Ch3 #20; VERIFIED)

> Two points about Eq. 3.3 rest on this paper: the positive-slope (monotonicity) condition, and the argument that logistic calibration on the logit is beta calibration with equal shape parameters. That argument is why beta calibration is not adopted separately. Stage 1 read the PMLR text.

**Lundberg & Lee (2017)** — *A unified approach to interpreting model predictions* (REF-034; Ch2 #27 · Ch3 #25; VERIFIED)

> Source of the linear attribution and local-accuracy identity in REM's audit record (Eqs. 3.11–3.12). In REM these are audit-only and do not affect the verdict. Chapter 3 notes an index mismatch in the printed formula.

**Platt (1999)** — *Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods* (REF-041; Ch2 #32 · Ch3 #31; PARTIALLY VERIFIED)

> Named in both chapters as the origin of Platt scaling, the method Eq. 3.3 adapts. The citation's title and year do not match the Crossref record of the MIT Press chapter at the cited pages (Section 6, OI-07).

### D. Financial-agent evaluation

**Z. Chen, J. Chen, et al. (2025)** — *Standard benchmarks fail — Auditing LLM agents in finance must prioritize risk* (REF-006; Ch2 #4; VERIFIED)

> This paper argues that accuracy- and return-based evaluation of financial agents misses their vulnerabilities, which is why REM evaluates security and utility together.

**Debenedetti et al. (2024)** — *AgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents* (REF-014; Ch2 #11 · Ch3 #10; VERIFIED)

> REM is evaluated in its banking suite (Ch3 §3.3.1, §3.11.1), and the task, tool and combination counts in Chapter 3 come from it. The paper describes the benchmark; the exact benchmark version used remains open (Section 6, OI-14).

**Jia et al. (2026)** — *FinHarness: An inline lifecycle safety harness for finance LLM agents* (REF-025; Ch2 #19 · Ch3 #19; VERIFIED)

> This is the closest runtime system built specifically for financial agents. Chapter 3 lists it as prior art, so "runtime protection of financial agents" is not claimed as new.

*18 papers in total.*

**Why some cited papers are not in this set.** Page (1954) and Basseville & Nikiforov (1993) underlie the CUSUM analysis, which in REM is optional and observe-only and outside the verdict path. Naeini et al. (2015) contributes one evaluation-metric detail, which Guo et al. (2017) largely covers. Hevner et al. (2004) and Peffers et al. (2007) frame the research method, not REM's design. All of them are in Sections 1–2.

---

## 6. Open Verification Items

Only unresolved citation and evidence issues are listed. Each item states **what is uncertain**, **what source is currently available** and **what still needs verification**. The list is descriptive and makes no recommendation about the thesis text.

**Environment constraint behind most items.** In the environment where Stage 2 and this index were produced, arXiv, SSRN, publisher pages and author-hosted PDFs are blocked by the network egress policy. Crossref and OpenAlex records and search-engine results were reachable. No full text could be opened here. Stage 1 was carried out elsewhere and records full-text reads of some sources; those reads cannot be reproduced here.

### 6.1 Items examined in Stage 2 and still open (14)

#### OI-01 — V-1: how NEXUS selects its intervention

- **What is uncertain:** V-1 asked whether NEXUS derives its intervention policy from expected loss. The repository records give a more specific picture than "unknown." Chapter 2 states that NEXUS "defines an expected-loss objective with fixed costs for each intervention" (§2.4.4, L65; §2.10, L134), and that "its deployed policy, however, is a rule cascade in which the learned score adjudicates particular cases, not a per-decision minimization of conditional risk" (§2.10, L134). What remains uncertain is the relationship between the two: whether NEXUS's runtime verdict is obtained by minimizing that objective, or by the score-gated rule cascade with the objective used for some other purpose.
- **Source currently available:** Stage 1 claim audit, workbook 01: Ch2-C028 (the expected-loss sentence) and Ch2-C024 (the rule-cascade sentence) are both recorded as **Support: Full — content read in full**. `V1_NEXUS_DIRECT_VERIFICATION.md` records V-1 as UNRESOLVED; it was written before the Stage 1 package was in this repository and did not have those records. The Stage 2 report also records V-1 as unresolved and did not cross-reference Ch2-C028 or Ch2-C024. Stage 2 index descriptions call NEXUS a "four-class scorer-gated demotion policy" (search-index tier).
- **Still needs verification:** The NEXUS section that defines the expected-loss objective and the section that specifies the deployed decision procedure, read in full text, to establish how the two relate. In this environment the full text is unreachable, so the Stage 1 reading cannot be reproduced.

#### OI-02 — NEXUS numerical claim N038 — "99 plan features"

- **What is uncertain:** Whether NEXUS's logistic-regression risk score uses 99 plan features (Ch2 §2.4.4, L65). Stage 2 index descriptions refer to "nine deterministic rules." The two are not contradictory, since rules and features are different components, but the closeness of 9 and 99 leaves a transcription error possible.
- **Source currently available:** Stage 1 workbook 06: UNVERIFIED, "Figure Read in Source? No." Stage 2: search-index descriptions only.
- **Still needs verification:** The feature count in the NEXUS paper's method section.

#### OI-03 — NEXUS numerical claim N039 — ECE 0.085 → 0.013 on a 128-instance test set

- **What is uncertain:** Whether ECE fell from 0.085 (raw) to 0.013 (after Platt scaling) on a 128-instance held-out test set (Ch2 §2.4.4, L65).
- **Source currently available:** Stage 1 workbook 06: UNVERIFIED. Stage 2: the 128-instance benchmark size is consistent with search-index descriptions; the ECE values are not corroborated at any tier.
- **Still needs verification:** Both ECE values and the test-set size in the NEXUS paper's calibration results.

#### OI-04 — NEXUS numerical claim N040 — 60-instance calibration split

- **What is uncertain:** Whether calibration used a 60-instance split (Ch2 §2.4.4, L65).
- **Source currently available:** Stage 1 workbook 06: UNVERIFIED. Stage 2: not corroborated at any tier.
- **Still needs verification:** The calibration split size in the NEXUS paper.

#### OI-05 — NEXUS numerical claim N067 — 300/63/128 train/validation/test

- **What is uncertain:** Whether NEXUS-Bench uses 300/63/128 train/validation/test instances (Ch2 §2.12 table, L161). **The Stage 1 records disagree:** workbook 01 (Ch2-C039) marks this table row **Support: Full — content read in full**, while workbook 06 (N067) marks the same figures **UNVERIFIED, "Figure Read in Source? No."**
- **Source currently available:** The two conflicting Stage 1 records. Stage 2: the 128 figure is consistent with search-index descriptions; the full split is not corroborated.
- **Still needs verification:** The dataset split in the NEXUS paper, and which of the two Stage 1 records is correct.

#### OI-06 — NEXUS submission date vs arXiv identifier

- **What is uncertain:** The paper's submission date. Its identifier 2607.19356 places it in July 2026, while its stated submission date is 25 May 2026. Stage 2 found that every field the chapter cites (title, five authors, identifier, year, preprint status) matches the index records; the chapter cites no submission date. The uncertainty is in the source's own record.
- **Source currently available:** Stage 1 reference master: CONFLICTED. Stage 2: index records confirm the title, authors and identifier, and place the listing in July 2026.
- **Still needs verification:** The arXiv version history for 2607.19356, which is unreachable in this environment.

#### OI-07 — Platt (1999) vs (2000) citation conflict

- **What is uncertain:** Which record the citation describes. Both chapters cite Platt, J. C. (1999), "Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods", in Smola et al. (Eds.), *Advances in large margin classifiers*, pp. 61–74. Crossref registers the MIT Press chapter at those pages as "Probabilities for SV Machines" (2000). The cited title and year belong to a 1999 circulation of the work, whose report number could not be confirmed. A candidate number was rejected because it appeared only in a search query the audit itself wrote.
- **Source currently available:** Crossref record 10.7551/mitpress/1113.003.0008 (Stage 2). Search-index records showing both forms in circulation. Stage 1: UNVERIFIED (host certificate error).
- **Still needs verification:** The physical MIT Press volume, or a confirmed record of the 1999 circulation. Separately, Platt's printed parameterization of the sigmoid, which Eq. 3.3 adapts and which has not been read.

#### OI-08 — Jackson (2025) — content

- **What is uncertain:** The paper's content. Its bibliographic record is confirmed. Chapter 2 mentions it by title only and states that its mechanism is not described and that no claim rests on it (§2.10, L132).
- **Source currently available:** Crossref: DOI 10.2139/ssrn.5904104 registered, and author, title, year and preprint status match (Stage 2). Full text: SSRN returned HTTP 403 in both Stage 1 and Stage 2.
- **Still needs verification:** The full text, if the chapter's characterization of its topic is to be checked.

#### OI-09 — Brier (1950) — scoring convention

- **What is uncertain:** The Brier score's original convention. Chapter 3 states that the Brier score is not reported until this convention has been confirmed (§3.12.2, L845).
- **Source currently available:** Crossref record matches every cited field (Stage 2). Publisher page: HTTP 403 (Stage 1).
- **Still needs verification:** The paper's definition of the score, which is 3 pages long.

#### OI-10 — le Cessie & van Houwelingen (1992) — penalty scaling constant

- **What is uncertain:** The exact scaling constant of the ridge penalty in Eq. 3.2. Chapter 3 states this itself (§3.7.1, L329) and argues that a positive rescaling changes the selected λ, not the set of attainable solutions.
- **Source currently available:** Crossref record matches (Stage 1 and Stage 2). Stage 2 independently checked that Eq. 3.2 penalizes β only and leaves the intercept unpenalized.
- **Still needs verification:** The penalized log-likelihood as printed in the paper.

#### OI-11 — Elkan (2001) — printed threshold expression

- **What is uncertain:** The form and equation number of Elkan's printed threshold. Chapter 3 states that it "could not be inspected directly during verification" and stands Eq. 3.9 on its own derivation (§3.7.5, L456).
- **Source currently available:** Stage 1 read the author PDF (cost convention and Eq. 1). Stage 2 confirmed pp. 973–978 through dblp and the ACM DL and independently re-derived Eqs. 3.8–3.10. The author PDF host is blocked in this environment.
- **Still needs verification:** The threshold expression in the paper and its equation number.

#### OI-12 — Cox (1958) — printed formulation

- **What is uncertain:** The printed form of the logistic model cited for Eq. 3.1, which Chapter 3 marks "established from source" (§3.7.1, L316).
- **Source currently available:** Crossref record matches every cited field (Stage 1 and Stage 2). The paper has not been read.
- **Still needs verification:** The model as printed in the paper.

#### OI-13 — Chow (1970) — reject rule

- **What is uncertain:** The content of the reject rule cited as the conceptual basis for Escalate (Ch2 §2.10; Ch3 §3.7.5).
- **Source currently available:** Crossref record matches every cited field (Stage 1 and Stage 2). Stage 1: "reject rule not read."
- **Still needs verification:** The paper's statement of the error–reject tradeoff.

#### OI-14 — AgentDojo — pinned benchmark version

- **What is uncertain:** Which AgentDojo version the evaluation uses. Chapter 3 cites "suite v1, AgentDojo repository main branch, accessed September 2026." Stage 2 verified the counts (16 user tasks, 9 injection tasks, 11 tools, 144 combinations) from the agentdojo 0.1.35 package source and showed that the counts are the same across benchmark versions 1.0.0–1.2.2. It also found that **task content differs between versions**: injection tasks were revised at v1.2.0, UserTask15 at v1.1.1 and UserTask6 at v1.2.2.
- **Source currently available:** agentdojo 0.1.35 package source from PyPI (Stage 2). The Chapter 3 access note.
- **Still needs verification:** The exact version or commit that the experiments run against. This is also listed as unresolved in the repository's design contract (`CLAUDE.md`, DATA / EVALUATION LOCK).

> **Record note on OI-01.** Section I of the Stage 2 report describes what REM does not concede to NEXUS as "the derivation of the verdict from an expected-loss argmin over a declared loss grid." That should be read together with the chapter's own, narrower wording. By Stage 1's full-text reading, NEXUS *does* define an expected-loss objective over its four interventions. The distinction Chapter 2 draws is between per-decision minimization and a score-gated rule cascade, not between having an expected-loss formulation and lacking one.

### 6.2 Carried forward from Stage 1, not examined in Stage 2 (11)

These references are PARTIALLY VERIFIED in the Stage 1 master: their records were confirmed, but the content the chapter uses was not checked in the source. Stage 2 did not re-examine them.

| Item | Reference | Used for | Uncertain | Available | Still needs verification |
| --- | --- | --- | --- | --- | --- |
| CF-01 | Davis & Goadrich (2006) — REF-013 | PR-AUC (Ch3 §3.12.2) | Content not read | Crossref metadata | The paper's treatment of PR-AUC |
| CF-02 | Efron (1979) — REF-016 | Bootstrap confidence intervals (Ch3 §3.11.9) | Content not read | Crossref metadata | The bootstrap procedure as described |
| CF-03 | Fawcett (2006) — REF-018 | ROC-AUC (Ch3 §3.12.2) | Content not read | Crossref metadata | The paper's treatment of ROC-AUC |
| CF-04 | Hevner et al. (2004) — REF-021 | Design science framing (Ch3 §3.1.1) | Content not read | Crossref metadata | The characterization of design science research |
| CF-05 | Peffers et al. (2007) — REF-040 | Six DSR activities (Ch3 §3.1.1 table) | Content not read | Crossref metadata | The six activities as the table lists them |
| CF-06 | Page (1954) — REF-038 | Origin of CUSUM (Ch2 §2.5); Eq. 3.16 (Ch3) | Content not read | Crossref metadata | The CUSUM recursion as printed |
| CF-07 | Reynolds & Stoumbos (1999) — REF-043 | Bernoulli CUSUM (Ch3 §3.11.10; Eq. 3.15) | Content not read | Crossref metadata | The Bernoulli CUSUM chart as printed |
| CF-08 | L. Wang et al. (2024) — REF-047 | Definition of an LLM agent (Ch2 §2.2) | Content not read | Crossref metadata | The definition as the survey states it |
| CF-09 | European Parliament & Council of the EU (2024) — REF-039 | Articles 12 and 14 (Ch2 §2.7, §2.11) | Read on a secondary host only | Article text from a secondary host (Stage 1) | Articles 12 and 14 against EUR-Lex |
| CF-10 | Lorden (1971) — REF-033 | Asymptotic optimality of CUSUM-type rules (Ch3 §3.11.10) | Assumptions not read | Project Euclid abstract (Stage 1) | The independence and known-distribution assumptions |
| CF-11 | Moustakides (1986) — REF-036 | Optimality of Page's stopping time (Ch3 §3.11.10) | Assumptions not read | Project Euclid abstract (Stage 1) | The sense of optimality and its assumptions |

**Not listed as open.** Seven figures in workbook 06 are marked "VERIFIED AT INSPECTION DATE". These are time-bound values that were confirmed when inspected. The 40 VERIFIED references are also not listed, although many were checked at abstract level only; their Basis fields in Sections 1–2 say so.

---

## Totals

```text
TOTAL CHAPTER 2 REFERENCES:     47
TOTAL CHAPTER 3 REFERENCES:     37
TOTAL UNIQUE REFERENCES:        58
TOTAL PAPERS AVAILABLE LOCALLY: 0
TOTAL PAPERS MISSING:           58
TOTAL VERIFIED:                 40
TOTAL PARTIALLY VERIFIED:       18
TOTAL UNVERIFIED:               0
TOTAL OPEN EVIDENCE ITEMS:      25   (14 examined in Stage 2 + 11 carried forward from Stage 1)
```

Notes on the totals:

- Verification counts are over the **58 unique** references, since a shared reference has one status. 40 + 18 + 0 = 58.
- "Papers" follows the requested wording. The 58 references include one book (Basseville & Nikiforov, 1993), one regulation (EU AI Act) and one web resource (OWASP LLM01:2025).
- UNVERIFIED is 0 because every reference's existence has now been confirmed by some record. It does **not** mean every claim is confirmed: 18 references are PARTIALLY VERIFIED, and 25 evidence items remain open.
