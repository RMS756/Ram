# Framework comparison validation (final compliance audit, 26 November 2026)

Scope: Section 4.4 of the defence-ready thesis (printed pages 109–140), and every statement about Progent, DRIFT and MELON elsewhere (Chapters 1, 2 and 5, the abstracts, Table 4.11 and Section 4.6).

## 1. Kind of evidence per framework

| Framework | Quantitative offline replay | Architecture / mechanism comparison | Scripted integration test | Live model-based evaluation |
|---|---|---|---|---|
| Progent (manual banking policy, `9befb41`) | **Yes.** Progent's own `check_tool_call` at `3e79753` decides each recorded call; 3 populations; paired with REM. Also checked on reference solutions. | Yes (Tables 4.12, 4.10; Section 4.4.5) | — | **No.** Generated or updated policies were not run. |
| DRIFT (`6fd3df4`) | **No** | Yes (from code; paper at abstract level) | **Yes:** 160 banking v1 episodes × 3 settings, 0 errors, with a test double instead of a model | **No** |
| MELON (`06014c7`) | **No** | Yes (from paper and code) | **Yes:** 480 episodes, 0 errors, with a stand-in embedding (19 Nov) | **No** |
| Defenses distributed with AgentDojo | Descriptive only: the authors' recorded closed-loop runs set against REM's replay on the same task pairs | Yes | — | Recorded by the benchmark authors, not run here |

**Check of the distinctions in the text:**
- Section 4.4.1 names the four kinds of quantitative evidence and states that no live evaluation was done.
- Table 4.13 labels each measurement with its kind.
- Section 4.4.7 opens the DRIFT/MELON subsection with "**No security or utility result was obtained for DRIFT or MELON.**"
- Table 4.12, row 12 (benign task preservation) says "Not measured here" for both.
- The abstract says "DRIFT and MELON … were compared at the level of architecture and code only."

**Verdict:** the distinctions are kept. No passage implies a measured security outcome for DRIFT or MELON.

## 2. Accuracy checks

| Statement in the thesis | Checked against | Result |
|---|---|---|
| Progent: 0 / 2,979, 0 / 681, 0 / 2,065 attack goals; 154 / 334 and 35 / 48 benign; 1,296, 417 and 1,270 tasks under attack | Raw records (`offline_comparison_episodes.jsonl.gz`) | Match |
| REM: 11 / 2,979, 2 / 681, 3 / 2,065; 105 / 334, 18 / 48 | Raw records | Match |
| REM − Progent paired differences, intervals, discordant counts and p-values (Table 4.15) | Raw records, recomputed | Match (all within rounding) |
| Official checker gives the counts of the earlier re-implementation | Old Table 4.21 (0 attacks, 154 benign; all tasks 1,450 = 1,296 + 154; second population 1,305 = 1,270 + 35) | Consistent |
| Every REM-only attack is in `user_task_15` | Raw records: P1 {ut15: 11}, P2 {ut15: 2}, P3 {ut15: 3} | Match |
| Reference solutions: 0 of 144 goals; 13 / 16 (v1) and 14 / 16 (v1.2) benign; refused calls in ut5, ut11, ut14 and ut15 (v1) | `itest_progent.json` | Match |
| Progent fails all benign episodes of "user tasks 14 and 15" | Raw records: true on the primary population; on the second population the zero-completion tasks are **ut9 and ut14** | **Corrected** (population-specific wording) |
| Progent check median 0.22 ms; REM 0.15 ms | Comparative-phase timing results | Consistent |
| DRIFT model calls per episode 10.15 / 9.19 / 3.48; 11 privilege calls per agent instance; 0 errors | `drift_scripted_integration.json` | Match |
| DRIFT "about 9–10 model calls per two-step episode" | Mean executed tool calls are 2.06 per episode (from 1 to 5) | **Corrected:** "per episode (about two tool calls per episode)" |
| DRIFT "adds several language-model calls to each step" | Measured per episode, not per step | **Corrected:** "to each episode (about six to seven more than its own agent without modules)" |
| MELON: cosine > 0.8 fixed in code; README `threshold` unused; `text-embedding-3-large`; AgentDojo ≤ 0.1.29 | `pi_detector.py`, pinned hash | Match |
| R8 sentence "MELON was not executed" | The official code was executed with a scripted agent on 19 Nov | **Corrected:** "not executed with a language model; its official code ran only with a scripted agent" |
| REM limitations row in Table 4.12: "detection and behavioral evidence add nothing measurable" | A3a raises benign completion by +10.5 points, so behavioral evidence has a measurable negative effect | **Corrected** |
| "a benchmark-informed policy reaches the same protection" | Progent 0 against REM 11 attack goals | **Corrected** to "at least the same protection" |

## 3. Progent benchmark-specific policy limitation

Section 4.4.8, item 1 states that the policy is benchmark-informed:
- two of the five permitted recipients occur only in task solutions (`UK123…` in the bill of user task 0; `CA133…` in the request of user task 15 from v1.1.1);
- the attacker's account is excluded, and there is no rule for password changes;
- so the policy "blocks every injection task of this benchmark by construction". Its zero "is not evidence about an attacker whose account is not known in advance".

The limitation is repeated in:
- 4.4.9 (the scope of the finding);
- 4.4.10;
- Table 4.59, row 15;
- threat 22;
- 5.6, item 10;
- 5.8;
- the abstract ("its list of permitted recipients contains values specific to the benchmark").

**Conclusions do not overstate.**
- 4.4.9: "Against Progent's published policy, offline, REM is not better."
- 4.4.11: "The supported conclusion is not that REM outperforms or underperforms these frameworks in general."
- 5.8 and the "does not support" list in 4.6.10: no ranking.

No passage claims REM superiority over Progent, DRIFT or MELON.

## 4. Fairness assessment

| Criterion | Assessment |
|---|---|
| Same episodes, same harness, same semantics for REM and Progent | Yes: paired, NO-ADAPT, step-level; Progent's own enforcement code; policy used as published, neither widened nor narrowed |
| Comparator weakened? | No. The comparator wins, and the thesis reports that it wins. |
| Effect of replay | Stated as affecting REM and Progent alike; not applicable to DRIFT or MELON (Section 4.4.8, item 4) |
| Benchmark version | Stated: all results on banking v1. DRIFT's published v1.2 runs (7 / 144 attack successes, 59 / 144 tasks under attack) are explicitly not set beside REM. |
| Development data for both | Stated (Section 4.4.8, item 5) |
| Recorded closed-loop defenses against replay | Labelled descriptive everywhere it appears |

**Verdict: academically fair.** The remaining asymmetry is unavoidable without a language model: DRIFT and MELON have no outcome measurement. It is stated as a limitation, not hidden.

## 5. Residual weaknesses (to state, not to fix)

1. **One external framework is measured quantitatively, and only in its manual-policy configuration.** That configuration is not one evaluated in the current Progent paper.
2. **The DRIFT paper was not read in full.** Its description rests on the abstract and the code.
3. **Duplication in Table 4.11.** This literature table, kept from R8 inside Section 4.4.3, again lists Progent and MELON (R8 text). Its entries are consistent with Section 4.4, but the duplication could be trimmed if the supervisor asks.
