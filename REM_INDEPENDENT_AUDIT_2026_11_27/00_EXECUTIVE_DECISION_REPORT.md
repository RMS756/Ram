# REM independent scientific audit: executive decision report (27 November 2026)

**Scope.**
- An audit of what the existing REM work proves.
- No file outside this directory was modified.
- No new experiment was run.

**One verification was re-executed:** the frozen REM v1.0 pipeline, from public inputs. It reproduced the stored results with **zero non-timing numeric differences** (02 §1.1).

**Independence caveat.** The same AI assistant produced the earlier studies, so this audit is not independent in authorship. It relies on recomputation and re-execution rather than on earlier documents' statements.

## Files

| File | Content |
|---|---|
| `01_Project_Inventory.md` | Versions, studies, thesis editions (including a fork), git-history limits, baseline |
| `02_Evidence_and_Results_Audit.md` | Fresh reproduction; recomputed counts; **utility-floor finding**; claim statuses; integrity checks A–D |
| `03_Literature_and_Research_Gap_Audit.md` | 24 entries with verified identifiers and evidence levels; gap verification |
| `04_Comparative_Framework_Analysis.md` | REM v1.0 / REM-DiD / REM-X vs ROPE, AGATE, Progent, MELON |
| `05_Research_Contribution_and_Novelty.md` | Levels A, B, C with novelty and defensibility |
| `06_Final_REM_Selection_and_Justification.md` | Version selection |
| `07_Additional_Experiment_Necessity.md` | What existing evidence answers; the one small offline arm worth running |
| `08_Final_Thesis_Scientific_Position.md` | Problem, gap, aim, objectives, RQs, contributions, novelty, architecture, evidence, limitations, ten examiner questions |

## Answers

1. **Is the research problem scientifically meaningful?**
   - **Yes.** Whether layered boundary defenses for financial agents provide real defense in depth, and whether a learned risk decision adds value over rules, are open evaluation questions with financial consequences.

2. **Is the claimed research gap supported by the literature?**
   - **Only as an evidence gap.** The thesis already frames it this way, correctly.
   - A *mechanism* or *architecture* gap is **not** supported. Every element and the layered combination are published (NEXUS, Agent-Sentry, Spotlight-Guard, Progent, ROPE, AGATE, CaMeL, AIS).
   - Several close works were read only at abstract level.

3. **Does REM have a defensible scientific contribution?**
   - **Yes, an empirical and methodological one.**
   - It is a pre-registered, component-level evaluation showing that REM's five layers do not provide depth: one learned component carries all measured protection, by withholding nearly every financial action.
   - Simple rules match it.
   - It is supported by verified replay-evaluation pitfalls.

4. **What is genuinely novel about REM?**
   - **No algorithm or architecture.**
   - What is distinctive is the **evidence**: a controlled ablation and rule comparison of a layered, risk-informed boundary defense on executable banking traces.
   - Two findings were not found in the literature read:
     - the replay benign-utility floor (REM v1.0's benign successes are exactly those of withholding every state-changing call, P1);
     - removal versus evasion disagreeing on the same layer.
   - Both need qualification: one benchmark, replay, and in the second case modelled evasion.

5. **Which REM version should be retained?**
   - **REM v1.0, unchanged.**
   - Pinned by the tree hashes of `rem/`, `configs/` and `experiments/pilot/`, identical from `7c79883` to `e50fbdd`, and by config sha256 `8e1aa107…`.

6. **Which previous development efforts should be excluded from the final thesis?** These are excluded **as artifacts**:
   - REM-X and Amendment 01 (design only);
   - REM-DiD's `remdid` candidate (its authorization is an oracle);
   - G1, GV/HV, REM-A/B/C, REM-B2/B3, C1 contracts, E1/E2, and the authorization-generalization candidate.

   Their consistent negative findings may be cited as supporting exploratory evidence. **REM v1.1** is reported as a confirmed utility result of one modification, not adopted.

7. **Are the existing experiments sufficient?**
   - **Yes, for the recommended position**, scoped to NO-ADAPT replay on AgentDojo banking.
   - They are **not** sufficient for any live, adaptive, cross-benchmark or deployment claim.

8. **Is any additional experiment essential?**
   - **No.**
   - One small offline arm is **recommended**: withhold every state-changing call on P2 and P3. It would test whether the utility-floor finding holds beyond P1. It costs minutes of CPU and no model calls.
   - A live closed-loop check is optional and blocked by undecided backbones and budget.

9. **What should the thesis claim?**
   - REM v1.0 was designed, implemented and reproduced.
   - In replay it withholds recorded injected financial actions (11 / 2,979; 3 / 2,065).
   - It does so almost entirely through its learned decision, by withholding almost all state-changing calls. Its benign completion on P1 equals the withhold-everything floor.
   - Its other layers add no measured protection.
   - Simple deterministic rules attain comparable replay security.
   - Removing behavioural evidence improves task completion (confirmed).
   - **Nominal layering is not defense in depth**, shown on this system and benchmark.

10. **What must the thesis explicitly avoid claiming?**
    - Any new algorithm or architecture.
    - That REM provides defense in depth.
    - That combining context and behavioural evidence helps.
    - That the learned or calibrated decision outperforms rules.
    - Robustness against adaptive attackers or live agents.
    - Superiority over Progent, ROPE, MELON, AGATE or any published defense.
    - That Progent's manual-policy result generalizes, since it is an oracle list.
    - Any REM-DiD or REM-X security property.
    - That 31% benign completion reflects REM's ability to release legitimate payments.
    - Any MELON or DRIFT comparison result: none was run.

## Decision table

| Decision | Recommendation | Evidence | Confidence |
|---|---|---|---|
| Experimental baseline | REM v1.0 on P1 / P2 / P3, NO-ADAPT replay | Fresh reproduction identical (02 §1.1); recomputed counts (02 §1.2) | **High** |
| Final artifact | REM v1.0 unchanged; v1.1, REM-DiD and REM-X excluded as artifacts | 06 | **High** |
| Primary contribution | Empirical: nominal five layers ≠ depth; one learned component carries all protection by near-total withholding | Pre-registered ablation `93e6630`; utility-floor identity (02 §1.3) | **High** (within replay scope) |
| Gap framing | Evidence gap only; no mechanism gap | 03 §2 | **Medium-high** (abstract-level reading of several works) |
| Novelty claim | None for mechanism or architecture; qualified novelty for empirical and methodological findings | 03, 05 | **Medium** |
| Learned-decision value over rules | Not shown; report as a negative result | Confirmatory rule arms (02 §2); studies in 02 §4; DiD-3 B9 vs B9n | **Medium-high** |
| Additional experiments | None essential; the withhold-all arm on P2 / P3 recommended | 07 | **High** |
| Thesis wording of utility | Must state that P1 benign completion equals the withhold-everything floor | 02 §1.3 | **High** |
| Title / topic wording | Supervisor to confirm: printed title is "Runtime Evaluation and Mitigation (REM)…"; stated topic is "Defense in Depth…" | 01 §2 | — (decision needed) |
| Submission edition | Supervisor to choose: humanized and DiD editions are forks of the ninth edition | 01 §2 | — (decision needed) |
| Literature update | NEXUS is now peer reviewed (Findings of AACL 2026); cite and position REM's decision engine against it | 03 row 15 | **High** |
