"""Produce the final (R3) chapters from the R2 chapters by exact, logged replacements.
Stops on any replacement that does not match exactly once. Writes:
  REM_FINAL_THESIS/chapters/CHAPTER{1..6}_FINAL.md  (per-chapter reference lists removed)
  REM_FINAL_THESIS/chapters/REFERENCES.md           (consolidated reference list)
  REM_FINAL_THESIS/reports/CHANGE_LOG_R3.md
usage: python3 REM_FINAL_THESIS/tools/make_r3.py  (from the repository root)"""
import json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'revision_R2', 'chapters_md')
OUT = os.path.join(ROOT, 'REM_FINAL_THESIS', 'chapters')
os.makedirs(OUT, exist_ok=True)
repro = json.load(open(os.path.join(ROOT, 'REM_FINAL_THESIS', 'verification', 'reproduction_comparison.json')))
T = repro['totals']
mem = json.load(open(os.path.join(ROOT, 'results', 'pilot_R2', 'latency_memory_profile.json')))
mem_rerun = repro.get('memory_rerun', {})

FILES = {1: 'CHAPTER1_INTRODUCTION', 2: 'CHAPTER2_LITERATURE_REVIEW', 3: 'CHAPTER3_METHODOLOGY',
         4: 'CHAPTER4_IMPLEMENTATION', 5: 'CHAPTER5_RESULTS', 6: 'CHAPTER6_DISCUSSION_CONCLUSION'}
text = {k: open(os.path.join(SRC, v + '_R2.md'), encoding='utf-8').read() for k, v in FILES.items()}
log = []


def rep(ch, old, new, tag, why):
    n = text[ch].count(old)
    if n != 1:
        sys.exit(f'[Ch{ch} {tag}] expected 1 match, found {n}: {old[:100]!r}')
    text[ch] = text[ch].replace(old, new)
    log.append((ch, tag, why))


# ---------------------------------------------------------------- Chapter 1
rep(1, 'The research questions below are derived from the approved objectives (Chapter 3, Section 3.1.3). Each is stated',
    'The research questions below are derived from the approved objectives (Chapter 3, Section 3.1.3). The approved proposal states no research questions, and these have not yet been confirmed by the supervisor; they remain proposed ([PD], decision D-10). Each is stated',
    'RQ status', 'Restores the [PD] status recorded in Chapter 3 §3.1.3 and the decision register; R2 had dropped it (CLAUDE.md § RESEARCH-QUESTION LOCK).')
rep(1, '- **C. Zhang et al. (2026)** show that calibrating a risk score need not improve the decisions taken with it.\n',
    '- **C. Zhang et al. (2026)** show that calibrating a risk score need not improve the decisions taken with it.\n\n'
    'A currency update of 30 October 2026 found further records close to this design, among them a controller that commits the proposed or an alternative action by a calibrated value learned from outcomes (Yan et al., 2026) and a three-way execute–confirm–block router with calibrated probabilities (Xin, 2026). They were examined at abstract level only and lie outside the systematic review (Chapter 2, Section 2.13.6).\n',
    'new prior art', 'Discloses prior-art records found in the 30 Oct 2026 update (Chapter 2 §2.13.6).')

# ---------------------------------------------------------------- Chapter 2
NEW_2136 = r'''### 2.13.6 Currency update of 30 October 2026 (outside the PRISMA flow)

The registered search ran on 25 September 2026. On 30 October 2026 the eleven queries of Table 2.1 were re-run in the same index (OpenAlex, through the same literature-search tool), restricted to publication year 2026, to find work that could change the gap assessment. **This update is not part of the PRISMA flow, and no count in Table 2.2 or Figure 2.1 changes:**

- the index returns the publication year but not the date, so records published after 25 September could not be separated reliably from earlier 2026 records;
- of the 215 unique records returned, 200 were not in the stored output of the registered search; they were title-screened by one reviewer for direct relevance to REM's decision mechanism or evaluation design, and were not assessed against criteria I1–I6;
- no record was added to the 71 included studies.

The raw output is stored with the thesis verification records (`update_search_2026-10-30.json`). Five records bear directly on REM's positioning. Each is described only as far as its index record states (level A); no full text was read.

| Record | Type | What the record states | Bearing on REM |
|---|---|---|---|
| Kekatos et al. (2026) | Peer-reviewed workshop paper (ACM, Crossref-registered) | Replays the recorded trajectories distributed with AgentDojo, STAC and R-Judge through a temporal-logic monitor, offline and without running an agent. Five generic obligations flag 70.1% of successful AgentDojo attacks and fire on 29.3% of benign runs. A planted line defeats a naive provenance check on 94–99% of the runs it would otherwise flag | Offline evaluation on AgentDojo's recorded traces has a published precedent, so it is not a methodological contribution of this thesis. Provenance evidence is itself attackable |
| Z. Liu (2026) | Preprint | Replays the ground-truth tool calls of AgentDojo and tau-bench without an LLM and evaluates fifteen prompt-injection detectors, including Prompt Guard 2. Rankings transfer poorly: the best detector on BIPIA catches 2% of AgentDojo injections at a 1% false-positive rate | The choice of the injection classifier x^ctx^~1~ (pending) should be evaluated on the agent's own tool outputs at a low false-positive rate |
| Ray (2026) | Preprint | Once blocking changes future proposals, static scores and ungated trajectories need not identify the closed-loop frontier; benign calibration alone does not transfer | Theoretical support for the limit of REM's replay analysis: replay of recorded trajectories cannot establish closed-loop enforcement |
| Yan et al. (2026) | Preprint | A controller that acts after the agent proposes an action and before it executes; it encodes trusted and external observations in provenance-typed memory and commits the action, proposed or alternative, with the highest calibrated value learned from outcomes | The closest record found to REM's combination of provenance evidence and a calibrated decision at the action boundary. It differs, by its abstract, in choosing between actions by learned value rather than among four verdicts by declared, tier-indexed losses. Prior-art risk to Gap A |
| Xin (2026) | Journal article | A pre-execution router with temperature-scaled three-class probabilities (execute, confirm, block), a fixed rule floor and confidence-triggered confirmation, evaluated on mobile-agent tasks that include financial applications | Calibrated multi-way routing with a confirmation verdict before execution has a further precedent. REM differs in deriving its thresholds from declared losses per consequence tier |

The other records of the update concern, among other topics, enforcement at the execution boundary, banking-agent benchmarks and step-labeled injection trajectories. They were not assessed and should be screened in the full update recommended in Section 2.13.4.

**Effect on the gap.** At abstract level, none of the five records reports the combination and evaluation stated in Section 2.13.2, but Yan et al. (2026) and Xin (2026) narrow the distance to it, and Kekatos et al. (2026) removes any claim of methodological novelty for offline evaluation on recorded AgentDojo traces. Because only records were examined, this conclusion has the same limits as the main review.

---

## 2.14 Chapter Summary'''
rep(2, '---\n\n## 2.14 Chapter Summary', NEW_2136, '§2.13.6', 'Adds the documented currency update of 30 Oct 2026 (outside the PRISMA flow).')

# ---------------------------------------------------------------- Chapter 3
rep(3, 'Both are implemented and evaluated, and step-level semantics is the reference definition.',
    'Both are implemented and evaluated, and step-level semantics is the reference definition. This alignment with the frozen design lock awaits the supervisor\'s confirmation (decision D-2, conflict SC-1).',
    'SC-1 status', 'Makes the pending status of the mitigation-semantics decision visible in Chapter 3; R2 stated the reference without it.')

# ---------------------------------------------------------------- Chapter 4
rep(4, '| Code version of the reported results |',
    '| Independent re-execution (R3) | 30 Oct 2026, merged repository state, Python 3.11.17, NumPy 2.4.6, AgentDojo 0.1.35, Intel Xeon @ 2.10 GHz, 4 vCPU; see Section 4.11.2 |\n| Code version of the reported results |',
    'Table 4.1', 'Records the environment of the independent re-execution.')
r12 = json.load(open(os.path.join(ROOT, 'REM_FINAL_THESIS', 'verification', 'r1_vs_r2_comparison.json')))['totals']
rep(4, 'An automated comparison of the 5,121 values the two runs share found 93 differences, all of them wall-clock time or memory measurements; every analytical value was identical.',
    f'An automated comparison of the 5,121 values the two runs share found 93 differences, all of them wall-clock time or memory measurements; every analytical value was identical. A second comparison with a different leaf-matching method (`compare_reproduction.py`, R3) counted {r12["shared"]:,} shared values and {r12["diff_volatile"]} differences, all in time, memory or provenance fields, and {r12["diff_analytical"]} analytical differences.',
    '§4.11.2 R1–R2', 'Independent re-check of the R1–R2 comparison; counts differ with the matching method, the conclusion does not.')
rep(4, '- **Attribution additivity.**',
    f'- **Independent re-execution (R3, 30 October 2026).** The complete pipeline (`run_all.sh`) was executed again, from the merged repository state, on a different processor and with the AgentDojo repository obtained afresh at commit `089ed468`. Of the {T["shared"]:,} numeric values that the re-run shares with `results/pilot_R2/`, {T["equal"]:,} were identical. The {T["diff_volatile"]:,} that differed are 100 per-step latency values, 13 code-commit stamps and one file path; no memory value and {T["diff_analytical"]} analytical values differed (`RESULTS_PROVENANCE_REPORT.md`; every differing value is listed in `verification/reproduction_all_differences.json`).\n- **Attribution additivity.**',
    '§4.11.2', 'Adds the independent re-execution and its exact outcome.')

# ---------------------------------------------------------------- Chapter 5
rep(5, 'All numbers come from `results/pilot_R2/`, produced at commit `84a8c21` by `experiments/pilot/run_all.sh`.',
    f'All numbers come from `results/pilot_R2/`, produced at commit `84a8c21` by `experiments/pilot/run_all.sh`. An independent re-execution on 30 October 2026 reproduced every analytical value; only time and memory measurements differed (Chapter 4, Section 4.11.2).',
    '§5.1 provenance', 'States the independent reproduction.')
rep(5, '- **Not independent runs.** Replaying a recorded trajectory is deterministic. Repeating it adds no information about LLM behavior.',
    '- **Not independent runs.** Replaying a recorded trajectory is deterministic. Repeating it adds no information about LLM behavior.\n'
    '- **Closed-loop identifiability.** Once blocking changes what an agent proposes next, static scores and ungated trajectories need not identify the closed-loop trade-off between false blocks and misses (Ray, 2026). Recorded trajectories are ungated in this sense. Offline replay of AgentDojo\'s recorded traces has also been used to evaluate temporal-logic monitors (Kekatos et al., 2026); neither use establishes enforcement against live agents.',
    '§5.6 limits', 'Adds the closed-loop identifiability limit and the published precedent for offline replay (Chapter 2 §2.13.6).')
kb = mem['peak_bytes_per_step_median'] / 1000; kb95 = mem['peak_bytes_per_step_p95'] / 1000
rr = mem_rerun.get('peak_bytes_per_step_median')
rr_txt = (' The independent re-execution of 30 October measured the same value.' if rr == mem['peak_bytes_per_step_median'] else f' The independent re-execution of 30 October measured {rr/1000:.1f} KB.') if rr else ''
rep(5, '- **Memory.** The median peak traced allocation was 2.9 KB per step (`latency_memory_profile.json`).',
    f'- **Memory.** The median peak traced allocation was {kb:.1f} KB per step, with a 95th percentile of {kb95:.1f} KB ({mem["steps_measured"]} steps of {mem["episodes"]} episodes; `latency_memory_profile.json`). The first run (R1) measured 2.9 KB; like time, memory varies between runs.{rr_txt}',
    '§5.6 memory', 'Corrects a number that did not match its cited artifact: results/pilot_R2/latency_memory_profile.json records a median of 4,364 bytes; 2.9 KB was the R1 value.')

lat = repro['latency_rerun_ms']
rep(5, 'across configurations and the two runs.',
    'across REM configurations and the two runs; the independent re-execution of 30 October gave values within these ranges for REM configurations.',
    '§5.6 latency', 'Records that the third execution stays within the reported range (REM configurations: median 0.137–0.156 ms, p95 0.400–0.476 ms; reproduction_comparison.json).')

rep(5, '# EXPLORATORY EVALUATION', '# EXPERIMENTAL RESULTS AND EVALUATION: AN EXPLORATORY STUDY', 'Ch5 title', 'Aligns the chapter title with the six-chapter structure requested by the author while keeping its exploratory status in the title.')

# ---------------------------------------------------------------- Chapter 6
rep(6, 'Each mechanism in REM has precedent. The distinguishing elements are the combination and the evaluation design; neither',
    'Records found in the currency update of 30 October 2026, examined at abstract level only, narrow the distance further (Chapter 2, Section 2.13.6): a controller that commits the proposed or an alternative action by a calibrated value learned from outcomes, with provenance-typed evidence (Yan et al., 2026); a three-way execute–confirm–block router with calibrated probabilities (Xin, 2026); and an offline evaluation of runtime monitors on AgentDojo\'s recorded traces (Kekatos et al., 2026).\n\n'
    'Each mechanism in REM has precedent. The distinguishing elements are the combination and the evaluation design; neither',
    '§6.3 new prior art', 'Adds the closest records from the currency update.')
rep(6, '9. **Runtime figures.**',
    '9. **Currency.** Work published after the review\'s search date was examined only at abstract level, and several close records were found (Chapter 2, Section 2.13.6).\n10. **Runtime figures.**',
    '§6.5 limitation', 'Adds the literature-currency limitation.')
rep(6, '5. **Feature revision.** Revise the behavioral features, for example by conditioning privilege escalation on provenance, and add the injection classifier.',
    '5. **Feature revision.** Revise the behavioral features, for example by conditioning privilege escalation on provenance, and add the injection classifier, selected on the agent\'s own tool outputs at a low false-positive rate (Z. Liu, 2026).',
    '§6.6 classifier', 'Grounds the classifier-selection future work in the update record.')


# ---------------------------------------------------------------- Chapter 2: disclosure of AI assistance in the review, as recorded
rep(2, 'Selection had two stages, both carried out by a single reviewer.',
    'Selection had two stages, both carried out by a single reviewer: the thesis author, assisted by an AI coding assistant (Claude Code), as recorded in the search-strategy file (`CHAPTER2_SYSTEMATIC_SEARCH_STRATEGY.md`).',
    '§2.2.5 reviewer', 'Aligns the text with the review record, which names AI assistance; the chapter did not disclose it.')
rep(2, '5. **Single reviewer.** Screening, extraction and appraisal were each done by one person, with no second screener and no agreement statistic.',
    '5. **Single reviewer, AI-assisted.** Screening, extraction and appraisal were each done by one reviewer, assisted by an AI coding assistant, with no independent second screener and no agreement statistic.',
    '§2.13.4 item 5', 'Same correction in the limitations; "one person" did not state the AI assistance recorded in the review files.')


# ---------------------------------------------------------------- Chapter 5: interval interpretation (examiner review, R3)
rep(5, 'With nine injection-task groups the intervals are wide. Where a category contains a single injection task, no interval can be formed and none is reported.',
    'With nine injection-task groups the intervals are wide. Bootstrap coverage is an asymptotic property, and with so few groups the intervals are not guaranteed to reach their nominal 95% coverage; a narrow interval, such as that of REM\'s replay ASR, is not evidence of precision. The intervals are therefore descriptive, and no hypothesis test is based on them. Where a category contains a single injection task, no interval can be formed and none is reported.',
    '§5.2 intervals', 'States that percentile intervals over nine groups need not reach nominal coverage (examiner review finding).')


# ---------------------------------------------------------------- equation encodings (rendering only; mathematics unchanged)
rep(2, r'$$a^{*}(x) = \arg\min_{a}', r'$$a^{\text{*}}(x) = \arg\min_{a}', 'Eq. 2.3 encoding', 'Same mathematics; the superscript asterisk is encoded so that it renders in both Word and LibreOffice.')
rep(3, r'$$ p^{*}_k = \frac{C_{\mathrm{FA}}(k)}', r'$$ p^{\text{*}}_k = \frac{C_{\mathrm{FA}}(k)}', 'Eq. 3.9 encoding', 'Same mathematics; rendering fix as for Eq. 2.3.')
rep(3, r'\frac{|B_m|}{N} \left| \bar{y}(B_m) - \bar{p}(B_m) \right|', r'\frac{\left\vert B_m \right\vert}{N} \left\vert \bar{y}(B_m) - \bar{p}(B_m) \right\vert', 'Eq. 3.20 encoding', 'Same mathematics; absolute-value bars encoded so that they render in LibreOffice.')

# ---------------------------------------------------------------- references: strip per-chapter lists, consolidate
NEW_REFS = [
    'Kekatos, N., Basagiannis, S., Chintri, M., Lekidis, A., Nianios, T., Seitoglou, I., Temperekidis, A., & Katsaros, P. (2026). Formal runtime verification for tool-using LLM agents: An offline same-benchmark study on AgentDojo and STAC. In *Proceedings of the 2026 8th Joint Workshop on CPS&IoT Security and Privacy* (pp. 129–142). ACM. https://doi.org/10.1145/3847353.3847499',
    'Liu, Z. (2026). *Passing the test you trained on: Re-evaluating prompt-injection detectors for LLM agents* (arXiv:2610.03448) [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2610.03448',
    'Ray, S. (2026). *What can be enforced? A theory of certified runtime safety for tool-using agents* (arXiv:2607.22868) [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2607.22868',
    'Xin, Q. (2026). TapGuard: Temperature-calibrated execute–confirm–block routing for LLM-powered mobile agents. *International Journal of Mobile Applications and Technologies, 2*(2). https://doi.org/10.51137/wrp.ijmat.1051',
    'Yan, B., Zhang, Q., Kan, Z., et al. (2026). *PROVISO: Provenance-informed action selection for secure LLM agents* (arXiv:2610.27115) [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2610.27115 [Author list abbreviated from the index record; full list not verified]',
]
entries = {}   # normalized key -> (preferred entry, set of chapters)
PREF = [2, 3, 1, 4, 5, 6]   # Chapter 2's entries passed the review's metadata verification; prefer them


def norm_key(e):
    m = re.match(r'(.+?)\s\((\d{4}[a-z]?)\)\.\s*(.+)', e)
    if not m:
        return e[:60].lower()
    authors, year, rest = m.groups()
    title = re.sub(r'[^a-z0-9]', '', rest.lower())[:40]
    return (authors.split(',')[0].lower(), year, title)


for ch in PREF:
    t = text[ch]
    if '\n## References' not in t:
        continue
    body, refs = t.split('\n## References', 1)
    for line in refs.split('\n'):
        l = line.strip()
        if not l or l.startswith('*APA') or l.startswith('#'):
            continue
        k = norm_key(l)
        if k not in entries:
            entries[k] = [l, {ch}]
        else:
            entries[k][1].add(ch)
    text[ch] = body.rstrip() + '\n'
for e in NEW_REFS:
    entries[norm_key(e)] = [e, {'R3'}]
refs_sorted = sorted(entries.values(), key=lambda v: re.sub(r'[^a-z ]', '', v[0].lower()))
header = ('# REFERENCES\n\n*APA 7th edition. One consolidated list for all chapters. Preprints, working papers and withdrawn preprints are marked. '
          'Official and regulatory sources are marked [Official source] and are not treated as research literature. For arXiv-only records identified through the index, '
          'author lists abbreviated in the index record are marked as such. The verification status of every entry is recorded in `REFERENCES_VERIFIED.md`.*\n\n')
open(os.path.join(OUT, 'REFERENCES.md'), 'w', encoding='utf-8').write(header + '\n\n'.join(v[0] for v in refs_sorted) + '\n')
json.dump([{'entry': v[0], 'chapters': sorted(map(str, v[1]))} for v in refs_sorted],
          open(os.path.join(ROOT, 'REM_FINAL_THESIS', 'verification', 'consolidated_references.json'), 'w'), indent=1, ensure_ascii=False)

for ch, name in FILES.items():
    open(os.path.join(OUT, name + '_FINAL.md'), 'w', encoding='utf-8').write(text[ch])

with open(os.path.join(ROOT, 'REM_FINAL_THESIS', 'reports', 'CHANGE_LOG_R3.md'), 'w', encoding='utf-8') as f:
    f.write('# Change Log — R3 (final verification pass, 30 October 2026)\n\n'
            'Base: `revision_R2/chapters_md/*_R2.md` (commit `3b15dc8`). Every change below was applied by `REM_FINAL_THESIS/tools/make_r3.py` as an exact replacement that must match once. Content not listed is unchanged from R2.\n\n'
            '| Chapter | Change | Reason |\n|---|---|---|\n')
    for ch, tag, why in log:
        f.write(f'| {ch} | {tag} | {why} |\n')
    f.write(f'| All | Per-chapter reference lists replaced by one consolidated list ({len(refs_sorted)} entries; `chapters/REFERENCES.md`) | Removes 21 cross-chapter formatting inconsistencies; Chapter 2 entries, which passed the review\'s metadata verification, are preferred where versions differ |\n')
print('chapters written; changes', len(log), '; references', len(refs_sorted))
