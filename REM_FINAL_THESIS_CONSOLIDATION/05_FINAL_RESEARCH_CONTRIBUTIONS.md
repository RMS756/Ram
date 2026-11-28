# 05: Final research contributions [PD]

**Basis.**
- Numbers are taken from `REM_FINAL_SCIENTIFIC_RECONCILIATION_2026_11_28/01` and `02` §10. Every number was re-checked against the stored results there; the working copy's tables re-verify at 0 mismatches.
- All results are **NO-ADAPT replay** results on AgentDojo 0.1.35 banking (v1) recordings at `089ed468`, unless stated otherwise.

**Terms.**

| Term | Meaning |
|---|---|
| P1 | Primary population: 2,979 attacked + 334 benign episodes |
| P2 | Held-out templates: 681 episodes |
| P3 | Second population: 2,065 attacked + 48 benign episodes |

**What the thesis does not claim:**
- a new algorithm, estimator, architecture or mechanism;
- superiority over NEXUS, Progent, AIS, MELON or any framework;
- to be the first layered or financial-agent defense;
- live or real-world financial operation.

## A. Primary empirical contribution: limited complementary protection

**Claim.** The thesis measures, rather than assumes, whether REM v1.0's five-layer organization produces defense in depth for a banking agent. It finds limited complementary protection **within a shared learned decision and enforcement pathway**:

| Finding | Evidence |
|---|---|
| Enforcement is necessary | Shadow mode equals no defense: 672 / 174 / 436 attacks on P1 / P2 / P3 |
| The learned pathway (estimator, calibration, expected-loss selection, removed together) is necessary | Removing it gives 672 / 174 / 435 attacks |
| Two evidence families cover different attack classes | Action evidence: removal lowers attack-call withholding on P3 by −9.12 pp [−23.45, −0.74] |
| | Behavioural evidence: under modelled suppression on P1, attacks rise from 11 to 131, and 119 of the 120 added are in the credential-change objective |
| Detection indicator and predicates | No measurable effect |

**Bound.** This is **not** evidence of robust operational defense in depth:
- one decision and one enforcement point carry all protection;
- the controls are partly redundant;
- there is no adaptive attacker and no live agent.

**Thesis location in the working copy:**
- Ch. 1 §1.11, paragraph "Primary empirical contribution" (edit `R1-5`);
- Ch. 4 §4.5.12 (`R4-6`) and §4.6.13 (`R4-8`);
- Ch. 5 Table 5.x RQ4 row (`C5-3`).

## B. Component-level evaluation contribution

**What it establishes.** Two protocol-frozen, paired ablations (19 Nov, commit `dc8407d`, P1; 21 Nov, commit `93e6630`, P1–P3) test, on identical episodes, which components are necessary for the measured protection and which add cost:
- calibration alone: no attack outcome changed (P1);
- consequence-independent thresholds instead of expected loss: 164 vs 11 attacks (P1), with more tasks completed;
- behavioural evidence removed: higher completion, no measured security change;
- context indicator, predicates, Modify: no measurable effect.

**What it cannot establish:**
- **The estimator's own contribution:** it is never isolated, because no non-predicate verdict exists without it.
- **The Input & Context layer's own contribution:** it is a dependency of the action features and `x_beh1`, so removing it is a combined removal.
- **The value of the classifier:** it is not implemented.
- **The value of hygiene:** it is not exercised by the data.
- **Interactions:** components were removed one at a time or as declared blocks.
- **Validation:** the data had been examined during development, so this is not validation on untouched data.

**Not called "pre-registered":** the protocols were committed before scoring. That order is supported by the commit history and hashes; it is not a formal pre-registration.

## C. Removal versus suppression (exploratory)

**Definitions:**
- **Removal** (realistic): the component is removed and REM is refitted without it.
- **Suppression** (idealized, label-conditioned): on attack-labelled calls only, a family's features are set to their not-fired values while everything else stays fixed.

**Finding:** the two give opposite assessments of the behavioural family:
- removal: no security loss (11 attacks), 35 more benign tasks (REM v1.1);
- suppression: 131 attacks;
- after removal, suppressing the action family gives 653 attacks, against 90 with the behavioural family present.

**Bound:**
- suppression is **not a model of an adaptive attacker**: it does not say how an attacker would silence a family;
- it is exploratory and on P1 only.

**Independent support:** a layered tool-call gateway study reports that deletion and constant-verdict substitution of one stage attribute contributions very differently (Abasıkeleş Turgut & Gümüş, 2026b; abstract). This supports, but does not prove, the lesson.

## D. Security–utility contribution

**Result on P1:**
- attack success falls from 22.6% to 0.4% (11 of 2,979);
- benign completion falls from 52% (175/334) to 31% (105/334);
- 81.5% of legitimate state-changing calls in benign episodes are withheld.

**The withhold-all reference (P1 only):**
- REM v1.0's 105 completed benign tasks are **exactly** those completed by a reference arm that executes no state-changing call;
- REM completes 94 more tasks under attack than that reference (1,083 vs 989);
- REM has 11 attacks to the reference's 0, all in `user_task_15`.

**The reference is not useful financial task completion.** It completes no payment, payment change or credential change. Its role is to show that REM v1.0's benign completion, in replay, is the completion attainable without any state change.

**Comparisons:**
- Progent's published banking policy, decided by its authors' code on the same episodes, admits no attack and completes more tasks. Its recipient list is benchmark-specific.
- Simple rules match REM's replay security on P3 with equal or higher completion; the differences are not resolved.

## E. Evaluation-methodology contribution

**Strengths:**
- whole attack objectives are held out;
- arms are paired on identical recorded episodes;
- protocols are committed before scoring;
- replay fidelity was checked: 3,313 of 3,334 episodes reproduce the recorded outcomes with every call allowed;
- the replay was reproduced exactly on 27 Nov 2026;
- a deployment simulation through a fail-closed gateway shows exact verdict parity (5 Nov 2026).

**Limits:**
- NO-ADAPT: a withheld call cannot redirect the agent;
- one benchmark, one attacker account, recordings examined during development;
- not a live deployment, not real financial transactions, not an independent replication;
- recorded-trace replay of AgentDojo has a published precedent (Kekatos et al., 2026; thesis §2.11.3), so it is not itself a methodological contribution.

## F. Negative findings (legitimate, qualified results)

| Negative finding | Qualification |
|---|---|
| Context indicator (`x_ctx2`): no measurable effect | Template-matched; the classifier is absent |
| Deterministic predicates D1/D2: no measurable effect | Predicates alone withhold no attack-labelled call |
| Calibration: changes no attack outcome; did not repair the miscalibrated credential-change fold (ECE 0.189) | Monotone map; rankings unchanged by construction |
| Modify, Escalate and Block are equivalent without a reviewer | Step-level semantics; no reviewer |
| The learned decision is not shown to add value over simple rules on P3 | Differences not resolved |
| Authorization-aware supervised policy rejected (132 vs 11 attacks) | Did not transfer to an unseen attack objective |
| Exact-string provenance fails under identifier reformatting | REM v1.0 held at 11 through `x_act2` |
| Behavioural evidence: no measured benefit on removal | Exploratory suppression shows a coverage role |

## Mapping to the working copy

| Contribution | Where (edit id) |
|---|---|
| A | `R1-5`, `R4-6`, `R4-8`, `C5-3`, `C5-10`, abstracts `AB-2`, `AB-3` |
| B | `R1-6b`, `R4-1`, `R4-2`, `R4-3`, `T1`–`T10` |
| C | `R4-4`, `R4-9a/b`, `C-NEG1`, `C5-4` |
| D | `R1-6a`, `R4-5`, `AB-1`, `C5-10` |
| E | `A3`, `A3-ch4`, `A6` |
| F | Existing Ch. 5 §5.5, unchanged; qualified by `C-NEG1` and `C5-4` |
