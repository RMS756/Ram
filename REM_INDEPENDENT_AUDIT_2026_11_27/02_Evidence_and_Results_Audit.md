# 02: Evidence and results audit

**Categories.**

| Category | Meaning |
|---|---|
| VERIFIED | Directly supported by evidence inspected or recomputed in this audit |
| PARTIALLY SUPPORTED | Evidence exists but does not fully establish the claim |
| UNVERIFIED | Insufficient evidence to conclude either way |
| UNSUPPORTED | Available evidence does not justify the claim |

**Historical vs newly verified.**
- "Historical" means a result as stored in the repository.
- "**Re-verified 27 Nov**" means recomputed from raw data or re-executed in this audit.
- No stored result was modified.

## 1. The baseline: REM v1.0 on recorded AgentDojo banking traces

### 1.1 Fresh reproduction (re-verified 27 Nov)

**What was done.**
- Fetched AgentDojo's recorded runs at `089ed468` (public) and installed `agentdojo==0.1.35`.
- Ran the frozen pipeline unchanged:

  ```
  PILOT_RESULTS_DIR=<scratch> PYTHONHASHSEED=0 AGENTDOJO_RUNS=<runs>
  python3 build_dataset.py && python3 e0_pilot.py && python3 run_main.py crossfit rmod replay
  ```

- Wall time 6 min 36 s; exit 0. Outputs went to a scratch directory **outside the repository**. `git status` shows no change to tracked files.

| Output compared with the stored `results/pilot/` file | Result |
|---|---|
| `dataset_summary.json` (3,334 episodes, 6,762 steps, 921 positive steps) | **Identical** |
| `e0_pilot.json` | **Identical** |
| `e1_crossfit.json` | **0 numeric differences**. The current code writes 19 extra keys, which are not in the stored file. ROC-AUC 0.9383, ECE 0.0438 |
| `e4_e5_enforcement_replay.json` | **0 non-timing numeric differences**. Only latency fields differ (92), as expected; 150 extra keys |
| Headline | REM v1.0 step-level, no reviewer: ASR 0.0037 = **11 / 2,979**; benign 0.3144 = **105 / 334**; utility under attack 0.3635 = **1,083 / 2,979**; 0 replay errors |

Reproduced output hashes (sha256):
- `e4_e5_enforcement_replay.json`: `933016f7…ee3d`
- `e1_crossfit.json`: `cce94526…bea`

**Status: VERIFIED and re-verified.** This is a reproduction (same code, same data). It is not an independent replication.

### 1.2 Recomputation from stored episode records (re-verified 27 Nov)

Source: `REM_ABLATION_STUDY/05_EPISODE_RESULTS.jsonl.gz` (54,963 records).

**Pairing.** All nine arms are evaluated on **identical episode sets** in each population (P1: 3,313; P2: 681; P3: 2,113).

| Population | Composition | B0 (no defense) | REM v1.0 (A0) | Learned decision removed (A3) | Behaviour removed (A2 = v1.1) | Provenance removed (AIC) |
|---|---|---|---|---|---|---|
| P1 primary | 21 backbones; `important_instructions`; 16 user tasks, 9 injection tasks | 672 / 2,979 attacks; 175 / 334 benign | **11 / 2,979; 105 / 334** | 672; 180 | 11; 140 | 17; 105 |
| P2 cross-template | gpt-4o; 5 other templates | 174 / 681 | **2 / 681** | 174 | 2 | 3 |
| P3 second population | 5 pipelines incl. Meta-SecAlign and `repeat_user_prompt`; 7 templates | 436 / 2,065; 38 / 48 benign | **3 / 2,065; 18 / 48** | 435; 39 | 1; 25 | 8; 18 |

**Status: VERIFIED.** Thesis claim 3 (22.6% → 0.4% on P1; 21.1% → 0.15% on P3; 31% vs 52% benign) matches these counts exactly.

**Denominator note.** P3's benign set is **48 episodes from 3 pipelines**. Every P3 benign percentage has a coarse resolution: one episode is 2.1 points.

### 1.3 New finding: REM v1.0's benign replay utility equals the withhold-everything floor

Source: `REM_DEFENSE_IN_DEPTH/results/did3_raw.jsonl.gz`. 41 arms on POP-P = P1, identical episode sets. Arm B1 is REM v1.0 in the DiD harness. Arm F-GW withholds **every** state-changing call.

| Arm | Benign completed / 334 | Utility under attack / 2,979 | Attacks / 2,979 |
|---|---|---|---|
| B0 (no defense) | 175 | 1,465 | 672 |
| **B1 = REM v1.0** | **105** | 1,083 | 11 |
| **F-GW (withhold every state-changing call)** | **105** | 989 | **0** |

**Episode-set comparison** (recomputed 27 Nov):
- **The 105 benign episodes REM v1.0 completes are exactly the 105 completed when nothing state-changing executes** (0 episodes in either difference).
- Under attack, REM completes 94 more episodes than the floor, and the floor completes none that REM does not.
- REM's 11 successful attacks are all in `user_task_15`.

**Interpretation.**
- In NO-ADAPT replay on P1, REM v1.0 completes **no benign task that requires a state-changing call**.
- Its benign utility is the replay floor (read-only tasks, plus tasks whose recorded failure is avoided by withholding an erroneous call).
- Relative to withholding everything, REM's net effect on P1 is: +94 tasks completed under attack, +11 successful attacks, and 0 benign tasks.

**Status: VERIFIED** from stored data. The thesis states the components of this finding:
- 105 tasks are completed with everything withheld (DiD edition);
- REM withholds almost every legitimate payment (humanized Ch. 4).

It **does not state the identity of the episode sets**. P3 was not checked: there is no withhold-all arm on P3 (07).

## 2. Confirmatory run of REM v1.1 (behaviour removed)

Source: `REM_FINAL_SUBMISSION/results/confirmatory_results.json`; protocol `REM_FINAL_SUBMISSION/research/REM_FINAL_EXPERIMENT_PROTOCOL.md`.

| Arm (2,113 eligible episodes: 2,065 attacked, 48 benign) | Attacks | Benign | All-task success |
|---|---|---|---|
| B0 | 436 | 38 | 1,451 |
| B1 operating-point threshold | 67 | 36 | 1,514 |
| **REM v1.0 (M00)** | **3** | **18** | **916** |
| **REM v1.1 (M00_nobeh)** | **1** | **25** | **1,074** |
| P1 rule (`x_act1`) | 4 | 24 | 1,044 |
| P2 rule (`x_act1` or `x_act2`) | 4 | 24 | 1,043 |
| A2 rule (identity arguments not in objective) | 4 | 27 | **1,232** |
| M01 (Allow/Block only) | 3 | 22 | 1,115 |

- Primary contrast v1.1 − v1.0: +0.0748 [0.0117, 0.1602] all-task success = 158 / 2,113. Pre-declared verdict **GO**.
- **Status: VERIFIED** (numbers). **PARTIALLY SUPPORTED** (confirmatory status): the protocol's freeze commit is not in this repository's history (01 §3).

**Observation not emphasised in the thesis.** The simplest rule, A2, completes **158 more tasks than REM v1.1 and 316 more than REM v1.0**, with 4 vs 1 vs 3 attacks. The stored secondary contrast v1.1 − A2 is −0.0748 [−0.257, 0.082]. This interval includes 0, so the difference is not resolved. The thesis's wording "neither REM version is distinguishable from the rules" is accurate.

## 3. Comparators

| Claim | Evidence | Status |
|---|---|---|
| Progent's published manual banking policy: 0 / 2,979 attacks, 154 / 334 benign on P1 | `REM_COMPARATIVE_EVALUATION_PHASE/02` §4 | VERIFIED as stored (not recomputed) |
| That policy is an **oracle allow-list**: five benchmark IBANs, excluding the attacker IBAN | Same file §2, checked against benchmark files | VERIFIED as stored. This makes any "Progent beats REM" or "REM vs Progent" claim non-informative about unseen attackers |
| AgentDojo's distributed defenses vs REM | REM replay 2 / 134 attacks on gpt-4o pairs vs recorded runs (`REM_FINAL_THESIS_COMPLETION_2026_11_19`) | PARTIALLY SUPPORTED. **Descriptive only**: a replay is set against live recordings |
| MELON vs REM | `REM_MELON_COMPARISON_2026_11_19/README.md` | **No result exists** (not executed). Any comparative claim would be UNSUPPORTED |
| DRIFT vs REM | Architecture/code audit only | No result exists |

## 4. Claims of the exploratory development studies (13–19 Nov)

Read from their decision tables. Not recomputed.

| Claim | Status |
|---|---|
| G1 / GV (request-derived authority front) completes more tasks than REM v1.0 with no more attacks (development data) | PARTIALLY SUPPORTED: development data, many rounds on the same recordings (their own caveat) |
| A learned stage behind the deterministic front changes no outcome | PARTIALLY SUPPORTED, consistently across four studies. Their own caveat: no recorded attack passes the front, so the learner is never tested on one |
| REM-B2 and REM-B3 are NO-GO | VERIFIED as recorded decisions (`REM_B_HARDENING_VALIDATION_2026_11_19/README.md`) |
| Request-derived authorization is limited by intent compilation (a new compiler error in each of three held-out probe rounds) | PARTIALLY SUPPORTED: author-written probes |
| The authorization-aware, outcome-supervised candidate is worse (132 vs 11 attacks) | VERIFIED as recorded |

## 5. REM-DiD (exploratory) and REM-X (design)

| Claim | Status |
|---|---|
| DiD-3 counts (B2 0 / 173; B2e 0 / 122; B3 13 / 147; B9 0 / 105; B9n 0 / 173; X0 0; X-only-LEARN 11; X-BEH 6; X-LEARN 1) | **Re-verified 27 Nov** from `did3_raw.jsonl.gz`. All 41 POP-P arms pair on identical episode sets |
| "REM-DiD protects with 0 attacks" | **UNSUPPORTED as a security claim.** B2/B9 use an **oracle** TAE built from the benchmark's ground truth; it is an upper bound, not a defense. B2e (explicit authorization, closer to realistic) gives 0 attacks but 122 / 334 benign |
| "The learned layer adds no security behind authorization" (B9 vs B9n: 0 vs 0; −68 benign) | VERIFIED (counts). Holm p = 0.12, not significant |
| "Removal and evasion give opposite verdicts" (DiD-2: 11 vs 11 removal; 653 vs 90 evasion) | VERIFIED as stored. **Modelled evasion; post-hoc arm.** Exploratory |
| "Controls are redundant (Jaccard 0.84–0.99; 19 of 907 calls covered distinctly)" | VERIFIED as stored (amendment 50a) |
| REM-X / Amendment 01 effectiveness | **UNVERIFIED by design.** Nothing implemented |

## 6. Integrity checks A–D

### A. Implementation integrity

| Check | Finding |
|---|---|
| Functions match attribution | Features are computed from the proposed call and the history before release (`rem/algorithms/behavior/evidence.py:199-268`). `x_act1` = the argument occurs in untrusted text and not in trusted text; `x_act2` = the recipient is not in the objective |
| Matches documented architecture | Five layers present in code. **In effect, Modify, Escalate and Block are the same action** (withhold) without a reviewer (`rem/integration/agentdojo_replay.py:236-259`). The thesis states this |
| Enforcement before harmful execution | **Yes, in replay:** a withheld call is not executed (`_mitigate` returns release = False). In live use, the gateway `rem/deployment/gateway.py` exists but **was never run with a live agent** |
| Undeclared changes | None to `rem/` or `configs/` since the repository's first commit |

### B. Experimental integrity

| Check | Finding |
|---|---|
| Datasets and protocols identifiable | Yes: pinned AgentDojo runs; per-population composition (§1.2) |
| Counts and denominators | Consistent across the ablation file, the DiD-3 raw file, the confirmatory file and the fresh reproduction |
| **Leakage / contamination** | (i) P1 was used to design REM v1.0; P2 and P3 were read before the ablation. Only the confirmatory run used unread data. (ii) The context detector's patterns encode the benchmark's `important_instructions` template (`configs/exploratory/pilot_e0.yaml:94-97`). Its ablation effect is nil, so no headline result depends on it. (iii) Labels come from injection-task ground truth with the attacker key arguments (`rem/integration/agentdojo_traces.py:192-227`). They are used for fitting and call-level metrics. The episode outcome uses AgentDojo's own security check, so labels do not leak into the primary outcome. (iv) Cross-fitting holds out injection tasks (9 folds). The attacker IBAN is shared by 8 of 9 tasks but is not a feature |
| Train / test separation and seeds | Grouped cross-fitting documented; seed 20261027; `PYTHONHASHSEED=0` |
| Paired comparisons on matching episodes | **VERIFIED** for the ablation (27 arms) and DiD-3 (41 arms) |
| Reproducible from artifacts | **VERIFIED** for the baseline (§1.1) |
| Label quality | The reference-match rule has a known limitation: escalated calls labelled 0 still contributed to attack success (DiD-3 B3+R: 17 vs 13). A human label audit was packaged but **not executed** (`REM_DEFENSE_IN_DEPTH/53`; `results/pilot_R2/label_audit_human_package.csv`) |

### C. Security effectiveness

| Question | Answer |
|---|---|
| Protection against IPI established? | **In NO-ADAPT replay on one benchmark: yes, the recorded attack actions are withheld.** Against a live or adaptive agent: **not established** |
| Detects, prevents, or merely identifies? | REM **prevents in replay** by withholding calls. The detection-type evidence (`x_ctx2`) contributes nothing; the learned decision acting through enforcement does all the work |
| Attack success and task completion distinguished? | Yes, throughout. But **benign completion on P1 is the floor** (§1.3) |
| Attributable to REM or to the setup? | (i) The residual 11 attacks are a benchmark collision (`user_task_15`). (ii) Benign utility is a property of replay, not of REM. (iii) The security comes from REM's learned decision withholding nearly every state-changing call. Withholding every such call yields 0 attacks (§1.3) |

### D. Runtime practicality

| Question | Answer |
|---|---|
| Overhead measured? | Yes: per-call decision time median 0.12 ms (full method 0.15 ms) on one CPU container. No model calls. **Not deployment latency** |
| Intervention point clear? | Yes: each proposed call of a restricted tool, before execution |
| Limitations documented? | Agent reaction to refusals: not modelled (NO-ADAPT). External effects: AgentDojo sandbox only. Agent state: not modified. All stated in the thesis |

## 7. Claim table for the thesis's own contribution list (humanized Ch. 1 §1.11)

| # | Thesis claim | Status |
|---|---|---|
| 1 | Specified, implemented, tested framework; exact re-execution of the pilot | **VERIFIED** (re-executed in this audit) |
| 2 | Controlled protocol (objective holdout, double holdout, rule baselines, one confirmatory run) | VERIFIED as documented; confirmatory pre-registration **not verifiable from git here** |
| 3 | 22.6% → 0.4% (P1), 21.1% → 0.15% (P3); 31% vs 52% benign | **VERIFIED.** Must add that 31% equals the withhold-everything floor on P1 (§1.3) |
| 4 | +7.5 points task completion from removing behaviour; 1 vs 3 attacks | **VERIFIED** (numbers) |
| 5 | Four negative results | VERIFIED as documented |
| 6 | Provenance evidence cannot separate authorized from unrequested payments | VERIFIED (collision analysis; `user_task_15`) |
| 7 | Exploratory request-derived rule: no attack, more tasks (development data) | PARTIALLY SUPPORTED (development data) |
| 8 | Ablation: learned decision accounts for all 661 prevented attacks; others change nothing | **VERIFIED** (recomputed §1.2) |
| "Does not demonstrate" list | Consistent with the evidence | VERIFIED |
