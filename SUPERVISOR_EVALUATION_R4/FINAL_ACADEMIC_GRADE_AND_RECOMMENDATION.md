# Final Academic Grade and Recommendation

**Thesis:** *Runtime Evaluation and Mitigation (REM): A Security Framework for Financial AI Agents*, version R4. Commit `9ab3f9e`, branch `claude/rem-r4-corrections-3ktvze`.

**Not an official grade.** This is an estimate by an evaluator acting as a supervisor and examiner. The awarding institution's rubric, grade bands and examiners decide the actual grade.

**Conflict of interest.** This evaluation was written by the same AI assistant that drafted much of the thesis text and code. **It is not independent.** An independent human examination is required.

## 1. Rubric

| Criterion | Weight | Score /100 | Weighted |
|---|---:|---:|---:|
| Problem and objectives | 10 | 65 | 6.50 |
| Literature and gap | 15 | 60 | 9.00 |
| Methodological rigour | 20 | 62 | 12.40 |
| Originality | 15 | 45 | 6.75 |
| Implementation | 10 | 75 | 7.50 |
| Experimental design and evidence | 15 | 45 | 6.75 |
| Discussion | 5 | 75 | 3.75 |
| Writing | 5 | 70 | 3.50 |
| References and integrity | 5 | 60 | 3.00 |
| **Total** | **100** | — | **59.15 ≈ 59** |

## 2. Justification by criterion

### Problem and objectives: 65

| | |
|---|---|
| **Justification** | The action boundary for financial tool calls is a sensible, well-motivated problem. Scope and RQs are explicit, and §1.11 is honest about what was and was not achieved |
| **Evidence** | Ch. 1 §1.3–1.11 |
| **Weaknesses** | The objectives come from an absent proposal. O1 names task-automation agents, but only banking is evaluated. Gap D was not re-assessed. The title is broader than the evidence |
| **Required** | Attach the proposal; narrow the title and objectives; restate Gap D |

### Literature and gap: 60

| | |
|---|---|
| **Justification** | Transparent and critical synthesis, with verification levels and a currency update that honestly narrows the gaps |
| **Evidence** | Ch. 2 §2.2, §2.12–2.13; PRISMA reproduced |
| **Weaknesses** | One index searched; recall of the named prior art 3/13; no full texts; Gap D semantic; the closest systems compared only on design features; excessive length |
| **Required** | Search a second index; read the full texts of the 10–15 closest works; restate the gaps; shorten the chapter |

### Methodological rigour: 62

| | |
|---|---|
| **Justification** | Mathematics correct. Nested grouped cross-fitting has no leakage. The decision layer is isolated by the same-estimator baseline |
| **Evidence** | `ALGORITHM_MATHEMATICAL_AUDIT.md`; `crossfit.py` |
| **Weaknesses** | r_mod circular; Modify ≡ Block in replay; replay outside the approved method; one run per configuration; proxy labels; no regret metric; x_act2 close to an identity proxy; a residual contradiction (§3.11.11) |
| **Required** | Fix the Modify/r_mod design; add repeats; add a cost-independent metric; correct the contradiction |

### Originality: 45

| | |
|---|---|
| **Justification** | Compositional only. The gap is narrow. A one-feature provenance rule matches REM's attack interception in this benchmark |
| **Evidence** | `NOVELTY_AND_CONTRIBUTION_ASSESSMENT.md` |
| **Weaknesses** | No mechanism-level novelty; added value not demonstrated |
| **Required** | Reframe as an empirical study, and show where the added machinery helps, if anywhere |

### Implementation: 75

| | |
|---|---|
| **Justification** | Clean, tested and fail-closed. Bit-for-bit reproducible; results traced cell by cell |
| **Evidence** | 205 tests pass; 2 re-executions with 0 analytical differences; independent recomputation matches |
| **Weaknesses** | The evaluated path is not the frozen pipeline; injection classifier and reviewer absent; Modify is not a modification; `converged` unchecked |
| **Required** | Equivalence test, or retire one path from the claims; implement a real Modify or rename it |

### Experimental design and evidence: 45

| | |
|---|---|
| **Justification** | The evidence is honestly labelled, but it is weak for the claims |
| **Evidence** | `EXPERIMENTAL_RESULTS_AUDIT.md` |
| **Weaknesses** | No live enforcement; labels unaudited; costs unapproved; no simple or published baselines; ASR difference concentrated in two single-task categories; one run |
| **Required** | The minimum experiments in §5 below |

### Discussion: 75

| | |
|---|---|
| **Justification** | Exemplary honesty about what is not supported; conclusions paired with their limits |
| **Evidence** | Ch. 6 Table 6.1, §6.1.4, §6.4 |
| **Weaknesses** | O3 self-assessment generous; omits the provenance-rule and r_mod points |
| **Required** | Update to follow the new baselines and the reframing |

### Writing: 70

| | |
|---|---|
| **Justification** | Clear and precise, with consistent notation |
| **Evidence** | All chapters |
| **Weaknesses** | Chapter 2 is too long; cross-reference errors (m-1, m-2); dense and partly reads like a report; formal pages missing |
| **Required** | Copy-edit; use the university template |

### References and integrity: 60

| | |
|---|---|
| **Justification** | References authentic: a 6/6 spot-check matched, and the register is transparent |
| **Evidence** | `REFERENCES_VERIFICATION_REPORT.md` |
| **Weaknesses** | No full texts; Platt never read; 21 partial records; FV codes inconsistent with the register; **no similarity check; formal declaration of AI use outstanding** |
| **Required** | Run the similarity check; make the declaration; read the core sources |

## 3. Recommendation

### **Verdict C: MAJOR REVISIONS REQUIRED.**

The thesis is **not ready for submission or defence in its current form.**

It is a careful, transparent, reproducible *exploratory* study, and its mathematics and implementation are sound. It is not rejected (verdict D), because none of the following applies:
- the work is not fabricated;
- the problem is legitimate;
- the defects can be corrected within a master's timeframe, provided LLM access or a re-scoping is agreed.

It is not "minor revisions" (verdict B), for two reasons:
- **New experiments are needed**: simple baselines, the human label audit, and live runs or a formal re-scoping.
- **The formal and integrity requirements are unmet.**

## 4. Answers to the ten questions

| # | Question | Answer |
|---|---|---|
| 1 | Is the research problem strong enough? | **Yes, partly.** It is legitimate and well motivated. The stated gap is narrower than presented |
| 2 | Is the literature review rigorous? | **Partly.** It is transparent and critical, but it is limited in reach (one index, no full texts, 3/13 recall) |
| 3 | Is the algorithm mathematically correct? | **Yes.** Every equation checked; no error. Weak spots: the plug-in nature of the rule, and r_mod circularity in the inputs |
| 4 | Is it a defensible master's-level contribution? | **Only if reframed** as an empirical study and the simple baselines are added. **Not as currently framed** |
| 5 | Is the code faithful? | **Yes for the estimator, decision rule and evaluation; partly for the features and mitigation.** x_act2 is weakened, Modify ≡ Block, the frozen pipeline is unused |
| 6 | Are the experiments valid and reproducible? | **Reproducible: yes** (verified). **Valid as evidence of protection: no.** It is replay under NO-ADAPT with proxy labels and a near-oracle feature |
| 7 | Are the results sufficient? | **No** |
| 8 | Are the references authentic? | **Yes, as far as checked** (6/6 sample; 90 recorded). They are not verified against full texts. Plagiarism has **not** been excluded |
| 9 | Is the thesis internally consistent? | **Mostly.** There are residual contradictions: §3.11.11 vs Table 5.11; the Table 5.12 reference; the FV codes vs the register; AS-9 vs one run |
| 10 | Should it proceed to defence? | **No.** Not before the CRITICAL issues are resolved |

## 5. The five most critical issues

1. **C-2: Added value not demonstrated.** A parameter-free provenance rule matches REM's attack interception (97.1% vs 97.3%) with fewer false interventions (14.7% vs 22.7%). It also releases 92 of 180 benign state-changing steps, against REM's 33. No such baseline is in the thesis.
2. **C-1: No enforcing evidence.** The central claim rests on replay under NO-ADAPT, which makes residual ASR and r_mod ≈ 0 by construction. In step-level replay, Modify is a Block.
3. **C-3: Labels unvalidated.** The labels are proxies built by reference matching. The user_task_15 collision affects 16 of 21 backbones. The human audit stands at 0 of 145 items.
4. **C-4: Design values unapproved.** Costs, tiers, predicates, features and the label rule are exploratory. Every decision result depends on them, and nothing makes them realistic for finance.
5. **C-5: Formal and integrity requirements.** There is no student name, no template, and no approved proposal attached. The formal declaration of AI use is outstanding, for text largely drafted by AI. No similarity check has been done.
