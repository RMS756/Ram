# 11 — Edit Change Log

Every edit applied in this stage, with the original text and the replacement. Nine edits were
applied in total: four to Chapter 2 and five to Chapter 3.

**Scope of editing.** Edits were applied only to the working copies in
`REM_AUDIT_OUTPUT/working/`. The original files `Chapter2_Literature_Review.md`,
`Chapter3_Methodology.md` and their DOCX versions were not opened for writing at any point; their
SHA-256 values are unchanged (Section B of `10_MASTER_AUDIT_REPORT.md`).

**What no edit did.** No equation was added, removed or renumbered (22 in Chapter 3, 0 in
Chapter 2, before and after). No reference entry was added or removed (47 in Chapter 2, 37 in
Chapter 3, before and after). No section was added, removed or renamed (21 and 57 headings before
and after). No numerical result was altered. No REM layer was added: the architecture remains
Input & Context, Detection, Behavioral Analysis, Decision Engine, Mitigation.

**Word counts.** Chapter 2: 6,259 → 6,335 words (+76). Chapter 3: 11,060 → 11,346 words (+286).
All growth is explanatory prose; nothing was deleted except the one unverifiable mechanism
description recorded in E-01.

**In-text citation counts.** Chapter 2: 108 → 108. Chapter 3: 90 → 92. The two additional
Chapter 3 citations are not new literature: Arp et al. (2022) was already cited in Section 3.5 and
is now also cited in Section 3.11.6, and the single parenthetical "(Lorden, 1971; Moustakides,
1986)" became two narrative citations when that sentence was rewritten.

---

## Evidence fixes

### E-01 — Chapter 2, Section 2.10 (line 132)

**Type:** evidence fix. **Audit row:** `01_CHAPTER2_LITERATURE_EVIDENCE_AUDIT.xlsx`, verification
UNVERIFIED, support None. **Reference:** REF-024 Jackson (2025), SSRN HTTP 403.

**Before:**
> A working paper by Jackson (2025) describes a policy engine that collects risk signals into a
> risk score and issues allow, deny, sanitize, or escalate decisions. It is not peer reviewed, and
> its full text could not be accessed during the September 2026 update.

**After:**
> A working paper by Jackson (2025), listed on SSRN as *Designing a policy engine for agentic AI
> systems: From governance requirements to runtime enforcement*, appears from its title to address
> the same question. Its full text returned an access error throughout the September 2026
> verification pass, so its mechanism is not described here. It is not peer reviewed, and no claim
> in this thesis rests on it.

**Reason.** The chapter disclosed that the full text was inaccessible but still described the
engine's mechanism, which no accessible record supports. The description was the only unsupported
part and was removed; the work itself, its title and the access failure are all retained, so no
evidence of the problem has been discarded. The reference entry remains in the list.

### E-02 — Chapter 2, Section 2.2 (line 19)

**Type:** evidence fix. **Audit row:** verification PARTIALLY SUPPORTED. **Reference:** REF-055
Yao et al. (2023).

**Before:** "The ReAct paradigm (Yao et al., 2023) made the dominant execution pattern explicit:"

**After:** "The ReAct paradigm (Yao et al., 2023) made explicit the execution pattern that most of
the systems reviewed here assume:"

**Reason.** ReAct introduces the interleaving of reasoning and acting; that it is *the dominant*
pattern is the chapter's own judgement and is not a finding of the cited paper. The replacement
states a claim the chapter can support from its own survey.

### E-03 — Chapter 3, Section 3.7.5, status note under Equation 3.9 (line 454)

**Type:** evidence fix. **Audit row:** `05_EQUATION_SOURCE_AUDIT.xlsx`, Eq. 3.9, PARTIALLY
VERIFIED. **Reference:** REF-017 Elkan (2001); Eq. (1) was read, the printed threshold expression
was not extractable from the author's PDF.

**Before:**
> *Status:* derived from Equation 3.8. It coincides with the two-class cost-sensitive threshold
> with zero-cost correct decisions discussed by Elkan (2001).

**After:**
> *Status:* derived from Equation 3.8. It has the form of the standard two-class cost-sensitive
> threshold for zero-cost correct decisions, which Elkan (2001) obtains from the same expected-cost
> criterion; the printed threshold expression in that paper could not be inspected directly during
> verification, so the derivation above stands on Equation 3.8 alone.

**Reason.** "Coincides with" asserts equality with a printed equation that was not read. The
derivation is unaffected: Equation 3.9 follows from Equation 3.8, which is proved in the chapter.

### E-04 — Chapter 3, Section 3.11.10 (line 796)

**Type:** evidence fix. **Audit row:** verification UNVERIFIED, support None. **References:**
REF-033 Lorden (1971), REF-036 Moustakides (1986).

**Before:**
> The optimality results for this procedure (Lorden, 1971; Moustakides, 1986) assume independent
> observations with known distributions. Neither assumption holds for agent trajectories, so the
> results motivate the procedure but provide no guarantee.

**After:**
> The procedure has known optimality properties in sequential change detection: Lorden (1971)
> proposed stopping rules that are asymptotically optimal in a defined sense, and Moustakides
> (1986) showed Page's stopping time to be optimal in a stronger sense. Both results are proved
> within a sequential-analysis model whose conditions could not be inspected during verification
> and are not claimed to hold for agent trajectories, where observations are neither independent
> nor drawn from known distributions. They therefore motivate the procedure and provide no
> guarantee in this setting.

**Reason.** The original stated the assumptions of two papers whose text was not read. During this
stage both abstracts were read on Project Euclid (2026-09-22), which confirms the optimality
statements but not the conditions. The replacement asserts only what the abstracts support, states
that the conditions were not inspected, and keeps the conclusion — that nothing here is guaranteed
for agent trajectories — which does not depend on those conditions.

---

## Prose edits

### P-01 — Chapter 3, Section 3.3.7 (inserted before the SO list)

**Type:** prose. **Audit row:** `07_AI_STYLE_AUDIT.xlsx` S-01, severity HIGH.

**Before:** the heading was followed immediately by the list `SO-1 … SO-6`.

**Inserted:**
> The threat model above states what an adversary can do; the objectives below state what REM must
> therefore do about it. They are ordered along the path of a single proposed tool call: from the
> evidence available about it, through the verdict selected for it, to the record left behind and
> the cost of producing it.

**Reason.** A bare list under a heading gives the reader items without stating where they come from
or how they are organised. The sentence claims nothing that the chapter does not already establish:
it names the relationship to Section 3.3 and describes the ordering of the existing list.

### P-02 — Chapter 3, Section 3.11.3 (inserted before the label list)

**Type:** prose. **Audit row:** S-02, severity HIGH.

**Inserted:**
> The label must represent the quantity the estimator is asked to predict, which is whether a
> proposed call serves the attacker's objective rather than the user's. Labels are therefore
> derived from the injection task's own reference solution, not from the presence of an injection
> in the episode, because an attacked episode also contains benign calls. The derivation is
> mechanical, so the rules below state exactly what is matched, where the rule is known to be
> uncertain, and how that uncertainty is measured.

**Reason.** Label construction is a contestable methodological decision presented as three bullets.
The inserted text states the principle behind the decision. Every factual element restates rules
already given in the list that follows (labels come from the injection task's reference solution;
benign calls in attacked episodes are labelled 0; the derivation is audited).

### P-03 — Chapter 3, Section 3.11.6 (inserted before the controls list)

**Type:** prose. **Audit row:** S-03, severity HIGH.

**Inserted:**
> Because the injection tasks in the banking suite share a small number of templates and a single
> attacker account, an estimator can reach a high score by memorising the benchmark rather than by
> recognising adversarial inducement. Arp et al. (2022) identify this family of errors as a
> recurring cause of overstated security-classification results. The following controls are
> therefore fixed before any held-out prediction is examined.

**Reason.** The list of controls did not say what they control for. The shared attacker account and
the small template count are both stated in Section 3.11.2 of the same chapter. Arp et al. (2022)
is already cited in Chapter 3 (Section 3.5) and in the reference list, and the claim used here is
the one verified from that paper's abstract; no new reference was introduced. The inserted text was
checked against the chapters' existing spelling convention (US: "labeled", "analyzed", "optimizes")
and corrected accordingly.

### P-04 — Chapter 2, Section 2.4.3 (line 53)

**Type:** prose. **Audit row:** S-05, severity MEDIUM.

**Before:** four consecutive sentences of identical shape — "LlamaFirewall (…) combines … ",
"GuardAgent (…) converts … ", "AGrail (…) generates … ", "ShieldAgent (…) extracts … ".

**After:** the paragraph now opens with "What unites the third family is that the check itself is
learned or generated rather than written by hand.", and the four systems are introduced with varied
constructions ("In GuardAgent … the generation is of code"; "AGrail … goes further and keeps
optimizing"; "ShieldAgent … instead extracts").

**Reason.** The paragraph catalogued systems without stating what makes them one family, and its
uniform sentence shape read as a generated list. Every citation, figure and percentage is carried
over unchanged: 98%, 83%, 11.3%, 90.1%, 64.7%, 58.2%. Reported results are now explicitly
attributed to their authors.

### P-05 — Chapter 2, Section 2.7 (line 95)

**Type:** prose. **Audit row:** S-06, severity MEDIUM.

**Before:** one sentence carrying five figures — "… with 31 regulatory case-driven sandbox
scenarios, 107 real-world vulnerabilities, and 963 test cases, reporting attack success rates of up
to 50.0% on state-of-the-art models and 6.7% for the most robust configuration."

**After:** split into two sentences — the benchmark's composition, then "Its authors reported
attack success rates of up to 50.0% on the strongest models they tested and 6.7% for the most
robust configuration."

**Reason.** Readability, plus attribution: the results are now marked as the authors' own report,
consistent with the convention stated in Section 2.1. All five figures are unchanged. "State-of-the-art
models" became "the strongest models they tested", which is the same claim without the marketing term.

---

## Recorded but not applied

| Audit row | Finding | Why no edit was made |
|---|---|---|
| S-07 | `**Synthesis.**` used as the closing label of eleven consecutive subsections in Chapter 2 | Consistent signposting across a chapter is defensible in a thesis, and varying only some labels would make the structure inconsistent. Left for the author's decision. |
| S-08 | "This loop is what makes agents useful. It is also what makes them attackable …" | Accurate, compact, and central to the chapter's argument. Recorded so the author can decide whether to rephrase in their own voice. |
| S-09 | "First … Second … Third …" enumeration in two adjacent sections | Standard academic practice, and the two passages enumerate genuinely different things. |
| S-04 | 38% of Chapter 3's words sit inside list items | Only the three sections with no prose at all were given lead-ins. Converting further lists into prose would change the chapter structure, which is frozen by the Stage 3 decision. |

## Editing principle applied throughout

Revisions add or restructure explanation only. No grammatical error, informality or vagueness was
introduced; nothing was simplified to appear less technical; no change was made for the purpose of
affecting any AI-detection tool, and no such tool was run in this stage.
