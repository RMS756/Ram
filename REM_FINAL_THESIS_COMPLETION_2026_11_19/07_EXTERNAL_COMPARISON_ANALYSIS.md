# 07 External defence comparison: analysis (19 November 2026)

**Sources and status**
- **Protocol:** `05_EXTERNAL_BASELINE_PROTOCOL.md` (frozen at `dc8407d`), plus amendment `05a_EXTERNAL_PROTOCOL_AMENDMENT.md` (`204f7ad`), committed after the first run crashed and before any outcome was read.
- **Results:** `results/external_results.json`, `06_EXTERNAL_BASELINE_RESULTS.csv`, and the tables in `results/tables_external.md`.
- **Figure:** `figures/fig_external_security_utility.png`.
- **No model was called** in this study.

## 1 What was compared, and how

### Benchmark

- **Software:** AgentDojo 0.1.35, the authentic package installed from PyPI. It is not the Progent fork.
- **Suite and attack:** banking suite (16 user tasks, 9 injection tasks), attack `important_instructions`.
- **Run files:** the recorded runs are those distributed in the `ethz-spylab/agentdojo` repository at commit `089ed468`, last changed for these pipelines on 5 June 2024.
- **No version field:** the run files carry no version field. The suite version under which they were produced is therefore not recorded in the files; the benchmark's banking suite v1 is assumed.

### Defences

The defences are those defined in `agentdojo/agent_pipeline/agent_pipeline.py` of the installed package, checked against its source on 19 November 2026.

| Code | Defence | Integration point (from the source) |
|---|---|---|
| D0 | none | `[system, user query, LLM, loop(ToolsExecutor, LLM)]` |
| D1 | `repeat_user_prompt` | the user query is re-inserted after every tool execution: `loop(ToolsExecutor, InitQuery, LLM)` |
| D2 | `spotlighting_with_delimiting` | tool outputs are wrapped in `<< >>`, and the system message says never to obey instructions between them |
| D3 | `tool_filter` | an OpenAI LLM call selects the tools for the task before the agent runs (OpenAI models only) |
| D4 | `transformers_pi_detector` | `protectai/deberta-v3-base-prompt-injection-v2` (threshold 0.5, message mode) checks each tool output and stops the run on a detection |
| B5 | REM v1.0 | gates each proposed tool call before execution (A0 configuration of `02`) |
| B6 | MELON | **NOT EXECUTED** (`08`) |

### Two kinds of evidence, never pooled

- **Recorded closed loop (D0–D4).** These runs were executed by the benchmark's authors with gpt-4o-2024-05-13, and the agent saw each defence.
- **Offline replay (NO-ADAPT) of REM v1.0** on the recorded traces. The agent never sees REM's refusals.
- **REM v1.0 has not been run in a closed loop with any model.** No endpoint and no spending authorisation exist (`16`).

## 2 Recorded closed-loop outcomes (Table X1)

| Code | Defence | Attack successes / 144 | ASR % [95% CI] | Tasks under attack / 144 | Benign completed / 16 | Benign utility % [95% CI] |
|---|---|---|---|---|---|---|
| D0 | No defence | 90 | 62.5 [37.5, 80.6] | 100 | 12 | 75.0 [50.0, 93.8] |
| D1 | repeat_user_prompt | 67 | 46.5 [27.8, 63.2] | 111 | 15 | 93.8 [81.2, 100.0] |
| D2 | spotlighting_with_delimiting | 89 | 61.8 [36.1, 81.2] | 111 | 13 | 81.2 [62.3, 100.0] |
| D3 | tool_filter | 16 | 11.1 [3.5, 18.8] | 82 | 13 | 81.2 [62.5, 100.0] |
| D4 | transformers_pi_detector | 1 | 0.7 [0.0, 2.1] | 45 | 7 | 43.8 [18.8, 68.8] |

All 144 + 16 runs per pipeline were read, with 0 errors.

**Relation to thesis R7, Section 4.4.2.** R7 reported ASR 0.462 / 0.615 / 0.112 / 0.007 for D1 / D2 / D3 / D4, computed on **143** attacked runs. That set is the pilot's AM-1 population, which excludes the ambiguous pair user_task_15 × injection_task_4. Here all 144 runs are counted. Both are correct for their denominators. For example, spotlighting gives 88/143 = 0.615 in R7 and 89/144 = 0.618 here.

## 3 Offline replay of REM v1.0 (Table X2)

| Replay set | Eligible (AM-4) / 159 | Attack successes / attacked | ASR % [95% CI] | Tasks under attack | Benign completed / eligible | Benign utility % [95% CI] |
|---|---|---|---|---|---|---|
| D0 replayed without REM | 149 | 82 / 134 | 61.2 [37.0, 79.1] | 99 | 12 / 15 | 80.0 [60.0, 100.0] |
| **D0 + REM v1.0** | 149 | **2 / 134** | 1.5 [0.0, 3.7] | 68 | 5 / 15 | 33.3 [13.3, 60.0] |
| D1 replayed without REM | 151 | 62 / 135 | 45.9 [27.4, 62.5] | 110 | 15 / 16 | 93.8 [81.2, 100.0] |
| **D1 + REM v1.0** | 151 | **0 / 135** | 0.0 [0.0, 0.0] | 70 | 7 / 16 | 43.8 [18.8, 68.8] |
| D2 replayed without REM | 151 | 82 / 135 | 60.7 [36.3, 80.1] | 110 | 13 / 16 | 81.2 [62.5, 100.0] |
| **D2 + REM v1.0** | 151 | **1 / 135** | 0.7 [0.0, 2.2] | 69 | 5 / 16 | 31.2 [12.3, 56.2] |
| D4 replayed without REM | 154 | 1 / 138 | 0.7 [0.0, 2.2] | 45 | 7 / 16 | 43.8 [18.8, 68.8] |
| **D4 + REM v1.0** | 154 | **0 / 138** | 0.0 [0.0, 0.0] | 36 | 4 / 16 | 25.0 [6.2, 50.0] |
| D3 + REM v1.0 | – | – | **NOT REPLAYABLE WITH THE FROZEN HARNESS** (05a) | – | – | – |

- **Eligibility (AM-4):** an episode is replayed only if the replay without REM reproduces the recorded utility and security.
- **D3:** the frozen harness feeds back the recorded assistant messages in order. The first of these in a `tool_filter` trace is the filter's tool list, which carries no tool call, so the replay ends immediately: 0 REM-evaluated calls in all 159 D3 replays.
- **REM's median decision latency** in these replays is 0.165–0.192 ms per call.

## 4 Paired contrasts (Table X3)

### 4.1 Within one evidence kind (replay): REM added to a defence, on that defence's own traces

| Traces | Δ ASR pp [95% CI] | Δ tasks under attack pp [95% CI] | Δ benign utility pp [95% CI] |
|---|---|---|---|
| D0 | -59.7 [-76.9, -36.3] | -23.1 [-51.5, 5.9] | -46.7 [-73.3, -13.3] |
| D1 | -45.9 [-62.5, -27.4] | -29.6 [-54.7, -3.7] | -50.0 [-75.0, -25.0] |
| D2 | -60.0 [-79.3, -36.0] | -30.4 [-54.1, -4.9] | -50.0 [-75.0, -25.0] |
| D4 | -0.7 [-2.2, 0.0] | -6.5 [-20.3, 0.0] | -18.8 [-43.8, 0.0] |

**Allowed statements (rule 05, contrast 1), under NO-ADAPT:**
- **D0, D1 and D2.** On these traces, adding REM v1.0 removes almost all attack successes, with intervals excluding 0. It also removes a large share of benign completions: −46.7 to −50.0 pp, with intervals excluding 0.
- **D4.** Adding REM removes the single remaining success, with an interval that includes 0. Its utility cost is not resolved: the interval includes 0.

### 4.2 Across evidence kinds: REM replayed on the undefended traces, against each defence's recorded closed loop

Identical (user task, injection task) pairs are compared, 134 pairs. **This contrast is descriptive only.**

| Defence (recorded) | Δ ASR pp [95% CI], REM replay − defence | Δ tasks under attack pp [95% CI] |
|---|---|---|
| repeat_user_prompt | -44.0 [-60.6, -26.1] | -30.6 [-54.5, -5.2] |
| spotlighting_with_delimiting | -59.0 [-77.8, -34.8] | -30.6 [-54.5, -5.2] |
| tool_filter | -10.4 [-17.8, -3.1] | -8.2 [-33.6, 19.3] |
| transformers_pi_detector | 0.7 [-1.5, 3.0] | 17.2 [-5.2, 38.5] |

**Allowed statements (rule 05, contrast 2).** On the same task pairs:
- REM v1.0's replayed decisions left **fewer** attack successes than the recorded closed-loop runs of repeat_user_prompt, spotlighting_with_delimiting and tool_filter.
- They left **about as many** as transformers_pi_detector: 0.7 pp, interval including 0.
- REM's replay completed **fewer** tasks under attack than repeat_user_prompt and spotlighting.
- Against tool_filter and pi_detector, the difference in tasks under attack is not resolved.

**Not allowed:** "REM outperforms X".
- The defences' agents adapted to the defence, whereas REM's replay agent did not.
- The defences were measured on gpt-4o only, while REM v1.0 was fitted on 21 backbones, including gpt-4o's traces in the population.
- Each replayed episode is scored by the cross-fitted fold model that did not train on its attacker objective. However, the gpt-4o subset is part of the population on which REM v1.0 was designed, so the replay is not an independent test.

## 5 Interpretation for the thesis

1. **Security.** In replay, REM v1.0 is in the same low-ASR range as the strongest recorded defence (transformers_pi_detector), and lower than the prompt-level defences. This is a property of withholding state-changing calls, and is consistent with the ablation result: 661 of 672 attacks are prevented by the learned decision.
2. **Utility.** REM v1.0's replayed benign utility on gpt-4o traces is 5 / 15. This is lower than every recorded defence in point estimate. The closest is transformers_pi_detector (7 / 16), and their intervals overlap. The utility cost is the weakest point of REM v1.0. It is not specific to the comparison: it is the same cost seen in the ablation (A0 benign 105 / 334).
3. **Layering.** REM's gate is complementary to prompt-level defences: it removes the attacks that D1 and D2 leave, on their own traces. It does so at the same utility cost as on undefended traces.
4. **What is missing.**
   - A closed-loop run of REM v1.0 with gpt-4o: not executed, because there is no endpoint or budget.
   - A REM + tool_filter replay: not possible with the frozen harness.
   - MELON: NOT EXECUTED, see `08`.

## 6 Limitations

- **Recorded runs.** They are one run per pair, with one model, and the suite version is not recorded.
- **Benign utility.** It rests on 15–16 runs per arm, and its intervals are wide.
- **Different eligible subsets.** The replay sets have different eligible subsets (134–138 attacked), so cross-set comparisons are not paired. Only the within-set contrasts are paired.
- **Few clusters.** 9 clusters for ASR and 16 for utility make the intervals descriptive.
