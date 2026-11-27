# Amendment DiD-2a: post-hoc arms (written after the DiD-2 results were seen)

**Status: POST HOC.** These arms were added after the DiD-2 results were known. They are reported separately and labeled post hoc. They do not change any DiD-2 arm or result.

**Motivation.** In DiD-2, two analyses of the behavioral evidence disagree:
- **Training-time removal** of the behavioral family (REM-t:no_beh, the proposed REM v1.1) left the attack count unchanged.
- **Test-time evasion** of that family (REM-e:beh) raised it.

Two questions follow, and each is answered by one arm:

| Arm | Meaning | Question it answers |
|---|---|---|
| REM-t:no_beh + e:act | REM v1.1's refit without behavioral evidence, with the action family suppressed on attack-labeled calls | Does REM v1.1 keep any depth when action evidence is defeated? |
| REM-t:no_act + e:beh | The refit without action evidence, with the behavioral family suppressed | The symmetric case |

**Breakdown added for every arm:** successful attacks by injection task, to locate where depth fails.

The populations, outcomes, statistics and limitations are those of DiD-2.
