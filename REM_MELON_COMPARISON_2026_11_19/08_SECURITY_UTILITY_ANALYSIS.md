# 08 Security–utility analysis: REM v1.0 vs MELON

## Status: NO MEASURED COMPARISON EXISTS

**No live episode was run** in any arm (`14`). There is therefore:
- no observed ASR, utility or false-positive figure for REM or MELON under a common agent;
- no security–utility trade-off to characterise from data.

**Nothing in this file is a result.**

## What must not be done with the material that does exist

| Material | Why it cannot stand in for the comparison |
|---|---|
| R8's replay of REM v1.0 (e.g. 2 / 134 attacks on gpt-4o undefended traces) | NO-ADAPT replay; MELON cannot be replayed (below) |
| MELON's published AgentDojo results (Zhu et al., 2025) | Different runs, models and possibly suite versions. Citing them beside REM's numbers would compare different populations as if paired, which the protocol forbids. |
| The scripted integration pilot (`05`) | The agent obeys every injection by construction and the embeddings are a stand-in. Its counts reflect the test double, not either defence's quality. |

## Can MELON be evaluated offline on recorded traces? (Phase 10)

**No.** MELON's decision at each step needs two things from a live model:
1. the agent's **next** call, generated in a context that already contains the current tool output;
2. a **masked re-execution**, a new generation by the same model in a context that never occurred in any recording.

A recorded trace supplies (1) only for the trajectory that actually happened. It never supplies (2).

- **A "replay MELON".** Substituting the recorded next call for (1) and inventing (2) would be a different algorithm. It is not run under MELON's name.
- **A detector-only diagnostic.** One that embeds recorded calls without a masked run would not be MELON either.
- **Status:** the **secondary replay analysis** and the **detector-only diagnostic** are both **NOT EXECUTED (not supported by MELON's algorithm)**.

## Expected differences: hypotheses, to be tested by the live run, not findings

| Aspect | REM v1.0 | MELON | Hypothesis |
|---|---|---|---|
| What triggers an intervention | estimated probability of attacker inducement, from provenance, behaviour and context features, under tier-dependent costs | similarity between the agent's next calls and the calls it makes when the user task is masked | MELON's trigger requires the injected call to be **task-independent**. REM's requires the call's evidence to look attacker-sourced. They can fail on different attacks. |
| Effect of an intervention | withholds one call; the agent continues | stops the episode | REM may complete more user tasks after an intervention if the agent re-plans. MELON loses the rest of the task. |
| False positives | R8 replay: 81.5% of legitimate state-changing calls withheld in benign episodes | depends on whether benign next calls resemble masked-run calls (e.g. both read transactions) | Both can over-intervene. The live run measures this. |
| First turn | evaluated | not inspected | An attack effective in the first turn cannot exist in AgentDojo banking, because the injection arrives through a tool output. |

**Use of this table.** These hypotheses are recorded **before** any result so that the analysis cannot be fitted to outcomes. They are not conclusions.
