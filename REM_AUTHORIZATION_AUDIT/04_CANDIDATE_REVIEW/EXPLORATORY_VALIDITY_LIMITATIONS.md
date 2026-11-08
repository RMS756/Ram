# Exploratory-evaluation disclosure (to be carried into the thesis)

1. **Post-hoc candidate development.**
   - REMnoEsc was declared after the R1 results.
   - The request cue, the parser and gating were designed after earlier results and after the first fixture set showed that every transfer was withheld.
   - None was pre-registered.
2. **Repeated use of one corpus.** Every arm used the same 3,313 eligible recorded episodes, the same corpus used to fit and evaluate the original REM. No arm has an independent confirmatory corpus.
3. **Many arms, no multiplicity correction.**
   - Arms: original; REMnoEsc; cue; cue + noEsc; parser; gating; parser + gating.
   - Each under two grouping schemes, plus two fixture sets.
   - No family-wise or false-discovery correction was applied. No arm-level difference should be called significant.
4. **Small diagnostic fixtures.**
   - 16 synthetic probes plus 5 logical cases, written by one author who knew the purpose.
   - Report counts only. They are not representative, not blind and not independent of design knowledge.
5. **Recorded-trace replay, not live agents.**
   - Every corpus number comes from offline, step-level replay under NO-ADAPT: the agent never reacts to a refusal.
   - A live agent might retry, rephrase or route around a refusal, so attack and utility outcomes could differ in either direction.
6. **Reviewer model.**
   - The primary configuration has no reviewer, so Escalate withholds the call.
   - With an idealized reviewer that approves exactly the legitimate escalations, REM's benign successes rise from 105 to 166 / 334 and attacks stay at 11 / 2,979 (reproduced).
   - The utility cost of REM is therefore largely the cost of an *absent* reviewer. Real reviewers are neither free nor perfect.
7. **Declared exploratory costs.** C_FA, C_miss, C_mod, C_esc and the amount limit are declared exploratory values pending supervisor approval (SD-1). The Allow boundaries (0.03 / 0.015) follow directly from them.
8. **Unavailable code.** The cue, parser, gating and user-task enforcement numbers are reported by the implementer, and their commit (`bb4218d`) was not available to the audit.
9. **Fold dependence.** On the same call, frozen folds disagree: 0–5 withhold every legitimate first payment, while 6–8 release some. Single-fold fixture results must not be generalized.
