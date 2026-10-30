# Cross-Chapter Consistency Report (R3, 30 October 2026)

**Scope:** the front matter, Chapters 1–6 and the consolidated reference list of `REM_FINAL_THESIS/chapters/`. Checks were made by script where possible (numbers, citations, equations) and by reading otherwise.

**Link status codes in the matrices:**
- **S:** supported by executed evidence;
- **P:** partly supported (the limit is stated);
- **U:** unsupported (no evidence exists; the thesis says so).

## 1. Traceability matrix: Research Question → Method → Code → Experiment → Result → Conclusion

All four RQs are derived from the objectives and are marked [PD] (proposed, pending supervisor confirmation; D-10).

| RQ | Method (Ch. 3) | Code (Ch. 4) | Experiment (Ch. 5) | Result (Ch. 5) | Conclusion (Ch. 6) | Weakest link |
|---|---|---|---|---|---|---|
| **RQ1** estimation and calibration | Eqs. 3.1–3.4; features Tables 3.8–3.9; Procedure 3.1 nested grouped cross-fitting; metrics Eqs. 3.20–3.21 | `ridge_logistic.py`, `platt.py`, `logit_nll.py`, `evidence.py`, `crossfit.py`, `probabilistic.py`; 193 tests | E0 pilot; E1 held-out predictions on 6,762 recorded steps, 9 outer folds | §5.4, Table 5.3: ROC-AUC 0.938 [0.908, 0.961]; ECE 0.044; per-objective 0.86–0.98; per-backbone 0.74–1.00 | Table 6.1 rows 2–3; §6.1.3 (no calibration benefit) | **P**: labels are a reference-match proxy, not human-audited (D-6); x_ctx1 absent (D-8); one benchmark |
| **RQ2** expected-loss decision vs B1 | Eqs. 3.5–3.10; Table 3.13; B1 by Eq. 3.14 | `loss_matrix.py`, `expected_loss.py`, `a3.py`, `a1.py`, `policy.py` | E2 observe-only verdicts; E4/E5 replay under NO-ADAPT; E6 cost grid | §5.5: interventions on y=1 steps 0.973 vs 0.740, on y=0 steps 0.227 vs 0.056; §5.6: replay ASR 0.004 vs 0.055 (B0 0.226); Δ benign utility −0.195 without reviewer, +0.003 with oracle reviewer; §5.9 grid | Table 6.1 rows 4–5; §6.1.2; §6.1.4 | **P / U**: costs and tiers are declared, not approved (D-9); replay is outside the original scope (D-1); **live enforcement U** (D-15) |
| **RQ3** mitigation residual, escalation rate, latency | Eq. 3.5 (r_mod); Table 3.14 mitigation; Table 3.15 latency | `RemGuard._mitigate`; `time.perf_counter` around `RemGuard.evaluate` | E4/E5 replay; runtime profile | r_mod and residual ASR ≈ 0 (assumption-driven); escalation 19.6% of steps; p95 below 0.6 ms per step | §6.1.4 (residual ≈ 0 is a consequence of NO-ADAPT); §6.5 item 10 | **U** for residual success of a live agent; **S** for the computational cost of REM itself (excludes LLM and tool time) |
| **RQ4** component contribution | §3.11.7 ablations | Evaluation path (the frozen pipeline refuses the calibration ablation, SC-3) | Ablations in held-out, observe-only and replay modes | Table 5.11: action evidence dominates (ROC-AUC 0.799 without it); behavioral evidence lowered utility by 10.5 points at equal ASR; no measured calibration effect | Table 6.1 row 3; §6.1.3 | **P**: nine attacked groups; one run per configuration; no multiplicity correction |

### Objectives (from the approved proposal, as quoted in Ch. 3 §3.1.2)

| Objective | Supported by | Status in Ch. 6 Table 6.2 | Consistent? |
|---|---|---|---|
| O1 Design a REM framework for financial and task-automation agents | Ch. 3, Ch. 4 | Achieved for banking only; design values not approved | Yes. The scope restriction is stated (SD-5) |
| O2 Evaluate against adversarial attacks | Ch. 5 | Partly: exploratory; no live enforcement | Yes |
| O3 Compare with existing approaches | Ch. 5 (B1; distributed defenses for orientation); Ch. 6 Table 6.3 (design level) | Partly: no controlled comparison with any published defense | Yes |

### Links the evidence does not support (stated as such in the thesis)

1. **Live enforcement.** Any claim that REM reduces attack success for a live or adaptive agent. Ch. 5 §5.1, Ch. 6 §6.1.4 and §6.4 state it is unestablished.
2. **Label correctness.** The human label audit has not been run (Ch. 5 §5.10; Ch. 6 §6.5 item 4).
3. **The injection classifier x_ctx1.** Absent. Conclusions about context evidence are restricted to the instruction-pattern indicator (Ch. 4 §4.5; Ch. 6 §6.1.4).
4. **Approved design values.** Costs, tiers, predicates, feature set and label rule are exploratory (Ch. 6 §6.5 item 1).
5. **Superiority.** No claim of superiority over B1 or any published system is made (Ch. 6 §6.4 "Not claimed").

## 2. Numerical consistency

| Check | Method | Result |
|---|---|---|
| Ch. 5 numbers vs `results/pilot_R2/*.json` | `check_chapter_numbers.py` | 538 checked; 524 matched directly; 14 explained (sums, configuration values, unit conversions, the labelled historical R1 memory value) |
| Ch. 4, 6, 1 numbers | Same script | All unmatched values explained (versions, test counts, section numbers, comparison counts) |
| Abstract numbers | Same script, run on `FRONT_MATTER.md` on 30 Oct | 13 checked; 12 matched; the 13th is the test count 193, verified in `pytest_2026-10-30.txt` |
| Abstract ↔ Ch. 5 ↔ Ch. 6 | Reading | ROC-AUC 0.938; 97.3% / 22.7% vs 74.0% / 5.6%; ASR 0.004 vs 0.055; utility −0.195 / +0.003; 3,334 episodes; 6,762 steps; 21 backbones. Identical in all three places. Ch. 6 §6.1.4 gives utility on state-changing tasks (0.47 → 0.17), a different denominator, labelled as such |
| Data counts across chapters | Reading | 3,334 episodes, 2,998 attacked, 336 benign, 6,762 steps, 921 positive steps: consistent in Ch. 1, 4, 5, 6. Ch. 6 Table 6.1 row 1 cites 3,313 replayed episodes (episodes whose all-Allow replay reproduced the record, AM-4), which is a different, stated quantity |
| Memory per step | Reading and re-run | 4.4 KB (R2 file, re-run identical). Corrected in R3 from 2.9 KB, which is now labelled as the R1 value |
| Equation numbers | Reading | Eqs. 3.1–3.22 are cited with the same meaning in Ch. 4 Table 4.6, Ch. 5 and Ch. 6. Eqs. 2.1–2.3 restate 3.1, 3.3 and the rule of 3.6 |

## 3. Terminology and design consistency

| Item | Finding |
|---|---|
| Five layers; no sixth, risk-score or feedback layer | Consistent in Ch. 1, 3, 4, 5, 6 and the architecture figure. The code's five layer constants are tested (`test_exactly_five_frozen_layers`) |
| Verdicts Allow / Modify / Escalate / Block | Same four names and order everywhere |
| Pipeline order (ridge LR → Platt on the logit → tier → predicates → expected-loss verdict → mitigation → audit) | Consistent with `CLAUDE.md` in Ch. 3 and Ch. 4 |
| CUSUM | Observe-only everywhere (Ch. 3 §3.11.10; Ch. 4 §4.10; Ch. 5 §5.8) |
| Attribution | Audit-only everywhere; contract test confirms it cannot reach the verdict |
| A1 / A2 / A3 | Ch. 4 §4.3 explains they are not three methodologies: A3 = REM, A1 = B1, A2 = observe-only CUSUM |
| B0, B1, REM without expected-loss Escalate, reviewer bounds | Defined in Ch. 3 §3.11.7 and used identically in Ch. 5 and 6 |
| Mitigation semantics | Step-level is the reference throughout; the episode-level variant is described as a separate policy pending D-2 |
| Layer of the estimator | Ch. 3 and the thesis text: Layer 4. Code comments: Layer 2. Disclosed in Ch. 4 §4.3 (SC-6) |
| Status labels | "Exploratory", "pending supervisor approval", "[PD]", "SOURCE NOT FULLY VERIFIED" and "NOT EXECUTED" are used consistently. No result is described as significant, superior or confirmatory |
| Chapter cross-references | Ch. 3 Table 3.1 assumes six chapters; the thesis has six (D-11 recorded as an author decision) |

## 4. Inconsistencies found and not corrected

| # | Location | Inconsistency | Why not corrected | Severity |
|---|---|---|---|---|
| 1 | Ch. 1 §1.x RQ list vs Ch. 3 §3.1.3 | Ch. 1 gives shortened RQ wording: RQ2 names "intervention behavior, attack success and utility" where Ch. 3 lists attack success, benign utility, utility under attack and intervention rates; RQ3 says "processing time" where Ch. 3 says "latency". The meaning is the same | The RQ wording is a supervisor decision (D-10); choosing one version would pre-empt it | MINOR |
| 2 | Architecture figure vs Ch. 3 §3.2 | The figure draws Layer 2 → Layer 3 as a sequence; Ch. 3 describes them as producing evidence in parallel. The figure footer reads "EXPLORATORY" | Redrawing the figure requires choosing the depiction; recorded for the author | MINOR |
| 3 | Ch. 6 | Conclusions are organized by finding (Table 6.1), not by RQ. The RQ-by-RQ answer is in Ch. 5 §5.12 | Structural choice of R2; the mapping is complete through §5.12 | MINOR |

## 5. Reference consistency

- One consolidated list of 113 entries replaces the six per-chapter lists. Twenty-one works had been formatted differently in different chapters.
- Every in-text citation resolves to an entry (`verification/citation_check.txt`, re-run on the final chapters).
- Every entry is cited at least once. The three "never matched" keys in the script output are parser artifacts: Chandola (2012) is cited as "Chandola et al. (2009, 2012)", and the two corporate authors are cited in full.
