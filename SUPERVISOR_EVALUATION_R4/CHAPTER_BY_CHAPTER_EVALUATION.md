# Chapter-by-Chapter Evaluation

**Version evaluated:** R4 Markdown sources at commit `9ab3f9e`. These are the sources from which `REM_THESIS_R4.docx` and `.pdf` are built. Every chapter and the front matter were read in full; the hashes are listed in `THESIS_SUPERVISOR_FULL_EVALUATION.md` §2. Line numbers refer to the `chapters_R4/*_R4.md` files.

**Status codes:**
- **ACCEPTABLE**: minor edits only;
- **REVISE**: major corrections needed within the existing scope;
- **NOT ACCEPTABLE**: requires new work.

---

## Front matter (`FRONT_MATTER_R4.md`, 935 words)

| Aspect | Assessment |
|---|---|
| Title | "Runtime Evaluation and Mitigation (REM): A Security Framework for Financial AI Agents". This is broader than the evidence, which comes from one benchmark suite, recorded traces and replay (m-10) |
| Abstract | Accurate and appropriately hedged. It states that there is no live enforcement and that the design values are exploratory |
| Formal pages | **Missing:** student name ("[NAME NOT SUPPLIED]"), university template, approval page, declaration of originality |
| AI use | A factual note (line 46) records the AI coding assistant's role, including "the drafting and verification of this text". The formal declaration is outstanding (C-5) |

**Status: NOT ACCEPTABLE** for submission, because of the formal requirements. The content of the abstract is acceptable.

---

## Chapter 1: Introduction (2,585 words)

**Strengths.**
- The problem is clearly motivated: the action boundary of financial tool calls is a sensible control point, and two open questions are named.
- The scope is explicit (§1.10).
- The RQs are marked [PD], consistent with CLAUDE.md.
- §1.11 separates "achieved / not achieved / not claimed". This is unusually honest.

**Weaknesses.**

| Issue | Location | Severity |
|---|---|---|
| The objectives O1–O3 are quoted from an "approved proposal" that is not available, so they cannot be checked | §1.5–1.6 | CRITICAL (formal; C-5) |
| O1 covers "task automation agents", but only banking is evaluated | §1.5 | MAJOR |
| Gap bullet 2 (no verified quantitative evaluation on financial actions in an open executable benchmark) was not re-assessed after the Kekatos et al. (2026) currency update, and it ignores AgentDojo-evaluated defences | §1.4 | MAJOR (M-5) |
| "None of these elements is new" (§1.8) is honest, but it leaves an exploratory empirical contribution that the evidence then only partly delivers | §1.8 | MAJOR (framing) |
| RQ wording differs from §3.1.3 | §1.7 | MINOR (m-8) |

**Status: REVISE.** Reframe the title, the gap and the objectives so that they match what is evidenced.

---

## Chapter 2: Literature Review (21,892 words; about 45% of the body)

**Strengths.**
- The search procedure is transparent: PRISMA counts are reproduced by script (320 records → 219 screened → 71 included), and verification levels (A / R / U / M) are attached to claims.
- The synthesis is critical, with Established / Uncertain / Under-evaluated / Implication per theme and conflicting evidence presented.
- §2.12 states what the evidence does not support.
- §2.13.5 discusses the risks from prior art.
- §2.13.6 is a currency update that honestly narrows Gaps A and D.

**Weaknesses.**

| Issue | Location | Severity |
|---|---|---|
| A "systematic" review on one index (OpenAlex), screening the top 24–25 records per query; recall of the named prior art 3/13; 31 of 71 studies from prior reading; one AI-assisted reviewer; **no full text read** | §2.2, §2.13.4 | MAJOR (M-4) |
| Gap D is semantic (Progent, Task Shield, CaMeL, MELON and RTBAS report AgentDojo results, which include Banking). The gap verdict "Retained" is too generous | §2.13.2, Table 2.11 | MAJOR (M-5) |
| The closest systems (NEXUS, AgentTrust, PROVISO, TapGuard, ProvenanceGuard) are compared only on design features, at abstract or README level | §2.9, Table 2.9 | MAJOR |
| "ProvenanceGuard … preprint", although the peer-reviewed ASE 2026 version is cited | line 571 | MINOR (m-3) |
| §2.2.7 says numbers come "from the primary report", but no claim reaches level F | §2.2.7 | MINOR (m-5) |
| The Appendix Table 2.8 row for AgentTrust states a level-U ablation result as fact | Table 2.8 | MINOR (m-4) |
| Length: the chapter is about twice the usual proportion | — | MINOR (m-9) |

**Gap verdict:** PARTIALLY SUPPORTED. The gap is narrow, empirical, and established only at record level.

**Status: REVISE.** Searching a second index, reading the full texts of the 10–15 closest works and restating Gap D are required.

---

## Chapter 3: Methodology (13,394 words)

**Strengths.**
- The mathematics is correct throughout (see `ALGORITHM_MATHEMATICAL_AUDIT.md`).
- The λ scale is reconciled explicitly.
- Eqs. 3.8–3.10 are derived correctly.
- The nested grouped cross-fitting is well designed: E0 retention is fold-specific, and no leakage was found in the code.
- The threat model is clear.
- §3.13 and Table 3.16 state the contribution boundaries honestly.
- Table 3.17 gives the provenance of each equation.

**Weaknesses.**

| Issue | Location | Severity |
|---|---|---|
| **Residual false statement:** replay "cannot distinguish step-level from episode-level semantics" | §3.11.11, line 821 | MAJOR (M-3) |
| r_mod is estimated by oracle-Modify replay under NO-ADAPT, which makes it ≈ 0 by construction, and that value is then used in the loss | Eq. 3.5; Proc. 3.1 line 9a; §3.11.7 | MAJOR (M-2) |
| Replay is admitted only by an unapproved amendment | §3.1.4, §3.11.11 | MAJOR (M-1) |
| AS-9 and §3.11.9 promise repeated runs; one run was done | §3.1.5, §3.11.9 | MAJOR (M-7) |
| x_act2 together with a single attacker IBAN acts almost as an attacker-identity proxy, despite design rule 1 (no identity features) | §3.6.2 | MAJOR (M-6) |
| "Bayes verdict": this is a plug-in rule. Acceptable, but it should be stated | §3.7 | MINOR |
| ASR is defined "(enforcing mode)" but only replay exists; the Brier score is withheld but reported in Ch. 5 | §3.12.1–3.12.2 | MINOR (m-6) |
| No cost-independent decision-quality metric (regret, frontier) | §3.12.3 | MAJOR (M-13) |
| Tie order vs the frozen code (SC-2) | Eq. 3.7 | MINOR (m-12) |
| The FV codes in Table 3.17 conflict with the reference register's "no full text in every session" | Table 3.17, line 1001 | MAJOR (R-9, concern) |
| "Exactly five layers, as approved in the research proposal": the proposal is absent | §3.2.1 | Formal (C-5) |

**Status: REVISE.** The method is sound. The design-validity issues (r_mod, Modify ≡ Block, x_act2) and the internal contradictions must be fixed.

---

## Chapter 4: Implementation (4,178 words)

**Strengths.**
- Unit, integration and effectiveness evidence are kept separate.
- Fail-closed configuration.
- The two execution paths are disclosed.
- The limits of the non-invasive placement are stated honestly (§4.9).
- The requirement–equation–function–test table is present.

**Weaknesses.**

| Issue | Location | Severity |
|---|---|---|
| The frozen `RemPipeline` is not the evaluated path; their equivalence is not tested | §4.3, §4.5 | MAJOR (CI-3) |
| x_act2 is reduced to "recipient not in the objective" | I-5, Table 4.4 | MAJOR (CI-4) |
| x_ctx1 classifier absent; reviewer absent; entity extraction partial | §4.3, Table 4.7 | MAJOR (M-10) |
| Step-level Modify withholds the call, so in replay it is equivalent to Block | §4.7 / replay | MAJOR (CI-1) |
| pytest version is 9.1.1 vs 9.2.0; "205 tests" includes 6 build-tooling tests | Table 4.1, §4.15 | MINOR (m-7) |
| The mitigation row of Table 4.6 omits `test_mitigation_semantics` | Table 4.6 | MINOR |

**Classification:** functional experimental implementation, evaluated offline and by replay. It is not a tested end-to-end framework.

**Status: REVISE** (mostly clarifications, plus one equivalence test).

---

## Chapter 5: Results (5,450 words)

**Strengths.**
- The table of evidence kinds (§5.1) is exemplary: recorded, held-out, observe-only, replay, and live = none.
- Every number traces to a file; 126 cells were checked by script, and the headline metrics were reproduced independently by the evaluator.
- Intervals are declared descriptive.
- Negative results are reported plainly:
  - no calibration benefit;
  - behavioural features hurt utility;
  - 93% intervention on legitimate transfers.
- The user_task_15 label problem is investigated, not hidden.

**Weaknesses.**

| Issue | Location | Severity |
|---|---|---|
| **No simple provenance-rule baseline**, and the evaluator's diagnostic shows that such a rule matches REM | §5.5, §5.7 | CRITICAL (C-2) |
| No live enforcement | §5.6 | CRITICAL (C-1) |
| Labels not audited by a human (0/145) | §5.10 | CRITICAL (C-3) |
| The RQ3 Modify / r_mod results are uninformative (circular) | §5.6 | MAJOR (M-2) |
| The ASR difference rests on two single-task categories | Table 5.9 | MAJOR (M-7) |
| Pre-registration: the first execution log was not preserved | §5.2.3 | MAJOR (M-11) |
| Wrong reference "Table 5.12" (should be 5.11); "Three properties", followed by four bullets | lines 188–190 | MINOR (m-1, m-2) |
| B2 and controlled published-defence comparisons are absent | §5.11 | MAJOR (M-8) |

**Status: NOT ACCEPTABLE** without new experiments: at minimum the simple baselines and the human label audit.

---

## Chapter 6: Discussion and Conclusion (2,492 words)

**Strengths.**
- Table 6.1 pairs each conclusion with its support and its limit.
- §6.1.4 states what the evidence does not support: live protection, deployability, superiority.
- §6.4 states that the central practical claim "remains unestablished".
- The limitations (10 items) are comprehensive.
- Future work is ordered by dependency.

**Weaknesses.**

| Issue | Location | Severity |
|---|---|---|
| O3 is marked "partly achieved", but B1 is not an existing approach | Table 6.2 | MAJOR (M-8) |
| O1 is "achieved for the banking setting", while the objective names task-automation agents and the classifier is missing | Table 6.2 | MAJOR |
| The limitations omit the following: the missing provenance-rule baseline; r_mod circularity and Modify ≡ Block; the breadth of the title | §6.5 | MAJOR |
| Contribution 1 cites "205 tests" (199 are REM tests) | §6.4 | MINOR |

**Status: REVISE.** The chapter is honest. It needs to follow the reframing and the new baseline results.

---

## Summary

| Chapter | Status | Dominant issue |
|---|---|---|
| Front matter | NOT ACCEPTABLE | Formal and integrity requirements (C-5) |
| 1 | REVISE | Gap and objective framing vs evidence |
| 2 | REVISE | Literature reach; Gap D |
| 3 | REVISE | r_mod circularity; residual contradiction; feature validity |
| 4 | REVISE | Two execution paths; Modify ≡ Block |
| 5 | NOT ACCEPTABLE | Missing simple baselines; unaudited labels; no live evidence |
| 6 | REVISE | O3 self-assessment; omitted limitations |
