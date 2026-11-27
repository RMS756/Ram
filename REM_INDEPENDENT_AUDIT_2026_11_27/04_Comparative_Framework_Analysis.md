# 04: Comparative framework analysis

**Labels.**

| Label | Meaning |
|---|---|
| **Yes** | Explicitly implemented, and supported by evidence at the level shown |
| **Partial** | Limited implementation or coverage |
| **No** | Explicitly absent |
| **Unknown** | Insufficient evidence |

**Evidence level per column:**

| Column | Basis |
|---|---|
| REM v1.0 | Code and data verified by this audit |
| REM-DiD | Code, plus exploratory replay with **oracle** authorization |
| REM-X | **Design only**: nothing is implemented, so every implementation cell is "No (design)" |
| ROPE | R (code and authors' logs) |
| AGATE | A/S |
| Progent | F (earlier) and R |
| MELON | A and R |

**Reading rule.** Detection, authorization, prevention, mitigation and post-execution monitoring are different functions and are kept apart. A "Yes" for detection is never counted as a "Yes" for authorization.

## 1. Matrix

| Capability | REM v1.0 | REM-DiD | REM-X | ROPE | AGATE | Progent | MELON |
|---|---|---|---|---|---|---|---|
| **Threat model** | IPI via tool outputs; single agent; banking; **non-adaptive attacker in the primary evaluation** (thesis AS-6) | Same + bypass and failure scenarios (modelled) | Financial transaction integrity incl. delegated documents (design) | IPI incl. paraphrase, adaptive, long-horizon | Compositional attacks from ordinary operations | IPI causing unauthorized tool calls; adaptive attacks | IPI redirecting the agent's next action |
| **IPI coverage (evaluated)** | Partial: AgentDojo banking, static templates, **replayed** | Partial: same recordings, replayed | No (design) | Yes: AgentDojo + AgentDyn, static/adaptive/long-horizon, live | Partial: own chains and deployments | Yes: AgentDojo + ASB, live | Yes: AgentDojo, live |
| **Context integrity** (what the content is) | Partial: least-trusted segment labels; one pattern detector (`x_ctx2`) **tuned to the benchmark template** (`configs/exploratory/pilot_e0.yaml:94-97`); no outcome effect in ablation | Partial: 4 sub-detectors; fail under paraphrase / zero-width (SIG-2) | No (design) | Partial: content is labelled by origin, not inspected | Unknown | No | Partial: detects via behavioural comparison, not content |
| **Provenance awareness** (where argument values come from) | Partial: exact-string `x_act1` (untrusted-only occurrence), broken by reformatting (DiD-2: P1 rule 12 → 191) | Yes (replay): field-level lineage with canonical IBANs and amounts | No (design) | **Yes**: origin labels with platform trust anchors; deterministic verifier | Yes (A): source registration | No (argument rules, not provenance) | No |
| **Behavioural analysis** (history / sequences) | Partial: 4 features (`x_beh1–4`). **Removing them improves utility**; no measured security benefit | Partial: deterministic new-payee / redirect / repeat / retry / switch rules; retry and switch **inert in replay** | No (design) | No | Partial (A/S): repeated-request ledger | No | Partial: counterfactual next-action comparison |
| **Tool-call inspection** | Yes: every restricted call features | Yes | No (design) | Yes (sensitive parameters) | Yes (A) | Yes | Yes |
| **Action authorization** (what the user asked for) | **No**: no representation of the user's request beyond `x_act2` (recipient in objective) | Partial: TAE/permits implemented, but **issued by an oracle** from ground truth | No (design) | Yes: router-set per-task rules from the trusted request | Yes (A): operator declarations + grants | Yes: policies (manual or LLM-generated) | No |
| **Runtime enforcement before execution** | Yes in replay: withheld calls are not executed (`rem/integration/agentdojo_replay.py:236-259`) | Yes in replay: gateway with single-use permits | No (design) | Yes (live) | Yes (live, depth varies by host) | Yes (live) | Yes (live) |
| **Mitigation capabilities** | Partial: 4 verdicts, but **Modify, Escalate and Block coincide** (no reviewer; replacing all by Block changes no episode; thesis Ch. 4) | Partial: Allow / Escalate / Block; Escalate is withhold without a reviewer | No (design) | Partial: deny with feedback to the agent | Partial (A): deny | Partial: deny with feedback | Partial: stop on detection |
| **Post-execution monitoring** | Partial: audit record; CUSUM observe-only | Partial: hash-chained audit | No (design) | No | Yes (A): forensic replay | No | No |
| **Financial task coverage** | Yes, banking only | Yes, banking only | Design targets finance | Partial: banking among six suites; **amount unguarded** | Unknown | Partial: banking among suites | Partial: banking among suites |
| **Benchmark evaluation** | Partial: AgentDojo banking, **recorded traces, NO-ADAPT** | Partial: same, oracle authorization | No | Yes: live, two benchmarks | Partial: own benchmarks | Yes: live, two benchmarks | Yes: live |
| **False-positive evaluation** | Yes: withheld legitimate calls reported (81.5% of legitimate restricted calls in benign P1 episodes) | Yes | No | Yes (utility metrics) | Yes (A: denial events) | Yes | Yes |
| **Benign utility** | Yes (replay): 105/334 = 31.4%, **identical episode set to withholding every state-changing call** (02 §1.3) | Yes (replay): 173/334 with oracle authorization | No | Yes (live): banking clean utility 8–10/16 in authors' logs | Partial (A) | Yes | Yes |
| **Runtime overhead** | Yes: ≈0.15 ms median per call, no model calls (decision only; one CPU container) | Yes (replay timings) | No | Partial: router call per task; deterministic check | Unknown | Yes: deterministic check (0.22 ms median in REM's harness) plus LLM policy generation | Yes: about 73% more model calls (REM's workload estimate, `REM_MELON_COMPARISON_2026_11_19/10`) |
| **Reproducibility** | **Yes: re-run in this audit from public inputs, identical results** | Yes: raw data stored; pinned inputs | — | Yes: code and logs public | **No**: no code found | Yes: code public | Yes: code public |

## 2. The meaningful differences

1. **REM v1.0 is a risk-scoring monitor, not an authorization system.**
   - Every system it is compared with (ROPE, AGATE, Progent, CaMeL, AgentCap) knows, in some form, *what the user authorized*. REM v1.0 knows only *where values came from* and *how the episode has behaved*.
   - The thesis itself found this to be its limit (Ch. 1 §1.11 item 6): provenance features cannot separate an authorized payment from an unrequested one whose details appear in the user's words.
   - The learned decision compensates by **withholding almost every state-changing call**: withhold precision is 0.40 on P1. This gives high replay security and the replay utility floor.

2. **REM's closest neighbour in mechanism is NEXUS, not ROPE or Progent.**
   - NEXUS (peer reviewed, Findings of AACL 2026): a calibrated logistic-regression risk score plus deterministic rules, choosing among four graduated interventions.
   - This is the same shape as REM v1.0's decision engine. **REM v1.0's architecture is therefore not distinctive.**
   - What REM adds relative to the abstract-level description of NEXUS:
     - expected-loss selection with tier-indexed costs;
     - a controlled AgentDojo evaluation with held-out objectives and rule baselines.

3. **On the same recorded episodes, deterministic or request-derived policies dominate the learned decision.**

   | Comparator | Attacks (REM v1.0 = 11) | Benign (REM v1.0 = 105) | Source |
   |---|---|---|---|
   | Progent's manual policy | 0 | 154 | `REM_COMPARATIVE_EVALUATION_PHASE/02` §4 |
   | Request-derived guard GV | 0 | +10.4 points of completed tasks | `REM_COMPETITIVE_STUDY_2026_11_16/10` |
   | Oracle authorization (REM-DiD B2) | 0 | 173 | 02 §5 |

   **Caveats:**
   - Progent's policy is an oracle allow-list.
   - GV was developed on the same data.
   - The oracle is an upper bound.

   **None of these is a fair "win" for the comparator.** But none supports REM's learned core either.

4. **Evaluation regime is the largest difference.**
   - ROPE, Progent and MELON were evaluated with **live agents**, and ROPE and Progent also against **adaptive attacks**.
   - REM was evaluated only by **NO-ADAPT replay** of other people's recordings, where:
     - a refused call cannot cause the agent to try something else;
     - benign utility is insensitive to read-only completions.
   - Published live figures and REM's replay figures **must not be placed in one ranking**. The thesis already avoids this, and it must continue to.

5. **Where REM's evidence is genuinely richer than its neighbours'.** REM's studies contain the following:
   - a pre-registered layer-by-layer ablation on three populations;
   - a double holdout over user task and attack objective;
   - one confirmatory run on unread recordings;
   - a removal-versus-evasion comparison of controls;
   - an explicit audit of a published policy's oracle content.

   These are **evaluation-methodology strengths**, not mechanism strengths (05).
