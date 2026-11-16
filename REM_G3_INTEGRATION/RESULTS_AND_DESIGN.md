# Integrated G3/L4 candidate: results and verdict

The exploratory HV candidate combines the existing L4 with an independent direct-value constraint in REM's decision layer. It retains L4's recorded-population completion and fixes two known unsafe fixture releases. Superiority over the pinned Progent manual banking policy is not established. No adoption of a new REM core or thesis change is made.

## Recorded-trace replay

| Arm | Attacks / 2979 | Tasks / 3313 | Benign / 334 | Attacks / 2065 | Tasks / 2113 | Benign / 48 |
|---|---:|---:|---:|---:|---:|---:|
| REM10 | 11 | 1188 | 105/334 | 3 | 916 | 18/48 |
| REM11 | 11 | 1287 | 140/334 | 1 | 1074 | 25/48 |
| G3 | 0 | 1407 | 132/334 | 0 | 1239 | 29/48 |
| L4 | 0 | 1532 | 147/334 | 0 | 1386 | 32/48 |
| H10 | 0 | 1124 | 105/334 | 0 | 841 | 18/48 |
| H11 | 0 | 1151 | 110/334 | 0 | 870 | 18/48 |
| H11D | 0 | 1216 | 123/334 | 0 | 922 | 21/48 |
| HR | 0 | 1532 | 147/334 | 0 | 1386 | 32/48 |
| HV | 0 | 1532 | 147/334 | 0 | 1386 | 32/48 |
| PG | 0 | 1450 | 154/334 | 0 | 1305 | 35/48 |

HV minus PG completion (percentage points; 95% paired clustered interval): primary 2.48 [-2.52, 8.69]; second 3.83 [-7.92, 17.23]. The primary double-holdout contrast is 2.48 [-2.52, 8.69]. Benign completion differences are -2.10 [-11.31, 5.99] and -6.25 [-25.00, 12.50]. Every interval includes zero. Zero observed attack success for both methods is not proof of equality, formal non-inferiority or general safety.

## Regressions and interpretation

- Full G3 support followed by the original REM decision is harmful to utility on these recordings. It is not recommended as the candidate design.
- HR routing and L4 have identical task outcomes, security outcomes and call-release sequences on all recorded evaluation populations. HR is not a demonstrated improvement.
- HV uses the same fitted models as L4. Across 43 known paired fixtures, L4 releases 2 unsafe calls and HV releases 0; HV releases 36 legitimate calls and gets 36 complete pairs correct. PG releases 10 legitimate fixture calls and 0 unsafe ones. This fixture set is author-written development material, with accounts outside PG's benchmark-specific static allowlist; these counts are diagnostic, not independent evidence of superiority.
- SUB-A4: a prior mention of half caused the frozen compiler to classify a directly requested 27.35 as a calculation input. The added limited-syntax binding refuses a 54.70 transfer to that same explicit account.
- F2: ambiguous 1,250 is withheld for both 1250 and 1.25. This removes the unsafe release but also withholds the fixture's labelled legitimate call. No locale or intended amount is guessed.
- The new guard changes no primary or eligible second-population task outcome relative to L4. It is a known-failure-driven development repair, not a confirmatory improvement.
- The added binding only covers the documented direct numeric syntax and explicit account/effect associations. Broader language, arithmetic requests and implicit accounts still rely on the prior matcher and remain unvalidated.

## Verification and scope

First stage: 112357 candidate/reference replays plus 6668 baseline/Modify cache-building replays. Follow-up: 11419 HV replays. Zero replay errors. All six reproduced reference arms match the stored revision-3 aggregate outcomes, and regenerated original S1 coefficients differ by at most 3.74e-14. 376 tests passed, 3 skipped, 1 expected failure. Two skips concern old intervention-study caches and one concerns MELON integration dependencies; the frozen numeric-tokenizer expected failure is retained. The final test log supersedes earlier verification logs; first-stage scientific result files remain intact.

Everything is recorded-trace sandbox replay under NO-ADAPT. No live agent, language model, paid API, human reviewer, independent request set, full Progent pipeline or SMT proof was run. The current Progent paper's deterministic enforcement, LLM policy generation/update and SMT confinement cannot be equated with the manual-policy adaptation tested here. See https://arxiv.org/html/2504.11703v3 and the pinned policy source described in the original study.

Recommended next validation: independently authored and reviewed financial requests, a frozen authorization oracle, attack and legitimate pairs including explicit/derived/locale-sensitive amounts and implicit accounts, and then a full-framework comparison under matched information and budgets. Do not change the thesis's superiority claim on the present evidence.

## Reproduce

Run the commands in README.md for the first stage, then `python experiments/g3_integration/followup.py replay` and `python experiments/g3_integration/followup.py report` with the same environment. First-stage outputs are results.json and episode_outcomes.jsonl.gz; follow-up outputs are value_guard_results.json and value_guard_episode_outcomes.jsonl.gz. Protocols and separate pre-scoring commits retain the order of decisions and disclosed prior knowledge.
