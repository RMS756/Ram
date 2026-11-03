"""Assemble the five-chapter thesis from the six R5 chapters (scripted, logged, reproducible).

usage: python3 REM_FINAL_THESIS/tools/make_5ch.py        (from the repository root)

Reads   REM_FINAL_THESIS/chapters_R5/*_R5.md   (left unchanged)
Writes  REM_FINAL_THESIS/final_five_chapters/src/*.md and audit/source_map.json, audit/crossref_check.txt

Structure (old R5 -> new):
  Ch1 <- old Ch1 (1.1 expanded with background subsections; 1.12 rewritten for five chapters)
  Ch2 <- old Ch2 (unchanged numbering)
  Ch3 <- old Ch3 3.1-3.15  + 3.16 System Implementation (old Ch4 4.1-4.14, demoted one level)
         + 3.17 Closed-loop live-agent evaluation (new: design and implementation status)
         + 3.18 Chapter Summary (old 3.16 and old 4.15 merged)
  Ch4 <- old Ch5 5.1-5.11 -> 4.1-4.11 + 4.12 live status (new) + 4.13 replay vs live (new)
         + 4.14 old 6.1 + 4.15 old 6.3 + 4.16 old 6.5 + 4.17 summary (new)
  Ch5 <- 5.1 intro (new) + 5.2 old 5.12 + 5.3 old 6.2 + 5.4 old 6.4 + 5.5 limitations summary (new)
         + 5.6 old 6.6 + 5.7 old 6.7
Every cross-reference to a section, table, figure or chapter is rewritten in one pass through explicit
maps; unresolved references are listed, never silently left. No number, result or equation is changed.
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'REM_FINAL_THESIS', 'chapters_R5')
OUT = os.path.join(ROOT, 'REM_FINAL_THESIS', 'final_five_chapters')
SRCOUT = os.path.join(OUT, 'src')
FIG = 'REM_FINAL_THESIS/final_five_chapters/figures'
os.makedirs(SRCOUT, exist_ok=True)
os.makedirs(os.path.join(OUT, 'audit'), exist_ok=True)

NAMES = {1: 'CHAPTER1_INTRODUCTION', 2: 'CHAPTER2_LITERATURE_REVIEW', 3: 'CHAPTER3_METHODOLOGY',
         4: 'CHAPTER4_IMPLEMENTATION', 5: 'CHAPTER5_RESULTS', 6: 'CHAPTER6_DISCUSSION_CONCLUSION'}
old = {k: open(os.path.join(SRC, v + '_R5.md'), encoding='utf-8').read() for k, v in NAMES.items()}
LOG = []


def sections(text):
    """[(number, title, body)] for level-2 headings; preamble under key None."""
    parts = re.split(r'^(## .+)$', text, flags=re.M)
    out = [(None, None, parts[0])]
    for i in range(1, len(parts), 2):
        h = parts[i][3:].strip()
        m = re.match(r'(\d+(?:\.\d+)*)\s+(.*)', h)
        out.append((m.group(1), m.group(2), parts[i + 1]) if m else (None, h, parts[i + 1]))
    return out


S = {k: sections(v) for k, v in old.items()}


def sec(ch, num):
    for n, t, b in S[ch]:
        if n == num:
            return t, b
    sys.exit(f'section {num} not found in old chapter {ch}')


# ------------------------------------------------------------------ number maps (old -> new)
SEC = {}
for ch in (1, 2, 3):
    for n, t, b in S[ch]:
        if n:
            SEC[n] = n
            for m in re.findall(r'^#{3,4} (\d+(?:\.\d+)+)\s', b, flags=re.M):
                SEC[m] = m
SEC['3.16'] = '3.18'
for n, t, b in S[4]:
    if n:
        SEC[n] = '3.16.' + n.split('.', 1)[1] if n != '4.15' else '3.18'
        for m in re.findall(r'^#{3,4} (\d+(?:\.\d+)+)\s', b, flags=re.M):
            SEC[m] = '3.16.' + m.split('.', 1)[1]
for n, t, b in S[5]:
    if n:
        SEC[n] = '4.' + n.split('.', 1)[1] if n != '5.12' else '5.2'
        for m in re.findall(r'^#{3,4} (\d+(?:\.\d+)+)\s', b, flags=re.M):
            SEC[m] = '4.' + m.split('.', 1)[1]
C6 = {'6.1': '4.14', '6.2': '5.3', '6.3': '4.15', '6.4': '5.4', '6.5': '4.16', '6.6': '5.6', '6.7': '5.7'}
for n, t, b in S[6]:
    if n:
        SEC[n] = C6[n]
        for m in re.findall(r'^#{3,4} (\d+(?:\.\d+)+)\s', b, flags=re.M):
            SEC[m] = C6[n] + m[len(n):]
TAB = {}
for ch in (1, 2, 3):
    for m in re.findall(r'\*\*Table (\d+\.\d+)\.', old[ch]):
        TAB[m] = m
TAB.update({f'4.{i}': f'3.{17 + i}' for i in range(1, 9)})          # 4.1-4.8 -> 3.18-3.25
TAB.update({f'5.{i}': f'4.{i}' for i in range(1, 13)})              # 5.1-5.12 -> 4.1-4.12
TAB.update({'5.13': '5.1', '6.1': '4.15', '6.3': '4.16', '6.2': '5.2'})
FIGM = {'2.1': '2.1', '3.1': '3.1', '5.1': '4.1', '5.2': '4.2',
        '1.1': '1.1', '3.2': '3.2', '3.3': '3.3', '3.4': '3.4', '3.5': '3.5', '4.3': '4.3'}   # new figures keep their numbers
CHMAP = {1: 1, 2: 2, 3: 3, 4: 3, 5: 4, 6: 5}
UNMAPPED = []

NUM = r'\d+(?:\.\d+)*[A-Z]?'
SEPS = r'(?:\s?[–-]\s?|,\s(?:and\s)?|\sand\s|\sto\s)'
LIST = rf'{NUM}(?:{SEPS}{NUM})*'
KW = r'(?:Sections?|Sec\.|§§?|Tables?|Figures?|Equations?|Eqs?\.|Procedure|Algorithm)'
PAT = re.compile(rf'(?P<combo>(?P<ckw>Chapters?)\s(?P<cn>\d)(?P<csep>,?\s)(?P<ikw>{KW})(?P<isp>\s?)(?P<inums>{LIST}))'
                 rf'|(?P<simple>(?P<kw>{KW}|Chapters?)(?P<sp>\s?)(?P<nums>{LIST}))')


def kind(kw):
    if kw.startswith(('Section', 'Sec', '§')):
        return 'sec'
    if kw.startswith('Table'):
        return 'tab'
    if kw.startswith('Figure'):
        return 'fig'
    if kw.startswith('Chapter'):
        return 'ch'
    return 'other'                       # equations, procedure, algorithm: Ch2/Ch3 numbering unchanged


def map_num(k, n, where):
    if k == 'other':
        return n
    if k == 'ch':
        return str(CHMAP.get(int(n), int(n)))
    table = {'sec': SEC, 'tab': TAB, 'fig': FIGM}[k]
    if n in table:
        return table[n]
    if k == 'sec' and re.match(r'^[123]\.', n):
        return n
    UNMAPPED.append((where, k, n))
    return n


def map_list(k, nums, where):
    toks = re.split(rf'({SEPS})', nums)
    out = [map_num(k, t, where) if i % 2 == 0 else t for i, t in enumerate(toks)]
    if k == 'ch' and len(out) == 3 and out[0] == out[2]:
        return out[0], True
    return ''.join(out), False


def at_sentence_start(s, pos):
    pre = s[max(0, pos - 3):pos]
    return pos == 0 or pre.endswith(('. ', '\n', '**', '- ', '| ', ': ')) or pre.strip() == ''


def rewrite(text, home, origin, where):
    def repl(m):
        if m.group('combo'):
            k = kind(m.group('ikw'))
            inums, _ = map_list(k, m.group('inums'), where)
            first = inums.split('.')[0] if k in ('sec', 'tab', 'fig') else str(CHMAP[int(m.group('cn'))])
            if k == 'other':
                first = m.group('cn')
            tgt = int(first)
            if tgt == home:
                return f"{m.group('ikw')}{m.group('isp')}{inums}"
            return f"Chapter {tgt}{m.group('csep')}{m.group('ikw')}{m.group('isp')}{inums}"
        kw, nums = m.group('kw'), m.group('nums')
        k = kind(kw)
        if k == 'ch':
            n0 = int(re.match(r'\d+', nums).group(0))
            if kw == 'Chapter' and re.fullmatch(r'\d', nums):
                if n0 == 4:
                    return 'Section 3.16'
                if n0 == 3 and origin == 4:
                    return 'the methodology (Sections 3.1–3.15)'
                tgt = CHMAP[n0]
                if tgt == home and origin != home:
                    return 'This chapter' if at_sentence_start(m.string, m.start()) else 'this chapter'
                return f'Chapter {tgt}'
            s, collapsed = map_list('ch', nums, where)
            return ('Chapter ' if collapsed else kw + m.group('sp')) + s
        s, _ = map_list(k, nums, where)
        return f'{kw}{m.group("sp")}{s}'
    return PAT.sub(repl, text)


def demote(body, levels=1):
    return re.sub(r'^(#{3,5}) ', lambda m: '#' * (len(m.group(1)) + levels) + ' ', body, flags=re.M)


def renum_subheads(body):
    return re.sub(r'^(#{3,6}) (\d+(?:\.\d+)+)(\s)', lambda m: f'{m.group(1)} {SEC.get(m.group(2), m.group(2))}{m.group(3)}',
                  body, flags=re.M)


def block(ch_old, num, home, new_num=None, new_title=None, level=2, extra_rep=()):
    t, b = sec(ch_old, num)
    b = renum_subheads(b)
    if level == 3:
        b = demote(b)
    # Inserted text is already written in the NEW numbering, so it is protected
    # from rewrite(); only the original anchor text (old numbering) is rewritten.
    protected = {}
    for i, (a, c) in enumerate(extra_rep):
        if a not in b:
            sys.exit(f'anchor not found in {num}: {a[:60]!r}')
        pieces = c.split(a) if a in c else [c]
        toks = []
        for j, p in enumerate(pieces):
            k = f'@@XREP{i}_{j}@@'
            protected[k] = p
            toks.append(k)
        b = b.replace(a, a.join(toks))
    b = rewrite(b, home, ch_old, f'old {num}')
    for k, v in protected.items():
        b = b.replace(k, v)
    nn = new_num or SEC[num]
    LOG.append({'new': nn, 'title': new_title or t, 'old_chapter': ch_old, 'old_section': num})
    return f"{'#' * level} {nn} {new_title or t}\n{b}"


def new(num, title, body, level=2):
    LOG.append({'new': num, 'title': title, 'old_chapter': None, 'old_section': 'NEW'})
    return f"{'#' * level} {num} {title}\n\n{body.strip()}\n\n"


def figure(num, caption, path):
    return f'![Figure {num}. {caption}]({path}){{width=100%}}\n\n'


# ================================================================== CHAPTER 1
ch1 = '# CHAPTER ONE\n\n# INTRODUCTION\n\n'
t11, b11 = sec(1, '1.1')
BG = '''### 1.1.1 Language models and AI agents

Artificial intelligence systems based on large language models (LLMs) generate text, and increasingly structured actions, from natural-language input. An *LLM agent* uses such a model as the controller of a system that perceives its context, reasons, plans and acts in pursuit of a task (L. Wang et al., 2024). In the execution pattern made explicit by ReAct (Yao et al., 2023), the model interleaves reasoning with actions, and the observations returned by those actions re-enter its context and shape the next step. The term *agentic AI* is used in this thesis only in this operational sense: a model-driven system that selects and executes actions with some autonomy.

### 1.1.2 Tool-using and financial AI agents

Tool-using agents act through calls to external tools, such as file readers, messaging services or payment interfaces, with arguments that the model generates. When such an agent operates in a financial setting, a single proposed tool call can have direct external effects:

- initiate a payment;
- schedule or alter a recurring payment;
- change account credentials;
- send customer data to an external recipient.

Evaluations of agents in finance have argued that capability benchmarks alone are insufficient and that the risk of such actions must be assessed directly (Z. Chen et al., 2025).

### 1.1.3 Indirect prompt injection

Indirect prompt injection is content placed in data that the agent retrieves or receives from a tool, rather than in the user's request, and that the agent then treats as an instruction (Greshake et al., 2023; OWASP Gen AI Security Project, 2025). Because tool outputs re-enter the model's context, an attacker who can write into an e-mail, a file or a transaction description can attempt to redirect the agent's next action. The resulting harm is caused by the action, not by the text: an injected instruction is dangerous when it leads the agent to propose a call that serves the attacker. Figure 1.1 illustrates this path in a banking task of the kind used in this thesis.

''' + figure('1.1', 'A financial agent task with an indirect prompt injection. The user request is trusted; the tool output carrying the injected instruction is untrusted; the harm occurs only if the proposed state-changing call (here a transfer to the attacker) is executed. REM is placed at the tool-execution boundary.', f'{FIG}/fig1_1_threat_scenario.png') + '''### 1.1.4 Runtime security at the tool-execution boundary

'''
b11_last = b11.strip().split('\n\n')[-1]           # "The security question therefore shifts ..."
ch1 += f'## 1.1 Background\n\n{BG}{rewrite(b11_last, 1, 1, "old 1.1")}\n\n'
LOG.append({'new': '1.1', 'title': 'Background (expanded: 1.1.1-1.1.4)', 'old_chapter': 1, 'old_section': '1.1'})
for n in ['1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8', '1.9', '1.10']:
    ch1 += block(1, n, 1)
ch1 += block(1, '1.11', 1, extra_rep=[(
    '- an evaluation of enforcement against live agents;',
    '- an evaluation of enforcement against live agents (a closed-loop harness is implemented and tested with scripted test agents, Section 3.17, but has not been executed with a language model, Section 4.12);')])
ch1 += new('1.12', 'Thesis Organization', '''The thesis is organized in five chapters:

- **Chapter 1** introduces the background, problem, gap, aim, objectives, research questions, approach, scope and contributions.
- **Chapter 2** reports a record-level systematic review of runtime security for tool-using AI agents, compares the closest prior work and states the research gap it supports.
- **Chapter 3** specifies the research methodology and the design of REM (architecture, threat model, evidence, estimator, calibration, consequence tiers, expected-loss decision, mitigation, audit), the experimental methodology and metrics, the software implementation and its verification (Section 3.16), and the design and implementation status of a closed-loop evaluation with live agents (Section 3.17).
- **Chapter 4** reports the exploratory evaluation on recorded agent traces, states the status of the live-agent evaluation, and discusses the findings, the comparison with prior work and the threats to validity.
- **Chapter 5** answers the research questions, assesses the objectives and contributions, summarises the limitations, and concludes with recommendations and future work ordered by dependency.''')

# ================================================================== CHAPTER 2 (unchanged numbering)
ch2_lines = old[2]
ch2 = rewrite(ch2_lines, 2, 2, 'old Ch2')
LOG.append({'new': '2.1-2.14, Appendix 2A', 'title': 'Literature Review (numbering unchanged)', 'old_chapter': 2, 'old_section': 'all'})

# ================================================================== CHAPTER 3
ch3 = '# CHAPTER THREE\n\n# RESEARCH METHODOLOGY, DESIGN AND IMPLEMENTATION OF THE REM FRAMEWORK\n\n'
RISKFIG = figure('3.2', 'Conditional risk R(v | p) of the four verdicts (Eq. 3.6) as a function of the calibrated probability p, for the declared exploratory costs of tiers 1–4 (C~FA~ = 1; C~miss~ = 1, 5, 10, 20; C~mod~ = 0.5; C~esc~ = 0.3; r~mod~ as estimated in the pilot: 1, 1, 0, 0.01). The verdict is the lower envelope. The figure plots the equations for declared values; it is not an experimental result.', f'{FIG}/fig3_2_conditional_risk.png')
for n in ['3.1', '3.2', '3.3', '3.4', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10', '3.11', '3.12', '3.13', '3.14', '3.15']:
    extra = ()
    if n == '3.7':
        extra = [('\n### 3.7.6 Explainability and audit record', '\n' + RISKFIG + '### 3.7.6 Explainability and audit record')]
    if n == '3.10':
        t, b = sec(3, n)
        ch3 += block(3, n, 3) + '\n' + figure('3.3', 'REM runtime workflow for one proposed tool call, as implemented in the evaluated path (`RemGuard.evaluate`): evidence, estimation and calibration, consequence tier, predicates, expected-loss verdict, mitigation before execution, and the audit record. Attribution is computed after the verdict and cannot change it.', f'{FIG}/fig3_3_runtime_workflow.png')
        continue
    if n == '3.11':
        extra = [('\n### 3.11.6 Leakage controls', '\n' + figure('3.4', 'Recorded-trace evaluation design: nested grouped cross-fitting (nine outer folds by injection task, four inner folds), held-out predictions, observe-only decisions and the NO-ADAPT replay sensitivity analysis in the AgentDojo sandbox.', f'{FIG}/fig3_4_evaluation_design.png') + '### 3.11.6 Leakage controls')]
    ch3 += block(3, n, 3, extra_rep=extra)
ch3 += new('3.16', 'System Implementation', '''This section reports how the methodology of Sections 3.1–3.15 is implemented in software: the environment, the organisation of the code and its execution paths, the implementation of each layer, the verification of the software, the correspondence between equations, code, tests and results, and the measurement of processing time. It was Chapter 4 of the six-chapter draft (R5); its content is preserved and renumbered.''')
for n, t, b in S[4]:
    if n and n != '4.15':
        title = 'Purpose and Scope' if n == '4.1' else t
        ch3 += block(4, n, 3, level=3, new_title=title,
                     extra_rep=[('This chapter', 'This section')] if 'This chapter' in b else ())
ch3 += new('3.17', 'Closed-Loop Evaluation with Live Agents: Design and Implementation Status', open(os.path.join(os.path.dirname(__file__), 'text_5ch', 'ch3_live.md'), encoding='utf-8').read())
t316, b316 = sec(3, '3.16')
t415, b415 = sec(4, '4.15')
ch3 += f"## 3.18 Chapter Summary\n\n**Methodology.** {rewrite(b316.strip(), 3, 3, 'old 3.16')}\n\n**Implementation.** {rewrite(b415.strip().replace('This chapter', 'Section 3.16'), 3, 4, 'old 4.15')}\n\n**Closed-loop evaluation.** A closed-loop integration in which a running agent receives REM's refusals is implemented and tested with scripted test agents (Section 3.17); it has not been executed with a language model.\n\n"
LOG.append({'new': '3.18', 'title': 'Chapter Summary (old 3.16 + old 4.15 merged)', 'old_chapter': '3+4', 'old_section': '3.16, 4.15'})

# ================================================================== CHAPTER 4
ch4 = '# CHAPTER FOUR\n\n# RESULTS AND DISCUSSION\n\n'
for n in ['5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9', '5.10', '5.11']:
    extra = ()
    if n == '5.1':
        extra = [('The results are therefore not presented as confirmation of any claim, and the confirmatory evaluation remains pending.',
                  'The results are therefore not presented as confirmation of any claim, and the confirmatory evaluation remains pending. The closed-loop harness for live agents (Section 3.17) is implemented but was not executed; its status is reported in Section 4.12, and no live result appears in this chapter.')]
    if n == '5.6':
        t, b = sec(5, n)
        anchor = next(l for l in b.split('\n') if l.startswith('![Figure 5.2.'))
        extra = [(anchor, anchor + '\n\n' + figure('4.3', 'Security–utility trade-off in the replay sensitivity analysis (NO-ADAPT, step-level semantics): attack success rate against benign utility for B0, B1, REM and REM without expected-loss Escalate under both reviewer bounds, and for the single-tier ablations. Values from `results/pilot_R2/e4_e5_enforcement_replay.json`; no live result.', f'{FIG}/fig4_3_security_utility_tradeoff.png').rstrip())]
    ch4 += block(5, n, 4, extra_rep=extra)
ch4 += new('4.12', 'Closed-Loop Evaluation with Live Agents: Status', open(os.path.join(os.path.dirname(__file__), 'text_5ch', 'ch4_live_status.md'), encoding='utf-8').read())
ch4 += new('4.13', 'Replay Versus Live Evaluation', open(os.path.join(os.path.dirname(__file__), 'text_5ch', 'ch4_replay_vs_live.md'), encoding='utf-8').read())
pre6 = S[6][0][2].split('# DISCUSSION, CONTRIBUTIONS, LIMITATIONS, AND CONCLUSION', 1)[1].strip()
PRE6_OLD = 'This chapter interprets the exploratory evaluation of Chapter 5.'
if PRE6_OLD not in pre6:
    sys.exit('Ch6 preamble anchor missing')
pre6 = pre6.replace(PRE6_OLD, '@@PRE6@@')
pre6 = rewrite(pre6, 4, 6, 'old Ch6 preamble').replace(
    '@@PRE6@@', 'This section interprets the exploratory evaluation reported in Sections 4.1–4.11.')  # new numbering, not rewritten
ch4 += block(6, '6.1', 4).replace('## 4.14 Interpretation of the Findings\n', '## 4.14 Interpretation of the Findings\n\n' + pre6 + '\n', 1)
ch4 += block(6, '6.3', 4)
ch4 += block(6, '6.5', 4, new_title='Threats to Validity and Limitations')
ch4 += new('4.17', 'Chapter Summary', open(os.path.join(os.path.dirname(__file__), 'text_5ch', 'ch4_summary.md'), encoding='utf-8').read())

# ================================================================== CHAPTER 5
ch5 = '# CHAPTER FIVE\n\n# CONCLUSIONS AND RECOMMENDATIONS\n\n'
ch5 += new('5.1', 'Introduction', '''This chapter draws the conclusions of the thesis. Section 5.2 answers the research questions from the evidence of Chapter 4; Section 5.3 assesses the objectives; Section 5.4 separates the contributions achieved from those proposed; Section 5.5 summarises the limitations discussed in Section 4.16; Section 5.6 gives recommendations and future work ordered by dependency; and Section 5.7 concludes. Every conclusion is bounded by the exploratory status of the evidence: recorded traces, observe-only decisions and a replay that assumes the agent does not adapt. No live-agent result exists (Section 4.12).''')
ch5 += block(5, '5.12', 5, new_title='Answers to the Research Questions')
ch5 += block(6, '6.2', 5)
ch5 += block(6, '6.4', 5)
ch5 += new('5.5', 'Limitations', open(os.path.join(os.path.dirname(__file__), 'text_5ch', 'ch5_limitations.md'), encoding='utf-8').read())
ch5 += block(6, '6.6', 5, new_title='Recommendations and Future Work, Ordered by Dependency')
ch5 += block(6, '6.7', 5)

OUTS = {'CHAPTER1_INTRODUCTION': ch1, 'CHAPTER2_LITERATURE_REVIEW': ch2, 'CHAPTER3_METHODOLOGY': ch3,
        'CHAPTER4_RESULTS_DISCUSSION': ch4, 'CHAPTER5_CONCLUSIONS': ch5}
POST = [('of the methodology (Sections 3.1–3.15) (Eqs. 3.15–3.19)', 'of Eqs. 3.15–3.19'),
        # integrity wording (see POST4 below): the R3 run re-executed this project's code; not an external replication
        ('| Independent re-execution (R3) |', '| Re-execution in a fresh environment (R3) |'),
        ('- **Independent re-execution (R3, 30 October 2026).**', '- **Re-execution in a fresh environment (R3, 30 October 2026; by this project, not an external replication).**')]
for a_, b_ in POST:
    if a_ not in OUTS['CHAPTER3_METHODOLOGY']:
        sys.exit(f'post anchor missing: {a_}')
    OUTS['CHAPTER3_METHODOLOGY'] = OUTS['CHAPTER3_METHODOLOGY'].replace(a_, b_)
# Wording corrections applied to R5 text (integrity rule: no claim of independent validation unless
# independently reproduced). The 30 Oct re-execution re-ran the project's own code in a fresh
# environment; it is not an external replication. Logged in audit/THESIS_SOURCE_MAP.md.
POST4 = [('An independent re-execution on 30 October 2026 reproduced every analytical value',
          'A re-execution of the full pipeline in a fresh environment on 30 October 2026 (by this project, not an external replication) reproduced every analytical value'),
         ('The independent re-execution of 30 October measured the same value.',
          'The re-execution of 30 October measured the same value.')]
for a_, b_ in POST4:
    if a_ not in OUTS['CHAPTER4_RESULTS_DISCUSSION']:
        sys.exit(f'post anchor missing: {a_}')
    OUTS['CHAPTER4_RESULTS_DISCUSSION'] = OUTS['CHAPTER4_RESULTS_DISCUSSION'].replace(a_, b_)
for k, v in OUTS.items():
    open(os.path.join(SRCOUT, k + '.md'), 'w', encoding='utf-8').write(re.sub(r'\n{3,}', '\n\n', v))

# ------------------------------------------------------------------ cross-reference check on the output
allt = '\n'.join(OUTS.values())
heads = set(re.findall(r'^#{2,6} (\d+(?:\.\d+)+)\s', allt, flags=re.M))
tabs = set(re.findall(r'\*\*Table (\d+\.\d+)\.', allt))
figs = set(re.findall(r'!\[Figure (\d+\.\d+)\.', allt))
eqs = set(re.findall(r'\\qquad \((\d+\.\d+)\)', allt))
bad = []
for m in re.finditer(rf'(Sections?|§§?|Tables?|Figures?)\s?({LIST})', allt):
    k = kind(m.group(1))
    for n in re.split(SEPS, m.group(2)):
        if not re.match(r'^\d+\.\d+', n):
            continue
        ok = n in (heads if k == 'sec' else tabs if k == 'tab' else figs)
        if not ok and k == 'sec':
            ok = n in ('2A',)
        if not ok:
            bad.append((m.group(0), allt[max(0, m.start() - 60):m.start()].replace('\n', ' ')))
for m in re.finditer(r'(?:Equations?|Eqs?\.)\s?(' + LIST + ')', allt):
    for n in re.split(SEPS, m.group(1)):
        if re.match(r'^\d+\.\d+$', n) and n not in eqs:
            bad.append((m.group(0), allt[max(0, m.start() - 60):m.start()].replace('\n', ' ')))
chap_counts = {k: len(re.findall(r'^# CHAPTER ', v, flags=re.M)) for k, v in OUTS.items()}
with open(os.path.join(OUT, 'audit', 'crossref_check.txt'), 'w', encoding='utf-8') as fh:
    fh.write(f'chapters: {sum(chap_counts.values())} ({chap_counts})\nnumbered headings: {len(heads)}; tables: {len(tabs)}; '
             f'figures: {len(figs)}; equations: {len(eqs)}\n')
    fh.write(f'unmapped old references during rewriting: {len(UNMAPPED)}\n')
    for u in UNMAPPED:
        fh.write(f'  UNMAPPED {u}\n')
    fh.write(f'unresolved references in the output: {len(bad)}\n')
    for b in bad:
        fh.write(f'  UNRESOLVED {b[0]!r} … {b[1]!r}\n')
json.dump({'sections': LOG, 'section_map': SEC, 'table_map': TAB, 'figure_map': FIGM, 'chapter_map': CHMAP},
          open(os.path.join(OUT, 'audit', 'source_map.json'), 'w'), indent=1)
print(open(os.path.join(OUT, 'audit', 'crossref_check.txt')).read())
