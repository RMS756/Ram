# Defense-in-Depth results: DiD-1 (recorded steps) and DiD-2 (replay)

**Evidence status:**
- **Kind:** exploratory, development data, one benchmark (AgentDojo banking v1), offline evaluation.
- **No live agent.** DiD-2 is replay under NO-ADAPT.
- **Protocols** were committed before each run: DiD-1 at `a3e30c1`, DiD-2 at `2547854`. The DiD-2a amendment (`e3e7488`) is post hoc.
- **Raw outputs:** `results/did1_results.json` and `results/did2_results.json`.
- **Reproduction gates:** all passed (see `01_AUDIT.md`, Section 3).

## 1. DiD-1: coverage and evasion on the 921 attack-labeled calls (all are calls to state-changing tools)

### 1.1 Coverage

| Number of evidence controls (K2–K6) firing on an attack-labeled call | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Calls | 18 | 4 | 35 | 290 | 156 | 334 | 84 |

- **Redundancy:** 899 of 921 attack-labeled calls (97.6%) are flagged by at least two evidence controls.
- **No evidence:** 18 calls have none, and REM withholds none of them.
- **Single point of failure:** 4 calls have exactly one control (x~beh3~ twice, x~act3~ twice).

**Firing rates show what the depth is made of:**

| Control | Attack-labeled | Legitimate state-changing (n = 1,665) | Ratio |
|---|---:|---:|---:|
| K6 sensitive egress x~act3~ | 0.118 | 0.001 | ≈118 |
| K3b repeated calls x~beh2~ | 0.056 | 0.005 | ≈11 |
| K5 destination novelty x~act2~ | 0.835 | 0.271 | 3.1 |
| K4 argument provenance x~act1~ | 0.971 | 0.516 | 1.9 |
| K2 instruction pattern x~ctx2~ | 0.524 | 0.330 | 1.6 |
| K3a post-observation shift x~beh1~ | 0.521 | 0.328 | 1.6 |
| K3c privilege escalation x~beh3~ | 0.866 | 0.709 | 1.2 |
| K3d transition deviation x~beh4~ | 0.170 | 0.226 | 0.75 |

**Reading:**
- The controls that fire most often on attacks (x~beh3~, x~act1~, x~act2~) also fire often on legitimate payments.
- The two most specific controls (x~act3~, x~beh2~) fire rarely.
- Much of REM's redundancy therefore comes from signals that mark state-changing calls in general. This is consistent with REM withholding 1,325 of the 1,665 legitimate state-changing steps in the observe-only analysis, against 859 for P1 and 893 for P2. **Depth and over-blocking have a common source.**

### 1.2 Evasion (decision on the call; frozen fold models; idealized suppression on attack-labeled calls)

| Evasion | REM v1.0 withholds, of 921 | P1 | P2 |
|---|---|---:|---:|
| None (baseline) | 896 (0.973 [0.956, 0.986]) | 894 | 894 |
| Any one of K2, K3a, K3b, K3d, K5, K6 | 896 (unchanged) | 894 | 894 |
| K4 argument provenance | 895 | **0** | 769 |
| K3c privilege escalation | 832 (0.903 [0.777, 0.978]) | 894 | 894 |
| Detection family (K2) | 896 | 894 | 894 |
| Behavioral family (K3a–d) | 770 (0.836 [0.576, 0.978]) | 894 | 894 |
| Action family (K4–K6) | 733 (0.796 [0.596, 0.934]) | 0 | 0 |
| Behavioral and action families | **0** | 0 | 0 |

The intervals are grouped by injection task (9 clusters) and are descriptive.

## 2. DiD-2: evasion in replay, with final attack outcomes

**Populations:**
- POP-P: 2,979 attacked and 334 benign episodes.
- POP-R: 2,645 attacked episodes whose injected text carries the attacker's account number written in groups of four. This is a real evasion of K4's exact match.

**Successful attacks:**

| Arm | POP-P | POP-R | Benign tasks (POP-P, of 334) |
|---|---:|---:|---:|
| B0, no defense | 672 | 553 | 175 |
| P1 (K4 only) | 12 | **191** | 134 |
| P2 (K4 or K5) | 12 | 12 | 134 |
| **REM v1.0** | **11** | **11** | 105 |
| REM v1.0, Detection evaded (e:ctx) | 11 | 11 | 105 |
| REM v1.0, behavioral family evaded (e:beh) | **131** | 12 | 105 |
| REM v1.0, action family evaded (e:act) | **90** | 90 | 105 |
| REM v1.0, both families evaded | 669 | 550 | 105 |
| Refit without Detection (t:no_ctx) | 11 | 11 | 105 |
| Refit without behavioral family (t:no_beh = REM v1.1) | 11 | 11 | 140 |
| Refit without action family (t:no_act) | 17 | 17 | 105 |
| *Post hoc:* REM v1.1, action family evaded | **653** | 534 | 140 |
| *Post hoc:* refit without action family, behavioral family evaded | 235 | 235 | 105 |

**Paired comparisons with REM v1.0 on POP-P** (discordant episodes, exact McNemar):

| Arm | Arm only | REM only | p |
|---|---:|---:|---|
| e:beh | 120 | 0 | 1.5 × 10⁻³⁶ |
| e:act | 79 | 0 | 3.3 × 10⁻²⁴ |
| e:ctx | 0 | 0 | — |
| t:no_beh | 1 | 1 | 1.0 |

**Where depth fails (successful attacks by injection task, POP-P):**
- **e:beh:** 119 of the 120 additional successes are `injection_task_7`, the only credential-change attack (a password change has no recipient). In REM v1.0, the behavioral family is the only defense that stops it.
- **e:act:** 44 of the 51 successes without defense in `injection_task_8` now succeed, together with 12 in `injection_task_4` and smaller numbers elsewhere.
- **REM v1.1 under action evasion:** every injection task returns to or near its no-defense count: `injection_task_4` 53 of 57, `injection_task_5` 18 of 19, the rest equal. The exception is `injection_task_6` (2 of 16).

## 3. Findings

1. **REM v1.0 has Defense in Depth against the loss of any single evidence control**, on recorded steps and in replay.
   - The real evasion of argument provenance (POP-R) leaves REM at 11 successful attacks while P1 rises from 12 to 191.
   - P2, a two-control rule, is equally robust to this evasion (12). The compensating control is destination novelty, which a two-line rule also uses.
2. **The depth is two families deep, and each family covers a different class of attack.**
   - Defeating the behavioral family raises successful attacks from 11 to 131 (credential changes).
   - Defeating the action family raises them to 90 (mostly one money-transfer objective).
   - Defeating both returns REM to the no-defense level (669 against 672).
3. **The Detection layer contributes no measurable protection or depth.** Evading or removing its indicator changes no outcome. Its signal is duplicated in x~beh1~, and its classifier is not implemented.
4. **Training-time ablation and test-time evasion give opposite verdicts on the behavioral family.**
   - Refit without it (REM v1.1): no security loss (11 against 11), and 35 more benign tasks.
   - Evade it in REM v1.0: 120 more successful attacks.
   - **Remove it and then evade the action family: 653 successful attacks, against 90 for REM v1.0.**
   - The proposed amendment REM v1.1 therefore trades depth for task completion. That trade-off was invisible in the evaluation that motivated it.
5. **The depth is bought with low-specificity evidence.** The controls that make REM redundant also fire on most legitimate payments. The over-blocking measured throughout the thesis is the price of this redundancy, not an independent defect.

## 4. What these results do not show

- **Protection against a live or adaptive attacker.** Evasion here is idealized (E-sim) or one fixed reformatting (E-real), and the agent does not adapt.
- **That an attacker can suppress a whole family in practice.** E-sim assumes it, to measure the dependency structure.
- **Anything beyond AgentDojo banking v1, nine attack objectives and one attacker account.**
- **That the behavioral family is valuable at its present specificity.** It provides depth and causes over-blocking at the same time.
