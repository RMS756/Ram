# Prioritized Correction Plan

The steps are ordered by dependency and by impact on the verdict.

**Effort scale:** S ≤ 1 day; M ≤ 1 week; L > 1 week.

**Owner:**
- **St** = student;
- **Sup** = supervisor;
- **St+AI** = the student, who may use tooling but must verify the result and declare its use.

Nothing in this plan should be done by silently choosing design values. Items that need a decision under CLAUDE.md are marked **[SUPERVISOR DECISION REQUIRED]**.

## Phase 0: Formal and governance prerequisites (blocks everything else)

| # | Action | Issue | Owner | Effort |
|---|---|---|---|---|
| 0.1 | Attach the approved proposal. Reconcile O1–O3 and the RQs with it, and freeze the RQ wording (remove the [PD] marks only after approval) | C-5, m-8 | St, Sup | S |
| 0.2 | Decide the open design items: costs and tiers (D-9), predicates, the feature set, the label rule, the mitigation semantics (D-2/SC-1), the tie rule (SC-2), the Brier convention (SC-5), the replay amendment (D-1/SC-7), and SD-FREEZE. **[SUPERVISOR DECISION REQUIRED]** | C-4, M-1 | Sup | M |
| 0.3 | Decide on LLM access for live runs (D-15). If none is possible, formally **re-scope** the thesis to an offline/replay decision-analysis study. **[SUPERVISOR DECISION REQUIRED]** | C-1 | Sup | S |
| 0.4 | Add the student's name, the university template, and the approval and originality pages. Complete the **formal declaration of AI use** and describe the student's own contribution | C-5 | St | S |

## Phase 1: Evidence that decides whether there is a contribution

| # | Action | Issue | Owner | Effort |
|---|---|---|---|---|
| 1.1 | Add **simple baselines** to the existing replay harness, held to the same protocol as REM: (a) intervene iff x_act1 = 1 on tier ≥ 2; (b) x_act1 ∨ x_act2; (c) B2 detection-only. Report ASR, benign utility and utility under attack with paired intervals | C-2, M-8 | St+AI | S–M |
| 1.2 | Run the **human label audit**: the 145-item package with two annotators. Report κ and re-estimate RQ1–RQ3 on the audited labels. Resolve user_task_15 | C-3 | St (+ second annotator) | M |
| 1.3 | Replace the circular r_mod. Either implement a **real Modify** (for example, substituting the argument from trusted context), which needs a design decision, or state that Modify is a costed variant of Block in replay and drop the claims about Modify residuals. **[SUPERVISOR DECISION REQUIRED]** for a new mechanism | M-2, CI-1 | St, Sup | M |
| 1.4 | Add a **cost-independent** analysis: ASR–utility frontiers across a cost sweep for REM, B1 and the rule baselines, and/or regret against an oracle policy. Make the sweep the primary decision result | M-13, C-4 | St+AI | M |
| 1.5 | Write a **robustness probe** for the near-oracle feature. Perturb the attacker destinations (encoded, split, paraphrased, or routed through trusted-looking content) in replay, and report how x_act1, REM and the rule degrade | M-6, CI-4, CI-5 | St+AI | M |

## Phase 2: Evidence that supports the practical claim (needs the decision in 0.3)

| # | Action | Issue | Owner | Effort |
|---|---|---|---|---|
| 2.1 | Run **live enforcement** with the existing protocol (`experiments/live/`): one or two open-weight backbones, at least 3 repeats, B0/B1/REM and the best rule baseline | C-1, AS-9, M-7 | St | L |
| 2.2 | Run at least **one controlled comparison with a published defence** (for example, a PI detector or a tool filter from AgentDojo), with the same backbones and tasks | M-8 (O3) | St | M–L |
| 2.3 | Add a second attack family or environment (another AgentDojo attack, or an adaptive attack) | M-5, M-6 | St | M–L |

## Phase 3: Text corrections (after Phases 1–2)

| # | Action | Issue | Owner | Effort |
|---|---|---|---|---|
| 3.1 | Correct Ch. 3 §3.11.11, line 821 ("cannot distinguish step-level from episode-level semantics") | M-3 | St | S |
| 3.2 | Correct Ch. 5 line 190 ("Table 5.12", which should be 5.11) and line 188 ("Three properties", followed by four bullets). Extend the trace checker to cross-references | m-1, m-2 | St+AI | S |
| 3.3 | Retitle, and reframe the contribution as an empirical study. Restate Gap D. Mark O3 as not achieved unless 2.2 is done. Add the missing limitations: the rule baseline, r_mod/Modify, title breadth | m-10, M-5, M-8 | St | M |
| 3.4 | Chapter 2: search a second index (for example, Scopus, IEEE Xplore or ACM DL); read the full texts of the 10–15 closest works; fix "preprint" (line 571) and the level-U fact in Table 2.8; shorten the chapter by about 30% | M-4, m-3, m-4, m-9 | St | L |
| 3.5 | Obtain and read the equation sources coded IV or NC, and Platt (2000). Reconcile the FV codes of Table 3.17 with the reference register, or downgrade them. Complete the 21 PARTIAL entries | M-12, R-1, R-9 | St | M |
| 3.6 | Fix Ch. 3 §3.12.1 (ASR "enforcing mode"), the Brier convention, Ch. 4 Table 4.1 (pytest version), and the test count (199 REM tests + 6 tooling) | m-6, m-7 | St | S |
| 3.7 | Add an equivalence test between `RemPipeline` and the evaluated path, or limit the claims to the evaluated path. Check `converged` | CI-2, CI-3 | St+AI | S |
| 3.8 | Remove or archive the superseded chapter generations, and make the authoritative branch the default | m-13 | St | S |

## Phase 4: Integrity and submission

| # | Action | Issue | Owner | Effort |
|---|---|---|---|---|
| 4.1 | Run the institution's **similarity check** on the final text, and address any matches | C-5 | St, Sup | S |
| 4.2 | Have an **independent human** pre-examination. This AI-produced evaluation is not independent | Conflict of interest | Sup | M |
| 4.3 | Rebuild the DOCX/PDF from the corrected sources; re-run the tests, the equation checks and the tracing; record the hashes | — | St+AI | S |

## Minimum path to a defensible thesis

**If live runs are impossible:** 0.1–0.4 → 1.1–1.5 → 3.1–3.8 → 4.1–4.3. The thesis is then submitted as an offline decision-analysis study with a narrowed title and claims.

**With live access:** add 2.1–2.3. This is the only path that can support a protection claim.
