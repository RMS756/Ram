# Results and interpretation

**Status of every number: development evidence** from offline recorded-trace replay (AgentDojo 0.1.35 banking; NO-ADAPT; no live agent; no model call; no reviewer). Tables: `03_RESULTS_TABLES.md`, generated from `results/`. Protocol: `PROTOCOL.md` (frozen at commit `3710267` before any fit or replay) and `PROTOCOL_ADDENDUM_SECTION11.md` (commit `d3cdee6`, after the main results and before its two arms were replayed). 99,458 + 16,212 replays, no replay error.

## 1. The main finding

**Behind the authority front, no decision method changed anything that matters, and the guard used alone is as good as every learned variant.**

| Arm | Primary: attacks / 2,979 | Primary: benign / 334 | Primary: all tasks / 3,313 | Second: attacks / 2,065 | Second: benign / 48 | Second: all tasks / 2,113 | Fixtures: unsafe released; pairs correct / 43 |
|---|---|---|---|---|---|---|---|
| G3 (strict rule) | 0 | 132 | 1,407 | 0 | 29 | 1,239 | 1; 35 |
| **GV (authority and value guard alone, no learner)** | 0 | 147 | 1,532 | 0 | 32 | 1,386 | 0; 36 |
| HV (ridge model, cost threshold) | 0 | 147 | 1,532 | 0 | 32 | 1,386 | 0; 36 |
| HVnc, HV4, NP05, CRC05, CRC01, GB | 0 | 147 | 1,532 | 0 | 32 | 1,386 | 0; 36 |
| NP01 | 0 | 144 | 1,526 (S2: 1,479) | 0 | 33 | 1,383 | 0; 36 |
| PG (Progent manual policy, replay adaptation) | 0 | 154 | 1,450 | 0 | 35 | 1,305 | 0; 10 |

The reason is visible in Table 5. On the primary recordings 907 attack-labelled calls to restricted tools are proposed during replay, and **all 907 are stopped by the authority front**; on the second population all 559 are. No attack-labelled call ever reaches the stage where a score, a cutoff or a tree decides. Of the 43 unsafe fixture calls, 41 are stopped by the front and 2 by the direct-value constraint. What reaches the rule is legitimate work only: 1,059 and 903 calls that GV releases. A learner at that stage can only withhold some of them.

Consequences:

1. **The gain that earlier documents reported as "L4 over G3" (125 and 147 tasks) belongs to the deterministic guard**, which releases calls whose authority is established although their value is not confirmed by the request. GV obtains exactly that gain without a model. The ridge model of L4 and HV blocked no call on any recording or fixture.
2. **The repair that distinguished HV from L4 on the fixtures is deterministic too** (the direct-value constraint).
3. The estimator is not weak (held-out ROC-AUC 0.993 on all steps, 0.976 on restricted steps; Table 9). It has nothing to discriminate where it is placed: among the 1,134 recorded calls that pass the front there is no attack-labelled one.

## 2. Hypotheses of the protocol

| Hypothesis | Outcome |
|---|---|
| GV completes more tasks than HV and releases an unsafe call that HV withholds | **Refuted in both parts.** Same outcomes on every episode; no unsafe fixture release; the same release decision on every fixture call. By the protocol's wording, the learner of HV has no measured security value over the guard alone |
| NP05 and CRC05: no successful attack and at least HV's task count | Holds, trivially: both equal GV. NP05 withholds 3 legitimate calls on the primary recordings without changing an outcome; CRC05 withholds none |
| NP and CRC cutoffs may not transfer to an unseen attacker objective | **NP transfers approximately; CRC does not** (Table 10). Deciding alone on the held-out objective, NP at 0.05 would release 0% to 5.4% of the attack-labelled steps (above 5% in 1 objective of 9; 2.0% overall); NP at 0.01 would release 1 step of 921. CRC at 0.05 would release up to 39% (above the level in 7 objectives of 9; 16.8% overall), and CRC at 0.01 exceeds its level in 5 of 9. The calibration episodes are not exchangeable with a new attacker objective, as stated before scoring |
| GB has lower held-out log loss than ridge and completes more tasks | **Refuted.** Log loss 0.074 against 0.071; ROC-AUC 0.992 against 0.993; identical outcomes. Its models have 393 to 1,596 leaves against 12 parameters |
| HVnc: removing calibration changes no outcome | Holds |
| HV4: fewer tasks than HV, no security gain | **Not as expected: identical to HV.** Its only Escalate verdicts are the 117 that the declared predicate D2 forces in every arm |

## 3. The two conclusions asked for

**(1) Does a candidate improve the frozen REM baseline, and which component causes it?** Yes, on development data, and the component is deterministic. Against REM v1.0, GV has 0 against 11 and 0 against 3 successful attacks and completes 1,532 against 1,188 and 1,386 against 916 tasks; the all-task interval is above zero on all three evaluations (+10.38 [+1.91, +20.49]; S2 +10.53 [+1.94, +20.88]; second +22.24 [+5.91, +40.26]) and the attack-success interval is below zero on the primary recordings. This contrast was fixed in advance; the arm was built after many rounds on the same data, so it is development evidence, not a confirmation. The cause is the request-derived authority front with the direct-value constraint. No learned or statistically calibrated component contributes.

**(2) Does a candidate add value over strong rules or HV, and does it compete with the Progent configuration that was run?**

- Over HV: no arm differs, except NP01, which loses tasks.
- Over the strict rule G3: GV completes 125 and 147 more tasks with no attack; the interval's lower bound is exactly zero (+3.77 [0.00, +9.25]; +6.96 [0.00, +18.27]); 3 and 2 user tasks gain, none loses. By the rule fixed in advance this is **not established**.
- The learner over deterministic rules: **not established, and matched by a rule.** GV has the task count, the attacks and the fixture outcomes of every learned arm. This is not evidence that a learner can never help: the recordings contain no attack that passes the front, so they cannot show what a learner would do against one.
- Against PG: GV minus PG is +2.48 points [−2.52, +8.69] under S1 and S2 and +3.83 [−7.92, +17.23] on the second population; PG completes more benign tasks (154 against 147; 35 against 32); both have no successful attack. **Not established in either direction.** No equivalence or non-inferiority is claimed. PG is the manual banking policy of repository commit `9befb41`; it is not a configuration of version 3 of the paper, and nothing here concerns Progent's generated or updated policies or live agents.

**Best supported candidate on development data (pre-declared rule): GV.** It ties with the learned arms on every criterion and is the simplest.

## 4. Observations that were not hypotheses

- **A declared predicate withholds authorized calls.** In GV, L4 and HV, predicate D2 (required evidence unavailable at a high tier) withholds 55 and 62 calls that the request supports: updates of a scheduled transaction that carry neither a recipient nor an amount, so that the argument-provenance indicator cannot be computed. G3, which has no predicates, releases them. Whether D2 should apply behind the front is a design decision; no arm without it was declared, and none was run.
- **Where GV and PG differ.** GV completes more episodes in 2 user tasks and fewer in 3 on both populations (Table 4, last column; Tables 8a and 8b). GV is ahead in user tasks 9 and 10 (primary: 200 against 141 and 210 against 140), where PG stays at the undefended agent's level. PG is ahead in user tasks 0, 2 and 12, whose payee or instruction is supplied by a file, and in user task 15 on the second population (49 against 0). The causes were not examined call by call in this study.
- **Decision time.** On the primary recordings the median per call is 0.13 to 0.25 ms for the arms without a model or with the ridge model and 0.62 ms with gradient boosting; the 95th percentile is about 3 ms for all (Table 1). A local diagnostic, not a deployment benchmark.

## 5. Section 11 addendum (Table 13)

- **Cedar front (GVc).** Nine Cedar policies over the context REM computes gave the same release decision as GV on all 7,098 restricted calls of 8,106 replays, with no authorizer error, and the same fixture outcomes. Median decision time of a restricted call 2.33 ms (95th percentile 3.90 ms) through the Python binding. This shows that Cedar can carry these constraints; it changes neither security nor utility. Cedar's documented behaviour of skipping a policy that errors is reproduced in a test in which Cedar answers Allow and the study's wrapper withholds.
- **Provenance rule (GVp).** Withholding value-unconfirmed calls whose value occurs in untrusted content removes no attack (none reaches that stage), withholds 27 and 6 legitimate calls, and moves a few outcomes in both directions: primary 1,530 against 1,532 tasks (−0.06 points [−0.73, +0.54]; user task 13 loses 8 episodes, user task 9 gains 6); second population 1,389 against 1,386 (+0.14 [0.00, +0.43]). Gains occur because withholding an agent's unnecessary call can let the benchmark's task check pass. **No benefit is established.** The matched set GV (no provenance, no learner), GVp (provenance as a rule) and HV (provenance as learned evidence) differs only in those few episodes.

## 6. What limits these results

1. **The benchmark's attacks do not exercise the stage under study.** Every benchmark attack is stopped by the front, in user task 15 as elsewhere. The comparison among decision methods behind the front is therefore a comparison of how much legitimate work each withholds.
2. **All material is exposed.** The front was developed over three revisions on these recordings and fixtures; zero observed attacks is not zero risk and says nothing about requests or attacks it was not written for. Nine attacker objectives and sixteen user tasks.
3. **No adaptation.** A live agent can retry or rephrase after a refusal.
4. **Sources.** The full texts of the NP, CRC and gradient-boosting papers were not readable in this session; the procedures were taken from the authors' or the library's documented implementations, and no formal guarantee is claimed.
5. **Fixtures favour neither side fairly against PG:** most fixture payees are outside PG's fixed list.

## 7. What would change the picture

Requests and attacks written and reviewed by other people (`07_PROSPECTIVE_VALIDATION_KIT.md`), including unauthorized amounts to authorized accounts where the request leaves the amount open, which is the one situation in which a learner or a provenance rule behind the front has something to decide. A live comparison with Progent's generated policies (`08_PROGENT_FULL_FRAMEWORK_PLAN.md`). Neither was executed.
