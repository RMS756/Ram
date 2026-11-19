"""Specification of the eighth edition (R8, 19 November 2026). Applied by make_r8.py to the assembled R7.

Every change is dated and traceable to REM_FINAL_THESIS_COMPLETION_2026_11_19/ (protocols 02, 05, 05a; results; analyses
04, 07, 09). Numbers in new text are copied from the generated tables results/tables_ablation.md and tables_external.md.
"""

C1, C3, C4, C5 = 'CHAPTER_01_FINAL', 'CHAPTER_03_FINAL', 'CHAPTER_04_FINAL', 'CHAPTER_05_FINAL'
APP = 'APPENDICES_FINAL'

# (file, heading prefix of the unit to replace, fragment in text_r8/)
REPLACE_UNIT = [
    (C4, '### 4.4.2 ', 'ch4_442.md'),
]

# (file, anchor heading, fragments inserted before it)
INSERT_BEFORE = [
    (C4, '## 4.6 Results and Discussion', ['ch4_455.md', 'ch4_456.md']),
]

EDITS = [
    # ---------------------------------------------------------------- Chapter 4: introduction and evidence kinds
    (C4, 'Section 4.4 compares REM with baselines, simple rules and a published policy. Section 4.5 reports the ablations.',
     'Section 4.4 compares REM with baselines, simple rules, a published policy and the four defenses distributed with the '
     'benchmark, the last through their authors\' recorded runs (Section 4.4.2). Section 4.5 reports the ablations, including '
     'the final pre-registered ablation of REM v1.0 of 19 November 2026 (Section 4.5.5) and a summary of the exploratory '
     'redesign studies of 18 and 19 November, which were not adopted (Section 4.5.6).'),
    (C4, '| Sections 4.6.3, 4.4.1, 4.6.6 and 4.6.7 |', '| Sections 4.6.3, 4.4.1, 4.4.2, 4.5.5, 4.6.6 and 4.6.7 |'),
    (C4, 'Every run used AgentDojo 0.1.35, the benchmark\'s recordings at one fixed commit, seed 20261027 and step-level '
         'mitigation without a reviewer unless a table says otherwise.',
     'The final ablation and the comparison with the distributed defenses of 19 November 2026 (Sections 4.4.2 and 4.5.5) are '
     'in `REM_FINAL_THESIS_COMPLETION_2026_11_19/results/`; their protocols and code hashes were committed before any arm '
     'was scored, and a fresh run of the frozen pilot pipeline first reproduced the published counts of REM v1.0 exactly. '
     'Every run used AgentDojo 0.1.35, the benchmark\'s recordings at one fixed commit, seed 20261027 and step-level '
     'mitigation without a reviewer unless a table says otherwise.'),
    (C4, 'This section reports what happens when a component is removed or replaced. It covers the components of REM v1.0, '
         'the verdict set, and the components of the exploratory extension.',
     'This section reports what happens when a component is removed or replaced. It covers the components of REM v1.0, '
     'the verdict set, and the components of the exploratory extension. Section 4.5.5 repeats the ablation of REM v1.0 '
     'under a protocol committed before scoring, with paired intervals, two further arms (without Modify and without the '
     'learned decision) and a call-level analysis of where the learned decision acts.'),
    # Table of conclusions: two rows added
    (C4, '|\n\n#### The limiting factor is what the evidence represents',
     '|\n| 12 | In REM v1.0 the learned decision carries the protection: without it no attack is prevented by the predicates, '
     'and with it 661 of the 672 attacks are prevented and none admitted | Section 4.5.5: A6 − A0, +22.19 ASR points '
     '[14.55, 28.86]; 2,129 releases changed by the learned decision | It also withholds 81.5% of legitimate state-changing '
     'calls in benign episodes; development data; replay |\n'
     '| 13 | On the same task pairs, REM v1.0\'s replayed decisions leave fewer successful attacks than the recorded runs of '
     'three distributed defenses and about as many as the injection classifier, with lower benign completion | Section 4.4.2, '
     'Tables 4.N1–4.N3 | Different evidence kinds (closed loop against NO-ADAPT replay); descriptive; one model; '
     'benign utility on 15–16 runs |\n\n#### The limiting factor is what the evidence represents'),
    (C4, '- **Limit.** The provenance features of REM do not represent what the user asked for;',
     '- **Final ablation (19 November 2026, pre-registered).** The learned decision prevents 661 of the 672 attacks that '
     'REM v1.0 prevents and admits none, at a cost of 22.5 points of benign utility; calibration and Modify change no attack '
     'outcome; behavioral evidence lowers task completion with no security effect; the consequence-aware rule admits 153 '
     'fewer attacks than consequence-independent thresholds and completes fewer tasks.\n'
     '- **Distributed defenses.** On the same task pairs REM v1.0\'s replayed decisions leave fewer successful attacks than '
     'the recorded runs of repeat_user_prompt, spotlighting_with_delimiting and tool_filter and about as many as '
     'transformers_pi_detector, with lower benign completion; the comparison is descriptive because the defenses\' runs are '
     'closed-loop and REM\'s is a replay. Added to a defense\'s own traces, REM removes almost every remaining success.\n'
     '- **Limit.** The provenance features of REM do not represent what the user asked for;'),
    (C4, '- **Not done.** Live-agent runs; any defense that needs a language model;',
     '- **Not done.** Live-agent runs; any defense run with a language model in this project (the distributed defenses are '
     'compared through their authors\' recorded runs); MELON;'),
    # ---------------------------------------------------------------- Chapter 3: arms of the final ablation
    (C3, '7. Observe-only (no mitigation).\n',
     '7. Observe-only (no mitigation).\n\n'
     '**Final ablation (added 19 November 2026).** A separately pre-registered study (Chapter 4, Section 4.5.5) repeats '
     'ablations 1–4 and 6 in replay with paired intervals and adds two arms, each changing only the decision: Modify removed '
     'from the verdict set, so that the expected loss is minimized over Allow, Escalate and Block; and the learned decision '
     'removed, so that only the predicates D1 and D2 act and every other call is allowed. The consequence-independent '
     'baseline B1 serves as the arm with the expected-loss decision replaced by thresholds. Linear SHAP attribution is not '
     'ablated, because it cannot change a verdict.\n'),
    (C3, '- **Distributed defenses (pending supervisor approval).** Any defenses distributed with the pinned benchmark version, to address O3.',
     '- **Distributed defenses (pending supervisor approval).** Any defenses distributed with the pinned benchmark version, '
     'to address O3. They were compared on 19 November 2026 through the benchmark authors\' recorded closed-loop runs and a '
     'replay of REM on the same traces (Chapter 4, Section 4.4.2); none was run with a language model in this project.'),
    # ---------------------------------------------------------------- Chapter 1: contributions
    (C1, '(Chapter 4, Sections 4.4.3, 4.5.3, 4.5.4 and 4.6.9).\n',
     '(Chapter 4, Sections 4.4.3, 4.5.3, 4.5.4 and 4.6.9).\n'
     '8. **A pre-registered final ablation and an external comparison (19 November 2026).** With protocols committed before '
     'scoring, the ablation shows where REM v1.0\'s protection comes from: the learned decision prevents 661 of the 672 '
     'prevented attacks and admits none, at a measurable cost in completed tasks, while calibration, context evidence, the '
     'predicates and Modify change no attack outcome and behavioral evidence lowers task completion. The four defenses '
     'distributed with the benchmark are compared through their authors\' recorded runs and REM\'s replay on the same task '
     'pairs; the comparison is descriptive (Chapter 4, Sections 4.4.2 and 4.5.5).\n'),
    (C1, '- any comparison with a published defense that needs a language model; the one published policy that was replayed '
         'has no successful attack and completes more tasks than REM (Chapter 4, Section 4.4.3).',
     '- any closed-loop comparison with a published defense: the four distributed defenses are compared through their '
     'authors\' recorded runs against REM\'s replay, which is descriptive (Chapter 4, Section 4.4.2); MELON was not run; the '
     'one published policy that was replayed has no successful attack and completes more tasks than REM (Chapter 4, '
     'Section 4.4.3).'),
    # ---------------------------------------------------------------- Chapter 5
    (C5, '| Ablations (Chapter 4, Sections 4.5.1, 4.5.2 and 4.5.3, Table 4.17); confirmatory replay (Chapter 4, Section 4.6.8) |',
     '| Ablations (Chapter 4, Sections 4.5.1, 4.5.2 and 4.5.3, Table 4.17); confirmatory replay (Chapter 4, Section 4.6.8); '
     'final pre-registered ablation with paired intervals (Chapter 4, Section 4.5.5): the learned decision prevents 661 of '
     'the 672 prevented attacks, admits none and costs 22.5 points of benign utility; Modify can be removed without '
     'changing any episode |'),
    (C5, '| Experimental comparison with any published defense that needs a language model. The MELON integration is implemented and unevaluated |',
     '| A closed-loop comparison: the four distributed defenses were compared through their authors\' recorded runs against '
     'REM\'s replay on the same task pairs, which is descriptive (Chapter 4, Section 4.4.2). The MELON integration is '
     'implemented and unevaluated |'),
    (C5, 'O3 is achieved for internal baselines and for one published deterministic policy in replay.',
     'O3 is achieved for internal baselines and for one published deterministic policy in replay, and descriptively for '
     'the four defenses distributed with the benchmark.'),
    (C5, '| 8. An exploratory extension and an attribution result:',
     '| 9. A pre-registered final ablation of REM v1.0 with a decision-reachability analysis, and a comparison with the '
     'four distributed defenses (19 November 2026) | Component ablation, as in the Progent paper (T. Shi et al., 2026); '
     'defenses distributed with AgentDojo (Debenedetti et al., 2024) | `experiments/final_thesis/` | Replay of 3,313 episodes in ten arms; '
     'recorded runs of four defenses and REM\'s replay on their traces | Learned decision: +22.19 ASR points without it '
     '[14.55, 28.86], 661 attacks prevented, 0 admitted, 599 tasks lost; calibration, context, predicates and Modify: no '
     'attack outcome changed; thresholds instead of expected loss: 153 more attacks, 552 more tasks. Against the defenses: '
     'fewer successful attacks than three, about as many as the injection classifier, lower benign completion | Development '
     'data; NO-ADAPT; cross-kind comparison descriptive; tool_filter traces not replayable; MELON not run |\n'
     '| 8. An exploratory extension and an attribution result:'),
    (C5, '10. **Limited external comparison.** One published deterministic policy was replayed on the recorded episodes. No defense that needs a language model was run.',
     '10. **Limited external comparison.** One published deterministic policy was replayed on the recorded episodes. The '
     'four distributed defenses are compared through their authors\' recorded runs with one model, against REM\'s replay, '
     'which is descriptive; REM was not run in a closed loop, MELON was not run, and the tool_filter traces could not be '
     'replayed with the frozen harness.'),
    (C5, 'These findings come from recorded traces and from a replay that assumes the agent does not adapt.',
     'A final ablation, pre-registered on the last day of the work, settles where REM v1.0\'s own protection comes from. '
     'The learned, consequence-aware decision is not idle in REM v1.0: it decides almost every call and prevents 661 of the '
     '672 attacks it stops, with none admitted. It does so by withholding broadly, and calibration, Modify, the predicates '
     'and context evidence change no attack outcome. Against the four defenses distributed with the benchmark, REM\'s replayed '
     'decisions leave fewer successful attacks than three of them and about as many as an injection classifier, at a lower '
     'completion of benign tasks; because their runs are closed-loop and REM\'s is a replay, this places REM among them '
     'without ranking it.\n\n'
     'These findings come from recorded traces and from a replay that assumes the agent does not adapt.'),
    # ---------------------------------------------------------------- Appendix B: one new decision
    (APP, '| D-10 | Wording of the research questions | Marked proposed | Confirm |',
     '| D-10 | Wording of the research questions | Marked proposed | Confirm |\n'
     '| SD-ARCH | Whether an authorization-first deterministic design (REM-B family, Chapter 4, Section 4.5.6) should replace '
     'or extend the approved REM v1.0 | Reported as exploratory and NO-GO under its own pre-registered rules; REM v1.0 '
     'unchanged | Keep REM v1.0 as the thesis design; or authorize a new, independently validated study |'),
]

FRONT_EDITS = [
    ('abstract_en.md', 'and Modify, Escalate and Block had identical effect.',
     'and Modify, Escalate and Block had identical effect. A final ablation committed before scoring confirmed, with paired '
     'intervals, that the learned decision prevents 661 of the 672 attacks that REM stops and admits none, at a cost of 22.5 '
     'percentage points of benign task completion, and that calibration and Modify change no attack outcome. On the same '
     'task pairs, REM\'s replayed decisions left fewer successful attacks than the recorded runs of three of the four '
     'defenses distributed with the benchmark and about as many as its injection classifier, with lower benign task '
     'completion; this comparison is descriptive, because the defenses\' runs are closed-loop and REM\'s is a replay.'),
    ('abstract_ar.md', 'النتائج استكشافية ومستمدة من إعادة التشغيل',
     'وأكّدت دراسة استئصال نهائية ثُبّت بروتوكولها قبل القياس، بفترات ثقة مزدوجة، أن القرار المتعلَّم يمنع 661 من أصل 672 '
     'هجوماً يوقفها الإطار ولا يسمح بأي هجوم إضافي، على حساب 22.5 نقطة مئوية من إنجاز المهام السليمة، وأن المعايرة وحكم '
     'التعديل لا يغيّران نتيجة أي هجوم. وعلى أزواج المهام نفسها، ترك الإطار في إعادة التشغيل هجمات ناجحة أقل من التشغيلات '
     'المسجّلة لثلاثة من الدفاعات الأربعة الموزّعة مع المعيار، ونحو العدد نفسه الذي تركه مصنِّف الحقن، مع إنجاز أقل للمهام '
     'السليمة؛ وهذه المقارنة وصفية لأن تشغيلات الدفاعات حلقية مغلقة بينما نتائج الإطار مستمدة من إعادة التشغيل.\n\n'
     'النتائج استكشافية ومستمدة من إعادة التشغيل'),
    ('front_matter.md', 'dated 17 November 2026 (seventh edition: the condensed editorial edition of the same date (sixth edition) '
                        'updated with the second version of the amount verifier; the fifth and sixth editions are preserved unchanged)',
     'dated 19 November 2026 (eighth edition: the seventh edition of 17 November 2026 with a final pre-registered ablation of '
     'REM v1.0 and a comparison with the defenses distributed with the benchmark; the fifth to seventh editions are preserved '
     'unchanged)'),
    ('front_matter.md', '- **New in this edition.** The second version of the amount verifier',
     '- **New in this edition.** A final ablation of REM v1.0 under a protocol committed before scoring (Chapter 4, Section '
     '4.5.5); a comparison with the four distributed defenses through their authors\' recorded runs and REM\'s replay on the '
     'same task pairs (Section 4.4.2); and a summary of the exploratory redesign studies of 18 and 19 November 2026, which '
     'were not adopted (Section 4.5.6). Existing table numbers are unchanged, because the supplement cites them; new tables '
     'carry lettered numbers (Tables 4.11a–4.11c and 4.21a–4.21e), and the figures of Chapter 4 are renumbered. '
     '**New in the seventh edition.** The second version of the amount verifier'),
]

