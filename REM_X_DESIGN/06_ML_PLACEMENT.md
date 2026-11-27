# Deliverable 6: Where machine learning belongs in REM-X

**Status of the evidence:**
- All REM-DiD numbers are **preliminary**: exploratory re-use of recorded AgentDojo 0.1.35 banking episodes, NO-ADAPT replay, and oracle authorization.
- Sources: `REM_DEFENSE_IN_DEPTH/51_DID3_RESULTS.md` (DiD-3), `05_DID_RESULTS.md` (DiD-2) and `20_ARCHITECTURE_CURRENT_V1_0.md` (thesis ablation, as recorded there).
- **None of it shows behaviour against an adaptive attacker.**

> **[SUPERVISOR DECISION REQUIRED]**
> - The frozen REM pipeline puts the ridge LR → Platt → tier → expected-loss verdict on the primary runtime path (CLAUDE.md, FROZEN REM PIPELINE).
> - Options 2 and 3 below change the *role or scope* of that component.
> - This document **recommends**; it does not change the frozen design.
> - REM v1.0 remains the thesis result as evaluated.

## 1. The four options against the evidence

| Option | What it means | Evidence for | Evidence against | Assessment |
|---|---|---|---|---|
| **1. Learned model as primary decision-maker** (REM v1.0 as evaluated) | 4B's expected-loss verdict decides every call; no authorization layer | **Without authorization**, the learned decision accounts for all 661 attacks REM v1.0 prevents (B1: 11 of 2,979 succeed vs 672 with no defense) | B1 withholds 1,305 of 1,644 legitimate state-changing calls; 105 of 334 benign tasks (the replay floor). **Fragile under evasion:** action-family evasion raises B1 to 90 attacks; REM v1.1 under the same evasion reaches 653 (DiD-2) | **Not recommended** for REM-X |
| **2. Learned model as advisory, tighten-only signal** | 4B stays in the verdict path under most-restrictive precedence. It can only withhold, never release. Recommended scope: calls whose sensitive fields are **not fully pinned** (unspecified or delegated) | B9p (4B consulted only for calls not fully pinned): 0 attacks, 172 benign tasks. With authorization bypassed, LEARN alone gives 11 attacks (vs 174) and covers 2 attack calls no other control covers. Removing it from X0 raises attacks from 0 to 1 | Behind oracle authorization, 4B adds 0 security in every one of 36 cost cells. Full-scope consultation (B9) costs 68 benign tasks vs B9n (105 vs 173; raw p = 0.014, **Holm p = 0.12, not significant**) | **Recommended, conditionally:** narrow scope; to be re-tested with non-oracle authorization |
| **3. Learned anomaly detector** (sequence model over tool calls, in L3) | An unsupervised or one-class score over action sequences, advisory | None in REM. Agent-Sentry reports a learned sequence bound (abstract level only) | Untested in REM. Would need its own training population, and must use action inputs only (invariant I-3.1). A GRU/LSTM/Transformer trajectory model is a **forbidden reintroduction** (CLAUDE.md) | **Not recommended now.** Any non-forbidden variant (e.g. n-gram or count model) needs a supervisor decision and a separate protocol |
| **4. Deterministic only** (no learned component in the verdict) | 4A, PROV, DET, BEH rules plus L5 | B9n (no LEARN, oracle authorization): 0 attacks, 173 benign tasks. With authorization bypassed, X-LEARN (all evidence controls but LEARN): 1 attack | Loses the 2 calls only LEARN covers; the +1 attack under bypass (not statistically distinguishable from 0, but the declared strict criterion fails) | **Viable baseline**; compare against option 2 in every experiment |

## 2. Inconsistencies that must be acknowledged, not smoothed over

1. **Regime dependence, not contradiction.**
   - The learned decision is decisive *without* authorization (thesis: all 661 prevented attacks) and adds nothing *behind* oracle authorization.
   - Its value depends on how much authorization already covers.
   - With realistic (non-oracle) authorization its value is unknown.
2. **Utility vs depth.**
   - REM v1.1 (refit without the behavioral family) gains 35 benign tasks with no security loss (11 vs 11 attacks), but loses depth: 653 vs 90 attacks under action-family evasion.
   - Removal-based ablation alone would have recommended v1.1.
3. **Labeling rule.**
   - With the idealized reviewer, PROV-only lets 17 attacks through, not 13: escalated calls labelled 0 by the reference rule still contributed to attack success.
   - The label rule, not the model, limits this comparison (human audit package, file 53).
4. **Replay floor.**
   - 105 of 334 benign episodes succeed even when every state-changing call is withheld.
   - Utility differences below that floor are invisible, and failures cost no measured utility in replay.
5. **Statistical strength.**
   - The 68-task cost of full-scope 4B is consistent across leave-one-user-task-out subsets, but not significant after Holm (p = 0.12) with 16 user-task clusters.
6. **Oracle authorization only.**
   - Every "behind authorization" result assumes a perfect trusted approval channel.
   - B2e (explicit-parameter authorization) completes 122 benign tasks, not 173.
7. **Detector construction.** The detectors were written with knowledge of the benchmark's injection templates. Their coverage is optimistic.
8. **Fail-open is not punished in replay.** F-AUTH-open allowed 0 attacks only because the recorded agent behaves as recorded.

## 3. Recommendation [PD]

| Item | Recommendation | Status |
|---|---|---|
| Primary decision | **Deterministic authorization (4A) plus L5 enforcement** | Recommended; supervisor decision on role |
| 4B (frozen learned decision) | Retained in the verdict path, **tighten-only**, consulted for calls not fully pinned (B9p configuration) | [SUPERVISOR DECISION REQUIRED] on scope |
| 4B on delegated fields (REM-X D1) | Candidate second line on the values delegation admits. **Not tested:** no delegation exists yet | [X-P]; must be tested in E-AC (file 07) |
| Learned anomaly detector in L3 | Not adopted | Needs supervisor decision and separate protocol |
| ML anywhere it can loosen a denial | **Never** (invariant I-4.1) | Fixed |
| Attribution | Audit only | Frozen |

**What would change this recommendation:**
- With non-oracle authorization (explicit or delegated), option 2 might reduce attacks that option 4 lets through. If it does at a measured utility cost, the trade-off must be reported in both directions.
- If it reduces none, option 4 is preferred on parsimony.
