"""Build the consolidated thesis working copy from the humanized edition (28 November 2026).

usage (from the repository root):
    python3 REM_FINAL_THESIS_CONSOLIDATION/thesis_working_copy/tools/make_working_copy.py
    python3 REM_FINAL_THESIS_CONSOLIDATION/thesis_working_copy/tools/build_wc.py

What it does
  1. Copies REM_HUMANIZED_THESIS/{src,text_front,references} into this working copy (the originals are only read).
  2. Merges the five dated insertions of the DiD edition (REM_DID_THESIS_EDITION/src) by their exact context
     (plan M1-M5 of REM_FINAL_SCIENTIFIC_RECONCILIATION_2026_11_28/03).
  3. Applies the edits listed in EDITS below. Every edit names its anchor; the script stops if an anchor does
     not occur exactly once, so no edit can land in the wrong place silently.
  4. Writes audit/edit_log.json (edit id, file, kind, characters before and after).

Edit identifiers match REM_FINAL_THESIS_CONSOLIDATION/10_FINAL_THESIS_INTEGRATION_GUIDE.md. No number, equation,
or result is changed; the edits correct documented overclaims, add documentation of what REM v1.0 already does
(A1-A7 of REM_LAYERED_FRAMEWORK_DESIGN_REVIEW/05), and merge the DiD insertions. Edits that need a supervisor
decision first (title, the RQ1-RQ5 restructuring) are NOT applied; see 07 and 08 of the consolidation.
"""
import difflib
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WC = os.path.abspath(os.path.join(HERE, '..'))
ROOT = os.path.abspath(os.path.join(WC, '..', '..'))
HUM = os.path.join(ROOT, 'REM_HUMANIZED_THESIS')
BASE = os.path.join(ROOT, 'REM_DEFENCE_READY_THESIS', 'src')
DID = os.path.join(ROOT, 'REM_DID_THESIS_EDITION')

for d in ('src', 'text_front', 'references'):
    shutil.rmtree(os.path.join(WC, d), ignore_errors=True)
    shutil.copytree(os.path.join(HUM, d), os.path.join(WC, d))

F = {}


def path(name):
    if name.startswith('REF'):
        return os.path.join(WC, 'references', 'REFERENCES_FINAL.md')
    if name.startswith('abstract'):
        return os.path.join(WC, 'text_front', name + '.md')
    return os.path.join(WC, 'src', name + '.md')


def get(name):
    if name not in F:
        F[name] = open(path(name), encoding='utf-8').read()
    return F[name]


LOG = []


def once(text, anchor, eid):
    n = text.count(anchor)
    if n != 1:
        sys.exit(f'[{eid}] anchor occurs {n} times: {anchor[:120]!r}')


def replace(eid, name, old, new):
    t = get(name)
    once(t, old, eid)
    F[name] = t.replace(old, new, 1)
    LOG.append({'id': eid, 'file': name, 'kind': 'replace', 'old_chars': len(old), 'new_chars': len(new),
                'old': old, 'new': new})


def line_starting(name, prefix, eid):
    lines = [l for l in get(name).split('\n') if l.startswith(prefix)]
    if len(lines) != 1:
        sys.exit(f'[{eid}] {len(lines)} lines start with {prefix[:100]!r}')
    return lines[0]


def replace_line(eid, name, prefix, new):
    replace(eid, name, line_starting(name, prefix, eid), new)


def insert_after_line(eid, name, prefix, block):
    l = line_starting(name, prefix, eid)
    replace(eid, name, l, l + '\n\n' + block)
    LOG[-1]['kind'] = 'insert_after'


def insert_before_line(eid, name, prefix, block):
    l = line_starting(name, prefix, eid)
    replace(eid, name, l, block + '\n\n' + l)
    LOG[-1]['kind'] = 'insert_before'


# ---------------------------------------------------------------------------------------------- 1. DiD merge
for ch in ('CHAPTER_02_FINAL', 'CHAPTER_03_FINAL', 'CHAPTER_04_FINAL', 'CHAPTER_05_FINAL'):
    b = open(os.path.join(BASE, ch + '.md'), encoding='utf-8').read().split('\n')
    d = open(os.path.join(DID, 'src', ch + '.md'), encoding='utf-8').read().split('\n')
    k = 0
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, b, d, autojunk=False).get_opcodes():
        if op == 'equal':
            continue
        k += 1
        eid = f'M-{ch[8:10]}-{k}'
        chunk = '\n'.join(d[j1:j2])
        if op == 'replace':
            old = '\n'.join(b[i1:i2])
            once(get(ch), old, eid)
            F[ch] = get(ch).replace(old, chunk, 1)
            LOG.append({'id': eid, 'file': ch, 'kind': 'did_replace', 'old_chars': len(old), 'new_chars': len(chunk)})
        elif op == 'insert':
            prev = b[i1 - 1]
            if prev.strip() and get(ch).count(prev) == 1:
                F[ch] = get(ch).replace(prev, prev + '\n' + chunk, 1)
            else:
                nxt = b[i1]
                once(get(ch), nxt, eid)
                F[ch] = get(ch).replace(nxt, chunk + '\n' + nxt, 1)
            LOG.append({'id': eid, 'file': ch, 'kind': 'did_insert', 'old_chars': 0, 'new_chars': len(chunk)})
        else:
            sys.exit(f'unexpected opcode {op} in {ch}')

# references added by the DiD edition (M5)
bref = open(os.path.join(ROOT, 'REM_DEFENCE_READY_THESIS', 'references', 'REFERENCES_FINAL.md'), encoding='utf-8').read().split('\n\n')
dref = open(os.path.join(DID, 'references', 'REFERENCES_FINAL.md'), encoding='utf-8').read().split('\n\n')
added = [e.strip() for e in dref if e.strip() and e not in bref]
NEW_REFS = list(added)

# ---------------------------------------------------------------------------------------------- 2. edits
# M1 (reconciliation 03): Spotlight-Guard row in Table 2.6, and the BARBICAN qualification of the "not found" statement
replace('M1a', 'CHAPTER_02_FINAL',
        '| AgentSandbox (K. Zhang et al., 2025; preprint) |',
        '| Spotlight-Guard (Demirol & Aydoğan, 2026; *Applied Sciences*) | A | Spotlighting-based input isolation, an LLM detection-and-quarantine pipeline and HMAC-based instruction integrity, in one layered defense for agents that read tool content | Reports a component ablation that isolates each layer, an adaptive-attack evaluation and benign-task success, on locally hosted 7B-class models; not a financial agent |\n'
        '| AgentSandbox (K. Zhang et al., 2025; preprint) |')
l = line_starting('CHAPTER_02_FINAL', '- What was not found, at the level read, is a measurement of how much protection remains', 'M1b')
replace('M1b', 'CHAPTER_02_FINAL', l, l + ' The closest measurement found later replaces the verdicts of one stage of a layered tool-call gateway by constants (Abasıkeleş Turgut & Gümüş, 2026b; Section 2.11.7); it concerns verdict substitution in one stage of a Model Context Protocol gateway, not suppression of an evidence family for a financial agent.')

# R4-9 (reconciliation 04): qualify the inserted Section 4.6.12
replace('R4-9a', 'CHAPTER_04_FINAL',
        '- In this replay, REM-DiD reaches Defense-in-Depth in the sense that independent controls protect when authorization is bypassed.',
        '- In this replay, with authorization bypassed by a broad envelope, REM-DiD\'s remaining controls stopped every replayed attack, individually reducing attacks and jointly removing them. The authorization itself was issued by an oracle or modelled as bypassed, so this shows residual coverage of the remaining controls, not defense in depth of a deployable system.')
replace('R4-9b', 'CHAPTER_04_FINAL',
        '- **Removing a control and evading it can therefore give opposite assessments.**',
        '- **Removing a control and evading it can therefore give opposite assessments.**\n'
        '- These evasion results concern REM v1.0 itself and are used in Sections 4.5.10 and 4.5.12 to qualify the removal-based ablation. The suppression is idealized: it sets a family\'s features to their not-fired values on attack-labeled calls and does not model how an attacker would achieve this.')

# ---- Chapter 1
replace_line('R1-1', 'CHAPTER_01_FINAL', 'The problem addressed in this thesis is the runtime compromise of tool-using financial agents',
             'The problem addressed in this thesis is the runtime compromise of tool-using financial agents through indirect prompt injection, and the question of whether a layered defense at the action boundary actually protects in depth. Such defenses are commonly organized as several layers (content inspection, behavioral analysis, action evidence, a risk-informed decision and enforcement), but layering is a property of the design, whereas defense in depth is a property of the protection: it holds only if more than one component contributes protection and the loss of one is covered by another. The thesis designs such a five-layer framework, REM, and evaluates on recorded agent behavior in a banking environment which of its components actually carry protection, at what cost to legitimate financial work, and how it compares with threshold and simple rule baselines.')
replace_line('R1-2a', 'CHAPTER_01_FINAL', '- **NEXUS** is a structured-plan safety monitor',
             '- **NEXUS**, published in the Findings of IJCNLP-AACL 2026, is a structured-plan safety monitor that applies a formal intervention policy to choose among allow, block, request confirmation and request revision. It combines deterministic rules, argument-level inspection and a calibrated logistic-regression risk score, and its abstract reports a comparison with rule-only intervention selection on non-financial benchmarks (Hossain et al., 2026). It is the closest published analogue of REM\'s Decision Engine.')
replace_line('R1-2b', 'CHAPTER_01_FINAL', 'The systematic review of Chapter 2 was conducted at record level in September 2026.',
             'The systematic review of Chapter 2 was conducted at record level in September 2026. Six of the papers above were read in full in November 2026, outside that review (Chapter 2, Section 2.11.4), and the Progent paper (version 3) on 16 November 2026. NEXUS is a peer-reviewed publication; its full text was not read, and statements about it rest on its abstract and its authors\' repository documentation. Several later works with layered or authorization-based designs (Chapter 2, Sections 2.11.4, 2.11.6 and 2.11.7) are known only from their abstracts. Substantial prior-art overlap therefore exists for every component of REM and for layered combinations of them, and this thesis does not claim an architectural or mechanism novelty. The review is not exhaustive, and no claim is made that every possible combination has been published.')
replace_line('C-GAP1', 'CHAPTER_01_FINAL', '> Runtime defenses for tool-using agents now combine',
             '> Layered runtime defenses against indirect prompt injection, combining content inspection, provenance-aware, behavioral, learned and rule-based controls, have been proposed and, in several cases, ablated layer by layer. Among the studies examined, most of them at abstract level, the evidence remains limited on three questions for a financial agent acting on an executable banking benchmark: which components of such a defense actually carry its protection, and whether removing a component and suppressing its evidence at test time lead to the same assessment; whether a learned, consequence-aware decision adds value over simple deterministic rules on the same proposed financial calls; and what the measured protection costs in legitimate financial task completion, including against a reference that executes no state-changing call.')
replace('C-GAP1b', 'CHAPTER_01_FINAL', 'Within these limits, the gap this thesis addresses is one of **evidence** (Chapter 2, Section 2.11.5):',
        'Within these limits, the gap this thesis addresses is one of **evidence** (Chapter 2, Sections 2.11.5 and 2.11.7):')
replace_line('R1-3', 'CHAPTER_01_FINAL', 'The aim of this research is to design a runtime evaluation and mitigation framework',
             line_starting('CHAPTER_01_FINAL', 'The aim of this research is to design a runtime evaluation and mitigation framework', 'R1-3') +
             '\n\n*Proposed focus, pending the supervisor\'s confirmation.* Within this aim, the evaluation focuses on one question: whether the framework\'s five-layer organization produces defense in depth, that is, which of its components contribute protection against indirect prompt injection, what that protection costs in legitimate task completion, and how it compares with simple deterministic rules.')
insert_before_line('R1-5', 'CHAPTER_01_FINAL', '**What the thesis demonstrates**',
                   '**Primary empirical contribution.** The thesis examines whether REM\'s five-layer architecture produces defense in depth, rather than assuming that it does. On recorded AgentDojo banking traces, protocol-frozen paired component-level ablations and an exploratory comparison of removal with test-time suppression show that it does so only narrowly. Enforcement and the combined learned scoring-and-decision pathway are each necessary for the measured protection. That protection rests on two evidence families that cover different attack classes: action/provenance evidence, whose removal measurably lowers the withholding of attack calls on one population, and behavioral evidence, which under modelled suppression is the only evidence that stops the credential-change objective. Context detection and the deterministic predicates show no measurable effect. The protection is obtained with low specificity: on the primary population, REM v1.0 completes exactly the benign tasks that withholding every state-changing call completes. All results are replay results on data examined during development.')
replace_line('R1-6a', 'CHAPTER_01_FINAL', '3. **Measured security and its cost.**',
             '3. **Measured security and its cost.** In replay, REM v1.0 reduces attack success from 22.6% to 0.4% on the primary recordings and from 21.1% to 0.15% on the second population. It completes 31% of benign tasks where the undefended agent completes 52%. On the primary recordings, the 105 benign tasks it completes are exactly those completed when every state-changing call is withheld, so in replay it completes no benign task that requires a payment, payment change or credential change. It completes 94 more tasks under attack than that reference and lets 11 attacks through, all in one task whose request names the attacker\'s account. This identity is established on the primary recordings only (Chapter 4, Sections 4.6.3 and 4.6.8).')
replace('C-NEG1', 'CHAPTER_01_FINAL', 'Four are documented (Chapter 5, Section 5.5): behavioral evidence did not help;',
        'Four are documented (Chapter 5, Section 5.5): behavioral evidence, when removed and refitted, did not help (under exploratory test-time suppression it was the only evidence that stopped the credential-change objective; Chapter 4, Section 4.6.12);')
replace_line('R1-6b', 'CHAPTER_01_FINAL', '8. **Pre-registered ablations of the five layers',
             '8. **Protocol-frozen component-level ablations within the layered architecture, and a comparison with existing frameworks (19 to 22 November 2026).** With protocols committed before any arm was scored, on recordings that had been examined during development, the ablations show how REM v1.0\'s protection is produced:\n'
             '   - enforcement and the combined learned pathway (estimator, calibration and expected-loss selection, removed together) are each necessary: without either, attack outcomes return to the no-defense level;\n'
             '   - on the primary population, removing calibration alone changes no attack outcome, and replacing expected-loss selection by consequence-independent thresholds raises successful attacks from 11 to 164;\n'
             '   - removing the action/provenance evidence lowers attack-call withholding measurably on the second population (−9.1 points, 95% interval −23.5 to −0.7) and increases the episodes in which an attack call is executed, while its effect on final attack outcomes is not resolved on any population;\n'
             '   - removing behavioral evidence raises task completion with no measured security change, whereas suppressing it at test time (exploratory) lets the credential-change objective succeed;\n'
             '   - context detection, the predicates and Modify show no measurable effect;\n'
             '   - provenance labelling and the Detection layer\'s classifier could not be ablated (the first is a dependency of later features, the second does not exist), and the context-hygiene step was not exercised by the recorded data.\n\n'
             '   The four defenses distributed with the benchmark are compared descriptively through their authors\' recorded runs. Progent\'s published banking policy, decided by its authors\' code on the same episodes, admits no attack and completes more tasks than REM; its list of permitted recipients is specific to the benchmark. DRIFT and MELON are compared at the level of architecture and code only (Chapter 4, Sections 4.4, 4.5 and 4.6.12).')
replace('A2-ch1', 'CHAPTER_01_FINAL', '- that the tested features establish what the user authorized;',
        '- that the tested features establish what the user authorized, or that REM authorizes actions: it estimates and decides, and holds no representation of what the user permitted (Chapter 3, Section 3.2.2);\n- that the number of layers, or the contributions found by removing them, is by itself evidence of defense in depth;')

# ---- Chapter 2: related work on layered defenses and their evaluation (A7, D-A), new Section 2.11.7
S2117 = '''### 2.11.7 Update of 28 November 2026: Layered Defenses and How Their Layers Are Evaluated (Outside the PRISMA Flow)

*Status of this addition.* The bibliographic records of the works below were verified through Crossref and OpenAlex on 28 November 2026. Their full texts could not be opened from the working environment, so every statement is at abstract level (A), except where Table 2.3 records a full-text (F) or repository (R) reading. No count of the review changes.

**Layered defenses for language-model applications.** Several frameworks protect the text that a model reads or writes. PromptGuard combines input gatekeeping, structured prompt formatting, semantic output validation and response refinement (Alzahrani, 2026). A three-layer framework for retrieval-augmented chatbots screens user input, enforces a provenance-based instruction hierarchy during context assembly so that retrieved content cannot override operator policy, and audits model output; its abstract reports an ablation in which the three layers provide complementary protection (Saleem et al., 2026, preprint). A five-layer framework for local models in air-gapped networks compares a policy-approved initial intent with the trajectory of observed events, including tool calls and their arguments (Jang et al., 2027). Spotlight-Guard layers spotlighting, LLM-based detection and quarantine, and HMAC-based instruction integrity, and reports a component ablation, an adaptive attack and benign-task success (Demirol & Aydoğan, 2026). At the level of their abstracts, none of these works authorizes the arguments of a state-changing financial tool call.

**Layered defenses at the tool-call boundary.** NEXUS chooses among allow, block, request confirmation and request revision by combining deterministic rules, argument-level inspection and a calibrated logistic-regression risk score, and reports a comparison with rule-only intervention selection (Hossain et al., 2026). Progent enforces symbolic privilege policies over tool names and arguments deterministically (T. Shi et al., 2026). Agent-Sentry layers three checks: a classifier over action sequences and argument provenance, a deterministic allow-list over sensitive argument values, and an LLM judge for residual cases (Sequeira et al., 2026). MELON compares the tool calls of the agent with those of a re-execution under a masked user prompt (Zhu, Yang, et al., 2025). CaMeL separates control flow from untrusted data and propagates capabilities (Debenedetti et al., 2025). In the financial domain, AIS separates model inference from execution authority and validates a typed financial intent against mandate, policy and exact economic terms before single-use authority is issued (Gong et al., 2026).

**How layers are evaluated.** Two recent studies of the same group question how the contribution of a layer is measured. A record-level audit of CASCADE, a local layered defense for the Model Context Protocol, reports that the convention by which "review" verdicts are counted, and the construction of the test corpus, determine the headline false-positive rate (Abasıkeleş-Turgut & Gümüş, 2026a). A study of a four-tier gateway for tool calls reports that deleting one stage credits it with contributions that differ by more than an order of magnitude depending on how deletion is defined, whereas substituting constant verdicts shows that the stage can change only a few inputs (Abasıkeleş Turgut & Gümüş, 2026b). Neither concerns financial agents. Both bear directly on how this thesis measures the contribution of REM's components: they are independent evidence that deletion-based ablation of a layered prompt-injection defense can misattribute contributions, which supports, but does not prove, the removal-versus-suppression finding of Chapter 4, Section 4.6.12.

**What this update changes.**
- A component- or layer-level ablation of a layered injection defense is published (Saleem et al., 2026; Demirol & Aydoğan, 2026), as is a comparison of a calibrated risk score with rule-only selection (Hossain et al., 2026). Neither is a gap.
- The methodological point that deletion and substitution of a layer can disagree is published for a tool-call gateway (Abasıkeleş Turgut & Gümüş, 2026b). This thesis does not claim it.
- What remains, at the level read, is narrower: evidence for a financial agent on an executable banking benchmark on which of a layered defense's components carry its protection, whether removing an evidence family and suppressing it at test time agree, and what the protection costs in legitimate financial task completion. The statement of Section 2.11.5 is narrowed accordingly, and Chapter 1, Section 1.4 uses the narrowed wording. It remains proposed wording, pending the supervisor's confirmation.'''
insert_before_line('A7', 'CHAPTER_02_FINAL', '## 2.12 Chapter Summary', S2117)
insert_after_line('C-GAP2', 'CHAPTER_02_FINAL', '**Bounds.** The gap is bounded by the record-level review',
                  '**Further narrowing (28 November 2026).** Layer-level ablations of layered injection defenses and a comparison of a calibrated risk score with rule-only selection are reported at abstract level by later works (Section 2.11.7). The statement above is therefore narrowed in Section 2.11.7 to the evidence on which components carry protection for a financial agent, on removal against test-time suppression, and on the cost in legitimate financial task completion.')
replace('C-GAP3', 'CHAPTER_02_FINAL', 'Only the controlled evaluation, including its negative results, is offered by this thesis.',
        'Only the controlled evaluation, including its negative results, is offered by this thesis. A further update of 28 November 2026 (Section 2.11.7) narrowed the gap to which components of a layered defense carry protection for a financial agent, how removal and test-time suppression compare, and at what cost in legitimate financial task completion.')

# ---- Chapter 3: A1, A2, A3, A4, A5
insert_after_line('A1', 'CHAPTER_03_FINAL', 'Each context segment receives one label from the ordered set trusted',
                  '**Where the trust boundary acts.** The labels are not used to filter or rewrite content. They are consumed by the action evidence x^act^~1~–x^act^~3~, by x^beh^~1~ and, through x^act^~1~, by predicate D2 (Sections 3.6.2 and 3.7.4), which compare the arguments of the proposed call with the trusted, semi-trusted and untrusted segments. REM therefore applies the principle that untrusted content must not acquire the authority of an instruction at the arguments of proposed actions, at boundary TB-3 of Table 3.3, and not during prompt assembly. The same principle appears as a provenance-based instruction hierarchy for retrieval-augmented chatbots (Saleem et al., 2026) and as capabilities attached to values (Debenedetti et al., 2025).')
insert_after_line('A2', 'CHAPTER_03_FINAL', 'The inputs and outputs of each layer are listed in Appendix A.',
                  '**Detection, decision and authorization.** REM estimates whether a proposed call was induced by injected content (Layers 2–4), decides among four verdicts (Layer 4), and enforces the verdict (Layer 5). It does not authorize actions: it holds no representation of what the user permitted beyond whether a key argument of the call also occurs in the user\'s request or in trusted content (x^act^~1~). This distinguishes REM from defenses that enforce deterministic rules or policies on tool arguments, such as Progent (T. Shi et al., 2026), CaMeL (Debenedetti et al., 2025) and the rule component of NEXUS (Hossain et al., 2026), and from the separation of execution authority from model inference proposed for financial agents (Gong et al., 2026). It is also why REM\'s evidence cannot distinguish an authorized payment from an unrequested one whose details appear in the user\'s own words (Chapter 4, Section 4.6.7).')
insert_after_line('A4', 'CHAPTER_03_FINAL', '3. **The feature set is frozen after pilot E0**',
                  '**Dependencies among the evidence families.** The families are not independent inputs. The action features x^act^~1~–x^act^~3~ depend on the provenance labels and entities of Layer 1, and predicate D2 depends on x^act^~1~; x^beh^~1~ depends on those labels and on the Detection Layer\'s indicator x^ctx^~2~. Removing an upstream component therefore also changes the features built on it, which is why the Input & Context layer cannot be ablated on its own (Chapter 4, Section 4.5.4). In the evaluation the families covered different attack classes: the action/provenance evidence carried most of the estimator\'s discrimination, while, under test-time suppression, the behavioral evidence was the only evidence against the credential-change objective, which has no recipient for the action evidence to examine (Chapter 4, Sections 4.5.7 and 4.6.12).')
insert_after_line('A3', 'CHAPTER_03_FINAL', '4. **Retries are observed.**',
                  '**Enforcement point.** The Mitigation Layer is also implemented as an HTTP gateway in front of the tool backend (`rem/deployment/gateway.py`). The agent framework sends each proposed call to the gateway, which runs Layers 1–5 and forwards only released calls; withheld calls never reach the backend. The gateway fails closed: an exception while a call is evaluated withholds the call, and an unknown episode or a malformed request is rejected without executing anything. A deployment simulation that sent the recorded episodes through the gateway to a simulated banking backend reproduced the in-process replay exactly (Chapter 4, Section 4.5.7). The gateway has not been operated with a live agent or a real payment system, and the simulation inherits the non-adaptive assumption of the replay (Section 3.11.9).')
A5 = '''**Table 3.17. Implementation status of the controls of REM v1.0** (I = implemented; E = evaluated with a measured outcome; X = implemented, not exercised by the recorded data; S = specified, not implemented)

| Control | Layer | Status | What the evaluation shows (Chapter 4) |
|---|---|---|---|
| Provenance labels with least-trusted inheritance | Input & Context | I; evaluated only through the features built on it | Not removable on its own (Section 4.5.4) |
| Context hygiene | Input & Context | X | Not exercised (Section 4.5.5) |
| Instruction-pattern indicator x^ctx^~2~ | Detection | I, E | No measurable effect (Section 4.5.7) |
| Injection classifier x^ctx^~1~ | Detection | S | Not available (Section 3.5) |
| Behavioral evidence x^beh^~1~–x^beh^~4~ | Behavioral Analysis | I, E | Removal: lower completion, no measured security change; suppression (exploratory): only evidence against the credential-change objective (Sections 4.5.7, 4.6.12) |
| Action evidence x^act^~1~–x^act^~3~ | Behavioral Analysis | I, E | Carries most of the discrimination; removal lowers attack-call withholding on the second population (Section 4.5.7) |
| Estimator, calibration and expected-loss verdict (learned pathway) | Decision Engine | I, E | Necessary for the measured protection; calibration alone changes no attack outcome (Section 4.5.7) |
| Consequence tiers and costs | Decision Engine | I, E; declared values awaiting approval | Thresholds without tiers admit more attacks and complete more tasks (Section 4.5.7) |
| Predicates D1, D2 | Decision Engine | I, E | No measurable effect (Section 4.5.7) |
| Audit record and linear attribution | Decision Engine (audit only) | I | Attribution never enters the verdict (Section 3.7.6) |
| Step-level withholding (Modify, Escalate, Block) | Mitigation | I, E | Necessary; without it REM equals no defense (Section 4.5.7) |
| Modify mechanism (tool restriction) | Mitigation | I; effect equal to withholding in replay | No distinct effect exercised (Section 4.5.7) |
| HTTP gateway, fail-closed | Mitigation | I; deployment simulation on recorded traffic | Exact parity with the replay (Section 4.5.7) |
| Reviewer for Escalate | Outside REM | Not part of REM; bounded by an idealized reviewer and by no reviewer | Section 4.6.3 |
| Sequential (CUSUM) monitor | Observe-only analysis | I; never in the verdict path | Held-out false-alarm rate above its fitting target (Section 4.6.4) |
| Live, closed-loop enforcement | — | Harness implemented and tested with scripted agents; not executed with a language model | Section S-4.4.4 |'''
insert_before_line('A5', 'CHAPTER_03_FINAL', '**Implementation.** The specification is implemented with one declared absence',
                   'Table 3.17 states the status of every control, so that implemented, evaluated and merely specified controls are not confused.\n\n' + A5)

# ---- Chapter 4: R4-1 ... R4-8, A3 evidence, A6, terminology
replace('R4-1a', 'CHAPTER_04_FINAL', 'The study therefore removes components, not always whole layers:',
        'The study is therefore a **component-level ablation within a layered architecture**: it removes components, not whole layers:')
replace('R4-1b', 'CHAPTER_04_FINAL', '- **Decision Engine:** every component removed separately.',
        '- **Decision Engine:** the learned pathway (estimator, calibration and expected-loss selection) is removed as one block, because no non-predicate verdict exists without the estimator; the estimator is therefore never isolated. On the primary population only, calibration is removed separately, expected-loss selection is replaced by consequence-independent thresholds on the same estimator, and Modify and the predicates are removed separately.')
replace_line('R4-2', 'CHAPTER_04_FINAL', '- *Status:* development evidence, because the primary recordings were used to design and fit REM v1.0.',
             '- *Status and data history:* these are **protocol-frozen paired ablations**, not validations on untouched data. The primary recordings were used to design and fit REM v1.0, and the outcomes of six arms on them had been reported before the protocol of 21 November was frozen; the held-out-template recordings were examined in revision R2; the second population has been development data since the confirmatory run of 11 November 2026. The protocols were committed before any arm was scored (commits `dc8407d` and `93e6630`), and the repository\'s history and hashes support that order.')
replace('R4-3', 'CHAPTER_04_FINAL',
        '- accounts for all 661 attacks that REM v1.0 prevents (of 672 reached without defense).\n\nWhat it does not do',
        '- is necessary for the prevention of 661 of the 672 attacks reached without defense: removing the pathway returns the attack outcomes to the no-defense level, while the predicates alone withhold no attack-labeled call. It is not the sole cause of that prevention: it decides on the action/provenance and behavioral evidence it is given, and it protects nothing without enforcement (Sections 4.5.10 and 4.6.12).\n\nWhat it does not do')
insert_after_line('A3-ch4', 'CHAPTER_04_FINAL', '**Runtime.** REM calls no model.',
                  '**Enforcement through a gateway (deployment simulation of 5 November 2026).** The Mitigation layer is also implemented as a fail-closed HTTP gateway at the tool boundary (Chapter 3, Section 3.8). All 3,334 recorded episodes were sent through it to a simulated banking backend, as recorded traffic without adaptation. For REM, B1 and the no-defense reference, the per-call verdicts and the utility and security outcomes matched the in-process replay in every episode; the backend executed exactly the released calls; malformed and unknown requests were rejected without execution; and the median REM time per call was 0.19 ms (95th percentile 0.40 ms) on four virtual CPUs (`results/deployment_sim/2026-11-05_full/RESULTS.md`). The simulation ran at commit `c30ad8a`, before the last change to `rem/` (commit `7c79883`); its outcomes equal those of the replay reported here, which was re-executed with the current code on 27 November 2026. It simulates enforcement on recorded traffic; it is not an operation with a live agent or a real payment system.')
insert_after_line('A6', 'CHAPTER_04_FINAL', '**A released attack-labeled call is not the same as a committed unauthorized change of the bank state.**',
                  '**Reporting conventions.** The headline numbers of a layered defense depend on how its verdicts are mapped to outcomes and on the population on which they are counted (Abasıkeleş-Turgut & Gümüş, 2026a). Four conventions therefore hold for every number in this chapter. First, Modify, Escalate and Block all withhold the current call, and an escalated call is released only where an idealized reviewer is stated. Second, each number names its population and that population\'s data history (Section 4.2.1). Third, each rate states its denominator: attacked episodes, benign episodes, attack-labeled calls or legitimate state-changing calls. Fourth, each number states which outcome it measures: the benchmark\'s attack outcome in replay, the execution of an attack-labeled call, or call-level withholding. These outcomes need not agree (Section 4.5.7).')
insert_after_line('R4-4', 'CHAPTER_04_FINAL', 'They therefore add probability mass to legitimate calls without separating attacks.',
                  'This is a result of removal and refitting. Suppressing the behavioral family at test time, with everything else fixed, gives a different picture (Section 4.6.12, exploratory): 131 instead of 11 successful attacks, 119 of the 120 additional ones in the only credential-change objective, which has no recipient for the action evidence to examine. After the family is removed, suppressing the action evidence lets 653 attacks succeed, against 90 when the behavioral family is present. Removal and suppression therefore lead to opposite assessments of this family; the suppression is modelled and idealized.')
insert_before_line('R4-5', 'CHAPTER_04_FINAL', '**Table 4.48. Replay ASR by the attacker\'s target action**',
                   '**Benign completion and the withhold-everything reference (primary population only).** A re-analysis of the stored per-episode records of the exploratory evaluation of Section 4.6.12 compares REM v1.0 with a reference arm in which no state-changing call is executed. On the primary population, the 105 benign episodes that REM v1.0 completes are exactly the 105 that the reference completes: no episode differs in either direction. REM v1.0 completes 94 more episodes under attack than the reference (1,083 against 989), and the reference has no successful attack where REM v1.0 has 11, all in user_task_15. In replay, REM v1.0\'s benign completion is therefore the completion attainable without any state change. This was established on the primary population only; no such reference arm exists for the other populations. These are replay quantities, not the performance of an agent that reacts to refusals.')
replace_line('R4-6a', 'CHAPTER_04_FINAL', '| Decision Engine | Learned decision |',
             '| Decision Engine | Learned pathway (estimator, calibration, expected loss; removed as one block) | Necessary for the prevention of 661 of 672 attacks on the primary population, and for nearly all prevention on the others; carries most of the false blocking; not the sole cause (it acts on the evidence below and through enforcement) |')
replace_line('R4-6b', 'CHAPTER_04_FINAL', '| Behavioral Analysis | Behavioral evidence |',
             '| Behavioral Analysis | Behavioral evidence | Removal: lowers completed tasks with no measured security change. Test-time suppression (exploratory): the only evidence that stops the credential-change objective |')
replace_line('R4-6c', 'CHAPTER_04_FINAL', '| Input & Context | – (not isolatable',
             '| Input & Context | Provenance labelling (not removable); hygiene (not exercised) | Contributes through the action/provenance evidence built on its labels: removing that evidence lowers attack-call withholding on the second population (−9.1 points [−23.5, −0.7]); effect on final attack outcomes not resolved |')
replace('R4-6d', 'CHAPTER_04_FINAL',
        '**Which components showed measurable contributions.** On this benchmark, the components that do the work are:\n- the learned decision;\n- its expected-loss rule;\n- the action/provenance evidence, built on the Input & Context labels;\n- enforcement.',
        '**Which components showed measurable contributions.** On this benchmark, protection is produced jointly by enforcement, the learned pathway, and the two evidence families the pathway consumes: action/provenance evidence, built on the Input & Context labels, and, under test-time suppression, behavioral evidence. Context detection, the predicates, calibration and Modify show no measurable effect. The architecture therefore has depth only within the evidence that one decision and one enforcement point use; the Detection layer and the predicates contribute no measured protection, and the Input & Context layer contributes only through the action evidence built on its labels. This is a finding about the evaluated configuration on replayed recordings, not grounds by itself for removing any layer.')
replace('R4-7a', 'CHAPTER_04_FINAL',
        '| 14 | Of REM\'s five layers, the Decision Engine\'s learned decision acting through the Mitigation layer\'s enforcement carries every measured outcome effect; the action/provenance evidence carries the discrimination; behavioral evidence lowers task completion; the Detection layer\'s indicator, the predicates, calibration and Modify have no measurable effect |',
        '| 14 | Of REM\'s five layers, enforcement and the learned pathway are each necessary for the measured outcome effects; the action/provenance evidence carries most of the discrimination and measurably raises attack-call withholding on one population; behavioral evidence lowers task completion when removed but covers one attack class under test-time suppression (exploratory); the Detection layer\'s indicator, the predicates, calibration and Modify have no measurable effect |')
replace('R4-7b', 'CHAPTER_04_FINAL',
        'the Input & Context layer is not isolatable and the injection classifier is absent; no measurable effect is not evidence of no value |',
        'the Input & Context layer is not isolatable and the injection classifier is absent; no measurable effect is not evidence of no value; protocol-frozen, on data examined during development; the estimator is not isolated; suppression is modelled |')
replace_line('R4-8', 'CHAPTER_04_FINAL', '- **Ablation of the five layers (19 and 21 November 2026, pre-registered).**',
             '- **Component-level ablation within the layered architecture (19 and 21 November 2026, protocol-frozen; data examined during development).** Enforcement and the learned pathway (estimator, calibration and expected-loss selection, removed together) are each necessary: without either, attack outcomes return to the no-defense level, and in shadow mode the same verdicts protect nothing. The pathway acts on two evidence families. Removing the action/provenance evidence lowers attack-call withholding on the second population and raises the number of episodes in which an attack call is executed; its effect on final outcomes is not resolved. Removing behavioral evidence raises task completion with no measured security change, but suppressing it at test time lets the credential-change objective succeed (exploratory). The Detection layer\'s indicator, the predicates, calibration and Modify have no measurable effect; provenance labelling could not be removed on its own and the classifier does not exist. On the primary population, the consequence-aware rule admits 153 fewer attacks than consequence-independent thresholds and completes fewer tasks, and REM v1.0\'s benign completions coincide with those of withholding every state-changing call.')

# terminology: "pre-registered" -> wording that the evidence supports (protocols committed before scoring)
TERMS = [
    ('T1', 'CHAPTER_04_FINAL', 'the pre-registered ablations of 19 and 21 November', 'the protocol-frozen ablations of 19 and 21 November'),
    ('T2', 'CHAPTER_04_FINAL', 'The **pre-registered values** are listed in Table 4.4.', 'The **values declared in advance** (committed before any held-out prediction was computed) are listed in Table 4.4.'),
    ('T3', 'CHAPTER_04_FINAL', '**Table 4.4. Pre-registered values**', '**Table 4.4. Values declared in advance**'),
    ('T4', 'CHAPTER_04_FINAL', 'All results above use the pre-registered label rule', 'All results above use the label rule declared in advance'),
    ('T5', 'CHAPTER_04_FINAL', 'The following report is that of the pre-registered study of 19 November 2026.', 'The following report is that of the protocol-frozen study of 19 November 2026.'),
    ('T6', 'CHAPTER_04_FINAL', 'Each study pre-registered its rules, but all used development data', 'Each study committed its rules before scoring, but all used development data'),
    ('T7', 'CHAPTER_04_FINAL', 'where the pre-registered costs put the Allow–Block indifference points', 'where the declared costs put the Allow–Block indifference points'),
    ('T8', 'CHAPTER_04_FINAL', 'because the pre-registered α~mod~ = 0.05 must exceed α~blk~', 'because the declared α~mod~ = 0.05 must exceed α~blk~'),
    ('T9', 'CHAPTER_03_FINAL', 'A separately pre-registered study (Chapter 4, Section 4.5.7)', 'A separate protocol-frozen study (Chapter 4, Section 4.5.7)'),
    ('T10', 'APPENDICES_FINAL', 'NO-GO under its own pre-registered rules', 'NO-GO under its own rules, committed before scoring'),
]
for eid, f, a, b in TERMS:
    replace(eid, f, a, b)

# ---- Chapter 5
replace('C5-1', 'CHAPTER_05_FINAL', 'pre-registered ablations of the five layers with paired intervals on three populations',
        'protocol-frozen component-level ablations within the five-layer architecture, with paired intervals on three populations')
replace('C5-2', 'CHAPTER_05_FINAL', 'the learned decision accounts for all 661 prevented attacks (of 672 reached without defense)',
        'the learned pathway is necessary for the prevention of 661 of the 672 attacks reached without defense')
replace('C5-3', 'CHAPTER_05_FINAL',
        'Across the five layers, every measured outcome effect comes from the Decision Engine\'s learned decision acting through the Mitigation layer\'s enforcement: in shadow mode the same verdicts protect nothing.',
        'Across the five layers, protection is produced jointly: enforcement and the learned pathway are each necessary, and the pathway acts on two evidence families that cover different attack classes (action/provenance evidence and, under test-time suppression, behavioral evidence); in shadow mode the same verdicts protect nothing.')
replace('C5-4', 'CHAPTER_05_FINAL', 'Behavioral evidence lowered task completion with no measured security benefit;',
        'Behavioral evidence, when removed and refitted, lowered task completion with no measured security benefit (under exploratory test-time suppression it was the only evidence that stopped the credential-change objective);')
replace('C5-5', 'CHAPTER_05_FINAL', '| 9. A pre-registered final ablation of REM v1.0', '| 9. A protocol-frozen final ablation of REM v1.0')
replace('C5-6', 'CHAPTER_05_FINAL', '| 10. A layer-to-implementation mapping and a component-level ablation of the five-layer design,',
        '| 10. A layer-to-implementation mapping and a protocol-frozen component-level ablation within the five-layer architecture,')
replace('C5-7', 'CHAPTER_05_FINAL', '| Every outcome effect from the learned decision acting through enforcement (shadow mode equals no defense);',
        '| Enforcement and the learned pathway each necessary (shadow mode equals no defense), with protection produced jointly with the two evidence families the pathway consumes;')
replace('C5-8', 'CHAPTER_05_FINAL', 'Two pre-registered ablations settle where REM v1.0\'s own protection comes from.',
        'Two protocol-frozen ablations show where REM v1.0\'s own protection comes from.')
replace('C5-9', 'CHAPTER_05_FINAL', 'it decides almost every call and accounts for all 661 attacks that REM v1.0 stops (of 672 reached without defense), with none admitted.',
        'it decides almost every call and is necessary for the prevention of 661 of the 672 attacks reached without defense, with none admitted.')
replace('C5-10', 'CHAPTER_05_FINAL', 'Across the five layers, every measured outcome effect comes from that decision acting through enforcement.',
        'Across the five layers, that protection is produced jointly by enforcement, the learned pathway and the two evidence families it consumes; on the primary population, REM v1.0 completes exactly the benign tasks that withholding every state-changing call completes.')
replace('C5-11', 'CHAPTER_05_FINAL', '9. **Literature.** The systematic review was conducted at record level.',
        '9. **Literature.** The systematic review was conducted at record level. The layered and authorization-based works added on 27 and 28 November 2026 (Chapter 2, Sections 2.11.6 and 2.11.7) are known only from their abstracts and bibliographic records; their full texts could not be opened from the working environment.')
FW = '''15. **Field-level provenance.** Record the source field of every value in a tool output, so that a typed bank field and a free-text field are not treated alike, and evaluate the effect by paired replay on the existing populations.
16. **Economic limits.** Add per-call, per-payee and cumulative limits, evaluated on financial scenarios that the benchmark does not contain (amount escalation to a trusted recipient, split transfers). The limit values are a supervisor decision.
17. **Component reachability by substitution.** Test whether each component's verdicts can reach an outcome by replacing them with constant verdicts, in addition to removing the component (Abasıkeleş Turgut & Gümüş, 2026b). Table 4.34 reports this for the learned decision only.'''
insert_after_line('FW', 'CHAPTER_05_FINAL', '14. **REM-DiD under adaptive attack.**', FW)

# ---- abstracts (same corrections as Chapters 1 and 4)
replace('AB-1', 'abstract_en', 'and only 33 of 178 legitimate state-changing calls were released.',
        'and only 33 of 178 legitimate state-changing calls were released. On these episodes the benign tasks it completed were exactly those completed when every state-changing call is withheld.')
replace('AB-2', 'abstract_en', 'showed with paired intervals that the learned decision accounts for all 661 attacks that REM stops (672 succeed without any defense) and admits none.',
        'showed with paired intervals that the learned decision is necessary for the prevention of 661 of the 672 attacks that succeed without any defense, and admits none.')
replace('AB-3', 'abstract_en', 'Every outcome effect came from the learned decision acting through enforcement: in shadow mode the same verdicts protected nothing. Removing the action/provenance evidence let more attack calls execute,',
        'Enforcement and the learned decision were each necessary, and the decision acted on two evidence families that covered different attack classes: in shadow mode the same verdicts protected nothing, removing the action/provenance evidence let more attack calls execute, and suppressing the behavioral evidence at test time (exploratory) let the credential-change objective succeed,')
replace('AB-4', 'abstract_en', 'A final ablation, committed before scoring,', 'A final ablation, with its protocol committed before scoring,')
replace('AB-5', 'abstract_ar', 'أن القرار المتعلَّم مسؤول عن منع جميع الهجمات الـ661 التي يوقفها الإطار (من أصل 672 هجوماً تنجح دون أي دفاع)',
        'أن القرار المتعلَّم ضروري لمنع 661 من أصل 672 هجوماً تنجح دون أي دفاع')
replace('AB-6', 'abstract_ar', 'أن كل أثر مقيس في النتائج يأتي من القرار المتعلَّم وهو يعمل من خلال التنفيذ في طبقة التخفيف.',
        'أن التنفيذ في طبقة التخفيف والقرار المتعلَّم ضروريان كلاهما، وأن القرار يعتمد على عائلتين من الأدلة تغطيان فئتين مختلفتين من الهجمات؛ إذ أدّى كبت الأدلة السلوكية وقت الاختبار (تحليل استكشافي) إلى نجاح هدف تغيير بيانات الاعتماد.')

# ---- references: DiD additions (M5) and the works cited by the new text (all verified 28 Nov 2026, see 09)
NEW_REFS += [
    'Abasıkeleş-Turgut, İ., & Gümüş, E. (2026a). *Evaluating a layered prompt-injection defence for the Model Context Protocol: A record-level audit of decision conventions, corpus provenance and reproducibility* (arXiv:2604.17125) [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2604.17125 [Abstract only; an audit of CASCADE, not CASCADE\'s own paper]',
    'Abasıkeleş Turgut, İ., & Gümüş, E. (2026b). *Deletion is not substitution: Component attribution in a layered prompt-injection gateway for LLM tool calls* (arXiv:2610.33198) [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2610.33198 [Abstract only]',
    'Alzahrani, A. (2026). PromptGuard a structured framework for injection resilient language models. *Scientific Reports, 16*, 1277. https://doi.org/10.1038/s41598-025-31086-y [Abstract and Crossref record only; title as registered by Crossref]',
    'Demirol, D., & Aydoğan, M. (2026). Balancing security and performance in LLM agents: Spotlight-Guard, a layered defense against indirect prompt injection. *Applied Sciences, 16*(15), 7662. https://doi.org/10.3390/app16157662 [Abstract only]',
    'Jang, S., Lee, M., & Shon, T. (2027). Intelligent multilayer defense-in-depth framework for securing local LLMs in air-gapped networks. *Computers, Materials & Continua, 90*(1), 1–10. https://doi.org/10.32604/cmc.2026.090355 [Abstract and Crossref record only; online first in 2026, issue year 2027]',
    'Saleem, G., Ahmed, N., Zaman, M. I., et al. (2026). *A layered security framework against prompt injection in RAG-based chatbots* (arXiv:2606.19660) [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2606.19660 [Abstract only; author list abbreviated from the index record. A journal DOI (10.62762/TISC.2026.712476) is not registered with Crossref and is not cited]',
]
def key(e):
    import unicodedata
    return unicodedata.normalize('NFKD', e).encode('ascii', 'ignore').decode().lower()


blocks = get('REF').split('\n\n')
for r in NEW_REFS:
    if r in blocks:
        continue
    # insert at its alphabetical position among the entries; existing blocks (heading, note) are never moved
    pos = next((i for i, b in enumerate(blocks) if b.strip()[:1].isalpha() and not b.startswith('#') and key(b) > key(r)), len(blocks))
    blocks.insert(pos, r)
    LOG.append({'id': 'REF+', 'file': 'REFERENCES_FINAL', 'kind': 'add_reference', 'old_chars': 0, 'new_chars': len(r), 'entry': r[:90]})
F['REF'] = '\n\n'.join(blocks)

# ---------------------------------------------------------------------------------------------- 3. write and check
for name, text in F.items():
    open(path(name), 'w', encoding='utf-8').write(text)
for bad in ('accounts for all 661', 'every measured outcome effect comes from', 'pre-registered', 'Pre-registered',
            'REM-DiD reaches Defense-in-Depth'):
    for name in [f for f in os.listdir(os.path.join(WC, 'src'))] :
        t = open(os.path.join(WC, 'src', name), encoding='utf-8').read()
        if bad in t:
            sys.exit(f'residual phrase {bad!r} in {name}')
json.dump({'edits': LOG, 'n_edits': len(LOG)}, open(os.path.join(WC, 'audit', 'edit_log.json'), 'w'), indent=1, ensure_ascii=False)
print('applied', len(LOG), 'edits; new references', sum(1 for x in LOG if x['id'] == 'REF+'))
