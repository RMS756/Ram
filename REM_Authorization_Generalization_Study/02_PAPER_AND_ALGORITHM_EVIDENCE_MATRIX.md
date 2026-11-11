# 02 — Paper and algorithm evidence matrix

**Source versions.** Six PDFs supplied by the candidate on 11 November 2026 (SHA-256 in `papers_provided/SHA256SUMS.txt`). `arxiv.org` is blocked in this session, so nothing was fetched from the web. Every equation below was read in the supplied full text. Section, equation and page locations refer to those PDFs.

**Verification status key.** FULL = method, equations, experiments and limitations read in the supplied full text. NOT READ = not supplied and not retrievable here; nothing is asserted about its equations.

## 1. Primary papers

### Paper A — PROVISO

| Field | Content |
|---|---|
| Paper | Bo Yan, Qi Zhang, Ziwen Kan, Fnu Suya, Song Wang, "PROVISO: Provenance-Informed Action Selection for Secure LLM Agents" |
| Publication | arXiv:2610.27115v1, October 2026, preprint |
| Verification | **FULL** |
| Problem setting | Decision at the *commitment point*: after the policy proposes an action and before the executor runs it (Sec. 3.1). Observations are split by provenance into trusted K (task contract: objective O, permitted scope S, authorized resources or recipients R, terminal condition T) and external G. |
| Authorization statement (Sec. 3.1, displayed rule) | "An action is admissible when its operation and target are licensed by K and its arguments are supported by K ∪ G. External observations may supply values, but they cannot change the objective." |
| Eq. (1), Sec. 3.1 | V*(x, a) = E[ y(x, a) \| x, a ], where x = (K, G, P0, P1), P0 the proposed action, P1 an alternative, and y ∈ [0, 1] the deployment's native outcome. The controller commits the action with the highest value. |
| Eq. (2)–(6), Sec. 3.2 | Adapter → provenance-typed memory m_j = W z_j + b + e_{r_j} (Eq. 3) → five role queries Q⁽⁰⁾ = [q_K; q_G; q_P0; q_P1; q_C] (Eq. 4) through L deliberation blocks (Eq. 5) → value readout V̂(x, P_c) = g_ρ([q_K; q_G; q_Pc; q_C]) (Eq. 6). |
| Admission form (Sec. 3.2, Stage 3) | When P1 is a refusal: with p(x) the probability that P0 is unsafe, V*(x, P1) − V*(x, P0) = 2p(x) − 1; V̂(x, P0) = 0, V̂(x, P1) = p̂(x) = σ(h_ρ(q_C)). |
| Eq. (7) | U(x, a) = V̂(x, a) − τ_a; a* = argmax_a U(x, a). Offsets τ are "chosen on development data"; "calibration here means selecting an operating point, not adjusting predicted probabilities". In admission, P0 is blocked whenever p̂(x) > τ_P1. |
| Training | Per deployment, on native outcomes: binary cross-entropy (plus a pairwise ranking term in candidate selection); frozen ModernBERT-large encoder; 17.40M trainable parameters; AdamW (Sec. 4, Implementation Details). |
| AgentDojo evidence | Candidate selection between the agent's trajectory and a recovery trajectory, both rolled out from the start in a restored environment; agent is Gemma 4 31B IT; 2,516 attacked and 97 clean episodes over all four suites; five folds "keep all attack variants of a user task together" (Appendix; Table 7). Table 4: benign utility 87.63, utility under attack 85.41, targeted ASR 0.28. A controlled payment task on the AgentDojo banking tools is used for one component analysis (Sec. 5.3, App. F.3). |
| Stated limitations (Limitations section) | "fitted separately for each benchmark and therefore requires labeled outcomes from the target setting; we do not study transfer of a single trained controller across tasks"; candidate selection needs restorable rollouts of both continuations; roles are assigned by benchmark-specific adapters; one agent LLM; "attacks adapted to PROVISO itself are not evaluated". |
| Code | No repository for PROVISO is named in the supplied text. |
| Applicability to REM | (i) The admissibility statement supports testing identity arguments (recipient, credential) against trusted user text while letting values such as amounts come from external content. (ii) In admission form, the decision is a threshold on an unsafe-probability chosen on development data. REM's B1 baseline is the same decision form with a different selection criterion. (iii) The typed-memory controller itself cannot be reproduced here (see `04`). |
| REM adaptation actually used | Only the admissibility statement, as the rationale for the deterministic evidence `z_exp` (protocol section 4). No PROVISO equation is implemented. |

### Paper B — AgentBoundary

| Field | Content |
|---|---|
| Paper | Yang, Mi, Huang et al. (7 authors), "AgentBoundary: Counterfactual Evaluation of Safety in Tool-Using LLM Agents" |
| Publication | arXiv:2609.33658v1, September 2026, preprint |
| Verification | **FULL** |
| Method | Four-way counterfactual task families that vary *apparent risk* and *action permissibility* independently on the same executable workflow: Easy-Benign, Hard-Benign (risky-looking but authorized), Covert-Malicious (routine-looking but unauthorized), Harmful-Source (Sec. 4.1). |
| Eq. (3), Sec. 3 | max_π E_{e∼D_B}[S_J(e, τ)] subject to E_{e∼D}[U_J(e, τ)] ≤ ε: maximize authorized-task success subject to a bound on unsafe behaviour. "task utility, unsafe behavior, and over-refusal are reported separately". |
| Eq. (6)–(8), App. D | Binarized utility and safety per trajectory; HB-Utility and CM-Safety as pass counts over valid scored trajectories. |
| Findings | "high safety frequently coexists with poor authorized-task completion" (abstract); e.g. GPT-5.5 blocks 99.5% of routine-looking unauthorized actions but completes 28.7% of risky-looking authorized tasks (Table 2). |
| Mitigation | An LLM "Thought aligner" (Qwen3-14B) that rewrites the agent's current Thought (Eq. 5, 9, 10). App. H: "It does not claim a formal guarantee". |
| Applicability to REM | The *evaluation design* is reusable: report authorized completion and unsafe blocking separately on matched pairs, and state the objective as utility under a safety constraint. This study's fixture pairs (legitimate vs substituted call on the same scaffold) and its separate reporting follow that design. The mitigation is an LLM component and is not reusable in REM (the design lock forbids LLM arbitration; no model is available). |
| REM adaptation actually used | Reporting structure only (authorized-action approval reported separately from attack outcomes; no scalar that trades one against the other). |

### Paper C — Calibration Is Not Control

| Field | Content |
|---|---|
| Paper | Zhang, Wan, Yu, Wu, Wen, Zhou, Zhao, Tsang, "Calibration Is Not Control: Intervention Value for LLM-Agent Oversight" |
| Publication | arXiv:2606.21399v2 (6 Oct 2026); header states NeurIPS 2026 |
| Verification | **FULL** (paper). The code repository named in the abstract (`github.com/bennidict23/calibration-is-not-control`) was **not accessed**. |
| Eq. (1), Sec. 2.1 | p_fail(h) = Pr(U_continue(h) ≤ 0 \| h); τ_i(h) = Q_i(h) − Q_continue(h), with Q_a(h) = E[U_a(h) \| h]. Optimal action A*(h) = argmax_{a∈A} Q_a(h). |
| Definition 1 / Proposition 1 | A summary g is *sufficient for control* iff a rule on g(h) selects an optimal action almost surely; in the binary case iff the sign of τ(h) is recoverable from g(h). |
| Eq. (2), Prop. 2 (App. A.2) | Gap(g) = V* − V_g = E[ E[max_a Q_a(h) \| g(h)] − max_a E[Q_a(h) \| g(h)] ] ≥ 0. |
| Remark 1 (Sec. 2.2; proof App. A.5) | For a strictly increasing continuous T, {h : T(g(h)) > T(t)} = {h : g(h) > t}: recalibration preserves the threshold policy class. Stated scope: "It concerns representable policies, not a fixed numerical threshold, a finite-sample threshold search, or rules that use probabilities and costs directly". |
| Eq. (3), Sec. 4.2 | Offline regret R̂(π) = (1/N) Σ_j [ max_a u_a(h_j) − u_{π(h_j)}(h_j) ]. |
| Prefix branching (Sec. 3) | Replay to a decision prefix, execute every candidate action from it, record downstream utilities; "the execution policy after each action fixed within a suite"; the deployed controller does not branch. |
| Utility (App. C.1, Table 4) | U_a(h) = outcome score − c_a − s·(branch steps) for continue/intervene; 0 for quit. Costs are declared constants. |
| Matched-target ablation (Sec. 5.2, App. D.1) | Same 26 features, same estimator, same router; only the supervision label changes. On ALFWorld, failure label → intervention utility lowers regret 0.513 → 0.094; "Both values (pair router)" 0.069. |
| Stated limits | Gains "depend on intervention value and are small on two reasoning benchmarks"; strong results "concentrated on ALFWorld"; no security benchmark is evaluated. |
| Applicability to REM | Direct. REM predicts an attack-attempt probability and routes on it; this paper says to supervise on the outcome of each available action at the same state. REM's replay harness can produce exactly such branch outcomes (release vs withhold one call, the rest of the recorded trajectory fixed). Remark 1 is also the published form of this project's earlier finding that thresholds re-selected on uncalibrated scores give identical verdicts to B1. |
| REM adaptation actually used | Arms M11, M11y, M11+AZ (see `05`). **DERIVED — NOT DIRECTLY QUOTED FROM THE SOURCE:** the branch utilities are written in REM's declared costs and the action set is {release, withhold}. |

### Paper D — CASEL

| Field | Content |
|---|---|
| Paper | Zhang, Shen, Yan, Zhang, "CASEL: Consequence-Aware Selective Execution for Reliable Long-Horizon Tool-Using Agents" |
| Publication | arXiv:2610.36570v1 (27 Oct 2026), preprint |
| Verification | **FULL** |
| Eq. (1)–(2), Sec. III | p_t = P(F_t = 1 \| h_t, a_t, s_t); with consequence c_t ∈ [0, 1], m*_t = argmin_{m∈M_t} [ p_t^(m) c_t + λ k(m) + μ q(m) ], over modes {direct, verify, sandbox, clarify, approve, abstain}. |
| Eq. (4), Sec. IV-A | ĉ_t = clip(c_base(z_t) · M_scope(θ_t, h_t), 0, 1). |
| Sec. IV-B | p̂_t^(m) = γ_m(ξ_t) p̂_t, so J(m) = γ_m r̂_t + λ k(m) + μ q(m) with r̂_t = p̂_t ĉ_t. |
| Eq. (5), Prop. 1 | Finite-sample direct-execution threshold: R̂(τ) + sqrt(ln(K/δ)/(2 n_τ)) ≤ ε, valid for i.i.d. records, one record per trajectory. |
| Evidence | **Simulation only** (20 seeds, 120,000 simulated test actions each). "Intervention effectiveness is assumed, not measured" (abstract). The γ_m, k(m), q(m) values "are assumed constants" (Sec. VI-A). |
| Authors' own negative findings | "The per-mode cost J(m) therefore does not reduce harm beyond a product-score gate" (Sec. VI-B); the trajectory budget "increases harm at equal cost". |
| Stated limits | "CASEL is an allocation policy, not a safety guarantee"; evaluations on AgentDojo and other benchmarks are "Planned (not yet run)" (Sec. VIII). |
| Applicability to REM | CASEL's Eq. (2) has the same structure as REM's expected-loss rule: a residual-risk term per mode (REM: r_mod·C_miss for Modify) plus a mode cost (REM: C_mod, C_esc). It is an independent, later statement of the same decision form, not a source of a better one, and it has no measured intervention effectiveness. It gives no AgentDojo numbers to compare with. |
| REM adaptation actually used | None. Cited as a structurally equivalent decision-cost formulation and for its explicit warning that intervention effectiveness must be measured. |

## 2. Tier-2 defences supplied in full text

### Task Shield

| Field | Content |
|---|---|
| Paper | Jia et al., "The Task Shield: Enforcing Task Alignment to Defend Against Indirect Prompt Injection in LLM Agents", ACL 2025 (long paper 1435) |
| Verification | **FULL** |
| Formalization | Def. 1 (task instruction); Eq. (1) E_L(M′) = ∪ E(M_i) over messages at privilege level L; Def. 2 ContributesTo(e, t \| H_i); Def. 3 / Eq. (2): an instruction e satisfies the alignment condition if some user-level t has ContributesTo(e, t) = True; Def. 4 task alignment. Alignment check: S(e) = Σ_{t∈T_u} s(e, t) with s ∈ [0, 1] returned by an LLM; misaligned ⇔ S(e) = 0. |
| Relevant remark | Sec. 3.2: a tool output can "merely supply supporting information or define new subtasks" when the user delegates ("Complete my to-do list tasks"). This is the delegated-source case that `z_del` tries to capture deterministically. |
| AgentDojo banking, GPT-4o, Important Instructions (Table 2a) | Clean utility 81.25, utility under attack 82.64, ASR 6.25; no defence 75.00 / 69.44 / 62.50. |
| Stated limits | Relies on a powerful LLM for extraction and scoring; extra LLM calls for every message; one model family on one benchmark. |
| Evaluable here? | **No**: both shield components are LLM calls; no model API is available. |

### MELON

| Field | Content |
|---|---|
| Paper | Zhu et al., "MELON: Provable Defense Against Indirect Prompt Injection Attacks in AI Agents", ICML 2025 (PMLR `zhu25z`) |
| Verification | **FULL** |
| Method | Re-executes the trajectory with a masked user prompt and compares the tool calls of the original and masked runs by embedding similarity. |
| AgentDojo, GPT-4o, all suites (Table 1) | MELON: benign utility 68.04%, utility under attack 32.91%, ASR 0.95% (Important Messages); MELON-Aug 76.29% / 52.46% / 1.27%. No banking-only figures are given in the main table. |
| Stated limits | Misses response-based attacks, tool-call redundancy, state hallucination (failure analysis of 66 cases). |
| Evaluable here? | **No**: needs the agent LLM and an embedding model. This project's MELON + REM integration exists and is verified with scripted agents only; no live run has been made. |

## 3. Additional literature named in the request

| Work | Status in this study |
|---|---|
| AgentDojo (Debenedetti et al., NeurIPS D&B 2024) | Used as the environment; verified earlier in this project from the installed package and recorded runs. |
| CaMeL (Debenedetti et al., 2025, arXiv:2503.18813) | **NOT READ in this session.** Cited by PROVISO as a system-level defence. No equation or number from it is used. |
| NEXUS, AgentTrust, ProvenanceGuard | Covered by the project's earlier prior-art reconciliation (`STAGE2_5_PRIOR_ART_RECONCILIATION.md`, `V1_NEXUS_DIRECT_VERIFICATION.md`); not re-read here. |
| KAIROS, FinHarness | **NOT READ.** Earlier project audits recorded FinHarness as not locatable; nothing is asserted. |
| DelegationBench (Pochampally, arXiv:2610.05532) | Abstract only (OpenAlex). Relevant finding in the abstract: a keyword rule written after seeing the benchmark agreed with annotators more often than eight models, yet changed its decision in only 9 of 48 matched pairs. Not used. |

**Search limits.** A literature search to 11 November 2026 could be run only through an OpenAlex connector (abstract level). It confirmed the four primary records and surfaced DelegationBench. It is not a systematic search, and newer competing work may exist.
