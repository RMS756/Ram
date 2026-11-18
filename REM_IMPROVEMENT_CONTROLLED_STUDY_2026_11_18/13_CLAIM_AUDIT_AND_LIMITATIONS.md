# 13 Claim audit and limitations

## Claims checked against stored outputs

| Claim | Evidence | Status |
|---|---|---|
| The frozen scripted closed loop reproduces exactly | `results/repro_closed_loop_scripted.json`: 960/960 identical | supported |
| The frozen arms reproduce their stored replays | `results/replay_reproducibility.json`: 0 differences | supported |
| "AgentDojo's own reference solutions for ut1/ut7 fail its evaluator" (earlier study) | the harness ended with "Done." instead of `GROUND_TRUTH_OUTPUT` | **retracted** (`01`) |
| "C1 stops ut15×it4, GV_math2 does not" (earlier study) | holds only when the user's calls come first; with the injection right after the first read both release it | **qualified: order dependent** (`02`) |
| ut15×it4 is a label collision | the legitimate update does not trigger the evaluator; the breach is a redirect of the Spotify subscription | **rejected**: a genuine unauthorised effect (`02`) |
| E1+E2 improve utility without security cost | all security constraints hold; +36 / +166 replay tasks; interval lower bound 0 | supported as **development** evidence; **not established** as a general improvement (INCONCLUSIVE) |
| The learned decision improves security | 0 beneficial changes; 0 attack-labelled calls reach it | **not supported** (NULL / harmful) |
| The PG arm equals Progent's manual-policy checker | upstream engine at 0d7ea07 with the 9befb41 policy; 2,551 recorded calls, 0 disagreements | supported |
| REM is better than Progent | full Progent not run; manual policy has higher AgentDojo utility | **not supported** |
| The ledger matters | 0 replay effect; 16 diagnostic and 1 fixture prevented releases; 1 scripted order | supported only for author-written and scripted cases |

## Limitations
1. **Development evidence only.**
   - The populations were seen in earlier studies.
   - E1/E2 were designed from ut11/ut15 and the generalisation cases are author-written.
   - No independent validation was run; the kit exists but no reviewers took part.
2. **Offline replay is NO-ADAPT.** Recorded agents do not react to refusals, so a withheld call can end an episode that a live agent might recover (or abandon).
3. **Scripted agents are not models.** They obey every injection fully and never refuse. They are not an attack-success rate.
4. **The benchmark is small.** There are 16 user tasks and 9 attack objectives. Grouped intervals are wide, and the unseen-task partitions cannot show gains for constructions that appear in only two tasks.
5. **Labels.** Attack labels come from AgentDojo-derived reference labelling. Calls without an attack label are not all legitimate; `03` audits them against the request's values.
6. **Evidence integrity is an assumption.** The `sender`, `recipient` and `amount` fields of executed transaction records are trusted. AgentDojo guarantees this; a deployment would need the bank API to guarantee it. E2 is exposed to a refund-scam pattern (an attacker paying the user the same amount first). Uniqueness only reduces this.
7. **Order dependence and object binding.** The contract ledger does not bind a modification instruction to the object it names. Not fixed.
8. **Full Progent, a live LLM and an external sandbox: not executed.**
9. **AgentDojo version.** The runs use the installed AgentDojo 0.1.35; the Progent fork is AgentDojo 0.1.29. Tool semantics of the banking suite were not diffed between them for this study.
