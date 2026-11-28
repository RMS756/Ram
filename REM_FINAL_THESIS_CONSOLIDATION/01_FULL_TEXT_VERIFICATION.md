# 01: Full-text verification of the reviewed studies (28 November 2026)

## 1. Result

**No new full text was obtained in this task.** Full-text verification is therefore **incomplete**: [SOURCE VERIFICATION INCOMPLETE] for every study below except those read in full earlier.

### Access routes tried

| Route | Result | Evidence |
|---|---|---|
| arXiv (`arxiv.org/html`, `/abs`) | Refused | DNS failure ("host outside the session's allowed network domains") for every URL |
| ACL Anthology (NEXUS) | Refused | Same |
| PMLR (MELON) | Refused | Same |
| MDPI (Spotlight-Guard, AIS) | Refused | Same |
| TechScience (Multilayer DiD) | Refused | Same |
| Nature (PromptGuard) | Refused | Same |
| Crossref, OpenAlex, Semantic Scholar from the shell | Refused | `curl` returned no connection |
| Crossref and OpenAlex through the literature connector | **Available** | Records and abstracts retrieved (§3) |
| Scholar Gateway connector | **Needs sign-in** | Reconnection was refused; the user must sign in again under claude.ai → Settings → Connectors |
| Elicit connector | **Plan restriction** | "This Elicit account's plan doesn't include API access" |
| Session environment | **Not changed** | This session runs on the Default environment, which allows no academic hosts. Another saved environment, "ram-thesis-research", allows `arxiv.org`, but this session cannot be moved onto it while it runs. Widening the Default environment for one repository was not proposed |

**What was not done.** No access control was bypassed, and no mirror or unofficial copy was used. No search snippet was treated as full text.

**How to finish this item.** Either of these should work:
- start a new session on the "ram-thesis-research" environment, which allows arXiv (add `aclanthology.org`, `www.mdpi.com`, `www.techscience.com` and `www.nature.com` there for the journal versions);
- sign in to Scholar Gateway.

Then update the table in §2 section by section from the full texts.

## 2. Study-by-study status

Levels:

| Code | Meaning |
|---|---|
| F | Full text read (earlier session) |
| P | Partial full text |
| A | Abstract only (OpenAlex or Crossref, retrieved 28 Nov 2026 unless stated) |
| B | Bibliographic record only |
| R | Official code read (not the paper) |
| X | Inaccessible |

**Sections inspected:** for level A, the abstract only, so no Related Work, Threat Model, Limitations, Future Work, Threats to Validity, Ablation or Evaluation section was inspected. Page or section references are therefore **not available** for any A-level work.

| # | Study | Verified bibliographic record | Publication status | Full text | What is verified (abstract level unless stated) | Author-acknowledged limitations / future work | Relevance to REM | Remaining uncertainty |
|---|---|---|---|---|---|---|---|---|
| 1 | NEXUS | Hossain, Nipu, Ornee, Rana & Yousefi (2026). Findings of IJCNLP-AACL 2026, pp. 2203–2232. DOI 10.18653/2026.findings-aacl.112 | Peer reviewed | A, R (repository read 13 Nov 2026) | Formal intervention policy Π over allow / block / request confirmation / request revision. Deterministic rules, argument-level inspection and a calibrated logistic-regression risk score. **Compared with rule-only intervention selection:** +27.3 points of 4-class intervention accuracy on a 128-instance synthetic benchmark; R-Judge F1 0.861 against 0.849; "matches rule-only on AgentHarm due to threat-model limits"; NEXUS-Stress F1 0.897 with REVISE recall 0.500 | Abstract: "highlighting both progress and remaining difficulty in fine-grained intervention routing". Repository working document (R): the learned scorer gives no binary-detection gain over rules alone | Closest decision-layer analogue. It shows that a learned-versus-rule comparison exists outside finance, so the gap must be narrowed (04) | Full-text limitations, ablation details and threat model not read. Abstract versions differ (0.38 ms vs 0.205 ms; F1 0.897 vs 0.881) |
| 2 | Progent | Shi et al. arXiv 2504.11703 v3 (14 May 2026) | Preprint | **F** (v3, 16 Nov 2026; thesis Table 2.3), R | Thesis Table 2.3: deterministic per-tool policies with argument restrictions; LLM-written and updated policies; monotonic confinement; AgentDojo ASR 39.9% → 1.0% at similar utility (gpt-4o); ablations of approver, model and adaptive attack | As recorded in Table 2.3 (no banking-only result) | Model-independent argument authorization (B3) | None beyond Table 2.3 |
| 3 | Agent-Sentry | Sequeira, Damianakis, Iqbal & Psounis. arXiv 2603.22868 | Preprint | A | "Layers three complementary checks": a structural classifier over action sequences and argument provenance; a deterministic allow-list over sensitive argument values; an LLM judge on the residual. Blocks 94.3% of successful injections while allowing 95.1% of benign executions (AgentDojo, AgentDyn) | Not determinable at A level | Layered agent defense with provenance | Per-layer ablation n.d.; v1 and v2 figures differ |
| 4 | MELON | Zhu, Yang, Wang, Guo & Wang (2025). ICML 2025, PMLR 267 | Peer reviewed | **F** (11 Nov 2026, author-supplied PDF; thesis Table 2.3), R | Masked re-execution with tool-call comparison; reported benign utility with GPT-4o falls from 80.41% to 68.04% | As recorded in Table 2.3 | LLM in the decision path (not adoptable under the design lock) | **Correction to the earlier review's 09:** it listed MELON as O and R; the thesis records an F reading. The thesis record is authoritative |
| 5 | CaMeL | Debenedetti et al. arXiv 2503.18813 | Preprint (SaTML 2026 publication not confirmed) | R; X for the paper | Repository: capability propagation and per-tool policies; the banking policy requires only the recipient to originate from the user (DiD edition Table 2.6) | n.d. | Capability-based trust boundary (A1) | Paper not read |
| 6 | AgentDojo | Debenedetti et al. (2024). NeurIPS 2024 Datasets and Benchmarks; arXiv 2406.13352 | Peer reviewed | A, plus the package (0.1.35) and recorded runs (`089ed468`) used directly | Executable benchmark; the banking suite has 16 user tasks and 9 injection tasks (thesis Ch. 3–4) | n.d. | Evaluation environment | Paper sections not re-read in this task |
| 7 | Intelligent Multilayer DiD | Jang, Lee & Shon. *Computers, Materials & Continua* 90(1), 1–10. DOI 10.32604/cmc.2026.090355 | Peer reviewed; online first 2026, **issue year 2027** (Crossref) | A, B | Five-layer framework for local LLMs in air-gapped networks, grounded in MITRE ATLAS; compares a policy-approved initial intent with the trajectory of observed events, including tool calls (earlier review) | n.d. | LLM application that observes agentic events without authorizing them | Full text not read; cite as **2027** |
| 8 | PromptGuard | Alzahrani (2026). *Scientific Reports* 16, 1277. DOI 10.1038/s41598-025-31086-y | Peer reviewed | A, B | Input gatekeeping, structured prompt formatting, semantic output validation, response refinement (earlier review). The Crossref title has no colon | n.d. | LLM text pipeline only; not a tool-call defense | Name clash with Meta's "Prompt Guard" classifier |
| 9 | Layered RAG chatbot framework | Saleem, Ahmed, Zaman et al. (5 authors). arXiv 2606.19660 | Preprint. **DOI 10.62762/TISC.2026.712476 not registered with Crossref** (re-checked 28 Nov 2026) | A | Three layers: (1) a rule library and a fine-tuned anomaly classifier on input; (2) a provenance-based instruction hierarchy during context assembly; (3) an output policy engine and a semantic drift detector, with an audit loop. 5,080 samples, three models; ASR 71.4% → 11.3%; FPR 4.8%. **"Ablation studies confirm that all three layers provide complementary protection and that their combined effect exceeds the sum of individual contributions"** | n.d. | RAG chatbot, not an agent. Its reported layer complementarity means "complementarity shown by ablation" is not new in general (04) | Journal version unverified; ablation design not read |
| 10 | CASCADE / CASCADE audit | Audit: Abasıkeleş-Turgut & Gümüş. arXiv 2604.17125 | Preprint | A | The audit's object is CASCADE (local; rule matching, embedding similarity and optional local LLM review; MCP). Findings: (1) the decision convention sets the headline FPR (11.70% vs 1.51%) while 68.5% of traffic is referred; (2) corpus construction shapes the aggregate; (3) the published description does not identify what ran; (4) the review model changes no binary outcome. A ten-item reporting checklist is derived | — | Evaluation methodology (A6, A7) | **CASCADE's own paper was not found**; its status is unknown. arXiv 2604.17125 must not be cited as CASCADE |
| 11 | Spotlight-Guard | Demirol & Aydoğan (2026). *Applied Sciences* 16(15), 7662. DOI 10.3390/app16157662 | Peer reviewed | A | Spotlighting, an LLM detection-and-quarantine pipeline and HMAC instruction integrity; 7B-class open-weight models; ASR 36.0% → 17.2% with 97.2% benign-task success; **a component ablation isolates each layer's contribution**; adaptive ASR 6.7%; cost in model invocations | n.d. | Layered agent defense with a component ablation and benign utility | Ablation design not read |
| 12 | AIS | Gong, Samawi & Medda (2026). *Systems* 14(10), 1329. DOI 10.3390/systems14101329 | Peer reviewed | A, B | Typed financial intent validated against mandate, policy, state, approvals and exact economic terms before single-use authority; mechanism ablations on attack fixtures (DiD edition Table 2.6) | n.d. | Financial agent; authority–inference separation (A2, B3) | Full text not read |
| — | BARBICAN ("Deletion is not substitution") | Abasıkeleş Turgut & Gümüş. arXiv 2610.33198 | Preprint | A | Four-tier fail-closed MCP gateway with a neural arbitrator. Deletion, constant substitution, repair and transplant applied to the arbitration stage; more than 30 instrumented runs over 25,000 prompts. Deletion credits contributions that differ by more than an order of magnitude; substitution shows the stage can affect only a few inputs; "its influence is set by its position, not its quality"; a CI gate for unreachable stages; a three-point roadmap for ablation studies | The roadmap is the authors' recommendation (content n.d.) | **Directly supports** REM's removal-versus-suppression lesson (A7) and motivates B7 | Full text not read; the authors' group developed BARBICAN |

## 3. Attribution rules applied in 02, 04, 05 and 07

1. A statement attributed to an author quotes or paraphrases the abstract only. Quoted phrases (for example Saleem et al.'s "complementary protection", NEXUS's "remaining difficulty") are verbatim from the abstract.
2. **No limitation or future-work statement is attributed to an A-level author beyond the abstract.** Analytical observations (for example "does not authorize financial arguments") are labelled "at the level of their abstracts".
3. No equation, threshold or score from these works enters REM or the thesis (03 §4).

## 4. Effect of the access limit on the conclusions

| Conclusion | Robust to the missing full texts? |
|---|---|
| These works exist, have the stated status, and propose the stated mechanisms | Yes (records and abstracts) |
| Layer- or component-level ablations of layered injection defenses exist (Saleem; Spotlight-Guard), and NEXUS compares against rule-only | Yes. Stated in the abstracts |
| Whether any of them suppresses an evidence family at test time, or uses a withhold-everything reference | **Not determinable** from abstracts. The gap (04) is worded "among the studies examined, at the level read" |
| Authors' own limitations and future work | **Not determinable** except where the abstract states them |
