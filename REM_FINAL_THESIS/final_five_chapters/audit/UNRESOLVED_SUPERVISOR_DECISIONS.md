# UNRESOLVED SUPERVISOR DECISIONS — five-chapter version

**No record of any supervisor decision exists in the repository.** Every item below is open.
The thesis text uses the recommended option, labelled as pending, wherever a wording was needed;
that wording is a proposal, not an approved decision. The full register with options and effects is
`REM_FINAL_THESIS/reports/UNRESOLVED_ITEMS_AND_SUPERVISOR_DECISIONS.md` (D-1 to D-15 and the other
codes); this file carries those items forward and adds the items raised by the five-chapter pass
(N-1 to N-9).

## A. Items that decide what the thesis may claim (CRITICAL)

| ID | Item | Current handling in the thesis | Decision needed |
|---|---|---|---|
| PILOT-AUTH | Whether pilot (exploratory) results may appear in the thesis, and under what label | Every Chapter 4 result is labelled exploratory | Authorise / restrict |
| SD-FREEZE | Approval of the Chapter 3 specification as frozen (provenance rule, feature set, predicates, Modify mechanism, grouping, labels, λ selection) | Implemented as specified; values declared exploratory | Freeze or amend |
| D-9 | Costs C_miss, C_FA, C_mod, C_esc; tier map κ; predicates | Declared exploratory values (C_FA = 1; C_miss = 1/5/10/20; C_mod = 0.5; C_esc = 0.3) | Approve, or elicit and pre-register new values and re-run |
| D-6 | Label rule (user_task_15 collision; alternative attacker routes); human label audit | Kept, with a post-hoc exclusion analysis; AI-only inspection; **no human audit** | Keep / redefine / human audit first |
| D-15 | Authorisation and resources for the live closed-loop experiment: backbone(s), decoding, repeats, frozen-parameter source (fold or refit), budget, credentials, pre-registration | Harness implemented and tested; **not executed** | Authorise and supply the inputs, **or** decide that the thesis is submitted as an exploratory study without live results |
| D-1 | Recorded-trace replay versus the Chapter 3 scope that excluded replay-based estimation | Replay kept as a labelled NO-ADAPT sensitivity analysis | Keep / drop / replace with live runs |
| D-2 / SC-1 | Mitigation semantics: step-level (CLAUDE.md lock) versus episode-level (original Ch. 3) | Step-level reference; episode-level reported as a separate experimental policy | Confirm |

## B. MAJOR items

| ID | Item | Current handling |
|---|---|---|
| D-10 / RQ-CONFIRM | Research-question wording (RQ1–RQ4) | Marked [PD] in Chapters 1 and 3 |
| D-12 | Thesis title | Title as supplied by the student; marked "Draft for supervisor review — not approved" |
| D-3 / SC-4 | Calibration fitting target: labels (Eq. 3.4) vs Platt smoothed targets | Both implemented; label-NLL primary |
| D-7 | Reviewer model for Escalate | Two bounds (idealised; no reviewer) |
| D-8 / SD-FEAT / SD-DET | Feature set; injection classifier x_ctx1 | Current set reported; no classifier chosen (x_ctx1 absent) |
| SD-5 | Banking-only scope vs O1 (financial and task-automation agents) | O1 achieved for banking only (Table 5.2) |
| Repeats | ≥ 3 repeated runs (Ch. 3 §3.11.9) | Recorded traces contain one run per configuration |
| RG-1 | Authoritative equation registry | Missing; no EQUATION_ID created |
| OI-01–OI-06 | NEXUS claims based on a Stage 1 reading | Marked U in Table 4.17 |
| OI-10–OI-13 | Printed formulations of le Cessie & van Houwelingen, Elkan, Cox, Chow not read | Record-level only |
| Full texts | No full text read for any reference | All of Chapter 2 |
| AM-1–AM-4 | Pilot amendments committed before held-out predictions | Disclosed |

## C. MINOR items

D-4 / SC-2 (tie rule), D-5 (features unavailable under k_D2), D-13 / REF-PLATT / REF-KULL (Platt
year; which Kull 2017; λ convention), D-14 (α grid cell), SC-3 (calibration-removed ablation run in
the evaluation path), SC-5 (Brier convention), SC-6 (layer label in code comments), SC-7 (= D-1),
A2-Q1 (CUSUM post-change rate), A2-ENFORCE (CUSUM enforcement variants: not implemented, conflict
with CLAUDE.md), OI-14 (AgentDojo version: package 0.1.35, commit `089ed468…`, not approved as the
frozen version), CF-01–CF-09.

## D. New items from the five-chapter pass

| ID | Item | What was done | Decision / action needed | Who |
|---|---|---|---|---|
| **N-1** | **Supervisor roles conflict.** The latest instruction names **Prof. Omar Ahmad Alzubi as Supervisor** and **Dr. Husam Fakhouri as Co-Supervisor**. The R4/R5 front matter named Dr. Husam Fakhouri as Supervisor; `thesis/FRONT_MATTER.md` named Dr. Husam Fakhouri as Supervisor and Prof. Omar as Reviewer | The latest instruction is followed on the title page; the conflict is stated on the Status page ("Unverified metadata") | Confirm roles and exact names/titles against the official appointment record. Note that Crossref spells the co-author of Kanaker et al. (2026) "Hussam" | Student / supervisor / graduate school |
| **N-2** | Faculty, department and degree on the title page ("Faculty of Artificial Intelligence — Department of Intelligent Systems"; "Master of Science in Cybersecurity") | Carried over from earlier drafts; **not verified** | Confirm against official records | Student |
| **N-3** | Arabic abstract and Arabic spellings of names (روان اللحام; أ.د. عمر أحمد الزعبي; د. حسام فاخوري) | AI-assisted draft translation; flagged on the Status page | Review the wording and the official Arabic spellings | Student |
| **N-4** | **Five chapters instead of six (D-11).** D-11 had recorded six chapters as the author's choice; the latest instruction requires five | Restructured into five chapters; no content removed; mapping in THESIS_SOURCE_MAP.md. Chapter locations inside the text (e.g. Table 3.1: demonstration → Section 3.16, evaluation → Chapter 4, communication → Chapter 5) were renumbered accordingly | Supervisor acknowledgement of the five-chapter structure | Supervisor |
| **N-5** | Placement choices within the five chapters: implementation as §3.16 (demoted, not rewritten); discussion, comparison with prior work and threats to validity in Chapter 4 (§4.15–4.17); Chapter 5 limitations as a summary (§5.5) pointing to §4.17 | As instructed (Ch. 3 merges old Ch. 3–4; Ch. 4 = results + discussion; Ch. 5 = conclusions and recommendations) | Confirm, or request another arrangement | Supervisor |
| **N-6** | **Potential conflict of interest / self-citation.** The named Co-Supervisor is a co-author of Kanaker et al. (2026), which the thesis cites and compares with (§2.13.7, §4.16) | Cited as a source and critical comparison only; evidence level stated | Decide whether a disclosure statement is required by the university | Supervisor / student |
| **N-7** | "Independent re-execution" wording in R5 | **Corrected** to "re-execution … in a fresh environment (by this project, not an external replication)" in §3.16.2 (Table 3.18), §3.16.11.2, §4.2, §4.6 and both abstracts | Confirm the wording; an external replication would be needed to claim independence | Supervisor |
| **N-8** | Front-matter placeholders: committee decision, declaration (including any AI-use declaration), dedication, acknowledgement | Placeholders only; nothing signed or affirmed; a factual note on AI assistance (not a declaration) | Complete with the university's wording | Student / university |
| **N-9** | Formatting rules and the layout reference (`enas-thesis_2026 (1).pdf`) | Not available; assumed A4 style (FORMATTING_AUDIT.md) | Provide the rules or the reference PDF; re-check the layout | Student |

## E. Live-experiment design inputs (all part of D-15; the runner refuses to run without them)

| Input (config field) | Status |
|---|---|
| LLM backbone(s) and provider | UNDECIDED |
| Decoding settings (temperature, max tokens) | UNDECIDED |
| Number of repeats per cell | UNDECIDED |
| Frozen fitted parameters (`fitted_parameters_source`: which fold, or a refit) | UNDECIDED |
| Conditions and semantics actually to be run (B0, B1, REM; step/episode level; reviewer model) | Supported by the code; selection UNDECIDED |
| Task cells (all 144 attacked pairs + 16 benign, or a subset) | UNDECIDED |
| Budget and authorisation | UNDECIDED |
| Pre-registered primary metric and analysis | UNDECIDED (draft protocol in `experiments/live/LIVE_EXPERIMENT_PROTOCOL.md`) |
| Adaptive-attack scope | UNDECIDED |

## F. MELON vs MELON + REM extension study (added 5 Nov 2026; thesis §4.14)

| ID | Item | Status |
|---|---|---|
| **M-1** | **Spending authorisation and cap** for the pilot and the final run; provider prices on the day | Required before any paid call; the runner refuses without it |
| **M-2** | Backbone model id (e.g. whether to match MELON's main GPT-4o setting), temperature, repeats, timeout and retry policy | Open (`REQUIRED_FROM_DESIGN`) |
| **M-3** | REM fitted-parameter source: `heldout_crossfit_assignment` (recommended [PD]; held-out attacker objective per case) or a single fold | Open |
| **M-4** | Whether to report the optional undefended context condition | Optional; not required for the comparison |
| **M-5** | Acceptance of compatibility measure C-2 (MELON's masked-call bank reset per episode; upstream code would carry it across episodes in one process) | Recorded; applied identically to both conditions |
| **M-6** | Use of AgentDojo 0.1.29 for this study (REM's main environment is 0.1.35; banking v1 task and attack code identical) | Recorded |
| **M-7** | The study inherits D-9 (exploratory costs), D-4 (tie rule), D-3 (calibration target) and D-8 (no injection classifier) | Inherited, not resolved |
