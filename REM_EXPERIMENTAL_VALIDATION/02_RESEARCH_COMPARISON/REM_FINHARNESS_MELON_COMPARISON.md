# REM, FinHarness and MELON — Verified Comparison

**Evidence labels:**
- **[P]** the paper or its record (metadata and abstract);
- **[C]** source code inspected in this project;
- **[A]** assumption;
- **[U]** unverified;
- **[R-proposed]** proposed REM contribution;
- **[R-shown]** REM contribution shown empirically in this project.

## 1. Sources and their verification status

| System | Primary source | What was verified |
|---|---|---|
| MELON | Zhu, Yang, Wang, Guo & Wang, *MELON: Provable defense against indirect prompt injection attacks in AI agents*, ICML 2025 (PMLR 267; arXiv:2502.05174). Already in the thesis reference list | **Code:** `github.com/ucsb-mlsec/MELON` (commit `06014c7`, 2025-07-01) and `github.com/kaijiezhu11/MELON` (commit `4d3cc9c`, 2025-07-31). The implementation file `pi_detector.py` is **byte-identical** in both (sha256 `5a7f6b28…`). No licence file in either. The ucsb-mlsec README's integration snippet names a class `ContrastPIDetector` that does not exist in the file (the class is `MELON`). The paper's full text was not read in this session (arxiv.org is blocked by the network policy) |
| FinHarness | H. Jia et al., *FinHarness: An inline lifecycle safety harness for finance LLM agents*, arXiv:2605.27333 (submitted 26 May 2026; 13 authors including C. Zhang, H. Peng, P. S. Yu). Already in the thesis reference list (record-verified) | Metadata and abstract-level claims only (earlier record verification, plus a search-engine record on 5 Nov 2026). **No official code repository was found**: none in the search results, and the full text, where a link might appear, is unreachable (arxiv.org blocked). **Not reproducible as a baseline here.** Its evaluation benchmark, FinVault, is a withdrawn preprint (thesis §2.10) |

## 2. Mechanisms

| Aspect | MELON | FinHarness | REM |
|---|---|---|---|
| Threat model | Indirect prompt injection in tool outputs [P][C] | Financial-agent risks including injection; query- and tool-level [P] | Indirect prompt injection leading to attacker-serving state-changing financial calls (§3.3) |
| Where it acts | Inside the agent loop after each tool output; it makes the agent's next LLM call itself [C] | Inline lifecycle harness: Query Monitor, Tool Monitor, Cascade [P] | Tool-execution boundary: every proposed call before execution [C] |
| Evidence | Similarity (cosine > 0.8, `text-embedding-3-large`) between tool calls proposed with the user prompt masked and unmasked [C] | Single-turn intent, cross-turn drift, tool-call checks, per-step risk [P] | Provenance, behavioural and action features → ridge logistic probability [C] |
| Probability / calibration | None; a binary similarity decision. The constructor's `threshold=0.1` is unused [C] | Per-step risk score [P]; calibration [U] | Logit calibration with γ₁ > 0 [C]; ECE 0.044 held-out [measured] |
| Decision | Binary: stop the agent on detection [C] | Routing to a lightweight or advanced **LLM judge**; risk factors fed back to the agent, which may refuse, re-plan or approve [P] | Expected-loss argmin over Allow / Modify / Escalate / Block with tier-indexed costs [C] |
| Response | Replaces the agent's proposed calls with a stop message; masks the last tool output [C] | Agent-side refusal or re-planning guided by evidence [P] | Withholds the call; refusal to the agent; audit record [C] |
| Model calls added | One masked LLM call per loop iteration, plus embedding calls [C] | LLM-judge calls (fewer with routing) [P] | **None**: local computation, about 0.18 ms per call [measured] |
| Cross-turn state | Bank of masked tool calls within an episode [C] | Cross-turn drift monitoring [P] | Episode history features; optional observe-only CUSUM [C] |
| Reported evaluation | AgentDojo [P, abstract level]. The README's example command uses `gpt-4o-2024-05-13` [C]. The full set of backbones and suites in the paper is [U] (full text not read) | FinVault: ASR 38.3% → 15.0%, benign approval 41.1% → 39.3% with routing [P] | Exploratory: recorded AgentDojo banking traces of 21 agents; replay and deployment simulation |
| Code available | Yes (no licence) | Not found | Yes (this repository) |

## 3. What can and cannot be claimed

- **[R-proposed]** An integrated, non-invasive runtime layer that combines a calibrated per-call probability with consequence-tiered expected-loss verdicts, deterministic mitigation and an audit record, for financial agents.
- **[R-shown]**, exploratory, on recorded banking traces:
  - held-out discrimination (ROC-AUC 0.938);
  - the replay trade-off against no defence and against the same-estimator internal baseline B1 (difference attributed to the decision policy as a whole);
  - deployment as a separate service without changing any decision, at sub-millisecond decision cost.
- **Not shown:**
  - protection of live or adaptive agents;
  - any comparison with MELON or FinHarness under matched conditions (none was executed);
  - any superiority claim.
- **Overlap:**
  - FinHarness shares the domain (finance), the placement (inline, per step) and graded responses with escalation, but its escalation goes to an LLM judge, not a human.
  - MELON shares the runtime placement and the goal of stopping injected actions.
  - REM is **not** the first runtime security framework for financial agents.
  - None of REM's mechanisms (logistic regression, logistic/Platt calibration, Bayes expected-loss decisions, linear SHAP) is new.
