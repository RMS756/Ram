# 07 Statistical analysis

## Unit of analysis and denominators

| Outcome | Unit | Denominator |
|---|---|---|
| Attack outcome, attack-call execution, utility under attack | attacked episode | the attacked episodes of the population |
| Benign completion, false-positive episode | benign episode | the benign episodes |

**Population sizes.**
- P1: 2,979 attacked and 334 benign.
- P2: 681 attacked, no benign.
- P3: 2,065 attacked and 48 benign.

**Calls are not treated as samples.** Call counts in `02` are descriptive only.

## Pairing

Every arm sees the same episodes and the same recorded call positions, so differences are within-episode. **Exact McNemar tests** use the discordant counts (b, c), which are reported with each p value.

## Intervals

- **Method:** grouped percentile bootstrap, 2,000 resamples, seed 20261027, 95% (`rem.evaluation.bootstrap.grouped_bootstrap`).
- **Clusters:** 9 injection tasks for attacked episodes; 16 user tasks for benign episodes. These are the levels declared in `pilot_e0.yaml`; confirmation is pending (`10`).
- **Caveat for attacked episodes:** with only 9 clusters, the intervals are coarse.
- **Caveat for benign episodes:** P3 has 48 episodes in 16 clusters, which gives very wide intervals (for example REM vs B0 benign completion: −41.7 pp [−70.8, −10.4]).

## Primary offline contrasts (P1; full tables in `02` and `06`)

| Contrast | Replay attack outcomes | Benign completion |
|---|---|---|
| REM vs none | 11 vs 672 / 2979; −22.2 pp [−28.9, −14.6]; b/c = 0/661 | 105 vs 175 / 334; −21.0 pp [−37.9, −5.1]; 13/83 |
| Progent vs none | 0 vs 672; −22.6 pp [−29.5, −14.8]; 0/672 | 154 vs 175; −6.3 pp [−17.2, −0.3]; 0/21 |
| REM vs Progent | 11 vs 0; +0.4 pp [0.1, 0.7]; 11/0, p = 0.00098 (all `user_task_15`) | 105 vs 154; −14.7 pp [−29.7, −0.9]; 13/62, p = 8e-9 |
| REM vs REM predicates only | 11 vs 672; −22.2 pp; 0/661 | 105 vs 180; −22.5 pp [−38.5, −8.0]; 8/83 |

## How to read the p values

- They test the paired episode outcomes **within these replayed populations**. They do not test a live agent.
- The very small p values reflect large numbers of discordant episodes. They are **not** evidence that the effect transfers to closed-loop use.
- They come from **development data**: REM was cross-fitted on P1, and Progent's policy was written for this benchmark.
- No correction for multiplicity was applied. The contrasts were pre-registered in `01`, and they are reported as estimates with intervals.

## Missing and invalid episodes

| Population | Replay errors | Excluded by AM-4 (no-defence replay differs from the recording) |
|---|---|---|
| P1 | 0 | 0 (P1 validity as in the frozen pilot) |
| P2 | 0 | 34 of 715 |
| P3 | 0 | 35 of 2,148 |

Exclusions apply to all arms of an episode (paired deletion). The ambiguous pair `user_task_15 × injection_task_4` is already excluded from P1 (AM-1).

## Small-sample and design limits

- **Live arms do not exist yet.** For the planned live run (16 benign episodes per repeat), a single repeat gives benign-utility intervals of about ±20 pp or more.
- **Version scope.** The data are v1. No v1.2 number (for example DRIFT's published runs) is compared with them.
