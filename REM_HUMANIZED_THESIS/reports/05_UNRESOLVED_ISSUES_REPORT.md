# Unresolved issues (Category C): supervisor decisions, institutional confirmation, missing evidence or new work

Nothing in this list was implemented. The items U-1 to U-17 of `REM_DEFENCE_READY_THESIS/final_review/UNRESOLVED_ISSUES_REPORT.md` remain open and are not repeated here. The items below are new from this review.

## Wording that only the supervisor can approve

| ID | Issue | Suggestion | Who |
|---|---|---|---|
| H-1 | The English abstract is about 1,150 words, longer than most university abstract limits. The limit of Al-Balqa Applied University is not known here. | Confirm the limit. If it is lower, shorten the abstract to the problem, method, three headline results and limits. The extension and redesign studies would move to the body. | Supervisor and university |
| H-2 | The research-gap statement (Sections 1.4 and 2.11.5) reads "Limited controlled evidence establishes whether …", which is grammatically awkward. It was not edited, because the gap wording is pending (D-10). | "There is little controlled evidence on whether a learned, consequence-aware runtime decision adds value …" (same meaning) | Supervisor |
| H-3 | The wording of RQ3 asks for residual attack success after Modify. Under NO-ADAPT replay this is zero by construction, so RQ3 can be answered only trivially. | Either keep RQ3 and state the limitation in Table 5.1 (already partly done), or reword RQ3 to ask what replay can measure | Supervisor |
| H-4 | "33 of 180 state-changing steps" (observe-only, Section 4.6.2) and "33 of 178 authorized calls" (replay, Section 4.4.7) use the same numerator with different units | Add one clarifying clause. This is a wording change only; it was not made because the sentences already name their units. | Student or supervisor |

## Structure and length (no scientific change; supervisor's preference)

| ID | Issue | Suggestion |
|---|---|---|
| H-5 | Chapter 4 is about 37,000 words, more than half the thesis. A large part reports exploratory extensions that are not part of REM v1.0: Sections 4.4.7 (extension), 4.5.8 and 4.6.9. | Move the extension and redesign studies to an appendix, or to the supplement with a two-page summary in Chapter 4 |
| H-6 | Repository paths, commit hashes and dated study names in the body (U-10) also lengthen the text | Move them to a reproducibility appendix |
| H-7 | Some content appears twice. For example, the calibration result is stated in both the pilot findings and the follow-up list of Section 4.5.7, and REM's withholding of legitimate payments in Sections 4.4.7, 4.5.10 and 4.6.10. Removing a repetition changes the printed numbers of a section, so it was not done under the preservation rule. | Trim after the supervisor's decision on H-5 |

## Literature (no reference was added)

| ID | Issue | Suggestion |
|---|---|---|
| H-8 | Possibly relevant works are not cited. Their records were verified in this review; their full texts were not read: SecAlign (ACM CCS 2025), PromptArmor (arXiv 2025) and Design Patterns for Securing LLM Agents (arXiv 2025). The Instruction Hierarchy (2024) could not be verified here. | Decide whether to discuss them in Chapter 2. If so, read the full texts first. |
| H-9 | The systematic review is record-level, with one database. Recall of known prior art was 3 of 13. | For a journal: replace it with a full-text related-work section |

## Evidence that does not exist yet (new work)

| ID | Missing evidence | Why it matters | Scale |
|---|---|---|---|
| H-10 | Replay sweep over declared cost ratios (C~miss~/C~FA~, C~esc~) | Separates "the learned decision over-blocks" from "these declared costs over-block" | Small: offline, no model; needs approval of a cost grid |
| H-11 | Human label audit of the prepared 145-item package (U-3/D-6) | Labels were inspected only by an AI assistant | Small to medium: annotator time |
| H-12 | Live closed-loop evaluation with an LLM agent: REM, rules, Progent with generated policies, MELON, DRIFT and PromptArmor | The only way to measure protection against an agent that adapts to refusals | Large: model access, budget, repeated runs |
| H-13 | A second benchmark or a second suite with new user tasks, and an attacker whose account is not fixed | External validity; tests REM's claimed advantage over allow-lists | Medium to large |
| H-14 | Cluster-aware hypothesis tests (for example, a permutation test over injection tasks) next to the bootstrap intervals | Few clusters make the bootstrap intervals descriptive only | Small: offline |
| H-15 | Native-speaker review of the Arabic abstract (U-8) | The translation is a draft | Small |
