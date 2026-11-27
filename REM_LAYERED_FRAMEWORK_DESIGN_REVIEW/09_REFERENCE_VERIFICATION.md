# 09: Reference verification

**Date:** 28 November 2026.

**Verification methods:**
- Crossref record (DOI lookup);
- OpenAlex record, via the literature connector;
- official repository code read in this or an earlier session;
- web-search excerpts.

**Full-text access.** Full texts could not be opened from this session:
- `arxiv.org`, `www.mdpi.com`, `www.techscience.com`, `www.nature.com`, `aclanthology.org`, `www.alphaxiv.org` and `doi.org` all failed DNS resolution through the web-fetch tool;
- a PubMed Central request was refused by the session's permission system and was **not** retried.

No access restriction was worked around.

**Evidence levels.**

| Level | Meaning |
|---|---|
| F | Full text read (earlier session) |
| R | Official code read |
| C | Crossref record |
| O | OpenAlex record with abstract |
| S | Web-search excerpt of the full text (indirect; may paraphrase) |

**A mechanism is described only at the level available.** Where the level is O or S, details beyond the abstract are marked "not determined" (n.d.).

## 1. The twelve requested works

| # | Work as requested | Verified bibliographic record | Status | Level | Notes and discrepancies |
|---|---|---|---|---|---|
| 1 | NEXUS (2026) | Hossain, E., Nipu, M. M. H., Ornee, T. N., Rana, R., & Yousefi, N. (2026). *NEXUS: Structured runtime safety for tool-using LLM agent.* Findings of the ACL: IJCNLP-AACL 2026, pp. 2203–2232. DOI [10.18653/2026.findings-aacl.112](https://doi.org/10.18653/2026.findings-aacl.112). arXiv version [2607.19356](https://arxiv.org/abs/2607.19356) | **Peer reviewed** | C, O, S; authors' repository read 13 Nov 2026 (thesis Appendix, OI-01 to OI-06) | Abstract versions differ: the latency is given as 0.38 ms (OpenAlex) and 0.205 ms (search excerpt of an arXiv version), and stress-benchmark F1 as 0.897 and 0.881. **Cite the proceedings version** |
| 2 | Progent | Shi, T., He, J., Wang, Z., Li, H., Wu, L., Guo, W., & Song, D. *Progent: Securing AI agents with privilege control.* arXiv [2504.11703](https://arxiv.org/abs/2504.11703) v3 (14 May 2026) | **Preprint** | F (v3, 16 Nov 2026), R (`sunblaze-ucb/progent` at `9befb41`) | The title in some citations ("Programmable Privilege Control") is an earlier version's |
| 3 | Agent-Sentry | Sequeira, R., Damianakis, S., Iqbal, U., & Psounis, K. *Agent-Sentry: Bounding LLM agents via execution provenance.* arXiv [2603.22868](https://arxiv.org/abs/2603.22868) | Preprint | O, S | v1 and v2 report different figures |
| 4 | MELON | Zhu, K., Yang, X., Wang, J., Guo, W., & Wang, W. Y. (2025). *MELON: Provable defense against indirect prompt injection attacks in AI agents.* ICML 2025, PMLR 267, pp. 80310–80329. arXiv [2502.05174](https://arxiv.org/abs/2502.05174) | **Peer reviewed** | O; **R** (`kaijiezhu11/MELON` at `4d3cc9c`, `ucsb-mlsec/MELON` at `06014c7`; `REM_MELON_COMPARISON_2026_11_19/02`) | — |
| 5 | CaMeL | Debenedetti, E., Shumailov, I., Fan, T., Hayes, J., Carlini, N., Fabian, D., Kern, C., Shi, C., Terzis, A., & Tramèr, F. *Defeating prompt injections by design.* arXiv [2503.18813](https://arxiv.org/abs/2503.18813) | Preprint (SaTML 2026 publication **not confirmed**) | R (code at `f083b6b`), S | — |
| 6 | AgentDojo | Debenedetti, E., Zhang, J., Balunović, M., Beurer-Kellner, L., Fischer, M., & Tramèr, F. (2024). *AgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents.* NeurIPS 2024 Datasets and Benchmarks. DOI 10.52202/079017-2636; arXiv [2406.13352](https://arxiv.org/abs/2406.13352) | **Peer reviewed** | O; package 0.1.35 and recorded runs at `089ed468` used and re-run in this project | — |
| 7 | Intelligent Multilayer Defense-in-Depth Framework (2026) | Jang, S., Lee, M., & Shon, T. *Intelligent multilayer defense-in-depth framework for securing local LLMs in air-gapped networks.* *Computers, Materials & Continua*, 90(1), 1–10. DOI [10.32604/cmc.2026.090355](https://doi.org/10.32604/cmc.2026.090355). Official page: <https://www.techscience.com/cmc/v90n1/70117/html> | **Peer-reviewed journal**; online first; Crossref issue year **2027** | C, O | Full text not opened (DNS). Web search did not surface the paper itself |
| 8 | PromptGuard | Alzahrani, A. (2026). *PromptGuard: A structured framework for injection resilient language models.* *Scientific Reports*, 16, 1277. DOI [10.1038/s41598-025-31086-y](https://doi.org/10.1038/s41598-025-31086-y). Also PMC12789616 | **Peer reviewed** | C, O, S | **Name clash:** "Prompt Guard" is also the name of Meta's classifier, used as a baseline in row 7. Do not conflate them. A search excerpt mentions a BERT-based input classifier; "MiniBERT" (from the abstract) is not further verified |
| 9 | A Layered Security Framework Against Prompt Injection in RAG-Based Chatbots (2026) | Saleem, G., Ahmed, N., Zaman, M. I., et al. (5 authors). arXiv [2606.19660](https://arxiv.org/abs/2606.19660) (preprint). DOI given by the user: 10.62762/TISC.2026.712476 (IECE prefix) | arXiv version: **preprint**. Journal version: **DOI not registered with Crossref** on 28 Nov 2026 | O (arXiv version) | **Journal version not verified.** Cite the arXiv version, or verify the journal record before citing the DOI |
| 10 | CASCADE (arXiv 2604.17125) | **arXiv 2604.17125 is not CASCADE's own paper.** It is Abasıkeleş-Turgut, İ., & Gümüş, E. *Evaluating a layered prompt-injection defence for the Model Context Protocol: A record-level audit of decision conventions, corpus provenance and reproducibility.* arXiv [2604.17125](https://arxiv.org/abs/2604.17125) | Preprint | O | Its object is CASCADE, a local layered MCP defence (rules, embedding similarity, optional local LLM review). **CASCADE's original publication was not found**; status unknown |
| 11 | Spotlight-Guard | Demirol, D., & Aydoğan, M. (2026). *Balancing security and performance in LLM agents: Spotlight-Guard, a layered defense against indirect prompt injection.* *Applied Sciences*, 16(15), 7662. DOI [10.3390/app16157662](https://doi.org/10.3390/app16157662) | **Peer reviewed** | O | — |
| 12 | AIS | Gong, H., Samawi, M., & Medda, F. (2026). *Authority–inference separation in agentic finance: Intent-bound control, EVM enforcement, and replayable assurance.* *Systems*, 14(10), 1329. DOI [10.3390/systems14101329](https://doi.org/10.3390/systems14101329). Earlier arXiv [2608.30519](https://arxiv.org/abs/2608.30519) with a different subtitle | **Peer reviewed** | C, O, S | — |

## 2. Additional works found and used

| Work | Record | Status | Level | Why used |
|---|---|---|---|---|
| ROPE | Ma, X., Xiao, C., Yeoh, W., Zhang, N., & Vorobeychik, Y. arXiv [2608.27496](https://arxiv.org/abs/2608.27496) | Preprint | **R** (code and logs at `ffe27c4`), O | Origin-based argument provenance on AgentDojo banking (`REM_X_DESIGN_AMENDMENT_01/02`) |
| AGATE | Zhang, X., Cheng, Z., Liu, K., et al. arXiv [2609.30830](https://arxiv.org/abs/2609.30830) | Preprint | O, S | Exact-parameter grants, effect ledger |
| AgentCap | Kabbinamakki Suresh, A. K., & Gao, P. arXiv [2611.00729](https://arxiv.org/abs/2611.00729) | Preprint | O, S | Capability tokens at the tool boundary |
| ClawGuard | Zhao, W., Li, Z., Zhang, P., et al. arXiv [2604.11790](https://arxiv.org/abs/2604.11790) | Preprint | O | User-confirmed rule set at every tool-call boundary |
| CapLite | Xu, Z., Liu, W., & Nakayama, H. arXiv [2611.17115](https://arxiv.org/abs/2611.17115) | Preprint | O | Writes admitted only with authority-bearing arguments stated in the request |
| SIEVE | Liang, Z., Hu, T., Chen, Z., et al. arXiv [2512.06716](https://arxiv.org/abs/2512.06716) | Preprint | O | Deterministic verification first; escalate ambiguous cases |
| **Deletion is not substitution** (BARBICAN) | Abasıkeleş Turgut, İ., & Gümüş, E. arXiv [2610.33198](https://arxiv.org/abs/2610.33198) | Preprint | O | Shows that deletion-based ablation of a layered gateway misleads; substitution changes the attribution. **Directly relevant to REM's removal-versus-suppression finding** |
| DEFER1 | Mitra, S., Patel, R., Neupane, S., et al. *Where rules end and judges begin.* arXiv [2610.07657](https://arxiv.org/abs/2610.07657) | Preprint | O | Deterministic-first cascade with residual judges; reports a risk-score approval gate that approves most attack proposals |
| A-VIP (AP2) | Louck, Y., Dvir, A. Z., & Stulman, A. *Signing the transaction but not the decision: Whisper attacks and a binding defense for AP2.* arXiv [2609.11757](https://arxiv.org/abs/2609.11757) | Preprint | O | **Financial payment agents:** binding credential lookups and cart lines; surfaces unauthorized spending for confirmation |
| Zhan et al. (2025) | *Adaptive attacks break defenses against indirect prompt injection attacks on LLM agents.* Findings of NAACL 2025. DOI [10.18653/v1/2025.findings-naacl.395](https://doi.org/10.18653/v1/2025.findings-naacl.395) | Peer reviewed | O | Adaptive-attack evaluation requirement |
| AutoDojo | Ma, X., Li, T., Xiao, C., et al. arXiv [2606.15057](https://arxiv.org/abs/2606.15057) | Preprint | O | Static benchmarks overestimate defenses |
| DRIFT | Li, H., Liu, X., Chiu, C., et al. (2025). NeurIPS 2025. DOI [10.52202/085713-2791](https://doi.org/10.52202/085713-2791) | Peer reviewed | O; code audited earlier (`REM_EXTERNAL_DEFENSE_AUDIT/01`) | Plan-and-validate with injection isolation |

## 3. Citation rules for the thesis

1. Cite the **peer-reviewed** version where one exists: NEXUS, MELON, AgentDojo, Spotlight-Guard, AIS, PromptGuard, the Multilayer DiD framework, DRIFT.
2. Mark the others as preprints.
3. Do **not** cite arXiv 2604.17125 as "CASCADE". Cite it as the record-level audit of CASCADE.
4. Do **not** cite DOI 10.62762/TISC.2026.712476 until the journal record is verified. Cite arXiv 2606.19660.
5. Every mechanism attributed at level O or S must be worded as "reported" or "according to the abstract". **No equation from these works may be reproduced in the thesis without reading the full text.**
