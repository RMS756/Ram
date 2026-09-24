# Chapter 2: Verification Log (September 2026 pass)

Raw working log of the checks behind the evidence matrix. Tools: Crossref (via a reference-verification service), OpenAlex, and web-search retrieval of arXiv, proceedings and publisher abstract pages. Direct fetching of arXiv, publisher or mirror pages was blocked by the container's network policy, so any detail visible only in a full text is marked as not re-confirmed.


- AgentTrust (Yang C., 2605.04785, 6 May 2026, single author Chenglin Yang). Verdicts allow/warn/block/review; 170 YAML rules; 42 regex patterns; SafeFixEngine 37 fix rules; SessionTracker (RiskChain) 7 order-aware chain detectors; LLMJudge; MCP server. 300-scenario benchmark (6 risk categories) + 630 external scenarios. Production ruleset 95.0% verdict acc, 73.7% risk-level acc, low-ms latency. 630: 96.7% under PATCHED ruleset, not zero-shot; ~93% on shell-obfuscated. Disabling SessionTracker leaves verdict accuracy unchanged on either benchmark. [max-severity aggregation, step-function confidence, reversibility rubric: from prior DOCX audit; NOT re-confirmed this session]
- NEXUS (Hossain, Nipu, Ornee, Rana, Yousefi; 2607.19356). allow/block/request confirmation/request revision; deterministic rules + argument-level inspection + calibrated LR risk score. Platt lowest ECE; isotonic lowest Brier; ECE 0.085->0.013. Median latency 0.205 ms. 92% of GPT-4o binary F1, 78% intervention accuracy, ~4,800x faster. [128 test / 60 calib split, 99 features, rule cascade vs expected-loss objective, upper-bound caveat: from prior DOCX audit; NOT re-confirmed]
- Calibration Is Not Control (Zhang Chubin, Wan Zhenglin, Yu Xingrui, Wu Jingxuan, Wen Qi, Zhou Pengfei, Zhao Wangbo, Tsang Ivor; 2606.21399; 19 Jun 2026). Intervention advantage; target error; prefix branching; four benchmarks; ALFWorld Platt ECE 0.463->0.006, regret fixed 0.318. VERIFIED (snippet from HTML).
- SafeAgent (Liu Hailin, Ilyushin Eugene, Ni Jie, Zhu Min; 2604.17562; 19 Apr 2026). Runtime controller + context-aware decision core over persistent session state; operators risk encoding, utility-cost evaluation, consequence modeling, policy arbitration, state synchronization. ASB + InjecAgent. [action space list, no calibration, no latency: from DOCX; NOT re-confirmed]
- FinHarness (2605.27333; 26 May 2026). Query Monitor (single-turn intent + cross-turn drift), Tool Monitor (each prospective tool call), Cascade (integrates per-step risk; routes lightweight vs advanced LLM judge). On FinVault: ASR 38.3%->15.0%; benign approval 41.1%->39.3%; 4.7x fewer advanced-judge calls. NOTE evaluated on FinVault (withdrawn). Authors per DOCX Jia H. et al. - not re-confirmed.
- ProvenanceGuard (She Yining, Liang Yiliang, Kang Eunsuk; 2607.01236). Error on misaligned traces 44.3%->2.1% Agent-SafetyBench; 32.4%->18.7% WorkBench. Intervention rate on aligned traces 10.9% baseline / 12.0% ProvePrompt / 14.5% ProvenanceGuard => v2.0 claim "reducing unnecessary interventions" and "42.9%->1.8%" are WRONG; DOCX figures correct. v2.0 author initials (Liang Z., Kang D.) WRONG.
- Insuring Every Action (2605.25632; author "H. Chen"; May 2026). Actuarial Action Interface (AAI): deterministic runtime contract pricing each action against safe default under time-consistent risk mapping; gates vs reserve capital budget; Authority Frontier = authority released per reserve capital level; quote-bind-commit with capability tokens; 7-class action taxonomy. Examples: DB mutations, refunds, payments. v2.0 attributed to "Chen, Z." -> WRONG; DOCX "Chen, H.-H." (full given name not re-confirmed).
- FinVault (2601.07853). 31 scenarios, 107 vulns, 963 cases; ASR up to 50.0%, 6.7% most robust. WITHDRAWN confirmed (legal/IP/affiliation comment). GitHub artifact exists (anonymized). => cite only as withdrawn; do not use numbers as evidence.
- DreamGuard (2608.05695). Recurrent latent state over trajectory; immediate-hazard + prefix-risk scores; calibrated fusion -> PASS/HOLD/BLOCK; four benchmarks; avg end-to-end latency 25 ms per call. Authors per DOCX Lin W. et al. (not re-confirmed).
- M. Q. Li et al. 2026 (2605.16282): Miles Q. Li, Benjamin C. M. Fung, Boyang Li, Heba Ismail, Farkhund Iqbal. 40 behavioural agent-safety benchmarks (2023-2026) + 5 adjacent; six-axis taxonomy; Kendall's W: no evidence of ranking concordance; benchmark choice systematically alters reported safety. VERIFIED.
- Y. Wang et al. 2026 (2607.28685, 30 Jul 2026): four benchmarks R-Judge, InjecAgent, AgentHarm, AgentDojo on up to 22 models; metric-validity failure (always-positive F1 baseline outranks five models on R-Judge); small-panel artifact correlation -0.64 (n=7) -> +0.02 (n=18). DOCX claim "higher capability can correlate with worse safety scores" NOT confirmed -> reword. Authors not re-confirmed.
- Cordon (2606.17573, 16 Jun 2026): semantic transaction; transaction manager; reversible mutations in shadow state; outward-facing actions staged in effect outbox; recovery metadata; exposes cross-step violations missed by existing defenses; reduces irreversible-effect failures while preserving benign completion. Authors per DOCX (Chen Z., Liu H., Xu D., Dong D., Li J., Pu B., Zhai J.) not re-confirmed; v2.0 "Chen [et al.]" placeholder.
- PRISM (Li, Frank; 2603.11853; Mar 2026). ten lifecycle hooks (message ingress, prompt construction, tool execution, tool-result persistence, outbound messaging, sub-agent spawning, gateway startup); hybrid heuristic+LLM scanning; conversation- and session-scoped risk accumulation with TTL decay; policy controls; tamper-evident audit. VERIFIED (abstract). "preliminary" per DOCX not re-confirmed.
- MI9 (Wang C. L., Singhal, Kelkar, Tuo; 2508.03858; also OpenReview TseVPnC26W). six components (ARI, agent-semantic telemetry, continuous authorization monitoring, FSM conformance, goal-conditioned drift detection, graduated containment); >1,000 synthetic scenarios (v2.0: 1,033), high detection low FPR. VERIFIED (abstract). Title changed between versions (v1/v2 "MI9 - Agent Intelligence Protocol: Runtime Governance for Agentic AI Systems").
- ProbGuard (Wang H., Poskitt, Wei J., Sun J.; 2508.00500; formerly Pro2Guard). symbolic state abstraction; learns DTMC from traces; intervene when probability of remaining safe falls below user threshold; PAC-style guarantees; LangChain; AV warnings up to 38.66 s ahead; embodied: unsafe behaviour reduced up to 65.37% while preserving up to 80.4% completion. ASE 2026 acceptance (DOCX) NOT confirmed this session -> cite as preprint. Latest title "ProbGuard: Probabilistic Runtime Monitoring for LLM Agent Safety" (v3) vs "ProbGuard: Proactive Runtime Monitoring for LLM Agent Safety via Probabilistic Prediction".
- Thought-Aligner (Jiang C. et al.; 2505.11063). Accepted ICML 2026 (confirmed via arXiv comment snippet). ~50% -> ~90% behavioural safety average; ~23% above SOTA guardrails; ~5% helpfulness; ten risk scenarios; six LLMs; low per-step latency. v2.0 "sub-100 ms" not re-confirmed -> drop.
- Progent (2504.11703). Current arXiv title "Progent: Securing AI Agents with Privilege Control"; earlier "Programmable Privilege Control for LLM Agents". Authors Tianneng Shi, Jingxuan He, Zhun Wang, Linyu Wu, Hongwei Li, Wenbo Guo, Dawn Song (order Wu/Li per snippet; DOCX has Li H., Wu L. order -> use snippet order, flag). DSL of symbolic rules over tool names+args; SMT: narrowing auto / expansion requires approval -> monotonic confinement. ASR 39.9%->1.0% AgentDojo; 70.3%->3.9% ASB. VERIFIED (abstract).
- CaMeL (Debenedetti, Shumailov, Fan, Hayes, Carlini, Fabian, Kern, Shi, Terzis, Tramèr; 2503.18813v2, 24 Jun 2025). Preprint (no venue found). Current abstract: 77% with provable security vs 84% undefended in AgentDojo; an earlier version reported 67%. Use 77/84 with version note.
- Jackson, Freeman (SSRN 5904104; 13 Nov 2025). Abstract: governed-action model (inference, tool usage, data access, external actuation); multi-dimensional risk scoring aligned w/ AI RMF; deterministic enforcement state machine with allow/deny/sanitize/escalate decisions with auditable safety/liveness properties; OPA/Envoy/K8s; append-only evidence store; "significant reductions in unsafe actions with minimal latency overhead" (no numbers in abstract). PARTIALLY VERIFIED (abstract only; full text not accessed). v2.0 "Jackson, F." -> Freeman Jackson.
- AgentSpec: ICSE '26, DOI 10.1145/3744916.3764546; >90% code-agent unsafe prevented; all hazardous embodied actions eliminated; 100% AV compliance; ms overheads. VERIFIED. (95.56%/70.96% LLM-generated rules: from DOCX/v2.0; not re-confirmed this session.)
## Crossref-verified metadata (FULLY VERIFIED metadata)
- Page 1954 Biometrika 41(1-2) 100-115 doi 10.1093/biomet/41.1-2.100
- Greshake et al. 2023 AISec pp.79-90 doi 10.1145/3605764.3623985
- Chow 1970 IEEE TIT 16(1) 41-46 doi 10.1109/TIT.1970.1054406
- Chandola 2009 ACM CSUR 41(3) 1-58 doi 10.1145/1541880.1541882
- Chandola 2012 IEEE TKDE 24(5) 823-839 doi 10.1109/TKDE.2010.235 (NEW)
- Cox 1958 JRSS-B 20(2) 215-232 doi 10.1111/j.2517-6161.1958.tb00292.x (NEW)
- Zadrozny & Elkan 2002 KDD 694-699 doi 10.1145/775047.775151 (NEW)
- Niculescu-Mizil & Caruana 2005 ICML 625-632 doi 10.1145/1102351.1102430 (NEW)
- Wald 1945 AMS 16(2) 117-186 doi 10.1214/aoms/1177731118 (NEW)
- Lorden 1971 AMS 42(6) 1897-1908 doi 10.1214/aoms/1177693055 (NEW)
- Naeini 2015 AAAI 29(1) doi 10.1609/aaai.v29i1.9602
- Forrest et al. 1996 IEEE S&P 120-128 doi 10.1109/SECPRI.1996.502675 (NEW)
- Sommer & Paxson 2010 IEEE S&P 305-316 doi 10.1109/SP.2010.25 (NEW)
- Schneider 2000 ACM TISSEC 3(1) 30-50 doi 10.1145/353323.353382 (NEW)
- Brier 1950 MWR 78(1) 1-3 doi 10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2 (NEW)
- Yu et al. 2025 KDD V.2 6216-6226 doi 10.1145/3711896.3736561 (12 authors confirmed)
- L. Wang et al. 2024 FCS 18(6) 186345 doi 10.1007/s11704-024-40231-1 (13 authors confirmed)
- Tsai & Bagdasarian 2025 HotOS pp. 8-17 doi 10.1145/3713082.3730378 (v2.0 lacked pages)
- Hua et al. 2024 Findings EMNLP 10000-10016 doi 10.18653/v1/2024.findings-emnlp.585
- Rebedea et al. 2023 EMNLP demo 431-445 doi 10.18653/v1/2023.emnlp-demo.40
- Zhan et al. 2024 InjecAgent Findings ACL 10471-10506 doi 10.18653/v1/2024.findings-acl.624
- Luo et al. 2025 AGrail ACL long 8104-8139 doi 10.18653/v1/2025.acl-long.399
- Arp et al. 2022 USENIX Sec (no DOI; Crossref shows later CACM 2024 / IEEE S&P mag 2023 versions) -> verify pages via web
## Web-verified (venue + abstract claims)
- AgentHarm ICLR 2025: 110 malicious tasks (440 w/ augmentations), 11 harm categories; requires multi-step capability retention after jailbreak.
- StruQ: Chen S., Piet, Sitawarin, Wagner; USENIX Security 2025; separates prompt/data channels; structured instruction tuning. (NEW)
- Adaptive attacks: Zhan Q., Fang R., Panchal H.S., Kang D.; Findings NAACL 2025, pp. 7116-7132; eight IPI defenses all bypassed. (NEW)
- Task Shield: Jia F., Wu T., Qin X., Squicciarini A.; ACL 2025 long (2025.acl-long.1435); verifies each instruction/tool call contributes to user goals; AgentDojo ASR 2.07%, utility 69.79% on GPT-4o. (NEW)
- MELON: Zhu K., Yang X., Wang J., Guo W., Wang W. Y.; ICML 2025 PMLR 267; masked re-execution + tool comparison. (NEW)
- ShieldAgent: ICML 2025 PMLR 267:8313-8344 (DOCX listed as preprint -> upgraded).
- GuardAgent: ICML 2025 PMLR 267:68316-68342 (DOCX "accepted" -> upgraded).
- AgentDojo: NeurIPS 2024 D&B; 97 tasks, 629 security test cases; Workspace, Slack, Travel, Banking; jointly measures utility and security.
- AgentPoison: NeurIPS 2024; avg ASR >=80%, benign impact <=1%, poison rate <0.1%; three agents (autonomous driving, QA, EHRAgent).
- ASB: ICLR 2025; 10 scenarios incl. finance; 10 agents; >400 tools; 27 attack/defense methods; 7 metrics; 13 backbones; highest avg ASR 84.30%; defenses often ineffective. v2.0 "memory poisoning lowest 7.92%" NOT re-confirmed -> dropped.
- ToolEmu: ICLR 2024; 36 toolkits, 144 cases; safest agent fails 23.9%; 68.8% valid.
- Liu Y. et al. USENIX Sec 2024 pp.1831-1847; 5 attacks, 10 defenses, 10 LLMs, 7 tasks.
- Arp et al. USENIX Sec 2022 pp.3971-3988; 30 papers from top-tier security venues over 10 years.
- Perez & Ribeiro 2022 NeurIPS ML Safety Workshop (best paper); goal hijacking, prompt leaking; arXiv 2211.09527.
- Hines et al. 2024 spotlighting: >50% -> <2% GPT-family, minimal task impact.
- LlamaFirewall: PromptGuard 2, Agent Alignment Checks, CodeShield. v2.0 "83%"/"96%" not re-confirmed -> dropped.
- Chen Z., Chen J., Chen J., Sra M. 2502.15865: current title "Standard Benchmarks Fail -- Auditing LLM Agents in Finance Must Prioritize Risk" (v1: "Position: Standard Benchmarks Fail - LLM Agents Present Overlooked Risks for Financial Applications"); position paper; venue NOT confirmed -> preprint; accuracy/return metrics illusion; hallucinated facts, stale data, adversarial prompt manipulation; three-level agenda; audit of six agents on three tasks. v2.0 "ten overlooked categories incl. interpretability" not re-confirmed -> dropped.
- Kull et al. AISTATS 2017 PMLR 54:623-631; logistic family excludes identity; beta calibration = bivariate LR on ln s, ln(1-s); a=b -> logistic on log-odds (follows from functional form).
- Guo et al. ICML 2017 PMLR 70:1321-1330; temperature scaling single-parameter variant of Platt scaling.
- Elkan IJCAI 2001 pp. 973-978; lowest expected cost prediction.
- Lundberg & Lee NIPS 2017 pp. 4765-4774 (Linear SHAP corollary: from paper, not re-read this session).
- Platt 1999 Advances in Large Margin Classifiers pp. 61-74 MIT Press; sigmoid fit to SVM outputs.
- EU AI Act Art. 12 automatic recording of events over lifetime; Art. 14 effective oversight; intervene/interrupt via stop button to halt in safe state. VERIFIED.
- OWASP LLM01:2025: direct vs indirect prompt injection; #1 in 2025 list. VERIFIED.
- SoK Agentic Commerce (Mao Q., Wang J., Liu Y., Zhu L., Ma C., Yan J.; 2604.15367; preprint): five dimensions (agent integrity, transaction authorization, inter-agent trust, market manipulation, regulatory compliance); 12 cross-layer attack vectors; failures propagate from reasoning/tooling into custody, settlement, market harm, compliance; layered defense architecture. (NEW)
- ReAct ICLR 2023; Toolformer NeurIPS 36 (2023); Llama Guard (Inan et al. 2023 preprint): Llama2-7b, input/output classification with taxonomy.
- Author corrections: FinHarness = Haoxuan Jia, Yang Liu, Bin Chong, Yingguang Yang, Yancheng Chen, Jiayu Liang, Qian Li, Hanning Lu, Kefu Xu, Hao Zheng, Chongyang Zhang, Hao Peng, Philip S. Yu (matches DOCX). DreamGuard = Wenhao Lin, Chenyu Yu, Xingwei Lin, Sicong Cao, Xiang Chen, Lei Xue, Le Yu, Letian Sha, Chunming Wu (matches DOCX; 6 Aug 2026). Y. Wang = Youting Wang, Xiao Han, Dingyan Shang, Yuan Tang, Bowen Liu (matches DOCX). Cordon = Zheng Chen, Dong Dong, Hanqing Liu, Jialin Li, Jidong Zhai, Duling Xu, Bangzheng Pu (ORDER differs from DOCX -> flag). H.-H. Chen = Hao-Hsuan Chen (search summary; single-source -> flag).
## Not re-checked this session (carried from prior DOCX audit): Basseville & Nikiforov 1993 (book); AgentTrust internals (max-severity aggregation, step-function confidence, reversibility rubric); NEXUS internals (128/60 split, 99 features, rule cascade, expected-loss objective, upper-bound caveat); SafeAgent action space & no-calibration/no-latency; AgentSpec 95.56/70.96; PRISM "preliminary"; Jiang et al. author list.

## Late additions
- NEXUS: F1 0.949; 4-class intervention accuracy 0.6406; +27.3 pp over rule-only intervention selection; 128-instance synthetic benchmark (retrieved abstract/HTML snippet).
- AgentTrust: LLM judge evaluates five risk dimensions (data exposure, system impact, credential risk, scope creep, reversibility). NOTE: a different 2026 preprint shares the name ('AgentTrust: A Self-Improving Trust Layer for AI-Agent Actions', arXiv 2606.08539); it is not cited.
- AgentHarm authors confirmed (14 authors incl. Winsor, Wynne).
- Thought-Aligner authors confirmed: Changyue Jiang, Wenqi Zhang, Xudong Pan, Geng Hong, Min Yang; v1 abstract: latency below 100 ms; current abstract: 'low per-step latency'.
- InjecAgent re-checked (24 Sep): 1,054 cases; 17 user tools; ReAct GPT-4 24%; nearly doubles with hacking prompt. One secondary summary says '62 attacker instructions' where the abstract says '62 attacker tools' — chapter keeps 'attacker tools'.
