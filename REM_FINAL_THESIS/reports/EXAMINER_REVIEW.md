# Examiner-Style Critical Review (R3, 30 October 2026)

**Reviewed:** `REM_FINAL_THESIS.docx` / `.pdf` (218 pages A4) and their Markdown sources, against the code, the result files and the verification records.

**Stance:** that of an external examiner for an MSc thesis who has not seen the project before. Findings are not softened for the deadline.

**Severity:**
- **CRITICAL:** prevents formal submission, because the thesis cannot support its central claim, or a mandatory element is missing.
- **MAJOR:** an examiner would require correction or substantial justification.
- **MINOR:** presentation, wording or consistency.

**Status:**
- **FIXED (R3):** corrected in this revision.
- **DISCLOSED:** stated in the thesis as a limitation; still a weakness.
- **OPEN:** needs action outside the author's assistant's authority.

## 1. CRITICAL

| # | Finding | Location | Evidence | Minimum valid action | Status |
|---|---|---|---|---|---|
| C-1 | **The central practical claim is not established.** The thesis proposes that tier-indexed expected-loss verdicts reduce financial harm at acceptable utility cost. No enforcing-mode run with a live agent was executed. All enforcement numbers come from replay under NO-ADAPT, where a withheld call can never be retried, so residual success after Modify is ≈ 0 by assumption | Ch. 1 §1.11; Ch. 5 §5.1, §5.6; Ch. 6 §6.4 | `RESULTS_PROVENANCE_REPORT.md` §1: "NOT EXECUTED — NO EMPIRICAL RESULT AVAILABLE" for live runs | Either (a) run a pre-registered live enforcing-mode experiment (D-15), or (b) obtain the supervisor's explicit decision that the thesis is submitted as an exploratory study without it, and reframe the title and contribution accordingly | DISCLOSED; OPEN |
| C-2 | **Every quantitative decision result rests on design values that nobody has approved.** These are the costs, the tier map, the predicates, the feature set and the label rule. The low tier-4 threshold (1/21) alone drives the utility cost | Ch. 3 Tables 3.11, 3.13; Ch. 5 §5.5, §5.9; Ch. 6 §6.1.2 | Decision register D-9, SD-FREEZE, PILOT-AUTH; no decision record exists | Supervisor approval of the values, or approval to present them as declared exploratory values (PILOT-AUTH) | DISCLOSED; OPEN |
| C-3 | **The labels are an unaudited proxy.** Positives are reference-matched attempts. user_task_15 is ambiguous in 16 of 21 recordings, and all of REM's residual replay ASR comes from it. The only inspection was by the AI assistant, which found 1 likely false negative in 30 | Ch. 5 §5.10; Ch. 6 §6.5 item 4 | `results/pilot_R2/label_audit_human_package.csv` (145 items, not annotated) | Human annotation of the prepared package (at least one annotator, preferably two), agreement reported, then decision D-6 | DISCLOSED; OPEN |
| C-4 | **The enforcement evaluation uses a method the approved methodology excluded.** Ch. 3 §3.1.4 originally excluded estimation by replaying trajectories. Replay is now proposed as a scope amendment (§3.11.11), but the amendment is unapproved | Ch. 3 §3.1.4, §3.11.11; Ch. 5 §5.6 | SC-7 / D-1 | Supervisor decision D-1: accept the amendment, drop the replay results, or replace them with live runs | DISCLOSED; OPEN |
| C-5 | **Mandatory formal elements are missing.** These are the approved title, the student name, the university template, the committee and approval pages, the declaration, and, if required, an Arabic abstract and an AI-use declaration | Title page; front matter | `UNRESOLVED_ITEMS…` §4 | Supply them from official records. None can be produced by the assistant without fabrication | OPEN |

## 2. MAJOR

| # | Finding | Location | Evidence | Minimum valid action | Status |
|---|---|---|---|---|---|
| M-1 | **No source was read in full in any recent session.** Seven equations carry SOURCE NOT FULLY VERIFIED (3.1, 3.2, 3.3, 3.9, 3.10, 3.15, 3.16). The Platt citation is in conflict (1999 report vs 2000 chapter) | Ch. 2–3; Ch. 3 Table 3.17 | `SOURCE_VERIFICATION_LOG.md`; `REFERENCES_VERIFIED.md` (90 recorded, 21 partial, 2 conflict/withdrawn) | Full-text checks starting with the equation sources; decision D-13 | DISCLOSED; OPEN |
| M-2 | **The literature review is systematic in procedure but narrow in reach.** One database (OpenAlex) was searched. The top 24–25 records per query were screened. The search retrieved 3 of 13 named prior-art studies. Screening was record-level only, by one AI-assisted reviewer | Ch. 2 §2.2, §2.13.4 | PRISMA records in `chapter2/slr/` (reproduced 30 Oct) | Run the protocol's Boolean blocks in IEEE Xplore, ACM DL, Scopus/WoS and arXiv; screen full texts; update the PRISMA flow | DISCLOSED; OPEN |
| M-3 | **Close prior art narrows the novelty margin.** Records published after the review describe a provenance-informed controller with calibrated values (PROVISO), a calibrated execute–confirm–block router (TapGuard), and an offline evaluation of runtime monitors on AgentDojo's recorded traces (Kekatos et al.). The last is very close to this thesis's evaluation design. All were examined at abstract level only | Ch. 2 §2.13.6; Ch. 1; Ch. 6 §6.3 | `verification/update_search_2026-10-30.json` | Read these works in full and state the differences precisely before any novelty statement is defended | DISCLOSED (added in R3); OPEN |
| M-4 | **The statistical basis is thin.** There are nine attacked groups, one run per configuration and several single-task categories. There is no multiplicity correction. Percentile intervals over nine groups need not reach nominal coverage | Ch. 5 §5.2, Tables 5.7–5.8 | `pilot_e0.yaml` (bootstrap settings) | Repeated runs (≥ 3) in a live experiment; treat intervals as descriptive | Coverage caveat **FIXED (R3)** in Ch. 5 §5.2; the rest DISCLOSED |
| M-5 | **The benchmark structure may inflate action-evidence performance.** There is one attacker identity, one attack template for fitting and short trajectories. "Destination not in the user's request" separates classes more easily here than in practice | Ch. 5 §5.4, §5.7; Ch. 6 Table 6.1 rows 2–3 | Held-out ROC-AUC 0.938; 0.799 without action evidence | Evaluation on a second benchmark or with varied attacker identities | DISCLOSED |
| M-6 | **Part of the Detection layer is missing.** The injection classifier x_ctx1, specified in Ch. 3, is absent. The Detection layer reduces to a regular-expression indicator authored with knowledge of the benchmark | Ch. 4 §4.5; Ch. 5 | Table 4.6 "Absent" | Decision D-8 (choose a classifier and re-run), or restrict the architecture claim | DISCLOSED |
| M-7 | **Escalate has no reviewer.** Results are bounded by "no reviewer" (−0.195 benign utility) and an oracle (+0.003). The practical value of the design depends on a reviewer that is not modelled | Ch. 5 §5.6; Ch. 6 §6.1.2 | D-7 | A reviewer model with an error rate and delay, at least as a sensitivity analysis | DISCLOSED |
| M-8 | **The evaluated system is not the frozen pipeline.** Chapter 5 results come from the evaluation path (`agentdojo_replay.py` + `a3.py`). The frozen `RemPipeline` is exercised only by tests. The two paths differ on ties (SC-2), the calibration ablation (SC-3) and the calibration target (SC-4) | Ch. 4 §4.3 | `METHODOLOGY_CODE_TRACEABILITY.md` §2–3 | State this in the defence; decide SC-2 to SC-4 | DISCLOSED |
| M-9 | **The research questions are unconfirmed.** The approved proposal has no RQs; RQ1–RQ4 are derived and marked [PD] | Ch. 1 §1.7; Ch. 3 §3.1.3 | D-10 | Supervisor confirmation | **FIXED (R3)**: Ch. 1 had dropped the [PD] status; now OPEN on D-10 |
| M-10 | **A reported number contradicted its own source file.** Median memory per step was 2.9 KB in Ch. 5 R2, while the cited R2 file records 4,364 bytes | Ch. 5 §5.6 | `latency_memory_profile.json`; re-run of 30 Oct | — | **FIXED (R3)** |
| M-11 | **The AI assistance in the review was not disclosed.** The review record names "the thesis author, assisted by Claude Code"; the chapter said "one person" | Ch. 2 §2.2.5, §2.13.4 | `chapter2/CHAPTER2_SYSTEMATIC_SEARCH_STRATEGY.md` line 4 | — | **FIXED (R3)**. A factual note was also added to the front matter. The formal AI-use declaration remains the author's (C-5) |
| M-12 | **Banking scope only, versus O1** (financial and task-automation agents) | Ch. 6 Table 6.2 | SD-5 | Supervisor confirmation of scope | DISCLOSED |

## 3. MINOR

| # | Finding | Location | Action | Status |
|---|---|---|---|---|
| m-1 | RQ wording in Ch. 1 is a shortened form of Ch. 3 (RQ2 metric list; "processing time" vs "latency") | Ch. 1 §1.7 | Align with the wording approved under D-10 | OPEN |
| m-2 | The architecture figure draws L2 → L3 in sequence (Ch. 3 says they run in parallel on L1's output) and carries an "EXPLORATORY" footer | Figure 3.1 | Redraw | OPEN |
| m-3 | Ch. 6 conclusions are organized by finding, not by RQ; the RQ answers are in Ch. 5 §5.12 | Ch. 6 | Optional cross-reference table | OPEN |
| m-4 | Ch. 2 is about 21,700 words (45% of the body) | Ch. 2 | Shorten if the supervisor or template requires it | OPEN |
| m-5 | Spec–code mismatches without numerical effect: ties (0 occurred), the estimator's layer label in code comments, the Brier convention | Ch. 4 §4.3, §4.7; Ch. 5 Table 5.3 | Decisions SC-2, SC-5, SC-6 | DISCLOSED |
| m-6 | Pre-registered α grid contains an invalid cell (α_blk = α_mod) | Ch. 5 §5.9 | D-14 | DISCLOSED |
| m-7 | The optional CUSUM's false-alarm rate is 0.106 against a 0.05 target | Ch. 5 §5.8 | A2-Q1 | DISCLOSED (observe-only) |
| m-8 | The instruction-pattern set was authored with knowledge of the benchmark | Ch. 4 §4.5 | None needed for conclusions: the ablation shows no contribution | DISCLOSED |
| m-9 | The realized-loss comparison favours REM by construction | Ch. 3, Ch. 5 §5.9 | — | DISCLOSED |
| m-10 | Page numbers in the contents, list of figures and list of tables were computed by LibreOffice; Word recomputes fields on opening | DOCX | Update fields in Word before printing | Note |
| m-11 | The Ch. 4 sentence on the re-run said the 114 differing values were "time or memory". They are 100 latency values, 13 commit stamps and 1 file path | Ch. 4 §4.11.2 | — | **FIXED (R3)** |
| m-12 | Display equations 2.3, 3.9 and 3.20 rendered as placeholder glyphs in the PDF | PDF | — | **FIXED (R3)** (0 placeholder glyphs) |
| m-13 | Twenty-one works were formatted differently in different chapters; Hevner (2004) and Peffers (2007) were cited without entries | References | — | **FIXED (R3)**: one list of 113 entries |

## 4. What an examiner would find sound

These are stated because a review that lists only faults misrepresents the work.

- **Reproducibility is unusually strong for an MSc thesis.** An independent re-execution on different hardware reproduced every analytical value (0 of 6,057 shared values differed analytically, every difference listed). The PRISMA counts reproduce from the stored search output.
- **The mathematics is correct where checked.** 22 symbolic and numerical checks pass, including the indifference thresholds and the escalation-feasibility condition. 193 tests pass.
- **Leakage control is careful.** Nested grouped cross-fitting holds out whole attacker objectives, and every fitted quantity, including feature retention, is fitted within the fold.
- **The evidence is honestly bounded.** Negative findings are reported (no calibration benefit; behavioural features harmful to utility). The thesis states repeatedly that it does not show protection of live agents. No significance, superiority or novelty claim was found.
- **The design lock is respected.** Five layers; CUSUM observe-only; attribution audit-only; the calibrator is Platt on the logit; no forbidden construct is present (contract test passes).

## 5. Chapter-level judgement (detail in `FINAL_SUBMISSION_READINESS_REPORT.md`)

| Chapter | Blocking findings for formal submission |
|---|---|
| 1 | C-1, C-5 (title), M-9 |
| 2 | M-1, M-2, M-3 |
| 3 | C-2, C-4, M-1 (equation sources) |
| 4 | M-6, M-8 (both disclosed; decisions SC-2 to SC-4) |
| 5 | C-1, C-2, C-3, C-4, M-4 |
| 6 | Follows from C-1 to C-4; the text itself is consistent with the evidence |
