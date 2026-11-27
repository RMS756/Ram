# 07: Is another experiment necessary?

## 1. Can the existing evidence answer the research questions?

The research questions are those in the thesis (Ch. 1 §1.7, still marked [PD]), plus the contribution claims in 05.

| Question | Answerable now? | Evidence |
|---|---|---|
| RQ1: discrimination and calibration of the estimator under grouped cross-fitting | **Yes** | Cross-fit ROC-AUC 0.938, ECE 0.044 (re-run in this audit, identical) |
| RQ2: expected-loss vs threshold policy | **Yes, in replay** | P1 and P3 contrasts (02 §2, 05 A2) |
| RQ3: residual attack success after mitigation; escalation frequency; overhead | **Partly.** Replay residual and per-call time are measured. Escalation is meaningless without a reviewer (verdicts coincide). Live residual: **not answerable** | 02 §1, §3 |
| RQ4: marginal contribution of each component | **Yes, in replay** | Pre-registered ablation (02 §1.2) |
| C1: nominal layering is not depth in REM v1.0 | **Yes, in replay** | Ablation |
| C2: learned decision adds nothing over rules / behind authorization | **Yes, in replay and development data** | Confirmatory rule baselines; studies listed in 05 |
| C3: replay measurement pitfalls | **Yes for P1.** For P3, the withhold-everything floor has not been computed | 02 §1.3 |

**Conclusion.** The defensible thesis position (08) can be established **with the existing evidence**, provided every claim is scoped to NO-ADAPT replay on AgentDojo banking.

**No new framework, version or detector is needed.**

## 2. Is any additional experiment essential?

**No experiment is essential** for the recommended position.

One small **offline re-analysis** is recommended, because it closes a specific gap that this audit itself opened. One live experiment is **optional** and depends on resources that are currently blocked.

### 2.1 Recommended (small, offline, no model): the withhold-everything reference arm on P2 and P3

| Item | Specification |
|---|---|
| Research question | On the second population (P3), does REM v1.0 complete any benign task, or any task under attack, that a policy withholding every state-changing call would not? |
| Gap | 02 §1.3 shows that on P1 REM v1.0's benign successes are exactly the withhold-everything set. On P3 this was not computed (the DiD-3 gateway-failure arm ran on P1 only) |
| Why existing data cannot answer it | No stored arm withholds every state-changing call on P2 or P3 |
| Minimum design | Replay of P2 and P3 with one extra arm in the existing frozen harness: release no call of a state-changing tool. Paired with the stored REM v1.0 arm on identical episodes. **Freeze the arm definition before running** |
| Baselines | B0 (no defense); REM v1.0 (stored) |
| Data and metrics | P2 (681 attacked), P3 (2,065 attacked + 48 benign). Metrics, per episode: benign completion, utility under attack, replay attack outcome. Episode-set comparison as in 02 §1.3 |
| Expected outputs | Counts and the set difference: episodes REM completes that the floor does not, and the reverse |
| What it would support | Whether the "REM utility = replay floor" finding generalizes beyond P1. That decides how Chapter 4's utility statements must be worded |
| What it would not support | Any statement about live utility, adaptive attackers, or other benchmarks |
| Cost | Minutes of CPU. Uses the harness re-run in this audit. No model call |

**This audit did not run it,** per the instruction not to run new experiments.

### 2.2 Optional (only if the supervisor requires live evidence): a closed-loop check of REM v1.0

| Item | Specification |
|---|---|
| Research question | When a live agent receives REM's refusals, are attack success and task completion close to the replay estimates? |
| Gap | Every REM outcome is NO-ADAPT replay. A refused call cannot lead the agent to retry, rephrase or abandon. Replay utility is insensitive to tasks that need writes (02 §1.3) |
| Why existing data cannot answer it | No live run exists (`REM_MELON_COMPARISON_2026_11_19`, `REM_ABLATION_STUDY/03`: NOT EXECUTED) |
| Minimum design | AgentDojo 0.1.35 banking; arms: no defense, REM v1.0, **one deterministic baseline** (rule P2, or Progent's manual policy, labelled as an oracle list). Same agent, same tasks, same injection template |
| Blocked items | Backbones, number of repeats, budget: **[DESIGN BLOCKED]** under CLAUDE.md. **No value is proposed here** |
| Statistics | Pairing by (user task, injection task); clustering as in the thesis. Choices are the researcher's |
| What it would support | Whether replay conclusions C1–C2 hold directionally for the chosen backbone(s) |
| What it would not support | Robustness against adaptive attackers. Generality across models or domains. **Any superiority over published defenses** |

**Not recommended:**
- live financial transactions;
- deployment against real banking systems;
- new REM versions;
- the REM-X evaluation protocol.

None addresses a gap in the recommended contribution.
