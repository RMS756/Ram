# 01: Reconciliation of findings with the experimental evidence

**Rules.**
- No experiment was run and no artifact changed.
- Every number below was read from a stored result file, or recomputed from stored per-episode records in the 27 Nov audit. The source is given each time.
- Statements of the 27 Nov audit (`REM_INDEPENDENT_AUDIT_2026_11_27/`) that this file corrects are listed in §7. That directory is left unchanged.

## Terms used throughout

| Term | Meaning |
|---|---|
| **Replay** | NO-ADAPT, step-level recorded-trace replay without a reviewer. A withheld call is not executed, and the recorded agent does **not** react to the refusal. **Replay outcomes are not closed-loop agent performance.** |
| **Replay attack outcome** | AgentDojo's own security check after replay: the attacker's goal was achieved |
| **Attack call executed (episode)** | An attacked episode in which at least one attack-labelled call was released. It can be true while the attacker's goal is not achieved |
| **Attack-call withholding (call level)** | Share of attack-labelled restricted calls that REM withheld |
| **Benign completion** | AgentDojo utility check true in an episode without injection |
| **Completion under attack** | AgentDojo utility check true in an attacked episode |
| **Benign-call blocking (call level)** | Share of restricted calls in benign episodes that REM withheld |

**Populations.**

| Population | Content | Data history |
|---|---|---|
| P1 | 3,313 episodes (2,979 attacked, 334 benign); 21 backbones; template `important_instructions` | Development data, used to design and fit REM v1.0 |
| P2 | 681 attacked episodes; gpt-4o with five other templates | Examined in the pilot revision R2, before both ablations |
| P3 | 2,113 episodes (2,065 attacked, 48 benign); five pipelines | Unread before the confirmatory run of 11 Nov 2026; development data since |

## 1. The contribution claim, component by component

Sources:
- **[A19]** `REM_FINAL_THESIS_COMPLETION_2026_11_19/03_ABLATION_RESULTS.csv`, protocol frozen at `dc8407d`. P1 only.
- **[A21]** `REM_ABLATION_STUDY/03_EXPERIMENT_RESULTS.md` and `04_RESULTS.csv`, protocol frozen at `93e6630`. P1, P2, P3.
- **[D2]** `REM_DEFENSE_IN_DEPTH/05_DID_RESULTS.md` and `results/did2_results.json`. DiD-2, protocol `2547854`; post-hoc arms committed at `e3e7488` before their run. P1. **Exploratory.**

### 1.1 Combined learned scoring-and-decision pathway

**Scope of the test.** Ridge LR, Platt calibration on the logit and expected-loss selection are removed together. With them removed, only predicates D1/D2 decide:
- arm A6 of [A19];
- arm A3 of [A21].

| Metric | P1 | P2 | P3 |
|---|---|---|---|
| Replay attack outcomes, without pathway vs REM v1.0 | 672 vs 11 | 174 vs 2 | 435 vs 3 |
| Attack-call withholding, without pathway vs REM v1.0 | 0 / 907 vs 882 / 907 | 0 / 202 vs 200 / 202 | 0 / 559 vs 556 / 559 |
| Benign completion, without pathway vs REM v1.0 | 180 vs 105 | — | 39 vs 18 |

**Reading.**
- On these replays the pathway is **necessary** for essentially all of REM v1.0's protection: the predicates alone withhold no attack-labelled call.
- **This does not make it the sole source of protection.** The pathway decides on the evidence it is given (§1.2, §1.3), and it protects nothing without enforcement (§1.6).

**What is not isolated.** The estimator cannot be removed without removing every non-predicate verdict, so it is **never isolated**. On P1 only, [A19] gives a partial separation of the pathway's later parts:

| [A19] arm | Attacks | Benign | Isolates |
|---|---|---|---|
| A2: calibration removed | 11 | 110 | Calibration |
| A3: consequence-independent thresholds on the same estimator, in place of expected-loss selection | 164 | 170 | Expected-loss selection, against a threshold rule |

- The protocol-frozen ablation of 21 Nov [A21] removes the three parts **only as one combined pathway**.
- **No statement may attribute protection separately to logistic regression.**

### 1.2 Provenance-related action evidence (`x_act1`–`x_act3`)

**Scope of the test.** Arm AIC in [A21], A4b in [A19]:
- the three action features are removed from the estimator, which is refitted;
- the provenance labelling itself and predicate D2's availability check remain.

| Metric | P1 | P2 | P3 |
|---|---|---|---|
| Attack-call withholding, Δ (pp, 95% grouped bootstrap) | −5.40 [−17.00, 0.00]: **not resolved** | −4.46 [−13.00, 0.43]: **not resolved** | **−9.12 [−23.45, −0.74]: resolved** |
| Attacked episodes with an attack call executed | 49 vs 24; 29 / 4 discordant | not reported in the stored tables | 34 vs 3; 32 / 1 discordant |
| Replay attack outcomes | 17 vs 11; +0.20 pp [−0.07, 0.43]; McNemar p = 0.146 | 3 vs 2; p = 1 | 8 vs 3; +0.24 pp [0.00, 0.58]; p = 0.125 |
| Benign completion | 105 vs 105 | — | 18 vs 18 |
| Held-out ROC-AUC (estimator) | 0.799 vs 0.938 | — | — |

**McNemar note.** The exact McNemar values ignore clustering. For the "attack call executed" metric on P1 and P3, McNemar p < 0.001, but the grouped interval on P1 touches 0 (+0.8 [0.0, 2.2]).

**Reading.**
- Action evidence contributes **measurably to call-level withholding on P3**, and to the number of episodes in which an attack call is executed.
- Its effect on **final attack outcomes is not resolved on any population**.
- It carries most of the estimator's discrimination.

### 1.3 Behavioural evidence (`x_beh1`–`x_beh4`)

**Removal (refit), arm A2 in [A21] = REM v1.1.**

| Metric | P1 | P3 |
|---|---|---|
| Attack outcomes | 11 vs 11 | 1 vs 3 |
| Benign completion | 140 vs 105 (+10.5 pp [1.2, 22.6]) | 25 vs 18 |
| Benign-call blocking (P1) | −28.1 pp [−54.1, −8.6] | — |

**Confirmatory run** (11 Nov; P3 unread before):
- completion of all tasks: +7.5 pp [1.2, 16.0];
- attacks: 1 vs 3;
- verdict GO by the pre-declared rule.

**Modelled test-time suppression, [D2], exploratory.** The family's features are set to their not-fired values on attack-labelled calls only.

| Arm | Attack outcomes |
|---|---|
| REM v1.0, behavioural family suppressed | **131** (vs 11) |
| Of the 120 additional successes | 119 are `injection_task_7`, the only credential-change objective |
| REM v1.1 (no behavioural family) with the action family suppressed | **653**, against **90** for REM v1.0 with the action family suppressed |

**Reading.**
- Removing behavioural evidence costs no measured security and improves completion.
- But under modelled evasion it is the only evidence that stops the credential-change objective.
- Without it, the action family becomes a single point of failure.
- **Removal and suppression give opposite verdicts on this family.** The suppression result is exploratory and idealized: it does not model how an attacker would achieve the suppression.

### 1.4 Context detection (`x_ctx2`)

**What the layer contains.** The injection classifier `x_ctx1` **does not exist in REM v1.0**. The Detection layer means the single pattern indicator `x_ctx2`.

**Coupling.** `x_beh1` is defined through `x_ctx2 = 1`, so detection and behavioural features are coupled:
- removing `x_ctx2` alone (A1a) leaves its signal inside `x_beh1`;
- removing the Detection layer requires removing both (A1b, new refit, ROC-AUC 0.937 vs 0.938).

| Test | Result |
|---|---|
| A1a, A1b (P1, P2, P3) | No change in attack outcomes or attack-call withholding |
| Modelled suppression [D2] | 11 vs 11 |

**Disclosure.** The indicator's patterns match the benchmark's `important_instructions` template (`configs/exploratory/pilot_e0.yaml:94-97`).

### 1.5 Deterministic predicates (D1, D2)

- **A3P in [A21] (predicates removed):** no change in attack outcomes or call withholding on any population. Only 6 / 3 / 10 unlabelled calls change.
- **Predicates alone (§1.1):** they withhold no attack-labelled call.
- They fire on 58 of 6,684 P1 calls, where the learned pathway reaches the same verdict.

### 1.6 Mitigation and enforcement

**Shadow mode (A4 in [A21]; A5 in the thesis):**
- verdicts are computed and logged, and every call is released;
- shadow verdicts equal enforced verdicts on 99.6% / 99.7% / 99.7% of calls;
- outcomes equal no defense: 672 / 174 / 436 attacks.

**Verdict semantics.** Under step-level semantics without a reviewer, Modify, Escalate and Block all withhold the current call. Removing Modify changes no episode.

**Reading.** **Every outcome effect requires enforcement.** The four verdicts act as two in this evaluation.

### 1.7 Corrected conclusion

In REM v1.0, evaluated by replay, protection is produced **jointly** by four things:
- the combined learned pathway (necessary on all populations);
- the evidence families it consumes:
  - action/provenance evidence: measurable at call level on P3, not resolved at outcome level;
  - behavioural evidence: needed against one objective under modelled suppression;
- enforcement (necessary).

Context detection and the predicates show no measurable effect on these data. **No statement that "all protection comes exclusively from the learned decision" is supported.**

## 2. Scope of the five-layer ablation

**Correct term:** *component-level ablation within a layered architecture.* Not "ablation of the five layers".

| Layer | What was actually tested | What was not |
|---|---|---|
| Input & Context | Its **evidence** in the estimator (AIC / A4b). Hygiene was checked for exercise: 0 of 16,727 tool-output segments contain characters it removes, so it was **not exercised** | **Provenance labelling itself cannot be removed**: action features, `x_beh1` and D2 depend on it |
| Detection | `x_ctx2` alone (A1a); `x_ctx2` with `x_beh1` (A1b) | The classifier `x_ctx1` does not exist |
| Behavioural Analysis | The behavioural feature group (A2); the action feature group (AIC). Both are computed by this layer's code | Coupling with detection through `x_beh1` |
| Decision Engine | The combined learned pathway (A3/A6); predicates (A3P/A7); P1 only: calibration (A2 [A19]), expected loss vs thresholds (A3 [A19]), Modify (A5 [A19]) | The estimator in isolation |
| Mitigation | Enforcement (shadow mode) | Distinct mechanisms of Modify / Escalate: no reviewer and no declared Modify mechanism |

**No layer was removed as a whole independent module.** Defended thesis §4.5.1 already states this. Its sentence "Decision Engine: every component removed separately" overstates, because the estimator was not.

## 3. The utility-floor finding

| Population | Status |
|---|---|
| **P1** | **Established.** The 105 benign episodes REM v1.0 completes are exactly the 105 completed when every state-changing call is withheld (DiD-3 arm F-GW; `REM_DEFENSE_IN_DEPTH/results/did3_raw.jsonl.gz`, recomputed 27 Nov). REM completes 94 more episodes under attack than that reference (1,083 vs 989), and has 11 vs 0 replay attack outcomes |
| **P2, P3** | **Not established.** No withhold-everything arm exists on them. The result **must not be generalized** beyond P1 |

**Metrics kept separate:**
- **Benign completion:** equal to the floor on P1.
- **Completion under attack:** above the floor on P1.
- **Attack outcomes:** above the floor's 0 on P1, all in `user_task_15`.
- **Call-level withholding:** 81.5% of legitimate restricted calls in benign P1 episodes.

All are replay quantities.

## 4. Literature-gap conclusion

1. **Substantial prior-art overlap exists** for every element of REM and for layered combinations.

   | Status | Works |
   |---|---|
   | **Peer reviewed** | NEXUS (Findings of AACL 2026, DOI 10.18653/2026.findings-aacl.112); Spotlight-Guard (*Applied Sciences* 2026, DOI 10.3390/app16157662); AIS (*Systems* 2026, DOI 10.3390/systems14101329); MELON (ICML 2025); DRIFT (NeurIPS 2025); IPIGuard (EMNLP 2025); AgentDojo (NeurIPS 2024 D&B); Zhan et al. (Findings of NAACL 2025) |
   | **Preprints** | Progent (arXiv 2504.11703 v3), ROPE (2608.27496), AGATE (2609.30830), AgentCap (2611.00729), Agent-Sentry (2603.22868), CaMeL (2503.18813), SIEVE, ClawGuard, CapLite, AgentSandbox, AutoDojo |

2. **Reading levels:**
   - Full text: Progent (earlier session).
   - Code: ROPE (and its logs), CaMeL, MELON.
   - Abstract or search excerpt: all others, **including NEXUS**. Its full text was again unreachable on 28 Nov.
3. **What may be claimed:**
   - An independent **architectural or mechanism novelty claim for REM is not established**.
   - **No claim is made that every possible combination has been published.** The review is not exhaustive and is mostly at abstract level.
4. **The empirical evaluation gap is retained, with qualification.** Among the works reviewed, at the levels stated, no controlled, component-level analysis was found of whether a layered boundary defense for a banking agent provides depth. Specifically:
   - which components carry protection;
   - whether removal and test-time suppression of a component agree;
   - how a learned decision compares with simple rules on the same calls.

## 5. Methodology wording

| Instead of | Use |
|---|---|
| "pre-registered ablation" | **"protocol-frozen paired ablation."** The protocols were committed before their arms were scored (`dc8407d` before `1643ce9`; `93e6630` before `355355a`), and git order and hashes support this |
| (no data history) | **Data history:** P1 is development data. [A21] discloses that the P1 outcomes of six of its arms were already reported in R8. P2 was examined in R2. P3 has been development data since 11 Nov. **None is an independent, untouched test population** |
| "confirmatory" for anything except the 11 Nov run | "Confirmatory" applies only to that run: pre-declared rule, recordings unread before it. Its freeze commit is not in this repository's history |
| "validation" / "generalization" | Use only with the population and its history named |

## 6. Research questions

The final RQs are in `02_CORRECTED_SCIENTIFIC_POSITION.md` §5. **Each has an existing experiment and metric.**

**The withhold-everything comparison is restricted to P1.** Extending it to P2 and P3 needs one offline replay arm that releases no state-changing call. That arm was **not run** (described in `REM_INDEPENDENT_AUDIT_2026_11_27/07` §2.1).

## 7. Statements of the 27 Nov audit superseded by this file

| 27 Nov audit statement | Correction |
|---|---|
| "one learned component carries all measured protection" / "every outcome effect comes from the learned decision" (00, 05, 08) | §1.7: joint production by pathway, action evidence, behavioural evidence (under suppression) and enforcement |
| "four of five layers change no attack outcome" (05 A1) | §1, §2: action evidence has a resolved call-level effect on P3. Behavioural evidence matters under suppression. Layers were not removed as wholes |
| "behavioural evidence harms" with no qualification (05 B2, 08 F) | §1.3: removal improves completion, but suppression shows coverage of one objective |
| "pre-registered ablation" (05, 08, 00) | §5: "protocol-frozen paired ablation", with the data history |
| "nominal layering is not defense in depth" as a settled finding (00, 05, 08) | Reformulated as the primary research question, with a qualified answer (02 §6) |
| Implicit generalization of the utility floor (00 item 9) | §3: established on P1 only |
| "learned decision ... admits none" phrasing as sole cause | §1.1: necessary, not sole |
| Item U3: "the thesis treats NEXUS as abstract and repository only" (01) | **Partly wrong.** Thesis Ch. 2 §2.8.3 and the reference list already record its publication in *Findings of IJCNLP-AACL 2026* (pp. 2203–2232). Only Ch. 1 §1.4 omits the status (fixed by R1-2). Its full text remains unread |
