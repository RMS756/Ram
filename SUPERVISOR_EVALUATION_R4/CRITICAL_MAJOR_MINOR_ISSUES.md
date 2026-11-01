# Critical, Major and Minor Issues

**Thesis evaluated:** R4, branch `claude/rem-r4-corrections-3ktvze`, commit `9ab3f9e`. The chapter sources are `REM_FINAL_THESIS/chapters_R4/*_R4.md`; the PDF is `REM_FINAL_THESIS/R4/REM_THESIS_R4.pdf` (212 pages).

**Evaluator's conflict of interest.** The thesis text, code and earlier verification reports were produced in sessions of the same AI assistant that wrote this evaluation; every commit in the repository is authored by it. This evaluation is therefore **not independent**. An independent human examination is required before any decision is taken on it.

**How to read this register.**
- *Severity:* CRITICAL blocks submission and defence; MAJOR must be corrected or justified; MINOR concerns presentation or consistency.
- *Basis:* **V** = verified by the evaluator, from the file or a command run on 1 Nov 2026; **D** = disclosed by the thesis itself and confirmed; **C** = a concern needing further investigation.

## CRITICAL

| ID | Issue | Location | Evidence | Basis |
|---|---|---|---|---|
| C-1 | **The central claim is untested.** The practical claim is that tier-indexed expected-loss verdicts reduce harm at acceptable utility cost. It has no enforcing-mode evidence from live agents. Every enforcement number comes from replay under NO-ADAPT, where a refused call cannot recur | Ch. 5 §5.1, §5.6; Ch. 6 §6.4 ("remains unestablished") | `results/pilot_R2/e4_e5_enforcement_replay.json`; `experiments/live/LIVE_EVALUATION_PROTOCOL.md` (NOT EXECUTED) | D, V |
| C-2 | **A one-line provenance rule matches REM's attack interception with fewer false interventions.** "Intervene on a state-changing call iff x_act1 = 1" intervenes on 97.1% of attack steps and 14.7% of legitimate steps, and releases 92 of 180 benign state-changing steps. REM's figures are 97.3%, 22.7% and 33/180. The thesis neither tests nor discusses such a baseline, so the value added by the estimator, calibration and expected-loss layers is **not demonstrated** in this benchmark | Ch. 5 §5.5, §5.7 (Table 5.12: only action evidence matters); Ch. 6 §6.4 | Evaluator diagnostic, observe-only, on the R4 re-run data (`data.steps`, 6,762 steps). The rule has no fitted parameters, so no cross-fitting is needed. It was not replayed and is not part of the thesis | V |
| C-3 | **The labels are an unaudited proxy.** Labels come from reference matching. The user_task_15 collision affects 16 of 21 backbones, and all of REM's residual replay ASR comes from those ambiguous episodes. The human audit package has 145 items and **0 annotations**; the only inspection was by the AI assistant | Ch. 3 §3.11.3; Ch. 5 §5.10 | `results/pilot_R2/label_audit_human_package.csv`; `REM_FINAL_THESIS/verification/label_audit_package_check_R4.json` | D, V |
| C-4 | **The design values are not approved.** Costs (C_miss = 1/5/10/20 by tier, C_FA = 1, C_mod = 0.5, C_esc = 0.3), the tier map, the predicates, the feature set and the label rule are declared exploratory values. Every decision result depends on them; at tier 4 the costs put the Allow–Block threshold at 1/21 | Ch. 5 Table 5.1; Ch. 6 §6.5 item 1 | `configs/exploratory/pilot_e0.yaml`; `SUPERVISOR_DECISIONS_REQUIRED.md` (D-9, SD-FREEZE) | D |
| C-5 | **Formal and academic-integrity requirements are unmet.** There is no approved title, no student name, no university template, and no approval or declaration pages. The approved proposal is absent, so the objectives quoted in Ch. 1 and Ch. 3 cannot be checked. For text largely drafted by an AI system, the front matter (line 46) gives only a factual note on the AI coding assistant's role, and states that it "is a factual record, not that declaration". The university's formal declaration of AI use has not been made. No plagiarism or similarity check was found | Front matter; Ch. 1 §1.5–1.6; Ch. 3 §3.1.2 | `FRONT_MATTER_R4.md` ("[NAME NOT SUPPLIED]"); repository history | V |

## MAJOR

| ID | Issue | Location | Evidence | Basis |
|---|---|---|---|---|
| M-1 | **Replay lies outside the approved methodology.** The amendment that admits replay (§3.11.11) is unapproved (D-1) | Ch. 3 §3.1.4, §3.11.11 | Register D-1 / SC-7 | D |
| M-2 | **r_mod is circular.** The residual rate after Modify enters the loss (Eq. 3.5), but it is "measured" by oracle-Modify replay under NO-ADAPT, so it is ≈ 0 by construction (0.000 at tier 3 and 0.010 at tier 4). That assumption-driven value then shapes the verdict mix: Modify is chosen for 615 of the 907 attack steps in replay | Ch. 3 Eq. 3.5, Proc. 3.1 line 9a, §3.11.7; Ch. 5 §5.6 RQ3 | `e4_rmod_and_replay_validity.json`; `configs.REM_step_level_no_reviewer.verdict_rates` | V |
| M-3 | **Residual false statement in R4.** Ch. 3 §3.11.11 still says replay results "cannot distinguish step-level from episode-level semantics". This contradicts Ch. 3 §3.8, Ch. 5 Table 5.11 and the stored results. The R4 correction log marks the invariance claim as removed everywhere | `CHAPTER3_METHODOLOGY_R4.md` line 821 | `grep "cannot distinguish"` | V |
| M-4 | **The literature review is narrow in reach.** One index (OpenAlex) was searched. The top 24–25 records per query were screened. Recall of the 13 named prior-art studies was 3/13. 31 of 71 included studies came from the author's earlier reading. No full text was read, and screening was by one AI-assisted reviewer | Ch. 2 §2.2, §2.13.4 | `chapter2/slr/prisma_counts.json` (reproduced) | D, V |
| M-5 | **The gap is narrow and partly semantic.** Gap D ("no verified quantitative evaluation … on financial actions in an open executable benchmark") overlooks the many defences evaluated on AgentDojo, whose suites include Banking (Progent, Task Shield, CaMeL, RTBAS, MELON). What is missing is only a finance-specific breakdown. Kekatos et al. (2026) already evaluate offline on AgentDojo's recorded traces, and PROVISO (Yan et al.) and TapGuard (Xin) narrow Gap A | Ch. 1 §1.4; Ch. 2 §2.13.2, §2.13.6 | Ch. 2 Table 2.5; currency update | V |
| M-6 | **The benchmark structure may inflate action evidence.** One attacker IBAN appears only in injected content. x_act2 was reduced in implementation to "recipient not in the objective" (Ch. 4 I-5). x_act1 is therefore close to an oracle in this benchmark (see C-2) | Ch. 3 §3.6.2; Ch. 4 Table 4.4; Ch. 6 Table 6.1 row 2 | Feature definitions; diagnostic | V |
| M-7 | **Statistics.** Nine attacked groups; one run per configuration (AS-9 and §3.11.9 unmet); no multiplicity correction; the ASR difference is concentrated in two single-task categories | Ch. 3 §3.11.9, §3.14; Ch. 5 §5.2, Table 5.9 | — | D |
| M-8 | **O3 is essentially unmet.** No controlled comparison with an existing published defence was made. B1 is an internal same-estimator baseline; B2 (detection-only) was not run; the distributed defences are uncontrolled. Ch. 6 calls O3 "partly achieved" | Ch. 6 Table 6.2; Ch. 3 §3.11.7 | — | V |
| M-9 | **The configuration as evaluated is practically unusable without a reviewer.** It intervenes on 93% of legitimate transfers ≤ 1000. Benign utility on state-changing tasks is 0.168 against 0.472 with no defence | Ch. 5 Tables 5.6, 5.10 | `r2_breakdowns.json` | D |
| M-10 | **Components are absent.** The injection classifier x_ctx1 is missing, so the Detection layer reduces to a regex indicator written with knowledge of the benchmark. There is no human reviewer. The frozen `RemPipeline` is not the evaluated path | Ch. 4 §4.3, §4.5, Table 4.7 | Code | D, V |
| M-11 | **Pre-registration evidence is incomplete.** The log of the first execution was not preserved, so the order of amendments relative to the first results rests on commit times and the session record | Ch. 5 §5.2.3 | — | D |
| M-12 | **Seven equation sources were never read in full.** Eqs. 3.1–3.3, 3.9, 3.10, 3.15 and 3.16 rest on sources coded IV or NC, including Platt, which was never read | Ch. 3 Table 3.17 | `SOURCE_VERIFICATION_LOG_R4.md` | D |
| M-13 | **No cost-independent decision-quality metric.** Realized loss favours REM by construction. There is no regret against an oracle or matched policy, and no elicited cost validation | Ch. 3 §3.12.3; Ch. 5 §5.9 | — | V |

## MINOR

| ID | Issue | Location | Basis |
|---|---|---|---|
| m-1 | Ch. 5 §5.6 says "Table 5.12 compares both semantics"; it should be Table 5.11 (5.12 is the ablation table). This is a renumbering error introduced in R4 | `CHAPTER5_RESULTS_R4.md` line 190 | V |
| m-2 | Ch. 5 §5.6: "Three properties limit what it can show", followed by four bullets | line 188 | V |
| m-3 | Ch. 2 §2.6.5 calls ProvenanceGuard a "preprint"; the reference list cites the peer-reviewed ASE 2026 version (confirmed via Crossref) | Ch. 2 line 571 | V |
| m-4 | The Appendix 2A row for AgentTrust states the level-U session-tracker ablation as fact | Ch. 2 Table 2.8 | V |
| m-5 | Ch. 2 §2.2.7 says numbers come from "the primary report", but no claim reaches level F | Ch. 2 | V |
| m-6 | Ch. 3 §3.12.1 defines ASR "(enforcing mode)"; only replay was used. §3.12.2 withholds the Brier score, but Ch. 5 reports it (SC-5) | Ch. 3, Ch. 5 Table 5.3 | V |
| m-7 | Ch. 4 Table 4.1 gives pytest 9.1.1; the R4 log records 9.2.0. "205 tests" includes 6 thesis-build tests; 199 test REM | Ch. 4 | V |
| m-8 | RQ wording differs between Ch. 1 and Ch. 3 (RQ2 metric list; "processing time" vs "latency") | §1.7 vs §3.1.3 | V |
| m-9 | Ch. 2 is 21.9k words (≈ 45% of the body) | Ch. 2 | V |
| m-10 | The title ("A Security Framework for Financial AI Agents") is broader than the evidence: one benchmark, recorded traces | Title page | V |
| m-11 | The ridge Newton solver has no line search, and its `converged` flag is never checked | `rem/algorithms/detection/ridge_logistic.py` | V |
| m-12 | The tie rule (Ch. 3 order) differs from the frozen code (raises); SC-2 is unresolved. No ties occurred | Ch. 3 Eq. 3.7; Ch. 4 §4.7 | D |
| m-13 | Four superseded generations of chapters remain in the repository (`thesis/`, `revision_R2/`, `REM_STAGE2_OUTPUT/THESIS_COMPLETION/`, `REM_FINAL_THESIS/chapters/`), and the default branch still points to R3. This risks confusion about which version is authoritative | Repository | V |
