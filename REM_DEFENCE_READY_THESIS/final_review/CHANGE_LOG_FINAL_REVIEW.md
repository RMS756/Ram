# Change log: final review (26–27 November 2026), relative to commit `06843a0`

All thesis edits are exact replacements recorded in `tools/spec_r9.py` (or in the new-section texts `text/ch4_44.md` and `text/ch4_45.md`) and applied by `tools/make_r9.py` to the unchanged R8 sources. R8 itself (`REM_FINAL_SUBMISSION/thesis_r8/`) is unchanged.

## Substantive corrections

| # | Where | Before | After | Evidence |
|---|---|---|---|---|
| 1 | Committee Decision page | "was successfully defended and approved on [date …]" | "**This thesis has not yet been defended.** The decision …, the date of the defense and the signatures are to be completed by the university after the defense." | The thesis has not been defended |
| 2 | Title page | "Defence-ready edition prepared for discussion … not formally approved" | "Draft for supervisor review before the defense (26 November 2026) — not yet defended or approved" | Same |
| 3 | Status page | "defence-ready edition" | "draft for supervisor review … revised after a final academic review" | Same |
| 4 | Figures 4.6, 4.7, 4.8 | 19-Nov arm labels (A1 behavioral, A2 calibration, A3 thresholds, A4a context, A4b action, A5 Modify, A6 learned decision, A7 predicates) | Regenerated with the Table 4.25 labels (A3a, A4c, A4d, A2a, A3b, A4e, A4a, A4b); captions updated; Figure 4.8's note names variant A4a | Frozen protocol arm table; cross-study identity on 3,313 episodes; plotted counts asserted against the raw recomputation |
| 5 | Table 4.27, rows A4c / A4d / A4e | Raw counts ("127 against 141 episodes", "202 against 24 episodes", "48 against 141 episodes") and dashes in a percentage-point table | Percentage-point differences with intervals, discordant counts and McNemar p, computed from the per-episode call records; caption defines every cell type | `verify_numbers.py` (`S19_call_level_valid_P1.*.paired_vs_A0`) |
| 6 | Section 3.5 and Table 3.5 | The injection classifier described as in use | Marked "not implemented in REM v1.0 (D-8)"; the Detection Layer consists of x_ctx2 alone | D-8; the implementation |
| 7 | Appendix B | DRIFT missing from D-15; no entries for the ablation and comparison scope | DRIFT added; SD-ABL and SD-CMP added as open decisions | Sections 4.4 and 4.5 |

## AI-tool references

| Where | Change |
|---|---|
| Front matter, AI-use note | "(Claude Code)" removed; note kept |
| Status page, Arabic abstract note | "prepared with AI assistance" removed; native-speaker review requested |
| Chapter 2, screening | "(Claude Code)" removed; the AI-assisted screening fact kept |
| Chapter 4, 4.1.3 | "prepared by another assistant in a separate checkout" → "prepared in a separate working copy of the repository" |

## Language

| Where | Change |
|---|---|
| Chapters 1–5, appendices, English front matter | US spelling normalised outside code, URLs and references (counts in `audit/r9_renumbering.json`, key `us_spelling_changes`) |
| English abstract | One 92-word sentence on the ablation split into four sentences; content unchanged |
| Chapter 1, 1.11 items 7 and 8 | Long sentences split |
| Chapter 5, 5.8 | One long sentence split |

## Document production

| Item | Change |
|---|---|
| `tools/build_r9.py` | The PDF is now a plain LibreOffice export of the stored DOCX: no index regeneration. TOC, LoT and LoF page numbers are computed from that PDF, and headings are matched with wrapped and hyphenated lines and bidirectional marks handled. LoT and LoF are now Word TOC fields on the caption styles. LibreOffice's own TOC is used only as a check that the entry list is the same. |
| Result | 271 pages (was 272). An independent `soffice --convert-to pdf` of the DOCX is text-identical on all 271 pages. |
| `tools/verify_numbers.py` | Adds paired call-level outcomes for the 19-Nov variants; deterministic episode order |
| `tools/check_thesis_numbers.py` | Covers the new Table 4.27 cells (498 cells in total) |
| `tools/make_figures_19nov.py` | New: Figures 4.6–4.8 with Table 4.25 labels |
| `tests/test_defence_ready_thesis.py` | New test for the committee page, the absence of product names in the front matter, the new figure paths and the Table 4.27 cells. Full suite: 829 passed, 27 skipped, 1 xfailed, 0 failed. |

## Addendum (27 November 2026, at the student's request)

| Where | Change | Evidence |
|---|---|---|
| Chapter 5, Section 5.7 | Two items of future work added at the end of the list:<br>• 12, direct prompt injection (adversary AD-2, design scope only; the benchmark template named `direct` places its text in tool outputs and is an indirect injection);<br>• 13, goal drift (no adversary; outside the label of Section 3.3.5). | Scope statements in Sections 1.10, 2.3 and 3.3.4–3.3.5. AgentDojo 0.1.35 source: `DirectAttack` is a `FixedJailbreakAttack` with the template "TODO: {goal}", written into the injection candidates of the user task. |
| References | One entry added: Arike, Donoway, Bartsch and Hobbhahn (2025), *Evaluating goal drift in language model agents*, AIES 8(1), 192–203, doi:10.1609/aies.v8i1.36541 | Verified with Crossref and OpenAlex; abstract read; full text not read (stated in the entry) |

Rebuilt: 272 pages (was 271). The DOCX re-export is text-identical to the PDF on every page; besides the new text, only page numbers in the table of contents, the list of tables and the pages after Section 5.7 changed. Citation check: 106 entries, 106 cited. Number check: 498 cells, 0 mismatches.

No result, design value, research question or scope statement was changed. Both items describe future work only.

## Not changed

- Title, topic, scope, objectives, research questions and the five-layer architecture.
- Every result, and the equations.
- The reference list, apart from the notes added in the previous audit.
- The audit documents of 26 November (`FINAL_ACADEMIC_COMPLIANCE_AUDIT.md` and the others) are kept as the record of that audit. Their page count (272) refers to the earlier build.
