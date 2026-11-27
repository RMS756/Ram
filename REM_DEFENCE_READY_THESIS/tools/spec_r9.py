"""Edits of the defence-ready edition (R9, 26 November 2026). Used by make_r9.py.

PRE_EDITS are written in R8 section numbering; POST_EDITS and AFTER_SWAP_EDITS in R9 numbering (after the section
remap, before the table/figure renumbering, so new tables are referred to by their placeholder numbers 4.N...).
An `old` of the form 'LINE:<prefix>' replaces the whole line that starts with <prefix>.
Every number written here was checked against REM_DEFENCE_READY_THESIS/audit/number_verification.json.
"""
C1, C2, C3, C4, C5, AP = ('CHAPTER_01_FINAL', 'CHAPTER_02_FINAL', 'CHAPTER_03_FINAL', 'CHAPTER_04_FINAL',
                          'CHAPTER_05_FINAL', 'APPENDICES_FINAL')

PRE_EDITS = [
    # an R8 reference range that pointed across sections (4.5.1–4.6.5); the observe-only analyses are these four
    (C4, 'Sections 4.6.2 and 4.5.1–4.6.5', 'Sections 4.6.2, 4.6.4, 4.6.5 and 4.5.1'),
    (C4, '(Sections 4.2.1 and 4.2.1)', '(Section 4.2.1)'),
    (C4, 'Section 4.5.5: A6 − A0, +22.19 ASR points', 'Section 4.5.5: variant A4a minus REM v1.0, +22.19 ASR points'),
]

POST_EDITS = [
    # ---------------------------------------------------------------- Chapter 4: introduction
    (C4, 'the experimental setup, the comparisons with baselines and with one published policy, the ablations, and the results with their discussion.',
     "the experimental setup, the comparison with existing security frameworks, the ablation study of REM's five layers, and the results with their discussion."),
    (C4, "Section 4.4 compares REM with baselines, simple rules, a published policy and the four defenses distributed with the benchmark, the last through their authors' recorded runs (Section 4.4.7). Section 4.5 reports the ablations, including the final pre-registered ablation of REM v1.0 of 19 November 2026 (Section 4.5.7) and a summary of the exploratory redesign studies of 18 and 19 November, which were not adopted (Section 4.5.8).",
     "Section 4.4 compares REM with existing security frameworks: Progent's published banking policy, decided by Progent's own code on the same recorded episodes; DRIFT and MELON, at the level of architecture and code; the four defenses distributed with the benchmark, through their authors' recorded runs; and the rule baselines. Section 4.5 reports the ablation study of REM's five layers: a layer-to-implementation mapping, the pre-registered ablations of 19 and 21 November 2026 with every variant compared with the full framework on the same episodes, and the ablations of exploratory extensions that are not part of REM v1.0."),
    # ---------------------------------------------------------------- 4.1.4 kinds of evidence
    (C4, 'Eight kinds of evidence are kept apart.', 'Ten kinds of evidence are kept apart.'),
    (C4, '| Call-level fixture | Hand-written paired calls scored by the frozen models | Prevalence; any benchmark outcome | Sections 4.6.7 and 4.6.9 |',
     '| Call-level fixture | Hand-written paired calls scored by the frozen models | Prevalence; any benchmark outcome | Sections 4.6.7 and 4.6.9 |\n'
     "| Replay with a published framework's own code | Recorded episodes replayed with every call decided by the official enforcement code of a published framework (Progent's checker) | Agent adaptation; the framework with generated or updated policies | Section 4.4.7 |\n"
     "| Scripted integration | A published framework's official code run end to end in the benchmark with a scripted agent that calls no model | Any security or utility performance; only compatibility and processing volume | Section 4.4.7 |"),
    (C4, 'Integration checks with scripted agents and simulated providers are not results and are reported only as status (Section S-4.4.4).',
     'Integration checks with scripted agents and simulated providers are not performance results and are reported only as status (Section S-4.4.4; for DRIFT and MELON, Section 4.4.7).'),
    (C4, 'a fresh run of the frozen pilot pipeline first reproduced the published counts of REM v1.0 exactly.',
     "a fresh run of the frozen pilot pipeline first reproduced the published counts of REM v1.0 exactly. The layer ablation of 21 November 2026 (Section 4.5.7) is in `REM_ABLATION_STUDY/results/`, and the comparison with Progent's own checker and the DRIFT integration of 22 November 2026 (Section 4.4.7) are in `REM_COMPARATIVE_EVALUATION_PHASE/results/`. Every number of Sections 4.4 and 4.5 that comes from these studies was recomputed for this edition from their stored per-episode records (`REM_DEFENCE_READY_THESIS/audit/`)."),
    # ---------------------------------------------------------------- 4.3.1 arms
    (C4, 'password change not permitted | none | 13 November |',
     "password change not permitted | none | 13 November |\n"
     "| Progent banking policy, official checker | The same policy, with every call decided by the enforcement code of the Progent repository at a pinned commit instead of this project's re-implementation (Section 4.4.7) | none | 22 November |"),
    (C4, 'a provenance rule (Section 4.5.8) | none (GV); their own | 16 November |',
     'a provenance rule (Section 4.5.8) | none (GV); their own | 16 November |\n'
     '| Ablation variants A1–A5 | REM v1.0 with one component of one layer removed or disabled (Section 4.5.5, Table 4.N8) | as REM v1.0; refitted when evidence is removed | 19 and 21 November |'),
    (C4, 'Published defenses that need a language model (MELON, Task Shield, CaMeL, Progent with generated policies) are not among the arms, because no model was available (Section S-4.4.4).',
     "Published defenses that need a language model (MELON, DRIFT, Task Shield, CaMeL, Progent with generated policies) are not among the arms, because no model was available (Section S-4.4.4). DRIFT's official code was executed with a scripted agent that calls no model, as an integration check only (Section 4.4.7)."),
    # ---------------------------------------------------------------- 4.3.4 comparisons fixed in advance
    (C4, 'Six sets of comparisons were fixed before their outcomes were computed', 'Nine sets of comparisons were fixed before their outcomes were computed'),
    (C4, 'with the rule that a learned method adds value only if it is not matched by GV (Section 4.5.8).',
     'with the rule that a learned method adds value only if it is not matched by GV (Section 4.5.8);\n'
     '- 19 November 2026: the final ablation of REM v1.0, eight ablation arms and the no-defense reference against the full framework (Section 4.5.7);\n'
     '- 21 November 2026: the layer ablation, including the Detection-layer, predicate and enforcement arms, on three populations (Section 4.5.7);\n'
     "- 22 November 2026: REM v1.0 against Progent's banking policy decided by Progent's own code, on three populations, and the scripted integration of DRIFT's official code (Section 4.4.7)."),
    # ---------------------------------------------------------------- 4.6.10 conclusions
    (C4, '| Different evidence kinds (closed loop against NO-ADAPT replay); descriptive; one model; benign utility on 15–16 runs |',
     '| Different evidence kinds (closed loop against NO-ADAPT replay); descriptive; one model; benign utility on 15–16 runs |\n'
     "| 14 | Of REM's five layers, the Decision Engine's learned decision acting through the Mitigation layer's enforcement carries every measured outcome effect; the action/provenance evidence carries the discrimination; behavioral evidence lowers task completion; the Detection layer's indicator, the predicates, calibration and Modify have no measurable effect | Section 4.5.7, Tables 4.N9–4.N12: A4a and A5 +22.2 ASR points; shadow mode computes the same verdict for 6,654 of 6,684 calls; without the action/provenance evidence 49 against 24 attacked episodes execute an attack call; A3a +10.5 benign points | Development data; replay; the Input & Context layer is not isolatable and the injection classifier is absent; no measurable effect is not evidence of no value |\n"
     "| 15 | Progent's published banking policy, decided by Progent's own code, has no successful attack and completes more tasks under attack than REM v1.0 on all three populations | Section 4.4.7, Tables 4.N4–4.N5: 0 against 11, 2 and 3 attacks (resolved on the primary population only); 7.2, 16.9 and 18.0 points more tasks under attack | Its list of recipients contains benchmark-specific values and excludes the attacker's account by construction; replay; not a configuration of the paper |"),
    (C4, 'The one published policy that was replayed has no successful attack and completes more tasks than either REM version. No defense that needs a language model was run.',
     "The one published policy that was replayed, now decided by Progent's own code, has no successful attack and completes more tasks than either REM version. No defense that needs a language model was run; DRIFT and MELON are compared at the level of architecture and code only (Section 4.4)."),
    (C4, 'because no attack reached it; that is not evidence of no value.',
     'because no attack reached it; that is not evidence of no value.\n'
     '- **That a component without a measurable effect in the ablation is unnecessary.** The Detection layer\'s indicator, the predicates, calibration and Modify changed no outcome on these recordings; that is a statement about this benchmark and this replay, not evidence that they are of no value (Section 4.5.10).'),
    # ---------------------------------------------------------------- 4.6.11 threats
    (C4, 'LINE:16. **One published policy was replayed, and no defense that needs a language model was run.**',
     "16. **One published policy was replayed, and no defense that needs a language model was run.** Since 22 November 2026 the published policy is decided by the enforcement code of the Progent repository at a pinned commit, which gives the same counts as the earlier re-implementation on every population (Section 4.4.7); the Progent framework was not run with generated or updated policies. DRIFT and MELON were examined at the level of their papers and code, and their official code was executed only with scripted agents, which yields no security or utility result (Section 4.4.7). No statement about the relative performance of REM and model-based defenses is supported."),
    (C4, '20. **Close work known from abstracts.** PACT, ROPE and CapLite (November 2026) are known from abstracts, ROPE also from its repository; none was run.',
     "20. **Close work known from abstracts.** PACT, ROPE and CapLite (November 2026) are known from abstracts, ROPE also from its repository; none was run.\n"
     "21. **Granularity of the layer ablation.** The Input & Context layer computes no evidence and could not be removed without fabricating the inputs of everything after it; it is assessed only through the action/provenance evidence. The Detection layer's classifier is absent, and its one indicator shares its pattern match with a behavioral feature. A component without a measurable effect in the ablation is not thereby shown to be unnecessary (Section 4.5.10).\n"
     "22. **Comparison with existing frameworks.** Progent's policy contains benchmark-specific recipients and excludes the attacker's account by construction; the comparison is a replay of one manual policy, not of the Progent system with generated policies. The DRIFT paper was not read in full; its code was. DRIFT's own results are on a different benchmark version (banking v1.2) and are not placed beside REM's (Section 4.4.8)."),
    # ---------------------------------------------------------------- 4.6.12 summary
    (C4, 'It is not a configuration evaluated in the current version of the paper.',
     "It is not a configuration evaluated in the current version of the paper. Decided by Progent's own enforcement code (22 November 2026), it gives the same counts on all three populations and completes 7.2, 16.9 and 18.0 percentage points more tasks under attack than REM v1.0; its list of permitted recipients contains values specific to the benchmark."),
    (C4, 'LINE:- **Final ablation (19 November 2026, pre-registered).**',
     "- **Ablation of the five layers (19 and 21 November 2026, pre-registered).** The learned decision of the Decision Engine accounts for all 661 attacks that REM v1.0 prevents (of 672 reached without defense) and admits none, at a cost of 22.5 points of benign utility, and only enforcement by the Mitigation layer turns its verdicts into outcomes: in shadow mode the same verdicts protect nothing. The action/provenance evidence carries the estimator's discrimination; without it 49 instead of 24 attacked episodes execute an attack call. Behavioral evidence lowers task completion with no security effect. The Detection layer's indicator, the predicates, calibration and Modify have no measurable effect, and the Input & Context layer cannot be removed on its own. The consequence-aware rule admits 153 fewer attacks than consequence-independent thresholds and completes fewer tasks.\n"
     "- **DRIFT and MELON.** Both need a language model in their decision path and are compared at the level of architecture and code. DRIFT's official code runs on the benchmark version used here; with a scripted agent it makes about three times as many model calls per episode as its own agent without its modules. No security or utility result was obtained for either."),
    (C4, 'any defense run with a language model in this project (the distributed defenses are compared through their authors\' recorded runs); MELON;',
     "any defense run with a language model in this project (the distributed defenses are compared through their authors' recorded runs); MELON and DRIFT with a model (both executed with scripted agents only);"),
    # R8 sentence made inaccurate by the scripted MELON pilot of 19 November (reported in Section 4.4.7)
    (C4, 'REM v1.0 was therefore not run in a closed loop, and MELON was not executed (Section S-4.4.4).',
     'REM v1.0 was therefore not run in a closed loop, and MELON was not executed with a language model; its official code ran only with a scripted agent (Sections S-4.4.4 and 4.4.7).'),
    # R8 wording that called the 672 no-defense attack outcomes "prevented": REM prevents 661 of them (672 - 11)
    (C4, '- carries 661 of the 672 prevented attacks.', '- accounts for all 661 attacks that REM v1.0 prevents (of 672 reached without defense).'),
    (C1, 'the learned decision prevents 661 of the 672 prevented attacks and admits none',
     'the learned decision accounts for all 661 attacks that REM v1.0 prevents (of 672 reached without defense) and admits none'),
    (C5, 'the learned decision prevents 661 of the 672 prevented attacks, admits none',
     'the learned decision accounts for all 661 prevented attacks (of 672 reached without defense), admits none'),
    (C5, 'prevents 661 of the 672 attacks it stops, with none admitted',
     'accounts for all 661 attacks that REM v1.0 stops (of 672 reached without defense), with none admitted'),
    # ---------------------------------------------------------------- final review (26 Nov 2026): figures 4.6-4.8 redrawn with Table 4.25 labels
    (C4, '![Figure 4.2. Final ablation of REM v1.0: attack success rate and benign utility per arm, with 95% grouped-bootstrap intervals and counts (replay, NO-ADAPT, primary population).](REM_FINAL_THESIS_COMPLETION_2026_11_19/figures/fig_ablation_security_utility.png)',
     '![Figure 4.2. Final ablation of REM v1.0 (19 November 2026): attack outcomes and benign tasks completed per variant, with 95% grouped-bootstrap intervals and counts (replay, NO-ADAPT, primary population; variant labels as in Table 4.N8).](REM_DEFENCE_READY_THESIS/figures/fig_19nov_security_utility.png)'),
    (C4, '![Figure 4.3. Paired differences of each arm from REM v1.0 (A0). Filled marks: the 95% interval excludes zero; open marks: it includes zero.](REM_FINAL_THESIS_COMPLETION_2026_11_19/figures/fig_ablation_paired_differences.png)',
     '![Figure 4.3. Paired differences of each variant from the full REM v1.0 (percentage points; variant labels as in Table 4.N8). Filled marks: the 95% interval excludes zero; open marks: it includes zero.](REM_DEFENCE_READY_THESIS/figures/fig_19nov_paired_differences.png)'),
    (C4, '](REM_FINAL_THESIS_COMPLETION_2026_11_19/figures/fig_ablation_reachability.png)', '](REM_DEFENCE_READY_THESIS/figures/fig_19nov_reachability.png)'),
    # ---------------------------------------------------------------- final review: tool-specific wording not needed for the method
    (C4, 'was prepared by another assistant in a separate checkout and delivered as a package.',
     'was prepared in a separate working copy of the repository and delivered as a package.'),
    (C2, 'the thesis author, assisted by an AI coding assistant (Claude Code), as recorded',
     'the thesis author, assisted by an AI coding assistant, as recorded'),
    # ---------------------------------------------------------------- final review: implementation status and readability
    (C3, '| [0, 1] | Derived (classifier choice pending supervisor approval) |',
     '| [0, 1] | Derived (classifier choice pending supervisor approval); **not implemented in REM v1.0** (decision D-8) |'),
    (C3, 'The classifier is used with fixed inference and is not retrained. A classifier distributed with an existing guardrail system, such as PromptGuard 2 in LlamaFirewall (Chennabasappa et al., 2025), is a candidate.',
     'In the design, the classifier is used with fixed inference and is not retrained; a classifier distributed with an existing guardrail system, such as PromptGuard 2 in LlamaFirewall (Chennabasappa et al., 2025), is a candidate. **No classifier was available for the implementation, so in REM v1.0 the Detection Layer consists of x^ctx^~2~ alone** (decision D-8; Chapter 4, Section 4.5.5).'),
    (C1, "Against the strongest simple rule it has fewer successful attacks, while the difference in completed tasks is not resolved; against a fixed-list policy from Progent's repository nothing is resolved; and the rule's authority guard used alone (GV), without any learned decision, gives the outcomes of every learned or statistically calibrated decision tested behind it, except a Neyman-Pearson threshold at 0.01, which loses tasks.",
     "Against the strongest simple rule it has fewer successful attacks, while the difference in completed tasks is not resolved; against a fixed-list policy from Progent's repository nothing is resolved. The rule's authority guard used alone (GV), without any learned decision, gives the outcomes of every learned or statistically calibrated decision tested behind it, except a Neyman-Pearson threshold at 0.01, which loses tasks."),
    (C1, "With protocols committed before scoring, the ablation shows where REM v1.0's protection comes from: the learned decision accounts for all 661 attacks that REM v1.0 prevents (of 672 reached without defense) and admits none, at a measurable cost in completed tasks, while calibration, context evidence, the predicates and Modify change no attack outcome and behavioral evidence lowers task completion.",
     "With protocols committed before scoring, the ablation shows where REM v1.0's protection comes from. The learned decision accounts for all 661 attacks that REM v1.0 prevents (of 672 reached without defense) and admits none, at a measurable cost in completed tasks. Calibration, context evidence, the predicates and Modify change no attack outcome, and behavioral evidence lowers task completion."),
    (C5, "Behind its authority guard, a learned model, calibrated thresholds and boosted trees gave exactly the outcomes of the guard used alone (GV), except one threshold that lost tasks, because every attack-labelled call was stopped before any of them was consulted; this is not evidence",
     "Behind its authority guard, a learned model, calibrated thresholds and boosted trees gave exactly the outcomes of the guard used alone (GV), except one threshold that lost tasks, because every attack-labelled call was stopped before any of them was consulted. This is not evidence"),
    # ---------------------------------------------------------------- Appendix B: decisions raised by the comparison and the ablation
    (AP, '| D-15 | Live closed-loop experiment and the comparisons that need a language model (MELON, Task Shield, Progent with generated policies, the semantic verifier):',
     '| D-15 | Live closed-loop experiment and the comparisons that need a language model (MELON, DRIFT, Task Shield, Progent with generated policies, the semantic verifier):'),
    (AP, '| D-12 | Thesis title |',
     '| SD-ABL | Whether the component-level ablation of Chapter 4, Section 4.5 answers the request for an ablation of the five layers (the Mitigation layer removed whole; every Decision Engine component; the implemented Detection and Behavioral Analysis evidence; the Input & Context layer only indirectly, because it computes no evidence) | Reported as a component-level ablation with its isolation limits stated | Accept, or specify a substitute input for an Input & Context ablation (a design decision) |\n'
     '| SD-CMP | Scope of the comparison with existing frameworks: Progent\'s published manual banking policy in offline replay; DRIFT and MELON at the level of architecture and code, with scripted integration tests only | Reported with the kind of evidence of each comparison stated (Chapter 4, Section 4.4) | Accept, or authorize live runs under D-15 |\n'
     '| D-12 | Thesis title |'),
    # ---------------------------------------------------------------- Chapter 5
    (C5, '| RQ4, component contribution | Action evidence carries the discrimination.',
     "| RQ4, component contribution | Across the five layers, every measured outcome effect comes from the Decision Engine's learned decision acting through the Mitigation layer's enforcement: in shadow mode the same verdicts protect nothing. The Input & Context layer could not be ablated on its own. Action evidence carries the discrimination."),
    (C5, 'final pre-registered ablation with paired intervals (Chapter 4, Section 4.5.7)',
     'pre-registered ablations of the five layers with paired intervals on three populations (Chapter 4, Section 4.5.7)'),
    (C5, '| The value of the injection classifier, which was not available; behavior of these components in other environments |',
     '| The value of the injection classifier, which was not available; behavior of these components in other environments; that a component without a measurable effect is unnecessary |'),
    (C5, "| Controlled comparison with a threshold baseline and three rule baselines on the same episodes; replay of one published policy (a manual banking policy from Progent's repository; not a configuration of the current paper) in the same harness; design-level comparison with the closest published systems |",
     "| Controlled comparison with a threshold baseline and three rule baselines on the same episodes; Progent's published banking policy (not a configuration of the current paper) replayed in the same harness and decided by Progent's own code on three populations; a fifteen-dimension architectural comparison with Progent, DRIFT and MELON; execution of DRIFT's official code with a scripted agent as an integration check (Chapter 4, Section 4.4) |"),
    (C5, '| A closed-loop comparison:', '| DRIFT and MELON were not run with a language model. A closed-loop comparison:'),
    (C5, 'and descriptively for the four defenses distributed with the benchmark.',
     'and descriptively for the four defenses distributed with the benchmark. For DRIFT and MELON it is achieved at the level of architecture and code only.'),
    (C5, 'LINE:10. **Limited external comparison.**',
     "10. **Limited external comparison.** One published deterministic policy was replayed on the recorded episodes, decided by its authors' own code; its list of recipients is informed by the benchmark. The four distributed defenses are compared through their authors' recorded runs with one model, against REM's replay, which is descriptive. DRIFT and MELON, which need a language model, were compared at the level of architecture and code and executed only with scripted agents. REM was not run in a closed loop, and the tool_filter traces could not be replayed with the frozen harness."),
    (C5, "11. **Fixtures and rules were written with knowledge of the benchmark and of REM's features.**",
     "11. **Fixtures and rules were written with knowledge of the benchmark and of REM's features.**\n"
     "12. **Granularity of the layer ablation.** The Input & Context layer could not be removed on its own, and the Detection layer's classifier is absent. A component without a measurable effect here is not shown to be unnecessary."),
    (C5, "The MELON integration is ready and needs a model credential, MELON's embedding service and an approved spending limit; Progent with generated policies and Task Shield need a model as well.",
     "The MELON integration is ready and needs a model credential, MELON's embedding service and an approved spending limit. DRIFT's official code already runs on the benchmark version used here with a scripted agent; a live run needs a model credential, an approved budget and a decision on the benchmark version, because DRIFT's defaults and its authors' runs use banking v1.2. Progent with generated policies and Task Shield need a model as well."),
    (C5, "A final ablation, pre-registered on the last day of the work, settles where REM v1.0's own protection comes from.",
     "Two pre-registered ablations settle where REM v1.0's own protection comes from."),
    (C5, 'and calibration, Modify, the predicates and context evidence change no attack outcome.',
     "and calibration, Modify, the predicates and context evidence change no attack outcome. Across the five layers, every measured outcome effect comes from that decision acting through enforcement: in shadow mode the same verdicts protect nothing, and the Input & Context layer's labels matter through the action/provenance evidence built on them."),
    (C5, 'this places REM among them without ranking it.',
     "this places REM among them without ranking it. Progent's published banking policy, decided by Progent's own code on the same recorded episodes, admits no attack and completes more tasks under attack than REM on all three populations; its list of permitted recipients is informed by the benchmark, so this, too, is not a ranking."),
    # ---------------------------------------------------------------- Chapter 1
    (C1, '8. **A pre-registered final ablation and an external comparison (19 November 2026).**',
     '8. **Pre-registered ablations of the five layers and a comparison with existing frameworks (19 to 22 November 2026).**'),
    (C1, 'the comparison is descriptive (Chapter 4, Sections 4.4.7 and 4.5.7).',
     "the comparison is descriptive. A component-level ablation of the five layers on three populations shows that every outcome effect comes from the learned decision acting through enforcement, and that the Input & Context layer cannot be removed on its own. Progent's published banking policy, decided by its authors' code on the same episodes, admits no attack and completes more tasks than REM; DRIFT and MELON are compared at the level of architecture and code (Chapter 4, Sections 4.4 and 4.5)."),
    (C1, 'MELON was not run; the one published policy that was replayed has no successful attack and completes more tasks than REM (Chapter 4, Section 4.4.7).',
     "MELON and DRIFT were not run with a language model (their official code was executed only with scripted agents); the one published policy that was replayed, decided by its authors' own code, has no successful attack and completes more tasks than REM (Chapter 4, Section 4.4.7)."),
    (C1, '- results under supervisor-approved design values, or with human-audited labels;',
     '- results under supervisor-approved design values, or with human-audited labels;\n'
     '- that a component without a measurable effect in the ablation is unnecessary (Chapter 4, Section 4.5.10);'),
    (C1, 'comparisons with existing models and defense frameworks; ablation studies; and results and discussion. It states that no live-agent experiment was executed and that the one published policy evaluated was replayed on recorded episodes.',
     "comparison with existing security frameworks (Progent, DRIFT, MELON and the defenses distributed with the benchmark); an ablation study of REM's five layers; and results and discussion. It states that no live-agent experiment was executed, that the one published policy evaluated was replayed on recorded episodes, and that DRIFT and MELON were compared at the level of architecture and code."),
    # ---------------------------------------------------------------- Chapter 2
    (C2, 'ToolSafe, DRIFT and FinHarness', 'ToolSafe, DRIFT (H. Li et al., 2025) and FinHarness'),
]

# Contribution rows of Table 5.3 were printed in the order 1-7, 9, 8; restore 8 before 9.
SWAP_LINES = [(C5, '| 9. A pre-registered final ablation', '| 8. An exploratory extension')]
ROW10 = ("| 10. A layer-to-implementation mapping and a component-level ablation of the five-layer design, and a comparison with existing security frameworks (21 and 22 November 2026) "
         "| Component ablation as in the Progent paper (T. Shi et al., 2026); Progent (T. Shi et al., 2026), DRIFT (H. Li et al., 2025) and MELON (Zhu, Yang, et al., 2025) "
         "| `experiments/ablation_study/`, `experiments/comparative_phase/` "
         "| Replay of three populations (3,313, 681 and 2,113 episodes) in nine arms; Progent's policy decided by its own code on the same episodes; DRIFT's official code with a scripted agent "
         "| Every outcome effect from the learned decision acting through enforcement (shadow mode equals no defense); without the action/provenance evidence, 49 against 24 attacked episodes with an attack call executed; Detection indicator and predicates: no outcome changed. Progent's policy: 0 against 11, 2 and 3 successful attacks and 7.2 to 18.0 points more tasks completed under attack "
         "| Development data; NO-ADAPT; Input & Context layer not isolatable; the policy's list is informed by the benchmark; DRIFT and MELON not run with a model |")
# The row is inserted after row 9 (which, after the swap, is the last row of Table 5.3).
AFTER_SWAP_EDITS = [(C5, '\n\n## 5.5 What Was Not Confirmed', '\n' + ROW10 + '\n\n## 5.5 What Was Not Confirmed')]

FRONT_EDITS = [
    ('front_matter.md', 'This thesis, *Runtime Evaluation and Mitigation (REM): A Security Framework for Financial AI Agents*, was successfully defended and approved on **[date to be completed by the university]**.',
     '**This thesis has not yet been defended.** The decision of the examination committee on the thesis *Runtime Evaluation and Mitigation (REM): A Security Framework for Financial AI Agents*, the date of the defense and the signatures are to be completed by the university after the defense.'),
    ('front_matter.md', 'An AI coding assistant (Claude Code) was used in this project,', 'An AI coding assistant was used in this project,'),
    ('front_matter.md', 'The Arabic abstract is a draft translation of the English abstract prepared with AI assistance; its wording and the Arabic spelling of the names require the student\'s review.',
     'The Arabic abstract is a draft translation of the English abstract; its wording and the Arabic spelling of the names require review by a native speaker.'),
    ('abstract_en.md', 'that the learned decision prevents 661 of the 672 attacks that REM stops and admits none',
     'that the learned decision accounts for all 661 attacks that REM stops (672 succeed without any defense) and admits none'),
    ('abstract_ar.md', 'أن القرار المتعلَّم يمنع 661 من أصل 672 هجوماً يوقفها الإطار ولا يسمح بأي هجوم إضافي',
     'أن القرار المتعلَّم مسؤول عن منع جميع الهجمات الـ661 التي يوقفها الإطار (من أصل 672 هجوماً تنجح دون أي دفاع)، ولا يسمح بأي هجوم إضافي'),
    ('front_matter.md', 'LINE:This document is a **draft for supervisor review** dated 19 November 2026',
     "This document is the **draft for supervisor review** dated 26 November 2026 (ninth edition, revised after a final academic review: the eighth edition of 19 November 2026 with a comparison with existing security frameworks and an ablation study of REM's five layers at component level, both requested by the supervisors; the earlier editions are preserved unchanged). It is prepared for discussion. It has not been formally approved, and no approval is implied."),
    ('front_matter.md', 'LINE:- **New in this edition.**',
     "- **New in this edition.** Section 4.4 is rewritten as a comparison with existing security frameworks: selection criteria, a fifteen-dimension architectural comparison, Progent's published banking policy decided by Progent's own code on three populations, and DRIFT and MELON at the level of architecture and code (DRIFT's official code executed with a scripted agent only). Section 4.5 is rewritten as an ablation study of the five layers, with a layer-to-implementation mapping, every variant compared with the full framework on the same episodes, and a statement of which layers could be isolated (only the Mitigation layer as a whole; the Input & Context layer only indirectly). All numbers of both sections were recomputed from the stored per-episode records. The units of the earlier Sections 4.4 and 4.5 are kept inside the new sections. Tables and figures of Chapter 4 are numbered sequentially; the correspondence with the eighth edition's numbers is listed in `REM_DEFENCE_READY_THESIS/THESIS_REVISION_LOG.md`, and the supplement's numbers are those of the fifth edition, as before. "
     "**New in the eighth edition.** A final ablation of REM v1.0 under a protocol committed before scoring (now in Section 4.5.7); a comparison with the four distributed defenses through their authors' recorded runs and REM's replay on the same task pairs (now in Section 4.4.7); and a summary of the exploratory redesign studies of 18 and 19 November 2026, which were not adopted (now in Section 4.5.8). "
     "**New in the seventh edition.** The second version of the amount verifier after an independent review (defects D3 and D4; corrected statement of the stage order) and a condensed Section 2.8.3. **New in the sixth edition.** The repair study of 17 November 2026 (typed verification of request-derived amounts, now in Section 4.5.8), corrections of statements about the guard and the learned decision, three close works of November 2026, and corrected references (NEXUS, MELON, PRISMA 2020, PRISMA-S)."),
    ('abstract_en.md', 'and that calibration and Modify change no attack outcome.',
     "and that calibration and Modify change no attack outcome. An ablation of the components of the five layers was then run on three populations. It removed the whole Mitigation layer, every Decision Engine component and the implemented Detection and Behavioral Analysis evidence; the Input & Context layer, which computes no evidence of its own, could be assessed only indirectly. Every outcome effect came from the learned decision acting through enforcement: in shadow mode the same verdicts protected nothing. Removing the action/provenance evidence let more attack calls execute, while the Detection layer's instruction-pattern indicator and the policy predicates had no measurable effect."),
    ('abstract_en.md', "because the defenses' runs are closed-loop and REM's is a replay.",
     "because the defenses' runs are closed-loop and REM's is a replay. Progent's published banking policy, decided by Progent's own enforcement code on the same recorded episodes, admitted no attack and completed more tasks under attack than REM on all three populations; its list of permitted recipients contains values specific to the benchmark. DRIFT and MELON, which need a language model, were compared at the level of architecture and code only."),
    ('abstract_en.md', 'a closed-loop harness and an integration with the MELON defense are implemented and were not executed with a language model.',
     'a closed-loop harness and integrations with the MELON and DRIFT defenses are implemented and were not executed with a language model.'),
    ('abstract_ar.md', 'وقد نُفّذ إطار اختبار حلقي مغلق وتكامل مع دفاع MELON دون تشغيلهما مع نموذج لغوي.',
     'وقد نُفّذ إطار اختبار حلقي مغلق وتكاملان مع دفاعَي MELON وDRIFT دون تشغيلها مع نموذج لغوي.'),
    ('abstract_ar.md', 'لأن تشغيلات الدفاعات حلقية مغلقة بينما نتائج الإطار مستمدة من إعادة التشغيل.',
     'لأن تشغيلات الدفاعات حلقية مغلقة بينما نتائج الإطار مستمدة من إعادة التشغيل.\n\n'
     'وأظهرت دراسة استئصال لمكوّنات الطبقات الخمس، أُجريت على ثلاث مجموعات من الحلقات (أُزيلت فيها طبقة التخفيف كاملة، وكل مكوّن من مكوّنات محرك القرار على حدة، بينما قُيّمت طبقة المدخلات والسياق بصورة غير مباشرة فقط)، أن كل أثر مقيس في النتائج يأتي من القرار المتعلَّم وهو يعمل من خلال التنفيذ في طبقة التخفيف: ففي وضع المراقبة دون تنفيذ لم تحمِ الأحكام نفسها شيئاً، وأدّت إزالة أدلة الفعل ومصدر المعطيات إلى تنفيذ مزيد من استدعاءات الهجوم، ولم يكن لمؤشر أنماط التعليمات في طبقة الكشف ولا لشروط السياسة أثر قابل للقياس، ولم يمكن استئصال طبقة المدخلات والسياق وحدها. أما سياسة Progent المصرفية المنشورة، وقد طُبّقت بشيفرة التنفيذ الأصلية لمؤلفيها على الحلقات المسجّلة نفسها، فلم تسمح بأي هجوم، وأنجزت مهاماً تحت الهجوم أكثر من الإطار في المجموعات الثلاث، مع أن قائمة المستفيدين المسموح بهم فيها تتضمن قيماً خاصة بالمعيار. وقورن الإطار بدفاعَي DRIFT وMELON، اللذين يحتاجان إلى نموذج لغوي، على مستوى البنية والشيفرة فقط.'),
]

REF_ADD = [
    ('Li, F. (2026). *OpenClaw PRISM',
     'Li, H., Liu, X., Chiu, H.-C., Li, D., Zhang, N., & Xiao, C. (2025). DRIFT: Dynamic rule-based defense with injection isolation for securing LLM agents. In *Advances in Neural Information Processing Systems 38* (NeurIPS 2025) (pp. 92825–92853). https://doi.org/10.52202/085713-2791 [DOI, title, venue and pages verified with Crossref and OpenAlex (W4415110937) on 26 November 2026; author names as in the official repository, where Crossref registers the third author as "CHIU Chun"; abstract read; full text not read; the official code, SaFo-Lab/DRIFT at commit 6fd3df4, was read and executed with a scripted agent]'),
    ('Li, H., Liu, X., Chiu, H.-C.',
     'Li, H., Wen, R., Shi, S., Zhang, N., Vorobeychik, Y., & Xiao, C. (2026). *AgentDyn: Are your agent security defenses deployable in real-world dynamic environments?* (arXiv:2602.03117) [Preprint]. arXiv. https://arxiv.org/abs/2602.03117 [Title, year, arXiv identifier and first three authors verified through OpenAlex (W7127632747), which lists six authors; the full author list as in the repository of its authors (SaFo-Lab/AgentDyn); abstract read; full text not read]'),
]

# Table 5.3 had six columns and set most of its words one or two letters per line; it is printed with three, by joining
# columns without changing any cell text.
MERGE_TABLES = [
    (C5, '**Table 5.3.', [[0], [1, 2, 3], [4, 5]],
     ['Contribution', 'Precedent, implementation and supporting experiment', 'Measured result, scope and limits'],
     ['{0}', '*Precedent:* {0}. *Implemented in:* {1}. *Experiment:* {2}', '{0}. *Scope and limits:* {1}']),
]

# Exact replacements inside existing reference entries (R8 text that later work made inaccurate).
REF_EDITS = [
    ('Official code repository read, not executed (github.com/sunblaze-ucb/progent, commits 9befb41, 8a8eb89 and 0d7ea07); the manual banking policy of commit 9befb41 is used in Chapter 4]',
     'Official code repository read (github.com/sunblaze-ucb/progent, commits 9befb41, 8a8eb89 and 0d7ea07); the manual banking policy of commit 9befb41 is used in Chapter 4, and since 22 November 2026 it is decided by the enforcement code of the repository at commit 3e79753, executed as a decision rule in offline replay (the Progent framework with generated policies was not run)]'),
]
