"""R4 corrections (independent review of 1 Nov 2026) applied to the R3 chapters.

usage: python3 REM_FINAL_THESIS/tools/make_r4.py   (from the repository root, after make_r3.py)

Reads   REM_FINAL_THESIS/chapters/*            (R3 output of make_r3.py; left unchanged)
Writes  REM_FINAL_THESIS/chapters_R4/*_R4.md   and reports/CHANGE_LOG_R4.md
Every number inserted here is read from a result file at run time:
  analytical values  results/pilot_R2/   (the reported result set; R4 re-run reproduces it, see reports)
  complete-call time results/pilot_R4/   (R4 re-run with the added complete-call timer)
  test counts        REM_FINAL_THESIS/verification/pytest_per_file_R4.txt
Each replacement must match exactly once, or the script stops.
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'REM_FINAL_THESIS', 'chapters')
DST = os.path.join(ROOT, 'REM_FINAL_THESIS', 'chapters_R4')
R2 = os.path.join(ROOT, 'results', 'pilot_R2')
R4 = os.path.join(ROOT, 'results', 'pilot_R4')
os.makedirs(DST, exist_ok=True)

NAMES = {0: 'FRONT_MATTER', 1: 'CHAPTER1_INTRODUCTION', 2: 'CHAPTER2_LITERATURE_REVIEW', 3: 'CHAPTER3_METHODOLOGY',
         4: 'CHAPTER4_IMPLEMENTATION', 5: 'CHAPTER5_RESULTS', 6: 'CHAPTER6_DISCUSSION_CONCLUSION', 7: 'REFERENCES'}
SRCFILE = {k: (v if k in (0, 7) else v + '_FINAL') + '.md' for k, v in NAMES.items()}
text = {k: open(os.path.join(SRC, f), encoding='utf-8').read() for k, f in SRCFILE.items()}
log = []


def rep(ch, old, new, tag, why, count=1):
    n = text[ch].count(old)
    if n != count:
        sys.exit(f'[{NAMES[ch]} {tag}] expected {count} match(es), found {n}: {old[:100]!r}')
    text[ch] = text[ch].replace(old, new)
    log.append((NAMES[ch], tag, why))


def load(d, f):
    return json.load(open(os.path.join(d, f), encoding='utf-8'))


def f3(x):
    return f'{x:.3f}'.replace('-', '−')


def ci(v):
    return f'{v[0]:.3f} [{v[1]:.3f}, {v[2]:.3f}]'


def ms(x):
    return f'{x:.2f}'


REPLAY = load(R2, 'e4_e5_enforcement_replay.json')['configs']
REPLAY4 = load(R4, 'e4_e5_enforcement_replay.json')['configs']
TESTS = {}
for line in open(os.path.join(ROOT, 'REM_FINAL_THESIS', 'verification', 'pytest_per_file_R4.txt'), encoding='utf-8'):
    m = re.match(r'^(\S+\.py)\s+(\d+)$', line.strip())
    if m:
        TESTS[m.group(1)] = int(m.group(2))
NTEST = sum(TESTS.values())

# ---------------------------------------------------------------- timing summary from the R4 re-run
REMCFG = sorted(k for k in REPLAY4 if k.startswith(('REM_', 'REMnoEsc_')))
part_med = [REPLAY4[k]['latency_ms_median'] for k in REMCFG]
part_p95 = [REPLAY4[k]['latency_ms_p95'] for k in REMCFG]
full_med = [REPLAY4[k]['latency_full_ms_median'] for k in REMCFG]
full_p95 = [REPLAY4[k]['latency_full_ms_p95'] for k in REMCFG]
nsteps = sorted({REPLAY4[k]['latency_steps'] for k in REMCFG})
rng = lambda v: f'{ms(min(v))}–{ms(max(v))} ms'
NSTEP = f'{nsteps[0]:,}' if len(nsteps) == 1 else f'{nsteps[0]:,}–{nsteps[-1]:,}'
TIMING = {'cfgs': len(REMCFG), 'part_med': rng(part_med), 'part_p95': rng(part_p95),
          'full_med': rng(full_med), 'full_p95': rng(full_p95), 'nsteps': NSTEP}

# ================================================================ Finding 1: mitigation semantics
rep(3, 'Under the replay of Section 3.11.11 the two cannot differ, because a non-adaptive agent never retries a refused tool; distinguishing them requires live, adaptive agents.',
    'The two semantics can release different actions even when the agent never retries a call or adapts: under the episode-level variant, Block adds every tool of 𝒯~R~ to the restriction set S, and Modify adds the tool class of a~t~, so a later, *different* state-changing call is refused even when its own verdict is Allow. They therefore give different results under the replay of Section 3.11.11 (Chapter 5, Table 5.11). Live, adaptive agents would add further differences, through retries and alternative routes.',
    '§3.8 semantics', 'Removes the false claim that the two semantics cannot differ under replay (review Finding 1).')
rep(4, 'Under the replay used in Chapter 5, the two semantics cannot differ, because a non-adaptive agent does not retry.',
    'The two semantics can differ without any retry: an episode-level Block refuses every later call to a tool in 𝒯~R~, including a call whose own verdict is Allow. `tests/test_mitigation_semantics.py` checks this on a fixed sequence: Block `send_money`, then Allow `update_password`; the second call is released under step-level semantics and refused under episode-level semantics. Chapter 5 (Table 5.11) reports the replay results of both semantics.',
    '§4.8 semantics', 'Same correction in Chapter 4; names the deterministic regression test (review Finding 1).')
rep(5, '- **Modify and Block.** Under NO-ADAPT, Modify and Block have the same effect on the withheld call, and step-level and episode-level semantics cannot differ, because no refused tool is retried. The replay results are identical for the two semantics; only step-level results are shown.',
    '- **Mitigation semantics.** Under step-level semantics, Modify and Block have the same effect on the withheld call. The episode-level variant also restricts later calls: after a Block, every later call to a tool in 𝒯~R~ is refused, even one whose own verdict is Allow, and even though the agent never retries. The two semantics therefore give different replay results. Tables 5.7–5.10 use step-level semantics, the declared reference pending decision D-2; Table 5.11 compares both semantics.',
    '§5.6 semantics', 'Removes the false statement that the replay results are identical for the two semantics (review Finding 1).')
rep(6, 'and distinguishes step-level from episode-level semantics.',
    'and shows how the two mitigation semantics differ once the agent can react to refusals; in replay they already differ, because episode-level restrictions also refuse later, different calls (Chapter 5, Table 5.11).',
    '§6.6 semantics', 'The two semantics are not distinguishable only with live agents (review Finding 1).')

# Chapter 5: renumber Tables 5.11 → 5.12 and 5.12 → 5.13, then insert the semantics table as 5.11
for old, new in (('Table 5.12', 'Table 5.13'), ('Table 5.11', 'Table 5.12')):
    n = text[5].count(old)
    text[5] = text[5].replace(old, new)
    log.append((NAMES[5], f'renumber {old}', f'{n} occurrence(s) → {new}, to make room for the new Table 5.11.'))

rows = []
for cfg, label in (('B1', 'B1'), ('REM', 'REM'), ('REMnoEsc', 'REM w/o Esc.')):
    for rev, rlabel in (('no_reviewer', 'no reviewer'), ('idealized', 'idealized reviewer')):
        for sem, slabel in (('step_level', 'step-level (ref.)'), ('episode_level', 'episode-level')):
            v = REPLAY[f'{cfg}_{sem}_{rev}']
            rows.append(f'| {label}, {rlabel} | {slabel} | {ci(v["ASR"])} | {ci(v["benign_utility"])} | {ci(v["utility_under_attack"])} |')
b1s, b1e = REPLAY['B1_step_level_no_reviewer'], REPLAY['B1_episode_level_no_reviewer']
rs, re_ = REPLAY['REM_step_level_no_reviewer'], REPLAY['REM_episode_level_no_reviewer']
ns, ne = REPLAY['REMnoEsc_step_level_no_reviewer'], REPLAY['REMnoEsc_episode_level_no_reviewer']
bu_equal = all(REPLAY[f'{c}_step_level_{r}']['benign_utility'] == REPLAY[f'{c}_episode_level_{r}']['benign_utility']
               for c in ('B1', 'REM', 'REMnoEsc') for r in ('no_reviewer', 'idealized'))
ua_lower = all(REPLAY[f'{c}_episode_level_{r}']['utility_under_attack'][0] <= REPLAY[f'{c}_step_level_{r}']['utility_under_attack'][0]
               for c in ('B1', 'REM', 'REMnoEsc') for r in ('no_reviewer', 'idealized'))
assert bu_equal and ua_lower, 'the prose below states both observations; re-check the data'
d_ep = re_['ASR'][0] - b1e['ASR'][0]
SAME = 'identical' if rs['ASR'][0] == re_['ASR'][0] else 'equal to three decimals'
PAIRED = load(R2, 'e4_e5_enforcement_replay.json')['paired_differences']
PD_S = PAIRED['REM_step_level_no_reviewer_minus_B1_step_level_no_reviewer']['ASR']
PD_E = PAIRED['REM_episode_level_no_reviewer_minus_B1_episode_level_no_reviewer']['ASR']
PD_EI = PAIRED['REM_episode_level_idealized_minus_B1_episode_level_idealized']['ASR']
assert [round(x, 3) for x in PD_E] == [round(x, 3) for x in PD_EI], 'the prose says the idealized-reviewer interval is the same'
VR_S, VR_E = rs['verdict_rates']['0'], re_['verdict_rates']['0']
VI_S, VI_E = REPLAY['REM_step_level_idealized']['verdict_rates']['0'], REPLAY['REM_episode_level_idealized']['verdict_rates']['0']
B1_SAME = REPLAY['B1_step_level_no_reviewer']['verdict_rates'] == REPLAY['B1_episode_level_no_reviewer']['verdict_rates']
assert VR_S != VR_E and B1_SAME, 'the prose below states that REM verdict counts differ and B1 counts do not'
cii = lambda v: f'{f3(v[0])} [{f3(v[1])}, {f3(v[2])}]'
SEM_TABLE = (
    '\n#### Sensitivity to the mitigation semantics\n\n'
    '**Table 5.11. Replay results under the two mitigation semantics** (same episodes; same estimator, calibration, costs, predicates and thresholds; '
    'matching reviewer treatment for REM and B1; only the mitigation semantics varies. Verdict sequences are not fixed: see the notes below. '
    'ref. = the reference semantics; REM w/o Esc. = REM without expected-loss Escalate; '
    'attacked n = 2,979; benign n = 334; `e4_e5_enforcement_replay.json`, `configs.<configuration>_<semantics>_<reviewer>`)\n\n'
    '| Configuration | Semantics | ASR | Benign utility | Utility under attack |\n|---|---|---|---|---|\n' + '\n'.join(rows) + '\n\n'
    'What is fixed and what differs, within NO-ADAPT:\n'
    '- **What is fixed and what varies.** Both runs of each configuration use the same recorded episodes, the same fitted parameters, costs, predicates and thresholds, and the same reviewer treatment. They differ in the mitigation semantics: under the episode-level variant, an earlier Block or Modify adds tools to a restriction set that refuses later calls.\n'
    f'- **The verdicts are not identical.** For REM without a reviewer, the y = 0 steps received {VR_S["modify"]:,} Modify and {VR_S["escalate"]:,} Escalate verdicts under step-level semantics, against {VR_E["modify"]:,} and {VR_E["escalate"]:,} under episode-level semantics (`verdict_rates` of the two REM configurations). With the idealized reviewer the counts are {VI_S["modify"]:,} / {VI_S["escalate"]:,} against {VI_E["modify"]:,} / {VI_E["escalate"]:,}. A call refused only under the episode-level variant returns no tool output, so the evidence for later steps can differ. B1\'s verdict counts are the same under both semantics.\n'
    f'- **B1\'s ASR is lower under episode-level semantics** ({f3(b1s["ASR"][0])} → {f3(b1e["ASR"][0])}): later state-changing calls are refused by the restriction set left by an earlier Block or Modify. REM\'s ASR is {SAME} ({f3(rs["ASR"][0])}). REM without expected-loss Escalate changes from {f3(ns["ASR"][0])} to {f3(ne["ASR"][0])} (unrounded {ns["ASR"][0]:.4f} → {ne["ASR"][0]:.4f}).\n'
    '- **Utility under attack is lower or equal under episode-level semantics** in every configuration: the restriction set also refuses legitimate later calls.\n'
    '- **Benign utility coincides** between the two semantics in every configuration of this replay. This is an observation about these episodes, not a property of the semantics.\n'
    f'- **REM − B1 ASR within each semantics** (paired grouped bootstrap, no reviewer): {cii(PD_S)} under step-level semantics (Table 5.8) and {cii(PD_E)} under episode-level semantics (`paired_differences`, episode-level REM − B1 entry). The idealized-reviewer interval under episode-level semantics is the same to three decimals. These are two within-semantics contrasts. No interval was computed for the difference between them, so none is reported. As for every interval in this chapter, the bootstrap over nine attacked groups need not reach nominal coverage, and no hypothesis test is based on these intervals (Section 5.2).\n\n'
    'Step-level semantics remains the declared reference (Chapter 3, Section 3.8), pending the supervisor\'s decision D-2. The episode-level rows are a sensitivity analysis, not a replacement for Tables 5.7–5.10.\n')
rep(5, '\n**RQ3 quantities:**', SEM_TABLE + '\n**RQ3 quantities:**', 'new Table 5.11',
    'Adds the compact table of both semantics from the stored results, with matched reviewer assumptions for REM and B1 (review Finding 1); caption states what is fixed and what varies, and reports the existing episode-level paired interval (independent check, Findings 3–4).')
rep(5, 'In replay, REM\'s ASR was lower than B1\'s (mostly credential and payment attacks)',
    'In replay, REM\'s ASR was lower than B1\'s under both mitigation semantics (mostly credential and payment attacks; Table 5.11)',
    'Table 5.13 RQ2', 'Summary states that the comparison holds under both semantics, with the table reference.')
rep(6, 'ΔASR −0.051 [−0.130, −0.007]; Δbenign utility −0.195 without a reviewer and +0.003 with an oracle reviewer (Section 5.6)',
    f'ΔASR −0.051 [−0.130, −0.007] under step-level semantics and {cii(PD_E)} under the episode-level variant (each a within-semantics paired interval); Δbenign utility −0.195 without a reviewer and +0.003 with an oracle reviewer (Section 5.6, Tables 5.8 and 5.11)',
    'Table 6.1 row 5', 'Conclusion reports the step-level result as the reference and the existing episode-level paired interval (independent check, Finding 4).')
rep(0, 'REM\'s attack success rate was 0.004, against 0.055 for the baseline.',
    f'REM\'s attack success rate was 0.004, against 0.055 for the baseline (step-level mitigation; {f3(b1e["ASR"][0])} for the baseline under the episode-level variant).',
    'abstract semantics', 'The abstract names the semantics of the quoted replay numbers.')

# ================================================================ Finding 2: timing boundaries
OLD_414 = text[4][text[4].index('## 4.14 Runtime Measurement'):text[4].index('## 4.15 Chapter Summary')]
NEW_414 = f'''## 4.14 Runtime Measurement

Two timers are recorded for every step. Both start with `time.perf_counter` at the entry of `RemGuard.evaluate`. They differ in where they stop (Table 4.8).

**Table 4.8. Boundaries of the two timers**

| Work inside `RemGuard.evaluate` | Partial timer `rem_latency_ms` (R1–R4) | Complete-call timer `rem_latency_full_ms` (R4) |
|---|---|---|
| Feature computation (Layers 1–3) | Included | Included |
| Tier, reference-label lookup, scoring and calibration | Included | Included |
| Predicates, verdict and mitigation decision | Included | Included |
| Linear attribution and additivity check | **Excluded** | Included |
| Audit-record construction, including the argument digest | **Excluded** | Included |
| Recording the proposal in the episode history | **Excluded** | Included |

Both timers **exclude**:
- LLM inference (absent in replay);
- tool execution and benchmark environment set-up;
- the benchmark pipeline's own overhead;
- the call into and return from `evaluate`.

Both **include** the reference-label lookup. This is evaluation bookkeeping, which a deployment would not perform: it computes the evaluation label recorded in the audit record and used by the idealized reviewer.

**Correction.** Revision R3 stated that the measured interval included attribution and audit-record construction. It did not: the timer of R1–R3 stopped before them. All R1–R3 timing values are partial-timer values. The complete-call timer was added in R4 without changing the partial timer. `tests/test_latency_instrumentation.py` checks both boundaries with a fake clock and an ordered event log, not with wall-clock thresholds.

**Conditions.** Measurements were taken in four parallel worker processes on a 4-vCPU container, so they include contention between workers, and they vary between runs (Section 4.11.2). The R4 run used an Intel Xeon @ 2.80 GHz with Python 3.11.17 and NumPy 2.4.6. Memory is a separate measurement: the peak allocation traced by `tracemalloc` around the complete `RemGuard.evaluate` call, on 300 episodes with the episode-level variant.

These figures describe the evaluated configuration: no injection classifier, no reviewer, and Python on this hardware. They do not describe a deployment that includes a neural classifier or a human review step.

'''
rep(4, OLD_414, NEW_414, '§4.14 timers', 'States the actual boundaries of the partial timer, adds the complete-call timer and its test (review Finding 2).')
rep(5, '- **Processing time.** REM\'s processing time per step, measured as described in Chapter 4, Section 4.14, had a median of 0.14–0.20 ms and a 95th percentile of 0.39–0.54 ms across REM configurations and the two runs; the independent re-execution of 30 October gave values within these ranges for REM configurations.',
    f'- **Processing time** (Chapter 4, Section 4.14, Table 4.8). **Complete call** (R4 re-execution, 1 November 2026; `results/pilot_R4/e4_e5_enforcement_replay.json`, `latency_full_ms_*`): median {TIMING["full_med"]} and 95th percentile {TIMING["full_p95"]} per step, across the {TIMING["cfgs"]} REM configurations ({TIMING["nsteps"]} steps each). **Partial timer**, which excludes attribution, audit-record construction and history recording: median {TIMING["part_med"]} and 95th percentile {TIMING["part_p95"]} in the same run. Earlier runs measured only the partial timer: median 0.14–0.20 ms and 95th percentile 0.39–0.54 ms (R1, R2), with the 30 October re-execution within these ranges.',
    '§5.6 processing time', 'Reports the measured complete-call timing and labels the earlier values as partial (review Finding 2).')
rep(5, 'REM processing below 0.6 ms per step at p95 in this configuration',
    f'REM complete-call processing per step: median {TIMING["full_med"]}, 95th percentile {TIMING["full_p95"]} in this configuration (R4); earlier values are partial',
    'Table 5.13 RQ3', 'Summary uses the complete-call measurement (review Finding 2).')

MEM2, MEM4 = load(R2, 'latency_memory_profile.json'), load(R4, 'latency_memory_profile.json')
rep(5, 'The independent re-execution of 30 October measured the same value.',
    f'The independent re-execution of 30 October measured the same value. In the R4 re-execution, where `evaluate` also records the complete-call timer, the median was {MEM4["peak_bytes_per_step_median"]:,.0f} bytes against {MEM2["peak_bytes_per_step_median"]:,.0f} bytes, with the same 95th percentile ({MEM4["peak_bytes_per_step_p95"]:,.1f} bytes; `results/pilot_R4/latency_memory_profile.json`). The memory boundary is the complete `evaluate` call in both.',
    '§5.6 memory R4', 'Reports the R4 memory value exactly instead of claiming reproduction.')

# ================================================================ other review items
rep(5, 'An independent re-execution on 30 October 2026 reproduced every analytical value; only time and memory measurements differed (Chapter 4, Section 4.11.2).',
    'An independent re-execution on 30 October 2026 reproduced every analytical value; the only differing values were per-step latency values, code-commit stamps and one file path, and no memory value differed (Chapter 4, Section 4.11.2). A further re-execution on 1 November 2026 (R4), which added the complete-call timer, is compared in the same section.',
    '§5.1 reproduction wording', 'Harmonizes with the comparison record (review, smaller corrections).')
rep(3, 'At each step, REM executes Layer 1, then Layers 2 and 3 in parallel on Layer 1\'s output, then Layer 4, then Layer 5, before the proposed action is released to the environment. The Detection and Behavioral Analysis Layers compute their evidence independently;',
    'At each step, REM executes Layer 1; then Layers 2 and 3, each computing its evidence from Layer 1\'s output without using the other\'s; then Layer 4; then Layer 5, before the proposed action is released to the environment. Layers 2 and 3 are independent computations, not concurrent ones: the implementation evaluates them one after the other in the same process (Chapter 4). They share the declared instruction-pattern set as a resource, not each other\'s output. The Detection and Behavioral Analysis Layers compute their evidence independently;',
    '§3.2.2 topology', 'Distinguishes independent computation from concurrent execution (review, smaller corrections).')
rep(3, 'results/pilot_R2/figures/fig_architecture.png', 'results/pilot_R4/figures/fig_architecture.png', 'Figure 3.1 file',
    'Redrawn figure: Layers 2 and 3 as independent branches from Layer 1 into Layer 4; no EXPLORATORY stamp on the design diagram.')

# tests and the R4 re-execution
T45 = text[4][text[4].index('**Table 4.5.'):text[4].index('\n\n', text[4].index('| `test_replay.py`'))]
rep(4, T45, T45.replace(
    '**Table 4.5. Test suite (executed on 28 Oct 2026: 193 passed with AgentDojo installed; 189 passed and 1 module skipped without it)**',
    f'**Table 4.5. Test suite (executed on 1 Nov 2026: {NTEST} passed with AgentDojo installed; log `verification/pytest_R4.txt`)**')
    + f'\n| `test_mitigation_semantics.py` | {TESTS["test_mitigation_semantics.py"]} | Step-level and episode-level policies on a fixed sequence (Block `send_money`, then Allow `update_password`): different release outcomes, neither policy altered (added in R4) |'
    + f'\n| `test_latency_instrumentation.py` | {TESTS["test_latency_instrumentation.py"]} | Fake-clock check that the partial timer stops before attribution, audit construction and history recording, and the complete-call timer after them (added in R4) |'
    + f'\n| `test_docx_tables.py` | {TESTS["test_docx_tables.py"]} | Thesis build tooling, not REM: the Word table transformation keeps exactly one run-property container per run, preserves hyperlinks and equations, and is idempotent (added in R4) |',
    'Table 4.5', 'Updates the test count from the R4 log and lists the three R4 test files.')
rep(4, 'The software is verified by 193 tests', f'The software is verified by {NTEST} tests', '§4.15 tests', 'Test count from the R4 log.')
rep(6, 'Chapters 3–4; 193 tests.', f'Chapters 3–4; {NTEST} tests.', '§6.4 tests', 'Test count from the R4 log.')
rep(0, 'verified by 193 automated tests', f'verified by {NTEST} automated tests', 'abstract tests', 'Test count from the R4 log.')
CMP = json.load(open(os.path.join(ROOT, 'REM_FINAL_THESIS', 'verification', 'reproduction_comparison_R4.json'), encoding='utf-8'))
T = CMP['totals']
rep(4, '| Code version of the reported results |',
    '| Re-execution with the complete-call timer (R4) | 1 Nov 2026, branch `claude/rem-r4-corrections-3ktvze`, Python 3.11.17, NumPy 2.4.6, AgentDojo 0.1.35, Intel Xeon @ 2.80 GHz, 4 vCPU; results in `results/pilot_R4/`; see Section 4.11.2 |\n| Code version of the reported results |',
    'Table 4.1 R4 row', 'Records the environment of the R4 re-execution.')
rep(4, '- **Attribution additivity.**',
    f'- **Re-execution with the complete-call timer (R4, 1 November 2026).** After the timer was added, the complete pipeline was executed again into `results/pilot_R4/`. Of the {T["shared"]:,} numeric values it shares with `results/pilot_R2/`, {T["equal"]:,} were identical, {T["diff_volatile"]:,} were latency, commit or file-path values, and {T["diff_analytical"]} analytical values differed. The new complete-call fields have no R2 counterpart. Every differing value is listed in `verification/reproduction_all_differences_R4.json`.\n- **Attribution additivity.**',
    '§4.11.2 R4 re-run', 'Reports the R4 re-execution against the reported result set.')

# label-audit package description (sampling code: 30 drawn episodes, items only for episodes with proposed calls)
AUD = json.load(open(os.path.join(ROOT, 'REM_FINAL_THESIS', 'verification', 'label_audit_package_check_R4.json'), encoding='utf-8'))
rep(5, '  - a random sample of 30 attacked episodes;',
    f'  - every proposed call of {AUD["random_drawn"]} randomly drawn attacked episodes ({AUD["random_items"]} items; {AUD["random_drawn"] - AUD["random_with_steps"]} of the drawn episodes contain no proposed tool call);',
    '§5.10 audit package', 'States how the 70 random-stratum items arise (checked against the generator and the file).')

# ================================================================ sources: NEXUS repository README, Platt
rep(2, '**Unverified details (level U).** The following rest on search-engine excerpts or on an earlier reading of the paper that could not be reproduced in the review environment:',
    '**Authors\' repository (level R, checked 1 November 2026).** The README of the authors\' public repository (github.com/eliashossain001/nexus, main branch; SHA-256 of the retrieved file recorded in `verification/sources_R4/`) states the intervention policy explicitly: Block if any critical violation, or if the risk score ρ ≥ τ~b~ with at least one violation; Confirm if ρ ≥ τ~c~ or any high-severity violation; Revise if any medium-severity violation; otherwise Allow. It states that (τ~b~, τ~c~) = (0.75, 0.70) was selected on a safety–utility loss L(Π) = E[λ~s~u~s~ + λ~o~u~o~ + λ~c~c(Π(P))] over a 5×5 grid of (λ~s~, λ~o~), and that Platt scaling, fitted on a 60-instance calibration split, reduced ECE from 0.085 to 0.013 on the 128-instance test split. The README describes a retrained 9-feature scorer, and its headline figures (for example F1 0.965 on the synthetic test split) differ from the abstract figures quoted above. Repository documentation can differ from the paper version cited, so the abstract figures are retained and the difference is recorded rather than resolved.\n\n**Still unverified (level U).** The following rest on search-engine excerpts or on an earlier reading of the paper that could not be reproduced in the review environment:',
    '§2.9.3 NEXUS level R', 'Adds what the authors\' repository README states; keeps the paper-version figures and records the discrepancy (review, source checks).')
rep(2, '- **Calibration figures.** Platt scaling reducing ECE from 0.085 to 0.013; isotonic regression also evaluated.',
    '- **Calibration figures.** Isotonic regression also evaluated (the ECE figures are now supported at level R).',
    '§2.9.3 calibration', 'ECE figures supported by the README; the isotonic comparison is not.')
rep(2, '- **Expected-loss objective.** *Fixed* intervention costs (0 allow, 0.1 revise, 0.3 confirm, 1 block) setting loss-optimal thresholds on the calibrated score.',
    '- **Expected-loss objective.** The specific intervention costs (0 allow, 0.1 revise, 0.3 confirm, 1 block). The use of a λ-weighted loss to select the thresholds is supported at level R.',
    '§2.9.3 costs', 'The loss-based threshold selection is supported by the README; the cost values are not.')
rep(2, '- **Deployed policy.** A rule-first cascade in which the score decides between block and confirm only in some rule states.\n',
    '', '§2.9.3 policy', 'The cascade is now supported at level R (stated above), so it leaves the unverified list.')
rep(2, 'A third difference, in the decision rule (per-step expected loss with tier-indexed losses in REM; fixed intervention costs inside a rule-first cascade in NEXUS), rests on level-U evidence and must be checked against the full text before it is relied on.',
    'A third difference lies in the decision rule. REM selects each verdict by minimum expected loss with tier-indexed losses. NEXUS, according to its repository README (level R), applies a rule-first cascade with two score thresholds chosen once by a loss criterion. The cost values NEXUS uses remain level U, and the paper\'s full text has not been read.',
    '§2.9.3 difference', 'The decision-rule difference now rests on level-R evidence for the cascade.')
rep(2, '(Hossain et al., 2026; the cost values and cascade are PARTLY UNVERIFIED)', '(Hossain et al., 2026; cascade and loss-based threshold selection stated in the authors\' repository README, level R; the cost values are PARTLY UNVERIFIED)',
    '§2.8.4 NEXUS', 'Same upgrade where the objective is first mentioned.')
rep(6, 'Fixed intervention costs and a rule-first cascade (U)', 'A rule-first cascade with loss-selected thresholds (R, authors\' repository README); the cost values (U)',
    'Table 6.3 NEXUS', 'Same upgrade in the comparison table.')
rep(6, 'The difference in decision rule rests partly on unverified evidence', 'The difference in decision rule rests on the repository description (R), not on the paper\'s full text',
    'Table 6.3 NEXUS 2', 'Same.')

# Platt: the entry cites the MIT Press chapter (editors, pp. 61–74), registered by Crossref as 2000
for ch in (1, 2, 3):
    for a, b in (('Platt (1999)', 'Platt (2000)'), ('Platt, 1999', 'Platt, 2000')):
        n = text[ch].count(a)
        if n:
            text[ch] = text[ch].replace(a, b)
            log.append((NAMES[ch], 'Platt year', f'{n} × {a!r} → {b!r}: the cited version is the 2000 MIT Press chapter.'))
rep(7, 'Platt, J. C. (1999). Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. In A. J. Smola, P. Bartlett, B. Schölkopf, & D. Schuurmans (Eds.), *Advances in large margin classifiers* (pp. 61–74). MIT Press.',
    'Platt, J. C. (2000). Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. In A. J. Smola, P. Bartlett, B. Schölkopf, & D. Schuurmans (Eds.), *Advances in large-margin classifiers* (pp. 61–74). MIT Press. https://doi.org/10.7551/mitpress/1113.003.0008 [Crossref registers this chapter, pp. 61–74, under the title "Probabilities for SV Machines"; the printed chapter title was not checked]',
    'Platt entry', 'The entry cites the edited-volume chapter; its registered year is 2000 (Crossref, checked 1 Nov 2026). The title discrepancy is disclosed, not resolved.')

# ================================================================ front matter
rep(0, 'date: "Final verification draft R3 — 30 October 2026 — for supervisor review"',
    'date: "Correction draft R4 — 1 November 2026 — for supervisor review"', 'date', 'R4 version label.')
rep(0, 'This is the R3 verification draft. It was produced for **supervisor review**.',
    'This is the R4 correction draft. It applies the corrections of an independent review of the R3 draft (1 November 2026) and was produced for **supervisor review**.',
    'status R4', 'R4 version label.')

for k, v in NAMES.items():
    out = os.path.join(DST, v + '_R4.md')
    open(out, 'w', encoding='utf-8').write(text[k])
with open(os.path.join(ROOT, 'REM_FINAL_THESIS', 'reports', 'CHANGE_LOG_R4.md'), 'w', encoding='utf-8') as fh:
    fh.write('# Change Log R4 (generated by `tools/make_r4.py`)\n\nSource: R3 chapters in `chapters/`. Output: `chapters_R4/`.\n\n| # | File | Change | Reason |\n|---|---|---|---|\n')
    for i, (f, t, w) in enumerate(log, 1):
        fh.write(f'| {i} | {f} | {t} | {w} |\n')
print('R4 chapters written;', len(log), 'logged changes; tests', NTEST, '; timing', TIMING)
