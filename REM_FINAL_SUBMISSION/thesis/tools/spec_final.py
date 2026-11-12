"""Selection spec for make_final.py. Numbers are those of the base five-chapter draft; new text uses x.41+."""


def K(num, **kw):
    d = {'num': num}
    d.update(kw)
    return d


def N(frag):
    return {'new': frag}


CHAPTERS = {
    1: [
        K('1.1'),
        K('1.2', drop={'1.2': [4, 5, 6]}, add={'1.2': 'ch1_problem_tail'}),
        K('1.3'),
        N('ch1_gap'),
        K('1.5'), K('1.6'),
        K('1.7', add={'1.7': 'ch1_rq_note'}),
        K('1.8', add={'1.8': 'ch1_approach_v11'}),
        N('ch1_methodology'),
        K('1.10'),
        N('ch1_contrib'),
        N('ch1_org'),
    ],
    2: [
        K('2.1', drop={'2.1': [7, 8]}, add={'2.1': 'ch2_structure'}),
        K('2.2', omit=['2.2.4', '2.2.6', '2.2.7', '2.2.8'], drop={'2.2.3': [4], '2.2.5': [6, 7, 8, 9]},
          add={'2.2.3': 'ch2_bridge_eligibility'}, after={'2.2.8': 'ch2_bridge_appraisal'}),
        K('2.4', omit=['2.4.2', '2.4.3', '2.4.4'], drop={'2.4.1': [0], '2.4.5': [1, 2, 3, 4]},
          add={'2.4': 'ch2_bridge_agent_risk'}),
        K('2.5', drop={'2.5': [2, 5, 12, 13]}),
        K('2.6', omit=['2.6.1', '2.6.2', '2.6.4'], drop={'2.6': [3], '2.6.5': [3, 4]}, add={'2.6': 'ch2_bridge_defenses'},
          after={'2.6.4': 'ch2_bridge_guardrails'}),
        K('2.7', omit=['2.7.1', '2.7.4'], add={'2.7': 'ch2_bridge_monitors'}),
        K('2.8', omit=['2.8.1', '2.8.3', '2.8.5'], add={'2.8': 'ch2_bridge_foundations'}, after={'2.8.5': 'ch2_bridge_attribution'}),
        K('2.9', drop={'2.9.1': [3], '2.9.2': [3, 4], '2.9.4': [7, 8]}, repl={'2.9.3': 'ch2_nexus'}),
        K('2.10', drop={'2.10.4': [2, 3]}),
        K('2.11', drop={'2.11': [2, 5, 6]}, add={'2.11': 'ch2_bridge_comparative'}),
        K('2.12', drop={'2.12': [0, 1]}, add={'2.12': 'ch2_bridge_critical'}),
        K('2.13', omit=['2.13.5', '2.13.6', '2.13.7'], drop={'2.13.1': [0, 1], '2.13.2': [4]}, add={'2.13.1': 'ch2_bridge_gaps'},
          subtitles={'2.13.2': 'Research gap supported by the systematic review (September 2026)'},
          after={'2.13.4': 'ch2_updates_early', '2.13.7': 'ch2_update_nov11'}),
        K('2.14', drop={'2.14': [4, 5, 6, 7]}, add={'2.14': 'ch2_summary_gap'}),
    ],
    3: [
        K('3.1', omit=['3.1.6'], drop={'3.1.3': [1]}, add={'3.1.5': 'ch3_notation_bridge'}),
        K('3.2', omit=['3.2.3'], add={'3.2.2': 'ch3_interfaces_bridge'}), K('3.3'), K('3.4'), K('3.5'), K('3.6'), K('3.7'), K('3.8'), K('3.9'), K('3.10'),
        K('3.11', omit=['3.11.10'], add={'3.11.9': 'ch3_cusum_bridge'}, after={'3.11.11': 'ch3_nov_protocols'}),
        K('3.12', after={'3.12.3': 'ch3_outcome_layers'}),
        N('ch3_v11'),
        N('ch3_impl'),
        K('3.14', add={'3.14': 'ch3_threats_add'}),
        N('ch3_summary'),
    ],
    4: [
        N('ch4_intro'),
        K('4.2', after={'4.2.3': 'ch4_data_nov'}),
        K('4.3'), K('4.4'), K('4.5'),
        K('4.6', drop={'4.6.2': [8, 9, 10, 11]}, add={'4.6.2': 'ch4_semantics_note'}),
        K('4.7'), K('4.8'), K('4.9'), K('4.10'), K('4.11'),
        N('ch4_rules'),
        N('ch4_generalization'),
        N('ch4_probes'),
        N('ch4_confirm'),
        N('ch4_live'),
        K('4.15', drop={'4.15': [0], '4.15.2': [1]}, add={'4.15': 'ch4_interp_pre'},
          repl={'4.15.1': 'ch4_interp_table', '4.15.4': 'ch4_not_supported'}, after={'4.15.3': 'ch4_interp_new'}),
        K('4.16', drop={'4.16': [1, 2, 3, 4, 5, 6]}, add={'4.16': 'ch4_priorart_nov'}),
        K('4.17', add={'4.17': 'ch4_threats_add'}),
        N('ch4_summary'),
    ],
    5: [N('ch5_all')],
}

# (letter, title, items); items: ('frag', name) | ('unit', chapter, base number, title or None) | ('block', chapter, unit, [indices], title)
APPENDICES = [
    ('A', 'Systematic Review: Search Strings, Supporting Tables and Evidence Matrix', [
        ('frag', 'app_a_intro'),
        ('block', 2, '2.2.3', [4], 'Database searches'),
        ('block', 2, '2.5', [2], 'Benchmarks used by included studies'),
        ('block', 2, '2.6', [3], 'Where included defenses intervene and what they observe'),
        ('block', 2, '2.9.1', [3], 'Runtime responses reported by included systems'),
        ('unit', 2, 'Appendix 2A', 'Comparative evidence matrix of defense and design studies'),
        ('unit', 2, '2.2.4', 'Eligibility criteria'),
        ('block', 2, '2.2.5', [6, 7, 8, 9], 'Exclusions at screening and at eligibility'),
        ('unit', 2, '2.2.6', 'Quality appraisal'),
        ('unit', 2, '2.2.7', 'Data extraction'),
        ('unit', 2, '2.2.8', 'Evidence synthesis'),
        ('block', 2, '2.4.5', [1, 2], 'Threat classes and the included evidence'),
        ('unit', 2, '2.6.4', 'Learned and LLM-based guardrails'),
        ('unit', 2, '2.7.1', 'Step-level, sequence-level and accumulating monitors'),
        ('unit', 2, '2.7.4', 'Foundations: behavioral anomaly detection and its cautions'),
        ('unit', 2, '2.8.5', 'What attribution contributes to auditability'),
        ('block', 2, '2.11', [5, 6], 'Decision mechanisms of the runtime systems closest to REM'),
        ('block', 2, '2.12', [1], 'Thematic synthesis of the included evidence'),
        ('block', 2, '2.13.1', [1], 'Assessment of candidate research gaps'),
        ('unit', 2, '2.3', 'AI agents and emerging security risks'),
        ('unit', 2, '2.4.2', 'Tool misuse, action manipulation and new tool channels'),
        ('unit', 2, '2.4.3', 'Context and memory manipulation'),
        ('unit', 2, '2.4.4', 'Multi-step propagation, goal drift and abnormal execution'),
        ('unit', 2, '2.6.1', 'Input-, context- and model-level protection'),
        ('unit', 2, '2.6.2', 'System-level and information-flow defenses'),
        ('unit', 2, '2.8.1', 'Why logistic regression'),
        ('unit', 2, '2.8.3', 'Why sequential evidence matters'),
        ('unit', 2, '2.13.6', 'Currency update of 30 October 2026 (outside the PRISMA flow)'),
        ('unit', 2, '2.13.7', 'Supplementary literature update of 2 November 2026: Kanaker et al. (2026) (outside the PRISMA flow)'),
    ]),
    ('B', 'System Implementation: Details', [
        ('frag', 'app_b_intro'),
        ('unit', 3, '3.16', 'Implementation of the REM framework'),
    ]),
    ('C', 'Notation, Optional Sequential Analysis and Equation Provenance', [
        ('unit', 3, '3.1.6', 'Notation'),
        ('unit', 3, '3.2.3', 'Layer interfaces'),
        ('unit', 3, '3.11.10', 'Optional observe-only sequential analysis'),
        ('unit', 3, '3.15', 'Provenance of the equations of Chapter 3'),
    ]),
    ('D', 'Live-Agent and MELON Evaluations: Design and Status (Not Executed)', [
        ('frag', 'app_d_intro'),
        ('unit', 3, '3.17', 'Closed-loop evaluation with live agents: design and implementation status'),
        ('unit', 4, '4.12', 'Closed-loop evaluation with live agents: status on 3 November 2026'),
        ('unit', 4, '4.13', 'Replay versus live evaluation'),
        ('unit', 4, '4.14', 'Controlled evaluation of MELON with and without REM: protocol'),
    ]),
    ('E', 'Sensitivity of the Replay Results to the Mitigation Semantics', [
        ('frag', 'app_e_intro'),
        ('block', 4, '4.6.2', [9, 10, 11], 'Replay results under the two mitigation semantics'),
    ]),
    ('F', 'Register of Open Supervisor Decisions', [
        ('frag', 'app_decisions'),
    ]),
]

# replacements applied to the assembled chapter text BEFORE renumbering (base numbering); each anchor must exist
REPLACE = {
    2: [
        ('**Table 2.8** (Appendix 2A)', '**Table 2.8** (Appendix A)'),
        ('is reproduced in **Appendix 2A**', 'is reproduced in **Appendix A**'),
    ],
    4: [
        ('Table 4.12 compares both semantics', 'Table 4.11 compares both semantics'),
    ],
}
# applied to every chapter and to the appendices where present (artifacts of the earlier automated assembly)
GLOBAL_PRE = [
    ('**No claim in this chapter is at level F**, because no full text was retrieved.',
     '**No claim of the systematic review is at level F**, because no full text was retrieved for it. Six papers were read in full on 11 November 2026, outside the review; they are reported separately in Section 2.13.41.'),
    ('These syntheses appear at the end of the relevant sections and are consolidated in Section 2.12 (Table 2.10).',
     'The syntheses are consolidated in Table 2.10.'),
    ('methodology of Sections 3.1–3.15', 'methodology of Chapter 3'),
    ('The observe-only analyses (Sections 3.11.5–3.11.10)', 'The observe-only analyses (Sections 3.11.5–3.11.9)'),
    ('Sections 2.3 to 2.5 cover agent risk, threats, benchmarks and threat models.', 'Sections 2.4 and 2.5 cover threats, benchmarks and threat models.'),
    ('the the methodology (Sections 3.1–3.15)', 'the Chapter 3'),
    ('the methodology (Sections 3.1–3.15)', 'the methodology of Chapter 3'),
    ('the methodology of Chapter 3 specified REM', 'Chapter 3 specified REM'),
]
# dropped base units -> surviving base (or new) number
REDIRECT = {
    '3.16.11.2': '3.16.11', '3.16.11.1': '3.16.11', '3.16.11.3': '3.16.11',
    '1.4': '1.41', '1.9': '1.42', '1.11': '1.43', '1.12': '1.44',
    '2.13.5': '2.13.4',
    '3.13': '1.43', '3.18': '3.43',
    '4.1': '4.41', '4.18': '4.48',
    '5.1': '5.41', '5.2': '5.42', '5.3': '5.43', '5.4': '5.44', '5.5': '5.46', '5.6': '5.47', '5.7': '5.48',
}
# section-level references to units moved to an appendix point to the main-text summary instead
OVERRIDE = {'2.6.4': '2.6', '2.7.1': '2.7', '2.8.5': '2.8', '2.2.6': '2.2.40', '2.2.7': '2.2.40', '2.2.8': '2.2.40', '3.16': '3.42', '4.12': '4.46', '4.13': '4.46', '4.14': '4.46', '2.13.6': '2.13.40', '2.13.7': '2.13.40'}
REDIRECT_TABLES = {'3.16': '2.12', '4.16': '4.54', '4.17': '4.56', '5.1': '5.41', '5.2': '5.42'}
# replacements applied AFTER renumbering (final numbering); each anchor must exist
POST = []
