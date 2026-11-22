# 06 Ablation results at the episode level (E-OFF; O2)

**Source.** `REM_ABLATION_STUDY/05_EPISODE_RESULTS.jsonl.gz` (sha256 `e98437f7…`, checked).

**Kind of evidence.** Offline replay (NO-ADAPT). These are **replay outcomes, not ASRs**.

**Statistics.**
- Differences are arm − A0 in percentage points, with 95% grouped-bootstrap intervals.
- Clusters: injection task for attacked episodes, user task for benign episodes.
- "a / b" means discordant episodes: arm only / A0 only. p is the exact McNemar test.

**Output:** `results/ablation_episode_level.json`.

**Reproduction check.** The comparative run O1 recomputed B0, A0 and A3 independently and matches these records **episode by episode and call by call** (`test_o1_shared_arms_reproduce_the_frozen_ablation_episode_by_episode`).

## P1 (2,979 attacked, 334 benign episodes; 22 backbones)

| Arm | Attack outcomes / 2979 | Episodes with an attack call executed | Utility under attack / 2979 | Benign completed / 334 | Benign episodes with a withheld call / 334 |
|---|---|---|---|---|---|
| B0 none | 672 | 828 | 1465 | 175 | 0 |
| **A0 full REM** | **11** | **24** | **1083** | **105** | **141** |
| A1a − `x_ctx2` | 11 | 24 | 1081 | 105 | 141 |
| A1b − Detection layer | 11 | 24 | 1094 | 105 | 141 |
| A2 − Behavioural | 11 | 24 | 1147 | **140** | **92** |
| AIC − provenance evidence | 17 | 49 | 1062 | 105 | 153 |
| **A3 − learned decision** | **672** | **828** | 1509 | 180 | 6 |
| A3P − predicates | 11 | 24 | 1078 | 105 | 141 |
| A4 shadow | 672 | 828 | 1465 | 175 | 0 |

**Paired against A0 on P1**, for the arms that change something:

| Arm | Outcome | Difference (pp) | Discordant (arm only / A0 only) | McNemar p |
|---|---|---|---|---|
| **A3** | attack outcome | +22.2 [14.6, 28.9] | 661 / 0 | 2e-199 |
| **A3** | benign completion | +22.5 [8.0, 38.5] | 83 / 8 | 8e-17 |
| **A3** | false-positive episodes | −40.4 [−55.2, −26.9] | — | — |
| **A2** | attack outcome | 0.0 [−0.1, 0.1] | 1 / 1 | 1.0 |
| **A2** | benign completion | +10.5 [1.2, 22.6] | 36 / 1 | 6e-10 |
| **A2** | false-positive episodes | −14.7 [−28.7, −4.2] | — | — |
| **AIC** | attack outcome | +0.2 [−0.1, 0.4] | 9 / 3 | 0.15 |
| **AIC** | attack-call-executed episodes | +0.8 [0.0, 2.2] | 29 / 4 | 1e-5 |
| **AIC** | false-positive episodes | +3.6 [0.0, 10.8] | 12 / 0 | — |
| **A1a, A1b, A3P** | attack outcome, benign completion, false positives | 0.0 | — | — |
| **A1a, A1b, A3P** | utility under attack | changes of ≤ 0.4 pp | at most 14 / 3 | — |
| **A4** | all outcomes | equal to B0 | — | — |

## P2 (681 attacked; cross-template) and P3 (2,065 attacked, 48 benign; unseen backbones and templates)

| Arm | P2 attack outcomes / 681 | P2 utility under attack | P3 attack outcomes / 2065 | P3 utility under attack | P3 benign completed / 48 | P3 benign FP episodes / 48 |
|---|---|---|---|---|---|---|
| B0 | 174 | 504 | 436 | 1413 | 38 | 0 |
| A0 | 2 | 302 | 3 | 898 | 18 | 33 |
| A1a | 2 | 300 | 3 | 898 | 18 | 33 |
| A1b | 2 | 299 | 3 | 902 | 18 | 33 |
| A2 | 2 | 370 | 1 | 1049 | 25 | 27 |
| AIC | 3 | 271 | 8 | 838 | 18 | 33 |
| A3 | 174 | 530 | 435 | 1458 | 39 | 1 |
| A3P | 2 | 299 | 3 | 893 | 18 | 33 |
| A4 | 174 | 504 | 436 | 1413 | 38 | 0 |

## Findings (including negative ones)

1. **The learned Decision Engine changes decisions and carries all of REM's protection on these traces.**
   - Without it (A3), REM's deterministic predicates stop no attack: 672 / 2979 attack outcomes, the same as no defence.
   - With it: 11 / 2979.
   - The same holds in P2 and P3.

   This **does not confirm** the earlier suggestion that the learned component does not change decisions. That suggestion concerned the REM-B family, not REM v1.0.
2. **The learned decision is also the main source of over-blocking.**
   - Benign completion: 105 / 334 with it, 180 / 334 without.
   - False-positive episodes: 141 vs 6.
3. **The learned decision is not shown to be better than every deterministic rule.**
   - Progent's published hand-written policy (`02`), another set of deterministic rules, reaches 0 attack outcomes with 154 / 334 benign completed on the same episodes.
   - That policy encodes benchmark-specific recipients. So "learned vs deterministic" here means "learned vs REM's own two predicates", which are much weaker than a task-informed allow-list.
4. **Detection (`x_ctx2`, and the layer A1b) and predicates D1/D2 have no measurable effect** on any episode-level outcome, in any population.
5. **Behavioural evidence costs utility and buys no measurable security.**
   - Removing it (A2) raises benign completion by 35 episodes on P1 (+10.5 pp [1.2, 22.6]) and 7 on P3, with attack outcomes unchanged or lower.
   - Under the ablation protocol, this supports the pending REM v1.1 amendment (decision SD-FEAT). The decision is the supervisors', not taken here.
6. **Provenance/action evidence is the only feature group whose removal measurably increases attack-call execution** (P1: 29 vs 4 episodes, p = 1e-5). The effect on final attack outcomes is not resolved (9 vs 3, p = 0.15).
7. **Enforcement is what produces the effect.** Shadow mode (A4) equals no defence.
