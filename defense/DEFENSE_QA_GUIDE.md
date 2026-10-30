# Anticipated Questions and Evidence-Based Answers (draft)

Each answer states only what the repository supports, with the file to show.

**Q1. What is new in REM, given NEXUS and AgentTrust?**
- No mechanism is new (Chapter 3 Table 3.16).
- The claim is a specified composition: per-step, tier-indexed expected-loss selection among four verdicts at the tool boundary of an executing financial agent. It is evaluated against a baseline that shares REM's estimator, so differences are attributable to the decision rule.
- NEXUS defines an expected-loss objective but deploys a rule cascade at plan level. Our reading of NEXUS is flagged OI-01.
- Show `RESEARCH_GAP_AND_NOVELTY_AUDIT.md`.

**Q2. Your enforcement numbers come from replaying recorded agents. Isn't that excluded by your own Chapter 3?**
- Yes. Chapter 3 §3.1.4 places it out of scope, and this is recorded as SC-7.
- Live runs were impossible without LLM access. The replay results are labelled out of scope and exploratory, and the supervisor must decide whether to keep them.
- The observe-only results (E0, E1, E3) do not depend on replay.

**Q3. ASR 0.4% looks too good.**
- It relies on NO-ADAPT: a refused agent never retries or reroutes.
- REM also pays for it. Without a reviewer, benign utility falls from 0.52 to 0.31.
- All of the residual 0.4% comes from user_task_15, where the attacker IBAN is the user's own payee in suite v1/v1.1.
- Show `EXPERIMENT_VALIDITY_REPORT.md` §2.4 and §3.1.

**Q4. Did calibration help?**
- No measurable gain: ECE 0.044 calibrated vs 0.042 uncalibrated.
- It did not fix miscalibration on the held-out credential-change fold (ECE 0.189).
- REM never claimed calibration improves control (Chapter 3 §3.7.2).

**Q5. Why keep behavioural evidence if removing it helps utility?**
- The pre-registered E0 rule retained it (fitting-portion AUC 0.80).
- The held-out ablation shows it costs 10.5 utility points at equal ASR.
- Whether to keep it is a pending decision (SD-FEAT update). It was not changed after seeing results.

**Q6. Aren't the costs arbitrary?**
- They are declared exploratory values, not institutional policy.
- E6 varies them over 36 cells, including misspecification. REM's realized loss stays below B1 in all cells.
- That comparison favours REM by construction. The informative outputs are the trade-off curves and the misspecified column.

**Q7. Are 6,762 steps independent?**
- No. All intervals use a grouped bootstrap (injection task, user task), and there are only 9 attacked groups.
- Repeated runs: one per configuration.

**Q8. Could the model just memorise the attacker IBAN?**
- No feature encodes an account identifier.
- Held-out folds remove whole attacker objectives.
- Destination novelty does benefit from the single attacker identity; this is acknowledged as a threat.

**Q9. How were labels validated?**
- The reference-match rule reads ground truths from the installed benchmark.
- Consistency was checked against recorded security outcomes for all episodes.
- 30 sampled episodes were inspected, but by an AI assistant, not a human. A human audit is pending.

**Q10. Why is CUSUM not used for decisions?**
- The design lock forbids CUSUM in the verdict path.
- The pilot also shows its threshold does not hold the false-alarm target on held-out episodes.

**Q11. Latency?**
- Median about 0.2 ms and p95 about 0.5 ms per step, excluding LLM inference, tools and human review.

**Q12. Can it be reproduced?**
- `experiments/pilot/run_all.sh` runs in about 10 minutes and reproduced every number exactly from commit `aa66f22`.
- It requires AgentDojo 0.1.35 and the repository's `runs/` at commit `089ed468`.
