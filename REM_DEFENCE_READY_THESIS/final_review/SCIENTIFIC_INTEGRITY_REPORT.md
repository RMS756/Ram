# Scientific integrity report: final review (27 November 2026)

## 1. Numerical consistency

| Check | Method | Result |
|---|---|---|
| Recomputation from raw records | `tools/verify_numbers.py` reads only per-episode and per-call records: `REM_ABLATION_STUDY/05_EPISODE_RESULTS.jsonl.gz`, `REM_FINAL_THESIS_COMPLETION_2026_11_19/results/raw/*.csv.gz`, `REM_COMPARATIVE_EVALUATION_PHASE/results/offline_comparison_episodes.jsonl.gz`, AgentDojo recorded runs, `itest_progent.json` and the DRIFT scripted-run file. Re-run on 26 Nov after its extension. | Reproduces every earlier value. Now also yields the paired call-level outcomes of the 19-Nov variants used in Table 4.27. |
| Printed cells against the recomputation | `tools/check_thesis_numbers.py`: counts in Tables 4.14, 4.26, 4.28, 4.29 and 4.30; point estimates, 95% intervals, discordant counts and McNemar p in Tables 4.15, 4.27 and 4.31 | **498 cells, 0 mismatches.** Tolerance is 0.05 for one-decimal rounding of values stored to two decimals. |
| Headline numbers | Raw records | REM v1.0: 11 / 2,979 attack goals reached, 105 / 334 benign tasks. Progent's policy (offline replay, own checker): 0 / 2,979 and 154 / 334. 21 recorded backbones; "22 backbones" appears nowhere. |
| Figures 4.6–4.8 | `tools/make_figures_19nov.py` asserts that the plotted counts equal the raw-record recomputation before drawing | Pass |
| Cross-study identity | 7 shared arms × 3,313 episodes | Identical |

**New values introduced by this review: Table 4.27, rows A4c, A4d and A4e.** All are computed from existing per-episode records. No experiment was run.

| Variant | Attack call executed | Tasks under attack | Benign episodes with a call withheld |
|---|---|---|---|
| A4c | 0.0; 0 / 0 | +0.6 [0.1, 1.6]; 19 / 0 | −4.2 [−11.6, 0.0]; 0 / 14 |
| A4d | +6.0 [1.1, 14.0]; 178 / 0 | +15.1 [12.7, 17.2]; 485 / 36 | −27.8 [−45.2, −12.8]; 0 / 93 |
| A4e | 0 / 0 in every column | | |

Each agrees with the raw counts already printed in Table 4.26, e.g. A4d: 202 − 24 = 178 episodes = 6.0 pp of 2,979. The p-value added to A4d's attack cell (p < 0.001) comes from the stored exact McNemar test (1.75 × 10⁻⁴⁶).

## 2. Evidence limits (preserved, not softened)

- **Offline replay only (NO-ADAPT).** No live agent, no language model call, no deployment. The phrase "live result" is never applied to replay.
- **Development data.** The primary recordings were used to design REM. One confirmatory run was made on recordings unread at the time.
- **One benchmark** (AgentDojo banking v1). Nine attack clusters and sixteen task clusters; intervals described as descriptive.
- **Negative results kept:**
  - simple rules match REM;
  - Progent's policy outperforms REM offline;
  - behavioral evidence lowers task completion;
  - the learned decision causes most of the false blocking;
  - the rejected candidate admitted 132 against 11 attacks.
- **Design values** (costs, tiers, predicates, features, label rule) are declared, not approved.

## 3. Methodology accuracy

| Item | Status |
|---|---|
| Five-layer architecture | Unchanged |
| Implemented vs designed | Corrected in Section 3.5: the injection classifier is designed but not implemented (D-8). Elsewhere the implementation is described as built (Section 4.5.4, Table 4.24). |
| Ablation | Described as component-level everywhere:<br>• Mitigation removed whole;<br>• every Decision Engine component removed separately (A4a keeps D1/D2);<br>• Detection at indicator level;<br>• the two Behavioral Analysis groups removed separately;<br>• Input & Context only indirectly.<br>No passage claims a complete leave-one-layer-out design. |
| Comparisons | Each framework's kind of evidence is named:<br>• Progent: offline replay with its own code;<br>• DRIFT and MELON: architecture, code and scripted integration only;<br>• distributed defenses: recorded runs, descriptive.<br>Differences in conditions are stated in Section 4.4.8. |

## 4. Claims

**Claims the thesis does not make:**
- superiority over any framework;
- complete protection;
- real-world or institutional deployment;
- live evaluation;
- approval of the RQs or design values;
- defense or approval of the thesis (committee page corrected).

**One claim corrected in the previous audit, and checked again:** "661 of the 672 prevented attacks". It now reads "all 661 attacks that REM prevents (of 672 reached without defense)".

## 5. References and evidence sources

- No reference was invented or replaced.
- New entries (DRIFT, AgentDyn) were checked against Crossref, OpenAlex and the authors' repositories. Their full texts were not read; this is stated in the entries.
- All 106 entries are cited (105 before the addendum of 27 November), and every citation has an entry.
- See `UNRESOLVED_ISSUES_REPORT.md` for the entries that need manual checking.

## 6. Authorship and AI-tool references

- No research contribution was reattributed.
- Product names were removed from the front matter and Chapter 2. Factual statements that bear on validity are kept: the AI-assisted screening, the AI-only label inspection, and the AI-assisted fixture writing.
- The existing note on AI assistance is kept, without the product name, because removing it would conceal an existing disclosure. Whether the university requires a formal declaration is for the student and the university to confirm.
- No signature, declaration or institutional form was created or altered.
